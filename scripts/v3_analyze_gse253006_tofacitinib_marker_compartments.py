#!/usr/bin/env python3
"""Marker-compartment GSE253006 UC tofacitinib response analysis.

The first GSE253006 script used all-cell sample-level scores because GEO did not
provide cell annotations. This script is the stronger reformulation: classify
cells into transparent marker-derived compartments, score V3 modules within
each compartment, and test whether baseline responders differ from
non-responders.

Guardrail: compartments are marker-derived, not curated cell labels.
"""

from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import io, stats
from sklearn.metrics import roc_auc_score
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import MODULES, ROOT
from v3_analyze_gse253006_tofacitinib_uc import parse_soft_metadata

SEED = 20260526
RAW = ROOT / "data" / "raw_v3" / "gse253006"
MATRIX_DIR = RAW / "raw"
OUT = ROOT / "phases/v3/results" / "gse253006_tofacitinib_marker"

MARKER_SETS = {
    "epithelial_like": ["EPCAM", "KRT8", "KRT18", "KRT19", "VIL1", "MUC2", "TFF3", "FABP1"],
    "myeloid_apc_like": ["LYZ", "LST1", "CD14", "FCGR3A", "ITGAX", "CST3", "HLA-DRA", "CD74", "MS4A7"],
    "t_cell_like": ["CD3D", "CD3E", "CD3G", "TRAC", "CD4", "CD8A", "CD8B", "NKG7", "GZMA"],
    "b_plasma_like": ["MS4A1", "CD79A", "CD79B", "CD74", "MZB1", "JCHAIN", "IGHG1"],
    "stromal_endothelial_like": ["COL1A1", "COL1A2", "DCN", "LUM", "PECAM1", "VWF", "CLDN5", "ACTA2"],
}

EXTRA_MODULES = {
    "published_nonresponse_macrophage_inflammation": [
        "IL1B",
        "IL6",
        "CXCL1",
        "CXCL8",
        "S100A9",
        "MMP9",
        "MMP12",
        "FCGR3A",
    ],
    "tofacitinib_responder_baseline_jakstat": [
        "STAT1",
        "STAT2",
        "IRF1",
        "IRF7",
        "JAK1",
        "JAK2",
        "TYK2",
        "CXCL10",
        "GBP1",
        "NLRC5",
    ],
}

ALL_MODULES = {**MODULES, **EXTRA_MODULES}
TARGET_GENES = sorted({gene for genes in ALL_MODULES.values() for gene in genes})
MARKER_GENES = sorted({gene for genes in MARKER_SETS.values() for gene in genes})
ALL_GENES = sorted(set(TARGET_GENES) | set(MARKER_GENES))


def read_features(path: Path) -> pd.DataFrame:
    rows = []
    with gzip.open(path, "rt") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                rows.append({"gene_id": parts[0], "gene_symbol": parts[1]})
    out = pd.DataFrame(rows)
    out["row_index"] = np.arange(out.shape[0])
    return out


