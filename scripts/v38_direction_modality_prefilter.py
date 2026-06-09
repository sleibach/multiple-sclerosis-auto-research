#!/usr/bin/env python3
"""Quantify whether direction/modality failures are recurrent enough to prefilter.

Input is the V38 failure-structure table, which was annotated from V37
committed artifacts. This script does not relitigate individual leads; it
quantifies recurring direction/modality constraints.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v38_failure_structure/failure_mode_table.tsv"
OUTDIR = ROOT / "analysis/v38_direction_modality_prefilter"


DIRECTION_MODE_PATTERNS = {
    "hard_up_function_or_restoration": [
        "hard_protective_direction",
        "restoration",
        "up_function",
        "agonism",
    ],
    "opposite_or_invalid_transfer_direction": [
        "opposite_direction",
        "transfer_invalid",
        "direction_conflict",
    ],
    "direction_unresolved_or_missing": [
        "direction_unresolved",
        "missing_qtl_direction",
        "no_direction",
        "no_shared_disease_signal",
    ],
    "modality_or_target_fit_failure": [
        "weak_modality_fit",
        "immature_chemical_matter",
        "covariate_not_target",
        "covariate_not_intervention",
        "marker_not_driver",
        "not_intervention",
    ],
}


def labels_for_row(row: pd.Series) -> list[str]:
    text = " ".join(
        str(row.get(col, ""))
        for col in ["failure_modes", "therapeutic_constraint", "status", "mechanism_level"]
    ).lower()
    labels = []
    for label, patterns in DIRECTION_MODE_PATTERNS.items():
        if any(pattern in text for pattern in patterns):
            labels.append(label)
    return labels


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT, sep="\t")
    rows = []
    for _, row in df.iterrows():
        labels = labels_for_row(row)
        rows.append(
            {
                "item": row["item"],
                "category": row["category"],
                "evidence_grade": row["evidence_grade"],
                "relevance": row["relevance"],
                "novelty": row["novelty"],
                "mechanism_level": row["mechanism_level"],
                "therapeutic_constraint": row["therapeutic_constraint"],
                "failure_modes": row["failure_modes"],
                "direction_modality_labels": ";".join(labels),
                "has_direction_modality_constraint": bool(labels),
            }
        )
    annotated = pd.DataFrame(rows)
    annotated.to_csv(OUTDIR / "direction_modality_annotated_failures.tsv", sep="\t", index=False)

    label_rows = []
    for label in DIRECTION_MODE_PATTERNS:
        mask = annotated["direction_modality_labels"].str.contains(label, regex=False)
        label_rows.append(
            {
                "constraint_label": label,
                "n_items": int(mask.sum()),
                "fraction_all_failures": float(mask.mean()),
                "items": " | ".join(annotated.loc[mask, "item"].tolist()),
            }
        )
    label_df = pd.DataFrame(label_rows).sort_values("n_items", ascending=False)
    label_df.to_csv(OUTDIR / "direction_modality_constraint_counts.tsv", sep="\t", index=False)

    by_mechanism = (
        annotated.groupby("mechanism_level", dropna=False)["has_direction_modality_constraint"]
        .agg(["count", "sum", "mean"])
        .reset_index()
        .rename(columns={"count": "n_items", "sum": "n_direction_modality", "mean": "fraction"})
        .sort_values(["n_direction_modality", "n_items"], ascending=False)
    )
    by_mechanism.to_csv(OUTDIR / "direction_modality_by_mechanism.tsv", sep="\t", index=False)

    targetlike_levels = {"genetics_to_target", "target_nomination", "genetics_coloc"}
    targetlike = annotated[annotated["mechanism_level"].isin(targetlike_levels)]
    summary = {
        "input": str(INPUT.relative_to(ROOT)),
        "n_total_failure_or_negative_items": int(len(annotated)),
        "n_direction_modality_constrained": int(annotated["has_direction_modality_constraint"].sum()),
        "fraction_direction_modality_constrained": float(
            annotated["has_direction_modality_constraint"].mean()
        ),
        "n_targetlike_items": int(len(targetlike)),
        "n_targetlike_direction_modality_constrained": int(
            targetlike["has_direction_modality_constraint"].sum()
        ),
        "fraction_targetlike_direction_modality_constrained": float(
            targetlike["has_direction_modality_constraint"].mean() if len(targetlike) else 0.0
        ),
        "constraint_counts": label_df.to_dict(orient="records"),
        "by_mechanism": by_mechanism.to_dict(orient="records"),
        "prefilter_recommendation": (
            "Direction/modality is recurrent enough to be a mandatory early "
            "prefilter, especially for target-like genetics leads. A future lead "
            "should be downgraded before deep work if the protective direction "
            "requires restoration/up-function/agonism without a realistic "
            "modality, if the cross-disease direction is opposite, or if no "
            "allele-aligned direction is available."
        ),
    }
    with (OUTDIR / "direction_modality_prefilter_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2)


if __name__ == "__main__":
    main()
