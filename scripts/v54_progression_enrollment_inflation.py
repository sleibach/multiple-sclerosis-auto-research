#!/usr/bin/env python3
"""Seeded synthetic enrollment-inflation audit for V54 progression design."""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_enrollment_inflation"
SEEDS = (54071, 54079, 54083)
REPLICATES = 5000
LOSS_RATES = (0.0, 0.1, 0.2)
EVENT_PROBABILITIES = (0.15, 0.30)
PER_SITE_CANDIDATES = tuple(range(150, 801, 5))
PASSIVE_TOTAL_CANDIDATES = tuple(range(450, 6001, 15))
SITE_SHARES = {
    "balanced_in_expectation": (1 / 3, 1 / 3, 1 / 3),
    "moderate_45_35_20": (0.45, 0.35, 0.20),
    "severe_60_30_10": (0.60, 0.30, 0.10),
}
TARGET_ANALYZABLE_TOTAL = 450
TARGET_ANALYZABLE_PER_SITE = 150
TARGET_CONFIRMED_EVENTS_TOTAL = 135
TARGET_CONFIRMED_EVENTS_PER_SITE = 10
ASSURANCE_LOWER_BOUND = 0.90
Z_95 = 1.959963984540054


def wilson_interval(successes: int, total: int) -> tuple[float, float]:
    probability = successes / total
    denominator = 1 + Z_95**2 / total
    center = (probability + Z_95**2 / (2 * total)) / denominator
    half = Z_95 * np.sqrt(
        probability * (1 - probability) / total + Z_95**2 / (4 * total**2)
    ) / denominator
    return float(max(0.0, center - half)), float(min(1.0, center + half))


def target_attainment(analyzable: np.ndarray, events: np.ndarray) -> np.ndarray:
    return (
        (analyzable.sum(axis=1) >= TARGET_ANALYZABLE_TOTAL)
        & (analyzable.min(axis=1) >= TARGET_ANALYZABLE_PER_SITE)
        & (events.sum(axis=1) >= TARGET_CONFIRMED_EVENTS_TOTAL)
        & (events.min(axis=1) >= TARGET_CONFIRMED_EVENTS_PER_SITE)
    )


