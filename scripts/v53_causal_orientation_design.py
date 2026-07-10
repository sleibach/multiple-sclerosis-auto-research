#!/usr/bin/env python3
"""Power and identifiability design for orienting the V53 APC module graph.

All generated cohorts are seeded synthetic method characterization. The script
does not infer a biological direction and does not treat current gene-level
perturbations as perfect module interventions.
"""

from __future__ import annotations

import csv
import itertools
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v53_causal_orientation_design"
NODES = ("hla_ii_apc", "ifn_apc", "mif_cd74_receptor_state")
INTERVENED = NODES[:2]
STRENGTHS = (0.3, 0.5, 0.8)
SAMPLE_SIZES = (8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256)
SEEDS = (53101, 53102, 53103)
N_REPLICATES_PER_SEED = 1_000
INTERVENTION_SHIFT = 1.0
MIN_EFFECT = 0.25
FDR = 0.05


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


def response_signature(order: tuple[str, ...], intervened: tuple[str, ...]) -> tuple[bool, ...]:
    position = {node: index for index, node in enumerate(order)}
    return tuple(
        position[source] < position[target]
        for source in intervened
        for target in order_nodes(order)
        if source != target
    )


def order_nodes(order: tuple[str, ...]) -> tuple[str, ...]:
    # Canonical target ordering makes signatures comparable across permutations.
    return tuple(sorted(order))


def ideal_identifiability() -> list[dict[str, Any]]:
    rows = []
    for node_count in (3, 4):
        nodes = tuple(chr(ord("A") + index) for index in range(node_count))
        orders = list(itertools.permutations(nodes))
        for n_interventions in range(node_count + 1):
            intervened = nodes[:n_interventions]
            signatures = {response_signature(order, intervened) for order in orders}
            rows.append(
                {
                    "complete_dag_nodes": node_count,
                    "possible_topological_orders": len(orders),
                    "perfect_single_node_interventions": n_interventions,
                    "distinct_reachability_signatures": len(signatures),
                    "all_orders_distinguishable": len(signatures) == len(orders),
                    "assumptions": "acyclic complete DAG; nonzero effects; perfect module-selective interventions; exact reachability",
                }
            )
    return rows


def simulate_arm(
    order: tuple[str, ...],
    strength: float,
    n_donors: int,
    n_replicates: int,
    rng: np.random.Generator,
    intervention: str | None,
) -> np.ndarray:
    index = {node: idx for idx, node in enumerate(NODES)}
    noise = rng.normal(size=(n_replicates, n_donors, len(NODES)))
    values = np.zeros_like(noise)
    previous: list[str] = []
    for node in order:
        node_index = index[node]
        if node == intervention:
            values[:, :, node_index] = INTERVENTION_SHIFT + noise[:, :, node_index]
        else:
            inherited = sum(strength * values[:, :, index[parent]] for parent in previous)
            values[:, :, node_index] = inherited + noise[:, :, node_index]
        previous.append(node)
    return values


def normal_two_sided_p(z: np.ndarray) -> np.ndarray:
    return np.fromiter(
        (math.erfc(abs(float(value)) / math.sqrt(2.0)) for value in z),
        dtype=float,
        count=z.size,
    ).reshape(z.shape)


def bh_rows(p_values: np.ndarray) -> np.ndarray:
    n_tests = p_values.shape[1]
    order = np.argsort(p_values, axis=1)
    ranked = np.take_along_axis(p_values, order, axis=1)
    adjusted_ranked = ranked * n_tests / np.arange(1, n_tests + 1)
    adjusted_ranked = np.minimum.accumulate(adjusted_ranked[:, ::-1], axis=1)[:, ::-1]
    adjusted_ranked = np.minimum(adjusted_ranked, 1.0)
    adjusted = np.empty_like(adjusted_ranked)
    np.put_along_axis(adjusted, order, adjusted_ranked, axis=1)
    return adjusted


