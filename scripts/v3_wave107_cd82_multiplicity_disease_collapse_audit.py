#!/usr/bin/env python3
"""Wave107 CD82 multiplicity and disease-collapse audit.

Wave105 nominally reopened CD82, but the hostile methods review argued that
module rows from the same donor set were counted as independent replication.
This audit adds BH correction and collapses evidence to disease/source-target
units before making a branch call.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave107_cd82_multiplicity_disease_collapse_audit"
W105_GRID = ROOT / "phases/v3/results" / "wave105_cd82_niche_robustness_audit" / "cd82_model_grid_tests.tsv"
W105_SUMMARY = ROOT / "phases/v3/results" / "wave105_cd82_niche_robustness_audit" / "cd82_robustness_summary.tsv"
W106_SUMMARY = ROOT / "phases/v3/results" / "wave106_cd82_specificity_confounder_audit" / "cd82_specificity_summary.tsv"


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def bh_q(pvals: pd.Series) -> pd.Series:
    p = pd.to_numeric(pvals, errors="coerce")
    out = pd.Series(np.nan, index=p.index, dtype=float)
    finite = p[np.isfinite(p)]
    if finite.empty:
        return out
    ordered = finite.sort_values()
    n = len(ordered)
    q = ordered.to_numpy(float) * n / np.arange(1, n + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.minimum(q, 1.0)
    out.loc[ordered.index] = q
    return out


def fisher_p(pvals: list[float]) -> float:
    vals = [float(p) for p in pvals if np.isfinite(p) and p > 0]
    if not vals:
        return math.nan
    stat = -2.0 * float(np.sum(np.log(vals)))
    return float(stats.chi2.sf(stat, 2 * len(vals)))


def stouffer_signed_p(rows: pd.DataFrame, p_col: str = "m3_perm_p") -> float:
    vals = []
    for _, r in rows.iterrows():
        p = r.get(p_col, math.nan)
        slope = r.get("m3_slope", math.nan)
        if not np.isfinite(p) or p <= 0 or not np.isfinite(slope):
            continue
        z = stats.norm.isf(float(p) / 2.0)
        vals.append(z if float(slope) > 0 else -z)
    if not vals:
        return math.nan
    zsum = float(np.sum(vals) / math.sqrt(len(vals)))
    return float(stats.norm.sf(zsum))


def prepare_context_summary(summary: pd.DataFrame, specificity: pd.DataFrame) -> pd.DataFrame:
    if summary.empty:
        return pd.DataFrame()
    out = summary.copy()
    out["m3_p_q_all_contexts"] = bh_q(out["m3_p"])
    out["m3_perm_q_all_contexts"] = bh_q(out["m3_perm_p"])
    out["m3_nominal_positive"] = (out["m3_slope"] > 0) & (out["m3_p"] < 0.05)
    out["m3_perm_positive"] = out["m3_nominal_positive"] & (out["m3_perm_p"] < 0.05)
    out["m3_perm_q_positive"] = out["m3_nominal_positive"] & (out["m3_perm_q_all_contexts"] < 0.05)
    out["m4_estimable"] = np.isfinite(pd.to_numeric(out["m4_slope"], errors="coerce"))
    out["m4_positive"] = out["m4_estimable"] & (out["m4_slope"] > 0)
    if not specificity.empty:
        keep = [
            "source_analysis",
            "target_analysis",
            "disease_name",
            "specificity_call",
            "primary_positive_m3_count",
            "control_positive_m3_count",
            "primary_positive_m7_count",
            "control_positive_m7_count",
        ]
        out = out.merge(specificity[keep], on=["source_analysis", "target_analysis", "disease_name"], how="left")
    else:
        out["specificity_call"] = ""
    out["specific_primary_context"] = out["specificity_call"].isin(
        ["SPECIFIC_PRIMARY_OVER_CONTROLS_M3", "SPECIFIC_PRIMARY_OVER_CONTROLS_M7"]
    )
    out["generic_context"] = out["specificity_call"].fillna("").str.startswith("GENERIC")
    out["strict_context_pass"] = (
        out["m3_perm_q_positive"]
        & out["m4_estimable"]
        & out["m4_positive"]
        & out["specific_primary_context"]
        & ~out["generic_context"]
    )
    out["provisional_context_pass"] = (
        out["m3_perm_positive"]
        & out["specific_primary_context"]
        & ~out["generic_context"]
    )
    return out.sort_values(["strict_context_pass", "m3_perm_p"], ascending=[False, True])


def collapse_disease(contexts: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if contexts.empty:
        return pd.DataFrame()
    for (disease, source, target), sub in contexts.groupby(["disease_name", "source_analysis", "target_analysis"], observed=True):
        sub = sub.copy()
        rows.append(
            {
                "disease_name": disease,
                "source_analysis": source,
                "target_analysis": target,
                "n_module_contexts": int(len(sub)),
                "n_m3_perm_positive": int(sub["m3_perm_positive"].sum()),
                "n_m3_perm_q_positive": int(sub["m3_perm_q_positive"].sum()),
                "n_strict_context_pass": int(sub["strict_context_pass"].sum()),
                "n_provisional_context_pass": int(sub["provisional_context_pass"].sum()),
                "n_generic_context": int(sub["generic_context"].sum()),
                "best_m3_p": float(sub["m3_p"].min(skipna=True)) if sub["m3_p"].notna().any() else math.nan,
                "best_m3_perm_p": float(sub["m3_perm_p"].min(skipna=True)) if sub["m3_perm_p"].notna().any() else math.nan,
                "best_m3_perm_q": float(sub["m3_perm_q_all_contexts"].min(skipna=True))
                if sub["m3_perm_q_all_contexts"].notna().any()
                else math.nan,
                "fisher_m3_perm_p": fisher_p(sub["m3_perm_p"].tolist()),
                "stouffer_signed_m3_perm_p": stouffer_signed_p(sub, "m3_perm_p"),
                "module_signs": ";".join(
                    f"{r['target_module']}:{'+' if r['m3_slope'] > 0 else '-' if r['m3_slope'] < 0 else 'NA'}"
                    for _, r in sub.iterrows()
                    if np.isfinite(r.get("m3_slope", math.nan))
                ),
                "specificity_calls": ";".join(sorted(set(str(x) for x in sub["specificity_call"].dropna()))),
            }
        )
    out = pd.DataFrame(rows)
    out["fisher_q"] = bh_q(out["fisher_m3_perm_p"])
    out["stouffer_q"] = bh_q(out["stouffer_signed_m3_perm_p"])
    out["strict_disease_pass"] = (
        (out["n_strict_context_pass"] > 0)
        & (out["fisher_q"] < 0.05)
        & (out["stouffer_q"] < 0.05)
        & (out["n_generic_context"] == 0)
    )
    out["provisional_disease_pass"] = (
        (out["n_provisional_context_pass"] > 0)
        & (out["stouffer_signed_m3_perm_p"] < 0.05)
        & (out["n_generic_context"] == 0)
    )
    return out.sort_values(["strict_disease_pass", "provisional_disease_pass", "best_m3_perm_p"], ascending=[False, False, True])


def write_report(contexts: pd.DataFrame, disease: pd.DataFrame, payload: dict[str, Any]) -> None:
    context_cols = [
        "source_analysis",
        "target_analysis",
        "disease_name",
        "target_module",
        "m3_slope",
        "m3_p",
        "m3_perm_p",
        "m3_perm_q_all_contexts",
        "m4_estimable",
        "specificity_call",
        "strict_context_pass",
        "provisional_context_pass",
    ]
    disease_cols = [
        "disease_name",
        "source_analysis",
        "target_analysis",
        "n_module_contexts",
        "n_m3_perm_q_positive",
        "n_strict_context_pass",
        "n_provisional_context_pass",
        "n_generic_context",
        "fisher_m3_perm_p",
        "fisher_q",
        "stouffer_signed_m3_perm_p",
        "stouffer_q",
        "strict_disease_pass",
        "provisional_disease_pass",
        "specificity_calls",
    ]
    report = f"""# Wave107 CD82 Multiplicity / Disease-Collapse Audit

