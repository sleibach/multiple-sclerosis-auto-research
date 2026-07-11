#!/usr/bin/env python3
"""Audit whether V26 cross-disease summary is independent evidence."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

import v3_build_cross_disease_convergence_tables as source


ROOT = Path(__file__).resolve().parents[1]
INPUT_ROWS = ROOT / "phases/v3/results/cross_disease_cell_state_convergence.tsv"
INPUT_SUMMARY = ROOT / "phases/v3/results/cross_disease_module_summary.tsv"
V26_MATRIX = ROOT / "analysis/v26_deep_structure/cross_disease_summary_module_matrix.tsv"
OUT = ROOT / "analysis/v53_cross_disease_summary_lineage_audit"
LEFT = "hla_ii_apc"
RIGHT = "mif_cd74_receptor_state"
METRICS = [
    "n_strong_diseases",
    "n_supportive_or_strong_diseases",
    "n_trend_or_better_diseases",
    "n_negative_trend_diseases",
    "mean_positive_delta",
    "median_positive_hedges_g",
]


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def summary_matrix(rows: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary = source.summarize_modules(rows)
    matrix = summary.set_index("module")[METRICS].T
    return summary, matrix


def safe_spearman(left: pd.Series, right: pd.Series) -> float:
    paired = pd.concat([left, right], axis=1).dropna()
    if len(paired) < 3 or paired.iloc[:, 0].std() == 0 or paired.iloc[:, 1].std() == 0:
        return float("nan")
    return float(stats.spearmanr(paired.iloc[:, 0], paired.iloc[:, 1]).statistic)


def summarize_variant(name: str, rows: pd.DataFrame) -> dict[str, Any]:
    summary, matrix = summary_matrix(rows)
    module_names = set(matrix.columns)
    rho = (
        safe_spearman(matrix[LEFT], matrix[RIGHT])
        if {LEFT, RIGHT}.issubset(module_names)
        else float("nan")
    )
    hla = summary[summary["module"].eq(LEFT)]
    mif = summary[summary["module"].eq(RIGHT)]
    return {
        "variant": name,
        "n_source_rows": len(rows),
        "n_dataset_labels": rows["dataset"].nunique(),
        "n_diseases": rows["disease"].nunique(),
        "hla_mif_six_derived_metric_spearman": rho,
        "hla_n_diseases_tested": int(hla["n_diseases_tested"].iloc[0]) if len(hla) else 0,
        "hla_n_trend_or_better": int(hla["n_trend_or_better_diseases"].iloc[0]) if len(hla) else 0,
        "mif_n_diseases_tested": int(mif["n_diseases_tested"].iloc[0]) if len(mif) else 0,
        "mif_n_trend_or_better": int(mif["n_trend_or_better_diseases"].iloc[0]) if len(mif) else 0,
    }


def main() -> int:
    rows = pd.read_csv(INPUT_ROWS, sep="\t")
    committed_summary = pd.read_csv(INPUT_SUMMARY, sep="\t")
    v26 = pd.read_csv(V26_MATRIX, sep="\t", index_col=0)
    rebuilt_summary, rebuilt_matrix = summary_matrix(rows)
    rebuilt_matrix = rebuilt_matrix.reindex(index=v26.index, columns=v26.columns).fillna(0.0)
    if rebuilt_matrix.shape != v26.shape or rebuilt_matrix.isna().any().any():
        raise RuntimeError("Cross-disease summary rebuild is incomplete")
    max_matrix_error = float(
        np.max(abs(rebuilt_matrix.to_numpy(dtype=float) - v26.to_numpy(dtype=float)))
    )
    if max_matrix_error > 1e-10:
        raise RuntimeError(f"Cross-disease summary rebuild mismatch: {max_matrix_error}")

    summary_columns = [column for column in committed_summary if column != "supporting_diseases"]
    left_summary = committed_summary.set_index("module")[summary_columns[1:]].sort_index()
    right_summary = rebuilt_summary.set_index("module")[summary_columns[1:]].sort_index()
    common = left_summary.index.intersection(right_summary.index)
    numeric_columns = left_summary.select_dtypes(include=[np.number]).columns
    max_summary_error = float(
        np.nanmax(
            abs(
                left_summary.loc[common, numeric_columns].to_numpy(dtype=float)
                - right_summary.loc[common, numeric_columns].to_numpy(dtype=float)
            )
        )
    )

    direct = rows["modality"].eq("single_cell_or_single_nucleus_h5ad")
    variant_rows = [
        summarize_variant("all_sources", rows),
        summarize_variant("direct_h5ad_only", rows[direct].copy()),
        summarize_variant("exclude_direct_h5ad", rows[~direct].copy()),
    ]
    for dataset in sorted(rows["dataset"].unique()):
        variant_rows.append(
            summarize_variant(f"leave_out:{dataset}", rows[~rows["dataset"].eq(dataset)].copy())
        )

    matched = rows[rows["module"].isin([LEFT, RIGHT])].pivot_table(
        index=["disease", "dataset", "modality", "compartment"],
        columns="module",
        values="delta",
        aggfunc="first",
    ).dropna(subset=[LEFT, RIGHT])
    matched = matched.reset_index()
    matched["source_class"] = np.where(
        matched["modality"].eq("single_cell_or_single_nucleus_h5ad"),
        "reused_direct_h5ad",
        "additional_atlas",
    )
    matched_rows = []
    for source_class, sub in matched.groupby("source_class"):
        matched_rows.append(
            {
                "source_class": source_class,
                "n_matched_contexts": len(sub),
                "n_datasets": sub["dataset"].nunique(),
                "n_diseases": sub["disease"].nunique(),
                "overlapping_definition_spearman": safe_spearman(sub[LEFT], sub[RIGHT]),
                "globally_disjoint_rebuild_available": source_class == "reused_direct_h5ad",
                "independent_of_v26_cell_state_matrix": source_class == "additional_atlas",
            }
        )

    direct_fraction = float(direct.mean())
    summary = {
        "purpose": "V53 source-lineage audit of the V26 cross-disease summary matrix",
        "n_source_rows": len(rows),
        "n_source_dataset_labels": rows["dataset"].nunique(),
        "n_diseases": rows["disease"].nunique(),
        "n_direct_h5ad_rows_reused_from_cell_state_layer": int(direct.sum()),
        "fraction_rows_reused_from_cell_state_layer": direct_fraction,
        "n_additional_atlas_rows": int((~direct).sum()),
        "max_absolute_committed_summary_rebuild_error": max_summary_error,
        "max_absolute_v26_matrix_rebuild_error": max_matrix_error,
        "full_disjoint_rebuild_available": False,
        "full_disjoint_rebuild_blocker": (
            "The direct-h5ad component has a V53 disjoint rebuild, but GSE111972, "
            "GSE248205, and GSE315138 require separate source-level rescoring. "
            "The aggregate summary cannot be de-overlapped algebraically."
        ),
        "independent_modality_status": "NO_DERIVED_SUMMARY_RETIRED_AS_INDEPENDENT_EVIDENCE",
        "verdict": "CROSS_DISEASE_SUMMARY_IS_DESCRIPTIVE_DERIVED_ATLAS_NOT_FIFTH_INDEPENDENT_MODALITY",
        "boundary": "This audit changes no source result or locked rule; it corrects evidence-lineage accounting.",
    }

    OUT.mkdir(parents=True, exist_ok=True)
    rebuilt_matrix.to_csv(OUT / "rebuilt_v26_cross_disease_summary_matrix.tsv", sep="\t")
    write_tsv(OUT / "source_exclusion_variants.tsv", variant_rows)
    write_tsv(OUT / "matched_hla_mif_source_classes.tsv", matched_rows)
    matched.to_csv(OUT / "matched_hla_mif_contexts.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 Cross-Disease Summary Lineage Audit",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"The V26 matrix rebuilds exactly (maximum error `{max_matrix_error:.3g}`). It is",
        f"derived from `{len(rows)}` source rows across `{rows['dataset'].nunique()}` dataset",
        f"labels and `{rows['disease'].nunique()}` diseases. `{int(direct.sum())}` rows",
        f"(`{100 * direct_fraction:.1f}%`) reuse the direct-h5ad cell-state analyses already",
        "represented in V26's cell-state matrix; the remaining rows come from GSE111972,",
        "GSE248205, and GSE315138.",
        "",
        "The matrix's six rows are support counts and positive-effect summaries computed",
        "from those source rows. They are not independent observations, and correlating",
        "module columns across those six derived metrics does not create a new modality.",
        "The cross-disease matrix remains useful as a descriptive atlas but is retired as",
        "independent corroboration of the coupled two-arm architecture.",
        "",
        "A full disjoint rebuild cannot be obtained from the aggregate matrix. The reused",
        "direct-h5ad component is already de-overlapped in V53; the three additional atlases",
        "would require source-level rescoring. That work may test broad recurrence, but it",
        "cannot make this derived summary an independent fifth modality.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
