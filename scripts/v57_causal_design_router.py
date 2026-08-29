#!/usr/bin/env python3
"""Fail-closed causal estimand router for returned cohort packages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v57_causal_design_router"

ROUTES: dict[str, dict[str, Any]] = {
    "R1_randomized_clinical_effect": {
        "requires": [
            "participant_level",
            "randomized_assignment",
            "concurrent_control",
            "known_time_zero",
            "longitudinal_clinical_outcome",
            "treatment_and_censoring_history",
        ],
        "allows": "intention-to-treat clinical treatment effect after exact primary-result reproduction",
        "forbids": "molecular mechanism or mediator claim without linked repeated molecular data",
    },
    "R2_randomized_molecular_effect": {
        "requires": [
            "participant_level",
            "randomized_assignment",
            "concurrent_control",
            "known_time_zero",
            "baseline_molecular",
            "early_molecular",
            "participant_sample_linkage",
            "batch_and_site_metadata",
        ],
        "allows": "randomized treatment-by-time molecular effect after batch and missingness gates",
        "forbids": "clinical mediation or CNS target engagement from peripheral change alone",
    },
    "R3_active_only_pharmacodynamics": {
        "requires": [
            "participant_level",
            "treated_participants",
            "known_time_zero",
            "baseline_molecular",
            "early_molecular",
            "participant_sample_linkage",
            "batch_and_site_metadata",
        ],
        "allows": "corrected within-participant temporal pharmacodynamic trajectory",
        "forbids": "randomized treatment effect, causal mechanism, mediation, or response classifier",
    },
    "R4_prognostic_monitoring": {
        "requires": [
            "participant_level",
            "treated_participants",
            "baseline_molecular",
            "early_molecular",
            "participant_sample_linkage",
            "prespecified_response_outcome",
            "batch_and_site_metadata",
        ],
        "allows": "external prognostic evaluation of a frozen monitoring rule",
        "forbids": "causal treatment effect, treatment selection, or progression mechanism",
    },
    "R5_randomized_mediation_candidate": {
        "requires": [
            "participant_level",
            "randomized_assignment",
            "concurrent_control",
            "known_time_zero",
            "baseline_molecular",
            "early_molecular",
            "participant_sample_linkage",
            "longitudinal_clinical_outcome",
            "treatment_and_censoring_history",
            "mediator_precedes_outcome",
        ],
        "allows": "pre-registered randomized molecular mediation analysis subject to mediator-outcome assumptions",
        "forbids": "mechanistic proof or mediation claim from cross-cohort or same-time measurements",
    },
    "R6_trial_to_trial_transport_candidate": {
        "requires": [
            "participant_level",
            "randomized_assignment",
            "concurrent_control",
            "known_time_zero",
            "longitudinal_clinical_outcome",
            "target_trial_participant_level",
            "harmonized_endpoint",
            "shared_baseline_modifier_set",
            "selection_provenance",
        ],
        "allows": "transport audit after the frozen overlap guard and target randomized comparison",
        "forbids": "transported effect when overlap fails or exchangeability is unjustified",
    },
}

BASE_FALSE = {
    field: False
    for route in ROUTES.values()
    for field in route["requires"]
}


def declaration(**updates: bool) -> dict[str, bool]:
    result = dict(BASE_FALSE)
    result.update(updates)
    return result


SYNTHETIC_CASES = [
    {
        "case": "randomized_clinical",
        "declaration": declaration(
            participant_level=True,
            treated_participants=True,
            randomized_assignment=True,
            concurrent_control=True,
            known_time_zero=True,
            longitudinal_clinical_outcome=True,
            treatment_and_censoring_history=True,
        ),
        "expected": {"R1_randomized_clinical_effect"},
    },
    {
        "case": "randomized_molecular",
        "declaration": declaration(
            participant_level=True,
            treated_participants=True,
            randomized_assignment=True,
            concurrent_control=True,
            known_time_zero=True,
            longitudinal_clinical_outcome=True,
            treatment_and_censoring_history=True,
            baseline_molecular=True,
            early_molecular=True,
            participant_sample_linkage=True,
            batch_and_site_metadata=True,
            mediator_precedes_outcome=True,
        ),
        "expected": {
            "R1_randomized_clinical_effect",
            "R2_randomized_molecular_effect",
            "R3_active_only_pharmacodynamics",
            "R5_randomized_mediation_candidate",
        },
    },
    {
        "case": "active_only_molecular",
        "declaration": declaration(
            participant_level=True,
            treated_participants=True,
            known_time_zero=True,
            baseline_molecular=True,
            early_molecular=True,
            participant_sample_linkage=True,
            batch_and_site_metadata=True,
        ),
        "expected": {"R3_active_only_pharmacodynamics"},
    },
    {
        "case": "response_monitoring",
        "declaration": declaration(
            participant_level=True,
            treated_participants=True,
            known_time_zero=True,
            baseline_molecular=True,
            early_molecular=True,
            participant_sample_linkage=True,
            prespecified_response_outcome=True,
            batch_and_site_metadata=True,
        ),
        "expected": {
            "R3_active_only_pharmacodynamics",
            "R4_prognostic_monitoring",
        },
    },
    {
        "case": "missing_time_zero",
        "declaration": declaration(
            participant_level=True,
            randomized_assignment=True,
            concurrent_control=True,
            longitudinal_clinical_outcome=True,
            treatment_and_censoring_history=True,
        ),
        "expected": set(),
    },
    {
        "case": "aggregate_only",
        "declaration": declaration(randomized_assignment=True, concurrent_control=True),
        "expected": set(),
    },
    {
        "case": "unharmonized_transport",
        "declaration": declaration(
            participant_level=True,
            randomized_assignment=True,
            concurrent_control=True,
            known_time_zero=True,
            longitudinal_clinical_outcome=True,
            treatment_and_censoring_history=True,
            target_trial_participant_level=True,
            shared_baseline_modifier_set=True,
            selection_provenance=True,
        ),
        "expected": {"R1_randomized_clinical_effect"},
    },
]

CURRENT_ROUTES = [
    {
        "package_route": "Gafson_requested_package",
        "availability": "not_received",
        "design_class": "treated paired molecular response cohort",
        "potential_route_if_complete": "R3_active_only_pharmacodynamics;R4_prognostic_monitoring",
        "not_identifiable": "randomized treatment effect;mediation;progression effect",
        "source_artifact": "docs/validation/PREREGISTRATION_V42.md",
    },
    {
        "package_route": "HERCULES_controlled_clinical_IPD",
        "availability": "requested_not_held",
        "design_class": "randomized progression clinical trial",
        "potential_route_if_complete": "R1_randomized_clinical_effect",
        "not_identifiable": "molecular effect or mediation unless linked molecular substudy exists",
        "source_artifact": "knowledge_external/synthesis/V56_HERCULES_VIVLI_REQUEST.md",
    },
    {
        "package_route": "ToleDYNAMIC_public_default",
        "availability": "enquiry_not_held",
        "design_class": "active-only paired molecular extension",
        "potential_route_if_complete": "R3_active_only_pharmacodynamics",
        "not_identifiable": "current randomized treatment effect;causal mechanism;mediation",
        "source_artifact": "docs/validation/TOLEDYNAMIC_DESIGN_BRANCH_LOCK_V56.json",
    },
    {
        "package_route": "ToleDYNAMIC_both_arm_exception",
        "availability": "requires_explicit_sponsor_documentation",
        "design_class": "randomized paired molecular substudy if exception is documented",
        "potential_route_if_complete": "R2_randomized_molecular_effect;R5_randomized_mediation_candidate_if_linked_later_outcome",
        "not_identifiable": "CNS target engagement or clinical mediation without required linkage and assumptions",
        "source_artifact": "docs/validation/TOLEDYNAMIC_DESIGN_BRANCH_LOCK_V56.json",
    },
    {
        "package_route": "HERCULES_PERSEUS_controlled_pair",
        "availability": "neither_IPD_pair_held",
        "design_class": "two randomized progression trials",
        "potential_route_if_complete": "R1_randomized_clinical_effect;R6_trial_to_trial_transport_candidate",
        "not_identifiable": "transport when endpoints/covariates are not harmonized or overlap fails",
        "source_artifact": "knowledge_external/synthesis/v56_progressive_trial_access_matrix.tsv",
    },
]


def evaluate(payload: dict[str, bool]) -> list[dict[str, Any]]:
    results = []
    for route_id, route in ROUTES.items():
        missing = [field for field in route["requires"] if not payload.get(field, False)]
        results.append(
            {
                "route_id": route_id,
                "eligible": not missing,
                "missing_requirements": ";".join(missing) if missing else "none",
                "allows": route["allows"],
                "forbids": route["forbids"],
            }
        )
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--declaration", type=Path)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    if args.declaration:
        payload = json.loads(args.declaration.read_text())
        result = evaluate(payload)
        print(json.dumps(result, indent=2))
        return

    route_rows = []
    for route_id, route in ROUTES.items():
        route_rows.append(
            {
                "route_id": route_id,
                "required_fields": ";".join(route["requires"]),
                "allows": route["allows"],
                "forbids": route["forbids"],
            }
        )
    pd.DataFrame(route_rows).to_csv(
        args.outdir / "estimand_contracts.tsv", sep="\t", index=False
    )

    current = pd.DataFrame(CURRENT_ROUTES)
    for source in current.source_artifact:
        if not (ROOT / source).exists():
            raise FileNotFoundError(source)
    current.to_csv(args.outdir / "current_route_matrix.tsv", sep="\t", index=False)

    checks = []
    for case in SYNTHETIC_CASES:
        result = evaluate(case["declaration"])
        observed = {row["route_id"] for row in result if row["eligible"]}
        expected = case["expected"]
        checks.append(
            {
                "case": case["case"],
                "expected_routes": ";".join(sorted(expected)) if expected else "none",
                "observed_routes": ";".join(sorted(observed)) if observed else "none",
                "pass": observed == expected,
                "synthetic": True,
            }
        )
    check_frame = pd.DataFrame(checks)
    check_frame.to_csv(args.outdir / "synthetic_route_checks.tsv", sep="\t", index=False)
    passed = bool(check_frame["pass"].all())
    summary = {
        "n_routes": len(ROUTES),
        "n_current_package_routes": len(CURRENT_ROUTES),
        "n_synthetic_cases": len(SYNTHETIC_CASES),
        "n_synthetic_cases_passed": int(check_frame["pass"].sum()),
        "overall_status": "PASS" if passed else "FAIL",
        "verdict": "CAUSAL_DESIGN_ROUTER_VERIFIED" if passed else "CAUSAL_DESIGN_ROUTER_FAILED",
        "boundary": "Route eligibility is not evidence, power, overlap, or a result. Unavailable package fields are never assumed.",
    }
    (args.outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    report = f"""# V57 Causal Design and Estimand Router

## Verification

- Routes: {len(ROUTES)}
- Synthetic declarations: {len(SYNTHETIC_CASES)}
- Exact route matches: {int(check_frame['pass'].sum())}/{len(SYNTHETIC_CASES)}
- Verdict: **{summary['verdict']}**

## Current Design Consequence

- Gafson can evaluate a frozen prognostic monitoring rule and temporal change,
  not a treatment effect.
- HERCULES clinical IPD can estimate a randomized clinical effect if received,
  but cannot identify molecular mediation without linked molecular data.
- The public-default ToleDYNAMIC route supports active-only pharmacodynamics;
  only explicit both-arm documentation can open the randomized molecular route.
- HERCULES-to-PERSEUS transport remains a candidate only after both controlled
  IPD packages, endpoint/covariate harmonization, and the fixed overlap guard.

These are design permissions and prohibitions, not trial or treatment results.
"""
    (args.outdir / "REPORT.md").write_text(report)
    if not passed:
        raise RuntimeError("Synthetic route verification failed")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
