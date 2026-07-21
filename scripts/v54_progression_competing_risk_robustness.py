#!/usr/bin/env python3
"""Simulate cause-specific progression inference under competing death."""

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
DEFAULT_OUT = ROOT / "analysis/v54_progression_competing_risk_robustness"
DEFAULT_SEEDS = [54931, 54932, 54933]
MECHANISMS = [
    "none",
    "independent",
    "score_dependent",
    "progression_risk_dependent",
    "joint_score_progression_risk",
]


def csv_numbers(value: str, cast: type) -> list[Any]:
    return [cast(item.strip()) for item in value.split(",") if item.strip()]


def death_targets(mechanism: str, targets: list[float]) -> list[float]:
    return [0.0] if mechanism == "none" else targets


def death_linear_predictor(
    mechanism: str, score: np.ndarray, frailty: np.ndarray
) -> np.ndarray:
    if mechanism in {"none", "independent"}:
        return np.zeros_like(score)
    if mechanism == "score_dependent":
        return 1.2 * score
    if mechanism == "progression_risk_dependent":
        return 1.2 * frailty
    if mechanism == "joint_score_progression_risk":
        return 0.6 * score + 0.6 * frailty + 1.8 * score * frailty
    raise ValueError(f"Unknown competing-risk mechanism: {mechanism}")


def simulate_cell(
    *,
    rng: np.random.Generator,
    n: int,
    event_probability: float,
    molecular_hr: float,
    death_probability: float,
    mechanism: str,
    replicates: int,
    reliability: float,
    missing_rate: float,
    alpha: float,
) -> dict[str, Any]:
    latent_score = rng.normal(size=(replicates, n))
    progression_frailty = rng.normal(size=(replicates, n))
    source = rng.random((replicates, n)) < expit(0.8 * latent_score)
    treatment = rng.random((replicates, n)) < expit(
        0.5 * source.astype(float) - 0.8 * latent_score
    )
    progression_multiplier = np.exp(
        np.log(molecular_hr) * latent_score
        + 0.7 * progression_frailty
        + np.log(1.6) * source
        + np.log(0.7) * treatment
    )
    progression_baseline = calibrate_scale(progression_multiplier, event_probability)
    progression_time = -np.log(np.clip(rng.random((replicates, n)), 1e-12, 1.0)) / (
        progression_baseline[:, None] * progression_multiplier
    )

    if mechanism == "none":
        death_time = np.full_like(progression_time, np.inf)
    else:
        death_multiplier = np.exp(
            death_linear_predictor(mechanism, latent_score, progression_frailty)
        )
        death_baseline = calibrate_scale(death_multiplier, death_probability)
        death_time = -np.log(np.clip(rng.random((replicates, n)), 1e-12, 1.0)) / (
            death_baseline[:, None] * death_multiplier
        )

    observed_time = np.minimum(np.minimum(progression_time, death_time), 1.0)
    progression_event = (progression_time <= death_time) & (progression_time <= 1.0)
    competing_death = (death_time < progression_time) & (death_time <= 1.0)
    observed_score = (
        np.sqrt(reliability) * latent_score
        + np.sqrt(1 - reliability) * rng.normal(size=latent_score.shape)
    )
    included = rng.random(latent_score.shape) >= missing_rate
    strata = 2 * source.astype(np.int8) + treatment.astype(np.int8)

    valid = 0
    positive = 0
    negative = 0
    z_values: list[float] = []
    one_steps: list[float] = []
    usable_values: list[int] = []
    event_values: list[int] = []
    death_values: list[int] = []
    for replicate in range(replicates):
        keep = included[replicate]
        usable = int(keep.sum())
        events = int(progression_event[replicate, keep].sum())
        deaths = int(competing_death[replicate, keep].sum())
        usable_values.append(usable)
        event_values.append(events)
        death_values.append(deaths)
        if usable < 20 or events < 10 or usable - events < 10:
            continue
        score = observed_score[replicate, keep]
        sd = float(np.std(score, ddof=1))
        if not np.isfinite(sd) or sd <= 0:
            continue
        score = (score - score.mean()) / sd
        z, p_value, one_step = cox_score_test(
            score,
            observed_time[replicate, keep],
            progression_event[replicate, keep],
            strata[replicate, keep],
        )
        if not np.isfinite(p_value):
            continue
        valid += 1
        z_values.append(z)
        one_steps.append(one_step)
        if p_value <= alpha and z > 0:
            positive += 1
        if p_value <= alpha and z < 0:
            negative += 1
    significant = positive + negative
    low, high = wilson(significant, replicates)
    return {
        "n_requested": n,
        "event_probability_before_competing_death": event_probability,
        "molecular_progression_hr_per_latent_sd": molecular_hr,
        "competing_death_probability": death_probability,
        "competing_event_mechanism": mechanism,
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
        "median_progression_events": float(np.median(event_values)),
        "median_competing_deaths": float(np.median(death_values)),
    }


