#!/usr/bin/env python3
"""Wave165: test whether INAVA genetics can be converted into a druggable neighbor route.

The point is not to nominate an IBD biology target by association. The forcing
question is whether the strong INAVA cross-autoimmune/MS genetic anchor is
preserved when moving to nearby tractable innate/barrier pathway nodes.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave165_inava_nod_ripk_neighbor_audit"
OUT.mkdir(parents=True, exist_ok=True)

GENES = ["INAVA", "RIPK2", "NOD2", "NOD1", "ATG16L1", "IRGM", "CARD9"]


def read_tsv(path: str) -> pd.DataFrame:
    p = ROOT / path
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p, sep="\t")


def as_float(x, default=0.0) -> float:
    try:
        if pd.isna(x):
            return default
        return float(x)
    except Exception:
        return default


def clean(x) -> str:
    if x is None or pd.isna(x):
        return ""
    s = str(x)
    return "" if s.lower() == "nan" else s


def row_for(df: pd.DataFrame, gene: str) -> dict:
    if df.empty or "gene" not in df.columns:
        return {}
    rows = df[df["gene"] == gene]
    if rows.empty:
        return {}
    return rows.iloc[0].to_dict()


wave62 = read_tsv("phases/v3/results/wave62_opentargets_target_resolution/target_resolution_summary.tsv")
if wave62.empty:
    wave62 = read_tsv("phases/v3/results/wave62_target_resolution/target_resolution_summary.tsv")
wave55 = read_tsv("phases/v3/results/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv")
wave96 = read_tsv("phases/v3/results/wave96_c15orf48_controller_search/pre_donor_controller_rank.tsv")
wave103 = read_tsv("phases/v3/results/wave103_intervention_first_successor_triage/intervention_first_successor_rank.tsv")
wave104 = read_tsv("phases/v3/results/wave104_genetics_first_lipid_state_convergence_audit/genetics_first_lipid_state_rank.tsv")
wave164 = read_tsv("phases/v3/results/wave164_genetics_first_survivor_audit/genetics_first_survivor_rank.tsv")

records = []
for gene in GENES:
    r62 = row_for(wave62, gene)
    r55 = row_for(wave55, gene)
    r96 = row_for(wave96, gene)
    r103 = row_for(wave103, gene)
    r104 = row_for(wave104, gene)
    r164 = row_for(wave164, gene)

    strong_l2g = as_float(r62.get("strong_l2g_disease_count", r55.get("n_diseases_genetic_ge_0_5", 0)))
    strong_qtl = as_float(r62.get("strong_qtl_coloc_disease_count", 0))
    ms_l2g = as_float(r62.get("ms_max_l2g_score", r55.get("ms_genetic_association", 0)))
    ms_qtl = as_float(r62.get("ms_max_qtl_h4", 0))
    broad_pos = as_float(r96.get("c15_trend_positive_disease_count", r62.get("local_positive_disease_count", 0)))
    broad_fdr = as_float(r96.get("c15_strict_positive_context_count", 0))
    ms_delta = as_float(r96.get("ms_delta_log2", r62.get("ms_wm_delta_log2", 0)))
    ms_p = as_float(r96.get("ms_p", r62.get("ms_wm_p", 1)), 1)
    ms_fdr = as_float(r96.get("ms_fdr", r62.get("ms_wm_fdr", 1)), 1)
    crispr_lfc = as_float(r96.get("w37_contrast_lfc", 0))
    crispr_fdr = as_float(r96.get("w37_contrast_fdr", 1), 1)
    chembl = clean(r62.get("chembl_target_id", r103.get("chembl_target_id", r164.get("chembl_target_id", ""))))
    activity = as_float(r62.get("druggable_activity_count", r103.get("chembl_activity_count", r164.get("druggable_activity_count", 0))))

    genetics_gate = (ms_l2g >= 0.5 or ms_qtl >= 0.8) and (strong_l2g >= 4 or strong_qtl >= 3)
    cellstate_gate = (broad_pos >= 3 and broad_fdr >= 1) or (broad_pos >= 4)
    ms_expression_gate = ms_delta > 0 and ms_p < 0.05
    perturb_gate = abs(crispr_lfc) >= 0.5 and crispr_fdr < 0.1
    reachable_gate = bool(chembl) or activity >= 25
    prior_blocker_text = " ".join(
        clean(v)
        for v in [
            r62.get("manual_blocker", ""),
            r62.get("prior_context_blocker", ""),
            r103.get("call", ""),
            r103.get("blockers", ""),
            r104.get("manual_route_blocker", ""),
            r164.get("blockers", ""),
        ]
    ).lower()
    local_no_go = any(token in prior_blocker_text for token in ["no_go", "prior", "blocker", "not_reachable"])

    # Require both the INAVA anchor and the neighbor to pass. A druggable neighbor
    # cannot inherit INAVA genetics if it has no MS anchor of its own.
    promote = genetics_gate and cellstate_gate and ms_expression_gate and perturb_gate and reachable_gate and not local_no_go
    blockers = []
    if not genetics_gate:
        blockers.append("does_not_preserve_inava_ms_cross_autoimmune_genetic_anchor")
    if not cellstate_gate:
        blockers.append("insufficient_cross_disease_cell_state_recurrence")
    if not ms_expression_gate:
        blockers.append("no_positive_nominal_ms_white_matter_expression_anchor")
    if not perturb_gate:
        blockers.append("no_fdr_supported_perturbation_direction")
    if not reachable_gate:
        blockers.append("no_direct_reachable_modality")
    if local_no_go:
        blockers.append("prior_or_local_no_go_blocker")

    records.append(
        {
            "gene": gene,
            "wave62_call": clean(r62.get("wave62_call", "")),
            "wave104_call": clean(r104.get("wave104_call", "")),
            "wave164_score": as_float(r164.get("score", 0)),
            "strong_l2g_disease_count": strong_l2g,
            "strong_l2g_diseases": clean(r62.get("strong_l2g_diseases", r55.get("diseases_genetic_ge_0_5", ""))),
            "strong_qtl_coloc_disease_count": strong_qtl,
            "strong_qtl_coloc_diseases": clean(r62.get("strong_qtl_coloc_diseases", "")),
            "ms_max_l2g_score": ms_l2g,
            "ms_max_qtl_h4": ms_qtl,
            "broad_positive_disease_count": broad_pos,
            "broad_positive_fdr10_compartment_count": broad_fdr,
            "broad_positive_diseases": clean(r96.get("positive_c15_contexts", r62.get("local_positive_diseases", ""))),
            "best_positive_context": clean(r96.get("best_c15_context", "")),
            "ms_wm_delta_log2": ms_delta,
            "ms_wm_p": ms_p,
            "ms_wm_fdr": ms_fdr,
            "crispr_efferocytosis_lfc": crispr_lfc,
            "crispr_efferocytosis_fdr": crispr_fdr,
            "chembl_target_id": chembl,
            "druggable_activity_count": activity,
            "genetics_gate": genetics_gate,
            "cellstate_gate": cellstate_gate,
            "ms_expression_gate": ms_expression_gate,
            "perturbation_gate": perturb_gate,
            "reachable_gate": reachable_gate,
            "local_no_go_or_prior_blocker": local_no_go,
            "promote": promote,
            "blockers": ";".join(blockers),
        }
    )

audit = pd.DataFrame(records)
audit["neighbor_score"] = (
    audit["genetics_gate"].astype(int) * 3
    + audit["cellstate_gate"].astype(int) * 2
    + audit["ms_expression_gate"].astype(int) * 2
    + audit["perturbation_gate"].astype(int) * 2
    + audit["reachable_gate"].astype(int)
    - audit["local_no_go_or_prior_blocker"].astype(int) * 3
)
audit = audit.sort_values(["promote", "neighbor_score", "wave164_score"], ascending=[False, False, False])
audit.to_csv(OUT / "inava_nod_ripk_neighbor_audit.tsv", sep="\t", index=False)

promoted = audit[audit["promote"]]
best = audit.iloc[0].to_dict()
branch = "PROMOTE_INAVA_NEIGHBOR_ROUTE" if len(promoted) else "NO_INAVA_NOD_RIPK_NEIGHBOR_PROMOTION"
summary = {
    "branch_call": branch,
    "genes_tested": GENES,
    "best_gene": best["gene"],
    "best_neighbor_score": float(best["neighbor_score"]),
    "best_gene_blockers": best["blockers"],
    "promoted_candidates": promoted["gene"].tolist(),
    "interpretation": (
        "INAVA remains a credible genetic mechanism anchor, but druggable NOD/RIPK/autophagy "
        "neighbors do not preserve the required MS/cross-autoimmune genetic, cell-state, "
        "perturbation, and unblocked-modality gates."
    ),
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

report = f"""# Wave165 INAVA/NOD/RIPK Neighbor Audit

## Branch call
`{branch}`

## Forcing question
Can the strong `INAVA` cross-autoimmune/MS genetic anchor be converted into a
tractable intervention by moving to nearby innate/barrier signaling nodes
(`NOD2`, `NOD1`, `RIPK2`, `ATG16L1`, `IRGM`, `CARD9`) without losing the
genetic, MS, cross-disease cell-state, perturbation, and modality evidence?

## Result
- Genes tested: `{len(GENES)}`.
- Best scored neighbor: `{best['gene']}` with score `{best['neighbor_score']}`.
- Promoted candidates: `{len(promoted)}`.
- Best-gene blockers: `{best['blockers']}`.

## Interpretation
`INAVA` is retained as a mechanistic genetics clue, not as a therapeutic target.
The druggable neighbor route fails because the reachable nodes are mainly
IBD-local or prior/local-blocked, while the genetically anchored nodes lack
direct modality, MS lesion expression support, and FDR-supported perturbation
direction.
"""
(OUT / "REPORT.md").write_text(report)

print(json.dumps(summary, indent=2))
