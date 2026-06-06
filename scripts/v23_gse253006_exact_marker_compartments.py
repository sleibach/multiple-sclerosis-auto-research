#!/usr/bin/env python3
"""Exact LOCKED_RULE_V22 rescoring in marker-derived GSE253006 compartments."""

from __future__ import annotations

import json
import math
import gzip
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import io, stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v23_apc_hla_monitoring" / "gse253006_exact_compartments"
SEED = 20260606

IFN_APC = ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"]
HLAII = ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"]
RECEPTOR = ["CD74", "CD44", "CXCR4"]
TARGET_GENES = sorted(set(IFN_APC + HLAII + RECEPTOR))
MARKER_SETS = {
    "epithelial_like": ["EPCAM", "KRT8", "KRT18", "KRT19", "VIL1", "MUC2", "TFF3", "FABP1"],
    "myeloid_apc_like": ["LYZ", "LST1", "CD14", "FCGR3A", "ITGAX", "CST3", "HLA-DRA", "CD74", "MS4A7"],
    "t_cell_like": ["CD3D", "CD3E", "CD3G", "TRAC", "CD4", "CD8A", "CD8B", "NKG7", "GZMA"],
    "b_plasma_like": ["MS4A1", "CD79A", "CD79B", "CD74", "MZB1", "JCHAIN", "IGHG1"],
    "stromal_endothelial_like": ["COL1A1", "COL1A2", "DCN", "LUM", "PECAM1", "VWF", "CLDN5", "ACTA2"],
}
ALL_GENES = sorted(set(TARGET_GENES) | {gene for genes in MARKER_SETS.values() for gene in genes})


def parse_soft_metadata() -> pd.DataFrame:
    raw = ROOT / "data" / "raw_v3" / "gse253006"
    rows = []
    cur: dict[str, str] = {}
    for line in (raw / "GSE253006_family.soft").read_text(errors="ignore").splitlines():
        if line.startswith("^SAMPLE"):
            if cur:
                rows.append(cur)
            cur = {"gsm": line.split("=", 1)[1].strip()}
        elif line.startswith("!Sample_title"):
            cur["title"] = line.split("=", 1)[1].strip()
        elif line.startswith("!Sample_source_name_ch1"):
            cur["source"] = line.split("=", 1)[1].strip()
        elif line.startswith("!Sample_characteristics_ch1"):
            val = line.split("=", 1)[1].strip()
            if ":" in val:
                key, value = val.split(":", 1)
                cur[key.strip().lower()] = value.strip()
    if cur:
        rows.append(cur)
    df = pd.DataFrame(rows)
    df["timepoint_norm"] = df["timepoint"].str.upper()
    df["responder"] = df["group"].eq("Responder")
    df["sample_prefix"] = df["gsm"] + "_" + df["title"]
    return df


def selected_log_expression(prefix: str) -> tuple[pd.DataFrame, np.ndarray, list[str]]:
    matrix_dir = ROOT / "data" / "raw_v3" / "gse253006" / "raw"
    features_path = matrix_dir / f"{prefix}_features.tsv.gz"
    matrix_path = matrix_dir / f"{prefix}_matrix.mtx.gz"
    barcodes_path = matrix_dir / f"{prefix}_barcodes.tsv.gz"
    features = []
    with gzip.open(features_path, "rt") as handle:
        for i, line in enumerate(handle):
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                features.append((i, parts[1]))
    row_to_gene = {}
    for idx, gene in features:
        if gene in ALL_GENES and gene not in row_to_gene.values():
            row_to_gene[idx] = gene
    rows = sorted(row_to_gene)
    genes = [row_to_gene[i] for i in rows]
    with gzip.open(barcodes_path, "rt") as handle:
        barcodes = [line.strip() for line in handle if line.strip()]
    mat = io.mmread(str(matrix_path)).tocsc().astype(float)
    if mat.shape[0] != len(features) and mat.shape[1] == len(features):
        mat = mat.T.tocsc()
    lib = np.asarray(mat.sum(axis=0)).ravel()
    valid = np.isfinite(lib) & (lib > 0)
    lib_safe = lib.copy()
    lib_safe[~valid] = np.nan
    selected = mat[rows, :].T.tocsr()
    norm = selected.multiply(np.divide(1.0, lib_safe, out=np.zeros_like(lib_safe), where=np.isfinite(lib_safe))[:, None]).multiply(1e4)
    log_expr = np.log1p(norm.toarray()).astype(np.float32)
    obs = pd.DataFrame({"sample_prefix": prefix, "barcode": barcodes, "n_counts": lib, "valid_cell": valid})
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
    out["marker_compartment"] = compartments
    out["marker_top_score"] = top_score
    out["marker_margin"] = top_score - second_score
    return out


