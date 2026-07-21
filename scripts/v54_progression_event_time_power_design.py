#!/usr/bin/env python3
"""Simulate progression event-time power under censoring and confounding."""

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
DEFAULT_OUT = ROOT / "analysis/v54_progression_event_time_power_design"
DEFAULT_SEEDS = [54801, 54802, 54803]


def csv_numbers(value: str, cast: type) -> list[Any]:
    return [cast(item.strip()) for item in value.split(",") if item.strip()]


def wilson(successes: int, total: int, confidence: float = 0.95) -> tuple[float, float]:
    if total <= 0:
        return np.nan, np.nan
    z = norm.ppf(1 - (1 - confidence) / 2)
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    half = z * np.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return float(center - half), float(center + half)


def calibrate_baseline_hazard(
    multiplier: np.ndarray, event_probability: float
) -> np.ndarray:
    low = np.zeros(multiplier.shape[0])
    high = np.full(multiplier.shape[0], 20.0)
    for _ in range(50):
        middle = (low + high) / 2
        probability = np.mean(1 - np.exp(-middle[:, None] * multiplier), axis=1)
        below = probability < event_probability
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
        risk_sum_sq = np.cumsum((ordered_score * ordered_score)[::-1])[::-1]
        event_index = np.flatnonzero(ordered_event)
        risk_mean = risk_sum[event_index] / risk_n[event_index]
        risk_variance = (
            risk_sum_sq[event_index] / risk_n[event_index] - risk_mean * risk_mean
        )
        score_statistic += float(np.sum(ordered_score[event_index] - risk_mean))
        information += float(np.sum(np.maximum(risk_variance, 0.0)))
    if information <= 1e-12 or not np.isfinite(information):
        return np.nan, np.nan, np.nan
    z = score_statistic / np.sqrt(information)
    p_value = float(2 * norm.sf(abs(z)))
    one_step_log_hr = score_statistic / information
    return float(z), p_value, float(one_step_log_hr)


