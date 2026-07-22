#!/usr/bin/env python3
"""Route blinded V54 site/event summaries without granting validation."""

from __future__ import annotations

import argparse
import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_precision_receipt_router"
PLACEHOLDERS = {"", "unknown", "tbd", "todo", "placeholder", "na", "n/a"}
ALLOWED_ASSUMPTIONS = {1.3, 1.5, 1.7}
ALLOWED_ALLOCATIONS = {"balanced", "imbalanced_60_30_10", "other_predeclared"}
FORBIDDEN_FIELDS = {
    "effect_estimate",
    "effect_direction",
    "p_value",
    "individual_outcomes",
    "molecular_values",
    "efficacy_recommendation",
    "futility_recommendation",
}


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def integer_counts(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and len(value) == 3
        and all(isinstance(item, int) and not isinstance(item, bool) and item >= 0 for item in value.values())
    )


def allocation_matches_counts(allocation: str, counts: dict[str, int]) -> bool:
    total = sum(counts.values())
    if total <= 0 or any(value <= 0 for value in counts.values()):
        return False
    fractions = sorted((value / total for value in counts.values()), reverse=True)
    if allocation == "balanced":
        return max(counts.values()) / min(counts.values()) <= 1.10
    if allocation == "imbalanced_60_30_10":
        return all(abs(observed - expected) <= 0.02 for observed, expected in zip(fractions, (0.60, 0.30, 0.10)))
    return allocation == "other_predeclared"


