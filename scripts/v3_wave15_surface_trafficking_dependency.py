#!/usr/bin/env python3
"""Wave15-A surface/trafficking dependency screen for CD74/CIITA/HLA-II state.

This worker asks a narrow question: among druggable or quasi-druggable surface,
endosomal, lysosomal, uptake, trafficking, protease, chaperone, and glycosylation
genes, which ones repeatedly track the recurring CD74/CIITA/HLA-II state in
local autoimmune single-cell/spatial datasets?

Guardrails:
- donor/sample is the statistical unit;
- analyses are compartment-restricted where curated cell types exist;
- disease-control deltas and state-couplings are separate evidence channels;
- state coupling is tested both raw and after residualizing generic myeloid,
  NF-kB, lipid-loader, and IFN covariates;
- genes that only track myeloid/phagocytic abundance are demoted.
"""

from __future__ import annotations

import gzip
import json
import math
import os
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import anndata as ad
import numpy as np
import pandas as pd
from scipy import io, sparse, stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_gse111972_microglia import load_expression as load_ms_expression
from v3_analyze_gse111972_microglia import load_sample_metadata as load_ms_metadata
from v3_analyze_osmr_complement_axes import CONFIGS as DIRECT_CONFIGS
from v3_analyze_osmr_complement_axes import ROOT

SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave15_surface_trafficking_dependency"
REPORT = ROOT / "phases/v3/subagents" / "wave15_surface_trafficking_dependency.md"


MINIMUM_CANDIDATES = [
    "CTSS",
    "CTSB",
    "CTSL",
    "CTSD",
    "IFI30",
    "HLA-DMA",
    "HLA-DMB",
    "LAMP1",
    "LAMP2",
    "LIPA",
    "NPC2",
    "SORT1",
    "M6PR",
    "AP2M1",
    "RAB5A",
    "RAB7A",
    "RAB11A",
    "VAMP3",
    "VAMP7",
    "SNX10",
    "SNX5",
    "FCGR2A",
    "FCGR3A",
    "C1QA",
    "C1QB",
    "C1QC",
    "TYROBP",
    "TREM2",
    "LGALS3",
    "LGALS9",
    "MRC1",
    "MSR1",
    "SCARB1",
]

EXTRA_CANDIDATES = [
    # Antigen-loading / lysosomal / vesicle neighbors.
    "HLA-DOA",
    "HLA-DOB",
    "LAMP3",
    "CD63",
    "LAPTM5",
    "TPP1",
    "NPC1",
    "CTSH",
    "CTSZ",
    "CTSK",
    "GNPTAB",
    "GNPTG",
    "IGF2R",
    "AP2A1",
    "CLTC",
    "RAB7B",
    "RAB9A",
    "RAB32",
    "RAB27A",
    "VAMP8",
    "SNX2",
    "SNX3",
    "SNX6",
    # Uptake/phagocytosis and lipid cargo receptors.
    "LRP1",
    "CD36",
    "MERTK",
    "AXL",
    "CLEC7A",
    "FCER1G",
    "ITGAX",
    "ITGAM",
    "CD68",
    "LYZ",
    "LST1",
    "CST3",
    "APOE",
    "GPNMB",
    "SPP1",
    # Positive state controls, kept out of go/no-go promotion.
    "CD74",
    "CIITA",
    "RFX5",
    "HLA-DRA",
    "HLA-DRB1",
    "HLA-DPA1",
    "HLA-DPB1",
]

CANDIDATE_GENES = sorted(set(MINIMUM_CANDIDATES) | set(EXTRA_CANDIDATES))
STATE_CONTROL_GENES = {"CD74", "CIITA", "RFX5", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1"}

GENE_FAMILIES = {
    **{g: "cathepsin_protease" for g in ["CTSS", "CTSB", "CTSL", "CTSD", "CTSH", "CTSZ", "CTSK"]},
    "IFI30": "lysosomal_thiol_reductase",
    **{g: "hla_chaperone_loading" for g in ["HLA-DMA", "HLA-DMB", "HLA-DOA", "HLA-DOB"]},
    **{g: "lysosome_membrane_or_lipid" for g in ["LAMP1", "LAMP2", "LAMP3", "LIPA", "NPC2", "NPC1", "TPP1", "CD63", "LAPTM5"]},
    **{g: "glycosylation_mannose6p" for g in ["GNPTAB", "GNPTG", "M6PR", "IGF2R"]},
    **{g: "vesicle_sorting_trafficking" for g in ["SORT1", "AP2M1", "AP2A1", "CLTC", "RAB5A", "RAB7A", "RAB7B", "RAB9A", "RAB11A", "RAB27A", "RAB32", "VAMP3", "VAMP7", "VAMP8", "SNX10", "SNX5", "SNX2", "SNX3", "SNX6"]},
    **{g: "surface_uptake_fc_complement" for g in ["FCGR2A", "FCGR3A", "FCER1G", "C1QA", "C1QB", "C1QC"]},
    **{g: "surface_phagocytic_lipid_receptor" for g in ["TYROBP", "TREM2", "MRC1", "MSR1", "SCARB1", "LRP1", "CD36", "MERTK", "AXL", "CLEC7A", "ITGAX", "ITGAM", "CD68"]},
    **{g: "galectin_glycan_checkpoint" for g in ["LGALS3", "LGALS9"]},
    **{g: "myeloid_marker_control" for g in ["LYZ", "LST1", "CST3", "APOE", "GPNMB", "SPP1"]},
    **{g: "state_positive_control" for g in STATE_CONTROL_GENES},
}

DRUGGABILITY_SCORE = {
    "cathepsin_protease": 3.0,
    "lysosomal_thiol_reductase": 2.0,
    "hla_chaperone_loading": 1.0,
    "lysosome_membrane_or_lipid": 2.0,
    "glycosylation_mannose6p": 1.25,
    "vesicle_sorting_trafficking": 1.25,
    "surface_uptake_fc_complement": 2.0,
    "surface_phagocytic_lipid_receptor": 2.25,
    "galectin_glycan_checkpoint": 2.0,
    "myeloid_marker_control": 0.5,
    "state_positive_control": 0.0,
}

STATE_MODULES = {
    "hla_cd74_ciita_state": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "CIITA", "RFX5"],
    "cd74_hla_surface_state": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1"],
    "ifn_apc_upstream": ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "IFI44L"],
    "myeloid_abundance": ["LST1", "LYZ", "AIF1", "CSF1R", "MS4A7", "FCGR1A", "FCER1G", "CD14"],
    "generic_nfkb": ["IL1B", "TNF", "CXCL8", "CCL2", "CCL3", "CCL4", "NFKBIA", "TREM1"],
    "lipid_loader_phagocytic": ["APOE", "GPNMB", "LPL", "SPP1", "CD36", "MERTK", "AXL", "MSR1", "TREM2"],
}

PRIMARY_STATE_MODULES = ["hla_cd74_ciita_state", "cd74_hla_surface_state"]
CONFOUNDERS_NON_IFN = ["myeloid_abundance", "generic_nfkb", "lipid_loader_phagocytic"]
CONFOUNDERS_WITH_IFN = ["ifn_apc_upstream", *CONFOUNDERS_NON_IFN]
ALL_GENES = sorted(set(CANDIDATE_GENES) | {g for genes in STATE_MODULES.values() for g in genes})


@dataclass(frozen=True)
class SampleConfig:
    sample_id: str
    prefix: str
    donor_id: str
    disease: str
    group: str


CELIAC_RAW = ROOT / "data" / "raw_v3" / "gse315138" / "raw"
CELIAC_SAMPLES = [
    SampleConfig("GSM9421934", "GSM9421934_2-PC004-h", "Healthy1", "normal", "control"),
    SampleConfig("GSM9421935", "GSM9421935_1-PC005-h", "Healthy2", "normal", "control"),
    SampleConfig("GSM9421936", "GSM9421936_3-PC006-c", "celiac1", "celiac disease", "case"),
    SampleConfig("GSM9421937", "GSM9421937_SI-TT-G4", "celiac2", "celiac disease", "case"),
    SampleConfig("GSM9421938", "GSE315138_Celiac-a2", "celiac_a2", "celiac disease", "case"),
    SampleConfig("GSM9421939", "GSE315138_Celiac304", "celiac304", "celiac disease", "case"),
]

