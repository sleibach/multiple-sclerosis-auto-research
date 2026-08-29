#!/usr/bin/env python3
"""Probe cross-environment stability and selective prediction for V22."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v57_environment_stability"
SEED = 57001
N_PERMUTATIONS = 200_000
PRIMARY_ALPHA = 0.10
SENSITIVITY_ALPHA = 0.20


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--permutations", type=int, default=N_PERMUTATIONS)
    parser.add_argument("--seed", type=int, default=SEED)
    return parser.parse_args()


def auc_score(y: np.ndarray, score: np.ndarray) -> float:
    positive = score[y == 1]
    negative = score[y == 0]
    if not len(positive) or not len(negative):
        return math.nan
    differences = positive[:, None] - negative[None, :]
    return float((np.sum(differences > 0) + 0.5 * np.sum(differences == 0)) / differences.size)


def hedges_g(y: np.ndarray, score: np.ndarray) -> tuple[float, float]:
    positive = score[y == 1]
    negative = score[y == 0]
    n1, n0 = len(positive), len(negative)
    if n1 < 2 or n0 < 2:
        return math.nan, math.nan
    pooled_variance = (
        (n1 - 1) * np.var(positive, ddof=1) + (n0 - 1) * np.var(negative, ddof=1)
    ) / (n1 + n0 - 2)
    if pooled_variance <= 0:
        return math.nan, math.nan
    correction = 1 - 3 / (4 * (n1 + n0) - 9)
    g = correction * (np.mean(positive) - np.mean(negative)) / math.sqrt(pooled_variance)
    variance = (n1 + n0) / (n1 * n0) + g * g / (2 * (n1 + n0 - 2))
    return float(g), float(variance)


def exact_auc_p(y: np.ndarray, score: np.ndarray) -> tuple[float, int]:
    observed = auc_score(y, score)
    n_positive = int(y.sum())
    exceed = 0
    total = 0
    for positive_indices in itertools.combinations(range(len(y)), n_positive):
        permuted = np.zeros(len(y), dtype=np.int8)
        permuted[list(positive_indices)] = 1
        if auc_score(permuted, score) >= observed - 1e-12:
            exceed += 1
        total += 1
    return exceed / total, total


def load_data() -> pd.DataFrame:
    v22 = pd.read_csv(
        ROOT / "analysis/v22_locked_apc_hla_validation/paired_locked_scores_v22.tsv",
        sep="\t",
    )
    cross = pd.read_csv(
        ROOT / "analysis/v22_locked_apc_hla_validation/paired_locked_scores_v22_cross_disease.tsv",
        sep="\t",
    )
    cross = cross[cross["cohort"].eq("GSE85034_ADA")].copy()
    exact = pd.read_csv(
        ROOT
        / "analysis/v23_apc_hla_monitoring/gse253006_exact_locked/gse253006_exact_paired_scores.tsv",
        sep="\t",
    )
    data = pd.concat([v22, cross, exact], ignore_index=True)
    data["response_binary"] = data["response"].eq("Responder").astype(np.int8)
    data["score_percentile"] = data.groupby("cohort")["locked_signed_score"].rank(
        method="average", pct=True
    )
    expected = {"GSE235357": 10, "GSE250453": 10, "GSE85034_ADA": 14, "GSE253006_TOF_exact": 9}
    observed = data.groupby("cohort").size().to_dict()
    if observed != expected:
        raise ValueError(f"Cohort contract mismatch: expected {expected}, observed {observed}")
    if data.duplicated(["cohort", "patient"]).any():
        raise ValueError("Duplicate cohort-patient rows")
    return data


def cohort_metrics(data: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for cohort, frame in data.groupby("cohort", sort=True):
        y = frame["response_binary"].to_numpy(dtype=np.int8)
        score = frame["locked_signed_score"].to_numpy(dtype=float)
        auc = auc_score(y, score)
        g, variance = hedges_g(y, score)
        p_value, assignments = exact_auc_p(y, score)
        rows.append(
            {
                "cohort": cohort,
                "n": len(frame),
                "responders": int(y.sum()),
                "nonresponders": int((1 - y).sum()),
                "auc": auc,
                "hedges_g": g,
                "hedges_g_variance": variance,
                "exact_one_sided_auc_p": p_value,
                "exact_label_assignments": assignments,
                "direction_consistent_auc_gt_half": bool(auc > 0.5),
            }
        )
    return pd.DataFrame(rows)


def environment_summary(
    data: pd.DataFrame, metrics: pd.DataFrame, rng: np.random.Generator, n_permutations: int
) -> tuple[dict[str, Any], dict[str, float]]:
    weights = metrics["n"].to_numpy(dtype=float)
    observed_aucs = metrics["auc"].to_numpy(dtype=float)
    observed_weighted_auc = float(np.average(observed_aucs, weights=weights))
    observed_worst_auc = float(np.min(observed_aucs))
    observed_sign_count = int(np.sum(observed_aucs > 0.5))

    groups = []
    for _, frame in data.groupby("cohort", sort=True):
        groups.append(
            (
                frame["response_binary"].to_numpy(dtype=np.int8),
                frame["locked_signed_score"].to_numpy(dtype=float),
            )
        )
    null_weighted = np.empty(n_permutations, dtype=float)
    null_worst = np.empty(n_permutations, dtype=float)
    null_sign_count = np.empty(n_permutations, dtype=np.int8)
    for index in range(n_permutations):
        aucs = np.array([auc_score(rng.permutation(y), score) for y, score in groups])
        null_weighted[index] = np.average(aucs, weights=weights)
        null_worst[index] = np.min(aucs)
        null_sign_count[index] = int(np.sum(aucs > 0.5))

    effects = metrics["hedges_g"].to_numpy(dtype=float)
    variances = metrics["hedges_g_variance"].to_numpy(dtype=float)
    inverse_variance = 1 / variances
    fixed_effect = float(np.sum(inverse_variance * effects) / np.sum(inverse_variance))
    q_statistic = float(np.sum(inverse_variance * (effects - fixed_effect) ** 2))
    q_p = float(stats.chi2.sf(q_statistic, len(effects) - 1))
    weighted_p = float((1 + np.sum(null_weighted >= observed_weighted_auc)) / (n_permutations + 1))
    worst_p = float((1 + np.sum(null_worst >= observed_worst_auc)) / (n_permutations + 1))
    sign_p = float((1 + np.sum(null_sign_count >= observed_sign_count)) / (n_permutations + 1))
    stable = bool(
        np.all(observed_aucs >= 0.55)
        and np.all(effects > 0)
        and weighted_p <= 0.05
        and q_p >= 0.10
    )
    summary = {
        "n_subjects": int(len(data)),
        "n_environments": int(len(metrics)),
        "weighted_mean_auc": observed_weighted_auc,
        "weighted_mean_auc_stratified_permutation_p": weighted_p,
        "worst_environment_auc": observed_worst_auc,
        "worst_auc_stratified_permutation_p": worst_p,
        "direction_consistent_environment_count": observed_sign_count,
        "direction_consistency_stratified_permutation_p": sign_p,
        "fixed_effect_hedges_g": fixed_effect,
        "cochran_q": q_statistic,
        "cochran_q_df": len(effects) - 1,
        "cochran_q_p": q_p,
        "stringent_environment_stability_gate": stable,
        "verdict": "SUPPORTED_FOR_DEDICATED_TRANSPORT_STUDY" if stable else "NOT_ENVIRONMENT_STABLE",
    }
    null_quantiles = {
        "weighted_auc_null_q95": float(np.quantile(null_weighted, 0.95)),
        "worst_auc_null_q95": float(np.quantile(null_worst, 0.95)),
        "sign_count_null_q95": float(np.quantile(null_sign_count, 0.95)),
    }
    return summary, null_quantiles


def conformal_p_values(train: pd.DataFrame, score: float) -> tuple[float, float]:
    responder = train.loc[train.response_binary.eq(1), "score_percentile"].to_numpy(float)
    nonresponder = train.loc[train.response_binary.eq(0), "score_percentile"].to_numpy(float)
    p_responder = (1 + np.sum(responder <= score)) / (len(responder) + 1)
    p_nonresponder = (1 + np.sum(nonresponder >= score)) / (len(nonresponder) + 1)
    return float(p_nonresponder), float(p_responder)


def prediction_rows(data: pd.DataFrame, alpha: float) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for held_cohort in sorted(data.cohort.unique()):
        train = data[data.cohort.ne(held_cohort)]
        test = data[data.cohort.eq(held_cohort)]
        for _, row in test.iterrows():
            p0, p1 = conformal_p_values(train, float(row.score_percentile))
            labels = [label for label, p_value in [(0, p0), (1, p1)] if p_value > alpha]
            rows.append(
                {
                    "alpha": alpha,
                    "held_out_cohort": held_cohort,
                    "patient": row.patient,
                    "true_label": int(row.response_binary),
                    "score_percentile": float(row.score_percentile),
                    "p_nonresponder": p0,
                    "p_responder": p1,
                    "prediction_set": ";".join(map(str, labels)) if labels else "EMPTY",
                    "set_size": len(labels),
                    "covered": int(row.response_binary) in labels,
                    "singleton": len(labels) == 1,
                    "singleton_correct": len(labels) == 1 and labels[0] == int(row.response_binary),
                }
            )
    return pd.DataFrame(rows)


def wilson(successes: int, total: int) -> tuple[float, float]:
    if total == 0:
        return math.nan, math.nan
    z = float(stats.norm.ppf(0.975))
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return center - half, center + half


def summarize_predictions(predictions: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for (alpha, cohort), frame in predictions.groupby(["alpha", "held_out_cohort"], sort=True):
        for label, sub in [("cohort", frame), ("pooled", predictions[predictions.alpha.eq(alpha)])]:
            if label == "pooled" and cohort != sorted(predictions.held_out_cohort.unique())[0]:
                continue
            coverage = int(sub.covered.sum())
            singleton = int(sub.singleton.sum())
            singleton_correct = int(sub.singleton_correct.sum())
            low, high = wilson(coverage, len(sub))
            rows.append(
                {
                    "alpha": alpha,
                    "scope": cohort if label == "cohort" else "POOLED",
                    "n": len(sub),
                    "covered": coverage,
                    "coverage": coverage / len(sub),
                    "coverage_ci_low": low,
                    "coverage_ci_high": high,
                    "singletons": singleton,
                    "singleton_rate": singleton / len(sub),
                    "singleton_correct": singleton_correct,
                    "singleton_accuracy": singleton_correct / singleton if singleton else math.nan,
                    "empty_rate": float(np.mean(sub.set_size.eq(0))),
                    "both_label_abstention_rate": float(np.mean(sub.set_size.eq(2))),
                }
            )
    return pd.DataFrame(rows)


def singleton_null_p(
    predictions: pd.DataFrame, rng: np.random.Generator, n_permutations: int
) -> tuple[float, int, int, dict[str, float]]:
    primary = predictions[predictions.alpha.eq(PRIMARY_ALPHA)].copy()
    observed = int(primary.singleton_correct.sum())
    singleton_total = int(primary.singleton.sum())
    null = np.empty(n_permutations, dtype=np.int16)
    groups = [frame.copy() for _, frame in primary.groupby("held_out_cohort", sort=True)]
    for index in range(n_permutations):
        correct = 0
        for frame in groups:
            labels = rng.permutation(frame.true_label.to_numpy(dtype=np.int8))
            predicted = frame.prediction_set.to_numpy(str)
            singleton = frame.singleton.to_numpy(bool)
            for prediction, label, is_singleton in zip(predicted, labels, singleton, strict=True):
                if is_singleton and prediction == str(int(label)):
                    correct += 1
        null[index] = correct
    p_value = float((1 + np.sum(null >= observed)) / (n_permutations + 1))
    quantiles = {f"q{q}": float(np.quantile(null, q / 100)) for q in [50, 90, 95, 99]}
    return p_value, observed, singleton_total, quantiles


def write_report(
    outdir: Path,
    environment: dict[str, Any],
    conformal_gate: dict[str, Any],
    metrics: pd.DataFrame,
) -> None:
    lines = [
        "# V57 Environment-Stability And Selective-Prediction Probe",
        "",
        "This is a method-behavior analysis around the immutable V22 score. It is",
        "not a new biomarker, target, treatment result, or causal finding.",
        "",
        "## Environment Stability",
        "",
        "| Cohort | n | AUC | Hedges g | Exact p |",
        "|---|---:|---:|---:|---:|",
    ]
    for _, row in metrics.iterrows():
        lines.append(
            f"| `{row.cohort}` | {int(row.n)} | {row.auc:.3f} | {row.hedges_g:.3f} | "
            f"{row.exact_one_sided_auc_p:.4f} |"
        )
    lines.extend(
        [
            "",
            f"- Weighted mean AUC: `{environment['weighted_mean_auc']:.3f}` "
            f"(stratified permutation p=`{environment['weighted_mean_auc_stratified_permutation_p']:.6f}`).",
            f"- Worst-environment AUC: `{environment['worst_environment_auc']:.3f}`.",
            f"- Cochran Q p: `{environment['cochran_q_p']:.4f}`.",
            f"- Frozen stability verdict: **{environment['verdict']}**.",
            "",
            "## Selective Prediction",
            "",
            f"- Primary alpha: `{PRIMARY_ALPHA}`.",
            f"- Pooled coverage: `{conformal_gate['pooled_coverage']:.3f}`.",
            f"- Worst-cohort coverage: `{conformal_gate['worst_cohort_coverage']:.3f}`.",
            f"- Singleton rate: `{conformal_gate['singleton_rate']:.3f}`.",
            f"- Singleton accuracy: `{conformal_gate['singleton_accuracy']}`.",
            f"- Singleton correctness stratified-null p: `{conformal_gate['singleton_null_p']:.6f}`.",
            f"- Frozen selective-prediction verdict: **{conformal_gate['verdict']}**.",
            "",
            "Whole-cohort holdout deliberately violates any casual IID assumption. Failure is",
            "evidence that an uncertainty wrapper calibrated on these source cohorts should not",
            "be trusted to guarantee coverage in a new MS cohort. Passing would still require",
            "prospective validation.",
        ]
    )
    (outdir / "REPORT.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    data = load_data()
    data.to_csv(outdir / "assembled_cohorts.tsv", sep="\t", index=False)
    metrics = cohort_metrics(data)
    metrics.to_csv(outdir / "cohort_metrics.tsv", sep="\t", index=False)
    environment, null_quantiles = environment_summary(data, metrics, rng, args.permutations)

    predictions = pd.concat(
        [prediction_rows(data, alpha) for alpha in [PRIMARY_ALPHA, SENSITIVITY_ALPHA]],
        ignore_index=True,
    )
    predictions.to_csv(outdir / "leave_one_cohort_prediction_sets.tsv", sep="\t", index=False)
    prediction_summary = summarize_predictions(predictions)
    prediction_summary.to_csv(outdir / "prediction_set_summary.tsv", sep="\t", index=False)
    singleton_p, singleton_correct, singleton_total, singleton_quantiles = singleton_null_p(
        predictions, rng, args.permutations
    )
    primary_summary = prediction_summary[prediction_summary.alpha.eq(PRIMARY_ALPHA)]
    pooled = primary_summary[primary_summary.scope.eq("POOLED")].iloc[0]
    cohorts = primary_summary[primary_summary.scope.ne("POOLED")]
    singleton_accuracy = (
        singleton_correct / singleton_total if singleton_total else math.nan
    )
    selective_pass = bool(
        pooled.coverage >= 0.90
        and cohorts.coverage.min() >= 0.80
        and pooled.singleton_rate >= 0.20
        and singleton_total > 0
        and singleton_accuracy >= 0.70
        and singleton_p <= 0.05
    )
    conformal_gate = {
        "pooled_coverage": float(pooled.coverage),
        "pooled_coverage_ci_low": float(pooled.coverage_ci_low),
        "worst_cohort_coverage": float(cohorts.coverage.min()),
        "singleton_rate": float(pooled.singleton_rate),
        "singleton_correct": singleton_correct,
        "singleton_total": singleton_total,
        "singleton_accuracy": singleton_accuracy,
        "singleton_null_p": singleton_p,
        "verdict": "WORTH_DEDICATED_VALIDATION" if selective_pass else "NOT_TRANSPORT_READY",
    }
    summary = {
        "purpose": "V57 held-data method probe; no biological discovery claim",
        "plan": "docs/plans/V57_ENVIRONMENT_STABILITY_PLAN.md",
        "seed": args.seed,
        "n_permutations": args.permutations,
        "environment_stability": environment,
        "environment_null_quantiles": null_quantiles,
        "selective_prediction": conformal_gate,
        "singleton_null_quantiles": singleton_quantiles,
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_report(outdir, environment, conformal_gate, metrics)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
