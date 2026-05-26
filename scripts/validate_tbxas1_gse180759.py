#!/usr/bin/env python3
"""Targeted lesion-edge transcript localization of the TBXAS1 pathway in GSE180759."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as st


SEED = 20260526
RAW = Path("data/raw")
OUT = Path("results")
TARGETS = [
    "TBXAS1",
    "PTGS1",
    "PTGS2",
    "TBXA2R",
    "ALOX5AP",
    "GPNMB",
    "APOE",
    "C1QA",
    "TREM2",
]
ACTIVE = "chronic_active_MS_lesion_edge"
INACTIVE = "chronic_inactive_MS_lesion_edge"
MIN_NUCLEI = 20


def stream_target_counts() -> tuple[pd.DataFrame, list[str]]:
    annotation = pd.read_csv(RAW / "GSE180759_annotation.txt.gz", sep="\t")
    expected = annotation["nucleus_barcode"].tolist()
    totals = np.zeros(len(annotation), dtype=np.float64)
    selected = {target: np.zeros(len(annotation), dtype=np.float64) for target in TARGETS}
    found: set[str] = set()
    with gzip.open(RAW / "GSE180759_expression_matrix.csv.gz", "rt") as source:
        header = source.readline().rstrip("\n").split(",")
        if header != expected:
            raise ValueError("GSE180759 expression columns do not match annotation order")
        for line in source:
            gene, values_text = line.rstrip("\n").split(",", 1)
            values = np.fromstring(values_text, sep=",", dtype=np.float64)
            if len(values) != len(annotation):
                raise ValueError(f"unexpected count length for {gene}")
            totals += values
            if gene in selected:
                selected[gene] += values
                found.add(gene)
    annotation = annotation.copy()
    annotation["library_size"] = totals
    for gene in found:
        annotation[gene] = selected[gene]
    return annotation, sorted(found)


def pseudobulk(annotation: pd.DataFrame, found: list[str], cell_type: str | None) -> pd.DataFrame:
    selected = annotation if cell_type is None else annotation.loc[annotation["cell_type"] == cell_type]
    columns = ["cell_type", "NBB_case", "pathology"] if cell_type is None else ["NBB_case", "pathology"]
    groups = selected.groupby(columns, observed=True, sort=True)
    result = groups.size().rename("n_nuclei").reset_index()
    result = result.merge(groups["library_size"].sum().rename("library_size").reset_index())
    for gene in found:
        result = result.merge(groups[gene].sum().rename(f"{gene}_raw").reset_index())
        result[gene] = np.log2(result[f"{gene}_raw"] / result["library_size"] * 1_000_000 + 1)
    return result.loc[result["n_nuclei"] >= MIN_NUCLEI].copy()


def compare_active_inactive(data: pd.DataFrame, found: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    active = data.loc[data["pathology"] == ACTIVE].set_index("NBB_case")
    inactive = data.loc[data["pathology"] == INACTIVE].set_index("NBB_case")
    donors = sorted(set(active.index) & set(inactive.index))
    records = []
    for donor in donors:
        for gene in found:
            records.append(
                {
                    "donor": donor,
                    "gene": gene,
                    "active_edge_log2_cpm1": float(active.loc[donor, gene]),
                    "inactive_edge_log2_cpm1": float(inactive.loc[donor, gene]),
                    "delta_active_minus_inactive": float(active.loc[donor, gene] - inactive.loc[donor, gene]),
                    "active_edge_n_cells": int(active.loc[donor, "n_nuclei"]),
                    "inactive_edge_n_cells": int(inactive.loc[donor, "n_nuclei"]),
                }
            )
    contrasts = pd.DataFrame(
        records,
        columns=[
            "donor",
            "gene",
            "active_edge_log2_cpm1",
            "inactive_edge_log2_cpm1",
            "delta_active_minus_inactive",
            "active_edge_n_cells",
            "inactive_edge_n_cells",
        ],
    )
    if contrasts.empty:
        return contrasts, pd.DataFrame()
    stats = []
    for gene in found:
        values = contrasts.loc[contrasts["gene"] == gene, "delta_active_minus_inactive"].to_numpy()
        if len(values) == 0:
            continue
        standard = np.std(values, ddof=1) if len(values) > 1 else np.nan
        stats.append(
            {
                "gene": gene,
                "paired_donors": int(len(values)),
                "mean_delta_active_minus_inactive": float(np.mean(values)),
                "paired_dz": float(np.mean(values) / standard) if standard > 0 else np.nan,
                "positive_fraction": float(np.mean(values > 0)),
                "wilcoxon_p": float(st.wilcoxon(values).pvalue) if np.any(values != 0) else 1.0,
            }
        )
    return contrasts, pd.DataFrame(stats).sort_values("gene")


def main() -> int:
    np.random.seed(SEED)
    OUT.mkdir(exist_ok=True)
    annotation, found = stream_target_counts()
    aggregate = pseudobulk(annotation, found, "immune")
    contrasts, statistics = compare_active_inactive(aggregate, found)
    all_aggregate = pseudobulk(annotation, found, None)
    all_contrasts = []
    all_statistics = []
    for cell_type, subset in all_aggregate.groupby("cell_type", observed=True, sort=True):
        cell_contrasts, cell_statistics = compare_active_inactive(subset.drop(columns="cell_type"), found)
        if len(cell_contrasts):
            cell_contrasts.insert(0, "cell_type", cell_type)
            all_contrasts.append(cell_contrasts)
        if len(cell_statistics):
            cell_statistics.insert(0, "cell_type", cell_type)
            all_statistics.append(cell_statistics)
    all_contrasts_frame = pd.concat(all_contrasts, ignore_index=True) if all_contrasts else pd.DataFrame()
    all_statistics_frame = pd.concat(all_statistics, ignore_index=True) if all_statistics else pd.DataFrame()
    aggregate.to_csv(OUT / "tbxas1_gse180759_immune_pseudobulks.tsv", sep="\t", index=False)
    contrasts.to_csv(OUT / "tbxas1_gse180759_paired_contrasts.tsv", sep="\t", index=False)
    statistics.to_csv(OUT / "tbxas1_gse180759_paired_statistics.tsv", sep="\t", index=False)
    all_aggregate.to_csv(OUT / "tbxas1_gse180759_all_celltype_pseudobulks.tsv", sep="\t", index=False)
    all_contrasts_frame.to_csv(OUT / "tbxas1_gse180759_all_celltype_paired_contrasts.tsv", sep="\t", index=False)
    all_statistics_frame.to_csv(OUT / "tbxas1_gse180759_all_celltype_paired_statistics.tsv", sep="\t", index=False)
    target = statistics.loc[statistics["gene"] == "TBXAS1"]
    target_by_celltype = all_statistics_frame.loc[
        all_statistics_frame["gene"] == "TBXAS1"
    ].to_dict(orient="records")
    summary = {
        "random_seed": SEED,
        "dataset": "GSE180759",
        "cell_type": "immune",
        "normalization": "log2(CPM + 1) pseudobulk using all-gene library size",
        "minimum_nuclei_per_block": MIN_NUCLEI,
        "primary_contrast": f"{ACTIVE} minus {INACTIVE}",
        "found_targets": found,
        "eligible_pseudobulks": int(len(aggregate)),
        "paired_donors_primary_contrast": int(contrasts["donor"].nunique()) if len(contrasts) else 0,
        "tbxas1": target.iloc[0].to_dict() if len(target) else None,
        "tbxas1_by_celltype": target_by_celltype,
        "interpretation_boundary": (
            "This independently tests cell-compartment transcript localization only; "
            "three paired donors cannot establish efficacy or rule out composition effects."
        ),
    }
    (OUT / "tbxas1_gse180759_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
