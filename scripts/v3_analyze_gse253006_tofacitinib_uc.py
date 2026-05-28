#!/usr/bin/env python3
"""Targeted GSE253006 UC tofacitinib response analysis.

This is a weak but useful treatment-response validation branch. The GEO
supplement exposes per-sample raw 10x matrices and response/timepoint metadata,
but no cell-type annotation file was found in GEO. Therefore this script does
sample-level target-gene/module scoring across all captured biopsy cells. It is
not used as cell-type-resolved mechanistic proof.

Primary question:

- Do baseline responder biopsies have higher IFN/APC or HLA-II/CD74 module
  scores than baseline non-responders, consistent with the published paper's
  reported higher baseline JAK-STAT activity in responders?
"""

from __future__ import annotations

import gzip
import json
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import io, sparse, stats
from statsmodels.stats.multitest import multipletests

SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "gse253006"
MATRIX_DIR = RAW / "raw"
OUT = ROOT / "results_v3" / "gse253006_tofacitinib"

MODULES = {
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "CD74", "IFI30", "HLA-DRA", "HLA-DRB1"],
    "hla_ii_apc": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "CIITA", "RFX5"],
    "lysosomal_apc": ["IFI30", "CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"],
    "mif_cd74_receptor_state": ["CD74", "CD44", "CXCR4", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1"],
    "mixscale_validated_ifng_readout": ["CD74", "CTSS", "IFI30", "CIITA", "TAP1", "TAP2", "B2M", "NLRC5"],
    "published_nonresponse_macrophage_inflammation": ["IL1B", "IL6", "CXCL1", "CXCL8", "S100A9", "MMP9", "MMP12", "FCGR3A"],
}
TARGET_GENES = sorted({g for genes in MODULES.values() for g in genes})


def parse_soft_metadata() -> pd.DataFrame:
    path = RAW / "GSE253006_family.soft"
    rows = []
    cur: dict[str, str] = {}
    for line in path.read_text(errors="ignore").splitlines():
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


def read_features(path: Path) -> pd.DataFrame:
    rows = []
    with gzip.open(path, "rt") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                rows.append({"gene_id": parts[0], "gene_symbol": parts[1]})
    return pd.DataFrame(rows)


def score_sample(prefix: str) -> dict[str, object]:
    features_path = MATRIX_DIR / f"{prefix}_features.tsv.gz"
    matrix_path = MATRIX_DIR / f"{prefix}_matrix.mtx.gz"
    barcode_path = MATRIX_DIR / f"{prefix}_barcodes.tsv.gz"
    features = read_features(features_path)
    gene_to_idx = {}
    for i, gene in enumerate(features["gene_symbol"].astype(str)):
        if gene in TARGET_GENES and gene not in gene_to_idx:
            gene_to_idx[gene] = i
    with gzip.open(barcode_path, "rt") as handle:
        n_barcodes = sum(1 for _ in handle)
    mat = io.mmread(str(matrix_path)).tocsr().astype(float)
    # 10x convention: features x cells. Defensively transpose if needed.
    if mat.shape[0] != len(features) and mat.shape[1] == len(features):
        mat = mat.T.tocsr()
    if mat.shape[0] != len(features):
        raise ValueError(f"unexpected matrix/features shape for {prefix}: {mat.shape}, {len(features)}")
    lib_size = np.asarray(mat.sum(axis=0)).ravel()
    valid_cells = np.isfinite(lib_size) & (lib_size > 0)
    lib_size_safe = lib_size.copy()
    lib_size_safe[~valid_cells] = np.nan
    rows = {
        "sample_prefix": prefix,
        "n_cells": int(mat.shape[1]),
        "n_barcodes": int(n_barcodes),
        "median_umis_per_cell": float(np.nanmedian(lib_size[valid_cells])) if valid_cells.any() else np.nan,
    }
    gene_values = {}
    detection = {}
    if gene_to_idx:
        sub = mat[[gene_to_idx[g] for g in gene_to_idx], :].tocsc()
        norm = sub.multiply(np.divide(1.0, lib_size_safe, out=np.zeros_like(lib_size_safe), where=np.isfinite(lib_size_safe))).multiply(1e4)
        log_norm = np.log1p(norm.toarray())
        for j, gene in enumerate(gene_to_idx):
            vals = log_norm[j, valid_cells]
            gene_values[gene] = float(np.nanmean(vals))
            detection[gene] = float((vals > 0).mean()) if vals.size else np.nan
    for gene in TARGET_GENES:
        rows[f"gene_{gene}"] = gene_values.get(gene, np.nan)
        rows[f"detect_{gene}"] = detection.get(gene, np.nan)
    for module, genes in MODULES.items():
        present = [gene for gene in genes if gene in gene_values]
        rows[f"module_{module}"] = float(np.nanmean([gene_values[g] for g in present])) if present else np.nan
        rows[f"module_{module}_genes_present"] = ",".join(present)
    return rows


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled = ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    if pooled <= 0:
        return np.nan
    correction = 1.0 - 3.0 / (4.0 * (len(a) + len(b)) - 9.0)
    return ((a.mean() - b.mean()) / math.sqrt(pooled)) * correction


