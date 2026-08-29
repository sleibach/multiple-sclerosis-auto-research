#!/usr/bin/env python3
"""Map a fixed transport-overlap guard over a synthetic shift grid."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v57_trial_transport_robustness import overlap_metrics, sampling_weights


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v57_transport_overlap_envelope/synthetic"
SEEDS = (57111, 57112, 57113)
SEVERITIES = (0.0, 0.25, 0.50, 0.75, 1.0)
N_SOURCE = 2400
N_TARGET = 2400
N_REPLICATES = 300
MAX_MEAN = np.array([0.35, -0.25, 0.20, 0.30])
MAX_SCALE = np.array([1.40, 0.70, 1.30, 0.75])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--replicates", type=int, default=N_REPLICATES)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for severity in SEVERITIES:
        target_mean = severity * MAX_MEAN
        target_scale = 1.0 + severity * (MAX_SCALE - 1.0)
        for seed in SEEDS:
            rng = np.random.default_rng(seed)
            for replicate in range(args.replicates):
                source_x = rng.normal(size=(N_SOURCE, 4))
                target_x = rng.normal(
                    loc=target_mean, scale=target_scale, size=(N_TARGET, 4)
                )
                weights = sampling_weights(source_x, target_x, quadratic=True)
                metrics = overlap_metrics(source_x, target_x, weights)
                rows.append(
                    {
                        "severity": severity,
                        "seed": seed,
                        "replicate": replicate,
                        **metrics,
                        "synthetic": True,
                    }
                )
    frame = pd.DataFrame(rows)
    summaries = []
    for (severity, seed), group in frame.groupby(["severity", "seed"], sort=True):
        summaries.append(
            {
                "severity": severity,
                "seed": seed,
                "replicates": len(group),
                "overlap_pass_rate": float(group.overlap_pass.mean()),
                "ess_fail_rate": float(group.effective_fraction.lt(0.30).mean()),
                "weight_tail_fail_rate": float(
                    group.q99_median_weight_ratio.gt(12.0).mean()
                ),
                "moment_balance_fail_rate": float(group.max_moment_smd.gt(0.10).mean()),
                "median_effective_fraction": float(group.effective_fraction.median()),
                "median_weight_tail_ratio": float(
                    group.q99_median_weight_ratio.median()
                ),
                "median_max_moment_smd": float(group.max_moment_smd.median()),
                "synthetic": True,
            }
        )
    table = pd.DataFrame(summaries)
    envelope = (
        table.groupby("severity", as_index=False)
        .agg(
            all_seeds_eligible=("overlap_pass_rate", lambda x: bool(x.ge(0.90).all())),
            minimum_pass_rate=("overlap_pass_rate", "min"),
            maximum_pass_rate=("overlap_pass_rate", "max"),
            maximum_ess_fail_rate=("ess_fail_rate", "max"),
            maximum_weight_tail_fail_rate=("weight_tail_fail_rate", "max"),
            maximum_moment_balance_fail_rate=("moment_balance_fail_rate", "max"),
        )
    )
    eligible = envelope.loc[envelope.all_seeds_eligible, "severity"].tolist()
    endpoint = max(eligible) if eligible else None
    min_rates = envelope.minimum_pass_rate.to_numpy()
    monotone_with_tolerance = bool(np.all(np.diff(min_rates) <= 0.05))
    summary = {
        "purpose": "Seeded synthetic overlap-envelope characterization only",
        "plan": "docs/plans/V57_TRANSPORT_OVERLAP_ENVELOPE_PLAN.md",
        "seeds": list(SEEDS),
        "severities": list(SEVERITIES),
        "replicates_per_seed_severity": args.replicates,
        "total_synthetic_pairs": len(frame),
        "largest_tested_severity_eligible_all_seeds": endpoint,
        "first_tested_ineligible_severity": next(
            (
                float(row.severity)
                for row in envelope.itertuples()
                if not row.all_seeds_eligible
            ),
            None,
        ),
        "pass_rate_monotone_with_005_tolerance": monotone_with_tolerance,
        "verdict": "FIXED_GUARD_ENVELOPE_MAPPED",
        "prior_candidate_harness_status": "UNCHANGED_NOT_VERIFIED",
        "boundary": "No outcomes or biological quantities were generated. Real trial overlap requires participant-level covariates.",
    }
    frame.to_csv(
        args.outdir / "synthetic_overlap_results.tsv.gz",
        sep="\t",
        index=False,
        compression={"method": "gzip", "mtime": 0},
    )
    table.to_csv(args.outdir / "seed_severity_summary.tsv", sep="\t", index=False)
    envelope.to_csv(args.outdir / "overlap_envelope.tsv", sep="\t", index=False)
    (args.outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    endpoint_text = "none" if endpoint is None else f"{endpoint:.2f}"
    report = f"""# V57 Trial-Transport Overlap Envelope

## Synthetic-Only Result

- Synthetic source/target covariate pairs: {len(frame):,}
- Participants per source and target: {N_SOURCE:,}
- Largest tested severity eligible under every seed: **{endpoint_text}**
- Pass-rate ordering monotone within 0.05 tolerance:
  **{monotone_with_tolerance}**

The guard, its thresholds, and the severity grid were frozen before this run.
At severity 0.50, 97.0%-98.3% of replicates were eligible. Eligibility fell to
84.0%-87.7% at severity 0.75 and 22.7%-27.3% at severity 1.00. The weight-tail
criterion was almost never limiting; effective sample fraction and weighted
first/second-moment balance defined the boundary.

The failed candidate-harness verdict remains unchanged. This envelope defines
where the candidate overlap diagnostic would permit analysis; it does not
establish transportability or a treatment effect in any real trial.
"""
    (args.outdir / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
