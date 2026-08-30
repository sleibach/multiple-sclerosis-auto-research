#!/usr/bin/env python3
"""Finite-sample donor sizing for the V57 negative-control fail-stop."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t


ROOT = Path(__file__).resolve().parents[1]
SEEDS = [20260911, 20260912, 20260913]
GRID = [(12, 8), (16, 12), (20, 16), (24, 20), (32, 24), (40, 32)]
N_SCREENS = 5000
N_CONTROLS = 4
ALPHA = 0.05
SD = 0.75


def panel_t(values: np.ndarray) -> np.ndarray:
    return values.mean(axis=1) / (values.std(axis=1, ddof=1) / np.sqrt(values.shape[1]))


def simulate(rng: np.random.Generator, n_train: int, n_test: int, scenario: str, critical: float) -> float:
    train = rng.normal(0.0, SD, (N_SCREENS, n_train, N_CONTROLS))
    test = rng.normal(0.0, SD, (N_SCREENS, n_test, N_CONTROLS))
    if scenario == "common_hidden_drift":
        train += 0.75
        test += 0.75
    elif scenario == "control_specific_artifact":
        train[:, :, 0] += 1.15
        test[:, :, 0] += 1.15
    max_stat = np.maximum(np.max(np.abs(panel_t(train)), axis=1), np.max(np.abs(panel_t(test)), axis=1))
    return float(np.mean(max_stat >= critical))


def run(outdir: Path) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for n_train, n_test in GRID:
        df = min(n_train, n_test) - 1
        critical = float(t.ppf(1.0 - ALPHA / (2 * N_CONTROLS * 2), df=df))
        for scenario in ["clean", "common_hidden_drift", "control_specific_artifact"]:
            for seed in SEEDS:
                rng = np.random.default_rng(seed)
                rows.append(
                    {
                        "n_train": n_train,
                        "n_test": n_test,
                        "df_for_critical": df,
                        "critical_value": critical,
                        "scenario": scenario,
                        "seed": seed,
                        "n_screens": N_SCREENS,
                        "stop_probability": simulate(rng, n_train, n_test, scenario, critical),
                    }
                )
    results = pd.DataFrame(rows)
    results.to_csv(outdir / "negative_control_finite_sample_results.tsv", sep="\t", index=False)
    boundary = []
    first_pass = None
    for (n_train, n_test), group in results.groupby(["n_train", "n_test"], sort=False):
        clean_max = float(group[group.scenario == "clean"].stop_probability.max())
        common_min = float(group[group.scenario == "common_hidden_drift"].stop_probability.min())
        specific_min = float(group[group.scenario == "control_specific_artifact"].stop_probability.min())
        passed = clean_max <= 0.05 and common_min >= 0.80 and specific_min >= 0.80
        row = {
            "n_train": int(n_train),
            "n_test": int(n_test),
            "maximum_seed_clean_fwer": clean_max,
            "minimum_seed_common_drift_power": common_min,
            "minimum_seed_specific_artifact_power": specific_min,
            "status": "PASS" if passed else "FAIL",
        }
        boundary.append(row)
        if passed and first_pass is None:
            first_pass = row
    pd.DataFrame(boundary).to_csv(outdir / "negative_control_finite_sample_boundary.tsv", sep="\t", index=False)
    summary = {
        "synthetic": True,
        "purpose": "finite-sample family-adjusted negative-control sizing; no biological claim",
        "n_screens": len(GRID) * 3 * len(SEEDS) * N_SCREENS,
        "first_all_seed_pass": first_pass,
        "overall_status": "PASS" if first_pass else "NO_PASSING_GRID_POINT",
    }
    (outdir / "negative_control_finite_sample_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=ROOT / "analysis/v57_negative_control_finite_sample")
    args = parser.parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    return run(outdir)


if __name__ == "__main__":
    raise SystemExit(main())
