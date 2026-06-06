#!/usr/bin/env python3
"""Wave105 CD82 matched-niche robustness audit.

Wave104 reopened CD82 because tissue-resident CD82 expression predicted
matched-donor myeloid lipid/lysosomal modules in three autoimmune tissue
contexts after adaptive covariate adjustment. This script tries to kill that
result by replacing the adaptive single model with a fixed model grid,
permutation p-values, and leave-one-donor-out influence checks.

This is a robustness audit, not a therapeutic nomination. Prior-art sidecars
already block direct CD82 therapeutic promotion.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json
from v3_wave104_accessible_survivor_niche_controller_test import (
    MIN_PAIRS,
    TARGET_MODULES,
    adaptive_covariates,
    clean,
    linreg,
    residualize,
)


SEED = 20260527
N_PERM = 2000
GENE = "CD82"
OUT = ROOT / "phases/v3/results" / "wave105_cd82_niche_robustness_audit"
W104 = ROOT / "phases/v3/results" / "wave104_accessible_survivor_niche_controller_test"
PAIRS = W104 / "matched_niche_pairs.tsv"
TESTS = W104 / "niche_controller_tests.tsv"


MODEL_SPECS: list[tuple[str, list[str], bool]] = [
    ("M0_raw", [], False),
    ("M1_case", ["case_indicator"], False),
    (
        "M2_target_inflammation",
        ["case_indicator", "target_inflammatory_nfkb", "target_hif_nampt_metabolic"],
        False,
    ),
    (
        "M3_source_target_inflammation",
        [
            "case_indicator",
            "target_inflammatory_nfkb",
            "target_hif_nampt_metabolic",
            "source_inflammatory_nfkb",
            "source_hif_nampt_metabolic",
        ],
        False,
    ),
    (
        "M4_ifn_hla_extension",
        [
            "case_indicator",
            "target_inflammatory_nfkb",
            "target_hif_nampt_metabolic",
            "source_inflammatory_nfkb",
            "source_hif_nampt_metabolic",
            "target_ifn_apc",
            "source_ifn_apc",
            "target_hla_ii_apc",
            "source_hla_ii_apc",
        ],
        False,
    ),
    (
        "M5_adaptive_wave104_like",
        [
            "case_indicator",
            "target_inflammatory_nfkb",
            "target_hif_nampt_metabolic",
            "source_inflammatory_nfkb",
            "source_hif_nampt_metabolic",
            "target_ifn_apc",
            "source_ifn_apc",
            "target_hla_ii_apc",
            "source_hla_ii_apc",
            "source_lipid_loader_repair",
            "target_lipid_loader_repair",
            "source_lysosomal_apc",
            "target_lysosomal_apc",
        ],
        True,
    ),
    (
        "M6_target_context_excluding_outcome",
        [
            "case_indicator",
            "target_inflammatory_nfkb",
            "target_hif_nampt_metabolic",
            "source_inflammatory_nfkb",
            "source_hif_nampt_metabolic",
            "target_ifn_apc",
            "source_ifn_apc",
            "target_hla_ii_apc",
            "source_hla_ii_apc",
            "target_lipid_loader_repair",
            "target_lysosomal_apc",
            "source_lipid_loader_repair",
            "source_lysosomal_apc",
        ],
        True,
    ),
]

CORE_MODELS = ["M0_raw", "M1_case", "M2_target_inflammation", "M3_source_target_inflammation"]
ROBUST_MODEL = "M3_source_target_inflammation"
STRICT_MODEL = "M4_ifn_hla_extension"


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def numeric_frame(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    return df[cols].apply(pd.to_numeric, errors="coerce") if cols else pd.DataFrame(index=df.index)


def fixed_covariates(sub: pd.DataFrame, requested: list[str], target_col: str) -> tuple[pd.DataFrame, list[str], str]:
    cols = [col for col in requested if col in sub.columns and col != target_col]
    if not cols:
        return pd.DataFrame(index=sub.index), [], "none"
    cov = numeric_frame(sub, cols)
    complete = np.isfinite(cov.to_numpy(float)).all(axis=1)
    n_complete = int(complete.sum())
    usable = []
    for col in cols:
        vals = pd.to_numeric(sub[col], errors="coerce").to_numpy(float)
        finite = np.isfinite(vals)
        if finite.sum() >= MIN_PAIRS and np.nanstd(vals[finite]) > 1e-8:
            usable.append(col)
    if not usable:
        return pd.DataFrame(index=sub.index), [], "constant_or_missing"
    # Residual-correlation p-values do not account for covariate-selection
    # uncertainty; require a small residual degrees-of-freedom buffer rather
    # than accepting nearly saturated fixed models.
    if n_complete < max(MIN_PAIRS, len(usable) + 5):
        return cov[usable], usable, f"fixed_underpowered_complete_n_{n_complete}_p_{len(usable)}"
    return cov[usable], usable, "fixed"


def perm_pvalue(x: np.ndarray, y: np.ndarray, rng: np.random.Generator, n_perm: int = N_PERM) -> float:
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < MIN_PAIRS:
        return math.nan
    xv = np.asarray(x[mask], dtype=float)
    yv = np.asarray(y[mask], dtype=float)
    if np.nanstd(xv) <= 1e-8 or np.nanstd(yv) <= 1e-8:
        return math.nan
    obs = abs(float(np.corrcoef(xv, yv)[0, 1]))
    ge = 0
    for _ in range(n_perm):
        xp = rng.permutation(xv)
        r = abs(float(np.corrcoef(xp, yv)[0, 1]))
        if r >= obs - 1e-12:
            ge += 1
    return float((ge + 1) / (n_perm + 1))


def fit_model(sub: pd.DataFrame, target_col: str, covariates: pd.DataFrame) -> dict[str, float]:
    x_raw = pd.to_numeric(sub["source_gene_z"], errors="coerce").to_numpy(float)
    y_raw = pd.to_numeric(sub[target_col], errors="coerce").to_numpy(float)
    x_resid, n_x, x_r2 = residualize(x_raw, covariates)
    y_resid, n_y, y_r2 = residualize(y_raw, covariates)
    fit = linreg(x_resid, y_resid)
    fit["x_covariate_r2"] = float(x_r2) if not pd.isna(x_r2) else math.nan
    fit["y_covariate_r2"] = float(y_r2) if not pd.isna(y_r2) else math.nan
    fit["n_x_complete"] = int(n_x)
    fit["n_y_complete"] = int(n_y)
    fit["x_resid"] = x_resid
    fit["y_resid"] = y_resid
    return fit


def loo_stats(sub: pd.DataFrame, target_col: str, requested: list[str], adaptive: bool, rng: np.random.Generator) -> dict[str, float]:
    slopes = []
    ps = []
    valid_indices = list(sub.index)
    for idx in valid_indices:
        loo = sub.drop(index=idx).copy()
        if adaptive:
            cov_cols = [col for col in requested if col in loo.columns and col != target_col]
            cov, _, _ = adaptive_covariates(loo, cov_cols)
        else:
            cov, _, mode = fixed_covariates(loo, requested, target_col)
            if mode.startswith("fixed_underpowered"):
                slopes.append(math.nan)
                ps.append(math.nan)
                continue
        fit = fit_model(loo, target_col, cov)
        slopes.append(float(fit["slope"]) if not pd.isna(fit["slope"]) else math.nan)
        ps.append(float(fit["p"]) if not pd.isna(fit["p"]) else math.nan)
    arr = np.asarray(slopes, dtype=float)
    parr = np.asarray(ps, dtype=float)
    finite = np.isfinite(arr)
    if finite.sum() == 0:
        return {
            "loo_n": 0,
            "loo_positive_fraction": math.nan,
            "loo_min_slope": math.nan,
            "loo_max_slope": math.nan,
            "loo_median_p": math.nan,
        }
    return {
        "loo_n": int(finite.sum()),
        "loo_positive_fraction": float((arr[finite] > 0).mean()),
        "loo_min_slope": float(np.nanmin(arr[finite])),
        "loo_max_slope": float(np.nanmax(arr[finite])),
        "loo_median_p": float(np.nanmedian(parr[np.isfinite(parr)])) if np.isfinite(parr).any() else math.nan,
    }


def run_grid(pairs: pd.DataFrame) -> pd.DataFrame:
    if pairs.empty:
        return pd.DataFrame()
    rng = np.random.default_rng(SEED)
    rows: list[dict[str, Any]] = []
    pairs = pairs[pairs["gene"].eq(GENE)].copy()
    if pairs.empty:
        return pd.DataFrame()
    pairs["case_indicator"] = pairs["group"].eq("case").astype(float)
    for (source_analysis, target_analysis), sub0 in pairs.groupby(["source_analysis", "target_analysis"], observed=True):
        sub0 = sub0.copy()
        for module in TARGET_MODULES:
            target_col = f"target_{module}"
            if target_col not in sub0.columns:
                continue
            sub = sub0[np.isfinite(pd.to_numeric(sub0[target_col], errors="coerce"))].copy()
            if len(sub) < MIN_PAIRS:
                continue
            for model_name, requested, adaptive in MODEL_SPECS:
                requested_effective = [col for col in requested if col != target_col]
                if adaptive:
                    cov_cols = [col for col in requested_effective if col in sub.columns]
                    cov, selected, mode = adaptive_covariates(sub, cov_cols)
                else:
                    cov, selected, mode = fixed_covariates(sub, requested_effective, target_col)
                if mode.startswith("fixed_underpowered"):
                    first = sub.iloc[0]
                    rows.append(
                        {
                            "gene": GENE,
                            "source_analysis": source_analysis,
                            "target_analysis": target_analysis,
                            "disease_name": first["disease_name"],
                            "dataset_path": first["dataset_path"],
                            "source_compartment": first["source_compartment"],
                            "target_compartment": first["target_compartment"],
                            "target_module": module,
                            "model": model_name,
                            "covariate_mode": mode,
                            "covariates": ";".join(selected),
                            "covariate_count": int(len(selected)),
                            "n": 0,
                            "slope": math.nan,
                            "r": math.nan,
                            "p": math.nan,
                            "perm_p": math.nan,
                            "spearman_rho": math.nan,
                            "spearman_p": math.nan,
                            "x_covariate_r2": math.nan,
                            "y_covariate_r2": math.nan,
                            "n_x_complete": int(np.isfinite(cov.to_numpy(float)).all(axis=1).sum()) if not cov.empty else len(sub),
                            "n_y_complete": int(np.isfinite(cov.to_numpy(float)).all(axis=1).sum()) if not cov.empty else len(sub),
                            "loo_n": 0,
                            "loo_positive_fraction": math.nan,
                            "loo_min_slope": math.nan,
                            "loo_max_slope": math.nan,
                            "loo_median_p": math.nan,
                        }
                    )
                    continue
                fit = fit_model(sub, target_col, cov)
                perm = perm_pvalue(np.asarray(fit.pop("x_resid"), dtype=float), np.asarray(fit.pop("y_resid"), dtype=float), rng)
                loo = loo_stats(sub, target_col, requested_effective, adaptive, rng)
                first = sub.iloc[0]
                rows.append(
                    {
                        "gene": GENE,
                        "source_analysis": source_analysis,
                        "target_analysis": target_analysis,
                        "disease_name": first["disease_name"],
                        "dataset_path": first["dataset_path"],
                        "source_compartment": first["source_compartment"],
                        "target_compartment": first["target_compartment"],
                        "target_module": module,
                        "model": model_name,
                        "covariate_mode": mode,
                        "covariates": ";".join(selected),
                        "covariate_count": int(len(selected)),
                        "n": int(fit["n"]),
                        "slope": fit["slope"],
                        "r": fit["r"],
                        "r2": fit["r2"],
                        "p": fit["p"],
                        "perm_p": perm,
                        "spearman_rho": fit["spearman_rho"],
                        "spearman_p": fit["spearman_p"],
                        "x_covariate_r2": fit["x_covariate_r2"],
                        "y_covariate_r2": fit["y_covariate_r2"],
                        "n_x_complete": fit["n_x_complete"],
                        "n_y_complete": fit["n_y_complete"],
                        **loo,
                    }
                )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["nominal_positive"] = (out["slope"] > 0) & (out["p"] < 0.05) & (out["n"] >= MIN_PAIRS)
        out["nominal_negative"] = (out["slope"] < 0) & (out["p"] < 0.05) & (out["n"] >= MIN_PAIRS)
        out["perm_positive"] = out["nominal_positive"] & (out["perm_p"] < 0.05)
        out = out.sort_values(["perm_positive", "p", "perm_p"], ascending=[False, True, True])
    return out


def summarize_tests(grid: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if grid.empty:
        return pd.DataFrame(), pd.DataFrame()
    key_cols = ["source_analysis", "target_analysis", "disease_name", "target_module"]
    rows = []
    robust_rows = []
    for key, sub in grid.groupby(key_cols, observed=True):
        source_analysis, target_analysis, disease_name, target_module = key
        by_model = {r["model"]: r for _, r in sub.iterrows()}
        core = [by_model[m] for m in CORE_MODELS if m in by_model and not pd.isna(by_model[m]["slope"])]
        m3 = by_model.get(ROBUST_MODEL)
        m4 = by_model.get(STRICT_MODEL)
        positive_core = bool(core) and all(float(r["slope"]) > 0 for r in core)
        no_core_negative_nominal = not any((float(r["slope"]) < 0 and float(r["p"]) < 0.05) for r in core if not pd.isna(r["p"]))
        m3_positive_perm = (
            m3 is not None
            and not pd.isna(m3["slope"])
            and float(m3["slope"]) > 0
            and float(m3["p"]) < 0.05
            and float(m3["perm_p"]) < 0.05
            and float(m3["loo_positive_fraction"]) >= 0.85
        )
        m4_supportive = (
            m4 is not None
            and (
                pd.isna(m4["slope"])
                or (float(m4["slope"]) > 0 and (pd.isna(m4["p"]) or float(m4["p"]) < 0.20))
                or str(m4["covariate_mode"]).startswith("fixed_underpowered")
            )
        )
        robust = positive_core and no_core_negative_nominal and m3_positive_perm and m4_supportive
        m3_negative = (
            m3 is not None
            and not pd.isna(m3["slope"])
            and float(m3["slope"]) < 0
            and float(m3["p"]) < 0.05
            and (pd.isna(m3["perm_p"]) or float(m3["perm_p"]) < 0.10)
        )
        row = {
            "gene": GENE,
            "source_analysis": source_analysis,
            "target_analysis": target_analysis,
            "disease_name": disease_name,
            "target_module": target_module,
            "positive_core_models": positive_core,
            "no_core_negative_nominal": no_core_negative_nominal,
            "m3_positive_perm_loo": m3_positive_perm,
            "m4_supportive": m4_supportive,
            "robust_positive": robust,
            "robust_negative": m3_negative,
            "m3_slope": float(m3["slope"]) if m3 is not None and not pd.isna(m3["slope"]) else math.nan,
            "m3_p": float(m3["p"]) if m3 is not None and not pd.isna(m3["p"]) else math.nan,
            "m3_perm_p": float(m3["perm_p"]) if m3 is not None and not pd.isna(m3["perm_p"]) else math.nan,
            "m3_loo_positive_fraction": (
                float(m3["loo_positive_fraction"])
                if m3 is not None and not pd.isna(m3["loo_positive_fraction"])
                else math.nan
            ),
            "m4_slope": float(m4["slope"]) if m4 is not None and not pd.isna(m4["slope"]) else math.nan,
            "m4_p": float(m4["p"]) if m4 is not None and not pd.isna(m4["p"]) else math.nan,
            "model_signs": ";".join(
                f"{r['model']}:{'+' if r['slope'] > 0 else '-' if r['slope'] < 0 else 'NA'}"
                for _, r in sub.sort_values("model").iterrows()
                if not pd.isna(r["slope"])
            ),
        }
        rows.append(row)
        if robust or m3_negative:
            robust_rows.append(row)
    all_summary = pd.DataFrame(rows).sort_values(
        ["robust_positive", "m3_p", "m3_perm_p"], ascending=[False, True, True]
    )
    robust = pd.DataFrame(robust_rows)
    if not robust.empty:
        robust = robust.sort_values(["robust_positive", "m3_p"], ascending=[False, True])
    return all_summary, robust


def write_report(grid: pd.DataFrame, summary: pd.DataFrame, robust: pd.DataFrame, payload: dict[str, Any]) -> None:
    summary_cols = [
        "source_analysis",
        "target_analysis",
        "disease_name",
        "target_module",
        "robust_positive",
        "robust_negative",
        "m3_slope",
        "m3_p",
        "m3_perm_p",
        "m3_loo_positive_fraction",
        "m4_slope",
        "m4_p",
        "model_signs",
    ]
    grid_cols = [
        "source_analysis",
        "target_analysis",
        "disease_name",
        "target_module",
        "model",
        "covariate_mode",
        "covariate_count",
        "n",
        "slope",
        "p",
        "perm_p",
        "loo_positive_fraction",
        "covariates",
    ]
    report = f"""# Wave105 CD82 Niche Robustness Audit