def simulate_equal_quotas() -> tuple[pd.DataFrame, pd.DataFrame, int]:
    rows: list[dict[str, Any]] = []
    n_cohorts = 0
    scenario_index = 0
    for followup_loss, score_missing, confirmation_loss, event_probability in product(
        LOSS_RATES, LOSS_RATES, LOSS_RATES, EVENT_PROBABILITIES
    ):
        analyzable_probability = (1 - followup_loss) * (1 - score_missing)
        confirmed_event_probability = event_probability * (1 - confirmation_loss)
        for seed_index, seed in enumerate(SEEDS):
            rng = np.random.default_rng(seed + scenario_index * 1009)
            for per_site in PER_SITE_CANDIDATES:
                analyzable = rng.binomial(
                    per_site, analyzable_probability, size=(REPLICATES, 3)
                )
                events = rng.binomial(analyzable, confirmed_event_probability)
                attained = target_attainment(analyzable, events)
                count = int(attained.sum())
                low, high = wilson_interval(count, REPLICATES)
                rows.append(
                    {
                        "followup_loss": followup_loss,
                        "score_missing": score_missing,
                        "confirmation_loss": confirmation_loss,
                        "event_probability": event_probability,
                        "seed": seed,
                        "gross_per_site": per_site,
                        "gross_total": 3 * per_site,
                        "n_replicates": REPLICATES,
                        "joint_target_count": count,
                        "joint_target_probability": count / REPLICATES,
                        "joint_target_ci_low": low,
                        "joint_target_ci_high": high,
                    }
                )
                n_cohorts += REPLICATES
        scenario_index += 1

    grid = pd.DataFrame(rows)
    key = ["followup_loss", "score_missing", "confirmation_loss", "event_probability"]
    seed_min = (
        grid.groupby(key + ["gross_per_site"], as_index=False)
        .agg(
            minimum_seed_probability=("joint_target_probability", "min"),
            minimum_seed_ci_low=("joint_target_ci_low", "min"),
            maximum_seed_ci_high=("joint_target_ci_high", "max"),
        )
    )
    minima_rows: list[dict[str, Any]] = []
    for values, frame in seed_min.groupby(key, sort=True):
        eligible = frame.loc[frame["minimum_seed_ci_low"] >= ASSURANCE_LOWER_BOUND]
        if eligible.empty:
            selected = frame.sort_values("gross_per_site").iloc[-1]
            reached = False
        else:
            selected = eligible.sort_values("gross_per_site").iloc[0]
            reached = True
        followup_loss, score_missing, confirmation_loss, event_probability = values
        analyzable_probability = (1 - followup_loss) * (1 - score_missing)
        event_observation_probability = event_probability * (1 - confirmation_loss)
        gross_total = int(selected["gross_per_site"]) * 3
        minima_rows.append(
            {
                "followup_loss": followup_loss,
                "score_missing": score_missing,
                "confirmation_loss": confirmation_loss,
                "event_probability": event_probability,
                "gross_per_site": int(selected["gross_per_site"]),
                "gross_total": gross_total,
                "inflation_over_450": gross_total / TARGET_ANALYZABLE_TOTAL,
                "expected_analyzable_total": gross_total * analyzable_probability,
                "expected_confirmed_events_total": gross_total
                * analyzable_probability
                * event_observation_probability,
                "minimum_seed_probability": selected["minimum_seed_probability"],
                "minimum_seed_ci_low": selected["minimum_seed_ci_low"],
                "reference_counts_reached": reached,
                "verdict": (
                    "REFERENCE_COUNTS_REACHED_WITHIN_GRID"
                    if reached
                    else "REFERENCE_COUNTS_NOT_REACHED_WITHIN_GRID"
                ),
            }
        )
    return grid, pd.DataFrame(minima_rows), n_cohorts


def simulate_passive_recruitment() -> tuple[pd.DataFrame, pd.DataFrame, int]:
    rows: list[dict[str, Any]] = []
    n_cohorts = 0
    analyzable_probability = 0.9 * 0.9
    confirmed_event_probability = 0.30 * 0.9
    for allocation_index, (name, shares) in enumerate(SITE_SHARES.items()):
        for seed in SEEDS:
            rng = np.random.default_rng(seed + 90001 + allocation_index * 1009)
            for gross_total in PASSIVE_TOTAL_CANDIDATES:
                enrolled = rng.multinomial(gross_total, shares, size=REPLICATES)
                analyzable = rng.binomial(enrolled, analyzable_probability)
                events = rng.binomial(analyzable, confirmed_event_probability)
                attained = target_attainment(analyzable, events)
                count = int(attained.sum())
                low, high = wilson_interval(count, REPLICATES)
                rows.append(
                    {
                        "allocation": name,
                        "site_shares": "/".join(f"{share:.2f}" for share in shares),
                        "seed": seed,
                        "gross_total": gross_total,
                        "n_replicates": REPLICATES,
                        "joint_target_count": count,
                        "joint_target_probability": count / REPLICATES,
                        "joint_target_ci_low": low,
                        "joint_target_ci_high": high,
                    }
                )
                n_cohorts += REPLICATES

    grid = pd.DataFrame(rows)
    collapsed = (
        grid.groupby(["allocation", "site_shares", "gross_total"], as_index=False)
        .agg(
            minimum_seed_probability=("joint_target_probability", "min"),
            minimum_seed_ci_low=("joint_target_ci_low", "min"),
            maximum_seed_ci_high=("joint_target_ci_high", "max"),
        )
    )
    minima_rows: list[dict[str, Any]] = []
    for (allocation, shares), frame in collapsed.groupby(["allocation", "site_shares"], sort=True):
        eligible = frame.loc[frame["minimum_seed_ci_low"] >= ASSURANCE_LOWER_BOUND]
        if eligible.empty:
            selected = frame.sort_values("gross_total").iloc[-1]
            reached = False
        else:
            selected = eligible.sort_values("gross_total").iloc[0]
            reached = True
        if allocation == "balanced_in_expectation":
            reference_status = "BALANCED_IN_EXPECTATION_NOT_FIXED_QUOTA"
        else:
            reference_status = "OUTSIDE_TESTED_BALANCED_REFERENCE"
        minima_rows.append(
            {
                "allocation": allocation,
                "site_shares": shares,
                "gross_total": int(selected["gross_total"]),
                "inflation_over_450": int(selected["gross_total"]) / 450,
                "minimum_seed_probability": selected["minimum_seed_probability"],
                "minimum_seed_ci_low": selected["minimum_seed_ci_low"],
                "reference_counts_reached": reached,
                "transport_reference_status": reference_status,
                "verdict": (
                    "ARITHMETIC_FLOORS_REACHED_BUT_TRANSPORT_NOT_ESTABLISHED"
                    if reached
                    else "ARITHMETIC_FLOORS_NOT_REACHED_WITHIN_GRID"
                ),
            }
        )
    return grid, pd.DataFrame(minima_rows), n_cohorts


