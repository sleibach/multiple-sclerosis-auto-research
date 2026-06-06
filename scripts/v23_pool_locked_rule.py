#!/usr/bin/env python3
"""Pool V22 locked-rule validation scores without changing the locked rule."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
IN_DIR = ROOT / "analysis" / "v22_locked_apc_hla_validation"
OUT_DIR = ROOT / "analysis" / "v23_apc_hla_monitoring"
SEED = 20260606


def auc_score(scores: np.ndarray, y: np.ndarray) -> float:
    if len(set(y.tolist())) < 2:
        return math.nan
    ranks = pd.Series(scores).rank(method="average").to_numpy()
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    rank_sum = float(ranks[y == 1].sum())
    return float((rank_sum - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def bootstrap_auc_ci(scores: np.ndarray, y: np.ndarray, strata: np.ndarray | None = None, n_boot: int = 5000) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    aucs: list[float] = []
    if strata is None:
        idx = np.arange(len(scores))
        for _ in range(n_boot):
            sample = rng.choice(idx, size=len(idx), replace=True)
            if len(set(y[sample].tolist())) < 2:
                continue
            aucs.append(auc_score(scores[sample], y[sample]))
    else:
        unique = np.unique(strata)
        by_stratum = {s: np.where(strata == s)[0] for s in unique}
        for _ in range(n_boot):
            sample_parts = [rng.choice(idx, size=len(idx), replace=True) for idx in by_stratum.values()]
            sample = np.concatenate(sample_parts)
            if len(set(y[sample].tolist())) < 2:
                continue
            aucs.append(auc_score(scores[sample], y[sample]))
    if not aucs:
        return math.nan, math.nan
    return float(np.percentile(aucs, 2.5)), float(np.percentile(aucs, 97.5))


def hedges_g_and_var(scores: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    a = scores[y == 1]
    b = scores[y == 0]
    if len(a) < 2 or len(b) < 2:
        return math.nan, math.nan
    s2 = ((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1)) / (len(a) + len(b) - 2)
    if s2 <= 0:
        g = 0.0
    else:
        d = (float(np.mean(a)) - float(np.mean(b))) / math.sqrt(s2)
        g = d * (1.0 - 3.0 / (4.0 * (len(a) + len(b)) - 9.0))
    # Approximate sampling variance for standardized mean difference.
    var = (len(a) + len(b)) / (len(a) * len(b)) + (g * g) / (2.0 * (len(a) + len(b) - 2))
    return float(g), float(var)


def fixed_random_meta(effects: pd.DataFrame) -> dict[str, float]:
    e = effects.dropna(subset=["hedges_g", "var_g"]).copy()
    w = 1.0 / e["var_g"].to_numpy(float)
    g = e["hedges_g"].to_numpy(float)
    fixed = float(np.sum(w * g) / np.sum(w))
    fixed_se = math.sqrt(1.0 / float(np.sum(w)))
    q = float(np.sum(w * (g - fixed) ** 2))
    df = max(len(g) - 1, 1)
    c = float(np.sum(w) - np.sum(w**2) / np.sum(w))
    tau2 = max(0.0, (q - df) / c) if c > 0 else 0.0
    wr = 1.0 / (e["var_g"].to_numpy(float) + tau2)
    random = float(np.sum(wr * g) / np.sum(wr))
    random_se = math.sqrt(1.0 / float(np.sum(wr)))
    i2 = max(0.0, (q - df) / q) if q > 0 else 0.0
    return {
        "fixed_g": fixed,
        "fixed_se": fixed_se,
        "fixed_ci_low": fixed - 1.96 * fixed_se,
        "fixed_ci_high": fixed + 1.96 * fixed_se,
        "random_g": random,
        "random_se": random_se,
        "random_ci_low": random - 1.96 * random_se,
        "random_ci_high": random + 1.96 * random_se,
        "q": q,
        "tau2": tau2,
        "i2": i2,
    }


def load_scores() -> pd.DataFrame:
    ms = pd.read_csv(IN_DIR / "paired_locked_scores_v22.tsv", sep="\t")
    cd = pd.read_csv(IN_DIR / "paired_locked_scores_v22_cross_disease.tsv", sep="\t")
    df = pd.concat([ms, cd], ignore_index=True, sort=False)
    scope = pd.read_csv(IN_DIR / "validation_ledger_v22.tsv", sep="\t")[["cohort", "validation_scope", "therapy", "therapy_class", "disease"]]
    df = df.merge(scope, on="cohort", how="left")
    exact_paired = OUT_DIR / "gse253006_exact_locked" / "gse253006_exact_paired_scores.tsv"
    exact_ledger = OUT_DIR / "gse253006_exact_locked" / "gse253006_exact_validation_ledger.tsv"
    if exact_paired.exists() and exact_ledger.exists():
        exact = pd.read_csv(exact_paired, sep="\t")
        exact_scope = pd.read_csv(exact_ledger, sep="\t")[["cohort", "validation_scope", "therapy", "therapy_class", "disease"]]
        exact = exact.merge(exact_scope, on="cohort", how="left")
        df = pd.concat([df, exact], ignore_index=True, sort=False)
    df["y"] = df["response"].eq("Responder").astype(int)
    return df


def summarize_group(name: str, df: pd.DataFrame) -> dict[str, object]:
    scores = df["locked_signed_score"].to_numpy(float)
    y = df["y"].to_numpy(int)
    cohort = df["cohort"].astype(str).to_numpy()
    auc = auc_score(scores, y)
    lo, hi = bootstrap_auc_ci(scores, y, cohort)
    g, var_g = hedges_g_and_var(scores, y)
    p = stats.ttest_ind(scores[y == 1], scores[y == 0], equal_var=False).pvalue if len(set(y.tolist())) == 2 else math.nan
    return {
        "group": name,
        "n": int(len(df)),
        "n_responders": int(y.sum()),
        "n_nonresponders": int(len(y) - y.sum()),
        "cohorts": ";".join(sorted(df["cohort"].unique())),
        "auc": auc,
        "auc_ci_low_stratified_bootstrap": lo,
        "auc_ci_high_stratified_bootstrap": hi,
        "hedges_g_pooled_subjects": g,
        "hedges_g_var": var_g,
        "welch_p": float(p),
    }


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_scores()
    primary = df[df["validation_scope"].eq("primary_locked")].copy()
    primary_with_exact_uc = df[df["validation_scope"].isin(["primary_locked", "primary_locked_exact_all_cell_compartment_unresolved"])].copy()
    primary_plus_exploratory = df.copy()
    compatible = df[df["cohort"].isin(["GSE235357", "GSE253006_TOF_exact"])].copy()
    summaries = [
        summarize_group("primary_locked_all", primary),
        summarize_group("primary_locked_plus_exact_uc_all_cell", primary_with_exact_uc),
        summarize_group("primary_plus_exploratory_all", primary_plus_exploratory),
        summarize_group("immunomodulatory_pass_hypothesis_DMF_plus_exact_TOF", compatible),
    ]
    summary_df = pd.DataFrame(summaries)
    summary_df.to_csv(OUT_DIR / "v23_pooled_locked_rule_summary.tsv", sep="\t", index=False)

    cohort_effects = []
    for cohort, sub in df.groupby("cohort"):
        g, var = hedges_g_and_var(sub["locked_signed_score"].to_numpy(float), sub["y"].to_numpy(int))
        row = {
            "cohort": cohort,
            "validation_scope": sub["validation_scope"].iloc[0],
            "therapy": sub["therapy"].iloc[0],
            "therapy_class": sub["therapy_class"].iloc[0],
            "disease": sub["disease"].iloc[0],
            "n": int(len(sub)),
            "hedges_g": g,
            "var_g": var,
        }
        cohort_effects.append(row)
    effects_df = pd.DataFrame(cohort_effects)
    effects_df.to_csv(OUT_DIR / "v23_cohort_effects.tsv", sep="\t", index=False)

    meta_primary = fixed_random_meta(effects_df[effects_df["validation_scope"].eq("primary_locked")])
    meta_primary_exact = fixed_random_meta(effects_df[effects_df["validation_scope"].isin(["primary_locked", "primary_locked_exact_all_cell_compartment_unresolved"])])
    meta_all = fixed_random_meta(effects_df)
    meta = {
        "primary_locked_meta": meta_primary,
        "primary_locked_plus_exact_uc_meta": meta_primary_exact,
        "primary_plus_exploratory_meta": meta_all,
    }
    (OUT_DIR / "v23_meta_analysis.json").write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"summaries": summaries, "meta": meta}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
