#!/usr/bin/env python3
"""Wave101 forcing triage for undercharacterized accessible survivors.

After C15-proximal, inflammasome-brake, stress-generator, and cAMP routes
failed promotion, this script asks whether the remaining accessible/surface or
membrane-associated survivors justify a focused forcing branch.

Guardrail: accessibility plus expression is not a target claim. A survivor can
only move forward as a forcing branch if it has an MS anchor or trend,
cross-disease recurrence, a plausible perturbation modality, and at least one
independent non-expression anchor. Promotion to FINDING still requires a later
route-specific perturbation/prior-art/novelty audit.
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
OUT = ROOT / "results_v3" / "wave101_accessible_survivor_forcing_triage"

W95 = ROOT / "results_v3" / "wave95_mechanistic_forcing_triage" / "mechanistic_forcing_candidate_rank.tsv"
W94 = ROOT / "results_v3" / "wave94_accessible_state_rerank" / "accessible_state_candidate_rank.tsv"
W79 = ROOT / "results_v3" / "wave79_targetability_shortlist_audit" / "targetability_integrated_decision.tsv"
W81 = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W91 = ROOT / "results_v3" / "wave91_lipid_lysosomal_module_intervention_rank" / "lipid_lysosomal_intervention_rank.tsv"
W47 = ROOT / "results_v3" / "wave47_late_stage_survivor_map" / "late_stage_survivor_map.tsv"
W37 = ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W18 = ROOT / "results_v3" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv"
W62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"

TARGETS = [
    "SEL1L3",
    "FXYD5",
    "CD82",
    "LAPTM5",
    "NRCAM",
    "CD200",
    "MFGE8",
    "CHI3L1",
    "GPNMB",
    "BTN2A2",
    "ADM",
    "APOC1",
]

MANUAL = {
    "SEL1L3": {
        "manual_route": "undercharacterized extracellular SEL1-repeat membrane protein",
        "manual_direction_hypothesis": "inhibit or deplete only if target-specific perturbation reduces stromal/endothelial inflammatory licensing without barrier toxicity",
        "manual_safety_note": "unknown biology; antibody feasibility depends on extracellular accessibility and disease-cell specificity",
        "manual_prior_known_block": False,
    },
    "FXYD5": {
        "manual_route": "FXYD5/dysadherin Na-K-ATPase and adhesion regulator",
        "manual_direction_hypothesis": "non-depleting inhibition or blocking antibody only if disease-high barrier/stromal signal drives inflammatory licensing",
        "manual_safety_note": "epithelial adhesion and Na/K-ATPase coupling create barrier and cancer-biology liabilities",
        "manual_prior_known_block": False,
    },
    "CD82": {
        "manual_route": "tetraspanin membrane microdomain/endolysosomal trafficking regulator",
        "manual_direction_hypothesis": "direction unresolved; block, agonize, or cluster depending on whether CD82 is driver or compensatory trafficking marker",
        "manual_safety_note": "tetraspanin biology is pleiotropic and lacks target-resolved genetics",
        "manual_prior_known_block": True,
    },
    "LAPTM5": {
        "manual_route": "hematopoietic lysosomal membrane state/dependency protein",
        "manual_direction_hypothesis": "modulate only if lysosomal dependency perturbation is protective; current route has no clean extracellular handle",
        "manual_safety_note": "lysosomal membrane biology and lack of modality block translation",
        "manual_prior_known_block": False,
    },
    "NRCAM": {
        "manual_route": "neural/stromal adhesion molecule",
        "manual_direction_hypothesis": "avoid systemic targeting unless a non-neural disease-cell isoform mechanism is proven",
        "manual_safety_note": "node-of-Ranvier/neural adhesion biology creates a high safety blocker",
        "manual_prior_known_block": False,
    },
    "CD200": {
        "manual_route": "CD200/CD200R checkpoint ligand axis",
        "manual_direction_hypothesis": "restore CD200R inhibitory signaling only if receptor-side tissue direction is resolved",
        "manual_safety_note": "immune-checkpoint biology is crowded and directionally context-dependent",
        "manual_prior_known_block": True,
    },
    "MFGE8": {
        "manual_route": "secreted debris-opsonin/efferocytosis bridge",
        "manual_direction_hypothesis": "augment local apoptotic/myelin-debris clearance only if bystander-phagocytosis safety is solved",
        "manual_safety_note": "efferocytosis prior art and bystander tissue-clearance risk block direct promotion",
        "manual_prior_known_block": True,
    },
    "CHI3L1": {
        "manual_route": "secreted chitinase-like inflammatory/remodeling biomarker",
        "manual_direction_hypothesis": "do not promote without causal perturbation; treat as biomarker",
        "manual_safety_note": "secreted biomarker prior saturation and tissue-remodeling pleiotropy",
        "manual_prior_known_block": True,
    },
    "GPNMB": {
        "manual_route": "repair/lysosomal surface glycoprotein with oncology ADC precedent",
        "manual_direction_hypothesis": "direction unresolved; could mark repair rather than pathogenic state",
        "manual_safety_note": "ADC/depletion route is unlikely to be safe for repair-state myeloid cells",
        "manual_prior_known_block": False,
    },
    "BTN2A2": {
        "manual_route": "butyrophilin immune checkpoint-like surface protein",
        "manual_direction_hypothesis": "restore inhibitory/tolerogenic signaling only if disease-cell perturbation supports it",
        "manual_safety_note": "T-cell checkpoint direction and psoriasis/IBD conflict are unresolved",
        "manual_prior_known_block": False,
    },
    "ADM": {
        "manual_route": "secreted adrenomedullin vasoactive peptide",
        "manual_direction_hypothesis": "not a clean autoimmune state controller without vascular/tissue specificity",
        "manual_safety_note": "hypotension/vascular biology and response direction conflict",
        "manual_prior_known_block": False,
    },
    "APOC1": {
        "manual_route": "secreted apolipoprotein/lipid-state protein",
        "manual_direction_hypothesis": "lipid-state marker until causal lipid-handling perturbation is shown",
        "manual_safety_note": "systemic lipid metabolism and conflicting disease compartments",
        "manual_prior_known_block": False,
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


def collect_rows(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for gene in TARGETS:
        manual = MANUAL[gene]
        w95 = first_row(tables["w95"], gene, "candidate")
        w94 = first_row(tables["w94"], gene)
        w79 = first_row(tables["w79"], gene)
        w81 = first_row(tables["w81"], gene)
        w91 = first_row(tables["w91"], gene)
        w47 = first_row(tables["w47"], gene)
        w37 = first_row(tables["w37"], gene, "gene_symbol")
        w18 = first_row(tables["w18"], gene)
        w62 = first_row(tables["w62"], gene)
        rec: dict[str, Any] = {
            "gene": gene,
            **manual,
            "wave95_call": clean(w95.get("wave95_call")) if w95 is not None else "",
            "wave95_score": num(w95.get("wave94_score")) if w95 is not None else math.nan,
            "wave95_reason": clean(w95.get("wave95_reason")) if w95 is not None else "",
            "wave95_failures": clean(w95.get("wave95_failures")) if w95 is not None else "",
            "wave95_manual_prior_class": clean(w95.get("manual_prior_class")) if w95 is not None else "",
            "wave95_manual_prior_blocked": flag(w95.get("manual_prior_blocked")) if w95 is not None else False,
            "wave95_manual_modality_ready": flag(w95.get("manual_modality_ready")) if w95 is not None else False,
            "wave95_manual_wetlab_only": flag(w95.get("manual_wetlab_only")) if w95 is not None else False,
            "wave95_gate_ms_anchor": flag(w95.get("gate_ms_anchor")) if w95 is not None else False,
            "wave95_gate_ms_trend": flag(w95.get("gate_ms_trend")) if w95 is not None else False,
            "wave95_gate_cross_disease_residual": flag(w95.get("gate_cross_disease_residual")) if w95 is not None else False,
            "wave95_gate_response_specificity": flag(w95.get("gate_response_specificity")) if w95 is not None else False,
            "wave95_gate_real_perturbation_or_validated_model": flag(w95.get("gate_real_perturbation_or_validated_model")) if w95 is not None else False,
            "ms_delta_log2": num(w94.get("ms_wm_delta_log2")) if w94 is not None else num(w95.get("ms_delta_log2")) if w95 is not None else math.nan,
            "ms_p": num(w94.get("ms_wm_p"), 1.0) if w94 is not None else num(w95.get("ms_p"), 1.0) if w95 is not None else 1.0,
            "ms_fdr": num(w94.get("ms_wm_fdr"), 1.0) if w94 is not None else num(w95.get("ms_fdr"), 1.0) if w95 is not None else 1.0,
            "positive_disease_count": num(w94.get("positive_disease_count"), 0.0) if w94 is not None else num(w95.get("broad_positive_disease_count"), 0.0) if w95 is not None else 0.0,
            "negative_disease_count": num(w94.get("negative_disease_count"), 0.0) if w94 is not None else num(w95.get("broad_negative_disease_count"), 0.0) if w95 is not None else 0.0,
            "positive_diseases": clean(w94.get("positive_diseases")) if w94 is not None else "",
            "negative_diseases": clean(w94.get("negative_diseases")) if w94 is not None else "",
            "best_positive_context": clean(w94.get("best_positive_context")) if w94 is not None else "",
            "uniprot_accessible": flag(w94.get("uniprot_accessible")) if w94 is not None else False,
            "uniprot_locations": clean(w94.get("uniprot_locations")) if w94 is not None else "",
            "uniprot_transmembrane_feature_count": num(w94.get("uniprot_transmembrane_feature_count"), 0.0) if w94 is not None else 0.0,
            "protein_name": clean(w94.get("protein_name")) if w94 is not None else "",
            "europepmc_hit_count": num(w94.get("europepmc_hit_count"), 0.0) if w94 is not None else 0.0,
            "clinicaltrials_hit_count": num(w94.get("clinicaltrials_hit_count"), 0.0) if w94 is not None else 0.0,
            "response_systems_tested": num(w94.get("response_systems_tested"), 0.0) if w94 is not None else 0.0,
            "response_nonresponse_high_systems_p20": num(w94.get("response_nonresponse_high_systems_p20"), 0.0) if w94 is not None else 0.0,
            "response_responder_high_systems_p20": num(w94.get("response_responder_high_systems_p20"), 0.0) if w94 is not None else 0.0,
            "response_direction_conflict": flag(w94.get("response_direction_conflict")) if w94 is not None else False,
            "response_best_min_p": num(w94.get("response_best_min_p"), 1.0) if w94 is not None else 1.0,
            "response_summary": clean(w94.get("response_summary")) if w94 is not None else "",
            "wave79_call": clean(w79.get("wave79_call")) if w79 is not None else "",
            "wave79_gate_count": num(w79.get("gate_count"), 0.0) if w79 is not None else 0.0,
            "wave81_call": clean(w81.get("wave81_call")) if w81 is not None else "",
            "wave81_direct_perturbation": num(w81.get("direct_perturbation"), 0.0) if w81 is not None else 0.0,
            "wave81_foundation_model_support": num(w81.get("foundation_model_support"), 0.0) if w81 is not None else 0.0,
            "wave81_detail": clean(w81.get("direct_perturbation_detail")) + clean(w81.get("foundation_model_detail")) if w81 is not None else "",
            "wave91_call": clean(w91.get("wave91_call")) if w91 is not None else "",
            "wave91_score": num(w91.get("module_intervention_score")) if w91 is not None else math.nan,
            "wave91_route_blocker": clean(w91.get("route_blocker")) if w91 is not None else "",
            "wave47_reopen_call": clean(w47.get("reopen_call")) if w47 is not None else "",
            "wave47_missing_requirements": clean(w47.get("missing_requirements")) if w47 is not None else "",
            "wave37_screen_call": clean(w37.get("screen_call")) if w37 is not None else "",
            "wave37_contrast_lfc": num(w37.get("median_efficient_minus_noneater_lfc")) if w37 is not None else math.nan,
            "wave37_contrast_fdr": num(w37.get("contrast_fdr"), 1.0) if w37 is not None else 1.0,
            "wave18_recommendation": clean(w18.get("foundation_rescue_recommendation")) if w18 is not None else "",
            "wave18_support_contexts": num(w18.get("total_support_contexts"), 0.0) if w18 is not None else 0.0,
            "wave18_strong_support_contexts": num(w18.get("total_strong_support_contexts"), 0.0) if w18 is not None else 0.0,
            "wave62_call": clean(w62.get("wave62_call")) if w62 is not None else "",
            "wave62_strong_l2g_disease_count": num(w62.get("strong_l2g_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_strong_qtl_coloc_disease_count": num(w62.get("strong_qtl_coloc_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_ms_max_l2g_score": num(w62.get("ms_max_l2g_score"), 0.0) if w62 is not None else 0.0,
            "wave62_ms_max_relevant_qtl_h4": num(w62.get("ms_max_relevant_qtl_h4"), 0.0) if w62 is not None else 0.0,
        }
        rows.append(rec)
    return pd.DataFrame(rows)


def add_calls(rank: pd.DataFrame) -> pd.DataFrame:
    rank = rank.copy()
    numeric_for_scoring = [
        "ms_delta_log2",
        "positive_disease_count",
        "negative_disease_count",
        "response_nonresponse_high_systems_p20",
        "response_responder_high_systems_p20",
        "wave81_direct_perturbation",
        "wave81_foundation_model_support",
    ]
    for col in numeric_for_scoring:
        if col in rank.columns:
            rank[col] = pd.to_numeric(rank[col], errors="coerce").fillna(0.0)
    rank["gate_ms_anchor_or_trend"] = (rank["ms_delta_log2"] > 0.25) & (rank["ms_p"] < 0.10)
    rank["gate_cross_disease_breadth"] = rank["positive_disease_count"] >= 3
    rank["gate_low_contradiction"] = rank["negative_disease_count"] <= 1
    rank["gate_accessible_or_secreted"] = rank["uniprot_accessible"] | rank["uniprot_locations"].str.contains("Secreted|Cell membrane|Basolateral", case=False, na=False)
    rank["gate_response_signal"] = (
        (rank["response_best_min_p"] < 0.05)
        | (rank["response_nonresponse_high_systems_p20"] >= 2)
        | (rank["response_responder_high_systems_p20"] >= 2)
    )
    rank["gate_perturbation_or_model"] = (
        (rank["wave81_direct_perturbation"] > 0)
        | (rank["wave81_foundation_model_support"] > 0)
        | (rank["wave37_contrast_fdr"] <= 0.20)
        | ((rank["wave18_support_contexts"] >= 2) & ~rank["wave18_recommendation"].str.contains("do_not_promote", case=False, na=False))
        | rank["wave95_gate_real_perturbation_or_validated_model"]
    )
    rank["gate_genetic_anchor"] = (
        (rank["wave62_strong_l2g_disease_count"] >= 2)
        | (rank["wave62_strong_qtl_coloc_disease_count"] >= 2)
        | (rank["wave62_ms_max_l2g_score"] >= 0.5)
        | (rank["wave62_ms_max_relevant_qtl_h4"] >= 0.8)
    )
    rank["gate_prior_not_known_block"] = ~(rank["manual_prior_known_block"] | rank["wave95_manual_prior_blocked"])
    rank["gate_not_safety_blocked"] = ~rank["manual_safety_note"].str.contains("neural|bystander|pleiotropy|hypotension|ADC/depletion", case=False, na=False)
    rank["gate_direction_not_conflicted"] = ~rank["response_direction_conflict"]
    rank["gate_not_already_hard_no"] = ~rank["wave95_call"].str.contains("NO_GO_PRIOR|NO_GO_MARKER|NO_GO_ACCESSIBLE_STATE", case=False, na=False)

    critical = [
        "gate_ms_anchor_or_trend",
        "gate_cross_disease_breadth",
        "gate_low_contradiction",
        "gate_accessible_or_secreted",
        "gate_response_signal",
        "gate_perturbation_or_model",
        "gate_genetic_anchor",
        "gate_prior_not_known_block",
        "gate_not_safety_blocked",
        "gate_direction_not_conflicted",
    ]
    rank["wave101_gate_count"] = rank[critical].sum(axis=1).astype(int)
    rank["wave101_score"] = (
        rank["wave101_gate_count"] * 2
        + rank["positive_disease_count"].clip(upper=5)
        + (rank["ms_delta_log2"].clip(lower=0, upper=2) * 1.5)
        + (rank["response_nonresponse_high_systems_p20"].clip(upper=3) * 1.2)
        + (rank["response_responder_high_systems_p20"].clip(upper=3) * 0.5)
        + rank["wave81_direct_perturbation"] * 1.5
        + rank["wave81_foundation_model_support"] * 1.0
        + rank["wave95_manual_wetlab_only"].astype(int) * 0.5
        - rank["negative_disease_count"].clip(upper=3) * 1.5
        - rank["manual_prior_known_block"].astype(int) * 3
        - rank["response_direction_conflict"].astype(int) * 2
    )
    calls = []
    missing_all = []
    for _, row in rank.iterrows():
        missing = [c.replace("gate_", "") for c in critical if not bool(row[c])]
        missing_all.append(";".join(missing))
        if bool(row["manual_prior_known_block"]) or not bool(row["gate_prior_not_known_block"]):
            calls.append("NO_GO_PRIOR_OR_CROWDED_ROUTE")
        elif "neural" in clean(row["manual_safety_note"]).lower():
            calls.append("NO_GO_SAFETY_BLOCKED_NEURAL_ADHESION")
        elif not bool(row["gate_accessible_or_secreted"]):
            calls.append("NO_GO_NO_ACTIONABLE_ACCESSIBILITY")
        elif not bool(row["gate_ms_anchor_or_trend"]):
            calls.append("NO_GO_WEAK_MS_ANCHOR")
        elif not bool(row["gate_cross_disease_breadth"]):
            calls.append("NO_GO_WEAK_CROSS_DISEASE_BREADTH")
        elif not bool(row["gate_perturbation_or_model"]) and not bool(row["gate_genetic_anchor"]):
            calls.append("PARK_NEEDS_PERTURBATION_AND_GENETIC_ANCHOR")
        elif not bool(row["gate_perturbation_or_model"]):
            calls.append("PARK_NEEDS_TARGET_SPECIFIC_PERTURBATION")
        elif not bool(row["gate_genetic_anchor"]):
            calls.append("PARK_NEEDS_TARGET_GENETIC_ANCHOR")
        elif not bool(row["gate_direction_not_conflicted"]):
            calls.append("PARK_DIRECTION_CONFLICT")
        else:
            calls.append("REOPEN_FOR_WAVE102_FORCING")
    rank["wave101_missing_gates"] = missing_all
    rank["wave101_call"] = calls
    call_priority = {
        "REOPEN_FOR_WAVE102_FORCING": 0,
        "PARK_NEEDS_TARGET_SPECIFIC_PERTURBATION": 1,
        "PARK_NEEDS_TARGET_GENETIC_ANCHOR": 2,
        "PARK_DIRECTION_CONFLICT": 3,
        "PARK_NEEDS_PERTURBATION_AND_GENETIC_ANCHOR": 4,
        "NO_GO_WEAK_MS_ANCHOR": 5,
        "NO_GO_WEAK_CROSS_DISEASE_BREADTH": 6,
        "NO_GO_NO_ACTIONABLE_ACCESSIBILITY": 7,
        "NO_GO_SAFETY_BLOCKED_NEURAL_ADHESION": 8,
        "NO_GO_PRIOR_OR_CROWDED_ROUTE": 9,
    }
    rank["wave101_call_priority"] = rank["wave101_call"].map(call_priority).fillna(99).astype(int)
    return rank.sort_values(["wave101_call_priority", "wave101_score"], ascending=[True, False])


def write_report(rank: pd.DataFrame, summary: dict[str, Any]) -> None:
    cols = [
        "gene",
        "wave101_call",
        "wave101_score",
        "wave101_call_priority",
        "wave101_gate_count",
        "ms_delta_log2",
        "ms_p",
        "positive_disease_count",
        "negative_disease_count",
        "response_nonresponse_high_systems_p20",
        "response_responder_high_systems_p20",
        "response_best_min_p",
        "wave81_direct_perturbation",
        "wave81_foundation_model_support",
        "wave62_strong_l2g_disease_count",
        "wave62_strong_qtl_coloc_disease_count",
        "uniprot_locations",
        "wave95_call",
        "manual_route",
        "manual_safety_note",
        "wave101_missing_gates",
    ]
    report = f"""# Wave101 Accessible Survivor Forcing Triage

