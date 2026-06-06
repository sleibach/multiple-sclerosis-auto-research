#!/usr/bin/env python3
"""Donor-level target-gene replication in direct h5ad autoimmune atlases.

This complements module scoring by asking whether individual target genes
(`IFI30`, `CTSS`, `CD74`, `CIITA`, etc.) are increased in disease compartments.
It reuses the exact dataset configs and normalization logic from
`v3_analyze_direct_h5ad_cell_states.py`.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse, stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import CONFIGS, ROOT, TARGET_GENES, get_gene_indices, hedges_g, read_counts

SEED = 20260526
OUT = ROOT / "phases/v3/results" / "direct_h5ad_gene_replication"


def donor_gene_scores(config, a, x) -> pd.DataFrame:
    obs = a.obs.copy()
    mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
    obs_sub = obs.loc[mask].copy()
    cell_idx = np.flatnonzero(mask.to_numpy())
    gene_idx = get_gene_indices(a, config.gene_symbol_column)
    present_genes = [g for g in TARGET_GENES if g in gene_idx]
    if len(obs_sub) == 0 or not present_genes:
        return pd.DataFrame()

    target_x = x[cell_idx][:, [gene_idx[g] for g in present_genes]].astype(float)
    lib_size = np.asarray(x[cell_idx].sum(axis=1)).ravel().astype(float)
    lib_size[~np.isfinite(lib_size) | (lib_size <= 0)] = np.nan
    normalized = target_x.multiply(np.divide(1.0, lib_size, out=np.zeros_like(lib_size), where=np.isfinite(lib_size))[:, None]).multiply(1e4)
    log_expr = np.log1p(normalized.toarray())
    normal_mask = obs_sub["disease"].eq(config.control_label).to_numpy()
    gene_mean = np.nanmean(log_expr[normal_mask], axis=0)
    gene_sd = np.nanstd(log_expr[normal_mask], axis=0, ddof=1)
    gene_sd[~np.isfinite(gene_sd) | (gene_sd < 1e-6)] = 1.0
    z = (log_expr - gene_mean) / gene_sd

    score_frame = obs_sub[["donor_id", "disease", "cell_type", "tissue"]].reset_index(drop=True).copy()
    rows = []
    for (donor, disease), sub_idx in score_frame.groupby(["donor_id", "disease"], observed=True).groups.items():
        idx = np.fromiter(sub_idx, dtype=int)
        if len(idx) < 10:
            continue
        for j, gene in enumerate(present_genes):
            vals = log_expr[idx, j]
            zvals = z[idx, j]
            rows.append(
                {
                    "analysis": config.name,
                    "dataset_path": str(config.path.relative_to(ROOT)),
                    "disease_name": config.disease_label,
                    "compartment": config.compartment,
                    "donor_id": donor,
                    "disease": disease,
                    "group": "case" if disease == config.disease_label else "control",
                    "gene": gene,
                    "n_cells": int(len(idx)),
                    "mean_log_norm": float(np.nanmean(vals)),
                    "mean_z_vs_controls": float(np.nanmean(zvals)),
                    "detection_fraction": float((vals > 0).mean()),
                    "cell_types": ",".join(sorted(score_frame.iloc[idx]["cell_type"].astype(str).unique())),
                }
            )
    return pd.DataFrame(rows)


def compare_scores(scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (analysis, gene), sub in scores.groupby(["analysis", "gene"], observed=True):
        for metric in ["mean_z_vs_controls", "detection_fraction"]:
            case = sub.loc[sub["group"] == "case", metric].to_numpy(float)
            control = sub.loc[sub["group"] == "control", metric].to_numpy(float)
            if len(case) >= 2 and len(control) >= 2:
                t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            first = sub.iloc[0]
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "gene": gene,
                    "metric": metric,
                    "n_case_donors": int(len(case)),
                    "n_control_donors": int(len(control)),
                    "mean_case": float(np.nanmean(case)) if len(case) else np.nan,
                    "mean_control": float(np.nanmean(control)) if len(control) else np.nan,
                    "delta_case_minus_control": float(np.nanmean(case) - np.nanmean(control)) if len(case) and len(control) else np.nan,
                    "hedges_g": hedges_g(case, control),
                    "welch_t": float(t_stat) if pd.notna(t_stat) else np.nan,
                    "p": float(p_value) if pd.notna(p_value) else np.nan,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
    return out


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    cache = {}
    score_tables = []
    run_log = []
    for config in CONFIGS:
        try:
            if config.path not in cache:
                cache[config.path] = read_counts(config.path)
            a, x = cache[config.path]
            scores = donor_gene_scores(config, a, x)
            score_tables.append(scores)
            run_log.append({"analysis": config.name, "status": "completed", "n_rows": int(len(scores))})
        except Exception as exc:
            run_log.append({"analysis": config.name, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})

    scores = pd.concat(score_tables, ignore_index=True) if score_tables else pd.DataFrame()
    comparisons = compare_scores(scores) if not scores.empty else pd.DataFrame()
    scores.to_csv(OUT / "direct_h5ad_gene_donor_scores.tsv", sep="\t", index=False)
    comparisons.to_csv(OUT / "direct_h5ad_gene_donor_comparisons.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "run_log": run_log,
        "top_positive_mean_z": (
            comparisons[
                (comparisons["metric"] == "mean_z_vs_controls")
                & (comparisons["delta_case_minus_control"] > 0)
            ]
            .sort_values(["fdr", "hedges_g"], ascending=[True, False])
            .head(40)
            .to_dict(orient="records")
            if not comparisons.empty
            else []
        ),
    }
    (OUT / "direct_h5ad_gene_replication_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
