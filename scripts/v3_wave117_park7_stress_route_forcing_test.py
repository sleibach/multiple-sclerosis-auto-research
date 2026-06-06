#!/usr/bin/env python3
"""Wave117 PARK7/DJ-1 stress-route forcing test."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave117_park7_stress_route_forcing_test"

W81_RANK = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W81_MS = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_ms_rows.tsv"
W81_BROAD = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_broad_summary.tsv"
W81_FOUNDATION = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_wave57_rows.tsv"
W81_IBD = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_ibd_response_summary.tsv"
W81_W62 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_wave62_rows.tsv"
W81_W37 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_wave37_rows.tsv"
W68 = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
BROAD = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
RESID = ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_residual_tests.tsv"
W55 = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_candidate_audit.tsv"

GENERIC_COVARS = {
    "er_upr_stress",
    "hif_nampt_metabolic",
    "inflammatory_nfkb",
    "ifn_apc",
    "lysosomal_apc",
    "generic_inflammation_mean",
    "injury_stress_mean",
}


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def gene_rows(df: pd.DataFrame, gene: str = "PARK7") -> pd.DataFrame:
    for col in ["gene", "candidate", "gene_symbol"]:
        if col in df.columns:
            return df[df[col].astype(str).eq(gene)].copy()
    return pd.DataFrame()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rank = gene_rows(read_tsv(W81_RANK))
    ms = gene_rows(read_tsv(W81_MS))
    broad = gene_rows(read_tsv(W81_BROAD))
    foundation = gene_rows(read_tsv(W81_FOUNDATION))
    ibd = gene_rows(read_tsv(W81_IBD))
    w62 = gene_rows(read_tsv(W81_W62))
    w37 = gene_rows(read_tsv(W81_W37))
    w68 = gene_rows(read_tsv(W68))
    broad_context = gene_rows(read_tsv(BROAD))
    resid = gene_rows(read_tsv(RESID))
    w55 = gene_rows(read_tsv(W55))

    broad_context.to_csv(OUT / "park7_broad_contexts.tsv", sep="\t", index=False)
    resid.to_csv(OUT / "park7_residual_contexts.tsv", sep="\t", index=False)

    if not broad_context.empty:
        broad_summary = (
            broad_context.assign(
                positive_nominal=lambda d: (pd.to_numeric(d["delta_log2_cpm"], errors="coerce") > 0)
                & (pd.to_numeric(d["p"], errors="coerce") < 0.05),
                myeloid_positive=lambda d: d["role"].eq("myeloid_apc")
                & (pd.to_numeric(d["delta_log2_cpm"], errors="coerce") > 0)
                & (pd.to_numeric(d["p"], errors="coerce") < 0.05),
            )
            .groupby("disease_name")
            .agg(
                tested_contexts=("analysis", "nunique"),
                positive_contexts=("positive_nominal", "sum"),
                myeloid_positive_contexts=("myeloid_positive", "sum"),
                best_p=("p", "min"),
                max_delta=("delta_log2_cpm", "max"),
            )
            .reset_index()
        )
    else:
        broad_summary = pd.DataFrame()
    broad_summary.to_csv(OUT / "park7_broad_disease_summary.tsv", sep="\t", index=False)

    if not resid.empty and {"covariates", "residual_positive", "disease_name"}.issubset(resid.columns):
        residual_generic = resid[resid["covariates"].astype(str).isin(GENERIC_COVARS)].copy()
        residual_summary = (
            residual_generic.groupby("disease_name")
            .agg(
                residual_tests=("analysis", "count"),
                residual_positive_tests=("residual_positive", "sum"),
                best_residual_p=("residual_p", "min"),
                max_residual_delta=("residual_delta_case_minus_control", "max"),
            )
            .reset_index()
            if not residual_generic.empty
            else pd.DataFrame()
        )
    else:
        residual_generic = pd.DataFrame()
        residual_summary = pd.DataFrame()
    residual_generic.to_csv(OUT / "park7_generic_covariate_residual_rows.tsv", sep="\t", index=False)
    residual_summary.to_csv(OUT / "park7_generic_covariate_residual_summary.tsv", sep="\t", index=False)

    ms_anchor = (not ms.empty) and (float(ms.iloc[0].get("p", 1)) < 0.05) and (float(ms.iloc[0].get("delta_log2", 0)) > 0)
    broad_myeloid_diseases = (
        int((broad_summary["myeloid_positive_contexts"] > 0).sum()) if not broad_summary.empty else 0
    )
    residual_diseases = (
        int((residual_summary["residual_positive_tests"] > 0).sum()) if not residual_summary.empty else 0
    )
    foundation_strong = (not foundation.empty) and (int(foundation.iloc[0].get("strong_support_contexts", 0) or 0) > 0)
    ibd_response = (not ibd.empty) and (float(ibd.iloc[0].get("remission_delta_p", 1) or 1) < 0.05) and (
        float(ibd.iloc[0].get("remission_delta_fdr", 1) or 1) < 0.10
    )
    w68_response = (not w68.empty) and (pd.to_numeric(w68.get("paired_post_minus_pre_fdr"), errors="coerce").min() < 0.10)
    target_resolution = (not w62.empty) and not str(w62.iloc[0].get("wave62_call", "")).startswith("NO_GO")
    crispr_support = (not w37.empty) and str(w37.iloc[0].get("screen_call", "")).startswith("KO_")
    broad_genetics = (not w55.empty) and (float(w55.iloc[0].get("n_diseases_genetic_ge_0_25", 0) or 0) >= 4)
    generic_stress_like = (residual_diseases < broad_myeloid_diseases) or (
        not residual_summary.empty and residual_summary["residual_positive_tests"].sum() == 0
    )

    branch_call = (
        "REOPEN_PARK7_STRESS_ROUTE"
        if ms_anchor
        and broad_myeloid_diseases >= 2
        and residual_diseases >= 2
        and (ibd_response or w68_response)
        and (foundation_strong or crispr_support)
        and target_resolution
        and not generic_stress_like
        else "NO_REOPEN_PARK7_GENERIC_STRESS_ROUTE"
    )

    evidence = pd.DataFrame(
        [
            {"evidence": "wave81_rank", "value": rank.to_dict(orient="records")},
            {"evidence": "ms", "value": ms.to_dict(orient="records")},
            {"evidence": "broad_summary", "value": broad.to_dict(orient="records")},
            {"evidence": "foundation", "value": foundation.to_dict(orient="records")},
            {"evidence": "ibd_response", "value": ibd.to_dict(orient="records")},
            {"evidence": "wave68_response", "value": w68.to_dict(orient="records")},
            {"evidence": "target_resolution", "value": w62.to_dict(orient="records")},
            {"evidence": "crispr", "value": w37.to_dict(orient="records")},
            {"evidence": "broad_genetics", "value": w55.to_dict(orient="records")},
        ]
    )
    evidence.to_csv(OUT / "park7_gate_evidence.tsv", sep="\t", index=False)

    payload = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "ms_anchor": bool(ms_anchor),
        "broad_myeloid_positive_diseases": broad_myeloid_diseases,
        "generic_covariate_residual_diseases": residual_diseases,
        "foundation_strong": bool(foundation_strong),
        "ibd_response": bool(ibd_response),
        "wave68_response": bool(w68_response),
        "target_resolution": bool(target_resolution),
        "crispr_support": bool(crispr_support),
        "broad_genetics": bool(broad_genetics),
        "generic_stress_like": bool(generic_stress_like),
        "inputs": {
            "wave81_rank": rel(W81_RANK),
            "wave81_ms": rel(W81_MS),
            "wave81_broad": rel(W81_BROAD),
            "wave81_foundation": rel(W81_FOUNDATION),
            "wave81_ibd": rel(W81_IBD),
            "wave81_w62": rel(W81_W62),
            "wave81_w37": rel(W81_W37),
            "wave68": rel(W68),
            "broad_context": rel(BROAD),
            "residual": rel(RESID),
            "wave55": rel(W55),
        },
    }
    write_json(OUT / "summary.json", payload)

    report = f"""# Wave117 PARK7/DJ-1 Stress-Route Forcing Test

