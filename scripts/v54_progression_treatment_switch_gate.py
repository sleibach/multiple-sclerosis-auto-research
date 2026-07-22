#!/usr/bin/env python3
"""Fail-closed blind treatment-switch estimand receipt gate for V54."""

from __future__ import annotations

import argparse
import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_treatment_switch_gate"
PLACEHOLDERS = {"", "unknown", "tbd", "todo", "placeholder", "na", "n/a"}
REQUIRED_TEXT = {
    "package_id",
    "protocol_source",
    "treatment_history_source",
    "switch_date_field",
    "switch_reason_field",
    "switch_reason_dictionary_source",
    "treatment_indication_context_source",
    "source_treatment_indication_adjustment",
    "competing_event_rule",
    "censor_at_switch_ipcw_model",
    "joint_score_progression_risk_sensitivity",
}
REQUIRED_TRUE = {
    "frozen_before_score_outcome_access",
    "switch_reason_dictionary_complete",
    "unknown_switch_reason_category_defined",
    "post_switch_outcomes_retained",
    "both_estimands_reported",
    "censor_at_switch_ipcw_prespecified",
    "joint_dependence_sensitivity_prespecified",
    "source_treatment_indication_adjustment_prespecified",
}
REQUIRED_FALSE = {
    "scores_accessed_before_freeze",
    "individual_outcomes_accessed_before_freeze",
    "post_result_estimand_selection",
    "outcome_driven_switch_exclusion",
    "endpoint_redefined_after_switch",
}
ESTIMANDS = {"treatment_policy", "censor_at_switch"}


