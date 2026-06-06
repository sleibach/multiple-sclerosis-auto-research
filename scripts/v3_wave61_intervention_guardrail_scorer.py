#!/usr/bin/env python3
"""Wave61 perturbation-first guardrail scorer.

This wave is deliberately intervention-centric. It does not ask which genes
are correlated with the autoimmune lipid-lysosomal/APC module. It asks whether
any actual perturbation or intervention has enough selective, translatable
evidence to reopen as a V3 therapeutic claim.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave61_perturbation_first_guardrail"
SEED = 20260527

INPUTS = {
    "wave15_direct": ROOT / "phases/v3/results" / "wave15_perturbation_drug_response" / "ranked_direct_perturbations.tsv",
    "wave15_synthesis": ROOT / "phases/v3/results" / "wave15_perturbation_drug_response" / "candidate_level_synthesis.tsv",
    "wave24_l1000": ROOT / "phases/v3/results" / "wave24_l1000_recurrent_reversal" / "recurrent_l1000_compound_triage.tsv",
    "wave24_mechanisms": ROOT / "phases/v3/results" / "wave24_l1000_recurrent_reversal" / "recurrent_l1000_mechanism_summary.tsv",
    "wave27_unknown": ROOT / "phases/v3/results" / "wave27_l1000_unknown_deconvolution" / "unknown_l1000_deconvolution.tsv",
    "wave35_contrasts": ROOT / "phases/v3/results" / "wave35_resolution_perturbation" / "contrast_level_calls.tsv",
    "wave37_efferocytosis": ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv",
    "wave53_decision": ROOT / "phases/v3/results" / "wave53_perturbation_first_pivot" / "decision_matrix.tsv",
    "wave57_calls": ROOT / "phases/v3/results" / "wave57_intervention_first_geneformer_screen" / "wave57_intervention_first_candidate_calls.tsv",
    "broad_h5ad": ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "broad_residual": ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
    "wave34": ROOT / "phases/v3/results" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv",
    "wave55": ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv",
}

BROAD_BLOCKERS = {
    "IFNGR1": "generic_IFN_blockade_host_defense",
    "IFNGR2": "generic_IFN_blockade_host_defense",
    "IFNAR1": "generic_IFN_blockade_host_defense",
    "JAK1": "generic_JAK_collapse",
    "JAK2": "generic_JAK_collapse",
    "TYK2": "generic_JAK_STAT_axis",
    "STAT1": "generic_IFN_transcription_axis",
    "IRF1": "generic_IFN_transcription_axis",
    "TNFRSF1A": "MS_directionally_unsafe_TNF_axis",
    "TNF": "MS_directionally_unsafe_TNF_axis",
    "CHUK": "broad_NFKB_host_defense",
    "IKBKB": "broad_NFKB_host_defense",
    "IKBKG": "broad_NFKB_host_defense",
    "MAP3K7": "broad_NFKB_MAPK_host_defense",
    "RFX5": "nonselective_MHCII_host_defense",
    "MED16": "broad_transcriptional_Mediator_risk",
    "MED16_KO": "broad_transcriptional_Mediator_risk",
    "GSK3B": "pleiotropic_neuroimmune_metabolic",
    "GSK3B_KO": "pleiotropic_neuroimmune_metabolic",
    "HSP90AA1": "cell_stress_oncology_chaperone",
    "ATP2A1": "cytotoxic_calcium_ER_stress",
    "TUBB": "cytotoxic_microtubule",
    "PLK1": "cell_cycle_oncology",
    "XPO1": "cell_cycle_oncology",
    "CTSB": "generic_cathepsin_prior_art",
    "PPARA": "generic_nuclear_receptor_prior_art",
    "NAMPT": "NAMPT_prior_art_directionality_blocked",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or pd.isna(value):
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def clean_gene(token: Any) -> str:
    text = str(token or "").upper().strip()
    text = re.sub(r"^GENE:", "", text)
    text = re.sub(r"_KO$", "", text)
    text = text.replace("-", "")
    return text


def mean_present(values: list[float | None]) -> float:
    present = [v for v in values if v is not None and not math.isnan(v)]
    return sum(present) / len(present) if present else 0.0


def evidence_join(parts: list[str]) -> str:
    return "; ".join(p for p in parts if p)


def lookup_row(df: pd.DataFrame, key: str, col: str = "gene") -> dict[str, Any]:
    if df.empty or col not in df.columns:
        return {}
    subset = df[df[col].astype(str).str.upper() == key.upper()]
    if subset.empty:
        return {}
    return subset.iloc[0].to_dict()


def enrich_gene_context(gene: str, broad: pd.DataFrame, residual: pd.DataFrame, wave34: pd.DataFrame, eff: pd.DataFrame, wave57: pd.DataFrame) -> dict[str, Any]:
    broad_row = lookup_row(broad, gene, "gene")
    residual_row = lookup_row(residual, gene, "gene")
    wave34_row = lookup_row(wave34, gene, "gene")
    eff_row = lookup_row(eff, gene, "gene_symbol")
    wave57_row = lookup_row(wave57, gene, "gene")
    return {
        "gene": gene,
        "positive_disease_count": to_float(broad_row.get("positive_disease_count"), 0.0),
        "negative_disease_count": to_float(broad_row.get("negative_disease_count"), 0.0),
        "positive_diseases": broad_row.get("positive_diseases", ""),
        "ms_wm_delta_log2": to_float(broad_row.get("ms_wm_delta_log2"), 0.0),
        "ms_wm_p": to_float(broad_row.get("ms_wm_p"), 1.0),
        "ms_wm_fdr": to_float(broad_row.get("ms_wm_fdr"), 1.0),
        "opentargets_max_genetic_association": to_float(broad_row.get("opentargets_max_genetic_association"), 0.0),
        "opentargets_disease_count": to_float(broad_row.get("opentargets_disease_count"), 0.0),
        "residual_retained_disease_count": to_float(residual_row.get("retained_positive_disease_count"), 0.0),
        "strict_core_covariate_surviving_disease_count": to_float(residual_row.get("strict_core_covariate_surviving_disease_count"), 0.0),
        "top_retained_tests": residual_row.get("top_retained_tests", ""),
        "wave34_call": wave34_row.get("wave34_call", ""),
        "gwas_catalog_trait_count": to_float(wave34_row.get("gwas_catalog_trait_count"), 0.0),
        "chembl_target_id": wave34_row.get("chembl_target_id", ""),
        "chembl_best_nM": to_float(wave34_row.get("chembl_best_nM"), math.nan),
        "druggable_activity_count": to_float(wave34_row.get("druggable_activity_count"), 0.0),
        "efferocytosis_screen_call": eff_row.get("screen_call", ""),
        "efferocytosis_median_efficient_minus_noneater_lfc": to_float(eff_row.get("median_efficient_minus_noneater_lfc"), math.nan),
        "efferocytosis_contrast_fdr": to_float(eff_row.get("contrast_fdr"), math.nan),
        "geneformer_model_support_pass": to_bool(wave57_row.get("model_support_pass")),
        "wave57_call": wave57_row.get("wave57_call", ""),
    }


def direct_perturbation_rows(direct: pd.DataFrame, **ctx: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, row in direct.iterrows():
        perturbation = str(row.get("perturbation", ""))
        gene = clean_gene(perturbation)
        gene_ctx = enrich_gene_context(gene, **ctx)
        target_suppression = to_float(row.get("target_suppression"))
        generic_suppression = to_float(row.get("generic_ifn_suppression"))
        selectivity = to_float(row.get("selectivity_score"))
        target_vs_ifn = to_float(row.get("target_vs_ifn_margin"))
        stress_induction = to_float(row.get("stress_induction"))
        stress_abs = to_float(row.get("stress_abs_effect"))
        source = str(row.get("source", ""))
        system = str(row.get("system", ""))
        blocker = BROAD_BLOCKERS.get(gene) or BROAD_BLOCKERS.get(perturbation.upper(), "")
        real_primary = "mouse_macrophage_RNAseq" in source or "primary" in system.lower()
        mixscale = "Mixscale" in source
        real_perturbation = target_suppression >= 0.5
        selective = selectivity >= 0.5 and target_vs_ifn >= 0.5 and target_suppression > max(0.0, generic_suppression)
        not_generic_collapse = generic_suppression < max(0.5, target_suppression * 0.8)
        stress_guardrail = stress_induction <= 0.25 and stress_abs <= 0.75
        eff_call = str(gene_ctx["efferocytosis_screen_call"])
        eff_guardrail = eff_call.startswith("KO_ENHANCES_EFFEROCYTOSIS") or "NEGATIVE_REGULATOR" in eff_call
        eff_fail = eff_call.startswith("KO_IMPAIRS_EFFEROCYTOSIS")
        recurrence = gene_ctx["positive_disease_count"] >= 3 and gene_ctx["negative_disease_count"] <= 1
        ms_anchor = gene_ctx["ms_wm_delta_log2"] > 0 and gene_ctx["ms_wm_p"] < 0.05
        residual = gene_ctx["residual_retained_disease_count"] >= 2
        genetic = gene_ctx["opentargets_max_genetic_association"] >= 0.25 or gene_ctx["gwas_catalog_trait_count"] >= 4
        druggable = gene_ctx["druggable_activity_count"] >= 10 or bool(str(gene_ctx["chembl_target_id"]).strip())
        strong_context = real_primary and not mixscale
        gates = {
            "real_perturbation": real_perturbation,
            "selective_over_ifn": selective,
            "not_generic_collapse": not_generic_collapse,
            "stress_guardrail": stress_guardrail,
            "primary_or_relevant_system": strong_context,
            "repair_or_efferocytosis_guardrail": eff_guardrail and not eff_fail,
            "cross_disease_recurrence": recurrence,
            "ms_nominal_anchor": ms_anchor,
            "residual_support": residual,
            "genetic_support": genetic,
            "druggable_or_modality": druggable,
            "no_manual_blocker": not blocker,
        }
        gate_count = sum(gates.values())
        direct_priority_score = (
            3.0 * real_perturbation
            + 2.0 * selective
            + 1.5 * not_generic_collapse
            + 1.0 * stress_guardrail
            + 1.0 * strong_context
            + 1.0 * max(0.0, min(target_suppression, 4.0))
            + 0.5 * max(0.0, min(selectivity, 3.0))
            - 2.0 * bool(blocker)
        )
        if all(gates[g] for g in ["real_perturbation", "selective_over_ifn", "not_generic_collapse", "stress_guardrail", "primary_or_relevant_system"]) and not blocker:
            call = "REOPEN_REAL_PERTURBATION_NEEDS_DISEASE_TRANSLATION"
        else:
            call = "NO_GO_WAVE61_GUARDRAIL"
        if gate_count >= 10 and not blocker:
            call = "PROMOTE_CANDIDATE_REQUIRES_SUBAGENT_PRIOR_ART_REVIEW"
        rows.append(
            {
                "evidence_tier": "real_direct_perturbation",
                "candidate": perturbation,
                "gene": gene,
                "source": source,
                "dataset": row.get("dataset", ""),
                "system": system,
                "perturbation_type": row.get("perturbation_type", ""),
                "target_suppression": target_suppression,
                "generic_ifn_suppression": generic_suppression,
                "target_vs_ifn_margin": target_vs_ifn,
                "selectivity_score": selectivity,
                "stress_induction": stress_induction,
                "manual_blocker": blocker,
                "gate_count": gate_count,
                "direct_priority_score": direct_priority_score,
                "wave61_call": call,
                **{f"gate_{k}": v for k, v in gates.items()},
                **gene_ctx,
            }
        )
    return rows


def l1000_rows(l1000: pd.DataFrame, mechanisms: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, row in l1000.iterrows():
        target = clean_gene(row.get("target", ""))
        blocker = row.get("wave24_blocker", "") or BROAD_BLOCKERS.get(target, "")
        call = "NO_GO_L1000_ONLY"
        if str(row.get("wave24_call", "")).startswith("PARK"):
            call = "PARK_L1000_ONLY_NEEDS_REAL_PERTURBATION"
        rows.append(
            {
                "evidence_tier": "l1000_reversal_support_only",
                "candidate": row.get("cmap_name", ""),
                "gene": target,
                "source": "L1000FWD",
                "dataset": "LINCS/L1000FWD",
                "system": "cell-line transcriptomic reversal",
                "target_suppression": math.nan,
                "generic_ifn_suppression": math.nan,
                "target_vs_ifn_margin": to_float(row.get("l1000_target_minus_generic_reversal_strength")),
                "selectivity_score": to_float(row.get("recurrence_strength")),
                "stress_induction": math.nan,
                "manual_blocker": blocker,
                "gate_count": 0,
                "wave61_call": call,
                "l1000_wave24_call": row.get("wave24_call", ""),
                "l1000_promotion_gate": row.get("promotion_gate", ""),
                "l1000_opposite_queries": row.get("opposite_queries", ""),
                "l1000_best_rank": row.get("best_opposite_rank", ""),
                "l1000_min_qval": row.get("min_opposite_qval", ""),
                "l1000_contradicted_by_similar_hit": row.get("contradicted_by_similar_hit", ""),
            }
        )
    for _, row in mechanisms.iterrows():
        rows.append(
            {
                "evidence_tier": "l1000_mechanism_summary_support_only",
                "candidate": row.get("compounds", ""),
                "gene": clean_gene(row.get("target", "")),
                "source": "L1000FWD",
                "dataset": "LINCS/L1000FWD",
                "system": "mechanism-level recurrent reversal",
                "target_suppression": math.nan,
                "generic_ifn_suppression": math.nan,
                "target_vs_ifn_margin": math.nan,
                "selectivity_score": to_float(row.get("max_opposite_queries")),
                "stress_induction": math.nan,
                "manual_blocker": row.get("wave24_call", ""),
                "gate_count": 0,
                "wave61_call": "NO_GO_L1000_MECHANISM_ONLY",
                "l1000_wave24_call": row.get("wave24_call", ""),
                "l1000_promotion_gate": row.get("promotion_gate", ""),
                "l1000_best_rank": row.get("best_rank", ""),
                "l1000_min_qval": row.get("min_qval", ""),
            }
        )
    return rows


def resolution_rows(contrasts: pd.DataFrame, **ctx: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    extractors = [
        (r"LIPA", "LIPA"),
        (r"Mertk|MERTK", "MERTK"),
        (r"Gpnmb|GPNMB", "GPNMB"),
        (r"BEX|bexarotene", "RXR_LXR_PPAR"),
        (r"IL10", "IL10"),
        (r"Trem2|TREM2", "TREM2"),
    ]
    for _, row in contrasts.iterrows():
        contrast = str(row.get("contrast", ""))
        gene = "UNRESOLVED"
        for pattern, name in extractors:
            if re.search(pattern, contrast):
                gene = name
                break
        gene_ctx = enrich_gene_context(gene, **ctx) if gene != "RXR_LXR_PPAR" else {}
        lipid_reduced = to_bool(row.get("lipid_apc_reduced"))
        ifn_not_collapsed = to_bool(row.get("ifn_not_collapsed"))
        stress_not_increased = to_bool(row.get("stress_not_increased"))
        resolution_gain = to_bool(row.get("resolution_gain"))
        profibrosis_ok = to_bool(row.get("profibrosis_not_increased"))
        statistical = str(row.get("statistical_status", ""))
        descriptive = "descriptive" in statistical
        gates = {
            "lipid_apc_reduced": lipid_reduced,
            "ifn_not_collapsed": ifn_not_collapsed,
            "stress_not_increased": stress_not_increased,
            "resolution_gain": resolution_gain,
            "profibrosis_not_increased": profibrosis_ok,
            "replicated_or_statistical": not descriptive,
        }
        gate_count = sum(gates.values())
        if lipid_reduced and ifn_not_collapsed and stress_not_increased and resolution_gain and not descriptive:
            call = "REOPEN_RESOLUTION_PERTURBATION"
        else:
            call = "NO_GO_RESOLUTION_GUARDRAIL"
        rows.append(
            {
                "evidence_tier": "resolution_perturbation_guardrail",
                "candidate": contrast,
                "gene": gene,
                "source": "wave35_resolution_perturbation",
                "dataset": row.get("dataset", ""),
                "system": row.get("note", ""),
                "target_suppression": -to_float(row.get("lipid_lysosomal_apc")),
                "generic_ifn_suppression": -to_float(row.get("generic_ifn")),
                "target_vs_ifn_margin": -to_float(row.get("lipid_lysosomal_apc")) - max(0.0, -to_float(row.get("generic_ifn"))),
                "selectivity_score": mean_present(
                    [
                        1.0 if lipid_reduced else 0.0,
                        1.0 if ifn_not_collapsed else 0.0,
                        1.0 if stress_not_increased else 0.0,
                        1.0 if resolution_gain else 0.0,
                    ]
                ),
                "stress_induction": to_float(row.get("stress_cytotoxicity")),
                "manual_blocker": "descriptive_no_replication" if descriptive else "",
                "gate_count": gate_count,
                "wave61_call": call,
                **{f"gate_{k}": v for k, v in gates.items()},
                **gene_ctx,
            }
        )
    return rows


def efferocytosis_reopener_rank(eff: pd.DataFrame, broad: pd.DataFrame, residual: pd.DataFrame, wave34: pd.DataFrame, wave57: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if eff.empty:
        return pd.DataFrame()
    for _, row in eff.iterrows():
        gene = clean_gene(row.get("gene_symbol", ""))
        call = str(row.get("screen_call", ""))
        if not call.startswith("KO_ENHANCES_EFFEROCYTOSIS"):
            continue
        ctx = enrich_gene_context(gene, broad, residual, wave34, eff, wave57)
        lfc = to_float(row.get("median_efficient_minus_noneater_lfc"))
        disease = ctx["positive_disease_count"] >= 3 and ctx["negative_disease_count"] <= 1
        ms = ctx["ms_wm_delta_log2"] > 0 and ctx["ms_wm_p"] < 0.05
        residual_pass = ctx["residual_retained_disease_count"] >= 2
        genetic = ctx["opentargets_max_genetic_association"] >= 0.25 or ctx["gwas_catalog_trait_count"] >= 4
        druggable = ctx["druggable_activity_count"] >= 10 or bool(str(ctx["chembl_target_id"]).strip())
        score = (
            lfc
            + 1.5 * disease
            + 1.0 * ms
            + 1.0 * residual_pass
            + 1.0 * genetic
            + 1.0 * druggable
            + 0.5 * ctx["geneformer_model_support_pass"]
        )
        if disease and (ms or genetic or residual_pass) and druggable:
            reopener_call = "REOPEN_EFFEROCYTOSIS_NEGATIVE_REGULATOR"
        elif disease and (ms or genetic or residual_pass):
            reopener_call = "PARK_EFFEROCYTOSIS_NEGATIVE_REGULATOR_NEEDS_DRUGGABILITY"
        else:
            reopener_call = "NO_GO_EFFEROCYTOSIS_ONLY"
        rows.append(
            {
                "gene": gene,
                "screen_call": call,
                "median_efficient_minus_noneater_lfc": lfc,
                "n_sgrna": row.get("n_sgrna", ""),
                "efficient_fdr": row.get("efficient_fdr", ""),
                "contrast_fdr": row.get("contrast_fdr", ""),
                "reopener_score": score,
                "reopener_call": reopener_call,
                **ctx,
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values(["reopener_call", "reopener_score"], ascending=[True, False])


def gate_matrix(evidence: pd.DataFrame) -> pd.DataFrame:
    gate_cols = [col for col in evidence.columns if col.startswith("gate_")]
    rows: list[dict[str, Any]] = []
    for _, row in evidence.iterrows():
        for gate in gate_cols:
            value = row.get(gate)
            if pd.isna(value):
                continue
            rows.append(
                {
                    "candidate": row.get("candidate", ""),
                    "gene": row.get("gene", ""),
                    "evidence_tier": row.get("evidence_tier", ""),
                    "gate": gate.removeprefix("gate_"),
                    "passed": bool(value),
                    "wave61_call": row.get("wave61_call", ""),
                }
            )
    return pd.DataFrame(rows)


def md_table(df: pd.DataFrame) -> str:
    if df.empty:
        return ""
    formatted = df.copy()
    for col in formatted.columns:
        formatted[col] = formatted[col].map(
            lambda value: ""
            if value is None or (isinstance(value, float) and math.isnan(value))
            else str(value).replace("|", "\\|").replace("\n", " ")
        )
    header = "| " + " | ".join(formatted.columns) + " |"
    separator = "| " + " | ".join(["---"] * len(formatted.columns)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in formatted.astype(str).values.tolist()]
    return "\n".join([header, separator, *body])


def write_report(evidence: pd.DataFrame, eff_rank: pd.DataFrame, summary: dict[str, Any]) -> None:
    report = OUT / "REPORT.md"
    top_cols = [
        "evidence_tier",
        "candidate",
        "gene",
        "source",
        "target_suppression",
        "generic_ifn_suppression",
        "target_vs_ifn_margin",
        "selectivity_score",
        "gate_count",
        "direct_priority_score",
        "manual_blocker",
        "wave61_call",
    ]
    promotable = evidence[evidence["wave61_call"].astype(str).str.startswith("PROMOTE")]
    reopened = evidence[evidence["wave61_call"].astype(str).str.startswith("REOPEN")]
    top_direct = evidence[evidence["evidence_tier"].eq("real_direct_perturbation")].sort_values(
        ["direct_priority_score", "target_suppression", "selectivity_score"], ascending=[False, False, False]
    ).head(12)
    top_eff = eff_rank.head(12) if not eff_rank.empty else pd.DataFrame()
    lines = [
        "# Wave61 Perturbation-First Guardrail Scorer",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Verdict",
        "",
        f"- Promotion candidates: `{len(promotable)}`.",
        f"- Reopened perturbation candidates: `{len(reopened)}`.",
        f"- L1000-only candidates were capped at support-only status by design.",
        "",
        "The scorer treats real perturbation evidence as necessary but not sufficient. A route also needs selectivity over generic IFN/JAK/NF-kB collapse, stress/viability guardrails, repair or efferocytosis guardrails, disease recurrence including MS, genetics or response anchoring, druggability, and no manual safety/prior-art blocker.",
        "",
        "## Top Direct Perturbation Rows",
        "",
        md_table(top_direct[top_cols]) if not top_direct.empty else "No direct perturbation rows.",
        "",
        "## Efferocytosis Negative-Regulator Reopener Scan",
        "",
    ]
    if top_eff.empty:
        lines.append("No efferocytosis reopener rows.")
    else:
        lines.append(
            md_table(
                top_eff[
                    [
                        "gene",
                        "median_efficient_minus_noneater_lfc",
                        "positive_disease_count",
                        "ms_wm_delta_log2",
                        "ms_wm_p",
                        "residual_retained_disease_count",
                        "gwas_catalog_trait_count",
                        "chembl_target_id",
                        "reopener_score",
                        "reopener_call",
                    ]
                ]
            )
        )
    lines.extend(
        [
            "",
            "## Summary JSON",
            "",
            "```json",
            json.dumps(summary, indent=2, sort_keys=True, allow_nan=True),
            "```",
            "",
            "## Guardrail",
            "",
            "No route from this wave is a therapeutic claim unless subagent prior-art and translational audits agree. The output is an intervention triage layer for the continuing V3 session.",
        ]
    )
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    direct = read_tsv(INPUTS["wave15_direct"])
    l1000 = read_tsv(INPUTS["wave24_l1000"])
    mechanisms = read_tsv(INPUTS["wave24_mechanisms"])
    contrasts = read_tsv(INPUTS["wave35_contrasts"])
    eff = read_tsv(INPUTS["wave37_efferocytosis"])
    broad = read_tsv(INPUTS["broad_h5ad"])
    residual = read_tsv(INPUTS["broad_residual"])
    wave34 = read_tsv(INPUTS["wave34"])
    wave57 = read_tsv(INPUTS["wave57_calls"])

    ctx = {
        "broad": broad,
        "residual": residual,
        "wave34": wave34,
        "eff": eff,
        "wave57": wave57,
    }
    rows = []
    rows.extend(direct_perturbation_rows(direct, **ctx))
    rows.extend(l1000_rows(l1000, mechanisms))
    rows.extend(resolution_rows(contrasts, **ctx))
    evidence = pd.DataFrame(rows)
    if not evidence.empty:
        evidence = evidence.sort_values(["wave61_call", "gate_count", "selectivity_score"], ascending=[True, False, False])
    eff_rank = efferocytosis_reopener_rank(eff, broad, residual, wave34, wave57)
    gates = gate_matrix(evidence)

    evidence.to_csv(OUT / "intervention_evidence_tiers.tsv", sep="\t", index=False)
    eff_rank.to_csv(OUT / "efferocytosis_expression_reopener_rank.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "gate_matrix.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "inputs": {k: rel(v) for k, v in INPUTS.items() if v.exists()},
        "n_evidence_rows": int(len(evidence)),
        "n_direct_perturbation_rows": int((evidence["evidence_tier"] == "real_direct_perturbation").sum()) if not evidence.empty else 0,
        "n_l1000_rows": int(evidence["evidence_tier"].astype(str).str.contains("l1000").sum()) if not evidence.empty else 0,
        "n_resolution_rows": int((evidence["evidence_tier"] == "resolution_perturbation_guardrail").sum()) if not evidence.empty else 0,
        "promotion_candidates": evidence[evidence["wave61_call"].astype(str).str.startswith("PROMOTE")]["candidate"].tolist() if not evidence.empty else [],
        "reopened_candidates": evidence[evidence["wave61_call"].astype(str).str.startswith("REOPEN")]["candidate"].tolist() if not evidence.empty else [],
        "top_direct_candidates": evidence[evidence["evidence_tier"].eq("real_direct_perturbation")]
        .sort_values(["direct_priority_score", "target_suppression", "selectivity_score"], ascending=[False, False, False])["candidate"]
        .head(10)
        .tolist()
        if not evidence.empty
        else [],
        "top_efferocytosis_reopeners": eff_rank.head(10)["gene"].tolist() if not eff_rank.empty else [],
        "interpretation": "Intervention-level triage only. No candidate is promoted without real perturbation, guardrails, translational feasibility, and prior-art clearance.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")
    write_report(evidence, eff_rank, summary)
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
