#!/usr/bin/env python3
"""Wave91 module-wide lipid/lysosomal intervention-rank audit.

Wave90 parked direct LPL modulation but preserved LPL as a marker of a
lipid-loaded myeloid/repair state. This script asks the more defensible
follow-up question: within the broader lipid/lysosomal/autoinflammatory module
already present in the V3 evidence stack, is there any single gene that survives
as a plausible cross-autoimmune intervention node?

The gate is intentionally stricter than a rank score. A candidate must show:

- anti-TNF nonresponse-high direction in at least two disease systems;
- MS white-matter lesion-up signal;
- no direct single-cell atlas contradiction that overwhelms support;
- either cross-disease genetic anchoring or perturbation/foundation support;
- a plausible intervention route not already blocked by prior V3 audits.

If no gene passes, the output is still useful: it separates a reproducible
state marker from an intervention-grade controller and forces the next pivot
upstream/downstream of the module.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from v3_analyze_direct_h5ad_cell_states import ROOT
from v3_wave85_external_geo_antitnf_validation import bh, hedges_g, markdown_table, rel, residualize, write_json, zscore_rows


SEED = 20260527
OUT = ROOT / "results_v3" / "wave91_lipid_lysosomal_module_intervention_rank"

PSO_TESTS = ROOT / "results_v3" / "wave89_psoriasis_gse85034_response" / "psoriasis_baseline_gene_response_tests.tsv"
PSO_SOURCES = ROOT / "results_v3" / "wave89_psoriasis_gse85034_response" / "candidate_gene_sources.tsv"
IBD_META = ROOT / "results_v3" / "wave86_external_geo_antitnf_gene_driver" / "external_geo_gene_meta_rank.tsv"
RA_COUNTS = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"
MS_WM = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
DIRECT_H5AD = ROOT / "results_v3" / "direct_h5ad_gene_replication" / "direct_h5ad_gene_donor_comparisons.tsv"
W55 = ROOT / "results_v3" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W81 = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"


ROUTE_BLOCKERS: dict[str, str] = {
    "ACSL1": "NO_GO_DEMOTED_TARGET_MARKER_AFTER_MODULE_ADJUSTED_TEST",
    "APOE": "NO_GO_SECRETED_LIPID_CARRIER_MARKER_CNS_AND_SYSTEMIC_LIPID_RISK",
    "AXL": "PARK_TAM_RECEPTOR_DIRECTION_AND_ONCOLOGY_SELECTIVITY_RISK",
    "C1QA": "NO_GO_COMPLEMENT_STATE_MARKER_AND_COMPLEMENT_PRIOR_ART",
    "C1QB": "NO_GO_COMPLEMENT_STATE_MARKER_AND_COMPLEMENT_PRIOR_ART",
    "C1QC": "NO_GO_COMPLEMENT_STATE_MARKER_AND_COMPLEMENT_PRIOR_ART",
    "CCL2": "NO_GO_BROAD_CHEMOKINE_REDUNDANCY_AND_PRIOR_ART",
    "CCL3": "NO_GO_BROAD_CHEMOKINE_REDUNDANCY",
    "CCL4": "NO_GO_BROAD_CHEMOKINE_REDUNDANCY",
    "CD36": "NO_GO_SYSTEMIC_LIPID_UPTAKE_RECEPTOR_LOW_SELECTIVITY",
    "CD44": "NO_GO_ADHESION_MATRIX_PRIOR_ART_AND_BROAD_BIOLOGY",
    "CD74": "NO_GO_BROAD_ANTIGEN_PRESENTATION_AXIS",
    "CTSB": "NO_GO_BROAD_CATHEPSIN_HOST_DEFENSE_AND_PROTEASE_SELECTIVITY",
    "CTSD": "NO_GO_BROAD_LYSOSOMAL_PROTEASE_HOST_DEFENSE",
    "CTSL": "NO_GO_BROAD_CATHEPSIN_HOST_DEFENSE_AND_PROTEASE_SELECTIVITY",
    "CTSS": "NO_GO_CATHEPSIN_S_PRIOR_AUDITED_HOST_DEFENSE_AND_PRIOR_ART",
    "CXCL8": "NO_GO_GENERIC_NEUTROPHIL_CHEMOKINE_LOW_MS_ANCHOR",
    "CXCL10": "NO_GO_GENERIC_IFN_CHEMOKINE_AXIS",
    "CXCR4": "NO_GO_BROAD_TRAFFICKING_AXIS_AND_EXISTING_AUTOIMMUNE_PRIOR_ART",
    "FABP5": "PARK_INTRACELLULAR_LIPID_CHAPERONE_SELECTIVITY_AND_CNS_ROUTE_UNRESOLVED",
    "GBP1": "NO_GO_IFN_MARKER_NOT_DRUGGABLE_CONTROLLER",
    "GPNMB": "PARK_MARKER_REPAIR_STATE_WITH_ONCOLOGY_ADC_PRECEDENT_BUT_WEAK_CAUSALITY",
    "HLA-DRA": "NO_GO_BROAD_MHC_CLASS_II",
    "HLA-DRB1": "NO_GO_BROAD_MHC_CLASS_II_AND_HLA_RISK_TAG",
    "IFI30": "NO_GO_DIRECT_ANTIGEN_PROCESSING_HOST_DEFENSE_AND_POOR_DRUGGABILITY",
    "IL1B": "NO_GO_GENERIC_IL1_INFLAMMATION_AND_EXISTING_IL1_BLOCKADE_PRIOR_ART",
    "LAMP1": "NO_GO_LYSOSOMAL_MARKER_NOT_INTERVENTION_CONTROLLER",
    "LAMP2": "NO_GO_LYSOSOMAL_MARKER_AUTOPHAGY_SYSTEMIC_RISK",
    "LAMP3": "NO_GO_DENDRITIC_LYSOSOMAL_MARKER_NOT_INTERVENTION_POINT",
    "LIPA": "PARK_LYSOSOMAL_ACID_LIPASE_BIOLOGY_INTERESTING_BUT_PRIOR_W81_NO_REOPEN",
    "LPL": "NO_GO_DIRECT_SYSTEMIC_LIPOLYSIS_TARGET_MARKER_ONLY",
    "MARCO": "PARK_SCAVENGER_RECEPTOR_HOST_DEFENSE_AND_TISSUE_SELECTIVITY_UNRESOLVED",
    "MERTK": "PARK_TAM_EFFEROCYTOSIS_RECEPTOR_DIRECTION_AND_AGONISM_ROUTE_UNRESOLVED",
    "MSR1": "PARK_SCAVENGER_RECEPTOR_HOST_DEFENSE_AND_TISSUE_SELECTIVITY_UNRESOLVED",
    "NFKBIA": "NO_GO_GENERIC_NFKB_FEEDBACK_AXIS",
    "OSM": "NO_GO_OSM_OSMR_IBD_RA_PRIOR_ART_AND_MS_DIRECTION_AMBIGUITY",
    "PLIN2": "NO_GO_LIPID_DROPLET_MARKER_NOT_CONTROLLER",
    "SPP1": "NO_GO_OSTEOPONTIN_CD44_PRIOR_ART_AND_WEAK_SINGLE_GENE_MS",
    "STAT1": "NO_GO_GENERIC_IFN_TRANSCRIPTION_AXIS",
    "TREM1": "PARK_RECEPTOR_ROUTE_BUT_NO_LOCAL_MS_OR_GENETIC_ANCHOR",
    "TREM2": "PARK_REPAIR_PHAGOCYTOSIS_RECEPTOR_DIRECTION_AND_CNS_SELECTIVITY_UNRESOLVED",
    "TNF": "NO_GO_EXISTING_ANTI_TNF_MS_RISK_AND_PRIOR_ART",
}


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def log_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0).replace(0, np.nan)
    return np.log2(counts.div(lib, axis=1) * 1_000_000.0 + 1.0)


def auc_score(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    pos = score[y == 1]
    neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    wins = 0.0
    for value in pos:
        wins += float((value > neg).sum())
        wins += 0.5 * float((value == neg).sum())
    return wins / float(len(pos) * len(neg))


def candidate_genes() -> list[str]:
    genes: set[str] = set()
    if PSO_TESTS.exists():
        pso = read_tsv(PSO_TESTS)
        genes.update(pso.loc[pso["feature_class"].eq("gene"), "feature"].astype(str).str.upper().tolist())
    if PSO_SOURCES.exists():
        src = read_tsv(PSO_SOURCES)
        genes.update(src["gene"].astype(str).str.upper().tolist())
    return sorted(g for g in genes if g and g != "NAN")


def test_ra_response(genes: list[str]) -> pd.DataFrame:
    if not RA_COUNTS.exists() or not RA_META.exists():
        return pd.DataFrame({"gene": genes})
    counts = read_tsv(RA_COUNTS).set_index("GeneSymbol")
    counts.index = counts.index.astype(str).str.upper()
    meta = read_tsv(RA_META)
    pre = meta[meta["timepoint"].astype(str).str.lower().eq("pre")].copy()
    expr = zscore_rows(log_cpm(counts))
    pre = pre[pre["count_column"].isin(expr.columns)].copy()
    pre["response"] = pre["responder_moderate_or_good"].astype(str).str.lower().isin(["true", "1", "yes"]).astype(int)
    pre = pre[pre["response"].isin([0, 1])].copy()

    rows: list[dict[str, Any]] = []
    for gene in genes:
        if gene not in expr.index:
            rows.append({"gene": gene, "ra_available": False, "ra_call": "MISSING"})
            continue
        score = expr.loc[gene, pre["count_column"].tolist()].astype(float).to_numpy()
        ok = np.isfinite(score)
        use = pre.loc[ok].copy()
        if len(use) < 8 or use["response"].nunique() < 2:
            rows.append({"gene": gene, "ra_available": True, "ra_call": "INSUFFICIENT"})
            continue
        adjusted = residualize(score[ok], use, ["pathotype", "biologic", "inflammatory_score", "das28_score"])
        y = use["response"].astype(int).to_numpy()
        responders = adjusted[y == 1]
        nonresponders = adjusted[y == 0]
        t_stat, p_value = stats.ttest_ind(responders, nonresponders, equal_var=False, nan_policy="omit")
        effect = float(np.nanmean(responders) - np.nanmean(nonresponders))
        auc_response = auc_score(y, adjusted)
        rows.append(
            {
                "gene": gene,
                "ra_available": True,
                "ra_n_subjects": int(len(use)),
                "ra_n_responders": int(y.sum()),
                "ra_n_nonresponders": int((1 - y).sum()),
                "ra_effect_responder_minus_non": effect,
                "ra_hedges_g_responder_minus_non": hedges_g(responders, nonresponders),
                "ra_auc_high_score_nonresponse": float(1.0 - auc_response) if np.isfinite(auc_response) else np.nan,
                "ra_p": float(p_value) if np.isfinite(p_value) else 1.0,
                "ra_nonresponse_high": bool(effect < 0),
                "ra_call": "NONRESPONSE_HIGH_NOMINAL"
                if effect < 0 and p_value < 0.05
                else ("NONRESPONSE_HIGH_TREND" if effect < 0 and p_value < 0.20 else ("NONRESPONSE_HIGH_WEAK" if effect < 0 else "NO_SUPPORT")),
            }
        )
    out = pd.DataFrame(rows)
    if "ra_p" in out.columns:
        out["ra_fdr_candidate_genes"] = bh(pd.to_numeric(out["ra_p"], errors="coerce").fillna(1.0).to_numpy())
    return out


def psoriasis_response(genes: list[str]) -> pd.DataFrame:
    pso = read_tsv(PSO_TESTS)
    if pso.empty:
        return pd.DataFrame({"gene": genes})
    ada = pso[(pso["treatment"].eq("ADA")) & (pso["feature_class"].eq("gene"))].copy()
    ada["gene"] = ada["feature"].astype(str).str.upper()
    keep = ada[ada["gene"].isin(genes)].copy()
    keep = keep.rename(
        columns={
            "hedges_g_responder_minus_non": "psoriasis_ada_hedges_g_responder_minus_non",
            "effect_responder_minus_non": "psoriasis_ada_effect_responder_minus_non",
            "auc_high_score_nonresponse": "psoriasis_ada_auc_high_score_nonresponse",
            "p": "psoriasis_ada_p",
            "fdr_within_treatment": "psoriasis_ada_fdr",
            "nonresponse_high_direction": "psoriasis_ada_nonresponse_high",
        }
    )
    keep["psoriasis_ada_call"] = np.where(
        keep["psoriasis_ada_nonresponse_high"].astype(bool) & (pd.to_numeric(keep["psoriasis_ada_p"], errors="coerce") < 0.05),
        "NONRESPONSE_HIGH_NOMINAL",
        np.where(
            keep["psoriasis_ada_nonresponse_high"].astype(bool) & (pd.to_numeric(keep["psoriasis_ada_p"], errors="coerce") < 0.20),
            "NONRESPONSE_HIGH_TREND",
            np.where(keep["psoriasis_ada_nonresponse_high"].astype(bool), "NONRESPONSE_HIGH_WEAK", "NO_SUPPORT"),
        ),
    )
    cols = [
        "gene",
        "n_subjects",
        "n_pasi75_responders",
        "n_pasi75_nonresponders",
        "psoriasis_ada_effect_responder_minus_non",
        "psoriasis_ada_hedges_g_responder_minus_non",
        "psoriasis_ada_auc_high_score_nonresponse",
        "psoriasis_ada_p",
        "psoriasis_ada_fdr",
        "psoriasis_ada_nonresponse_high",
        "psoriasis_ada_call",
    ]
    out = keep[[c for c in cols if c in keep.columns]].copy()
    out = out.rename(
        columns={
            "n_subjects": "psoriasis_ada_n_subjects",
            "n_pasi75_responders": "psoriasis_ada_n_responders",
            "n_pasi75_nonresponders": "psoriasis_ada_n_nonresponders",
        }
    )
    return out


def ibd_response(genes: list[str]) -> pd.DataFrame:
    ibd = read_tsv(IBD_META)
    if ibd.empty:
        return pd.DataFrame({"gene": genes})
    ibd["gene"] = ibd["gene"].astype(str).str.upper()
    keep = ibd[ibd["gene"].isin(genes)].copy()
    keep = keep.rename(
        columns={
            "weighted_mean_hedges_g_responder_minus_non": "ibd_weighted_hedges_g_responder_minus_non",
            "median_auc_high_score_nonresponse": "ibd_median_auc_high_score_nonresponse",
            "min_p": "ibd_min_p",
            "call": "ibd_wave86_call",
        }
    )
    keep["ibd_nonresponse_high"] = pd.to_numeric(keep["ibd_weighted_hedges_g_responder_minus_non"], errors="coerce") < 0
    keep["ibd_call"] = np.where(
        keep["ibd_nonresponse_high"].astype(bool) & (pd.to_numeric(keep["ibd_min_p"], errors="coerce") < 0.05),
        "NONRESPONSE_HIGH_NOMINAL",
        np.where(keep["ibd_nonresponse_high"].astype(bool), "NONRESPONSE_HIGH_WEAK", "NO_SUPPORT"),
    )
    cols = [
        "gene",
        "modules",
        "n_primary_contexts",
        "nonresponse_high_contexts",
        "responder_high_contexts",
        "nominal_nonresponse_contexts_p_lt_0_05",
        "fdr10_nonresponse_contexts",
        "ibd_weighted_hedges_g_responder_minus_non",
        "ibd_median_auc_high_score_nonresponse",
        "ibd_min_p",
        "best_context",
        "ibd_wave86_call",
        "ibd_nonresponse_high",
        "ibd_call",
    ]
    return keep[[c for c in cols if c in keep.columns]].copy()


def ms_white_matter(genes: list[str]) -> pd.DataFrame:
    ms = read_tsv(MS_WM)
    if ms.empty:
        return pd.DataFrame({"gene": genes})
    ms["gene"] = ms["gene"].astype(str).str.upper()
    keep = ms[ms["gene"].isin(genes)].copy()
    keep = keep.rename(
        columns={
            "delta_log2": "ms_wm_delta_log2",
            "hedges_g": "ms_wm_hedges_g",
            "p": "ms_wm_p",
            "fdr": "ms_wm_fdr",
        }
    )
    keep["ms_wm_positive_nominal"] = (pd.to_numeric(keep["ms_wm_delta_log2"], errors="coerce") > 0) & (pd.to_numeric(keep["ms_wm_p"], errors="coerce") < 0.05)
    keep["ms_wm_negative_nominal"] = (pd.to_numeric(keep["ms_wm_delta_log2"], errors="coerce") < 0) & (pd.to_numeric(keep["ms_wm_p"], errors="coerce") < 0.05)
    keep["ms_wm_call"] = np.where(
        keep["ms_wm_positive_nominal"],
        "MS_WM_UP_NOMINAL",
        np.where(keep["ms_wm_negative_nominal"], "MS_WM_DOWN_NOMINAL", "MS_WM_NULL_OR_WEAK"),
    )
    cols = ["gene", "ms_wm_delta_log2", "ms_wm_hedges_g", "ms_wm_p", "ms_wm_fdr", "ms_wm_positive_nominal", "ms_wm_negative_nominal", "ms_wm_call"]
    return keep[[c for c in cols if c in keep.columns]].copy()


def direct_h5ad_summary(genes: list[str]) -> pd.DataFrame:
    direct = read_tsv(DIRECT_H5AD)
    if direct.empty:
        return pd.DataFrame({"gene": genes})
    direct["gene"] = direct["gene"].astype(str).str.upper()
    direct = direct[(direct["gene"].isin(genes)) & (direct["metric"].eq("mean_z_vs_controls"))].copy()
    rows: list[dict[str, Any]] = []
    for gene, sub in direct.groupby("gene", sort=False):
        pos = sub[(pd.to_numeric(sub["delta_case_minus_control"], errors="coerce") > 0) & (pd.to_numeric(sub["p"], errors="coerce") < 0.05)]
        neg = sub[(pd.to_numeric(sub["delta_case_minus_control"], errors="coerce") < 0) & (pd.to_numeric(sub["p"], errors="coerce") < 0.05)]
        pos_fdr = sub[(pd.to_numeric(sub["delta_case_minus_control"], errors="coerce") > 0) & (pd.to_numeric(sub["fdr"], errors="coerce") < 0.10)]
        neg_fdr = sub[(pd.to_numeric(sub["delta_case_minus_control"], errors="coerce") < 0) & (pd.to_numeric(sub["fdr"], errors="coerce") < 0.10)]
        top_pos = pos.sort_values("p").head(3).copy()
        top_neg = neg.sort_values("p").head(3).copy()
        rows.append(
            {
                "gene": gene,
                "direct_h5ad_contexts": int(len(sub)),
                "direct_positive_p05_disease_count": int(pos["disease_name"].nunique()),
                "direct_positive_p05_diseases": ";".join(sorted(pos["disease_name"].unique())),
                "direct_negative_p05_disease_count": int(neg["disease_name"].nunique()),
                "direct_negative_p05_diseases": ";".join(sorted(neg["disease_name"].unique())),
                "direct_positive_fdr10_disease_count": int(pos_fdr["disease_name"].nunique()),
                "direct_negative_fdr10_disease_count": int(neg_fdr["disease_name"].nunique()),
                "direct_top_positive_contexts": ";".join(
                    (top_pos["analysis"].astype(str) + ":" + top_pos["delta_case_minus_control"].round(3).astype(str) + ",p=" + top_pos["p"].map(lambda x: f"{x:.3g}")).tolist()
                ),
                "direct_top_negative_contexts": ";".join(
                    (top_neg["analysis"].astype(str) + ":" + top_neg["delta_case_minus_control"].round(3).astype(str) + ",p=" + top_neg["p"].map(lambda x: f"{x:.3g}")).tolist()
                ),
            }
        )
    return pd.DataFrame(rows)


def prior_evidence(genes: list[str]) -> pd.DataFrame:
    base = pd.DataFrame({"gene": genes})
    w55 = read_tsv(W55)
    if not w55.empty:
        w55["gene"] = w55["gene"].astype(str).str.upper()
        cols = [
            "gene",
            "wave55_score",
            "n_diseases_genetic_ge_0_25",
            "diseases_genetic_ge_0_25",
            "n_diseases_genetic_ge_0_5",
            "diseases_genetic_ge_0_5",
            "ms_genetic_association",
            "ms_overall_score",
            "strict_residual_disease_count",
            "foundation_recommendation",
        ]
        base = base.merge(w55[w55["gene"].isin(genes)][[c for c in cols if c in w55.columns]], on="gene", how="left")
    w62 = read_tsv(W62)
    if not w62.empty:
        w62["gene"] = w62["gene"].astype(str).str.upper()
        cols = [
            "gene",
            "wave62_score",
            "wave62_call",
            "manual_blocker",
            "strong_l2g_disease_count",
            "strong_l2g_diseases",
            "ms_max_l2g_score",
            "strong_qtl_coloc_disease_count",
            "strong_qtl_coloc_diseases",
            "chembl_target_id",
            "druggable_activity_count",
            "wave61_best_call",
            "wave61_best_manual_blocker",
        ]
        base = base.merge(w62[w62["gene"].isin(genes)][[c for c in cols if c in w62.columns]], on="gene", how="left")
    w81 = read_tsv(W81)
    if not w81.empty:
        w81["gene"] = w81["gene"].astype(str).str.upper()
        cols = [
            "gene",
            "wave81_call",
            "direct_perturbation",
            "foundation_model_support",
            "direct_perturbation_detail",
            "foundation_model_detail",
            "wave71_call",
            "decision_reason",
        ]
        base = base.merge(w81[w81["gene"].isin(genes)][[c for c in cols if c in w81.columns]], on="gene", how="left")
    return base


def classify(row: pd.Series) -> str:
    response_contexts = int(row.get("response_nonresponse_high_context_count", 0) or 0)
    response_nominal = int(row.get("response_nominal_or_trend_context_count", 0) or 0)
    ms_positive = bool(row.get("ms_wm_positive_nominal", False))
    direct_neg = int(row.get("direct_negative_p05_disease_count", 0) or 0)
    direct_pos = int(row.get("direct_positive_p05_disease_count", 0) or 0)
    genetic = int(row.get("n_diseases_genetic_ge_0_25", 0) or 0) if not pd.isna(row.get("n_diseases_genetic_ge_0_25", np.nan)) else 0
    l2g = int(row.get("strong_l2g_disease_count", 0) or 0) if not pd.isna(row.get("strong_l2g_disease_count", np.nan)) else 0
    qtl = int(row.get("strong_qtl_coloc_disease_count", 0) or 0) if not pd.isna(row.get("strong_qtl_coloc_disease_count", np.nan)) else 0
    direct_perturb = int(row.get("direct_perturbation", 0) or 0) if not pd.isna(row.get("direct_perturbation", np.nan)) else 0
    fm_support = int(row.get("foundation_model_support", 0) or 0) if not pd.isna(row.get("foundation_model_support", np.nan)) else 0
    druggable = bool(str(row.get("chembl_target_id", "")).strip()) or (float(row.get("druggable_activity_count", 0) or 0) > 0)
    blocker = str(row.get("route_blocker", ""))

    if response_contexts < 2:
        return "NO_GO_RESPONSE_SIGNAL_NOT_SHARED_ACROSS_DISEASES"
    if response_nominal < 1:
        return "PARK_RESPONSE_DIRECTIONS_WEAK_OR_UNDERPOWERED"
    if not ms_positive:
        return "NO_GO_NO_MS_WHITE_MATTER_SINGLE_GENE_ANCHOR"
    if direct_neg > 0 and direct_neg >= direct_pos:
        return "NO_GO_DIRECT_ATLAS_CONTRADICTION"
    if blocker.startswith("NO_GO"):
        return "NO_GO_ROUTE_BLOCKED"
    if (genetic + l2g + qtl) < 2 and (direct_perturb + fm_support) == 0:
        return "PARK_NO_CAUSAL_OR_PERTURBATION_ANCHOR"
    if not druggable and blocker.startswith("PARK"):
        return "PARK_BIOLOGY_INTERESTING_BUT_ROUTE_UNRESOLVED"
    if not druggable:
        return "NO_GO_NO_DRUGGABLE_HANDLE"
    if blocker.startswith("PARK"):
        return "PARK_ROUTE_STILL_UNRESOLVED_DESPITE_CONVERGENCE"
    return "REOPEN_LIPID_LYSOSOMAL_INTERVENTION_NODE"


def build_rank() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    genes = candidate_genes()
    if not genes:
        raise RuntimeError("No candidate genes found from Wave89 inputs")

    ra = test_ra_response(genes)
    pso = psoriasis_response(genes)
    ibd = ibd_response(genes)
    ms = ms_white_matter(genes)
    direct = direct_h5ad_summary(genes)
    prior = prior_evidence(genes)

    rows = pd.DataFrame({"gene": genes})
    for table in [ibd, ra, pso, ms, direct, prior]:
        if not table.empty:
            rows = rows.merge(table, on="gene", how="left")

    bool_cols = ["ibd_nonresponse_high", "ra_nonresponse_high", "psoriasis_ada_nonresponse_high", "ms_wm_positive_nominal"]
    for col in bool_cols:
        if col in rows.columns:
            rows[col] = rows[col].fillna(False).astype(bool)
    count_cols = [
        "direct_positive_p05_disease_count",
        "direct_negative_p05_disease_count",
        "direct_positive_fdr10_disease_count",
        "direct_negative_fdr10_disease_count",
        "n_diseases_genetic_ge_0_25",
        "strong_l2g_disease_count",
        "strong_qtl_coloc_disease_count",
        "direct_perturbation",
        "foundation_model_support",
        "druggable_activity_count",
        "nonresponse_high_contexts",
        "nominal_nonresponse_contexts_p_lt_0_05",
        "fdr10_nonresponse_contexts",
    ]
    for col in count_cols:
        if col in rows.columns:
            rows[col] = pd.to_numeric(rows[col], errors="coerce").fillna(0)

    rows["response_nonresponse_high_context_count"] = (
        rows.get("ibd_nonresponse_high", False).astype(int)
        + rows.get("ra_nonresponse_high", False).astype(int)
        + rows.get("psoriasis_ada_nonresponse_high", False).astype(int)
    )
    rows["response_nominal_or_trend_context_count"] = (
        rows.get("ibd_call", "").isin(["NONRESPONSE_HIGH_NOMINAL"]).astype(int)
        + rows.get("ra_call", "").isin(["NONRESPONSE_HIGH_NOMINAL", "NONRESPONSE_HIGH_TREND"]).astype(int)
        + rows.get("psoriasis_ada_call", "").isin(["NONRESPONSE_HIGH_NOMINAL", "NONRESPONSE_HIGH_TREND"]).astype(int)
    )
    effect_cols = [
        "ibd_weighted_hedges_g_responder_minus_non",
        "ra_hedges_g_responder_minus_non",
        "psoriasis_ada_hedges_g_responder_minus_non",
    ]
    rows["response_mean_hedges_g_responder_minus_non"] = rows[[c for c in effect_cols if c in rows.columns]].apply(lambda x: float(np.nanmean(pd.to_numeric(x, errors="coerce"))) if pd.to_numeric(x, errors="coerce").notna().any() else np.nan, axis=1)
    rows["response_effect_sd"] = rows[[c for c in effect_cols if c in rows.columns]].apply(lambda x: float(np.nanstd(pd.to_numeric(x, errors="coerce"), ddof=1)) if pd.to_numeric(x, errors="coerce").notna().sum() > 1 else np.nan, axis=1)
    rows["route_blocker"] = rows["gene"].map(ROUTE_BLOCKERS).fillna("UNSPECIFIED_ROUTE_NOT_AUDITED")
    rows["wave91_call"] = rows.apply(classify, axis=1)

    rows["module_intervention_score"] = (
        rows["response_nonresponse_high_context_count"].astype(float) * 2.0
        + rows["response_nominal_or_trend_context_count"].astype(float) * 1.5
        + np.where(rows["ms_wm_positive_nominal"], 2.0, 0.0)
        + rows.get("direct_positive_p05_disease_count", 0).astype(float) * 1.0
        - rows.get("direct_negative_p05_disease_count", 0).astype(float) * 1.5
        + rows.get("n_diseases_genetic_ge_0_25", 0).astype(float) * 0.5
        + rows.get("strong_l2g_disease_count", 0).astype(float) * 0.5
        + rows.get("strong_qtl_coloc_disease_count", 0).astype(float) * 0.5
        + rows.get("direct_perturbation", 0).astype(float) * 1.0
        + rows.get("foundation_model_support", 0).astype(float) * 1.0
        + np.where(rows["route_blocker"].str.startswith("PARK"), -1.0, 0.0)
        + np.where(rows["route_blocker"].str.startswith("NO_GO"), -4.0, 0.0)
    )

    rank = rows.sort_values(["wave91_call", "module_intervention_score"], ascending=[True, False]).copy()
    display_rank = rows.sort_values("module_intervention_score", ascending=False).copy()

    ra.to_csv(OUT / "ra_all_candidate_response_tests.tsv", sep="\t", index=False)
    rows.to_csv(OUT / "module_wide_evidence_matrix.tsv", sep="\t", index=False)
    display_rank.to_csv(OUT / "lipid_lysosomal_intervention_rank.tsv", sep="\t", index=False)

    reopened = rows[rows["wave91_call"].eq("REOPEN_LIPID_LYSOSOMAL_INTERVENTION_NODE")].copy()
    parked = rows[rows["wave91_call"].str.startswith("PARK", na=False)].copy()
    summary = {
        "seed": SEED,
        "analysis_call": "NO_REOPEN_MODULE_WIDE_LIPID_LYSOSOMAL_INTERVENTION_NODE" if reopened.empty else "REOPEN_MODULE_WIDE_CANDIDATE",
        "n_candidate_genes": int(len(genes)),
        "n_reopened": int(len(reopened)),
        "n_parked": int(len(parked)),
        "top_scored_gene": str(display_rank.iloc[0]["gene"]) if not display_rank.empty else "",
        "top_scored_call": str(display_rank.iloc[0]["wave91_call"]) if not display_rank.empty else "",
        "call_counts": {str(k): int(v) for k, v in rows["wave91_call"].value_counts().to_dict().items()},
        "inputs": {
            "psoriasis_response": rel(PSO_TESTS),
            "psoriasis_candidate_sources": rel(PSO_SOURCES),
            "ibd_external_antitnf_meta": rel(IBD_META),
            "ra_counts": rel(RA_COUNTS),
            "ra_metadata": rel(RA_META),
            "ms_white_matter_signature": rel(MS_WM),
            "direct_h5ad_donor_comparisons": rel(DIRECT_H5AD),
            "wave55_external_genetics": rel(W55),
            "wave62_target_resolution": rel(W62),
            "wave81_perturbation_first_rescue": rel(W81),
        },
    }
    write_json(OUT / "summary.json", summary)

    selected = [
        "gene",
        "module_intervention_score",
        "wave91_call",
        "route_blocker",
        "response_nonresponse_high_context_count",
        "response_nominal_or_trend_context_count",
        "response_mean_hedges_g_responder_minus_non",
        "response_effect_sd",
        "ibd_weighted_hedges_g_responder_minus_non",
        "ra_hedges_g_responder_minus_non",
        "psoriasis_ada_hedges_g_responder_minus_non",
        "ms_wm_delta_log2",
        "ms_wm_p",
        "ms_wm_call",
        "direct_positive_p05_disease_count",
        "direct_positive_p05_diseases",
        "direct_negative_p05_disease_count",
        "direct_negative_p05_diseases",
        "n_diseases_genetic_ge_0_25",
        "diseases_genetic_ge_0_25",
        "strong_l2g_disease_count",
        "strong_qtl_coloc_disease_count",
        "chembl_target_id",
        "druggable_activity_count",
        "wave62_call",
        "wave81_call",
        "direct_perturbation",
        "foundation_model_support",
    ]
    available = [c for c in selected if c in display_rank.columns]
    report = [
        "# Wave91 Lipid/Lysosomal Module Intervention-Rank Audit",
        "",
        f"Analysis call: `{summary['analysis_call']}`.",
        "",
        "## Question",
        "",
        "After LPL was parked as a marker, can any neighboring lipid/lysosomal/autoinflammatory gene become an intervention-grade cross-autoimmune node?",
        "",
        "## Top Evidence-Ranked Genes",
        "",
        markdown_table(display_rank[available], max_rows=35),
        "",
        "## Strict Call Counts",
        "",
        markdown_table(pd.DataFrame(sorted(summary["call_counts"].items()), columns=["wave91_call", "n_genes"]), max_rows=30),
        "",
        "## Interpretation",
        "",
        "- No candidate is allowed to advance on response-direction rank alone.",
        "- A direct module member must also survive MS lesion anchoring, atlas consistency, causal/perturbation support, and a plausible non-blocked intervention route.",
        "- The highest response/state markers remain biologically informative, but the intervention handle likely sits upstream or downstream of the measured lipid-loader state rather than inside the marker set itself.",
    ]
    if not reopened.empty:
        report.extend(["", "## Reopened Candidates", "", markdown_table(reopened[available], max_rows=20)])
    if not parked.empty:
        report.extend(["", "## Parked Candidates", "", markdown_table(parked.sort_values("module_intervention_score", ascending=False)[available], max_rows=20)])
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    np.random.seed(SEED)
    summary = build_rank()
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
