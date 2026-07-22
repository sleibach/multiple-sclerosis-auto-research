#!/usr/bin/env python3
"""Audit blinded site-score harmonization for progression transport."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import binom, chi2

from v54_progression_event_time_assumption_robustness import (
    calibrate_scale,
    finite_median,
    wilson,
)
from v54_progression_multisite_transportability import (
    ALLOCATIONS,
    SITE_BASELINE_MULTIPLIERS,
    component_test,
    cox_score_components,
    site_vector,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_site_score_harmonization"
DEFAULT_SEEDS = [54971, 54972, 54973]
SITE_OFFSETS = np.array([-0.8, 0.0, 0.8])
SCALE_PATTERNS = {
    "uniform": np.array([1.0, 1.0, 1.0]),
    "moderate": np.array([0.7, 1.0, 1.4]),
    "severe": np.array([0.5, 1.0, 2.0]),
}
EFFECT_PATTERNS = {
    "null": np.array([1.0, 1.0, 1.0]),
    "homogeneous": np.array([1.7, 1.7, 1.7]),
    "one_site_reversed": np.array([1.7, 1.7, 0.6]),
}
ROUTES = ["global_scale", "within_site_scale"]


def csv_numbers(value: str, cast: type) -> list[Any]:
    return [cast(item.strip()) for item in value.split(",") if item.strip()]


def transform_score(raw: np.ndarray, site: np.ndarray, route: str) -> np.ndarray:
    transformed = raw.copy()
    if route == "global_scale":
        sd = float(np.std(transformed, ddof=1))
        return (transformed - transformed.mean()) / sd
    if route != "within_site_scale":
        raise ValueError(f"Unknown score route: {route}")
    for site_id in range(3):
        selected = site == site_id
        sd = float(np.std(transformed[selected], ddof=1))
        transformed[selected] = (
            transformed[selected] - transformed[selected].mean()
        ) / sd
    return transformed


def analyze_route(
    *,
    observed_score: np.ndarray,
    included: np.ndarray,
    observed_time: np.ndarray,
    event: np.ndarray,
    site_matrix: np.ndarray,
    route: str,
    replicates: int,
    alpha: float,
) -> dict[str, Any]:
    valid = positive = negative = transport_pass = heterogeneity_detected = 0
    z_values: list[float] = []
    heterogeneity_values: list[float] = []
    minimum_event_values: list[int] = []
    for replicate in range(replicates):
        keep = included[replicate]
        if keep.sum() < 30:
            continue
        sites = site_matrix[replicate, keep]
        score = transform_score(observed_score[replicate, keep], sites, route)
        time = observed_time[replicate, keep]
        status = event[replicate, keep]
        if status.sum() < 10 or (~status).sum() < 10:
            continue
        site_components = []
        site_events = []
        for site_id in range(3):
            selected = sites == site_id
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
        z_value, p_value, global_beta = component_test(
            float(site_u.sum()), float(site_i.sum())
        )
        if not np.isfinite(p_value):
            continue
        valid += 1
        z_values.append(z_value)
        minimum_event_values.append(min(site_events))
        if p_value <= alpha and z_value > 0:
            positive += 1
        if p_value <= alpha and z_value < 0:
            negative += 1

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
        heterogeneity_values.append(heterogeneity_p)
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
        if (
            p_value <= alpha
            and z_value > 0
            and bool(np.all(site_beta > 0))
            and bool(np.all(leave_out_pass))
            and min(site_events) >= 10
            and np.isfinite(heterogeneity_p)
            and heterogeneity_p >= alpha
        ):
            transport_pass += 1
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
        "positive_probability": positive / replicates,
        "negative_probability": negative / replicates,
        "transport_pass_probability": transport_pass / replicates,
        "heterogeneity_detection_probability": heterogeneity_detected / replicates,
        "median_z": finite_median(z_values),
        "median_heterogeneity_p": finite_median(heterogeneity_values),
        "median_minimum_site_events": finite_median(minimum_event_values),
    }


def simulate_cell(
    *,
    rng: np.random.Generator,
    n: int,
    event_probability: float,
    allocation_name: str,
    scale_pattern: str,
    effect_pattern: str,
    replicates: int,
    reliability: float,
    score_missing_rate: float,
    alpha: float,
) -> list[dict[str, Any]]:
    site = site_vector(n, ALLOCATIONS[allocation_name])
    site_matrix = np.broadcast_to(site, (replicates, n))
    true_state = rng.normal(size=(replicates, n))
    frailty = rng.normal(size=(replicates, n))
    site_hr = EFFECT_PATTERNS[effect_pattern][site]
    multiplier = (
        SITE_BASELINE_MULTIPLIERS[site][None, :]
        * np.exp(np.log(site_hr)[None, :] * true_state + 0.7 * frailty)
    )
    baseline = calibrate_scale(multiplier, event_probability)
    event_time = -np.log(
        np.clip(rng.random((replicates, n)), 1e-12, 1.0)
    ) / (baseline[:, None] * multiplier)
    event = event_time <= 1.0
    observed_time = np.minimum(event_time, 1.0)
    pre_scale = (
        np.sqrt(reliability) * true_state
        + np.sqrt(1 - reliability) * rng.normal(size=true_state.shape)
    )
    observed_score = (
        SITE_OFFSETS[site][None, :]
        + SCALE_PATTERNS[scale_pattern][site][None, :] * pre_scale
    )
    included = rng.random(true_state.shape) >= score_missing_rate
    rows = []
    for route in ROUTES:
        rows.append(
            {
                "n_requested": n,
                "latent_event_probability": event_probability,
                "allocation": allocation_name,
                "site_scale_pattern": scale_pattern,
                "effect_pattern": effect_pattern,
                "score_transform": route,
                **analyze_route(
                    observed_score=observed_score,
                    included=included,
                    observed_time=observed_time,
                    event=event,
                    site_matrix=site_matrix,
                    route=route,
                    replicates=replicates,
                    alpha=alpha,
                ),
            }
        )
    return rows


def aggregate(seed_frame: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "n_requested",
        "latent_event_probability",
        "allocation",
        "site_scale_pattern",
        "effect_pattern",
        "score_transform",
    ]
    rows = []
    for values, group in seed_frame.groupby(keys, sort=True):
        row = dict(zip(keys, values))
        total = int(group.n_simulated_cohorts.sum())
        significant = int(group.significant_count.sum())
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
                "minimum_seed_significant_probability": float(
                    group.significant_probability.min()
                ),
                "positive_probability": float(group.positive_probability.mean()),
                "negative_probability": float(group.negative_probability.mean()),
                "transport_pass_probability": float(
                    group.transport_pass_probability.mean()
                ),
                "minimum_seed_transport_pass_probability": float(
                    group.transport_pass_probability.min()
                ),
                "maximum_seed_transport_pass_probability": float(
                    group.transport_pass_probability.max()
                ),
                "heterogeneity_detection_probability": float(
                    group.heterogeneity_detection_probability.mean()
                ),
                "median_z_across_seeds": finite_median(group.median_z),
                "median_heterogeneity_p_across_seeds": finite_median(
                    group.median_heterogeneity_p
                ),
                "median_minimum_site_events_across_seeds": finite_median(
                    group.median_minimum_site_events
                ),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def calibration(grid: pd.DataFrame, alpha: float) -> pd.DataFrame:
    null = grid.loc[grid.effect_pattern.eq("null")]
    rows = []
    for values, group in null.groupby(
        ["allocation", "site_scale_pattern", "score_transform"], sort=True
    ):
        allocation, scale_pattern, transform = values
        maximum = group.loc[group.significant_probability.idxmax()]
        count = int(maximum.significant_count)
        total = int(maximum.n_simulated_cohorts)
        single_tail = float(binom.sf(count - 1, total, alpha))
        family_tail = float(1 - (1 - single_tail) ** len(group))
        strict = bool((group.significant_probability_ci_low > alpha).any())
        rows.append(
            {
                "allocation": allocation,
                "site_scale_pattern": scale_pattern,
                "score_transform": transform,
                "n_null_cells": len(group),
                "median_null_probability": float(group.significant_probability.median()),
                "maximum_null_probability": float(maximum.significant_probability),
                "maximum_count": count,
                "maximum_total": total,
                "family_probability_maximum_at_least_observed": family_tail,
                "strict_cell_flag": strict,
                "invalid_by_frozen_rule": strict and family_tail < 0.05,
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
        "site_score_offsets": SITE_OFFSETS.tolist(),
        "site_scale_patterns": {key: value.tolist() for key, value in SCALE_PATTERNS.items()},
        "effect_patterns_site_hrs": {key: value.tolist() for key, value in EFFECT_PATTERNS.items()},
        "score_transforms": ROUTES,
        "measurement_reliability_before_site_scaling": args.reliability,
        "score_missing_rate": args.score_missing_rate,
        "replicates_per_seed": args.replicates_per_seed,
        "seeds": seeds,
        "alpha": args.alpha,
        "boundary": "Seeded synthetic method behavior only; not empirical MS progression, assay, site, treatment, or biology.",
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
                    for scale_pattern in SCALE_PATTERNS:
                        for effect_pattern in EFFECT_PATTERNS:
                            cell_rows = simulate_cell(
                                rng=rng,
                                n=n,
                                event_probability=event_probability,
                                allocation_name=allocation,
                                scale_pattern=scale_pattern,
                                effect_pattern=effect_pattern,
                                replicates=args.replicates_per_seed,
                                reliability=args.reliability,
                                score_missing_rate=args.score_missing_rate,
                                alpha=args.alpha,
                            )
                            rows.extend({"seed": seed, **row} for row in cell_rows)
    seed_frame = pd.DataFrame(rows)
    seed_frame.to_csv(args.output_dir / "seed_results.tsv", sep="\t", index=False)
    grid = aggregate(seed_frame)
    grid.to_csv(args.output_dir / "harmonization_grid.tsv", sep="\t", index=False)
    calibration_frame = calibration(grid, args.alpha)
    calibration_frame.to_csv(
        args.output_dir / "null_calibration.tsv", sep="\t", index=False
    )

    homogeneous = grid.loc[grid.effect_pattern.eq("homogeneous")]
    comparison_keys = [
        "n_requested",
        "latent_event_probability",
        "allocation",
        "site_scale_pattern",
    ]
    comparison = homogeneous.pivot_table(
        index=comparison_keys,
        columns="score_transform",
        values=["transport_pass_probability", "minimum_seed_transport_pass_probability"],
    )
    comparison.columns = ["_".join(column) for column in comparison.columns]
    comparison = comparison.reset_index()
    reversed_grid = grid.loc[grid.effect_pattern.eq("one_site_reversed")]
    reversed_pivot = reversed_grid.pivot_table(
        index=comparison_keys,
        columns="score_transform",
        values="transport_pass_probability",
    ).reset_index().rename(
        columns={route: f"false_transport_{route}" for route in ROUTES}
    )
    comparison = comparison.merge(
        reversed_pivot, on=comparison_keys, how="left", validate="one_to_one"
    )
    comparison["aggregate_transport_gain"] = (
        comparison.transport_pass_probability_within_site_scale
        - comparison.transport_pass_probability_global_scale
    )
    comparison["minimum_seed_transport_gain"] = (
        comparison.minimum_seed_transport_pass_probability_within_site_scale
        - comparison.minimum_seed_transport_pass_probability_global_scale
    )
    valid_within_families = calibration_frame.loc[
        calibration_frame.score_transform.eq("within_site_scale")
        & ~calibration_frame.strict_cell_flag
    ][["allocation", "site_scale_pattern"]].drop_duplicates()
    valid_pairs = set(map(tuple, valid_within_families.to_numpy()))
    comparison["within_site_null_calibrated"] = comparison.apply(
        lambda row: (row.allocation, row.site_scale_pattern) in valid_pairs,
        axis=1,
    )
    comparison["material_harmonization_gain"] = (
        comparison.within_site_null_calibrated
        & comparison.aggregate_transport_gain.ge(0.10)
        & comparison.minimum_seed_transport_gain.ge(0.10)
        & comparison.false_transport_within_site_scale.le(0.05)
    )
    comparison.to_csv(
        args.output_dir / "harmonization_transport_gains.tsv", sep="\t", index=False
    )

    invalid = calibration_frame.loc[calibration_frame.invalid_by_frozen_rule]
    material = comparison.loc[comparison.material_harmonization_gain]
    summary = {
        "purpose": "Synthetic site-score harmonization and progression transport audit; no biological claim",
        "synthetic": True,
        "n_unique_simulated_cohorts": int(seed_frame.n_simulated_cohorts.sum() / len(ROUTES)),
        "n_route_evaluations": int(seed_frame.n_simulated_cohorts.sum()),
        "n_aggregate_route_cells": len(grid),
        "n_invalid_null_families": len(invalid),
        "n_harmonization_comparisons": len(comparison),
        "n_material_harmonization_gains": len(material),
        "material_gain_scale_patterns": sorted(material.site_scale_pattern.unique().tolist()),
        "maximum_false_transport_within_site_scale": float(
            comparison.false_transport_within_site_scale.max()
        ),
        "verdict": "WITHIN_SITE_SCALING_IS_REQUIRED_WHEN_ASSAY_SCALES_DIFFER" if len(material) else "NO_MATERIAL_HARMONIZATION_GAIN",
        "boundary": "All values are seeded synthetic method behavior, not empirical MS progression, assay, site, treatment, or biology.",
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    (args.output_dir / "REPORT.md").write_text(
        "# V54 Progression Site-Score Harmonization\n\n"
        "All outputs are seeded synthetic method behavior, not biological evidence.\n\n"
        f"The audit generated {summary['n_unique_simulated_cohorts']:,} cohorts and "
        f"{summary['n_route_evaluations']:,} route evaluations. "
        f"{summary['n_material_harmonization_gains']}/{summary['n_harmonization_comparisons']} "
        "comparisons meet the frozen harmonization-gain rule.\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
