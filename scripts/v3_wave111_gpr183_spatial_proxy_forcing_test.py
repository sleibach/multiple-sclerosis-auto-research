#!/usr/bin/env python3
"""Wave111 GPR183/EBI2 spatial-proxy forcing test.

The GPR183 route only remains interesting if ligand-producing tissue niches and
GPR183+ myeloid/APC response states co-occur in the same disease/donor context.
This script uses existing direct h5ad donor-level data as a spatial proxy:
non-myeloid ligand-axis expression paired with myeloid/APC GPR183 and response
modules from the same donor.
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
from v3_wave104_accessible_survivor_niche_controller_test import MIN_PAIRS, linreg, residualize


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave111_gpr183_spatial_proxy_forcing_test"
DONOR = ROOT / "phases/v3/results" / "wave102_accessible_survivor_residual_compartment_test" / "accessible_survivor_donor_scores.tsv"
MODULES = ROOT / "phases/v3/results" / "direct_h5ad_cell_state" / "direct_h5ad_donor_module_scores.tsv"
BROAD = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"

RECEPTOR = "GPR183"
LIGAND_GENES = ["CH25H", "CYP7B1", "HSD3B7", "CYP27A1"]
RESPONSE_MODULES = ["lysosomal_apc", "lipid_loader_repair", "complement_phagocytosis", "mif_cd74_receptor_state"]
CONTROL_MODULES = ["ifn_apc", "inflammatory_nfkb", "hif_nampt_metabolic", "hla_ii_apc"]


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def module_wide(modules: pd.DataFrame) -> pd.DataFrame:
    base = ["analysis", "dataset_path", "disease_name", "compartment", "donor_id", "disease", "group"]
    wide = modules.pivot_table(index=base, columns="module", values="mean_score", aggfunc="mean").reset_index()
    wide.columns.name = None
    return wide


def build_donor_scores() -> pd.DataFrame:
    donor = read_tsv(DONOR)
    modules = read_tsv(MODULES)
    if donor.empty or modules.empty:
        return pd.DataFrame()
    wanted = [RECEPTOR, *LIGAND_GENES]
    donor = donor[donor["gene"].isin(wanted)].copy()
    if donor.empty:
        return pd.DataFrame()
    role_map = donor[["analysis", "role"]].drop_duplicates()
    wide = module_wide(modules).merge(role_map, on="analysis", how="left")
    gene_wide = donor.pivot_table(
        index=[
            "analysis",
            "dataset_path",
            "disease_name",
            "compartment",
            "role",
            "donor_id",
            "disease",
            "group",
        ],
        columns="gene",
        values="mean_z_vs_controls",
        aggfunc="mean",
    ).reset_index()
    gene_wide.columns.name = None
    merged = gene_wide.merge(
        wide,
        on=["analysis", "dataset_path", "disease_name", "compartment", "donor_id", "disease", "group", "role"],
        how="left",
    )
    ligand_cols = [g for g in LIGAND_GENES if g in merged.columns]
    if ligand_cols:
        merged["ligand_axis_mean_z"] = merged[ligand_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
        merged["ligand_axis_max_z"] = merged[ligand_cols].apply(pd.to_numeric, errors="coerce").max(axis=1)
    else:
        merged["ligand_axis_mean_z"] = np.nan
        merged["ligand_axis_max_z"] = np.nan
    return merged


def build_pairs(scores: pd.DataFrame) -> pd.DataFrame:
    if scores.empty:
        return pd.DataFrame()
    source = scores[scores["role"].ne("myeloid_apc")].copy()
    target = scores[scores["role"].eq("myeloid_apc")].copy()
    source = source.rename(
        columns={
            "analysis": "source_analysis",
            "compartment": "source_compartment",
            "role": "source_role",
            "ligand_axis_mean_z": "source_ligand_axis_mean_z",
            "ligand_axis_max_z": "source_ligand_axis_max_z",
        }
    )
    target = target.rename(
        columns={
            "analysis": "target_analysis",
            "compartment": "target_compartment",
            "role": "target_role",
            RECEPTOR: "target_gpr183_z",
        }
    )
    keep_source = [
        "source_analysis",
        "dataset_path",
        "disease_name",
        "source_compartment",
        "source_role",
        "donor_id",
        "disease",
        "group",
        "source_ligand_axis_mean_z",
        "source_ligand_axis_max_z",
        *[g for g in LIGAND_GENES if g in source.columns],
    ]
    keep_target = [
        "target_analysis",
        "dataset_path",
        "disease_name",
        "target_compartment",
        "target_role",
        "donor_id",
        "disease",
        "group",
        "target_gpr183_z",
        *[m for m in RESPONSE_MODULES + CONTROL_MODULES if m in target.columns],
    ]
    pairs = source[keep_source].merge(
        target[keep_target],
        on=["dataset_path", "disease_name", "donor_id", "disease", "group"],
        how="inner",
    )
    pairs["case_indicator"] = pairs["group"].eq("case").astype(float)
    return pairs


def partial_fit(sub: pd.DataFrame, x_col: str, y_col: str, cov_cols: list[str]) -> dict[str, Any]:
    cov_cols = [c for c in cov_cols if c in sub.columns and c not in {x_col, y_col}]
    usable = []
    for col in cov_cols:
        vals = pd.to_numeric(sub[col], errors="coerce").to_numpy(float)
        finite = np.isfinite(vals)
        if finite.sum() >= MIN_PAIRS and np.nanstd(vals[finite]) > 1e-8:
            usable.append(col)
    cov = sub[usable].apply(pd.to_numeric, errors="coerce") if usable else pd.DataFrame(index=sub.index)
    if usable:
        complete = int(np.isfinite(cov.to_numpy(float)).all(axis=1).sum())
        if complete < max(MIN_PAIRS, len(usable) + 5):
            return {"n": 0, "slope": math.nan, "p": math.nan, "r": math.nan, "covariates": ";".join(usable), "covariate_mode": f"underpowered_n_{complete}_p_{len(usable)}"}
    x = pd.to_numeric(sub[x_col], errors="coerce").to_numpy(float)
    y = pd.to_numeric(sub[y_col], errors="coerce").to_numpy(float)
    xr, _, _ = residualize(x, cov)
    yr, _, _ = residualize(y, cov)
    res = linreg(xr, yr)
    res["covariates"] = ";".join(usable)
    res["covariate_mode"] = "fixed" if usable else "none"
    return res


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
    out.loc[ordered.index] = np.minimum(q, 1.0)
    return out


def run_tests(pairs: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if pairs.empty:
        return pd.DataFrame()
    for (source_analysis, target_analysis), sub0 in pairs.groupby(["source_analysis", "target_analysis"], observed=True):
        sub0 = sub0.copy()
        if len(sub0) < MIN_PAIRS:
            continue
        first = sub0.iloc[0]
        ligand_cols = ["source_ligand_axis_mean_z", "source_ligand_axis_max_z"]
        for ligand_col in ligand_cols:
            rec = partial_fit(sub0, ligand_col, "target_gpr183_z", ["case_indicator"])
            rows.append(
                {
                    "test_class": "ligand_to_receptor",
                    "source_analysis": source_analysis,
                    "target_analysis": target_analysis,
                    "disease_name": first["disease_name"],
                    "source_compartment": first["source_compartment"],
                    "target_compartment": first["target_compartment"],
                    "predictor": ligand_col,
                    "outcome": "target_gpr183_z",
                    **rec,
                }
            )
            for module in RESPONSE_MODULES + CONTROL_MODULES:
                if module not in sub0.columns:
                    continue
                rec2 = partial_fit(sub0, ligand_col, module, ["case_indicator", "target_gpr183_z"])
                rows.append(
                    {
                        "test_class": "ligand_to_response_after_receptor",
                        "source_analysis": source_analysis,
                        "target_analysis": target_analysis,
                        "disease_name": first["disease_name"],
                        "source_compartment": first["source_compartment"],
                        "target_compartment": first["target_compartment"],
                        "predictor": ligand_col,
                        "outcome": module,
                        "outcome_class": "response" if module in RESPONSE_MODULES else "control",
                        **rec2,
                    }
                )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["positive_nominal"] = (out["slope"] > 0) & (out["p"] < 0.05) & (out["n"] >= MIN_PAIRS)
        out["q_all"] = bh_q(out["p"])
        out["positive_q10"] = (out["slope"] > 0) & (out["q_all"] < 0.10) & (out["n"] >= MIN_PAIRS)
    return out


def summarize(tests: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if tests.empty:
        return pd.DataFrame()
    for (disease, source, target), sub in tests.groupby(["disease_name", "source_analysis", "target_analysis"], observed=True):
        lr = sub[sub["test_class"].eq("ligand_to_receptor")]
        resp = sub[(sub["test_class"].eq("ligand_to_response_after_receptor")) & sub["outcome_class"].eq("response")]
        ctrl = sub[(sub["test_class"].eq("ligand_to_response_after_receptor")) & sub["outcome_class"].eq("control")]
        rows.append(
            {
                "disease_name": disease,
                "source_analysis": source,
                "target_analysis": target,
                "ligand_to_receptor_positive_q10": int(lr["positive_q10"].sum()) if not lr.empty else 0,
                "response_positive_q10": int(resp["positive_q10"].sum()) if not resp.empty else 0,
                "control_positive_q10": int(ctrl["positive_q10"].sum()) if not ctrl.empty else 0,
                "best_ligand_receptor_p": float(lr["p"].min(skipna=True)) if lr["p"].notna().any() else math.nan,
                "best_response_p": float(resp["p"].min(skipna=True)) if resp["p"].notna().any() else math.nan,
                "best_control_p": float(ctrl["p"].min(skipna=True)) if ctrl["p"].notna().any() else math.nan,
                "coherent_specific_context": bool(
                    (not lr.empty and lr["positive_q10"].any())
                    and (not resp.empty and resp["positive_q10"].any())
                    and (ctrl.empty or not ctrl["positive_q10"].any())
                ),
                "response_modules_positive": ";".join(resp[resp["positive_q10"]]["outcome"].dropna().astype(str).tolist()),
                "control_modules_positive": ";".join(ctrl[ctrl["positive_q10"]]["outcome"].dropna().astype(str).tolist()),
            }
        )
    return pd.DataFrame(rows).sort_values(["coherent_specific_context", "best_response_p"], ascending=[False, True])


def write_report(tests: pd.DataFrame, summary: pd.DataFrame, payload: dict[str, Any]) -> None:
    summary_cols = [
        "disease_name",
        "source_analysis",
        "target_analysis",
        "ligand_to_receptor_positive_q10",
        "response_positive_q10",
        "control_positive_q10",
        "coherent_specific_context",
        "response_modules_positive",
        "control_modules_positive",
    ]
    test_cols = [
        "test_class",
        "source_analysis",
        "target_analysis",
        "disease_name",
        "predictor",
        "outcome",
        "outcome_class",
        "n",
        "slope",
        "p",
        "q_all",
        "positive_q10",
    ]
    report = f"""# Wave111 GPR183 Spatial-Proxy Forcing Test

