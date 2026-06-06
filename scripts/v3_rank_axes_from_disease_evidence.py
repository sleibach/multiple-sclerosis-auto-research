#!/usr/bin/env python3
"""Rank V3 candidate mechanisms from disease-axis evidence.

This script intentionally separates evidence breadth from target nomination.
Manual disease classifications are traceable to subagent reports and local
analyses. The output is a convergence map, not a causal proof.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "data" / "derived_v3" / "disease_axis_evidence_v3.tsv"
OUT = ROOT / "phases/v3/results"

SCORES = {
    "strong": 2.0,
    "partial": 1.0,
    "mixed": 0.3,
    "weak": 0.0,
    "contradictory": -1.0,
}

AXIS_COLS = [
    "ifn_apc",
    "lysosomal_apc",
    "lipid_loader_repair",
    "hif_nampt_metabolic",
    "complement_phagocytosis",
]

GENE_AXES = {
    "STAT1": ["ifn_apc"],
    "IRF1": ["ifn_apc"],
    "CXCL10": ["ifn_apc"],
    "CD74": ["ifn_apc", "lysosomal_apc"],
    "HLA-DRA": ["ifn_apc", "lysosomal_apc"],
    "IFI30": ["ifn_apc", "lysosomal_apc"],
    "CTSS": ["lysosomal_apc"],
    "CTSB": ["lysosomal_apc"],
    "CTSD": ["lysosomal_apc", "lipid_loader_repair"],
    "LAMP1": ["lysosomal_apc"],
    "LAMP3": ["lysosomal_apc", "ifn_apc"],
    "NAMPT": ["hif_nampt_metabolic"],
    "HIF1A": ["hif_nampt_metabolic"],
    "GPNMB": ["lipid_loader_repair"],
    "SPP1": ["lipid_loader_repair"],
    "TREM2": ["lipid_loader_repair", "complement_phagocytosis"],
    "APOE": ["lipid_loader_repair"],
    "C1QA": ["complement_phagocytosis"],
    "C1QB": ["complement_phagocytosis"],
    "C1QBP": ["complement_phagocytosis", "hif_nampt_metabolic"],
    "SARM1": ["hif_nampt_metabolic"],
    "IL1B": ["ifn_apc", "hif_nampt_metabolic"],
    "TNF": ["ifn_apc", "hif_nampt_metabolic"],
    "OSM": ["ifn_apc"],
    "TREM1": ["ifn_apc"],
}


def level_weight(level: str) -> float:
    if level == "quantitative":
        return 1.0
    if level == "reviewed":
        return 0.7
    return 0.5


def main() -> None:
    OUT.mkdir(exist_ok=True)
    df = pd.read_csv(IN, sep="\t")
    for axis in AXIS_COLS:
        df[f"{axis}_score"] = df[axis].map(SCORES).fillna(0.0) * df["evidence_level"].map(level_weight)

    axis_rows = []
    for axis in AXIS_COLS:
        sub = df[["disease", "channel", f"{axis}_score", axis]].copy()
        axis_rows.append(
            {
                "axis": axis,
                "weighted_score": float(sub[f"{axis}_score"].sum()),
                "strong_disease_count": int((sub[axis] == "strong").sum()),
                "supportive_disease_count": int(sub[axis].isin(["strong", "partial", "mixed"]).sum()),
                "weak_or_contradictory_count": int(sub[axis].isin(["weak", "contradictory"]).sum()),
                "supporting_diseases": ";".join(sub.loc[sub[axis].isin(["strong", "partial", "mixed"]), "disease"]),
                "strong_diseases": ";".join(sub.loc[sub[axis] == "strong", "disease"]),
            }
        )
    axis_rank = pd.DataFrame(axis_rows).sort_values(
        ["weighted_score", "strong_disease_count", "supportive_disease_count"], ascending=False
    )
    axis_rank.to_csv(OUT / "disease_axis_convergence_rank.tsv", sep="\t", index=False)

    gene_rows = []
    for gene, axes in GENE_AXES.items():
        mentions = df["key_nodes"].fillna("").str.split(";").map(lambda xs: gene in xs)
        mentioned = df.loc[mentions]
        axis_score = float(df[[f"{axis}_score" for axis in axes]].mean(axis=1).sum())
        gene_rows.append(
            {
                "gene": gene,
                "axes": ",".join(axes),
                "axis_weighted_score": axis_score,
                "mentioned_disease_count": int(mentioned["disease"].nunique()),
                "mentioned_diseases": ";".join(mentioned["disease"].drop_duplicates()),
                "priority_score": axis_score + 0.8 * int(mentioned["disease"].nunique()),
            }
        )
    gene_rank = pd.DataFrame(gene_rows).sort_values(
        ["priority_score", "mentioned_disease_count", "axis_weighted_score"], ascending=False
    )
    gene_rank.to_csv(OUT / "disease_axis_candidate_gene_rank.tsv", sep="\t", index=False)

    summary = {
        "input": str(IN.relative_to(ROOT)),
        "n_disease_rows": int(df.shape[0]),
        "top_axes": axis_rank.head(5).to_dict(orient="records"),
        "top_candidate_genes": gene_rank.head(15).to_dict(orient="records"),
        "interpretation": (
            "Current breadth favors IFN/APC first, lysosomal antigen-processing second, "
            "HIF/NAMPT third, with lipid-loader/repair strong mainly in MS and lupus-like "
            "macrophage contexts rather than uniformly pan-autoimmune."
        ),
    }
    (OUT / "disease_axis_convergence_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
