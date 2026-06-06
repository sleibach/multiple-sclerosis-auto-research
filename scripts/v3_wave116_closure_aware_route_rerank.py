#!/usr/bin/env python3
"""Wave116 closure-aware route rerank after local branch closures."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave116_closure_aware_route_rerank"
W110 = ROOT / "phases/v3/results" / "wave110_post_closure_intervention_route_map" / "post_closure_route_map.tsv"
W95 = ROOT / "phases/v3/results" / "wave95_mechanistic_forcing_triage" / "mechanistic_forcing_candidate_rank.tsv"
W83 = ROOT / "phases/v3/results" / "wave83_intervention_class_meta_rank" / "intervention_class_meta_rank.tsv"
W91 = ROOT / "phases/v3/results" / "wave91_lipid_lysosomal_module_intervention_rank" / "lipid_lysosomal_intervention_rank.tsv"

CLOSED_TERMS = {
    "PSAP": "wave113_no_recurrence",
    "GPR183": "wave112_no_compartment_coherence",
    "EBI2": "wave112_no_compartment_coherence",
    "P2RX7": "wave114_no_target_specificity",
    "CD82": "wave107_niche_biomarker_only",
    "MFGE8": "wave108_109_no_strict_safety_window",
    "SPNS1": "wave115_no_controller_route",
    "CD58": "prior_art_direction_conflict",
    "SEL1L3": "wave102_no_target_specific_evidence",
    "FXYD5": "wave102_no_target_specific_evidence",
    "P4HB": "generic_er_pdi_toxicity",
    "NAMPT": "prior_art_blocked",
    "IL1B": "prior_art_crowded",
    "LAMP3": "marker_no_intervention",
    "FABP5": "wave92_prior_art_or_weak_route",
    "DAB2": "wave118_directionality_modality_failed",
    "CD9": "wave118_directionality_modality_failed",
    "PARK7": "wave117_generic_stress_route_failed",
    "BLK": "prefilter_no_ms_no_response_no_crispr_fdr",
    "LRRC61": "prefilter_no_ms_no_genetics_no_modality_two_guides",
    "CLEC7A": "wave119_remaining_wave110_prefilter_failed",
    "FAM49B": "wave119_remaining_wave110_prefilter_failed",
    "LYN": "wave119_remaining_wave110_prefilter_failed",
    "CCDC121": "wave119_remaining_wave110_prefilter_failed",
    "CHST11": "wave119_remaining_wave110_prefilter_failed",
    "FBXO16": "wave119_remaining_wave110_prefilter_failed",
    "RECQL4": "wave119_remaining_wave110_prefilter_failed",
    "EFR3A": "wave119_remaining_wave110_prefilter_failed",
    "IGLON5": "wave119_remaining_wave110_prefilter_failed",
    "MAN1A2": "wave119_remaining_wave110_prefilter_failed",
    "MREG": "wave119_remaining_wave110_prefilter_failed",
    "PLIN4": "wave119_remaining_wave110_prefilter_failed",
    "SLC39A3": "wave119_remaining_wave110_prefilter_failed",
    "YWHAE": "wave119_remaining_wave110_prefilter_failed",
    "EPHX2": "wave120_no_target_pd_coherence",
    "ABTB2": "wave116_selected_but_no_concrete_test_no_ms_no_fdr",
    "CD44": "adhesion_matrix_prior_art_and_broad_biology",
    "SPP1": "osteopontin_cd44_prior_art_and_broad_biology",
    "HLA-DPA1": "broad_mhc_class_ii_host_defense_no_selective_route",
    "HLA-DPB1": "broad_mhc_class_ii_host_defense_no_selective_route",
    "HLA-DRA": "broad_mhc_class_ii_host_defense_no_selective_route",
    "FPR2": "wave121_wetlab_only_route_closed",
    "ANXA1": "wave121_wetlab_only_route_closed",
    "FPR2_ANXA1_BIASED_RESOLUTION": "wave121_wetlab_only_route_closed",
    "CD300": "wave121_wetlab_only_route_closed",
    "CD300_RECEPTOR_SPECIFIC_TUNING": "wave121_wetlab_only_route_closed",
}


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def closure_reason(text: str) -> str:
    hits = []
    upper = str(text).upper()
    for term, reason in CLOSED_TERMS.items():
        if term in upper:
            hits.append(f"{term}:{reason}")
    return ";".join(hits)


def boolish(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []

    w110 = read_tsv(W110)
    if not w110.empty:
        for _, r in w110.iterrows():
            candidate = str(r.get("candidate", ""))
            rows.append(
                {
                    "candidate": candidate,
                    "source": "wave110",
                    "mechanism": r.get("mechanism", ""),
                    "modality": r.get("modality", ""),
                    "source_call": r.get("source_call", ""),
                    "base_score": float(r.get("escape_score", 0) or 0),
                    "support_summary": r.get("support_summary", ""),
                    "recommended_next_test": r.get("recommended_next_test", ""),
                    "has_concrete_next_test": boolish(r.get("has_concrete_next_test", False)),
                }
            )

    w95 = read_tsv(W95)
    if not w95.empty:
        for _, r in w95.iterrows():
            candidate = str(r.get("candidate", ""))
            rows.append(
                {
                    "candidate": candidate,
                    "source": "wave95",
                    "mechanism": r.get("route_class", ""),
                    "modality": r.get("manual_prior_class", ""),
                    "source_call": r.get("wave95_call", ""),
                    "base_score": float(r.get("support_gate_count", 0) or 0) - float(r.get("critical_gate_count", 0) or 0),
                    "support_summary": r.get("response_summary", ""),
                    "recommended_next_test": r.get("wave95_reason", ""),
                    "has_concrete_next_test": True,
                }
            )

    w83 = read_tsv(W83)
    if not w83.empty:
        for _, r in w83.iterrows():
            candidate = str(r.get("candidate", ""))
            rows.append(
                {
                    "candidate": candidate,
                    "source": "wave83",
                    "mechanism": r.get("mechanism", ""),
                    "modality": r.get("modality", ""),
                    "source_call": r.get("wave83_call", ""),
                    "base_score": float(r.get("interestingness_score", 0) or 0),
                    "support_summary": r.get("source_value", ""),
                    "recommended_next_test": r.get("primary_blocker", ""),
                    "has_concrete_next_test": True,
                }
            )

    w91 = read_tsv(W91)
    if not w91.empty:
        for _, r in w91.iterrows():
            candidate = str(r.get("candidate", r.get("gene", "")))
            rows.append(
                {
                    "candidate": candidate,
                    "source": "wave91",
                    "mechanism": r.get("modules", r.get("mechanism", r.get("route", ""))),
                    "modality": r.get("chembl_target_id", r.get("modality", "")),
                    "source_call": r.get("wave91_call", r.get("call", r.get("decision", ""))),
                    "base_score": float(
                        r.get("module_intervention_score", r.get("score", r.get("rank_score", 0))) or 0
                    ),
                    "support_summary": (
                        f"ibd={r.get('ibd_call', '')}; ra={r.get('ra_call', '')}; "
                        f"ms={r.get('ms_wm_call', '')}; wave62={r.get('wave62_call', '')}"
                    ),
                    "recommended_next_test": r.get("route_blocker", r.get("recommended_next_test", "")),
                    "has_concrete_next_test": True,
                }
            )

    universe = pd.DataFrame(rows).drop_duplicates(subset=["candidate", "source"])
    if universe.empty:
        universe = pd.DataFrame(columns=["candidate", "source", "base_score"])
    universe["closure_reason"] = universe.apply(
        lambda r: closure_reason(" ".join(str(r.get(c, "")) for c in ["candidate", "mechanism", "modality", "source_call"])),
        axis=1,
    )
    universe["closed_or_blocked"] = universe["closure_reason"].ne("")
    universe["no_go_source"] = (
        universe["source_call"].astype(str).str.contains("NO_GO|BLOCKED|NOT_V3", case=False, na=False)
        | universe["recommended_next_test"].astype(str).str.contains("NO_GO|BLOCKED|NOT_V3|UNSPECIFIED", case=False, na=False)
    )
    universe["concrete_bonus"] = universe["has_concrete_next_test"].map(lambda x: 0.5 if x else -1.0)
    universe["closure_penalty"] = universe["closed_or_blocked"].map(lambda x: -5.0 if x else 0.0)
    universe["no_go_penalty"] = universe["no_go_source"].map(lambda x: -2.0 if x else 0.0)
    universe["rerank_score"] = universe["base_score"] + universe["concrete_bonus"] + universe["closure_penalty"] + universe["no_go_penalty"]
    universe = universe.sort_values(["closed_or_blocked", "rerank_score"], ascending=[True, False])
    universe.to_csv(OUT / "closure_aware_route_universe.tsv", sep="\t", index=False)

    open_routes = universe[~universe["closed_or_blocked"]].copy()
    actionable_routes = open_routes[
        (~open_routes["no_go_source"]) & (open_routes["has_concrete_next_test"])
    ].copy()
    top_open = open_routes.head(20)
    selected = actionable_routes.iloc[0].to_dict() if not actionable_routes.empty else {}
    branch_call = "ROUTE_AVAILABLE_FOR_FORCING_TEST" if selected else "NO_OPEN_ROUTE_AFTER_CLOSURE_RERANK"
    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "branch_call": branch_call,
            "n_routes": int(len(universe)),
            "n_open_routes": int(len(open_routes)),
            "n_actionable_routes": int(len(actionable_routes)),
            "selected_candidate": selected.get("candidate", ""),
            "selected_source": selected.get("source", ""),
            "selected_score": selected.get("rerank_score", None),
            "inputs": {
                "wave110": rel(W110),
                "wave95": rel(W95),
                "wave83": rel(W83),
                "wave91": rel(W91),
            },
        },
    )

    report = f"""# Wave116 Closure-Aware Route Rerank

## Bottom Line

Branch call: `{branch_call}`.

Selected next route: `{selected.get("candidate", "")}` from `{selected.get("source", "")}`.

## Top Open Routes

{markdown_table(top_open, max_rows=20)}

## Top Actionable Routes

{markdown_table(actionable_routes.head(20), max_rows=20)}

## Top Closed / Blocked Routes

{markdown_table(universe[universe["closed_or_blocked"]].head(20), max_rows=20)}

## Interpretation

This rerank is not biological evidence. It is orchestration hygiene after many
local closures. Any selected route must still pass a new forcing test with
direct perturbation, disease anchoring, and prior-art checks.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave116_closure_aware_route_rerank.py")}`
- Output: `{rel(OUT / "closure_aware_route_universe.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
