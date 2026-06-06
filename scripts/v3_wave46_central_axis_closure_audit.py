#!/usr/bin/env python3
"""Wave46 closure audit for the original central IFN/HLA-II/lysosomal axes.

This is not a discovery script. It consolidates the already executed V3 tests
that repeatedly returned to the same five central axes, so the orchestrator can
avoid re-opening IFI30/CTSS/CD74/CIITA/IFNGR variants without new evidence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave46_central_axis_closure_audit"
SEED = 20260527

CENTRAL = ROOT / "phases/v3/results" / "central_and_intervention_candidate_rank.tsv"
MODEL = ROOT / "phases/v3/results" / "mechanistic_model" / "ifng_apc_feedback_intervention_effects.tsv"
MODEL_SUMMARY = ROOT / "phases/v3/results" / "mechanistic_model" / "ifng_apc_feedback_summary.json"
TARGET_GENETICS = ROOT / "phases/v3/results" / "wave14_target_level_genetics" / "target_level_genetics_truth_table.tsv"
WAVE15_LOADER = ROOT / "phases/v3/results" / "wave15_loader_external_gate" / "loader_external_gate_summary.tsv"
WAVE19_LOCAL = ROOT / "phases/v3/results" / "wave19_lysosomal_controller" / "candidate_local_evidence.tsv"
WAVE19_ROUTES = ROOT / "phases/v3/results" / "wave19_lysosomal_controller" / "route_summary.tsv"
WAVE31 = ROOT / "phases/v3/results" / "wave31_dynamic_transition_controller_audit" / "dynamic_transition_controller_audit.tsv"
WAVE34 = ROOT / "phases/v3/results" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv"
WAVE43 = ROOT / "phases/v3/results" / "wave43_genetic_druggable_failfast" / "genetic_druggable_failfast.tsv"
WAVE45 = ROOT / "phases/v3/results" / "wave45_regulatory_controller_audit" / "regulatory_controller_audit.tsv"


AXIS_RULES = {
    "IFNGR_JAK_STAT1_upstream_control": {
        "intervention_point": "IFNGR/JAK/STAT1 pathway suppression",
        "model_intervention": "ifngr_jak_70pct_suppression",
        "central_conclusion": "central_but_not_novel_or_selective",
        "primary_blocker": "Upstream control is quantitatively real but collapses into broad JAK/IFN immunosuppression and prior-arted approved-class biology.",
        "final_call": "NO_GO_GENERIC_IFN_JAK_CONTROL",
        "supporting_prior_waves": "mechanistic_model;Wave31;Wave43;Wave45",
    },
    "CD74_HLAII_receptor_APC_state_biomarker": {
        "intervention_point": "CD74/HLA-II/APC-state receptor and biomarker axis",
        "model_intervention": "",
        "central_conclusion": "state_biomarker_not_intervention",
        "primary_blocker": "Cell-state signal is strong, but CD74/HLA-II is better as a stratification readout than a selective therapeutic handle; direct CD74/MIF and HLA-II targeting are prior-arted and biologically broad.",
        "final_call": "NO_GO_BIOMARKER_NOT_TARGET",
        "supporting_prior_waves": "Wave14 target genetics;Wave31;prior-art gates",
    },
    "CIITA_RFX5_HLAII_transcriptional_gate": {
        "intervention_point": "CIITA/RFX5/NLRC5 HLA-II transcriptional gate",
        "model_intervention": "",
        "central_conclusion": "mechanistically_narrow_but_undruggable",
        "primary_blocker": "Perturbation can narrow HLA-II output, but the practical targets are transcription-factor/enhanceosome machinery without a current selective clinical modality or target-level genetics.",
        "final_call": "NO_GO_HLAII_TF_GATE_UNDRUGGABLE",
        "supporting_prior_waves": "Wave14 target genetics;Wave31;Wave45",
    },
    "IFI30_GILT_lysosomal_feedback_effector": {
        "intervention_point": "IFI30/GILT lysosomal thiol-reductase modulation",
        "model_intervention": "ifi30_95pct_suppression",
        "central_conclusion": "downstream_effector_not_transition_controller",
        "primary_blocker": "Even extreme modeled IFI30 suppression mostly changes the GILT/lysosomal readout and fails to shut down the upstream IFN/APC or HLA-II/CD74 transition; chemical matter is immature and prior art already covers broad IFI30/GILT autoimmunity.",
        "final_call": "NO_GO_IFI30_DOWNSTREAM_AND_UNTRACTABLE",
        "supporting_prior_waves": "mechanistic_model;Wave15 loader external gate;Wave19;Wave21",
    },
    "CTSS_cathepsinS_lysosomal_effector": {
        "intervention_point": "CTSS/cathepsin-S antigen-processing inhibition",
        "model_intervention": "ctss_70pct_suppression",
        "central_conclusion": "druggable_comparator_but_blocked",
        "primary_blocker": "CTSS is druggable and mechanistically adjacent, but modeled downstream suppression does not control the transition and autoimmune cathepsin-S inhibitor prior art/clinical history undercuts novelty and feasibility.",
        "final_call": "NO_GO_CTSS_PRIOR_ART_DOWNSTREAM_EFFECTOR",
        "supporting_prior_waves": "mechanistic_model;Wave15 loader external gate;Wave19;Wave21",
    },
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def safe_float(value: Any) -> float | None:
    if value is None or pd.isna(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def first_row_by_value(df: pd.DataFrame, column: str, value: str) -> dict[str, Any]:
    if df.empty or column not in df.columns:
        return {}
    sub = df[df[column].astype(str).eq(value)]
    if sub.empty:
        return {}
    return sub.iloc[0].to_dict()


def rows_for_genes(df: pd.DataFrame, genes: list[str], column: str = "gene") -> pd.DataFrame:
    if df.empty or column not in df.columns:
        return pd.DataFrame()
    return df[df[column].astype(str).isin(genes)].copy()


def summarize_target_genetics(df: pd.DataFrame, genes: list[str]) -> tuple[str, str, float]:
    rows = rows_for_genes(df, genes)
    if rows.empty:
        return "not_available_in_wave14_truth_table", "", 0.0
    calls = sorted(set(rows.get("target_level_genetics_dod_call", pd.Series(dtype=str)).dropna().astype(str)))
    blockers = sorted(set(rows.get("coloc_mr_blocker", pd.Series(dtype=str)).dropna().astype(str)))
    max_diseases = safe_float(rows.get("ot_n_diseases_score_ge_0_5", pd.Series([0])).max()) or 0.0
    return ";".join(calls), " | ".join(blockers[:3]), max_diseases


def summarize_wave34(df: pd.DataFrame, genes: list[str]) -> dict[str, Any]:
    rows = rows_for_genes(df, genes)
    if rows.empty:
        return {
            "wave34_calls": "",
            "wave34_max_score": None,
            "wave34_max_gwas_trait_count": None,
            "wave34_max_local_positive_diseases": None,
            "wave34_any_ms_anchor": False,
        }
    return {
        "wave34_calls": ";".join(sorted(set(rows["wave34_call"].dropna().astype(str)))) if "wave34_call" in rows.columns else "",
        "wave34_max_score": safe_float(rows["wave34_score"].max()) if "wave34_score" in rows.columns else None,
        "wave34_max_gwas_trait_count": safe_float(rows["gwas_catalog_trait_count"].max()) if "gwas_catalog_trait_count" in rows.columns else None,
        "wave34_max_local_positive_diseases": safe_float(rows["local_positive_disease_count"].max()) if "local_positive_disease_count" in rows.columns else None,
        "wave34_any_ms_anchor": bool(rows.get("ms_anchor", pd.Series(dtype=bool)).fillna(False).astype(bool).any()),
    }


def summarize_lysosomal_local(df: pd.DataFrame, genes: list[str]) -> dict[str, Any]:
    rows = rows_for_genes(df, genes)
    if rows.empty:
        return {
            "wave19_genes_seen": "",
            "wave19_go_scout_genes": "",
            "wave19_state_supported_genes": "",
            "wave19_max_score": None,
        }
    return {
        "wave19_genes_seen": ";".join(rows["gene"].astype(str)),
        "wave19_go_scout_genes": ";".join(rows.loc[rows.get("local_gate_call", pd.Series(dtype=str)).astype(str).eq("GO_SCOUT"), "gene"].astype(str))
        if "local_gate_call" in rows.columns
        else "",
        "wave19_state_supported_genes": ";".join(rows.loc[rows.get("state_coupling_call", pd.Series(dtype=str)).astype(str).str.contains("state_supported", na=False), "gene"].astype(str))
        if "state_coupling_call" in rows.columns
        else "",
        "wave19_max_score": safe_float(rows["route_priority_score"].max()) if "route_priority_score" in rows.columns else None,
    }


def summarize_loader_gate(df: pd.DataFrame, genes: list[str]) -> dict[str, Any]:
    rows = rows_for_genes(df, genes)
    if rows.empty:
        return {"loader_ot_n_diseases_ge_0_5": None, "loader_trials_max": None, "loader_europepmc_max": None}
    return {
        "loader_ot_n_diseases_ge_0_5": safe_float(rows["ot_n_diseases_score_ge_0_5"].max()) if "ot_n_diseases_score_ge_0_5" in rows.columns else None,
        "loader_trials_max": safe_float(rows["clinical_trials_hit_count"].max()) if "clinical_trials_hit_count" in rows.columns else None,
        "loader_europepmc_max": safe_float(rows["europepmc_total_hits_across_queries"].max()) if "europepmc_total_hits_across_queries" in rows.columns else None,
    }


def summarize_model(model: pd.DataFrame, intervention: str) -> dict[str, Any]:
    if model.empty or not intervention:
        return {
            "model_intervention": intervention,
            "model_min_ifn_apc_log2fc": None,
            "model_min_hla_cd74_log2fc": None,
            "model_min_gilt_log2fc": None,
            "model_interpretation": "not_directly_modeled",
        }
    rows = model[model["intervention"].astype(str).eq(intervention)]
    if rows.empty:
        return {
            "model_intervention": intervention,
            "model_min_ifn_apc_log2fc": None,
            "model_min_hla_cd74_log2fc": None,
            "model_min_gilt_log2fc": None,
            "model_interpretation": "intervention_not_found",
        }
    min_ifn = safe_float(rows["ifn_apc_readout_log2fc_vs_control"].min())
    min_hla = safe_float(rows["hla_ii_cd74_readout_log2fc_vs_control"].min())
    min_gilt = safe_float(rows["gilt_lysosomal_readout_log2fc_vs_control"].min())
    if intervention.startswith("ifngr"):
        interp = "upstream_suppression_reduces_all_three_readouts_but_is_generic"
    elif intervention.startswith("ifi30"):
        interp = "extreme_IFI30_suppression_is_mostly_lysosomal_and_weak_on_IFN_HLA_state"
    elif intervention.startswith("ctss"):
        interp = "CTSS_suppression_is_lysosomal_only_with_no_IFN_HLA_state_control"
    else:
        interp = "modeled"
    return {
        "model_intervention": intervention,
        "model_min_ifn_apc_log2fc": min_ifn,
        "model_min_hla_cd74_log2fc": min_hla,
        "model_min_gilt_log2fc": min_gilt,
        "model_interpretation": interp,
    }


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        vals = []
        for col in cols:
            val = "" if pd.isna(row[col]) else str(row[col])
            vals.append(val.replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    central = read_tsv(CENTRAL)
    model = read_tsv(MODEL)
    target_genetics = read_tsv(TARGET_GENETICS)
    loader = read_tsv(WAVE15_LOADER)
    wave19_local = read_tsv(WAVE19_LOCAL)
    wave19_routes = read_tsv(WAVE19_ROUTES)
    wave31 = read_tsv(WAVE31)
    wave34 = read_tsv(WAVE34)
    wave43 = read_tsv(WAVE43)
    wave45 = read_tsv(WAVE45)

    rows = []
    for _, central_row in central.iterrows():
        candidate = str(central_row["candidate"])
        rule = AXIS_RULES[candidate]
        genes = [g.strip() for g in str(central_row["genes"]).split(",") if g.strip()]
        genetics_call, genetics_blocker, max_ot_diseases = summarize_target_genetics(target_genetics, genes)
        model_stats = summarize_model(model, rule["model_intervention"])
        w34 = summarize_wave34(wave34, genes)
        lys = summarize_lysosomal_local(wave19_local, genes)
        load = summarize_loader_gate(loader, genes)

        wave31_rows = wave31[wave31["candidate"].astype(str).isin(genes)] if not wave31.empty and "candidate" in wave31.columns else pd.DataFrame()
        wave45_rows = wave45[wave45["candidate"].astype(str).isin(genes)] if not wave45.empty and "candidate" in wave45.columns else pd.DataFrame()
        wave43_rows = wave43[wave43["gene"].astype(str).isin(genes)] if not wave43.empty and "gene" in wave43.columns else pd.DataFrame()

        rows.append(
            {
                "candidate": candidate,
                "genes": ",".join(genes),
                "centrality_score": central_row.get("centrality_score"),
                "intervention_score": central_row.get("intervention_score"),
                "prior_art_penalty": central_row.get("prior_art_penalty"),
                "intervention_point": rule["intervention_point"],
                "central_conclusion": rule["central_conclusion"],
                "final_call": rule["final_call"],
                "promotion_allowed": False,
                "primary_blocker": rule["primary_blocker"],
                "target_level_genetics_call": genetics_call,
                "target_level_genetics_max_ot_diseases_ge_0_5": max_ot_diseases,
                "target_level_genetics_blocker": genetics_blocker,
                "wave34_calls": w34["wave34_calls"],
                "wave34_max_gwas_trait_count": w34["wave34_max_gwas_trait_count"],
                "wave34_max_local_positive_diseases": w34["wave34_max_local_positive_diseases"],
                "wave34_any_ms_anchor": w34["wave34_any_ms_anchor"],
                "wave19_go_scout_genes": lys["wave19_go_scout_genes"],
                "wave19_state_supported_genes": lys["wave19_state_supported_genes"],
                "loader_ot_n_diseases_ge_0_5": load["loader_ot_n_diseases_ge_0_5"],
                "loader_trials_max": load["loader_trials_max"],
                "loader_europepmc_max": load["loader_europepmc_max"],
                "wave31_calls": ";".join(sorted(set(wave31_rows["wave31_call"].dropna().astype(str)))) if not wave31_rows.empty and "wave31_call" in wave31_rows.columns else "",
                "wave43_calls": ";".join(sorted(set(wave43_rows["call"].dropna().astype(str)))) if not wave43_rows.empty and "call" in wave43_rows.columns else "",
                "wave45_calls": ";".join(sorted(set(wave45_rows["call"].dropna().astype(str)))) if not wave45_rows.empty and "call" in wave45_rows.columns else "",
                **model_stats,
                "supporting_prior_waves": rule["supporting_prior_waves"],
            }
        )

    audit = pd.DataFrame(rows)
    audit.to_csv(OUT / "central_axis_closure_audit.tsv", sep="\t", index=False)

    gate_rows = []
    dod_gates = [
        "specific_cross_autoimmune_mechanism",
        "breadth_coverage_and_cell_state",
        "cross_disease_genetic_anchoring",
        "foundation_or_real_perturbation",
        "intervention_druggability_selectivity",
        "verified_novelty_or_prior_art",
        "therapeutic_feasibility",
    ]
    for _, row in audit.iterrows():
        for gate in dod_gates:
            status = "fail"
            reason = row["primary_blocker"]
            if gate == "specific_cross_autoimmune_mechanism":
                status = "pass_mechanistic_axis"
                reason = "The axis is biologically coherent and central enough to audit."
            elif gate == "breadth_coverage_and_cell_state":
                status = "partial"
                reason = "Cell-state evidence exists for the module, but target-specific disease breadth is inconsistent or confounded."
            elif gate == "cross_disease_genetic_anchoring":
                reason = str(row["target_level_genetics_blocker"] or "No target-resolved coloc/MR package across four diseases.")
            elif gate == "foundation_or_real_perturbation":
                reason = str(row["model_interpretation"])
            elif gate == "intervention_druggability_selectivity":
                reason = str(row["primary_blocker"])
            elif gate == "verified_novelty_or_prior_art":
                reason = "Prior V3 novelty/prior-art gates blocked this route or reduced it to comparator/biomarker status."
            elif gate == "therapeutic_feasibility":
                reason = str(row["primary_blocker"])
            gate_rows.append({"candidate": row["candidate"], "dod_gate": gate, "status": status, "reason": reason})
    gate_matrix = pd.DataFrame(gate_rows)
    gate_matrix.to_csv(OUT / "central_axis_dod_gate_matrix.tsv", sep="\t", index=False)

    route_summary = wave19_routes[wave19_routes.get("route", pd.Series(dtype=str)).astype(str).eq("cathepsin_IFI30_local_controls")].copy() if not wave19_routes.empty else pd.DataFrame()
    route_summary.to_csv(OUT / "wave19_cathepsin_ifi30_route_context.tsv", sep="\t", index=False)

    model_summary = {}
    if MODEL_SUMMARY.exists():
        model_summary = json.loads(MODEL_SUMMARY.read_text(encoding="utf-8"))

    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "n_axes": int(len(audit)),
        "promoted_count": int(audit["promotion_allowed"].sum()),
        "final_call_counts": audit["final_call"].value_counts().to_dict(),
        "interpretation": (
            "The original central IFN/HLA-II/lysosomal antigen-processing axes remain biologically central but none is "
            "a promotable V3 therapeutic finding. Upstream IFN/JAK control is too generic/prior-arted; CD74/HLA-II is a "
            "biomarker state; CIITA/RFX5 is undruggable transcriptional machinery; IFI30 and CTSS are downstream lysosomal "
            "effectors whose modeled perturbation does not control the upstream transition, with IFI30 lacking mature "
            "chemical matter and CTSS blocked by prior art."
        ),
        "model_summary_interpretation": model_summary.get("interpretation", ""),
        "inputs": [
            rel(p)
            for p in [
                CENTRAL,
                MODEL,
                MODEL_SUMMARY,
                TARGET_GENETICS,
                WAVE15_LOADER,
                WAVE19_LOCAL,
                WAVE19_ROUTES,
                WAVE31,
                WAVE34,
                WAVE43,
                WAVE45,
            ]
            if p.exists()
        ],
        "outputs": {
            "audit": rel(OUT / "central_axis_closure_audit.tsv"),
            "gate_matrix": rel(OUT / "central_axis_dod_gate_matrix.tsv"),
            "route_context": rel(OUT / "wave19_cathepsin_ifi30_route_context.tsv"),
            "report": rel(OUT / "REPORT.md"),
        },
    }
    write_json(OUT / "summary.json", summary)

    report_cols = [
        "candidate",
        "final_call",
        "central_conclusion",
        "target_level_genetics_call",
        "model_intervention",
        "model_min_ifn_apc_log2fc",
        "model_min_hla_cd74_log2fc",
        "model_min_gilt_log2fc",
        "primary_blocker",
    ]
    report = [
        "# Wave46 Central Axis Closure Audit",
        "",
        "## Result",
        "",
        summary["interpretation"],
        "",
        "## Axis Calls",
        "",
        markdown_table(audit[report_cols]),
        "",
        "## DoD Gate Matrix",
        "",
        markdown_table(gate_matrix),
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
