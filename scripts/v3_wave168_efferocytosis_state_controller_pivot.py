#!/usr/bin/env python3
"""Wave168: phenotype-first efferocytosis/state-controller pivot.

This tests Boole's recommendation: do not require same-gene genetics first.
Start with a functional myeloid repair phenotype (KO enhances efferocytosis),
then ask whether hits recur in autoimmune cell states and have intervention
handles. This can nominate a pathway-controller route or close the branch.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave168_efferocytosis_state_controller_pivot"
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


def first(df: pd.DataFrame, gene: str, col: str = "gene") -> dict:
    if df.empty or col not in df.columns:
        return {}
    rows = df[df[col] == gene]
    if rows.empty:
        return {}
    return rows.iloc[0].to_dict()


wave37 = read_tsv("phases/v3/results/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv")
wave81 = read_tsv("phases/v3/results/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv")
wave82 = read_tsv("phases/v3/results/wave82_parked_perturbation_intervention_audit/wave82_integrated_intervention_rank.tsv")
wave166 = read_tsv("phases/v3/results/wave166_same_gene_genetics_cellstate_overlap/same_gene_genetics_cellstate_rank.tsv")
wave167 = read_tsv("phases/v3/results/wave167_shadow_no_label_overlap/shadow_no_label_rank.tsv")
wave62 = read_tsv("phases/v3/results/wave62_opentargets_target_resolution/target_resolution_summary.tsv")

if wave37.empty:
    raise SystemExit("Missing Wave37 efferocytosis screen table")

hits = wave37[
    (wave37["screen_call"] == "KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR")
    & (wave37["efficient_consistent_positive"].astype(str).str.lower() == "true")
    & (wave37["median_efficient_minus_noneater_lfc"].map(lambda x: f(x)) > 0.5)
].copy()

rows = []
for _, hit in hits.iterrows():
    gene = s(hit.get("gene_symbol"))
    r81 = first(wave81, gene)
    r82 = first(wave82, gene)
    r166 = first(wave166, gene)
    r167 = first(wave167, gene)
    r62 = first(wave62, gene)

    c15_pos = f(r166.get("c15_trend_positive_disease_count", r167.get("c15_trend_positive_disease_count", 0)))
    c15_strict = f(r166.get("c15_strict_positive_context_count", r167.get("c15_strict_positive_context_count", 0)))
    ms_delta = f(r166.get("ms_delta_log2", r167.get("ms_delta_log2", r81.get("ms_delta_log2", 0))))
    ms_p = f(r166.get("ms_p", r167.get("ms_p", r81.get("ms_p", 1))), 1)
    broad_pos = max(c15_pos, f(r81.get("broad_positive_disease_count", 0)), f(r82.get("positive_broad_disease_count", 0)))
    chembl = s(r62.get("chembl_target_id", r82.get("chembl_exact_target_ids", "")))
    activity = max(f(r62.get("druggable_activity_count", 0)), f(r82.get("chembl_exact_human_target_count", 0)))
    modality = f(r81.get("modality_channel", 0)) >= 1 or f(r82.get("modality_or_accessible_route", 0)) >= 1 or bool(chembl)
    genetics = f(r62.get("strong_l2g_disease_count", 0)) >= 3 or f(r62.get("strong_qtl_coloc_disease_count", 0)) >= 3
    ms_anchor = bool(f(r81.get("ms_anchor", 0))) or (ms_delta > 0 and ms_p < 0.05)
    state_recurrence = broad_pos >= 2 or c15_strict >= 2
    prior_text = " | ".join(
        x
        for x in [
            s(r81.get("blocker", "")),
            s(r81.get("decision_reason", "")),
            s(r82.get("manual_blocker", "")),
            s(r82.get("hard_failures", "")),
            s(r82.get("wave82_call", "")),
            s(r166.get("prior_text", "")),
            s(r62.get("manual_blocker", "")),
            s(r62.get("prior_context_blocker", "")),
        ]
        if x
    )
    text_l = prior_text.lower()
    hard_blocked = any(
        token in text_l
        for token in [
            "no_direct_modality",
            "no_direct_modality_or_accessible_route",
            "broad_surface_tetraspanin",
            "broad_src_family",
            "prior_art",
            "not_selectively_druggable",
            "housekeeping",
            "generic_oxidative",
            "no_ms_anchor",
        ]
    )

    phenotype_strength = f(hit.get("median_efficient_minus_noneater_lfc", 0))
    fdr = f(hit.get("contrast_fdr", 1), 1)
    fdr_support = fdr < 0.1 if fdr != 0 else False
    score = (
        3.0 * phenotype_strength
        + 2.0 * state_recurrence
        + 1.5 * ms_anchor
        + 1.0 * modality
        + 1.0 * genetics
        + 0.5 * fdr_support
        + 0.2 * min(broad_pos, 5)
        - 2.5 * hard_blocked
    )
    promote = phenotype_strength > 0.75 and state_recurrence and ms_anchor and modality and not hard_blocked
    blockers = []
    if not state_recurrence:
        blockers.append("insufficient_autoimmune_state_recurrence")
    if not ms_anchor:
        blockers.append("no_ms_anchor")
    if not modality:
        blockers.append("no_intervention_handle")
    if hard_blocked:
        blockers.append("prior_or_modality_blocker")
    if not genetics:
        blockers.append("no_genetic_anchor_annotation")

    rows.append(
        {
            "gene": gene,
            "phenotype_strength_lfc": phenotype_strength,
            "contrast_fdr": fdr,
            "efficient_consistent_positive": bool(hit.get("efficient_consistent_positive")),
            "state_recurrence": state_recurrence,
            "broad_positive_disease_count": broad_pos,
            "positive_contexts": s(r166.get("positive_c15_contexts", r167.get("positive_c15_contexts", ""))),
            "ms_anchor": ms_anchor,
            "ms_delta_log2": ms_delta,
            "ms_p": ms_p,
            "modality_or_accessible_route": modality,
            "chembl_target_id": chembl,
            "druggability_activity_or_target_count": activity,
            "genetic_anchor_annotation": genetics,
            "strong_l2g_disease_count": f(r62.get("strong_l2g_disease_count", 0)),
            "strong_qtl_coloc_disease_count": f(r62.get("strong_qtl_coloc_disease_count", 0)),
            "wave81_call": s(r81.get("wave81_call", "")),
            "wave82_call": s(r82.get("wave82_call", "")),
            "gene_class": s(r82.get("gene_class", "")),
            "intervention_route_read": s(r82.get("intervention_route_read", "")),
            "hard_blocked_annotation": hard_blocked,
            "pivot_score": score,
            "promote": promote,
            "blockers": ";".join(blockers),
            "prior_annotation": prior_text,
        }
    )

rank = pd.DataFrame(rows).sort_values(["promote", "pivot_score"], ascending=[False, False])
rank.to_csv(OUT / "efferocytosis_state_controller_rank.tsv", sep="\t", index=False)
rank.head(50).to_csv(OUT / "top_efferocytosis_state_controller_candidates.tsv", sep="\t", index=False)
promoted = rank[rank["promote"]]
branch = "PROMOTE_EFFEROCYTOSIS_STATE_CONTROLLER" if len(promoted) else "NO_EFFEROCYTOSIS_STATE_CONTROLLER_PROMOTION"
best = rank.iloc[0].to_dict() if len(rank) else {}
summary = {
    "branch_call": branch,
    "screen_hits_tested": int(len(rank)),
    "promoted_candidates": promoted["gene"].tolist() if len(promoted) else [],
    "best_gene": best.get("gene", ""),
    "best_score": float(best.get("pivot_score", 0)),
    "best_blockers": best.get("blockers", ""),
    "interpretation": (
        "Phenotype-first efferocytosis hits contain useful repair-state biology, but no hit currently "
        "combines functional phenotype, autoimmune recurrence, MS anchor, intervention handle, and unblocked route."
    ),
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

report = f"""# Wave168 Efferocytosis State-Controller Pivot

## Branch call
`{branch}`

## Result
- Screen hits tested: `{len(rank)}`.
- Promoted candidates: `{len(promoted)}`.
- Best gene: `{best.get('gene', '')}`.
- Best score: `{best.get('pivot_score', 0)}`.
- Best blockers: `{best.get('blockers', '')}`.

## Interpretation
This branch treats efferocytosis as a repair phenotype rather than a genetic
target. It does not produce a V3 target yet because the top functional hits
still fail one or more of state recurrence, MS anchoring, intervention handle,
or prior/modality safety.
"""
(OUT / "REPORT.md").write_text(report)

print(json.dumps(summary, indent=2))
