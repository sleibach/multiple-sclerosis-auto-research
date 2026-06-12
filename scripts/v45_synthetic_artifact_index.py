#!/usr/bin/env python3
"""Index V43-V45 synthetic/method-characterization artifacts.

The goal is governance: make clear which artifacts are synthetic method checks,
which are public-metadata preparation, and which are internal convergence
analyses. The index is not a biological analysis.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v45_synthetic_artifact_index"


MANUAL_CLASS = {
    "analysis/v43_method_validation": ("synthetic_method_characterization", "method behavior only"),
    "analysis/v44_batch_guard": ("synthetic_method_characterization", "method behavior only"),
    "analysis/v44_secondary_lead_harnesses": ("synthetic_harness_verification", "method behavior only"),
    "analysis/v45_multiconfounder_batch_guard": ("synthetic_method_characterization", "method behavior only"),
    "analysis/v45_postpartum_pathology": ("synthetic_method_characterization", "method behavior only"),
    "analysis/v45_tb_compartment_pathology": ("synthetic_method_characterization", "method behavior only"),
    "analysis/v45_batch_guard_calibration": ("synthetic_method_characterization", "method behavior only"),
    "analysis/v45_batch_guard_calibration_full": ("synthetic_method_characterization", "method behavior only"),
    "analysis/v45_secondary_batch_calibration": ("synthetic_method_characterization", "method behavior only"),
    "analysis/v45_seed_variation_stability": ("synthetic_method_characterization", "method behavior only"),
    "analysis/v45_secondary_real_ingest": ("synthetic_harness_verification", "method behavior only"),
    "analysis/v45_pharmacodynamic_only_harness": ("synthetic_harness_verification", "method behavior only"),
    "analysis/v45_validation_intake_preflight": ("synthetic_intake_verification", "method behavior only"),
    "analysis/v45_harness_regression_tests": ("synthetic_regression", "software regression only"),
    "analysis/v45_preflight_regression_tests": ("synthetic_regression", "software regression only"),
    "analysis/v45_primary_harness_regression_tests": ("synthetic_regression", "software regression only"),
    "analysis/v45_regression_aggregator": ("synthetic_regression", "software regression only"),
    "analysis/v44_internal_validation": ("internal_convergence_null", "data-free internal support, not clinical validation"),
    "analysis/v44_self_audit_weak_leg": ("internal_convergence_null", "data-free internal support, not clinical validation"),
    "analysis/v45_convergence_sensitivity": ("internal_convergence_null", "data-free internal support, not clinical validation"),
    "analysis/v45_convergence_family_jackknife": ("internal_convergence_null", "data-free internal support, not clinical validation"),
    "analysis/v45_convergence_no_reports": ("internal_convergence_null", "data-free internal support, not clinical validation"),
    "analysis/v45_convergence_no_readiness": ("internal_convergence_null", "data-free internal support, not clinical validation"),
    "analysis/v44_alt_cohort_scout": ("public_metadata_scout", "cohort availability evidence only"),
    "analysis/v45_gse228330_outcome_scout": ("public_metadata_scout", "cohort availability evidence only"),
    "analysis/v45_gse228330_pharmacodynamic_runbook": ("public_metadata_preparation", "acquisition readiness only"),
    "analysis/v45_karolinska_access": ("public_metadata_scout", "cohort availability evidence only"),
    "analysis/v45_outbound_data_requests": ("operations", "acquisition operations only"),
    "analysis/v45_live_cohort_acquisition_index": ("operations", "acquisition operations only"),
    "analysis/v45_collaborator_package": ("operations", "acquisition operations only"),
    "analysis/v45_collaborator_path_resolver": ("integrity_governance", "collaborator package path integrity only"),
    "analysis/v45_author_run_packet_bundle": ("operations", "author-run packet bundle only"),
    "analysis/v45_author_run_packet_checksums": ("integrity_governance", "author-run packet checksum integrity only"),
    "analysis/v45_author_run_bundle_dryrun_manifest": ("integrity_governance", "author-run packet dry-run integrity only"),
    "analysis/v45_author_run_redaction_precheck": ("synthetic_intake_verification", "method behavior only"),
    "analysis/v45_author_run_return_gate_runner": ("synthetic_intake_verification", "method behavior only"),
    "analysis/v45_received_data_triage": ("operations", "acquisition operations only"),
    "analysis/v45_received_status_updater": ("operations", "received-package status update only"),
    "analysis/v45_request_sent_updater": ("operations", "request-sent status update only"),
    "analysis/v45_followup_due_board": ("operations", "acquisition follow-up status only"),
    "analysis/v45_followup_message_templates": ("operations", "unsent acquisition message drafts only"),
    "analysis/v45_external_blocker_board": ("operations", "external blocker status only"),
    "analysis/v45_external_blocker_escalation_matrix": ("operations", "external blocker escalation status only"),
    "analysis/v45_route_arrival_packets": ("operations", "route-specific arrival commands only"),
    "analysis/v45_route_packet_integrity_manifest": ("integrity_governance", "route packet checksum/freshness only"),
    "analysis/v45_current_action_card": ("operations", "current action navigation only"),
    "analysis/v45_send_log_intake_template": ("operations", "request-sent intake template only"),
    "analysis/v45_rpt_readiness": ("proposal_lens_grounding", "proposal prioritization only"),
    "analysis/v45_synthetic_artifact_index": ("artifact_governance", "index only"),
    "analysis/v45_artifact_index": ("artifact_governance", "index only"),
    "analysis/v45_compute_storage_summary": ("artifact_governance", "storage/accounting only"),
    "analysis/v45_governance_refresh": ("artifact_governance", "refresh log only"),
    "analysis/v45_precommit_readiness": ("integrity_governance", "pre-commit readiness only"),
    "analysis/v45_readiness_status_dashboard": ("integrity_governance", "readiness dashboard only"),
    "analysis/v45_generated_checker_registry": ("integrity_governance", "generated-checker registry only"),
    "analysis/v45_readiness_stale_output_detector": ("integrity_governance", "readiness freshness check only"),
    "analysis/v45_no_raw_git_scanner": ("integrity_governance", "repository hygiene only"),
    "analysis/v45_locked_artifact_hash_audit": ("integrity_governance", "locked-artifact integrity only"),
    "analysis/v45_command_plan_consistency": ("integrity_governance", "command-plan integrity only"),
    "analysis/v45_state_machine_validator": ("integrity_governance", "state-machine transition consistency only"),
    "analysis/v45_array_processing_readiness": ("validation_infrastructure", "toolchain readiness only"),
    "analysis/v45_validation_command_runner": ("validation_infrastructure", "command handoff only"),
    "analysis/v45_gate_output_bundle_manifest": ("validation_infrastructure", "handoff manifest only"),
    "analysis/v45_handoff_completeness": ("validation_infrastructure", "handoff completeness only"),
    "analysis/v45_handoff_completeness_scored_missing": ("validation_infrastructure", "expected missing-output guard only"),
    "analysis/v45_author_run_output_check": ("synthetic_intake_verification", "method behavior only"),
    "analysis/v45_author_run_output_check_incomplete": ("synthetic_intake_verification", "expected missing-output guard only"),
    "analysis/v45_power_decision_table": ("power_design_planning", "study design planning only"),
    "analysis/v45_dropout_sensitivity_table": ("power_design_planning", "study design planning only"),
    "analysis/v45_route_analyzable_pair_calculator": ("power_design_planning", "study design planning only"),
    "analysis/v45_checksum_manifest_validator": ("synthetic_intake_verification", "method behavior only"),
    "analysis/v45_intake_template_dryrun": ("synthetic_intake_verification", "method behavior only"),
    "analysis/v45_module_coverage_precheck": ("synthetic_intake_verification", "method behavior only"),
    "analysis/v45_metadata_contradiction_stress": ("synthetic_intake_verification", "method behavior only"),
    "analysis/v45_metadata_missingness_scorer": ("synthetic_intake_verification", "method behavior only"),
    "analysis/v45_outcome_label_dictionary_validator": ("synthetic_intake_verification", "method behavior only"),
    "analysis/v45_response_column_audit": ("synthetic_intake_verification", "method behavior only"),
    "analysis/v45_subject_map_sanity_check": ("synthetic_intake_verification", "method behavior only"),
    "analysis/v45_secondary_missing_timepoint_stress": ("synthetic_method_characterization", "method behavior only"),
}


def text_sample_has_synthetic(path: Path) -> bool:
    try:
        if path.stat().st_size > 2_000_000:
            return False
        text = path.read_text(errors="ignore").lower()
    except OSError:
        return False
    return '"synthetic": true' in text or "\tsynthetic\t" in text or "synthetic_" in text


def summarize_dir(path: Path) -> dict[str, object]:
    files = [p for p in path.rglob("*") if p.is_file()]
    rel = str(path.relative_to(ROOT))
    cls, allowed = MANUAL_CLASS.get(rel, ("unclassified_v43_v45", "review before use"))
    synthetic_by_path = any("synthetic" in str(p.relative_to(path)).lower() for p in files)
    synthetic_by_content = any(text_sample_has_synthetic(p) for p in files[:200])
    json_summaries = [str(p.relative_to(ROOT)) for p in files if p.name in {"summary.json", "regression_summary.json", "synthetic_check_summary.json"}]
    return {
        "artifact_dir": rel,
        "class": cls,
        "allowed_interpretation": allowed,
        "n_files": len(files),
        "has_synthetic_path_marker": synthetic_by_path,
        "has_synthetic_content_marker": synthetic_by_content,
        "contains_synthetic": synthetic_by_path or synthetic_by_content or cls.startswith("synthetic"),
        "summary_files": ";".join(json_summaries[:12]),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    dirs = sorted(
        p for p in (ROOT / "analysis").iterdir()
        if p.is_dir() and (p.name.startswith("v43") or p.name.startswith("v44") or p.name.startswith("v45"))
    )
    rows = [summarize_dir(path) for path in dirs]
    table = pd.DataFrame(rows)
    table.to_csv(OUT / "v43_v45_artifact_index.tsv", sep="\t", index=False)
    class_summary = (
        table.groupby(["class", "allowed_interpretation"], as_index=False)
        .agg(n_dirs=("artifact_dir", "nunique"), n_files=("n_files", "sum"))
        .sort_values(["class", "n_dirs"])
    )
    class_summary.to_csv(OUT / "class_summary.tsv", sep="\t", index=False)
    summary = {
        "synthetic": False,
        "purpose": "artifact governance index; no biological claim",
        "n_dirs_indexed": int(len(table)),
        "n_dirs_containing_synthetic": int(table["contains_synthetic"].sum()),
        "classes": class_summary.to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
