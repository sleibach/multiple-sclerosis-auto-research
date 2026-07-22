#!/usr/bin/env python3
"""Fail-closed blind receipt gate for progression site/score calibration."""

from __future__ import annotations

import argparse
import csv
import json
import math
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_site_score_calibration_gate"
PLACEHOLDERS = {"", "unknown", "tbd", "todo", "placeholder", "na", "n/a"}
SCALE_STATUSES = {
    "single_site",
    "equivalent_across_sites",
    "different_across_sites",
    "unknown",
}
NORMALIZATION_ROUTES = {"global_fixed", "within_site_fixed"}
REQUIRED_TEXT = {
    "package_id",
    "protocol_source",
    "data_dictionary_source",
    "site_mapping_source",
    "platform_mapping_source",
    "score_definition_source",
    "normalization_plan_source",
    "scale_equivalence_evidence_source",
    "normalization_parameters_scope",
}
REQUIRED_TRUE = {
    "score_definition_frozen_before_score_access",
    "site_mapping_frozen_before_score_access",
    "normalization_route_frozen_before_score_access",
    "normalization_parameters_outcome_blind",
    "scale_diagnostics_outcome_blind",
}
REQUIRED_FALSE = {
    "scores_accessed_before_rule_freeze",
    "individual_outcomes_accessed_before_rule_freeze",
    "site_labels_inferred_after_outcome_access",
    "outcome_driven_site_merging",
    "outcome_driven_transform_selection",
    "outcome_driven_subject_exclusion",
}


