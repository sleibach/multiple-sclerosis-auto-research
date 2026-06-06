#!/usr/bin/env python3
"""GSE248205 autoimmune thyroid Visium module validation.

This is spot-level spatial transcriptomics, not single-cell. It tests whether
the IFN/HLA-II/CD74/GILT antigen-processing state recurs in Hashimoto thyroiditis
and Graves disease thyroid tissue compared with controls.
"""

from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import io, stats
from statsmodels.stats.multitest import multipletests

SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "gse248205"
PROCESSED = RAW / "processed"
OUT = ROOT / "phases/v3/results" / "gse248205_thyroid_spatial"

MODULES = {
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "CD74", "IFI30", "HLA-DRA", "HLA-DRB1"],
    "hla_ii_apc": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "CIITA", "RFX5"],
    "lysosomal_apc": ["IFI30", "CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"],
    "mif_cd74_receptor_state": ["CD74", "CD44", "CXCR4", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1"],
    "mixscale_validated_ifng_readout": ["CD74", "CTSS", "IFI30", "CIITA", "TAP1", "TAP2", "B2M", "NLRC5"],
}
TARGET_GENES = sorted({g for genes in MODULES.values() for g in genes})

SAMPLE_DISEASE = {
    "C1": "control",
    "C2": "control",
    "HT1": "Hashimoto thyroiditis",
    "HT2": "Hashimoto thyroiditis",
    "HT3": "Hashimoto thyroiditis",
    "GD1": "Graves disease",
    "GD2": "Graves disease",
    "GD3": "Graves disease",
}


def read_features(path: Path) -> pd.DataFrame:
    rows = []
    with gzip.open(path, "rt") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                rows.append({"gene_id": parts[0], "gene_symbol": parts[1]})
    return pd.DataFrame(rows)


def score_sample(sample: str) -> dict[str, object]:
    sample_dir = PROCESSED / sample
    features = read_features(sample_dir / f"{sample}_features.tsv.gz")
    gene_to_idx = {}
    for i, gene in enumerate(features["gene_symbol"].astype(str)):
        if gene in TARGET_GENES and gene not in gene_to_idx:
            gene_to_idx[gene] = i
    mat = io.mmread(str(sample_dir / f"{sample}_matrix.mtx.gz")).tocsr().astype(float)
    if mat.shape[0] != len(features) and mat.shape[1] == len(features):
        mat = mat.T.tocsr()
    lib = np.asarray(mat.sum(axis=0)).ravel()
    valid = np.isfinite(lib) & (lib > 0)
    lib_safe = lib.copy()
    lib_safe[~valid] = np.nan
    row = {
        "sample": sample,
        "disease": SAMPLE_DISEASE[sample],
        "group": "control" if SAMPLE_DISEASE[sample] == "control" else "case",
        "n_spots": int(mat.shape[1]),
        "median_umis_per_spot": float(np.nanmedian(lib[valid])) if valid.any() else np.nan,
    }
    gene_values = {}
    detection = {}
    if gene_to_idx:
        genes = list(gene_to_idx)
        sub = mat[[gene_to_idx[g] for g in genes], :].tocsc()
        norm = sub.multiply(np.divide(1.0, lib_safe, out=np.zeros_like(lib_safe), where=np.isfinite(lib_safe))).multiply(1e4)
        log_norm = np.log1p(norm.toarray())
        for j, gene in enumerate(genes):
            vals = log_norm[j, valid]
            gene_values[gene] = float(np.nanmean(vals))
            detection[gene] = float((vals > 0).mean()) if vals.size else np.nan
    for gene in TARGET_GENES:
        row[f"gene_{gene}"] = gene_values.get(gene, np.nan)
        row[f"detect_{gene}"] = detection.get(gene, np.nan)
    for module, genes in MODULES.items():
        present = [g for g in genes if g in gene_values]
        row[f"module_{module}"] = float(np.nanmean([gene_values[g] for g in present])) if present else np.nan
        row[f"module_{module}_genes_present"] = ",".join(present)
    return row


def hedges_g(case, control):
    case = np.asarray(case, dtype=float)
    control = np.asarray(control, dtype=float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if len(case) < 2 or len(control) < 2:
        return np.nan
    pooled = ((len(case) - 1) * case.var(ddof=1) + (len(control) - 1) * control.var(ddof=1)) / (len(case) + len(control) - 2)
    if pooled <= 0:
        return np.nan
    return ((case.mean() - control.mean()) / math.sqrt(pooled)) * (1 - 3 / (4 * (len(case) + len(control)) - 9))


def compare(samples: pd.DataFrame) -> pd.DataFrame:
    rows = []
    features = [c for c in samples.columns if c.startswith("module_") and not c.endswith("_genes_present")]
    features.extend([f"gene_{g}" for g in TARGET_GENES])
    for disease in ["Hashimoto thyroiditis", "Graves disease"]:
        case_df = samples[samples["disease"].eq(disease)]
        ctrl_df = samples[samples["disease"].eq("control")]
        for feature in features:
            case = case_df[feature].to_numpy(float)
            ctrl = ctrl_df[feature].to_numpy(float)
            t, p = stats.ttest_ind(case, ctrl, equal_var=False, nan_policy="omit") if len(case) >= 2 and len(ctrl) >= 2 else (np.nan, np.nan)
            rows.append(
                {
                    "contrast": f"{disease}_vs_control",
                    "feature": feature.replace("module_", "").replace("gene_", ""),
                    "feature_type": "module" if feature.startswith("module_") else "gene",
                    "n_case_samples": int(len(case)),
                    "n_control_samples": int(len(ctrl)),
                    "mean_case": float(np.nanmean(case)) if len(case) else np.nan,
                    "mean_control": float(np.nanmean(ctrl)) if len(ctrl) else np.nan,
                    "delta_case_minus_control": float(np.nanmean(case) - np.nanmean(ctrl)) if len(case) and len(ctrl) else np.nan,
                    "hedges_g": hedges_g(case, ctrl),
                    "welch_t": float(t) if pd.notna(t) else np.nan,
                    "p": float(p) if pd.notna(p) else np.nan,
                }
            )
    out = pd.DataFrame(rows)
    out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
    return out


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    samples = pd.DataFrame([score_sample(s) for s in SAMPLE_DISEASE])
    comparisons = compare(samples)
    samples.to_csv(OUT / "gse248205_sample_module_scores.tsv", sep="\t", index=False)
    comparisons.to_csv(OUT / "gse248205_module_gene_contrasts.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "n_samples": int(len(samples)),
        "sample_counts": samples["disease"].value_counts().to_dict(),
        "top_positive": comparisons[comparisons["delta_case_minus_control"] > 0]
        .sort_values(["p", "hedges_g"], ascending=[True, False])
        .head(30)
        .to_dict(orient="records"),
        "guardrail": "Visium spot-level sample means; n=2 controls, n=3 per disease. Treat as spatial tissue support only.",
    }
    (OUT / "gse248205_thyroid_spatial_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
