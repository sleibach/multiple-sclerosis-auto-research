#!/usr/bin/env python3
"""GSE315138 celiac duodenum marker-compartment module analysis.

GSE315138 provides raw 10x matrices for active celiac disease and healthy
duodenal biopsies but no cell-level annotation table in the GEO supplement.
This script therefore uses a deliberately transparent marker classifier before
scoring the V3 autoimmune modules.

This is stronger than whole-biopsy pseudobulk but weaker than curated
single-cell annotation. Outputs are labeled as marker-compartment evidence.
"""

from __future__ import annotations

import gzip
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import io, sparse, stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import MODULES, ROOT

SEED = 20260526
RAW = ROOT / "data" / "raw_v3" / "gse315138" / "raw"
OUT = ROOT / "results_v3" / "gse315138_celiac_marker"

MARKER_SETS = {
    "epithelial_like": ["EPCAM", "KRT8", "KRT18", "KRT19", "VIL1", "APOA4", "ALPI", "FABP1", "MUC2"],
    "t_cell_like": ["CD3D", "CD3E", "CD3G", "TRAC", "CD4", "CD8A", "CD8B", "NKG7", "GZMA", "GZMB"],
    "myeloid_apc_like": ["LST1", "LYZ", "CD14", "FCGR3A", "ITGAX", "CST3", "HLA-DRA", "CD74", "FCER1A", "MS4A7"],
    "b_plasma_like": ["MS4A1", "CD79A", "CD79B", "CD74", "MZB1", "JCHAIN", "IGHG1", "IGHG4"],
    "stromal_endothelial_like": ["COL1A1", "COL1A2", "DCN", "LUM", "PECAM1", "VWF", "CLDN5", "ACTA2", "RGS5"],
}

TARGET_GENES = sorted({gene for genes in MODULES.values() for gene in genes})
MARKER_GENES = sorted({gene for genes in MARKER_SETS.values() for gene in genes})
ALL_GENES = sorted(set(TARGET_GENES) | set(MARKER_GENES))


@dataclass(frozen=True)
class SampleConfig:
    sample_id: str
    prefix: str
    donor_id: str
    disease: str
    group: str


SAMPLES = [
    SampleConfig("GSM9421934", "GSM9421934_2-PC004-h", "Healthy1", "normal", "control"),
    SampleConfig("GSM9421935", "GSM9421935_1-PC005-h", "Healthy2", "normal", "control"),
    SampleConfig("GSM9421936", "GSM9421936_3-PC006-c", "celiac1", "celiac disease", "case"),
    SampleConfig("GSM9421937", "GSM9421937_SI-TT-G4", "celiac2", "celiac disease", "case"),
    SampleConfig("GSM9421938", "GSE315138_Celiac-a2", "celiac_a2", "celiac disease", "case"),
    SampleConfig("GSM9421939", "GSE315138_Celiac304", "celiac304", "celiac disease", "case"),
]


