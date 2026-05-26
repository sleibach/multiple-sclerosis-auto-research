#!/usr/bin/env python3
"""Targeted lesion-edge transcript validation of PLA2G7 in independent GSE180759."""

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
TARGETS = ["PLA2G7", "GPNMB", "LPL", "APOE", "TREM2", "C1QA", "CTSD", "MGLL", "ABHD6", "LIPA"]
PRIMARY_A = "chronic_active_MS_lesion_edge"
PRIMARY_B = "chronic_inactive_MS_lesion_edge"
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


def pseudobulk_immune(annotation: pd.DataFrame, found: list[str]) -> pd.DataFrame:
    immune = annotation.loc[annotation["cell_type"] == "immune"].copy()
    group_columns = ["NBB_case", "pathology"]
    grouped = immune.groupby(group_columns, observed=True, sort=True)
    result = grouped.size().rename("n_nuclei").reset_index()
    result = result.merge(grouped["library_size"].sum().rename("library_size").reset_index())
    for gene in found:
        result = result.merge(grouped[gene].sum().rename(f"{gene}_raw").reset_index())
        result[gene] = np.log2(result[f"{gene}_raw"] / result["library_size"] * 1_000_000 + 1)
    return result.loc[result["n_nuclei"] >= MIN_NUCLEI].copy()


def paired_contrasts(pseudobulk: pd.DataFrame, found: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    a = pseudobulk.loc[pseudobulk["pathology"] == PRIMARY_A].set_index("NBB_case")
    b = pseudobulk.loc[pseudobulk["pathology"] == PRIMARY_B].set_index("NBB_case")
    donors = sorted(set(a.index) & set(b.index))
    rows = []
    for donor in donors:
        for gene in found:
            rows.append(
                {
                    "donor": donor,
                    "gene": gene,
                    "active_edge_log2_cpm1": float(a.loc[donor, gene]),
                    "inactive_edge_log2_cpm1": float(b.loc[donor, gene]),
                    "delta_active_minus_inactive": float(a.loc[donor, gene] - b.loc[donor, gene]),
                    "active_edge_n_immune": int(a.loc[donor, "n_nuclei"]),
                    "inactive_edge_n_immune": int(b.loc[donor, "n_nuclei"]),
                }
            )
    contrasts = pd.DataFrame(rows)
    statistics = []
    for gene in found:
        deltas = contrasts.loc[contrasts["gene"] == gene, "delta_active_minus_inactive"].to_numpy()
        if len(deltas) == 0:
            continue
        dz = float(np.mean(deltas) / np.std(deltas, ddof=1)) if len(deltas) > 1 and np.std(deltas, ddof=1) else np.nan
        p_value = float(st.wilcoxon(deltas).pvalue) if np.any(deltas != 0) else 1.0
        statistics.append(
            {
                "gene": gene,
                "paired_donors": int(len(deltas)),
                "mean_delta_active_minus_inactive": float(np.mean(deltas)),
                "paired_dz": dz,
                "positive_fraction": float(np.mean(deltas > 0)),
                "wilcoxon_p": p_value,
                "inference_boundary": "descriptive targeted validation: n is too small for exclusionary inference",
            }
        )
    return contrasts, pd.DataFrame(statistics).sort_values("gene")


def main() -> int:
    np.random.seed(SEED)
    OUT.mkdir(exist_ok=True)
    annotation, found = stream_target_counts()
    pseudobulk = pseudobulk_immune(annotation, found)
    contrasts, statistics = paired_contrasts(pseudobulk, found)
    pseudobulk.to_csv(OUT / "pla2g7_gse180759_immune_pseudobulks.tsv", sep="\t", index=False)
    contrasts.to_csv(OUT / "pla2g7_gse180759_paired_contrasts.tsv", sep="\t", index=False)
    statistics.to_csv(OUT / "pla2g7_gse180759_paired_statistics.tsv", sep="\t", index=False)
    pla2g7 = statistics.loc[statistics["gene"] == "PLA2G7"]
    summary = {
        "random_seed": SEED,
        "dataset": "GSE180759",
        "cell_type": "immune",
        "normalization": "log2(CPM + 1) pseudobulk using all-gene library size",
        "minimum_nuclei_per_block": MIN_NUCLEI,
        "primary_contrast": f"{PRIMARY_A} minus {PRIMARY_B}",
        "found_targets": found,
        "eligible_pseudobulks": int(len(pseudobulk)),
        "paired_donors_primary_contrast": int(contrasts["donor"].nunique()) if len(contrasts) else 0,
        "pla2g7": pla2g7.iloc[0].to_dict() if len(pla2g7) else None,
        "interpretation_boundary": (
            "This is independent lesion-edge localization of transcript, not ABPP activity, "
            "spatial proximity, target engagement, or therapeutic efficacy."
        ),
    }
    (OUT / "pla2g7_gse180759_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
