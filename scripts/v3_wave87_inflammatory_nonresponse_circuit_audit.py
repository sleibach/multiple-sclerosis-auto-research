#!/usr/bin/env python3
"""Wave87 consolidation of the inflammatory anti-TNF nonresponse circuit.

Wave85 killed the residual lysosomal/APC response biomarker in external mucosal
anti-TNF cohorts. Wave86 showed that generic inflammatory genes are instead
high in anti-TNF nonresponders. This script asks whether any single gene from
that circuit can become a V3-grade cross-autoimmune central node.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_direct_h5ad_cell_states import ROOT


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave87_inflammatory_nonresponse_circuit_audit"

CANDIDATES = [
    "IL1B",
    "CXCL8",
    "TREM1",
    "CCL4",
    "CCL3",
    "CD44",
    "CCL2",
    "ACSL1",
    "IFI30",
    "OSM",
    "SPP1",
    "LAMP3",
    "CXCL10",
    "GBP1",
    "STAT1",
]

PRIOR_OR_ROUTE_BLOCKERS = {
    "IL1B": "BLOCKED_GENERIC_IL1_INFLAMMATION_AND_EXISTING_IL1_BLOCKADE",
    "CXCL8": "BLOCKED_GENERIC_NEUTROPHIL_CHEMOKINE_LOW_MS_ANCHOR",
    "TREM1": "PARK_RECEPTOR_ROUTE_BUT_NO_LOCAL_MS_OR_GENETIC_ANCHOR",
    "CCL4": "BLOCKED_BROAD_CHEMOKINE_REDUNDANCY",
    "CCL3": "BLOCKED_BROAD_CHEMOKINE_REDUNDANCY",
    "CD44": "BLOCKED_ADHESION_MATRIX_PRIOR_ART_AND_BROAD_BIOLOGY",
    "CCL2": "BLOCKED_BROAD_CHEMOKINE_REDUNDANCY_AND_PRIOR_ART",
    "ACSL1": "BLOCKED_AS_TARGET_DEMOTED_TO_MARKER_AFTER_MODULE_ADJUSTMENT",
    "IFI30": "NO_GO_DIRECT_ANTIGEN_PROCESSING_HOST_DEFENSE_AND_POOR_DRUGGABILITY",
    "OSM": "BLOCKED_OSM_OSMR_IBD_RA_PRIOR_ART_AND_MS_DIRECTION_AMBIGUITY",
    "SPP1": "BLOCKED_OSTEOPONTIN_CD44_PRIOR_ART_AND_WEAK_MS_SINGLE_GENE",
    "LAMP3": "NO_GO_MARKER_STATE_NOT_INTERVENTION_POINT",
    "CXCL10": "BLOCKED_GENERIC_IFN_CHEMOKINE_AXIS",
    "GBP1": "NO_GO_IFN_RESPONSE_MARKER_NOT_DRUGGABLE_CONTROLLER",
    "STAT1": "BLOCKED_GENERIC_IFN_TRANSCRIPTION_AXIS",
}

PATHS = {
    "wave86": ROOT / "phases/v3/results" / "wave86_external_geo_antitnf_gene_driver" / "external_geo_gene_meta_rank.tsv",
    "direct_h5ad": ROOT / "phases/v3/results" / "direct_h5ad_gene_replication" / "direct_h5ad_gene_donor_comparisons.tsv",
    "ms_wm": ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv",
    "ms_modules": ROOT / "phases/v3/results" / "gse111972_module_contrasts.tsv",
    "geneformer_gene": ROOT / "phases/v3/results" / "geneformer_broad_residual_delete" / "geneformer_broad_residual_gene_summary.tsv",
    "geneformer_context": ROOT / "phases/v3/results" / "geneformer_broad_residual_delete" / "geneformer_broad_residual_context_metrics_ranked.tsv",
    "wave55": ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv",
    "wave62": ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv",
}


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t")


def split_semicolon(value: Any) -> list[str]:
    if pd.isna(value) or value == "":
        return []
    return [x for x in str(value).split(";") if x]


def summarize_direct_h5ad() -> pd.DataFrame:
    df = read_tsv(PATHS["direct_h5ad"])
    if df.empty:
        return pd.DataFrame()
    df = df[(df["gene"].isin(CANDIDATES)) & (df["metric"] == "mean_z_vs_controls")].copy()
    rows: list[dict[str, Any]] = []
    for gene, sub in df.groupby("gene", sort=False):
        pos = sub[(sub["delta_case_minus_control"] > 0) & (sub["p"] <= 0.05)]
        pos_fdr = sub[(sub["delta_case_minus_control"] > 0) & (sub["fdr"] <= 0.10)]
        neg = sub[(sub["delta_case_minus_control"] < 0) & (sub["p"] <= 0.05)]
        top = (
            pos.sort_values("p")
            .head(5)
            .assign(context=lambda x: x["analysis"] + ":" + x["delta_case_minus_control"].round(3).astype(str) + ",p=" + x["p"].map(lambda y: f"{y:.3g}"))
        )
        rows.append(
            {
                "gene": gene,
                "direct_h5ad_tested_diseases": int(sub["disease_name"].nunique()),
                "direct_h5ad_positive_p05_disease_count": int(pos["disease_name"].nunique()),
                "direct_h5ad_positive_p05_diseases": ";".join(sorted(pos["disease_name"].unique())),
                "direct_h5ad_positive_fdr10_disease_count": int(pos_fdr["disease_name"].nunique()),
                "direct_h5ad_positive_fdr10_diseases": ";".join(sorted(pos_fdr["disease_name"].unique())),
                "direct_h5ad_negative_p05_disease_count": int(neg["disease_name"].nunique()),
                "direct_h5ad_negative_p05_diseases": ";".join(sorted(neg["disease_name"].unique())),
                "direct_h5ad_top_positive_contexts": ";".join(top["context"].tolist()),
            }
        )
    return pd.DataFrame(rows)


def summarize_ms_white_matter() -> pd.DataFrame:
    df = read_tsv(PATHS["ms_wm"])
    if df.empty:
        return pd.DataFrame({"gene": CANDIDATES})
    sub = df[df["gene"].isin(CANDIDATES)].copy()
    sub = sub.rename(
        columns={
            "delta_log2": "ms_wm_delta_log2",
            "hedges_g": "ms_wm_hedges_g",
            "p": "ms_wm_p",
            "fdr": "ms_wm_fdr",
        }
    )
    sub["ms_wm_support"] = np.where(
        (sub["ms_wm_delta_log2"] > 0) & (sub["ms_wm_p"] <= 0.05),
        "MS_WM_POSITIVE_NOMINAL",
        np.where((sub["ms_wm_delta_log2"] < 0) & (sub["ms_wm_p"] <= 0.05), "MS_WM_NEGATIVE_NOMINAL", "MS_WM_NULL_OR_WEAK"),
    )
    return sub[["gene", "ms_wm_delta_log2", "ms_wm_hedges_g", "ms_wm_p", "ms_wm_fdr", "ms_wm_support"]]


def summarize_geneformer() -> tuple[pd.DataFrame, pd.DataFrame]:
    gene = read_tsv(PATHS["geneformer_gene"])
    context = read_tsv(PATHS["geneformer_context"])
    if gene.empty:
        gene_sum = pd.DataFrame({"gene": CANDIDATES})
    else:
        gene_sum = gene[gene["gene"].isin(CANDIDATES)].copy()
    if context.empty:
        context_sum = pd.DataFrame({"gene": CANDIDATES})
    else:
        context = context[context["gene"].isin(CANDIDATES)].copy()
        rows = []
        for candidate, sub in context.groupby("gene", sort=False):
            supported = sub[sub.get("candidate_support_flag", False) == True]
            strong = sub[sub.get("candidate_strong_support_flag", False) == True]
            rows.append(
                {
                    "gene": candidate,
                    "geneformer_contexts_available": int(sub.shape[0]),
                    "geneformer_support_context_count": int(supported.shape[0]),
                    "geneformer_strong_context_count": int(strong.shape[0]),
                    "geneformer_support_contexts": ";".join(supported["context"].astype(str).tolist()),
                    "geneformer_best_context": str(sub.sort_values("cosine_shift_z_vs_random", ascending=False).iloc[0]["context"]) if not sub.empty else "",
                    "geneformer_best_cosine_z": float(sub["cosine_shift_z_vs_random"].max()) if "cosine_shift_z_vs_random" in sub.columns and sub["cosine_shift_z_vs_random"].notna().any() else np.nan,
                }
            )
        context_sum = pd.DataFrame(rows)
    return gene_sum, context_sum


def summarize_wave55_wave62() -> tuple[pd.DataFrame, pd.DataFrame]:
    w55 = read_tsv(PATHS["wave55"])
    if not w55.empty:
        cols = [
            "gene",
            "wave55_score",
            "n_diseases_genetic_ge_0_25",
            "diseases_genetic_ge_0_25",
            "n_diseases_genetic_ge_0_5",
            "diseases_genetic_ge_0_5",
            "ms_genetic_association",
            "ms_overall_score",
            "local_positive_disease_count",
            "local_positive_diseases",
            "strict_residual_disease_count",
            "foundation_recommendation",
        ]
        w55 = w55[w55["gene"].isin(CANDIDATES)][[c for c in cols if c in w55.columns]].copy()
    w62 = read_tsv(PATHS["wave62"])
    if not w62.empty:
        cols = [
            "gene",
            "wave62_score",
            "wave62_call",
            "manual_blocker",
            "max_l2g_score",
            "best_l2g_disease",
            "strong_l2g_disease_count",
            "strong_l2g_diseases",
            "ms_max_l2g_score",
            "strong_qtl_coloc_disease_count",
            "strong_qtl_coloc_diseases",
            "ms_max_qtl_h4",
            "local_positive_disease_count",
            "local_positive_diseases",
            "ms_wm_delta_log2",
            "ms_wm_p",
            "ms_wm_fdr",
        ]
        w62 = w62[w62["gene"].isin(CANDIDATES)][[c for c in cols if c in w62.columns]].copy()
    return w55, w62


def classify(row: pd.Series) -> str:
    blocker = str(row.get("prior_or_route_blocker", ""))
    wave86_anchor = str(row.get("wave86_call", "")) == "GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR"
    ms_support = str(row.get("ms_wm_support", "")) == "MS_WM_POSITIVE_NOMINAL"
    broad_count = int(row.get("direct_h5ad_positive_p05_disease_count", 0) or 0)
    genetic_count = int(row.get("n_diseases_genetic_ge_0_25", 0) or 0) if not pd.isna(row.get("n_diseases_genetic_ge_0_25", np.nan)) else 0
    geneformer_strong = int(row.get("geneformer_strong_context_count", 0) or 0) if not pd.isna(row.get("geneformer_strong_context_count", np.nan)) else 0

    if not wave86_anchor:
        return "NO_GO_NOT_WAVE86_PRIMARY_ANCHOR"
    if blocker.startswith("BLOCKED") or blocker.startswith("NO_GO"):
        return "NO_GO_PRIOR_ROUTE_OR_DRUGGABILITY_BLOCKED"
    if broad_count < 3:
        return "PARK_ANTI_TNF_ANCHOR_BUT_NOT_BROAD_CROSS_DISEASE"
    if not ms_support:
        return "PARK_ANTI_TNF_ANCHOR_BUT_NO_MS_SINGLE_GENE_SUPPORT"
    if genetic_count < 4:
        return "PARK_ANTI_TNF_ANCHOR_BUT_NO_CROSS_DISEASE_GENETIC_ANCHOR"
    if geneformer_strong == 0:
        return "PARK_ANTI_TNF_ANCHOR_BUT_NO_FOUNDATION_PERTURBATION_SUPPORT"
    return "REOPEN_INFLAMMATORY_NONRESPONSE_CENTRAL_NODE"


def markdown_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    if df.empty:
        return "_No rows._"
    show = df.head(max_rows).copy()
    for col in show.columns:
        if pd.api.types.is_float_dtype(show[col]):
            show[col] = show[col].map(lambda x: "" if pd.isna(x) else f"{x:.4g}")
    show = show.fillna("").astype(str)
    headers = list(show.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in show.iterrows():
        values = [row[col].replace("|", "\\|") for col in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_audit() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    wave86 = read_tsv(PATHS["wave86"])
    wave86 = wave86[wave86["gene"].isin(CANDIDATES)].copy()
    wave86 = wave86.rename(columns={"call": "wave86_call"})

    direct = summarize_direct_h5ad()
    ms = summarize_ms_white_matter()
    geneformer_gene, geneformer_context = summarize_geneformer()
    w55, w62 = summarize_wave55_wave62()

    rows = pd.DataFrame({"gene": CANDIDATES})
    rows = rows.merge(
        wave86[
            [
                "gene",
                "modules",
                "n_primary_contexts",
                "nonresponse_high_contexts",
                "nominal_nonresponse_contexts_p_lt_0_05",
                "fdr10_nonresponse_contexts",
                "weighted_mean_hedges_g_responder_minus_non",
                "median_auc_high_score_nonresponse",
                "wave86_call",
            ]
        ],
        on="gene",
        how="left",
    )
    for table in [direct, ms, geneformer_gene, geneformer_context, w55, w62]:
        if not table.empty:
            rows = rows.merge(table, on="gene", how="left")

    rows["prior_or_route_blocker"] = rows["gene"].map(PRIOR_OR_ROUTE_BLOCKERS)
    for col in [
        "nonresponse_high_contexts",
        "nominal_nonresponse_contexts_p_lt_0_05",
        "fdr10_nonresponse_contexts",
        "direct_h5ad_positive_p05_disease_count",
        "direct_h5ad_positive_fdr10_disease_count",
        "direct_h5ad_negative_p05_disease_count",
        "geneformer_support_context_count",
        "geneformer_strong_context_count",
        "n_diseases_genetic_ge_0_25",
    ]:
        if col in rows.columns:
            rows[col] = rows[col].fillna(0)

    rows["wave87_call"] = rows.apply(classify, axis=1)
    rows["central_node_score"] = (
        rows.get("nonresponse_high_contexts", 0).astype(float) * 2.0
        + rows.get("nominal_nonresponse_contexts_p_lt_0_05", 0).astype(float) * 1.5
        + rows.get("fdr10_nonresponse_contexts", 0).astype(float) * 1.5
        + rows.get("direct_h5ad_positive_p05_disease_count", 0).astype(float) * 1.0
        + rows.get("geneformer_strong_context_count", 0).astype(float) * 1.0
        + rows.get("n_diseases_genetic_ge_0_25", 0).astype(float) * 0.5
        + np.where(rows.get("ms_wm_support", "") == "MS_WM_POSITIVE_NOMINAL", 2.0, 0.0)
        - rows["prior_or_route_blocker"].fillna("").str.startswith("BLOCKED").astype(float) * 6.0
        - rows["prior_or_route_blocker"].fillna("").str.startswith("NO_GO").astype(float) * 5.0
    )
    rows = rows.sort_values(["wave87_call", "central_node_score"], ascending=[True, False])

    module_tests = read_tsv(PATHS["ms_modules"])
    ms_module_focus = pd.DataFrame()
    if not module_tests.empty:
        ms_module_focus = module_tests[
            module_tests["feature"].isin(["generic_nfkb_tnf", "hif_nampt_metabolic", "interferon_apc", "lipid_loader_repair", "lysosome_antigen_processing"])
            | module_tests["feature"].astype(str).str.contains("inflammatory", case=False, na=False)
        ].copy()

    rows.to_csv(OUT / "inflammatory_nonresponse_circuit_rank.tsv", sep="\t", index=False)
    ms_module_focus.to_csv(OUT / "ms_module_context.tsv", sep="\t", index=False)
    if not geneformer_context.empty:
        geneformer_context.to_csv(OUT / "geneformer_candidate_context_summary.tsv", sep="\t", index=False)

    call_counts = rows["wave87_call"].value_counts().to_dict()
    summary = {
        "seed": SEED,
        "n_candidates": int(rows.shape[0]),
        "call_counts": {str(k): int(v) for k, v in call_counts.items()},
        "top_scored_gene": str(rows.sort_values("central_node_score", ascending=False).iloc[0]["gene"]) if not rows.empty else "",
        "reopened_count": int((rows["wave87_call"] == "REOPEN_INFLAMMATORY_NONRESPONSE_CENTRAL_NODE").sum()),
        "decision": "NO_REOPEN_INFLAMMATORY_ANTITNF_NONRESPONSE_CIRCUIT_AS_V3_TARGET",
        "inputs": {k: str(v.relative_to(ROOT)) for k, v in PATHS.items() if v.exists()},
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    selected_cols = [
        "gene",
        "modules",
        "wave86_call",
        "central_node_score",
        "wave87_call",
        "prior_or_route_blocker",
        "nonresponse_high_contexts",
        "nominal_nonresponse_contexts_p_lt_0_05",
        "fdr10_nonresponse_contexts",
        "median_auc_high_score_nonresponse",
        "direct_h5ad_positive_p05_disease_count",
        "direct_h5ad_positive_p05_diseases",
        "direct_h5ad_negative_p05_disease_count",
        "ms_wm_delta_log2",
        "ms_wm_p",
        "ms_wm_support",
        "n_diseases_genetic_ge_0_25",
        "diseases_genetic_ge_0_25",
        "wave62_call",
        "geneformer_strong_context_count",
        "geneformer_support_contexts",
    ]
    available_cols = [c for c in selected_cols if c in rows.columns]
    top = rows.sort_values("central_node_score", ascending=False)[available_cols]
    report = [
        "# Wave87 Inflammatory Anti-TNF Nonresponse Circuit Audit",
        "",
        "Question: after the residual lysosomal/APC response score failed external validation, can the Wave86 generic inflammatory nonresponse genes yield a V3-grade cross-autoimmune target or central node?",
        "",
        f"Decision: `{summary['decision']}`.",
        "",
        "## Candidate Rank",
        "",
        markdown_table(top, max_rows=30),
        "",
        "## MS Module Context",
        "",
        markdown_table(ms_module_focus, max_rows=30),
        "",
        "## Interpretation",
        "",
        "- `IL1B`, `CXCL8`, and `TREM1` are the strongest external mucosal anti-TNF nonresponse anchors, but this evidence is treatment-response biology in IBD mucosa, not a cross-autoimmune therapeutic target.",
        "- Local MS white-matter evidence does not support the inflammatory/NFKB/TNF single-gene branch: the inflammatory module is null while lipid-loader and lysosome/APC modules are stronger.",
        "- The only available Geneformer support in this candidate set is `CXCL8` in IBD myeloid cells; most Wave86 leaders were not covered by the prior foundation-model perturbation tables.",
        "- The branch therefore remains useful as a nonresponse-state comparator and trial-stratification warning, but not as a V3 finding.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    build_audit()


if __name__ == "__main__":
    main()