def text_present(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() not in PLACEHOLDERS


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def validate(declaration: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    blockers: list[str] = []
    checks: list[dict[str, Any]] = []

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

    switching = declaration.get("switching_present")
    check("switching_present", "yes|no", switching in {"yes", "no"}, switching)
    unknown = declaration.get("unknown_switch_reasons_present")
    check("unknown_switch_reasons_present", "yes|no", unknown in {"yes", "no"}, unknown)
    count = declaration.get("blinded_aggregate_switch_count")
    count_valid = isinstance(count, int) and not isinstance(count, bool) and count >= 0
    check("blinded_aggregate_switch_count", "nonnegative integer", count_valid, count)
    presence_consistent = bool(
        count_valid
        and ((switching == "no" and count == 0) or (switching == "yes" and count > 0))
    )
    check(
        "switch_presence_count_consistency",
        "no iff count=0; yes iff count>0",
        presence_consistent,
        {"switching_present": switching, "count": count},
    )

    primary = declaration.get("primary_estimand")
    sensitivity = declaration.get("sensitivity_estimand")
    check("primary_estimand", "treatment_policy|censor_at_switch", primary in ESTIMANDS, primary)
    check("sensitivity_estimand", "opposite valid estimand", sensitivity in ESTIMANDS, sensitivity)
    check(
        "dual_estimand_complement",
        "primary and sensitivity are different and exhaustive",
        {primary, sensitivity} == ESTIMANDS,
        {"primary": primary, "sensitivity": sensitivity},
    )
    if unknown == "yes":
        blockers.append("unknown_switch_reasons_present:fail_closed")

    blockers = sorted(set(blockers))
    if blockers:
        decision = "FAIL_CLOSED"
    elif switching == "yes":
        decision = "PASS_SWITCH_SENSITIVITY_REQUIRED"
    else:
        decision = "PASS_NO_OBSERVED_SWITCH_DUAL_PLAN"

    output_dir.mkdir(parents=True, exist_ok=True)
    write_tsv(output_dir / "field_checks.tsv", checks)
    summary = {
        "purpose": "V54 blind progression treatment-switch estimand gate; no biological claim",
        "synthetic": declaration.get("synthetic") is True,
        "package_id": declaration.get("package_id", ""),
        "primary_estimand": primary,
        "sensitivity_estimand": sensitivity,
        "n_checks": len(checks),
        "n_blockers": len(blockers),
        "blockers": blockers,
        "decision": decision,
        "boundary": "A pass freezes dual estimands and switch metadata only; it is not evidence of independent switching, treatment effect, prognosis, progression, or MS biology.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def base_declaration() -> dict[str, Any]:
    return {
        "synthetic": True,
        "package_id": "SYNTHETIC_SWITCH_PACKAGE_DO_NOT_USE_AS_DATA",
        "protocol_source": "SYNTHETIC_ONLY/protocol.txt",
        "treatment_history_source": "SYNTHETIC_ONLY/treatment.tsv",
        "switch_date_field": "synthetic_switch_date",
        "switch_reason_field": "synthetic_switch_reason",
        "switch_reason_dictionary_source": "SYNTHETIC_ONLY/switch_dictionary.tsv",
        "treatment_indication_context_source": "SYNTHETIC_ONLY/indication.tsv",
        "source_treatment_indication_adjustment": "SYNTHETIC frozen strata/covariates",
        "competing_event_rule": "SYNTHETIC frozen cause-specific sensitivity",
        "censor_at_switch_ipcw_model": "SYNTHETIC baseline and observed history model",
        "joint_score_progression_risk_sensitivity": "SYNTHETIC fixed selection bound",
        "frozen_before_score_outcome_access": True,
        "switch_reason_dictionary_complete": True,
        "unknown_switch_reason_category_defined": True,
        "post_switch_outcomes_retained": True,
        "both_estimands_reported": True,
        "censor_at_switch_ipcw_prespecified": True,
        "joint_dependence_sensitivity_prespecified": True,
        "source_treatment_indication_adjustment_prespecified": True,
        "scores_accessed_before_freeze": False,
        "individual_outcomes_accessed_before_freeze": False,
        "post_result_estimand_selection": False,
        "outcome_driven_switch_exclusion": False,
        "endpoint_redefined_after_switch": False,
        "switching_present": "yes",
        "unknown_switch_reasons_present": "no",
        "blinded_aggregate_switch_count": 24,
        "primary_estimand": "treatment_policy",
        "sensitivity_estimand": "censor_at_switch",
    }


def synthetic_regression(output_dir: Path) -> dict[str, Any]:
    cases = [
        ("switches_complete", {}, "PASS_SWITCH_SENSITIVITY_REQUIRED"),
        ("no_switches", {"switching_present": "no", "blinded_aggregate_switch_count": 0}, "PASS_NO_OBSERVED_SWITCH_DUAL_PLAN"),
        ("unknown_reason", {"unknown_switch_reasons_present": "yes"}, "FAIL_CLOSED"),
        ("count_mismatch", {"switching_present": "no", "blinded_aggregate_switch_count": 3}, "FAIL_CLOSED"),
        ("same_estimand_twice", {"sensitivity_estimand": "treatment_policy"}, "FAIL_CLOSED"),
        ("one_estimand_only", {"both_estimands_reported": False}, "FAIL_CLOSED"),
        ("post_result_selection", {"post_result_estimand_selection": True}, "FAIL_CLOSED"),
        ("missing_ipcw", {"censor_at_switch_ipcw_prespecified": False}, "FAIL_CLOSED"),
        ("score_accessed", {"scores_accessed_before_freeze": True}, "FAIL_CLOSED"),
        ("post_switch_outcomes_missing", {"post_switch_outcomes_retained": False}, "FAIL_CLOSED"),
    ]
    rows: list[dict[str, Any]] = []
    for name, edits, expected in cases:
        declaration = base_declaration()
        declaration.update(deepcopy(edits))
        declaration["package_id"] = f"SYNTHETIC_{name.upper()}_DO_NOT_USE_AS_DATA"
        path = output_dir / "synthetic" / f"{name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(declaration, indent=2) + "\n")
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
        "purpose": "Synthetic regression of V54 treatment-switch estimand receipt gate",
        "synthetic": True,
        "n_fixtures": len(rows),
        "n_pass": n_pass,
        "n_expected_process_pass": 2,
        "n_expected_fail_closed": 8,
        "overall_status": "PASS" if n_pass == len(rows) else "FAIL",
        "boundary": "Synthetic gate behavior only; no patient data, treatment effect, progression evidence, or biological claim.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if summary["overall_status"] != "PASS":
        raise RuntimeError("V54 treatment-switch gate regression failed")
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
