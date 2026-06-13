#!/usr/bin/env python3
"""Lint validation result reports against V46 safe-interpretation classes.

This is report-governance infrastructure only. It verifies that a report cites a
V46 safe class and that blocked/no-score classes do not contain metric or
pass/fail validation language. It does not inspect data, compute scores, or make
biological claims.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_result_report_safe_class_linter"

NO_SCORE_CLASSES = {
    "BLOCKED_TERMS_OR_RECEIPT_GATES",
    "BLOCKED_REDACTION",
    "BLOCKED_COMPLETENESS",
    "BLOCKED_RETURN_GATE",
    "BLOCKED_SCHEMA",
    "BLOCKED_METADATA_CONTRADICTION",
    "CONTEXT_ONLY_OR_LABELS_NEEDED",
    "BELOW_V45_PLANNING_FLOOR",
}
SCORE_ALLOWED_CLASSES = {
    "INCONCLUSIVE_SMALL_COHORT",
    "MINIMUM_DECISION_GRADE_CAUTION",
    "CAUTION_BATCH_OR_CONFOUNDER",
    "ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION",
}
SAFE_CLASSES = NO_SCORE_CLASSES | SCORE_ALLOWED_CLASSES

FORBIDDEN_SCORE_PATTERNS = [
    r"\bAUC\b",
    r"\bHedges\b",
    r"\beffect[- ]size\b",
    r"\bp[- ]?value\b",
    r"\bpermutation\b",
    r"\bconfidence interval\b",
    r"\blocked_rule_metrics\.tsv\b",
    r"\bvalidation (?:pass|fail|passed|failed)\b",
    r"\b(?:pass|fail|passed|failed) validation\b",
    r"\bclean pre-registered pass\b",
]
REQUIRED_BOUNDARIES = [
    r"locked rule is unchanged",
    r"no post-hoc",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    lint = sub.add_parser("lint")
    lint.add_argument("--report", type=Path, required=True)
    lint.add_argument("--safe-class", choices=sorted(SAFE_CLASSES), required=True)
    lint.add_argument("--outdir", type=Path, required=True)
    lint.add_argument("--expect-status", choices=["PASS", "FAIL"])

    syn = sub.add_parser("synthetic-check")
    syn.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    syn.add_argument("--fail-on-error", action="store_true")
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


def contains(pattern: str, text: str) -> bool:
    return bool(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE))


def lint_text(report: Path, safe_class: str) -> list[dict[str, object]]:
    text = report.read_text(errors="ignore")
    rows: list[dict[str, object]] = []
    rows.append(
        {
            "report": rel(report),
            "safe_class": safe_class,
            "check": "safe_class_cited",
            "status": "PASS" if safe_class in text else "FAIL",
            "detail": "safe class literal found" if safe_class in text else "safe class literal missing",
        }
    )
    for pattern in REQUIRED_BOUNDARIES:
        found = contains(pattern, text)
        rows.append(
            {
                "report": rel(report),
                "safe_class": safe_class,
                "check": f"required_boundary:{pattern}",
                "status": "PASS" if found else "FAIL",
                "detail": "found" if found else "missing",
            }
        )
    if safe_class in NO_SCORE_CLASSES:
        for pattern in FORBIDDEN_SCORE_PATTERNS:
            found = contains(pattern, text)
            rows.append(
                {
                    "report": rel(report),
                    "safe_class": safe_class,
                    "check": f"forbidden_score_language:{pattern}",
                    "status": "FAIL" if found else "PASS",
                    "detail": "forbidden result language present" if found else "absent",
                }
            )
    else:
        has_grid = "V42" in text or "OUTCOME_INTERPRETATION_GRID_V42" in text
        has_source_boundary = "returned aggregate" in text.lower() or "locked_rule_metrics.tsv" in text
        rows.extend(
            [
                {
                    "report": rel(report),
                    "safe_class": safe_class,
                    "check": "score_allowed_report_uses_v42_grid",
                    "status": "PASS" if has_grid else "FAIL",
                    "detail": "V42/grid boundary found" if has_grid else "missing V42/grid boundary",
                },
                {
                    "report": rel(report),
                    "safe_class": safe_class,
                    "check": "score_allowed_report_sources_returned_aggregate",
                    "status": "PASS" if has_source_boundary else "FAIL",
                    "detail": "returned aggregate/source boundary found" if has_source_boundary else "missing returned aggregate/source boundary",
                },
            ]
        )
    return rows


def lint_report(report: Path, safe_class: str, outdir: Path, expect_status: str | None) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    report = resolve(report)
    report_text = report.read_text(errors="ignore")
    rows = lint_text(report, safe_class)
    lint_path = outdir / "result_report_safe_class_lint.tsv"
    write_tsv(lint_path, rows, ["report", "safe_class", "check", "status", "detail"])
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    observed = "PASS" if n_fail == 0 else "FAIL"
    summary = {
        "synthetic": "synthetic" in str(report).lower() or "synthetic" in str(outdir).lower() or "synthetic: true" in report_text.lower(),
        "purpose": "V46 result-report safe-class linter; no biological claim",
        "report": rel(report),
        "safe_class": safe_class,
        "n_checks": len(rows),
        "n_fail": n_fail,
        "observed_status": observed,
        "expected_status": expect_status or "",
        "expectation_met": not expect_status or observed == expect_status,
        "lint": rel(lint_path),
    }
    (outdir / "result_report_safe_class_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["expectation_met"] else 2


def write_fixture(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def synthetic_fixtures(outdir: Path) -> list[tuple[str, Path, str, str]]:
    fixtures = outdir / "fixtures"
    return [
        (
            "blocked_good",
            write_fixture(
                fixtures / "blocked_good.md",
                "# Synthetic Blocked Report\n\n"
                "synthetic: true\n\n"
                "V46 safe class: BLOCKED_COMPLETENESS\n\n"
                "Allowed wording: required aggregate outputs are missing. Request a complete return package only.\n\n"
                "Boundary: locked rule is unchanged; no post-hoc thresholds or interpretation are permitted.\n",
            ),
            "BLOCKED_COMPLETENESS",
            "PASS",
        ),
        (
            "blocked_bad_metric_leak",
            write_fixture(
                fixtures / "blocked_bad_metric_leak.md",
                "# Synthetic Bad Blocked Report\n\n"
                "synthetic: true\n\n"
                "V46 safe class: BLOCKED_COMPLETENESS\n\n"
                "AUC was 0.82 with a strong Hedges effect-size, so this is a validation pass.\n\n"
                "Boundary: locked rule is unchanged; no post-hoc thresholds are permitted.\n",
            ),
            "BLOCKED_COMPLETENESS",
            "FAIL",
        ),
        (
            "missing_safe_class",
            write_fixture(
                fixtures / "missing_safe_class.md",
                "# Synthetic Missing Safe Class Report\n\n"
                "synthetic: true\n\n"
                "Allowed wording: package is operationally blocked.\n\n"
                "Boundary: locked rule is unchanged; no post-hoc thresholds are permitted.\n",
            ),
            "BLOCKED_SCHEMA",
            "FAIL",
        ),
        (
            "eligible_good",
            write_fixture(
                fixtures / "eligible_good.md",
                "# Synthetic Eligible Report\n\n"
                "synthetic: true\n\n"
                "V46 safe class: ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION\n\n"
                "Interpretation uses the V42 outcome grid and returned aggregate outputs only.\n"
                "Metric source: locked_rule_metrics.tsv.\n\n"
                "Boundary: locked rule is unchanged; no post-hoc thresholds or modules are permitted.\n",
            ),
            "ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION",
            "PASS",
        ),
        (
            "caution_good",
            write_fixture(
                fixtures / "caution_good.md",
                "# Synthetic Caution Report\n\n"
                "synthetic: true\n\n"
                "V46 safe class: CAUTION_BATCH_OR_CONFOUNDER\n\n"
                "Interpretation uses the V42 outcome grid and returned aggregate diagnostics with explicit batch/confounder caveat.\n\n"
                "Boundary: locked rule is unchanged; no post-hoc thresholds or analyses are permitted.\n",
            ),
            "CAUTION_BATCH_OR_CONFOUNDER",
            "PASS",
        ),
    ]


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = resolve(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    fixture_rows: list[dict[str, object]] = []
    for name, report, safe_class, expected in synthetic_fixtures(outdir):
        case_out = outdir / name
        rc = lint_report(report, safe_class, case_out, expected)
        summary = json.loads((case_out / "result_report_safe_class_lint_summary.json").read_text())
        fixture_rows.append(
            {
                "case": name,
                "report": rel(report),
                "safe_class": safe_class,
                "expected_status": expected,
                "observed_status": summary["observed_status"],
                "expectation_met": str(summary["expectation_met"]).lower(),
                "returncode": rc,
                "summary": rel(case_out / "result_report_safe_class_lint_summary.json"),
            }
        )
    write_tsv(
        outdir / "result_report_safe_class_synthetic_cases.tsv",
        fixture_rows,
        ["case", "report", "safe_class", "expected_status", "observed_status", "expectation_met", "returncode", "summary"],
    )
    n_fail = sum(1 for row in fixture_rows if row["expectation_met"] != "true" or row["returncode"] != 0)
    summary = {
        "synthetic": True,
        "purpose": "V46 result-report safe-class linter synthetic check; no biological claim",
        "n_cases": len(fixture_rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "cases": rel(outdir / "result_report_safe_class_synthetic_cases.tsv"),
    }
    (outdir / "result_report_safe_class_synthetic_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if fail_on_error and n_fail else (0 if n_fail == 0 else 2)


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    return lint_report(resolve(args.report), args.safe_class, resolve(args.outdir), args.expect_status)


if __name__ == "__main__":
    raise SystemExit(main())
