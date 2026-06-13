#!/usr/bin/env python3
"""Generate the current V45 operational action card.

The card is a read-only synthesis of existing readiness/blocker boards. It does
not send requests, update trackers, inspect data, or run validation.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_current_action_card"
DEFAULTS = {
    "external": ROOT / "analysis/v45_external_blocker_board/external_blocker_board.tsv",
    "followup": ROOT / "analysis/v45_followup_due_board/live_template/followup_due_board.tsv",
    "dashboard": ROOT / "analysis/v45_readiness_status_dashboard/readiness_status_dashboard_summary.json",
    "state_validator": ROOT / "analysis/v45_state_machine_validator/live/state_machine_validator_summary.json",
    "packet_integrity": ROOT / "analysis/v45_route_packet_integrity_manifest/live/route_packet_integrity_summary.json",
    "precommit": ROOT / "analysis/v45_precommit_readiness/precommit_readiness_summary.json",
    "returned_package_regression": ROOT / "analysis/v46_returned_package_regression_suite/returned_package_regression_summary.json",
    "operator_smoke": ROOT / "analysis/v46_operator_smoke_test_bundle/operator_smoke_test_summary.json",
}

TRACKER_TO_COHORT_ID = {
    "Gafson_2018_DMF_PBMC_PMID30283812": "gafson_dmf_2018",
    "Karolinska_DMF_ROS_GSE130478_GSE130491_GSE130494": "karolinska_dmf_ros_2019",
    "GSE228330_ocrelizumab_PBMC": "gse228330_ocrelizumab_pbmc",
    "Any_author_run_fallback": "any_author_run_fallback",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
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
    return json.loads(path.read_text()) if path.exists() else {}


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_actions() -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, object]]:
    external_rows = read_tsv(DEFAULTS["external"])
    followup_rows = read_tsv(DEFAULTS["followup"])
    dashboard = read_json(DEFAULTS["dashboard"])
    state_validator = read_json(DEFAULTS["state_validator"])
    packet_integrity = read_json(DEFAULTS["packet_integrity"])
    precommit = read_json(DEFAULTS["precommit"])
    returned_package_regression = read_json(DEFAULTS["returned_package_regression"])
    operator_smoke = read_json(DEFAULTS["operator_smoke"])

    guard_rows = [
        {
            "guard": "precommit_readiness",
            "status": str(precommit.get("overall_status", "MISSING")),
            "source": rel(DEFAULTS["precommit"]),
        },
        {
            "guard": "state_machine_transition_validator",
            "status": str(state_validator.get("observed_status", "MISSING")),
            "source": rel(DEFAULTS["state_validator"]),
        },
        {
            "guard": "route_packet_integrity",
            "status": str(packet_integrity.get("observed_status", "MISSING")),
            "source": rel(DEFAULTS["packet_integrity"]),
        },
        {
            "guard": "v46_returned_package_regression_suite",
            "status": str(returned_package_regression.get("overall_status", "MISSING")),
            "source": rel(DEFAULTS["returned_package_regression"]),
        },
        {
            "guard": "v46_operator_smoke_test_bundle",
            "status": str(operator_smoke.get("overall_status", "MISSING")),
            "source": rel(DEFAULTS["operator_smoke"]),
        },
    ]
    internal_block = any(row["status"] not in {"PASS", "EXPECTED_FAIL"} for row in guard_rows)

    followup_by_id = {
        TRACKER_TO_COHORT_ID.get(row.get("cohort", ""), row.get("cohort", "")): row
        for row in followup_rows
    }
    actions: list[dict[str, str]] = []
    if internal_block:
        actions.append(
            {
                "priority": "0",
                "cohort_id": "internal_guards",
                "action_type": "repair_internal_guard",
                "recommended_action": "repair failing guard before any external send or received-data work",
                "request_or_packet": "",
                "recipient_or_path": "",
                "blocker": "internal_guard_failure",
                "why_now": "a readiness guard is not passing",
            }
        )
    else:
        for row in external_rows:
            cohort_id = row.get("cohort_id", "")
            followup = followup_by_id.get(cohort_id, {})
            priority = followup.get("priority", "99")
            if row.get("harness_ready") == "yes":
                action_type = "review_harness_ready_before_scoring"
                why_now = "a route claims harness-ready status"
            elif row.get("blocker_type") == "external_send_or_author_approval":
                action_type = "send_or_approve_external_request"
                why_now = "route is internally prepared but externally blocked"
            elif row.get("request_sent") == "yes":
                action_type = "wait_or_follow_up"
                why_now = "request has already been sent"
            else:
                action_type = "review_route_state"
                why_now = "route has nonstandard blocker state"
            actions.append(
                {
                    "priority": priority,
                    "cohort_id": cohort_id,
                    "action_type": action_type,
                    "recommended_action": row.get("recommended_action") or followup.get("recommended_action", ""),
                    "request_or_packet": row.get("request_packet") or followup.get("prepared_request", ""),
                    "recipient_or_path": followup.get("recipient_or_path", ""),
                    "blocker": row.get("external_blocker") or row.get("triage_current_blocker", ""),
                    "why_now": why_now,
                }
            )
    actions.sort(key=lambda row: (int(row["priority"]) if row["priority"].isdigit() else 99, row["cohort_id"]))

    summary = {
        "synthetic": False,
        "purpose": "V45 current operational action card; no biological claim",
        "headline_status": dashboard.get("headline_status", "MISSING"),
        "n_actions": len(actions),
        "n_external_send_or_approval": sum(1 for row in actions if row["action_type"] == "send_or_approve_external_request"),
        "n_internal_guard_blocks": 1 if internal_block else 0,
        "guard_statuses": {row["guard"]: row["status"] for row in guard_rows},
    }
    return actions, guard_rows, summary


def write_markdown(path: Path, actions: list[dict[str, str]], guard_rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    lines = [
        "# V45 Current Action Card",
        "",
        "Status: generated operational card. No biological claim.",
        "",
        f"Headline status: `{summary['headline_status']}`",
        "",
        "## Guard Status",
        "",
        "| Guard | Status | Source |",
        "|---|---|---|",
    ]
    for row in guard_rows:
        lines.append(f"| {row['guard']} | `{row['status']}` | `{row['source']}` |")
    lines.extend(
        [
            "",
            "## Current Actions",
            "",
            "| Priority | Route | Action | Request/Packet | Why now |",
            "|---:|---|---|---|---|",
        ]
    )
    for row in actions:
        lines.append(
            f"| {row['priority']} | `{row['cohort_id']}` | `{row['recommended_action']}` | `{row['request_or_packet']}` | {row['why_now']} |"
        )
    lines.extend(
        [
            "",
            "This card does not mark requests as sent, mark data as received, or make any",
            "cohort harness-ready. It is a navigation layer over existing boards.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    actions, guard_rows, summary = build_actions()

    action_path = outdir / "current_action_card.tsv"
    guard_path = outdir / "current_action_guard_status.tsv"
    markdown_path = outdir / "CURRENT_ACTION_CARD.md"
    write_tsv(
        action_path,
        actions,
        [
            "priority",
            "cohort_id",
            "action_type",
            "recommended_action",
            "request_or_packet",
            "recipient_or_path",
            "blocker",
            "why_now",
        ],
    )
    write_tsv(guard_path, guard_rows, ["guard", "status", "source"])
    write_markdown(markdown_path, actions, guard_rows, summary)
    summary.update(
        {
            "actions": rel(action_path),
            "guards": rel(guard_path),
            "markdown": rel(markdown_path),
        }
    )
    (outdir / "current_action_card_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