def baseline_response_tests(samples: pd.DataFrame) -> pd.DataFrame:
    rows = []
    base = samples[samples["timepoint_norm"].eq("W0")].copy()
    features = [c for c in samples.columns if c.startswith("module_") and not c.endswith("_genes_present")]
    features.extend([f"gene_{g}" for g in TARGET_GENES])
    for feature in features:
        resp = base.loc[base["responder"], feature].to_numpy(float)
        non = base.loc[~base["responder"], feature].to_numpy(float)
        if len(resp) >= 2 and len(non) >= 2:
            t, p = stats.ttest_ind(resp, non, equal_var=False, nan_policy="omit")
        else:
            t, p = np.nan, np.nan
        rows.append(
            {
                "test": "baseline_responder_minus_nonresponder",
                "feature": feature.replace("module_", "").replace("gene_", ""),
                "n_responder": int(len(resp)),
                "n_nonresponder": int(len(non)),
                "mean_responder": float(np.nanmean(resp)) if len(resp) else np.nan,
                "mean_nonresponder": float(np.nanmean(non)) if len(non) else np.nan,
                "delta_responder_minus_nonresponder": float(np.nanmean(resp) - np.nanmean(non)) if len(resp) and len(non) else np.nan,
                "hedges_g": hedges_g(resp, non),
                "welch_t": float(t) if pd.notna(t) else np.nan,
                "p": float(p) if pd.notna(p) else np.nan,
            }
        )
    out = pd.DataFrame(rows)
    out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
    return out


def paired_prepost_tests(samples: pd.DataFrame) -> pd.DataFrame:
    rows = []
    features = [c for c in samples.columns if c.startswith("module_") and not c.endswith("_genes_present")]
    for response_label, sub in samples.groupby("group", observed=True):
        base = sub[sub["timepoint_norm"].eq("W0")].set_index("patient")
        post = sub[sub["treatment"].eq("post-tx")].copy()
        # Use each patient's earliest post-treatment timepoint for a simple paired contrast.
        order = {"W8": 8, "W16": 16, "W24": 24, "W48": 48}
        post["tp_order"] = post["timepoint_norm"].map(order).fillna(999)
        post = post.sort_values("tp_order").drop_duplicates("patient").set_index("patient")
        common = sorted(set(base.index) & set(post.index))
        for feature in features:
            if len(common) >= 2:
                diff = post.loc[common, feature].to_numpy(float) - base.loc[common, feature].to_numpy(float)
                t, p = stats.ttest_1samp(diff, 0.0, nan_policy="omit")
            else:
                diff, t, p = np.array([]), np.nan, np.nan
            rows.append(
                {
                    "test": "earliest_post_minus_baseline",
                    "group": response_label,
                    "feature": feature.replace("module_", ""),
                    "n_pairs": int(len(diff)),
                    "mean_delta": float(np.nanmean(diff)) if len(diff) else np.nan,
                    "median_delta": float(np.nanmedian(diff)) if len(diff) else np.nan,
                    "one_sample_t": float(t) if pd.notna(t) else np.nan,
                    "p": float(p) if pd.notna(p) else np.nan,
                }
            )
    out = pd.DataFrame(rows)
    out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1] if not out.empty else []
    return out


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    meta = parse_soft_metadata()
    sample_rows = []
    for _, row in meta.iterrows():
        sample_rows.append(score_sample(row["sample_prefix"]))
    scores = meta.merge(pd.DataFrame(sample_rows), on="sample_prefix", how="left")
    baseline = baseline_response_tests(scores)
    paired = paired_prepost_tests(scores)
    scores.to_csv(OUT / "gse253006_sample_target_scores.tsv", sep="\t", index=False)
    baseline.to_csv(OUT / "gse253006_baseline_response_tests.tsv", sep="\t", index=False)
    paired.to_csv(OUT / "gse253006_paired_prepost_tests.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "n_samples": int(len(scores)),
        "n_baseline_samples": int(scores["timepoint_norm"].eq("W0").sum()),
        "baseline_group_counts": scores[scores["timepoint_norm"].eq("W0")]["group"].value_counts().to_dict(),
        "top_baseline_responder_high": baseline.sort_values(["p"]).head(20).to_dict(orient="records"),
        "guardrail": (
            "GSE253006 GEO supplement lacks cell-type annotations; these are all-cell sample-level "
            "scores and validate/triage a published response dataset, not cell-type-resolved proof."
        ),
    }
    (OUT / "gse253006_tofacitinib_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
