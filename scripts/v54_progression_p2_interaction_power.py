#!/usr/bin/env python3
"""Simulate direct P2 compartment-interaction power under composition stress."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import binom, norm, t as student_t


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_p2_interaction_power"
DEFAULT_SEEDS = [54911, 54912, 54913]


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


def batched_ols_test(
    response: np.ndarray,
    design: np.ndarray,
    coefficient_index: int,
) -> dict[str, np.ndarray]:
    xtx = np.einsum("rni,rnj->rij", design, design)
    condition = np.linalg.cond(xtx)
    inverse = np.linalg.pinv(xtx, rcond=1e-12)
    xty = np.einsum("rni,rn->ri", design, response)
    beta = np.einsum("rij,rj->ri", inverse, xty)
    fitted = np.einsum("rni,ri->rn", design, beta)
    residual = response - fitted
    df = response.shape[1] - design.shape[2]
    rss = np.sum(residual * residual, axis=1)
    sigma2 = rss / df
    variance = sigma2 * inverse[:, coefficient_index, coefficient_index]
    se = np.sqrt(np.maximum(variance, 0.0))
    estimate = beta[:, coefficient_index]
    statistic = np.divide(
        estimate,
        se,
        out=np.full_like(estimate, np.nan),
        where=se > 0,
    )
    p_value = 2 * student_t.sf(np.abs(statistic), df)
    valid = (
        np.isfinite(estimate)
        & np.isfinite(se)
        & np.isfinite(p_value)
        & (condition < 1e10)
        & (df > 0)
    )
    return {
        "estimate": estimate,
        "se": se,
        "statistic": statistic,
        "p_value": p_value,
        "condition": condition,
        "valid": valid,
        "df": np.full(response.shape[0], df),
    }


def measured_composition(
    rng: np.random.Generator,
    truth: np.ndarray,
    reliability: float,
) -> np.ndarray:
    centered = truth - truth.mean(axis=1, keepdims=True)
    sd = truth.std(axis=1, ddof=1, keepdims=True)
    standardized = np.divide(
        centered,
        sd,
        out=np.zeros_like(centered),
        where=sd > 0,
    )
    return (
        np.sqrt(reliability) * standardized
        + np.sqrt(1 - reliability) * rng.normal(size=truth.shape)
    )


def summarize_route(
    result: dict[str, np.ndarray],
    interaction_effect: float,
    alpha: float,
    replicates: int,
) -> dict[str, Any]:
    valid = result["valid"]
    conclusive = valid & (result["p_value"] <= alpha)
    if interaction_effect > 0:
        conclusive &= result["estimate"] > 0
    count = int(conclusive.sum())
    ci_low, ci_high = wilson(count, replicates)
    return {
        "n_simulated_cohorts": replicates,
        "n_valid_fits": int(valid.sum()),
        "valid_fit_rate": float(valid.mean()),
        "conclusive_count": count,
        "conclusive_probability": count / replicates,
        "conclusive_probability_ci_low": ci_low,
        "conclusive_probability_ci_high": ci_high,
        "median_interaction_estimate": (
            float(np.median(result["estimate"][valid])) if np.any(valid) else np.nan
        ),
        "median_interaction_se": (
            float(np.median(result["se"][valid])) if np.any(valid) else np.nan
        ),
        "maximum_design_condition": float(np.nanmax(result["condition"])),
    }


def simulate_paired(
    *,
    rng: np.random.Generator,
    n_per_group: int,
    interaction_effect: float,
    residual_correlation: float,
    composition_imbalance: float,
    composition_reliability: float,
    alpha: float,
    replicates: int,
) -> list[dict[str, Any]]:
    n_subjects = 2 * n_per_group
    outcome = np.concatenate([np.zeros(n_per_group), np.ones(n_per_group)])
    outcome_matrix = np.broadcast_to(outcome, (replicates, n_subjects))

    shared_error = rng.normal(size=(replicates, n_subjects))
    blood_error = (
        np.sqrt(residual_correlation) * shared_error
        + np.sqrt(1 - residual_correlation) * rng.normal(size=(replicates, n_subjects))
    )
    cns_error = (
        np.sqrt(residual_correlation) * shared_error
        + np.sqrt(1 - residual_correlation) * rng.normal(size=(replicates, n_subjects))
    )
    shared_composition = rng.normal(size=(replicates, n_subjects))
    blood_composition = (
        np.sqrt(0.5) * shared_composition
        + np.sqrt(0.5) * rng.normal(size=(replicates, n_subjects))
        + 0.2 * outcome_matrix
    )
    cns_composition = (
        np.sqrt(0.5) * shared_composition
        + np.sqrt(0.5) * rng.normal(size=(replicates, n_subjects))
        + (0.2 + composition_imbalance) * outcome_matrix
    )
    measured_blood = measured_composition(rng, blood_composition, composition_reliability)
    measured_cns = measured_composition(rng, cns_composition, composition_reliability)

    blood_score = 0.3 * outcome_matrix + 0.6 * blood_composition + blood_error
    cns_score = (
        (0.3 + interaction_effect) * outcome_matrix
        + 0.6 * cns_composition
        + cns_error
    )
    difference = cns_score - blood_score
    composition_difference = measured_cns - measured_blood

    intercept = np.ones_like(outcome_matrix)
    unadjusted_design = np.stack([intercept, outcome_matrix], axis=2)
    adjusted_design = np.stack(
        [intercept, outcome_matrix, composition_difference], axis=2
    )
    results = []
    for route, design in (
        ("unadjusted", unadjusted_design),
        ("composition_adjusted", adjusted_design),
    ):
        result = batched_ols_test(difference, design, coefficient_index=1)
        results.append(
            {
                "analysis_route": route,
                **summarize_route(result, interaction_effect, alpha, replicates),
            }
        )
    return results


def simulate_unpaired(
    *,
    rng: np.random.Generator,
    n_per_group: int,
    interaction_effect: float,
    composition_imbalance: float,
    composition_reliability: float,
    alpha: float,
    replicates: int,
) -> list[dict[str, Any]]:
    outcome = np.tile(
        np.concatenate([np.zeros(n_per_group), np.ones(n_per_group)]), 2
    )
    compartment = np.concatenate(
        [np.zeros(2 * n_per_group), np.ones(2 * n_per_group)]
    )
    interaction = outcome * compartment
    outcome_matrix = np.broadcast_to(outcome, (replicates, len(outcome)))
    compartment_matrix = np.broadcast_to(compartment, (replicates, len(outcome)))
    interaction_matrix = np.broadcast_to(interaction, (replicates, len(outcome)))

    true_composition = (
        rng.normal(size=(replicates, len(outcome)))
        + 0.2 * outcome_matrix
        + composition_imbalance * interaction_matrix
    )
    observed_composition = measured_composition(
        rng, true_composition, composition_reliability
    )
    score = (
        0.3 * outcome_matrix
        + interaction_effect * interaction_matrix
        + 0.6 * true_composition
        + rng.normal(size=(replicates, len(outcome)))
    )
    intercept = np.ones_like(outcome_matrix)
    unadjusted_design = np.stack(
        [intercept, outcome_matrix, compartment_matrix, interaction_matrix], axis=2
    )
    adjusted_design = np.stack(
        [
            intercept,
            outcome_matrix,
            compartment_matrix,
            interaction_matrix,
            observed_composition,
            observed_composition * compartment_matrix,
        ],
        axis=2,
    )
    results = []
    for route, design in (
        ("unadjusted", unadjusted_design),
        ("composition_adjusted", adjusted_design),
    ):
        result = batched_ols_test(score, design, coefficient_index=3)
        results.append(
            {
                "analysis_route": route,
                **summarize_route(result, interaction_effect, alpha, replicates),
            }
        )
    return results


def aggregate(seed_frame: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "design",
        "analysis_route",
        "n_per_outcome_group_per_compartment",
        "n_unique_subjects",
        "n_samples",
        "interaction_effect_sd",
        "paired_residual_correlation",
        "composition_imbalance",
        "composition_reliability",
        "alpha",
    ]
    rows = []
    for values, group in seed_frame.groupby(keys, sort=True, dropna=False):
        row = dict(zip(keys, values))
        total = int(group["n_simulated_cohorts"].sum())
        count = int(group["conclusive_count"].sum())
        ci_low, ci_high = wilson(count, total)
        row.update(
            {
                "n_simulated_cohorts": total,
                "n_valid_fits": int(group["n_valid_fits"].sum()),
                "valid_fit_rate": float(group["n_valid_fits"].sum() / total),
                "conclusive_probability": count / total,
                "conclusive_probability_ci_low": ci_low,
                "conclusive_probability_ci_high": ci_high,
                "minimum_seed_probability": float(group["conclusive_probability"].min()),
                "maximum_seed_probability": float(group["conclusive_probability"].max()),
                "median_interaction_estimate_across_seeds": float(
                    group["median_interaction_estimate"].median()
                ),
                "median_interaction_se_across_seeds": float(
                    group["median_interaction_se"].median()
                ),
                "maximum_design_condition": float(group["maximum_design_condition"].max()),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def minimum_n(grid: pd.DataFrame) -> pd.DataFrame:
    scenario_keys = [
        "design",
        "analysis_route",
        "interaction_effect_sd",
        "paired_residual_correlation",
        "composition_imbalance",
        "composition_reliability",
        "alpha",
    ]
    rows = []
    nonnull = grid.loc[grid["interaction_effect_sd"].gt(0)]
    for values, group in nonnull.groupby(scenario_keys, sort=True, dropna=False):
        ordered = group.sort_values("n_per_outcome_group_per_compartment")
        reached = ordered.loc[
            ordered["conclusive_probability"].ge(0.80)
            & ordered["minimum_seed_probability"].ge(0.75)
        ]
        row = dict(zip(scenario_keys, values))
        last = ordered.iloc[-1]
        row.update(
            {
                "largest_group_n_simulated": int(
                    last["n_per_outcome_group_per_compartment"]
                ),
                "power_at_largest_group_n": float(last["conclusive_probability"]),
                "minimum_group_n_reaching_80pct": (
                    "not_reached"
                    if reached.empty
                    else int(reached.iloc[0]["n_per_outcome_group_per_compartment"])
                ),
                "unique_subjects_at_minimum": (
                    "not_reached"
                    if reached.empty
                    else int(reached.iloc[0]["n_unique_subjects"])
                ),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def null_family_summary(null: pd.DataFrame, label: str) -> dict[str, Any]:
    maximum_row = null.loc[null["conclusive_probability"].idxmax()]
    total = int(maximum_row["n_simulated_cohorts"])
    count = int(round(maximum_row["conclusive_probability"] * total))
    cell_tail = float(binom.sf(count - 1, total, 0.05))
    family_tail = float(1 - (1 - cell_tail) ** len(null))
    return {
        "label": label,
        "n_cells": len(null),
        "median": float(null["conclusive_probability"].median()),
        "maximum": float(maximum_row["conclusive_probability"]),
        "maximum_count": count,
        "maximum_total": total,
        "maximum_ci_low": float(maximum_row["conclusive_probability_ci_low"]),
        "maximum_ci_high": float(maximum_row["conclusive_probability_ci_high"]),
        "binomial_reference_probability_maximum_at_least_observed": family_tail,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group-sizes", default="10,15,20,30,50,80")
    parser.add_argument("--interaction-effects", default="0.0,0.4,0.7,1.0")
    parser.add_argument("--paired-correlations", default="0.0,0.5,0.8")
    parser.add_argument("--composition-imbalances", default="0.0,0.5")
    parser.add_argument("--composition-reliabilities", default="1.0,0.7")
    parser.add_argument("--replicates-per-seed", type=int, default=250)
    parser.add_argument("--seeds", default=",".join(map(str, DEFAULT_SEEDS)))
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    group_sizes = csv_numbers(args.group_sizes, int)
    effects = csv_numbers(args.interaction_effects, float)
    correlations = csv_numbers(args.paired_correlations, float)
    imbalances = csv_numbers(args.composition_imbalances, float)
    reliabilities = csv_numbers(args.composition_reliabilities, float)
    seeds = csv_numbers(args.seeds, int)
    if len(seeds) < 2:
        raise SystemExit("At least two seeds are required")
    if min(group_sizes) < 10:
        raise SystemExit("P2 group sizes below the V54 eligibility floor are not allowed")
    if not all(0 <= value < 1 for value in correlations):
        raise SystemExit("Paired correlations must be in [0,1)")
    if not all(0 < value <= 1 for value in reliabilities):
        raise SystemExit("Composition reliabilities must be in (0,1]")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    config = {
        "synthetic": True,
        "group_sizes_per_outcome_per_compartment": group_sizes,
        "interaction_effects_sd": effects,
        "paired_residual_correlations": correlations,
        "composition_imbalances": imbalances,
        "composition_reliabilities": reliabilities,
        "score_composition_coefficient": 0.6,
        "common_outcome_effect": 0.3,
        "replicates_per_seed": args.replicates_per_seed,
        "seeds": seeds,
        "alpha": args.alpha,
        "analysis_routes": ["unadjusted", "composition_adjusted"],
        "boundary": "Synthetic P2 method behavior only; not a biological or localization claim.",
    }
    (args.output_dir / "simulation_config.json").write_text(
        json.dumps(config, indent=2) + "\n"
    )

    rows = []
    unique_cohorts = 0
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for group_n in group_sizes:
            for effect in effects:
                for imbalance in imbalances:
                    for reliability in reliabilities:
                        for correlation in correlations:
                            route_rows = simulate_paired(
                                rng=rng,
                                n_per_group=group_n,
                                interaction_effect=effect,
                                residual_correlation=correlation,
                                composition_imbalance=imbalance,
                                composition_reliability=reliability,
                                alpha=args.alpha,
                                replicates=args.replicates_per_seed,
                            )
                            unique_cohorts += args.replicates_per_seed
                            for route_row in route_rows:
                                rows.append(
                                    {
                                        "seed": seed,
                                        "design": "paired",
                                        "n_per_outcome_group_per_compartment": group_n,
                                        "n_unique_subjects": 2 * group_n,
                                        "n_samples": 4 * group_n,
                                        "interaction_effect_sd": effect,
                                        "paired_residual_correlation": correlation,
                                        "composition_imbalance": imbalance,
                                        "composition_reliability": reliability,
                                        "alpha": args.alpha,
                                        **route_row,
                                    }
                                )
                        route_rows = simulate_unpaired(
                            rng=rng,
                            n_per_group=group_n,
                            interaction_effect=effect,
                            composition_imbalance=imbalance,
                            composition_reliability=reliability,
                            alpha=args.alpha,
                            replicates=args.replicates_per_seed,
                        )
                        unique_cohorts += args.replicates_per_seed
                        for route_row in route_rows:
                            rows.append(
                                {
                                    "seed": seed,
                                    "design": "unpaired",
                                    "n_per_outcome_group_per_compartment": group_n,
                                    "n_unique_subjects": 4 * group_n,
                                    "n_samples": 4 * group_n,
                                    "interaction_effect_sd": effect,
                                    "paired_residual_correlation": 0.0,
                                    "composition_imbalance": imbalance,
                                    "composition_reliability": reliability,
                                    "alpha": args.alpha,
                                    **route_row,
                                }
                            )
    seed_frame = pd.DataFrame(rows)
    seed_frame.to_csv(args.output_dir / "seed_results.tsv", sep="\t", index=False)
    grid = aggregate(seed_frame)
    grid.to_csv(args.output_dir / "power_grid.tsv", sep="\t", index=False)
    null = grid.loc[grid["interaction_effect_sd"].eq(0)].copy()
    null.to_csv(args.output_dir / "null_calibration_grid.tsv", sep="\t", index=False)
    minimum = minimum_n(grid)
    minimum.to_csv(args.output_dir / "minimum_group_n.tsv", sep="\t", index=False)

    adjusted_perfect = null.loc[
        null["analysis_route"].eq("composition_adjusted")
        & null["composition_reliability"].eq(1.0)
    ]
    adjusted_noisy_imbalanced = null.loc[
        null["analysis_route"].eq("composition_adjusted")
        & null["composition_reliability"].eq(0.7)
        & null["composition_imbalance"].gt(0)
    ]
    unadjusted_imbalanced = null.loc[
        null["analysis_route"].eq("unadjusted")
        & null["composition_imbalance"].gt(0)
    ]
    calibration = [
        null_family_summary(adjusted_perfect, "adjusted_perfect_composition"),
        null_family_summary(
            null.loc[
                null["analysis_route"].eq("composition_adjusted")
                & null["composition_reliability"].eq(0.7)
                & null["composition_imbalance"].eq(0)
            ],
            "adjusted_noisy_composition_without_imbalance",
        ),
        null_family_summary(
            adjusted_noisy_imbalanced, "adjusted_noisy_composition_with_imbalance"
        ),
        null_family_summary(unadjusted_imbalanced, "unadjusted_with_composition_imbalance"),
    ]
    pd.DataFrame(calibration).to_csv(
        args.output_dir / "calibration_families.tsv", sep="\t", index=False
    )
    adjusted_minimum = minimum.loc[minimum["analysis_route"].eq("composition_adjusted")]
    trustworthy_adjusted = adjusted_minimum.loc[
        adjusted_minimum["composition_reliability"].eq(1.0)
        | adjusted_minimum["composition_imbalance"].eq(0)
    ]
    residual_confounded = adjusted_minimum.loc[
        adjusted_minimum["composition_reliability"].eq(0.7)
        & adjusted_minimum["composition_imbalance"].gt(0)
    ]
    trusted_threshold_rows = []
    for (design, effect), group in trustworthy_adjusted.groupby(
        ["design", "interaction_effect_sd"], sort=True
    ):
        reached = group.loc[group["minimum_group_n_reaching_80pct"] != "not_reached"]
        trusted_threshold_rows.append(
            {
                "design": design,
                "interaction_effect_sd": effect,
                "n_calibrated_scenarios": len(group),
                "n_reaching_80pct": len(reached),
                "smallest_group_n_reaching_80pct": (
                    "not_reached"
                    if reached.empty
                    else int(reached["minimum_group_n_reaching_80pct"].astype(int).min())
                ),
                "minimum_power_at_group_n_80": float(group["power_at_largest_group_n"].min()),
                "maximum_power_at_group_n_80": float(group["power_at_largest_group_n"].max()),
            }
        )
    pd.DataFrame(trusted_threshold_rows).to_csv(
        args.output_dir / "trusted_threshold_summary.tsv", sep="\t", index=False
    )
    summary = {
        "purpose": "Synthetic P2 direct compartment-interaction power design; no biological claim",
        "synthetic": True,
        "n_unique_simulated_cohorts": unique_cohorts,
        "n_route_evaluations": int(seed_frame["n_simulated_cohorts"].sum()),
        "n_aggregate_route_cells": len(grid),
        "calibration_families": calibration,
        "trustworthy_adjusted_nonnull_scenarios_reaching_80pct": int(
            (trustworthy_adjusted["minimum_group_n_reaching_80pct"] != "not_reached").sum()
        ),
        "trustworthy_adjusted_nonnull_scenarios": len(trustworthy_adjusted),
        "residual_confounded_scenarios_reaching_80pct_not_interpreted_as_power": int(
            (residual_confounded["minimum_group_n_reaching_80pct"] != "not_reached").sum()
        ),
        "residual_confounded_scenarios": len(residual_confounded),
        "verdict": "P2_ROUTE_CONDITIONALLY_READY_REQUIRES_HIGH_FIDELITY_COMPOSITION",
        "boundary": (
            "All values arise from seeded synthetic assumptions. They are method behavior, "
            "not empirical MS compartment effects or localization evidence."
        ),
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = [
        "# V54 P2 Compartment-Interaction Power Design",
        "",
        "All outputs are seeded synthetic method behavior. They are not biological",
        "evidence and do not estimate compartment effects in MS.",
        "",
        f"The grid generated {unique_cohorts:,} unique synthetic cohorts and",
        f"{summary['n_route_evaluations']:,} route evaluations. Each used a direct",
        "outcome-by-compartment interaction; no difference-of-significance rule was used.",
        "",
        "## Null Calibration Families",
        "",
        "| family | cells | median | maximum | max Wilson CI | family max-tail |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for family in calibration:
        report.append(
            f"| {family['label']} | {family['n_cells']} | {family['median']:.3f} | "
            f"{family['maximum']:.3f} | {family['maximum_ci_low']:.3f}-"
            f"{family['maximum_ci_high']:.3f} | "
            f"{family['binomial_reference_probability_maximum_at_least_observed']:.3f} |"
        )
    report.extend(
        [
            "",
            "## Planning Boundary",
            "",
            f"Within calibration-eligible regimes, the composition-adjusted route "
            f"reached the 80% criterion in "
            f"{summary['trustworthy_adjusted_nonnull_scenarios_reaching_80pct']}/"
            f"{summary['trustworthy_adjusted_nonnull_scenarios']} assumption scenarios.",
            f"The {summary['residual_confounded_scenarios_reaching_80pct_not_interpreted_as_power']}/"
            f"{summary['residual_confounded_scenarios']} apparent passes under noisy measured "
            "composition plus true imbalance are not interpreted as power because that null",
            "family is miscalibrated.",
            "`minimum_group_n.tsv` reports the exact conditional thresholds. A real P2",
            "package must rerun this design from blinded pairing, composition, outcome,",
            "and compartment metadata and must first pass P1 endpoint semantics.",
        ]
    )
    (args.output_dir / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