CELIAC_MARKER_SETS = {
    "epithelial_like": ["EPCAM", "KRT8", "KRT18", "KRT19", "VIL1", "APOA4", "ALPI", "FABP1", "MUC2"],
    "t_cell_like": ["CD3D", "CD3E", "CD3G", "TRAC", "CD4", "CD8A", "CD8B", "NKG7", "GZMA", "GZMB"],
    "myeloid_apc_like": ["LST1", "LYZ", "CD14", "FCGR3A", "ITGAX", "CST3", "HLA-DRA", "CD74", "FCER1A", "MS4A7"],
    "b_plasma_like": ["MS4A1", "CD79A", "CD79B", "CD74", "MZB1", "JCHAIN", "IGHG1", "IGHG4"],
    "stromal_endothelial_like": ["COL1A1", "COL1A2", "DCN", "LUM", "PECAM1", "VWF", "CLDN5", "ACTA2", "RGS5"],
}

THYROID_PROCESSED = ROOT / "data" / "raw_v3" / "gse248205" / "processed"
THYROID_SAMPLE_DISEASE = {
    "C1": "control",
    "C2": "control",
    "HT1": "Hashimoto thyroiditis",
    "HT2": "Hashimoto thyroiditis",
    "HT3": "Hashimoto thyroiditis",
    "GD1": "Graves disease",
    "GD2": "Graves disease",
    "GD3": "Graves disease",
}


def safe_float(value) -> float:
    try:
        out = float(value)
    except Exception:
        return float("nan")
    return out if math.isfinite(out) else float("nan")


