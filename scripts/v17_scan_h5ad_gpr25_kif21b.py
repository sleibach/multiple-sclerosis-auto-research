#!/usr/bin/env python3
"""Scan local h5ad atlases for GPR25/KIF21B/CXCL17 expression.

This reproduces the V17 h5ad tables:

- analysis/v17_gpr25_mechanism/h5ad_gene_presence_expression.tsv
- analysis/v17_gpr25_mechanism/h5ad_gene_expression_by_celltype.tsv

The script intentionally avoids downloading data. It scans the local h5ad
files accumulated by earlier project phases.
"""

from __future__ import annotations

from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v17_gpr25_mechanism"

GENES = {
    "GPR25": {"GPR25", "ENSG00000170128"},
    "KIF21B": {"KIF21B", "ENSG00000116852"},
    "CXCL17": {"CXCL17", "ENSG00000189377"},
}

DATASETS = [
    ("ibd_human_10x", ROOT / "data/raw_v3/cell_state/ibd_human_10x.h5ad"),
    (
        "ibd_gse282122_myeloid",
        ROOT / "data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad",
    ),
    ("ra_binvignat_blood", ROOT / "data/raw_v3/cell_state/ra_binvignat_blood.h5ad"),
    ("sjogren_salivary", ROOT / "data/raw_v3/cell_state/sjogren_salivary.h5ad"),
    ("psoriasis_skin", ROOT / "data/raw_v3/cell_state/psoriasis_skin.h5ad"),
]

CELLTYPE_COLUMNS = [
    "cell_type",
    "celltype",
    "cell.type",
    "CellType",
    "cell_type_major",
    "major_cell_type",
    "majority_voting",
    "annotation",
    "cluster",
    "seurat_clusters",
]


def _as_dense_vector(x) -> np.ndarray:
    if hasattr(x, "toarray"):
        return np.asarray(x.toarray()).ravel()
    return np.asarray(x).ravel()


def _gene_indices(adata, aliases: set[str]) -> list[int]:
    names = pd.Index(adata.var_names.astype(str))
    hits = [i for i, name in enumerate(names) if name in aliases]
    for column in ["gene_symbols", "gene_symbol", "feature_name", "name"]:
        if column in adata.var:
            values = adata.var[column].astype(str)
            hits.extend(i for i, value in enumerate(values) if value in aliases)
    return sorted(set(hits))


def _celltype_column(adata) -> str | None:
    for column in CELLTYPE_COLUMNS:
        if column in adata.obs:
            return column
    return None


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dataset_rows = []
    celltype_rows = []

    for dataset_name, path in DATASETS:
        if not path.exists():
            for gene in GENES:
                dataset_rows.append(
                    {
                        "dataset": dataset_name,
                        "path": str(path.relative_to(ROOT)),
                        "gene": gene,
                        "status": "missing_file",
                        "n_cells": 0,
                        "n_features": 0,
                        "feature_hits": 0,
                        "pct_detected": np.nan,
                        "mean_expression": np.nan,
                    }
                )
            continue

        adata = ad.read_h5ad(path, backed="r")
        n_cells, n_features = adata.n_obs, adata.n_vars
        celltype_col = _celltype_column(adata)

        for gene, aliases in GENES.items():
            indices = _gene_indices(adata, aliases)
            if not indices:
                dataset_rows.append(
                    {
                        "dataset": dataset_name,
                        "path": str(path.relative_to(ROOT)),
                        "gene": gene,
                        "status": "gene_absent",
                        "n_cells": n_cells,
                        "n_features": n_features,
                        "feature_hits": 0,
                        "pct_detected": 0.0,
                        "mean_expression": 0.0,
                    }
                )
                continue

            expr = np.zeros(n_cells, dtype=float)
            for idx in indices:
                expr += _as_dense_vector(adata.X[:, idx])

            dataset_rows.append(
                {
                    "dataset": dataset_name,
                    "path": str(path.relative_to(ROOT)),
                    "gene": gene,
                    "status": "ok",
                    "n_cells": n_cells,
                    "n_features": n_features,
                    "feature_hits": len(indices),
                    "pct_detected": float(np.mean(expr > 0)),
                    "mean_expression": float(np.mean(expr)),
                }
            )

            if celltype_col is None:
                continue
            groups = adata.obs[celltype_col].astype(str).to_numpy()
            for celltype in sorted(pd.unique(groups)):
                vals = expr[groups == celltype]
                celltype_rows.append(
                    {
                        "dataset": dataset_name,
                        "celltype_column": celltype_col,
                        "celltype": celltype,
                        "gene": gene,
                        "n_cells": int(len(vals)),
                        "pct_detected": float(np.mean(vals > 0)),
                        "mean_expression": float(np.mean(vals)),
                    }
                )

        adata.file.close()

    pd.DataFrame(dataset_rows).to_csv(
        OUT / "h5ad_gene_presence_expression.tsv", sep="\t", index=False
    )
    pd.DataFrame(celltype_rows).to_csv(
        OUT / "h5ad_gene_expression_by_celltype.tsv", sep="\t", index=False
    )


if __name__ == "__main__":
    main()
