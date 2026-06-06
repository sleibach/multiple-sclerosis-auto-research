#!/usr/bin/env python3
"""Wave79 strict targetability-shortlist residual audit.

Wave78 closed the inhibitory-receptor escape route. This wave tests the
remaining Wave75-C targetability shortlist (`CD58`, `SPNS1`, `P4HB`,
`SEL1L3`) plus `IFI30` as a benchmark. It is deliberately falsification-first:
the candidate must retain donor-level disease signal after generic
inflammation, APC/lysosomal, stress/injury, and T-cell-admixture adjustment,
and then show an MS anchor plus treatment-response support.
"""

from __future__ import annotations

import json
import math
import warnings
from pathlib import Path
from typing import Any

import anndata as ad
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import sparse, stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_osmr_complement_axes import CONFIGS, ROOT


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave79_targetability_shortlist_residual_audit"

CANDIDATE_GENES = ["CD58", "SPNS1", "P4HB", "SEL1L3"]
BENCHMARK_GENES = ["IFI30"]
ALL_TARGET_GENES = CANDIDATE_GENES + BENCHMARK_GENES

MODULES = {
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "CD74", "IFI30", "HLA-DRA", "HLA-DRB1"],
    "hla_ii_apc": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "CIITA", "RFX5"],
    "lysosomal_apc": ["IFI30", "CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"],
    "inflammatory_nfkb": ["IL1B", "TNF", "CXCL8", "CCL2", "CCL3", "CCL4", "NFKBIA", "TREM1", "OSM"],
    "lipid_loader_repair": [
        "ACSL1",
        "APOE",
        "GPNMB",
        "LPL",
        "PLIN2",
        "CD36",
        "LIPA",
        "FABP5",
        "TREM2",
        "MSR1",
        "MERTK",
        "SPP1",
    ],
    "er_upr_stress": ["HSPA5", "XBP1", "DDIT3", "ATF4", "HERPUD1", "DNAJB9", "HSP90B1", "CALR", "PDIA3"],
    "stromal_injury": ["VIM", "FN1", "COL1A1", "COL1A2", "COL3A1", "SPARC", "TIMP1", "MMP2"],
    "t_cell_admixture": ["CD3D", "CD3E", "TRAC", "CD2", "LCK", "IL7R"],
}
CORE_COVARIATES = ["ifn_apc", "hla_ii_apc", "lysosomal_apc", "inflammatory_nfkb"]
EXTRA_COVARIATES = ["lipid_loader_repair", "er_upr_stress", "stromal_injury", "t_cell_admixture"]

