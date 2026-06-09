#!/usr/bin/env python3
"""Compare V38 failure families with V36 exploratory fragility families.

The two inputs have different row units: V38 rows are failed/closed findings;
V36 rows are analysis artifacts. This script therefore maps both to a shared
gate taxonomy and compares distributions instead of forcing a false item join.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
V38_FAILURE = ROOT / "analysis/v38_failure_structure/failure_family_counts.tsv"
V36_FRAGILITY = ROOT / "analysis/v38_v36_fragility_map/v36_fragility_family_counts.tsv"
OUTDIR = ROOT / "analysis/v38_failure_fragility_concordance"


GATES = [
    "evidence_resolution_or_data_gap",
    "context_axis_or_branch",
    "direction_modality",
    "specificity_control",
    "complexity_overfit",
    "marker_not_driver",
]

V38_MAP = {
    "evidence_resolution_failure": "evidence_resolution_or_data_gap",
    "context_or_axis_dependence": "context_axis_or_branch",
    "direction_or_modality_constraint": "direction_modality",
    "specificity_or_control_failure": "specificity_control",
    "complexity_or_modeling_failure": "complexity_overfit",
    "marker_not_driver": "marker_not_driver",
}

V36_MAP = {
    "composition_confounding": "specificity_control",
    "creative_generation_data_gate": "evidence_resolution_or_data_gap",
    "multiplicity_overfit": "complexity_overfit",
    "missing_decisive_metadata": "evidence_resolution_or_data_gap",
    "missing_decisive_modality": "evidence_resolution_or_data_gap",
    "multiplicity_compartment_scan": "complexity_overfit",
    "sample_size_power": "evidence_resolution_or_data_gap",
    "small_n_therapy_specificity": "context_axis_or_branch",
    "technical_qc_limit": "evidence_resolution_or_data_gap",
    "therapy_branch_specificity": "context_axis_or_branch",
}


def distribution(df: pd.DataFrame, source_col: str, count_col: str, mapping: dict[str, str]) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        source = row[source_col]
        gate = mapping[source]
        rows.append({"source_family": source, "gate": gate, "n": int(row[count_col])})
    mapped = pd.DataFrame(rows)
    gate_counts = mapped.groupby("gate")["n"].sum().reindex(GATES, fill_value=0).reset_index()
    gate_counts["fraction"] = gate_counts["n"] / gate_counts["n"].sum()
    return mapped, gate_counts


def js_divergence(p: list[float], q: list[float]) -> float:
    def kl(a: list[float], b: list[float]) -> float:
        total = 0.0
        for ai, bi in zip(a, b):
            if ai == 0:
                continue
            total += ai * math.log2(ai / bi)
        return total

    m = [(pi + qi) / 2.0 for pi, qi in zip(p, q)]
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    v38 = pd.read_csv(V38_FAILURE, sep="\t")
    v36 = pd.read_csv(V36_FRAGILITY, sep="\t")

    v38_mapped, v38_gate = distribution(v38, "family", "n_items", V38_MAP)
    v36_mapped, v36_gate = distribution(v36, "fragility_family", "n_items", V36_MAP)
    v38_mapped.to_csv(OUTDIR / "v38_failure_family_to_gate.tsv", sep="\t", index=False)
    v36_mapped.to_csv(OUTDIR / "v36_fragility_family_to_gate.tsv", sep="\t", index=False)

    compare = v38_gate.rename(columns={"n": "v38_n", "fraction": "v38_fraction"}).merge(
        v36_gate.rename(columns={"n": "v36_n", "fraction": "v36_fraction"}), on="gate"
    )
    compare["fraction_delta_v36_minus_v38"] = compare["v36_fraction"] - compare["v38_fraction"]
    compare.to_csv(OUTDIR / "failure_fragility_gate_comparison.tsv", sep="\t", index=False)

    jsd = js_divergence(compare["v38_fraction"].tolist(), compare["v36_fraction"].tolist())
    summary = {
        "v38_failure_source": str(V38_FAILURE.relative_to(ROOT)),
        "v36_fragility_source": str(V36_FRAGILITY.relative_to(ROOT)),
        "row_units_warning": (
            "V38 rows are failed/closed findings; V36 rows are analysis artifacts. "
            "The comparison is gate-level, not item-level."
        ),
        "jensen_shannon_divergence_bits": jsd,
        "gate_comparison": compare.to_dict(orient="records"),
        "interpretation": (
            "The two maps are complementary, not redundant. Both emphasize "
            "evidence/data gaps and context/branch constraints, but V38 uniquely "
            "captures direction/modality and marker-not-driver target failures, "
            "while V36 uniquely emphasizes multiplicity/overfit, sample-size, "
            "and technical/confounder fragility in exploratory analyses."
        ),
    }
    with (OUTDIR / "failure_fragility_concordance_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2)


if __name__ == "__main__":
    main()
