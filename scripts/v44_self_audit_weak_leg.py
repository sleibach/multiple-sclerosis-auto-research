#!/usr/bin/env python3
"""Characterize why V41 joint z is borderline while recurrence is robust."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
V41 = ROOT / "analysis" / "v41_joint_inference"
OUT = ROOT / "analysis" / "v44_self_audit_weak_leg"
OUT.mkdir(parents=True, exist_ok=True)

TARGET = "apc_hla_ifn_monitoring"


def stouffer(values: list[float]) -> float:
    vals = [float(v) for v in values if pd.notna(v)]
    if not vals:
        return 0.0
    return sum(vals) / math.sqrt(len(vals))


def main() -> int:
    matrix = pd.read_csv(V41 / "entity_modality_evidence_matrix.tsv", sep="\t")
    joint = pd.read_csv(V41 / "joint_inference_entity_results.tsv", sep="\t")
    recur = pd.read_csv(V41 / "recurring_signal_meta_results.tsv", sep="\t")
    split = json.loads((V41 / "heldout_modality_split.json").read_text())
    train = set(split["train_modalities"])
    train_matrix = matrix[matrix["modality"].isin(train)].copy()

    target_rows = train_matrix[train_matrix["entity"].eq(TARGET)].copy()
    target_values = target_rows["support_z"].astype(float).tolist()
    full_z = stouffer(target_values)
    contribution_rows = []
    for row in target_rows.to_dict(orient="records"):
        leave_values = [
            float(other["support_z"])
            for other in target_rows.to_dict(orient="records")
            if other["modality"] != row["modality"]
        ]
        contribution_rows.append(
            {
                "entity": TARGET,
                "modality": row["modality"],
                "support_z": row["support_z"],
                "n_rows": row["n_rows"],
                "min_p": row["min_p"],
                "leave_one_joint_z": stouffer(leave_values),
                "delta_joint_z_if_removed": full_z - stouffer(leave_values),
                "sources": row["sources"],
            }
        )
    contributions = pd.DataFrame(contribution_rows).sort_values(
        "delta_joint_z_if_removed", ascending=False
    )
    contributions.to_csv(OUT / "apc_hla_ifn_modality_contributions.tsv", sep="\t", index=False)

    modality_max_rows = []
    for modality, sub in train_matrix.groupby("modality"):
        top = sub.sort_values("support_z", ascending=False).head(5)
        for rank, row in enumerate(top.to_dict(orient="records"), start=1):
            modality_max_rows.append(
                {
                    "modality": modality,
                    "rank": rank,
                    "entity": row["entity"],
                    "support_z": row["support_z"],
                    "n_rows": row["n_rows"],
                    "min_p": row["min_p"],
                }
            )
    modality_max = pd.DataFrame(modality_max_rows)
    modality_max.to_csv(OUT / "train_modality_top_z_entities.tsv", sep="\t", index=False)

    top_joint = joint.sort_values("train_joint_z", ascending=False).head(20).copy()
    top_joint["passes_recurrence_fwer_0_10"] = top_joint["entity"].isin(
        recur[recur["recurrence_empirical_fwer_p"].lt(0.10)]["entity"]
    )
    top_joint.to_csv(OUT / "joint_vs_recurrence_top_entities.tsv", sep="\t", index=False)

    target_joint = joint[joint["entity"].eq(TARGET)].iloc[0].to_dict()
    target_recur = recur[recur["entity"].eq(TARGET)].iloc[0].to_dict()
    recurrence_top = int(target_recur["positive_source_units"])
    recurrence_null_p95 = 12
    recurrence_margin = recurrence_top / recurrence_null_p95
    joint_null_p95 = 8.1547
    joint_margin = float(target_joint["train_joint_z"]) / joint_null_p95
    single_modality_extremes = modality_max[modality_max["rank"].eq(1)].sort_values(
        "support_z", ascending=False
    )
    summary = {
        "target": TARGET,
        "target_train_joint_z": float(target_joint["train_joint_z"]),
        "target_train_fwer": float(target_joint["train_empirical_fwer_p"]),
        "joint_null_p95_from_v41_v43": joint_null_p95,
        "joint_z_to_null_p95_ratio": joint_margin,
        "target_positive_source_units": recurrence_top,
        "recurrence_fwer": float(target_recur["recurrence_empirical_fwer_p"]),
        "recurrence_null_max_p95": recurrence_null_p95,
        "recurrence_to_null_p95_ratio": recurrence_margin,
        "target_train_modalities": int(target_joint["train_support_modalities"]),
        "largest_leave_one_delta": float(contributions["delta_joint_z_if_removed"].max()),
        "smallest_leave_one_joint_z": float(contributions["leave_one_joint_z"].min()),
        "top_single_modality_z": float(single_modality_extremes["support_z"].max()),
        "top_single_modality_entity": str(single_modality_extremes.iloc[0]["entity"]),
        "interpretation": "joint z is borderline because the family-wise max-z null is high relative to the target z; recurrence is robust because the source-unit count is far beyond its null envelope",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
