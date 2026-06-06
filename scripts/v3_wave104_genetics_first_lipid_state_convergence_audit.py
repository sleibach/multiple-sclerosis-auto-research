#!/usr/bin/env python3
"""Wave104 genetics-first lipid-state convergence audit.

Wave103 failed because intervention-first candidates either lacked cross-disease
anchoring or were not actionable. This wave reverses the order: start from
target-resolved autoimmune genetic nodes, then ask whether any of them converge
with the lipid-lysosomal inflammatory state and remain worth target-specific
sidecars.

Guardrail: GWAS overlap alone is not enough. A candidate must have an MS genetic
anchor, cross-autoimmune target-resolution/QTL breadth, and at least one
non-genetic state/direction layer before it can be reopened. Modality and prior
art remain promotion gates.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave104_genetics_first_lipid_state_convergence_audit"

W62 = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W91 = ROOT / "phases/v3/results" / "wave91_lipid_lysosomal_module_intervention_rank" / "lipid_lysosomal_intervention_rank.tsv"
W94 = ROOT / "phases/v3/results" / "wave94_accessible_state_rerank" / "accessible_state_candidate_rank.tsv"
W103 = ROOT / "phases/v3/results" / "wave103_intervention_first_successor_triage" / "intervention_first_successor_rank.tsv"
W57 = ROOT / "phases/v3/results" / "wave57_intervention_first_geneformer_screen" / "wave57_intervention_first_candidate_calls.tsv"
W81 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W37 = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
RESIDUAL = ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
BROAD = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
W83 = ROOT / "phases/v3/results" / "wave83_intervention_class_first_scan" / "reachable_intervention_rank.tsv"


PRIOR_OR_SAFETY_RE = re.compile(
    r"prior|blocked|saturat|generic|host.?defense|safety|wrong.?direction|"
    r"checkpoint|costimulation|jak|tyk|cathepsin|broad|systemic|hla|mhc|"
    r"adhesion|neutrophil|chemokine|cytokine|anti.?tnf|paradox",
    re.I,
)

ROUTE_HINTS: dict[str, dict[str, Any]] = {
    "SP140": {
        "route_hypothesis": "myeloid chromatin/nuclear-body regulator; possible PROTAC or epigenetic reader-modulation route only if causal direction is established",
        "manual_route_blocker": "nuclear protein with no mature selective autoimmune modality; disease genetics may reflect loss-of-function rather than inhibit-to-treat direction",
        "manual_reachable": False,
        "manual_prior_or_safety": False,
    },
    "GALC": {
        "route_hypothesis": "lysosomal sphingolipid enzyme; intervention would likely be enzyme restoration, substrate handling, or lipid-trafficking correction",
        "manual_route_blocker": "loss of GALC causes Krabbe disease, so inhibition is biologically unsafe; activation/restoration modality for inflammatory autoimmune lesions is unproven",
        "manual_reachable": True,
        "manual_prior_or_safety": True,
    },
    "RGS1": {
        "route_hypothesis": "immune-cell migration and GPCR desensitization regulator at genetically colocalized autoimmune loci",
        "manual_route_blocker": "intracellular RGS protein with difficult selectivity and unclear agonize-vs-inhibit disease direction",
        "manual_reachable": False,
        "manual_prior_or_safety": False,
    },
    "INAVA": {
        "route_hypothesis": "innate immune adaptor at IBD/MS/AS/UC genetic loci",
        "manual_route_blocker": "intracellular adaptor, weak local lipid-state evidence, and no clear selective modality",
        "manual_reachable": False,
        "manual_prior_or_safety": False,
    },
    "ANKRD55": {
        "route_hypothesis": "T-cell genetic node rather than lipid-lysosomal myeloid controller",
        "manual_route_blocker": "does not map cleanly to the shared lipid-lysosomal myeloid state",
        "manual_reachable": False,
        "manual_prior_or_safety": False,
    },
    "IL7R": {
        "route_hypothesis": "known autoimmune cytokine-receptor axis",
        "manual_route_blocker": "prior-art crowded CD127/IL-7R autoimmune route",
        "manual_reachable": True,
        "manual_prior_or_safety": True,
    },
    "STAT4": {
        "route_hypothesis": "broad Th1/Th17 transcriptional axis",
        "manual_route_blocker": "not selectively druggable and prior-art crowded pathway",
        "manual_reachable": False,
        "manual_prior_or_safety": True,
    },
    "PTGER4": {
        "route_hypothesis": "EP4 receptor barrier/tolerance axis",
        "manual_route_blocker": "directionality and prior-art conflicts across autoimmune indications",
        "manual_reachable": True,
        "manual_prior_or_safety": True,
    },
    "TNFRSF1A": {
        "route_hypothesis": "TNF receptor signaling",
        "manual_route_blocker": "TNF-axis prior art and MS paradox risk",
        "manual_reachable": True,
        "manual_prior_or_safety": True,
    },
    "IFI30": {
        "route_hypothesis": "lysosomal thiol reductase / antigen-processing node",
        "manual_route_blocker": "host-defense and antigen-processing risk; prior waves already demoted cathepsin-like lysosomal inhibition",
        "manual_reachable": False,
        "manual_prior_or_safety": True,
    },
    "CTSH": {
        "route_hypothesis": "lysosomal cathepsin",
        "manual_route_blocker": "cathepsin route is host-defense and selectivity blocked",
        "manual_reachable": True,
        "manual_prior_or_safety": True,
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


def union_diseases(*values: Any) -> list[str]:
    diseases: set[str] = set()
    for value in values:
        for item in split_semicolon(value):
            if item:
                diseases.add(item)
    return sorted(diseases)


def candidate_genes(w62: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> list[str]:
    genes: set[str] = set()
    if not w62.empty:
        w = w62.copy()
        for col in [
            "ms_max_l2g_score",
            "ms_max_relevant_qtl_h4",
            "strong_l2g_disease_count",
            "strong_qtl_coloc_disease_count",
            "local_positive_disease_count",
            "residual_retained_disease_count",
            "wave62_score",
        ]:
            if col in w.columns:
                w[col] = pd.to_numeric(w[col], errors="coerce").fillna(0.0)
        mask = (
            (w["ms_max_l2g_score"] >= 0.5)
            | (w["ms_max_relevant_qtl_h4"] >= 0.8)
            | (w["strong_l2g_diseases"].astype(str).str.contains(r"(^|;)MS(;|$)", regex=True, na=False))
            | (w["strong_qtl_coloc_diseases"].astype(str).str.contains(r"(^|;)MS(;|$)", regex=True, na=False))
        )
        mask &= (
            (w["strong_l2g_disease_count"] >= 2)
            | (w["strong_qtl_coloc_disease_count"] >= 2)
            | (w["local_positive_disease_count"] >= 2)
            | (w["wave62_score"] >= 2.0)
        )
        genes.update(w.loc[mask, "gene"].dropna().astype(str).str.upper())

    for name, df in tables.items():
        if df.empty:
            continue
        col = "gene_symbol" if name == "w37" else "gene"
        if col in df.columns:
            genes.update(df[col].dropna().astype(str).str.upper())
    return sorted(g for g in genes if g and g != "NAN")


def collect() -> pd.DataFrame:
    tables = {
        "w91": read_tsv(W91),
        "w94": read_tsv(W94),
        "w103": read_tsv(W103),
        "w57": read_tsv(W57),
        "w81": read_tsv(W81),
        "w37": read_tsv(W37),
        "residual": read_tsv(RESIDUAL),
        "broad": read_tsv(BROAD),
        "w83": read_tsv(W83),
    }
    w62 = read_tsv(W62)
    rows: list[dict[str, Any]] = []
    for gene in candidate_genes(w62, tables):
        w62r = first_row(w62, gene)
        if w62r is None:
            continue
        w91 = first_row(tables["w91"], gene)
        w94 = first_row(tables["w94"], gene)
        w103 = first_row(tables["w103"], gene)
        w57 = first_row(tables["w57"], gene)
        w81 = first_row(tables["w81"], gene)
        w37 = first_row(tables["w37"], gene, "gene_symbol")
        resid = first_row(tables["residual"], gene)
        broad = first_row(tables["broad"], gene)
        w83 = first_row(tables["w83"], gene)
        hint = ROUTE_HINTS.get(gene, {})

        genetic_diseases = union_diseases(
            w62r.get("strong_l2g_diseases"),
            w62r.get("strong_qtl_coloc_diseases"),
            w62r.get("wave55_genetic_diseases_ge_0_25"),
            w83.get("genetic_breadth_diseases") if w83 is not None else "",
            w57.get("diseases_genetic_ge_0_25") if w57 is not None else "",
        )
        local_diseases = union_diseases(
            w62r.get("local_positive_diseases"),
            broad.get("positive_diseases") if broad is not None else "",
            w94.get("positive_diseases") if w94 is not None else "",
            w91.get("direct_positive_p05_diseases") if w91 is not None else "",
            w81.get("broad_positive_diseases") if w81 is not None else "",
        )

        closure_text = " | ".join(
            [
                clean(w62r.get("manual_blocker")),
                clean(w62r.get("prior_context_blocker")),
                clean(w83.get("hard_failures")) if w83 is not None else "",
                clean(w83.get("manual_closure_reason")) if w83 is not None else "",
                clean(w103.get("closure_text")) if w103 is not None else "",
                clean(hint.get("manual_route_blocker")),
            ]
        )

        ms_l2g = num(w62r.get("ms_max_l2g_score"), 0.0)
        ms_qtl = max(num(w62r.get("ms_max_relevant_qtl_h4"), 0.0), num(w62r.get("ms_max_qtl_h4"), 0.0))
        strong_l2g = int(num(w62r.get("strong_l2g_disease_count"), 0.0))
        strong_qtl = int(num(w62r.get("strong_qtl_coloc_disease_count"), 0.0))
        relevant_qtl = int(num(w62r.get("relevant_qtl_coloc_disease_count"), 0.0))
        local_positive = int(max(
            num(w62r.get("local_positive_disease_count"), 0.0),
            num(broad.get("positive_disease_count"), 0.0) if broad is not None else 0.0,
            num(w94.get("positive_disease_count"), 0.0) if w94 is not None else 0.0,
            num(w81.get("broad_positive_disease_count"), 0.0) if w81 is not None else 0.0,
        ))
        residual_retained = int(max(
            num(w62r.get("residual_retained_disease_count"), 0.0),
            num(resid.get("retained_positive_disease_count"), 0.0) if resid is not None else 0.0,
            num(w57.get("retained_positive_disease_count"), 0.0) if w57 is not None else 0.0,
        ))
        strict_residual = int(max(
            num(w62r.get("strict_core_covariate_surviving_disease_count"), 0.0),
            num(resid.get("strict_core_covariate_surviving_disease_count"), 0.0) if resid is not None else 0.0,
            num(w57.get("strict_core_covariate_surviving_disease_count"), 0.0) if w57 is not None else 0.0,
        ))

        response_nonresponse = int(num(w91.get("response_nonresponse_high_context_count"), 0.0) if w91 is not None else 0.0)
        response_nominal = int(num(w91.get("response_nominal_or_trend_context_count"), 0.0) if w91 is not None else 0.0)
        direct_perturbation = flag(w81.get("direct_perturbation")) if w81 is not None else False
        foundation_support = bool(
            (num(w81.get("foundation_model_support"), 0.0) if w81 is not None else 0.0) > 0
            or (num(w57.get("support_contexts"), 0.0) if w57 is not None else 0.0) > 0
        )
        strong_foundation = bool(num(w57.get("strong_support_contexts"), 0.0) if w57 is not None else 0.0)
        efferocytosis_call = clean(w37.get("screen_call")) if w37 is not None else ""
        efferocytosis_lfc = num(w37.get("median_efficient_minus_noneater_lfc")) if w37 is not None else math.nan
        efferocytosis_fdr = num(w37.get("contrast_fdr")) if w37 is not None else math.nan

        chembl_count = int(max(
            num(w62r.get("druggable_activity_count"), 0.0),
            num(w83.get("chembl_activity_count"), 0.0) if w83 is not None else 0.0,
            num(w103.get("chembl_activity_count"), 0.0) if w103 is not None else 0.0,
        ))
        reachability = max(
            num(w83.get("reachability_score"), 0.0) if w83 is not None else 0.0,
            num(w103.get("reachability_score"), 0.0) if w103 is not None else 0.0,
            2.0 if hint.get("manual_reachable") else 0.0,
        )

        gate_ms_genetic = ms_l2g >= 0.5 or ms_qtl >= 0.8 or "MS" in genetic_diseases
        gate_cross_genetic = strong_l2g >= 3 or strong_qtl >= 3 or len(genetic_diseases) >= 4
        gate_lipid_state = (
            flag(w62r.get("in_lipid_lysosomal_myeloid_neighborhood"))
            or (broad is not None and flag(broad.get("in_lipid_lysosomal_myeloid_neighborhood")))
            or (w94 is not None and flag(w94.get("in_lipid_lysosomal_myeloid_neighborhood")))
            or local_positive >= 3
            or residual_retained >= 1
            or response_nonresponse >= 2
        )
        gate_directional = direct_perturbation or foundation_support or response_nonresponse >= 2 or residual_retained >= 1 or strict_residual >= 1
        gate_modality = reachability >= 2.0 or chembl_count > 0 or bool(hint.get("manual_reachable"))
        prior_or_safety = (
            PRIOR_OR_SAFETY_RE.search(closure_text) is not None
            or flag(w103.get("prior_or_safety_blocked")) if w103 is not None else False
            or bool(hint.get("manual_prior_or_safety"))
        )

        score = 0.0
        score += 2.5 if gate_ms_genetic else 0.0
        score += min(3.0, 0.45 * len(genetic_diseases))
        score += min(2.0, 0.4 * strong_l2g)
        score += min(2.0, 0.4 * strong_qtl)
        score += min(2.5, 0.45 * local_positive)
        score += 1.5 if residual_retained >= 1 else 0.0
        score += 1.5 if strict_residual >= 1 else 0.0
        score += 1.0 if flag(w62r.get("in_lipid_lysosomal_myeloid_neighborhood")) else 0.0
        score += min(2.0, 0.5 * response_nonresponse)
        score += 1.5 if direct_perturbation else 0.0
        score += 1.0 if foundation_support else 0.0
        score += 0.75 if strong_foundation else 0.0
        score += min(1.5, 0.3 * reachability)
        score += 1.0 if chembl_count > 0 else 0.0
        score -= 3.0 if prior_or_safety else 0.0
        score -= 1.5 if not gate_modality else 0.0

        missing = []
        if not gate_ms_genetic:
            missing.append("ms_genetic_anchor")
        if not gate_cross_genetic:
            missing.append("cross_autoimmune_genetics")
        if not gate_lipid_state:
            missing.append("lipid_state_or_recurrence")
        if not gate_directional:
            missing.append("directional_or_perturbation_support")
        if not gate_modality:
            missing.append("reachable_modality")
        if prior_or_safety:
            missing.append("prior_or_safety")

        if gate_ms_genetic and gate_cross_genetic and gate_lipid_state and gate_directional and gate_modality and not prior_or_safety:
            call = "REOPEN_GENETICS_FIRST_TARGET_SIDECARS"
            priority = 0
        elif gate_ms_genetic and gate_cross_genetic and gate_lipid_state and gate_directional and not gate_modality:
            call = "PARK_GENETICS_STATE_DIRECTION_NO_MODALITY"
            priority = 1
        elif gate_ms_genetic and gate_cross_genetic and gate_lipid_state:
            call = "PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY"
            priority = 2
        elif gate_ms_genetic and gate_cross_genetic:
            call = "PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE"
            priority = 3
        elif gate_ms_genetic:
            call = "PARK_MS_GENETICS_NARROW_OR_WEAK"
            priority = 4
        else:
            call = "NO_GO_NO_MS_GENETIC_ANCHOR"
            priority = 5

        rows.append(
            {
                "gene": gene,
                "approved_name": clean(w62r.get("approved_name")),
                "wave104_call": call,
                "wave104_call_priority": priority,
                "wave104_score": score,
                "wave104_missing_gates": ";".join(missing),
                "route_hypothesis": clean(hint.get("route_hypothesis")),
                "manual_route_blocker": clean(hint.get("manual_route_blocker")),
                "prior_or_safety": prior_or_safety,
                "gate_ms_genetic": gate_ms_genetic,
                "gate_cross_autoimmune_genetics": gate_cross_genetic,
                "gate_lipid_state_or_recurrence": gate_lipid_state,
                "gate_directional_or_perturbation": gate_directional,
                "gate_reachable_modality": gate_modality,
                "ms_max_l2g_score": ms_l2g,
                "ms_max_relevant_qtl_h4": ms_qtl,
                "strong_l2g_disease_count": strong_l2g,
                "strong_l2g_diseases": clean(w62r.get("strong_l2g_diseases")),
                "strong_qtl_coloc_disease_count": strong_qtl,
                "relevant_qtl_coloc_disease_count": relevant_qtl,
                "strong_qtl_coloc_diseases": clean(w62r.get("strong_qtl_coloc_diseases")),
                "genetic_disease_count_union": len(genetic_diseases),
                "genetic_diseases_union": ";".join(genetic_diseases),
                "local_positive_disease_count": local_positive,
                "local_positive_diseases": ";".join(local_diseases),
                "in_lipid_lysosomal_myeloid_neighborhood": bool(
                    flag(w62r.get("in_lipid_lysosomal_myeloid_neighborhood"))
                    or (broad is not None and flag(broad.get("in_lipid_lysosomal_myeloid_neighborhood")))
                    or (w94 is not None and flag(w94.get("in_lipid_lysosomal_myeloid_neighborhood")))
                ),
                "residual_retained_disease_count": residual_retained,
                "strict_residual_disease_count": strict_residual,
                "response_nonresponse_high_context_count": response_nonresponse,
                "response_nominal_or_trend_context_count": response_nominal,
                "direct_perturbation": direct_perturbation,
                "direct_perturbation_detail": clean(w81.get("direct_perturbation_detail")) if w81 is not None else "",
                "foundation_support": foundation_support,
                "model_support_contexts_w57": num(w57.get("support_contexts"), 0.0) if w57 is not None else 0.0,
                "model_strong_contexts_w57": num(w57.get("strong_support_contexts"), 0.0) if w57 is not None else 0.0,
                "best_model_context": clean(w57.get("best_context")) if w57 is not None else "",
                "efferocytosis_screen_call": efferocytosis_call,
                "efferocytosis_contrast_lfc": efferocytosis_lfc,
                "efferocytosis_contrast_fdr": efferocytosis_fdr,
                "reachability_score": reachability,
                "intervention_class": clean(w83.get("intervention_class")) if w83 is not None else clean(w103.get("intervention_class")) if w103 is not None else "",
                "chembl_activity_count": chembl_count,
                "chembl_target_id": clean(w62r.get("chembl_target_id")) or (clean(w83.get("chembl_target_id")) if w83 is not None else ""),
                "wave62_score": num(w62r.get("wave62_score"), 0.0),
                "wave62_call": clean(w62r.get("wave62_call")),
                "wave83_call": clean(w83.get("wave83_call")) if w83 is not None else "",
                "wave91_call": clean(w91.get("wave91_call")) if w91 is not None else "",
                "wave103_call": clean(w103.get("wave103_call")) if w103 is not None else "",
                "closure_text": closure_text,
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values(
        ["wave104_call_priority", "wave104_score", "genetic_disease_count_union", "local_positive_disease_count"],
        ascending=[True, False, False, False],
    )


def write_report(rank: pd.DataFrame) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rank.to_csv(OUT / "genetics_first_lipid_state_rank.tsv", sep="\t", index=False)

    counts = rank["wave104_call"].value_counts().sort_index().to_dict() if not rank.empty else {}
    reopen = rank[rank["wave104_call"].eq("REOPEN_GENETICS_FIRST_TARGET_SIDECARS")].copy() if not rank.empty else pd.DataFrame()
    park = rank[rank["wave104_call"].str.startswith("PARK_", na=False)].copy() if not rank.empty else pd.DataFrame()

    top_cols = [
        "gene",
        "approved_name",
        "wave104_call",
        "wave104_score",
        "wave104_missing_gates",
        "ms_max_l2g_score",
        "ms_max_relevant_qtl_h4",
        "genetic_disease_count_union",
        "genetic_diseases_union",
        "local_positive_disease_count",
        "local_positive_diseases",
        "residual_retained_disease_count",
        "response_nonresponse_high_context_count",
        "direct_perturbation",
        "foundation_support",
        "reachability_score",
        "chembl_activity_count",
        "prior_or_safety",
        "route_hypothesis",
        "manual_route_blocker",
    ]
    if not rank.empty:
        top = rank.head(40)[top_cols]
        sidecar = rank[
            rank["wave104_call"].isin(
                [
                    "REOPEN_GENETICS_FIRST_TARGET_SIDECARS",
                    "PARK_GENETICS_STATE_DIRECTION_NO_MODALITY",
                    "PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY",
                ]
            )
        ].head(12)[top_cols]
    else:
        top = pd.DataFrame(columns=top_cols)
        sidecar = pd.DataFrame(columns=top_cols)

    if not reopen.empty:
        branch = "REOPEN_GENETICS_FIRST_TARGET_SIDECARS"
    elif not sidecar.empty:
        branch = "NO_PROMOTABLE_TARGET_BUT_DISPATCH_GENETICS_STATE_SIDECARS"
    else:
        branch = "NO_GENETICS_FIRST_LIPID_STATE_CANDIDATE"

    summary = {
        "seed": SEED,
        "branch_call": branch,
        "n_ranked": int(len(rank)),
        "call_counts": counts,
        "reopen_genes": reopen["gene"].tolist() if not reopen.empty else [],
        "sidecar_recommendation_genes": sidecar["gene"].tolist() if not sidecar.empty else [],
        "inputs": {
            "wave62": rel(W62),
            "wave91": rel(W91),
            "wave94": rel(W94),
            "wave103": rel(W103),
            "wave57": rel(W57),
            "wave81": rel(W81),
            "wave37": rel(W37),
            "residual": rel(RESIDUAL),
            "broad": rel(BROAD),
            "wave83": rel(W83),
        },
    }
    write_json(OUT / "summary.json", summary)

    lines = [
        "# Wave104 Genetics-First Lipid-State Convergence Audit",
        "",
        "## Bottom Line",
        "",
        f"Branch call: `{branch}`.",
        "",
        "This wave starts with target-resolved autoimmune genetics and only then asks",
        "whether the gene intersects the shared lipid-lysosomal/cell-state module.",
        "A genetics-only result is not treated as a therapeutic finding.",
        "",
        "## Call Counts",
        "",
        "```json",
        json.dumps(counts, indent=2, sort_keys=True),
        "```",
        "",
        "## Top Ranked Candidates",
        "",
        markdown_table(top, max_rows=40),
        "",
        "## Sidecar Dispatch Set",
        "",
        markdown_table(sidecar, max_rows=12),
        "",
        "## Interpretation",
        "",
        "- Candidates in `REOPEN_GENETICS_FIRST_TARGET_SIDECARS` would deserve immediate",
        "  target-specific mechanism, perturbation, novelty, and modality sidecars.",
        "- `PARK_GENETICS_STATE_DIRECTION_NO_MODALITY` means the biology is interesting",
        "  but no intervention point is currently credible.",
        "- `PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY` means the node overlaps the",
        "  cross-disease state but still lacks causal direction or a credible route.",
        "- Prior/safety flags are retained as hard promotion blockers even when genetics",
        "  and state recurrence are strong.",
        "",
        "## Reproducibility",
        "",
        f"- Script: `{rel(ROOT / 'scripts' / 'v3_wave104_genetics_first_lipid_state_convergence_audit.py')}`",
        f"- Rank table: `{rel(OUT / 'genetics_first_lipid_state_rank.tsv')}`",
        f"- Summary: `{rel(OUT / 'summary.json')}`",
        f"- Seed: `{SEED}`",
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    rank = collect()
    write_report(rank)


if __name__ == "__main__":
    main()
