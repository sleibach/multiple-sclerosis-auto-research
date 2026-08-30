#!/usr/bin/env python3
"""Calibrate the fixed four-site, at-least-two partial-conjunction gate."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import ndtr


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v57_federated_replicability_calibration"
SEEDS = (57031, 57032, 57033)
RHOS = (0.0, 0.5, 0.9)
N_REPLICATES = 250_000
ALPHA = 0.05
NULL_GATE = 0.055


def correlated_uniform(rng: np.random.Generator, n: int, rho: float) -> np.ndarray:
    common = rng.normal(size=(N_REPLICATES, 1))
    residual = rng.normal(size=(N_REPLICATES, n))
    z = np.sqrt(rho) * common + np.sqrt(1.0 - rho) * residual
    return ndtr(z)


def partial_conjunction_p(p_values: np.ndarray) -> np.ndarray:
    second = np.partition(p_values, 1, axis=1)[:, 1]
    return np.minimum(1.0, 3.0 * second)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for seed in SEEDS:
        for rho in RHOS:
            rng = np.random.default_rng(seed + round(rho * 1000))
            all_null = correlated_uniform(rng, 4, rho)
            one_nonnull = np.column_stack(
                [np.zeros(N_REPLICATES), correlated_uniform(rng, 3, rho)]
            )
            for configuration, p_values in (
                ("all_null", all_null),
                ("one_arbitrarily_nonnull", one_nonnull),
            ):
                pc_p = partial_conjunction_p(p_values)
                rejects = int(np.count_nonzero(pc_p <= ALPHA))
                rate = rejects / N_REPLICATES
                standard_error = float(np.sqrt(rate * (1.0 - rate) / N_REPLICATES))
                rows.append(
                    {
                        "seed": seed,
                        "rho": rho,
                        "configuration": configuration,
                        "n_replicates": N_REPLICATES,
                        "n_reject": rejects,
                        "rejection_rate": rate,
                        "mc_standard_error": standard_error,
                        "upper_two_se": rate + 2.0 * standard_error,
                        "gate_pass": rate <= NULL_GATE,
                    }
                )
    frame = pd.DataFrame(rows)
    frame.to_csv(OUT / "null_calibration.tsv", sep="\t", index=False)
    maximum = float(frame["rejection_rate"].max())
    passed = bool(frame["gate_pass"].all())
    summary = {
        "synthetic": True,
        "purpose": "partial-conjunction implementation calibration; no biological claim",
        "n_families": int(len(frame) * N_REPLICATES),
        "seeds": list(SEEDS),
        "rhos": list(RHOS),
        "configurations": ["all_null", "one_arbitrarily_nonnull"],
        "alpha": ALPHA,
        "null_gate": NULL_GATE,
        "maximum_rejection_rate": maximum,
        "maximum_upper_two_se": float(frame["upper_two_se"].max()),
        "overall_status": "PASS" if passed else "FAIL",
        "verdict": "FIXED_FAMILY_REPLICABILITY_GATE_CALIBRATED" if passed else "CALIBRATION_FAILED",
        "interpretation_boundary": "fixed complete family only; no optional stopping, adaptive family size, or MS evidence",
    }
    (OUT / "replicability_calibration_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
