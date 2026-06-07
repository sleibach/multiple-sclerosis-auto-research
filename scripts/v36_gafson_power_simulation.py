#!/usr/bin/env python3
"""Empirical power simulation for fresh DMF validation of the locked rule."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_gafson_power_simulation"
SEED = 20260607


def auc_score(scores: np.ndarray, y: np.ndarray) -> float:
    ranks = pd.Series(scores).rank(method="average").to_numpy()
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    if n1 == 0 or n0 == 0:
        return math.nan
    return float((float(ranks[y == 1].sum()) - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def normal_auc_p(scores: np.ndarray, y: np.ndarray) -> float:
    """Large-sample Mann-Whitney normal approximation, one-sided AUC > 0.5."""
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    auc = auc_score(scores, y)
    if n1 == 0 or n0 == 0 or not np.isfinite(auc):
        return math.nan
    u = auc * n1 * n0
    mean = n1 * n0 / 2.0
    sd = math.sqrt(n1 * n0 * (n1 + n0 + 1) / 12.0)
    if sd == 0:
        return math.nan
    z = (u - mean) / sd
    return float(1.0 - stats.norm.cdf(z))


def simulate_power(responder: np.ndarray, nonresponder: np.ndarray, n_per_group: int, n_sim: int = 20000) -> dict[str, object]:
    rng = np.random.default_rng(SEED + n_per_group)
    aucs = []
    pvals = []
    y = np.array([1] * n_per_group + [0] * n_per_group, dtype=int)
    for _ in range(n_sim):
        r = rng.choice(responder, size=n_per_group, replace=True)
        nr = rng.choice(nonresponder, size=n_per_group, replace=True)
        scores = np.concatenate([r, nr])
        aucs.append(auc_score(scores, y))
        pvals.append(normal_auc_p(scores, y))
    aucs_arr = np.asarray(aucs, dtype=float)
    pvals_arr = np.asarray(pvals, dtype=float)
    return {
        "n_per_group": n_per_group,
        "total_n": n_per_group * 2,
        "n_sim": n_sim,
        "median_auc": float(np.nanmedian(aucs_arr)),
        "auc_ci_low": float(np.nanpercentile(aucs_arr, 2.5)),
        "auc_ci_high": float(np.nanpercentile(aucs_arr, 97.5)),
        "power_one_sided_p_lt_0_05": float(np.nanmean(pvals_arr < 0.05)),
        "power_auc_ge_0_70": float(np.nanmean(aucs_arr >= 0.70)),
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
    dmf = df[df["cohort"].eq("GSE235357")].copy()
    responder = dmf.loc[dmf["response"].eq("Responder"), "locked_signed_score"].to_numpy(float)
    nonresponder = dmf.loc[dmf["response"].eq("Non-responder"), "locked_signed_score"].to_numpy(float)
    observed = {
        "n_responder": int(len(responder)),
        "n_nonresponder": int(len(nonresponder)),
        "observed_auc": auc_score(np.concatenate([responder, nonresponder]), np.array([1] * len(responder) + [0] * len(nonresponder))),
        "responder_scores": responder.tolist(),
        "nonresponder_scores": nonresponder.tolist(),
    }
    rows = [simulate_power(responder, nonresponder, n) for n in [8, 10, 12, 15, 20, 25, 30, 40, 50]]
    result = pd.DataFrame(rows)
    result.to_csv(OUT / "dmf_empirical_power.tsv", sep="\t", index=False)
    summary = {
        "question": "What sample size is needed to validate the locked DMF-like effect if the observed GSE235357 score distributions are representative?",
        "assumption": "Nonparametric bootstrap from observed n=5/5 GSE235357 locked-score distributions; one-sided Mann-Whitney normal approximation for p-values.",
        "observed": observed,
        "power_table": result.to_dict("records"),
        "interpretation": "At the observed effect size, roughly 40-50 per group is needed for high one-sided p<0.05 power; smaller fresh cohorts can still estimate direction but are unlikely to settle the claim.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = [
        "# V36 Gafson-Style DMF Power Simulation",
        "",
        "Assumption: the observed `GSE235357` responder/nonresponder locked-score",
        "distributions are an empirical template for a fresh DMF validation cohort.",
        "This is a planning simulation, not evidence that the effect will replicate.",
        "",
        f"Observed AUC: `{observed['observed_auc']:.3f}` from `5` responders and `5` nonresponders.",
        "",
        markdown_table(result),
        "",
        "## Interpretation",
        "",
        "At the observed effect size, small n=10-20 total cohorts are expected to be",
        "directional but underpowered. A decisive fresh validation likely needs on",
        "the order of `40-50` subjects per response group, or a stronger true effect",
        "than the small GSE235357 template suggests.",
    ]
    (OUT / "summary.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
