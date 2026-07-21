#!/usr/bin/env python3
"""Build the V54 metadata-only candidate matrix for progression roles P1-P3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_candidate_role_matrix"


def candidates() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "Gafson 2018 DMF PBMC package",
            "source_artifact": "docs/validation/GAFSON_DATA_REQUEST_V36.md",
            "access_state": "external package not held",
            "living_participants": "yes",
            "verified_subject_map": "unknown",
            "repeated_molecular": "expected_unverified",
            "repeated_disability_components": "no",
            "documented_cdp_or_pira": "no",
            "relapse_steroid_treatment_context": "partial_requested",
            "paired_cns_or_csf_and_blood": "no",
            "direct_composition_measurement": "unknown",
            "progression_association_gate_passed": "no",
            "selective_multidonor_functional_perturbation": "no",
            "safe_current_use": "frozen V22/V42 NEDA-4 monitoring validation if received",
            "primary_blocker": "NEDA-4 response is not repeated disability progression",
            "next_action": "retain monitoring route; request raw repeated disability only if collected",
        },
        {
            "candidate": "Karolinska DMF ROS GSE130478/GSE130491",
            "source_artifact": "docs/validation/KAROLINSKA_DMF_LABEL_REQUEST_V45.md",
            "access_state": "public omics; labels/map requested",
            "living_participants": "yes",
            "verified_subject_map": "no",
            "repeated_molecular": "nominal_unverified",
            "repeated_disability_components": "no",
            "documented_cdp_or_pira": "no",
            "relapse_steroid_treatment_context": "partial_requested",
            "paired_cns_or_csf_and_blood": "no",
            "direct_composition_measurement": "partial_cell_sorted",
            "progression_association_gate_passed": "no",
            "selective_multidonor_functional_perturbation": "no",
            "safe_current_use": "secondary late-time DMF monitoring stress test if labels/map arrive",
            "primary_blocker": "beneficial response is not repeated disability progression",
            "next_action": "retain secondary monitoring request; add disability fields only if collected",
        },
        {
            "candidate": "GSE228330 ocrelizumab PBMC",
            "source_artifact": "docs/validation/GSE228330_OUTCOME_SCOUT_V45.md",
            "access_state": "public expression; critical metadata absent",
            "living_participants": "yes",
            "verified_subject_map": "no",
            "repeated_molecular": "nominal_unverified",
            "repeated_disability_components": "no",
            "documented_cdp_or_pira": "no",
            "relapse_steroid_treatment_context": "no",
            "paired_cns_or_csf_and_blood": "no",
            "direct_composition_measurement": "no",
            "progression_association_gate_passed": "no",
            "selective_multidonor_functional_perturbation": "no",
            "safe_current_use": "unpaired pharmacodynamic context after metadata repair",
            "primary_blocker": "no verified map or disability/outcome labels",
            "next_action": "send prepared 29-field addendum; remain context-only unless all gates pass",
        },
        {
            "candidate": "GSE24427 longitudinal IFN-beta blood",
            "source_artifact": "analysis/v54_transition_identifiability/transition_identifiability.tsv",
            "access_state": "held",
            "living_participants": "yes",
            "verified_subject_map": "yes",
            "repeated_molecular": "yes",
            "repeated_disability_components": "no",
            "documented_cdp_or_pira": "no",
            "relapse_steroid_treatment_context": "partial_relapse_only",
            "paired_cns_or_csf_and_blood": "no",
            "direct_composition_measurement": "no",
            "progression_association_gate_passed": "no",
            "selective_multidonor_functional_perturbation": "no",
            "safe_current_use": "IFN-beta pharmacodynamic and relapse context",
            "primary_blocker": "baseline EDSS only; relapse follow-up is not disability accumulation",
            "next_action": "do not repurpose as progression; ask source only if repeated disability exists off-record",
        },
        {
            "candidate": "Macnair postmortem microglia discovery/validation",
            "source_artifact": "analysis/v54_progression_data_inventory/progression_data_inventory.tsv",
            "access_state": "held",
            "living_participants": "no",
            "verified_subject_map": "yes",
            "repeated_molecular": "no",
            "repeated_disability_components": "no",
            "documented_cdp_or_pira": "no",
            "relapse_steroid_treatment_context": "no",
            "paired_cns_or_csf_and_blood": "no",
            "direct_composition_measurement": "microglia_pseudobulk_only",
            "progression_association_gate_passed": "no",
            "selective_multidonor_functional_perturbation": "no",
            "safe_current_use": "source-balanced cross-sectional stage context",
            "primary_blocker": "one postmortem timepoint and no disability trajectory",
            "next_action": "no progression reuse; retain bounded stage context",
        },
        {
            "candidate": "GSE180759 chronic-active lesion snRNA-seq",
            "source_artifact": "analysis/v54_progression_data_inventory/progression_data_inventory.tsv",
            "access_state": "held",
            "living_participants": "no",
            "verified_subject_map": "yes",
            "repeated_molecular": "no",
            "repeated_disability_components": "no",
            "documented_cdp_or_pira": "no",
            "relapse_steroid_treatment_context": "no",
            "paired_cns_or_csf_and_blood": "no",
            "direct_composition_measurement": "single_nucleus_counts",
            "progression_association_gate_passed": "no",
            "selective_multidonor_functional_perturbation": "no",
            "safe_current_use": "small-donor lesion-state context",
            "primary_blocker": "same-death pathology contexts are not longitudinal progression",
            "next_action": "retain pathology context only",
        },
        {
            "candidate": "GSE279972 lesion morphology bulk RNA-seq",
            "source_artifact": "analysis/v54_progression_data_inventory/progression_data_inventory.tsv",
            "access_state": "held",
            "living_participants": "no",
            "verified_subject_map": "yes",
            "repeated_molecular": "no",
            "repeated_disability_components": "no",
            "documented_cdp_or_pira": "no",
            "relapse_steroid_treatment_context": "no",
            "paired_cns_or_csf_and_blood": "no",
            "direct_composition_measurement": "no",
            "progression_association_gate_passed": "no",
            "selective_multidonor_functional_perturbation": "no",
            "safe_current_use": "exploratory donor-aware morphology context",
            "primary_blocker": "no clinical time, subtype trajectory, or measured composition",
            "next_action": "retain downgraded morphology context only",
        },
        {
            "candidate": "GSE111972/GSE301908 microglia state cohorts",
            "source_artifact": "analysis/v54_progression_data_inventory/progression_data_inventory.tsv",
            "access_state": "held",
            "living_participants": "no",
            "verified_subject_map": "yes",
            "repeated_molecular": "no",
            "repeated_disability_components": "no",
            "documented_cdp_or_pira": "no",
            "relapse_steroid_treatment_context": "no",
            "paired_cns_or_csf_and_blood": "no",
            "direct_composition_measurement": "microglia_only",
            "progression_association_gate_passed": "no",
            "selective_multidonor_functional_perturbation": "no",
            "safe_current_use": "MS-versus-control microglial state context",
            "primary_blocker": "not progression-specific and no longitudinal outcome",
            "next_action": "do not promote disease-state replication to progression",
        },
        {
            "candidate": "GSE17410 MS pregnancy PBMC",
            "source_artifact": "analysis/v54_transition_identifiability/transition_identifiability.tsv",
            "access_state": "held",
            "living_participants": "yes",
            "verified_subject_map": "partial",
            "repeated_molecular": "partial",
            "repeated_disability_components": "no",
            "documented_cdp_or_pira": "no",
            "relapse_steroid_treatment_context": "partial",
            "paired_cns_or_csf_and_blood": "no",
            "direct_composition_measurement": "no",
            "progression_association_gate_passed": "no",
            "selective_multidonor_functional_perturbation": "no",
            "safe_current_use": "pregnancy-state natural-experiment context",
            "primary_blocker": "pregnancy timing is not progression and disability is absent",
            "next_action": "retain pregnancy context only",
        },
        {
            "candidate": "Held pre/post-ocrelizumab MS microbiome",
            "source_artifact": "analysis/v54_transition_identifiability/transition_identifiability.tsv",
            "access_state": "held",
            "living_participants": "yes",
            "verified_subject_map": "yes",
            "repeated_molecular": "wrong_modality",
            "repeated_disability_components": "no",
            "documented_cdp_or_pira": "no",
            "relapse_steroid_treatment_context": "partial_treatment",
            "paired_cns_or_csf_and_blood": "no",
            "direct_composition_measurement": "not_applicable",
            "progression_association_gate_passed": "no",
            "selective_multidonor_functional_perturbation": "no",
            "safe_current_use": "treatment-associated microbiome context",
            "primary_blocker": "wrong modality and no disability outcome",
            "next_action": "do not repurpose as molecular progression cohort",
        },
    ]


def exact_yes(row: pd.Series, fields: list[str]) -> bool:
    return all(str(row[field]).lower() == "yes" for field in fields)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(candidates())
    missing_artifacts = []
    for artifact in frame.source_artifact:
        if not (ROOT / artifact).exists():
            missing_artifacts.append(artifact)
    if missing_artifacts:
        raise RuntimeError(f"Missing source artifacts: {sorted(set(missing_artifacts))}")

    p1_fields = [
        "living_participants",
        "verified_subject_map",
        "repeated_molecular",
        "repeated_disability_components",
        "documented_cdp_or_pira",
        "relapse_steroid_treatment_context",
        "direct_composition_measurement",
    ]
    frame["P1_status"] = [
        "eligible_metadata_only" if exact_yes(row, p1_fields) else "not_eligible"
        for _, row in frame.iterrows()
    ]
    frame["P2_status"] = [
        "eligible_metadata_only"
        if row.P1_status == "eligible_metadata_only"
        and str(row.paired_cns_or_csf_and_blood).lower() == "yes"
        else "not_eligible"
        for _, row in frame.iterrows()
    ]
    frame["P3_status"] = [
        "eligible_metadata_only"
        if exact_yes(
            row,
            [
                "progression_association_gate_passed",
                "selective_multidonor_functional_perturbation",
            ],
        )
        else "not_eligible"
        for _, row in frame.iterrows()
    ]
    frame.to_csv(OUT / "candidate_role_matrix.tsv", sep="\t", index=False)
    summary = {
        "purpose": "V54 metadata-only progression candidate role matrix; no score access or biological claim",
        "n_candidates": len(frame),
        "P1_eligible": int(frame.P1_status.eq("eligible_metadata_only").sum()),
        "P2_eligible": int(frame.P2_status.eq("eligible_metadata_only").sum()),
        "P3_eligible": int(frame.P3_status.eq("eligible_metadata_only").sum()),
        "n_source_artifacts_verified_present": int(frame.source_artifact.nunique()),
        "verdict": "NO_KNOWN_CANDIDATE_CURRENTLY_ELIGIBLE_FOR_P1_P2_OR_P3",
        "boundary": "Metadata and semantic eligibility only. No expression values, quarantined packages, or molecular scores were read.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
