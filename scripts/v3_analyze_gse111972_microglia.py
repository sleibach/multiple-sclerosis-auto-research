#!/usr/bin/env python3
"""Independent MS microglia validation in GSE111972.

Dataset: van der Poel et al. sorted human microglia RNA-seq from MS and
control grey/white matter. The input matrix is DESeq2-normalized counts from
GEO, not raw counts, so this script uses log2(count + 1) expression and treats
results as validation-scale evidence rather than a definitive DESeq2 reanalysis.
"""

from __future__ import annotations

import gzip
import json
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

try:
    import statsmodels.api as sm
except Exception:  # pragma: no cover - statsmodels is expected in the V3 env.
    sm = None


SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "gse111972"
OUT = ROOT / "phases/v3/results"

NORM_PATH = RAW / "GSE111972_norm_data.txt.gz"
MATRIX_PATH = RAW / "GSE111972_series_matrix.txt.gz"

TARGET_GENES = [
    "IFI30",
    "NAMPT",
    "CXCL10",
    "C1QB",
    "C1QA",
    "C1QC",
    "CTSB",
    "CTSD",
    "CTSS",
    "LAMP1",
    "LAMP2",
    "TPP1",
    "GPNMB",
    "SPP1",
    "TNF",
    "IL1B",
    "LIPA",
    "ACSL1",
    "APOE",
    "PLIN2",
    "MSR1",
    "TREM2",
    "MERTK",
    "STAT1",
    "IRF1",
    "IRF7",
    "HIF1A",
    "CD74",
    "CD44",
    "CXCR4",
    "MIF",
    "DDT",
    "HLA-DRA",
    "HLA-DRB1",
    "HLA-DPA1",
    "HLA-DPB1",
    "GBP1",
    "ISG15",
    "IFI44L",
    "LDHA",
    "SLC2A1",
    "HK2",
    "PFKFB3",
    "NFKBIA",
]

MODULES = {
    "lysosome_antigen_processing": [
        "IFI30",
        "CTSD",
        "CTSB",
        "CTSS",
        "CTSL",
        "LAMP1",
        "LAMP2",
        "TPP1",
        "HLA-DRA",
        "HLA-DRB1",
        "HLA-DPA1",
        "HLA-DPB1",
        "CD74",
    ],
    "interferon_apc": [
        "STAT1",
        "IRF1",
        "IRF7",
        "CXCL10",
        "IFI30",
        "HLA-DRA",
        "HLA-DRB1",
        "CD74",
        "GBP1",
        "ISG15",
        "IFI44L",
    ],
    "hif_nampt_metabolic": [
        "HIF1A",
        "NAMPT",
        "LDHA",
        "SLC2A1",
        "NFKBIA",
        "IL1B",
        "HK2",
        "PFKFB3",
    ],
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
    ],
    "complement_phagocytosis": [
        "C1QA",
        "C1QB",
        "C1QC",
        "CD68",
        "TREM2",
        "MERTK",
        "MSR1",
    ],
    "mif_cd74_receptor_state": [
        "CD74",
        "CD44",
        "CXCR4",
        "HLA-DRA",
        "HLA-DRB1",
        "HLA-DPA1",
        "HLA-DPB1",
    ],
    "mif_ligand_axis": [
        "MIF",
        "DDT",
    ],
}


def parse_quoted_fields(line: str) -> list[str]:
    return [field.strip().strip('"') for field in line.rstrip("\n").split("\t")]


def load_sample_metadata() -> pd.DataFrame:
    wanted_prefixes = {
        "!Sample_title": "sample",
        "!Sample_geo_accession": "geo_accession",
        "!Sample_characteristics_ch1": "characteristic",
        "!Sample_source_name_ch1": "source",
    }
    rows: dict[str, list[list[str]]] = {}
    with gzip.open(MATRIX_PATH, "rt") as handle:
        for line in handle:
            for prefix in wanted_prefixes:
                if line.startswith(prefix + "\t"):
                    rows.setdefault(prefix, []).append(parse_quoted_fields(line)[1:])

    titles = rows["!Sample_title"][0]
    meta = pd.DataFrame({"sample": titles})
    meta["geo_accession"] = rows["!Sample_geo_accession"][0]
    meta["source"] = rows["!Sample_source_name_ch1"][0]

    for characteristic in rows.get("!Sample_characteristics_ch1", []):
        if not characteristic:
            continue
        first = characteristic[0]
        if ":" not in first:
            continue
        key = first.split(":", 1)[0].strip().lower().replace(" ", "_")
        meta[key] = [value.split(":", 1)[1].strip() if ":" in value else "" for value in characteristic]

    parsed = meta["sample"].str.extract(r"Sample_(?P<disease>MS|CON)_(?P<region>WM|GM)_(?P<sample_number>\d+)")
    meta = pd.concat([meta, parsed], axis=1)
    meta["disease"] = meta["disease"].replace({"CON": "control"})
    meta["region"] = meta["region"].replace({"WM": "white_matter", "GM": "grey_matter"})
    meta["age"] = pd.to_numeric(meta.get("age"), errors="coerce")
    meta["patient"] = meta.get("patient", pd.Series(index=meta.index, dtype=str)).astype(str)
    meta["sex_male"] = (meta.get("gender", "").astype(str).str.lower() == "m").astype(int)
    meta["disease_ms"] = (meta["disease"] == "MS").astype(int)
    meta["region_white_matter"] = (meta["region"] == "white_matter").astype(int)
    return meta


