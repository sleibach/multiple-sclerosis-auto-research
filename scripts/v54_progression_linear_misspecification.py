#!/usr/bin/env python3
"""Audit one-linear-coefficient progression models under fixed nonlinear risks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import binom, chi2, norm


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_linear_misspecification"
SEEDS = (54121, 54133, 54139)
CALIBRATION_SEEDS = (64121, 64133, 64139)
N_VALUES = (180, 320)
PATTERNS = (
    "null",
    "linear",
    "high_threshold",
    "monotone_saturation",
    "u_shaped_crossing",
    "inverted_u",
)
METHODS = (
    "primary_linear",
    "threshold_diagnostic",
    "saturation_diagnostic",
    "linear_quadratic_diagnostic",
    "diagnostic_any",
)
EXPECTED_DIAGNOSTIC = {
    "high_threshold": "threshold_diagnostic",
    "monotone_saturation": "saturation_diagnostic",
    "u_shaped_crossing": "linear_quadratic_diagnostic",
    "inverted_u": "linear_quadratic_diagnostic",
}
REPLICATES = 3000
CALIBRATION_REPLICATES = 3000
EVENT_PROBABILITY = 0.30
RELIABILITY = 0.70
SCORE_MISSING = 0.10
ALPHA = 0.05
DIAGNOSTIC_ALPHA = ALPHA / 3
CRITICAL_VALUES: dict[tuple[int, str], float] = {}


def wilson(successes: int, total: int) -> tuple[float, float]:
    z = norm.ppf(0.975)
    probability = successes / total
    denominator = 1 + z * z / total
    center = (probability + z * z / (2 * total)) / denominator
    half = z * np.sqrt(
        probability * (1 - probability) / total + z * z / (4 * total * total)
    ) / denominator
    return float(center - half), float(center + half)


def calibrate_scale(multiplier: np.ndarray, target: float) -> np.ndarray:
    low = np.zeros(multiplier.shape[0])
    high = np.full(multiplier.shape[0], 20.0)
    for _ in range(50):
        middle = (low + high) / 2
        probability = np.mean(1 - np.exp(-middle[:, None] * multiplier), axis=1)
        below = probability < target
        low[below] = middle[below]
        high[~below] = middle[~below]
    return (low + high) / 2


def log_hazard(pattern: str, latent: np.ndarray) -> np.ndarray:
    if pattern == "null":
        value = np.zeros_like(latent)
    elif pattern == "linear":
        value = np.log(1.7) * latent
    elif pattern == "high_threshold":
        value = np.log(2.2) * (latent > 0.674).astype(float)
    elif pattern == "monotone_saturation":
        value = np.log(2.0) * np.tanh(1.5 * latent)
    elif pattern == "u_shaped_crossing":
        value = np.log(1.8) * (latent**2 - 1) / np.sqrt(2)
    elif pattern == "inverted_u":
        value = -np.log(1.8) * (latent**2 - 1) / np.sqrt(2)
    else:
        raise ValueError(pattern)
    return np.clip(value, -5, 5)


def cox_score_matrix(features: np.ndarray, time: np.ndarray, event: np.ndarray) -> tuple[float, float]:
    order = np.argsort(time, kind="mergesort")
    x = features[order]
    observed_event = event[order]
    event_index = np.flatnonzero(observed_event)
    if not len(event_index):
        return np.nan, np.nan
    risk_n = np.arange(len(order), 0, -1, dtype=float)
    risk_sum = np.cumsum(x[::-1], axis=0)[::-1]
    outer = x[:, :, None] * x[:, None, :]
    risk_outer = np.cumsum(outer[::-1], axis=0)[::-1]
    means = risk_sum[event_index] / risk_n[event_index, None]
    covariance = (
        risk_outer[event_index] / risk_n[event_index, None, None]
        - means[:, :, None] * means[:, None, :]
    )
    score = np.sum(x[event_index] - means, axis=0)
    information = np.sum(covariance, axis=0)
    if not np.all(np.isfinite(information)):
        return np.nan, np.nan
    try:
        statistic = float(score @ np.linalg.pinv(information, rcond=1e-10) @ score)
    except np.linalg.LinAlgError:
        return np.nan, np.nan
    rank = int(np.linalg.matrix_rank(information, tol=1e-9))
    if rank < features.shape[1] or statistic < 0:
        return np.nan, np.nan
    return statistic, float(chi2.sf(statistic, rank))


def standardize(value: np.ndarray) -> np.ndarray | None:
    sd = float(np.std(value, ddof=1))
    if not np.isfinite(sd) or sd <= 0:
        return None
    return (value - value.mean()) / sd


def generate_cohorts(
    rng: np.random.Generator, n: int, pattern: str, replicates: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    latent = rng.normal(size=(replicates, n))
    frailty = rng.normal(size=(replicates, n))
    multiplier = np.exp(log_hazard(pattern, latent) + 0.7 * frailty)
    baseline = calibrate_scale(multiplier, EVENT_PROBABILITY)
    event_time = -np.log(np.clip(rng.random((replicates, n)), 1e-12, 1.0)) / (
        baseline[:, None] * multiplier
    )
    time = np.minimum(event_time, 1.0)
    event = event_time <= 1.0
    observed = (
        np.sqrt(RELIABILITY) * latent
        + np.sqrt(1 - RELIABILITY) * rng.normal(size=latent.shape)
    )
    included = rng.random(size=latent.shape) >= SCORE_MISSING
    return time, event, observed, included


def evaluate_pvalues(
    time: np.ndarray,
    event: np.ndarray,
    observed: np.ndarray,
    included: np.ndarray,
) -> tuple[dict[str, np.ndarray], np.ndarray, np.ndarray]:
    replicates = len(time)
    p_values = {
        method: np.full(replicates, np.nan)
        for method in METHODS
        if method != "diagnostic_any"
    }
    linear_direction = np.full(replicates, np.nan)
    event_counts = np.zeros(replicates, dtype=int)
    for replicate in range(replicates):
        keep = included[replicate]
        selected_event = event[replicate, keep]
        event_counts[replicate] = int(selected_event.sum())
        if keep.sum() < 20 or selected_event.sum() < 10 or (~selected_event).sum() < 10:
            continue
        z = standardize(observed[replicate, keep])
        if z is None:
            continue
        threshold = standardize((z > 0.674).astype(float))
        saturated = standardize(np.tanh(1.5 * z))
        quadratic = standardize(z**2)
        if threshold is None or saturated is None or quadratic is None:
            continue
        selected_time = time[replicate, keep]
        _, p_values["primary_linear"][replicate] = cox_score_matrix(
            z[:, None], selected_time, selected_event
        )
        _, p_values["threshold_diagnostic"][replicate] = cox_score_matrix(
            threshold[:, None], selected_time, selected_event
        )
        _, p_values["saturation_diagnostic"][replicate] = cox_score_matrix(
            saturated[:, None], selected_time, selected_event
        )
        _, p_values["linear_quadratic_diagnostic"][replicate] = cox_score_matrix(
            np.column_stack([z, quadratic]), selected_time, selected_event
        )
        order = np.argsort(selected_time, kind="mergesort")
        ordered_z = z[order]
        event_index = np.flatnonzero(selected_event[order])
        risk_mean = np.cumsum(ordered_z[::-1])[::-1][event_index] / np.arange(
            len(order), 0, -1, dtype=float
        )[event_index]
        linear_direction[replicate] = float(
            np.sum(ordered_z[event_index] - risk_mean)
        )
    return p_values, linear_direction, event_counts


def empirical_thresholds() -> tuple[dict[tuple[int, str], float], pd.DataFrame]:
    collected: dict[tuple[int, str], list[np.ndarray]] = {}
    for seed in CALIBRATION_SEEDS:
        rng = np.random.default_rng(seed)
        for n in N_VALUES:
            arrays = generate_cohorts(rng, n, "null", CALIBRATION_REPLICATES)
            p_values, _, _ = evaluate_pvalues(*arrays)
            for method, values in p_values.items():
                collected.setdefault((n, method), []).append(values[np.isfinite(values)])
            diagnostic_min = np.nanmin(
                np.vstack(
                    [
                        p_values["threshold_diagnostic"],
                        p_values["saturation_diagnostic"],
                        p_values["linear_quadratic_diagnostic"],
                    ]
                ),
                axis=0,
            )
            collected.setdefault((n, "diagnostic_any"), []).append(
                diagnostic_min[np.isfinite(diagnostic_min)]
            )
    thresholds: dict[tuple[int, str], float] = {}
    rows: list[dict[str, Any]] = []
    for (n, method), arrays in sorted(collected.items()):
        values = np.concatenate(arrays)
        nominal_alpha = (
            DIAGNOSTIC_ALPHA
            if method in {
                "threshold_diagnostic",
                "saturation_diagnostic",
                "linear_quadratic_diagnostic",
            }
            else ALPHA
        )
        threshold = float(np.quantile(values, nominal_alpha, method="lower"))
        thresholds[(n, method)] = threshold
        rows.append(
            {
                "n_requested": n,
                "method": method,
                "nominal_alpha": nominal_alpha,
                "n_independent_null_pvalues": len(values),
                "empirical_p_threshold": threshold,
                "calibration_seeds": ";".join(str(seed) for seed in CALIBRATION_SEEDS),
            }
        )
    return thresholds, pd.DataFrame(rows)


def simulate_cell(rng: np.random.Generator, n: int, pattern: str) -> list[dict[str, Any]]:
    arrays = generate_cohorts(rng, n, pattern, REPLICATES)
    p_values, linear_direction, event_counts = evaluate_pvalues(*arrays)
    diagnostic_min = np.nanmin(
        np.vstack(
            [
                p_values["threshold_diagnostic"],
                p_values["saturation_diagnostic"],
                p_values["linear_quadratic_diagnostic"],
            ]
        ),
        axis=0,
    )
    p_values["diagnostic_any"] = diagnostic_min
    rows: list[dict[str, Any]] = []
    for method in METHODS:
        values = p_values[method]
        finite = np.isfinite(values)
        detected = finite & (values <= CRITICAL_VALUES[(n, method)])
        count = int(detected.sum())
        low, high = wilson(count, REPLICATES)
        positive = int((detected & (linear_direction >= 0)).sum()) if method == "primary_linear" else 0
        negative = int((detected & (linear_direction < 0)).sum()) if method == "primary_linear" else 0
        rows.append(
            {
                "n_requested": n,
                "effect_pattern": pattern,
                "method": method,
                "method_alpha": ALPHA if method in {"primary_linear", "diagnostic_any"} else DIAGNOSTIC_ALPHA,
                "empirical_p_threshold": CRITICAL_VALUES[(n, method)],
                "n_simulated_cohorts": REPLICATES,
                "n_valid_fits": int(finite.sum()),
                "valid_fit_rate": float(finite.mean()),
                "detection_count": count,
                "detection_probability": count / REPLICATES,
                "detection_probability_ci_low": low,
                "detection_probability_ci_high": high,
                "positive_call_probability": positive / REPLICATES if method == "primary_linear" else np.nan,
                "negative_call_probability": negative / REPLICATES if method == "primary_linear" else np.nan,
                "median_events": float(np.median(event_counts)),
            }
        )
    return rows


def aggregate(seed_frame: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "n_requested",
        "effect_pattern",
        "method",
        "method_alpha",
        "empirical_p_threshold",
    ]
    rows: list[dict[str, Any]] = []
    for values, group in seed_frame.groupby(keys, sort=True):
        row = dict(zip(keys, values))
        total = int(group.n_simulated_cohorts.sum())
        count = int(group.detection_count.sum())
        low, high = wilson(count, total)
        row.update(
            {
                "n_simulated_cohorts": total,
                "n_valid_fits": int(group.n_valid_fits.sum()),
                "valid_fit_rate": float(group.n_valid_fits.sum() / total),
                "detection_count": count,
                "detection_probability": count / total,
                "detection_probability_ci_low": low,
                "detection_probability_ci_high": high,
                "minimum_seed_probability": float(group.detection_probability.min()),
                "maximum_seed_probability": float(group.detection_probability.max()),
                "median_events_across_seeds": float(group.median_events.median()),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def null_calibration(grid: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    null = grid.loc[grid.effect_pattern.eq("null")]
    for method, group in null.groupby("method", sort=True):
        maximum = group.loc[group.detection_probability.idxmax()]
        count = int(maximum.detection_count)
        total = int(maximum.n_simulated_cohorts)
        alpha = float(maximum.method_alpha)
        tail = float(binom.sf(count - 1, total, alpha))
        family_tail = float(1 - (1 - tail) ** len(group))
        strict = bool((group.detection_probability_ci_low > alpha).any())
        invalid = bool(strict and family_tail < ALPHA)
        rows.append(
            {
                "method": method,
                "method_alpha": alpha,
                "n_null_cells": len(group),
                "median_null_probability": float(group.detection_probability.median()),
                "maximum_null_probability": float(maximum.detection_probability),
                "maximum_count": count,
                "maximum_total": total,
                "family_probability_maximum_at_least_observed": family_tail,
                "strict_cell_flag": strict,
                "strict_cell_flag_but_family_compatible": bool(strict and not invalid),
                "invalid_by_frozen_rule": invalid,
            }
        )
    return pd.DataFrame(rows)


def expected_diagnostic_comparison(grid: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for pattern, expected in EXPECTED_DIAGNOSTIC.items():
        for n in N_VALUES:
            selected = grid.loc[(grid.effect_pattern == pattern) & (grid.n_requested == n)].set_index("method")
            linear = selected.loc["primary_linear"]
            diagnostic = selected.loc[expected]
            gain = float(diagnostic.detection_probability - linear.detection_probability)
            seed_frame = _SEED_FRAME.loc[
                (_SEED_FRAME.effect_pattern == pattern)
                & (_SEED_FRAME.n_requested == n)
                & (_SEED_FRAME.method.isin(["primary_linear", expected]))
            ]
            pivot = seed_frame.pivot(index="seed", columns="method", values="detection_probability")
            minimum_seed_gain = float((pivot[expected] - pivot["primary_linear"]).min())
            materially_missed = bool(
                linear.detection_probability < 0.50
                and diagnostic.detection_probability >= 0.80
                and gain >= 0.20
                and minimum_seed_gain >= 0.20
            )
            rows.append(
                {
                    "effect_pattern": pattern,
                    "n_requested": n,
                    "expected_diagnostic": expected,
                    "primary_linear_probability": float(linear.detection_probability),
                    "expected_diagnostic_probability": float(diagnostic.detection_probability),
                    "aggregate_gain": gain,
                    "minimum_seed_gain": minimum_seed_gain,
                    "materially_missed_by_linear": materially_missed,
                }
            )
    return pd.DataFrame(rows)


def write_report(output_dir: Path, comparison: pd.DataFrame, calibration: pd.DataFrame, summary: dict[str, Any]) -> None:
    comparison_lines = "\n".join(
        f"- `{row.effect_pattern}`, n={row.n_requested}: linear "
        f"`{row.primary_linear_probability:.3f}`, expected diagnostic "
        f"`{row.expected_diagnostic_probability:.3f}`, gain `{row.aggregate_gain:.3f}`, "
        f"materially missed `{bool(row.materially_missed_by_linear)}`."
        for row in comparison.itertuples(index=False)
    )
    report = f"""# V54 Linear-Effect Misspecification Audit

