#!/usr/bin/env python3
"""Simulate the method-only power envelope for the fixed ToleDYNAMIC family.

The simulation uses a correlated noncentral-t approximation for paired-change
arm contrasts. It characterizes design behavior only; effect sizes are
hypothetical and are not evidence about MS or tolebrutinib.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v56_toledynamic_power_envelope"
N_PER_ARM = (8, 10, 15, 20, 30, 40)
EFFECTS = (0.4, 0.6, 0.8, 1.0, 1.2)
CORRELATIONS = (0.0, 0.5, 0.8)
N_ENDPOINTS = 18
ALPHA = 0.05


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--null-calibration", type=int, default=100_000)
    parser.add_argument("--null-audit-per-seed", type=int, default=20_000)
    parser.add_argument("--alternative-per-seed", type=int, default=5_000)
    parser.add_argument("--seeds", type=int, default=3)
    return parser.parse_args()


def correlated_normals(rng: np.random.Generator, n: int, rho: float) -> np.ndarray:
    common = rng.standard_normal((n, 1))
    independent = rng.standard_normal((n, N_ENDPOINTS))
    return np.sqrt(rho) * common + np.sqrt(1.0 - rho) * independent


def t_statistics(
    rng: np.random.Generator,
    n_families: int,
    n_per_arm: int,
    rho: float,
    effect: float = 0.0,
) -> np.ndarray:
    numerator = correlated_normals(rng, n_families, rho)
    numerator[:, 0] += effect * np.sqrt(n_per_arm / 2.0)
    variance = rng.chisquare(2 * n_per_arm - 2, size=(n_families, N_ENDPOINTS))
    denominator = np.sqrt(variance / (2 * n_per_arm - 2))
    return numerator / denominator


def run(args: argparse.Namespace) -> tuple[pd.DataFrame, dict[str, object]]:
    rows = []
    calibration_rows = []
    for n_per_arm in N_PER_ARM:
        for rho in CORRELATIONS:
            calibration_rng = np.random.default_rng(56_000_000 + 1000 * n_per_arm + int(rho * 100))
            null_t = t_statistics(calibration_rng, args.null_calibration, n_per_arm, rho)
            critical = float(np.quantile(np.max(np.abs(null_t), axis=1), 1.0 - ALPHA, method="higher"))

            audit_rates = []
            for seed_index in range(args.seeds):
                rng = np.random.default_rng(56_100_000 + 10_000 * seed_index + 100 * n_per_arm + int(rho * 10))
                audit = t_statistics(rng, args.null_audit_per_seed, n_per_arm, rho)
                audit_rates.append(float(np.mean(np.max(np.abs(audit), axis=1) >= critical)))
            calibration_rows.append(
                {
                    "n_per_arm": n_per_arm,
                    "module_correlation": rho,
                    "max_t_critical": critical,
                    "null_fwer_mean": float(np.mean(audit_rates)),
                    "null_fwer_min": float(np.min(audit_rates)),
                    "null_fwer_max": float(np.max(audit_rates)),
                }
            )

            for effect in EFFECTS:
                powers = []
                null_slot_false_positive = []
                for seed_index in range(args.seeds):
                    rng = np.random.default_rng(
                        56_200_000
                        + 100_000 * seed_index
                        + 1000 * n_per_arm
                        + int(rho * 100)
                        + int(effect * 10)
                    )
                    values = t_statistics(rng, args.alternative_per_seed, n_per_arm, rho, effect)
                    powers.append(float(np.mean(np.abs(values[:, 0]) >= critical)))
                    null_slot_false_positive.append(
                        float(np.mean(np.max(np.abs(values[:, 1:]), axis=1) >= critical))
                    )
                rows.append(
                    {
                        "n_per_arm": n_per_arm,
                        "total_n": 2 * n_per_arm,
                        "module_correlation": rho,
                        "planted_standardized_change_difference": effect,
                        "max_t_critical": critical,
                        "power_mean": float(np.mean(powers)),
                        "power_min_seed": float(np.min(powers)),
                        "power_max_seed": float(np.max(powers)),
                        "null_slots_any_false_positive_mean": float(np.mean(null_slot_false_positive)),
                        "replicates": args.alternative_per_seed * args.seeds,
                        "synthetic": True,
                    }
                )

    power = pd.DataFrame(rows)
    calibration = pd.DataFrame(calibration_rows)
    summary: dict[str, object] = {
        "purpose": "synthetic method-power envelope for a fixed 18-slot family; no biological evidence",
        "synthetic": True,
        "n_endpoints": N_ENDPOINTS,
        "alpha_familywise": ALPHA,
        "n_null_calibration_families_per_design": args.null_calibration,
        "n_independent_null_audit_families": len(calibration) * args.null_audit_per_seed * args.seeds,
        "n_alternative_families": len(power) * args.alternative_per_seed * args.seeds,
        "seed_count": args.seeds,
        "null_fwer_mean_over_designs": float(calibration.null_fwer_mean.mean()),
        "null_fwer_range_over_designs": [
            float(calibration.null_fwer_min.min()),
            float(calibration.null_fwer_max.max()),
        ],
        "boundary": (
            "Correlated noncentral-t design approximation for one planted slot; "
            "not the frozen mixed-model/permutation harness and not an assumed biological effect."
        ),
    }
    args.outdir.mkdir(parents=True, exist_ok=True)
    power.to_csv(args.outdir / "power_grid.tsv", sep="\t", index=False)
    calibration.to_csv(args.outdir / "null_calibration.tsv", sep="\t", index=False)
    (args.outdir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return power, summary


def main() -> int:
    args = parse_args()
    power, summary = run(args)
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("\nMaximum total n=40 design (20 per arm):")
    print(
        power.loc[power.n_per_arm.eq(20), [
            "module_correlation",
            "planted_standardized_change_difference",
            "power_mean",
            "power_min_seed",
            "power_max_seed",
        ]].to_string(index=False)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
