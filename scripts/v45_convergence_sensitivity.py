#!/usr/bin/env python3
"""Sensitivity checks for APC/HLA/IFN recurrence convergence.

This is internal method-characterization only. It does not change the V41/V44
recurrence definition; it tests whether the target remains exceptional after
source-file weighting and source-family collapse.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
V41 = ROOT / "analysis" / "v41_joint_inference"
OUT = ROOT / "analysis" / "v45_convergence_sensitivity"
OUT.mkdir(parents=True, exist_ok=True)

TARGET = "apc_hla_ifn_monitoring"
SEED = 45345
N_REPS = 20000


def source_family(source_file: str) -> str:
    path = Path(str(source_file))
    parts = path.parts
    if len(parts) >= 2:
        if parts[0] == "analysis":
            return "/".join(parts[:2])
        if parts[0] == "docs" and parts[1] in {"reports", "history", "validation", "workups"}:
            return "/".join(parts[:2])
    return parts[0] if parts else str(source_file)


def positive_units(evidence: pd.DataFrame) -> pd.DataFrame:
    usable = evidence[evidence["direction"] > 0].copy()
    usable["source_unit"] = (
        usable["modality"].astype(str)
        + "::"
        + usable["source_file"].astype(str)
        + "::"
        + usable["evidence_label"].astype(str)
    )
    usable["source_family"] = usable["source_file"].map(source_family)
    usable["modality_family_unit"] = usable["modality"].astype(str) + "::" + usable["source_family"].astype(str)
    return usable[
        ["source_unit", "modality", "source_file", "source_family", "modality_family_unit", "entity"]
    ].drop_duplicates()


def weighted_scores(units: pd.DataFrame) -> pd.Series:
    work = units.copy()
    source_unit_counts = work[["source_file", "source_unit"]].drop_duplicates().groupby("source_file").size()
    work["weight"] = work["source_file"].map(lambda s: 1.0 / float(source_unit_counts.loc[s]))
    return work.groupby("entity")["weight"].sum().sort_values(ascending=False)


def collapsed_scores(units: pd.DataFrame, collapse_col: str) -> pd.Series:
    work = units[[collapse_col, "entity"]].drop_duplicates()
    return work.groupby("entity")[collapse_col].nunique().sort_values(ascending=False)


def weighted_null(units: pd.DataFrame, entities: list[str], rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    rows = units.groupby(["source_unit", "source_file"])["entity"].nunique().reset_index(name="n")
    source_unit_counts = units[["source_file", "source_unit"]].drop_duplicates().groupby("source_file").size()
    rows["weight"] = rows["source_file"].map(lambda s: 1.0 / float(source_unit_counts.loc[s]))
    entities_arr = np.array(entities)
    max_scores = np.zeros(N_REPS, dtype=float)
    target_scores = np.zeros(N_REPS, dtype=float)
    records = rows.to_dict(orient="records")
    for i in range(N_REPS):
        counts = {entity: 0.0 for entity in entities}
        for row in records:
            sampled = rng.choice(entities_arr, size=min(int(row["n"]), len(entities_arr)), replace=False)
            weight = float(row["weight"])
            for entity in sampled:
                counts[str(entity)] += weight
        values = np.array(list(counts.values()), dtype=float)
        max_scores[i] = float(values.max()) if len(values) else 0.0
        target_scores[i] = float(counts.get(TARGET, 0.0))
    return max_scores, target_scores


def collapsed_null(units: pd.DataFrame, entities: list[str], collapse_col: str, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    rows = units.groupby(collapse_col)["entity"].nunique().reset_index(name="n")
    entities_arr = np.array(entities)
    max_scores = np.zeros(N_REPS, dtype=int)
    target_scores = np.zeros(N_REPS, dtype=int)
    records = rows.to_dict(orient="records")
    for i in range(N_REPS):
        counts = {entity: 0 for entity in entities}
        for row in records:
            sampled = rng.choice(entities_arr, size=min(int(row["n"]), len(entities_arr)), replace=False)
            for entity in sampled:
                counts[str(entity)] += 1
        values = np.array(list(counts.values()), dtype=int)
        max_scores[i] = int(values.max()) if len(values) else 0
        target_scores[i] = int(counts.get(TARGET, 0))
    return max_scores, target_scores


def pvals(observed: float, max_null: np.ndarray, target_null: np.ndarray) -> dict[str, float]:
    return {
        "target_entity_p": float((np.sum(target_null >= observed) + 1) / (len(target_null) + 1)),
        "target_fwer_p": float((np.sum(max_null >= observed) + 1) / (len(max_null) + 1)),
        "max_null_p95": float(np.quantile(max_null, 0.95)),
        "max_null_p99": float(np.quantile(max_null, 0.99)),
        "target_null_p95": float(np.quantile(target_null, 0.95)),
        "target_null_p99": float(np.quantile(target_null, 0.99)),
    }


def main() -> int:
    evidence = pd.read_csv(V41 / "integrated_evidence_frame.tsv", sep="\t")
    units = positive_units(evidence)
    entities = sorted(evidence["entity"].unique().tolist())
    rng = np.random.default_rng(SEED)

    weighted = weighted_scores(units)
    weighted.to_frame("source_file_weighted_recurrence").reset_index().to_csv(
        OUT / "source_file_weighted_recurrence.tsv", sep="\t", index=False
    )
    w_max, w_target = weighted_null(units, entities, rng)
    weighted_observed = float(weighted.get(TARGET, 0.0))
    weighted_row = {
        "sensitivity": "source_file_weighted",
        "observed_target": weighted_observed,
        "observed_target_rank": int(weighted.rank(ascending=False, method="min").get(TARGET, np.nan)),
        "n_reps": N_REPS,
        **pvals(weighted_observed, w_max, w_target),
    }

    collapsed_rows = []
    for collapse_col, label in [
        ("modality_family_unit", "modality_source_family_collapsed"),
        ("source_family", "source_family_collapsed"),
    ]:
        collapsed = collapsed_scores(units, collapse_col)
        collapsed.to_frame(f"{label}_recurrence").reset_index().to_csv(
            OUT / f"{label}_recurrence.tsv", sep="\t", index=False
        )
        c_max, c_target = collapsed_null(units, entities, collapse_col, rng)
        observed = float(collapsed.get(TARGET, 0))
        collapsed_rows.append(
            {
                "sensitivity": label,
                "observed_target": observed,
                "observed_target_rank": int(collapsed.rank(ascending=False, method="min").get(TARGET, np.nan)),
                "n_reps": N_REPS,
                **pvals(observed, c_max, c_target),
            }
        )

    null_summary = pd.DataFrame([weighted_row] + collapsed_rows)
    null_summary.to_csv(OUT / "convergence_sensitivity_null_summary.tsv", sep="\t", index=False)
    family_table = (
        units[units["entity"].eq(TARGET)]
        .groupby(["source_family", "modality"], as_index=False)
        .agg(source_units=("source_unit", "nunique"))
        .sort_values("source_units", ascending=False)
    )
    family_table.to_csv(OUT / "target_source_family_breakdown.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "n_reps": N_REPS,
        "target": TARGET,
        "target_source_file_weighted_observed": weighted_observed,
        "target_source_file_weighted_fwer_p": float(weighted_row["target_fwer_p"]),
        "target_modality_family_observed": float(collapsed_rows[0]["observed_target"]),
        "target_modality_family_fwer_p": float(collapsed_rows[0]["target_fwer_p"]),
        "target_source_family_observed": float(collapsed_rows[1]["observed_target"]),
        "target_source_family_fwer_p": float(collapsed_rows[1]["target_fwer_p"]),
        "interpretation": (
            "APC/HLA/IFN recurrence remains exceptional after source-file "
            "weighting and source-family collapse if all FWER p-values stay "
            "below 0.05."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

