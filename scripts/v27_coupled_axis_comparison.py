#!/usr/bin/env python3
"""V27 fixed coupled-axis comparison against immutable V22 scalar."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v27_coupled_axis"
SEED = 27027
N_PERM = 5000
N_BOOT = 2000
RNG = np.random.default_rng(SEED)

W_IFN = 0.4519
W_HLA = 0.2709
W_REC = 0.2772

COHORT_META = {
    "GSE235357": {
        "disease": "MS",
        "therapy": "dimethyl_fumarate",
        "therapy_class": "Class C",
        "domain": "bounded",
        "source": "V22 primary",
    },
    "GSE250453": {
        "disease": "MS",
        "therapy": "fingolimod",
        "therapy_class": "Class C",
        "domain": "out_of_scope_s1p",
        "source": "V22 primary",
    },
    "GSE85034_ADA": {
        "disease": "psoriasis",
        "therapy": "adalimumab",
        "therapy_class": "Class A",
        "domain": "out_of_scope_skin_tnf",
        "source": "V22 primary",
    },
    "GSE253006_TOF_exact": {
        "disease": "ulcerative_colitis",
        "therapy": "tofacitinib",
        "therapy_class": "Class A",
        "domain": "bounded",
        "source": "V23 exact all-cell",
    },
}


def auc_score(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y).astype(int)
    score = np.asarray(score).astype(float)
    pos = score[y == 1]
    neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    wins = 0.0
    for p in pos:
        wins += np.sum(p > neg)
        wins += 0.5 * np.sum(p == neg)
    return float(wins / (len(pos) * len(neg)))


def hedges_g(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y).astype(int)
    a = np.asarray(score)[y == 1]
    b = np.asarray(score)[y == 0]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    va = np.var(a, ddof=1)
    vb = np.var(b, ddof=1)
    pooled = np.sqrt(((len(a) - 1) * va + (len(b) - 1) * vb) / (len(a) + len(b) - 2))
    if pooled == 0:
        return np.nan
    d = (np.mean(a) - np.mean(b)) / pooled
    correction = 1 - (3 / (4 * (len(a) + len(b)) - 9))
    return float(d * correction)


def bootstrap_auc_ci(y: np.ndarray, score: np.ndarray) -> tuple[float, float]:
    vals = []
    idx_pos = np.where(y == 1)[0]
    idx_neg = np.where(y == 0)[0]
    for _ in range(N_BOOT):
        idx = np.concatenate([
            RNG.choice(idx_pos, size=len(idx_pos), replace=True),
            RNG.choice(idx_neg, size=len(idx_neg), replace=True),
        ])
        vals.append(auc_score(y[idx], score[idx]))
    return float(np.nanpercentile(vals, 2.5)), float(np.nanpercentile(vals, 97.5))


def load_paired() -> pd.DataFrame:
    v22 = pd.read_csv(ROOT / "analysis/v22_locked_apc_hla_validation/paired_locked_scores_v22.tsv", sep="\t")
    cross = pd.read_csv(ROOT / "analysis/v22_locked_apc_hla_validation/paired_locked_scores_v22_cross_disease.tsv", sep="\t")
    ada = cross[cross["cohort"] == "GSE85034_ADA"].copy()
    tof = pd.read_csv(ROOT / "analysis/v23_apc_hla_monitoring/gse253006_exact_locked/gse253006_exact_paired_scores.tsv", sep="\t")
    df = pd.concat([v22, ada, tof], ignore_index=True, sort=False)
    df["response_binary"] = (df["response"].astype(str).str.lower() == "responder").astype(int)
    for key, meta in COHORT_META.items():
        mask = df["cohort"] == key
        for col, val in meta.items():
            df.loc[mask, col] = val
    df = df[df["cohort"].isin(COHORT_META)].copy()
    df.to_csv(OUT / "v27_paired_score_input.tsv", sep="\t", index=False)
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    projection = W_IFN * df["delta_IFN_APC"] + W_HLA * df["delta_HLAII"] + W_REC * df["delta_RECEPTOR"]
    df["coupled_projection"] = np.where(df["therapy_class"] == "Class A", -projection, projection)

    class_a = -((W_IFN * df["delta_IFN_APC"] + W_REC * df["delta_RECEPTOR"]) / (W_IFN + W_REC))
    class_b = (W_HLA * df["delta_HLAII"] + W_REC * df["delta_RECEPTOR"]) / (W_HLA + W_REC)
    class_c = W_HLA * df["delta_HLAII"] - W_IFN * df["delta_IFN_APC"] + W_REC * df["delta_RECEPTOR"]
    df["coupled_v22_augmented"] = np.select(
        [df["therapy_class"] == "Class A", df["therapy_class"] == "Class B", df["therapy_class"] == "Class C"],
        [class_a, class_b, class_c],
        default=np.nan,
    )

    parts = []
    for cohort, sub in df.groupby("cohort", sort=False):
        z = sub[["delta_IFN_APC", "delta_HLAII", "delta_RECEPTOR"]].astype(float)
        z = (z - z.mean(axis=0)) / z.std(axis=0, ddof=0).replace(0, np.nan)
        z = z.fillna(0.0)
        center = W_IFN * z["delta_IFN_APC"] + W_HLA * z["delta_HLAII"] + W_REC * z["delta_RECEPTOR"]
        penalty = (
            W_IFN * np.abs(z["delta_IFN_APC"] - center)
            + W_HLA * np.abs(z["delta_HLAII"] - center)
            + W_REC * np.abs(z["delta_RECEPTOR"] - center)
        )
        tmp = sub.copy()
        tmp["coordination_penalty"] = penalty.to_numpy()
        parts.append(tmp)
    df = pd.concat(parts, ignore_index=True)
    df["coupling_coordination"] = np.where(
        df["therapy_class"] == "Class A",
        df["coupled_projection"] - df["coordination_penalty"],
        df["coupled_v22_augmented"] - df["coordination_penalty"],
    )
    df.to_csv(OUT / "v27_feature_table.tsv", sep="\t", index=False)
    return df


def eval_feature(df: pd.DataFrame, feature: str, subset_name: str, cohort: str | None = None) -> dict:
    y = df["response_binary"].to_numpy(int)
    s = df[feature].to_numpy(float)
    auc = auc_score(y, s)
    ci_low, ci_high = bootstrap_auc_ci(y, s) if len(np.unique(y)) == 2 else (np.nan, np.nan)
    g = hedges_g(y, s)
    p = stats.ttest_ind(s[y == 1], s[y == 0], equal_var=False, nan_policy="omit").pvalue if len(np.unique(y)) == 2 else np.nan
    return {
        "subset": subset_name,
        "cohort": cohort or "pooled",
        "feature": feature,
        "n": int(len(df)),
        "n_responders": int(y.sum()),
        "n_nonresponders": int((1 - y).sum()),
        "auc": auc,
        "auc_ci_low": ci_low,
        "auc_ci_high": ci_high,
        "hedges_g": g,
        "welch_p": float(p) if np.isfinite(p) else np.nan,
        "parameter_count": 0,
    }


def permutation_advantage(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    rows = []
    for subset_name, sub in {
        "bounded": df[df["domain"] == "bounded"].copy(),
        "all_primary_plus_exact": df.copy(),
    }.items():
        y = sub["response_binary"].to_numpy(int)
        scalar = sub["locked_signed_score"].to_numpy(float)
        scalar_auc = auc_score(y, scalar)
        observed = {}
        for feat in feature_cols:
            observed[feat] = auc_score(y, sub[feat].to_numpy(float)) - scalar_auc
        obs_best_feat = max(observed, key=observed.get)
        obs_best = observed[obs_best_feat]

        null_best = []
        null_each = {feat: [] for feat in feature_cols}
        for _ in range(N_PERM):
            yp = RNG.permutation(y)
            s_auc = auc_score(yp, scalar)
            diffs = []
            for feat in feature_cols:
                diff = auc_score(yp, sub[feat].to_numpy(float)) - s_auc
                null_each[feat].append(diff)
                diffs.append(diff)
            null_best.append(max(diffs))
        rows.append({
            "subset": subset_name,
            "feature": "best_of_coupled_candidates",
            "observed_best_feature": obs_best_feat,
            "observed_delta_auc": obs_best,
            "max_candidate_null_p": (np.sum(np.array(null_best) >= obs_best) + 1) / (N_PERM + 1),
            "null_mean_delta_auc": float(np.mean(null_best)),
            "null_p95_delta_auc": float(np.percentile(null_best, 95)),
            "n_permutations": N_PERM,
        })
        for feat in feature_cols:
            vals = np.array(null_each[feat])
            rows.append({
                "subset": subset_name,
                "feature": feat,
                "observed_best_feature": feat,
                "observed_delta_auc": observed[feat],
                "max_candidate_null_p": (np.sum(vals >= observed[feat]) + 1) / (N_PERM + 1),
                "null_mean_delta_auc": float(np.mean(vals)),
                "null_p95_delta_auc": float(np.percentile(vals, 95)),
                "n_permutations": N_PERM,
            })
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = add_features(load_paired())
    features = ["locked_signed_score", "coupled_projection", "coupled_v22_augmented", "coupling_coordination"]
    subsets = {
        "bounded": df[df["domain"] == "bounded"].copy(),
        "all_primary_plus_exact": df.copy(),
        "out_of_scope": df[df["domain"] != "bounded"].copy(),
    }
    rows = []
    for subset_name, sub in subsets.items():
        for feat in features:
            rows.append(eval_feature(sub, feat, subset_name))
        for cohort, csub in sub.groupby("cohort"):
            for feat in features:
                rows.append(eval_feature(csub, feat, subset_name, cohort=cohort))
    metrics = pd.DataFrame(rows)
    metrics.to_csv(OUT / "v27_scalar_vs_coupled_metrics.tsv", sep="\t", index=False)
    perm = permutation_advantage(df, ["coupled_projection", "coupled_v22_augmented", "coupling_coordination"])
    perm.to_csv(OUT / "v27_permutation_advantage.tsv", sep="\t", index=False)

    bounded_metrics = metrics[(metrics["subset"] == "bounded") & (metrics["cohort"] == "pooled")].set_index("feature")
    scalar_auc = float(bounded_metrics.loc["locked_signed_score", "auc"])
    scalar_g = float(bounded_metrics.loc["locked_signed_score", "hedges_g"])
    coupled = bounded_metrics.loc[["coupled_projection", "coupled_v22_augmented", "coupling_coordination"]].copy()
    best = coupled.sort_values("auc", ascending=False).iloc[0]
    best_feature = coupled.sort_values("auc", ascending=False).index[0]
    best_delta = float(best["auc"] - scalar_auc)
    best_perm = perm[(perm["subset"] == "bounded") & (perm["feature"] == "best_of_coupled_candidates")].iloc[0]
    cohort_drops = []
    for cohort in df[df["domain"] == "bounded"]["cohort"].unique():
        cm = metrics[(metrics["subset"] == "bounded") & (metrics["cohort"] == cohort)].set_index("feature")
        cohort_drops.append(float(cm.loc[best_feature, "auc"] - cm.loc["locked_signed_score", "auc"]))
    successor_warranted = (
        best_delta >= 0.05
        and float(best_perm["max_candidate_null_p"]) < 0.10
        and float(best["hedges_g"]) >= scalar_g
        and min(cohort_drops) >= -0.10
    )
    summary = {
        "seed": SEED,
        "n_permutations": N_PERM,
        "n_bootstrap": N_BOOT,
        "bounded_scalar_auc": scalar_auc,
        "bounded_scalar_hedges_g": scalar_g,
        "bounded_best_coupled_feature": best_feature,
        "bounded_best_coupled_auc": float(best["auc"]),
        "bounded_best_coupled_hedges_g": float(best["hedges_g"]),
        "bounded_best_delta_auc": best_delta,
        "bounded_max_candidate_permutation_p": float(best_perm["max_candidate_null_p"]),
        "bounded_best_null_p95_delta_auc": float(best_perm["null_p95_delta_auc"]),
        "bounded_cohort_auc_deltas_vs_scalar": cohort_drops,
        "successor_warranted": bool(successor_warranted),
        "verdict": "lock_successor" if successor_warranted else "no_successor_lock_scalar_remains_best_available",
    }
    (OUT / "v27_comparison_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
