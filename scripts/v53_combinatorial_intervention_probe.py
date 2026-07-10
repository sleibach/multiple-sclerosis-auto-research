#!/usr/bin/env python3
"""Test additive two-node APC-axis intervention logic on held perturbations.

This is a grounded triage of an additive-combination hypothesis, not evidence
of pharmacologic synergy. It uses the committed V26 perturbation module matrix
and a seeded within-row module-label permutation null.
"""

from __future__ import annotations

import csv
import itertools
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v26_deep_structure/perturbation_module_matrix.tsv"
OUT = ROOT / "analysis/v53_combinatorial_intervention_probe"
MODULES = (
    "gilt_lysosomal_apc",
    "hla_ii_apc",
    "ifn_apc",
    "mif_cd74_receptor_state",
)
TARGET_MODULES = ("hla_ii_apc", "mif_cd74_receptor_state")
SEED = 53002
N_PERMUTATIONS = 20_000
MIN_EFFECTIVE_TARGET_SUPPRESSION = 0.5
MIN_PAIR_IMPROVEMENT = 0.2


@dataclass(frozen=True)
class Signature:
    stimulus: str
    node: str
    values: np.ndarray


def load_signatures() -> list[Signature]:
    rows: list[Signature] = []
    with INPUT.open() as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        first_column = reader.fieldnames[0] if reader.fieldnames else ""
        for row in reader:
            label = str(row[first_column])
            stimulus, node = label.split(":", 1)
            rows.append(
                Signature(
                    stimulus=stimulus,
                    node=node,
                    values=np.array([float(row[module]) for module in MODULES], dtype=float),
                )
            )
    if not rows:
        raise RuntimeError(f"No perturbation signatures loaded from {INPUT}")
    return rows


def metrics(values: np.ndarray) -> dict[str, float]:
    by_module = dict(zip(MODULES, values, strict=True))
    target_suppression = -float(np.mean([by_module[module] for module in TARGET_MODULES]))
    ifn_collateral = max(0.0, -float(by_module["ifn_apc"]))
    lysosomal_collateral = max(0.0, -float(by_module["gilt_lysosomal_apc"]))
    return {
        "target_suppression": target_suppression,
        "ifn_collateral_suppression": ifn_collateral,
        "lysosomal_collateral_suppression": lysosomal_collateral,
        "primary_selectivity": target_suppression - ifn_collateral,
        "guarded_selectivity": target_suppression - max(ifn_collateral, lysosomal_collateral),
    }


def evaluate_context(
    signatures: list[Signature],
    pair_mode: str,
    objective: str,
) -> dict[str, Any]:
    singles = [(signature.node, metrics(signature.values), signature.values) for signature in signatures]
    best_single = max(singles, key=lambda item: item[1][objective])
    pairs: list[tuple[str, dict[str, float], np.ndarray]] = []
    for left, right in itertools.combinations(signatures, 2):
        values = left.values + right.values
        if pair_mode == "fixed_total_average":
            values = values / 2.0
        pairs.append((f"{left.node}+{right.node}", metrics(values), values))
    best_pair = max(pairs, key=lambda item: item[1][objective])
    return {
        "best_single": best_single[0],
        "best_single_metrics": best_single[1],
        "best_pair": best_pair[0],
        "best_pair_metrics": best_pair[1],
        "pair_improvement_over_best_single": (
            best_pair[1][objective] - best_single[1][objective]
        ),
    }


def bh_adjust(p_values: list[float]) -> list[float]:
    order = np.argsort(p_values)
    adjusted = np.ones(len(p_values), dtype=float)
    running = 1.0
    for rank_from_end, index in enumerate(order[::-1], start=1):
        rank = len(p_values) - rank_from_end + 1
        running = min(running, p_values[int(index)] * len(p_values) / rank)
        adjusted[int(index)] = running
    return adjusted.tolist()


