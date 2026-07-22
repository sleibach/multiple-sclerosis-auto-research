#!/usr/bin/env python3
"""Seeded synthetic audit of combined progression ascertainment mechanisms."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import binom

from v54_progression_event_time_assumption_robustness import (
    calibrate_scale,
    cox_score_test,
    finite_median,
    wilson,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_combined_ascertainment"
SEEDS = (54201, 54203, 54209)
N_VALUES = (180, 320, 450)
EVENT_PROBABILITIES = (0.15, 0.30)
MOLECULAR_HRS = (1.0, 1.5)
REPLICATES = 800
PROCESS_PROBABILITY = 0.10
RELIABILITY = 0.70
SCORE_MISSING = 0.10
ALPHA = 0.05
ROUTES = ("guarded_within_site_stratified", "naive_global_pooled")
STACKS = {
    "clean": ("none", "none", "none", "balanced"),
    "attendance_score_only": ("score", "none", "none", "balanced"),
    "death_risk_only": ("none", "risk", "none", "balanced"),
    "switch_score_only": ("none", "none", "score", "balanced"),
    "separable_all": ("score", "risk", "score", "balanced"),
    "attendance_weak_joint": ("weak_joint", "none", "none", "balanced"),
    "death_weak_joint": ("none", "weak_joint", "none", "balanced"),
    "switch_weak_joint": ("none", "none", "weak_joint", "balanced"),
    "weak_joint_all": ("weak_joint", "weak_joint", "weak_joint", "balanced"),
    "weak_joint_all_site_linked": ("weak_joint", "weak_joint", "weak_joint", "score_linked_60_30_10"),
}
COMBINATIONS = {
    "separable_all": ["attendance_score_only", "death_risk_only", "switch_score_only"],
    "weak_joint_all": ["attendance_weak_joint", "death_weak_joint", "switch_weak_joint"],
    "weak_joint_all_site_linked": ["attendance_weak_joint", "death_weak_joint", "switch_weak_joint"],
}


def process_lp(mode: str, score: np.ndarray, frailty: np.ndarray) -> np.ndarray:
    if mode == "none":
        return np.zeros_like(score)
    if mode == "score":
        return 0.8 * score
    if mode == "risk":
        return 0.8 * frailty
    if mode == "weak_joint":
        return 0.2 * score + 0.2 * frailty + 0.35 * score * frailty
    raise ValueError(mode)


def process_time(
    rng: np.random.Generator,
    mode: str,
    score: np.ndarray,
    frailty: np.ndarray,
) -> np.ndarray:
    if mode == "none":
        return np.full_like(score, np.inf)
    multiplier = np.exp(np.clip(process_lp(mode, score, frailty), -6, 6))
    baseline = calibrate_scale(multiplier, PROCESS_PROBABILITY)
    return -np.log(np.clip(rng.random(score.shape), 1e-12, 1.0)) / (
        baseline[:, None] * multiplier
    )


def assign_sites(
    rng: np.random.Generator, score: np.ndarray, mode: str
) -> np.ndarray:
    if mode == "balanced":
        return rng.integers(0, 3, size=score.shape, dtype=np.int8)
    if mode != "score_linked_60_30_10":
        raise ValueError(mode)
    order = np.argsort(score, axis=1)
    sites = np.empty(score.shape, dtype=np.int8)
    n = score.shape[1]
    cut_10 = int(round(0.10 * n))
    cut_40 = int(round(0.40 * n))
    rows = np.arange(score.shape[0])[:, None]
    sites[rows, order[:, :cut_10]] = 2
    sites[rows, order[:, cut_10:cut_40]] = 1
    sites[rows, order[:, cut_40:]] = 0
    return sites


def within_site_standardize(values: np.ndarray, sites: np.ndarray) -> np.ndarray:
    result = np.full(values.shape, np.nan)
    for replicate in range(values.shape[0]):
        for site in (0, 1, 2):
            selected = sites[replicate] == site
            subset = values[replicate, selected]
            sd = float(np.std(subset, ddof=1))
            if len(subset) >= 2 and np.isfinite(sd) and sd > 0:
                result[replicate, selected] = (subset - subset.mean()) / sd
    return result


def analyze(
    score: np.ndarray,
    time: np.ndarray,
    event: np.ndarray,
    included: np.ndarray,
    sites: np.ndarray,
    route: str,
) -> dict[str, Any]:
    significant = positive = negative = valid = 0
    z_values: list[float] = []
    beta_values: list[float] = []
    event_counts: list[int] = []
    usable_counts: list[int] = []
    for replicate in range(score.shape[0]):
        keep = included[replicate] & np.isfinite(score[replicate])
        events = int(event[replicate, keep].sum())
        usable = int(keep.sum())
        event_counts.append(events)
        usable_counts.append(usable)
        if usable < 20 or events < 10 or usable - events < 10:
            continue
        current = score[replicate, keep]
        if route == "naive_global_pooled":
            sd = float(np.std(current, ddof=1))
            if not np.isfinite(sd) or sd <= 0:
                continue
            current = (current - current.mean()) / sd
            strata = np.zeros(usable, dtype=np.int8)
        else:
            strata = sites[replicate, keep]
        z_value, p_value, beta = cox_score_test(
            current, time[replicate, keep], event[replicate, keep], strata
        )
        if not np.isfinite(p_value):
            continue
        valid += 1
        z_values.append(z_value)
        beta_values.append(beta)
        if p_value <= ALPHA:
            significant += 1
            positive += int(z_value > 0)
            negative += int(z_value < 0)
    low, high = wilson(significant, score.shape[0])
    return {
        "n_simulated_cohorts": score.shape[0],
        "n_valid_fits": valid,
        "significant_count": significant,
        "significant_probability": significant / score.shape[0],
        "significant_probability_ci_low": low,
        "significant_probability_ci_high": high,
        "positive_call_probability": positive / score.shape[0],
        "negative_call_probability": negative / score.shape[0],
        "median_z": finite_median(z_values),
        "median_one_step_log_hr": finite_median(beta_values),
        "median_events": float(np.median(event_counts)),
        "median_usable_n": float(np.median(usable_counts)),
    }


def simulate_cell(
    rng: np.random.Generator,
    stack: str,
    n: int,
    event_probability: float,
    molecular_hr: float,
    replicates: int,
) -> list[dict[str, Any]]:
    attendance_mode, death_mode, switch_mode, site_mode = STACKS[stack]
    latent_score = rng.normal(size=(replicates, n))
    frailty = rng.normal(size=(replicates, n))
    sites = assign_sites(rng, latent_score, site_mode)
    site_hr = np.array([1.50, 1.00, 0.67])[sites]
    event_multiplier = np.exp(
        np.log(molecular_hr) * latent_score + 0.70 * frailty
    ) * site_hr
    event_baseline = calibrate_scale(event_multiplier, event_probability)
    event_time = -np.log(np.clip(rng.random(latent_score.shape), 1e-12, 1.0)) / (
        event_baseline[:, None] * event_multiplier
    )
    attendance_time = process_time(rng, attendance_mode, latent_score, frailty)
    death_time = process_time(rng, death_mode, latent_score, frailty)
    switch_time = process_time(rng, switch_mode, latent_score, frailty)
    censor_time = np.minimum(np.minimum(attendance_time, death_time), switch_time)
    observed_time = np.minimum(np.minimum(event_time, censor_time), 1.0)
    observed_event = (event_time <= censor_time) & (event_time <= 1.0)

    base_score = np.sqrt(RELIABILITY) * latent_score + np.sqrt(1 - RELIABILITY) * rng.normal(
        size=latent_score.shape
    )
    assay_scale = np.array([0.50, 1.00, 2.00])[sites]
    assay_offset = np.array([-1.00, 0.00, 1.00])[sites]
    assay_score = assay_offset + assay_scale * base_score
    guarded_score = within_site_standardize(assay_score, sites)
    included = rng.random(latent_score.shape) >= SCORE_MISSING
    results = []
    for route, score in (
        ("guarded_within_site_stratified", guarded_score),
        ("naive_global_pooled", assay_score),
    ):
        row = analyze(score, observed_time, observed_event, included, sites, route)
        row.update(
            {
                "stack": stack,
                "attendance_mode": attendance_mode,
                "death_mode": death_mode,
                "switch_mode": switch_mode,
                "site_mode": site_mode,
                "route": route,
                "n_requested": n,
                "event_probability_before_ascertainment": event_probability,
                "molecular_progression_hr": molecular_hr,
            }
        )
        results.append(row)
    return results


def aggregate(frame: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "stack", "attendance_mode", "death_mode", "switch_mode", "site_mode",
        "route", "n_requested", "event_probability_before_ascertainment",
        "molecular_progression_hr",
    ]
    rows = []
    for values, group in frame.groupby(keys, sort=True, dropna=False):
        row = dict(zip(keys, values))
        total = int(group.n_simulated_cohorts.sum())
        significant = int(group.significant_count.sum())
        low, high = wilson(significant, total)
        row.update(
            {
                "n_simulated_cohorts": total,
                "n_valid_fits": int(group.n_valid_fits.sum()),
                "significant_count": significant,
                "significant_probability": significant / total,
                "significant_probability_ci_low": low,
                "significant_probability_ci_high": high,
                "minimum_seed_probability": float(group.significant_probability.min()),
                "maximum_seed_probability": float(group.significant_probability.max()),
                "positive_call_probability": float((group.positive_call_probability * group.n_simulated_cohorts).sum() / total),
                "negative_call_probability": float((group.negative_call_probability * group.n_simulated_cohorts).sum() / total),
                "median_z_across_seeds": finite_median(group.median_z.to_numpy()),
                "median_one_step_log_hr_across_seeds": finite_median(group.median_one_step_log_hr.to_numpy()),
                "median_events_across_seeds": float(group.median_events.median()),
                "median_usable_n_across_seeds": float(group.median_usable_n.median()),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def calibration(grid: pd.DataFrame) -> pd.DataFrame:
    null = grid.loc[grid.molecular_progression_hr.eq(1.0)]
    rows = []
    for (stack, route), group in null.groupby(["stack", "route"], sort=True):
        maximum = group.loc[group.significant_probability.idxmax()]
        count = int(maximum.significant_count)
        total = int(maximum.n_simulated_cohorts)
        single_tail = float(binom.sf(count - 1, total, ALPHA))
        family_tail = float(1 - (1 - single_tail) ** len(group))
        strict = bool((group.significant_probability_ci_low > ALPHA).any())
        invalid = bool(strict and family_tail < ALPHA)
        rows.append(
            {
                "stack": stack,
                "route": route,
                "n_null_cells": len(group),
                "median_null_probability": float(group.significant_probability.median()),
                "maximum_null_probability": float(maximum.significant_probability),
                "maximum_ci_low": float(maximum.significant_probability_ci_low),
                "maximum_ci_high": float(maximum.significant_probability_ci_high),
                "maximum_family_tail_probability": family_tail,
                "strict_cell_flag": strict,
                "strict_cell_flag_but_family_compatible": bool(strict and not invalid),
                "invalid_null_family": invalid,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, default=REPLICATES)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    config = {
        "synthetic": True,
        "seeds": list(SEEDS),
        "sample_sizes": list(N_VALUES),
        "event_probabilities_before_ascertainment": list(EVENT_PROBABILITIES),
        "molecular_progression_hrs": list(MOLECULAR_HRS),
        "replicates_per_cell_seed": args.replicates,
        "process_probability": PROCESS_PROBABILITY,
        "reliability": RELIABILITY,
        "score_missing": SCORE_MISSING,
        "alpha": ALPHA,
        "stacks": {key: list(value) for key, value in STACKS.items()},
        "routes": list(ROUTES),
        "boundary": "Seeded synthetic method behavior only; no empirical MS progression, ascertainment, or biological claim.",
    }
    (args.output_dir / "simulation_config.json").write_text(json.dumps(config, indent=2) + "\n")

    rows = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        for stack in STACKS:
            for n in N_VALUES:
                for event_probability in EVENT_PROBABILITIES:
                    for molecular_hr in MOLECULAR_HRS:
                        for row in simulate_cell(
                            rng, stack, n, event_probability, molecular_hr, args.replicates
                        ):
                            row["seed"] = seed
                            rows.append(row)
    seed_frame = pd.DataFrame(rows)
    seed_frame.to_csv(args.output_dir / "seed_grid.tsv", sep="\t", index=False)
    grid = aggregate(seed_frame)
    grid.to_csv(args.output_dir / "aggregate_grid.tsv", sep="\t", index=False)
    calibration_frame = calibration(grid)
    calibration_frame.to_csv(args.output_dir / "null_calibration.tsv", sep="\t", index=False)

    calibration_lookup = calibration_frame.set_index(["stack", "route"])
    compounding_rows = []
    for combined, constituents in COMBINATIONS.items():
        for route in ROUTES:
            combined_invalid = bool(calibration_lookup.loc[(combined, route), "invalid_null_family"])
            constituent_invalid = [
                bool(calibration_lookup.loc[(item, route), "invalid_null_family"])
                for item in constituents
            ]
            compounding_rows.append(
                {
                    "combined_stack": combined,
                    "route": route,
                    "constituents": ";".join(constituents),
                    "all_constituents_calibrated": not any(constituent_invalid),
                    "combined_invalid": combined_invalid,
                    "compounded_invalidity": combined_invalid and not any(constituent_invalid),
                }
            )
    compounding = pd.DataFrame(compounding_rows)
    compounding.to_csv(args.output_dir / "compounding_adjudication.tsv", sep="\t", index=False)
    invalid = calibration_frame.loc[calibration_frame.invalid_null_family]
    compounded = compounding.loc[compounding.compounded_invalidity]
    nonnull = grid.loc[grid.molecular_progression_hr.eq(1.5)].merge(
        calibration_frame[["stack", "route", "invalid_null_family"]],
        on=["stack", "route"],
    )
    calibrated_nonnull = nonnull.loc[~nonnull.invalid_null_family]
    summary = {
        "purpose": "V54 combined progression ascertainment synthetic audit; no biological claim",
        "synthetic": True,
        "n_unique_simulated_cohorts": len(SEEDS) * len(STACKS) * len(N_VALUES) * len(EVENT_PROBABILITIES) * len(MOLECULAR_HRS) * args.replicates,
        "n_route_evaluations": len(SEEDS) * len(STACKS) * len(N_VALUES) * len(EVENT_PROBABILITIES) * len(MOLECULAR_HRS) * args.replicates * len(ROUTES),
        "n_null_families": len(calibration_frame),
        "n_invalid_null_families": len(invalid),
        "invalid_null_families": [f"{row.stack}|{row.route}" for row in invalid.itertuples()],
        "n_compounded_invalidity_families": len(compounded),
        "compounded_invalidity_families": [f"{row.combined_stack}|{row.route}" for row in compounded.itertuples()],
        "n_calibrated_nonnull_cells": len(calibrated_nonnull),
        "n_calibrated_nonnull_cells_at_least_80pct": int((calibrated_nonnull.significant_probability >= 0.80).sum()),
        "verdict": "COMBINED_ASCERTAINMENT_CAN_INVALIDATE_BOUNDED_COMPONENTS" if len(compounded) else "NO_COMPOUND_INVALIDITY_DETECTED_IN_FROZEN_STACKS",
        "boundary": "Synthetic method behavior only; no empirical progression effect, ascertainment process, therapeutic target, or route to halting MS.",
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    report = [
        "# V54 Combined Progression Ascertainment Audit",
        "",
        "**Synthetic method behavior only. No patient data or biological claim.**",
        "",
        f"- Cohorts: `{summary['n_unique_simulated_cohorts']:,}`; route evaluations: `{summary['n_route_evaluations']:,}`.",
        f"- Invalid null families: `{summary['n_invalid_null_families']}/{summary['n_null_families']}`.",
        f"- Compounded-invalidity families: `{summary['n_compounded_invalidity_families']}`.",
        f"- Verdict: `{summary['verdict']}`.",
        "",
        "A calibrated stack bounds only this frozen generator. An invalid stack is a method warning, not evidence that any real MS cohort follows that ascertainment process.",
    ]
    (args.output_dir / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
