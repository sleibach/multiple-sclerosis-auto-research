#!/usr/bin/env python3
"""Ground V35 T/B compartment remodeling gate on exact compartment scores.

Uses only the V23 paired compartment scores and exact-label permutations.
"""

from __future__ import annotations

import csv
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INFILE = ROOT / "analysis/v23_apc_hla_monitoring/gse253006_exact_compartments/gse253006_exact_compartment_paired_scores.tsv"
OUTDIR = ROOT / "analysis/v35_tb_compartment_gate"
OUTDIR.mkdir(parents=True, exist_ok=True)


def auc(scores: list[float], labels: list[int]) -> float:
    pos = [s for s, y in zip(scores, labels) if y == 1]
    neg = [s for s, y in zip(scores, labels) if y == 0]
    total = 0.0
    for p in pos:
        for n in neg:
            if p > n:
                total += 1.0
            elif p == n:
                total += 0.5
    return total / (len(pos) * len(neg))


def exact_auc_p(scores: list[float], labels: list[int], observed: float) -> float:
    n_pos = sum(labels)
    n = len(labels)
    extreme = 0
    total = 0
    for pos_idx in itertools.combinations(range(n), n_pos):
        y = [0] * n
        for i in pos_idx:
            y[i] = 1
        total += 1
        if auc(scores, y) >= observed - 1e-12:
            extreme += 1
    return extreme / total


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


rows: list[dict[str, str]] = []
with INFILE.open() as fh:
    reader = csv.DictReader(fh, delimiter="\t")
    rows = list(reader)

compartments = sorted({r["marker_compartment"] for r in rows})
lymphoid = {"t_cell_like", "b_plasma_like"}

per_compartment = []
for comp in compartments:
    sub = [r for r in rows if r["marker_compartment"] == comp]
    labels = [1 if r["response"] == "Responder" else 0 for r in sub]
    locked = [float(r["locked_signed_score"]) for r in sub]
    receptor = [float(r["delta_RECEPTOR"]) for r in sub]
    obs_auc = auc(locked, labels)
    rec_auc = auc(receptor, labels)
    per_compartment.append(
        {
            "marker_compartment": comp,
            "class": "T/B-like" if comp in lymphoid else "non-T/B-like",
            "n": len(sub),
            "n_responders": sum(labels),
            "locked_auc": obs_auc,
            "locked_exact_perm_p_auc_ge_observed": exact_auc_p(locked, labels, obs_auc),
            "receptor_auc": rec_auc,
            "mean_locked_responder": mean([s for s, y in zip(locked, labels) if y == 1]),
            "mean_locked_nonresponder": mean([s for s, y in zip(locked, labels) if y == 0]),
        }
    )

tb_aucs = [r["locked_auc"] for r in per_compartment if r["marker_compartment"] in lymphoid]
non_tb_aucs = [r["locked_auc"] for r in per_compartment if r["marker_compartment"] not in lymphoid]
observed_gate_gap = mean(tb_aucs) - mean(non_tb_aucs)

# Exact patient-label permutation of the gate gap, keeping each patient's labels
# consistent across compartments. This tests whether T/B superiority is larger
# than expected under response-label exchangeability.
patients = sorted({r["patient"] for r in rows})
n_pos = len({r["patient"] for r in rows if r["response"] == "Responder"})
patient_scores: dict[str, dict[str, float]] = {p: {} for p in patients}
for r in rows:
    patient_scores[r["patient"]][r["marker_compartment"]] = float(r["locked_signed_score"])

extreme = 0
total = 0
null_gaps = []
for pos_patients in itertools.combinations(patients, n_pos):
    pos_set = set(pos_patients)
    comp_aucs = {}
    for comp in compartments:
        scores = [patient_scores[p][comp] for p in patients]
        labels = [1 if p in pos_set else 0 for p in patients]
        comp_aucs[comp] = auc(scores, labels)
    gap = mean([comp_aucs[c] for c in lymphoid]) - mean(
        [comp_aucs[c] for c in compartments if c not in lymphoid]
    )
    null_gaps.append(gap)
    total += 1
    if gap >= observed_gate_gap - 1e-12:
        extreme += 1

gate_perm_p = extreme / total

with (OUTDIR / "tb_compartment_gate.tsv").open("w", newline="") as fh:
    fieldnames = [
        "marker_compartment",
        "class",
        "n",
        "n_responders",
        "locked_auc",
        "locked_exact_perm_p_auc_ge_observed",
        "receptor_auc",
        "mean_locked_responder",
        "mean_locked_nonresponder",
    ]
    writer = csv.DictWriter(fh, delimiter="\t", fieldnames=fieldnames)
    writer.writeheader()
    for row in sorted(per_compartment, key=lambda x: x["locked_auc"], reverse=True):
        writer.writerow(row)

summary = {
    "hypothesis": "T/B compartment remodeling gate",
    "dataset": str(INFILE.relative_to(ROOT)),
    "n_patients": len(patients),
    "n_responders": n_pos,
    "tb_mean_locked_auc": mean(tb_aucs),
    "non_tb_mean_locked_auc": mean(non_tb_aucs),
    "observed_tb_minus_non_tb_auc_gap": observed_gate_gap,
    "patient_label_exact_permutation_p_gap_ge_observed": gate_perm_p,
    "null_permutations": total,
    "grounded_result": (
        "supported_but_small_n"
        if observed_gate_gap > 0 and gate_perm_p <= 0.10
        else "inconclusive_or_not_supported"
    ),
    "interpretation": (
        "T/B-like compartments have the highest locked-rule AUCs in the exact "
        "tofacitinib recheck; exact patient-label permutation tests whether that "
        "compartment advantage exceeds label-exchangeable expectation."
    ),
}
with (OUTDIR / "summary.json").open("w") as fh:
    json.dump(summary, fh, indent=2, sort_keys=True)

print(json.dumps(summary, indent=2, sort_keys=True))
