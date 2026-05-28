#!/usr/bin/env python3
"""Wave63 transition-controller integrator.

This branch asks whether Wave62 target-resolved genetics can be converted into
an intervention-grade state-transition controller. It intentionally treats
prior waves as guardrails: a candidate is not promoted unless target
resolution, cross-disease state evidence, perturbation/foundation support,
druggability, and blocker status all agree.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave63_transition_controller_integrator"
SEED = 20260527

INPUTS = {
    "wave62": ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv",
    "broad": ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "residual": ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
    "wave31": ROOT / "results_v3" / "wave31_dynamic_transition_controller_audit" / "dynamic_transition_controller_audit.tsv",
    "wave34": ROOT / "results_v3" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv",
    "wave34a": ROOT / "results_v3" / "wave34a_genetics_first_target_rescue" / "genetics_first_candidate_rank.tsv",
    "wave45": ROOT / "results_v3" / "wave45_regulatory_controller_audit" / "regulatory_controller_audit.tsv",
    "wave55": ROOT / "results_v3" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv",
    "wave57": ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_intervention_first_candidate_calls.tsv",
    "wave59": ROOT / "results_v3" / "wave59_lysosomal_sphingolipid_model_reopener_audit" / "lysosomal_sphingolipid_evidence.tsv",
    "wave59_decision": ROOT / "results_v3" / "wave59_lysosomal_sphingolipid_model_reopener_audit" / "lysosomal_sphingolipid_decision.tsv",
    "wave61": ROOT / "results_v3" / "wave61_perturbation_first_guardrail" / "intervention_evidence_tiers.tsv",
}

BENCHMARK_GENES = [
    "BACH2",
    "IRF5",
    "IFI30",
    "SP140",
    "IL7R",
    "STAT4",
    "CD40",
    "IL12A",
]

ROUTE_CANDIDATES = [
    {
        "candidate": "SP140_TOP1_TOP2_RESCUE",
        "gene": "SP140",
        "intervention_node": "TOP1_TOP2",
        "reason": "Wave62 SP140 genetics plus published Crohn SP140-loss topoisomerase rescue route; tested here as transferability hypothesis only.",
        "manual_blocker": "topoisomerase_cytotoxicity_and_Crohn_genotype_specificity",
    },
    {
        "candidate": "BACH2_TOLERANCE_RESTORATION",
        "gene": "BACH2",
        "intervention_node": "BACH2",
        "reason": "Strong broad genetics benchmark; restoration route has no selective modality.",
        "manual_blocker": "tolerance_TF_restoration_not_druggable",
    },
    {
        "candidate": "IRF5_MYEL0ID_INHIBITION",
        "gene": "IRF5",
        "intervention_node": "IRF5",
        "reason": "Strong broad genetics benchmark; inhibited myeloid TF route is prior-art/crowded.",
        "manual_blocker": "IRF5_TF_prior_art_and_druggability",
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def f(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def s(value: Any) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return str(value)


def first_gene(df: pd.DataFrame, gene: str) -> dict[str, Any]:
    if df.empty or "gene" not in df.columns:
        return {}
    sub = df[df["gene"].astype(str).str.upper() == gene.upper()]
    if sub.empty:
        return {}
    return sub.iloc[0].to_dict()


def best_wave61(df: pd.DataFrame, gene: str) -> dict[str, Any]:
    if df.empty or "gene" not in df.columns:
        return {}
    sub = df[df["gene"].astype(str).str.upper() == gene.upper()].copy()
    if sub.empty:
        return {}
    for col in ["gate_count", "selectivity_score", "target_suppression", "direct_priority_score"]:
        if col in sub.columns:
            sub[col] = pd.to_numeric(sub[col], errors="coerce")
    sort_cols = [c for c in ["gate_count", "selectivity_score", "target_suppression", "direct_priority_score"] if c in sub.columns]
    if sort_cols:
        sub = sub.sort_values(sort_cols, ascending=[False] * len(sort_cols))
    return sub.iloc[0].to_dict()


def first_candidate(df: pd.DataFrame, candidate: str) -> dict[str, Any]:
    if df.empty or "candidate" not in df.columns:
        return {}
    sub = df[df["candidate"].astype(str).str.upper() == candidate.upper()]
    if sub.empty:
        return {}
    return sub.iloc[0].to_dict()


def route_gene(candidate: str) -> str:
    if candidate == "CDK8_CDK19_MEDIATOR_KINASE":
        return "CDK8"
    if candidate in {"MED16", "GSK3B", "LRRK2", "CTSB", "CXCR2"}:
        return candidate
    return candidate.split("_")[0]


def build_universe(dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, str]] = []
    wave62 = dfs["wave62"]
    if not wave62.empty:
        parked = wave62[wave62["wave62_call"].astype(str).str.startswith("PARK")]
        for gene in parked["gene"].dropna().astype(str).unique():
            rows.append({"candidate": gene, "gene": gene, "intervention_node": gene, "reason": "wave62_parked_target_resolution"})
    for gene in BENCHMARK_GENES:
        rows.append({"candidate": gene, "gene": gene, "intervention_node": gene, "reason": "wave62v_benchmark_or_module_control"})
    wave57 = dfs["wave57"]
    if not wave57.empty and "wave57_call" in wave57.columns:
        for gene in wave57[wave57["wave57_call"].astype(str).str.contains("REOPEN|PROMOTE", na=False)]["gene"].dropna().astype(str).unique():
            rows.append({"candidate": gene, "gene": gene, "intervention_node": gene, "reason": "foundation_model_reopener"})
    wave31 = dfs["wave31"]
    if not wave31.empty and "candidate" in wave31.columns:
        for candidate in wave31["candidate"].dropna().astype(str).unique():
            rows.append({"candidate": candidate, "gene": route_gene(candidate), "intervention_node": candidate, "reason": "prior_transition_controller_audit"})
    for route in ROUTE_CANDIDATES:
        rows.append(route)
    out = pd.DataFrame(rows).drop_duplicates(["candidate", "gene", "intervention_node"]).reset_index(drop=True)
    return out


def collect_candidate(row: pd.Series, dfs: dict[str, pd.DataFrame]) -> dict[str, Any]:
    candidate = s(row["candidate"])
    gene = s(row["gene"])
    intervention = s(row["intervention_node"])

    w62 = first_gene(dfs["wave62"], gene)
    broad = first_gene(dfs["broad"], gene)
    residual = first_gene(dfs["residual"], gene)
    w34 = first_gene(dfs["wave34"], gene)
    w34a = first_gene(dfs["wave34a"], gene)
    w55 = first_gene(dfs["wave55"], gene)
    w57 = first_gene(dfs["wave57"], gene)
    w59 = first_gene(dfs["wave59"], gene)
    w61 = best_wave61(dfs["wave61"], gene)

    w31 = {}
    if not dfs["wave31"].empty and "candidate" in dfs["wave31"].columns:
        sub = dfs["wave31"][dfs["wave31"]["candidate"].astype(str).str.upper() == candidate.upper()]
        if not sub.empty:
            w31 = sub.iloc[0].to_dict()
    w45 = first_candidate(dfs["wave45"], candidate)
    if not w45:
        w45 = first_candidate(dfs["wave45"], gene)
    w59_decision = first_gene(dfs["wave59_decision"], gene)

    manual_blockers = [
        s(row.get("manual_blocker", "")),
        s(w62.get("manual_blocker", "")),
        s(w62.get("prior_context_blocker", "")),
        s(w31.get("manual_blocker", "")),
        s(w45.get("manual_blocker", "")),
        s(w45.get("call", "")) if "NO_GO" in s(w45.get("call", "")) else "",
        s(w34a.get("wave34a_call", "")) if "DEMOTE" in s(w34a.get("wave34a_call", "")) else "",
        s(w59.get("manual_directionality_risk", "")),
        s(w59_decision.get("call", "")) if "NO_GO" in s(w59_decision.get("call", "")) else "",
        s(w59_decision.get("failed_gates", "")),
        s(w61.get("manual_blocker", "")),
        s(w61.get("wave61_call", "")) if "NO_GO" in s(w61.get("wave61_call", "")) else "",
    ]
    manual_blocker = ";".join([x for x in manual_blockers if x])

    ms_l2g = f(w62.get("ms_max_l2g_score"))
    ms_qtl = f(w62.get("ms_max_relevant_qtl_h4"))
    strong_l2g_n = f(w62.get("strong_l2g_disease_count"))
    relevant_qtl_n = f(w62.get("relevant_qtl_coloc_disease_count"))
    wave55_genetic_n = f(w55.get("n_diseases_genetic_ge_0_25"))
    local_pos = max(f(w62.get("local_positive_disease_count")), f(broad.get("positive_disease_count")), f(w55.get("local_positive_disease_count")))
    local_neg = max(f(w62.get("local_negative_disease_count")), f(broad.get("negative_disease_count")), f(w55.get("local_negative_disease_count")))
    residual_n = max(f(w62.get("residual_retained_disease_count")), f(residual.get("retained_positive_disease_count")), f(w55.get("strict_residual_disease_count")))
    strict_resid_n = max(
        f(w62.get("strict_core_covariate_surviving_disease_count")),
        f(residual.get("strict_core_covariate_surviving_disease_count")),
    )
    ms_p = min(
        f(w62.get("ms_wm_p"), 1.0),
        f(broad.get("ms_wm_p"), 1.0),
        f(w55.get("ms_wm_p"), 1.0),
        f(w34.get("ms_wm_p"), 1.0),
    )
    ms_fdr = min(
        f(w62.get("ms_wm_fdr"), 1.0),
        f(broad.get("ms_wm_fdr"), 1.0),
        f(w55.get("ms_wm_fdr"), 1.0),
    )
    lipid_neighborhood = any(
        bool(x)
        for x in [
            w62.get("in_lipid_lysosomal_myeloid_neighborhood", False),
            broad.get("in_lipid_lysosomal_myeloid_neighborhood", False),
            residual.get("in_lipid_lysosomal_myeloid_neighborhood", False),
            w55.get("in_lipid_lysosomal_myeloid_neighborhood", False),
        ]
    )
    direct_selectivity = max(f(w61.get("selectivity_score")), f(w31.get("direct_selectivity_score")), f(w55.get("best_direct_selectivity_score")))
    direct_target_suppression = max(f(w61.get("target_suppression")), f(w31.get("direct_target_suppression")), f(w55.get("best_direct_target_suppression")))
    real_perturbation = bool(
        s(w61.get("evidence_tier")) == "real_direct_perturbation"
        or s(w31.get("direct_evidence_call")).startswith("selective")
        or f(w61.get("gate_real_perturbation")) == 1
    )
    foundation_support = bool(
        f(w57.get("strong_support_contexts")) >= 1
        or s(w57.get("wave57_call")).startswith("REOPEN")
        or s(w57.get("wave57_call")).startswith("PROMOTE")
    )
    efferocytosis_support = bool(
        f(w61.get("efferocytosis_median_efficient_minus_noneater_lfc")) > 0.5
        and f(w61.get("efferocytosis_contrast_fdr"), 1.0) < 0.2
    )
    chembl_activity = max(
        f(w62.get("druggable_activity_count")),
        f(w34.get("druggable_activity_count")),
        f(w34a.get("chembl_activity_count_nM")),
        f(w59.get("chembl_activity_rows")),
    )
    route_druggability = max(f(w31.get("manual_druggability")), 0.0)
    route_literature_support = False

    if candidate == "SP140_TOP1_TOP2_RESCUE":
        route_literature_support = True
        chembl_activity = 0.0
        route_druggability = 0.0

    gates = {
        "ms_target_resolved": ms_l2g >= 0.5 and ms_qtl >= 0.8,
        "cross_disease_target_resolved": strong_l2g_n >= 4 and relevant_qtl_n >= 3,
        "broad_genetic_support": max(strong_l2g_n, wave55_genetic_n) >= 5,
        "module_or_state_support": lipid_neighborhood or local_pos >= 3 or residual_n >= 2,
        "strict_residual_or_ms_expression": strict_resid_n >= 1 or ms_fdr < 0.1,
        "real_perturbation_support": real_perturbation and direct_selectivity > 0.5,
        "foundation_model_support": foundation_support,
        "repair_or_efferocytosis_guardrail": efferocytosis_support,
        "druggable_or_modality": chembl_activity >= 10 or route_druggability >= 2,
        "no_manual_or_prior_blocker": not bool(manual_blocker),
        "not_generic_or_cytotoxic": "cytotoxic" not in manual_blocker.lower()
        and "broad" not in manual_blocker.lower()
        and "host_defense" not in manual_blocker.lower(),
    }

    gate_pass_count = sum(bool(v) for v in gates.values())
    promotion_gate = all(
        [
            gates["ms_target_resolved"],
            gates["cross_disease_target_resolved"] or gates["broad_genetic_support"],
            gates["module_or_state_support"],
            gates["strict_residual_or_ms_expression"],
            gates["real_perturbation_support"] or (gates["foundation_model_support"] and gates["repair_or_efferocytosis_guardrail"]),
            gates["druggable_or_modality"],
            gates["no_manual_or_prior_blocker"],
            gates["not_generic_or_cytotoxic"],
        ]
    )
    reopener_gate = (
        gates["ms_target_resolved"]
        and (gates["cross_disease_target_resolved"] or gates["broad_genetic_support"])
        and gates["module_or_state_support"]
        and (gates["real_perturbation_support"] or gates["foundation_model_support"] or gates["druggable_or_modality"])
    )

    if promotion_gate:
        call = "PROMOTE_TRANSITION_CONTROLLER_FOR_FULL_V3_AUDIT"
    elif reopener_gate:
        call = "PARK_TRANSITION_CONTROLLER_NEEDS_MISSING_GATE"
    else:
        call = "NO_GO_WAVE63_TRANSITION_CONTROLLER"

    blockers = [gate for gate, passed in gates.items() if not passed]
    score = (
        2.0 * gates["ms_target_resolved"]
        + 1.5 * gates["cross_disease_target_resolved"]
        + 1.0 * gates["broad_genetic_support"]
        + 1.5 * gates["module_or_state_support"]
        + 1.0 * gates["strict_residual_or_ms_expression"]
        + 1.5 * gates["real_perturbation_support"]
        + 0.75 * gates["foundation_model_support"]
        + 0.75 * gates["druggable_or_modality"]
        + 0.25 * route_literature_support
        - 2.0 * (not gates["no_manual_or_prior_blocker"])
        - 1.0 * (not gates["not_generic_or_cytotoxic"])
    )

    return {
        "candidate": candidate,
        "gene": gene,
        "intervention_node": intervention,
        "source_reason": s(row.get("reason")),
        "wave63_score": score,
        "wave63_call": call,
        "gate_pass_count": gate_pass_count,
        "failed_gates": ";".join(blockers),
        "manual_or_prior_blocker": manual_blocker,
        "ms_l2g": ms_l2g,
        "ms_relevant_qtl_h4": ms_qtl,
        "strong_l2g_disease_count": strong_l2g_n,
        "relevant_qtl_coloc_disease_count": relevant_qtl_n,
        "wave55_genetic_disease_count": wave55_genetic_n,
        "local_positive_disease_count": local_pos,
        "local_negative_disease_count": local_neg,
        "residual_retained_disease_count": residual_n,
        "strict_residual_disease_count": strict_resid_n,
        "ms_expression_min_p": ms_p,
        "ms_expression_min_fdr": ms_fdr,
        "lipid_lysosomal_myeloid_neighborhood": lipid_neighborhood,
        "real_perturbation": real_perturbation,
        "direct_selectivity_score": direct_selectivity,
        "direct_target_suppression": direct_target_suppression,
        "foundation_model_support": foundation_support,
        "efferocytosis_support": efferocytosis_support,
        "route_literature_support": route_literature_support,
        "chembl_activity_count": chembl_activity,
        "route_druggability": route_druggability,
        "wave62_call": s(w62.get("wave62_call")),
        "wave31_call": s(w31.get("wave31_call")),
        "wave34_call": s(w34.get("wave34_call")),
        "wave34a_call": s(w34a.get("wave34a_call")),
        "wave57_call": s(w57.get("wave57_call")),
        "wave61_call": s(w61.get("wave61_call")),
        **{f"gate_{k}": bool(v) for k, v in gates.items()},
    }


def build_gate_matrix(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    gate_cols = [c for c in summary.columns if c.startswith("gate_") and c != "gate_pass_count"]
    for _, row in summary.iterrows():
        for col in gate_cols:
            rows.append(
                {
                    "candidate": row["candidate"],
                    "gene": row["gene"],
                    "gate": col.removeprefix("gate_"),
                    "passed": bool(row[col]),
                    "wave63_call": row["wave63_call"],
                }
            )
    return pd.DataFrame(rows)


def md_table(df: pd.DataFrame) -> str:
    if df.empty:
        return ""
    formatted = df.copy()
    for col in formatted.columns:
        formatted[col] = formatted[col].map(lambda value: "" if value is None or (isinstance(value, float) and math.isnan(value)) else str(value).replace("|", "\\|").replace("\n", " "))
    header = "| " + " | ".join(formatted.columns) + " |"
    separator = "| " + " | ".join(["---"] * len(formatted.columns)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in formatted.astype(str).values.tolist()]
    return "\n".join([header, separator, *body])


def write_report(summary: pd.DataFrame, payload: dict[str, Any]) -> None:
    cols = [
        "candidate",
        "gene",
        "intervention_node",
        "wave63_call",
        "wave63_score",
        "gate_pass_count",
        "failed_gates",
        "manual_or_prior_blocker",
        "ms_l2g",
        "ms_relevant_qtl_h4",
        "strong_l2g_disease_count",
        "relevant_qtl_coloc_disease_count",
        "local_positive_disease_count",
        "residual_retained_disease_count",
        "real_perturbation",
        "foundation_model_support",
        "chembl_activity_count",
    ]
    lines = [
        "# Wave63 Transition-Controller Integrator",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Verdict",
        "",
        f"- Promotion calls: `{payload['promotion_count']}`.",
        f"- Park calls: `{payload['park_count']}`.",
        f"- Candidates evaluated: `{payload['n_candidates']}`.",
        "",
        "This is an intersection guardrail, not a discovery claim. It asks whether a",
        "parked genetic/state node gains enough perturbation and modality evidence to",
        "become intervention-grade.",
        "",
        "## Top Rows",
        "",
        md_table(summary[cols].head(25)) if not summary.empty else "No rows.",
        "",
        "## Interpretation",
        "",
        "- Broad target-resolved genetics benchmarks (`BACH2`, `IRF5`, `IL7R`, `STAT4`) remain blocked by module relevance, direction, druggability, or prior art.",
        "- Module-linked rows (`SP140`, `IFI30`, `GALC`) still lack a clean combination of perturbation support, strict residual/MS expression support, and safe modality.",
        "- The SP140-topoisomerase transfer route is explicitly parked because druggability exists only through cytotoxic topoisomerase inhibition and the rescue evidence is not yet cross-autoimmune.",
        "",
        "## Summary JSON",
        "",
        "```json",
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=True),
        "```",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dfs = {name: read_tsv(path) for name, path in INPUTS.items()}
    universe = build_universe(dfs)
    rows = [collect_candidate(row, dfs) for _, row in universe.iterrows()]
    summary = pd.DataFrame(rows)
    if not summary.empty:
        priority = {
            "PROMOTE_TRANSITION_CONTROLLER_FOR_FULL_V3_AUDIT": 0,
            "PARK_TRANSITION_CONTROLLER_NEEDS_MISSING_GATE": 1,
            "NO_GO_WAVE63_TRANSITION_CONTROLLER": 2,
        }
        summary["_priority"] = summary["wave63_call"].map(priority).fillna(9)
        summary = summary.sort_values(["_priority", "wave63_score", "gate_pass_count"], ascending=[True, False, False]).drop(columns=["_priority"])
    gates = build_gate_matrix(summary)
    summary.to_csv(OUT / "transition_controller_candidates.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "transition_controller_gate_matrix.tsv", sep="\t", index=False)
    payload = {
        "seed": SEED,
        "inputs": {k: rel(v) for k, v in INPUTS.items() if v.exists()},
        "n_candidates": int(len(summary)),
        "promotion_count": int(summary["wave63_call"].astype(str).str.startswith("PROMOTE").sum()) if not summary.empty else 0,
        "park_count": int(summary["wave63_call"].astype(str).str.startswith("PARK").sum()) if not summary.empty else 0,
        "top_candidates": summary.head(15)["candidate"].tolist() if not summary.empty else [],
        "interpretation": "No transition-controller is promoted unless target resolution, state/module evidence, perturbation/foundation support, modality, and blocker gates agree.",
    }
    write_json(OUT / "summary.json", payload)
    write_report(summary, payload)
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
