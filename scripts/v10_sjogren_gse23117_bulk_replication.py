#!/usr/bin/env python3
"""Bulk salivary-gland replication audit for the V10 Sjogren axis split.

Inputs:
  - data/raw_v2/GSE23117_series_matrix.txt.gz
  - data/raw_v3/wave84_external_geo/GPL570.annot.gz

This is an orthogonal bulk sanity check, not a replacement for matched
single-cell compartment replication.
"""

from __future__ import annotations

import gzip
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
SERIES = ROOT / "data/raw_v2/GSE23117_series_matrix.txt.gz"
GPL = ROOT / "data/raw_v3/wave84_external_geo/GPL570.annot.gz"
OUTDIR = ROOT / "analysis/v10_sjogren_gse23117"

MODULES = {
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"],
    "hla_ii_apc": ["CD74", "HLA-DRA", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1", "HLA-DRB1"],
    "mif_cd74_receptor_state": ["MIF", "CD74", "CD44", "CXCR4", "HLA-DRA", "HLA-DPA1"],
    "lipid_loader_repair": ["APOE", "LPL", "TREM2", "GPNMB", "LIPA", "ABCA1", "ABCG1", "PLIN2"],
    "lysosomal_apc": ["CTSS", "CTSB", "LAMP1", "LAMP2", "IFI30", "TYROBP", "TREM2", "APOE"],
    "hif_nampt_metabolic": ["HIF1A", "NAMPT", "SLC2A1", "LDHA", "HK2", "VEGFA"],
}


def parse_series() -> tuple[pd.DataFrame, pd.DataFrame]:
    metadata_rows: dict[str, list[list[str]]] = {}
    table_lines: list[str] = []
    in_table = False
    with gzip.open(SERIES, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line == "!series_matrix_table_begin":
                in_table = True
                continue
            if line == "!series_matrix_table_end":
                break
            if in_table:
                table_lines.append(line)
                continue
            if line.startswith("!Sample_"):
                parts = [p.strip().strip('"') for p in line.split("\t")]
                metadata_rows.setdefault(parts[0], []).append(parts[1:])

    if not table_lines:
        raise RuntimeError("No series matrix table found")

    from io import StringIO

    expr = pd.read_csv(StringIO("\n".join(table_lines)), sep="\t")
    expr = expr.rename(columns={expr.columns[0]: "probe"})
    expr["probe"] = expr["probe"].str.strip('"')
    for col in expr.columns[1:]:
        expr[col] = pd.to_numeric(expr[col], errors="coerce")

    samples = metadata_rows["!Sample_geo_accession"][0]
    titles = metadata_rows["!Sample_title"][0]
    disease = titles
    for row in metadata_rows.get("!Sample_characteristics_ch1", []):
        if len(row) == len(samples) and any("disease status:" in value for value in row):
            disease = [value.replace("disease status:", "").strip() for value in row]
            break
    meta = pd.DataFrame({"sample": samples, "title": titles, "disease_raw": disease})
    meta["group"] = "exclude"
    meta.loc[meta["disease_raw"].str.contains("non-SS control", case=False), "group"] = "control"
    ss_mask = meta["disease_raw"].str.contains("early SS|moderate SS|advanced SS", case=False)
    meta.loc[ss_mask, "group"] = "case"
    return expr, meta


def parse_gpl() -> pd.DataFrame:
    rows = []
    in_table = False
    with gzip.open(GPL, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line == "!platform_table_begin":
                in_table = True
                header = next(handle).rstrip("\n").split("\t")
                continue
            if line == "!platform_table_end":
                break
            if in_table:
                parts = line.split("\t")
                if len(parts) >= len(header):
                    rows.append(parts[: len(header)])
    annot = pd.DataFrame(rows, columns=header)
    annot = annot[["ID", "Gene symbol"]].rename(columns={"ID": "probe", "Gene symbol": "gene_symbol"})
    annot["gene_symbol"] = annot["gene_symbol"].fillna("").astype(str)
    annot = annot.assign(gene=annot["gene_symbol"].str.split("///")).explode("gene")
    annot["gene"] = annot["gene"].str.strip()
    annot = annot[annot["gene"].ne("")]
    return annot[["probe", "gene"]].drop_duplicates()


def hedges_g(case: np.ndarray, control: np.ndarray) -> float:
    n1, n0 = len(case), len(control)
    if n1 < 2 or n0 < 2:
        return np.nan
    s1 = np.var(case, ddof=1)
    s0 = np.var(control, ddof=1)
    pooled = ((n1 - 1) * s1 + (n0 - 1) * s0) / (n1 + n0 - 2)
    if pooled <= 0:
        return np.nan
    d = (np.mean(case) - np.mean(control)) / np.sqrt(pooled)
    correction = 1 - (3 / (4 * (n1 + n0) - 9))
    return float(d * correction)


def bh(pvals: list[float]) -> list[float]:
    p = np.asarray(pvals, dtype=float)
    order = np.argsort(p)
    ranked = np.empty_like(p)
    prev = 1.0
    n = len(p)
    for i in range(n - 1, -1, -1):
        idx = order[i]
        val = p[idx] * n / (i + 1)
        prev = min(prev, val)
        ranked[idx] = min(prev, 1.0)
    return ranked.tolist()


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    expr, meta = parse_series()
    annot = parse_gpl()
    merged = expr.merge(annot, on="probe", how="inner")
    sample_cols = [c for c in expr.columns if c != "probe"]
    gene_expr = merged.groupby("gene")[sample_cols].median()
    gene_expr = np.log2(gene_expr + 1.0)

    usable_meta = meta[meta["group"].isin(["case", "control"])].copy()
    case_samples = usable_meta.loc[usable_meta["group"].eq("case"), "sample"].tolist()
    control_samples = usable_meta.loc[usable_meta["group"].eq("control"), "sample"].tolist()

    rows = []
    module_scores = {}
    for module, genes in MODULES.items():
        present = [g for g in genes if g in gene_expr.index]
        missing = [g for g in genes if g not in gene_expr.index]
        scores = gene_expr.loc[present, usable_meta["sample"]].mean(axis=0)
        module_scores[module] = scores
        case = scores[case_samples].to_numpy()
        control = scores[control_samples].to_numpy()
        p = stats.ttest_ind(case, control, equal_var=False).pvalue
        rows.append(
            {
                "module": module,
                "n_genes": len(genes),
                "n_present": len(present),
                "genes_present": ";".join(present),
                "genes_missing": ";".join(missing),
                "n_case": len(case),
                "n_control": len(control),
                "case_mean": float(np.mean(case)),
                "control_mean": float(np.mean(control)),
                "delta": float(np.mean(case) - np.mean(control)),
                "hedges_g": hedges_g(case, control),
                "p": float(p),
            }
        )

    results = pd.DataFrame(rows)
    results["fdr"] = bh(results["p"].tolist())
    results.to_csv(OUTDIR / "module_results.tsv", sep="\t", index=False)
    usable_meta.to_csv(OUTDIR / "sample_groups.tsv", sep="\t", index=False)

    report = [
        "# GSE23117 Sjogren Bulk Replication Audit",
        "",
        "Comparison: non-SS controls versus early/moderate/advanced SS minor salivary gland.",
        "",
        "Excluded sample: `SS gland, control gland, patient 1` because it is not a clean non-SS control.",
        "",
        f"Cases: `{len(case_samples)}`; controls: `{len(control_samples)}`.",
        "",
        "## Module Results",
        "",
        results.sort_values("module").to_csv(sep="\t", index=False),
        "",
        "## Interpretation Guardrail",
        "",
        "This is bulk tissue. It can support cross-dataset directionality but cannot resolve whether signal originates in epithelium, APC, or infiltrating immune composition.",
    ]
    (OUTDIR / "REPORT.md").write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
