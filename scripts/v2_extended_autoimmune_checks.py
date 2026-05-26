#!/usr/bin/env python3
"""Second-wave autoimmune checks after beta1 recommendations.

Adds SLE sorted-cell and Sjogren salivary gland public GEO matrices.
T1D GSE154609 was downloaded, but its GPL17692 annotation requires a
multi-gigabyte SOFT file in GEO; that path is explicitly not used here.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd

from v2_cross_autoimmune_bulk import (
    INFLAMMATION,
    LDAM_MODULE,
    MYELOID_DENSITY,
    TARGET_GENES,
    collapse_to_gene,
    module_score,
    parse_geo_annotation,
    parse_series_matrix,
    sample_meta,
    welch,
)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v2"
OUT = ROOT / "results_v2"


def contains(series: pd.Series, pattern: str) -> pd.Series:
    return series.fillna("").str.contains(pattern, case=False, regex=True)


def run_dataset(
    accession: str,
    matrix_path: Path,
    platform_path: Path,
    comparisons: list[dict[str, object]],
    limitation: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    expr, md = parse_series_matrix(matrix_path)
    ann = parse_geo_annotation(platform_path)
    gene_expr = collapse_to_gene(expr, ann)
    meta = sample_meta(md)
    gene_expr = gene_expr.loc[:, [c for c in gene_expr.columns if c in meta.index]]
    meta = meta.loc[gene_expr.columns]

    module_values = {
        "LDAM_MODULE": module_score(gene_expr, LDAM_MODULE),
        "MYELOID_DENSITY": module_score(gene_expr, MYELOID_DENSITY),
        "INFLAMMATION": module_score(gene_expr, INFLAMMATION),
    }
    target_rows = []
    module_rows = []
    for comp in comparisons:
        case = comp["case_mask"](meta)
        control = comp["control_mask"](meta)
        case_samples = meta.index[case].tolist()
        control_samples = meta.index[control].tolist()
        for gene in TARGET_GENES:
            if gene not in gene_expr.index:
                continue
            target_rows.append(
                {
                    "dataset": accession,
                    "comparison": comp["name"],
                    "feature_type": "gene",
                    "feature": gene,
                    **welch(gene_expr.loc[gene, case_samples], gene_expr.loc[gene, control_samples]),
                    "limitation": limitation,
                }
            )
        for mod, values in module_values.items():
            genes = LDAM_MODULE if mod == "LDAM_MODULE" else MYELOID_DENSITY if mod == "MYELOID_DENSITY" else INFLAMMATION
            module_rows.append(
                {
                    "dataset": accession,
                    "comparison": comp["name"],
                    "feature_type": "module",
                    "feature": mod,
                    "present_genes": ",".join([g for g in genes if g in gene_expr.index]),
                    **welch(values.loc[case_samples], values.loc[control_samples]),
                    "limitation": limitation,
                }
            )
    meta.to_csv(OUT / f"{accession.lower()}_metadata.tsv", sep="\t")
    return pd.DataFrame(target_rows), pd.DataFrame(module_rows)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    targets_all = []
    modules_all = []

    # SLE sorted immune subsets.
    t, m = run_dataset(
        "GSE10325",
        RAW / "GSE10325_series_matrix.txt.gz",
        RAW / "GPL96.annot.gz",
        [
            {
                "name": "SLE_myeloid_vs_healthy_myeloid",
                "case_mask": lambda meta: contains(meta["title"], r"^SLE myeloid"),
                "control_mask": lambda meta: contains(meta["title"], r"^healthy myeloid"),
            },
            {
                "name": "SLE_CD4_T_vs_healthy_CD4_T",
                "case_mask": lambda meta: contains(meta["title"], r"^SLE CD4"),
                "control_mask": lambda meta: contains(meta["title"], r"^healthy CD4"),
            },
            {
                "name": "SLE_CD19_B_vs_healthy_CD19_B",
                "case_mask": lambda meta: contains(meta["title"], r"^SLE CD19"),
                "control_mask": lambda meta: contains(meta["title"], r"^healthy CD19"),
            },
        ],
        "sorted peripheral blood subsets; not tissue lesions, but cell-type specific for SLE",
    )
    targets_all.append(t)
    modules_all.append(m)

    # Sjogren salivary gland, bulk tissue by disease stage.
    t, m = run_dataset(
        "GSE23117",
        RAW / "GSE23117_series_matrix.txt.gz",
        RAW / "GPL570.annot.gz",
        [
            {
                "name": "Sjogren_all_SS_vs_nonSS_control",
                "case_mask": lambda meta: contains(meta["title"], r"SS gland, (?:early|moderate|advanced)"),
                "control_mask": lambda meta: contains(meta["title"], r"non-SS control"),
            },
            {
                "name": "Sjogren_advanced_SS_vs_nonSS_control",
                "case_mask": lambda meta: contains(meta["title"], r"SS gland, advanced"),
                "control_mask": lambda meta: contains(meta["title"], r"non-SS control"),
            },
        ],
        "bulk minor salivary gland; cell-composition and inflammation confounding",
    )
    targets_all.append(t)
    modules_all.append(m)

    targets = pd.concat(targets_all, ignore_index=True)
    modules = pd.concat(modules_all, ignore_index=True)
    targets.to_csv(OUT / "extended_autoimmune_target_gene_contrasts.tsv", sep="\t", index=False)
    modules.to_csv(OUT / "extended_autoimmune_module_contrasts.tsv", sep="\t", index=False)

    key = targets[targets["feature"].isin(["ACSL1", "NAMPT", "GPNMB", "CTSD", "IFI30", "SPP1"])].copy()
    summary = {
        "datasets": ["GSE10325", "GSE23117"],
        "blocked_dataset": {
            "GSE154609": "Downloaded, but GPL17692 annotation via GEO SOFT is ~2.3GB; downscoped rather than silently escalating compute/network.",
        },
        "nampt_positive_nominal": int(((targets["feature"] == "NAMPT") & (targets["delta"] > 0) & (targets["p"] < 0.05)).sum()),
        "acsl1_positive_nominal": int(((targets["feature"] == "ACSL1") & (targets["delta"] > 0) & (targets["p"] < 0.05)).sum()),
        "ldam_positive_nominal": int(((modules["feature"] == "LDAM_MODULE") & (modules["delta"] > 0) & (modules["p"] < 0.05)).sum()),
    }
    (OUT / "extended_autoimmune_checks_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(key[["dataset", "comparison", "feature", "n_case", "n_control", "delta", "hedges_g", "p", "limitation"]].to_string(index=False))
    print(modules[["dataset", "comparison", "feature", "n_case", "n_control", "delta", "hedges_g", "p"]].to_string(index=False))


if __name__ == "__main__":
    main()
