#!/usr/bin/env python3
"""Fail-closed blind negative-control declaration gate for V54 P1."""

from __future__ import annotations

import argparse
import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_negative_control_gate"
PLACEHOLDERS = {"", "unknown", "tbd", "todo", "placeholder", "na", "n/a"}
CONTROL_IDS = {
    "subject_blocked_score_permutation",
    "matched_random_module_bank",
    "unconfirmed_transient_worsening",
    "relapse_associated_worsening",
    "pre_index_progression_event",
    "attendance_censoring_process",
    "site_batch_quality_process",
}
ENDPOINT_CONTROLS = {
    "unconfirmed_transient_worsening",
    "relapse_associated_worsening",
    "pre_index_progression_event",
}
PERMUTATION_STRATA = {"source_cohort", "collection_site", "treatment_stratum"}
RANDOM_MATCHING = {"module_size", "detected_gene_count", "mean_expression", "expression_variance"}
REQUIRED_ACTIONS = {
    "subject_blocked_score_permutation": "PRIMARY_INFERENCE_INVALID",
    "matched_random_module_bank": "PRIMARY_INFERENCE_INVALID",
    "unconfirmed_transient_worsening": "PROGRESSION_SPECIFICITY_DOWNGRADE",
    "relapse_associated_worsening": "PROGRESSION_SPECIFICITY_DOWNGRADE",
    "pre_index_progression_event": "PROGRESSION_SPECIFICITY_DOWNGRADE",
    "attendance_censoring_process": "EVENT_TIME_INFERENCE_FAIL_CLOSED",
    "site_batch_quality_process": "TRANSPORT_OR_TECHNICAL_INTERPRETATION_FAIL_CLOSED",
}
REQUIRED_TEXT = {
    "package_id",
    "protocol_source",
    "analysis_plan_source",
    "primary_model",
    "primary_endpoint",
    "multiplicity_method",
    "random_module_exclusion_rule",
    "all_controls_pass_interpretation",
}
REQUIRED_TRUE = {
    "frozen_before_score_outcome_access",
    "preserve_subject_blocks",
    "exclude_primary_module_genes",
    "primary_reported_regardless",
    "all_controls_reported",
    "control_failures_apply_mandatory_actions",
    "future_control_change_requires_separate_preregistration",
}
REQUIRED_FALSE = {
    "scores_accessed_before_freeze",
    "individual_outcomes_accessed_before_freeze",
    "post_result_control_selection",
    "control_can_replace_primary",
    "control_can_rescue_primary",
    "clean_controls_can_upgrade_primary",
    "failed_control_can_be_omitted",
}


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
    check(
        "synthetic",
        "explicit boolean",
        isinstance(declaration.get("synthetic"), bool),
        declaration.get("synthetic"),
    )

    controls = declaration.get("control_family")
    check(
        "control_family",
        "exact seven-control family",
        isinstance(controls, list) and set(controls) == CONTROL_IDS and len(controls) == 7,
        controls,
    )
    endpoints = declaration.get("endpoint_specificity_controls")
    check(
        "endpoint_specificity_controls",
        "exact three endpoint controls",
        isinstance(endpoints, list) and set(endpoints) == ENDPOINT_CONTROLS and len(endpoints) == 3,
        endpoints,
    )
    strata = declaration.get("permutation_strata")
    check(
        "permutation_strata",
        "exact source/site/treatment strata",
        isinstance(strata, list) and set(strata) == PERMUTATION_STRATA and len(strata) == 3,
        strata,
    )
    matching = declaration.get("random_module_matching")
    check(
        "random_module_matching",
        "exact four-factor matching",
        isinstance(matching, list) and set(matching) == RANDOM_MATCHING and len(matching) == 4,
        matching,
    )
    check("seeds", "exact fixed seeds", declaration.get("seeds") == [55451, 55453, 55459], declaration.get("seeds"))
    check(
        "permutations_per_seed",
        ">=10000",
        isinstance(declaration.get("permutations_per_seed"), int) and declaration["permutations_per_seed"] >= 10000,
        declaration.get("permutations_per_seed"),
    )
    check("random_modules_per_seed", "100", declaration.get("random_modules_per_seed") == 100, declaration.get("random_modules_per_seed"))
    check("diagnostic_family_alpha", "0.05", declaration.get("diagnostic_family_alpha") == 0.05, declaration.get("diagnostic_family_alpha"))
    check(
        "multiplicity_method_exact",
        "holm_diagnostic_plus_maxT_random_bank",
        declaration.get("multiplicity_method") == "holm_diagnostic_plus_maxT_random_bank",
        declaration.get("multiplicity_method"),
    )
    check("random_bank_method", "maxT", declaration.get("random_bank_method") == "maxT", declaration.get("random_bank_method"))
    check("diagnostic_method", "holm", declaration.get("diagnostic_method") == "holm", declaration.get("diagnostic_method"))
    check("analysis_count_budget", "7", declaration.get("analysis_count_budget") == 7, declaration.get("analysis_count_budget"))
    check("mandatory_actions", "exact control-action map", declaration.get("mandatory_actions") == REQUIRED_ACTIONS, declaration.get("mandatory_actions"))

    blockers = sorted(set(blockers))
    decision = "FAIL_CLOSED" if blockers else "PASS_FIXED_NEGATIVE_CONTROL_FAMILY"
    output_dir.mkdir(parents=True, exist_ok=True)
    write_tsv(output_dir / "field_checks.tsv", checks)
    summary = {
        "purpose": "V54 blind P1 negative-control declaration gate; no biological claim",
        "synthetic": declaration.get("synthetic") is True,
        "package_id": declaration.get("package_id", ""),
        "n_controls": len(controls) if isinstance(controls, list) else 0,
        "n_checks": len(checks),
        "n_blockers": len(blockers),
        "blockers": blockers,
        "decision": decision,
        "boundary": "A pass freezes diagnostic controls only; clean controls cannot validate, rescue, or upgrade a progression claim.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def base_declaration() -> dict[str, Any]:
    return {
        "synthetic": True,
        "package_id": "SYNTHETIC_NEGATIVE_CONTROL_PACKAGE_DO_NOT_USE_AS_DATA",
        "protocol_source": "SYNTHETIC_ONLY/protocol.txt",
        "analysis_plan_source": "SYNTHETIC_ONLY/analysis_plan.txt",
        "primary_model": "one frozen site-stratified molecular Cox coefficient",
        "primary_endpoint": "one frozen confirmed CDP or PIRA endpoint",
        "control_family": sorted(CONTROL_IDS),
        "endpoint_specificity_controls": sorted(ENDPOINT_CONTROLS),
        "permutation_strata": sorted(PERMUTATION_STRATA),
        "preserve_subject_blocks": True,
        "seeds": [55451, 55453, 55459],
        "permutations_per_seed": 10000,
        "random_modules_per_seed": 100,
        "random_module_matching": sorted(RANDOM_MATCHING),
        "exclude_primary_module_genes": True,
        "random_module_exclusion_rule": "exclude every primary module gene before blind matching",
        "multiplicity_method": "holm_diagnostic_plus_maxT_random_bank",
        "diagnostic_method": "holm",
        "random_bank_method": "maxT",
        "diagnostic_family_alpha": 0.05,
        "analysis_count_budget": 7,
        "mandatory_actions": REQUIRED_ACTIONS,
        "all_controls_pass_interpretation": "retain primary grade only; no upgrade or causal claim",
        "frozen_before_score_outcome_access": True,
        "primary_reported_regardless": True,
        "all_controls_reported": True,
        "control_failures_apply_mandatory_actions": True,
        "future_control_change_requires_separate_preregistration": True,
        "scores_accessed_before_freeze": False,
        "individual_outcomes_accessed_before_freeze": False,
        "post_result_control_selection": False,
        "control_can_replace_primary": False,
        "control_can_rescue_primary": False,
        "clean_controls_can_upgrade_primary": False,
        "failed_control_can_be_omitted": False,
    }


def synthetic_regression(output_dir: Path) -> dict[str, Any]:
    cases = [
        ("fixed_family", {}, "PASS_FIXED_NEGATIVE_CONTROL_FAMILY"),
        ("missing_site_process", {"control_family": sorted(CONTROL_IDS - {"site_batch_quality_process"})}, "FAIL_CLOSED"),
        ("missing_endpoint_control", {"endpoint_specificity_controls": sorted(ENDPOINT_CONTROLS - {"pre_index_progression_event"})}, "FAIL_CLOSED"),
        ("too_few_permutations", {"permutations_per_seed": 1000}, "FAIL_CLOSED"),
        ("changed_permutation_strata", {"permutation_strata": ["collection_site"]}, "FAIL_CLOSED"),
        ("post_access_freeze", {"scores_accessed_before_freeze": True}, "FAIL_CLOSED"),
        ("rescue_authority", {"control_can_rescue_primary": True}, "FAIL_CLOSED"),
        ("omit_failed_control", {"failed_control_can_be_omitted": True}, "FAIL_CLOSED"),
        ("changed_failure_action", {"mandatory_actions": {**REQUIRED_ACTIONS, "site_batch_quality_process": "REPORT_ONLY"}}, "FAIL_CLOSED"),
        ("selected_random_bank", {"random_modules_per_seed": 20}, "FAIL_CLOSED"),
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
        "purpose": "Synthetic regression of V54 P1 negative-control declaration gate",
        "synthetic": True,
        "n_fixtures": len(rows),
        "n_pass": n_pass,
        "n_expected_process_pass": 1,
        "n_expected_fail_closed": 9,
        "n_controls": len(CONTROL_IDS),
        "overall_status": "PASS" if n_pass == len(rows) else "FAIL",
        "boundary": "Synthetic gate behavior only; no patient data, progression association, control result, or biological claim.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if summary["overall_status"] != "PASS":
        raise RuntimeError("V54 negative-control gate regression failed")
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
