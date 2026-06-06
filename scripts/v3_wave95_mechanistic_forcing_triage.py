#!/usr/bin/env python3
"""Wave95 mechanistic forcing triage after accessible-state rerank.

Wave94 identified several accessible/state-transition candidates, but its
output was only a branch selector. This wave applies stricter mechanistic gates:

- residualized cell-state support rather than raw disease expression;
- MS expression or target-resolved genetic anchor;
- cell-resolved response or real perturbation/foundation support;
- targetability/modality and prior-art feasibility;
- explicit demotion of marker-only or wet-lab-only routes.

This is a triage/falsification matrix, not a finding generator.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_direct_h5ad_cell_states import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave95_mechanistic_forcing_triage"

W94 = ROOT / "phases/v3/results" / "wave94_accessible_state_rerank" / "accessible_state_candidate_rank.tsv"
W92_ROUTE = ROOT / "phases/v3/results" / "wave92_lipid_state_controller_route_audit" / "controller_route_rank.tsv"
W39 = ROOT / "phases/v3/results" / "wave39_surfaceome_rescue_after_resolution_pivot" / "surfaceome_rescue_rank_full.tsv"
MS = ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv"
RESID = ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
W55 = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W62 = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W68 = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
W68_OLS = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "adjusted_top_gene_ols.tsv"
W37 = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W18 = ROOT / "phases/v3/results" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv"
W79 = ROOT / "phases/v3/results" / "wave79_targetability_shortlist_audit" / "targetability_integrated_decision.tsv"
W83 = ROOT / "phases/v3/results" / "wave83_intervention_class_meta_rank" / "intervention_class_meta_rank.tsv"


GENE_CANDIDATES: list[str] = [
    # Wave94 top forcing-test genes
    "SEL1L3",
    "NRCAM",
    "PLEK2",
    "C15ORF48",
    "CD200",
    "CHI3L1",
    "ROMO1",
    # Sidecar / comparator genes
    "CD58",
    "CD82",
    "FXYD5",
    "MFGE8",
    "P2RX7",
    "P4HB",
    "MFGE8",
]

ROUTE_CANDIDATES: dict[str, str] = {
    "CD300_RECEPTOR_SPECIFIC_TUNING": "CD300 receptor-specific lipid/efferocytosis checkpoint tuning",
    "FPR2_ANXA1_BIASED_RESOLUTION": "FPR2/ANXA1 biased pro-resolution GPCR signaling",
}

MANUAL_PRIOR: dict[str, dict[str, Any]] = {
    "CD58": {
        "prior_class": "blocked_generic_autoimmune_intervention",
        "prior_blocked": True,
        "modality_ready": True,
        "route_note": "CD2/CD58 biology strong, but alefacept/CD2-CD58 autoimmune prior art and MS protective-CD58 direction conflict block promotion.",
    },
    "CD82": {
        "prior_class": "direction_actionability_blocked",
        "prior_blocked": False,
        "modality_ready": False,
        "route_note": "Accessible tetraspanin marker; direction and target engagement are not interpretable enough for standalone promotion.",
    },
    "FXYD5": {
        "prior_class": "novelty_not_blocked_safety_modality_unresolved",
        "prior_blocked": False,
        "modality_ready": False,
        "wetlab_only": True,
        "route_note": "Only a non-depleting, barrier-preserving perturbation kill test could reopen this route.",
    },
    "MFGE8": {
        "prior_class": "close_efferocytosis_prior_art_safety_unresolved",
        "prior_blocked": False,
        "modality_ready": True,
        "wetlab_only": True,
        "route_note": "Mechanistically clean debris-opsonin assay concept, but local MS/cross-disease support and bystander-phagocytosis safety are weak.",
    },
    "P2RX7": {
        "prior_class": "blocked_broad_p2x7_autoimmune_ms",
        "prior_blocked": True,
        "modality_ready": True,
        "route_note": "Broad antagonist route is blocked by RA/Crohn clinical trials and MS patent precedent; subgroup-only comparator.",
    },
    "P4HB": {
        "prior_class": "nonspecific_redox_er_biology",
        "prior_blocked": False,
        "modality_ready": True,
        "route_note": "Druggable-looking but lacks MS anchor and state-specific mechanism.",
    },
    "SEL1L3": {
        "prior_class": "undercharacterized_no_intervention_package",
        "prior_blocked": False,
        "modality_ready": False,
        "route_note": "Expression survivor without a target mechanism or selective modality.",
    },
    "NRCAM": {
        "prior_class": "neural_adhesion_safety_and_weak_genetics",
        "prior_blocked": False,
        "modality_ready": False,
        "route_note": "Consistent response marker but neural adhesion biology and weak genetics make it unsafe as target-first route.",
    },
    "PLEK2": {
        "prior_class": "intracellular_cytoskeletal_no_modality",
        "prior_blocked": False,
        "modality_ready": False,
        "route_note": "Strong MS expression but no response, genetics, or perturbation package.",
    },
    "C15ORF48": {
        "prior_class": "mitochondrial_microprotein_no_direct_modality",
        "prior_blocked": False,
        "modality_ready": False,
        "route_note": "Mechanistically interesting immunometabolic clue; not yet a tractable intervention point.",
    },
    "CD200": {
        "prior_class": "checkpoint_direction_receptor_side_unresolved",
        "prior_blocked": False,
        "modality_ready": True,
        "route_note": "Ligand-side signal with unresolved CD200R1 direction and prior checkpoint closure.",
    },
    "CHI3L1": {
        "prior_class": "secreted_biomarker_prior_saturation",
        "prior_blocked": True,
        "modality_ready": True,
        "route_note": "Secreted biomarker/remodeling route with response conflict and high prior saturation.",
    },
    "ROMO1": {
        "prior_class": "mitochondrial_ros_no_selective_modality",
        "prior_blocked": False,
        "modality_ready": False,
        "route_note": "ROS/mitochondrial marker with no selective autoimmune modality.",
    },
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
        return float(value)
    except (TypeError, ValueError):
        return default


def first_row(df: pd.DataFrame, key: str, col: str = "gene") -> pd.Series | None:
    if df.empty or col not in df.columns:
        return None
    sub = df[df[col].astype(str).str.upper().eq(key.upper())]
    if sub.empty:
        return None
    return sub.iloc[0]


def best_w68_row(df: pd.DataFrame, key: str) -> pd.Series | None:
    if df.empty or "gene" not in df.columns:
        return None
    sub = df[df["gene"].astype(str).str.upper().eq(key.upper())].copy()
    if sub.empty:
        return None
    sub["_sort_fdr"] = pd.to_numeric(sub.get("remission_adjusted_fdr", np.nan), errors="coerce").fillna(1.0)
    sub["_sort_p"] = pd.to_numeric(sub.get("remission_adjusted_p", np.nan), errors="coerce").fillna(1.0)
    return sub.sort_values(["_sort_fdr", "_sort_p"]).iloc[0]


def best_w37_row(df: pd.DataFrame, key: str) -> pd.Series | None:
    if df.empty or "gene_symbol" not in df.columns:
        return None
    sub = df[df["gene_symbol"].astype(str).str.upper().eq(key.upper())].copy()
    if sub.empty:
        return None
    sub["_sort_fdr"] = pd.to_numeric(sub.get("contrast_fdr", np.nan), errors="coerce").fillna(1.0)
    return sub.sort_values("_sort_fdr").iloc[0]


def best_w18_row(df: pd.DataFrame, key: str) -> pd.Series | None:
    if df.empty or "gene" not in df.columns:
        return None
    sub = df[df["gene"].astype(str).str.upper().eq(key.upper())].copy()
    if sub.empty:
        return None
    sub["_sort_rank"] = pd.to_numeric(sub.get("wave18_rank", np.nan), errors="coerce").fillna(9999)
    return sub.sort_values("_sort_rank").iloc[0]


def prior_status_is_blocking(value: Any) -> bool:
    status = clean(value).upper()
    if status.startswith("NOT_BLOCKED"):
        return False
    return status.startswith("BLOCKED") or status.startswith("PARTLY_BLOCKED")


def build_gene_row(gene: str, tables: dict[str, pd.DataFrame]) -> dict[str, Any]:
    gene = gene.upper()
    manual = MANUAL_PRIOR.get(gene, {})
    row: dict[str, Any] = {
        "candidate": gene,
        "candidate_type": "gene",
        "route_class": manual.get("route_note", ""),
        "manual_prior_class": manual.get("prior_class", "not_manually_classified"),
        "manual_prior_blocked": bool(manual.get("prior_blocked", False)),
        "manual_modality_ready": bool(manual.get("modality_ready", False)),
        "manual_wetlab_only": bool(manual.get("wetlab_only", False)),
    }

    w94 = first_row(tables["w94"], gene)
    w39 = first_row(tables["w39"], gene)
    ms = first_row(tables["ms"], gene)
    resid = first_row(tables["resid"], gene)
    w55 = first_row(tables["w55"], gene)
    w62 = first_row(tables["w62"], gene)
    w68 = best_w68_row(tables["w68"], gene)
    w37 = best_w37_row(tables["w37"], gene)
    w18 = best_w18_row(tables["w18"], gene)
    w79 = first_row(tables["w79"], gene)

    row.update(
        {
            "wave94_call": clean(w94.get("wave94_call")) if w94 is not None else "",
            "wave94_score": num(w94.get("wave94_score")) if w94 is not None else math.nan,
            "wave94_failures": clean(w94.get("wave94_failures")) if w94 is not None else "",
            "wave39_call": clean(w39.get("wave39_call")) if w39 is not None else "",
            "wave39_score": num(w39.get("wave39_score")) if w39 is not None else math.nan,
            "ms_delta_log2": num(ms.get("delta_log2")) if ms is not None else num(w94.get("ms_delta_log2_direct")) if w94 is not None else math.nan,
            "ms_p": num(ms.get("p")) if ms is not None else num(w94.get("ms_p_direct")) if w94 is not None else math.nan,
            "ms_fdr": num(ms.get("fdr")) if ms is not None else math.nan,
            "broad_positive_disease_count": num(w94.get("broad_positive_disease_count"), 0.0) if w94 is not None else num(w39.get("positive_disease_count"), 0.0) if w39 is not None else 0.0,
            "broad_negative_disease_count": num(w94.get("broad_negative_disease_count"), 0.0) if w94 is not None else num(w39.get("negative_disease_count"), 0.0) if w39 is not None else 0.0,
            "myeloid_positive_disease_count": num(w94.get("myeloid_positive_disease_count"), 0.0) if w94 is not None else 0.0,
            "response_nonresponse_high_systems_p20": num(w94.get("response_nonresponse_high_systems_p20"), 0.0) if w94 is not None else 0.0,
            "response_responder_high_systems_p20": num(w94.get("response_responder_high_systems_p20"), 0.0) if w94 is not None else 0.0,
            "response_direction_conflict": clean(w94.get("response_direction_conflict")).lower() in {"1", "true", "yes"} if w94 is not None else False,
            "response_summary": clean(w94.get("response_summary")) if w94 is not None else "",
            "strict_core_residual_disease_count": num(resid.get("strict_core_covariate_surviving_disease_count"), 0.0) if resid is not None else 0.0,
            "strict_core_residual_analyses": clean(resid.get("strict_core_covariate_surviving_analyses")) if resid is not None else "",
            "retained_residual_disease_count": num(resid.get("retained_positive_disease_count"), 0.0) if resid is not None else 0.0,
            "non_ibd_retained_residual_disease_count": num(resid.get("non_ibd_retained_positive_disease_count"), 0.0) if resid is not None else 0.0,
            "wave55_genetic_diseases_ge_0_25": clean(w55.get("wave55_genetic_diseases_ge_0_25")) if w55 is not None else clean(w55.get("diseases_genetic_ge_0_25")) if w55 is not None else "",
            "wave55_n_genetic_diseases_ge_0_25": num(w55.get("n_diseases_genetic_ge_0_25"), 0.0) if w55 is not None else 0.0,
            "wave62_call": clean(w62.get("wave62_call")) if w62 is not None else "",
            "wave62_strong_l2g_disease_count": num(w62.get("strong_l2g_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_strong_qtl_coloc_disease_count": num(w62.get("strong_qtl_coloc_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_ms_max_l2g_score": num(w62.get("ms_max_l2g_score"), 0.0) if w62 is not None else 0.0,
            "wave62_ms_max_relevant_qtl_h4": num(w62.get("ms_max_relevant_qtl_h4"), 0.0) if w62 is not None else 0.0,
            "chembl_activity_count": num(w39.get("chembl_activity_count"), 0.0) if w39 is not None else num(w62.get("druggable_activity_count"), 0.0) if w62 is not None else 0.0,
            "uniprot_accessible": clean(w39.get("uniprot_accessible")) if w39 is not None else "",
            "w68_best_cell_state": clean(w68.get("cell_state")) if w68 is not None else "",
            "w68_remission_adjusted_delta": num(w68.get("remission_adjusted_delta")) if w68 is not None else math.nan,
            "w68_remission_adjusted_p": num(w68.get("remission_adjusted_p")) if w68 is not None else math.nan,
            "w68_remission_adjusted_fdr": num(w68.get("remission_adjusted_fdr")) if w68 is not None else math.nan,
            "w68_call": clean(w68.get("wave68_call")) if w68 is not None else "",
            "w37_screen_call": clean(w37.get("screen_call")) if w37 is not None else "",
            "w37_contrast_lfc": num(w37.get("median_efficient_minus_noneater_lfc")) if w37 is not None else math.nan,
            "w37_contrast_fdr": num(w37.get("contrast_fdr")) if w37 is not None else math.nan,
            "w18_geneformer_support_contexts": num(w18.get("total_support_contexts"), 0.0) if w18 is not None else 0.0,
            "w18_strong_support_contexts": num(w18.get("total_strong_support_contexts"), 0.0) if w18 is not None else 0.0,
            "w18_real_perturbation_alignment_call": clean(w18.get("real_perturbation_alignment_call")) if w18 is not None else "",
            "w18_foundation_recommendation": clean(w18.get("foundation_rescue_recommendation")) if w18 is not None else "",
            "wave79_call": clean(w79.get("wave79_call")) if w79 is not None else "",
            "wave79_gate_count": num(w79.get("gate_count"), 0.0) if w79 is not None else 0.0,
            "wave79_decision_reason": clean(w79.get("decision_reason")) if w79 is not None else "",
        }
    )
    return apply_gates(row)


def build_route_row(route: str, label: str, tables: dict[str, pd.DataFrame]) -> dict[str, Any]:
    df = tables["w92_route"]
    sub = df[df["route"].astype(str).eq(route)] if not df.empty and "route" in df.columns else pd.DataFrame()
    r = sub.iloc[0] if not sub.empty else pd.Series(dtype=object)
    prior_blocked = prior_status_is_blocking(r.get("prior_status"))
    row: dict[str, Any] = {
        "candidate": route,
        "candidate_type": "route",
        "route_class": label,
        "manual_prior_class": clean(r.get("prior_status")) or "route_prior_status_missing",
        "manual_prior_blocked": prior_blocked,
        "manual_modality_ready": True,
        "manual_wetlab_only": True,
        "wave94_call": "",
        "wave94_score": math.nan,
        "wave94_failures": "",
        "wave39_call": "",
        "wave39_score": math.nan,
        "ms_delta_log2": num(r.get("ms_mean_delta_log2")),
        "ms_p": num(r.get("ms_combined_p")),
        "ms_fdr": math.nan,
        "broad_positive_disease_count": num(r.get("h5ad_positive_disease_count"), 0.0),
        "broad_negative_disease_count": num(r.get("h5ad_negative_disease_count"), 0.0),
        "myeloid_positive_disease_count": 0.0,
        "strict_core_residual_disease_count": 0.0,
        "strict_core_residual_analyses": "",
        "retained_residual_disease_count": 0.0,
        "non_ibd_retained_residual_disease_count": 0.0,
        "wave55_genetic_diseases_ge_0_25": "",
        "wave55_n_genetic_diseases_ge_0_25": 0.0,
        "wave62_call": "",
        "wave62_strong_l2g_disease_count": 0.0,
        "wave62_strong_qtl_coloc_disease_count": 0.0,
        "wave62_ms_max_l2g_score": 0.0,
        "wave62_ms_max_relevant_qtl_h4": 0.0,
        "chembl_activity_count": math.nan,
        "uniprot_accessible": "",
        "w68_best_cell_state": "",
        "w68_remission_adjusted_delta": math.nan,
        "w68_remission_adjusted_p": math.nan,
        "w68_remission_adjusted_fdr": math.nan,
        "w68_call": "",
        "w37_screen_call": "",
        "w37_contrast_lfc": math.nan,
        "w37_contrast_fdr": math.nan,
        "w18_geneformer_support_contexts": 0.0,
        "w18_strong_support_contexts": 0.0,
        "w18_real_perturbation_alignment_call": "",
        "w18_foundation_recommendation": "",
        "wave79_call": "",
        "wave79_gate_count": math.nan,
        "wave79_decision_reason": "",
        "route_response_systems": num(r.get("response_nonresponse_high_system_count"), 0.0),
        "route_response_nominal_systems": num(r.get("response_nominal_or_trend_system_count"), 0.0),
        "route_ms_call": clean(r.get("ms_route_call")),
        "route_wave92_call": clean(r.get("wave92_call")),
        "route_genes": clean(r.get("route_genes")),
    }
    return apply_gates(row)


def apply_gates(row: dict[str, Any]) -> dict[str, Any]:
    ms_expr_strict = num(row.get("ms_delta_log2"), -999) > 0.25 and num(row.get("ms_p"), 1.0) < 0.05
    ms_expr_trend = num(row.get("ms_delta_log2"), -999) > 0.25 and num(row.get("ms_p"), 1.0) < 0.10
    ms_genetic = num(row.get("wave62_ms_max_l2g_score"), 0.0) >= 0.5 or num(row.get("wave62_ms_max_relevant_qtl_h4"), 0.0) >= 0.8
    broad_genetic = max(num(row.get("wave62_strong_l2g_disease_count"), 0.0), num(row.get("wave62_strong_qtl_coloc_disease_count"), 0.0), num(row.get("wave55_n_genetic_diseases_ge_0_25"), 0.0)) >= 4
    target_resolved = max(num(row.get("wave62_strong_l2g_disease_count"), 0.0), num(row.get("wave62_strong_qtl_coloc_disease_count"), 0.0)) >= 2
    residual = num(row.get("strict_core_residual_disease_count"), 0.0) >= 2 and num(row.get("non_ibd_retained_residual_disease_count"), 0.0) >= 1
    cell_response = num(row.get("w68_remission_adjusted_fdr"), 1.0) <= 0.10
    wave94_response = num(row.get("response_nonresponse_high_systems_p20"), 0.0) >= 2 and not bool(row.get("response_direction_conflict", False))
    route_response = num(row.get("route_response_systems"), 0.0) >= 2
    w37_real = (
        clean(row.get("w37_screen_call")).startswith("KO_")
        and clean(row.get("w37_screen_call")) != "UNRESOLVED"
        and num(row.get("w37_contrast_fdr"), 1.0) <= 0.20
    )
    w18_real = "model_only" not in clean(row.get("w18_real_perturbation_alignment_call")).lower() and "do_not_promote" not in clean(row.get("w18_foundation_recommendation")).lower() and num(row.get("w18_strong_support_contexts"), 0.0) >= 1
    perturb_model = w37_real or w18_real
    modality = bool(row.get("manual_modality_ready")) or clean(row.get("uniprot_accessible")).lower() in {"true", "1"} or num(row.get("chembl_activity_count"), 0.0) > 0
    prior_ok = not bool(row.get("manual_prior_blocked"))
    generic_or_closed = any(token in clean(row.get("wave94_failures")).lower() for token in ["generic_immune_marker", "known_closed_route", "prior_or_class_saturated"])
    wetlab_only = bool(row.get("manual_wetlab_only"))

    gates = {
        "gate_ms_anchor": bool(ms_expr_strict or ms_genetic),
        "gate_ms_trend": bool(ms_expr_trend or ms_genetic),
        "gate_cross_disease_residual": bool(residual),
        "gate_cell_resolved_response_or_transition": bool(cell_response),
        "gate_response_specificity": bool(wave94_response or route_response),
        "gate_target_resolved_genetics_ge2": bool(target_resolved),
        "gate_broad_genetics_ge4": bool(broad_genetic),
        "gate_real_perturbation_or_validated_model": bool(perturb_model),
        "gate_modality": bool(modality),
        "gate_prior_not_blocked": bool(prior_ok),
        "gate_not_generic_or_closed": not bool(generic_or_closed),
    }
    row.update(gates)
    row["critical_gate_count"] = int(
        sum(
            [
                gates["gate_ms_anchor"],
                gates["gate_cross_disease_residual"],
                gates["gate_real_perturbation_or_validated_model"],
                gates["gate_modality"],
                gates["gate_prior_not_blocked"],
                gates["gate_not_generic_or_closed"],
            ]
        )
    )
    row["support_gate_count"] = int(
        sum(
            [
                gates["gate_ms_trend"],
                gates["gate_cell_resolved_response_or_transition"],
                gates["gate_response_specificity"],
                gates["gate_target_resolved_genetics_ge2"],
                gates["gate_broad_genetics_ge4"],
            ]
        )
    )

    failures = [name for name, passed in gates.items() if not passed]
    row["wave95_failures"] = ";".join(failures)

    if row["critical_gate_count"] >= 6 and row["support_gate_count"] >= 3:
        call = "REOPEN_MECHANISTIC_FORCING_CANDIDATE"
        reason = "all critical gates and multiple support gates pass"
    elif row.get("manual_prior_blocked"):
        call = "NO_GO_PRIOR_ART_OR_SAFETY_BLOCKED"
        reason = "prior-art/safety gate blocks therapeutic promotion"
    elif wetlab_only:
        call = "PARK_WETLAB_KILL_TEST_ONLY"
        reason = "route can only be reopened by target-specific wet-lab perturbation/safety test"
    elif not gates["gate_real_perturbation_or_validated_model"] and not gates["gate_cross_disease_residual"]:
        call = "NO_GO_MARKER_WITHOUT_RESIDUAL_OR_PERTURBATION_SUPPORT"
        reason = "expression/response signal lacks residualized controller evidence and validated perturbation direction"
    elif not gates["gate_modality"]:
        call = "PARK_MECHANISM_CLUE_NO_INTERVENTION_PACKAGE"
        reason = "candidate may mark a transition but lacks selective modality or target package"
    else:
        call = "PARK_INCOMPLETE_MECHANISTIC_PACKAGE"
        reason = "some evidence survives but strict mechanistic therapeutic gates do not"
    row["wave95_call"] = call
    row["wave95_reason"] = reason
    return row


def report_table(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "candidate",
        "candidate_type",
        "wave95_call",
        "critical_gate_count",
        "support_gate_count",
        "ms_delta_log2",
        "ms_p",
        "broad_positive_disease_count",
        "strict_core_residual_disease_count",
        "w68_remission_adjusted_fdr",
        "w37_screen_call",
        "w18_foundation_recommendation",
        "wave62_strong_qtl_coloc_disease_count",
        "wave55_n_genetic_diseases_ge_0_25",
        "manual_prior_class",
        "wave95_reason",
    ]
    return df[[c for c in cols if c in df.columns]].copy()


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    tables = {
        "w94": read_tsv(W94),
        "w92_route": read_tsv(W92_ROUTE),
        "w39": read_tsv(W39),
        "ms": read_tsv(MS),
        "resid": read_tsv(RESID),
        "w55": read_tsv(W55),
        "w62": read_tsv(W62),
        "w68": read_tsv(W68),
        "w68_ols": read_tsv(W68_OLS),
        "w37": read_tsv(W37),
        "w18": read_tsv(W18),
        "w79": read_tsv(W79),
        "w83": read_tsv(W83),
    }
    for key in ["w94", "w39", "ms", "resid", "w55", "w62", "w68", "w18", "w79"]:
        if not tables[key].empty and "gene" in tables[key].columns:
            tables[key]["gene"] = tables[key]["gene"].astype(str).str.upper()
    if not tables["w37"].empty and "gene_symbol" in tables["w37"].columns:
        tables["w37"]["gene_symbol"] = tables["w37"]["gene_symbol"].astype(str).str.upper()

    genes = sorted(set(GENE_CANDIDATES))
    rows = [build_gene_row(gene, tables) for gene in genes]
    rows.extend(build_route_row(route, label, tables) for route, label in ROUTE_CANDIDATES.items())
    rank = pd.DataFrame(rows)
    rank = rank.sort_values(
        [
            "critical_gate_count",
            "support_gate_count",
            "gate_ms_trend",
            "broad_positive_disease_count",
            "candidate",
        ],
        ascending=[False, False, False, False, True],
    )

    gate_cols = [c for c in rank.columns if c.startswith("gate_")]
    gate_audit = rank[["candidate", "candidate_type", "wave95_call", *gate_cols, "wave95_failures"]].copy()

    metric_cols = [
        c
        for c in [
            "candidate",
            "ms_delta_log2",
            "ms_p",
            "ms_fdr",
            "broad_positive_disease_count",
            "broad_negative_disease_count",
            "myeloid_positive_disease_count",
            "strict_core_residual_disease_count",
            "retained_residual_disease_count",
            "w68_remission_adjusted_delta",
            "w68_remission_adjusted_p",
            "w68_remission_adjusted_fdr",
            "w37_contrast_lfc",
            "w37_contrast_fdr",
            "w18_geneformer_support_contexts",
            "w18_strong_support_contexts",
            "wave62_strong_l2g_disease_count",
            "wave62_strong_qtl_coloc_disease_count",
            "wave55_n_genetic_diseases_ge_0_25",
            "chembl_activity_count",
        ]
        if c in rank.columns
    ]
    metric_long = rank[metric_cols].melt(id_vars=["candidate"], var_name="metric", value_name="value")

    rank.to_csv(OUT / "mechanistic_forcing_candidate_rank.tsv", sep="\t", index=False)
    gate_audit.to_csv(OUT / "mechanistic_forcing_gate_audit.tsv", sep="\t", index=False)
    metric_long.to_csv(OUT / "mechanistic_forcing_metric_long.tsv", sep="\t", index=False)

    call_counts = rank["wave95_call"].value_counts().to_dict()
    promoted = rank[rank["wave95_call"].eq("REOPEN_MECHANISTIC_FORCING_CANDIDATE")]
    summary = {
        "seed": SEED,
        "analysis_call": "NO_MECHANISTIC_THERAPEUTIC_PROMOTION",
        "n_candidates": int(len(rank)),
        "n_promoted": int(len(promoted)),
        "call_counts": call_counts,
        "top_candidate": clean(rank.iloc[0]["candidate"]) if not rank.empty else "",
        "top_candidate_call": clean(rank.iloc[0]["wave95_call"]) if not rank.empty else "",
        "inputs": {
            "wave94": rel(W94),
            "wave92_route": rel(W92_ROUTE),
            "broad_residual": rel(RESID),
            "gse111972_ms": rel(MS),
            "wave68_gse282122": rel(W68),
            "wave37_efferocytosis": rel(W37),
            "wave18_foundation": rel(W18),
            "wave55_genetics": rel(W55),
            "wave62_target_resolution": rel(W62),
        },
    }
    write_json(OUT / "summary.json", summary)

    top = report_table(rank.head(14))
    report = [
        "# Wave95 Mechanistic Forcing Triage",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Question",
        "",
        "Do the Wave94 accessible/state-transition candidates survive stricter",
        "mechanistic therapeutic gates: residualized state control, MS anchoring,",
        "validated perturbation/model direction, modality, and non-blocking prior art?",
        "",
        "## Verdict",
        "",
        "`NO_MECHANISTIC_THERAPEUTIC_PROMOTION`",
        "",
        f"Candidates tested: `{len(rank)}`. Promoted candidates: `{len(promoted)}`.",
        "",
        "## Call Counts",
        "",
        markdown_table(pd.DataFrame([{"wave95_call": k, "n": v} for k, v in call_counts.items()])),
        "",
        "## Top Ranked Rows",
        "",
        markdown_table(top, max_rows=20),
        "",
        "## Interpretation",
        "",
        "The Wave94 branch selection survives as a useful forcing map, but no",
        "candidate becomes a therapeutic nomination. `SEL1L3` remains the top",
        "statistical survivor, yet it has no validated perturbation direction, no",
        "strong target-resolved genetics, and no intervention package. `CD58/CD2`",
        "has the best genetic/biological evidence but is prior-art and direction",
        "blocked. `FXYD5`, `MFGE8`, and `CD300` are wet-lab kill-test routes, not",
        "in-silico findings. `C15ORF48` is a mechanistic clue rather than a druggable",
        "intervention point.",
        "",
        "The next computational move should not be another accessible-marker rerank.",
        "It should either (a) discover residualized transition controllers across",
        "cell-resolved autoimmune tissues de novo, or (b) move into explicit wet-lab",
        "assay design for the highest-ranked kill-test routes.",
        "",
        "## Output Files",
        "",
        f"- `{rel(OUT / 'mechanistic_forcing_candidate_rank.tsv')}`",
        f"- `{rel(OUT / 'mechanistic_forcing_gate_audit.tsv')}`",
        f"- `{rel(OUT / 'mechanistic_forcing_metric_long.tsv')}`",
        f"- `{rel(OUT / 'summary.json')}`",
        f"- `{rel(OUT / 'REPORT.md')}`",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
