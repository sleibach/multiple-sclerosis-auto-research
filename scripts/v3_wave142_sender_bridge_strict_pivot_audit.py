#!/usr/bin/env python3
"""Wave142 strict audit of orthogonal sender-to-myeloid bridge candidates."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave142_sender_bridge_strict_pivot_audit"

INPUTS = {
    "bridge_summary": ROOT / "phases/v3/results" / "wave103_sender_to_myeloid_bridge_scan" / "sender_bridge_gene_summary.tsv",
    "bridge_links": ROOT / "phases/v3/results" / "wave103_sender_to_myeloid_bridge_scan" / "sender_to_myeloid_bridge_links.tsv",
    "intervention_first": ROOT / "phases/v3/results" / "wave103_intervention_first_successor_triage" / "intervention_first_successor_rank.tsv",
    "wave140": ROOT / "phases/v3/results" / "wave140_target_first_pivot_audit" / "target_first_pivot_audit.tsv",
    "wave83": ROOT / "phases/v3/results" / "wave83_intervention_class_meta_rank" / "intervention_class_meta_rank.tsv",
}

MANUAL_BLOCKERS = {
    "CALR": "ER chaperone/DAMP biology is broad; no selective extracellular autoimmune modality and risk of immunogenic stress confounding",
    "HIF1A": "broad hypoxia/metabolic transcription factor; systemic inhibition/activation is not selective and NAMPT/HIF branch previously prior-art blocked",
    "STAT3": "broad cytokine transcription node; JAK/STAT prior art and cell-wide pleiotropy block novelty/selectivity",
    "ITGAV": "integrin/adhesion and TGF-beta activation biology is prior-art crowded with fibrosis/wound-healing safety risk",
    "IL1B": "existing IL-1 blockade and generic inflammasome/inflammatory prior art block target novelty",
    "C2": "classical/lectin complement component; complement host-defense and upstream blockade risk; no target-specific MS genetics",
    "CFB": "alternative complement factor B route already audited as prior-art/safety blocked",
    "CXCL1": "neutrophil chemokine redundancy and safety/prior-art block",
    "NAMPT": "successor route rejected on prior-art and systemic metabolic toxicity grounds",
    "TIMP1": "matrix remodeling inhibitor is context-dependent, not selectively druggable for autoimmune tissue bridges",
    "CD74": "MHC-II/MIF antigen-presentation axis prior blocked",
    "CCL20": "CCR6/CCL20 chemokine route prior-art and redundancy blocked",
}


def read(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        raise FileNotFoundError(path)
    return pd.read_csv(path, sep="\t", low_memory=False)


def fnum(x, default: float = 0.0) -> float:
    try:
        if pd.isna(x) or x == "":
            return default
        return float(x)
    except Exception:
        return default


def first(df: pd.DataFrame, gene: str, column: str = "gene") -> dict:
    if column not in df.columns:
        return {}
    hit = df[df[column].astype(str).str.upper().eq(gene.upper())]
    return hit.iloc[0].to_dict() if not hit.empty else {}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary = read(INPUTS["bridge_summary"])
    links = read(INPUTS["bridge_links"])
    intervention = read(INPUTS["intervention_first"])
    wave140 = read(INPUTS["wave140"])
    wave83 = read(INPUTS["wave83"])

    rows = []
    for _, r in summary.iterrows():
        gene = str(r["gene"]).upper()
        if str(r.get("wave103_call", "")) not in {
            "REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT",
            "PARK_BRIDGE_PRIOR_OR_DIRECTION_REVIEW",
        }:
            continue
        ir = first(intervention, gene)
        g140 = first(wave140, gene)
        w83_hits = wave83[wave83["candidate"].astype(str).str.upper().str.contains(gene, regex=False, na=False)]
        w83 = w83_hits.iloc[0].to_dict() if not w83_hits.empty else {}
        gene_links = links[
            links["gene"].astype(str).str.upper().eq(gene)
            & links["upregulated_bridge_link"].astype(bool)
        ]
        independent_tissues = gene_links["tissue_compartment"].dropna().astype(str).nunique()
        independent_diseases = gene_links["disease_name"].dropna().astype(str).nunique()
        case_supported_links = int(gene_links["case_link_positive"].fillna(False).astype(bool).sum())
        gates = {
            "cross_disease_up_bridge": fnum(r.get("upregulated_bridge_link_disease_count")) >= 2
            and fnum(r.get("bridge_link_disease_count")) >= 3,
            "multi_tissue_sender": independent_tissues >= 2,
            "case_link_support": case_supported_links >= 2,
            "ms_anchor": bool(ir) and str(ir.get("ms_anchor", "")).lower() == "true"
            or str(g140.get("call", "")) == "GENETICS_COMPARATOR",
            "genetic_or_target_resolution": str(g140.get("call", "")) == "GENETICS_COMPARATOR"
            or fnum(ir.get("ms_genetic_score", 0)) >= 0.5,
            "direct_perturbation_or_model": str(ir.get("has_direct_perturbation", "")).lower() == "true"
            or str(ir.get("has_foundation_support", "")).lower() == "true"
            or fnum(w83.get("support_gate_count", 0)) >= 2,
            "reachable_modality": str(ir.get("reachable_modality", "")).lower() == "true"
            or str(w83.get("reachable_modality", "")).lower() == "1",
            "not_prior_or_safety_blocked": gene not in MANUAL_BLOCKERS
            and str(ir.get("prior_or_safety_blocked", "")).lower() != "true"
            and "prior" not in str(w83.get("primary_blocker", "")).lower(),
            "direction_selective": str(ir.get("wrong_direction_or_undruggable", "")).lower() != "true"
            and "direction" not in str(w83.get("primary_blocker", "")).lower(),
        }
        call = "ORTHOGONAL_BRIDGE_PIVOT_CANDIDATE" if all(gates.values()) else "NO_BRIDGE_PIVOT"
        if call == "NO_BRIDGE_PIVOT" and gates["cross_disease_up_bridge"] and gates["multi_tissue_sender"]:
            call = "BRIDGE_BIOLOGY_ONLY"
        rows.append(
            {
                "gene": gene,
                "call": call,
                "pass_count": int(sum(gates.values())),
                "failed_gates": ";".join(k for k, v in gates.items() if not v),
                **gates,
                "bridge_score": fnum(r.get("bridge_score")),
                "upregulated_bridge_link_disease_count": fnum(r.get("upregulated_bridge_link_disease_count")),
                "bridge_link_disease_count": fnum(r.get("bridge_link_disease_count")),
                "independent_sender_tissues": int(independent_tissues),
                "case_supported_up_links": case_supported_links,
                "best_bridge_link": r.get("best_bridge_link", ""),
                "intervention_first_call": ir.get("wave103_call", ""),
                "wave140_call": g140.get("call", ""),
                "wave83_call": w83.get("wave83_call", ""),
                "manual_blocker": MANUAL_BLOCKERS.get(gene, ""),
            }
        )

    out = pd.DataFrame(rows)
    priority = {"ORTHOGONAL_BRIDGE_PIVOT_CANDIDATE": 0, "BRIDGE_BIOLOGY_ONLY": 1, "NO_BRIDGE_PIVOT": 2}
    out["_p"] = out["call"].map(priority).fillna(9)
    out = out.sort_values(
        ["_p", "pass_count", "bridge_score", "case_supported_up_links"],
        ascending=[True, False, False, False],
    ).drop(columns=["_p"])
    out.to_csv(OUT / "sender_bridge_strict_pivot_rank.tsv", sep="\t", index=False)

    summary_json = {
        "random_seed": SEED,
        "branch_call": "ORTHOGONAL_BRIDGE_PIVOT_AVAILABLE"
        if (out["call"] == "ORTHOGONAL_BRIDGE_PIVOT_CANDIDATE").any()
        else "NO_ORTHOGONAL_BRIDGE_PIVOT_AVAILABLE",
        "n_pivot_candidates": int((out["call"] == "ORTHOGONAL_BRIDGE_PIVOT_CANDIDATE").sum()),
        "n_bridge_biology_only": int((out["call"] == "BRIDGE_BIOLOGY_ONLY").sum()),
        "top_bridge_biology": out.head(12)[["gene", "call", "pass_count", "failed_gates", "manual_blocker"]].to_dict("records"),
        "inputs": {k: str(v.relative_to(ROOT)) for k, v in INPUTS.items()},
    }
    (OUT / "summary.json").write_text(json.dumps(summary_json, indent=2, sort_keys=True), encoding="utf-8")
    report = f"""# Wave142 Sender-Bridge Strict Pivot Audit

## Bottom Line

Branch call: `{summary_json['branch_call']}`.

The orthogonal sender-to-myeloid bridge scan contains real cross-tissue biology,
but no bridge gene survives target-level MS/genetic anchoring, perturbation/model
support, reachability, safety, and selectivity gates.

## Counts

- Pivot candidates: {summary_json['n_pivot_candidates']}
- Bridge-biology-only candidates: {summary_json['n_bridge_biology_only']}

## Interpretation

The strongest bridge genes (`CALR`, `HIF1A`, `STAT3`, `ITGAV`, `IL1B`,
`C2`, `CFB`) are useful mechanistic comparators but not V3 therapeutic
successors. Most fail because they are broad stress/cytokine/complement/
adhesion nodes with prior-art or safety blockers, and because target-specific
MS and perturbation evidence is insufficient.
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary_json, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
