#!/usr/bin/env python3
"""Calibrate batch-diagnostic over-flagging with permutation/FDR.

This script reuses V45 multi-confounder synthetic cohorts. It tests whether a
permutation/FDR diagnostic can reduce chance over-flagging while preserving
synthetic-null protection. It does not change the frozen validation harness.
"""

from __future__ import annotations

import json
import math
import argparse
from pathlib import Path

import numpy as np
import pandas as pd


IN = Path("analysis/v45_multiconfounder_batch_guard/synthetic/multiconfounder_subjects.tsv.gz")
OUT = Path("analysis/v45_batch_guard_calibration")
OUT.mkdir(parents=True, exist_ok=True)

SEED = 45445
N_PERM_DEFAULT = 50
TECH_FEATURES = ["batch", "lane", "sequencing_depth", "rin", "steroid_exposure"]
GROUP_COLS = ["truth", "scenario", "severity", "replicate", "seed"]


def auc_score(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    ok = np.isfinite(score)
    y = y[ok]
    score = score[ok]
    pos = score[y == 1]
    neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return math.nan
    ranks = pd.Series(score).rank(method="average").to_numpy()
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def hedges_g(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    ok = np.isfinite(score)
    y = y[ok]
    score = score[ok]
    a = score[y == 1]
    b = score[y == 0]
    if len(a) < 2 or len(b) < 2:
        return math.nan
    pooled = math.sqrt(
        ((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1))
        / (len(a) + len(b) - 2)
    )
    if pooled == 0:
        return 0.0
    correction = 1 - 3 / (4 * (len(a) + len(b)) - 9)
    return float(((np.mean(a) - np.mean(b)) / pooled) * correction)


def residualize(values: np.ndarray, covariates: pd.DataFrame) -> np.ndarray:
    x = covariates.copy()
    for col in x.columns:
        x[col] = pd.to_numeric(x[col], errors="coerce")
    x = x.replace([np.inf, -np.inf], np.nan).fillna(x.mean(numeric_only=True)).fillna(0.0)
    design = np.column_stack([np.ones(len(x)), x.to_numpy(float)])
    beta = np.linalg.lstsq(design, values, rcond=None)[0]
    return values - design @ beta


def pass_like(n: int, auc: float, g: float, receptor_auc: float) -> bool:
    receptor_bad = np.isfinite(receptor_auc) and receptor_auc - auc >= 0.10
    return bool(n >= 30 and np.isfinite(auc) and np.isfinite(g) and auc >= 0.70 and g >= 0.50 and not receptor_bad)


def bh_qvalues(pvals: list[float]) -> list[float]:
    p = np.asarray(pvals, dtype=float)
    order = np.argsort(p)
    ranked = p[order]
    q = np.empty_like(ranked)
    m = len(p)
    running = 1.0
    for i in range(m - 1, -1, -1):
        running = min(running, ranked[i] * m / (i + 1))
        q[i] = running
    out = np.empty_like(q)
    out[order] = np.minimum(q, 1.0)
    return out.tolist()


def permutation_p_response_auc(
    y: np.ndarray,
    values: np.ndarray,
    observed_auc: float,
    rng: np.random.Generator,
    n_perm: int,
) -> float:
    observed = abs(observed_auc - 0.5)
    count = 1
    for _ in range(n_perm):
        yp = rng.permutation(y)
        val = auc_score(yp, values)
        count += abs(val - 0.5) >= observed
    return count / (n_perm + 1)


def permutation_p_corr(
    values: np.ndarray,
    score: np.ndarray,
    observed_corr: float,
    rng: np.random.Generator,
    n_perm: int,
) -> float:
    observed = abs(observed_corr)
    count = 1
    values = np.asarray(values, dtype=float)
    for _ in range(n_perm):
        vp = rng.permutation(values)
        corr = pd.Series(vp).corr(pd.Series(score), method="spearman")
        count += np.isfinite(corr) and abs(float(corr)) >= observed
    return count / (n_perm + 1)


def feature_metrics(group: pd.DataFrame, rng: np.random.Generator, n_perm: int) -> tuple[pd.DataFrame, dict[str, bool]]:
    y = group["response_observed"].to_numpy(int)
    score = group["locked_score"].to_numpy(float)
    raw_auc = auc_score(y, score)
    rows = []
    pvals = []
    pval_labels = []
    for feature in TECH_FEATURES:
        values = pd.to_numeric(group[feature], errors="coerce").to_numpy(float)
        metadata_auc = auc_score(y, values)
        if np.isfinite(metadata_auc) and metadata_auc < 0.5:
            metadata_auc = 1.0 - metadata_auc
        corr = float(pd.Series(values).corr(pd.Series(score), method="spearman"))
        resid = residualize(score, pd.DataFrame({feature: values}))
        residual_auc = auc_score(y, resid)
        if np.isfinite(residual_auc) and residual_auc < 0.5:
            residual_auc = auc_score(y, -resid)
        attenuation = raw_auc - residual_auc
        response_p = permutation_p_response_auc(y, values, metadata_auc, rng, n_perm)
        corr_p = permutation_p_corr(values, score, corr, rng, n_perm)
        pvals.extend([response_p, corr_p])
        pval_labels.extend([(feature, "response_q"), (feature, "corr_q")])
        rows.append(
            {
                "feature": feature,
                "metadata_auc": metadata_auc,
                "spearman_with_locked": corr,
                "residualized_auc": residual_auc,
                "auc_attenuation": attenuation,
                "response_p": response_p,
                "corr_p": corr_p,
                "existing_effect_flag": bool(
                    (np.isfinite(metadata_auc) and metadata_auc >= 0.60)
                    or (np.isfinite(corr) and abs(corr) >= 0.35)
                    or (np.isfinite(attenuation) and attenuation >= 0.05)
                ),
            }
        )
    qvals = bh_qvalues(pvals)
    qmap = {label: q for label, q in zip(pval_labels, qvals)}
    for row in rows:
        feature = row["feature"]
        row["response_q"] = qmap[(feature, "response_q")]
        row["corr_q"] = qmap[(feature, "corr_q")]
        row["calibrated_q10_flag"] = bool(
            (
                np.isfinite(row["metadata_auc"])
                and row["metadata_auc"] >= 0.60
                and row["response_q"] <= 0.10
            )
            or (
                np.isfinite(row["spearman_with_locked"])
                and abs(row["spearman_with_locked"]) >= 0.35
                and row["corr_q"] <= 0.10
            )
            or (
                np.isfinite(row["auc_attenuation"])
                and row["auc_attenuation"] >= 0.05
                and row["corr_q"] <= 0.10
            )
        )
        row["calibrated_q20_flag"] = bool(
            (
                np.isfinite(row["metadata_auc"])
                and row["metadata_auc"] >= 0.60
                and row["response_q"] <= 0.20
            )
            or (
                np.isfinite(row["spearman_with_locked"])
                and abs(row["spearman_with_locked"]) >= 0.35
                and row["corr_q"] <= 0.20
            )
            or (
                np.isfinite(row["auc_attenuation"])
                and row["auc_attenuation"] >= 0.05
                and row["corr_q"] <= 0.20
            )
        )
    feature_df = pd.DataFrame(rows)
    flags = {
        "existing_guard_flag": bool(feature_df["existing_effect_flag"].any()),
        "calibrated_q10_guard_flag": bool(feature_df["calibrated_q10_flag"].any()),
        "calibrated_q20_guard_flag": bool(feature_df["calibrated_q20_flag"].any()),
    }
    return feature_df, flags


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-perm", type=int, default=N_PERM_DEFAULT)
    parser.add_argument(
        "--scenarios",
        default="",
        help="Optional comma-separated scenario filter for focused calibration runs.",
    )
    parser.add_argument(
        "--max-replicates-per-cell",
        type=int,
        default=0,
        help="Optional cap on replicate number per truth/scenario/severity cell.",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=OUT,
        help="Output directory. Defaults to the original V45 pilot output path.",
    )
    args = parser.parse_args()
    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(IN, sep="\t")
    if args.scenarios:
        keep = {item.strip() for item in args.scenarios.split(",") if item.strip()}
        df = df[df["scenario"].isin(keep)].copy()
    if args.max_replicates_per_cell > 0:
        df = df[df["replicate"] < args.max_replicates_per_cell].copy()
    cohort_rows = []
    feature_rows = []
    rng = np.random.default_rng(SEED)
    for keys, group in df.groupby(GROUP_COLS, sort=True):
        record = dict(zip(GROUP_COLS, keys))
        y = group["response_observed"].to_numpy(int)
        score = group["locked_score"].to_numpy(float)
        receptor = group["delta_RECEPTOR"].to_numpy(float)
        auc = auc_score(y, score)
        g = hedges_g(y, score)
        receptor_auc = auc_score(y, receptor)
        primary = pass_like(len(group), auc, g, receptor_auc)
        feats, flags = feature_metrics(group, rng, args.n_perm)
        feats.insert(0, "seed", record["seed"])
        feats.insert(0, "replicate", record["replicate"])
        feats.insert(0, "severity", record["severity"])
        feats.insert(0, "scenario", record["scenario"])
        feats.insert(0, "truth", record["truth"])
        feature_rows.append(feats)
        cohort_rows.append(
            {
                **record,
                "n": int(len(group)),
                "auc": auc,
                "hedges_g": g,
                "receptor_auc": receptor_auc,
                "primary_pass": primary,
                **flags,
                "existing_guarded_acceptable_pass": bool(primary and not flags["existing_guard_flag"]),
                "calibrated_q10_acceptable_pass": bool(primary and not flags["calibrated_q10_guard_flag"]),
                "calibrated_q20_acceptable_pass": bool(primary and not flags["calibrated_q20_guard_flag"]),
            }
        )
    cohort = pd.DataFrame(cohort_rows)
    features = pd.concat(feature_rows, ignore_index=True)
    cohort.to_csv(outdir / "batch_guard_calibrated_cohort_metrics.tsv", sep="\t", index=False)
    features.to_csv(outdir / "batch_guard_calibrated_feature_metrics.tsv", sep="\t", index=False)
    summary = (
        cohort.groupby(["truth", "scenario", "severity"], as_index=False)
        .agg(
            cohorts=("primary_pass", "size"),
            primary_pass_rate=("primary_pass", "mean"),
            existing_guard_flag_rate=("existing_guard_flag", "mean"),
            existing_guarded_acceptable_pass_rate=("existing_guarded_acceptable_pass", "mean"),
            calibrated_q10_guard_flag_rate=("calibrated_q10_guard_flag", "mean"),
            calibrated_q10_acceptable_pass_rate=("calibrated_q10_acceptable_pass", "mean"),
            calibrated_q20_guard_flag_rate=("calibrated_q20_guard_flag", "mean"),
            calibrated_q20_acceptable_pass_rate=("calibrated_q20_acceptable_pass", "mean"),
            mean_auc=("auc", "mean"),
        )
    )
    summary.to_csv(outdir / "batch_guard_calibration_summary.tsv", sep="\t", index=False)
    null = summary[summary["truth"].eq("synthetic_null")]
    planted = summary[summary["truth"].eq("planted")]
    independent_planted = summary[
        summary["truth"].eq("planted")
        & summary["scenario"].eq("independent_technical")
        & summary["severity"].eq(0.0)
    ].iloc[0]
    out = {
        "synthetic": True,
        "seed": SEED,
        "cohorts": int(len(cohort)),
        "features_tested": int(len(features)),
        "permutations_per_feature_test": int(args.n_perm),
        "scenario_filter": args.scenarios or "all",
        "max_replicates_per_cell": int(args.max_replicates_per_cell),
        "worst_null_existing_acceptable_pass": float(null["existing_guarded_acceptable_pass_rate"].max()),
        "worst_null_calibrated_q10_acceptable_pass": float(null["calibrated_q10_acceptable_pass_rate"].max()),
        "worst_null_calibrated_q20_acceptable_pass": float(null["calibrated_q20_acceptable_pass_rate"].max()),
        "planted_independent_existing_acceptable_pass": float(independent_planted["existing_guarded_acceptable_pass_rate"]),
        "planted_independent_calibrated_q10_acceptable_pass": float(independent_planted["calibrated_q10_acceptable_pass_rate"]),
        "planted_independent_calibrated_q20_acceptable_pass": float(independent_planted["calibrated_q20_acceptable_pass_rate"]),
        "output_dir": str(outdir),
    }
    (outdir / "summary.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
