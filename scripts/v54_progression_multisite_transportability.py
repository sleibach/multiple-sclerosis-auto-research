#!/usr/bin/env python3
"""Simulate multi-site transportability gates for progression studies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import binom, chi2, norm

from v54_progression_event_time_assumption_robustness import (
    calibrate_scale,
    finite_median,
    wilson,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_multisite_transportability"
DEFAULT_SEEDS = [54961, 54962, 54963]
SITE_BASELINE_MULTIPLIERS = np.array([0.6, 1.0, 1.8])
SITE_SCORE_MEANS = {
    "balanced_score": np.array([0.0, 0.0, 0.0]),
    "hazard_aligned_score": np.array([-0.8, 0.0, 0.8]),
}
EFFECT_PATTERNS = {
    "null": np.array([1.0, 1.0, 1.0]),
    "homogeneous": np.array([1.7, 1.7, 1.7]),
    "one_site_only": np.array([1.7, 1.0, 1.0]),
    "one_site_reversed": np.array([1.7, 1.7, 0.6]),
}
ALLOCATIONS = {
    "balanced": np.array([1 / 3, 1 / 3, 1 / 3]),
    "imbalanced_60_30_10": np.array([0.6, 0.3, 0.1]),
}


def csv_numbers(value: str, cast: type) -> list[Any]:
    return [cast(item.strip()) for item in value.split(",") if item.strip()]


def site_vector(n: int, proportions: np.ndarray) -> np.ndarray:
    counts = np.floor(n * proportions).astype(int)
    counts[-1] = n - int(counts[:-1].sum())
    return np.repeat(np.arange(3, dtype=np.int8), counts)


def cox_score_components(
    score: np.ndarray,
    time: np.ndarray,
    event: np.ndarray,
    strata: np.ndarray,
) -> tuple[float, float]:
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
        risk_variance = (
            risk_sum_sq[event_index] / risk_n[event_index] - risk_mean**2
        )
        score_statistic += float(
            np.sum(ordered_score[event_index] - risk_mean)
        )
        information += float(np.sum(np.maximum(risk_variance, 0.0)))
    return score_statistic, information


def component_test(score_statistic: float, information: float) -> tuple[float, float, float]:
    if information <= 1e-12 or not np.isfinite(information):
        return np.nan, np.nan, np.nan
    z_value = score_statistic / np.sqrt(information)
    return (
        float(z_value),
        float(2 * norm.sf(abs(z_value))),
        float(score_statistic / information),
    )


def simulate_cell(
    *,
    rng: np.random.Generator,
    n: int,
    event_probability: float,
    allocation_name: str,
    score_structure: str,
    effect_pattern: str,
    replicates: int,
    reliability: float,
    score_missing_rate: float,
    alpha: float,
) -> dict[str, Any]:
    site = site_vector(n, ALLOCATIONS[allocation_name])
    site_matrix = np.broadcast_to(site, (replicates, n))
    true_state = rng.normal(size=(replicates, n))
    progression_frailty = rng.normal(size=(replicates, n))
    site_hr = EFFECT_PATTERNS[effect_pattern][site]
    multiplier = (
        SITE_BASELINE_MULTIPLIERS[site][None, :]
        * np.exp(np.log(site_hr)[None, :] * true_state + 0.7 * progression_frailty)
    )
    baseline = calibrate_scale(multiplier, event_probability)
    event_time = -np.log(
        np.clip(rng.random((replicates, n)), 1e-12, 1.0)
    ) / (baseline[:, None] * multiplier)
    event = event_time <= 1.0
    observed_time = np.minimum(event_time, 1.0)
    observed_score = (
        SITE_SCORE_MEANS[score_structure][site][None, :]
        + np.sqrt(reliability) * true_state
        + np.sqrt(1 - reliability) * rng.normal(size=true_state.shape)
    )
    included = rng.random(true_state.shape) >= score_missing_rate

    valid = pooled_positive = pooled_negative = 0
    stratified_positive = stratified_negative = 0
    transport_pass = heterogeneity_detected = 0
    pooled_z_values: list[float] = []
    stratified_z_values: list[float] = []
    heterogeneity_p_values: list[float] = []
    minimum_site_event_values: list[int] = []
    minimum_site_n_values: list[int] = []
    for replicate in range(replicates):
        keep = included[replicate]
        if keep.sum() < 30:
            continue
        score = observed_score[replicate, keep]
        sd = float(np.std(score, ddof=1))
        if not np.isfinite(sd) or sd <= 0:
            continue
        score = (score - score.mean()) / sd
        time = observed_time[replicate, keep]
        status = event[replicate, keep]
        sites = site_matrix[replicate, keep]
        if status.sum() < 10 or (~status).sum() < 10:
            continue
        pooled_u, pooled_i = cox_score_components(
            score, time, status, np.zeros(len(score), dtype=np.int8)
        )
        pooled_z, pooled_p, _ = component_test(pooled_u, pooled_i)
        site_components = []
        site_events = []
        site_ns = []
        for site_id in range(3):
            selected = sites == site_id
            site_ns.append(int(selected.sum()))
            site_events.append(int(status[selected].sum()))
            site_components.append(
                cox_score_components(
                    score[selected],
                    time[selected],
                    status[selected],
                    np.zeros(int(selected.sum()), dtype=np.int8),
                )
            )
        site_u = np.array([item[0] for item in site_components])
        site_i = np.array([item[1] for item in site_components])
        stratified_z, stratified_p, global_beta = component_test(
            float(site_u.sum()), float(site_i.sum())
        )
        if not np.isfinite(pooled_p) or not np.isfinite(stratified_p):
            continue
        valid += 1
        pooled_z_values.append(pooled_z)
        stratified_z_values.append(stratified_z)
        minimum_site_event_values.append(min(site_events))
        minimum_site_n_values.append(min(site_ns))
        if pooled_p <= alpha and pooled_z > 0:
            pooled_positive += 1
        if pooled_p <= alpha and pooled_z < 0:
            pooled_negative += 1
        if stratified_p <= alpha and stratified_z > 0:
            stratified_positive += 1
        if stratified_p <= alpha and stratified_z < 0:
            stratified_negative += 1

        valid_sites = site_i > 1e-12
        site_beta = np.full(3, np.nan)
        site_beta[valid_sites] = site_u[valid_sites] / site_i[valid_sites]
        if valid_sites.sum() >= 2:
            q_value = float(
                np.sum(site_i[valid_sites] * (site_beta[valid_sites] - global_beta) ** 2)
            )
            heterogeneity_p = float(chi2.sf(q_value, valid_sites.sum() - 1))
        else:
            heterogeneity_p = np.nan
        heterogeneity_p_values.append(heterogeneity_p)
        if np.isfinite(heterogeneity_p) and heterogeneity_p < alpha:
            heterogeneity_detected += 1

        leave_out_pass = []
        for omitted in range(3):
            retained = np.arange(3) != omitted
            loo_z, loo_p, _ = component_test(
                float(site_u[retained].sum()), float(site_i[retained].sum())
            )
            leave_out_pass.append(
                np.isfinite(loo_p) and loo_p <= alpha and loo_z > 0
            )
        passes = (
            stratified_p <= alpha
            and stratified_z > 0
            and bool(np.all(site_beta > 0))
            and bool(np.all(leave_out_pass))
            and min(site_events) >= 10
            and np.isfinite(heterogeneity_p)
            and heterogeneity_p >= alpha
        )
        if passes:
            transport_pass += 1

    pooled_significant = pooled_positive + pooled_negative
    stratified_significant = stratified_positive + stratified_negative
    pooled_low, pooled_high = wilson(pooled_significant, replicates)
    stratified_low, stratified_high = wilson(stratified_significant, replicates)
    return {
        "n_requested": n,
        "latent_event_probability": event_probability,
        "allocation": allocation_name,
        "score_site_structure": score_structure,
        "effect_pattern": effect_pattern,
        "n_simulated_cohorts": replicates,
        "n_valid_fits": valid,
        "valid_fit_rate": valid / replicates,
        "pooled_significant_count": pooled_significant,
        "pooled_significant_probability": pooled_significant / replicates,
        "pooled_significant_ci_low": pooled_low,
        "pooled_significant_ci_high": pooled_high,
        "pooled_positive_probability": pooled_positive / replicates,
        "pooled_negative_probability": pooled_negative / replicates,
        "stratified_significant_count": stratified_significant,
        "stratified_significant_probability": stratified_significant / replicates,
        "stratified_significant_ci_low": stratified_low,
        "stratified_significant_ci_high": stratified_high,
        "stratified_positive_probability": stratified_positive / replicates,
        "stratified_negative_probability": stratified_negative / replicates,
        "transport_pass_probability": transport_pass / replicates,
        "heterogeneity_detection_probability": heterogeneity_detected / replicates,
        "median_pooled_z": finite_median(pooled_z_values),
        "median_stratified_z": finite_median(stratified_z_values),
        "median_heterogeneity_p": finite_median(heterogeneity_p_values),
        "median_minimum_site_events": finite_median(minimum_site_event_values),
        "median_minimum_site_n": finite_median(minimum_site_n_values),
    }


def aggregate(seed_frame: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "n_requested",
        "latent_event_probability",
        "allocation",
        "score_site_structure",
        "effect_pattern",
    ]
    rows = []
    count_probability_pairs = [
        ("pooled_significant_count", "pooled_significant_probability"),
        ("stratified_significant_count", "stratified_significant_probability"),
    ]
    for values, group in seed_frame.groupby(keys, sort=True):
        row = dict(zip(keys, values))
        total = int(group.n_simulated_cohorts.sum())
        row["n_simulated_cohorts"] = total
        row["n_valid_fits"] = int(group.n_valid_fits.sum())
        row["valid_fit_rate"] = row["n_valid_fits"] / total
        for count_column, probability_column in count_probability_pairs:
            count = int(group[count_column].sum())
            low, high = wilson(count, total)
            prefix = probability_column.removesuffix("_probability")
            row[count_column] = count
            row[probability_column] = count / total
            row[f"{prefix}_ci_low"] = low
            row[f"{prefix}_ci_high"] = high
            row[f"minimum_seed_{probability_column}"] = float(
                group[probability_column].min()
            )
        for probability_column in [
            "pooled_positive_probability",
            "pooled_negative_probability",
            "stratified_positive_probability",
            "stratified_negative_probability",
            "transport_pass_probability",
            "heterogeneity_detection_probability",
        ]:
            row[probability_column] = float(group[probability_column].mean())
            row[f"minimum_seed_{probability_column}"] = float(
                group[probability_column].min()
            )
            row[f"maximum_seed_{probability_column}"] = float(
                group[probability_column].max()
            )
        for median_column in [
            "median_pooled_z",
            "median_stratified_z",
            "median_heterogeneity_p",
            "median_minimum_site_events",
            "median_minimum_site_n",
        ]:
            row[f"{median_column}_across_seeds"] = finite_median(group[median_column])
        rows.append(row)
    return pd.DataFrame(rows)


def null_calibration(grid: pd.DataFrame, route: str, alpha: float) -> pd.DataFrame:
    probability = f"{route}_significant_probability"
    count_column = f"{route}_significant_count"
    ci_low = f"{route}_significant_ci_low"
    null = grid.loc[grid.effect_pattern.eq("null")]
    rows = []
    for values, group in null.groupby(
        ["allocation", "score_site_structure"], sort=True
    ):
        allocation, structure = values
        maximum = group.loc[group[probability].idxmax()]
        count = int(maximum[count_column])
        total = int(maximum.n_simulated_cohorts)
        single_tail = float(binom.sf(count - 1, total, alpha))
        family_tail = float(1 - (1 - single_tail) ** len(group))
        strict_flag = bool((group[ci_low] > alpha).any())
        rows.append(
            {
                "analysis_route": route,
                "allocation": allocation,
                "score_site_structure": structure,
                "n_null_cells": len(group),
                "median_null_probability": float(group[probability].median()),
                "maximum_null_probability": float(maximum[probability]),
                "maximum_count": count,
                "maximum_total": total,
                "family_probability_maximum_at_least_observed": family_tail,
                "strict_cell_flag": strict_flag,
                "invalid_by_frozen_rule": strict_flag and family_tail < 0.05,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-sizes", default="180,300,450")
    parser.add_argument("--event-probabilities", default="0.15,0.30")
    parser.add_argument("--replicates-per-seed", type=int, default=400)
    parser.add_argument("--seeds", default=",".join(map(str, DEFAULT_SEEDS)))
    parser.add_argument("--reliability", type=float, default=0.70)
    parser.add_argument("--score-missing-rate", type=float, default=0.10)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    sizes = csv_numbers(args.sample_sizes, int)
    event_probabilities = csv_numbers(args.event_probabilities, float)
    seeds = csv_numbers(args.seeds, int)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    config = {
        "synthetic": True,
        "sample_sizes": sizes,
        "latent_event_probabilities": event_probabilities,
        "allocations": {key: value.tolist() for key, value in ALLOCATIONS.items()},
        "site_baseline_hazard_multipliers": SITE_BASELINE_MULTIPLIERS.tolist(),
        "site_score_means": {key: value.tolist() for key, value in SITE_SCORE_MEANS.items()},
        "effect_patterns_site_hrs": {key: value.tolist() for key, value in EFFECT_PATTERNS.items()},
        "measurement_reliability": args.reliability,
        "score_missing_rate": args.score_missing_rate,
        "replicates_per_seed": args.replicates_per_seed,
        "seeds": seeds,
        "alpha": args.alpha,
        "transport_gate": {
            "stratified_positive_p_max": 0.05,
            "all_site_estimates_positive": True,
            "all_leave_site_out_positive_p_max": 0.05,
            "minimum_events_per_site": 10,
            "heterogeneity_p_min": 0.05,
        },
        "boundary": "Seeded synthetic method behavior only; not empirical MS progression, site effects, treatment, or biology.",
    }
    (args.output_dir / "simulation_config.json").write_text(
        json.dumps(config, indent=2) + "\n"
    )

    rows = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for n in sizes:
            for event_probability in event_probabilities:
                for allocation in ALLOCATIONS:
                    for score_structure in SITE_SCORE_MEANS:
                        for effect_pattern in EFFECT_PATTERNS:
                            rows.append(
                                {
                                    "seed": seed,
                                    **simulate_cell(
                                        rng=rng,
                                        n=n,
                                        event_probability=event_probability,
                                        allocation_name=allocation,
                                        score_structure=score_structure,
                                        effect_pattern=effect_pattern,
                                        replicates=args.replicates_per_seed,
                                        reliability=args.reliability,
                                        score_missing_rate=args.score_missing_rate,
                                        alpha=args.alpha,
                                    ),
                                }
                            )
    seed_frame = pd.DataFrame(rows)
    seed_frame.to_csv(args.output_dir / "seed_results.tsv", sep="\t", index=False)
    grid = aggregate(seed_frame)
    grid.to_csv(args.output_dir / "multisite_grid.tsv", sep="\t", index=False)
    calibration = pd.concat(
        [
            null_calibration(grid, "pooled", args.alpha),
            null_calibration(grid, "stratified", args.alpha),
        ],
        ignore_index=True,
    )
    calibration.to_csv(
        args.output_dir / "null_calibration_by_route.tsv", sep="\t", index=False
    )

    decision_keys = [
        "n_requested",
        "latent_event_probability",
        "allocation",
        "score_site_structure",
    ]
    homogeneous = grid.loc[grid.effect_pattern.eq("homogeneous")].copy()
    controls = grid.loc[
        grid.effect_pattern.isin(["one_site_only", "one_site_reversed"])
    ]
    false_transport = controls.pivot_table(
        index=decision_keys,
        columns="effect_pattern",
        values="transport_pass_probability",
    ).reset_index().rename_axis(None, axis=1)
    decisions = homogeneous.merge(
        false_transport, on=decision_keys, how="left", validate="one_to_one"
    )
    decisions["transport_ready"] = (
        decisions.transport_pass_probability.ge(0.80)
        & decisions.minimum_seed_transport_pass_probability.ge(0.75)
        & decisions.one_site_only.le(0.05)
        & decisions.one_site_reversed.le(0.05)
    )
    decisions[[
        *decision_keys,
        "stratified_positive_probability",
        "transport_pass_probability",
        "minimum_seed_transport_pass_probability",
        "median_minimum_site_events_across_seeds",
        "heterogeneity_detection_probability",
        "one_site_only",
        "one_site_reversed",
        "transport_ready",
    ]].to_csv(args.output_dir / "transport_readiness.tsv", sep="\t", index=False)

    pooled_invalid = calibration.loc[
        calibration.analysis_route.eq("pooled") & calibration.invalid_by_frozen_rule
    ]
    stratified_invalid = calibration.loc[
        calibration.analysis_route.eq("stratified") & calibration.invalid_by_frozen_rule
    ]
    ready = decisions.loc[decisions.transport_ready]
    summary = {
        "purpose": "Synthetic multi-site progression transportability audit; no biological claim",
        "synthetic": True,
        "n_unique_simulated_cohorts": int(seed_frame.n_simulated_cohorts.sum()),
        "n_aggregate_cells": len(grid),
        "n_pooled_invalid_null_families": len(pooled_invalid),
        "pooled_invalid_null_families": sorted(
            f"{row.allocation}|{row.score_site_structure}"
            for row in pooled_invalid.itertuples(index=False)
        ),
        "n_stratified_invalid_null_families": len(stratified_invalid),
        "n_transport_ready_designs": len(ready),
        "n_transport_designs": len(decisions),
        "maximum_false_transport_one_site_only": float(decisions.one_site_only.max()),
        "maximum_false_transport_one_site_reversed": float(decisions.one_site_reversed.max()),
        "verdict": "NO_DESIGN_PASSES_FULL_TRANSPORT_GATE" if ready.empty else "TRANSPORT_READY_DESIGNS_IDENTIFIED",
        "boundary": "All values are seeded synthetic method behavior, not empirical MS progression, site effects, treatment, or biology.",
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    (args.output_dir / "REPORT.md").write_text(
        "# V54 Progression Multi-Site Transportability\n\n"
        "All outputs are seeded synthetic method behavior, not biological evidence.\n\n"
        f"The audit generated {summary['n_unique_simulated_cohorts']:,} unique cohorts. "
        f"{summary['n_transport_ready_designs']}/{summary['n_transport_designs']} designs pass the full transport gate. "
        "Pooled significance is never a substitute for site-stratified, leave-site-out, and heterogeneity checks.\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
