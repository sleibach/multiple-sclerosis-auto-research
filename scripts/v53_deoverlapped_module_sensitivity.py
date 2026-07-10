#!/usr/bin/env python3
"""Test V26 perturbation dependencies after removing shared readout genes.

This is a sensitivity analysis only. It does not alter frozen module definitions
or any locked rule.
"""

from __future__ import annotations

import ast
import csv
import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
MODULE_SCRIPT = ROOT / "scripts/v3_analyze_mixscale_perturbseq.py"
GENE_EFFECTS = ROOT / "phases/v3/results/mixscale/mixscale_readout_gene_effects.tsv"
V26_MATRIX = ROOT / "analysis/v26_deep_structure/perturbation_module_matrix.tsv"
OUT = ROOT / "analysis/v53_deoverlapped_module_sensitivity"
MODULES = (
    "gilt_lysosomal_apc",
    "hla_ii_apc",
    "ifn_apc",
    "mif_cd74_receptor_state",
)
SEED = 53201
N_PERMUTATIONS = 20_000
N_BOOTSTRAP = 5_000


def literal_assignment(path: Path, name: str) -> Any:
    tree = ast.parse(path.read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
                return ast.literal_eval(node.value)
    raise KeyError(name)


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


def build_matrix(gene_sets: dict[str, list[str]]) -> pd.DataFrame:
    effects = pd.read_csv(GENE_EFFECTS, sep="\t")
    rows = []
    for module, genes in gene_sets.items():
        subset = effects[effects["gene"].isin(genes)].copy()
        per_cell = (
            subset.groupby(["pathway", "perturbation", "cell_type"], as_index=False)["log2fc"]
            .mean()
            .rename(columns={"log2fc": "module_effect"})
        )
        summary = per_cell.groupby(["pathway", "perturbation"], as_index=False)[
            "module_effect"
        ].mean()
        summary["module"] = module
        rows.append(summary)
    combined = pd.concat(rows, ignore_index=True)
    matrix = combined.pivot(
        index=["pathway", "perturbation"], columns="module", values="module_effect"
    )
    matrix.index = [f"{pathway}:{perturbation}" for pathway, perturbation in matrix.index]
    return matrix.reindex(columns=MODULES)


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


def main() -> int:
    module_genes: dict[str, list[str]] = literal_assignment(MODULE_SCRIPT, "READOUT_MODULES")
    membership_count: dict[str, int] = {}
    for genes in module_genes.values():
        for gene in set(genes):
            membership_count[gene] = membership_count.get(gene, 0) + 1
    unique_genes = {
        module: [gene for gene in genes if membership_count[gene] == 1]
        for module, genes in module_genes.items()
        if module in MODULES
    }

    rebuilt = build_matrix({module: module_genes[module] for module in MODULES})
    unique = build_matrix(unique_genes)
    original = pd.read_csv(V26_MATRIX, sep="\t", index_col=0).reindex(columns=MODULES)
    rebuilt = rebuilt.reindex(original.index)
    max_rebuild_error = float(np.nanmax(np.abs(rebuilt.to_numpy() - original.to_numpy())))
    if max_rebuild_error > 1e-10:
        raise RuntimeError(f"Original module rebuild does not match V26: {max_rebuild_error}")

    rng = np.random.default_rng(SEED)
    pairs = list(itertools.combinations(MODULES, 2))
    result_rows = []
    raw_p_values = []
    stratified_p_values = []
    original_stratified_p_values = []
    for left, right in pairs:
        complete = original[[left, right]].notna().all(axis=1) & unique[[left, right]].notna().all(axis=1)
        original_left = original.loc[complete, left].to_numpy(dtype=float)
        original_right = original.loc[complete, right].to_numpy(dtype=float)
        unique_left = unique.loc[complete, left].to_numpy(dtype=float)
        unique_right = unique.loc[complete, right].to_numpy(dtype=float)
        original_rho = safe_spearman(original_left, original_right)
        unique_rho = safe_spearman(unique_left, unique_right)

        labels = np.asarray(original.index[complete], dtype=str)
        stimuli = np.asarray([label.split(":", 1)[0] for label in labels])
        null = np.empty(N_PERMUTATIONS, dtype=float)
        stratified_null = np.empty(N_PERMUTATIONS, dtype=float)
        original_stratified_null = np.empty(N_PERMUTATIONS, dtype=float)
        for index in range(N_PERMUTATIONS):
            null[index] = abs(safe_spearman(unique_left, rng.permutation(unique_right)))
            unique_permuted = unique_right.copy()
            original_permuted = original_right.copy()
            for stimulus in np.unique(stimuli):
                group = np.flatnonzero(stimuli == stimulus)
                permutation = rng.permutation(len(group))
                unique_permuted[group] = unique_right[group[permutation]]
                original_permuted[group] = original_right[group[permutation]]
            stratified_null[index] = abs(safe_spearman(unique_left, unique_permuted))
            original_stratified_null[index] = abs(
                safe_spearman(original_left, original_permuted)
            )
        empirical_p = (1 + int(np.sum(null >= abs(unique_rho)))) / (N_PERMUTATIONS + 1)
        stratified_p = (
            1 + int(np.sum(stratified_null >= abs(unique_rho)))
        ) / (N_PERMUTATIONS + 1)
        original_stratified_p = (
            1 + int(np.sum(original_stratified_null >= abs(original_rho)))
        ) / (N_PERMUTATIONS + 1)
        raw_p_values.append(empirical_p)
        stratified_p_values.append(stratified_p)
        original_stratified_p_values.append(original_stratified_p)

        bootstrap_delta = np.empty(N_BOOTSTRAP, dtype=float)
        for index in range(N_BOOTSTRAP):
            sample = rng.integers(0, len(unique_left), size=len(unique_left))
            bootstrap_delta[index] = safe_spearman(
                unique_left[sample], unique_right[sample]
            ) - safe_spearman(original_left[sample], original_right[sample])

        stimulus_rhos = {}
        for stimulus in ("IFNB", "IFNG", "TNFA"):
            mask = np.array([label.startswith(f"{stimulus}:") for label in original.index[complete]])
            stimulus_rhos[stimulus] = safe_spearman(unique_left[mask], unique_right[mask])

        result_rows.append(
            {
                "module_a": left,
                "module_b": right,
                "n_signatures": len(unique_left),
                "original_spearman": original_rho,
                "globally_unique_gene_spearman": unique_rho,
                "rho_delta_unique_minus_original": unique_rho - original_rho,
                "paired_bootstrap_delta_ci_low": float(np.nanquantile(bootstrap_delta, 0.025)),
                "paired_bootstrap_delta_ci_high": float(np.nanquantile(bootstrap_delta, 0.975)),
                "unique_empirical_permutation_p": empirical_p,
                "unique_within_stimulus_permutation_p": stratified_p,
                "original_within_stimulus_permutation_p": original_stratified_p,
                "unique_IFNB_spearman": stimulus_rhos["IFNB"],
                "unique_IFNG_spearman": stimulus_rhos["IFNG"],
                "unique_TNFA_spearman": stimulus_rhos["TNFA"],
            }
        )

    q_values = bh_adjust(raw_p_values)
    stratified_q_values = bh_adjust(stratified_p_values)
    original_stratified_q_values = bh_adjust(original_stratified_p_values)
    for row, q_value, stratified_q, original_stratified_q in zip(
        result_rows,
        q_values,
        stratified_q_values,
        original_stratified_q_values,
        strict=True,
    ):
        row["unique_q_bh_six_pairs"] = q_value
        row["unique_within_stimulus_q_bh_six_pairs"] = stratified_q
        row["original_within_stimulus_q_bh_six_pairs"] = original_stratified_q
        row["survives_deoverlap_gate"] = (
            abs(float(row["globally_unique_gene_spearman"])) >= 0.5
            and q_value <= 0.10
            and stratified_q <= 0.10
            and int(row["n_signatures"]) >= 18
        )

    target = next(
        row
        for row in result_rows
        if {row["module_a"], row["module_b"]}
        == {"hla_ii_apc", "mif_cd74_receptor_state"}
    )
    target_persists = bool(target["survives_deoverlap_gate"])
    attenuation_established = float(target["paired_bootstrap_delta_ci_high"]) < 0
    summary = {
        "purpose": "V53 perturbation-module dependency sensitivity after removing every shared readout gene",
        "input": str(GENE_EFFECTS.relative_to(ROOT)),
        "seed": SEED,
        "n_permutations_per_pair": N_PERMUTATIONS,
        "n_paired_bootstrap": N_BOOTSTRAP,
        "max_absolute_original_rebuild_error": max_rebuild_error,
        "unique_gene_counts": {module: len(genes) for module, genes in unique_genes.items()},
        "hla_mif_original_spearman": target["original_spearman"],
        "hla_mif_unique_spearman": target["globally_unique_gene_spearman"],
        "hla_mif_unique_q_bh": target["unique_q_bh_six_pairs"],
        "hla_mif_unique_within_stimulus_q_bh": target[
            "unique_within_stimulus_q_bh_six_pairs"
        ],
        "hla_mif_original_within_stimulus_q_bh": target[
            "original_within_stimulus_q_bh_six_pairs"
        ],
        "hla_mif_attenuation_established_by_paired_bootstrap": attenuation_established,
        "hla_mif_survives_deoverlap_gate": target_persists,
        "global_coupled_axis_status_changed": False,
        "verdict": (
            "PERTURBATION_HLA_MIF_EDGE_PERSISTS_WITH_DISJOINT_READOUTS_AND_STIMULUS_CONTROL_GLOBAL_STATUS_UNCHANGED"
            if target_persists
            else "PERTURBATION_HLA_MIF_GLOBAL_ASSOCIATION_FAILS_STIMULUS_CONTROL_GLOBAL_STATUS_UNCHANGED"
        ),
        "boundary": "Only the held Mixscale perturbation modality is recomputed. The multi-modality V26 coupled-axis status is not re-estimated or changed by this sensitivity.",
    }

    gene_rows = []
    for module in MODULES:
        original_genes = list(module_genes[module])
        retained = unique_genes[module]
        gene_rows.append(
            {
                "module": module,
                "n_original_genes": len(original_genes),
                "n_globally_unique_genes": len(retained),
                "globally_unique_genes": ";".join(retained) or "none",
                "removed_shared_genes": ";".join(
                    gene for gene in original_genes if gene not in retained
                )
                or "none",
            }
        )

    OUT.mkdir(parents=True, exist_ok=True)
    rebuilt.to_csv(OUT / "rebuilt_original_module_matrix.tsv", sep="\t")
    unique.to_csv(OUT / "globally_unique_gene_module_matrix.tsv", sep="\t")
    write_tsv(OUT / "module_gene_partition.tsv", gene_rows)
    write_tsv(OUT / "dependency_sensitivity.tsv", result_rows)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 De-overlapped APC Module Sensitivity",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"The gene-level rebuild matches the committed V26 perturbation matrix to a maximum",
        f"absolute error of `{max_rebuild_error:.3g}`. Every gene appearing in more than one",
        "module was then removed before recomputing all 24 signatures.",
        "",
        f"For HLA-II/APC versus receptor-state, Spearman rho changes from",
        f"`{float(target['original_spearman']):.3f}` to",
        f"`{float(target['globally_unique_gene_spearman']):.3f}`; the six-pair BH q-value is",
        f"`{float(target['unique_q_bh_six_pairs']):.4f}` under a global shuffle but",
        f"`{float(target['unique_within_stimulus_q_bh_six_pairs']):.4f}` when labels are",
        "shuffled only within cytokine stimuli. The paired-bootstrap attenuation interval",
        f"is `{float(target['paired_bootstrap_delta_ci_low']):.3f}` to",
        f"`{float(target['paired_bootstrap_delta_ci_high']):.3f}`. The result is a sensitivity for the",
        "perturbation modality only. It does not edit the modules or change the V26",
        "multi-modality architecture by itself.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