def aggregate(seed_frame: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "n_requested",
        "event_probability_before_competing_death",
        "molecular_progression_hr_per_latent_sd",
        "competing_death_probability",
        "competing_event_mechanism",
    ]
    rows = []
    for values, group in seed_frame.groupby(keys, sort=True, dropna=False):
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
                "minimum_seed_probability": float(group.significant_probability.min()),
                "maximum_seed_probability": float(group.significant_probability.max()),
                "positive_call_probability": positive / total,
                "negative_call_probability": negative / total,
                "median_score_z_across_seeds": finite_median(group.median_score_z.to_numpy()),
                "median_one_step_log_hr_across_seeds": finite_median(group.median_one_step_log_hr.to_numpy()),
                "median_usable_n_across_seeds": float(group.median_usable_n.median()),
                "median_progression_events_across_seeds": float(group.median_progression_events.median()),
                "median_competing_deaths_across_seeds": float(group.median_competing_deaths.median()),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def calibration(grid: pd.DataFrame, alpha: float) -> pd.DataFrame:
    null = grid.loc[grid.molecular_progression_hr_per_latent_sd.eq(1.0)]
    rows = []
    for mechanism, group in null.groupby("competing_event_mechanism", sort=True):
        maximum = group.loc[group.significant_probability.idxmax()]
        count = int(maximum.significant_count)
        total = int(maximum.n_simulated_cohorts)
        single = float(binom.sf(count - 1, total, alpha))
        family_tail = float(1 - (1 - single) ** len(group))
        anti = bool((group.significant_probability_ci_low > alpha).any())
        rows.append(
            {
                "competing_event_mechanism": mechanism,
                "n_null_cells": len(group),
                "median_null_probability": float(group.significant_probability.median()),
                "maximum_null_probability": float(maximum.significant_probability),
                "maximum_count": count,
                "maximum_total": total,
                "maximum_ci_low": float(maximum.significant_probability_ci_low),
                "maximum_ci_high": float(maximum.significant_probability_ci_high),
                "family_probability_maximum_at_least_observed": family_tail,
                "anti_conservative_by_frozen_rule": anti,
                "maximum_positive_call_probability": float(group.positive_call_probability.max()),
                "maximum_negative_call_probability": float(group.negative_call_probability.max()),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-sizes", default="120,240,320")
    parser.add_argument("--event-probabilities", default="0.15,0.30")
    parser.add_argument("--molecular-hrs", default="1.0,1.7")
    parser.add_argument("--death-probabilities", default="0.10,0.25")
    parser.add_argument("--replicates-per-seed", type=int, default=400)
    parser.add_argument("--seeds", default=",".join(map(str, DEFAULT_SEEDS)))
    parser.add_argument("--reliability", type=float, default=0.70)
    parser.add_argument("--missing-rate", type=float, default=0.10)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    sizes = csv_numbers(args.sample_sizes, int)
    event_probabilities = csv_numbers(args.event_probabilities, float)
    molecular_hrs = csv_numbers(args.molecular_hrs, float)
    death_probabilities = csv_numbers(args.death_probabilities, float)
    seeds = csv_numbers(args.seeds, int)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    config = {
        "synthetic": True,
        "sample_sizes": sizes,
        "event_probabilities_before_competing_death": event_probabilities,
        "molecular_progression_hrs_per_latent_sd": molecular_hrs,
        "competing_death_probabilities": death_probabilities,
        "competing_event_mechanisms": MECHANISMS,
        "progression_frailty_log_hr": 0.7,
        "death_mechanism_coefficients": {
            "score_dependent": {"score": 1.2},
            "progression_risk_dependent": {"frailty": 1.2},
            "joint_score_progression_risk": {"score": 0.6, "frailty": 0.6, "interaction": 1.8},
        },
        "replicates_per_seed": args.replicates_per_seed,
        "seeds": seeds,
        "measurement_reliability": args.reliability,
        "missing_rate": args.missing_rate,
        "alpha": args.alpha,
        "boundary": "Seeded synthetic method behavior only; not empirical MS progression, death, or biology.",
    }
    (args.output_dir / "simulation_config.json").write_text(json.dumps(config, indent=2) + "\n")

    seed_rows = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for n in sizes:
            for event_probability in event_probabilities:
                for molecular_hr in molecular_hrs:
                    for mechanism in MECHANISMS:
                        for death_probability in death_targets(mechanism, death_probabilities):
                            row = simulate_cell(
                                rng=rng,
                                n=n,
                                event_probability=event_probability,
                                molecular_hr=molecular_hr,
                                death_probability=death_probability,
                                mechanism=mechanism,
                                replicates=args.replicates_per_seed,
                                reliability=args.reliability,
                                missing_rate=args.missing_rate,
                                alpha=args.alpha,
                            )
                            seed_rows.append({"seed": seed, **row})
    seed_frame = pd.DataFrame(seed_rows)
    seed_frame.to_csv(args.output_dir / "seed_results.tsv", sep="\t", index=False)
    grid = aggregate(seed_frame)
    grid.to_csv(args.output_dir / "competing_risk_grid.tsv", sep="\t", index=False)
    calibration_frame = calibration(grid, args.alpha)
    calibration_frame.to_csv(args.output_dir / "null_calibration_by_mechanism.tsv", sep="\t", index=False)
    calibrated = set(
        calibration_frame.loc[
            ~calibration_frame.anti_conservative_by_frozen_rule,
            "competing_event_mechanism",
        ]
    )
    strict_cell_flag_family_compatible = set(
        calibration_frame.loc[
            calibration_frame.anti_conservative_by_frozen_rule
            & calibration_frame.family_probability_maximum_at_least_observed.ge(0.05),
            "competing_event_mechanism",
        ]
    )
    invalid = set(
        calibration_frame.loc[
            calibration_frame.anti_conservative_by_frozen_rule
            & calibration_frame.family_probability_maximum_at_least_observed.lt(0.05),
            "competing_event_mechanism",
        ]
    )
    nonnull = grid.loc[
        grid.molecular_progression_hr_per_latent_sd.gt(1.0)
        & grid.competing_event_mechanism.isin(calibrated)
    ]
    scenario_keys = [
        "event_probability_before_competing_death",
        "molecular_progression_hr_per_latent_sd",
        "competing_death_probability",
        "competing_event_mechanism",
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
        row["minimum_n_reaching_80pct"] = "not_reached" if reached.empty else int(reached.iloc[0].n_requested)
        row["power_at_n320"] = float(ordered.iloc[-1].positive_call_probability)
        thresholds.append(row)
    threshold_frame = pd.DataFrame(thresholds)
    threshold_frame.to_csv(args.output_dir / "calibrated_power_thresholds.tsv", sep="\t", index=False)

    summary = {
        "purpose": "Synthetic cause-specific progression Cox audit under competing death; no biological claim",
        "synthetic": True,
        "n_unique_simulated_cohorts": int(seed_frame.n_simulated_cohorts.sum()),
        "n_aggregate_cells": len(grid),
        "calibrated_competing_event_mechanisms": sorted(calibrated),
        "strict_cell_flag_but_family_compatible_mechanisms": sorted(strict_cell_flag_family_compatible),
        "invalid_competing_event_mechanisms": sorted(invalid),
        "nonnull_scenarios_reaching_80pct": int((threshold_frame.minimum_n_reaching_80pct != "not_reached").sum()),
        "nonnull_scenarios": len(threshold_frame),
        "verdict": "CAUSE_SPECIFIC_ROUTE_REQUIRES_COMPETING_EVENT_DEPENDENCE_AUDIT",
        "boundary": "All values are seeded synthetic method behavior, not empirical MS progression effects, mortality, or biology.",
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "# V54 Progression Competing-Risk Robustness",
        "",
        "All outputs are seeded synthetic method behavior, not biological evidence.",
        "",
        f"The audit generated {summary['n_unique_simulated_cohorts']:,} unique cohorts.",
        "",
        "| mechanism | null cells | median | maximum | Wilson CI | max-tail | verdict |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in calibration_frame.itertuples(index=False):
        if not row.anti_conservative_by_frozen_rule:
            status = "calibrated"
        elif row.family_probability_maximum_at_least_observed >= 0.05:
            status = "STRICT CELL FLAG; FAMILY-COMPATIBLE"
        else:
            status = "INVALID"
        lines.append(
            f"| {row.competing_event_mechanism} | {row.n_null_cells} | {row.median_null_probability:.3f} | "
            f"{row.maximum_null_probability:.3f} | {row.maximum_ci_low:.3f}-{row.maximum_ci_high:.3f} | "
            f"{row.family_probability_maximum_at_least_observed:.3f} | "
            f"{status} |"
        )
    lines.extend(
        [
            "",
            "Only mechanisms passing both frozen calibration criteria enter `calibrated_power_thresholds.tsv`. A mechanism may fail the strict single-cell Wilson rule while remaining compatible with the predeclared family-maximum reference; that is reported as inconclusive and excluded from power, not equated with directional invalidity. A competing event is not automatically bias, but joint dependence on molecular state and latent progression risk can invalidate ordinary death censoring.",
        ]
    )
    (args.output_dir / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
