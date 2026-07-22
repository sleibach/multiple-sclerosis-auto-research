#!/usr/bin/env python3
"""Seeded synthetic progression endpoint-confirmation error audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.special import expit

import v54_progression_combined_ascertainment as base


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_confirmation_error"
SEEDS = (55401, 55403, 55409)
N_VALUES = (450, 900, 1500)
EVENT_PROBABILITIES = (0.15, 0.30)
HRS = (1.0, 1.5)
REPLICATES = 800
CONFIRMATION_LAG = 0.25
MECHANISMS = {
    "complete": ("none", 0.0, "none", 0.0),
    "independent_miss_10pct": ("independent", 0.10, "none", 0.0),
    "score_miss_10pct": ("score", 0.10, "none", 0.0),
    "risk_miss_10pct": ("risk", 0.10, "none", 0.0),
    "joint_miss_10pct": ("joint", 0.10, "none", 0.0),
    "independent_false_2pct": ("none", 0.0, "independent", 0.02),
    "score_false_2pct": ("none", 0.0, "score", 0.02),
    "mixed_joint_miss_score_false": ("joint", 0.10, "score", 0.02),
}


def linear_predictor(mode: str, score: np.ndarray, frailty: np.ndarray) -> np.ndarray:
    if mode in {"none", "independent"}:
        return np.zeros_like(score)
    if mode == "score":
        return score
    if mode == "risk":
        return frailty
    if mode == "joint":
        return 0.5 * score + 0.5 * frailty + 1.2 * score * frailty
    raise ValueError(mode)


def masked_probabilities(
    lp: np.ndarray, mask: np.ndarray, target: float
) -> np.ndarray:
    if target == 0:
        return np.zeros_like(lp)
    low = np.full(lp.shape[0], -20.0)
    high = np.full(lp.shape[0], 20.0)
    denominators = np.maximum(mask.sum(axis=1), 1)
    for _ in range(50):
        middle = (low + high) / 2
        observed = (expit(middle[:, None] + lp) * mask).sum(axis=1) / denominators
        below = observed < target
        low[below] = middle[below]
        high[~below] = middle[~below]
    return expit(((low + high) / 2)[:, None] + lp)


def simulate_cell(
    rng: np.random.Generator,
    mechanism: str,
    n: int,
    event_probability: float,
    hr: float,
) -> dict[str, Any]:
    miss_mode, miss_target, false_mode, false_target = MECHANISMS[mechanism]
    score = rng.normal(size=(REPLICATES, n))
    frailty = rng.normal(size=(REPLICATES, n))
    sites = base.assign_sites(rng, score, "balanced")
    site_hr = np.array([1.50, 1.00, 0.67])[sites]
    multiplier = np.exp(np.log(hr) * score + 0.70 * frailty) * site_hr
    baseline = base.calibrate_scale(multiplier, event_probability)
    latent_time = -np.log(np.clip(rng.random(score.shape), 1e-12, 1.0)) / (
        baseline[:, None] * multiplier
    )
    latent_event = latent_time <= 1.0
    confirmable = latent_time <= 1.0 - CONFIRMATION_LAG
    nonconfirmable = ~confirmable

    miss_lp = linear_predictor(miss_mode, score, frailty)
    miss_probability = masked_probabilities(miss_lp, confirmable, miss_target)
    missed = confirmable & (rng.random(score.shape) < miss_probability)
    true_confirmed = confirmable & ~missed

    false_lp = linear_predictor(false_mode, score, frailty)
    false_probability = masked_probabilities(false_lp, nonconfirmable, false_target)
    false_confirmed = nonconfirmable & (rng.random(score.shape) < false_probability)
    false_time = rng.uniform(CONFIRMATION_LAG, 1.0, size=score.shape)
    observed_event = true_confirmed | false_confirmed
    observed_time = np.where(
        true_confirmed,
        latent_time + CONFIRMATION_LAG,
        np.where(false_confirmed, false_time, 1.0),
    )

    measured = np.sqrt(base.RELIABILITY) * score + np.sqrt(1 - base.RELIABILITY) * rng.normal(
        size=score.shape
    )
    assay_scale = np.array([0.50, 1.00, 2.00])[sites]
    assay_offset = np.array([-1.00, 0.00, 1.00])[sites]
    assay_score = assay_offset + assay_scale * measured
    guarded = base.within_site_standardize(assay_score, sites)
    included = rng.random(score.shape) >= base.SCORE_MISSING
    result = base.analyze(
        guarded, observed_time, observed_event, included, sites,
        "guarded_within_site_stratified",
    )
    result.update(
        {
            "stack": mechanism,
            "attendance_mode": miss_mode,
            "death_mode": false_mode,
            "switch_mode": "none",
            "site_mode": "balanced",
            "route": "guarded_within_site_stratified",
            "n_requested": n,
            "event_probability_before_ascertainment": event_probability,
            "molecular_progression_hr": hr,
            "median_latent_events": float(np.median(latent_event.sum(axis=1))),
            "median_confirmable_events": float(np.median(confirmable.sum(axis=1))),
            "median_missed_confirmations": float(np.median(missed.sum(axis=1))),
            "median_false_confirmations": float(np.median(false_confirmed.sum(axis=1))),
        }
    )
    return result


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    config = {
        "synthetic": True,
        "seeds": list(SEEDS),
        "sample_sizes": list(N_VALUES),
        "event_probabilities": list(EVENT_PROBABILITIES),
        "molecular_hrs": list(HRS),
        "replicates_per_seed_cell": REPLICATES,
        "confirmation_lag": CONFIRMATION_LAG,
        "mechanisms": {key: list(value) for key, value in MECHANISMS.items()},
        "route": "guarded_within_site_stratified",
        "boundary": "Seeded synthetic endpoint-method behavior only; no empirical error rate, MS effect, or biological claim.",
    }
    (OUT / "simulation_config.json").write_text(json.dumps(config, indent=2) + "\n")
    rows = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        for mechanism in MECHANISMS:
            for n in N_VALUES:
                for event_probability in EVENT_PROBABILITIES:
                    for hr in HRS:
                        row = simulate_cell(rng, mechanism, n, event_probability, hr)
                        row["seed"] = seed
                        rows.append(row)
    seed_frame = pd.DataFrame(rows)
    seed_frame.to_csv(OUT / "seed_grid.tsv", sep="\t", index=False)
    grid = base.aggregate(seed_frame)
    metrics = seed_frame.groupby(
        ["stack", "route", "n_requested", "event_probability_before_ascertainment", "molecular_progression_hr"],
        as_index=False,
    )[["median_latent_events", "median_confirmable_events", "median_missed_confirmations", "median_false_confirmations"]].median()
    grid = grid.merge(
        metrics,
        on=["stack", "route", "n_requested", "event_probability_before_ascertainment", "molecular_progression_hr"],
        how="left",
    )
    grid.to_csv(OUT / "aggregate_grid.tsv", sep="\t", index=False)
    calibration = base.calibration(grid)
    calibration.to_csv(OUT / "null_calibration.tsv", sep="\t", index=False)
    invalid = set(calibration.loc[calibration.invalid_null_family, "stack"])

    minimum_rows = []
    for mechanism in MECHANISMS:
        for event_probability in EVENT_PROBABILITIES:
            current = grid.loc[
                grid["stack"].eq(mechanism)
                & grid.event_probability_before_ascertainment.eq(event_probability)
                & grid.molecular_progression_hr.eq(1.5)
            ].sort_values("n_requested")
            seed_subset = seed_frame.loc[
                seed_frame["stack"].eq(mechanism)
                & seed_frame.event_probability_before_ascertainment.eq(event_probability)
                & seed_frame.molecular_progression_hr.eq(1.5)
            ]
            reached = []
            for row in current.itertuples(index=False):
                seed_min = float(seed_subset.loc[seed_subset.n_requested.eq(row.n_requested), "positive_call_probability"].min())
                if mechanism not in invalid and row.positive_call_probability >= 0.80 and seed_min >= 0.75:
                    reached.append((int(row.n_requested), float(row.positive_call_probability), seed_min))
            minimum_rows.append(
                {
                    "mechanism": mechanism,
                    "event_probability": event_probability,
                    "null_family_valid": mechanism not in invalid,
                    "minimum_n_reaching_rule": reached[0][0] if reached else "not_reached_or_invalid",
                    "positive_probability_at_minimum_or_largest": reached[0][1] if reached else float(current.iloc[-1].positive_call_probability),
                }
            )
    minimum = pd.DataFrame(minimum_rows)
    minimum.to_csv(OUT / "minimum_n_by_confirmation_mechanism.tsv", sep="\t", index=False)
    complete_minimum = minimum.loc[minimum.mechanism.eq("complete")].set_index(
        "event_probability"
    )["minimum_n_reaching_rule"]
    summary = {
        "purpose": "V54 synthetic endpoint-confirmation error audit; no biological claim",
        "synthetic": True,
        "n_unique_simulated_cohorts": len(SEEDS) * len(MECHANISMS) * len(N_VALUES) * len(EVENT_PROBABILITIES) * len(HRS) * REPLICATES,
        "n_null_families": len(calibration),
        "n_invalid_null_families": len(invalid),
        "invalid_null_families": sorted(invalid),
        "n_calibrated_families": len(MECHANISMS) - len(invalid),
        "calibrated_families": sorted(set(MECHANISMS) - invalid),
        "complete_minimum_n_for_hr_1_5": {
            "event_015": int(complete_minimum.loc[0.15]),
            "event_030": int(complete_minimum.loc[0.30]),
        },
        "verdict": "CONFIRMATION_DEPENDENCE_MUST_BE_AUDITED_BEFORE_PROGRESSION_INFERENCE",
        "boundary": "Synthetic endpoint-method behavior only; no empirical confirmation error rate, progression association, or biological claim.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
