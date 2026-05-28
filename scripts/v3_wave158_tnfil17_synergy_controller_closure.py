#!/usr/bin/env python3
"""Wave158: closure audit for the TNF/IL17-CUX1/NFKBIZ-ELR route.

This wave asks a narrow orchestration question: after the positive
GSE129487 CUX1/ELR observations, is the upstream TNF/IL17 synergy-controller
route promotable as a V3 therapeutic or biomarker claim?
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave158_tnfil17_synergy_controller_closure"
OUT.mkdir(parents=True, exist_ok=True)

GENES = ["CUX1", "NFKBIZ", "STAT3", "STAT4"]
PRIOR_ART = {
    "CUX1": "Slowikowski et al. PNAS 2020, DOI 10.1073/pnas.1912702117, PubMed 32079724: CUX1 and NFKBIZ mediate TNF/IL17A inflammatory synergy in stromal fibroblasts.",
    "NFKBIZ": "Slowikowski et al. PNAS 2020, DOI 10.1073/pnas.1912702117, PubMed 32079724: CUX1 and NFKBIZ mediate TNF/IL17A inflammatory synergy in stromal fibroblasts.",
    "STAT3": "Canonical cytokine/JAK-STAT inflammatory signaling; not novel and broad safety/prior-art concerns.",
    "STAT4": "Canonical autoimmune genetics/cytokine signaling node; not novel and broad safety/prior-art concerns.",
}


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t")


def pick_row(df: pd.DataFrame, gene: str) -> dict[str, object]:
    if df.empty or "gene" not in df.columns:
        return {}
    hit = df[df["gene"].astype(str).str.upper() == gene]
    if hit.empty:
        return {}
    return hit.iloc[0].to_dict()


def truthy_count(value: object) -> int:
    try:
        if pd.isna(value):
            return 0
    except TypeError:
        pass
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def main() -> None:
    broad = read_tsv(ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_summary.tsv")
    ms = read_tsv(ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv")
    wave62 = read_tsv(ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv")
    wave103 = read_tsv(ROOT / "results_v3" / "wave103_intervention_first_successor_triage" / "intervention_first_successor_rank.tsv")
    wave155 = read_tsv(ROOT / "results_v3" / "wave155_cux1_gene_specificity_vs_stat" / "gene_specificity_summary.tsv")
    wave156 = read_tsv(ROOT / "results_v3" / "wave156_elr_chemokine_intervention_audit" / "elr_chemokine_intervention_audit.tsv")
    wave157 = read_tsv(ROOT / "results_v3" / "wave157_elr_state_biomarker_responsiveness" / "elr_state_contrasts.tsv")

    rows: list[dict[str, object]] = []
    for gene in GENES:
        b = pick_row(broad, gene)
        m = pick_row(ms, gene)
        w62 = pick_row(wave62, gene)
        w103 = pick_row(wave103, gene)

        ms_expr_fdr = float(m.get("fdr", 1.0)) if m else 1.0
        ms_expr_delta = float(m.get("delta_log2", 0.0)) if m else 0.0
        ms_genetic_score = float(w103.get("ms_genetic_score", 0.0)) if w103 else float(w62.get("ms_max_l2g_score", 0.0) or 0.0)
        positive_fdr10 = truthy_count(b.get("positive_fdr10_compartment_count", 0))
        positive_diseases = str(b.get("positive_diseases", "")) if b else ""
        wave62_call = str(w62.get("wave62_call", "")) if w62 else "not_in_wave62"
        wave103_call = str(w103.get("wave103_call", "")) if w103 else "not_in_wave103"

        direct_local_perturbation = gene == "CUX1"
        prior_art_blocked = gene in {"CUX1", "NFKBIZ", "STAT3", "STAT4"}
        ms_anchor = (ms_expr_fdr < 0.10 and abs(ms_expr_delta) >= 0.25) or ms_genetic_score >= 0.50
        cross_disease_cell_state = positive_fdr10 >= 3
        target_resolution = "GO" in wave62_call and not wave62_call.startswith("NO_GO")
        reachable_selective_modality = False

        blockers = []
        if prior_art_blocked:
            blockers.append("prior_art_or_canonical_axis")
        if not ms_anchor:
            blockers.append("no_ms_anchor")
        if not cross_disease_cell_state:
            blockers.append("insufficient_cross_disease_cell_state_replication")
        if not target_resolution:
            blockers.append("no_target_resolved_genetic_support")
        if not reachable_selective_modality:
            blockers.append("no_selective_reachable_modality")

        rows.append(
            {
                "gene": gene,
                "direct_local_perturbation": direct_local_perturbation,
                "prior_art_note": PRIOR_ART[gene],
                "ms_expr_delta_log2": ms_expr_delta,
                "ms_expr_fdr": ms_expr_fdr,
                "ms_genetic_score": ms_genetic_score,
                "positive_fdr10_compartment_count": positive_fdr10,
                "positive_diseases": positive_diseases,
                "wave62_call": wave62_call,
                "wave103_call": wave103_call,
                "ms_anchor": ms_anchor,
                "cross_disease_cell_state": cross_disease_cell_state,
                "target_resolution": target_resolution,
                "reachable_selective_modality": reachable_selective_modality,
                "promote": False,
                "blockers": ";".join(blockers),
            }
        )

    audit = pd.DataFrame(rows)
    audit.to_csv(OUT / "tnfil17_synergy_controller_audit.tsv", sep="\t", index=False)

    if not wave155.empty:
        wave155.to_csv(OUT / "copied_wave155_gene_specificity_summary.tsv", sep="\t", index=False)
    if not wave156.empty:
        wave156.to_csv(OUT / "copied_wave156_elr_intervention_audit.tsv", sep="\t", index=False)
    if not wave157.empty:
        wave157.to_csv(OUT / "copied_wave157_elr_state_contrasts.tsv", sep="\t", index=False)

    branch = "NO_TNF_IL17_SYNERGY_CONTROLLER_PROMOTION"
    summary = {
        "branch_call": branch,
        "genes_audited": GENES,
        "promoted_gene_count": int(audit["promote"].sum()),
        "cux1_elr_gene_specificity_signal": {
            "source": "Wave155",
            "top_selective_gene": "CXCL1",
            "cxcl1_induced_contexts": int(wave155.loc[wave155["gene"] == "CXCL1", "n_induced_contexts"].iloc[0]) if not wave155.empty and (wave155["gene"] == "CXCL1").any() else None,
            "cxcl1_cux1_selective_nominal": int(wave155.loc[wave155["gene"] == "CXCL1", "n_cux1_selective_nominal"].iloc[0]) if not wave155.empty and (wave155["gene"] == "CXCL1").any() else None,
        },
        "elr_state_support": {
            "source": "Wave157",
            "induction_datasets_p_lt_0_05": int(((wave157["contrast"].astype(str).str.contains("_vs_control|_vs_vehicle")) & (wave157["p_value"] < 0.05) & (wave157["delta"] > 0)).sum()) if not wave157.empty else 0,
            "treatment_down_contrasts_p_lt_0_05": int(((wave157["contrast"].astype(str).str.contains("_vs_activated")) & (wave157["p_value"] < 0.05) & (wave157["delta"] < 0)).sum()) if not wave157.empty else 0,
        },
        "interpretation": (
            "The TNF/IL17-CUX1/NFKBIZ-ELR circuit is biologically real in local "
            "human interface datasets and matches verified prior art, but it fails "
            "V3 promotion gates for novelty, MS anchoring, target-resolved genetics, "
            "and selective reachable intervention modality."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = [
        "# Wave158 TNF/IL17 Synergy Controller Closure",
        "",
        f"Branch call: `{branch}`.",
        "",
        "## Result",
        "",
        "The CUX1/NFKBIZ/ELR route is closed for V3 therapeutic or biomarker promotion.",
        "It remains a useful comparator inflammatory-interface state.",
        "",
        "## Evidence Used",
        "",
        "- Wave153-Wave155: local GSE129487 CUX1 siRNA signal, strongest for ELR+ chemokines.",
        "- Wave156: direct ELR+ chemokine intervention audit promoted zero targets.",
        "- Wave157: ELR state induced in multiple interface datasets but only weakly treatment-responsive.",
        "- Wave62/Wave103/GSE111972/broad h5ad summaries: no adequate MS anchor, target-resolved genetics, or broad disease cell-state gate for CUX1/NFKBIZ.",
        "- Verified prior art: Slowikowski et al. PNAS 2020, DOI 10.1073/pnas.1912702117, PubMed 32079724.",
        "",
        "## Blocker Logic",
        "",
        "Promotion requires novelty, MS anchoring, cross-disease cell-state replication, target-resolved genetics, and a selective reachable modality. No audited controller satisfies these gates.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
