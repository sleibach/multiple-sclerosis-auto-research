#!/usr/bin/env python3
"""V28 heterogeneous re-analysis of the locked APC/HLA-II monitoring lead."""

from __future__ import annotations

import json
import math
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import LeaveOneOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
INFILE = ROOT / "analysis/v27_coupled_axis/v27_feature_table.tsv"
OUTDIR = ROOT / "analysis/v28_heterogeneous_response"
SEED = 28028
N_PERM = 2000
N_BOOT = 2000
N_LOOCV_PERM = 0

warnings.filterwarnings("ignore", category=FutureWarning)


def auc_safe(y: np.ndarray, score: np.ndarray) -> float:
    if len(np.unique(y)) < 2:
        return float("nan")
    return float(roc_auc_score(y, score))


def hedges_g(y: np.ndarray, score: np.ndarray) -> float:
    a = score[y == 1]
    b = score[y == 0]
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    va = np.var(a, ddof=1)
    vb = np.var(b, ddof=1)
    pooled = ((len(a) - 1) * va + (len(b) - 1) * vb) / (len(a) + len(b) - 2)
    if pooled <= 0:
        return float("nan")
    d = (np.mean(a) - np.mean(b)) / math.sqrt(pooled)
    correction = 1 - 3 / (4 * (len(a) + len(b)) - 9)
    return float(d * correction)


def bootstrap_auc_ci(y: np.ndarray, score: np.ndarray, rng: np.random.Generator) -> tuple[float, float]:
    vals = []
    idx = np.arange(len(y))
    for _ in range(N_BOOT):
        sample = rng.choice(idx, size=len(idx), replace=True)
        if len(np.unique(y[sample])) < 2:
            continue
        vals.append(auc_safe(y[sample], score[sample]))
    if not vals:
        return float("nan"), float("nan")
    return float(np.quantile(vals, 0.025)), float(np.quantile(vals, 0.975))


def permutation_auc_p(
    y: np.ndarray, score: np.ndarray, observed: float, rng: np.random.Generator
) -> float:
    null = []
    for _ in range(N_PERM):
        yp = rng.permutation(y)
        null.append(auc_safe(yp, score))
    null = np.asarray(null)
    return float((np.sum(null >= observed) + 1) / (len(null) + 1))


def score_summary(name: str, df: pd.DataFrame, score_col: str, set_name: str, rng: np.random.Generator) -> dict:
    y = df["response_binary"].to_numpy(dtype=int)
    score = df[score_col].to_numpy(dtype=float)
    auc = auc_safe(y, score)
    ci_lo, ci_hi = bootstrap_auc_ci(y, score, rng)
    g = hedges_g(y, score)
    p_perm = permutation_auc_p(y, score, auc, rng)
    u_p = stats.mannwhitneyu(score[y == 1], score[y == 0], alternative="greater").pvalue
    return {
        "analysis_set": set_name,
        "method_family": "fixed_score_nonparametric",
        "method": name,
        "n": len(df),
        "n_responders": int(y.sum()),
        "n_nonresponders": int((1 - y).sum()),
        "auc": auc,
        "auc_ci_low": ci_lo,
        "auc_ci_high": ci_hi,
        "hedges_g": g,
        "permutation_p_auc": p_perm,
        "mann_whitney_p_greater": float(u_p),
    }


