#!/usr/bin/env python3
"""Wave106 CD82 specificity and confounder audit.

Wave105 says CD82 matched-niche coupling survives a robustness grid in Crohn
and Sjogren. This script asks a harsher question: is CD82 specifically coupled
to myeloid lipid/lysosomal modules, or is it just a proxy for generic target
APC activation / tissue inflammation?
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json
from v3_wave104_accessible_survivor_niche_controller_test import MIN_PAIRS, clean, linreg, residualize


SEED = 20260527
GENE = "CD82"
OUT = ROOT / "results_v3" / "wave106_cd82_specificity_confounder_audit"
PAIRS = ROOT / "results_v3" / "wave104_accessible_survivor_niche_controller_test" / "matched_niche_pairs.tsv"
W105 = ROOT / "results_v3" / "wave105_cd82_niche_robustness_audit" / "cd82_robust_tests.tsv"

PRIMARY_MODULES = ["lysosomal_apc", "lipid_loader_repair", "complement_phagocytosis"]
CONTROL_MODULES = ["ifn_apc", "inflammatory_nfkb", "hif_nampt_metabolic", "hla_ii_apc"]

BASE_COVARIATES = [
    "case_indicator",
    "target_inflammatory_nfkb",
    "target_hif_nampt_metabolic",
    "source_inflammatory_nfkb",
    "source_hif_nampt_metabolic",
]

BROAD_COVARIATES = [
    *BASE_COVARIATES,
    "target_ifn_apc",
    "source_ifn_apc",
    "target_hla_ii_apc",
    "source_hla_ii_apc",
    "source_lipid_loader_repair",
    "source_lysosomal_apc",
]


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def covariates_for(sub: pd.DataFrame, requested: list[str], outcome_col: str) -> tuple[pd.DataFrame, list[str], str]:
    cols = [col for col in requested if col in sub.columns and col != outcome_col]
    usable = []
    for col in cols:
        vals = pd.to_numeric(sub[col], errors="coerce").to_numpy(float)
        finite = np.isfinite(vals)
        if finite.sum() >= MIN_PAIRS and np.nanstd(vals[finite]) > 1e-8:
            usable.append(col)
    if not usable:
        return pd.DataFrame(index=sub.index), [], "none"
    cov = sub[usable].apply(pd.to_numeric, errors="coerce")
    complete = np.isfinite(cov.to_numpy(float)).all(axis=1)
    n_complete = int(complete.sum())
    if n_complete < max(MIN_PAIRS, len(usable) + 5):
        return cov, usable, f"underpowered_complete_n_{n_complete}_p_{len(usable)}"
    return cov, usable, "fixed"


def fit(sub: pd.DataFrame, outcome_col: str, cov: pd.DataFrame) -> dict[str, Any]:
    x = pd.to_numeric(sub["source_gene_z"], errors="coerce").to_numpy(float)
    y = pd.to_numeric(sub[outcome_col], errors="coerce").to_numpy(float)
    xr, n_x, x_r2 = residualize(x, cov)
    yr, n_y, y_r2 = residualize(y, cov)
    out = linreg(xr, yr)
    out["x_covariate_r2"] = x_r2
    out["y_covariate_r2"] = y_r2
    out["n_x_complete"] = n_x
    out["n_y_complete"] = n_y
    return out


def run_tests(pairs: pd.DataFrame) -> pd.DataFrame:
    if pairs.empty:
        return pd.DataFrame()
    pairs = pairs[pairs["gene"].eq(GENE)].copy()
    pairs["case_indicator"] = pairs["group"].eq("case").astype(float)
    rows: list[dict[str, Any]] = []
    modules = list(dict.fromkeys(PRIMARY_MODULES + CONTROL_MODULES))
    for (source_analysis, target_analysis), sub0 in pairs.groupby(["source_analysis", "target_analysis"], observed=True):
        sub0 = sub0.copy()
        first = sub0.iloc[0]
        for module in modules:
            outcome_col = f"target_{module}"
            if outcome_col not in sub0.columns:
                continue
            sub = sub0[np.isfinite(pd.to_numeric(sub0[outcome_col], errors="coerce"))].copy()
            if len(sub) < MIN_PAIRS:
                continue
            for model, requested in [
                ("M0_raw", []),
                ("M3_base_inflammation", BASE_COVARIATES),
                ("M7_broad_nonoutcome_context", BROAD_COVARIATES),
            ]:
                cov, selected, mode = covariates_for(sub, requested, outcome_col)
                if mode.startswith("underpowered"):
                    rows.append(
                        {
                            "gene": GENE,
                            "source_analysis": source_analysis,
                            "target_analysis": target_analysis,
                            "disease_name": first["disease_name"],
                            "source_compartment": first["source_compartment"],
                            "target_compartment": first["target_compartment"],
                            "outcome_module": module,
                            "outcome_class": "primary" if module in PRIMARY_MODULES else "control",
                            "model": model,
                            "covariate_mode": mode,
                            "covariates": ";".join(selected),
                            "covariate_count": len(selected),
                            "n": 0,
                            "slope": math.nan,
                            "r": math.nan,
                            "p": math.nan,
                        }
                    )
                    continue
                res = fit(sub, outcome_col, cov)
                rows.append(
                    {
                        "gene": GENE,
                        "source_analysis": source_analysis,
                        "target_analysis": target_analysis,
                        "disease_name": first["disease_name"],
                        "source_compartment": first["source_compartment"],
                        "target_compartment": first["target_compartment"],
                        "outcome_module": module,
                        "outcome_class": "primary" if module in PRIMARY_MODULES else "control",
                        "model": model,
                        "covariate_mode": mode,
                        "covariates": ";".join(selected),
                        "covariate_count": len(selected),
                        **res,
                    }
                )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["positive_nominal"] = (out["slope"] > 0) & (out["p"] < 0.05) & (out["n"] >= MIN_PAIRS)
        out["negative_nominal"] = (out["slope"] < 0) & (out["p"] < 0.05) & (out["n"] >= MIN_PAIRS)
    return out


def summarize(tests: pd.DataFrame, robust: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if tests.empty:
        return pd.DataFrame()
    contexts = tests[["source_analysis", "target_analysis", "disease_name"]].drop_duplicates()
    robust_keys = set()
    if not robust.empty:
        for _, r in robust.iterrows():
            robust_keys.add((r["source_analysis"], r["target_analysis"], r["disease_name"]))
    for _, ctx in contexts.iterrows():
        key = (ctx["source_analysis"], ctx["target_analysis"], ctx["disease_name"])
        sub = tests[
            tests["source_analysis"].eq(ctx["source_analysis"])
            & tests["target_analysis"].eq(ctx["target_analysis"])
            & tests["disease_name"].eq(ctx["disease_name"])
        ]
        m3 = sub[sub["model"].eq("M3_base_inflammation")]
        m7 = sub[sub["model"].eq("M7_broad_nonoutcome_context")]
        primary_m3 = m3[m3["outcome_class"].eq("primary")]
        control_m3 = m3[m3["outcome_class"].eq("control")]
        primary_m7 = m7[m7["outcome_class"].eq("primary")]
        control_m7 = m7[m7["outcome_class"].eq("control")]
        best_primary_m3 = primary_m3["p"].min(skipna=True)
        best_control_m3 = control_m3["p"].min(skipna=True)
        best_primary_m7 = primary_m7["p"].min(skipna=True)
        best_control_m7 = control_m7["p"].min(skipna=True)
        primary_pos_m3 = primary_m3[primary_m3["positive_nominal"]]
        control_pos_m3 = control_m3[control_m3["positive_nominal"]]
        primary_pos_m7 = primary_m7[primary_m7["positive_nominal"]]
        control_pos_m7 = control_m7[control_m7["positive_nominal"]]
        specificity_call = "NO_PRIMARY_SIGNAL"
        if len(primary_pos_m3) > 0:
            if len(control_pos_m3) == 0:
                specificity_call = "SPECIFIC_PRIMARY_OVER_CONTROLS_M3"
            else:
                specificity_call = "GENERIC_TARGET_ACTIVATION_COUPLING"
        if len(primary_pos_m7) > 0 and len(control_pos_m7) == 0:
            specificity_call = "SPECIFIC_PRIMARY_OVER_CONTROLS_M7"
        elif len(primary_pos_m7) > 0 and len(control_pos_m7) > 0:
            specificity_call = "GENERIC_TARGET_ACTIVATION_COUPLING_M7"
        rows.append(
            {
                "gene": GENE,
                "source_analysis": ctx["source_analysis"],
                "target_analysis": ctx["target_analysis"],
                "disease_name": ctx["disease_name"],
                "wave105_robust_context": key in robust_keys,
                "primary_positive_m3_count": int(len(primary_pos_m3)),
                "control_positive_m3_count": int(len(control_pos_m3)),
                "primary_positive_m7_count": int(len(primary_pos_m7)),
                "control_positive_m7_count": int(len(control_pos_m7)),
                "best_primary_m3_p": best_primary_m3,
                "best_control_m3_p": best_control_m3,
                "best_primary_m7_p": best_primary_m7,
                "best_control_m7_p": best_control_m7,
                "specificity_call": specificity_call,
                "best_primary_modules_m3": ";".join(primary_pos_m3["outcome_module"].tolist()),
                "best_control_modules_m3": ";".join(control_pos_m3["outcome_module"].tolist()),
                "best_primary_modules_m7": ";".join(primary_pos_m7["outcome_module"].tolist()),
                "best_control_modules_m7": ";".join(control_pos_m7["outcome_module"].tolist()),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["wave105_robust_context", "specificity_call", "best_primary_m3_p"],
        ascending=[False, True, True],
    )


def write_report(tests: pd.DataFrame, summary: pd.DataFrame, payload: dict[str, Any]) -> None:
    summary_cols = [
        "source_analysis",
        "target_analysis",
        "disease_name",
        "wave105_robust_context",
        "specificity_call",
        "primary_positive_m3_count",
        "control_positive_m3_count",
        "primary_positive_m7_count",
        "control_positive_m7_count",
        "best_primary_modules_m3",
        "best_control_modules_m3",
        "best_primary_modules_m7",
        "best_control_modules_m7",
    ]
    test_cols = [
        "source_analysis",
        "target_analysis",
        "disease_name",
        "outcome_module",
        "outcome_class",
        "model",
        "covariate_mode",
        "n",
        "slope",
        "p",
        "positive_nominal",
    ]
    report = f"""# Wave106 CD82 Specificity / Confounder Audit

