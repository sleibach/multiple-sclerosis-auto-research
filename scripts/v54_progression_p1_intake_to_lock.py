#!/usr/bin/env python3
"""Compose V54 blind P1 gates into a synthetic intake-to-lock state machine."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import v54_progression_blinded_feasibility as feasibility
import v54_progression_combined_intake_gate as intake
import v54_progression_event_time_assumption_gate as event_time
import v54_progression_information_monitor as information
import v54_progression_nonlinear_diagnostic_gate as nonlinear
import v54_progression_outcome_semantic_checker as semantic
import v54_progression_site_score_calibration_gate as site_score
import v54_progression_treatment_switch_gate as treatment_switch


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_p1_intake_to_lock"
PASS_DECISIONS = {
    "intake": {"PASS_BLINDED_PROGRESSION_INTAKE"},
    "event_time": {"PASS_STANDARD_PLUS_DIAGNOSTICS", "PASS_SENSITIVITY_REQUIRED"},
    "site_score": {
        "PASS_SINGLE_SITE_FIXED_TRANSFORM",
        "PASS_MULTISITE_EQUIVALENT_SCALE",
        "PASS_MULTISITE_WITHIN_SITE_SCALE_REQUIRED",
    },
    "treatment_switch": {
        "PASS_SWITCH_SENSITIVITY_REQUIRED",
        "PASS_NO_OBSERVED_SWITCH_DUAL_PLAN",
    },
    "nonlinear": {"PASS_FIXED_NONLINEAR_DIAGNOSTIC_FAMILY"},
    "feasibility": {
        "REFERENCE_ALIGNED_FOR_COHORT_SPECIFIC_POWER",
        "REFERENCE_ALIGNED_SENSITIVITY_REQUIRED",
    },
}


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def stage_summary(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def run_case(name: str, edits: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    case_root = output_dir / "runs" / name
    package_id = f"SYNTHETIC_P1_{name.upper()}_DO_NOT_USE_AS_DATA"
    source = case_root / "inputs" / "SYNTHETIC_ONLY.tsv"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("synthetic\tvalue\nmethod_behavior_only\t1\n")

    inventory_path = case_root / "inputs" / "inventory.tsv"
    missing = {"progression_event"} if edits.get("intake_fail") else set()
    intake.make_inventory(inventory_path, relative(source), missing)
    semantic_values = semantic.base_fixture("P1", "pira")
    semantic_values["package_id"] = package_id
    declaration_path = case_root / "inputs" / "endpoint_declaration.tsv"
    semantic.write_fixture(declaration_path, semantic_values)
    intake_result = intake.run_gate(
        inventory_path=inventory_path,
        declaration_path=declaration_path,
        package_id=package_id,
        role="P1",
        endpoint_mode="pira",
        output_dir=case_root / "stages" / "intake",
        synthetic=True,
        enforce_source_paths=True,
    )

    event_declaration = event_time.base_declaration()
    event_declaration["package_id"] = package_id
    if edits.get("event_fail"):
        event_declaration.update(
            {
                "nonadministrative_censoring_present": "yes",
                "unknown_censoring_reasons_present": "yes",
            }
        )
    event_result = event_time.validate(event_declaration, case_root / "stages" / "event_time")

    site_declaration = site_score.base_declaration()
    site_declaration["package_id"] = package_id
    if edits.get("site_fail"):
        site_declaration["assay_scale_status"] = "unknown"
    site_result = site_score.validate(site_declaration, case_root / "stages" / "site_score")

    switch_declaration = treatment_switch.base_declaration()
    switch_declaration["package_id"] = package_id
    if edits.get("switch_fail"):
        switch_declaration["unknown_switch_reasons_present"] = "yes"
    switch_result = treatment_switch.validate(
        switch_declaration, case_root / "stages" / "treatment_switch"
    )

    nonlinear_declaration = nonlinear.base_declaration()
    nonlinear_declaration["package_id"] = (
        "SYNTHETIC_DIFFERENT_PACKAGE"
        if edits.get("cross_stage_package_mismatch")
        else package_id
    )
    if edits.get("nonlinear_fail"):
        nonlinear_declaration["diagnostic_can_reinterpret_failed_primary"] = True
    nonlinear_result = nonlinear.validate(
        nonlinear_declaration, case_root / "stages" / "nonlinear"
    )

    upstream_paths = {
        "combined_intake": relative(case_root / "stages" / "intake" / "summary.json"),
        "event_time": relative(case_root / "stages" / "event_time" / "summary.json"),
        "site_score": relative(case_root / "stages" / "site_score" / "summary.json"),
    }
    if edits.get("feasibility_summary_mismatch"):
        event_path = ROOT / upstream_paths["event_time"]
        altered = stage_summary(event_path)
        altered["package_id"] = "SYNTHETIC_DIFFERENT_PACKAGE"
        event_path.write_text(json.dumps(altered, indent=2) + "\n")
        event_result = altered
    feasibility_declaration = feasibility.base_declaration(package_id, upstream_paths)
    feasibility_result = feasibility.validate(
        feasibility_declaration, case_root / "stages" / "feasibility"
    )

    plan = information.base_plan(package_id)
    snapshot = information.base_snapshot(package_id)
    if edits.get("continue_accrual"):
        snapshot.update(
            {
                "site_analyzable_counts": {"SITE_A": 100, "SITE_B": 100, "SITE_C": 100},
                "site_confirmed_event_counts": {"SITE_A": 25, "SITE_B": 25, "SITE_C": 25},
                "completed_visit_count": 3000,
                "pending_confirmation_count": 12,
                "followup_complete": False,
            }
        )
    if edits.get("forbidden_information"):
        snapshot["p_value"] = 0.001
    information_result = information.validate(
        plan, snapshot, case_root / "stages" / "information"
    )

    stages = {
        "intake": intake_result,
        "event_time": event_result,
        "site_score": site_result,
        "treatment_switch": switch_result,
        "nonlinear": nonlinear_result,
        "feasibility": feasibility_result,
        "information": information_result,
    }
    rows: list[dict[str, Any]] = []
    blockers: list[str] = []
    for stage, summary in stages.items():
        observed_package = summary.get("package_id")
        bound = observed_package == package_id
        decision = summary.get("decision")
        if stage in PASS_DECISIONS and decision not in PASS_DECISIONS[stage]:
            blockers.append(f"{stage}:decision:{decision}")
        if not bound:
            blockers.append(f"{stage}:package_id_mismatch")
        if summary.get("synthetic") is not True:
            blockers.append(f"{stage}:synthetic_status_mismatch")
        rows.append(
            {
                "stage": stage,
                "package_id": observed_package,
                "package_bound": bound,
                "decision": decision,
                "synthetic": summary.get("synthetic"),
            }
        )

    information_decision = information_result.get("decision")
    if information_decision == "FAIL_CLOSED_PEEKING_OR_METADATA":
        blockers.append(f"information:decision:{information_decision}")
    blockers = sorted(set(blockers))
    if blockers:
        final_decision = "FAIL_CLOSED"
    elif information_decision == "REFERENCE_INFORMATION_REACHED_LOCK_AND_HANDOFF":
        final_decision = "LOCK_READY_FOR_FROZEN_ANALYSIS"
    elif information_decision == "HOLD_UNRESOLVED_CENSORING_METADATA":
        final_decision = "HOLD_UNRESOLVED_METADATA"
    else:
        final_decision = "CONTINUE_BLINDED_ACCRUAL"

    write_tsv(case_root / "stage_bindings.tsv", rows)
    summary = {
        "purpose": "V54 synthetic P1 intake-to-lock composition; no biological claim",
        "synthetic": True,
        "package_id": package_id,
        "n_stages": len(stages),
        "n_blockers": len(blockers),
        "blockers": blockers,
        "information_decision": information_decision,
        "decision": final_decision,
        "boundary": "Synthetic package-routing behavior only; lock readiness is not validation, efficacy, progression evidence, or MS biology.",
    }
    (case_root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def synthetic_regression(output_dir: Path = DEFAULT_OUT) -> dict[str, Any]:
    cases = [
        ("reference_lock", {}, "LOCK_READY_FOR_FROZEN_ANALYSIS"),
        ("continue_accrual", {"continue_accrual": True}, "CONTINUE_BLINDED_ACCRUAL"),
        ("intake_failure", {"intake_fail": True}, "FAIL_CLOSED"),
        ("unknown_censoring", {"event_fail": True}, "FAIL_CLOSED"),
        ("unknown_site_scale", {"site_fail": True}, "FAIL_CLOSED"),
        ("unknown_switch_reason", {"switch_fail": True}, "FAIL_CLOSED"),
        ("diagnostic_rescue", {"nonlinear_fail": True}, "FAIL_CLOSED"),
        ("feasibility_summary_mismatch", {"feasibility_summary_mismatch": True}, "FAIL_CLOSED"),
        ("forbidden_efficacy_field", {"forbidden_information": True}, "FAIL_CLOSED"),
        ("cross_stage_package_mismatch", {"cross_stage_package_mismatch": True}, "FAIL_CLOSED"),
    ]
    rows: list[dict[str, Any]] = []
    for name, edits, expected in cases:
        result = run_case(name, deepcopy(edits), output_dir)
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
        "purpose": "Synthetic regression of V54 P1 intake-to-lock composition",
        "synthetic": True,
        "n_fixtures": len(rows),
        "n_pass": n_pass,
        "n_lock_ready": sum(row["observed_decision"] == "LOCK_READY_FOR_FROZEN_ANALYSIS" for row in rows),
        "n_continue_accrual": sum(row["observed_decision"] == "CONTINUE_BLINDED_ACCRUAL" for row in rows),
        "n_fail_closed": sum(row["observed_decision"] == "FAIL_CLOSED" for row in rows),
        "overall_status": "PASS" if n_pass == len(rows) else "FAIL",
        "boundary": "Synthetic composition behavior only; no patient data, validation result, treatment effect, progression evidence, or biological claim.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if summary["overall_status"] != "PASS":
        raise RuntimeError("V54 P1 intake-to-lock composition regression failed")
    return summary


if __name__ == "__main__":
    print(json.dumps(synthetic_regression(), indent=2))
