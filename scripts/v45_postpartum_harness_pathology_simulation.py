#!/usr/bin/env python3
"""Stress-test the V44 postpartum APC-arm validation plan on synthetic pathologies.

Synthetic data are method-characterization artifacts only. This script does not
read any real postpartum MS data and does not change the frozen V44
pre-registration.
"""

from __future__ import annotations

import gzip
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


OUT = Path("analysis/v45_postpartum_pathology")
SYNTHETIC = OUT / "synthetic"
OUT.mkdir(parents=True, exist_ok=True)
SYNTHETIC.mkdir(parents=True, exist_ok=True)

SEED = 45145
N_PER_GROUP = 30
REPLICATES = 90
SEVERITIES = [0.0, 0.25, 0.50, 0.75, 1.00]
TRUTHS = ["synthetic_null", "planted"]
PATHOLOGIES = [
    "missing_postpartum_timepoint",
    "steroid_response_correlated",
    "dmt_restart_imbalance",
    "batch_response_correlated",
    "combined_steroid_dmt_batch",
    "timepoint_jitter",
    "module_coverage_loss",
]


@dataclass(frozen=True)
class SimSpec:
    truth: str
    pathology: str
    severity: float
    replicate: int
    seed: int


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


def bootstrap_auc_ci(y: np.ndarray, score: np.ndarray, rng: np.random.Generator, n_boot: int = 200) -> tuple[float, float]:
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


def response_correlated_binary(rng: np.random.Generator, y: np.ndarray, severity: float, base: float) -> np.ndarray:
    prob = np.clip(base + severity * 0.35 * (y - 0.5) * 2, 0.02, 0.98)
    return (rng.random(len(y)) < prob).astype(float)


def simulate(spec: SimSpec) -> pd.DataFrame:
    rng = np.random.default_rng(spec.seed)
    n = N_PER_GROUP * 2
    y = np.array([1] * N_PER_GROUP + [0] * N_PER_GROUP, dtype=int)
    rng.shuffle(y)
    s = spec.severity

    steroid = rng.normal(0.0, 1.0, n)
    dmt_restart = (rng.random(n) < 0.40).astype(float)
    batch = rng.integers(0, 2, n).astype(float)
    weeks_postpartum = rng.normal(6.0, 0.75, n)
    hla_coverage = np.ones(n)
    cd64_coverage = np.ones(n)

    if spec.pathology == "steroid_response_correlated":
        steroid = 1.10 * s * y + rng.normal(0.0, 1.0, n)
    elif spec.pathology == "dmt_restart_imbalance":
        dmt_restart = response_correlated_binary(rng, y, s, base=0.35)
    elif spec.pathology == "batch_response_correlated":
        batch = response_correlated_binary(rng, y, s, base=0.50)
    elif spec.pathology == "combined_steroid_dmt_batch":
        steroid = 0.80 * s * y + rng.normal(0.0, 1.0, n)
        dmt_restart = response_correlated_binary(rng, y, s * 0.75, base=0.35)
        batch = response_correlated_binary(rng, y, s * 0.75, base=0.50)
    elif spec.pathology == "timepoint_jitter":
        weeks_postpartum = rng.normal(6.0, 0.75 + 2.50 * s, n)
    elif spec.pathology == "module_coverage_loss":
        hla_coverage = np.clip(1.0 - s * rng.beta(2.0, 2.0, n), 0.0, 1.0)
        cd64_coverage = np.clip(1.0 - s * rng.beta(2.0, 3.0, n), 0.0, 1.0)

    healthy_rebound = rng.normal(0.65, 0.35, n)
    if spec.truth == "planted":
        rebound = healthy_rebound - 1.20 * y + rng.normal(0.0, 0.30, n)
    else:
        rebound = healthy_rebound + rng.normal(0.0, 0.35, n)

    # Synthetic confounding effects on the measured HLA-II-minus-CD64 rebound.
    if spec.pathology in {"steroid_response_correlated", "combined_steroid_dmt_batch"}:
        rebound -= 0.55 * s * steroid
    if spec.pathology in {"dmt_restart_imbalance", "combined_steroid_dmt_batch"}:
        rebound += 0.45 * s * dmt_restart
    if spec.pathology in {"batch_response_correlated", "combined_steroid_dmt_batch"}:
        rebound -= 0.70 * s * (batch - batch.mean())
    if spec.pathology == "timepoint_jitter":
        rebound += 0.10 * (weeks_postpartum - 6.0) + rng.normal(0.0, 0.20 * s, n)
    if spec.pathology == "module_coverage_loss":
        rebound += rng.normal(0.0, 1.2 * s * (2.0 - hla_coverage - cd64_coverage), n)

    keep = np.ones(n, dtype=bool)
    if spec.pathology == "missing_postpartum_timepoint":
        keep = rng.random(n) >= 0.45 * s

    arm_late = rng.normal(0.0, 0.70, n)
    arm_6w = arm_late + rebound
    risk_score = -(arm_6w - arm_late)
    frame = pd.DataFrame(
        {
            "synthetic": True,
            "subject": [f"P{i:04d}" for i in range(n)],
            "postpartum_relapse_3m": y,
            "late_pregnancy_hla_minus_cd64": arm_late,
            "postpartum_6w_hla_minus_cd64": arm_6w,
            "postpartum_apc_risk_score": risk_score,
            "steroid_exposure": steroid,
            "dmt_restart": dmt_restart,
            "batch": batch,
            "weeks_postpartum": weeks_postpartum,
            "hla_coverage": hla_coverage,
            "cd64_coverage": cd64_coverage,
            "kept_by_pathology": keep,
            "truth": spec.truth,
            "pathology": spec.pathology,
            "severity": spec.severity,
            "replicate": spec.replicate,
            "seed": spec.seed,
        }
    )
    return frame[frame["kept_by_pathology"]].copy()


