#!/usr/bin/env python3
"""Recompute the V26 cell-state layer with globally disjoint APC modules."""

from __future__ import annotations

import csv
import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

import v3_analyze_direct_h5ad_cell_states as source


ROOT = Path(__file__).resolve().parents[1]
COMMITTED_DONORS = ROOT / "phases/v3/results/direct_h5ad_cell_state/direct_h5ad_donor_module_scores.tsv"
V26_MATRIX = ROOT / "analysis/v26_deep_structure/cell_state_module_matrix.tsv"
OUT = ROOT / "analysis/v53_cell_state_deoverlap_sensitivity"
MODULES = ("hla_ii_apc", "ifn_apc", "lysosomal_apc", "mif_cd74_receptor_state")
SEED = 53301
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


def analyze_with_modules(
    config: source.DirectConfig,
    adata: Any,
    counts: Any,
    modules: dict[str, list[str]],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    source.MODULES = modules
    source.TARGET_GENES = sorted({gene for genes in modules.values() for gene in genes})
    donors, _, coverage = source.analyze_config(config, adata, counts)
    return donors, coverage


def comparison_matrix(donors: pd.DataFrame) -> pd.DataFrame:
    comparisons = source.compare_donors(donors)
    means = comparisons[
        (comparisons["metric"] == "mean_score") & comparisons["module"].isin(MODULES)
    ].copy()
    matrix = means.pivot_table(
        index=["analysis", "disease_name", "compartment"],
        columns="module",
        values="delta_case_minus_control",
        aggfunc="mean",
    )
    matrix.index = ["|".join(map(str, index)) for index in matrix.index]
    return matrix.reindex(columns=MODULES)


def main() -> int:
    np.random.seed(SEED)
    original_modules = {module: list(source.MODULES[module]) for module in MODULES}
    unique_modules = globally_unique_modules(original_modules)
    cache: dict[Path, tuple[Any, Any]] = {}
    original_donors = []
    unique_donors = []
    coverage_rows = []
    run_rows = []
    for config in source.CONFIGS:
        if config.path not in cache:
            cache[config.path] = source.read_counts(config.path)
        adata, counts = cache[config.path]
        original, _ = analyze_with_modules(
            config, adata, counts, original_modules
        )
        unique, coverage = analyze_with_modules(
            config, adata, counts, unique_modules
        )
        original_donors.append(original)
        unique_donors.append(unique)
        coverage_rows.append(coverage)
        run_rows.append(
            {
                "analysis": config.name,
                "dataset_path": str(config.path.relative_to(ROOT)),
                "n_original_donor_module_rows": len(original),
                "n_unique_donor_module_rows": len(unique),
                "status": "PASS",
            }
        )

    source.MODULES = original_modules
    source.TARGET_GENES = sorted(
        {gene for genes in original_modules.values() for gene in genes}
    )
    original = pd.concat(original_donors, ignore_index=True)
    unique = pd.concat(unique_donors, ignore_index=True)
    coverage = pd.concat(coverage_rows, ignore_index=True)

    committed = pd.read_csv(COMMITTED_DONORS, sep="\t")
    committed = committed[committed["module"].isin(MODULES)].copy()
    keys = ["analysis", "donor_id", "module"]
    check = original.merge(
        committed[keys + ["mean_score", "high_fraction"]],
        on=keys,
        suffixes=("_rebuilt", "_committed"),
        how="outer",
        indicator=True,
    )
    if not (check["_merge"] == "both").all():
        raise RuntimeError("Original donor rebuild does not match committed row keys")
    max_mean_error = float(
        np.nanmax(abs(check["mean_score_rebuilt"] - check["mean_score_committed"]))
    )
    max_fraction_error = float(
        np.nanmax(abs(check["high_fraction_rebuilt"] - check["high_fraction_committed"]))
    )
    if max_mean_error > 1e-10 or max_fraction_error > 1e-10:
        raise RuntimeError(
            f"Original donor rebuild mismatch: mean={max_mean_error}, fraction={max_fraction_error}"
        )

    original_matrix = comparison_matrix(original)
    unique_matrix = comparison_matrix(unique)
    v26 = pd.read_csv(V26_MATRIX, sep="\t", index_col=0).reindex(columns=MODULES)
    original_matrix = original_matrix.reindex(v26.index)
    max_matrix_error = float(
        np.nanmax(abs(original_matrix.to_numpy() - v26.to_numpy()))
    )
    if max_matrix_error > 1e-10:
        raise RuntimeError(f"Original comparison rebuild mismatch: {max_matrix_error}")

    rng = np.random.default_rng(SEED)
    pair_rows = []
    p_values = []
    for left, right in itertools.combinations(MODULES, 2):
        complete = unique_matrix[[left, right]].notna().all(axis=1)
        original_left = original_matrix.loc[complete, left].to_numpy(dtype=float)
        original_right = original_matrix.loc[complete, right].to_numpy(dtype=float)
        unique_left = unique_matrix.loc[complete, left].to_numpy(dtype=float)
        unique_right = unique_matrix.loc[complete, right].to_numpy(dtype=float)
        original_rho = safe_spearman(original_left, original_right)
        unique_rho = safe_spearman(unique_left, unique_right)
        null = np.empty(N_PERMUTATIONS, dtype=float)
        for index in range(N_PERMUTATIONS):
            null[index] = abs(safe_spearman(unique_left, rng.permutation(unique_right)))
        p_value = (1 + int(np.sum(null >= abs(unique_rho)))) / (N_PERMUTATIONS + 1)
        p_values.append(p_value)
        bootstrap_delta = np.empty(N_BOOTSTRAP, dtype=float)
        for index in range(N_BOOTSTRAP):
            sample = rng.integers(0, len(unique_left), size=len(unique_left))
            bootstrap_delta[index] = safe_spearman(
                unique_left[sample], unique_right[sample]
            ) - safe_spearman(original_left[sample], original_right[sample])
        pair_rows.append(
            {
                "module_a": left,
                "module_b": right,
                "n_contexts": len(unique_left),
                "original_spearman": original_rho,
                "globally_unique_gene_spearman": unique_rho,
                "rho_delta_unique_minus_original": unique_rho - original_rho,
                "paired_bootstrap_delta_ci_low": float(np.nanquantile(bootstrap_delta, 0.025)),
                "paired_bootstrap_delta_ci_high": float(np.nanquantile(bootstrap_delta, 0.975)),
                "unique_empirical_permutation_p": p_value,
            }
        )
    for row, q_value in zip(pair_rows, bh_adjust(p_values), strict=True):
        row["unique_q_bh_six_pairs"] = q_value
        row["survives_deoverlap_gate"] = (
            abs(float(row["globally_unique_gene_spearman"])) >= 0.5
            and q_value <= 0.10
            and int(row["n_contexts"]) == len(source.CONFIGS)
        )

    target = next(
        row
        for row in pair_rows
        if {row["module_a"], row["module_b"]}
        == {"hla_ii_apc", "mif_cd74_receptor_state"}
    )
    target_persists = bool(target["survives_deoverlap_gate"])
    summary = {
        "purpose": "V53 cell-state dependency sensitivity using globally disjoint module genes",
        "n_contexts": len(source.CONFIGS),
        "n_source_h5ad_files": len(cache),
        "max_absolute_donor_mean_rebuild_error": max_mean_error,
        "max_absolute_donor_high_fraction_rebuild_error": max_fraction_error,
        "max_absolute_v26_matrix_rebuild_error": max_matrix_error,
        "unique_gene_counts": {module: len(genes) for module, genes in unique_modules.items()},
        "hla_mif_original_spearman": target["original_spearman"],
        "hla_mif_unique_spearman": target["globally_unique_gene_spearman"],
        "hla_mif_unique_q_bh": target["unique_q_bh_six_pairs"],
        "hla_mif_survives_deoverlap_gate": target_persists,
        "global_coupled_axis_status_changed": False,
        "verdict": (
            "CELL_STATE_HLA_MIF_EDGE_PERSISTS_WITH_DISJOINT_READOUTS_GLOBAL_STATUS_UNCHANGED"
            if target_persists
            else "CELL_STATE_HLA_MIF_EDGE_FAILS_DISJOINT_READOUT_GATE_GLOBAL_STATUS_REQUIRES_REASSESSMENT"
        ),
        "boundary": "This recomputes the 12 direct-h5ad cell-state contexts only. Treatment-response and cross-disease-summary layers require separate provenance-preserving rebuilds.",
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
    unique.to_csv(OUT / "globally_unique_gene_donor_module_scores.tsv", sep="\t", index=False)
    unique_matrix.to_csv(OUT / "globally_unique_gene_cell_state_matrix.tsv", sep="\t")
    coverage.to_csv(OUT / "globally_unique_gene_coverage.tsv", sep="\t", index=False)
    write_tsv(OUT / "run_log.tsv", run_rows)
    write_tsv(OUT / "module_gene_partition.tsv", gene_rows)
    write_tsv(OUT / "dependency_sensitivity.tsv", pair_rows)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 Cell-State De-overlap Sensitivity",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"Five held h5ad files were read once to rebuild all `{len(source.CONFIGS)}` donor-level",
        "contexts under original and globally disjoint module definitions. Original donor",
        f"scores and the V26 matrix reproduce to maximum errors `{max_mean_error:.3g}` and",
        f"`{max_matrix_error:.3g}`.",
        "",
        f"HLA-II/APC versus receptor-state rho changes from",
        f"`{float(target['original_spearman']):.3f}` to",
        f"`{float(target['globally_unique_gene_spearman']):.3f}` with six-pair BH",
        f"`q={float(target['unique_q_bh_six_pairs']):.4f}`. This sensitivity alone does not",
        "change the global architecture; remaining modalities require separate rebuilds.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
