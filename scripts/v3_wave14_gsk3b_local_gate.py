#!/usr/bin/env python3
"""Local recurrence and novelty gate for the GSK3B/CIITA scout.

The perturbation scout found `Gsk3b` KO can preferentially reduce
IFN-gamma-induced CIITA/MHC-II/CD74 in mouse macrophages. This script asks
whether `GSK3B` itself has cross-autoimmune local recurrence, whether it tracks
the IFN/HLA/CD74 state in donor-level data, and how crowded the public
autoimmune literature/trial space is.

This is a veto/gate analysis, not a therapeutic claim.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from urllib.parse import quote_plus

import anndata as ad
import numpy as np
import pandas as pd
import requests
from scipy import sparse, stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_osmr_complement_axes import CONFIGS, ROOT

OUT = ROOT / "results_v3" / "wave14_gsk3b_local_gate"
MS_SIGNATURE = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
MODULE_SCORES = ROOT / "results_v3" / "direct_h5ad_cell_state" / "direct_h5ad_donor_module_scores.tsv"

GENE_ALIASES = {
    "GSK3B": ("GSK3B",),
    "GSK3A": ("GSK3A",),
    "MED16": ("MED16",),
    "CIITA": ("CIITA",),
    "RFX5": ("RFX5",),
    "CD74": ("CD74",),
}

MODULES_FOR_CORR = ["ifn_apc", "hla_ii_apc", "mif_cd74_receptor_state", "mixscale_validated_ifng_readout"]


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


def compare(case: pd.Series, control: pd.Series) -> dict[str, float]:
    case = pd.to_numeric(case, errors="coerce").dropna().to_numpy(dtype=float)
    control = pd.to_numeric(control, errors="coerce").dropna().to_numpy(dtype=float)
    if case.size >= 2 and control.size >= 2:
        t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
    else:
        t_stat, p_value = np.nan, np.nan
    return {
        "n_case_donors": int(case.size),
        "n_control_donors": int(control.size),
        "mean_case": float(np.nanmean(case)) if case.size else np.nan,
        "mean_control": float(np.nanmean(control)) if control.size else np.nan,
        "delta_case_minus_control": float(np.nanmean(case) - np.nanmean(control)) if case.size and control.size else np.nan,
        "hedges_g": hedges_g(case, control),
        "welch_t": float(t_stat) if pd.notna(t_stat) else np.nan,
        "p": float(p_value) if pd.notna(p_value) else np.nan,
    }


def support_level(delta: float, p_value: float, fdr: float) -> str:
    if not np.isfinite(delta):
        return "missing"
    if delta < 0 and np.isfinite(p_value) and p_value <= 0.10:
        return "negative_trend"
    if delta <= 0:
        return "null_or_negative"
    if np.isfinite(fdr) and fdr <= 0.10:
        return "fdr10_positive"
    if np.isfinite(p_value) and p_value <= 0.10:
        return "trend_positive"
    return "positive_null"


def gene_symbol_series(a: ad.AnnData, symbol_column: str) -> pd.Series:
    if symbol_column in a.var.columns:
        return a.var[symbol_column].astype(str)
    if "feature_name" in a.var.columns:
        return a.var["feature_name"].astype(str)
    return pd.Series(a.var_names.astype(str), index=a.var_names)


def selected_gene_columns(a: ad.AnnData, symbol_column: str) -> dict[str, int]:
    symbol_to_first: dict[str, int] = {}
    for idx, symbol in enumerate(gene_symbol_series(a, symbol_column)):
        key = str(symbol).upper()
        symbol_to_first.setdefault(key, idx)
    mapping: dict[str, int] = {}
    for gene, aliases in GENE_ALIASES.items():
        for alias in aliases:
            idx = symbol_to_first.get(alias.upper())
            if idx is not None:
                mapping[gene] = idx
                break
    return mapping


def read_counts(path: Path):
    a = ad.read_h5ad(path)
    x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
    return a, x


def analyze_config(config) -> tuple[pd.DataFrame, pd.DataFrame]:
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
                    "role": config.role,
                    "gene": gene,
                    "present": gene in gene_to_col,
                }
                for gene in GENE_ALIASES
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
        for (donor, disease), indices in obs_sub.reset_index(drop=True).groupby(["donor_id", "disease"], observed=True).groups.items():
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
                        "donor_id": donor,
                        "disease": disease,
                        "group": group,
                        "gene": gene,
                        "n_cells": int(idx.size),
                        "mean_log_norm": float(np.nanmean(vals)),
                        "detection_fraction": float(np.mean(vals > 0)),
                    }
                )
        return pd.DataFrame(rows), presence
    finally:
        a.file.close() if getattr(a, "isbacked", False) else None


def summarize_gene(comparisons: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gene, sub in comparisons.groupby("gene", observed=True):
        best = []
        support = set()
        negative = set()
        fdr10 = set()
        trend = set()
        for disease, dsub in sub.groupby("disease_name", observed=True):
            ranked = dsub.assign(score=dsub["support_level"].map({"fdr10_positive": 3, "trend_positive": 2, "positive_null": 1, "null_or_negative": 0, "negative_trend": -1, "missing": -2}).fillna(0))
            row = ranked.sort_values(["score", "hedges_g"], ascending=[False, False]).iloc[0]
            if row["support_level"] == "fdr10_positive":
                fdr10.add(str(disease))
            if row["support_level"] in {"fdr10_positive", "trend_positive"}:
                trend.add(str(disease))
                support.add(str(disease))
            elif row["support_level"] == "negative_trend":
                negative.add(str(disease))
            best.append(row.to_dict())
        positives = [float(x["hedges_g"]) for x in best if x.get("support_level") in {"fdr10_positive", "trend_positive"} and pd.notna(x.get("hedges_g"))]
        rows.append(
            {
                "gene": gene,
                "n_diseases_tested": int(sub["disease_name"].nunique()),
                "n_fdr10_positive_diseases": len(fdr10),
                "n_trend_or_better_diseases": len(trend),
                "n_negative_trend_diseases": len(negative),
                "median_positive_hedges_g": float(np.median(positives)) if positives else np.nan,
                "supporting_diseases": ";".join(sorted(support)),
                "negative_diseases": ";".join(sorted(negative)),
                "best_details": json.dumps(best),
            }
        )
    return pd.DataFrame(rows).sort_values(["n_fdr10_positive_diseases", "n_trend_or_better_diseases", "median_positive_hedges_g"], ascending=[False, False, False])


def add_ms_signature(comparisons: pd.DataFrame) -> pd.DataFrame:
    if not MS_SIGNATURE.exists():
        return comparisons
    sig = pd.read_csv(MS_SIGNATURE, sep="\t")
    rows = []
    for gene in GENE_ALIASES:
        hit = sig[sig["gene"] == gene]
        if hit.empty:
            continue
        row = hit.iloc[0]
        for metric in ["bulk_log2_expression"]:
            rows.append(
                {
                    "analysis": "GSE111972_MS_WM_microglia",
                    "disease_name": "MS",
                    "compartment": "white matter microglia",
                    "role": "ms_anchor",
                    "gene": gene,
                    "metric": metric,
                    "n_case_donors": np.nan,
                    "n_control_donors": np.nan,
                    "mean_case": row.get("mean_case"),
                    "mean_control": row.get("mean_control"),
                    "delta_case_minus_control": row.get("delta_log2"),
                    "hedges_g": row.get("hedges_g"),
                    "welch_t": row.get("welch_t"),
                    "p": row.get("p"),
                    "fdr": row.get("fdr"),
                }
            )
    if rows:
        add = pd.DataFrame(rows)
        add["support_level"] = [
            support_level(float(r["delta_case_minus_control"]), float(r["p"]), float(r["fdr"]))
            for _, r in add.iterrows()
        ]
        return pd.concat([comparisons, add], ignore_index=True, sort=False)
    return comparisons


def correlations(gene_scores: pd.DataFrame) -> pd.DataFrame:
    if not MODULE_SCORES.exists():
        return pd.DataFrame()
    mods = pd.read_csv(MODULE_SCORES, sep="\t")
    mods = mods[mods["module"].isin(MODULES_FOR_CORR)]
    rows = []
    for analysis, gsub in gene_scores.groupby("analysis", observed=True):
        msub = mods[mods["analysis"] == analysis]
        for gene, gg in gsub.groupby("gene", observed=True):
            gf = gg[["donor_id", "group", "mean_log_norm", "detection_fraction"]].drop_duplicates()
            for module, mm in msub.groupby("module", observed=True):
                mf = mm[["donor_id", "mean_score", "high_fraction"]].drop_duplicates()
                merged = gf.merge(mf, on="donor_id", how="inner")
                for gene_metric in ["mean_log_norm", "detection_fraction"]:
                    for module_metric in ["mean_score", "high_fraction"]:
                        ok = merged[[gene_metric, module_metric]].replace([np.inf, -np.inf], np.nan).dropna()
                        if len(ok) < 5 or ok[gene_metric].nunique() < 3 or ok[module_metric].nunique() < 3:
                            rho = np.nan
                            p = np.nan
                        else:
                            res = stats.spearmanr(ok[gene_metric], ok[module_metric])
                            rho = float(res.statistic)
                            p = float(res.pvalue)
                        rows.append(
                            {
                                "analysis": analysis,
                                "gene": gene,
                                "module": module,
                                "gene_metric": gene_metric,
                                "module_metric": module_metric,
                                "n": int(len(ok)),
                                "spearman_r": rho,
                                "spearman_p": p,
                            }
                        )
    return pd.DataFrame(rows)


def europepmc_count(query: str) -> dict[str, object]:
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {"query": query, "format": "json", "pageSize": 5, "resultType": "lite"}
    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as exc:
        return {
            "query": query,
            "hit_count": None,
            "examples": [],
            "error": f"{type(exc).__name__}: {exc}",
            "url": f"https://europepmc.org/search?query={quote_plus(query)}",
        }
    examples = [
        {
            "id": item.get("id"),
            "source": item.get("source"),
            "title": item.get("title"),
            "journal": item.get("journalTitle"),
            "year": item.get("pubYear"),
            "doi": item.get("doi"),
        }
        for item in data.get("resultList", {}).get("result", [])
    ]
    return {"query": query, "hit_count": int(data.get("hitCount", 0)), "examples": examples, "url": f"https://europepmc.org/search?query={quote_plus(query)}"}


def clinical_trials(term: str) -> dict[str, object]:
    url = "https://clinicaltrials.gov/api/v2/studies"
    try:
        r = requests.get(url, params={"query.term": term, "pageSize": 10, "format": "json"}, timeout=30)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as exc:
        return {
            "term": term,
            "hit_count": None,
            "studies": [],
            "error": f"{type(exc).__name__}: {exc}",
            "url": f"https://clinicaltrials.gov/search?term={quote_plus(term)}",
        }
    studies = []
    for st in data.get("studies", []):
        p = st.get("protocolSection", {})
        studies.append(
            {
                "nct_id": p.get("identificationModule", {}).get("nctId"),
                "title": p.get("identificationModule", {}).get("briefTitle"),
                "status": p.get("statusModule", {}).get("overallStatus"),
                "conditions": ";".join(p.get("conditionsModule", {}).get("conditions", [])),
                "interventions": ";".join(i.get("name", "") for i in p.get("armsInterventionsModule", {}).get("interventions", [])),
            }
        )
    return {"term": term, "hit_count": len(studies), "studies": studies, "url": f"https://clinicaltrials.gov/search?term={quote_plus(term)}"}


def prior_art() -> dict[str, object]:
    queries = {
        "gsk3b_autoimmune": '("GSK3B" OR "GSK-3 beta" OR "glycogen synthase kinase 3 beta") AND (autoimmune OR "multiple sclerosis" OR lupus OR psoriasis OR Crohn OR "rheumatoid arthritis")',
        "gsk3_inhibitor_autoimmune": '("GSK3 inhibitor" OR "GSK-3 inhibitor" OR lithium OR tideglusib) AND (autoimmune OR "multiple sclerosis" OR lupus OR psoriasis OR Crohn OR "rheumatoid arthritis")',
        "gsk3b_ciita_mhcii": '("GSK3B" OR "GSK-3 beta") AND (CIITA OR "MHC class II" OR CD74 OR HLA)',
    }
    out: dict[str, object] = {"europepmc": {}, "clinical_trials": {}}
    for key, query in queries.items():
        out["europepmc"][key] = europepmc_count(query)
        time.sleep(0.3)
    for key, term in {
        "gsk3_autoimmune": "GSK3 autoimmune",
        "lithium_multiple_sclerosis": "lithium multiple sclerosis",
        "tideglusib_autoimmune": "tideglusib autoimmune",
    }.items():
        out["clinical_trials"][key] = clinical_trials(term)
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    all_scores = []
    presence = []
    run_log = []
    for config in CONFIGS:
        try:
            scores, pres = analyze_config(config)
            all_scores.append(scores)
            presence.append(pres)
            run_log.append({"analysis": config.name, "status": "completed", "n_rows": int(len(scores))})
        except Exception as exc:
            run_log.append({"analysis": config.name, "status": f"failed:{type(exc).__name__}:{exc}", "n_rows": 0})
    scores = pd.concat(all_scores, ignore_index=True) if all_scores else pd.DataFrame()
    pres = pd.concat(presence, ignore_index=True) if presence else pd.DataFrame()
    scores.to_csv(OUT / "gsk3b_local_gate_donor_scores.tsv", sep="\t", index=False)
    pres.to_csv(OUT / "gsk3b_local_gate_gene_presence.tsv", sep="\t", index=False)
    pd.DataFrame(run_log).to_csv(OUT / "run_log.tsv", sep="\t", index=False)

    comparison_rows = []
    for (analysis, gene), sub in scores.groupby(["analysis", "gene"], observed=True):
        first = sub.iloc[0]
        for metric in ["mean_log_norm", "detection_fraction"]:
            vals = compare(sub.loc[sub["group"] == "case", metric], sub.loc[sub["group"] == "control", metric])
            comparison_rows.append(
                {
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "gene": gene,
                    "metric": metric,
                    **vals,
                }
            )
    comps = pd.DataFrame(comparison_rows)
    if not comps.empty:
        comps["fdr"] = np.nan
        for analysis, idx in comps.groupby("analysis", observed=True).groups.items():
            valid = comps.loc[idx, "p"].notna()
            if valid.any():
                comps.loc[comps.loc[idx].index[valid], "fdr"] = multipletests(comps.loc[comps.loc[idx].index[valid], "p"], method="fdr_bh")[1]
        comps["support_level"] = [
            support_level(float(r["delta_case_minus_control"]), float(r["p"]) if pd.notna(r["p"]) else np.nan, float(r["fdr"]) if pd.notna(r["fdr"]) else np.nan)
            for _, r in comps.iterrows()
        ]
    comps = add_ms_signature(comps)
    comps.to_csv(OUT / "gsk3b_local_gate_comparisons.tsv", sep="\t", index=False)
    gene_summary = summarize_gene(comps) if not comps.empty else pd.DataFrame()
    gene_summary.to_csv(OUT / "gsk3b_local_gate_gene_summary.tsv", sep="\t", index=False)

    corr = correlations(scores)
    corr.to_csv(OUT / "gsk3b_local_gate_module_correlations.tsv", sep="\t", index=False)
    corr_summary = (
        corr.groupby("gene", observed=True)
        .agg(
            n_tests=("spearman_r", "size"),
            median_spearman_r=("spearman_r", "median"),
            n_positive_r_gt_0_5=("spearman_r", lambda s: int((s > 0.5).sum())),
            n_negative_r_lt_minus_0_5=("spearman_r", lambda s: int((s < -0.5).sum())),
        )
        .reset_index()
        if not corr.empty
        else pd.DataFrame()
    )
    corr_summary.to_csv(OUT / "gsk3b_local_gate_correlation_summary.tsv", sep="\t", index=False)

    pa = prior_art()
    (OUT / "gsk3b_prior_art_detail.json").write_text(json.dumps(pa, indent=2) + "\n")
    summary = {
        "run_log": run_log,
        "gene_summary": gene_summary.to_dict(orient="records"),
        "correlation_summary": corr_summary.to_dict(orient="records"),
        "prior_art_hit_counts": {
            "europepmc": {k: v["hit_count"] for k, v in pa["europepmc"].items()},
            "clinical_trials": {k: v["hit_count"] for k, v in pa["clinical_trials"].items()},
        },
        "interpretation": (
            "GSK3B local recurrence and prior-art gate for the perturbation scout. "
            "Positive perturbation evidence alone is insufficient if cross-disease expression/genetics/novelty fail."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