MS_SIG = ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv"
W39 = ROOT / "phases/v3/results" / "wave39_surfaceome_rescue_after_resolution_pivot" / "surfaceome_rescue_rank.tsv"
W62 = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W68_RAW = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "raw_remission_response_gene_tests.tsv"
W68_ADJ = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
W71 = ROOT / "phases/v3/results" / "wave71_global_survivor_meta_rank" / "global_survivor_meta_rank.tsv"
RA_COUNTS = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"
RA_MODULES = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_module_scores.tsv"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
    if df.empty:
        return "_No rows._"
    view = df.head(max_rows).copy()
    cols = list(view.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in view.iterrows():
        vals = []
        for col in cols:
            value = row[col]
            if isinstance(value, float):
                vals.append("" if math.isnan(value) else f"{value:.4g}")
            else:
                vals.append(str(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def bh(values: pd.Series | np.ndarray) -> np.ndarray:
    return multipletests(pd.Series(values).fillna(1.0).to_numpy(float), method="fdr_bh")[1]


def numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series.replace("NA", np.nan), errors="coerce")


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled = ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    if pooled <= 0:
        return np.nan
    correction = 1.0 - 3.0 / (4.0 * (len(a) + len(b)) - 9.0)
    return float(((a.mean() - b.mean()) / math.sqrt(pooled)) * correction)


def contrast(values: pd.Series, groups: pd.Series) -> dict[str, Any]:
    case = values.loc[groups.eq("case")].astype(float).to_numpy()
    control = values.loc[groups.eq("control")].astype(float).to_numpy()
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if len(case) >= 2 and len(control) >= 2 and (np.nanstd(case, ddof=1) + np.nanstd(control, ddof=1)) >= 1e-8:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
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
        "p": float(p_value) if np.isfinite(p_value) else np.nan,
    }


def selected_gene_indices(a: ad.AnnData, symbol_column: str, selected: set[str]) -> dict[str, list[int]]:
    if symbol_column in a.var.columns:
        symbols = a.var[symbol_column].astype(str).tolist()
    elif "feature_name" in a.var.columns:
        symbols = a.var["feature_name"].astype(str).tolist()
    else:
        symbols = list(map(str, a.var_names))
    out: dict[str, list[int]] = {}
    for idx, symbol in enumerate(symbols):
        gene = str(symbol).strip().upper()
        if gene in selected:
            out.setdefault(gene, []).append(idx)
    return out


def aggregate_selected_config(config, a: ad.AnnData, x) -> pd.DataFrame:
    selected = set(ALL_TARGET_GENES)
    for genes in MODULES.values():
        selected.update(genes)

    obs = a.obs.copy()
    mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
    obs_sub = obs.loc[mask].copy()
    cell_idx = np.flatnonzero(mask.to_numpy())
    if obs_sub.empty:
        return pd.DataFrame()
    donor_counts = obs_sub.groupby(["donor_id", "disease"], observed=True).size().rename("n_cells").reset_index()
    donor_counts = donor_counts.loc[donor_counts["n_cells"] >= 10].copy()
    if donor_counts.empty:
        return pd.DataFrame()
    donor_keys = list(zip(donor_counts["donor_id"].astype(str), donor_counts["disease"].astype(str), strict=False))
    key_to_row = {key: i for i, key in enumerate(donor_keys)}
    rows = []
    cols = []
    data = []
    for local_cell, (donor, disease) in enumerate(
        zip(obs_sub["donor_id"].astype(str), obs_sub["disease"].astype(str), strict=False)
    ):
        key = (donor, disease)
        if key in key_to_row:
            rows.append(key_to_row[key])
            cols.append(local_cell)
            data.append(1.0)
    group = sparse.csr_matrix((data, (rows, cols)), shape=(len(donor_keys), len(obs_sub)))
    x_sub = x[cell_idx]
    lib_size = np.asarray(group @ np.asarray(x_sub.sum(axis=1)).ravel()).ravel().astype(float)
    lib_size[~np.isfinite(lib_size) | (lib_size <= 0)] = np.nan

    gene_to_idx = selected_gene_indices(a, config.gene_symbol_column, selected)
    counts_by_gene: dict[str, np.ndarray] = {}
    for gene, idxs in gene_to_idx.items():
        summed = group @ x_sub[:, idxs]
        arr = summed.toarray() if sparse.issparse(summed) else np.asarray(summed)
        counts_by_gene[gene] = np.asarray(arr.sum(axis=1)).ravel().astype(float)
    if not counts_by_gene:
        return pd.DataFrame()
    counts = pd.DataFrame(counts_by_gene)
    log2_cpm = np.log2(counts.div(lib_size, axis=0).mul(1e6) + 1.0)

    meta = donor_counts.copy().reset_index(drop=True)
    meta["analysis"] = config.name
    meta["dataset_path"] = str(config.path.relative_to(ROOT))
    meta["disease_name"] = config.disease_label
    meta["compartment"] = config.compartment
    meta["role"] = config.role
    meta["group"] = np.where(meta["disease"].eq(config.disease_label), "case", "control")

    z = log2_cpm.copy()
    control_mask = meta["group"].eq("control").to_numpy()
    for gene in z.columns:
        mean = float(np.nanmean(log2_cpm.loc[control_mask, gene]))
        sd = float(np.nanstd(log2_cpm.loc[control_mask, gene], ddof=1))
        if not math.isfinite(sd) or sd < 1e-6:
            sd = 1.0
        z[gene] = (log2_cpm[gene] - mean) / sd

    out = meta.copy()
    for gene in ALL_TARGET_GENES:
        out[f"target_{gene}"] = z[gene] if gene in z.columns else np.nan
        out[f"log2cpm_{gene}"] = log2_cpm[gene] if gene in log2_cpm.columns else np.nan
    for module, genes in MODULES.items():
        present = [g for g in genes if g in z.columns]
        out[f"module_{module}"] = z[present].mean(axis=1) if present else np.nan
        out[f"module_{module}_n_genes"] = len(present)
    out["generic_inflammation_mean"] = out[[f"module_{m}" for m in CORE_COVARIATES if f"module_{m}" in out]].mean(axis=1)
    out["injury_stress_mean"] = out[["module_er_upr_stress", "module_stromal_injury"]].mean(axis=1)
    return out


def residualize_univariate(y: np.ndarray, x: np.ndarray) -> tuple[np.ndarray, float, float]:
    mask = np.isfinite(y) & np.isfinite(x)
    residuals = np.full(len(y), np.nan)
    if mask.sum() < 5 or np.nanstd(x[mask]) < 1e-8:
        return residuals, np.nan, np.nan
    slope, intercept, r_value, _, _ = stats.linregress(x[mask], y[mask])
    residuals[mask] = y[mask] - (intercept + slope * x[mask])
    return residuals, float(slope), float(r_value**2)


def residualize_multivariable(sub: pd.DataFrame, y_col: str, covariates: list[str]) -> tuple[pd.Series, str]:
    needed = [y_col] + covariates
    df = sub.dropna(subset=needed).copy()
    residuals = pd.Series(np.nan, index=sub.index)
    if df.shape[0] < max(8, len(covariates) + 5):
        return residuals, "insufficient_rows"
    if df[y_col].std(ddof=1) < 1e-8:
        return residuals, "insufficient_target_variance"
    usable = []
    for cov in covariates:
        if df[cov].std(ddof=1) >= 1e-8:
            usable.append(cov)
    if not usable:
        return residuals, "no_usable_covariates"
    model_df = df.rename(columns={y_col: "target_y"})
    formula = "target_y ~ " + " + ".join(usable)
    try:
        model = smf.ols(formula, data=model_df).fit()
        residuals.loc[df.index] = model.resid
        return residuals, "ok:" + formula
    except Exception as exc:  # noqa: BLE001
        return residuals, f"fit_failed:{type(exc).__name__}:{exc}"


def build_direct_residual_tests() -> tuple[pd.DataFrame, pd.DataFrame]:
    cache: dict[Path, tuple[ad.AnnData, Any]] = {}
    donor_tables = []
    run_log = []
    for config in CONFIGS:
        try:
            if config.path not in cache:
                a = ad.read_h5ad(config.path)
                x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
                cache[config.path] = (a, x)
            a, x = cache[config.path]
            donor = aggregate_selected_config(config, a, x)
            donor_tables.append(donor)
            run_log.append({"analysis": config.name, "status": "completed", "n_rows": int(len(donor))})
        except Exception as exc:  # noqa: BLE001
            run_log.append({"analysis": config.name, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})
    donor_scores = pd.concat(donor_tables, ignore_index=True) if donor_tables else pd.DataFrame()
    donor_scores.to_csv(OUT / "direct_shortlist_donor_scores.tsv", sep="\t", index=False)
    pd.DataFrame(run_log).to_csv(OUT / "direct_shortlist_run_log.tsv", sep="\t", index=False)

    rows: list[dict[str, Any]] = []
    covariates = [f"module_{m}" for m in CORE_COVARIATES + EXTRA_COVARIATES] + [
        "generic_inflammation_mean",
        "injury_stress_mean",
    ]
    multi_covariates = ["generic_inflammation_mean", "injury_stress_mean", "module_t_cell_admixture"]
    for analysis, sub in donor_scores.groupby("analysis", observed=True):
        first = sub.iloc[0]
        for gene in ALL_TARGET_GENES:
            y_col = f"target_{gene}"
            if y_col not in sub.columns or sub[y_col].notna().sum() < 4:
                continue
            raw = contrast(sub[y_col], sub["group"])
            base = {
                "analysis": analysis,
                "dataset_path": first["dataset_path"],
                "disease_name": first["disease_name"],
                "compartment": first["compartment"],
                "role": first["role"],
                "gene": gene,
                "model": "RAW",
                "covariates": "",
                "covariate_slope": np.nan,
                "covariate_r2": np.nan,
                "model_status": "ok",
                **{f"raw_{k}": v for k, v in raw.items()},
                **{f"residual_{k}": v for k, v in raw.items()},
            }
            rows.append(base)
            y = sub[y_col].astype(float).to_numpy()
            for cov in covariates:
                if cov not in sub.columns:
                    continue
                residuals, slope, r2 = residualize_univariate(y, sub[cov].astype(float).to_numpy())
                residual = contrast(pd.Series(residuals, index=sub.index), sub["group"])
                rows.append(
                    {
                        "analysis": analysis,
                        "dataset_path": first["dataset_path"],
                        "disease_name": first["disease_name"],
                        "compartment": first["compartment"],
                        "role": first["role"],
                        "gene": gene,
                        "model": "univariate_residual",
                        "covariates": cov.replace("module_", ""),
                        "covariate_slope": slope,
                        "covariate_r2": r2,
                        "model_status": "ok" if np.isfinite(r2) else "insufficient_covariate",
                        **{f"raw_{k}": v for k, v in raw.items()},
                        **{f"residual_{k}": v for k, v in residual.items()},
                    }
                )
            usable_multi = [cov for cov in multi_covariates if cov in sub.columns]
            residuals, status = residualize_multivariable(sub, y_col, usable_multi)
            residual = contrast(residuals, sub["group"])
            rows.append(
                {
                    "analysis": analysis,
                    "dataset_path": first["dataset_path"],
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "gene": gene,
                    "model": "multivariable_residual",
                    "covariates": ";".join(c.replace("module_", "") for c in usable_multi),
                    "covariate_slope": np.nan,
                    "covariate_r2": np.nan,
                    "model_status": status,
                    **{f"raw_{k}": v for k, v in raw.items()},
                    **{f"residual_{k}": v for k, v in residual.items()},
                }
            )
    tests = pd.DataFrame(rows)
    if not tests.empty:
        tests["raw_positive"] = (tests["raw_delta_case_minus_control"] >= 0.20) & (tests["raw_p"] <= 0.05)
        tests["residual_positive"] = (
            tests["model"].ne("RAW")
            & tests["raw_positive"]
            & (tests["residual_delta_case_minus_control"] >= 0.20)
            & (tests["residual_p"] <= 0.05)
        )
        tests["multivariable_positive_trend"] = (
            tests["model"].eq("multivariable_residual")
            & tests["raw_positive"]
            & (tests["residual_delta_case_minus_control"] >= 0.20)
            & (tests["residual_p"] <= 0.10)
            & tests["model_status"].astype(str).str.startswith("ok")
        )
        tests["residual_fdr"] = np.nan
        mask = tests["model"].ne("RAW") & tests["residual_p"].notna()
        if mask.any():
            tests.loc[mask, "residual_fdr"] = bh(tests.loc[mask, "residual_p"])
    tests.to_csv(OUT / "direct_shortlist_residual_tests.tsv", sep="\t", index=False)
    return donor_scores, tests


def load_ms() -> pd.DataFrame:
    df = read_tsv(MS_SIG)
    if df.empty:
        return pd.DataFrame()
    sub = df[df["gene"].astype(str).str.upper().isin(ALL_TARGET_GENES)].copy()
    sub["ms_expression_anchor"] = (sub["delta_log2"] >= 0.20) & (sub["p"] <= 0.05)
    return sub.sort_values("p")


def load_w62() -> pd.DataFrame:
    df = read_tsv(W62)
    if df.empty:
        return pd.DataFrame()
    sub = df[df["gene"].astype(str).str.upper().isin(ALL_TARGET_GENES)].copy()
    sub["ms_genetic_anchor"] = (sub["ms_max_l2g_score"].fillna(0) >= 0.50) | (
        sub["strong_qtl_coloc_diseases"].fillna("").astype(str).str.contains("MS")
    )
    return sub


def load_response() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = read_tsv(W68_RAW)
    adj = read_tsv(W68_ADJ)
    rows = []
    if not raw.empty:
        sub = raw[raw["gene"].astype(str).str.upper().isin(ALL_TARGET_GENES)].copy()
        for _, row in sub.iterrows():
            rows.append(
                {
                    "dataset": "GSE282122_IBD_myeloid_antiTNF",
                    "gene": row["gene"],
                    "cell_state": row["cell_state"],
                    "test": "raw_remission_delta_difference",
                    "effect": row["raw_delta_remission_minus_non"],
                    "p": row["raw_p"],
                    "fdr": row["raw_fdr"],
                    "supportive_suppression_response": bool(row["raw_delta_remission_minus_non"] < 0 and row["raw_p"] <= 0.10),
                }
            )
    if not adj.empty:
        sub = adj[adj["gene"].astype(str).str.upper().isin(ALL_TARGET_GENES)].copy()
        for _, row in sub.iterrows():
            rows.append(
                {
                    "dataset": "GSE282122_IBD_myeloid_antiTNF",
                    "gene": row["gene"],
                    "cell_state": row["cell_state"],
                    "test": "generic_adjusted_remission_delta",
                    "effect": row.get("remission_adjusted_delta", np.nan),
                    "p": row.get("remission_adjusted_p", np.nan),
                    "fdr": row.get("remission_adjusted_fdr", np.nan),
                    "supportive_suppression_response": bool(
                        pd.notna(row.get("remission_adjusted_delta", np.nan))
                        and row.get("remission_adjusted_delta", np.nan) < 0
                        and row.get("remission_adjusted_p", 1.0) <= 0.10
                        and row.get("remission_adjusted_fdr", 1.0) <= 0.10
                    ),
                }
            )
    ibd = pd.DataFrame(rows)

    ra = compute_ra_response()
    return ibd, ra


def compute_ra_response() -> pd.DataFrame:
    counts = read_tsv(RA_COUNTS)
    meta = read_tsv(RA_META)
    modules = read_tsv(RA_MODULES)
    if counts.empty or meta.empty or modules.empty:
        return pd.DataFrame()
    counts = counts.set_index("GeneSymbol")
    genes = [g for g in ALL_TARGET_GENES if g in counts.index]
    if not genes:
        return pd.DataFrame()
    lib = counts.sum(axis=0).replace(0, np.nan)
    expr = np.log2(counts.loc[genes].astype(float).div(lib, axis=1).mul(1_000_000.0) + 1.0).T
    expr = expr.reset_index().rename(columns={"index": "count_column"})
    long = expr.merge(meta, on="count_column", how="left")
    generic = modules[modules["module"].eq("inflammatory_nfkb")][["count_column", "score"]].rename(
        columns={"score": "generic_nfkb_score"}
    )
    long = long.merge(generic, on="count_column", how="left")
    for col in ["inflammatory_score", "das28_score", "generic_nfkb_score"]:
        if col in long.columns:
            long[col] = numeric(long[col])
    rows = []
    for gene in genes:
        g = long[[
            "patient",
            "timepoint",
            "response_code",
            "inflammatory_score",
            "das28_score",
            "generic_nfkb_score",
            gene,
        ]].dropna(subset=["patient", "timepoint", gene])
        wide = g.pivot_table(index="patient", columns="timepoint", values=[gene, "generic_nfkb_score"], aggfunc="first")
        wide.columns = [f"{a}_{b}" for a, b in wide.columns]
        wide = wide.reset_index()
        pre = g[g["timepoint"].eq("pre")].drop_duplicates("patient")
        wide = wide.merge(pre[["patient", "response_code", "inflammatory_score", "das28_score"]], on="patient", how="left")
        if f"{gene}_pre" not in wide.columns or f"{gene}_post" not in wide.columns:
            continue
        wide["target_pre"] = wide[f"{gene}_pre"]
        wide["target_delta"] = wide[f"{gene}_post"] - wide[f"{gene}_pre"]
        for col in ["target_pre", "target_delta", "generic_nfkb_score_pre", "generic_nfkb_score_post"]:
            if col in wide.columns:
                sd = wide[col].std(ddof=1)
                wide[col + "_z"] = (wide[col] - wide[col].mean()) / sd if pd.notna(sd) and sd > 0 else np.nan
        wide["generic_delta_z"] = wide.get("generic_nfkb_score_post_z", np.nan) - wide.get("generic_nfkb_score_pre_z", np.nan)
        wide["good_response"] = wide["response_code"].eq("r").astype(int)
        for endpoint, y_col in [("baseline_pre", "target_pre_z"), ("delta_post_minus_pre", "target_delta_z")]:
            model_df = wide.rename(columns={"good_response": "response"}).dropna(
                subset=[y_col, "response", "generic_nfkb_score_pre_z", "inflammatory_score", "das28_score"]
            ).copy()
            if endpoint == "delta_post_minus_pre":
                model_df = model_df.dropna(subset=["target_pre_z", "generic_delta_z"])
                rhs = "response + target_pre_z + generic_delta_z + generic_nfkb_score_pre_z + inflammatory_score + das28_score"
            else:
                rhs = "response + generic_nfkb_score_pre_z + inflammatory_score + das28_score"
            if model_df.shape[0] < 20 or model_df["response"].nunique() < 2 or model_df[y_col].std(ddof=1) < 1e-8:
                coef, pval, status = np.nan, np.nan, "insufficient"
            else:
                try:
                    model = smf.ols(f"{y_col} ~ {rhs}", data=model_df).fit()
                    coef = float(model.params.get("response", np.nan))
                    pval = float(model.pvalues.get("response", np.nan))
                    status = "ok"
                except Exception as exc:  # noqa: BLE001
                    coef, pval, status = np.nan, np.nan, f"fit_failed:{type(exc).__name__}:{exc}"
            rows.append(
                {
                    "dataset": "GSE198520_RA_synovium_antiTNF",
                    "gene": gene,
                    "endpoint": endpoint,
                    "comparison": "good_vs_moderate_none",
                    "n": int(model_df.shape[0]),
                    "effect": coef,
                    "p": pval,
                    "model_status": status,
                    "supportive_suppression_response": bool(endpoint == "delta_post_minus_pre" and coef < 0 and pval <= 0.10),
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = bh(out["p"])
    return out.sort_values(["supportive_suppression_response", "p"], ascending=[False, True])


def load_modality_rows() -> pd.DataFrame:
    frames = []
    for label, path in [("wave39_surfaceome", W39), ("wave62_target_resolution", W62), ("wave71_meta", W71)]:
        df = read_tsv(path)
        if df.empty or "gene" not in df.columns:
            continue
        sub = df[df["gene"].astype(str).str.upper().isin(ALL_TARGET_GENES)].copy()
        if not sub.empty:
            sub.insert(0, "source", label)
            frames.append(sub)
    return pd.concat(frames, ignore_index=True, sort=False) if frames else pd.DataFrame()


def build_candidate_matrix(
    residual_tests: pd.DataFrame,
    ms: pd.DataFrame,
    w62: pd.DataFrame,
    ibd: pd.DataFrame,
    ra: pd.DataFrame,
    modality: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for gene in ALL_TARGET_GENES:
        r = residual_tests[residual_tests["gene"].eq(gene)] if not residual_tests.empty else pd.DataFrame()
        raw = r[(r["model"].eq("RAW")) & (r["raw_positive"])] if not r.empty else pd.DataFrame()
        mv = r[(r["model"].eq("multivariable_residual")) & (r["multivariable_positive_trend"])] if not r.empty else pd.DataFrame()
        core = r[
            (r["model"].eq("univariate_residual"))
            & (r["covariates"].isin(CORE_COVARIATES))
            & (r["residual_positive"])
        ] if not r.empty else pd.DataFrame()
        core_counts = (
            core.groupby(["analysis", "disease_name", "role"], observed=True)["covariates"].nunique().reset_index(name="n_core_retained")
            if not core.empty
            else pd.DataFrame(columns=["analysis", "disease_name", "role", "n_core_retained"])
        )
        strict_core = core_counts[core_counts["n_core_retained"] >= len(CORE_COVARIATES)]
        myeloid_mv = mv[mv["role"].eq("myeloid_apc")]
        ms_row = ms[ms["gene"].eq(gene)] if not ms.empty else pd.DataFrame()
        w62_row = w62[w62["gene"].eq(gene)] if not w62.empty else pd.DataFrame()
        ms_expression_anchor = bool(ms_row["ms_expression_anchor"].iloc[0]) if not ms_row.empty else False
        ms_genetic_anchor = bool(w62_row["ms_genetic_anchor"].iloc[0]) if not w62_row.empty else False
        ibd_gene = ibd[ibd["gene"].eq(gene)] if not ibd.empty else pd.DataFrame()
        ra_gene = ra[ra["gene"].eq(gene)] if not ra.empty else pd.DataFrame()
        ibd_support = bool(ibd_gene["supportive_suppression_response"].any()) if not ibd_gene.empty else False
        ra_support = bool(ra_gene["supportive_suppression_response"].any()) if not ra_gene.empty else False
        modality_gene = modality[modality["gene"].eq(gene)] if not modality.empty else pd.DataFrame()

        direct_residual_disease_count = int(mv["disease_name"].nunique()) if not mv.empty else 0
        myeloid_residual_disease_count = int(myeloid_mv["disease_name"].nunique()) if not myeloid_mv.empty else 0
        strict_core_disease_count = int(strict_core["disease_name"].nunique()) if not strict_core.empty else 0
        response_support_count = int(ibd_support) + int(ra_support)
        ms_anchor = ms_expression_anchor or ms_genetic_anchor
        modality_ready = False
        if gene == "CD58":
            modality_ready = True  # extracellular ligand/interface, biologic-accessible in principle
        elif gene == "P4HB":
            modality_ready = bool(
                not modality_gene.empty
                and (
                    modality_gene.get("chembl_activity_count", pd.Series([0])).fillna(0).astype(float).max() > 0
                )
            )
        else:
            modality_ready = False

        pass_count = sum(
            [
                direct_residual_disease_count >= 3,
                myeloid_residual_disease_count >= 2,
                strict_core_disease_count >= 2,
                ms_anchor,
                response_support_count >= 1,
                response_support_count >= 2,
                modality_ready,
            ]
        )
        if gene == "IFI30":
            call = "BENCHMARK_NOT_NOMINATION"
        elif pass_count >= 6:
            call = "PARK_SHORTLIST_SURVIVOR_NEEDS_PRIOR_ART_AND_PERTURBATION"
        elif gene == "CD58" and ms_genetic_anchor:
            call = "PARK_CD58_MS_GENETIC_BUT_NO_STATE_RESPONSE_CONVERGENCE"
        else:
            call = "NO_GO_TARGETABILITY_SHORTLIST"

        reasons = []
        if direct_residual_disease_count < 3:
            reasons.append("insufficient multivariable residual disease breadth")
        if myeloid_residual_disease_count < 2:
            reasons.append("insufficient APC/myeloid residual breadth")
        if strict_core_disease_count < 2:
            reasons.append("does not survive all core IFN/HLA/lysosome/NFkB covariates in >=2 diseases")
        if not ms_anchor:
            reasons.append("no MS expression or target-resolved genetic anchor")
        if response_support_count == 0:
            reasons.append("no RA/IBD suppression-response support")
        elif response_support_count == 1:
            reasons.append("response support does not cross-replicate")
        if not modality_ready:
            reasons.append("no near-term selective modality in local evidence")

        rows.append(
            {
                "gene": gene,
                "call": call,
                "pass_count": pass_count,
                "direct_multivariable_residual_disease_count": direct_residual_disease_count,
                "direct_multivariable_residual_diseases": ";".join(sorted(mv["disease_name"].dropna().astype(str).unique())) if not mv.empty else "",
                "myeloid_multivariable_residual_disease_count": myeloid_residual_disease_count,
                "strict_core_residual_disease_count": strict_core_disease_count,
                "raw_positive_disease_count": int(raw["disease_name"].nunique()) if not raw.empty else 0,
                "ms_expression_anchor": ms_expression_anchor,
                "ms_delta_log2": np.nan if ms_row.empty else float(ms_row["delta_log2"].iloc[0]),
                "ms_p": np.nan if ms_row.empty else float(ms_row["p"].iloc[0]),
                "ms_genetic_anchor": ms_genetic_anchor,
                "wave62_call": "" if w62_row.empty else str(w62_row["wave62_call"].iloc[0]),
                "ms_max_l2g_score": np.nan if w62_row.empty else float(w62_row["ms_max_l2g_score"].iloc[0]),
                "ibd_response_support": ibd_support,
                "ra_response_support": ra_support,
                "response_support_count": response_support_count,
                "modality_ready_local": modality_ready,
                "decision_reason": "; ".join(reasons) if reasons else "all local gates pass pending prior-art/perturbation",
            }
        )
    out = pd.DataFrame(rows)
    return out.sort_values(["pass_count", "direct_multivariable_residual_disease_count"], ascending=[False, False])


def write_report(
    candidate_matrix: pd.DataFrame,
    residual_tests: pd.DataFrame,
    ms: pd.DataFrame,
    w62: pd.DataFrame,
    ibd: pd.DataFrame,
    ra: pd.DataFrame,
    modality: pd.DataFrame,
) -> None:
    top_call = candidate_matrix["call"].iloc[0] if not candidate_matrix.empty else "NO_DATA"
    positive_mv = residual_tests[
        residual_tests.get("multivariable_positive_trend", pd.Series(False, index=residual_tests.index)).fillna(False)
    ].copy() if not residual_tests.empty else pd.DataFrame()
    report = [
        "# Wave79 Targetability Shortlist Residual Audit",
        "",
        "## Question",
        "",
        "Do `CD58`, `SPNS1`, `P4HB`, or `SEL1L3` retain disease-state signal",
        "after donor-level residualization and show MS plus treatment-response",
        "support sufficient to reopen targetability?",
        "",
        "## Verdict",
        "",
        top_call,
        "",
        "## Candidate Matrix",
        "",
        markdown_table(candidate_matrix, 20),
        "",
        "## Multivariable Residual Positive Contexts",
        "",
        markdown_table(
            positive_mv[
                [
                    "gene",
                    "analysis",
                    "disease_name",
                    "compartment",
                    "role",
                    "raw_delta_case_minus_control",
                    "raw_p",
                    "residual_delta_case_minus_control",
                    "residual_p",
                    "model_status",
                ]
            ].sort_values(["gene", "residual_p"])
            if not positive_mv.empty
            else positive_mv,
            40,
        ),
        "",
        "## MS White-Matter Rows",
        "",
        markdown_table(ms, 15),
        "",
        "## Wave62 Target-Resolution Rows",
        "",
        markdown_table(w62, 15),
        "",
        "## IBD Anti-TNF Response Rows",
        "",
        markdown_table(ibd, 30),
        "",
        "## RA Anti-TNF Response Rows",
        "",
        markdown_table(ra, 30),
        "",
        "## Modality/Prior Local Rows",
        "",
        markdown_table(modality, 30),
        "",
        "## Interpretation Guardrails",
        "",
        "- `CD58` can pass MS genetics without passing disease-state or response",
        "  convergence; that is a genetics benchmark, not a therapeutic claim.",
        "- `SPNS1` and `P4HB` broad expression must survive stress/injury",
        "  residualization and show an MS anchor; otherwise they are state/stress",
        "  markers.",
        "- `SEL1L3` MS expression is not enough without cell-compartment and",
        "  response support.",
        "- `IFI30` is included as an APC/lysosomal benchmark, not a target",
        "  nomination, because broad antigen-processing suppression has host-defense",
        "  and prior-art liabilities.",
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    donor_scores, residual_tests = build_direct_residual_tests()
    ms = load_ms()
    w62 = load_w62()
    ibd, ra = load_response()
    modality = load_modality_rows()
    candidate_matrix = build_candidate_matrix(residual_tests, ms, w62, ibd, ra, modality)

    ms.to_csv(OUT / "ms_white_matter_shortlist_rows.tsv", sep="\t", index=False)
    w62.to_csv(OUT / "wave62_shortlist_rows.tsv", sep="\t", index=False)
    ibd.to_csv(OUT / "ibd_antitnf_shortlist_response_rows.tsv", sep="\t", index=False)
    ra.to_csv(OUT / "ra_antitnf_shortlist_response_rows.tsv", sep="\t", index=False)
    modality.to_csv(OUT / "local_modality_shortlist_rows.tsv", sep="\t", index=False)
    candidate_matrix.to_csv(OUT / "targetability_shortlist_candidate_matrix.tsv", sep="\t", index=False)
    summary = {
        "seed": SEED,
        "top_call": candidate_matrix["call"].iloc[0] if not candidate_matrix.empty else "NO_DATA",
        "top_gene": candidate_matrix["gene"].iloc[0] if not candidate_matrix.empty else "",
        "candidate_genes": CANDIDATE_GENES,
        "benchmark_genes": BENCHMARK_GENES,
        "n_donor_score_rows": int(len(donor_scores)),
        "n_residual_tests": int(len(residual_tests)),
        "inputs": {
            "ms_signature": rel(MS_SIG),
            "wave39_surfaceome": rel(W39),
            "wave62_target_resolution": rel(W62),
            "wave68_raw": rel(W68_RAW),
            "wave68_adjusted": rel(W68_ADJ),
            "wave71_meta": rel(W71),
            "ra_counts": rel(RA_COUNTS),
            "ra_meta": rel(RA_META),
            "ra_modules": rel(RA_MODULES),
        },
    }
    write_json(OUT / "summary.json", summary)
    write_report(candidate_matrix, residual_tests, ms, w62, ibd, ra, modality)


if __name__ == "__main__":
    main()
