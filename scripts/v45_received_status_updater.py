#!/usr/bin/env python3
"""Derive a received-data triage board row from the first-24h operator TSV.

This script is operational only. It reads gate-status metadata, not raw
expression or clinical data, and writes a proposed board update for review.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OPERATOR = ROOT / "docs/validation/input_schemas/V45_first_24h_operator_status_template.tsv"
DEFAULT_BOARD = ROOT / "analysis/v45_received_data_triage/received_data_triage_status.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v45_received_status_updater"

PASS_VALUES = {"pass", "passed", "complete", "completed", "done", "yes", "approved", "approved_for_preflight"}
NA_VALUES = {"na", "n/a", "not_applicable", "not_required", "only_if_labels_received", "yes_if_labels_received"}
FAIL_VALUES = {"fail", "failed", "blocked", "missing", "ambiguous", "no"}


GATE_TO_COLUMN = {
    "receipt_log": "data_received",
    "quarantine_path": "quarantined",
    "data_use_terms": "terms_captured",
    "checksum_manifest": "checksum_verified",
    "intake_preflight": "metadata_preflight_passed",
    "subject_map_sanity": "subject_map_passed",
    "outcome_dictionary": "outcome_dictionary_frozen",
    "preregistration_or_addendum": "addendum_committed",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operator-status", type=Path, default=DEFAULT_OPERATOR)
    parser.add_argument("--board", type=Path, default=DEFAULT_BOARD)
    parser.add_argument("--cohort-id", required=True)
    parser.add_argument("--role", default="")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--write-board", action="store_true", help="Overwrite the board file with the proposed update.")
    return parser.parse_args()


def norm(value: object) -> str:
    return str(value).strip().lower()


def gate_status(table: pd.DataFrame, gate: str) -> str:
    rows = table.loc[table["gate"] == gate, "status"]
    if rows.empty:
        return "missing_gate"
    return norm(rows.iloc[0])


def status_to_board_value(status: str, current: str = "no") -> str:
    if status in PASS_VALUES:
        return "yes"
    if status in NA_VALUES:
        return "not_applicable"
    if status in FAIL_VALUES:
        return "blocked"
    if status == "todo":
        return "no"
    return current if current else "unknown"


def first_blocker(table: pd.DataFrame) -> tuple[str, str]:
    for row in table.sort_values("order").to_dict(orient="records"):
        required = norm(row["required_for_harness_ready"])
        status = norm(row["status"])
        if required in NA_VALUES:
            continue
        if status in PASS_VALUES or status in NA_VALUES:
            continue
        return str(row["gate"]), str(row["blocker_if_not_passed"])
    return "", ""


def derive_harness_ready(table: pd.DataFrame, row: dict[str, object]) -> str:
    ready_gate = gate_status(table, "harness_ready_decision")
    if ready_gate not in PASS_VALUES:
        return "no"
    required_columns = [
        "terms_captured",
        "quarantined",
        "checksum_verified",
        "metadata_preflight_passed",
        "subject_map_passed",
        "outcome_dictionary_frozen",
        "addendum_committed",
    ]
    for column in required_columns:
        value = norm(row.get(column, "no"))
        if value not in {"yes", "not_applicable"}:
            return "no"
    return "yes"


def main() -> int:
    args = parse_args()
    operator_path = args.operator_status if args.operator_status.is_absolute() else ROOT / args.operator_status
    board_path = args.board if args.board.is_absolute() else ROOT / args.board
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    operator = pd.read_csv(operator_path, sep="\t").fillna("")
    board = pd.read_csv(board_path, sep="\t").fillna("")

    if args.cohort_id in set(board["cohort_id"]):
        row = board.loc[board["cohort_id"] == args.cohort_id].iloc[0].to_dict()
    else:
        row = {
            "cohort_id": args.cohort_id,
            "role": args.role or "unknown",
            "request_packet_ready": "unknown",
            "request_sent": "unknown",
            "data_received": "no",
            "terms_captured": "no",
            "quarantined": "no",
            "checksum_verified": "no",
            "metadata_preflight_passed": "no",
            "subject_map_required": "unknown",
            "subject_map_passed": "no",
            "outcome_dictionary_required": "unknown",
            "outcome_dictionary_frozen": "no",
            "addendum_required": "unknown",
            "addendum_committed": "no",
            "harness_ready": "no",
            "current_blocker": "",
            "next_action": "",
        }

    for gate, column in GATE_TO_COLUMN.items():
        row[column] = status_to_board_value(gate_status(operator, gate), str(row.get(column, "")))

    if norm(row.get("subject_map_required", "")) in {"no", "not_applicable"}:
        row["subject_map_passed"] = "not_applicable"
    if norm(row.get("outcome_dictionary_required", "")) in {"no", "not_applicable", "only_if_labels_received"}:
        row["outcome_dictionary_frozen"] = "not_applicable"
    if norm(row.get("addendum_required", "")) in {"no", "not_applicable", "yes_if_labels_received"}:
        row["addendum_committed"] = "not_applicable"

    blocker_gate, blocker_text = first_blocker(operator)
    row["harness_ready"] = derive_harness_ready(operator, row)
    if row["harness_ready"] == "yes":
        row["current_blocker"] = "none"
        row["next_action"] = "run_matching_frozen_harness_only"
    else:
        row["current_blocker"] = blocker_text or str(row.get("current_blocker", "status_incomplete"))
        row["next_action"] = f"complete_or_repair_{blocker_gate}" if blocker_gate else "review_operator_status"

    updated = board.copy()
    if args.cohort_id in set(updated["cohort_id"]):
        for column, value in row.items():
            if column in updated.columns:
                updated.loc[updated["cohort_id"] == args.cohort_id, column] = value
    else:
        updated = pd.concat([updated, pd.DataFrame([row], columns=updated.columns)], ignore_index=True)

    proposed_path = outdir / "received_data_triage_status.proposed.tsv"
    updated.to_csv(proposed_path, sep="\t", index=False)
    gate_path = outdir / "operator_gate_status_used.tsv"
    operator.to_csv(gate_path, sep="\t", index=False)

    if args.write_board:
        updated.to_csv(board_path, sep="\t", index=False)

    summary = {
        "synthetic": False,
        "purpose": "received-data triage status updater; no biological claim",
        "cohort_id": args.cohort_id,
        "operator_status": str(operator_path.relative_to(ROOT)),
        "board": str(board_path.relative_to(ROOT)),
        "write_board": bool(args.write_board),
        "proposed_board": str(proposed_path.relative_to(ROOT)),
        "harness_ready": row["harness_ready"],
        "current_blocker": row["current_blocker"],
        "next_action": row["next_action"],
        "n_gates": int(len(operator)),
    }
    (outdir / "received_status_update_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
