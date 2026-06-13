#!/usr/bin/env python3
"""Lint returned-package report headers before result text.

This is report-governance infrastructure only. It verifies that any returned-
package result report names the cohort token, route class, terms class, V46
safe class, and the frozen V22 locked-rule hash before a result section or
score-bearing text appears. It does not read returned score tables, expression
matrices, labels, or quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_report_header_metadata_linter"
BASELINE = ROOT / "docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv"
LOCKED_RULE_PATH = "docs/locked_rules/LOCKED_RULE_V22.md"

TERMS_CLASSES = {
    "LOCAL_PREFLIGHT_ALLOWED",
    "AGGREGATE_ONLY_LOCAL_PREFLIGHT",
    "AUTHOR_RUN_ONLY",
    "NO_PROCESSING_ALLOWED",
    "AMBIGUOUS_TERMS_BLOCK",
    "UNKNOWN",
}

ROUTE_CLASSES = {
    "BLOCKED_BEFORE_PACKAGE_HANDLING",
    "UNSCOREABLE_AGGREGATE_PREFLIGHT_ONLY",
    "SCORED_AGGREGATE_ADAPTER_REQUIRED",
    "SCORED_AGGREGATE_ALIAS_BRANCH_REQUIRED",
    "SCORED_AUTHOR_RUN_AGGREGATE_ONLY",
    "SCORED_AGGREGATE_CANONICAL_PATH",
}

SAFE_CLASSES = {
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
}

REQUIRED_FIELDS = [
    "cohort_token",
    "route_class",
    "terms_class",
    "safe_class",
    "locked_rule_path",
    "locked_rule_sha256",
]

RESULT_MARKERS = [
    re.compile(r"^\s*#{1,6}\s*(?:result|results|validation result|outcome interpretation)\b", re.I),
    re.compile(r"\b(?:AUC|Hedges|effect[- ]size|p[- ]?value|confidence interval)\b", re.I),
    re.compile(r"\blocked_rule_metrics\.tsv\b", re.I),
]
COHORT_TOKEN_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]{2,96}$")
HEADER_LINE_RE = re.compile(r"^\s*(?:[-*]\s*)?(?P<key>[A-Za-z0-9 _-]+)\s*:\s*`?(?P<value>[^`\n]+?)`?\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    lint = sub.add_parser("lint")
    lint.add_argument("--report", type=Path, required=True)
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


def locked_rule_hash() -> str:
    with BASELINE.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["path"] == LOCKED_RULE_PATH:
                return row["sha256"]
    raise RuntimeError(f"locked rule hash not found in {BASELINE}")


def normalize_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", key.strip().lower()).strip("_")


def first_result_line(lines: list[str]) -> int:
    for idx, line in enumerate(lines):
        if any(pattern.search(line) for pattern in RESULT_MARKERS):
            return idx
    return len(lines)


def parse_header(lines: list[str], limit: int) -> tuple[dict[str, str], dict[str, int]]:
    fields: dict[str, str] = {}
    locations: dict[str, int] = {}
    for idx, line in enumerate(lines):
        match = HEADER_LINE_RE.match(line)
        if not match:
            continue
        key = normalize_key(match.group("key"))
        value = match.group("value").strip()
        if key not in fields:
            fields[key] = value
            locations[key] = idx
    return fields, locations


def lint_text(report: Path, text: str) -> tuple[list[dict[str, object]], dict[str, str]]:
    lines = text.splitlines()
    result_idx = first_result_line(lines)
    fields, locations = parse_header(lines, result_idx)
    expected_hash = locked_rule_hash()
    rows: list[dict[str, object]] = []

    for field in REQUIRED_FIELDS:
        found = field in fields
        before_result = found and locations[field] < result_idx
        rows.append(
            {
                "report": rel(report),
                "check": f"required_field:{field}",
                "status": "PASS" if found and before_result else "FAIL",
                "detail": fields.get(field, "missing") if found else "missing",
                "field": field,
                "score_values_read": "false",
            }
        )

    token = fields.get("cohort_token", "")
    rows.append(
        {
            "report": rel(report),
            "check": "cohort_token_format",
            "status": "PASS" if COHORT_TOKEN_RE.match(token) else "FAIL",
            "detail": token or "missing",
            "field": "cohort_token",
            "score_values_read": "false",
        }
    )

    route = fields.get("route_class", "")
    rows.append(
        {
            "report": rel(report),
            "check": "route_class_known",
            "status": "PASS" if route in ROUTE_CLASSES else "FAIL",
            "detail": route or "missing",
            "field": "route_class",
            "score_values_read": "false",
        }
    )

    terms = fields.get("terms_class", "")
    rows.append(
        {
            "report": rel(report),
            "check": "terms_class_known",
            "status": "PASS" if terms in TERMS_CLASSES else "FAIL",
            "detail": terms or "missing",
            "field": "terms_class",
            "score_values_read": "false",
        }
    )

    safe_class = fields.get("safe_class", "")
    rows.append(
        {
            "report": rel(report),
            "check": "safe_class_known",
            "status": "PASS" if safe_class in SAFE_CLASSES else "FAIL",
            "detail": safe_class or "missing",
            "field": "safe_class",
            "score_values_read": "false",
        }
    )

    path_value = fields.get("locked_rule_path", "")
    rows.append(
        {
            "report": rel(report),
            "check": "locked_rule_path_exact",
            "status": "PASS" if path_value == LOCKED_RULE_PATH else "FAIL",
            "detail": path_value or "missing",
            "field": "locked_rule_path",
            "score_values_read": "false",
        }
    )

    hash_value = fields.get("locked_rule_sha256", "")
    rows.append(
        {
            "report": rel(report),
            "check": "locked_rule_hash_matches_v45_baseline",
            "status": "PASS" if hash_value == expected_hash else "FAIL",
            "detail": hash_value or "missing",
            "field": "locked_rule_sha256",
            "score_values_read": "false",
        }
    )

    rows.append(
        {
            "report": rel(report),
            "check": "metadata_before_result_text",
            "status": "PASS" if all(field in locations and locations[field] < result_idx for field in REQUIRED_FIELDS) else "FAIL",
            "detail": f"first_result_line={result_idx + 1 if result_idx < len(lines) else 'none'}",
            "field": "all_required_fields",
            "score_values_read": "false",
        }
    )
    return rows, fields


def lint_report(report: Path, outdir: Path, expect_status: str | None) -> int:
    report = resolve(report)
    outdir = resolve(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    text = report.read_text(errors="ignore")
    rows, fields = lint_text(report, text)
    lint_path = outdir / "report_header_metadata_lint.tsv"
    write_tsv(lint_path, rows, ["report", "check", "status", "detail", "field", "score_values_read"])
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    observed = "PASS" if n_fail == 0 else "FAIL"
    all_score_false = all(row["score_values_read"] == "false" for row in rows)
    summary = {
        "synthetic": "synthetic" in str(report).lower() or "synthetic: true" in text.lower(),
        "purpose": "V46 report-header metadata linter; no biological claim",
        "report": rel(report),
        "observed_status": observed,
        "expected_status": expect_status or "",
        "expectation_met": not expect_status or observed == expect_status,
        "n_checks": len(rows),
        "n_fail": n_fail,
        "all_score_values_read_false": all_score_false,
        "required_fields": REQUIRED_FIELDS,
        "observed_fields": {field: fields.get(field, "") for field in REQUIRED_FIELDS},
        "lint": rel(lint_path),
    }
    (outdir / "report_header_metadata_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["expectation_met"] and all_score_false else 2


def fixture_text(
    *,
    cohort_token: str = "synthetic_gafson_return_20260613",
    route_class: str = "SCORED_AGGREGATE_CANONICAL_PATH",
    terms_class: str = "AGGREGATE_ONLY_LOCAL_PREFLIGHT",
    safe_class: str = "ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION",
    locked_path: str = LOCKED_RULE_PATH,
    locked_hash: str | None = None,
    include_result_heading: bool = True,
) -> str:
    locked_hash = locked_hash or locked_rule_hash()
    result = ""
    if include_result_heading:
        result = (
            "\n## Result Text\n\n"
            "Result placeholders may be filled only after the metadata header, V46 safe class, and V42 grid are satisfied.\n"
        )
    return (
        "# Synthetic Returned-Package Report\n\n"
        "synthetic: true\n\n"
        "## V46 Report Header\n\n"
        f"cohort_token: {cohort_token}\n"
        f"route_class: {route_class}\n"
        f"terms_class: {terms_class}\n"
        f"safe_class: {safe_class}\n"
        f"locked_rule_path: {locked_path}\n"
        f"locked_rule_sha256: {locked_hash}\n"
        "score_values_read: false\n"
        f"{result}\n"
        "Boundary: locked rule is unchanged; no post-hoc thresholds are permitted.\n"
    )


def write_fixture(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def synthetic_fixtures(outdir: Path) -> list[tuple[str, Path, str]]:
    fixtures = outdir / "fixtures"
    expected_hash = locked_rule_hash()
    return [
        (
            "eligible_good",
            write_fixture(fixtures / "eligible_good.md", fixture_text()),
            "PASS",
        ),
        (
            "blocked_good",
            write_fixture(
                fixtures / "blocked_good.md",
                fixture_text(
                    route_class="BLOCKED_BEFORE_PACKAGE_HANDLING",
                    terms_class="NO_PROCESSING_ALLOWED",
                    safe_class="BLOCKED_TERMS_OR_RECEIPT_GATES",
                    include_result_heading=False,
                ),
            ),
            "PASS",
        ),
        (
            "missing_cohort_token",
            write_fixture(
                fixtures / "missing_cohort_token.md",
                fixture_text().replace("cohort_token: synthetic_gafson_return_20260613\n", ""),
            ),
            "FAIL",
        ),
        (
            "metadata_after_result",
            write_fixture(
                fixtures / "metadata_after_result.md",
                (
                    "# Synthetic Late Metadata Report\n\n"
                    "synthetic: true\n\n"
                    "## Result Text\n\n"
                    "Result placeholders are not allowed before metadata.\n\n"
                    "cohort_token: synthetic_late_metadata\n"
                    "route_class: SCORED_AGGREGATE_CANONICAL_PATH\n"
                    "terms_class: AGGREGATE_ONLY_LOCAL_PREFLIGHT\n"
                    "safe_class: ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION\n"
                    f"locked_rule_path: {LOCKED_RULE_PATH}\n"
                    f"locked_rule_sha256: {expected_hash}\n"
                ),
            ),
            "FAIL",
        ),
        (
            "wrong_locked_hash",
            write_fixture(fixtures / "wrong_locked_hash.md", fixture_text(locked_hash="0" * 64)),
            "FAIL",
        ),
        (
            "unknown_safe_class",
            write_fixture(fixtures / "unknown_safe_class.md", fixture_text(safe_class="UNREGISTERED_SAFE_CLASS")),
            "FAIL",
        ),
    ]


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = resolve(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    case_rows: list[dict[str, object]] = []
    for case, report, expected in synthetic_fixtures(outdir):
        case_out = outdir / case
        rc = lint_report(report, case_out, expected)
        summary = json.loads((case_out / "report_header_metadata_lint_summary.json").read_text())
        case_rows.append(
            {
                "case": case,
                "report": rel(report),
                "expected_status": expected,
                "observed_status": summary["observed_status"],
                "expectation_met": str(summary["expectation_met"]).lower(),
                "returncode": rc,
                "n_checks": summary["n_checks"],
                "n_fail": summary["n_fail"],
                "score_values_read": "false",
                "summary": rel(case_out / "report_header_metadata_lint_summary.json"),
            }
        )
    write_tsv(
        outdir / "report_header_metadata_synthetic_cases.tsv",
        case_rows,
        [
            "case",
            "report",
            "expected_status",
            "observed_status",
            "expectation_met",
            "returncode",
            "n_checks",
            "n_fail",
            "score_values_read",
            "summary",
        ],
    )
    n_fail = sum(1 for row in case_rows if row["expectation_met"] != "true" or row["score_values_read"] != "false")
    summary = {
        "synthetic": True,
        "purpose": "V46 report-header metadata linter synthetic check; no biological claim",
        "n_cases": len(case_rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in case_rows),
        "cases": rel(outdir / "report_header_metadata_synthetic_cases.tsv"),
    }
    (outdir / "report_header_metadata_synthetic_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if fail_on_error and n_fail else (0 if n_fail == 0 else 2)


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    return lint_report(args.report, args.outdir, args.expect_status)


if __name__ == "__main__":
    raise SystemExit(main())
