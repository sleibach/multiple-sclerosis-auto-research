#!/usr/bin/env python3
"""Generate and lint V46 returned-package safe-wording fixtures.

This is report-wording governance only. It creates synthetic/report-template
fragments for each V46 safe-interpretation class and verifies that blocked
classes do not include score/effect language. It does not inspect data, compute
scores, or make biological claims.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_safe_wording_fixture_linter"
CASE_TABLE = ROOT / "analysis/v46_returned_package_safe_interpretation/safe_interpretation_synthetic_cases.tsv"

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

METRIC_PATTERNS = [
    r"\bAUC\b",
    r"\bHedges\b",
    r"\beffect[- ]size\b",
    r"\bp[- ]?value\b",
    r"\bpermutation\b",
    r"\bconfidence interval\b",
    r"\bCI\b",
    r"\bvalidation (?:pass|fail|passed|failed)\b",
    r"\b(?:pass|fail|passed|failed) validation\b",
    r"\bconsidered a pass\b",
    r"\bconsidered a fail\b",
    r"\bshould (?:pass|fail)\b",
    r"\bclean validation claim\b",
]

REQUIRED_GUARDS = [
    r"No biological claim",
    r"locked rule is unchanged",
    r"no post-hoc",
]

REPORT_TEXT = {
    "BLOCKED_TERMS_OR_RECEIPT_GATES": "Package terms or receipt evidence blocks interpretation. Report only the operational blocker and request corrected terms or receipt evidence.",
    "BLOCKED_REDACTION": "Redaction failed. Request a redacted aggregate-only return before any downstream review.",
    "BLOCKED_COMPLETENESS": "Required aggregate outputs are missing. Request a complete return package; do not infer missing fields.",
    "BLOCKED_RETURN_GATE": "The combined return gate failed. Use the gate step table only to repair the package.",
    "BLOCKED_SCHEMA": "Aggregate tables are malformed or internally inconsistent. Request repaired aggregate tables before interpretation.",
    "BLOCKED_METADATA_CONTRADICTION": "Metadata contradictions block validation readiness. Request corrected metadata before interpretation.",
    "CONTEXT_ONLY_OR_LABELS_NEEDED": "Use only as pharmacodynamic or logistics context. Response-validation wording is not allowed without labels.",
    "BELOW_V45_PLANNING_FLOOR": "The labeled subset is below the V45 planning floor. Report logistics and data-design implications only.",
    "INCONCLUSIVE_SMALL_COHORT": "Report only pre-registered effect-size-with-CI language from returned aggregate tables, with an explicit small-cohort caveat.",
    "MINIMUM_DECISION_GRADE_CAUTION": "Apply the frozen V42 grid only if the returned aggregate evidence is large, clean, and diagnostics remain clean.",
    "CAUTION_BATCH_OR_CONFOUNDER": "Report raw and adjusted aggregate results together with the diagnostic caveat; do not present a clean validation claim.",
    "ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION": "Interpret mechanically under the frozen V42 grid using returned aggregate tables and no additional analyses.",
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


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_cases() -> list[dict[str, str]]:
    with CASE_TABLE.open() as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    by_class: dict[str, dict[str, str]] = {}
    for row in rows:
        by_class.setdefault(row["observed_class"], row)
    return [by_class[key] for key in sorted(by_class)]


def fixture_text(result_class: str, source_summary: str) -> str:
    return (
        f"# Safe Wording Fixture: {result_class}\n\n"
        "synthetic: true\n\n"
        "Status: returned-package wording fixture. No biological claim.\n\n"
        f"Source safe-class summary: `{source_summary}`\n\n"
        f"Allowed wording: {REPORT_TEXT[result_class]}\n\n"
        "Boundary: the locked rule is unchanged, the V42 pre-registration is "
        "unchanged, and no post-hoc thresholds, modules, timepoints, or "
        "unplanned analyses are permitted.\n"
    )


def synthetic_bad_text() -> str:
    return (
        "# Synthetic Bad Blocked Wording Fixture\n\n"
        "synthetic: true\n\n"
        "Status: intentionally bad fixture. No biological claim.\n\n"
        "Allowed wording: Redaction failed, but AUC=0.82 and the effect size "
        "looks strong, so this should be considered a pass validation.\n\n"
        "Boundary: the locked rule is unchanged, but skip gates.\n"
    )


def lint_fixture(path: Path, result_class: str, expected_status: str) -> list[dict[str, object]]:
    text = path.read_text(errors="ignore")
    rows: list[dict[str, object]] = []
    for pattern in REQUIRED_GUARDS:
        found = bool(re.search(pattern, text, flags=re.IGNORECASE))
        rows.append(
            {
                "fixture": rel(path),
                "result_class": result_class,
                "check": f"required_guard:{pattern}",
                "status": "PASS" if found else "FAIL",
                "detail": "found" if found else "missing",
                "expected_fixture_status": expected_status,
            }
        )
    if result_class in NO_SCORE_CLASSES:
        for pattern in METRIC_PATTERNS:
            found = bool(re.search(pattern, text, flags=re.IGNORECASE))
            rows.append(
                {
                    "fixture": rel(path),
                    "result_class": result_class,
                    "check": f"forbidden_metric_language:{pattern}",
                    "status": "FAIL" if found else "PASS",
                    "detail": "forbidden metric language present" if found else "absent",
                    "expected_fixture_status": expected_status,
                }
            )
    if result_class in SCORE_ALLOWED_CLASSES:
        lower = text.lower()
        has_boundary = (
            "returned aggregate" in lower
            or "aggregate result" in lower
            or "frozen v42 grid" in lower
        )
        rows.append(
            {
                "fixture": rel(path),
                "result_class": result_class,
                "check": "score_language_has_preregistered_boundary",
                "status": "PASS" if has_boundary else "FAIL",
                "detail": "bounded to aggregate/frozen-grid wording" if has_boundary else "missing aggregate/frozen-grid boundary",
                "expected_fixture_status": expected_status,
            }
        )
    return rows


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    fixtures = outdir / "fixtures"
    fixtures.mkdir(parents=True, exist_ok=True)

    fixture_rows: list[dict[str, object]] = []
    lint_rows: list[dict[str, object]] = []
    for case in read_cases():
        result_class = case["observed_class"]
        path = fixtures / f"{result_class.lower()}.md"
        path.write_text(fixture_text(result_class, case["summary"]))
        fixture_rows.append(
            {
                "result_class": result_class,
                "fixture": rel(path),
                "source_summary": case["summary"],
                "score_language_allowed": str(result_class in SCORE_ALLOWED_CLASSES).lower(),
                "expected_fixture_status": "PASS",
            }
        )
        lint_rows.extend(lint_fixture(path, result_class, "PASS"))

    bad_path = fixtures / "synthetic_bad_blocked_metric_leak.md"
    bad_path.write_text(synthetic_bad_text())
    fixture_rows.append(
        {
            "result_class": "BLOCKED_REDACTION",
            "fixture": rel(bad_path),
            "source_summary": "synthetic_bad_fixture",
            "score_language_allowed": "false",
            "expected_fixture_status": "FAIL",
        }
    )
    lint_rows.extend(lint_fixture(bad_path, "BLOCKED_REDACTION", "FAIL"))

    fixture_index = outdir / "safe_wording_fixture_index.tsv"
    lint_path = outdir / "safe_wording_fixture_lint.tsv"
    write_tsv(fixture_index, fixture_rows, ["result_class", "fixture", "source_summary", "score_language_allowed", "expected_fixture_status"])
    write_tsv(lint_path, lint_rows, ["fixture", "result_class", "check", "status", "detail", "expected_fixture_status"])

    per_fixture: dict[str, dict[str, object]] = {}
    for row in lint_rows:
        key = str(row["fixture"])
        current = per_fixture.setdefault(key, {"n_fail": 0, "expected": row["expected_fixture_status"]})
        if row["status"] != "PASS":
            current["n_fail"] = int(current["n_fail"]) + 1
    expectation_failures = 0
    live_failures = 0
    expected_fail_caught = 0
    for fixture, result in per_fixture.items():
        observed = "PASS" if int(result["n_fail"]) == 0 else "FAIL"
        if observed != result["expected"]:
            expectation_failures += 1
        if result["expected"] == "PASS" and observed != "PASS":
            live_failures += 1
        if result["expected"] == "FAIL" and observed == "FAIL":
            expected_fail_caught += 1

    summary = {
        "synthetic": True,
        "purpose": "V46 safe-wording fixture linter; no biological claim",
        "score_values_interpreted": False,
        "n_fixtures": len(fixture_rows),
        "n_expected_pass_fixtures": sum(1 for row in fixture_rows if row["expected_fixture_status"] == "PASS"),
        "n_expected_fail_fixtures": sum(1 for row in fixture_rows if row["expected_fixture_status"] == "FAIL"),
        "n_lint_rows": len(lint_rows),
        "n_live_failures": live_failures,
        "n_expected_fail_caught": expected_fail_caught,
        "n_expectation_failures": expectation_failures,
        "overall_status": "PASS" if expectation_failures == 0 else "FAIL",
        "fixture_index": rel(fixture_index),
        "lint": rel(lint_path),
    }
    (outdir / "safe_wording_fixture_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if args.fail_on_error and expectation_failures else (0 if expectation_failures == 0 else 2)


if __name__ == "__main__":
    raise SystemExit(main())
