#!/usr/bin/env python3
"""Run a bounded association-network control probe for the APC axis.

V26 dependencies are symmetric associations, not causal edges. This script
therefore treats controllability metrics as cross-domain triage only and
requires fixed-direction goal alignment, a seeded label-permutation null, and
cross-stimulus replication before prioritizing a control node.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "analysis/v26_deep_structure/workstream_b_module_dependencies.tsv"
PERTURBATIONS = ROOT / "analysis/v26_deep_structure/perturbation_module_matrix.tsv"
OUT = ROOT / "analysis/v53_network_control_probe"
MODULES = (
    "gilt_lysosomal_apc",
    "hla_ii_apc",
    "ifn_apc",
    "mif_cd74_receptor_state",
)
GOAL = np.array([0.0, -1.0, 0.0, -1.0], dtype=float)
SPECTRAL_RADIUS = 0.8
HORIZON = 5
SEED = 53003
N_PERMUTATIONS = 20_000


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def build_network() -> tuple[np.ndarray, list[dict[str, Any]]]:
    rows = read_tsv(DEPENDENCIES)
    grouped: dict[tuple[str, str], list[float]] = {}
    modalities: dict[tuple[str, str], list[str]] = {}
    for row in rows:
        if row["claim_grade"] != "supported":
            continue
        left = row["module_a"]
        right = row["module_b"]
        if left not in MODULES or right not in MODULES:
            continue
        pair = tuple(sorted((left, right)))
        grouped.setdefault(pair, []).append(float(row["spearman_r"]))
        modalities.setdefault(pair, []).append(row["modality"])

    adjacency = np.zeros((len(MODULES), len(MODULES)), dtype=float)
    edge_rows: list[dict[str, Any]] = []
    for pair, values in sorted(grouped.items()):
        left, right = pair
        weight = float(np.median(values))
        left_index = MODULES.index(left)
        right_index = MODULES.index(right)
        adjacency[left_index, right_index] = weight
        adjacency[right_index, left_index] = weight
        edge_rows.append(
            {
                "module_a": left,
                "module_b": right,
                "median_supported_spearman": weight,
                "n_supported_modalities": len(values),
                "supported_modalities": ";".join(sorted(modalities[pair])),
            }
        )
    eigenvalues = np.linalg.eigvals(adjacency)
    observed_radius = float(np.max(np.abs(eigenvalues))) if eigenvalues.size else 0.0
    if observed_radius > 0:
        adjacency *= SPECTRAL_RADIUS / observed_radius
    return adjacency, edge_rows


def load_perturbations() -> list[dict[str, Any]]:
    rows = read_tsv(PERTURBATIONS)
    label_column = next(iter(rows[0]))
    parsed: list[dict[str, Any]] = []
    for row in rows:
        stimulus, node = row[label_column].split(":", 1)
        parsed.append(
            {
                "stimulus": stimulus,
                "node": node,
                "label": row[label_column],
                "values": np.array([float(row[module]) for module in MODULES], dtype=float),
            }
        )
    return parsed


def propagated_response(adjacency: np.ndarray, control: np.ndarray) -> np.ndarray:
    response = np.zeros_like(control)
    transition = np.eye(len(control))
    for _ in range(HORIZON):
        response += transition @ control
        transition = adjacency @ transition
    return response


def alignment_metrics(adjacency: np.ndarray, control: np.ndarray) -> dict[str, float]:
    response = propagated_response(adjacency, control)
    response_norm = float(np.linalg.norm(response))
    goal_norm = float(np.linalg.norm(GOAL))
    cosine = float(np.dot(response, GOAL) / (response_norm * goal_norm)) if response_norm else 0.0
    by_module = dict(zip(MODULES, response, strict=True))
    target_suppression = -float(
        np.mean([by_module["hla_ii_apc"], by_module["mif_cd74_receptor_state"]])
    )
    collateral = max(0.0, -float(by_module["ifn_apc"])) + max(
        0.0, -float(by_module["gilt_lysosomal_apc"])
    )

    return {
        "goal_cosine": cosine,
        "target_suppression": target_suppression,
        "collateral_suppression": collateral,
        "selective_goal_score": target_suppression - collateral,
    }


def control_metrics(adjacency: np.ndarray, control: np.ndarray) -> dict[str, float | int]:
    alignment = alignment_metrics(adjacency, control)
    goal_norm = float(np.linalg.norm(GOAL))
    columns = []
    transition_control = control.copy()
    for _ in range(len(MODULES)):
        columns.append(transition_control)
        transition_control = adjacency @ transition_control
    controllability = np.column_stack(columns)
    rank = int(np.linalg.matrix_rank(controllability, tol=1e-10))

    gramian = np.zeros_like(adjacency)
    transition = np.eye(len(MODULES))
    for _ in range(HORIZON):
        vector = transition @ control
        gramian += np.outer(vector, vector)
        transition = adjacency @ transition
    projection = gramian @ np.linalg.pinv(gramian) @ GOAL
    residual_ratio = float(np.linalg.norm(GOAL - projection) / goal_norm)
    minimum_energy = (
        float(GOAL @ np.linalg.pinv(gramian) @ GOAL)
        if residual_ratio <= 1e-8
        else float("inf")
    )
    return {
        **alignment,
        "controllability_rank": rank,
        "goal_projection_residual_ratio": residual_ratio,
        "unconstrained_minimum_energy": minimum_energy,
    }


def bh_adjust(p_values: list[float]) -> list[float]:
    order = np.argsort(p_values)
    adjusted = np.ones(len(p_values), dtype=float)
    running = 1.0
    for offset, index in enumerate(order[::-1], start=1):
        rank = len(p_values) - offset + 1
        running = min(running, p_values[int(index)] * len(p_values) / rank)
        adjusted[int(index)] = running
    return adjusted.tolist()


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


def main() -> int:
    adjacency, edge_rows = build_network()
    perturbations = load_perturbations()
    rng = np.random.default_rng(SEED)
    observed_metrics = [control_metrics(adjacency, row["values"]) for row in perturbations]
    null_scores = np.empty((N_PERMUTATIONS, len(perturbations)), dtype=float)
    null_cosines = np.empty_like(null_scores)
    for permutation_index in range(N_PERMUTATIONS):
        for row_index, row in enumerate(perturbations):
            metrics = alignment_metrics(adjacency, rng.permutation(row["values"]))
            null_scores[permutation_index, row_index] = float(metrics["selective_goal_score"])
            null_cosines[permutation_index, row_index] = float(metrics["goal_cosine"])

    score_p_values: list[float] = []
    cosine_p_values: list[float] = []
    for row_index, metrics in enumerate(observed_metrics):
        score = float(metrics["selective_goal_score"])
        cosine = float(metrics["goal_cosine"])
        score_p_values.append(
            (1 + int(np.sum(null_scores[:, row_index] >= score))) / (N_PERMUTATIONS + 1)
        )
        cosine_p_values.append(
            (1 + int(np.sum(null_cosines[:, row_index] >= cosine))) / (N_PERMUTATIONS + 1)
        )
    score_q_values = bh_adjust(score_p_values)
    cosine_q_values = bh_adjust(cosine_p_values)

    preliminary: list[bool] = []
    for row_index, metrics in enumerate(observed_metrics):
        preliminary.append(
            float(metrics["goal_cosine"]) >= 0.7
            and float(metrics["target_suppression"]) >= 0.5
            and float(metrics["selective_goal_score"]) > 0
            and score_q_values[row_index] <= 0.10
            and cosine_q_values[row_index] <= 0.10
        )
    passing_contexts_by_node: dict[str, int] = {}
    for row, passed in zip(perturbations, preliminary, strict=True):
        if passed:
            passing_contexts_by_node[row["node"]] = passing_contexts_by_node.get(row["node"], 0) + 1

    result_rows: list[dict[str, Any]] = []
    for row_index, (row, metrics) in enumerate(zip(perturbations, observed_metrics, strict=True)):
        replicated = preliminary[row_index] and passing_contexts_by_node.get(row["node"], 0) >= 2
        result_rows.append(
            {
                "stimulus": row["stimulus"],
                "node": row["node"],
                "label": row["label"],
                "goal_cosine": round(float(metrics["goal_cosine"]), 6),
                "target_suppression": round(float(metrics["target_suppression"]), 6),
                "collateral_suppression": round(float(metrics["collateral_suppression"]), 6),
                "selective_goal_score": round(float(metrics["selective_goal_score"]), 6),
                "controllability_rank": int(metrics["controllability_rank"]),
                "goal_projection_residual_ratio": round(
                    float(metrics["goal_projection_residual_ratio"]), 9
                ),
                "unconstrained_minimum_energy": (
                    round(float(metrics["unconstrained_minimum_energy"]), 6)
                    if np.isfinite(float(metrics["unconstrained_minimum_energy"]))
                    else "inf"
                ),
                "score_empirical_p": score_p_values[row_index],
                "score_q_bh": score_q_values[row_index],
                "cosine_empirical_p": cosine_p_values[row_index],
                "cosine_q_bh": cosine_q_values[row_index],
                "preliminary_context_gate": preliminary[row_index],
                "passing_contexts_for_node": passing_contexts_by_node.get(row["node"], 0),
                "replicated_control_candidate": replicated,
            }
        )

    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "network_edges.tsv", edge_rows)
    matrix_rows = [
        {"module": module, **{other: round(float(adjacency[i, j]), 8) for j, other in enumerate(MODULES)}}
        for i, module in enumerate(MODULES)
    ]
    write_tsv(OUT / "stable_adjacency_matrix.tsv", matrix_rows)
    result_rows.sort(key=lambda row: float(row["selective_goal_score"]), reverse=True)
    write_tsv(OUT / "control_signature_tests.tsv", result_rows)

    replicated_candidates = sorted(
        {row["node"] for row in result_rows if row["replicated_control_candidate"]}
    )
    preliminary_rows = [row["label"] for row in result_rows if row["preliminary_context_gate"]]
    summary = {
        "purpose": "V53 bounded association-network control probe",
        "inputs": [str(DEPENDENCIES.relative_to(ROOT)), str(PERTURBATIONS.relative_to(ROOT))],
        "modules": list(MODULES),
        "goal": dict(zip(MODULES, GOAL.tolist(), strict=True)),
        "network_edge_rule": "median Spearman across V26 claim_grade=supported modality rows",
        "network_is_causal": False,
        "spectral_radius": SPECTRAL_RADIUS,
        "horizon": HORIZON,
        "seed": SEED,
        "n_permutations": N_PERMUTATIONS,
        "n_perturbation_signatures": len(perturbations),
        "n_preliminary_context_passes": len(preliminary_rows),
        "preliminary_context_pass_labels": preliminary_rows,
        "replicated_control_candidates": replicated_candidates,
        "verdict": (
            "REPLICATED_CONTROL_CANDIDATE_SUPPORTED_FOR_FOLLOWUP"
            if replicated_candidates
            else "NO_REPLICATED_SELECTIVE_CONTROL_NODE_UNDER_NULL_GATE"
        ),
        "interpretation": (
            "Association-network propagation did not nominate a causal target. A node must also "
            "pass held-data direction, modality, and perturbation-specificity gates."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 APC Association-Network Control Probe",
        "",
        "The network uses symmetric replicated V26 module dependencies and is not a causal graph.",
        "Controllability metrics are cross-domain triage, not target evidence.",
        "",
        f"Signatures: `{len(perturbations)}`. Seeded label permutations: `{N_PERMUTATIONS}`.",
        f"Horizon: `{HORIZON}`. Stabilized spectral radius: `{SPECTRAL_RADIUS}`.",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"Preliminary context passes: `{len(preliminary_rows)}`.",
        f"Replicated control candidates: `{';'.join(replicated_candidates) or 'none'}`.",
        "",
        "Any single-context pass remains a hypothesis requiring an independent context and a real",
        "directed perturbation experiment. No network score overrides causal, direction, or modality",
        "gates.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