## Bottom Line

Branch call: `{payload["branch_call"]}`.

This audit implements the hostile methods review's core correction: do not
count multiple target modules from the same donor set as independent disease
replication, and do not call a context strong if it fails BH correction,
specificity controls, or estimable strict-model support.

## Disease-Collapsed Evidence

{markdown_table(disease[disease_cols], max_rows=30) if not disease.empty else "_No disease-collapsed rows._"}

## Context-Level Evidence

{markdown_table(contexts[context_cols], max_rows=40) if not contexts.empty else "_No context rows._"}

## Decision Rule

`CD82_REOPENED_AFTER_MULTIPLICITY_COLLAPSE` would require strict disease pass
in at least two diseases. Strict pass requires context-level BH-corrected
permutation support, estimable positive M4, specificity over control modules,
and no generic target-activation coupling.

## Interpretation

If this audit downgrades CD82, CD82 remains usable only as a provisional
matched-niche biomarker/readout for ex vivo mechanism experiments. It is not a
target and not an indirect intervention nomination.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave107_cd82_multiplicity_disease_collapse_audit.py")}`
- Wave105 context summary: `{rel(W105_SUMMARY)}`
- Wave105 model grid: `{rel(W105_GRID)}`
- Wave106 specificity summary: `{rel(W106_SUMMARY)}`
- Context output: `{rel(OUT / "cd82_context_multiplicity.tsv")}`
- Disease output: `{rel(OUT / "cd82_disease_collapsed_evidence.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary = read_tsv(W105_SUMMARY)
    specificity = read_tsv(W106_SUMMARY)
    contexts = prepare_context_summary(summary, specificity)
    disease = collapse_disease(contexts)
    contexts.to_csv(OUT / "cd82_context_multiplicity.tsv", sep="\t", index=False)
    disease.to_csv(OUT / "cd82_disease_collapsed_evidence.tsv", sep="\t", index=False)
    strict_disease_count = int(disease["strict_disease_pass"].sum()) if not disease.empty else 0
    provisional_disease_count = int(disease["provisional_disease_pass"].sum()) if not disease.empty else 0
    branch_call = (
        "CD82_REOPENED_AFTER_MULTIPLICITY_COLLAPSE"
        if strict_disease_count >= 2
        else "CD82_PROVISIONAL_NICHE_BIOMARKER_SIGNAL_NOT_REOPENED"
    )
    payload = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "strict_disease_pass_count": strict_disease_count,
        "provisional_disease_pass_count": provisional_disease_count,
        "n_contexts": int(len(contexts)),
        "n_disease_source_target_units": int(len(disease)),
        "inputs": {
            "wave105_summary": rel(W105_SUMMARY),
            "wave105_grid": rel(W105_GRID),
            "wave106_summary": rel(W106_SUMMARY),
        },
    }
    write_json(OUT / "summary.json", payload)
    write_report(contexts, disease, payload)


if __name__ == "__main__":
    main()
