#!/usr/bin/env python3
"""Consolidate V22/V36 held-cohort therapy-branch evidence."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_therapy_branch_map"


def finite(value: object) -> float:
    try:
        out = float(value)
    except Exception:
        return float("nan")
    return out


def add_row(rows: list[dict[str, object]], **kwargs: object) -> None:
    rows.append(kwargs)


def feature_branch(feature: str) -> str:
    f = feature.lower()
    if "hla" in f:
        return "HLA-II competence/induction"
    if "receptor" in f or "cd74" in f:
        return "CD74/receptor-state dynamics"
    if "ifn" in f or "stat1" in f or "locked" in f:
        return "IFN/APC/STAT1 dynamics"
    if "glycolysis" in f:
        return "metabolic/glycolysis-coupled"
    return "other"


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    clean = df.copy()
    for col in clean.columns:
        clean[col] = clean[col].map(lambda x: f"{x:.4g}" if isinstance(x, float) and np.isfinite(x) else x)
    header = "| " + " | ".join(clean.columns.astype(str)) + " |"
    sep = "| " + " | ".join(["---"] * len(clean.columns)) + " |"
    rows = ["| " + " | ".join(str(x) for x in row) + " |" for row in clean.to_numpy()]
    return "\n".join([header, sep, *rows])


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []

    ms_dmt = pd.read_csv(ROOT / "analysis/v22_locked_apc_hla_validation/validation_ledger_v22_ms_dmt.tsv", sep="\t")
    for _, row in ms_dmt.iterrows():
        add_row(
            rows,
            source_table="validation_ledger_v22_ms_dmt",
            cohort=row["cohort"],
            disease=row["disease"],
            therapy=row["therapy"],
            context="locked V22/V23 MS DMT validation",
            candidate_feature=row["feature_applied"],
            branch="locked scalar",
            auc=finite(row["auc"]),
            p_value=finite(row.get("welch_p", np.nan)),
            effect=finite(row.get("hedges_g", np.nan)),
            status=row["pass_fail"],
            caveat="small held cohort; primary rule pre-specified",
        )

    cross = pd.read_csv(ROOT / "analysis/v22_locked_apc_hla_validation/validation_ledger_v22_cross_disease.tsv", sep="\t")
    for _, row in cross.iterrows():
        add_row(
            rows,
            source_table="validation_ledger_v22_cross_disease",
            cohort=row["cohort"],
            disease=row["disease"],
            therapy=row["therapy"],
            context="locked V22 cross-disease stress",
            candidate_feature=row["feature_applied"],
            branch="locked scalar",
            auc=finite(row["auc"]),
            p_value=finite(row.get("welch_p", np.nan)),
            effect=finite(row.get("hedges_g", np.nan)),
            status=row["pass_fail"],
            caveat="cross-disease; tofacitinib exact all-cell approximation caveated",
        )

    mtx = pd.read_csv(ROOT / "analysis/v36_gse85034_mtx_stress/gse85034_mtx_feature_tests.tsv", sep="\t")
    for _, row in mtx.sort_values("auc_high_score_response", ascending=False).head(2).iterrows():
        add_row(
            rows,
            source_table="gse85034_mtx_feature_tests",
            cohort="GSE85034_MTX",
            disease="psoriasis",
            therapy="methotrexate",
            context="out-of-domain skin stress test",
            candidate_feature=row["feature"],
            branch=feature_branch(str(row["feature"])),
            auc=finite(row["auc_high_score_response"]),
            p_value=finite(row["exact_auc_p"]),
            effect=finite(row["hedges_g_responder_minus_non"]),
            status="post_hoc_stress_only",
            caveat="not bounded validation domain; 3 responders",
        )

    ifnb_long = pd.read_csv(ROOT / "analysis/v36_ms_ifnb_longitudinal_audit/gse24427_ifnb_timepoint_tests.tsv", sep="\t")
    for _, row in ifnb_long.sort_values("auc_high_score_relapse_free", ascending=False).head(3).iterrows():
        add_row(
            rows,
            source_table="gse24427_ifnb_timepoint_tests",
            cohort=f"GSE24427_{row['timepoint']}",
            disease="MS",
            therapy="interferon-beta",
            context="longitudinal relapse-free timing audit",
            candidate_feature=row["feature"],
            branch=feature_branch(str(row["feature"])),
            auc=finite(row["auc_high_score_relapse_free"]),
            p_value=finite(row["auc_permutation_p"]),
            effect=finite(row["hedges_g_relapsefree_minus_relapsed"]),
            status="exploratory_context",
            caveat="older IFN-beta cohort; therapy-specific branch only",
        )

    ifnb_dose = pd.read_csv(ROOT / "analysis/v36_ms_ifnb_dose_hour_audit/gse138064_ifnb_dose_hour_tests.tsv", sep="\t")
    for _, row in ifnb_dose.sort_values("auc_high_score_complete", ascending=False).head(5).iterrows():
        add_row(
            rows,
            source_table="gse138064_ifnb_dose_hour_tests",
            cohort=f"GSE138064_{row['subset']}",
            disease="MS",
            therapy="interferon-beta",
            context="dose/hour complete-vs-partial responder audit",
            candidate_feature=row["feature"],
            branch=feature_branch(str(row["feature"])),
            auc=finite(row["auc_high_score_complete"]),
            p_value=finite(row["auc_permutation_p"]),
            effect=finite(row["hedges_g_complete_minus_partial"]),
            status="exploratory_context",
            caveat="complete-vs-partial labels; repeated dose/hour rows",
        )

    branch = pd.DataFrame(rows)
    branch.to_csv(OUT / "therapy_branch_evidence.tsv", sep="\t", index=False)
    summary_counts = (
        branch.groupby(["therapy", "branch"], dropna=False)
        .agg(n_rows=("cohort", "count"), max_auc=("auc", "max"), min_p=("p_value", "min"))
        .reset_index()
        .sort_values(["therapy", "branch"])
    )
    summary_counts.to_csv(OUT / "therapy_branch_summary.tsv", sep="\t", index=False)

    interpretation = {
        "primary_validation_target": "locked V22/V23 bounded monitoring rule",
        "branch_summary": summary_counts.to_dict("records"),
        "main_readout": "IFN-beta held artifacts repeatedly emphasize HLA-II competence and CD74/receptor dynamics, whereas tofacitinib emphasizes IFN/APC/STAT1 downshift; MTX/ADA psoriasis skin are out-of-domain and do not support a universal scalar.",
    }
    (OUT / "summary.json").write_text(json.dumps(interpretation, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = [
        "# V36 Therapy-Branch Evidence Map",
        "",
        "This table consolidates held V22/V36 evidence by therapy context. It does",
        "not change locked rules; it clarifies which secondary branch should be",
        "reported for each therapy class in future validation.",
        "",
        "## Branch Summary",
        "",
        markdown_table(summary_counts),
        "",
        "## Evidence Rows",
        "",
        markdown_table(branch),
        "",
        "## Interpretation",
        "",
        interpretation["main_readout"],
    ]
    (OUT / "summary.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(interpretation, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