def loocv_predictions(model, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    out = np.zeros(len(y), dtype=float)
    loo = LeaveOneOut()
    for train, test in loo.split(x):
        if len(np.unique(y[train])) < 2:
            out[test] = np.mean(y[train])
            continue
        clf = model()
        clf.fit(x[train], y[train])
        if hasattr(clf, "predict_proba"):
            out[test] = clf.predict_proba(x[test])[:, 1]
        else:
            dec = clf.decision_function(x[test])
            out[test] = 1 / (1 + np.exp(-dec))
    return out


def permutation_loocv_p(model, x: np.ndarray, y: np.ndarray, observed: float, rng: np.random.Generator) -> float:
    vals = []
    for _ in range(N_LOOCV_PERM):
        yp = rng.permutation(y)
        pred = loocv_predictions(model, x, yp)
        vals.append(auc_safe(yp, pred))
    vals = np.asarray(vals)
    return float((np.sum(vals >= observed) + 1) / (len(vals) + 1))


def ml_summaries(df: pd.DataFrame, set_name: str, rng: np.random.Generator) -> list[dict]:
    y = df["response_binary"].to_numpy(dtype=int)
    feature_cols = ["delta_IFN_APC", "delta_HLAII", "delta_RECEPTOR", "locked_signed_score"]
    x = df[feature_cols].to_numpy(dtype=float)
    models = {
        "ridge_logistic_modules": lambda: make_pipeline(
            StandardScaler(), LogisticRegression(C=0.25, solver="liblinear", random_state=SEED)
        ),
    }
    rows = []
    for name, maker in models.items():
        pred = loocv_predictions(maker, x, y)
        auc = auc_safe(y, pred)
        ci_lo, ci_hi = bootstrap_auc_ci(y, pred, rng)
        perm_p = float("nan")
        rows.append(
            {
                "analysis_set": set_name,
                "method_family": "loocv_ml",
                "method": name,
                "features": ",".join(feature_cols),
                "n": len(df),
                "auc": auc,
                "auc_ci_low": ci_lo,
                "auc_ci_high": ci_hi,
                "hedges_g": hedges_g(y, pred),
                "permutation_p_auc": perm_p,
            }
        )
    return rows


def cohort_adjusted(df: pd.DataFrame, set_name: str) -> dict:
    y = df["response_binary"].to_numpy(dtype=float)
    x = pd.get_dummies(df[["cohort"]], drop_first=True, dtype=float)
    x.insert(0, "locked_signed_score", df["locked_signed_score"].astype(float).to_numpy())
    x = sm.add_constant(x, has_constant="add")
    fit = sm.OLS(y, x).fit(cov_type="HC1")
    return {
        "analysis_set": set_name,
        "method_family": "cohort_adjusted_ols",
        "method": "response_binary_on_locked_score_plus_cohort_fixed_effects",
        "n": len(df),
        "coef_locked_score": float(fit.params["locked_signed_score"]),
        "p_locked_score": float(fit.pvalues["locked_signed_score"]),
        "r2": float(fit.rsquared),
    }


def bayesian_bootstrap_effect(df: pd.DataFrame, set_name: str, rng: np.random.Generator) -> dict:
    y = df["response_binary"].to_numpy(dtype=int)
    score = df["locked_signed_score"].to_numpy(dtype=float)
    resp = score[y == 1]
    non = score[y == 0]
    draws = []
    for _ in range(N_BOOT):
        wr = rng.dirichlet(np.ones(len(resp)))
        wn = rng.dirichlet(np.ones(len(non)))
        draws.append(float(np.sum(wr * resp) - np.sum(wn * non)))
    arr = np.asarray(draws)
    return {
        "analysis_set": set_name,
        "method_family": "bayesian_bootstrap",
        "method": "posterior_responder_minus_nonresponder_locked_score",
        "n": len(df),
        "posterior_mean_diff": float(np.mean(arr)),
        "posterior_ci_low": float(np.quantile(arr, 0.025)),
        "posterior_ci_high": float(np.quantile(arr, 0.975)),
        "posterior_p_diff_gt_0": float(np.mean(arr > 0)),
    }


def jackknife(df: pd.DataFrame, set_name: str) -> pd.DataFrame:
    rows = []
    for i, row in df.reset_index(drop=True).iterrows():
        sub = df.reset_index(drop=True).drop(index=i)
        rows.append(
            {
                "analysis_set": set_name,
                "dropped_cohort": row["cohort"],
                "dropped_patient": row["patient"],
                "auc_after_drop": auc_safe(
                    sub["response_binary"].to_numpy(dtype=int),
                    sub["locked_signed_score"].to_numpy(dtype=float),
                ),
            }
        )
    return pd.DataFrame(rows)


def adjacent_feature_tests(df: pd.DataFrame, set_name: str, rng: np.random.Generator) -> list[dict]:
    d = df.copy()
    d["apc_vector_norm"] = np.sqrt(d["delta_IFN_APC"] ** 2 + d["delta_HLAII"] ** 2 + d["delta_RECEPTOR"] ** 2)
    d["hla_vs_ifn_angle"] = np.arctan2(d["delta_HLAII"], -d["delta_IFN_APC"])
    d["hla_ifn_product"] = d["delta_HLAII"] * (-d["delta_IFN_APC"])
    rows = []
    for col in ["apc_vector_norm", "hla_vs_ifn_angle", "hla_ifn_product"]:
        rows.append(score_summary(col, d, col, set_name, rng) | {"method_family": "adjacent_dynamic_feature"})
    return rows


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    df = pd.read_csv(INFILE, sep="\t")
    df["response_binary"] = df["response_binary"].astype(int)
    sets = {
        "bounded_immune_remodeling": df[df["domain"] == "bounded"].copy(),
        "all_primary_plus_exact_uc": df.copy(),
    }
    all_rows = []
    cohort_rows = []
    bayes_rows = []
    jackknife_tables = []
    for set_name, sub in sets.items():
        for col in ["locked_signed_score", "delta_RECEPTOR", "coupled_projection", "coupled_v22_augmented", "coupling_coordination"]:
            all_rows.append(score_summary(col, sub, col, set_name, rng))
        all_rows.extend(ml_summaries(sub, set_name, rng))
        all_rows.extend(adjacent_feature_tests(sub, set_name, rng))
        cohort_rows.append(cohort_adjusted(sub, set_name))
        bayes_rows.append(bayesian_bootstrap_effect(sub, set_name, rng))
        jk = jackknife(sub, set_name)
        jk.to_csv(OUTDIR / f"jackknife_{set_name}.tsv", sep="\t", index=False)
        jackknife_tables.append(jk.assign(analysis_set=set_name))

    metrics = pd.DataFrame(all_rows)
    metrics.to_csv(OUTDIR / "heterogeneous_method_metrics.tsv", sep="\t", index=False)
    pd.DataFrame(cohort_rows).to_csv(OUTDIR / "cohort_adjusted_models.tsv", sep="\t", index=False)
    pd.DataFrame(bayes_rows).to_csv(OUTDIR / "bayesian_bootstrap_effects.tsv", sep="\t", index=False)
    pd.concat(jackknife_tables, ignore_index=True).to_csv(OUTDIR / "jackknife_influence.tsv", sep="\t", index=False)

    bounded = metrics[metrics["analysis_set"] == "bounded_immune_remodeling"].copy()
    scalar = bounded[bounded["method"] == "locked_signed_score"].iloc[0]
    robust_support = bounded[
        (bounded["auc"] >= 0.70)
        & (bounded["hedges_g"] >= 0.50)
        & (bounded["permutation_p_auc"] <= 0.10)
    ]
    summary = {
        "seed": SEED,
        "n_permutations_fixed_scores": N_PERM,
        "n_permutations_loocv": N_LOOCV_PERM,
        "n_bootstrap": N_BOOT,
        "bounded_scalar_auc": float(scalar["auc"]),
        "bounded_scalar_hedges_g": float(scalar["hedges_g"]),
        "bounded_scalar_permutation_p": float(scalar["permutation_p_auc"]),
        "bounded_methods_meeting_auc_g_perm_gate": robust_support["method"].tolist(),
        "bounded_methods_meeting_gate_count": int(len(robust_support)),
        "all_methods_count": int(len(metrics)),
        "verdict": "tool_robust_but_data_limited"
        if len(robust_support) >= 3
        else "tool_fragile_or_underpowered",
    }
    with (OUTDIR / "v28_summary.json").open("w") as fh:
        json.dump(summary, fh, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
