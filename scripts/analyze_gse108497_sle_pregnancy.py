#!/usr/bin/env python3
"""Analyze GSE108497 SLE pregnancy whole-blood module trajectories."""

from __future__ import annotations

import csv
import gzip
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data/derived/GSE108497/sample_metadata.tsv"
SOFT = ROOT / "data/raw/GSE108497/GSE108497_family.soft.gz"
MATRIX = ROOT / "data/raw/GSE108497/GSE108497_normalized_data.txt.gz"
OUT = ROOT / "results/pregnancy_dimension/gse108497_sle"

MODULES = {
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"],
    "mif_cd74_receptor_state": ["MIF", "CD74", "CD44", "CXCR4", "HLA-DRA", "HLA-DRB1"],
    "hla_ii_only": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"],
    "lysosomal_apc": ["CTSS", "CTSB", "LAMP1", "LAMP2", "IFI30", "TYROBP", "TREM2", "APOE"],
    "monocyte_cd64": ["FCGR1A", "FCGR1B", "JAK2", "STAT1", "IL8", "CXCL2", "CD38", "PTX3"],
    "hif_nampt_metabolic": ["NAMPT", "HIF1A", "SLC2A1", "LDHA", "VEGFA", "NFKB1"],
    "regulatory_pregnancy": ["FOXP3", "IL10", "TGFB1", "IL2RA", "CTLA4", "IKZF2"],
}

TP_LABELS = {
    "1": "<16 weeks",
    "2": "16-23 weeks",
    "3": "24-31 weeks",
    "4": "32-40 weeks",
    "5": "8-20 weeks postpartum",
}


def parse_characteristics(text: str) -> dict[str, str]:
    values = {}
    for item in str(text).split(" | "):
        if ": " in item:
            k, v = item.split(": ", 1)
            values[k.strip()] = v.strip()
    return values


def parse_platform_symbols() -> pd.DataFrame:
    rows = []
    in_table = False
    header = None
    with gzip.open(SOFT, "rt", errors="replace") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line == "!platform_table_begin":
                in_table = True
                continue
            if line == "!platform_table_end":
                break
            if not in_table:
                continue
            if header is None:
                header = line.split("\t")
                continue
            parts = line.split("\t")
            if len(parts) == len(header):
                row = dict(zip(header, parts))
                symbol = row.get("Symbol", "").strip()
                if symbol:
                    rows.append({"ID_REF": row["ID"], "gene": symbol.split(" /// ")[0]})
    return pd.DataFrame(rows).drop_duplicates()


def md_tsv(frame: pd.DataFrame) -> str:
    return "```tsv\n" + frame.to_csv(sep="\t", index=False) + "```"


