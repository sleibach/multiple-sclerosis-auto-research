#!/usr/bin/env python3
"""Fail-closed endpoint-confirmation provenance receipt gate for V54."""

from __future__ import annotations

import argparse
import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_confirmation_provenance_gate"
PLACEHOLDERS = {"", "unknown", "tbd", "todo", "placeholder", "na", "n/a"}
REQUIRED_TEXT = {
    "package_id",
    "endpoint_declaration_id",
    "protocol_source",
    "confirmation_process_source",
    "candidate_worsening_date_field",
    "confirmation_date_field",
    "confirmation_status_field",
    "unconfirmed_reason_field",
    "status_dictionary_source",
    "reason_dictionary_source",
    "site_source_mapping_field",
    "confirmation_process_audit_plan",
}
REQUIRED_TRUE = {
    "raw_candidate_records_present",
    "raw_confirmation_records_present",
    "confirmed_and_unconfirmed_records_retained",
    "transient_candidates_retained",
    "late_valid_candidates_retained",
    "censored_before_confirmation_retained",
    "missing_confirmation_distinct_from_no_event",
    "site_specific_process_auditable",
    "confirmation_process_association_audit_frozen",
    "frozen_before_score_outcome_access",
}
REQUIRED_FALSE = {
    "derived_progression_label_only",
    "scores_accessed_before_freeze",
    "individual_outcomes_accessed_before_freeze",
    "post_result_event_reclassification_allowed",
    "missing_confirmation_recoded_as_no_event",
    "unconfirmed_records_dropped",
}
ALLOWED_BLINDING = {"blinded", "molecular_score_not_computed"}


