#!/usr/bin/env python3
"""Calibrate secondary-lead batch over-flagging on V45 synthetic pathologies.

Synthetic method-characterization only. This does not change the V44 secondary
pre-registrations or any harness threshold.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


OUT = Path("analysis/v45_secondary_batch_calibration")
OUT.mkdir(parents=True, exist_ok=True)

POST_SUBJECTS = Path("analysis/v45_postpartum_pathology/synthetic/postpartum_pathology_subjects.tsv.gz")
POST_METRICS = Path("analysis/v45_postpartum_pathology/postpartum_pathology_metrics.tsv")
TB_SUBJECTS = Path("analysis/v45_tb_compartment_pathology/synthetic/tb_compartment_pathology_subjects.tsv.gz")
TB_METRICS = Path("analysis/v45_tb_compartment_pathology/tb_compartment_pathology_metrics.tsv")

SEED = 45545
N_PERM_DEFAULT = 50


def auc_score(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    ok = np.isfinite(score)
    y = y[ok]
    score = score[ok]
    pos = score[y == 1]
    neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    ranks = pd.Series(score).rank(method="average").to_numpy()
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def residualize(values: np.ndarray, covariate: np.ndarray) -> np.ndarray:
    x = np.asarray(covariate, dtype=float)
    design = np.column_stack([np.ones(len(x)), x])
    beta = np.linalg.lstsq(design, values, rcond=None)[0]
    return values - design @ beta


def batch_effect_metrics(y: np.ndarray, score: np.ndarray, batch: np.ndarray) -> dict[str, float | bool]:
    metadata_auc = auc_score(y, batch)
    if np.isfinite(metadata_auc) and metadata_auc < 0.5:
        metadata_auc = 1.0 - metadata_auc
    corr = float(pd.Series(batch).corr(pd.Series(score), method="spearman"))
    raw_auc = auc_score(y, score)
    resid = residualize(score, batch)
    residual_auc = auc_score(y, resid)
    if np.isfinite(residual_auc) and residual_auc < 0.5:
        residual_auc = auc_score(y, -resid)
    attenuation = raw_auc - residual_auc
    existing_flag = bool(
        (np.isfinite(metadata_auc) and metadata_auc >= 0.60)
        or (np.isfinite(corr) and abs(corr) >= 0.35)
        or (np.isfinite(attenuation) and attenuation >= 0.05)
    )
    return {
        "batch_metadata_auc": metadata_auc,
        "batch_spearman_with_score": corr,
        "batch_auc_attenuation": attenuation,
        "existing_batch_flag_recomputed": existing_flag,
    }


def permutation_ps(
    y: np.ndarray,
    score: np.ndarray,
    batch: np.ndarray,
    metadata_auc: float,
    corr: float,
    rng: np.random.Generator,
    n_perm: int,
) -> tuple[float, float]:
    obs_auc = abs(metadata_auc - 0.5)
    obs_corr = abs(corr)
    auc_count = 1
    corr_count = 1
    for _ in range(n_perm):
        yp = rng.permutation(y)
        auc_count += abs(auc_score(yp, batch) - 0.5) >= obs_auc
        bp = rng.permutation(batch)
        cp = pd.Series(bp).corr(pd.Series(score), method="spearman")
        corr_count += np.isfinite(cp) and abs(float(cp)) >= obs_corr
    return auc_count / (n_perm + 1), corr_count / (n_perm + 1)


def calibrate_postpartum(n_perm: int, rng: np.random.Generator) -> pd.DataFrame:
    subjects = pd.read_csv(POST_SUBJECTS, sep="\t")
    metrics = pd.read_csv(POST_METRICS, sep="\t")
    rows = []
    group_cols = ["truth", "pathology", "severity", "replicate", "seed"]
    for keys, group in subjects.groupby(group_cols, sort=True):
        rec = dict(zip(group_cols, keys))
        y = group["postpartum_relapse_3m"].to_numpy(int)
        score = group["postpartum_apc_risk_score"].to_numpy(float)
        batch = group["batch"].to_numpy(float)
        bm = batch_effect_metrics(y, score, batch)
        p_resp, p_corr = permutation_ps(y, score, batch, bm["batch_metadata_auc"], bm["batch_spearman_with_score"], rng, n_perm)
        rec.update(bm)
        rec["batch_response_p"] = p_resp
        rec["batch_corr_p"] = p_corr
        rec["calibrated_batch_flag_q10"] = bool(bm["existing_batch_flag_recomputed"] and min(p_resp, p_corr) <= 0.10)
        rows.append(rec)
    cal = pd.DataFrame(rows)
    merged = metrics.merge(cal, on=group_cols, how="left")
    merged["calibrated_guarded_clean_pass"] = merged["primary_pass"].astype(bool) & ~merged["calibrated_batch_flag_q10"].astype(bool)
    merged["lead"] = "postpartum_apc_arm"
    return merged


def calibrate_tb(n_perm: int, rng: np.random.Generator) -> pd.DataFrame:
    subjects = pd.read_csv(TB_SUBJECTS, sep="\t")
    metrics = pd.read_csv(TB_METRICS, sep="\t")
    rows = []
    group_cols = ["truth", "pathology", "severity", "replicate", "seed"]
    for keys, group in subjects.groupby(group_cols, sort=True):
        rec = dict(zip(group_cols, keys))
        y = group["responder"].to_numpy(int)
        score = group["b_plasma_locked_delta"].to_numpy(float)
        batch = group["batch"].to_numpy(float)
        bm = batch_effect_metrics(y, score, batch)
        p_resp, p_corr = permutation_ps(y, score, batch, bm["batch_metadata_auc"], bm["batch_spearman_with_score"], rng, n_perm)
        rec.update(bm)
        rec["batch_response_p"] = p_resp
        rec["batch_corr_p"] = p_corr
        rec["calibrated_batch_flag_q10"] = bool(bm["existing_batch_flag_recomputed"] and min(p_resp, p_corr) <= 0.10)
        rows.append(rec)
    cal = pd.DataFrame(rows)
    merged = metrics.merge(cal, on=group_cols, how="left")
    merged["calibrated_guarded_clean_pass"] = (
        merged["composition_adjusted_pass"].astype(bool)
        & ~merged["coverage_flag"].astype(bool)
        & ~merged["calibrated_batch_flag_q10"].astype(bool)
    )
    merged["lead"] = "tb_compartment"
    return merged


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-perm", type=int, default=N_PERM_DEFAULT)
    args = parser.parse_args()
    rng = np.random.default_rng(SEED)
    post = calibrate_postpartum(args.n_perm, rng)
    tb = calibrate_tb(args.n_perm, rng)
    metrics = pd.concat([post, tb], ignore_index=True, sort=False)
    metrics.to_csv(OUT / "secondary_batch_calibration_metrics.tsv", sep="\t", index=False)
    existing_col = "guarded_clean_pass"
    summary = (
        metrics.groupby(["lead", "truth", "pathology", "severity"], as_index=False)
        .agg(
            cohorts=("calibrated_guarded_clean_pass", "size"),
            existing_guarded_clean_pass_rate=(existing_col, "mean"),
            calibrated_guarded_clean_pass_rate=("calibrated_guarded_clean_pass", "mean"),
            existing_batch_flag_rate=("batch_guard_flag", "mean"),
            calibrated_batch_flag_rate=("calibrated_batch_flag_q10", "mean"),
        )
    )
    summary.to_csv(OUT / "secondary_batch_calibration_summary.tsv", sep="\t", index=False)
    null = summary[summary["truth"].eq("synthetic_null")]
    planted = summary[summary["truth"].eq("planted")]
    out = {
        "synthetic": True,
        "seed": SEED,
        "permutations_per_batch_test": int(args.n_perm),
        "cohorts": int(len(metrics)),
        "worst_null_existing_guarded_clean_pass_rate": float(null["existing_guarded_clean_pass_rate"].max()),
        "worst_null_calibrated_guarded_clean_pass_rate": float(null["calibrated_guarded_clean_pass_rate"].max()),
        "best_planted_existing_guarded_clean_pass_rate": float(planted["existing_guarded_clean_pass_rate"].max()),
        "best_planted_calibrated_guarded_clean_pass_rate": float(planted["calibrated_guarded_clean_pass_rate"].max()),
        "output_dir": str(OUT),
    }
    (OUT / "summary.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

