#!/usr/bin/env python3
"""Wave102 residual/controller test for SEL1L3 versus FXYD5.

Wave101 left SEL1L3 and FXYD5 as parked accessible survivors but the mechanism
sidecar warned that both could be surface/tissue-state markers. This script
tests the stronger question:

1. Does candidate expression retain a disease residual after adjustment for
   lipid-lysosomal, lysosomal, IFN/APC, NF-kB, HIF/NAMPT, and C15/MOCCI-like
   inflammatory state modules?
2. In datasets with paired tissue-resident and myeloid/APC compartments, does
   tissue-resident candidate expression predict same-donor myeloid
   lipid-lysosomal state?

This is still observational. A positive result can only reopen a perturbation
branch; it cannot establish causality.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import sparse, stats
from statsmodels.stats.multitest import multipletests

try:
    import statsmodels.api as sm
except Exception:  # pragma: no cover - statsmodels is expected in V3 env.
    sm = None

from v3_analyze_osmr_complement_axes import CONFIGS, ROOT, hedges_g, read_counts
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave102_sel1l3_fxyd5_residual_controller_test"

CANDIDATES = ["SEL1L3", "FXYD5", "APOC1", "CD82", "LAPTM5"]

MODULES = {
    "lipid_loader_repair": ["ACSL1", "APOE", "GPNMB", "LPL", "PLIN2", "CD36", "LIPA", "FABP5", "TREM2", "MSR1", "MERTK", "SPP1"],
    "lysosomal_apc": ["IFI30", "CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"],
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "CD74", "IFI30", "HLA-DRA", "HLA-DRB1"],
    "hla_ii_apc": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "CIITA", "RFX5"],
    "inflammatory_nfkb": ["IL1B", "TNF", "CXCL8", "CCL2", "CCL3", "CCL4", "NFKBIA", "TREM1", "OSM"],
    "hif_nampt_metabolic": ["HIF1A", "NAMPT", "LDHA", "SLC2A1", "NFKBIA", "IL1B", "HK2", "PFKFB3"],
    "c15_mocci_costate": ["C15ORF48", "NDUFA4", "LITAF", "CASP4", "TNF", "IL1B"],
    "tissue_barrier_adhesion": ["CDH1", "EPCAM", "KRT8", "KRT18", "VIM", "FN1", "COL1A1", "COL1A2"],
}

ADJUST_MODULES = [
    "lipid_loader_repair",
    "lysosomal_apc",
    "ifn_apc",
    "inflammatory_nfkb",
    "hif_nampt_metabolic",
    "c15_mocci_costate",
]

MYELOID_LINK_MODULES = ["lipid_loader_repair", "lysosomal_apc", "c15_mocci_costate", "inflammatory_nfkb"]

MS_SIG = ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv"
W101 = ROOT / "phases/v3/results" / "wave101_accessible_survivor_forcing_triage" / "accessible_survivor_forcing_rank.tsv"

MIN_DONOR_CELLS = 10


def clean_symbol(value: object) -> str:
    return str(value).strip().upper()


def compare_values(values: pd.Series | np.ndarray, groups: pd.Series | np.ndarray) -> dict[str, float]:
    values = pd.Series(values, dtype=float)
    groups = pd.Series(groups).astype(str)
    case = values.loc[groups.eq("case")].dropna().to_numpy(float)
    control = values.loc[groups.eq("control")].dropna().to_numpy(float)
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


def gene_indices(a: Any, symbol_column: str, wanted: set[str]) -> dict[str, int]:
    if symbol_column in a.var.columns:
        symbols = a.var[symbol_column].astype(str)
    elif "feature_name" in a.var.columns:
        symbols = a.var["feature_name"].astype(str)
    elif "gene_symbols" in a.var.columns:
        symbols = a.var["gene_symbols"].astype(str)
    else:
        symbols = pd.Series(a.var_names.astype(str), index=a.var.index)
    mapping: dict[str, int] = {}
    for idx, raw_symbol in enumerate(symbols):
        symbol = clean_symbol(raw_symbol)
        if symbol in wanted and symbol not in mapping:
            mapping[symbol] = idx
    return mapping


def analyze_config(config: Any, a: Any, x: sparse.csr_matrix) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    wanted = set(CANDIDATES)
    for genes in MODULES.values():
        wanted.update(map(str.upper, genes))

    obs = a.obs.copy()
    mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
    obs_sub = obs.loc[mask].copy()
    cell_idx = np.flatnonzero(mask.to_numpy())
    idx_map = gene_indices(a, config.gene_symbol_column, wanted)
    present_genes = sorted(idx_map)
    if obs_sub.empty or not present_genes:
        raise ValueError(f"no cells or target genes for {config.name}")

    target_x = x[cell_idx][:, [idx_map[g] for g in present_genes]].astype(float)
    lib_size = np.asarray(x[cell_idx].sum(axis=1)).ravel().astype(float)
    lib_size[~np.isfinite(lib_size) | (lib_size <= 0)] = np.nan
    normalizer = np.divide(1.0, lib_size, out=np.zeros_like(lib_size), where=np.isfinite(lib_size))
    normalized = target_x.multiply(normalizer[:, None]).multiply(1e4)
    log_expr = np.log1p(normalized.toarray())

    normal_mask = obs_sub["disease"].eq(config.control_label).to_numpy()
    gene_mean = np.nanmean(log_expr[normal_mask], axis=0)
    gene_sd = np.nanstd(log_expr[normal_mask], axis=0, ddof=1)
    gene_sd[~np.isfinite(gene_sd) | (gene_sd < 1e-6)] = 1.0
    z_expr = (log_expr - gene_mean) / gene_sd
    gene_to_local = {gene: i for i, gene in enumerate(present_genes)}

    cell_frame = obs_sub[["donor_id", "disease", "cell_type", "tissue"]].reset_index(drop=True).copy()
    module_gene_rows: list[dict[str, object]] = []
    for module, genes in MODULES.items():
        present = [gene for gene in map(str.upper, genes) if gene in gene_to_local]
        module_gene_rows.append(
            {
                "analysis": config.name,
                "disease_name": config.disease_label,
                "compartment": config.compartment,
                "role": config.role,
                "module": module,
                "n_genes_present": len(present),
                "genes_present": ",".join(present),
            }
        )
        idxs = [gene_to_local[g] for g in present]
        if idxs:
            cell_frame[module] = np.nanmean(z_expr[:, idxs], axis=1)
        else:
            cell_frame[module] = np.nan

    gene_rows: list[dict[str, object]] = []
    module_rows: list[dict[str, object]] = []
    for (donor_id, disease), sub_idx in cell_frame.groupby(["donor_id", "disease"], observed=True).groups.items():
        idx = np.fromiter(sub_idx, dtype=int)
        if len(idx) < MIN_DONOR_CELLS:
            continue
        group = "case" if disease == config.disease_label else "control"
        base = {
            "analysis": config.name,
            "dataset_path": str(config.path.relative_to(ROOT)),
            "disease_name": config.disease_label,
            "compartment": config.compartment,
            "role": config.role,
            "donor_id": str(donor_id),
            "disease": str(disease),
            "group": group,
            "n_cells": int(len(idx)),
            "cell_types": ",".join(sorted(cell_frame.iloc[idx]["cell_type"].astype(str).unique())),
        }
        for module in MODULES:
            module_rows.append(
                {
                    **base,
                    "module": module,
                    "mean_score": float(np.nanmean(cell_frame.iloc[idx][module])),
                }
            )
        for gene in CANDIDATES:
            if gene not in gene_to_local:
                continue
            j = gene_to_local[gene]
            vals = log_expr[idx, j]
            zvals = z_expr[idx, j]
            gene_rows.append(
                {
                    **base,
                    "gene": gene,
                    "mean_log_norm": float(np.nanmean(vals)),
                    "mean_z_vs_controls": float(np.nanmean(zvals)),
                    "detection_fraction": float((vals > 0).mean()),
                }
            )
    return pd.DataFrame(gene_rows), pd.DataFrame(module_rows), pd.DataFrame(module_gene_rows)


def raw_gene_contrasts(gene_scores: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (analysis, gene), sub in gene_scores.groupby(["analysis", "gene"], observed=True):
        first = sub.iloc[0]
        stats_row = compare_values(sub["mean_z_vs_controls"], sub["group"])
        rows.append(
            {
                "analysis": analysis,
                "disease_name": first["disease_name"],
                "compartment": first["compartment"],
                "role": first["role"],
                "gene": gene,
                "metric": "mean_z_vs_controls",
                **stats_row,
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
        out["positive_trend"] = (out["delta_case_minus_control"] > 0.30) & (out["p"] < 0.10)
        out["negative_trend"] = (out["delta_case_minus_control"] < -0.30) & (out["p"] < 0.10)
    return out.sort_values(["gene", "p"], na_position="last") if not out.empty else out


def wide_scores(gene_scores: pd.DataFrame, module_scores: pd.DataFrame) -> pd.DataFrame:
    genes = gene_scores.pivot_table(
        index=["analysis", "dataset_path", "disease_name", "compartment", "role", "donor_id", "group"],
        columns="gene",
        values="mean_z_vs_controls",
        aggfunc="mean",
    ).reset_index()
    modules = module_scores.pivot_table(
        index=["analysis", "donor_id"],
        columns="module",
        values="mean_score",
        aggfunc="mean",
    ).reset_index()
    return genes.merge(modules, on=["analysis", "donor_id"], how="left")


def zscore_series(values: pd.Series) -> pd.Series:
    values = pd.to_numeric(values, errors="coerce")
    sd = float(values.std(ddof=1))
    if not math.isfinite(sd) or sd < 1e-8:
        return pd.Series(np.nan, index=values.index)
    return (values - float(values.mean())) / sd


def residualize_on_composite(sub: pd.DataFrame, gene: str) -> dict[str, object]:
    covs = [m for m in ADJUST_MODULES if m in sub.columns and sub[m].notna().sum() >= 4 and sub[m].std(ddof=1) > 1e-8]
    out_base = {
        "residual_method": "composite_adjustment",
        "covariate_modules": ";".join(covs),
        "n_covariates": int(len(covs)),
    }
    if gene not in sub.columns or len(covs) < 2:
        return {**out_base, "residual_note": "missing_gene_or_too_few_covariates"}
    df = sub[["group", gene, *covs]].copy()
    for col in covs:
        df[col] = zscore_series(df[col])
    df["composite_state"] = df[covs].mean(axis=1)
    valid = df[[gene, "composite_state"]].notna().all(axis=1)
    if valid.sum() < 6 or df.loc[valid, "composite_state"].std(ddof=1) <= 1e-8:
        return {**out_base, "residual_note": "too_few_valid_samples"}
    slope, intercept, r_value, _, _ = stats.linregress(
        df.loc[valid, "composite_state"].to_numpy(float),
        df.loc[valid, gene].to_numpy(float),
    )
    residuals = pd.Series(np.nan, index=df.index, dtype=float)
    residuals.loc[valid] = df.loc[valid, gene] - (intercept + slope * df.loc[valid, "composite_state"])
    raw = compare_values(df[gene], df["group"])
    residual = compare_values(residuals, df["group"])
    return {
        **out_base,
        "residual_note": "ok",
        "composite_slope": float(slope),
        "composite_r2": float(r_value**2),
        **{f"raw_{k}": v for k, v in raw.items()},
        **{f"residual_{k}": v for k, v in residual.items()},
    }


def residualize_full_ols(sub: pd.DataFrame, gene: str) -> dict[str, object]:
    covs = [m for m in ADJUST_MODULES if m in sub.columns and sub[m].notna().sum() >= 4 and sub[m].std(ddof=1) > 1e-8]
    out_base = {
        "ols_covariate_modules": ";".join(covs),
        "ols_n_covariates": int(len(covs)),
    }
    if sm is None:
        return {**out_base, "ols_note": "statsmodels_unavailable"}
    if gene not in sub.columns or len(covs) < 2:
        return {**out_base, "ols_note": "missing_gene_or_too_few_covariates"}
    df = sub[["group", gene, *covs]].copy()
    df["disease_case"] = df["group"].eq("case").astype(float)
    for col in covs:
        df[col] = zscore_series(df[col])
    valid_cols = [gene, "disease_case", *covs]
    valid = df[valid_cols].notna().all(axis=1)
    n_params = 2 + len(covs)
    if valid.sum() < n_params + 3:
        return {**out_base, "ols_note": "too_few_valid_samples_for_full_ols", "ols_n_valid": int(valid.sum())}
    design = sm.add_constant(df.loc[valid, ["disease_case", *covs]], has_constant="add")
    try:
        fit = sm.OLS(df.loc[valid, gene], design).fit(cov_type="HC3")
    except Exception as exc:
        return {**out_base, "ols_note": f"failed:{type(exc).__name__}:{exc}", "ols_n_valid": int(valid.sum())}
    return {
        **out_base,
        "ols_note": "HC3 robust SE; covariates disease plus state modules",
        "ols_n_valid": int(valid.sum()),
        "ols_beta_disease_case": float(fit.params.get("disease_case", np.nan)),
        "ols_p_disease_case": float(fit.pvalues.get("disease_case", np.nan)),
        "ols_r2": float(fit.rsquared) if math.isfinite(float(fit.rsquared)) else np.nan,
    }


def residual_tests(gene_scores: pd.DataFrame, module_scores: pd.DataFrame) -> pd.DataFrame:
    wide = wide_scores(gene_scores, module_scores)
    rows: list[dict[str, object]] = []
    for (analysis, gene), sub_gene in gene_scores.groupby(["analysis", "gene"], observed=True):
        sub = wide.loc[wide["analysis"].eq(analysis)].copy()
        if gene not in sub.columns:
            continue
        first = sub.iloc[0]
        composite = residualize_on_composite(sub, gene)
        ols = residualize_full_ols(sub, gene)
        rows.append(
            {
                "analysis": analysis,
                "disease_name": first["disease_name"],
                "compartment": first["compartment"],
                "role": first["role"],
                "gene": gene,
                **composite,
                **ols,
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["residual_fdr"] = multipletests(out["residual_p"].fillna(1.0), method="fdr_bh")[1]
        out["ols_fdr"] = multipletests(out["ols_p_disease_case"].fillna(1.0), method="fdr_bh")[1] if "ols_p_disease_case" in out else 1.0
        out["retains_positive_residual_trend"] = (
            (out["raw_delta_case_minus_control"] > 0.30)
            & (out["raw_p"] < 0.10)
            & (out["residual_delta_case_minus_control"] > 0.20)
            & (out["residual_p"] < 0.10)
        )
        out["residual_negative_trend"] = (out["residual_delta_case_minus_control"] < -0.20) & (out["residual_p"] < 0.10)
    return out.sort_values(["gene", "residual_p"], na_position="last") if not out.empty else out


def same_donor_tissue_myeloid_links(gene_scores: pd.DataFrame, module_scores: pd.DataFrame) -> pd.DataFrame:
    module_wide = module_scores.pivot_table(
        index=["analysis", "dataset_path", "disease_name", "role", "donor_id", "group"],
        columns="module",
        values="mean_score",
        aggfunc="mean",
    ).reset_index()
    gene_tissue = gene_scores.loc[gene_scores["role"].ne("myeloid_apc")].copy()
    myeloid = module_wide.loc[module_wide["role"].eq("myeloid_apc")].copy()
    rows: list[dict[str, object]] = []
    if gene_tissue.empty or myeloid.empty:
        return pd.DataFrame()
    for (analysis, gene), gsub in gene_tissue.groupby(["analysis", "gene"], observed=True):
        first = gsub.iloc[0]
        matching_myeloid = myeloid.loc[
            myeloid["dataset_path"].eq(first["dataset_path"]) & myeloid["disease_name"].eq(first["disease_name"])
        ].copy()
        if matching_myeloid.empty:
            continue
        gcols = [
            "dataset_path",
            "disease_name",
            "donor_id",
            "group",
            "mean_z_vs_controls",
            "compartment",
        ]
        merged = gsub[gcols].merge(
            matching_myeloid[["donor_id", "group", "analysis", *[m for m in MYELOID_LINK_MODULES if m in matching_myeloid.columns]]],
            on=["donor_id", "group"],
            how="inner",
            suffixes=("_tissue", "_myeloid"),
        )
        for module in MYELOID_LINK_MODULES:
            if module not in merged.columns:
                continue
            valid = merged[["mean_z_vs_controls", module]].dropna()
            if len(valid) >= 5 and valid["mean_z_vs_controls"].std(ddof=1) > 1e-8 and valid[module].std(ddof=1) > 1e-8:
                rho, p_value = stats.spearmanr(valid["mean_z_vs_controls"], valid[module])
            else:
                rho, p_value = np.nan, np.nan
            case_valid = merged.loc[merged["group"].eq("case"), ["mean_z_vs_controls", module]].dropna()
            if len(case_valid) >= 4 and case_valid["mean_z_vs_controls"].std(ddof=1) > 1e-8 and case_valid[module].std(ddof=1) > 1e-8:
                case_rho, case_p = stats.spearmanr(case_valid["mean_z_vs_controls"], case_valid[module])
            else:
                case_rho, case_p = np.nan, np.nan
            rows.append(
                {
                    "tissue_analysis": analysis,
                    "myeloid_analysis": matching_myeloid["analysis"].iloc[0],
                    "disease_name": first["disease_name"],
                    "tissue_compartment": first["compartment"],
                    "gene": gene,
                    "myeloid_module": module,
                    "n_paired_donors": int(len(valid)),
                    "spearman_rho_all": float(rho) if pd.notna(rho) else np.nan,
                    "spearman_p_all": float(p_value) if pd.notna(p_value) else np.nan,
                    "n_case_paired_donors": int(len(case_valid)),
                    "spearman_rho_case": float(case_rho) if pd.notna(case_rho) else np.nan,
                    "spearman_p_case": float(case_p) if pd.notna(case_p) else np.nan,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["all_link_positive_trend"] = (out["spearman_rho_all"] >= 0.40) & (out["spearman_p_all"] < 0.10)
        out["case_link_positive_trend"] = (out["spearman_rho_case"] >= 0.40) & (out["spearman_p_case"] < 0.10)
    return out.sort_values(["gene", "spearman_p_all"], na_position="last") if not out.empty else out


def read_ms_rows() -> pd.DataFrame:
    if not MS_SIG.exists():
        return pd.DataFrame()
    ms = pd.read_csv(MS_SIG, sep="\t")
    ms["gene"] = ms["gene"].astype(str).str.upper()
    return ms.loc[ms["gene"].isin(CANDIDATES)].copy()


def read_wave101_rows() -> pd.DataFrame:
    if not W101.exists():
        return pd.DataFrame()
    w101 = pd.read_csv(W101, sep="\t", low_memory=False)
    w101["gene"] = w101["gene"].astype(str).str.upper()
    return w101.loc[w101["gene"].isin(CANDIDATES)].copy()


def safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
        return out if math.isfinite(out) else default
    except (TypeError, ValueError):
        return default


def integrated_summary(raw: pd.DataFrame, residuals: pd.DataFrame, links: pd.DataFrame, ms: pd.DataFrame, w101: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for gene in CANDIDATES:
        rsub = raw.loc[raw["gene"].eq(gene)] if not raw.empty else pd.DataFrame()
        resub = residuals.loc[residuals["gene"].eq(gene)] if not residuals.empty else pd.DataFrame()
        lsub = links.loc[links["gene"].eq(gene)] if not links.empty else pd.DataFrame()
        mrow = ms.loc[ms["gene"].eq(gene)].iloc[0] if not ms.empty and ms["gene"].eq(gene).any() else None
        wrow = w101.loc[w101["gene"].eq(gene)].iloc[0] if not w101.empty and w101["gene"].eq(gene).any() else None

        raw_pos = rsub.loc[rsub.get("positive_trend", False).astype(bool)] if not rsub.empty else pd.DataFrame()
        raw_neg = rsub.loc[rsub.get("negative_trend", False).astype(bool)] if not rsub.empty else pd.DataFrame()
        retained = resub.loc[resub.get("retains_positive_residual_trend", False).astype(bool)] if not resub.empty else pd.DataFrame()
        residual_neg = resub.loc[resub.get("residual_negative_trend", False).astype(bool)] if not resub.empty else pd.DataFrame()
        link_pos = lsub.loc[(lsub.get("all_link_positive_trend", False).astype(bool)) | (lsub.get("case_link_positive_trend", False).astype(bool))] if not lsub.empty else pd.DataFrame()

        retained_diseases = sorted(map(str, retained["disease_name"].dropna().unique())) if not retained.empty else []
        link_diseases = sorted(map(str, link_pos["disease_name"].dropna().unique())) if not link_pos.empty else []
        blocker_notes = []
        if retained["disease_name"].nunique() < 2:
            blocker_notes.append("residual_retained_diseases_lt2")
        if link_pos["disease_name"].nunique() < 1:
            blocker_notes.append("no_same_donor_tissue_to_myeloid_link")
        if not residual_neg.empty:
            blocker_notes.append("residual_negative_context_present")
        if wrow is not None and "wave101_missing_gates" in wrow and str(wrow["wave101_missing_gates"]):
            blocker_notes.append(f"wave101_missing:{wrow['wave101_missing_gates']}")

        if gene == "SEL1L3" and retained["disease_name"].nunique() >= 2 and link_pos["disease_name"].nunique() >= 1 and residual_neg.empty:
            call = "REOPEN_FOR_TARGET_SPECIFIC_PERTURBATION"
        elif retained["disease_name"].nunique() >= 2 and link_pos["disease_name"].nunique() >= 1 and residual_neg.empty:
            call = "PARK_RESIDUAL_SUPPORT_BUT_NOT_PROMOTABLE"
        else:
            call = "NO_GO_RESIDUAL_CONTROLLER_NOT_PROVEN"

        rows.append(
            {
                "gene": gene,
                "integrated_call": call,
                "blocker_notes": ";".join(blocker_notes),
                "wave101_call": str(wrow["wave101_call"]) if wrow is not None and "wave101_call" in wrow else "",
                "wave101_score": safe_float(wrow["wave101_score"]) if wrow is not None and "wave101_score" in wrow else np.nan,
                "ms_delta_log2": safe_float(mrow["delta_log2"]) if mrow is not None and "delta_log2" in mrow else np.nan,
                "ms_p": safe_float(mrow["p"]) if mrow is not None and "p" in mrow else np.nan,
                "raw_positive_context_count": int(len(raw_pos)),
                "raw_positive_disease_count": int(raw_pos["disease_name"].nunique()) if not raw_pos.empty else 0,
                "raw_negative_context_count": int(len(raw_neg)),
                "raw_negative_disease_count": int(raw_neg["disease_name"].nunique()) if not raw_neg.empty else 0,
                "residual_retained_context_count": int(len(retained)),
                "residual_retained_disease_count": int(retained["disease_name"].nunique()) if not retained.empty else 0,
                "residual_retained_diseases": ";".join(retained_diseases),
                "residual_negative_context_count": int(len(residual_neg)),
                "same_donor_positive_link_count": int(len(link_pos)),
                "same_donor_positive_link_disease_count": int(link_pos["disease_name"].nunique()) if not link_pos.empty else 0,
                "same_donor_positive_link_diseases": ";".join(link_diseases),
                "best_residual_context": (
                    retained.sort_values(["residual_delta_case_minus_control", "residual_p"], ascending=[False, True])
                    .head(1)
                    .apply(
                        lambda r: f"{r['analysis']}|{r['disease_name']}|{r['compartment']}|delta={r['residual_delta_case_minus_control']:.3g}|p={r['residual_p']:.3g}",
                        axis=1,
                    )
                    .iloc[0]
                    if not retained.empty
                    else ""
                ),
                "best_same_donor_link": (
                    link_pos.sort_values(["spearman_p_all", "spearman_p_case"], na_position="last")
                    .head(1)
                    .apply(
                        lambda r: f"{r['tissue_analysis']}->{r['myeloid_analysis']}|{r['myeloid_module']}|rho_all={r['spearman_rho_all']:.3g}|p_all={r['spearman_p_all']:.3g}|rho_case={r['spearman_rho_case']:.3g}|p_case={r['spearman_p_case']:.3g}",
                        axis=1,
                    )
                    .iloc[0]
                    if not link_pos.empty
                    else ""
                ),
            }
        )
    out = pd.DataFrame(rows)
    return out.sort_values(
        ["integrated_call", "residual_retained_disease_count", "same_donor_positive_link_disease_count", "wave101_score"],
        ascending=[True, False, False, False],
    )


def write_report(summary: pd.DataFrame, raw: pd.DataFrame, residuals: pd.DataFrame, links: pd.DataFrame, run_log: list[dict[str, object]]) -> None:
    promoted = summary.loc[summary["integrated_call"].eq("REOPEN_FOR_TARGET_SPECIFIC_PERTURBATION")]
    branch_call = "REOPEN_SEL1L3_FOR_WETLAB_PERTURBATION" if not promoted.empty else "NO_REOPEN_ACCESSIBLE_SURVIVOR_AFTER_RESIDUAL_TEST"
    top = summary.head(5)
    retained = residuals.loc[residuals.get("retains_positive_residual_trend", pd.Series(False, index=residuals.index)).astype(bool)] if not residuals.empty else pd.DataFrame()
    positive_links = links.loc[(links.get("all_link_positive_trend", pd.Series(False, index=links.index)).astype(bool)) | (links.get("case_link_positive_trend", pd.Series(False, index=links.index)).astype(bool))] if not links.empty else pd.DataFrame()
    failed_runs = [r for r in run_log if r.get("status") != "completed"]

    lines = [
        "# Wave102 SEL1L3/FXYD5 Residual Controller Test",
        "",
        "## Bottom Line",
        "",
        f"Branch call: `{branch_call}`.",
        "",
    ]
    if branch_call.startswith("REOPEN"):
        lines.extend(
            [
                "At least one accessible survivor retained disease residual support after",
                "state-module adjustment and had same-donor tissue-to-myeloid linkage.",
                "This is not a therapeutic claim; it only justifies target-specific",
                "perturbation follow-up.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "`SEL1L3` and `FXYD5` do not clear the residual/controller bar. Their",
                "accessible disease signals remain insufficiently separated from",
                "generic lipid-lysosomal, lysosomal, IFN/APC, NF-kB, HIF/NAMPT, and",
                "C15/MOCCI-like tissue state variation.",
                "",
            ]
        )

    lines.extend(
        [
            "## Integrated Candidate Summary",
            "",
            markdown_table(
                top[
                    [
                        "gene",
                        "integrated_call",
                        "wave101_score",
                        "ms_delta_log2",
                        "ms_p",
                        "raw_positive_disease_count",
                        "residual_retained_disease_count",
                        "same_donor_positive_link_disease_count",
                        "blocker_notes",
                        "best_residual_context",
                        "best_same_donor_link",
                    ]
                ],
                max_rows=10,
            ),
            "",
            "## Retained Residual Contexts",
            "",
            markdown_table(
                retained[
                    [
                        "gene",
                        "analysis",
                        "disease_name",
                        "compartment",
                        "role",
                        "raw_delta_case_minus_control",
                        "raw_p",
                        "residual_delta_case_minus_control",
                        "residual_p",
                        "covariate_modules",
                    ]
                ].sort_values(["gene", "residual_p"], na_position="last")
                if not retained.empty
                else pd.DataFrame(),
                max_rows=30,
            ),
            "",
            "## Same-Donor Tissue-to-Myeloid Links",
            "",
            markdown_table(
                positive_links[
                    [
                        "gene",
                        "tissue_analysis",
                        "myeloid_analysis",
                        "disease_name",
                        "tissue_compartment",
                        "myeloid_module",
                        "n_paired_donors",
                        "spearman_rho_all",
                        "spearman_p_all",
                        "n_case_paired_donors",
                        "spearman_rho_case",
                        "spearman_p_case",
                    ]
                ].sort_values(["gene", "spearman_p_all"], na_position="last")
                if not positive_links.empty
                else pd.DataFrame(),
                max_rows=30,
            ),
            "",
            "## Interpretation",
            "",
            "- This test is stricter than Wave101 because it asks whether candidate",
            "  expression retains disease signal after state-module adjustment and",
            "  whether tissue candidate expression tracks same-donor myeloid state.",
            "- A retained residual is still observational; it does not prove that the",
            "  candidate controls the myeloid module.",
            "- A no-reopen call means the branch should not proceed without direct",
            "  perturbation data.",
            "",
            "## Run Log",
            "",
            markdown_table(pd.DataFrame(run_log), max_rows=40),
            "",
        ]
    )
    if failed_runs:
        lines.extend(
            [
                "Failed or skipped configs are listed above and should not be counted",
                "as negative biological evidence.",
                "",
            ]
        )
    lines.extend(
        [
            "## Reproducibility",
            "",
            "- Script: `scripts/v3_wave102_sel1l3_fxyd5_residual_controller_test.py`",
            "- Candidate gene scores: `phases/v3/results/wave102_sel1l3_fxyd5_residual_controller_test/candidate_gene_scores.tsv`",
            "- Module scores: `phases/v3/results/wave102_sel1l3_fxyd5_residual_controller_test/candidate_module_scores.tsv`",
            "- Residual tests: `phases/v3/results/wave102_sel1l3_fxyd5_residual_controller_test/candidate_multicovariate_residual_tests.tsv`",
            "- Same-donor links: `phases/v3/results/wave102_sel1l3_fxyd5_residual_controller_test/same_donor_tissue_to_myeloid_links.tsv`",
            f"- Seed: `{SEED}`",
            "",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    cache: dict[Path, tuple[Any, sparse.csr_matrix]] = {}
    gene_tables: list[pd.DataFrame] = []
    module_tables: list[pd.DataFrame] = []
    module_gene_tables: list[pd.DataFrame] = []
    run_log: list[dict[str, object]] = []

    for config in CONFIGS:
        try:
            if config.path not in cache:
                cache[config.path] = read_counts(config.path)
            a, x = cache[config.path]
            gene_scores, module_scores, module_genes = analyze_config(config, a, x)
            gene_tables.append(gene_scores)
            module_tables.append(module_scores)
            module_gene_tables.append(module_genes)
            run_log.append(
                {
                    "analysis": config.name,
                    "status": "completed",
                    "gene_rows": int(len(gene_scores)),
                    "module_rows": int(len(module_scores)),
                }
            )
        except Exception as exc:
            run_log.append({"analysis": config.name, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})

    gene_scores = pd.concat(gene_tables, ignore_index=True) if gene_tables else pd.DataFrame()
    module_scores = pd.concat(module_tables, ignore_index=True) if module_tables else pd.DataFrame()
    module_genes = pd.concat(module_gene_tables, ignore_index=True) if module_gene_tables else pd.DataFrame()

    raw = raw_gene_contrasts(gene_scores) if not gene_scores.empty else pd.DataFrame()
    residuals = residual_tests(gene_scores, module_scores) if not gene_scores.empty and not module_scores.empty else pd.DataFrame()
    links = same_donor_tissue_myeloid_links(gene_scores, module_scores) if not gene_scores.empty and not module_scores.empty else pd.DataFrame()
    ms = read_ms_rows()
    w101 = read_wave101_rows()
    summary = integrated_summary(raw, residuals, links, ms, w101)

    gene_scores.to_csv(OUT / "candidate_gene_scores.tsv", sep="\t", index=False)
    module_scores.to_csv(OUT / "candidate_module_scores.tsv", sep="\t", index=False)
    module_genes.to_csv(OUT / "candidate_module_gene_coverage.tsv", sep="\t", index=False)
    raw.to_csv(OUT / "candidate_raw_contrasts.tsv", sep="\t", index=False)
    residuals.to_csv(OUT / "candidate_multicovariate_residual_tests.tsv", sep="\t", index=False)
    links.to_csv(OUT / "same_donor_tissue_to_myeloid_links.tsv", sep="\t", index=False)
    summary.to_csv(OUT / "candidate_integrated_summary.tsv", sep="\t", index=False)

    branch_call = (
        "REOPEN_SEL1L3_FOR_WETLAB_PERTURBATION"
        if summary["integrated_call"].eq("REOPEN_FOR_TARGET_SPECIFIC_PERTURBATION").any()
        else "NO_REOPEN_ACCESSIBLE_SURVIVOR_AFTER_RESIDUAL_TEST"
    )
    summary_json = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "n_candidates": len(CANDIDATES),
        "candidate_calls": summary.set_index("gene")["integrated_call"].to_dict(),
        "completed_configs": int(sum(1 for row in run_log if row.get("status") == "completed")),
        "failed_configs": [row for row in run_log if row.get("status") != "completed"],
        "outputs": {
            "candidate_gene_scores": rel(OUT / "candidate_gene_scores.tsv"),
            "candidate_module_scores": rel(OUT / "candidate_module_scores.tsv"),
            "candidate_module_gene_coverage": rel(OUT / "candidate_module_gene_coverage.tsv"),
            "candidate_raw_contrasts": rel(OUT / "candidate_raw_contrasts.tsv"),
            "candidate_multicovariate_residual_tests": rel(OUT / "candidate_multicovariate_residual_tests.tsv"),
            "same_donor_tissue_to_myeloid_links": rel(OUT / "same_donor_tissue_to_myeloid_links.tsv"),
            "candidate_integrated_summary": rel(OUT / "candidate_integrated_summary.tsv"),
            "report": rel(OUT / "REPORT.md"),
        },
    }
    write_json(OUT / "summary.json", summary_json)
    write_report(summary, raw, residuals, links, run_log)
    print(json.dumps(summary_json, indent=2))


if __name__ == "__main__":
    main()
