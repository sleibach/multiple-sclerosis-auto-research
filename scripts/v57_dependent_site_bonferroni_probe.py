#!/usr/bin/env python3
"""Test Bonferroni-minimum cluster evidence under known site dependence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from v57_dependent_site_eprocess_probe import (
    CONFIGS,
    N_SITES,
    ROOT,
    SHAPES,
    mixture_path,
    simulate_p_values,
    summarize,
)
import numpy as np


DEFAULT_OUT = ROOT / "analysis/v57_dependent_site_bonferroni"
PLAN = "docs/plans/V57_DEPENDENT_SITE_BONFERRONI_PLAN.md"
SEEDS = (57151, 57152, 57153)
DEPENDENT_CONFIGS = tuple(config for config in CONFIGS if config[0] > 1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--sequences", type=int, default=50_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for seed in SEEDS:
        for cluster_size, correlation in DEPENDENT_CONFIGS:
            for beta_shape in SHAPES:
                rng = np.random.default_rng(
                    seed + cluster_size * 1000 + int(correlation * 100) + int(beta_shape * 10_000)
                )
                clustered = simulate_p_values(
                    rng, args.sequences, cluster_size, correlation, beta_shape
                )
                maximum_p = np.max(clustered, axis=2)
                bonferroni_p = np.minimum(1.0, cluster_size * np.min(clustered, axis=2))
                maximum = summarize(mixture_path(maximum_p))
                bonferroni = summarize(mixture_path(bonferroni_p))
                rows.append(
                    {
                        "seed": seed,
                        "cluster_size": cluster_size,
                        "within_cluster_correlation": correlation,
                        "beta_shape": beta_shape,
                        "n_sequences": args.sequences,
                        "cluster_arrivals": N_SITES // cluster_size,
                        "maximum_p_ever_crossing": maximum[0],
                        "maximum_p_final_e_q90": maximum[1],
                        "bonferroni_ever_crossing": bonferroni[0],
                        "bonferroni_final_e_q90": bonferroni[1],
                        "bonferroni_minus_maximum_crossing": bonferroni[0] - maximum[0],
                    }
                )
    results = pd.DataFrame(rows)
    null = results[results.beta_shape.eq(1.0)]
    strong = results[results.beta_shape.eq(0.25)]
    null_gate = bool(null.bonferroni_ever_crossing.le(0.055).all())
    strong_gate = bool(strong.bonferroni_ever_crossing.ge(0.75).all())
    dominance_gate = bool(strong.bonferroni_minus_maximum_crossing.ge(0.0).all())
    passed = null_gate and strong_gate and dominance_gate
    summary = {
        "synthetic": True,
        "purpose": "Known-dependence Bonferroni cluster remediation; no MS biological evidence",
        "plan": PLAN,
        "seeds": list(SEEDS),
        "sequences_per_cell": args.sequences,
        "total_sequences": len(SEEDS) * len(DEPENDENT_CONFIGS) * len(SHAPES) * args.sequences,
        "bonferroni_null_crossing_range": [
            float(null.bonferroni_ever_crossing.min()),
            float(null.bonferroni_ever_crossing.max()),
        ],
        "bonferroni_strong_crossing_range": [
            float(strong.bonferroni_ever_crossing.min()),
            float(strong.bonferroni_ever_crossing.max()),
        ],
        "maximum_p_strong_crossing_range": [
            float(strong.maximum_p_ever_crossing.min()),
            float(strong.maximum_p_ever_crossing.max()),
        ],
        "minimum_strong_crossing_gain": float(strong.bonferroni_minus_maximum_crossing.min()),
        "maximum_strong_crossing_gain": float(strong.bonferroni_minus_maximum_crossing.max()),
        "null_gate": null_gate,
        "strong_power_gate": strong_gate,
        "maximum_p_dominance_gate": dominance_gate,
        "overall_status": "PASS" if passed else "FAIL",
        "verdict": "BONFERRONI_DEPENDENCE_CLUSTER_RULE_VERIFIED" if passed else "BONFERRONI_DEPENDENCE_CLUSTER_RULE_NOT_VERIFIED",
        "interpretation_boundary": "Use only for truthfully declared within-cluster dependence; resulting clusters must be mutually independent.",
    }
    results.to_csv(outdir / "dependent_site_bonferroni_results.tsv", sep="\t", index=False)
    (outdir / "dependent_site_bonferroni_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
