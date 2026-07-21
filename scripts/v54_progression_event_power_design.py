#!/usr/bin/env python3
"""Simulate pre-data power for a generic frozen progression-event association."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.special import expit
from scipy.stats import norm


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_event_power_design"
DEFAULT_SEEDS = [54701, 54702, 54703]


def csv_numbers(value: str, cast: type) -> list[Any]:
    return [cast(item.strip()) for item in value.split(",") if item.strip()]


def calibrated_intercept(event_rate: float, beta: float) -> float:
    nodes, weights = np.polynomial.hermite.hermgauss(60)
    x = np.sqrt(2.0) * nodes
    weights = weights / np.sqrt(np.pi)
    low, high = -15.0, 15.0
    for _ in range(80):
        middle = (low + high) / 2.0
        mean = float(np.sum(weights * expit(middle + beta * x)))
        if mean < event_rate:
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


def wilson(successes: int, total: int, confidence: float = 0.95) -> tuple[float, float]:
    if total <= 0:
        return np.nan, np.nan
    z = norm.ppf(1 - (1 - confidence) / 2)
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    half = z * np.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return float(center - half), float(center + half)


def simulate_cell(
    *,
    rng: np.random.Generator,
    n: int,
    event_rate: float,
    odds_ratio: float,
    missing_rate: float,
    molecular_repeats: int,
    measurement_reliability: float,
    label_noise: float,
    alpha: float,
    replicates: int,
) -> dict[str, Any]:
    beta_true = float(np.log(odds_ratio))
    intercept = calibrated_intercept(event_rate, beta_true)
    latent = rng.normal(size=(replicates, n))
    observed_sum = np.zeros_like(latent)
    for _ in range(molecular_repeats):
        noise = rng.normal(size=(replicates, n))
        observed_sum += (
            np.sqrt(measurement_reliability) * latent
            + np.sqrt(1 - measurement_reliability) * noise
        )
    observed = observed_sum / molecular_repeats
    probability = expit(intercept + beta_true * latent)
    outcome = rng.random((replicates, n)) < probability
    if label_noise > 0:
        outcome ^= rng.random((replicates, n)) < label_noise
    included = rng.random((replicates, n)) >= missing_rate
    weights = included.astype(float)
    usable_n = weights.sum(axis=1)
    events = (weights * outcome).sum(axis=1)
    nonevents = usable_n - events

    mean = np.divide(
        (weights * observed).sum(axis=1),
        usable_n,
        out=np.zeros(replicates),
        where=usable_n > 0,
    )
    centered = observed - mean[:, None]
    variance = np.divide(
        (weights * centered * centered).sum(axis=1),
        np.maximum(usable_n - 1, 1),
    )
    sd = np.sqrt(variance)
    x = np.divide(
        centered,
        sd[:, None],
        out=np.zeros_like(centered),
        where=sd[:, None] > 0,
    )
    valid = (usable_n >= 20) & (events >= 5) & (nonevents >= 5) & (sd > 0)

    b0 = np.log(np.clip(events + 0.5, 1e-6, None) / np.clip(nonevents + 0.5, 1e-6, None))
    b1 = np.zeros(replicates)
    determinant = np.full(replicates, np.nan)
    h00 = np.full(replicates, np.nan)
    for _ in range(30):
        fitted = expit(b0[:, None] + b1[:, None] * x)
        residual = weights * (outcome - fitted)
        information_weight = weights * fitted * (1 - fitted)
        g0 = residual.sum(axis=1)
        g1 = (residual * x).sum(axis=1)
        h00 = information_weight.sum(axis=1)
        h01 = (information_weight * x).sum(axis=1)
        h11 = (information_weight * x * x).sum(axis=1)
        determinant = h00 * h11 - h01 * h01
        stable = valid & (determinant > 1e-10) & np.isfinite(determinant)
        delta0 = np.zeros(replicates)
        delta1 = np.zeros(replicates)
        delta0[stable] = (h11[stable] * g0[stable] - h01[stable] * g1[stable]) / determinant[stable]
        delta1[stable] = (-h01[stable] * g0[stable] + h00[stable] * g1[stable]) / determinant[stable]
        b0[stable] = np.clip(b0[stable] + delta0[stable], -20, 20)
        b1[stable] = np.clip(b1[stable] + delta1[stable], -20, 20)
        if np.max(np.abs(delta0[stable]), initial=0) < 1e-8 and np.max(
            np.abs(delta1[stable]), initial=0
        ) < 1e-8:
            break

    fitted = expit(b0[:, None] + b1[:, None] * x)
    information_weight = weights * fitted * (1 - fitted)
    h00 = information_weight.sum(axis=1)
    h01 = (information_weight * x).sum(axis=1)
    h11 = (information_weight * x * x).sum(axis=1)
    determinant = h00 * h11 - h01 * h01
    stable = valid & (determinant > 1e-10) & np.isfinite(b1)
    se = np.full(replicates, np.nan)
    se[stable] = np.sqrt(h00[stable] / determinant[stable])
    z = np.divide(b1, se, out=np.full(replicates, np.nan), where=se > 0)
    p_value = 2 * norm.sf(np.abs(z))
    if odds_ratio == 1.0:
        conclusive = stable & (p_value <= alpha)
    else:
        conclusive = stable & (p_value <= alpha) & (b1 > 0)
    successes = int(conclusive.sum())
    ci_low, ci_high = wilson(successes, replicates)
    stable_beta = b1[stable]
    return {
        "n_requested": n,
        "event_rate_target": event_rate,
        "odds_ratio_per_latent_sd": odds_ratio,
        "missing_rate": missing_rate,
        "molecular_repeats": molecular_repeats,
        "measurement_reliability_per_repeat": measurement_reliability,
        "label_noise": label_noise,
        "alpha": alpha,
        "n_simulated_cohorts": replicates,
        "n_valid_fits": int(stable.sum()),
        "valid_fit_rate": float(stable.mean()),
        "median_usable_n": float(np.median(usable_n)),
        "median_events": float(np.median(events)),
        "conclusive_count": successes,
        "conclusive_probability": successes / replicates,
        "conclusive_probability_ci_low": ci_low,
        "conclusive_probability_ci_high": ci_high,
        "median_fitted_log_odds_per_observed_sd": (
            float(np.median(stable_beta)) if stable_beta.size else np.nan
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-sizes", default="40,60,80,120,160,240")
    parser.add_argument("--event-rates", default="0.15,0.30")
    parser.add_argument("--odds-ratios", default="1.0,1.25,1.5,2.0")
    parser.add_argument("--missing-rates", default="0.0,0.20")
    parser.add_argument("--molecular-repeats", default="1,2")
    parser.add_argument("--measurement-reliability", type=float, default=0.70)
    parser.add_argument("--label-noise", type=float, default=0.0)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--replicates-per-seed", type=int, default=500)
    parser.add_argument("--seeds", default=",".join(map(str, DEFAULT_SEEDS)))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    sample_sizes = csv_numbers(args.sample_sizes, int)
    event_rates = csv_numbers(args.event_rates, float)
    odds_ratios = csv_numbers(args.odds_ratios, float)
    missing_rates = csv_numbers(args.missing_rates, float)
    molecular_repeats = csv_numbers(args.molecular_repeats, int)
    seeds = csv_numbers(args.seeds, int)
    if not all(0 < value < 1 for value in event_rates):
        raise SystemExit("Event rates must be in (0,1)")
    if not all(value >= 1 for value in odds_ratios):
        raise SystemExit("Odds ratios must be >=1")
    if not 0 < args.measurement_reliability <= 1:
        raise SystemExit("Measurement reliability must be in (0,1]")
    if len(seeds) < 2:
        raise SystemExit("At least two seeds are required")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    config = {
        "synthetic": True,
        "sample_sizes": sample_sizes,
        "event_rates": event_rates,
        "odds_ratios": odds_ratios,
        "missing_rates": missing_rates,
        "molecular_repeats": molecular_repeats,
        "measurement_reliability": args.measurement_reliability,
        "label_noise": args.label_noise,
        "alpha": args.alpha,
        "replicates_per_seed": args.replicates_per_seed,
        "seeds": seeds,
        "primary_test": "two-sided single-predictor logistic Wald test; positive sign required under OR>1",
        "minimum_valid_counts": "usable n>=20 and at least 5 events and 5 non-events",
        "boundary": "Method-design assumptions only; not an empirical MS effect or biological claim.",
    }
    (args.output_dir / "simulation_config.json").write_text(json.dumps(config, indent=2) + "\n")

    seed_rows = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for n in sample_sizes:
            for event_rate in event_rates:
                for odds_ratio in odds_ratios:
                    for missing_rate in missing_rates:
                        for repeats in molecular_repeats:
                            result = simulate_cell(
                                rng=rng,
                                n=n,
                                event_rate=event_rate,
                                odds_ratio=odds_ratio,
                                missing_rate=missing_rate,
                                molecular_repeats=repeats,
                                measurement_reliability=args.measurement_reliability,
                                label_noise=args.label_noise,
                                alpha=args.alpha,
                                replicates=args.replicates_per_seed,
                            )
                            seed_rows.append({"seed": seed, **result})
    seed_frame = pd.DataFrame(seed_rows)
    seed_frame.to_csv(args.output_dir / "seed_results.tsv", sep="\t", index=False)

    group_columns = [
        "n_requested", "event_rate_target", "odds_ratio_per_latent_sd",
        "missing_rate", "molecular_repeats", "measurement_reliability_per_repeat",
        "label_noise", "alpha",
    ]
    aggregate_rows = []
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
                "median_events_across_seeds": float(group["median_events"].median()),
                "conclusive_probability": successes / total,
                "conclusive_probability_ci_low": ci_low,
                "conclusive_probability_ci_high": ci_high,
                "minimum_seed_probability": float(group["conclusive_probability"].min()),
                "maximum_seed_probability": float(group["conclusive_probability"].max()),
            }
        )
        aggregate_rows.append(row)
    grid = pd.DataFrame(aggregate_rows)
    grid.to_csv(args.output_dir / "power_grid.tsv", sep="\t", index=False)

    null = grid.loc[grid["odds_ratio_per_latent_sd"].eq(1.0)].copy()
    null.to_csv(args.output_dir / "null_false_positive_grid.tsv", sep="\t", index=False)
    min_rows = []
    scenario_columns = [
        "event_rate_target", "odds_ratio_per_latent_sd", "missing_rate",
        "molecular_repeats", "measurement_reliability_per_repeat", "label_noise", "alpha",
    ]
    nonnull = grid.loc[grid["odds_ratio_per_latent_sd"].gt(1.0)]
    for keys, group in nonnull.groupby(scenario_columns, sort=True, dropna=False):
        ordered = group.sort_values("n_requested")
        reached = ordered.loc[
            ordered["conclusive_probability"].ge(0.80)
            & ordered["minimum_seed_probability"].ge(0.75)
        ]
        row = dict(zip(scenario_columns, keys))
        if reached.empty:
            row.update(
                {
                    "minimum_n_reaching_80pct": "not_reached",
                    "power_at_largest_n": float(ordered.iloc[-1]["conclusive_probability"]),
                    "largest_n_simulated": int(ordered.iloc[-1]["n_requested"]),
                }
            )
        else:
            first = reached.iloc[0]
            row.update(
                {
                    "minimum_n_reaching_80pct": int(first["n_requested"]),
                    "power_at_largest_n": float(ordered.iloc[-1]["conclusive_probability"]),
                    "largest_n_simulated": int(ordered.iloc[-1]["n_requested"]),
                }
            )
        min_rows.append(row)
    minimum = pd.DataFrame(min_rows)
    minimum.to_csv(args.output_dir / "minimum_n_by_assumption.tsv", sep="\t", index=False)

    null_max = float(null["conclusive_probability"].max())
    null_median = float(null["conclusive_probability"].median())
    reached_count = int((minimum["minimum_n_reaching_80pct"] != "not_reached").sum())
    summary = {
        "purpose": "Synthetic pre-data progression-event power design; no biological claim",
        "synthetic": True,
        "n_grid_cells": len(grid),
        "n_seed_cells": len(seed_frame),
        "n_simulated_cohorts": int(seed_frame["n_simulated_cohorts"].sum()),
        "n_seeds": len(seeds),
        "null_false_positive_median": null_median,
        "null_false_positive_maximum": null_max,
        "n_nonnull_scenarios_reaching_80pct": reached_count,
        "n_nonnull_scenarios": len(minimum),
        "verdict": "ASSUMPTION_GRID_READY_FOR_RECEIVED_COHORT_PARAMETERIZATION",
        "boundary": (
            "Power values are conditional on explicit synthetic odds ratios, event rates, "
            "measurement reliability, missingness, and model correctness. They are not an "
            "empirical MS effect estimate or a claim that a cohort will validate a state."
        ),
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    notable = minimum.sort_values(
        ["odds_ratio_per_latent_sd", "event_rate_target", "missing_rate", "molecular_repeats"]
    )
    report = [
        "# V54 Progression-Event Power Design",
        "",
        "> Later method audits: `analysis/v54_progression_power_calibration_audit/`",
        "> finds the 0.060 null maximum compatible with finite-grid variation, while",
        "> `analysis/v54_progression_power_label_noise/` shows material power loss at",
        "> 5% and 10% symmetric label error. Both are synthetic method behavior.",
        "",
        "All outputs are synthetic method behavior, not biological evidence.",
        "",
        f"The default grid simulated {summary['n_simulated_cohorts']:,} cohorts across "
        f"{len(grid)} cells and {len(seeds)} seeds. Median null false-positive rate was "
        f"`{null_median:.3f}` and the maximum grid-cell null rate was `{null_max:.3f}`.",
        "",
        "The grid models one frozen standardized molecular predictor of a binary",
        "progression event. It is deliberately generic: a received cohort must replace",
        "the assumed event rate, missingness, reliability, and analysis route before any",
        "score is viewed.",
        "",
        "## Minimum N Under Explicit Assumptions",
        "",
        "`minimum_n_by_assumption.tsv` reports the first simulated sample size with",
        "aggregate conclusive probability >=0.80 and every seed >=0.75. `not_reached`",
        "means the default grid through n=240 did not meet that method-design threshold.",
        "",
        "| event rate | OR / latent SD | missing | repeats | minimum n | power at n=240 |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for row in notable.itertuples(index=False):
        report.append(
            f"| {row.event_rate_target:.2f} | {row.odds_ratio_per_latent_sd:.2f} | "
            f"{row.missing_rate:.2f} | {row.molecular_repeats} | "
            f"{row.minimum_n_reaching_80pct} | {row.power_at_largest_n:.3f} |"
        )
    report.extend(
        [
            "",
            "These values cannot be used as a universal progression cohort target. The",
            "true effect is unknown, event definitions differ, and the model omits many",
            "real longitudinal complexities. The durable output is the parameterized",
            "interface and calibrated null, to be rerun on the blinded receipt inventory.",
        ]
    )
    (args.output_dir / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
