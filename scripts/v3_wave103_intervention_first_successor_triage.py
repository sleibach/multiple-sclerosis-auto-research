#!/usr/bin/env python3
"""Wave103 intervention-first successor triage.

The accessible-survivor route failed because expression recurrence did not
translate into target-specific leverage. This wave restarts from candidates
with at least one non-expression anchor: direct perturbation, foundation-model
support, target genetics, or a reachable/druggable intervention class. It then
asks which candidates deserve route-specific sidecars.

Guardrail: a familiar prior-art-heavy immunology node is not a successor target
even if the score is high. Prior closure, host-defense risk, generic cytokine/
chemokine biology, and wrong-direction modality are explicit blockers.
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
OUT = ROOT / "results_v3" / "wave103_intervention_first_successor_triage"

W81 = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W57 = ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_intervention_first_candidate_calls.tsv"
W83 = ROOT / "results_v3" / "wave83_intervention_class_first_scan" / "reachable_intervention_rank.tsv"
W91 = ROOT / "results_v3" / "wave91_lipid_lysosomal_module_intervention_rank" / "lipid_lysosomal_intervention_rank.tsv"
W94 = ROOT / "results_v3" / "wave94_accessible_state_rerank" / "accessible_state_candidate_rank.tsv"
W102 = ROOT / "results_v3" / "wave102_accessible_survivor_residual_compartment_test" / "accessible_survivor_residual_summary.tsv"
W37 = ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"

PRIOR_BLOCK_RE = re.compile(
    r"prior|saturat|generic|host.?defense|safety|blocked|wrong.?direction|"
    r"checkpoint|costimulation|jak|tyk|cathepsin|broad|systemic|hla|mhc|"
    r"adhesion|neutrophil|chemokine|cytokine|anti.?tnf",
    re.I,
)

MANUAL_NOTES = {
    "DAB2": {
        "manual_route": "intracellular adaptor; DAB2 loss enhances macrophage efferocytosis in local CRISPR screen",
        "manual_blocker": "not externally druggable; agonist/restoration route is unclear",
    },
    "CD9": {
        "manual_route": "surface tetraspanin; local CRISPR suggests knockout enhances efferocytosis",
        "manual_blocker": "tetraspanin pleiotropy and unclear safe inhibition/agonism direction",
    },
    "PSAP": {
        "manual_route": "secreted/lysosomal saposin precursor; plausible lipid-remyelination biology",
        "manual_blocker": "broad trophic/lysosomal biology; no strong cross-autoimmune local recurrence",
    },
    "DAP": {
        "manual_route": "death-associated/autophagy-linked protein with broad genetics and MS expression",
        "manual_blocker": "no actionable modality or directional perturbation support",
    },
    "FAP": {
        "manual_route": "cell-surface serine protease and stromal handle",
        "manual_blocker": "oncology/fibrosis prior art and uncertain autoimmune direction",
    },
    "CD226": {
        "manual_route": "immune receptor checkpoint-like axis",
        "manual_blocker": "known autoimmune genetics but checkpoint biology and prior programs crowd route",
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


def genes_from_sources(tables: dict[str, pd.DataFrame]) -> list[str]:
    genes: set[str] = set()
    for name, df in tables.items():
        if df.empty:
            continue
        col = "gene_symbol" if name == "w37" else "gene"
        if col in df.columns:
            genes.update(df[col].dropna().astype(str).str.upper())
    return sorted(g for g in genes if g and g != "NAN")


def collect(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for gene in genes_from_sources(tables):
        w81 = first_row(tables["w81"], gene)
        w57 = first_row(tables["w57"], gene)
        w83 = first_row(tables["w83"], gene)
        w91 = first_row(tables["w91"], gene)
        w94 = first_row(tables["w94"], gene)
        w102 = first_row(tables["w102"], gene)
        w37 = first_row(tables["w37"], gene, "gene_symbol")
        w62 = first_row(tables["w62"], gene)
        note = MANUAL_NOTES.get(gene, {})

        closure_text = " | ".join(
            [
                clean(w83.get("hard_failures")) if w83 is not None else "",
                clean(w83.get("manual_closure_reason")) if w83 is not None else "",
                clean(w83.get("primary_route_note")) if w83 is not None else "",
                clean(w91.get("route_blocker")) if w91 is not None else "",
                clean(w62.get("manual_blocker")) if w62 is not None else "",
                clean(note.get("manual_blocker")),
            ]
        )
        direct_detail = clean(w81.get("direct_perturbation_detail")) if w81 is not None else ""
        foundation_detail = clean(w81.get("foundation_model_detail")) if w81 is not None else ""

        rec: dict[str, Any] = {
            "gene": gene,
            "sources_present": ";".join(
                name for name, row in [
                    ("wave81", w81),
                    ("wave57", w57),
                    ("wave83", w83),
                    ("wave91", w91),
                    ("wave94", w94),
                    ("wave102", w102),
                    ("wave37", w37),
                    ("wave62", w62),
                ] if row is not None
            ),
            "manual_route": clean(note.get("manual_route")),
            "manual_blocker": clean(note.get("manual_blocker")),
            "closure_text": closure_text,
            "wave81_call": clean(w81.get("wave81_call")) if w81 is not None else "",
            "wave81_score": num(w81.get("score"), 0.0) if w81 is not None else 0.0,
            "direct_perturbation": num(w81.get("direct_perturbation"), 0.0) if w81 is not None else 0.0,
            "direct_perturbation_detail": direct_detail,
            "foundation_model_support_w81": num(w81.get("foundation_model_support"), 0.0) if w81 is not None else 0.0,
            "foundation_model_detail_w81": foundation_detail,
            "model_support_contexts_w57": num(w57.get("support_contexts"), 0.0) if w57 is not None else 0.0,
            "model_strong_contexts_w57": num(w57.get("strong_support_contexts"), 0.0) if w57 is not None else 0.0,
            "wave57_call": clean(w57.get("wave57_call")) if w57 is not None else "",
            "best_model_context": clean(w57.get("best_context")) if w57 is not None else "",
            "best_model_z": num(w57.get("best_cosine_shift_z_vs_random")) if w57 is not None else math.nan,
            "best_model_projection": num(w57.get("best_projection_minus_random")) if w57 is not None else math.nan,
            "reachability_score": num(w83.get("reachability_score"), 0.0) if w83 is not None else 0.0,
            "intervention_class": clean(w83.get("intervention_class")) if w83 is not None else "",
            "chembl_activity_count": num(w83.get("chembl_activity_count"), 0.0) if w83 is not None else 0.0,
            "chembl_target_id": clean(w83.get("chembl_target_id")) if w83 is not None else "",
            "manual_prior_blocked": flag(w83.get("manual_prior_blocked")) if w83 is not None else False,
            "cross_autoimmune_score_w83": num(w83.get("cross_autoimmune_score"), 0.0) if w83 is not None else 0.0,
            "genetic_breadth_disease_count": num(w83.get("genetic_breadth_disease_count"), 0.0) if w83 is not None else (
                num(w57.get("n_diseases_genetic_ge_0_25"), 0.0) if w57 is not None else 0.0
            ),
            "genetic_breadth_diseases": clean(w83.get("genetic_breadth_diseases")) if w83 is not None else clean(w57.get("diseases_genetic_ge_0_25")) if w57 is not None else "",
            "qtl_breadth_disease_count": num(w83.get("qtl_breadth_disease_count"), 0.0) if w83 is not None else 0.0,
            "wave62_strong_l2g_disease_count": num(w62.get("strong_l2g_disease_count"), 0.0) if w62 is not None else 0.0,
            "wave62_strong_qtl_coloc_disease_count": num(w62.get("strong_qtl_coloc_disease_count"), 0.0) if w62 is not None else 0.0,
            "ms_genetic_score": max(
                num(w83.get("ms_genetic_score"), 0.0) if w83 is not None else 0.0,
                num(w57.get("ms_genetic_association"), 0.0) if w57 is not None else 0.0,
                num(w62.get("ms_max_l2g_score"), 0.0) if w62 is not None else 0.0,
            ),
            "ms_expr_delta": max(
                num(w81.get("ms_delta_log2"), -999.0) if w81 is not None else -999.0,
                num(w83.get("ms_expr_delta"), -999.0) if w83 is not None else -999.0,
                num(w57.get("ms_wm_delta_log2"), -999.0) if w57 is not None else -999.0,
                num(w91.get("ms_wm_delta_log2"), -999.0) if w91 is not None else -999.0,
                num(w94.get("ms_wm_delta_log2"), -999.0) if w94 is not None else -999.0,
            ),
            "ms_expr_p": min(
                num(w81.get("ms_p"), 1.0) if w81 is not None else 1.0,
                num(w83.get("ms_expr_p"), 1.0) if w83 is not None else 1.0,
                num(w57.get("ms_wm_p"), 1.0) if w57 is not None else 1.0,
                num(w91.get("ms_wm_p"), 1.0) if w91 is not None else 1.0,
                num(w94.get("ms_wm_p"), 1.0) if w94 is not None else 1.0,
            ),
            "positive_disease_count": max(
                num(w81.get("broad_positive_disease_count"), 0.0) if w81 is not None else 0.0,
                num(w83.get("positive_disease_count"), 0.0) if w83 is not None else 0.0,
                num(w57.get("positive_disease_count"), 0.0) if w57 is not None else 0.0,
                num(w91.get("direct_positive_p05_disease_count"), 0.0) if w91 is not None else 0.0,
                num(w94.get("positive_disease_count"), 0.0) if w94 is not None else 0.0,
            ),
            "positive_diseases": clean(w83.get("positive_diseases"))
            if w83 is not None
            else clean(w81.get("broad_positive_diseases"))
            if w81 is not None
            else clean(w57.get("positive_diseases"))
            if w57 is not None
            else clean(w94.get("positive_diseases"))
            if w94 is not None
            else "",
            "negative_disease_count": max(
                num(w94.get("negative_disease_count"), 0.0) if w94 is not None else 0.0,
                num(w91.get("direct_negative_p05_disease_count"), 0.0) if w91 is not None else 0.0,
            ),
            "retained_residual_disease_count": max(
                num(w57.get("retained_positive_disease_count"), 0.0) if w57 is not None else 0.0,
                num(w102.get("retained_positive_disease_count"), 0.0) if w102 is not None else 0.0,
            ),
            "strict_residual_disease_count": max(
                num(w57.get("strict_core_covariate_surviving_disease_count"), 0.0) if w57 is not None else 0.0,
                num(w102.get("strict_core_covariate_surviving_disease_count"), 0.0) if w102 is not None else 0.0,
            ),
            "response_nonresponse_high_context_count": num(w91.get("response_nonresponse_high_context_count"), 0.0) if w91 is not None else 0.0,
            "response_nominal_or_trend_context_count": num(w91.get("response_nominal_or_trend_context_count"), 0.0) if w91 is not None else 0.0,
            "ibd_response_fdr10": max(
                num(w81.get("ibd_response_fdr10"), 0.0) if w81 is not None else 0.0,
                1.0 if (w57 is not None and clean(w57.get("ibd_wave86_call")).startswith("GENE_LEVEL")) else 0.0,
            ),
            "efferocytosis_screen_call": clean(w37.get("screen_call")) if w37 is not None else "",
            "efferocytosis_contrast_lfc": num(w37.get("median_efficient_minus_noneater_lfc")) if w37 is not None else math.nan,
            "efferocytosis_contrast_fdr": num(w37.get("contrast_fdr"), 1.0) if w37 is not None else 1.0,
            "wave91_call": clean(w91.get("wave91_call")) if w91 is not None else "",
            "wave83_call": clean(w83.get("wave83_call")) if w83 is not None else "",
            "wave62_call": clean(w62.get("wave62_call")) if w62 is not None else "",
        }
        rows.append(rec)
    return pd.DataFrame(rows)


def add_calls(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in [
        "direct_perturbation",
        "foundation_model_support_w81",
        "model_support_contexts_w57",
        "model_strong_contexts_w57",
        "reachability_score",
        "chembl_activity_count",
        "genetic_breadth_disease_count",
        "qtl_breadth_disease_count",
        "wave62_strong_l2g_disease_count",
        "wave62_strong_qtl_coloc_disease_count",
        "ms_genetic_score",
        "ms_expr_delta",
        "ms_expr_p",
        "positive_disease_count",
        "negative_disease_count",
        "retained_residual_disease_count",
        "strict_residual_disease_count",
        "response_nonresponse_high_context_count",
        "response_nominal_or_trend_context_count",
        "ibd_response_fdr10",
    ]:
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)

    out["has_direct_perturbation"] = out["direct_perturbation"] > 0
    out["has_foundation_support"] = (
        (out["foundation_model_support_w81"] > 0)
        | (out["model_strong_contexts_w57"] >= 1)
        | (out["model_support_contexts_w57"] >= 2)
    )
    out["has_nonexpression_anchor"] = (
        out["has_direct_perturbation"]
        | out["has_foundation_support"]
        | (out["genetic_breadth_disease_count"] >= 4)
        | (out["wave62_strong_l2g_disease_count"] >= 2)
        | (out["wave62_strong_qtl_coloc_disease_count"] >= 2)
        | (out["chembl_activity_count"] >= 25)
    )
    out["ms_anchor"] = ((out["ms_expr_delta"] > 0.25) & (out["ms_expr_p"] < 0.10)) | (out["ms_genetic_score"] >= 0.5)
    out["cross_disease_anchor"] = (
        (out["positive_disease_count"] >= 3)
        | (out["genetic_breadth_disease_count"] >= 4)
        | (out["retained_residual_disease_count"] >= 2)
    )
    out["direction_or_response_support"] = (
        out["has_direct_perturbation"]
        | (out["response_nonresponse_high_context_count"] >= 2)
        | (out["ibd_response_fdr10"] > 0)
        | out["has_foundation_support"]
    )
    out["reachable_modality"] = (
        (out["reachability_score"] >= 3)
        | (out["chembl_activity_count"] >= 25)
        | out["intervention_class"].str.contains("receptor|enzyme|kinase|phospho|surface|transporter|lysosomal", case=False, na=False)
    )
    out["prior_or_safety_blocked"] = out["manual_prior_blocked"] | out["closure_text"].str.contains(PRIOR_BLOCK_RE, na=False)
    out["wrong_direction_or_undruggable"] = out["closure_text"].str.contains(
        r"wrong.?direction|restoration|not druggable|no actionable modality|unclear|unresolved|poor", case=False, na=False
    )
    out["expression_only"] = ~out["has_nonexpression_anchor"]

    out["wave103_score"] = (
        out["has_direct_perturbation"].astype(int) * 4
        + out["has_foundation_support"].astype(int) * 3
        + out["ms_anchor"].astype(int) * 3
        + out["cross_disease_anchor"].astype(int) * 3
        + out["direction_or_response_support"].astype(int) * 2
        + out["reachable_modality"].astype(int) * 2
        + out["genetic_breadth_disease_count"].clip(upper=8) * 0.5
        + out["retained_residual_disease_count"].clip(upper=4) * 0.75
        + out["strict_residual_disease_count"].clip(upper=3) * 1.5
        + out["positive_disease_count"].clip(upper=5) * 0.4
        - out["negative_disease_count"].clip(upper=3) * 1.5
        - out["prior_or_safety_blocked"].astype(int) * 4
        - out["wrong_direction_or_undruggable"].astype(int) * 2
        - out["expression_only"].astype(int) * 3
    )

    required = [
        "has_nonexpression_anchor",
        "ms_anchor",
        "cross_disease_anchor",
        "direction_or_response_support",
        "reachable_modality",
    ]
    out["wave103_gate_count"] = out[required].sum(axis=1).astype(int)
    missing = []
    calls = []
    for _, row in out.iterrows():
        missing_gates = [g for g in required if not bool(row[g])]
        missing.append(";".join(missing_gates))
        if not bool(row["has_nonexpression_anchor"]):
            calls.append("NO_GO_EXPRESSION_OR_CLASS_ONLY")
        elif bool(row["prior_or_safety_blocked"]):
            calls.append("NO_GO_PRIOR_OR_SAFETY_BLOCKED")
        elif bool(row["wrong_direction_or_undruggable"]):
            calls.append("NO_GO_WRONG_DIRECTION_OR_UNDRUGGABLE")
        elif not bool(row["ms_anchor"]):
            calls.append("NO_GO_NO_MS_ANCHOR")
        elif not bool(row["cross_disease_anchor"]):
            calls.append("NO_GO_NO_CROSS_DISEASE_ANCHOR")
        elif not bool(row["direction_or_response_support"]):
            calls.append("NO_GO_NO_DIRECTIONAL_SUPPORT")
        elif not bool(row["reachable_modality"]):
            calls.append("PARK_NEEDS_MODALITY")
        elif row["wave103_gate_count"] >= 5:
            calls.append("REOPEN_FOR_ROUTE_SPECIFIC_SIDECARE")
        else:
            calls.append("PARK_INCOMPLETE_INTERVENTION_FIRST")
    out["wave103_missing_gates"] = missing
    out["wave103_call"] = calls
    priority = {
        "REOPEN_FOR_ROUTE_SPECIFIC_SIDECARE": 0,
        "PARK_NEEDS_MODALITY": 1,
        "PARK_INCOMPLETE_INTERVENTION_FIRST": 2,
        "NO_GO_WRONG_DIRECTION_OR_UNDRUGGABLE": 3,
        "NO_GO_NO_MS_ANCHOR": 4,
        "NO_GO_NO_CROSS_DISEASE_ANCHOR": 5,
        "NO_GO_NO_DIRECTIONAL_SUPPORT": 6,
        "NO_GO_PRIOR_OR_SAFETY_BLOCKED": 7,
        "NO_GO_EXPRESSION_OR_CLASS_ONLY": 8,
    }
    out["wave103_call_priority"] = out["wave103_call"].map(priority).fillna(99).astype(int)
    return out.sort_values(["wave103_call_priority", "wave103_score"], ascending=[True, False])


def write_report(rank: pd.DataFrame, summary: dict[str, Any]) -> None:
    cols = [
        "gene",
        "wave103_call",
        "wave103_score",
        "wave103_gate_count",
        "has_direct_perturbation",
        "has_foundation_support",
        "ms_anchor",
        "cross_disease_anchor",
        "reachable_modality",
        "prior_or_safety_blocked",
        "wrong_direction_or_undruggable",
        "intervention_class",
        "positive_disease_count",
        "genetic_breadth_disease_count",
        "ms_expr_delta",
        "ms_expr_p",
        "ms_genetic_score",
        "model_support_contexts_w57",
        "model_strong_contexts_w57",
        "direct_perturbation_detail",
        "chembl_activity_count",
        "manual_route",
        "manual_blocker",
        "wave103_missing_gates",
    ]
    top = rank[cols].head(40)
    reopened = rank[rank["wave103_call"].eq("REOPEN_FOR_ROUTE_SPECIFIC_SIDECARE")]
    report = f"""# Wave103 Intervention-First Successor Triage

