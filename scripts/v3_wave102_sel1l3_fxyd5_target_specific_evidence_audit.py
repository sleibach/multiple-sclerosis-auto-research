#!/usr/bin/env python3
"""Wave102 target-specific forcing audit for SEL1L3 and FXYD5.

Wave101 left SEL1L3 and FXYD5 as accessible/surface survivors. This script
asks a stricter question: does either candidate have enough non-expression
evidence to become a target hypothesis rather than a marker/readout?

Guardrail: a tissue/cell-state expression signal is not sufficient. A candidate
must clear residualized disease signal, target-specific perturbation or
validated model support, target-resolved genetics, and modality/direction
gates. If those gates fail, the route closes even when the raw expression
effect looks attractive.
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
OUT = ROOT / "phases/v3/results" / "wave102_sel1l3_fxyd5_target_specific_evidence_audit"

W101 = ROOT / "phases/v3/results" / "wave101_accessible_survivor_forcing_triage" / "accessible_survivor_forcing_rank.tsv"
W94 = ROOT / "phases/v3/results" / "wave94_accessible_state_rerank" / "accessible_state_candidate_rank.tsv"
W94_CONTEXT = ROOT / "phases/v3/results" / "wave94_accessible_state_rerank" / "broad_candidate_context_rows.tsv"
W94_IBD_RESPONSE = ROOT / "phases/v3/results" / "wave94_accessible_state_rerank" / "ibd_candidate_response_tests.tsv"
W94_RA_RESPONSE = ROOT / "phases/v3/results" / "wave94_accessible_state_rerank" / "ra_candidate_response_tests.tsv"
W94_PS_RESPONSE = ROOT / "phases/v3/results" / "wave94_accessible_state_rerank" / "psoriasis_candidate_response_tests.tsv"
W94_GENETICS = ROOT / "phases/v3/results" / "wave94_accessible_state_rerank" / "candidate_genetics_summary.tsv"
RESIDUAL = ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
W79 = ROOT / "phases/v3/results" / "wave79_targetability_shortlist_audit" / "targetability_integrated_decision.tsv"
W79_FOUNDATION = ROOT / "phases/v3/results" / "wave79_targetability_shortlist_audit" / "targetability_foundation_rank_rows.tsv"
W81 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W37 = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W62 = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"

TARGETS = ["SEL1L3", "FXYD5", "APOC1", "CD82", "LAPTM5"]
FOCAL = {"SEL1L3", "FXYD5"}

MANUAL_TARGET_AUDIT = {
    "SEL1L3": {
        "manual_candidate_role": "undercharacterized SEL1-repeat single-pass membrane protein",
        "manual_intervention_concept": "antibody or ligand-blocking modality only if extracellular epitope and disease-cell driver function are proven",
        "manual_modality_status": "immature",
        "manual_direction_status": "unknown_driver_vs_architecture_marker",
        "manual_modality_ready": False,
        "manual_safety_blocked": False,
        "manual_route_blocker": "no known ligand/catalytic function, no target-specific perturbation, and no strong autoimmune genetic anchor",
    },
    "FXYD5": {
        "manual_candidate_role": "FXYD/dysadherin Na-K-ATPase and adhesion regulator",
        "manual_intervention_concept": "non-depleting barrier-preserving blocker only if pathogenic adhesion/licensing function is proven",
        "manual_modality_status": "conceptual_but_safety_limited",
        "manual_direction_status": "direction_conflicted_across_response_systems",
        "manual_modality_ready": False,
        "manual_safety_blocked": True,
        "manual_route_blocker": "epithelial/barrier and Na-K-ATPase coupling create liability; Crohn myeloid negative signal conflicts with a pan-autoimmune target",
    },
    "APOC1": {
        "manual_candidate_role": "secreted apolipoprotein/lipid-state protein",
        "manual_intervention_concept": "not a compartment-specific autoimmune intervention without a local delivery or isoform strategy",
        "manual_modality_status": "systemic_lipid_confounded",
        "manual_direction_status": "context_conflicted_lipid_state_marker",
        "manual_modality_ready": False,
        "manual_safety_blocked": True,
        "manual_route_blocker": "systemic lipid metabolism and contradictory tissue directions",
    },
    "CD82": {
        "manual_candidate_role": "tetraspanin/endolysosomal trafficking membrane protein",
        "manual_intervention_concept": "no clean agonist/antagonist direction from local data",
        "manual_modality_status": "pleiotropic_surface_complex",
        "manual_direction_status": "unresolved",
        "manual_modality_ready": False,
        "manual_safety_blocked": True,
        "manual_route_blocker": "tetraspanin pleiotropy and prior demotion as marker without controller evidence",
    },
    "LAPTM5": {
        "manual_candidate_role": "hematopoietic lysosomal membrane protein",
        "manual_intervention_concept": "intracellular lysosomal membrane route lacks selective accessible modality",
        "manual_modality_status": "poor_modality",
        "manual_direction_status": "unresolved",
        "manual_modality_ready": False,
        "manual_safety_blocked": False,
        "manual_route_blocker": "lysosomal membrane localization and absent causal perturbation",
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


def flag(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return clean(value).strip().lower() in {"1", "true", "yes", "y"}


def first_row(df: pd.DataFrame, gene: str, col: str = "gene") -> pd.Series | None:
    if df.empty or col not in df.columns:
        return None
    sub = df[df[col].astype(str).str.upper().eq(gene.upper())]
    if sub.empty:
        return None
    return sub.iloc[0]


def split_semicolon(value: Any) -> list[str]:
    return [x.strip() for x in clean(value).split(";") if x.strip()]


def summarize_contexts(context: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if context.empty:
        return pd.DataFrame(), pd.DataFrame()
    c = context[context["gene"].astype(str).isin(TARGETS)].copy()
    c["p"] = pd.to_numeric(c["p"], errors="coerce")
    c["delta_log2_cpm"] = pd.to_numeric(c["delta_log2_cpm"], errors="coerce")
    c["positive_nominal"] = c["positive_nominal"].astype(str).str.lower().eq("true")
    c["negative_nominal"] = c["negative_nominal"].astype(str).str.lower().eq("true")
    positive = c[c["positive_nominal"]].copy()
    negative = c[c["negative_nominal"]].copy()
    rows: list[dict[str, Any]] = []
    for gene in TARGETS:
        sub = c[c["gene"].eq(gene)]
        pos = positive[positive["gene"].eq(gene)]
        neg = negative[negative["gene"].eq(gene)]
        tissue_pos = pos[pos["role"].eq("tissue_resident")]
        myeloid_pos = pos[pos["role"].eq("myeloid_apc")]
        rows.append(
            {
                "gene": gene,
                "raw_contexts_tested": int(len(sub)),
                "raw_positive_contexts": int(len(pos)),
                "raw_negative_contexts": int(len(neg)),
                "raw_positive_diseases": ";".join(sorted(pos["disease_name"].dropna().astype(str).unique())),
                "raw_negative_diseases": ";".join(sorted(neg["disease_name"].dropna().astype(str).unique())),
                "raw_tissue_resident_positive_contexts": int(len(tissue_pos)),
                "raw_myeloid_positive_contexts": int(len(myeloid_pos)),
                "best_raw_positive_context": "",
                "best_raw_positive_delta": math.nan,
                "best_raw_positive_p": math.nan,
            }
        )
        if not pos.empty:
            best = pos.sort_values(["p", "delta_log2_cpm"], ascending=[True, False]).iloc[0]
            rows[-1]["best_raw_positive_context"] = (
                f"{best['analysis']}|{best['disease_name']}|{best['compartment']}"
            )
            rows[-1]["best_raw_positive_delta"] = num(best.get("delta_log2_cpm"))
            rows[-1]["best_raw_positive_p"] = num(best.get("p"))
    return pd.DataFrame(rows), c


def aggregate_response(paths: list[Path]) -> pd.DataFrame:
    frames = []
    for path in paths:
        df = read_tsv(path)
        if not df.empty:
            df["source_file"] = rel(path)
            frames.append(df)
    if not frames:
        return pd.DataFrame()
    r = pd.concat(frames, ignore_index=True, sort=False)
    r = r[r["gene"].astype(str).isin(TARGETS)].copy()
    r["p"] = pd.to_numeric(r["p"], errors="coerce")
    for col in ["fdr", "fdr_all", "fdr_within_cohort", "fdr_within_treatment"]:
        if col in r.columns:
            r[col] = pd.to_numeric(r[col], errors="coerce")
    r["hedges_g_responder_minus_non"] = pd.to_numeric(r["hedges_g_responder_minus_non"], errors="coerce")
    r["nonresponse_high_direction"] = r["nonresponse_high_direction"].astype(str).str.lower().eq("true")
    rows: list[dict[str, Any]] = []
    for gene in TARGETS:
        sub = r[r["gene"].eq(gene)].copy()
        nominal = sub[sub["p"] < 0.05]
        nonresp = nominal[nominal["nonresponse_high_direction"]]
        resp = nominal[~nominal["nonresponse_high_direction"]]
        best = sub.sort_values("p").iloc[0] if not sub.empty else None
        rows.append(
            {
                "gene": gene,
                "response_tests": int(len(sub)),
                "response_nominal_tests": int(len(nominal)),
                "response_nonresponse_high_nominal": int(len(nonresp)),
                "response_responder_high_nominal": int(len(resp)),
                "response_direction_conflict_from_rows": bool((len(nonresp) > 0) and (len(resp) > 0)),
                "response_best_p": num(best.get("p"), 1.0) if best is not None else 1.0,
                "response_best_system": clean(best.get("system")) if best is not None else "",
                "response_best_cohort": clean(best.get("cohort")) if best is not None else "",
                "response_best_g": num(best.get("hedges_g_responder_minus_non")) if best is not None else math.nan,
                "response_best_nonresponse_high": flag(best.get("nonresponse_high_direction")) if best is not None else False,
            }
        )
    return pd.DataFrame(rows)


def collect_evidence(tables: dict[str, pd.DataFrame], context_summary: pd.DataFrame, response: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for gene in TARGETS:
        manual = MANUAL_TARGET_AUDIT[gene]
        w101 = first_row(tables["w101"], gene)
        w94 = first_row(tables["w94"], gene)
        residual = first_row(tables["residual"], gene)
        w79 = first_row(tables["w79"], gene)
        w79f = first_row(tables["w79_foundation"], gene)
        w81 = first_row(tables["w81"], gene)
        w37 = first_row(tables["w37"], gene, "gene_symbol")
        w62 = first_row(tables["w62"], gene)
        w94g = first_row(tables["w94_genetics"], gene)
        ctx = first_row(context_summary, gene)
        resp = first_row(response, gene)

        rec: dict[str, Any] = {
            "gene": gene,
            "is_focal": gene in FOCAL,
            **manual,
            "wave101_call": clean(w101.get("wave101_call")) if w101 is not None else "",
            "wave101_score": num(w101.get("wave101_score")) if w101 is not None else math.nan,
            "ms_delta_log2": num(w101.get("ms_delta_log2")) if w101 is not None else num(w94.get("ms_wm_delta_log2")) if w94 is not None else math.nan,
            "ms_p": num(w101.get("ms_p"), 1.0) if w101 is not None else num(w94.get("ms_wm_p"), 1.0) if w94 is not None else 1.0,
            "ms_fdr": num(w94.get("ms_wm_fdr"), 1.0) if w94 is not None else 1.0,
            "raw_positive_disease_count": num(w94.get("positive_disease_count"), 0.0) if w94 is not None else 0.0,
            "raw_negative_disease_count": num(w94.get("negative_disease_count"), 0.0) if w94 is not None else 0.0,
            "raw_positive_diseases_w94": clean(w94.get("positive_diseases")) if w94 is not None else "",
            "raw_negative_diseases_w94": clean(w94.get("negative_diseases")) if w94 is not None else "",
            "raw_positive_contexts": num(ctx.get("raw_positive_contexts"), 0.0) if ctx is not None else 0.0,
            "raw_negative_contexts": num(ctx.get("raw_negative_contexts"), 0.0) if ctx is not None else 0.0,
            "raw_tissue_resident_positive_contexts": num(ctx.get("raw_tissue_resident_positive_contexts"), 0.0) if ctx is not None else 0.0,
            "raw_myeloid_positive_contexts": num(ctx.get("raw_myeloid_positive_contexts"), 0.0) if ctx is not None else 0.0,
            "best_raw_positive_context": clean(ctx.get("best_raw_positive_context")) if ctx is not None else "",
            "best_raw_positive_delta": num(ctx.get("best_raw_positive_delta")) if ctx is not None else math.nan,
            "best_raw_positive_p": num(ctx.get("best_raw_positive_p"), 1.0) if ctx is not None else 1.0,
            "residual_raw_positive_analysis_count": num(residual.get("raw_positive_analysis_count"), 0.0) if residual is not None else 0.0,
            "residual_raw_positive_disease_count": num(residual.get("raw_positive_disease_count"), 0.0) if residual is not None else 0.0,
            "residual_retained_positive_analysis_count": num(residual.get("retained_positive_analysis_count"), 0.0) if residual is not None else 0.0,
            "residual_retained_positive_disease_count": num(residual.get("retained_positive_disease_count"), 0.0) if residual is not None else 0.0,
            "residual_strict_core_disease_count": num(residual.get("strict_core_covariate_surviving_disease_count"), 0.0) if residual is not None else 0.0,
            "residual_top_retained_tests": clean(residual.get("top_retained_tests")) if residual is not None else "",
            "response_tests": num(resp.get("response_tests"), 0.0) if resp is not None else 0.0,
            "response_nominal_tests": num(resp.get("response_nominal_tests"), 0.0) if resp is not None else 0.0,
            "response_nonresponse_high_nominal": num(resp.get("response_nonresponse_high_nominal"), 0.0) if resp is not None else 0.0,
            "response_responder_high_nominal": num(resp.get("response_responder_high_nominal"), 0.0) if resp is not None else 0.0,
            "response_direction_conflict_from_rows": flag(resp.get("response_direction_conflict_from_rows")) if resp is not None else False,
            "response_best_p": num(resp.get("response_best_p"), 1.0) if resp is not None else 1.0,
            "response_best_system": clean(resp.get("response_best_system")) if resp is not None else "",
            "response_best_cohort": clean(resp.get("response_best_cohort")) if resp is not None else "",
            "response_best_g": num(resp.get("response_best_g")) if resp is not None else math.nan,
            "response_best_nonresponse_high": flag(resp.get("response_best_nonresponse_high")) if resp is not None else False,
            "wave81_call": clean(w81.get("wave81_call")) if w81 is not None else "",
            "wave81_direct_perturbation": num(w81.get("direct_perturbation"), 0.0) if w81 is not None else 0.0,
            "wave81_foundation_model_support": num(w81.get("foundation_model_support"), 0.0) if w81 is not None else 0.0,
            "wave81_detail": (clean(w81.get("direct_perturbation_detail")) + " " + clean(w81.get("foundation_model_detail"))).strip() if w81 is not None else "",
            "wave37_screen_call": clean(w37.get("screen_call")) if w37 is not None else "",
            "wave37_contrast_lfc": num(w37.get("median_efficient_minus_noneater_lfc")) if w37 is not None else math.nan,
            "wave37_contrast_fdr": num(w37.get("contrast_fdr"), 1.0) if w37 is not None else 1.0,
            "foundation_total_support_contexts": num(w79f.get("total_support_contexts"), 0.0) if w79f is not None else 0.0,
            "foundation_total_strong_support_contexts": num(w79f.get("total_strong_support_contexts"), 0.0) if w79f is not None else 0.0,
            "foundation_alignment_call": clean(w79f.get("real_perturbation_alignment_call")) if w79f is not None else "",
            "foundation_recommendation": clean(w79f.get("foundation_rescue_recommendation")) if w79f is not None else "",
            "foundation_best_context": clean(w79f.get("best_geneformer_context")) if w79f is not None else "",
            "foundation_best_projection_shift": num(w79f.get("best_mean_projection_shift")) if w79f is not None else math.nan,
            "wave62_call": clean(w62.get("wave62_call")) if w62 is not None else "",
            "wave62_max_l2g_score": num(w62.get("max_l2g_score"), 0.0) if w62 is not None else 0.0,
            "wave62_best_l2g_disease": clean(w62.get("best_l2g_disease")) if w62 is not None else "",
            "wave62_strong_l2g_disease_count": num(w62.get("strong_l2g_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_supporting_l2g_disease_count": num(w62.get("supporting_l2g_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_strong_qtl_coloc_disease_count": num(w62.get("strong_qtl_coloc_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_ms_max_l2g_score": num(w62.get("ms_max_l2g_score"), 0.0) if w62 is not None else 0.0,
            "wave62_ms_max_relevant_qtl_h4": num(w62.get("ms_max_relevant_qtl_h4"), 0.0) if w62 is not None else 0.0,
            "wave94_genetic_disease_count_max": num(w94g.get("genetic_disease_count_max"), 0.0) if w94g is not None else 0.0,
            "wave94_genetic_disease_text": clean(w94g.get("genetic_disease_text")) if w94g is not None else "",
            "wave79_call": clean(w79.get("wave79_call")) if w79 is not None else "",
            "wave79_reason": clean(w79.get("decision_reason")) if w79 is not None else "",
        }
        rows.append(rec)
    return pd.DataFrame(rows)


def add_target_calls(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    numeric_cols = [
        "ms_delta_log2",
        "raw_positive_disease_count",
        "raw_negative_disease_count",
        "raw_tissue_resident_positive_contexts",
        "raw_myeloid_positive_contexts",
        "residual_retained_positive_disease_count",
        "residual_strict_core_disease_count",
        "response_nonresponse_high_nominal",
        "response_responder_high_nominal",
        "wave81_direct_perturbation",
        "wave81_foundation_model_support",
        "wave37_contrast_fdr",
        "foundation_total_strong_support_contexts",
        "wave62_strong_l2g_disease_count",
        "wave62_strong_qtl_coloc_disease_count",
        "wave62_ms_max_l2g_score",
        "wave62_ms_max_relevant_qtl_h4",
    ]
    for col in numeric_cols:
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)

    out["gate_ms_nominal_anchor"] = (out["ms_delta_log2"] > 0.25) & (out["ms_p"] < 0.10)
    out["gate_cross_disease_raw_breadth"] = out["raw_positive_disease_count"] >= 3
    out["gate_low_raw_contradiction"] = out["raw_negative_disease_count"] <= 1
    out["gate_compartment_specificity"] = out["raw_tissue_resident_positive_contexts"] >= 3
    out["gate_residualized_cross_disease"] = (
        (out["residual_retained_positive_disease_count"] >= 3)
        & (out["residual_strict_core_disease_count"] >= 1)
    )
    out["gate_response_direction_support"] = (
        (out["response_nonresponse_high_nominal"] >= 2)
        & (out["response_responder_high_nominal"] == 0)
        & ~out["response_direction_conflict_from_rows"]
    )
    out["gate_real_perturbation_or_validated_model"] = (
        (out["wave81_direct_perturbation"] > 0)
        | (
            (out["wave81_foundation_model_support"] > 0)
            & ~out["wave81_detail"].str.contains("do_not_promote|model_only", case=False, na=False)
        )
        | (
            (out["foundation_total_strong_support_contexts"] >= 2)
            & ~out["foundation_recommendation"].str.contains("do_not_promote|triage_only", case=False, na=False)
            & ~out["foundation_alignment_call"].str.contains("model_only", case=False, na=False)
        )
        | (out["wave37_contrast_fdr"] <= 0.10)
    )
    out["gate_target_resolved_genetic_anchor"] = (
        (out["wave62_strong_l2g_disease_count"] >= 2)
        | (out["wave62_strong_qtl_coloc_disease_count"] >= 2)
        | (out["wave62_ms_max_l2g_score"] >= 0.5)
        | (out["wave62_ms_max_relevant_qtl_h4"] >= 0.8)
    )
    out["gate_modality_ready"] = out["manual_modality_ready"].astype(bool)
    out["gate_no_safety_blocker"] = ~out["manual_safety_blocked"].astype(bool)
    out["gate_focal_candidate"] = out["is_focal"].astype(bool)

    strict_gates = [
        "gate_ms_nominal_anchor",
        "gate_cross_disease_raw_breadth",
        "gate_low_raw_contradiction",
        "gate_compartment_specificity",
        "gate_residualized_cross_disease",
        "gate_response_direction_support",
        "gate_real_perturbation_or_validated_model",
        "gate_target_resolved_genetic_anchor",
        "gate_modality_ready",
        "gate_no_safety_blocker",
    ]
    out["wave102_gate_count"] = out[strict_gates].sum(axis=1).astype(int)
    missing = []
    calls = []
    for _, row in out.iterrows():
        missing_gates = [g.replace("gate_", "") for g in strict_gates if not bool(row[g])]
        missing.append(";".join(missing_gates))
        if not bool(row["gate_focal_candidate"]):
            calls.append("COMPARATOR_ONLY")
        elif not bool(row["gate_real_perturbation_or_validated_model"]):
            calls.append("NO_GO_NO_TARGET_SPECIFIC_PERTURBATION_OR_VALIDATED_MODEL")
        elif not bool(row["gate_residualized_cross_disease"]):
            calls.append("NO_GO_RAW_EXPRESSION_NOT_RESIDUALIZED")
        elif not bool(row["gate_target_resolved_genetic_anchor"]):
            calls.append("NO_GO_NO_TARGET_RESOLVED_GENETIC_ANCHOR")
        elif not bool(row["gate_modality_ready"]):
            calls.append("NO_GO_NO_SELECTIVE_MODALITY")
        elif not bool(row["gate_no_safety_blocker"]):
            calls.append("NO_GO_SAFETY_OR_DIRECTIONALITY_BLOCKED")
        elif not bool(row["gate_response_direction_support"]):
            calls.append("PARK_RESPONSE_DIRECTION_UNRESOLVED")
        else:
            calls.append("PROMOTE_TARGET_SPECIFIC_BRANCH")
    out["wave102_missing_gates"] = missing
    out["wave102_call"] = calls
    out["wave102_target_score"] = (
        out["wave102_gate_count"] * 2.0
        + out["raw_positive_disease_count"].clip(upper=5) * 0.75
        + out["residual_retained_positive_disease_count"].clip(upper=5) * 1.25
        + out["residual_strict_core_disease_count"].clip(upper=3) * 2.0
        + out["response_nonresponse_high_nominal"].clip(upper=5) * 0.75
        + out["wave81_direct_perturbation"] * 3.0
        + out["foundation_total_strong_support_contexts"].clip(upper=3) * 0.5
        + out["wave62_strong_l2g_disease_count"].clip(upper=4) * 1.5
        - out["raw_negative_disease_count"].clip(upper=3) * 1.5
        - out["response_responder_high_nominal"].clip(upper=5) * 1.0
        - out["manual_safety_blocked"].astype(int) * 2.5
    )
    return out.sort_values(["is_focal", "wave102_target_score"], ascending=[False, False])


def write_report(rank: pd.DataFrame, context_rows: pd.DataFrame, summary: dict[str, Any]) -> None:
    cols = [
        "gene",
        "wave102_call",
        "wave102_target_score",
        "wave102_gate_count",
        "ms_delta_log2",
        "ms_p",
        "raw_positive_disease_count",
        "raw_negative_disease_count",
        "residual_retained_positive_disease_count",
        "residual_strict_core_disease_count",
        "response_nonresponse_high_nominal",
        "response_responder_high_nominal",
        "wave81_direct_perturbation",
        "foundation_total_strong_support_contexts",
        "wave62_strong_l2g_disease_count",
        "wave62_strong_qtl_coloc_disease_count",
        "manual_modality_status",
        "manual_direction_status",
        "manual_route_blocker",
        "wave102_missing_gates",
    ]
    ctx_cols = [
        "analysis",
        "disease_name",
        "compartment",
        "role",
        "gene",
        "delta_log2_cpm",
        "hedges_g",
        "p",
        "fdr",
        "positive_nominal",
        "negative_nominal",
    ]
    focal_context = context_rows[
        context_rows["gene"].isin(sorted(FOCAL))
        & (context_rows["positive_nominal"] | context_rows["negative_nominal"])
    ].sort_values(["gene", "positive_nominal", "p"], ascending=[True, False, True])
    report = f"""# Wave102 SEL1L3/FXYD5 Target-Specific Evidence Audit