def text_present(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() not in PLACEHOLDERS


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0]) if rows else []
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def validate(declaration: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []
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

    n_sites = declaration.get("n_sites")
    n_sites_valid = isinstance(n_sites, int) and not isinstance(n_sites, bool) and n_sites >= 1
    check("n_sites", "integer >= 1", n_sites_valid, n_sites)

    site_ids = declaration.get("site_ids")
    site_ids_valid = (
        isinstance(site_ids, list)
        and bool(site_ids)
        and all(text_present(item) for item in site_ids)
        and len(site_ids) == len(set(site_ids))
        and (not n_sites_valid or len(site_ids) == n_sites)
    )
    check("site_ids", "unique non-placeholder list matching n_sites", site_ids_valid, site_ids)
    expected_sites = set(site_ids) if site_ids_valid else set()

    def check_site_map(field: str, value_check: Any, expectation: str) -> dict[str, Any]:
        mapping = declaration.get(field)
        keys_valid = isinstance(mapping, dict) and set(mapping) == expected_sites and bool(expected_sites)
        values_valid = keys_valid and all(value_check(value) for value in mapping.values())
        check(field, expectation, bool(keys_valid and values_valid), mapping)
        return mapping if isinstance(mapping, dict) else {}

    sample_counts = check_site_map(
        "site_sample_counts",
        lambda value: isinstance(value, int) and not isinstance(value, bool) and value >= 2,
        "exact site map; integer counts >= 2",
    )
    score_counts = check_site_map(
        "site_score_available_counts",
        lambda value: isinstance(value, int) and not isinstance(value, bool) and value >= 2,
        "exact site map; score-available counts >= 2",
    )
    check_site_map("site_platforms", text_present, "exact site map; non-placeholder platform")
    check_site_map(
        "site_score_variances",
        lambda value: isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
        and float(value) > 0,
        "exact site map; finite positive blind score variance",
    )

    count_consistency = bool(expected_sites) and all(
        site in sample_counts
        and site in score_counts
        and isinstance(sample_counts[site], int)
        and isinstance(score_counts[site], int)
        and 2 <= score_counts[site] <= sample_counts[site]
        for site in expected_sites
    )
    check(
        "score_count_consistency",
        "2 <= score-available count <= sample count at every site",
        count_consistency,
        {"sample": sample_counts, "score_available": score_counts},
    )

    scale_status = declaration.get("assay_scale_status")
    check("assay_scale_status", "allowed frozen status", scale_status in SCALE_STATUSES, scale_status)
    route = declaration.get("normalization_route")
    check("normalization_route", "global_fixed|within_site_fixed", route in NORMALIZATION_ROUTES, route)

    multisite = bool(n_sites_valid and n_sites > 1)
    status_matches_sites = (n_sites == 1 and scale_status == "single_site") or (
        multisite and scale_status in {"equivalent_across_sites", "different_across_sites", "unknown"}
    )
    check(
        "scale_status_matches_site_count",
        "single_site iff n_sites=1; cross-site status otherwise",
        status_matches_sites,
        {"n_sites": n_sites, "assay_scale_status": scale_status},
    )

    if scale_status == "unknown":
        blockers.append("assay_scale_status:unknown_fails_closed")
    if multisite:
        for field in (
            "site_stratified_inference_prespecified",
            "minimum_site_event_gate_prespecified",
            "leave_site_out_transport_gate_prespecified",
            "site_heterogeneity_gate_prespecified",
        ):
            check(field, "true for every multisite route", declaration.get(field) is True, declaration.get(field))
    if scale_status == "different_across_sites" and route != "within_site_fixed":
        blockers.append("normalization_route:within_site_required_for_scale_difference")
    if route == "within_site_fixed":
        check(
            "all_score_available_subjects_used",
            "true for within-site parameter estimation",
            declaration.get("all_score_available_subjects_used") is True,
            declaration.get("all_score_available_subjects_used"),
        )
        scope_ok = declaration.get("normalization_parameters_scope") == (
            "all_score_available_within_predeclared_site"
        )
        check(
            "within_site_parameter_scope",
            "all_score_available_within_predeclared_site",
            scope_ok,
            declaration.get("normalization_parameters_scope"),
        )

    balanced_reference = False
    if multisite and count_consistency:
        counts = [sample_counts[site] for site in site_ids]
        balanced_reference = max(counts) - min(counts) <= 1
        if not balanced_reference:
            warnings.append(
                "site_allocation:outside_exact_balanced_reference;normalization_does_not_establish_transport"
            )
    transport_reference_status = (
        "NOT_APPLICABLE_SINGLE_SITE"
        if not multisite
        else "MATCHES_TESTED_BALANCED_REFERENCE"
        if balanced_reference
        else "OUTSIDE_TESTED_BALANCED_REFERENCE"
    )

    blockers = sorted(set(blockers))
    warnings = sorted(set(warnings))
    if blockers:
        decision = "FAIL_CLOSED"
    elif not multisite:
        decision = "PASS_SINGLE_SITE_FIXED_TRANSFORM"
    elif scale_status == "different_across_sites":
        decision = "PASS_MULTISITE_WITHIN_SITE_SCALE_REQUIRED"
    else:
        decision = "PASS_MULTISITE_EQUIVALENT_SCALE"

    output_dir.mkdir(parents=True, exist_ok=True)
    write_tsv(output_dir / "field_checks.tsv", checks)
    summary = {
        "purpose": "V54 blind progression site/score calibration receipt gate; no biological claim",
        "synthetic": declaration.get("synthetic") is True,
        "package_id": declaration.get("package_id", ""),
        "n_sites": n_sites,
        "assay_scale_status": scale_status,
        "normalization_route": route,
        "n_checks": len(checks),
        "n_blockers": len(blockers),
        "blockers": blockers,
        "n_warnings": len(warnings),
        "warnings": warnings,
        "decision": decision,
        "transport_reference_status": transport_reference_status,
        "boundary": (
            "A pass establishes blinded metadata and a frozen score-scaling route only. "
            "It does not establish score validity, site transport, progression association, "
            "MS biology, or therapeutic relevance."
        ),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def base_declaration() -> dict[str, Any]:
    sites = ["SITE_A", "SITE_B", "SITE_C"]
    return {
        "synthetic": True,
        "package_id": "SYNTHETIC_SITE_SCORE_PACKAGE_DO_NOT_USE_AS_DATA",
        "protocol_source": "SYNTHETIC_ONLY/protocol.txt",
        "data_dictionary_source": "SYNTHETIC_ONLY/data_dictionary.tsv",
        "site_mapping_source": "SYNTHETIC_ONLY/site_map.tsv",
        "platform_mapping_source": "SYNTHETIC_ONLY/platform_map.tsv",
        "score_definition_source": "SYNTHETIC_ONLY/frozen_score.txt",
        "normalization_plan_source": "SYNTHETIC_ONLY/normalization_plan.txt",
        "scale_equivalence_evidence_source": "SYNTHETIC_ONLY/blind_scale_diagnostics.tsv",
        "score_definition_frozen_before_score_access": True,
        "site_mapping_frozen_before_score_access": True,
        "normalization_route_frozen_before_score_access": True,
        "normalization_parameters_outcome_blind": True,
        "scale_diagnostics_outcome_blind": True,
        "scores_accessed_before_rule_freeze": False,
        "individual_outcomes_accessed_before_rule_freeze": False,
        "site_labels_inferred_after_outcome_access": False,
        "outcome_driven_site_merging": False,
        "outcome_driven_transform_selection": False,
        "outcome_driven_subject_exclusion": False,
        "n_sites": 3,
        "site_ids": sites,
        "site_sample_counts": {site: 150 for site in sites},
        "site_score_available_counts": {site: 135 for site in sites},
        "site_platforms": {"SITE_A": "platform_x", "SITE_B": "platform_y", "SITE_C": "platform_z"},
        "site_score_variances": {"SITE_A": 0.25, "SITE_B": 1.0, "SITE_C": 4.0},
        "assay_scale_status": "different_across_sites",
        "normalization_route": "within_site_fixed",
        "normalization_parameters_scope": "all_score_available_within_predeclared_site",
        "all_score_available_subjects_used": True,
        "site_stratified_inference_prespecified": True,
        "minimum_site_event_gate_prespecified": True,
        "leave_site_out_transport_gate_prespecified": True,
        "site_heterogeneity_gate_prespecified": True,
    }


def single_site_declaration() -> dict[str, Any]:
    declaration = base_declaration()
    declaration.update(
        {
            "n_sites": 1,
            "site_ids": ["SITE_A"],
            "site_sample_counts": {"SITE_A": 150},
            "site_score_available_counts": {"SITE_A": 135},
            "site_platforms": {"SITE_A": "platform_x"},
            "site_score_variances": {"SITE_A": 1.0},
            "assay_scale_status": "single_site",
            "normalization_route": "global_fixed",
            "normalization_parameters_scope": "all_score_available_single_predeclared_site",
            "all_score_available_subjects_used": True,
            "site_stratified_inference_prespecified": False,
            "minimum_site_event_gate_prespecified": False,
            "leave_site_out_transport_gate_prespecified": False,
            "site_heterogeneity_gate_prespecified": False,
        }
    )
    return declaration


def synthetic_regression(output_dir: Path) -> dict[str, Any]:
    equivalent = base_declaration()
    equivalent.update(
        {
            "site_platforms": {site: "platform_x" for site in equivalent["site_ids"]},
            "site_score_variances": {site: 1.0 for site in equivalent["site_ids"]},
            "assay_scale_status": "equivalent_across_sites",
            "normalization_route": "global_fixed",
            "normalization_parameters_scope": "all_score_available_across_predeclared_sites",
        }
    )
    imbalanced = base_declaration()
    imbalanced["site_sample_counts"] = {"SITE_A": 270, "SITE_B": 135, "SITE_C": 45}
    imbalanced["site_score_available_counts"] = {"SITE_A": 243, "SITE_B": 121, "SITE_C": 41}

    fixtures: list[tuple[str, dict[str, Any], str, str]] = [
        ("single_site_valid", single_site_declaration(), "PASS_SINGLE_SITE_FIXED_TRANSFORM", "NOT_APPLICABLE_SINGLE_SITE"),
        ("multisite_equivalent_global", equivalent, "PASS_MULTISITE_EQUIVALENT_SCALE", "MATCHES_TESTED_BALANCED_REFERENCE"),
        ("multisite_difference_within", base_declaration(), "PASS_MULTISITE_WITHIN_SITE_SCALE_REQUIRED", "MATCHES_TESTED_BALANCED_REFERENCE"),
        ("multisite_difference_global", {**base_declaration(), "normalization_route": "global_fixed", "normalization_parameters_scope": "all_score_available_across_predeclared_sites"}, "FAIL_CLOSED", "MATCHES_TESTED_BALANCED_REFERENCE"),
        ("unknown_scale", {**base_declaration(), "assay_scale_status": "unknown"}, "FAIL_CLOSED", "MATCHES_TESTED_BALANCED_REFERENCE"),
        ("score_unblinded_before_freeze", {**base_declaration(), "scores_accessed_before_rule_freeze": True}, "FAIL_CLOSED", "MATCHES_TESTED_BALANCED_REFERENCE"),
        ("missing_platform_mapping", base_declaration(), "FAIL_CLOSED", "MATCHES_TESTED_BALANCED_REFERENCE"),
        ("zero_site_variance", base_declaration(), "FAIL_CLOSED", "MATCHES_TESTED_BALANCED_REFERENCE"),
        ("outcome_selected_transform", {**base_declaration(), "outcome_driven_transform_selection": True}, "FAIL_CLOSED", "MATCHES_TESTED_BALANCED_REFERENCE"),
        ("imbalanced_but_blindly_harmonized", imbalanced, "PASS_MULTISITE_WITHIN_SITE_SCALE_REQUIRED", "OUTSIDE_TESTED_BALANCED_REFERENCE"),
    ]
    del fixtures[6][1]["site_platforms"]["SITE_C"]
    fixtures[7][1]["site_score_variances"]["SITE_C"] = 0.0

    rows: list[dict[str, Any]] = []
    fixture_dir = output_dir / "synthetic"
    for name, declaration, expected_decision, expected_transport in fixtures:
        declaration = deepcopy(declaration)
        declaration["package_id"] = f"SYNTHETIC_{name.upper()}_DO_NOT_USE_AS_DATA"
        path = fixture_dir / f"{name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(declaration, indent=2) + "\n")
        result = validate(declaration, output_dir / "runs" / name)
        passed = (
            result["decision"] == expected_decision
            and result["transport_reference_status"] == expected_transport
        )
        rows.append(
            {
                "fixture": name,
                "synthetic": True,
                "expected_decision": expected_decision,
                "observed_decision": result["decision"],
                "expected_transport_reference_status": expected_transport,
                "observed_transport_reference_status": result["transport_reference_status"],
                "n_blockers": result["n_blockers"],
                "n_warnings": result["n_warnings"],
                "regression_pass": passed,
            }
        )

    write_tsv(output_dir / "synthetic_regression.tsv", rows)
    n_pass = sum(bool(row["regression_pass"]) for row in rows)
    summary = {
        "purpose": "Synthetic regression of V54 blind site/score calibration receipt gate",
        "synthetic": True,
        "n_fixtures": len(rows),
        "n_pass": n_pass,
        "n_fail_closed_fixtures": sum(row["observed_decision"] == "FAIL_CLOSED" for row in rows),
        "overall_status": "PASS" if n_pass == len(rows) else "FAIL",
        "boundary": "Synthetic gate behavior only; no patient data, progression evidence, or biological claim.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if summary["overall_status"] != "PASS":
        raise RuntimeError("V54 site/score calibration gate regression failed")
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
