#!/usr/bin/env python3
"""Test whether antigen-processing state survives generic IFN-score control.

This is an adversarial analysis prompted by the hour-3 critique. For each
dataset/compartment contrast, it compares disease vs control on module scores
before and after residualizing target antigen-presentation modules against the
same-sample `ifn_apc` score.

The analysis is intentionally conservative: each donor/sample is the unit, and
the IFN residual model is fit only within the relevant case/control contrast.
"""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "residualization"

TARGET_MODULES = [
    "hla_ii_apc",
    "mif_cd74_receptor_state",
    "lysosomal_apc",
    "mixscale_validated_ifng_readout",
]


def hedges_g(case: np.ndarray, control: np.ndarray) -> float:
    case = np.asarray(case, dtype=float)
    control = np.asarray(control, dtype=float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if len(case) < 2 or len(control) < 2:
        return np.nan
    pooled = ((len(case) - 1) * case.var(ddof=1) + (len(control) - 1) * control.var(ddof=1)) / (len(case) + len(control) - 2)
    if pooled <= 0:
        return np.nan
    return ((case.mean() - control.mean()) / math.sqrt(pooled)) * (1 - 3 / (4 * (len(case) + len(control)) - 9))


def compare_values(df: pd.DataFrame, value_col: str) -> dict[str, float | int]:
    case = df.loc[df["group"].eq("case"), value_col].to_numpy(float)
    control = df.loc[df["group"].eq("control"), value_col].to_numpy(float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if len(case) < 2 or len(control) < 2:
        return {
            "n_case": int(len(case)),
            "n_control": int(len(control)),
            "mean_case": np.nan,
            "mean_control": np.nan,
            "delta_case_minus_control": np.nan,
            "hedges_g": np.nan,
            "p": np.nan,
        }
    t, p = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
    return {
        "n_case": int(len(case)),
        "n_control": int(len(control)),
        "mean_case": float(np.nanmean(case)),
        "mean_control": float(np.nanmean(control)),
        "delta_case_minus_control": float(np.nanmean(case) - np.nanmean(control)),
        "hedges_g": hedges_g(case, control),
        "p": float(p),
    }


def residualize(y: np.ndarray, x: np.ndarray) -> tuple[np.ndarray, float, float]:
    valid = np.isfinite(y) & np.isfinite(x)
    residuals = np.full_like(y, np.nan, dtype=float)
    if valid.sum() < 4 or np.nanstd(x[valid]) == 0:
        return residuals, np.nan, np.nan
    slope, intercept, r_value, _, _ = stats.linregress(x[valid], y[valid])
    residuals[valid] = y[valid] - (intercept + slope * x[valid])
    return residuals, float(slope), float(r_value * r_value)


def direct_h5ad_wide() -> pd.DataFrame:
    path = ROOT / "results_v3" / "direct_h5ad_cell_state" / "direct_h5ad_donor_module_scores.tsv"
    long = pd.read_csv(path, sep="\t")
    long = long[long["module"].isin(["ifn_apc", *TARGET_MODULES])].copy()
    rows = []
    for keys, sub in long.groupby(["analysis", "disease_name", "compartment", "donor_id", "disease", "group"], dropna=False):
        row = dict(zip(["dataset", "disease_name", "compartment", "unit_id", "disease", "group"], keys))
        for _, r in sub.iterrows():
            row[str(r["module"])] = float(r["mean_score"])
            row[f"{r['module']}_high_fraction"] = float(r["high_fraction"])
        row["n_cells"] = int(sub["n_cells"].max())
        row["modality"] = "single_cell_or_single_nucleus_h5ad"
        rows.append(row)
    return pd.DataFrame(rows)


def thyroid_wide() -> pd.DataFrame:
    path = ROOT / "results_v3" / "gse248205_thyroid_spatial" / "gse248205_sample_module_scores.tsv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, sep="\t")
    rows = []
    for _, r in df.iterrows():
        for contrast_disease in ["Hashimoto thyroiditis", "Graves disease"]:
            if r["disease"] not in ["control", contrast_disease]:
                continue
            row = {
                "dataset": f"GSE248205_{contrast_disease.replace(' ', '_')}",
                "disease_name": contrast_disease,
                "compartment": "thyroid tissue spots",
                "unit_id": r["sample"],
                "disease": r["disease"],
                "group": "case" if r["disease"] == contrast_disease else "control",
                "modality": "spatial_visium",
                "n_cells": int(r["n_spots"]),
            }
            for module in ["ifn_apc", *TARGET_MODULES]:
                col = f"module_{module}"
                if col in df.columns:
                    row[module] = float(r[col])
            rows.append(row)
    return pd.DataFrame(rows)


def gse111972_wide() -> pd.DataFrame:
    spec = importlib.util.spec_from_file_location(
        "gse111972", ROOT / "scripts" / "v3_analyze_gse111972_microglia.py"
    )
    if spec is None or spec.loader is None:
        return pd.DataFrame()
    gse = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gse)
    meta = gse.load_sample_metadata()
    log_expr = gse.load_expression()
    meta = meta.loc[meta["sample"].isin(log_expr.columns)].reset_index(drop=True)
    scores = gse.module_scores(log_expr, meta).T.reset_index().rename(columns={"index": "unit_id"})
    scores = scores.rename(
        columns={
            "interferon_apc": "ifn_apc",
            "lysosome_antigen_processing": "lysosomal_apc",
        }
    )
    rows = []
    for _, r in meta.iterrows():
        for region_name, region_value in [("white matter microglia", "white_matter"), ("grey matter microglia", "grey_matter")]:
            if r["region"] != region_value:
                continue
            group = "case" if r["disease"] == "MS" else "control"
            row = {
                "dataset": f"GSE111972_{region_value}",
                "disease_name": "MS",
                "compartment": region_name,
                "unit_id": r["sample"],
                "disease": r["disease"],
                "group": group,
                "modality": "sorted_bulk_microglia",
                "n_cells": np.nan,
            }
            s = scores[scores["unit_id"].eq(r["sample"])]
            if not s.empty:
                for module in ["ifn_apc", "mif_cd74_receptor_state", "lysosomal_apc"]:
                    if module in s.columns:
                        row[module] = float(s.iloc[0][module])
            rows.append(row)
    return pd.DataFrame(rows)


def analyze_dataset(wide: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (dataset, disease_name, compartment, modality), sub in wide.groupby(["dataset", "disease_name", "compartment", "modality"], dropna=False):
        if sub["group"].nunique() != 2 or "ifn_apc" not in sub.columns:
            continue
        for target in TARGET_MODULES:
            if target not in sub.columns:
                continue
            tmp = sub[["unit_id", "group", "ifn_apc", target]].dropna().copy()
            if tmp["group"].nunique() != 2:
                continue
            raw = compare_values(tmp.rename(columns={target: "value"}), "value")
            residual, slope, r2 = residualize(tmp[target].to_numpy(float), tmp["ifn_apc"].to_numpy(float))
            tmp["residual"] = residual
            resid = compare_values(tmp, "residual")
            rows.append(
                {
                    "dataset": dataset,
                    "disease_name": disease_name,
                    "compartment": compartment,
                    "modality": modality,
                    "target_module": target,
                    "ifn_covariate": "ifn_apc",
                    "residual_model": f"{target} ~ ifn_apc",
                    "target_vs_ifn_slope": slope,
                    "target_vs_ifn_r2": r2,
                    **{f"raw_{k}": v for k, v in raw.items()},
                    **{f"residual_{k}": v for k, v in resid.items()},
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["raw_fdr"] = multipletests(out["raw_p"].fillna(1.0), method="fdr_bh")[1]
        out["residual_fdr"] = multipletests(out["residual_p"].fillna(1.0), method="fdr_bh")[1]
        out["residual_retains_nominal_support"] = (out["residual_delta_case_minus_control"] > 0) & (out["residual_p"] <= 0.10)
        out["raw_nominal_support"] = (out["raw_delta_case_minus_control"] > 0) & (out["raw_p"] <= 0.10)
    return out.sort_values(["residual_retains_nominal_support", "residual_p"], ascending=[False, True]) if not out.empty else out


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    wide = pd.concat([direct_h5ad_wide(), thyroid_wide(), gse111972_wide()], ignore_index=True, sort=False)
    wide.to_csv(OUT / "ifn_residualization_input_wide.tsv", sep="\t", index=False)
    results = analyze_dataset(wide)
    results.to_csv(OUT / "ifn_residualization_module_tests.tsv", sep="\t", index=False)

    if not results.empty:
        raw_supported = int(results["raw_nominal_support"].sum())
        residual_supported = int(results["residual_retains_nominal_support"].sum())
        disease_residual = (
            results[results["residual_retains_nominal_support"]]
            .groupby("disease_name")["target_module"]
            .apply(lambda x: ",".join(sorted(set(x))))
            .to_dict()
        )
    else:
        raw_supported = residual_supported = 0
        disease_residual = {}
    summary = {
        "random_seed": SEED,
        "n_input_units": int(wide.shape[0]),
        "n_tests": int(results.shape[0]),
        "raw_nominal_supported_tests": raw_supported,
        "ifn_residual_nominal_supported_tests": residual_supported,
        "residual_support_by_disease": disease_residual,
        "top_residual_support": (
            results[results["residual_retains_nominal_support"]]
            .head(25)
            .to_dict(orient="records")
            if not results.empty
            else []
        ),
        "guardrail": (
            "Residualizing target modules against ifn_apc removes one generic IFN dimension only. "
            "It does not control all severity, infiltration, treatment, or batch effects."
        ),
    }
    (OUT / "ifn_residualization_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