def read_features(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", header=None, compression="gzip")
    if df.shape[1] < 2:
        raise ValueError(f"feature table has fewer than two columns: {path}")
    df = df.iloc[:, :2].copy()
    df.columns = ["gene_id", "gene_symbol"]
    df["row_index"] = np.arange(df.shape[0])
    return df


def selected_log_expression(config: SampleConfig) -> tuple[pd.DataFrame, np.ndarray, list[str]]:
    features_path = RAW / f"{config.prefix}_features.tsv.gz"
    matrix_path = RAW / f"{config.prefix}_matrix.mtx.gz"
    barcodes_path = RAW / f"{config.prefix}_barcodes.tsv.gz"
    missing = [p for p in [features_path, matrix_path, barcodes_path] if not p.exists() or p.stat().st_size == 0]
    if missing:
        raise FileNotFoundError("missing sample files: " + ", ".join(str(p) for p in missing))

    features = read_features(features_path)
    row_to_gene: dict[int, str] = {}
    for gene in ALL_GENES:
        hits = features.loc[features["gene_symbol"].eq(gene), "row_index"]
        if not hits.empty:
            row_to_gene[int(hits.iloc[0])] = gene
    selected_rows = sorted(row_to_gene)
    selected_genes = [row_to_gene[i] for i in selected_rows]
    with gzip.open(barcodes_path, "rt") as fh:
        barcodes = [line.strip() for line in fh if line.strip()]

    mat = io.mmread(matrix_path).tocsc().astype(float)
    if mat.shape[1] != len(barcodes):
        raise ValueError(f"barcode count mismatch for {config.sample_id}: {mat.shape[1]} vs {len(barcodes)}")
    library_size = np.asarray(mat.sum(axis=0)).ravel()
    library_size[~np.isfinite(library_size) | (library_size <= 0)] = np.nan
    selected = mat[selected_rows, :].T.tocsr()
    normalized = selected.multiply(np.divide(1.0, library_size, out=np.zeros_like(library_size), where=np.isfinite(library_size))[:, None]).multiply(1e4)
    log_expr = np.log1p(normalized.toarray()).astype(np.float32)
    obs = pd.DataFrame(
        {
            "sample_id": config.sample_id,
            "donor_id": config.donor_id,
            "disease": config.disease,
            "group": config.group,
            "barcode": barcodes,
            "n_counts": library_size,
        }
    )
    return obs, log_expr, selected_genes


def classify_compartments(obs: pd.DataFrame, log_expr: np.ndarray, genes: list[str]) -> pd.DataFrame:
    gene_to_idx = {gene: i for i, gene in enumerate(genes)}
    scores = {}
    for compartment, marker_genes in MARKER_SETS.items():
        present = [gene for gene in marker_genes if gene in gene_to_idx]
        if present:
            scores[compartment] = np.nanmean(log_expr[:, [gene_to_idx[g] for g in present]], axis=1)
        else:
            scores[compartment] = np.full(log_expr.shape[0], np.nan)
    score_df = pd.DataFrame(scores)
    values = score_df.to_numpy(float)
    order = np.argsort(np.nan_to_num(values, nan=-np.inf), axis=1)
    top_idx = order[:, -1]
    second_idx = order[:, -2]
    top_score = values[np.arange(values.shape[0]), top_idx]
    second_score = values[np.arange(values.shape[0]), second_idx]
    compartments = np.array(score_df.columns)[top_idx].astype(object)
    # Conservative ambiguity filter: keep high-signal cells and label the rest.
    ambiguous = (~np.isfinite(top_score)) | (top_score < 0.20) | ((top_score - second_score) < 0.05)
    compartments[ambiguous] = "ambiguous"
    out = obs.copy()
    for col in score_df:
        out[f"marker_{col}"] = score_df[col].to_numpy(float)
    out["marker_compartment"] = compartments
    out["marker_top_score"] = top_score
    out["marker_margin"] = top_score - second_score
    return out


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


def compare_donors(donors: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (compartment, module), sub in donors.groupby(["marker_compartment", "module"], observed=True):
        for metric in ["mean_score", "high_fraction"]:
            case = sub.loc[sub["group"].eq("case"), metric].to_numpy(float)
            control = sub.loc[sub["group"].eq("control"), metric].to_numpy(float)
            if case.size >= 2 and control.size >= 2:
                t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            rows.append(
                {
                    "analysis": "gse315138_celiac_marker",
                    "disease_name": "celiac disease",
                    "compartment": compartment,
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
    obs_tables = []
    expr_tables = []
    gene_sets = []
    run_log = []
    for config in SAMPLES:
        try:
            obs, log_expr, genes = selected_log_expression(config)
            obs = classify_compartments(obs, log_expr, genes)
            obs_tables.append(obs)
            expr_tables.append(pd.DataFrame(log_expr, columns=genes))
            gene_sets.append(set(genes))
            run_log.append({"sample_id": config.sample_id, "status": "completed", "n_cells": int(len(obs)), "n_genes_selected": int(len(genes))})
        except Exception as exc:
            run_log.append({"sample_id": config.sample_id, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})
    if not obs_tables:
        raise RuntimeError("No GSE315138 samples could be analyzed")

    obs_all = pd.concat(obs_tables, ignore_index=True)
    common_genes = sorted(set.intersection(*gene_sets))
    expr_all = pd.concat([df.reindex(columns=common_genes) for df in expr_tables], ignore_index=True).to_numpy(dtype=float)
    gene_to_idx = {gene: i for i, gene in enumerate(common_genes)}

    cell_module_rows = []
    module_gene_rows = []
    for compartment, comp_obs in obs_all.groupby("marker_compartment", observed=True):
        comp_idx = comp_obs.index.to_numpy()
        if compartment == "ambiguous":
            continue
        normal_mask = comp_obs["group"].eq("control").to_numpy()
        if normal_mask.sum() < 50:
            continue
        comp_expr = expr_all[comp_idx, :]
        mean = np.nanmean(comp_expr[normal_mask], axis=0)
        sd = np.nanstd(comp_expr[normal_mask], axis=0, ddof=1)
        sd[~np.isfinite(sd) | (sd < 1e-6)] = 1.0
        z = (comp_expr - mean) / sd
        for module, module_genes in MODULES.items():
            present = [gene for gene in module_genes if gene in gene_to_idx]
            module_gene_rows.append(
                {
                    "analysis": "gse315138_celiac_marker",
                    "marker_compartment": compartment,
                    "module": module,
                    "n_genes_present": len(present),
                    "genes_present": ",".join(present),
                }
            )
            if not present:
                continue
            vals = np.nanmean(z[:, [gene_to_idx[g] for g in present]], axis=1)
            threshold = np.nanpercentile(vals[normal_mask], 75) if np.isfinite(vals[normal_mask]).any() else np.nan
            tmp = comp_obs[["sample_id", "donor_id", "disease", "group", "marker_compartment"]].copy()
            tmp["module"] = module
            tmp["score"] = vals
            tmp["high"] = vals > threshold
            cell_module_rows.append(tmp)
    cell_modules = pd.concat(cell_module_rows, ignore_index=True) if cell_module_rows else pd.DataFrame()

    donor_rows = []
    if not cell_modules.empty:
        for (donor, group, disease, compartment, module), sub in cell_modules.groupby(
            ["donor_id", "group", "disease", "marker_compartment", "module"],
            observed=True,
        ):
            if len(sub) < 50:
                continue
            donor_rows.append(
                {
                    "analysis": "gse315138_celiac_marker",
                    "disease_name": "celiac disease",
                    "donor_id": donor,
                    "disease": disease,
                    "group": group,
                    "marker_compartment": compartment,
                    "module": module,
                    "n_cells": int(len(sub)),
                    "mean_score": float(np.nanmean(sub["score"])),
                    "high_fraction": float(np.nanmean(sub["high"])),
                }
            )
    donors = pd.DataFrame(donor_rows)
    comparisons = compare_donors(donors) if not donors.empty else pd.DataFrame()
    compartment_counts = (
        obs_all.groupby(["donor_id", "group", "disease", "marker_compartment"], observed=True)
        .size()
        .reset_index(name="n_cells")
    )

    compartment_counts.to_csv(OUT / "gse315138_compartment_counts.tsv", sep="\t", index=False)
    pd.DataFrame(module_gene_rows).to_csv(OUT / "gse315138_module_genes_present.tsv", sep="\t", index=False)
    donors.to_csv(OUT / "gse315138_donor_module_scores.tsv", sep="\t", index=False)
    comparisons.to_csv(OUT / "gse315138_donor_module_comparisons.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "run_log": run_log,
        "n_cells_total": int(len(obs_all)),
        "n_case_donors": int(obs_all.loc[obs_all["group"].eq("case"), "donor_id"].nunique()),
        "n_control_donors": int(obs_all.loc[obs_all["group"].eq("control"), "donor_id"].nunique()),
        "compartment_counts": compartment_counts.groupby("marker_compartment")["n_cells"].sum().to_dict(),
        "top_positive_results": (
            comparisons[comparisons["delta_case_minus_control"] > 0]
            .sort_values(["fdr", "hedges_g"], ascending=[True, False])
            .head(30)
            .to_dict(orient="records")
            if not comparisons.empty
            else []
        ),
        "guardrail": (
            "GSE315138 GEO supplement lacks curated cell annotations; compartments "
            "are canonical-marker approximations and should be treated as recurrence "
            "evidence only."
        ),
    }
    (OUT / "gse315138_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
