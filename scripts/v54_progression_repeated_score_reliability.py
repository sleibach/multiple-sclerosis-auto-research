#!/usr/bin/env python3
"""Simulate repeated molecular-score measurement for progression studies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.special import expit
from scipy.stats import binom

from v54_progression_event_time_assumption_robustness import (
    calibrate_scale,
    cox_score_test,
    finite_median,
    wilson,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_repeated_score_reliability"
DEFAULT_SEEDS = [54951, 54952, 54953]
MEASUREMENT_PLANS = [
    (1, 0.0),
    (2, 0.0),
    (2, 0.5),
    (3, 0.0),
    (3, 0.5),
]


def csv_numbers(value: str, cast: type) -> list[Any]:
    return [cast(item.strip()) for item in value.split(",") if item.strip()]


def simulate_cell(
    *,
    rng: np.random.Generator,
    n: int,
    event_probability: float,
    molecular_hr: float,
    single_reliability: float,
    repeats: int,
    error_correlation: float,
    replicates: int,
    measurement_missing_rate: float,
    alpha: float,
) -> dict[str, Any]:
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
    baseline = calibrate_scale(multiplier, event_probability)
    event_time = -np.log(
        np.clip(rng.random((replicates, n)), 1e-12, 1.0)
    ) / (baseline[:, None] * multiplier)
    event = event_time <= 1.0
    observed_time = np.minimum(event_time, 1.0)

    shared_error = rng.normal(size=(replicates, n, 1))
    independent_error = rng.normal(size=(replicates, n, repeats))
    measurement_error = (
        np.sqrt(error_correlation) * shared_error
        + np.sqrt(1 - error_correlation) * independent_error
    )
    measurements = (
        np.sqrt(single_reliability) * latent_score[:, :, None]
        + np.sqrt(1 - single_reliability) * measurement_error
    )
    observed_measurement = (
        rng.random(measurements.shape) >= measurement_missing_rate
    )
    available_count = observed_measurement.sum(axis=2)
    measurement_sum = np.where(observed_measurement, measurements, 0.0).sum(axis=2)
    averaged_score = np.divide(
        measurement_sum,
        available_count,
        out=np.full_like(measurement_sum, np.nan),
        where=available_count > 0,
    )
    included = available_count > 0
    strata = 2 * source.astype(np.int8) + treatment.astype(np.int8)

    valid = positive = negative = 0
    z_values: list[float] = []
    one_steps: list[float] = []
    usable_values: list[int] = []
    event_values: list[int] = []
    repeat_values: list[float] = []
    reliability_values: list[float] = []
    for replicate in range(replicates):
        keep = included[replicate]
        usable = int(keep.sum())
        events = int(event[replicate, keep].sum())
        usable_values.append(usable)
        event_values.append(events)
        repeat_values.append(float(available_count[replicate, keep].mean()))
        if usable >= 3:
            correlation = np.corrcoef(
                averaged_score[replicate, keep], latent_score[replicate, keep]
            )[0, 1]
            reliability_values.append(float(correlation**2))
        if usable < 20 or events < 10 or usable - events < 10:
            continue
        score = averaged_score[replicate, keep]
        sd = float(np.std(score, ddof=1))
        if not np.isfinite(sd) or sd <= 0:
            continue
        score = (score - score.mean()) / sd
        z_value, p_value, one_step = cox_score_test(
            score,
            observed_time[replicate, keep],
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
        "n_requested": n,
        "latent_event_probability": event_probability,
        "molecular_progression_hr_per_latent_sd": molecular_hr,
        "single_measurement_reliability": single_reliability,
        "planned_measurements": repeats,
        "measurement_error_correlation": error_correlation,
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
        "median_events": float(np.median(event_values)),
        "median_measurements_available": float(np.median(repeat_values)),
        "median_empirical_reliability": float(np.median(reliability_values)),
    }


def aggregate(seed_frame: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "n_requested",
        "latent_event_probability",
        "molecular_progression_hr_per_latent_sd",
        "single_measurement_reliability",
        "planned_measurements",
        "measurement_error_correlation",
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
                "median_events_across_seeds": float(group.median_events.median()),
                "median_measurements_available_across_seeds": float(
                    group.median_measurements_available.median()
                ),
                "median_empirical_reliability_across_seeds": float(
                    group.median_empirical_reliability.median()
                ),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def plan_label(repeats: int, correlation: float) -> str:
    return f"k{repeats}|error_corr_{correlation:.1f}"


def calibration(grid: pd.DataFrame, alpha: float) -> pd.DataFrame:
    null = grid.loc[grid.molecular_progression_hr_per_latent_sd.eq(1.0)]
    rows = []
    keys = [
        "single_measurement_reliability",
        "planned_measurements",
        "measurement_error_correlation",
    ]
    for values, group in null.groupby(keys, sort=True):
        reliability, repeats, correlation = values
        maximum = group.loc[group.significant_probability.idxmax()]
        count = int(maximum.significant_count)
        total = int(maximum.n_simulated_cohorts)
        single_tail = float(binom.sf(count - 1, total, alpha))
        family_tail = float(1 - (1 - single_tail) ** len(group))
        strict_flag = bool((group.significant_probability_ci_low > alpha).any())
        rows.append(
            {
                "single_measurement_reliability": reliability,
                "planned_measurements": repeats,
                "measurement_error_correlation": correlation,
                "plan": plan_label(int(repeats), float(correlation)),
                "n_null_cells": len(group),
                "median_null_probability": float(group.significant_probability.median()),
                "maximum_null_probability": float(maximum.significant_probability),
                "maximum_count": count,
                "maximum_total": total,
                "maximum_ci_low": float(maximum.significant_probability_ci_low),
                "maximum_ci_high": float(maximum.significant_probability_ci_high),
                "family_probability_maximum_at_least_observed": family_tail,
                "strict_cell_flag": strict_flag,
                "invalid_by_frozen_rule": strict_flag and family_tail < 0.05,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-sizes", default="120,240,320")
    parser.add_argument("--event-probabilities", default="0.15,0.30")
    parser.add_argument("--molecular-hrs", default="1.0,1.5,1.7")
    parser.add_argument("--single-reliabilities", default="0.40,0.70")
    parser.add_argument("--replicates-per-seed", type=int, default=400)
    parser.add_argument("--seeds", default=",".join(map(str, DEFAULT_SEEDS)))
    parser.add_argument("--measurement-missing-rate", type=float, default=0.10)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    sizes = csv_numbers(args.sample_sizes, int)
    event_probabilities = csv_numbers(args.event_probabilities, float)
    molecular_hrs = csv_numbers(args.molecular_hrs, float)
    reliabilities = csv_numbers(args.single_reliabilities, float)
    seeds = csv_numbers(args.seeds, int)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    config = {
        "synthetic": True,
        "sample_sizes": sizes,
        "latent_event_probabilities": event_probabilities,
        "molecular_progression_hrs_per_latent_sd": molecular_hrs,
        "single_measurement_reliabilities": reliabilities,
        "measurement_plans": [
            {"planned_measurements": k, "measurement_error_correlation": rho}
            for k, rho in MEASUREMENT_PLANS
        ],
        "measurement_missing_rate": args.measurement_missing_rate,
        "replicates_per_seed": args.replicates_per_seed,
        "seeds": seeds,
        "alpha": args.alpha,
        "material_absolute_power_gain": 0.10,
        "boundary": "Seeded synthetic method behavior only; not empirical MS progression, molecular stability, or biology.",
    }
    (args.output_dir / "simulation_config.json").write_text(
        json.dumps(config, indent=2) + "\n"
    )

    rows = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for n in sizes:
            for event_probability in event_probabilities:
                for molecular_hr in molecular_hrs:
                    for reliability in reliabilities:
                        for repeats, correlation in MEASUREMENT_PLANS:
                            rows.append(
                                {
                                    "seed": seed,
                                    **simulate_cell(
                                        rng=rng,
                                        n=n,
                                        event_probability=event_probability,
                                        molecular_hr=molecular_hr,
                                        single_reliability=reliability,
                                        repeats=repeats,
                                        error_correlation=correlation,
                                        replicates=args.replicates_per_seed,
                                        measurement_missing_rate=args.measurement_missing_rate,
                                        alpha=args.alpha,
                                    ),
                                }
                            )
    seed_frame = pd.DataFrame(rows)
    seed_frame.to_csv(args.output_dir / "seed_results.tsv", sep="\t", index=False)
    grid = aggregate(seed_frame)
    grid.to_csv(args.output_dir / "reliability_power_grid.tsv", sep="\t", index=False)
    calibration_frame = calibration(grid, args.alpha)
    calibration_frame.to_csv(
        args.output_dir / "null_calibration_by_measurement_plan.tsv",
        sep="\t",
        index=False,
    )
    calibration_lookup = {
        (row.single_measurement_reliability, row.planned_measurements, row.measurement_error_correlation): not row.strict_cell_flag
        for row in calibration_frame.itertuples(index=False)
    }

    nonnull = grid.loc[grid.molecular_progression_hr_per_latent_sd.gt(1.0)].copy()
    baseline = nonnull.loc[nonnull.planned_measurements.eq(1)].copy()
    baseline_keys = [
        "n_requested",
        "latent_event_probability",
        "molecular_progression_hr_per_latent_sd",
        "single_measurement_reliability",
    ]
    baseline = baseline[baseline_keys + [
        "significant_probability",
        "median_empirical_reliability_across_seeds",
    ]].rename(
        columns={
            "significant_probability": "single_measurement_power",
            "median_empirical_reliability_across_seeds": "single_measurement_empirical_reliability",
        }
    )
    gains = nonnull.loc[nonnull.planned_measurements.gt(1)].merge(
        baseline, on=baseline_keys, how="left", validate="many_to_one"
    )
    gains["aggregate_power_gain"] = (
        gains.significant_probability - gains.single_measurement_power
    )
    gains["empirical_reliability_gain"] = (
        gains.median_empirical_reliability_across_seeds
        - gains.single_measurement_empirical_reliability
    )

    seed_nonnull = seed_frame.loc[
        seed_frame.molecular_progression_hr_per_latent_sd.gt(1.0)
    ].copy()
    seed_baseline = seed_nonnull.loc[
        seed_nonnull.planned_measurements.eq(1)
    ][["seed", *baseline_keys, "significant_probability"]].rename(
        columns={"significant_probability": "seed_single_power"}
    )
    seed_gains = seed_nonnull.loc[
        seed_nonnull.planned_measurements.gt(1)
    ].merge(
        seed_baseline,
        on=["seed", *baseline_keys],
        how="left",
        validate="many_to_one",
    )
    seed_gains["seed_power_gain"] = (
        seed_gains.significant_probability - seed_gains.seed_single_power
    )
    seed_gain_minimum = seed_gains.groupby(
        [*baseline_keys, "planned_measurements", "measurement_error_correlation"],
        as_index=False,
    ).seed_power_gain.min().rename(
        columns={"seed_power_gain": "minimum_seed_power_gain"}
    )
    gains = gains.merge(
        seed_gain_minimum,
        on=[*baseline_keys, "planned_measurements", "measurement_error_correlation"],
        how="left",
        validate="one_to_one",
    )
    gains["null_calibrated"] = gains.apply(
        lambda row: calibration_lookup[
            (
                row.single_measurement_reliability,
                row.planned_measurements,
                row.measurement_error_correlation,
            )
        ],
        axis=1,
    )
    gains["materially_useful"] = (
        gains.null_calibrated
        & gains.aggregate_power_gain.ge(0.10)
        & gains.minimum_seed_power_gain.ge(0.10)
    )
    gain_columns = [
        *baseline_keys,
        "planned_measurements",
        "measurement_error_correlation",
        "median_empirical_reliability_across_seeds",
        "single_measurement_empirical_reliability",
        "empirical_reliability_gain",
        "significant_probability",
        "single_measurement_power",
        "aggregate_power_gain",
        "minimum_seed_power_gain",
        "null_calibrated",
        "materially_useful",
    ]
    gains[gain_columns].to_csv(
        args.output_dir / "repeat_measurement_power_gains.tsv",
        sep="\t",
        index=False,
    )

    thresholds = []
    for values, group in nonnull.groupby(
        [
            "latent_event_probability",
            "molecular_progression_hr_per_latent_sd",
            "single_measurement_reliability",
            "planned_measurements",
            "measurement_error_correlation",
        ],
        sort=True,
    ):
        reliability = values[2]
        repeats = values[3]
        correlation = values[4]
        calibrated = calibration_lookup[(reliability, repeats, correlation)]
        ordered = group.sort_values("n_requested")
        reached = ordered.loc[
            calibrated
            & ordered.significant_probability.ge(0.80)
            & ordered.minimum_seed_probability.ge(0.75)
            & ordered.positive_call_probability.eq(ordered.significant_probability)
        ]
        row = dict(
            zip(
                [
                    "latent_event_probability",
                    "molecular_progression_hr_per_latent_sd",
                    "single_measurement_reliability",
                    "planned_measurements",
                    "measurement_error_correlation",
                ],
                values,
            )
        )
        row["null_calibrated"] = calibrated
        row["minimum_n_reaching_80pct"] = (
            "not_reached" if reached.empty else int(reached.iloc[0].n_requested)
        )
        row["power_at_n320"] = float(ordered.iloc[-1].positive_call_probability)
        row["empirical_reliability_at_n320"] = float(
            ordered.iloc[-1].median_empirical_reliability_across_seeds
        )
        thresholds.append(row)
    threshold_frame = pd.DataFrame(thresholds)
    threshold_frame.to_csv(
        args.output_dir / "measurement_plan_power_thresholds.tsv",
        sep="\t",
        index=False,
    )

    def labels(frame: pd.DataFrame) -> list[str]:
        return sorted(
            f"reliability_{row.single_measurement_reliability:.1f}|{row.plan}"
            for row in frame.itertuples(index=False)
        )

    strict = calibration_frame.loc[
        calibration_frame.strict_cell_flag & ~calibration_frame.invalid_by_frozen_rule
    ]
    invalid = calibration_frame.loc[calibration_frame.invalid_by_frozen_rule]
    calibrated = calibration_frame.loc[~calibration_frame.strict_cell_flag]
    material = gains.loc[gains.materially_useful]
    summary = {
        "purpose": "Synthetic repeated molecular-score reliability and power audit; no biological claim",
        "synthetic": True,
        "n_unique_simulated_cohorts": int(seed_frame.n_simulated_cohorts.sum()),
        "n_aggregate_cells": len(grid),
        "calibrated_measurement_plans": labels(calibrated),
        "strict_cell_flag_but_family_compatible_plans": labels(strict),
        "invalid_measurement_plans": labels(invalid),
        "n_repeat_gain_cells": len(gains),
        "n_materially_useful_repeat_cells": len(material),
        "materially_useful_repeat_plans": sorted(
            {
                f"reliability_{row.single_measurement_reliability:.1f}|{plan_label(int(row.planned_measurements), float(row.measurement_error_correlation))}"
                for row in material.itertuples(index=False)
            }
        ),
        "verdict": "REPEATS_HELP_ONLY_WHEN_ERROR_IS_SUFFICIENTLY_INDEPENDENT_AND_BASE_RELIABILITY_IS_LOW",
        "boundary": "All values are seeded synthetic method behavior, not empirical MS progression, score stability, treatment, or biology.",
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    (args.output_dir / "REPORT.md").write_text(
        "# V54 Repeated Progression Molecular-Score Reliability\n\n"
        "All outputs are seeded synthetic method behavior, not biological evidence.\n\n"
        f"The audit generated {summary['n_unique_simulated_cohorts']:,} unique cohorts. "
        f"{summary['n_materially_useful_repeat_cells']}/{summary['n_repeat_gain_cells']} "
        "repeat-plan cells meet the frozen absolute and every-seed power-gain rule. "
        "Effective reliability alone is not a utility claim; see the committed gain and threshold tables.\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
