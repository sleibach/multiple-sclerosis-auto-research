#!/usr/bin/env python3
"""Wave 5 local quantification of OSM/OSMR and C1q/complement axes.

This script intentionally writes a separate output directory and does not
modify the standing direct-h5ad or GSE111972 result tables. It scores two
candidate axis families plus same-sample covariates at donor/sample level,
then retests case-control contrasts after one-at-a-time residual controls.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse, stats
from statsmodels.stats.multitest import multipletests

import v3_analyze_direct_h5ad_cell_states as direct
import v3_analyze_gse111972_microglia as gse111972

SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave5_local_quant"


@dataclass(frozen=True)
class ModuleSpec:
    axis_family: str
    genes: tuple[str, ...]
    plausible_compartment_terms: tuple[str, ...]
    note: str


AXIS_MODULES: dict[str, ModuleSpec] = {
    "osm_ligand_inflammatory": ModuleSpec(
        axis_family="OSM_OSMR",
        genes=("OSM", "IL1B", "TNF", "CSF2", "CCL2", "CXCL8", "NFKBIA"),
        plausible_compartment_terms=("myeloid", "apc", "macrophage", "monocyte", "microglia"),
        note="OSM ligand-bearing inflammatory myeloid-like donor state; residual NF-kB control is essential because this is intentionally inflammatory.",
    ),
    "osmr_receptor_response": ModuleSpec(
        axis_family="OSM_OSMR",
        genes=("OSMR", "IL6ST", "STAT3", "SOCS3", "JUNB", "FOS", "CXCL1", "CXCL2", "CXCL8", "CCL2", "SERPINE1", "SOD2"),
        plausible_compartment_terms=("epithelial", "keratinocyte", "acinar", "ductal", "salivary", "skin", "colon"),
        note="OSMR/IL6ST receptor-response state in tissue target cells; OSM itself need not be expressed in the same compartment.",
    ),
    "osm_osmr_core": ModuleSpec(
        axis_family="OSM_OSMR",
        genes=("OSM", "OSMR", "IL6ST", "LIFR", "STAT3", "SOCS3"),
        plausible_compartment_terms=("myeloid", "apc", "microglia", "epithelial", "keratinocyte", "acinar", "ductal", "salivary", "skin", "colon"),
        note="Compact OSM ligand/receptor/signaling core; biologically weaker than split ligand and receptor modules but useful as a sanity check.",
    ),
    "c1q_core": ModuleSpec(
        axis_family="C1Q_COMPLEMENT",
        genes=("C1QA", "C1QB", "C1QC"),
        plausible_compartment_terms=("myeloid", "apc", "macrophage", "monocyte", "microglia"),
        note="Canonical C1q-producing myeloid/microglial core.",
    ),
    "c1q_phagolysosomal": ModuleSpec(
        axis_family="C1Q_COMPLEMENT",
        genes=("C1QA", "C1QB", "C1QC", "C3", "C3AR1", "C5AR1", "TYROBP", "TREM2", "APOE", "CD68", "CSF1R", "CX3CR1"),
        plausible_compartment_terms=("myeloid", "apc", "macrophage", "monocyte", "microglia"),
        note="C1q-complement phagolysosomal myeloid state, separated from lipid-loader and lysosomal-APC covariates downstream.",
    ),
}

COVARIATE_MODULES: dict[str, tuple[str, ...]] = {
    "ifn_apc": ("STAT1", "IRF1", "CXCL10", "GBP1", "CD74", "IFI30", "HLA-DRA", "HLA-DRB1"),
    "inflammatory_nfkb": ("IL1B", "TNF", "CXCL8", "CCL2", "CCL3", "CCL4", "NFKBIA", "TREM1", "OSM"),
    "hif_nampt_metabolic": ("HIF1A", "NAMPT", "LDHA", "SLC2A1", "NFKBIA", "IL1B", "HK2", "PFKFB3"),
    "lipid_loader_repair": ("ACSL1", "APOE", "GPNMB", "LPL", "PLIN2", "CD36", "LIPA", "FABP5", "TREM2", "MSR1", "MERTK", "SPP1"),
    "lysosomal_apc": ("IFI30", "CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"),
}

ALL_MODULES: dict[str, tuple[str, ...]] = {
    **{name: spec.genes for name, spec in AXIS_MODULES.items()},
    **COVARIATE_MODULES,
}
ALL_GENES = sorted({gene for genes in ALL_MODULES.values() for gene in genes})


def hedges_g(case: np.ndarray, control: np.ndarray) -> float:
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
    return ((case.mean() - control.mean()) / math.sqrt(pooled)) * correction


def compare_arrays(case: np.ndarray, control: np.ndarray) -> dict[str, float | int]:
    case = np.asarray(case, dtype=float)
    control = np.asarray(control, dtype=float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if len(case) >= 2 and len(control) >= 2:
        t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
    else:
        t_stat, p_value = np.nan, np.nan
    return {
        "n_case": int(len(case)),
        "n_control": int(len(control)),
        "mean_case": float(np.nanmean(case)) if len(case) else np.nan,
        "mean_control": float(np.nanmean(control)) if len(control) else np.nan,
        "delta_case_minus_control": float(np.nanmean(case) - np.nanmean(control)) if len(case) and len(control) else np.nan,
        "hedges_g": hedges_g(case, control),
        "welch_t": float(t_stat) if np.isfinite(t_stat) else np.nan,
        "p": float(p_value) if np.isfinite(p_value) else np.nan,
    }


def residualize(y: np.ndarray, x: np.ndarray) -> tuple[np.ndarray, float, float]:
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    valid = np.isfinite(y) & np.isfinite(x)
    residuals = np.full(len(y), np.nan)
    if valid.sum() < 4 or np.nanstd(x[valid]) < 1e-8:
        return residuals, np.nan, np.nan
    slope, intercept, r_value, _, _ = stats.linregress(x[valid], y[valid])
    residuals[valid] = y[valid] - (intercept + slope * x[valid])
    return residuals, float(slope), float(r_value**2)


def add_fdr(df: pd.DataFrame, p_col: str, fdr_col: str, group_cols: list[str] | None = None) -> pd.DataFrame:
    out = df.copy()
    out[fdr_col] = np.nan
    if out.empty or p_col not in out.columns:
        return out
    groups = [(None, out.index)] if not group_cols else out.groupby(group_cols, observed=True).groups.items()
    for _, idx in groups:
        pvals = out.loc[idx, p_col].to_numpy(dtype=float)
        valid = np.isfinite(pvals)
        if valid.any():
            adjusted = np.full(pvals.shape, np.nan)
            adjusted[valid] = multipletests(pvals[valid], method="fdr_bh")[1]
            out.loc[idx, fdr_col] = adjusted
    return out


def gene_indices(adata, symbol_column: str) -> dict[str, int]:
    if symbol_column in adata.var.columns:
        symbols = adata.var[symbol_column].astype(str)
    elif "feature_name" in adata.var.columns:
        symbols = adata.var["feature_name"].astype(str)
    else:
        symbols = adata.var_names.astype(str)
    mapping: dict[str, int] = {}
    for idx, symbol in enumerate(symbols):
        if symbol in ALL_GENES and symbol not in mapping:
            mapping[symbol] = idx
    return mapping


def score_modules_from_matrix(z: np.ndarray, present_genes: list[str], normal_mask: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame]:
    gene_to_local = {gene: idx for idx, gene in enumerate(present_genes)}
    scores: dict[str, np.ndarray] = {}
    gene_rows: list[dict[str, object]] = []
    for module, genes in ALL_MODULES.items():
        present = [gene for gene in genes if gene in gene_to_local]
        gene_rows.append({"module": module, "n_genes_present": len(present), "genes_present": ",".join(present)})
        if present:
            values = np.nanmean(z[:, [gene_to_local[gene] for gene in present]], axis=1)
        else:
            values = np.full(z.shape[0], np.nan)
        scores[module] = values
        threshold = np.nanpercentile(values[normal_mask], 75) if np.isfinite(values[normal_mask]).any() else np.nan
        scores[f"{module}_high"] = values > threshold if np.isfinite(threshold) else np.full(z.shape[0], False)
    return pd.DataFrame(scores), pd.DataFrame(gene_rows)


def direct_h5ad_scores() -> tuple[pd.DataFrame, pd.DataFrame]:
    cache: dict[Path, tuple] = {}
    donor_rows: list[dict[str, object]] = []
    module_gene_rows: list[dict[str, object]] = []
    for config in direct.CONFIGS:
        if not config.path.exists():
            module_gene_rows.append({"analysis": config.name, "status": "skipped_missing_file", "path": str(config.path)})
            continue
        if config.path not in cache:
            cache[config.path] = direct.read_counts(config.path)
        adata, x = cache[config.path]
        obs = adata.obs.copy()
        mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
        obs_sub = obs.loc[mask].copy()
        cell_idx = np.flatnonzero(mask.to_numpy())
        mapping = gene_indices(adata, config.gene_symbol_column)
        present_genes = sorted(mapping)
        if obs_sub.empty or not present_genes:
            module_gene_rows.append({"analysis": config.name, "status": "skipped_no_cells_or_genes", "path": str(config.path)})
            continue

        target_x = x[cell_idx][:, [mapping[gene] for gene in present_genes]].astype(float)
        if not sparse.issparse(target_x):
            target_x = sparse.csr_matrix(target_x)
        lib_size = np.asarray(x[cell_idx].sum(axis=1)).ravel().astype(float)
        lib_size[~np.isfinite(lib_size) | (lib_size <= 0)] = np.nan
        normalized = target_x.multiply(
            np.divide(1.0, lib_size, out=np.zeros_like(lib_size), where=np.isfinite(lib_size))[:, None]
        ).multiply(1e4)
        log_expr = np.log1p(normalized.toarray())
        normal_mask = obs_sub["disease"].eq(config.control_label).to_numpy()
        gene_mean = np.nanmean(log_expr[normal_mask], axis=0)
        gene_sd = np.nanstd(log_expr[normal_mask], axis=0, ddof=1)
        gene_sd[~np.isfinite(gene_sd) | (gene_sd < 1e-6)] = 1.0
        z = (log_expr - gene_mean) / gene_sd

        cell_scores, module_genes = score_modules_from_matrix(z, present_genes, normal_mask)
        module_genes.insert(0, "analysis", config.name)
        module_genes["status"] = "completed"
        module_genes["path"] = str(config.path.relative_to(ROOT))
        module_gene_rows.extend(module_genes.to_dict(orient="records"))

        cell_scores = pd.concat(
            [obs_sub[["donor_id", "disease", "cell_type", "tissue"]].reset_index(drop=True), cell_scores],
            axis=1,
        )
        for (donor, disease), sub in cell_scores.groupby(["donor_id", "disease"], observed=True):
            if len(sub) < 10:
                continue
            for module, spec in AXIS_MODULES.items():
                donor_rows.append(
                    {
                        "source": "direct_h5ad",
                        "analysis": config.name,
                        "dataset": str(config.path.relative_to(ROOT)),
                        "disease_name": config.disease_label,
                        "compartment": config.compartment,
                        "unit_id": donor,
                        "group_label": disease,
                        "group": "case" if disease == config.disease_label else "control",
                        "axis_family": spec.axis_family,
                        "module": module,
                        "n_cells": int(len(sub)),
                        "mean_score": float(np.nanmean(sub[module])),
                        "high_fraction": float(sub[f"{module}_high"].mean()),
                        "cell_types": ",".join(sorted(sub["cell_type"].astype(str).unique())),
                    }
                )
            for module in COVARIATE_MODULES:
                donor_rows.append(
                    {
                        "source": "direct_h5ad",
                        "analysis": config.name,
                        "dataset": str(config.path.relative_to(ROOT)),
                        "disease_name": config.disease_label,
                        "compartment": config.compartment,
                        "unit_id": donor,
                        "group_label": disease,
                        "group": "case" if disease == config.disease_label else "control",
                        "axis_family": "COVARIATE",
                        "module": module,
                        "n_cells": int(len(sub)),
                        "mean_score": float(np.nanmean(sub[module])),
                        "high_fraction": float(sub[f"{module}_high"].mean()),
                        "cell_types": ",".join(sorted(sub["cell_type"].astype(str).unique())),
                    }
                )
    return pd.DataFrame(donor_rows), pd.DataFrame(module_gene_rows)


def gse111972_scores() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not gse111972.NORM_PATH.exists() or not gse111972.MATRIX_PATH.exists():
        return pd.DataFrame(), pd.DataFrame([{"analysis": "GSE111972", "status": "skipped_missing_file"}])
    meta = gse111972.load_sample_metadata()
    log_expr = gse111972.load_expression()
    meta = meta.loc[meta["sample"].isin(log_expr.columns)].reset_index(drop=True)
    present_genes = [gene for gene in ALL_GENES if gene in log_expr.index]
    if not present_genes:
        return pd.DataFrame(), pd.DataFrame([{"analysis": "GSE111972", "status": "skipped_no_genes"}])
    z = log_expr.loc[present_genes, meta["sample"]]
    z = z.sub(z.mean(axis=1), axis=0).div(z.std(axis=1).replace(0, np.nan), axis=0)
    sample_scores: dict[str, pd.Series] = {}
    module_gene_rows: list[dict[str, object]] = []
    for module, genes in ALL_MODULES.items():
        present = [gene for gene in genes if gene in z.index]
        module_gene_rows.append(
            {
                "analysis": "GSE111972",
                "status": "completed",
                "path": str(gse111972.NORM_PATH.relative_to(ROOT)),
                "module": module,
                "n_genes_present": len(present),
                "genes_present": ",".join(present),
            }
        )
        sample_scores[module] = z.loc[present].mean(axis=0) if present else pd.Series(np.nan, index=meta["sample"])
    score_df = pd.DataFrame(sample_scores).reset_index(names="sample")
    joined = meta.merge(score_df, left_on="sample", right_on="sample", how="left")
    rows: list[dict[str, object]] = []
    for region_label, region_name in [("white_matter", "white matter microglia"), ("grey_matter", "grey matter microglia"), ("all", "all microglia")]:
        region_meta = joined if region_label == "all" else joined[joined["region"].eq(region_label)]
        if region_meta.empty:
            continue
        for _, r in region_meta.iterrows():
            group = "case" if r["disease"] == "MS" else "control"
            for module, spec in AXIS_MODULES.items():
                rows.append(
                    {
                        "source": "GSE111972",
                        "analysis": f"GSE111972_{region_label}",
                        "dataset": str(gse111972.NORM_PATH.relative_to(ROOT)),
                        "disease_name": "multiple sclerosis",
                        "compartment": region_name,
                        "unit_id": r["sample"],
                        "group_label": r["disease"],
                        "group": group,
                        "axis_family": spec.axis_family,
                        "module": module,
                        "n_cells": np.nan,
                        "mean_score": float(r[module]),
                        "high_fraction": np.nan,
                        "cell_types": "sorted microglia",
                    }
                )
            for module in COVARIATE_MODULES:
                rows.append(
                    {
                        "source": "GSE111972",
                        "analysis": f"GSE111972_{region_label}",
                        "dataset": str(gse111972.NORM_PATH.relative_to(ROOT)),
                        "disease_name": "multiple sclerosis",
                        "compartment": region_name,
                        "unit_id": r["sample"],
                        "group_label": r["disease"],
                        "group": group,
                        "axis_family": "COVARIATE",
                        "module": module,
                        "n_cells": np.nan,
                        "mean_score": float(r[module]),
                        "high_fraction": np.nan,
                        "cell_types": "sorted microglia",
                    }
                )
    return pd.DataFrame(rows), pd.DataFrame(module_gene_rows)


def compartment_plausible(module: str, compartment: str) -> bool:
    terms = AXIS_MODULES[module].plausible_compartment_terms
    text = compartment.lower()
    return any(term in text for term in terms)


def raw_contrasts(scores: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    axes = scores[scores["axis_family"].ne("COVARIATE")].copy()
    for (source, analysis, module, metric), sub in axes.groupby(["source", "analysis", "module", "metric"], observed=True):
        case = sub.loc[sub["group"].eq("case"), "value"].to_numpy(float)
        control = sub.loc[sub["group"].eq("control"), "value"].to_numpy(float)
        first = sub.iloc[0]
        rows.append(
            {
                "source": source,
                "analysis": analysis,
                "dataset": first["dataset"],
                "disease_name": first["disease_name"],
                "compartment": first["compartment"],
                "axis_family": first["axis_family"],
                "module": module,
                "metric": metric,
                "compartment_plausible": compartment_plausible(module, str(first["compartment"])),
                **compare_arrays(case, control),
            }
        )
    out = pd.DataFrame(rows)
    return add_fdr(out, "p", "fdr", ["metric"]) if not out.empty else out


def long_metric_scores(scores: pd.DataFrame) -> pd.DataFrame:
    parts = []
    for metric in ["mean_score", "high_fraction"]:
        sub = scores.copy()
        sub["metric"] = metric
        sub["value"] = sub[metric]
        if metric == "high_fraction":
            sub = sub[sub["source"].eq("direct_h5ad")].copy()
        parts.append(sub)
    return pd.concat(parts, ignore_index=True)


def residual_tests(scores: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    mean_scores = scores.copy()
    wide = mean_scores.pivot_table(
        index=[
            "source",
            "analysis",
            "dataset",
            "disease_name",
            "compartment",
            "unit_id",
            "group",
            "group_label",
            "cell_types",
        ],
        columns="module",
        values="mean_score",
        aggfunc="first",
    ).reset_index()
    for (source, analysis), sub in wide.groupby(["source", "analysis"], observed=True):
        for module, spec in AXIS_MODULES.items():
            if module not in sub.columns:
                continue
            raw = compare_arrays(
                sub.loc[sub["group"].eq("case"), module].to_numpy(float),
                sub.loc[sub["group"].eq("control"), module].to_numpy(float),
            )
            first = sub.iloc[0]
            for covariate in COVARIATE_MODULES:
                if covariate not in sub.columns:
                    continue
                residuals, slope, r2 = residualize(sub[module].to_numpy(float), sub[covariate].to_numpy(float))
                tmp = sub.copy()
                tmp["residual"] = residuals
                residual = compare_arrays(
                    tmp.loc[tmp["group"].eq("case"), "residual"].to_numpy(float),
                    tmp.loc[tmp["group"].eq("control"), "residual"].to_numpy(float),
                )
                rows.append(
                    {
                        "source": source,
                        "analysis": analysis,
                        "dataset": first["dataset"],
                        "disease_name": first["disease_name"],
                        "compartment": first["compartment"],
                        "axis_family": spec.axis_family,
                        "module": module,
                        "covariate_module": covariate,
                        "compartment_plausible": compartment_plausible(module, str(first["compartment"])),
                        "n_units_total": int(len(tmp)),
                        "residual_model": f"{module} ~ {covariate}",
                        "covariate_slope": slope,
                        "covariate_r2": r2,
                        **{f"raw_{key}": value for key, value in raw.items()},
                        **{f"residual_{key}": value for key, value in residual.items()},
                    }
                )
    out = pd.DataFrame(rows)
    if not out.empty:
        out = add_fdr(out, "residual_p", "residual_fdr", ["axis_family"])
        out["raw_nominal_positive"] = (out["raw_delta_case_minus_control"] > 0) & (out["raw_p"] <= 0.10)
        out["residual_direction_stable"] = out["residual_delta_case_minus_control"] > 0
        out["residual_nominal_positive"] = (out["residual_delta_case_minus_control"] > 0) & (out["residual_p"] <= 0.10)
    return out


def summarize_go_no_go(raw: pd.DataFrame, residuals: pd.DataFrame, module_genes: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    rows: list[dict[str, object]] = []
    if residuals.empty:
        return pd.DataFrame(), {
            "go_no_go": "NO_GO",
            "reason": "No residual tests were generated.",
            "axis_support_counts": {},
        }
    for (axis_family, disease_name), sub in residuals.groupby(["axis_family", "disease_name"], observed=True):
        plausible = sub[sub["compartment_plausible"]].copy()
        best_rows = []
        for (analysis, module), msub in plausible.groupby(["analysis", "module"], observed=True):
            tested_covariates = sorted(msub["covariate_module"].dropna().unique())
            if not tested_covariates:
                continue
            raw_positive = bool(msub["raw_nominal_positive"].all())
            all_direction_stable = bool(msub["residual_direction_stable"].all())
            nominal_covariates = int(msub["residual_nominal_positive"].sum())
            fdr_10_covariates = int(((msub["residual_delta_case_minus_control"] > 0) & (msub["residual_fdr"] <= 0.10)).sum())
            all_residual_p_le_10 = bool((msub["residual_p"] <= 0.10).all())
            median_residual_g = float(msub["residual_hedges_g"].median()) if msub["residual_hedges_g"].notna().any() else np.nan
            max_residual_p = float(msub["residual_p"].max()) if msub["residual_p"].notna().any() else np.nan
            min_residual_p = float(msub["residual_p"].min()) if msub["residual_p"].notna().any() else np.nan
            passes = (
                raw_positive
                and all_direction_stable
                and len(tested_covariates) >= 4
                and nominal_covariates >= 1
                and np.isfinite(median_residual_g)
                and median_residual_g >= 0.5
            )
            first = msub.iloc[0]
            best_rows.append(
                {
                    "axis_family": axis_family,
                    "disease_name": disease_name,
                    "analysis": analysis,
                    "compartment": first["compartment"],
                    "module": module,
                    "passes_basic_residual_controls": passes,
                    "raw_delta": float(first["raw_delta_case_minus_control"]),
                    "raw_p": float(first["raw_p"]),
                    "n_covariates_tested": len(tested_covariates),
                    "n_covariates_residual_nominal_positive": nominal_covariates,
                    "n_covariates_residual_fdr_lt_0_10": fdr_10_covariates,
                    "all_covariate_residual_p_le_0_10": all_residual_p_le_10,
                    "all_residual_deltas_positive": all_direction_stable,
                    "median_residual_hedges_g": median_residual_g,
                    "min_residual_p": min_residual_p,
                    "max_residual_p": max_residual_p,
                    "covariates_tested": ",".join(tested_covariates),
                }
            )
        if best_rows:
            best = sorted(
                best_rows,
                key=lambda row: (
                    not row["passes_basic_residual_controls"],
                    -row["n_covariates_residual_nominal_positive"],
                    -row["median_residual_hedges_g"] if np.isfinite(row["median_residual_hedges_g"]) else 0,
                    row["min_residual_p"] if np.isfinite(row["min_residual_p"]) else 1,
                ),
            )[0]
            rows.append(best)
    disease_support = pd.DataFrame(rows)
    axis_support_counts = (
        disease_support[disease_support["passes_basic_residual_controls"]]
        .groupby("axis_family")["disease_name"]
        .nunique()
        .to_dict()
        if not disease_support.empty
        else {}
    )
    axis_support_counts = {axis: int(axis_support_counts.get(axis, 0)) for axis in sorted({spec.axis_family for spec in AXIS_MODULES.values()})}
    go_axes = [axis for axis, count in axis_support_counts.items() if count >= 3]
    summary = {
        "random_seed": SEED,
        "axis_support_counts_after_basic_residual_controls": axis_support_counts,
        "go_axes": go_axes,
        "go_no_go": "GO" if go_axes else "NO_GO",
        "pivot_recommendation": (
            "At least one axis reaches three diseases with compartment-plausible raw positive signal and direction-stable residual support."
            if go_axes
            else "Pivot before hour 6: neither OSM/OSMR nor C1q/complement reaches three diseases with compartment-plausible signal after basic residual controls."
        ),
        "decision_rule": (
            "A disease supports an axis if one compartment-plausible module has raw positive p<=0.10, all available residual deltas remain positive across at least four covariates, "
            "at least one covariate residual remains nominal positive p<=0.10, and median residual Hedges g>=0.5."
        ),
        "module_gene_presence_file": str((OUT / "wave5_module_gene_presence.tsv").relative_to(ROOT)),
        "n_raw_contrasts": int(len(raw)),
        "n_residual_tests": int(len(residuals)),
        "n_module_gene_rows": int(len(module_genes)),
    }
    return disease_support, summary


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    direct_scores, direct_genes = direct_h5ad_scores()
    gse_scores, gse_genes = gse111972_scores()
    scores = pd.concat([direct_scores, gse_scores], ignore_index=True, sort=False)
    module_genes = pd.concat([direct_genes, gse_genes], ignore_index=True, sort=False)
    scores.to_csv(OUT / "wave5_donor_sample_axis_scores.tsv", sep="\t", index=False)
    module_genes.to_csv(OUT / "wave5_module_gene_presence.tsv", sep="\t", index=False)

    long_scores = long_metric_scores(scores) if not scores.empty else pd.DataFrame()
    raw = raw_contrasts(long_scores) if not long_scores.empty else pd.DataFrame()
    raw.to_csv(OUT / "wave5_raw_axis_contrasts.tsv", sep="\t", index=False)

    residuals = residual_tests(scores) if not scores.empty else pd.DataFrame()
    residuals.to_csv(OUT / "wave5_residual_axis_tests.tsv", sep="\t", index=False)

    disease_support, summary = summarize_go_no_go(raw, residuals, module_genes)
    disease_support.to_csv(OUT / "wave5_axis_go_no_go.tsv", sep="\t", index=False)
    (OUT / "wave5_local_quant_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