## Bottom Line

Branch call: `{branch_call}`.

This test asks whether `PARK7` is a disease-resolved myeloid lipid-stress
intervention route, or merely a generic oxidative/adaptive-stress marker.

## Gate Summary

| gate | value |
| --- | --- |
| MS anchor | {bool(ms_anchor)} |
| Broad myeloid-positive diseases | {broad_myeloid_diseases} |
| Generic-covariate residual diseases | {residual_diseases} |
| Foundation strong support | {bool(foundation_strong)} |
| IBD response support | {bool(ibd_response)} |
| Wave68 response support | {bool(w68_response)} |
| Target-resolution support | {bool(target_resolution)} |
| CRISPR/efferocytosis support | {bool(crispr_support)} |
| Broad genetics support | {bool(broad_genetics)} |
| Generic-stress-like | {bool(generic_stress_like)} |

## Broad Disease Summary

{markdown_table(broad_summary, max_rows=20)}

## Generic-Covariate Residual Summary

{markdown_table(residual_summary, max_rows=20)}

## Evidence Rows

{markdown_table(evidence, max_rows=20)}

## Decision Rule

Reopen only if `PARK7` has nominal positive MS expression, at least two
myeloid-positive diseases, at least two generic-covariate residual diseases,
response or perturbation support, target-resolution genetics, and no generic
stress collapse. Otherwise close as generic stress biology.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave117_park7_stress_route_forcing_test.py")}`
- Output: `{rel(OUT / "park7_gate_evidence.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