## Bottom Line

Branch call: `{summary["branch_call"]}`.

Neither focal accessible survivor clears the minimum target-specific evidence
bar. `SEL1L3` has the cleaner raw tissue-resident expression signal, but it
does not survive as a cross-disease residualized controller and has no real
perturbation, validated model, selective modality, or strong target-resolved
genetic anchor. `FXYD5` has a clearer protein-biophysics story, but the route
is direction-conflicted, safety-limited by epithelial/barrier and Na-K-ATPase
biology, and lacks the same perturbation/genetic anchors.

## Target-Specific Ranking

{markdown_table(rank[cols], max_rows=20)}

## Focal Raw Contexts

{markdown_table(focal_context[ctx_cols], max_rows=30)}

## Interpretation

- Raw expression is not the limiting issue. `SEL1L3` and `FXYD5` both recur
  across tissue-resident disease compartments.
- The limiting issue is non-expression anchoring. The residual gate collapses
  the apparent breadth to weak or narrow context support, and neither focal
  candidate has a target-specific perturbation that reverses the
  lipid-lysosomal/inflammatory state.
- Foundation-model rows are retained only as triage evidence. `SEL1L3` has a
  prior model-only supportive row, but it is explicitly marked
  `do_not_promote_from_foundation_model`, so it cannot satisfy perturbation.
