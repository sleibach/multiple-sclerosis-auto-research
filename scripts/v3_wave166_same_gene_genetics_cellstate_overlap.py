#!/usr/bin/env python3
"""Wave166: rank same-gene overlap of genetics-first and cell-state evidence.

After Wave165, borrowed-neighbor druggability is treated as a failed strategy.
This wave asks which genes already carry both target-resolved autoimmune/MS
genetics and local cross-disease cell-state recurrence before any intervention
route is considered.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave166_same_gene_genetics_cellstate_overlap"
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
    m = df[df["gene"] == gene]
    if m.empty:
        return {}
    return m.iloc[0].to_dict()


wave62 = read_tsv("phases/v3/results/wave62_opentargets_target_resolution/target_resolution_summary.tsv")
wave96 = read_tsv("phases/v3/results/wave96_c15orf48_controller_search/pre_donor_controller_rank.tsv")
wave103 = read_tsv("phases/v3/results/wave103_intervention_first_successor_triage/intervention_first_successor_rank.tsv")
wave164 = read_tsv("phases/v3/results/wave164_genetics_first_survivor_audit/genetics_first_survivor_rank.tsv")

genes = sorted(set(wave62.get("gene", [])) | set(wave96.get("gene", [])) | set(wave164.get("gene", [])))

hard_closed_tokens = [
    "no_go",
    "prior_or_local",
    "prior_art",
    "prior_branch_blocker",
    "no_direct_druggable",
    "not_selectively_druggable",
    "NO_GO_PRIOR",
    "NO_GO_NOT_REACHABLE",
    "NO_GO_NO_MS",
]
hard_closed_genes = {
    "SP140",
    "STAT4",
    "STAT3",
    "IL7R",
    "IFI30",
    "GPR183",
    "P2RX7",
    "FPR2",
    "ANXA1",
    "CD300A",
    "CD300E",
    "CD300LF",
    "TYK2",
    "IL12A",
    "IL12B",
    "PTPN2",
    "IRF5",
    "NOD2",
    "RIPK2",
    "INAVA",
}

rows = []
for gene in genes:
    r62 = first(wave62, gene)
    r96 = first(wave96, gene)
    r103 = first(wave103, gene)
    r164 = first(wave164, gene)
    if not (r62 or r96 or r164):
        continue

    strong_l2g = f(r62.get("strong_l2g_disease_count", r164.get("strong_l2g_disease_count", 0)))
    strong_qtl = f(r62.get("strong_qtl_coloc_disease_count", r164.get("strong_qtl_coloc_disease_count", 0)))
    ms_l2g = f(r62.get("ms_max_l2g_score", r164.get("ms_max_l2g_score", 0)))
    ms_qtl = f(r62.get("ms_max_qtl_h4", r164.get("ms_max_qtl_h4", 0)))
    c15_pos_disease = f(r96.get("c15_trend_positive_disease_count", 0))
    c15_strict_context = f(r96.get("c15_strict_positive_context_count", 0))
    c15_myeloid = f(r96.get("c15_myeloid_positive_context_count", 0))
    ms_delta = f(r96.get("ms_delta_log2", r62.get("ms_wm_delta_log2", 0)))
    ms_p = f(r96.get("ms_p", r62.get("ms_wm_p", 1)), 1)
    ms_fdr = f(r96.get("ms_fdr", r62.get("ms_wm_fdr", 1)), 1)
    w37_lfc = f(r96.get("w37_contrast_lfc", 0))
    w37_fdr = f(r96.get("w37_contrast_fdr", 1), 1)
    activity = f(r62.get("druggable_activity_count", r164.get("druggable_activity_count", 0)))
    chembl = s(r62.get("chembl_target_id", r164.get("chembl_target_id", "")))

    genetics_gate = (ms_l2g >= 0.5 or ms_qtl >= 0.8) and (strong_l2g >= 3 or strong_qtl >= 3)
    same_gene_cellstate_gate = c15_pos_disease >= 2 and c15_strict_context >= 1
    ms_expression_trend = ms_delta > 0 and ms_p < 0.25
    perturb_trend = abs(w37_lfc) >= 0.25 and w37_fdr < 0.95
    reachable = bool(chembl) or activity >= 25
    prior_text = " ".join(
        [
            s(r62.get("manual_blocker", "")),
            s(r62.get("prior_context_blocker", "")),
            s(r62.get("wave62_call", "")),
            s(r103.get("call", "")),
            s(r103.get("blockers", "")),
            s(r164.get("blockers", "")),
        ]
    )
    hard_closed = gene in hard_closed_genes or any(tok.lower() in prior_text.lower() for tok in hard_closed_tokens)

    score = (
        3 * genetics_gate
        + 3 * same_gene_cellstate_gate
        + 1.5 * ms_expression_trend
        + 1.0 * perturb_trend
        + 1.0 * reachable
        + 0.2 * min(strong_l2g + strong_qtl, 10)
        + 0.2 * min(c15_pos_disease + c15_strict_context, 10)
        - 2.5 * hard_closed
    )
    candidate_for_route = genetics_gate and same_gene_cellstate_gate and not hard_closed
    rows.append(
        {
            "gene": gene,
            "score": score,
            "candidate_for_route": candidate_for_route,
            "genetics_gate": genetics_gate,
            "same_gene_cellstate_gate": same_gene_cellstate_gate,
            "ms_expression_trend": ms_expression_trend,
            "perturbation_trend": perturb_trend,
            "reachable": reachable,
            "hard_closed_or_prior_blocked": hard_closed,
            "strong_l2g_disease_count": strong_l2g,
            "strong_l2g_diseases": s(r62.get("strong_l2g_diseases", r164.get("strong_l2g_diseases", ""))),
            "strong_qtl_coloc_disease_count": strong_qtl,
            "strong_qtl_coloc_diseases": s(r62.get("strong_qtl_coloc_diseases", r164.get("strong_qtl_coloc_diseases", ""))),
            "ms_max_l2g_score": ms_l2g,
            "ms_max_qtl_h4": ms_qtl,
            "c15_trend_positive_disease_count": c15_pos_disease,
            "c15_strict_positive_context_count": c15_strict_context,
            "c15_myeloid_positive_context_count": c15_myeloid,
            "positive_c15_contexts": s(r96.get("positive_c15_contexts", "")),
            "best_c15_context": s(r96.get("best_c15_context", "")),
            "ms_delta_log2": ms_delta,
            "ms_p": ms_p,
            "ms_fdr": ms_fdr,
            "w37_contrast_lfc": w37_lfc,
            "w37_contrast_fdr": w37_fdr,
            "chembl_target_id": chembl,
            "druggable_activity_count": activity,
            "wave62_call": s(r62.get("wave62_call", "")),
            "wave103_call": s(r103.get("call", "")),
            "wave164_blockers": s(r164.get("blockers", "")),
            "prior_text": prior_text,
        }
    )

rank = pd.DataFrame(rows).sort_values(["candidate_for_route", "score"], ascending=[False, False])
rank.to_csv(OUT / "same_gene_genetics_cellstate_rank.tsv", sep="\t", index=False)
top = rank.head(50)
top.to_csv(OUT / "top_same_gene_genetics_cellstate.tsv", sep="\t", index=False)
eligible = rank[rank["candidate_for_route"]]
eligible.head(50).to_csv(OUT / "eligible_same_gene_routes.tsv", sep="\t", index=False)

if len(eligible):
    branch = "SAME_GENE_GENETICS_CELLSTATE_CANDIDATES_FOUND"
    selected = eligible.iloc[0].to_dict()
else:
    branch = "NO_UNBLOCKED_SAME_GENE_GENETICS_CELLSTATE_ROUTE"
    selected = rank.iloc[0].to_dict()

summary = {
    "branch_call": branch,
    "genes_ranked": int(len(rank)),
    "eligible_routes": int(len(eligible)),
    "selected_gene": selected["gene"],
    "selected_score": float(selected["score"]),
    "selected_flags": {
        "genetics_gate": bool(selected["genetics_gate"]),
        "same_gene_cellstate_gate": bool(selected["same_gene_cellstate_gate"]),
        "ms_expression_trend": bool(selected["ms_expression_trend"]),
        "perturbation_trend": bool(selected["perturbation_trend"]),
        "reachable": bool(selected["reachable"]),
        "hard_closed_or_prior_blocked": bool(selected["hard_closed_or_prior_blocked"]),
    },
    "interpretation": (
        "Same-gene overlap is now the preferred search space; eligible rows, if any, "
        "should be tested next for intervention feasibility instead of using neighbor-borrowed druggability."
    ),
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

report = f"""# Wave166 Same-Gene Genetics + Cell-State Overlap

## Branch call
`{branch}`

## Result
- Genes ranked: `{len(rank)}`.
- Eligible same-gene routes: `{len(eligible)}`.
- Selected gene for next forcing test: `{selected['gene']}`.
- Selected score: `{selected['score']}`.

## Rationale
Wave165 showed that borrowing a druggable neighbor from a genetic anchor loses
the central evidence. This wave therefore ranks only genes where genetics and
cell-state recurrence coexist on the same node before asking about modality.
"""
(OUT / "REPORT.md").write_text(report)

print(json.dumps(summary, indent=2))
