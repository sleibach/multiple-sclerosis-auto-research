#!/usr/bin/env python3
"""Targeted CELLxGENE Census SLE PBMC validation.

The Perez et al. lupus PBMC source h5ad is 11.3 GB. This script avoids a full
download by sampling disease/control monocyte and dendritic-cell strata from
the Census and materializing only the V3 module genes.

This is a route-around for a real resource ceiling, not a substitute for a
full atlas reanalysis. Outputs are donor-level and should be interpreted as
recurrence evidence only.
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

import cellxgene_census
import numpy as np
import pandas as pd
from scipy import sparse, stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import MODULES, ROOT, TARGET_GENES

SEED = 20260526
CENSUS_URI = "s3://cellxgene-census-public-us-west-2/cell-census/2025-11-17/soma/"
DATASET_ID = "218acb0f-9f2f-4f76-b90b-15a4b7c7f629"
DATASET_VERSION = "4118e166-34f5-4c1f-9eed-c64b90a3dace"
OUT = ROOT / "results_v3" / "sle_census_targeted"

DISEASE_LABEL = "systemic lupus erythematosus"
CONTROL_LABEL = "normal"
CELL_TYPES = (
    "classical monocyte",
    "non-classical monocyte",
    "conventional dendritic cell",
    "plasmacytoid dendritic cell",
)
MAX_CELLS_PER_DONOR_CELLTYPE = int(os.environ.get("SLE_MAX_CELLS_PER_DONOR_CELLTYPE", "40"))
MAX_TOTAL_CELLS = int(os.environ.get("SLE_MAX_TOTAL_CELLS", "20000"))


def quoted(values: list[str] | tuple[str, ...]) -> str:
    return "[" + ", ".join(repr(v) for v in values) + "]"


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


def normalize_log(adata) -> np.ndarray:
    x = adata.X
    raw_sum = adata.obs["raw_sum"].to_numpy(dtype=float)
    raw_sum[~np.isfinite(raw_sum) | (raw_sum <= 0)] = np.nan
    inv = np.divide(1.0, raw_sum, out=np.zeros_like(raw_sum), where=np.isfinite(raw_sum))
    if sparse.issparse(x):
        norm = x.tocsr().astype(float).multiply(inv[:, None]).multiply(1e4)
        return np.log1p(norm.toarray())
    arr = np.asarray(x, dtype=float)
    norm = arr * inv[:, None] * 1e4
    return np.log1p(norm)


def compare(donors: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for module, sub in donors.groupby("module", observed=True):
        for metric in ["mean_score", "high_fraction"]:
            case = sub.loc[sub["group"] == "case", metric].to_numpy(float)
            control = sub.loc[sub["group"] == "control", metric].to_numpy(float)
            if case.size >= 2 and control.size >= 2:
                t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            rows.append(
                {
                    "analysis": "sle_blood_myeloid_census_targeted",
                    "disease_name": DISEASE_LABEL,
                    "compartment": "blood myeloid/APC",
                    "module": module,
                    "metric": metric,
                    "n_case_donors": int(case.size),
                    "n_control_donors": int(control.size),
                    "mean_case": float(np.nanmean(case)) if case.size else np.nan,
                    "mean_control": float(np.nanmean(control)) if control.size else np.nan,
                    "delta_case_minus_control": float(np.nanmean(case) - np.nanmean(control)) if case.size and control.size else np.nan,
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

    with cellxgene_census.open_soma(uri=CENSUS_URI) as census:
        obs = census["census_data"]["homo_sapiens"].obs
        var = census["census_data"]["homo_sapiens"].ms["RNA"].var
        cell_filter = " or ".join(f"cell_type == {ct!r}" for ct in CELL_TYPES)
        obs_filter = (
            f"dataset_id == {DATASET_ID!r} and "
            f"(disease == {DISEASE_LABEL!r} or disease == {CONTROL_LABEL!r}) and "
            f"({cell_filter}) and is_primary_data == True"
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
            raise RuntimeError("No SLE Census cells matched the selected compartment")
        sampled = (
            obs_df.groupby(["disease", "donor_id", "cell_type"], group_keys=False, observed=True)
            .apply(
                lambda sub: sub.sample(
                    n=min(len(sub), MAX_CELLS_PER_DONOR_CELLTYPE),
                    random_state=SEED,
                )
            )
            .reset_index(drop=True)
        )
        if len(sampled) > MAX_TOTAL_CELLS:
            sampled = sampled.sample(n=MAX_TOTAL_CELLS, random_state=SEED).reset_index(drop=True)
        var_df = var.read(
            value_filter="feature_name in " + quoted(TARGET_GENES),
            column_names=["soma_joinid", "feature_name", "feature_id"],
        ).concat().to_pandas()
        if var_df.empty:
            raise RuntimeError("No target genes found in Census var table")
        adata = cellxgene_census.get_anndata(
            census,
            organism="homo_sapiens",
            measurement_name="RNA",
            X_name="raw",
            obs_coords=sampled["soma_joinid"].to_numpy(),
            var_coords=var_df["soma_joinid"].to_numpy(),
            obs_column_names=["dataset_id", "disease", "donor_id", "cell_type", "tissue", "raw_sum"],
            var_column_names=["feature_name", "feature_id"],
        )

    log_expr = normalize_log(adata)
    obs_out = adata.obs.reset_index(drop=True).copy()
    genes = adata.var["feature_name"].astype(str).tolist()
    gene_to_idx = {gene: i for i, gene in enumerate(genes)}
    normal_mask = obs_out["disease"].eq(CONTROL_LABEL).to_numpy()
    gene_mean = np.nanmean(log_expr[normal_mask], axis=0)
    gene_sd = np.nanstd(log_expr[normal_mask], axis=0, ddof=1)
    gene_sd[~np.isfinite(gene_sd) | (gene_sd < 1e-6)] = 1.0
    z = (log_expr - gene_mean) / gene_sd

    cell_scores = obs_out[["dataset_id", "disease", "donor_id", "cell_type", "tissue"]].copy()
    module_gene_rows = []
    for module, module_genes in MODULES.items():
        present = [gene for gene in module_genes if gene in gene_to_idx]
        module_gene_rows.append(
            {
                "analysis": "sle_blood_myeloid_census_targeted",
                "module": module,
                "n_genes_present": len(present),
                "genes_present": ",".join(present),
            }
        )
        if present:
            scores = np.nanmean(z[:, [gene_to_idx[g] for g in present]], axis=1)
        else:
            scores = np.full(z.shape[0], np.nan)
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
                    "analysis": "sle_blood_myeloid_census_targeted",
                    "dataset_id": DATASET_ID,
                    "dataset_version_id": DATASET_VERSION,
                    "disease_name": DISEASE_LABEL,
                    "compartment": "blood myeloid/APC",
                    "donor_id": donor,
                    "disease": disease,
                    "group": "case" if disease == DISEASE_LABEL else "control",
                    "module": module,
                    "n_cells": int(len(sub)),
                    "mean_score": float(np.nanmean(sub[module])),
                    "high_fraction": float(sub[f"{module}_high"].mean()),
                    "cell_types": ",".join(sorted(sub["cell_type"].astype(str).unique())),
                }
            )
    donors = pd.DataFrame(donor_rows)
    comparisons = compare(donors)
    sampled.to_csv(OUT / "sle_census_sampled_obs.tsv.gz", sep="\t", index=False, compression="gzip")
    pd.DataFrame(module_gene_rows).to_csv(OUT / "sle_census_module_genes_present.tsv", sep="\t", index=False)
    donors.to_csv(OUT / "sle_census_donor_module_scores.tsv", sep="\t", index=False)
    comparisons.to_csv(OUT / "sle_census_donor_module_comparisons.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "census_uri": CENSUS_URI,
        "dataset_id": DATASET_ID,
        "dataset_version_id": DATASET_VERSION,
        "n_cells_matching_filter": int(len(obs_df)),
        "n_cells_sampled": int(len(sampled)),
        "n_donors_case": int(donors.loc[donors["group"] == "case", "donor_id"].nunique()),
        "n_donors_control": int(donors.loc[donors["group"] == "control", "donor_id"].nunique()),
        "cell_types": list(CELL_TYPES),
        "top_positive_results": (
            comparisons[comparisons["delta_case_minus_control"] > 0]
            .sort_values(["fdr", "hedges_g"], ascending=[True, False])
            .head(30)
            .to_dict(orient="records")
        ),
        "guardrail": (
            "Targeted Census extraction of selected genes only; donor-level SLE PBMC "
            "recurrence evidence, not full atlas reanalysis or causal perturbation."
        ),
    }
    (OUT / "sle_census_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
