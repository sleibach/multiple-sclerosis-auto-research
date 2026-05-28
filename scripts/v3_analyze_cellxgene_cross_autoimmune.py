#!/usr/bin/env python3
"""Cross-autoimmune cell-state replication using CELLxGENE Census.

The analysis is compartment-restricted and donor-level:

1. Pull only target genes for disease-relevant cell compartments.
2. Normalize raw counts per cell with raw_sum.
3. Z-score each gene relative to normal cells within the same dataset/compartment.
4. Average gene z-scores into modules.
5. Test donor-level disease vs normal mean score and high-state fraction.

This is still observational single-cell evidence, not causality.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse, stats
from statsmodels.stats.multitest import multipletests

import cellxgene_census

SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "cellxgene"
CENSUS_URI = "s3://cellxgene-census-public-us-west-2/cell-census/2025-11-17/soma/"
MAX_CELLS_PER_DONOR_CELLTYPE = 200

MODULES = {
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "CD74", "IFI30", "HLA-DRA", "HLA-DRB1"],
    "hla_ii_apc": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "CIITA", "RFX5"],
    "lysosomal_apc": ["IFI30", "CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"],
    "mif_cd74_receptor_state": ["CD74", "CD44", "CXCR4", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1"],
    "mixscale_validated_ifng_readout": ["CD74", "CTSS", "IFI30", "CIITA", "TAP1", "TAP2", "B2M", "NLRC5"],
}
TARGET_GENES = sorted({gene for genes in MODULES.values() for gene in genes})


@dataclass(frozen=True)
class AnalysisConfig:
    name: str
    disease_label: str
    control_label: str
    dataset_id: str
    compartment: str
    cell_types: tuple[str, ...]


CONFIGS = [
    AnalysisConfig(
        name="psoriasis_skin_apc",
        disease_label="psoriasis",
        control_label="normal",
        dataset_id="b796f27e-e191-4f2d-b40c-e6ac58163b4e",
        compartment="skin APC",
        cell_types=("dendritic cell, human", "macrophage", "monocyte", "Langerhans cell"),
    ),
    AnalysisConfig(
        name="sjogren_salivary_myeloid",
        disease_label="Sjogren syndrome",
        control_label="normal",
        dataset_id="df1edb87-e512-43ae-b5f4-cb179cfc2bb4",
        compartment="salivary gland myeloid/APC",
        cell_types=("inflammatory macrophage", "alternatively activated macrophage", "dendritic cell"),
    ),
    AnalysisConfig(
        name="sjogren_salivary_epithelial",
        disease_label="Sjogren syndrome",
        control_label="normal",
        dataset_id="df1edb87-e512-43ae-b5f4-cb179cfc2bb4",
        compartment="salivary gland epithelial",
        cell_types=("acinar cell of salivary gland", "duct epithelial cell", "myoepithelial cell"),
    ),
    AnalysisConfig(
        name="crohn_gut_myeloid",
        disease_label="Crohn disease",
        control_label="normal",
        dataset_id="a37f857c-779f-464e-9310-3db43a1811e7",
        compartment="terminal ileum immune myeloid/APC",
        cell_types=("macrophage", "plasmacytoid dendritic cell", "dendritic cell"),
    ),
    AnalysisConfig(
        name="ra_blood_myeloid",
        disease_label="rheumatoid arthritis",
        control_label="normal",
        dataset_id="d18736c3-6292-4379-919a-d6d973204c87",
        compartment="blood myeloid/APC",
        cell_types=("classical monocyte", "non-classical monocyte", "myeloid dendritic cell"),
    ),
    AnalysisConfig(
        name="sle_blood_myeloid",
        disease_label="systemic lupus erythematosus",
        control_label="normal",
        dataset_id="218acb0f-9f2f-4f76-b90b-15a4b7c7f629",
        compartment="blood myeloid/APC",
        cell_types=(
            "classical monocyte",
            "non-classical monocyte",
            "conventional dendritic cell",
            "plasmacytoid dendritic cell",
        ),
    ),
]


def quoted_list(values: tuple[str, ...] | list[str]) -> str:
    return "[" + ", ".join(repr(v) for v in values) + "]"


def hedges_g(case: np.ndarray, control: np.ndarray) -> float:
    case = np.asarray(case, dtype=float)
    control = np.asarray(control, dtype=float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    nx = case.size
    ny = control.size
    if nx < 2 or ny < 2:
        return np.nan
    pooled = ((nx - 1) * case.var(ddof=1) + (ny - 1) * control.var(ddof=1)) / (nx + ny - 2)
    if pooled <= 0:
        return np.nan
    correction = 1.0 - (3.0 / (4.0 * (nx + ny) - 9.0))
    return ((case.mean() - control.mean()) / math.sqrt(pooled)) * correction


def get_subset(census, config: AnalysisConfig):
    obs = census["census_data"]["homo_sapiens"].obs
    var = census["census_data"]["homo_sapiens"].ms["RNA"].var
    disease_filter = f"(disease == {config.disease_label!r} or disease == {config.control_label!r})"
    cell_filter = " or ".join(f"cell_type == {cell_type!r}" for cell_type in config.cell_types)
    obs_filter = (
        f"dataset_id == {config.dataset_id!r} and {disease_filter} "
        f"and ({cell_filter}) and is_primary_data == True"
    )
    obs_df = obs.read(
        value_filter=obs_filter,
        column_names=[
            "soma_joinid",
            "dataset_id",
            "disease",
            "donor_id",
            "cell_type",
            "tissue",
            "raw_sum",
        ],
    ).concat().to_pandas()
    if obs_df.empty:
        raise ValueError("no cells matched obs filter")
    obs_df = (
        obs_df.groupby(["disease", "donor_id", "cell_type"], group_keys=False, observed=True)
        .apply(
            lambda sub: sub.sample(
                n=min(len(sub), MAX_CELLS_PER_DONOR_CELLTYPE),
                random_state=SEED,
            )
        )
        .reset_index(drop=True)
    )
    var_filter = "feature_name in " + quoted_list(TARGET_GENES)
    var_df = var.read(
        value_filter=var_filter,
        column_names=["soma_joinid", "feature_name", "feature_id"],
    ).concat().to_pandas()
    if var_df.empty:
        raise ValueError("no target genes matched var filter")
    return cellxgene_census.get_anndata(
        census,
        organism="homo_sapiens",
        measurement_name="RNA",
        X_name="raw",
        obs_coords=obs_df["soma_joinid"].to_numpy(),
        var_coords=var_df["soma_joinid"].to_numpy(),
        obs_column_names=["dataset_id", "disease", "donor_id", "cell_type", "tissue", "raw_sum"],
        var_column_names=["feature_name", "feature_id"],
    )


def normalized_log_matrix(adata) -> np.ndarray:
    x = adata.X
    if sparse.issparse(x):
        x = x.tocsr().astype(float)
        raw_sum = adata.obs["raw_sum"].to_numpy(dtype=float)
        raw_sum[~np.isfinite(raw_sum) | (raw_sum <= 0)] = np.nan
        inv = np.divide(1.0, raw_sum, out=np.zeros_like(raw_sum, dtype=float), where=np.isfinite(raw_sum))
        normalized = x.multiply(inv[:, None]).multiply(1e4)
        return np.log1p(normalized.toarray())
    arr = np.asarray(x, dtype=float)
    raw_sum = adata.obs["raw_sum"].to_numpy(dtype=float)
    raw_sum[~np.isfinite(raw_sum) | (raw_sum <= 0)] = np.nan
    normalized = np.divide(arr, raw_sum[:, None], out=np.zeros_like(arr, dtype=float), where=np.isfinite(raw_sum[:, None])) * 1e4
    return np.log1p(normalized)


def score_modules(adata, config: AnalysisConfig) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    obs = adata.obs.reset_index(drop=True).copy()
    genes = adata.var["feature_name"].astype(str).tolist()
    gene_to_idx = {gene: i for i, gene in enumerate(genes)}
    log_expr = normalized_log_matrix(adata)
    normal_mask = obs["disease"].eq(config.control_label).to_numpy()
    gene_mean = np.nanmean(log_expr[normal_mask], axis=0)
    gene_sd = np.nanstd(log_expr[normal_mask], axis=0, ddof=1)
    gene_sd[~np.isfinite(gene_sd) | (gene_sd < 1e-6)] = 1.0
    z = (log_expr - gene_mean) / gene_sd

    cell_scores = obs[["dataset_id", "disease", "donor_id", "cell_type", "tissue"]].copy()
    gene_rows = []
    for gene, idx in gene_to_idx.items():
        vals = log_expr[:, idx]
        for disease, mask in [("case", obs["disease"].eq(config.disease_label)), ("control", obs["disease"].eq(config.control_label))]:
            gene_rows.append(
                {
                    "analysis": config.name,
                    "gene": gene,
                    "group": disease,
                    "n_cells": int(mask.sum()),
                    "mean_log_norm": float(np.nanmean(vals[mask])),
                    "detection_fraction": float((vals[mask] > 0).mean()) if int(mask.sum()) else np.nan,
                }
            )

    for module, module_genes in MODULES.items():
        present = [gene for gene in module_genes if gene in gene_to_idx]
        if not present:
            cell_scores[module] = np.nan
            cell_scores[f"{module}_high"] = False
            continue
        idxs = [gene_to_idx[gene] for gene in present]
        scores = np.nanmean(z[:, idxs], axis=1)
        threshold = np.nanpercentile(scores[normal_mask], 75) if normal_mask.sum() else np.nan
        cell_scores[module] = scores
        cell_scores[f"{module}_high"] = scores > threshold
    return cell_scores, pd.DataFrame(gene_rows), pd.DataFrame({"gene": genes})


def donor_summary(cell_scores: pd.DataFrame, config: AnalysisConfig) -> pd.DataFrame:
    rows = []
    for (donor, disease), sub in cell_scores.groupby(["donor_id", "disease"], observed=True):
        if len(sub) < 10:
            continue
        for module in MODULES:
            values = sub[module].to_numpy(dtype=float)
            rows.append(
                {
                    "analysis": config.name,
                    "disease_name": config.disease_label,
                    "dataset_id": config.dataset_id,
                    "compartment": config.compartment,
                    "donor_id": donor,
                    "disease": disease,
                    "group": "case" if disease == config.disease_label else "control",
                    "module": module,
                    "n_cells": int(len(sub)),
                    "mean_score": float(np.nanmean(values)),
                    "median_score": float(np.nanmedian(values)),
                    "high_fraction": float(sub[f"{module}_high"].mean()),
                    "cell_types": ",".join(sorted(sub["cell_type"].astype(str).unique())),
                }
            )
    return pd.DataFrame(rows)


def compare_donors(donors: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (analysis, module), sub in donors.groupby(["analysis", "module"]):
        for metric in ["mean_score", "high_fraction"]:
            case = sub.loc[sub["group"] == "case", metric].to_numpy(dtype=float)
            control = sub.loc[sub["group"] == "control", metric].to_numpy(dtype=float)
            if len(case) >= 2 and len(control) >= 2:
                t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            first = sub.iloc[0]
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "dataset_id": first["dataset_id"],
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
    all_cells = []
    all_donors = []
    all_genes = []
    run_log = []
    with cellxgene_census.open_soma(uri=CENSUS_URI) as census:
        for config in CONFIGS:
            try:
                print(f"Loading {config.name}", flush=True)
                adata = get_subset(census, config)
                n_cells, n_genes = adata.shape
                print(f"Loaded {config.name}: {n_cells} cells x {n_genes} genes", flush=True)
                run_log.append(
                    {
                        "analysis": config.name,
                        "status": "loaded",
                        "n_cells": int(n_cells),
                        "n_genes": int(n_genes),
                        "cell_types": list(config.cell_types),
                    }
                )
                if n_cells == 0 or n_genes == 0:
                    continue
                cell_scores, gene_summary, genes_present = score_modules(adata, config)
                donors = donor_summary(cell_scores, config)
                cell_scores["analysis"] = config.name
                cell_scores["disease_name"] = config.disease_label
                gene_summary["dataset_id"] = config.dataset_id
                gene_summary["compartment"] = config.compartment
                genes_present["analysis"] = config.name
                all_cells.append(cell_scores)
                all_donors.append(donors)
                all_genes.append(gene_summary)
                donors.to_csv(OUT / f"{config.name}_donor_module_scores.tsv", sep="\t", index=False)
                gene_summary.to_csv(OUT / f"{config.name}_gene_detection_summary.tsv", sep="\t", index=False)
            except Exception as exc:
                print(f"Failed {config.name}: {type(exc).__name__}: {exc}", flush=True)
                run_log.append(
                    {
                        "analysis": config.name,
                        "status": "failed",
                        "error": f"{type(exc).__name__}: {exc}",
                        "cell_types": list(config.cell_types),
                    }
                )

    cells = pd.concat(all_cells, ignore_index=True) if all_cells else pd.DataFrame()
    donors = pd.concat(all_donors, ignore_index=True) if all_donors else pd.DataFrame()
    genes = pd.concat(all_genes, ignore_index=True) if all_genes else pd.DataFrame()
    comparisons = compare_donors(donors) if not donors.empty else pd.DataFrame()
    cells.to_csv(OUT / "cellxgene_cell_module_scores.tsv.gz", sep="\t", index=False, compression="gzip")
    donors.to_csv(OUT / "cellxgene_donor_module_scores.tsv", sep="\t", index=False)
    genes.to_csv(OUT / "cellxgene_gene_detection_summary.tsv", sep="\t", index=False)
    comparisons.to_csv(OUT / "cellxgene_donor_module_comparisons.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "census_uri": CENSUS_URI,
        "configs": [config.__dict__ for config in CONFIGS],
        "run_log": run_log,
        "top_positive_results": (
            comparisons.sort_values(["fdr", "hedges_g"], ascending=[True, False])
            .head(30)
            .to_dict(orient="records")
            if not comparisons.empty
            else []
        ),
        "interpretation_guardrail": (
            "CELLxGENE results are observational, donor-level, compartment-restricted single-cell evidence. "
            "They do not prove causality and remain sensitive to donor mix, tissue site, and study integration."
        ),
    }
    (OUT / "cellxgene_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
