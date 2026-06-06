#!/usr/bin/env python3
"""Wave167: no-label shadow ranking for same-gene genetics/cell-state overlap.

This addresses Linnaeus's critique that Wave166 may have created circular
depletion by using inherited no-go labels as eligibility gates. Here, prior
labels are annotations only. Evidence ranking is independent of those labels.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave167_shadow_no_label_overlap"
OUT.mkdir(parents=True, exist_ok=True)


def read_tsv(rel: str) -> pd.DataFrame:
    p = ROOT / rel
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p, sep="\t", low_memory=False)


def f(x, default=0.0) -> float:
    try:
        if pd.isna(x):
            return default
        return float(x)
    except Exception:
        return default


def s(x) -> str:
    if x is None or pd.isna(x):
        return ""
    val = str(x)
    return "" if val.lower() == "nan" else val


def first(df: pd.DataFrame, gene: str) -> dict:
    if df.empty or "gene" not in df.columns:
        return {}
    rows = df[df["gene"] == gene]
    if rows.empty:
        return {}
    return rows.iloc[0].to_dict()


wave62 = read_tsv("phases/v3/results/wave62_opentargets_target_resolution/target_resolution_summary.tsv")
wave96 = read_tsv("phases/v3/results/wave96_c15orf48_controller_search/pre_donor_controller_rank.tsv")
wave164 = read_tsv("phases/v3/results/wave164_genetics_first_survivor_audit/genetics_first_survivor_rank.tsv")
wave166 = read_tsv("phases/v3/results/wave166_same_gene_genetics_cellstate_overlap/same_gene_genetics_cellstate_rank.tsv")
wave82 = read_tsv("phases/v3/results/wave82_parked_perturbation_intervention_audit/wave82_integrated_intervention_rank.tsv")

genes = sorted(set(wave62.get("gene", [])) | set(wave96.get("gene", [])) | set(wave164.get("gene", [])) | set(wave82.get("gene", [])))

rows = []
for gene in genes:
    r62 = first(wave62, gene)
    r96 = first(wave96, gene)
    r164 = first(wave164, gene)
    r166 = first(wave166, gene)
    r82 = first(wave82, gene)

    strong_l2g = f(r62.get("strong_l2g_disease_count", r164.get("strong_l2g_disease_count", 0)))
    strong_qtl = f(r62.get("strong_qtl_coloc_disease_count", r164.get("strong_qtl_coloc_disease_count", 0)))
    ms_l2g = f(r62.get("ms_max_l2g_score", r164.get("ms_max_l2g_score", 0)))
    ms_qtl = f(r62.get("ms_max_qtl_h4", r164.get("ms_max_qtl_h4", 0)))
    c15_pos_disease = f(r96.get("c15_trend_positive_disease_count", 0))
    c15_strict = f(r96.get("c15_strict_positive_context_count", 0))
    c15_myeloid = f(r96.get("c15_myeloid_positive_context_count", 0))
    ms_delta = f(r96.get("ms_delta_log2", r62.get("ms_wm_delta_log2", r82.get("ms_delta_log2", 0))))
    ms_p = f(r96.get("ms_p", r62.get("ms_wm_p", r82.get("ms_p", 1))), 1)
    w37_lfc = f(r96.get("w37_contrast_lfc", 0))
    w37_fdr = f(r96.get("w37_contrast_fdr", 1), 1)
    chembl = s(r62.get("chembl_target_id", r164.get("chembl_target_id", r82.get("chembl_exact_target_ids", ""))))
    activity = f(r62.get("druggable_activity_count", r164.get("druggable_activity_count", 0)))
    wave82_channels = f(r82.get("evidence_channel_count", 0))

    genetics_gate = (ms_l2g >= 0.5 or ms_qtl >= 0.8) and (strong_l2g >= 3 or strong_qtl >= 3)
    cellstate_gate = c15_pos_disease >= 2 and c15_strict >= 1
    ms_trend = ms_delta > 0 and ms_p < 0.25
    perturb_trend = abs(w37_lfc) >= 0.25 and w37_fdr < 0.95
    reachable_annotation = bool(chembl) or activity >= 25 or f(r82.get("modality_or_accessible_route", 0)) >= 1

    evidence_score = (
        4.0 * genetics_gate
        + 3.0 * cellstate_gate
        + 1.5 * ms_trend
        + 1.0 * perturb_trend
        + 0.7 * reachable_annotation
        + 0.4 * min(strong_l2g, 8)
        + 0.4 * min(strong_qtl, 8)
        + 0.5 * min(c15_pos_disease, 5)
        + 0.3 * min(c15_strict, 5)
        + 0.2 * min(wave82_channels, 4)
    )

    prior_annotation = " | ".join(
        x
        for x in [
            s(r62.get("wave62_call", "")),
            s(r62.get("manual_blocker", "")),
            s(r62.get("prior_context_blocker", "")),
            s(r164.get("blockers", "")),
            s(r166.get("prior_text", "")),
            s(r82.get("hard_failures", "")),
            s(r82.get("manual_blocker", "")),
        ]
        if x
    )

    # Not a gate: rough classification for review.
    text_l = prior_annotation.lower()
    if "prior_art" in text_l or "prior" in text_l:
        label_class = "prior_art_or_local_prior"
    elif "no_direct" in text_l or "not_reachable" in text_l or "druggable" in text_l:
        label_class = "modality_blocker"
    elif "no_go" in text_l:
        label_class = "local_no_go_label"
    elif "safety" in text_l:
        label_class = "safety_blocker"
    else:
        label_class = "unlabeled_or_data_blocked"

    rows.append(
        {
            "gene": gene,
            "shadow_evidence_score": evidence_score,
            "genetics_gate": genetics_gate,
            "cellstate_gate": cellstate_gate,
            "ms_expression_trend": ms_trend,
            "perturbation_trend": perturb_trend,
            "reachable_annotation": reachable_annotation,
            "strong_l2g_disease_count": strong_l2g,
            "strong_l2g_diseases": s(r62.get("strong_l2g_diseases", r164.get("strong_l2g_diseases", ""))),
            "strong_qtl_coloc_disease_count": strong_qtl,
            "strong_qtl_coloc_diseases": s(r62.get("strong_qtl_coloc_diseases", r164.get("strong_qtl_coloc_diseases", ""))),
            "ms_max_l2g_score": ms_l2g,
            "ms_max_qtl_h4": ms_qtl,
            "c15_trend_positive_disease_count": c15_pos_disease,
            "c15_strict_positive_context_count": c15_strict,
            "c15_myeloid_positive_context_count": c15_myeloid,
            "positive_c15_contexts": s(r96.get("positive_c15_contexts", "")),
            "best_c15_context": s(r96.get("best_c15_context", "")),
            "ms_delta_log2": ms_delta,
            "ms_p": ms_p,
            "w37_contrast_lfc": w37_lfc,
            "w37_contrast_fdr": w37_fdr,
            "chembl_target_id": chembl,
            "druggable_activity_count": activity,
            "wave82_evidence_channel_count": wave82_channels,
            "wave82_call": s(r82.get("wave82_call", "")),
            "label_class_annotation": label_class,
            "prior_annotation": prior_annotation,
        }
    )

rank = pd.DataFrame(rows).sort_values("shadow_evidence_score", ascending=False)
top25 = rank.head(25).copy()

def data_reason(r: pd.Series) -> str:
    missing = []
    for col, name in [
        ("genetics_gate", "genetics"),
        ("cellstate_gate", "cell_state"),
        ("ms_expression_trend", "ms_expression"),
        ("perturbation_trend", "perturbation"),
        ("reachable_annotation", "reachability"),
    ]:
        if not bool(r[col]):
            missing.append(name)
    return "passes_all_shadow_gates" if not missing else "missing_" + ",".join(missing)

top25["data_gap_annotation"] = top25.apply(data_reason, axis=1)

rank.to_csv(OUT / "shadow_no_label_rank.tsv", sep="\t", index=False)
top25.to_csv(OUT / "shadow_no_label_top25.tsv", sep="\t", index=False)

gate_pass = rank[(rank["genetics_gate"]) & (rank["cellstate_gate"])]
gate_pass.to_csv(OUT / "shadow_same_gene_gate_pass.tsv", sep="\t", index=False)

summary = {
    "branch_call": "SHADOW_RANK_READY_FOR_TARGET_QUALITY_AND_INDEPENDENT_STATE_VALIDATION",
    "genes_ranked": int(len(rank)),
    "same_gene_genetics_cellstate_shadow_pass": int(len(gate_pass)),
    "top_gene": str(rank.iloc[0]["gene"]),
    "top_gene_score": float(rank.iloc[0]["shadow_evidence_score"]),
    "top25_label_classes": top25["label_class_annotation"].value_counts().to_dict(),
    "interpretation": (
        "Removing inherited labels restores a ranked evidence space. This does not rescue a target; "
        "it defines the next candidates requiring target-quality and C15-independent state validation."
    ),
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

report = f"""# Wave167 No-Label Shadow Ranking

## Branch call
`{summary['branch_call']}`

## Result
- Genes ranked: `{summary['genes_ranked']}`.
- Same-gene genetics + C15 cell-state shadow pass: `{summary['same_gene_genetics_cellstate_shadow_pass']}`.
- Top gene by evidence without no-go labels: `{summary['top_gene']}`.

## Interpretation
This is not a finding. It is a guardrail against circular depletion. The next
step is to run target-quality and C15-independent validation on the top no-label
candidates before accepting or rejecting them.
"""
(OUT / "REPORT.md").write_text(report)

print(json.dumps(summary, indent=2))