def infer_signatures(
    order: tuple[str, ...], strength: float, n_donors: int, seed: int
) -> tuple[float, float, float]:
    rng = np.random.default_rng(
        seed + n_donors * 101 + round(strength * 1000) + 10_000 * list(itertools.permutations(NODES)).index(order)
    )
    control = simulate_arm(
        order, strength, n_donors, N_REPLICATES_PER_SEED, rng, intervention=None
    )
    effects = []
    p_values = []
    for source in INTERVENED:
        arm = simulate_arm(
            order, strength, n_donors, N_REPLICATES_PER_SEED, rng, intervention=source
        )
        for target in sorted(NODES):
            if target == source:
                continue
            target_index = NODES.index(target)
            delta = arm[:, :, target_index].mean(axis=1) - control[:, :, target_index].mean(axis=1)
            variance = arm[:, :, target_index].var(axis=1, ddof=1) / n_donors
            variance += control[:, :, target_index].var(axis=1, ddof=1) / n_donors
            z = delta / np.sqrt(np.maximum(variance, 1e-12))
            effects.append(delta)
            p_values.append(normal_two_sided_p(z))
    effect_matrix = np.column_stack(effects)
    p_matrix = np.column_stack(p_values)
    q_matrix = bh_rows(p_matrix)
    signatures = (q_matrix <= FDR) & (effect_matrix >= MIN_EFFECT)

    all_orders = list(itertools.permutations(NODES))
    signature_to_order = {
        response_signature(candidate, INTERVENED): candidate for candidate in all_orders
    }
    true_signature = response_signature(order, INTERVENED)
    recovered = 0
    wrong = 0
    unresolved = 0
    for signature in signatures:
        key = tuple(bool(value) for value in signature)
        inferred = signature_to_order.get(key)
        if inferred == order:
            recovered += 1
        elif inferred is None:
            unresolved += 1
        else:
            wrong += 1
    total = len(signatures)
    assert true_signature in signature_to_order
    return recovered / total, wrong / total, unresolved / total


def power_sweep() -> list[dict[str, Any]]:
    rows = []
    orders = list(itertools.permutations(NODES))
    for strength in STRENGTHS:
        for n_donors in SAMPLE_SIZES:
            order_seed_results = {order: [] for order in orders}
            wrong_results = []
            unresolved_results = []
            for seed in SEEDS:
                for order in orders:
                    recovered, wrong, unresolved = infer_signatures(
                        order, strength, n_donors, seed
                    )
                    order_seed_results[order].append(recovered)
                    wrong_results.append(wrong)
                    unresolved_results.append(unresolved)
            order_means = [float(np.mean(values)) for values in order_seed_results.values()]
            rows.append(
                {
                    "edge_coefficient_assumption": strength,
                    "n_donors_per_arm": n_donors,
                    "arms": "control;do(hla_ii_apc);do(ifn_apc)",
                    "replicates_per_seed_order": N_REPLICATES_PER_SEED,
                    "n_seeds": len(SEEDS),
                    "n_true_orders": len(orders),
                    "mean_exact_order_recovery": float(np.mean(order_means)),
                    "worst_order_recovery": min(order_means),
                    "best_order_recovery": max(order_means),
                    "mean_wrong_order_rate": float(np.mean(wrong_results)),
                    "mean_unresolved_rate": float(np.mean(unresolved_results)),
                    "synthetic_marker": "SYNTHETIC_METHOD_CHARACTERIZATION_NOT_BIOLOGICAL_EVIDENCE",
                }
            )
    return rows