def auc_score(scores: np.ndarray, y: np.ndarray) -> float:
    if len(set(y.tolist())) < 2:
        return math.nan
    ranks = pd.Series(scores).rank(method="average").to_numpy()
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    rank_sum = float(ranks[y == 1].sum())
    return float((rank_sum - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def hedges_g(scores: np.ndarray, y: np.ndarray) -> float:
    a = scores[y == 1]
    b = scores[y == 0]
    if len(a) < 2 or len(b) < 2:
        return math.nan
    pooled = math.sqrt(((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0:
        return 0.0
    return float(((np.mean(a) - np.mean(b)) / pooled) * (1.0 - 3.0 / (4.0 * (len(a) + len(b)) - 9.0)))


def bootstrap_auc_ci(scores: np.ndarray, y: np.ndarray, n_boot: int = 2000) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    idx = np.arange(len(scores))
    aucs = []
    for _ in range(n_boot):
        sample = rng.choice(idx, size=len(idx), replace=True)
        if len(set(y[sample].tolist())) < 2:
            continue
        aucs.append(auc_score(scores[sample], y[sample]))
    if not aucs:
        return math.nan, math.nan
    return float(np.percentile(aucs, 2.5)), float(np.percentile(aucs, 97.5))


def module_score(df: pd.DataFrame, genes: list[str]) -> tuple[pd.Series, list[str]]:
    present = [g for g in genes if f"gene_{g}" in df.columns and df[f"gene_{g}"].notna().any()]
    values = df[[f"gene_{g}" for g in present]].copy()
    z = (values - values.mean(axis=0)) / values.std(axis=0).replace(0, np.nan)
    return z.mean(axis=1), present


def summarize(compartment: str, paired: pd.DataFrame, present_ifn: list[str], present_hla: list[str], present_rec: list[str]) -> dict[str, object]:
    y = paired["response"].eq("Responder").astype(int).to_numpy()
    signed = paired["locked_signed_score"].to_numpy(float)
    receptor = paired["delta_RECEPTOR"].to_numpy(float)
    auc = auc_score(signed, y)
    lo, hi = bootstrap_auc_ci(signed, y)
    g = hedges_g(signed, y)
    p = float(stats.ttest_ind(signed[y == 1], signed[y == 0], equal_var=False).pvalue) if len(set(y.tolist())) == 2 else math.nan
    rauc = auc_score(receptor, y)
    return {
        "cohort": "GSE253006_TOF_exact",
        "marker_compartment": compartment,
        "n_labeled": int(len(paired)),
        "n_responders": int(y.sum()),
        "n_nonresponders": int(len(y) - y.sum()),
        "auc": auc,
        "auc_ci_low": lo,
        "auc_ci_high": hi,
        "hedges_g": g,
        "welch_p": p,
        "receptor_auc": rauc,
        "receptor_auc_delta": rauc - auc,
        "pass_fail": "pass" if auc >= 0.70 and g >= 0.50 else "fail",
        "present_IFN_APC": ";".join(present_ifn),
        "present_HLAII": ";".join(present_hla),
        "present_RECEPTOR": ";".join(present_rec),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = parse_soft_metadata()
    comp_rows = []
    count_rows = []
    for _, m in meta.iterrows():
        obs, expr, genes = selected_log_expression(m["sample_prefix"])
        obs = classify(obs, expr, genes)
        gene_to_idx = {g: i for i, g in enumerate(genes)}
        for compartment, idx in obs.groupby("marker_compartment", observed=True).groups.items():
            cell_idx = np.asarray(list(idx), dtype=int)
            row = {k: m[k] for k in ["gsm", "title", "patient", "group", "timepoint_norm", "responder", "treatment", "tissue", "sample_prefix"]}
            row["marker_compartment"] = compartment
            row["n_cells"] = int(len(cell_idx))
            for gene in TARGET_GENES:
                if gene in gene_to_idx and len(cell_idx):
                    vals = expr[cell_idx, gene_to_idx[gene]]
                    row[f"gene_{gene}"] = float(np.mean(vals))
                    row[f"detect_{gene}"] = float((vals > 0).mean())
                else:
                    row[f"gene_{gene}"] = np.nan
                    row[f"detect_{gene}"] = np.nan
            comp_rows.append(row)
            count_rows.append({"gsm": m["gsm"], "patient": m["patient"], "timepoint_norm": m["timepoint_norm"], "marker_compartment": compartment, "n_cells": int(len(cell_idx))})
    scores = pd.DataFrame(comp_rows)
    paired_rows = []
    summaries = []
    order = {"W8": 8, "W16": 16, "W24": 24, "W48": 48}
    for compartment, comp in scores[scores["marker_compartment"].ne("ambiguous")].groupby("marker_compartment"):
        comp = comp.copy()
        comp["module_IFN_APC"], ifn_present = module_score(comp, IFN_APC)
        comp["module_HLAII"], hla_present = module_score(comp, HLAII)
        comp["module_RECEPTOR"], rec_present = module_score(comp, RECEPTOR)
        local_pairs = []
        for patient, sub in comp.groupby("patient"):
            base = sub[sub["timepoint_norm"].eq("W0")]
            post = sub[sub["timepoint_norm"].isin(order)].copy()
            if base.empty or post.empty:
                continue
            post["_order"] = post["timepoint_norm"].map(order)
            b = base.sort_values("gsm").iloc[0]
            p = post.sort_values("_order").iloc[0]
            local_pairs.append(
                {
                    "patient": patient,
                    "marker_compartment": compartment,
                    "response": "Responder" if bool(b["responder"]) else "Non-responder",
                    "baseline_sample": b["gsm"],
                    "treated_sample": p["gsm"],
                    "treated_timepoint": p["timepoint_norm"],
                    "delta_IFN_APC": float(p["module_IFN_APC"] - b["module_IFN_APC"]),
                    "delta_HLAII": float(p["module_HLAII"] - b["module_HLAII"]),
                    "locked_signed_score": float(-(p["module_IFN_APC"] - b["module_IFN_APC"])),
                    "delta_RECEPTOR": float(-(p["module_RECEPTOR"] - b["module_RECEPTOR"])),
                }
            )
        pair_df = pd.DataFrame(local_pairs)
        if len(pair_df) >= 4 and len(set(pair_df["response"])) == 2:
            summaries.append(summarize(compartment, pair_df, ifn_present, hla_present, rec_present))
            paired_rows.append(pair_df)
    pd.DataFrame(comp_rows).to_csv(OUT / "gse253006_exact_compartment_gene_scores.tsv", sep="\t", index=False)
    pd.DataFrame(count_rows).to_csv(OUT / "gse253006_exact_compartment_counts.tsv", sep="\t", index=False)
    summary_df = pd.DataFrame(summaries).sort_values("auc", ascending=False)
    summary_df.to_csv(OUT / "gse253006_exact_compartment_validation.tsv", sep="\t", index=False)
    if paired_rows:
        pd.concat(paired_rows, ignore_index=True).to_csv(OUT / "gse253006_exact_compartment_paired_scores.tsv", sep="\t", index=False)
    print(json.dumps(summary_df.to_dict(orient="records"), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
