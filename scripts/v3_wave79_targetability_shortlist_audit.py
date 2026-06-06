#!/usr/bin/env python3
"""Wave79 non-LILRB targetability shortlist audit.

Question:
After LILRB closure, do any of the Wave75-C non-LILRB targetability scouts
(`CD58`, `SPNS1`, `P4HB`, `SEL1L3`) survive a target-level, anti-proxy audit?

This script reuses the Wave78 patient-level RA/IBD response machinery but
changes the biology and gates. The shortlist must show target-level support,
not merely expression recurrence: MS/genetic anchor, APC/myeloid localization
or a justified target tissue, response specificity beyond generic inflammation,
residual-survival support, model/perturbation evidence, and a realistic
intervention route.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

import v3_wave78_lilrb_inhibitory_receptor_audit as w78
from v3_analyze_direct_h5ad_cell_states import ROOT


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave79_targetability_shortlist_audit"

TARGET_GENES = ["CD58", "SPNS1", "P4HB", "SEL1L3"]
BENCHMARK_GENES = ["IFI30"]
GENES = TARGET_GENES + BENCHMARK_GENES

W21 = ROOT / "phases/v3/results" / "wave21_residual_druggability_scan" / "wave21_residual_druggability_ranked_full.tsv"
W39 = ROOT / "phases/v3/results" / "wave39_surfaceome_rescue_after_resolution_pivot" / "surfaceome_rescue_rank_full.tsv"
W71 = ROOT / "phases/v3/results" / "wave71_global_survivor_meta_rank" / "global_survivor_meta_rank.tsv"
W18_RANK = ROOT / "phases/v3/results" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv"
W18_GENEFORMER = ROOT / "phases/v3/results" / "wave18_foundation_rescue" / "geneformer_consolidated_context_metrics.tsv"


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
    return w78.markdown_table(df, max_rows=max_rows)


def rows_for_genes(path: Path) -> pd.DataFrame:
    df = read_tsv(path)
    if df.empty:
        return df
    gene_col = None
    for col in ["gene", "candidate", "gene_symbol", "target_gene"]:
        if col in df.columns:
            gene_col = col
            break
    if gene_col is None:
        return pd.DataFrame()
    out = df[df[gene_col].astype(str).str.upper().isin(GENES)].copy()
    if not out.empty:
        out[gene_col] = out[gene_col].astype(str).str.upper()
    return out


def configure_wave78_gene_set() -> None:
    """Reuse Wave78 data loaders with the Wave79 gene set."""
    w78.TARGET_GENES = TARGET_GENES
    w78.COMPARATOR_GENES = BENCHMARK_GENES
    w78.GENES = GENES


def compartment_summary(broad_rows: pd.DataFrame) -> pd.DataFrame:
    if broad_rows.empty:
        return pd.DataFrame()
    rows = []
    apc_pattern = r"myeloid|apc|mono|macrophage|dendritic|microglia"
    non_target_pattern = r"epithelial|stromal|endothelial|ductal|acinar|keratinocyte|stellate"
    for gene, sub in broad_rows.groupby("gene", observed=True):
        pos = sub[sub["nominal_positive"]].copy()
        apc = pos[
            pos["compartment"].astype(str).str.contains(apc_pattern, case=False, regex=True, na=False)
            | pos["role"].astype(str).str.contains(apc_pattern, case=False, regex=True, na=False)
            | pos["analysis"].astype(str).str.contains(apc_pattern, case=False, regex=True, na=False)
        ]
        nontarget = pos[
            pos["compartment"].astype(str).str.contains(non_target_pattern, case=False, regex=True, na=False)
            | pos["analysis"].astype(str).str.contains(non_target_pattern, case=False, regex=True, na=False)
        ]
        rows.append(
            {
                "gene": gene,
                "positive_contexts": int(pos.shape[0]),
                "apc_myeloid_positive_contexts": int(apc.shape[0]),
                "apc_myeloid_positive_disease_count": int(apc["disease_name"].nunique()),
                "apc_myeloid_positive_diseases": ";".join(sorted(apc["disease_name"].astype(str).unique())),
                "non_target_positive_contexts": int(nontarget.shape[0]),
                "non_target_positive_disease_count": int(nontarget["disease_name"].nunique()),
                "non_target_positive_diseases": ";".join(sorted(nontarget["disease_name"].astype(str).unique())),
                "top_positive_contexts": ";".join(
                    pos.sort_values("p")
                    .head(8)
                    .apply(
                        lambda r: f"{r['analysis']}:{r['delta_log2_cpm']:.3g},p={r['p']:.3g}",
                        axis=1,
                    )
                    .tolist()
                ),
            }
        )
    return pd.DataFrame(rows).sort_values(["apc_myeloid_positive_disease_count", "positive_contexts"], ascending=[False, False])


def foundation_summary(geneformer_rows: pd.DataFrame, rank_rows: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gene in GENES:
        gf = geneformer_rows[geneformer_rows.get("gene", pd.Series(dtype=str)).astype(str).str.upper().eq(gene)].copy() if not geneformer_rows.empty and "gene" in geneformer_rows.columns else pd.DataFrame()
        rr = rank_rows[rank_rows.get("gene", pd.Series(dtype=str)).astype(str).str.upper().eq(gene)].copy() if not rank_rows.empty and "gene" in rank_rows.columns else pd.DataFrame()
        supportive = 0
        do_not_promote = 0
        best_context = ""
        best_projection = np.nan
        if not gf.empty:
            text = " ".join(gf.astype(str).agg(" ".join, axis=1).tolist()).lower()
            supportive = int("positive_shift" in text or "supportive" in text)
            do_not_promote = int("do_not_promote" in text or "token_not_detected" in text)
            proj_cols = [c for c in gf.columns if "projection" in c or "effect" in c or "shift" in c]
            if "context" in gf.columns:
                best_context = str(gf.iloc[0]["context"])
            elif "cell_context" in gf.columns:
                best_context = str(gf.iloc[0]["cell_context"])
            for col in proj_cols:
                vals = pd.to_numeric(gf[col], errors="coerce")
                if vals.notna().any():
                    idx = vals.abs().idxmax()
                    best_projection = float(vals.loc[idx])
                    break
        if not rr.empty:
            text = " ".join(rr.astype(str).agg(" ".join, axis=1).tolist()).lower()
            do_not_promote = int(do_not_promote or "do_not_promote" in text or "model_only_no_real_perturbation" in text)
            supportive = int(supportive or "supportive" in text)
        rows.append(
            {
                "gene": gene,
                "foundation_rows": int(gf.shape[0] + rr.shape[0]),
                "foundation_supportive_text": supportive,
                "foundation_do_not_promote_text": do_not_promote,
                "best_context": best_context,
                "best_projection_like_value": best_projection,
            }
        )
    return pd.DataFrame(rows)


def row_by_gene(df: pd.DataFrame, gene_col: str = "gene") -> dict[str, dict[str, Any]]:
    if df.empty or gene_col not in df.columns:
        return {}
    out: dict[str, dict[str, Any]] = {}
    for gene, sub in df.groupby(gene_col, observed=True):
        out[str(gene).upper()] = sub.iloc[0].to_dict()
    return out


def decision_table(
    broad_sum: pd.DataFrame,
    compartments: pd.DataFrame,
    ms: pd.DataFrame,
    w62: pd.DataFrame,
    qtl_summary: pd.DataFrame,
    conv: pd.DataFrame,
    w21: pd.DataFrame,
    w39: pd.DataFrame,
    w71: pd.DataFrame,
    foundation: pd.DataFrame,
) -> pd.DataFrame:
    broad_by = row_by_gene(broad_sum)
    comp_by = row_by_gene(compartments)
    ms_by = row_by_gene(ms)
    w62_by = row_by_gene(w62)
    qtl_by = row_by_gene(qtl_summary)
    w21_by = row_by_gene(w21)
    w39_by = row_by_gene(w39)
    w71_by = row_by_gene(w71)
    foundation_by = row_by_gene(foundation)
    conv_by: dict[str, dict[str, Any]] = {}
    if not conv.empty:
        for gene, sub in conv.groupby("gene", observed=True):
            conv_by[str(gene).upper()] = sub.sort_values(["priority", "ra_p", "ibd_p"], ascending=[False, True, True]).iloc[0].to_dict()

    rows = []
    for gene in GENES:
        b = broad_by.get(gene, {})
        c = comp_by.get(gene, {})
        m = ms_by.get(gene, {})
        s = w62_by.get(gene, {})
        q = qtl_by.get(gene, {})
        r = conv_by.get(gene, {})
        d21 = w21_by.get(gene, {})
        d39 = w39_by.get(gene, {})
        d71 = w71_by.get(gene, {})
        f = foundation_by.get(gene, {})

        ms_expr_anchor = bool(m.get("delta_log2", np.nan) >= 0.35 and m.get("p", 1.0) <= 0.05)
        ms_genetic_anchor = bool(s.get("ms_max_l2g_score", 0.0) >= 0.5 or q.get("ms_max_h4", 0.0) >= 0.8)
        gate_ms_anchor = int(ms_expr_anchor or ms_genetic_anchor)
        gate_ms_guardrail = int(not bool(m.get("delta_log2", 0.0) <= -0.35 and m.get("p", 1.0) <= 0.05))
        gate_breadth = int(b.get("positive_disease_count", 0) >= 3)
        gate_apc_myeloid = int(c.get("apc_myeloid_positive_disease_count", 0) >= 2)
        gate_response = int(bool(r.get("response_specificity_pass", False)))
        gate_genetics = int(
            not str(s.get("wave62_call", "NO_GO")).startswith("NO_GO")
            or q.get("strong_h4_disease_count", 0) >= 2
            or d71.get("genetics_channel_count", 0) >= 2
        )
        strict_resid = max(
            float(d21.get("strict_core_covariate_surviving_disease_count", 0) or 0),
            float(s.get("strict_core_covariate_surviving_disease_count", 0) or 0),
            float(s.get("residual_retained_disease_count", 0) or 0),
        )
        gate_residual = int(strict_resid >= 2)
        foundation_ok = bool(f.get("foundation_supportive_text", 0) and not f.get("foundation_do_not_promote_text", 0))
        perturbation_channel = int(d71.get("perturbation_channel_count", 0) or 0)
        gate_model_perturb = int(foundation_ok or perturbation_channel >= 1)
        chembl_count = float(d39.get("chembl_activity_count", d21.get("chembl_nM_activity_count", 0)) or 0)
        accessible = bool(d39.get("uniprot_accessible", False) or d21.get("wave21_modality_read", "") == "accessible_biologic_or_surface")
        if gene == "CD58":
            modality_strength = "surface_biologic_possible"
            gate_modality = 1
        elif gene == "P4HB" and chembl_count > 0:
            modality_strength = "chembl_enzyme_but_broad_er_redox"
            gate_modality = 1
        elif gene == "SPNS1":
            modality_strength = "lysosomal_transporter_no_chemical_matter"
            gate_modality = 0
        elif gene == "SEL1L3":
            modality_strength = "undercharacterized_membrane_marker"
            gate_modality = 0
        elif gene == "IFI30":
            modality_strength = "benchmark_antigen_processing_no_clean_modality"
            gate_modality = 0
        else:
            modality_strength = "unknown"
            gate_modality = int(accessible or chembl_count > 0)

        prior_text = " ".join(
            [
                str(d21.get("wave21_call", "")),
                str(d21.get("wave21_failures", "")),
                str(d39.get("wave39_call", "")),
                str(d39.get("wave39_reason", "")),
                str(d71.get("wave71_call", "")),
                str(d71.get("blockers", "")),
                str(s.get("manual_blocker", "")),
                str(s.get("prior_context_blocker", "")),
            ]
        )
        gate_prior_not_blocked = int(
            "NO_GO" not in prior_text
            and "DEMOTE" not in prior_text
            and "direct_antigen_processing_host_defense" not in prior_text
        )

        gate_count = sum(
            [
                gate_ms_anchor,
                gate_ms_guardrail,
                gate_breadth,
                gate_apc_myeloid,
                gate_response,
                gate_genetics,
                gate_residual,
                gate_model_perturb,
                gate_modality,
                gate_prior_not_blocked,
            ]
        )
        if gene in TARGET_GENES and gate_count >= 7 and gate_ms_anchor and gate_response and gate_modality and gate_prior_not_blocked:
            call = "REOPEN_TARGETABILITY_SHORTLIST_NODE"
            reason = "shortlist node passes strict targetability gates"
        elif gene in TARGET_GENES and gate_count >= 4:
            call = "PARK_TARGETABILITY_SHORTLIST_NODE"
            reason = "partial support remains but one or more critical targetability gates fail"
        else:
            call = "NO_GO_TARGETABILITY_SHORTLIST_NODE"
            reason = "insufficient target-level convergence after strict gates"

        rows.append(
            {
                "gene": gene,
                "wave79_call": call,
                "gate_count": gate_count,
                "gate_ms_anchor": gate_ms_anchor,
                "gate_ms_nonnegative_guardrail": gate_ms_guardrail,
                "gate_breadth_ge3": gate_breadth,
                "gate_apc_myeloid_ge2": gate_apc_myeloid,
                "gate_adjusted_ra_ibd_response_specific": gate_response,
                "gate_genetics_or_target_resolution": gate_genetics,
                "gate_residual_survival": gate_residual,
                "gate_model_or_perturbation": gate_model_perturb,
                "gate_modality": gate_modality,
                "gate_prior_not_blocked": gate_prior_not_blocked,
                "positive_disease_count": b.get("positive_disease_count", 0),
                "positive_diseases": b.get("positive_diseases", ""),
                "apc_myeloid_positive_disease_count": c.get("apc_myeloid_positive_disease_count", 0),
                "apc_myeloid_positive_diseases": c.get("apc_myeloid_positive_diseases", ""),
                "non_target_positive_disease_count": c.get("non_target_positive_disease_count", 0),
                "ms_delta_log2": m.get("delta_log2", np.nan),
                "ms_p": m.get("p", np.nan),
                "ms_fdr": m.get("fdr", np.nan),
                "ms_max_l2g_score": s.get("ms_max_l2g_score", np.nan),
                "qtl_strong_h4_disease_count": q.get("strong_h4_disease_count", 0),
                "qtl_strong_h4_diseases": q.get("strong_h4_diseases", ""),
                "best_response_endpoint": r.get("endpoint", ""),
                "ra_response_p": r.get("ra_p", np.nan),
                "ibd_response_p": r.get("ibd_p", np.nan),
                "ra_target_generic_abs_ratio": r.get("ra_target_generic_abs_ratio", np.nan),
                "ibd_target_generic_abs_ratio": r.get("ibd_target_generic_abs_ratio", np.nan),
                "strict_residual_surviving_disease_count": strict_resid,
                "foundation_rows": f.get("foundation_rows", 0),
                "foundation_supportive_text": f.get("foundation_supportive_text", 0),
                "foundation_do_not_promote_text": f.get("foundation_do_not_promote_text", 0),
                "chembl_activity_count": chembl_count,
                "modality_strength": modality_strength,
                "wave62_call": s.get("wave62_call", ""),
                "wave39_call": d39.get("wave39_call", ""),
                "wave21_call": d21.get("wave21_call", ""),
                "wave71_call": d71.get("wave71_call", ""),
                "decision_reason": reason,
                "is_target_gene": gene in TARGET_GENES,
            }
        )
    out = pd.DataFrame(rows)
    return out.sort_values(["is_target_gene", "gate_count", "positive_disease_count"], ascending=[False, False, False])


def write_report(
    decision: pd.DataFrame,
    broad_sum: pd.DataFrame,
    compartments: pd.DataFrame,
    ms: pd.DataFrame,
    qtl_summary: pd.DataFrame,
    conv: pd.DataFrame,
    ra_models: pd.DataFrame,
    ibd_models: pd.DataFrame,
    w21: pd.DataFrame,
    w39: pd.DataFrame,
    w71: pd.DataFrame,
    foundation: pd.DataFrame,
) -> None:
    lines = [
        "# Wave79 Targetability Shortlist Audit",
        "",
        "## Question",
        "",
        "Do `CD58`, `SPNS1`, `P4HB`, or `SEL1L3` survive strict target-level",
        "gates after the LILRB branch failed?",
        "",
        "## Verdict",
        "",
        str(decision.iloc[0]["wave79_call"]) if not decision.empty else "NO_GO_NO_DECISION_ROWS",
        "",
        "## Integrated Decision",
        "",
        markdown_table(decision, max_rows=20),
        "",
        "## Broad Disease Summary",
        "",
        markdown_table(broad_sum, max_rows=20),
        "",
        "## Compartment Localization",
        "",
        markdown_table(compartments, max_rows=20),
        "",
        "## MS White-Matter Rows",
        "",
        markdown_table(ms, max_rows=20),
        "",
        "## QTL Colocalization Summary",
        "",
        markdown_table(qtl_summary, max_rows=20),
        "",
        "## Adjusted RA/IBD Response Convergence",
        "",
        markdown_table(conv, max_rows=40),
        "",
        "## RA Adjusted Models",
        "",
        markdown_table(
            ra_models.sort_values("response_p")[
                [
                    "gene",
                    "endpoint",
                    "comparison",
                    "n",
                    "response_coef",
                    "response_p",
                    "response_fdr",
                    "generic_response_coef",
                    "target_generic_abs_ratio",
                    "model_status",
                ]
            ]
            if not ra_models.empty
            else ra_models,
            max_rows=50,
        ),
        "",
        "## IBD Adjusted Models",
        "",
        markdown_table(
            ibd_models.sort_values("response_p")[
                [
                    "gene",
                    "cell_state",
                    "endpoint",
                    "n",
                    "response_coef",
                    "response_p",
                    "response_fdr",
                    "generic_response_coef",
                    "target_generic_abs_ratio",
                    "model_status",
                ]
            ]
            if not ibd_models.empty
            else ibd_models,
            max_rows=60,
        ),
        "",
        "## Wave21 Residual/Druggability Rows",
        "",
        markdown_table(w21, max_rows=20),
        "",
        "## Wave39 Surfaceome Rows",
        "",
        markdown_table(w39, max_rows=20),
        "",
        "## Wave71 Global Survivor Rows",
        "",
        markdown_table(w71, max_rows=20),
        "",
        "## Foundation/Model Summary",
        "",
        markdown_table(foundation, max_rows=20),
        "",
        "## Interpretation",
        "",
        "A Wave79 survivor must be more than reachable or genetically interesting.",
        "The essential failure modes are T-cell/admixture signal (`CD58`), generic",
        "lysosomal or ER stress (`SPNS1`, `P4HB`), and undercharacterized marker",
        "biology (`SEL1L3`).",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    configure_wave78_gene_set()

    broad_rows, broad_sum = w78.broad_summary()
    compartments = compartment_summary(broad_rows)
    ms = w78.ms_rows()
    w62_summary, qtl_rows, qtl_summary = w78.wave62_rows()
    ra_pairs, ra_models_raw = w78.ra_pairs_and_models()
    ibd_pairs, ibd_models_raw = w78.ibd_pairs_and_models()
    generic = w78.generic_reference_coefficients(ra_pairs, ibd_pairs)
    ra_models = w78.add_generic_ratios(ra_models_raw, generic)
    ibd_models = w78.add_generic_ratios(ibd_models_raw, generic)
    conv = w78.response_convergence(ra_models, ibd_models)
    w21 = rows_for_genes(W21)
    w39 = rows_for_genes(W39)
    w71 = rows_for_genes(W71)
    rank_rows = rows_for_genes(W18_RANK)
    geneformer_rows = rows_for_genes(W18_GENEFORMER)
    foundation = foundation_summary(geneformer_rows, rank_rows)
    decision = decision_table(broad_sum, compartments, ms, w62_summary, qtl_summary, conv, w21, w39, w71, foundation)

    broad_rows.to_csv(OUT / "targetability_broad_context_rows.tsv", sep="\t", index=False)
    broad_sum.to_csv(OUT / "targetability_broad_gene_summary.tsv", sep="\t", index=False)
    compartments.to_csv(OUT / "targetability_compartment_summary.tsv", sep="\t", index=False)
    ms.to_csv(OUT / "targetability_ms_white_matter_rows.tsv", sep="\t", index=False)
    w62_summary.to_csv(OUT / "targetability_wave62_summary_rows.tsv", sep="\t", index=False)
    qtl_rows.to_csv(OUT / "targetability_qtl_coloc_rows.tsv", sep="\t", index=False)
    qtl_summary.to_csv(OUT / "targetability_qtl_coloc_summary.tsv", sep="\t", index=False)
    ra_pairs.to_csv(OUT / "targetability_ra_patient_pairs.tsv", sep="\t", index=False)
    ibd_pairs.to_csv(OUT / "targetability_ibd_patient_pairs.tsv", sep="\t", index=False)
    generic.to_csv(OUT / "generic_reference_models.tsv", sep="\t", index=False)
    ra_models.to_csv(OUT / "targetability_ra_adjusted_models.tsv", sep="\t", index=False)
    ibd_models.to_csv(OUT / "targetability_ibd_adjusted_models.tsv", sep="\t", index=False)
    conv.to_csv(OUT / "targetability_adjusted_response_convergence.tsv", sep="\t", index=False)
    w21.to_csv(OUT / "targetability_wave21_rows.tsv", sep="\t", index=False)
    w39.to_csv(OUT / "targetability_wave39_rows.tsv", sep="\t", index=False)
    w71.to_csv(OUT / "targetability_wave71_rows.tsv", sep="\t", index=False)
    geneformer_rows.to_csv(OUT / "targetability_geneformer_rows.tsv", sep="\t", index=False)
    rank_rows.to_csv(OUT / "targetability_foundation_rank_rows.tsv", sep="\t", index=False)
    foundation.to_csv(OUT / "targetability_foundation_summary.tsv", sep="\t", index=False)
    decision.to_csv(OUT / "targetability_integrated_decision.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "inputs": {
            "broad": rel(w78.BROAD),
            "ms_signature": rel(w78.MS_SIG),
            "wave62_summary": rel(w78.W62),
            "wave62_qtl": rel(w78.W62_QTL),
            "wave21": rel(W21),
            "wave39": rel(W39),
            "wave71": rel(W71),
            "wave18_rank": rel(W18_RANK),
            "wave18_geneformer": rel(W18_GENEFORMER),
            "ra_counts": rel(w78.RA_COUNTS),
            "ra_meta": rel(w78.RA_META),
            "ibd_h5ad_loader": "v3_wave68_gse282122_unrestricted_gene_screen.load_inputs",
            "ibd_pair_meta": rel(w78.IBD_PAIR_META),
        },
        "targets": TARGET_GENES,
        "benchmark_genes": BENCHMARK_GENES,
        "decision": decision.replace({np.nan: None}).to_dict(orient="records"),
    }
    write_json(OUT / "summary.json", summary)
    write_report(decision, broad_sum, compartments, ms, qtl_summary, conv, ra_models, ibd_models, w21, w39, w71, foundation)


if __name__ == "__main__":
    main()
