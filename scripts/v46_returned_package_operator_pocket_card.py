#!/usr/bin/env python3
"""Generate a compact returned-package operator pocket card.

This is operator navigation infrastructure only. It summarizes existing V46
machine-readable routing, first-30-minute status, and safe-class boundaries into
a one-page handoff card. It does not open returned score tables, labels,
expression matrices, or quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_returned_package_operator_pocket_card"
QUICKSTART_COMMANDS = ROOT / "analysis/v46_returned_package_quickstart_readme/returned_package_quickstart_commands.tsv"
FIRST30 = ROOT / "analysis/v46_first30_returned_package_status_board_dryrun/first30_status_board_dryrun.tsv"
SAFE_MAP = ROOT / "analysis/v46_safe_class_report_template_readiness/safe_class_report_template_map.tsv"
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


def selected_commands() -> list[dict[str, str]]:
    rows = read_tsv(QUICKSTART_COMMANDS)
    artifact_ids = {
        "current_action_card",
        "cold_start_operator_sequence",
        "receipt_manifest_schema_linter",
        "package_manifest_shape_classifier",
        "first30_status_board",
        "command_order_planner",
        "safe_interpretation_classifier",
    }
    return [row for row in rows if row["artifact_id"] in artifact_ids]


def safe_class_summary() -> list[dict[str, str]]:
    rows = read_tsv(SAFE_MAP)
    priority = [
        "BLOCKED_TERMS_OR_RECEIPT_GATES",
        "BLOCKED_COMPLETENESS",
        "CONTEXT_ONLY_OR_LABELS_NEEDED",
        "INCONCLUSIVE_SMALL_COHORT",
        "CAUTION_BATCH_OR_CONFOUNDER",
        "ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION",
    ]
    by_class = {row["safe_class"]: row for row in rows}
    return [by_class[name] for name in priority if name in by_class]


def write_card(path: Path, commands: list[dict[str, str]], first30: list[dict[str, str]], safe_rows: list[dict[str, str]]) -> None:
    lines = [
        "# Returned-Package Operator Pocket Card V46",
        "",
        "Status: generated operator pocket card. No validation result and no biological claim.",
        "",
        "## First Rule",
        "",
        "Do not open score-bearing files, labels, expression matrices, or quarantined cohorts until the route gates say the package is reviewable.",
        "",
        "## Minimal Command Path",
        "",
        "| Order | Artifact | Command |",
        "|---:|---|---|",
    ]
    for row in commands:
        lines.append(f"| {row['sequence']} | `{row['artifact_id']}` | `{row['command']}` |")
    lines.extend(["", "## First-30-Minute Branches", "", "| Scenario | Status | Next action | Safe wording |", "|---|---|---|---|"])
    for row in first30:
        lines.append(
            f"| `{row['scenario']}` | `{row['board_status']}` | {row['next_action']} | {row['allowed_language']} |"
        )
    lines.extend(["", "## Safe-Class Boundaries", "", "| Safe class | Report mode | Meaning |", "|---|---|---|"])
    for row in safe_rows:
        lines.append(
            f"| `{row['safe_class']}` | `{row['report_mode']}` | {row['allowed_interpretation']} |"
        )
    lines.extend(
        [
            "",
            "Boundary: this pocket card is generated from quickstart commands, the",
            "first-30 status board, and the safe-class map. It is navigation only.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def lint(card: Path, commands: list[dict[str, str]], first30: list[dict[str, str]], safe_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    text = card.read_text(errors="ignore") if card.exists() else ""
    checks = {
        "card_exists": card.exists(),
        "boundary_text_present": "No validation result and no biological claim" in text,
        "all_selected_commands_present": all(row["command"] in text for row in commands),
        "first30_scenarios_present": all(row["scenario"] in text for row in first30),
        "safe_classes_present": all(row["safe_class"] in text for row in safe_rows),
        "score_values_read_false": all(row.get("score_values_read", "false") == "false" for row in commands + first30 + safe_rows),
        "no_forbidden_result_language": not any(pattern.search(text) for pattern in FORBIDDEN_RESULT_TEXT),
    }
    return [
        {
            "check": check,
            "status": "PASS" if ok else "FAIL",
            "detail": rel(card) if check == "card_exists" else check,
            "score_values_read": "false",
        }
        for check, ok in checks.items()
    ]


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    commands = selected_commands()
    first30 = read_tsv(FIRST30)
    safe_rows = safe_class_summary()
    card = outdir / "RETURNED_PACKAGE_OPERATOR_POCKET_CARD.md"
    write_card(card, commands, first30, safe_rows)
    checks = lint(card, commands, first30, safe_rows)
    n_fail = sum(1 for row in checks if row["status"] != "PASS")
    write_tsv(outdir / "pocket_card_commands.tsv", commands, list(commands[0].keys()))
    write_tsv(outdir / "pocket_card_first30.tsv", first30, list(first30[0].keys()))
    write_tsv(outdir / "pocket_card_safe_classes.tsv", safe_rows, list(safe_rows[0].keys()))
    write_tsv(outdir / "pocket_card_lint.tsv", checks, ["check", "status", "detail", "score_values_read"])
    summary = {
        "synthetic": False,
        "purpose": "V46 returned-package operator pocket card; no biological claim",
        "n_selected_commands": len(commands),
        "n_first30_scenarios": len(first30),
        "n_safe_classes": len(safe_rows),
        "n_lint_checks": len(checks),
        "n_lint_fail": n_fail,
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in checks),
        "card": rel(card),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "pocket_card_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and n_fail:
        return 1
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