def validate(declaration: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    blockers: list[str] = []

    def check(field: str, expected: str, passed: bool, observed: Any) -> None:
        checks.append(
            {
                "field": field,
                "expected": expected,
                "observed": json.dumps(observed, sort_keys=True),
                "pass": passed,
            }
        )
        if not passed:
            blockers.append(f"{field}:invalid")

    package_id = declaration.get("package_id")
    check(
        "package_id",
        "non-placeholder text",
        isinstance(package_id, str) and package_id.strip().lower() not in PLACEHOLDERS,
        package_id,
    )
    check("synthetic", "explicit boolean", isinstance(declaration.get("synthetic"), bool), declaration.get("synthetic"))
    check("aggregate_only", "true", declaration.get("aggregate_only") is True, declaration.get("aggregate_only"))
    check("frozen_before_score_access", "true", declaration.get("frozen_before_score_access") is True, declaration.get("frozen_before_score_access"))
    check("scores_accessed", "false", declaration.get("scores_accessed") is False, declaration.get("scores_accessed"))
    check("cohort_specific_simulation_required", "true", declaration.get("cohort_specific_simulation_required") is True, declaration.get("cohort_specific_simulation_required"))
    check("interpretation_not_validation", "true", declaration.get("interpretation_not_validation") is True, declaration.get("interpretation_not_validation"))
    check("precision_claim_requires_every_site_ci", "true", declaration.get("precision_claim_requires_every_site_ci") is True, declaration.get("precision_claim_requires_every_site_ci"))
    assumption = declaration.get("planning_hr_assumption")
    check("planning_hr_assumption", "one frozen tested assumption", assumption in ALLOWED_ASSUMPTIONS, assumption)
    allocation = declaration.get("site_allocation")
    check("site_allocation", "one predeclared allocation class", allocation in ALLOWED_ALLOCATIONS, allocation)
    analyzable = declaration.get("site_analyzable_counts")
    events = declaration.get("site_confirmed_event_counts")
    check("site_analyzable_counts", "three nonnegative integer counts", integer_counts(analyzable), analyzable)
    check("site_confirmed_event_counts", "three nonnegative integer counts", integer_counts(events), events)
    for field in sorted(FORBIDDEN_FIELDS):
        check(field, "absent", field not in declaration, declaration.get(field, "ABSENT"))

    if not blockers:
        assert isinstance(analyzable, dict) and isinstance(events, dict)
        check("site_keys_match", "identical three sites", set(analyzable) == set(events), {"analyzable": sorted(analyzable), "events": sorted(events)})
        check("site_analyzable_positive", "positive analyzable count at every site", all(value > 0 for value in analyzable.values()), analyzable)
        check(
            "site_allocation_matches_counts",
            "declared allocation agrees with observed blinded site counts",
            allocation_matches_counts(allocation, analyzable),
            {"allocation": allocation, "counts": analyzable},
        )
        check("event_counts_within_analyzable", "events <= analyzable at each site", all(events[key] <= analyzable[key] for key in analyzable), events)
        check("analyzable_total", "sum of site counts", declaration.get("analyzable_total") == sum(analyzable.values()), declaration.get("analyzable_total"))
        check("confirmed_event_total", "sum of site events", declaration.get("confirmed_event_total") == sum(events.values()), declaration.get("confirmed_event_total"))

    blockers = sorted(set(blockers))
    if blockers:
        decision = "FAIL_CLOSED"
        event_fraction = None
        minimum_site_events = None
    else:
        total = int(declaration["analyzable_total"])
        confirmed = int(declaration["confirmed_event_total"])
        event_fraction = confirmed / total if total else 0.0
        minimum_site_events = min(events.values())
        balanced_counts = max(analyzable.values()) / max(min(analyzable.values()), 1) <= 1.10
        balanced_precision = (
            assumption == 1.5
            and allocation == "balanced"
            and balanced_counts
            and total >= 1800
            and event_fraction >= 0.30
            and minimum_site_events >= 102
        )
        imbalanced_precision = (
            assumption == 1.5
            and allocation == "imbalanced_60_30_10"
            and total >= 3000
            and event_fraction >= 0.30
            and minimum_site_events >= 137
        )
        sign_reference = (
            assumption == 1.7
            and allocation == "balanced"
            and balanced_counts
            and total >= 450
            and event_fraction >= 0.30
            and minimum_site_events >= 26
        )
        if balanced_precision or imbalanced_precision:
            decision = "TESTED_PRECISION_REFERENCE_REQUIRES_COHORT_SIMULATION"
        elif sign_reference:
            decision = "TESTED_SIGN_REFERENCE_REQUIRES_COHORT_SIMULATION"
        else:
            decision = "VALID_OUTSIDE_TESTED_REFERENCE_REPARAMETERIZE"

    output_dir.mkdir(parents=True, exist_ok=True)
    write_tsv(output_dir / "field_checks.tsv", checks)
    summary = {
        "purpose": "V54 blinded per-site precision receipt router; no biological claim",
        "synthetic": declaration.get("synthetic") is True,
        "package_id": package_id or "",
        "planning_hr_assumption": assumption,
        "event_fraction": event_fraction,
        "minimum_site_events": minimum_site_events,
        "n_blockers": len(blockers),
        "blockers": blockers,
        "decision": decision,
        "boundary": "Reference alignment only; every route requires cohort-specific simulation and creates no validation, progression, precision, or treatment claim.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def base_declaration() -> dict[str, Any]:
    return {
        "synthetic": True,
        "package_id": "SYNTHETIC_PRECISION_PACKAGE_DO_NOT_USE_AS_DATA",
        "aggregate_only": True,
        "frozen_before_score_access": True,
        "scores_accessed": False,
        "cohort_specific_simulation_required": True,
        "interpretation_not_validation": True,
        "precision_claim_requires_every_site_ci": True,
        "planning_hr_assumption": 1.5,
        "site_allocation": "balanced",
        "site_analyzable_counts": {"SITE_A": 600, "SITE_B": 600, "SITE_C": 600},
        "site_confirmed_event_counts": {"SITE_A": 102, "SITE_B": 180, "SITE_C": 258},
        "analyzable_total": 1800,
        "confirmed_event_total": 540,
    }


def synthetic_regression(output_dir: Path) -> dict[str, Any]:
    cases = [
        ("precision_balanced", {}, "TESTED_PRECISION_REFERENCE_REQUIRES_COHORT_SIMULATION"),
        ("precision_imbalanced", {"site_allocation": "imbalanced_60_30_10", "site_analyzable_counts": {"SITE_A": 1800, "SITE_B": 900, "SITE_C": 300}, "site_confirmed_event_counts": {"SITE_A": 500, "SITE_B": 263, "SITE_C": 137}, "analyzable_total": 3000, "confirmed_event_total": 900}, "TESTED_PRECISION_REFERENCE_REQUIRES_COHORT_SIMULATION"),
        ("sign_reference", {"planning_hr_assumption": 1.7, "site_analyzable_counts": {"SITE_A": 150, "SITE_B": 150, "SITE_C": 150}, "site_confirmed_event_counts": {"SITE_A": 26, "SITE_B": 45, "SITE_C": 64}, "analyzable_total": 450, "confirmed_event_total": 135}, "TESTED_SIGN_REFERENCE_REQUIRES_COHORT_SIMULATION"),
        ("hr13_outside", {"planning_hr_assumption": 1.3}, "VALID_OUTSIDE_TESTED_REFERENCE_REPARAMETERIZE"),
        ("low_event_outside", {"site_confirmed_event_counts": {"SITE_A": 50, "SITE_B": 100, "SITE_C": 120}, "confirmed_event_total": 270}, "VALID_OUTSIDE_TESTED_REFERENCE_REPARAMETERIZE"),
        ("n1500_outside", {"site_analyzable_counts": {"SITE_A": 500, "SITE_B": 500, "SITE_C": 500}, "site_confirmed_event_counts": {"SITE_A": 85, "SITE_B": 150, "SITE_C": 215}, "analyzable_total": 1500, "confirmed_event_total": 450}, "VALID_OUTSIDE_TESTED_REFERENCE_REPARAMETERIZE"),
        ("missing_site", {"site_analyzable_counts": {"SITE_A": 900, "SITE_B": 900}}, "FAIL_CLOSED"),
        ("effect_estimate_present", {"effect_estimate": 0.4}, "FAIL_CLOSED"),
        ("score_accessed", {"scores_accessed": True}, "FAIL_CLOSED"),
        ("unknown_assumption", {"planning_hr_assumption": 1.4}, "FAIL_CLOSED"),
        ("mislabeled_imbalance", {"site_allocation": "imbalanced_60_30_10"}, "FAIL_CLOSED"),
    ]
    rows: list[dict[str, Any]] = []
    for name, edits, expected in cases:
        declaration = base_declaration()
        declaration.update(deepcopy(edits))
        declaration["package_id"] = f"SYNTHETIC_{name.upper()}_DO_NOT_USE_AS_DATA"
        fixture = output_dir / "synthetic" / f"{name}.json"
        fixture.parent.mkdir(parents=True, exist_ok=True)
        fixture.write_text(json.dumps(declaration, indent=2) + "\n")
        result = validate(declaration, output_dir / "runs" / name)
        rows.append(
            {
                "fixture": name,
                "synthetic": True,
                "expected_decision": expected,
                "observed_decision": result["decision"],
                "n_blockers": result["n_blockers"],
                "regression_pass": result["decision"] == expected,
            }
        )
    write_tsv(output_dir / "synthetic_regression.tsv", rows)
    n_pass = sum(row["regression_pass"] for row in rows)
    summary = {
        "purpose": "Synthetic regression of V54 per-site precision receipt router",
        "synthetic": True,
        "n_fixtures": len(rows),
        "n_pass": n_pass,
        "n_precision_reference": sum(row["observed_decision"] == "TESTED_PRECISION_REFERENCE_REQUIRES_COHORT_SIMULATION" for row in rows),
        "n_sign_reference": sum(row["observed_decision"] == "TESTED_SIGN_REFERENCE_REQUIRES_COHORT_SIMULATION" for row in rows),
        "n_reparameterize": sum(row["observed_decision"] == "VALID_OUTSIDE_TESTED_REFERENCE_REPARAMETERIZE" for row in rows),
        "n_fail_closed": sum(row["observed_decision"] == "FAIL_CLOSED" for row in rows),
        "overall_status": "PASS" if n_pass == len(rows) else "FAIL",
        "boundary": "Synthetic routing behavior only; no patient data, validation result, progression association, precision claim, or biological evidence.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if summary["overall_status"] != "PASS":
        raise RuntimeError("V54 precision receipt router regression failed")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--declaration", type=Path)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()
    if args.declaration:
        result = validate(json.loads(args.declaration.read_text()), args.output_dir)
        print(json.dumps(result, indent=2))
        if args.fail_on_error and result["decision"] == "FAIL_CLOSED":
            raise SystemExit(1)
    else:
        print(json.dumps(synthetic_regression(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