Status: **{summary['verdict']}**.

This is seeded synthetic method behavior only. It is not evidence that an MS
molecular state has a linear, threshold, saturated, U-shaped, or inverted-U
relationship with progression.

## Expected Diagnostic Comparisons

{comparison_lines}

The primary remains one linear coefficient. The fixed threshold, saturated,
and linear-quadratic tests are multiplicity-controlled diagnostics. They can
flag a model class for a future, separately pre-registered study; they cannot
replace a failed primary model after outcomes are inspected.

## Calibration

All {len(calibration)} method families are assessed under their fixed alpha;
`{summary['n_invalid_null_families']}` are invalid and
`{summary['n_strict_cell_flag_but_family_compatible']}` have strict-cell but
family-compatible flags. Flagged families are excluded from any positive
performance claim.

## Boundary

The audit quantifies model behavior under fixed synthetic shapes. Even a clean
diagnostic advantage does not establish that shape in MS, validate a molecular
score, or identify a way to halt progression.
"""
    (output_dir / "REPORT.md").write_text(report)


_SEED_FRAME = pd.DataFrame()


def main() -> None:
    global _SEED_FRAME, CRITICAL_VALUES
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    CRITICAL_VALUES, threshold_frame = empirical_thresholds()
    rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        for n in N_VALUES:
            for pattern in PATTERNS:
                for row in simulate_cell(rng, n, pattern):
                    rows.append({"seed": seed, **row})
    _SEED_FRAME = pd.DataFrame(rows)
    grid = aggregate(_SEED_FRAME)
    calibration = null_calibration(grid)
    comparison = expected_diagnostic_comparison(grid)
    _SEED_FRAME.to_csv(output_dir / "seed_results.tsv", sep="\t", index=False)
    threshold_frame.to_csv(
        output_dir / "independent_null_calibration_thresholds.tsv", sep="\t", index=False
    )
    grid.to_csv(output_dir / "method_grid.tsv", sep="\t", index=False)
    calibration.to_csv(output_dir / "null_calibration.tsv", sep="\t", index=False)
    comparison.to_csv(output_dir / "expected_diagnostic_comparison.tsv", sep="\t", index=False)

    invalid = calibration.loc[calibration.invalid_by_frozen_rule, "method"].tolist()
    flagged = calibration.loc[
        calibration.strict_cell_flag_but_family_compatible, "method"
    ].tolist()
    summary = {
        "purpose": "V54 seeded synthetic progression linear-effect misspecification audit; no biological claim",
        "synthetic": True,
        "seeds": list(SEEDS),
        "calibration_seeds": list(CALIBRATION_SEEDS),
        "replicates_per_cell_seed": REPLICATES,
        "null_calibration_replicates_per_n_seed": CALIBRATION_REPLICATES,
        "n_independent_null_calibration_cohorts": len(CALIBRATION_SEEDS)
        * len(N_VALUES)
        * CALIBRATION_REPLICATES,
        "n_unique_simulated_cohorts": len(SEEDS) * len(N_VALUES) * len(PATTERNS) * REPLICATES,
        "n_method_route_evaluations": len(SEEDS) * len(N_VALUES) * len(PATTERNS) * REPLICATES * len(METHODS),
        "n_null_families": len(calibration),
        "n_invalid_null_families": len(invalid),
        "invalid_null_families": invalid,
        "n_strict_cell_flag_but_family_compatible": len(flagged),
        "strict_cell_flag_but_family_compatible": flagged,
        "n_expected_diagnostic_comparisons": len(comparison),
        "n_materially_missed_by_linear": int(comparison.materially_missed_by_linear.sum()),
        "materially_missed_cells": comparison.loc[
            comparison.materially_missed_by_linear,
            ["effect_pattern", "n_requested", "expected_diagnostic"],
        ].to_dict("records"),
        "verdict": "FIXED_NONLINEAR_DIAGNOSTICS_ARE_NONRESCUING_MODEL_CHECKS",
        "boundary": "Synthetic method behavior only; no empirical MS risk shape, progression association, or biological claim.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    config = {
        "purpose": summary["purpose"],
        "synthetic": True,
        "seeds": list(SEEDS),
        "calibration_seeds": list(CALIBRATION_SEEDS),
        "n_values": list(N_VALUES),
        "patterns": list(PATTERNS),
        "methods": list(METHODS),
        "replicates": REPLICATES,
        "null_calibration_replicates": CALIBRATION_REPLICATES,
        "event_probability": EVENT_PROBABILITY,
        "reliability": RELIABILITY,
        "score_missing": SCORE_MISSING,
        "primary_alpha": ALPHA,
        "diagnostic_alpha": DIAGNOSTIC_ALPHA,
        "material_miss_rule": "linear<0.50; expected diagnostic>=0.80; aggregate and every-seed gain>=0.20",
    }
    (output_dir / "simulation_config.json").write_text(json.dumps(config, indent=2) + "\n")
    write_report(output_dir, comparison, calibration, summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
