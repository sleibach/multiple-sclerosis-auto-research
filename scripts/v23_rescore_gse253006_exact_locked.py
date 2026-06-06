#!/usr/bin/env python3
"""Recompute exact LOCKED_RULE_V22 modules in GSE253006 all-cell pseudobulk."""

from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import io, stats

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "gse253006"
MATRIX_DIR = RAW / "raw"
OUT = ROOT / "analysis" / "v23_apc_hla_monitoring" / "gse253006_exact_locked"
SEED = 20260606

IFN_APC = ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"]
HLAII = ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"]
RECEPTOR = ["CD74", "CD44", "CXCR4"]
TARGET_GENES = sorted(set(IFN_APC + HLAII + RECEPTOR))


def parse_soft_metadata() -> pd.DataFrame:
    rows = []
    cur: dict[str, str] = {}
    for line in (RAW / "GSE253006_family.soft").read_text(errors="ignore").splitlines():
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


def read_features(prefix: str) -> pd.DataFrame:
    rows = []
    with gzip.open(MATRIX_DIR / f"{prefix}_features.tsv.gz", "rt") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                rows.append((parts[0], parts[1]))
    return pd.DataFrame(rows, columns=["gene_id", "gene_symbol"])


def sample_gene_means(prefix: str) -> dict[str, object]:
    features = read_features(prefix)
    gene_to_idx = {}
    for i, gene in enumerate(features["gene_symbol"].astype(str)):
        if gene in TARGET_GENES and gene not in gene_to_idx:
            gene_to_idx[gene] = i
    mat = io.mmread(str(MATRIX_DIR / f"{prefix}_matrix.mtx.gz")).tocsr().astype(float)
    if mat.shape[0] != len(features) and mat.shape[1] == len(features):
        mat = mat.T.tocsr()
    if mat.shape[0] != len(features):
        raise ValueError(f"unexpected matrix/features shape for {prefix}: {mat.shape}, {len(features)}")
    lib_size = np.asarray(mat.sum(axis=0)).ravel()
    valid = np.isfinite(lib_size) & (lib_size > 0)
    lib_safe = lib_size.copy()
    lib_safe[~valid] = np.nan
    out: dict[str, object] = {
        "sample_prefix": prefix,
        "n_cells": int(valid.sum()),
        "n_target_genes_found": int(len(gene_to_idx)),
        "target_genes_found": ";".join(sorted(gene_to_idx)),
    }
    for gene in TARGET_GENES:
        if gene not in gene_to_idx:
            out[f"gene_{gene}"] = np.nan
            out[f"detect_{gene}"] = np.nan
            continue
        sub = mat[gene_to_idx[gene], :].tocoo()
        vals = np.asarray(mat[gene_to_idx[gene], :].todense()).ravel()
        norm = np.divide(vals, lib_safe, out=np.zeros_like(vals, dtype=float), where=np.isfinite(lib_safe)) * 1e4
        log_norm = np.log1p(norm[valid])
        out[f"gene_{gene}"] = float(np.mean(log_norm)) if log_norm.size else np.nan
        out[f"detect_{gene}"] = float((log_norm > 0).mean()) if log_norm.size else np.nan
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


def bootstrap_auc_ci(scores: np.ndarray, y: np.ndarray, n_boot: int = 5000) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    idx = np.arange(len(scores))
    aucs = []
    for _ in range(n_boot):
        sample = rng.choice(idx, size=len(idx), replace=True)
        if len(set(y[sample].tolist())) < 2:
            continue
        aucs.append(auc_score(scores[sample], y[sample]))
    return float(np.percentile(aucs, 2.5)), float(np.percentile(aucs, 97.5))


