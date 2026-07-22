#!/usr/bin/env python3
"""Fail-closed blind nonlinear-diagnostic receipt gate for V54."""

from __future__ import annotations

import argparse
import csv
import json
import math
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_nonlinear_diagnostic_gate"
PLACEHOLDERS = {"", "unknown", "tbd", "todo", "placeholder", "na", "n/a"}
FROZEN_DIAGNOSTICS = {
    "high_threshold_z_0.674",
    "tanh_1.5_observed_z",
    "linear_plus_quadratic_2df",
}
REQUIRED_TEXT = {
    "package_id",
    "protocol_source",
    "analysis_plan_source",
    "primary_model",
    "primary_interpretation_rule",
    "diagnostic_interpretation_rule",
    "cutpoint_basis",
    "saturation_transform",
    "omnibus_formula",
    "multiplicity_method",
}
REQUIRED_TRUE = {
    "frozen_before_score_outcome_access",
    "primary_linear_coefficient_remains_primary",
    "primary_reported_regardless",
    "all_diagnostics_reported",
    "diagnostics_nonrescuing",
    "future_model_requires_separate_preregistration",
}
REQUIRED_FALSE = {
    "scores_accessed_before_freeze",
    "individual_outcomes_accessed_before_freeze",
    "post_result_diagnostic_substitution",
    "post_result_transform_selection",
    "diagnostic_can_replace_primary",
    "diagnostic_can_reinterpret_failed_primary",
}
ALLOWED_MULTIPLICITY = {"asymptotic_bonferroni", "independent_empirical_null_bank"}


