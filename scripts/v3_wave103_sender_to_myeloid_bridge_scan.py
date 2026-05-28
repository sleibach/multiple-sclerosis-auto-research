#!/usr/bin/env python3
"""Wave103 sender-to-myeloid bridge scan.

After the accessible-marker branch failed, Wave102 still showed a repeated
pattern: tissue-resident candidate expression can track same-donor myeloid
lipid/C15/inflammatory state. This script pivots from marker nomination to the
bridge question:

Which tissue-resident ligand/receptor/signaling genes most consistently track
same-donor myeloid lipid-lysosomal, lysosomal, C15/MOCCI-like, or inflammatory
modules across autoimmune tissues?

The output is a ranked bridge-scan table, not a therapeutic finding. A top hit
must still survive prior-art, perturbation, genetics, and selectivity gates.
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

from v3_analyze_osmr_complement_axes import CONFIGS, ROOT, hedges_g, read_counts
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "results_v3" / "wave103_sender_to_myeloid_bridge_scan"

W30 = ROOT / "results_v3" / "wave30_niche_driver_audit" / "niche_driver_axis_audit.tsv"
MYELOID_MODULE_SCORES = (
    ROOT / "results_v3" / "wave102_sel1l3_fxyd5_residual_controller_test" / "candidate_module_scores.tsv"
)

MYELOID_MODULES = ["lipid_loader_repair", "lysosomal_apc", "c15_mocci_costate", "inflammatory_nfkb"]

MANUAL_BRIDGE_GENES = {
    # Cytokine / JAK / inflammatory state drivers.
    "OSM", "LIF", "IL6", "IL1A", "IL1B", "IL18", "IL33", "TNF", "TNFSF10", "TNFSF13B", "TNFSF14",
    "CD40", "CD40LG", "CD70", "CD27", "CD274", "PDCD1LG2", "PDCD1", "IL10", "IL12A", "IL12B", "IL23A",
    "CSF1", "CSF2", "CSF3", "IL34", "IFNG", "IFNGR1", "IFNGR2", "JAK1", "JAK2", "STAT1", "IRF1",
    # Chemokine / recruitment / retention.
    "CCL2", "CCL3", "CCL4", "CCL5", "CCL7", "CCL8", "CCL13", "CCL20", "CCR2", "CCR5", "CCR6",
    "CXCL1", "CXCL2", "CXCL3", "CXCL8", "CXCL9", "CXCL10", "CXCL11", "CXCL12", "CXCL13", "CXCR3", "CXCR4",
    # Damage, alarmin, and metabolic mediators.
    "MIF", "DDT", "NAMPT", "HMGB1", "S100A8", "S100A9", "S100A12", "ANXA1", "FPR2", "PTGS2", "ALOX5",
    "PLA2G7", "TBXAS1", "HIF1A", "NFKBIA",
    # Growth, barrier, stromal, and matrix-remodeling mediators.
    "TGFB1", "TGFB2", "TGFB3", "AREG", "EREG", "HBEGF", "EGF", "VEGFA", "VEGFB", "ANGPT1", "ANGPT2",
    "SEMA4D", "SEMA7A", "ICAM1", "VCAM1", "MMP3", "MMP9", "MMP12", "MMP14", "TIMP1", "SERPINE1",
    # Lipid/efferocytosis/complement/lysosomal interface.
    "SPP1", "CD44", "ITGAV", "ITGB1", "ITGB2", "ITGB3", "ITGAM", "LGALS1", "LGALS3", "GAS6", "PROS1",
    "AXL", "MERTK", "TYRO3", "C1QA", "C1QB", "C1QC", "C1R", "C1S", "C2", "C3", "CFB", "CFD", "C3AR1",
    "C5AR1", "CALR", "LRP1", "MSR1", "MARCO", "CD36", "SCARB1", "SCARB2", "TREM2", "TYROBP",
    # Myeloid checkpoints and endolysosomal candidates from prior waves.
    "LILRB1", "LILRB2", "LILRB3", "LILRB4", "SIGLEC10", "CD24", "CD200", "CD200R1", "SLC15A4", "IRF5",
    "GPR65", "P2RX7", "PTGER4", "ADORA2A", "ADORA2B",
}

MIN_DONOR_CELLS = 10


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def clean_symbol(value: object) -> str:
    return str(value).strip().upper()


def safe_float(value: Any, default: float = np.nan) -> float:
    try:
        out = float(value)
        return out if math.isfinite(out) else default
    except (TypeError, ValueError):
        return default


def wave30_gene_map() -> tuple[set[str], pd.DataFrame]:
    w30 = read_tsv(W30)
    genes = set(MANUAL_BRIDGE_GENES)
    if w30.empty:
        return genes, pd.DataFrame()
    rows = []
    for _, row in w30.iterrows():
        axis_genes = [g.strip().upper() for g in str(row.get("genes", "")).split(";") if g.strip()]
        core_genes = [g.strip().upper() for g in str(row.get("core_intervention_genes", "")).split(";") if g.strip()]
        for gene in set(axis_genes + core_genes):
            genes.add(gene)
            rows.append(
                {
                    "gene": gene,
                    "wave30_axis": row.get("axis", ""),
                    "wave30_call": row.get("wave30_call", ""),
                    "wave30_centrality_score": safe_float(row.get("centrality_score")),
                    "wave30_intervention_score": safe_float(row.get("intervention_score")),
                    "wave30_gate_failures": row.get("gate_failures", ""),
                    "wave30_manual_prior_risk": row.get("manual_prior_risk", ""),
                    "wave30_manual_druggability": safe_float(row.get("manual_druggability")),
                    "wave30_manual_selectivity": safe_float(row.get("manual_selectivity")),
                }
            )
    gene_axis = pd.DataFrame(rows).drop_duplicates() if rows else pd.DataFrame()
    return genes, gene_axis


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


def donor_sender_scores(config: Any, a: Any, x: sparse.csr_matrix, wanted: set[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    obs = a.obs.copy()
    mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
    obs_sub = obs.loc[mask].copy()
    cell_idx = np.flatnonzero(mask.to_numpy())
    idx_map = gene_indices(a, config.gene_symbol_column, wanted)
    present_genes = sorted(idx_map)
    if obs_sub.empty or not present_genes:
        raise ValueError(f"no cells or bridge genes for {config.name}")

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
    rows = []
    for (donor_id, disease), sub_idx in cell_frame.groupby(["donor_id", "disease"], observed=True).groups.items():
        idx = np.fromiter(sub_idx, dtype=int)
        if len(idx) < MIN_DONOR_CELLS:
            continue
        base = {
            "analysis": config.name,
            "dataset_path": str(config.path.relative_to(ROOT)),
            "disease_name": config.disease_label,
            "compartment": config.compartment,
            "role": config.role,
            "donor_id": str(donor_id),
            "disease": str(disease),
            "group": "case" if disease == config.disease_label else "control",
            "n_cells": int(len(idx)),
            "cell_types": ",".join(sorted(cell_frame.iloc[idx]["cell_type"].astype(str).unique())),
        }
        for gene, j in gene_to_local.items():
            vals = log_expr[idx, j]
            zvals = z_expr[idx, j]
            rows.append(
                {
                    **base,
                    "gene": gene,
                    "mean_log_norm": float(np.nanmean(vals)),
                    "mean_z_vs_controls": float(np.nanmean(zvals)),
                    "detection_fraction": float((vals > 0).mean()),
                }
            )
    presence = pd.DataFrame(
        [
            {
                "analysis": config.name,
                "disease_name": config.disease_label,
                "compartment": config.compartment,
                "role": config.role,
                "gene": gene,
            }
            for gene in present_genes
        ]
    )
    return pd.DataFrame(rows), presence


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


def sender_raw_contrasts(sender_scores: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (analysis, gene), sub in sender_scores.groupby(["analysis", "gene"], observed=True):
        first = sub.iloc[0]
        rows.append(
            {
                "analysis": analysis,
                "disease_name": first["disease_name"],
                "compartment": first["compartment"],
                "role": first["role"],
                "gene": gene,
                **compare_values(sub["mean_z_vs_controls"], sub["group"]),
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
        out["tissue_up_trend"] = (out["delta_case_minus_control"] > 0.30) & (out["p"] < 0.10)
        out["tissue_down_trend"] = (out["delta_case_minus_control"] < -0.30) & (out["p"] < 0.10)
    return out.sort_values(["gene", "p"], na_position="last") if not out.empty else out


def myeloid_module_wide() -> pd.DataFrame:
    scores = read_tsv(MYELOID_MODULE_SCORES)
    if scores.empty:
        return pd.DataFrame()
    scores = scores.loc[scores["role"].eq("myeloid_apc") & scores["module"].isin(MYELOID_MODULES)].copy()
    wide = scores.pivot_table(
        index=["analysis", "dataset_path", "disease_name", "donor_id", "group"],
        columns="module",
        values="mean_score",
        aggfunc="mean",
    ).reset_index()
    return wide


def bridge_links(sender_scores: pd.DataFrame, raw: pd.DataFrame, myeloid: pd.DataFrame) -> pd.DataFrame:
    tissue = sender_scores.loc[sender_scores["role"].ne("myeloid_apc")].copy()
    if tissue.empty or myeloid.empty:
        return pd.DataFrame()
    raw_key = raw.set_index(["analysis", "gene"]) if not raw.empty else pd.DataFrame()
    rows: list[dict[str, object]] = []
    for (analysis, gene), sub in tissue.groupby(["analysis", "gene"], observed=True):
        first = sub.iloc[0]
        msub = myeloid.loc[
            myeloid["dataset_path"].eq(first["dataset_path"]) & myeloid["disease_name"].eq(first["disease_name"])
        ].copy()
        if msub.empty:
            continue
        merged = sub[
            [
                "dataset_path",
                "disease_name",
                "donor_id",
                "group",
                "gene",
                "mean_z_vs_controls",
                "detection_fraction",
                "compartment",
                "role",
            ]
        ].merge(
            msub[["analysis", "donor_id", "group", *[m for m in MYELOID_MODULES if m in msub.columns]]],
            on=["donor_id", "group"],
            how="inner",
            suffixes=("_tissue", "_myeloid"),
        )
        raw_row = raw_key.loc[(analysis, gene)] if not raw.empty and (analysis, gene) in raw_key.index else None
        for module in MYELOID_MODULES:
            if module not in merged.columns:
                continue
            valid = merged[["mean_z_vs_controls", module]].dropna()
            if len(valid) >= 5 and valid["mean_z_vs_controls"].std(ddof=1) > 1e-8 and valid[module].std(ddof=1) > 1e-8:
                rho_all, p_all = stats.spearmanr(valid["mean_z_vs_controls"], valid[module])
            else:
                rho_all, p_all = np.nan, np.nan
            case_valid = merged.loc[merged["group"].eq("case"), ["mean_z_vs_controls", module]].dropna()
            if len(case_valid) >= 4 and case_valid["mean_z_vs_controls"].std(ddof=1) > 1e-8 and case_valid[module].std(ddof=1) > 1e-8:
                rho_case, p_case = stats.spearmanr(case_valid["mean_z_vs_controls"], case_valid[module])
            else:
                rho_case, p_case = np.nan, np.nan
            rows.append(
                {
                    "tissue_analysis": analysis,
                    "myeloid_analysis": msub["analysis"].iloc[0],
                    "dataset_path": first["dataset_path"],
                    "disease_name": first["disease_name"],
                    "tissue_compartment": first["compartment"],
                    "gene": gene,
                    "myeloid_module": module,
                    "n_paired_donors": int(len(valid)),
                    "spearman_rho_all": float(rho_all) if pd.notna(rho_all) else np.nan,
                    "spearman_p_all": float(p_all) if pd.notna(p_all) else np.nan,
                    "n_case_paired_donors": int(len(case_valid)),
                    "spearman_rho_case": float(rho_case) if pd.notna(rho_case) else np.nan,
                    "spearman_p_case": float(p_case) if pd.notna(p_case) else np.nan,
                    "sender_tissue_delta": safe_float(raw_row.get("delta_case_minus_control")) if raw_row is not None else np.nan,
                    "sender_tissue_p": safe_float(raw_row.get("p"), 1.0) if raw_row is not None else 1.0,
                    "sender_tissue_up_trend": bool(raw_row.get("tissue_up_trend")) if raw_row is not None else False,
                    "sender_tissue_down_trend": bool(raw_row.get("tissue_down_trend")) if raw_row is not None else False,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["all_link_positive"] = (out["spearman_rho_all"] >= 0.55) & (out["spearman_p_all"] < 0.05)
        out["case_link_positive"] = (out["n_case_paired_donors"] >= 5) & (out["spearman_rho_case"] >= 0.75) & (out["spearman_p_case"] < 0.10)
        out["bridge_link_positive"] = out["all_link_positive"] | out["case_link_positive"]
        out["upregulated_bridge_link"] = out["bridge_link_positive"] & out["sender_tissue_up_trend"]
    return out.sort_values(["gene", "spearman_p_all"], na_position="last") if not out.empty else out


def summarize_genes(links: pd.DataFrame, raw: pd.DataFrame, gene_axis: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    genes = sorted(set(links["gene"].unique()) | set(raw["gene"].unique())) if not links.empty or not raw.empty else []
    for gene in genes:
        lsub = links.loc[links["gene"].eq(gene)] if not links.empty else pd.DataFrame()
        rsub = raw.loc[raw["gene"].eq(gene)] if not raw.empty else pd.DataFrame()
        bridge = lsub.loc[lsub.get("bridge_link_positive", False).astype(bool)] if not lsub.empty else pd.DataFrame()
        up_bridge = lsub.loc[lsub.get("upregulated_bridge_link", False).astype(bool)] if not lsub.empty else pd.DataFrame()
        up_raw = rsub.loc[rsub.get("tissue_up_trend", False).astype(bool)] if not rsub.empty else pd.DataFrame()
        down_raw = rsub.loc[rsub.get("tissue_down_trend", False).astype(bool)] if not rsub.empty else pd.DataFrame()
        axis = gene_axis.loc[gene_axis["gene"].eq(gene)] if not gene_axis.empty else pd.DataFrame()
        best_axis = axis.sort_values(["wave30_centrality_score", "wave30_intervention_score"], ascending=[False, False]).head(1)
        prior_blocking = bool(axis["wave30_manual_prior_risk"].astype(str).str.contains("blocking", case=False, na=False).any()) if not axis.empty else False
        rows.append(
            {
                "gene": gene,
                "bridge_link_count": int(len(bridge)),
                "bridge_link_disease_count": int(bridge["disease_name"].nunique()) if not bridge.empty else 0,
                "bridge_link_diseases": ";".join(sorted(bridge["disease_name"].dropna().astype(str).unique())) if not bridge.empty else "",
                "upregulated_bridge_link_count": int(len(up_bridge)),
                "upregulated_bridge_link_disease_count": int(up_bridge["disease_name"].nunique()) if not up_bridge.empty else 0,
                "upregulated_bridge_link_diseases": ";".join(sorted(up_bridge["disease_name"].dropna().astype(str).unique())) if not up_bridge.empty else "",
                "raw_up_tissue_disease_count": int(up_raw["disease_name"].nunique()) if not up_raw.empty else 0,
                "raw_down_tissue_disease_count": int(down_raw["disease_name"].nunique()) if not down_raw.empty else 0,
                "case_link_count": int(lsub.get("case_link_positive", pd.Series(False, index=lsub.index)).sum()) if not lsub.empty else 0,
                "best_bridge_link": (
                    bridge.sort_values(["spearman_p_all", "spearman_p_case"], na_position="last")
                    .head(1)
                    .apply(
                        lambda r: (
                            f"{r['tissue_analysis']}->{r['myeloid_analysis']}|{r['myeloid_module']}|"
                            f"rho_all={r['spearman_rho_all']:.3g}|p_all={r['spearman_p_all']:.3g}|"
                            f"rho_case={r['spearman_rho_case']:.3g}|p_case={r['spearman_p_case']:.3g}|"
                            f"sender_delta={r['sender_tissue_delta']:.3g}|sender_p={r['sender_tissue_p']:.3g}"
                        ),
                        axis=1,
                    )
                    .iloc[0]
                    if not bridge.empty
                    else ""
                ),
                "wave30_axis_count": int(axis["wave30_axis"].nunique()) if not axis.empty else 0,
                "best_wave30_axis": best_axis["wave30_axis"].iloc[0] if not best_axis.empty else "",
                "best_wave30_call": best_axis["wave30_call"].iloc[0] if not best_axis.empty else "",
                "best_wave30_centrality": safe_float(best_axis["wave30_centrality_score"].iloc[0]) if not best_axis.empty else np.nan,
                "best_wave30_intervention_score": safe_float(best_axis["wave30_intervention_score"].iloc[0]) if not best_axis.empty else np.nan,
                "wave30_prior_blocking": prior_blocking,
                "best_wave30_gate_failures": best_axis["wave30_gate_failures"].iloc[0] if not best_axis.empty else "",
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["bridge_score"] = (
        4 * out["upregulated_bridge_link_disease_count"].fillna(0)
        + 2 * out["bridge_link_disease_count"].fillna(0)
        + out["case_link_count"].fillna(0)
        + out["raw_up_tissue_disease_count"].fillna(0)
        + out["best_wave30_centrality"].fillna(0) / 10
        + out["best_wave30_intervention_score"].fillna(0).clip(lower=-2, upper=5) / 5
        - 2 * out["raw_down_tissue_disease_count"].fillna(0)
        - 2 * out["wave30_prior_blocking"].astype(int)
    )
    calls = []
    for _, row in out.iterrows():
        if row["upregulated_bridge_link_disease_count"] >= 2 and row["case_link_count"] >= 1 and not row["wave30_prior_blocking"]:
            calls.append("REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT")
        elif row["upregulated_bridge_link_disease_count"] >= 2:
            calls.append("PARK_BRIDGE_PRIOR_OR_DIRECTION_REVIEW")
        elif row["bridge_link_disease_count"] >= 3:
            calls.append("PARK_CORRELATION_ONLY_NOT_DISEASE_UP")
        else:
            calls.append("NO_GO_WEAK_OR_CONTEXT_SPECIFIC_BRIDGE")
    out["wave103_call"] = calls
    priority = {
        "REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT": 0,
        "PARK_BRIDGE_PRIOR_OR_DIRECTION_REVIEW": 1,
        "PARK_CORRELATION_ONLY_NOT_DISEASE_UP": 2,
        "NO_GO_WEAK_OR_CONTEXT_SPECIFIC_BRIDGE": 3,
    }
    out["wave103_call_priority"] = out["wave103_call"].map(priority).fillna(99).astype(int)
    return out.sort_values(["wave103_call_priority", "bridge_score"], ascending=[True, False])


def write_report(summary: pd.DataFrame, links: pd.DataFrame, run_log: list[dict[str, object]]) -> None:
    promoted = summary.loc[summary["wave103_call"].eq("REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT")]
    branch_call = "REOPEN_BRIDGE_AXIS_FOR_WAVE104" if not promoted.empty else "NO_PROMOTABLE_BRIDGE_AXIS_YET"
    bridge = links.loc[links.get("bridge_link_positive", pd.Series(False, index=links.index)).astype(bool)] if not links.empty else pd.DataFrame()
    up_bridge = links.loc[links.get("upregulated_bridge_link", pd.Series(False, index=links.index)).astype(bool)] if not links.empty else pd.DataFrame()

    lines = [
        "# Wave103 Sender-to-Myeloid Bridge Scan",
        "",
        "## Bottom Line",
        "",
        f"Branch call: `{branch_call}`.",
        "",
        "This scan ranks tissue-resident communication genes by same-donor",
        "association with paired myeloid lipid/C15/inflammatory modules. It is",
        "a bridge-discovery screen, not a therapeutic claim.",
        "",
        "## Top Gene Summary",
        "",
        markdown_table(
            summary[
                [
                    "gene",
                    "wave103_call",
                    "bridge_score",
                    "upregulated_bridge_link_disease_count",
                    "bridge_link_disease_count",
                    "raw_up_tissue_disease_count",
                    "raw_down_tissue_disease_count",
                    "case_link_count",
                    "best_wave30_axis",
                    "best_wave30_call",
                    "wave30_prior_blocking",
                    "best_bridge_link",
                ]
            ],
            max_rows=30,
        ),
        "",
        "## Upregulated Bridge Links",
        "",
        markdown_table(
            up_bridge[
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
                    "sender_tissue_delta",
                    "sender_tissue_p",
                ]
            ].sort_values(["gene", "spearman_p_all"], na_position="last")
            if not up_bridge.empty
            else pd.DataFrame(),
            max_rows=40,
        ),
        "",
        "## All Positive Bridge Links",
        "",
        markdown_table(
            bridge[
                [
                    "gene",
                    "tissue_analysis",
                    "myeloid_analysis",
                    "disease_name",
                    "tissue_compartment",
                    "myeloid_module",
                    "spearman_rho_all",
                    "spearman_p_all",
                    "spearman_rho_case",
                    "spearman_p_case",
                    "sender_tissue_delta",
                    "sender_tissue_p",
                ]
            ].sort_values(["spearman_p_all"], na_position="last")
            if not bridge.empty
            else pd.DataFrame(),
            max_rows=60,
        ),
        "",
        "## Interpretation",
        "",
        "- A top bridge hit needs disease-up sender expression and same-donor",
        "  myeloid module association across multiple autoimmune tissues.",
        "- Links that are not disease-up may still be useful biology, but they",
        "  are not intervention-ready because they can reflect tissue composition",
        "  or compensatory repair.",
        "- Wave30 prior-risk flags are carried forward; prior-blocked canonical",
        "  axes should not be promoted without a narrow new therapeutic delta.",
        "",
        "## Run Log",
        "",
        markdown_table(pd.DataFrame(run_log), max_rows=40),
        "",
        "## Reproducibility",
        "",
        "- Script: `scripts/v3_wave103_sender_to_myeloid_bridge_scan.py`",
        "- Sender scores: `results_v3/wave103_sender_to_myeloid_bridge_scan/sender_gene_scores.tsv`",
        "- Raw contrasts: `results_v3/wave103_sender_to_myeloid_bridge_scan/sender_raw_contrasts.tsv`",
        "- Bridge links: `results_v3/wave103_sender_to_myeloid_bridge_scan/sender_to_myeloid_bridge_links.tsv`",
        "- Summary: `results_v3/wave103_sender_to_myeloid_bridge_scan/sender_bridge_gene_summary.tsv`",
        f"- Seed: `{SEED}`",
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    bridge_genes, gene_axis = wave30_gene_map()
    cache: dict[Path, tuple[Any, sparse.csr_matrix]] = {}
    score_tables: list[pd.DataFrame] = []
    presence_tables: list[pd.DataFrame] = []
    run_log: list[dict[str, object]] = []

    for config in CONFIGS:
        try:
            if config.path not in cache:
                cache[config.path] = read_counts(config.path)
            a, x = cache[config.path]
            scores, presence = donor_sender_scores(config, a, x, bridge_genes)
            score_tables.append(scores)
            presence_tables.append(presence)
            run_log.append(
                {
                    "analysis": config.name,
                    "status": "completed",
                    "sender_rows": int(len(scores)),
                    "genes_present": int(presence["gene"].nunique()) if not presence.empty else 0,
                }
            )
        except Exception as exc:
            run_log.append({"analysis": config.name, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})

    sender_scores = pd.concat(score_tables, ignore_index=True) if score_tables else pd.DataFrame()
    presence = pd.concat(presence_tables, ignore_index=True) if presence_tables else pd.DataFrame()
    raw = sender_raw_contrasts(sender_scores) if not sender_scores.empty else pd.DataFrame()
    myeloid = myeloid_module_wide()
    links = bridge_links(sender_scores, raw, myeloid) if not sender_scores.empty and not myeloid.empty else pd.DataFrame()
    summary = summarize_genes(links, raw, gene_axis)

    sender_scores.to_csv(OUT / "sender_gene_scores.tsv", sep="\t", index=False)
    presence.to_csv(OUT / "sender_gene_presence.tsv", sep="\t", index=False)
    raw.to_csv(OUT / "sender_raw_contrasts.tsv", sep="\t", index=False)
    links.to_csv(OUT / "sender_to_myeloid_bridge_links.tsv", sep="\t", index=False)
    gene_axis.to_csv(OUT / "wave30_gene_axis_map.tsv", sep="\t", index=False)
    summary.to_csv(OUT / "sender_bridge_gene_summary.tsv", sep="\t", index=False)

    branch_call = (
        "REOPEN_BRIDGE_AXIS_FOR_WAVE104"
        if not summary.empty and summary["wave103_call"].eq("REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT").any()
        else "NO_PROMOTABLE_BRIDGE_AXIS_YET"
    )
    summary_json = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "n_bridge_genes_requested": len(bridge_genes),
        "n_sender_genes_observed": int(sender_scores["gene"].nunique()) if not sender_scores.empty else 0,
        "n_bridge_links": int(links.get("bridge_link_positive", pd.Series(dtype=bool)).sum()) if not links.empty else 0,
        "n_upregulated_bridge_links": int(links.get("upregulated_bridge_link", pd.Series(dtype=bool)).sum()) if not links.empty else 0,
        "top_rows": summary.head(20).to_dict(orient="records") if not summary.empty else [],
        "run_log": run_log,
        "outputs": {
            "sender_gene_scores": rel(OUT / "sender_gene_scores.tsv"),
            "sender_gene_presence": rel(OUT / "sender_gene_presence.tsv"),
            "sender_raw_contrasts": rel(OUT / "sender_raw_contrasts.tsv"),
            "sender_to_myeloid_bridge_links": rel(OUT / "sender_to_myeloid_bridge_links.tsv"),
            "sender_bridge_gene_summary": rel(OUT / "sender_bridge_gene_summary.tsv"),
            "wave30_gene_axis_map": rel(OUT / "wave30_gene_axis_map.tsv"),
            "report": rel(OUT / "REPORT.md"),
        },
    }
    write_json(OUT / "summary.json", summary_json)
    write_report(summary, links, run_log)
    print(json.dumps(summary_json, indent=2))


if __name__ == "__main__":
    main()
