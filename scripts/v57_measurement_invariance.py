#!/usr/bin/env python3
"""Cross-environment gene-correlation measurement-invariance audit for V57."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata

import v32_confounder_audit as v32
from v57_v22_gene_influence import prepare


MODULES = {
    "IFN_APC": tuple(v32.IFN_APC),
    "HLAII": tuple(v32.HLAII),
    "UNION_EXPLORATORY": tuple(sorted(set(v32.IFN_APC) | set(v32.HLAII))),
}
PRIMARY = ("IFN_APC", "HLAII")
BOOTSTRAP_SEEDS = (5711, 5712, 5713)
N_BOOTSTRAP = 10_000
N_UNION_PERMUTATIONS = 200_000


def spearman_matrix(values: np.ndarray) -> np.ndarray:
    ranked = np.apply_along_axis(rankdata, 0, values)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.corrcoef(ranked, rowvar=False)


def edge_vector(matrix: np.ndarray) -> np.ndarray:
    return matrix[np.triu_indices(matrix.shape[0], k=1)]


def edge_concordance(first: np.ndarray, second: np.ndarray) -> float:
    a = edge_vector(first)
    b = edge_vector(second)
    if not np.isfinite(a).all() or not np.isfinite(b).all() or np.std(a) == 0 or np.std(b) == 0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def gene_label_null(
    first: np.ndarray,
    second: np.ndarray,
    module: str,
) -> tuple[float, int, dict[str, float]]:
    observed = edge_concordance(first, second)
    n_genes = first.shape[0]
    if module in PRIMARY:
        permutations = itertools.permutations(range(n_genes))
    else:
        rng = np.random.default_rng(5714)
        permutations = (rng.permutation(n_genes) for _ in range(N_UNION_PERMUTATIONS))
    count = 0
    total = 0
    values = []
    for permutation in permutations:
        idx = np.asarray(permutation, dtype=int)
        value = edge_concordance(first, second[np.ix_(idx, idx)])
        if np.isfinite(value):
            count += int(value >= observed - 1e-12)
            total += 1
            values.append(value)
    return count / total, total, {
        "null_q95": float(np.quantile(values, 0.95)),
        "null_max": float(np.max(values)),
    }


def bootstrap_concordance(
    first_values: np.ndarray,
    second_values: np.ndarray,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(N_BOOTSTRAP):
        first_idx = rng.integers(0, len(first_values), len(first_values))
        second_idx = rng.integers(0, len(second_values), len(second_values))
        value = edge_concordance(
            spearman_matrix(first_values[first_idx]),
            spearman_matrix(second_values[second_idx]),
        )
        if np.isfinite(value):
            out.append(value)
    return np.asarray(out)


def run(outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    frames = {}
    for cohort in (v32.load_gse235(), v32.load_gse253006()):
        frame, _ = prepare(cohort)
        frames[cohort.cohort] = frame
    cohort_names = list(frames)

    metric_rows = []
    bootstrap_rows = []
    for module, genes in MODULES.items():
        first_values = frames[cohort_names[0]][list(genes)].to_numpy(float)
        second_values = frames[cohort_names[1]][list(genes)].to_numpy(float)
        first_matrix = spearman_matrix(first_values)
        second_matrix = spearman_matrix(second_values)
        observed = edge_concordance(first_matrix, second_matrix)
        permutation_p, n_permutations, null = gene_label_null(first_matrix, second_matrix, module)
        lower_bounds = []
        for seed in BOOTSTRAP_SEEDS:
            boot = bootstrap_concordance(first_values, second_values, seed)
            low, high = np.quantile(boot, [0.025, 0.975])
            lower_bounds.append(float(low))
            bootstrap_rows.append(
                {
                    "module": module,
                    "seed": seed,
                    "n_valid_bootstraps": len(boot),
                    "median": float(np.median(boot)),
                    "ci_low": float(low),
                    "ci_high": float(high),
                    "fraction_above_zero": float(np.mean(boot > 0)),
                }
            )
        module_pass = bool(
            module in PRIMARY
            and observed >= 0.50
            and permutation_p < 0.025
            and min(lower_bounds) > 0
        )
        metric_rows.append(
            {
                "module": module,
                "n_genes": len(genes),
                "n_edges": len(genes) * (len(genes) - 1) // 2,
                "edge_concordance": observed,
                "gene_label_permutation_p": permutation_p,
                "n_gene_label_permutations": n_permutations,
                "null_q95": null["null_q95"],
                "bootstrap_min_ci_low": min(lower_bounds),
                "primary_module_pass": module_pass if module in PRIMARY else "not_applicable",
            }
        )

    metrics = pd.DataFrame(metric_rows)
    bootstrap = pd.DataFrame(bootstrap_rows)
    metrics.to_csv(outdir / "module_concordance.tsv", sep="\t", index=False)
    bootstrap.to_csv(outdir / "bootstrap_stability.tsv", sep="\t", index=False)
    primary_pass = metrics[metrics["module"].isin(PRIMARY)]["primary_module_pass"].astype(bool)
    global_pass = bool(primary_pass.all())
    summary = {
        "purpose": "cross-environment measurement-architecture audit; no new rule or biological claim",
        "cohorts": {name: len(frame) for name, frame in frames.items()},
        "primary_modules": list(PRIMARY),
        "n_bootstraps_per_module": N_BOOTSTRAP * len(BOOTSTRAP_SEEDS),
        "global_measurement_invariance_gate": "PASS" if global_pass else "FAIL",
        "interpretation": (
            "Both frozen modules show gene-architecture concordance under the predeclared gate."
            if global_pass
            else "The bounded environments do not establish invariant internal measurement architecture for both frozen modules."
        ),
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    table_rows = []
    for row in metrics.to_dict(orient="records"):
        table_rows.append(
            f"| {row['module']} | {row['n_genes']} | {row['edge_concordance']:.3f} | "
            f"{row['gene_label_permutation_p']:.6f} | {row['bootstrap_min_ci_low']:.3f} | "
            f"{row['primary_module_pass']} |"
        )
    report = f"""# V57 Cross-Environment Measurement-Invariance Result

## Result

- Global two-module gate: **{summary['global_measurement_invariance_gate']}**.
- Cohorts: {', '.join(f'{name} n={len(frame)}' for name, frame in frames.items())}.
- Patient uncertainty: {N_BOOTSTRAP * len(BOOTSTRAP_SEEDS):,} seeded bootstrap
  resamples per module; only aggregate intervals retained.

| module | genes | edge concordance | gene-label p | minimum bootstrap CI low | primary pass |
|---|---:|---:|---:|---:|---|
{chr(10).join(table_rows)}

## Interpretation

The test asks whether the same frozen names behave as a comparable multigene
measurement across environments. It does not retest outcome performance. A
failure prevents upgrading the bounded association to a shared latent
APC/HLA-II construct from these cohorts alone; it does not erase the empirical
within-cohort score associations. Different tissue, treatment, and platform are
inseparable from environment here, so the result localizes a transportability
problem rather than identifying its cause.
"""
    (outdir / "REPORT.md").write_text(report)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path("analysis/v57_measurement_invariance"))
    args = parser.parse_args()
    run(args.outdir)


if __name__ == "__main__":
    main()