- The accessible-survivor route should be closed unless a new wet-lab or public
  perturbation dataset directly perturbs `SEL1L3` or `FXYD5` in the relevant
  stromal/epithelial/endothelial context and shows disease-state reversal
  without barrier toxicity.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave102_sel1l3_fxyd5_target_specific_evidence_audit.py")}`
- Rank table: `{rel(OUT / "target_specific_evidence_rank.tsv")}`
- Context rows: `{rel(OUT / "focal_context_rows.tsv")}`
- Summary: `{rel(OUT / "summary.json")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    tables = {
        "w101": read_tsv(W101),
        "w94": read_tsv(W94),
        "residual": read_tsv(RESIDUAL),
        "w79": read_tsv(W79),
        "w79_foundation": read_tsv(W79_FOUNDATION),
        "w81": read_tsv(W81),
        "w37": read_tsv(W37),
        "w62": read_tsv(W62),
        "w94_genetics": read_tsv(W94_GENETICS),
    }
    context_summary, context_rows = summarize_contexts(read_tsv(W94_CONTEXT))
    response = aggregate_response([W94_IBD_RESPONSE, W94_RA_RESPONSE, W94_PS_RESPONSE])
    rank = add_target_calls(collect_evidence(tables, context_summary, response))

    rank.to_csv(OUT / "target_specific_evidence_rank.tsv", sep="\t", index=False)
    context_summary.to_csv(OUT / "context_summary.tsv", sep="\t", index=False)
    response.to_csv(OUT / "response_summary.tsv", sep="\t", index=False)
    context_rows[context_rows["gene"].isin(sorted(FOCAL))].to_csv(OUT / "focal_context_rows.tsv", sep="\t", index=False)

    promoted = rank[rank["wave102_call"].eq("PROMOTE_TARGET_SPECIFIC_BRANCH")]
    branch_call = (
        "PROMOTE_TARGET_SPECIFIC_BRANCH"
        if not promoted.empty
        else "NO_PROMOTABLE_SEL1L3_FXYD5_TARGET_SPECIFIC_EVIDENCE"
    )
    summary = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "n_candidates": int(len(rank)),
        "focal_candidates": sorted(FOCAL),
        "promoted_candidates": promoted["gene"].tolist(),
        "call_counts": rank["wave102_call"].value_counts().to_dict(),
        "top_focal_candidate": rank[rank["is_focal"]].iloc[0]["gene"],
        "top_focal_call": rank[rank["is_focal"]].iloc[0]["wave102_call"],
        "inputs": {
            "wave101": rel(W101),
            "wave94": rel(W94),
            "wave94_context": rel(W94_CONTEXT),
            "wave94_ibd_response": rel(W94_IBD_RESPONSE),
            "wave94_ra_response": rel(W94_RA_RESPONSE),
            "wave94_ps_response": rel(W94_PS_RESPONSE),
            "wave94_genetics": rel(W94_GENETICS),
            "broad_residual": rel(RESIDUAL),
            "wave79": rel(W79),
            "wave79_foundation": rel(W79_FOUNDATION),
            "wave81": rel(W81),
            "wave37": rel(W37),
            "wave62": rel(W62),
        },
    }
    write_json(OUT / "summary.json", summary)
    write_report(rank, context_rows, summary)


if __name__ == "__main__":
    main()
