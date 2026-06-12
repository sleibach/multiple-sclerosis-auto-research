#!/usr/bin/env python3
"""Stress-test V44 batch diagnostics under interacting technical confounders.

Synthetic data are method-characterization artifacts only. This script does not
read real Gafson data, does not change the immutable V22 rule, and does not
change the frozen V42/V44 validation harness.
"""

from __future__ import annotations

import gzip
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v45_multiconfounder_batch_guard"
SYNTHETIC = OUT / "synthetic"
OUT.mkdir(parents=True, exist_ok=True)
SYNTHETIC.mkdir(parents=True, exist_ok=True)

SEED = 45045
N_PER_GROUP = 30
REPLICATES = 80
SEVERITIES = [0.0, 0.25, 0.50, 0.75, 1.00]
TRUTHS = ["synthetic_null", "planted"]
SCENARIOS = [
    "independent_technical",
    "batch_only",
    "distributed_weak_technical",
    "batch_plus_depth",
    "batch_plus_steroid",
    "immune_tone_plus_batch",
    "normalization_plus_depth",
]


@dataclass(frozen=True)
class SimSpec:
    truth: str
    scenario: str
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
    values = np.asarray(values, dtype=float)
    design = np.column_stack([np.ones(len(x)), x.to_numpy(float)])
    beta = np.linalg.lstsq(design, values, rcond=None)[0]
    return values - design @ beta


def pass_like(n: int, auc: float, g: float, receptor_auc: float) -> bool:
    if not np.isfinite(auc) or not np.isfinite(g):
        return False
    receptor_bad = np.isfinite(receptor_auc) and receptor_auc - auc >= 0.10
    return bool(n >= 30 and auc >= 0.70 and g >= 0.50 and not receptor_bad)


def response_correlated_binary(rng: np.random.Generator, y: np.ndarray, severity: float, base: float = 0.50) -> np.ndarray:
    prob = np.clip(base + severity * 0.35 * (y - 0.5) * 2, 0.02, 0.98)
    return (rng.random(len(y)) < prob).astype(float)


def simulate(spec: SimSpec) -> pd.DataFrame:
    rng = np.random.default_rng(spec.seed)
    n = N_PER_GROUP * 2
    y = np.array([1] * N_PER_GROUP + [0] * N_PER_GROUP, dtype=int)
    rng.shuffle(y)

    truth_signal = np.zeros(n)
    if spec.truth == "planted":
        truth_signal = 1.0 * y + rng.normal(0, 0.40, n)

    # Technical and biological-context covariates. These are not biology claims;
    # they are synthetic proxies for real-world data pathologies.
    batch = rng.integers(0, 2, n).astype(float)
    lane = rng.integers(0, 2, n).astype(float)
    depth = rng.normal(0, 1.0, n)
    rin = rng.normal(0, 1.0, n)
    steroid = rng.normal(0, 1.0, n)
    immune_tone = rng.normal(0, 1.0, n)

    s = spec.severity
    if spec.scenario == "batch_only":
        batch = response_correlated_binary(rng, y, s)
    elif spec.scenario == "distributed_weak_technical":
        # Each feature is only weakly response-correlated, but the joint
        # technical axis can be strong. This is the main blind-spot stress test.
        batch = response_correlated_binary(rng, y, s * 0.45)
        lane = response_correlated_binary(rng, y, s * 0.40)
        depth = 0.30 * s * y + rng.normal(0, 1.0, n)
        rin = -0.25 * s * y + rng.normal(0, 1.0, n)
    elif spec.scenario == "batch_plus_depth":
        batch = response_correlated_binary(rng, y, s)
        depth = 0.80 * s * y + rng.normal(0, 1.0, n)
    elif spec.scenario == "batch_plus_steroid":
        batch = response_correlated_binary(rng, y, s * 0.75)
        steroid = 0.90 * s * y + rng.normal(0, 1.0, n)
    elif spec.scenario == "immune_tone_plus_batch":
        batch = response_correlated_binary(rng, y, s * 0.60)
        immune_tone = 0.90 * s * y + rng.normal(0, 1.0, n)
    elif spec.scenario == "normalization_plus_depth":
        depth = 1.10 * s * y + rng.normal(0, 1.0, n)
        rin = -0.70 * s * y + rng.normal(0, 1.0, n)

    technical_axis = (
        0.45 * (batch - batch.mean())
        + 0.35 * (lane - lane.mean())
        + 0.30 * depth
        - 0.25 * rin
        + 0.35 * steroid
    )
    locked_latent = truth_signal + rng.normal(0, 0.80, n)
    if spec.scenario != "independent_technical":
        locked_latent += s * technical_axis
    if spec.scenario == "immune_tone_plus_batch":
        locked_latent = 0.65 * locked_latent + 0.45 * immune_tone
    if spec.scenario == "normalization_plus_depth":
        locked_latent += 0.65 * s * depth - 0.35 * s * rin

    receptor = rng.normal(0, 0.80, n) + (0.10 * s * technical_axis)
    if spec.scenario == "batch_plus_depth":
        receptor += 0.25 * s * depth
    df = pd.DataFrame(
        {
            "synthetic": True,
            "patient": [f"S{i:04d}" for i in range(n)],
            "response_observed": y,
            "locked_score": locked_latent,
            "delta_RECEPTOR": receptor,
            "batch": batch,
            "lane": lane,
            "sequencing_depth": depth,
            "rin": rin,
            "steroid_exposure": steroid,
            "immune_tone": immune_tone,
            "truth": spec.truth,
            "scenario": spec.scenario,
            "severity": spec.severity,
            "replicate": spec.replicate,
            "seed": spec.seed,
        }
    )
    return df


