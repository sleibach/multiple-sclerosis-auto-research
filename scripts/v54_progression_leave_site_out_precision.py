#!/usr/bin/env python3
"""Seeded synthetic leave-site-out and per-site precision audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import binom, chi2, norm

import v54_progression_multisite_transportability as base


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_leave_site_out_precision"
SEEDS = (55431, 55433, 55439)
N_VALUES = (450, 600, 900, 1500)
EVENT_PROBABILITIES = (0.15, 0.30)
ALLOCATIONS = ("balanced", "imbalanced_60_30_10")
REPLICATES = 400
RELIABILITY = 0.70
SCORE_MISSING = 0.10
ALPHA = 0.05
SITE_SCALES = np.array([0.50, 1.00, 2.00])
SITE_OFFSETS = np.array([-1.00, 0.00, 1.00])
EFFECT_PATTERNS = {
    "null": np.array([1.0, 1.0, 1.0]),
    "homogeneous_hr13": np.array([1.3, 1.3, 1.3]),
    "homogeneous_hr15": np.array([1.5, 1.5, 1.5]),
    "one_site_only_hr15": np.array([1.5, 1.0, 1.0]),
    "one_site_reversed_hr15": np.array([1.5, 1.5, 1 / 1.5]),
}


def simulate_cell(
    rng: np.random.Generator,
    n: int,
    event_probability: float,
    allocation: str,
    effect_pattern: str,
) -> dict[str, Any]:
    site = base.site_vector(n, base.ALLOCATIONS[allocation])
    true_state = rng.normal(size=(REPLICATES, n))
    frailty = rng.normal(size=(REPLICATES, n))
    site_hr = EFFECT_PATTERNS[effect_pattern][site]
    multiplier = base.SITE_BASELINE_MULTIPLIERS[site][None, :] * np.exp(
        np.log(site_hr)[None, :] * true_state + 0.70 * frailty
    )
    baseline = base.calibrate_scale(multiplier, event_probability)
    event_time = -np.log(np.clip(rng.random(true_state.shape), 1e-12, 1.0)) / (
        baseline[:, None] * multiplier
    )
    event = event_time <= 1.0
    observed_time = np.minimum(event_time, 1.0)
    measured = np.sqrt(RELIABILITY) * true_state + np.sqrt(1 - RELIABILITY) * rng.normal(
        size=true_state.shape
    )
    assay_score = SITE_OFFSETS[site][None, :] + SITE_SCALES[site][None, :] * measured
    included = rng.random(true_state.shape) >= SCORE_MISSING

    counters = {
        "valid": 0,
        "global_positive": 0,
        "all_site_sign": 0,
        "all_site_ci_positive": 0,
        "all_leave_site_out_ci_positive": 0,
        "sign_transport": 0,
        "strict_precision": 0,
    }
    minimum_events: list[int] = []
    widest_half_widths: list[float] = []
    minimum_site_z_values: list[float] = []
    for replicate in range(REPLICATES):
        site_u: list[float] = []
        site_i: list[float] = []
        site_events: list[int] = []
        valid_replicate = True
        for site_id in range(3):
            selected = (site == site_id) & included[replicate]
            values = assay_score[replicate, selected]
            if len(values) < 20:
                valid_replicate = False
                break
            sd = float(np.std(values, ddof=1))
            if not np.isfinite(sd) or sd <= 0:
                valid_replicate = False
                break
            values = (values - values.mean()) / sd
            current_event = event[replicate, selected]
            current_time = observed_time[replicate, selected]
            site_events.append(int(current_event.sum()))
            u_value, i_value = base.cox_score_components(
                values,
                current_time,
                current_event,
                np.zeros(len(values), dtype=np.int8),
            )
            site_u.append(u_value)
            site_i.append(i_value)
        if not valid_replicate:
            continue
        site_u_array = np.asarray(site_u)
        site_i_array = np.asarray(site_i)
        if np.any(site_i_array <= 1e-12):
            continue
        global_z, global_p, global_beta = base.component_test(
            float(site_u_array.sum()), float(site_i_array.sum())
        )
        if not np.isfinite(global_p):
            continue
        site_beta = site_u_array / site_i_array
        site_se = 1 / np.sqrt(site_i_array)
        site_lower = site_beta - norm.ppf(0.975) * site_se
        leave_out_lower = []
        for omitted in range(3):
            retained = np.arange(3) != omitted
            _, _, loo_beta = base.component_test(
                float(site_u_array[retained].sum()),
                float(site_i_array[retained].sum()),
            )
            loo_se = 1 / np.sqrt(float(site_i_array[retained].sum()))
            leave_out_lower.append(loo_beta - norm.ppf(0.975) * loo_se)
        q_value = float(np.sum(site_i_array * (site_beta - global_beta) ** 2))
        heterogeneity_p = float(chi2.sf(q_value, 2))

        counters["valid"] += 1
        global_positive = global_p <= ALPHA and global_z > 0
        all_site_sign = bool(np.all(site_beta > 0))
        all_site_ci = bool(np.all(site_lower > 0))
        all_loo_ci = bool(np.all(np.asarray(leave_out_lower) > 0))
        enough_events = min(site_events) >= 10
        homogeneous = heterogeneity_p >= ALPHA
        sign_transport = (
            global_positive and all_site_sign and all_loo_ci and enough_events and homogeneous
        )
        strict_precision = sign_transport and all_site_ci
        counters["global_positive"] += int(global_positive)
        counters["all_site_sign"] += int(all_site_sign)
        counters["all_site_ci_positive"] += int(all_site_ci)
        counters["all_leave_site_out_ci_positive"] += int(all_loo_ci)
        counters["sign_transport"] += int(sign_transport)
        counters["strict_precision"] += int(strict_precision)
        minimum_events.append(min(site_events))
        widest_half_widths.append(float(np.max(norm.ppf(0.975) * site_se)))
        minimum_site_z_values.append(float(np.min(site_beta / site_se)))

    result: dict[str, Any] = {
        "n_requested": n,
        "event_probability": event_probability,
        "allocation": allocation,
        "effect_pattern": effect_pattern,
        "n_simulated_cohorts": REPLICATES,
        "n_valid_fits": counters["valid"],
        "median_minimum_site_events": base.finite_median(minimum_events),
        "median_widest_site_ci_half_width": base.finite_median(widest_half_widths),
        "median_minimum_site_z": base.finite_median(minimum_site_z_values),
    }
    for name in [
        "global_positive",
        "all_site_sign",
        "all_site_ci_positive",
        "all_leave_site_out_ci_positive",
        "sign_transport",
        "strict_precision",
    ]:
        count = counters[name]
        low, high = base.wilson(count, REPLICATES)
        result[f"{name}_count"] = count
        result[f"{name}_probability"] = count / REPLICATES
        result[f"{name}_ci_low"] = low
        result[f"{name}_ci_high"] = high
    return result


def aggregate(frame: pd.DataFrame) -> pd.DataFrame:
    keys = ["n_requested", "event_probability", "allocation", "effect_pattern"]
    rows = []
    probability_names = [
        "global_positive",
        "all_site_sign",
        "all_site_ci_positive",
        "all_leave_site_out_ci_positive",
        "sign_transport",
        "strict_precision",
    ]
    for values, group in frame.groupby(keys, sort=True):
        row = dict(zip(keys, values))
        total = int(group.n_simulated_cohorts.sum())
        row["n_simulated_cohorts"] = total
        row["n_valid_fits"] = int(group.n_valid_fits.sum())
        for name in probability_names:
            count = int(group[f"{name}_count"].sum())
            low, high = base.wilson(count, total)
            row[f"{name}_count"] = count
            row[f"{name}_probability"] = count / total
            row[f"{name}_ci_low"] = low
            row[f"{name}_ci_high"] = high
            row[f"minimum_seed_{name}_probability"] = float(
                group[f"{name}_probability"].min()
            )
        for name in [
            "median_minimum_site_events",
            "median_widest_site_ci_half_width",
            "median_minimum_site_z",
        ]:
            row[f"{name}_across_seeds"] = base.finite_median(group[name])
        rows.append(row)
    return pd.DataFrame(rows)


def null_calibration(grid: pd.DataFrame, metric: str) -> dict[str, Any]:
    null = grid.loc[grid.effect_pattern.eq("null")]
    probability = f"{metric}_probability"
    count_column = f"{metric}_count"
    ci_low = f"{metric}_ci_low"
    maximum = null.loc[null[probability].idxmax()]
    single_tail = float(
        binom.sf(int(maximum[count_column]) - 1, int(maximum.n_simulated_cohorts), ALPHA)
    )
    family_tail = float(1 - (1 - single_tail) ** len(null))
    strict = bool((null[ci_low] > ALPHA).any())
    invalid = bool(strict and family_tail < ALPHA)
    return {
        "metric": metric,
        "n_null_cells": len(null),
        "maximum_probability": float(maximum[probability]),
        "maximum_ci_low": float(maximum[ci_low]),
        "maximum_ci_high": float(maximum[f"{metric}_ci_high"]),
        "family_tail_probability": family_tail,
        "strict_cell_flag": strict,
        "invalid_null_family": invalid,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    config = {
        "synthetic": True,
        "seeds": list(SEEDS),
        "sample_sizes": list(N_VALUES),
        "event_probabilities": list(EVENT_PROBABILITIES),
        "allocations": list(ALLOCATIONS),
        "effect_patterns": {key: value.tolist() for key, value in EFFECT_PATTERNS.items()},
        "replicates_per_seed_cell": REPLICATES,
        "precision_gate": "global positive; every site CI lower > 0; every leave-site-out CI lower > 0; min site events >= 10; heterogeneity p >= 0.05",
        "boundary": "Seeded synthetic precision-method behavior only; no empirical MS effect, event rate, or universal sample-size claim.",
    }
    (OUT / "simulation_config.json").write_text(json.dumps(config, indent=2) + "\n")
    rows = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        for effect_pattern in EFFECT_PATTERNS:
            for n in N_VALUES:
                for event_probability in EVENT_PROBABILITIES:
                    for allocation in ALLOCATIONS:
                        row = simulate_cell(rng, n, event_probability, allocation, effect_pattern)
                        row["seed"] = seed
                        rows.append(row)
    seed_frame = pd.DataFrame(rows)
    seed_frame.to_csv(OUT / "seed_grid.tsv", sep="\t", index=False)
    grid = aggregate(seed_frame)
    grid.to_csv(OUT / "aggregate_grid.tsv", sep="\t", index=False)

    calibrations = [
        null_calibration(grid, "global_positive"),
        null_calibration(grid, "strict_precision"),
    ]
    pd.DataFrame(calibrations).to_csv(OUT / "null_calibration.tsv", sep="\t", index=False)
    null_valid = not any(item["invalid_null_family"] for item in calibrations)

    controls = grid.loc[grid.effect_pattern.isin(["one_site_only_hr15", "one_site_reversed_hr15"])].pivot_table(
        index=["n_requested", "event_probability", "allocation"],
        columns="effect_pattern",
        values="strict_precision_probability",
    ).reset_index()
    homogeneous = grid.loc[grid.effect_pattern.str.startswith("homogeneous")].copy()
    readiness = homogeneous.merge(
        controls,
        on=["n_requested", "event_probability", "allocation"],
        how="left",
        validate="many_to_one",
    )
    readiness["precision_ready"] = (
        null_valid
        & readiness.strict_precision_probability.ge(0.80)
        & readiness.minimum_seed_strict_precision_probability.ge(0.75)
        & readiness.one_site_only_hr15.le(0.05)
        & readiness.one_site_reversed_hr15.le(0.05)
    )
    readiness.to_csv(OUT / "precision_readiness.tsv", sep="\t", index=False)

    minimum_rows = []
    for pattern in ("homogeneous_hr13", "homogeneous_hr15"):
        for event_probability in EVENT_PROBABILITIES:
            for allocation in ALLOCATIONS:
                current = readiness.loc[
                    readiness.effect_pattern.eq(pattern)
                    & readiness.event_probability.eq(event_probability)
                    & readiness.allocation.eq(allocation)
                ].sort_values("n_requested")
                passed = current.loc[current.precision_ready]
                minimum_rows.append(
                    {
                        "effect_pattern": pattern,
                        "event_probability": event_probability,
                        "allocation": allocation,
                        "minimum_n_precision_ready": int(passed.iloc[0].n_requested) if len(passed) else "not_reached",
                        "strict_probability_at_largest_n": float(current.iloc[-1].strict_precision_probability),
                        "median_minimum_site_events_at_largest_n": float(current.iloc[-1].median_minimum_site_events_across_seeds),
                        "median_widest_site_ci_half_width_at_largest_n": float(current.iloc[-1].median_widest_site_ci_half_width_across_seeds),
                    }
                )
    minimum = pd.DataFrame(minimum_rows)
    minimum.to_csv(OUT / "minimum_n.tsv", sep="\t", index=False)
    ready = readiness.loc[readiness.precision_ready]
    best = readiness.loc[readiness.strict_precision_probability.idxmax()]
    summary = {
        "purpose": "V54 synthetic leave-site-out and per-site precision audit; no biological claim",
        "synthetic": True,
        "n_unique_simulated_cohorts": len(SEEDS) * len(EFFECT_PATTERNS) * len(N_VALUES) * len(EVENT_PROBABILITIES) * len(ALLOCATIONS) * REPLICATES,
        "n_null_families_invalid": sum(item["invalid_null_family"] for item in calibrations),
        "n_precision_ready_designs": len(ready),
        "n_homogeneous_designs": len(readiness),
        "ready_designs": ready[["effect_pattern", "n_requested", "event_probability", "allocation"]].to_dict("records"),
        "best_tested_design": {
            "effect_pattern": best.effect_pattern,
            "n_requested": int(best.n_requested),
            "event_probability": float(best.event_probability),
            "allocation": best.allocation,
            "strict_precision_probability": float(best.strict_precision_probability),
            "minimum_seed_probability": float(best.minimum_seed_strict_precision_probability),
            "median_minimum_site_events": float(best.median_minimum_site_events_across_seeds),
            "median_widest_site_ci_half_width": float(best.median_widest_site_ci_half_width_across_seeds),
        },
        "maximum_false_precision_one_site_only": float(readiness.one_site_only_hr15.max()),
        "maximum_false_precision_one_site_reversed": float(readiness.one_site_reversed_hr15.max()),
        "verdict": "PER_SITE_PRECISION_REQUIRES_MORE_THAN_SIGN_CONSISTENCY",
        "boundary": "Synthetic precision-method behavior only; no empirical MS effect, event rate, or universal sample-size claim.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
