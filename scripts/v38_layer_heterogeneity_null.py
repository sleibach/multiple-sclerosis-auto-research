#!/usr/bin/env python3
"""Permutation null for simple disease-axis heterogeneity in the layer map.

This is a narrower adversarial test than the V38 layer-transfer inversion:
does the simple statistic "all key diseases have heterogeneous placements" look
exceptional if placement labels are randomly reassigned across the same
disease-axis table?
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v38_layer_transfer_inversion/key_disease_axis_placements.tsv"
OUTDIR = ROOT / "analysis/v38_layer_heterogeneity_null"
SEED = 3813
N_PERM = 10000

PLACEMENT_SCORE = {
    "far": 0.0,
    "intermediate": 1.0,
    "contradictory": 1.5,
    "near": 2.0,
}


def stats_for(df: pd.DataFrame) -> dict[str, float]:
    supported = df[df["grade"].isin(["supported", "robust"]) & (df["placement"] != "unresolved")]
    disease_rows = []
    for disease, sub in supported.groupby("disease"):
        scores = sub["placement"].map(PLACEMENT_SCORE).dropna()
        if len(scores) == 0:
            continue
        disease_rows.append(
            {
                "disease": disease,
                "range": float(scores.max() - scores.min()),
                "heterogeneous": bool(scores.max() - scores.min() > 0),
            }
        )
    d = pd.DataFrame(disease_rows)
    return {
        "n_diseases": int(len(d)),
        "n_heterogeneous": int(d["heterogeneous"].sum()),
        "mean_range": float(d["range"].mean()),
        "max_range": float(d["range"].max()),
    }


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT, sep="\t")
    observed = stats_for(df)

    rng = np.random.default_rng(SEED)
    placement_pool = df["placement"].to_numpy(copy=True)
    rows = []
    for _ in range(N_PERM):
        perm = df.copy()
        perm["placement"] = rng.permutation(placement_pool)
        s = stats_for(perm)
        rows.append(s)
    null = pd.DataFrame(rows)
    null.to_csv(OUTDIR / "layer_heterogeneity_null_distribution.tsv", sep="\t", index=False)

    p_n_heterogeneous = (np.sum(null["n_heterogeneous"] >= observed["n_heterogeneous"]) + 1) / (
        N_PERM + 1
    )
    p_mean_range = (np.sum(null["mean_range"] >= observed["mean_range"]) + 1) / (N_PERM + 1)
    summary = {
        "input": str(INPUT.relative_to(ROOT)),
        "seed": SEED,
        "n_permutations": N_PERM,
        "observed": observed,
        "null_n_heterogeneous_mean": float(null["n_heterogeneous"].mean()),
        "null_n_heterogeneous_p95": float(null["n_heterogeneous"].quantile(0.95)),
        "null_mean_range_mean": float(null["mean_range"].mean()),
        "null_mean_range_p95": float(null["mean_range"].quantile(0.95)),
        "empirical_p_n_heterogeneous_ge_observed": float(p_n_heterogeneous),
        "empirical_p_mean_range_ge_observed": float(p_mean_range),
        "interpretation": (
            "If this null p is high, simple disease-level heterogeneity is not "
            "itself surprising given the placement-label distribution. The "
            "layer-transfer claim should then rest on the disagreement-cell "
            "axis/compartment/causality evidence, not on heterogeneity count alone."
        ),
    }
    with (OUTDIR / "layer_heterogeneity_null_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2)


if __name__ == "__main__":
    main()
