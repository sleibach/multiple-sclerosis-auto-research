#!/usr/bin/env python3
"""Build and verify the role-based V54 progression artifact index."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_artifact_index"
DOCUMENT = ROOT / "docs/validation/PROGRESSION_ARTIFACT_INDEX_V54.md"

READERS = {"medical", "data_acquisition", "analysis_operator", "method_reviewer"}
CLASSES = {"grounded_analysis", "grounded_review", "method_only_synthetic", "operational_contract"}
AUTHORITIES = {"bounded_evidence", "negative_evidence", "method_behavior_only", "execution_authority_only"}


def row(
    artifact_id: str,
    reader: str,
    lifecycle: str,
    evidence_class: str,
    authority: str,
    artifact: str,
    purpose: str,
    boundary: str,
) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "primary_reader": reader,
        "lifecycle": lifecycle,
        "evidence_class": evidence_class,
        "claim_authority": authority,
        "artifact": artifact,
        "purpose": purpose,
        "boundary": boundary,
    }


ARTIFACTS = [
    row("M01", "medical", "synthesis", "grounded_review", "bounded_evidence", "docs/history/PROGRESSION_FRONTIER_V54.md", "Cumulative progression verdict and method boundary.", "No progression-associated molecular state or tractable progression target is established."),
    row("M02", "medical", "synthesis", "grounded_review", "bounded_evidence", "docs/reports/PROGRESSION_EVIDENCE_DELTA_V54.md", "Changes to the V37 evidence state.", "Scope and grade changes do not create progression evidence or a target."),
    row("M03", "medical", "stage_biology", "grounded_analysis", "negative_evidence", "analysis/v54_progressive_stage_modules/REPORT.md", "Source-adjusted PPMS-versus-SPMS module audit.", "Cross-sectional held data support no portable progression-stage module."),
    row("M04", "medical", "lesion_biology", "grounded_analysis", "negative_evidence", "analysis/v54_progression_lesion_state/REPORT.md", "Lesion and microglial state tests across eligible contexts.", "No orthogonally consistent progression-associated lesion state is established."),
    row("M05", "medical", "therapeutic_triage", "grounded_analysis", "negative_evidence", "analysis/v54_progression_intervention_direction_map/REPORT.md", "Progression-specific intervention-direction screen.", "Zero candidates pass the progression-specific first gate; AlphaFold context is ineligible."),
    row("M06", "medical", "lesion_biology", "grounded_analysis", "negative_evidence", "analysis/v54_foamy_donor_estimand_audit/REPORT.md", "Within-donor audit of foamy-state module effects.", "Sparse within-donor variation does not support either endpoint."),
    row("M07", "medical", "external_review", "grounded_review", "bounded_evidence", "docs/reports/PROGRESSION_EXTERNAL_REVIEW_V54.md", "Skeptic-facing account with falsifiers and acquisition path.", "Artifact-checked synthesis; conditional design references are not empirical effects."),
    row("D01", "data_acquisition", "role_definition", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_COHORT_ACQUISITION_SPEC_V54.md", "Required cohort roles, fields, and fail-closed criteria.", "Receipt does not imply eligibility and no requirement is biological evidence."),
    row("D02", "data_acquisition", "role_definition", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_COHORT_ROLE_MATRIX_V54.md", "Separates P1, P2, and P3 candidate roles.", "Current inventory contains zero eligible candidates in every role."),
    row("D03", "data_acquisition", "prioritization", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_ACQUISITION_VOI_V54.md", "Artifact-bound value-of-information ordering.", "Priority is operational utility, not probability of a positive result."),
    row("D04", "data_acquisition", "request", "operational_contract", "execution_authority_only", "docs/validation/outbound_requests/progression_p1_core_ready_to_send_V54.md", "Generic P1 provider request and handling instructions.", "Requested fields may be unavailable; no cohort is counted usable before verification."),
    row("D05", "data_acquisition", "schema", "operational_contract", "execution_authority_only", "docs/validation/input_schemas/V54_progression_p1_request_response_template.tsv", "Machine-readable provider response template.", "Supplied, not-collected, not-shareable, and unknown remain distinct."),
    row("D06", "data_acquisition", "schema", "operational_contract", "execution_authority_only", "docs/validation/input_schemas/V54_progression_cohort_required_fields.tsv", "Canonical progression cohort field inventory.", "Field presence is checked before values or molecular scores are interpreted."),
    row("D07", "data_acquisition", "intake", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_PACKAGE_ELIGIBILITY_VALIDATOR_V54.md", "Fail-closed package and role validator.", "A passing inventory is only eligible for the next blind gate."),
    row("D08", "data_acquisition", "ascertainment", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_CONFIRMATION_PROVENANCE_GATE_V54.md", "Confirmation-process provenance declaration.", "Auditable dates, reasons, and blinding do not prove adjudication unbiased."),
    row("D09", "data_acquisition", "harmonization", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_SITE_SCORE_CALIBRATION_GATE_V54.md", "Outcome-blind site/score calibration declaration.", "Known scale differences route preprocessing; unknown or post-access choices fail closed."),
    row("A01", "analysis_operator", "preregistration", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_P1_P2_BLINDED_PREREGISTRATION_V54.md", "Frozen P1/P2 questions, endpoints, and analysis families.", "The declaration authorizes only the specified future test and changes no locked rule."),
    row("A02", "analysis_operator", "design", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_PROSPECTIVE_DESIGN_V54.md", "Integrated conditional prospective design.", "Synthetic reference assumptions are not universal sample-size requirements."),
    row("A03", "analysis_operator", "manifest", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_REFERENCE_MANIFEST_V54.md", "Hash-bound gate/source manifest.", "Verification protects the frozen contract; it does not validate a cohort."),
    row("A04", "analysis_operator", "intake", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_COMBINED_INTAKE_GATE_V54.md", "Composes inventory and endpoint semantics.", "Passing preserves blindness and permits only downstream intake checks."),
    row("A05", "analysis_operator", "lock", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_P1_INTAKE_TO_LOCK_V54.md", "Seven-stage package-identity-preserving intake composition.", "Information lock is not a favorable result or progression evidence."),
    row("A06", "analysis_operator", "release", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_P1_ANALYSIS_RELEASE_GATE_V54.md", "Composes lock, confirmation, controls, identity, and manifest hash.", "Release means execute the frozen analysis; it does not mean validation."),
    row("A07", "analysis_operator", "negative_controls", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_NEGATIVE_CONTROL_GATE_V54.md", "Exact seven-control, non-rescuing family.", "Clean controls cannot upgrade the primary and failed controls can only downgrade specificity."),
    row("A08", "analysis_operator", "accrual", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_BLINDED_INFORMATION_MONITOR_V54.md", "Aggregate-only information accrual monitor.", "No efficacy/futility authority and no access to effects, outcomes, or molecular values."),
    row("A09", "analysis_operator", "precision_planning", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_PRECISION_RECEIPT_ROUTER_V54.md", "Routes blinded site/event summaries to tested reference families.", "Every valid route requires cohort-specific simulation and grants no precision claim."),
    row("A10", "analysis_operator", "event_time", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_EVENT_TIME_ASSUMPTION_GATE_V54.md", "Freezes censoring and event-time sensitivities.", "Unknown or outcome-related loss fails closed; a pass is not evidence of noninformative censoring."),
    row("A11", "analysis_operator", "estimand", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_TREATMENT_SWITCH_GATE_V54.md", "Freezes treatment-policy and switch sensitivity estimands.", "Estimands cannot be selected after results and neither universally repairs informative switching."),
    row("A12", "analysis_operator", "diagnostics", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_NONLINEAR_DIAGNOSTIC_GATE_V54.md", "Predeclared non-rescuing nonlinear diagnostic family.", "Diagnostics cannot replace the linear primary or create a post-hoc positive claim."),
    row("A13", "analysis_operator", "composition", "operational_contract", "execution_authority_only", "docs/validation/PROGRESSION_P2_COMPOSITION_ACCEPTANCE_V54.md", "P2 composition-method acceptance gate.", "Expression-only or outcome-selected composition estimates fail closed."),
    row("R01", "method_reviewer", "power", "method_only_synthetic", "method_behavior_only", "analysis/v54_progression_event_time_power_design/REPORT.md", "Stratified Cox reference power and calibration grid.", "Seeded synthetic method behavior only; no empirical MS effect or universal N."),
    row("R02", "method_reviewer", "power", "method_only_synthetic", "method_behavior_only", "docs/validation/PROGRESSION_WEAKER_EFFECT_POWER_V54.md", "Weaker-effect and low-event power sensitivity.", "Effect sizes are planning assumptions, not estimates from MS data."),
    row("R03", "method_reviewer", "ascertainment", "method_only_synthetic", "method_behavior_only", "docs/validation/PROGRESSION_CONFIRMATION_ERROR_V54.md", "Missed/false endpoint confirmation sensitivity.", "Synthetic score-linked error defines an invalidity boundary, not its real prevalence."),
    row("R04", "method_reviewer", "competing_risk", "method_only_synthetic", "method_behavior_only", "analysis/v54_progression_competing_risk_robustness/REPORT.md", "Death/competing-event dependence stress test.", "Synthetic dependence mechanisms do not estimate real competing-risk behavior."),
    row("R05", "method_reviewer", "visit_schedule", "method_only_synthetic", "method_behavior_only", "analysis/v54_progression_visit_schedule_robustness/REPORT.md", "Sparse and informative attendance stress test.", "Synthetic attendance defines method failure modes, not cohort quality."),
    row("R06", "method_reviewer", "measurement", "method_only_synthetic", "method_behavior_only", "analysis/v54_progression_repeated_score_reliability/REPORT.md", "Repeat-measurement reliability and correlated-error grid.", "Utility is conditional on simulated reliability assumptions."),
    row("R07", "method_reviewer", "transport", "method_only_synthetic", "method_behavior_only", "analysis/v54_progression_multisite_transportability/REPORT.md", "Site-stratified transport and leave-site-out sign tests.", "Two synthetic reference designs are not evidence of real transportability."),
    row("R08", "method_reviewer", "precision", "method_only_synthetic", "method_behavior_only", "docs/validation/PROGRESSION_LEAVE_SITE_OUT_PRECISION_V54.md", "Initial every-site confidence-interval audit.", "No tested design through N=1,500 met the frozen precision rule."),
    row("R09", "method_reviewer", "precision", "method_only_synthetic", "method_behavior_only", "docs/validation/PROGRESSION_LEAVE_SITE_OUT_PRECISION_EXTENSION_V54.md", "Upper-range every-site precision extension.", "Conditional first-pass cells are not universal enrollment thresholds."),
    row("R10", "method_reviewer", "harmonization", "method_only_synthetic", "method_behavior_only", "analysis/v54_progression_site_score_harmonization/REPORT.md", "Within-site score scaling stress test.", "Blinded scaling helps severe synthetic mismatch but does not rescue recruitment imbalance."),
    row("R11", "method_reviewer", "ascertainment", "method_only_synthetic", "method_behavior_only", "docs/plans/PROGRESSION_COMBINED_ASCERTAINMENT_CONFIRMATION_V54.md", "Independent confirmation of stacked ascertainment behavior.", "The initial unique-compounding interpretation was withdrawn when a constituent failed."),
    row("R12", "method_reviewer", "interaction", "method_only_synthetic", "method_behavior_only", "analysis/v54_progression_p2_interaction_power/REPORT.md", "P2 composition-interaction calibration and power.", "Readiness is conditional on high-fidelity composition measurement."),
    row("R13", "method_reviewer", "misspecification", "method_only_synthetic", "method_behavior_only", "analysis/v54_progression_linear_misspecification/REPORT.md", "Fixed nonlinear alternatives versus linear Cox.", "The detected U-shaped synthetic pattern does not imply an MS response shape."),
    row("R14", "method_reviewer", "regression", "method_only_synthetic", "method_behavior_only", "analysis/v54_progression_regression_suite/REPORT.md", "One-command executable and claim-boundary regression suite.", "A suite pass establishes repository behavior only, not biology."),
    row("R15", "method_reviewer", "adversarial_review", "grounded_review", "bounded_evidence", "analysis/v54_multilineage_progression_review/REPORT.md", "Grounded disposition of Claude/Gemini objections.", "Models proposed objections; only committed data/method audits determined dispositions."),
]


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    checks: list[dict[str, Any]] = []
    for item in ARTIFACTS:
        path = ROOT / item["artifact"]
        problems: list[str] = []
        if item["artifact_id"] in seen_ids:
            problems.append("duplicate_id")
        if item["artifact"] in seen_paths:
            problems.append("duplicate_path")
        if item["primary_reader"] not in READERS:
            problems.append("invalid_reader")
        if item["evidence_class"] not in CLASSES:
            problems.append("invalid_evidence_class")
        if item["claim_authority"] not in AUTHORITIES:
            problems.append("invalid_claim_authority")
        if not path.is_file():
            problems.append("missing_artifact")
        if "/tmp/" in f"/{item['artifact']}":
            problems.append("tmp_path")
        if len(item["boundary"]) < 30:
            problems.append("weak_boundary")
        seen_ids.add(item["artifact_id"])
        seen_paths.add(item["artifact"])
        checks.append(
            {
                "artifact_id": item["artifact_id"],
                "artifact": item["artifact"],
                "exists": path.is_file(),
                "n_problems": len(problems),
                "problems": ";".join(problems) or "-",
                "pass": not problems,
            }
        )

    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "artifact_index.tsv", ARTIFACTS)
    write_tsv(OUT / "artifact_checks.tsv", checks)

    by_reader = Counter(item["primary_reader"] for item in ARTIFACTS)
    by_class = Counter(item["evidence_class"] for item in ARTIFACTS)
    summary = {
        "purpose": "Role-based navigation across committed V54 progression artifacts",
        "n_artifacts": len(ARTIFACTS),
        "n_missing": sum(not item["exists"] for item in checks),
        "n_invalid": sum(item["n_problems"] > 0 for item in checks),
        "n_readers": len(by_reader),
        "by_reader": dict(sorted(by_reader.items())),
        "by_evidence_class": dict(sorted(by_class.items())),
        "overall_status": "PASS" if all(item["pass"] for item in checks) else "FAIL",
        "boundary": "Navigation and repository-integrity result only; indexing an artifact does not upgrade its evidence or authority.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = [
        "# V54 Progression Artifact Index",
        "",
        "Status: **machine-verified navigation; no evidence upgrade**.",
        "",
        "This index routes readers to the committed artifact that answers their",
        "question. `claim_authority` is controlling: synthetic method behavior and",
        "operational release authority are never biological evidence.",
        "",
        "## Quick Start",
        "",
        "- Medical interpretation: start at `M01`, then inspect the relevant",
        "  grounded negative/bounded analysis (`M03`-`M06`).",
        "- Data owner: start at `D01`, use `D04`/`D05` for response, then run the",
        "  blind intake declarations (`D07`-`D09`).",
        "- Analysis operator: execute `A01` through `A13` in lifecycle order; a",
        "  release or reference-alignment decision is permission, not a result.",
        "- Method reviewer: use `R01`-`R15` for calibration, invalidity boundaries,",
        "  precision, adversarial review, and the one-command regression suite.",
        "",
    ]
    for reader in ("medical", "data_acquisition", "analysis_operator", "method_reviewer"):
        lines.extend(
            [
                f"## {reader.replace('_', ' ').title()}",
                "",
                "| id | lifecycle | evidence class | claim authority | artifact | purpose | boundary |",
                "|---|---|---|---|---|---|---|",
            ]
        )
        for item in ARTIFACTS:
            if item["primary_reader"] != reader:
                continue
            lines.append(
                f"| {item['artifact_id']} | {item['lifecycle']} | {item['evidence_class']} | "
                f"{item['claim_authority']} | `{item['artifact']}` | {item['purpose']} | {item['boundary']} |"
            )
        lines.append("")
    lines.extend(
        [
            "## Verification",
            "",
            "```bash",
            ".venv/bin/python scripts/v54_progression_artifact_index.py",
            "```",
            "",
            "The checker rejects missing/duplicate artifacts, unknown evidence or",
            "authority classes, temporary paths, and absent claim boundaries.",
        ]
    )
    DOCUMENT.parent.mkdir(parents=True, exist_ok=True)
    DOCUMENT.write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))
    if summary["overall_status"] != "PASS":
        raise RuntimeError("V54 progression artifact index failed")


if __name__ == "__main__":
    main()
