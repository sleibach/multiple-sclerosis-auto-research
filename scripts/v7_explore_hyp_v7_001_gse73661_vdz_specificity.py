#!/usr/bin/env python3
"""Exploratory specificity check for HYP_V7_001 in GSE73661 vedolizumab arms.

This is not counted as locked V7 validation because vedolizumab is Class C under
docs/locked_rules/LOCKED_RULE_V7.md. It asks whether the IBD IFN/APC downshift is anti-TNF-like
or a generic mucosal response/healing signal.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd

from v7_apply_locked_rule_affy_validation import (
    ROOT,
    evaluate_scores,
    load_scored_soft,
    zscore_modules,
)


OUT = ROOT / "analysis" / "v7_hyp_v7_001_specificity"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta, gene_expr, map_rows = load_scored_soft("GSE73661")
    rows = []
    response_by_patient: dict[str, int] = {}
    for _, row in meta.iterrows():
        chars = row.get("characteristics", {})
        therapy = str(chars.get("induction therapy_maintenance therapy", ""))
        week = str(chars.get("week (w)", ""))
        patient = str(chars.get("study individual number", ""))
        title = str(row.get("title", ""))
        if therapy not in {"vdz_vdz4w", "vdz_vdz8w"} or week not in {"W0", "W6"} or not patient:
            continue
        if week == "W6":
            if "_UC R " in title:
                response_by_patient[patient] = 1
            elif "_UC NR " in title:
                response_by_patient[patient] = 0
        rows.append({"sample": row["sample"], "patient": patient, "timepoint": "baseline" if week == "W0" else "post", "therapy": therapy, "title": title})

    sample_ids = [row["sample"] for row in rows]
    scores = zscore_modules(gene_expr, sample_ids)
    sample_df = pd.DataFrame(rows).merge(scores, left_on="sample", right_index=True)
    sample_df["response"] = sample_df["patient"].map(response_by_patient)
    wide = sample_df.dropna(subset=["response"]).pivot_table(index=["patient", "response"], columns="timepoint", values=["ifn_apc", "receptor"], aggfunc="mean")
    records = []
    for (patient, response), row in wide.iterrows():
        if ("ifn_apc", "baseline") not in row.index or ("ifn_apc", "post") not in row.index:
            continue
        records.append(
            {
                "patient": patient,
                "response": int(response),
                "delta_ifn_apc": float(row[("ifn_apc", "post")] - row[("ifn_apc", "baseline")]),
                "delta_receptor": float(row[("receptor", "post")] - row[("receptor", "baseline")]) if ("receptor", "baseline") in row.index and ("receptor", "post") in row.index else math.nan,
            }
        )
    paired = pd.DataFrame(records)
    paired["locked_like_score"] = -1.0 * paired["delta_ifn_apc"]
    paired["locked_score"] = paired["locked_like_score"]
    paired["receptor_score"] = -1.0 * paired["delta_receptor"]
    result = evaluate_scores(
        cohort="GSE73661_VDZ_W6_exploratory",
        disease="UC",
        therapy="vedolizumab",
        therapy_class="Class C exploratory",
        feature="-delta_IFN_APC",
        df=paired,
        notes="Exploratory Class C vedolizumab W0-to-W6 mucosal response check; not counted as locked V7 validation.",
    )
    paired.to_csv(OUT / "gse73661_vdz_w6_scores.tsv", sep="\t", index=False)
    (OUT / "gse73661_vdz_w6_result.json").write_text(json.dumps(result.__dict__, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = f"""# HYP_V7_001 Specificity Check: GSE73661 Vedolizumab

This is exploratory and not counted as locked V7 validation because
vedolizumab is Class C in `docs/locked_rules/LOCKED_RULE_V7.md`.

| Metric | Value |
| --- | --- |
| N | {result.n_labeled} |
| AUC | {result.auc:.3f} |
| AUC 95% CI | {result.auc_ci_low:.3f}-{result.auc_ci_high:.3f} |
| Hedges g | {result.hedges_g:.3f} |
| Welch p | {result.p_value:.4g} |
| Receptor-only AUC | {result.receptor_auc:.3f} |
| Pass/fail under locked thresholds | {result.pass_fail} |

Interpretation: if this looks similar to the infliximab arms, the IFN/APC
downshift may be generic mucosal healing biology rather than anti-TNF-specific
architecture.
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