def hedges_g(case: np.ndarray, control: np.ndarray) -> float:
    case = np.asarray(case, dtype=float)
    control = np.asarray(control, dtype=float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if case.size < 2 or control.size < 2:
        return np.nan
    pooled = ((case.size - 1) * case.var(ddof=1) + (control.size - 1) * control.var(ddof=1)) / (
        case.size + control.size - 2
    )
    if pooled <= 0:
        return np.nan
    correction = 1.0 - (3.0 / (4.0 * (case.size + control.size) - 9.0))
    return float(((case.mean() - control.mean()) / math.sqrt(pooled)) * correction)


def compare(case: Iterable[float], control: Iterable[float]) -> dict[str, float | int]:
    case_arr = np.asarray(list(case), dtype=float)
    control_arr = np.asarray(list(control), dtype=float)
    case_arr = case_arr[np.isfinite(case_arr)]
    control_arr = control_arr[np.isfinite(control_arr)]
    if case_arr.size >= 2 and control_arr.size >= 2:
        t_stat, p_value = stats.ttest_ind(case_arr, control_arr, equal_var=False, nan_policy="omit")
    else:
        t_stat, p_value = np.nan, np.nan
    return {
        "n_case_units": int(case_arr.size),
        "n_control_units": int(control_arr.size),
        "mean_case": float(np.nanmean(case_arr)) if case_arr.size else np.nan,
        "mean_control": float(np.nanmean(control_arr)) if control_arr.size else np.nan,
        "delta_case_minus_control": float(np.nanmean(case_arr) - np.nanmean(control_arr)) if case_arr.size and control_arr.size else np.nan,
        "hedges_g": hedges_g(case_arr, control_arr),
        "welch_t": float(t_stat) if pd.notna(t_stat) else np.nan,
        "p": float(p_value) if pd.notna(p_value) else np.nan,
    }


def support_level(delta: float, p_value: float, fdr: float) -> str:
    if not np.isfinite(delta):
        return "missing"
    if delta < 0 and np.isfinite(p_value) and p_value <= 0.10:
        return "negative_trend"
    if delta <= 0:
        return "null_or_negative"
    if np.isfinite(fdr) and fdr <= 0.10:
        return "fdr10_positive"
    if np.isfinite(p_value) and p_value <= 0.10:
        return "trend_positive"
    return "positive_null"


def add_fdr_by_group(df: pd.DataFrame, p_col: str, group_cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    if p_col == "p":
        fdr_col = "fdr"
    elif p_col.endswith("_p"):
        fdr_col = f"{p_col[:-2]}_fdr"
    else:
        fdr_col = f"{p_col}_fdr"
    out[fdr_col] = np.nan
    if out.empty:
        return out
    for _, idx in out.groupby(group_cols, dropna=False).groups.items():
        pvals = pd.to_numeric(out.loc[idx, p_col], errors="coerce").to_numpy(float)
        valid = np.isfinite(pvals)
        adjusted = np.full(pvals.shape, np.nan)
        if valid.any():
            adjusted[valid] = multipletests(pvals[valid], method="fdr_bh")[1]
        out.loc[idx, fdr_col] = adjusted
    return out


def gene_symbol_indices(a: ad.AnnData, symbol_column: str) -> dict[str, int]:
    if symbol_column in a.var.columns:
        symbols = a.var[symbol_column].astype(str)
    elif "feature_name" in a.var.columns:
        symbols = a.var["feature_name"].astype(str)
    else:
        symbols = pd.Series(a.var_names.astype(str), index=a.var.index)
    mapping: dict[str, int] = {}
    wanted = {g.upper() for g in ALL_GENES}
    for idx, raw in enumerate(symbols):
        symbol = str(raw).strip()
        key = symbol.upper()
        if key in wanted and key not in mapping:
            mapping[key] = idx
    return {gene: mapping[gene.upper()] for gene in ALL_GENES if gene.upper() in mapping}


def zscore_against_controls(log_expr: np.ndarray, control_mask: np.ndarray) -> np.ndarray:
    if control_mask.sum() < 2:
        mean = np.nanmean(log_expr, axis=0)
        sd = np.nanstd(log_expr, axis=0, ddof=1)
    else:
        mean = np.nanmean(log_expr[control_mask], axis=0)
        sd = np.nanstd(log_expr[control_mask], axis=0, ddof=1)
    sd[~np.isfinite(sd) | (sd < 1e-6)] = 1.0
    return (log_expr - mean) / sd


def module_scores_from_z(z: np.ndarray, genes: list[str], gene_to_col: dict[str, int]) -> dict[str, np.ndarray]:
    scores: dict[str, np.ndarray] = {}
    for module, module_genes in STATE_MODULES.items():
        present = [g for g in module_genes if g in gene_to_col]
        if present:
            scores[module] = np.nanmean(z[:, [gene_to_col[g] for g in present]], axis=1)
        else:
            scores[module] = np.full(z.shape[0], np.nan)
    return scores


def aggregate_scores(
    *,
    analysis: str,
    dataset_path: str,
    disease_name: str,
    compartment: str,
    role: str,
    obs: pd.DataFrame,
    log_expr: np.ndarray,
    z: np.ndarray,
    genes: list[str],
    min_units: int,
    unit_col: str = "donor_id",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    gene_to_col = {g: i for i, g in enumerate(genes)}
    modules = module_scores_from_z(z, genes, gene_to_col)
    rows_gene: list[dict[str, object]] = []
    rows_module: list[dict[str, object]] = []
    for (unit, disease, group), idx_values in obs.groupby([unit_col, "disease", "group"], observed=True).groups.items():
        idx = np.fromiter(idx_values, dtype=int)
        if idx.size < min_units:
            continue
        base = {
            "analysis": analysis,
            "dataset_path": dataset_path,
            "disease_name": disease_name,
            "compartment": compartment,
            "role": role,
            "unit_id": str(unit),
            "disease": str(disease),
            "group": str(group),
            "n_observations": int(idx.size),
        }
        for gene in genes:
            if gene not in CANDIDATE_GENES:
                continue
            vals = log_expr[idx, gene_to_col[gene]]
            zvals = z[idx, gene_to_col[gene]]
            rows_gene.append(
                {
                    **base,
                    "gene": gene,
                    "family": GENE_FAMILIES.get(gene, "other"),
                    "is_minimum_candidate": gene in MINIMUM_CANDIDATES,
                    "is_state_control": gene in STATE_CONTROL_GENES,
                    "mean_log_norm": float(np.nanmean(vals)),
                    "mean_z_vs_controls": float(np.nanmean(zvals)),
                    "detection_fraction": float((vals > 0).mean()),
                }
            )
        for module, vals in modules.items():
            rows_module.append(
                {
                    **base,
                    "module": module,
                    "mean_score": float(np.nanmean(vals[idx])),
                }
            )
    return pd.DataFrame(rows_gene), pd.DataFrame(rows_module)


def analyze_direct_h5ad() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list[dict[str, object]]]:
    gene_tables = []
    module_tables = []
    presence_tables = []
    run_log: list[dict[str, object]] = []
    cache: dict[Path, tuple[ad.AnnData, sparse.csr_matrix]] = {}
    for config in DIRECT_CONFIGS:
        try:
            if config.path not in cache:
                a = ad.read_h5ad(config.path)
                x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
                cache[config.path] = (a, x)
            a, x = cache[config.path]
            obs = a.obs.copy()
            mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
            obs_sub = obs.loc[mask].reset_index(drop=True).copy()
            cell_idx = np.flatnonzero(mask.to_numpy())
            gene_idx = gene_symbol_indices(a, config.gene_symbol_column)
            presence_tables.append(
                pd.DataFrame(
                    [
                        {
                            "analysis": config.name,
                            "dataset_path": str(config.path.relative_to(ROOT)),
                            "disease_name": config.disease_label,
                            "compartment": config.compartment,
                            "role": config.role,
                            "gene": gene,
                            "present": gene in gene_idx,
                            "family": GENE_FAMILIES.get(gene, "other"),
                        }
                        for gene in CANDIDATE_GENES
                    ]
                )
            )
            present = [g for g in ALL_GENES if g in gene_idx]
            if obs_sub.empty or not present:
                raise ValueError("no selected cells or genes")
            target_x = x[cell_idx][:, [gene_idx[g] for g in present]].astype(float)
            lib_size = np.asarray(x[cell_idx].sum(axis=1)).ravel().astype(float)
            lib_size[~np.isfinite(lib_size) | (lib_size <= 0)] = np.nan
            normalizer = np.divide(1.0, lib_size, out=np.zeros_like(lib_size), where=np.isfinite(lib_size))
            log_expr = np.log1p(target_x.multiply(normalizer[:, None]).multiply(1e4).toarray())
            control_mask = obs_sub["disease"].eq(config.control_label).to_numpy()
            z = zscore_against_controls(log_expr, control_mask)
            obs_sub["group"] = np.where(obs_sub["disease"].eq(config.disease_label), "case", "control")
            genes, mods = aggregate_scores(
                analysis=config.name,
                dataset_path=str(config.path.relative_to(ROOT)),
                disease_name=config.disease_label,
                compartment=config.compartment,
                role=config.role,
                obs=obs_sub[["donor_id", "disease", "group"]].copy(),
                log_expr=log_expr,
                z=z,
                genes=present,
                min_units=10,
            )
            gene_tables.append(genes)
            module_tables.append(mods)
            run_log.append(
                {
                    "analysis": config.name,
                    "modality": "single_cell_h5ad",
                    "status": "completed",
                    "n_cells": int(len(obs_sub)),
                    "n_units": int(obs_sub["donor_id"].nunique()),
                    "n_candidate_genes_present": int(sum(g in gene_idx for g in CANDIDATE_GENES)),
                }
            )
        except Exception as exc:
            run_log.append(
                {
                    "analysis": getattr(config, "name", "unknown"),
                    "modality": "single_cell_h5ad",
                    "status": "failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    return (
        pd.concat(gene_tables, ignore_index=True) if gene_tables else pd.DataFrame(),
        pd.concat(module_tables, ignore_index=True) if module_tables else pd.DataFrame(),
        pd.concat(presence_tables, ignore_index=True) if presence_tables else pd.DataFrame(),
        run_log,
    )


def analyze_ms_microglia() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list[dict[str, object]]]:
    run_log: list[dict[str, object]] = []
    try:
        meta = load_ms_metadata()
        expr = load_ms_expression()
        meta = meta.loc[meta["sample"].isin(expr.columns)].reset_index(drop=True)
        genes = [g for g in ALL_GENES if g in expr.index]
        presence = pd.DataFrame(
            [
                {
                    "analysis": "gse111972_ms_microglia",
                    "dataset_path": "data/raw_v3/gse111972/GSE111972_norm_data.txt.gz",
                    "disease_name": "MS",
                    "compartment": "sorted microglia",
                    "role": "myeloid_apc",
                    "gene": gene,
                    "present": gene in expr.index,
                    "family": GENE_FAMILIES.get(gene, "other"),
                }
                for gene in CANDIDATE_GENES
            ]
        )
        gene_rows = []
        module_rows = []
        for region, compartment in [("white_matter", "white matter microglia"), ("grey_matter", "grey matter microglia")]:
            sub_meta = meta.loc[meta["region"].eq(region)].reset_index(drop=True).copy()
            if sub_meta.empty:
                continue
            sub_meta["group"] = np.where(sub_meta["disease"].eq("MS"), "case", "control")
            log_expr = expr.loc[genes, sub_meta["sample"]].T.to_numpy(dtype=float)
            z = zscore_against_controls(log_expr, sub_meta["group"].eq("control").to_numpy())
            obs = pd.DataFrame(
                {
                    "donor_id": sub_meta["sample"].astype(str),
                    "disease": sub_meta["disease"].astype(str),
                    "group": sub_meta["group"].astype(str),
                }
            )
            g, m = aggregate_scores(
                analysis=f"gse111972_ms_{region}_microglia",
                dataset_path="data/raw_v3/gse111972/GSE111972_norm_data.txt.gz",
                disease_name="MS",
                compartment=compartment,
                role="myeloid_apc",
                obs=obs,
                log_expr=log_expr,
                z=z,
                genes=genes,
                min_units=1,
            )
            gene_rows.append(g)
            module_rows.append(m)
        run_log.append(
            {
                "analysis": "gse111972_ms_microglia",
                "modality": "sorted_bulk_microglia",
                "status": "completed",
                "n_samples": int(len(meta)),
                "n_candidate_genes_present": int(sum(g in expr.index for g in CANDIDATE_GENES)),
            }
        )
        return (
            pd.concat(gene_rows, ignore_index=True) if gene_rows else pd.DataFrame(),
            pd.concat(module_rows, ignore_index=True) if module_rows else pd.DataFrame(),
            presence,
            run_log,
        )
    except Exception as exc:
        run_log.append(
            {
                "analysis": "gse111972_ms_microglia",
                "modality": "sorted_bulk_microglia",
                "status": "failed",
                "error": f"{type(exc).__name__}: {exc}",
            }
        )
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), run_log


def read_feature_table(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", header=None, compression="gzip")
    if df.shape[1] < 2:
        raise ValueError(f"feature table has fewer than 2 columns: {path}")
    out = df.iloc[:, :2].copy()
    out.columns = ["gene_id", "gene_symbol"]
    out["row_index"] = np.arange(out.shape[0])
    return out


def classify_celiac(obs: pd.DataFrame, log_expr: np.ndarray, genes: list[str]) -> pd.DataFrame:
    gene_to_col = {g: i for i, g in enumerate(genes)}
    score_df = pd.DataFrame(index=obs.index)
    for compartment, marker_genes in CELIAC_MARKER_SETS.items():
        present = [g for g in marker_genes if g in gene_to_col]
        score_df[compartment] = np.nanmean(log_expr[:, [gene_to_col[g] for g in present]], axis=1) if present else np.nan
    values = score_df.to_numpy(float)
    order = np.argsort(np.nan_to_num(values, nan=-np.inf), axis=1)
    top_idx = order[:, -1]
    second_idx = order[:, -2]
    top_score = values[np.arange(values.shape[0]), top_idx]
    second_score = values[np.arange(values.shape[0]), second_idx]
    labels = np.array(score_df.columns)[top_idx].astype(object)
    ambiguous = (~np.isfinite(top_score)) | (top_score < 0.20) | ((top_score - second_score) < 0.05)
    labels[ambiguous] = "ambiguous"
    out = obs.copy()
    out["marker_compartment"] = labels
    return out


def load_celiac_sample(config: SampleConfig) -> tuple[pd.DataFrame, np.ndarray, list[str]]:
    features = read_feature_table(CELIAC_RAW / f"{config.prefix}_features.tsv.gz")
    row_map: dict[int, str] = {}
    wanted = set(ALL_GENES) | {g for genes in CELIAC_MARKER_SETS.values() for g in genes}
    for gene in wanted:
        hits = features.loc[features["gene_symbol"].astype(str).eq(gene), "row_index"]
        if not hits.empty:
            row_map[int(hits.iloc[0])] = gene
    selected_rows = sorted(row_map)
    genes = [row_map[i] for i in selected_rows]
    mat = io.mmread(CELIAC_RAW / f"{config.prefix}_matrix.mtx.gz").tocsc().astype(float)
    with gzip.open(CELIAC_RAW / f"{config.prefix}_barcodes.tsv.gz", "rt") as handle:
        barcodes = [line.strip() for line in handle if line.strip()]
    if mat.shape[1] != len(barcodes):
        raise ValueError(f"barcode mismatch in {config.sample_id}")
    lib = np.asarray(mat.sum(axis=0)).ravel().astype(float)
    lib[~np.isfinite(lib) | (lib <= 0)] = np.nan
    selected = mat[selected_rows, :].T.tocsr()
    norm = selected.multiply(np.divide(1.0, lib, out=np.zeros_like(lib), where=np.isfinite(lib))[:, None]).multiply(1e4)
    log_expr = np.log1p(norm.toarray())
    obs = pd.DataFrame(
        {
            "donor_id": config.donor_id,
            "disease": config.disease,
            "group": config.group,
            "barcode": barcodes,
        }
    )
    return obs, log_expr, genes


def analyze_celiac_marker() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list[dict[str, object]]]:
    run_log: list[dict[str, object]] = []
    try:
        obs_tables = []
        expr_tables = []
        gene_sets = []
        for config in CELIAC_SAMPLES:
            obs, expr, genes = load_celiac_sample(config)
            obs = classify_celiac(obs, expr, genes)
            obs_tables.append(obs)
            expr_tables.append(pd.DataFrame(expr, columns=genes))
            gene_sets.append(set(genes))
            run_log.append(
                {
                    "analysis": f"gse315138_{config.donor_id}",
                    "modality": "single_cell_10x_marker_compartment",
                    "status": "completed",
                    "n_cells": int(len(obs)),
                    "n_genes_selected": int(len(genes)),
                }
            )
        common_genes = sorted(set.intersection(*gene_sets))
        obs_all = pd.concat(obs_tables, ignore_index=True)
        expr_all = pd.concat([df.reindex(columns=common_genes) for df in expr_tables], ignore_index=True).to_numpy(float)
        gene_tables = []
        module_tables = []
        for compartment, comp_obs in obs_all.groupby("marker_compartment", observed=True):
            if compartment == "ambiguous":
                continue
            idx = comp_obs.index.to_numpy()
            if len(idx) < 100:
                continue
            comp_expr = expr_all[idx, :]
            z = zscore_against_controls(comp_expr, comp_obs["group"].eq("control").to_numpy())
            obs = comp_obs[["donor_id", "disease", "group"]].reset_index(drop=True)
            g, m = aggregate_scores(
                analysis=f"gse315138_celiac_{compartment}",
                dataset_path="data/raw_v3/gse315138/raw/*_matrix.mtx.gz",
                disease_name="celiac disease",
                compartment=f"duodenum {compartment}",
                role="marker_compartment",
                obs=obs,
                log_expr=comp_expr,
                z=z,
                genes=common_genes,
                min_units=50,
            )
            gene_tables.append(g)
            module_tables.append(m)
        presence = pd.DataFrame(
            [
                {
                    "analysis": "gse315138_celiac_marker",
                    "dataset_path": "data/raw_v3/gse315138/raw/*_matrix.mtx.gz",
                    "disease_name": "celiac disease",
                    "compartment": "all marker compartments",
                    "role": "marker_compartment",
                    "gene": gene,
                    "present": gene in common_genes,
                    "family": GENE_FAMILIES.get(gene, "other"),
                }
                for gene in CANDIDATE_GENES
            ]
        )
        return (
            pd.concat(gene_tables, ignore_index=True) if gene_tables else pd.DataFrame(),
            pd.concat(module_tables, ignore_index=True) if module_tables else pd.DataFrame(),
            presence,
            run_log,
        )
    except Exception as exc:
        run_log.append(
            {
                "analysis": "gse315138_celiac_marker",
                "modality": "single_cell_10x_marker_compartment",
                "status": "failed",
                "error": f"{type(exc).__name__}: {exc}",
            }
        )
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), run_log


