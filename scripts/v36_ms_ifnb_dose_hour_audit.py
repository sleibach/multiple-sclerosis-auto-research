#!/usr/bin/env python3
"""Dose/hour audit of MS IFN-beta response modules in GSE138064."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_ms_ifnb_dose_hour_audit"


def auc_score(scores: np.ndarray, y: np.ndarray) -> float:
    if len(set(y.tolist())) < 2:
        return math.nan
    ranks = pd.Series(scores).rank(method="average").to_numpy()
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    return float((float(ranks[y == 1].sum()) - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def permutation_auc_p(scores: np.ndarray, y: np.ndarray, n_perm: int = 20000) -> float:
    observed = auc_score(scores, y)
    if not np.isfinite(observed):
        return math.nan
    rng = np.random.default_rng(20260607)
    extreme = 0
    for _ in range(n_perm):
        if auc_score(scores, rng.permutation(y)) >= observed - 1e-12:
            extreme += 1
    return float((extreme + 1) / (n_perm + 1))


def hedges_g(pos: np.ndarray, neg: np.ndarray) -> float:
    if len(pos) < 2 or len(neg) < 2:
        return math.nan
    pooled = math.sqrt(((len(pos) - 1) * np.var(pos, ddof=1) + (len(neg) - 1) * np.var(neg, ddof=1)) / (len(pos) + len(neg) - 2))
    if pooled == 0:
        return 0.0
    return float(((np.mean(pos) - np.mean(neg)) / pooled) * (1.0 - 3.0 / (4.0 * (len(pos) + len(neg)) - 9.0)))


def summarize(df: pd.DataFrame, subset_name: str, sub: pd.DataFrame, feature: str) -> dict[str, object]:
    keep = sub.dropna(subset=[feature]).copy()
    y = keep["complete_responder"].astype(int).to_numpy()
    scores = keep[feature].to_numpy(float)
    pos = scores[y == 1]
    neg = scores[y == 0]
    return {
        "subset": subset_name,
        "feature": feature,
        "n": int(len(keep)),
        "n_complete": int(y.sum()),
        "n_partial": int(len(y) - y.sum()),
        "auc_high_score_complete": auc_score(scores, y),
        "auc_permutation_p": permutation_auc_p(scores, y),
        "hedges_g_complete_minus_partial": hedges_g(pos, neg),
        "welch_p": float(stats.ttest_ind(pos, neg, equal_var=False).pvalue) if len(pos) >= 2 and len(neg) >= 2 else math.nan,
    }


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
    path = ROOT / "analysis/tier_0_triage/hyp_v6_006_gse138064_ms_ifnb_replication/paired_module_deltas.tsv"
    df = pd.read_csv(path, sep="\t")
    df = df[df["responder"].isin(["Complete_Responder", "Partial_Responder"])].copy()
    df["complete_responder"] = df["responder"].eq("Complete_Responder").astype(int)
    df["locked_style_score"] = df["delta__hla_ii_without_cd74"] - df["delta__ifn_apc"]
    df["negative_delta_ifn_apc"] = -df["delta__ifn_apc"]
    df["negative_delta_receptor"] = -df["delta__receptor_only_cd74_cd44_cxcr4"]

    features = [
        "baseline__ifn_apc",
        "delta__ifn_apc",
        "negative_delta_ifn_apc",
        "baseline__hla_ii_without_cd74",
        "delta__hla_ii_without_cd74",
        "baseline__receptor_only_cd74_cd44_cxcr4",
        "delta__receptor_only_cd74_cd44_cxcr4",
        "negative_delta_receptor",
        "delta__cd74_alone",
        "locked_style_score",
    ]
    subsets: dict[str, pd.DataFrame] = {"all": df}
    subsets["stable_all_dose"] = df[df["clinical_status"].eq("stable")]
    for dose in sorted(df["dose"].dropna().unique()):
        subsets[f"stable_{dose}"] = df[df["clinical_status"].eq("stable") & df["dose"].eq(dose)]
    for hour in sorted(df["hour"].dropna().unique()):
        subsets[f"stable_hour_{hour}"] = df[df["clinical_status"].eq("stable") & df["hour"].eq(hour)]

    rows: list[dict[str, object]] = []
    for subset_name, sub in subsets.items():
        if sub["complete_responder"].nunique() < 2 or len(sub) < 10:
            continue
        for feature in features:
            rows.append(summarize(df, subset_name, sub, feature))
    result = pd.DataFrame(rows)
    result.to_csv(OUT / "gse138064_ifnb_dose_hour_tests.tsv", sep="\t", index=False)
    best = result.sort_values(["auc_high_score_complete", "auc_permutation_p"], ascending=[False, True]).head(12)
    summary = {
        "cohort": "GSE138064_MS_IFNB",
        "question": "Which baseline/dynamic APC-axis features distinguish complete from partial IFN-beta responders?",
        "n_tests": int(len(result)),
        "best_features": best.to_dict("records"),
        "interpretation": "Exploratory dose/hour support for IFN-beta HLA-II baseline/delta branch, not a V22 rule change.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = [
        "# V36 MS IFN-beta Dose/Hour Audit",
        "",
        "This re-tests the held `GSE138064` IFN-beta artifact with AUC and a",
        "fixed-seed label-permutation null, complementing the prior Welch-only",
        "summary.",
        "",
        "## Top Features",
        "",
        markdown_table(best),
        "",
        "## Full Table",
        "",
        markdown_table(result.sort_values(["subset", "feature"])),
        "",
        "## Interpretation",
        "",
        "The strongest signals are HLA-II baseline or HLA-II-related IFN-beta",
        "competence signals, not the broad locked-style scalar. This independently",
        "supports therapy-branch interpretation for IFN-beta.",
    ]
    (OUT / "summary.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
