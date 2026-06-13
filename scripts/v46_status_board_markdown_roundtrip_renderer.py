#!/usr/bin/env python3
"""Regenerate returned-package status-board Markdown from the TSV.

This is operator-readiness infrastructure only. It proves the first-30 returned
package Markdown status board is mechanically reproducible from the TSV, so
manual team-update drift is caught before package handling. It does not read
returned scores, expression data, labels, or quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import difflib
import json
from pathlib import Path

import v46_returned_package_status_board_schema_linter as schema_linter


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_status_board_markdown_roundtrip_renderer"
DEFAULT_BOARD = ROOT / "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun.tsv"
DEFAULT_MARKDOWN = ROOT / "analysis/v46_first30_returned_package_status_board_dryrun/FIRST30_STATUS_BOARD_DRYRUN.md"
DEFAULT_SUMMARY = ROOT / "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun_summary.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board", type=Path, default=DEFAULT_BOARD)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
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
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_summary(path: Path, rows: list[dict[str, str]]) -> dict[str, object]:
    if path.exists():
        data = json.loads(path.read_text())
        return {
            "n_board_rows": data.get("n_board_rows", len(rows)),
            "n_lint_checks": data.get("n_lint_checks", ""),
            "n_lint_fail": data.get("n_lint_fail", ""),
        }
    return {"n_board_rows": len(rows), "n_lint_checks": "", "n_lint_fail": ""}


def render_markdown(rows: list[dict[str, str]], summary: dict[str, object]) -> str:
    lines = [
        "# First-30 Returned-Package Status Board Dry Run V46",
        "",
        "Status: operator infrastructure. No validation result and no biological claim.",
        "",
        "This dry-run board summarizes the first-30-minute returned-package route",
        "status without reading result values. It is intended for team status updates",
        "before the V46 safe-interpretation classifier and V42 grid permit any result",
        "language.",
        "",
        f"Rows: `{summary['n_board_rows']}`; lint checks: `{summary['n_lint_checks']}`; failures: `{summary['n_lint_fail']}`.",
        "",
        "| Scenario | Status | Blocker | Next action | Repair template |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['scenario']}` | `{row['board_status']}` | {row['blocker']} | "
            f"{row['next_action']} | `{row['repair_template_id'] or 'not_needed'}` |"
        )
    lines.extend(
        [
            "",
            "Every row has `score_values_read=false`. Status sentences are deliberately",
            "pre-result and cannot be used as validation interpretation.",
            "",
        ]
    )
    return "\n".join(lines)


def normalized(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()).rstrip() + "\n"


def diff_text(expected: str, observed: str) -> str:
    return "\n".join(
        difflib.unified_diff(
            expected.splitlines(),
            observed.splitlines(),
            fromfile="regenerated",
            tofile="live",
            lineterm="",
        )
    )


def add_check(checks: list[dict[str, object]], check: str, status: bool, detail: object) -> None:
    checks.append(
        {
            "check": check,
            "status": "PASS" if status else "FAIL",
            "detail": str(detail),
            "score_values_read": "false",
        }
    )


def main() -> int:
    args = parse_args()
    board = resolve(args.board)
    markdown = resolve(args.markdown)
    summary_path = resolve(args.summary)
    outdir = resolve(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = read_tsv(board)
    summary_input = read_summary(summary_path, rows)
    regenerated = normalized(render_markdown(rows, summary_input))
    live_text = normalized(markdown.read_text())
    regenerated_path = outdir / "FIRST30_STATUS_BOARD_DRYRUN.roundtrip.md"
    regenerated_path.write_text(regenerated)

    diff_path = outdir / "first30_status_board_roundtrip.diff"
    drift_path = outdir / "synthetic_manual_drift.md"
    drift_text = regenerated.replace("ROUTE_READY_FOR_GATED_REVIEW", "MANUAL_DRIFT_STATUS", 1)
    drift_path.write_text(drift_text)
    diff_path.write_text(diff_text(regenerated, live_text) + ("\n" if regenerated != live_text else ""))

    checks: list[dict[str, object]] = []
    add_check(checks, "board_exists", board.exists(), rel(board))
    add_check(checks, "markdown_exists", markdown.exists(), rel(markdown))
    add_check(checks, "roundtrip_markdown_matches_live", regenerated == live_text, rel(diff_path) if regenerated != live_text else "exact_match")
    add_check(checks, "synthetic_drift_detected", normalized(drift_text) != live_text, rel(drift_path))
    add_check(checks, "scenario_set_exact", {row["scenario"] for row in rows} == schema_linter.REQUIRED_SCENARIOS, sorted(row["scenario"] for row in rows))
    add_check(checks, "all_score_values_read_false", all(row.get("score_values_read") == "false" for row in rows), "board score_values_read column")
    for row in rows:
        add_check(
            checks,
            f"scenario_rendered:{row['scenario']}",
            f"`{row['scenario']}`" in regenerated and f"`{row['board_status']}`" in regenerated,
            row["board_status"],
        )

    lint_path = outdir / "status_board_markdown_roundtrip_lint.tsv"
    write_tsv(lint_path, checks, ["check", "status", "detail", "score_values_read"])
    n_fail = sum(1 for row in checks if row["status"] != "PASS")
    summary = {
        "synthetic": False,
        "purpose": "V46 status-board Markdown round-trip renderer; no biological claim and no score values read",
        "board": rel(board),
        "live_markdown": rel(markdown),
        "regenerated_markdown": rel(regenerated_path),
        "synthetic_drift_fixture": rel(drift_path),
        "diff": rel(diff_path),
        "n_board_rows": len(rows),
        "n_lint_checks": len(checks),
        "n_lint_fail": n_fail,
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in checks),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "status_board_markdown_roundtrip_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if args.fail_on_error and n_fail else (0 if n_fail == 0 else 2)


if __name__ == "__main__":
    raise SystemExit(main())