## Bottom Line

Branch call: `{payload["branch_call"]}`.

This test uses matched-donor compartment data as a spatial proxy. It requires
non-myeloid oxysterol-ligand-axis signal to predict myeloid/APC `GPR183`, and
then predict response modules after receptor adjustment, without parallel
control-module positives.

## Disease-Collapsed Summary

{markdown_table(summary[summary_cols], max_rows=40) if not summary.empty else "_No summary rows._"}

## Top Tests

{markdown_table(tests.sort_values("p", na_position="last").head(80)[test_cols], max_rows=80) if not tests.empty else "_No tests._"}

## Decision Rule

Promotion to a deeper GPR183 branch would require coherent specific contexts in
at least two diseases. A coherent context needs FDR10 ligand-to-receptor support
and FDR10 response support, with zero FDR10 control-module support.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave111_gpr183_spatial_proxy_forcing_test.py")}`
- Donor gene scores: `{rel(DONOR)}`
- Donor module scores: `{rel(MODULES)}`
- Pair output: `{rel(OUT / "gpr183_spatial_proxy_pairs.tsv")}`
- Test output: `{rel(OUT / "gpr183_spatial_proxy_tests.tsv")}`
- Summary output: `{rel(OUT / "gpr183_spatial_proxy_summary.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    scores = build_donor_scores()
    pairs = build_pairs(scores)
    tests = run_tests(pairs)
    summary = summarize(tests)
    scores.to_csv(OUT / "gpr183_gene_module_donor_scores.tsv", sep="\t", index=False)
    pairs.to_csv(OUT / "gpr183_spatial_proxy_pairs.tsv", sep="\t", index=False)
    tests.to_csv(OUT / "gpr183_spatial_proxy_tests.tsv", sep="\t", index=False)
    summary.to_csv(OUT / "gpr183_spatial_proxy_summary.tsv", sep="\t", index=False)
    coherent_diseases = int(summary[summary["coherent_specific_context"]]["disease_name"].nunique()) if not summary.empty else 0
    branch_call = (
        "REOPEN_GPR183_SPATIAL_PROXY_BRANCH"
        if coherent_diseases >= 2
        else "NO_REOPEN_GPR183_SPATIAL_PROXY"
    )
    payload = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "n_pairs": int(len(pairs)),
        "n_tests": int(len(tests)),
        "coherent_specific_disease_count": coherent_diseases,
        "inputs": {"donor_scores": rel(DONOR), "module_scores": rel(MODULES), "broad_h5ad": rel(BROAD)},
    }
    write_json(OUT / "summary.json", payload)
    write_report(tests, summary, payload)


if __name__ == "__main__":
    main()
