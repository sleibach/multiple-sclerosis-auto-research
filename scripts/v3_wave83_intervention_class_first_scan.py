#!/usr/bin/env python3
"""Wave83 intervention-class-first scan.

Previous branches started from recurrent expression or residual perturbation
markers and then asked whether a route existed. This wave reverses the order:
start with locally reachable intervention classes, then require evidence that
the target controls the MS/cross-autoimmune lipid-lysosomal/myeloid module.

This is a triage scan, not a novelty or therapeutic claim.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_direct_h5ad_cell_states import ROOT


SEED = 20260527
OUT = ROOT / "results_v3" / "wave83_intervention_class_first_scan"

W39 = ROOT / "results_v3" / "wave39_surfaceome_rescue_after_resolution_pivot" / "surfaceome_rescue_rank_full.tsv"
W62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W55 = ROOT / "results_v3" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W34A = ROOT / "results_v3" / "wave34a_genetics_first_target_rescue" / "genetics_first_candidate_rank.tsv"
W57 = ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_geneformer_gene_summary.tsv"
W68 = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
W15 = ROOT / "results_v3" / "wave15_perturbation_drug_response" / "candidate_level_synthesis.tsv"
W37 = ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W24 = ROOT / "results_v3" / "wave24_l1000_recurrent_reversal" / "recurrent_l1000_mechanism_summary.tsv"
W61 = ROOT / "results_v3" / "wave61_perturbation_first_guardrail" / "intervention_evidence_tiers.tsv"
W71 = ROOT / "results_v3" / "wave71_global_survivor_meta_rank" / "global_survivor_meta_rank.tsv"


MANUAL_BRANCH_CLOSURES: dict[str, tuple[str, str]] = {
    # Prior V3 branches that already had dedicated audits. These are not
    # permanent biological rejections; they prevent Wave83 from rediscovering a
    # previously closed therapeutic claim without new evidence.
    "ANKRD55": ("nonselective_regulatory_locus_no_modality", "wave62/wave34a target-resolution closure"),
    "BACH2": ("broad_transcriptional_regulator_prior_art_direction_unclear", "wave55 external genetics sweep"),
    "CD5": ("broad_t_cell_surface_axis_prior_art_and_direction_unclear", "wave71 global survivor rank"),
    "CD40": ("costimulation_axis_prior_art_and_systemic_safety", "wave55 external genetics sweep"),
    "CD58": ("genetic_anchor_without_state_response_and_prior_art_cd2_axis", "wave80/wave82 closure"),
    "CD80": ("costimulation_axis_prior_art_and_systemic_safety", "wave33/wave55 closure"),
    "CD86": ("costimulation_axis_prior_art_and_systemic_safety", "wave33/wave55 closure"),
    "CTLA4": ("checkpoint_axis_prior_art_systemic_immunosuppression", "wave33 closure"),
    "CXCR2": ("neutrophil_chemokine_axis_prior_art_and_safety", "wave58 closure"),
    "FADS1": ("lipid_desaturation_axis_not_cell_state_specific", "wave42 closure"),
    "FADS2": ("lipid_desaturation_axis_not_cell_state_specific", "wave42 closure"),
    "FPR2": ("resolution_axis_prior_art_and_uncertain_direction", "wave34b/wave48 closure"),
    "GALC": ("lysosomal_enzyme_delivery_direction_blocker", "wave59 closure"),
    "GPR65": ("acid_sensing_gpcr_prior_art_local_mismatch", "wave50 closure"),
    "IL2RA": ("cd25_axis_prior_art_and_treg_effector_direction_conflict", "wave62/wave71 closure"),
    "IL7R": ("cd127_axis_prior_art_and_cell_type_direction_conflict", "wave58/wave62 closure"),
    "INAVA": ("innate_regulatory_locus_no_druggable_route", "wave62 closure"),
    "IRF5": ("lupus_irf5_prior_art_and_tf_druggability", "wave34a closure"),
    "LILRB1": ("inhibitory_receptor_family_direction_prior_art_unclear", "wave78 closure"),
    "LILRB2": ("inhibitory_receptor_family_direction_prior_art_unclear", "wave78 closure"),
    "LYN": ("src_family_kinase_safety_direction_conflict", "wave82 closure"),
    "MAPK3": ("broad_mapk_kinase_nonselective_safety", "wave62/wave71 closure"),
    "MMEL1": ("locus_resolved_without_module_or_modality_support", "wave62 closure"),
    "NAMPT": ("prior_art_blocked_metabolic_inflammation_target", "V2 EXHAUSTION"),
    "PTGER4": ("ep4_directionality_prior_art_conflicted", "wave62 manual blocker"),
    "PTPN2": ("restoration_needed_no_selective_intervention_route", "wave29/wave34a closure"),
    "PTPN22": ("restoration_direction_and_pleiotropy_blocker", "wave49 closure"),
    "RGS1": ("g_protein_regulator_locus_no_druggable_route", "wave62 closure"),
    "RGS14": ("genetics_without_state_breadth_or_modality", "wave82 closure"),
    "SH2B3": ("lnk_restoration_needed_no_modality_and_pleiotropy", "wave34a closure"),
    "SP140": ("bromodomain_prior_art_weak_perturbation_selectivity", "wave56/wave82 closure"),
    "STAT4": ("broad_tf_jak_stat_axis_prior_art_no_selective_target", "wave82 closure"),
    "TNFRSF1A": ("tnf_axis_ms_paradox_and_safety_blocker", "wave62/wave71 closure"),
    "TYK2": ("jak_tyk_prior_art_direction_and_selectivity_blocker", "wave34a/wave55 closure"),
    "ZC2HC1A": ("locus_marker_without_druggable_route", "wave62 closure"),
}

CALL_PRIORITY = {
    "REOPEN_REACHABLE_INTERVENTION_CANDIDATE": 0,
    "PARK_REACHABLE_BUT_EVIDENCE_INCOMPLETE": 1,
    "PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED": 2,
    "NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED": 3,
    "NO_GO_NOT_REACHABLE_FIRST_CLASS": 4,
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
    if df.empty:
        return "_No rows._"
    view = df.head(max_rows).copy()
    cols = list(view.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in view.iterrows():
        vals: list[str] = []
        for col in cols:
            value = row[col]
            if isinstance(value, float):
                vals.append("" if math.isnan(value) else f"{value:.4g}")
            else:
                vals.append(str(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def norm_gene(value: Any) -> str:
    text = str(value).strip()
    if text == "" or text.lower() in {"nan", "none"}:
        return ""
    text = re.sub(r"_(KO|KD|CRISPRI|CRISPRIA|OE)$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"[- ](KO|KD)$", "", text, flags=re.IGNORECASE)
    return text.upper()


def truthy(value: Any) -> bool:
    text = str(value).strip().lower()
    return text in {"true", "1", "yes", "y"}


def f(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    return str(value)


def first_by_gene(df: pd.DataFrame, gene_col: str = "gene") -> dict[str, dict[str, Any]]:
    if df.empty or gene_col not in df.columns:
        return {}
    tmp = df.copy()
    tmp["gene_norm"] = tmp[gene_col].map(norm_gene)
    tmp = tmp[tmp["gene_norm"] != ""]
    return tmp.drop_duplicates("gene_norm", keep="first").set_index("gene_norm").to_dict(orient="index")


def best_w68(df: pd.DataFrame) -> dict[str, dict[str, Any]]:
    if df.empty or "gene" not in df.columns:
        return {}
    tmp = df.copy()
    tmp["gene_norm"] = tmp["gene"].map(norm_gene)
    tmp = tmp[tmp["gene_norm"] != ""]
    if "wave68_call_priority" in tmp.columns:
        tmp = tmp.sort_values(["gene_norm", "wave68_call_priority", "remission_adjusted_p"], ascending=[True, True, True])
    elif "remission_adjusted_p" in tmp.columns:
        tmp = tmp.sort_values(["gene_norm", "remission_adjusted_p"], ascending=[True, True])
    return tmp.drop_duplicates("gene_norm", keep="first").set_index("gene_norm").to_dict(orient="index")


def best_w15(df: pd.DataFrame) -> dict[str, dict[str, Any]]:
    if df.empty or "candidate" not in df.columns:
        return {}
    tmp = df.copy()
    tmp["gene_norm"] = tmp["candidate"].map(norm_gene)
    tmp = tmp[tmp["gene_norm"] != ""]
    tmp = tmp.sort_values(["gene_norm", "best_direct_selectivity_score"], ascending=[True, False])
    return tmp.drop_duplicates("gene_norm", keep="first").set_index("gene_norm").to_dict(orient="index")


def best_w37(df: pd.DataFrame) -> dict[str, dict[str, Any]]:
    if df.empty or "gene_symbol" not in df.columns:
        return {}
    tmp = df.copy()
    tmp["gene_norm"] = tmp["gene_symbol"].map(norm_gene)
    tmp = tmp[tmp["gene_norm"] != ""]
    tmp["abs_effect"] = tmp.get("median_efficient_minus_noneater_lfc", pd.Series(dtype=float)).map(abs)
    tmp = tmp.sort_values(["gene_norm", "abs_effect"], ascending=[True, False])
    return tmp.drop_duplicates("gene_norm", keep="first").set_index("gene_norm").to_dict(orient="index")


def l1000_by_gene(df: pd.DataFrame) -> dict[str, dict[str, Any]]:
    if df.empty or "target" not in df.columns:
        return {}
    tmp = df.copy()
    tmp["gene_norm"] = tmp["target"].map(norm_gene)
    tmp = tmp[tmp["gene_norm"] != ""]
    tmp = tmp.sort_values(["gene_norm", "min_qval"], ascending=[True, True])
    return tmp.drop_duplicates("gene_norm", keep="first").set_index("gene_norm").to_dict(orient="index")


def infer_class(row: dict[str, Any]) -> str:
    blob = " ".join(
        [
            text(row.get("target_class")),
            text(row.get("modality")),
            text(row.get("protein_name")),
            text(row.get("uniprot_keywords")),
            text(row.get("uniprot_locations")),
            text(row.get("chembl_target_pref_name")),
            text(row.get("chembl_target_type")),
            text(row.get("function_excerpt")),
        ]
    ).lower()
    if "kinase" in blob:
        return "kinase_or_phosphosignaling"
    if "phosphatase" in blob:
        return "phosphatase_or_signaling_adaptor"
    if "receptor" in blob or "cytokine" in blob or "chemokine" in blob:
        return "receptor_or_ligand_axis"
    if "transporter" in blob or "transport" in blob or "solute" in blob:
        return "transporter_or_trafficking"
    if "lysosome" in blob or "lysosomal" in blob:
        return "lysosomal_enzyme_or_trafficking"
    if "enzyme" in blob or "isomerase" in blob or "catalytic" in blob or "active site" in blob:
        return "enzyme"
    if "cell membrane" in blob or "secreted" in blob or "extracellular" in blob:
        return "surface_secreted_other"
    if "dna-binding" in blob or "transcription" in blob or "chromatin" in blob:
        return "nuclear_regulatory"
    return "intracellular_other"


def has_prior_blocker(*values: Any) -> bool:
    blob = " | ".join(text(v).lower() for v in values)
    blocker_terms = [
        "prior_art",
        "prior art",
        "blocked",
        "host_defense",
        "host-defense",
        "toxicity",
        "paradox",
        "generic",
        "not_selectively_druggable",
        "no_go",
        "do_not_promote",
    ]
    return any(term in blob for term in blocker_terms)


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    w39 = read_tsv(W39)
    w62 = read_tsv(W62)
    w55 = read_tsv(W55)
    w34a = read_tsv(W34A)
    w57 = read_tsv(W57)
    w68 = read_tsv(W68)
    w15 = read_tsv(W15)
    w37 = read_tsv(W37)
    w24 = read_tsv(W24)
    w61 = read_tsv(W61)
    w71 = read_tsv(W71)

    l39 = first_by_gene(w39)
    l62 = first_by_gene(w62)
    l55 = first_by_gene(w55)
    l34a = first_by_gene(w34a)
    l57 = first_by_gene(w57)
    l68 = best_w68(w68)
    l15 = best_w15(w15)
    l37 = best_w37(w37)
    l24 = l1000_by_gene(w24)
    l61 = first_by_gene(w61)
    l71 = first_by_gene(w71)

    candidate_genes: set[str] = set()
    for gene, row in l62.items():
        if (
            f(row.get("strong_l2g_disease_count")) >= 2
            or f(row.get("supporting_l2g_disease_count")) >= 3
            or f(row.get("ms_max_l2g_score")) >= 0.5
            or f(row.get("relevant_qtl_coloc_disease_count")) >= 2
            or text(row.get("chembl_target_id"))
            or f(row.get("druggable_activity_count")) > 0
        ):
            candidate_genes.add(gene)
    for gene, row in l55.items():
        if (
            f(row.get("n_diseases_genetic_ge_0_25")) >= 4
            or f(row.get("n_diseases_genetic_ge_0_5")) >= 3
            or f(row.get("ms_genetic_association")) >= 0.5
            or f(row.get("local_positive_disease_count")) >= 3
        ):
            candidate_genes.add(gene)
    for gene, row in l34a.items():
        if (
            f(row.get("ot_n_diseases_score_ge_0_5")) >= 4
            or f(row.get("manual_druggability")) >= 1
            or text(row.get("chembl_target_id"))
            or f(row.get("chembl_activity_count_nM")) > 0
        ):
            candidate_genes.add(gene)
    for gene, row in l71.items():
        if f(row.get("evidence_channel_count")) >= 3 or f(row.get("genetics_channel_count")) >= 2:
            candidate_genes.add(gene)
    for gene, row in l39.items():
        if truthy(row.get("uniprot_accessible")) or f(row.get("chembl_activity_count")) > 0:
            candidate_genes.add(gene)
    for gene, row in l68.items():
        if truthy(row.get("has_any_druggability_flag")):
            candidate_genes.add(gene)
    for gene, row in l24.items():
        if text(row.get("target")):
            candidate_genes.add(gene)
    for gene, row in l61.items():
        if text(row.get("chembl_target_id")) or f(row.get("druggable_activity_count")) > 0:
            candidate_genes.add(gene)

    rows: list[dict[str, Any]] = []
    for gene in sorted(candidate_genes):
        r39 = l39.get(gene, {})
        r62 = l62.get(gene, {})
        r55 = l55.get(gene, {})
        r34a = l34a.get(gene, {})
        r57 = l57.get(gene, {})
        r68 = l68.get(gene, {})
        r15 = l15.get(gene, {})
        r37 = l37.get(gene, {})
        r24 = l24.get(gene, {})
        r61 = l61.get(gene, {})
        r71 = l71.get(gene, {})

        chembl_activity = max(
            f(r39.get("chembl_activity_count")),
            f(r62.get("druggable_activity_count")),
            f(r34a.get("chembl_activity_count_nM")),
            f(r61.get("druggable_activity_count")),
        )
        target_class_blob = " ".join(
            [
                text(r34a.get("target_class")),
                text(r39.get("uniprot_locations")),
                text(r39.get("uniprot_keywords")),
                text(r62.get("approved_name")),
                text(r34a.get("chembl_target_type")),
            ]
        ).lower()
        accessible = truthy(r39.get("uniprot_accessible")) or any(
            token in target_class_blob
            for token in ["surface", "secret", "receptor", "cytokine", "chemokine", "extracellular", "membrane"]
        )
        known_or_clinical = max(
            f(r39.get("opentargets_max_known_drug_or_clinical")),
            f(r55.get("max_clinical_score")),
            f(r39.get("clinicaltrials_hit_count")),
            f(r39.get("clinicaltrials_autoimmune_count")),
            f(r34a.get("clinicaltrials_count")),
        )
        modality_flag = (
            accessible
            or chembl_activity > 0
            or text(r62.get("chembl_target_id")) != ""
            or text(r34a.get("chembl_target_id")) != ""
            or f(r34a.get("manual_druggability")) >= 1
            or truthy(r68.get("has_any_druggability_flag"))
            or text(r24.get("target")) != ""
        )

        reachability_score = 0.0
        reachability_score += 2.0 if accessible else 0.0
        reachability_score += 2.0 if chembl_activity > 0 else 0.0
        reachability_score += 1.0 if text(r62.get("chembl_target_id")) else 0.0
        reachability_score += 1.0 if text(r34a.get("chembl_target_id")) else 0.0
        reachability_score += min(f(r34a.get("manual_druggability")), 2.0) * 0.75
        reachability_score += 1.0 if known_or_clinical > 0 else 0.0
        reachability_score += 1.0 if truthy(r68.get("has_any_druggability_flag")) else 0.0
        reachability_score += 0.5 if text(r24.get("target")) else 0.0

        positive_disease_count = max(
            f(r39.get("positive_disease_count")),
            f(r55.get("local_positive_disease_count")),
            f(r62.get("local_positive_disease_count")),
            f(r68.get("local_positive_disease_count")),
            f(r34a.get("broad_positive_disease_count")),
        )
        positive_fdr10 = f(r39.get("positive_fdr10_compartment_count"))
        genetic_breadth = max(
            f(r62.get("strong_l2g_disease_count")),
            f(r62.get("supporting_l2g_disease_count")),
            f(r55.get("n_diseases_genetic_ge_0_25")),
            f(r34a.get("ot_n_diseases_score_ge_0_5")),
        )
        qtl_breadth = f(r62.get("relevant_qtl_coloc_disease_count"))
        cross_score = min(positive_disease_count, 5.0)
        cross_score += min(genetic_breadth, 5.0) * 0.7
        cross_score += min(qtl_breadth, 5.0) * 0.5
        cross_score += min(positive_fdr10, 3.0)

        ms_genetic = max(
            f(r62.get("ms_max_l2g_score")),
            f(r55.get("ms_genetic_association")),
            f(r68.get("ms_max_l2g_score")),
            1.0 if "MS" in text(r34a.get("ot_diseases_score_ge_0_5")).split(";") else 0.0,
        )
        ms_expr_p = min(
            [
                p
                for p in [
                    f(r39.get("ms_wm_p"), 1.0),
                    f(r55.get("ms_wm_p"), 1.0),
                    f(r62.get("ms_wm_p"), 1.0),
                    f(r34a.get("ms_wm_p"), 1.0),
                ]
                if p > 0
            ]
            or [1.0]
        )
        ms_expr_delta = max(
            f(r39.get("ms_wm_delta_log2")),
            f(r55.get("ms_wm_delta_log2")),
            f(r62.get("ms_wm_delta_log2")),
            f(r34a.get("ms_wm_delta_log2")),
        )
        ms_score = 0.0
        ms_score += 2.0 if ms_genetic >= 0.5 else 0.0
        ms_score += 1.0 if 0.25 <= ms_genetic < 0.5 else 0.0
        ms_score += 1.0 if ms_expr_p < 0.05 and ms_expr_delta > 0 else 0.0
        ms_score += 1.0 if truthy(r39.get("has_ms_anchor")) else 0.0

        model_support = f(r57.get("support_contexts")) > 0
        strong_model = f(r57.get("strong_support_contexts")) > 0
        direct_selective = f(r15.get("best_direct_selectivity_score")) >= 0.5 and "selective" in text(r15.get("direct_evidence_calls")).lower()
        efferocytosis_direct = "KO_ENHANCES_EFFEROCYTOSIS" in text(r37.get("screen_call"))
        response_fdr = f(r68.get("remission_adjusted_fdr"), 1.0) <= 0.1 or f(r68.get("raw_fdr"), 1.0) <= 0.1
        l1000_reversal = text(r24.get("wave24_call")).startswith("PARK") or text(r24.get("wave24_call")).startswith("REOPEN")

        perturbation_score = 0.0
        perturbation_score += 1.5 if model_support else 0.0
        perturbation_score += 1.0 if strong_model else 0.0
        perturbation_score += 2.0 if direct_selective else 0.0
        perturbation_score += 1.0 if efferocytosis_direct else 0.0
        perturbation_score += 2.0 if response_fdr else 0.0
        perturbation_score += 0.5 if l1000_reversal else 0.0

        prior_blocked = has_prior_blocker(
            r62.get("manual_blocker"),
            r62.get("prior_context_blocker"),
            r34a.get("prior_risk"),
            r34a.get("manual_note"),
            r34a.get("route_reason"),
            r34a.get("wave34a_call"),
            r39.get("prior_flags"),
            r39.get("wave39_reason"),
            r55.get("foundation_recommendation"),
            r61.get("manual_blocker"),
            r68.get("manual_blocker"),
            r68.get("wave68_posthoc_blocker"),
            r68.get("wave68_call"),
            r71.get("hard_block_reason"),
            r71.get("soft_penalty_reason"),
            r71.get("blockers"),
        )
        manual_closure = MANUAL_BRANCH_CLOSURES.get(gene)
        if manual_closure is not None:
            prior_blocked = True
        generic_penalty = 1.0 if has_prior_blocker(r39.get("wave39_call"), r62.get("wave62_call")) else 0.0
        safety_penalty = 3.0 if manual_closure is not None else (2.0 if prior_blocked else generic_penalty)

        global_meta_score = f(r71.get("meta_score"))
        genetics_first_score = f(r34a.get("genetics_first_score"))
        target_resolution_score = f(r62.get("wave62_score"))
        total_score = (
            reachability_score
            + cross_score
            + ms_score
            + perturbation_score
            + min(global_meta_score, 6.0) * 0.25
            + min(genetics_first_score, 25.0) * 0.05
            + min(target_resolution_score, 8.0) * 0.15
            - safety_penalty
        )

        hard_failures: list[str] = []
        if reachability_score < 3:
            hard_failures.append("weak_reachability")
        if positive_disease_count < 3 and genetic_breadth < 3:
            hard_failures.append("insufficient_cross_disease_breadth")
        if ms_score < 2:
            hard_failures.append("no_strong_ms_anchor")
        if perturbation_score < 2:
            hard_failures.append("no_positive_perturbation_or_response_direction")
        if prior_blocked:
            hard_failures.append("manual_or_prior_blocker")
        if manual_closure is not None:
            hard_failures.append(f"prior_branch_closed:{manual_closure[0]}")
        if response_fdr is False and direct_selective is False and strong_model is False:
            hard_failures.append("no_high_confidence_directional_support")

        if not hard_failures and total_score >= 14:
            call = "REOPEN_REACHABLE_INTERVENTION_CANDIDATE"
        elif manual_closure is not None and reachability_score >= 3 and (genetic_breadth >= 3 or positive_disease_count >= 3):
            call = "PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED"
        elif (
            reachability_score >= 3
            and total_score >= 9
            and len(hard_failures) <= 2
            and not prior_blocked
            and "no_strong_ms_anchor" not in hard_failures
        ):
            call = "PARK_REACHABLE_BUT_EVIDENCE_INCOMPLETE"
        elif reachability_score >= 3:
            call = "NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED"
        else:
            call = "NO_GO_NOT_REACHABLE_FIRST_CLASS"

        merged_for_class = {**r39, **r62, **r34a}
        intervention_class = infer_class(merged_for_class)
        rows.append(
            {
                "gene": gene,
                "intervention_class": intervention_class,
                "wave83_call": call,
                "total_score": total_score,
                "reachability_score": reachability_score,
                "cross_autoimmune_score": cross_score,
                "ms_score": ms_score,
                "perturbation_response_score": perturbation_score,
                "safety_prior_penalty": safety_penalty,
                "hard_failures": ";".join(hard_failures),
                "accessible_uniprot": int(accessible),
                "manual_closure_reason": manual_closure[0] if manual_closure else "",
                "manual_closure_source": manual_closure[1] if manual_closure else "",
                "chembl_activity_count": chembl_activity,
                "chembl_target_id": (
                    text(r62.get("chembl_target_id"))
                    or text(r34a.get("chembl_target_id"))
                    or text(r39.get("chembl_target_chembl_id"))
                ),
                "wave34a_target_class": text(r34a.get("target_class")),
                "wave34a_modality": text(r34a.get("modality")),
                "positive_disease_count": positive_disease_count,
                "positive_diseases": (
                    text(r39.get("positive_diseases"))
                    or text(r55.get("local_positive_diseases"))
                    or text(r62.get("local_positive_diseases"))
                    or text(r34a.get("broad_positive_diseases"))
                ),
                "positive_fdr10_compartment_count": positive_fdr10,
                "genetic_breadth_disease_count": genetic_breadth,
                "genetic_breadth_diseases": (
                    text(r62.get("strong_l2g_diseases"))
                    or text(r55.get("diseases_genetic_ge_0_25"))
                    or text(r34a.get("ot_diseases_score_ge_0_5"))
                ),
                "qtl_breadth_disease_count": qtl_breadth,
                "ms_genetic_score": ms_genetic,
                "ms_expr_delta": ms_expr_delta,
                "ms_expr_p": ms_expr_p,
                "target_resolution_score": target_resolution_score,
                "genetics_first_score": genetics_first_score,
                "global_meta_score": global_meta_score,
                "model_support_contexts": f(r57.get("support_contexts")),
                "model_strong_support_contexts": f(r57.get("strong_support_contexts")),
                "direct_selective": int(direct_selective),
                "direct_selectivity_score": f(r15.get("best_direct_selectivity_score")),
                "efferocytosis_screen_call": text(r37.get("screen_call")),
                "ibd_response_fdr10": int(response_fdr),
                "wave68_call": text(r68.get("wave68_call")),
                "l1000_wave24_call": text(r24.get("wave24_call")),
                "wave39_call": text(r39.get("wave39_call")),
                "wave62_call": text(r62.get("wave62_call")),
                "wave34a_call": text(r34a.get("wave34a_call")),
                "wave71_call": text(r71.get("wave71_call")),
                "wave55_score": f(r55.get("wave55_score")),
                "manual_prior_blocked": int(prior_blocked),
                "primary_route_note": (
                    text(r39.get("wave39_reason"))
                    or text(r62.get("wave34a_route_reason"))
                    or text(r34a.get("route_reason"))
                    or text(r68.get("wave68_posthoc_blocker"))
                    or text(r71.get("wave71_reason"))
                ),
            }
        )

    rank = pd.DataFrame(rows)
    if not rank.empty:
        rank["call_priority"] = rank["wave83_call"].map(CALL_PRIORITY).fillna(99).astype(int)
        rank = rank.sort_values(
            [
                "call_priority",
                "total_score",
                "reachability_score",
                "cross_autoimmune_score",
                "ms_score",
                "perturbation_response_score",
            ],
            ascending=[True, False, False, False, False, False],
        )
        rank = rank.drop(columns=["call_priority"])
    rank.to_csv(OUT / "reachable_intervention_rank.tsv", sep="\t", index=False)

    class_summary = (
        rank.groupby("intervention_class", dropna=False)
        .agg(
            n_candidates=("gene", "count"),
            n_parked=("wave83_call", lambda s: int(s.str.startswith("PARK").sum())),
            n_reopened=("wave83_call", lambda s: int(s.str.startswith("REOPEN").sum())),
            max_total_score=("total_score", "max"),
            median_reachability_score=("reachability_score", "median"),
            median_ms_score=("ms_score", "median"),
            median_perturbation_response_score=("perturbation_response_score", "median"),
            top_gene=("gene", "first"),
        )
        .reset_index()
        .sort_values(["n_reopened", "n_parked", "max_total_score"], ascending=[False, False, False])
    )
    class_summary.to_csv(OUT / "reachable_intervention_class_summary.tsv", sep="\t", index=False)

    top = rank.head(25).copy()
    parked = rank[rank["wave83_call"].str.startswith("PARK")].head(25).copy()
    reopened = rank[rank["wave83_call"].str.startswith("REOPEN")].copy()

    summary = {
        "random_seed": SEED,
        "inputs": {
            "wave39": rel(W39),
            "wave62": rel(W62),
            "wave55": rel(W55),
            "wave34a": rel(W34A),
            "wave57": rel(W57),
            "wave68": rel(W68),
            "wave15": rel(W15),
            "wave37": rel(W37),
            "wave24": rel(W24),
            "wave61": rel(W61),
            "wave71": rel(W71),
        },
        "n_reachable_first_candidates": int(len(rank)),
        "call_counts": rank["wave83_call"].value_counts().to_dict(),
        "class_summary_top": class_summary.head(10).to_dict(orient="records"),
        "top_candidate": rank.head(1).to_dict(orient="records")[0] if not rank.empty else {},
    }
    write_json(OUT / "summary.json", summary)

    report = f"""# Wave83 Intervention-Class-First Scan

