#!/usr/bin/env python3
"""Analyze Mixscale pathway Perturb-seq DE tables for V3 APC-state wiring.

Dataset: GSE281048 / Zenodo 14035992, processed file
DE_results_all_pathway.zip. Each table is a named CRISPRi perturbation under a
cytokine pathway context, with per-cell-line log2FC and p-values.

This script tests whether perturbing IFN/TNF pathway regulators shifts the
specific readout genes in the V3 IFN/HLA-II/GILT lysosomal APC transition.
It does not treat cancer cell lines as disease tissue; it uses them as a
gene-specific perturbation wiring assay.
"""

from __future__ import annotations

import json
import re
import zipfile
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "mixscale"
OUT = ROOT / "results_v3" / "mixscale"
ZIP_PATH = RAW / "DE_results_all_pathway.zip"

PRIMARY_PERTURBATIONS = {
    "IFNG": ["IFNGR1", "IFNGR2", "JAK1", "JAK2", "STAT1", "IRF1", "RFX5", "NFKB1", "HLA-DQB1"],
    "IFNB": ["IFNAR1", "JAK1", "TYK2", "STAT1", "IRF1", "SOCS1", "NFKB1"],
    "TNFA": ["TNFRSF1A", "CHUK", "IKBKB", "IKBKG", "MAP3K7", "NFKB1", "IRF1", "RELB"],
}