def module_score(df: pd.DataFrame, genes: list[str], prefix: str) -> tuple[pd.Series, list[str]]:
    present = [g for g in genes if f"gene_{g}" in df.columns and df[f"gene_{g}"].notna().any()]
    values = df[[f"gene_{g}" for g in present]].copy()
    z = (values - values.mean(axis=0)) / values.std(axis=0).replace(0, np.nan)
    return z.mean(axis=1), present


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = parse_soft_metadata()
    rows = []
    for prefix in meta["sample_prefix"]:
        rows.append(sample_gene_means(prefix))
    scores = meta.merge(pd.DataFrame(rows), on="sample_prefix", how="left")
    scores["module_IFN_APC"], ifn_present = module_score(scores, IFN_APC, "IFN_APC")
    scores["module_HLAII"], hla_present = module_score(scores, HLAII, "HLAII")
    scores["module_RECEPTOR"], rec_present = module_score(scores, RECEPTOR, "RECEPTOR")

    paired = []
    order = {"W8": 8, "W16": 16, "W24": 24, "W48": 48}
    for patient, sub in scores.groupby("patient"):
        base = sub[sub["timepoint_norm"].eq("W0")]
        post = sub[sub["timepoint_norm"].isin(order)].copy()
        if base.empty or post.empty:
            continue
        post["_order"] = post["timepoint_norm"].map(order)
        b = base.sort_values("gsm").iloc[0]
        p = post.sort_values("_order").iloc[0]
        delta_ifn = float(p["module_IFN_APC"] - b["module_IFN_APC"])
        delta_hla = float(p["module_HLAII"] - b["module_HLAII"])
        delta_rec = float(p["module_RECEPTOR"] - b["module_RECEPTOR"])
        paired.append(
            {
                "cohort": "GSE253006_TOF_exact",
                "patient": patient,
                "response": "Responder" if bool(b["responder"]) else "Non-responder",
                "baseline_sample": b["gsm"],
                "treated_sample": p["gsm"],
                "treated_timepoint": p["timepoint_norm"],
                "delta_IFN_APC": delta_ifn,
                "delta_HLAII": delta_hla,
                "locked_signed_score": -delta_ifn,
                "delta_RECEPTOR": -delta_rec,
            }
        )
    paired_df = pd.DataFrame(paired)
    y = paired_df["response"].eq("Responder").astype(int).to_numpy()
    signed = paired_df["locked_signed_score"].to_numpy(float)
    receptor = paired_df["delta_RECEPTOR"].to_numpy(float)
    auc = auc_score(signed, y)
    lo, hi = bootstrap_auc_ci(signed, y)
    g = hedges_g(signed, y)
    p = float(stats.ttest_ind(signed[y == 1], signed[y == 0], equal_var=False).pvalue)
    rauc = auc_score(receptor, y)
    passed = auc >= 0.70 and g >= 0.50
    ledger = pd.DataFrame(
        [
            {
                "cohort": "GSE253006_TOF_exact",
                "disease": "ulcerative_colitis",
                "therapy": "tofacitinib",
                "therapy_class": "Class A",
                "validation_scope": "primary_locked_exact_all_cell_compartment_unresolved",
                "n_labeled": int(len(paired_df)),
                "n_responders": int(y.sum()),
                "n_nonresponders": int(len(y) - y.sum()),
                "feature_applied": "-delta_IFN_APC",
                "auc": auc,
                "auc_ci_low": lo,
                "auc_ci_high": hi,
                "hedges_g": g,
                "welch_p": p,
                "receptor_auc": rauc,
                "receptor_auc_delta": rauc - auc,
                "pass_fail": "pass" if passed else "fail",
                "specificity": "non_specific" if rauc - auc >= 0.10 else "specificity_ok",
                "present_IFN_APC": ";".join(ifn_present),
                "present_HLAII": ";".join(hla_present),
                "present_RECEPTOR": ";".join(rec_present),
                "notes": "Exact frozen V22 genes recomputed from raw 10x all-cell sample pseudobulk; no saved per-cell compartment labels, so compartment unresolved.",
            }
        ]
    )
    scores.to_csv(OUT / "gse253006_exact_sample_gene_scores.tsv", sep="\t", index=False)
    paired_df.to_csv(OUT / "gse253006_exact_paired_scores.tsv", sep="\t", index=False)
    ledger.to_csv(OUT / "gse253006_exact_validation_ledger.tsv", sep="\t", index=False)
    print(json.dumps(ledger.iloc[0].to_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