def feature_guard_metrics(y: np.ndarray, score: np.ndarray, values: pd.Series) -> dict[str, float | bool]:
    vals = pd.to_numeric(values, errors="coerce")
    metadata_auc = auc_score(y, vals.to_numpy(float))
    if np.isfinite(metadata_auc) and metadata_auc < 0.5:
        metadata_auc = 1.0 - metadata_auc
    corr = float(pd.Series(vals).corr(pd.Series(score), method="spearman"))
    resid = residualize(score, pd.DataFrame({"feature": vals}))
    residual_auc = auc_score(y, resid)
    if np.isfinite(residual_auc) and residual_auc < 0.5:
        resid = -resid
        residual_auc = auc_score(y, resid)
    attenuation = auc_score(y, score) - residual_auc
    risky = (
        (np.isfinite(metadata_auc) and metadata_auc >= 0.60)
        or (np.isfinite(corr) and abs(corr) >= 0.35)
        or (np.isfinite(attenuation) and attenuation >= 0.05)
    )
    return {
        "metadata_auc": metadata_auc,
        "spearman_with_locked": corr,
        "residualized_auc": residual_auc,
        "auc_attenuation": attenuation,
        "risk": bool(risky),
    }


def evaluate(group: pd.DataFrame) -> dict[str, object]:
    y = group["response_observed"].to_numpy(int)
    score = group["locked_score"].to_numpy(float)
    receptor = group["delta_RECEPTOR"].to_numpy(float)
    auc = auc_score(y, score)
    g = hedges_g(y, score)
    receptor_auc = auc_score(y, receptor)
    primary_pass = pass_like(len(group), auc, g, receptor_auc)

    technical_features = ["batch", "lane", "sequencing_depth", "rin", "steroid_exposure"]
    per_feature = {feature: feature_guard_metrics(y, score, group[feature]) for feature in technical_features}
    individual_guard = any(metric["risk"] for metric in per_feature.values())

    tech = group[technical_features].copy()
    joint_resid = residualize(score, tech)
    joint_auc = auc_score(y, joint_resid)
    if np.isfinite(joint_auc) and joint_auc < 0.5:
        joint_resid = -joint_resid
        joint_auc = auc_score(y, joint_resid)
    joint_attenuation = auc - joint_auc
    joint_guard = bool(np.isfinite(joint_attenuation) and joint_attenuation >= 0.05)

    return {
        "n": int(len(group)),
        "auc": auc,
        "hedges_g": g,
        "receptor_auc": receptor_auc,
        "primary_pass": bool(primary_pass),
        "individual_guard_flag": bool(individual_guard),
        "individual_guarded_acceptable_pass": bool(primary_pass and not individual_guard),
        "joint_technical_auc": joint_auc,
        "joint_technical_attenuation": joint_attenuation,
        "joint_guard_flag": joint_guard,
        "joint_guarded_acceptable_pass": bool(primary_pass and not joint_guard),
        "max_feature_metadata_auc": max(float(m["metadata_auc"]) for m in per_feature.values() if np.isfinite(m["metadata_auc"])),
        "max_feature_abs_spearman": max(abs(float(m["spearman_with_locked"])) for m in per_feature.values() if np.isfinite(m["spearman_with_locked"])),
        "max_feature_attenuation": max(float(m["auc_attenuation"]) for m in per_feature.values() if np.isfinite(m["auc_attenuation"])),
        "feature_flags": ";".join([feature for feature, metric in per_feature.items() if metric["risk"]]),
    }