def load_thyroid_sample(sample: str) -> tuple[dict[str, object], np.ndarray, list[str]]:
    sample_dir = THYROID_PROCESSED / sample
    features = read_feature_table(sample_dir / f"{sample}_features.tsv.gz")
    row_map: dict[int, str] = {}
    for gene in ALL_GENES:
        hits = features.loc[features["gene_symbol"].astype(str).eq(gene), "row_index"]
        if not hits.empty:
            row_map[int(hits.iloc[0])] = gene
    selected_rows = sorted(row_map)
    genes = [row_map[i] for i in selected_rows]
    mat = io.mmread(sample_dir / f"{sample}_matrix.mtx.gz").tocsr().astype(float)
    if mat.shape[0] != len(features) and mat.shape[1] == len(features):
        mat = mat.T.tocsr()
    lib = np.asarray(mat.sum(axis=0)).ravel().astype(float)
    lib[~np.isfinite(lib) | (lib <= 0)] = np.nan
    selected = mat[selected_rows, :].tocsc()
    norm = selected.multiply(np.divide(1.0, lib, out=np.zeros_like(lib), where=np.isfinite(lib))).multiply(1e4)
    log_expr = np.log1p(norm.toarray()).T
    row = {
        "donor_id": sample,
        "disease": THYROID_SAMPLE_DISEASE[sample],
        "group": "control" if THYROID_SAMPLE_DISEASE[sample] == "control" else "case",
        "n_spots": int(mat.shape[1]),
    }
    return row, log_expr, genes


def analyze_thyroid_spatial() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list[dict[str, object]]]:
    run_log: list[dict[str, object]] = []
    try:
        obs_tables = []
        expr_tables = []
        gene_sets = []
        for sample in THYROID_SAMPLE_DISEASE:
            row, expr, genes = load_thyroid_sample(sample)
            obs_tables.append(
                pd.DataFrame(
                    {
                        "donor_id": row["donor_id"],
                        "disease": row["disease"],
                        "group": row["group"],
                        "spot_index": np.arange(expr.shape[0]),
                    }
                )
            )
            expr_tables.append(pd.DataFrame(expr, columns=genes))
            gene_sets.append(set(genes))
        common_genes = sorted(set.intersection(*gene_sets))
        obs_all = pd.concat(obs_tables, ignore_index=True)
        expr_all = pd.concat([df.reindex(columns=common_genes) for df in expr_tables], ignore_index=True).to_numpy(float)
        out_gene = []
        out_mod = []
        for disease in ["Hashimoto thyroiditis", "Graves disease"]:
            mask = obs_all["disease"].isin(["control", disease]).to_numpy()
            obs = obs_all.loc[mask, ["donor_id", "disease", "group"]].reset_index(drop=True).copy()
            expr = expr_all[mask, :]
            z = zscore_against_controls(expr, obs["group"].eq("control").to_numpy())
            g, m = aggregate_scores(
                analysis=f"gse248205_thyroid_{disease.replace(' ', '_').lower()}",
                dataset_path="data/raw_v3/gse248205/processed/*/*_matrix.mtx.gz",
                disease_name=disease,
                compartment="thyroid Visium spots",
                role="spatial_tissue",
                obs=obs,
                log_expr=expr,
                z=z,
                genes=common_genes,
                min_units=50,
            )
            out_gene.append(g)
            out_mod.append(m)
        presence = pd.DataFrame(
            [
                {
                    "analysis": "gse248205_thyroid_spatial",
                    "dataset_path": "data/raw_v3/gse248205/processed/*/*_matrix.mtx.gz",
                    "disease_name": "Hashimoto thyroiditis;Graves disease",
                    "compartment": "thyroid Visium spots",
                    "role": "spatial_tissue",
                    "gene": gene,
                    "present": gene in common_genes,
                    "family": GENE_FAMILIES.get(gene, "other"),
                }
                for gene in CANDIDATE_GENES
            ]
        )
        run_log.append(
            {
                "analysis": "gse248205_thyroid_spatial",
                "modality": "spatial_visium_sample_level",
                "status": "completed",
                "n_samples": int(obs_all["donor_id"].nunique()),
                "n_spots": int(len(obs_all)),
                "n_candidate_genes_present": int(sum(g in common_genes for g in CANDIDATE_GENES)),
            }
        )
        return (
            pd.concat(out_gene, ignore_index=True) if out_gene else pd.DataFrame(),
            pd.concat(out_mod, ignore_index=True) if out_mod else pd.DataFrame(),
            presence,
            run_log,
        )
    except Exception as exc:
        run_log.append(
            {
                "analysis": "gse248205_thyroid_spatial",
                "modality": "spatial_visium_sample_level",
                "status": "failed",
                "error": f"{type(exc).__name__}: {exc}",
            }
        )
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), run_log