def selected_log_expression(prefix: str) -> tuple[pd.DataFrame, np.ndarray, list[str]]:
    features_path = MATRIX_DIR / f"{prefix}_features.tsv.gz"
    matrix_path = MATRIX_DIR / f"{prefix}_matrix.mtx.gz"
    barcodes_path = MATRIX_DIR / f"{prefix}_barcodes.tsv.gz"
    missing = [p for p in [features_path, matrix_path, barcodes_path] if not p.exists() or p.stat().st_size == 0]
    if missing:
        raise FileNotFoundError("missing sample files: " + ", ".join(str(p) for p in missing))

    features = read_features(features_path)
    row_to_gene: dict[int, str] = {}
    for gene in ALL_GENES:
        hits = features.loc[features["gene_symbol"].eq(gene), "row_index"]
        if not hits.empty:
            row_to_gene[int(hits.iloc[0])] = gene
    rows = sorted(row_to_gene)
    genes = [row_to_gene[i] for i in rows]
    with gzip.open(barcodes_path, "rt") as handle:
        barcodes = [line.strip() for line in handle if line.strip()]

    mat = io.mmread(str(matrix_path)).tocsc().astype(float)
    if mat.shape[0] != len(features) and mat.shape[1] == len(features):
        mat = mat.T.tocsc()
    if mat.shape[0] != len(features):
        raise ValueError(f"unexpected matrix/features shape for {prefix}: {mat.shape}, {len(features)}")
    if mat.shape[1] != len(barcodes):
        raise ValueError(f"barcode count mismatch for {prefix}: {mat.shape[1]} vs {len(barcodes)}")

    lib = np.asarray(mat.sum(axis=0)).ravel()
    valid = np.isfinite(lib) & (lib > 0)
    lib_safe = lib.copy()
    lib_safe[~valid] = np.nan
    selected = mat[rows, :].T.tocsr()
    norm = selected.multiply(np.divide(1.0, lib_safe, out=np.zeros_like(lib_safe), where=np.isfinite(lib_safe))[:, None]).multiply(1e4)
    log_expr = np.log1p(norm.toarray()).astype(np.float32)
    obs = pd.DataFrame({"sample_prefix": prefix, "barcode": barcodes, "n_counts": lib})
    return obs, log_expr, genes


def classify(obs: pd.DataFrame, expr: np.ndarray, genes: list[str]) -> pd.DataFrame:
    gene_to_idx = {gene: i for i, gene in enumerate(genes)}
    scores = {}
    for compartment, markers in MARKER_SETS.items():
        present = [g for g in markers if g in gene_to_idx]
        scores[compartment] = (
            np.nanmean(expr[:, [gene_to_idx[g] for g in present]], axis=1)
            if present
            else np.full(expr.shape[0], np.nan)
        )
    score_df = pd.DataFrame(scores)
    vals = score_df.to_numpy(float)
    order = np.argsort(np.nan_to_num(vals, nan=-np.inf), axis=1)
    top = order[:, -1]
    second = order[:, -2]
    top_score = vals[np.arange(vals.shape[0]), top]
    second_score = vals[np.arange(vals.shape[0]), second]
    compartments = np.array(score_df.columns)[top].astype(object)
    ambiguous = (~np.isfinite(top_score)) | (top_score < 0.20) | ((top_score - second_score) < 0.05)
    compartments[ambiguous] = "ambiguous"
    out = obs.copy()
    for col in score_df:
        out[f"marker_{col}"] = score_df[col].to_numpy(float)
    out["marker_compartment"] = compartments
    out["marker_top_score"] = top_score
    out["marker_margin"] = top_score - second_score
    return out


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled = ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    if pooled <= 0:
        return np.nan
    correction = 1.0 - 3.0 / (4.0 * (len(a) + len(b)) - 9.0)
    return float(((a.mean() - b.mean()) / math.sqrt(pooled)) * correction)


def auc_safe(labels: np.ndarray, scores: np.ndarray) -> float:
    mask = np.isfinite(scores)
    if mask.sum() < 4 or len(set(labels[mask])) < 2:
        return np.nan
    return float(roc_auc_score(labels[mask], scores[mask]))