def batch_flag(y: np.ndarray, score: np.ndarray, batch: np.ndarray, raw_auc: float) -> bool:
    if len(set(batch)) <= 1:
        return False
    metadata_auc = auc_score(y, batch)
    if np.isfinite(metadata_auc) and metadata_auc < 0.5:
        metadata_auc = 1.0 - metadata_auc
    corr = float(pd.Series(batch).corr(pd.Series(score), method="spearman"))
    resid = residualize(score, pd.DataFrame({"batch": batch}))
    residual_auc = auc_score(y, resid)
    if np.isfinite(residual_auc) and residual_auc < 0.5:
        residual_auc = auc_score(y, -resid)
    attenuation = raw_auc - residual_auc
    return bool(
        (np.isfinite(metadata_auc) and metadata_auc >= 0.60)
        or (np.isfinite(corr) and abs(corr) >= 0.35)
        or (np.isfinite(attenuation) and attenuation >= 0.05)
    )


def evaluate(group: pd.DataFrame, seed: int) -> dict[str, object]:
    y = group["postpartum_relapse_3m"].to_numpy(int)
    score = group["postpartum_apc_risk_score"].to_numpy(float)
    rng = np.random.default_rng(seed + 100_000)
    auc = auc_score(y, score)
    g = hedges_g(y, score)
    ci_low, ci_high = bootstrap_auc_ci(y, score, rng)
    if len(group) < 10 or len(np.unique(y)) < 2:
        return {
            "n": int(len(group)),
            "n_relapse": int(y.sum()) if len(group) else 0,
            "n_no_relapse": int(len(group) - y.sum()) if len(group) else 0,
            "primary_auc": math.nan,
            "primary_hedges_g": math.nan,
            "auc_ci_low": math.nan,
            "auc_ci_high": math.nan,
            "residual_auc_steroid_dmt": math.nan,
            "batch_guard_flag": False,
            "module_coverage_flag": True,
            "primary_pass": False,
            "guarded_clean_pass": False,
            "mechanical_status": "INSUFFICIENT_AFTER_ATTRITION",
        }
    resid = residualize(score, group[["steroid_exposure", "dmt_restart"]])
    resid_auc = auc_score(y, resid)
    if np.isfinite(resid_auc) and resid_auc < 0.5:
        resid_auc = auc_score(y, -resid)
    bflag = batch_flag(y, score, group["batch"].to_numpy(float), auc)
    coverage_flag = bool((group["hla_coverage"].min() < 0.50) or (group["cd64_coverage"].min() <= 0.0))
    primary_pass = bool(auc >= 0.70 and g >= 0.50 and ci_low > 0.55 and resid_auc >= 0.65 and not coverage_flag)
    guarded_clean = bool(primary_pass and not bflag)
    return {
        "n": int(len(group)),
        "n_relapse": int(y.sum()),
        "n_no_relapse": int(len(group) - y.sum()),
        "primary_auc": auc,
        "primary_hedges_g": g,
        "auc_ci_low": ci_low,
        "auc_ci_high": ci_high,
        "residual_auc_steroid_dmt": resid_auc,
        "batch_guard_flag": bflag,
        "module_coverage_flag": coverage_flag,
        "primary_pass": primary_pass,
        "guarded_clean_pass": guarded_clean,
        "mechanical_status": "SCOREABLE",
    }