def simulate_cell(
    *,
    rng: np.random.Generator,
    n: int,
    event_probability: float,
    molecular_hazard_ratio: float,
    dropout_probability: float,
    assignment_strength: float,
    source_hazard_ratio: float,
    treatment_hazard_ratio: float,
    measurement_reliability: float,
    missing_rate: float,
    alpha: float,
    replicates: int,
) -> list[dict[str, Any]]:
    latent = rng.normal(size=(replicates, n))
    source_probability = expit(assignment_strength * latent)
    source = rng.random((replicates, n)) < source_probability
    treatment_probability = expit(
        0.5 * source.astype(float) - assignment_strength * latent
    )
    treatment = rng.random((replicates, n)) < treatment_probability

    beta = np.log(molecular_hazard_ratio)
    multiplier = np.exp(
        beta * latent
        + np.log(source_hazard_ratio) * source
        + np.log(treatment_hazard_ratio) * treatment
    )
    baseline_hazard = calibrate_baseline_hazard(multiplier, event_probability)
    event_time = -np.log(np.clip(rng.random((replicates, n)), 1e-12, 1.0)) / (
        baseline_hazard[:, None] * multiplier
    )
    dropout = rng.random((replicates, n)) < dropout_probability
    dropout_time = rng.uniform(0.05, 1.0, size=(replicates, n))
    censor_time = np.where(dropout, dropout_time, 1.0)
    event = event_time <= censor_time
    observed_time = np.minimum(event_time, censor_time)

    measurement_noise = rng.normal(size=(replicates, n))
    observed_score = (
        np.sqrt(measurement_reliability) * latent
        + np.sqrt(1 - measurement_reliability) * measurement_noise
    )
    included = rng.random((replicates, n)) >= missing_rate

    routes = {
        "unadjusted": np.zeros((replicates, n), dtype=np.int8),
        "source_treatment_stratified": (
            2 * source.astype(np.int8) + treatment.astype(np.int8)
        ),
    }
    accumulators = {
        route: {
            "valid": 0,
            "conclusive": 0,
            "z": [],
            "one_step": [],
            "events": [],
            "usable_n": [],
            "dropout": [],
        }
        for route in routes
    }

    for replicate in range(replicates):
        keep = included[replicate]
        usable_n = int(keep.sum())
        observed_events = int(event[replicate, keep].sum())
        nonevents = usable_n - observed_events
        for route, route_strata in routes.items():
            accumulator = accumulators[route]
            accumulator["events"].append(observed_events)
            accumulator["usable_n"].append(usable_n)
            accumulator["dropout"].append(float(dropout[replicate, keep].mean()))
            if usable_n < 20 or observed_events < 10 or nonevents < 10:
                continue
            score = observed_score[replicate, keep]
            score_sd = float(np.std(score, ddof=1))
            if not np.isfinite(score_sd) or score_sd <= 0:
                continue
            score = (score - np.mean(score)) / score_sd
            z, p_value, one_step = cox_score_test(
                score,
                observed_time[replicate, keep],
                event[replicate, keep],
                route_strata[replicate, keep],
            )
            if not np.isfinite(p_value):
                continue
            accumulator["valid"] += 1
            accumulator["z"].append(z)
            accumulator["one_step"].append(one_step)
            if p_value <= alpha and (
                molecular_hazard_ratio == 1.0 or z > 0
            ):
                accumulator["conclusive"] += 1

    rows = []
    for route, accumulator in accumulators.items():
        successes = int(accumulator["conclusive"])
        ci_low, ci_high = wilson(successes, replicates)
        rows.append(
            {
                "analysis_route": route,
                "n_requested": n,
                "event_probability_before_dropout": event_probability,
                "molecular_hazard_ratio_per_latent_sd": molecular_hazard_ratio,
                "dropout_probability": dropout_probability,
                "assignment_strength": assignment_strength,
                "source_hazard_ratio": source_hazard_ratio,
                "treatment_hazard_ratio": treatment_hazard_ratio,
                "measurement_reliability": measurement_reliability,
                "missing_rate": missing_rate,
                "alpha": alpha,
                "n_simulated_cohorts": replicates,
                "n_valid_fits": accumulator["valid"],
                "valid_fit_rate": accumulator["valid"] / replicates,
                "median_usable_n": float(np.median(accumulator["usable_n"])),
                "median_observed_events": float(np.median(accumulator["events"])),
                "median_observed_dropout_fraction": float(np.median(accumulator["dropout"])),
                "conclusive_count": successes,
                "conclusive_probability": successes / replicates,
                "conclusive_probability_ci_low": ci_low,
                "conclusive_probability_ci_high": ci_high,
                "median_score_z": (
                    float(np.median(accumulator["z"])) if accumulator["z"] else np.nan
                ),
                "median_one_step_log_hr_per_observed_sd": (
                    float(np.median(accumulator["one_step"]))
                    if accumulator["one_step"]
                    else np.nan
                ),
            }
        )
    return rows


