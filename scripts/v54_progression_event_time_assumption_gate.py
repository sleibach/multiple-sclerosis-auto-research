#!/usr/bin/env python3
"""Fail-closed metadata gate for V54 progression event-time inference."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_event_time_assumption_gate"
REQUIRED_TEXT = {
    "package_id",
    "protocol_source",
    "data_dictionary_source",
    "followup_time_origin",
    "administrative_horizon",
    "event_date_field",
    "last_observation_date_field",
    "censoring_date_field",
    "censoring_reason_field",
    "censoring_reason_dictionary",
    "death_competing_event_rule",
    "treatment_switch_rule",
    "source_treatment_stratification",
    "joint_score_event_risk_sensitivity",
    "ipcw_model",
    "worst_case_censoring_bounds",
    "time_variation_diagnostic",
    "diagnostic_cut_basis",
    "window_contrast_rule",
}
REQUIRED_TRUE = {
    "frozen_before_score_access",
    "reason_dictionary_complete",
    "unknown_reason_category_defined",
    "outcome_related_reason_category_defined",
    "source_treatment_stratification_prespecified",
    "joint_score_event_risk_sensitivity_prespecified",
    "ipcw_prespecified",
    "worst_case_bounds_prespecified",
    "time_variation_diagnostic_prespecified",
}
REQUIRED_FALSE = {
    "scores_accessed_before_freeze",
    "individual_outcomes_accessed_before_freeze",
    "window_p_values_substitute_for_interaction",
}
ALLOWED_PRESENCE = {"yes", "no"}


def text_present(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value.strip().lower() not in {
        "unknown",
        "tbd",
        "todo",
        "placeholder",
    }


def validate(declaration: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    blockers: list[str] = []
    checks: list[dict[str, Any]] = []

    for field in sorted(REQUIRED_TEXT):
        passed = text_present(declaration.get(field))
        checks.append({"field": field, "expected": "non-placeholder text", "pass": passed})
        if not passed:
            blockers.append(f"{field}:missing_or_placeholder")
    for field in sorted(REQUIRED_TRUE):
        passed = declaration.get(field) is True
        checks.append({"field": field, "expected": True, "pass": passed})
        if not passed:
            blockers.append(f"{field}:must_be_true")
    for field in sorted(REQUIRED_FALSE):
        passed = declaration.get(field) is False
        checks.append({"field": field, "expected": False, "pass": passed})
        if not passed:
            blockers.append(f"{field}:must_be_false")

    for field in (
        "nonadministrative_censoring_present",
        "unknown_censoring_reasons_present",
        "outcome_related_censoring_present",
    ):
        value = str(declaration.get(field, "")).strip().lower()
        passed = value in ALLOWED_PRESENCE
        checks.append({"field": field, "expected": "yes|no", "pass": passed})
        if not passed:
            blockers.append(f"{field}:must_be_yes_or_no")

    analysis_budget = declaration.get("analysis_count_budget")
    budget_pass = isinstance(analysis_budget, int) and analysis_budget >= 1
    checks.append({"field": "analysis_count_budget", "expected": "positive integer", "pass": budget_pass})
    if not budget_pass:
        blockers.append("analysis_count_budget:must_be_positive_integer")

    unknown = str(declaration.get("unknown_censoring_reasons_present", "")).lower() == "yes"
    outcome_related = str(declaration.get("outcome_related_censoring_present", "")).lower() == "yes"
    nonadministrative = str(declaration.get("nonadministrative_censoring_present", "")).lower() == "yes"
    if unknown:
        blockers.append("unknown_censoring_reasons_present:cannot_exclude_joint_dependency")
    if outcome_related:
        blockers.append("outcome_related_censoring_present:cannot_exclude_joint_dependency")
    if text_present(declaration.get("window_contrast_rule")) and "direct" not in declaration["window_contrast_rule"].lower():
        blockers.append("window_contrast_rule:must_require_direct_prespecified_time_interaction")

    blockers = sorted(set(blockers))
    if blockers:
        decision = "FAIL_CLOSED"
    elif nonadministrative:
        decision = "PASS_SENSITIVITY_REQUIRED"
    else:
        decision = "PASS_STANDARD_PLUS_DIAGNOSTICS"

    output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(checks).to_csv(output_dir / "field_checks.tsv", sep="\t", index=False)
    summary = {
        "purpose": "V54 blind event-time assumption metadata gate; no biological claim",
        "synthetic": declaration.get("synthetic") is True,
        "package_id": declaration.get("package_id", ""),
        "n_checks": len(checks),
        "n_blockers": len(blockers),
        "blockers": blockers,
        "decision": decision,
        "boundary": "A pass establishes blind metadata and sensitivity readiness only; it is not evidence of independent censoring, proportional hazards, progression association, or MS biology.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def base_declaration() -> dict[str, Any]:
    return {
        "synthetic": True,
        "package_id": "SYNTHETIC_EVENT_TIME_PACKAGE_DO_NOT_USE_AS_DATA",
        "protocol_source": "SYNTHETIC_ONLY/protocol.txt",
        "data_dictionary_source": "SYNTHETIC_ONLY/dictionary.tsv",
        "frozen_before_score_access": True,
        "scores_accessed_before_freeze": False,
        "individual_outcomes_accessed_before_freeze": False,
        "followup_time_origin": "SYNTHETIC baseline assessment date",
        "administrative_horizon": "SYNTHETIC day 730",
        "event_date_field": "synthetic_event_date",
        "last_observation_date_field": "synthetic_last_observation_date",
        "censoring_date_field": "synthetic_censor_date",
        "censoring_reason_field": "synthetic_censor_reason",
        "censoring_reason_dictionary": "SYNTHETIC_ONLY/censor_reason_dictionary.tsv",
        "reason_dictionary_complete": True,
        "unknown_reason_category_defined": True,
        "outcome_related_reason_category_defined": True,
        "nonadministrative_censoring_present": "no",
        "unknown_censoring_reasons_present": "no",
        "outcome_related_censoring_present": "no",
        "death_competing_event_rule": "SYNTHETIC competing-risk sensitivity and censoring report",
        "treatment_switch_rule": "SYNTHETIC censor at switch with reason retained",
        "source_treatment_stratification": "SYNTHETIC four source-by-treatment strata",
        "source_treatment_stratification_prespecified": True,
        "joint_score_event_risk_sensitivity": "SYNTHETIC selection-weight and bound sensitivity",
        "joint_score_event_risk_sensitivity_prespecified": True,
        "ipcw_model": "SYNTHETIC baseline covariates and time-updated observed history only",
        "ipcw_prespecified": True,
        "worst_case_censoring_bounds": "SYNTHETIC all dropped subjects assigned adverse/favorable rank bounds",
        "worst_case_bounds_prespecified": True,
        "time_variation_diagnostic": "SYNTHETIC scaled Schoenfeld and fixed early/late descriptive windows",
        "time_variation_diagnostic_prespecified": True,
        "diagnostic_cut_basis": "SYNTHETIC protocol midpoint fixed before score access",
        "window_contrast_rule": "Only a direct prespecified score-by-time interaction may support time variation",
        "window_p_values_substitute_for_interaction": False,
        "analysis_count_budget": 4,
    }


def synthetic_regression(output_dir: Path) -> dict[str, Any]:
    cases: list[tuple[str, dict[str, Any], str]] = []
    cases.append(("administrative_only", {}, "PASS_STANDARD_PLUS_DIAGNOSTICS"))
    cases.append(("documented_nonadministrative", {"nonadministrative_censoring_present": "yes"}, "PASS_SENSITIVITY_REQUIRED"))
    cases.append(("unknown_reason", {"nonadministrative_censoring_present": "yes", "unknown_censoring_reasons_present": "yes"}, "FAIL_CLOSED"))
    cases.append(("outcome_related_loss", {"nonadministrative_censoring_present": "yes", "outcome_related_censoring_present": "yes"}, "FAIL_CLOSED"))
    cases.append(("score_unblinded", {"scores_accessed_before_freeze": True}, "FAIL_CLOSED"))
    cases.append(("missing_censor_date", {"censoring_date_field": ""}, "FAIL_CLOSED"))
    cases.append(("missing_time_diagnostic", {"time_variation_diagnostic_prespecified": False}, "FAIL_CLOSED"))
    cases.append(("window_p_substitution", {"window_p_values_substitute_for_interaction": True}, "FAIL_CLOSED"))

    fixture_dir = output_dir / "synthetic"
    rows = []
    for name, edits, expected in cases:
        declaration = deepcopy(base_declaration())
        declaration.update(edits)
        path = fixture_dir / f"{name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(declaration, indent=2) + "\n")
        result = validate(declaration, output_dir / "runs" / name)
        rows.append(
            {
                "fixture": name,
                "synthetic": True,
                "expected_decision": expected,
                "observed_decision": result["decision"],
                "regression_pass": result["decision"] == expected,
                "n_blockers": result["n_blockers"],
            }
        )
    frame = pd.DataFrame(rows)
    frame.to_csv(output_dir / "synthetic_regression.tsv", sep="\t", index=False)
    passed = bool(frame.regression_pass.all())
    summary = {
        "purpose": "Synthetic regression for the V54 event-time assumption metadata gate",
        "synthetic": True,
        "n_fixtures": len(frame),
        "n_pass": int(frame.regression_pass.sum()),
        "overall_status": "PASS" if passed else "FAIL",
        "boundary": "Synthetic gate behavior only; no patient data or biological evidence.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if not passed:
        raise RuntimeError("V54 event-time assumption gate regression failed")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--declaration", type=Path)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()
    if args.declaration:
        declaration = json.loads(args.declaration.read_text())
        summary = validate(declaration, args.output_dir)
        print(json.dumps(summary, indent=2))
        if args.fail_on_error and summary["decision"] == "FAIL_CLOSED":
            raise SystemExit(1)
    else:
        summary = synthetic_regression(args.output_dir)
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
