#!/usr/bin/env python3
"""Wave45 audit of restoration/regulatory-controller routes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave45_regulatory_controller_audit"
SEED = 20260527

WAVE34 = ROOT / "results_v3" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv"
BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
RESIDUAL = ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
WAVE23_REST = ROOT / "results_v3" / "wave23_genetics_restoration_modality" / "ranked_go_park_no_go.tsv"
WAVE31 = ROOT / "results_v3" / "wave31_dynamic_transition_controller_audit" / "dynamic_transition_controller_audit.tsv"
WAVE25 = ROOT / "results_v3" / "wave25_causal_genetics_module_proxy" / "causal_proxy_candidate_matrix.tsv"


RULES = {
    "TNFAIP3": {
        "route": "A20 restoration / NF-kB-TNF-TLR brake",
        "modality_status": "requires restoration/editing; no selective current pharmacology",
        "blocker": "strong autoimmune genetics but wrong-direction druggability and no target-resolved coloc/MR in this run",
        "call": "NO_GO_RESTORATION_NO_MODALITY",
    },
    "SBNO2": {
        "route": "IL-10-induced anti-inflammatory transcriptional co-regulator",
        "modality_status": "intracellular regulatory protein; no current target-selective modality",
        "blocker": "good cross-disease state recurrence but no perturbation, MS anchor, or druggable handle",
        "call": "NO_GO_UNDRUGGABLE_STATE_CONTROLLER",
    },
    "SP140": {
        "route": "immune chromatin reader / nuclear-body regulator",
        "modality_status": "nuclear immune regulator; no mature selective degrader/inhibitor package",
        "blocker": "genetic and state signal, but no correct-direction modality or direct perturbation validation",
        "call": "NO_GO_UNDRUGGABLE_CHROMATIN_CONTROLLER",
    },
    "GPR65": {
        "route": "acidic pH-sensing GPCR/cAMP immunometabolic brake",
        "modality_status": "GPCR agonist/PAM possible in principle",
        "blocker": "local module support weak, no rescue in foundation/perturbation gates, and IBD prior art crowds the route",
        "call": "NO_GO_WEAK_LOCAL_AND_PRIOR_ART",
    },
    "IL10": {
        "route": "IL-10 restoration / anti-inflammatory cytokine",
        "modality_status": "cytokine/restoration modality exists in principle",
        "blocker": "direct prior art, systemic pleiotropy, and no new local biomarker delta",
        "call": "NO_GO_PRIOR_ART_RESTORATION",
    },
    "MED16": {
        "route": "Mediator-complex perturbation comparator",
        "modality_status": "not a direct drug target",
        "blocker": "strong selective macrophage perturbation clue but no direct druggable handle",
        "call": "NO_GO_STRONG_PERTURBATION_NO_HANDLE",
    },
    "CDK8_CDK19_MEDIATOR_KINASE": {
        "route": "Mediator kinase inhibition as MED16-adjacent surrogate",
        "modality_status": "chemical matter exists",
        "blocker": "does not phenocopy MED16 enough locally; prior broad IFN/IL-10/Treg biology and no APC autoimmune validation",
        "call": "NO_GO_SURROGATE_TRANSLATION_BLOCKED",
    },
    "GSK3B": {
        "route": "GSK3B partial cytokine/APC controller",
        "modality_status": "small-molecule target but pleiotropic",
        "blocker": "partial selectivity only, weak genetics/local breadth, chronic pleiotropic safety concerns",
        "call": "NO_GO_PLEIOTROPIC_PARTIAL_CONTROLLER",
    },
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def get_row(df: pd.DataFrame, gene: str, gene_cols: list[str]) -> dict[str, Any]:
    if df.empty:
        return {}
    for col in gene_cols:
        if col in df.columns:
            sub = df[df[col].astype(str).eq(gene)]
            if not sub.empty:
                return sub.iloc[0].to_dict()
    return {}


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        values = []
        for col in cols:
            value = "" if pd.isna(row[col]) else str(row[col])
            values.append(value.replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    wave34 = read_tsv(WAVE34)
    broad = read_tsv(BROAD)
    residual = read_tsv(RESIDUAL)
    rest = read_tsv(WAVE23_REST)
    wave31 = read_tsv(WAVE31)
    wave25 = read_tsv(WAVE25)

    rows = []
    for gene, rule in RULES.items():
        w34 = get_row(wave34, gene, ["gene"])
        br = get_row(broad, gene, ["gene"])
        res = get_row(residual, gene, ["gene"])
        r23 = get_row(rest, gene, ["gene", "candidate"])
        w31 = get_row(wave31, gene, ["candidate", "gene"])
        w25 = get_row(wave25, gene, ["gene"])
        rows.append(
            {
                "candidate": gene,
                "route": rule["route"],
                "call": rule["call"],
                "modality_status": rule["modality_status"],
                "manual_blocker": rule["blocker"],
                "wave34_call": w34.get("wave34_call"),
                "gwas_catalog_trait_count": w34.get("gwas_catalog_trait_count"),
                "local_positive_disease_count": w34.get("local_positive_disease_count", br.get("positive_disease_count")),
                "residual_retained_disease_count": w34.get("residual_retained_disease_count", res.get("retained_positive_disease_count")),
                "ms_anchor": w34.get("ms_anchor"),
                "ms_wm_delta_log2": w34.get("ms_wm_delta_log2", br.get("ms_wm_delta_log2")),
                "ms_wm_p": w34.get("ms_wm_p", br.get("ms_wm_p")),
                "broad_positive_diseases": br.get("positive_diseases"),
                "strict_core_residual_analyses": res.get("strict_core_covariate_surviving_analyses"),
                "wave23_restoration_call": r23.get("call", r23.get("restoration_call")),
                "wave31_call": w31.get("wave31_call"),
                "dynamic_controller_score": w31.get("dynamic_controller_score"),
                "proxy_call": w25.get("proxy_call"),
                "proxy_reason": w25.get("decision_reason"),
                "promotion_allowed": False,
            }
        )

    out = pd.DataFrame(rows)
    out.to_csv(OUT / "regulatory_controller_audit.tsv", sep="\t", index=False)
    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "n_candidates": int(len(out)),
        "promoted_count": int(out["promotion_allowed"].sum()),
        "call_counts": out["call"].value_counts().to_dict(),
        "interpretation": (
            "Regulatory/restoration routes do not yield a V3 finding. TNFAIP3, SBNO2, and SP140 are plausible biology "
            "but lack a current correct-direction modality; MED16 remains the best perturbation comparator but has no "
            "druggable handle; CDK8/CDK19 and GSK3B are only weak or unsafe surrogates; GPR65/IL10 are blocked by weak "
            "local evidence and prior art."
        ),
        "output_paths": {"audit": rel(OUT / "regulatory_controller_audit.tsv")},
        "inputs": [rel(p) for p in [WAVE34, BROAD, RESIDUAL, WAVE23_REST, WAVE31, WAVE25] if p.exists()],
    }
    write_json(OUT / "summary.json", summary)
    report = [
        "# Wave45 Regulatory Controller Audit",
        "",
        "## Result",
        "",
        summary["interpretation"],
        "",
        "## Calls",
        "",
        markdown_table(out),
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
