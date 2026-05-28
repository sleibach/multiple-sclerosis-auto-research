#!/usr/bin/env python3
"""Analyze E-MTAB-12260 MS pregnancy T-cell RNA-seq module trajectories."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[1]
SDRF = ROOT / "data/raw/E-MTAB-12260/E-MTAB-12260.sdrf.txt"
SAMPLES = ROOT / "data/raw/E-MTAB-12260/samples"
OUT = ROOT / "results/pregnancy_dimension/emt12260_ms_tcells"

MODULES = {
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"],
    "mif_cd74_receptor_state": ["MIF", "CD74", "CD44", "CXCR4", "HLA-DRA", "HLA-DRB1"],
    "hla_ii_only": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"],
    "lysosomal_apc": ["CTSS", "CTSB", "LAMP1", "LAMP2", "IFI30", "TYROBP", "TREM2", "APOE"],
    "monocyte_cd64": ["FCGR1A", "FCGR1B", "JAK2", "STAT1", "IL8", "CXCL2", "CD38", "PTX3"],
    "trafficking_th": ["CXCR3", "CCR6", "ITGA4", "SELL", "S1PR1"],
    "regulatory_pregnancy": ["FOXP3", "IL10", "TGFB1", "IL2RA", "CTLA4", "IKZF2"],
}

TIME_ORDER = ["before pregnancy", "1st trimester", "2nd trimester", "3rd trimester", "postpartum"]


def md_tsv(frame: pd.DataFrame) -> str:
    return "```tsv\n" + frame.to_csv(sep="\t", index=False) + "```"


def read_counts(filename: str) -> pd.Series | None:
    path = SAMPLES / filename
    frame = pd.read_csv(path, sep="\t")
    if not {"gene", "count"}.issubset(frame.columns):
        return None
    frame = frame.groupby("gene", as_index=True)["count"].sum()
    return frame


def hedges_g(a: pd.Series, b: pd.Series) -> float:
    a = a.dropna().astype(float)
    b = b.dropna().astype(float)
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    n1, n2 = len(a), len(b)
    pooled = np.sqrt(((n1 - 1) * a.var(ddof=1) + (n2 - 1) * b.var(ddof=1)) / (n1 + n2 - 2))
    if pooled == 0:
        return float("nan")
    d = (a.mean() - b.mean()) / pooled
    correction = 1 - (3 / (4 * (n1 + n2) - 9))
    return float(d * correction)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = pd.read_csv(SDRF, sep="\t")
    meta = meta.rename(
        columns={
            "Characteristics[disease]": "disease",
            "Characteristics[sampling time point]": "timepoint",
            "Characteristics[cell type]": "cell_type",
            "Characteristics[stimulus]": "stimulus",
            "Characteristics[individual]": "individual",
            "Derived Array Data File": "file",
        }
    )
    meta = meta[["disease", "timepoint", "cell_type", "stimulus", "individual", "file"]].copy()
    meta = meta[meta["file"].map(lambda x: (SAMPLES / x).exists())].reset_index(drop=True)
    meta = meta.drop_duplicates(subset=["file"]).reset_index(drop=True)

    counts = []
    excluded = []
    kept_files = []
    for row in meta.itertuples(index=False):
        sample_counts = read_counts(row.file)
        if sample_counts is None:
            excluded.append({"file": row.file, "reason": "not_gene_count_table"})
            continue
        counts.append(sample_counts.rename(row.file))
        kept_files.append(row.file)
    meta = meta[meta["file"].isin(kept_files)].reset_index(drop=True)
    count_mat = pd.concat(counts, axis=1).fillna(0)
    lib_sizes = count_mat.sum(axis=0)
    log_cpm = np.log2((count_mat / lib_sizes) * 1_000_000 + 1)

    module_rows = []
    gene_rows = []
    for module, genes in MODULES.items():
        present = [g for g in genes if g in log_cpm.index]
        missing = sorted(set(genes) - set(present))
        gene_rows.append({"module": module, "n_genes": len(genes), "present": ",".join(present), "missing": ",".join(missing)})
        if len(present) == 0:
            continue
        expr = log_cpm.loc[present].T
        z = (expr - expr.mean(axis=0)) / expr.std(axis=0, ddof=0).replace(0, np.nan)
        scores = z.mean(axis=1)
        for sample, score in scores.items():
            module_rows.append({"file": sample, "module": module, "score": float(score)})

    scores = pd.DataFrame(module_rows).merge(meta, on="file", how="left")
    lib_size_map = {str(k): float(v) for k, v in lib_sizes.items()}
    scores["log_library_size"] = scores["file"].map(lambda f: np.log2(lib_size_map[f]))
    scores["timepoint"] = pd.Categorical(scores["timepoint"], categories=TIME_ORDER, ordered=True)
    scores["cell_type_short"] = scores["cell_type"].str.replace(", alpha-beta T cell", "", regex=False)

    mean_table = (
        scores.groupby(["disease", "timepoint", "cell_type_short", "stimulus", "module"], observed=True)
        .agg(n=("score", "size"), mean=("score", "mean"), sd=("score", "std"))
        .reset_index()
    )
    mean_table.to_csv(OUT / "module_means.tsv", sep="\t", index=False)
    pd.DataFrame(gene_rows).to_csv(OUT / "module_gene_coverage.tsv", sep="\t", index=False)
    pd.DataFrame(excluded).to_csv(OUT / "excluded_files.tsv", sep="\t", index=False)

    contrast_rows = []
    for (disease, module), sub in scores.groupby(["disease", "module"], observed=True):
        for a, b in [("3rd trimester", "before pregnancy"), ("postpartum", "3rd trimester"), ("postpartum", "before pregnancy")]:
            aa = sub[sub["timepoint"] == a]["score"]
            bb = sub[sub["timepoint"] == b]["score"]
            if len(aa) >= 2 and len(bb) >= 2:
                stat = st.ttest_ind(aa, bb, equal_var=False)
                contrast_rows.append(
                    {
                        "disease": disease,
                        "module": module,
                        "contrast": f"{a} - {b}",
                        "n_a": len(aa),
                        "n_b": len(bb),
                        "mean_a": aa.mean(),
                        "mean_b": bb.mean(),
                        "delta": aa.mean() - bb.mean(),
                        "hedges_g": hedges_g(aa, bb),
                        "welch_p": stat.pvalue,
                    }
                )

    contrasts = pd.DataFrame(contrast_rows)
    contrasts.to_csv(OUT / "timepoint_contrasts.tsv", sep="\t", index=False)

    model_rows = []
    ms = scores[scores["disease"] == "multiple sclerosis"].copy()
    for module, sub in ms.groupby("module", observed=True):
        fit = smf.ols(
            "score ~ C(timepoint, Treatment(reference='before pregnancy')) + C(cell_type_short) + C(stimulus) + log_library_size",
            data=sub,
        ).fit(cov_type="cluster", cov_kwds={"groups": sub["individual"]})
        for term, coef in fit.params.items():
            if "C(timepoint" in term:
                model_rows.append(
                    {
                        "disease": "multiple sclerosis",
                        "module": module,
                        "term": term,
                        "coef": coef,
                        "se": fit.bse[term],
                        "p": fit.pvalues[term],
                        "n": int(fit.nobs),
                        "r2": fit.rsquared,
                    }
                )
    model_terms = pd.DataFrame(model_rows)
    model_terms.to_csv(OUT / "ms_ols_clustered_terms.tsv", sep="\t", index=False)

    summary = {
        "dataset": "E-MTAB-12260",
        "n_samples": int(len(meta)),
        "excluded_files": excluded,
        "n_genes": int(log_cpm.shape[0]),
        "analysis_scope": "sorted CD4/CD8 T cells from MS and normal pregnancy; not PBMC APC",
        "key_ms_contrasts": contrasts[(contrasts["disease"] == "multiple sclerosis") & (contrasts["contrast"].isin(["3rd trimester - before pregnancy", "postpartum - 3rd trimester"]))].to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))

    report = [
        "# E-MTAB-12260 MS Pregnancy T-cell Module Validation",
        "",
        "## Scope",
        "This analysis tests whether the V4/V5 MS PBMC late-pregnancy IFN/APC signal appears in an independent MS pregnancy RNA-seq cohort of sorted T cells. Because the data are CD4/CD8 T-cell fractions, APC conclusions are deliberately not transferred directly.",
        "",
        f"Samples analyzed: {len(meta)}. Genes in count matrix: {log_cpm.shape[0]}.",
        "",
        "## Key MS Contrasts",
        md_tsv(
            contrasts[(contrasts["disease"] == "multiple sclerosis") & (contrasts["contrast"].isin(["3rd trimester - before pregnancy", "postpartum - 3rd trimester"]))]
            .sort_values(["module", "contrast"])
        ),
        "",
        "## Covariate-Adjusted MS Timepoint Terms",
        "OLS with cell type, stimulus, and log library size covariates; standard errors clustered by individual.",
        md_tsv(model_terms.sort_values(["module", "term"])),
        "",
        "## Interpretation Guardrail",
        "A null or opposite result here would not refute a PBMC monocyte/APC mechanism, but it would argue against a pan-lymphocyte explanation for the GSE17410 month-9 signal.",
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
