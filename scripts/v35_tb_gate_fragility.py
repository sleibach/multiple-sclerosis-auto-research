#!/usr/bin/env python3
"""Fragility checks for V35 T/B compartment remodeling gate."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INFILE = ROOT / "analysis/v23_apc_hla_monitoring/gse253006_exact_compartments/gse253006_exact_compartment_paired_scores.tsv"
OUTDIR = ROOT / "analysis/v35_tb_gate_fragility"
OUTDIR.mkdir(parents=True, exist_ok=True)


def auc(scores: list[float], labels: list[int]) -> float | None:
    pos = [s for s, y in zip(scores, labels) if y == 1]
    neg = [s for s, y in zip(scores, labels) if y == 0]
    if not pos or not neg:
        return None
    total = 0.0
    for p in pos:
        for n in neg:
            total += 1.0 if p > n else 0.5 if p == n else 0.0
    return total / (len(pos) * len(neg))


rows = list(csv.DictReader(INFILE.open(), delimiter="\t"))
patients = sorted({r["patient"] for r in rows})
compartments = sorted({r["marker_compartment"] for r in rows})
tb = {"t_cell_like", "b_plasma_like"}


def comp_aucs(subrows: list[dict[str, str]]) -> dict[str, float | None]:
    out = {}
    for comp in compartments:
        s = [r for r in subrows if r["marker_compartment"] == comp]
        labels = [1 if r["response"] == "Responder" else 0 for r in s]
        scores = [float(r["locked_signed_score"]) for r in s]
        out[comp] = auc(scores, labels)
    return out


def gate_gap(aucs: dict[str, float | None]) -> float | None:
    tb_vals = [aucs[c] for c in tb if aucs[c] is not None]
    non_vals = [v for c, v in aucs.items() if c not in tb and v is not None]
    if not tb_vals or not non_vals:
        return None
    return sum(tb_vals) / len(tb_vals) - sum(non_vals) / len(non_vals)


original = comp_aucs(rows)
original_gap = gate_gap(original)

loo = []
for patient in patients:
    sub = [r for r in rows if r["patient"] != patient]
    aucs = comp_aucs(sub)
    loo.append(
        {
            "left_out_patient": patient,
            "left_out_response": next(r["response"] for r in rows if r["patient"] == patient),
            "left_out_timepoint": next(r["treated_timepoint"] for r in rows if r["patient"] == patient),
            "tb_minus_non_tb_auc_gap": gate_gap(aucs),
            **{f"auc_{k}": v for k, v in aucs.items()},
        }
    )

no_w48 = [r for r in rows if r["treated_timepoint"] != "W48"]
no_w48_aucs = comp_aucs(no_w48)

with (OUTDIR / "leave_one_patient.tsv").open("w", newline="") as fh:
    fields = list(loo[0].keys())
    writer = csv.DictWriter(fh, delimiter="\t", fieldnames=fields)
    writer.writeheader()
    writer.writerows(loo)

with (OUTDIR / "original_and_no_w48.tsv").open("w", newline="") as fh:
    fields = ["scenario", "tb_minus_non_tb_auc_gap"] + [f"auc_{c}" for c in compartments]
    writer = csv.DictWriter(fh, delimiter="\t", fieldnames=fields)
    writer.writeheader()
    writer.writerow(
        {
            "scenario": "original_n9",
            "tb_minus_non_tb_auc_gap": original_gap,
            **{f"auc_{c}": v for c, v in original.items()},
        }
    )
    writer.writerow(
        {
            "scenario": "exclude_W48_n8",
            "tb_minus_non_tb_auc_gap": gate_gap(no_w48_aucs),
            **{f"auc_{c}": v for c, v in no_w48_aucs.items()},
        }
    )

valid_gaps = [r["tb_minus_non_tb_auc_gap"] for r in loo if r["tb_minus_non_tb_auc_gap"] is not None]
summary = {
    "hypothesis": "T/B compartment remodeling gate fragility",
    "grounded_result": "fragile_but_not_collapsed",
    "original": {
        "n_patients": len(patients),
        "tb_minus_non_tb_auc_gap": original_gap,
        "compartment_aucs": original,
    },
    "exclude_W48": {
        "n_patients": len({r["patient"] for r in no_w48}),
        "tb_minus_non_tb_auc_gap": gate_gap(no_w48_aucs),
        "compartment_aucs": no_w48_aucs,
    },
    "leave_one_patient_gap_min": min(valid_gaps),
    "leave_one_patient_gap_max": max(valid_gaps),
    "leave_one_patient_n_negative_or_zero_gap": sum(1 for g in valid_gaps if g <= 0),
    "interpretation": (
        "The T/B gate remains directionally positive under leave-one-patient and "
        "W48 exclusion checks, but the gap varies substantially in n=8 subsets. "
        "This is compatible with a real compartment context signal but is too "
        "fragile for a generalizable biomarker claim without independent replication."
    ),
}
with (OUTDIR / "summary.json").open("w") as fh:
    json.dump(summary, fh, indent=2, sort_keys=True)
print(json.dumps(summary, indent=2, sort_keys=True))