## Question

If we start from locally reachable intervention classes instead of residual
expression markers, does any target pass MS/cross-autoimmune module evidence and
directional perturbation gates?

## Verdict

`REOPEN_REACHABLE_INTERVENTION_CANDIDATE`: `{len(reopened)}`.

This wave is a triage scan. A park is not a therapeutic claim.

## Call Counts

{markdown_table(rank["wave83_call"].value_counts().rename_axis("call").reset_index(name="n"))}

## Top Reachable-First Candidates

{markdown_table(top[["gene", "intervention_class", "wave83_call", "total_score", "reachability_score", "cross_autoimmune_score", "ms_score", "perturbation_response_score", "hard_failures", "manual_closure_reason", "positive_diseases", "genetic_breadth_diseases", "wave39_call", "wave62_call", "wave34a_call", "wave68_call"]])}

## Parked Candidates

{markdown_table(parked[["gene", "intervention_class", "wave83_call", "total_score", "hard_failures", "manual_closure_reason", "positive_diseases", "ms_genetic_score", "model_support_contexts", "ibd_response_fdr10", "manual_prior_blocked", "primary_route_note"]])}

## Intervention-Class Summary

{markdown_table(class_summary)}

## Interpretation

This scan deliberately penalizes the pattern that failed in Wave82: a reachable
or recurrent marker is not enough without MS anchoring and directional
perturbation/response support. The ranked table should be used to choose the
next branch only if a parked candidate has a specific missing evidence gap that
can be resolved with an independent dataset or model.

## Outputs

- `reachable_intervention_rank.tsv`
- `reachable_intervention_class_summary.tsv`
- `summary.json`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
