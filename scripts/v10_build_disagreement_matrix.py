#!/usr/bin/env python3
"""Build the V10 supported-axis disagreement matrix."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PLACEMENTS = ROOT / "analysis" / "v8_map" / "placement_matrix.tsv"
OUT = ROOT / "analysis" / "v10_disagreement"

GRADE_WEIGHT = {"supported": 1.0, "robust": 1.25}
CONF_WEIGHT = {"low": 0.5, "medium": 1.0, "high": 1.25}
PLACEMENT_SCORE = {"far": 0.0, "intermediate": 2.0, "near": 3.0}
AXIS_LABELS = {
    "axis_01_ifn_apc": "IFN/APC antigen-presentation state",
    "axis_02_genetics": "genetic risk architecture",
    "axis_03_microbiome": "gut microbiome and microbial-immune signaling",
    "axis_04_lipid_lysosomal": "lipid-lysosomal / foamy myeloid state",
    "axis_05_complement_innate": "complement and innate effector biology",
    "axis_06_tcell_adaptive_repertoire": "T-cell and adaptive repertoire",
    "axis_07_treatment_response": "treatment-response architecture",
    "axis_08_tissue_repair_resolution": "tissue repair and resolution biology",
    "axis_09_sex_hormonal_pregnancy": "sex, hormonal, and pregnancy modulation",
    "axis_10_infectious_trigger": "infectious-trigger biology",
}


def placement_distance(a: str, b: str) -> float:
    if a == b:
        return 0.0
    if "contradictory" in {a, b}:
        return 2.5
    return abs(PLACEMENT_SCORE[a] - PLACEMENT_SCORE[b])


def grade_weight(grade: str) -> float:
    return GRADE_WEIGHT.get(grade, 0.0)


def confidence_weight(confidence: str) -> float:
    return CONF_WEIGHT.get(confidence, 0.0)


def ms_relevance_weight(row_a: pd.Series, row_b: pd.Series) -> float:
    axes = {row_a["axis"], row_b["axis"]}
    high_value = {
        "axis_02_genetics",
        "axis_01_ifn_apc",
        "axis_03_microbiome",
        "axis_07_treatment_response",
        "axis_08_tissue_repair_resolution",
    }
    weight = 1.0
    if axes & high_value:
        weight += 0.25
    if "axis_02_genetics" in axes:
        weight += 0.25
    return weight


def artifact_flags(row_a: pd.Series, row_b: pd.Series) -> dict[str, str]:
    comp_a = str(row_a.get("compartment_summary", ""))
    comp_b = str(row_b.get("compartment_summary", ""))
    caus_a = str(row_a.get("causality_summary", ""))
    caus_b = str(row_b.get("causality_summary", ""))
    notes = []
    compartment_mismatch = comp_a != comp_b
    causality_mismatch = caus_a != caus_b
    if compartment_mismatch:
        notes.append("compartment mismatch")
    if causality_mismatch:
        notes.append("causality/measurement mismatch")
    if row_a["confidence"] != row_b["confidence"]:
        notes.append("confidence mismatch")
    axes = {row_a["axis"], row_b["axis"]}
    axis_nonindependence = False
    if axes == {"axis_07_treatment_response", "axis_08_tissue_repair_resolution"}:
        axis_nonindependence = True
        notes.append("axis non-independence risk: treatment-response and repair evidence may overlap")
    return {
        "compartment_mismatch": str(compartment_mismatch),
        "causality_mismatch": str(causality_mismatch),
        "axis_nonindependence_risk": "high" if axis_nonindependence else "not_flagged",
        "artifact_risk_notes": "; ".join(notes) if notes else "none obvious from matrix metadata",
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    placements = pd.read_csv(PLACEMENTS, sep="\t")
    placements["axis_label"] = placements["axis"].map(AXIS_LABELS).fillna(placements["axis"])
    placements["v10_overlay_note"] = ""

    # V9 microbiome overlay. This does not change UC/CD microbiome grade because
    # V9 explicitly failed to support MS/IBD broad taxonomic proximity.
    microbiome_mask = placements["axis"].eq("axis_03_microbiome")
    placements.loc[microbiome_mask, "v10_overlay_note"] = (
        "V9: MS has one-dataset primary stool microbiome signal, but MS/IBD broad "
        "taxonomic proximity remains unsupported after IBDMDB participant-aware tests."
    )
    placements.to_csv(OUT / "placement_matrix_v10_overlay.tsv", sep="\t", index=False)

    supported = placements[placements["grade"].isin(["supported", "robust"])].copy()
    rows = []
    for disease, disease_df in supported.groupby("disease"):
        for (_, a), (_, b) in combinations(disease_df.iterrows(), 2):
            if a["placement"] == "unresolved" or b["placement"] == "unresolved":
                continue
            dist = placement_distance(str(a["placement"]), str(b["placement"]))
            if dist <= 0:
                continue
            conf = (confidence_weight(str(a["confidence"])) + confidence_weight(str(b["confidence"]))) / 2
            grade = (grade_weight(str(a["grade"])) + grade_weight(str(b["grade"]))) / 2
            relevance = ms_relevance_weight(a, b)
            rank_score = dist * conf * grade * relevance
            flags = artifact_flags(a, b)
            independence_penalty = 0.25 if flags["axis_nonindependence_risk"] == "high" else 1.0
            rank_score = rank_score * independence_penalty
            rows.append(
                {
                    "disease": disease,
                    "axis_a": a["axis"],
                    "axis_a_label": a["axis_label"],
                    "placement_a": a["placement"],
                    "grade_a": a["grade"],
                    "confidence_a": a["confidence"],
                    "compartment_a": a["compartment_summary"],
                    "causality_a": a["causality_summary"],
                    "axis_b": b["axis"],
                    "axis_b_label": b["axis_label"],
                    "placement_b": b["placement"],
                    "grade_b": b["grade"],
                    "confidence_b": b["confidence"],
                    "compartment_b": b["compartment_summary"],
                    "causality_b": b["causality_summary"],
                    "placement_distance": dist,
                    "independence_penalty": independence_penalty,
                    "rank_score": rank_score,
                    **flags,
                    "initial_classification": "unresolved_pending_artifact_audit",
                }
            )

    disagreements = pd.DataFrame(rows).sort_values(
        ["rank_score", "placement_distance"], ascending=[False, False]
    )
    disagreements.to_csv(OUT / "disagreement_pairs.tsv", sep="\t", index=False)

    summary = [
        "# V10 Disagreement Matrix Build Report",
        "",
        f"Input placements: `{len(placements)}`",
        f"Supported/robust placements considered: `{len(supported)}`",
        f"Supported-axis disagreement pairs: `{len(disagreements)}`",
        "",
        "V9 overlay: microbiome placements retain their V8 grade for disease-relative",
        "MS proximity because V9 did not support broad MS/IBD taxonomic proximity.",
        "",
    ]
    if not disagreements.empty:
        display = disagreements[
            [
                "disease",
                "axis_a_label",
                "placement_a",
                "axis_b_label",
                "placement_b",
                "placement_distance",
                "rank_score",
                "artifact_risk_notes",
            ]
        ].head(20)
        summary.extend(["## Top 20", "", markdown_table(display), ""])
    (OUT / "BUILD_REPORT.md").write_text("\n".join(summary), encoding="utf-8")


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in df.itertuples(index=False, name=None):
        lines.append("| " + " | ".join("" if pd.isna(x) else str(x) for x in row) + " |")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
