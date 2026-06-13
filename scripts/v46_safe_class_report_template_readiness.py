#!/usr/bin/env python3
"""Map V46 safe classes to report skeleton readiness.

This is returned-package report-governance infrastructure only. It proves that
every V46 safe interpretation class has either explicit stop wording or a
pre-registered report skeleton before any returned score value is read.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_safe_class_report_template_readiness"

NO_SCORE_CLASSES = {
    "BLOCKED_TERMS_OR_RECEIPT_GATES": ("STOP_TERMS_OR_RECEIPT", "Terms or receipt evidence blocks interpretation."),
    "BLOCKED_REDACTION": ("STOP_REDACTION", "Returned package is not safely redacted."),
    "BLOCKED_COMPLETENESS": ("STOP_COMPLETENESS", "Required aggregate outputs are missing."),
    "BLOCKED_RETURN_GATE": ("STOP_RETURN_GATE", "Combined return gate failed."),
    "BLOCKED_SCHEMA": ("STOP_SCHEMA", "Aggregate outputs are malformed or internally invalid."),
    "BLOCKED_METADATA_CONTRADICTION": ("STOP_METADATA", "Metadata contradictions invalidate readiness."),
    "CONTEXT_ONLY_OR_LABELS_NEEDED": ("STOP_CONTEXT_ONLY", "Package can support context only; response labels are absent or insufficient."),
    "BELOW_V45_PLANNING_FLOOR": ("STOP_BELOW_FLOOR", "Analyzable labeled pairs are below the V45 planning floor."),
}

SCORE_ALLOWED_CLASSES = {
    "INCONCLUSIVE_SMALL_COHORT": ("RESULT_INCONCLUSIVE_SMALL_COHORT", "Effect-size-with-CI placeholders only, with small-n caution."),
    "MINIMUM_DECISION_GRADE_CAUTION": ("RESULT_MINIMUM_DECISION_GRADE", "V42 grid may be applied only with explicit caution language."),
    "CAUTION_BATCH_OR_CONFOUNDER": ("RESULT_CONFOUNDER_CAUTION", "V42 grid may be applied only with diagnostic caveat language."),
    "ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION": ("RESULT_PREREGISTERED", "Mechanical V42 interpretation skeleton is available."),
}

SAFE_CLASS_ORDER = [
    "BLOCKED_TERMS_OR_RECEIPT_GATES",
    "BLOCKED_REDACTION",
    "BLOCKED_COMPLETENESS",
    "BLOCKED_RETURN_GATE",
    "BLOCKED_SCHEMA",
    "BLOCKED_METADATA_CONTRADICTION",
    "CONTEXT_ONLY_OR_LABELS_NEEDED",
    "BELOW_V45_PLANNING_FLOOR",
    "INCONCLUSIVE_SMALL_COHORT",
    "MINIMUM_DECISION_GRADE_CAUTION",
    "CAUTION_BATCH_OR_CONFOUNDER",
    "ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION",
]

FORBIDDEN_LITERAL_VALUES = [
    "0.5",
    "0.6",
    "0.7",
    "0.8",
    "0.9",
    "1.0",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
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


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def skeleton_text(safe_class: str, skeleton_id: str, mode: str, description: str) -> str:
    header = (
        f"# Synthetic Report Skeleton: {safe_class}\n\n"
        "synthetic: true\n\n"
        f"V46 safe class: {safe_class}\n\n"
        f"Skeleton id: {skeleton_id}\n\n"
        f"Purpose: {description}\n\n"
    )
    boundary = "Boundary: locked rule is unchanged; no post-hoc thresholds, modules, timepoints, or analyses are permitted.\n"
    if mode == "STOP_ONLY":
        return (
            header
            +
            "Allowed report action: stop. Do not inspect or interpret returned score tables.\n\n"
            "Required wording: this returned package is not ready for validation interpretation. "
            "Use the matching V46 repair path or context-only handoff.\n\n"
            f"{boundary}"
        )
    extra = ""
    if safe_class == "INCONCLUSIVE_SMALL_COHORT":
        extra = "Small-n caution: the report must preserve inconclusive language when the V42 grid so requires.\n\n"
    elif safe_class == "MINIMUM_DECISION_GRADE_CAUTION":
        extra = "Minimum decision-grade caution: the report must not broaden beyond the frozen route.\n\n"
    elif safe_class == "CAUTION_BATCH_OR_CONFOUNDER":
        extra = "Diagnostic caution: batch/confounder warnings must be stated next to the V42 grid result.\n\n"
    return (
        header
        +
        "Allowed report action: use the V42 outcome grid and returned aggregate outputs only.\n"
        "Metric source: locked_rule_metrics.tsv from the returned aggregate package.\n"
        "Do not fill result placeholders until all route gates and the V46 safe class have passed.\n\n"
        f"{extra}"
        f"{boundary}"
    )


def class_rows(outdir: Path) -> list[dict[str, object]]:
    fixture_dir = outdir / "fixtures"
    rows: list[dict[str, object]] = []
    for safe_class in SAFE_CLASS_ORDER:
        if safe_class in NO_SCORE_CLASSES:
            skeleton_id, description = NO_SCORE_CLASSES[safe_class]
            mode = "STOP_ONLY"
            may_use_score_language = "false"
        else:
            skeleton_id, description = SCORE_ALLOWED_CLASSES[safe_class]
            mode = "RESULT_SKELETON_ALLOWED_AFTER_GATES"
            may_use_score_language = "true"
        fixture = fixture_dir / f"{safe_class.lower()}.md"
        fixture.parent.mkdir(parents=True, exist_ok=True)
        fixture.write_text(skeleton_text(safe_class, skeleton_id, mode, description))
        rows.append(
            {
                "safe_class": safe_class,
                "report_mode": mode,
                "skeleton_id": skeleton_id,
                "skeleton_path": rel(fixture),
                "may_use_score_language_after_gates": may_use_score_language,
                "requires_v42_grid": str(safe_class in SCORE_ALLOWED_CLASSES).lower(),
                "requires_returned_aggregate_source": str(safe_class in SCORE_ALLOWED_CLASSES).lower(),
                "explicit_stop_wording": str(safe_class in NO_SCORE_CLASSES).lower(),
                "score_values_read": "false",
                "allowed_interpretation": description,
            }
        )
    return rows


def run_report_linter(row: dict[str, object], outdir: Path) -> dict[str, object]:
    safe_class = str(row["safe_class"])
    lint_out = outdir / "report_lint" / safe_class.lower()
    command = [
        sys.executable,
        "scripts/v46_result_report_safe_class_linter.py",
        "lint",
        "--report",
        str(row["skeleton_path"]),
        "--safe-class",
        safe_class,
        "--outdir",
        rel(lint_out),
        "--expect-status",
        "PASS",
    ]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    summary_path = lint_out / "result_report_safe_class_lint_summary.json"
    observed_status = "MISSING_SUMMARY"
    n_checks = 0
    n_fail = 1
    if summary_path.exists():
        summary = json.loads(summary_path.read_text())
        observed_status = str(summary.get("observed_status", ""))
        n_checks = int(summary.get("n_checks", 0))
        n_fail = int(summary.get("n_fail", 0))
    return {
        "safe_class": safe_class,
        "report_linter_returncode": result.returncode,
        "observed_status": observed_status,
        "n_linter_checks": n_checks,
        "n_linter_fail": n_fail,
        "summary": rel(summary_path),
        "stdout_tail": result.stdout[-500:],
        "stderr_tail": result.stderr[-500:],
        "score_values_read": "false",
    }


def build_lint_rows(rows: list[dict[str, object]], linter_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    lint: list[dict[str, object]] = []
    classes = [str(row["safe_class"]) for row in rows]
    expected = set(SAFE_CLASS_ORDER)
    lint.append(
        {
            "scope": "coverage",
            "item": "safe_classes",
            "check": "safe_class_set_exact",
            "status": "PASS" if set(classes) == expected else "FAIL",
            "detail": ",".join(classes),
            "score_values_read": "false",
        }
    )
    lint.append(
        {
            "scope": "coverage",
            "item": "safe_classes",
            "check": "safe_classes_unique",
            "status": "PASS" if len(classes) == len(set(classes)) else "FAIL",
            "detail": len(classes),
            "score_values_read": "false",
        }
    )
    for row in rows:
        text = (ROOT / str(row["skeleton_path"])).read_text()
        if row["report_mode"] == "STOP_ONLY":
            ok = row["explicit_stop_wording"] == "true" and row["may_use_score_language_after_gates"] == "false"
        else:
            ok = row["requires_v42_grid"] == "true" and row["requires_returned_aggregate_source"] == "true"
        lint.append(
            {
                "scope": "template_map",
                "item": row["safe_class"],
                "check": "mode_requirements",
                "status": "PASS" if ok else "FAIL",
                "detail": row["report_mode"],
                "score_values_read": "false",
            }
        )
        forbidden_hits = [value for value in FORBIDDEN_LITERAL_VALUES if value in text]
        lint.append(
            {
                "scope": "template_map",
                "item": row["safe_class"],
                "check": "no_literal_result_values",
                "status": "PASS" if not forbidden_hits else "FAIL",
                "detail": ";".join(forbidden_hits) if forbidden_hits else "clean",
                "score_values_read": "false",
            }
        )
    for linter_row in linter_rows:
        ok = linter_row["observed_status"] == "PASS" and int(linter_row["n_linter_fail"]) == 0
        lint.append(
            {
                "scope": "report_linter",
                "item": linter_row["safe_class"],
                "check": "skeleton_passes_result_report_safe_class_linter",
                "status": "PASS" if ok else "FAIL",
                "detail": linter_row["observed_status"],
                "score_values_read": "false",
            }
        )
    return lint


def write_markdown(path: Path, summary: dict[str, object], rows: list[dict[str, object]]) -> None:
    lines = [
        "# Safe-Class Report-Template Readiness V46",
        "",
        "Status: returned-package report-governance infrastructure. No validation result and no biological claim.",
        "",
        "## Current Result",
        "",
        f"- safe classes covered: `{summary['n_safe_classes']}`",
        f"- lint checks: `{summary['n_lint_checks']}`",
        f"- lint failures: `{summary['n_lint_fail']}`",
        f"- all `score_values_read=false`: `{str(summary['all_score_values_read_false']).lower()}`",
        f"- overall status: `{summary['overall_status']}`",
        "",
        "## Template Map",
        "",
        "| Safe class | Report mode | Skeleton id | Score values read |",
        "|---|---|---|---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['safe_class']}` | `{row['report_mode']}` | `{row['skeleton_id']}` | `{row['score_values_read']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This map proves report skeleton availability and safe stop wording only. It does not read returned score values, expression matrices, labels, or quarantined cohorts, and it does not alter the locked V22 rule or V42 pre-registration.",
        ]
    )
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    outdir = resolve(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rows = class_rows(outdir)
    linter_rows = [run_report_linter(row, outdir) for row in rows]
    lint_rows = build_lint_rows(rows, linter_rows)

    map_path = outdir / "safe_class_report_template_map.tsv"
    linter_path = outdir / "safe_class_report_template_linter_results.tsv"
    lint_path = outdir / "safe_class_report_template_lint.tsv"
    write_tsv(
        map_path,
        rows,
        [
            "safe_class",
            "report_mode",
            "skeleton_id",
            "skeleton_path",
            "may_use_score_language_after_gates",
            "requires_v42_grid",
            "requires_returned_aggregate_source",
            "explicit_stop_wording",
            "score_values_read",
            "allowed_interpretation",
        ],
    )
    write_tsv(
        linter_path,
        linter_rows,
        [
            "safe_class",
            "report_linter_returncode",
            "observed_status",
            "n_linter_checks",
            "n_linter_fail",
            "summary",
            "stdout_tail",
            "stderr_tail",
            "score_values_read",
        ],
    )
    write_tsv(lint_path, lint_rows, ["scope", "item", "check", "status", "detail", "score_values_read"])

    n_fail = sum(1 for row in lint_rows if row["status"] != "PASS")
    all_score_false = all(row["score_values_read"] == "false" for row in rows + linter_rows + lint_rows)
    summary = {
        "synthetic": True,
        "purpose": "V46 safe-class report-template readiness; no biological claim",
        "n_safe_classes": len(rows),
        "n_linter_runs": len(linter_rows),
        "n_lint_checks": len(lint_rows),
        "n_lint_fail": n_fail,
        "all_score_values_read_false": all_score_false,
        "overall_status": "PASS" if n_fail == 0 and all_score_false else "FAIL",
        "map": rel(map_path),
        "linter_results": rel(linter_path),
        "lint": rel(lint_path),
    }
    (outdir / "safe_class_report_template_readiness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_markdown(outdir / "SAFE_CLASS_REPORT_TEMPLATE_READINESS.md", summary, rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if args.fail_on_error and summary["overall_status"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