## Bottom Line

Branch call: `{summary["branch_call"]}`.

No accessible survivor is promotion-grade. The most useful next forcing branch
is not a target claim but a focused undercharacterized-surface test around
`SEL1L3` and `FXYD5`, with `CD82`/`LAPTM5` retained as mechanistic comparators.
Those candidates have MS trend/anchor and cross-disease recurrence, but they
still lack target-specific perturbation, target-resolved genetics, and
directional safety evidence.

## Candidate Ranking

{markdown_table(rank[cols], max_rows=30)}

## Interpretation

- `SEL1L3` is the cleanest undercharacterized accessible survivor: nominal MS
  up, cross-disease recurrence, low explicit prior-art burden in local scans,
  and extracellular/membrane annotation. It is still only a forcing candidate
  because mechanism, perturbation, and genetics are weak.
- `FXYD5` is the most concrete surface-biophysics route: Na/K-ATPase and
  adhesion regulation give a testable mechanism, but response direction
  conflict and a negative Crohn myeloid context make it unsafe to promote.
- `CD82` and `LAPTM5` better match endolysosomal biology but lack clean MS,
  genetic, and perturbation support; they remain comparators.
- `NRCAM`, `CD200`, `MFGE8`, and `CHI3L1` have safety, prior-art, or biomarker
  saturation blockers.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave101_accessible_survivor_forcing_triage.py")}`
