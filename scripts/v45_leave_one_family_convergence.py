#!/usr/bin/env python3
"""Leave-one-source-family-out APC/HLA/IFN convergence check.

Uses the V45 weighted/collapsed null envelopes as fixed references. This tests
whether one artifact family is carrying the recurrence signal.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v45_convergence_sensitivity import (
    OUT as SENS_OUT,
    TARGET,
    collapsed_scores,
    positive_units,
    source_family,
    weighted_scores,
)


ROOT = Path(__file__).resolve().parents[1]
V41 = ROOT / "analysis" / "v41_joint_inference"
OUT = ROOT / "analysis" / "v45_convergence_family_jackknife"
OUT.mkdir(parents=True, exist_ok=True)


def target_rank(scores: pd.Series) -> int | None:
    if TARGET not in scores.index:
        return None
    return int(scores.rank(ascending=False, method="min").get(TARGET))


def main() -> int:
    evidence = pd.read_csv(V41 / "integrated_evidence_frame.tsv", sep="\t")
    units = positive_units(evidence)
    nulls = pd.read_csv(SENS_OUT / "convergence_sensitivity_null_summary.tsv", sep="\t")
    p99 = nulls.set_index("sensitivity")["max_null_p99"].to_dict()
    families = sorted(units["source_family"].dropna().unique().tolist())
    rows = []
    for family in families:
        sub = units[units["source_family"] != family].copy()
        weighted = weighted_scores(sub)
        modfam = collapsed_scores(sub, "modality_family_unit")
        family_collapsed = collapsed_scores(sub, "source_family")
        removed = units[units["source_family"].eq(family)]
        rows.append(
            {
                "removed_source_family": family,
                "removed_total_source_units": int(removed["source_unit"].nunique()),
                "removed_target_source_units": int(removed[removed["entity"].eq(TARGET)]["source_unit"].nunique()),
                "weighted_target": float(weighted.get(TARGET, 0.0)),
                "weighted_rank": target_rank(weighted),
                "weighted_above_v45_p99": bool(float(weighted.get(TARGET, 0.0)) > float(p99["source_file_weighted"])),
                "modality_family_target": int(modfam.get(TARGET, 0)),
                "modality_family_rank": target_rank(modfam),
                "modality_family_above_v45_p99": bool(float(modfam.get(TARGET, 0)) > float(p99["modality_source_family_collapsed"])),
                "source_family_target": int(family_collapsed.get(TARGET, 0)),
                "source_family_rank": target_rank(family_collapsed),
                "source_family_above_v45_p99": bool(float(family_collapsed.get(TARGET, 0)) > float(p99["source_family_collapsed"])),
            }
        )
    result = pd.DataFrame(rows).sort_values("removed_target_source_units", ascending=False)
    result.to_csv(OUT / "leave_one_source_family_out.tsv", sep="\t", index=False)
    summary = {
        "target": TARGET,
        "source_families_tested": int(len(result)),
        "min_weighted_target": float(result["weighted_target"].min()),
        "min_modality_family_target": int(result["modality_family_target"].min()),
        "min_source_family_target": int(result["source_family_target"].min()),
        "all_weighted_above_v45_p99": bool(result["weighted_above_v45_p99"].all()),
        "all_modality_family_above_v45_p99": bool(result["modality_family_above_v45_p99"].all()),
        "all_source_family_above_v45_p99": bool(result["source_family_above_v45_p99"].all()),
        "worst_removed_by_target_units": result.head(5).to_dict(orient="records"),
        "interpretation": (
            "APC/HLA/IFN convergence is not carried by any single source family "
            "if all three above-p99 flags remain true for every leave-one-family "
            "removal."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

