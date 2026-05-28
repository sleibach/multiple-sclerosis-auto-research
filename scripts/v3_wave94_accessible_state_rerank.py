#!/usr/bin/env python3
"""Wave94 systematic rerank of accessible state-transition candidates.

The lipid-lysosomal branch repeatedly failed when treated as a direct
lipid-enzyme target problem. This wave inverts the search: start from
accessible or druggable proteins with an MS anchor and cross-disease recurrence,
then ask whether any candidate is more than a marker.

This is a prioritization/routing analysis, not a therapeutic claim.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from v3_analyze_direct_h5ad_cell_states import ROOT
from v3_wave85_external_geo_antitnf_validation import (
    GPL570_ANNOT,
    SERIES_FILES,
    bh,
    cohort_specs,
    expression_to_gene_level as gpl570_expression_to_gene_level,
    hedges_g,
    markdown_table,
    mask_for_spec,
    patient_level_scores,
    read_gpl570_gene_map,
    read_series_matrix as read_gpl570_series_matrix,
    rel,
    residualize,
    sample_metadata as gpl570_sample_metadata,
    write_json,
    zscore_rows,
)
from v3_wave89_psoriasis_gse85034_response_validation import (
    GPL10558_ANNOT,
    SERIES as GSE85034_SERIES,
    build_patient_response_table,
    expression_to_gene_level as gpl10558_expression_to_gene_level,
    read_gpl10558_gene_map,
    read_series_matrix as read_gse85034_series_matrix,
    sample_metadata as gse85034_sample_metadata,
    test_feature as test_psoriasis_feature,
)
from v3_wave93_gpr183_oxysterol_forcing_test import auc_score, log_cpm


SEED = 20260527
OUT = ROOT / "results_v3" / "wave94_accessible_state_rerank"

W39 = ROOT / "results_v3" / "wave39_surfaceome_rescue_after_resolution_pivot" / "surfaceome_rescue_rank_full.tsv"
W55 = ROOT / "results_v3" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W91 = ROOT / "results_v3" / "wave91_lipid_neighborhood_controller_scan" / "lipid_neighborhood_controller_rank.tsv"
BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
MS_SIG = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
RA_COUNTS = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"

FOUNDATION_FILES = [
    ROOT / "results_v3" / "geneformer_pivot_panel_delete" / "geneformer_pivot_panel_context_metrics_ranked.tsv",
    ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_geneformer_gene_summary.tsv",
    ROOT / "results_v3" / "wave69d_gse282122_geneformer_remission_centroid" / "geneformer_remission_gene_summary.tsv",
    ROOT / "results_v3" / "wave70c_inhibitory_receptor_geneformer_direction" / "geneformer_direction_metrics.tsv",
    ROOT / "results_v3" / "wave79_targetability_shortlist_audit" / "targetability_foundation_rank_rows.tsv",
]

PRIMARY_IBD_CONTEXTS = {
    "GSE12251_UC_ACT1_baseline",
    "GSE14580_UC_Leuven_baseline",
    "GSE16879_Crohn_colitis_Leuven_baseline",
    "GSE16879_Crohn_ileitis_Leuven_baseline",
}

MANUAL_INCLUDE = {
    "APOC1",
    "APOE",
    "LPL",
    "GPNMB",
    "CHI3L1",
    "CD200",
    "CD82",
    "FXYD5",
    "SCD",
    "SPNS1",
    "SEL1L3",
    "FABP5",
}

KNOWN_CLOSED_OR_SATURATED = {
    "ACSL1",
    "FABP5",
    "GPR183",
    "IL1B",
    "LAMP3",
    "NAMPT",
    "OSM",
    "TREM1",
}

GENERIC_IMMUNE_PREFIXES = ("HLA-", "CCL", "CXCL", "IL", "GBP", "IFI", "IFIT", "ISG", "TNF")
GENERIC_IMMUNE_EXCEPTIONS = {"SEL1L3"}


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def f(value: Any) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return math.nan
    return out


def s(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value)


def boolish(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["true", "1", "yes"])


def candidate_pool() -> pd.DataFrame:
    w39 = read_tsv(W39)
    if w39.empty:
        return pd.DataFrame()
    w39["gene"] = w39["gene"].astype(str).str.upper()
    for col in ["has_ms_anchor", "uniprot_accessible", "in_lipid_lysosomal_myeloid_neighborhood"]:
        if col in w39.columns:
            w39[col] = boolish(w39[col])
        else:
            w39[col] = False
    w39["positive_disease_count"] = pd.to_numeric(w39["positive_disease_count"], errors="coerce").fillna(0).astype(int)
    w39["negative_disease_count"] = pd.to_numeric(w39["negative_disease_count"], errors="coerce").fillna(0).astype(int)
    w39["ms_wm_delta_log2"] = pd.to_numeric(w39["ms_wm_delta_log2"], errors="coerce")
    w39["ms_wm_p"] = pd.to_numeric(w39["ms_wm_p"], errors="coerce")
    base = w39[
        (
            w39["has_ms_anchor"]
            | ((w39["ms_wm_delta_log2"] > 0.25) & (w39["ms_wm_p"] < 0.20))
            | w39["gene"].isin(MANUAL_INCLUDE)
        )
        & (w39["uniprot_accessible"] | w39["gene"].isin(MANUAL_INCLUDE))
        & ((w39["positive_disease_count"] >= 3) | w39["gene"].isin(MANUAL_INCLUDE))
    ].copy()

    w91 = read_tsv(W91)
    if not w91.empty and "gene" in w91.columns:
        w91["gene"] = w91["gene"].astype(str).str.upper()
        keep = w91[w91["gene"].isin(MANUAL_INCLUDE)].copy()
        for gene in keep["gene"].unique():
            if gene not in set(base["gene"]):
                base = pd.concat(
                    [
                        base,
                        pd.DataFrame(
                            [
                                {
                                    "gene": gene,
                                    "wave39_call": "NOT_IN_W39_MANUAL_LIPID_INCLUDE",
                                    "wave39_score": np.nan,
                                    "wave39_reason": "manual_include_from_wave91_or_lipid_axis",
                                    "positive_disease_count": np.nan,
                                    "negative_disease_count": np.nan,
                                    "positive_diseases": "",
                                    "negative_diseases": "",
                                    "has_ms_anchor": False,
                                    "uniprot_accessible": False,
                                    "in_lipid_lysosomal_myeloid_neighborhood": True,
                                    "ms_wm_delta_log2": np.nan,
                                    "ms_wm_p": np.nan,
                                    "function_excerpt": "",
                                }
                            ]
                        ),
                    ],
                    ignore_index=True,
                    sort=False,
                )
    return base.drop_duplicates("gene").sort_values("gene")


def broad_summaries(genes: set[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    broad = read_tsv(BROAD)
    if broad.empty:
        return pd.DataFrame(), pd.DataFrame()
    broad["gene"] = broad["gene"].astype(str).str.upper()
    rows = broad[broad["gene"].isin(genes)].copy()
    rows["positive_trend"] = (pd.to_numeric(rows["delta_log2_cpm"], errors="coerce") > 0.30) & (
        pd.to_numeric(rows["p"], errors="coerce") < 0.10
    )
    rows["negative_trend"] = (pd.to_numeric(rows["delta_log2_cpm"], errors="coerce") < -0.30) & (
        pd.to_numeric(rows["p"], errors="coerce") < 0.10
    )
    summary_rows: list[dict[str, Any]] = []
    for gene, sub in rows.groupby("gene", dropna=False):
        pos = sub[sub["positive_trend"]]
        neg = sub[sub["negative_trend"]]
        pos_myeloid = pos[pos["role"].astype(str).eq("myeloid_apc")]
        pos_tissue = pos[~pos["role"].astype(str).eq("myeloid_apc")]
        summary_rows.append(
            {
                "gene": gene,
                "broad_tested_contexts": int(len(sub)),
                "broad_positive_contexts": int(len(pos)),
                "broad_negative_contexts": int(len(neg)),
                "broad_positive_disease_count": int(pos["disease_name"].nunique()) if not pos.empty else 0,
                "broad_negative_disease_count": int(neg["disease_name"].nunique()) if not neg.empty else 0,
                "myeloid_positive_contexts": int(len(pos_myeloid)),
                "myeloid_positive_disease_count": int(pos_myeloid["disease_name"].nunique()) if not pos_myeloid.empty else 0,
                "tissue_resident_positive_contexts": int(len(pos_tissue)),
                "positive_diseases_broad": ";".join(sorted(map(str, pos["disease_name"].dropna().unique()))) if not pos.empty else "",
                "negative_diseases_broad": ";".join(sorted(map(str, neg["disease_name"].dropna().unique()))) if not neg.empty else "",
                "best_positive_context": (
                    pos.sort_values(["delta_log2_cpm", "p"], ascending=[False, True])
                    .head(1)
                    .apply(lambda r: f"{r['analysis']}|{r['disease_name']}|{r['compartment']}|role={r['role']}|delta={r['delta_log2_cpm']:.3g}|p={r['p']:.3g}", axis=1)
                    .iloc[0]
                    if not pos.empty
                    else ""
                ),
                "best_negative_context": (
                    neg.sort_values(["delta_log2_cpm", "p"], ascending=[True, True])
                    .head(1)
                    .apply(lambda r: f"{r['analysis']}|{r['disease_name']}|{r['compartment']}|role={r['role']}|delta={r['delta_log2_cpm']:.3g}|p={r['p']:.3g}", axis=1)
                    .iloc[0]
                    if not neg.empty
                    else ""
                ),
            }
        )
    return rows.sort_values(["gene", "p"]), pd.DataFrame(summary_rows).sort_values("gene")


def ms_rows(genes: set[str]) -> pd.DataFrame:
    ms = read_tsv(MS_SIG)
    if ms.empty:
        return pd.DataFrame()
    ms["gene"] = ms["gene"].astype(str).str.upper()
    rows = ms[ms["gene"].isin(genes)].copy()
    rows["ms_positive_anchor"] = (pd.to_numeric(rows["delta_log2"], errors="coerce") > 0) & (pd.to_numeric(rows["p"], errors="coerce") < 0.10)
    rows["ms_positive_trend"] = (pd.to_numeric(rows["delta_log2"], errors="coerce") > 0) & (pd.to_numeric(rows["p"], errors="coerce") < 0.20)
    return rows.sort_values("gene")


def test_response_gene(df: pd.DataFrame, gene: str, spec: Any | None = None) -> dict[str, Any]:
    if gene not in df.columns:
        return {}
    response_col = "response"
    base = df[[col for col in ["patient_id", "response", "disease", "tissue", gene] if col in df.columns]].copy()
    base[gene] = pd.to_numeric(base[gene], errors="coerce")
    base = base[np.isfinite(base[gene]) & base[response_col].isin([0, 1])].copy()
    if len(base) < 6 or base[response_col].nunique() < 2:
        return {}
    score = base[gene].to_numpy(float)
    if spec is not None and getattr(spec, "adjustment_covariates", None):
        score = residualize(score, base, list(spec.adjustment_covariates))
    y = base[response_col].astype(int).to_numpy()
    responders = score[y == 1]
    nonresponders = score[y == 0]
    t_stat, p_value = (
        stats.ttest_ind(responders, nonresponders, equal_var=False, nan_policy="omit")
        if len(responders) >= 3 and len(nonresponders) >= 3
        else (math.nan, math.nan)
    )
    effect = float(np.nanmean(responders) - np.nanmean(nonresponders))
    auc_response = auc_score(y, score)
    return {
        "gene": gene,
        "n_patients": int(len(base)),
        "n_responders": int(y.sum()),
        "n_nonresponders": int((1 - y).sum()),
        "effect_responder_minus_non": effect,
        "hedges_g_responder_minus_non": hedges_g(responders, nonresponders),
        "auc_high_expression_nonresponse": float(1.0 - auc_response) if np.isfinite(auc_response) else math.nan,
        "p": float(p_value) if np.isfinite(p_value) else 1.0,
        "nonresponse_high_direction": bool(effect < 0),
    }


def ibd_response_tests(genes: set[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    probe_to_genes, coverage = read_gpl570_gene_map(GPL570_ANNOT, genes)
    rows: list[dict[str, Any]] = []
    for series, path in SERIES_FILES.items():
        metadata, expr_probe = read_gpl570_series_matrix(path)
        info = gpl570_sample_metadata(series, metadata)
        gene_expr = gpl570_expression_to_gene_level(expr_probe, probe_to_genes)
        for spec in cohort_specs(series, info):
            selected = info.loc[mask_for_spec(info, spec)].copy()
            samples = [sample for sample in selected["sample"] if sample in gene_expr.columns]
            if len(samples) < 6:
                continue
            gene_z = zscore_rows(gene_expr[samples])
            present = sorted(genes & set(gene_z.index))
            if not present:
                continue
            score_df = gene_z.loc[present].T.copy()
            score_df.index.name = "sample"
            patients = patient_level_scores(score_df, selected, spec)
            for gene in present:
                row = test_response_gene(patients, gene, spec)
                if row:
                    row.update(
                        {
                            "system": "IBD_external_antitnf",
                            "cohort": spec.cohort,
                            "series": series,
                            "primary_independent_context": bool(spec.cohort in PRIMARY_IBD_CONTEXTS),
                            "disease_scope": spec.disease_scope,
                            "tissue_scope": spec.tissue_scope,
                        }
                    )
                    rows.append(row)
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr_all"] = bh(out["p"].astype(float).to_numpy())
        out["fdr_within_cohort"] = out.groupby("cohort")["p"].transform(lambda vals: bh(vals.astype(float).to_numpy()))
    return out, coverage


def ra_response_tests(genes: set[str]) -> pd.DataFrame:
    counts = read_tsv(RA_COUNTS)
    meta = read_tsv(RA_META)
    if counts.empty or meta.empty:
        return pd.DataFrame()
    counts["GeneSymbol"] = counts["GeneSymbol"].astype(str).str.upper()
    expr = log_cpm(counts)
    sample_cols = [col for col in expr.columns if col != "GeneSymbol"]
    gene_z = zscore_rows(expr.set_index("GeneSymbol")[sample_cols])
    pre = meta[meta["timepoint"].astype(str).str.lower().eq("pre")].copy()
    pre = pre[pre["count_column"].isin(gene_z.columns)].copy()
    pre["response"] = pre["responder_moderate_or_good"].astype(str).str.lower().isin(["true", "1", "yes"]).astype(int)
    rows: list[dict[str, Any]] = []
    for gene in sorted(genes & set(gene_z.index)):
        base = pre.copy()
        base["_score"] = pd.to_numeric(gene_z.loc[gene, base["count_column"].tolist()].to_numpy(), errors="coerce")
        base = base[np.isfinite(base["_score"]) & base["response"].isin([0, 1])].copy()
        if len(base) < 8 or base["response"].nunique() < 2:
            continue
        adjusted = residualize(base["_score"].to_numpy(float), base, ["pathotype", "biologic", "inflammatory_score", "das28_score"])
        test_df = pd.DataFrame(
            {
                "patient_id": base["patient"].astype(str).to_numpy(),
                "response": base["response"].astype(int).to_numpy(),
                "disease": "rheumatoid arthritis",
                "tissue": "synovium",
                gene: adjusted,
            }
        )
        row = test_response_gene(test_df, gene)
        if row:
            row.update({"system": "RA_GSE198520_baseline_synovium", "cohort": "GSE198520_pre"})
            rows.append(row)
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = bh(out["p"].astype(float).to_numpy())
    return out


def psoriasis_response_tests(genes: set[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not GSE85034_SERIES.exists() or not GPL10558_ANNOT.exists():
        return pd.DataFrame(), pd.DataFrame()
    metadata, expr_probe = read_gse85034_series_matrix(GSE85034_SERIES)
    info = gse85034_sample_metadata(metadata)
    patients = build_patient_response_table(info)
    probe_to_genes, coverage = read_gpl10558_gene_map(GPL10558_ANNOT, genes)
    gene_expr = gpl10558_expression_to_gene_level(expr_probe, probe_to_genes)
    if gene_expr.empty:
        return pd.DataFrame(), coverage
    gene_z = zscore_rows(gene_expr)
    patient_gene = gene_z.T.copy()
    patient_gene.index.name = "sample"
    rows: list[dict[str, Any]] = []
    for treatment in ["ADA", "MTX", "ALL"]:
        for gene in sorted(genes & set(patient_gene.columns)):
            row = test_psoriasis_feature(patient_gene, patients, gene, treatment, "gene")
            if row:
                row.update({"system": "psoriasis_GSE85034_baseline_skin", "cohort": f"GSE85034_{treatment}"})
                rows.append(row)
    out = pd.DataFrame(rows)
    if not out.empty:
        out = out.rename(columns={"feature": "gene", "auc_high_score_nonresponse": "auc_high_expression_nonresponse"})
        out["fdr_within_treatment"] = np.nan
        for treatment, idx in out.groupby("treatment").groups.items():
            out.loc[idx, "fdr_within_treatment"] = bh(out.loc[idx, "p"].astype(float).to_numpy())
    return out, coverage


def response_meta(ibd: pd.DataFrame, ra: pd.DataFrame, pso: pd.DataFrame) -> pd.DataFrame:
    blocks: list[pd.DataFrame] = []
    if not ibd.empty:
        blocks.append(ibd[ibd["primary_independent_context"]].copy())
    if not ra.empty:
        blocks.append(ra.copy())
    if not pso.empty:
        blocks.append(pso[pso["treatment"].eq("ADA")].copy())
    if not blocks:
        return pd.DataFrame()
    all_tests = pd.concat(blocks, ignore_index=True, sort=False)
    rows: list[dict[str, Any]] = []
    for (system, gene), sub in all_tests.groupby(["system", "gene"], dropna=False):
        clean = sub[np.isfinite(pd.to_numeric(sub["hedges_g_responder_minus_non"], errors="coerce"))].copy()
        if clean.empty:
            continue
        weights = pd.to_numeric(clean.get("n_patients", pd.Series(1, index=clean.index)), errors="coerce").fillna(1).clip(lower=1)
        rows.append(
            {
                "system": system,
                "gene": gene,
                "n_contexts": int(len(clean)),
                "nonresponse_high_contexts": int((pd.to_numeric(clean["effect_responder_minus_non"], errors="coerce") < 0).sum()),
                "responder_high_contexts": int((pd.to_numeric(clean["effect_responder_minus_non"], errors="coerce") > 0).sum()),
                "nominal_nonresponse_contexts_p_lt_0_10": int(
                    (
                        (pd.to_numeric(clean["effect_responder_minus_non"], errors="coerce") < 0)
                        & (pd.to_numeric(clean["p"], errors="coerce") < 0.10)
                    ).sum()
                ),
                "weighted_mean_hedges_g_responder_minus_non": float(
                    np.average(pd.to_numeric(clean["hedges_g_responder_minus_non"], errors="coerce"), weights=weights)
                ),
                "median_auc_high_expression_nonresponse": float(pd.to_numeric(clean["auc_high_expression_nonresponse"], errors="coerce").median())
                if "auc_high_expression_nonresponse" in clean.columns
                else math.nan,
                "min_p": float(pd.to_numeric(clean["p"], errors="coerce").min()),
            }
        )
    return pd.DataFrame(rows).sort_values(["gene", "system"])


def genetics_rows(genes: set[str]) -> pd.DataFrame:
    rows = []
    for source, path in [("wave55", W55), ("wave62", W62)]:
        df = read_tsv(path)
        if df.empty or "gene" not in df.columns:
            continue
        df["gene"] = df["gene"].astype(str).str.upper()
        keep = df[df["gene"].isin(genes)].copy()
        keep.insert(0, "source", source)
        rows.append(keep)
    return pd.concat(rows, ignore_index=True, sort=False) if rows else pd.DataFrame()


def genetics_summary(genetics: pd.DataFrame) -> pd.DataFrame:
    if genetics.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for gene, sub in genetics.groupby("gene"):
        max_diseases = 0
        disease_text = []
        for col in ["n_diseases_genetic_ge_0_25", "strong_l2g_disease_count", "supporting_l2g_disease_count"]:
            if col in sub.columns:
                max_diseases = max(max_diseases, int(pd.to_numeric(sub[col], errors="coerce").fillna(0).max()))
        for col in ["diseases_genetic_ge_0_25", "strong_l2g_diseases", "supporting_l2g_diseases"]:
            if col in sub.columns:
                disease_text.extend([x for x in sub[col].dropna().astype(str).tolist() if x and x != "nan"])
        chembl = 0
        for col in ["druggable_activity_count", "chembl_activity_count"]:
            if col in sub.columns:
                chembl = max(chembl, int(pd.to_numeric(sub[col], errors="coerce").fillna(0).max()))
        rows.append(
            {
                "gene": gene,
                "genetic_disease_count_max": max_diseases,
                "genetic_disease_text": ";".join(sorted(set(";".join(disease_text).split(";")) - {""})),
                "target_resolution_sources": ";".join(sorted(set(sub["source"].astype(str)))),
                "chembl_or_druggable_activity_count_max": chembl,
            }
        )
    return pd.DataFrame(rows).sort_values("gene")


def foundation_summary(genes: set[str]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for path in FOUNDATION_FILES:
        df = read_tsv(path)
        if df.empty or "gene" not in df.columns:
            continue
        df["gene"] = df["gene"].astype(str).str.upper()
        keep = df[df["gene"].isin(genes)].copy()
        if keep.empty:
            continue
        for gene, sub in keep.groupby("gene"):
            support_cols = [col for col in sub.columns if "support" in col.lower() or "recommend" in col.lower() or "call" in col.lower()]
            support_text = " ".join(sub[support_cols].astype(str).fillna("").agg(" ".join, axis=1).tolist()).lower() if support_cols else ""
            rows.append(
                {
                    "gene": gene,
                    "source_file": rel(path),
                    "n_rows": int(len(sub)),
                    "supportive_text_hits": int(sum(token in support_text for token in ["support", "rescue", "promote", "candidate"])),
                    "do_not_promote_text_hits": int(sum(token in support_text for token in ["no_go", "do_not_promote", "wrong_direction", "demote"])),
                    "support_text_excerpt": support_text[:500],
                }
            )
    if not rows:
        return pd.DataFrame()
    out = pd.DataFrame(rows)
    summary = out.groupby("gene", as_index=False).agg(
        foundation_files=("source_file", lambda s: ";".join(sorted(set(s)))),
        foundation_rows=("n_rows", "sum"),
        foundation_supportive_text_hits=("supportive_text_hits", "sum"),
        foundation_do_not_promote_text_hits=("do_not_promote_text_hits", "sum"),
    )
    return summary.sort_values("gene")


def integrate(
    candidates: pd.DataFrame,
    broad_summary: pd.DataFrame,
    ms: pd.DataFrame,
    resp: pd.DataFrame,
    genetics: pd.DataFrame,
    foundation: pd.DataFrame,
) -> pd.DataFrame:
    df = candidates.copy()
    df = df.merge(broad_summary, on="gene", how="left")
    ms_keep = ms[["gene", "delta_log2", "hedges_g", "p", "fdr", "ms_positive_anchor", "ms_positive_trend"]].rename(
        columns={"delta_log2": "ms_delta_log2_direct", "hedges_g": "ms_hedges_g_direct", "p": "ms_p_direct", "fdr": "ms_fdr_direct"}
    )
    df = df.merge(ms_keep, on="gene", how="left")
    df = df.merge(genetics, on="gene", how="left")
    df = df.merge(foundation, on="gene", how="left")

    response_rows: list[dict[str, Any]] = []
    for gene, sub in resp.groupby("gene") if not resp.empty else []:
        systems = sub.copy()
        nonresponse_systems = int(
            (
                (systems["nonresponse_high_contexts"] > systems["responder_high_contexts"])
                & (pd.to_numeric(systems["min_p"], errors="coerce") < 0.20)
            ).sum()
        )
        responder_systems = int(
            (
                (systems["responder_high_contexts"] > systems["nonresponse_high_contexts"])
                & (pd.to_numeric(systems["min_p"], errors="coerce") < 0.20)
            ).sum()
        )
        response_rows.append(
            {
                "gene": gene,
                "response_systems_tested": int(systems["system"].nunique()),
                "response_nonresponse_high_systems_p20": nonresponse_systems,
                "response_responder_high_systems_p20": responder_systems,
                "response_direction_conflict": bool(nonresponse_systems > 0 and responder_systems > 0),
                "response_best_min_p": float(pd.to_numeric(systems["min_p"], errors="coerce").min()),
                "response_summary": "; ".join(
                    systems.apply(
                        lambda r: f"{r['system']}:g={r['weighted_mean_hedges_g_responder_minus_non']:.3g},p={r['min_p']:.3g},nonctx={int(r['nonresponse_high_contexts'])},respctx={int(r['responder_high_contexts'])}",
                        axis=1,
                    ).tolist()
                ),
            }
        )
    response_summary = pd.DataFrame(response_rows)
    df = df.merge(response_summary, on="gene", how="left")

    for col in [
        "positive_disease_count",
        "negative_disease_count",
        "broad_positive_disease_count",
        "broad_negative_disease_count",
        "myeloid_positive_disease_count",
        "response_nonresponse_high_systems_p20",
        "response_responder_high_systems_p20",
        "genetic_disease_count_max",
        "chembl_or_druggable_activity_count_max",
        "foundation_rows",
        "foundation_supportive_text_hits",
        "foundation_do_not_promote_text_hits",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        else:
            df[col] = 0
    for col in ["in_lipid_lysosomal_myeloid_neighborhood", "uniprot_accessible", "ms_positive_anchor", "ms_positive_trend"]:
        if col in df.columns:
            df[col] = boolish(df[col])
        else:
            df[col] = False

    reason = df.get("wave39_reason", pd.Series("", index=df.index)).astype(str).str.lower()
    df["known_closed_or_saturated"] = df["gene"].astype(str).isin(KNOWN_CLOSED_OR_SATURATED)
    df["generic_immune_marker_symbol"] = df["gene"].astype(str).map(
        lambda gene: gene not in GENERIC_IMMUNE_EXCEPTIONS and gene.startswith(GENERIC_IMMUNE_PREFIXES)
    )
    df["prior_saturation_penalty"] = (
        reason.str.contains("prior_art_or_trial_saturation").astype(int) * 3
        + reason.str.contains("generic_ifn_cytokine").astype(int) * 4
        + reason.str.contains("core_machinery").astype(int) * 4
        + reason.str.contains("prior_demoted").astype(int) * 1
        + reason.str.contains("directional_negative").astype(int) * 1
        + (pd.to_numeric(df.get("europepmc_hit_count", 0), errors="coerce").fillna(0) > 1000).astype(int)
        + (pd.to_numeric(df.get("clinicaltrials_hit_count", 0), errors="coerce").fillna(0) > 0).astype(int)
        + df["foundation_do_not_promote_text_hits"].clip(upper=2)
        + df["known_closed_or_saturated"].astype(int) * 8
        + df["generic_immune_marker_symbol"].astype(int) * 5
    )
    df["targetability_score"] = (
        df["uniprot_accessible"].astype(int) * 1.0
        + df["in_lipid_lysosomal_myeloid_neighborhood"].astype(int) * 1.5
        + (pd.to_numeric(df.get("chembl_activity_count", 0), errors="coerce").fillna(0) > 0).astype(int) * 1.0
        + (df["chembl_or_druggable_activity_count_max"] > 0).astype(int) * 1.0
        + (df.get("uniprot_transmembrane_feature_count", pd.Series(0, index=df.index)).fillna(0).astype(float) > 0).astype(int) * 0.75
    )
    df["biology_score"] = (
        df["ms_positive_anchor"].astype(int) * 3.0
        + df["ms_positive_trend"].astype(int) * 1.0
        + pd.to_numeric(df.get("ms_delta_log2_direct", df.get("ms_wm_delta_log2", 0)), errors="coerce").fillna(0).clip(lower=0, upper=2)
        + df["broad_positive_disease_count"].clip(upper=5) * 1.0
        + df["myeloid_positive_disease_count"].clip(upper=3) * 0.75
        - df["broad_negative_disease_count"].clip(upper=3) * 1.5
    )
    df["support_score"] = (
        df["response_nonresponse_high_systems_p20"].clip(upper=3) * 1.0
        - df["response_responder_high_systems_p20"].clip(upper=3) * 0.75
        - boolish(df.get("response_direction_conflict", pd.Series(False, index=df.index))).astype(int) * 2.0
        + df["genetic_disease_count_max"].clip(upper=5) * 0.5
        + df["foundation_supportive_text_hits"].clip(upper=3) * 0.5
    )
    df["wave94_score"] = df["biology_score"] + df["targetability_score"] + df["support_score"] - df["prior_saturation_penalty"]

    failures: list[str] = []
    calls: list[str] = []
    for _, row in df.iterrows():
        fail = []
        if not bool(row.get("ms_positive_anchor", False)) and not bool(row.get("ms_positive_trend", False)):
            fail.append("weak_ms_anchor")
        if int(row.get("broad_positive_disease_count", 0)) < 4 and not bool(row.get("in_lipid_lysosomal_myeloid_neighborhood", False)):
            fail.append("limited_cross_disease_breadth")
        if int(row.get("broad_negative_disease_count", 0)) > 0:
            fail.append("directional_negative_context")
        if int(row.get("prior_saturation_penalty", 0)) >= 4:
            fail.append("prior_or_class_saturated")
        if bool(row.get("known_closed_or_saturated", False)):
            fail.append("known_closed_route")
        if bool(row.get("generic_immune_marker_symbol", False)):
            fail.append("generic_immune_marker")
        if int(row.get("genetic_disease_count_max", 0)) < 2:
            fail.append("weak_genetic_target_resolution")
        if int(row.get("response_nonresponse_high_systems_p20", 0)) + int(row.get("response_responder_high_systems_p20", 0)) == 0:
            fail.append("no_response_or_perturbation_support")
        if bool(row.get("response_direction_conflict", False)):
            fail.append("response_direction_conflict")
        failures.append(";".join(fail))
        if row["wave94_score"] >= 8 and "prior_or_class_saturated" not in fail and "weak_ms_anchor" not in fail:
            calls.append("PARK_FOR_NEXT_FORCING_TEST")
        elif row["wave94_score"] >= 5 and "prior_or_class_saturated" not in fail:
            calls.append("PARK_ACCESSIBLE_MARKER_OR_WEAK_ROUTE")
        else:
            calls.append("NO_GO_ACCESSIBLE_STATE_RERANK")
    df["wave94_failures"] = failures
    df["wave94_call"] = calls
    call_rank = {
        "PARK_FOR_NEXT_FORCING_TEST": 0,
        "PARK_ACCESSIBLE_MARKER_OR_WEAK_ROUTE": 1,
        "NO_GO_ACCESSIBLE_STATE_RERANK": 2,
    }
    df["_call_rank"] = df["wave94_call"].map(call_rank).fillna(9).astype(int)
    return df.sort_values(["_call_rank", "wave94_score", "biology_score"], ascending=[True, False, False]).drop(columns=["_call_rank"])


def analyze() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    candidates = candidate_pool()
    genes = set(candidates["gene"].astype(str)) if not candidates.empty else set()
    broad_rows, broad_summary = broad_summaries(genes)
    ms = ms_rows(genes)
    ibd, ibd_cov = ibd_response_tests(genes)
    ra = ra_response_tests(genes)
    pso, pso_cov = psoriasis_response_tests(genes)
    resp_meta = response_meta(ibd, ra, pso)
    genetics = genetics_rows(genes)
    gen_sum = genetics_summary(genetics)
    foundation = foundation_summary(genes)
    ranked = integrate(candidates, broad_summary, ms, resp_meta, gen_sum, foundation)

    candidates.to_csv(OUT / "candidate_pool.tsv", sep="\t", index=False)
    broad_rows.to_csv(OUT / "broad_candidate_context_rows.tsv", sep="\t", index=False)
    broad_summary.to_csv(OUT / "broad_candidate_summary.tsv", sep="\t", index=False)
    ms.to_csv(OUT / "ms_candidate_rows.tsv", sep="\t", index=False)
    ibd.to_csv(OUT / "ibd_candidate_response_tests.tsv", sep="\t", index=False)
    ibd_cov.to_csv(OUT / "ibd_platform_coverage.tsv", sep="\t", index=False)
    ra.to_csv(OUT / "ra_candidate_response_tests.tsv", sep="\t", index=False)
    pso.to_csv(OUT / "psoriasis_candidate_response_tests.tsv", sep="\t", index=False)
    pso_cov.to_csv(OUT / "psoriasis_platform_coverage.tsv", sep="\t", index=False)
    resp_meta.to_csv(OUT / "candidate_response_meta.tsv", sep="\t", index=False)
    genetics.to_csv(OUT / "candidate_genetics_rows.tsv", sep="\t", index=False)
    gen_sum.to_csv(OUT / "candidate_genetics_summary.tsv", sep="\t", index=False)
    foundation.to_csv(OUT / "candidate_foundation_summary.tsv", sep="\t", index=False)
    ranked.to_csv(OUT / "accessible_state_candidate_rank.tsv", sep="\t", index=False)

    call_counts = ranked["wave94_call"].value_counts().to_dict() if not ranked.empty else {}
    summary = {
        "seed": SEED,
        "analysis_call": "ACCESSIBLE_STATE_RERANK_COMPLETED",
        "n_candidates": int(len(candidates)),
        "call_counts": {str(k): int(v) for k, v in call_counts.items()},
        "top_candidate": str(ranked.iloc[0]["gene"]) if not ranked.empty else "",
        "top_candidate_call": str(ranked.iloc[0]["wave94_call"]) if not ranked.empty else "",
        "top_candidate_score": float(ranked.iloc[0]["wave94_score"]) if not ranked.empty else math.nan,
        "inputs": {
            "wave39": rel(W39),
            "wave91": rel(W91),
            "broad_h5ad": rel(BROAD),
            "ms_signature": rel(MS_SIG),
            "wave55": rel(W55),
            "wave62": rel(W62),
            "ra_counts": rel(RA_COUNTS),
            "ra_meta": rel(RA_META),
            "psoriasis_series": rel(GSE85034_SERIES),
            "psoriasis_platform": rel(GPL10558_ANNOT),
        },
    }
    write_json(OUT / "summary.json", summary)

    display_cols = [
        "gene",
        "wave94_call",
        "wave94_score",
        "biology_score",
        "targetability_score",
        "support_score",
        "prior_saturation_penalty",
        "ms_delta_log2_direct",
        "ms_p_direct",
        "broad_positive_disease_count",
        "broad_negative_disease_count",
        "myeloid_positive_disease_count",
        "in_lipid_lysosomal_myeloid_neighborhood",
        "response_nonresponse_high_systems_p20",
        "response_responder_high_systems_p20",
        "genetic_disease_count_max",
        "foundation_rows",
        "wave94_failures",
        "response_summary",
    ]
    display = ranked[[col for col in display_cols if col in ranked.columns]].head(40) if not ranked.empty else pd.DataFrame()
    report = [
        "# Wave94 Accessible State Candidate Rerank",
        "",
        "Question: after closing direct lipid enzymes and GPR183, which accessible/druggable state-transition candidates deserve the next forcing test?",
        "",
        f"Analysis call: `{summary['analysis_call']}`.",
        "",
        "## Summary",
        "",
        f"- Candidate count: `{summary['n_candidates']}`",
        f"- Call counts: `{summary['call_counts']}`",
        f"- Top candidate: `{summary['top_candidate']}` (`{summary['top_candidate_call']}`, score `{summary['top_candidate_score']:.3g}`)",
        "",
        "## Ranked Candidates",
        "",
        markdown_table(display, max_rows=40),
        "",
        "## Guardrails",
        "",
        "- This is not a finding. It only selects the next branch for forcing tests.",
        "- Response direction is scored as support only when it repeats across systems; conflicting responder/nonresponder directions are penalized.",
        "- Prior-art and class-saturation penalties are intentionally coarse at this stage and must be replaced with direct novelty audits before any claim.",
        "- Secreted or surface accessibility is not assumed to imply causal control.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    np.random.seed(SEED)
    result = analyze()
    print(json.dumps(result, indent=2, sort_keys=True))
