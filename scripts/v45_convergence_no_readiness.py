#!/usr/bin/env python3
"""APC/HLA/IFN convergence sensitivity excluding post-V42 readiness rows.

This tests a narrow circularity question: whether V41/V45 convergence evidence
depends on validation-readiness artifacts generated after the V42
pre-registration. The expected correct result may be zero excluded rows if the
V41 integrated frame was not rebuilt from those later artifacts.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from v45_convergence_sensitivity import (
    TARGET,
    collapsed_null,
    collapsed_scores,
    pvals,
    positive_units,
    weighted_null,
    weighted_scores,
)


ROOT = Path(__file__).resolve().parents[1]
V41 = ROOT / "analysis" / "v41_joint_inference"
OUT = ROOT / "analysis" / "v45_convergence_no_readiness"
OUT.mkdir(parents=True, exist_ok=True)

SEED = 45945
N_REPS = 20000


POST_V42_PREFIXES = (
    "analysis/v43_",
    "analysis/v44_",
    "analysis/v45_",
    "docs/validation/",
)
READINESS_TOKENS = (
    "PREREGISTRATION",
    "VALIDATION_READINESS",
    "OUTCOME_INTERPRETATION",
    "POWER_MAP",
    "HARNESS",
    "ROBUSTNESS",
    "BATCH_GUARD",
    "COHORT_SPEC",
    "KAROLINSKA",
    "GSE228330",
    "PREFLIGHT",
)


def readiness_mask(evidence: pd.DataFrame) -> pd.Series:
    source = evidence["source_file"].astype(str)
    upper = source.str.upper()
    by_prefix = source.map(lambda s: any(s.startswith(prefix) for prefix in POST_V42_PREFIXES))
    by_token = upper.map(lambda s: any(token in s for token in READINESS_TOKENS))
    return by_prefix | by_token


def recurrence_rows(units: pd.DataFrame, entities: list[str], rng: np.random.Generator) -> list[dict[str, object]]:
    weighted = weighted_scores(units)
    weighted.to_frame("source_file_weighted_recurrence_no_readiness").reset_index().to_csv(
        OUT / "source_file_weighted_recurrence_no_readiness.tsv", sep="\t", index=False
    )
    w_max, w_target = weighted_null(units, entities, rng)
    weighted_observed = float(weighted.get(TARGET, 0.0))
    rows = [
        {
            "sensitivity": "source_file_weighted_no_readiness",
            "observed_target": weighted_observed,
            "observed_target_rank": int(weighted.rank(ascending=False, method="min").get(TARGET, np.nan)),
            "n_reps": N_REPS,
            **pvals(weighted_observed, w_max, w_target),
        }
    ]

    for collapse_col, label in [
        ("modality_family_unit", "modality_source_family_collapsed_no_readiness"),
        ("source_family", "source_family_collapsed_no_readiness"),
    ]:
        collapsed = collapsed_scores(units, collapse_col)
        collapsed.to_frame(f"{label}_recurrence").reset_index().to_csv(
            OUT / f"{label}_recurrence.tsv", sep="\t", index=False
        )
        c_max, c_target = collapsed_null(units, entities, collapse_col, rng)
        observed = float(collapsed.get(TARGET, 0))
        rows.append(
            {
                "sensitivity": label,
                "observed_target": observed,
                "observed_target_rank": int(collapsed.rank(ascending=False, method="min").get(TARGET, np.nan)),
                "n_reps": N_REPS,
                **pvals(observed, c_max, c_target),
            }
        )
    return rows


def main() -> int:
    evidence = pd.read_csv(V41 / "integrated_evidence_frame.tsv", sep="\t")
    mask = readiness_mask(evidence)
    filtered = evidence[~mask].copy()
    units = positive_units(filtered)
    entities = sorted(evidence["entity"].unique().tolist())
    rng = np.random.default_rng(SEED)

    rows = recurrence_rows(units, entities, rng)
    null_summary = pd.DataFrame(rows)
    null_summary.to_csv(OUT / "convergence_no_readiness_null_summary.tsv", sep="\t", index=False)

    excluded = (
        evidence.loc[mask]
        .groupby(["modality", "source_file"], as_index=False)
        .size()
        .sort_values("size", ascending=False)
    )
    excluded.to_csv(OUT / "excluded_readiness_rows.tsv", sep="\t", index=False)

    target_breakdown = (
        units[units["entity"].eq(TARGET)]
        .groupby(["source_family", "modality"], as_index=False)
        .agg(source_units=("source_unit", "nunique"))
        .sort_values("source_units", ascending=False)
    )
    target_breakdown.to_csv(OUT / "target_source_family_breakdown_no_readiness.tsv", sep="\t", index=False)

    source_audit = (
        evidence.groupby(["modality", "source_file"], as_index=False)
        .size()
        .sort_values(["source_file", "modality"])
    )
    source_audit.to_csv(OUT / "all_source_files_audited.tsv", sep="\t", index=False)

    summary = {
        "target": TARGET,
        "seed": SEED,
        "n_reps": N_REPS,
        "n_rows_original": int(len(evidence)),
        "n_rows_excluded_readiness": int(mask.sum()),
        "n_rows_filtered": int(len(filtered)),
        "n_positive_units_filtered": int(units["source_unit"].nunique()),
        "target_source_file_weighted_observed": float(rows[0]["observed_target"]),
        "target_source_file_weighted_rank": int(rows[0]["observed_target_rank"]),
        "target_source_file_weighted_fwer_p": float(rows[0]["target_fwer_p"]),
        "target_modality_family_observed": float(rows[1]["observed_target"]),
        "target_modality_family_rank": int(rows[1]["observed_target_rank"]),
        "target_modality_family_fwer_p": float(rows[1]["target_fwer_p"]),
        "target_source_family_observed": float(rows[2]["observed_target"]),
        "target_source_family_rank": int(rows[2]["observed_target_rank"]),
        "target_source_family_fwer_p": float(rows[2]["target_fwer_p"]),
        "interpretation": (
            "If n_rows_excluded_readiness is zero, the V41 integrated frame "
            "contains no post-V42 readiness rows; readiness-document circularity "
            "is absent in this convergence object. If rows are excluded, the "
            "target must remain rank 1 and FWER p < 0.05."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
