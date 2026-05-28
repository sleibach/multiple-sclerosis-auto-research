#!/usr/bin/env python3
"""Direct h5ad cell-state validation for tractable autoimmune atlases.

Inputs are public CZI h5ad files downloaded into data/raw_v3/cell_state:

- ibd_human_10x.h5ad: Crohn disease, ulcerative colitis, normal colon.
- psoriasis_skin.h5ad: psoriasis and normal skin.
- sjogren_salivary.h5ad: Sjogren syndrome and normal labial gland.
- ra_binvignat_blood.h5ad: rheumatoid arthritis and normal blood PBMCs.

The statistic is donor-level and compartment-restricted. Each gene is
library-size normalized per cell, log1p transformed, z-scored against normal
cells within the same analysis, then averaged into modules.
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
OUT = ROOT / "results_v3" / "direct_h5ad_cell_state"

MODULES = {
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "CD74", "IFI30", "HLA-DRA", "HLA-DRB1"],
    "hla_ii_apc": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "CIITA", "RFX5"],
    "lysosomal_apc": ["IFI30", "CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"],
    "mif_cd74_receptor_state": ["CD74", "CD44", "CXCR4", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1"],
    "mixscale_validated_ifng_readout": ["CD74", "CTSS", "IFI30", "CIITA", "TAP1", "TAP2", "B2M", "NLRC5"],
    "lipid_loader_repair": ["ACSL1", "APOE", "GPNMB", "LPL", "PLIN2", "CD36", "LIPA", "FABP5", "TREM2", "MSR1", "MERTK", "SPP1"],
    "complement_phagocytosis": ["C1QA", "C1QB", "C1QC", "CD68", "TREM2", "MERTK", "MSR1"],
    "hif_nampt_metabolic": ["HIF1A", "NAMPT", "LDHA", "SLC2A1", "NFKBIA", "IL1B", "HK2", "PFKFB3"],
    "inflammatory_nfkb": ["IL1B", "TNF", "CXCL8", "CCL2", "CCL3", "CCL4", "NFKBIA", "TREM1", "OSM"],
}
TARGET_GENES = sorted({gene for genes in MODULES.values() for gene in genes})


@dataclass(frozen=True)
class DirectConfig:
    name: str
    path: Path
    disease_label: str
    control_label: str
    compartment: str
    cell_types: tuple[str, ...]
    gene_symbol_column: str


CONFIGS = [
    DirectConfig(
        name="ibd_crohn_myeloid",
        path=RAW / "ibd_human_10x.h5ad",
        disease_label="Crohn disease",
        control_label="normal",
        compartment="colon myeloid",
        cell_types=("myeloid cell",),
        gene_symbol_column="gene_symbols",
    ),
    DirectConfig(
        name="ibd_uc_myeloid",
        path=RAW / "ibd_human_10x.h5ad",
        disease_label="ulcerative colitis",
        control_label="normal",
        compartment="colon myeloid",
        cell_types=("myeloid cell",),
        gene_symbol_column="gene_symbols",
    ),
    DirectConfig(
        name="ibd_crohn_epithelial",
        path=RAW / "ibd_human_10x.h5ad",
        disease_label="Crohn disease",
        control_label="normal",
        compartment="colon epithelial",
        cell_types=("colon epithelial cell",),
        gene_symbol_column="gene_symbols",
    ),
    DirectConfig(
        name="ibd_uc_epithelial",
        path=RAW / "ibd_human_10x.h5ad",
        disease_label="ulcerative colitis",
        control_label="normal",
        compartment="colon epithelial",
        cell_types=("colon epithelial cell",),
        gene_symbol_column="gene_symbols",
    ),
    DirectConfig(
        name="psoriasis_skin_apc",
        path=RAW / "psoriasis_skin.h5ad",
        disease_label="psoriasis",
        control_label="normal",
        compartment="skin APC",
        cell_types=("dendritic cell, human", "macrophage", "monocyte", "Langerhans cell"),
        gene_symbol_column="GeneSym",
    ),
    DirectConfig(
        name="psoriasis_keratinocyte",
        path=RAW / "psoriasis_skin.h5ad",
        disease_label="psoriasis",
        control_label="normal",
        compartment="skin keratinocyte",
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
        name="sjogren_gland_apc",
        path=RAW / "sjogren_salivary.h5ad",
        disease_label="Sjogren syndrome",
        control_label="normal",
        compartment="salivary gland APC",
        cell_types=("inflammatory macrophage", "alternatively activated macrophage", "dendritic cell"),
        gene_symbol_column="feature_name",
    ),
    DirectConfig(
        name="sjogren_gland_epithelial",
        path=RAW / "sjogren_salivary.h5ad",
        disease_label="Sjogren syndrome",
        control_label="normal",
        compartment="salivary gland epithelial",
        cell_types=("acinar cell of salivary gland", "duct epithelial cell"),
        gene_symbol_column="feature_name",
    ),
    DirectConfig(
        name="ra_blood_myeloid",
        path=RAW / "ra_binvignat_blood.h5ad",
        disease_label="rheumatoid arthritis",
        control_label="normal",
        compartment="blood myeloid/APC",
        cell_types=("classical monocyte", "non-classical monocyte", "myeloid dendritic cell"),
        gene_symbol_column="feature_name",
    ),
    DirectConfig(
        name="t1d_beta_cell",
        path=RAW / "t1d_hpap_islet.h5ad",
        disease_label="type 1 diabetes mellitus",
        control_label="normal",
        compartment="pancreatic beta cell",
        cell_types=("type B pancreatic cell",),
        gene_symbol_column="feature_name",
    ),
    DirectConfig(
        name="t1d_ductal_cell",
        path=RAW / "t1d_hpap_islet.h5ad",
        disease_label="type 1 diabetes mellitus",
        control_label="normal",
        compartment="pancreatic ductal cell",
        cell_types=("pancreatic ductal cell",),
        gene_symbol_column="feature_name",
    ),
    DirectConfig(
        name="t1d_acinar_cell",
        path=RAW / "t1d_hpap_islet.h5ad",
        disease_label="type 1 diabetes mellitus",
        control_label="normal",
        compartment="pancreatic acinar cell",
        cell_types=("pancreatic acinar cell",),
        gene_symbol_column="feature_name",
    ),
]


def hedges_g(case: np.ndarray, control: np.ndarray) -> float:
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
    return ((case.mean() - control.mean()) / math.sqrt(pooled)) * correction


def read_counts(path: Path):
    a = ad.read_h5ad(path)
    x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
    return a, x


def get_gene_indices(a, symbol_column: str) -> dict[str, int]:
    symbols = a.var[symbol_column].astype(str) if symbol_column in a.var.columns else a.var["feature_name"].astype(str)
    mapping = {}
    for idx, symbol in enumerate(symbols):
        if symbol in TARGET_GENES and symbol not in mapping:
            mapping[symbol] = idx
    return mapping


def analyze_config(config: DirectConfig, a, x) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    obs = a.obs.copy()
    mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
    obs_sub = obs.loc[mask].copy()
    cell_idx = np.flatnonzero(mask.to_numpy())
    gene_idx = get_gene_indices(a, config.gene_symbol_column)
    present_genes = sorted(gene_idx)
    if len(obs_sub) == 0 or not present_genes:
        raise ValueError(f"no cells or genes for {config.name}")
    target_x = x[cell_idx][:, [gene_idx[g] for g in present_genes]].astype(float)
    lib_size = np.asarray(x[cell_idx].sum(axis=1)).ravel().astype(float)
    lib_size[~np.isfinite(lib_size) | (lib_size <= 0)] = np.nan
    normalized = target_x.multiply(np.divide(1.0, lib_size, out=np.zeros_like(lib_size), where=np.isfinite(lib_size))[:, None]).multiply(1e4)
    log_expr = np.log1p(normalized.toarray())
    normal_mask = obs_sub["disease"].eq(config.control_label).to_numpy()
    gene_mean = np.nanmean(log_expr[normal_mask], axis=0)
    gene_sd = np.nanstd(log_expr[normal_mask], axis=0, ddof=1)
    gene_sd[~np.isfinite(gene_sd) | (gene_sd < 1e-6)] = 1.0
    z = (log_expr - gene_mean) / gene_sd

    gene_rows = []
    for j, gene in enumerate(present_genes):
        for group_name, group_mask in [
            ("case", obs_sub["disease"].eq(config.disease_label).to_numpy()),
            ("control", obs_sub["disease"].eq(config.control_label).to_numpy()),
        ]:
            vals = log_expr[group_mask, j]
            gene_rows.append(
                {
                    "analysis": config.name,
                    "gene": gene,
                    "group": group_name,
                    "n_cells": int(group_mask.sum()),
                    "mean_log_norm": float(np.nanmean(vals)),
                    "detection_fraction": float((vals > 0).mean()) if group_mask.sum() else np.nan,
                }
            )

    cell_scores = obs_sub[["donor_id", "disease", "cell_type", "tissue"]].reset_index(drop=True).copy()
    gene_to_local = {gene: i for i, gene in enumerate(present_genes)}
    module_gene_rows = []
    for module, genes in MODULES.items():
        present = [gene for gene in genes if gene in gene_to_local]
        module_gene_rows.append(
            {
                "analysis": config.name,
                "module": module,
                "n_genes_present": len(present),
                "genes_present": ",".join(present),
            }
        )
        idxs = [gene_to_local[gene] for gene in present]
        scores = np.nanmean(z[:, idxs], axis=1) if idxs else np.full(z.shape[0], np.nan)
        threshold = np.nanpercentile(scores[normal_mask], 75) if np.isfinite(scores[normal_mask]).any() else np.nan
        cell_scores[module] = scores
        cell_scores[f"{module}_high"] = scores > threshold

    donor_rows = []
    for (donor, disease), sub in cell_scores.groupby(["donor_id", "disease"], observed=True):
        if len(sub) < 10:
            continue
        for module in MODULES:
            donor_rows.append(
                {
                    "analysis": config.name,
                    "dataset_path": str(config.path.relative_to(ROOT)),
                    "disease_name": config.disease_label,
                    "compartment": config.compartment,
                    "donor_id": donor,
                    "disease": disease,
                    "group": "case" if disease == config.disease_label else "control",
                    "module": module,
                    "n_cells": int(len(sub)),
                    "mean_score": float(np.nanmean(sub[module])),
                    "high_fraction": float(sub[f"{module}_high"].mean()),
                    "cell_types": ",".join(sorted(sub["cell_type"].astype(str).unique())),
                }
            )
    return pd.DataFrame(donor_rows), pd.DataFrame(gene_rows), pd.DataFrame(module_gene_rows)


def compare_donors(donors: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (analysis, module), sub in donors.groupby(["analysis", "module"], observed=True):
        for metric in ["mean_score", "high_fraction"]:
            case = sub.loc[sub["group"] == "case", metric].to_numpy(float)
            control = sub.loc[sub["group"] == "control", metric].to_numpy(float)
            if len(case) >= 2 and len(control) >= 2:
                t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            first = sub.iloc[0]
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "module": module,
                    "metric": metric,
                    "n_case_donors": int(len(case)),
                    "n_control_donors": int(len(control)),
                    "mean_case": float(np.nanmean(case)) if len(case) else np.nan,
                    "mean_control": float(np.nanmean(control)) if len(control) else np.nan,
                    "delta_case_minus_control": float(np.nanmean(case) - np.nanmean(control)) if len(case) and len(control) else np.nan,
                    "hedges_g": hedges_g(case, control),
                    "welch_t": float(t_stat) if pd.notna(t_stat) else np.nan,
                    "p": float(p_value) if pd.notna(p_value) else np.nan,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
    return out


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    cache: dict[Path, tuple] = {}
    donor_tables = []
    gene_tables = []
    module_gene_tables = []
    run_log = []
    for config in CONFIGS:
        try:
            if config.path not in cache:
                cache[config.path] = read_counts(config.path)
            a, x = cache[config.path]
            donors, genes, module_genes = analyze_config(config, a, x)
            donor_tables.append(donors)
            gene_tables.append(genes)
            module_gene_tables.append(module_genes)
            run_log.append(
                {
                    "analysis": config.name,
                    "status": "completed",
                    "n_donor_module_rows": int(len(donors)),
                    "path": str(config.path.relative_to(ROOT)),
                }
            )
        except Exception as exc:
            run_log.append({"analysis": config.name, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})
    donors = pd.concat(donor_tables, ignore_index=True) if donor_tables else pd.DataFrame()
    genes = pd.concat(gene_tables, ignore_index=True) if gene_tables else pd.DataFrame()
    module_genes = pd.concat(module_gene_tables, ignore_index=True) if module_gene_tables else pd.DataFrame()
    comparisons = compare_donors(donors) if not donors.empty else pd.DataFrame()
    donors.to_csv(OUT / "direct_h5ad_donor_module_scores.tsv", sep="\t", index=False)
    genes.to_csv(OUT / "direct_h5ad_gene_detection_summary.tsv", sep="\t", index=False)
    module_genes.to_csv(OUT / "direct_h5ad_module_genes_present.tsv", sep="\t", index=False)
    comparisons.to_csv(OUT / "direct_h5ad_donor_module_comparisons.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "run_log": run_log,
        "top_positive_results": (
            comparisons.sort_values(["fdr", "hedges_g"], ascending=[True, False]).head(30).to_dict(orient="records")
            if not comparisons.empty
            else []
        ),
        "interpretation_guardrail": (
            "Direct h5ad results are observational donor-level validation in selected compartments. "
            "They support cross-disease recurrence of a cell state, not causality or treatment response."
        ),
    }
    (OUT / "direct_h5ad_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
