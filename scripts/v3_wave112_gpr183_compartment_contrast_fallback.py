#!/usr/bin/env python3
"""Wave112 GPR183 compartment-contrast fallback.

Wave111 could not run matched-donor spatial proxies because donor-level gene
scores for GPR183/ligand genes were not precomputed. This fallback uses weaker
but real broad h5ad compartment-level contrasts: a disease passes only if
GPR183 is up in myeloid/APC, at least one oxysterol ligand-axis gene is up in a
non-myeloid compartment from the same dataset/disease, and the direction is not
contradicted by negative receptor/ligand compartments.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave112_gpr183_compartment_contrast_fallback"
BROAD = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
W93_IBD = ROOT / "phases/v3/results" / "wave93_gpr183_oxysterol_forcing_test" / "ibd_external_antitnf_gene_response_meta.tsv"
W93_RA = ROOT / "phases/v3/results" / "wave93_gpr183_oxysterol_forcing_test" / "ra_gse198520_baseline_gene_response_meta.tsv"
W93_PSO = ROOT / "phases/v3/results" / "wave93_gpr183_oxysterol_forcing_test" / "psoriasis_gse85034_ada_gene_response_meta.tsv"

RECEPTOR = "GPR183"
LIGANDS = ["CH25H", "CYP7B1", "HSD3B7", "CYP27A1"]


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def response_support() -> pd.DataFrame:
    rows = []
    for system, path in [("IBD", W93_IBD), ("RA", W93_RA), ("psoriasis", W93_PSO)]:
        df = read_tsv(path)
        if df.empty or "gene" not in df.columns:
            continue
        sub = df[df["gene"].isin([RECEPTOR, *LIGANDS])].copy()
        if sub.empty:
            continue
        for _, r in sub.iterrows():
            rows.append(
                {
                    "system": system,
                    "gene": r.get("gene"),
                    "nonresponse_high_contexts": r.get("nonresponse_high_contexts", 0),
                    "responder_high_contexts": r.get("responder_high_contexts", 0),
                    "min_p": r.get("min_p", math.nan),
                    "weighted_mean_hedges_g_responder_minus_non": r.get("weighted_mean_hedges_g_responder_minus_non", math.nan),
                }
            )
    return pd.DataFrame(rows)


def summarize_broad(broad: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if broad.empty:
        return pd.DataFrame(), pd.DataFrame()
    genes = [RECEPTOR, *LIGANDS]
    sub = broad[broad["gene"].isin(genes)].copy()
    if sub.empty:
        return pd.DataFrame(), pd.DataFrame()
    sub["is_myeloid"] = sub["role"].eq("myeloid_apc")
    sub["positive"] = (sub["delta_log2_cpm"] > 0) & (sub["p"] < 0.10)
    sub["negative"] = (sub["delta_log2_cpm"] < 0) & (sub["p"] < 0.10)
    rows = []
    for disease, d in sub.groupby("disease_name", observed=True):
        receptor_my = d[(d["gene"].eq(RECEPTOR)) & d["is_myeloid"]]
        ligand_nonmy = d[(d["gene"].isin(LIGANDS)) & ~d["is_myeloid"]]
        receptor_pos = receptor_my[receptor_my["positive"]]
        receptor_neg = receptor_my[receptor_my["negative"]]
        ligand_pos = ligand_nonmy[ligand_nonmy["positive"]]
        ligand_neg = ligand_nonmy[ligand_nonmy["negative"]]
        rows.append(
            {
                "disease_name": disease,
                "receptor_myeloid_tested_contexts": int(len(receptor_my)),
                "receptor_myeloid_positive_contexts": int(len(receptor_pos)),
                "receptor_myeloid_negative_contexts": int(len(receptor_neg)),
                "ligand_nonmyeloid_tested_contexts": int(len(ligand_nonmy)),
                "ligand_nonmyeloid_positive_contexts": int(len(ligand_pos)),
                "ligand_nonmyeloid_negative_contexts": int(len(ligand_neg)),
                "best_receptor_context": (
                    receptor_my.sort_values("p").head(1)[["analysis", "delta_log2_cpm", "p"]].to_dict(orient="records")[0]
                    if not receptor_my.empty
                    else {}
                ),
                "best_ligand_context": (
                    ligand_nonmy.sort_values("p").head(1)[["analysis", "gene", "delta_log2_cpm", "p"]].to_dict(orient="records")[0]
                    if not ligand_nonmy.empty
                    else {}
                ),
                "coherent_compartment_signal": bool(
                    len(receptor_pos) >= 1
                    and len(ligand_pos) >= 1
                    and len(receptor_neg) == 0
                    and len(ligand_neg) <= len(ligand_pos)
                ),
            }
        )
    return sub, pd.DataFrame(rows).sort_values(["coherent_compartment_signal", "disease_name"], ascending=[False, True])


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    broad = read_tsv(BROAD)
    rows, summary = summarize_broad(broad)
    resp = response_support()
    rows.to_csv(OUT / "gpr183_broad_target_gene_rows.tsv", sep="\t", index=False)
    summary.to_csv(OUT / "gpr183_compartment_contrast_summary.tsv", sep="\t", index=False)
    resp.to_csv(OUT / "gpr183_response_support_rows.tsv", sep="\t", index=False)
    coherent_diseases = int(summary["coherent_compartment_signal"].sum()) if not summary.empty else 0
    response_systems = int(resp[(resp["gene"].eq(RECEPTOR)) & (pd.to_numeric(resp["min_p"], errors="coerce") < 0.10)]["system"].nunique()) if not resp.empty else 0
    branch_call = (
        "PARK_GPR183_WEAK_COMPARTMENT_SIGNAL_NO_SPATIAL_PROOF"
        if coherent_diseases >= 2 and response_systems >= 1
        else "NO_REOPEN_GPR183_COMPARTMENT_FALLBACK"
    )
    payload = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "coherent_compartment_disease_count": coherent_diseases,
        "gpr183_response_support_system_count_p_lt_0_10": response_systems,
        "inputs": {"broad_h5ad": rel(BROAD), "wave93_ibd": rel(W93_IBD), "wave93_ra": rel(W93_RA), "wave93_psoriasis": rel(W93_PSO)},
        "scope": "weak_compartment_contrast_fallback_not_spatial_or_donor_matched",
    }
    write_json(OUT / "summary.json", payload)
    cols = [
        "disease_name",
        "receptor_myeloid_positive_contexts",
        "receptor_myeloid_negative_contexts",
        "ligand_nonmyeloid_positive_contexts",
        "ligand_nonmyeloid_negative_contexts",
        "coherent_compartment_signal",
        "best_receptor_context",
        "best_ligand_context",
    ]
    report = f"""# Wave112 GPR183 Compartment-Contrast Fallback

## Bottom Line

Branch call: `{branch_call}`.

Wave111 could not run matched-donor spatial proxies. This fallback is weaker:
it asks whether broad compartment contrasts show myeloid/APC `GPR183` up in
the same disease where non-myeloid oxysterol-axis genes are up, with no strong
directional contradiction.

## Disease Summary

{markdown_table(summary[cols], max_rows=30) if not summary.empty else "_No summary rows._"}

## Response Support Rows

{markdown_table(resp, max_rows=30) if not resp.empty else "_No response rows._"}

## Interpretation

This cannot promote GPR183. At best it can justify rebuilding donor-level
GPR183/ligand scores from h5ad. If coherent disease count is below two, the
route remains closed locally.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave112_gpr183_compartment_contrast_fallback.py")}`
- Broad h5ad rows: `{rel(BROAD)}`
- Output summary: `{rel(OUT / "gpr183_compartment_contrast_summary.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