def main() -> int:
    ideal_rows = ideal_identifiability()
    power_rows = power_sweep()
    minimum_n = {}
    for strength in STRENGTHS:
        eligible = [
            int(row["n_donors_per_arm"])
            for row in power_rows
            if row["edge_coefficient_assumption"] == strength
            and row["worst_order_recovery"] >= 0.80
        ]
        minimum_n[str(strength)] = min(eligible) if eligible else None

    synthetic_replicates = (
        len(STRENGTHS)
        * len(SAMPLE_SIZES)
        * len(SEEDS)
        * math.factorial(len(NODES))
        * N_REPLICATES_PER_SEED
    )
    summary = {
        "purpose": "V53 minimal direction-informative APC module intervention design",
        "strict_k3_minimum_perfect_interventions": 2,
        "permissive_k4_minimum_perfect_interventions": 3,
        "minimum_n_per_arm_for_worst_order_recovery_ge_0_80": minimum_n,
        "synthetic_replicates": synthetic_replicates,
        "seeds": list(SEEDS),
        "current_instrument_status": "NO_HELD_PERTURBATION_SATISFIES_PERFECT_MODULE_SELECTIVE_INTERVENTION_ASSUMPTION",
        "verdict": "DESIGN_IDENTIFIABLE_IN_PRINCIPLE_CURRENTLY_BLOCKED_ON_VALID_MODULE_INSTRUMENTS",
        "biological_direction_inferred": False,
    }
    design = {
        "purpose": "Pre-specified acquisition design to orient, not discover, the APC module graph",
        "strict_k3_minimal_arms": [
            "non-targeting/control",
            "one validated selective intervention on hla_ii_apc",
            "one validated selective intervention on ifn_apc",
        ],
        "permissive_k4_addition": "one validated selective intervention on gilt_lysosomal_apc",
        "required_measurements": [
            "all four frozen module scores from donor-level pseudobulk",
            "perturbation efficiency measured independently of module outcomes",
            "at least one early and one later readout to detect violations of endpoint-only DAG assumptions",
        ],
        "primary_analysis": "For each intervention, test every non-intervened module versus control; BH across the fixed reachability family; effect floor 0.25 standardized units; map the binary reachability signature to a topological order.",
        "assumptions_to_validate_before_orientation": [
            "intervention is selective at the module level rather than merely targeting a member gene",
            "relevant effects are nonzero and monotone over the locked readout window",
            "DAG/acyclic approximation is adequate over that window",
            "no unmodeled intervention-dependent batch or donor imbalance",
        ],
        "recommended_nonlinearity_check": "Add the double-intervention arm after the minimal single-intervention design; use it to test interaction/nonadditivity, not to tune the orientation gate.",
        "temporal_fallback": "If module-selective instruments cannot be built, acquire randomized-pulse donor-level trajectories with at least six pre-locked timepoints and analyze under a separately pre-specified dynamic model; current aggregate rows cannot power this route.",
        "current_blocker": "RFX5 is only a nominal HLA-II member-gene proxy, IFNGR/JAK perturbations broadly collapse IFN/APC, and MIF/CD74 has no component-specific validated intervention. None is a valid do(module) instrument.",
        "synthetic_marker": "SYNTHETIC_METHOD_CHARACTERIZATION_NOT_BIOLOGICAL_EVIDENCE",
    }

    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "ideal_identifiability.tsv", ideal_rows)
    write_tsv(OUT / "synthetic_orientation_power_map.tsv", power_rows)
    (OUT / "design_spec.json").write_text(json.dumps(design, indent=2, sort_keys=True) + "\n")
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 Causal-Orientation Acquisition Design",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        "For a complete three-module DAG, one perfect intervention yields only four",
        "distinct reachability signatures for six possible orders; two interventions",
        "distinguish all six. For permissive complete K4, three interventions are minimal",
        "for all 24 orders. This is an exact idealized result under nonzero, acyclic,",
        "module-selective intervention assumptions.",
        "",
        f"The seeded power sweep covers `{synthetic_replicates:,}` synthetic order/design",
        "replicates across three seeds. Minimum donor counts are reported only against",
        "assumed edge coefficients and never as empirical APC effect estimates.",
        f"Worst-order recovery exceeds 80% at `{minimum_n['0.8']}` donors per arm for an",
        f"assumed coefficient of 0.8 and `{minimum_n['0.5']}` for 0.5; coefficient 0.3",
        "does not reach that criterion through 256 donors per arm.",
        "",
        "The design is not executable with current instruments: held RFX5, IFNGR/JAK, and",
        "MIF/CD74 perturbations do not satisfy the perfect selective module-intervention",
        "assumption. The immediate acquisition problem is therefore instrument validation,",
        "not another orientation algorithm on the existing summaries.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
