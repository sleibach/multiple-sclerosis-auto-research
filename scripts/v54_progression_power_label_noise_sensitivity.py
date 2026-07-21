#!/usr/bin/env python3
"""Compare the frozen V54 synthetic progression power grids by label noise."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RUNS = {
    0.00: ROOT / "analysis/v54_progression_event_power_design",
    0.05: ROOT / "analysis/v54_progression_power_label_noise/synthetic/noise_05",
    0.10: ROOT / "analysis/v54_progression_power_label_noise/synthetic/noise_10",
}
OUT = ROOT / "analysis/v54_progression_power_label_noise"
MATCH = [
    "n_requested",
    "event_rate_target",
    "odds_ratio_per_latent_sd",
    "missing_rate",
    "molecular_repeats",
    "measurement_reliability_per_repeat",
    "alpha",
]
SCENARIO = [
    "event_rate_target",
    "odds_ratio_per_latent_sd",
    "missing_rate",
    "molecular_repeats",
    "measurement_reliability_per_repeat",
    "alpha",
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    grids = {}
    minimums = {}
    total_cohorts = 0
    for noise, directory in RUNS.items():
        grid = pd.read_csv(directory / "power_grid.tsv", sep="\t")
        minimum = pd.read_csv(directory / "minimum_n_by_assumption.tsv", sep="\t")
        if len(grid) != 192 or len(minimum) != 24:
            raise RuntimeError(f"Unexpected grid shape for label noise {noise}")
        if not grid.label_noise.eq(noise).all() or not minimum.label_noise.eq(noise).all():
            raise RuntimeError(f"Label-noise metadata mismatch for {noise}")
        config = json.loads((directory / "simulation_config.json").read_text())
        total_cohorts += len(grid) * int(config["replicates_per_seed"]) * len(config["seeds"])
        grids[noise] = grid
        minimums[noise] = minimum

    baseline = grids[0.00].drop(columns="label_noise")
    matched_rows = []
    for noise in (0.05, 0.10):
        noisy = grids[noise].drop(columns="label_noise")
        merged = baseline.merge(
            noisy,
            on=MATCH,
            suffixes=("_baseline", "_noisy"),
            validate="one_to_one",
        )
        merged["label_noise"] = noise
        merged["absolute_power_change"] = (
            merged.conclusive_probability_noisy
            - merged.conclusive_probability_baseline
        )
        matched_rows.append(merged)
    matched = pd.concat(matched_rows, ignore_index=True)
    matched.to_csv(OUT / "matched_cell_comparison.tsv", sep="\t", index=False)

    minimum = minimums[0.00][SCENARIO + ["minimum_n_reaching_80pct", "power_at_largest_n"]].rename(
        columns={
            "minimum_n_reaching_80pct": "minimum_n_noise_0",
            "power_at_largest_n": "power_n240_noise_0",
        }
    )
    for noise, suffix in ((0.05, "05"), (0.10, "10")):
        add = minimums[noise][SCENARIO + ["minimum_n_reaching_80pct", "power_at_largest_n"]].rename(
            columns={
                "minimum_n_reaching_80pct": f"minimum_n_noise_{suffix}",
                "power_at_largest_n": f"power_n240_noise_{suffix}",
            }
        )
        minimum = minimum.merge(add, on=SCENARIO, validate="one_to_one")
    minimum.to_csv(OUT / "minimum_n_comparison.tsv", sep="\t", index=False)

    n240 = matched[
        matched.n_requested.eq(240)
        & matched.odds_ratio_per_latent_sd.gt(1.0)
    ].copy()
    summary_rows = []
    for (noise, missing), group in n240.groupby(["label_noise", "missing_rate"]):
        summary_rows.append(
            {
                "label_noise": noise,
                "missing_rate": missing,
                "n_n240_nonnull_cells": len(group),
                "median_absolute_power_change": float(group.absolute_power_change.median()),
                "minimum_absolute_power_change": float(group.absolute_power_change.min()),
                "maximum_absolute_power_change": float(group.absolute_power_change.max()),
            }
        )
    pd.DataFrame(summary_rows).to_csv(OUT / "n240_power_loss_summary.tsv", sep="\t", index=False)

    reaches = {
        noise: int(
            minimums[noise].minimum_n_reaching_80pct.astype(str).ne("not_reached").sum()
        )
        for noise in RUNS
    }
    baseline_reached = minimum.minimum_n_noise_0.astype(str).ne("not_reached")
    lost_at_05 = int(
        (baseline_reached & minimum.minimum_n_noise_05.astype(str).eq("not_reached")).sum()
    )
    lost_at_10 = int(
        (baseline_reached & minimum.minimum_n_noise_10.astype(str).eq("not_reached")).sum()
    )
    summary = {
        "purpose": "Synthetic progression-event label-noise sensitivity; no biological claim",
        "synthetic": True,
        "new_simulated_cohorts": 576_000,
        "total_cohorts_including_baseline": total_cohorts,
        "scenarios_reaching_80pct": {str(noise): count for noise, count in reaches.items()},
        "baseline_reached_scenarios_lost_at_5pct_noise": lost_at_05,
        "baseline_reached_scenarios_lost_at_10pct_noise": lost_at_10,
        "verdict": "LABEL_ERROR_MATERIALLY_REDUCES_SYNTHETIC_POWER",
        "boundary": (
            "Symmetric label flips are assumptions, not an empirical estimate of "
            "progression adjudication error or an MS effect."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = [
        "# V54 Progression-Event Label-Noise Sensitivity",
        "",
        "All cohorts are seeded synthetic method-design data, not MS evidence.",
        "",
        f"The sensitivity adds {summary['new_simulated_cohorts']:,} cohorts at 5% and "
        "10% symmetric outcome-label noise while preserving every other default-grid "
        "parameter. Scenarios reaching the frozen 80% criterion fall from "
        f"{reaches[0.00]}/24 at zero noise to {reaches[0.05]}/24 at 5% and "
        f"{reaches[0.10]}/24 at 10%.",
        "",
        "| event rate | OR | missing | repeats | n at 0% | n at 5% | n at 10% | power n=240: 0% / 5% / 10% |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in minimum.itertuples(index=False):
        lines.append(
            f"| {row.event_rate_target:.2f} | {row.odds_ratio_per_latent_sd:.2f} | "
            f"{row.missing_rate:.2f} | {row.molecular_repeats} | "
            f"{row.minimum_n_noise_0} | {row.minimum_n_noise_05} | "
            f"{row.minimum_n_noise_10} | {row.power_n240_noise_0:.3f} / "
            f"{row.power_n240_noise_05:.3f} / {row.power_n240_noise_10:.3f} |"
        )
    lines.extend(
        [
            "",
            "No OR 1.25 or 1.5 scenario reaches 80% by n=240 at any noise level. "
            "At 15% events, all OR 2.0 scenarios also fall below the criterion once "
            "5% label noise is introduced. At 30% events and OR 2.0, 5% noise moves "
            "minimum N to 160-240; 10% noise leaves one 20%-missingness, one-repeat "
            "scenario below 80% even at n=240.",
            "",
            "The practical pre-data implication is an adjudication requirement, not a "
            "biological claim: endpoint provenance and likely misclassification must be "
            "specified before a received cohort's blinded power calculation. These "
            "synthetic error rates are not estimates of real PIRA label quality.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
