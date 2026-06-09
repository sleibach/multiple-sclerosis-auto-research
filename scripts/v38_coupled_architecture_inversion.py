#!/usr/bin/env python3
"""Adversarial inversion of the V26 coupled APC architecture.

Inversion tested: the V26 HLA-II/IFN-APC/MIF-CD74 coupling could be a generic
immune-tone/composition covariance artifact rather than a structured APC
architecture. The grounding test residualizes each context by its row-wise
module mean ("global tone") and asks whether core module-pair correlations
survive.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
V26 = ROOT / "analysis/v26_deep_structure"
V27 = ROOT / "analysis/v27_coupled_axis"
OUTDIR = ROOT / "analysis/v38_coupled_architecture_inversion"
SEED = 3806
N_PERM = 5000


MATRIX_FILES = {
    "perturbation_mixscale": V26 / "perturbation_module_matrix.tsv",
    "treatment_pharmacodynamic": V26 / "treatment_pharmacodynamic_module_matrix.tsv",
    "treatment_response_tests": V26 / "treatment_response_module_matrix.tsv",
    "cell_state_h5ad": V26 / "cell_state_module_matrix.tsv",
    "cross_disease_summary": V26 / "cross_disease_summary_module_matrix.tsv",
}

CORE_EDGES = {
    tuple(sorted(edge))
    for edge in [
        ("hla_ii_apc", "mif_cd74_receptor_state"),
        ("ifn_apc", "mif_cd74_receptor_state"),
        ("hla_ii_apc", "ifn_apc"),
        ("mif_cd74_receptor_state", "mixscale_validated_ifng_readout"),
        ("hla_ii_apc", "mixscale_validated_ifng_readout"),
        ("ifn_apc", "mixscale_validated_ifng_readout"),
        ("ifn_apc", "lysosomal_apc"),
        ("hla_ii_apc", "lysosomal_apc"),
    ]
}


def read_matrix(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", index_col=0)
    return df.apply(pd.to_numeric, errors="coerce")


def spearman(x: np.ndarray, y: np.ndarray) -> float:
    rx = average_ranks(x)
    ry = average_ranks(y)
    return pearson(rx, ry)


def average_ranks(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="mergesort")
    sorted_values = values[order]
    ranks = np.empty(len(values), dtype=float)
    i = 0
    while i < len(values):
        j = i + 1
        while j < len(values) and sorted_values[j] == sorted_values[i]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        ranks[order[i:j]] = avg_rank
        i = j
    return ranks


def pearson(x: np.ndarray, y: np.ndarray) -> float:
    if np.nanstd(x) == 0 or np.nanstd(y) == 0:
        return float("nan")
    xc = x - np.nanmean(x)
    yc = y - np.nanmean(y)
    denom = np.sqrt(np.nansum(xc * xc) * np.nansum(yc * yc))
    if denom == 0:
        return float("nan")
    return float(np.nansum(xc * yc) / denom)


def perm_p_abs_spearman(x: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> float:
    rx = average_ranks(x)
    ry = average_ranks(y)
    obs = abs(pearson(rx, ry))
    rx = rx - np.nanmean(rx)
    ry = ry - np.nanmean(ry)
    denom = np.sqrt(np.nansum(rx * rx) * np.nansum(ry * ry))
    if denom == 0:
        return 1.0
    perms = np.array([rng.permutation(len(ry)) for _ in range(N_PERM)])
    null = np.abs((ry[perms] @ rx) / denom)
    ge = int(np.sum(null >= obs - 1e-12))
    return (ge + 1.0) / (N_PERM + 1.0)


def bh_qvalues(pvalues: list[float]) -> list[float]:
    m = len(pvalues)
    order = np.argsort(pvalues)
    q = np.empty(m, dtype=float)
    running = 1.0
    for rank, idx in enumerate(order[::-1], start=1):
        true_rank = m - rank + 1
        running = min(running, pvalues[idx] * m / true_rank)
        q[idx] = running
    return q.tolist()


def edge_rows_for_matrix(name: str, matrix: pd.DataFrame) -> list[dict[str, object]]:
    rng = np.random.default_rng(SEED + len(name))
    row_mean = matrix.mean(axis=1)
    residual = matrix.sub(row_mean, axis=0)
    rows = []
    for a, b in itertools.combinations(matrix.columns, 2):
        edge = tuple(sorted((a, b)))
        raw_r = spearman(matrix[a].to_numpy(float), matrix[b].to_numpy(float))
        residual_r = spearman(residual[a].to_numpy(float), residual[b].to_numpy(float))
        raw_p = perm_p_abs_spearman(matrix[a].to_numpy(float), matrix[b].to_numpy(float), rng)
        residual_p = perm_p_abs_spearman(residual[a].to_numpy(float), residual[b].to_numpy(float), rng)
        rows.append(
            {
                "modality": name,
                "n_rows": int(matrix.shape[0]),
                "n_modules": int(matrix.shape[1]),
                "module_a": a,
                "module_b": b,
                "is_core_apc_edge": edge in CORE_EDGES,
                "raw_spearman": raw_r,
                "raw_abs_spearman": abs(raw_r),
                "raw_perm_p": raw_p,
                "row_centered_spearman": residual_r,
                "row_centered_abs_spearman": abs(residual_r),
                "row_centered_perm_p": residual_p,
                "abs_r_drop_after_row_centering": abs(raw_r) - abs(residual_r),
            }
        )
    return rows


def tone_rows_for_matrix(name: str, matrix: pd.DataFrame) -> list[dict[str, object]]:
    rng = np.random.default_rng(SEED + 100 + len(name))
    row_mean = matrix.mean(axis=1).to_numpy(float)
    rows = []
    for module in matrix.columns:
        values = matrix[module].to_numpy(float)
        r = spearman(values, row_mean)
        p = perm_p_abs_spearman(values, row_mean, rng)
        rows.append(
            {
                "modality": name,
                "module": module,
                "module_vs_row_mean_spearman": r,
                "abs_spearman": abs(r),
                "perm_p": p,
                "is_core_module": module
                in {
                    "hla_ii_apc",
                    "ifn_apc",
                    "mif_cd74_receptor_state",
                    "mixscale_validated_ifng_readout",
                    "lysosomal_apc",
                },
            }
        )
    return rows


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    edge_rows = []
    tone_rows = []
    matrix_summaries = []

    for name, path in MATRIX_FILES.items():
        matrix = read_matrix(path)
        edge_rows.extend(edge_rows_for_matrix(name, matrix))
        tone_rows.extend(tone_rows_for_matrix(name, matrix))
        matrix_summaries.append(
            {
                "modality": name,
                "rows": int(matrix.shape[0]),
                "modules": int(matrix.shape[1]),
                "source": str(path.relative_to(ROOT)),
            }
        )

    edge_df = pd.DataFrame(edge_rows)
    edge_df["row_centered_q_bh_all_edges"] = bh_qvalues(edge_df["row_centered_perm_p"].tolist())
    edge_df["raw_q_bh_all_edges"] = bh_qvalues(edge_df["raw_perm_p"].tolist())
    edge_df = edge_df.sort_values(
        ["is_core_apc_edge", "row_centered_abs_spearman", "raw_abs_spearman"],
        ascending=[False, False, False],
    )
    edge_df.to_csv(OUTDIR / "coupled_edge_residual_tests.tsv", sep="\t", index=False)

    tone_df = pd.DataFrame(tone_rows)
    tone_df["q_bh_all_module_tone_tests"] = bh_qvalues(tone_df["perm_p"].tolist())
    tone_df = tone_df.sort_values(["is_core_module", "abs_spearman"], ascending=[False, False])
    tone_df.to_csv(OUTDIR / "module_global_tone_tests.tsv", sep="\t", index=False)

    v27_metrics = pd.read_csv(V27 / "v27_scalar_vs_coupled_metrics.tsv", sep="\t")
    bounded_pooled = v27_metrics[
        (v27_metrics["subset"] == "bounded") & (v27_metrics["cohort"] == "pooled")
    ][["feature", "auc", "hedges_g", "welch_p"]]
    bounded_pooled.to_csv(OUTDIR / "v27_bounded_predictive_constraint.tsv", sep="\t", index=False)

    core = edge_df[edge_df["is_core_apc_edge"]]
    noncore = edge_df[~edge_df["is_core_apc_edge"]]
    core_raw_supported = int(((core["raw_abs_spearman"] >= 0.5) & (core["raw_perm_p"] < 0.05)).sum())
    core_residual_supported = int(
        ((core["row_centered_abs_spearman"] >= 0.5) & (core["row_centered_perm_p"] < 0.05)).sum()
    )
    residual_strong_edges = core[
        (core["row_centered_abs_spearman"] >= 0.5) & (core["row_centered_perm_p"] < 0.05)
    ][
        [
            "modality",
            "module_a",
            "module_b",
            "row_centered_spearman",
            "row_centered_perm_p",
            "row_centered_q_bh_all_edges",
        ]
    ].to_dict(orient="records")

    summary = {
        "seed": SEED,
        "n_permutations_per_edge": N_PERM,
        "matrices": matrix_summaries,
        "n_edges_tested": int(len(edge_df)),
        "n_core_edge_tests": int(len(core)),
        "n_noncore_edge_tests": int(len(noncore)),
        "core_raw_supported_abs_r_ge_0_5_p_lt_0_05": core_raw_supported,
        "core_row_centered_supported_abs_r_ge_0_5_p_lt_0_05": core_residual_supported,
        "core_median_raw_abs_r": float(core["raw_abs_spearman"].median()),
        "core_median_row_centered_abs_r": float(core["row_centered_abs_spearman"].median()),
        "noncore_median_raw_abs_r": float(noncore["raw_abs_spearman"].median()),
        "noncore_median_row_centered_abs_r": float(noncore["row_centered_abs_spearman"].median()),
        "residual_strong_core_edges": residual_strong_edges,
        "v27_bounded_pooled_auc": bounded_pooled.to_dict(orient="records"),
        "interpretation": (
            "The immune-tone inversion is only partly supported if row-centering "
            "collapses most core edges. Any residual strong HLA-II/IFN/MIF-CD74 "
            "edges support coupled architecture as more than row-wise global "
            "module tone. V27 remains a predictive constraint: coupling did not "
            "improve response prediction over the locked scalar."
        ),
    }
    with (OUTDIR / "coupled_inversion_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2)


if __name__ == "__main__":
    main()
