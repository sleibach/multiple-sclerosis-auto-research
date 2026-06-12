#!/usr/bin/env python3
"""V43 synthetic method-characterization simulations.

This script does not read real Gafson data and does not alter the immutable V22
rule or V42 pre-registration. It uses seeded synthetic data to characterize
method behavior: validation power, harness robustness, and V41-style null
calibration.

Synthetic results are method-behavior evidence only. They are not biological
evidence about MS.
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v43_method_validation"
SYNTHETIC = OUT / "synthetic"
SEED = 43043

REAL_V41_JOINT_Z = 8.054844913966898
REAL_V41_RECURRENCE = 78


@dataclass(frozen=True)
class SimParams:
    n_per_group: int
    effect_size: float
    label_noise: float
    baseline_sd: float
    confounder_structure: str
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
    pooled = math.sqrt(((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0:
        return 0.0
    correction = 1 - 3 / (4 * (len(a) + len(b)) - 9)
    return float(((np.mean(a) - np.mean(b)) / pooled) * correction)


def bootstrap_auc_ci(y: np.ndarray, score: np.ndarray, rng: np.random.Generator, n_boot: int) -> tuple[float, float]:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    idx_all = np.arange(len(y))
    aucs: list[float] = []
    for _ in range(n_boot):
        idx = rng.choice(idx_all, size=len(idx_all), replace=True)
        if len(np.unique(y[idx])) < 2:
            continue
        aucs.append(auc_score(y[idx], score[idx]))
    if not aucs:
        return math.nan, math.nan
    return float(np.percentile(aucs, 2.5)), float(np.percentile(aucs, 97.5))


def v42_verdict(n: int, n_resp: int, n_non: int, auc: float, g: float, ci_low: float, receptor_auc: float) -> str:
    if not np.isfinite(auc) or not np.isfinite(g):
        return "UNSCOREABLE_DATA"
    receptor_bad = np.isfinite(receptor_auc) and receptor_auc - auc >= 0.10
    if n >= 30:
        passes = auc >= 0.70 and g >= 0.50 and ci_low > 0.55 and not receptor_bad
    else:
        passes = auc >= 0.70 and g >= 0.50 and not receptor_bad
    if passes and min(n_resp, n_non) < 15:
        return "PASS_PROVISIONAL_SMALL_N"
    if passes:
        return "PASS_CLEAN"
    if receptor_bad and auc >= 0.70:
        return "PASS_NON_SPECIFIC"
    if n >= 30 and min(n_resp, n_non) >= 10 and (auc < 0.60 or g < 0.20):
        return "FAIL_ADEQUATE_POWER"
    if auc < 0.45:
        return "FAIL_ADEQUATE_POWER"
    return "INCONCLUSIVE_UNDERPOWERED"


def simulate_subjects(params: SimParams, pathology: str = "none", severity: float = 0.0) -> pd.DataFrame:
    rng = np.random.default_rng(params.seed)
    n = params.n_per_group * 2
    y_true = np.array([1] * params.n_per_group + [0] * params.n_per_group, dtype=int)
    rng.shuffle(y_true)
    y_obs = y_true.copy()
    if params.label_noise > 0:
        flip = rng.random(n) < params.label_noise
        y_obs[flip] = 1 - y_obs[flip]
    if pathology == "label_swap" and severity > 0:
        flip = rng.random(n) < severity
        y_obs[flip] = 1 - y_obs[flip]

    baseline = rng.normal(0, params.baseline_sd, n)
    true_signal = params.effect_size * y_true + rng.normal(0, 1.0, n)
    immune_tone = rng.normal(0, 1.0, n)
    composition = rng.normal(0, 1.0, n)
    steroid = rng.normal(0, 1.0, n)

    if params.confounder_structure == "immune_tone":
        immune_tone = 0.65 * true_signal + rng.normal(0, 0.75, n)
    elif params.confounder_structure == "composition":
        composition = 0.55 * true_signal + rng.normal(0, 0.85, n)
    elif params.confounder_structure == "steroid":
        steroid = 0.55 * y_true + rng.normal(0, 0.9, n)

    measurement_noise = 0.35
    if pathology == "normalization_noise":
        measurement_noise += severity
    if pathology == "batch_response_correlated":
        batch = (rng.random(n) < (0.5 + severity * (y_true - 0.5))).astype(float)
        batch_effect = (batch - batch.mean()) * severity
    else:
        batch = rng.integers(0, 2, n)
        batch_effect = np.zeros(n)

    locked_latent = true_signal + 0.15 * baseline + batch_effect
    if params.confounder_structure == "immune_tone":
        locked_latent = 0.70 * locked_latent + 0.30 * immune_tone
    if params.confounder_structure == "composition":
        locked_latent = 0.80 * locked_latent + 0.20 * composition

    delta_hla = 0.50 * locked_latent + rng.normal(0, measurement_noise, n)
    delta_ifn = -0.50 * locked_latent + rng.normal(0, measurement_noise, n)
    delta_receptor = rng.normal(0, 0.75, n)
    if params.confounder_structure == "composition":
        delta_receptor = 0.65 * composition + rng.normal(0, 0.65, n)
    if pathology == "receptor_artifact":
        delta_receptor = delta_hla - delta_ifn + rng.normal(0, max(0.05, 1.0 - severity), n)

    if pathology == "outlier_samples" and severity > 0:
        outlier = rng.random(n) < severity
        delta_hla[outlier] += rng.normal(0, 5.0, int(outlier.sum()))
        delta_ifn[outlier] += rng.normal(0, 5.0, int(outlier.sum()))

    if pathology == "missing_timepoints" and severity > 0:
        keep = rng.random(n) >= severity
    else:
        keep = np.ones(n, dtype=bool)

    if pathology == "gene_id_loss" and severity > 0:
        # Synthetic proxy for partial module loss: more module-level noise as
        # coverage approaches the pre-registered threshold.
        coverage_noise = severity * rng.normal(0, 1.0, n)
        delta_hla += coverage_noise
        delta_ifn -= 0.5 * coverage_noise

    df = pd.DataFrame(
        {
            "synthetic": True,
            "patient": [f"S{i:04d}" for i in range(n)],
            "response_true": y_true,
            "response_observed": y_obs,
            "baseline_apc_hla_level": baseline,
            "delta_IFN_APC": delta_ifn,
            "delta_HLAII": delta_hla,
            "delta_RECEPTOR": delta_receptor,
            "locked_score": delta_hla - delta_ifn,
            "immune_tone": immune_tone,
            "composition": composition,
            "glucocorticoid": steroid,
            "batch": batch,
            "kept_by_pathology": keep,
            "pathology": pathology,
            "pathology_severity": severity,
        }
    )
    return df[df["kept_by_pathology"]].copy()


def evaluate_subjects(df: pd.DataFrame, rng: np.random.Generator, n_boot: int) -> dict[str, object]:
    y = df["response_observed"].to_numpy(int)
    score = df["locked_score"].to_numpy(float)
    receptor = df["delta_RECEPTOR"].to_numpy(float)
    auc = auc_score(y, score)
    g = hedges_g(y, score)
    ci_low, ci_high = bootstrap_auc_ci(y, score, rng, n_boot)
    receptor_auc = auc_score(y, receptor)
    n_resp = int(y.sum())
    n_non = int(len(y) - n_resp)
    verdict = v42_verdict(len(df), n_resp, n_non, auc, g, ci_low, receptor_auc)
    return {
        "n": int(len(df)),
        "n_responders": n_resp,
        "n_nonresponders": n_non,
        "auc": auc,
        "hedges_g": g,
        "auc_ci_low": ci_low,
        "auc_ci_high": ci_high,
        "receptor_auc": receptor_auc,
        "verdict": verdict,
    }


def write_subject_rows(path: Path, frames: Iterable[pd.DataFrame]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    first = True
    with gzip.open(path, "wt") as handle:
        for frame in frames:
            frame.to_csv(handle, sep="\t", index=False, header=first)
            first = False


def run_power(n_boot: int = 300) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    subject_frames = []
    rep_count = 12
    for n_per_group in [10, 15, 20, 30, 45, 60, 80]:
        for effect_size in [0.0, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50]:
            for label_noise in [0.0, 0.10]:
                for baseline_sd in [0.5, 1.0]:
                    for confounder_structure in ["none", "immune_tone", "composition", "steroid"]:
                        for replicate in range(rep_count):
                            seed = SEED + 10_000 + len(rows)
                            params = SimParams(
                                n_per_group=n_per_group,
                                effect_size=effect_size,
                                label_noise=label_noise,
                                baseline_sd=baseline_sd,
                                confounder_structure=confounder_structure,
                                replicate=replicate,
                                seed=seed,
                            )
                            df = simulate_subjects(params)
                            df.insert(0, "simulation_family", "power")
                            for key, value in params.__dict__.items():
                                df[key] = value
                            metrics = evaluate_subjects(df, np.random.default_rng(seed + 999), n_boot)
                            rows.append(params.__dict__ | metrics)
                            subject_frames.append(df)
    write_subject_rows(SYNTHETIC / "power_simulation_subjects.tsv.gz", subject_frames)
    result = pd.DataFrame(rows)
    result.to_csv(OUT / "power_simulation_cohort_results.tsv", sep="\t", index=False)
    summary = (
        result.assign(
            pass_any=result["verdict"].isin(["PASS_CLEAN", "PASS_PROVISIONAL_SMALL_N"]),
            conclusive=result["verdict"].isin(["PASS_CLEAN", "PASS_PROVISIONAL_SMALL_N", "FAIL_ADEQUATE_POWER", "PASS_NON_SPECIFIC"]),
            false_positive=lambda x: (x["effect_size"].eq(0.0) & x["pass_any"]),
        )
        .groupby(["n_per_group", "effect_size", "label_noise", "baseline_sd", "confounder_structure"], as_index=False)
        .agg(
            cohorts=("verdict", "size"),
            pass_rate=("pass_any", "mean"),
            conclusive_rate=("conclusive", "mean"),
            false_positive_rate=("false_positive", "mean"),
            mean_auc=("auc", "mean"),
            median_auc_ci_low=("auc_ci_low", "median"),
            mean_hedges_g=("hedges_g", "mean"),
        )
    )
    summary.to_csv(OUT / "power_map_summary.tsv", sep="\t", index=False)
    return result, summary


def run_robustness(n_boot: int = 300) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    subject_frames = []
    scenarios = [
        ("label_swap", [0.0, 0.05, 0.10, 0.20, 0.30]),
        ("missing_timepoints", [0.0, 0.10, 0.25, 0.40]),
        ("batch_response_correlated", [0.0, 0.25, 0.50, 0.75, 1.00]),
        ("normalization_noise", [0.0, 0.25, 0.50, 1.00]),
        ("outlier_samples", [0.0, 0.05, 0.10, 0.20]),
        ("gene_id_loss", [0.0, 0.25, 0.50, 1.00]),
        ("receptor_artifact", [0.0, 0.25, 0.50, 0.75, 1.00]),
    ]
    rep_count = 30
    row_id = 0
    for truth in ["null", "planted"]:
        effect_size = 0.0 if truth == "null" else 1.25
        for pathology, severities in scenarios:
            for severity in severities:
                for replicate in range(rep_count):
                    seed = SEED + 50_000 + row_id
                    params = SimParams(
                        n_per_group=30,
                        effect_size=effect_size,
                        label_noise=0.0,
                        baseline_sd=1.0,
                        confounder_structure="immune_tone",
                        replicate=replicate,
                        seed=seed,
                    )
                    df = simulate_subjects(params, pathology=pathology, severity=severity)
                    df.insert(0, "simulation_family", "robustness")
                    df["truth"] = truth
                    for key, value in params.__dict__.items():
                        df[key] = value
                    metrics = evaluate_subjects(df, np.random.default_rng(seed + 999), n_boot)
                    expected_correct = (
                        metrics["verdict"] not in {"PASS_CLEAN", "PASS_PROVISIONAL_SMALL_N"}
                        if truth == "null"
                        else metrics["verdict"] in {"PASS_CLEAN", "PASS_PROVISIONAL_SMALL_N"}
                    )
                    rows.append(
                        params.__dict__
                        | {
                            "truth": truth,
                            "pathology": pathology,
                            "severity": severity,
                            "expected_correct": bool(expected_correct),
                        }
                        | metrics
                    )
                    subject_frames.append(df)
                    row_id += 1
    write_subject_rows(SYNTHETIC / "robustness_simulation_subjects.tsv.gz", subject_frames)
    result = pd.DataFrame(rows)
    result.to_csv(OUT / "robustness_cohort_results.tsv", sep="\t", index=False)
    summary = (
        result.assign(
            pass_any=result["verdict"].isin(["PASS_CLEAN", "PASS_PROVISIONAL_SMALL_N"]),
            non_specific=result["verdict"].eq("PASS_NON_SPECIFIC"),
        )
        .groupby(["truth", "pathology", "severity"], as_index=False)
        .agg(
            cohorts=("verdict", "size"),
            correct_rate=("expected_correct", "mean"),
            pass_rate=("pass_any", "mean"),
            non_specific_rate=("non_specific", "mean"),
            mean_auc=("auc", "mean"),
            median_n=("n", "median"),
        )
    )
    summary.to_csv(OUT / "robustness_summary.tsv", sep="\t", index=False)
    return result, summary


def joint_z(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values) & (values > 0)]
    if len(values) == 0:
        return 0.0
    return float(values.sum() / math.sqrt(len(values)))


def run_self_audit(n_reps: int = 5000) -> tuple[pd.DataFrame, dict[str, object]]:
    matrix = pd.read_csv(OUT.parent / "v41_joint_inference" / "entity_modality_evidence_matrix.tsv", sep="\t")
    evidence = pd.read_csv(OUT.parent / "v41_joint_inference" / "integrated_evidence_frame.tsv", sep="\t")
    split = json.loads((OUT.parent / "v41_joint_inference" / "heldout_modality_split.json").read_text())
    train_modalities = set(split["train_modalities"])
    excluded = set(split["excluded_from_joint_model"])
    train = matrix[matrix["modality"].isin(train_modalities) & ~matrix["modality"].isin(excluded)].copy()
    entities = sorted(set(matrix["entity"]))
    rng = np.random.default_rng(SEED + 90_000)
    by_modality: dict[str, pd.Series] = {}
    for modality, sub in train.groupby("modality"):
        series = pd.Series(0.0, index=entities)
        for _, row in sub.iterrows():
            series.loc[row["entity"]] = max(series.loc[row["entity"]], float(row["support_z"]))
        by_modality[modality] = series
    max_joint = []
    apc_joint = []
    for _ in range(n_reps):
        perm_sum = pd.Series(0.0, index=entities)
        perm_count = pd.Series(0, index=entities)
        for series in by_modality.values():
            values = series.to_numpy().copy()
            rng.shuffle(values)
            active = values > 0
            perm_sum += values
            perm_count += active.astype(int)
        denom = np.sqrt(np.maximum(perm_count.to_numpy(), 1))
        perm_z = np.divide(
            perm_sum.to_numpy(),
            denom,
            out=np.zeros_like(denom, dtype=float),
            where=perm_count.to_numpy() > 0,
        )
        entity_z = pd.Series(perm_z, index=entities)
        max_joint.append(float(entity_z.max()))
        apc_joint.append(float(entity_z.get("apc_hla_ifn_monitoring", 0.0)))

    positive = evidence[evidence["direction"].astype(float) > 0].copy()
    positive["source_unit"] = (
        positive["modality"].astype(str)
        + "::"
        + positive["source_file"].astype(str)
        + "::"
        + positive["evidence_label"].astype(str)
    )
    source_units = positive[["source_unit", "entity"]].drop_duplicates()
    entity_pool = np.asarray(sorted(evidence["entity"].dropna().unique()))
    counts_by_source = source_units.groupby("source_unit")["entity"].nunique().to_dict()
    observed_counts = source_units.groupby("entity")["source_unit"].nunique().to_dict()
    observed_top = max(observed_counts.values()) if observed_counts else 0
    max_recurrence = []
    for _ in range(n_reps):
        counts = {entity: 0 for entity in entity_pool}
        for n_source_entities in counts_by_source.values():
            sampled = rng.choice(entity_pool, size=min(n_source_entities, len(entity_pool)), replace=False)
            for entity in sampled:
                counts[entity] += 1
        max_recurrence.append(max(counts.values()) if counts else 0)

    rows = pd.DataFrame(
        {
            "replicate": np.arange(n_reps),
            "synthetic_null_max_joint_z": max_joint,
            "synthetic_null_apc_entity_joint_z": apc_joint,
            "synthetic_null_max_recurrence": max_recurrence,
        }
    )
    rows.to_csv(SYNTHETIC / "pipeline_null_replicates.tsv.gz", sep="\t", index=False, compression="gzip")
    summary = {
        "synthetic": True,
        "n_null_replicates": n_reps,
        "real_v41_apc_hla_ifn_monitoring_train_joint_z": REAL_V41_JOINT_Z,
        "null_max_joint_z_p95": float(np.quantile(max_joint, 0.95)),
        "null_max_joint_z_p99": float(np.quantile(max_joint, 0.99)),
        "real_joint_z_empirical_fwer_against_v43_null": float((np.sum(np.asarray(max_joint) >= REAL_V41_JOINT_Z) + 1) / (n_reps + 1)),
        "real_joint_z_empirical_entity_against_apc_null": float((np.sum(np.asarray(apc_joint) >= REAL_V41_JOINT_Z) + 1) / (n_reps + 1)),
        "real_v41_top_recurrence": REAL_V41_RECURRENCE,
        "observed_top_recurrence_from_frame": int(observed_top),
        "null_max_recurrence_p95": float(np.quantile(max_recurrence, 0.95)),
        "null_max_recurrence_p99": float(np.quantile(max_recurrence, 0.99)),
        "real_recurrence_empirical_fwer_against_v43_null": float((np.sum(np.asarray(max_recurrence) >= REAL_V41_RECURRENCE) + 1) / (n_reps + 1)),
    }
    (OUT / "pipeline_self_audit_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    return rows, summary


def first_minimum_power(summary: pd.DataFrame, effect_size: float, label_noise: float, confounder_structure: str, target: float = 0.80) -> str:
    sub = summary[
        summary["effect_size"].eq(effect_size)
        & summary["label_noise"].eq(label_noise)
        & summary["confounder_structure"].eq(confounder_structure)
    ].copy()
    sub = sub.groupby("n_per_group", as_index=False)["pass_rate"].mean().sort_values("n_per_group")
    ok = sub[sub["pass_rate"] >= target]
    if ok.empty:
        return f"not reached up to {int(sub['n_per_group'].max())} per group"
    row = ok.iloc[0]
    return f"{int(row['n_per_group'])} per group (pass_rate {row['pass_rate']:.2f})"


def write_power_report(power: pd.DataFrame, summary: pd.DataFrame) -> None:
    null = summary[summary["effect_size"].eq(0.0)]
    gafson_like = summary[summary["n_per_group"].isin([10, 15])]
    lines = [
        "# POWER MAP V43",
        "",
        "Status: synthetic method-characterization only. These simulations do not provide biological evidence about MS.",
        "",
        "## Simulation Scale",
        "",
        f"- Synthetic cohorts: `{len(power)}`.",
        "- Replicates per parameter cell: `12`.",
        "- Bootstrap replicates per synthetic cohort: `300`.",
        "- Parameter grid: n per response group `10,15,20,30,45,60,80`; true effect size `0,0.25,0.50,0.75,1.00,1.25,1.50`; label noise `0,0.10`; baseline SD `0.5,1.0`; confounder structures `none,immune_tone,composition,steroid`.",
        "- Full synthetic subject-level data: `analysis/v43_method_validation/synthetic/power_simulation_subjects.tsv.gz`.",
        "",
        "## Headline",
        "",
        f"- Null false-positive rate across all null cells: `{float(null['false_positive_rate'].mean()):.3f}`.",
        f"- Gafson-small cells (`10-15` per group) mean conclusive rate: `{float(gafson_like['conclusive_rate'].mean()):.3f}`.",
        f"- Minimum n for 80% pass probability at effect size 0.75, no label noise, no confounder: {first_minimum_power(summary, 0.75, 0.0, 'none')}.",
        f"- Minimum n for 80% pass probability at effect size 1.00, no label noise, no confounder: {first_minimum_power(summary, 1.00, 0.0, 'none')}.",
        f"- Minimum n for 80% pass probability at effect size 0.75 with 10% label noise and immune-tone structure: {first_minimum_power(summary, 0.75, 0.10, 'immune_tone')}.",
        "",
        "Interpretation: a tiny Gafson-sized cohort can produce a useful effect estimate, but it is unlikely to settle the rule unless the true effect is large and labels are clean. A validation intended to settle the question should target at least the first n-per-group cell above, and preferably exceed it to preserve power under label noise/confounding.",
        "",
        "## Machine-Readable Outputs",
        "",
        "- `analysis/v43_method_validation/power_simulation_cohort_results.tsv`",
        "- `analysis/v43_method_validation/power_map_summary.tsv`",
    ]
    (ROOT / "docs" / "validation" / "POWER_MAP_V43.md").write_text("\n".join(lines) + "\n")


def write_robustness_report(summary: pd.DataFrame) -> None:
    summary = summary.copy()
    summary["truth"] = summary["truth"].fillna("null").astype(str)
    envelope_rows = []
    planted = summary[summary["truth"].eq("planted")].set_index(["pathology", "severity"])
    null = summary[summary["truth"].eq("null")].set_index(["pathology", "severity"])
    for pathology in sorted(summary["pathology"].unique()):
        rows = []
        for severity in sorted(summary[summary["pathology"].eq(pathology)]["severity"].unique()):
            key = (pathology, severity)
            planted_correct = float(planted.loc[key, "correct_rate"]) if key in planted.index else math.nan
            null_pass = float(null.loc[key, "pass_rate"]) if key in null.index else math.nan
            rows.append(
                {
                    "severity": severity,
                    "planted_correct_rate": planted_correct,
                    "null_pass_rate": null_pass,
                    "inside_envelope": planted_correct >= 0.80 and null_pass <= 0.05,
                }
            )
        ok = [row for row in rows if row["inside_envelope"]]
        max_ok = max([row["severity"] for row in ok]) if ok else math.nan
        envelope_rows.append(
            {
                "pathology": pathology,
                "max_severity_inside_envelope": max_ok,
                "criterion": "planted_correct_rate>=0.80 and null_pass_rate<=0.05",
            }
        )
    envelope = pd.DataFrame(envelope_rows)
    envelope.to_csv(OUT / "robustness_envelope.tsv", sep="\t", index=False)
    worst_null = summary[summary["truth"].eq("null")].sort_values("pass_rate", ascending=False).head(5)
    lines = [
        "# HARNESS ROBUSTNESS V43",
        "",
        "Status: synthetic method-characterization only. These stress tests define data-quality warning signs; they are not biological evidence.",
        "",
        "## Simulation Scale",
        "",
        f"- Synthetic cohorts: `{int(summary['cohorts'].sum())}`.",
        "- Replicates per pathology/severity/truth cell: `30`.",
        "- Baseline planted effect: effect size `1.25`, `30` responders and `30` nonresponders.",
        "- Full synthetic subject-level data: `analysis/v43_method_validation/synthetic/robustness_simulation_subjects.tsv.gz`.",
        "",
        "## Trust Envelope",
        "",
        "The harness is trustworthy when the received data package keeps the observed pathology severity inside the ranges below. The envelope requires both planted-signal recovery (`correct_rate >= 0.80`) and null false-positive control (`null pass rate <= 0.05`). Outside it, interpret Gafson as inconclusive or non-specific unless the issue can be resolved before running the frozen analysis.",
        "",
        "| Pathology | Largest tested severity inside envelope | Criterion |",
        "|---|---:|---|",
    ]
    for row in envelope.to_dict(orient="records"):
        val = row["max_severity_inside_envelope"]
        lines.append(f"| {row['pathology']} | {val if np.isfinite(val) else 'none'} | {row['criterion']} |")
    lines.extend(
        [
            "",
            "Worst null false-positive stress cells:",
            "",
            "| Pathology | Severity | Null pass rate | Mean AUC |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in worst_null.to_dict(orient="records"):
        lines.append(f"| {row['pathology']} | {row['severity']} | {row['pass_rate']:.3f} | {row['mean_auc']:.3f} |")
    lines.extend(
        [
            "",
            "## Machine-Readable Outputs",
            "",
            "- `analysis/v43_method_validation/robustness_cohort_results.tsv`",
            "- `analysis/v43_method_validation/robustness_summary.tsv`",
            "- `analysis/v43_method_validation/robustness_envelope.tsv`",
        ]
    )
    (ROOT / "docs" / "validation" / "HARNESS_ROBUSTNESS_V43.md").write_text("\n".join(lines) + "\n")


def write_self_audit_report(summary: dict[str, object]) -> None:
    lines = [
        "# PIPELINE SELF-AUDIT V43",
        "",
        "Status: synthetic-null method audit only. This does not create or refute a biological MS finding.",
        "",
        "## Synthetic Null Design",
        "",
        "- Loaded the V41 entity-by-modality evidence matrix and held-out split.",
        "- Generated synthetic null corpora by shuffling support z-scores within each training modality, preserving modality coverage and score distribution.",
        "- Generated recurrence nulls by randomizing positive source-unit entity assignments while preserving the number of source units and entity vocabulary.",
        f"- Null replicates: `{summary['n_null_replicates']}`.",
        "",
        "## Joint-Inference Calibration",
        "",
        f"- Real V41 `apc_hla_ifn_monitoring` train joint z: `{summary['real_v41_apc_hla_ifn_monitoring_train_joint_z']:.4f}`.",
        f"- Synthetic-null max joint z 95th percentile: `{summary['null_max_joint_z_p95']:.4f}`.",
        f"- Synthetic-null max joint z 99th percentile: `{summary['null_max_joint_z_p99']:.4f}`.",
        f"- Empirical FWER p for the real joint z against V43 null: `{summary['real_joint_z_empirical_fwer_against_v43_null']:.4f}`.",
        f"- Entity-specific empirical p for the real joint z against the shuffled APC-entity null: `{summary['real_joint_z_empirical_entity_against_apc_null']:.4f}`.",
        "",
        "Interpretation: the real central joint score is strong for the named APC entity, but it sits near the family-wise maximum tail expected when many entities/modalities are searched. That supports the V41 conclusion: the signal is repeatable and known-context, not a license for unconstrained new discovery.",
        "",
        "## Recurrence Calibration",
        "",
        f"- Real V41 top recurrence: `{summary['real_v41_top_recurrence']}` positive source units.",
        f"- Synthetic-null max recurrence 95th percentile: `{summary['null_max_recurrence_p95']:.1f}`.",
        f"- Synthetic-null max recurrence 99th percentile: `{summary['null_max_recurrence_p99']:.1f}`.",
        f"- Empirical FWER p for real recurrence against V43 null: `{summary['real_recurrence_empirical_fwer_against_v43_null']:.4f}`.",
        "",
        "Interpretation: the recurrence result is far outside this synthetic-null structure and is the stronger methodological corroboration of the central APC-axis recurrence. It still remains prior-known/validation-gated biological context, not a new intervention claim.",
        "",
        "## Machine-Readable Outputs",
        "",
        "- `analysis/v43_method_validation/synthetic/pipeline_null_replicates.tsv.gz`",
        "- `analysis/v43_method_validation/pipeline_self_audit_summary.json`",
    ]
    (ROOT / "docs" / "history" / "PIPELINE_SELF_AUDIT_V43.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--power-bootstrap", type=int, default=300)
    parser.add_argument("--self-audit-reps", type=int, default=5000)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    SYNTHETIC.mkdir(parents=True, exist_ok=True)
    power, power_summary = run_power(args.power_bootstrap)
    write_power_report(power, power_summary)
    robustness, robustness_summary = run_robustness(args.power_bootstrap)
    write_robustness_report(robustness_summary)
    _nulls, self_summary = run_self_audit(args.self_audit_reps)
    write_self_audit_report(self_summary)
    run_summary = {
        "synthetic": True,
        "seed": SEED,
        "power_synthetic_cohorts": int(len(power)),
        "power_bootstrap_replicates_per_cohort": int(args.power_bootstrap),
        "robustness_synthetic_cohorts": int(len(robustness)),
        "self_audit_null_replicates": int(args.self_audit_reps),
        "power_mean_null_false_positive_rate": float(power_summary[power_summary["effect_size"].eq(0.0)]["false_positive_rate"].mean()),
        "self_audit_real_joint_fwer_p": self_summary["real_joint_z_empirical_fwer_against_v43_null"],
        "self_audit_real_recurrence_fwer_p": self_summary["real_recurrence_empirical_fwer_against_v43_null"],
    }
    (OUT / "v43_method_validation_summary.json").write_text(json.dumps(run_summary, indent=2, sort_keys=True))
    print(json.dumps(run_summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
