#!/usr/bin/env python3
"""Independent-seed confirmation of the V54 guarded ascertainment boundary."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import v54_progression_combined_ascertainment as primary


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_combined_ascertainment_confirmation"
SEEDS = (55201, 55207, 55213)
REPLICATES = 2000
STACKS = (
    "attendance_weak_joint",
    "death_weak_joint",
    "switch_weak_joint",
    "weak_joint_all",
)
ROUTE = "guarded_within_site_stratified"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    config = {
        "synthetic": True,
        "independent_of_primary_seeds": True,
        "seeds": list(SEEDS),
        "replicates_per_cell_seed": REPLICATES,
        "sample_sizes": list(primary.N_VALUES),
        "event_probabilities": list(primary.EVENT_PROBABILITIES),
        "molecular_progression_hr": 1.0,
        "stacks": list(STACKS),
        "route": ROUTE,
        "generator_source": "scripts/v54_progression_combined_ascertainment.py",
        "boundary": "Independent synthetic method confirmation only; no patient data or biological claim.",
    }
    (OUT / "confirmation_config.json").write_text(json.dumps(config, indent=2) + "\n")
    rows = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        for stack in STACKS:
            for n in primary.N_VALUES:
                for event_probability in primary.EVENT_PROBABILITIES:
                    results = primary.simulate_cell(
                        rng, stack, n, event_probability, 1.0, REPLICATES
                    )
                    row = next(item for item in results if item["route"] == ROUTE)
                    row["seed"] = seed
                    rows.append(row)
    seed_frame = pd.DataFrame(rows)
    seed_frame.to_csv(OUT / "seed_grid.tsv", sep="\t", index=False)
    grid = primary.aggregate(seed_frame)
    grid.to_csv(OUT / "aggregate_grid.tsv", sep="\t", index=False)
    calibration = primary.calibration(grid)
    calibration.to_csv(OUT / "null_calibration.tsv", sep="\t", index=False)
    indexed = calibration.set_index("stack")
    constituents = [item for item in STACKS if item != "weak_joint_all"]
    invalid_constituents = [
        item for item in constituents
        if bool(indexed.loc[item, "invalid_null_family"])
    ]
    constituents_calibrated = not invalid_constituents
    combined_invalid = bool(indexed.loc["weak_joint_all", "invalid_null_family"])
    confirmed = constituents_calibrated and combined_invalid
    combined_row = indexed.loc["weak_joint_all"]
    if confirmed:
        verdict = "COMPOUNDED_INVALIDITY_INDEPENDENTLY_CONFIRMED"
    elif combined_invalid and invalid_constituents:
        verdict = "JOINT_SCORE_RISK_COMPONENT_AND_STACK_UNSAFE_NOT_UNIQUE_COMPOUNDING"
    else:
        verdict = "PRIMARY_COMPOUNDING_CALL_NOT_INDEPENDENTLY_CONFIRMED"
    summary = {
        "purpose": "Independent-seed synthetic confirmation of V54 combined ascertainment boundary",
        "synthetic": True,
        "n_unique_simulated_cohorts": len(SEEDS) * len(STACKS) * len(primary.N_VALUES) * len(primary.EVENT_PROBABILITIES) * REPLICATES,
        "n_guarded_route_evaluations": len(SEEDS) * len(STACKS) * len(primary.N_VALUES) * len(primary.EVENT_PROBABILITIES) * REPLICATES,
        "all_constituent_families_calibrated": constituents_calibrated,
        "invalid_constituent_families": invalid_constituents,
        "combined_family_invalid": combined_invalid,
        "combined_maximum_null_probability": float(combined_row["maximum_null_probability"]),
        "combined_maximum_ci_low": float(combined_row["maximum_ci_low"]),
        "combined_family_tail_probability": float(combined_row["maximum_family_tail_probability"]),
        "compounded_invalidity_independently_confirmed": confirmed,
        "verdict": verdict,
        "boundary": "Independent synthetic method confirmation only; no empirical MS ascertainment, progression, or biological claim.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
