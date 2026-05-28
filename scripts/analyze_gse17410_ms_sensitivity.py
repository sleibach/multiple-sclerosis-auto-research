#!/usr/bin/env python3
"""Sensitivity checks for the fragile GSE17410 MS pregnancy PBMC signal."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

from analyze_gse17410_ms_pregnancy_modules import load_metadata, parse_soft


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/pregnancy_dimension/gse17410_ms_sensitivity"

COMPONENTS = {
    "isg_only": ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15"],
    "cd74_alone": ["CD74"],
    "receptor_only_cd74_cd44_cxcr4": ["CD74", "CD44", "CXCR4"],
    "hla_ii_without_cd74": ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1"],
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"],
    "monocyte_marker": ["LYZ", "LST1", "S100A8", "S100A9", "FCGR3A", "MS4A7"],
    "pdc_marker": ["GZMB", "IRF7", "TCF4", "IL3RA", "CLEC4C"],
    "neutrophil_marker": ["CSF3R", "FCGR3B", "S100A8", "S100A9", "MPO"],
    "platelet_marker": ["PPBP", "PF4", "ITGA2B", "GP9"],
    "erythroid_marker": ["HBB", "HBA1", "HBA2", "ALAS2"],
}


def hedges_g(a: pd.Series, b: pd.Series) -> float:
    a = a.dropna().astype(float)
    b = b.dropna().astype(float)
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0:
        return np.nan
    return float(((a.mean() - b.mean()) / pooled) * (1 - 3 / (4 * (len(a) + len(b)) - 9)))


def contrast(scores: pd.Series, state: pd.Series) -> dict:
    month9 = scores[state == "month9_pregnancy_ms"]
    pre = scores[state == "pre_pregnancy_ms"]
    test = st.ttest_ind(month9, pre, equal_var=False, nan_policy="omit")
    return {
        "n_pre": int(len(pre)),
        "n_month9": int(len(month9)),
        "mean_pre": float(pre.mean()),
        "mean_month9": float(month9.mean()),
        "delta_month9_minus_pre": float(month9.mean() - pre.mean()),
        "hedges_g": hedges_g(month9, pre),
        "welch_p": float(test.pvalue),
    }


def residualize(y: pd.Series, cov: pd.DataFrame) -> pd.Series:
    frame = pd.concat([y.rename("y"), cov], axis=1).dropna()
    out = pd.Series(np.nan, index=y.index)
    if len(frame) < cov.shape[1] + 4:
        return out
    x = sm.add_constant(frame[cov.columns])
    fit = sm.OLS(frame["y"], x).fit()
    out.loc[frame.index] = fit.resid
    return out


def md_tsv(df: pd.DataFrame) -> str:
    return "```tsv\n" + df.to_csv(sep="\t", index=False) + "```"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = load_metadata()
    platform, expr = parse_soft()
    probe_map = platform[["ID", "Gene Symbol"]].rename(columns={"ID": "probe_id", "Gene Symbol": "symbol"})
    probe_map["symbol"] = probe_map["symbol"].fillna("").str.split(" /// ").str[0].str.strip()
    wanted = sorted({g for genes in COMPONENTS.values() for g in genes})
    probe_map = probe_map[probe_map["symbol"].isin(wanted)]
    expr = expr.loc[expr.index.intersection(probe_map["probe_id"])]
    symbol_expr = expr.merge(probe_map, left_index=True, right_on="probe_id").groupby("symbol").mean(numeric_only=True)

    scores = meta[["geo_accession", "title", "state"]].copy()
    coverage = []
    for comp, genes in COMPONENTS.items():
        present = [g for g in genes if g in symbol_expr.index]
        coverage.append({"component": comp, "present": ";".join(present), "missing": ";".join(sorted(set(genes) - set(present))), "n_present": len(present)})
        scores[comp] = scores["geo_accession"].map(symbol_expr.loc[present].mean(axis=0).to_dict()) if present else np.nan
    scores = scores[scores["state"].isin(["pre_pregnancy_ms", "month9_pregnancy_ms"])].copy()
    scores.to_csv(OUT / "component_scores.tsv", sep="\t", index=False)
    pd.DataFrame(coverage).to_csv(OUT / "component_gene_coverage.tsv", sep="\t", index=False)

    contrasts = []
    for comp in COMPONENTS:
        row = {"component": comp, **contrast(scores[comp], scores["state"])}
        contrasts.append(row)
    contrast_df = pd.DataFrame(contrasts)
    contrast_df["fdr"] = multipletests(contrast_df["welch_p"].fillna(1), method="fdr_bh")[1]
    contrast_df.to_csv(OUT / "component_contrasts.tsv", sep="\t", index=False)

    loo_rows = []
    for comp in COMPONENTS:
        for sample in scores["geo_accession"]:
            sub = scores[scores["geo_accession"] != sample]
            res = contrast(sub[comp], sub["state"])
            loo_rows.append({"component": comp, "left_out": sample, "left_out_state": scores.set_index("geo_accession").loc[sample, "state"], **res})
    loo = pd.DataFrame(loo_rows)
    loo.to_csv(OUT / "leave_one_out_contrasts.tsv", sep="\t", index=False)

    cov_cols = [c for c in ["monocyte_marker", "pdc_marker", "neutrophil_marker", "platelet_marker", "erythroid_marker"] if scores[c].notna().sum() >= 6]
    residual_rows = []
    for comp in ["ifn_apc", "isg_only", "cd74_alone", "receptor_only_cd74_cd44_cxcr4", "hla_ii_without_cd74"]:
        y = scores[comp]
        for covset_name, covset in {
            "monocyte_only": ["monocyte_marker"],
            "monocyte_pdc": ["monocyte_marker", "pdc_marker"],
            "all_available_composition": cov_cols,
        }.items():
            covset = [c for c in covset if c in cov_cols]
            if not covset:
                continue
            resid = residualize(y, scores[covset])
            residual_rows.append({"component": comp, "covariates": covset_name, **contrast(resid, scores["state"])})
    residual_df = pd.DataFrame(residual_rows)
    if not residual_df.empty:
        residual_df["fdr"] = multipletests(residual_df["welch_p"].fillna(1), method="fdr_bh")[1]
    residual_df.to_csv(OUT / "composition_residual_contrasts.tsv", sep="\t", index=False)

    ifn_loo = loo[loo["component"] == "ifn_apc"]
    summary = {
        "dataset": "GSE17410",
        "n_samples": int(len(scores)),
        "component_contrasts": contrast_df.to_dict(orient="records"),
        "ifn_apc_leave_one_out_min_delta": float(ifn_loo["delta_month9_minus_pre"].min()),
        "ifn_apc_leave_one_out_max_p": float(ifn_loo["welch_p"].max()),
        "composition_covariates_available": cov_cols,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))

    report = [
        "# GSE17410 MS Pregnancy Sensitivity",
        "",
        "## Component Contrasts",
        md_tsv(contrast_df.sort_values("welch_p")),
        "",
        "## IFN/APC Leave-One-Out Summary",
        md_tsv(ifn_loo.sort_values("welch_p", ascending=False).head(10)),
        "",
        "## Composition Residual Contrasts",
        md_tsv(residual_df.sort_values("welch_p") if not residual_df.empty else residual_df),
        "",
        "## Interpretation Guardrail",
        "This sensitivity analysis tests robustness of the small GSE17410 PBMC observation. It cannot prove cell-intrinsic activation because only bulk PBMC expression is available.",
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
