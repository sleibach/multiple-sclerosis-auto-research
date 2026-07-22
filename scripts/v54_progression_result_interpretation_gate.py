#!/usr/bin/env python3
"""Apply the frozen V54 P1 post-result interpretation classes."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_result_interpretation_gate"
PLACEHOLDERS = {"", "unknown", "tbd", "todo", "placeholder", "na", "n/a"}
FAVORABLE_DIRECTIONS = {"lower", "higher"}


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def valid_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(char in "0123456789abcdef" for char in value)


def classify(packet: dict[str, Any], output_dir: Path) -> dict[str, Any]:
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

    package_id = packet.get("package_id")
    check("package_id", "non-placeholder text", isinstance(package_id, str) and package_id.strip().lower() not in PLACEHOLDERS, package_id)
    check("synthetic", "explicit boolean", isinstance(packet.get("synthetic"), bool), packet.get("synthetic"))
    check("release_decision", "RELEASE_READY_FOR_FROZEN_ANALYSIS", packet.get("release_decision") == "RELEASE_READY_FOR_FROZEN_ANALYSIS", packet.get("release_decision"))
    check("release_package_id", "same package ID", packet.get("release_package_id") == package_id, packet.get("release_package_id"))
    frozen_hash = packet.get("frozen_plan_sha256")
    result_hash = packet.get("result_plan_sha256")
    plan_path_value = packet.get("frozen_plan_path")
    plan_path = Path(plan_path_value) if isinstance(plan_path_value, str) else Path("")
    if not plan_path.is_absolute():
        plan_path = ROOT / plan_path
    computed_hash = hashlib.sha256(plan_path.read_bytes()).hexdigest() if plan_path.is_file() else None
    check("frozen_plan_path", "existing file", isinstance(plan_path_value, str) and plan_path.is_file(), plan_path_value)
    check("frozen_plan_sha256", "SHA-256 of frozen plan file", valid_sha256(frozen_hash) and frozen_hash == computed_hash, frozen_hash)
    check("result_plan_sha256", "same lowercase SHA-256", valid_sha256(result_hash) and result_hash == frozen_hash, result_hash)
    check("frozen_before_score_access", "true", packet.get("frozen_before_score_access") is True, packet.get("frozen_before_score_access"))
    check("scores_accessed_before_freeze", "false", packet.get("scores_accessed_before_freeze") is False, packet.get("scores_accessed_before_freeze"))
    check("primary_analysis_executed_once", "true", packet.get("primary_analysis_executed_once") is True, packet.get("primary_analysis_executed_once"))
    check("alternate_primary_selected", "false", packet.get("alternate_primary_selected") is False, packet.get("alternate_primary_selected"))
    direction = packet.get("favorable_direction")
    check("favorable_direction", "lower or higher", direction in FAVORABLE_DIRECTIONS, direction)

    numeric_fields = ("estimate", "ci_lower", "ci_upper", "null_boundary", "minimum_material_effect")
    for field in numeric_fields:
        check(field, "finite number", finite_number(packet.get(field)), packet.get(field))
    event_floor = packet.get("predeclared_event_floor")
    events = packet.get("independent_progression_events")
    check("predeclared_event_floor", "integer >= 10", isinstance(event_floor, int) and not isinstance(event_floor, bool) and event_floor >= 10, event_floor)
    check("independent_progression_events", "nonnegative integer", isinstance(events, int) and not isinstance(events, bool) and events >= 0, events)

    boolean_fields = (
        "information_floor_met",
        "data_quality_resolved",
        "corrected_family_pass",
        "source_sensitivity_retains_direction",
        "batch_sensitivity_retains_direction",
        "composition_sensitivity_retains_direction",
        "influence_sensitivity_retains_direction",
        "calibration_controls_valid",
        "attendance_censoring_control_clean",
        "site_batch_quality_control_clean",
        "endpoint_specificity_controls_clean",
    )
    for field in boolean_fields:
        check(field, "explicit boolean", isinstance(packet.get(field), bool), packet.get(field))

    if not blockers:
        estimate = float(packet["estimate"])
        lower = float(packet["ci_lower"])
        upper = float(packet["ci_upper"])
        null = float(packet["null_boundary"])
        material = float(packet["minimum_material_effect"])
        check("confidence_interval_order", "lower <= estimate <= upper", lower <= estimate <= upper, [lower, estimate, upper])
        check("minimum_material_direction", "material boundary lies in favorable direction from null", (direction == "lower" and material < null) or (direction == "higher" and material > null), {"direction": direction, "material": material, "null": null})
        check("information_floor_consistency", "boolean equals events >= frozen floor", packet["information_floor_met"] == (events >= event_floor), {"declared": packet["information_floor_met"], "events": events, "floor": event_floor})

    blockers = sorted(set(blockers))
    if blockers:
        decision = "INVALID_INPUT_OR_PROVENANCE"
        decision_reason = "One or more identity, freeze, schema, numeric, or plan-binding checks failed."
    elif not packet["calibration_controls_valid"]:
        decision = "INVALID_CALIBRATION_CONTROL"
        decision_reason = "Blocked permutation or matched-random-module calibration failed."
    elif not packet["attendance_censoring_control_clean"]:
        decision = "INVALID_EVENT_TIME_PROCESS_CONTROL"
        decision_reason = "Attendance, confirmation, censoring, or death process control failed."
    elif not packet["site_batch_quality_control_clean"]:
        decision = "INVALID_TRANSPORT_OR_TECHNICAL_CONTROL"
        decision_reason = "Site, batch, platform, or quality process control failed."
    elif events < 10:
        decision = "INCONCLUSIVE_DESCRIPTIVE_ONLY"
        decision_reason = "Fewer than ten independent progression events."
    elif not packet["information_floor_met"]:
        decision = "INCONCLUSIVE_INFORMATION_FLOOR_NOT_MET"
        decision_reason = "The cohort-specific predeclared information floor was not met."
    elif not packet["data_quality_resolved"]:
        decision = "INCONCLUSIVE_DATA_QUALITY"
        decision_reason = "A mandatory data-quality sensitivity remains unresolved."
    else:
        estimate = float(packet["estimate"])
        lower = float(packet["ci_lower"])
        upper = float(packet["ci_upper"])
        null = float(packet["null_boundary"])
        material = float(packet["minimum_material_effect"])
        wrong_direction = estimate > null if direction == "lower" else estimate < null
        null_excluded_favorably = upper < null if direction == "lower" else lower > null
        material_compatible = lower <= material if direction == "lower" else upper >= material
        spans_null_and_material = (lower <= material and upper >= null) if direction == "lower" else (lower <= null and upper >= material)
        sensitivities_retain = all(
            packet[field]
            for field in (
                "source_sensitivity_retains_direction",
                "batch_sensitivity_retains_direction",
                "composition_sensitivity_retains_direction",
                "influence_sensitivity_retains_direction",
            )
        )
        if wrong_direction:
            decision = "FAIL_WRONG_DIRECTION"
            decision_reason = "The primary estimate is opposite the frozen favorable direction."
        elif not material_compatible:
            decision = "FAIL_MINIMUM_MATERIAL_EFFECT_EXCLUDED"
            decision_reason = "The interval excludes the frozen minimum material effect in the favorable direction."
        elif spans_null_and_material:
            decision = "INCONCLUSIVE_INTERVAL_SPANS_NULL_AND_MATERIAL"
            decision_reason = "The interval includes both the frozen null and minimum material boundaries."
        elif not packet["corrected_family_pass"] or not null_excluded_favorably or not sensitivities_retain:
            decision = "INCONCLUSIVE_PRIMARY_CRITERIA_NOT_ALL_MET"
            decision_reason = "The corrected family, favorable null exclusion, and mandatory direction-retention criteria did not all pass."
        elif not packet["endpoint_specificity_controls_clean"]:
            decision = "PASS_WITH_PROGRESSION_SPECIFICITY_DOWNGRADE"
            decision_reason = "Primary bounded criteria pass, but a transient, relapse-associated, or pre-index specificity control is positive."
        else:
            decision = "PASS_BOUNDED_ASSOCIATION"
            decision_reason = "All frozen primary, uncertainty, sensitivity, and process-control criteria pass."

    if decision.startswith("PASS"):
        authority = "Bounded predictive-association transport under the declared design only; not mechanism, target, treatment effect, efficacy, or evidence of halting progression."
    elif decision.startswith("FAIL"):
        authority = "Rejects transport of the frozen state under the declared design; does not prove progression biology absent."
    elif decision.startswith("INCONCLUSIVE"):
        authority = "Only the effect estimate and interval may inform future design; no confirmatory biological interpretation."
    else:
        authority = "No biological interpretation is permitted."

    output_dir.mkdir(parents=True, exist_ok=True)
    write_tsv(output_dir / "field_checks.tsv", checks)
    summary = {
        "purpose": "V54 P1 post-result interpretation composition; no biological claim",
        "synthetic": packet.get("synthetic") is True,
        "package_id": package_id or "",
        "n_blockers": len(blockers),
        "blockers": blockers,
        "decision": decision,
        "decision_reason": decision_reason,
        "authority": authority,
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def base_packet(plan_path: Path, plan_hash: str) -> dict[str, Any]:
    return {
        "synthetic": True,
        "package_id": "SYNTHETIC_RESULT_PACKAGE_DO_NOT_USE_AS_DATA",
        "release_decision": "RELEASE_READY_FOR_FROZEN_ANALYSIS",
        "release_package_id": "SYNTHETIC_RESULT_PACKAGE_DO_NOT_USE_AS_DATA",
        "frozen_plan_path": str(plan_path.relative_to(ROOT)),
        "frozen_plan_sha256": plan_hash,
        "result_plan_sha256": plan_hash,
        "frozen_before_score_access": True,
        "scores_accessed_before_freeze": False,
        "primary_analysis_executed_once": True,
        "alternate_primary_selected": False,
        "favorable_direction": "lower",
        "estimate": 0.75,
        "ci_lower": 0.68,
        "ci_upper": 0.88,
        "null_boundary": 1.0,
        "minimum_material_effect": 0.80,
        "predeclared_event_floor": 50,
        "independent_progression_events": 75,
        "information_floor_met": True,
        "data_quality_resolved": True,
        "corrected_family_pass": True,
        "source_sensitivity_retains_direction": True,
        "batch_sensitivity_retains_direction": True,
        "composition_sensitivity_retains_direction": True,
        "influence_sensitivity_retains_direction": True,
        "calibration_controls_valid": True,
        "attendance_censoring_control_clean": True,
        "site_batch_quality_control_clean": True,
        "endpoint_specificity_controls_clean": True,
    }


def synthetic_regression(output_dir: Path) -> dict[str, Any]:
    plan_path = output_dir / "synthetic" / "frozen_plan.json"
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(json.dumps({"synthetic": True, "purpose": "V54 frozen-plan hash fixture; no biological data"}, indent=2) + "\n")
    plan_hash = hashlib.sha256(plan_path.read_bytes()).hexdigest()
    bad_hash = "0" * 64
    cases = [
        ("pass_lower", {}, "PASS_BOUNDED_ASSOCIATION"),
        ("pass_higher", {"favorable_direction": "higher", "estimate": 1.30, "ci_lower": 1.12, "ci_upper": 1.42, "minimum_material_effect": 1.20}, "PASS_BOUNDED_ASSOCIATION"),
        ("pass_specificity_downgrade", {"endpoint_specificity_controls_clean": False}, "PASS_WITH_PROGRESSION_SPECIFICITY_DOWNGRADE"),
        ("fail_wrong_direction", {"estimate": 1.10, "ci_lower": 0.98, "ci_upper": 1.20}, "FAIL_WRONG_DIRECTION"),
        ("fail_material_excluded", {"estimate": 0.94, "ci_lower": 0.90, "ci_upper": 0.98}, "FAIL_MINIMUM_MATERIAL_EFFECT_EXCLUDED"),
        ("inconclusive_spans_both", {"estimate": 0.90, "ci_lower": 0.75, "ci_upper": 1.05}, "INCONCLUSIVE_INTERVAL_SPANS_NULL_AND_MATERIAL"),
        ("inconclusive_exact_null", {"estimate": 1.0, "ci_lower": 0.75, "ci_upper": 1.10}, "INCONCLUSIVE_INTERVAL_SPANS_NULL_AND_MATERIAL"),
        ("inconclusive_descriptive", {"independent_progression_events": 8, "information_floor_met": False}, "INCONCLUSIVE_DESCRIPTIVE_ONLY"),
        ("inconclusive_information", {"independent_progression_events": 40, "information_floor_met": False}, "INCONCLUSIVE_INFORMATION_FLOOR_NOT_MET"),
        ("inconclusive_quality", {"data_quality_resolved": False}, "INCONCLUSIVE_DATA_QUALITY"),
        ("inconclusive_family", {"corrected_family_pass": False}, "INCONCLUSIVE_PRIMARY_CRITERIA_NOT_ALL_MET"),
        ("inconclusive_sensitivity", {"influence_sensitivity_retains_direction": False}, "INCONCLUSIVE_PRIMARY_CRITERIA_NOT_ALL_MET"),
        ("invalid_calibration", {"calibration_controls_valid": False}, "INVALID_CALIBRATION_CONTROL"),
        ("invalid_attendance", {"attendance_censoring_control_clean": False}, "INVALID_EVENT_TIME_PROCESS_CONTROL"),
        ("invalid_site_batch", {"site_batch_quality_control_clean": False}, "INVALID_TRANSPORT_OR_TECHNICAL_CONTROL"),
        ("invalid_plan_hash", {"result_plan_sha256": bad_hash}, "INVALID_INPUT_OR_PROVENANCE"),
        ("invalid_not_released", {"release_decision": "CONTINUE_BLINDED_ACCRUAL"}, "INVALID_INPUT_OR_PROVENANCE"),
    ]
    rows: list[dict[str, Any]] = []
    for name, edits, expected in cases:
        packet = base_packet(plan_path, plan_hash)
        packet.update(deepcopy(edits))
        packet["package_id"] = f"SYNTHETIC_{name.upper()}_DO_NOT_USE_AS_DATA"
        packet["release_package_id"] = packet["package_id"]
        fixture = output_dir / "synthetic" / f"{name}.json"
        fixture.parent.mkdir(parents=True, exist_ok=True)
        fixture.write_text(json.dumps(packet, indent=2) + "\n")
        result = classify(packet, output_dir / "runs" / name)
        rows.append(
            {
                "fixture": name,
                "synthetic": True,
                "expected_decision": expected,
                "observed_decision": result["decision"],
                "regression_pass": result["decision"] == expected,
            }
        )
    write_tsv(output_dir / "synthetic_regression.tsv", rows)
    n_pass = sum(item["regression_pass"] for item in rows)
    summary = {
        "purpose": "Synthetic regression of V54 P1 post-result interpretation gate",
        "synthetic": True,
        "n_fixtures": len(rows),
        "n_pass": n_pass,
        "n_bounded_pass": sum(item["observed_decision"] == "PASS_BOUNDED_ASSOCIATION" for item in rows),
        "n_specificity_downgrade": sum(item["observed_decision"] == "PASS_WITH_PROGRESSION_SPECIFICITY_DOWNGRADE" for item in rows),
        "n_fail": sum(item["observed_decision"].startswith("FAIL") for item in rows),
        "n_inconclusive": sum(item["observed_decision"].startswith("INCONCLUSIVE") for item in rows),
        "n_invalid": sum(item["observed_decision"].startswith("INVALID") for item in rows),
        "overall_status": "PASS" if n_pass == len(rows) else "FAIL",
        "boundary": "Synthetic method behavior only; no patient data, progression association, mechanism, target, treatment effect, or efficacy evidence.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if summary["overall_status"] != "PASS":
        raise RuntimeError("V54 result interpretation regression failed")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--fail-on-invalid", action="store_true")
    args = parser.parse_args()
    if args.packet:
        result = classify(json.loads(args.packet.read_text()), args.output_dir)
        print(json.dumps(result, indent=2))
        if args.fail_on_invalid and result["decision"].startswith("INVALID"):
            raise SystemExit(1)
    else:
        print(json.dumps(synthetic_regression(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
