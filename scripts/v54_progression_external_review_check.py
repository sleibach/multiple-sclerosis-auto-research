#!/usr/bin/env python3
"""Check the V54 external-review brief's evidence and claim boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_external_review"
REPORT = ROOT / "docs/reports/PROGRESSION_EXTERNAL_REVIEW_V54.md"
REQUIRED_ARTIFACTS = [
    "docs/history/PROGRESSION_FRONTIER_V54.md",
    "docs/validation/PROGRESSION_COHORT_ACQUISITION_SPEC_V54.md",
    "docs/validation/PROGRESSION_PROSPECTIVE_DESIGN_V54.md",
    "docs/validation/PROGRESSION_ACQUISITION_VOI_V54.md",
    "docs/validation/PROGRESSION_CONFIRMATION_ERROR_V54.md",
    "docs/validation/PROGRESSION_LEAVE_SITE_OUT_PRECISION_V54.md",
    "docs/validation/PROGRESSION_LEAVE_SITE_OUT_PRECISION_EXTENSION_V54.md",
    "docs/validation/PROGRESSION_NEGATIVE_CONTROL_GATE_V54.md",
    "docs/validation/PROGRESSION_CONFIRMATION_PROVENANCE_GATE_V54.md",
    "docs/validation/PROGRESSION_P1_INTAKE_TO_LOCK_V54.md",
    "docs/validation/PROGRESSION_P1_ANALYSIS_RELEASE_GATE_V54.md",
    "docs/validation/PROGRESSION_PRECISION_RECEIPT_ROUTER_V54.md",
    "docs/validation/PROGRESSION_P1_RESULT_INTERPRETATION_GATE_V54.md",
    "docs/validation/PROGRESSION_P1_CANDIDATE_STATE_HANDOFF_V54.md",
    "docs/validation/PROGRESSION_ARTIFACT_INDEX_V54.md",
    "docs/validation/PROGRESSION_COMPUTE_LEDGER_V54.md",
    "analysis/v54_progression_candidate_role_matrix/summary.json",
    "analysis/v54_progression_intervention_direction_map/summary.json",
]
REQUIRED_BOUNDARIES = [
    "no progression-associated molecular state and no therapeutic target",
    "did not produce a route to halting MS progression",
    "Zero of ten known candidate cohorts/packages",
    "A nonlinear diagnostic, subgroup, alternate endpoint, or random control cannot rescue it.",
    "Passing process controls never upgrades the primary result.",
    "Predicted structure was not used",
    "it has not yet found something that halts progression",
    "Release means permission to execute, not evidence.",
    "A bounded pass remains a predictive-association transport result",
    "Unlike compute units are intentionally not summed",
    "Only score identity transfers",
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    text = REPORT.read_text()
    normalized_text = " ".join(text.split())
    missing_artifacts = [path for path in REQUIRED_ARTIFACTS if not (ROOT / path).is_file()]
    missing_references = [path for path in REQUIRED_ARTIFACTS[:-2] if path not in text]
    missing_boundaries = [
        phrase for phrase in REQUIRED_BOUNDARIES if " ".join(phrase.split()) not in normalized_text
    ]
    passed = not (missing_artifacts or missing_references or missing_boundaries)
    summary = {
        "purpose": "Artifact and claim-boundary check for V54 external-review brief",
        "n_required_artifacts": len(REQUIRED_ARTIFACTS),
        "n_missing_artifacts": len(missing_artifacts),
        "n_required_report_references": len(REQUIRED_ARTIFACTS[:-2]),
        "n_missing_report_references": len(missing_references),
        "n_required_claim_boundaries": len(REQUIRED_BOUNDARIES),
        "n_missing_claim_boundaries": len(missing_boundaries),
        "missing_artifacts": missing_artifacts,
        "missing_report_references": missing_references,
        "missing_claim_boundaries": missing_boundaries,
        "overall_status": "PASS" if passed else "FAIL",
        "boundary": "Documentation consistency only; passing creates no progression, target, therapeutic, or biological claim.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    if not passed:
        raise RuntimeError("V54 external-review brief check failed")


if __name__ == "__main__":
    main()