def compare_gene_deltas(gene_scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if gene_scores.empty:
        return pd.DataFrame()
    for (analysis, gene), sub in gene_scores.groupby(["analysis", "gene"], observed=True):
        first = sub.iloc[0]
        for metric in ["mean_z_vs_controls", "detection_fraction"]:
            stats_row = compare(
                sub.loc[sub["group"].eq("case"), metric],
                sub.loc[sub["group"].eq("control"), metric],
            )
            rows.append(
                {
                    "analysis": analysis,
                    "dataset_path": first["dataset_path"],
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "gene": gene,
                    "family": first["family"],
                    "is_minimum_candidate": bool(first["is_minimum_candidate"]),
                    "is_state_control": bool(first["is_state_control"]),
                    "metric": metric,
                    **stats_row,
                }
            )
    out = pd.DataFrame(rows)
    out = add_fdr_by_group(out, "p", ["analysis", "metric"]) if not out.empty else out
    if not out.empty:
        out["support_level"] = [
            support_level(safe_float(r["delta_case_minus_control"]), safe_float(r["p"]), safe_float(r["fdr"]))
            for _, r in out.iterrows()
        ]
    return out


def residualize_vector(y: np.ndarray, covariates: pd.DataFrame) -> np.ndarray:
    y = np.asarray(y, dtype=float)
    cov = covariates.apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    valid = np.isfinite(y)
    if cov.size:
        valid &= np.isfinite(cov).all(axis=1)
    resid = np.full(y.shape, np.nan)
    if valid.sum() < max(4, cov.shape[1] + 3):
        return resid
    if cov.shape[1] == 0:
        resid[valid] = y[valid] - np.nanmean(y[valid])
        return resid
    design = np.column_stack([np.ones(valid.sum()), cov[valid]])
    try:
        beta, *_ = np.linalg.lstsq(design, y[valid], rcond=None)
        resid[valid] = y[valid] - design @ beta
    except np.linalg.LinAlgError:
        return np.full(y.shape, np.nan)
    return resid


def spearman_pair(x: pd.Series | np.ndarray, y: pd.Series | np.ndarray) -> tuple[int, float, float]:
    xv = pd.to_numeric(pd.Series(x), errors="coerce")
    yv = pd.to_numeric(pd.Series(y), errors="coerce")
    ok = pd.DataFrame({"x": xv, "y": yv}).replace([np.inf, -np.inf], np.nan).dropna()
    if len(ok) < 5 or ok["x"].nunique() < 3 or ok["y"].nunique() < 3:
        return int(len(ok)), np.nan, np.nan
    res = stats.spearmanr(ok["x"], ok["y"])
    return int(len(ok)), float(res.statistic), float(res.pvalue)


def module_wide(module_scores: pd.DataFrame) -> pd.DataFrame:
    if module_scores.empty:
        return pd.DataFrame()
    idx_cols = ["analysis", "dataset_path", "disease_name", "compartment", "role", "unit_id", "disease", "group", "n_observations"]
    wide = (
        module_scores.pivot_table(index=idx_cols, columns="module", values="mean_score", aggfunc="first")
        .reset_index()
        .rename_axis(None, axis=1)
    )
    return wide


def state_couplings(gene_scores: pd.DataFrame, module_scores: pd.DataFrame) -> pd.DataFrame:
    wide = module_wide(module_scores)
    if gene_scores.empty or wide.empty:
        return pd.DataFrame()
    merged = gene_scores.merge(
        wide,
        on=["analysis", "dataset_path", "disease_name", "compartment", "role", "unit_id", "disease", "group", "n_observations"],
        how="inner",
    )
    rows = []
    for (analysis, gene), sub in merged.groupby(["analysis", "gene"], observed=True):
        first = sub.iloc[0]
        for target in PRIMARY_STATE_MODULES + ["myeloid_abundance", "lipid_loader_phagocytic", "generic_nfkb", "ifn_apc_upstream"]:
            if target not in sub.columns:
                continue
            n, rho, p = spearman_pair(sub["mean_z_vs_controls"], sub[target])
            rows.append(
                {
                    "analysis": analysis,
                    "dataset_path": first["dataset_path"],
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "gene": gene,
                    "family": first["family"],
                    "is_minimum_candidate": bool(first["is_minimum_candidate"]),
                    "is_state_control": bool(first["is_state_control"]),
                    "target_module": target,
                    "model": "raw",
                    "n_units": n,
                    "spearman_r": rho,
                    "spearman_p": p,
                }
            )
        for target, covariates, model_name in [
            ("hla_cd74_ciita_state", CONFOUNDERS_NON_IFN, "residual_non_ifn_confounders"),
            ("cd74_hla_surface_state", CONFOUNDERS_NON_IFN, "residual_non_ifn_confounders"),
            ("hla_cd74_ciita_state", CONFOUNDERS_WITH_IFN, "residual_with_ifn_confounders"),
            ("cd74_hla_surface_state", CONFOUNDERS_WITH_IFN, "residual_with_ifn_confounders"),
        ]:
            cols = [c for c in covariates if c in sub.columns]
            if target not in sub.columns or not cols:
                continue
            gene_resid = residualize_vector(sub["mean_z_vs_controls"].to_numpy(float), sub[cols])
            state_resid = residualize_vector(sub[target].to_numpy(float), sub[cols])
            n, rho, p = spearman_pair(gene_resid, state_resid)
            rows.append(
                {
                    "analysis": analysis,
                    "dataset_path": first["dataset_path"],
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "gene": gene,
                    "family": first["family"],
                    "is_minimum_candidate": bool(first["is_minimum_candidate"]),
                    "is_state_control": bool(first["is_state_control"]),
                    "target_module": target,
                    "model": model_name,
                    "covariates": ",".join(cols),
                    "n_units": n,
                    "spearman_r": rho,
                    "spearman_p": p,
                }
            )
    out = pd.DataFrame(rows)
    out = add_fdr_by_group(out, "spearman_p", ["target_module", "model"]) if not out.empty else out
    return out


def summarize_gene_deltas(delta_tests: pd.DataFrame) -> pd.DataFrame:
    if delta_tests.empty:
        return pd.DataFrame()
    primary = delta_tests[delta_tests["metric"].eq("mean_z_vs_controls")].copy()
    support_rank = {
        "fdr10_positive": 3,
        "trend_positive": 2,
        "positive_null": 1,
        "null_or_negative": 0,
        "negative_trend": -1,
        "missing": -2,
    }
    primary["support_rank"] = primary["support_level"].map(support_rank).fillna(0)
    best = (
        primary.sort_values(["support_rank", "hedges_g"], ascending=[False, False])
        .groupby(["gene", "disease_name"], as_index=False)
        .first()
    )
    rows = []
    for gene, sub in best.groupby("gene", observed=True):
        fdr10 = sub[sub["support_level"].eq("fdr10_positive")]
        trend = sub[sub["support_level"].isin(["fdr10_positive", "trend_positive"])]
        negative = sub[sub["support_level"].eq("negative_trend")]
        rows.append(
            {
                "gene": gene,
                "n_delta_diseases_tested": int(sub["disease_name"].nunique()),
                "n_delta_fdr10_positive_diseases": int(len(fdr10)),
                "n_delta_trend_or_better_diseases": int(len(trend)),
                "n_delta_negative_trend_diseases": int(len(negative)),
                "median_delta_hedges_g_supported": float(trend["hedges_g"].median()) if not trend.empty else np.nan,
                "delta_supporting_diseases": ";".join(sorted(trend["disease_name"].astype(str).unique())),
                "delta_negative_diseases": ";".join(sorted(negative["disease_name"].astype(str).unique())),
                "best_delta_details": json.dumps(
                    sub[
                        [
                            "disease_name",
                            "analysis",
                            "compartment",
                            "delta_case_minus_control",
                            "hedges_g",
                            "p",
                            "fdr",
                            "support_level",
                        ]
                    ].to_dict(orient="records")
                ),
            }
        )
    return pd.DataFrame(rows)


def summarize_couplings(couplings: pd.DataFrame) -> pd.DataFrame:
    if couplings.empty:
        return pd.DataFrame()
    rows = []
    primary_raw = couplings[
        couplings["target_module"].isin(PRIMARY_STATE_MODULES) & couplings["model"].eq("raw")
    ].copy()
    primary_non_ifn = couplings[
        couplings["target_module"].isin(PRIMARY_STATE_MODULES)
        & couplings["model"].eq("residual_non_ifn_confounders")
    ].copy()
    primary_with_ifn = couplings[
        couplings["target_module"].isin(PRIMARY_STATE_MODULES)
        & couplings["model"].eq("residual_with_ifn_confounders")
    ].copy()
    confounder_raw = couplings[
        couplings["target_module"].isin(["myeloid_abundance", "lipid_loader_phagocytic", "generic_nfkb"])
        & couplings["model"].eq("raw")
    ].copy()
    for gene in sorted(couplings["gene"].unique()):
        raw_gene = primary_raw[primary_raw["gene"].eq(gene)]
        non_ifn_gene = primary_non_ifn[primary_non_ifn["gene"].eq(gene)]
        with_ifn_gene = primary_with_ifn[primary_with_ifn["gene"].eq(gene)]
        conf_gene = confounder_raw[confounder_raw["gene"].eq(gene)]

        def disease_count(df: pd.DataFrame, threshold: float) -> int:
            if df.empty:
                return 0
            best = df.sort_values("spearman_r", ascending=False).groupby("disease_name", as_index=False).first()
            return int((best["spearman_r"] >= threshold).sum())

        raw_best = raw_gene.sort_values("spearman_r", ascending=False).groupby("disease_name", as_index=False).first() if not raw_gene.empty else pd.DataFrame()
        non_ifn_best = non_ifn_gene.sort_values("spearman_r", ascending=False).groupby("disease_name", as_index=False).first() if not non_ifn_gene.empty else pd.DataFrame()
        conf_best = conf_gene.sort_values("spearman_r", ascending=False).groupby("disease_name", as_index=False).first() if not conf_gene.empty else pd.DataFrame()
        conf_dominant = 0
        if not raw_best.empty and not conf_best.empty:
            merged = raw_best[["disease_name", "spearman_r"]].rename(columns={"spearman_r": "state_r"}).merge(
                conf_best[["disease_name", "spearman_r", "target_module"]].rename(columns={"spearman_r": "confounder_r"}),
                on="disease_name",
                how="inner",
            )
            conf_dominant = int((merged["confounder_r"] > (merged["state_r"] + 0.10)).sum())
        rows.append(
            {
                "gene": gene,
                "n_state_raw_r_ge_0_5_diseases": disease_count(raw_gene, 0.50),
                "n_state_raw_r_ge_0_7_diseases": disease_count(raw_gene, 0.70),
                "n_state_resid_non_ifn_r_ge_0_35_diseases": disease_count(non_ifn_gene, 0.35),
                "n_state_resid_with_ifn_r_ge_0_25_diseases": disease_count(with_ifn_gene, 0.25),
                "median_raw_state_r": float(raw_gene["spearman_r"].median()) if not raw_gene.empty else np.nan,
                "median_resid_non_ifn_state_r": float(non_ifn_gene["spearman_r"].median()) if not non_ifn_gene.empty else np.nan,
                "median_resid_with_ifn_state_r": float(with_ifn_gene["spearman_r"].median()) if not with_ifn_gene.empty else np.nan,
                "n_confounder_raw_r_ge_0_5_diseases": disease_count(conf_gene, 0.50),
                "n_confounder_dominant_diseases": conf_dominant,
                "raw_state_supporting_diseases": ";".join(sorted(raw_best.loc[raw_best["spearman_r"] >= 0.50, "disease_name"].astype(str).unique())) if not raw_best.empty else "",
                "resid_non_ifn_supporting_diseases": ";".join(sorted(non_ifn_best.loc[non_ifn_best["spearman_r"] >= 0.35, "disease_name"].astype(str).unique())) if not non_ifn_best.empty else "",
                "best_raw_state_details": json.dumps(
                    raw_best[
                        ["disease_name", "analysis", "compartment", "target_module", "n_units", "spearman_r", "spearman_p", "spearman_fdr"]
                    ].to_dict(orient="records")
                    if not raw_best.empty
                    else []
                ),
                "best_resid_non_ifn_details": json.dumps(
                    non_ifn_best[
                        ["disease_name", "analysis", "compartment", "target_module", "n_units", "spearman_r", "spearman_p", "spearman_fdr"]
                    ].to_dict(orient="records")
                    if not non_ifn_best.empty
                    else []
                ),
            }
        )
    return pd.DataFrame(rows)


def rank_candidates(delta_summary: pd.DataFrame, coupling_summary: pd.DataFrame, presence: pd.DataFrame) -> pd.DataFrame:
    base = pd.DataFrame({"gene": CANDIDATE_GENES})
    base["family"] = base["gene"].map(lambda g: GENE_FAMILIES.get(g, "other"))
    base["is_minimum_candidate"] = base["gene"].isin(MINIMUM_CANDIDATES)
    base["is_state_control"] = base["gene"].isin(STATE_CONTROL_GENES)
    base["druggability_score"] = base["family"].map(DRUGGABILITY_SCORE).fillna(1.0)
    if not delta_summary.empty:
        base = base.merge(delta_summary, on="gene", how="left")
    if not coupling_summary.empty:
        base = base.merge(coupling_summary, on="gene", how="left")
    if not presence.empty:
        pres = (
            presence.groupby("gene", observed=True)
            .agg(
                n_analyses_present=("present", lambda s: int(s.sum())),
                n_analyses_checked=("present", "size"),
            )
            .reset_index()
        )
        base = base.merge(pres, on="gene", how="left")
    fill_zero = [
        "n_delta_diseases_tested",
        "n_delta_fdr10_positive_diseases",
        "n_delta_trend_or_better_diseases",
        "n_delta_negative_trend_diseases",
        "n_state_raw_r_ge_0_5_diseases",
        "n_state_raw_r_ge_0_7_diseases",
        "n_state_resid_non_ifn_r_ge_0_35_diseases",
        "n_state_resid_with_ifn_r_ge_0_25_diseases",
        "n_confounder_raw_r_ge_0_5_diseases",
        "n_confounder_dominant_diseases",
        "n_analyses_present",
        "n_analyses_checked",
    ]
    for col in fill_zero:
        if col in base.columns:
            base[col] = base[col].fillna(0).astype(int)
    base["delta_score"] = (
        2.0 * base.get("n_delta_fdr10_positive_diseases", 0)
        + 1.0 * base.get("n_delta_trend_or_better_diseases", 0)
        - 1.0 * base.get("n_delta_negative_trend_diseases", 0)
    )
    base["state_coupling_score"] = (
        1.0 * base.get("n_state_raw_r_ge_0_5_diseases", 0)
        + 1.5 * base.get("n_state_resid_non_ifn_r_ge_0_35_diseases", 0)
        + 0.5 * base.get("n_state_resid_with_ifn_r_ge_0_25_diseases", 0)
        - 0.75 * base.get("n_confounder_dominant_diseases", 0)
    )
    base["breadth_penalty"] = np.where(base.get("n_delta_diseases_tested", 0) < 5, 2.0, 0.0)
    base["state_control_penalty"] = np.where(base["is_state_control"], 20.0, 0.0)
    base["rank_score"] = (
        base["delta_score"]
        + base["state_coupling_score"]
        + 0.75 * base["druggability_score"]
        - base["breadth_penalty"]
        - base["state_control_penalty"]
    )
    recommendations = []
    demotions = []
    for _, row in base.iterrows():
        reasons = []
        rec = "NO_GO"
        if row["is_state_control"]:
            reasons.append("state-definition positive control, not dependency nomination")
        if row.get("n_delta_negative_trend_diseases", 0) >= max(2, row.get("n_delta_trend_or_better_diseases", 0)):
            reasons.append("directionally inconsistent disease-control deltas")
        if row.get("n_state_resid_non_ifn_r_ge_0_35_diseases", 0) == 0 and row.get("n_state_raw_r_ge_0_5_diseases", 0) > 0:
            reasons.append("raw state coupling collapses after non-IFN confounder residualization")
        if row.get("n_confounder_dominant_diseases", 0) >= max(2, row.get("n_state_resid_non_ifn_r_ge_0_35_diseases", 0)):
            reasons.append("confounder/myeloid coupling dominates state coupling")
        elif row.get("n_confounder_dominant_diseases", 0) >= 4 and row.get("n_confounder_dominant_diseases", 0) >= (
            row.get("n_state_resid_non_ifn_r_ge_0_35_diseases", 0) - 1
        ):
            reasons.append("near-confounder-dominant; not cleanly independent of myeloid/phagocytic state")
        if row.get("n_delta_diseases_tested", 0) < 5:
            reasons.append("insufficient cross-disease local breadth")
        if row["druggability_score"] < 1.5 and not row["is_state_control"]:
            reasons.append("strong local state biology but weak direct druggability/tractable modulation")
        if not reasons:
            if (
                row.get("n_delta_trend_or_better_diseases", 0) >= 3
                and row.get("n_state_resid_non_ifn_r_ge_0_35_diseases", 0) >= 3
                and row["druggability_score"] >= 2.0
                and row.get("n_delta_negative_trend_diseases", 0) <= 1
            ):
                rec = "GO_SCOUT"
            elif (
                row.get("n_state_raw_r_ge_0_5_diseases", 0) >= 4
                and row.get("n_state_resid_non_ifn_r_ge_0_35_diseases", 0) >= 2
                and row["druggability_score"] >= 1.5
            ):
                rec = "WATCHLIST"
                reasons.append("watchlist: residual state support present but GO gate not met")
            else:
                rec = "NO_GO"
                reasons.append("does not meet recurrence plus residual-coupling gate")
        recommendations.append(rec)
        demotions.append("; ".join(reasons) if reasons else "passes local dependency gate")
    base["go_no_go"] = recommendations
    base["demotion_or_support_reason"] = demotions
    return base.sort_values(["go_no_go", "rank_score"], ascending=[True, False])


def write_markdown_report(rank: pd.DataFrame, delta_tests: pd.DataFrame, couplings: pd.DataFrame, run_log: list[dict[str, object]], summary: dict[str, object]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    top = rank[~rank["is_state_control"]].sort_values("rank_score", ascending=False).head(15)
    gos = rank[rank["go_no_go"].eq("GO_SCOUT") & ~rank["is_state_control"]].sort_values("rank_score", ascending=False)
    watch = rank[rank["go_no_go"].eq("WATCHLIST") & ~rank["is_state_control"]].sort_values("rank_score", ascending=False)
    mandatory = rank[rank["is_minimum_candidate"] & ~rank["is_state_control"]].sort_values("rank_score", ascending=False)

    def fmt(x, digits=3):
        val = safe_float(x)
        return "NA" if not np.isfinite(val) else f"{val:.{digits}f}"

    lines = [
        "# Wave15-A Surface/Trafficking Dependency Screen",
        "",
        "## Scope",
        "",
        "I tested candidate surface, endosomal trafficking, protease, chaperone, glycosylation, lysosomal, and uptake genes against the recurring `CD74`/`CIITA`/HLA-II state using only local V3 datasets. The statistical unit is donor/sample, not cells. Direct h5ad analyses are compartment-restricted; celiac uses marker-derived compartments; thyroid Visium and MS sorted microglia are sample-level tissue validations.",
        "",
        "## Inputs",
        "",
    ]
    for row in run_log:
        status = row.get("status")
        analysis = row.get("analysis")
        modality = row.get("modality", "")
        extra = ", ".join(f"{k}={v}" for k, v in row.items() if k not in {"analysis", "status", "modality"} and not str(k).startswith("error"))
        err = f"; error={row.get('error')}" if row.get("error") else ""
        lines.append(f"- `{analysis}` ({modality}): {status}" + (f"; {extra}" if extra else "") + err)
    lines += [
        "",
        "## Methods",
        "",
        "- For each analysis I library-size normalized selected genes, log-transformed them, z-scored genes against matched controls, and averaged to donor/sample-level gene scores.",
        "- Disease-control evidence uses Welch tests and Hedges g on donor/sample gene z-scores and detection fractions, with BH FDR within each analysis/metric.",
        "- State-coupling evidence uses donor/sample Spearman correlations between each candidate and two state modules: `hla_cd74_ciita_state` and `cd74_hla_surface_state`.",
        "- Residual state coupling regresses both candidate and state module against `myeloid_abundance`, `generic_nfkb`, and `lipid_loader_phagocytic`; a stricter secondary model also includes `ifn_apc_upstream`.",
        "- Pivot criterion applied: candidates with raw state coupling but no residual coupling, or stronger myeloid/confounder coupling than state coupling, are demoted as abundance/state markers.",
        "",
        "## Ranked Candidates",
        "",
        "| rank | gene | family | local call | rank score | delta trend+ diseases | residual state diseases | raw state diseases | confounder-dominant diseases | reason |",
        "|---:|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for i, (_, r) in enumerate(top.iterrows(), start=1):
        lines.append(
            "| {rank} | `{gene}` | {family} | {call} | {score} | {delta} | {resid} | {raw} | {conf} | {reason} |".format(
                rank=i,
                gene=r["gene"],
                family=r["family"],
                call=r["go_no_go"],
                score=fmt(r["rank_score"], 2),
                delta=int(r.get("n_delta_trend_or_better_diseases", 0)),
                resid=int(r.get("n_state_resid_non_ifn_r_ge_0_35_diseases", 0)),
                raw=int(r.get("n_state_raw_r_ge_0_5_diseases", 0)),
                conf=int(r.get("n_confounder_dominant_diseases", 0)),
                reason=str(r["demotion_or_support_reason"]).replace("|", "/"),
            )
        )
    lines += [
        "",
        "## Go/No-Go",
        "",
    ]
    if gos.empty:
        lines.append("No non-state candidate met the strict `GO_SCOUT` gate of at least three disease-control trend-or-better diseases, at least three residual state-coupling diseases, druggability score >=2, and <=1 negative-trend disease.")
    else:
        lines.append("Local `GO_SCOUT` candidates:")
        for _, r in gos.iterrows():
            lines.append(
                f"- `{r['gene']}`: {r['family']}; delta support {int(r['n_delta_trend_or_better_diseases'])} diseases; residual state support {int(r['n_state_resid_non_ifn_r_ge_0_35_diseases'])} diseases; rank score {fmt(r['rank_score'], 2)}."
            )
    if not watch.empty:
        lines.append("")
        lines.append("Watchlist candidates that did not meet the strict local gate:")
        for _, r in watch.head(10).iterrows():
            lines.append(
                f"- `{r['gene']}`: {r['family']}; raw state support {int(r['n_state_raw_r_ge_0_5_diseases'])}, residual support {int(r['n_state_resid_non_ifn_r_ge_0_35_diseases'])}; reason: {r['demotion_or_support_reason']}."
            )
    evidence_focus = pd.concat(
        [
            gos,
            watch.head(5),
            top[top["family"].eq("hla_chaperone_loading")].head(4),
        ],
        ignore_index=True,
    ).drop_duplicates("gene")
    lines += [
        "",
        "## Per-Disease Evidence For Survivors And Biological Anchors",
        "",
        "| gene | role in this screen | disease-control support | residual state-coupling support | raw state-coupling support | negative disease-control trends |",
        "|---|---|---|---|---|---|",
    ]
    for _, r in evidence_focus.iterrows():
        role = r["go_no_go"] if r["go_no_go"] != "NO_GO" else r["demotion_or_support_reason"]
        lines.append(
            "| `{gene}` | {role} | {delta} | {resid} | {raw} | {neg} |".format(
                gene=r["gene"],
                role=str(role).replace("|", "/"),
                delta=str(r.get("delta_supporting_diseases", "")).replace(";", "; "),
                resid=str(r.get("resid_non_ifn_supporting_diseases", "")).replace(";", "; "),
                raw=str(r.get("raw_state_supporting_diseases", "")).replace(";", "; "),
                neg=str(r.get("delta_negative_diseases", "")).replace(";", "; "),
            )
        )
    lines += [
        "",
        "## Mandatory Candidate Family Check",
        "",
        "| gene | family | local call | delta trend+ | residual state | raw state | negative deltas | reason |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ]
    for _, r in mandatory.iterrows():
        lines.append(
            f"| `{r['gene']}` | {r['family']} | {r['go_no_go']} | {int(r.get('n_delta_trend_or_better_diseases', 0))} | {int(r.get('n_state_resid_non_ifn_r_ge_0_35_diseases', 0))} | {int(r.get('n_state_raw_r_ge_0_5_diseases', 0))} | {int(r.get('n_delta_negative_trend_diseases', 0))} | {str(r['demotion_or_support_reason']).replace('|', '/')} |"
        )
    lines += [
        "",
        "## Confounder Critique",
        "",
        "- C1q/TYROBP/TREM2/APOE/GPNMB-like genes are biologically close to the original lipid-lysosomal myeloid module, but this screen treats them skeptically: if their strongest association is with `myeloid_abundance` or `lipid_loader_phagocytic` instead of residual HLA/CD74 state, they are demoted.",
        "- Thyroid Visium has only two controls and three cases per autoimmune thyroid subgroup; it is useful spatial recurrence evidence but not robust enough alone.",
        "- Celiac compartments are marker-derived because no curated cell labels were present in the GEO supplement; celiac results are recurrence evidence, not definitive cell-type-specific inference.",
        "- MS GSE111972 is sorted microglia from white/grey matter, not lesion-rim spatial data; it is an independent MS myeloid validation/contradiction only.",
        "- Residualizing against `ifn_apc_upstream` is intentionally harsh and can remove the biology of an IFN-induced antigen-presentation dependency. The primary demotion gate therefore uses the non-IFN residual model, with the IFN residual model reported separately.",
        "",
        "## Output Files",
        "",
        "- `phases/v3/results/wave15_surface_trafficking_dependency/candidate_donor_scores.tsv`",
        "- `phases/v3/results/wave15_surface_trafficking_dependency/state_module_scores.tsv`",
        "- `phases/v3/results/wave15_surface_trafficking_dependency/candidate_disease_delta_tests.tsv`",
        "- `phases/v3/results/wave15_surface_trafficking_dependency/candidate_state_couplings.tsv`",
        "- `phases/v3/results/wave15_surface_trafficking_dependency/candidate_ranked.tsv`",
        "- `phases/v3/results/wave15_surface_trafficking_dependency/summary.json`",
        "",
        "## Bottom Line",
        "",
        str(summary["bottom_line"]),
        "",
    ]
    REPORT.write_text("\n".join(lines) + "\n")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    gene_tables = []
    module_tables = []
    presence_tables = []
    run_log: list[dict[str, object]] = []

    for label, func in [
        ("direct_h5ad", analyze_direct_h5ad),
        ("ms_microglia", analyze_ms_microglia),
        ("celiac_marker", analyze_celiac_marker),
        ("thyroid_spatial", analyze_thyroid_spatial),
    ]:
        genes, modules, presence, log_rows = func()
        if not genes.empty:
            gene_tables.append(genes)
        if not modules.empty:
            module_tables.append(modules)
        if not presence.empty:
            presence_tables.append(presence)
        run_log.extend(log_rows)
        if genes.empty and modules.empty:
            run_log.append({"analysis": label, "status": "no_output"})

    gene_scores = pd.concat(gene_tables, ignore_index=True) if gene_tables else pd.DataFrame()
    module_scores = pd.concat(module_tables, ignore_index=True) if module_tables else pd.DataFrame()
    presence = pd.concat(presence_tables, ignore_index=True) if presence_tables else pd.DataFrame()

    delta_tests = compare_gene_deltas(gene_scores)
    couplings = state_couplings(gene_scores, module_scores)
    delta_summary = summarize_gene_deltas(delta_tests)
    coupling_summary = summarize_couplings(couplings)
    rank = rank_candidates(delta_summary, coupling_summary, presence)

    gene_scores.to_csv(OUT / "candidate_donor_scores.tsv", sep="\t", index=False)
    module_scores.to_csv(OUT / "state_module_scores.tsv", sep="\t", index=False)
    presence.to_csv(OUT / "candidate_presence.tsv", sep="\t", index=False)
    pd.DataFrame(run_log).to_csv(OUT / "run_log.tsv", sep="\t", index=False)
    delta_tests.to_csv(OUT / "candidate_disease_delta_tests.tsv", sep="\t", index=False)
    couplings.to_csv(OUT / "candidate_state_couplings.tsv", sep="\t", index=False)
    delta_summary.to_csv(OUT / "candidate_delta_summary.tsv", sep="\t", index=False)
    coupling_summary.to_csv(OUT / "candidate_state_coupling_summary.tsv", sep="\t", index=False)
    rank.to_csv(OUT / "candidate_ranked.tsv", sep="\t", index=False)

    non_state = rank[~rank["is_state_control"]].sort_values("rank_score", ascending=False)
    go = non_state[non_state["go_no_go"].eq("GO_SCOUT")]
    if go.empty:
        bottom_line = (
            "No non-state surface/trafficking dependency met the strict local GO_SCOUT gate. "
            "The strongest local signals are useful dependency scouts, but each either lacks "
            "residual cross-disease coupling or is partly confounded by myeloid/phagocytic state."
        )
    else:
        top_gene = go.iloc[0]
        bottom_line = (
            f"{top_gene['gene']} is the top local GO_SCOUT dependency candidate in this family screen, "
            f"with residual CD74/HLA state coupling across {int(top_gene['n_state_resid_non_ifn_r_ge_0_35_diseases'])} diseases "
            f"and disease-control trend support across {int(top_gene['n_delta_trend_or_better_diseases'])} diseases. "
            "This is a local expression/state-coupling nomination, not causal validation."
        )

    summary = {
        "random_seed": SEED,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "n_candidate_genes": len(CANDIDATE_GENES),
        "minimum_candidates": MINIMUM_CANDIDATES,
        "extra_candidates": EXTRA_CANDIDATES,
        "n_gene_score_rows": int(len(gene_scores)),
        "n_module_score_rows": int(len(module_scores)),
        "n_delta_tests": int(len(delta_tests)),
        "n_coupling_tests": int(len(couplings)),
        "top_ranked_non_state": non_state.head(20).to_dict(orient="records"),
        "go_scout_candidates": go.to_dict(orient="records"),
        "bottom_line": bottom_line,
        "guardrail": (
            "Local donor/sample expression and state-coupling screen only; not causal inference, "
            "not prior-art/novelty, and not a clinical recommendation."
        ),
        "compute": {
            "pid": os.getpid(),
        },
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_markdown_report(rank, delta_tests, couplings, run_log, summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
