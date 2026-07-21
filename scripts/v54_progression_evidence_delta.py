#!/usr/bin/env python3
"""Build an artifact-checked progression-specific delta against V37 findings."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
V37 = ROOT / "docs/reports/FINDINGS_SCORES_V37.tsv"
OUT = ROOT / "analysis/v54_progression_evidence_delta"


ROWS = [
    (
        "Bounded APC/HLA-II early treatment-response monitoring scalar",
        "unchanged_scope",
        "provisional",
        "not_a_progression_endpoint",
        "V54 does not alter its monitoring evidence; no held analysis links it to disability progression.",
        "docs/locked_rules/LOCKED_RULE_V22.md;analysis/v54_progression_intervention_direction_map/REPORT.md",
    ),
    (
        "Tool-robust but simple V22 scalar",
        "unchanged_scope",
        "supported",
        "not_a_progression_endpoint",
        "Tool robustness remains valid for treatment monitoring and is not evidence of progression prediction.",
        "docs/workups/treatment_response/ROBUSTNESS_MAP_V28.md;analysis/v54_progression_data_inventory/REPORT.md",
    ),
    (
        "V22 scalar is immune-tone bounded, not steroid/composition artifact",
        "unchanged_scope",
        "supported",
        "not_a_progression_endpoint",
        "Its confounder-bounded monitoring interpretation is unchanged; V54 adds no disability outcome.",
        "docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md;analysis/v54_progression_data_inventory/REPORT.md",
    ),
    (
        "Coupled APC remodeling architecture",
        "narrowed_for_progression",
        "supported",
        "architecture_supported_progression_transfer_not_supported",
        "The architecture remains supported as cross-context structure, but no module transfers through the V54 progression-stage/lesion gates.",
        "docs/findings/DEEP_STRUCTURE_V26.md;analysis/v54_progressive_stage_modules/REPORT.md;analysis/v54_progression_lesion_state/REPORT.md",
    ),
    (
        "IFN-beta HLA-II/CD74 branch",
        "unchanged_scope",
        "provisional",
        "pharmacodynamic_context_only_for_progression",
        "The branch remains therapy-specific context and cannot substitute for longitudinal disability.",
        "analysis/v36_ms_ifnb_longitudinal_audit/;analysis/v54_transition_identifiability/REPORT.md",
    ),
    (
        "T/B-readable early IFN/APC/STAT1 monitoring state",
        "unchanged_scope",
        "provisional",
        "monitoring_context_only_for_progression",
        "The state remains a replication-gated monitoring audit; no progression endpoint was added.",
        "docs/history/HYPOTHESIS_SLATE_V36.md;analysis/v54_progression_data_inventory/REPORT.md",
    ),
    (
        "Postpartum HLA-II/CD64 APC-arm imbalance",
        "unchanged_scope",
        "provisional",
        "relapse_window_not_disability_progression",
        "Postpartum timing remains data-gated and relapse risk cannot be substituted for disability accumulation.",
        "docs/history/HYPOTHESIS_SLATE_V35.md;analysis/v54_transition_identifiability/REPORT.md",
    ),
    (
        "Complement/lipid progressive axis downgraded",
        "negative_reinforced",
        "negative-established",
        "no_orthogonal_progression_support",
        "V54 targeted lesion tests provide no orthogonally supported complement/lipid progression state.",
        "docs/history/HYPOTHESIS_SLATE_V36.md;analysis/v54_progression_lesion_state/REPORT.md",
    ),
    (
        "Lysosomal APC bottleneck not proven",
        "narrowed_for_progression",
        "provisional",
        "exploratory_morphology_only_no_bottleneck",
        "A local foamy-morphology association fails the global sequential family and donor-estimand checks; bottleneck and progression claims remain unproven.",
        "analysis/v54_post_result_morphology_multiplicity/REPORT.md;analysis/v54_foamy_donor_estimand_audit/REPORT.md",
    ),
    (
        "Metabolic/sterol setpoint is context/confounder axis, not intervention-grade",
        "narrowed_for_progression",
        "provisional",
        "exploratory_morphology_context_only",
        "OXPHOS is morphology-associated only before the global/donor limitations and supplies no progression or intervention direction.",
        "analysis/v54_progression_lesion_module_panel/REPORT.md;analysis/v54_post_result_morphology_multiplicity/REPORT.md",
    ),
    (
        "Multi-lineage and RPT lenses add prioritization, not evidence",
        "method_strengthened",
        "supported",
        "proposal_only_review_changed_grade_after_grounding",
        "Claude/Gemini review added value by triggering a data-grounded morphology downgrade; model output itself remained non-evidence.",
        "analysis/v54_multilineage_progression_review/REPORT.md",
    ),
    (
        "First-principles druggability discipline changed target interpretation",
        "method_strengthened",
        "supported",
        "no_progression_candidate_reached_structure_gate",
        "Zero of nine candidates passed the progression-specific association/direction gate, so structure was correctly not used to decorate a target.",
        "analysis/v54_progression_intervention_direction_map/REPORT.md",
    ),
    (
        "",
        "new_post_v37_item",
        "supported-provisional",
        "cd44_cxcr4_ms_state_not_progression_marker",
        "The replicated MS microglial disease-state association remains real at its bounded scope; V54 found no portable PPMS-versus-SPMS association.",
        "analysis/v53_microglia_cross_cohort_meta/REPORT.md;analysis/v54_progressive_stage_modules/REPORT.md",
    ),
    (
        "",
        "new_post_v37_item",
        "exploratory",
        "foamy_oxphos_lysosomal_state_not_progression",
        "Post-result morphology coefficients do not survive the complete family and are substantially between-donor or unresolved.",
        "analysis/v54_post_result_morphology_multiplicity/REPORT.md;analysis/v54_foamy_donor_estimand_audit/REPORT.md",
    ),
    (
        "",
        "new_post_v37_boundary",
        "supported-boundary",
        "longitudinal_progression_not_identifiable",
        "No held transcriptomic dataset contains time-varying stage plus repeated disability/adjudicated conversion.",
        "analysis/v54_transition_identifiability/REPORT.md",
    ),
    (
        "",
        "new_post_v37_boundary",
        "supported-boundary",
        "cns_peripheral_progression_localization_not_identifiable",
        "No held compartment pair has matched phenotype, outcome window, pairing, and source/composition controls.",
        "analysis/v54_cns_peripheral_identifiability/REPORT.md",
    ),
    (
        "",
        "new_post_v37_negative",
        "negative-established-within-tested-candidates",
        "no_direction_resolved_progression_intervention_route",
        "Zero of nine pre-existing states passes the first progression-specific gate; this closes these routes, not all possible targets.",
        "analysis/v54_progression_intervention_direction_map/REPORT.md",
    ),
    (
        "",
        "new_post_v37_method",
        "supported-method",
        "progression_intake_and_power_ready",
        "Inventory, semantic, blinded preregistration, binary power, and event-time/covariate routes are synthetic-verified and ready for future data.",
        "analysis/v54_progression_package_eligibility_validator/summary.json;analysis/v54_progression_outcome_semantic_checker/summary.json;analysis/v54_progression_event_time_power_design/summary.json",
    ),
]


def main() -> None:
    v37 = pd.read_csv(V37, sep="\t", dtype=str, keep_default_na=False).set_index("item")
    rows = []
    missing_artifacts = []
    missing_v37 = []
    for index, (
        v37_item,
        delta_type,
        current_grade,
        current_status,
        interpretation,
        artifacts,
    ) in enumerate(ROWS, start=1):
        if v37_item and v37_item not in v37.index:
            missing_v37.append(v37_item)
        for artifact in artifacts.split(";"):
            if not (ROOT / artifact).exists():
                missing_artifacts.append(artifact)
        prior = v37.loc[v37_item] if v37_item else None
        rows.append(
            {
                "delta_id": f"V54D{index:02d}",
                "item": v37_item or current_status,
                "v37_relevance": prior["relevance"] if prior is not None else "not_scored_in_v37",
                "v37_novelty": prior["novelty"] if prior is not None else "not_scored_in_v37",
                "v37_evidence_grade": prior["evidence_grade"] if prior is not None else "not_in_v37",
                "v54_current_grade": current_grade,
                "delta_type": delta_type,
                "progression_specific_status": current_status,
                "interpretation": interpretation,
                "supporting_artifacts": artifacts,
            }
        )
    if missing_v37 or missing_artifacts:
        raise RuntimeError(
            f"Delta traceability failed; missing V37={missing_v37}; artifacts={missing_artifacts}"
        )
    OUT.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(rows)
    frame.to_csv(OUT / "progression_evidence_delta.tsv", sep="\t", index=False)
    summary = {
        "purpose": "Artifact-checked progression-specific evidence delta against V37",
        "n_items": len(frame),
        "n_v37_items_carried": int(frame["v37_evidence_grade"].ne("not_in_v37").sum()),
        "n_new_post_v37_items": int(frame["v37_evidence_grade"].eq("not_in_v37").sum()),
        "delta_counts": frame["delta_type"].value_counts().sort_index().to_dict(),
        "traceability_status": "PASS",
        "headline": (
            "No V37 item becomes progression evidence or a target. V54 reinforces selected "
            "negative/method conclusions, narrows architecture and morphology claims, and "
            "adds progression identifiability/readiness boundaries."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
