#!/usr/bin/env python3
"""Ground every V54 progression-review objection against committed artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "knowledge_external/model_outputs/v54_progression_review"
OUT = ROOT / "analysis/v54_multilineage_progression_review"


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


GROUNDING: dict[str, dict[str, Any]] = {
    "claude:OBJ1": {
        "grounded_outcome": "held_changes_evidential_grade",
        "disposition": "valid_selection_risk_confirmed",
        "evidence": "Holm across the complete 12-test post-result morphology sequence leaves only a partial resident-adjusted variant passing; the required fully adjusted lysosomal and both mutual-adjustment endpoints fail.",
        "artifacts": "analysis/v54_post_result_morphology_multiplicity/global_post_result_family.tsv;analysis/v54_post_result_morphology_multiplicity/summary.json",
        "changes_evidential_grade": True,
    },
    "claude:OBJ2": {
        "grounded_outcome": "failed_as_positive_heterogeneity_claim",
        "disposition": "concrete_check_completed",
        "evidence": "No five-module source-by-stage interaction passes HC3, 300,000 reduced-model wild nulls, BH, and max-T. CD44/CXCR4 source effects are similar but individually imprecise.",
        "artifacts": "analysis/v54_progressive_stage_source_interaction/interaction_tests.tsv;analysis/v54_progressive_stage_source_interaction/source_effects_lodo.tsv",
        "changes_evidential_grade": False,
    },
    "claude:OBJ3": {
        "grounded_outcome": "already_addressed",
        "disposition": "requested_safeguard_already_committed",
        "evidence": "The actual family contains six, not five, modules. CD44/CXCR4 3/3 has exact two-sided p=0.25, BH q=0.50, max-T p=0.25, and is explicitly descriptive/inconclusive.",
        "artifacts": "analysis/v54_progression_lesion_state/gse180759_active_inactive_exact_tests.tsv;analysis/v54_progression_lesion_state/cross_context_outcomes.tsv",
        "changes_evidential_grade": False,
    },
    "claude:OBJ4": {
        "grounded_outcome": "already_addressed",
        "disposition": "fail_closed_contract_already_committed",
        "evidence": "GSE228330 is formally ineligible and context-only until its subject map, expression, batch, composition, and disability fields pass the P1/P2 contract; the ready-unsent addendum names every blocker.",
        "artifacts": "analysis/v54_cns_peripheral_identifiability/summary.json;docs/validation/PROGRESSION_COHORT_ACQUISITION_SPEC_V54.md;docs/validation/outbound_requests/gse228330_progression_metadata_addendum_V54.md",
        "changes_evidential_grade": False,
    },
    "claude:OBJ5": {
        "grounded_outcome": "calibration_concern_failed_label_noise_concern_held",
        "disposition": "two_part_check_completed",
        "evidence": "The 0.060 null maximum is 90/1,500 with Wilson CI 0.049-0.073; no cell lower bound exceeds 0.05 and the 48-cell reference max-tail is 0.895. Separate 5%/10% label-noise runs materially reduce power and tighten acquisition requirements.",
        "artifacts": "analysis/v54_progression_power_calibration_audit/summary.json;analysis/v54_progression_power_label_noise/summary.json",
        "changes_evidential_grade": False,
    },
    "claude:OBJ6": {
        "grounded_outcome": "already_addressed_with_traceability_tightening",
        "disposition": "objection_conflates_sequential_gates",
        "evidence": "The 0/9 result is determined entirely by the frozen first progression-specific gate. Downstream V53 context uses explicit numeric and corrected rules but cannot rescue a first-gate failure; no threshold was created after the V54 result.",
        "artifacts": "docs/plans/PROGRESSION_INTERVENTION_DIRECTION_MAP_V54.md;analysis/v54_progression_intervention_direction_map/gate_counts.tsv;scripts/v53_network_control_probe.py;scripts/v53_combinatorial_intervention_probe.py;analysis/v53_causal_identifiability_sensitivity/summary.json",
        "changes_evidential_grade": False,
    },
    "gemini:STATIC_PROGRESSION_LEAP": {
        "grounded_outcome": "proposal_rejected_semantic_and_artifact_mismatch",
        "disposition": "targets_a_claim_not_made",
        "evidence": "V54 explicitly prohibits ordering cross-sectional stage and morphology states as temporal progression. The committed inputs are not a shared cell-level trajectory object, and pseudotime cannot manufacture disability time or conversion labels.",
        "artifacts": "analysis/v54_progression_data_inventory/progression_question_semantic_contract.tsv;analysis/v54_transition_identifiability/transition_identifiability.tsv",
        "changes_evidential_grade": False,
    },
    "gemini:PM_INTERACTION_FAILURE": {
        "grounded_outcome": "failed_as_positive_heterogeneity_claim",
        "disposition": "concrete_check_completed",
        "evidence": "Formal source-by-stage interactions were run for all five modules. None passes. The source/tissue-confounded heterogeneity hypothesis is therefore unsupported, not converted into a positive finding.",
        "artifacts": "analysis/v54_progressive_stage_source_interaction/interaction_tests.tsv",
        "changes_evidential_grade": False,
    },
    "gemini:MORPH_LODO_CONFUSION": {
        "grounded_outcome": "held_changes_morphology_interpretation",
        "disposition": "concern_valid_proposed_test_replaced",
        "evidence": "The proposed Fisher test is invalid for repeated multi-class samples. A donor-FE audit shows only 6/21 donors and 3/43 donor-lesion blocks vary in morphology; OXPHOS is direction-retained but null/unstable and lysosomal reverses near zero within donors.",
        "artifacts": "analysis/v54_foamy_donor_estimand_audit/within_donor_tests.tsv;analysis/v54_foamy_donor_estimand_audit/donor_lesion_morphology_coverage.tsv",
        "changes_evidential_grade": True,
    },
    "gemini:INTERACTION_MODEL_INSTABILITY": {
        "grounded_outcome": "partly_held_wording_already_bounded",
        "disposition": "influence_check_completed",
        "evidence": "Donor deletion flips signs around near-zero interactions, but no deletion changes either coefficient by more than one committed cluster SE. This supports under-resolution, not a donor-specific interaction finding or a valid pooled upgrade.",
        "artifacts": "analysis/v54_foamy_donor_estimand_audit/interaction_donor_influence.tsv;analysis/v54_foamy_lesion_heterogeneity/interaction_tests.tsv",
        "changes_evidential_grade": False,
    },
    "gemini:SIMULATION_ASSUMPTION_BLINDNESS": {
        "grounded_outcome": "partly_held_design_sensitivity_added",
        "disposition": "assumptions_were_disclosed_requested_empirical_mapping_rejected",
        "evidence": "The committed config already lists every parameter. Cross-sectional lesion variance cannot estimate progression-event noise. Prespecified 5%/10% synthetic label-error runs nonetheless show material power loss and make endpoint adjudication mandatory.",
        "artifacts": "analysis/v54_progression_event_power_design/simulation_config.json;analysis/v54_progression_power_label_noise/summary.json;docs/plans/PROGRESSION_POWER_CALIBRATION_AND_LABEL_NOISE_V54.md",
        "changes_evidential_grade": False,
    },
    "gemini:PERIPHERAL_ANALYSIS_AVOIDANCE": {
        "grounded_outcome": "blocked_and_fail_closed",
        "disposition": "proposal_not_executable_and_not_informative",
        "evidence": "The proposal itself requires the absent processed matrix and verified subject map. Subtype and activity are imbalanced, and batch, age, composition, and disability are absent. Running a residual-confounded score would create rather than reduce a degree of freedom.",
        "artifacts": "analysis/v54_cns_peripheral_identifiability/compartment_evidence_matrix.tsv;analysis/v54_cns_peripheral_identifiability/gse228330_baseline_confounding.tsv;docs/validation/outbound_requests/gse228330_progression_metadata_addendum_V54.md",
        "changes_evidential_grade": False,
    },
}


def load_objections(source: str) -> list[dict[str, Any]]:
    record = json.loads((MODEL_DIR / f"{source}_record.json").read_text())
    objections = record.get("objections")
    if not isinstance(objections, list) or len(objections) != 6:
        raise RuntimeError(f"Expected six objections for {source}")
    return objections


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for source in ("claude", "gemini"):
        for objection in load_objections(source):
            key = f"{source}:{objection['id']}"
            if key not in GROUNDING:
                raise KeyError(f"No grounded disposition for {key}")
            disposition = GROUNDING[key]
            rows.append(
                {
                    "source": source,
                    "objection_id": objection["id"],
                    "target_claim": objection["target_claim"],
                    **disposition,
                    "changes_progression_or_target_verdict": False,
                }
            )
    if len(rows) != 12 or set(GROUNDING) != {
        f"{row['source']}:{row['objection_id']}" for row in rows
    }:
        raise RuntimeError("Objection grounding is incomplete")
    write_tsv(OUT / "objection_grounding.tsv", rows)

    clusters = [
        {
            "cluster": "source_by_stage_heterogeneity",
            "sources": "claude;gemini",
            "objections": "OBJ2;PM_INTERACTION_FAILURE",
            "priority_basis": "multi_lineage_agreement",
            "grounded_outcome": "no_supported_interaction",
            "evidence": "analysis/v54_progressive_stage_source_interaction/interaction_tests.tsv",
        },
        {
            "cluster": "morphology_selection_and_estimand",
            "sources": "claude;gemini",
            "objections": "OBJ1;MORPH_LODO_CONFUSION;INTERACTION_MODEL_INSTABILITY",
            "priority_basis": "complementary_concerns",
            "grounded_outcome": "global_family_fails_and_within_donor_estimand_not_supported",
            "evidence": "analysis/v54_post_result_morphology_multiplicity/summary.json;analysis/v54_foamy_donor_estimand_audit/summary.json",
        },
        {
            "cluster": "synthetic_power_design",
            "sources": "claude;gemini",
            "objections": "OBJ5;SIMULATION_ASSUMPTION_BLINDNESS",
            "priority_basis": "multi_lineage_agreement",
            "grounded_outcome": "null_calibration_acceptable_but_label_error_material",
            "evidence": "analysis/v54_progression_power_calibration_audit/summary.json;analysis/v54_progression_power_label_noise/summary.json",
        },
        {
            "cluster": "peripheral_fail_closed_boundary",
            "sources": "claude;gemini",
            "objections": "OBJ4;PERIPHERAL_ANALYSIS_AVOIDANCE",
            "priority_basis": "shared_degree_of_freedom_question",
            "grounded_outcome": "already_fail_closed_missing_artifacts_requested",
            "evidence": "analysis/v54_cns_peripheral_identifiability/summary.json;docs/validation/outbound_requests/gse228330_progression_metadata_addendum_V54.md",
        },
    ]
    write_tsv(OUT / "agreement_clusters.tsv", clusters)

    n_grade_changes = sum(bool(row["changes_evidential_grade"]) for row in rows)
    summary = {
        "purpose": "Artifact-grounded disposition of all V54 multi-lineage objections",
        "model_objections": len(rows),
        "lineages": 2,
        "objections_changing_evidential_grade": n_grade_changes,
        "objections_changing_progression_or_target_verdict": 0,
        "model_spend": "not exposed by the current SAP AI Core client response path",
        "overall_verdict": "REVIEW_ADDED_VALUE_BY_DOWNGRADING_POST_RESULT_MORPHOLOGY",
        "boundary": "Model agreement prioritized checks; only committed analyses determined every disposition.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = [
        "# V54 Multi-Lineage Progression Review: Grounded Dispositions",
        "",
        "Claude and Gemini supplied 12 proposal-only objections. Their agreement only "
        "ordered the checks; the table below reports the committed-data result.",
        "",
        "| source | objection | grounded outcome | grade changed | evidence |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['source']} | {row['objection_id']} | {row['grounded_outcome']} | "
            f"{str(bool(row['changes_evidential_grade'])).lower()} | "
            f"{row['evidence']} |"
        )
    lines.extend(
        [
            "",
            "## Methodological Value",
            "",
            "The review added real value. Claude's global-family objection and Gemini's "
            "donor-estimand concern survived grounding. Together they downgrade the "
            "pooled OXPHOS/lysosomal morphology state from a bounded, locally gate-passing "
            "association to an exploratory post-result, substantially between-donor or "
            "unresolved pattern. No progression or target verdict changes because the "
            "state had never passed those gates.",
            "",
            "The agreed source-by-stage concern did not ground as positive heterogeneity. "
            "The power maximum was calibrated, while label-noise sensitivity materially "
            "tightened the future cohort design. Peripheral analysis remains correctly "
            "fail-closed because its required inputs are absent.",
            "",
            "No model commentary is evidence, and model spend was not exposed by the "
            "current SAP AI Core response path.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
