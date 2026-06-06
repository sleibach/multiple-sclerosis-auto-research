#!/usr/bin/env python3
"""Wave164: genetics-first survivor audit after route-map depletion."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave164_genetics_first_survivor_audit"
OUT.mkdir(parents=True, exist_ok=True)

CLOSED = {
    "IL7R", "SP140", "STAT4", "GPR65", "PTGER4", "TNFRSF1A", "CD58",
    "CD274", "CXCR2", "CCL20", "CTSB", "CD44", "SELL", "IL23A",
}


def main() -> None:
    w62 = pd.read_csv(ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv", sep="\t", low_memory=False)
    broad = pd.read_csv(ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_summary.tsv", sep="\t", low_memory=False)
    w103 = pd.read_csv(ROOT / "phases/v3/results" / "wave103_intervention_first_successor_triage" / "intervention_first_successor_rank.tsv", sep="\t", low_memory=False)

    b = broad.set_index("gene")
    i103 = w103.set_index("gene")
    rows = []
    for _, r in w62.iterrows():
        gene = str(r["gene"])
        if gene in CLOSED:
            continue
        br = b.loc[gene].to_dict() if gene in b.index else {}
        x103 = i103.loc[gene].to_dict() if gene in i103.index else {}
        strong_l2g = int(float(r.get("strong_l2g_disease_count", 0) or 0))
        strong_qtl = int(float(r.get("strong_qtl_coloc_disease_count", 0) or 0))
        ms_l2g = float(r.get("ms_max_l2g_score", 0) or 0)
        ms_qtl = float(r.get("ms_max_qtl_h4", 0) or 0)
        local_pos = int(float(r.get("local_positive_disease_count", 0) or 0))
        broad_pos = int(float(br.get("positive_disease_count", 0) or 0)) if br else local_pos
        broad_fdr10 = int(float(br.get("positive_fdr10_compartment_count", 0) or 0)) if br else 0
        raw_chembl = r.get("chembl_target_id", "")
        chembl = "" if pd.isna(raw_chembl) else str(raw_chembl)
        activity = int(float(r.get("druggable_activity_count", 0) or 0))
        manual_block = str(r.get("manual_blocker", "") or "")
        prior_block = str(r.get("prior_context_blocker", "") or "")
        w103_call = str(x103.get("wave103_call", "")) if x103 else ""

        genetics = strong_l2g >= 3 and strong_qtl >= 2 and (ms_l2g >= 0.5 or ms_qtl >= 0.8)
        cellstate = broad_pos >= 2 or broad_fdr10 >= 1
        reachable = bool(chembl) or activity > 0
        unblocked = not manual_block and not prior_block and "NO_GO" not in w103_call
        score = (
            2 * strong_l2g
            + 1.5 * strong_qtl
            + 2 * (ms_l2g >= 0.5)
            + 2 * (ms_qtl >= 0.8)
            + broad_pos
            + broad_fdr10
            + 2 * int(reachable)
            - 3 * int(not unblocked)
        )
        blockers = []
        if not genetics:
            blockers.append("insufficient_cross_disease_ms_genetic_anchor")
        if not cellstate:
            blockers.append("insufficient_cell_state_support")
        if not reachable:
            blockers.append("no_direct_druggable_modality")
        if not unblocked:
            blockers.append("prior_or_local_no_go_blocker")

        rows.append({
            "gene": gene,
            "score": score,
            "wave62_call": r.get("wave62_call", ""),
            "strong_l2g_disease_count": strong_l2g,
            "strong_l2g_diseases": r.get("strong_l2g_diseases", ""),
            "strong_qtl_coloc_disease_count": strong_qtl,
            "strong_qtl_coloc_diseases": r.get("strong_qtl_coloc_diseases", ""),
            "ms_max_l2g_score": ms_l2g,
            "ms_max_qtl_h4": ms_qtl,
            "broad_positive_disease_count": broad_pos,
            "broad_positive_fdr10_compartment_count": broad_fdr10,
            "broad_positive_diseases": br.get("positive_diseases", r.get("local_positive_diseases", "")) if br else r.get("local_positive_diseases", ""),
            "chembl_target_id": chembl,
            "druggable_activity_count": activity,
            "manual_blocker": manual_block,
            "prior_context_blocker": prior_block,
            "wave103_call": w103_call,
            "genetics_gate": genetics,
            "cellstate_gate": cellstate,
            "reachable_gate": reachable,
            "unblocked_gate": unblocked,
            "promote": False,
            "blockers": ";".join(blockers),
        })

    out = pd.DataFrame(rows).sort_values("score", ascending=False)
    out.to_csv(OUT / "genetics_first_survivor_rank.tsv", sep="\t", index=False)
    top = out.head(25)
    top.to_csv(OUT / "top_genetics_first_survivors.tsv", sep="\t", index=False)

    branch = "GENETICS_FIRST_MECHANISM_BUT_NO_DIRECT_TARGET"
    best = top.iloc[0].to_dict()
    summary = {
        "branch_call": branch,
        "candidates_ranked": int(out.shape[0]),
        "top_gene": best["gene"],
        "top_gene_score": float(best["score"]),
        "top_gene_blockers": best["blockers"],
        "promoted_candidates": [],
        "interpretation": (
            "The strongest remaining genetics-first candidates are credible "
            "mechanistic anchors, but none simultaneously has direct druggability, "
            "cell-state support, and unblocked therapeutic direction."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUT / "REPORT.md").write_text(
        "# Wave164 Genetics-First Survivor Audit\n\n"
        f"Branch call: `{branch}`.\n\n"
        f"Top gene: `{summary['top_gene']}`; blockers: `{summary['top_gene_blockers']}`.\n\n"
        "No candidate is promoted; use the top genes as mechanistic anchors only.\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
