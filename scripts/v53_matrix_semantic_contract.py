#!/usr/bin/env python3
"""Build and enforce semantic contracts for the V26 summary matrices."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "meta/V26_MATRIX_SEMANTIC_CONTRACT_V53.json"
OUT = ROOT / "analysis/v53_matrix_semantic_contract"


MATRIX_SPECS: dict[str, dict[str, Any]] = {
    "perturbation_module_matrix": {
        "path": "analysis/v26_deep_structure/perturbation_module_matrix.tsv",
        "expected_rows": 24,
        "label_column": "",
        "row_key_columns": [""],
        "row_unit": "one stimulus:gene perturbation aggregate module-effect signature",
        "row_label_semantics": "STIMULUS:PERTURBED_GENE",
        "capabilities": {
            "sample_level": False,
            "patient_level": False,
            "within_subject_longitudinal": False,
            "ordered_timepoints": False,
            "response_group_aggregate": False,
            "matched_rows_across_matrices": False,
            "gene_perturbation_summary": True,
            "causal_intervention_on_modules": False,
            "protein_complex_structure": False,
            "context_level_module_effects": True,
            "pairwise_dependency_summary": False,
        },
        "allowed_uses": [
            "context-level module correlation",
            "single-signature or explicitly model-based additive triage",
            "gene-perturbation effect comparison within stated stimulus",
        ],
        "prohibited_inferences": [
            "temporal ordering or transfer entropy",
            "patient response prediction",
            "biological synergy from additive signature arithmetic",
            "direct module-level causal orientation",
        ],
        "minimum_data_to_unlock": "ordered repeated perturbation measurements or factorial perturbations in matched cells/donors",
    },
    "treatment_pharmacodynamic_module_matrix": {
        "path": "analysis/v26_deep_structure/treatment_pharmacodynamic_module_matrix.tsv",
        "expected_rows": 24,
        "label_column": "",
        "row_key_columns": [""],
        "row_unit": "one dataset/therapy/response-group-or-compartment aggregate effect",
        "row_label_semantics": "DATASET|THERAPY|GROUP_OR_COMPARTMENT_METADATA",
        "capabilities": {
            "sample_level": False,
            "patient_level": False,
            "within_subject_longitudinal": False,
            "ordered_timepoints": False,
            "response_group_aggregate": True,
            "matched_rows_across_matrices": False,
            "gene_perturbation_summary": False,
            "causal_intervention_on_modules": False,
            "protein_complex_structure": False,
            "context_level_module_effects": True,
            "pairwise_dependency_summary": False,
        },
        "allowed_uses": [
            "aggregate response-group effect comparison within exact dataset/therapy pairs",
            "cross-context module association with context-level nulls",
            "bounded source-target transfer diagnostics labeled as aggregate",
        ],
        "prohibited_inferences": [
            "patient-level classification or confidence intervals",
            "within-subject trajectory or hysteresis",
            "mutual-information change within response groups",
            "causal DAG estimation",
        ],
        "minimum_data_to_unlock": "sample-level paired baseline/on-treatment rows with subject, time, and response identifiers",
    },
    "treatment_response_module_matrix": {
        "path": "analysis/v26_deep_structure/treatment_response_module_matrix.tsv",
        "expected_rows": 20,
        "label_column": "row",
        "row_key_columns": ["row"],
        "row_unit": "one dataset/compartment/time-or-contrast aggregate response statistic",
        "row_label_semantics": "DATASET|COMPARTMENT|TIME_OR_DELTA|CONTRAST_OR_STATISTIC",
        "capabilities": {
            "sample_level": False,
            "patient_level": False,
            "within_subject_longitudinal": False,
            "ordered_timepoints": False,
            "response_group_aggregate": True,
            "matched_rows_across_matrices": False,
            "gene_perturbation_summary": False,
            "causal_intervention_on_modules": False,
            "protein_complex_structure": False,
            "context_level_module_effects": True,
            "pairwise_dependency_summary": False,
        },
        "allowed_uses": [
            "aggregate contrast comparison",
            "context-level module association",
            "meta-analysis that preserves contrast identity",
        ],
        "prohibited_inferences": [
            "patient-level machine learning",
            "joint baseline/on-treatment mutual information",
            "within-person state transition",
            "cross-matrix row joins without an explicit verified key",
        ],
        "minimum_data_to_unlock": "underlying sample-level scores with subject, timepoint, response, and cohort keys",
    },
    "cell_state_module_matrix": {
        "path": "analysis/v26_deep_structure/cell_state_module_matrix.tsv",
        "expected_rows": 12,
        "label_column": "",
        "row_key_columns": [""],
        "row_unit": "one disease/tissue-compartment aggregate cell-state effect",
        "row_label_semantics": "SOURCE_CONTEXT|DISEASE|COMPARTMENT",
        "capabilities": {
            "sample_level": False,
            "patient_level": False,
            "within_subject_longitudinal": False,
            "ordered_timepoints": False,
            "response_group_aggregate": False,
            "matched_rows_across_matrices": False,
            "gene_perturbation_summary": False,
            "causal_intervention_on_modules": False,
            "protein_complex_structure": False,
            "context_level_module_effects": True,
            "pairwise_dependency_summary": False,
        },
        "allowed_uses": [
            "disease/compartment-level module comparison",
            "context-level dependency analysis",
        ],
        "prohibited_inferences": [
            "sample-distribution bimodality",
            "cellular bistability",
            "patient subgroup covariance",
            "treatment trajectory",
        ],
        "minimum_data_to_unlock": "sample- or cell-level module scores with donor and condition identifiers",
    },
    "cross_disease_summary_module_matrix": {
        "path": "analysis/v26_deep_structure/cross_disease_summary_module_matrix.tsv",
        "expected_rows": 6,
        "label_column": "",
        "row_key_columns": [""],
        "row_unit": "one aggregate statistic across diseases",
        "row_label_semantics": "SUMMARY_STATISTIC_NAME",
        "capabilities": {
            "sample_level": False,
            "patient_level": False,
            "within_subject_longitudinal": False,
            "ordered_timepoints": False,
            "response_group_aggregate": False,
            "matched_rows_across_matrices": False,
            "gene_perturbation_summary": False,
            "causal_intervention_on_modules": False,
            "protein_complex_structure": False,
            "context_level_module_effects": False,
            "pairwise_dependency_summary": False,
        },
        "allowed_uses": [
            "module-level summary ranking with statistic identity preserved",
            "descriptive cross-disease breadth accounting",
        ],
        "prohibited_inferences": [
            "disease-level counterfactual prediction",
            "row-wise joining to treatment contexts",
            "causal or patient-level analysis",
        ],
        "minimum_data_to_unlock": "disease-by-module effect matrix with harmonized disease rows and uncertainty",
    },
    "workstream_b_module_dependencies": {
        "path": "analysis/v26_deep_structure/workstream_b_module_dependencies.tsv",
        "expected_rows": 100,
        "label_column": "modality",
        "row_key_columns": ["modality", "module_a", "module_b"],
        "row_unit": "one modality/module-pair association test summary",
        "row_label_semantics": "MODALITY + MODULE_A + MODULE_B",
        "capabilities": {
            "sample_level": False,
            "patient_level": False,
            "within_subject_longitudinal": False,
            "ordered_timepoints": False,
            "response_group_aggregate": False,
            "matched_rows_across_matrices": False,
            "gene_perturbation_summary": False,
            "causal_intervention_on_modules": False,
            "protein_complex_structure": False,
            "context_level_module_effects": False,
            "pairwise_dependency_summary": True,
        },
        "allowed_uses": [
            "undirected dependency topology",
            "replication and negative-space assessment with missingness preserved",
            "causal identifiability bounds",
        ],
        "prohibited_inferences": [
            "edge direction from correlation sign",
            "PC/GES on association-summary rows as if they were samples",
            "module intervention effect",
        ],
        "minimum_data_to_unlock": "sample-level joint module matrix or true intervention/temporal data with pre-specified causal assumptions",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    audit = sub.add_parser("audit")
    audit.add_argument("--fail-on-error", action="store_true")
    check = sub.add_parser("check-requirements")
    check.add_argument("--requirements-file", type=Path, required=True)
    check.add_argument("--output", type=Path)
    check.add_argument("--fail-on-error", action="store_true")
    synthetic = sub.add_parser("synthetic-check")
    synthetic.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_header_and_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open() as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def build_contract() -> dict[str, Any]:
    matrices = {}
    for name, spec in MATRIX_SPECS.items():
        path = ROOT / spec["path"]
        header, rows = read_header_and_rows(path)
        matrices[name] = {
            **spec,
            "observed_columns": header,
            "content_sha256": sha256(path),
            "contract_status": "frozen_semantics_for_v53_downstream_use",
        }
    contract = {
        "purpose": "Machine-readable semantic boundary for V26 summary matrices",
        "version": "V53-1",
        "date_frozen": "2026-07-10",
        "global_rules": [
            "A row is never treated as a patient, sample, cell, or timepoint unless its matrix capability says so.",
            "Missing cross-matrix keys are not inferred from similar labels.",
            "Aggregate response labels do not license patient-level prediction.",
            "Correlation sign does not orient a causal edge.",
        ],
        "matrices": matrices,
    }
    CONTRACT_PATH.write_text(json.dumps(contract, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "contract": str(CONTRACT_PATH.relative_to(ROOT)), "matrices": len(matrices)}, indent=2))
    return contract


def load_contract() -> dict[str, Any]:
    if not CONTRACT_PATH.exists():
        raise RuntimeError(f"Contract missing: {CONTRACT_PATH}")
    return json.loads(CONTRACT_PATH.read_text())


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def audit_contract(contract: dict[str, Any], fail_on_error: bool) -> int:
    checks: list[dict[str, Any]] = []
    for name, spec in contract["matrices"].items():
        path = ROOT / spec["path"]
        header, rows = read_header_and_rows(path)
        label_column = spec["label_column"]
        labels = [row.get(label_column, "") for row in rows]
        row_key_columns = list(spec["row_key_columns"])
        row_keys = [tuple(row.get(column, "") for column in row_key_columns) for row in rows]
        matrix_checks = {
            "file_exists": path.exists(),
            "row_count_matches": len(rows) == int(spec["expected_rows"]),
            "columns_match": header == spec["observed_columns"],
            "content_hash_matches": sha256(path) == spec["content_sha256"],
            "label_column_present": label_column in header,
            "labels_nonempty": all(bool(label) for label in labels),
            "row_key_columns_present": all(column in header for column in row_key_columns),
            "row_keys_nonempty": all(all(bool(value) for value in key) for key in row_keys),
            "row_keys_unique": len(row_keys) == len(set(row_keys)),
            "capabilities_present": bool(spec.get("capabilities")),
            "allowed_uses_present": bool(spec.get("allowed_uses")),
            "prohibited_inferences_present": bool(spec.get("prohibited_inferences")),
        }
        for check, passed in matrix_checks.items():
            checks.append({"matrix": name, "check": check, "status": "PASS" if passed else "FAIL"})
    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "contract_audit.tsv", checks)
    failures = sum(row["status"] == "FAIL" for row in checks)
    summary = {
        "purpose": "V53 V26 matrix semantic-contract audit",
        "n_matrices": len(contract["matrices"]),
        "n_checks": len(checks),
        "n_fail": failures,
        "overall_status": "PASS" if failures == 0 else "FAIL",
    }
    (OUT / "contract_audit_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if fail_on_error and failures:
        return 1
    return 0


def check_requirements(
    contract: dict[str, Any], requests: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], int]:
    rows = []
    for request in requests:
        matrix = request["matrix"]
        capabilities = contract["matrices"][matrix]["capabilities"]
        required = list(request.get("requires", []))
        missing = [capability for capability in required if not capabilities.get(capability, False)]
        rows.append(
            {
                "request_id": request["request_id"],
                "matrix": matrix,
                "required_capabilities": ";".join(required) or "none",
                "missing_capabilities": ";".join(missing) or "none",
                "status": "PASS" if not missing else "FAIL",
            }
        )
    return rows, sum(row["status"] == "FAIL" for row in rows)


def synthetic_check(fail_on_error: bool) -> int:
    contract = load_contract()
    requests = [
        {
            "request_id": "valid_context_perturbation",
            "matrix": "perturbation_module_matrix",
            "requires": ["context_level_module_effects", "gene_perturbation_summary"],
        },
        {
            "request_id": "invalid_patient_temporal_mi",
            "matrix": "treatment_pharmacodynamic_module_matrix",
            "requires": ["patient_level", "ordered_timepoints"],
        },
    ]
    rows, failures = check_requirements(contract, requests)
    expected = {"valid_context_perturbation": "PASS", "invalid_patient_temporal_mi": "FAIL"}
    expectation_failures = sum(row["status"] != expected[row["request_id"]] for row in rows)
    write_tsv(OUT / "synthetic_requirement_checks.tsv", rows)
    summary = {
        "purpose": "V53 matrix semantic-contract synthetic check",
        "requests": len(rows),
        "observed_requirement_failures": failures,
        "expectation_failures": expectation_failures,
        "overall_status": "PASS" if expectation_failures == 0 else "FAIL",
    }
    (OUT / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if fail_on_error and expectation_failures else 0


def main() -> int:
    args = parse_args()
    if args.command == "build":
        build_contract()
        return 0
    if args.command == "audit":
        return audit_contract(load_contract(), args.fail_on_error)
    if args.command == "check-requirements":
        requests = json.loads(args.requirements_file.read_text())
        rows, failures = check_requirements(load_contract(), requests)
        if args.output:
            write_tsv(args.output, rows)
            summary_path = args.output.with_name(f"{args.output.stem}_summary.json")
            summary_path.write_text(
                json.dumps(
                    {
                        "n_requests": len(rows),
                        "n_pass": len(rows) - failures,
                        "n_fail": failures,
                        "overall_status": "PASS" if failures == 0 else "BOUNDED",
                        "interpretation": "FAIL means the requested analysis exceeds the frozen matrix semantics, not that its biological hypothesis is false.",
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n"
            )
        print(json.dumps(rows, indent=2))
        return 1 if args.fail_on_error and failures else 0
    if args.command == "synthetic-check":
        return synthetic_check(args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
