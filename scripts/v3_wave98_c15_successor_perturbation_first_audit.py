#!/usr/bin/env python3
"""Wave98 perturbation-first audit for novelty-open C15 successor candidates.

Wave97 closed the direct C15ORF48-state branch as a therapeutic nomination.
The only remaining novelty-open candidates were LITAF, PLEK2, CASP4, and
PIK3R2. This wave applies a perturbation-first standard to those four.

Key rule: residual C15 co-state and remission associations are not perturbation.
They can justify a wet-lab ordering experiment, but they cannot promote a
therapeutic target without real or model-validated perturbation direction.
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
OUT = ROOT / "phases/v3/results" / "wave98_c15_successor_perturbation_first_audit"

W96 = ROOT / "phases/v3/results" / "wave96_c15orf48_controller_search" / "c15orf48_controller_candidate_rank.tsv"
W97 = ROOT / "phases/v3/results" / "wave97_c15_residual_costate_falsification" / "residual_costate_candidate_summary.tsv"
W97_CTX = ROOT / "phases/v3/results" / "wave97_c15_residual_costate_falsification" / "residual_costate_context_tests.tsv"
W68 = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
W68_OLS = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "adjusted_top_gene_ols.tsv"
W37 = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W37_GUIDE = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "guide_level_lfc.tsv"
W18 = ROOT / "phases/v3/results" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv"
W18_SRC = ROOT / "phases/v3/results" / "wave18_foundation_rescue" / "geneformer_source_gene_summary.tsv"
W39 = ROOT / "phases/v3/results" / "wave39_surfaceome_rescue_after_resolution_pivot" / "surfaceome_rescue_rank_full.tsv"
W55 = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W62 = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W81 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"

CANDIDATES = ["LITAF", "PLEK2", "CASP4", "PIK3R2"]

MANUAL_CLASS = {
    "LITAF": {
        "mechanistic_direction": "upstream_inflammatory_stress_generator",
        "intervention_direction": "reduce LITAF/TNF/endolysosomal stress if perturbation ordering confirms C15 induction is secondary",
        "modality_class": "no selective direct modality",
        "prior_status": "novelty_open_but_generic_tnf_lps_prior",
        "safety_note": "loss-of-function disease/neuropathy and broad TNF/endosomal biology make direct systemic targeting unsafe without cell-selective delivery",
        "manual_prior_blocked": False,
        "manual_modality_ready": False,
    },
    "PLEK2": {
        "mechanistic_direction": "cytoskeletal_state_marker_until_proven_controller",
        "intervention_direction": "unknown; perturbation ordering required before any target logic",
        "modality_class": "no selective direct modality",
        "prior_status": "autoimmune_novelty_open",
        "safety_note": "hematopoietic/cytoskeletal biology; no selective autoimmune pharmacology",
        "manual_prior_blocked": False,
        "manual_modality_ready": False,
    },
    "CASP4": {
        "mechanistic_direction": "upstream_pyroptosis_danger_stress_generator",
        "intervention_direction": "selective CASP4 inhibition only if separable from CASP1/CASP5 and host-defense pyroptosis",
        "modality_class": "enzymatic but selectivity/host-defense risk",
        "prior_status": "close_eae_caspase_and_inhibitor_prior",
        "safety_note": "noncanonical inflammasome and antimicrobial host-defense liability; close CASP11/EAE prior art",
        "manual_prior_blocked": True,
        "manual_modality_ready": True,
    },
    "PIK3R2": {
        "mechanistic_direction": "generic_pi3k_autophagy_adjacency",
        "intervention_direction": "not target-specific; pan-PI3K or catalytic-subunit modulation is broad",
        "modality_class": "PI3K-family chemistry exists but PIK3R2-specific selectivity is not established",
        "prior_status": "pi3k_autoimmune_field_saturated",
        "safety_note": "broad PI3K immune/metabolic toxicity and no MS anchor",
        "manual_prior_blocked": False,
        "manual_modality_ready": False,
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
    # Use the same contrast sign as the gene-level screen: efficient minus non-eater.
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


def build_rows(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for gene in CANDIDATES:
        manual = MANUAL_CLASS[gene]
        w96 = first_row(tables["w96"], gene)
        w97 = first_row(tables["w97"], gene)
        w68 = best_w68(tables["w68"], gene)
        w37 = first_row(tables["w37"], gene, col="gene_symbol")
        w18 = first_row(tables["w18"], gene)
        w18_src = first_row(tables["w18_src"], gene)
        w39 = first_row(tables["w39"], gene)
        w55 = first_row(tables["w55"], gene)
        w62 = first_row(tables["w62"], gene)
        w81 = first_row(tables["w81"], gene)
        rec: dict[str, Any] = {
            "gene": gene,
            **manual,
            "wave96_score": num(w96.get("wave96_score")) if w96 is not None else math.nan,
            "wave96_call": clean(w96.get("wave96_call")) if w96 is not None else "",
            "c15_trend_positive_context_count": num(w96.get("c15_trend_positive_context_count"), 0.0) if w96 is not None else 0.0,
            "c15_trend_positive_disease_count": num(w96.get("c15_trend_positive_disease_count"), 0.0) if w96 is not None else 0.0,
            "c15_state_pearson_r": num(w96.get("c15_state_pearson_r")) if w96 is not None else math.nan,
            "ms_delta_log2": num(w96.get("ms_delta_log2")) if w96 is not None else math.nan,
            "ms_p": num(w96.get("ms_p"), 1.0) if w96 is not None else 1.0,
            "ms_fdr": num(w96.get("ms_fdr"), 1.0) if w96 is not None else 1.0,
            "residual_case_positive_context_count": num(w97.get("residual_case_positive_context_count"), 0.0) if w97 is not None else 0.0,
            "residual_case_positive_disease_count": num(w97.get("residual_case_positive_disease_count"), 0.0) if w97 is not None else 0.0,
            "median_residual_case_r": num(w97.get("median_residual_case_r")) if w97 is not None else math.nan,
            "residual_survival_fraction": num(w97.get("residual_survival_fraction"), 0.0) if w97 is not None else 0.0,
            "wave68_best_cell_state": clean(w68.get("cell_state")) if w68 is not None else "",
            "wave68_remission_adjusted_delta": num(w68.get("remission_adjusted_delta")) if w68 is not None else math.nan,
            "wave68_remission_adjusted_p": num(w68.get("remission_adjusted_p"), 1.0) if w68 is not None else 1.0,
            "wave68_remission_adjusted_fdr": num(w68.get("remission_adjusted_fdr"), 1.0) if w68 is not None else 1.0,
            "wave37_screen_call": clean(w37.get("screen_call")) if w37 is not None else "",
            "wave37_contrast_lfc": num(w37.get("median_efficient_minus_noneater_lfc")) if w37 is not None else math.nan,
            "wave37_contrast_fdr": num(w37.get("contrast_fdr"), 1.0) if w37 is not None else 1.0,
            "wave18_recommendation": clean(w18.get("foundation_rescue_recommendation")) if w18 is not None else "",
            "wave18_support_contexts": num(w18.get("total_support_contexts"), 0.0) if w18 is not None else 0.0,
            "wave18_strong_support_contexts": num(w18.get("total_strong_support_contexts"), 0.0) if w18 is not None else 0.0,
            "wave18_source_contexts": num(w18_src.get("support_contexts"), 0.0) if w18_src is not None else 0.0,
            "wave18_source_strong_contexts": num(w18_src.get("strong_support_contexts"), 0.0) if w18_src is not None else 0.0,
            "wave39_call": clean(w39.get("wave39_call")) if w39 is not None else "",
            "chembl_activity_count": num(w39.get("chembl_activity_count"), 0.0) if w39 is not None else 0.0,
            "uniprot_accessible": clean(w39.get("uniprot_accessible")) if w39 is not None else "",
            "uniprot_function_excerpt": clean(w39.get("function_excerpt")) if w39 is not None else "",
            "wave55_n_genetic_diseases_ge_0_25": num(w55.get("n_diseases_genetic_ge_0_25"), 0.0) if w55 is not None else 0.0,
            "wave55_genetic_diseases_ge_0_25": clean(w55.get("diseases_genetic_ge_0_25")) if w55 is not None else "",
            "wave62_call": clean(w62.get("wave62_call")) if w62 is not None else "",
            "wave62_strong_l2g_disease_count": num(w62.get("strong_l2g_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_strong_qtl_coloc_disease_count": num(w62.get("strong_qtl_coloc_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_ms_max_l2g_score": num(w62.get("ms_max_l2g_score"), 0.0) if w62 is not None else 0.0,
            "wave62_ms_max_relevant_qtl_h4": num(w62.get("ms_max_relevant_qtl_h4"), 0.0) if w62 is not None else 0.0,
            "wave81_call": clean(w81.get("wave81_call")) if w81 is not None else "",
            "wave81_direct_perturbation": num(w81.get("direct_perturbation"), 0.0) if w81 is not None else 0.0,
            "wave81_foundation_model_support": num(w81.get("foundation_model_support"), 0.0) if w81 is not None else 0.0,
            "wave81_decision_reason": clean(w81.get("decision_reason")) if w81 is not None else "",
        }
        rec.update(guide_consistency(tables["w37_guide"], gene))
        rows.append(rec)
    return pd.DataFrame(rows)


def add_gates(rank: pd.DataFrame) -> pd.DataFrame:
    rank["gate_residual_c15_survives"] = rank["residual_case_positive_disease_count"] >= 2
    rank["gate_ms_strict"] = (rank["ms_delta_log2"] > 0.25) & (rank["ms_p"] < 0.05)
    rank["gate_ms_trend"] = (rank["ms_delta_log2"] > 0.25) & (rank["ms_p"] < 0.10)
    rank["gate_response_beneficial_for_inhibition"] = (
        (rank["wave68_remission_adjusted_delta"] <= -0.30)
        & (rank["wave68_remission_adjusted_fdr"] <= 0.10)
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
    # Manual modality-ready means a candidate has a plausible direct target
    # class after selectivity/safety audit, not just UniProt accessibility.
    rank["gate_modality_selective"] = rank["manual_modality_ready"].astype(bool)
    rank["gate_prior_not_blocking"] = ~rank["manual_prior_blocked"].astype(bool)
    rank["critical_gate_count"] = (
        rank["gate_residual_c15_survives"].astype(int)
        + rank["gate_ms_strict"].astype(int)
        + rank["gate_real_perturbation_direction"].astype(int)
        + rank["gate_modality_selective"].astype(int)
        + rank["gate_prior_not_blocking"].astype(int)
    )
    rank["support_gate_count"] = (
        rank["gate_response_beneficial_for_inhibition"].astype(int)
        + rank["gate_model_perturbation_direction"].astype(int)
        + rank["gate_genetics"].astype(int)
        + rank["gate_ms_genetics"].astype(int)
        + rank["gate_ms_trend"].astype(int)
    )
    rank["wave98_score"] = (
        2.0 * rank["gate_residual_c15_survives"].astype(int)
        + 2.5 * rank["gate_ms_strict"].astype(int)
        + 1.0 * rank["gate_ms_trend"].astype(int)
        + 2.0 * rank["gate_response_beneficial_for_inhibition"].astype(int)
        + 3.0 * rank["gate_real_perturbation_direction"].astype(int)
        + 2.0 * rank["gate_model_perturbation_direction"].astype(int)
        + 2.0 * rank["gate_genetics"].astype(int)
        + 1.5 * rank["gate_modality_selective"].astype(int)
        + 1.0 * rank["gate_prior_not_blocking"].astype(int)
        + rank["residual_case_positive_disease_count"].clip(upper=3)
        + rank["c15_state_pearson_r"].fillna(0).clip(lower=0)
    )
    calls = []
    reasons = []
    for rec in rank.to_dict("records"):
        failed = [
            gate
            for gate in [
                "gate_residual_c15_survives",
                "gate_ms_strict",
                "gate_real_perturbation_direction",
                "gate_modality_selective",
                "gate_prior_not_blocking",
                "gate_response_beneficial_for_inhibition",
                "gate_model_perturbation_direction",
                "gate_genetics",
            ]
            if not bool(rec.get(gate, False))
        ]
        if rec["critical_gate_count"] >= 5 and rec["support_gate_count"] >= 2:
            call = "REOPEN_C15_SUCCESSOR_TARGET"
            reason = "residual C15 state, MS anchor, perturbation direction, modality, and prior gates pass"
        elif not rec["gate_prior_not_blocking"]:
            call = "NO_GO_CLOSE_PRIOR_OR_SAFETY_BLOCKED"
            reason = "close prior-art/safety gate blocks therapeutic promotion"
        elif rec["gate_residual_c15_survives"] and rec["gate_response_beneficial_for_inhibition"]:
            call = "PARK_PERTURBATION_ORDERING_REQUIRED"
            reason = "residual C15 co-state plus remission direction survive, but real perturbation or modality is missing"
        elif rec["gate_ms_strict"] and rec["gate_residual_c15_survives"]:
            call = "PARK_MARKER_NEEDS_PERTURBATION_AND_MODALITY"
            reason = "MS expression and residual C15 co-state survive, but perturbation and modality gates fail"
        else:
            call = "NO_GO_C15_SUCCESSOR_PERTURBATION_FIRST"
            reason = "successor candidate lacks required MS/residual/perturbation/modality convergence"
        calls.append(call)
        reasons.append(reason + "; failed=" + ";".join(failed))
    rank["wave98_call"] = calls
    rank["wave98_reason"] = reasons
    priority = {
        "REOPEN_C15_SUCCESSOR_TARGET": 0,
        "PARK_PERTURBATION_ORDERING_REQUIRED": 1,
        "PARK_MARKER_NEEDS_PERTURBATION_AND_MODALITY": 2,
        "NO_GO_CLOSE_PRIOR_OR_SAFETY_BLOCKED": 3,
        "NO_GO_C15_SUCCESSOR_PERTURBATION_FIRST": 4,
    }
    rank["call_priority"] = rank["wave98_call"].map(priority).fillna(9).astype(int)
    return rank.sort_values(["call_priority", "wave98_score"], ascending=[True, False]).drop(columns=["call_priority"])


def report_table(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "gene",
        "wave98_call",
        "wave98_score",
        "critical_gate_count",
        "support_gate_count",
        "mechanistic_direction",
        "residual_case_positive_disease_count",
        "median_residual_case_r",
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
        "prior_status",
        "wave98_reason",
    ]
    return df[[c for c in cols if c in df.columns]].copy()


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    tables = {
        "w96": read_tsv(W96),
        "w97": read_tsv(W97),
        "w97_ctx": read_tsv(W97_CTX),
        "w68": read_tsv(W68),
        "w68_ols": read_tsv(W68_OLS),
        "w37": read_tsv(W37),
        "w37_guide": read_tsv(W37_GUIDE),
        "w18": read_tsv(W18),
        "w18_src": read_tsv(W18_SRC),
        "w39": read_tsv(W39),
        "w55": read_tsv(W55),
        "w62": read_tsv(W62),
        "w81": read_tsv(W81),
    }
    for key, df in tables.items():
        for col in ["gene", "candidate", "gene_symbol"]:
            if not df.empty and col in df.columns:
                df[col] = df[col].astype(str).str.upper()

    rank = add_gates(build_rows(tables))
    rank.to_csv(OUT / "c15_successor_perturbation_first_rank.tsv", sep="\t", index=False)
    tables["w97_ctx"][tables["w97_ctx"]["gene"].astype(str).str.upper().isin(CANDIDATES)].to_csv(
        OUT / "c15_successor_residual_context_tests.tsv", sep="\t", index=False
    )
    summary = {
        "seed": SEED,
        "analysis_call": "NO_REOPEN_C15_SUCCESSOR_TARGET",
        "candidates": CANDIDATES,
        "call_counts": rank["wave98_call"].value_counts().to_dict(),
        "top_call": clean(rank.iloc[0]["wave98_call"]) if not rank.empty else "",
        "top_gene": clean(rank.iloc[0]["gene"]) if not rank.empty else "",
        "inputs": {
            "wave96": rel(W96),
            "wave97": rel(W97),
            "wave68": rel(W68),
            "wave37": rel(W37),
            "wave18": rel(W18),
            "wave39": rel(W39),
            "wave55": rel(W55),
            "wave62": rel(W62),
            "wave81": rel(W81),
        },
    }
    write_json(OUT / "summary.json", summary)

    report = [
        "# Wave98 C15 Successor Perturbation-First Audit",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Question",
        "",
        "Can any novelty-open C15ORF48-state successor candidate be reopened after",
        "requiring perturbation-direction evidence rather than residual co-state",
        "alone?",
        "",
        "## Verdict",
        "",
        "`NO_REOPEN_C15_SUCCESSOR_TARGET`",
        "",
        "## Call Counts",
        "",
        markdown_table(pd.DataFrame([{"wave98_call": k, "n": v} for k, v in summary["call_counts"].items()])),
        "",
        "## Candidate Matrix",
        "",
        markdown_table(report_table(rank), max_rows=20),
        "",
        "## Interpretation",
        "",
        "`LITAF` is the strongest wet-lab ordering hypothesis because residual",
        "C15 co-state and remission-direction support survive, but it lacks a",
        "validated perturbation edge and a selective modality. `CASP4` has similar",
        "biology but is close-prior/safety blocked. `PLEK2` is MS-anchored but",
        "still marker-like. `PIK3R2` is broad PI3K adjacency without MS or C15",
        "specificity. None is a therapeutic nomination.",
        "",
        "## Output Files",
        "",
        f"- `{rel(OUT / 'c15_successor_perturbation_first_rank.tsv')}`",
        f"- `{rel(OUT / 'c15_successor_residual_context_tests.tsv')}`",
        f"- `{rel(OUT / 'summary.json')}`",
        f"- `{rel(OUT / 'REPORT.md')}`",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
