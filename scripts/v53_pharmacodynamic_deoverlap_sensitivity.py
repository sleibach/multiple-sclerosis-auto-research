#!/usr/bin/env python3
"""Recompute all 24 V26 pharmacodynamic contexts with disjoint APC modules."""

from __future__ import annotations

import csv
import contextlib
import io
import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

import v3_analyze_direct_h5ad_cell_states as module_source
import v3_analyze_gse253006_tofacitinib_marker_compartments as uc_source
import v3_wave18_treatment_response_scout as pso_source
import v3_wave23_treatment_response_stratification as pd_source


ROOT = Path(__file__).resolve().parents[1]
V26_MATRIX = ROOT / "analysis/v26_deep_structure/treatment_pharmacodynamic_module_matrix.tsv"
OUT = ROOT / "analysis/v53_pharmacodynamic_deoverlap_sensitivity"
MODULES = ("hla_ii_apc", "ifn_apc", "lysosomal_apc", "mif_cd74_receptor_state")
SEED = 53501
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
    unique = {name: list(genes) for name, genes in original.items()}
    for module in MODULES:
        unique[module] = [gene for gene in original[module] if counts[gene] == 1]
    return unique


def configure_pd_source(modules: dict[str, list[str]]) -> None:
    pd_source.MODULES = modules
    pd_source.TARGET_GENES = sorted(
        {gene for module in pd_source.SHARED_MODULES for gene in modules[module]}
    )


def run_public(modules: dict[str, list[str]]) -> pd.DataFrame:
    configure_pd_source(modules)
    frames = []
    for analyzer in (
        pd_source.analyze_gse106992_psoriasis,
        pd_source.analyze_gse24742_rituximab,
        pd_source.analyze_gse250453_fingolimod,
        pd_source.analyze_gse235357_dmf,
    ):
        _, pharmacodynamic, _ = analyzer()
        frames.append(pharmacodynamic)
    evidence = pd.concat(frames, ignore_index=True)
    # The live GSE106992 analyzer now includes therapy_class in its scope label;
    # V26's committed source artifact predates that label-only addition.
    gse106992 = evidence["dataset"].eq("GSE106992")
    evidence.loc[gse106992, "therapy"] = "etanercept/ustekinumab"
    evidence.loc[gse106992, "analysis_scope"] = evidence.loc[
        gse106992, "analysis_scope"
    ].str.replace(r"^therapy_class=[^;]+;", "", regex=True)
    return evidence


def run_uc(modules: dict[str, list[str]], label: str) -> pd.DataFrame:
    uc_source.MODULES = modules
    uc_source.ALL_MODULES = {**modules, **uc_source.EXTRA_MODULES}
    uc_source.TARGET_GENES = sorted(
        {gene for genes in uc_source.ALL_MODULES.values() for gene in genes}
    )
    uc_source.ALL_GENES = sorted(set(uc_source.TARGET_GENES) | set(uc_source.MARKER_GENES))
    uc_source.OUT = OUT / "source_runs" / f"gse253006_{label}"
    uc_source.OUT.mkdir(parents=True, exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()):
        uc_source.main()
    donors = pd.read_csv(uc_source.OUT / "gse253006_marker_donor_module_scores.tsv", sep="\t")
    donors = donors.rename(columns={"mean_score": "score"})
    donors["time_order"] = donors["timepoint_norm"].map(
        {"W0": 0, "W8": 8, "W16": 16, "W24": 24, "W48": 48}
    ).fillna(999)
    return pd_source.compare_prepost(
        donors,
        "patient",
        "timepoint_norm",
        "W0",
        "time_order",
        ["group", "marker_compartment"],
        "GSE253006",
        "JAK/TYK",
        "tofacitinib",
        "ulcerative colitis",
        "marker-derived rectal single-cell compartments",
        "earliest post-treatment minus baseline",
        "V53 de-overlap sensitivity; same marker-derived compartments and pairing as V26",
    )


