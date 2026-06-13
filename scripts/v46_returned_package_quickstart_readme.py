#!/usr/bin/env python3
"""Generate the V46 returned-package quickstart from machine-readable routing.

This is operator navigation infrastructure. It converts the committed handoff
manifest and receipt-manifest-to-command-plan handoff into a compact README so
operator instructions stay tied to runnable commands. It does not read returned
score tables, expression matrices, labels, or quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_returned_package_quickstart_readme"
HANDOFF = ROOT / "analysis/v46_returned_package_handoff_bundle_manifest/returned_package_handoff_bundle_manifest.tsv"
RECEIPT_HANDOFF = ROOT / "analysis/v46_receipt_manifest_to_command_plan_handoff/receipt_manifest_to_command_plan_handoff.tsv"
REGRESSION_STEPS = ROOT / "analysis/v46_returned_package_regression_suite/returned_package_regression_steps.tsv"
SMOKE_STEPS = ROOT / "analysis/v46_operator_smoke_test_bundle/operator_smoke_test_steps.tsv"

SCRIPT_RE = re.compile(r"(scripts/[A-Za-z0-9_./-]+\.py)")
FORBIDDEN_RESULT_PATTERNS = [
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


def command_script(command: str) -> str:
    match = SCRIPT_RE.search(command)
    return match.group(1) if match else ""


def load_handoff_commands() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in read_tsv(HANDOFF):
        script = command_script(row["command"])
        rows.append(
            {
                "section": "handoff_manifest",
                "sequence": int(row["sequence"]),
                "phase": row["phase"],
                "artifact_id": row["artifact_id"],
                "command": row["command"],
                "doc": row["doc"],
                "primary_output": row["primary_output"],
                "script": script,
                "script_exists": str((ROOT / script).exists() if script else True).lower(),
                "source": rel(HANDOFF),
                "score_values_read": "false",
            }
        )
    return rows


def load_receipt_handoff_examples(start_sequence: int) -> list[dict[str, object]]:
    if not RECEIPT_HANDOFF.exists():
        return []
    rows: list[dict[str, object]] = []
    for index, row in enumerate(read_tsv(RECEIPT_HANDOFF), start=start_sequence):
        rows.append(
            {
                "section": "receipt_manifest_examples",
                "sequence": index,
                "phase": "receipt_to_command_plan",
                "artifact_id": row["case"],
                "command": row["command_plan_command"],
                "doc": "docs/validation/RECEIPT_MANIFEST_TO_COMMAND_PLAN_HANDOFF_V46.md",
                "primary_output": row["receipt_manifest"],
                "script": command_script(row["command_plan_command"]),
                "script_exists": str((ROOT / command_script(row["command_plan_command"])).exists()).lower()
                if command_script(row["command_plan_command"])
                else "true",
                "source": rel(RECEIPT_HANDOFF),
                "expected_status": row["expected_plan_status"],
                "terminal_stage": row["terminal_stage"],
                "stop_condition": row["stop_condition"],
                "score_values_read": row["score_values_read"],
            }
        )
    return rows


def phase_groups(rows: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["phase"])].append(row)
    return grouped


def read_step_count(path: Path) -> int:
    if not path.exists():
        return 0
    return max(0, len(read_tsv(path)))


def write_markdown(path: Path, rows: list[dict[str, object]], receipt_examples: list[dict[str, object]]) -> None:
    grouped = phase_groups(rows)
    lines = [
        "# Returned-Package Quickstart V46",
        "",
        "Status: generated operator quickstart. No validation result and no biological claim.",
        "",
        "This quickstart is generated from the returned-package handoff manifest and",
        "the receipt-manifest-to-command-plan handoff. Edit those machine-readable",
        "sources, not this Markdown, when the route changes.",
        "",
        "## Start Here",
        "",
        "Run these guards before touching a returned package:",
        "",
        "```bash",
        ".venv/bin/python scripts/v46_returned_package_regression_suite.py --outdir analysis/v46_returned_package_regression_suite --fail-on-error",
        ".venv/bin/python scripts/v46_operator_smoke_test_bundle.py --outdir analysis/v46_operator_smoke_test_bundle --fail-on-error",
        ".venv/bin/python scripts/v46_returned_package_handoff_bundle_manifest.py --outdir analysis/v46_returned_package_handoff_bundle_manifest --fail-on-error",
        "```",
        "",
        "If these commands do not pass, stop at readiness repair. Do not inspect",
        "returned score-bearing files, labels, expression matrices, or quarantined",
        "cohorts while resolving navigation failures.",
        "",
        "## Operator Order",
        "",
    ]
    for phase in grouped:
        lines.extend([f"### {phase}", "", "| Order | Artifact | Command | Primary output |", "|---:|---|---|---|"])
        for row in grouped[phase]:
            lines.append(
                f"| {row['sequence']} | `{row['artifact_id']}` | `{row['command']}` | `{row['primary_output']}` |"
            )
        lines.append("")

    lines.extend(
        [
            "## Receipt-Manifest Branch Examples",
            "",
            "These examples are generated from the handoff table and show the next",
            "command or stop condition without reading score values.",
            "",
            "| Case | Expected plan status | Terminal stage | Stop condition | Command |",
            "|---|---|---|---|---|",
        ]
    )
    for row in receipt_examples:
        lines.append(
            f"| `{row['artifact_id']}` | `{row['expected_status']}` | `{row['terminal_stage']}` | {row['stop_condition']} | `{row['command']}` |"
        )

    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "This quickstart does not authorize any result wording. The V46 safe class,",
            "the result-report header linter, and the frozen V42 pre-registration remain",
            "the boundary before any result text can be drafted.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def lint_rows(
    readme: Path,
    command_rows: list[dict[str, object]],
    receipt_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    text = readme.read_text(errors="ignore") if readme.exists() else ""
    rows: list[dict[str, object]] = []

    def add(check: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "check": check,
                "status": "PASS" if ok else "FAIL",
                "detail": detail,
                "score_values_read": "false",
            }
        )

    add("handoff_manifest_exists", HANDOFF.exists(), rel(HANDOFF))
    add("receipt_handoff_exists", RECEIPT_HANDOFF.exists(), rel(RECEIPT_HANDOFF))
    add("commands_present", bool(command_rows), f"{len(command_rows)} handoff commands")
    add("receipt_examples_present", bool(receipt_rows), f"{len(receipt_rows)} receipt branch examples")
    add("readme_exists", readme.exists(), rel(readme))
    add("boundary_text_present", "No validation result and no biological claim" in text, rel(readme))
    add("no_score_values_read", all(str(row.get("score_values_read")) == "false" for row in command_rows + receipt_rows), "all rows")
    missing_scripts = sorted({str(row["script"]) for row in command_rows + receipt_rows if row.get("script") and row.get("script_exists") != "true"})
    add("referenced_scripts_exist", not missing_scripts, ";".join(missing_scripts) if missing_scripts else "all referenced scripts exist")
    forbidden_hits = [pattern.pattern for pattern in FORBIDDEN_RESULT_PATTERNS if pattern.search(text)]
    add("no_forbidden_result_language", not forbidden_hits, ";".join(forbidden_hits) if forbidden_hits else "none")
    for required_command in [
        "scripts/v46_returned_package_regression_suite.py",
        "scripts/v46_operator_smoke_test_bundle.py",
        "scripts/v46_returned_package_handoff_bundle_manifest.py",
        "scripts/v46_returned_package_command_order_planner.py",
    ]:
        add(f"readme_mentions_{Path(required_command).stem}", required_command in text, required_command)
    return rows


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    command_rows = load_handoff_commands()
    receipt_rows = load_receipt_handoff_examples(start_sequence=len(command_rows) + 1)
    all_commands = command_rows + receipt_rows
    commands_path = outdir / "returned_package_quickstart_commands.tsv"
    readme = outdir / "RETURNED_PACKAGE_QUICKSTART.md"
    lint_path = outdir / "returned_package_quickstart_lint.tsv"
    write_tsv(
        commands_path,
        all_commands,
        [
            "section",
            "sequence",
            "phase",
            "artifact_id",
            "command",
            "doc",
            "primary_output",
            "script",
            "script_exists",
            "source",
            "score_values_read",
            "expected_status",
            "terminal_stage",
            "stop_condition",
        ],
    )
    write_markdown(readme, command_rows, receipt_rows)
    checks = lint_rows(readme, command_rows, receipt_rows)
    write_tsv(lint_path, checks, ["check", "status", "detail", "score_values_read"])

    n_fail = sum(1 for row in checks if row["status"] != "PASS")
    summary = {
        "synthetic": False,
        "purpose": "V46 returned-package generated quickstart; no biological claim",
        "n_handoff_commands": len(command_rows),
        "n_receipt_branch_examples": len(receipt_rows),
        "n_total_command_rows": len(all_commands),
        "n_regression_steps": read_step_count(REGRESSION_STEPS),
        "n_smoke_steps": read_step_count(SMOKE_STEPS),
        "n_lint_checks": len(checks),
        "n_lint_fail": n_fail,
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in checks),
        "commands": rel(commands_path),
        "lint": rel(lint_path),
        "markdown": rel(readme),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "returned_package_quickstart_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and n_fail:
        return 1
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
