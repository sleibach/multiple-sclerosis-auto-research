#!/usr/bin/env python3
"""Wave100 cAMP-restoration intervention-class forcing audit.

Wave99 closed the C15ORF48-proximal branch for therapeutic nomination.
This wave tests a broader intervention-first idea that repeatedly resurfaced
as a near-miss: restore anti-inflammatory cAMP signaling in lipid-lysosomal
myeloid states.

Guardrail: "cAMP is anti-inflammatory" is too broad to nominate a target.
Promotion requires a specific route with cross-disease local state support,
MS anchoring, target-resolved genetics, real perturbation or class reversal
evidence, a feasible modality, clear direction, and no blocking prior art.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave100_camp_restoration_class_audit"

MS_WM = ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv"
BROAD_RAW = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
BROAD_RESID = ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
W55 = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W62 = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W68 = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
W37 = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W18 = ROOT / "phases/v3/results" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv"
W96 = ROOT / "phases/v3/results" / "wave96_c15orf48_controller_search" / "contrast_state_rank_all.tsv"
W96_DONOR = ROOT / "phases/v3/results" / "wave96_c15orf48_controller_search" / "donor_level_c15_costate_summary.tsv"
W28 = ROOT / "phases/v3/results" / "wave28_target_first_rescue" / "target_first_rescue_matrix.tsv"
W50_SUMMARY = ROOT / "phases/v3/results" / "wave50_gpr65_acid_sensing_gpcr_audit" / "summary.json"
PDE4_L1000 = ROOT / "phases/v3/results" / "pde4_camp_l1000_audit_summary.json"


CANDIDATES: dict[str, dict[str, Any]] = {
    "ADCY3": {
        "route": "ADCY3_positive_modulation",
        "class": "adenylyl_cyclase_generation",
        "desired_effect": "increase local cAMP production if reduced ADCY3 activity is causal",
        "modality": "no ADCY3-selective clinical positive modulator identified in local evidence",
        "manual_modality_ready": False,
        "manual_prior_blocked": False,
        "manual_safety_blocked": False,
        "manual_direction_clear": False,
        "manual_note": "nominal MS expression and broad genetics make it a biology clue, but gene-high disease expression is not proof that activation is beneficial",
    },
    "GPR65": {
        "route": "GPR65_acidic_tissue_cAMP_PAM",
        "class": "acid_sensing_gpcr",
        "desired_effect": "positive allosteric modulation or agonism at acidic inflammatory pH",
        "modality": "GPCR small molecule agonist/PAM feasible",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": False,
        "manual_direction_clear": False,
        "manual_note": "prior V3 GPR65 audit found direct autoimmune/IBD prior art and weak or contradictory local disease-cell support",
    },
    "PDE4B": {
        "route": "PDE4B_selective_inhibition",
        "class": "cAMP_degradation_blockade",
        "desired_effect": "raise cAMP by inhibiting PDE4B in inflammatory myeloid cells",
        "modality": "PDE4 inhibitor chemistry exists; isoform-selective disease delivery unresolved",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": True,
        "manual_direction_clear": True,
        "manual_note": "reachable pharmacology but class is crowded and local MS direction is not disease-high",
    },
    "PDE4D": {
        "route": "PDE4D_selective_or_sparing_inhibition",
        "class": "cAMP_degradation_blockade",
        "desired_effect": "raise cAMP while avoiding PDE4D-emesis liabilities",
        "modality": "PDE4 chemistry exists; selectivity and tolerability are limiting",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": True,
        "manual_direction_clear": True,
        "manual_note": "accessible but not supported by local MS/cross-disease signal and has known class liabilities",
    },
    "PTGER4": {
        "route": "EP4_contextual_modulation",
        "class": "prostanoid_gpcr_cAMP",
        "desired_effect": "context-specific EP4 signaling modulation",
        "modality": "EP4 ligands exist",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": False,
        "manual_direction_clear": False,
        "manual_note": "excellent genetics but prostaglandin direction is tissue-dependent and prior V3 marked EP4 direction/prior art as blocking",
    },
    "ADORA2A": {
        "route": "A2A_adenosine_agonism",
        "class": "purinergic_gpcr_cAMP",
        "desired_effect": "agonize anti-inflammatory adenosine receptor signaling",
        "modality": "adenosine receptor agonists exist",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": True,
        "manual_direction_clear": True,
        "manual_note": "anti-inflammatory logic is known but broad cardiovascular/CNS and immunosuppressive liabilities block a cross-autoimmune claim here",
    },
    "ADORA2B": {
        "route": "A2B_adenosine_modulation",
        "class": "purinergic_gpcr_cAMP",
        "desired_effect": "modulate adenosine signaling in inflamed tissue",
        "modality": "adenosine receptor ligands exist",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": True,
        "manual_direction_clear": False,
        "manual_note": "A2B biology is context-dependent and not anchored in local MS/cross-disease signal",
    },
    "HCAR2": {
        "route": "HCAR2_agonism",
        "class": "hydroxycarboxylic_acid_gpcr",
        "desired_effect": "agonize HCAR2/GPR109A-like anti-inflammatory signaling",
        "modality": "niacin/fumarate-adjacent pharmacology exists",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": False,
        "manual_direction_clear": True,
        "manual_note": "route is crowded by niacin/fumarate-adjacent MS and inflammatory literature and lacks local disease-state support",
    },
    "HCAR3": {
        "route": "HCAR3_agonism",
        "class": "hydroxycarboxylic_acid_gpcr",
        "desired_effect": "agonize HCAR3 if it controls myeloid lipid-inflammatory state",
        "modality": "GPCR route plausible but less mature than HCAR2",
        "manual_modality_ready": False,
        "manual_prior_blocked": False,
        "manual_safety_blocked": False,
        "manual_direction_clear": False,
        "manual_note": "less prior-crowded than HCAR2 but lacks disease-cell, MS, genetics, and perturbation support",
    },
    "FFAR2": {
        "route": "FFAR2_SCFA_receptor_modulation",
        "class": "microbial_metabolite_gpcr_cAMP",
        "desired_effect": "modulate SCFA receptor signaling in inflammatory myeloid cells",
        "modality": "GPCR/metabolite route plausible",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": False,
        "manual_direction_clear": False,
        "manual_note": "microbiome/SCFA autoimmunity is crowded and local target-level support is absent",
    },
}


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


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


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    text = clean(value).strip().lower()
    return text in {"1", "true", "yes", "y"}


def first_row(df: pd.DataFrame, gene: str, col: str = "gene") -> pd.Series | None:
    if df.empty or col not in df.columns:
        return None
    sub = df[df[col].astype(str).str.upper().eq(gene.upper())]
    if sub.empty:
        return None
    return sub.iloc[0]


def best_w68(df: pd.DataFrame, gene: str) -> pd.Series | None:
    if df.empty or "gene" not in df.columns:
        return None
    sub = df[df["gene"].astype(str).str.upper().eq(gene.upper())].copy()
    if sub.empty:
        return None
    sub["_fdr"] = pd.to_numeric(sub.get("remission_adjusted_fdr", np.nan), errors="coerce").fillna(1.0)
    sub["_p"] = pd.to_numeric(sub.get("remission_adjusted_p", np.nan), errors="coerce").fillna(1.0)
    sub["_abs_delta"] = pd.to_numeric(sub.get("remission_adjusted_delta", 0.0), errors="coerce").abs().fillna(0.0)
    return sub.sort_values(["_fdr", "_p", "_abs_delta"], ascending=[True, True, False]).iloc[0]


def broad_raw_summary(df: pd.DataFrame, gene: str) -> dict[str, Any]:
    if df.empty or "gene" not in df.columns:
        return {
            "raw_positive_disease_count": 0,
            "raw_negative_disease_count": 0,
            "raw_positive_diseases": "",
            "raw_negative_diseases": "",
            "raw_fdr10_positive_disease_count": 0,
            "raw_fdr10_negative_disease_count": 0,
        }
    sub = df[df["gene"].astype(str).str.upper().eq(gene.upper())].copy()
    if sub.empty:
        return {
            "raw_positive_disease_count": 0,
            "raw_negative_disease_count": 0,
            "raw_positive_diseases": "",
            "raw_negative_diseases": "",
            "raw_fdr10_positive_disease_count": 0,
            "raw_fdr10_negative_disease_count": 0,
        }
    sub["delta"] = pd.to_numeric(sub.get("delta_log2_cpm", np.nan), errors="coerce")
    sub["p_num"] = pd.to_numeric(sub.get("p", np.nan), errors="coerce")
    sub["fdr_num"] = pd.to_numeric(sub.get("fdr", np.nan), errors="coerce")
    pos = sub[(sub["delta"] > 0) & (sub["p_num"] < 0.10)]
    neg = sub[(sub["delta"] < 0) & (sub["p_num"] < 0.10)]
    pos_fdr = sub[(sub["delta"] > 0) & (sub["fdr_num"] <= 0.10)]
    neg_fdr = sub[(sub["delta"] < 0) & (sub["fdr_num"] <= 0.10)]
    return {
        "raw_positive_disease_count": int(pos["disease_name"].nunique()) if "disease_name" in pos.columns else 0,
        "raw_negative_disease_count": int(neg["disease_name"].nunique()) if "disease_name" in neg.columns else 0,
        "raw_positive_diseases": ";".join(sorted(pos["disease_name"].dropna().astype(str).unique())) if "disease_name" in pos.columns else "",
        "raw_negative_diseases": ";".join(sorted(neg["disease_name"].dropna().astype(str).unique())) if "disease_name" in neg.columns else "",
        "raw_fdr10_positive_disease_count": int(pos_fdr["disease_name"].nunique()) if "disease_name" in pos_fdr.columns else 0,
        "raw_fdr10_negative_disease_count": int(neg_fdr["disease_name"].nunique()) if "disease_name" in neg_fdr.columns else 0,
    }


def collect_context_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "gene" not in df.columns:
        return pd.DataFrame()
    genes = set(CANDIDATES)
    keep_cols = [
        "gene",
        "disease_name",
        "compartment",
        "role",
        "n_case_donors",
        "n_control_donors",
        "delta_log2_cpm",
        "hedges_g",
        "p",
        "fdr",
        "positive_nominal",
        "negative_nominal",
        "positive_fdr10",
        "negative_fdr10",
    ]
    cols = [c for c in keep_cols if c in df.columns]
    out = df[df["gene"].astype(str).str.upper().isin(genes)][cols].copy()
    if out.empty:
        return out
    out["abs_delta"] = pd.to_numeric(out.get("delta_log2_cpm", 0.0), errors="coerce").abs()
    return out.sort_values(["gene", "p", "abs_delta"], ascending=[True, True, False]).drop(columns=["abs_delta"])


def collect_rows(tables: dict[str, pd.DataFrame], aux: dict[str, Any]) -> pd.DataFrame:
    l1000 = aux["pde4_l1000"]
    gpr65_summary = aux["gpr65_summary"]
    l1000_core_hits = int(l1000.get("n_l1000_top_hit_rows_matching_core_compounds", 0) or 0)
    l1000_any_hits = int(l1000.get("n_l1000_top_hit_rows_matching_terms", 0) or 0)
    rows: list[dict[str, Any]] = []
    for gene, manual in CANDIDATES.items():
        ms = first_row(tables["ms_wm"], gene)
        broad_resid = first_row(tables["broad_resid"], gene)
        w55 = first_row(tables["w55"], gene)
        w62 = first_row(tables["w62"], gene)
        w68 = best_w68(tables["w68"], gene)
        w37 = first_row(tables["w37"], gene, col="gene_symbol")
        w18 = first_row(tables["w18"], gene)
        w96 = first_row(tables["w96"], gene)
        w96_donor = first_row(tables["w96_donor"], gene)
        w28 = first_row(tables["w28"], gene)
        raw_summary = broad_raw_summary(tables["broad_raw"], gene)

        rec: dict[str, Any] = {
            "gene": gene,
            **manual,
            **raw_summary,
            "ms_delta_log2": num(ms.get("delta_log2")) if ms is not None else math.nan,
            "ms_p": num(ms.get("p"), 1.0) if ms is not None else 1.0,
            "ms_fdr": num(ms.get("fdr"), 1.0) if ms is not None else 1.0,
            "broad_resid_positive_disease_count": num(broad_resid.get("broad_positive_disease_count"), 0.0) if broad_resid is not None else 0.0,
            "broad_resid_negative_disease_count": num(broad_resid.get("broad_negative_disease_count"), 0.0) if broad_resid is not None else 0.0,
            "retained_positive_disease_count": num(broad_resid.get("retained_positive_disease_count"), 0.0) if broad_resid is not None else 0.0,
            "strict_core_covariate_surviving_disease_count": num(broad_resid.get("strict_core_covariate_surviving_disease_count"), 0.0) if broad_resid is not None else 0.0,
            "top_retained_tests": clean(broad_resid.get("top_retained_tests")) if broad_resid is not None else "",
            "wave55_n_genetic_diseases_ge_0_25": num(w55.get("n_diseases_genetic_ge_0_25"), 0.0) if w55 is not None else 0.0,
            "wave55_genetic_diseases_ge_0_25": clean(w55.get("diseases_genetic_ge_0_25")) if w55 is not None else "",
            "wave55_ms_genetic_association": num(w55.get("ms_genetic_association"), 0.0) if w55 is not None else 0.0,
            "wave55_direct_evidence_calls": clean(w55.get("direct_evidence_calls")) if w55 is not None else "",
            "wave62_call": clean(w62.get("wave62_call")) if w62 is not None else "",
            "wave62_manual_blocker": clean(w62.get("manual_blocker")) if w62 is not None else "",
            "wave62_prior_context_blocker": clean(w62.get("prior_context_blocker")) if w62 is not None else "",
            "wave62_strong_l2g_disease_count": num(w62.get("strong_l2g_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_strong_l2g_diseases": clean(w62.get("strong_l2g_diseases")) if w62 is not None else "",
            "wave62_strong_qtl_coloc_disease_count": num(w62.get("strong_qtl_coloc_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_strong_qtl_coloc_diseases": clean(w62.get("strong_qtl_coloc_diseases")) if w62 is not None else "",
            "wave62_relevant_qtl_coloc_disease_count": num(w62.get("relevant_qtl_coloc_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_ms_max_l2g_score": num(w62.get("ms_max_l2g_score"), 0.0) if w62 is not None else 0.0,
            "wave62_ms_max_relevant_qtl_h4": num(w62.get("ms_max_relevant_qtl_h4"), 0.0) if w62 is not None else 0.0,
            "wave68_best_cell_state": clean(w68.get("cell_state")) if w68 is not None else "",
            "wave68_remission_adjusted_delta": num(w68.get("remission_adjusted_delta")) if w68 is not None else math.nan,
            "wave68_remission_adjusted_p": num(w68.get("remission_adjusted_p"), 1.0) if w68 is not None else 1.0,
            "wave68_remission_adjusted_fdr": num(w68.get("remission_adjusted_fdr"), 1.0) if w68 is not None else 1.0,
            "wave68_call": clean(w68.get("wave68_call")) if w68 is not None else "",
            "wave37_screen_call": clean(w37.get("screen_call")) if w37 is not None else "",
            "wave37_contrast_lfc": num(w37.get("median_efficient_minus_noneater_lfc")) if w37 is not None else math.nan,
            "wave37_contrast_fdr": num(w37.get("contrast_fdr"), 1.0) if w37 is not None else 1.0,
            "wave18_recommendation": clean(w18.get("foundation_rescue_recommendation")) if w18 is not None else "",
            "wave18_support_contexts": num(w18.get("total_support_contexts"), 0.0) if w18 is not None else 0.0,
            "wave18_strong_support_contexts": num(w18.get("total_strong_support_contexts"), 0.0) if w18 is not None else 0.0,
            "wave18_direct_evidence_call": clean(w18.get("best_direct_evidence_call")) if w18 is not None else "",
            "wave96_c15_positive_disease_count": num(w96.get("c15_trend_positive_disease_count"), 0.0) if w96 is not None else 0.0,
            "wave96_c15_negative_context_count": num(w96.get("c15_trend_negative_context_count"), 0.0) if w96 is not None else 0.0,
            "wave96_c15_state_pearson_r": num(w96.get("c15_state_pearson_r")) if w96 is not None else math.nan,
            "wave96_c15_state_pearson_p": num(w96.get("c15_state_pearson_p"), 1.0) if w96 is not None else 1.0,
            "wave96_donor_case_positive_disease_count": num(w96_donor.get("donor_case_positive_disease_count"), 0.0) if w96_donor is not None else 0.0,
            "wave28_gate_call": clean(w28.get("gate_call")) if w28 is not None else "",
            "wave28_hard_failures": clean(w28.get("hard_failures")) if w28 is not None else "",
            "wave28_target_first_score": num(w28.get("target_first_score")) if w28 is not None else math.nan,
            "wave28_l1000_non_no_go": boolish(w28.get("l1000_non_no_go")) if w28 is not None else False,
            "wave28_chembl_activity_records": num(w28.get("chembl_activity_records"), 0.0) if w28 is not None else 0.0,
            "wave28_manual_prior_risk": clean(w28.get("manual_prior_risk")) if w28 is not None else "",
            "wave28_manual_blocker": clean(w28.get("manual_blocker")) if w28 is not None else "",
            "class_l1000_metadata_rows": int(l1000.get("n_lincs_metadata_rows_matching_terms", 0) or 0),
            "class_l1000_unique_pert_ids": int(l1000.get("n_lincs_unique_pert_ids_matching_terms", 0) or 0),
            "class_l1000_top_hit_rows_matching_terms": l1000_any_hits,
            "class_l1000_top_hit_rows_matching_core_compounds": l1000_core_hits,
            "class_l1000_core_compounds_present_in_top_hits": ";".join(l1000.get("core_compounds_present_in_l1000_top_hits", []) or []),
            "gpr65_prior_branch_call": gpr65_summary.get("call", "") if gene == "GPR65" else "",
        }
        rows.append(rec)
    return pd.DataFrame(rows)


def add_gates(rank: pd.DataFrame) -> pd.DataFrame:
    rank = rank.copy()
    rank["gate_ms_expression_anchor"] = (rank["ms_delta_log2"] > 0.25) & (rank["ms_p"] < 0.05)
    rank["gate_cross_disease_cellstate"] = (
        (rank["raw_positive_disease_count"] >= 3)
        & (rank["raw_negative_disease_count"] <= 1)
    ) | (rank["retained_positive_disease_count"] >= 3)
    rank["gate_target_resolved_breadth"] = (
        (rank["wave62_strong_l2g_disease_count"] >= 4)
        | (rank["wave62_strong_qtl_coloc_disease_count"] >= 4)
    )
    rank["gate_broad_genetics_proxy"] = rank["wave55_n_genetic_diseases_ge_0_25"] >= 5
    rank["gate_ms_genetic_anchor"] = (
        (rank["wave62_ms_max_l2g_score"] >= 0.50)
        | (rank["wave62_ms_max_relevant_qtl_h4"] >= 0.80)
        | (rank["wave55_ms_genetic_association"] >= 0.25)
    )
    rank["gate_real_perturbation"] = (
        (rank["wave37_contrast_fdr"] <= 0.20)
        & (rank["wave37_contrast_lfc"].abs() >= 0.10)
    )
    rank["gate_response_association"] = rank["wave68_remission_adjusted_fdr"] <= 0.10
    rank["gate_foundation_support"] = (
        (rank["wave18_strong_support_contexts"] >= 1)
        & (~rank["wave18_recommendation"].str.contains("do_not_promote", case=False, na=False))
    )
    rank["gate_l1000_class_reversal"] = rank["class_l1000_top_hit_rows_matching_core_compounds"] > 0
    rank["gate_actionable_modality"] = rank["manual_modality_ready"].astype(bool)
    rank["gate_prior_not_blocking"] = (
        ~rank["manual_prior_blocked"].astype(bool)
        & ~rank["wave62_prior_context_blocker"].astype(str).str.len().gt(0)
        & ~rank["wave28_manual_prior_risk"].astype(str).str.lower().eq("high")
    )
    rank["gate_direction_clear"] = rank["manual_direction_clear"].astype(bool)
    rank["gate_safety_not_blocking"] = ~rank["manual_safety_blocked"].astype(bool)
    rank["gate_any_perturbation_or_model"] = (
        rank["gate_real_perturbation"]
        | rank["gate_foundation_support"]
        | rank["gate_l1000_class_reversal"]
        | rank["wave28_l1000_non_no_go"].astype(bool)
    )

    support_cols = [
        "gate_ms_expression_anchor",
        "gate_cross_disease_cellstate",
        "gate_target_resolved_breadth",
        "gate_broad_genetics_proxy",
        "gate_ms_genetic_anchor",
        "gate_real_perturbation",
        "gate_response_association",
        "gate_foundation_support",
        "gate_l1000_class_reversal",
        "gate_actionable_modality",
        "gate_prior_not_blocking",
        "gate_direction_clear",
        "gate_safety_not_blocking",
    ]
    rank["support_gate_count"] = rank[support_cols].sum(axis=1).astype(int)
    rank["critical_gate_count"] = rank[
        [
            "gate_ms_expression_anchor",
            "gate_cross_disease_cellstate",
            "gate_target_resolved_breadth",
            "gate_ms_genetic_anchor",
            "gate_any_perturbation_or_model",
            "gate_actionable_modality",
            "gate_prior_not_blocking",
            "gate_direction_clear",
            "gate_safety_not_blocking",
        ]
    ].sum(axis=1).astype(int)

    missing = []
    calls = []
    for _, row in rank.iterrows():
        row_missing: list[str] = []
        for col in [
            "gate_ms_expression_anchor",
            "gate_cross_disease_cellstate",
            "gate_target_resolved_breadth",
            "gate_ms_genetic_anchor",
            "gate_any_perturbation_or_model",
            "gate_actionable_modality",
            "gate_prior_not_blocking",
            "gate_direction_clear",
            "gate_safety_not_blocking",
        ]:
            if not bool(row[col]):
                row_missing.append(col.replace("gate_", ""))
        missing.append(";".join(row_missing))
        if bool(row["manual_prior_blocked"]) or not bool(row["gate_prior_not_blocking"]):
            calls.append("NO_GO_PRIOR_ART_OR_BRANCH_BLOCKED")
        elif bool(row["manual_safety_blocked"]) or not bool(row["gate_safety_not_blocking"]):
            calls.append("NO_GO_SAFETY_OR_CLASS_TOXICITY")
        elif not bool(row["gate_actionable_modality"]):
            calls.append("NO_GO_NO_SELECTIVE_ACTIONABLE_MODALITY")
        elif not bool(row["gate_direction_clear"]):
            calls.append("NO_GO_DIRECTIONALITY_UNRESOLVED")
        elif not bool(row["gate_any_perturbation_or_model"]):
            calls.append("NO_GO_NO_PERTURBATION_OR_MODEL_SUPPORT")
        elif not bool(row["gate_cross_disease_cellstate"]) or not bool(row["gate_ms_expression_anchor"]):
            calls.append("NO_GO_LOCAL_CELLSTATE_SUPPORT_INADEQUATE")
        elif not bool(row["gate_target_resolved_breadth"]) or not bool(row["gate_ms_genetic_anchor"]):
            calls.append("NO_GO_TARGET_GENETICS_INADEQUATE")
        else:
            calls.append("PROMOTE_CAMP_RESTORATION_ROUTE")
    rank["missing_critical_gates"] = missing
    rank["wave100_call"] = calls
    rank["wave100_priority_score"] = (
        rank["critical_gate_count"] * 2
        + rank["support_gate_count"]
        + rank["raw_positive_disease_count"].clip(upper=5)
        + rank["wave55_n_genetic_diseases_ge_0_25"].clip(upper=5)
        - rank["raw_negative_disease_count"].clip(upper=3)
        - rank["manual_prior_blocked"].astype(int) * 4
        - rank["manual_safety_blocked"].astype(int) * 3
    )
    return rank.sort_values(
        ["wave100_call", "wave100_priority_score", "critical_gate_count"],
        ascending=[True, False, False],
    )


def write_report(rank: pd.DataFrame, context_rows: pd.DataFrame, summary: dict[str, Any]) -> None:
    top_cols = [
        "gene",
        "route",
        "wave100_call",
        "wave100_priority_score",
        "critical_gate_count",
        "support_gate_count",
        "ms_delta_log2",
        "ms_p",
        "raw_positive_disease_count",
        "raw_negative_disease_count",
        "retained_positive_disease_count",
        "wave55_n_genetic_diseases_ge_0_25",
        "wave62_strong_l2g_disease_count",
        "wave62_strong_qtl_coloc_disease_count",
        "wave62_ms_max_l2g_score",
        "wave62_ms_max_relevant_qtl_h4",
        "wave37_screen_call",
        "wave37_contrast_fdr",
        "wave18_recommendation",
        "class_l1000_top_hit_rows_matching_core_compounds",
        "missing_critical_gates",
        "manual_note",
    ]
    report = f"""# Wave100 cAMP-Restoration Intervention-Class Audit