def find_scenario(frame: pd.DataFrame, **values: float) -> dict[str, Any]:
    selected = frame.copy()
    for key, value in values.items():
        selected = selected.loc[np.isclose(selected[key], value)]
    if len(selected) != 1:
        raise RuntimeError(f"Expected one scenario for {values}, found {len(selected)}")
    return selected.iloc[0].to_dict()


def write_report(
    output_dir: Path,
    quota_minima: pd.DataFrame,
    passive_minima: pd.DataFrame,
    summary: dict[str, Any],
) -> None:
    reference = summary["reference_scenario"]
    severe = summary["severe_loss_scenario"]
    low_event = summary["low_event_scenario"]
    passive_lines = "\n".join(
        f"- `{row.allocation}`: gross total `{row.gross_total}`, minimum-seed "
        f"assurance `{row.minimum_seed_probability:.3f}` (Wilson lower "
        f"`{row.minimum_seed_ci_low:.3f}`), `{row.transport_reference_status}`."
        for row in passive_minima.itertuples(index=False)
    )
    report = f"""# V54 Progression Enrollment-Inflation Audit

Status: **{summary['verdict']}**.

This is seeded synthetic study-planning behavior only. It is not an empirical
MS event rate, loss rate, effect size, or universal sample-size recommendation.

## Equal-Quota Results

Across {summary['n_equal_quota_scenarios']} fixed loss/event scenarios, all
{summary['n_equal_quota_scenarios_reaching_reference']} reach the frozen count
targets within the searched total-enrollment range of 450-2,400. Each selected
minimum requires the 95% Wilson lower bound for joint target attainment to be
at least 0.90 in every one of three seeds.

- Reference planning scenario (10% follow-up loss, 10% score missingness, 10%
  confirmation loss, event probability 0.30): gross `{reference['gross_total']}`
  (`{reference['gross_per_site']}` per site; inflation
  `{reference['inflation_over_450']:.2f}x`), minimum-seed assurance
  `{reference['minimum_seed_probability']:.3f}`.
- Severe-loss scenario (20% in all three loss channels, event probability
  0.30): gross `{severe['gross_total']}` (`{severe['gross_per_site']}` per
  site; `{severe['inflation_over_450']:.2f}x`).
- Lower-event scenario (10% in all loss channels, event probability 0.15):
  gross `{low_event['gross_total']}` (`{low_event['gross_per_site']}` per site;
  `{low_event['inflation_over_450']:.2f}x`).

The event target, not merely participant retention, drives inflation in the
lower-event setting. These numbers are conditional on the generator and are a
planning lookup, not a guarantee.

## Passive Recruitment Stress

With all three loss channels fixed at 10% and event probability 0.30:

{passive_lines}

Clearing participant/event arithmetic by enrolling more does not validate an
unequal site allocation. Only explicit equal site quotas align with the fixed
balanced design that previously passed transport; all passive strategies need
the full site transport gate on realized data.

## Boundary

The generator assumes independent loss channels. Any score/risk-dependent
attendance, censoring, death, or confirmation mechanism invokes the separate
V54 invalidity and sensitivity boundaries. Enrollment inflation cannot repair
informative missingness, endpoint misclassification, unknown site scale, or a
nonportable site effect.
"""
    (output_dir / "REPORT.md").write_text(report)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    quota_grid, quota_minima, quota_cohorts = simulate_equal_quotas()
    passive_grid, passive_minima, passive_cohorts = simulate_passive_recruitment()
    quota_grid.to_csv(output_dir / "equal_quota_candidate_grid.tsv", sep="\t", index=False)
    quota_minima.to_csv(output_dir / "equal_quota_scenario_minima.tsv", sep="\t", index=False)
    passive_grid.to_csv(output_dir / "passive_recruitment_candidate_grid.tsv", sep="\t", index=False)
    passive_minima.to_csv(output_dir / "passive_recruitment_minima.tsv", sep="\t", index=False)

    reference = find_scenario(
        quota_minima,
        followup_loss=0.1,
        score_missing=0.1,
        confirmation_loss=0.1,
        event_probability=0.30,
    )
    severe = find_scenario(
        quota_minima,
        followup_loss=0.2,
        score_missing=0.2,
        confirmation_loss=0.2,
        event_probability=0.30,
    )
    low_event = find_scenario(
        quota_minima,
        followup_loss=0.1,
        score_missing=0.1,
        confirmation_loss=0.1,
        event_probability=0.15,
    )
    n_reached = int(quota_minima["reference_counts_reached"].sum())
    summary = {
        "purpose": "V54 seeded synthetic progression enrollment-inflation audit; no biological claim",
        "synthetic": True,
        "seeds": list(SEEDS),
        "replicates_per_candidate_seed": REPLICATES,
        "n_equal_quota_scenarios": len(quota_minima),
        "n_equal_quota_scenarios_reaching_reference": n_reached,
        "n_candidate_seed_cells": len(quota_grid) + len(passive_grid),
        "n_synthetic_cohort_replicates": quota_cohorts + passive_cohorts,
        "assurance_wilson_lower_bound": ASSURANCE_LOWER_BOUND,
        "targets": {
            "analyzable_total": TARGET_ANALYZABLE_TOTAL,
            "analyzable_per_site": TARGET_ANALYZABLE_PER_SITE,
            "confirmed_events_total": TARGET_CONFIRMED_EVENTS_TOTAL,
            "confirmed_events_per_site": TARGET_CONFIRMED_EVENTS_PER_SITE,
        },
        "reference_scenario": reference,
        "severe_loss_scenario": severe,
        "low_event_scenario": low_event,
        "passive_recruitment": passive_minima.to_dict("records"),
        "verdict": (
            "CONDITIONAL_ENROLLMENT_LOOKUP_COMPLETE_NO_UNIVERSAL_N"
            if n_reached == len(quota_minima)
            else "SOME_REFERENCE_COUNTS_NOT_REACHED_WITHIN_GRID"
        ),
        "boundary": "Synthetic independent-loss planning behavior only; no empirical MS rate, effect, or universal cohort size.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    config = {
        "purpose": summary["purpose"],
        "synthetic": True,
        "seeds": list(SEEDS),
        "replicates": REPLICATES,
        "loss_rates": list(LOSS_RATES),
        "event_probabilities": list(EVENT_PROBABILITIES),
        "per_site_candidates": [min(PER_SITE_CANDIDATES), max(PER_SITE_CANDIDATES), 5],
        "passive_total_candidates": [min(PASSIVE_TOTAL_CANDIDATES), max(PASSIVE_TOTAL_CANDIDATES), 15],
        "site_shares": SITE_SHARES,
        "targets": summary["targets"],
        "assurance_rule": "95% Wilson lower bound >= 0.90 in every seed",
    }
    (output_dir / "simulation_config.json").write_text(json.dumps(config, indent=2) + "\n")
    write_report(output_dir, quota_minima, passive_minima, summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
