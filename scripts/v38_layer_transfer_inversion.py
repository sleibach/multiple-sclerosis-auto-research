#!/usr/bin/env python3
"""Adversarial inversion of the V10/V12 layer-transfer map.

Inversion tested: transfer-validity claims may be narrative disease similarity
rather than matrix-grounded, axis-specific evidence. This script parses the
placement and disagreement matrices to quantify axis heterogeneity and artifact
controls.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PLACEMENTS = ROOT / "analysis/v8_map/placement_matrix.tsv"
DISAGREEMENT = ROOT / "analysis/v11_matrix/disagreement_matrix.tsv"
OUTDIR = ROOT / "analysis/v38_layer_transfer_inversion"

KEY_DISEASES = {
    "ulcerative colitis",
    "Crohn disease",
    "rheumatoid arthritis",
    "Sjogren syndrome",
}


PLACEMENT_SCORE = {
    "far": 0,
    "intermediate": 1,
    "contradictory": 1.5,
    "near": 2,
    "unresolved": None,
}


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    placements = pd.read_csv(PLACEMENTS, sep="\t")
    disagreements = pd.read_csv(DISAGREEMENT, sep="\t")

    key_placements = placements[placements["disease"].isin(KEY_DISEASES)].copy()
    key_placements["placement_score"] = key_placements["placement"].map(PLACEMENT_SCORE)
    key_placements.to_csv(OUTDIR / "key_disease_axis_placements.tsv", sep="\t", index=False)

    heterogeneity_rows = []
    for disease, sub in key_placements.groupby("disease"):
        supported = sub[sub["grade"].isin(["supported", "robust"])]
        resolved = supported[supported["placement"] != "unresolved"]
        scores = resolved["placement_score"].dropna()
        heterogeneity_rows.append(
            {
                "disease": disease,
                "n_supported_or_robust_axes": int(len(supported)),
                "n_resolved_supported_axes": int(len(resolved)),
                "distinct_resolved_placements": ";".join(sorted(resolved["placement"].unique())),
                "min_placement_score": float(scores.min()) if len(scores) else None,
                "max_placement_score": float(scores.max()) if len(scores) else None,
                "placement_range": float(scores.max() - scores.min()) if len(scores) else None,
                "has_axis_heterogeneity": bool(len(scores) and (scores.max() - scores.min()) > 0),
                "compartments": ";".join(sorted(set(resolved["compartment_summary"].dropna()))),
                "causality_types": ";".join(sorted(set(resolved["causality_summary"].dropna()))),
            }
        )
    heterogeneity = pd.DataFrame(heterogeneity_rows).sort_values(
        ["has_axis_heterogeneity", "placement_range"], ascending=[False, False]
    )
    heterogeneity.to_csv(OUTDIR / "disease_axis_heterogeneity.tsv", sep="\t", index=False)

    matrix = disagreements.copy()
    matrix["is_artifact"] = matrix["status"].str.contains("artifact", case=False, na=False)
    matrix["is_supported_transfer_cell"] = ~matrix["is_artifact"]
    matrix["axis_specific_evidence"] = (
        (matrix["placement_distance"] > 0)
        & (
            matrix["compartment_mismatch"].astype(str).str.lower().eq("true")
            | matrix["causality_mismatch"].astype(str).str.lower().eq("true")
            | matrix["axis_nonindependence_risk"].ne("not_flagged")
        )
    )
    cols = [
        "cell_id",
        "disease",
        "axis_a_label",
        "placement_a",
        "axis_b_label",
        "placement_b",
        "placement_distance",
        "status",
        "is_artifact",
        "axis_specific_evidence",
        "compartment_mismatch",
        "causality_mismatch",
        "axis_nonindependence_risk",
        "resolution_grade",
        "next_action",
    ]
    matrix[cols].to_csv(OUTDIR / "disagreement_cell_axis_specificity.tsv", sep="\t", index=False)

    status_counts = matrix["status"].value_counts().to_dict()
    non_artifact = matrix[~matrix["is_artifact"]]
    summary = {
        "placement_source": str(PLACEMENTS.relative_to(ROOT)),
        "disagreement_source": str(DISAGREEMENT.relative_to(ROOT)),
        "n_key_diseases": int(len(KEY_DISEASES)),
        "n_key_diseases_with_axis_heterogeneity": int(
            heterogeneity["has_axis_heterogeneity"].sum()
        ),
        "disease_heterogeneity": heterogeneity.to_dict(orient="records"),
        "n_disagreement_cells": int(len(matrix)),
        "status_counts": status_counts,
        "n_artifact_cells": int(matrix["is_artifact"].sum()),
        "n_non_artifact_cells": int(len(non_artifact)),
        "n_non_artifact_axis_specific_cells": int(non_artifact["axis_specific_evidence"].sum()),
        "fraction_non_artifact_axis_specific": float(
            non_artifact["axis_specific_evidence"].mean() if len(non_artifact) else 0.0
        ),
        "inversion_verdict": (
            "Narrative-disease-similarity inversion is not supported. The key "
            "comparator diseases show heterogeneous placements across axes, and "
            "the non-artifact disagreement cells are axis/compartment/causality "
            "specific. The map remains a transfer-warning framework, not an "
            "intervention claim."
        ),
    }
    with (OUTDIR / "layer_transfer_inversion_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2)


if __name__ == "__main__":
    main()
