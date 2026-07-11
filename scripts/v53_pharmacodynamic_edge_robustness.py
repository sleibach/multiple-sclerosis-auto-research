#!/usr/bin/env python3
"""Stress-test the sole V53 disjoint pharmacodynamic APC coupling edge."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "analysis/v53_pharmacodynamic_deoverlap_sensitivity"
OUT = ROOT / "analysis/v53_pharmacodynamic_edge_robustness"
ORIGINAL = INPUT_DIR / "rebuilt_original_pharmacodynamic_matrix.tsv"
UNIQUE = INPUT_DIR / "globally_unique_gene_pharmacodynamic_matrix.tsv"
LEFT = "hla_ii_apc"
RIGHT = "mif_cd74_receptor_state"
SEED = 53502
N_PERMUTATIONS = 50_000
N_BOOTSTRAP = 20_000


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def safe_spearman(left: np.ndarray, right: np.ndarray) -> float:
    if len(left) < 3 or np.std(left) == 0 or np.std(right) == 0:
        return float("nan")
    return float(stats.spearmanr(left, right).statistic)


def bh_adjust(p_values: list[float]) -> list[float]:
    order = np.argsort(p_values)
    adjusted = np.ones(len(p_values), dtype=float)
    running = 1.0
    for offset, index in enumerate(order[::-1], start=1):
        rank = len(p_values) - offset + 1
        running = min(running, p_values[int(index)] * len(p_values) / rank)
        adjusted[int(index)] = running
    return adjusted.tolist()


def center_within(values: np.ndarray, strata: np.ndarray) -> np.ndarray:
    centered = values.copy().astype(float)
    for stratum in np.unique(strata):
        group = np.flatnonzero(strata == stratum)
        centered[group] -= np.mean(centered[group])
    return centered


def rank_within(values: np.ndarray, strata: np.ndarray) -> np.ndarray:
    ranked = np.empty(len(values), dtype=float)
    for stratum in np.unique(strata):
        group = np.flatnonzero(strata == stratum)
        ranked[group] = stats.rankdata(values[group], method="average") / (len(group) + 1)
    return ranked


def stratified_permutation_p(
    left: np.ndarray,
    right: np.ndarray,
    strata: np.ndarray,
    statistic,
    rng: np.random.Generator,
) -> tuple[float, float]:
    observed = float(statistic(left, right, strata))
    null = np.empty(N_PERMUTATIONS, dtype=float)
    for iteration in range(N_PERMUTATIONS):
        permuted = right.copy()
        for stratum in np.unique(strata):
            group = np.flatnonzero(strata == stratum)
            permuted[group] = right[group[rng.permutation(len(group))]]
        null[iteration] = abs(float(statistic(left, permuted, strata)))
    p_value = (1 + int(np.sum(null >= abs(observed)))) / (N_PERMUTATIONS + 1)
    return observed, p_value


def raw_spearman(left: np.ndarray, right: np.ndarray, _: np.ndarray) -> float:
    return safe_spearman(left, right)


def centered_spearman(left: np.ndarray, right: np.ndarray, strata: np.ndarray) -> float:
    return safe_spearman(center_within(left, strata), center_within(right, strata))


def ranked_spearman(left: np.ndarray, right: np.ndarray, strata: np.ndarray) -> float:
    return safe_spearman(rank_within(left, strata), rank_within(right, strata))


def cluster_bootstrap_centered_rho(
    left: np.ndarray,
    right: np.ndarray,
    strata: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    datasets = np.unique(strata)
    draws = np.empty(N_BOOTSTRAP, dtype=float)
    for iteration in range(N_BOOTSTRAP):
        sampled_left: list[float] = []
        sampled_right: list[float] = []
        sampled_strata: list[str] = []
        for slot, dataset in enumerate(rng.choice(datasets, size=len(datasets), replace=True)):
            group = np.flatnonzero(strata == dataset)
            sample = rng.choice(group, size=len(group), replace=True)
            sampled_left.extend(left[sample])
            sampled_right.extend(right[sample])
            sampled_strata.extend([f"slot_{slot}"] * len(sample))
        draws[iteration] = centered_spearman(
            np.asarray(sampled_left),
            np.asarray(sampled_right),
            np.asarray(sampled_strata),
        )
    return draws


def main() -> int:
    original = pd.read_csv(ORIGINAL, sep="\t", index_col=0)
    unique = pd.read_csv(UNIQUE, sep="\t", index_col=0)
    if not original.index.equals(unique.index):
        raise RuntimeError("Original and disjoint matrices do not have identical context order")
    if original[[LEFT, RIGHT]].isna().any().any() or unique[[LEFT, RIGHT]].isna().any().any():
        raise RuntimeError("Robustness audit requires complete HLA-II and receptor-state coverage")

    strata = np.asarray([label.split("|", 1)[0] for label in unique.index], dtype=str)
    left = unique[LEFT].to_numpy(dtype=float)
    right = unique[RIGHT].to_numpy(dtype=float)
    rng = np.random.default_rng(SEED)

    full_rho, full_stratified_p = stratified_permutation_p(
        left, right, strata, raw_spearman, rng
    )
    centered_rho, centered_p = stratified_permutation_p(
        left, right, strata, centered_spearman, rng
    )
    ranked_rho, ranked_p = stratified_permutation_p(
        left, right, strata, ranked_spearman, rng
    )

    lodo_rows = []
    lodo_p_values = []
    for omitted in sorted(np.unique(strata)):
        keep = strata != omitted
        rho, p_value = stratified_permutation_p(
            left[keep], right[keep], strata[keep], raw_spearman, rng
        )
        centered, centered_subset_p = stratified_permutation_p(
            left[keep], right[keep], strata[keep], centered_spearman, rng
        )
        lodo_rows.append(
            {
                "omitted_dataset": omitted,
                "n_contexts_retained": int(np.sum(keep)),
                "global_spearman": rho,
                "global_stratified_permutation_p": p_value,
                "within_dataset_centered_spearman": centered,
                "centered_stratified_permutation_p": centered_subset_p,
            }
        )
        lodo_p_values.append(centered_subset_p)
    for row, q_value in zip(lodo_rows, bh_adjust(lodo_p_values), strict=True):
        row["centered_q_bh_six_lodo"] = q_value

    dataset_rows = []
    for dataset in sorted(np.unique(strata)):
        group = strata == dataset
        dataset_rows.append(
            {
                "dataset": dataset,
                "n_contexts": int(np.sum(group)),
                "within_dataset_spearman": safe_spearman(left[group], right[group]),
                "mean_hla_ii_apc": float(np.mean(left[group])),
                "mean_receptor_state": float(np.mean(right[group])),
            }
        )

    bootstrap = cluster_bootstrap_centered_rho(left, right, strata, rng)
    finite_bootstrap = bootstrap[np.isfinite(bootstrap)]
    bootstrap_ci = [
        float(np.quantile(finite_bootstrap, 0.025)),
        float(np.quantile(finite_bootstrap, 0.975)),
    ]
    lodo_min_global = min(float(row["global_spearman"]) for row in lodo_rows)
    lodo_min_centered = min(
        float(row["within_dataset_centered_spearman"]) for row in lodo_rows
    )

    # Frozen before execution: a portable edge must survive dataset centering,
    # remain directionally material under every leave-one-dataset-out deletion,
    # and have a positive dataset-cluster bootstrap lower bound.
    gate_components = {
        "full_stratified_permutation_p_le_0_10": full_stratified_p <= 0.10,
        "centered_stratified_permutation_p_le_0_10": centered_p <= 0.10,
        "all_lodo_global_rho_ge_0_30": lodo_min_global >= 0.30,
        "all_lodo_centered_rho_positive": lodo_min_centered > 0,
        "cluster_bootstrap_ci_low_positive": bootstrap_ci[0] > 0,
    }
    portable = all(gate_components.values())
    summary = {
        "purpose": "V53 stability audit of the sole disjoint pharmacodynamic HLA-II/receptor-state edge",
        "seed": SEED,
        "n_contexts": len(unique),
        "n_datasets": len(np.unique(strata)),
        "n_permutations_per_test": N_PERMUTATIONS,
        "n_cluster_bootstrap_replicates": N_BOOTSTRAP,
        "global_spearman": full_rho,
        "global_stratified_permutation_p": full_stratified_p,
        "within_dataset_centered_spearman": centered_rho,
        "centered_stratified_permutation_p": centered_p,
        "within_dataset_rank_spearman": ranked_rho,
        "ranked_stratified_permutation_p": ranked_p,
        "dataset_cluster_bootstrap_centered_rho_ci": bootstrap_ci,
        "lodo_min_global_spearman": lodo_min_global,
        "lodo_min_centered_spearman": lodo_min_centered,
        "gate_components": gate_components,
        "portable_across_dataset_gate": portable,
        "verdict": (
            "PHARMACODYNAMIC_EDGE_PORTABLE_ACROSS_DATASET_SENSITIVITIES"
            if portable
            else "PHARMACODYNAMIC_EDGE_NOT_PORTABLE_ACROSS_DATASET_SENSITIVITIES"
        ),
        "boundary": "Targeted robustness analysis of an existing V53 edge; no discovery search, locked-rule change, or therapeutic promotion.",
    }

    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "leave_one_dataset_out.tsv", lodo_rows)
    write_tsv(OUT / "dataset_components.tsv", dataset_rows)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 Pharmacodynamic Edge Robustness",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"The disjoint edge has global rho `{full_rho:.3f}` and a dataset-stratified",
        f"permutation p-value of `{full_stratified_p:.4f}`. After removing dataset",
        f"means, rho is `{centered_rho:.3f}` (`p={centered_p:.4f}`); pooled",
        f"within-dataset ranks give rho `{ranked_rho:.3f}` (`p={ranked_p:.4f}`).",
        "",
        f"The leave-one-dataset-out minimum global rho is `{lodo_min_global:.3f}`",
        f"and the minimum centered rho is `{lodo_min_centered:.3f}`. The dataset-cluster",
        f"bootstrap centered-rho interval is `[{bootstrap_ci[0]:.3f}, {bootstrap_ci[1]:.3f}]`.",
        "",
        "This is a stability test of an existing pharmacodynamic relationship. It does",
        "not establish causal direction, component specificity, treatment benefit, or a",
        "therapeutic target, and it changes no frozen rule or validation threshold.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
