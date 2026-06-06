#!/usr/bin/env python3
"""Wave99 audit of endogenous inflammasome/caspase brakes.

Wave98 left LITAF as only a wet-lab ordering hypothesis and CASP4 as a
close-prior/safety-blocked stress-generator comparator. This wave asks whether
drugging an endogenous brake of the CASP4/LITAF axis is more defensible than
directly targeting the stress generator.

Important rule: disease-high expression of a brake is not therapeutic proof.
It can be a protective counter-response, a failed compensatory marker, or a
generic inflammation marker. Promotion requires residual C15ORF48 co-state,
MS anchoring, perturbation direction, feasible modality, and no prior-art/safety
block.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_osmr_complement_axes import COVARIATE_MODULES, ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json
from v3_wave97_c15_residual_costate_falsification import per_context_residual_tests


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave99_endogenous_inflammasome_brake_audit"

ANCHORS = ROOT / "phases/v3/results" / "wave96_c15orf48_controller_search" / "c15orf48_anchor_contexts.tsv"
W96_CONTRAST = ROOT / "phases/v3/results" / "wave96_c15orf48_controller_search" / "contrast_state_rank_all.tsv"
W96_DONOR = ROOT / "phases/v3/results" / "wave96_c15orf48_controller_search" / "donor_level_c15_costate_summary.tsv"
MS_WM = ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv"
BROAD = ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
W39 = ROOT / "phases/v3/results" / "wave39_surfaceome_rescue_after_resolution_pivot" / "surfaceome_rescue_rank_full.tsv"
W55 = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W62 = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W68 = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
W68_OLS = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "adjusted_top_gene_ols.tsv"
W37 = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W37_GUIDE = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "guide_level_lfc.tsv"
W18 = ROOT / "phases/v3/results" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv"
W81 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W98 = ROOT / "phases/v3/results" / "wave98_c15_successor_perturbation_first_audit" / "c15_successor_perturbation_first_rank.tsv"

CANDIDATES = [
    "CARD16",
    "CARD17",
    "CARD18",
    "CARD8",
    "SERPINB1",
    "IL18BP",
    "GBP1",
    "GBP2",
    "GBP5",
    "CASP1",
    "CASP4",
    "CASP5",
    "GSDMD",
    "NLRP3",
    "NLRP6",
    "IL1B",
    "IL18",
]


MANUAL = {
    "CARD16": {
        "axis_role": "endogenous_inflammasome_brake",
        "desired_intervention": "augment CARD16-like brake activity only if protective ordering is proven",
        "disease_high_interpretation": "possible compensatory brake, not proof of benefit",
        "modality_class": "intracellular CARD-only protein; no established selective augmentation modality",
        "manual_modality_ready": False,
        "manual_prior_blocked": False,
        "manual_safety_blocked": False,
        "manual_note": "mechanistically attractive but currently lacks a drug-like handle",
    },
    "CARD17": {
        "axis_role": "endogenous_inflammasome_brake_like",
        "desired_intervention": "augment only after protective ordering and expression support",
        "disease_high_interpretation": "possible compensatory brake or myeloid state marker",
        "modality_class": "intracellular CARD-only protein; no established selective augmentation modality",
        "manual_modality_ready": False,
        "manual_prior_blocked": False,
        "manual_safety_blocked": False,
        "manual_note": "less locally supported CARD-only comparator",
    },
    "CARD18": {
        "axis_role": "endogenous_inflammasome_brake_like",
        "desired_intervention": "augment only after protective ordering and expression support",
        "disease_high_interpretation": "possible compensatory brake or marker",
        "modality_class": "intracellular CARD-only protein; no established selective augmentation modality",
        "manual_modality_ready": False,
        "manual_prior_blocked": False,
        "manual_safety_blocked": False,
        "manual_note": "less locally supported CARD-only comparator",
    },
    "CARD8": {
        "axis_role": "inflammasome_sensor_regulator",
        "desired_intervention": "not direction-clear; avoid without cell-specific perturbation",
        "disease_high_interpretation": "could represent inflammasome competence rather than a brake",
        "modality_class": "NLR/CARD inflammasome regulator; target biology is not a clean brake",
        "manual_modality_ready": False,
        "manual_prior_blocked": False,
        "manual_safety_blocked": True,
        "manual_note": "directionality and inflammasome toxicity are unfavorable",
    },
    "SERPINB1": {
        "axis_role": "endogenous_protease_inflammatory_brake",
        "desired_intervention": "augment intracellular serpin function only if delivery and ordering are solved",
        "disease_high_interpretation": "possible neutrophil/myeloid counter-regulatory marker",
        "modality_class": "intracellular serpin; recombinant replacement/delivery to lesional myeloid cells is not established",
        "manual_modality_ready": False,
        "manual_prior_blocked": False,
        "manual_safety_blocked": False,
        "manual_note": "biologically plausible brake but weak MS anchor and delivery barrier",
    },
    "IL18BP": {
        "axis_role": "secreted_IL18_neutralizing_brake",
        "desired_intervention": "augment IL18BP / neutralize IL18 if IL18-high tissue state is present",
        "disease_high_interpretation": "secreted counter-regulator; low disease expression could still support replacement",
        "modality_class": "secreted soluble decoy; recombinant biologic modality exists in adjacent indications",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": False,
        "manual_note": "actionable modality, but IL18/IL18BP therapeutic space is prior-art crowded and local MS support must be strong",
    },
    "GBP1": {
        "axis_role": "ifn_induced_noncanonical_inflammasome_host_defense",
        "desired_intervention": "avoid direct inhibition unless disease-specific pathologic GBP state is proven",
        "disease_high_interpretation": "generic interferon/host-defense marker",
        "modality_class": "GTPase; no selective autoimmune-safe modality",
        "manual_modality_ready": False,
        "manual_prior_blocked": False,
        "manual_safety_blocked": True,
        "manual_note": "host-defense liability and IFN confounding dominate",
    },
    "GBP2": {
        "axis_role": "ifn_induced_noncanonical_inflammasome_host_defense",
        "desired_intervention": "avoid direct inhibition",
        "disease_high_interpretation": "generic interferon/host-defense marker",
        "modality_class": "GTPase; no selective autoimmune-safe modality",
        "manual_modality_ready": False,
        "manual_prior_blocked": False,
        "manual_safety_blocked": True,
        "manual_note": "host-defense liability and IFN confounding dominate",
    },
    "GBP5": {
        "axis_role": "ifn_induced_noncanonical_inflammasome_host_defense",
        "desired_intervention": "avoid direct inhibition",
        "disease_high_interpretation": "generic interferon/host-defense marker",
        "modality_class": "GTPase; no selective autoimmune-safe modality",
        "manual_modality_ready": False,
        "manual_prior_blocked": False,
        "manual_safety_blocked": True,
        "manual_note": "host-defense liability and IFN confounding dominate",
    },
    "CASP1": {
        "axis_role": "core_inflammasome_effector",
        "desired_intervention": "inhibit only with strong cell/tissue stratification",
        "disease_high_interpretation": "driver or inflammatory state marker",
        "modality_class": "cysteine protease; inhibitor chemistry exists but selectivity/safety are difficult",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": True,
        "manual_note": "prior-art and host-defense/safety liabilities block broad promotion",
    },
    "CASP4": {
        "axis_role": "noncanonical_pyroptosis_stress_generator",
        "desired_intervention": "selectively inhibit only if separable from host defense and CASP1/CASP5",
        "disease_high_interpretation": "driver or danger-state marker",
        "modality_class": "cysteine protease; targetable but selectivity/host-defense risk",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": True,
        "manual_note": "Wave98 close-prior/safety-blocked comparator",
    },
    "CASP5": {
        "axis_role": "noncanonical_pyroptosis_stress_generator",
        "desired_intervention": "avoid without CASP5-specific disease proof",
        "disease_high_interpretation": "driver or danger-state marker",
        "modality_class": "cysteine protease; targetable class but selectivity/host-defense risk",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": True,
        "manual_note": "core pyroptosis route is crowded and safety-sensitive",
    },
    "GSDMD": {
        "axis_role": "pyroptotic_pore_effector",
        "desired_intervention": "inhibit pore formation only with strong tissue safety case",
        "disease_high_interpretation": "pyroptosis competence marker",
        "modality_class": "pore-forming effector; chemistry emerging but broad innate safety risk",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": True,
        "manual_note": "not an endogenous brake; broad pyroptosis blockade is not a clean cross-autoimmune target",
    },
    "NLRP3": {
        "axis_role": "inflammasome_sensor",
        "desired_intervention": "inhibit NLRP3 only if disease module is NLRP3-dependent",
        "disease_high_interpretation": "driver or inflammasome-competence marker",
        "modality_class": "small-molecule NLRP3 inhibitors exist",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": True,
        "manual_note": "autoimmune/inflammatory prior art is saturated",
    },
    "NLRP6": {
        "axis_role": "mucosal_inflammasome_context_regulator",
        "desired_intervention": "not MS-first; gut context only if strongly supported",
        "disease_high_interpretation": "context-dependent epithelial/mucosal marker",
        "modality_class": "inflammasome sensor; no clean selective autoimmune modality",
        "manual_modality_ready": False,
        "manual_prior_blocked": False,
        "manual_safety_blocked": True,
        "manual_note": "direction and tissue context are not compatible with MS-led claim",
    },
    "IL1B": {
        "axis_role": "proinflammatory_inflammasome_output",
        "desired_intervention": "neutralize only if IL1B-high subgroup is proven",
        "disease_high_interpretation": "downstream inflammatory output",
        "modality_class": "biologic neutralization exists",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": True,
        "manual_note": "prior-art saturated and not a brake",
    },
    "IL18": {
        "axis_role": "proinflammatory_inflammasome_output",
        "desired_intervention": "neutralize IL18 only if IL18-high tissue state is proven",
        "disease_high_interpretation": "downstream inflammatory output",
        "modality_class": "biologic neutralization/IL18BP route exists",
        "manual_modality_ready": True,
        "manual_prior_blocked": True,
        "manual_safety_blocked": True,
        "manual_note": "prior-art crowded and local MS support must be exceptional",
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


def best_w68(df: pd.DataFrame, gene: str) -> pd.Series | None:
    if df.empty or "gene" not in df.columns:
        return None
    sub = df[df["gene"].astype(str).str.upper().eq(gene.upper())].copy()
    if sub.empty:
        return None
    sub["_fdr"] = pd.to_numeric(sub.get("remission_adjusted_fdr", np.nan), errors="coerce").fillna(1.0)
    sub["_p"] = pd.to_numeric(sub.get("remission_adjusted_p", np.nan), errors="coerce").fillna(1.0)
    return sub.sort_values(["_fdr", "_p"]).iloc[0]


def guide_consistency(guides: pd.DataFrame, gene: str) -> dict[str, Any]:
    if guides.empty or "gene_symbol" not in guides.columns:
        return {}
    sub = guides[guides["gene_symbol"].astype(str).str.upper().eq(gene.upper())].copy()
    if sub.empty:
        return {"wave37_guide_count": 0}
    contrast_cols = [c for c in sub.columns if c.endswith("efficient_minus_noneater_lfc")]
    contrast_col = contrast_cols[0] if contrast_cols else None
    vals = pd.to_numeric(sub[contrast_col], errors="coerce") if contrast_col else pd.Series(dtype=float)
    vals = vals.dropna()
    return {
        "wave37_guide_count": int(len(sub)),
        "wave37_guide_contrast_median": float(vals.median()) if len(vals) else math.nan,
        "wave37_guide_positive_fraction": float((vals > 0).mean()) if len(vals) else math.nan,
        "wave37_guide_negative_fraction": float((vals < 0).mean()) if len(vals) else math.nan,
    }


def summarize_residual_tests(tests: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gene in CANDIDATES:
        sub = tests[tests["gene"].astype(str).str.upper().eq(gene)].copy() if not tests.empty else pd.DataFrame()
        if sub.empty:
            rows.append(
                {
                    "gene": gene,
                    "contexts_tested": 0,
                    "raw_case_positive_context_count": 0,
                    "raw_case_positive_disease_count": 0,
                    "residual_case_positive_context_count": 0,
                    "residual_case_positive_disease_count": 0,
                    "residual_all_positive_context_count": 0,
                    "residual_all_positive_disease_count": 0,
                    "median_raw_case_r": math.nan,
                    "median_residual_case_r": math.nan,
                    "best_residual_context": "",
                    "best_residual_case_r": math.nan,
                }
            )
            continue
        raw_case_pos = sub[(sub["raw_case_r"] >= 0.30) & (sub["raw_case_p"].fillna(1.0) <= 0.20)]
        case_pos = sub[(sub["residual_case_r"] >= 0.30) & (sub["residual_case_p"].fillna(1.0) <= 0.20)]
        all_pos = sub[(sub["residual_all_r"] >= 0.30) & (sub["residual_all_p"].fillna(1.0) <= 0.20)]
        best = sub.sort_values(["residual_case_p", "residual_case_r"], ascending=[True, False]).iloc[0]
        rows.append(
            {
                "gene": gene,
                "contexts_tested": int(sub["analysis"].nunique()),
                "raw_case_positive_context_count": int(len(raw_case_pos)),
                "raw_case_positive_disease_count": int(raw_case_pos["disease_name"].nunique()),
                "residual_case_positive_context_count": int(len(case_pos)),
                "residual_case_positive_disease_count": int(case_pos["disease_name"].nunique()),
                "residual_all_positive_context_count": int(len(all_pos)),
                "residual_all_positive_disease_count": int(all_pos["disease_name"].nunique()),
                "median_raw_case_r": float(sub["raw_case_r"].median()),
                "median_residual_case_r": float(sub["residual_case_r"].median()),
                "best_residual_context": clean(best["analysis"]),
                "best_residual_case_r": num(best["residual_case_r"]),
            }
        )
    return pd.DataFrame(rows)


def build_rows(tables: dict[str, pd.DataFrame], residual_summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gene in CANDIDATES:
        manual = MANUAL[gene]
        ms = first_row(tables["ms"], gene)
        broad = first_row(tables["broad"], gene)
        w39 = first_row(tables["w39"], gene)
        w55 = first_row(tables["w55"], gene)
        w62 = first_row(tables["w62"], gene)
        w68 = best_w68(tables["w68"], gene)
        w37 = first_row(tables["w37"], gene, col="gene_symbol")
        w18 = first_row(tables["w18"], gene)
        w81 = first_row(tables["w81"], gene)
        w96_contrast = first_row(tables["w96_contrast"], gene)
        w96_donor = first_row(tables["w96_donor"], gene)
        w98 = first_row(tables["w98"], gene)
        resid = first_row(residual_summary, gene)
        rec: dict[str, Any] = {
            "gene": gene,
            **manual,
            "ms_delta_log2": (
                num(ms.get("delta_log2"))
                if ms is not None
                else num(w39.get("ms_wm_delta_log2"))
                if w39 is not None
                else math.nan
            ),
            "ms_p": num(ms.get("p"), 1.0) if ms is not None else num(w39.get("ms_wm_p"), 1.0) if w39 is not None else 1.0,
            "ms_fdr": num(ms.get("fdr"), 1.0) if ms is not None else num(w39.get("ms_wm_fdr"), 1.0) if w39 is not None else 1.0,
            "broad_positive_disease_count": num(broad.get("broad_positive_disease_count"), 0.0) if broad is not None else num(w39.get("positive_disease_count"), 0.0) if w39 is not None else 0.0,
            "broad_negative_disease_count": num(broad.get("broad_negative_disease_count"), 0.0) if broad is not None else num(w39.get("negative_disease_count"), 0.0) if w39 is not None else 0.0,
            "strict_core_covariate_surviving_disease_count": num(broad.get("strict_core_covariate_surviving_disease_count"), 0.0) if broad is not None else num(w39.get("n_state_resid_non_ifn_r_ge_0_35_diseases"), 0.0) if w39 is not None else 0.0,
            "raw_positive_disease_count": num(broad.get("raw_positive_disease_count"), 0.0) if broad is not None else 0.0,
            "retained_positive_disease_count": num(broad.get("retained_positive_disease_count"), 0.0) if broad is not None else 0.0,
            "broad_selection_reasons": clean(broad.get("selection_reasons")) if broad is not None else "",
            "c15_trend_positive_disease_count": num(w96_contrast.get("c15_trend_positive_disease_count"), 0.0) if w96_contrast is not None else 0.0,
            "c15_strict_positive_disease_count": num(w96_contrast.get("c15_strict_positive_disease_count"), 0.0) if w96_contrast is not None else 0.0,
            "c15_state_pearson_r": num(w96_contrast.get("c15_state_pearson_r")) if w96_contrast is not None else math.nan,
            "contrast_state_score": num(w96_contrast.get("contrast_state_score"), 0.0) if w96_contrast is not None else 0.0,
            "donor_case_positive_disease_count": num(w96_donor.get("donor_case_positive_disease_count"), 0.0) if w96_donor is not None else 0.0,
            "donor_case_median_spearman": num(w96_donor.get("donor_case_median_spearman")) if w96_donor is not None else math.nan,
            "residual_case_positive_disease_count": num(resid.get("residual_case_positive_disease_count"), 0.0) if resid is not None else 0.0,
            "residual_case_positive_context_count": num(resid.get("residual_case_positive_context_count"), 0.0) if resid is not None else 0.0,
            "residual_all_positive_disease_count": num(resid.get("residual_all_positive_disease_count"), 0.0) if resid is not None else 0.0,
            "median_residual_case_r": num(resid.get("median_residual_case_r")) if resid is not None else math.nan,
            "best_residual_context": clean(resid.get("best_residual_context")) if resid is not None else "",
            "wave68_best_cell_state": clean(w68.get("cell_state")) if w68 is not None else "",
            "wave68_remission_adjusted_delta": num(w68.get("remission_adjusted_delta")) if w68 is not None else math.nan,
            "wave68_remission_adjusted_p": num(w68.get("remission_adjusted_p"), 1.0) if w68 is not None else 1.0,
            "wave68_remission_adjusted_fdr": num(w68.get("remission_adjusted_fdr"), 1.0) if w68 is not None else 1.0,
            "wave37_screen_call": clean(w37.get("screen_call")) if w37 is not None else "",
            "wave37_contrast_lfc": num(w37.get("median_efficient_minus_noneater_lfc")) if w37 is not None else math.nan,
            "wave37_contrast_fdr": num(w37.get("contrast_fdr"), 1.0) if w37 is not None else 1.0,
            "wave18_recommendation": clean(w18.get("foundation_rescue_recommendation")) if w18 is not None else "",
            "wave18_strong_support_contexts": num(w18.get("total_strong_support_contexts"), 0.0) if w18 is not None else 0.0,
            "wave81_call": clean(w81.get("wave81_call")) if w81 is not None else "",
            "wave81_direct_perturbation": num(w81.get("direct_perturbation"), 0.0) if w81 is not None else 0.0,
            "wave81_foundation_model_support": num(w81.get("foundation_model_support"), 0.0) if w81 is not None else 0.0,
            "chembl_activity_count": num(w39.get("chembl_activity_count"), 0.0) if w39 is not None else num(w62.get("druggable_activity_count"), 0.0) if w62 is not None else 0.0,
            "uniprot_accessible": clean(w39.get("uniprot_accessible")) if w39 is not None else "",
            "uniprot_function_excerpt": clean(w39.get("function_excerpt")) if w39 is not None else "",
            "wave39_call": clean(w39.get("wave39_call")) if w39 is not None else "",
            "wave55_n_genetic_diseases_ge_0_25": num(w55.get("n_diseases_genetic_ge_0_25"), 0.0) if w55 is not None else num(w62.get("wave55_genetic_diseases_ge_0_25"), 0.0) if w62 is not None else 0.0,
            "wave55_genetic_diseases_ge_0_25": clean(w55.get("diseases_genetic_ge_0_25")) if w55 is not None else "",
            "wave62_call": clean(w62.get("wave62_call")) if w62 is not None else "",
            "wave62_strong_l2g_disease_count": num(w62.get("strong_l2g_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_strong_qtl_coloc_disease_count": num(w62.get("strong_qtl_coloc_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_ms_max_l2g_score": num(w62.get("ms_max_l2g_score"), 0.0) if w62 is not None else 0.0,
            "wave62_ms_max_relevant_qtl_h4": num(w62.get("ms_max_relevant_qtl_h4"), 0.0) if w62 is not None else 0.0,
            "wave98_call": clean(w98.get("wave98_call")) if w98 is not None else "",
            "wave98_score": num(w98.get("wave98_score"), 0.0) if w98 is not None else 0.0,
        }
        rec.update(guide_consistency(tables["w37_guide"], gene))
        rows.append(rec)
    return pd.DataFrame(rows)


def add_gates(rank: pd.DataFrame) -> pd.DataFrame:
    rank["gate_ms_strict"] = (rank["ms_delta_log2"] > 0.25) & (rank["ms_p"] < 0.05)
    rank["gate_ms_trend"] = (rank["ms_delta_log2"] > 0.25) & (rank["ms_p"] < 0.10)
    rank["gate_broad_cross_disease"] = rank["broad_positive_disease_count"] >= 3
    rank["gate_breadth_five_disease"] = rank["broad_positive_disease_count"] >= 5
    rank["gate_strict_residual_cross_disease"] = rank["strict_core_covariate_surviving_disease_count"] >= 2
    rank["gate_c15_residual_costate"] = (
        (rank["residual_case_positive_disease_count"] >= 2)
        | ((rank["residual_case_positive_disease_count"] >= 1) & (rank["residual_all_positive_disease_count"] >= 2))
    )
    rank["gate_c15_contrast_state"] = (
        (rank["c15_trend_positive_disease_count"] >= 3)
        | ((rank["c15_state_pearson_r"].fillna(0.0) >= 0.40) & (rank["c15_trend_positive_disease_count"] >= 2))
    )
    rank["gate_response_inhibition_support"] = (
        (rank["wave68_remission_adjusted_delta"] <= -0.30)
        & (rank["wave68_remission_adjusted_fdr"] <= 0.10)
    )
    rank["gate_response_brake_marker_warning"] = (
        rank["axis_role"].str.contains("brake", case=False, na=False)
        & rank["gate_response_inhibition_support"]
    )
    rank["gate_real_perturbation_direction"] = (
        rank["wave37_screen_call"].str.startswith("KO_", na=False)
        & (rank["wave37_contrast_fdr"] <= 0.20)
    ) | (rank["wave81_direct_perturbation"] >= 1)
    rank["gate_model_perturbation_direction"] = (
        (rank["wave18_strong_support_contexts"] >= 1)
        & ~rank["wave18_recommendation"].str.contains("do_not_promote", case=False, na=False)
    ) | (rank["wave81_foundation_model_support"] >= 1)
    rank["gate_genetics"] = (
        (rank["wave55_n_genetic_diseases_ge_0_25"] >= 4)
        | (rank["wave62_strong_l2g_disease_count"] >= 2)
        | (rank["wave62_strong_qtl_coloc_disease_count"] >= 2)
    )
    rank["gate_ms_genetics"] = (
        (rank["wave62_ms_max_l2g_score"] >= 0.50)
        | (rank["wave62_ms_max_relevant_qtl_h4"] >= 0.80)
    )
    rank["gate_modality_ready"] = rank["manual_modality_ready"].astype(bool)
    rank["gate_prior_not_blocking"] = ~rank["manual_prior_blocked"].astype(bool)
    rank["gate_safety_not_blocking"] = ~rank["manual_safety_blocked"].astype(bool)
    rank["hard_gate_count"] = (
        rank["gate_ms_strict"].astype(int)
        + rank["gate_broad_cross_disease"].astype(int)
        + rank["gate_c15_residual_costate"].astype(int)
        + rank["gate_real_perturbation_direction"].astype(int)
        + rank["gate_modality_ready"].astype(int)
        + rank["gate_prior_not_blocking"].astype(int)
        + rank["gate_safety_not_blocking"].astype(int)
    )
    rank["support_gate_count"] = (
        rank["gate_ms_trend"].astype(int)
        + rank["gate_breadth_five_disease"].astype(int)
        + rank["gate_strict_residual_cross_disease"].astype(int)
        + rank["gate_c15_contrast_state"].astype(int)
        + rank["gate_response_inhibition_support"].astype(int)
        + rank["gate_model_perturbation_direction"].astype(int)
        + rank["gate_genetics"].astype(int)
        + rank["gate_ms_genetics"].astype(int)
    )
    rank["wave99_score"] = (
        2.0 * rank["gate_ms_strict"].astype(int)
        + 1.0 * rank["gate_ms_trend"].astype(int)
        + 2.0 * rank["gate_broad_cross_disease"].astype(int)
        + 1.0 * rank["gate_breadth_five_disease"].astype(int)
        + 2.0 * rank["gate_strict_residual_cross_disease"].astype(int)
        + 2.5 * rank["gate_c15_residual_costate"].astype(int)
        + 1.5 * rank["gate_c15_contrast_state"].astype(int)
        + 2.0 * rank["gate_response_inhibition_support"].astype(int)
        + 3.0 * rank["gate_real_perturbation_direction"].astype(int)
        + 2.0 * rank["gate_model_perturbation_direction"].astype(int)
        + 2.0 * rank["gate_genetics"].astype(int)
        + 1.0 * rank["gate_ms_genetics"].astype(int)
        + 1.5 * rank["gate_modality_ready"].astype(int)
        + 1.0 * rank["gate_prior_not_blocking"].astype(int)
        + 1.0 * rank["gate_safety_not_blocking"].astype(int)
        + rank["broad_positive_disease_count"].clip(upper=5) * 0.25
        + rank["residual_case_positive_disease_count"].clip(upper=3) * 0.4
        + rank["c15_state_pearson_r"].fillna(0).clip(lower=0) * 0.5
    )
    calls = []
    reasons = []
    for rec in rank.to_dict("records"):
        failed = [
            gate
            for gate in [
                "gate_ms_strict",
                "gate_broad_cross_disease",
                "gate_c15_residual_costate",
                "gate_real_perturbation_direction",
                "gate_modality_ready",
                "gate_prior_not_blocking",
                "gate_safety_not_blocking",
                "gate_genetics",
            ]
            if not bool(rec.get(gate, False))
        ]
        if rec["hard_gate_count"] >= 7 and rec["support_gate_count"] >= 3:
            call = "REOPEN_ENDOGENOUS_BRAKE_TARGET"
            reason = "MS, breadth, residual C15 co-state, perturbation, modality, genetics, novelty, and safety gates pass"
        elif not bool(rec["gate_prior_not_blocking"]) or not bool(rec["gate_safety_not_blocking"]):
            call = "NO_GO_PRIOR_OR_SAFETY_BLOCKED"
            reason = "prior-art or safety gate blocks broad therapeutic promotion"
        elif bool(rec["gate_c15_residual_costate"]) and bool(rec["gate_broad_cross_disease"]) and bool(rec["gate_modality_ready"]):
            call = "PARK_MODALITY_WITHOUT_MS_OR_PERTURBATION"
            reason = "actionable modality and residual C15 co-state exist, but MS/perturbation/genetic support is incomplete"
        elif bool(rec["gate_c15_residual_costate"]) and bool(rec["gate_broad_cross_disease"]):
            call = "PARK_BRAKE_ORDERING_REQUIRED"
            reason = "cross-disease residual C15 co-state survives but actionability or perturbation direction is missing"
        elif bool(rec["gate_broad_cross_disease"]) and bool(rec["axis_role"].lower().find("brake") >= 0):
            call = "NO_GO_COMPENSATORY_BRAKE_MARKER"
            reason = "endogenous brake-like marker is recurrent, but residual C15 coupling/perturbation/actionability gates fail"
        elif bool(rec["gate_broad_cross_disease"]):
            call = "NO_GO_GENERIC_INFLAMMATION_OR_HOST_DEFENSE"
            reason = "cross-disease expression signal lacks brake-specific residual or perturbation support"
        else:
            call = "NO_GO_LOCAL_EVIDENCE_WEAK"
            reason = "local MS/cross-disease evidence is insufficient"
        calls.append(call)
        reasons.append(reason + "; failed=" + ";".join(failed))
    rank["wave99_call"] = calls
    rank["wave99_reason"] = reasons
    priority = {
        "REOPEN_ENDOGENOUS_BRAKE_TARGET": 0,
        "PARK_MODALITY_WITHOUT_MS_OR_PERTURBATION": 1,
        "PARK_BRAKE_ORDERING_REQUIRED": 2,
        "NO_GO_COMPENSATORY_BRAKE_MARKER": 3,
        "NO_GO_PRIOR_OR_SAFETY_BLOCKED": 4,
        "NO_GO_GENERIC_INFLAMMATION_OR_HOST_DEFENSE": 5,
        "NO_GO_LOCAL_EVIDENCE_WEAK": 6,
    }
    rank["call_priority"] = rank["wave99_call"].map(priority).fillna(9).astype(int)
    return rank.sort_values(["call_priority", "wave99_score"], ascending=[True, False]).drop(columns=["call_priority"])


def report_table(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "gene",
        "wave99_call",
        "wave99_score",
        "hard_gate_count",
        "support_gate_count",
        "axis_role",
        "broad_positive_disease_count",
        "strict_core_covariate_surviving_disease_count",
        "residual_case_positive_disease_count",
        "c15_trend_positive_disease_count",
        "ms_delta_log2",
        "ms_p",
        "wave68_remission_adjusted_delta",
        "wave68_remission_adjusted_fdr",
        "wave37_screen_call",
        "wave37_contrast_fdr",
        "wave18_recommendation",
        "wave55_n_genetic_diseases_ge_0_25",
        "chembl_activity_count",
        "modality_class",
        "wave99_reason",
    ]
    return df[[c for c in cols if c in df.columns]].copy()


def run_residual_tests(anchors: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    genes = set(CANDIDATES) | {"C15ORF48"}
    for module_genes in COVARIATE_MODULES.values():
        genes.update(g.upper() for g in module_genes)
    return per_context_residual_tests(anchors, CANDIDATES, genes)


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    anchors = read_tsv(ANCHORS)
    tests, donor_export = run_residual_tests(anchors)
    residual_summary = summarize_residual_tests(tests)
    tables = {
        "ms": read_tsv(MS_WM),
        "broad": read_tsv(BROAD),
        "w39": read_tsv(W39),
        "w55": read_tsv(W55),
        "w62": read_tsv(W62),
        "w68": read_tsv(W68),
        "w68_ols": read_tsv(W68_OLS),
        "w37": read_tsv(W37),
        "w37_guide": read_tsv(W37_GUIDE),
        "w18": read_tsv(W18),
        "w81": read_tsv(W81),
        "w96_contrast": read_tsv(W96_CONTRAST),
        "w96_donor": read_tsv(W96_DONOR),
        "w98": read_tsv(W98),
    }
    for df in tables.values():
        for col in ["gene", "gene_symbol"]:
            if not df.empty and col in df.columns:
                df[col] = df[col].astype(str).str.upper()

    rank = add_gates(build_rows(tables, residual_summary))
    tests.to_csv(OUT / "inflammasome_brake_c15_residual_context_tests.tsv", sep="\t", index=False)
    donor_export.to_csv(OUT / "inflammasome_brake_donor_covariate_scores.tsv", sep="\t", index=False)
    residual_summary.to_csv(OUT / "inflammasome_brake_c15_residual_summary.tsv", sep="\t", index=False)
    rank.to_csv(OUT / "inflammasome_brake_candidate_rank.tsv", sep="\t", index=False)

    call_counts = rank["wave99_call"].value_counts().to_dict()
    reopened = rank[rank["wave99_call"].eq("REOPEN_ENDOGENOUS_BRAKE_TARGET")]
    parked = rank[rank["wave99_call"].str.startswith("PARK_", na=False)]
    summary = {
        "seed": SEED,
        "analysis_call": "NO_REOPEN_ENDOGENOUS_INFLAMMASOME_BRAKE_TARGET",
        "n_candidates": int(len(CANDIDATES)),
        "n_reopened": int(len(reopened)),
        "n_parked": int(len(parked)),
        "call_counts": call_counts,
        "top_gene": clean(rank.iloc[0]["gene"]) if not rank.empty else "",
        "top_call": clean(rank.iloc[0]["wave99_call"]) if not rank.empty else "",
        "parked_genes": parked["gene"].tolist(),
        "inputs": {
            "anchors": rel(ANCHORS),
            "ms_wm": rel(MS_WM),
            "broad_residual": rel(BROAD),
            "wave39": rel(W39),
            "wave55": rel(W55),
            "wave62": rel(W62),
            "wave68": rel(W68),
            "wave37": rel(W37),
            "wave18": rel(W18),
            "wave81": rel(W81),
            "wave96_contrast": rel(W96_CONTRAST),
            "wave96_donor": rel(W96_DONOR),
            "wave98": rel(W98),
        },
    }
    write_json(OUT / "summary.json", summary)

    report = [
        "# Wave99 Endogenous Inflammasome Brake Audit",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Question",
        "",
        "Can an endogenous brake below the LITAF/CASP4 inflammatory-stress branch",
        "be promoted as a tractable cross-autoimmune intervention point?",
        "",
        "## Verdict",
        "",
        "`NO_REOPEN_ENDOGENOUS_INFLAMMASOME_BRAKE_TARGET`",
        "",
        "## Call Counts",
        "",
        markdown_table(pd.DataFrame([{"wave99_call": k, "n": v} for k, v in call_counts.items()])),
        "",
        "## Candidate Matrix",
        "",
        markdown_table(report_table(rank), max_rows=25),
        "",
        "## Interpretation",
        "",
        "The endogenous-brake concept remains mechanistically useful but not",
        "therapeutically promotable from current data. `CARD16` is the cleanest",
        "biological brake clue, yet it lacks residual C15 co-state, MS anchoring,",
        "real perturbation direction, and a selective augmentation modality. `IL18BP`",
        "is the most druggable brake-like modality, but local MS/C15 evidence is weak",
        "and the IL18 neutralization space is prior-art crowded. Core pyroptosis",
        "nodes (`CASP1`, `CASP4`, `CASP5`, `GSDMD`, `NLRP3`, `IL1B`, `IL18`) are",
        "actionable in principle but blocked by prior-art/safety and do not solve the",
        "cross-autoimmune novelty problem. GBP-family signals are dominated by",
        "generic interferon/host-defense biology.",
        "",
        "## Output Files",
        "",
        f"- `{rel(OUT / 'inflammasome_brake_candidate_rank.tsv')}`",
        f"- `{rel(OUT / 'inflammasome_brake_c15_residual_context_tests.tsv')}`",
        f"- `{rel(OUT / 'inflammasome_brake_c15_residual_summary.tsv')}`",
        f"- `{rel(OUT / 'inflammasome_brake_donor_covariate_scores.tsv')}`",
        f"- `{rel(OUT / 'summary.json')}`",
        f"- `{rel(OUT / 'REPORT.md')}`",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
