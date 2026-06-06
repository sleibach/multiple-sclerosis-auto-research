#!/usr/bin/env python3
"""Targeted OSM/OSMR and complement-axis analysis in direct h5ad atlases.

This is a post-hour-4 pivot analysis. Earlier IFN/HLA/CD74 and LIPA lanes
were demoted because they were either generic inflammatory states, prior-arted,
or inconsistent after residualization. This script tests two successor axes:

1. OSM-producing inflammatory myeloid/APC cells licensing OSMR+ tissue cells.
2. C1q/complement resident-myeloid and tissue-effector programs.

The operationalization is deliberately stronger than a single bulk score:
scores are donor-level, compartment-restricted, z-scored against matched
controls, and residualized against generic IFN, NF-kB, HIF/NAMPT, lipid-loader,
and lysosomal covariates.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse, stats
from statsmodels.stats.multitest import multipletests

SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "cell_state"
OUT = ROOT / "phases/v3/results" / "osmr_complement_axes"

TARGET_MODULES = {
    # OSM itself is sparse; the ligand module keeps OSM explicit while asking
    # whether it travels with inflammatory myeloid ligands.
    "osm_ligand_inflammatory_myeloid": [
        "OSM",
        "IL1B",
        "TNF",
        "CXCL8",
        "CCL2",
        "CCL3",
        "CCL4",
        "TREM1",
        "NFKBIA",
    ],
    # Receptor core is intentionally narrow. A positive result must involve the
    # actual OSM receptor machinery, not only downstream STAT3/NF-kB targets.
    "osmr_receptor_core": ["OSMR", "IL6ST", "LIFR", "IL31RA"],
    "osmr_signal_response": [
        "OSMR",
        "IL6ST",
        "STAT3",
        "SOCS3",
        "JUNB",
        "FOS",
        "CEBPB",
        "CXCL1",
        "CXCL2",
        "CXCL8",
        "CCL2",
        "C3",
        "SERPINE1",
        "SAA1",
        "SAA2",
    ],
    "c1q_phagocytic_myeloid": [
        "C1QA",
        "C1QB",
        "C1QC",
        "TYROBP",
        "TREM2",
        "APOE",
        "GPNMB",
        "LPL",
        "CD68",
        "MERTK",
        "MSR1",
        "LRP1",
    ],
    "complement_effector": [
        "C1R",
        "C1S",
        "C2",
        "C3",
        "CFB",
        "CFD",
        "SERPING1",
        "C3AR1",
        "C5AR1",
        "CD93",
        "CALR",
        "LRP1",
    ],
}

COVARIATE_MODULES = {
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "CD74", "IFI30", "HLA-DRA", "HLA-DRB1"],
    "hla_ii_apc": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "CIITA", "RFX5"],
    "lysosomal_apc": ["IFI30", "CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"],
    "lipid_loader_repair": ["ACSL1", "APOE", "GPNMB", "LPL", "PLIN2", "CD36", "LIPA", "FABP5", "TREM2", "MSR1", "MERTK", "SPP1"],
    "hif_nampt_metabolic": ["HIF1A", "NAMPT", "LDHA", "SLC2A1", "NFKBIA", "IL1B", "HK2", "PFKFB3"],
    "inflammatory_nfkb": ["IL1B", "TNF", "CXCL8", "CCL2", "CCL3", "CCL4", "NFKBIA", "TREM1", "OSM"],
}

MODULES = {**TARGET_MODULES, **COVARIATE_MODULES}
TARGET_GENES = sorted({gene for genes in MODULES.values() for gene in genes})


@dataclass(frozen=True)
class DirectConfig:
    name: str
    path: Path
    disease_label: str
    control_label: str
    compartment: str
    role: str
    cell_types: tuple[str, ...]
    gene_symbol_column: str


CONFIGS = [
    DirectConfig(
        name="ibd_crohn_myeloid",
        path=RAW / "ibd_human_10x.h5ad",
        disease_label="Crohn disease",
        control_label="normal",
        compartment="colon myeloid",
        role="myeloid_apc",
        cell_types=("myeloid cell",),
        gene_symbol_column="gene_symbols",
    ),
    DirectConfig(
        name="ibd_uc_myeloid",
        path=RAW / "ibd_human_10x.h5ad",
        disease_label="ulcerative colitis",
        control_label="normal",
        compartment="colon myeloid",
        role="myeloid_apc",
        cell_types=("myeloid cell",),
        gene_symbol_column="gene_symbols",
    ),
    DirectConfig(
        name="ibd_crohn_epithelial",
        path=RAW / "ibd_human_10x.h5ad",
        disease_label="Crohn disease",
        control_label="normal",
        compartment="colon epithelial",
        role="tissue_resident",
        cell_types=("colon epithelial cell",),
        gene_symbol_column="gene_symbols",
    ),
    DirectConfig(
        name="ibd_uc_epithelial",
        path=RAW / "ibd_human_10x.h5ad",
        disease_label="ulcerative colitis",
        control_label="normal",
        compartment="colon epithelial",
        role="tissue_resident",
        cell_types=("colon epithelial cell",),
        gene_symbol_column="gene_symbols",
    ),
    DirectConfig(
        name="ibd_crohn_stromal",
        path=RAW / "ibd_human_10x.h5ad",
        disease_label="Crohn disease",
        control_label="normal",
        compartment="colon stromal",
        role="tissue_resident",
        cell_types=("stromal cell of lamina propria of colon",),
        gene_symbol_column="gene_symbols",
    ),
    DirectConfig(
        name="ibd_uc_stromal",
        path=RAW / "ibd_human_10x.h5ad",
        disease_label="ulcerative colitis",
        control_label="normal",
        compartment="colon stromal",
        role="tissue_resident",
        cell_types=("stromal cell of lamina propria of colon",),
        gene_symbol_column="gene_symbols",
    ),
    DirectConfig(
        name="psoriasis_skin_apc",
        path=RAW / "psoriasis_skin.h5ad",
        disease_label="psoriasis",
        control_label="normal",
        compartment="skin APC",
        role="myeloid_apc",
        cell_types=("dendritic cell, human", "macrophage", "monocyte", "Langerhans cell"),
        gene_symbol_column="GeneSym",
    ),
    DirectConfig(
        name="psoriasis_keratinocyte",
        path=RAW / "psoriasis_skin.h5ad",
        disease_label="psoriasis",
        control_label="normal",
        compartment="skin keratinocyte",
        role="tissue_resident",
        cell_types=(
            "suprabasal keratinocyte",
            "spinous cell of epidermis",
            "granular cell of epidermis",
            "hair follicular keratinocyte",
            "basal cell of epidermis",
        ),
        gene_symbol_column="GeneSym",
    ),
    DirectConfig(
        name="psoriasis_skin_stromal",
        path=RAW / "psoriasis_skin.h5ad",
        disease_label="psoriasis",
        control_label="normal",
        compartment="skin stromal",
        role="tissue_resident",
        cell_types=(
            "fibroblast of papillary layer of dermis",
            "skin fibroblast",
            "fibroblast",
            "pericyte",
            "endothelial cell",
            "endothelial cell of lymphatic vessel",
        ),
        gene_symbol_column="GeneSym",
    ),
    DirectConfig(
        name="sjogren_gland_apc",
        path=RAW / "sjogren_salivary.h5ad",
        disease_label="Sjogren syndrome",
        control_label="normal",
        compartment="salivary gland APC",
        role="myeloid_apc",
        cell_types=("inflammatory macrophage", "alternatively activated macrophage", "dendritic cell"),
        gene_symbol_column="feature_name",
    ),
    DirectConfig(
        name="sjogren_gland_epithelial",
        path=RAW / "sjogren_salivary.h5ad",
        disease_label="Sjogren syndrome",
        control_label="normal",
        compartment="salivary gland epithelial",
        role="tissue_resident",
        cell_types=("acinar cell of salivary gland", "duct epithelial cell"),
        gene_symbol_column="feature_name",
    ),
    DirectConfig(
        name="sjogren_gland_stromal",
        path=RAW / "sjogren_salivary.h5ad",
        disease_label="Sjogren syndrome",
        control_label="normal",
        compartment="salivary gland stromal/endothelial",
        role="tissue_resident",
        cell_types=("fibroblast", "endothelial cell", "smooth muscle cell"),
        gene_symbol_column="feature_name",
    ),
    DirectConfig(
        name="ra_blood_myeloid",
        path=RAW / "ra_binvignat_blood.h5ad",
        disease_label="rheumatoid arthritis",
        control_label="normal",
        compartment="blood myeloid/APC",
        role="myeloid_apc",
        cell_types=("classical monocyte", "non-classical monocyte", "myeloid dendritic cell"),
        gene_symbol_column="feature_name",
    ),
    DirectConfig(
        name="t1d_beta_cell",
        path=RAW / "t1d_hpap_islet.h5ad",
        disease_label="type 1 diabetes mellitus",
        control_label="normal",
        compartment="pancreatic beta cell",
        role="tissue_resident",
        cell_types=("type B pancreatic cell",),
        gene_symbol_column="feature_name",
    ),
    DirectConfig(
        name="t1d_ductal_cell",
        path=RAW / "t1d_hpap_islet.h5ad",
        disease_label="type 1 diabetes mellitus",
        control_label="normal",
        compartment="pancreatic ductal cell",
        role="tissue_resident",
        cell_types=("pancreatic ductal cell",),
        gene_symbol_column="feature_name",
    ),
    DirectConfig(
        name="t1d_acinar_cell",
        path=RAW / "t1d_hpap_islet.h5ad",
        disease_label="type 1 diabetes mellitus",
        control_label="normal",
        compartment="pancreatic acinar cell",
        role="tissue_resident",
        cell_types=("pancreatic acinar cell",),
        gene_symbol_column="feature_name",
    ),
    DirectConfig(
        name="t1d_stellate_cell",
        path=RAW / "t1d_hpap_islet.h5ad",
        disease_label="type 1 diabetes mellitus",
        control_label="normal",
        compartment="pancreatic stellate cell",
        role="tissue_resident",
        cell_types=("pancreatic stellate cell",),
        gene_symbol_column="feature_name",
    ),
    DirectConfig(
        name="t1d_endothelial_cell",
        path=RAW / "t1d_hpap_islet.h5ad",
        disease_label="type 1 diabetes mellitus",
        control_label="normal",
        compartment="pancreatic endothelial cell",
        role="tissue_resident",
        cell_types=("endothelial cell",),
        gene_symbol_column="feature_name",
    ),
]


def hedges_g(case: np.ndarray, control: np.ndarray) -> float:
    case = np.asarray(case, dtype=float)
    control = np.asarray(control, dtype=float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if len(case) < 2 or len(control) < 2:
        return np.nan
    pooled = ((len(case) - 1) * case.var(ddof=1) + (len(control) - 1) * control.var(ddof=1)) / (
        len(case) + len(control) - 2
    )
    if pooled <= 0:
        return np.nan
    correction = 1.0 - (3.0 / (4.0 * (len(case) + len(control)) - 9.0))
    return float(((case.mean() - control.mean()) / math.sqrt(pooled)) * correction)


def read_counts(path: Path):
    a = ad.read_h5ad(path)
    x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
    return a, x


def get_gene_indices(a, symbol_column: str) -> dict[str, int]:
    if symbol_column in a.var.columns:
        symbols = a.var[symbol_column].astype(str)
    elif "feature_name" in a.var.columns:
        symbols = a.var["feature_name"].astype(str)
    else:
        symbols = pd.Series(a.var_names.astype(str), index=a.var.index)
    mapping: dict[str, int] = {}
    for idx, symbol in enumerate(symbols):
        if symbol in TARGET_GENES and symbol not in mapping:
            mapping[symbol] = idx
    return mapping


def compare_values(values: pd.Series, groups: pd.Series) -> dict[str, float]:
    case = values.loc[groups == "case"].to_numpy(float)
    control = values.loc[groups == "control"].to_numpy(float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if len(case) >= 2 and len(control) >= 2:
        t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
    else:
        t_stat, p_value = np.nan, np.nan
    return {
        "n_case_donors": int(len(case)),
        "n_control_donors": int(len(control)),
        "mean_case": float(np.nanmean(case)) if len(case) else np.nan,
        "mean_control": float(np.nanmean(control)) if len(control) else np.nan,
        "delta_case_minus_control": float(np.nanmean(case) - np.nanmean(control)) if len(case) and len(control) else np.nan,
        "hedges_g": hedges_g(case, control),
        "welch_t": float(t_stat) if pd.notna(t_stat) else np.nan,
        "p": float(p_value) if pd.notna(p_value) else np.nan,
    }


def residualize(y: np.ndarray, x: np.ndarray) -> tuple[np.ndarray, float, float]:
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    mask = np.isfinite(y) & np.isfinite(x)
    residuals = np.full(len(y), np.nan)
    if mask.sum() < 4 or np.nanstd(x[mask]) <= 0:
        return residuals, np.nan, np.nan
    slope, intercept, r_value, _, _ = stats.linregress(x[mask], y[mask])
    residuals[mask] = y[mask] - (intercept + slope * x[mask])
    return residuals, float(slope), float(r_value**2)


def analyze_config(config: DirectConfig, a, x) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    obs = a.obs.copy()
    mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
    obs_sub = obs.loc[mask].copy()
    cell_idx = np.flatnonzero(mask.to_numpy())
    gene_idx = get_gene_indices(a, config.gene_symbol_column)
    present_genes = [gene for gene in TARGET_GENES if gene in gene_idx]
    if len(obs_sub) == 0 or not present_genes:
        raise ValueError(f"no cells or target genes for {config.name}")

    target_x = x[cell_idx][:, [gene_idx[g] for g in present_genes]].astype(float)
    lib_size = np.asarray(x[cell_idx].sum(axis=1)).ravel().astype(float)
    lib_size[~np.isfinite(lib_size) | (lib_size <= 0)] = np.nan
    normalizer = np.divide(1.0, lib_size, out=np.zeros_like(lib_size), where=np.isfinite(lib_size))
    normalized = target_x.multiply(normalizer[:, None]).multiply(1e4)
    log_expr = np.log1p(normalized.toarray())

    normal_mask = obs_sub["disease"].eq(config.control_label).to_numpy()
    gene_mean = np.nanmean(log_expr[normal_mask], axis=0)
    gene_sd = np.nanstd(log_expr[normal_mask], axis=0, ddof=1)
    gene_sd[~np.isfinite(gene_sd) | (gene_sd < 1e-6)] = 1.0
    z = (log_expr - gene_mean) / gene_sd

    gene_to_local = {gene: i for i, gene in enumerate(present_genes)}
    cell_scores = obs_sub[["donor_id", "disease", "cell_type", "tissue"]].reset_index(drop=True).copy()
    module_gene_rows: list[dict[str, object]] = []
    for module, genes in MODULES.items():
        present = [gene for gene in genes if gene in gene_to_local]
        module_gene_rows.append(
            {
                "analysis": config.name,
                "disease_name": config.disease_label,
                "compartment": config.compartment,
                "role": config.role,
                "module": module,
                "module_class": "target" if module in TARGET_MODULES else "covariate",
                "n_genes_present": len(present),
                "genes_present": ",".join(present),
            }
        )
        idxs = [gene_to_local[gene] for gene in present]
        scores = np.nanmean(z[:, idxs], axis=1) if idxs else np.full(z.shape[0], np.nan)
        threshold = np.nanpercentile(scores[normal_mask], 75) if np.isfinite(scores[normal_mask]).any() else np.nan
        cell_scores[module] = scores
        cell_scores[f"{module}_high"] = scores > threshold

    module_rows: list[dict[str, object]] = []
    gene_rows: list[dict[str, object]] = []
    for (donor, disease), sub_idx in cell_scores.groupby(["donor_id", "disease"], observed=True).groups.items():
        idx = np.fromiter(sub_idx, dtype=int)
        if len(idx) < 10:
            continue
        group = "case" if disease == config.disease_label else "control"
        base = {
            "analysis": config.name,
            "dataset_path": str(config.path.relative_to(ROOT)),
            "disease_name": config.disease_label,
            "compartment": config.compartment,
            "role": config.role,
            "donor_id": donor,
            "disease": disease,
            "group": group,
            "n_cells": int(len(idx)),
            "cell_types": ",".join(sorted(cell_scores.iloc[idx]["cell_type"].astype(str).unique())),
        }
        for module in MODULES:
            module_rows.append(
                {
                    **base,
                    "module": module,
                    "module_class": "target" if module in TARGET_MODULES else "covariate",
                    "mean_score": float(np.nanmean(cell_scores.iloc[idx][module])),
                    "high_fraction": float(cell_scores.iloc[idx][f"{module}_high"].mean()),
                }
            )
        for gene in present_genes:
            j = gene_to_local[gene]
            vals = log_expr[idx, j]
            zvals = z[idx, j]
            gene_rows.append(
                {
                    **base,
                    "gene": gene,
                    "mean_log_norm": float(np.nanmean(vals)),
                    "mean_z_vs_controls": float(np.nanmean(zvals)),
                    "detection_fraction": float((vals > 0).mean()),
                }
            )

    return pd.DataFrame(module_rows), pd.DataFrame(gene_rows), pd.DataFrame(module_gene_rows)


def compare_modules(module_scores: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (analysis, module), sub in module_scores.groupby(["analysis", "module"], observed=True):
        for metric in ["mean_score", "high_fraction"]:
            stats_row = compare_values(sub[metric], sub["group"])
            first = sub.iloc[0]
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "module": module,
                    "module_class": first["module_class"],
                    "metric": metric,
                    **stats_row,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
    return out


def compare_genes(gene_scores: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (analysis, gene), sub in gene_scores.groupby(["analysis", "gene"], observed=True):
        for metric in ["mean_z_vs_controls", "detection_fraction"]:
            stats_row = compare_values(sub[metric], sub["group"])
            first = sub.iloc[0]
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "gene": gene,
                    "metric": metric,
                    **stats_row,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
    return out


def residual_tests(module_scores: pd.DataFrame, gene_scores: pd.DataFrame) -> pd.DataFrame:
    module_wide = module_scores.pivot_table(
        index=["analysis", "donor_id"],
        columns="module",
        values="mean_score",
        aggfunc="mean",
    ).reset_index()
    sample_meta = module_scores.drop_duplicates(["analysis", "donor_id"])[
        ["analysis", "donor_id", "disease_name", "compartment", "role", "group"]
    ]
    module_wide = sample_meta.merge(module_wide, on=["analysis", "donor_id"], how="left")

    rows: list[dict[str, object]] = []
    for target in TARGET_MODULES:
        for (analysis, compartment), sub in module_wide.groupby(["analysis", "compartment"], observed=True):
            if target not in sub.columns:
                continue
            raw = compare_values(sub[target], sub["group"])
            for covariate in COVARIATE_MODULES:
                if covariate not in sub.columns:
                    continue
                residuals, slope, r2 = residualize(sub[target].to_numpy(float), sub[covariate].to_numpy(float))
                residual = compare_values(pd.Series(residuals, index=sub.index), sub["group"])
                first = sub.iloc[0]
                rows.append(
                    {
                        "feature_type": "module",
                        "feature": target,
                        "analysis": analysis,
                        "disease_name": first["disease_name"],
                        "compartment": compartment,
                        "role": first["role"],
                        "covariate_module": covariate,
                        "covariate_slope": slope,
                        "covariate_r2": r2,
                        **{f"raw_{k}": v for k, v in raw.items()},
                        **{f"residual_{k}": v for k, v in residual.items()},
                    }
                )

    genes_of_interest = ["OSM", "OSMR", "IL6ST", "SOCS3", "C1QA", "C1QB", "C1QC", "C3", "C3AR1", "C5AR1"]
    covariates = module_wide[
        ["analysis", "donor_id", *[c for c in COVARIATE_MODULES if c in module_wide.columns]]
    ]
    gene_aug = gene_scores.loc[gene_scores["gene"].isin(genes_of_interest)].merge(
        covariates, on=["analysis", "donor_id"], how="left"
    )
    for (analysis, gene), sub in gene_aug.groupby(["analysis", "gene"], observed=True):
        raw = compare_values(sub["mean_z_vs_controls"], sub["group"])
        for covariate in COVARIATE_MODULES:
            if covariate not in sub.columns:
                continue
            residuals, slope, r2 = residualize(
                sub["mean_z_vs_controls"].to_numpy(float),
                sub[covariate].to_numpy(float),
            )
            residual = compare_values(pd.Series(residuals, index=sub.index), sub["group"])
            first = sub.iloc[0]
            rows.append(
                {
                    "feature_type": "gene",
                    "feature": gene,
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "covariate_module": covariate,
                    "covariate_slope": slope,
                    "covariate_r2": r2,
                    **{f"raw_{k}": v for k, v in raw.items()},
                    **{f"residual_{k}": v for k, v in residual.items()},
                }
            )

    out = pd.DataFrame(rows)
    if not out.empty:
        out["residual_fdr"] = multipletests(out["residual_p"].fillna(1.0), method="fdr_bh")[1]
        out["retains_nominal_positive"] = (
            (out["raw_delta_case_minus_control"] > 0)
            & (out["raw_p"] < 0.05)
            & (out["residual_delta_case_minus_control"] > 0)
            & (out["residual_p"] < 0.05)
        )
    return out


def build_axis_summary(module_comparisons: pd.DataFrame, gene_comparisons: pd.DataFrame, residuals: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    module_mean = module_comparisons.loc[module_comparisons["metric"] == "mean_score"].copy()
    gene_mean = gene_comparisons.loc[gene_comparisons["metric"] == "mean_z_vs_controls"].copy()
    for disease, dmods in module_mean.groupby("disease_name", observed=True):
        dgenes = gene_mean.loc[gene_mean["disease_name"] == disease]
        dres = residuals.loc[residuals["disease_name"] == disease] if not residuals.empty else pd.DataFrame()
        for axis, features in {
            "osm_osmr": ["osm_ligand_inflammatory_myeloid", "osmr_receptor_core", "osmr_signal_response"],
            "complement_c1q": ["c1q_phagocytic_myeloid", "complement_effector"],
        }.items():
            module_support = dmods.loc[
                dmods["module"].isin(features)
                & (dmods["delta_case_minus_control"] > 0)
                & (dmods["p"] < 0.05)
            ]
            gene_features = ["OSM", "OSMR", "IL6ST", "SOCS3"] if axis == "osm_osmr" else ["C1QA", "C1QB", "C1QC", "C3", "C3AR1", "C5AR1"]
            gene_support = dgenes.loc[
                dgenes["gene"].isin(gene_features)
                & (dgenes["delta_case_minus_control"] > 0)
                & (dgenes["p"] < 0.05)
            ]
            residual_support = (
                dres.loc[
                    dres["feature"].isin([*features, *gene_features])
                    & dres.get("retains_nominal_positive", False)
                ]
                if not dres.empty
                else pd.DataFrame()
            )
            rows.append(
                {
                    "disease_name": disease,
                    "axis": axis,
                    "n_positive_modules_nominal": int(len(module_support)),
                    "positive_modules": ";".join(
                        module_support.sort_values("p")["analysis"].astype(str)
                        + ":"
                        + module_support.sort_values("p")["module"].astype(str)
                    ),
                    "n_positive_genes_nominal": int(len(gene_support)),
                    "positive_genes": ";".join(
                        gene_support.sort_values("p")["analysis"].astype(str)
                        + ":"
                        + gene_support.sort_values("p")["gene"].astype(str)
                    ),
                    "n_residual_retained_nominal_tests": int(len(residual_support)),
                    "residual_retained_features": ";".join(
                        residual_support.sort_values("residual_p")["analysis"].astype(str)
                        + ":"
                        + residual_support.sort_values("residual_p")["feature"].astype(str)
                        + "|"
                        + residual_support.sort_values("residual_p")["covariate_module"].astype(str)
                    )
                    if not residual_support.empty
                    else "",
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    cache: dict[Path, tuple] = {}
    module_tables: list[pd.DataFrame] = []
    gene_tables: list[pd.DataFrame] = []
    module_gene_tables: list[pd.DataFrame] = []
    run_log: list[dict[str, object]] = []

    for config in CONFIGS:
        try:
            if config.path not in cache:
                cache[config.path] = read_counts(config.path)
            a, x = cache[config.path]
            modules, genes, module_genes = analyze_config(config, a, x)
            module_tables.append(modules)
            gene_tables.append(genes)
            module_gene_tables.append(module_genes)
            run_log.append(
                {
                    "analysis": config.name,
                    "status": "completed",
                    "n_module_rows": int(len(modules)),
                    "n_gene_rows": int(len(genes)),
                    "path": str(config.path.relative_to(ROOT)),
                }
            )
        except Exception as exc:
            run_log.append({"analysis": config.name, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})

    module_scores = pd.concat(module_tables, ignore_index=True) if module_tables else pd.DataFrame()
    gene_scores = pd.concat(gene_tables, ignore_index=True) if gene_tables else pd.DataFrame()
    module_genes = pd.concat(module_gene_tables, ignore_index=True) if module_gene_tables else pd.DataFrame()
    module_comparisons = compare_modules(module_scores) if not module_scores.empty else pd.DataFrame()
    gene_comparisons = compare_genes(gene_scores) if not gene_scores.empty else pd.DataFrame()
    residual_table = residual_tests(module_scores, gene_scores) if not module_scores.empty and not gene_scores.empty else pd.DataFrame()
    axis_summary = build_axis_summary(module_comparisons, gene_comparisons, residual_table)

    module_scores.to_csv(OUT / "osmr_complement_donor_module_scores.tsv", sep="\t", index=False)
    gene_scores.to_csv(OUT / "osmr_complement_gene_scores.tsv", sep="\t", index=False)
    module_genes.to_csv(OUT / "osmr_complement_module_genes_present.tsv", sep="\t", index=False)
    module_comparisons.to_csv(OUT / "osmr_complement_module_comparisons.tsv", sep="\t", index=False)
    gene_comparisons.to_csv(OUT / "osmr_complement_gene_comparisons.tsv", sep="\t", index=False)
    residual_table.to_csv(OUT / "osmr_complement_residual_tests.tsv", sep="\t", index=False)
    axis_summary.to_csv(OUT / "osmr_complement_axis_summary.tsv", sep="\t", index=False)

    target_module_mean = module_comparisons.loc[
        (module_comparisons["metric"] == "mean_score")
        & (module_comparisons["module_class"] == "target")
        & (module_comparisons["delta_case_minus_control"] > 0)
    ].sort_values(["fdr", "p", "hedges_g"], ascending=[True, True, False])
    target_gene_mean = gene_comparisons.loc[
        (gene_comparisons["metric"] == "mean_z_vs_controls")
        & (gene_comparisons["gene"].isin(["OSM", "OSMR", "IL6ST", "SOCS3", "C1QA", "C1QB", "C1QC", "C3", "C3AR1", "C5AR1"]))
        & (gene_comparisons["delta_case_minus_control"] > 0)
    ].sort_values(["fdr", "p", "hedges_g"], ascending=[True, True, False])
    retained_residuals = (
        residual_table.loc[residual_table["retains_nominal_positive"]]
        .sort_values(["residual_fdr", "residual_p", "residual_hedges_g"], ascending=[True, True, False])
        if not residual_table.empty
        else pd.DataFrame()
    )

    summary = {
        "random_seed": SEED,
        "run_log": run_log,
        "n_module_comparisons": int(len(module_comparisons)),
        "n_gene_comparisons": int(len(gene_comparisons)),
        "n_residual_tests": int(len(residual_table)),
        "top_target_module_positive_mean_score": target_module_mean.head(40).to_dict(orient="records"),
        "top_target_gene_positive_mean_z": target_gene_mean.head(60).to_dict(orient="records"),
        "residual_retained_nominal_positive_tests": retained_residuals.head(80).to_dict(orient="records"),
        "axis_summary": axis_summary.to_dict(orient="records"),
        "interpretation_guardrail": (
            "This analysis supports or demotes compartment-specific paracrine axes. "
            "It is observational and donor-level; residualization against one covariate module at a time "
            "does not establish causality, remove all severity/composition effects, or prove ligand-receptor contact."
        ),
    }
    (OUT / "osmr_complement_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
