#!/usr/bin/env python3
"""Rank successor targets after ACSL1 demotion.

The ranking combines prior MS convergence with the V2 cross-autoimmune screen.
It is a prioritization aid, not a claim of causality.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v2"


def disease_label(comparison: str) -> str:
    if comparison.startswith("RA_"):
        return "RA"
    if comparison.startswith("psoriasis") and "paired" in comparison:
        return "psoriasis"
    if comparison.startswith("UC_active_colon_vs_UC_inactive") or comparison.startswith("CD_active_ileum_vs_CD_inactive"):
        return "IBD_active_vs_inactive"
    if comparison.startswith("LN_"):
        return "lupus_nephritis"
    return "secondary"


def main() -> None:
    ms = pd.read_csv(ROOT / "results" / "mims2_proteome_convergent_targets.tsv", sep="\t")
    cross = pd.read_csv(OUT / "cross_autoimmune_target_gene_contrasts.tsv", sep="\t")
    cross["disease"] = cross["comparison"].map(disease_label)
    cross = cross[cross["disease"] != "secondary"].copy()

    disease_rows = []
    for (gene, disease), sub in cross.groupby(["feature", "disease"]):
        informative = sub[sub["p"].notna()]
        if informative.empty:
            continue
        # Average repeated compartment/UC-CD contrasts within a disease family.
        disease_rows.append(
            {
                "gene": gene,
                "disease": disease,
                "mean_delta": informative["delta"].mean(),
                "mean_hedges_g": informative["hedges_g"].mean(),
                "min_p": informative["p"].min(),
                "positive_all": bool((informative["delta"] > 0).all()),
                "positive_any_nominal": bool(((informative["delta"] > 0) & (informative["p"] < 0.05)).any()),
                "negative_any_nominal": bool(((informative["delta"] < 0) & (informative["p"] < 0.05)).any()),
                "n_contrasts": len(informative),
            }
        )
    disease = pd.DataFrame(disease_rows)
    disease.to_csv(OUT / "successor_target_cross_disease_by_gene.tsv", sep="\t", index=False)

    rows = []
    for gene, sub in disease.groupby("gene"):
        ms_row = ms[ms["gene"] == gene]
        if ms_row.empty:
            ms_pass = False
            ms_score = 0.0
            ms_summary = {}
        else:
            m = ms_row.iloc[0]
            ms_pass = bool(m["passes_convergence_gate"])
            ms_score = (
                (2.0 if ms_pass else 0.0)
                + max(0.0, float(m["dz"]))
                + max(0.0, -np.log10(float(m["fdr_bh"]) + 1e-300)) / 5.0
            )
            ms_summary = {
                "ms_mean_delta": float(m["mean_delta"]),
                "ms_dz": float(m["dz"]),
                "ms_positive_fraction": float(m["positive_fraction"]),
                "ms_proteomics_fdr": float(m["fdr_bh"]),
                "ms_passes_convergence_gate": ms_pass,
            }
        pos_diseases = int(sub["positive_any_nominal"].sum())
        neg_diseases = int(sub["negative_any_nominal"].sum())
        score = ms_score + pos_diseases * 1.5 - neg_diseases * 1.5 + sub["mean_hedges_g"].clip(lower=-2, upper=2).mean()
        rows.append(
            {
                "gene": gene,
                "priority_score": score,
                "ms_score_component": ms_score,
                "positive_non_ms_disease_count": pos_diseases,
                "negative_non_ms_disease_count": neg_diseases,
                "mean_non_ms_hedges_g": sub["mean_hedges_g"].mean(),
                "diseases_positive": ",".join(sub.loc[sub["positive_any_nominal"], "disease"].tolist()),
                "diseases_negative": ",".join(sub.loc[sub["negative_any_nominal"], "disease"].tolist()),
                **ms_summary,
            }
        )
    ranked = pd.DataFrame(rows).sort_values("priority_score", ascending=False)
    ranked.to_csv(OUT / "successor_target_priority_rank.tsv", sep="\t", index=False)
    summary = {
        "top_gene": ranked.iloc[0]["gene"],
        "top_priority_score": float(ranked.iloc[0]["priority_score"]),
        "interpretation": "High score requires MS convergence plus non-MS disease recurrence; known biology/novelty still requires manual vetting.",
    }
    (OUT / "successor_target_priority_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(ranked.head(12).to_string(index=False))


if __name__ == "__main__":
    main()
