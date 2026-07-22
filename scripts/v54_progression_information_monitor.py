#!/usr/bin/env python3
"""Blinded aggregate information-accrual monitor for V54 progression studies."""

from __future__ import annotations

import argparse
import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_information_monitor"
PLAN_FIELDS = {
    "synthetic",
    "package_id",
    "plan_source",
    "frozen_before_score_outcome_access",
    "scores_accessed_before_freeze",
    "individual_outcomes_accessed_before_freeze",
    "efficacy_stopping_allowed",
    "futility_stopping_allowed",
    "site_analyzable_targets",
    "total_analyzable_target",
    "total_confirmed_event_target",
    "minimum_confirmed_events_per_site",
}
SNAPSHOT_FIELDS = {
    "synthetic",
    "package_id",
    "snapshot_timestamp",
    "site_enrolled_counts",
    "site_analyzable_counts",
    "site_confirmed_event_counts",
    "expected_visit_count",
    "completed_visit_count",
    "pending_confirmation_count",
    "unknown_visit_reason_count",
    "unknown_censoring_reason_count",
    "followup_complete",
}
FORBIDDEN_FIELDS = {
    "effect_direction",
    "effect_estimate",
    "hazard_ratio",
    "coefficient",
    "p_value",
    "q_value",
    "confidence_interval",
    "auc",
    "score_outcome_association",
    "score_strata_outcomes",
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


def nonnegative_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def validate(plan: dict[str, Any], snapshot: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    blockers: list[str] = []
    checks: list[dict[str, Any]] = []

    def check(name: str, expected: str, passed: bool, observed: Any) -> None:
        checks.append(
            {
                "check": name,
                "expected": expected,
                "observed": json.dumps(observed, sort_keys=True),
                "pass": passed,
            }
        )
        if not passed:
            blockers.append(f"{name}:invalid")

    extra_plan = sorted(set(plan) - PLAN_FIELDS)
    extra_snapshot = sorted(set(snapshot) - SNAPSHOT_FIELDS)
    forbidden = sorted((set(plan) | set(snapshot)) & FORBIDDEN_FIELDS)
    check("plan_schema", "no unknown fields", not extra_plan, extra_plan)
    check("snapshot_schema", "no unknown fields", not extra_snapshot, extra_snapshot)
    check("forbidden_efficacy_fields", "none", not forbidden, forbidden)

    package_id = plan.get("package_id")
    check(
        "package_binding",
        "nonempty identical package_id",
        isinstance(package_id, str) and bool(package_id.strip()) and snapshot.get("package_id") == package_id,
        {"plan": package_id, "snapshot": snapshot.get("package_id")},
    )
    check(
        "plan_source",
        "nonempty text",
        isinstance(plan.get("plan_source"), str) and bool(plan["plan_source"].strip()),
        plan.get("plan_source"),
    )
    check(
        "snapshot_timestamp",
        "nonempty text",
        isinstance(snapshot.get("snapshot_timestamp"), str) and bool(snapshot["snapshot_timestamp"].strip()),
        snapshot.get("snapshot_timestamp"),
    )
    check(
        "plan_frozen_blind",
        "true",
        plan.get("frozen_before_score_outcome_access") is True,
        plan.get("frozen_before_score_outcome_access"),
    )
    for field in (
        "scores_accessed_before_freeze",
        "individual_outcomes_accessed_before_freeze",
        "efficacy_stopping_allowed",
        "futility_stopping_allowed",
    ):
        check(field, "false", plan.get(field) is False, plan.get(field))

    site_targets = plan.get("site_analyzable_targets")
    sites_valid = (
        isinstance(site_targets, dict)
        and bool(site_targets)
        and all(isinstance(site, str) and site.strip() for site in site_targets)
        and all(nonnegative_integer(value) and value > 0 for value in site_targets.values())
    )
    check("site_analyzable_targets", "nonempty site->positive integer map", sites_valid, site_targets)
    sites = set(site_targets) if sites_valid else set()

    for field in (
        "total_analyzable_target",
        "total_confirmed_event_target",
        "minimum_confirmed_events_per_site",
    ):
        value = plan.get(field)
        check(field, "positive integer", nonnegative_integer(value) and value > 0, value)
    if sites_valid and nonnegative_integer(plan.get("total_analyzable_target")):
        check(
            "site_target_sum",
            "sum site targets == total analyzable target",
            sum(site_targets.values()) == plan["total_analyzable_target"],
            sum(site_targets.values()),
        )

    count_maps: dict[str, dict[str, int]] = {}
    for field in ("site_enrolled_counts", "site_analyzable_counts", "site_confirmed_event_counts"):
        mapping = snapshot.get(field)
        valid = (
            isinstance(mapping, dict)
            and set(mapping) == sites
            and bool(sites)
            and all(nonnegative_integer(value) for value in mapping.values())
        )
        check(field, "exact site map with nonnegative integer counts", valid, mapping)
        count_maps[field] = mapping if isinstance(mapping, dict) else {}

    count_consistency = bool(sites) and all(
        count_maps["site_confirmed_event_counts"].get(site, -1)
        <= count_maps["site_analyzable_counts"].get(site, -2)
        <= count_maps["site_enrolled_counts"].get(site, -3)
        for site in sites
    )
    check("count_nesting", "events <= analyzable <= enrolled at every site", count_consistency, count_maps)

    scalar_counts = (
        "expected_visit_count",
        "completed_visit_count",
        "pending_confirmation_count",
        "unknown_visit_reason_count",
        "unknown_censoring_reason_count",
    )
    for field in scalar_counts:
        check(field, "nonnegative integer", nonnegative_integer(snapshot.get(field)), snapshot.get(field))
    if nonnegative_integer(snapshot.get("expected_visit_count")) and nonnegative_integer(
        snapshot.get("completed_visit_count")
    ):
        check(
            "visit_count_consistency",
            "completed <= expected",
            snapshot["completed_visit_count"] <= snapshot["expected_visit_count"],
            {
                "expected": snapshot["expected_visit_count"],
                "completed": snapshot["completed_visit_count"],
            },
        )
    check(
        "followup_complete_type",
        "boolean",
        isinstance(snapshot.get("followup_complete"), bool),
        snapshot.get("followup_complete"),
    )

    blockers = sorted(set(blockers))
    unknown_metadata = bool(
        nonnegative_integer(snapshot.get("unknown_visit_reason_count"))
        and snapshot["unknown_visit_reason_count"] > 0
    ) or bool(
        nonnegative_integer(snapshot.get("unknown_censoring_reason_count"))
        and snapshot["unknown_censoring_reason_count"] > 0
    )

    total_analyzable = sum(count_maps["site_analyzable_counts"].values()) if count_maps["site_analyzable_counts"] else 0
    total_events = sum(count_maps["site_confirmed_event_counts"].values()) if count_maps["site_confirmed_event_counts"] else 0
    site_analyzable_met = bool(sites_valid and all(
        count_maps["site_analyzable_counts"].get(site, -1) >= site_targets[site] for site in sites
    ))
    site_events_met = bool(sites_valid and nonnegative_integer(plan.get("minimum_confirmed_events_per_site")) and all(
        count_maps["site_confirmed_event_counts"].get(site, -1)
        >= plan["minimum_confirmed_events_per_site"]
        for site in sites
    ))
    information_reached = bool(
        not blockers
        and not unknown_metadata
        and total_analyzable >= plan["total_analyzable_target"]
        and total_events >= plan["total_confirmed_event_target"]
        and site_analyzable_met
        and site_events_met
        and snapshot.get("followup_complete") is True
        and snapshot.get("pending_confirmation_count") == 0
    )

    if blockers:
        decision = "FAIL_CLOSED_PEEKING_OR_METADATA"
    elif unknown_metadata:
        decision = "HOLD_UNRESOLVED_CENSORING_METADATA"
    elif information_reached:
        decision = "REFERENCE_INFORMATION_REACHED_LOCK_AND_HANDOFF"
    else:
        decision = "CONTINUE_BLINDED_ACCRUAL"

    progress_rows = [
        {
            "metric": "total_analyzable",
            "observed": total_analyzable,
            "target": plan.get("total_analyzable_target"),
            "target_met": total_analyzable >= plan.get("total_analyzable_target", 10**18),
        },
        {
            "metric": "total_confirmed_events",
            "observed": total_events,
            "target": plan.get("total_confirmed_event_target"),
            "target_met": total_events >= plan.get("total_confirmed_event_target", 10**18),
        },
        {
            "metric": "all_site_analyzable_targets",
            "observed": site_analyzable_met,
            "target": True,
            "target_met": site_analyzable_met,
        },
        {
            "metric": "all_site_event_floors",
            "observed": site_events_met,
            "target": True,
            "target_met": site_events_met,
        },
        {
            "metric": "followup_complete",
            "observed": snapshot.get("followup_complete"),
            "target": True,
            "target_met": snapshot.get("followup_complete") is True,
        },
        {
            "metric": "pending_confirmations",
            "observed": snapshot.get("pending_confirmation_count"),
            "target": 0,
            "target_met": snapshot.get("pending_confirmation_count") == 0,
        },
    ]
    output_dir.mkdir(parents=True, exist_ok=True)
    write_tsv(output_dir / "validity_checks.tsv", checks)
    write_tsv(output_dir / "information_progress.tsv", progress_rows)
    summary = {
        "purpose": "V54 blinded aggregate progression information monitor; no biological claim",
        "synthetic": plan.get("synthetic") is True and snapshot.get("synthetic") is True,
        "package_id": package_id,
        "n_validity_checks": len(checks),
        "n_blockers": len(blockers),
        "blockers": blockers,
        "unknown_metadata_hold": unknown_metadata,
        "total_analyzable": total_analyzable,
        "total_confirmed_events": total_events,
        "site_analyzable_targets_met": site_analyzable_met,
        "site_event_floors_met": site_events_met,
        "information_reached": information_reached,
        "efficacy_stopping_authority": False,
        "decision": decision,
        "boundary": (
            "This monitor sees aggregate information counts only and has no efficacy, harm, "
            "futility, association, progression, or biological interpretation authority."
        ),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def base_plan(package_id: str) -> dict[str, Any]:
    return {
        "synthetic": True,
        "package_id": package_id,
        "plan_source": "SYNTHETIC_ONLY/frozen_information_plan.json",
        "frozen_before_score_outcome_access": True,
        "scores_accessed_before_freeze": False,
        "individual_outcomes_accessed_before_freeze": False,
        "efficacy_stopping_allowed": False,
        "futility_stopping_allowed": False,
        "site_analyzable_targets": {"SITE_A": 150, "SITE_B": 150, "SITE_C": 150},
        "total_analyzable_target": 450,
        "total_confirmed_event_target": 135,
        "minimum_confirmed_events_per_site": 10,
    }


def base_snapshot(package_id: str) -> dict[str, Any]:
    return {
        "synthetic": True,
        "package_id": package_id,
        "snapshot_timestamp": "2026-01-01T00:00:00Z",
        "site_enrolled_counts": {"SITE_A": 230, "SITE_B": 230, "SITE_C": 230},
        "site_analyzable_counts": {"SITE_A": 160, "SITE_B": 160, "SITE_C": 160},
        "site_confirmed_event_counts": {"SITE_A": 46, "SITE_B": 46, "SITE_C": 46},
        "expected_visit_count": 5520,
        "completed_visit_count": 5520,
        "pending_confirmation_count": 0,
        "unknown_visit_reason_count": 0,
        "unknown_censoring_reason_count": 0,
        "followup_complete": True,
    }


def synthetic_regression(output_dir: Path) -> dict[str, Any]:
    cases = [
        ("mid_accrual", {}, {"site_enrolled_counts": {"SITE_A": 100, "SITE_B": 100, "SITE_C": 100}, "site_analyzable_counts": {"SITE_A": 80, "SITE_B": 80, "SITE_C": 80}, "site_confirmed_event_counts": {"SITE_A": 20, "SITE_B": 20, "SITE_C": 20}, "followup_complete": False}, "CONTINUE_BLINDED_ACCRUAL"),
        ("pending_confirmation", {}, {"pending_confirmation_count": 7}, "CONTINUE_BLINDED_ACCRUAL"),
        ("site_shortfall", {}, {"site_enrolled_counts": {"SITE_A": 300, "SITE_B": 230, "SITE_C": 100}, "site_analyzable_counts": {"SITE_A": 250, "SITE_B": 180, "SITE_C": 50}}, "CONTINUE_BLINDED_ACCRUAL"),
        ("information_reached", {}, {}, "REFERENCE_INFORMATION_REACHED_LOCK_AND_HANDOFF"),
        ("unknown_censor_reason", {}, {"unknown_censoring_reason_count": 2}, "HOLD_UNRESOLVED_CENSORING_METADATA"),
        ("p_value_peeking", {}, {"p_value": 0.01}, "FAIL_CLOSED_PEEKING_OR_METADATA"),
        ("effect_direction_peeking", {}, {"effect_direction": "protective"}, "FAIL_CLOSED_PEEKING_OR_METADATA"),
        ("negative_count", {}, {"site_confirmed_event_counts": {"SITE_A": 46, "SITE_B": -1, "SITE_C": 46}}, "FAIL_CLOSED_PEEKING_OR_METADATA"),
        ("package_mismatch", {}, {"package_id": "SYNTHETIC_DIFFERENT_PACKAGE"}, "FAIL_CLOSED_PEEKING_OR_METADATA"),
        ("efficacy_stopping_enabled", {"efficacy_stopping_allowed": True}, {}, "FAIL_CLOSED_PEEKING_OR_METADATA"),
    ]
    rows: list[dict[str, Any]] = []
    fixture_root = output_dir / "synthetic"
    for name, plan_edits, snapshot_edits, expected in cases:
        package_id = f"SYNTHETIC_{name.upper()}_DO_NOT_USE_AS_DATA"
        plan = base_plan(package_id)
        snapshot = base_snapshot(package_id)
        plan.update(deepcopy(plan_edits))
        snapshot.update(deepcopy(snapshot_edits))
        plan_path = fixture_root / "plans" / f"{name}.json"
        snapshot_path = fixture_root / "snapshots" / f"{name}.json"
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(json.dumps(plan, indent=2) + "\n")
        snapshot_path.write_text(json.dumps(snapshot, indent=2) + "\n")
        result = validate(plan, snapshot, output_dir / "runs" / name)
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
        "purpose": "Synthetic regression of V54 blinded information-accrual monitor",
        "synthetic": True,
        "n_fixtures": len(rows),
        "n_pass": n_pass,
        "n_information_reached": sum(row["observed_decision"] == "REFERENCE_INFORMATION_REACHED_LOCK_AND_HANDOFF" for row in rows),
        "n_continue": sum(row["observed_decision"] == "CONTINUE_BLINDED_ACCRUAL" for row in rows),
        "n_hold": sum(row["observed_decision"] == "HOLD_UNRESOLVED_CENSORING_METADATA" for row in rows),
        "n_fail_closed": sum(row["observed_decision"] == "FAIL_CLOSED_PEEKING_OR_METADATA" for row in rows),
        "efficacy_stopping_authority": False,
        "overall_status": "PASS" if n_pass == len(rows) else "FAIL",
        "boundary": "Synthetic monitor behavior only; no patient data, effect, progression, or biological claim.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if summary["overall_status"] != "PASS":
        raise RuntimeError("V54 information-monitor regression failed")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()
    if bool(args.plan) != bool(args.snapshot):
        parser.error("--plan and --snapshot must be supplied together")
    if args.plan:
        result = validate(json.loads(args.plan.read_text()), json.loads(args.snapshot.read_text()), args.output_dir)
        print(json.dumps(result, indent=2))
        if args.fail_on_error and result["decision"].startswith("FAIL_CLOSED"):
            raise SystemExit(1)
    else:
        print(json.dumps(synthetic_regression(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
