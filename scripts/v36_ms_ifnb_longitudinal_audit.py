#!/usr/bin/env python3
"""Timepoint audit of locked-style APC/HLA-II dynamics in MS IFN-beta GSE24427."""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_ms_ifnb_longitudinal_audit"


def auc_score(scores: np.ndarray, y: np.ndarray) -> float:
    if len(set(y.tolist())) < 2:
        return math.nan
    ranks = pd.Series(scores).rank(method="average").to_numpy()
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    return float((float(ranks[y == 1].sum()) - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def exact_auc_p(scores: np.ndarray, y: np.ndarray) -> float:
    n = len(y)
    n_pos = int(y.sum())
    observed = auc_score(scores, y)
    if n > 24 or not np.isfinite(observed) or n_pos == 0 or n_pos == n:
        return math.nan
    total = 0
    extreme = 0
    for pos_idx in itertools.combinations(range(n), n_pos):
        yy = np.zeros(n, dtype=int)
        yy[list(pos_idx)] = 1
        total += 1
        if auc_score(scores, yy) >= observed - 1e-12:
            extreme += 1
    return float(extreme / total)


def permutation_auc_p(scores: np.ndarray, y: np.ndarray, n_perm: int = 50000) -> float:
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


def summarize(df: pd.DataFrame, timepoint: str, feature: str) -> dict[str, object]:
    sub = df[df["timepoint"].eq(timepoint)].dropna(subset=[feature, "relapse_free_2y"]).copy()
    y = sub["relapse_free_2y"].astype(int).to_numpy()
    scores = sub[feature].to_numpy(float)
    pos = scores[y == 1]
    neg = scores[y == 0]
    return {
        "timepoint": timepoint,
        "feature": feature,
        "n": int(len(sub)),
        "n_relapse_free": int(y.sum()),
        "n_relapsed": int(len(y) - y.sum()),
        "auc_high_score_relapse_free": auc_score(scores, y),
        "auc_permutation_p": exact_auc_p(scores, y) if len(y) <= 24 else permutation_auc_p(scores, y),
        "permutation_mode": "exact" if len(y) <= 24 else "monte_carlo_50000",
        "hedges_g_relapsefree_minus_relapsed": hedges_g(pos, neg),
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
    path = ROOT / "analysis/tier_0_triage/hyp_v6_006_gse24427_ms_ifnb_longitudinal/paired_module_deltas.tsv"
    df = pd.read_csv(path, sep="\t")
    df["locked_style_score"] = df["delta__hla_ii_without_cd74"] - df["delta__ifn_apc"]
    df["negative_delta_ifn_apc"] = -df["delta__ifn_apc"]
    df["negative_delta_receptor"] = -df["delta__receptor_only_cd74_cd44_cxcr4"]
    features = [
        "locked_style_score",
        "delta__ifn_apc",
        "negative_delta_ifn_apc",
        "delta__hla_ii_without_cd74",
        "negative_delta_receptor",
        "delta__cd74_alone",
    ]
    timepoints = ["second_injection", "month_1", "month_24"]
    rows = [summarize(df, tp, feature) for tp in timepoints for feature in features]
    result = pd.DataFrame(rows)
    result.to_csv(OUT / "gse24427_ifnb_timepoint_tests.tsv", sep="\t", index=False)

    best = result.sort_values(["auc_high_score_relapse_free", "auc_permutation_p"], ascending=[False, True]).head(8)
    summary = {
        "cohort": "GSE24427_MS_IFNB",
        "question": "Does a locked-style APC/HLA-II dynamic score act as early monitoring for relapse-free status?",
        "n_tests": int(len(result)),
        "best_features": best.to_dict("records"),
        "interpretation": "Exploratory longitudinal stress test; no rule change without fresh validation.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = [
        "# V36 MS IFN-beta Longitudinal Audit",
        "",
        "This uses the held `GSE24427` MS IFN-beta longitudinal artifact to test",
        "whether a locked-style dynamic APC/HLA-II score behaves like an early",
        "monitoring signal for 2-year relapse-free status.",
        "",
        markdown_table(result.sort_values(["timepoint", "feature"])),
        "",
        "## Interpretation",
        "",
        "This is an exploratory stress test on an older IFN-beta cohort. It can add",
        "context about timing, but it does not edit the immutable V22 rule or create",
        "a successor rule.",
    ]
    (OUT / "summary.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
