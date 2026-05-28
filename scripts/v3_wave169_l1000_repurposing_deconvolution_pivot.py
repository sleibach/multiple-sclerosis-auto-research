#!/usr/bin/env python3
"""Wave169: L1000 repurposing deconvolution pivot.

Start from compounds with module-reversal signatures and ask whether their
putative targets survive target/state/druggability guardrails. This treats
Wave150 PARK_REVIEW rows as unresolved, not as automatically dead.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave169_l1000_repurposing_deconvolution_pivot"
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


triage = read_tsv("results_v3/wave150_repurposing_first_strict_audit/repurposing_triage_reaudit.tsv")
wave62 = read_tsv("results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv")
wave103 = read_tsv("results_v3/wave103_intervention_first_successor_triage/intervention_first_successor_rank.tsv")
wave166 = read_tsv("results_v3/wave166_same_gene_genetics_cellstate_overlap/same_gene_genetics_cellstate_rank.tsv")
wave167 = read_tsv("results_v3/wave167_shadow_no_label_overlap/shadow_no_label_rank.tsv")

if triage.empty:
    raise SystemExit("Missing Wave150 repurposing triage")

review = triage[triage["wave24_call"].astype(str).eq("PARK_REVIEW")].copy()
bad_reason_tokens = ["cytotoxic", "steroid", "oncology", "generic/prior-art", "glucocorticoid"]

rows = []
for _, r in review.iterrows():
    target_field = s(r.get("target"))
    targets = [t.strip() for t in target_field.replace(";", "|").replace(",", "|").split("|") if t.strip()]
    if not targets:
        targets = [""]
    for gene in targets:
        r62 = first(wave62, gene)
        r103 = first(wave103, gene)
        r166 = first(wave166, gene)
        r167 = first(wave167, gene)

        c15_pos = f(r166.get("c15_trend_positive_disease_count", r167.get("c15_trend_positive_disease_count", 0)))
        c15_strict = f(r166.get("c15_strict_positive_context_count", r167.get("c15_strict_positive_context_count", 0)))
        ms_delta = f(r166.get("ms_delta_log2", r167.get("ms_delta_log2", r62.get("ms_wm_delta_log2", 0))))
        ms_p = f(r166.get("ms_p", r167.get("ms_p", r62.get("ms_wm_p", 1))), 1)
        ms_l2g = f(r62.get("ms_max_l2g_score", r167.get("ms_max_l2g_score", 0)))
        ms_qtl = f(r62.get("ms_max_qtl_h4", r167.get("ms_max_qtl_h4", 0)))
        strong_l2g = f(r62.get("strong_l2g_disease_count", r167.get("strong_l2g_disease_count", 0)))
        strong_qtl = f(r62.get("strong_qtl_coloc_disease_count", r167.get("strong_qtl_coloc_disease_count", 0)))
        chembl = s(r62.get("chembl_target_id", r103.get("chembl_target_id", "")))
        activity = f(r62.get("druggable_activity_count", r103.get("chembl_activity_count", 0)))
        reason = s(r.get("strict_reason", r.get("wave24_blocker", "")))
        reason_l = reason.lower()

        review_not_toxic = not any(tok in reason_l for tok in bad_reason_tokens)
        reversal_strength = f(r.get("max_opposite_abs_score", 0))
        recurrence = f(r.get("recurrence_strength", 0))
        selective = s(r.get("l1000_selectivity_call")) != "generic_ifn_reversal_at_least_as_strong"
        state = c15_pos >= 2 or c15_strict >= 1
        ms_anchor = (ms_delta > 0 and ms_p < 0.25) or ms_l2g >= 0.5 or ms_qtl >= 0.8
        genetics = (ms_l2g >= 0.5 or ms_qtl >= 0.8) and (strong_l2g >= 3 or strong_qtl >= 3)
        target_quality_proxy = bool(chembl) or activity >= 25
        prior_text = " | ".join(
            x
            for x in [
                s(r62.get("wave62_call", "")),
                s(r62.get("manual_blocker", "")),
                s(r62.get("prior_context_blocker", "")),
                s(r103.get("call", "")),
                s(r103.get("blockers", "")),
                s(r166.get("prior_text", "")),
            ]
            if x
        ).lower()
        prior_blocked = any(tok in prior_text for tok in ["prior_art", "prior_or_local", "no_go_prior", "safety", "not_selectively_druggable"])
        delivery_annotation = s(r.get("cmap_name")).lower() not in {"thapsigargin", "calyculin", "vincristine"}

        score = (
            0.35 * reversal_strength
            + 0.25 * recurrence
            + 2.0 * review_not_toxic
            + 1.5 * selective
            + 1.5 * state
            + 1.5 * ms_anchor
            + 1.0 * target_quality_proxy
            + 1.0 * genetics
            + 0.5 * delivery_annotation
            - 2.0 * prior_blocked
        )
        promote = (
            review_not_toxic
            and reversal_strength >= 8
            and state
            and ms_anchor
            and target_quality_proxy
            and not prior_blocked
            and delivery_annotation
        )
        blockers = []
        if not review_not_toxic:
            blockers.append("toxic_or_generic_reason")
        if reversal_strength < 8:
            blockers.append("weak_l1000_reversal")
        if not selective:
            blockers.append("generic_ifn_reversal_not_selective")
        if not state:
            blockers.append("no_target_cellstate_recurrence")
        if not ms_anchor:
            blockers.append("no_ms_target_anchor")
        if not target_quality_proxy:
            blockers.append("weak_target_quality_proxy")
        if prior_blocked:
            blockers.append("prior_or_safety_blocked")

        rows.append(
            {
                "pert_id": s(r.get("pert_id")),
                "compound": s(r.get("cmap_name")),
                "target_gene": gene,
                "moa": s(r.get("moa")),
                "opposite_queries": s(r.get("opposite_queries")),
                "best_opposite_rank": f(r.get("best_opposite_rank", 999)),
                "min_opposite_qval": f(r.get("min_opposite_qval", 1), 1),
                "max_opposite_abs_score": reversal_strength,
                "recurrence_strength": recurrence,
                "l1000_selectivity_call": s(r.get("l1000_selectivity_call")),
                "review_not_toxic_or_generic": review_not_toxic,
                "target_state_recurrence": state,
                "c15_trend_positive_disease_count": c15_pos,
                "c15_strict_positive_context_count": c15_strict,
                "positive_c15_contexts": s(r166.get("positive_c15_contexts", r167.get("positive_c15_contexts", ""))),
                "ms_anchor": ms_anchor,
                "ms_delta_log2": ms_delta,
                "ms_p": ms_p,
                "ms_max_l2g_score": ms_l2g,
                "ms_max_qtl_h4": ms_qtl,
                "genetics_annotation": genetics,
                "chembl_target_id": chembl,
                "druggable_activity_count": activity,
                "target_quality_proxy": target_quality_proxy,
                "prior_blocked_annotation": prior_blocked,
                "delivery_annotation": delivery_annotation,
                "repurposing_pivot_score": score,
                "promote": promote,
                "blockers": ";".join(blockers),
                "strict_reason": reason,
                "prior_annotation": prior_text,
            }
        )

rank = pd.DataFrame(rows).sort_values(["promote", "repurposing_pivot_score"], ascending=[False, False])
rank.to_csv(OUT / "l1000_repurposing_deconvolution_rank.tsv", sep="\t", index=False)
rank.head(50).to_csv(OUT / "top_l1000_repurposing_deconvolution.tsv", sep="\t", index=False)
promoted = rank[rank["promote"]]
branch = "PROMOTE_L1000_REPURPOSING_CANDIDATE" if len(promoted) else "NO_L1000_REPURPOSING_PROMOTION"
best = rank.iloc[0].to_dict() if len(rank) else {}
summary = {
    "branch_call": branch,
    "review_rows_tested": int(len(rank)),
    "promoted_candidates": (promoted["compound"] + "/" + promoted["target_gene"]).tolist() if len(promoted) else [],
    "best_candidate": f"{best.get('compound', '')}/{best.get('target_gene', '')}",
    "best_score": float(best.get("repurposing_pivot_score", 0)),
    "best_blockers": best.get("blockers", ""),
    "interpretation": (
        "PARK_REVIEW L1000 compounds retain reversal signal, but target-level state/MS/quality gates "
        "do not converge strongly enough for a V3 repurposing claim."
    ),
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

report = f"""# Wave169 L1000 Repurposing Deconvolution Pivot

## Branch call
`{branch}`

## Result
- Review target rows tested: `{len(rank)}`.
- Promoted candidates: `{len(promoted)}`.
- Best candidate: `{best.get('compound', '')}/{best.get('target_gene', '')}`.
- Best score: `{best.get('repurposing_pivot_score', 0)}`.
- Best blockers: `{best.get('blockers', '')}`.

## Interpretation
This branch starts with compound reversal. It does not currently produce a
therapeutic claim because reversal, target recurrence, MS anchor, target
quality, and prior/safety status do not converge on one candidate.
"""
(OUT / "REPORT.md").write_text(report)

print(json.dumps(summary, indent=2))