def text_present(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() not in PLACEHOLDERS


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def validate(declaration: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    blockers: list[str] = []

    def check(field: str, expected: str, passed: bool, observed: Any) -> None:
        checks.append(
            {
                "field": field,
                "expected": expected,
                "observed": json.dumps(observed, sort_keys=True),
                "pass": passed,
            }
        )
        if not passed:
            blockers.append(f"{field}:invalid")

    for field in sorted(REQUIRED_TEXT):
        check(field, "non-placeholder text", text_present(declaration.get(field)), declaration.get(field))
    for field in sorted(REQUIRED_TRUE):
        check(field, "true", declaration.get(field) is True, declaration.get(field))
    for field in sorted(REQUIRED_FALSE):
        check(field, "false", declaration.get(field) is False, declaration.get(field))
    check("synthetic", "explicit boolean", isinstance(declaration.get("synthetic"), bool), declaration.get("synthetic"))
    check(
        "confirmation_assessor_molecular_blinding",
        "blinded or molecular_score_not_computed",
        declaration.get("confirmation_assessor_molecular_blinding") in ALLOWED_BLINDING,
        declaration.get("confirmation_assessor_molecular_blinding"),
    )
    interval = declaration.get("confirmation_interval_days")
    check(
        "confirmation_interval_days",
        "positive integer",
        isinstance(interval, int) and not isinstance(interval, bool) and interval > 0,
        interval,
    )
    tolerance = declaration.get("confirmation_visit_tolerance_days")
    check(
        "confirmation_visit_tolerance_days",
        "nonnegative integer",
        isinstance(tolerance, int) and not isinstance(tolerance, bool) and tolerance >= 0,
        tolerance,
    )

    blockers = sorted(set(blockers))
    decision = "FAIL_CLOSED" if blockers else "PASS_CONFIRMATION_PROVENANCE_GATE"
    output_dir.mkdir(parents=True, exist_ok=True)
    write_tsv(output_dir / "field_checks.tsv", checks)
    summary = {
        "purpose": "V54 blind endpoint-confirmation provenance receipt gate; no biological claim",
        "synthetic": declaration.get("synthetic") is True,
        "package_id": declaration.get("package_id", ""),
        "n_checks": len(checks),
        "n_blockers": len(blockers),
        "blockers": blockers,
        "decision": decision,
        "boundary": "A pass establishes auditable confirmation provenance only; it is not evidence of unbiased adjudication, progression association, or treatment effect.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def base_declaration() -> dict[str, Any]:
    return {
        "synthetic": True,
        "package_id": "SYNTHETIC_CONFIRMATION_PACKAGE_DO_NOT_USE_AS_DATA",
        "endpoint_declaration_id": "SYNTHETIC_ENDPOINT_DECLARATION",
        "protocol_source": "SYNTHETIC_ONLY/protocol.txt",
        "confirmation_process_source": "SYNTHETIC_ONLY/confirmation_process.txt",
        "candidate_worsening_date_field": "candidate_worsening_day",
        "confirmation_date_field": "confirmation_day",
        "confirmation_status_field": "confirmation_status",
        "unconfirmed_reason_field": "unconfirmed_reason",
        "status_dictionary_source": "SYNTHETIC_ONLY/status_dictionary.tsv",
        "reason_dictionary_source": "SYNTHETIC_ONLY/reason_dictionary.tsv",
        "site_source_mapping_field": "collection_site",
        "confirmation_process_audit_plan": "Holm-corrected frozen score-confirmation process association audit",
        "confirmation_assessor_molecular_blinding": "blinded",
        "confirmation_interval_days": 180,
        "confirmation_visit_tolerance_days": 30,
        "raw_candidate_records_present": True,
        "raw_confirmation_records_present": True,
        "confirmed_and_unconfirmed_records_retained": True,
        "transient_candidates_retained": True,
        "late_valid_candidates_retained": True,
        "censored_before_confirmation_retained": True,
        "missing_confirmation_distinct_from_no_event": True,
        "site_specific_process_auditable": True,
        "confirmation_process_association_audit_frozen": True,
        "frozen_before_score_outcome_access": True,
        "derived_progression_label_only": False,
        "scores_accessed_before_freeze": False,
        "individual_outcomes_accessed_before_freeze": False,
        "post_result_event_reclassification_allowed": False,
        "missing_confirmation_recoded_as_no_event": False,
        "unconfirmed_records_dropped": False,
    }


def synthetic_regression(output_dir: Path) -> dict[str, Any]:
    cases = [
        ("blinded_assessor", {}, "PASS_CONFIRMATION_PROVENANCE_GATE"),
        ("score_not_computed", {"confirmation_assessor_molecular_blinding": "molecular_score_not_computed"}, "PASS_CONFIRMATION_PROVENANCE_GATE"),
        ("derived_label_only", {"derived_progression_label_only": True}, "FAIL_CLOSED"),
        ("missing_candidate_date", {"candidate_worsening_date_field": ""}, "FAIL_CLOSED"),
        ("unknown_blinding", {"confirmation_assessor_molecular_blinding": "unknown"}, "FAIL_CLOSED"),
        ("unconfirmed_dropped", {"unconfirmed_records_dropped": True}, "FAIL_CLOSED"),
        ("missing_as_no_event", {"missing_confirmation_recoded_as_no_event": True}, "FAIL_CLOSED"),
        ("post_result_reclassification", {"post_result_event_reclassification_allowed": True}, "FAIL_CLOSED"),
        ("missing_reason_dictionary", {"reason_dictionary_source": "TBD"}, "FAIL_CLOSED"),
        ("score_accessed", {"scores_accessed_before_freeze": True}, "FAIL_CLOSED"),
    ]
    rows: list[dict[str, Any]] = []
    for name, edits, expected in cases:
        declaration = base_declaration()
        declaration.update(deepcopy(edits))
        declaration["package_id"] = f"SYNTHETIC_{name.upper()}_DO_NOT_USE_AS_DATA"
        fixture = output_dir / "synthetic" / f"{name}.json"
        fixture.parent.mkdir(parents=True, exist_ok=True)
        fixture.write_text(json.dumps(declaration, indent=2) + "\n")
        result = validate(declaration, output_dir / "runs" / name)
        rows.append(
            {
                "fixture": name,
                "synthetic": True,
                "expected_decision": expected,
                "observed_decision": result["decision"],
                "n_blockers": result["n_blockers"],
                "regression_pass": result["decision"] == expected,
            }
        )
    write_tsv(output_dir / "synthetic_regression.tsv", rows)
    n_pass = sum(row["regression_pass"] for row in rows)
    summary = {
        "purpose": "Synthetic regression of V54 endpoint-confirmation provenance receipt gate",
        "synthetic": True,
        "n_fixtures": len(rows),
        "n_pass": n_pass,
        "n_expected_process_pass": 2,
        "n_expected_fail_closed": 8,
        "overall_status": "PASS" if n_pass == len(rows) else "FAIL",
        "boundary": "Synthetic gate behavior only; no patient data, confirmation error estimate, progression association, or biological claim.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if summary["overall_status"] != "PASS":
        raise RuntimeError("V54 confirmation-provenance gate regression failed")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--declaration", type=Path)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()
    if args.declaration:
        result = validate(json.loads(args.declaration.read_text()), args.output_dir)
        print(json.dumps(result, indent=2))
        if args.fail_on_error and result["decision"] == "FAIL_CLOSED":
            raise SystemExit(1)
    else:
        print(json.dumps(synthetic_regression(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