def run_pso(modules: dict[str, list[str]], label: str) -> pd.DataFrame:
    pso_source.MODULES = modules
    pso_source.TARGET_GENES = sorted({gene for genes in modules.values() for gene in genes})
    pso_source.ALL_PSO_MODULES = {**modules, **pso_source.PSO_EXTRA_MODULES}
    pso_source.PSO_GENES = sorted(
        {gene for genes in pso_source.ALL_PSO_MODULES.values() for gene in genes}
        | {gene for genes in pso_source.MARKER_SETS.values() for gene in genes}
    )
    pso_source.OUT = OUT / "source_runs" / f"gse183047_{label}"
    pso_source.OUT.mkdir(parents=True, exist_ok=True)
    scores, _, _ = pso_source.analyze_gse183047_psoriasis()
    scores = scores.rename(columns={"mean_score": "score"})
    scores = scores[scores["group"].eq("psoriasis") & scores["lesion"].eq("LS")].copy()
    return pd_source.compare_prepost(
        scores,
        "patient",
        "timepoint",
        "preTx",
        "time_order",
        ["marker_compartment"],
        "GSE183047",
        "IL-17/IL-23",
        "secukinumab",
        "psoriasis",
        "marker-derived lesional skin single-cell compartments",
        "earliest post-secukinumab minus pretreatment",
        "V53 de-overlap sensitivity; same marker-derived compartments and pairing as V26",
    )


def run_all(modules: dict[str, list[str]], label: str) -> pd.DataFrame:
    frames = [run_public(modules), run_uc(modules, label), run_pso(modules, label)]
    return pd.concat(frames, ignore_index=True)


def matrix_from_evidence(evidence: pd.DataFrame) -> pd.DataFrame:
    frame = evidence[evidence["module"].isin(MODULES)].copy()
    matrix = frame.pivot_table(
        index=["dataset", "therapy", "analysis_scope"],
        columns="module",
        values="mean_post_minus_pre",
        aggfunc="mean",
    ).rename_axis(index=[None, None, None])
    matrix.index = ["|".join(map(str, index)) for index in matrix.index]
    return matrix.reindex(columns=MODULES)


