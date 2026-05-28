#!/usr/bin/env python3
"""Orchestrator dependency scan around the recurrent CD74/HLA-II state.

This is a post-convergence forcing analysis. Earlier work established that the
cross-autoimmune signal is a CD74/CIITA/HLA-II antigen-presentation state, but
direct state markers and several obvious controllers failed target gates. This
script asks a narrower question:

Which druggable or tractable surface/lysosomal/trafficking dependencies
recurrently track the CD74/HLA-II state after adjusting for generic IFN and
case/control status?

The output is a prioritization artifact, not a therapeutic claim.
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

from v3_analyze_osmr_complement_axes import CONFIGS, ROOT

SEED = 20260526
OUT = ROOT / "results_v3" / "wave15_orchestrator_dependency_scan"
MODULE_SCORES = ROOT / "results_v3" / "direct_h5ad_cell_state" / "direct_h5ad_donor_module_scores.tsv"
MS_SIGNATURE = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"

STATE_MODULES = ("hla_ii_apc", "mif_cd74_receptor_state")
IFN_MODULE = "ifn_apc"

CANDIDATE_CLASSES: dict[str, list[str]] = {
    "state_markers_positive_controls": [
        "CD74",
        "CIITA",
        "RFX5",
        "HLA-DRA",
        "HLA-DRB1",
        "HLA-DPA1",
        "HLA-DPB1",
    ],
    "hla_ii_loading_editing": [
        "HLA-DMA",
        "HLA-DMB",
        "HLA-DOA",
        "HLA-DOB",
        "IFI30",
        "CTSS",
        "CTSL",
        "CTSB",
        "CTSD",
        "CTSH",
        "CTSZ",
        "CST3",
        "CSTA",
        "CSTB",
    ],
    "lysosome_endosome_lipid": [
        "LAMP1",
        "LAMP2",
        "LAMP3",
        "LIPA",
        "NPC1",
        "NPC2",
        "SCARB1",
        "SCARB2",
        "SORT1",
        "M6PR",
        "IGF2R",
        "LAPTM5",
        "ATP6V0D2",
        "ATP6V1B2",
        "TCIRG1",
    ],
    "trafficking_sorting": [
        "AP2M1",
        "AP1S2",
        "RAB5A",
        "RAB7A",
        "RAB11A",
        "VAMP3",
        "VAMP7",
        "SNX5",
        "SNX10",
        "VPS35",
        "VPS26A",
        "HGS",
        "EEA1",
    ],
    "uptake_complement_phagocytosis": [
        "FCGR2A",
        "FCGR2B",
        "FCGR3A",
        "C1QA",
        "C1QB",
        "C1QC",
        "C3AR1",
        "C5AR1",
        "TYROBP",
        "TREM2",
        "MERTK",
        "AXL",
        "MSR1",
        "MRC1",
        "MARCO",
        "LRP1",
        "CALR",
        "ITGAX",
        "ITGAM",
    ],
    "glycan_checkpoint_surface": [
        "LGALS1",
        "LGALS3",
        "LGALS8",
        "LGALS9",
        "SIGLEC1",
        "SIGLEC10",
        "CD44",
        "CD83",
        "CD86",
        "PDCD1LG2",
        "CD274",
    ],
    "failed_or_crowded_comparators": [
        "GSK3B",
        "GSK3A",
        "SLC15A4",
        "TASL",
        "CXorf21",
        "IRF5",
        "PTPN2",
        "TNFAIP3",
        "SH2B3",
        "GPR65",
        "MIF",
    ],
}

GENE_TO_CLASS = {gene: klass for klass, genes in CANDIDATE_CLASSES.items() for gene in genes}
TARGET_GENES = sorted(GENE_TO_CLASS)


def zscore(values: pd.Series) -> pd.Series:
    vals = pd.to_numeric(values, errors="coerce")
    sd = vals.std(ddof=0)
    if not np.isfinite(sd) or sd == 0:
        return pd.Series(np.zeros(len(vals)), index=vals.index, dtype=float)
    return (vals - vals.mean()) / sd


def residualize(y: np.ndarray, covariates: np.ndarray) -> np.ndarray:
    y = np.asarray(y, dtype=float)
    x = np.asarray(covariates, dtype=float)
    ok = np.isfinite(y) & np.isfinite(x).all(axis=1)
    resid = np.full_like(y, np.nan, dtype=float)
    if ok.sum() < x.shape[1] + 2:
        return resid
    design = np.column_stack([np.ones(ok.sum()), x[ok]])
    beta, *_ = np.linalg.lstsq(design, y[ok], rcond=None)
    resid[ok] = y[ok] - design @ beta
    return resid


def hedges_g(case: np.ndarray, control: np.ndarray) -> float:
    case = np.asarray(case, dtype=float)
    control = np.asarray(control, dtype=float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if case.size < 2 or control.size < 2:
        return np.nan
    pooled = ((case.size - 1) * case.var(ddof=1) + (control.size - 1) * control.var(ddof=1)) / (
        case.size + control.size - 2
    )
    if pooled <= 0:
        return np.nan
    correction = 1.0 - (3.0 / (4.0 * (case.size + control.size) - 9.0))
    return float(((case.mean() - control.mean()) / math.sqrt(pooled)) * correction)


def gene_symbols(a: ad.AnnData, symbol_column: str) -> pd.Series:
    if symbol_column in a.var.columns:
        return a.var[symbol_column].astype(str)
    if "feature_name" in a.var.columns:
        return a.var["feature_name"].astype(str)
    return pd.Series(a.var_names.astype(str), index=a.var_names)


def selected_gene_columns(a: ad.AnnData, symbol_column: str) -> dict[str, int]:
    symbol_to_first: dict[str, int] = {}
    for idx, symbol in enumerate(gene_symbols(a, symbol_column)):
        symbol_to_first.setdefault(str(symbol).upper(), idx)
    out: dict[str, int] = {}
    for gene in TARGET_GENES:
        idx = symbol_to_first.get(gene.upper())
        if idx is not None:
            out[gene] = idx
    return out


def read_counts(path: Path):
    a = ad.read_h5ad(path)
    x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
    return a, x


def donor_gene_scores(config) -> tuple[pd.DataFrame, pd.DataFrame]:
    a, x = read_counts(config.path)
    try:
        obs = a.obs.copy()
        mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
        obs_sub = obs.loc[mask].copy()
        cell_idx = np.flatnonzero(mask.to_numpy())
        gene_to_col = selected_gene_columns(a, config.gene_symbol_column)
        presence = pd.DataFrame(
            [
                {
                    "analysis": config.name,
                    "disease_name": config.disease_label,
                    "compartment": config.compartment,
                    "gene": gene,
                    "candidate_class": GENE_TO_CLASS[gene],
                    "present": gene in gene_to_col,
                }
                for gene in TARGET_GENES
            ]
        )
        if obs_sub.empty or not gene_to_col:
            return pd.DataFrame(), presence
        present = list(gene_to_col)
        target_x = x[cell_idx][:, [gene_to_col[g] for g in present]].astype(float)
        lib_size = np.asarray(x[cell_idx].sum(axis=1)).ravel().astype(float)
        lib_size[~np.isfinite(lib_size) | (lib_size <= 0)] = np.nan
        normalizer = np.divide(1.0, lib_size, out=np.zeros_like(lib_size), where=np.isfinite(lib_size))
        log_expr = np.log1p(target_x.multiply(normalizer[:, None]).multiply(1e4).toarray())
        rows = []
        grouped = obs_sub.reset_index(drop=True).groupby(["donor_id", "disease"], observed=True).groups
        for (donor, disease), indices in grouped.items():
            idx = np.fromiter(indices, dtype=int)
            if idx.size < 10:
                continue
            group = "case" if disease == config.disease_label else "control"
            for j, gene in enumerate(present):
                vals = log_expr[idx, j]
                rows.append(
                    {
                        "analysis": config.name,
                        "dataset_path": str(config.path.relative_to(ROOT)),
                        "disease_name": config.disease_label,
                        "compartment": config.compartment,
                        "role": config.role,
                        "donor_id": str(donor),
                        "disease": str(disease),
                        "group": group,
                        "gene": gene,
                        "candidate_class": GENE_TO_CLASS[gene],
                        "n_cells": int(idx.size),
                        "mean_log_norm": float(np.nanmean(vals)),
                        "detection_fraction": float(np.mean(vals > 0)),
                    }
                )
        return pd.DataFrame(rows), presence
    finally:
        a.file.close() if getattr(a, "isbacked", False) else None


def compare_groups(scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (analysis, gene), sub in scores.groupby(["analysis", "gene"], observed=True):
        first = sub.iloc[0]
        for metric in ("mean_log_norm", "detection_fraction"):
            case = pd.to_numeric(sub.loc[sub["group"] == "case", metric], errors="coerce").dropna().to_numpy(float)
            control = pd.to_numeric(sub.loc[sub["group"] == "control", metric], errors="coerce").dropna().to_numpy(float)
            if case.size >= 2 and control.size >= 2:
                t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "gene": gene,
                    "candidate_class": first["candidate_class"],
                    "metric": metric,
                    "n_case_donors": int(case.size),
                    "n_control_donors": int(control.size),
                    "mean_case": float(np.nanmean(case)) if case.size else np.nan,
                    "mean_control": float(np.nanmean(control)) if control.size else np.nan,
                    "delta_case_minus_control": float(np.nanmean(case) - np.nanmean(control)) if case.size and control.size else np.nan,
                    "hedges_g": hedges_g(case, control),
                    "welch_t": float(t_stat) if pd.notna(t_stat) else np.nan,
                    "p": float(p_value) if pd.notna(p_value) else np.nan,
                }
            )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["fdr"] = np.nan
    for analysis, idx in out.groupby("analysis", observed=True).groups.items():
        valid = out.loc[idx, "p"].notna()
        if valid.any():
            out.loc[out.loc[idx].index[valid], "fdr"] = multipletests(out.loc[out.loc[idx].index[valid], "p"], method="fdr_bh")[1]
    out["positive_fdr10"] = (out["delta_case_minus_control"] > 0) & (out["fdr"] <= 0.10)
    out["positive_trend"] = (out["delta_case_minus_control"] > 0) & (out["p"] <= 0.10)
    out["negative_trend"] = (out["delta_case_minus_control"] < 0) & (out["p"] <= 0.10)
    return out


def module_matrix() -> pd.DataFrame:
    mods = pd.read_csv(MODULE_SCORES, sep="\t")
    keep = set(STATE_MODULES) | {IFN_MODULE}
    mods = mods[mods["module"].isin(keep)].copy()
    mat = (
        mods.pivot_table(
            index=["analysis", "donor_id", "disease_name", "compartment", "group"],
            columns="module",
            values="mean_score",
            aggfunc="mean",
        )
        .reset_index()
        .rename_axis(None, axis=1)
    )
    for mod in STATE_MODULES + (IFN_MODULE,):
        if mod not in mat.columns:
            mat[mod] = np.nan
    mat["target_state"] = np.nan
    for analysis, idx in mat.groupby("analysis", observed=True).groups.items():
        sub = mat.loc[idx, list(STATE_MODULES)]
        mat.loc[idx, "target_state"] = sub.apply(zscore).mean(axis=1)
        mat.loc[idx, "ifn_z"] = zscore(mat.loc[idx, IFN_MODULE])
    mat["group_code"] = np.where(mat["group"].eq("case"), 1.0, 0.0)
    return mat


def residual_state_associations(scores: pd.DataFrame) -> pd.DataFrame:
    mods = module_matrix()
    rows = []
    for (analysis, gene), sub in scores.groupby(["analysis", "gene"], observed=True):
        first = sub.iloc[0]
        gf = sub[["analysis", "donor_id", "gene", "mean_log_norm", "detection_fraction"]].drop_duplicates()
        merged = gf.merge(mods, on=["analysis", "donor_id"], how="inner", suffixes=("", "_module"))
        for gene_metric in ("mean_log_norm", "detection_fraction"):
            ok = merged[[gene_metric, "target_state", "ifn_z", "group_code"]].replace([np.inf, -np.inf], np.nan).dropna()
            if len(ok) < 6 or ok[gene_metric].nunique() < 3 or ok["target_state"].nunique() < 3:
                raw_r = raw_p = resid_r = resid_p = np.nan
            else:
                raw = stats.spearmanr(ok[gene_metric], ok["target_state"])
                raw_r = float(raw.statistic)
                raw_p = float(raw.pvalue)
                cov = ok[["ifn_z", "group_code"]].to_numpy(float)
                gene_resid = residualize(ok[gene_metric].to_numpy(float), cov)
                state_resid = residualize(ok["target_state"].to_numpy(float), cov)
                resid_ok = np.isfinite(gene_resid) & np.isfinite(state_resid)
                if resid_ok.sum() < 6 or len(np.unique(gene_resid[resid_ok])) < 3 or len(np.unique(state_resid[resid_ok])) < 3:
                    resid_r = resid_p = np.nan
                else:
                    resid = stats.spearmanr(gene_resid[resid_ok], state_resid[resid_ok])
                    resid_r = float(resid.statistic)
                    resid_p = float(resid.pvalue)
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "gene": gene,
                    "candidate_class": first["candidate_class"],
                    "gene_metric": gene_metric,
                    "n_donors": int(len(ok)) if "ok" in locals() else 0,
                    "raw_spearman_r": raw_r,
                    "raw_spearman_p": raw_p,
                    "ifn_group_resid_spearman_r": resid_r,
                    "ifn_group_resid_spearman_p": resid_p,
                }
            )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["resid_positive_support"] = (out["ifn_group_resid_spearman_r"] >= 0.35) & (out["ifn_group_resid_spearman_p"] <= 0.10)
    out["raw_positive_support"] = (out["raw_spearman_r"] >= 0.50) & (out["raw_spearman_p"] <= 0.05)
    return out


def add_ms_signature(comps: pd.DataFrame) -> pd.DataFrame:
    if not MS_SIGNATURE.exists():
        return comps
    sig = pd.read_csv(MS_SIGNATURE, sep="\t")
    rows = []
    for gene in TARGET_GENES:
        hit = sig[sig["gene"].str.upper() == gene.upper()] if "gene" in sig.columns else pd.DataFrame()
        if hit.empty:
            continue
        row = hit.iloc[0]
        rows.append(
            {
                "analysis": "GSE111972_MS_WM_microglia",
                "disease_name": "MS",
                "compartment": "white matter microglia",
                "role": "ms_anchor",
                "gene": gene,
                "candidate_class": GENE_TO_CLASS[gene],
                "metric": "bulk_log2_expression",
                "n_case_donors": np.nan,
                "n_control_donors": np.nan,
                "mean_case": row.get("mean_case"),
                "mean_control": row.get("mean_control"),
                "delta_case_minus_control": row.get("delta_log2"),
                "hedges_g": row.get("hedges_g"),
                "welch_t": row.get("welch_t"),
                "p": row.get("p"),
                "fdr": row.get("fdr"),
                "positive_fdr10": bool(row.get("delta_log2", 0) > 0 and row.get("fdr", 1) <= 0.10),
                "positive_trend": bool(row.get("delta_log2", 0) > 0 and row.get("p", 1) <= 0.10),
                "negative_trend": bool(row.get("delta_log2", 0) < 0 and row.get("p", 1) <= 0.10),
            }
        )
    if rows:
        return pd.concat([comps, pd.DataFrame(rows)], ignore_index=True, sort=False)
    return comps


def summarize(comps: pd.DataFrame, assoc: pd.DataFrame) -> pd.DataFrame:
    rows = []
    genes = sorted(set(comps["gene"]) | set(assoc["gene"]))
    for gene in genes:
        c = comps[comps["gene"] == gene]
        a = assoc[assoc["gene"] == gene]
        expr_best = []
        expr_pos_diseases = set()
        expr_fdr_diseases = set()
        expr_neg_diseases = set()
        for disease, dsub in c.groupby("disease_name", observed=True):
            ranked = dsub.assign(
                score=np.select(
                    [dsub["positive_fdr10"], dsub["positive_trend"], dsub["negative_trend"]],
                    [3, 2, -1],
                    default=0,
                )
            )
            row = ranked.sort_values(["score", "hedges_g"], ascending=[False, False]).iloc[0]
            if bool(row.get("positive_fdr10", False)):
                expr_fdr_diseases.add(str(disease))
            if bool(row.get("positive_fdr10", False)) or bool(row.get("positive_trend", False)):
                expr_pos_diseases.add(str(disease))
            if bool(row.get("negative_trend", False)):
                expr_neg_diseases.add(str(disease))
            expr_best.append(row.to_dict())
        resid_pos_diseases = set()
        raw_pos_diseases = set()
        for disease, dsub in a.groupby("disease_name", observed=True):
            if dsub["resid_positive_support"].any():
                resid_pos_diseases.add(str(disease))
            if dsub["raw_positive_support"].any():
                raw_pos_diseases.add(str(disease))
        resid_r = pd.to_numeric(a["ifn_group_resid_spearman_r"], errors="coerce")
        raw_r = pd.to_numeric(a["raw_spearman_r"], errors="coerce")
        rows.append(
            {
                "gene": gene,
                "candidate_class": GENE_TO_CLASS.get(gene, "unknown"),
                "n_expression_diseases_tested": int(c["disease_name"].nunique()) if not c.empty else 0,
                "n_expr_fdr10_positive_diseases": len(expr_fdr_diseases),
                "n_expr_trend_or_better_diseases": len(expr_pos_diseases),
                "n_expr_negative_trend_diseases": len(expr_neg_diseases),
                "n_resid_state_support_diseases": len(resid_pos_diseases),
                "n_raw_state_support_diseases": len(raw_pos_diseases),
                "median_resid_spearman_r": float(resid_r.median()) if resid_r.notna().any() else np.nan,
                "median_raw_spearman_r": float(raw_r.median()) if raw_r.notna().any() else np.nan,
                "expression_supporting_diseases": ";".join(sorted(expr_pos_diseases)),
                "resid_state_supporting_diseases": ";".join(sorted(resid_pos_diseases)),
                "raw_state_supporting_diseases": ";".join(sorted(raw_pos_diseases)),
                "negative_diseases": ";".join(sorted(expr_neg_diseases)),
                "best_expression_details": json.dumps(expr_best),
            }
        )
    out = pd.DataFrame(rows)
    out["priority_score"] = (
        2.0 * out["n_expr_fdr10_positive_diseases"]
        + 1.0 * out["n_expr_trend_or_better_diseases"]
        + 1.5 * out["n_resid_state_support_diseases"]
        + 0.5 * out["n_raw_state_support_diseases"]
        - 0.75 * out["n_expr_negative_trend_diseases"]
    )
    return out.sort_values(
        [
            "priority_score",
            "n_resid_state_support_diseases",
            "n_expr_fdr10_positive_diseases",
            "n_expr_trend_or_better_diseases",
            "median_resid_spearman_r",
        ],
        ascending=[False, False, False, False, False],
    )


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    score_frames = []
    presence_frames = []
    run_log = []
    for config in CONFIGS:
        try:
            scores, presence = donor_gene_scores(config)
            score_frames.append(scores)
            presence_frames.append(presence)
            run_log.append({"analysis": config.name, "status": "completed", "n_rows": int(len(scores))})
        except Exception as exc:
            run_log.append({"analysis": config.name, "status": f"failed:{type(exc).__name__}:{exc}", "n_rows": 0})
    scores = pd.concat(score_frames, ignore_index=True) if score_frames else pd.DataFrame()
    presence = pd.concat(presence_frames, ignore_index=True) if presence_frames else pd.DataFrame()
    scores.to_csv(OUT / "donor_candidate_gene_scores.tsv", sep="\t", index=False)
    presence.to_csv(OUT / "candidate_gene_presence.tsv", sep="\t", index=False)
    pd.DataFrame(run_log).to_csv(OUT / "run_log.tsv", sep="\t", index=False)

    comps = compare_groups(scores) if not scores.empty else pd.DataFrame()
    comps = add_ms_signature(comps) if not comps.empty else comps
    comps.to_csv(OUT / "candidate_gene_case_control_comparisons.tsv", sep="\t", index=False)

    assoc = residual_state_associations(scores) if not scores.empty else pd.DataFrame()
    assoc.to_csv(OUT / "candidate_gene_state_residual_associations.tsv", sep="\t", index=False)

    summary = summarize(comps, assoc) if not comps.empty or not assoc.empty else pd.DataFrame()
    summary.to_csv(OUT / "candidate_dependency_priority_summary.tsv", sep="\t", index=False)

    top = summary.head(25).to_dict(orient="records") if not summary.empty else []
    result = {
        "seed": SEED,
        "run_log": run_log,
        "state_modules": STATE_MODULES,
        "ifn_covariate_module": IFN_MODULE,
        "n_candidate_genes": len(TARGET_GENES),
        "top_25": top,
        "interpretation": (
            "Prioritization scan for dependencies that track CD74/HLA-II state "
            "after IFN and group adjustment. Requires independent perturbation, "
            "genetics, druggability, and novelty before any therapeutic claim."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
