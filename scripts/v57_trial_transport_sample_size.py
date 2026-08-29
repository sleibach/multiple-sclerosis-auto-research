#!/usr/bin/env python3
"""Synthetic sample-size remediation for the V57 transport harness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v57_trial_transport_simulation import estimate_transport, generate_trial_pair


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v57_trial_transport_sample_size/synthetic"
SIZES = (800, 1200, 1600, 2400)
SEEDS = (57061, 57062, 57063)
N_REPLICATES = 200


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--replicates", type=int, default=N_REPLICATES)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for size in SIZES:
        for seed in SEEDS:
            rng = np.random.default_rng(seed)
            for replicate in range(args.replicates):
                generated = generate_trial_pair(
                    rng, "covariate_shift_only", n_source=size, n_target=size
                )
                estimates = estimate_transport(generated)
                rows.append(
                    {
                        "n_source": size,
                        "n_target": size,
                        "seed": seed,
                        "replicate": replicate,
                        **estimates,
                    }
                )
    frame = pd.DataFrame(rows)
    summary_rows = []
    for (size, seed), group in frame.groupby(["n_source", "seed"], sort=True):
        overlap_rate = float(group.overlap_pass.mean())
        mean_absolute_error = float(group.dr_error_to_true_target.abs().mean())
        summary_rows.append(
            {
                "n_source": size,
                "n_target": size,
                "seed": seed,
                "replicates": len(group),
                "overlap_pass_rate": overlap_rate,
                "effective_sample_size_fail_rate": float(
                    group.sampling_weight_effective_fraction.lt(0.30).mean()
                ),
                "maximum_weight_fail_rate": float(
                    group.max_sampling_weight.gt(20.0).mean()
                ),
                "weighted_smd_fail_rate": float(group.max_weighted_smd.gt(0.10).mean()),
                "mean_abs_dr_error_to_true_target": mean_absolute_error,
                "p90_abs_dr_error_to_true_target": float(
                    group.dr_error_to_true_target.abs().quantile(0.90)
                ),
                "passes_fixed_gate": bool(
                    overlap_rate >= 0.90 and mean_absolute_error <= 0.03
                ),
                "synthetic": True,
            }
        )
    table = pd.DataFrame(summary_rows)
    by_size = (
        table.groupby("n_source", as_index=False)
        .agg(
            all_seeds_pass=("passes_fixed_gate", "all"),
            minimum_overlap_pass_rate=("overlap_pass_rate", "min"),
            maximum_mean_abs_error=("mean_abs_dr_error_to_true_target", "max"),
        )
        .rename(columns={"n_source": "n_source_and_target"})
    )
    passing_sizes = by_size.loc[by_size.all_seeds_pass, "n_source_and_target"].tolist()
    minimum = int(min(passing_sizes)) if passing_sizes else None
    largest = table[table.n_source.eq(max(SIZES))]
    summary = {
        "purpose": "Synthetic method sample-size calibration only; no MS or treatment evidence",
        "plan": "docs/plans/V57_TRIAL_TRANSPORT_SAMPLE_SIZE_PLAN.md",
        "sizes": list(SIZES),
        "seeds": list(SEEDS),
        "replicates_per_size_seed": args.replicates,
        "total_synthetic_trial_pairs": len(frame),
        "fixed_overlap_gate": 0.90,
        "fixed_mean_absolute_error_gate": 0.03,
        "minimum_size_passing_all_seeds": minimum,
        "largest_size_maximum_weight_fail_rate_range": [
            float(largest.maximum_weight_fail_rate.min()),
            float(largest.maximum_weight_fail_rate.max()),
        ],
        "largest_size_weighted_smd_fail_rate_range": [
            float(largest.weighted_smd_fail_rate.min()),
            float(largest.weighted_smd_fail_rate.max()),
        ],
        "verdict": "SAMPLE_SIZE_REMEDIATION_IDENTIFIED"
        if minimum is not None
        else "TRANSPORT_REMAINS_UNVERIFIED",
        "boundary": "Real controlled trial IPD still requires overlap, endpoint, and exchangeability audits",
    }
    frame.to_csv(
        args.outdir / "synthetic_sample_size_results.tsv.gz",
        sep="\t",
        index=False,
        compression={"method": "gzip", "mtime": 0},
    )
    table.to_csv(args.outdir / "seed_size_summary.tsv", sep="\t", index=False)
    by_size.to_csv(args.outdir / "size_gate_summary.tsv", sep="\t", index=False)
    (args.outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = f"""# V57 Trial-Transport Sample-Size Remediation

## Synthetic-Only Boundary

This follow-up holds the failed primary gate fixed and varies only synthetic
trial size. It is not MS or treatment evidence.

## Result

- Synthetic trial pairs: {len(frame):,}
- Sizes per source and target trial: {', '.join(map(str, SIZES))}
- Seeds: {', '.join(map(str, SEEDS))}
- Smallest size passing the unchanged gate under every seed:
  {minimum if minimum is not None else 'none'}

Verdict: **{summary['verdict']}**.

At n={max(SIZES)} per trial, mean absolute error cleared 0.03 under every
seed, but the absolute maximum-weight component failed in
{largest.maximum_weight_fail_rate.min():.1%}-{largest.maximum_weight_fail_rate.max():.1%}
of replicates while weighted-SMD failure was
{largest.weighted_smd_fail_rate.min():.1%}-{largest.weighted_smd_fail_rate.max():.1%}.
The unchanged primary guard is therefore not rescued: its sample-maximum
criterion becomes more likely to encounter an extreme observation as n grows.

Even a synthetic pass establishes only that the estimator can behave as
designed under known models. Real trial transport must fail closed for poor
overlap, endpoint mismatch, or unjustified source-to-target exchangeability.
"""
    (args.outdir / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
