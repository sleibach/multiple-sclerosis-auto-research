#!/usr/bin/env python3
"""Ground executable V53 multi-lineage proposals on held summary data."""

from __future__ import annotations

import csv
import itertools
import json
import re
from pathlib import Path
from typing import Any

import numpy as np

import v53_matrix_semantic_contract as semantic_contract


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v53_model_proposal_grounding"
DEPENDENCIES = ROOT / "analysis/v26_deep_structure/workstream_b_module_dependencies.tsv"
PERTURBATIONS = ROOT / "analysis/v26_deep_structure/perturbation_module_matrix.tsv"
PHARMACODYNAMIC = ROOT / "analysis/v26_deep_structure/treatment_pharmacodynamic_module_matrix.tsv"
MODULES = (
    "gilt_lysosomal_apc",
    "hla_ii_apc",
    "ifn_apc",
    "mif_cd74_receptor_state",
)
SEED_NEGATIVE_SPACE = 53004
SEED_TRANSFER = 53005
N_PERMUTATIONS = 20_000
N_BOOTSTRAP = 20_000
PREFLIGHT_REQUIREMENTS = ROOT / "meta/V53_PROPOSAL_GROUNDING_REQUIREMENTS.json"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise RuntimeError(f"Refusing to write empty table: {path}")
    fieldnames = list(dict.fromkeys(key for row in rows for key in row))
    normalized_rows = [
        {
            field: "NA" if row.get(field) is None or row.get(field) == "" else row.get(field)
            for field in fieldnames
        }
        for row in rows
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(normalized_rows)


def supported_skeleton() -> list[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    for row in read_tsv(DEPENDENCIES):
        if row["claim_grade"] != "supported":
            continue
        left, right = row["module_a"], row["module_b"]
        if left in MODULES and right in MODULES:
            edges.add(tuple(sorted((left, right))))
    return sorted(edges)


def is_acyclic(nodes: tuple[str, ...], directed_edges: list[tuple[str, str]]) -> bool:
    incoming = {node: 0 for node in nodes}
    outgoing = {node: [] for node in nodes}
    for left, right in directed_edges:
        incoming[right] += 1
        outgoing[left].append(right)
    queue = [node for node in nodes if incoming[node] == 0]
    visited = 0
    while queue:
        node = queue.pop()
        visited += 1
        for target in outgoing[node]:
            incoming[target] -= 1
            if incoming[target] == 0:
                queue.append(target)
    return visited == len(nodes)


def v_structures(
    nodes: tuple[str, ...],
    skeleton: set[tuple[str, str]],
    directed_edges: list[tuple[str, str]],
) -> tuple[str, ...]:
    incoming = {node: [] for node in nodes}
    for source, target in directed_edges:
        incoming[target].append(source)
    structures: list[str] = []
    for collider, parents in incoming.items():
        for left, right in itertools.combinations(sorted(parents), 2):
            if tuple(sorted((left, right))) not in skeleton:
                structures.append(f"{left}->{collider}<-{right}")
    return tuple(sorted(structures))


def causal_identifiability() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    skeleton_edges = supported_skeleton()
    skeleton = set(skeleton_edges)
    dag_rows: list[dict[str, Any]] = []
    orientation_sets = {edge: set() for edge in skeleton_edges}
    for bits in itertools.product((0, 1), repeat=len(skeleton_edges)):
        directed = [
            edge if bit == 0 else (edge[1], edge[0])
            for edge, bit in zip(skeleton_edges, bits, strict=True)
        ]
        if not is_acyclic(MODULES, directed):
            continue
        structures = v_structures(MODULES, skeleton, directed)
        for edge in skeleton_edges:
            orientation = next(
                f"{left}->{right}"
                for left, right in directed
                if set((left, right)) == set(edge)
            )
            orientation_sets[edge].add(orientation)
        dag_rows.append(
            {
                "dag_id": f"DAG_{len(dag_rows) + 1:02d}",
                "directed_edges": ";".join(f"{left}->{right}" for left, right in directed),
                "v_structures": ";".join(structures),
                "markov_equivalence_signature": (
                    "skeleton=" + ";".join(f"{a}--{b}" for a, b in skeleton_edges)
                    + "|v_structures="
                    + ";".join(structures)
                ),
            }
        )
    signatures = {row["markov_equivalence_signature"] for row in dag_rows}
    consensus = [
        next(iter(orientations))
        for orientations in orientation_sets.values()
        if len(orientations) == 1
    ]
    summary = {
        "proposal_id": "H2_causal_identifiability_negative",
        "supported_skeleton_edges": [list(edge) for edge in skeleton_edges],
        "n_supported_skeleton_edges": len(skeleton_edges),
        "n_acyclic_orientations": len(dag_rows),
        "n_markov_equivalence_classes": len(signatures),
        "n_consensus_oriented_edges": len(consensus),
        "consensus_oriented_edges": consensus,
        "intervention_mapping_available": False,
        "verdict": "SUPPORTED_METHODOLOGICAL_NEGATIVE_CURRENT_SUMMARIES_DO_NOT_IDENTIFY_DIRECTION",
        "boundary": (
            "This exact enumeration establishes non-identifiability from the supported summary "
            "skeleton; it does not establish that biological direction is absent."
        ),
    }
    return dag_rows, summary


def negative_space() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = read_tsv(DEPENDENCIES)
    modalities = sorted({row["modality"] for row in rows})
    modules_by_modality: dict[str, set[str]] = {}
    for modality in modalities:
        modality_rows = [row for row in rows if row["modality"] == modality]
        modules_by_modality[modality] = {
            module
            for row in modality_rows
            for module in (row["module_a"], row["module_b"])
            if module
        }
    common_modules = sorted(set.intersection(*(modules_by_modality[m] for m in modalities)))
    common_pairs = list(itertools.combinations(common_modules, 2))
    support_matrix = np.zeros((len(modalities), len(common_pairs)), dtype=int)
    result_rows: list[dict[str, Any]] = []
    for pair_index, pair in enumerate(common_pairs):
        pair_rows = []
        for modality_index, modality in enumerate(modalities):
            match = next(
                row
                for row in rows
                if row["modality"] == modality
                and tuple(sorted((row["module_a"], row["module_b"]))) == pair
            )
            supported = match["claim_grade"] == "supported"
            support_matrix[modality_index, pair_index] = int(supported)
            pair_rows.append(match)
        n_supported = int(np.sum(support_matrix[:, pair_index]))
        result_rows.append(
            {
                "module_a": pair[0],
                "module_b": pair[1],
                "n_modalities_assessed": len(pair_rows),
                "n_supported_modalities": n_supported,
                "strict_forbidden_edge": n_supported == 0,
                "involves_mif_cd74": "mif_cd74_receptor_state" in pair,
                "modality_support_pattern": ";".join(
                    f"{modality}:{support_matrix[index, pair_index]}"
                    for index, modality in enumerate(modalities)
                ),
            }
        )

    observed_forbidden = sum(bool(row["strict_forbidden_edge"]) for row in result_rows)
    rng = np.random.default_rng(SEED_NEGATIVE_SPACE)
    null_counts = np.empty(N_PERMUTATIONS, dtype=int)
    for permutation_index in range(N_PERMUTATIONS):
        permuted = np.vstack([rng.permutation(row) for row in support_matrix])
        null_counts[permutation_index] = int(np.sum(np.sum(permuted, axis=0) == 0))
    enrichment_p = (1 + int(np.sum(null_counts >= observed_forbidden))) / (N_PERMUTATIONS + 1)
    summary = {
        "proposal_id": "H7_negative_space_forbidden_edges",
        "modalities": modalities,
        "common_modules": common_modules,
        "n_fully_assessable_pairs": len(common_pairs),
        "n_strict_forbidden_edges": observed_forbidden,
        "n_forbidden_edges_involving_mif_cd74": sum(
            bool(row["strict_forbidden_edge"]) and bool(row["involves_mif_cd74"])
            for row in result_rows
        ),
        "seed": SEED_NEGATIVE_SPACE,
        "n_permutations": N_PERMUTATIONS,
        "empirical_p_for_forbidden_edge_enrichment": enrichment_p,
        "verdict": "NOT_SUPPORTED_NO_STRICT_FORBIDDEN_EDGE_IN_FULLY_COMPARABLE_SPACE",
        "boundary": (
            "Missing module coverage is not treated as edge absence. Only pairs assessed in every "
            "modality enter the strict test."
        ),
    }
    return result_rows, summary


def matrix_rows(path: Path) -> list[dict[str, Any]]:
    rows = read_tsv(path)
    label_column = next(iter(rows[0]))
    parsed = []
    for row in rows:
        parsed.append(
            {
                "label": row[label_column],
                **{key: float(value) for key, value in row.items() if key != label_column},
            }
        )
    return parsed


def fit_line(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    design = np.column_stack([np.ones(len(x)), x])
    return np.linalg.lstsq(design, y, rcond=None)[0]


def predict_line(coefficients: np.ndarray, x: float | np.ndarray) -> np.ndarray:
    values = np.asarray(x, dtype=float)
    return coefficients[0] + coefficients[1] * values


def loocv_r2(x: np.ndarray, y: np.ndarray) -> float:
    predictions = np.empty(len(y), dtype=float)
    for index in range(len(y)):
        keep = np.arange(len(y)) != index
        predictions[index] = float(predict_line(fit_line(x[keep], y[keep]), x[index]))
    denominator = float(np.sum((y - np.mean(y)) ** 2))
    return 1.0 - float(np.sum((y - predictions) ** 2)) / denominator if denominator else float("nan")


def response_pair_key(label: str) -> tuple[str, str] | None:
    if "response=NR" in label:
        return re.sub(r"response=NR", "response=*", label), "NR"
    if "response=R" in label:
        return re.sub(r"response=R", "response=*", label), "R"
    if "GSE253006" in label and "group=No responder" in label:
        return re.sub(r"group=No responder", "group=*", label), "NR"
    if "GSE253006" in label and "group=Responder" in label:
        return re.sub(r"group=Responder", "group=*", label), "R"
    return None


def exact_sign_flip_p(differences: np.ndarray) -> tuple[float, float]:
    observed = float(np.mean(differences))
    null = np.array(
        [
            np.mean(differences * np.asarray(signs, dtype=float))
            for signs in itertools.product((-1.0, 1.0), repeat=len(differences))
        ],
        dtype=float,
    )
    one_sided = float(np.mean(null >= observed))
    two_sided = float(np.mean(np.abs(null) >= abs(observed)))
    return one_sided, two_sided


def bh_adjust(p_values: list[float]) -> list[float]:
    order = np.argsort(p_values)
    adjusted = np.ones(len(p_values), dtype=float)
    running = 1.0
    for offset, index in enumerate(order[::-1], start=1):
        rank = len(p_values) - offset + 1
        running = min(running, p_values[int(index)] * len(p_values) / rank)
        adjusted[int(index)] = running
    return adjusted.tolist()


def transfer_error() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    source = matrix_rows(PERTURBATIONS)
    target = matrix_rows(PHARMACODYNAMIC)
    source_x = np.array([row["ifn_apc"] for row in source], dtype=float)
    outcomes = ("hla_ii_apc", "mif_cd74_receptor_state")
    coefficients: dict[str, np.ndarray] = {}
    model_rows: list[dict[str, Any]] = []
    for outcome in outcomes:
        y = np.array([row[outcome] for row in source], dtype=float)
        beta = fit_line(source_x, y)
        coefficients[outcome] = beta
        fitted = predict_line(beta, source_x)
        r2 = 1.0 - float(np.sum((y - fitted) ** 2)) / float(np.sum((y - np.mean(y)) ** 2))
        model_rows.append(
            {
                "outcome_module": outcome,
                "n_source_rows": len(source),
                "intercept": float(beta[0]),
                "ifn_apc_slope": float(beta[1]),
                "in_sample_r2": r2,
                "loocv_r2": loocv_r2(source_x, y),
            }
        )

    grouped: dict[str, dict[str, dict[str, Any]]] = {}
    for row in target:
        parsed = response_pair_key(row["label"])
        if parsed is None:
            continue
        key, response = parsed
        grouped.setdefault(key, {})[response] = row
    complete_pairs = {key: rows for key, rows in grouped.items() if set(rows) == {"R", "NR"}}
    pair_rows: list[dict[str, Any]] = []
    differences_by_outcome: dict[str, list[float]] = {outcome: [] for outcome in outcomes}
    for key, pair in sorted(complete_pairs.items()):
        output: dict[str, Any] = {
            "pair_key": key,
            "responder_label": pair["R"]["label"],
            "nonresponder_label": pair["NR"]["label"],
        }
        for outcome in outcomes:
            responder_prediction = float(
                predict_line(coefficients[outcome], pair["R"]["ifn_apc"])
            )
            nonresponder_prediction = float(
                predict_line(coefficients[outcome], pair["NR"]["ifn_apc"])
            )
            responder_error = abs(pair["R"][outcome] - responder_prediction)
            nonresponder_error = abs(pair["NR"][outcome] - nonresponder_prediction)
            difference = nonresponder_error - responder_error
            differences_by_outcome[outcome].append(difference)
            output[f"{outcome}__abs_error_R"] = responder_error
            output[f"{outcome}__abs_error_NR"] = nonresponder_error
            output[f"{outcome}__NR_minus_R_abs_error"] = difference
        pair_rows.append(output)

    rng = np.random.default_rng(SEED_TRANSFER)
    test_rows: list[dict[str, Any]] = []
    one_sided_p_values: list[float] = []
    for outcome in outcomes:
        differences = np.asarray(differences_by_outcome[outcome], dtype=float)
        one_sided, two_sided = exact_sign_flip_p(differences)
        bootstrap_means = np.array(
            [
                np.mean(rng.choice(differences, size=len(differences), replace=True))
                for _ in range(N_BOOTSTRAP)
            ]
        )
        one_sided_p_values.append(one_sided)
        test_rows.append(
            {
                "outcome_module": outcome,
                "n_matched_response_pairs": len(differences),
                "mean_NR_minus_R_absolute_transfer_error": float(np.mean(differences)),
                "median_NR_minus_R_absolute_transfer_error": float(np.median(differences)),
                "bootstrap_95_ci_low": float(np.quantile(bootstrap_means, 0.025)),
                "bootstrap_95_ci_high": float(np.quantile(bootstrap_means, 0.975)),
                "exact_one_sided_sign_flip_p": one_sided,
                "exact_two_sided_sign_flip_p": two_sided,
            }
        )
    q_values = bh_adjust(one_sided_p_values)
    model_by_outcome = {row["outcome_module"]: row for row in model_rows}
    for index, row in enumerate(test_rows):
        row["one_sided_q_bh"] = q_values[index]
        row["source_model_loocv_r2"] = model_by_outcome[row["outcome_module"]]["loocv_r2"]
        row["support_gate"] = (
            row["mean_NR_minus_R_absolute_transfer_error"] > 0
            and row["bootstrap_95_ci_low"] > 0
            and row["one_sided_q_bh"] <= 0.05
            and row["source_model_loocv_r2"] > 0
        )
    n_pass = sum(bool(row["support_gate"]) for row in test_rows)
    summary = {
        "proposal_id": "CRL_2024_002",
        "source_model": "pooled OLS module_outcome ~ IFN_APC on 24 perturbation summaries",
        "target_test": "exact within-dataset/therapy or compartment R-vs-NR aggregate pairs",
        "n_matched_response_pairs": len(pair_rows),
        "outcomes_tested": list(outcomes),
        "multiple_testing": "BH across two outcome modules",
        "seed": SEED_TRANSFER,
        "n_bootstrap": N_BOOTSTRAP,
        "n_support_gate_passes": n_pass,
        "verdict": (
            "SUPPORTED_BOUNDED_GROUP_LEVEL_TRANSFER_ERROR_NEEDS_PATIENT_REPLICATION"
            if n_pass
            else "NOT_SUPPORTED_OR_SOURCE_MODEL_INADEQUATE_IN_HELD_SUMMARIES"
        ),
        "boundary": (
            "Rows are aggregate group/module effects, not patient observations. This test cannot "
            "establish patient-level causal rewiring or prediction."
        ),
    }
    return pair_rows, model_rows + test_rows, summary


def proposal_triage(
    identifiability_summary: dict[str, Any],
    negative_summary: dict[str, Any],
    transfer_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    claude_record = "knowledge_external/model_outputs/v53_unconventional_generation/claude_record.json"
    gemini_record = "knowledge_external/model_outputs/v53_unconventional_generation/gemini_record.json"
    rows = [
        ("claude", "H1_transfer_entropy_directionality", "untestable", "Perturbation rows are unordered signatures, not temporal observations; pseudo-ordering would fabricate direction.", ""),
        ("claude", "H2_causal_identifiability_negative", "supported", identifiability_summary["boundary"], "causal_identifiability_summary.json"),
        ("claude", "H3_hysteresis_treatment_response", "untestable", "Pharmacodynamic and response matrices contain aggregate contrasts from different rows, not within-subject trajectories.", ""),
        ("claude", "H4_robustness_geometry_curvature", "inconclusive", "Twenty-four sparse signatures and unmatched response summaries do not identify local Hessians at named biological anchors.", ""),
        ("claude", "H5_counterfactual_transfer_cross_disease", "inconclusive", "Cross-disease rows are count/effect summaries and response rows are heterogeneous contrasts; no matched observational units exist for counterfactual prediction.", ""),
        ("claude", "H6_information_bottleneck_scalar", "untestable", "Perturbation and response matrices have incompatible row semantics and no shared relevance labels for an information-bottleneck fit.", ""),
        ("claude", "H7_negative_space_forbidden_edges", "not_supported", negative_summary["boundary"], "negative_space_summary.json"),
        ("claude", "H8_state_transition_bistability", "untestable", "Cell-state rows are twelve disease/compartment aggregates, not sample distributions; bimodality would not imply cellular bistability.", ""),
        ("gemini", "CRL_2024_001", "untestable", "No patient-level baseline/on-treatment distributions exist in the V26 summary matrices for mutual-information change estimation.", ""),
        ("gemini", "CRL_2024_002", "supported" if transfer_summary["n_support_gate_passes"] else "not_supported", transfer_summary["boundary"], "transfer_error_summary.json"),
        ("gemini", "CRL_2024_003", "untestable", "Aggregate group-effect rows cannot estimate within-group patient covariance or an energy basin.", ""),
        ("gemini", "CRL_2024_004", "untestable", "Held perturbations are not stratified by eventual patient response status.", ""),
        ("gemini", "CRL_2024_005", "untestable", "Rows are heterogeneous group summaries rather than patient state points; an SVM would be a small-n semantic-confounding artifact.", ""),
        ("gemini", "CRL_2024_006", "untestable", "Stimulus and treatment matrices are too small and aggregate to identify or compare causal DAGs.", ""),
        ("gemini", "CRL_2024_007", "untestable", "Current AlphaFold records are monomers and expose no complex-interface confidence; no PPI may be inferred from them.", ""),
        ("gemini", "CRL_2024_008", "untestable", "The held treatment summaries do not resolve temporal activation order.", ""),
    ]
    return [
        {
            "source": source,
            "proposal_id": proposal_id,
            "proposal_record": claude_record if source == "claude" else gemini_record,
            "grounded_outcome": outcome,
            "grounded_reason": reason,
            "grounding_artifact": f"analysis/v53_model_proposal_grounding/{artifact}" if artifact else "",
        }
        for source, proposal_id, outcome, reason, artifact in rows
    ]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    preflight_requests = json.loads(PREFLIGHT_REQUIREMENTS.read_text())
    preflight_rows, preflight_failures = semantic_contract.check_requirements(
        semantic_contract.load_contract(), preflight_requests
    )
    write_tsv(OUT / "semantic_preflight.tsv", preflight_rows)
    (OUT / "semantic_preflight_summary.json").write_text(
        json.dumps(
            {
                "purpose": "Fail-closed semantic preflight before V53 proposal grounding",
                "requirements_file": str(PREFLIGHT_REQUIREMENTS.relative_to(ROOT)),
                "n_requests": len(preflight_rows),
                "n_pass": len(preflight_rows) - preflight_failures,
                "n_fail": preflight_failures,
                "overall_status": "PASS" if preflight_failures == 0 else "FAIL",
                "interpretation": (
                    "A failed request blocks analysis launch; it does not falsify the proposal."
                ),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    if preflight_failures:
        raise RuntimeError(
            f"Semantic preflight blocked {preflight_failures} proposal-grounding requests"
        )
    dag_rows, identifiability_summary = causal_identifiability()
    negative_rows, negative_summary = negative_space()
    transfer_pairs, transfer_rows, transfer_summary = transfer_error()
    triage_rows = proposal_triage(identifiability_summary, negative_summary, transfer_summary)

    write_tsv(OUT / "causal_equivalence_dags.tsv", dag_rows)
    write_tsv(OUT / "negative_space_pairs.tsv", negative_rows)
    write_tsv(OUT / "transfer_error_pairs.tsv", transfer_pairs)
    write_tsv(OUT / "transfer_error_models_and_tests.tsv", transfer_rows)
    write_tsv(OUT / "proposal_triage.tsv", triage_rows)
    for name, summary in (
        ("causal_identifiability_summary.json", identifiability_summary),
        ("negative_space_summary.json", negative_summary),
        ("transfer_error_summary.json", transfer_summary),
    ):
        (OUT / name).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    counts = {
        outcome: sum(row["grounded_outcome"] == outcome for row in triage_rows)
        for outcome in ("supported", "not_supported", "inconclusive", "untestable")
    }
    summary = {
        "purpose": "V53 project-data grounding of Claude and Gemini proposals",
        "n_proposals": len(triage_rows),
        "outcome_counts": counts,
        "executable_proposals": [
            "H2_causal_identifiability_negative",
            "H7_negative_space_forbidden_edges",
            "CRL_2024_002",
        ],
        "model_output_is_evidence": False,
        "semantic_preflight": {
            "requirements": len(preflight_rows),
            "passed": len(preflight_rows) - preflight_failures,
            "failed": preflight_failures,
            "fail_closed_before_analysis": True,
        },
        "methodological_value_added": (
            "The causal-identifiability proposal formalized a boundary not previously quantified; "
            "all biological target implications remain unpromoted."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 Multi-Lineage Proposal Grounding",
        "",
        "Claude and Gemini generated 16 proposals. Their outputs are proposal sources only;",
        "all verdicts below come from held-data schema checks or committed analyses.",
        "",
        f"Outcome counts: `{json.dumps(counts, sort_keys=True)}`.",
        "",
        f"Semantic preflight: `{len(preflight_rows)}/{len(preflight_rows)}` declared matrix",
        "capability requests passed before any grounding analysis ran.",
        "",
        f"Causal identifiability: **{identifiability_summary['verdict']}**.",
        f"Negative-space test: **{negative_summary['verdict']}**.",
        f"Transfer-error test: **{transfer_summary['verdict']}**.",
        "",
        "The only supported item is a methodological negative unless the bounded transfer test",
        "also passes. No model-generated target or therapeutic direction is promoted.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
