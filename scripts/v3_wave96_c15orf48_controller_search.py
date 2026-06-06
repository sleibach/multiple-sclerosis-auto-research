#!/usr/bin/env python3
"""Wave96 de novo controller search around the C15ORF48 state.

Wave95 left C15ORF48 as a mechanistic state clue, not a druggable target. This
wave asks a narrower question: are there reachable genes that travel with the
C15ORF48-positive autoimmune tissue state across public atlases and have an
independent intervention package?

The script deliberately separates:

1. disease-contrast state proximity to C15ORF48;
2. donor-level pseudo-bulk co-state validation in raw h5ad atlases;
3. independent intervention evidence from genetics, perturbation, response, and
   targetability files.

It does not infer causality from co-expression.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse, stats

from v3_analyze_osmr_complement_axes import CONFIGS, ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave96_c15orf48_controller_search"

BROAD = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
MS = ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv"
RESID = ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
W39 = ROOT / "phases/v3/results" / "wave39_surfaceome_rescue_after_resolution_pivot" / "surfaceome_rescue_rank_full.tsv"
W55 = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W62 = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W68 = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
W37 = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W18 = ROOT / "phases/v3/results" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv"
W79 = ROOT / "phases/v3/results" / "wave79_targetability_shortlist_audit" / "targetability_integrated_decision.tsv"
W94 = ROOT / "phases/v3/results" / "wave94_accessible_state_rerank" / "accessible_state_candidate_rank.tsv"
W95 = ROOT / "phases/v3/results" / "wave95_mechanistic_forcing_triage" / "mechanistic_forcing_candidate_rank.tsv"


MECHANISTIC_SEEDS = {
    "C15ORF48",
    "COX4I1",
    "COX4I2",
    "NDUFA4",
    "HIF1A",
    "NAMPT",
    "LDHA",
    "SLC2A1",
    "HK2",
    "PFKFB3",
    "PRKAA1",
    "PRKAA2",
    "ULK1",
    "MTOR",
    "TSC1",
    "TSC2",
    "SQSTM1",
    "ATG5",
    "ATG7",
    "NFE2L2",
    "KEAP1",
    "HMOX1",
    "GCLC",
    "GCLM",
    "SLC7A11",
    "GPX4",
    "TXNRD1",
    "SOD2",
    "PPARGC1A",
    "PPARG",
    "AHR",
    "SQLE",
    "FADS1",
    "FADS2",
    "LIPA",
    "ABCA1",
    "ABCG1",
    "NR1H3",
    "NR1H2",
}


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value)


def num(value: Any, default: float = math.nan) -> float:
    try:
        if pd.isna(value):
            return default
        out = float(value)
        return out if math.isfinite(out) else default
    except (TypeError, ValueError):
        return default


def first_row(df: pd.DataFrame, gene: str, col: str = "gene") -> pd.Series | None:
    if df.empty or col not in df.columns:
        return None
    sub = df[df[col].astype(str).str.upper().eq(gene.upper())]
    if sub.empty:
        return None
    return sub.iloc[0]


def best_w68_row(df: pd.DataFrame, gene: str) -> pd.Series | None:
    if df.empty or "gene" not in df.columns:
        return None
    sub = df[df["gene"].astype(str).str.upper().eq(gene.upper())].copy()
    if sub.empty:
        return None
    sub["_fdr"] = pd.to_numeric(sub.get("remission_adjusted_fdr", np.nan), errors="coerce").fillna(1.0)
    sub["_p"] = pd.to_numeric(sub.get("remission_adjusted_p", np.nan), errors="coerce").fillna(1.0)
    return sub.sort_values(["_fdr", "_p"]).iloc[0]


def best_w37_row(df: pd.DataFrame, gene: str) -> pd.Series | None:
    if df.empty or "gene_symbol" not in df.columns:
        return None
    sub = df[df["gene_symbol"].astype(str).str.upper().eq(gene.upper())].copy()
    if sub.empty:
        return None
    sub["_fdr"] = pd.to_numeric(sub.get("contrast_fdr", np.nan), errors="coerce").fillna(1.0)
    return sub.sort_values("_fdr").iloc[0]


def best_w18_row(df: pd.DataFrame, gene: str) -> pd.Series | None:
    if df.empty or "gene" not in df.columns:
        return None
    sub = df[df["gene"].astype(str).str.upper().eq(gene.upper())].copy()
    if sub.empty:
        return None
    sub["_rank"] = pd.to_numeric(sub.get("wave18_rank", np.nan), errors="coerce").fillna(9999)
    return sub.sort_values("_rank").iloc[0]


def gene_symbol_map(a: ad.AnnData, symbol_column: str, genes: set[str]) -> dict[str, int]:
    if symbol_column in a.var.columns:
        symbols = a.var[symbol_column].astype(str).str.upper()
    elif "feature_name" in a.var.columns:
        symbols = a.var["feature_name"].astype(str).str.upper()
    else:
        symbols = pd.Series(a.var_names.astype(str)).str.upper()
    mapping: dict[str, int] = {}
    wanted = {gene.upper() for gene in genes}
    for idx, symbol in enumerate(symbols):
        if symbol in wanted and symbol not in mapping:
            mapping[symbol] = idx
    return mapping


def build_anchor_contexts(broad: pd.DataFrame) -> pd.DataFrame:
    c15 = broad[broad["gene"].astype(str).str.upper().eq("C15ORF48")].copy()
    c15["c15_anchor_strict"] = (c15["delta_log2_cpm"] > 0) & (c15["p"] < 0.05)
    c15["c15_anchor_trend"] = (c15["delta_log2_cpm"] > 0) & (c15["p"] < 0.10)
    c15["c15_anchor_fdr10"] = (c15["delta_log2_cpm"] > 0) & (c15["fdr"] < 0.10)
    keep = [
        "analysis",
        "disease_name",
        "compartment",
        "role",
        "delta_log2_cpm",
        "hedges_g",
        "p",
        "fdr",
        "c15_anchor_strict",
        "c15_anchor_trend",
        "c15_anchor_fdr10",
    ]
    return c15[keep].rename(
        columns={
            "delta_log2_cpm": "c15_delta_log2_cpm",
            "hedges_g": "c15_hedges_g",
            "p": "c15_p",
            "fdr": "c15_fdr",
        }
    )


def contrast_state_rank(broad: pd.DataFrame, anchors: pd.DataFrame) -> pd.DataFrame:
    c15_vec = anchors[["analysis", "c15_delta_log2_cpm", "c15_anchor_strict", "c15_anchor_trend"]]
    merged = broad.merge(c15_vec, on="analysis", how="inner")
    merged["gene"] = merged["gene"].astype(str).str.upper()
    rows = []
    trend_contexts = set(anchors.loc[anchors["c15_anchor_trend"], "analysis"].astype(str))
    strict_contexts = set(anchors.loc[anchors["c15_anchor_strict"], "analysis"].astype(str))
    for gene, sub in merged.groupby("gene", sort=False):
        if gene == "C15ORF48":
            continue
        sub = sub.copy()
        sub["candidate_positive_trend"] = (sub["delta_log2_cpm"] > 0) & (sub["p"] < 0.10)
        sub["candidate_negative_trend"] = (sub["delta_log2_cpm"] < 0) & (sub["p"] < 0.10)
        trend = sub[sub["analysis"].astype(str).isin(trend_contexts)]
        strict = sub[sub["analysis"].astype(str).isin(strict_contexts)]
        if len(sub) >= 4 and sub["delta_log2_cpm"].std(ddof=0) > 1e-9:
            pearson_r, pearson_p = stats.pearsonr(sub["delta_log2_cpm"], sub["c15_delta_log2_cpm"])
            spearman_r, spearman_p = stats.spearmanr(sub["delta_log2_cpm"], sub["c15_delta_log2_cpm"])
        else:
            pearson_r, pearson_p, spearman_r, spearman_p = np.nan, np.nan, np.nan, np.nan
        trend_pos = trend[trend["candidate_positive_trend"]]
        trend_neg = trend[trend["candidate_negative_trend"]]
        strict_pos = strict[strict["candidate_positive_trend"]]
        rows.append(
            {
                "gene": gene,
                "n_contexts_compared": int(len(sub)),
                "c15_trend_contexts_tested": int(len(trend)),
                "c15_trend_positive_context_count": int(len(trend_pos)),
                "c15_trend_positive_disease_count": int(trend_pos["disease_name"].nunique()),
                "c15_trend_negative_context_count": int(len(trend_neg)),
                "c15_strict_positive_context_count": int(len(strict_pos)),
                "c15_strict_positive_disease_count": int(strict_pos["disease_name"].nunique()),
                "c15_myeloid_positive_context_count": int(len(trend_pos[trend_pos["role"].eq("myeloid_apc")])),
                "c15_state_pearson_r": float(pearson_r) if pd.notna(pearson_r) else np.nan,
                "c15_state_pearson_p": float(pearson_p) if pd.notna(pearson_p) else np.nan,
                "c15_state_spearman_r": float(spearman_r) if pd.notna(spearman_r) else np.nan,
                "c15_state_spearman_p": float(spearman_p) if pd.notna(spearman_p) else np.nan,
                "best_c15_context_delta": float(trend_pos["delta_log2_cpm"].max()) if not trend_pos.empty else np.nan,
                "best_c15_context": clean(
                    trend_pos.sort_values("p").iloc[0]["analysis"] if not trend_pos.empty else ""
                ),
                "positive_c15_contexts": ";".join(trend_pos["analysis"].astype(str).tolist()[:12]),
                "negative_c15_contexts": ";".join(trend_neg["analysis"].astype(str).tolist()[:12]),
            }
        )
    rank = pd.DataFrame(rows)
    rank["contrast_state_score"] = (
        rank["c15_trend_positive_context_count"].clip(upper=8)
        + 1.5 * rank["c15_strict_positive_disease_count"].clip(upper=4)
        + rank["c15_myeloid_positive_context_count"].clip(upper=3)
        + rank["c15_state_pearson_r"].fillna(0).clip(lower=-1, upper=1) * 2.0
        - 1.5 * rank["c15_trend_negative_context_count"].clip(upper=4)
    )
    return rank


def add_external_evidence(rank: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for rec in rank.to_dict("records"):
        gene = clean(rec["gene"]).upper()
        ms = first_row(tables["ms"], gene)
        resid = first_row(tables["resid"], gene)
        w39 = first_row(tables["w39"], gene)
        w55 = first_row(tables["w55"], gene)
        w62 = first_row(tables["w62"], gene)
        w68 = best_w68_row(tables["w68"], gene)
        w37 = best_w37_row(tables["w37"], gene)
        w18 = best_w18_row(tables["w18"], gene)
        w79 = first_row(tables["w79"], gene)
        w94 = first_row(tables["w94"], gene)
        w95 = first_row(tables["w95"], gene, col="candidate")

        rec.update(
            {
                "mechanistic_seed": gene in MECHANISTIC_SEEDS,
                "ms_delta_log2": num(ms.get("delta_log2")) if ms is not None else num(w39.get("ms_wm_delta_log2")) if w39 is not None else math.nan,
                "ms_p": num(ms.get("p")) if ms is not None else num(w39.get("ms_wm_p")) if w39 is not None else math.nan,
                "ms_fdr": num(ms.get("fdr")) if ms is not None else math.nan,
                "residual_strict_disease_count": num(resid.get("strict_core_covariate_surviving_disease_count"), 0.0) if resid is not None else 0.0,
                "residual_retained_disease_count": num(resid.get("retained_positive_disease_count"), 0.0) if resid is not None else 0.0,
                "wave39_call": clean(w39.get("wave39_call")) if w39 is not None else "",
                "wave39_score": num(w39.get("wave39_score")) if w39 is not None else math.nan,
                "uniprot_accessible": clean(w39.get("uniprot_accessible")) if w39 is not None else "",
                "chembl_activity_count": num(w39.get("chembl_activity_count"), 0.0) if w39 is not None else num(w62.get("druggable_activity_count"), 0.0) if w62 is not None else 0.0,
                "wave55_score": num(w55.get("wave55_score"), 0.0) if w55 is not None else 0.0,
                "wave55_n_genetic_diseases_ge_0_25": num(w55.get("n_diseases_genetic_ge_0_25"), 0.0) if w55 is not None else 0.0,
                "wave55_genetic_diseases_ge_0_25": clean(w55.get("diseases_genetic_ge_0_25")) if w55 is not None else "",
                "wave62_score": num(w62.get("wave62_score"), 0.0) if w62 is not None else 0.0,
                "wave62_call": clean(w62.get("wave62_call")) if w62 is not None else "",
                "wave62_ms_max_l2g_score": num(w62.get("ms_max_l2g_score"), 0.0) if w62 is not None else 0.0,
                "wave62_ms_max_relevant_qtl_h4": num(w62.get("ms_max_relevant_qtl_h4"), 0.0) if w62 is not None else 0.0,
                "wave62_strong_l2g_disease_count": num(w62.get("strong_l2g_disease_count"), 0.0) if w62 is not None else 0.0,
                "wave62_strong_qtl_coloc_disease_count": num(w62.get("strong_qtl_coloc_disease_count"), 0.0) if w62 is not None else 0.0,
                "manual_blocker": clean(w62.get("manual_blocker")) if w62 is not None else "",
                "prior_context_blocker": clean(w62.get("prior_context_blocker")) if w62 is not None else "",
                "w68_cell_state": clean(w68.get("cell_state")) if w68 is not None else "",
                "w68_remission_adjusted_delta": num(w68.get("remission_adjusted_delta")) if w68 is not None else math.nan,
                "w68_remission_adjusted_p": num(w68.get("remission_adjusted_p")) if w68 is not None else math.nan,
                "w68_remission_adjusted_fdr": num(w68.get("remission_adjusted_fdr")) if w68 is not None else math.nan,
                "w68_call": clean(w68.get("wave68_call")) if w68 is not None else "",
                "w37_screen_call": clean(w37.get("screen_call")) if w37 is not None else "",
                "w37_contrast_lfc": num(w37.get("median_efficient_minus_noneater_lfc")) if w37 is not None else math.nan,
                "w37_contrast_fdr": num(w37.get("contrast_fdr"), 1.0) if w37 is not None else 1.0,
                "w18_strong_support_contexts": num(w18.get("total_strong_support_contexts"), 0.0) if w18 is not None else 0.0,
                "w18_recommendation": clean(w18.get("foundation_rescue_recommendation")) if w18 is not None else "",
                "wave79_call": clean(w79.get("wave79_call")) if w79 is not None else "",
                "wave79_gate_count": num(w79.get("gate_count"), 0.0) if w79 is not None else 0.0,
                "wave94_call": clean(w94.get("wave94_call")) if w94 is not None else "",
                "wave94_score": num(w94.get("wave94_score")) if w94 is not None else math.nan,
                "wave95_call": clean(w95.get("wave95_call")) if w95 is not None else "",
            }
        )
        rows.append(rec)
    return pd.DataFrame(rows)


def score_with_external_evidence(rank: pd.DataFrame) -> pd.DataFrame:
    ms_expr = (rank["ms_delta_log2"] > 0.25) & (rank["ms_p"] < 0.10)
    ms_gen = (rank["wave62_ms_max_l2g_score"] >= 0.5) | (rank["wave62_ms_max_relevant_qtl_h4"] >= 0.8)
    rank["gate_ms_anchor"] = ms_expr | ms_gen
    rank["gate_c15_contrast_state"] = (
        (rank["c15_trend_positive_context_count"] >= 4)
        & (rank["c15_trend_positive_disease_count"] >= 2)
        & (rank["c15_trend_negative_context_count"] <= 1)
        & (rank["c15_state_pearson_r"].fillna(0) >= 0.25)
    )
    rank["gate_cross_disease_residual"] = rank["residual_strict_disease_count"] >= 2
    rank["gate_cell_response_or_transition"] = rank["w68_remission_adjusted_fdr"].fillna(1.0) <= 0.10
    rank["gate_real_perturbation"] = rank["w37_screen_call"].str.startswith("KO_", na=False) & (rank["w37_contrast_fdr"].fillna(1.0) <= 0.20)
    rank["gate_foundation_support"] = (rank["w18_strong_support_contexts"] >= 1) & ~rank["w18_recommendation"].str.contains("do_not_promote", case=False, na=False)
    rank["gate_genetics"] = (
        (rank["wave62_strong_l2g_disease_count"] >= 2)
        | (rank["wave62_strong_qtl_coloc_disease_count"] >= 2)
        | (rank["wave55_n_genetic_diseases_ge_0_25"] >= 4)
    )
    rank["gate_modality"] = (
        rank["uniprot_accessible"].astype(str).str.lower().isin({"true", "1", "yes"})
        | (rank["chembl_activity_count"].fillna(0) > 0)
        | rank["wave79_call"].astype(str).str.contains("PARK_TARGETABILITY", na=False)
    )
    blocker_text = (
        rank["manual_blocker"].fillna("")
        + " "
        + rank["prior_context_blocker"].fillna("")
        + " "
        + rank["wave95_call"].fillna("")
    )
    rank["gate_prior_not_blocked"] = ~blocker_text.str.contains("prior_art|PRIOR_ART|BLOCKED", regex=True, na=False)
    rank["intervention_evidence_count"] = (
        rank["gate_cell_response_or_transition"].astype(int)
        + rank["gate_real_perturbation"].astype(int)
        + rank["gate_foundation_support"].astype(int)
        + rank["gate_genetics"].astype(int)
        + rank["gate_modality"].astype(int)
    )
    rank["pre_donor_controller_score"] = (
        rank["contrast_state_score"].fillna(0)
        + 2.0 * rank["gate_ms_anchor"].astype(int)
        + 1.5 * rank["gate_cross_disease_residual"].astype(int)
        + 1.5 * rank["gate_cell_response_or_transition"].astype(int)
        + 1.5 * rank["gate_real_perturbation"].astype(int)
        + 1.0 * rank["gate_foundation_support"].astype(int)
        + 1.5 * rank["gate_genetics"].astype(int)
        + 1.0 * rank["gate_modality"].astype(int)
        + 0.75 * rank["mechanistic_seed"].astype(int)
        - 3.0 * (~rank["gate_prior_not_blocked"]).astype(int)
        - 1.0 * rank["c15_trend_negative_context_count"].clip(upper=3)
    )
    return rank


def donor_pseudobulk_for_config(config: Any, genes: set[str]) -> pd.DataFrame:
    a = ad.read_h5ad(config.path)
    obs = a.obs.copy()
    mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
    if mask.sum() == 0:
        return pd.DataFrame()
    x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
    mapping = gene_symbol_map(a, config.gene_symbol_column, genes)
    if "C15ORF48" not in mapping:
        return pd.DataFrame()
    present = sorted(mapping)
    cell_idx = np.flatnonzero(mask.to_numpy())
    gene_idx = [mapping[gene] for gene in present]
    sub_x = x[cell_idx][:, gene_idx].astype(float)
    lib_size = np.asarray(x[cell_idx].sum(axis=1)).ravel().astype(float)
    lib_size[~np.isfinite(lib_size) | (lib_size <= 0)] = np.nan
    scale = np.divide(1e4, lib_size, out=np.zeros_like(lib_size), where=np.isfinite(lib_size))
    log_expr = np.log1p(sub_x.multiply(scale[:, None]).toarray())
    expr = pd.DataFrame(log_expr, columns=present)
    meta = obs.loc[mask, ["donor_id", "disease", "cell_type"]].reset_index(drop=True)
    expr["donor_id"] = meta["donor_id"].astype(str).values
    expr["disease"] = meta["disease"].astype(str).values
    donor = expr.groupby(["donor_id", "disease"], as_index=False)[present].mean()
    return donor


def donor_correlations(anchor_contexts: pd.DataFrame, candidates: set[str]) -> pd.DataFrame:
    genes = {gene.upper() for gene in candidates} | {"C15ORF48"}
    config_by_name = {config.name: config for config in CONFIGS}
    rows = []
    for _, anchor in anchor_contexts[anchor_contexts["c15_anchor_trend"]].iterrows():
        analysis = clean(anchor["analysis"])
        config = config_by_name.get(analysis)
        if config is None:
            continue
        donor = donor_pseudobulk_for_config(config, genes)
        if donor.empty or "C15ORF48" not in donor.columns:
            continue
        donor["is_case"] = donor["disease"].eq(config.disease_label)
        for gene in sorted(genes - {"C15ORF48"}):
            if gene not in donor.columns:
                continue
            for scope, scope_df in [("all_donors", donor), ("case_donors", donor[donor["is_case"]])]:
                x = scope_df["C15ORF48"].to_numpy(float)
                y = scope_df[gene].to_numpy(float)
                ok = np.isfinite(x) & np.isfinite(y)
                if ok.sum() >= 3 and np.nanstd(x[ok]) > 1e-9 and np.nanstd(y[ok]) > 1e-9:
                    rho, p = stats.spearmanr(x[ok], y[ok])
                    pearson, pearson_p = stats.pearsonr(x[ok], y[ok]) if ok.sum() >= 3 else (np.nan, np.nan)
                else:
                    rho, p, pearson, pearson_p = np.nan, np.nan, np.nan, np.nan
                rows.append(
                    {
                        "analysis": analysis,
                        "disease_name": anchor["disease_name"],
                        "compartment": anchor["compartment"],
                        "role": anchor["role"],
                        "gene": gene,
                        "scope": scope,
                        "n_donors": int(ok.sum()),
                        "spearman_rho": float(rho) if pd.notna(rho) else np.nan,
                        "spearman_p": float(p) if pd.notna(p) else np.nan,
                        "pearson_r": float(pearson) if pd.notna(pearson) else np.nan,
                        "pearson_p": float(pearson_p) if pd.notna(pearson_p) else np.nan,
                    }
                )
    return pd.DataFrame(rows)


def summarize_donor_correlations(corr: pd.DataFrame) -> pd.DataFrame:
    if corr.empty:
        return pd.DataFrame(columns=["gene"])
    case = corr[corr["scope"].eq("case_donors")].copy()
    all_donors = corr[corr["scope"].eq("all_donors")].copy()
    rows = []
    for gene in sorted(set(corr["gene"].astype(str))):
        c = case[case["gene"].eq(gene)]
        a = all_donors[all_donors["gene"].eq(gene)]
        c_pos = c[(c["spearman_rho"] >= 0.30) & (c["spearman_p"].fillna(1.0) <= 0.20)]
        a_pos = a[(a["spearman_rho"] >= 0.30) & (a["spearman_p"].fillna(1.0) <= 0.20)]
        rows.append(
            {
                "gene": gene,
                "donor_case_contexts_tested": int(c["analysis"].nunique()),
                "donor_case_positive_context_count": int(len(c_pos)),
                "donor_case_positive_disease_count": int(c_pos["disease_name"].nunique()),
                "donor_case_median_spearman": float(c["spearman_rho"].median()) if not c.empty else np.nan,
                "donor_all_positive_context_count": int(len(a_pos)),
                "donor_all_positive_disease_count": int(a_pos["disease_name"].nunique()),
                "donor_all_median_spearman": float(a["spearman_rho"].median()) if not a.empty else np.nan,
                "best_donor_context": clean(c.sort_values(["spearman_p", "spearman_rho"], ascending=[True, False]).iloc[0]["analysis"] if not c.empty else ""),
                "best_donor_spearman": float(c["spearman_rho"].max()) if not c.empty else np.nan,
            }
        )
    return pd.DataFrame(rows)


def final_calls(rank: pd.DataFrame) -> pd.DataFrame:
    rank["gate_donor_costate"] = (
        (rank["donor_case_positive_context_count"].fillna(0) >= 2)
        | ((rank["donor_case_positive_context_count"].fillna(0) >= 1) & (rank["donor_all_positive_context_count"].fillna(0) >= 2))
    )
    rank["critical_gate_count"] = (
        rank["gate_c15_contrast_state"].astype(int)
        + rank["gate_donor_costate"].astype(int)
        + rank["gate_ms_anchor"].astype(int)
        + rank["gate_modality"].astype(int)
        + rank["gate_prior_not_blocked"].astype(int)
    )
    rank["support_gate_count"] = (
        rank["gate_cross_disease_residual"].astype(int)
        + rank["gate_cell_response_or_transition"].astype(int)
        + rank["gate_real_perturbation"].astype(int)
        + rank["gate_foundation_support"].astype(int)
        + rank["gate_genetics"].astype(int)
    )
    rank["wave96_score"] = (
        rank["pre_donor_controller_score"].fillna(0)
        + 2.0 * rank["gate_donor_costate"].astype(int)
        + rank["donor_case_positive_disease_count"].fillna(0).clip(upper=3)
        + 0.5 * rank["donor_all_positive_disease_count"].fillna(0).clip(upper=3)
    )
    calls = []
    reasons = []
    for rec in rank.to_dict("records"):
        failures = []
        for gate in [
            "gate_c15_contrast_state",
            "gate_donor_costate",
            "gate_ms_anchor",
            "gate_modality",
            "gate_prior_not_blocked",
            "gate_genetics",
        ]:
            if not bool(rec.get(gate, False)):
                failures.append(gate)
        if rec["critical_gate_count"] >= 5 and rec["support_gate_count"] >= 2:
            call = "REOPEN_C15_STATE_CONTROLLER_CANDIDATE"
            reason = "C15 state proximity, donor co-state, MS anchor, modality, and independent support all pass"
        elif not rec.get("gate_prior_not_blocked", False):
            call = "NO_GO_PRIOR_OR_BLOCKER"
            reason = "explicit prior/context blocker in upstream evidence"
        elif rec.get("gate_c15_contrast_state", False) and rec.get("gate_donor_costate", False) and rec.get("gate_modality", False):
            call = "PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE"
            reason = "state and modality support survive, but MS/genetics/perturbation package is incomplete"
        elif rec.get("gate_c15_contrast_state", False) and rec.get("gate_donor_costate", False):
            call = "PARK_C15_COSTATE_MARKER_NO_MODALITY"
            reason = "state support survives donor validation but lacks a selective intervention package"
        else:
            call = "NO_GO_C15_CONTROLLER_SEARCH"
            reason = "insufficient C15 state proximity or donor-level co-state support"
        calls.append(call)
        reasons.append(reason + "; failures=" + ";".join(failures))
    rank["wave96_call"] = calls
    rank["wave96_reason"] = reasons
    return rank.sort_values(
        [
            "wave96_call",
            "critical_gate_count",
            "support_gate_count",
            "wave96_score",
            "gene",
        ],
        ascending=[True, False, False, False, True],
    )


def report_table(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "gene",
        "wave96_call",
        "wave96_score",
        "critical_gate_count",
        "support_gate_count",
        "c15_trend_positive_context_count",
        "c15_trend_positive_disease_count",
        "c15_trend_negative_context_count",
        "c15_state_pearson_r",
        "donor_case_positive_context_count",
        "donor_case_positive_disease_count",
        "donor_case_median_spearman",
        "ms_delta_log2",
        "ms_p",
        "wave62_strong_qtl_coloc_disease_count",
        "wave55_n_genetic_diseases_ge_0_25",
        "chembl_activity_count",
        "w68_remission_adjusted_fdr",
        "w37_screen_call",
        "wave96_reason",
    ]
    return df[[c for c in cols if c in df.columns]]


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    broad = read_tsv(BROAD)
    broad["gene"] = broad["gene"].astype(str).str.upper()
    anchors = build_anchor_contexts(broad)
    anchors.to_csv(OUT / "c15orf48_anchor_contexts.tsv", sep="\t", index=False)

    contrast_rank = contrast_state_rank(broad, anchors)
    tables = {
        "ms": read_tsv(MS),
        "resid": read_tsv(RESID),
        "w39": read_tsv(W39),
        "w55": read_tsv(W55),
        "w62": read_tsv(W62),
        "w68": read_tsv(W68),
        "w37": read_tsv(W37),
        "w18": read_tsv(W18),
        "w79": read_tsv(W79),
        "w94": read_tsv(W94),
        "w95": read_tsv(W95),
    }
    for key, df in tables.items():
        if not df.empty and "gene" in df.columns:
            df["gene"] = df["gene"].astype(str).str.upper()
    if not tables["w37"].empty and "gene_symbol" in tables["w37"].columns:
        tables["w37"]["gene_symbol"] = tables["w37"]["gene_symbol"].astype(str).str.upper()
    if not tables["w95"].empty and "candidate" in tables["w95"].columns:
        tables["w95"]["candidate"] = tables["w95"]["candidate"].astype(str).str.upper()

    ranked = add_external_evidence(contrast_rank, tables)
    ranked = score_with_external_evidence(ranked)
    ranked["candidate_for_donor_validation"] = False
    donor_genes = set(ranked.sort_values("pre_donor_controller_score", ascending=False).head(250)["gene"])
    donor_genes |= {gene for gene in MECHANISTIC_SEEDS if gene in set(broad["gene"])}
    donor_genes |= set(ranked[ranked["gate_modality"] | ranked["gate_genetics"]]["gene"].head(100))
    ranked.loc[ranked["gene"].isin(donor_genes), "candidate_for_donor_validation"] = True

    donor_corr = donor_correlations(anchors, donor_genes)
    donor_summary = summarize_donor_correlations(donor_corr)
    final = ranked.merge(donor_summary, on="gene", how="left")
    donor_cols = [c for c in final.columns if c.startswith("donor_") or c.startswith("best_donor")]
    for col in donor_cols:
        if col.endswith("_count") or col.endswith("_tested"):
            final[col] = final[col].fillna(0)
    final = final_calls(final)

    contrast_rank.to_csv(OUT / "contrast_state_rank_all.tsv", sep="\t", index=False)
    ranked.to_csv(OUT / "pre_donor_controller_rank.tsv", sep="\t", index=False)
    donor_corr.to_csv(OUT / "donor_level_c15_costate_correlations.tsv", sep="\t", index=False)
    donor_summary.to_csv(OUT / "donor_level_c15_costate_summary.tsv", sep="\t", index=False)
    final.to_csv(OUT / "c15orf48_controller_candidate_rank.tsv", sep="\t", index=False)

    call_counts = final["wave96_call"].value_counts().to_dict()
    reopened = final[final["wave96_call"].eq("REOPEN_C15_STATE_CONTROLLER_CANDIDATE")]
    parked = final[final["wave96_call"].str.startswith("PARK_", na=False)]
    summary = {
        "seed": SEED,
        "analysis_call": "C15_CONTROLLER_SEARCH_COMPLETED",
        "n_genes_ranked": int(len(final)),
        "n_donor_validated_genes": int(len(donor_genes)),
        "n_reopened": int(len(reopened)),
        "n_parked": int(len(parked)),
        "call_counts": call_counts,
        "top_reopened": reopened.head(10)["gene"].tolist(),
        "top_parked": parked.head(10)["gene"].tolist(),
        "anchor_contexts_strict": anchors.loc[anchors["c15_anchor_strict"], "analysis"].tolist(),
        "anchor_contexts_trend": anchors.loc[anchors["c15_anchor_trend"], "analysis"].tolist(),
        "inputs": {
            "broad": rel(BROAD),
            "ms": rel(MS),
            "residual": rel(RESID),
            "wave39": rel(W39),
            "wave55": rel(W55),
            "wave62": rel(W62),
            "wave68": rel(W68),
            "wave37": rel(W37),
            "wave18": rel(W18),
            "wave79": rel(W79),
            "wave94": rel(W94),
            "wave95": rel(W95),
        },
    }
    write_json(OUT / "summary.json", summary)

    top = report_table(final.head(25))
    report = [
        "# Wave96 C15ORF48 Controller Search",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Question",
        "",
        "Can the C15ORF48-positive autoimmune mitochondrial/inflammatory-brake",
        "state be converted into a druggable controller or intervention point?",
        "",
        "## Anchor Contexts",
        "",
        f"Strict C15ORF48-positive contexts: `{len(summary['anchor_contexts_strict'])}`.",
        f"Trend C15ORF48-positive contexts: `{len(summary['anchor_contexts_trend'])}`.",
        "",
        "Strict contexts:",
        "",
        markdown_table(anchors[anchors["c15_anchor_strict"]][["analysis", "disease_name", "compartment", "role", "c15_delta_log2_cpm", "c15_p", "c15_fdr"]]),
        "",
        "## Verdict",
        "",
        f"Reopened controller candidates: `{len(reopened)}`.",
        f"Parked proximal candidates: `{len(parked)}`.",
        "",
        "## Call Counts",
        "",
        markdown_table(pd.DataFrame([{"wave96_call": k, "n": v} for k, v in call_counts.items()])),
        "",
        "## Top Ranked Rows",
        "",
        markdown_table(top, max_rows=25),
        "",
        "## Interpretation Guardrail",
        "",
        "C15ORF48 co-state evidence is not causality. A candidate can only be",
        "reopened here if the C15 contrast vector, donor-level co-state validation,",
        "MS anchoring, modality, and independent support channels agree. Otherwise",
        "the output is a branch map for the next forcing test.",
        "",
        "## Output Files",
        "",
        f"- `{rel(OUT / 'c15orf48_anchor_contexts.tsv')}`",
        f"- `{rel(OUT / 'contrast_state_rank_all.tsv')}`",
        f"- `{rel(OUT / 'pre_donor_controller_rank.tsv')}`",
        f"- `{rel(OUT / 'donor_level_c15_costate_correlations.tsv')}`",
        f"- `{rel(OUT / 'donor_level_c15_costate_summary.tsv')}`",
        f"- `{rel(OUT / 'c15orf48_controller_candidate_rank.tsv')}`",
        f"- `{rel(OUT / 'summary.json')}`",
        f"- `{rel(OUT / 'REPORT.md')}`",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