def main() -> int:
    subject_path = SYNTHETIC / "multiconfounder_subjects.tsv.gz"
    metric_rows = []
    first = True
    with gzip.open(subject_path, "wt") as handle:
        for truth in TRUTHS:
            for scenario in SCENARIOS:
                for severity in SEVERITIES:
                    for replicate in range(REPLICATES):
                        seed = SEED + len(metric_rows)
                        spec = SimSpec(truth=truth, scenario=scenario, severity=severity, replicate=replicate, seed=seed)
                        df = simulate(spec)
                        df.to_csv(handle, sep="\t", index=False, header=first)
                        first = False
                        record = {
                            "truth": truth,
                            "scenario": scenario,
                            "severity": severity,
                            "replicate": replicate,
                            "seed": seed,
                        }
                        record.update(evaluate(df))
                        metric_rows.append(record)

    metrics = pd.DataFrame(metric_rows)
    metrics.to_csv(OUT / "multiconfounder_batch_guard_metrics.tsv", sep="\t", index=False)
    summary = (
        metrics.groupby(["truth", "scenario", "severity"], as_index=False)
        .agg(
            cohorts=("primary_pass", "size"),
            primary_pass_rate=("primary_pass", "mean"),
            individual_guard_flag_rate=("individual_guard_flag", "mean"),
            individual_guarded_acceptable_pass_rate=("individual_guarded_acceptable_pass", "mean"),
            joint_guard_flag_rate=("joint_guard_flag", "mean"),
            joint_guarded_acceptable_pass_rate=("joint_guarded_acceptable_pass", "mean"),
            mean_auc=("auc", "mean"),
            mean_joint_technical_attenuation=("joint_technical_attenuation", "mean"),
            mean_max_feature_metadata_auc=("max_feature_metadata_auc", "mean"),
            mean_max_feature_abs_spearman=("max_feature_abs_spearman", "mean"),
            mean_max_feature_attenuation=("max_feature_attenuation", "mean"),
        )
    )
    summary.to_csv(OUT / "multiconfounder_batch_guard_summary.tsv", sep="\t", index=False)

    null = summary[summary["truth"].eq("synthetic_null")]
    planted = summary[summary["truth"].eq("planted")]
    worst_rows = []
    for scenario in SCENARIOS:
        nrow = null[null["scenario"].eq(scenario)].sort_values("individual_guarded_acceptable_pass_rate", ascending=False).head(1)
        prow = planted[planted["scenario"].eq(scenario)].sort_values("individual_guarded_acceptable_pass_rate", ascending=True).head(1)
        if not nrow.empty:
            worst_rows.append(
                {
                    "scenario": scenario,
                    "truth": "synthetic_null",
                    "worst_severity": float(nrow["severity"].iloc[0]),
                    "primary_pass_rate": float(nrow["primary_pass_rate"].iloc[0]),
                    "individual_guarded_acceptable_pass_rate": float(nrow["individual_guarded_acceptable_pass_rate"].iloc[0]),
                    "joint_guarded_acceptable_pass_rate": float(nrow["joint_guarded_acceptable_pass_rate"].iloc[0]),
                }
            )
        if not prow.empty:
            worst_rows.append(
                {
                    "scenario": scenario,
                    "truth": "planted",
                    "worst_severity": float(prow["severity"].iloc[0]),
                    "primary_pass_rate": float(prow["primary_pass_rate"].iloc[0]),
                    "individual_guarded_acceptable_pass_rate": float(prow["individual_guarded_acceptable_pass_rate"].iloc[0]),
                    "joint_guarded_acceptable_pass_rate": float(prow["joint_guarded_acceptable_pass_rate"].iloc[0]),
                }
            )
    worst = pd.DataFrame(worst_rows)
    worst.to_csv(OUT / "multiconfounder_worst_cases.tsv", sep="\t", index=False)

    out = {
        "synthetic": True,
        "seed": SEED,
        "cohorts": int(len(metrics)),
        "subjects": int(len(metrics) * N_PER_GROUP * 2),
        "replicates_per_cell": REPLICATES,
        "scenarios": SCENARIOS,
        "worst_null_individual_guarded_acceptable_pass_rate": float(null["individual_guarded_acceptable_pass_rate"].max()),
        "worst_null_joint_guarded_acceptable_pass_rate": float(null["joint_guarded_acceptable_pass_rate"].max()),
        "worst_null_primary_pass_rate": float(null["primary_pass_rate"].max()),
        "output_dir": str(OUT),
    }
    (OUT / "summary.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