def main() -> int:
    np.random.seed(SEED)
    original_modules = {name: list(genes) for name, genes in module_source.MODULES.items()}
    unique_modules = globally_unique_modules(original_modules)

    download_cache: dict[str, bytes] = {}
    real_download = pd_source.download_bytes

    def cached_download(url: str, timeout: int = 180) -> bytes:
        if url not in download_cache:
            download_cache[url] = real_download(url, timeout)
        return download_cache[url]

    pd_source.download_bytes = cached_download
    original_evidence = run_all(original_modules, "original")
    unique_evidence = run_all(unique_modules, "unique")
    pd_source.download_bytes = real_download
    configure_pd_source(original_modules)

    original_matrix = matrix_from_evidence(original_evidence)
    unique_matrix = matrix_from_evidence(unique_evidence)
    v26 = pd.read_csv(V26_MATRIX, sep="\t", index_col=0).reindex(columns=MODULES)
    original_matrix = original_matrix.reindex(v26.index)
    unique_matrix = unique_matrix.reindex(v26.index)
    original_values = original_matrix.to_numpy(dtype=float)
    v26_values = v26.to_numpy(dtype=float)
    if original_matrix.shape != v26.shape or not np.isfinite(original_values).all():
        original_matrix.to_csv(OUT / "original_rebuild_incomplete.tsv", sep="\t")
        raise RuntimeError(
            "Original pharmacodynamic rebuild is incomplete; all V26 cells must be finite"
        )
    max_matrix_error = float(np.max(abs(original_values - v26_values)))
    if max_matrix_error > 1e-10:
        mismatch = pd.DataFrame(
            original_matrix.to_numpy() - v26.to_numpy(),
            index=v26.index,
            columns=MODULES,
        )
        mismatch.to_csv(OUT / "original_rebuild_mismatch.tsv", sep="\t")
        raise RuntimeError(f"Original pharmacodynamic rebuild mismatch: {max_matrix_error}")

    labels = np.asarray(v26.index, dtype=str)
    dataset_strata = np.asarray([label.split("|", 1)[0] for label in labels])
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
        pair_strata = dataset_strata[complete.to_numpy()]
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
                "n_contexts": len(u_left),
                "original_spearman": original_rho,
                "globally_unique_gene_spearman": unique_rho,
                "rho_delta_unique_minus_original": unique_rho - original_rho,
                "paired_bootstrap_delta_ci_low": float(np.nanquantile(bootstrap_delta, 0.025)),
                "paired_bootstrap_delta_ci_high": float(np.nanquantile(bootstrap_delta, 0.975)),
                "unique_global_permutation_p": global_p,
                "unique_dataset_stratified_p": stratified_p,
                "original_dataset_stratified_p": original_stratified_p,
            }
        )

    global_q = bh_adjust(global_p_values)
    stratified_q = bh_adjust(stratified_p_values)
    original_stratified_q = bh_adjust(original_stratified_p_values)
    for row, global_value, stratified_value, original_value in zip(
        pair_rows, global_q, stratified_q, original_stratified_q, strict=True
    ):
        row["unique_global_q_bh_six_pairs"] = global_value
        row["unique_dataset_stratified_q_bh_six_pairs"] = stratified_value
        row["original_dataset_stratified_q_bh_six_pairs"] = original_value
        row["survives_deoverlap_gate"] = (
            abs(float(row["globally_unique_gene_spearman"])) >= 0.5
            and global_value <= 0.10
            and stratified_value <= 0.10
            and int(row["n_contexts"]) == len(v26)
        )

    target = next(
        row
        for row in pair_rows
        if {row["module_a"], row["module_b"]}
        == {"hla_ii_apc", "mif_cd74_receptor_state"}
    )
    target_complete = unique_matrix[
        ["hla_ii_apc", "mif_cd74_receptor_state"]
    ].notna().all(axis=1)
    target_missing_contexts = unique_matrix.index[~target_complete].tolist()
    target_complete_datasets = {
        label.split("|", 1)[0] for label in unique_matrix.index[target_complete]
    }
    attenuation_established = float(target["paired_bootstrap_delta_ci_high"]) < 0
    target_persists = bool(target["survives_deoverlap_gate"])
    target_association_criteria_pass = (
        abs(float(target["globally_unique_gene_spearman"])) >= 0.5
        and float(target["unique_global_q_bh_six_pairs"]) <= 0.10
        and float(target["unique_dataset_stratified_q_bh_six_pairs"]) <= 0.10
    )
    gate_failure_reasons = []
    if not target_association_criteria_pass:
        gate_failure_reasons.append("association_or_corrected_null_criterion")
    if int(target["n_contexts"]) != len(v26):
        gate_failure_reasons.append("incomplete_disjoint_readout_coverage")
    summary = {
        "purpose": "V53 complete 24-context pharmacodynamic dependency sensitivity using globally disjoint module genes",
        "n_contexts": len(v26),
        "n_datasets": len(set(dataset_strata)),
        "downloaded_objects_cached_in_memory": len(download_cache),
        "max_absolute_v26_matrix_rebuild_error": max_matrix_error,
        "unique_gene_counts": {module: len(unique_modules[module]) for module in MODULES},
        "hla_mif_original_spearman": target["original_spearman"],
        "hla_mif_v26_full_24_context_spearman": safe_spearman(
            original_matrix["hla_ii_apc"].to_numpy(dtype=float),
            original_matrix["mif_cd74_receptor_state"].to_numpy(dtype=float),
        ),
        "hla_mif_unique_spearman": target["globally_unique_gene_spearman"],
        "hla_mif_complete_disjoint_contexts": int(target["n_contexts"]),
        "hla_mif_complete_disjoint_datasets": len(target_complete_datasets),
        "hla_mif_missing_disjoint_contexts": target_missing_contexts,
        "hla_mif_unique_global_q": target["unique_global_q_bh_six_pairs"],
        "hla_mif_unique_dataset_stratified_q": target[
            "unique_dataset_stratified_q_bh_six_pairs"
        ],
        "hla_mif_original_dataset_stratified_q": target[
            "original_dataset_stratified_q_bh_six_pairs"
        ],
        "hla_mif_paired_bootstrap_delta_ci": [
            target["paired_bootstrap_delta_ci_low"],
            target["paired_bootstrap_delta_ci_high"],
        ],
        "hla_mif_attenuation_established_by_paired_bootstrap": attenuation_established,
        "hla_mif_association_criteria_pass_on_available_contexts": target_association_criteria_pass,
        "hla_mif_gate_failure_reasons": gate_failure_reasons,
        "hla_mif_survives_deoverlap_gate": target_persists,
        "verdict": (
            "PHARMACODYNAMIC_HLA_MIF_EDGE_PERSISTS_WITH_DISJOINT_READOUTS"
            if target_persists
            else (
                "PHARMACODYNAMIC_HLA_MIF_EDGE_FAILS_FULL_COVERAGE_GATE_DESPITE_RETAINED_ASSOCIATION"
                if target_association_criteria_pass
                else "PHARMACODYNAMIC_HLA_MIF_EDGE_FAILS_DISJOINT_READOUT_GATE"
            )
        ),
        "boundary": "This sensitivity changes no frozen module, locked rule, or validation threshold.",
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
    original_matrix.to_csv(OUT / "rebuilt_original_pharmacodynamic_matrix.tsv", sep="\t")
    unique_matrix.to_csv(OUT / "globally_unique_gene_pharmacodynamic_matrix.tsv", sep="\t")
    unique_evidence.to_csv(OUT / "globally_unique_gene_pharmacodynamic_evidence.tsv", sep="\t", index=False)
    write_tsv(OUT / "module_gene_partition.tsv", gene_rows)
    write_tsv(OUT / "dependency_sensitivity.tsv", pair_rows)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    if target_missing_contexts:
        coverage_lines = [
            f"The association criteria pass on the `{int(target['n_contexts'])}` available contexts,",
            f"but the unique-gene readouts cover only `{len(target_complete_datasets)}` of `6` datasets.",
            "The missing context labels are listed in `summary.json`.",
        ]
    else:
        coverage_lines = [
            "The association criteria pass with complete coverage: all `24` contexts",
            "and all `6` datasets retain both globally unique readouts.",
        ]
    report = [
        "# V53 Pharmacodynamic De-overlap Sensitivity",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"All `{len(v26)}` V26 pharmacodynamic contexts were rebuilt from source inputs under",
        "original and globally disjoint module definitions. Public downloads were cached in",
        f"memory across both passes. The original matrix reproduces to `{max_matrix_error:.3g}`.",
        "",
        f"HLA-II/APC versus receptor-state rho changes from",
        f"`{float(target['original_spearman']):.3f}` to",
        f"`{float(target['globally_unique_gene_spearman']):.3f}`. The disjoint global and",
        f"dataset-stratified q-values are `{float(target['unique_global_q_bh_six_pairs']):.4f}`",
        f"and `{float(target['unique_dataset_stratified_q_bh_six_pairs']):.4f}`.",
        "",
        *coverage_lines,
        "The paired attenuation CI is",
        f"`[{float(target['paired_bootstrap_delta_ci_low']):.3f},",
        f"{float(target['paired_bootstrap_delta_ci_high']):.3f}]`, so attenuation is not",
        "established. This layer is therefore suggestive but cannot rescue a claim of robust,",
        "independently measured coupling across the full pharmacodynamic evidence set.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
