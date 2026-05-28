#!/usr/bin/env python3
"""Wave102 residual compartment test for accessible-survivor candidates.

Wave101 left SEL1L3 and FXYD5 as undercharacterized accessible survivors, but
only as forcing candidates. This script asks a narrower question:

Do SEL1L3, FXYD5, or comparator accessible survivors remain disease-associated
in donor-level h5ad compartments after adjusting for lipid-lysosomal,
lysosomal/APC, IFN/APC, NF-kB, and HIF/NAMPT inflammatory modules?

This is still not a target claim. It only decides whether a candidate deserves
target-specific perturbation, genetics, and modality work.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse

import v3_snx10_c15orf48_residual_gate as residual_gate
from v3_analyze_osmr_complement_axes import CONFIGS, ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "results_v3" / "wave102_accessible_survivor_residual_compartment_test"
W101 = ROOT / "results_v3" / "wave101_accessible_survivor_forcing_triage" / "accessible_survivor_forcing_rank.tsv"

CANDIDATES = [
    "SEL1L3",
    "FXYD5",
    "APOC1",
    "CD82",
    "LAPTM5",
    "NRCAM",
    "CD200",
    "CHI3L1",
    "MFGE8",
    "BTN2A2",
    "ADM",
    "GPNMB",
]

FOCUS = {"SEL1L3", "FXYD5", "APOC1"}
CORE_SINGLE = set(residual_gate.CORE_COVARIATES)


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value)


def summarize(raw_tests: pd.DataFrame, residuals: pd.DataFrame, presence: pd.DataFrame) -> pd.DataFrame:
    raw_gene = raw_tests.loc[raw_tests["metric"].eq("mean_z_vs_controls")].copy()
    rows: list[dict[str, Any]] = []
    for gene in CANDIDATES:
        raw_sub = raw_gene.loc[raw_gene["gene"].eq(gene)].copy()
        resid_sub = residuals.loc[residuals["gene"].eq(gene)].copy()
        raw_pos = raw_sub.loc[raw_sub["positive_nominal"]].copy()
        raw_neg = raw_sub.loc[raw_sub["negative_nominal"]].copy()
        retained = resid_sub.loc[resid_sub["retains_nominal_positive"]].copy()
        core_uni = retained.loc[
            retained["residual_model"].eq("univariate")
            & retained["covariate_set"].isin(CORE_SINGLE)
        ].copy()
        core_all = retained.loc[
            retained["residual_model"].eq("multivariable")
            & retained["covariate_set"].eq("core_all")
        ].copy()
        lipid_lysosomal = retained.loc[
            retained["covariate_set"].isin(["lipid_loader_repair", "lysosomal_apc", "core_lysosomal_lipid"])
        ].copy()

        strict_core_rows = []
        for analysis, sub in resid_sub.loc[
            resid_sub["residual_model"].eq("univariate") & resid_sub["covariate_set"].isin(CORE_SINGLE)
        ].groupby("analysis", observed=True):
            if len(sub) == len(CORE_SINGLE) and bool(sub["retains_nominal_positive"].all()):
                first = sub.iloc[0]
                strict_core_rows.append(
                    {
                        "analysis": analysis,
                        "disease_name": first["disease_name"],
                        "compartment": first["compartment"],
                    }
                )
        strict_core = pd.DataFrame(strict_core_rows)
        non_ibd_retained = retained.loc[
            ~retained["disease_name"].astype(str).isin(["Crohn disease", "ulcerative colitis"])
        ]
        rows.append(
            {
                "gene": gene,
                "focus_candidate": gene in FOCUS,
                "present_analysis_count": int(presence.loc[presence["gene"].eq(gene), "analysis"].nunique()),
                "raw_positive_analysis_count": int(raw_pos["analysis"].nunique()),
                "raw_positive_disease_count": int(raw_pos["disease_name"].nunique()),
                "raw_negative_analysis_count": int(raw_neg["analysis"].nunique()),
                "retained_positive_test_count": int(len(retained)),
                "retained_positive_analysis_count": int(retained["analysis"].nunique()),
                "retained_positive_disease_count": int(retained["disease_name"].nunique()),
                "non_ibd_retained_positive_analysis_count": int(non_ibd_retained["analysis"].nunique()),
                "non_ibd_retained_positive_disease_count": int(non_ibd_retained["disease_name"].nunique()),
                "strict_core_covariate_surviving_analysis_count": int(len(strict_core)),
                "strict_core_covariate_surviving_disease_count": int(strict_core["disease_name"].nunique())
                if not strict_core.empty
                else 0,
                "core_all_multivariable_surviving_analysis_count": int(core_all["analysis"].nunique()),
                "core_all_multivariable_surviving_disease_count": int(core_all["disease_name"].nunique()),
                "lipid_lysosomal_surviving_analysis_count": int(lipid_lysosomal["analysis"].nunique()),
                "lipid_lysosomal_surviving_disease_count": int(lipid_lysosomal["disease_name"].nunique()),
                "raw_positive_analyses": ";".join(
                    raw_pos.sort_values(["p", "delta_case_minus_control"], ascending=[True, False])
                    .head(8)
                    .apply(lambda r: f"{r['analysis']}:{r['delta_case_minus_control']:.3g},p={r['p']:.2g}", axis=1)
                    .tolist()
                ),
                "top_retained_tests": ";".join(
                    retained.sort_values(["residual_p", "residual_delta_case_minus_control"], ascending=[True, False])
                    .head(10)
                    .apply(
                        lambda r: (
                            f"{r['analysis']}|{r['covariate_set']}:"
                            f"{r['residual_delta_case_minus_control']:.3g},p={r['residual_p']:.2g}"
                        ),
                        axis=1,
                    )
                    .tolist()
                ),
            }
        )
    out = pd.DataFrame(rows)
    out["wave102_residual_priority_score"] = (
        5 * out["strict_core_covariate_surviving_disease_count"].fillna(0)
        + 3 * out["core_all_multivariable_surviving_disease_count"].fillna(0)
        + 2 * out["non_ibd_retained_positive_disease_count"].fillna(0)
        + out["retained_positive_disease_count"].fillna(0)
        + out["raw_positive_disease_count"].fillna(0)
        + out["focus_candidate"].astype(int)
        - 3 * out["raw_negative_analysis_count"].fillna(0)
    )
    calls = []
    for _, row in out.iterrows():
        if row["raw_positive_disease_count"] == 0:
            calls.append("NO_GO_NO_DIRECT_H5AD_REPLICATION")
        elif row["retained_positive_disease_count"] == 0:
            calls.append("NO_GO_MODULE_CONFOUNDED_OR_UNSTABLE")
        elif row["strict_core_covariate_surviving_disease_count"] >= 2 and row[
            "core_all_multivariable_surviving_disease_count"
        ] >= 1:
            calls.append("REOPEN_FOR_WAVE103_TARGET_SPECIFIC_FORCING")
        elif row["strict_core_covariate_surviving_disease_count"] >= 1 or row[
            "core_all_multivariable_surviving_disease_count"
        ] >= 1:
            calls.append("PARK_RESIDUAL_SIGNAL_NEEDS_NONEXPRESSION_ANCHOR")
        else:
            calls.append("PARK_WEAK_RESIDUAL_SIGNAL_ONLY")
    out["wave102_call"] = calls
    call_priority = {
        "REOPEN_FOR_WAVE103_TARGET_SPECIFIC_FORCING": 0,
        "PARK_RESIDUAL_SIGNAL_NEEDS_NONEXPRESSION_ANCHOR": 1,
        "PARK_WEAK_RESIDUAL_SIGNAL_ONLY": 2,
        "NO_GO_MODULE_CONFOUNDED_OR_UNSTABLE": 3,
        "NO_GO_NO_DIRECT_H5AD_REPLICATION": 4,
    }
    out["wave102_call_priority"] = out["wave102_call"].map(call_priority).fillna(99).astype(int)
    return out.sort_values(
        ["wave102_call_priority", "wave102_residual_priority_score", "raw_positive_disease_count"],
        ascending=[True, False, False],
    )


def write_report(summary_table: pd.DataFrame, run_summary: dict[str, Any]) -> None:
    cols = [
        "gene",
        "wave102_call",
        "wave102_residual_priority_score",
        "present_analysis_count",
        "raw_positive_disease_count",
        "retained_positive_disease_count",
        "strict_core_covariate_surviving_disease_count",
        "core_all_multivariable_surviving_disease_count",
        "non_ibd_retained_positive_disease_count",
        "lipid_lysosomal_surviving_disease_count",
        "raw_negative_analysis_count",
        "raw_positive_analyses",
        "top_retained_tests",
    ]
    report = f"""# Wave102 Accessible-Survivor Residual Compartment Test

