#!/usr/bin/env python3
"""Lint returned-package status-board TSV/Markdown schema.

This is operator-readiness infrastructure only. It checks that the first-30
returned-package status board remains parseable and safe for team updates. It
does not read returned scores, expression data, labels, or quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_returned_package_status_board_schema_linter"
DEFAULT_BOARD = ROOT / "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun.tsv"
DEFAULT_MARKDOWN = ROOT / "analysis/v46_first30_returned_package_status_board_dryrun/FIRST30_STATUS_BOARD_DRYRUN.md"

REQUIRED_COLUMNS = [
    "scenario",
    "board_status",
    "status_summary",
    "blocker",
    "next_minute_window",
    "next_step_order",
    "next_action",
    "next_command_or_artifact",
    "stop_route_if_next_step_fails",
    "repair_template_id",
    "repair_template_path",
    "allowed_language",
    "team_status_sentence",
    "score_values_read",
]

REQUIRED_SCENARIOS = {
    "scored_canonical_aggregate",
    "scored_noncanonical_aggregate",
    "scored_unknown_alias_aggregate",
    "unscoreable_aggregate",
    "partial_label_scored_aggregate",
    "terms_blocked_return",
}

ALLOWED_STATUSES = {
    "ROUTE_READY_FOR_GATED_REVIEW",
    "FORMAT_NORMALIZATION_REQUIRED",
    "FORMAT_ALIAS_TRIAGE_REQUIRED",
    "UNSCOREABLE_AGGREGATE_PREFLIGHT",
    "PARTIAL_LABEL_PAIR_COUNT_REQUIRED",
    "BLOCKED_TERMS_OR_RECEIPT",
}

MARKDOWN_HEADER = ["Scenario", "Status", "Blocker", "Next action", "Repair template"]
FORBIDDEN_PRE_RESULT_TERMS = [
    "auc",
    "effect size",
    "passed",
    "failed",
    "breakthrough",
    "response-predictive",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board", type=Path, default=DEFAULT_BOARD)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), [{key: value or "" for key, value in row.items()} for row in reader]


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def add_check(
    checks: list[dict[str, object]],
    scope: str,
    item: str,
    check: str,
    ok: bool,
    detail: object,
) -> None:
    checks.append(
        {
            "scope": scope,
            "item": item,
            "check": check,
            "status": "PASS" if ok else "FAIL",
            "detail": str(detail),
            "score_values_read": "false",
        }
    )


def forbidden_hits(text: str) -> list[str]:
    lowered = text.lower()
    return [term for term in FORBIDDEN_PRE_RESULT_TERMS if term in lowered]


def lint_board_tsv(path: Path, scope: str) -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    checks: list[dict[str, object]] = []
    if not path.exists():
        add_check(checks, scope, rel(path), "tsv_exists", False, path)
        return checks, []

    columns, rows = read_tsv(path)
    add_check(checks, scope, rel(path), "tsv_columns_exact", columns == REQUIRED_COLUMNS, columns)
    add_check(checks, scope, rel(path), "tsv_row_count", len(rows) == len(REQUIRED_SCENARIOS), len(rows))

    scenarios = [row.get("scenario", "") for row in rows]
    add_check(checks, scope, rel(path), "scenario_set_exact", set(scenarios) == REQUIRED_SCENARIOS, sorted(scenarios))
    add_check(checks, scope, rel(path), "scenario_unique", len(scenarios) == len(set(scenarios)), sorted(scenarios))

    for row in rows:
        scenario = row.get("scenario", "")
        add_check(checks, scope, scenario, "board_status_allowed", row.get("board_status", "") in ALLOWED_STATUSES, row.get("board_status", ""))
        add_check(checks, scope, scenario, "next_step_order_integer", row.get("next_step_order", "").isdigit(), row.get("next_step_order", ""))
        add_check(checks, scope, scenario, "score_values_read_false", row.get("score_values_read", "") == "false", row.get("score_values_read", ""))
        for column in [
            "status_summary",
            "blocker",
            "next_action",
            "next_command_or_artifact",
            "allowed_language",
            "team_status_sentence",
        ]:
            add_check(checks, scope, f"{scenario}:{column}", "required_text_nonempty", bool(row.get(column, "").strip()), row.get(column, ""))

        template_id = row.get("repair_template_id", "")
        template_path = row.get("repair_template_path", "")
        add_check(
            checks,
            scope,
            scenario,
            "repair_template_consistency",
            (bool(template_id) and bool(template_path)) or (not template_id and not template_path),
            f"{template_id}|{template_path}",
        )
        hits = forbidden_hits(f"{row.get('allowed_language', '')} {row.get('team_status_sentence', '')}")
        add_check(checks, scope, scenario, "pre_result_language_no_score_terms", not hits, ";".join(hits) if hits else "clean")

    return checks, rows


def markdown_table_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    lines = path.read_text().splitlines()
    header_index = -1
    for index, line in enumerate(lines):
        if line.strip().startswith("| Scenario | Status | Blocker | Next action | Repair template |"):
            header_index = index
            break
    if header_index < 0 or header_index + 1 >= len(lines):
        return [], []
    header = [cell.strip() for cell in lines[header_index].strip().strip("|").split("|")]
    rows: list[list[str]] = []
    for line in lines[header_index + 2 :]:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return header, rows


def clean_markdown_token(value: str) -> str:
    return re.sub(r"^`|`$", "", value.strip())


def lint_markdown(path: Path, tsv_rows: list[dict[str, str]], scope: str) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    if not path.exists():
        add_check(checks, scope, rel(path), "markdown_exists", False, path)
        return checks

    header, rows = markdown_table_rows(path)
    add_check(checks, scope, rel(path), "markdown_header_exact", header == MARKDOWN_HEADER, header)
    add_check(checks, scope, rel(path), "markdown_row_count", len(rows) == len(REQUIRED_SCENARIOS), len(rows))

    tsv_by_scenario = {row["scenario"]: row for row in tsv_rows if row.get("scenario")}
    markdown_scenarios = [clean_markdown_token(row[0]) for row in rows if row]
    add_check(
        checks,
        scope,
        rel(path),
        "markdown_scenarios_match_tsv",
        set(markdown_scenarios) == set(tsv_by_scenario),
        sorted(markdown_scenarios),
    )
    for row in rows:
        if len(row) != len(MARKDOWN_HEADER):
            add_check(checks, scope, rel(path), "markdown_row_width", False, row)
            continue
        scenario = clean_markdown_token(row[0])
        status = clean_markdown_token(row[1])
        template = clean_markdown_token(row[4])
        tsv_row = tsv_by_scenario.get(scenario, {})
        add_check(checks, scope, scenario, "markdown_status_matches_tsv", status == tsv_row.get("board_status", ""), status)
        expected_template = tsv_row.get("repair_template_id") or "not_needed"
        add_check(checks, scope, scenario, "markdown_template_matches_tsv", template == expected_template, template)
        hits = forbidden_hits(" ".join(row))
        add_check(checks, scope, scenario, "markdown_table_no_score_terms", not hits, ";".join(hits) if hits else "clean")
    return checks


def fixture_paths(outdir: Path, live_board: Path, live_markdown: Path) -> list[tuple[str, Path, Path, str]]:
    fixtures = outdir / "fixtures"
    fixtures.mkdir(parents=True, exist_ok=True)
    _, rows = read_tsv(live_board)

    good_tsv = fixtures / "good_status_board.tsv"
    good_md = fixtures / "good_status_board.md"
    write_tsv(good_tsv, rows, REQUIRED_COLUMNS)
    good_md.write_text(live_markdown.read_text())

    missing_column = fixtures / "missing_column_status_board.tsv"
    write_tsv(missing_column, rows, [column for column in REQUIRED_COLUMNS if column != "team_status_sentence"])

    score_read = fixtures / "score_read_status_board.tsv"
    score_rows = [dict(row) for row in rows]
    score_rows[0]["score_values_read"] = "true"
    write_tsv(score_read, score_rows, REQUIRED_COLUMNS)

    malformed_md = fixtures / "malformed_status_board.md"
    malformed_md.write_text("# Bad status board\n\n| Scenario | Status |\n|---|---|\n| `scored_canonical_aggregate` | `PASSED` |\n")

    return [
        ("good", good_tsv, good_md, "PASS"),
        ("missing_column", missing_column, good_md, "FAIL"),
        ("score_values_read_true", score_read, good_md, "FAIL"),
        ("malformed_markdown", good_tsv, malformed_md, "FAIL"),
    ]


def write_markdown(path: Path, summary: dict[str, object]) -> None:
    path.write_text(
        "\n".join(
            [
                "# Returned-Package Status-Board Schema Linter V46",
                "",
                "Status: operator infrastructure. No validation result and no biological claim.",
                "",
                f"Overall status: `{summary['overall_status']}`.",
                f"Live lint checks: `{summary['n_live_checks']}`; live failures: `{summary['n_live_fail']}`.",
                f"Synthetic fixture cases: `{summary['n_fixture_cases']}`; expectation failures: `{summary['n_fixture_expectation_fail']}`.",
                "",
                "The linter checks only status-board schema and pre-result wording. It does not read returned scores, expression matrices, labels, or quarantined cohorts.",
                "",
            ]
        )
    )


def main() -> int:
    args = parse_args()
    outdir = resolve(args.outdir)
    board = resolve(args.board)
    markdown = resolve(args.markdown)
    outdir.mkdir(parents=True, exist_ok=True)

    live_checks, live_rows = lint_board_tsv(board, "live_tsv")
    live_checks.extend(lint_markdown(markdown, live_rows, "live_markdown"))
    n_live_fail = sum(1 for row in live_checks if row["status"] != "PASS")

    fixture_results: list[dict[str, object]] = []
    all_fixture_checks: list[dict[str, object]] = []
    for name, fixture_tsv, fixture_md, expected in fixture_paths(outdir, board, markdown):
        checks, rows = lint_board_tsv(fixture_tsv, f"fixture:{name}:tsv")
        checks.extend(lint_markdown(fixture_md, rows, f"fixture:{name}:markdown"))
        observed = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
        fixture_results.append(
            {
                "fixture": name,
                "expected_status": expected,
                "observed_status": observed,
                "expectation_met": str(observed == expected).lower(),
                "n_checks": len(checks),
                "n_fail": sum(1 for row in checks if row["status"] != "PASS"),
                "score_values_read": "false",
            }
        )
        all_fixture_checks.extend(checks)

    n_fixture_expectation_fail = sum(1 for row in fixture_results if row["expectation_met"] != "true")
    all_score_values_read_false = all(row["score_values_read"] == "false" for row in live_checks + all_fixture_checks)
    summary = {
        "synthetic": True,
        "purpose": "V46 returned-package status-board schema linter; no biological claim",
        "live_board": rel(board),
        "live_markdown": rel(markdown),
        "n_live_checks": len(live_checks),
        "n_live_fail": n_live_fail,
        "n_fixture_cases": len(fixture_results),
        "n_fixture_expectation_fail": n_fixture_expectation_fail,
        "n_all_checks": len(live_checks) + len(all_fixture_checks),
        "all_score_values_read_false": all_score_values_read_false,
        "overall_status": "PASS" if n_live_fail == 0 and n_fixture_expectation_fail == 0 and all_score_values_read_false else "FAIL",
    }

    write_tsv(
        outdir / "status_board_schema_lint.tsv",
        live_checks + all_fixture_checks,
        ["scope", "item", "check", "status", "detail", "score_values_read"],
    )
    write_tsv(
        outdir / "status_board_schema_fixture_results.tsv",
        fixture_results,
        ["fixture", "expected_status", "observed_status", "expectation_met", "n_checks", "n_fail", "score_values_read"],
    )
    write_markdown(outdir / "RETURNED_PACKAGE_STATUS_BOARD_SCHEMA_LINTER.md", summary)
    (outdir / "status_board_schema_linter_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if args.fail_on_error and summary["overall_status"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