## Bottom Line

Branch call: `{payload["branch_call"]}`.

This test asks whether CD82's matched-niche signal is specific to myeloid
lipid/lysosomal modules or whether it is better explained as generic target
APC/inflammatory activation.

## Context Summary

{markdown_table(summary[summary_cols], max_rows=30) if not summary.empty else "_No summary rows._"}

## Top Tests

{markdown_table(tests.sort_values(["p"], na_position="last").head(80)[test_cols], max_rows=80) if not tests.empty else "_No tests._"}

## Interpretation

Specificity requires primary lipid/lysosomal positive tests without parallel
positive control-module tests (`ifn_apc`, `inflammatory_nfkb`,
`hif_nampt_metabolic`, `hla_ii_apc`) in the same paired context. If controls
are also positive, CD82 is interpreted as a generic tissue activation marker.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave106_cd82_specificity_confounder_audit.py")}`
- Input pairs: `{rel(PAIRS)}`
- Wave105 robust contexts: `{rel(W105)}`
- Tests: `{rel(OUT / "cd82_specificity_tests.tsv")}`
- Summary: `{rel(OUT / "cd82_specificity_summary.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pairs = read_tsv(PAIRS)
    robust = read_tsv(W105)
    tests = run_tests(pairs)
    summary = summarize(tests, robust)
    tests.to_csv(OUT / "cd82_specificity_tests.tsv", sep="\t", index=False)
    summary.to_csv(OUT / "cd82_specificity_summary.tsv", sep="\t", index=False)
    robust_specific = summary[
        summary["wave105_robust_context"]
        & summary["specificity_call"].isin(["SPECIFIC_PRIMARY_OVER_CONTROLS_M3", "SPECIFIC_PRIMARY_OVER_CONTROLS_M7"])
    ]
    generic = summary[summary["wave105_robust_context"] & summary["specificity_call"].str.startswith("GENERIC")]
    branch_call = (
        "CD82_SPECIFIC_NICHE_SIGNAL_SURVIVES"
        if robust_specific["disease_name"].nunique() >= 2 and generic.empty
        else "CD82_SIGNAL_PARTLY_GENERIC_OR_CONTEXT_LIMITED"
    )
    payload = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "n_tests": int(len(tests)),
        "n_contexts": int(len(summary)),
        "robust_specific_context_count": int(len(robust_specific)),
        "robust_specific_disease_count": int(robust_specific["disease_name"].nunique()) if not robust_specific.empty else 0,
        "robust_generic_context_count": int(len(generic)),
        "inputs": {"pairs": rel(PAIRS), "wave105_robust": rel(W105)},
    }
    write_json(OUT / "summary.json", payload)
    write_report(tests, summary, payload)


if __name__ == "__main__":
    main()
