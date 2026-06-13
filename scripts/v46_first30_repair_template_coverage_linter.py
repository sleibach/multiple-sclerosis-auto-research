#!/usr/bin/env python3
"""Lint first-30-minute stop routes against repair-request templates.

This is operations infrastructure only. It verifies that every author-facing
repair stop in the first-30-minute returned-package decision table maps to an
existing safe repair-request template, and that referenced templates pass their
forbidden-language lint. It does not read returned scores, real data, labels, or
quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_first30_repair_template_coverage_linter"
FIRST30_TABLE = ROOT / "analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_table.tsv"
TEMPLATE_INDEX = ROOT / "analysis/v46_return_repair_request_templates/repair_request_template_index.tsv"
TEMPLATE_LINT = ROOT / "analysis/v46_return_repair_request_templates/repair_request_template_lint.tsv"

LOCAL_ONLY_PATTERNS = [
    "repair local software/readiness guard",
    "keep package outside git and run no-raw scanner",
    "repair local planning artifact before report drafting",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def template_maps() -> tuple[dict[str, dict[str, str]], dict[str, list[str]], dict[str, int]]:
    rows = read_tsv(TEMPLATE_INDEX)
    by_id = {row["template_id"]: row for row in rows}
    by_safe_class: dict[str, list[str]] = {}
    for row in rows:
        by_safe_class.setdefault(row["safe_class"], []).append(row["template_id"])
    lint_failures: dict[str, int] = {}
    for row in read_tsv(TEMPLATE_LINT):
        if row["status"] != "PASS":
            lint_failures[row["template_id"]] = lint_failures.get(row["template_id"], 0) + 1
    return by_id, by_safe_class, lint_failures


def extract_template_ids(route: str, valid_ids: set[str]) -> list[str]:
    hits = []
    for template_id in sorted(valid_ids):
        if re.search(rf"(?<![A-Za-z0-9_]){re.escape(template_id)}(?![A-Za-z0-9_])", route):
            hits.append(template_id)
    return hits


def coverage_type(route: str, ids: list[str]) -> str:
    route_lower = route.lower()
    if any(pattern in route_lower for pattern in LOCAL_ONLY_PATTERNS):
        return "local_operator_guard"
    if "matching repair template" in route_lower:
        return "dynamic_safe_class_template"
    if ids:
        return "explicit_repair_template"
    if "repair template" in route_lower:
        return "unresolved_repair_template_reference"
    return "no_repair_needed"


def build_rows() -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    first30 = read_tsv(FIRST30_TABLE)
    by_id, by_safe_class, lint_failures = template_maps()
    valid_ids = set(by_id)
    rows: list[dict[str, object]] = []
    checks: list[dict[str, object]] = []

    for row in first30:
        route = row["route_to_if_stopped"]
        ids = extract_template_ids(route, valid_ids)
        kind = coverage_type(route, ids)
        if kind == "dynamic_safe_class_template":
            ids = sorted(valid_ids)
        if not ids:
            ids = [""]
        for template_id in ids:
            template_exists = (template_id in by_id) if template_id else kind in {"local_operator_guard", "no_repair_needed"}
            lint_fail_count = lint_failures.get(template_id, 0) if template_id else 0
            status = "PASS"
            if kind == "unresolved_repair_template_reference" or not template_exists or lint_fail_count:
                status = "FAIL"
            rows.append(
                {
                    "scenario": row["scenario"],
                    "step_order": row["step_order"],
                    "action": row["action"],
                    "route_to_if_stopped": route,
                    "coverage_type": kind,
                    "template_id": template_id,
                    "template_exists": str(template_exists).lower(),
                    "template_lint_failures": lint_fail_count,
                    "coverage_status": status,
                    "score_values_read": "false",
                }
            )
            checks.append(
                {
                    "scenario": row["scenario"],
                    "step_order": row["step_order"],
                    "check": f"coverage_{kind}",
                    "status": status,
                    "detail": template_id or route,
                }
            )

    safe_class_rows = [
        {
            "safe_class": safe_class,
            "template_ids": ";".join(sorted(template_ids)),
            "n_templates": len(template_ids),
            "status": "PASS" if template_ids else "FAIL",
        }
        for safe_class, template_ids in sorted(by_safe_class.items())
    ]
    for row in safe_class_rows:
        checks.append(
            {
                "scenario": "safe_class_template_index",
                "step_order": "",
                "check": f"safe_class_has_template:{row['safe_class']}",
                "status": row["status"],
                "detail": row["template_ids"],
            }
        )

    summary = {
        "synthetic": False,
        "purpose": "V46 first-30 stop-route to repair-template coverage linter; no biological claim",
        "n_first30_rows": len(first30),
        "n_coverage_rows": len(rows),
        "n_template_ids": len(valid_ids),
        "n_safe_classes_with_templates": len(safe_class_rows),
        "n_local_operator_guard_rows": sum(1 for row in rows if row["coverage_type"] == "local_operator_guard"),
        "n_dynamic_safe_class_rows": sum(1 for row in rows if row["coverage_type"] == "dynamic_safe_class_template"),
        "n_explicit_template_rows": sum(1 for row in rows if row["coverage_type"] == "explicit_repair_template"),
        "n_lint_checks": len(checks),
        "n_lint_fail": sum(1 for row in checks if row["status"] != "PASS"),
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in rows),
    }
    summary["overall_status"] = "PASS" if summary["n_lint_fail"] == 0 and summary["all_score_values_read_false"] else "FAIL"
    return rows, safe_class_rows, checks, summary


def write_markdown(path: Path, summary: dict[str, object], safe_class_rows: list[dict[str, object]]) -> None:
    lines = [
        "# First-30 Repair Template Coverage Linter V46",
        "",
        "Status: operations infrastructure. No validation result and no biological claim.",
        "",
        "This linter verifies that first-30-minute returned-package stop routes either",
        "stay local to operator software/no-raw repair or map to an existing safe",
        "author-facing repair-request template.",
        "",
        f"Overall status: `{summary['overall_status']}`.",
        f"First-30 rows: `{summary['n_first30_rows']}`; coverage rows: `{summary['n_coverage_rows']}`; lint failures: `{summary['n_lint_fail']}`.",
        "",
        "| Safe class | Template IDs |",
        "|---|---|",
    ]
    for row in safe_class_rows:
        lines.append(f"| `{row['safe_class']}` | `{row['template_ids']}` |")
    lines.extend(
        [
            "",
            "Dynamic safe-class stop routes are covered by the full template index.",
            "Local operator stops do not contact an author and therefore do not require",
            "a repair-request template.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    coverage_rows, safe_class_rows, checks, summary = build_rows()

    coverage_path = outdir / "first30_repair_template_coverage.tsv"
    safe_class_path = outdir / "repair_template_safe_class_coverage.tsv"
    lint_path = outdir / "first30_repair_template_coverage_lint.tsv"
    markdown_path = outdir / "FIRST30_REPAIR_TEMPLATE_COVERAGE.md"

    write_tsv(
        coverage_path,
        coverage_rows,
        [
            "scenario",
            "step_order",
            "action",
            "route_to_if_stopped",
            "coverage_type",
            "template_id",
            "template_exists",
            "template_lint_failures",
            "coverage_status",
            "score_values_read",
        ],
    )
    write_tsv(safe_class_path, safe_class_rows, ["safe_class", "template_ids", "n_templates", "status"])
    write_tsv(lint_path, checks, ["scenario", "step_order", "check", "status", "detail"])
    summary.update(
        {
            "coverage": rel(coverage_path),
            "safe_class_coverage": rel(safe_class_path),
            "lint": rel(lint_path),
            "markdown": rel(markdown_path),
        }
    )
    write_markdown(markdown_path, summary, safe_class_rows)
    (outdir / "first30_repair_template_coverage_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and summary["overall_status"] != "PASS":
        return 1
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