def hedges_g(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    x = x[np.isfinite(x)]
    y = y[np.isfinite(y)]
    nx = x.size
    ny = y.size
    if nx < 2 or ny < 2:
        return float("nan")
    sx = x.var(ddof=1)
    sy = y.var(ddof=1)
    pooled = ((nx - 1) * sx + (ny - 1) * sy) / (nx + ny - 2)
    if pooled <= 0:
        return float("nan")
    d = (x.mean() - y.mean()) / math.sqrt(pooled)
    correction = 1.0 - (3.0 / (4.0 * (nx + ny) - 9.0))
    return d * correction


def welch_contrast(values: pd.Series, meta: pd.DataFrame, contrast: str) -> dict[str, object]:
    if contrast == "MS_WM_vs_CON_WM":
        case_mask = (meta["disease"] == "MS") & (meta["region"] == "white_matter")
        control_mask = (meta["disease"] == "control") & (meta["region"] == "white_matter")
    elif contrast == "MS_GM_vs_CON_GM":
        case_mask = (meta["disease"] == "MS") & (meta["region"] == "grey_matter")
        control_mask = (meta["disease"] == "control") & (meta["region"] == "grey_matter")
    elif contrast == "MS_all_vs_CON_all":
        case_mask = meta["disease"] == "MS"
        control_mask = meta["disease"] == "control"
    else:
        raise ValueError(f"unknown contrast: {contrast}")

    case = values.loc[meta.loc[case_mask, "sample"]].to_numpy(dtype=float)
    control = values.loc[meta.loc[control_mask, "sample"]].to_numpy(dtype=float)
    t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
    return {
        "contrast": contrast,
        "n_case": int(np.isfinite(case).sum()),
        "n_control": int(np.isfinite(control).sum()),
        "mean_case": float(np.nanmean(case)),
        "mean_control": float(np.nanmean(control)),
        "delta_log2": float(np.nanmean(case) - np.nanmean(control)),
        "hedges_g": hedges_g(case, control),
        "welch_t": float(t_stat),
        "p": float(p_value),
    }


def adjusted_ols(values: pd.Series, meta: pd.DataFrame) -> dict[str, object]:
    if sm is None:
        return {"ols_beta_disease_ms": np.nan, "ols_p_disease_ms": np.nan, "ols_note": "statsmodels_unavailable"}
    df = meta.copy()
    df["y"] = values.loc[df["sample"]].to_numpy(dtype=float)
    design = df[["disease_ms", "region_white_matter", "age", "sex_male"]].copy()
    design = sm.add_constant(design, has_constant="add")
    valid = np.isfinite(df["y"].to_numpy()) & np.isfinite(design.to_numpy()).all(axis=1)
    if valid.sum() < 10:
        return {"ols_beta_disease_ms": np.nan, "ols_p_disease_ms": np.nan, "ols_note": "too_few_valid_samples"}
    model = sm.OLS(df.loc[valid, "y"], design.loc[valid])
    fitted = model.fit(cov_type="HC3")
    return {
        "ols_beta_disease_ms": float(fitted.params["disease_ms"]),
        "ols_p_disease_ms": float(fitted.pvalues["disease_ms"]),
        "ols_note": "HC3 robust SE; covariates disease, region, age, sex",
    }


def add_fdr(df: pd.DataFrame, p_col: str, group_cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    out[p_col.replace("p", "fdr")] = np.nan
    fdr_col = p_col.replace("p", "fdr")
    for _, idx in out.groupby(group_cols).groups.items():
        pvals = out.loc[idx, p_col].to_numpy(dtype=float)
        valid = np.isfinite(pvals)
        if valid.any():
            adjusted = np.full(pvals.shape, np.nan)
            adjusted[valid] = multipletests(pvals[valid], method="fdr_bh")[1]
            out.loc[idx, fdr_col] = adjusted
    return out


def load_expression() -> pd.DataFrame:
    expr = pd.read_csv(NORM_PATH, sep="\t", compression="gzip")
    first_col = expr.columns[0]
    expr = expr.rename(columns={first_col: "gene"}).set_index("gene")
    expr.index = expr.index.astype(str).str.strip('"')
    expr = expr.apply(pd.to_numeric, errors="coerce")
    return np.log2(expr + 1.0)


def module_scores(log_expr: pd.DataFrame, meta: pd.DataFrame) -> pd.DataFrame:
    z = log_expr.sub(log_expr.mean(axis=1), axis=0).div(log_expr.std(axis=1).replace(0, np.nan), axis=0)
    scores: dict[str, pd.Series] = {}
    for module, genes in MODULES.items():
        present = [gene for gene in genes if gene in z.index]
        if not present:
            continue
        scores[module] = z.loc[present, meta["sample"]].mean(axis=0)
    return pd.DataFrame(scores).T


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(exist_ok=True)

    meta = load_sample_metadata()
    log_expr = load_expression()

    missing_samples = sorted(set(meta["sample"]) - set(log_expr.columns))
    if missing_samples:
        raise RuntimeError(f"metadata samples missing from expression matrix: {missing_samples}")
    meta = meta.loc[meta["sample"].isin(log_expr.columns)].reset_index(drop=True)

    contrasts = ["MS_WM_vs_CON_WM", "MS_GM_vs_CON_GM", "MS_all_vs_CON_all"]

    gene_rows: list[dict[str, object]] = []
    for gene in TARGET_GENES:
        if gene not in log_expr.index:
            continue
        values = log_expr.loc[gene, meta["sample"]]
        ols = adjusted_ols(values, meta)
        for contrast in contrasts:
            row = {"feature_type": "gene", "feature": gene, **welch_contrast(values, meta, contrast), **ols}
            gene_rows.append(row)
    gene_df = pd.DataFrame(gene_rows)
    gene_df = add_fdr(gene_df, "p", ["contrast"]) if not gene_df.empty else gene_df
    gene_df = gene_df.sort_values(["contrast", "fdr", "p", "feature"])

    module_expr = module_scores(log_expr, meta)
    module_rows: list[dict[str, object]] = []
    for module in module_expr.index:
        values = module_expr.loc[module, meta["sample"]]
        present_genes = [gene for gene in MODULES[module] if gene in log_expr.index]
        ols = adjusted_ols(values, meta)
        for contrast in contrasts:
            row = {
                "feature_type": "module",
                "feature": module,
                "n_genes_present": len(present_genes),
                "genes_present": ",".join(present_genes),
                **welch_contrast(values, meta, contrast),
                **ols,
            }
            module_rows.append(row)
    module_df = pd.DataFrame(module_rows)
    module_df = add_fdr(module_df, "p", ["contrast"]) if not module_df.empty else module_df
    module_df = module_df.sort_values(["contrast", "fdr", "p", "feature"])

    sample_counts = (
        meta.groupby(["disease", "region"]).size().reset_index(name="n").sort_values(["disease", "region"])
    )
    sample_counts.to_csv(OUT / "gse111972_sample_counts.tsv", sep="\t", index=False)
    gene_df.to_csv(OUT / "gse111972_target_contrasts.tsv", sep="\t", index=False)
    module_df.to_csv(OUT / "gse111972_module_contrasts.tsv", sep="\t", index=False)

    focus_features = [
        "IFI30",
        "NAMPT",
        "CXCL10",
        "CTSD",
        "GPNMB",
        "SPP1",
        "STAT1",
        "IRF1",
        "CD74",
        "CD44",
        "CXCR4",
        "MIF",
        "DDT",
    ]
    focus_rows = gene_df[(gene_df["feature"].isin(focus_features)) & (gene_df["contrast"] == "MS_WM_vs_CON_WM")]
    module_focus = module_df[module_df["contrast"] == "MS_WM_vs_CON_WM"]
    summary = {
        "dataset": "GSE111972",
        "pubmed_id": "30867424",
        "input": str(NORM_PATH.relative_to(ROOT)),
        "random_seed": SEED,
        "n_samples": int(meta.shape[0]),
        "sample_counts": sample_counts.to_dict(orient="records"),
        "n_target_genes_tested": int(gene_df["feature"].nunique()) if not gene_df.empty else 0,
        "n_modules_tested": int(module_df["feature"].nunique()) if not module_df.empty else 0,
        "primary_contrast": "MS_WM_vs_CON_WM",
        "focus_gene_primary_results": focus_rows[
            ["feature", "delta_log2", "hedges_g", "p", "fdr", "ols_beta_disease_ms", "ols_p_disease_ms"]
        ].to_dict(orient="records"),
        "module_primary_results": module_focus[
            [
                "feature",
                "n_genes_present",
                "delta_log2",
                "hedges_g",
                "p",
                "fdr",
                "ols_beta_disease_ms",
                "ols_p_disease_ms",
            ]
        ].to_dict(orient="records"),
        "interpretation_guardrail": (
            "GSE111972 is sorted microglia from normal-appearing WM/GM, not lesion-rim spatial data; "
            "use as independent MS microglia support/contradiction only."
        ),
    }
    with (OUT / "gse111972_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