## Bottom Line

Branch call: `{payload["branch_call"]}`.

This audit stress-tests the Wave104 CD82 matched-niche signal with a fixed
covariate model grid, empirical permutation p-values (`{N_PERM}` permutations),
and leave-one-donor-out sign stability. Direct CD82 therapeutic promotion is
already blocked by sidecar prior art; the only question here is whether CD82
remains useful as a tissue-niche mechanism/biomarker branch.

## Robustness Summary

{markdown_table(summary[summary_cols], max_rows=30) if not summary.empty else "_No CD82 tests available._"}

## Robust Or Direction-Conflict Tests

{markdown_table(robust[summary_cols], max_rows=30) if not robust.empty else "_No robust positive or robust negative tests._"}

## Model Grid

{markdown_table(grid[grid_cols].head(80), max_rows=80) if not grid.empty else "_No model-grid rows._"}

## Decision Rule

`REOPEN_CD82_ROBUST_NICHE_SIGNAL` requires robust positive CD82 niche coupling
in at least two diseases with no robust negative disease. A robust positive
requires positive signs through M0-M3, M3 nominal p < 0.05, M3 permutation
p < 0.05, M3 leave-one-out positive fraction >= 0.85, and supportive or
underpowered M4 behavior.

## Interpretation Guardrail

