#!/usr/bin/env python3
"""Build an artifact-bound operational acquisition priority for V54."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_acquisition_voi"
SCHEMA = ROOT / "docs/validation/input_schemas/V54_progression_cohort_required_fields.tsv"
MATRIX = ROOT / "analysis/v54_progression_candidate_role_matrix/candidate_role_matrix.tsv"
MANIFEST = ROOT / "analysis/v54_progression_reference_manifest/manifest.json"
LIVING_MOLECULAR_CANDIDATES = [
    "Gafson 2018 DMF PBMC package",
    "Karolinska DMF ROS GSE130478/GSE130491",
    "GSE228330 ocrelizumab PBMC",
    "GSE24427 longitudinal IFN-beta blood",
    "GSE17410 MS pregnancy PBMC",
]


def bundle(
    rank: int,
    identifier: str,
    timing: str,
    decision: str,
    fields: list[str],
    gates: list[str],
    dependencies: list[str],
    candidates: list[str],
    basis: list[str],
    missing_consequence: str,
) -> dict[str, Any]:
    return {
        "rank": rank,
        "bundle_id": identifier,
        "timing": timing,
        "decision_unlocked": decision,
        "required_fields_or_features": ";".join(fields),
        "gates_unblocked": ";".join(gates),
        "dependencies": ";".join(dependencies) if dependencies else "none",
        "current_candidates_potentially_addressed": ";".join(candidates) if candidates else "none",
        "n_current_candidates_potentially_addressed": len(candidates),
        "supporting_artifacts": ";".join(basis),
        "non_substitutable": True,
        "missing_consequence": missing_consequence,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    schema = pd.read_csv(SCHEMA, sep="\t", dtype=str, keep_default_na=False)
    known_fields = set(schema.field)
    matrix = pd.read_csv(MATRIX, sep="\t", dtype=str, keep_default_na=False)
    manifest = json.loads(MANIFEST.read_text())
    gate_ids = {item["id"] for item in manifest["gates"]}
    candidate_names = set(matrix.candidate)
    if not set(LIVING_MOLECULAR_CANDIDATES).issubset(candidate_names):
        raise RuntimeError("Candidate matrix changed; acquisition priority requires review")
    if any(int(manifest["current_known_eligible_roles"][role]) != 0 for role in ("P1", "P2", "P3")):
        raise RuntimeError("Eligible-role state changed; acquisition priority requires review")

    common_basis = [
        "docs/validation/PROGRESSION_COHORT_ACQUISITION_SPEC_V54.md",
        "analysis/v54_progression_candidate_role_matrix/candidate_role_matrix.tsv",
    ]
    bundles = [
        bundle(
            1,
            "p1_longitudinal_disability_link",
            "immediate",
            "Test whether a frozen molecular state precedes confirmed disability accumulation",
            ["subject_id", "sample_id", "visit_id", "collection_date", "days_from_baseline", "edss_value", "edss_assessment_date", "progression_event", "progression_definition", "progression_confirmation_interval_days", "expression_file", "expression_scale", "feature_annotation_file", "feature_id_version"],
            ["combined_intake"],
            [],
            LIVING_MOLECULAR_CANDIDATES,
            common_basis + ["analysis/v54_transition_identifiability/summary.json"],
            "No P1 progression association can be estimated; relapse, stage, or pharmacodynamic response cannot substitute.",
        ),
        bundle(
            2,
            "attendance_censoring_provenance",
            "immediate",
            "Determine whether event-time inference is interpretable rather than selection-biased",
            ["expected_and_actual_visit_dates", "attendance_status", "attendance_reason_dictionary", "last_observation_date", "censoring_date", "censoring_reason", "death_date_and_cause"],
            ["event_time", "information_monitor"],
            ["p1_longitudinal_disability_link"],
            LIVING_MOLECULAR_CANDIDATES,
            common_basis + ["analysis/v54_progression_combined_ascertainment_confirmation/summary.json"],
            "Unknown or joint score/risk attendance fails closed; even 10% weak-joint loss was method-invalid.",
        ),
        bundle(
            3,
            "site_batch_scale_identity",
            "immediate",
            "Separate within-site molecular association from site, platform, and assay-scale structure",
            ["processing_batch", "collection_site", "library_or_array_platform", "rin_or_quality_metric", "library_depth_or_array_qc"],
            ["site_score", "blinded_feasibility"],
            ["p1_longitudinal_disability_link"],
            LIVING_MOLECULAR_CANDIDATES,
            common_basis + ["analysis/v54_progression_multisite_transportability/summary.json"],
            "Pooled association is not interpretable and transport cannot be claimed.",
        ),
        bundle(
            4,
            "balanced_event_yield",
            "immediate",
            "Reach a transport-informative P1 test rather than an underpowered descriptive estimate",
            ["three_predeclared_sites", "balanced_analyzable_targets", "confirmed_event_total", "minimum_confirmed_events_per_site", "quarterly_24_month_followup"],
            ["blinded_feasibility", "information_monitor"],
            ["p1_longitudinal_disability_link", "site_batch_scale_identity"],
            [],
            common_basis + ["analysis/v54_progression_enrollment_inflation/summary.json", "analysis/v54_progression_multisite_transportability/transport_readiness.tsv"],
            "A small or imbalanced package may estimate an effect but cannot settle or transport it; n=450 is a conditional reference, not a universal minimum.",
        ),
        bundle(
            5,
            "pira_treatment_activity_context",
            "immediate",
            "Distinguish relapse-independent accumulation and freeze treatment-switch estimands",
            ["pira_label", "pira_definition", "relapse_onset_date", "relapse_recovery_date", "steroid_start_date", "infection_date_and_status", "dmt_name", "dmt_start_date", "dmt_stop_date", "dmt_dose_or_infusion_date", "treatment_switch_reason"],
            ["combined_intake", "treatment_switch"],
            ["p1_longitudinal_disability_link"],
            LIVING_MOLECULAR_CANDIDATES,
            common_basis + ["analysis/v54_progression_treatment_switch_estimand/summary.json"],
            "CDP cannot be interpreted as PIRA and post-switch follow-up cannot be assigned a defensible estimand.",
        ),
        bundle(
            6,
            "molecular_reliability_repeats",
            "conditional_after_core_receipt",
            "Choose one versus repeated molecular measurements without outcome-driven timepoint selection",
            ["replicate_or_repeat_sample_ids", "blinded_test_retest_reliability", "shared_batch_error_audit"],
            ["blinded_feasibility"],
            ["p1_longitudinal_disability_link"],
            LIVING_MOLECULAR_CANDIDATES,
            common_basis + ["analysis/v54_progression_repeated_score_reliability/summary.json"],
            "Measurement error may erase power; repeats help only when starting reliability is low and errors are sufficiently independent.",
        ),
        bundle(
            7,
            "paired_csf_blood_direct_composition",
            "conditional_after_p1_signal",
            "Test whether a P1 association localizes to CNS/CSF rather than peripheral composition",
            ["compartment", "cell_count_file", "paired_compartment_sample_id"],
            ["combined_intake"],
            ["p1_longitudinal_disability_link", "P1_association_pass"],
            [],
            common_basis + ["analysis/v54_cns_peripheral_identifiability/summary.json", "analysis/v54_progression_p2_interaction_power/summary.json"],
            "No compartment localization claim is identifiable; separate brain and blood cohorts do not substitute for a formal interaction.",
        ),
        bundle(
            8,
            "longitudinal_chronic_active_imaging",
            "conditional_after_core_receipt",
            "Relate molecular state to chronic-active lesion persistence rather than cross-sectional lesion morphology",
            ["mri_date", "new_enlarging_t2_count", "gadolinium_enhancing_count", "prl_or_slowly_expanding_lesion_id", "prl_detection_protocol", "prl_persistence_or_change"],
            [],
            ["p1_longitudinal_disability_link"],
            [],
            common_basis + ["analysis/v54_progression_lesion_state/summary.json"],
            "Lesion morphology remains pathology context and cannot establish disability progression or a target.",
        ),
        bundle(
            9,
            "p3_direction_resolved_function",
            "conditional_after_p1_p2",
            "Test whether selective direction-matched modulation improves a progression-relevant function safely",
            ["perturbation_id", "perturbation_target", "perturbation_direction", "perturbation_dose", "donor_id", "primary_human_context", "target_engagement_readout", "functional_progression_readout", "viability_readout", "host_defense_readout", "myelin_clearance_or_remyelination_readout", "wrong_direction_control", "non_targeting_or_vehicle_control"],
            [],
            ["P1_association_pass", "P2_localization_or_justified_context"],
            [],
            common_basis + ["analysis/v54_progression_intervention_direction_map/summary.json"],
            "No intervention or halting-progression claim is permitted; structural tractability cannot substitute for functional direction.",
        ),
    ]

    external_features = {
        "expected_and_actual_visit_dates", "attendance_status", "attendance_reason_dictionary",
        "last_observation_date", "censoring_date", "censoring_reason", "death_date_and_cause",
        "three_predeclared_sites", "balanced_analyzable_targets", "confirmed_event_total",
        "minimum_confirmed_events_per_site", "quarterly_24_month_followup",
        "replicate_or_repeat_sample_ids", "blinded_test_retest_reliability", "shared_batch_error_audit",
    }
    for item in bundles:
        fields = set(item["required_fields_or_features"].split(";"))
        unknown = fields - known_fields - external_features
        if unknown:
            raise RuntimeError(f"Unknown acquisition fields for {item['bundle_id']}: {sorted(unknown)}")
        gates = set(filter(None, item["gates_unblocked"].split(";")))
        if not gates.issubset(gate_ids):
            raise RuntimeError(f"Unknown gates for {item['bundle_id']}: {sorted(gates - gate_ids)}")
        for artifact in item["supporting_artifacts"].split(";"):
            if not (ROOT / artifact).is_file():
                raise RuntimeError(f"Missing supporting artifact: {artifact}")

    frame = pd.DataFrame(bundles).sort_values("rank")
    frame.to_csv(OUT / "acquisition_priority.tsv", sep="\t", index=False)
    summary = {
        "purpose": "Artifact-bound operational acquisition value-of-information synthesis for V54",
        "synthetic_or_method_only": True,
        "n_bundles": len(frame),
        "n_immediate_bundles": int(frame.timing.eq("immediate").sum()),
        "n_conditional_bundles": int((~frame.timing.eq("immediate")).sum()),
        "top_priority": frame.iloc[0].bundle_id,
        "current_p1_eligible": int(manifest["current_known_eligible_roles"]["P1"]),
        "current_p2_eligible": int(manifest["current_known_eligible_roles"]["P2"]),
        "current_p3_eligible": int(manifest["current_known_eligible_roles"]["P3"]),
        "ranking_basis": "Dependency order, non-substitutability, executable gate unlocks, and documented current blockers; not a probability of biological success or monetary VOI.",
        "verdict": "ACQUIRE_P1_LONGITUDINAL_CORE_AND_ASCERTAINMENT_PROVENANCE_FIRST",
        "boundary": "Operational acquisition priority only; no biological finding, expected effect, or guarantee that acquired data validates a progression state.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
