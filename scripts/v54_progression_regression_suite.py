#!/usr/bin/env python3
"""Run the fast V54 progression gates and assert durable claim boundaries."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_regression_suite"


def run(name: str, arguments: list[str], timeout: int = 240) -> dict[str, Any]:
    started = time.monotonic()
    completed = subprocess.run(
        arguments,
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return {
        "check": name,
        "command": " ".join(arguments),
        "returncode": completed.returncode,
        "duration_seconds": round(time.monotonic() - started, 3),
        "pass": completed.returncode == 0,
        "stdout_tail": completed.stdout[-800:].replace("\n", " ").strip(),
        "stderr_tail": completed.stderr[-800:].replace("\n", " ").strip(),
    }


def get_path(document: Any, dotted: str) -> Any:
    current = document
    for part in dotted.split("."):
        if isinstance(current, list):
            current = current[int(part)]
        else:
            current = current[part]
    return current


def invariant(
    artifact: str,
    key: str,
    operator: str,
    expected: Any,
) -> dict[str, Any]:
    path = ROOT / artifact
    if not path.exists():
        return {
            "artifact": artifact,
            "key": key,
            "operator": operator,
            "expected": json.dumps(expected),
            "observed": "MISSING_ARTIFACT",
            "pass": False,
        }
    observed = get_path(json.loads(path.read_text()), key)
    if operator == "eq":
        passed = observed == expected
    elif operator == "contains":
        passed = expected in observed
    elif operator == "gt":
        passed = observed > expected
    else:
        raise ValueError(f"Unknown invariant operator: {operator}")
    return {
        "artifact": artifact,
        "key": key,
        "operator": operator,
        "expected": json.dumps(expected, sort_keys=True),
        "observed": json.dumps(observed, sort_keys=True),
        "pass": passed,
    }


def repository_guards() -> list[dict[str, Any]]:
    tracked = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
    ).stdout.split(b"\0")
    paths = [item.decode() for item in tracked if item]
    oversized = [
        path for path in paths if (ROOT / path).is_file() and (ROOT / path).stat().st_size > 50 * 1024 * 1024
    ]
    tmp_paths = [path for path in paths if "/tmp/" in f"/{path}"]
    return [
        {
            "check": "tracked_file_size_guard",
            "command": "internal git ls-files + stat",
            "returncode": 0 if not oversized else 1,
            "duration_seconds": 0.0,
            "pass": not oversized,
            "stdout_tail": ";".join(oversized),
            "stderr_tail": "",
        },
        {
            "check": "tracked_tmp_path_guard",
            "command": "internal git ls-files path audit",
            "returncode": 0 if not tmp_paths else 1,
            "duration_seconds": 0.0,
            "pass": not tmp_paths,
            "stdout_tail": ";".join(tmp_paths),
            "stderr_tail": "",
        },
    ]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # Keep the virtualenv entry point. Resolving its symlink discards the
    # environment's site-packages for child processes on this installation.
    python = sys.executable
    scripts = sorted(str(path.relative_to(ROOT)) for path in (ROOT / "scripts").glob("v54*.py"))
    checks = [
        run("python_compile", [python, "-m", "py_compile", *scripts]),
        run("package_inventory_regression", [python, "scripts/v54_progression_package_eligibility_validator.py"]),
        run("endpoint_semantic_regression", [python, "scripts/v54_progression_outcome_semantic_checker.py"]),
        run("combined_intake_regression", [python, "scripts/v54_progression_combined_intake_gate.py"]),
        run("p1_intake_to_lock_regression", [python, "scripts/v54_progression_p1_intake_to_lock.py"]),
        run("endpoint_adjudication_regression", [python, "scripts/v54_progression_endpoint_adjudication.py"]),
        run("event_time_receipt_regression", [python, "scripts/v54_progression_event_time_assumption_gate.py"]),
        run("site_score_calibration_regression", [python, "scripts/v54_progression_site_score_calibration_gate.py"]),
        run("blinded_feasibility_regression", [python, "scripts/v54_progression_blinded_feasibility.py"]),
        run("information_monitor_regression", [python, "scripts/v54_progression_information_monitor.py"]),
        run("treatment_switch_gate_regression", [python, "scripts/v54_progression_treatment_switch_gate.py"]),
        run("nonlinear_diagnostic_gate_regression", [python, "scripts/v54_progression_nonlinear_diagnostic_gate.py"]),
        run("p2_composition_regression", [python, "scripts/v54_progression_p2_composition_gate.py"]),
        run("candidate_role_matrix", [python, "scripts/v54_progression_candidate_role_matrix.py"]),
        run("cox_reference", [python, "scripts/v54_event_time_score_reference_check.py"]),
        run("event_assumption_reference", [python, "scripts/v54_event_time_assumption_reference_check.py"]),
        run("p2_ols_reference", [python, "scripts/v54_p2_interaction_reference_check.py"]),
        run("visit_schedule_breslow_reference", [python, "scripts/v54_visit_schedule_breslow_reference_check.py"]),
        run("multisite_cox_reference", [python, "scripts/v54_multisite_cox_reference_check.py"]),
        run("prospective_design_synthesis", [python, "scripts/v54_progression_design_synthesis.py"]),
        run("reference_manifest_verify", [python, "scripts/v54_progression_reference_manifest.py", "--verify"]),
        run("acquisition_voi_synthesis", [python, "scripts/v54_progression_acquisition_voi.py"]),
        run("provenance_gate", [python, "scripts/v47_provenance_gate.py", "audit", "--fail-on-error"]),
        run("structural_gate", [python, "scripts/v51_structural_prediction_gate.py", "audit", "--fail-on-error"]),
        run("whitespace_guard", ["git", "diff", "--check"]),
    ]
    checks.extend(repository_guards())

    specifications = [
        ("analysis/v54_progressive_stage_modules/summary.json", "n_supported_modules", "eq", 0),
        ("analysis/v54_progression_lesion_state/summary.json", "n_orthogonally_consistent_needs_data", "eq", 0),
        ("analysis/v54_transition_identifiability/summary.json", "n_transition_identifiable", "eq", 0),
        ("analysis/v54_progression_intervention_direction_map/summary.json", "n_target_revisit", "eq", 0),
        ("analysis/v54_progression_intervention_direction_map/summary.json", "alphafold_context_used", "eq", False),
        ("analysis/v54_multilineage_progression_review/summary.json", "objections_changing_progression_or_target_verdict", "eq", 0),
        ("analysis/v54_post_result_morphology_multiplicity/summary.json", "fully_adjusted_lysosomal_specificity_retained", "eq", False),
        ("analysis/v54_post_result_morphology_multiplicity/summary.json", "mutually_adjusted_two_endpoint_state_retained", "eq", False),
        ("analysis/v54_foamy_donor_estimand_audit/summary.json", "supported_within_donor_endpoints", "eq", []),
        ("analysis/v54_progression_p2_interaction_power/summary.json", "verdict", "eq", "P2_ROUTE_CONDITIONALLY_READY_REQUIRES_HIGH_FIDELITY_COMPOSITION"),
        ("analysis/v54_progression_p2_interaction_power/summary.json", "calibration_families.2.maximum", "gt", 0.20),
        ("analysis/v54_progression_event_time_assumption_robustness/summary.json", "invalid_censoring_mechanisms", "contains", "joint_score_event_risk"),
        ("analysis/v54_progression_combined_ascertainment/summary.json", "n_unique_simulated_cohorts", "eq", 288000),
        ("analysis/v54_progression_combined_ascertainment/summary.json", "n_route_evaluations", "eq", 576000),
        ("analysis/v54_progression_combined_ascertainment/summary.json", "n_compounded_invalidity_families", "eq", 1),
        ("analysis/v54_progression_combined_ascertainment_confirmation/summary.json", "n_unique_simulated_cohorts", "eq", 144000),
        ("analysis/v54_progression_combined_ascertainment_confirmation/summary.json", "all_constituent_families_calibrated", "eq", False),
        ("analysis/v54_progression_combined_ascertainment_confirmation/summary.json", "invalid_constituent_families", "contains", "attendance_weak_joint"),
        ("analysis/v54_progression_combined_ascertainment_confirmation/summary.json", "combined_family_invalid", "eq", True),
        ("analysis/v54_progression_combined_ascertainment_confirmation/summary.json", "compounded_invalidity_independently_confirmed", "eq", False),
        ("analysis/v54_progression_combined_ascertainment_confirmation/summary.json", "verdict", "eq", "JOINT_SCORE_RISK_COMPONENT_AND_STACK_UNSAFE_NOT_UNIQUE_COMPOUNDING"),
        ("analysis/v54_progression_competing_risk_robustness/summary.json", "n_unique_simulated_cohorts", "eq", 129600),
        ("analysis/v54_progression_competing_risk_robustness/summary.json", "strict_cell_flag_but_family_compatible_mechanisms", "contains", "independent"),
        ("analysis/v54_progression_competing_risk_robustness/summary.json", "invalid_competing_event_mechanisms", "contains", "joint_score_progression_risk"),
        ("analysis/v54_progression_visit_schedule_robustness/summary.json", "n_unique_simulated_cohorts", "eq", 172800),
        ("analysis/v54_progression_visit_schedule_robustness/summary.json", "invalid_observed_route_mechanisms", "contains", "detected_visit_time|score_dependent_20pct"),
        ("analysis/v54_progression_visit_schedule_robustness/summary.json", "invalid_observed_route_mechanisms", "contains", "detected_visit_time|joint_score_progression_risk_20pct"),
        ("analysis/v54_progression_visit_schedule_robustness/reference_check/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_repeated_score_reliability/summary.json", "n_unique_simulated_cohorts", "eq", 216000),
        ("analysis/v54_progression_repeated_score_reliability/summary.json", "invalid_measurement_plans", "eq", []),
        ("analysis/v54_progression_repeated_score_reliability/summary.json", "n_materially_useful_repeat_cells", "eq", 16),
        ("analysis/v54_progression_repeated_score_reliability/summary.json", "verdict", "eq", "REPEATS_HELP_ONLY_WHEN_ERROR_IS_SUFFICIENTLY_INDEPENDENT_AND_BASE_RELIABILITY_IS_LOW"),
        ("analysis/v54_progression_multisite_transportability/summary.json", "n_unique_simulated_cohorts", "eq", 115200),
        ("analysis/v54_progression_multisite_transportability/summary.json", "n_pooled_invalid_null_families", "eq", 2),
        ("analysis/v54_progression_multisite_transportability/summary.json", "n_stratified_invalid_null_families", "eq", 0),
        ("analysis/v54_progression_multisite_transportability/summary.json", "n_transport_ready_designs", "eq", 2),
        ("analysis/v54_progression_multisite_transportability/reference_check/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_design_synthesis/summary.json", "n_requirements", "eq", 16),
        ("analysis/v54_progression_design_synthesis/summary.json", "reference_total_n", "eq", 450),
        ("analysis/v54_progression_design_synthesis/summary.json", "current_known_p1_eligible_cohorts", "eq", 0),
        ("analysis/v54_progression_design_synthesis/summary.json", "verdict", "eq", "REFERENCE_DESIGN_SPECIFIED_BUT_NO_CURRENT_COHORT_ELIGIBLE"),
        ("analysis/v54_progression_reference_manifest/summary.json", "n_gates", "eq", 8),
        ("analysis/v54_progression_reference_manifest/summary.json", "n_bound_sources", "eq", 18),
        ("analysis/v54_progression_reference_manifest/summary.json", "n_current_blockers", "eq", 0),
        ("analysis/v54_progression_reference_manifest/summary.json", "n_synthetic_fixtures", "eq", 2),
        ("analysis/v54_progression_reference_manifest/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_acquisition_voi/summary.json", "n_bundles", "eq", 9),
        ("analysis/v54_progression_acquisition_voi/summary.json", "n_immediate_bundles", "eq", 5),
        ("analysis/v54_progression_acquisition_voi/summary.json", "top_priority", "eq", "p1_longitudinal_disability_link"),
        ("analysis/v54_progression_acquisition_voi/summary.json", "current_p1_eligible", "eq", 0),
        ("analysis/v54_progression_acquisition_voi/summary.json", "current_p2_eligible", "eq", 0),
        ("analysis/v54_progression_acquisition_voi/summary.json", "verdict", "eq", "ACQUIRE_P1_LONGITUDINAL_CORE_AND_ASCERTAINMENT_PROVENANCE_FIRST"),
        ("analysis/v54_progression_site_score_harmonization/summary.json", "n_unique_simulated_cohorts", "eq", 129600),
        ("analysis/v54_progression_site_score_harmonization/summary.json", "n_invalid_null_families", "eq", 0),
        ("analysis/v54_progression_site_score_harmonization/summary.json", "n_material_harmonization_gains", "eq", 6),
        ("analysis/v54_progression_site_score_harmonization/summary.json", "verdict", "eq", "WITHIN_SITE_SCALING_IS_REQUIRED_WHEN_ASSAY_SCALES_DIFFER"),
        ("analysis/v54_progression_site_score_calibration_gate/summary.json", "n_fixtures", "eq", 10),
        ("analysis/v54_progression_site_score_calibration_gate/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_enrollment_inflation/summary.json", "n_synthetic_cohort_replicates", "eq", 122805000),
        ("analysis/v54_progression_enrollment_inflation/summary.json", "reference_scenario.gross_total", "eq", 690),
        ("analysis/v54_progression_enrollment_inflation/summary.json", "severe_loss_scenario.gross_total", "eq", 990),
        ("analysis/v54_progression_enrollment_inflation/summary.json", "low_event_scenario.gross_total", "eq", 1380),
        ("analysis/v54_progression_enrollment_inflation/summary.json", "verdict", "eq", "CONDITIONAL_ENROLLMENT_LOOKUP_COMPLETE_NO_UNIVERSAL_N"),
        ("analysis/v54_progression_weaker_effect_power/summary.json", "n_unique_simulated_cohorts", "eq", 90000),
        ("analysis/v54_progression_weaker_effect_power/summary.json", "null_family_calibrated", "eq", True),
        ("analysis/v54_progression_weaker_effect_power/summary.json", "n_nonnull_scenarios", "eq", 8),
        ("analysis/v54_progression_weaker_effect_power/summary.json", "n_scenarios_reaching_rule", "eq", 6),
        ("analysis/v54_progression_weaker_effect_power/summary.json", "minimum_n_by_scenario.event_030_hr_12", "eq", "not_reached"),
        ("analysis/v54_progression_weaker_effect_power/summary.json", "minimum_n_by_scenario.event_030_hr_13", "eq", 900),
        ("analysis/v54_progression_weaker_effect_power/summary.json", "minimum_n_by_scenario.event_015_hr_13", "eq", 1500),
        ("analysis/v54_progression_weaker_effect_power/summary.json", "minimum_n_by_scenario.event_015_hr_15", "eq", 600),
        ("analysis/v54_progression_blinded_feasibility/summary.json", "n_fixtures", "eq", 9),
        ("analysis/v54_progression_blinded_feasibility/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_information_monitor/summary.json", "n_fixtures", "eq", 10),
        ("analysis/v54_progression_information_monitor/summary.json", "efficacy_stopping_authority", "eq", False),
        ("analysis/v54_progression_information_monitor/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_treatment_switch_estimand/summary.json", "n_unique_simulated_cohorts", "eq", 72000),
        ("analysis/v54_progression_treatment_switch_estimand/summary.json", "n_invalid_null_families", "eq", 3),
        ("analysis/v54_progression_treatment_switch_estimand/summary.json", "n_strict_cell_flag_but_family_compatible", "eq", 2),
        ("analysis/v54_progression_treatment_switch_estimand/summary.json", "verdict", "eq", "ESTIMAND_MUST_BE_FROZEN_SWITCHING_CAN_CHANGE_OR_INVALIDATE_INTERPRETATION"),
        ("analysis/v54_progression_linear_misspecification/summary.json", "n_independent_null_calibration_cohorts", "eq", 18000),
        ("analysis/v54_progression_linear_misspecification/summary.json", "n_unique_simulated_cohorts", "eq", 108000),
        ("analysis/v54_progression_linear_misspecification/summary.json", "n_invalid_null_families", "eq", 0),
        ("analysis/v54_progression_linear_misspecification/summary.json", "n_materially_missed_by_linear", "eq", 1),
        ("analysis/v54_progression_linear_misspecification/summary.json", "materially_missed_cells.0.effect_pattern", "eq", "u_shaped_crossing"),
        ("analysis/v54_progression_treatment_switch_gate/summary.json", "n_fixtures", "eq", 10),
        ("analysis/v54_progression_treatment_switch_gate/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_nonlinear_diagnostic_gate/summary.json", "n_fixtures", "eq", 10),
        ("analysis/v54_progression_nonlinear_diagnostic_gate/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_candidate_role_matrix/summary.json", "P1_eligible", "eq", 0),
        ("analysis/v54_progression_candidate_role_matrix/summary.json", "P2_eligible", "eq", 0),
        ("analysis/v54_progression_candidate_role_matrix/summary.json", "P3_eligible", "eq", 0),
        ("analysis/v54_progression_evidence_delta/summary.json", "traceability_status", "eq", "PASS"),
        ("analysis/v54_progression_package_eligibility_validator/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_outcome_semantic_checker/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_combined_intake_gate/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_p1_intake_to_lock/summary.json", "n_fixtures", "eq", 10),
        ("analysis/v54_progression_p1_intake_to_lock/summary.json", "n_pass", "eq", 10),
        ("analysis/v54_progression_p1_intake_to_lock/summary.json", "n_lock_ready", "eq", 1),
        ("analysis/v54_progression_p1_intake_to_lock/summary.json", "n_fail_closed", "eq", 8),
        ("analysis/v54_progression_p1_intake_to_lock/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_endpoint_adjudication/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_endpoint_adjudication/summary.json", "n_fixtures", "eq", 16),
        ("analysis/v54_progression_event_time_assumption_gate/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_p2_composition_gate/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_event_time_power_design/reference_check/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_event_time_assumption_robustness/reference_check/summary.json", "overall_status", "eq", "PASS"),
        ("analysis/v54_progression_p2_interaction_power/reference_check/summary.json", "overall_status", "eq", "PASS"),
    ]
    invariants = [invariant(*specification) for specification in specifications]

    report = (ROOT / "docs/history/PROGRESSION_FRONTIER_V54.md").read_text()
    required_phrases = [
        "does **not** contain a transcriptomic cohort with a\nlongitudinal disability outcome",
        "Status: **no progression-direction-resolved intervention route**.",
        "None of ten candidates\nqualifies for P1, P2, or P3",
    ]
    for phrase in required_phrases:
        invariants.append(
            {
                "artifact": "docs/history/PROGRESSION_FRONTIER_V54.md",
                "key": "required_claim_boundary",
                "operator": "contains",
                "expected": json.dumps(phrase),
                "observed": json.dumps(phrase if phrase in report else "MISSING"),
                "pass": phrase in report,
            }
        )

    check_frame = pd.DataFrame(checks)
    invariant_frame = pd.DataFrame(invariants)
    # Keep generated TSVs compatible with `git diff --check`: an empty final
    # diagnostic field serializes as a trailing tab even when the check passes.
    check_frame = check_frame.replace("", "-")
    check_frame.to_csv(OUT / "command_checks.tsv", sep="\t", index=False)
    invariant_frame.to_csv(OUT / "artifact_invariants.tsv", sep="\t", index=False)
    passed = bool(check_frame["pass"].all() and invariant_frame["pass"].all())
    summary = {
        "purpose": "V54 consolidated progression regression and claim-boundary suite",
        "synthetic_or_method_only": True,
        "n_command_checks": len(check_frame),
        "n_command_pass": int(check_frame["pass"].sum()),
        "n_artifact_invariants": len(invariant_frame),
        "n_artifact_invariants_pass": int(invariant_frame["pass"].sum()),
        "overall_status": "PASS" if passed else "FAIL",
        "boundary": "Regression and artifact-consistency behavior only; passing creates no progression or biological claim.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUT / "REPORT.md").write_text(
        "# V54 Consolidated Progression Regression Suite\n\n"
        f"Status: **{summary['overall_status']}**.\n\n"
        f"{summary['n_command_pass']}/{summary['n_command_checks']} command checks and "
        f"{summary['n_artifact_invariants_pass']}/{summary['n_artifact_invariants']} "
        "claim/artifact invariants pass. This is method and repository behavior, not biological evidence.\n"
    )
    print(json.dumps(summary, indent=2))
    if not passed:
        failures = check_frame.loc[~check_frame["pass"], "check"].tolist()
        failed_invariants = invariant_frame.loc[~invariant_frame["pass"], ["artifact", "key"]].to_dict("records")
        raise RuntimeError(f"V54 suite failed: commands={failures}; invariants={failed_invariants}")


if __name__ == "__main__":
    main()