def compare_baseline(donor_scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    base = donor_scores[donor_scores["timepoint_norm"].eq("W0")].copy()
    for (compartment, module), sub in base.groupby(["marker_compartment", "module"], observed=True):
        if compartment == "ambiguous":
            continue
        for metric in ["mean_score", "high_fraction"]:
            resp = sub.loc[sub["responder"], metric].to_numpy(float)
            non = sub.loc[~sub["responder"], metric].to_numpy(float)
            if len(resp) >= 2 and len(non) >= 2:
                t_stat, p_value = stats.ttest_ind(resp, non, equal_var=False, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            labels = sub["responder"].astype(int).to_numpy()
            scores = sub[metric].to_numpy(float)
            rows.append(
                {
                    "test": "baseline_responder_minus_nonresponder",
                    "marker_compartment": compartment,
                    "module": module,
                    "metric": metric,
                    "n_responder": int(len(resp)),
                    "n_nonresponder": int(len(non)),
                    "mean_responder": float(np.nanmean(resp)) if len(resp) else np.nan,
                    "mean_nonresponder": float(np.nanmean(non)) if len(non) else np.nan,
                    "delta_responder_minus_nonresponder": float(np.nanmean(resp) - np.nanmean(non)) if len(resp) and len(non) else np.nan,
                    "hedges_g": hedges_g(resp, non),
                    "welch_t": float(t_stat) if pd.notna(t_stat) else np.nan,
                    "p": float(p_value) if pd.notna(p_value) else np.nan,
                    "auc_responder_high": auc_safe(labels, scores),
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
    return out


def compare_prepost(donor_scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (group, compartment, module), sub in donor_scores.groupby(["group", "marker_compartment", "module"], observed=True):
        if compartment == "ambiguous":
            continue
        base = sub[sub["timepoint_norm"].eq("W0")].set_index("patient")
        post = sub[sub["treatment"].eq("post-tx")].copy()
        order = {"W8": 8, "W16": 16, "W24": 24, "W48": 48}
        post["tp_order"] = post["timepoint_norm"].map(order).fillna(999)
        post = post.sort_values("tp_order").drop_duplicates("patient").set_index("patient")
        common = sorted(set(base.index) & set(post.index))
        for metric in ["mean_score", "high_fraction"]:
            if len(common) >= 2:
                diff = post.loc[common, metric].to_numpy(float) - base.loc[common, metric].to_numpy(float)
                t_stat, p_value = stats.ttest_1samp(diff, 0.0, nan_policy="omit")
            else:
                diff, t_stat, p_value = np.array([]), np.nan, np.nan
            rows.append(
                {
                    "test": "earliest_post_minus_baseline",
                    "group": group,
                    "marker_compartment": compartment,
                    "module": module,
                    "metric": metric,
                    "n_pairs": int(len(diff)),
                    "mean_delta": float(np.nanmean(diff)) if len(diff) else np.nan,
                    "median_delta": float(np.nanmedian(diff)) if len(diff) else np.nan,
                    "one_sample_t": float(t_stat) if pd.notna(t_stat) else np.nan,
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
    meta = parse_soft_metadata()
    obs_tables = []
    expr_tables = []
    gene_sets = []
    run_log = []
    for _, sample in meta.iterrows():
        prefix = sample["sample_prefix"]
        try:
            obs, expr, genes = selected_log_expression(prefix)
            obs = classify(obs, expr, genes)
            for col in ["gsm", "title", "patient", "group", "timepoint_norm", "responder", "treatment", "tissue"]:
                obs[col] = sample.get(col)
            obs_tables.append(obs)
            expr_tables.append(pd.DataFrame(expr, columns=genes))
            gene_sets.append(set(genes))
            run_log.append({"sample_prefix": prefix, "status": "completed", "n_cells": int(len(obs)), "n_genes_selected": int(len(genes))})
        except Exception as exc:  # noqa: BLE001
            run_log.append({"sample_prefix": prefix, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})
    if not obs_tables:
        raise RuntimeError("No GSE253006 samples analyzed")

    obs_all = pd.concat(obs_tables, ignore_index=True)
    common_genes = sorted(set.intersection(*gene_sets))
    expr_all = pd.concat([df.reindex(columns=common_genes) for df in expr_tables], ignore_index=True).to_numpy(dtype=float)
    gene_to_idx = {gene: i for i, gene in enumerate(common_genes)}

    cell_rows = []
    module_gene_rows = []
    for compartment, comp_obs in obs_all.groupby("marker_compartment", observed=True):
        if compartment == "ambiguous":
            continue
        comp_idx = comp_obs.index.to_numpy()
        baseline_mask = comp_obs["timepoint_norm"].eq("W0").to_numpy()
        if baseline_mask.sum() < 100:
            continue
        comp_expr = expr_all[comp_idx, :]
        baseline_expr = comp_expr[baseline_mask, :]
        mean = np.nanmean(baseline_expr, axis=0)
        sd = np.nanstd(baseline_expr, axis=0, ddof=1)
        sd[~np.isfinite(sd) | (sd < 1e-6)] = 1.0
        z = (comp_expr - mean) / sd
        for module, genes in ALL_MODULES.items():
            present = [g for g in genes if g in gene_to_idx]
            module_gene_rows.append(
                {
                    "marker_compartment": compartment,
                    "module": module,
                    "n_genes_present": len(present),
                    "genes_present": ",".join(present),
                }
            )
            if not present:
                continue
            vals = np.nanmean(z[:, [gene_to_idx[g] for g in present]], axis=1)
            threshold = np.nanpercentile(vals[baseline_mask], 75)
            tmp = comp_obs[["gsm", "title", "patient", "group", "timepoint_norm", "responder", "treatment", "tissue", "marker_compartment"]].copy()
            tmp["module"] = module
            tmp["score"] = vals
            tmp["high"] = vals > threshold
            cell_rows.append(tmp)
    cell_scores = pd.concat(cell_rows, ignore_index=True) if cell_rows else pd.DataFrame()

    donor_rows = []
    if not cell_scores.empty:
        for keys, sub in cell_scores.groupby(
            ["gsm", "title", "patient", "group", "timepoint_norm", "responder", "treatment", "tissue", "marker_compartment", "module"],
            observed=True,
        ):
            if len(sub) < 50:
                continue
            gsm, title, patient, group, timepoint_norm, responder, treatment, tissue, compartment, module = keys
            donor_rows.append(
                {
                    "gsm": gsm,
                    "title": title,
                    "patient": patient,
                    "group": group,
                    "timepoint_norm": timepoint_norm,
                    "responder": bool(responder),
                    "treatment": treatment,
                    "tissue": tissue,
                    "marker_compartment": compartment,
                    "module": module,
                    "n_cells": int(len(sub)),
                    "mean_score": float(np.nanmean(sub["score"])),
                    "high_fraction": float(np.nanmean(sub["high"])),
                }
            )
    donor_scores = pd.DataFrame(donor_rows)
    baseline = compare_baseline(donor_scores) if not donor_scores.empty else pd.DataFrame()
    prepost = compare_prepost(donor_scores) if not donor_scores.empty else pd.DataFrame()
    counts = (
        obs_all.groupby(["gsm", "title", "patient", "group", "timepoint_norm", "responder", "marker_compartment"], observed=True)
        .size()
        .reset_index(name="n_cells")
    )

    counts.to_csv(OUT / "gse253006_marker_compartment_counts.tsv", sep="\t", index=False)
    pd.DataFrame(module_gene_rows).to_csv(OUT / "gse253006_marker_module_genes_present.tsv", sep="\t", index=False)
    donor_scores.to_csv(OUT / "gse253006_marker_donor_module_scores.tsv", sep="\t", index=False)
    baseline.to_csv(OUT / "gse253006_marker_baseline_response_tests.tsv", sep="\t", index=False)
    prepost.to_csv(OUT / "gse253006_marker_prepost_tests.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "run_log": run_log,
        "n_cells_total": int(len(obs_all)),
        "n_samples": int(obs_all["gsm"].nunique()),
        "n_baseline_samples": int(obs_all.loc[obs_all["timepoint_norm"].eq("W0"), "gsm"].nunique()),
        "baseline_group_counts": obs_all.loc[obs_all["timepoint_norm"].eq("W0")].drop_duplicates("gsm")["group"].value_counts().to_dict(),
        "compartment_counts_total": counts.groupby("marker_compartment")["n_cells"].sum().to_dict(),
        "top_baseline_responder_high": (
            baseline[baseline["delta_responder_minus_nonresponder"] > 0]
            .sort_values(["p", "hedges_g"], ascending=[True, False])
            .head(30)
            .to_dict(orient="records")
            if not baseline.empty
            else []
        ),
        "top_prepost_decreases": (
            prepost[prepost["mean_delta"] < 0]
            .sort_values(["p", "mean_delta"], ascending=[True, True])
            .head(30)
            .to_dict(orient="records")
            if not prepost.empty
            else []
        ),
        "guardrail": "Marker-derived compartments, no curated cell labels; small baseline n=11.",
    }
    (OUT / "gse253006_marker_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
