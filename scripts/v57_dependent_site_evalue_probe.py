#!/usr/bin/env python3
"""Test averaged cluster e-factors under known within-cluster dependence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from v57_dependent_site_eprocess_probe import (
    CONFIGS,
    KAPPAS,
    N_SITES,
    ROOT,
    SHAPES,
    THRESHOLD,
    mixture_path,
    simulate_p_values,
    summarize,
)


DEFAULT_OUT = ROOT / "analysis/v57_dependent_site_evalue"
PLAN = "docs/plans/V57_DEPENDENT_SITE_EVALUE_PLAN.md"
SEEDS = (57161, 57162, 57163)
DEPENDENT_CONFIGS = tuple(config for config in CONFIGS if config[0] > 1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--sequences", type=int, default=50_000)
    return parser.parse_args()


def cluster_e_path(clustered_p: np.ndarray) -> np.ndarray:
    clipped = np.clip(clustered_p, np.finfo(float).tiny, 1.0)
    site_factors = KAPPAS[None, None, None, :] * clipped[:, :, :, None] ** (
        KAPPAS[None, None, None, :] - 1.0
    )
    cluster_factors = np.mean(site_factors, axis=2)
    log_products = np.cumsum(np.log(cluster_factors), axis=1)
    maximum = np.max(log_products, axis=2, keepdims=True)
    return np.exp(maximum[:, :, 0]) * np.mean(np.exp(log_products - maximum), axis=2)


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
                bonferroni_p = np.minimum(1.0, cluster_size * np.min(clustered, axis=2))
                bonferroni = summarize(mixture_path(bonferroni_p))
                cluster_e = summarize(cluster_e_path(clustered))
                rows.append(
                    {
                        "seed": seed,
                        "cluster_size": cluster_size,
                        "within_cluster_correlation": correlation,
                        "beta_shape": beta_shape,
                        "n_sequences": args.sequences,
                        "cluster_arrivals": N_SITES // cluster_size,
                        "bonferroni_ever_crossing": bonferroni[0],
                        "cluster_e_ever_crossing": cluster_e[0],
                        "cluster_e_final_q90": cluster_e[1],
                        "cluster_e_maximum_q95": cluster_e[2],
                        "cluster_e_minus_bonferroni_crossing": cluster_e[0] - bonferroni[0],
                    }
                )
    results = pd.DataFrame(rows)
    null = results[results.beta_shape.eq(1.0)]
    strong = results[results.beta_shape.eq(0.25)]
    null_gate = bool(null.cluster_e_ever_crossing.le(0.055).all())
    strong_gate = bool(strong.cluster_e_ever_crossing.ge(0.75).all())
    dominance_gate = bool(strong.cluster_e_minus_bonferroni_crossing.ge(0.0).all())
    passed = null_gate and strong_gate and dominance_gate
    summary = {
        "synthetic": True,
        "purpose": "Known-dependence cluster e-value remediation; no MS biological evidence",
        "plan": PLAN,
        "seeds": list(SEEDS),
        "sequences_per_cell": args.sequences,
        "total_sequences": len(SEEDS) * len(DEPENDENT_CONFIGS) * len(SHAPES) * args.sequences,
        "cluster_e_null_crossing_range": [
            float(null.cluster_e_ever_crossing.min()),
            float(null.cluster_e_ever_crossing.max()),
        ],
        "cluster_e_strong_crossing_range": [
            float(strong.cluster_e_ever_crossing.min()),
            float(strong.cluster_e_ever_crossing.max()),
        ],
        "bonferroni_strong_crossing_range": [
            float(strong.bonferroni_ever_crossing.min()),
            float(strong.bonferroni_ever_crossing.max()),
        ],
        "minimum_strong_crossing_gain": float(strong.cluster_e_minus_bonferroni_crossing.min()),
        "maximum_strong_crossing_gain": float(strong.cluster_e_minus_bonferroni_crossing.max()),
        "null_gate": null_gate,
        "strong_power_gate": strong_gate,
        "bonferroni_dominance_gate": dominance_gate,
        "overall_status": "PASS" if passed else "FAIL",
        "verdict": "DEPENDENCE_CLUSTER_E_RULE_VERIFIED" if passed else "DEPENDENCE_CLUSTER_E_RULE_NOT_VERIFIED",
        "interpretation_boundary": "Average e-factors only within truthfully declared clusters; products require independent clusters and completed arrivals.",
    }
    results.to_csv(outdir / "dependent_site_evalue_results.tsv", sep="\t", index=False)
    (outdir / "dependent_site_evalue_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