## Bottom Line

Branch call: `{summary["branch_call"]}`.

The cAMP-restoration class remains a useful comparator but is not promoted as
a V3 therapeutic mechanism. The best biology clues split across incompatible
gates: `ADCY3` has nominal MS white-matter expression and broad genetics but
no selective activation modality or direction proof; `GPR65` and `PTGER4`
carry stronger GPCR/genetic tractability but are prior-art/directionality
blocked; `PDE4B/PDE4D` are pharmacologically reachable but have negative/weak
local L1000 support, no clean MS disease-high anchor, and class toxicity/prior
art.

## Candidate Ranking

{markdown_table(rank[top_cols], max_rows=30)}

## Class-Level Perturbation Evidence

- LINCS metadata rows matching PDE4/cAMP terms: `{summary["pde4_l1000_metadata_rows"]}`.
- Unique LINCS perturbagen IDs matching PDE4/cAMP terms: `{summary["pde4_l1000_unique_pert_ids"]}`.
- Retrieved L1000FWD opposite-hit rows matching broad PDE4/cAMP terms:
  `{summary["pde4_l1000_top_hit_rows_matching_terms"]}`.
- Retrieved opposite-hit rows matching core compounds
  (`apremilast`, `roflumilast`, `rolipram`, `cilomilast`, `ibudilast`,
  `piclamilast`, `forskolin`, `bucladesine`):
  `{summary["pde4_l1000_top_hit_rows_matching_core_compounds"]}`.

