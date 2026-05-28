#!/usr/bin/env python3
"""Wave71-A global existing-artifact survivor meta-rank.

This script does not fetch new data. It re-mines existing V3 artifacts for
genes that repeatedly survived as parked, review-worthy, target-resolved, or
positive-evidence nodes outside the now-closed Fc/ROS branch.

The rank is deliberately conservative: prior-art saturated families, broad
host-defense nodes, and Wave70 Fc/ROS comparators are penalized or hard blocked.
A reopener requires multi-channel convergence, not a single high score.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave71_global_survivor_meta_rank"
SUBAGENT = ROOT / "subagents_v3" / "wave71a_global_survivor_meta_rank.md"
SEED = 20260527


@dataclass(frozen=True)
class SourceSpec:
    wave: str
    channel: str
    path: str
    gene_cols: tuple[str, ...]
    call_cols: tuple[str, ...] = ()
    score_cols: tuple[str, ...] = ()
    blocker_cols: tuple[str, ...] = ()
    evidence_cols: tuple[str, ...] = ()
    weight: float = 1.0
    max_rows: int | None = None
    include_no_go: bool = False
    include_unlabeled_top: int = 0


SOURCES = [
    SourceSpec(
        "wave21",
        "residual_druggability",
        "results_v3/wave21_residual_druggability_scan/wave21_residual_druggability_ranked_full.tsv",
        ("gene",),
        ("wave21_call", "audit_priority_call", "target_level_genetics_dod_call"),
        ("wave21_residual_modality_score", "residual_gate_priority_score", "discovery_priority_score_broad"),
        ("prior_exclusion_reason", "wave21_failures", "existing_prior_flag"),
        (
            "wave21_modality_read",
            "strict_core_covariate_surviving_disease_count",
            "retained_positive_disease_count",
            "positive_diseases",
            "ms_wm_delta_log2_broad",
            "ms_wm_p_broad",
            "chembl_nM_activity_count",
            "uniprot_location",
        ),
        1.00,
    ),
    SourceSpec(
        "wave23",
        "genetics_restoration",
        "results_v3/wave23_genetics_restoration_modality/ranked_go_park_no_go.tsv",
        ("gene",),
        ("call",),
        ("rank_score",),
        ("decision_reason", "needed_to_reopen", "prior_art_signal", "safety"),
        ("genetic_anchor", "target_level_status", "restoration_direction", "current_feasible_modality", "perturbation_evidence"),
        1.05,
        include_no_go=True,
    ),
    SourceSpec(
        "wave25",
        "causal_proxy",
        "results_v3/wave25_causal_genetics_module_proxy/causal_proxy_candidate_matrix.tsv",
        ("gene",),
        ("proxy_call", "wave23_restoration_call"),
        ("overall_proxy_score", "genetics_ready_score", "module_state_score", "perturbation_score"),
        ("primary_blocker", "coloc_mr_blocker", "decision_reason"),
        (
            "ot_n_diseases_score_ge_0_5",
            "ot_diseases_score_ge_0_5",
            "gwas_catalog_trait_count",
            "proper_coloc_or_mr_feasible_this_run",
            "direct_perturbation_support_binary",
            "geneformer_support_contexts",
            "broad_positive_disease_count",
        ),
        1.10,
        include_no_go=True,
    ),
    SourceSpec(
        "wave34",
        "genetics_expression_druggability",
        "results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv",
        ("gene",),
        ("wave34_call", "proxy_call"),
        ("wave34_score", "genetics_ready_score", "druggable_activity_count"),
        ("failed_gates", "manual_blocker_class", "manual_blocker_text_wave34", "primary_blocker"),
        (
            "gwas_catalog_trait_count",
            "local_positive_disease_count",
            "positive_diseases",
            "residual_retained_disease_count",
            "ms_anchor",
            "chembl_target_id",
            "perturbation_or_model_support",
        ),
        1.00,
        max_rows=500,
    ),
    SourceSpec(
        "wave34a",
        "genetics_first_target_rescue",
        "results_v3/wave34a_genetics_first_target_rescue/genetics_first_candidate_rank.tsv",
        ("gene",),
        ("wave34a_call", "wave28_gate_call", "wave14_target_level_call"),
        ("genetics_first_score", "ot_n_diseases_score_ge_0_5", "chembl_activity_count_nM"),
        ("route_reason", "prior_risk", "manual_note"),
        (
            "axis",
            "modality",
            "direction",
            "target_class",
            "ot_diseases_score_ge_0_5",
            "broad_positive_disease_count",
            "residual_positive_disease_count",
            "ms_wm_delta_log2",
        ),
        1.10,
    ),
    SourceSpec(
        "wave38",
        "crispr_state_druggability",
        "results_v3/wave38_crispr_state_druggability_rescue/crispr_state_druggability_rescue_rank.tsv",
        ("gene", "gene_symbol"),
        ("wave38_call", "screen_call", "wave34_call"),
        ("rescue_score", "median_efficient_minus_noneater_lfc", "discovery_priority_score"),
        ("gate_failures", "manual_blocker_class", "primary_blocker"),
        (
            "desired_intervention",
            "directional_disease_support_count",
            "positive_disease_count",
            "positive_diseases",
            "ms_wm_delta_log2",
            "contrast_fdr",
            "druggable_activity_count",
        ),
        1.20,
        include_no_go=True,
    ),
    SourceSpec(
        "wave39",
        "surfaceome_rescue",
        "results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank.tsv",
        ("gene",),
        ("wave39_call", "go_no_go"),
        ("wave39_score", "chembl_activity_count", "positive_disease_count"),
        ("wave39_reason", "demotion_or_support_reason", "prior_flags", "family"),
        (
            "uniprot_accessible",
            "uniprot_locations",
            "positive_diseases",
            "has_ms_anchor",
            "ms_wm_delta_log2",
            "best_positive_fdr",
            "chembl_target_chembl_id",
        ),
        1.00,
    ),
    SourceSpec(
        "wave48",
        "resolution_reopener",
        "results_v3/wave48_resolution_reopener_audit/route_reopener_audit.tsv",
        ("genes",),
        ("call", "wave32_prior_call", "wave32c_translational_verdict"),
        ("critical_gate_pass_count",),
        ("primary_blocker", "wave32_gate_failures", "wave32c_blocking_status"),
        ("route", "description", "route_signal_summary", "lead_reopen_assay"),
        1.05,
        include_no_go=True,
    ),
    SourceSpec(
        "wave52",
        "remaining_reopeners",
        "results_v3/wave52_remaining_mechanistic_reopeners/remaining_reopeners_audit.tsv",
        ("primary_gene", "genes", "candidate"),
        ("call", "source_calls"),
        ("critical_gate_pass_count", "supporting_disease_count_union", "foundation_contexts"),
        ("primary_blocker", "blocker_text", "prior_art_or_crowding_block"),
        (
            "candidate",
            "desired_intervention",
            "reason_for_reopen",
            "local_positive_disease_count",
            "strict_core_covariate_surviving_disease_count",
            "real_perturbation_alignment_pass",
            "chemical_matter",
        ),
        1.05,
        include_no_go=True,
    ),
    SourceSpec(
        "wave55",
        "external_genetics",
        "results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv",
        ("gene",),
        ("foundation_recommendation", "direct_evidence_calls", "closed_axis"),
        ("wave55_score", "n_diseases_genetic_ge_0_5", "best_direct_selectivity_score"),
        ("closed_axis",),
        (
            "approved_name",
            "diseases_genetic_ge_0_5",
            "ms_genetic_association",
            "max_clinical_score",
            "max_literature_score",
            "local_positive_disease_count",
            "strict_residual_disease_count",
        ),
        1.20,
        max_rows=300,
        include_no_go=True,
        include_unlabeled_top=120,
    ),
    SourceSpec(
        "wave57",
        "geneformer",
        "results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv",
        ("gene",),
        ("wave57_call", "screen_call"),
        ("wave57_model_priority_score", "support_contexts", "strong_support_contexts"),
        ("wave57_call",),
        (
            "best_context",
            "supporting_contexts",
            "cross_disease_genetics_pass",
            "local_recurrence_pass",
            "strict_ms_pass",
            "model_support_pass",
            "efferocytosis_pass",
            "critical_gate_pass_count",
        ),
        0.85,
    ),
    SourceSpec(
        "wave60",
        "circuit_coupling",
        "results_v3/wave60_circuit_coupling_pivot/circuit_predictor_rank.tsv",
        ("gene", "predictor"),
        ("wave60_call", "wave57_call", "screen_call"),
        ("combined_fisher_z", "best_abs_rho", "support_contexts", "strong_support_contexts"),
        ("existing_prior_flag", "highlight"),
        (
            "predictor_type",
            "n_diseases",
            "diseases",
            "passes_circuit_coupling",
            "passes_disease_up",
            "passes_ms_anchor",
            "passes_perturbation_hint",
            "positive_diseases",
        ),
        0.90,
        include_unlabeled_top=30,
    ),
    SourceSpec(
        "wave61",
        "perturbation_guardrail",
        "results_v3/wave61_perturbation_first_guardrail/intervention_evidence_tiers.tsv",
        ("gene",),
        ("wave61_call", "evidence_tier", "source"),
        ("direct_priority_score", "selectivity_score", "gate_count", "target_vs_ifn_margin"),
        ("manual_blocker",),
        (
            "dataset",
            "system",
            "perturbation_type",
            "target_suppression",
            "generic_ifn_suppression",
            "gate_real_perturbation",
            "gate_selective_over_ifn",
            "gate_no_manual_blocker",
            "positive_diseases",
        ),
        1.25,
    ),
    SourceSpec(
        "wave62",
        "target_resolution",
        "results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv",
        ("gene",),
        ("wave62_call", "wave34_call", "wave34a_call", "wave61_best_call"),
        ("wave62_score", "max_l2g_score", "max_qtl_h4", "wave55_score"),
        ("manual_blocker", "prior_context_blocker", "wave61_best_manual_blocker"),
        (
            "approved_name",
            "best_l2g_disease",
            "strong_l2g_disease_count",
            "strong_l2g_diseases",
            "strong_qtl_coloc_disease_count",
            "strong_qtl_coloc_diseases",
            "myeloid_qtl_coloc_disease_count",
            "ms_max_l2g_score",
            "ms_max_relevant_qtl_h4",
        ),
        1.30,
    ),
    SourceSpec(
        "wave63",
        "transition_controller",
        "results_v3/wave63_transition_controller_integrator/transition_controller_candidates.tsv",
        ("gene", "candidate", "intervention_node"),
        ("wave63_call", "wave62_call", "wave31_call", "wave34_call", "wave57_call", "wave61_call"),
        ("wave63_score", "gate_pass_count", "direct_selectivity_score", "direct_target_suppression"),
        ("failed_gates", "manual_or_prior_blocker"),
        (
            "source_reason",
            "strong_l2g_disease_count",
            "relevant_qtl_coloc_disease_count",
            "wave55_genetic_disease_count",
            "local_positive_disease_count",
            "real_perturbation",
            "foundation_model_support",
            "route_druggability",
        ),
        1.20,
        include_no_go=True,
    ),
    SourceSpec(
        "wave68",
        "unrestricted_gene_screen",
        "results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv",
        ("gene",),
        ("wave68_call", "wave62_call"),
        ("integrated_score", "perturbation_strength", "wave62_score", "wave55_score"),
        ("manual_blocker", "prior_context_blocker", "wave68_posthoc_blocker"),
        (
            "cell_state",
            "remission_adjusted_delta",
            "remission_adjusted_fdr",
            "paired_fdr",
            "has_cross_autoimmune_genetics",
            "has_any_druggability_flag",
            "strong_l2g_disease_count",
            "strong_qtl_coloc_disease_count",
            "myeloid_qtl_coloc_disease_count",
        ),
        1.35,
        max_rows=500,
        include_unlabeled_top=120,
    ),
    SourceSpec(
        "wave70",
        "fc_ros_resolution_closure",
        "results_v3/wave70_fc_ros_resolution_matrix/fc_ros_resolution_candidate_matrix.tsv",
        ("gene",),
        ("wave70_call", "wave62_call", "wave57_call", "wave61_call"),
        ("wave70_score", "evidence_count"),
        ("manual_blocker", "wave61_manual_blocker"),
        ("route", "gse282122_best_call", "strong_l2g_diseases", "strong_qtl_coloc_diseases"),
        0.50,
        include_no_go=True,
    ),
    SourceSpec(
        "wave70b",
        "fc_ros_computational_closure",
        "results_v3/wave70b_fc_ros_computational_scout/integrated_fc_ros_candidate_scout.tsv",
        ("gene",),
        ("integrated_call", "wave68_best_call", "ra_antitnf_call", "ra_response_call", "wave37_screen_call"),
        ("support_score_0_9", "geneformer_support_contexts_max", "geneformer_strong_support_contexts_max"),
        ("manual_or_empirical_blocker",),
        (
            "gse282122_response_call",
            "ms_gse111972_call",
            "positive_disease_count",
            "positive_diseases",
            "has_cross_autoimmune_genetics",
            "has_any_druggability_flag_wave68",
        ),
        0.50,
        include_no_go=True,
    ),
    SourceSpec(
        "wave70c",
        "fc_ros_geneformer_direction_closure",
        "results_v3/wave70c_inhibitory_receptor_geneformer_direction/geneformer_direction_candidate_calls.tsv",
        ("gene",),
        ("direction_model_call", "wave70_call"),
        ("geneformer_direction_priority_score", "support_contexts", "strong_support_contexts"),
        ("manual_blocker",),
        ("directional_interpretation", "best_context", "supporting_contexts"),
        0.45,
        include_no_go=True,
    ),
]


HARD_BLOCKED_EXACT = {
    "ACSL1": "closed_prior_branch_acsl1",
    "NAMPT": "closed_prior_branch_nampt",
    "SP140": "closed_prior_branch_sp140",
    "INPP5D": "wave70_failed_reopener_threshold_ship1",
    "LILRB2": "wave70_failed_reopener_threshold_lilrb2",
    "SYK": "closed_fc_ros_syk_comparator",
    "BTK": "closed_fc_ros_btk_comparator",
    "FCGR2A": "closed_fc_receptor_branch",
    "FCGR2B": "closed_fc_receptor_branch",
    "FCGR3A": "closed_fc_receptor_branch",
    "FCGR3B": "closed_fc_receptor_branch",
    "FCGR1A": "closed_fc_receptor_branch",
    "NCF1": "closed_nox_ros_branch",
    "NCF2": "closed_nox_ros_branch",
    "NCF4": "closed_nox_ros_branch",
    "CYBB": "closed_nox_ros_branch",
    "CYBA": "closed_nox_ros_branch",
    "PIK3CD": "closed_pi3k_comparator",
    "PIK3CG": "closed_pi3k_comparator",
    "PIK3R1": "closed_pi3k_comparator",
    "PIK3R2": "closed_pi3k_comparator",
    "CD274": "closed_checkpoint_comparator",
    "PDCD1": "closed_checkpoint_comparator",
    "PDCD1LG2": "closed_checkpoint_comparator",
    "CTLA4": "closed_checkpoint_costimulation_comparator",
    "CD28": "closed_checkpoint_costimulation_comparator",
    "CD80": "closed_costimulation_comparator",
    "CD86": "closed_costimulation_comparator",
    "CD40": "prior_art_saturated_costimulation",
    "CD40LG": "prior_art_saturated_costimulation",
    "ICOS": "prior_art_saturated_costimulation",
    "ICOSLG": "prior_art_saturated_costimulation",
}

HARD_BLOCKED_PREFIXES = {
    "FCGR": "closed_fc_receptor_family",
    "JAK": "closed_jak_comparator_family",
}

BROAD_HOST_DEFENSE = {
    "TNF": "broad_host_defense_ms_direction_risk",
    "TNFRSF1A": "broad_host_defense_ms_direction_risk",
    "IL6R": "prior_art_saturated_cytokine_axis",
    "IL6": "broad_host_defense_cytokine_axis",
    "IL12A": "prior_art_saturated_cytokine_axis",
    "IL12B": "prior_art_saturated_cytokine_axis",
    "IL23A": "prior_art_saturated_cytokine_axis",
    "IL7R": "prior_art_saturated_cytokine_axis",
    "STAT1": "generic_ifn_jak_stat_axis",
    "STAT3": "generic_jak_stat_axis",
    "STAT4": "generic_jak_stat_axis",
    "STAT5A": "generic_jak_stat_axis",
    "STAT5B": "generic_jak_stat_axis",
    "TYK2": "prior_art_saturated_jak_stat_axis",
    "NFKB1": "generic_nfkb_host_defense",
    "NFKB2": "generic_nfkb_host_defense",
    "RELA": "generic_nfkb_host_defense",
    "MYD88": "generic_tlr_host_defense",
    "IRF5": "broad_innate_tf_no_selective_modality",
    "IRF7": "broad_innate_tf_no_selective_modality",
    "HIF1A": "broad_metabolic_stress_host_defense",
    "CFB": "prior_art_saturated_complement_axis",
    "C3": "prior_art_saturated_complement_axis",
    "CFD": "prior_art_saturated_complement_axis",
    "PSMB8": "broad_antigen_processing_immunoproteasome",
    "PSMB9": "broad_antigen_processing_immunoproteasome",
    "PSMA6": "broad_antigen_processing_proteasome",
    "TAP1": "broad_antigen_processing_transporter",
    "TAP2": "broad_antigen_processing_transporter",
    "PTPRC": "pan_leukocyte_broad_immune_node",
    "HLA-DRA": "broad_antigen_presentation",
    "HLA-DRB1": "broad_antigen_presentation",
    "HLA-DMA": "broad_antigen_presentation",
}

PRIOR_ART_SATURATED = {
    "PTPN2": "wrong_direction_restoration_and_prior_art_saturated",
    "PTPN22": "wrong_direction_restoration_and_prior_art_saturated",
    "GPR65": "prior_reopener_blocked_by_local_evidence_gap",
    "CXCR2": "prior_art_and_safety_saturated_neutrophil_axis",
    "OSMR": "prior_branch_blocked",
    "SLC15A4": "prior_branch_blocked",
    "TASL": "prior_branch_blocked",
    "SQLE": "prior_wave_failfast_no_ms_or_genetic_support",
}

CHANNEL_FAMILIES = {
    "genetics": {"genetics_restoration", "causal_proxy", "genetics_expression_druggability", "genetics_first_target_rescue", "external_genetics", "target_resolution", "unrestricted_gene_screen"},
    "perturbation": {"crispr_state_druggability", "geneformer", "perturbation_guardrail", "transition_controller", "unrestricted_gene_screen", "fc_ros_geneformer_direction_closure"},
    "modality": {"residual_druggability", "genetics_expression_druggability", "genetics_first_target_rescue", "surfaceome_rescue", "external_genetics", "perturbation_guardrail", "transition_controller"},
    "expression": {"residual_druggability", "surfaceome_rescue", "circuit_coupling", "unrestricted_gene_screen"},
    "reopener": {"resolution_reopener", "remaining_reopeners"},
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    text = str(value).strip()
    if text.lower() in {"", "nan", "none", "null"}:
        return ""
    return re.sub(r"\s+", " ", text)


def to_float(value: Any, default: float = np.nan) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def gene_tokens(value: Any) -> list[str]:
    text = clean_text(value)
    if not text:
        return []
    tokens = re.split(r"[;,/|+\s]+", text)
    genes: list[str] = []
    for token in tokens:
        gene = re.sub(r"[^A-Za-z0-9_.-]", "", token).upper()
        if not gene or len(gene) < 2:
            continue
        if gene in {"AND", "OR", "NA", "NAN", "NONE", "NULL", "GENES", "ROUTE"}:
            continue
        genes.append(gene)
    return sorted(set(genes))


def first_present(row: pd.Series, cols: tuple[str, ...]) -> str:
    vals = [clean_text(row.get(col, "")) for col in cols if col in row.index]
    vals = [v for v in vals if v and v.lower() not in {"true", "false"}]
    return "; ".join(vals)


def call_status(call_text: str) -> str:
    c = call_text.upper()
    if not c:
        return "unlabeled"
    if any(k in c for k in ["NO_GO", "DEMOTE", "BLOCKED", "FAIL", "INSUFFICIENT", "CONTRADICT", "LOW_TOKEN", "LOCAL_SUPPORT_WEAK", "DO_NOT_PROMOTE"]):
        return "hard_no"
    if any(k in c for k in ["PARK", "REVIEW", "REOPEN", "COLOC_NEEDED", "TARGET_RESOLVED", "INTERSECTION"]):
        return "parked"
    if any(k in c for k in ["GO", "PASS", "SUPPORT", "PROMOTE", "POSITIVE", "REMISSION_ADJUSTED"]):
        return "positive"
    return "unlabeled"


def channel_score(status: str, score_pct: float, spec: SourceSpec) -> float:
    status_bonus = {
        "positive": 0.70,
        "parked": 0.45,
        "unlabeled": 0.15,
        "hard_no": -0.35,
    }[status]
    return spec.weight * (status_bonus + 0.85 * score_pct)


def hard_block_reason(gene: str) -> str:
    if gene in HARD_BLOCKED_EXACT:
        return HARD_BLOCKED_EXACT[gene]
    for prefix, reason in HARD_BLOCKED_PREFIXES.items():
        if gene.startswith(prefix):
            return reason
    return ""


def soft_penalty_reason(gene: str) -> str:
    if gene in BROAD_HOST_DEFENSE:
        return BROAD_HOST_DEFENSE[gene]
    if gene in PRIOR_ART_SATURATED:
        return PRIOR_ART_SATURATED[gene]
    return ""


def row_numeric_score(row: pd.Series, spec: SourceSpec) -> float:
    vals = [abs(to_float(row.get(col))) for col in spec.score_cols if col in row.index and np.isfinite(to_float(row.get(col)))]
    if not vals:
        return np.nan
    return max(vals)


def read_source(spec: SourceSpec) -> tuple[pd.DataFrame, dict[str, Any]]:
    path = ROOT / spec.path
    meta = {"wave": spec.wave, "channel": spec.channel, "path": spec.path, "exists": path.exists(), "rows_read": 0, "rows_used": 0}
    if not path.exists():
        return pd.DataFrame(), meta
    df = pd.read_csv(path, sep="\t", low_memory=False)
    meta["rows_read"] = int(len(df))
    if spec.max_rows and len(df) > spec.max_rows:
        score = df.apply(lambda r: row_numeric_score(r, spec), axis=1)
        df = df.assign(_source_numeric_score=score).sort_values("_source_numeric_score", ascending=False, na_position="last").head(spec.max_rows)
    else:
        df = df.assign(_source_numeric_score=df.apply(lambda r: row_numeric_score(r, spec), axis=1))
    if df["_source_numeric_score"].notna().any():
        ranks = df["_source_numeric_score"].rank(pct=True, method="average").fillna(0.0)
    else:
        ranks = pd.Series(0.0, index=df.index)
    out_rows: list[dict[str, Any]] = []
    for idx, row in df.iterrows():
        genes: list[str] = []
        for col in spec.gene_cols:
            if col in row.index:
                genes.extend(gene_tokens(row.get(col)))
        genes = sorted(set(genes))
        if not genes:
            continue
        call_text = first_present(row, spec.call_cols)
        status = call_status(call_text)
        if status == "hard_no" and not spec.include_no_go:
            # Keep hard negative information in explicitly requested closure
            # sources, but avoid filling the rank with thousands of inert rows.
            continue
        if status == "unlabeled" and spec.include_unlabeled_top <= 0:
            continue
        if status == "unlabeled":
            numeric_rank = int((df["_source_numeric_score"].rank(method="first", ascending=False, na_option="bottom")).loc[idx])
            if numeric_rank > spec.include_unlabeled_top:
                continue
        blocker_text = first_present(row, spec.blocker_cols)
        evidence_text = first_present(row, spec.evidence_cols)
        score_pct = float(ranks.loc[idx]) if idx in ranks.index else 0.0
        points = channel_score(status, score_pct, spec)
        for gene in genes:
            out_rows.append(
                {
                    "gene": gene,
                    "wave": spec.wave,
                    "channel": spec.channel,
                    "source_path": spec.path,
                    "source_row_index": int(idx),
                    "call_text": call_text,
                    "status": status,
                    "source_numeric_score": to_float(row.get("_source_numeric_score")),
                    "source_score_percentile": score_pct,
                    "channel_points": points,
                    "blocker_text": blocker_text,
                    "evidence_text": evidence_text,
                }
            )
    meta["rows_used"] = int(len(out_rows))
    return pd.DataFrame(out_rows), meta


def compact_join(values: list[str], limit: int = 8) -> str:
    seen: list[str] = []
    for value in values:
        for part in re.split(r"\s*;\s*", clean_text(value)):
            part = clean_text(part)
            if part.lower() in {"true", "false"}:
                continue
            if part and part not in seen:
                seen.append(part)
    if len(seen) > limit:
        return "; ".join(seen[:limit]) + f"; ...(+{len(seen) - limit})"
    return "; ".join(seen)


def summarize_gene(gene: str, gd: pd.DataFrame) -> dict[str, Any]:
    positive = gd[gd["status"].isin(["positive", "parked", "unlabeled"])].copy()
    hard_no = gd[gd["status"].eq("hard_no")].copy()
    channel_set = set(positive["channel"])
    family_counts = {family: len(channel_set & channels) for family, channels in CHANNEL_FAMILIES.items()}
    raw_points = float(gd["channel_points"].sum())
    positive_points = float(positive["channel_points"].clip(lower=0).sum())
    hard_no_penalty = 0.70 * len(set(hard_no["channel"]))
    hard_reason = hard_block_reason(gene)
    soft_reason = soft_penalty_reason(gene)
    hard_penalty = 12.0 if hard_reason else 0.0
    soft_penalty = 3.5 if soft_reason else 0.0
    broad_prior_text = " ".join([compact_join(gd["blocker_text"].tolist(), limit=20), compact_join(gd["call_text"].tolist(), limit=20)]).lower()
    text_penalty_terms = [
        "prior_art",
        "saturated",
        "broad",
        "host_defense",
        "wrong_direction",
        "l1000_only",
        "needs_real_perturbation",
        "unresolved target",
        "unresolved_target",
        "non-obvious target",
        "core machinery",
        "generic",
        "no_target_resolved_coloc",
    ]
    text_prior_penalty = 1.5 if any(k in broad_prior_text for k in text_penalty_terms) else 0.0
    meta_score = positive_points - hard_no_penalty - hard_penalty - soft_penalty - text_prior_penalty
    strong_modalities = sum(1 for key in ["genetics", "perturbation", "modality"] if family_counts[key] > 0)
    reopener_ready = (
        not hard_reason
        and meta_score >= 7.5
        and len(channel_set) >= 5
        and strong_modalities == 3
        and family_counts["genetics"] >= 2
        and family_counts["perturbation"] >= 1
        and family_counts["modality"] >= 1
        and len(set(hard_no["channel"])) <= 2
        and not soft_reason
    )
    if reopener_ready:
        call = "REOPEN_REVIEW"
        reason = "multi_channel_genetics_perturbation_modality_convergence_without_explicit_branch_blocker"
    elif hard_reason:
        call = "NO_REOPEN_BLOCKED_BRANCH"
        reason = hard_reason
    elif soft_reason:
        call = "PARK_PRIOR_ART_OR_HOST_DEFENSE_PENALIZED"
        reason = soft_reason
    elif meta_score >= 5.0 and len(channel_set) >= 3:
        call = "PARK_SURVIVOR_NO_REOPEN"
        reason = "survives_existing_artifact_meta_rank_but_misses_reopener_threshold"
    else:
        call = "NO_REOPEN_INSUFFICIENT_CONVERGENCE"
        reason = "insufficient_independent_convergence_after_guardrails"
    return {
        "gene": gene,
        "wave71_call": call,
        "wave71_reason": reason,
        "meta_score": round(meta_score, 6),
        "raw_channel_points": round(raw_points, 6),
        "positive_channel_points": round(positive_points, 6),
        "hard_no_channel_penalty": round(hard_no_penalty, 6),
        "hard_block_penalty": hard_penalty,
        "soft_prior_penalty": soft_penalty,
        "text_prior_penalty": text_prior_penalty,
        "evidence_channel_count": int(len(channel_set)),
        "positive_status_count": int((gd["status"].eq("positive")).sum()),
        "parked_status_count": int((gd["status"].eq("parked")).sum()),
        "hard_no_status_count": int((gd["status"].eq("hard_no")).sum()),
        "genetics_channel_count": int(family_counts["genetics"]),
        "perturbation_channel_count": int(family_counts["perturbation"]),
        "modality_channel_count": int(family_counts["modality"]),
        "expression_channel_count": int(family_counts["expression"]),
        "reopener_channel_count": int(family_counts["reopener"]),
        "evidence_channels": ";".join(sorted(channel_set)),
        "hard_block_reason": hard_reason,
        "soft_penalty_reason": soft_reason,
        "top_calls": compact_join(gd.sort_values("channel_points", ascending=False)["call_text"].tolist(), limit=8),
        "evidence_summary": compact_join(gd.sort_values("channel_points", ascending=False)["evidence_text"].tolist(), limit=10),
        "blockers": compact_join(gd["blocker_text"].tolist(), limit=10),
        "source_waves": ";".join(sorted(set(gd["wave"]))),
    }


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def markdown_table(df: pd.DataFrame, cols: list[str], n: int = 10) -> str:
    sub = df.head(n).copy()
    if sub.empty:
        return "_No rows._\n"
    lines = ["|" + "|".join(cols) + "|", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, row in sub.iterrows():
        vals = []
        for col in cols:
            text = clean_text(row.get(col, ""))
            text = text.replace("|", "/")
            if len(text) > 130:
                text = text[:127] + "..."
            vals.append(text)
        lines.append("|" + "|".join(vals) + "|")
    return "\n".join(lines) + "\n"


def write_report(rank: pd.DataFrame, evidence: pd.DataFrame, source_meta: list[dict[str, Any]]) -> None:
    top = rank.head(10)
    reopen = rank[rank["wave71_call"].eq("REOPEN_REVIEW")]
    call_counts = rank["wave71_call"].value_counts().to_dict()
    report = [
        "# Wave71-A Global Survivor Meta-Rank",
        "",
        f"Random seed: `{SEED}`. No new external data were fetched.",
        "",
        "## Decision",
        "",
        (
            "No candidate meets the Wave71-A reopen threshold."
            if reopen.empty
            else f"{len(reopen)} candidate(s) meet the Wave71-A reopen-review threshold."
        ),
        "",
        "The threshold required non-blocked convergence across genetics, perturbation, and modality channels. "
        "Closed Fc/ROS, JAK/SYK/BTK/PI3K, checkpoint/costimulation, ACSL1, NAMPT, SP140, LILRB2, and INPP5D branches were explicitly blocked.",
        "",
        "## Top 10 After Guardrails",
        "",
        markdown_table(
            top,
            [
                "gene",
                "wave71_call",
                "meta_score",
                "evidence_channel_count",
                "genetics_channel_count",
                "perturbation_channel_count",
                "modality_channel_count",
                "wave71_reason",
            ],
            10,
        ),
        "",
        "## Top 10 Evidence And Blockers",
        "",
        markdown_table(top, ["gene", "evidence_channels", "top_calls", "blockers"], 10),
        "",
        "## Inputs Used",
        "",
        markdown_table(pd.DataFrame(source_meta), ["wave", "channel", "exists", "rows_read", "rows_used", "path"], len(source_meta)),
        "",
        "## Output Files",
        "",
        f"- `{rel(OUT / 'global_survivor_meta_rank.tsv')}`",
        f"- `{rel(OUT / 'evidence_long.tsv')}`",
        f"- `{rel(OUT / 'summary.json')}`",
        f"- `{rel(OUT / 'REPORT.md')}`",
        f"- `{rel(SUBAGENT)}`",
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report), encoding="utf-8")

    subagent = [
        "# Wave71-A Subagent Report: Global Survivor Meta-Rank",
        "",
        "## Bottom Line",
        "",
        (
            "No candidate should reopen from this existing-artifact meta-rank. "
            "Several genes remain parked as surveillance items, but all miss the multi-channel reopener threshold or carry branch/prior-art blockers."
            if reopen.empty
            else "One or more candidates reached REOPEN_REVIEW; inspect the TSV before acting."
        ),
        "",
        "## Top 10 Candidates",
        "",
        markdown_table(
            top,
            [
                "gene",
                "wave71_call",
                "meta_score",
                "evidence_channels",
                "wave71_reason",
                "blockers",
            ],
            10,
        ),
        "",
        "## Reopen Assessment",
        "",
        "- Reopen now: " + ("none" if reopen.empty else ", ".join(reopen["gene"].head(20).tolist())),
        "- Main blockers: closed Fc/ROS or comparator branch, prior-art saturation, broad host-defense biology, missing real perturbation, missing target-resolved causal genetics, or missing actionable selective modality.",
        "- Interpretation: this is a reproducible triage rank over existing V3 artifacts, not a new biological claim.",
        "",
        "## Call Counts",
        "",
    ]
    for key, value in call_counts.items():
        subagent.append(f"- `{key}`: {value}")
    subagent.append("")
    SUBAGENT.write_text("\n".join(subagent), encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    SUBAGENT.parent.mkdir(parents=True, exist_ok=True)

    evidence_frames: list[pd.DataFrame] = []
    source_meta: list[dict[str, Any]] = []
    for spec in SOURCES:
        frame, meta = read_source(spec)
        source_meta.append(meta)
        if not frame.empty:
            evidence_frames.append(frame)
    if evidence_frames:
        evidence = pd.concat(evidence_frames, ignore_index=True)
    else:
        evidence = pd.DataFrame(
            columns=[
                "gene",
                "wave",
                "channel",
                "source_path",
                "source_row_index",
                "call_text",
                "status",
                "source_numeric_score",
                "source_score_percentile",
                "channel_points",
                "blocker_text",
                "evidence_text",
            ]
        )
    evidence = evidence.sort_values(["gene", "wave", "channel", "source_row_index"]).reset_index(drop=True)
    evidence.to_csv(OUT / "evidence_long.tsv", sep="\t", index=False)

    rows = [summarize_gene(gene, gd) for gene, gd in evidence.groupby("gene", sort=True)]
    rank = pd.DataFrame(rows)
    if not rank.empty:
        call_priority = {
            "REOPEN_REVIEW": 0,
            "PARK_SURVIVOR_NO_REOPEN": 1,
            "NO_REOPEN_INSUFFICIENT_CONVERGENCE": 2,
            "PARK_PRIOR_ART_OR_HOST_DEFENSE_PENALIZED": 3,
            "NO_REOPEN_BLOCKED_BRANCH": 4,
        }
        rank["_call_priority"] = rank["wave71_call"].map(call_priority).fillna(9)
        rank = rank.sort_values(
            ["_call_priority", "meta_score", "evidence_channel_count", "genetics_channel_count", "perturbation_channel_count", "gene"],
            ascending=[True, False, False, False, False, True],
        ).drop(columns=["_call_priority"])
    rank.to_csv(OUT / "global_survivor_meta_rank.tsv", sep="\t", index=False)

    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "candidate_count": int(len(rank)),
        "evidence_row_count": int(len(evidence)),
        "source_count": len(SOURCES),
        "source_meta": source_meta,
        "call_counts": rank["wave71_call"].value_counts().to_dict() if not rank.empty else {},
        "reopen_candidates": rank.loc[rank["wave71_call"].eq("REOPEN_REVIEW"), "gene"].tolist() if not rank.empty else [],
        "top_10": rank.head(10).to_dict(orient="records") if not rank.empty else [],
        "threshold": {
            "minimum_meta_score": 7.5,
            "minimum_evidence_channels": 5,
            "required_channel_families": ["genetics", "perturbation", "modality"],
            "minimum_genetics_channels": 2,
            "maximum_hard_no_channels": 2,
            "hard_blocked_families": ["ACSL1", "NAMPT", "SP140", "FCGR*", "NOX/NCF/CYBB/CYBA", "JAK*", "SYK", "BTK", "PI3K", "checkpoint", "costimulation", "LILRB2", "INPP5D"],
        },
        "interpretation": "No candidate should reopen unless listed in reopen_candidates; hard-blocked Wave70/Fc/ROS comparators remain closed.",
    }
    write_json(OUT / "summary.json", summary)
    write_report(rank, evidence, source_meta)


if __name__ == "__main__":
    main()
