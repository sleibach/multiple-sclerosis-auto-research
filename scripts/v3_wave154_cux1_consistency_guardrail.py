#!/usr/bin/env python3
"""Wave154: guardrail analysis for CUX1 consistency in GSE129487."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


SEED = 20260527
ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "results_v3" / "wave153_gse129487_synovial_fibroblast_sirna_rescue"
OUT = ROOT / "results_v3" / "wave154_cux1_consistency_guardrail"
OUT.mkdir(parents=True, exist_ok=True)


def bh(pvalues: pd.Series) -> pd.Series:
    valid = pvalues.notna()
    q = pd.Series(np.nan, index=pvalues.index, dtype=float)
    p = pvalues[valid].astype(float)
    if p.empty:
        return q
    order = np.argsort(p.values)
    ranks = np.empty_like(order)
    ranks[order] = np.arange(1, len(p) + 1)
    q.loc[valid] = np.minimum(1.0, p.values * len(p) / ranks)
    return q


def one_sided_wilcoxon(values: np.ndarray) -> float:
    values = values[np.isfinite(values)]
    if len(values) < 3:
        return np.nan
    if np.all(values == 0):
        return 1.0
    return float(stats.wilcoxon(values, alternative="less", zero_method="wilcox").pvalue)


def binom_negative_p(n_negative: int, n: int) -> float:
    if n == 0:
        return np.nan
    return float(stats.binomtest(n_negative, n, 0.5, alternative="greater").pvalue)


def main() -> None:
    rescue = pd.read_csv(IN / "sirna_rescue_module_tests.tsv", sep="\t")
    induced = rescue[(rescue["mean_ctrl_induction"] > 0) & (rescue["ctrl_induction_q_value_bh"] < 0.05)].copy()

    rows = []
    for sirna, grp in induced.groupby("sirna"):
        values = grp["mean_sirna_effect_vs_ctrl"].astype(float).values
        n_neg = int(np.sum(values < 0))
        rows.append(
            {
                "sirna": sirna,
                "scope": "all_induced_contexts",
                "module": "ALL",
                "n_contexts": int(len(values)),
                "n_negative": n_neg,
                "fraction_negative": float(n_neg / len(values)) if len(values) else np.nan,
                "mean_effect": float(np.mean(values)) if len(values) else np.nan,
                "median_effect": float(np.median(values)) if len(values) else np.nan,
                "wilcoxon_less_p": one_sided_wilcoxon(values),
                "binomial_negative_p": binom_negative_p(n_neg, len(values)),
            }
        )
    for (sirna, module), grp in induced.groupby(["sirna", "module"]):
        values = grp["mean_sirna_effect_vs_ctrl"].astype(float).values
        n_neg = int(np.sum(values < 0))
        rows.append(
            {
                "sirna": sirna,
                "scope": "module_induced_contexts",
                "module": module,
                "n_contexts": int(len(values)),
                "n_negative": n_neg,
                "fraction_negative": float(n_neg / len(values)) if len(values) else np.nan,
                "mean_effect": float(np.mean(values)) if len(values) else np.nan,
                "median_effect": float(np.median(values)) if len(values) else np.nan,
                "wilcoxon_less_p": one_sided_wilcoxon(values),
                "binomial_negative_p": binom_negative_p(n_neg, len(values)),
            }
        )

    agg = pd.DataFrame(rows)
    agg["wilcoxon_less_q_bh"] = bh(agg["wilcoxon_less_p"])
    agg["binomial_negative_q_bh"] = bh(agg["binomial_negative_p"])
    agg = agg.sort_values(["scope", "wilcoxon_less_p", "binomial_negative_p"], na_position="last")
    agg.to_csv(OUT / "sirna_consistency_summary.tsv", sep="\t", index=False)
    induced.to_csv(OUT / "induced_context_sirna_effects.tsv", sep="\t", index=False)

    all_scope = agg[agg["scope"] == "all_induced_contexts"].copy()
    cux1 = all_scope[all_scope["sirna"] == "CUX1"]
    cux1_pass = False
    if not cux1.empty:
        row = cux1.iloc[0]
        cux1_pass = bool(row["fraction_negative"] >= 0.75 and row["wilcoxon_less_q_bh"] < 0.10)

    branch = "CUX1_CONSISTENT_DIRECTIONAL_CONTROLLER_SIGNAL" if cux1_pass else "NO_FDR_ROBUST_CUX1_CONTROLLER_SIGNAL"
    summary = {
        "branch_call": branch,
        "random_seed": SEED,
        "n_induced_context_sirna_tests": int(induced.shape[0]),
        "cux1_all_context_summary": cux1.to_dict(orient="records"),
        "top_all_context_sirnas": all_scope.head(10).to_dict(orient="records"),
        "interpretation_guardrail": "Requires CUX1 >=75% negative effects across induced contexts and BH q<0.10 for one-sided Wilcoxon.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUT / "REPORT.md").write_text(
        "# Wave154 CUX1 Consistency Guardrail\n\n"
        f"Branch call: `{branch}`.\n\n"
        "This wave aggregates siRNA effects only in contexts where the module is positively induced "
        "under control siRNA at BH q<0.05. It asks whether CUX1 is consistently negative across "
        "contexts rather than relying on individual nominal rescue tests.\n"
    )


if __name__ == "__main__":
    main()
