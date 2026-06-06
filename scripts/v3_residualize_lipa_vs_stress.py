#!/usr/bin/env python3
"""Residualize LIPA and comparator genes against stress/inflammatory modules.

The LIPA lane is only useful if it is not just a proxy for generic IFN,
NF-kB/inflammation, HIF/NAMPT metabolic stress, or the same lipid module used to
select it. This script performs donor-level univariate residual tests within
each direct h5ad compartment:

    gene_mean_z_vs_controls ~ module_mean_score

and retests disease-vs-control on the residuals.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "phases/v3/results"
OUT = RESULTS / "lipa_residualization"

GENES = [
    "LIPA",
    "ACSL1",
    "NAMPT",
    "CD74",
    "IFI30",
    "CTSS",
    "CTSB",
    "CTSD",
    "FABP5",
    "MSR1",
]

COVARIATE_MODULES = [
    "ifn_apc",
    "inflammatory_nfkb",
    "hif_nampt_metabolic",
    "lipid_loader_repair",
    "lysosomal_apc",
]


def hedges_g(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    x = x[np.isfinite(x)]
    y = y[np.isfinite(y)]
    nx = len(x)
    ny = len(y)
    if nx < 2 or ny < 2:
        return np.nan
    pooled = ((nx - 1) * x.var(ddof=1) + (ny - 1) * y.var(ddof=1)) / (nx + ny - 2)
    if pooled <= 0:
        return np.nan
    correction = 1.0 - (3.0 / (4.0 * (nx + ny) - 9.0))
    return ((x.mean() - y.mean()) / math.sqrt(pooled)) * correction


def contrast(values: pd.Series, groups: pd.Series) -> dict[str, float]:
    case = values.loc[groups == "case"].astype(float).to_numpy()
    control = values.loc[groups == "control"].astype(float).to_numpy()
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if len(case) < 2 or len(control) < 2:
        return {
            "n_case": len(case),
            "n_control": len(control),
            "mean_case": np.nan,
            "mean_control": np.nan,
            "delta_case_minus_control": np.nan,
            "hedges_g": np.nan,
            "p": np.nan,
        }
    t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
    return {
        "n_case": int(len(case)),
        "n_control": int(len(control)),
        "mean_case": float(np.mean(case)),
        "mean_control": float(np.mean(control)),
        "delta_case_minus_control": float(np.mean(case) - np.mean(control)),
        "hedges_g": float(hedges_g(case, control)),
        "p": float(p_value),
    }


def residualize(y: np.ndarray, x: np.ndarray) -> tuple[np.ndarray, float, float]:
    mask = np.isfinite(y) & np.isfinite(x)
    residuals = np.full(len(y), np.nan)
    if mask.sum() < 4 or np.nanstd(x[mask]) <= 0:
        return residuals, np.nan, np.nan
    slope, intercept, r_value, _, _ = stats.linregress(x[mask], y[mask])
    residuals[mask] = y[mask] - (intercept + slope * x[mask])
    return residuals, float(slope), float(r_value**2)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    gene_scores = pd.read_csv(
        RESULTS / "direct_h5ad_gene_replication" / "direct_h5ad_gene_donor_scores.tsv",
        sep="\t",
    )
    module_scores = pd.read_csv(
        RESULTS / "direct_h5ad_cell_state" / "direct_h5ad_donor_module_scores.tsv",
        sep="\t",
    )

    g = gene_scores.loc[gene_scores["gene"].isin(GENES)].copy()
    m = module_scores.loc[module_scores["module"].isin(COVARIATE_MODULES)].copy()
    m_wide = m.pivot_table(
        index=["analysis", "donor_id"],
        columns="module",
        values="mean_score",
        aggfunc="mean",
    ).reset_index()

    merged = g.merge(m_wide, on=["analysis", "donor_id"], how="left")
    merged.to_csv(OUT / "lipa_residualization_input.tsv", sep="\t", index=False)

    rows: list[dict[str, object]] = []
    for (analysis, gene), sub in merged.groupby(["analysis", "gene"], sort=True):
        sub = sub.copy()
        raw = contrast(sub["mean_z_vs_controls"], sub["group"])
        base = {
            "analysis": analysis,
            "disease_name": sub["disease_name"].iloc[0],
            "compartment": sub["compartment"].iloc[0],
            "gene": gene,
            "covariate_module": "RAW",
            "covariate_slope": np.nan,
            "covariate_r2": np.nan,
            **{f"raw_{k}": v for k, v in raw.items()},
            **{f"residual_{k}": v for k, v in raw.items()},
        }
        rows.append(base)
        for covariate in COVARIATE_MODULES:
            if covariate not in sub.columns:
                continue
            residuals, slope, r2 = residualize(
                sub["mean_z_vs_controls"].astype(float).to_numpy(),
                sub[covariate].astype(float).to_numpy(),
            )
            residual = contrast(pd.Series(residuals, index=sub.index), sub["group"])
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": sub["disease_name"].iloc[0],
                    "compartment": sub["compartment"].iloc[0],
                    "gene": gene,
                    "covariate_module": covariate,
                    "covariate_slope": slope,
                    "covariate_r2": r2,
                    **{f"raw_{k}": v for k, v in raw.items()},
                    **{f"residual_{k}": v for k, v in residual.items()},
                }
            )

    tests = pd.DataFrame(rows)
    mask = tests["covariate_module"].ne("RAW") & tests["residual_p"].notna()
    tests["residual_fdr"] = np.nan
    if mask.any():
        tests.loc[mask, "residual_fdr"] = multipletests(tests.loc[mask, "residual_p"], method="fdr_bh")[1]
    raw_mask = tests["covariate_module"].eq("RAW") & tests["raw_p"].notna()
    tests["raw_fdr_internal"] = np.nan
    if raw_mask.any():
        tests.loc[raw_mask, "raw_fdr_internal"] = multipletests(
            tests.loc[raw_mask, "raw_p"], method="fdr_bh"
        )[1]
    tests["retains_nominal_positive"] = (
        (tests["covariate_module"].ne("RAW"))
        & (tests["raw_delta_case_minus_control"] > 0)
        & (tests["raw_p"] < 0.05)
        & (tests["residual_delta_case_minus_control"] > 0)
        & (tests["residual_p"] < 0.05)
    )
    tests.to_csv(OUT / "lipa_residualization_tests.tsv", sep="\t", index=False)

    lipa = tests.loc[tests["gene"] == "LIPA"].copy()
    raw_lipa = lipa.loc[lipa["covariate_module"].eq("RAW")]
    lipa_resid = lipa.loc[lipa["covariate_module"].ne("RAW")]
    summary = {
        "random_seed": 20260526,
        "n_tests": int(len(tests)),
        "n_lipa_raw_positive_nominal": int(
            ((raw_lipa["raw_delta_case_minus_control"] > 0) & (raw_lipa["raw_p"] < 0.05)).sum()
        ),
        "n_lipa_raw_negative_nominal": int(
            ((raw_lipa["raw_delta_case_minus_control"] < 0) & (raw_lipa["raw_p"] < 0.05)).sum()
        ),
        "lipa_raw_positive_analyses": raw_lipa.loc[
            (raw_lipa["raw_delta_case_minus_control"] > 0) & (raw_lipa["raw_p"] < 0.05),
            ["analysis", "disease_name", "compartment", "raw_delta_case_minus_control", "raw_hedges_g", "raw_p"],
        ].to_dict(orient="records"),
        "lipa_raw_negative_analyses": raw_lipa.loc[
            (raw_lipa["raw_delta_case_minus_control"] < 0) & (raw_lipa["raw_p"] < 0.05),
            ["analysis", "disease_name", "compartment", "raw_delta_case_minus_control", "raw_hedges_g", "raw_p"],
        ].to_dict(orient="records"),
        "lipa_residual_retained_nominal_tests": lipa_resid.loc[
            lipa_resid["retains_nominal_positive"],
            [
                "analysis",
                "disease_name",
                "compartment",
                "covariate_module",
                "covariate_r2",
                "residual_delta_case_minus_control",
                "residual_hedges_g",
                "residual_p",
                "residual_fdr",
            ],
        ].to_dict(orient="records"),
        "guardrail": (
            "Univariate residuals control one same-compartment module at a time. "
            "They do not prove causality or fully remove severity, tissue damage, batch, or donor composition."
        ),
    }
    (OUT / "lipa_residualization_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
