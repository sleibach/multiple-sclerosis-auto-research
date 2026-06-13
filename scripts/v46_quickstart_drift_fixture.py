#!/usr/bin/env python3
"""Verify that manual drift in the generated quickstart is caught.

This is operator-documentation regression infrastructure. It compares copied
quickstart Markdown fixtures against the machine-readable quickstart command
table and proves that an edited command or removed boundary text is detected.
It does not read returned score tables, expression data, labels, or quarantined
cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_quickstart_drift_fixture"
README = ROOT / "analysis/v46_returned_package_quickstart_readme/RETURNED_PACKAGE_QUICKSTART.md"
COMMANDS = ROOT / "analysis/v46_returned_package_quickstart_readme/returned_package_quickstart_commands.tsv"
FORBIDDEN_RESULT_TEXT = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bAUC\s*[=:]",
        r"\bp\s*[=<]",
        r"\beffect[- ]size\s*[=:]",
        r"\bvalidated\b",
        r"\bclinical\s+interpretation\b",
        r"\bresult\s+is\b",
    ]
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


def command_rows() -> list[dict[str, str]]:
    return read_tsv(COMMANDS)


def fixture_cases(readme_text: str, rows: list[dict[str, str]]) -> list[dict[str, str]]:
    first_command = rows[0]["command"]
    scored_command = next(row["command"] for row in rows if row["artifact_id"] == "scored_canonical_to_plan")
    return [
        {
            "case_id": "exact_generated_quickstart",
            "expected_status": "PASS",
            "text": readme_text,
            "mutation": "none",
        },
        {
            "case_id": "edited_handoff_command",
            "expected_status": "FAIL",
            "text": readme_text.replace(first_command, first_command.replace("analysis/v45_current_action_card", "analysis/manual_edit_current_action_card"), 1),
            "mutation": "changed first handoff command outdir",
        },
        {
            "case_id": "edited_receipt_branch_command",
            "expected_status": "FAIL",
            "text": readme_text.replace(scored_command, scored_command.replace("--expect-status PASS", "--expect-status BLOCKED"), 1),
            "mutation": "changed scoreable receipt-branch expectation",
        },
        {
            "case_id": "removed_boundary_text",
            "expected_status": "FAIL",
            "text": readme_text.replace("No validation result and no biological claim.", "Manual quickstart copy.", 1),
            "mutation": "removed no-biological-claim boundary",
        },
    ]


def lint_fixture(text: str, rows: list[dict[str, str]]) -> tuple[str, list[str], list[str]]:
    missing = [row["artifact_id"] for row in rows if row["command"] not in text]
    failures: list[str] = []
    if missing:
        failures.append("command_table_parity")
    if "No validation result and no biological claim" not in text:
        failures.append("boundary_text_present")
    forbidden = [pattern.pattern for pattern in FORBIDDEN_RESULT_TEXT if pattern.search(text)]
    if forbidden:
        failures.append("no_forbidden_result_language")
    return ("PASS" if not failures else "FAIL", missing, failures)


def write_markdown(path: Path, case_rows: list[dict[str, object]], summary: dict[str, object]) -> None:
    lines = [
        "# Quickstart Drift Fixture V46",
        "",
        "Status: synthetic documentation-regression fixture. No validation result and no biological claim.",
        "",
        f"Overall status: `{summary['overall_status']}`; cases: `{summary['n_cases']}`; expectation failures: `{summary['n_expectation_failures']}`.",
        "",
        "| Case | Mutation | Expected | Observed | Missing commands |",
        "|---|---|---|---|---:|",
    ]
    for row in case_rows:
        lines.append(
            f"| `{row['case_id']}` | {row['mutation']} | `{row['expected_status']}` | `{row['observed_status']}` | `{row['n_missing_commands']}` |"
        )
    lines.extend(
        [
            "",
            "Boundary: these fixtures mutate copied quickstart Markdown only. They do not",
            "read returned score values or change the generated quickstart source tables.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    fixtures = outdir / "fixtures"
    fixtures.mkdir(parents=True, exist_ok=True)

    rows = command_rows()
    readme_text = README.read_text()
    case_rows: list[dict[str, object]] = []
    lint_rows: list[dict[str, object]] = []
    for case in fixture_cases(readme_text, rows):
        fixture_path = fixtures / f"{case['case_id']}.md"
        fixture_path.write_text(case["text"])
        observed, missing, failures = lint_fixture(case["text"], rows)
        expectation_met = observed == case["expected_status"]
        case_row = {
            "case_id": case["case_id"],
            "mutation": case["mutation"],
            "expected_status": case["expected_status"],
            "observed_status": observed,
            "expectation_met": str(expectation_met).lower(),
            "n_missing_commands": len(missing),
            "missing_command_artifact_ids": ";".join(missing[:20]),
            "failure_checks": ";".join(failures),
            "fixture_path": rel(fixture_path),
            "score_values_read": "false",
        }
        case_rows.append(case_row)
        for check, ok, detail in [
            ("expectation_met", expectation_met, case["expected_status"]),
            ("score_values_read_false", True, "false"),
            ("command_table_parity", "command_table_parity" not in failures, ";".join(missing[:20]) if missing else "all commands present"),
            ("boundary_text_present", "boundary_text_present" not in failures, case["case_id"]),
            ("no_forbidden_result_language", "no_forbidden_result_language" not in failures, case["case_id"]),
        ]:
            lint_rows.append(
                {
                    "case_id": case["case_id"],
                    "check": check,
                    "status": "PASS" if ok else "FAIL",
                    "detail": detail,
                    "expected_status": case["expected_status"],
                    "observed_status": observed,
                    "score_values_read": "false",
                }
            )

    n_expectation_failures = sum(1 for row in case_rows if row["expectation_met"] != "true")
    summary = {
        "synthetic": True,
        "purpose": "V46 quickstart drift fixture; no biological claim",
        "n_cases": len(case_rows),
        "n_expected_fail_cases": sum(1 for row in case_rows if row["expected_status"] == "FAIL"),
        "n_expectation_failures": n_expectation_failures,
        "n_command_rows_checked": len(rows),
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in case_rows + lint_rows),
        "cases": rel(outdir / "quickstart_drift_cases.tsv"),
        "lint": rel(outdir / "quickstart_drift_lint.tsv"),
        "markdown": rel(outdir / "QUICKSTART_DRIFT_FIXTURE.md"),
        "overall_status": "PASS" if n_expectation_failures == 0 else "FAIL",
    }
    write_tsv(
        outdir / "quickstart_drift_cases.tsv",
        case_rows,
        [
            "case_id",
            "mutation",
            "expected_status",
            "observed_status",
            "expectation_met",
            "n_missing_commands",
            "missing_command_artifact_ids",
            "failure_checks",
            "fixture_path",
            "score_values_read",
        ],
    )
    write_tsv(
        outdir / "quickstart_drift_lint.tsv",
        lint_rows,
        ["case_id", "check", "status", "detail", "expected_status", "observed_status", "score_values_read"],
    )
    write_markdown(outdir / "QUICKSTART_DRIFT_FIXTURE.md", case_rows, summary)
    (outdir / "quickstart_drift_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and n_expectation_failures:
        return 1
    return 0 if n_expectation_failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
