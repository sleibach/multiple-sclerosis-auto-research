#!/usr/bin/env python3
"""Real-cohort ingestion harness for V44/V45 secondary validation schemas.

This script is validation infrastructure only. It does not read any quarantined
real cohort unless explicitly pointed at one later, and it does not alter any
locked rule or frozen pre-registration.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


SEED = 45645


POST_REQUIRED = [
    "subject",
    "late_pregnancy_sample",
    "postpartum_sample",
    "postpartum_relapse_3m",
    "late_pregnancy_HLAII_minus_CD64",
    "postpartum_6w_HLAII_minus_CD64",
    "postpartum_days",
]
POST_STRONGLY_REQUIRED = [
    "steroid_exposure",
    "dmt_restart",
    "infection",
    "lactation",
    "batch",
    "hla_coverage",
    "cd64_coverage",
]

TB_REQUIRED = [
    "subject",
    "baseline_sample",
    "treated_sample",
    "response",
    "days_since_treatment",
    "b_plasma_locked_delta",
    "t_cell_locked_delta",
]
TB_STRONGLY_REQUIRED = [
    "b_fraction",
    "t_fraction",
    "myeloid_fraction",
    "batch",
    "compartment_method",
    "b_coverage",
    "t_coverage",
    "steroid_exposure",
]


ALIASES = {
    "late_pregnancy_hla_minus_cd64": "late_pregnancy_HLAII_minus_CD64",
    "postpartum_6w_hla_minus_cd64": "postpartum_6w_HLAII_minus_CD64",
    "treated_day": "days_since_treatment",
    "responder": "response",
}


@dataclass(frozen=True)
class HarnessResult:
    metrics: dict[str, object]
    subject_scores: pd.DataFrame
    qc: pd.DataFrame
    batch: pd.DataFrame


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


def bootstrap_auc_ci(y: np.ndarray, score: np.ndarray, rng: np.random.Generator, n_boot: int) -> tuple[float, float]:
    idx = np.arange(len(y))
    aucs = []
    for _ in range(n_boot):
        take = rng.choice(idx, len(idx), replace=True)
        if len(np.unique(y[take])) < 2:
            continue
        aucs.append(auc_score(y[take], score[take]))
    if not aucs:
        return math.nan, math.nan
    return float(np.percentile(aucs, 2.5)), float(np.percentile(aucs, 97.5))


def normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    for old, new in ALIASES.items():
        if old in out.columns and new not in out.columns:
            out = out.rename(columns={old: new})
    return out


def binary_series(values: pd.Series, name: str) -> pd.Series:
    if pd.api.types.is_numeric_dtype(values):
        out = pd.to_numeric(values, errors="coerce")
    else:
        mapping = {
            "1": 1,
            "true": 1,
            "yes": 1,
            "y": 1,
            "responder": 1,
            "response": 1,
            "remission": 1,
            "neda": 1,
            "relapse": 1,
            "relapser": 1,
            "0": 0,
            "false": 0,
            "no": 0,
            "n": 0,
            "nonresponder": 0,
            "non_response": 0,
            "non-response": 0,
            "no_response": 0,
            "no-relapse": 0,
            "no_relapse": 0,
            "relapse_free": 0,
            "stable": 0,
        }
        out = values.astype(str).str.strip().str.lower().map(mapping)
    bad = out.isna()
    if bad.any():
        examples = values[bad].astype(str).head(5).tolist()
        raise ValueError(f"Column {name} contains non-binary values: {examples}")
    unique = sorted(set(out.astype(int)))
    if unique != [0, 1]:
        raise ValueError(f"Column {name} must contain both binary classes; observed {unique}")
    return out.astype(int)


def numeric_series(frame: pd.DataFrame, col: str) -> pd.Series:
    vals = pd.to_numeric(frame[col], errors="coerce")
    if vals.isna().any():
        examples = frame.loc[vals.isna(), col].astype(str).head(5).tolist()
        raise ValueError(f"Column {col} must be numeric; bad examples: {examples}")
    return vals.astype(float)


def present_nonmissing(frame: pd.DataFrame, col: str) -> bool:
    return col in frame.columns and frame[col].notna().any()


def validate_columns(frame: pd.DataFrame, required: Iterable[str]) -> list[dict[str, object]]:
    rows = []
    for col in required:
        exists = col in frame.columns
        nonmissing = bool(exists and frame[col].notna().all())
        rows.append(
            {
                "field": col,
                "required_level": "required",
                "present": exists,
                "complete": nonmissing,
                "missing_count": int(frame[col].isna().sum()) if exists else len(frame),
            }
        )
        if not exists:
            raise ValueError(f"Missing required column: {col}")
        if not nonmissing:
            raise ValueError(f"Required column has missing values: {col}")
    return rows


def add_strong_qc(frame: pd.DataFrame, qc_rows: list[dict[str, object]], cols: Iterable[str]) -> list[str]:
    missing = []
    for col in cols:
        exists = col in frame.columns
        complete = bool(exists and frame[col].notna().all())
        qc_rows.append(
            {
                "field": col,
                "required_level": "strongly_required",
                "present": exists,
                "complete": complete,
                "missing_count": int(frame[col].isna().sum()) if exists else len(frame),
            }
        )
        if not complete:
            missing.append(col)
    return missing


def design_matrix(frame: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    pieces = []
    for col in cols:
        if col not in frame.columns:
            continue
        values = frame[col]
        if pd.api.types.is_numeric_dtype(values):
            pieces.append(pd.DataFrame({col: pd.to_numeric(values, errors="coerce")}))
        else:
            dummies = pd.get_dummies(values.astype(str), prefix=col, drop_first=True, dtype=float)
            if not dummies.empty:
                pieces.append(dummies)
    if not pieces:
        return pd.DataFrame(index=frame.index)
    x = pd.concat(pieces, axis=1)
    return x.replace([np.inf, -np.inf], np.nan).fillna(x.mean(numeric_only=True)).fillna(0.0)


def residualize(values: np.ndarray, covariates: pd.DataFrame) -> np.ndarray:
    if covariates.empty:
        return np.full(len(values), np.nan)
    x = covariates.replace([np.inf, -np.inf], np.nan).fillna(covariates.mean(numeric_only=True)).fillna(0.0)
    design = np.column_stack([np.ones(len(x)), x.to_numpy(float)])
    beta = np.linalg.lstsq(design, values, rcond=None)[0]
    return values - design @ beta


def oriented_residual_auc(y: np.ndarray, score: np.ndarray, covariates: pd.DataFrame) -> float:
    resid = residualize(score, covariates)
    if np.isnan(resid).all():
        return math.nan
    auc = auc_score(y, resid)
    if np.isfinite(auc) and auc < 0.5:
        auc = auc_score(y, -resid)
    return auc


def batch_diagnostics(y: np.ndarray, score: np.ndarray, frame: pd.DataFrame, batch_col: str, raw_auc: float) -> pd.DataFrame:
    if batch_col not in frame.columns or frame[batch_col].isna().all():
        return pd.DataFrame(
            [
                {
                    "field": batch_col,
                    "available": False,
                    "metadata_auc": math.nan,
                    "spearman_with_score": math.nan,
                    "auc_after_residualization": math.nan,
                    "auc_attenuation": math.nan,
                    "batch_guard_flag": True,
                    "reason": "batch_metadata_missing",
                }
            ]
        )
    x = design_matrix(frame, [batch_col])
    if x.empty or x.nunique(dropna=False).max() <= 1:
        return pd.DataFrame(
            [
                {
                    "field": batch_col,
                    "available": True,
                    "metadata_auc": math.nan,
                    "spearman_with_score": math.nan,
                    "auc_after_residualization": raw_auc,
                    "auc_attenuation": 0.0,
                    "batch_guard_flag": False,
                    "reason": "single_batch_or_uninformative",
                }
            ]
        )
    metadata_aucs = []
    corrs = []
    for col in x.columns:
        vals = x[col].to_numpy(float)
        ma = auc_score(y, vals)
        if np.isfinite(ma) and ma < 0.5:
            ma = 1.0 - ma
        metadata_aucs.append(ma)
        corr = pd.Series(vals).corr(pd.Series(score), method="spearman")
        corrs.append(abs(float(corr)) if np.isfinite(corr) else math.nan)
    metadata_auc = float(np.nanmax(metadata_aucs)) if metadata_aucs else math.nan
    score_corr = float(np.nanmax(corrs)) if corrs else math.nan
    resid = residualize(score, x)
    resid_auc = auc_score(y, resid)
    if np.isfinite(resid_auc) and resid_auc < 0.5:
        resid_auc = auc_score(y, -resid)
    attenuation = raw_auc - resid_auc if np.isfinite(raw_auc) and np.isfinite(resid_auc) else math.nan
    flag = bool(
        (np.isfinite(metadata_auc) and metadata_auc >= 0.60)
        or (np.isfinite(score_corr) and score_corr >= 0.35)
        or (np.isfinite(attenuation) and attenuation >= 0.05)
    )
    return pd.DataFrame(
        [
            {
                "field": batch_col,
                "available": True,
                "metadata_auc": metadata_auc,
                "spearman_with_score": score_corr,
                "auc_after_residualization": resid_auc,
                "auc_attenuation": attenuation,
                "batch_guard_flag": flag,
                "reason": "threshold_flag" if flag else "no_threshold_flag",
            }
        ]
    )


def classification_postpartum(metrics: dict[str, object]) -> str:
    if metrics["n"] < 10 or metrics["n_relapse"] == 0 or metrics["n_no_relapse"] == 0:
        return "INCONCLUSIVE_INSUFFICIENT_LABELS"
    if metrics["coverage_flag"]:
        return "INCONCLUSIVE_MODULE_COVERAGE"
    if metrics["guarded_clean_pass"]:
        return "CLEAN_PASS"
    if metrics["primary_pass"] and metrics["batch_guard_flag"]:
        return "RAW_PASS_BATCH_FLAGGED_NON_SPECIFIC"
    if metrics["small_n_directional_pass"]:
        return "SMALL_N_DIRECTIONAL_PASS_PROVISIONAL"
    if metrics["adequate_power_fail"]:
        return "FAIL"
    return "INCONCLUSIVE"


def run_postpartum(input_path: Path, outdir: Path, n_boot: int) -> HarnessResult:
    rng = np.random.default_rng(SEED)
    frame = normalize_columns(pd.read_csv(input_path, sep="\t"))
    is_synthetic = bool("synthetic" in frame.columns and frame["synthetic"].astype(bool).all())
    qc_rows = validate_columns(frame, POST_REQUIRED)
    missing_strong = add_strong_qc(frame, qc_rows, POST_STRONGLY_REQUIRED)

    y = binary_series(frame["postpartum_relapse_3m"], "postpartum_relapse_3m").to_numpy(int)
    late = numeric_series(frame, "late_pregnancy_HLAII_minus_CD64")
    post = numeric_series(frame, "postpartum_6w_HLAII_minus_CD64")
    score = -((post - late).to_numpy(float))
    frame["postpartum_apc_risk_score"] = score
    frame["HLAII_minus_CD64_rebound"] = (post - late).to_numpy(float)
    auc = auc_score(y, score)
    g = hedges_g(y, score)
    ci_low, ci_high = bootstrap_auc_ci(y, score, rng, n_boot)
    residual_auc = oriented_residual_auc(y, score, design_matrix(frame, ["steroid_exposure", "dmt_restart"]))
    batch = batch_diagnostics(y, score, frame, "batch", auc)
    hla_cov_missing = "hla_coverage" not in frame.columns
    cd64_cov_missing = "cd64_coverage" not in frame.columns
    hla_cov = pd.to_numeric(frame["hla_coverage"], errors="coerce") if not hla_cov_missing else pd.Series([math.nan] * len(frame))
    cd64_cov = pd.to_numeric(frame["cd64_coverage"], errors="coerce") if not cd64_cov_missing else pd.Series([math.nan] * len(frame))
    coverage_flag = bool(
        hla_cov_missing
        or cd64_cov_missing
        or hla_cov.isna().any()
        or cd64_cov.isna().any()
        or hla_cov.min() < 0.50
        or cd64_cov.min() <= 0.0
    )
    n = int(len(frame))
    n_relapse = int(y.sum())
    n_no = int(n - n_relapse)
    primary_pass = bool(
        n >= 30
        and auc >= 0.70
        and g >= 0.50
        and ci_low > 0.55
        and np.isfinite(residual_auc)
        and residual_auc >= 0.65
        and not coverage_flag
    )
    small_n = bool(
        n >= 10
        and min(n_relapse, n_no) < 15
        and auc >= 0.70
        and g >= 0.50
        and np.isfinite(residual_auc)
        and residual_auc >= 0.65
        and not coverage_flag
    )
    adequate_fail = bool(n >= 30 and (auc < 0.60 or g < 0.20))
    batch_flag = bool(batch["batch_guard_flag"].iloc[0])
    guarded_clean = bool(primary_pass and not batch_flag and not missing_strong)
    metrics = {
        "lead": "postpartum_apc_arm",
        "synthetic": is_synthetic,
        "n": n,
        "n_relapse": n_relapse,
        "n_no_relapse": n_no,
        "primary_auc": auc,
        "primary_hedges_g": g,
        "auc_ci_low": ci_low,
        "auc_ci_high": ci_high,
        "residual_auc_steroid_dmt": residual_auc,
        "coverage_flag": coverage_flag,
        "batch_guard_flag": batch_flag,
        "missing_strongly_required_fields": ",".join(missing_strong),
        "primary_pass": primary_pass,
        "small_n_directional_pass": small_n,
        "adequate_power_fail": adequate_fail,
        "guarded_clean_pass": guarded_clean,
    }
    metrics["interpretation"] = classification_postpartum(metrics)
    out = frame[
        [
            "subject",
            "late_pregnancy_sample",
            "postpartum_sample",
            "postpartum_relapse_3m",
            "late_pregnancy_HLAII_minus_CD64",
            "postpartum_6w_HLAII_minus_CD64",
            "HLAII_minus_CD64_rebound",
            "postpartum_apc_risk_score",
        ]
    ].copy()
    return HarnessResult(metrics, out, pd.DataFrame(qc_rows), batch)


def classification_tb(metrics: dict[str, object]) -> str:
    if metrics["n"] < 10 or metrics["n_responders"] == 0 or metrics["n_nonresponders"] == 0:
        return "INCONCLUSIVE_INSUFFICIENT_LABELS"
    if metrics["coverage_flag"]:
        return "INCONCLUSIVE_COMPARTMENT_COVERAGE"
    if metrics["guarded_clean_pass"]:
        return "CLEAN_PASS"
    if metrics["composition_adjusted_pass"] and metrics["batch_guard_flag"]:
        return "RAW_PASS_BATCH_FLAGGED_NON_SPECIFIC"
    if metrics["b_plasma_pass"] and metrics["t_cell_auc"] < 0.60:
        return "B_PLASMA_ONLY_DIRECTIONAL_SUPPORT"
    if metrics["small_n_directional_pass"]:
        return "SMALL_N_DIRECTIONAL_PASS_PROVISIONAL"
    if metrics["adequate_power_fail"]:
        return "FAIL"
    return "INCONCLUSIVE"


def run_tb(input_path: Path, outdir: Path, n_boot: int) -> HarnessResult:
    rng = np.random.default_rng(SEED + 1)
    frame = normalize_columns(pd.read_csv(input_path, sep="\t"))
    is_synthetic = bool("synthetic" in frame.columns and frame["synthetic"].astype(bool).all())
    qc_rows = validate_columns(frame, TB_REQUIRED)
    missing_strong = add_strong_qc(frame, qc_rows, TB_STRONGLY_REQUIRED)

    y = binary_series(frame["response"], "response").to_numpy(int)
    b_score = numeric_series(frame, "b_plasma_locked_delta").to_numpy(float)
    t_score = numeric_series(frame, "t_cell_locked_delta").to_numpy(float)
    b_auc = auc_score(y, b_score)
    t_auc = auc_score(y, t_score)
    b_g = hedges_g(y, b_score)
    t_g = hedges_g(y, t_score)
    b_ci_low, b_ci_high = bootstrap_auc_ci(y, b_score, rng, n_boot)
    t_ci_low, t_ci_high = bootstrap_auc_ci(y, t_score, rng, n_boot)
    composition_x = design_matrix(frame, ["b_fraction", "t_fraction", "myeloid_fraction"])
    b_resid_auc = oriented_residual_auc(y, b_score, composition_x)
    t_resid_auc = oriented_residual_auc(y, t_score, composition_x)
    batch = batch_diagnostics(y, b_score, frame, "batch", b_auc)
    b_cov_missing = "b_coverage" not in frame.columns
    t_cov_missing = "t_coverage" not in frame.columns
    b_cov = pd.to_numeric(frame["b_coverage"], errors="coerce") if not b_cov_missing else pd.Series([math.nan] * len(frame))
    t_cov = pd.to_numeric(frame["t_coverage"], errors="coerce") if not t_cov_missing else pd.Series([math.nan] * len(frame))
    coverage_flag = bool(
        b_cov_missing
        or t_cov_missing
        or b_cov.isna().any()
        or t_cov.isna().any()
        or b_cov.min() < 0.50
        or t_cov.min() < 0.50
    )
    n = int(len(frame))
    n_resp = int(y.sum())
    n_non = int(n - n_resp)
    b_pass = bool(n >= 30 and b_auc >= 0.70 and b_g >= 0.50 and b_ci_low > 0.55 and not coverage_flag)
    raw_pass = bool(b_pass and t_auc >= 0.60)
    composition_pass = bool(raw_pass and np.isfinite(b_resid_auc) and b_resid_auc >= 0.65)
    small_n = bool(
        n >= 10
        and min(n_resp, n_non) < 15
        and b_auc >= 0.70
        and b_g >= 0.50
        and t_auc >= 0.60
        and np.isfinite(b_resid_auc)
        and b_resid_auc >= 0.65
        and not coverage_flag
    )
    adequate_fail = bool(n >= 30 and (b_auc < 0.60 or b_g < 0.20 or (np.isfinite(b_resid_auc) and b_resid_auc < 0.55)))
    batch_flag = bool(batch["batch_guard_flag"].iloc[0])
    guarded_clean = bool(composition_pass and not batch_flag and not missing_strong)
    metrics = {
        "lead": "tb_compartment",
        "synthetic": is_synthetic,
        "n": n,
        "n_responders": n_resp,
        "n_nonresponders": n_non,
        "b_plasma_auc": b_auc,
        "b_plasma_hedges_g": b_g,
        "b_plasma_auc_ci_low": b_ci_low,
        "b_plasma_auc_ci_high": b_ci_high,
        "t_cell_auc": t_auc,
        "t_cell_hedges_g": t_g,
        "t_cell_auc_ci_low": t_ci_low,
        "t_cell_auc_ci_high": t_ci_high,
        "b_plasma_residual_auc": b_resid_auc,
        "t_cell_residual_auc": t_resid_auc,
        "coverage_flag": coverage_flag,
        "batch_guard_flag": batch_flag,
        "missing_strongly_required_fields": ",".join(missing_strong),
        "b_plasma_pass": b_pass,
        "raw_pass": raw_pass,
        "composition_adjusted_pass": composition_pass,
        "small_n_directional_pass": small_n,
        "adequate_power_fail": adequate_fail,
        "guarded_clean_pass": guarded_clean,
    }
    metrics["interpretation"] = classification_tb(metrics)
    out = frame[
        [
            "subject",
            "baseline_sample",
            "treated_sample",
            "response",
            "b_plasma_locked_delta",
            "t_cell_locked_delta",
        ]
    ].copy()
    return HarnessResult(metrics, out, pd.DataFrame(qc_rows), batch)


def write_result(result: HarnessResult, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "validation_summary.json").write_text(json.dumps(result.metrics, indent=2, sort_keys=True) + "\n")
    pd.DataFrame([result.metrics]).to_csv(outdir / "metrics.tsv", sep="\t", index=False)
    result.subject_scores.to_csv(outdir / "subject_scores.tsv", sep="\t", index=False)
    result.qc.to_csv(outdir / "input_qc.tsv", sep="\t", index=False)
    result.batch.to_csv(outdir / "batch_diagnostic_metrics.tsv", sep="\t", index=False)


def make_postpartum_synthetic(path: Path, mode: str) -> None:
    rng = np.random.default_rng(SEED + (1 if mode == "planted" else 0))
    n = 60
    y = np.array([1] * 30 + [0] * 30)
    rng.shuffle(y)
    late = rng.normal(0.0, 0.7, n)
    rebound = rng.normal(0.55, 0.30, n)
    if mode == "planted":
        rebound -= 1.15 * y + rng.normal(0.0, 0.10, n)
    else:
        rebound += rng.normal(0.0, 0.25, n)
    post = late + rebound
    frame = pd.DataFrame(
        {
            "synthetic": True,
            "subject": [f"PP{i:03d}" for i in range(n)],
            "late_pregnancy_sample": [f"PP{i:03d}_T3" for i in range(n)],
            "postpartum_sample": [f"PP{i:03d}_W6" for i in range(n)],
            "postpartum_relapse_3m": y,
            "late_pregnancy_HLAII_minus_CD64": late,
            "postpartum_6w_HLAII_minus_CD64": post,
            "postpartum_days": rng.normal(42, 4, n).round(1),
            "steroid_exposure": rng.normal(0.0, 0.5, n),
            "dmt_restart": rng.integers(0, 2, n),
            "infection": 0,
            "lactation": rng.integers(0, 2, n),
            "batch": rng.integers(0, 3, n),
            "hla_coverage": 1.0,
            "cd64_coverage": 1.0,
        }
    )
    frame.to_csv(path, sep="\t", index=False)


def make_tb_synthetic(path: Path, mode: str) -> None:
    rng = np.random.default_rng(SEED + (11 if mode == "planted" else 10))
    n = 60
    y = np.array([1] * 30 + [0] * 30)
    rng.shuffle(y)
    b_frac = np.clip(rng.normal(0.18, 0.04, n), 0.02, 0.60)
    t_frac = np.clip(rng.normal(0.55, 0.07, n), 0.10, 0.90)
    myeloid = np.clip(1.0 - b_frac - t_frac + rng.normal(0.0, 0.03, n), 0.02, 0.70)
    if mode == "planted":
        b = 1.15 * y + rng.normal(0.0, 0.45, n)
        t = 0.45 * y + rng.normal(0.0, 0.55, n)
    else:
        b = rng.normal(0.0, 0.75, n)
        t = rng.normal(0.0, 0.75, n)
    b += 0.15 * (b_frac - b_frac.mean())
    t += 0.15 * (t_frac - t_frac.mean())
    frame = pd.DataFrame(
        {
            "synthetic": True,
            "subject": [f"TB{i:03d}" for i in range(n)],
            "baseline_sample": [f"TB{i:03d}_BL" for i in range(n)],
            "treated_sample": [f"TB{i:03d}_EARLY" for i in range(n)],
            "response": y,
            "days_since_treatment": rng.normal(56, 5, n).round(1),
            "b_plasma_locked_delta": b,
            "t_cell_locked_delta": t,
            "b_fraction": b_frac,
            "t_fraction": t_frac,
            "myeloid_fraction": myeloid,
            "batch": rng.integers(0, 3, n),
            "compartment_method": "synthetic_pseudobulk",
            "b_coverage": 1.0,
            "t_coverage": 1.0,
            "steroid_exposure": rng.normal(0.0, 0.5, n),
        }
    )
    frame.to_csv(path, sep="\t", index=False)


def synthetic_check(outdir: Path, n_boot: int) -> int:
    synth = outdir / "synthetic"
    synth.mkdir(parents=True, exist_ok=True)
    inputs = {
        "postpartum_null": synth / "postpartum_null_input.tsv",
        "postpartum_planted": synth / "postpartum_planted_input.tsv",
        "tb_null": synth / "tb_null_input.tsv",
        "tb_planted": synth / "tb_planted_input.tsv",
    }
    make_postpartum_synthetic(inputs["postpartum_null"], "null")
    make_postpartum_synthetic(inputs["postpartum_planted"], "planted")
    make_tb_synthetic(inputs["tb_null"], "null")
    make_tb_synthetic(inputs["tb_planted"], "planted")

    results = {
        "postpartum_null": run_postpartum(inputs["postpartum_null"], outdir / "postpartum_null", n_boot).metrics,
        "postpartum_planted": run_postpartum(inputs["postpartum_planted"], outdir / "postpartum_planted", n_boot).metrics,
        "tb_null": run_tb(inputs["tb_null"], outdir / "tb_null", n_boot).metrics,
        "tb_planted": run_tb(inputs["tb_planted"], outdir / "tb_planted", n_boot).metrics,
    }
    for key, metrics in results.items():
        lead_out = outdir / key
        if key.startswith("postpartum"):
            write_result(run_postpartum(inputs[key], lead_out, n_boot), lead_out)
        else:
            write_result(run_tb(inputs[key], lead_out, n_boot), lead_out)
    checks = {
        "postpartum_null_expected_fail": not results["postpartum_null"]["guarded_clean_pass"],
        "postpartum_planted_expected_pass": results["postpartum_planted"]["guarded_clean_pass"],
        "tb_null_expected_fail": not results["tb_null"]["guarded_clean_pass"],
        "tb_planted_expected_pass": results["tb_planted"]["guarded_clean_pass"],
    }
    summary = {"synthetic": True, "seed": SEED, "checks": checks, "results": results}
    (outdir / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    pd.DataFrame([{"scenario": k, **v} for k, v in results.items()]).to_csv(
        outdir / "synthetic_check_metrics.tsv", sep="\t", index=False
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_post = sub.add_parser("postpartum", help="Run postpartum APC-arm real-cohort ingestion.")
    p_post.add_argument("--input", required=True, type=Path)
    p_post.add_argument("--outdir", required=True, type=Path)
    p_post.add_argument("--n-boot", type=int, default=1000)

    p_tb = sub.add_parser("tb", help="Run T/B compartment real-cohort ingestion.")
    p_tb.add_argument("--input", required=True, type=Path)
    p_tb.add_argument("--outdir", required=True, type=Path)
    p_tb.add_argument("--n-boot", type=int, default=1000)

    p_check = sub.add_parser("synthetic-check", help="Verify mechanics on labeled synthetic data.")
    p_check.add_argument("--outdir", type=Path, default=Path("analysis/v45_secondary_real_ingest"))
    p_check.add_argument("--n-boot", type=int, default=300)

    args = parser.parse_args()
    if args.cmd == "postpartum":
        result = run_postpartum(args.input, args.outdir, args.n_boot)
        write_result(result, args.outdir)
        print(json.dumps(result.metrics, indent=2, sort_keys=True))
        return 0
    if args.cmd == "tb":
        result = run_tb(args.input, args.outdir, args.n_boot)
        write_result(result, args.outdir)
        print(json.dumps(result.metrics, indent=2, sort_keys=True))
        return 0
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir, args.n_boot)
    raise AssertionError(args.cmd)


if __name__ == "__main__":
    raise SystemExit(main())
