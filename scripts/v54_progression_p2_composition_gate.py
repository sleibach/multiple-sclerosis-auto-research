#!/usr/bin/env python3
"""Validate composition measurement eligibility for the frozen V54 P2 route."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_p2_composition_gate"
DIRECT_METHODS = {"flow_cytometry", "cytof", "cite_seq", "single_cell_counts"}
PROXY_METHODS = {"deconvolution", "other_proxy"}
REQUIRED_TRUE = {
    "synthetic_or_quarantined",
    "frozen_before_score_access",
    "same_method_all_compartments",
    "same_method_all_outcome_groups",
    "exact_sample_linkage",
    "collection_time_correspondence_verified",
    "cell_definitions_frozen",
    "qc_rule_frozen",
    "missingness_rule_frozen",
    "batch_rule_frozen",
    "differential_missingness_action_frozen",
}
REQUIRED_FALSE = {
    "scores_accessed_before_freeze",
    "individual_outcomes_accessed_before_freeze",
    "method_selected_from_outcome_association",
}
REQUIRED_TEXT = {
    "package_id",
    "measurement_method",
    "measurement_artifact",
    "sample_linkage_artifact",
    "cell_definition_artifact",
    "qc_artifact",
    "missingness_action",
    "batch_action",
}


def present(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() not in {
        "",
        "unknown",
        "tbd",
        "todo",
        "placeholder",
    }


def validate(declaration: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    blockers: list[str] = []
    checks: list[dict[str, Any]] = []
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
    for field in sorted(REQUIRED_TEXT):
        passed = present(declaration.get(field))
        checks.append({"field": field, "expected": "non-placeholder text", "pass": passed})
        if not passed:
            blockers.append(f"{field}:missing_or_placeholder")

    method = str(declaration.get("measurement_method", "")).strip().lower()
    if method in DIRECT_METHODS:
        route = "direct"
    elif method in PROXY_METHODS:
        route = "proxy"
    else:
        route = "ineligible"
        blockers.append("measurement_method:not_direct_or_eligible_proxy")

    if declaration.get("expression_derived_proxy_only") is True:
        blockers.append("expression_derived_proxy_only:ineligible")

    if route == "proxy":
        proxy_requirements = {
            "direct_reference_subset_present": True,
            "direct_reference_sample_linked": True,
            "calibration_subset_blinded": True,
            "empirical_reliability_reported_by_compartment": True,
            "empirical_null_calibration_rerun": True,
            "empirical_null_calibration_pass": True,
            "proxy_not_sole_localization_evidence": True,
        }
        for field, expected in proxy_requirements.items():
            passed = declaration.get(field) is expected
            checks.append({"field": field, "expected": expected, "pass": passed})
            if not passed:
                blockers.append(f"{field}:required_for_proxy")
        reliability = declaration.get("minimum_empirical_reliability")
        reliability_pass = isinstance(reliability, (float, int)) and 0 < reliability <= 1
        checks.append({"field": "minimum_empirical_reliability", "expected": "0 < value <= 1", "pass": reliability_pass})
        if not reliability_pass:
            blockers.append("minimum_empirical_reliability:invalid_or_missing")
        for field in ("direct_reference_artifact", "empirical_calibration_artifact"):
            passed = present(declaration.get(field))
            checks.append({"field": field, "expected": "non-placeholder text", "pass": passed})
            if not passed:
                blockers.append(f"{field}:required_for_proxy")

    blockers = sorted(set(blockers))
    if blockers:
        decision = "FAIL_CLOSED"
    elif route == "direct":
        decision = "PASS_DIRECT_MEASUREMENT"
    else:
        decision = "PASS_VALIDATED_PROXY_REQUIRES_SENSITIVITY"

    output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(checks).to_csv(output_dir / "field_checks.tsv", sep="\t", index=False)
    summary = {
        "purpose": "V54 P2 composition measurement eligibility gate; no biological claim",
        "synthetic": declaration.get("synthetic") is True,
        "package_id": declaration.get("package_id", ""),
        "measurement_method": method,
        "route": route,
        "n_checks": len(checks),
        "n_blockers": len(blockers),
        "blockers": blockers,
        "decision": decision,
        "boundary": "A pass establishes composition-method eligibility only; it is not localization, progression, or biological evidence.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def base(method: str = "flow_cytometry") -> dict[str, Any]:
    return {
        "synthetic": True,
        "synthetic_or_quarantined": True,
        "package_id": "SYNTHETIC_P2_PACKAGE_DO_NOT_USE_AS_DATA",
        "measurement_method": method,
        "measurement_artifact": "SYNTHETIC_ONLY/composition.tsv",
        "sample_linkage_artifact": "SYNTHETIC_ONLY/linkage.tsv",
        "cell_definition_artifact": "SYNTHETIC_ONLY/cell_definitions.tsv",
        "qc_artifact": "SYNTHETIC_ONLY/qc.tsv",
        "missingness_action": "SYNTHETIC fail/inconclusive on differential missingness",
        "batch_action": "SYNTHETIC fixed batch adjustment",
        "frozen_before_score_access": True,
        "scores_accessed_before_freeze": False,
        "individual_outcomes_accessed_before_freeze": False,
        "same_method_all_compartments": True,
        "same_method_all_outcome_groups": True,
        "exact_sample_linkage": True,
        "collection_time_correspondence_verified": True,
        "cell_definitions_frozen": True,
        "qc_rule_frozen": True,
        "missingness_rule_frozen": True,
        "batch_rule_frozen": True,
        "differential_missingness_action_frozen": True,
        "method_selected_from_outcome_association": False,
        "expression_derived_proxy_only": False,
    }


def proxy_base() -> dict[str, Any]:
    declaration = base("deconvolution")
    declaration.update(
        {
            "direct_reference_subset_present": True,
            "direct_reference_sample_linked": True,
            "calibration_subset_blinded": True,
            "empirical_reliability_reported_by_compartment": True,
            "minimum_empirical_reliability": 0.82,
            "empirical_null_calibration_rerun": True,
            "empirical_null_calibration_pass": True,
            "proxy_not_sole_localization_evidence": True,
            "direct_reference_artifact": "SYNTHETIC_ONLY/direct_reference.tsv",
            "empirical_calibration_artifact": "SYNTHETIC_ONLY/null_calibration.json",
        }
    )
    return declaration


def synthetic_regression(output_dir: Path) -> dict[str, Any]:
    cases = [
        ("direct_flow", base("flow_cytometry"), "PASS_DIRECT_MEASUREMENT"),
        ("direct_cite", base("cite_seq"), "PASS_DIRECT_MEASUREMENT"),
        ("validated_proxy", proxy_base(), "PASS_VALIDATED_PROXY_REQUIRES_SENSITIVITY"),
        ("proxy_without_direct_subset", {**proxy_base(), "direct_reference_subset_present": False}, "FAIL_CLOSED"),
        ("proxy_failed_null_calibration", {**proxy_base(), "empirical_null_calibration_pass": False}, "FAIL_CLOSED"),
        ("expression_proxy_only", {**base("expression_module_score"), "expression_derived_proxy_only": True}, "FAIL_CLOSED"),
        ("missing_sample_linkage", {**base(), "exact_sample_linkage": False}, "FAIL_CLOSED"),
        ("outcome_selected_method", {**base(), "method_selected_from_outcome_association": True}, "FAIL_CLOSED"),
        ("unresolved_missingness", {**base(), "differential_missingness_action_frozen": False}, "FAIL_CLOSED"),
    ]
    fixture_dir = output_dir / "synthetic"
    rows = []
    for name, declaration, expected in cases:
        fixture_dir.mkdir(parents=True, exist_ok=True)
        (fixture_dir / f"{name}.json").write_text(json.dumps(declaration, indent=2) + "\n")
        result = validate(declaration, output_dir / "runs" / name)
        rows.append(
            {
                "fixture": name,
                "synthetic": True,
                "expected_decision": expected,
                "observed_decision": result["decision"],
                "regression_pass": result["decision"] == expected,
            }
        )
    frame = pd.DataFrame(rows)
    frame.to_csv(output_dir / "synthetic_regression.tsv", sep="\t", index=False)
    passed = bool(frame.regression_pass.all())
    summary = {
        "purpose": "Synthetic regression for V54 P2 composition measurement eligibility",
        "synthetic": True,
        "n_fixtures": len(frame),
        "n_pass": int(frame.regression_pass.sum()),
        "overall_status": "PASS" if passed else "FAIL",
        "boundary": "Synthetic gate behavior only; no patient data or biological evidence.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if not passed:
        raise RuntimeError("V54 P2 composition gate regression failed")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--declaration", type=Path)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()
    if args.declaration:
        summary = validate(json.loads(args.declaration.read_text()), args.output_dir)
        print(json.dumps(summary, indent=2))
        if args.fail_on_error and summary["decision"] == "FAIL_CLOSED":
            raise SystemExit(1)
    else:
        print(json.dumps(synthetic_regression(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