def text_present(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() not in PLACEHOLDERS


def close(value: Any, expected: float) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isclose(
        float(value), expected, rel_tol=0.0, abs_tol=1e-12
    )


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

    family = declaration.get("diagnostic_family")
    family_valid = isinstance(family, list) and set(family) == FROZEN_DIAGNOSTICS and len(family) == 3
    check("diagnostic_family", "exact frozen three-test family", family_valid, family)
    check("threshold_z", "0.674", close(declaration.get("threshold_z"), 0.674), declaration.get("threshold_z"))
    check("saturation_scale", "1.5", close(declaration.get("saturation_scale"), 1.5), declaration.get("saturation_scale"))
    check("primary_alpha", "0.05", close(declaration.get("primary_alpha"), 0.05), declaration.get("primary_alpha"))
    check("diagnostic_alpha", "0.05/3", close(declaration.get("diagnostic_alpha"), 0.05 / 3.0), declaration.get("diagnostic_alpha"))
    check("diagnostic_family_alpha", "0.05", close(declaration.get("diagnostic_family_alpha"), 0.05), declaration.get("diagnostic_family_alpha"))
    check("analysis_count_budget", "4", declaration.get("analysis_count_budget") == 4, declaration.get("analysis_count_budget"))

    method = declaration.get("multiplicity_method")
    check("multiplicity_method_allowed", "one frozen allowed route", method in ALLOWED_MULTIPLICITY, method)
    if method == "independent_empirical_null_bank":
        check("calibration_source", "non-placeholder source", text_present(declaration.get("calibration_source")), declaration.get("calibration_source"))
        check("calibration_seeds_disjoint", "true", declaration.get("calibration_seeds_disjoint") is True, declaration.get("calibration_seeds_disjoint"))
        check("calibration_data_disjoint", "true", declaration.get("calibration_data_disjoint") is True, declaration.get("calibration_data_disjoint"))

    blockers = sorted(set(blockers))
    decision = "FAIL_CLOSED" if blockers else "PASS_FIXED_NONLINEAR_DIAGNOSTIC_FAMILY"
    output_dir.mkdir(parents=True, exist_ok=True)
    write_tsv(output_dir / "field_checks.tsv", checks)
    summary = {
        "purpose": "V54 blind nonlinear-diagnostic receipt gate; no biological claim",
        "synthetic": declaration.get("synthetic") is True,
        "package_id": declaration.get("package_id", ""),
        "multiplicity_method": method,
        "n_checks": len(checks),
        "n_blockers": len(blockers),
        "blockers": blockers,
        "decision": decision,
        "boundary": "A pass freezes non-rescuing model diagnostics only; it is not evidence of nonlinear MS risk, progression, mechanism, or treatment effect.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def base_declaration() -> dict[str, Any]:
    return {
        "synthetic": True,
        "package_id": "SYNTHETIC_NONLINEAR_PACKAGE_DO_NOT_USE_AS_DATA",
        "protocol_source": "SYNTHETIC_ONLY/protocol.txt",
        "analysis_plan_source": "SYNTHETIC_ONLY/analysis_plan.txt",
        "primary_model": "one standardized linear Cox score coefficient",
        "primary_interpretation_rule": "report one linear coefficient at alpha 0.05",
        "diagnostic_interpretation_rule": "non-rescuing checks; future model requires separate preregistration",
        "diagnostic_family": sorted(FROZEN_DIAGNOSTICS),
        "cutpoint_basis": "observed standardized score z > 0.674",
        "threshold_z": 0.674,
        "saturation_transform": "tanh(1.5 * observed_z)",
        "saturation_scale": 1.5,
        "omnibus_formula": "observed_z + observed_z_squared; two degrees of freedom",
        "primary_alpha": 0.05,
        "diagnostic_alpha": 0.05 / 3.0,
        "diagnostic_family_alpha": 0.05,
        "multiplicity_method": "asymptotic_bonferroni",
        "calibration_source": "not_applicable_asymptotic_route",
        "calibration_seeds_disjoint": True,
        "calibration_data_disjoint": True,
        "analysis_count_budget": 4,
        "frozen_before_score_outcome_access": True,
        "primary_linear_coefficient_remains_primary": True,
        "primary_reported_regardless": True,
        "all_diagnostics_reported": True,
        "diagnostics_nonrescuing": True,
        "future_model_requires_separate_preregistration": True,
        "scores_accessed_before_freeze": False,
        "individual_outcomes_accessed_before_freeze": False,
        "post_result_diagnostic_substitution": False,
        "post_result_transform_selection": False,
        "diagnostic_can_replace_primary": False,
        "diagnostic_can_reinterpret_failed_primary": False,
    }


def synthetic_regression(output_dir: Path) -> dict[str, Any]:
    cases = [
        ("fixed_asymptotic", {}, "PASS_FIXED_NONLINEAR_DIAGNOSTIC_FAMILY"),
        ("fixed_empirical", {"multiplicity_method": "independent_empirical_null_bank", "calibration_source": "SYNTHETIC_ONLY/disjoint_null_bank.json"}, "PASS_FIXED_NONLINEAR_DIAGNOSTIC_FAMILY"),
        ("missing_quadratic", {"diagnostic_family": ["high_threshold_z_0.674", "tanh_1.5_observed_z"]}, "FAIL_CLOSED"),
        ("threshold_changed", {"threshold_z": 1.0}, "FAIL_CLOSED"),
        ("uncorrected_alpha", {"diagnostic_alpha": 0.05}, "FAIL_CLOSED"),
        ("score_accessed", {"scores_accessed_before_freeze": True}, "FAIL_CLOSED"),
        ("posthoc_rescue", {"diagnostic_can_reinterpret_failed_primary": True}, "FAIL_CLOSED"),
        ("primary_replacement", {"diagnostic_can_replace_primary": True}, "FAIL_CLOSED"),
        ("nondisjoint_calibration", {"multiplicity_method": "independent_empirical_null_bank", "calibration_source": "SYNTHETIC_ONLY/null_bank.json", "calibration_seeds_disjoint": False}, "FAIL_CLOSED"),
        ("missing_calibration_source", {"multiplicity_method": "independent_empirical_null_bank", "calibration_source": ""}, "FAIL_CLOSED"),
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
        "purpose": "Synthetic regression of V54 nonlinear-diagnostic receipt gate",
        "synthetic": True,
        "n_fixtures": len(rows),
        "n_pass": n_pass,
        "n_expected_process_pass": 2,
        "n_expected_fail_closed": 8,
        "overall_status": "PASS" if n_pass == len(rows) else "FAIL",
        "boundary": "Synthetic gate behavior only; no patient data, nonlinear MS association, progression evidence, or biological claim.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if summary["overall_status"] != "PASS":
        raise RuntimeError("V54 nonlinear-diagnostic gate regression failed")
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
