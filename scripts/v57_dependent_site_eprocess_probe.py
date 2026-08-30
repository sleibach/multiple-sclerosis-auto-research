#!/usr/bin/env python3
"""Stress the V57 mixture e-process under correlated site p-values."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import ndtr


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v57_dependent_site_eprocess"
PLAN = "docs/plans/V57_DEPENDENT_SITE_EPROCESS_PLAN.md"
SEEDS = (57141, 57142, 57143)
KAPPAS = np.asarray((0.25, 0.50, 0.75), dtype=float)
SHAPES = (1.0, 0.5, 0.25)
CONFIGS = ((1, 0.0),) + tuple(
    (cluster_size, correlation)
    for cluster_size in (2, 3, 4)
    for correlation in (0.25, 0.50, 0.75)
)
N_SITES = 12
THRESHOLD = 20.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--sequences", type=int, default=50_000)
    return parser.parse_args()


def mixture_path(p_values: np.ndarray) -> np.ndarray:
    clipped = np.clip(p_values, np.finfo(float).tiny, 1.0)
    log_factors = np.log(KAPPAS)[None, None, :] + (
        KAPPAS[None, None, :] - 1.0
    ) * np.log(clipped)[:, :, None]
    log_products = np.cumsum(log_factors, axis=1)
    maximum = np.max(log_products, axis=2, keepdims=True)
    return np.exp(maximum[:, :, 0]) * np.mean(np.exp(log_products - maximum), axis=2)


def simulate_p_values(
    rng: np.random.Generator,
    n_sequences: int,
    cluster_size: int,
    correlation: float,
    beta_shape: float,
) -> np.ndarray:
    n_clusters = N_SITES // cluster_size
    common = rng.normal(size=(n_sequences, n_clusters, 1))
    independent = rng.normal(size=(n_sequences, n_clusters, cluster_size))
    latent = np.sqrt(correlation) * common + np.sqrt(1.0 - correlation) * independent
    uniform = ndtr(latent)
    return uniform ** (1.0 / beta_shape)


def summarize(path: np.ndarray) -> tuple[float, float, float]:
    crossed = path >= THRESHOLD
    return (
        float(np.mean(np.any(crossed, axis=1))),
        float(np.quantile(path[:, -1], 0.90)),
        float(np.quantile(np.max(path, axis=1), 0.95)),
    )


def main() -> None:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for seed in SEEDS:
        for cluster_size, correlation in CONFIGS:
            for beta_shape in SHAPES:
                rng = np.random.default_rng(
                    seed + cluster_size * 1000 + int(correlation * 100) + int(beta_shape * 10_000)
                )
                clustered = simulate_p_values(
                    rng, args.sequences, cluster_size, correlation, beta_shape
                )
                naive_p = clustered.reshape(args.sequences, N_SITES)
                guarded_p = np.max(clustered, axis=2)
                naive = summarize(mixture_path(naive_p))
                guarded = summarize(mixture_path(guarded_p))
                rows.append(
                    {
                        "seed": seed,
                        "cluster_size": cluster_size,
                        "within_cluster_correlation": correlation,
                        "beta_shape": beta_shape,
                        "n_sequences": args.sequences,
                        "naive_arrivals": N_SITES,
                        "guarded_arrivals": N_SITES // cluster_size,
                        "naive_ever_crossing": naive[0],
                        "naive_final_e_q90": naive[1],
                        "naive_maximum_e_q95": naive[2],
                        "guarded_ever_crossing": guarded[0],
                        "guarded_final_e_q90": guarded[1],
                        "guarded_maximum_e_q95": guarded[2],
                    }
                )
    results = pd.DataFrame(rows)
    null = results[results.beta_shape.eq(1.0)]
    baseline = null[(null.cluster_size.eq(1)) & (null.within_cluster_correlation.eq(0.0))]
    correlated = null[null.cluster_size.gt(1)]
    independent_gate = bool(baseline.naive_ever_crossing.le(0.055).all())
    guarded_gate = bool(correlated.guarded_ever_crossing.le(0.055).all())
    worst_index = correlated.naive_ever_crossing.idxmax()
    worst = correlated.loc[worst_index]
    strongest = results[results.beta_shape.eq(0.25)]
    summary = {
        "synthetic": True,
        "purpose": "Dependent-site sequential-evidence stress test; no MS biological evidence",
        "plan": PLAN,
        "seeds": list(SEEDS),
        "sequences_per_cell": args.sequences,
        "total_sequences": len(SEEDS) * len(CONFIGS) * len(SHAPES) * args.sequences,
        "independent_naive_null_crossing_range": [
            float(baseline.naive_ever_crossing.min()),
            float(baseline.naive_ever_crossing.max()),
        ],
        "correlated_naive_null_crossing_range": [
            float(correlated.naive_ever_crossing.min()),
            float(correlated.naive_ever_crossing.max()),
        ],
        "correlated_guarded_null_crossing_range": [
            float(correlated.guarded_ever_crossing.min()),
            float(correlated.guarded_ever_crossing.max()),
        ],
        "worst_naive_null": {
            "cluster_size": int(worst.cluster_size),
            "correlation": float(worst.within_cluster_correlation),
            "crossing": float(worst.naive_ever_crossing),
        },
        "strong_guarded_crossing_range": [
            float(strongest.guarded_ever_crossing.min()),
            float(strongest.guarded_ever_crossing.max()),
        ],
        "independent_baseline_gate": independent_gate,
        "known_cluster_guard_gate": guarded_gate,
        "overall_status": "PASS" if independent_gate and guarded_gate else "FAIL",
        "verdict": "KNOWN_DEPENDENCE_CLUSTER_GUARD_VERIFIED" if independent_gate and guarded_gate else "KNOWN_DEPENDENCE_CLUSTER_GUARD_NOT_VERIFIED",
        "interpretation_boundary": "Known clusters may be collapsed conservatively; hidden or cross-cluster dependence remains disqualifying.",
    }
    results.to_csv(outdir / "dependent_site_eprocess_results.tsv", sep="\t", index=False)
    (outdir / "dependent_site_eprocess_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