Interpretation: class perturbagens are present in the background LINCS
metadata, but core cAMP/PDE4 compounds are absent from the retrieved disease
signature reversal hits. This is not proof the biology is false; it is a
negative intervention-prioritization signal for the current V3 claim.

## Local Context Rows

Most significant context-level rows for cAMP-route genes:

{markdown_table(context_rows.head(30), max_rows=30)}

## Gate Logic

Promotion required all of: MS expression anchor, cross-disease cell-state
support, target-resolved broad genetics, MS genetic anchor, real perturbation
or model/class reversal support, actionable modality, prior-art clearance,
clear direction, and safety not blocking. No route satisfied that combined
standard.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave100_camp_restoration_class_audit.py")}`
- Rank table: `{rel(OUT / "camp_restoration_candidate_rank.tsv")}`
- Context rows: `{rel(OUT / "camp_candidate_context_rows.tsv")}`
- Summary JSON: `{rel(OUT / "summary.json")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    tables = {
        "ms_wm": read_tsv(MS_WM),
        "broad_raw": read_tsv(BROAD_RAW),
        "broad_resid": read_tsv(BROAD_RESID),
        "w55": read_tsv(W55),
        "w62": read_tsv(W62),
        "w68": read_tsv(W68),
        "w37": read_tsv(W37),
        "w18": read_tsv(W18),
        "w96": read_tsv(W96),
        "w96_donor": read_tsv(W96_DONOR),
        "w28": read_tsv(W28),
    }
    aux = {
        "pde4_l1000": read_json(PDE4_L1000),
        "gpr65_summary": read_json(W50_SUMMARY),
    }
    context_rows = collect_context_rows(tables["broad_raw"])
    context_rows.to_csv(OUT / "camp_candidate_context_rows.tsv", sep="\t", index=False)

    rank = add_gates(collect_rows(tables, aux))
    rank.to_csv(OUT / "camp_restoration_candidate_rank.tsv", sep="\t", index=False)

    promoted = rank[rank["wave100_call"].eq("PROMOTE_CAMP_RESTORATION_ROUTE")]
    branch_call = "PROMOTE_CAMP_RESTORATION_ROUTE" if not promoted.empty else "NO_REOPEN_CAMP_RESTORATION_CLASS"
    l1000 = aux["pde4_l1000"]
    summary = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "n_candidates": int(len(rank)),
        "call_counts": rank["wave100_call"].value_counts().to_dict(),
        "top_candidate": rank.iloc[0]["gene"] if not rank.empty else "",
        "top_candidate_call": rank.iloc[0]["wave100_call"] if not rank.empty else "",
        "promoted_candidates": promoted["gene"].tolist(),
        "pde4_l1000_metadata_rows": int(l1000.get("n_lincs_metadata_rows_matching_terms", 0) or 0),
        "pde4_l1000_unique_pert_ids": int(l1000.get("n_lincs_unique_pert_ids_matching_terms", 0) or 0),
        "pde4_l1000_top_hit_rows_matching_terms": int(l1000.get("n_l1000_top_hit_rows_matching_terms", 0) or 0),
        "pde4_l1000_top_hit_rows_matching_core_compounds": int(l1000.get("n_l1000_top_hit_rows_matching_core_compounds", 0) or 0),
        "inputs": {
            "ms_wm": rel(MS_WM),
            "broad_raw": rel(BROAD_RAW),
            "broad_resid": rel(BROAD_RESID),
            "wave55": rel(W55),
            "wave62": rel(W62),
            "wave68": rel(W68),
            "wave37": rel(W37),
            "wave18": rel(W18),
            "wave96": rel(W96),
            "wave28": rel(W28),
            "pde4_l1000": rel(PDE4_L1000),
            "gpr65_summary": rel(W50_SUMMARY),
        },
    }
    write_json(OUT / "summary.json", summary)
    write_report(rank, context_rows, summary)


if __name__ == "__main__":
    main()
