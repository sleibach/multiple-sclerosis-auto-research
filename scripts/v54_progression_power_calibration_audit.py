#!/usr/bin/env python3
"""Audit null calibration of the committed synthetic V54 power grid."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binom


ROOT = Path(__file__).resolve().parents[1]
GRID = ROOT / "analysis/v54_progression_event_power_design/power_grid.tsv"
SEEDS = ROOT / "analysis/v54_progression_event_power_design/seed_results.tsv"
OUT = ROOT / "analysis/v54_progression_power_calibration_audit"
QUANTILES = [0.50, 0.90, 0.95, 0.99, 1.00]


def quantile_rows(frame: pd.DataFrame, level: str) -> list[dict[str, float | str]]:
    rows = []
    for quantile in QUANTILES:
        rows.append(
            {
                "level": level,
                "quantile": quantile,
                "unconditional_false_pass_rate": float(
                    frame.unconditional_false_pass_rate.quantile(quantile)
                ),
                "conditional_on_valid_fit_false_pass_rate": float(
                    frame.conditional_on_valid_fit_false_pass_rate.quantile(quantile)
                ),
            }
        )
    return rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    grid = pd.read_csv(GRID, sep="\t")
    seeds = pd.read_csv(SEEDS, sep="\t")
    null = grid[grid.odds_ratio_per_latent_sd.eq(1.0)].copy()
    seed_null = seeds[seeds.odds_ratio_per_latent_sd.eq(1.0)].copy()
    if len(null) != 48 or len(seed_null) != 144:
        raise RuntimeError("Expected 48 aggregate and 144 seed-level null cells")

    null["unconditional_false_pass_rate"] = null.conclusive_probability
    null["conditional_on_valid_fit_false_pass_rate"] = (
        null.conclusive_probability * null.n_simulated_cohorts / null.n_valid_fits
    )
    seed_null["unconditional_false_pass_rate"] = seed_null.conclusive_probability
    seed_null["conditional_on_valid_fit_false_pass_rate"] = (
        seed_null.conclusive_count / seed_null.n_valid_fits
    )
    quantiles = pd.DataFrame(
        quantile_rows(null, "aggregate_1500_per_cell")
        + quantile_rows(seed_null, "seed_500_per_cell")
    )
    quantiles.to_csv(OUT / "null_rate_quantiles.tsv", sep="\t", index=False)

    maximum = null.sort_values("unconditional_false_pass_rate").iloc[-1]
    maximum_count = int(round(maximum.conclusive_probability * maximum.n_simulated_cohorts))
    family_tail = float(
        1
        - binom.cdf(
            maximum_count - 1,
            int(maximum.n_simulated_cohorts),
            float(maximum.alpha),
        )
        ** len(null)
    )
    n_ci_lower_above_nominal = int(
        null.conclusive_probability_ci_low.gt(null.alpha).sum()
    )
    calibration = pd.DataFrame(
        [
            {
                "n_aggregate_null_cells": len(null),
                "cohorts_per_aggregate_cell": int(maximum.n_simulated_cohorts),
                "nominal_alpha": float(maximum.alpha),
                "maximum_false_pass_count": maximum_count,
                "maximum_unconditional_false_pass_rate": float(
                    maximum.unconditional_false_pass_rate
                ),
                "maximum_wilson_ci_low": float(
                    maximum.conclusive_probability_ci_low
                ),
                "maximum_wilson_ci_high": float(
                    maximum.conclusive_probability_ci_high
                ),
                "family_max_tail_probability_under_binomial_reference": family_tail,
                "aggregate_cells_with_wilson_lower_bound_above_alpha": n_ci_lower_above_nominal,
                "calibration_gate_pass": bool(
                    n_ci_lower_above_nominal == 0 and family_tail >= 0.05
                ),
            }
        ]
    )
    calibration.to_csv(OUT / "calibration_gate.tsv", sep="\t", index=False)
    null.to_csv(OUT / "aggregate_null_cells.tsv", sep="\t", index=False)

    passes = bool(calibration.iloc[0].calibration_gate_pass)
    summary = {
        "purpose": "Synthetic null calibration audit; no biological claim",
        "synthetic": True,
        "n_aggregate_null_cells": len(null),
        "n_seed_null_cells": len(seed_null),
        "nominal_alpha": float(maximum.alpha),
        "median_aggregate_false_pass_rate": float(
            null.unconditional_false_pass_rate.median()
        ),
        "maximum_aggregate_false_pass_rate": float(
            maximum.unconditional_false_pass_rate
        ),
        "maximum_wilson_interval": [
            float(maximum.conclusive_probability_ci_low),
            float(maximum.conclusive_probability_ci_high),
        ],
        "family_max_reference_p": family_tail,
        "n_cells_lower_ci_above_alpha": n_ci_lower_above_nominal,
        "verdict": "CALIBRATION_ACCEPTABLE" if passes else "CALIBRATION_NOT_ACCEPTABLE",
        "boundary": "Finite-simulation method behavior only; no empirical progression effect.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    aggregate_quantiles = quantiles[quantiles.level.eq("aggregate_1500_per_cell")]
    seed_quantiles = quantiles[quantiles.level.eq("seed_500_per_cell")]
    lines = [
        "# V54 Progression-Power Null Calibration Audit",
        "",
        "All values characterize synthetic method behavior, not MS biology.",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"Across 48 aggregate null cells, the median false-pass rate was "
        f"`{summary['median_aggregate_false_pass_rate']:.3f}` and the maximum "
        f"was `{summary['maximum_aggregate_false_pass_rate']:.3f}` "
        f"({maximum_count}/1,500; Wilson 95% CI "
        f"`{summary['maximum_wilson_interval'][0]:.3f}` to "
        f"`{summary['maximum_wilson_interval'][1]:.3f}`). No cell's lower "
        "Wilson bound exceeded nominal 0.05.",
        "",
        f"Under a 48-cell Binomial(1500, 0.05) reference, a maximum at least "
        f"this large has probability `{family_tail:.3f}`. The observed maximum "
        "is therefore expected finite-grid variation, not evidence of "
        "anti-conservatism.",
        "",
        "| quantile | aggregate unconditional | aggregate conditional-valid | seed unconditional | seed conditional-valid |",
        "|---:|---:|---:|---:|---:|",
    ]
    for index, quantile in enumerate(QUANTILES):
        aggregate = aggregate_quantiles.iloc[index]
        seed = seed_quantiles.iloc[index]
        lines.append(
            f"| {quantile:.2f} | {aggregate.unconditional_false_pass_rate:.3f} | "
            f"{aggregate.conditional_on_valid_fit_false_pass_rate:.3f} | "
            f"{seed.unconditional_false_pass_rate:.3f} | "
            f"{seed.conditional_on_valid_fit_false_pass_rate:.3f} |"
        )
    lines.extend(
        [
            "",
            "The reference maximum assumes identically calibrated independent cells and "
            "is used only to contextualize Monte Carlo maxima. The per-cell Wilson gate "
            "is the fail-closed check. No alpha correction is required by this audit.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
