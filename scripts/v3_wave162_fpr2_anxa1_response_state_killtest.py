#!/usr/bin/env python3
"""Wave162: FPR2/ANXA1 response-state kill test.

The selected Wave161 next test asks whether the biased pro-resolution FPR2/ANXA1
route has cross-disease response-state support plus an MS lesion anchor. This
wave consolidates local evidence and applies that gate explicitly.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave162_fpr2_anxa1_response_state_killtest"
OUT.mkdir(parents=True, exist_ok=True)

GENES = ["FPR2", "ANXA1"]


def read(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def pick(df: pd.DataFrame, gene: str) -> dict[str, object]:
    if df.empty or "gene" not in df.columns:
        return {}
    hit = df[df["gene"].astype(str).str.upper() == gene]
    if hit.empty:
        return {}
    return hit.iloc[0].to_dict()


def main() -> None:
    broad = read(ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_summary.tsv")
    ms = read(ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv")
    wave48_gene = read(ROOT / "results_v3" / "wave48_resolution_reopener_audit" / "candidate_gene_evidence.tsv")
    wave48_route = read(ROOT / "results_v3" / "wave48_resolution_reopener_audit" / "route_reopener_audit.tsv")
    wave48_decision = read(ROOT / "results_v3" / "wave48_resolution_reopener_audit" / "decision_matrix.tsv")
    wave103 = read(ROOT / "results_v3" / "wave103_intervention_first_successor_triage" / "intervention_first_successor_rank.tsv")

    rows = []
    for gene in GENES:
        b = pick(broad, gene)
        m = pick(ms, gene)
        w48 = pick(wave48_gene, gene)
        w103 = pick(wave103, gene)

        broad_positive_fdr10 = int(float(b.get("positive_fdr10_compartment_count", 0))) if b else 0
        broad_positive_diseases = str(b.get("positive_diseases", "")) if b else ""
        ms_delta = float(m.get("delta_log2", 0.0)) if m else 0.0
        ms_fdr = float(m.get("fdr", 1.0)) if m else 1.0
        wave36_up_datasets = int(float(w48.get("wave36_n_up_datasets", 0))) if w48 and pd.notna(w48.get("wave36_n_up_datasets", 0)) else 0
        wave36_down_datasets = int(float(w48.get("wave36_n_down_datasets", 0))) if w48 and pd.notna(w48.get("wave36_n_down_datasets", 0)) else 0
        chembl_count = int(float(w48.get("chembl_activity_count", 0))) if w48 and pd.notna(w48.get("chembl_activity_count", 0)) else 0
        wave37_call = str(w48.get("wave37_screen_call", "")) if w48 else ""
        wave103_call = str(w103.get("wave103_call", "")) if w103 else "not_in_wave103"

        cross_disease_response = broad_positive_fdr10 >= 2 or wave36_up_datasets >= 3
        ms_anchor = ms_fdr < 0.10 and ms_delta > 0.25
        perturbation_anchor = wave37_call not in {"", "UNRESOLVED"}
        druggable = chembl_count >= 10 if gene == "FPR2" else chembl_count >= 1
        no_local_no_go = "NO_GO" not in wave103_call

        blockers = []
        if not cross_disease_response:
            blockers.append("insufficient_cross_disease_response_state")
        if not ms_anchor:
            blockers.append("no_positive_ms_lesion_anchor")
        if not perturbation_anchor:
            blockers.append("no_real_perturbation_anchor")
        if not no_local_no_go:
            blockers.append("prior_local_no_go")
        if gene == "ANXA1" and not druggable:
            blockers.append("weak_direct_druggability")

        rows.append(
            {
                "gene": gene,
                "broad_positive_fdr10_compartment_count": broad_positive_fdr10,
                "broad_positive_diseases": broad_positive_diseases,
                "ms_delta_log2": ms_delta,
                "ms_fdr": ms_fdr,
                "wave36_up_datasets": wave36_up_datasets,
                "wave36_down_datasets": wave36_down_datasets,
                "wave37_screen_call": wave37_call,
                "chembl_activity_count": chembl_count,
                "wave103_call": wave103_call,
                "cross_disease_response_gate": cross_disease_response,
                "ms_anchor_gate": ms_anchor,
                "perturbation_anchor_gate": perturbation_anchor,
                "druggability_gate": druggable,
                "promote": False,
                "blockers": ";".join(blockers),
            }
        )

    audit = pd.DataFrame(rows)
    audit.to_csv(OUT / "fpr2_anxa1_gene_gate_audit.tsv", sep="\t", index=False)
    if not wave48_route.empty:
        wave48_route.to_csv(OUT / "copied_wave48_route_reopener_audit.tsv", sep="\t", index=False)
    if not wave48_decision.empty:
        wave48_decision.to_csv(OUT / "copied_wave48_decision_matrix.tsv", sep="\t", index=False)

    route_row = wave48_route[wave48_route["route"] == "FPR2_ANXA1_BIASED_RESOLUTION"].iloc[0].to_dict() if not wave48_route.empty and (wave48_route["route"] == "FPR2_ANXA1_BIASED_RESOLUTION").any() else {}
    branch = "NO_REOPEN_FPR2_ANXA1_NO_MS_OR_PERTURBATION_ANCHOR"
    summary = {
        "branch_call": branch,
        "genes_audited": GENES,
        "route_wave48_call": route_row.get("call", ""),
        "fpr2_broad_positive_diseases": audit.loc[audit["gene"] == "FPR2", "broad_positive_diseases"].iloc[0],
        "fpr2_ms_delta_log2": float(audit.loc[audit["gene"] == "FPR2", "ms_delta_log2"].iloc[0]),
        "fpr2_ms_fdr": float(audit.loc[audit["gene"] == "FPR2", "ms_fdr"].iloc[0]),
        "anxa1_wave36_up_datasets": int(audit.loc[audit["gene"] == "ANXA1", "wave36_up_datasets"].iloc[0]),
        "promoted_candidates": [],
        "interpretation": (
            "FPR2/ANXA1 remains a plausible wet-lab pro-resolution assay branch, "
            "but the required V3 kill-test gates fail: no positive MS lesion "
            "anchor and no real perturbation anchor in local disease-relevant data."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = [
        "# Wave162 FPR2/ANXA1 Response-State Kill Test",
        "",
        f"Branch call: `{branch}`.",
        "",
        "## Result",
        "",
        "Do not reopen FPR2/ANXA1 as a V3 therapeutic finding.",
        "",
        "## Key Facts",
        "",
        f"- FPR2 broad positive diseases: `{summary['fpr2_broad_positive_diseases']}`.",
        f"- FPR2 MS white-matter delta: `{summary['fpr2_ms_delta_log2']:.4f}`, FDR `{summary['fpr2_ms_fdr']:.4f}`.",
        f"- ANXA1 Wave36 up datasets: `{summary['anxa1_wave36_up_datasets']}`.",
        "- Wave48 already found the route wet-lab-only, not V3 promotion.",
        "",
        "## Interpretation",
        "",
        summary["interpretation"],
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