## Bottom Line

Branch call: `{summary["branch_call"]}`.

This wave starts from non-expression anchors rather than marker recurrence. It
does not yet produce a therapeutic finding. It identifies candidates that are
worth route-specific sidecars only if they have perturbation/model/genetic or
druggability evidence before expression is considered.

## Reopened / Top Candidates

{markdown_table(top, max_rows=40)}

## Interpretation

- High-scoring prior-art-heavy nodes remain blocked even when genetics and
  druggability are strong. This prevents the run from rediscovering IL7R,
  CXCR2, TYK2, IL23R, PTPN2, or broad MHC/cytokine axes as supposedly novel.
- Direct perturbation-only candidates such as `DAB2` and `CD9` are useful
  biology, but they still fail as translational targets if modality and
  direction cannot be made plausible.
- Candidates reopened by this wave require sidecar validation. The score is a
  dispatch tool, not a claim.

## Dispatch Recommendation

{", ".join(reopened["gene"].head(8).tolist()) if not reopened.empty else "No immediate route-specific sidecar candidate survived all gates."}

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave103_intervention_first_successor_triage.py")}`
- Rank table: `{rel(OUT / "intervention_first_successor_rank.tsv")}`
- Summary: `{rel(OUT / "summary.json")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    tables = {
        "w81": read_tsv(W81),
        "w57": read_tsv(W57),
        "w83": read_tsv(W83),
        "w91": read_tsv(W91),
        "w94": read_tsv(W94),
        "w102": read_tsv(W102),
        "w37": read_tsv(W37),
        "w62": read_tsv(W62),
    }
    rank = add_calls(collect(tables))
    rank.to_csv(OUT / "intervention_first_successor_rank.tsv", sep="\t", index=False)
    reopened = rank[rank["wave103_call"].eq("REOPEN_FOR_ROUTE_SPECIFIC_SIDECARE")]
    summary = {
        "random_seed": SEED,
        "branch_call": "REOPEN_INTERVENTION_FIRST_SIDECARE_CANDIDATES" if not reopened.empty else "NO_INTERVENTION_FIRST_SUCCESSOR_SURVIVES_ALL_GATES",
        "n_candidates": int(len(rank)),
        "call_counts": rank["wave103_call"].value_counts().to_dict(),
        "reopened_candidates": reopened["gene"].head(20).tolist(),
        "top_parked_or_no_go": rank.head(20)["gene"].tolist(),
        "inputs": {
            "wave81": rel(W81),
            "wave57": rel(W57),
            "wave83": rel(W83),
            "wave91": rel(W91),
            "wave94": rel(W94),
            "wave102": rel(W102),
            "wave37": rel(W37),
            "wave62": rel(W62),
        },
    }
    write_json(OUT / "summary.json", summary)
    write_report(rank, summary)


if __name__ == "__main__":
    main()
