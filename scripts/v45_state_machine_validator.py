#!/usr/bin/env python3
"""Validate V45 route-state consistency across live operational boards.

This is an operational guard only. It does not read expression matrices,
outcomes, quarantined data, or run any validation harness.
"""

from __future__ import annotations

import argparse
import csv
import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_state_machine_validator/live"

DEFAULTS = {
    "triage": ROOT / "analysis/v45_received_data_triage/received_data_triage_status.tsv",
    "external": ROOT / "analysis/v45_external_blocker_board/external_blocker_board.tsv",
    "followup": ROOT / "analysis/v45_followup_due_board/live_template/followup_due_board.tsv",
    "dashboard": ROOT / "analysis/v45_readiness_status_dashboard/readiness_status_dashboard_summary.json",
}

TRACKER_TO_COHORT_ID = {
    "Gafson_2018_DMF_PBMC_PMID30283812": "gafson_dmf_2018",
    "Karolinska_DMF_ROS_GSE130478_GSE130491_GSE130494": "karolinska_dmf_ros_2019",
    "GSE228330_ocrelizumab_PBMC": "gse228330_ocrelizumab_pbmc",
    "Any_author_run_fallback": "any_author_run_fallback",
}

YES = {"yes", "yes_optional", "yes_if_labels_received"}
NO_DATA = {"", "no", "public_partial", "public_partial_labels_absent", "not_applicable_for_fallback"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage", type=Path, default=DEFAULTS["triage"])
    parser.add_argument("--external", type=Path, default=DEFAULTS["external"])
    parser.add_argument("--followup", type=Path, default=DEFAULTS["followup"])
    parser.add_argument("--dashboard", type=Path, default=DEFAULTS["dashboard"])
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument(
        "--synthetic-case",
        choices=["none", "impossible"],
        default="none",
        help="Apply a labeled synthetic mutation for regression testing.",
    )
    parser.add_argument(
        "--expect-status",
        choices=["PASS", "FAIL"],
        default="PASS",
        help="Expected observed status. Used so synthetic failure fixtures can pass regression.",
    )
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text())


def by_key(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row.get(key, ""): row for row in rows}


def is_yes(value: str) -> bool:
    return value.strip().lower() in YES


def is_no(value: str) -> bool:
    return value.strip().lower() in {"", "no", "not_applicable"}


def route_state(triage: dict[str, str], external: dict[str, str] | None) -> str:
    if is_yes(triage.get("harness_ready", "")):
        return "frozen_harness_ready"
    if is_yes(triage.get("metadata_preflight_passed", "")):
        return "metadata_preflight"
    if triage.get("data_received", "").strip().lower() not in NO_DATA:
        return "package_received"
    if is_yes(triage.get("request_sent", "")) or (external and is_yes(external.get("request_sent", ""))):
        return "request_sent"
    if is_yes(triage.get("request_packet_ready", "")) or triage.get("request_packet_ready", "") == "yes_optional":
        return "request_packet_ready"
    return "uninitialized_or_inconsistent"


def add_violation(
    violations: list[dict[str, str]],
    severity: str,
    cohort_id: str,
    check: str,
    detail: str,
) -> None:
    violations.append(
        {
            "severity": severity,
            "cohort_id": cohort_id,
            "check": check,
            "detail": detail,
        }
    )


def apply_synthetic_case(
    triage: list[dict[str, str]],
    external: list[dict[str, str]],
    followup: list[dict[str, str]],
    dashboard: dict[str, object],
    synthetic_case: str,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], dict[str, object]]:
    triage = deepcopy(triage)
    external = deepcopy(external)
    followup = deepcopy(followup)
    dashboard = deepcopy(dashboard)
    if synthetic_case == "impossible":
        for row in triage:
            if row.get("cohort_id") == "gafson_dmf_2018":
                row["harness_ready"] = "yes"
                row["metadata_preflight_passed"] = "no"
                row["checksum_verified"] = "no"
                row["subject_map_passed"] = "no"
                row["outcome_dictionary_frozen"] = "no"
        for row in external:
            if row.get("cohort_id") == "gafson_dmf_2018":
                row["harness_ready"] = "yes"
                row["blocker_type"] = "external_send_or_author_approval"
                row["request_sent"] = "no"
        for row in followup:
            if TRACKER_TO_COHORT_ID.get(row.get("cohort", ""), "") == "gafson_dmf_2018":
                row["request_sent"] = "yes"
                row["due_status"] = "not_sent_ready"
        dashboard["n_harness_ready"] = 0
        dashboard["headline_status"] = "READY_AWAITING_EXTERNAL_DATA"
    return triage, external, followup, dashboard


