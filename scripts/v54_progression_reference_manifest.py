#!/usr/bin/env python3
"""Write or verify the hash-bound V54 progression reference manifest."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_reference_manifest"
MANIFEST = OUT / "manifest.json"
FROZEN_AT = "2026-07-22T01:13:18Z"
SOURCES = (
    "analysis/v54_progression_design_synthesis/summary.json",
    "analysis/v54_progression_design_synthesis/prospective_design_requirements.tsv",
    "docs/validation/PROGRESSION_COMBINED_INTAKE_GATE_V54.md",
    "docs/validation/PROGRESSION_EVENT_TIME_ASSUMPTION_GATE_V54.md",
    "docs/validation/PROGRESSION_SITE_SCORE_CALIBRATION_GATE_V54.md",
    "docs/validation/PROGRESSION_TREATMENT_SWITCH_GATE_V54.md",
    "docs/validation/PROGRESSION_NONLINEAR_DIAGNOSTIC_GATE_V54.md",
    "docs/validation/PROGRESSION_BLINDED_FEASIBILITY_CALCULATOR_V54.md",
    "docs/validation/PROGRESSION_BLINDED_INFORMATION_MONITOR_V54.md",
    "docs/validation/PROGRESSION_P1_INTAKE_TO_LOCK_V54.md",
    "scripts/v54_progression_combined_intake_gate.py",
    "scripts/v54_progression_event_time_assumption_gate.py",
    "scripts/v54_progression_site_score_calibration_gate.py",
    "scripts/v54_progression_treatment_switch_gate.py",
    "scripts/v54_progression_nonlinear_diagnostic_gate.py",
    "scripts/v54_progression_blinded_feasibility.py",
    "scripts/v54_progression_information_monitor.py",
    "scripts/v54_progression_p1_intake_to_lock.py",
)


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical(document: Any) -> bytes:
    return json.dumps(document, sort_keys=True, separators=(",", ":")).encode()


def source_records() -> list[dict[str, Any]]:
    records = []
    for relative in SOURCES:
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"Manifest source missing: {relative}")
        records.append(
            {
                "path": relative,
                "sha256": digest_bytes(path.read_bytes()),
                "bytes": path.stat().st_size,
            }
        )
    return records


def gates() -> list[dict[str, Any]]:
    return [
        {
            "id": "combined_intake",
            "stage": "quarantine_to_intake",
            "script": "scripts/v54_progression_combined_intake_gate.py",
            "allowed_decisions": ["PASS_BLINDED_PROGRESSION_INTAKE"],
            "failure_decision": "FAIL_CLOSED",
        },
        {
            "id": "event_time",
            "stage": "assumptions_freeze",
            "script": "scripts/v54_progression_event_time_assumption_gate.py",
            "allowed_decisions": ["PASS_STANDARD_PLUS_DIAGNOSTICS", "PASS_SENSITIVITY_REQUIRED"],
            "failure_decision": "FAIL_CLOSED",
        },
        {
            "id": "site_score",
            "stage": "assumptions_freeze",
            "script": "scripts/v54_progression_site_score_calibration_gate.py",
            "allowed_decisions": ["PASS_SINGLE_SITE_FIXED_TRANSFORM", "PASS_MULTISITE_EQUIVALENT_SCALE", "PASS_MULTISITE_WITHIN_SITE_SCALE_REQUIRED"],
            "failure_decision": "FAIL_CLOSED",
        },
        {
            "id": "treatment_switch",
            "stage": "assumptions_freeze",
            "script": "scripts/v54_progression_treatment_switch_gate.py",
            "allowed_decisions": ["PASS_SWITCH_SENSITIVITY_REQUIRED", "PASS_NO_OBSERVED_SWITCH_DUAL_PLAN"],
            "failure_decision": "FAIL_CLOSED",
        },
        {
            "id": "nonlinear_diagnostics",
            "stage": "assumptions_freeze",
            "script": "scripts/v54_progression_nonlinear_diagnostic_gate.py",
            "allowed_decisions": ["PASS_FIXED_NONLINEAR_DIAGNOSTIC_FAMILY"],
            "failure_decision": "FAIL_CLOSED",
        },
        {
            "id": "blinded_feasibility",
            "stage": "feasibility_routing",
            "script": "scripts/v54_progression_blinded_feasibility.py",
            "allowed_decisions": ["REFERENCE_ALIGNED_FOR_COHORT_SPECIFIC_POWER", "REFERENCE_ALIGNED_SENSITIVITY_REQUIRED", "VALID_BELOW_REFERENCE_REPARAMETERIZE"],
            "failure_decision": "FAIL_CLOSED",
        },
        {
            "id": "information_monitor",
            "stage": "blinded_accrual",
            "script": "scripts/v54_progression_information_monitor.py",
            "allowed_decisions": ["CONTINUE_BLINDED_ACCRUAL", "HOLD_UNRESOLVED_CENSORING_METADATA", "REFERENCE_INFORMATION_REACHED_LOCK_AND_HANDOFF"],
            "failure_decision": "FAIL_CLOSED_PEEKING_OR_METADATA",
        },
        {
            "id": "p1_intake_to_lock",
            "stage": "composition",
            "script": "scripts/v54_progression_p1_intake_to_lock.py",
            "allowed_decisions": ["CONTINUE_BLINDED_ACCRUAL", "HOLD_UNRESOLVED_METADATA", "LOCK_READY_FOR_FROZEN_ANALYSIS"],
            "failure_decision": "FAIL_CLOSED",
        },
    ]


def build_manifest() -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema_version": "1.0.0",
        "contract_id": "V54_PROGRESSION_REFERENCE_DESIGN",
        "frozen_at_utc": FROZEN_AT,
        "synthetic_or_method_only": True,
        "reference_design": {
            "planned_gross_enrollment_under_10pct_losses": 690,
            "analyzable_total": 450,
            "sites": 3,
            "analyzable_per_site": 150,
            "confirmed_event_total": 135,
            "minimum_confirmed_events_per_site": 10,
            "event_probability_assumption": 0.30,
            "visit_interval_months": 3,
            "followup_months": 24,
            "score_reliability_assumption": 0.70,
            "molecular_repeat_count": 1,
            "status": "stress_tested_reference_not_universal_minimum",
        },
        "analysis": {
            "primary_route": "within-site standardized score; site/source/treatment-stratified event-time model",
            "endpoint": "protocol-defined confirmed progression; CDP and PIRA separate",
            "switch_estimands": ["treatment_policy", "censor_at_switch"],
            "nonlinear_diagnostics": ["high_threshold_z_0.674", "tanh_1.5_observed_z", "linear_plus_quadratic_2df"],
            "attendance_boundary": "unknown, outcome-related, or joint score/risk attendance fails closed",
            "diagnostics_nonrescuing": True,
        },
        "lifecycle": [
            "quarantined",
            "intake_passed",
            "assumptions_frozen",
            "feasibility_classified",
            "blinded_accrual",
            "information_locked",
            "frozen_analysis_handoff",
        ],
        "forbidden_before_lock": [
            "individual_outcomes",
            "molecular_values",
            "effect_direction",
            "effect_estimate",
            "p_value",
            "efficacy_recommendation",
            "futility_recommendation",
        ],
        "gates": gates(),
        "sources": source_records(),
        "current_known_eligible_roles": {"P1": 0, "P2": 0, "P3": 0},
        "interpretation_boundary": "Reference alignment and lock readiness are process states, not validation, progression evidence, target evidence, treatment effect, or proof that an intervention halts MS.",
    }
    body["contract_sha256"] = digest_bytes(canonical(body))
    return body


def blockers(document: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    issues = []
    if document != expected:
        issues.append("manifest_content_or_source_hash_drift")
    supplied_digest = document.get("contract_sha256")
    without_digest = copy.deepcopy(document)
    without_digest.pop("contract_sha256", None)
    if supplied_digest != digest_bytes(canonical(without_digest)):
        issues.append("contract_sha256_invalid")
    if document.get("reference_design", {}).get("analyzable_total") != 450:
        issues.append("reference_analyzable_total_changed")
    if len(document.get("gates", [])) != 8:
        issues.append("gate_count_changed")
    return sorted(set(issues))


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def evaluate(write: bool) -> dict[str, Any]:
    expected = build_manifest()
    OUT.mkdir(parents=True, exist_ok=True)
    if write:
        MANIFEST.write_text(json.dumps(expected, indent=2) + "\n")
        write_tsv(OUT / "source_hashes.tsv", expected["sources"])
    if not MANIFEST.is_file():
        raise RuntimeError("Manifest missing; run with --write after review")
    observed = json.loads(MANIFEST.read_text())
    current_blockers = blockers(observed, expected)
    tampered = copy.deepcopy(expected)
    tampered["reference_design"]["analyzable_total"] = 449
    synthetic_rows = [
        {
            "fixture": "current_committed_manifest",
            "synthetic": True,
            "expected_pass": True,
            "observed_pass": not current_blockers,
            "regression_pass": not current_blockers,
        },
        {
            "fixture": "tampered_reference_total",
            "synthetic": True,
            "expected_pass": False,
            "observed_pass": not blockers(tampered, expected),
            "regression_pass": bool(blockers(tampered, expected)),
        },
    ]
    write_tsv(OUT / "synthetic_regression.tsv", synthetic_rows)
    passed = all(row["regression_pass"] for row in synthetic_rows)
    summary = {
        "purpose": "V54 hash-bound progression reference manifest verification",
        "synthetic_or_method_only": True,
        "mode": "write" if write else "verify",
        "n_gates": len(expected["gates"]),
        "n_bound_sources": len(expected["sources"]),
        "n_current_blockers": len(current_blockers),
        "current_blockers": current_blockers,
        "n_synthetic_fixtures": len(synthetic_rows),
        "n_synthetic_pass": sum(row["regression_pass"] for row in synthetic_rows),
        "contract_sha256": expected["contract_sha256"],
        "overall_status": "PASS" if passed and not current_blockers else "FAIL",
        "boundary": "Machine contract and drift behavior only; no progression, treatment, target, or biological claim.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if summary["overall_status"] != "PASS":
        raise RuntimeError(f"V54 progression manifest verification failed: {current_blockers}")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    print(json.dumps(evaluate(write=args.write), indent=2))


if __name__ == "__main__":
    main()