def permuted_signatures(signatures: list[Signature], rng: np.random.Generator) -> list[Signature]:
    return [
        Signature(signature.stimulus, signature.node, rng.permutation(signature.values))
        for signature in signatures
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


def main() -> int:
    signatures = load_signatures()
    stimuli = sorted({signature.stimulus for signature in signatures})
    by_stimulus = {
        stimulus: [signature for signature in signatures if signature.stimulus == stimulus]
        for stimulus in stimuli
    }
    test_specs = [
        (stimulus, pair_mode, objective)
        for stimulus in stimuli
        for pair_mode in ("full_additive", "fixed_total_average")
        for objective in ("primary_selectivity", "guarded_selectivity")
    ]
    observed = [
        evaluate_context(by_stimulus[stimulus], pair_mode, objective)
        for stimulus, pair_mode, objective in test_specs
    ]

    rng = np.random.default_rng(SEED)
    null_improvements = np.empty((N_PERMUTATIONS, len(test_specs)), dtype=float)
    for permutation_index in range(N_PERMUTATIONS):
        permuted = permuted_signatures(signatures, rng)
        permuted_by_stimulus = {
            stimulus: [signature for signature in permuted if signature.stimulus == stimulus]
            for stimulus in stimuli
        }
        for test_index, (stimulus, pair_mode, objective) in enumerate(test_specs):
            null_result = evaluate_context(
                permuted_by_stimulus[stimulus], pair_mode, objective
            )
            null_improvements[permutation_index, test_index] = float(
                null_result["pair_improvement_over_best_single"]
            )

    raw_p_values = []
    max_null = np.max(null_improvements, axis=1)
    for test_index, result in enumerate(observed):
        observed_improvement = float(result["pair_improvement_over_best_single"])
        raw_p_values.append(
            (1 + int(np.sum(null_improvements[:, test_index] >= observed_improvement)))
            / (N_PERMUTATIONS + 1)
        )
    q_values = bh_adjust(raw_p_values)

    result_rows: list[dict[str, Any]] = []
    for test_index, ((stimulus, pair_mode, objective), result) in enumerate(
        zip(test_specs, observed, strict=True)
    ):
        improvement = float(result["pair_improvement_over_best_single"])
        best_pair_metrics = result["best_pair_metrics"]
        fwer_p = (1 + int(np.sum(max_null >= improvement))) / (N_PERMUTATIONS + 1)
        prioritization_gate = (
            improvement >= MIN_PAIR_IMPROVEMENT
            and float(best_pair_metrics["target_suppression"])
            >= MIN_EFFECTIVE_TARGET_SUPPRESSION
            and float(best_pair_metrics[objective]) > 0
            and q_values[test_index] <= 0.05
            and fwer_p <= 0.05
        )
        result_rows.append(
            {
                "stimulus": stimulus,
                "n_single_nodes": len(by_stimulus[stimulus]),
                "n_pairs": len(list(itertools.combinations(by_stimulus[stimulus], 2))),
                "pair_mode": pair_mode,
                "objective": objective,
                "best_single": result["best_single"],
                "best_single_objective": round(
                    float(result["best_single_metrics"][objective]), 6
                ),
                "best_pair": result["best_pair"],
                "best_pair_objective": round(float(best_pair_metrics[objective]), 6),
                "best_pair_target_suppression": round(
                    float(best_pair_metrics["target_suppression"]), 6
                ),
                "pair_improvement_over_best_single": round(improvement, 6),
                "empirical_p": raw_p_values[test_index],
                "q_bh": q_values[test_index],
                "max_t_fwer_p": fwer_p,
                "prioritization_gate": prioritization_gate,
            }
        )

    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "combination_tests.tsv", result_rows)
    n_pass = sum(bool(row["prioritization_gate"]) for row in result_rows)
    summary = {
        "purpose": "V53 additive two-node intervention triage on held perturbation signatures",
        "input": str(INPUT.relative_to(ROOT)),
        "seed": SEED,
        "n_permutations": N_PERMUTATIONS,
        "n_signatures": len(signatures),
        "stimuli": stimuli,
        "n_tests": len(result_rows),
        "multiple_testing": "BH across all tests plus max-T family-wise permutation p",
        "n_prioritization_gate_passes": n_pass,
        "verdict": (
            "ADDITIVE_COMBINATION_PRIORITY_SUPPORTED_NEEDS_REAL_COMBINATION_DATA"
            if n_pass
            else "NO_ADDITIVE_PAIR_OUTPERFORMS_THE_BEST_SINGLE_NODE_UNDER_NULL_GATE"
        ),
        "interpretation": (
            "No biological synergy is claimed. The additive model only tests whether held "
            "single-node signatures justify prioritizing a real combination experiment."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 Combinatorial Intervention Probe",
        "",
        "This analysis uses real held perturbation-module signatures. Additive and fixed-total",
        "pair constructions are model-based triage and are not biological combination evidence.",
        "",
        f"Seed: `{SEED}`. Module-label permutations: `{N_PERMUTATIONS}`.",
        "Multiple testing: BH across all tests plus max-T family-wise permutation p.",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"Prioritization-gate passes: `{n_pass}/{len(result_rows)}`.",
        "",
        "The result cannot establish synergy. A passing row would only prioritize a real",
        "factorial perturbation experiment; a null means the current single-node data do not",
        "justify a multi-node therapeutic upgrade.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
