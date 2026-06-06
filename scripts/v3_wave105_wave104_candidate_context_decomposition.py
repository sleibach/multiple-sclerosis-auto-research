#!/usr/bin/env python3
"""Wave105 decomposition of Wave104 genetics-first sidecar candidates.

This script turns the Wave104 sidecar set into per-disease/per-compartment
evidence. It is deliberately descriptive: it asks whether the genetic candidate
is actually present in the disease cell state being pursued, or whether the
signal is off-compartment, residualization-fragile, or mostly prior-art biology.
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
OUT = ROOT / "phases/v3/results" / "wave105_wave104_candidate_context_decomposition"

TARGETS = ["IFI30", "IL7R", "SP140", "GALC", "CD58"]

BROAD_CONTRASTS = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
W94_CONTEXT = ROOT / "phases/v3/results" / "wave94_accessible_state_rerank" / "broad_candidate_context_rows.tsv"
RESIDUAL_RAW = ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_raw_tests.tsv"
RESIDUAL_TESTS = ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_residual_tests.tsv"
W91_MATRIX = ROOT / "phases/v3/results" / "wave91_lipid_lysosomal_module_intervention_rank" / "module_wide_evidence_matrix.tsv"
W104_RANK = ROOT / "phases/v3/results" / "wave104_genetics_first_lipid_state_convergence_audit" / "genetics_first_lipid_state_rank.tsv"


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


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return clean(value).strip().lower() in {"1", "true", "yes", "y"}


def target_rows(df: pd.DataFrame, col: str = "gene") -> pd.DataFrame:
    if df.empty or col not in df.columns:
        return pd.DataFrame()
    out = df[df[col].astype(str).str.upper().isin(TARGETS)].copy()
    if col != "gene" and col in out.columns:
        out = out.rename(columns={col: "gene"})
    out["gene"] = out["gene"].astype(str).str.upper()
    return out


def summarize_contexts(context: pd.DataFrame, source: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    c = target_rows(context)
    if c.empty:
        return pd.DataFrame(), pd.DataFrame()
    for col in ["p", "fdr", "delta_log2_cpm", "hedges_g"]:
        if col in c.columns:
            c[col] = pd.to_numeric(c[col], errors="coerce")
    for col in ["positive_nominal", "negative_nominal", "positive_fdr10", "negative_fdr10"]:
        if col in c.columns:
            c[col] = c[col].map(boolish)
    c["source"] = source
    c["context_id"] = (
        c["analysis"].astype(str)
        + "|"
        + c["disease_name"].astype(str)
        + "|"
        + c["compartment"].astype(str)
        + "|"
        + c["role"].astype(str)
    )
    rows = []
    for gene, sub in c.groupby("gene"):
        pos = sub[sub.get("positive_nominal", False).astype(bool)] if "positive_nominal" in sub.columns else sub.iloc[0:0]
        neg = sub[sub.get("negative_nominal", False).astype(bool)] if "negative_nominal" in sub.columns else sub.iloc[0:0]
        pos_fdr = sub[sub.get("positive_fdr10", False).astype(bool)] if "positive_fdr10" in sub.columns else sub.iloc[0:0]
        myeloid = pos[pos["role"].astype(str).str.contains("myeloid|apc|microgl", case=False, na=False)]
        tissue = pos[pos["role"].astype(str).str.contains("stromal|epithelial|keratinocyte|acinar|ductal|endothelial|stellate", case=False, na=False)]
        lipid = sub[sub["in_lipid_lysosomal_myeloid_neighborhood"].map(boolish)] if "in_lipid_lysosomal_myeloid_neighborhood" in sub.columns else sub.iloc[0:0]
        best_pos = pos.sort_values(["p", "delta_log2_cpm"], ascending=[True, False]).head(6)
        rows.append(
            {
                "gene": gene,
                "source": source,
                "tested_context_count": int(len(sub)),
                "positive_context_count": int(len(pos)),
                "positive_fdr10_context_count": int(len(pos_fdr)),
                "negative_context_count": int(len(neg)),
                "positive_disease_count": int(pos["disease_name"].nunique()) if not pos.empty else 0,
                "positive_diseases": ";".join(sorted(pos["disease_name"].dropna().astype(str).unique())),
                "myeloid_positive_context_count": int(len(myeloid)),
                "myeloid_positive_disease_count": int(myeloid["disease_name"].nunique()) if not myeloid.empty else 0,
                "tissue_resident_positive_context_count": int(len(tissue)),
                "lipid_neighborhood_context_count": int(len(lipid)),
                "best_positive_contexts": "; ".join(
                    f"{r.context_id}:delta={num(r.get('delta_log2_cpm')):.3g},p={num(r.get('p')):.3g},fdr={num(r.get('fdr')):.3g}"
                    for _, r in best_pos.iterrows()
                ),
            }
        )
    return pd.DataFrame(rows), c


def summarize_residual(raw: pd.DataFrame, residual: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    r = target_rows(raw)
    rr = target_rows(residual)
    for df in [r, rr]:
        if df.empty:
            continue
        for col in ["p", "fdr", "delta_case_minus_control", "hedges_g", "residual_delta_case_minus_control", "residual_p", "residual_fdr"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        for col in ["positive_nominal", "negative_nominal", "retains_nominal_positive", "retains_direction_only"]:
            if col in df.columns:
                df[col] = df[col].map(boolish)

    rows = []
    for gene in TARGETS:
        sub_raw = r[r["gene"].eq(gene)] if not r.empty else pd.DataFrame()
        sub_resid = rr[rr["gene"].eq(gene)] if not rr.empty else pd.DataFrame()
        raw_pos = sub_raw[sub_raw["positive_nominal"].astype(bool)] if not sub_raw.empty and "positive_nominal" in sub_raw.columns else pd.DataFrame()
        retained = sub_resid[sub_resid["retains_nominal_positive"].astype(bool)] if not sub_resid.empty and "retains_nominal_positive" in sub_resid.columns else pd.DataFrame()
        direction = sub_resid[sub_resid["retains_direction_only"].astype(bool)] if not sub_resid.empty and "retains_direction_only" in sub_resid.columns else pd.DataFrame()
        best_retained = retained.sort_values(["residual_p", "residual_delta_case_minus_control"], ascending=[True, False]).head(6) if not retained.empty else pd.DataFrame()
        rows.append(
            {
                "gene": gene,
                "raw_positive_analysis_count": int(len(raw_pos)),
                "raw_positive_disease_count": int(raw_pos["disease_name"].nunique()) if not raw_pos.empty else 0,
                "retained_positive_analysis_count": int(len(retained)),
                "retained_positive_disease_count": int(retained["disease_name"].nunique()) if not retained.empty else 0,
                "direction_only_analysis_count": int(len(direction)),
                "direction_only_disease_count": int(direction["disease_name"].nunique()) if not direction.empty else 0,
                "best_retained_residual_tests": "; ".join(
                    f"{x.analysis}|{x.disease_name}|{x.compartment}|{x.role}:delta={num(x.get('residual_delta_case_minus_control')):.3g},p={num(x.get('residual_p')):.3g},fdr={num(x.get('residual_fdr')):.3g}"
                    for _, x in best_retained.iterrows()
                ),
            }
        )
    return pd.DataFrame(rows), pd.concat([r.assign(residual_layer="raw"), rr.assign(residual_layer="residual")], ignore_index=True)


def summarize_w91(w91: pd.DataFrame) -> pd.DataFrame:
    c = target_rows(w91)
    if c.empty:
        return pd.DataFrame({"gene": TARGETS})
    keep = [
        "gene",
        "modules",
        "nonresponse_high_contexts",
        "responder_high_contexts",
        "ibd_weighted_hedges_g_responder_minus_non",
        "ibd_min_p",
        "best_context",
        "ra_hedges_g_responder_minus_non",
        "ra_p",
        "psoriasis_ada_hedges_g_responder_minus_non",
        "psoriasis_ada_p",
        "ms_wm_delta_log2",
        "ms_wm_p",
        "direct_positive_p05_disease_count",
        "direct_positive_p05_diseases",
        "strict_residual_disease_count",
        "wave91_call",
        "route_blocker",
    ]
    keep = [x for x in keep if x in c.columns]
    return c[keep].copy()


def classify(row: pd.Series) -> tuple[str, str]:
    gene = clean(row.get("gene"))
    retained = num(row.get("retained_positive_disease_count"), 0.0)
    myeloid = num(row.get("myeloid_positive_disease_count_broad"), 0.0)
    local = num(row.get("positive_disease_count_broad"), 0.0)
    response = num(row.get("nonresponse_high_contexts"), 0.0)
    prior = boolish(row.get("prior_or_safety"))
    modality_missing = "reachable_modality" in clean(row.get("wave104_missing_gates"))
    direction_missing = "directional_or_perturbation_support" in clean(row.get("wave104_missing_gates"))
    if gene in {"IL7R", "CD58"}:
        return "CONTROL_PRIOR_ART_OR_KNOWN_IMMUNE_AXIS", "Useful comparator, not a novel target in this run."
    if retained >= 1 and (myeloid >= 1 or response >= 2) and not direction_missing and not modality_missing and not prior:
        return "REOPEN_CONTEXT_SUPPORTED", "Residual/state evidence aligns and hard gates are not currently blocked."
    if retained >= 1 and (myeloid >= 1 or response >= 2):
        return "PARK_STATE_SUPPORTED_BUT_ROUTE_BLOCKED", "State evidence exists but prior, modality, or direction remains blocking."
    if local >= 3 and retained == 0:
        return "PARK_RAW_RECURRENCE_RESIDUAL_WEAK", "Raw cross-disease recurrence exists but residual support is absent or weak."
    return "NO_GO_CONTEXT_SUPPORT_WEAK", "No strong residualized disease-cell-state support."


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    broad_summary, broad_context = summarize_contexts(read_tsv(BROAD_CONTRASTS), "broad_h5ad")
    w94_summary, w94_context = summarize_contexts(read_tsv(W94_CONTEXT), "wave94_accessible")
    residual_summary, residual_context = summarize_residual(read_tsv(RESIDUAL_RAW), read_tsv(RESIDUAL_TESTS))
    w91_summary = summarize_w91(read_tsv(W91_MATRIX))
    w104 = target_rows(read_tsv(W104_RANK))

    broad_summary = broad_summary.add_suffix("_broad").rename(columns={"gene_broad": "gene"})
    w94_summary = w94_summary.add_suffix("_wave94").rename(columns={"gene_wave94": "gene"})

    summary = pd.DataFrame({"gene": TARGETS})
    for df in [w104, broad_summary, w94_summary, residual_summary, w91_summary]:
        if not df.empty:
            summary = summary.merge(df, on="gene", how="left", suffixes=("", "_dup"))
            dup_cols = [c for c in summary.columns if c.endswith("_dup")]
            if dup_cols:
                summary = summary.drop(columns=dup_cols)

    calls = summary.apply(classify, axis=1, result_type="expand")
    summary["wave105_context_call"] = calls[0]
    summary["wave105_context_reason"] = calls[1]

    summary.to_csv(OUT / "wave104_candidate_context_summary.tsv", sep="\t", index=False)
    if not broad_context.empty:
        broad_context.to_csv(OUT / "wave104_candidate_broad_context_rows.tsv", sep="\t", index=False)
    if not w94_context.empty:
        w94_context.to_csv(OUT / "wave104_candidate_wave94_context_rows.tsv", sep="\t", index=False)
    if not residual_context.empty:
        residual_context.to_csv(OUT / "wave104_candidate_residual_context_rows.tsv", sep="\t", index=False)

    report_cols = [
        "gene",
        "wave105_context_call",
        "wave105_context_reason",
        "wave104_call",
        "wave104_missing_gates",
        "positive_disease_count_broad",
        "positive_diseases_broad",
        "myeloid_positive_disease_count_broad",
        "tissue_resident_positive_context_count_broad",
        "retained_positive_disease_count",
        "best_retained_residual_tests",
        "nonresponse_high_contexts",
        "ms_wm_delta_log2",
        "ms_wm_p",
        "route_blocker",
    ]
    report_cols = [c for c in report_cols if c in summary.columns]

    counts = summary["wave105_context_call"].value_counts().sort_index().to_dict()
    write_json(
        OUT / "summary.json",
        {
            "seed": SEED,
            "targets": TARGETS,
            "call_counts": counts,
            "inputs": {
                "broad_contrasts": rel(BROAD_CONTRASTS),
                "wave94_context": rel(W94_CONTEXT),
                "residual_raw": rel(RESIDUAL_RAW),
                "residual_tests": rel(RESIDUAL_TESTS),
                "wave91_matrix": rel(W91_MATRIX),
                "wave104_rank": rel(W104_RANK),
            },
        },
    )

    lines = [
        "# Wave105 Wave104 Candidate Context Decomposition",
        "",
        "## Bottom Line",
        "",
        "This wave decomposes the Wave104 genetics-first sidecar set by disease,",
        "compartment, response state, and residual support. It does not nominate a",
        "target by itself.",
        "",
        "## Context Calls",
        "",
        "```json",
        json.dumps(counts, indent=2, sort_keys=True),
        "```",
        "",
        "## Candidate Summary",
        "",
        markdown_table(summary[report_cols], max_rows=20),
        "",
        "## Interpretation",
        "",
        "- A target-resolved genetic signal is only useful here if it lands in the",
        "  cross-disease lipid/myeloid disease state after compartment and residual",
        "  checks.",
        "- Raw recurrence without residual retention is treated as dispatch material,",
        "  not as mechanism.",
        "- Known immune axes are retained as calibration controls, not as novelty",
        "  candidates.",
        "",
        "## Reproducibility",
        "",
        f"- Script: `{rel(ROOT / 'scripts' / 'v3_wave105_wave104_candidate_context_decomposition.py')}`",
        f"- Summary: `{rel(OUT / 'wave104_candidate_context_summary.tsv')}`",
        f"- Seed: `{SEED}`",
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