Even a robust matched-niche correlation is not causal. It can reflect shared
tissue severity, therapy, donor composition, or unmeasured batch. Given CD82
prior art in colitis/NLRP3 and RA synovial fibroblasts, a positive result would
support a biomarker/mechanism branch, not a therapeutic target claim.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave105_cd82_niche_robustness_audit.py")}`
- Input pairs: `{rel(PAIRS)}`
- Model grid: `{rel(OUT / "cd82_model_grid_tests.tsv")}`
- Robustness summary: `{rel(OUT / "cd82_robustness_summary.tsv")}`
- Robust tests: `{rel(OUT / "cd82_robust_tests.tsv")}`
- Seed: `{SEED}`
- Permutations per model: `{N_PERM}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pairs = read_tsv(PAIRS)
    grid = run_grid(pairs)
    summary, robust = summarize_tests(grid)
    grid.to_csv(OUT / "cd82_model_grid_tests.tsv", sep="\t", index=False)
    summary.to_csv(OUT / "cd82_robustness_summary.tsv", sep="\t", index=False)
    robust.to_csv(OUT / "cd82_robust_tests.tsv", sep="\t", index=False)

    robust_pos = summary[summary["robust_positive"]] if not summary.empty else pd.DataFrame()
    robust_neg = summary[summary["robust_negative"]] if not summary.empty else pd.DataFrame()
    robust_pos_diseases = int(robust_pos["disease_name"].nunique()) if not robust_pos.empty else 0
    robust_neg_diseases = int(robust_neg["disease_name"].nunique()) if not robust_neg.empty else 0
    branch_call = (
        "REOPEN_CD82_ROBUST_NICHE_SIGNAL"
        if robust_pos_diseases >= 2 and robust_neg_diseases == 0
        else "NO_REOPEN_CD82_AFTER_ROBUSTNESS"
    )
    payload = {
        "random_seed": SEED,
        "n_permutations": N_PERM,
        "gene": GENE,
        "branch_call": branch_call,
        "n_model_grid_rows": int(len(grid)),
        "n_test_contexts": int(len(summary)),
        "robust_positive_test_count": int(len(robust_pos)),
        "robust_positive_disease_count": robust_pos_diseases,
        "robust_negative_test_count": int(len(robust_neg)),
        "robust_negative_disease_count": robust_neg_diseases,
        "robust_positive_contexts": (
            robust_pos[
                ["source_analysis", "target_analysis", "disease_name", "target_module", "m3_slope", "m3_p", "m3_perm_p"]
            ].to_dict(orient="records")
            if not robust_pos.empty
            else []
        ),
        "inputs": {
            "wave104_pairs": rel(PAIRS),
            "wave104_tests": rel(TESTS),
        },
        "guardrail": (
            "This result can only reopen CD82 as a mechanism/biomarker branch; "
            "prior-art sidecars block direct therapeutic CD82 promotion."
        ),
    }
    write_json(OUT / "summary.json", payload)
    write_report(grid, summary, robust, payload)


if __name__ == "__main__":
    main()
