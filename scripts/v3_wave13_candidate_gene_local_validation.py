#!/usr/bin/env python3
"""Local validation of wave-13 genetics/prior-art candidate genes.

This tests whether reopened genetics candidates such as GPR65 and the
SLC15A4/TASL/IRF5 branch have local cell-state recurrence in the available
direct h5ad atlases. It is an expression recurrence screen, not causal
inference.
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
OUT = ROOT / "phases/v3/results" / "wave13_candidate_gene_local_validation"
MS_SIGNATURE = ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv"

CANDIDATE_GENES = [
    "GPR65",
    "SLC15A4",
    "TASL",
    "CXorf21",
    "IRF5",
    "TNFAIP3",
    "PTPN2",
    "CLEC16A",
    "SH2B3",
    "IL10",
    "OSMR",
    "IL6R",
    "ATG16L1",
    "CARD9",
    "MERTK",
    "AXL",
    "CFB",
    "CFH",
    "P2RX7",
    "NLRP3",
    "CTSS",
    "CD74",
    "CIITA",
    "RFX5",
]


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


def gene_indices(a, symbol_column: str) -> dict[str, int]:
    if symbol_column in a.var.columns:
        symbols = a.var[symbol_column].astype(str)
    elif "feature_name" in a.var.columns:
        symbols = a.var["feature_name"].astype(str)
    else:
        symbols = pd.Series(a.var_names.astype(str), index=a.var.index)
    mapping: dict[str, int] = {}
    aliases = {"TASL": "CXorf21"}
    wanted = set(CANDIDATE_GENES) | set(aliases.values())
    for idx, raw in enumerate(symbols):
        symbol = str(raw).strip()
        if symbol in wanted and symbol not in mapping:
            mapping[symbol] = idx
    if "CXorf21" in mapping and "TASL" not in mapping:
        mapping["TASL"] = mapping["CXorf21"]
    return mapping


def analyze_config(config) -> tuple[pd.DataFrame, pd.DataFrame]:
    a = ad.read_h5ad(config.path)
    x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
    obs = a.obs.copy()
    mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
    obs_sub = obs.loc[mask].copy()
    cell_idx = np.flatnonzero(mask.to_numpy())
    idx = gene_indices(a, config.gene_symbol_column)
    present = [gene for gene in CANDIDATE_GENES if gene in idx]
    if len(obs_sub) == 0 or not present:
        return pd.DataFrame(), pd.DataFrame(
            [{"analysis": config.name, "status": "no_cells_or_no_genes", "present_genes": ",".join(present)}]
        )
    target_x = x[cell_idx][:, [idx[gene] for gene in present]].astype(float)
    lib = np.asarray(x[cell_idx].sum(axis=1)).ravel().astype(float)
    lib[~np.isfinite(lib) | (lib <= 0)] = np.nan
    normalized = target_x.multiply(np.divide(1.0, lib, out=np.zeros_like(lib), where=np.isfinite(lib))[:, None]).multiply(1e4)
    log_expr = np.log1p(normalized.toarray())
    cell_meta = obs_sub[["donor_id", "disease", "cell_type"]].reset_index(drop=True).copy()
    rows = []
    for (donor, disease), group_idx in cell_meta.groupby(["donor_id", "disease"], observed=True).groups.items():
        group_idx = np.fromiter(group_idx, dtype=int)
        if len(group_idx) < 10:
            continue
        for j, gene in enumerate(present):
            vals = log_expr[group_idx, j]
            rows.append(
                {
                    "analysis": config.name,
                    "dataset_path": str(config.path.relative_to(ROOT)),
                    "disease_name": config.disease_label,
                    "compartment": config.compartment,
                    "role": config.role,
                    "donor_id": donor,
                    "disease": disease,
                    "group": "case" if disease == config.disease_label else "control",
                    "gene": gene,
                    "n_cells": int(len(group_idx)),
                    "mean_log_norm": float(np.nanmean(vals)),
                    "detection_fraction": float((vals > 0).mean()),
                    "cell_types": ",".join(sorted(cell_meta.iloc[group_idx]["cell_type"].astype(str).unique())),
                }
            )
    run = pd.DataFrame(
        [{"analysis": config.name, "status": "completed", "n_rows": len(rows), "present_genes": ",".join(present)}]
    )
    return pd.DataFrame(rows), run


def compare(scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (analysis, gene), sub in scores.groupby(["analysis", "gene"], observed=True):
        for metric in ["mean_log_norm", "detection_fraction"]:
            case = sub.loc[sub["group"].eq("case"), metric].to_numpy(float)
            control = sub.loc[sub["group"].eq("control"), metric].to_numpy(float)
            if case.size >= 2 and control.size >= 2:
                t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            first = sub.iloc[0]
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "gene": gene,
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
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
    return out


def ms_rows() -> pd.DataFrame:
    if not MS_SIGNATURE.exists():
        return pd.DataFrame()
    df = pd.read_csv(MS_SIGNATURE, sep="\t")
    gene_col = "gene" if "gene" in df.columns else "feature"
    rows = []
    for gene in CANDIDATE_GENES:
        sub = df[df[gene_col].astype(str).eq(gene)]
        if sub.empty and gene == "TASL":
            sub = df[df[gene_col].astype(str).eq("CXorf21")]
        if sub.empty:
            continue
        row = sub.iloc[0]
        delta = row.get("delta_log2", row.get("delta_log2_cpm", np.nan))
        effect = row.get("hedges_g", np.nan)
        p = row.get("p", np.nan)
        fdr = row.get("fdr", np.nan)
        rows.append(
            {
                "analysis": "GSE111972_MS_WM_microglia",
                "disease_name": "MS",
                "compartment": "white matter microglia",
                "role": "myeloid_apc",
                "gene": gene,
                "metric": "bulk_log2_expression",
                "n_case_donors": row.get("n_case", np.nan),
                "n_control_donors": row.get("n_control", np.nan),
                "mean_case": np.nan,
                "mean_control": np.nan,
                "delta_case_minus_control": float(delta) if pd.notna(delta) else np.nan,
                "hedges_g": float(effect) if pd.notna(effect) else np.nan,
                "welch_t": np.nan,
                "p": float(p) if pd.notna(p) else np.nan,
                "fdr": float(fdr) if pd.notna(fdr) else np.nan,
            }
        )
    return pd.DataFrame(rows)


def level(delta: float, p: float, fdr: float) -> str:
    if not np.isfinite(delta):
        return "missing"
    if delta < 0 and np.isfinite(p) and p <= 0.10:
        return "negative_trend"
    if delta <= 0:
        return "null_or_negative"
    if np.isfinite(fdr) and fdr <= 0.10:
        return "fdr10_positive"
    if np.isfinite(p) and p <= 0.10:
        return "trend_positive"
    return "positive_null"


def summarize(comparisons: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if comparisons.empty:
        return pd.DataFrame()
    work = comparisons.copy()
    work["support_level"] = [
        level(d, p, f) for d, p, f in zip(work["delta_case_minus_control"], work["p"], work["fdr"])
    ]
    score_map = {"fdr10_positive": 2.0, "trend_positive": 1.0, "positive_null": 0.25, "null_or_negative": 0.0, "negative_trend": -1.0}
    work["support_score"] = work["support_level"].map(score_map).fillna(0.0)
    best = work.sort_values("support_score", ascending=False).groupby(["gene", "disease_name"], as_index=False).first()
    for gene, sub in best.groupby("gene", observed=True):
        pos = sub[sub["support_level"].isin(["fdr10_positive", "trend_positive"])]
        neg = sub[sub["support_level"].eq("negative_trend")]
        rows.append(
            {
                "gene": gene,
                "n_diseases_tested": int(sub["disease_name"].nunique()),
                "n_fdr10_positive_diseases": int((sub["support_level"] == "fdr10_positive").sum()),
                "n_trend_or_better_diseases": int(sub["support_level"].isin(["fdr10_positive", "trend_positive"]).sum()),
                "n_negative_trend_diseases": int(len(neg)),
                "median_positive_hedges_g": float(pos["hedges_g"].median()) if not pos.empty else np.nan,
                "supporting_diseases": ";".join(pos["disease_name"].tolist()),
                "negative_diseases": ";".join(neg["disease_name"].tolist()),
                "best_details": json.dumps(
                    sub.sort_values("support_score", ascending=False)[
                        ["disease_name", "analysis", "compartment", "metric", "delta_case_minus_control", "hedges_g", "p", "fdr", "support_level"]
                    ]
                    .to_dict(orient="records")
                ),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["n_fdr10_positive_diseases", "n_trend_or_better_diseases", "n_negative_trend_diseases", "median_positive_hedges_g"],
        ascending=[False, False, True, False],
    )


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    score_tables = []
    run_tables = []
    cache = {}
    for config in CONFIGS:
        try:
            scores, run = analyze_config(config)
            score_tables.append(scores)
            run_tables.append(run)
        except Exception as exc:
            run_tables.append(pd.DataFrame([{"analysis": config.name, "status": "failed", "error": f"{type(exc).__name__}: {exc}"}]))
    scores = pd.concat(score_tables, ignore_index=True) if score_tables else pd.DataFrame()
    comparisons = compare(scores) if not scores.empty else pd.DataFrame()
    ms = ms_rows()
    combined = pd.concat([comparisons, ms], ignore_index=True, sort=False) if not ms.empty else comparisons
    summary = summarize(combined)
    pd.concat(run_tables, ignore_index=True).to_csv(OUT / "wave13_candidate_gene_run_log.tsv", sep="\t", index=False)
    scores.to_csv(OUT / "wave13_candidate_gene_donor_scores.tsv", sep="\t", index=False)
    comparisons.to_csv(OUT / "wave13_candidate_gene_direct_h5ad_comparisons.tsv", sep="\t", index=False)
    combined.to_csv(OUT / "wave13_candidate_gene_combined_comparisons.tsv", sep="\t", index=False)
    summary.to_csv(OUT / "wave13_candidate_gene_summary.tsv", sep="\t", index=False)
    out = {
        "random_seed": SEED,
        "candidate_genes": CANDIDATE_GENES,
        "n_direct_donor_rows": int(len(scores)),
        "n_combined_comparison_rows": int(len(combined)),
        "top_summary": summary.head(20).to_dict(orient="records") if not summary.empty else [],
        "guardrail": "Expression recurrence screen; OpenTargets genetics and prior art remain separate evidence channels.",
    }
    (OUT / "wave13_candidate_gene_summary.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
