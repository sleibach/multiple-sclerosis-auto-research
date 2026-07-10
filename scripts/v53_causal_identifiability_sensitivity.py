#!/usr/bin/env python3
"""Stress-test APC causal non-identifiability across skeleton definitions."""

from __future__ import annotations

import csv
import itertools
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v26_deep_structure/workstream_b_module_dependencies.tsv"
OUT = ROOT / "analysis/v53_causal_identifiability_sensitivity"
MODULES = (
    "gilt_lysosomal_apc",
    "hla_ii_apc",
    "ifn_apc",
    "mif_cd74_receptor_state",
)


def read_rows() -> list[dict[str, str]]:
    with INPUT.open() as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def pair(row: dict[str, str]) -> tuple[str, str]:
    return tuple(sorted((row["module_a"], row["module_b"])))


def relevant_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if row["module_a"] in MODULES and row["module_b"] in MODULES
    ]


def q_le(row: dict[str, str], threshold: float = 0.10) -> bool:
    value = row.get("q_bh_within_modality", "")
    return bool(value) and float(value) <= threshold


def skeleton_variants(rows: list[dict[str, str]]) -> dict[str, set[tuple[str, str]]]:
    rows = relevant_rows(rows)
    pairs = sorted({pair(row) for row in rows})
    modalities = sorted({row["modality"] for row in rows})
    variants: dict[str, set[tuple[str, str]]] = {
        "strict_claim_grade_supported": {
            pair(row) for row in rows if row["claim_grade"] == "supported"
        },
        "replicated_modalities_ge_2": {
            edge
            for edge in pairs
            if max(
                int(float(row.get("replicated_significant_modalities") or 0))
                for row in rows
                if pair(row) == edge
            )
            >= 2
        },
        "any_modality_q_le_0_10": {
            edge for edge in pairs if any(q_le(row) for row in rows if pair(row) == edge)
        },
        "at_least_two_modalities_q_le_0_10": {
            edge
            for edge in pairs
            if sum(q_le(row) for row in rows if pair(row) == edge) >= 2
        },
        "perturbation_only_q_le_0_10": {
            pair(row)
            for row in rows
            if row["modality"] == "perturbation_mixscale" and q_le(row)
        },
    }
    for omitted in modalities:
        variants[f"leave_out_{omitted}__at_least_two_q_le_0_10"] = {
            edge
            for edge in pairs
            if sum(
                q_le(row)
                for row in rows
                if pair(row) == edge and row["modality"] != omitted
            )
            >= 2
        }
    return variants


def is_acyclic(edges: list[tuple[str, str]]) -> bool:
    incoming = {node: 0 for node in MODULES}
    outgoing = {node: [] for node in MODULES}
    for source, target in edges:
        incoming[target] += 1
        outgoing[source].append(target)
    queue = [node for node, degree in incoming.items() if degree == 0]
    visited = 0
    while queue:
        node = queue.pop()
        visited += 1
        for target in outgoing[node]:
            incoming[target] -= 1
            if incoming[target] == 0:
                queue.append(target)
    return visited == len(MODULES)


def v_structures(
    skeleton: set[tuple[str, str]], directed: list[tuple[str, str]]
) -> tuple[str, ...]:
    incoming = {node: [] for node in MODULES}
    for source, target in directed:
        incoming[target].append(source)
    result = []
    for collider, parents in incoming.items():
        for left, right in itertools.combinations(sorted(parents), 2):
            if tuple(sorted((left, right))) not in skeleton:
                result.append(f"{left}->{collider}<-{right}")
    return tuple(sorted(result))


def enumerate_variant(name: str, skeleton: set[tuple[str, str]]) -> dict[str, Any]:
    edges = sorted(skeleton)
    dags: list[list[tuple[str, str]]] = []
    equivalence_signatures: set[tuple[str, ...]] = set()
    orientation_counts = {edge: {f"{edge[0]}->{edge[1]}": 0, f"{edge[1]}->{edge[0]}": 0} for edge in edges}
    for bits in itertools.product((0, 1), repeat=len(edges)):
        directed = [
            edge if bit == 0 else (edge[1], edge[0])
            for edge, bit in zip(edges, bits, strict=True)
        ]
        if not is_acyclic(directed):
            continue
        dags.append(directed)
        equivalence_signatures.add(v_structures(skeleton, directed))
        for source, target in directed:
            orientation_counts[tuple(sorted((source, target)))][f"{source}->{target}"] += 1
    consensus = []
    minimum_orientation_fraction = 1.0
    for counts in orientation_counts.values():
        nonzero = [count for count in counts.values() if count > 0]
        if len(nonzero) == 1:
            consensus.append(next(direction for direction, count in counts.items() if count > 0))
        if dags:
            minimum_orientation_fraction = min(
                minimum_orientation_fraction,
                *(count / len(dags) for count in counts.values()),
            )
    return {
        "variant": name,
        "n_edges": len(edges),
        "edges": ";".join(f"{left}--{right}" for left, right in edges) or "none",
        "n_possible_orientations": 2 ** len(edges),
        "n_acyclic_orientations": len(dags),
        "n_markov_equivalence_classes_without_orientation_data": len(equivalence_signatures),
        "n_consensus_oriented_edges": len(consensus),
        "consensus_oriented_edges": ";".join(consensus) or "none",
        "minimum_direction_frequency_across_edges": minimum_orientation_fraction if edges else 0.0,
        "direction_identified": bool(consensus),
    }


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    rows = [enumerate_variant(name, skeleton) for name, skeleton in skeleton_variants(read_rows()).items()]
    rows.sort(key=lambda row: row["variant"])
    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "skeleton_sensitivity.tsv", rows)
    summary = {
        "purpose": "V53 causal-identifiability sensitivity across edge-selection rules",
        "input": str(INPUT.relative_to(ROOT)),
        "modules": list(MODULES),
        "n_skeleton_variants": len(rows),
        "n_variants_with_any_consensus_orientation": sum(
            bool(row["direction_identified"]) for row in rows
        ),
        "edge_count_range": [min(row["n_edges"] for row in rows), max(row["n_edges"] for row in rows)],
        "verdict": "ZERO_EDGE_DIRECTION_SURVIVES_ALL_REASONABLE_SKELETON_DEFINITIONS",
        "interpretation": (
            "The result is structural, not biological: undirected summary dependencies provide "
            "no intervention target direction. Signed correlation is not an arrow."
        ),
        "next_data": (
            "A true module-level intervention or sufficiently sampled temporal design with "
            "pre-specified causal assumptions is required to orient the APC network."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 Causal Identifiability Sensitivity",
        "",
        f"Skeleton variants: `{len(rows)}`.",
        f"Edge-count range: `{summary['edge_count_range'][0]}-{summary['edge_count_range'][1]}`.",
        f"Variants with any consensus-oriented edge: `{summary['n_variants_with_any_consensus_orientation']}`.",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        "This is a methodological boundary. It does not show that the biological network lacks",
        "direction; it shows that the current undirected summary evidence cannot identify it.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