READOUT_MODULES = {
    "hla_ii_apc": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQB1", "CIITA", "RFX5"],
    "gilt_lysosomal_apc": ["IFI30", "CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3", "CTSL"],
    "ifn_apc": [
        "STAT1",
        "IRF1",
        "NLRC5",
        "CIITA",
        "CXCL10",
        "GBP1",
        "GBP2",
        "TAP1",
        "TAP2",
        "B2M",
        "CD74",
        "IFI30",
    ],
    "mif_cd74_receptor_state": ["CD74", "CD44", "CXCR4", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1"],
}

ALL_READOUTS = sorted({gene for genes in READOUT_MODULES.values() for gene in genes})


def list_relevant_members() -> list[tuple[str, str, str]]:
    pattern = re.compile(r"DE_results_all_pathway/Parse_([^/]+)/([^/_]+)_\1_pathway_DE_results\.txt$")
    rows = []
    with zipfile.ZipFile(ZIP_PATH) as zf:
        for name in zf.namelist():
            match = pattern.match(name)
            if not match:
                continue
            cytokine = match.group(1).replace("Parse_", "")
            perturbation = match.group(2)
            cytokine = cytokine.removeprefix("Parse_")
            pathway = name.split("/")[1].replace("Parse_", "")
            perturbation = Path(name).name.split(f"_{pathway}_pathway_DE_results.txt")[0]
            if perturbation in PRIMARY_PERTURBATIONS.get(pathway, []):
                rows.append((pathway, perturbation, name))
    return sorted(rows)


def read_member(zf: zipfile.ZipFile, member: str) -> pd.DataFrame:
    with zf.open(member) as handle:
        data = handle.read()
    return pd.read_csv(BytesIO(data), sep=r"\s+", na_values=["NA"], engine="python")


def tidy_file(pathway: str, perturbation: str, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    cell_types = sorted(column.removeprefix("log2FC_") for column in df.columns if column.startswith("log2FC_"))
    readout_rows: list[dict[str, object]] = []
    module_rows: list[dict[str, object]] = []
    for cell_type in cell_types:
        log_col = f"log2FC_{cell_type}"
        p_col = f"p_cell_type{cell_type}"
        if p_col not in df.columns:
            continue
        pvals = pd.to_numeric(df[p_col], errors="coerce")
        valid = pvals.notna()
        fdr = pd.Series(np.nan, index=df.index, dtype=float)
        if valid.sum() > 0:
            fdr.loc[valid] = multipletests(pvals.loc[valid], method="fdr_bh")[1]
        sub = pd.DataFrame(
            {
                "pathway": pathway,
                "perturbation": perturbation,
                "cell_type": cell_type,
                "gene": df["gene_ID"].astype(str),
                "log2fc": pd.to_numeric(df[log_col], errors="coerce"),
                "p": pvals,
                "fdr": fdr,
            }
        )
        readouts = sub[sub["gene"].isin(ALL_READOUTS)].copy()
        readout_rows.extend(readouts.to_dict(orient="records"))
        for module, genes in READOUT_MODULES.items():
            vals = readouts[readouts["gene"].isin(genes)].copy()
            vals = vals[vals["log2fc"].notna()]
            if vals.empty:
                module_rows.append(
                    {
                        "pathway": pathway,
                        "perturbation": perturbation,
                        "cell_type": cell_type,
                        "module": module,
                        "n_genes": 0,
                        "genes_present": "",
                        "mean_log2fc": np.nan,
                        "median_log2fc": np.nan,
                        "negative_fraction": np.nan,
                        "sig_negative_fdr05": 0,
                        "sig_positive_fdr05": 0,
                    }
                )
                continue
            module_rows.append(
                {
                    "pathway": pathway,
                    "perturbation": perturbation,
                    "cell_type": cell_type,
                    "module": module,
                    "n_genes": int(vals["gene"].nunique()),
                    "genes_present": ",".join(sorted(vals["gene"].unique())),
                    "mean_log2fc": float(vals["log2fc"].mean()),
                    "median_log2fc": float(vals["log2fc"].median()),
                    "negative_fraction": float((vals["log2fc"] < 0).mean()),
                    "sig_negative_fdr05": int(((vals["log2fc"] < 0) & (vals["fdr"] <= 0.05)).sum()),
                    "sig_positive_fdr05": int(((vals["log2fc"] > 0) & (vals["fdr"] <= 0.05)).sum()),
                }
            )
    return pd.DataFrame(readout_rows), pd.DataFrame(module_rows)


def summarize_modules(modules: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (pathway, perturbation, module), sub in modules.groupby(["pathway", "perturbation", "module"]):
        valid = sub[sub["mean_log2fc"].notna()]
        rows.append(
            {
                "pathway": pathway,
                "perturbation": perturbation,
                "module": module,
                "n_cell_types": int(valid["cell_type"].nunique()),
                "mean_module_log2fc_across_cell_types": float(valid["mean_log2fc"].mean()) if not valid.empty else np.nan,
                "median_module_log2fc_across_cell_types": float(valid["mean_log2fc"].median()) if not valid.empty else np.nan,
                "cell_type_negative_fraction": float((valid["mean_log2fc"] < 0).mean()) if not valid.empty else np.nan,
                "total_sig_negative_gene_celltype": int(valid["sig_negative_fdr05"].sum()),
                "total_sig_positive_gene_celltype": int(valid["sig_positive_fdr05"].sum()),
                "mean_genes_present": float(valid["n_genes"].mean()) if not valid.empty else np.nan,
                "cell_types": ",".join(sorted(valid["cell_type"].unique())),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["pathway", "module", "mean_module_log2fc_across_cell_types"],
        ascending=[True, True, True],
    )


def summarize_readouts(readouts: pd.DataFrame) -> pd.DataFrame:
    if readouts.empty:
        return readouts
    rows = []
    for (pathway, perturbation, gene), sub in readouts.groupby(["pathway", "perturbation", "gene"]):
        vals = sub[sub["log2fc"].notna()]
        rows.append(
            {
                "pathway": pathway,
                "perturbation": perturbation,
                "gene": gene,
                "n_cell_types": int(vals["cell_type"].nunique()),
                "mean_log2fc": float(vals["log2fc"].mean()) if not vals.empty else np.nan,
                "median_log2fc": float(vals["log2fc"].median()) if not vals.empty else np.nan,
                "negative_fraction": float((vals["log2fc"] < 0).mean()) if not vals.empty else np.nan,
                "sig_negative_fdr05": int(((vals["log2fc"] < 0) & (vals["fdr"] <= 0.05)).sum()),
                "sig_positive_fdr05": int(((vals["log2fc"] > 0) & (vals["fdr"] <= 0.05)).sum()),
            }
        )
    return pd.DataFrame(rows).sort_values(["pathway", "perturbation", "gene"])


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    relevant = list_relevant_members()
    readout_tables = []
    module_tables = []
    with zipfile.ZipFile(ZIP_PATH) as zf:
        for pathway, perturbation, member in relevant:
            df = read_member(zf, member)
            readouts, modules = tidy_file(pathway, perturbation, df)
            readout_tables.append(readouts)
            module_tables.append(modules)
    readouts = pd.concat(readout_tables, ignore_index=True) if readout_tables else pd.DataFrame()
    modules = pd.concat(module_tables, ignore_index=True) if module_tables else pd.DataFrame()
    readout_summary = summarize_readouts(readouts)
    module_summary = summarize_modules(modules)

    readouts.to_csv(OUT / "mixscale_readout_gene_effects.tsv", sep="\t", index=False)
    modules.to_csv(OUT / "mixscale_module_effects_by_cell_type.tsv", sep="\t", index=False)
    readout_summary.to_csv(OUT / "mixscale_readout_gene_summary.tsv", sep="\t", index=False)
    module_summary.to_csv(OUT / "mixscale_module_summary.tsv", sep="\t", index=False)

    primary = module_summary[
        (module_summary["pathway"].isin(["IFNG", "IFNB"]))
        & (module_summary["module"].isin(["hla_ii_apc", "ifn_apc", "gilt_lysosomal_apc", "mif_cd74_receptor_state"]))
    ].copy()
    primary = primary.sort_values(["module", "mean_module_log2fc_across_cell_types"])
    summary = {
        "random_seed": SEED,
        "dataset": "GSE281048 / Zenodo 14035992 DE_results_all_pathway.zip",
        "archive_md5_expected": "f077cba680a1affc599f5153d99b0e45",
        "n_relevant_perturbation_files": len(relevant),
        "pathways": sorted({pathway for pathway, _, _ in relevant}),
        "primary_result_top_negative_module_effects": primary.head(20).to_dict(orient="records"),
        "interpretation_guardrail": (
            "These are real gene-specific CRISPRi perturbation effects in stimulated human cancer cell lines. "
            "They test pathway wiring and readout movability, not MS microglia or autoimmune tissue efficacy."
        ),
    }
    (OUT / "mixscale_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
