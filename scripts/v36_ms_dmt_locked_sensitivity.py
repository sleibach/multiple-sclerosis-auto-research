#!/usr/bin/env python3
"""Exact permutation and leave-one-out sensitivity for V22 MS DMT cohorts."""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_ms_dmt_locked_sensitivity"


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
    total = 0
    extreme = 0
    for pos_idx in itertools.combinations(range(n), n_pos):
        yy = np.zeros(n, dtype=int)
        yy[list(pos_idx)] = 1
        total += 1
        if auc_score(scores, yy) >= observed - 1e-12:
            extreme += 1
    return float(extreme / total)


def summarize_feature(df: pd.DataFrame, cohort: str, feature: str) -> dict[str, object]:
    sub = df[df["cohort"].eq(cohort)].dropna(subset=[feature]).copy()
    y = sub["response"].eq("Responder").astype(int).to_numpy()
    scores = sub[feature].to_numpy(float)
    loo = []
    for idx in range(len(sub)):
        keep = np.arange(len(sub)) != idx
        loo.append(auc_score(scores[keep], y[keep]))
    return {
        "cohort": cohort,
        "feature": feature,
        "n": int(len(sub)),
        "n_responders": int(y.sum()),
        "n_nonresponders": int(len(y) - y.sum()),
        "auc": auc_score(scores, y),
        "exact_auc_p": exact_auc_p(scores, y),
        "loo_min_auc": float(np.nanmin(loo)),
        "loo_max_auc": float(np.nanmax(loo)),
        "loo_auc_values": ";".join(f"{x:.3f}" for x in loo),
    }


def markdown_table(df: pd.DataFrame) -> str:
    clean = df.copy()
    for col in clean.columns:
        clean[col] = clean[col].map(lambda x: f"{x:.4g}" if isinstance(x, float) and np.isfinite(x) else x)
    header = "| " + " | ".join(clean.columns.astype(str)) + " |"
    sep = "| " + " | ".join(["---"] * len(clean.columns)) + " |"
    rows = ["| " + " | ".join(str(x) for x in row) + " |" for row in clean.to_numpy()]
    return "\n".join([header, sep, *rows])


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(ROOT / "analysis/v22_locked_apc_hla_validation/paired_locked_scores_v22.tsv", sep="\t")
    df["negative_delta_ifn_apc"] = -df["delta_IFN_APC"]
    df["negative_delta_receptor"] = -df["delta_RECEPTOR"]
    features = ["locked_signed_score", "delta_IFN_APC", "negative_delta_ifn_apc", "delta_HLAII", "delta_RECEPTOR", "negative_delta_receptor"]
    rows = [summarize_feature(df, cohort, feature) for cohort in sorted(df["cohort"].unique()) for feature in features]
    result = pd.DataFrame(rows)
    result.to_csv(OUT / "ms_dmt_locked_sensitivity.tsv", sep="\t", index=False)
    summary = {
        "question": "How robust are the locked V22 MS DMT cohort signals under exact label permutation and leave-one-out?",
        "dmf_locked": result[(result["cohort"].eq("GSE235357")) & (result["feature"].eq("locked_signed_score"))].iloc[0].to_dict(),
        "fingolimod_locked": result[(result["cohort"].eq("GSE250453")) & (result["feature"].eq("locked_signed_score"))].iloc[0].to_dict(),
        "interpretation": "DMF remains directionally supportive but fragile in n=10; fingolimod remains weak/null.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = [
        "# V36 MS DMT Locked-Rule Sensitivity",
        "",
        "Exact permutation and leave-one-out sensitivity for the two V22 MS DMT",
        "paired cohorts.",
        "",
        markdown_table(result),
        "",
        "## Interpretation",
        "",
        "The DMF locked score remains directionally supportive but is fragile in",
        "n=10. Fingolimod remains weak/null. This reinforces that fresh Gafson-style",
        "validation is required before any clinical claim.",
    ]
    (OUT / "summary.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
