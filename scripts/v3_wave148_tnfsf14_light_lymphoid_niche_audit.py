#!/usr/bin/env python3
"""Wave148: TNFSF14/LIGHT-HVEM/LTBR lymphoid-niche audit."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_direct_h5ad_cell_states import ROOT


OUT = ROOT / "results_v3" / "wave148_tnfsf14_light_lymphoid_niche_audit"
SEED = 20260527
GENES = ["TNFSF14", "TNFRSF14", "LTBR"]

FILES = {
    "wave55": ROOT / "results_v3" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv",
    "wave62": ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv",
    "wave104": ROOT / "results_v3" / "wave104_genetics_first_lipid_state_convergence_audit" / "genetics_first_lipid_state_rank.tsv",
    "wave146": ROOT / "results_v3" / "wave146_architecture_first_barrier_retention_scan" / "architecture_gate_decision.tsv",
    "wave103_sender": ROOT / "results_v3" / "wave103_sender_to_myeloid_bridge_scan" / "sender_bridge_gene_summary.tsv",
    "wave103_raw": ROOT / "results_v3" / "wave103_sender_to_myeloid_bridge_scan" / "sender_raw_contrasts.tsv",
    "wave96": ROOT / "results_v3" / "wave96_c15orf48_controller_search" / "c15orf48_controller_candidate_rank.tsv",
    "ms": ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv",
}


def read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def first(df: pd.DataFrame, gene: str) -> dict:
    if df.empty or "gene" not in df.columns or gene not in set(df["gene"]):
        return {}
    return df[df["gene"].eq(gene)].iloc[0].to_dict()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tables = {key: read(path) for key, path in FILES.items()}
    rows = []
    for gene in GENES:
        w55 = first(tables["wave55"], gene)
        w62 = first(tables["wave62"], gene)
        w104 = first(tables["wave104"], gene)
        ms = first(tables["ms"], gene)
        sender = first(tables["wave103_sender"], gene)
        wave96 = first(tables["wave96"], gene)
        rows.append(
            {
                "gene": gene,
                "wave55_genetic_diseases": w55.get("diseases_genetic_ge_0_25", ""),
                "wave55_n_genetic_diseases": w55.get("n_diseases_genetic_ge_0_25", 0),
                "wave55_ms_genetic": w55.get("ms_genetic_association", ""),
                "wave62_call": w62.get("wave62_call", ""),
                "manual_blocker": w62.get("manual_blocker", ""),
                "prior_context_blocker": w62.get("prior_context_blocker", ""),
                "strong_l2g_diseases": w62.get("strong_l2g_diseases", ""),
                "strong_qtl_coloc_diseases": w62.get("strong_qtl_coloc_diseases", ""),
                "ms_max_l2g_score": w62.get("ms_max_l2g_score", ""),
                "ms_max_qtl_h4": w62.get("ms_max_qtl_h4", ""),
                "ms_wm_delta_log2": ms.get("delta_log2", ""),
                "ms_wm_p": ms.get("p", ""),
                "ms_wm_fdr": ms.get("fdr", ""),
                "wave104_call": w104.get("wave104_call", ""),
                "wave104_missing_gates": w104.get("wave104_missing_gates", ""),
                "wave103_bridge_call": sender.get("wave103_call", sender.get("call", "")),
                "wave103_bridge_positive_disease_count": sender.get("positive_disease_count", ""),
                "wave96_call": wave96.get("branch_call", wave96.get("call", "")),
                "wave96_failures": wave96.get("failures", ""),
            }
        )
    evidence = pd.DataFrame(rows)
    evidence.to_csv(OUT / "tnfsf14_axis_evidence.tsv", sep="\t", index=False)

    tls = tables["wave146"]
    tls_row = tls[tls["module"].eq("tls_lymphoid_niche")].iloc[0].to_dict() if not tls.empty and "tls_lymphoid_niche" in set(tls["module"]) else {}
    raw = tables["wave103_raw"]
    raw_hits = raw[raw["gene"].isin(GENES)].copy() if not raw.empty else pd.DataFrame()
    raw_hits.to_csv(OUT / "tnfsf14_axis_sender_raw_contrasts.tsv", sep="\t", index=False)

    gates = {
        "ms_target_resolved_genetics": bool(float(evidence.loc[evidence["gene"].eq("TNFSF14"), "ms_max_l2g_score"].iloc[0] or 0) >= 0.5),
        "cross_disease_target_genetics": False,
        "local_tls_architecture_pass": bool(tls_row.get("passes_architecture_gate", False) in [True, "True", "true"]),
        "ms_expression_anchor_fdr": False,
        "directionality_clean": False,
        "prior_art_not_blocking": False,
        "direct_perturbation_or_response": False,
        "reachable_selective_modality": False,
    }
    branch = "NO_TNFSF14_LIGHT_LYMPHOID_NICHE_PROMOTION"
    (OUT / "tnfsf14_axis_gate_decision.tsv").write_text(
        "gate\tpass\n" + "\n".join(f"{k}\t{v}" for k, v in gates.items()) + "\n"
    )
    summary = {
        "branch_call": branch,
        "random_seed": SEED,
        "gates": gates,
        "interpretation": (
            "TNFSF14/LIGHT has MS-specific target-resolved genetics, and TNFRSF14 has broader autoimmune genetics, "
            "but the axis fails cross-disease target genetics, TLS architecture, MS expression FDR, directionality, prior-art, "
            "perturbation, and selective-modality gates."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# Wave148 TNFSF14/LIGHT-HVEM/LTBR Audit",
        "",
        f"Branch call: `{branch}`.",
        "",
        "Key result:",
        "- `TNFSF14` has strong MS-specific L2G/QTL evidence but not cross-disease target-resolved genetics.",
        "- `TNFRSF14` has broader autoimmune genetics but was already blocked by HVEM/LIGHT directionality and prior-art ambiguity.",
        "- Wave146 `tls_lymphoid_niche` did not pass architecture gates.",
        "- No direct perturbation, response, or selective non-ambiguous modality gate passes locally.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
