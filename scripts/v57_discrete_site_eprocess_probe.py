#!/usr/bin/env python3
"""Calibrate the frozen mixture e-process for discrete small-site p-values."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v57_discrete_site_eprocess"
PLAN = "docs/plans/V57_DISCRETE_SITE_EPROCESS_PLAN.md"
SEEDS = (57121, 57122, 57123)
SITE_SPLITS = ((4, 5), (5, 5), (6, 6), (7, 7), (8, 8), (10, 10))
EFFECTS = (0.0, 0.5, 0.9)
MODES = ("exact_discrete", "v42_plus_one_mc")
KAPPAS = np.asarray((0.25, 0.50, 0.75), dtype=float)
THRESHOLD = 20.0
N_ARRIVALS = 12
N_PERMUTATIONS = 10_000


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--sequences", type=int, default=100_000)
    return parser.parse_args()


def u_distribution(n_pos: int, n_neg: int) -> np.ndarray:
    """Return the exact tie-free null distribution of Mann-Whitney U."""
    n = n_pos + n_neg
    max_sum = n_pos * (2 * n - n_pos + 1) // 2
    counts = np.zeros((n_pos + 1, max_sum + 1), dtype=np.int64)
    counts[0, 0] = 1
    for rank in range(1, n + 1):
        upper = min(rank, n_pos)
        for chosen in range(upper, 0, -1):
            counts[chosen, rank:] += counts[chosen - 1, :-rank]
    minimum_sum = n_pos * (n_pos + 1) // 2
    u_counts = counts[n_pos, minimum_sum : minimum_sum + n_pos * n_neg + 1]
    assert int(u_counts.sum()) == math.comb(n, n_pos)
    return u_counts.astype(float) / float(u_counts.sum())


def exact_tail_lookup(n_pos: int, n_neg: int) -> tuple[np.ndarray, np.ndarray]:
    probabilities = u_distribution(n_pos, n_neg)
    tails = np.clip(np.cumsum(probabilities[::-1])[::-1], 0.0, 1.0)
    return probabilities, tails


def simulate_u(
    rng: np.random.Generator,
    n_sequences: int,
    n_pos: int,
    n_neg: int,
    effect: float,
) -> np.ndarray:
    if effect == 0.0:
        probabilities, _ = exact_tail_lookup(n_pos, n_neg)
        return rng.choice(len(probabilities), size=n_sequences, p=probabilities)
    positive = rng.normal(effect, 1.0, size=(n_sequences, n_pos))
    negative = rng.normal(0.0, 1.0, size=(n_sequences, n_neg))
    return np.sum(positive[:, :, None] > negative[:, None, :], axis=(1, 2))


def e_factors(p_values: np.ndarray) -> np.ndarray:
    clipped = np.clip(p_values, np.finfo(float).tiny, 1.0)
    return KAPPAS[None, :] * clipped[:, None] ** (KAPPAS[None, :] - 1.0)


def mixture_path(site_factors: np.ndarray) -> np.ndarray:
    log_products = np.cumsum(np.log(site_factors), axis=1)
    maximum = np.max(log_products, axis=2, keepdims=True)
    return np.exp(maximum[:, :, 0]) * np.mean(
        np.exp(log_products - maximum), axis=2
    )


def simulate(
    rng: np.random.Generator,
    n_sequences: int,
    effect: float,
    mode: str,
) -> tuple[np.ndarray, list[dict[str, object]]]:
    factors = np.empty((n_sequences, N_ARRIVALS, len(KAPPAS)), dtype=float)
    site_rows: list[dict[str, object]] = []
    for arrival in range(N_ARRIVALS):
        n_pos, n_neg = SITE_SPLITS[arrival % len(SITE_SPLITS)]
        _, tails = exact_tail_lookup(n_pos, n_neg)
        u_values = simulate_u(rng, n_sequences, n_pos, n_neg, effect)
        exact_p = tails[u_values]
        if mode == "exact_discrete":
            p_values = exact_p
        elif mode == "v42_plus_one_mc":
            exceedances = rng.binomial(N_PERMUTATIONS, exact_p)
            p_values = (1.0 + exceedances) / (N_PERMUTATIONS + 1.0)
        else:
            raise ValueError(mode)
        site_factor = e_factors(p_values)
        factors[:, arrival, :] = site_factor
        site_rows.append(
            {
                "arrival": arrival + 1,
                "n_responders": n_pos,
                "n_nonresponders": n_neg,
                "mean_p": float(np.mean(p_values)),
                "minimum_p": float(np.min(p_values)),
                "maximum_mean_e_factor": float(np.max(np.mean(site_factor, axis=0))),
            }
        )
    return mixture_path(factors), site_rows


def main() -> None:
    cli = args()
    outdir = cli.outdir if cli.outdir.is_absolute() else ROOT / cli.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    site_rows: list[dict[str, object]] = []
    for seed in SEEDS:
        for mode in MODES:
            for effect in EFFECTS:
                rng = np.random.default_rng(seed + int(effect * 1000) + 10_000 * MODES.index(mode))
                path, sites = simulate(rng, cli.sequences, effect, mode)
                crossed = path >= THRESHOLD
                ever = np.any(crossed, axis=1)
                first = np.where(ever, np.argmax(crossed, axis=1) + 1, 0)
                rows.append(
                    {
                        "seed": seed,
                        "mode": mode,
                        "effect": effect,
                        "n_sequences": cli.sequences,
                        "crossing_by_6": float(np.mean(np.any(crossed[:, :6], axis=1))),
                        "crossing_by_12": float(np.mean(ever)),
                        "median_first_crossing_when_crossed": float(np.median(first[ever])) if np.any(ever) else math.nan,
                        "final_e_q50": float(np.quantile(path[:, -1], 0.50)),
                        "final_e_q90": float(np.quantile(path[:, -1], 0.90)),
                        "maximum_e_q95": float(np.quantile(np.max(path, axis=1), 0.95)),
                    }
                )
                for site in sites:
                    site_rows.append({"seed": seed, "mode": mode, "effect": effect, **site})

    results = pd.DataFrame(rows)
    sites = pd.DataFrame(site_rows)
    null = results[results.effect.eq(0.0)]
    strong = results[results.effect.eq(0.9)]
    null_sites = sites[sites.effect.eq(0.0)]
    null_gate = bool(null.crossing_by_12.le(0.055).all())
    factor_gate = bool(null_sites.maximum_mean_e_factor.le(1.01).all())
    strong_gate = bool(strong.crossing_by_12.ge(0.80).all())
    passed = null_gate and factor_gate and strong_gate
    summary = {
        "synthetic": True,
        "purpose": "Discrete small-site sequential-method calibration; no MS biological evidence",
        "plan": PLAN,
        "seeds": list(SEEDS),
        "site_splits": [list(split) for split in SITE_SPLITS],
        "arrivals": N_ARRIVALS,
        "sequences_per_seed_effect_mode": cli.sequences,
        "total_sequences": len(SEEDS) * len(EFFECTS) * len(MODES) * cli.sequences,
        "total_site_records_simulated": len(SEEDS) * len(EFFECTS) * len(MODES) * cli.sequences * N_ARRIVALS,
        "null_crossing_range": [float(null.crossing_by_12.min()), float(null.crossing_by_12.max())],
        "strong_crossing_range": [float(strong.crossing_by_12.min()), float(strong.crossing_by_12.max())],
        "maximum_null_mean_e_factor": float(null_sites.maximum_mean_e_factor.max()),
        "null_optional_stopping_gate": null_gate,
        "null_e_factor_gate": factor_gate,
        "strong_power_gate": strong_gate,
        "overall_status": "PASS" if passed else "FAIL",
        "verdict": "DISCRETE_SITE_EPROCESS_VERIFIED" if passed else "DISCRETE_SITE_EPROCESS_NOT_VERIFIED",
        "interpretation_boundary": "Synthetic method behavior only; no site or MS evidence accumulated.",
    }
    results.to_csv(outdir / "discrete_site_eprocess_results.tsv", sep="\t", index=False)
    sites.to_csv(outdir / "discrete_site_eprocess_site_diagnostics.tsv", sep="\t", index=False)
    (outdir / "discrete_site_eprocess_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
