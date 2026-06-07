#!/usr/bin/env python3
"""Ground V35 complement/lipid progressive axis on GSE180759.

Streams selected genes from the local GSE180759 single-nucleus expression matrix
and summarizes module detection/expression by pathology and cell type.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v35_complement_lipid_progressive"
OUT.mkdir(parents=True, exist_ok=True)

MATRIX = ROOT / "data/raw/GSE180759_expression_matrix.csv.gz"
ANNOT = ROOT / "data/raw/GSE180759_annotation.txt.gz"

MODULES = {
    "complement_phagocytosis": ["C1QA", "C1QB", "C1QC", "C3", "ITGAM", "ITGB2", "TYROBP", "AIF1"],
    "lipid_repair": ["APOE", "LPL", "TREM2", "ABCA1", "ABCG1", "SPP1", "LGALS3", "GPNMB"],
    "ifn_hla_apc": ["STAT1", "IRF1", "CXCL10", "ISG15", "CD74", "HLA-DRA", "HLA-DPA1"],
}


def main() -> None:
    annot = pd.read_csv(ANNOT, sep="\t")
    wanted = {g for genes in MODULES.values() for g in genes}
    rows = []
    with gzip.open(MATRIX, "rt") as handle:
        header = handle.readline().rstrip("\n").split(",")
        for line in handle:
            gene, rest = line.rstrip("\n").split(",", 1)
            if gene not in wanted:
                continue
            vals = pd.Series(rest.split(","), dtype="float32")
            vals.index = header
            df = pd.DataFrame({"nucleus_barcode": header, "expr": vals.values})
            df = df.merge(annot[["nucleus_barcode", "pathology", "cell_type"]], on="nucleus_barcode", how="left")
            grouped = df.groupby(["pathology", "cell_type"], dropna=False)["expr"].agg(
                n="size",
                pct_detected=lambda x: float((x > 0).mean()),
                mean_expr="mean",
            ).reset_index()
            grouped["gene"] = gene
            rows.append(grouped)
    gene_summary = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    gene_summary.to_csv(OUT / "selected_gene_by_pathology_celltype.tsv", sep="\t", index=False)

    module_rows = []
    for module, genes in MODULES.items():
        sub = gene_summary[gene_summary["gene"].isin(genes)].copy()
        if sub.empty:
            continue
        agg = sub.groupby(["pathology", "cell_type"]).agg(
            n_genes_present=("gene", "nunique"),
            mean_pct_detected=("pct_detected", "mean"),
            mean_expr=("mean_expr", "mean"),
        ).reset_index()
        agg["module"] = module
        module_rows.append(agg)
    module_summary = pd.concat(module_rows, ignore_index=True) if module_rows else pd.DataFrame()
    module_summary.to_csv(OUT / "module_by_pathology_celltype.tsv", sep="\t", index=False)

    micro = module_summary[module_summary["cell_type"].str.contains("micro|mac", case=False, na=False)]
    top = micro.sort_values(["module", "mean_expr"], ascending=[True, False]).groupby("module").head(5)
    top.to_csv(OUT / "microglia_macrophage_module_top.tsv", sep="\t", index=False)

    result = {
        "grounded_result": "computed_module_context_not_yet_statistically_tested",
        "n_selected_genes_found": int(gene_summary["gene"].nunique()) if not gene_summary.empty else 0,
        "modules": sorted(MODULES),
        "pathologies": sorted([str(x) for x in annot["pathology"].dropna().unique()]),
        "cell_types": sorted([str(x) for x in annot["cell_type"].dropna().unique()])[:20],
        "next_test": "Use module_by_pathology_celltype.tsv to compare chronic_active_MS_lesion_edge against control/other pathology within microglia/macrophage-like cell types with permutation over nuclei or donor-aware tests if donor labels support it.",
    }
    (OUT / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
