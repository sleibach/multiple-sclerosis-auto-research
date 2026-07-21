#!/usr/bin/env python3
"""Audit progression inference under scheduled, confirmatory observation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.special import expit
from scipy.stats import binom, norm

from v54_progression_event_time_assumption_robustness import (
    calibrate_logistic_intercept,
    calibrate_scale,
    finite_median,
    wilson,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_visit_schedule_robustness"
DEFAULT_SEEDS = [54941, 54942, 54943]
HORIZON = 2.0
CONFIRMATION_LAG = 0.25
MECHANISMS = [
    "complete",
    "independent_20pct",
    "score_dependent_20pct",
    "joint_score_progression_risk_20pct",
]
ROUTES = [
    "full_latent_time_oracle",
    "ascertained_latent_time_oracle",
    "detected_visit_time",
    "midpoint_imputed_time",
]


def csv_numbers(value: str, cast: type) -> list[Any]:
    return [cast(item.strip()) for item in value.split(",") if item.strip()]


def breslow_score_test(
    score: np.ndarray,
    time: np.ndarray,
    event: np.ndarray,
    strata: np.ndarray,
) -> tuple[float, float, float]:
    """Cox score, two-sided p-value, and one-step beta at zero with ties."""
    score_statistic = 0.0
    information = 0.0
    for stratum in np.unique(strata):
        selected = strata == stratum
        if not np.any(event[selected]):
            continue
        order = np.argsort(time[selected], kind="mergesort")
        ordered_time = time[selected][order]
        ordered_score = score[selected][order]
        ordered_event = event[selected][order]
        risk_sum = np.cumsum(ordered_score[::-1])[::-1]
        risk_sum_sq = np.cumsum(ordered_score[::-1] ** 2)[::-1]
        event_time = ordered_time[ordered_event]
        event_score = ordered_score[ordered_event]
        unique_time, inverse, event_count = np.unique(
            event_time, return_inverse=True, return_counts=True
        )
        first_risk = np.searchsorted(ordered_time, unique_time, side="left")
        risk_count = len(order) - first_risk
        event_score_sum = np.bincount(
            inverse, weights=event_score, minlength=len(unique_time)
        )
        risk_mean = risk_sum[first_risk] / risk_count
        risk_variance = (
            risk_sum_sq[first_risk] / risk_count - risk_mean**2
        )
        score_statistic += float(
            np.sum(event_score_sum - event_count * risk_mean)
        )
        information += float(
            np.sum(event_count * np.maximum(risk_variance, 0.0))
        )
    if information <= 1e-12 or not np.isfinite(information):
        return np.nan, np.nan, np.nan
    z_value = score_statistic / np.sqrt(information)
    return (
        float(z_value),
        float(2 * norm.sf(abs(z_value))),
        float(score_statistic / information),
    )


def attendance_probability(
    mechanism: str,
    latent_score: np.ndarray,
    progression_frailty: np.ndarray,
) -> np.ndarray:
    if mechanism == "complete":
        return np.ones_like(latent_score)
    if mechanism == "independent_20pct":
        return np.full_like(latent_score, 0.80)
    if mechanism == "score_dependent_20pct":
        missing_linear = 1.2 * latent_score
    elif mechanism == "joint_score_progression_risk_20pct":
        missing_linear = (
            0.6 * latent_score
            + 0.6 * progression_frailty
            + 1.8 * latent_score * progression_frailty
        )
    else:
        raise ValueError(f"Unknown attendance mechanism: {mechanism}")
    intercept = calibrate_logistic_intercept(missing_linear, 0.20)
    return 1.0 - expit(intercept[:, None] + missing_linear)


def observe_schedule(
    rng: np.random.Generator,
    latent_time: np.ndarray,
    attendance_probability_by_subject: np.ndarray,
    interval: float,
) -> dict[str, np.ndarray]:
    visits = np.arange(interval, HORIZON + 1e-9, interval)
    attendance = rng.random((*latent_time.shape, len(visits))) < (
        attendance_probability_by_subject[:, :, None]
    )
    detected = np.zeros(latent_time.shape, dtype=bool)
    confirmed = np.zeros(latent_time.shape, dtype=bool)
    detection_time = np.full(latent_time.shape, np.nan)
    prior_normal_time = np.zeros(latent_time.shape)
    last_attended_time = np.zeros(latent_time.shape)
    for visit_index, visit_time in enumerate(visits):
        attended = attendance[:, :, visit_index]
        last_attended_time[attended] = visit_time
        can_confirm = (
            detected
            & ~confirmed
            & attended
            & (visit_time >= detection_time + CONFIRMATION_LAG - 1e-12)
        )
        confirmed[can_confirm] = True
        newly_detected = (
            ~detected & attended & (latent_time <= visit_time)
        )
        detection_time[newly_detected] = visit_time
        detected[newly_detected] = True
        still_normal = ~detected & attended
        prior_normal_time[still_normal] = visit_time
    midpoint_time = (prior_normal_time + detection_time) / 2
    latent_event = latent_time <= HORIZON
    return {
        "latent_event": latent_event,
        "confirmed": confirmed,
        "detection_time": detection_time,
        "midpoint_time": midpoint_time,
        "last_attended_time": last_attended_time,
        "attendance": attendance,
    }


def analyze_route(
    *,
    observed_score: np.ndarray,
    included: np.ndarray,
    strata: np.ndarray,
    time: np.ndarray,
    event: np.ndarray,
    latent_event: np.ndarray,
    confirmed: np.ndarray,
    detection_delay: np.ndarray,
    replicates: int,
    alpha: float,
) -> dict[str, Any]:
    valid = positive = negative = 0
    z_values: list[float] = []
    one_steps: list[float] = []
    usable_values: list[int] = []
    event_values: list[int] = []
    latent_values: list[int] = []
    unconfirmed_values: list[int] = []
    delay_values: list[float] = []
    for replicate in range(replicates):
        keep = included[replicate]
        usable = int(keep.sum())
        events = int(event[replicate, keep].sum())
        latent_events = int(latent_event[replicate, keep].sum())
        unconfirmed = int(
            (latent_event[replicate, keep] & ~confirmed[replicate, keep]).sum()
        )
        usable_values.append(usable)
        event_values.append(events)
        latent_values.append(latent_events)
        unconfirmed_values.append(unconfirmed)
        delays = detection_delay[replicate, keep]
        delays = delays[np.isfinite(delays)]
        if len(delays):
            delay_values.append(float(np.median(delays)))
        if usable < 20 or events < 10 or usable - events < 10:
            continue
        score = observed_score[replicate, keep]
        sd = float(np.std(score, ddof=1))
        if not np.isfinite(sd) or sd <= 0:
            continue
        score = (score - score.mean()) / sd
        z_value, p_value, one_step = breslow_score_test(
            score,
            time[replicate, keep],
            event[replicate, keep],
            strata[replicate, keep],
        )
        if not np.isfinite(p_value):
            continue
        valid += 1
        z_values.append(z_value)
        one_steps.append(one_step)
        if p_value <= alpha and z_value > 0:
            positive += 1
        if p_value <= alpha and z_value < 0:
            negative += 1
    significant = positive + negative
    low, high = wilson(significant, replicates)
    return {
        "n_simulated_cohorts": replicates,
        "n_valid_fits": valid,
        "valid_fit_rate": valid / replicates,
        "significant_count": significant,
        "significant_probability": significant / replicates,
        "significant_probability_ci_low": low,
        "significant_probability_ci_high": high,
        "positive_call_probability": positive / replicates,
        "negative_call_probability": negative / replicates,
        "median_score_z": finite_median(z_values),
        "median_one_step_log_hr": finite_median(one_steps),
        "median_usable_n": float(np.median(usable_values)),
        "median_analyzed_events": float(np.median(event_values)),
        "median_latent_events": float(np.median(latent_values)),
        "median_unconfirmed_latent_events": float(np.median(unconfirmed_values)),
        "median_detection_delay": finite_median(delay_values),
    }


def simulate_cell(
    *,
    rng: np.random.Generator,
    n: int,
    event_probability: float,
    molecular_hr: float,
    interval: float,
    mechanism: str,
    replicates: int,
    reliability: float,
    score_missing_rate: float,
    alpha: float,
) -> list[dict[str, Any]]:
    latent_score = rng.normal(size=(replicates, n))
    progression_frailty = rng.normal(size=(replicates, n))
    source = rng.random((replicates, n)) < expit(0.8 * latent_score)
    treatment = rng.random((replicates, n)) < expit(
        0.5 * source.astype(float) - 0.8 * latent_score
    )
    multiplier = np.exp(
        np.log(molecular_hr) * latent_score
        + 0.7 * progression_frailty
        + np.log(1.6) * source
        + np.log(0.7) * treatment
    )
    baseline = calibrate_scale(HORIZON * multiplier, event_probability)
    latent_time = -np.log(
        np.clip(rng.random((replicates, n)), 1e-12, 1.0)
    ) / (baseline[:, None] * multiplier)
    observed_score = (
        np.sqrt(reliability) * latent_score
        + np.sqrt(1 - reliability) * rng.normal(size=latent_score.shape)
    )
    included = rng.random(latent_score.shape) >= score_missing_rate
    strata = 2 * source.astype(np.int8) + treatment.astype(np.int8)
    subject_attendance_probability = attendance_probability(
        mechanism, latent_score, progression_frailty
    )
    observed = observe_schedule(
        rng, latent_time, subject_attendance_probability, interval
    )
    confirmed = observed["confirmed"]
    latent_event = observed["latent_event"]
    censor_time = observed["last_attended_time"]
    detection_delay = np.where(
        confirmed, observed["detection_time"] - latent_time, np.nan
    )
    route_data = {
        "full_latent_time_oracle": (
            np.minimum(latent_time, HORIZON),
            latent_event,
        ),
        "ascertained_latent_time_oracle": (
            np.where(confirmed, latent_time, censor_time),
            confirmed,
        ),
        "detected_visit_time": (
            np.where(confirmed, observed["detection_time"], censor_time),
            confirmed,
        ),
        "midpoint_imputed_time": (
            np.where(confirmed, observed["midpoint_time"], censor_time),
            confirmed,
        ),
    }
    achieved_missing = float(1 - observed["attendance"].mean())
    rows = []
    for route in ROUTES:
        time, event = route_data[route]
        result = analyze_route(
            observed_score=observed_score,
            included=included,
            strata=strata,
            time=time,
            event=event,
            latent_event=latent_event,
            confirmed=confirmed,
            detection_delay=detection_delay,
            replicates=replicates,
            alpha=alpha,
        )
        rows.append(
            {
                "n_requested": n,
                "latent_event_probability": event_probability,
                "molecular_progression_hr_per_latent_sd": molecular_hr,
                "visit_interval_years": interval,
                "attendance_mechanism": mechanism,
                "analysis_route": route,
                "achieved_missing_visit_probability": achieved_missing,
                **result,
            }
        )
    return rows


def aggregate(seed_frame: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "n_requested",
        "latent_event_probability",
        "molecular_progression_hr_per_latent_sd",
        "visit_interval_years",
        "attendance_mechanism",
        "analysis_route",
    ]
    rows = []
    for values, group in seed_frame.groupby(keys, sort=True, dropna=False):
        row = dict(zip(keys, values))
        total = int(group.n_simulated_cohorts.sum())
        significant = int(group.significant_count.sum())
        positive = int(
            round((group.positive_call_probability * group.n_simulated_cohorts).sum())
        )
        negative = int(
            round((group.negative_call_probability * group.n_simulated_cohorts).sum())
        )
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
                "minimum_seed_probability": float(group.significant_probability.min()),
                "maximum_seed_probability": float(group.significant_probability.max()),
                "positive_call_probability": positive / total,
                "negative_call_probability": negative / total,
                "median_score_z_across_seeds": finite_median(group.median_score_z),
                "median_one_step_log_hr_across_seeds": finite_median(
                    group.median_one_step_log_hr
                ),
                "median_usable_n_across_seeds": float(group.median_usable_n.median()),
                "median_analyzed_events_across_seeds": float(
                    group.median_analyzed_events.median()
                ),
                "median_latent_events_across_seeds": float(
                    group.median_latent_events.median()
                ),
                "median_unconfirmed_latent_events_across_seeds": float(
                    group.median_unconfirmed_latent_events.median()
                ),
                "median_detection_delay_across_seeds": finite_median(
                    group.median_detection_delay
                ),
                "achieved_missing_visit_probability": float(
                    group.achieved_missing_visit_probability.mean()
                ),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def calibration(grid: pd.DataFrame, alpha: float) -> pd.DataFrame:
    observed_routes = {"detected_visit_time", "midpoint_imputed_time"}
    null = grid.loc[
        grid.molecular_progression_hr_per_latent_sd.eq(1.0)
        & grid.analysis_route.isin(observed_routes)
    ]
    rows = []
    for (route, mechanism), group in null.groupby(
        ["analysis_route", "attendance_mechanism"], sort=True
    ):
        maximum = group.loc[group.significant_probability.idxmax()]
        count = int(maximum.significant_count)
        total = int(maximum.n_simulated_cohorts)
        single_tail = float(binom.sf(count - 1, total, alpha))
        family_tail = float(1 - (1 - single_tail) ** len(group))
        strict_flag = bool((group.significant_probability_ci_low > alpha).any())
        invalid = strict_flag and family_tail < 0.05
        rows.append(
            {
                "analysis_route": route,
                "attendance_mechanism": mechanism,
                "n_null_cells": len(group),
                "median_null_probability": float(group.significant_probability.median()),
                "maximum_null_probability": float(maximum.significant_probability),
                "maximum_count": count,
                "maximum_total": total,
                "maximum_ci_low": float(maximum.significant_probability_ci_low),
                "maximum_ci_high": float(maximum.significant_probability_ci_high),
                "family_probability_maximum_at_least_observed": family_tail,
                "strict_cell_flag": strict_flag,
                "invalid_by_frozen_rule": invalid,
                "maximum_positive_call_probability": float(
                    group.positive_call_probability.max()
                ),
                "maximum_negative_call_probability": float(
                    group.negative_call_probability.max()
                ),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-sizes", default="120,240,320")
    parser.add_argument("--event-probabilities", default="0.15,0.30")
    parser.add_argument("--molecular-hrs", default="1.0,1.7")
    parser.add_argument("--visit-intervals", default="0.25,0.50,1.00")
    parser.add_argument("--replicates-per-seed", type=int, default=400)
    parser.add_argument("--seeds", default=",".join(map(str, DEFAULT_SEEDS)))
    parser.add_argument("--reliability", type=float, default=0.70)
    parser.add_argument("--score-missing-rate", type=float, default=0.10)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    sizes = csv_numbers(args.sample_sizes, int)
    event_probabilities = csv_numbers(args.event_probabilities, float)
    molecular_hrs = csv_numbers(args.molecular_hrs, float)
    intervals = csv_numbers(args.visit_intervals, float)
    seeds = csv_numbers(args.seeds, int)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    config = {
        "synthetic": True,
        "horizon_years": HORIZON,
        "confirmation_lag_years": CONFIRMATION_LAG,
        "sample_sizes": sizes,
        "latent_event_probabilities": event_probabilities,
        "molecular_progression_hrs_per_latent_sd": molecular_hrs,
        "visit_intervals_years": intervals,
        "attendance_mechanisms": MECHANISMS,
        "analysis_routes": ROUTES,
        "replicates_per_seed": args.replicates_per_seed,
        "seeds": seeds,
        "measurement_reliability": args.reliability,
        "score_missing_rate": args.score_missing_rate,
        "alpha": args.alpha,
        "boundary": "Seeded synthetic method behavior only; not empirical MS progression, attendance, treatment, or biology.",
    }
    (args.output_dir / "simulation_config.json").write_text(
        json.dumps(config, indent=2) + "\n"
    )

    seed_rows = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for n in sizes:
            for event_probability in event_probabilities:
                for molecular_hr in molecular_hrs:
                    for interval in intervals:
                        for mechanism in MECHANISMS:
                            rows = simulate_cell(
                                rng=rng,
                                n=n,
                                event_probability=event_probability,
                                molecular_hr=molecular_hr,
                                interval=interval,
                                mechanism=mechanism,
                                replicates=args.replicates_per_seed,
                                reliability=args.reliability,
                                score_missing_rate=args.score_missing_rate,
                                alpha=args.alpha,
                            )
                            seed_rows.extend({"seed": seed, **row} for row in rows)
    seed_frame = pd.DataFrame(seed_rows)
    seed_frame.to_csv(args.output_dir / "seed_results.tsv", sep="\t", index=False)
    grid = aggregate(seed_frame)
    grid.to_csv(args.output_dir / "visit_schedule_grid.tsv", sep="\t", index=False)
    calibration_frame = calibration(grid, args.alpha)
    calibration_frame.to_csv(
        args.output_dir / "null_calibration_by_route_mechanism.tsv",
        sep="\t",
        index=False,
    )
    calibrated_pairs = {
        (row.analysis_route, row.attendance_mechanism)
        for row in calibration_frame.itertuples(index=False)
        if not row.strict_cell_flag
    }
    strict_family_compatible = {
        (row.analysis_route, row.attendance_mechanism)
        for row in calibration_frame.itertuples(index=False)
        if row.strict_cell_flag and not row.invalid_by_frozen_rule
    }
    invalid_pairs = {
        (row.analysis_route, row.attendance_mechanism)
        for row in calibration_frame.itertuples(index=False)
        if row.invalid_by_frozen_rule
    }
    eligible = grid.apply(
        lambda row: (row.analysis_route, row.attendance_mechanism)
        in calibrated_pairs,
        axis=1,
    )
    nonnull = grid.loc[
        grid.molecular_progression_hr_per_latent_sd.gt(1.0) & eligible
    ]
    scenario_keys = [
        "latent_event_probability",
        "molecular_progression_hr_per_latent_sd",
        "visit_interval_years",
        "attendance_mechanism",
        "analysis_route",
    ]
    thresholds = []
    for values, group in nonnull.groupby(scenario_keys, sort=True):
        ordered = group.sort_values("n_requested")
        reached = ordered.loc[
            ordered.significant_probability.ge(0.80)
            & ordered.minimum_seed_probability.ge(0.75)
            & ordered.positive_call_probability.eq(ordered.significant_probability)
        ]
        row = dict(zip(scenario_keys, values))
        row["minimum_n_reaching_80pct"] = (
            "not_reached" if reached.empty else int(reached.iloc[0].n_requested)
        )
        row["power_at_n320"] = float(ordered.iloc[-1].positive_call_probability)
        row["median_events_at_n320"] = float(
            ordered.iloc[-1].median_analyzed_events_across_seeds
        )
        row["median_unconfirmed_at_n320"] = float(
            ordered.iloc[-1].median_unconfirmed_latent_events_across_seeds
        )
        thresholds.append(row)
    threshold_frame = pd.DataFrame(thresholds)
    threshold_frame.to_csv(
        args.output_dir / "calibrated_observed_route_power.tsv",
        sep="\t",
        index=False,
    )

    def labels(values: set[tuple[str, str]]) -> list[str]:
        return sorted(f"{route}|{mechanism}" for route, mechanism in values)

    summary = {
        "purpose": "Synthetic progression visit-schedule and interval-observation audit; no biological claim",
        "synthetic": True,
        "n_unique_simulated_cohorts": int(
            len(seeds)
            * len(sizes)
            * len(event_probabilities)
            * len(molecular_hrs)
            * len(intervals)
            * len(MECHANISMS)
            * args.replicates_per_seed
        ),
        "n_route_evaluations": int(seed_frame.n_simulated_cohorts.sum()),
        "n_aggregate_route_cells": len(grid),
        "calibrated_observed_route_mechanisms": labels(calibrated_pairs),
        "strict_cell_flag_but_family_compatible": labels(strict_family_compatible),
        "invalid_observed_route_mechanisms": labels(invalid_pairs),
        "nonnull_scenarios_reaching_80pct": int(
            (threshold_frame.minimum_n_reaching_80pct != "not_reached").sum()
        ),
        "nonnull_scenarios": len(threshold_frame),
        "verdict": "VISIT_SCHEDULE_AND_ATTENDANCE_MUST_BE_AUDITED_BEFORE_PROGRESSION_INFERENCE",
        "boundary": "All values are seeded synthetic method behavior, not empirical MS progression, attendance, treatment, or biology.",
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    lines = [
        "# V54 Progression Visit-Schedule Robustness",
        "",
        "All outputs are seeded synthetic method behavior, not biological evidence.",
        "",
        f"The audit generated {summary['n_unique_simulated_cohorts']:,} unique cohorts and "
        f"{summary['n_route_evaluations']:,} route evaluations.",
        "",
        "| route | attendance | median null | maximum null | max-tail | verdict |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in calibration_frame.itertuples(index=False):
        if row.invalid_by_frozen_rule:
            verdict = "INVALID"
        elif row.strict_cell_flag:
            verdict = "STRICT CELL FLAG; FAMILY-COMPATIBLE"
        else:
            verdict = "calibrated"
        lines.append(
            f"| {row.analysis_route} | {row.attendance_mechanism} | "
            f"{row.median_null_probability:.3f} | {row.maximum_null_probability:.3f} | "
            f"{row.family_probability_maximum_at_least_observed:.3f} | {verdict} |"
        )
    lines.extend(
        [
            "",
            "Only observed route/attendance pairs passing the frozen strict calibration rule enter the power table. Oracles are diagnostics only. Sparse schedules and absent confirmation may lower ascertainment without creating type-I bias; informative attendance may instead invalidate the route. Neither is biological evidence.",
        ]
    )
    (args.output_dir / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
