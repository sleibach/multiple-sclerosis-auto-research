#!/usr/bin/env python3
"""Stress-test the V44 T/B compartment monitoring validation plan.

Synthetic data are method-characterization artifacts only. This script does not
read real validation data and does not change the frozen V44 T/B
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


OUT = Path("analysis/v45_tb_compartment_pathology")
SYNTHETIC = OUT / "synthetic"
OUT.mkdir(parents=True, exist_ok=True)
SYNTHETIC.mkdir(parents=True, exist_ok=True)

SEED = 45245
N_PER_GROUP = 30
REPLICATES = 90
SEVERITIES = [0.0, 0.25, 0.50, 0.75, 1.00]
TRUTHS = ["synthetic_null", "planted"]
PATHOLOGIES = [
    "composition_shift_only",
    "b_fraction_response_correlated",
    "t_fraction_response_correlated",
    "compartment_label_noise",
    "batch_response_correlated",
    "timepoint_jitter",
    "low_compartment_coverage",
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


def response_correlated_binary(rng: np.random.Generator, y: np.ndarray, severity: float, base: float = 0.50) -> np.ndarray:
    prob = np.clip(base + severity * 0.35 * (y - 0.5) * 2, 0.02, 0.98)
    return (rng.random(len(y)) < prob).astype(float)


def simulate(spec: SimSpec) -> pd.DataFrame:
    rng = np.random.default_rng(spec.seed)
    n = N_PER_GROUP * 2
    y = np.array([1] * N_PER_GROUP + [0] * N_PER_GROUP, dtype=int)
    rng.shuffle(y)
    s = spec.severity

    b_fraction = np.clip(rng.normal(0.18, 0.05, n), 0.02, 0.55)
    t_fraction = np.clip(rng.normal(0.55, 0.08, n), 0.15, 0.90)
    myeloid_fraction = np.clip(1.0 - b_fraction - t_fraction + rng.normal(0.0, 0.03, n), 0.02, 0.70)
    batch = rng.integers(0, 2, n).astype(float)
    treated_day = rng.normal(56.0, 5.0, n)
    b_coverage = np.ones(n)
    t_coverage = np.ones(n)

    if spec.pathology == "composition_shift_only":
        b_fraction = np.clip(0.12 + 0.18 * s * y + rng.normal(0.0, 0.04, n), 0.02, 0.60)
        t_fraction = np.clip(0.60 - 0.15 * s * y + rng.normal(0.0, 0.06, n), 0.10, 0.90)
    elif spec.pathology == "b_fraction_response_correlated":
        b_fraction = np.clip(0.15 + 0.25 * s * y + rng.normal(0.0, 0.04, n), 0.02, 0.70)
    elif spec.pathology == "t_fraction_response_correlated":
        t_fraction = np.clip(0.50 + 0.25 * s * y + rng.normal(0.0, 0.06, n), 0.10, 0.95)
    elif spec.pathology == "batch_response_correlated":
        batch = response_correlated_binary(rng, y, s)
    elif spec.pathology == "timepoint_jitter":
        treated_day = rng.normal(56.0, 5.0 + 25.0 * s, n)
    elif spec.pathology == "low_compartment_coverage":
        b_coverage = np.clip(1.0 - s * rng.beta(2.0, 2.0, n), 0.0, 1.0)
        t_coverage = np.clip(1.0 - s * rng.beta(2.0, 2.5, n), 0.0, 1.0)

    true_b = np.zeros(n)
    true_t = np.zeros(n)
    if spec.truth == "planted":
        true_b = 1.10 * y + rng.normal(0.0, 0.45, n)
        true_t = 0.55 * y + rng.normal(0.0, 0.55, n)
    else:
        true_b = rng.normal(0.0, 0.70, n)
        true_t = rng.normal(0.0, 0.70, n)

    composition_axis = 1.8 * (b_fraction - b_fraction.mean()) - 0.7 * (t_fraction - t_fraction.mean())
    b_locked = true_b + 1.00 * s * composition_axis + rng.normal(0.0, 0.30, n)
    t_locked = true_t + 0.65 * s * (t_fraction - t_fraction.mean()) + rng.normal(0.0, 0.35, n)
    if spec.pathology == "batch_response_correlated":
        b_locked += 1.00 * s * (batch - batch.mean())
        t_locked += 0.45 * s * (batch - batch.mean())
    if spec.pathology == "timepoint_jitter":
        b_locked += 0.010 * (treated_day - 56.0)
        t_locked += 0.006 * (treated_day - 56.0)
    if spec.pathology == "compartment_label_noise":
        # Synthetic label mixing: B and T readouts leak into each other as
        # compartment identity becomes noisy.
        b_orig = b_locked.copy()
        t_orig = t_locked.copy()
        b_locked = (1.0 - 0.55 * s) * b_orig + (0.55 * s) * t_orig + rng.normal(0.0, 0.20 * s, n)
        t_locked = (1.0 - 0.55 * s) * t_orig + (0.55 * s) * b_orig + rng.normal(0.0, 0.20 * s, n)
    if spec.pathology == "low_compartment_coverage":
        b_locked += rng.normal(0.0, 1.0 * s * (1.0 - b_coverage), n)
        t_locked += rng.normal(0.0, 1.0 * s * (1.0 - t_coverage), n)

    return pd.DataFrame(
        {
            "synthetic": True,
            "subject": [f"TB{i:04d}" for i in range(n)],
            "responder": y,
            "b_plasma_locked_delta": b_locked,
            "t_cell_locked_delta": t_locked,
            "b_fraction": b_fraction,
            "t_fraction": t_fraction,
            "myeloid_fraction": myeloid_fraction,
            "batch": batch,
            "treated_day": treated_day,
            "b_coverage": b_coverage,
            "t_coverage": t_coverage,
            "truth": spec.truth,
            "pathology": spec.pathology,
            "severity": spec.severity,
            "replicate": spec.replicate,
            "seed": spec.seed,
        }
    )


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
    y = group["responder"].to_numpy(int)
    b_score = group["b_plasma_locked_delta"].to_numpy(float)
    t_score = group["t_cell_locked_delta"].to_numpy(float)
    rng = np.random.default_rng(seed + 100_000)
    b_auc = auc_score(y, b_score)
    b_g = hedges_g(y, b_score)
    b_ci_low, b_ci_high = bootstrap_auc_ci(y, b_score, rng)
    t_auc = auc_score(y, t_score)
    t_g = hedges_g(y, t_score)
    composition = group[["b_fraction", "t_fraction", "myeloid_fraction"]]
    b_resid = residualize(b_score, composition)
    t_resid = residualize(t_score, composition)
    b_resid_auc = auc_score(y, b_resid)
    if np.isfinite(b_resid_auc) and b_resid_auc < 0.5:
        b_resid_auc = auc_score(y, -b_resid)
    t_resid_auc = auc_score(y, t_resid)
    if np.isfinite(t_resid_auc) and t_resid_auc < 0.5:
        t_resid_auc = auc_score(y, -t_resid)
    b_batch = batch_flag(y, b_score, group["batch"].to_numpy(float), b_auc)
    coverage_flag = bool((group["b_coverage"].min() < 0.50) or (group["t_coverage"].min() < 0.50))
    raw_pass = bool(b_auc >= 0.70 and b_g >= 0.50 and b_ci_low > 0.55 and t_auc >= 0.60)
    composition_adjusted_pass = bool(raw_pass and b_resid_auc >= 0.65)
    guarded_clean_pass = bool(composition_adjusted_pass and not b_batch and not coverage_flag)
    return {
        "n": int(len(group)),
        "b_plasma_auc": b_auc,
        "b_plasma_hedges_g": b_g,
        "b_plasma_auc_ci_low": b_ci_low,
        "b_plasma_auc_ci_high": b_ci_high,
        "t_cell_auc": t_auc,
        "t_cell_hedges_g": t_g,
        "b_plasma_residual_auc": b_resid_auc,
        "t_cell_residual_auc": t_resid_auc,
        "batch_guard_flag": b_batch,
        "coverage_flag": coverage_flag,
        "raw_pass": raw_pass,
        "composition_adjusted_pass": composition_adjusted_pass,
        "guarded_clean_pass": guarded_clean_pass,
    }


def main() -> int:
    subject_path = SYNTHETIC / "tb_compartment_pathology_subjects.tsv.gz"
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
    metrics.to_csv(OUT / "tb_compartment_pathology_metrics.tsv", sep="\t", index=False)
    summary = (
        metrics.groupby(["truth", "pathology", "severity"], as_index=False)
        .agg(
            cohorts=("raw_pass", "size"),
            raw_pass_rate=("raw_pass", "mean"),
            composition_adjusted_pass_rate=("composition_adjusted_pass", "mean"),
            guarded_clean_pass_rate=("guarded_clean_pass", "mean"),
            batch_guard_flag_rate=("batch_guard_flag", "mean"),
            coverage_flag_rate=("coverage_flag", "mean"),
            mean_b_auc=("b_plasma_auc", "mean"),
            mean_t_auc=("t_cell_auc", "mean"),
            mean_b_residual_auc=("b_plasma_residual_auc", "mean"),
            mean_t_residual_auc=("t_cell_residual_auc", "mean"),
        )
    )
    summary.to_csv(OUT / "tb_compartment_pathology_summary.tsv", sep="\t", index=False)
    null = summary[summary["truth"].eq("synthetic_null")]
    planted = summary[summary["truth"].eq("planted")]
    out = {
        "synthetic": True,
        "seed": SEED,
        "cohorts": int(len(metrics)),
        "subjects": int(len(metrics) * N_PER_GROUP * 2),
        "replicates_per_cell": REPLICATES,
        "worst_null_raw_pass_rate": float(null["raw_pass_rate"].max()),
        "worst_null_composition_adjusted_pass_rate": float(null["composition_adjusted_pass_rate"].max()),
        "worst_null_guarded_clean_pass_rate": float(null["guarded_clean_pass_rate"].max()),
        "worst_planted_guarded_clean_pass_drop": float(1.0 - planted["guarded_clean_pass_rate"].min()),
        "output_dir": str(OUT),
    }
    (OUT / "summary.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

