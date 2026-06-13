#!/usr/bin/env python3
"""Check safe-class coverage for V46 safe-interpretation examples.

This is operator-wording governance only. It proves every safe class either has
an example card or an explicit reason for being represented elsewhere. It does
not read returned score values, labels, expression data, or quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_safe_interpretation_example_coverage_linter"
SAFE_MAP = ROOT / "analysis/v46_safe_class_report_template_readiness/safe_class_report_template_map.tsv"
EXAMPLES = ROOT / "analysis/v46_safe_interpretation_examples/safe_interpretation_examples.tsv"

NON_EXAMPLE_REASONS = {
    "BLOCKED_TERMS_OR_RECEIPT_GATES": "Covered by terms-governance, receipt-manifest, first-30 stop-route, and repair-template fixtures; no returned-package interpretation example is permitted.",
    "BLOCKED_REDACTION": "Covered by author-run return gate and redaction precheck fixtures; no operator interpretation wording is allowed before redaction passes.",
    "BLOCKED_COMPLETENESS": "Covered by unscoreable-return composition and repair-template fixtures; examples stop before safe interpretation when required outputs are missing.",
    "BLOCKED_RETURN_GATE": "Covered by command-order and return-gate fixtures; no example should normalize a failed combined gate into result wording.",
    "BLOCKED_SCHEMA": "Covered by receipt/schema and result-report linters; malformed aggregate outputs stop before example-card wording.",
    "BLOCKED_METADATA_CONTRADICTION": "Covered by report-header metadata and metadata-contradiction guards; contradictory metadata blocks result review.",
}


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


def write_markdown(path: Path, rows: list[dict[str, object]], summary: dict[str, object]) -> None:
    lines = [
        "# Safe-Interpretation Example Coverage Linter V46",
        "",
        "Status: safe-class coverage governance. No validation result and no biological claim.",
        "",
        f"Overall status: `{summary['overall_status']}`; safe classes: `{summary['n_safe_classes']}`; represented: `{summary['n_represented_by_example']}`; explicit non-example reasons: `{summary['n_explicit_non_example_reason']}`.",
        "",
        "| Safe class | Coverage status | Example count | Reason |",
        "|---|---|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['safe_class']}` | `{row['coverage_status']}` | `{row['n_examples']}` | {row['non_example_reason']} |"
        )
    lines.extend(
        [
            "",
            "Boundary: this linter only checks example coverage accounting. It does not",
            "make blocked safe classes interpretable and does not read score values.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    safe_rows = read_tsv(SAFE_MAP)
    examples = read_tsv(EXAMPLES)
    example_counts: dict[str, int] = {}
    example_ids: dict[str, list[str]] = {}
    for row in examples:
        example_counts[row["safe_class"]] = example_counts.get(row["safe_class"], 0) + 1
        example_ids.setdefault(row["safe_class"], []).append(row["example_id"])

    coverage_rows: list[dict[str, object]] = []
    lint_rows: list[dict[str, object]] = []
    for safe in safe_rows:
        safe_class = safe["safe_class"]
        n_examples = example_counts.get(safe_class, 0)
        reason = NON_EXAMPLE_REASONS.get(safe_class, "")
        covered = n_examples > 0 or bool(reason)
        status = "EXAMPLE_CARD" if n_examples else "EXPLICIT_NON_EXAMPLE_REASON"
        row = {
            "safe_class": safe_class,
            "report_mode": safe["report_mode"],
            "n_examples": n_examples,
            "example_ids": ";".join(example_ids.get(safe_class, [])),
            "coverage_status": status if covered else "MISSING_COVERAGE",
            "non_example_reason": reason,
            "score_values_read": "false",
        }
        coverage_rows.append(row)
        for check, ok, detail in [
            ("safe_class_covered", covered, safe_class),
            ("stop_only_missing_examples_have_reason", bool(reason) if n_examples == 0 else True, safe_class),
            ("score_values_read_false", row["score_values_read"] == "false", safe_class),
        ]:
            lint_rows.append(
                {
                    "safe_class": safe_class,
                    "check": check,
                    "status": "PASS" if ok else "FAIL",
                    "detail": detail,
                    "score_values_read": "false",
                }
            )

    n_fail = sum(1 for row in lint_rows if row["status"] != "PASS")
    summary = {
        "synthetic": False,
        "purpose": "V46 safe-interpretation example coverage linter; no biological claim",
        "n_safe_classes": len(coverage_rows),
        "n_represented_by_example": sum(1 for row in coverage_rows if int(row["n_examples"]) > 0),
        "n_explicit_non_example_reason": sum(1 for row in coverage_rows if int(row["n_examples"]) == 0 and row["non_example_reason"]),
        "n_lint_checks": len(lint_rows),
        "n_lint_fail": n_fail,
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in coverage_rows + lint_rows),
        "coverage": rel(outdir / "safe_interpretation_example_coverage.tsv"),
        "lint": rel(outdir / "safe_interpretation_example_coverage_lint.tsv"),
        "markdown": rel(outdir / "SAFE_INTERPRETATION_EXAMPLE_COVERAGE.md"),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    write_tsv(
        outdir / "safe_interpretation_example_coverage.tsv",
        coverage_rows,
        ["safe_class", "report_mode", "n_examples", "example_ids", "coverage_status", "non_example_reason", "score_values_read"],
    )
    write_tsv(
        outdir / "safe_interpretation_example_coverage_lint.tsv",
        lint_rows,
        ["safe_class", "check", "status", "detail", "score_values_read"],
    )
    write_markdown(outdir / "SAFE_INTERPRETATION_EXAMPLE_COVERAGE.md", coverage_rows, summary)
    (outdir / "safe_interpretation_example_coverage_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and n_fail:
        return 1
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
