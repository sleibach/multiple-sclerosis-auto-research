#!/usr/bin/env python3
"""Wave113 PSAP recurrence and specificity audit."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave113_psap_recurrence_specificity_audit"
BROAD = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
MS = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_ms_rows.tsv"
W57 = ROOT / "phases/v3/results" / "wave57_intervention_first_geneformer_screen" / "wave57_geneformer_gene_summary.tsv"
W37 = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W81 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"

GENE = "PSAP"


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    broad = read_tsv(BROAD)
    psap = broad[broad["gene"].eq(GENE)].copy() if not broad.empty else pd.DataFrame()
    if not psap.empty:
        psap["positive_p10"] = (psap["delta_log2_cpm"] > 0) & (psap["p"] < 0.10)
        psap["negative_p10"] = (psap["delta_log2_cpm"] < 0) & (psap["p"] < 0.10)
    disease = []
    if not psap.empty:
        for disease_name, sub in psap.groupby("disease_name", observed=True):
            pos = sub[sub["positive_p10"]]
            neg = sub[sub["negative_p10"]]
            disease.append(
                {
                    "disease_name": disease_name,
                    "tested_contexts": int(len(sub)),
                    "positive_contexts_p10": int(len(pos)),
                    "negative_contexts_p10": int(len(neg)),
                    "myeloid_positive_contexts_p10": int(len(pos[pos["role"].eq("myeloid_apc")])),
                    "best_positive": (
                        pos.sort_values("p").head(1)[["analysis", "delta_log2_cpm", "p"]].to_dict(orient="records")[0]
                        if not pos.empty
                        else {}
                    ),
                    "best_negative": (
                        neg.sort_values("p").head(1)[["analysis", "delta_log2_cpm", "p"]].to_dict(orient="records")[0]
                        if not neg.empty
                        else {}
                    ),
                }
            )
    disease_df = pd.DataFrame(disease).sort_values(["myeloid_positive_contexts_p10", "positive_contexts_p10"], ascending=[False, False])
    ms = read_tsv(MS)
    ms_row = ms[ms["gene"].eq(GENE)].copy() if not ms.empty else pd.DataFrame()
    w57 = read_tsv(W57)
    w57_row = w57[w57["gene"].eq(GENE)].copy() if not w57.empty else pd.DataFrame()
    w37 = read_tsv(W37)
    w37_row = pd.DataFrame()
    if not w37.empty and "gene" in w37.columns:
        w37_row = w37[w37["gene"].eq(GENE)].copy()
    elif not w37.empty and "gene_symbol" in w37.columns:
        w37_row = w37[w37["gene_symbol"].eq(GENE)].copy()
    w81 = read_tsv(W81)
    w81_row = w81[w81["gene"].eq(GENE)].copy() if not w81.empty else pd.DataFrame()

    psap.to_csv(OUT / "psap_broad_contexts.tsv", sep="\t", index=False)
    disease_df.to_csv(OUT / "psap_disease_summary.tsv", sep="\t", index=False)
    rows = []
    rows.append({"evidence": "ms_anchor", "value": ms_row.to_dict(orient="records")[0] if not ms_row.empty else {}})
    rows.append({"evidence": "geneformer", "value": w57_row.to_dict(orient="records")[0] if not w57_row.empty else {}})
    rows.append({"evidence": "crispr_efferocytosis", "value": w37_row.to_dict(orient="records")[0] if not w37_row.empty else {}})
    rows.append({"evidence": "wave81_integrated", "value": w81_row.to_dict(orient="records")[0] if not w81_row.empty else {}})
    evidence_df = pd.DataFrame(rows)
    evidence_df.to_csv(OUT / "psap_evidence_rows.tsv", sep="\t", index=False)

    positive_diseases = int((disease_df["positive_contexts_p10"] > 0).sum()) if not disease_df.empty else 0
    myeloid_positive_diseases = int((disease_df["myeloid_positive_contexts_p10"] > 0).sum()) if not disease_df.empty else 0
    negative_diseases = int((disease_df["negative_contexts_p10"] > 0).sum()) if not disease_df.empty else 0
    ms_nominal = bool(not ms_row.empty and float(ms_row.iloc[0].get("p", 1.0)) < 0.05 and float(ms_row.iloc[0].get("delta_log2", 0.0)) > 0)
    geneformer_strong = bool(not w57_row.empty and float(w57_row.iloc[0].get("strong_support_contexts", 0) or 0) >= 1)
    crispr_support = bool(not w37_row.empty and str(w37_row.iloc[0].get("call", "")).startswith("KO_"))
    branch_call = (
        "REOPEN_PSAP_FOR_DEEP_VALIDATION"
        if positive_diseases >= 3 and myeloid_positive_diseases >= 2 and ms_nominal and geneformer_strong and crispr_support
        else "NO_REOPEN_PSAP_WEAK_SINGLE_CONTEXT_MARKER"
    )
    payload = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "positive_disease_count_p10": positive_diseases,
        "myeloid_positive_disease_count_p10": myeloid_positive_diseases,
        "negative_disease_count_p10": negative_diseases,
        "ms_nominal_positive": ms_nominal,
        "geneformer_strong_support": geneformer_strong,
        "crispr_support": crispr_support,
        "inputs": {"broad": rel(BROAD), "ms": rel(MS), "wave57": rel(W57), "wave37": rel(W37), "wave81": rel(W81)},
    }
    write_json(OUT / "summary.json", payload)
    report = f"""# Wave113 PSAP Recurrence / Specificity Audit

## Bottom Line

Branch call: `{branch_call}`.

PSAP/prosaposin is tested as a secreted lysosomal lipid-cofactor route, not as
a generic lysosomal marker. Reopening requires cross-disease recurrence,
myeloid recurrence, nominal MS support, strong foundation-model support, and
direct efferocytosis perturbation support.

## Disease Summary

{markdown_table(disease_df, max_rows=30) if not disease_df.empty else "_No PSAP broad h5ad rows._"}

## Evidence Rows

{markdown_table(evidence_df, max_rows=10)}

## Interpretation

PSAP remains parked unless it shows disease breadth and perturbation direction.
Single-context or nominal MS-only support is insufficient.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave113_psap_recurrence_specificity_audit.py")}`
- Output summary: `{rel(OUT / "psap_disease_summary.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
