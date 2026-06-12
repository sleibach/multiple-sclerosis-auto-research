#!/usr/bin/env python3
"""Lint cross-route V45 validation readiness handoff coverage.

This is an operational/readiness guard only. It does not inspect expression
matrices, outcomes, quarantined data, or run any validation harness.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_cross_route_readiness_linter/live"
DEFAULTS = {
    "external": ROOT / "analysis/v45_external_blocker_board/external_blocker_board.tsv",
    "arrival_index": ROOT / "analysis/v45_route_arrival_packets/route_arrival_packet_index.tsv",
    "command_runner_root": ROOT / "analysis/v45_validation_command_runner",
    "author_run_gate_summary": ROOT / "analysis/v45_author_run_return_gate_runner/synthetic_check_summary.json",
}

COHORT_ALIASES = {
    "gse228330_ocrelizumab": "gse228330_ocrelizumab_pbmc",
}

REQUIRED_PACKET_PHRASES = [
    "No scoring is authorized",
    "Do not run module scoring",
    "all required gates pass",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--external", type=Path, default=DEFAULTS["external"])
    parser.add_argument("--arrival-index", type=Path, default=DEFAULTS["arrival_index"])
    parser.add_argument("--command-runner-root", type=Path, default=DEFAULTS["command_runner_root"])
    parser.add_argument("--author-run-gate-summary", type=Path, default=DEFAULTS["author_run_gate_summary"])
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument(
        "--synthetic-case",
        choices=["none", "missing_request"],
        default="none",
        help="Apply a labeled synthetic mutation for regression testing.",
    )
    parser.add_argument("--expect-status", choices=["PASS", "WARN", "FAIL"], default="PASS")
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
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalize_cohort_id(cohort_id: str) -> str:
    return COHORT_ALIASES.get(cohort_id, cohort_id)


def command_plan_summaries(root: Path) -> dict[str, dict[str, str]]:
    summaries: dict[str, dict[str, str]] = {}
    if not root.exists():
        return summaries
    for path in root.glob("*/command_plan_summary.json"):
        data = json.loads(path.read_text())
        cohort_id = normalize_cohort_id(str(data.get("cohort_id", "")))
        summaries[cohort_id] = {
            "command_plan_summary": rel(path),
            "command_plan_status": str(data.get("status", "")),
            "command_plan_mode": str(data.get("mode", "")),
            "command_plan_steps": str(data.get("n_steps", "")),
        }
    return summaries


def packet_has_gate_text(packet_path: Path) -> bool:
    if not packet_path.exists():
        return False
    text = packet_path.read_text(errors="ignore")
    return all(phrase.lower() in text.lower() for phrase in REQUIRED_PACKET_PHRASES)


def request_has_gate_text(request_path: Path) -> bool:
    if not request_path.exists():
        return False
    text = request_path.read_text(errors="ignore").lower()
    return any(
        phrase in text
        for phrase in [
            "frozen",
            "pre-registered",
            "pre-specified",
            "preregistration",
            "no raw",
            "aggregate",
            "neda-4",
            "would not make response-validation claims",
        ]
    )


def author_run_plan_equivalent(summary_path: Path) -> dict[str, str]:
    if not summary_path.exists():
        return {
            "command_plan_summary": rel(summary_path),
            "command_plan_status": "missing_author_run_gate_summary",
            "command_plan_mode": "author_run",
            "command_plan_steps": "",
        }
    data = json.loads(summary_path.read_text())
    return {
        "command_plan_summary": rel(summary_path),
        "command_plan_status": f"author_run_gate_{data.get('overall_status', 'UNKNOWN')}",
        "command_plan_mode": "author_run",
        "command_plan_steps": str(data.get("n_cases", "")),
    }


def main() -> int:
    args = parse_args()
    external_path = resolve(args.external)
    arrival_index_path = resolve(args.arrival_index)
    command_root = resolve(args.command_runner_root)
    author_summary = resolve(args.author_run_gate_summary)
    outdir = resolve(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    external_rows = read_tsv(external_path)
    if args.synthetic_case == "missing_request" and external_rows:
        external_rows = [dict(row) for row in external_rows]
        external_rows[0]["request_packet"] = "docs/validation/outbound_requests/SYNTHETIC_MISSING_REQUEST.md"

    arrival_by_id = {row.get("cohort_id", ""): row for row in read_tsv(arrival_index_path)}
    command_by_id = command_plan_summaries(command_root)

    rows: list[dict[str, str]] = []
    issues: list[dict[str, str]] = []

    def add_issue(severity: str, cohort_id: str, check: str, detail: str) -> None:
        issues.append({"severity": severity, "cohort_id": cohort_id, "check": check, "detail": detail})

    for route in sorted(external_rows, key=lambda row: row.get("cohort_id", "")):
        cohort_id = route.get("cohort_id", "")
        role = route.get("role", "")
        request = resolve(Path(route.get("request_packet", "")))
        arrival = arrival_by_id.get(cohort_id, {})
        packet = resolve(Path(arrival.get("packet", ""))) if arrival else ROOT / "__missing_packet__"

        request_exists = request.exists()
        packet_exists = packet.exists()
        blocker_present = bool(route.get("blocker_type", "") and (route.get("external_blocker", "") or route.get("triage_current_blocker", "")))
        packet_gate = packet_has_gate_text(packet)
        request_gate = request_has_gate_text(request)

        command = command_by_id.get(cohort_id, {})
        if cohort_id == "any_author_run_fallback":
            command = author_run_plan_equivalent(author_summary)
        command_present = bool(command)

        if not request_exists:
            add_issue("hard", cohort_id, "request_artifact_missing", f"request artifact not found: {rel(request)}")
        if not blocker_present:
            add_issue("hard", cohort_id, "blocker_state_missing", "route lacks explicit blocker_type/current blocker")
        if not packet_exists:
            add_issue("hard", cohort_id, "arrival_packet_missing", "route arrival packet not found")
        if packet_exists and not packet_gate:
            add_issue("hard", cohort_id, "arrival_packet_missing_no_score_gate", "arrival packet lacks required no-scoring hard-stop text")
        if request_exists and not request_gate:
            add_issue("soft", cohort_id, "request_packet_gate_language_sparse", "request exists but lacks expected frozen/no-raw/aggregate wording")
        if not command_present:
            add_issue("soft", cohort_id, "command_plan_missing", "no generated command plan or author-run gate equivalent found")

        route_status = "PASS"
        if any(issue["severity"] == "hard" and issue["cohort_id"] == cohort_id for issue in issues):
            route_status = "FAIL"
        elif any(issue["severity"] == "soft" and issue["cohort_id"] == cohort_id for issue in issues):
            route_status = "WARN"

        rows.append(
            {
                "cohort_id": cohort_id,
                "role": role,
                "route_status": route_status,
                "request_artifact": rel(request),
                "request_exists": str(request_exists).lower(),
                "request_gate_language_present": str(request_gate).lower(),
                "blocker_type": route.get("blocker_type", ""),
                "blocker_present": str(blocker_present).lower(),
                "arrival_packet": rel(packet) if packet_exists else arrival.get("packet", ""),
                "arrival_packet_exists": str(packet_exists).lower(),
                "arrival_packet_no_score_gate": str(packet_gate).lower(),
                "command_plan_summary": command.get("command_plan_summary", ""),
                "command_plan_status": command.get("command_plan_status", ""),
                "command_plan_mode": command.get("command_plan_mode", ""),
                "command_plan_steps": command.get("command_plan_steps", ""),
            }
        )

    n_hard = sum(1 for row in issues if row["severity"] == "hard")
    n_soft = sum(1 for row in issues if row["severity"] == "soft")
    observed = "FAIL" if n_hard else ("WARN" if n_soft else "PASS")

    routes_path = outdir / "cross_route_readiness_lint.tsv"
    issues_path = outdir / "cross_route_readiness_issues.tsv"
    write_tsv(
        routes_path,
        rows,
        [
            "cohort_id",
            "role",
            "route_status",
            "request_artifact",
            "request_exists",
            "request_gate_language_present",
            "blocker_type",
            "blocker_present",
            "arrival_packet",
            "arrival_packet_exists",
            "arrival_packet_no_score_gate",
            "command_plan_summary",
            "command_plan_status",
            "command_plan_mode",
            "command_plan_steps",
        ],
    )
    write_tsv(issues_path, issues, ["severity", "cohort_id", "check", "detail"])

    summary = {
        "synthetic": args.synthetic_case != "none",
        "synthetic_case": args.synthetic_case,
        "purpose": "V45 cross-route readiness linter; no biological claim",
        "observed_status": observed,
        "expected_status": args.expect_status,
        "expectation_met": observed == args.expect_status,
        "n_routes": len(rows),
        "n_hard_issues": n_hard,
        "n_soft_issues": n_soft,
        "routes": rel(routes_path),
        "issues": rel(issues_path),
        "sources": {
            "external": rel(external_path),
            "arrival_index": rel(arrival_index_path),
            "command_runner_root": rel(command_root),
            "author_run_gate_summary": rel(author_summary),
        },
    }
    (outdir / "cross_route_readiness_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["expectation_met"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
