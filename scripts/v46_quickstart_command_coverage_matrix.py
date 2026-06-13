#!/usr/bin/env python3
"""Build a coverage matrix for generated returned-package quickstart commands.

This is command-navigation governance. It checks that every generated
quickstart command is present in the quickstart Markdown and protected by the
drift fixture. It does not read returned score values, labels, expression data,
or quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_quickstart_command_coverage_matrix"
COMMANDS = ROOT / "analysis/v46_returned_package_quickstart_readme/returned_package_quickstart_commands.tsv"
README = ROOT / "analysis/v46_returned_package_quickstart_readme/RETURNED_PACKAGE_QUICKSTART.md"
REGRESSION_STEPS = ROOT / "analysis/v46_returned_package_regression_suite/returned_package_regression_steps.tsv"
SMOKE_STEPS = ROOT / "analysis/v46_operator_smoke_test_bundle/operator_smoke_test_steps.tsv"
DRIFT_SUMMARY = ROOT / "analysis/v46_quickstart_drift_fixture/quickstart_drift_summary.json"


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


def step_scripts(path: Path) -> set[str]:
    scripts: set[str] = set()
    if not path.exists():
        return scripts
    for row in read_tsv(path):
        command = row.get("command", "")
        for token in command.split():
            if token.startswith("scripts/") and token.endswith(".py"):
                scripts.add(token)
    return scripts


def write_markdown(path: Path, rows: list[dict[str, object]], summary: dict[str, object]) -> None:
    lines = [
        "# Quickstart Command Coverage Matrix V46",
        "",
        "Status: quickstart command-governance matrix. No validation result and no biological claim.",
        "",
        f"Overall status: `{summary['overall_status']}`; command rows: `{summary['n_command_rows']}`; lint failures: `{summary['n_lint_fail']}`.",
        "",
        "| Sequence | Artifact | README | Regression script | Smoke script | Drift parity |",
        "|---:|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['sequence']} | `{row['artifact_id']}` | `{row['present_in_readme']}` | `{row['script_in_regression_suite']}` | `{row['script_in_smoke_bundle']}` | `{row['covered_by_drift_fixture']}` |"
        )
    lines.extend(
        [
            "",
            "Boundary: this matrix checks command coverage only. It does not run a",
            "validation and does not inspect returned data.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    commands = read_tsv(COMMANDS)
    readme_text = README.read_text(errors="ignore")
    regression_scripts = step_scripts(REGRESSION_STEPS)
    smoke_scripts = step_scripts(SMOKE_STEPS)
    drift = json.loads(DRIFT_SUMMARY.read_text()) if DRIFT_SUMMARY.exists() else {}
    drift_ok = drift.get("overall_status") == "PASS" and int(drift.get("n_command_rows_checked", 0)) >= len(commands)

    rows: list[dict[str, object]] = []
    lint_rows: list[dict[str, object]] = []
    for row in commands:
        script = row.get("script", "")
        present = row["command"] in readme_text
        matrix_row = {
            "sequence": row["sequence"],
            "section": row["section"],
            "phase": row["phase"],
            "artifact_id": row["artifact_id"],
            "script": script,
            "present_in_readme": str(present).lower(),
            "script_in_regression_suite": str((not script) or script in regression_scripts).lower(),
            "script_in_smoke_bundle": str((not script) or script in smoke_scripts).lower(),
            "covered_by_drift_fixture": str(drift_ok).lower(),
            "source": row["source"],
            "score_values_read": "false",
        }
        rows.append(matrix_row)
        for check, ok in [
            ("present_in_readme", present),
            ("covered_by_drift_fixture", drift_ok),
            ("score_values_read_false", row.get("score_values_read") == "false"),
        ]:
            lint_rows.append(
                {
                    "artifact_id": row["artifact_id"],
                    "check": check,
                    "status": "PASS" if ok else "FAIL",
                    "detail": script or row["command"],
                    "score_values_read": "false",
                }
            )

    n_fail = sum(1 for row in lint_rows if row["status"] != "PASS")
    summary = {
        "synthetic": False,
        "purpose": "V46 quickstart command coverage matrix; no biological claim",
        "n_command_rows": len(rows),
        "n_lint_checks": len(lint_rows),
        "n_lint_fail": n_fail,
        "n_present_in_readme": sum(1 for row in rows if row["present_in_readme"] == "true"),
        "n_drift_fixture_covered": sum(1 for row in rows if row["covered_by_drift_fixture"] == "true"),
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in rows + lint_rows),
        "matrix": rel(outdir / "quickstart_command_coverage_matrix.tsv"),
        "lint": rel(outdir / "quickstart_command_coverage_lint.tsv"),
        "markdown": rel(outdir / "QUICKSTART_COMMAND_COVERAGE_MATRIX.md"),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    write_tsv(
        outdir / "quickstart_command_coverage_matrix.tsv",
        rows,
        [
            "sequence",
            "section",
            "phase",
            "artifact_id",
            "script",
            "present_in_readme",
            "script_in_regression_suite",
            "script_in_smoke_bundle",
            "covered_by_drift_fixture",
            "source",
            "score_values_read",
        ],
    )
    write_tsv(outdir / "quickstart_command_coverage_lint.tsv", lint_rows, ["artifact_id", "check", "status", "detail", "score_values_read"])
    write_markdown(outdir / "QUICKSTART_COMMAND_COVERAGE_MATRIX.md", rows, summary)
    (outdir / "quickstart_command_coverage_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and n_fail:
        return 1
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
