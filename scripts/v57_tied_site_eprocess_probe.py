#!/usr/bin/env python3
"""Calibrate the frozen e-process for exact tied-score permutation p-values."""

from __future__ import annotations

import argparse
import json
import math
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v57_tied_site_eprocess"
PLAN = "docs/plans/V57_TIED_SITE_EPROCESS_PLAN.md"
SEEDS = (57131, 57132, 57133)
SITE_SPLITS = ((4, 5), (5, 5), (6, 6), (7, 7), (8, 8), (10, 10))
EFFECTS = (0.0, 0.5, 0.9)
MODES = ("exact_tied", "v42_plus_one_mc_tied")
CUTS = np.asarray((-0.841621, -0.253347, 0.253347, 0.841621))
KAPPAS = np.asarray((0.25, 0.50, 0.75), dtype=float)
N_ARRIVALS = 12
N_PERMUTATIONS = 10_000
THRESHOLD = 20.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--sequences", type=int, default=50_000)
    return parser.parse_args()


@lru_cache(maxsize=None)
def tied_tail_lookup(counts: tuple[int, ...], n_pos: int) -> np.ndarray:
    """Exact label-permutation tail probabilities indexed by doubled rank sum."""
    n = sum(counts)
    cumulative = np.cumsum(np.asarray(counts, dtype=int))
    rank2 = 2 * cumulative - np.asarray(counts, dtype=int) + 1
    maximum = n_pos * (2 * n)
    dp = np.zeros((n_pos + 1, maximum + 1), dtype=np.int64)
    dp[0, 0] = 1
    for count, rank in zip(counts, rank2, strict=True):
        updated = np.zeros_like(dp)
        for selected in range(n_pos + 1):
            occupied = np.flatnonzero(dp[selected])
            if not len(occupied):
                continue
            for take in range(min(count, n_pos - selected) + 1):
                shifted = occupied + take * int(rank)
                updated[selected + take, shifted] += dp[selected, occupied] * math.comb(count, take)
        dp = updated
    distribution = dp[n_pos].astype(float)
    assert int(distribution.sum()) == math.comb(n, n_pos)
    return np.clip(np.cumsum(distribution[::-1])[::-1] / distribution.sum(), 0.0, 1.0)


def exact_tied_p_values(pos_levels: np.ndarray, neg_levels: np.ndarray) -> np.ndarray:
    n_sequences = len(pos_levels)
    n_pos = pos_levels.shape[1]
    pos_counts = np.column_stack([(pos_levels == level).sum(axis=1) for level in range(5)])
    neg_counts = np.column_stack([(neg_levels == level).sum(axis=1) for level in range(5)])
    total = pos_counts + neg_counts
    cumulative = np.cumsum(total, axis=1)
    rank2 = 2 * cumulative - total + 1
    observed = np.sum(pos_counts * rank2, axis=1)
    unique, inverse = np.unique(total, axis=0, return_inverse=True)
    p_values = np.empty(n_sequences, dtype=float)
    for group, pattern in enumerate(unique):
        rows = inverse == group
        lookup = tied_tail_lookup(tuple(int(value) for value in pattern), n_pos)
        p_values[rows] = lookup[observed[rows]]
    return p_values


def e_factors(p_values: np.ndarray) -> np.ndarray:
    clipped = np.clip(p_values, np.finfo(float).tiny, 1.0)
    return KAPPAS[None, :] * clipped[:, None] ** (KAPPAS[None, :] - 1.0)


def mixture_path(factors: np.ndarray) -> np.ndarray:
    products = np.cumsum(np.log(factors), axis=1)
    maximum = np.max(products, axis=2, keepdims=True)
    return np.exp(maximum[:, :, 0]) * np.mean(np.exp(products - maximum), axis=2)


