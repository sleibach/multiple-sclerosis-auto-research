#!/usr/bin/env python3
"""Resolve the independent-cluster count boundary for the V57 cluster-e rule."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import ndtr

from v57_dependent_site_eprocess_probe import ROOT, summarize
from v57_dependent_site_evalue_probe import cluster_e_path


DEFAULT_OUT = ROOT / "analysis/v57_dependence_cluster_count"
PLAN = "docs/plans/V57_DEPENDENCE_CLUSTER_COUNT_PLAN.md"
SEEDS = (57171, 57172, 57173)
CLUSTER_COUNTS = (3, 4, 5, 6)
CLUSTER_SIZE = 4
CORRELATION = 0.75
SHAPES = (1.0, 0.25)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--sequences", type=int, default=100_000)
    return parser.parse_args()


def generate(
    rng: np.random.Generator,
    n_sequences: int,
    n_clusters: int,
    beta_shape: float,
) -> np.ndarray:
    common = rng.normal(size=(n_sequences, n_clusters, 1))
    independent = rng.normal(size=(n_sequences, n_clusters, CLUSTER_SIZE))
    latent = np.sqrt(CORRELATION) * common + np.sqrt(1.0 - CORRELATION) * independent
    return ndtr(latent) ** (1.0 / beta_shape)


def main() -> None:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for seed in SEEDS:
        for n_clusters in CLUSTER_COUNTS:
            for beta_shape in SHAPES:
                rng = np.random.default_rng(seed + n_clusters * 1000 + int(beta_shape * 10_000))
                p_values = generate(rng, args.sequences, n_clusters, beta_shape)
                crossing, final_q90, maximum_q95 = summarize(cluster_e_path(p_values))
                rows.append(
                    {
                        "seed": seed,
                        "n_independent_clusters": n_clusters,
                        "nominal_sites": n_clusters * CLUSTER_SIZE,
                        "cluster_size": CLUSTER_SIZE,
                        "within_cluster_correlation": CORRELATION,
                        "beta_shape": beta_shape,
                        "n_sequences": args.sequences,
                        "ever_crossing": crossing,
                        "final_e_q90": final_q90,
                        "maximum_e_q95": maximum_q95,
                    }
                )
    results = pd.DataFrame(rows)
    boundaries: list[dict[str, object]] = []
    first_pass: dict[str, object] | None = None
    for n_clusters in CLUSTER_COUNTS:
        cell = results[results.n_independent_clusters.eq(n_clusters)]
        null = cell[cell.beta_shape.eq(1.0)]
        strong = cell[cell.beta_shape.eq(0.25)]
        null_pass = bool(null.ever_crossing.le(0.055).all())
        strong_pass = bool(strong.ever_crossing.ge(0.75).all())
        row = {
            "n_independent_clusters": n_clusters,
            "nominal_sites": n_clusters * CLUSTER_SIZE,
            "maximum_seed_null_crossing": float(null.ever_crossing.max()),
            "minimum_seed_strong_crossing": float(strong.ever_crossing.min()),
            "null_gate": null_pass,
            "strong_power_gate": strong_pass,
            "status": "PASS" if null_pass and strong_pass else "FAIL",
        }
        boundaries.append(row)
        if first_pass is None and row["status"] == "PASS":
            first_pass = row
    summary = {
        "synthetic": True,
        "purpose": "Independent dependence-cluster count sizing; no MS biological evidence",
        "plan": PLAN,
        "seeds": list(SEEDS),
        "sequences_per_cell": args.sequences,
        "total_sequences": len(SEEDS) * len(CLUSTER_COUNTS) * len(SHAPES) * args.sequences,
        "cluster_size": CLUSTER_SIZE,
        "within_cluster_correlation": CORRELATION,
        "first_all_seed_pass": first_pass,
        "overall_status": "PASS" if first_pass is not None else "FAIL",
        "verdict": "INDEPENDENT_CLUSTER_COUNT_BOUNDARY_RESOLVED" if first_pass is not None else "INDEPENDENT_CLUSTER_COUNT_BOUNDARY_UNRESOLVED",
        "interpretation_boundary": "Conditional synthetic boundary; real overlap declaration and cross-cluster independence remain required.",
    }
    results.to_csv(outdir / "dependence_cluster_count_results.tsv", sep="\t", index=False)
    pd.DataFrame(boundaries).to_csv(outdir / "dependence_cluster_count_boundary.tsv", sep="\t", index=False)
    (outdir / "dependence_cluster_count_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
