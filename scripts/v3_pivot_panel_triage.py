#!/usr/bin/env python3
"""Transparent triage of post-hour-4 lipid-lysosomal pivot candidates.

This script does not claim a target. It consolidates the actual local evidence
after the LGALS3, CD44, TYROBP, and cathepsin checks so the next foundation-model
work is spent only on candidates that pass explicit breadth and MS-anchor gates.

Inputs are all produced by earlier V3 scripts from real public/local data:

* broad h5ad donor-level gene discovery
* MS white-matter microglia/macrophage signature
* curated prior local evidence matrix
* Geneformer lightweight named-gene deletion screens

The scoring is deliberately simple and auditable. It is a routing heuristic, not
a statistical test or causal model.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "pivot_panel_triage"

PANEL = [
    "APOC1",
    "ACSL3",
    "LAMP3",
    "CTSL",
    "CTSB",
    "CD44",
    "CHI3L1",
    "LGALS8",
    "UGCG",
    "GBA2",
    "CD300LF",
    "CD300E",
    "TYROBP",
    "APOE",
    "GPNMB",
    "LPL",
    "PLIN2",
    "FABP5",
    "MSR1",
    "SCARB2",
    "LGALS3",
    "LGALS1",
]

# Manual labels summarize already-written, source-backed V3 audits and are used
# only to route deeper analyses. Final novelty/druggability claims still require
# fresh source-specific searches.
MANUAL_STATUS: dict[str, dict[str, str]] = {
    "CHI3L1": {
        "intervention_status": "demote",
        "reason": "crowded YKL-40 biomarker/therapeutic-target prior art and generic injury/fibrosis biology",
    },
    "CD44": {
        "intervention_status": "demote",
        "reason": "crowded matrix/integrin biology plus Geneformer deletion veto",
    },
    "CTSL": {
        "intervention_status": "hold",
        "reason": "model-supported cathepsin biology but protease inhibition has repair/debris-clearance liability and prior-art crowding",
    },
    "CTSB": {
        "intervention_status": "hold",
        "reason": "strongest Geneformer cathepsin comparator, but not MS-anchored in GSE111972 and has lysosomal repair liability",
    },
    "LGALS3": {
        "intervention_status": "demote",
        "reason": "failed residualized cross-disease local test despite MS foamy-state support",
    },
    "LGALS1": {
        "intervention_status": "demote",
        "reason": "broad immunoregulatory/repair axis with crowded prior art",
    },
    "FABP5": {
        "intervention_status": "demote",
        "reason": "tractable but directionally conflicted and prior-art risk in EAE/MS and psoriasis",
    },
    "MSR1": {
        "intervention_status": "hold",
        "reason": "MS-positive scavenger receptor marker but poor direct intervention point and weak non-MS local breadth",
    },
    "SCARB2": {
        "intervention_status": "hold",
        "reason": "MS-positive lysosomal receptor marker but unclear selective intervention point",
    },
    "LGALS8": {
        "intervention_status": "test_only_if_local_positive",
        "reason": "suggested by prior-art scout, but local expression breadth must pass first",
    },
    "UGCG": {
        "intervention_status": "test_only_if_local_positive",
        "reason": "druggable sphingolipid node but local disease direction must support it",
    },
    "GBA2": {
        "intervention_status": "test_only_if_local_positive",
        "reason": "glycosphingolipid node but MS and local direction are currently unfavorable",
    },
    "CD300LF": {
        "intervention_status": "test_only_if_local_positive",
        "reason": "CD300F synonym candidate from prior-art scout; local symbol is CD300LF and MS anchor is weak",
    },
}


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def bool_series(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series.fillna(False)
    return series.astype(str).str.lower().isin(["true", "1", "yes"])


def first_float(row: pd.Series, col: str) -> float:
    val = row.get(col, np.nan)
    try:
        return float(val)
    except (TypeError, ValueError):
        return float("nan")


def parse_disease_count(row: pd.Series, col: str) -> int:
    val = row.get(col, 0)
    if pd.isna(val) or val == "":
        return 0
    return int(float(val))


def top_compartments(contrasts: pd.DataFrame, gene: str, positive: bool) -> str:
    if contrasts.empty:
        return ""
    sub = contrasts.loc[contrasts["gene"] == gene].copy()
    if sub.empty:
        return ""
    flag = "positive_nominal" if positive else "negative_nominal"
    if flag not in sub.columns:
        return ""
    sub[flag] = bool_series(sub[flag])
    sub = sub.loc[sub[flag]]
    if sub.empty:
        return ""
    if positive:
        sub = sub.sort_values(["p", "delta_log2_cpm"], ascending=[True, False]).head(8)
    else:
        sub = sub.sort_values(["p", "delta_log2_cpm"], ascending=[True, True]).head(8)
    return ";".join(
        sub["analysis"].astype(str)
        + ":"
        + sub["delta_log2_cpm"].round(3).astype(str)
        + ",p="
        + sub["p"].map(lambda x: f"{float(x):.3g}")
    )


def existing_summary(existing: pd.DataFrame, gene: str) -> dict[str, Any]:
    if existing.empty or "gene" not in existing.columns:
        return {
            "existing_positive_disease_count": 0,
            "existing_negative_disease_count": 0,
            "existing_positive_diseases": "",
            "existing_negative_diseases": "",
        }
    sub = existing.loc[existing["gene"] == gene].copy()
    if sub.empty:
        return {
            "existing_positive_disease_count": 0,
            "existing_negative_disease_count": 0,
            "existing_positive_diseases": "",
            "existing_negative_diseases": "",
        }
    for col in ["positive_nominal", "negative_nominal"]:
        if col in sub.columns:
            sub[col] = bool_series(sub[col])
    pos = sorted(sub.loc[sub.get("positive_nominal", False), "disease"].astype(str).unique())
    neg = sorted(sub.loc[sub.get("negative_nominal", False), "disease"].astype(str).unique())
    return {
        "existing_positive_disease_count": len(pos),
        "existing_negative_disease_count": len(neg),
        "existing_positive_diseases": ";".join(pos),
        "existing_negative_diseases": ";".join(neg),
    }


def geneformer_summary(*tables: pd.DataFrame, gene: str) -> dict[str, Any]:
    rows: list[pd.Series] = []
    sources: list[str] = []
    for table in tables:
        if table.empty or "gene" not in table.columns:
            continue
        sub = table.loc[table["gene"] == gene]
        for _, row in sub.iterrows():
            rows.append(row)
            sources.append(str(table.attrs.get("source", "unknown")))
    if not rows:
        return {
            "geneformer_sources": "",
            "geneformer_contexts_with_token": 0,
            "geneformer_disease_cells_with_token": 0,
            "geneformer_support_contexts": 0,
            "geneformer_mean_cosine_z_vs_random": np.nan,
            "geneformer_mean_projection_shift": np.nan,
        }
    df = pd.DataFrame(rows)
    return {
        "geneformer_sources": ";".join(sorted(set(sources))),
        "geneformer_contexts_with_token": int(pd.to_numeric(df.get("contexts_with_token", 0), errors="coerce").fillna(0).sum()),
        "geneformer_disease_cells_with_token": int(pd.to_numeric(df.get("disease_cells_with_token", 0), errors="coerce").fillna(0).sum()),
        "geneformer_support_contexts": int(pd.to_numeric(df.get("support_contexts", 0), errors="coerce").fillna(0).sum()),
        "geneformer_mean_cosine_z_vs_random": float(pd.to_numeric(df.get("mean_cosine_z_vs_random", np.nan), errors="coerce").mean()),
        "geneformer_mean_projection_shift": float(pd.to_numeric(df.get("mean_projection_shift", np.nan), errors="coerce").mean()),
    }


def rank_decision(row: dict[str, Any]) -> tuple[str, str]:
    ms_positive = bool(row["ms_positive_nominal"])
    ms_trend = bool(row["ms_positive_trend"])
    positive_disease_count = int(row["direct_positive_disease_count"])
    negative_disease_count = int(row["direct_negative_disease_count"])
    support_contexts = int(row["geneformer_support_contexts"])
    manual = str(row["manual_intervention_status"])

    if manual == "demote":
        return "demote", "manual audit or model veto already blocks promotion"
    if manual == "hold":
        return "hold_comparator", "manual audit keeps this as comparator biology, not a target nomination"
    if not (ms_positive or ms_trend):
        return "demote", "no MS white-matter positive anchor"
    if positive_disease_count < 2 and int(row["existing_positive_disease_count"]) < 3:
        return "hold", "insufficient direct cross-disease breadth"
    if negative_disease_count >= 2:
        return "hold", "direction conflict in multiple diseases"
    if support_contexts >= 2:
        return "advance_with_caution", "has cross-disease breadth, MS anchor, and Geneformer support"
    if row["geneformer_contexts_with_token"] == 0:
        return "advance_to_geneformer", "passes local breadth/MS gates but lacks foundation-model perturbation test"
    return "hold", "passes some local gates but Geneformer support is absent or weak"


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    broad = read_tsv(ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv")
    contrasts = read_tsv(ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv")
    existing = read_tsv(ROOT / "phases/v3/results" / "existing_evidence_candidate_matrix.tsv")
    ms = read_tsv(ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv")
    gf_candidate = read_tsv(ROOT / "phases/v3/results" / "geneformer_candidate_delete" / "geneformer_candidate_delete_gene_summary.tsv")
    gf_candidate.attrs["source"] = "candidate_delete"
    gf_matrix = read_tsv(ROOT / "phases/v3/results" / "geneformer_phagolysosomal_matrix_delete" / "geneformer_phagolysosomal_matrix_gene_summary.tsv")
    gf_matrix.attrs["source"] = "phagolysosomal_matrix_delete"
    gf_pivot = read_tsv(ROOT / "phases/v3/results" / "geneformer_pivot_panel_delete" / "geneformer_pivot_panel_gene_summary.tsv")
    gf_pivot.attrs["source"] = "pivot_panel_delete"

    rows: list[dict[str, Any]] = []
    for gene in PANEL:
        brow = broad.loc[broad["gene"] == gene].head(1) if not broad.empty else pd.DataFrame()
        mrow = ms.loc[ms["gene"] == gene].head(1) if not ms.empty else pd.DataFrame()
        row: dict[str, Any] = {"gene": gene}
        if not brow.empty:
            b = brow.iloc[0]
            row.update(
                {
                    "direct_positive_disease_count": parse_disease_count(b, "positive_disease_count"),
                    "direct_negative_disease_count": parse_disease_count(b, "negative_disease_count"),
                    "direct_positive_compartment_count": parse_disease_count(b, "positive_compartment_count"),
                    "direct_negative_compartment_count": parse_disease_count(b, "negative_compartment_count"),
                    "direct_positive_diseases": str(b.get("positive_diseases", "")),
                    "direct_negative_diseases": str(b.get("negative_diseases", "")),
                    "broad_rank": int(b.get("rank", 0)) if "rank" in b.index and pd.notna(b.get("rank")) else np.nan,
                    "broad_discovery_priority_score": first_float(b, "discovery_priority_score"),
                    "ms_wm_delta_log2": first_float(b, "ms_wm_delta_log2"),
                    "ms_wm_hedges_g": first_float(b, "ms_wm_hedges_g"),
                    "ms_wm_p": first_float(b, "ms_wm_p"),
                    "ms_wm_fdr": first_float(b, "ms_wm_fdr"),
                    "broad_existing_priority_score": first_float(b, "existing_priority_score"),
                    "broad_opentargets_disease_count": parse_disease_count(b, "opentargets_disease_count"),
                    "broad_opentargets_max_genetic_association": first_float(b, "opentargets_max_genetic_association"),
                }
            )
        elif not mrow.empty:
            m = mrow.iloc[0]
            row.update(
                {
                    "direct_positive_disease_count": 0,
                    "direct_negative_disease_count": 0,
                    "direct_positive_compartment_count": 0,
                    "direct_negative_compartment_count": 0,
                    "direct_positive_diseases": "",
                    "direct_negative_diseases": "",
                    "broad_rank": np.nan,
                    "broad_discovery_priority_score": np.nan,
                    "ms_wm_delta_log2": first_float(m, "delta_log2"),
                    "ms_wm_hedges_g": first_float(m, "hedges_g"),
                    "ms_wm_p": first_float(m, "p"),
                    "ms_wm_fdr": first_float(m, "fdr"),
                    "broad_existing_priority_score": np.nan,
                    "broad_opentargets_disease_count": 0,
                    "broad_opentargets_max_genetic_association": np.nan,
                }
            )
        else:
            row.update(
                {
                    "direct_positive_disease_count": 0,
                    "direct_negative_disease_count": 0,
                    "direct_positive_compartment_count": 0,
                    "direct_negative_compartment_count": 0,
                    "direct_positive_diseases": "",
                    "direct_negative_diseases": "",
                    "broad_rank": np.nan,
                    "broad_discovery_priority_score": np.nan,
                    "ms_wm_delta_log2": np.nan,
                    "ms_wm_hedges_g": np.nan,
                    "ms_wm_p": np.nan,
                    "ms_wm_fdr": np.nan,
                    "broad_existing_priority_score": np.nan,
                    "broad_opentargets_disease_count": 0,
                    "broad_opentargets_max_genetic_association": np.nan,
                }
            )
        row["direct_top_positive_compartments"] = top_compartments(contrasts, gene, positive=True)
        row["direct_top_negative_compartments"] = top_compartments(contrasts, gene, positive=False)
        row.update(existing_summary(existing, gene))
        row.update(geneformer_summary(gf_candidate, gf_matrix, gf_pivot, gene=gene))
        row["ms_positive_nominal"] = bool(row["ms_wm_delta_log2"] > 0 and row["ms_wm_p"] < 0.05)
        row["ms_positive_trend"] = bool(row["ms_wm_delta_log2"] > 0 and row["ms_wm_p"] < 0.10)
        manual = MANUAL_STATUS.get(gene, {"intervention_status": "unknown", "reason": ""})
        row["manual_intervention_status"] = manual["intervention_status"]
        row["manual_intervention_reason"] = manual["reason"]
        row["triage_score"] = (
            2.0 * int(row["ms_positive_nominal"])
            + 1.0 * int(row["ms_positive_trend"])
            + 1.5 * min(int(row["direct_positive_disease_count"]), 5)
            - 1.25 * int(row["direct_negative_disease_count"])
            + 0.5 * min(int(row["existing_positive_disease_count"]), 5)
            - 0.5 * int(row["existing_negative_disease_count"])
            + 1.0 * min(int(row["geneformer_support_contexts"]), 4)
        )
        decision, rationale = rank_decision(row)
        row["routing_decision"] = decision
        row["routing_rationale"] = rationale
        rows.append(row)

    out = pd.DataFrame(rows).sort_values(
        ["routing_decision", "triage_score", "direct_positive_disease_count", "geneformer_support_contexts"],
        ascending=[True, False, False, False],
    )
    out.to_csv(OUT / "pivot_panel_summary.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "panel": PANEL,
        "scoring_guardrail": (
            "triage_score is a routing heuristic only. A final claim still requires genetic anchoring, "
            "independent MS replication, foundation-model prediction against real perturbation where possible, "
            "and verified literature/patent/trial novelty."
        ),
        "routing_counts": out["routing_decision"].value_counts().to_dict(),
        "top_rows": out.head(20).to_dict(orient="records"),
    }
    (OUT / "pivot_panel_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(out.to_string(index=False))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
