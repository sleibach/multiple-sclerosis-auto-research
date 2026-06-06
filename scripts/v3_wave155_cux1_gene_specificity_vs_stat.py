#!/usr/bin/env python3
"""Wave155: gene-level CUX1 specificity versus STAT3/STAT4 in GSE129487."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


SEED = 20260527
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "interface_perturbation_geo"
OUT = ROOT / "phases/v3/results" / "wave155_cux1_gene_specificity_vs_stat"
OUT.mkdir(parents=True, exist_ok=True)

MODULES: dict[str, list[str]] = {
    "epithelial_chemokine_entry": ["CXCL1", "CXCL2", "CXCL3", "CXCL5", "CXCL8", "CCL20", "ICAM1", "SELE", "SAA1", "SAA2"],
    "stromal_retention_fibrosis": ["PDPN", "VCAM1", "ICAM1", "SERPINE1", "COL1A1", "COL1A2", "COL3A1", "ITGA5", "ITGB1", "CXCL12", "MMP3", "MMP9"],
    "endothelial_entry": ["VCAM1", "ICAM1", "SELE", "ANGPT2", "CXCL10", "CXCL11", "CCL2", "ACKR1", "VWF", "PECAM1"],
    "tls_lymphoid_niche": ["CXCL13", "CCL19", "CCL21", "LTBR", "TNFSF14", "TNFRSF14", "PDPN", "CXCL12", "ICAM1", "VCAM1"],
}


def symbol_map() -> dict[str, str]:
    hgnc = pd.read_csv(RAW / "hgnc_complete_set.txt", sep="\t", dtype=str)
    out: dict[str, str] = {}
    for _, row in hgnc.iterrows():
        ens = str(row.get("ensembl_gene_id", "")).strip()
        sym = str(row.get("symbol", "")).strip()
        if ens and sym and ens != "nan":
            out[ens.split(".")[0]] = sym.upper()
    return out


def paired(values: list[float]) -> tuple[float, float]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if len(arr) < 3:
        return (float(np.nanmean(arr)) if len(arr) else np.nan, np.nan)
    return float(np.nanmean(arr)), float(stats.ttest_1samp(arr, 0.0).pvalue)


def bh(pvalues: pd.Series) -> pd.Series:
    valid = pvalues.notna()
    q = pd.Series(np.nan, index=pvalues.index, dtype=float)
    p = pvalues[valid].astype(float)
    if p.empty:
        return q
    order = np.argsort(p.values)
    ranks = np.empty_like(order)
    ranks[order] = np.arange(1, len(p) + 1)
    q.loc[valid] = np.minimum(1.0, p.values * len(p) / ranks)
    return q


def main() -> None:
    smap = symbol_map()
    tpm = pd.read_csv(RAW / "GSE129487_rnaseq-data-2_gene-tpm.tsv.gz", sep="\t", compression="gzip")
    meta = pd.read_csv(RAW / "GSE129487_rnaseq-data-2_metadata.tsv.gz", sep="\t", compression="gzip", keep_default_na=False)
    tpm["symbol"] = tpm["ID_REF"].astype(str).str.split(".").str[0].map(smap)
    tpm = tpm.dropna(subset=["symbol"])
    samples = [c for c in tpm.columns if c.startswith("S")]
    expr = np.log2(tpm.groupby("symbol")[samples].sum(min_count=1) + 1.0)

    gene_to_modules: dict[str, list[str]] = {}
    for module, genes in MODULES.items():
        for gene in genes:
            gene_to_modules.setdefault(gene, []).append(module)
    genes = sorted(g for g in gene_to_modules if g in expr.index)

    long = expr.loc[genes].T.reset_index().rename(columns={"index": "sample"})
    long = long.merge(meta, on="sample", how="left")

    rows = []
    for gene in genes:
        for stim in ["TNF (1)", "TNF (1) + IL17 (1)"]:
            for time in [1, 6, 16]:
                induction_vals = []
                for donor in sorted(long["donor"].unique()):
                    base = long[(long["donor"] == donor) & (long["sirna"] == "Ctrl") & (long["time"] == 0) & (long["stimulation"] == "None")][gene].mean()
                    stimv = long[(long["donor"] == donor) & (long["sirna"] == "Ctrl") & (long["time"] == time) & (long["stimulation"] == stim)][gene].mean()
                    induction_vals.append(stimv - base)
                ind_mean, ind_p = paired(induction_vals)
                if not (np.isfinite(ind_mean) and ind_mean > 0 and np.isfinite(ind_p) and ind_p < 0.05):
                    continue
                effects: dict[str, tuple[float, float]] = {}
                for sirna in ["CUX1", "LIFR", "ELF3", "STAT3", "STAT4"]:
                    vals = []
                    for donor in sorted(long["donor"].unique()):
                        ctrl = long[(long["donor"] == donor) & (long["sirna"] == "Ctrl") & (long["time"] == time) & (long["stimulation"] == stim)][gene].mean()
                        kd = long[(long["donor"] == donor) & (long["sirna"] == sirna) & (long["time"] == time) & (long["stimulation"] == stim)][gene].mean()
                        vals.append(kd - ctrl)
                    effects[sirna] = paired(vals)
                cux1_mean, cux1_p = effects["CUX1"]
                stat3_mean, stat3_p = effects["STAT3"]
                stat4_mean, stat4_p = effects["STAT4"]
                rows.append(
                    {
                        "gene": gene,
                        "modules": ";".join(gene_to_modules[gene]),
                        "stimulation": stim,
                        "time": time,
                        "ctrl_induction_mean": ind_mean,
                        "ctrl_induction_p": ind_p,
                        "cux1_effect": cux1_mean,
                        "cux1_p": cux1_p,
                        "stat3_effect": stat3_mean,
                        "stat3_p": stat3_p,
                        "stat4_effect": stat4_mean,
                        "stat4_p": stat4_p,
                        "lifr_effect": effects["LIFR"][0],
                        "lifr_p": effects["LIFR"][1],
                        "elf3_effect": effects["ELF3"][0],
                        "elf3_p": effects["ELF3"][1],
                    }
                )
    df = pd.DataFrame(rows)
    if not df.empty:
        for col in ["ctrl_induction_p", "cux1_p", "stat3_p", "stat4_p", "lifr_p", "elf3_p"]:
            df[col.replace("_p", "_q")] = bh(df[col])
        df["cux1_nominal_suppressed"] = (df["cux1_effect"] < 0) & (df["cux1_p"] < 0.05)
        df["stat3_nominal_suppressed"] = (df["stat3_effect"] < 0) & (df["stat3_p"] < 0.05)
        df["stat4_nominal_suppressed"] = (df["stat4_effect"] < 0) & (df["stat4_p"] < 0.05)
        df["cux1_selective_nominal"] = df["cux1_nominal_suppressed"] & ~df["stat3_nominal_suppressed"] & ~df["stat4_nominal_suppressed"]
    df.to_csv(OUT / "module_gene_specificity_tests.tsv", sep="\t", index=False)

    summary_by_gene = []
    if not df.empty:
        for gene, grp in df.groupby("gene"):
            summary_by_gene.append(
                {
                    "gene": gene,
                    "modules": ";".join(sorted(set(";".join(grp["modules"]).split(";")))),
                    "n_induced_contexts": int(len(grp)),
                    "n_cux1_nominal_suppressed": int(grp["cux1_nominal_suppressed"].sum()),
                    "n_cux1_selective_nominal": int(grp["cux1_selective_nominal"].sum()),
                    "mean_cux1_effect": float(grp["cux1_effect"].mean()),
                    "mean_stat3_effect": float(grp["stat3_effect"].mean()),
                    "mean_stat4_effect": float(grp["stat4_effect"].mean()),
                }
            )
    gene_summary = pd.DataFrame(summary_by_gene).sort_values(["n_cux1_selective_nominal", "n_cux1_nominal_suppressed", "mean_cux1_effect"], ascending=[False, False, True])
    gene_summary.to_csv(OUT / "gene_specificity_summary.tsv", sep="\t", index=False)

    n_selective = int(df["cux1_selective_nominal"].sum()) if not df.empty else 0
    branch = "CUX1_HAS_NOMINAL_NONSTAT_INTERFACE_GENE_SUBSET" if n_selective else "CUX1_EFFECT_NOT_SEPARABLE_FROM_STAT_AT_NOMINAL_LEVEL"
    summary = {
        "branch_call": branch,
        "random_seed": SEED,
        "n_induced_gene_contexts": int(df.shape[0]),
        "n_cux1_nominal_suppressed_gene_contexts": int(df["cux1_nominal_suppressed"].sum()) if not df.empty else 0,
        "n_cux1_selective_nominal_gene_contexts": n_selective,
        "top_gene_summary": gene_summary.head(15).to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUT / "REPORT.md").write_text(
        "# Wave155 CUX1 Gene Specificity Versus STAT\n\n"
        f"Branch call: `{branch}`.\n\n"
        "This wave tests individual genes in the recurrent interface modules. A CUX1-selective nominal "
        "gene-context is induced under control siRNA, suppressed by CUX1 siRNA at p<0.05, and not suppressed "
        "by STAT3 or STAT4 siRNA at p<0.05 in the same context.\n"
    )


if __name__ == "__main__":
    main()
