#!/usr/bin/env python3
"""Site-aware synthetic power extension for weaker progression effects."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

import v54_progression_combined_ascertainment as generator


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_weaker_effect_power"
SEEDS = (55301, 55303, 55309)
N_VALUES = (450, 600, 900, 1200, 1500)
EVENT_PROBABILITIES = (0.15, 0.30)
HRS = (1.0, 1.2, 1.3, 1.5, 1.7)
REPLICATES = 600
ROUTE = "guarded_within_site_stratified"


def gross_multiple_of_three(analyzable: int) -> int:
    raw = math.ceil(analyzable * 690 / 450)
    return int(math.ceil(raw / 3) * 3)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    config = {
        "synthetic": True,
        "seeds": list(SEEDS),
        "analyzable_sample_sizes": list(N_VALUES),
        "event_probabilities_before_ascertainment": list(EVENT_PROBABILITIES),
        "molecular_hrs_per_latent_sd": list(HRS),
        "replicates_per_seed_cell": REPLICATES,
        "stack": "clean",
        "route": ROUTE,
        "gross_inflation_basis": "690/450 under independent 10% molecular/clinical/site losses",
        "boundary": "Seeded synthetic method behavior only; no empirical progression effect, universal N, or biological claim.",
    }
    (OUT / "simulation_config.json").write_text(json.dumps(config, indent=2) + "\n")
    rows = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        for n in N_VALUES:
            for event_probability in EVENT_PROBABILITIES:
                for hr in HRS:
                    results = generator.simulate_cell(
                        rng, "clean", n, event_probability, hr, REPLICATES
                    )
                    row = next(item for item in results if item["route"] == ROUTE)
                    row["seed"] = seed
                    rows.append(row)
    seed_frame = pd.DataFrame(rows)
    seed_frame.to_csv(OUT / "seed_grid.tsv", sep="\t", index=False)
    grid = generator.aggregate(seed_frame)
    grid.to_csv(OUT / "aggregate_grid.tsv", sep="\t", index=False)
    null_calibration = generator.calibration(grid)
    null_calibration.to_csv(OUT / "null_calibration.tsv", sep="\t", index=False)
    null_valid = not bool(null_calibration.invalid_null_family.any())

    minimum_rows = []
    for (event_probability, hr), group in grid.loc[grid.molecular_progression_hr.gt(1.0)].groupby(
        ["event_probability_before_ascertainment", "molecular_progression_hr"], sort=True
    ):
        ordered = group.sort_values("n_requested")
        seed_subset = seed_frame.loc[
            seed_frame.event_probability_before_ascertainment.eq(event_probability)
            & seed_frame.molecular_progression_hr.eq(hr)
        ]
        eligible = []
        for row in ordered.itertuples(index=False):
            seed_rates = seed_subset.loc[
                seed_subset.n_requested.eq(row.n_requested), "positive_call_probability"
            ]
            aggregate_positive = float(row.positive_call_probability)
            minimum_seed = float(seed_rates.min())
            if null_valid and aggregate_positive >= 0.80 and minimum_seed >= 0.75:
                eligible.append((int(row.n_requested), aggregate_positive, minimum_seed))
        if eligible:
            minimum_n, probability, minimum_seed = eligible[0]
            gross = gross_multiple_of_three(minimum_n)
        else:
            minimum_n = "not_reached"
            probability = float(ordered.iloc[-1].positive_call_probability)
            largest_seed_rates = seed_subset.loc[
                seed_subset.n_requested.eq(max(N_VALUES)), "positive_call_probability"
            ]
            minimum_seed = float(largest_seed_rates.min())
            gross = "not_reached"
        minimum_rows.append(
            {
                "event_probability": event_probability,
                "molecular_hr_per_latent_sd": hr,
                "minimum_analyzable_n_reaching_rule": minimum_n,
                "conditional_gross_n_at_10pct_each_loss": gross,
                "positive_call_probability_at_decision_n_or_largest": probability,
                "minimum_seed_probability_at_decision_n_or_largest": minimum_seed,
                "largest_n_simulated": max(N_VALUES),
            }
        )
    minimum = pd.DataFrame(minimum_rows)
    minimum.to_csv(OUT / "minimum_n_by_effect.tsv", sep="\t", index=False)
    reached = minimum.loc[minimum.minimum_analyzable_n_reaching_rule.ne("not_reached")]
    by_hr = {
        f"event_{int(round(row.event_probability * 100)):03d}_hr_{int(round(row.molecular_hr_per_latent_sd * 10)):02d}": row.minimum_analyzable_n_reaching_rule
        for row in minimum.itertuples(index=False)
    }
    summary = {
        "purpose": "V54 site-aware weaker-effect progression power extension; no biological claim",
        "synthetic": True,
        "n_unique_simulated_cohorts": len(SEEDS) * len(N_VALUES) * len(EVENT_PROBABILITIES) * len(HRS) * REPLICATES,
        "n_guarded_route_evaluations": len(SEEDS) * len(N_VALUES) * len(EVENT_PROBABILITIES) * len(HRS) * REPLICATES,
        "null_family_calibrated": null_valid,
        "n_nonnull_scenarios": len(minimum),
        "n_scenarios_reaching_rule": len(reached),
        "minimum_n_by_scenario": by_hr,
        "verdict": "WEAKER_EFFECT_REFERENCE_EXTENDED_CONDITIONALLY" if null_valid else "POWER_INTERPRETATION_BLOCKED_BY_NULL_CALIBRATION",
        "boundary": "Synthetic clean-reference power only; true MS effect is unknown and no value is a universal cohort-size guarantee.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
