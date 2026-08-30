#!/usr/bin/env python3
"""Audit V57 claim boundaries and key machine-readable results."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v57_regression_suite"


def load(path: str) -> dict[str, object]:
    return json.loads((ROOT / path).read_text())


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    report_path = ROOT / "docs/history/METHOD_PROBES_V57.md"
    report = report_path.read_text()
    current = (ROOT / "meta/CURRENT_STATUS.md").read_text()
    next_actions = (ROOT / "meta/NEXT_ACTIONS.md").read_text()
    queue = (ROOT / "meta/V57_QUEUE.md").read_text()

    check("cumulative_report_exists", report_path.exists(), str(report_path.relative_to(ROOT)))
    check("report_explicit_no_cure", "did **not** discover a cure" in report, "explicit negative boundary")
    report_flat = " ".join(report.split())
    current_flat = " ".join(current.split())
    check("report_explicit_no_target", "no new intervention-grade target" in report_flat, "target boundary")
    check("report_epistemic_separation", "## Epistemic Separation" in report, "result classes separated")
    check("report_ranks_code_to_data_first", "### 1. Privacy-Preserving Same-Estimand Validation" in report, "rank 1")
    check("report_preserves_v41", "public-data search remains exhausted" in report, "discovery boundary")
    check("current_status_no_cure", "It did not identify a cure" in current_flat, "live status boundary")
    check("next_actions_opengwas_renewal", "Renew OpenGWAS before any genetics API work" in next_actions, "expired-token route")
    check("queue_synthesis_done", "| 10 | Consolidate grounded method probes and ranked dedicated-run shortlist | done |" in queue, "task 10")

    environment = load("analysis/v57_environment_stability/summary.json")
    env = environment["environment_stability"]
    selective = environment["selective_prediction"]
    check("environment_stability_failed", env["verdict"] == "NOT_ENVIRONMENT_STABLE", str(env["verdict"]))
    check("environment_worst_near_chance", float(env["worst_environment_auc"]) < 0.55, str(env["worst_environment_auc"]))
    check("selective_transport_failed", selective["verdict"] == "NOT_TRANSPORT_READY", str(selective["verdict"]))

    partial = load("analysis/v57_partial_conjunction/summary.json")
    check("cross_environment_recurrence_not_established", partial["primary_transport_replicability_pass"] is False, str(partial["primary_bonferroni_pc_p"]))
    measurement = load("analysis/v57_measurement_invariance/summary.json")
    check("measurement_invariance_failed", measurement["global_measurement_invariance_gate"] == "FAIL", str(measurement["global_measurement_invariance_gate"]))
    competitive = load("analysis/v57_competitive_module_null/summary.json")
    check("competitive_module_null_passed", competitive["competitive_specificity_gate"] == "PASS", str(competitive["observed_v22_pooled_percentile_auc"]))

    held_nulls = {
        "composition": ("analysis/v57_compositional_response/summary.json", "verdict", "NO_RESPONSE_SPECIFIC_COMPOSITION"),
        "state_geometry": ("analysis/v57_multivariate_state_geometry/summary.json", "verdict", "NO_RESPONSE_SPECIFIC_JOINT_GEOMETRY"),
        "neighborhood_da": ("analysis/v57_neighborhood_da/summary.json", "verdict", "NO_STABLE_RESPONSE_SPECIFIC_NEIGHBORHOOD"),
        "transport_map": ("analysis/v57_multivariate_transport_map/summary.json", "verdict", "NO_STABLE_RESPONSE_SPECIFIC_TRANSPORT_MAP"),
        "tensor": ("analysis/v57_tensor_interaction/summary.json", "verdict", "NO_REPRODUCIBLE_TENSOR_GAIN"),
        "hierarchy": ("analysis/v57_hierarchical_environment/summary.json", "verdict", "HIERARCHICAL_MODEL_NOT_READY"),
        "topology": ("analysis/v57_cell_state_topology/summary.json", "verdict", "TOPOLOGY_NOT_ESTIMABLE_AT_FROZEN_CELL_COUNT"),
    }
    for name, (path, field, expected) in held_nulls.items():
        observed = load(path).get(field)
        check(f"held_{name}_verdict", observed == expected, f"expected={expected};observed={observed}")

    sequential = load("analysis/v57_sequential_evidence/synthetic/summary.json")
    check("sequential_is_method_only", "no MS biological evidence" in str(sequential["purpose"]), str(sequential["purpose"]))
    check("sequential_verified", sequential["method_verified"] is True, str(sequential["verdict"]))
    check("sequential_null_gate", sequential["null_gate"] is True, str(sequential["null_crossing_probability_range"]))

    for name, path, expected in (
        ("discrete", "analysis/v57_discrete_site_eprocess/discrete_site_eprocess_summary.json", "DISCRETE_SITE_EPROCESS_VERIFIED"),
        ("tied", "analysis/v57_tied_site_eprocess/tied_site_eprocess_summary.json", "TIED_SITE_EPROCESS_VERIFIED"),
    ):
        result = load(path)
        check(f"{name}_site_synthetic", result["synthetic"] is True, str(result["synthetic"]))
        check(f"{name}_site_verified", result["verdict"] == expected, str(result["verdict"]))
        check(f"{name}_site_null_gate", result["null_optional_stopping_gate"] is True, str(result["null_crossing_range"]))
        check(f"{name}_site_power_gate", result["strong_power_gate"] is True, str(result["strong_crossing_range"]))

    code_to_data = load("analysis/v57_code_to_data_validation/synthetic_check_summary.json")
    check("code_to_data_synthetic", code_to_data["synthetic"] is True, str(code_to_data["synthetic"]))
    check("code_to_data_valid_passes", code_to_data["valid_export_status"] == "PASS", str(code_to_data["valid_export_status"]))
    check("code_to_data_tamper_fails", code_to_data["tamper_detected"] is True, str(code_to_data["tamper_detected"]))
    check("code_to_data_leak_fails", code_to_data["leak_detected"] is True and code_to_data["private_score_table_exported"] is False, str(code_to_data))

    federated = load("analysis/v57_federated_evidence/synthetic_check_summary.json")
    check("federated_synthetic", federated["synthetic"] is True, str(federated["synthetic"]))
    check("federated_valid_passes", federated["valid_combination_passed"] is True, str(federated["valid_combination_passed"]))
    check("federated_duplicate_rejected", federated["duplicate_independence_group_rejected"] is True, str(federated["duplicate_independence_group_rejected"]))
    check("federated_hash_mismatch_rejected", federated["harness_hash_mismatch_rejected"] is True, str(federated["harness_hash_mismatch_rejected"]))

    parent = load("analysis/v57_multifidelity_escalation/multifidelity_escalation_summary.json")
    safety = load("analysis/v57_multifidelity_safety_power/multifidelity_safety_power_summary.json")
    negative = load("analysis/v57_negative_control_finite_sample/negative_control_finite_sample_summary.json")
    check("multifidelity_parent_failure_retained", parent["overall_status"] == "FAIL" and parent["n_fail"] == 1, f"status={parent['overall_status']};n_fail={parent['n_fail']}")
    check("multifidelity_parent_synthetic", parent["synthetic"] is True, str(parent["synthetic"]))
    check("multifidelity_safety_extension_passed", safety["overall_status"] == "PASS", str(safety["first_all_seed_pass"]))
    check("multifidelity_safety_synthetic", safety["synthetic"] is True, str(safety["synthetic"]))
    check("negative_control_passed", negative["overall_status"] == "PASS", str(negative["first_all_seed_pass"]))
    check("negative_control_synthetic", negative["synthetic"] is True, str(negative["synthetic"]))

    external_records = (
        "knowledge_external/records/method_human_ipsc_microglia_crispri_a_2022.json",
        "knowledge_external/records/method_microglia_oligodendrocyte_assembloid_2024.json",
        "knowledge_external/records/method_ms_glia_enriched_organoid_2025.json",
        "knowledge_external/records/model_v57_claude_method_critique_2026.json",
        "knowledge_external/records/model_v57_gemini_method_critique_2026.json",
    )
    for path in external_records:
        record = load(path)
        classed = str(record.get("epistemic_class", "")).startswith("external-")
        check(f"external_record_classed_{Path(path).stem}", classed, "external class prefix present" if classed else "class prefix missing")
        marker = record.get("not_project_grounded_marker")
        marker_ok = marker == "NOT_PROJECT_GROUNDED"
        check(f"external_record_not_grounded_{Path(path).stem}", marker_ok, "not-grounded marker present" if marker_ok else "not-grounded marker missing")

    plans = (
        "docs/plans/V57_ENVIRONMENT_STABILITY_PLAN.md",
        "docs/plans/V57_SEQUENTIAL_EVIDENCE_PLAN.md",
        "docs/plans/V57_MULTIFIDELITY_ESCALATION_PLAN.md",
        "docs/plans/V57_NEGATIVE_CONTROL_FINITE_SAMPLE_PLAN.md",
        "docs/plans/V57_DISCRETE_SITE_EPROCESS_PLAN.md",
        "docs/plans/V57_TIED_SITE_EPROCESS_PLAN.md",
    )
    for path in plans:
        check(f"plan_exists_{Path(path).stem}", (ROOT / path).exists(), path)

    with (OUT / "v57_regression_checks.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "status", "detail"), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    failures = [row for row in rows if row["status"] == "FAIL"]
    summary = {
        "purpose": "V57 claim/artifact regression; no biological claim",
        "n_checks": len(rows),
        "n_pass": len(rows) - len(failures),
        "n_fail": len(failures),
        "overall_status": "PASS" if not failures else "FAIL",
        "failures": [row["check_id"] for row in failures],
        "checks": "analysis/v57_regression_suite/v57_regression_checks.tsv",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
