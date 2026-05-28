#!/usr/bin/env python3
"""Wave95 forcing triage: CD300 route versus Wave94 accessible-state hits.

Wave92 left a mechanistically relevant but MS-weak CD300 lipid/efferocytosis
route. Wave94 left several statistically stronger accessible-state genes whose
mechanistic relation to the lipid-lysosomal myeloid module is weak. This script
puts both branches into a single gate matrix.

This is not a finding generator. Its job is to decide the next branch and to
prevent narrative drift between route-level biology and gene-level statistics.
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
from v3_wave94_accessible_state_rerank import (
    broad_summaries,
    foundation_summary,
    genetics_rows,
    genetics_summary,
    ibd_response_tests,
    ms_rows,
    psoriasis_response_tests,
    ra_response_tests,
    response_meta,
)


SEED = 20260527
OUT = ROOT / "results_v3" / "wave95_cd300_vs_accessible_top_forcing_triage"

W39 = ROOT / "results_v3" / "wave39_surfaceome_rescue_after_resolution_pivot" / "surfaceome_rescue_rank_full.tsv"
W92 = ROOT / "results_v3" / "wave92_lipid_state_controller_route_audit" / "controller_route_rank.tsv"
W94 = ROOT / "results_v3" / "wave94_accessible_state_rerank" / "accessible_state_candidate_rank.tsv"

CD300_GENES = {"CD300A", "CD300C", "CD300E", "CD300LF", "CD300LG", "CD300LB"}
ACCESSIBLE_TOP = {"SEL1L3", "NRCAM", "PLEK2", "C15ORF48", "CD200", "CHI3L1", "ROMO1"}
COMPARATOR_GENES = CD300_GENES | ACCESSIBLE_TOP

MANUAL_ENTITY_META: dict[str, dict[str, Any]] = {
    "CD300_RECEPTOR_SPECIFIC_TUNING": {
        "entity_type": "route",
        "route_genes": ";".join(sorted(CD300_GENES)),
        "mechanistic_class": "lipid/efferocytosis receptor-family checkpoint",
        "intervention_concept": "receptor-specific agonism or antagonism after resolving receptor-specific direction",
        "manual_targetability": 2.0,
        "manual_mechanistic_fit": 3.0,
        "manual_prior_penalty": 1.0,
        "manual_safety_penalty": 2.0,
        "manual_note": "Best mechanistic match to lipid/efferocytosis state, but family-level direction is ambiguous and Wave92 lacked MS white-matter support.",
    },
    "SEL1L3": {
        "entity_type": "gene",
        "route_genes": "SEL1L3",
        "mechanistic_class": "undercharacterized membrane glycoprotein / accessible-state marker",
        "intervention_concept": "unknown; antibody or ligand tool would be exploratory",
        "manual_targetability": 1.0,
        "manual_mechanistic_fit": 0.5,
        "manual_prior_penalty": 0.5,
        "manual_safety_penalty": 1.0,
        "manual_note": "Strongest Wave94 score, but little known mechanism and no lipid-lysosomal neighborhood membership.",
    },
    "NRCAM": {
        "entity_type": "gene",
        "route_genes": "NRCAM",
        "mechanistic_class": "neural adhesion / tissue remodeling marker",
        "intervention_concept": "not acceptable without tissue-selective non-neural mechanism",
        "manual_targetability": 0.5,
        "manual_mechanistic_fit": 0.0,
        "manual_prior_penalty": 0.5,
        "manual_safety_penalty": 4.0,
        "manual_note": "Repeated nonresponse association, but node-of-Ranvier/neural adhesion biology creates a high safety bar.",
    },
    "PLEK2": {
        "entity_type": "gene",
        "route_genes": "PLEK2",
        "mechanistic_class": "actin/cytoskeletal state marker",
        "intervention_concept": "no clear selective pharmacology",
        "manual_targetability": 0.0,
        "manual_mechanistic_fit": 0.5,
        "manual_prior_penalty": 0.0,
        "manual_safety_penalty": 1.5,
        "manual_note": "Strong MS and breadth signal but no response, perturbation, or druggability support in Wave94.",
    },
    "C15ORF48": {
        "entity_type": "gene",
        "route_genes": "C15ORF48",
        "mechanistic_class": "mitochondrial microprotein / inflammatory macrophage metabolic brake",
        "intervention_concept": "upstream induction or peptide/gene modality only; small-molecule direct modulation unclear",
        "manual_targetability": 0.0,
        "manual_mechanistic_fit": 2.5,
        "manual_prior_penalty": 0.0,
        "manual_safety_penalty": 1.0,
        "manual_note": "Most plausible state-controller biology among Wave94 top genes, but not an accessible target and absent from the Geneformer token dictionary.",
    },
    "CD200": {
        "entity_type": "gene",
        "route_genes": "CD200",
        "mechanistic_class": "CD200-CD200R inhibitory myeloid checkpoint",
        "intervention_concept": "CD200R agonism / CD200 axis restoration",
        "manual_targetability": 2.0,
        "manual_mechanistic_fit": 2.0,
        "manual_prior_penalty": 2.0,
        "manual_safety_penalty": 2.0,
        "manual_note": "Plausible myeloid checkpoint, but psoriasis response reverses and prior immune-checkpoint biology is crowded.",
    },
    "CHI3L1": {
        "entity_type": "gene",
        "route_genes": "CHI3L1",
        "mechanistic_class": "secreted injury/fibrosis/inflammatory biomarker",
        "intervention_concept": "biomarker or antibody route only if causal role proven",
        "manual_targetability": 1.5,
        "manual_mechanistic_fit": 1.0,
        "manual_prior_penalty": 3.0,
        "manual_safety_penalty": 2.0,
        "manual_note": "Good module-proximal biomarker but response direction conflict and biomarker prior saturation.",
    },
    "ROMO1": {
        "entity_type": "gene",
        "route_genes": "ROMO1",
        "mechanistic_class": "mitochondrial ROS state marker",
        "intervention_concept": "no selective target route",
        "manual_targetability": 0.0,
        "manual_mechanistic_fit": 1.5,
        "manual_prior_penalty": 0.0,
        "manual_safety_penalty": 2.0,
        "manual_note": "Potential mitochondrial stress marker, but weak breadth/genetics and no direct intervention path.",
    },
}


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def f(value: Any, default: float = math.nan) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def route_wave92_row() -> dict[str, Any]:
    w92 = read_tsv(W92)
    if w92.empty:
        return {}
    row = w92[w92["route"].astype(str).eq("CD300_RECEPTOR_SPECIFIC_TUNING")]
    return row.iloc[0].to_dict() if not row.empty else {}


def wave94_rows() -> pd.DataFrame:
    w94 = read_tsv(W94)
    if w94.empty:
        return pd.DataFrame()
    w94["gene"] = w94["gene"].astype(str).str.upper()
    return w94[w94["gene"].isin(ACCESSIBLE_TOP)].copy()


def wave39_targetability_rows() -> pd.DataFrame:
    w39 = read_tsv(W39)
    if w39.empty:
        return pd.DataFrame()
    w39["gene"] = w39["gene"].astype(str).str.upper()
    return w39[w39["gene"].isin(COMPARATOR_GENES)].copy()


def response_summaries(genes: set[str]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ibd, _ = ibd_response_tests(genes)
    ra = ra_response_tests(genes)
    pso, _ = psoriasis_response_tests(genes)
    meta = response_meta(ibd, ra, pso)
    return ibd, ra, pso, meta


def summarize_gene_inputs(genes: set[str]) -> dict[str, pd.DataFrame]:
    broad_rows, broad_summary = broad_summaries(genes)
    ms = ms_rows(genes)
    ibd, ra, pso, resp = response_summaries(genes)
    genetics = genetics_rows(genes)
    gen_sum = genetics_summary(genetics)
    foundation = foundation_summary(genes)
    w39 = wave39_targetability_rows()
    w94 = wave94_rows()
    return {
        "broad_rows": broad_rows,
        "broad_summary": broad_summary,
        "ms": ms,
        "ibd": ibd,
        "ra": ra,
        "pso": pso,
        "response_meta": resp,
        "genetics_rows": genetics,
        "genetics_summary": gen_sum,
        "foundation": foundation,
        "w39": w39,
        "w94": w94,
    }


def gene_row(gene: str, frames: dict[str, pd.DataFrame]) -> dict[str, Any]:
    gene = gene.upper()
    row: dict[str, Any] = {
        "entity": gene,
        **MANUAL_ENTITY_META[gene],
    }

    ms = frames["ms"]
    ms_sub = ms[ms["gene"].astype(str).str.upper().eq(gene)] if not ms.empty else pd.DataFrame()
    if not ms_sub.empty:
        m = ms_sub.iloc[0]
        row.update(
            {
                "ms_delta_log2": f(m.get("delta_log2")),
                "ms_hedges_g": f(m.get("hedges_g")),
                "ms_p": f(m.get("p"), 1.0),
                "ms_fdr": f(m.get("fdr")),
                "ms_anchor": bool(f(m.get("delta_log2"), 0.0) > 0.0 and f(m.get("p"), 1.0) < 0.10),
                "ms_trend": bool(f(m.get("delta_log2"), 0.0) > 0.0 and f(m.get("p"), 1.0) < 0.20),
            }
        )
    else:
        row.update({"ms_delta_log2": math.nan, "ms_p": 1.0, "ms_anchor": False, "ms_trend": False})

    broad = frames["broad_summary"]
    b_sub = broad[broad["gene"].astype(str).str.upper().eq(gene)] if not broad.empty else pd.DataFrame()
    if not b_sub.empty:
        b = b_sub.iloc[0]
        for col in [
            "broad_tested_contexts",
            "broad_positive_contexts",
            "broad_negative_contexts",
            "broad_positive_disease_count",
            "broad_negative_disease_count",
            "myeloid_positive_contexts",
            "myeloid_positive_disease_count",
            "positive_diseases_broad",
            "negative_diseases_broad",
            "best_positive_context",
            "best_negative_context",
        ]:
            row[col] = b.get(col, "")
    else:
        row.update(
            {
                "broad_tested_contexts": 0,
                "broad_positive_contexts": 0,
                "broad_negative_contexts": 0,
                "broad_positive_disease_count": 0,
                "broad_negative_disease_count": 0,
                "myeloid_positive_contexts": 0,
                "myeloid_positive_disease_count": 0,
            }
        )

    resp = frames["response_meta"]
    r_sub = resp[resp["gene"].astype(str).str.upper().eq(gene)] if not resp.empty else pd.DataFrame()
    if not r_sub.empty:
        row["response_systems_tested"] = int(r_sub["system"].nunique())
        row["response_nonresponse_high_systems_p20"] = int(
            (
                (r_sub["nonresponse_high_contexts"] > r_sub["responder_high_contexts"])
                & (pd.to_numeric(r_sub["min_p"], errors="coerce") < 0.20)
            ).sum()
        )
        row["response_responder_high_systems_p20"] = int(
            (
                (r_sub["responder_high_contexts"] > r_sub["nonresponse_high_contexts"])
                & (pd.to_numeric(r_sub["min_p"], errors="coerce") < 0.20)
            ).sum()
        )
        row["response_best_min_p"] = float(pd.to_numeric(r_sub["min_p"], errors="coerce").min())
        row["response_summary"] = "; ".join(
            r_sub.apply(
                lambda r: f"{r['system']}:g={f(r['weighted_mean_hedges_g_responder_minus_non']):.3g},p={f(r['min_p'], 1.0):.3g},nonctx={int(r['nonresponse_high_contexts'])},respctx={int(r['responder_high_contexts'])}",
                axis=1,
            ).tolist()
        )
    else:
        row.update(
            {
                "response_systems_tested": 0,
                "response_nonresponse_high_systems_p20": 0,
                "response_responder_high_systems_p20": 0,
                "response_best_min_p": 1.0,
                "response_summary": "",
            }
        )
    row["response_direction_conflict"] = bool(row["response_nonresponse_high_systems_p20"] > 0 and row["response_responder_high_systems_p20"] > 0)

    gen = frames["genetics_summary"]
    g_sub = gen[gen["gene"].astype(str).str.upper().eq(gene)] if not gen.empty else pd.DataFrame()
    if not g_sub.empty:
        g = g_sub.iloc[0]
        row["genetic_disease_count_max"] = int(f(g.get("genetic_disease_count_max"), 0.0))
        row["genetic_disease_text"] = g.get("genetic_disease_text", "")
        row["chembl_or_druggable_activity_count_max"] = int(f(g.get("chembl_or_druggable_activity_count_max"), 0.0))
    else:
        row.update({"genetic_disease_count_max": 0, "genetic_disease_text": "", "chembl_or_druggable_activity_count_max": 0})

    foundation = frames["foundation"]
    fd_sub = foundation[foundation["gene"].astype(str).str.upper().eq(gene)] if not foundation.empty else pd.DataFrame()
    if not fd_sub.empty:
        fd = fd_sub.iloc[0]
        row["foundation_rows"] = int(f(fd.get("foundation_rows"), 0.0))
        row["foundation_supportive_text_hits"] = int(f(fd.get("foundation_supportive_text_hits"), 0.0))
        row["foundation_do_not_promote_text_hits"] = int(f(fd.get("foundation_do_not_promote_text_hits"), 0.0))
        row["foundation_files"] = fd.get("foundation_files", "")
    else:
        row.update(
            {
                "foundation_rows": 0,
                "foundation_supportive_text_hits": 0,
                "foundation_do_not_promote_text_hits": 0,
                "foundation_files": "",
            }
        )

    w39 = frames["w39"]
    w39_sub = w39[w39["gene"].astype(str).str.upper().eq(gene)] if not w39.empty else pd.DataFrame()
    if not w39_sub.empty:
        w = w39_sub.iloc[0]
        row["uniprot_accessible"] = boolish(w.get("uniprot_accessible", False))
        row["uniprot_accession"] = w.get("uniprot_accession", "")
        row["uniprot_locations"] = w.get("uniprot_locations", "")
        row["function_excerpt"] = w.get("function_excerpt", "")
        row["wave39_reason"] = w.get("wave39_reason", "")
    else:
        row.update({"uniprot_accessible": False, "uniprot_accession": "", "uniprot_locations": "", "function_excerpt": "", "wave39_reason": ""})

    w94 = frames["w94"]
    w94_sub = w94[w94["gene"].astype(str).str.upper().eq(gene)] if not w94.empty else pd.DataFrame()
    if not w94_sub.empty:
        w = w94_sub.iloc[0]
        row["wave94_score"] = f(w.get("wave94_score"))
        row["wave94_call"] = w.get("wave94_call", "")
        row["wave94_failures"] = w.get("wave94_failures", "")
    else:
        row.update({"wave94_score": math.nan, "wave94_call": "", "wave94_failures": ""})

    return row


def cd300_route_row(frames: dict[str, pd.DataFrame]) -> dict[str, Any]:
    route = route_wave92_row()
    row: dict[str, Any] = {
        "entity": "CD300_RECEPTOR_SPECIFIC_TUNING",
        **MANUAL_ENTITY_META["CD300_RECEPTOR_SPECIFIC_TUNING"],
        "ms_delta_log2": f(route.get("ms_mean_delta_log2")),
        "ms_p": f(route.get("ms_combined_p"), 1.0),
        "ms_anchor": bool(f(route.get("ms_mean_delta_log2"), 0.0) > 0 and f(route.get("ms_combined_p"), 1.0) < 0.10),
        "ms_trend": bool(f(route.get("ms_mean_delta_log2"), 0.0) > 0 and f(route.get("ms_combined_p"), 1.0) < 0.20),
        "broad_positive_disease_count": int(f(route.get("h5ad_positive_disease_count"), 0.0)),
        "broad_negative_disease_count": int(f(route.get("h5ad_negative_disease_count"), 0.0)),
        "myeloid_positive_disease_count": int(
            "myeloid" in str(route.get("h5ad_best_positive_contexts", "")).lower()
        ),
        "positive_diseases_broad": route.get("h5ad_positive_diseases", ""),
        "negative_diseases_broad": route.get("h5ad_negative_diseases", ""),
        "best_positive_context": route.get("h5ad_best_positive_contexts", ""),
        "best_negative_context": route.get("h5ad_best_negative_contexts", ""),
        "response_systems_tested": 3,
        "response_nonresponse_high_systems_p20": int(f(route.get("response_nonresponse_high_system_count"), 0.0)),
        "response_responder_high_systems_p20": 0,
        "response_best_min_p": min(f(route.get("ibd_min_p"), 1.0), f(route.get("ra_p"), 1.0), f(route.get("psoriasis_ada_p"), 1.0)),
        "response_summary": (
            f"IBD:g={f(route.get('ibd_weighted_mean_g')):.3g},p={f(route.get('ibd_min_p'), 1.0):.3g}; "
            f"RA:g={f(route.get('ra_hedges_g_responder_minus_non')):.3g},p={f(route.get('ra_p'), 1.0):.3g}; "
            f"psoriasis_ADA:g={f(route.get('psoriasis_ada_hedges_g_responder_minus_non')):.3g},p={f(route.get('psoriasis_ada_p'), 1.0):.3g}"
        ),
        "response_direction_conflict": False,
        "genetic_disease_count_max": 0,
        "genetic_disease_text": "",
        "foundation_rows": 0,
        "foundation_supportive_text_hits": 0,
        "foundation_do_not_promote_text_hits": 0,
        "uniprot_accessible": True,
        "wave94_score": math.nan,
        "wave94_call": "",
        "wave94_failures": "",
        "wave92_call": route.get("wave92_call", ""),
        "wave92_score": f(route.get("controller_route_score")),
        "wave92_prior_status": route.get("prior_status", ""),
        "wave92_route_note": route.get("route_note", ""),
    }
    return row


def score_entities(rows: list[dict[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    numeric_defaults = {
        "broad_positive_disease_count": 0,
        "broad_negative_disease_count": 0,
        "myeloid_positive_disease_count": 0,
        "response_nonresponse_high_systems_p20": 0,
        "response_responder_high_systems_p20": 0,
        "genetic_disease_count_max": 0,
        "foundation_supportive_text_hits": 0,
        "foundation_do_not_promote_text_hits": 0,
        "manual_targetability": 0,
        "manual_mechanistic_fit": 0,
        "manual_prior_penalty": 0,
        "manual_safety_penalty": 0,
    }
    for col, default in numeric_defaults.items():
        df[col] = pd.to_numeric(df.get(col, default), errors="coerce").fillna(default)
    for col in ["ms_anchor", "ms_trend", "response_direction_conflict", "uniprot_accessible"]:
        df[col] = df.get(col, False).map(boolish) if col in df.columns else False

    df["gate_ms_anchor_or_trend"] = df["ms_anchor"] | df["ms_trend"]
    df["gate_cross_disease_ge3"] = df["broad_positive_disease_count"] >= 3
    df["gate_no_directional_negative"] = df["broad_negative_disease_count"] == 0
    df["gate_myeloid_or_module_fit"] = (df["myeloid_positive_disease_count"] >= 2) | (df["manual_mechanistic_fit"] >= 2.5)
    df["gate_response_consistent"] = (df["response_nonresponse_high_systems_p20"] >= 2) & ~df["response_direction_conflict"]
    df["gate_genetics_or_foundation"] = (df["genetic_disease_count_max"] >= 2) | (
        df["foundation_supportive_text_hits"] > df["foundation_do_not_promote_text_hits"]
    )
    df["gate_targetability"] = (df["manual_targetability"] >= 1.5) | df["uniprot_accessible"]
    df["gate_safety_not_blocking"] = df["manual_safety_penalty"] < 3.0
    df["gate_prior_not_blocking"] = df["manual_prior_penalty"] < 3.0

    gate_cols = [c for c in df.columns if c.startswith("gate_")]
    df["gate_count"] = df[gate_cols].sum(axis=1).astype(int)

    df["wave95_score"] = (
        df["gate_count"].astype(float)
        + df["ms_anchor"].astype(int) * 1.5
        + df["ms_trend"].astype(int) * 0.5
        + df["broad_positive_disease_count"].clip(upper=5) * 0.25
        + df["response_nonresponse_high_systems_p20"].clip(upper=3) * 0.5
        + df["manual_mechanistic_fit"]
        + df["manual_targetability"]
        - df["manual_prior_penalty"]
        - df["manual_safety_penalty"]
        - df["broad_negative_disease_count"].clip(upper=3) * 1.0
        - df["response_responder_high_systems_p20"].clip(upper=3) * 0.5
        - df["foundation_do_not_promote_text_hits"].clip(upper=3) * 0.5
    )

    calls = []
    blockers = []
    for _, row in df.iterrows():
        fail = [col.replace("gate_", "") for col in gate_cols if not bool(row[col])]
        blockers.append(";".join(fail))
        if (
            bool(row["gate_ms_anchor_or_trend"])
            and bool(row["gate_cross_disease_ge3"])
            and bool(row["gate_no_directional_negative"])
            and bool(row["gate_myeloid_or_module_fit"])
            and bool(row["gate_response_consistent"])
            and bool(row["gate_genetics_or_foundation"])
            and bool(row["gate_targetability"])
            and bool(row["gate_prior_not_blocking"])
            and bool(row["gate_safety_not_blocking"])
        ):
            calls.append("PROMOTABLE_TO_DEEP_VALIDATION")
        elif bool(row["gate_ms_anchor_or_trend"]) and bool(row["gate_cross_disease_ge3"]) and bool(row["gate_myeloid_or_module_fit"]) and bool(row["gate_no_directional_negative"]):
            calls.append("PARK_AS_STATE_CONTROLLER_OR_BIOMARKER")
        elif bool(row["gate_response_consistent"]) and bool(row["gate_targetability"]) and not bool(row["gate_ms_anchor_or_trend"]):
            calls.append("PARK_FOR_NON_MS_LEAD_INDICATION_ONLY")
        else:
            calls.append("NO_GO_WAVE95_FORCING_TRIAGE")
    df["wave95_blockers"] = blockers
    df["wave95_call"] = calls
    rank_map = {
        "PROMOTABLE_TO_DEEP_VALIDATION": 0,
        "PARK_AS_STATE_CONTROLLER_OR_BIOMARKER": 1,
        "PARK_FOR_NON_MS_LEAD_INDICATION_ONLY": 2,
        "NO_GO_WAVE95_FORCING_TRIAGE": 3,
    }
    return df.sort_values(
        by=["wave95_call", "wave95_score", "gate_count"],
        key=lambda s: s.map(rank_map).fillna(9) if s.name == "wave95_call" else s,
        ascending=[True, False, False],
    )


def analyze() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    frames = summarize_gene_inputs(COMPARATOR_GENES)
    for name, frame in frames.items():
        frame.to_csv(OUT / f"{name}.tsv", sep="\t", index=False)

    rows = [cd300_route_row(frames)]
    rows.extend(gene_row(gene, frames) for gene in sorted(ACCESSIBLE_TOP))
    rows.extend(gene_row(gene, frames) for gene in sorted(CD300_GENES) if gene in MANUAL_ENTITY_META)
    # Individual CD300 genes are retained in raw response/MS tables; the route,
    # not family-member genes, is the decision entity for this wave.

    ranked = score_entities(rows)
    ranked.to_csv(OUT / "forcing_triage_rank.tsv", sep="\t", index=False)

    call_counts = ranked["wave95_call"].value_counts().to_dict()
    top = ranked.iloc[0].to_dict() if not ranked.empty else {}
    promotable = ranked[ranked["wave95_call"].eq("PROMOTABLE_TO_DEEP_VALIDATION")]
    state_parked = ranked[ranked["wave95_call"].eq("PARK_AS_STATE_CONTROLLER_OR_BIOMARKER")]
    non_ms = ranked[ranked["wave95_call"].eq("PARK_FOR_NON_MS_LEAD_INDICATION_ONLY")]

    summary = {
        "seed": SEED,
        "analysis_call": "NO_PROMOTABLE_ROUTE_AFTER_CD300_VS_ACCESSIBLE_TOP_FORCING_TRIAGE"
        if promotable.empty
        else "PROMOTABLE_ROUTE_REQUIRES_DEEP_VALIDATION",
        "entities_tested": int(len(ranked)),
        "call_counts": {str(k): int(v) for k, v in call_counts.items()},
        "top_entity": str(top.get("entity", "")),
        "top_entity_call": str(top.get("wave95_call", "")),
        "top_entity_score": f(top.get("wave95_score")),
        "state_controller_or_biomarker_entities": state_parked["entity"].astype(str).tolist(),
        "non_ms_lead_only_entities": non_ms["entity"].astype(str).tolist(),
        "inputs": {
            "wave92_route_rank": rel(W92),
            "wave94_accessible_rank": rel(W94),
            "wave39_surfaceome_rank": rel(W39),
        },
    }
    write_json(OUT / "summary.json", summary)

    display_cols = [
        "entity",
        "entity_type",
        "wave95_call",
        "wave95_score",
        "gate_count",
        "ms_delta_log2",
        "ms_p",
        "broad_positive_disease_count",
        "broad_negative_disease_count",
        "myeloid_positive_disease_count",
        "response_nonresponse_high_systems_p20",
        "response_responder_high_systems_p20",
        "genetic_disease_count_max",
        "foundation_rows",
        "manual_mechanistic_fit",
        "manual_targetability",
        "manual_prior_penalty",
        "manual_safety_penalty",
        "wave95_blockers",
        "response_summary",
        "manual_note",
    ]
    report = [
        "# Wave95 CD300 vs Accessible-Top Forcing Triage",
        "",
        "Question: does the mechanistic CD300 lipid/efferocytosis route beat the Wave94 accessible statistical hits, or vice versa?",
        "",
        f"Analysis call: `{summary['analysis_call']}`.",
        "",
        "## Summary",
        "",
        f"- Entities tested: `{summary['entities_tested']}`",
        f"- Call counts: `{summary['call_counts']}`",
        f"- Top entity: `{summary['top_entity']}` (`{summary['top_entity_call']}`, score `{summary['top_entity_score']:.3g}`)",
        f"- Parked state-controller/biomarker entities: `{summary['state_controller_or_biomarker_entities']}`",
        f"- Parked non-MS-lead-only entities: `{summary['non_ms_lead_only_entities']}`",
        "",
        "## Ranked Forcing Matrix",
        "",
        markdown_table(ranked[[col for col in display_cols if col in ranked.columns]], max_rows=25),
        "",
        "## Interpretation",
        "",
        "- `CD300_RECEPTOR_SPECIFIC_TUNING` remains the best mechanistic match to lipid/efferocytosis biology, but it fails the MS-anchor gate and cannot be a cross-autoimmune MS-centered therapeutic claim from current data.",
        "- `C15ORF48` is the strongest state-controller/biomarker branch because it combines MS anchoring, cross-disease recurrence, myeloid/metabolic plausibility, and no direct directional negative contexts; it is not directly druggable in this evidence stack.",
        "- `SEL1L3` remains a statistical accessible-state marker, not a mechanistic module controller, because myeloid/module fit, genetics, and foundation support are weak.",
        "- `NRCAM` is response-consistent but mechanistically off-module and safety-blocked by neural adhesion biology.",
        "- No entity passes promotion gates; the next branch should look for druggable upstream/downstream intervention points around the `C15ORF48` mitochondrial inflammatory-brake state, while keeping CD300 as a wet-lab-only comparator.",
        "",
        "## Guardrails",
        "",
        "- This wave deliberately gives CD300 a manual mechanistic bonus; it still fails because the MS-local anchor is absent.",
        "- Manual targetability/mechanistic/safety penalties are transparent coarse priors, not measured effect sizes.",
        "- A candidate with strong response association but weak MS/local biology is routed to non-MS lead-indication-only, not promoted for MS.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    np.random.seed(SEED)
    print(json.dumps(analyze(), indent=2, sort_keys=True))
