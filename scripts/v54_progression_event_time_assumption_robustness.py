#!/usr/bin/env python3
"""Audit Cox progression inference under time-varying effects and censoring."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.special import expit
from scipy.stats import binom, norm


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_event_time_assumption_robustness"
DEFAULT_SEEDS = [54901, 54902, 54903]
PATTERNS = {
    "null": (1.0, 1.0),
    "proportional": (1.7, 1.7),
    "early_only": (2.2, 1.0),
    "late_only": (1.0, 2.2),
    "crossing": (2.0, 0.5),
}
CENSORING = [
    "administrative_only",
    "independent",
    "score_dependent",
    "event_risk_dependent",
    "joint_score_event_risk",
]


def csv_numbers(value: str, cast: type) -> list[Any]:
    return [cast(item.strip()) for item in value.split(",") if item.strip()]


def wilson(successes: int, total: int) -> tuple[float, float]:
    if total <= 0:
        return np.nan, np.nan
    z = norm.ppf(0.975)
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    half = z * np.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return float(center - half), float(center + half)


def calibrate_scale(multiplier: np.ndarray, probability: float) -> np.ndarray:
    low = np.zeros(multiplier.shape[0])
    high = np.full(multiplier.shape[0], 20.0)
    for _ in range(50):
        middle = (low + high) / 2
        observed = np.mean(1 - np.exp(-middle[:, None] * multiplier), axis=1)
        below = observed < probability
        low[below] = middle[below]
        high[~below] = middle[~below]
    return (low + high) / 2


def calibrate_logistic_intercept(linear_predictor: np.ndarray, target: float) -> np.ndarray:
    low = np.full(linear_predictor.shape[0], -20.0)
    high = np.full(linear_predictor.shape[0], 20.0)
    for _ in range(50):
        middle = (low + high) / 2
        observed = expit(middle[:, None] + linear_predictor).mean(axis=1)
        below = observed < target
        low[below] = middle[below]
        high[~below] = middle[~below]
    return (low + high) / 2


def cox_score_test(
    score: np.ndarray,
    time: np.ndarray,
    event: np.ndarray,
    strata: np.ndarray,
) -> tuple[float, float, float]:
    score_statistic = 0.0
    information = 0.0
    for stratum in np.unique(strata):
        selected = strata == stratum
        if not np.any(event[selected]):
            continue
        order = np.argsort(time[selected], kind="mergesort")
        ordered_score = score[selected][order]
        ordered_event = event[selected][order]
        risk_n = np.arange(len(order), 0, -1, dtype=float)
        risk_sum = np.cumsum(ordered_score[::-1])[::-1]
        risk_sum_sq = np.cumsum(ordered_score[::-1] ** 2)[::-1]
        event_index = np.flatnonzero(ordered_event)
        risk_mean = risk_sum[event_index] / risk_n[event_index]
        risk_variance = risk_sum_sq[event_index] / risk_n[event_index] - risk_mean**2
        score_statistic += float(np.sum(ordered_score[event_index] - risk_mean))
        information += float(np.sum(np.maximum(risk_variance, 0.0)))
    if information <= 1e-12 or not np.isfinite(information):
        return np.nan, np.nan, np.nan
    z = score_statistic / np.sqrt(information)
    return float(z), float(2 * norm.sf(abs(z))), float(score_statistic / information)


def piecewise_event_time_from_exponential(
    exponential_draw: np.ndarray,
    baseline: np.ndarray,
    early_multiplier: np.ndarray,
    late_multiplier: np.ndarray,
    cut: float,
) -> np.ndarray:
    baseline_matrix = np.broadcast_to(baseline[:, None], exponential_draw.shape)
    early_cumulative_hazard = baseline_matrix * early_multiplier * cut
    event_time = np.empty_like(exponential_draw)
    early = exponential_draw <= early_cumulative_hazard
    event_time[early] = exponential_draw[early] / (
        baseline_matrix[early] * early_multiplier[early]
    )
    late_numerator = exponential_draw - early_cumulative_hazard
    event_time[~early] = cut + late_numerator[~early] / (
        baseline_matrix[~early] * late_multiplier[~early]
    )
    return event_time


def draw_event_times(
    rng: np.random.Generator,
    latent: np.ndarray,
    source: np.ndarray,
    treatment: np.ndarray,
    event_probability: float,
    early_hr: float,
    late_hr: float,
    cut: float,
) -> np.ndarray:
    nuisance = np.exp(np.log(1.6) * source + np.log(0.7) * treatment)
    early_multiplier = nuisance * np.exp(np.log(early_hr) * latent)
    late_multiplier = nuisance * np.exp(np.log(late_hr) * latent)
    horizon_multiplier = cut * early_multiplier + (1 - cut) * late_multiplier
    baseline = calibrate_scale(horizon_multiplier, event_probability)
    exponential_draw = -np.log(np.clip(rng.random(latent.shape), 1e-12, 1.0))
    return piecewise_event_time_from_exponential(
        exponential_draw, baseline, early_multiplier, late_multiplier, cut
    )


def finite_median(values: list[float] | np.ndarray) -> float:
    array = np.asarray(values, dtype=float)
    finite = array[np.isfinite(array)]
    return float(np.median(finite)) if len(finite) else np.nan


def draw_censoring(
    rng: np.random.Generator,
    mechanism: str,
    latent: np.ndarray,
    event_time: np.ndarray,
    target: float,
) -> tuple[np.ndarray, np.ndarray]:
    if mechanism == "administrative_only":
        return np.ones_like(event_time), np.zeros_like(event_time, dtype=bool)

    if mechanism == "independent":
        probability = np.full_like(event_time, target)
        censor_time = rng.uniform(0.05, 1.0, size=event_time.shape)
    else:
        event_risk = -np.log(np.clip(event_time, 0.02, 20.0))
        event_risk = (event_risk - event_risk.mean(axis=1, keepdims=True)) / np.maximum(
            event_risk.std(axis=1, keepdims=True), 1e-8
        )
        if mechanism == "score_dependent":
            linear = 1.5 * latent
            independent_timing = True
        elif mechanism == "event_risk_dependent":
            linear = 1.5 * event_risk
            independent_timing = False
        elif mechanism == "joint_score_event_risk":
            linear = 0.75 * latent + 0.75 * event_risk + 2.0 * latent * event_risk
            independent_timing = False
        else:
            raise ValueError(f"Unknown censoring mechanism: {mechanism}")
        intercept = calibrate_logistic_intercept(linear, target)
        probability = expit(intercept[:, None] + linear)
        if independent_timing:
            censor_time = rng.uniform(0.05, 1.0, size=event_time.shape)
        else:
            before_event_or_horizon = np.minimum(event_time, 1.0)
            censor_time = rng.uniform(0.1, 0.9, size=event_time.shape) * before_event_or_horizon

    assigned = rng.random(event_time.shape) < probability
    return np.where(assigned, censor_time, 1.0), assigned


def analysis_views(
    observed_time: np.ndarray, event: np.ndarray, cut: float
) -> dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]]:
    all_rows = np.ones(observed_time.shape[0], dtype=bool)
    early_time = np.minimum(observed_time, cut)
    early_event = event & (observed_time <= cut)
    late_rows = observed_time > cut
    late_time = observed_time[late_rows] - cut
    late_event = event[late_rows]
    return {
        "whole_followup": (all_rows, observed_time, event),
        "early_window_diagnostic": (all_rows, early_time, early_event),
        "late_landmark_diagnostic": (late_rows, late_time, late_event),
    }


def simulate_cell(
    *,
    rng: np.random.Generator,
    n: int,
    event_probability: float,
    pattern: str,
    censoring: str,
    replicates: int,
    cut: float,
    dropout_target: float,
    reliability: float,
    missing_rate: float,
    alpha: float,
) -> list[dict[str, Any]]:
    latent = rng.normal(size=(replicates, n))
    source = rng.random((replicates, n)) < expit(0.8 * latent)
    treatment = rng.random((replicates, n)) < expit(0.5 * source - 0.8 * latent)
    early_hr, late_hr = PATTERNS[pattern]
    event_time = draw_event_times(
        rng, latent, source, treatment, event_probability, early_hr, late_hr, cut
    )
    censor_time, dropout_assigned = draw_censoring(
        rng, censoring, latent, event_time, dropout_target
    )
    event = event_time <= censor_time
    observed_time = np.minimum(event_time, censor_time)
    observed_score = (
        np.sqrt(reliability) * latent
        + np.sqrt(1 - reliability) * rng.normal(size=latent.shape)
    )
    included = rng.random(latent.shape) >= missing_rate
    strata = 2 * source.astype(np.int8) + treatment.astype(np.int8)

    accumulators = {
        name: {
            "valid": 0,
            "positive": 0,
            "negative": 0,
            "z": [],
            "one_step": [],
            "events": [],
            "usable": [],
            "dropout_assigned": [],
            "dropout_observed": [],
        }
        for name in [
            "whole_followup",
            "early_window_diagnostic",
            "late_landmark_diagnostic",
        ]
    }

    for replicate in range(replicates):
        base_keep = included[replicate]
        views = analysis_views(observed_time[replicate], event[replicate], cut)
        for name, (view_keep, view_time, view_event) in views.items():
            keep = base_keep & view_keep
            time = view_time if len(view_time) == n else view_time
            outcome = view_event if len(view_event) == n else view_event
            if len(time) == n:
                selected_time = time[keep]
                selected_event = outcome[keep]
                selected_score = observed_score[replicate, keep]
                selected_strata = strata[replicate, keep]
                selected_dropout = dropout_assigned[replicate, keep]
                selected_censor = censor_time[replicate, keep] < np.minimum(
                    event_time[replicate, keep], 1.0
                )
            else:
                landmark_indices = np.flatnonzero(view_keep)
                retained_base = base_keep[landmark_indices]
                selected_time = time[retained_base]
                selected_event = outcome[retained_base]
                selected_score = observed_score[replicate, landmark_indices][retained_base]
                selected_strata = strata[replicate, landmark_indices][retained_base]
                selected_dropout = dropout_assigned[replicate, landmark_indices][retained_base]
                selected_censor = censor_time[replicate, landmark_indices][retained_base] < np.minimum(
                    event_time[replicate, landmark_indices][retained_base], 1.0
                )

            accumulator = accumulators[name]
            usable_n = len(selected_score)
            observed_events = int(selected_event.sum())
            accumulator["usable"].append(usable_n)
            accumulator["events"].append(observed_events)
            accumulator["dropout_assigned"].append(float(selected_dropout.mean()) if usable_n else np.nan)
            accumulator["dropout_observed"].append(float(selected_censor.mean()) if usable_n else np.nan)
            if usable_n < 20 or observed_events < 10 or usable_n - observed_events < 10:
                continue
            score_sd = float(np.std(selected_score, ddof=1))
            if not np.isfinite(score_sd) or score_sd <= 0:
                continue
            standardized = (selected_score - selected_score.mean()) / score_sd
            z, p_value, one_step = cox_score_test(
                standardized, selected_time, selected_event, selected_strata
            )
            if not np.isfinite(p_value):
                continue
            accumulator["valid"] += 1
            accumulator["z"].append(z)
            accumulator["one_step"].append(one_step)
            if p_value <= alpha and z > 0:
                accumulator["positive"] += 1
            if p_value <= alpha and z < 0:
                accumulator["negative"] += 1

    rows = []
    for name, accumulator in accumulators.items():
        positive = int(accumulator["positive"])
        negative = int(accumulator["negative"])
        significant = positive + negative
        ci_low, ci_high = wilson(significant, replicates)
        rows.append(
            {
                "analysis_window": name,
                "n_requested": n,
                "event_probability_before_censoring": event_probability,
                "effect_pattern": pattern,
                "early_hazard_ratio_per_latent_sd": early_hr,
                "late_hazard_ratio_per_latent_sd": late_hr,
                "censoring_mechanism": censoring,
                "dropout_target": 0.0 if censoring == "administrative_only" else dropout_target,
                "n_simulated_cohorts": replicates,
                "n_valid_fits": accumulator["valid"],
                "valid_fit_rate": accumulator["valid"] / replicates,
                "significant_count": significant,
                "significant_probability": significant / replicates,
                "significant_probability_ci_low": ci_low,
                "significant_probability_ci_high": ci_high,
                "positive_call_probability": positive / replicates,
                "negative_call_probability": negative / replicates,
                "median_score_z": float(np.median(accumulator["z"])) if accumulator["z"] else np.nan,
                "median_one_step_log_hr": float(np.median(accumulator["one_step"])) if accumulator["one_step"] else np.nan,
                "median_usable_n": float(np.nanmedian(accumulator["usable"])),
                "median_observed_events": float(np.nanmedian(accumulator["events"])),
                "median_assigned_dropout": finite_median(accumulator["dropout_assigned"]),
                "median_observed_pre_event_dropout": finite_median(accumulator["dropout_observed"]),
            }
        )
    return rows


def aggregate(frame: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "analysis_window",
        "n_requested",
        "event_probability_before_censoring",
        "effect_pattern",
        "early_hazard_ratio_per_latent_sd",
        "late_hazard_ratio_per_latent_sd",
        "censoring_mechanism",
        "dropout_target",
    ]
    rows = []
    for values, group in frame.groupby(keys, sort=True, dropna=False):
        row = dict(zip(keys, values))
        total = int(group.n_simulated_cohorts.sum())
        significant = int(group.significant_count.sum())
        positive = int(round((group.positive_call_probability * group.n_simulated_cohorts).sum()))
        negative = int(round((group.negative_call_probability * group.n_simulated_cohorts).sum()))
        low, high = wilson(significant, total)
        row.update(
            {
                "n_simulated_cohorts": total,
                "n_valid_fits": int(group.n_valid_fits.sum()),
                "valid_fit_rate": float(group.n_valid_fits.sum() / total),
                "significant_count": significant,
                "significant_probability": significant / total,
                "significant_probability_ci_low": low,
                "significant_probability_ci_high": high,
                "minimum_seed_significant_probability": float(group.significant_probability.min()),
                "maximum_seed_significant_probability": float(group.significant_probability.max()),
                "positive_call_probability": positive / total,
                "negative_call_probability": negative / total,
                "median_score_z_across_seeds": finite_median(group.median_score_z.to_numpy()),
                "median_one_step_log_hr_across_seeds": finite_median(group.median_one_step_log_hr.to_numpy()),
                "median_usable_n_across_seeds": float(group.median_usable_n.median()),
                "median_observed_events_across_seeds": float(group.median_observed_events.median()),
                "median_assigned_dropout_across_seeds": float(group.median_assigned_dropout.median()),
                "median_observed_pre_event_dropout_across_seeds": float(group.median_observed_pre_event_dropout.median()),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def calibration_summary(grid: pd.DataFrame, alpha: float) -> pd.DataFrame:
    null = grid.loc[
        grid.effect_pattern.eq("null") & grid.analysis_window.eq("whole_followup")
    ]
    rows = []
    for mechanism, group in null.groupby("censoring_mechanism", sort=True):
        maximum = group.loc[group.significant_probability.idxmax()]
        count = int(maximum.significant_count)
        total = int(maximum.n_simulated_cohorts)
        single_tail = float(binom.sf(count - 1, total, alpha))
        max_tail = float(1 - (1 - single_tail) ** len(group))
        anti = bool((group.significant_probability_ci_low > alpha).any())
        rows.append(
            {
                "censoring_mechanism": mechanism,
                "n_cells": len(group),
                "median_null_probability": float(group.significant_probability.median()),
                "maximum_null_probability": float(maximum.significant_probability),
                "maximum_count": count,
                "maximum_total": total,
                "maximum_ci_low": float(maximum.significant_probability_ci_low),
                "maximum_ci_high": float(maximum.significant_probability_ci_high),
                "family_probability_maximum_at_least_observed": max_tail,
                "anti_conservative_by_frozen_rule": anti,
                "maximum_positive_call_probability": float(group.positive_call_probability.max()),
                "maximum_negative_call_probability": float(group.negative_call_probability.max()),
            }
        )
    return pd.DataFrame(rows)


def nph_snapshot(grid: pd.DataFrame, calibrated: set[str]) -> pd.DataFrame:
    selected = grid.loc[
        grid.censoring_mechanism.isin(calibrated)
        & grid.n_requested.eq(grid.n_requested.max())
        & grid.event_probability_before_censoring.eq(0.30)
    ].copy()
    return selected.sort_values(["effect_pattern", "censoring_mechanism", "analysis_window"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-sizes", default="120,240,320")
    parser.add_argument("--event-probabilities", default="0.15,0.30")
    parser.add_argument("--replicates-per-seed", type=int, default=500)
    parser.add_argument("--seeds", default=",".join(map(str, DEFAULT_SEEDS)))
    parser.add_argument("--cut", type=float, default=0.5)
    parser.add_argument("--dropout-target", type=float, default=0.25)
    parser.add_argument("--reliability", type=float, default=0.70)
    parser.add_argument("--missing-rate", type=float, default=0.10)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    sizes = csv_numbers(args.sample_sizes, int)
    probabilities = csv_numbers(args.event_probabilities, float)
    seeds = csv_numbers(args.seeds, int)
    if len(seeds) < 2:
        raise SystemExit("At least two seeds are required")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    config = {
        "synthetic": True,
        "sample_sizes": sizes,
        "event_probabilities_before_censoring": probabilities,
        "effect_patterns": PATTERNS,
        "censoring_mechanisms": CENSORING,
        "replicates_per_seed": args.replicates_per_seed,
        "seeds": seeds,
        "piecewise_cut": args.cut,
        "dropout_target": args.dropout_target,
        "measurement_reliability": args.reliability,
        "missing_rate": args.missing_rate,
        "alpha": args.alpha,
        "boundary": "Seeded synthetic method behavior only; not empirical MS evidence or an empirical dropout estimate.",
    }
    (args.output_dir / "simulation_config.json").write_text(json.dumps(config, indent=2) + "\n")

    seed_rows = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for n in sizes:
            for probability in probabilities:
                for pattern in PATTERNS:
                    for censoring in CENSORING:
                        rows = simulate_cell(
                            rng=rng,
                            n=n,
                            event_probability=probability,
                            pattern=pattern,
                            censoring=censoring,
                            replicates=args.replicates_per_seed,
                            cut=args.cut,
                            dropout_target=args.dropout_target,
                            reliability=args.reliability,
                            missing_rate=args.missing_rate,
                            alpha=args.alpha,
                        )
                        seed_rows.extend({"seed": seed, **row} for row in rows)

    seed_frame = pd.DataFrame(seed_rows)
    seed_frame.to_csv(args.output_dir / "seed_results.tsv", sep="\t", index=False)
    grid = aggregate(seed_frame)
    grid.to_csv(args.output_dir / "assumption_grid.tsv", sep="\t", index=False)
    calibration = calibration_summary(grid, args.alpha)
    calibration.to_csv(args.output_dir / "null_calibration_by_censoring.tsv", sep="\t", index=False)
    calibrated = set(
        calibration.loc[~calibration.anti_conservative_by_frozen_rule, "censoring_mechanism"]
    )
    snapshot = nph_snapshot(grid, calibrated)
    snapshot.to_csv(args.output_dir / "nph_diagnostic_snapshot.tsv", sep="\t", index=False)

    whole = snapshot.loc[snapshot.analysis_window.eq("whole_followup")]
    crossing = snapshot.loc[snapshot.effect_pattern.eq("crossing")]
    crossing_whole = crossing.loc[crossing.analysis_window.eq("whole_followup")]
    crossing_early = crossing.loc[crossing.analysis_window.eq("early_window_diagnostic")]
    crossing_late = crossing.loc[crossing.analysis_window.eq("late_landmark_diagnostic")]
    summary = {
        "purpose": "Synthetic Cox assumption audit under non-proportional effects and informative censoring; no biological claim",
        "synthetic": True,
        "n_unique_simulated_cohorts": len(seeds) * len(sizes) * len(probabilities) * len(PATTERNS) * len(CENSORING) * args.replicates_per_seed,
        "n_analysis_evaluations": int(seed_frame.n_simulated_cohorts.sum()),
        "n_aggregate_cells": len(grid),
        "calibrated_censoring_mechanisms": sorted(calibrated),
        "invalid_censoring_mechanisms": sorted(set(CENSORING) - calibrated),
        "whole_followup_cells_at_n320_event030": len(whole),
        "crossing_whole_median_detection_calibrated": float(crossing_whole.significant_probability.median()) if len(crossing_whole) else None,
        "crossing_early_median_positive_call_calibrated": float(crossing_early.positive_call_probability.median()) if len(crossing_early) else None,
        "crossing_late_median_negative_call_calibrated": float(crossing_late.negative_call_probability.median()) if len(crossing_late) else None,
        "verdict": "COX_ROUTE_REQUIRES_CENSORING_AUDIT_AND_TIME_VARIATION_DIAGNOSTICS",
        "boundary": "All values arise from seeded synthetic assumptions. They are method behavior, not empirical MS hazards, progression effects, or dropout rates.",
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = [
        "# V54 Progression Event-Time Assumption Robustness",
        "",
        "All results are seeded synthetic method behavior, not biological evidence.",
        "",
        f"The audit generated {summary['n_unique_simulated_cohorts']:,} unique synthetic cohorts and {summary['n_analysis_evaluations']:,} window evaluations.",
        "",
        "## Whole-Follow-Up Null Calibration",
        "",
        "| censoring mechanism | cells | median null | maximum null | Wilson CI | family max-tail | frozen verdict |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in calibration.itertuples(index=False):
        lines.append(
            f"| {row.censoring_mechanism} | {row.n_cells} | {row.median_null_probability:.3f} | "
            f"{row.maximum_null_probability:.3f} | {row.maximum_ci_low:.3f}-{row.maximum_ci_high:.3f} | "
            f"{row.family_probability_maximum_at_least_observed:.3f} | "
            f"{'INVALID' if row.anti_conservative_by_frozen_rule else 'calibrated'} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "Only censoring families passing the frozen null rule are eligible for power interpretation. Early and late windows are diagnostics, not post-hoc replacement analyses. A whole-follow-up null under a crossing effect cannot establish absence when the window diagnostics recover opposite signs.",
            "",
            "See `nph_diagnostic_snapshot.tsv` for the fixed n=320, pre-censoring event-probability 0.30 comparison.",
        ]
    )
    (args.output_dir / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