## Bottom Line

Branch call: `{run_summary["branch_call"]}`.

This test asks whether accessible survivors remain disease-associated after
same-compartment donor-level adjustment for lipid-lysosomal, lysosomal/APC,
IFN/APC, NF-kB, and HIF/NAMPT inflammatory modules. Passing this test is not a
therapeutic claim; it only justifies spending effort on target-specific
perturbation, genetics, and modality.

## Candidate Summary

{markdown_table(summary_table[cols], max_rows=30)}

## Guardrail

Residual survival can still reflect severity, cell composition within broad
compartments, batch, medication, tissue injury, or unmodeled stromal state.
Failure, however, is strong evidence against treating a candidate expression
signal as a mechanistic anchor in this V3 session.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave102_accessible_survivor_residual_compartment_test.py")}`
- Donor scores: `{rel(OUT / "accessible_survivor_donor_scores.tsv")}`
- Raw tests: `{rel(OUT / "accessible_survivor_raw_tests.tsv")}`
- Residual tests: `{rel(OUT / "accessible_survivor_residual_tests.tsv")}`
- Summary: `{rel(OUT / "accessible_survivor_residual_summary.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    residual_gate.TARGET_GENES = sorted(CANDIDATES)
    cache: dict[Path, tuple] = {}
    gene_score_tables: list[pd.DataFrame] = []
    presence_tables: list[pd.DataFrame] = []
    run_log: list[dict[str, Any]] = []
    for config in CONFIGS:
        try:
            print(f"[wave102] starting {config.name}", flush=True)
            if config.path not in cache:
                a = ad.read_h5ad(config.path)
                x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
                cache[config.path] = (a, x)
            a, x = cache[config.path]
            scores, presence = residual_gate.aggregate_config(config, a, x)
            gene_score_tables.append(scores)
            presence_tables.append(presence)
            run_log.append(
                {
                    "analysis": config.name,
                    "status": "completed",
                    "n_donor_gene_rows": int(len(scores)),
                    "n_present_genes": int(presence["gene"].nunique()),
                }
            )
            print(f"[wave102] completed {config.name}: {len(scores)} rows", flush=True)
        except Exception as exc:
            run_log.append(
                {
                    "analysis": config.name,
                    "status": "failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            print(f"[wave102] failed {config.name}: {type(exc).__name__}: {exc}", flush=True)

    gene_scores = pd.concat(gene_score_tables, ignore_index=True) if gene_score_tables else pd.DataFrame()
    presence = pd.concat(presence_tables, ignore_index=True) if presence_tables else pd.DataFrame()
    gene_scores.to_csv(OUT / "accessible_survivor_donor_scores.tsv", sep="\t", index=False)
    presence.to_csv(OUT / "accessible_survivor_gene_presence.tsv", sep="\t", index=False)

    if gene_scores.empty:
        payload = {
            "random_seed": SEED,
            "branch_call": "FAILED_NO_DONOR_SCORES",
            "run_log": run_log,
            "guardrail": "No target claim; no donor-level data were generated.",
        }
        write_json(OUT / "summary.json", payload)
        return

    raw_tests = residual_gate.run_raw_tests(gene_scores)
    residuals = residual_gate.run_residual_tests(gene_scores, residual_gate.load_module_wide())
    summary_table = summarize(raw_tests, residuals, presence)

    wave101 = read_tsv(W101)
    if not wave101.empty and "gene" in wave101.columns:
        wave101_keep = wave101[
            [
                col
                for col in [
                    "gene",
                    "wave101_call",
                    "wave101_score",
                    "ms_delta_log2",
                    "ms_p",
                    "positive_disease_count",
                    "negative_disease_count",
                    "wave101_missing_gates",
                ]
                if col in wave101.columns
            ]
        ].copy()
        summary_table = summary_table.merge(wave101_keep, on="gene", how="left")

    raw_tests.to_csv(OUT / "accessible_survivor_raw_tests.tsv", sep="\t", index=False)
    residuals.to_csv(OUT / "accessible_survivor_residual_tests.tsv", sep="\t", index=False)
    summary_table.to_csv(OUT / "accessible_survivor_residual_summary.tsv", sep="\t", index=False)

    reopened = summary_table[summary_table["wave102_call"].eq("REOPEN_FOR_WAVE103_TARGET_SPECIFIC_FORCING")]
    branch_call = (
        "REOPEN_ACCESSIBLE_SURVIVOR_TARGET_FORCING"
        if not reopened.empty
        else "NO_ACCESSIBLE_SURVIVOR_RESIDUAL_REOPEN"
    )
    payload = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "n_candidates": int(len(summary_table)),
        "call_counts": summary_table["wave102_call"].value_counts().to_dict(),
        "top_candidate": clean(summary_table.iloc[0]["gene"]) if not summary_table.empty else "",
        "top_candidate_call": clean(summary_table.iloc[0]["wave102_call"]) if not summary_table.empty else "",
        "run_log": run_log,
        "covariate_modules": residual_gate.COVARIATE_MODULES,
        "core_covariates": residual_gate.CORE_COVARIATES,
        "guardrail": (
            "This is donor-level residualized expression evidence. It does not "
            "supply target-specific perturbation, genetic causality, modality, "
            "novelty, or safety evidence."
        ),
        "top_rows": summary_table.head(20).to_dict(orient="records"),
    }
    write_json(OUT / "summary.json", payload)
    write_report(summary_table, payload)


if __name__ == "__main__":
    main()