def main() -> int:
    subject_path = SYNTHETIC / "postpartum_pathology_subjects.tsv.gz"
    rows = []
    first = True
    with gzip.open(subject_path, "wt") as handle:
        for truth in TRUTHS:
            for pathology in PATHOLOGIES:
                for severity in SEVERITIES:
                    for replicate in range(REPLICATES):
                        seed = SEED + len(rows)
                        spec = SimSpec(truth=truth, pathology=pathology, severity=severity, replicate=replicate, seed=seed)
                        frame = simulate(spec)
                        frame.to_csv(handle, sep="\t", index=False, header=first)
                        first = False
                        record = {
                            "truth": truth,
                            "pathology": pathology,
                            "severity": severity,
                            "replicate": replicate,
                            "seed": seed,
                        }
                        record.update(evaluate(frame, seed))
                        rows.append(record)

    metrics = pd.DataFrame(rows)
    metrics.to_csv(OUT / "postpartum_pathology_metrics.tsv", sep="\t", index=False)
    summary = (
        metrics.groupby(["truth", "pathology", "severity"], as_index=False)
        .agg(
            cohorts=("primary_pass", "size"),
            mean_n=("n", "mean"),
            primary_pass_rate=("primary_pass", "mean"),
            guarded_clean_pass_rate=("guarded_clean_pass", "mean"),
            batch_guard_flag_rate=("batch_guard_flag", "mean"),
            module_coverage_flag_rate=("module_coverage_flag", "mean"),
            insufficient_rate=("mechanical_status", lambda x: float((x == "INSUFFICIENT_AFTER_ATTRITION").mean())),
            mean_auc=("primary_auc", "mean"),
            mean_residual_auc_steroid_dmt=("residual_auc_steroid_dmt", "mean"),
        )
    )
    summary.to_csv(OUT / "postpartum_pathology_summary.tsv", sep="\t", index=False)

    null = summary[summary["truth"].eq("synthetic_null")]
    planted = summary[summary["truth"].eq("planted")]
    out = {
        "synthetic": True,
        "seed": SEED,
        "cohorts": int(len(metrics)),
        "subjects_max": int(len(metrics) * N_PER_GROUP * 2),
        "replicates_per_cell": REPLICATES,
        "worst_null_primary_pass_rate": float(null["primary_pass_rate"].max()),
        "worst_null_guarded_clean_pass_rate": float(null["guarded_clean_pass_rate"].max()),
        "worst_planted_guarded_clean_pass_drop": float(1.0 - planted["guarded_clean_pass_rate"].min()),
        "output_dir": str(OUT),
    }
    (OUT / "summary.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

