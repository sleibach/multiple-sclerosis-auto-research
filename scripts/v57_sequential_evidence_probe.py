#!/usr/bin/env python3
"""Synthetic calibration of a mixture e-process for sequential cohorts."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v57_environment_stability_probe import cohort_metrics, load_data


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v57_sequential_evidence/synthetic"
SEEDS = (57081, 57082, 57083)
KAPPAS = np.array([0.25, 0.50, 0.75], dtype=np.float64)
N_SEQUENCES = 200_000
N_ARRIVALS = 20
THRESHOLD = 20.0
SCENARIOS = {
    "null_uniform": 1.0,
    "moderate_beta_0p5": 0.50,
    "strong_beta_0p25": 0.25,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--sequences", type=int, default=N_SEQUENCES)
    return parser.parse_args()


def mixture_e_path(p_values: np.ndarray) -> np.ndarray:
    clipped = np.clip(p_values, np.finfo(float).tiny, 1.0)
    log_factors = np.log(KAPPAS)[None, None, :] + (
        KAPPAS[None, None, :] - 1.0
    ) * np.log(clipped)[:, :, None]
    log_products = np.cumsum(log_factors, axis=1)
    maximum = np.max(log_products, axis=2, keepdims=True)
    return np.exp(maximum[:, :, 0]) * np.mean(
        np.exp(log_products - maximum), axis=2
    )


def scenario_summary(
    rng: np.random.Generator,
    shape: float,
    n_sequences: int,
) -> dict[str, float | int]:
    p_values = rng.beta(shape, 1.0, size=(n_sequences, N_ARRIVALS))
    path = mixture_e_path(p_values)
    crossed = path >= THRESHOLD
    ever = np.any(crossed, axis=1)
    first = np.argmax(crossed, axis=1) + 1
    first = np.where(ever, first, 0)
    maximum = np.max(path, axis=1)
    return {
        "n_sequences": n_sequences,
        "crossing_probability_by_5": float(np.mean(np.any(crossed[:, :5], axis=1))),
        "crossing_probability_by_10": float(np.mean(np.any(crossed[:, :10], axis=1))),
        "crossing_probability_by_20": float(np.mean(ever)),
        "median_first_crossing_when_crossed": float(np.median(first[ever]))
        if np.any(ever)
        else math.nan,
        "maximum_e_q50": float(np.quantile(maximum, 0.50)),
        "maximum_e_q90": float(np.quantile(maximum, 0.90)),
        "maximum_e_q95": float(np.quantile(maximum, 0.95)),
        "maximum_e_q99": float(np.quantile(maximum, 0.99)),
    }


def held_context_dry_run() -> tuple[pd.DataFrame, dict[str, Any]]:
    metrics = cohort_metrics(load_data()).sort_values("cohort").reset_index(drop=True)
    p_values = metrics.exact_one_sided_auc_p.to_numpy(float)[None, :]
    path = mixture_e_path(p_values)[0]
    frame = metrics[["cohort", "n", "auc", "exact_one_sided_auc_p"]].copy()
    frame["arrival"] = np.arange(1, len(frame) + 1)
    frame["mixture_e_value"] = path
    summary = {
        "ordered_cohorts": frame.cohort.tolist(),
        "final_mixture_e_value": float(path[-1]),
        "crossed_20": bool(np.any(path >= THRESHOLD)),
        "boundary": "Contextual heterogeneous-cohort dry run only; not confirmatory combined evidence",
    }
    return frame, summary


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        for scenario, shape in SCENARIOS.items():
            rows.append(
                {
                    "seed": seed,
                    "scenario": scenario,
                    "beta_shape": shape,
                    **scenario_summary(rng, shape, args.sequences),
                    "synthetic": True,
                }
            )
    simulation = pd.DataFrame(rows)
    null = simulation[simulation.scenario.eq("null_uniform")]
    strong = simulation[simulation.scenario.eq("strong_beta_0p25")]
    null_gate = bool(null.crossing_probability_by_20.le(0.055).all())
    strong_gate = bool(strong.crossing_probability_by_20.ge(0.80).all())
    verified = null_gate and strong_gate
    dry_run, dry_summary = held_context_dry_run()
    summary = {
        "purpose": "Synthetic sequential-method calibration; no MS biological evidence",
        "plan": "docs/plans/V57_SEQUENTIAL_EVIDENCE_PLAN.md",
        "seeds": list(SEEDS),
        "kappas": KAPPAS.tolist(),
        "threshold": THRESHOLD,
        "arrivals_per_sequence": N_ARRIVALS,
        "sequences_per_seed_scenario": args.sequences,
        "total_synthetic_sequences": len(SEEDS) * len(SCENARIOS) * args.sequences,
        "null_crossing_probability_range": [
            float(null.crossing_probability_by_20.min()),
            float(null.crossing_probability_by_20.max()),
        ],
        "strong_crossing_probability_range": [
            float(strong.crossing_probability_by_20.min()),
            float(strong.crossing_probability_by_20.max()),
        ],
        "null_gate": null_gate,
        "strong_alternative_gate": strong_gate,
        "method_verified": verified,
        "verdict": "SEQUENTIAL_EVIDENCE_HARNESS_VERIFIED"
        if verified
        else "SEQUENTIAL_EVIDENCE_HARNESS_NOT_VERIFIED",
        "held_context_dry_run": dry_summary,
    }
    simulation.to_csv(args.outdir / "synthetic_calibration.tsv", sep="\t", index=False)
    dry_run.to_csv(args.outdir / "held_context_dry_run.tsv", sep="\t", index=False)
    (args.outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    moderate = simulation[simulation.scenario.eq("moderate_beta_0p5")]
    report = f"""# V57 Sequential Cohort-Evidence Accumulator

## Synthetic-Only Calibration

- Synthetic sequences: {summary['total_synthetic_sequences']:,}
- Maximum arrivals: {N_ARRIVALS}
- Mixture e-value boundary: {THRESHOLD}
- Null crossing range by 20: {summary['null_crossing_probability_range'][0]:.4f}-
  {summary['null_crossing_probability_range'][1]:.4f}
- Moderate-alternative crossing range by 20:
  {moderate.crossing_probability_by_20.min():.3f}-{moderate.crossing_probability_by_20.max():.3f}
- Strong-alternative crossing range by 20:
  {summary['strong_crossing_probability_range'][0]:.3f}-
  {summary['strong_crossing_probability_range'][1]:.3f}

Verdict: **{summary['verdict']}**.

## Held-Context Dry Run

The four heterogeneous held cohorts finish at mixture e-value
{dry_summary['final_mixture_e_value']:.3f} and do not cross 20. This is not a
confirmatory combination because their diseases and therapies differ.

## Use

A verified harness is a future accumulation rule for independent cohorts that
test the same frozen estimand. It does not replace effect sizes, confidence
intervals, transport diagnostics, or the V42 interpretation grid, and it
cannot turn heterogeneous comparator evidence into MS validation.
"""
    (args.outdir / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