def validate(
    triage_rows: list[dict[str, str]],
    external_rows: list[dict[str, str]],
    followup_rows: list[dict[str, str]],
    dashboard: dict[str, object],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    triage_by_id = by_key(triage_rows, "cohort_id")
    external_by_id = by_key(external_rows, "cohort_id")
    followup_by_id = {
        TRACKER_TO_COHORT_ID.get(row.get("cohort", ""), row.get("cohort", "")): row
        for row in followup_rows
    }
    violations: list[dict[str, str]] = []
    route_rows: list[dict[str, str]] = []

    for cohort_id, triage in sorted(triage_by_id.items()):
        external = external_by_id.get(cohort_id)
        followup = followup_by_id.get(cohort_id, {})
        state = route_state(triage, external)
        route_rows.append(
            {
                "cohort_id": cohort_id,
                "derived_state": state,
                "request_packet_ready": triage.get("request_packet_ready", ""),
                "request_sent": triage.get("request_sent", ""),
                "data_received": triage.get("data_received", ""),
                "metadata_preflight_passed": triage.get("metadata_preflight_passed", ""),
                "harness_ready": triage.get("harness_ready", ""),
                "external_blocker_type": external.get("blocker_type", "missing_external_row") if external else "missing_external_row",
                "followup_due_status": followup.get("due_status", "missing_followup_row"),
            }
        )

        if external is None:
            add_violation(violations, "hard", cohort_id, "external_row_missing", "triage cohort is absent from external blocker board")
        if not is_yes(triage.get("request_packet_ready", "")):
            add_violation(violations, "hard", cohort_id, "request_packet_not_ready", "route cannot enter the state machine without a request packet")
        if is_yes(triage.get("harness_ready", "")):
            required = [
                "checksum_verified",
                "metadata_preflight_passed",
                "subject_map_passed",
                "outcome_dictionary_frozen",
            ]
            if triage.get("addendum_required", "").strip().lower() in {"yes", "yes_if_labels_received"}:
                required.append("addendum_committed")
            for column in required:
                if not is_yes(triage.get(column, "")):
                    add_violation(
                        violations,
                        "hard",
                        cohort_id,
                        "harness_ready_missing_gate",
                        f"harness_ready=yes but {column}={triage.get(column, '')!r}",
                    )
            if external and external.get("blocker_type") == "external_send_or_author_approval":
                add_violation(
                    violations,
                    "hard",
                    cohort_id,
                    "harness_ready_external_blocker",
                    "harness_ready=yes conflicts with external_send_or_author_approval",
                )
        if triage.get("data_received", "").strip().lower() in NO_DATA:
            for column in ["terms_captured", "quarantined", "checksum_verified", "metadata_preflight_passed"]:
                if is_yes(triage.get(column, "")):
                    add_violation(
                        violations,
                        "hard",
                        cohort_id,
                        "post_receipt_gate_before_receipt",
                        f"data_received={triage.get('data_received', '')!r} but {column}={triage.get(column, '')!r}",
                    )
        if followup:
            if is_yes(followup.get("request_sent", "")) and followup.get("due_status") == "not_sent_ready":
                add_violation(
                    violations,
                    "hard",
                    cohort_id,
                    "sent_but_not_sent_ready",
                    "follow-up board says request_sent=yes and due_status=not_sent_ready",
                )
            if is_yes(followup.get("request_sent", "")) != is_yes(triage.get("request_sent", "")):
                add_violation(
                    violations,
                    "hard",
                    cohort_id,
                    "request_sent_disagreement",
                    f"triage request_sent={triage.get('request_sent', '')!r}; followup request_sent={followup.get('request_sent', '')!r}",
                )

    for cohort_id, external in sorted(external_by_id.items()):
        if cohort_id == "any_author_run_fallback":
            continue
        if cohort_id not in triage_by_id:
            add_violation(violations, "hard", cohort_id, "triage_row_missing", "external blocker cohort is absent from received-data triage")
        if external.get("blocker_type") == "external_send_or_author_approval":
            if is_yes(external.get("request_sent", "")):
                add_violation(violations, "hard", cohort_id, "external_blocker_sent_conflict", "external-send blocker conflicts with request_sent=yes")
            if is_yes(external.get("harness_ready", "")):
                add_violation(violations, "hard", cohort_id, "external_blocker_harness_conflict", "external-send blocker conflicts with harness_ready=yes")

    triage_harness_ready = sum(1 for row in triage_rows if is_yes(row.get("harness_ready", "")))
    external_harness_ready = sum(1 for row in external_rows if is_yes(row.get("harness_ready", "")))
    dashboard_harness_ready = int(dashboard.get("n_harness_ready", -1))
    if dashboard_harness_ready != triage_harness_ready:
        add_violation(
            violations,
            "hard",
            "dashboard",
            "dashboard_triage_harness_ready_mismatch",
            f"dashboard n_harness_ready={dashboard_harness_ready}; triage count={triage_harness_ready}",
        )
    if external_harness_ready and dashboard_harness_ready == 0:
        add_violation(
            violations,
            "hard",
            "dashboard",
            "dashboard_external_harness_ready_mismatch",
            f"dashboard n_harness_ready=0; external blocker board has {external_harness_ready} harness-ready rows",
        )
    if dashboard.get("headline_status") == "READY_AWAITING_EXTERNAL_DATA" and triage_harness_ready:
        add_violation(
            violations,
            "hard",
            "dashboard",
            "headline_harness_ready_conflict",
            "READY_AWAITING_EXTERNAL_DATA conflicts with at least one harness-ready route",
        )
    return route_rows, violations


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    triage = read_tsv(args.triage)
    external = read_tsv(args.external)
    followup = read_tsv(args.followup)
    dashboard = read_json(args.dashboard)
    triage, external, followup, dashboard = apply_synthetic_case(
        triage, external, followup, dashboard, args.synthetic_case
    )
    route_rows, violations = validate(triage, external, followup, dashboard)

    route_path = outdir / "route_state_validation.tsv"
    violations_path = outdir / "state_machine_violations.tsv"
    write_tsv(
        route_path,
        route_rows,
        [
            "cohort_id",
            "derived_state",
            "request_packet_ready",
            "request_sent",
            "data_received",
            "metadata_preflight_passed",
            "harness_ready",
            "external_blocker_type",
            "followup_due_status",
        ],
    )
    write_tsv(violations_path, violations, ["severity", "cohort_id", "check", "detail"])

    n_hard = sum(1 for row in violations if row["severity"] == "hard")
    observed = "PASS" if n_hard == 0 else "FAIL"
    summary = {
        "synthetic": args.synthetic_case != "none",
        "synthetic_case": args.synthetic_case,
        "purpose": "V45 state-machine transition consistency guard; no biological claim",
        "observed_status": observed,
        "expected_status": args.expect_status,
        "expectation_met": observed == args.expect_status,
        "n_routes": len(route_rows),
        "n_violations": len(violations),
        "n_hard_violations": n_hard,
        "route_states": rel(route_path),
        "violations": rel(violations_path),
        "sources": {
            "triage": rel(args.triage),
            "external": rel(args.external),
            "followup": rel(args.followup),
            "dashboard": rel(args.dashboard),
        },
    }
    (outdir / "state_machine_validator_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["expectation_met"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
