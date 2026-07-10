#!/usr/bin/env python3
"""Recompute V26 treatment-response dependencies with disjoint APC modules."""

from __future__ import annotations

import csv
import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

import v3_wave75_response_state_stratification as source


ROOT = Path(__file__).resolve().parents[1]
V26_MATRIX = ROOT / "analysis/v26_deep_structure/treatment_response_module_matrix.tsv"
OUT = ROOT / "analysis/v53_treatment_response_deoverlap_sensitivity"
MODULES = ("hla_ii_apc", "ifn_apc", "lysosomal_apc", "mif_cd74_receptor_state")
SEED = 53401
N_PERMUTATIONS = 20_000
N_BOOTSTRAP = 5_000


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


def bh_adjust(p_values: list[float]) -> list[float]:
    order = np.argsort(p_values)
    adjusted = np.ones(len(p_values), dtype=float)
    running = 1.0
    for offset, index in enumerate(order[::-1], start=1):
        rank = len(p_values) - offset + 1
        running = min(running, p_values[int(index)] * len(p_values) / rank)
        adjusted[int(index)] = running
    return adjusted.tolist()


def safe_spearman(left: np.ndarray, right: np.ndarray) -> float:
    if len(left) < 3 or np.std(left) == 0 or np.std(right) == 0:
        return float("nan")
    return float(stats.spearmanr(left, right).statistic)


def globally_unique_modules(original: dict[str, list[str]]) -> dict[str, list[str]]:
    counts: dict[str, int] = {}
    for module in MODULES:
        for gene in set(original[module]):
            counts[gene] = counts.get(gene, 0) + 1
    return {
        module: [gene for gene in original[module] if counts[gene] == 1]
        for module in MODULES
    }


def matrix_from_tests(ra: pd.DataFrame, ibd: pd.DataFrame) -> pd.DataFrame:
    parts = []
    for tests in (ra, ibd):
        frame = tests[tests["module"].isin(MODULES)].copy()
        frame["row"] = (
            frame["dataset"].astype(str)
            + "|"
            + frame["cell_state"].astype(str)
            + "|"
            + frame["endpoint"].astype(str)
            + "|"
            + frame["comparison"].astype(str)
        )
        parts.append(frame)
    combined = pd.concat(parts, ignore_index=True)
    return combined.pivot_table(
        index="row", columns="module", values="effect_group_a_minus_b", aggfunc="mean"
    ).reindex(columns=MODULES)


def run_modules(modules: dict[str, list[str]]) -> dict[str, pd.DataFrame]:
    source.MODULES = modules
    ra_sample, ra_pairs, ra_genes = source.ra_tables()
    ra_tests = source.ra_tests(ra_pairs)
    ibd_sample, ibd_pairs, ibd_genes = source.ibd_scores_and_pairs()
    ibd_tests = source.ibd_tests(ibd_pairs)
    return {
        "ra_sample": ra_sample,
        "ra_pairs": ra_pairs,
        "ra_genes": ra_genes,
        "ra_tests": ra_tests,
        "ibd_sample": ibd_sample,
        "ibd_pairs": ibd_pairs,
        "ibd_genes": ibd_genes,
        "ibd_tests": ibd_tests,
        "matrix": matrix_from_tests(ra_tests, ibd_tests),
    }