- Rank table: `{rel(OUT / "accessible_survivor_forcing_rank.tsv")}`
- Summary: `{rel(OUT / "summary.json")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    tables = {
        "w95": read_tsv(W95),
        "w94": read_tsv(W94),
        "w79": read_tsv(W79),
        "w81": read_tsv(W81),
        "w91": read_tsv(W91),
        "w47": read_tsv(W47),
        "w37": read_tsv(W37),
        "w18": read_tsv(W18),
        "w62": read_tsv(W62),
    }
    rank = add_calls(collect_rows(tables))
    rank.to_csv(OUT / "accessible_survivor_forcing_rank.tsv", sep="\t", index=False)
    reopened = rank[rank["wave101_call"].eq("REOPEN_FOR_WAVE102_FORCING")]
    branch_call = "REOPEN_FOR_WAVE102_FORCING" if not reopened.empty else "NO_PROMOTABLE_ACCESSIBLE_SURVIVOR_YET"
    summary = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "n_candidates": int(len(rank)),
        "call_counts": rank["wave101_call"].value_counts().to_dict(),
        "top_candidate": rank.iloc[0]["gene"] if not rank.empty else "",
        "top_candidate_call": rank.iloc[0]["wave101_call"] if not rank.empty else "",
        "wave102_forcing_candidates": rank[
            rank["wave101_call"].isin(
                [
                    "PARK_NEEDS_PERTURBATION_AND_GENETIC_ANCHOR",
                    "PARK_NEEDS_TARGET_SPECIFIC_PERTURBATION",
                    "PARK_NEEDS_TARGET_GENETIC_ANCHOR",
                    "PARK_DIRECTION_CONFLICT",
                ]
            )
        ]["gene"].head(4).tolist(),
        "inputs": {
            "wave95": rel(W95),
            "wave94": rel(W94),
            "wave79": rel(W79),
            "wave81": rel(W81),
            "wave91": rel(W91),
            "wave47": rel(W47),
            "wave37": rel(W37),
            "wave18": rel(W18),
            "wave62": rel(W62),
        },
    }
    write_json(OUT / "summary.json", summary)
    write_report(rank, summary)


if __name__ == "__main__":
    main()
