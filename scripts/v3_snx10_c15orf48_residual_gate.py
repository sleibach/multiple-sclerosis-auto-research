#!/usr/bin/env python3
"""Fail-fast residualization gate for post-APOC1 survivor genes.

The unrestricted survivor scan elevated SNX10 and C15ORF48 because they have
nominal MS white-matter trends and recurrent local h5ad expression positives.
That evidence is vulnerable to generic inflammation, stress, tissue injury, and
compartment mismatch. This script builds donor-level selected-gene pseudobulk
scores from the same direct h5ad atlases used in V3, merges the precomputed
same-compartment module scores, and asks whether candidate genes retain a
disease-vs-control signal after residualizing against those modules.

This is a no-go gate. Passing it does not prove causality or druggability.
Failing it demotes the candidate for V3 target purposes.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse, stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_osmr_complement_axes import CONFIGS, DirectConfig, ROOT

SEED = 20260526
RESULTS = ROOT / "phases/v3/results"
OUT = RESULTS / "snx10_c15orf48_residual_gate"

MIN_DONOR_CELLS = 10
MIN_RAW_DELTA = 0.20

PRIMARY_GENES = ["SNX10", "C15ORF48"]

SENTINEL_GENES = [
    "SDC4",
    "CD300A",
    "CD300E",
    "CD300F",
    "CD300LF",
    "PIKFYVE",
    "TFEB",
    "TFE3",
    "PPARG",
    "NR1H3",
    "CXCL9",
    "BIRC3",
    "DAP",
    "IL2RG",
    "LIPA",
    "CTSS",
    "CTSB",
    "CTSL",
    "IFI30",
    "APOC1",
    "CHI3L1",
    "TYK2",
    "JAK1",
    "JAK2",
    "STAT1",
    "IRF1",
    "FABP5",
    "MSR1",
    "SCARB2",
    "LAMP3",
    "LGALS3",
    "TYROBP",
    "TREM2",
    "MERTK",
]

TARGET_GENES = sorted(set(PRIMARY_GENES + SENTINEL_GENES))

COVARIATE_MODULES = [
    "ifn_apc",
    "inflammatory_nfkb",
    "hif_nampt_metabolic",
    "hla_ii_apc",
    "lysosomal_apc",
    "lipid_loader_repair",
    "c1q_phagocytic_myeloid",
    "complement_effector",
    "complement_phagocytosis",
    "mif_cd74_receptor_state",
    "mixscale_validated_ifng_readout",
]

CORE_COVARIATES = [
    "ifn_apc",
    "inflammatory_nfkb",
    "hif_nampt_metabolic",
    "lysosomal_apc",
    "lipid_loader_repair",
]

MULTIVARIABLE_COVARIATE_SETS = {
    "core_inflammation_stress": ["ifn_apc", "inflammatory_nfkb", "hif_nampt_metabolic"],
    "core_lysosomal_lipid": ["lysosomal_apc", "lipid_loader_repair"],
    "core_all": CORE_COVARIATES,
}


def hedges_g(case: np.ndarray, control: np.ndarray) -> float:
    case = np.asarray(case, dtype=float)
    control = np.asarray(control, dtype=float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if len(case) < 2 or len(control) < 2:
        return np.nan
    pooled = ((len(case) - 1) * case.var(ddof=1) + (len(control) - 1) * control.var(ddof=1)) / (
        len(case) + len(control) - 2
    )
    if pooled <= 0:
        return np.nan
    correction = 1.0 - (3.0 / (4.0 * (len(case) + len(control)) - 9.0))
    return float(((case.mean() - control.mean()) / math.sqrt(pooled)) * correction)


def contrast(values: pd.Series, groups: pd.Series) -> dict[str, float]:
    case = values.loc[groups == "case"].astype(float).to_numpy()
    control = values.loc[groups == "control"].astype(float).to_numpy()
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
    t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
    return {
        "n_case": int(len(case)),
        "n_control": int(len(control)),
        "mean_case": float(np.mean(case)),
        "mean_control": float(np.mean(control)),
        "delta_case_minus_control": float(np.mean(case) - np.mean(control)),
        "hedges_g": float(hedges_g(case, control)),
        "welch_t": float(t_stat),
        "p": float(p_value),
    }


def residualize_univariate(y: np.ndarray, x: np.ndarray) -> tuple[np.ndarray, float, float]:
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    mask = np.isfinite(y) & np.isfinite(x)
    residuals = np.full(len(y), np.nan)
    if mask.sum() < 4 or np.nanstd(x[mask]) <= 0:
        return residuals, np.nan, np.nan
    slope, intercept, r_value, _, _ = stats.linregress(x[mask], y[mask])
    residuals[mask] = y[mask] - (intercept + slope * x[mask])
    return residuals, float(slope), float(r_value**2)


def residualize_multivariable(y: np.ndarray, x_df: pd.DataFrame) -> tuple[np.ndarray, int, float]:
    y = np.asarray(y, dtype=float)
    x = x_df.astype(float).to_numpy()
    mask = np.isfinite(y) & np.all(np.isfinite(x), axis=1)
    residuals = np.full(len(y), np.nan)
    p = x.shape[1]
    if mask.sum() < max(6, p + 4):
        return residuals, int(mask.sum()), np.nan
    x_mask = x[mask]
    if np.any(np.nanstd(x_mask, axis=0) <= 0):
        return residuals, int(mask.sum()), np.nan
    design = np.column_stack([np.ones(mask.sum()), x_mask])
    beta, *_ = np.linalg.lstsq(design, y[mask], rcond=None)
    fitted = design @ beta
    resid = y[mask] - fitted
    ss_res = float(np.sum(resid**2))
    ss_tot = float(np.sum((y[mask] - np.mean(y[mask])) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
    residuals[mask] = resid
    return residuals, int(mask.sum()), float(r2)


def gene_symbols_for_config(a, config: DirectConfig) -> list[str]:
    if config.gene_symbol_column in a.var.columns:
        raw = a.var[config.gene_symbol_column].astype(str).tolist()
    elif "feature_name" in a.var.columns:
        raw = a.var["feature_name"].astype(str).tolist()
    else:
        raw = list(map(str, a.var_names))
    return [value.strip().upper() for value in raw]


def selected_gene_columns(a, config: DirectConfig) -> dict[str, list[int]]:
    mapping: dict[str, list[int]] = {gene: [] for gene in TARGET_GENES}
    for idx, symbol in enumerate(gene_symbols_for_config(a, config)):
        if symbol in mapping:
            mapping[symbol].append(idx)
    return {gene: idxs for gene, idxs in mapping.items() if idxs}


def aggregate_config(config: DirectConfig, a, x) -> tuple[pd.DataFrame, pd.DataFrame]:
    obs = a.obs.copy()
    mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
    obs_sub = obs.loc[mask].copy()
    cell_idx = np.flatnonzero(mask.to_numpy())
    gene_to_cols = selected_gene_columns(a, config)
    if obs_sub.empty or not gene_to_cols:
        raise ValueError(f"no cells or selected genes for {config.name}")

    lib_size = np.asarray(x[cell_idx].sum(axis=1)).ravel().astype(float)
    lib_size[~np.isfinite(lib_size) | (lib_size <= 0)] = np.nan
    present_genes = sorted(gene_to_cols)

    expr_by_gene: list[np.ndarray] = []
    for gene in present_genes:
        sub_x = x[cell_idx][:, gene_to_cols[gene]]
        summed = np.asarray(sub_x.sum(axis=1)).ravel().astype(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            log_norm = np.log1p((summed / lib_size) * 1e4)
        expr_by_gene.append(log_norm)
    log_expr = np.column_stack(expr_by_gene)

    control_mask = obs_sub["disease"].eq(config.control_label).to_numpy()
    control_mean = np.nanmean(log_expr[control_mask], axis=0)
    control_sd = np.nanstd(log_expr[control_mask], axis=0, ddof=1)
    control_sd[~np.isfinite(control_sd) | (control_sd < 1e-6)] = 1.0
    z_expr = (log_expr - control_mean) / control_sd

    cell_scores = obs_sub[["donor_id", "disease", "cell_type"]].reset_index(drop=True).copy()
    cell_scores["group"] = np.where(cell_scores["disease"].eq(config.disease_label), "case", "control")

    rows: list[dict[str, object]] = []
    for (donor, disease), sub_idx in cell_scores.groupby(["donor_id", "disease"], observed=True).groups.items():
        idx = np.fromiter(sub_idx, dtype=int)
        if len(idx) < MIN_DONOR_CELLS:
            continue
        group = "case" if disease == config.disease_label else "control"
        base = {
            "analysis": config.name,
            "dataset_path": str(config.path.relative_to(ROOT)),
            "disease_name": config.disease_label,
            "compartment": config.compartment,
            "role": config.role,
            "donor_id": donor,
            "disease": disease,
            "group": group,
            "n_cells": int(len(idx)),
            "cell_types": ",".join(sorted(cell_scores.iloc[idx]["cell_type"].astype(str).unique())),
        }
        for j, gene in enumerate(present_genes):
            vals = log_expr[idx, j]
            zvals = z_expr[idx, j]
            rows.append(
                {
                    **base,
                    "gene": gene,
                    "mean_log_norm": float(np.nanmean(vals)),
                    "mean_z_vs_controls": float(np.nanmean(zvals)),
                    "detection_fraction": float(np.mean(vals > 0)),
                }
            )

    presence = pd.DataFrame(
        [
            {
                "analysis": config.name,
                "disease_name": config.disease_label,
                "compartment": config.compartment,
                "gene": gene,
                "n_feature_columns": len(idxs),
            }
            for gene, idxs in sorted(gene_to_cols.items())
        ]
    )
    return pd.DataFrame(rows), presence


def add_fdr(df: pd.DataFrame, p_col: str, out_col: str) -> pd.DataFrame:
    df[out_col] = np.nan
    mask = df[p_col].notna()
    if mask.any():
        df.loc[mask, out_col] = multipletests(df.loc[mask, p_col].fillna(1.0), method="fdr_bh")[1]
    return df


def load_module_wide() -> pd.DataFrame:
    module_tables: list[pd.DataFrame] = []
    specs = [
        (
            RESULTS / "osmr_complement_axes" / "osmr_complement_donor_module_scores.tsv",
            "osmr_complement_axes",
        ),
        (
            RESULTS / "direct_h5ad_cell_state" / "direct_h5ad_donor_module_scores.tsv",
            "direct_h5ad_cell_state",
        ),
    ]
    for path, source in specs:
        if not path.exists():
            continue
        table = pd.read_csv(path, sep="\t")
        table = table.loc[table["module"].isin(COVARIATE_MODULES)].copy()
        if table.empty:
            continue
        table["module_source"] = source
        module_tables.append(table)
    if not module_tables:
        return pd.DataFrame(columns=["analysis", "donor_id", *COVARIATE_MODULES])
    module_scores = pd.concat(module_tables, ignore_index=True)
    source_priority = {"osmr_complement_axes": 0, "direct_h5ad_cell_state": 1}
    module_scores["source_priority"] = module_scores["module_source"].map(source_priority).fillna(9)
    module_scores = (
        module_scores.sort_values(["analysis", "donor_id", "module", "source_priority"])
        .drop_duplicates(["analysis", "donor_id", "module"], keep="first")
        .copy()
    )
    wide = module_scores.pivot_table(
        index=["analysis", "donor_id"],
        columns="module",
        values="mean_score",
        aggfunc="mean",
    ).reset_index()
    meta_cols = [
        col
        for col in ["analysis", "donor_id", "disease_name", "compartment", "role", "group"]
        if col in module_scores.columns
    ]
    meta = module_scores.drop_duplicates(["analysis", "donor_id"])[meta_cols]
    return meta.merge(wide, on=["analysis", "donor_id"], how="left")


def run_raw_tests(gene_scores: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (analysis, gene), sub in gene_scores.groupby(["analysis", "gene"], observed=True):
        for metric in ["mean_z_vs_controls", "detection_fraction"]:
            stats_row = contrast(sub[metric], sub["group"])
            first = sub.iloc[0]
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "gene": gene,
                    "metric": metric,
                    **stats_row,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out = add_fdr(out, "p", "fdr")
        out["positive_nominal"] = (out["delta_case_minus_control"] >= MIN_RAW_DELTA) & (out["p"] < 0.05)
        out["negative_nominal"] = (out["delta_case_minus_control"] <= -MIN_RAW_DELTA) & (out["p"] < 0.05)
    return out


def run_residual_tests(gene_scores: pd.DataFrame, module_wide: pd.DataFrame) -> pd.DataFrame:
    covariates = module_wide[["analysis", "donor_id", *COVARIATE_MODULES]]
    merged = gene_scores.merge(covariates, on=["analysis", "donor_id"], how="left")
    rows: list[dict[str, object]] = []
    for (analysis, gene), sub in merged.groupby(["analysis", "gene"], observed=True):
        sub = sub.copy()
        raw = contrast(sub["mean_z_vs_controls"], sub["group"])
        first = sub.iloc[0]
        for covariate in COVARIATE_MODULES:
            if covariate not in sub:
                continue
            residuals, slope, r2 = residualize_univariate(
                sub["mean_z_vs_controls"].to_numpy(float),
                sub[covariate].to_numpy(float),
            )
            residual = contrast(pd.Series(residuals, index=sub.index), sub["group"])
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "gene": gene,
                    "residual_model": "univariate",
                    "covariate_set": covariate,
                    "covariate_count": 1,
                    "n_complete_for_model": int(np.isfinite(sub[covariate].to_numpy(float)).sum()),
                    "covariate_slope": slope,
                    "covariate_r2": r2,
                    **{f"raw_{k}": v for k, v in raw.items()},
                    **{f"residual_{k}": v for k, v in residual.items()},
                }
            )
        for label, covariate_set in MULTIVARIABLE_COVARIATE_SETS.items():
            present = [cov for cov in covariate_set if cov in sub.columns]
            if len(present) != len(covariate_set):
                continue
            residuals, n_complete, r2 = residualize_multivariable(
                sub["mean_z_vs_controls"].to_numpy(float),
                sub[present],
            )
            residual = contrast(pd.Series(residuals, index=sub.index), sub["group"])
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "gene": gene,
                    "residual_model": "multivariable",
                    "covariate_set": label,
                    "covariate_count": len(present),
                    "n_complete_for_model": n_complete,
                    "covariate_slope": np.nan,
                    "covariate_r2": r2,
                    **{f"raw_{k}": v for k, v in raw.items()},
                    **{f"residual_{k}": v for k, v in residual.items()},
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out = add_fdr(out, "residual_p", "residual_fdr")
        out["retains_nominal_positive"] = (
            (out["raw_delta_case_minus_control"] >= MIN_RAW_DELTA)
            & (out["raw_p"] < 0.05)
            & (out["residual_delta_case_minus_control"] >= MIN_RAW_DELTA)
            & (out["residual_p"] < 0.05)
        )
        out["retains_direction_only"] = (
            (out["raw_delta_case_minus_control"] >= MIN_RAW_DELTA)
            & (out["raw_p"] < 0.05)
            & (out["residual_delta_case_minus_control"] > 0)
        )
    return out


def summarize_gate(raw_tests: pd.DataFrame, residual_tests: pd.DataFrame, presence: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    raw_gene = raw_tests.loc[raw_tests["metric"] == "mean_z_vs_controls"].copy()
    for gene in TARGET_GENES:
        raw_sub = raw_gene.loc[raw_gene["gene"] == gene]
        resid_sub = residual_tests.loc[residual_tests["gene"] == gene]
        raw_pos = raw_sub.loc[raw_sub["positive_nominal"]]
        raw_neg = raw_sub.loc[raw_sub["negative_nominal"]]
        retained = resid_sub.loc[resid_sub["retains_nominal_positive"]]
        retained_uni = retained.loc[retained["residual_model"] == "univariate"]
        retained_multi = retained.loc[retained["residual_model"] == "multivariable"]

        core_uni = resid_sub.loc[
            resid_sub["residual_model"].eq("univariate") & resid_sub["covariate_set"].isin(CORE_COVARIATES)
        ]
        strict_core_analyses: list[str] = []
        for analysis, sub in core_uni.groupby("analysis", observed=True):
            if len(sub) == len(CORE_COVARIATES) and bool(sub["retains_nominal_positive"].all()):
                strict_core_analyses.append(str(analysis))

        non_ibd_retained = retained.loc[
            ~retained["disease_name"].astype(str).isin(["Crohn disease", "ulcerative colitis"])
        ]
        present_analyses = presence.loc[presence["gene"] == gene, "analysis"].nunique()
        rows.append(
            {
                "gene": gene,
                "primary_gene": gene in PRIMARY_GENES,
                "present_analysis_count": int(present_analyses),
                "raw_positive_analysis_count": int(raw_pos["analysis"].nunique()),
                "raw_positive_disease_count": int(raw_pos["disease_name"].nunique()),
                "raw_negative_analysis_count": int(raw_neg["analysis"].nunique()),
                "raw_positive_analyses": ";".join(
                    raw_pos.sort_values(["p", "delta_case_minus_control"], ascending=[True, False])
                    .apply(lambda r: f"{r['analysis']}:{r['delta_case_minus_control']:.3g},p={r['p']:.2g}", axis=1)
                    .tolist()
                ),
                "retained_positive_test_count": int(len(retained)),
                "retained_univariate_positive_test_count": int(len(retained_uni)),
                "retained_multivariable_positive_test_count": int(len(retained_multi)),
                "retained_positive_analysis_count": int(retained["analysis"].nunique()),
                "retained_positive_disease_count": int(retained["disease_name"].nunique()),
                "non_ibd_retained_positive_analysis_count": int(non_ibd_retained["analysis"].nunique()),
                "non_ibd_retained_positive_disease_count": int(non_ibd_retained["disease_name"].nunique()),
                "strict_core_covariate_surviving_analysis_count": len(strict_core_analyses),
                "strict_core_covariate_surviving_analyses": ";".join(sorted(strict_core_analyses)),
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
    out = pd.DataFrame(rows).sort_values(
        [
            "primary_gene",
            "strict_core_covariate_surviving_analysis_count",
            "non_ibd_retained_positive_disease_count",
            "retained_positive_disease_count",
            "raw_positive_disease_count",
        ],
        ascending=[False, False, False, False, False],
    )
    return out


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    cache: dict[Path, tuple] = {}
    gene_score_tables: list[pd.DataFrame] = []
    presence_tables: list[pd.DataFrame] = []
    run_log: list[dict[str, object]] = []
    for config in CONFIGS:
        try:
            print(f"[residual-gate] starting {config.name}", flush=True)
            if config.path not in cache:
                a = ad.read_h5ad(config.path)
                x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
                cache[config.path] = (a, x)
            a, x = cache[config.path]
            scores, presence = aggregate_config(config, a, x)
            gene_score_tables.append(scores)
            presence_tables.append(presence)
            run_log.append(
                {
                    "analysis": config.name,
                    "status": "completed",
                    "n_donor_gene_rows": int(len(scores)),
                    "n_present_target_genes": int(presence["gene"].nunique()),
                }
            )
            print(
                f"[residual-gate] completed {config.name}: "
                f"{len(scores)} donor-gene rows, {presence['gene'].nunique()} genes",
                flush=True,
            )
        except Exception as exc:
            run_log.append(
                {
                    "analysis": config.name,
                    "status": "failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            print(f"[residual-gate] failed {config.name}: {type(exc).__name__}: {exc}", flush=True)

    gene_scores = pd.concat(gene_score_tables, ignore_index=True) if gene_score_tables else pd.DataFrame()
    presence = pd.concat(presence_tables, ignore_index=True) if presence_tables else pd.DataFrame()
    gene_scores.to_csv(OUT / "selected_gene_donor_scores.tsv", sep="\t", index=False)
    presence.to_csv(OUT / "selected_gene_presence.tsv", sep="\t", index=False)

    if gene_scores.empty:
        summary = {
            "random_seed": SEED,
            "status": "failed",
            "run_log": run_log,
            "reason": "No donor-level selected-gene scores were generated.",
        }
        (OUT / "snx10_c15orf48_residual_gate_summary.json").write_text(
            json.dumps(summary, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(summary, indent=2))
        return

    module_wide = load_module_wide()
    raw_tests = run_raw_tests(gene_scores)
    residuals = run_residual_tests(gene_scores, module_wide)
    gate = summarize_gate(raw_tests, residuals, presence)

    raw_tests.to_csv(OUT / "selected_gene_raw_tests.tsv", sep="\t", index=False)
    residuals.to_csv(OUT / "selected_gene_residual_tests.tsv", sep="\t", index=False)
    gate.to_csv(OUT / "snx10_c15orf48_residual_gate.tsv", sep="\t", index=False)

    primary_gate = gate.loc[gate["gene"].isin(PRIMARY_GENES)].copy()
    summary = {
        "random_seed": SEED,
        "run_log": run_log,
        "primary_genes": PRIMARY_GENES,
        "covariate_modules": COVARIATE_MODULES,
        "core_covariates": CORE_COVARIATES,
        "strict_gate_definition": (
            "A strict core survivor is raw-positive and remains nominally positive "
            "after separate residualization against every core covariate module in "
            "the same analysis. Passing is only a fail-fast survival criterion, not "
            "a causality, novelty, or druggability claim."
        ),
        "primary_gate": primary_gate.to_dict(orient="records"),
        "top_gate_rows": gate.head(20).to_dict(orient="records"),
        "guardrail": (
            "Donor-level residualization uses available module scores and cannot "
            "fully remove severity, medication, batch, sampling, non-autoimmune "
            "inflammation, or cross-tissue compartment mismatch."
        ),
    }
    (OUT / "snx10_c15orf48_residual_gate_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