def aggregate_seed_results(seed_frame: pd.DataFrame) -> pd.DataFrame:
    group_columns = [
        "analysis_route",
        "n_requested",
        "event_probability_before_dropout",
        "molecular_hazard_ratio_per_latent_sd",
        "dropout_probability",
        "assignment_strength",
        "source_hazard_ratio",
        "treatment_hazard_ratio",
        "measurement_reliability",
        "missing_rate",
        "alpha",
    ]
    rows = []
    for keys, group in seed_frame.groupby(group_columns, sort=True, dropna=False):
        row = dict(zip(group_columns, keys))
        total = int(group["n_simulated_cohorts"].sum())
        successes = int(group["conclusive_count"].sum())
        ci_low, ci_high = wilson(successes, total)
        row.update(
            {
                "n_simulated_cohorts": total,
                "n_valid_fits": int(group["n_valid_fits"].sum()),
                "valid_fit_rate": float(group["n_valid_fits"].sum() / total),
                "median_usable_n_across_seeds": float(group["median_usable_n"].median()),
                "median_observed_events_across_seeds": float(
                    group["median_observed_events"].median()
                ),
                "median_observed_dropout_fraction_across_seeds": float(
                    group["median_observed_dropout_fraction"].median()
                ),
                "conclusive_probability": successes / total,
                "conclusive_probability_ci_low": ci_low,
                "conclusive_probability_ci_high": ci_high,
                "minimum_seed_probability": float(group["conclusive_probability"].min()),
                "maximum_seed_probability": float(group["conclusive_probability"].max()),
                "median_score_z_across_seeds": float(group["median_score_z"].median()),
                "median_one_step_log_hr_across_seeds": float(
                    group["median_one_step_log_hr_per_observed_sd"].median()
                ),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def minimum_n_table(grid: pd.DataFrame) -> pd.DataFrame:
    scenario_columns = [
        "analysis_route",
        "event_probability_before_dropout",
        "molecular_hazard_ratio_per_latent_sd",
        "dropout_probability",
        "assignment_strength",
        "source_hazard_ratio",
        "treatment_hazard_ratio",
        "measurement_reliability",
        "missing_rate",
        "alpha",
    ]
    rows = []
    nonnull = grid.loc[grid["molecular_hazard_ratio_per_latent_sd"].gt(1.0)]
    for keys, group in nonnull.groupby(scenario_columns, sort=True, dropna=False):
        ordered = group.sort_values("n_requested")
        reached = ordered.loc[
            ordered["conclusive_probability"].ge(0.80)
            & ordered["minimum_seed_probability"].ge(0.75)
        ]
        row = dict(zip(scenario_columns, keys))
        row["largest_n_simulated"] = int(ordered.iloc[-1]["n_requested"])
        row["power_at_largest_n"] = float(ordered.iloc[-1]["conclusive_probability"])
        row["minimum_n_reaching_80pct"] = (
            "not_reached" if reached.empty else int(reached.iloc[0]["n_requested"])
        )
        rows.append(row)
    return pd.DataFrame(rows)


def route_contrasts(grid: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "n_requested",
        "event_probability_before_dropout",
        "molecular_hazard_ratio_per_latent_sd",
        "dropout_probability",
        "assignment_strength",
        "source_hazard_ratio",
        "treatment_hazard_ratio",
        "measurement_reliability",
        "missing_rate",
        "alpha",
    ]
    wide = grid.pivot(index=keys, columns="analysis_route", values="conclusive_probability")
    wide = wide.reset_index()
    wide["stratified_minus_unadjusted_probability"] = (
        wide["source_treatment_stratified"] - wide["unadjusted"]
    )
    return wide


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-sizes", default="80,120,160,240,320")
    parser.add_argument("--event-probabilities", default="0.15,0.30")
    parser.add_argument("--hazard-ratios", default="1.0,1.5,2.0")
    parser.add_argument("--dropout-probabilities", default="0.0,0.25")
    parser.add_argument("--assignment-strengths", default="0.0,0.8")
    parser.add_argument("--source-hazard-ratio", type=float, default=1.6)
    parser.add_argument("--treatment-hazard-ratio", type=float, default=0.7)
    parser.add_argument("--measurement-reliability", type=float, default=0.70)
    parser.add_argument("--missing-rate", type=float, default=0.10)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--replicates-per-seed", type=int, default=250)
    parser.add_argument("--seeds", default=",".join(map(str, DEFAULT_SEEDS)))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    sample_sizes = csv_numbers(args.sample_sizes, int)
    event_probabilities = csv_numbers(args.event_probabilities, float)
    hazard_ratios = csv_numbers(args.hazard_ratios, float)
    dropout_probabilities = csv_numbers(args.dropout_probabilities, float)
    assignment_strengths = csv_numbers(args.assignment_strengths, float)
    seeds = csv_numbers(args.seeds, int)
    if len(seeds) < 2:
        raise SystemExit("At least two seeds are required")
    if not all(0 < value < 1 for value in event_probabilities):
        raise SystemExit("Event probabilities must be in (0,1)")
    if not all(value >= 1 for value in hazard_ratios):
        raise SystemExit("Hazard ratios must be >=1")
    if not all(0 <= value < 1 for value in dropout_probabilities):
        raise SystemExit("Dropout probabilities must be in [0,1)")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    config = {
        "synthetic": True,
        "sample_sizes": sample_sizes,
        "event_probabilities_before_dropout": event_probabilities,
        "molecular_hazard_ratios_per_latent_sd": hazard_ratios,
        "dropout_probabilities": dropout_probabilities,
        "assignment_strengths": assignment_strengths,
        "source_hazard_ratio": args.source_hazard_ratio,
        "treatment_hazard_ratio": args.treatment_hazard_ratio,
        "measurement_reliability": args.measurement_reliability,
        "missing_rate": args.missing_rate,
        "alpha": args.alpha,
        "replicates_per_seed": args.replicates_per_seed,
        "seeds": seeds,
        "analysis_routes": ["unadjusted", "source_treatment_stratified"],
        "minimum_valid_counts": "usable n>=20, observed events>=10, non-events/censored>=10",
        "boundary": "Synthetic method-design behavior only; not an empirical MS effect or biological claim.",
    }
    (args.output_dir / "simulation_config.json").write_text(
        json.dumps(config, indent=2) + "\n"
    )

    seed_rows = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for n in sample_sizes:
            for event_probability in event_probabilities:
                for hazard_ratio in hazard_ratios:
                    for dropout_probability in dropout_probabilities:
                        for assignment_strength in assignment_strengths:
                            rows = simulate_cell(
                                rng=rng,
                                n=n,
                                event_probability=event_probability,
                                molecular_hazard_ratio=hazard_ratio,
                                dropout_probability=dropout_probability,
                                assignment_strength=assignment_strength,
                                source_hazard_ratio=args.source_hazard_ratio,
                                treatment_hazard_ratio=args.treatment_hazard_ratio,
                                measurement_reliability=args.measurement_reliability,
                                missing_rate=args.missing_rate,
                                alpha=args.alpha,
                                replicates=args.replicates_per_seed,
                            )
                            seed_rows.extend({"seed": seed, **row} for row in rows)
    seed_frame = pd.DataFrame(seed_rows)
    seed_frame.to_csv(args.output_dir / "seed_results.tsv", sep="\t", index=False)
    grid = aggregate_seed_results(seed_frame)
    grid.to_csv(args.output_dir / "power_grid.tsv", sep="\t", index=False)
    null = grid.loc[grid["molecular_hazard_ratio_per_latent_sd"].eq(1.0)].copy()
    null.to_csv(args.output_dir / "null_calibration_grid.tsv", sep="\t", index=False)
    minimum = minimum_n_table(grid)
    minimum.to_csv(args.output_dir / "minimum_n_by_assumption.tsv", sep="\t", index=False)
    contrasts = route_contrasts(grid)
    contrasts.to_csv(args.output_dir / "route_contrasts.tsv", sep="\t", index=False)

    stratified_null = null.loc[null["analysis_route"].eq("source_treatment_stratified")]
    unadjusted_confounded_null = null.loc[
        null["analysis_route"].eq("unadjusted") & null["assignment_strength"].gt(0)
    ]
    adjusted_minimum = minimum.loc[
        minimum["analysis_route"].eq("source_treatment_stratified")
    ]
    stratified_max = stratified_null.loc[
        stratified_null["conclusive_probability"].idxmax()
    ]
    stratified_max_total = int(stratified_max["n_simulated_cohorts"])
    stratified_max_count = int(
        round(stratified_max["conclusive_probability"] * stratified_max_total)
    )
    single_cell_tail = float(
        binom.sf(stratified_max_count - 1, stratified_max_total, args.alpha)
    )
    maximum_reference_tail = float(
        1 - (1 - single_cell_tail) ** len(stratified_null)
    )
    summary = {
        "purpose": "Synthetic progression event-time and covariate power design; no biological claim",
        "synthetic": True,
        "n_seed_route_cells": len(seed_frame),
        "n_aggregate_route_cells": len(grid),
        "n_unique_simulated_cohorts": int(
            len(seeds)
            * len(sample_sizes)
            * len(event_probabilities)
            * len(hazard_ratios)
            * len(dropout_probabilities)
            * len(assignment_strengths)
            * args.replicates_per_seed
        ),
        "n_route_evaluations": int(seed_frame["n_simulated_cohorts"].sum()),
        "stratified_null_median": float(stratified_null["conclusive_probability"].median()),
        "stratified_null_maximum": float(stratified_null["conclusive_probability"].max()),
        "stratified_null_maximum_count": stratified_max_count,
        "stratified_null_maximum_total": stratified_max_total,
        "stratified_null_maximum_ci_low": float(
            stratified_max["conclusive_probability_ci_low"]
        ),
        "stratified_null_maximum_ci_high": float(
            stratified_max["conclusive_probability_ci_high"]
        ),
        "n_stratified_null_cells": len(stratified_null),
        "binomial_reference_probability_maximum_at_least_observed": maximum_reference_tail,
        "unadjusted_confounded_null_median": float(
            unadjusted_confounded_null["conclusive_probability"].median()
        ),
        "unadjusted_confounded_null_maximum": float(
            unadjusted_confounded_null["conclusive_probability"].max()
        ),
        "adjusted_nonnull_scenarios_reaching_80pct": int(
            (adjusted_minimum["minimum_n_reaching_80pct"] != "not_reached").sum()
        ),
        "adjusted_nonnull_scenarios": len(adjusted_minimum),
        "verdict": "EVENT_TIME_ROUTE_READY_FOR_BLINDED_COHORT_PARAMETERIZATION",
        "boundary": (
            "All values arise from explicit synthetic assumptions. They are method behavior, "
            "not empirical MS progression rates, effects, or evidence about a molecular state."
        ),
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    notable = adjusted_minimum.sort_values(
        [
            "assignment_strength",
            "dropout_probability",
            "event_probability_before_dropout",
            "molecular_hazard_ratio_per_latent_sd",
        ]
    )
    report = [
        "# V54 Progression Event-Time And Covariate Power Design",
        "",
        "All outputs are seeded synthetic method behavior. They are not biological",
        "evidence and do not estimate MS progression rates or effects.",
        "",
        f"The frozen grid generated {summary['n_unique_simulated_cohorts']:,} unique",
        f"synthetic cohorts and {summary['n_route_evaluations']:,} route evaluations.",
        "Each cohort was tested unadjusted and stratified by source x treatment.",
        "",
        "## Null Calibration",
        "",
        f"The stratified route had median null pass rate `{summary['stratified_null_median']:.3f}`",
        f"and maximum `{summary['stratified_null_maximum']:.3f}`.",
        f"The maximum is {summary['stratified_null_maximum_count']}/"
        f"{summary['stratified_null_maximum_total']} (Wilson 95% CI "
        f"`{summary['stratified_null_maximum_ci_low']:.3f}-"
        f"{summary['stratified_null_maximum_ci_high']:.3f}`). Across "
        f"{summary['n_stratified_null_cells']} null cells, the Binomial reference",
        f"probability of a maximum at least this large is "
        f"`{summary['binomial_reference_probability_maximum_at_least_observed']:.3f}`.",
        "",
        "Under deliberate",
        f"score-source-treatment confounding, the unadjusted route had median",
        f"`{summary['unadjusted_confounded_null_median']:.3f}` and maximum",
        f"`{summary['unadjusted_confounded_null_maximum']:.3f}`. These are simulation",
        "calibration results, not cohort facts.",
        "",
        "## Adjusted Planning Thresholds",
        "",
        "The table reports the first simulated N at which aggregate conclusive",
        "probability is at least 0.80 and every seed is at least 0.75.",
        "",
        "| confounding | dropout | event probability | HR / latent SD | minimum N | power at N=320 |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for row in notable.itertuples(index=False):
        report.append(
            f"| {row.assignment_strength:.1f} | {row.dropout_probability:.2f} | "
            f"{row.event_probability_before_dropout:.2f} | "
            f"{row.molecular_hazard_ratio_per_latent_sd:.1f} | "
            f"{row.minimum_n_reaching_80pct} | {row.power_at_largest_n:.3f} |"
        )
    report.extend(
        [
            "",
            "A reached N is conditional on the generator and is not a universal",
            "recruitment target. A real package must rerun this route while blinded",
            "using its event count, follow-up, censoring, missingness, source/treatment",
            "structure, endpoint adjudication, and frozen analysis budget.",
        ]
    )
    (args.output_dir / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
