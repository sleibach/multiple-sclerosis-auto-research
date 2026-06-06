#!/usr/bin/env python3
"""Wave83 intervention-class-first meta-rank.

Prior branches repeatedly started from genes or cell-state markers and then
failed at druggability/direction. This wave inverts the order: start from
reachable intervention classes already tested in V3, then ask whether any class
also has MS anchoring, cross-autoimmune module relevance, perturbation/response
support, and a non-blocked novelty/safety path.

The output is a forcing function, not a finding claim.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_direct_h5ad_cell_states import ROOT


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave83_intervention_class_meta_rank"

W23 = ROOT / "phases/v3/results" / "wave23_metabolite_barrier_circuit" / "wave23_ranked_routes.tsv"
W44_CFB = ROOT / "phases/v3/results" / "wave44_cfb_complement_stratification_audit" / "wave21_prior_CFB_row.tsv"
W48_ROUTE = ROOT / "phases/v3/results" / "wave48_resolution_reopener_audit" / "route_reopener_audit.tsv"
W48_MATRIX = ROOT / "phases/v3/results" / "wave48_resolution_reopener_audit" / "decision_matrix.tsv"
W50_GPR65 = ROOT / "phases/v3/results" / "wave50_gpr65_acid_sensing_gpcr_audit" / "gpr65_audit.tsv"
W53 = ROOT / "phases/v3/results" / "wave53_perturbation_first_pivot" / "perturbation_first_audit.tsv"
W54 = ROOT / "phases/v3/results" / "wave54_mfge8_debris_opsonin_audit" / "decision_matrix.tsv"
W58 = ROOT / "phases/v3/results" / "wave58_cxcr2_il7r_targeted_audit" / "cxcr2_il7r_decision.tsv"
W59 = ROOT / "phases/v3/results" / "wave59_lysosomal_sphingolipid_model_reopener_audit" / "lysosomal_sphingolipid_decision.tsv"
W64 = ROOT / "phases/v3/results" / "wave64_slamf7_perturbation_audit" / "wave64c_gate_row.tsv"
W72 = ROOT / "phases/v3/results" / "wave72_lipid_mediator_intervention_scout" / "lipid_mediator_decisions.tsv"
W73 = ROOT / "phases/v3/results" / "wave73_p2rx7_stratification_test" / "p2rx7_stratification_decision.tsv"
W74_GPR183 = ROOT / "phases/v3/results" / "wave74_gpr183_oxysterol_niche" / "integrated_decision.tsv"
W74_EPHX2 = ROOT / "phases/v3/results" / "wave74_ephx2_oxylipin_specificity" / "final_decision.tsv"
W78 = ROOT / "phases/v3/results" / "wave78_lilrb_inhibitory_receptor_audit" / "lilrb_integrated_decision.tsv"
W79 = ROOT / "phases/v3/results" / "wave79_targetability_shortlist_audit" / "targetability_integrated_decision.tsv"
W80 = ROOT / "phases/v3/results" / "wave80_cd58_cd2_axis_deepening" / "cd58_cd2_axis_decision.tsv"
W82 = ROOT / "phases/v3/results" / "wave82_parked_intervention_route_audit" / "parked_intervention_route_audit.tsv"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none"} else text


def num(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def flag(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    text = clean_text(value).lower()
    return int(text in {"true", "1", "yes", "pass", "passed"})


def markdown_table(df: pd.DataFrame, max_rows: int = 40) -> str:
    if df.empty:
        return "_No rows._"
    view = df.head(max_rows).copy()
    cols = list(view.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in view.iterrows():
        values = []
        for col in cols:
            value = row[col]
            if isinstance(value, float):
                values.append("" if math.isnan(value) else f"{value:.4g}")
            else:
                values.append(clean_text(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def row_template(
    *,
    candidate: str,
    intervention_class: str,
    source_wave: str,
    mechanism: str,
    modality: str,
    direction: str,
) -> dict[str, Any]:
    return {
        "candidate": candidate,
        "intervention_class": intervention_class,
        "source_wave": source_wave,
        "mechanism": mechanism,
        "modality": modality,
        "direction": direction,
        "reachable_modality": 0,
        "direct_perturbation": 0,
        "foundation_model": 0,
        "cross_disease_cellstate": 0,
        "cross_disease_count": 0.0,
        "ms_anchor": 0,
        "genetic_or_target_resolution": 0,
        "response_support": 0,
        "biochemical_support": 0,
        "specificity_support": 0,
        "prior_not_blocked": 0,
        "safety_direction_clear": 0,
        "primary_blocker": "",
        "source_call": "",
        "source_value": "",
    }


def add_wave23(rows: list[dict[str, Any]]) -> None:
    df = read_tsv(W23)
    if df.empty:
        return
    for _, r in df.iterrows():
        row = row_template(
            candidate=clean_text(r.get("route")),
            intervention_class=clean_text(r.get("route_label")),
            source_wave="wave23_metabolite_barrier_circuit",
            mechanism=clean_text(r.get("route_label")),
            modality=clean_text(r.get("modality")),
            direction=clean_text(r.get("direction")),
        )
        row.update(
            {
                "reachable_modality": int(num(r.get("genes_with_chembl_activity")) > 0 or num(r.get("lincs_metadata_presence_count_capped")) > 0),
                "direct_perturbation": int(num(r.get("l1000_opposite_qval_le_0_05_count")) > 0),
                "cross_disease_cellstate": int(num(r.get("route_positive_disease_union_count")) >= 3),
                "cross_disease_count": num(r.get("route_positive_disease_union_count")),
                "ms_anchor": int(num(r.get("best_ms_wm_p"), 1.0) <= 0.05 and num(r.get("best_ms_wm_delta_log2")) > 0),
                "genetic_or_target_resolution": int(num(r.get("local_genetics_ge_0_5_disease_union_count")) >= 2),
                "prior_not_blocked": int(not flag(r.get("crowded_prior_art_flag"))),
                "safety_direction_clear": int(clean_text(r.get("not_already_crowded_assessment")) == "least_crowded_but_unsupported"),
                "primary_blocker": clean_text(r.get("manual_prior_blocker")) or clean_text(r.get("gate_rationale")),
                "source_call": clean_text(r.get("gate_call")),
                "source_value": f"route_positive_disease_union_count={num(r.get('route_positive_disease_union_count'))}; l1000_qval_hits={num(r.get('l1000_opposite_qval_le_0_05_count'))}",
            }
        )
        rows.append(row)


def add_wave48(rows: list[dict[str, Any]]) -> None:
    route = read_tsv(W48_ROUTE)
    matrix = read_tsv(W48_MATRIX)
    if route.empty:
        return
    r = route.iloc[0]
    gates = matrix[matrix["route"].eq("FPR2_ANXA1_BIASED_RESOLUTION")] if not matrix.empty else pd.DataFrame()
    gate = {str(x["gate"]): flag(x["passed"]) for _, x in gates.iterrows()} if not gates.empty else {}
    row = row_template(
        candidate="FPR2_ANXA1_BIASED_RESOLUTION",
        intervention_class="Biased pro-resolution GPCR / ANXA1 mimetic",
        source_wave="wave48_resolution_reopener_audit",
        mechanism="FPR2/ALX biased agonism or ANXA1-mimetic resolution signaling",
        modality="small molecule or peptide biased agonist; pro-resolution biologic",
        direction="agonize pro-resolution signaling while avoiding inflammatory FPR2 modes",
    )
    row.update(
        {
            "reachable_modality": gate.get("druggability_selectivity", 0),
            "direct_perturbation": gate.get("real_perturbation_anchor", 0),
            "foundation_model": gate.get("foundation_model_support", 0),
            "cross_disease_cellstate": gate.get("cross_autoimmune_local_signal", 0),
            "cross_disease_count": 4.0 if gate.get("cross_autoimmune_local_signal", 0) else 0.0,
            "ms_anchor": gate.get("strict_ms_anchor", 0),
            "prior_not_blocked": gate.get("prior_art_not_blocking", 0),
            "safety_direction_clear": gate.get("specific_directionality", 0),
            "primary_blocker": clean_text(r.get("primary_blocker")),
            "source_call": clean_text(r.get("call")),
            "source_value": clean_text(r.get("route_signal_summary")),
        }
    )
    rows.append(row)


def add_wave54(rows: list[dict[str, Any]]) -> None:
    df = read_tsv(W54)
    if df.empty:
        return
    gates = {str(x["gate"]): flag(x["passed"]) for _, x in df.iterrows()}
    values = {str(x["gate"]): clean_text(x["value"]) for _, x in df.iterrows()}
    row = row_template(
        candidate="MFGE8_DEBRIS_OPSONIN",
        intervention_class="Debris-opsonin / efferocytosis biologic",
        source_wave="wave54_mfge8_debris_opsonin_audit",
        mechanism="MFGE8 bridging of apoptotic or myelin debris to phagocytes",
        modality="secreted recombinant protein or engineered local biologic",
        direction="augment debris clearance while avoiding bystander phagocytosis",
    )
    row.update(
        {
            "reachable_modality": gates.get("tractable_modality", 0),
            "direct_perturbation": gates.get("efferocytosis_screen_support", 0),
            "cross_disease_cellstate": gates.get("local_cross_autoimmune_cell_state", 0),
            "cross_disease_count": 1.0 if "positive=1" in values.get("local_cross_autoimmune_cell_state", "") else 0.0,
            "ms_anchor": gates.get("strict_ms_anchor", 0),
            "prior_not_blocked": gates.get("novelty_prior_art_unblocked", 0),
            "safety_direction_clear": gates.get("safety_bystander_phagocytosis_resolved", 0),
            "primary_blocker": "cross-autoimmune/MS/efferocytosis/safety gates fail",
            "source_call": "PARK_BIOLOGIC_ROUTE_NOT_PROMOTED",
            "source_value": "; ".join(f"{k}={v}" for k, v in values.items()),
        }
    )
    rows.append(row)


def add_simple_decision_rows(rows: list[dict[str, Any]]) -> None:
    # GPR65 acid-sensing GPCR
    df = read_tsv(W50_GPR65)
    if not df.empty:
        r = df.iloc[0]
        row = row_template(
            candidate="GPR65_ACID_SENSING_GPCR",
            intervention_class="Acid-sensing GPCR",
            source_wave="wave50_gpr65_acid_sensing_gpcr_audit",
            mechanism="GPR65/TDAG8 pH-sensing immune modulation",
            modality="small-molecule agonist/PAM or GPCR modulator",
            direction="restore or bias GPR65 signaling in acidic inflammatory tissue",
        )
        row.update(
            {
                "reachable_modality": 1,
                "cross_disease_cellstate": 0,
                "cross_disease_count": 1.0,
                "ms_anchor": 0,
                "genetic_or_target_resolution": 1,
                "prior_not_blocked": 0,
                "safety_direction_clear": 0,
                "primary_blocker": clean_text(r.get("primary_blocker")),
                "source_call": clean_text(r.get("call")),
                "source_value": clean_text(r.get("summary")),
            }
        )
        rows.append(row)

    # Complement factor B
    df = read_tsv(W44_CFB)
    if not df.empty:
        r = df.iloc[0]
        row = row_template(
            candidate="CFB_FACTOR_B_INHIBITION",
            intervention_class="Alternative complement inhibition",
            source_wave="wave44_cfb_complement_stratification_audit",
            mechanism="Factor B inhibition of alternative complement amplification",
            modality=clean_text(r.get("modality")),
            direction=clean_text(r.get("intervention_direction")),
        )
        row.update(
            {
                "reachable_modality": 1,
                "cross_disease_cellstate": 1,
                "cross_disease_count": 4.0,
                "ms_anchor": 0,
                "genetic_or_target_resolution": 0,
                "prior_not_blocked": 0,
                "safety_direction_clear": 0,
                "primary_blocker": clean_text(r.get("prior_art_blockers")) + "; " + clean_text(r.get("safety_repair_risks")),
                "source_call": clean_text(r.get("recommendation")),
                "source_value": clean_text(r.get("local_residual_gate")),
            }
        )
        rows.append(row)

    # Perturbation-first routes with chemical matter.
    df = read_tsv(W53)
    for _, r in df.iterrows() if not df.empty else []:
        candidate = clean_text(r.get("route"))
        row = row_template(
            candidate=candidate,
            intervention_class="Perturbation-first transcription/signaling route",
            source_wave="wave53_perturbation_first_pivot",
            mechanism=clean_text(r.get("intervention")),
            modality="small molecule or genetic perturbation depending on route",
            direction=clean_text(r.get("intervention")),
        )
        row.update(
            {
                "reachable_modality": int(flag(r.get("chemical_matter"))),
                "direct_perturbation": int(num(r.get("selectivity_score")) > 0.5),
                "foundation_model": int(num(r.get("foundation_support_rows")) > 0),
                "cross_disease_cellstate": int(num(r.get("local_positive_disease_count")) >= 3 and num(r.get("local_negative_disease_count")) == 0),
                "cross_disease_count": num(r.get("local_positive_disease_count")),
                "ms_anchor": int(num(r.get("ms_wm_p"), 1.0) <= 0.05 and num(r.get("ms_wm_delta_log2")) > 0),
                "genetic_or_target_resolution": int(num(r.get("gwas_trait_count")) >= 4),
                "prior_not_blocked": int("NO_GO" not in clean_text(r.get("call")) and "unsafe" not in clean_text(r.get("manual_safety")).lower()),
                "safety_direction_clear": int(clean_text(r.get("manual_safety")) not in {"high_risk_broad_transcription", "pleiotropic_neuroimmune_metabolic", "ms_directionally_unsafe", "antigen_presentation_host_defense"}),
                "primary_blocker": clean_text(r.get("primary_blocker")),
                "source_call": clean_text(r.get("call")),
                "source_value": f"selectivity={num(r.get('selectivity_score'))}; target_vs_ifn={num(r.get('target_vs_ifn_margin'))}",
            }
        )
        rows.append(row)


def add_lipid_and_receptor_rows(rows: list[dict[str, Any]]) -> None:
    df = read_tsv(W72)
    for _, r in df.iterrows() if not df.empty else []:
        row = row_template(
            candidate=clean_text(r.get("branch")),
            intervention_class="Lipid mediator / danger-metabolite route",
            source_wave="wave72_lipid_mediator_intervention_scout",
            mechanism=clean_text(r.get("branch")),
            modality="small molecule or receptor/enzyme modulation",
            direction=clean_text(r.get("branch")),
        )
        row.update(
            {
                "reachable_modality": 1,
                "cross_disease_cellstate": int(num(r.get("local_positive_disease_count")) >= 3),
                "cross_disease_count": num(r.get("local_positive_disease_count")),
                "genetic_or_target_resolution": int(num(r.get("genetic_anchor_count")) > 0),
                "response_support": int(num(r.get("normalizing_treatment_hit_count")) > 0),
                "biochemical_support": int(num(r.get("biochemical_supportive_disease_count")) >= 2),
                "prior_not_blocked": int("NO_GO" not in clean_text(r.get("wave72_call"))),
                "safety_direction_clear": int("PARK" in clean_text(r.get("wave72_call"))),
                "primary_blocker": clean_text(r.get("decisive_blocker")),
                "source_call": clean_text(r.get("wave72_call")),
                "source_value": f"biochem_diseases={num(r.get('biochemical_supportive_disease_count'))}; treatment_hits={num(r.get('normalizing_treatment_hit_count'))}",
            }
        )
        rows.append(row)

    df = read_tsv(W73)
    if not df.empty:
        r = df.iloc[0]
        row = row_template(
            candidate="P2RX7_PURINERGIC_STRATIFICATION",
            intervention_class="Purinergic inflammasome stratification",
            source_wave="wave73_p2rx7_stratification_test",
            mechanism="P2RX7/NLRP3/IL1B purine-danger module",
            modality="P2RX7 antagonist or purine-high biomarker stratification",
            direction="antagonize P2RX7 only in purine/inflammasome-high subset",
        )
        row.update(
            {
                "reachable_modality": 1,
                "cross_disease_cellstate": flag(r.get("cellstate_broad_support")),
                "cross_disease_count": 3.0 if flag(r.get("cellstate_broad_support")) else 0.0,
                "ms_anchor": flag(r.get("ms_module_anchor")),
                "response_support": int(flag(r.get("gse282122_response_support")) or flag(r.get("ra_response_support"))),
                "biochemical_support": flag(r.get("biochemical_purine_support")),
                "specificity_support": flag(r.get("specificity_vs_generic_modules")),
                "prior_not_blocked": 1,
                "safety_direction_clear": 0,
                "primary_blocker": clean_text(r.get("decision_reason")),
                "source_call": clean_text(r.get("wave73_call")),
                "source_value": f"wave72_supportive_diseases={clean_text(r.get('wave72_supportive_diseases'))}",
            }
        )
        rows.append(row)

    df = read_tsv(W74_GPR183)
    if not df.empty:
        r = df.iloc[0]
        row = row_template(
            candidate="GPR183_EBI2_OXYSTEROL_NICHE",
            intervention_class="Oxysterol-guided immune niche GPCR",
            source_wave="wave74_gpr183_oxysterol_niche",
            mechanism="GPR183/EBI2 oxysterol-guided migration and APC niche",
            modality="GPR183 antagonist/biased modulator",
            direction="modulate oxysterol-guided inflammatory niches",
        )
        row.update(
            {
                "reachable_modality": 1,
                "cross_disease_cellstate": flag(r.get("response_module_cross_disease")),
                "cross_disease_count": num(r.get("coherent_program_disease_count")),
                "ms_anchor": flag(r.get("ms_support")),
                "genetic_or_target_resolution": flag(r.get("target_resolved_genetics_or_druggability")),
                "response_support": int(flag(r.get("ibd_response_support")) or flag(r.get("ra_response_support"))),
                "biochemical_support": flag(r.get("oxysterol_like_metabolite_support")),
                "specificity_support": flag(r.get("specificity_vs_ifn_apc_generic")),
                "prior_not_blocked": 1,
                "safety_direction_clear": flag(r.get("direct_gpr183_receptor_anchor")),
                "primary_blocker": clean_text(r.get("decision_blockers")),
                "source_call": clean_text(r.get("wave74b_call")),
                "source_value": f"gpr183_positive_diseases={clean_text(r.get('gpr183_positive_diseases'))}",
            }
        )
        rows.append(row)

    df = read_tsv(W74_EPHX2)
    if not df.empty:
        r = df.iloc[0]
        row = row_template(
            candidate="EPHX2_SEH_OXYLIPIN_RATIO",
            intervention_class="Oxylipin epoxide/diol enzyme modulation",
            source_wave="wave74_ephx2_oxylipin_specificity",
            mechanism="soluble epoxide hydrolase inhibition to preserve epoxy-fatty acids",
            modality="small-molecule EPHX2/sEH inhibitor",
            direction="inhibit EPHX2 only if EpFA:diol disease ratio is demonstrated",
        )
        row.update(
            {
                "reachable_modality": 1,
                "biochemical_support": int(num(r.get("specific_supportive_disease_count")) >= 1),
                "response_support": int(num(r.get("specific_normalizing_treatment_hit_count")) >= 1),
                "specificity_support": flag(r.get("specificity_vs_generic_modules")),
                "prior_not_blocked": 1,
                "safety_direction_clear": 1,
                "primary_blocker": clean_text(r.get("decision_reason")),
                "source_call": clean_text(r.get("wave74_call")),
                "source_value": f"specific_diseases={num(r.get('specific_supportive_disease_count'))}; ratio_proxy={num(r.get('ratio_proxy_support_count'))}",
            }
        )
        rows.append(row)


def add_surface_and_residual_rows(rows: list[dict[str, Any]]) -> None:
    df = read_tsv(W64)
    if not df.empty:
        r = df.iloc[0]
        row = row_template(
            candidate="SLAMF7_SIGNAL_BIAS",
            intervention_class="Surface immune receptor signal bias",
            source_wave="wave64_slamf7_perturbation_audit",
            mechanism="SLAMF7 engagement or antagonism in myeloid/APC states",
            modality=clean_text(r.get("modality")),
            direction=clean_text(r.get("intervention_direction")),
        )
        row.update(
            {
                "reachable_modality": 1,
                "direct_perturbation": flag(r.get("direct_human_perturbation")),
                "cross_disease_cellstate": 0,
                "ms_anchor": 0,
                "response_support": flag(r.get("heldout_readout_pass")),
                "prior_not_blocked": int(not flag(r.get("prior_art_blocker"))),
                "safety_direction_clear": flag(r.get("direction_matches_claim")),
                "primary_blocker": clean_text(r.get("wave64c_failed_gates")),
                "source_call": clean_text(r.get("wave64c_call")),
                "source_value": f"target_generic_ratio={num(r.get('target_to_generic_effect_ratio'))}",
            }
        )
        rows.append(row)

    df = read_tsv(W78)
    for _, r in df.iterrows() if not df.empty else []:
        if not flag(r.get("is_lilrb_target")):
            continue
        gene = clean_text(r.get("gene"))
        row = row_template(
            candidate=f"{gene}_INHIBITORY_RECEPTOR",
            intervention_class="Myeloid inhibitory receptor",
            source_wave="wave78_lilrb_inhibitory_receptor_audit",
            mechanism=f"{gene} immune inhibitory-receptor modulation",
            modality="antibody, agonist, antagonist, or ligand engineering depending on direction",
            direction="unresolved: restore inhibitory signaling versus block myeloid suppression",
        )
        row.update(
            {
                "reachable_modality": 1,
                "foundation_model": flag(r.get("gate_foundation_model_direction")),
                "cross_disease_cellstate": flag(r.get("gate_breadth_ge3_diseases")),
                "cross_disease_count": num(r.get("positive_disease_count")),
                "ms_anchor": flag(r.get("gate_ms_positive_anchor")),
                "genetic_or_target_resolution": flag(r.get("gate_cross_disease_genetics")),
                "response_support": flag(r.get("gate_adjusted_ra_ibd_response_specific")),
                "prior_not_blocked": flag(r.get("gate_nonblocked_intervention_route")),
                "safety_direction_clear": int("UNRESOLVED" not in clean_text(r.get("wave78_call"))),
                "primary_blocker": clean_text(r.get("decision_reason")),
                "source_call": clean_text(r.get("wave78_call")),
                "source_value": f"ra_p={r.get('ra_response_p')}; ibd_p={r.get('ibd_response_p')}",
            }
        )
        rows.append(row)

    df = read_tsv(W79)
    for _, r in df.iterrows() if not df.empty else []:
        gene = clean_text(r.get("gene"))
        if gene not in {"CD58", "P4HB", "SPNS1", "SEL1L3", "IFI30"}:
            continue
        row = row_template(
            candidate=f"{gene}_TARGETABILITY",
            intervention_class="Targetability shortlist node",
            source_wave="wave79_targetability_shortlist_audit",
            mechanism=f"{gene} targetability shortlist route",
            modality=clean_text(r.get("modality_strength")),
            direction="target-specific modulation unresolved",
        )
        row.update(
            {
                "reachable_modality": flag(r.get("gate_modality")),
                "direct_perturbation": flag(r.get("gate_model_or_perturbation")),
                "cross_disease_cellstate": flag(r.get("gate_breadth_ge3")),
                "cross_disease_count": num(r.get("positive_disease_count")),
                "ms_anchor": flag(r.get("gate_ms_anchor")),
                "genetic_or_target_resolution": flag(r.get("gate_genetics_or_target_resolution")),
                "response_support": flag(r.get("gate_adjusted_ra_ibd_response_specific")),
                "prior_not_blocked": flag(r.get("gate_prior_not_blocked")),
                "safety_direction_clear": flag(r.get("gate_ms_nonnegative_guardrail")),
                "primary_blocker": clean_text(r.get("decision_reason")),
                "source_call": clean_text(r.get("wave79_call")),
                "source_value": f"gate_count={num(r.get('gate_count'))}; ra_p={r.get('ra_response_p')}; ibd_p={r.get('ibd_response_p')}",
            }
        )
        rows.append(row)

    df = read_tsv(W80)
    if not df.empty:
        r = df.iloc[0]
        row = row_template(
            candidate="CD58_CD2_AXIS",
            intervention_class="T-cell/APC adhesion and costimulation axis",
            source_wave="wave80_cd58_cd2_axis_deepening",
            mechanism="CD58-CD2 interaction/state marker",
            modality="biologic or fusion protein precedent",
            direction="conflicted: blockade/depletion versus restored CD58 protective biology",
        )
        row.update(
            {
                "reachable_modality": 1,
                "cross_disease_cellstate": 1,
                "cross_disease_count": 3.0,
                "ms_anchor": flag(r.get("ms_anchor")),
                "genetic_or_target_resolution": 1,
                "response_support": int(num(r.get("ra_full_tcell_adjusted_p"), 1.0) <= 0.01),
                "prior_not_blocked": int(not flag(r.get("generic_autoimmune_prior_art"))),
                "safety_direction_clear": int(not flag(r.get("direction_conflict"))),
                "primary_blocker": clean_text(r.get("decision_reason")),
                "source_call": clean_text(r.get("wave80_call")),
                "source_value": f"ra_p={r.get('ra_full_tcell_adjusted_p')}; ibd_p={r.get('wave79_ibd_response_p')}",
            }
        )
        rows.append(row)

    # Residual Wave82 target routes, retained as negative controls.
    df = read_tsv(W82)
    for _, r in df.iterrows() if not df.empty else []:
        if clean_text(r.get("analysis_role")) != "residual_candidate":
            continue
        gene = clean_text(r.get("gene"))
        row = row_template(
            candidate=f"{gene}_RESIDUAL_ROUTE",
            intervention_class="Residual perturbation/model candidate",
            source_wave="wave82_parked_intervention_route_audit",
            mechanism=clean_text(r.get("route_blocker")),
            modality=clean_text(r.get("plausible_modality")),
            direction=clean_text(r.get("desired_direction")),
        )
        row.update(
            {
                "reachable_modality": int(num(r.get("accessible_surface_secreted")) > 0 or num(r.get("chembl_activity_count")) > 0 or num(r.get("modality_channel")) > 0),
                "direct_perturbation": int(num(r.get("direct_perturbation")) > 0),
                "foundation_model": int(num(r.get("foundation_model_support")) > 0),
                "cross_disease_cellstate": int(num(r.get("broad_positive_disease_count")) >= 3),
                "cross_disease_count": num(r.get("broad_positive_disease_count")),
                "ms_anchor": int(num(r.get("ms_anchor")) > 0),
                "genetic_or_target_resolution": int(num(r.get("genetics_or_target_resolution")) > 0 or num(r.get("target_resolved_local")) > 0),
                "response_support": int(num(r.get("ibd_response_fdr10")) > 0),
                "prior_not_blocked": int("NO_GO" not in clean_text(r.get("wave82_call"))),
                "safety_direction_clear": 0,
                "primary_blocker": clean_text(r.get("hard_failures")),
                "source_call": clean_text(r.get("wave82_call")),
                "source_value": f"route_score={num(r.get('route_score'))}",
            }
        )
        rows.append(row)


def add_targeted_no_go_rows(rows: list[dict[str, Any]]) -> None:
    df = read_tsv(W58)
    for _, r in df.iterrows() if not df.empty else []:
        gene = clean_text(r.get("gene"))
        row = row_template(
            candidate=f"{gene}_TARGETED_ROUTE",
            intervention_class="Canonical immune receptor/chemokine route",
            source_wave="wave58_cxcr2_il7r_targeted_audit",
            mechanism=f"{gene} targeted autoimmune route",
            modality="small molecule or biologic depending on target",
            direction="inhibit/rebalance immune signaling",
        )
        failed = clean_text(r.get("failed_gates"))
        row.update(
            {
                "reachable_modality": 1,
                "foundation_model": 1,
                "cross_disease_cellstate": 1,
                "genetic_or_target_resolution": int(gene == "IL7R"),
                "ms_anchor": int("strict_ms_white_matter_anchor" not in failed and gene == "IL7R"),
                "prior_not_blocked": int("prior_art_not_blocking" not in failed),
                "safety_direction_clear": int("module_specific_not_generic_immunology" not in failed),
                "primary_blocker": failed,
                "source_call": clean_text(r.get("call")),
                "source_value": f"gate_pass={r.get('gate_pass_count')}/{r.get('gate_total')}",
            }
        )
        rows.append(row)

    df = read_tsv(W59)
    for _, r in df.iterrows() if not df.empty else []:
        gene = clean_text(r.get("gene"))
        row = row_template(
            candidate=f"{gene}_LYSOSOMAL_SPHINGOLIPID",
            intervention_class="Lysosomal/sphingolipid enzyme route",
            source_wave="wave59_lysosomal_sphingolipid_model_reopener_audit",
            mechanism=f"{gene} lysosomal or sphingolipid modulation",
            modality="enzyme, small molecule, or gene therapy depending on target",
            direction="restore lysosomal lipid handling without host-defense or storage-disease risk",
        )
        failed = clean_text(r.get("failed_gates"))
        row.update(
            {
                "reachable_modality": 1,
                "foundation_model": int("foundation_model_support" not in failed),
                "cross_disease_cellstate": int("local_recurrence" not in failed),
                "ms_anchor": int("strict_ms_white_matter" not in failed),
                "genetic_or_target_resolution": int("ms_genetic_anchor" not in failed),
                "direct_perturbation": int("real_perturbation_or_efferocytosis" not in failed),
                "prior_not_blocked": int("prior_art_not_blocking" not in failed),
                "safety_direction_clear": int("directionality_safe_and_selective" not in failed),
                "primary_blocker": failed,
                "source_call": clean_text(r.get("call")),
                "source_value": f"gate_pass={r.get('gate_pass_count')}/{r.get('gate_total')}",
            }
        )
        rows.append(row)


def score_rows(rows: list[dict[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["breadth_capped"] = df["cross_disease_count"].astype(float).clip(upper=5.0)
    df["interestingness_score"] = (
        2.0 * df["reachable_modality"].astype(float)
        + 2.0 * df["direct_perturbation"].astype(float)
        + 1.5 * df["foundation_model"].astype(float)
        + 1.5 * df["cross_disease_cellstate"].astype(float)
        + 0.4 * df["breadth_capped"]
        + 2.0 * df["ms_anchor"].astype(float)
        + 2.0 * df["genetic_or_target_resolution"].astype(float)
        + 1.5 * df["response_support"].astype(float)
        + 1.0 * df["biochemical_support"].astype(float)
        + 1.0 * df["specificity_support"].astype(float)
        + 1.0 * df["prior_not_blocked"].astype(float)
        + 1.0 * df["safety_direction_clear"].astype(float)
    )
    critical = [
        "reachable_modality",
        "cross_disease_cellstate",
        "ms_anchor",
        "genetic_or_target_resolution",
        "prior_not_blocked",
        "safety_direction_clear",
    ]
    df["critical_gate_count"] = df[critical].sum(axis=1)
    df["support_gate_count"] = df[["direct_perturbation", "foundation_model", "response_support", "biochemical_support", "specificity_support"]].sum(axis=1)
    blockers = []
    calls = []
    for _, row in df.iterrows():
        missing = [gate for gate in critical if int(row[gate]) == 0]
        source_call = clean_text(row.get("source_call")).upper()
        if source_call.startswith("PARK") or source_call.startswith("NO_GO") or "NO_GO" in source_call:
            missing.append("source_audit_not_promotional")
        if int(row["direct_perturbation"] or row["foundation_model"] or row["response_support"] or row["biochemical_support"]) == 0:
            missing.append("no_perturbation_model_response_or_biochemistry")
        if int(row["support_gate_count"]) < 2:
            missing.append("fewer_than_two_support_channels")
        if not missing:
            calls.append("REOPEN_INTERVENTION_CLASS")
            blockers.append("")
        elif row["critical_gate_count"] >= 4 and row["support_gate_count"] >= 2:
            calls.append("PARK_INTERVENTION_CLASS_NEEDS_FORCING_TEST")
            blockers.append(";".join(missing))
        else:
            calls.append("NO_GO_INTERVENTION_CLASS_META_RANK")
            blockers.append(";".join(missing))
    df["wave83_call"] = calls
    df["wave83_missing_gates"] = blockers
    priority = {
        "REOPEN_INTERVENTION_CLASS": 0,
        "PARK_INTERVENTION_CLASS_NEEDS_FORCING_TEST": 1,
        "NO_GO_INTERVENTION_CLASS_META_RANK": 2,
    }
    df["priority"] = df["wave83_call"].map(priority).fillna(9).astype(int)
    return df.sort_values(["priority", "interestingness_score"], ascending=[True, False]).drop(columns=["priority"])


def write_report(rank: pd.DataFrame) -> None:
    top = rank.head(25).copy() if not rank.empty else rank
    cols = [
        "candidate",
        "wave83_call",
        "interestingness_score",
        "critical_gate_count",
        "support_gate_count",
        "wave83_missing_gates",
        "source_call",
        "primary_blocker",
    ]
    lines = [
        "# Wave83 Intervention-Class-First Meta-Rank",
        "",
        "## Question",
        "",
        "If we start from reachable intervention classes rather than residual genes,",
        "does any class satisfy the V3 therapeutic gate stack?",
        "",
        "## Verdict",
        "",
        clean_text(rank.iloc[0]["wave83_call"]) if not rank.empty else "NO_GO_NO_ROWS",
        "",
        "## Top Rows",
        "",
        markdown_table(top[cols], max_rows=25) if not top.empty else "_No rows._",
        "",
        "## Interpretation",
        "",
        "The intervention-class-first inversion does not produce a finding. It does",
        "identify the least-bad forcing routes: pro-resolution FPR2/ANXA1,",
        "GPR183 oxysterol niche modulation, CD58/CD2 as a blocked genetics/response",
        "comparator, P2RX7 purinergic stratification, and MFGE8 debris-opsonin",
        "biology. Each fails at least one hard gate, usually MS anchoring,",
        "target-resolution genetics, direction/safety, or prior art.",
        "",
        "## Full Rank",
        "",
        markdown_table(rank, max_rows=80),
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    add_wave23(rows)
    add_wave48(rows)
    add_wave54(rows)
    add_simple_decision_rows(rows)
    add_lipid_and_receptor_rows(rows)
    add_surface_and_residual_rows(rows)
    add_targeted_no_go_rows(rows)
    raw = pd.DataFrame(rows)
    rank = score_rows(rows)
    raw.to_csv(OUT / "intervention_class_candidate_universe.tsv", sep="\t", index=False)
    rank.to_csv(OUT / "intervention_class_meta_rank.tsv", sep="\t", index=False)
    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "inputs": {
                "wave23": rel(W23),
                "wave44_cfb": rel(W44_CFB),
                "wave48_route": rel(W48_ROUTE),
                "wave48_matrix": rel(W48_MATRIX),
                "wave50_gpr65": rel(W50_GPR65),
                "wave53": rel(W53),
                "wave54": rel(W54),
                "wave58": rel(W58),
                "wave59": rel(W59),
                "wave64": rel(W64),
                "wave72": rel(W72),
                "wave73": rel(W73),
                "wave74_gpr183": rel(W74_GPR183),
                "wave74_ephx2": rel(W74_EPHX2),
                "wave78": rel(W78),
                "wave79": rel(W79),
                "wave80": rel(W80),
                "wave82": rel(W82),
            },
            "n_candidates": int(len(rank)),
            "call_counts": rank["wave83_call"].value_counts().to_dict() if not rank.empty else {},
            "top_rows": rank.head(10).replace({np.nan: None}).to_dict(orient="records") if not rank.empty else [],
        },
    )
    write_report(rank)


if __name__ == "__main__":
    main()
