#!/usr/bin/env python3
"""Generate the V45 first-24h received-package decision tree.

This is an operator/navigation artifact. It reads only existing operational
boards and summaries. It does not inspect received files, expression matrices,
clinical labels, or run validation.
"""

from __future__ import annotations

import argparse
import csv
import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_received_package_decision_tree/live"
DEFAULTS = {
    "actions": ROOT / "analysis/v45_current_action_card/current_action_card.tsv",
    "state_rows": ROOT / "analysis/v45_state_machine_validator/live/route_state_validation.tsv",
    "state_summary": ROOT / "analysis/v45_state_machine_validator/live/state_machine_validator_summary.json",
}

ARRIVAL_PACKET = {
    "gafson_dmf_2018": "analysis/v45_route_arrival_packets/gafson_dmf_2018_arrival_packet.md",
    "karolinska_dmf_ros_2019": "analysis/v45_route_arrival_packets/karolinska_dmf_ros_2019_arrival_packet.md",
    "gse228330_ocrelizumab_pbmc": "analysis/v45_route_arrival_packets/gse228330_ocrelizumab_pbmc_arrival_packet.md",
    "any_author_run_fallback": "analysis/v45_route_arrival_packets/any_author_run_fallback_arrival_packet.md",
}

STATUS_UPDATER_ROLE = {
    "gafson_dmf_2018": "primary_V22_V42_validation",
    "karolinska_dmf_ros_2019": "secondary_MS_DMF_label_path",
    "gse228330_ocrelizumab_pbmc": "pharmacodynamic_context_optional_label_request",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--actions", type=Path, default=DEFAULTS["actions"])
    parser.add_argument("--state-rows", type=Path, default=DEFAULTS["state_rows"])
    parser.add_argument("--state-summary", type=Path, default=DEFAULTS["state_summary"])
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument(
        "--synthetic-case",
        choices=["none", "premature_harness_ready"],
        default="none",
        help="Apply a labeled synthetic mutation for regression testing.",
    )
    parser.add_argument("--expect-status", choices=["PASS", "FAIL"], default="PASS")
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def status_update_command(cohort_id: str) -> str:
    role = STATUS_UPDATER_ROLE.get(cohort_id)
    if not role:
        return "use AUTHOR_RUN_RETURN_OPERATOR_CHECKLIST_V45.md for aggregate author-run returns"
    return (
        ".venv/bin/python scripts/v45_received_status_updater.py "
        f"--cohort-id {cohort_id} --role {role} "
        "--operator-status <filled_first_24h_operator_status.tsv> "
        f"--outdir analysis/received_status_updater/{cohort_id}"
    )


def next_if_arrives(cohort_id: str) -> str:
    if cohort_id == "any_author_run_fallback":
        return "run author-run return redaction/completeness gate on aggregate output package only"
    return "quarantine files, capture terms, write checksums, fill first-24h operator status, then run received-status updater"


def apply_synthetic_case(
    actions: list[dict[str, str]],
    states: list[dict[str, str]],
    state_summary: dict[str, object],
    synthetic_case: str,
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, object]]:
    actions = deepcopy(actions)
    states = deepcopy(states)
    state_summary = deepcopy(state_summary)
    if synthetic_case == "premature_harness_ready":
        for row in actions:
            if row.get("cohort_id") == "gafson_dmf_2018":
                row["action_type"] = "review_harness_ready_before_scoring"
                row["why_now"] = "SYNTHETIC premature harness-ready mutation"
        for row in states:
            if row.get("cohort_id") == "gafson_dmf_2018":
                row["derived_state"] = "request_packet_ready"
                row["harness_ready"] = "yes"
        state_summary["observed_status"] = "PASS"
    return actions, states, state_summary


def main() -> int:
    args = parse_args()
    actions_path = resolve(args.actions)
    states_path = resolve(args.state_rows)
    state_summary_path = resolve(args.state_summary)
    outdir = resolve(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    actions = read_tsv(actions_path)
    states = read_tsv(states_path)
    state_summary = json.loads(state_summary_path.read_text())
    actions, states, state_summary = apply_synthetic_case(actions, states, state_summary, args.synthetic_case)

    state_by_id = {row.get("cohort_id", ""): row for row in states}
    issues: list[dict[str, str]] = []
    rows: list[dict[str, str]] = []

    def add_issue(cohort_id: str, check: str, detail: str) -> None:
        issues.append({"severity": "hard", "cohort_id": cohort_id, "check": check, "detail": detail})

    if state_summary.get("observed_status") != "PASS":
        add_issue("global", "state_machine_not_pass", "state-machine validator is not PASS")

    for action in sorted(actions, key=lambda row: row.get("priority", "99")):
        cohort_id = action.get("cohort_id", "")
        state = state_by_id.get(cohort_id, {})
        derived_state = state.get("derived_state", "author_run_fallback_prearrival" if cohort_id == "any_author_run_fallback" else "missing_state_row")
        action_type = action.get("action_type", "")
        harness_ready = state.get("harness_ready", "not_applicable_for_fallback" if cohort_id == "any_author_run_fallback" else "")
        may_score_now = "yes" if action_type == "review_harness_ready_before_scoring" and harness_ready == "yes" else "no"

        if may_score_now == "yes" and derived_state != "frozen_harness_ready":
            add_issue(cohort_id, "premature_harness_ready", f"action_type={action_type} but derived_state={derived_state}")
        if may_score_now == "yes" and state_summary.get("observed_status") != "PASS":
            add_issue(cohort_id, "state_machine_not_pass_for_scoring", "state-machine validator must pass before scoring")

        rows.append(
            {
                "priority": action.get("priority", ""),
                "cohort_id": cohort_id,
                "current_action_type": action_type,
                "derived_state": derived_state,
                "may_score_now": may_score_now,
                "if_package_arrives": next_if_arrives(cohort_id),
                "arrival_packet": ARRIVAL_PACKET.get(cohort_id, ""),
                "operator_status_template": "docs/validation/input_schemas/V45_first_24h_operator_status_template.tsv",
                "status_updater_or_gate": status_update_command(cohort_id),
                "hard_stop": "no module scoring, outcome scoring, or interpretation until all first-24h gates and frozen-plan checks pass",
            }
        )

    observed = "FAIL" if issues else "PASS"
    tree_path = outdir / "received_package_decision_tree.tsv"
    issues_path = outdir / "received_package_decision_tree_issues.tsv"
    write_tsv(
        tree_path,
        rows,
        [
            "priority",
            "cohort_id",
            "current_action_type",
            "derived_state",
            "may_score_now",
            "if_package_arrives",
            "arrival_packet",
            "operator_status_template",
            "status_updater_or_gate",
            "hard_stop",
        ],
    )
    write_tsv(issues_path, issues, ["severity", "cohort_id", "check", "detail"])
    summary = {
        "synthetic": args.synthetic_case != "none",
        "synthetic_case": args.synthetic_case,
        "purpose": "V45 first-24h received-package decision tree; no biological claim",
        "observed_status": observed,
        "expected_status": args.expect_status,
        "expectation_met": observed == args.expect_status,
        "n_routes": len(rows),
        "n_may_score_now": sum(1 for row in rows if row["may_score_now"] == "yes"),
        "n_hard_issues": len(issues),
        "tree": rel(tree_path),
        "issues": rel(issues_path),
        "sources": {
            "actions": rel(actions_path),
            "state_rows": rel(states_path),
            "state_summary": rel(state_summary_path),
        },
    }
    (outdir / "received_package_decision_tree_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["expectation_met"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