def simulate(
    rng: np.random.Generator,
    n_sequences: int,
    effect: float,
    mode: str,
) -> tuple[np.ndarray, list[dict[str, object]]]:
    factors = np.empty((n_sequences, N_ARRIVALS, len(KAPPAS)), dtype=float)
    diagnostics: list[dict[str, object]] = []
    for arrival in range(N_ARRIVALS):
        n_pos, n_neg = SITE_SPLITS[arrival % len(SITE_SPLITS)]
        pos = np.digitize(rng.normal(effect, 1.0, (n_sequences, n_pos)), CUTS)
        neg = np.digitize(rng.normal(0.0, 1.0, (n_sequences, n_neg)), CUTS)
        exact_p = exact_tied_p_values(pos, neg)
        if mode == "exact_tied":
            p_values = exact_p
        elif mode == "v42_plus_one_mc_tied":
            p_values = (1.0 + rng.binomial(N_PERMUTATIONS, exact_p)) / (N_PERMUTATIONS + 1.0)
        else:
            raise ValueError(mode)
        current = e_factors(p_values)
        factors[:, arrival] = current
        diagnostics.append(
            {
                "arrival": arrival + 1,
                "n_responders": n_pos,
                "n_nonresponders": n_neg,
                "mean_p": float(p_values.mean()),
                "minimum_p": float(p_values.min()),
                "maximum_mean_e_factor": float(np.mean(current, axis=0).max()),
                "mean_unique_score_levels": float(np.mean(np.sum(np.column_stack([
                    np.any(pos == level, axis=1) | np.any(neg == level, axis=1)
                    for level in range(5)
                ]), axis=1))),
            }
        )
    return mixture_path(factors), diagnostics


def main() -> None:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    diagnostic_rows: list[dict[str, object]] = []
    for seed in SEEDS:
        for mode_index, mode in enumerate(MODES):
            for effect in EFFECTS:
                rng = np.random.default_rng(seed + mode_index * 10_000 + int(effect * 1000))
                path, diagnostics = simulate(rng, args.sequences, effect, mode)
                crossed = path >= THRESHOLD
                ever = np.any(crossed, axis=1)
                rows.append(
                    {
                        "seed": seed,
                        "mode": mode,
                        "effect": effect,
                        "n_sequences": args.sequences,
                        "crossing_by_6": float(np.mean(np.any(crossed[:, :6], axis=1))),
                        "crossing_by_12": float(np.mean(ever)),
                        "final_e_q50": float(np.quantile(path[:, -1], 0.50)),
                        "final_e_q90": float(np.quantile(path[:, -1], 0.90)),
                        "maximum_e_q95": float(np.quantile(np.max(path, axis=1), 0.95)),
                    }
                )
                diagnostic_rows.extend(
                    {"seed": seed, "mode": mode, "effect": effect, **row}
                    for row in diagnostics
                )
    results = pd.DataFrame(rows)
    diagnostics = pd.DataFrame(diagnostic_rows)
    null = results[results.effect.eq(0.0)]
    strong = results[results.effect.eq(0.9)]
    null_diagnostics = diagnostics[diagnostics.effect.eq(0.0)]
    null_crossing_gate = bool(null.crossing_by_12.le(0.055).all())
    null_factor_gate = bool(null_diagnostics.maximum_mean_e_factor.le(1.01).all())
    strong_gate = bool(strong.crossing_by_12.ge(0.75).all())
    passed = null_crossing_gate and null_factor_gate and strong_gate
    summary = {
        "synthetic": True,
        "purpose": "Tied-score sequential-method calibration; no MS biological evidence",
        "plan": PLAN,
        "seeds": list(SEEDS),
        "score_levels": 5,
        "arrivals": N_ARRIVALS,
        "sequences_per_seed_effect_mode": args.sequences,
        "total_sequences": len(SEEDS) * len(MODES) * len(EFFECTS) * args.sequences,
        "total_site_records_simulated": len(SEEDS) * len(MODES) * len(EFFECTS) * args.sequences * N_ARRIVALS,
        "null_crossing_range": [float(null.crossing_by_12.min()), float(null.crossing_by_12.max())],
        "strong_crossing_range": [float(strong.crossing_by_12.min()), float(strong.crossing_by_12.max())],
        "maximum_null_mean_e_factor": float(null_diagnostics.maximum_mean_e_factor.max()),
        "null_optional_stopping_gate": null_crossing_gate,
        "null_e_factor_gate": null_factor_gate,
        "strong_power_gate": strong_gate,
        "overall_status": "PASS" if passed else "FAIL",
        "verdict": "TIED_SITE_EPROCESS_VERIFIED" if passed else "TIED_SITE_EPROCESS_NOT_VERIFIED",
        "interpretation_boundary": "Synthetic method behavior only; valid conditional permutation and independent sites remain required.",
    }
    results.to_csv(outdir / "tied_site_eprocess_results.tsv", sep="\t", index=False)
    diagnostics.to_csv(outdir / "tied_site_eprocess_diagnostics.tsv", sep="\t", index=False)
    (outdir / "tied_site_eprocess_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