def main() -> int:
    np.random.seed(SEED)
    original_modules = {module: list(source.BASE_MODULES[module]) for module in MODULES}
    unique_modules = globally_unique_modules(original_modules)
    original = run_modules(original_modules)
    unique = run_modules(unique_modules)
    source.MODULES = original_modules

    v26 = pd.read_csv(V26_MATRIX, sep="\t", index_col=0).reindex(columns=MODULES)
    original_matrix = original["matrix"].reindex(v26.index)
    unique_matrix = unique["matrix"].reindex(v26.index)
    max_matrix_error = float(np.nanmax(abs(original_matrix.to_numpy() - v26.to_numpy())))
    if max_matrix_error > 1e-10:
        raise RuntimeError(f"Original response matrix rebuild mismatch: {max_matrix_error}")

    labels = np.asarray(v26.index, dtype=str)
    strata = np.asarray(
        ["|".join(label.split("|")[::2][:2]) for label in labels], dtype=str
    )
    # The expression above produces dataset|endpoint from the four-part row key.
    strata = np.asarray(
        [f"{parts[0]}|{parts[2]}" for parts in map(lambda value: value.split("|"), labels)]
    )

    rng = np.random.default_rng(SEED)
    pair_rows = []
    global_p_values = []
    stratified_p_values = []
    original_stratified_p_values = []
    for left, right in itertools.combinations(MODULES, 2):
        complete = unique_matrix[[left, right]].notna().all(axis=1)
        o_left = original_matrix.loc[complete, left].to_numpy(dtype=float)
        o_right = original_matrix.loc[complete, right].to_numpy(dtype=float)
        u_left = unique_matrix.loc[complete, left].to_numpy(dtype=float)
        u_right = unique_matrix.loc[complete, right].to_numpy(dtype=float)
        pair_strata = strata[complete.to_numpy()]
        original_rho = safe_spearman(o_left, o_right)
        unique_rho = safe_spearman(u_left, u_right)
        global_null = np.empty(N_PERMUTATIONS, dtype=float)
        stratified_null = np.empty(N_PERMUTATIONS, dtype=float)
        original_stratified_null = np.empty(N_PERMUTATIONS, dtype=float)
        for index in range(N_PERMUTATIONS):
            global_null[index] = abs(safe_spearman(u_left, rng.permutation(u_right)))
            u_permuted = u_right.copy()
            o_permuted = o_right.copy()
            for stratum in np.unique(pair_strata):
                group = np.flatnonzero(pair_strata == stratum)
                permutation = rng.permutation(len(group))
                u_permuted[group] = u_right[group[permutation]]
                o_permuted[group] = o_right[group[permutation]]
            stratified_null[index] = abs(safe_spearman(u_left, u_permuted))
            original_stratified_null[index] = abs(safe_spearman(o_left, o_permuted))
        global_p = (1 + int(np.sum(global_null >= abs(unique_rho)))) / (N_PERMUTATIONS + 1)
        stratified_p = (
            1 + int(np.sum(stratified_null >= abs(unique_rho)))
        ) / (N_PERMUTATIONS + 1)
        original_stratified_p = (
            1 + int(np.sum(original_stratified_null >= abs(original_rho)))
        ) / (N_PERMUTATIONS + 1)
        global_p_values.append(global_p)
        stratified_p_values.append(stratified_p)
        original_stratified_p_values.append(original_stratified_p)
        bootstrap_delta = np.empty(N_BOOTSTRAP, dtype=float)
        for index in range(N_BOOTSTRAP):
            sample = rng.integers(0, len(u_left), size=len(u_left))
            bootstrap_delta[index] = safe_spearman(
                u_left[sample], u_right[sample]
            ) - safe_spearman(o_left[sample], o_right[sample])
        pair_rows.append(
            {
                "module_a": left,
                "module_b": right,
                "n_test_contexts": len(u_left),
                "original_spearman": original_rho,
                "globally_unique_gene_spearman": unique_rho,
                "rho_delta_unique_minus_original": unique_rho - original_rho,
                "paired_bootstrap_delta_ci_low": float(np.nanquantile(bootstrap_delta, 0.025)),
                "paired_bootstrap_delta_ci_high": float(np.nanquantile(bootstrap_delta, 0.975)),
                "unique_global_permutation_p": global_p,
                "unique_dataset_endpoint_stratified_p": stratified_p,
                "original_dataset_endpoint_stratified_p": original_stratified_p,
            }
        )

    global_q = bh_adjust(global_p_values)
    stratified_q = bh_adjust(stratified_p_values)
    original_stratified_q = bh_adjust(original_stratified_p_values)
    for row, global_value, stratified_value, original_value in zip(
        pair_rows, global_q, stratified_q, original_stratified_q, strict=True
    ):
        row["unique_global_q_bh_six_pairs"] = global_value
        row["unique_dataset_endpoint_stratified_q_bh_six_pairs"] = stratified_value
        row["original_dataset_endpoint_stratified_q_bh_six_pairs"] = original_value
        row["survives_deoverlap_gate"] = (
            abs(float(row["globally_unique_gene_spearman"])) >= 0.5
            and global_value <= 0.10
            and stratified_value <= 0.10
            and int(row["n_test_contexts"]) == len(v26)
        )

    target = next(
        row
        for row in pair_rows
        if {row["module_a"], row["module_b"]}
        == {"hla_ii_apc", "mif_cd74_receptor_state"}
    )
    target_persists = bool(target["survives_deoverlap_gate"])
    summary = {
        "purpose": "V53 RA/IBD treatment-response dependency sensitivity using globally disjoint module genes",
        "ra_patients": int(original["ra_pairs"]["patient"].nunique()),
        "ibd_patients": int(original["ibd_pairs"]["Patient"].nunique()),
        "n_test_contexts": len(v26),
        "max_absolute_v26_matrix_rebuild_error": max_matrix_error,
        "unique_gene_counts": {module: len(genes) for module, genes in unique_modules.items()},
        "hla_mif_original_spearman": target["original_spearman"],
        "hla_mif_unique_spearman": target["globally_unique_gene_spearman"],
        "hla_mif_unique_global_q": target["unique_global_q_bh_six_pairs"],
        "hla_mif_unique_stratified_q": target[
            "unique_dataset_endpoint_stratified_q_bh_six_pairs"
        ],
        "hla_mif_original_stratified_q": target[
            "original_dataset_endpoint_stratified_q_bh_six_pairs"
        ],
        "hla_mif_survives_deoverlap_gate": target_persists,
        "verdict": (
            "TREATMENT_RESPONSE_HLA_MIF_EDGE_PERSISTS_WITH_DISJOINT_READOUTS"
            if target_persists
            else "TREATMENT_RESPONSE_HLA_MIF_EDGE_FAILS_DISJOINT_READOUT_GATE"
        ),
        "boundary": "This recomputes the V26 RA/IBD response-test layer only; it does not alter V22 or any locked validation rule.",
    }

    gene_rows = []
    for module in MODULES:
        gene_rows.append(
            {
                "module": module,
                "n_original_genes": len(original_modules[module]),
                "n_globally_unique_genes": len(unique_modules[module]),
                "globally_unique_genes": ";".join(unique_modules[module]) or "none",
                "removed_shared_genes": ";".join(
                    gene for gene in original_modules[module] if gene not in unique_modules[module]
                )
                or "none",
            }
        )

    OUT.mkdir(parents=True, exist_ok=True)
    unique["matrix"].to_csv(OUT / "globally_unique_gene_treatment_response_matrix.tsv", sep="\t")
    unique["ra_sample"].to_csv(OUT / "ra_unique_sample_module_scores.tsv", sep="\t", index=False)
    unique["ibd_sample"].to_csv(OUT / "ibd_unique_sample_module_scores.tsv", sep="\t", index=False)
    unique["ra_tests"].to_csv(OUT / "ra_unique_response_tests.tsv", sep="\t", index=False)
    unique["ibd_tests"].to_csv(OUT / "ibd_unique_response_tests.tsv", sep="\t", index=False)
    write_tsv(OUT / "module_gene_partition.tsv", gene_rows)
    write_tsv(OUT / "dependency_sensitivity.tsv", pair_rows)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 Treatment-Response De-overlap Sensitivity",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"Held RA counts and IBD single-cell pseudobulk inputs were reprocessed under original",
        "and globally disjoint module definitions. The original 20-row V26 response matrix",
        f"reproduces to maximum absolute error `{max_matrix_error:.3g}`.",
        "",
        f"HLA-II/APC versus receptor-state rho changes from",
        f"`{float(target['original_spearman']):.3f}` to",
        f"`{float(target['globally_unique_gene_spearman']):.3f}`. The unique-score global and",
        f"dataset/endpoint-stratified q-values are",
        f"`{float(target['unique_global_q_bh_six_pairs']):.4f}` and",
        f"`{float(target['unique_dataset_endpoint_stratified_q_bh_six_pairs']):.4f}`.",
        "This sensitivity does not alter the locked V22 rule.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