def hedges_g(a: pd.Series, b: pd.Series) -> float:
    a = a.dropna().astype(float)
    b = b.dropna().astype(float)
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    pooled = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0:
        return float("nan")
    return float(((a.mean() - b.mean()) / pooled) * (1 - 3 / (4 * (len(a) + len(b)) - 9)))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = pd.read_csv(META, sep="\t")
    char_rows = []
    for row in meta.itertuples(index=False):
        chars = parse_characteristics(row.Sample_characteristics_ch1)
        array_id = str(row.Sample_description).split("|")[0].strip()
        char_rows.append(
            {
                "geo_accession": row.geo_accession,
                "array_id": array_id,
                "title": row.Sample_title,
                "sample_name": chars.get("sample_name"),
                "donor_id": chars.get("donor_id"),
                "sle": int(chars.get("sle", "0")),
                "tp": chars.get("tp"),
                "tp_label": TP_LABELS.get(chars.get("tp"), chars.get("tp")),
                "batch": chars.get("batch"),
                "pe": int(chars.get("pe", "0")),
                "fd": int(chars.get("fd", "0")),
                "nnd": int(chars.get("nnd", "0")),
                "pl_insuff": int(chars.get("pl_insuff", "0")),
                "iugr": int(chars.get("iugr", "0")),
                "sga": int(chars.get("sga", "0")),
            }
        )
    sample_meta = pd.DataFrame(char_rows)
    sample_meta["complication_any"] = sample_meta[["pe", "fd", "nnd", "pl_insuff", "iugr", "sga"]].max(axis=1)
    sample_meta.to_csv(OUT / "sample_metadata_parsed.tsv", sep="\t", index=False)

    symbols = parse_platform_symbols()
    symbols.to_csv(OUT / "platform_probe_symbols.tsv", sep="\t", index=False)

    matrix = pd.read_csv(MATRIX, sep="\t", compression="gzip")
    expr_cols = [c for i, c in enumerate(matrix.columns) if c != "ID_REF" and c != "Detection Pval" and not c.startswith("Detection")]
    # The normalized file alternates expression and repeated "Detection Pval" columns.
    expr_cols = [c for c in matrix.columns[1:] if re.match(r"^\d+_[A-Z]$", str(c))]
    expr = matrix[["ID_REF"] + expr_cols].merge(symbols, on="ID_REF", how="inner")
    gene_expr = expr.groupby("gene", as_index=True)[expr_cols].mean()
    sample_meta = sample_meta[sample_meta["array_id"].isin(gene_expr.columns)].copy()
    gene_expr = gene_expr[sample_meta["array_id"].tolist()]
    gene_expr = np.log2(gene_expr.clip(lower=0) + 1)

    module_rows = []
    coverage = []
    for module, genes in MODULES.items():
        present = [g for g in genes if g in gene_expr.index]
        missing = sorted(set(genes) - set(present))
        coverage.append({"module": module, "n_genes": len(genes), "present": ",".join(present), "missing": ",".join(missing)})
        z = ((gene_expr.loc[present].T - gene_expr.loc[present].T.mean()) / gene_expr.loc[present].T.std(ddof=0).replace(0, np.nan)).mean(axis=1)
        for array_id, score in z.items():
            module_rows.append({"array_id": array_id, "module": module, "score": float(score)})
    pd.DataFrame(coverage).to_csv(OUT / "module_gene_coverage.tsv", sep="\t", index=False)
    scores = pd.DataFrame(module_rows).merge(sample_meta, on="array_id", how="left")
    scores.to_csv(OUT / "module_scores.tsv", sep="\t", index=False)

    means = scores.groupby(["sle", "tp", "tp_label", "complication_any", "module"], observed=True).agg(n=("score", "size"), mean=("score", "mean"), sd=("score", "std")).reset_index()
    means.to_csv(OUT / "module_timepoint_means.tsv", sep="\t", index=False)

    contrast_rows = []
    for (sle, complication, module), sub in scores.groupby(["sle", "complication_any", "module"], observed=True):
        for a, b in [("4", "1"), ("5", "4"), ("5", "1")]:
            aa = sub[sub["tp"] == a]["score"]
            bb = sub[sub["tp"] == b]["score"]
            if len(aa) >= 2 and len(bb) >= 2:
                test = st.ttest_ind(aa, bb, equal_var=False)
                contrast_rows.append(
                    {
                        "sle": sle,
                        "complication_any": complication,
                        "module": module,
                        "contrast": f"{TP_LABELS[a]} - {TP_LABELS[b]}",
                        "n_a": len(aa),
                        "n_b": len(bb),
                        "delta": aa.mean() - bb.mean(),
                        "hedges_g": hedges_g(aa, bb),
                        "welch_p": test.pvalue,
                    }
                )
    contrasts = pd.DataFrame(contrast_rows)
    contrasts.to_csv(OUT / "timepoint_contrasts.tsv", sep="\t", index=False)

    model_rows = []
    sle_scores = scores[scores["sle"] == 1].copy()
    for module, sub in sle_scores.groupby("module", observed=True):
        fit = smf.ols("score ~ C(tp, Treatment(reference='1')) + complication_any + C(batch)", data=sub).fit(
            cov_type="cluster", cov_kwds={"groups": sub["donor_id"]}
        )
        for term, coef in fit.params.items():
            if "C(tp" in term:
                model_rows.append({"module": module, "term": term, "coef": coef, "se": fit.bse[term], "p": fit.pvalues[term], "n": int(fit.nobs), "r2": fit.rsquared})
    model_terms = pd.DataFrame(model_rows)
    model_terms.to_csv(OUT / "sle_ols_clustered_terms.tsv", sep="\t", index=False)

    key = contrasts[(contrasts["sle"] == 1) & (contrasts["contrast"].isin(["32-40 weeks - <16 weeks", "8-20 weeks postpartum - 32-40 weeks"]))]
    summary = {
        "dataset": "GSE108497",
        "n_samples_mapped": int(len(sample_meta)),
        "n_genes": int(gene_expr.shape[0]),
        "key_sle_contrasts": key.to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    report = [
        "# GSE108497 SLE Pregnancy Module Trajectories",
        "",
        "## Scope",
        "Whole-blood Illumina HumanHT-12 v4 pregnancy/postpartum cohort with SLE and healthy controls. Timepoints are parsed from GEO characteristics: TP1 <16 weeks, TP2 16-23 weeks, TP3 24-31 weeks, TP4 32-40 weeks, TP5 8-20 weeks postpartum.",
        "",
        f"Mapped samples: {len(sample_meta)}. Gene symbols after probe aggregation: {gene_expr.shape[0]}.",
        "",
        "## Key SLE Contrasts",
        md_tsv(key.sort_values(["complication_any", "module", "contrast"])),
        "",
        "## SLE Covariate-Adjusted Timepoint Terms",
        "OLS with complication status and batch covariates; standard errors clustered by donor.",
        md_tsv(model_terms.sort_values(["module", "term"])),
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
