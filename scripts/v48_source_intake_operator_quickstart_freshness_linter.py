#!/usr/bin/env python3
"""Check that the V48 source-intake operator quickstart is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUICKSTART = ROOT / "knowledge_external/templates/SOURCE_INTAKE_OPERATOR_QUICKSTART_V48.md"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/source_intake_operator_quickstart_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_source_intake_operator_quickstart_freshness_linter"

REQUIRED_SECTIONS = [
    "Scope",
    "Mechanical Intake Order",
    "Required Checklist",
    "Safe Classification Table",
    "Minimum Record Fields",
    "Verification Before Commit",
    "Boundary",
]

REQUIRED_LINKS = [
    "knowledge_external/synthesis/HIGH_PRIORITY_SOURCE_SEARCH_QUERIES_V48.md",
    "knowledge_external/synthesis/HIGH_PRIORITY_EXTERNAL_SOURCING_PLAN_V48.md",
    "knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md",
    "docs/knowledge/EPISTEMIC_CLASSES.md",
    "knowledge_external/templates/README.md",
    "scripts/v47_external_record_schema_linter.py",
    "scripts/v47_external_markdown_index_linter.py",
    "scripts/v47_provenance_gate.py",
    "scripts/v48_governance_preflight.py",
]

REQUIRED_PHRASES = {
    "status_template_only": "template/navigation only",
    "no_external_records": "does not add external records",
    "no_convergence_assertion": "assert convergence",
    "terms_before_content": "Check source terms and reuse constraints before copying or summarizing any content.",
    "forbidden_shortcut": "Generic adjacent context cannot satisfy a source-specific acceptance criterion.",
    "checklist_before_review": "not ready for relationship-matrix review until every checklist step",
    "not_source_record": "This is an operator quickstart, not a source record.",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint source-intake operator quickstart freshness")
    lint.add_argument("--quickstart", type=Path, default=DEFAULT_QUICKSTART)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic source-intake quickstart freshness fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return data if isinstance(data, dict) else {}


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def add(rows: list[dict[str, object]], check: str, status: str, detail: str) -> None:
    rows.append({"check": check, "status": status, "detail": detail})


def h2_sections(text: str) -> list[str]:
    return [line.removeprefix("## ").strip() for line in text.splitlines() if line.startswith("## ")]


def mechanical_step_count(text: str) -> int:
    in_section = False
    count = 0
    for line in text.splitlines():
        if line.startswith("## Mechanical Intake Order"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and re.match(r"^\d+\.\s+", line):
            count += 1
    return count


def lint_quickstart(quickstart: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    text = quickstart.read_text(errors="ignore") if quickstart.exists() else ""
    normalized_text = " ".join(text.split())
    rows: list[dict[str, object]] = []
    add(rows, "quickstart_exists", "PASS" if quickstart.exists() else "FAIL", str(quickstart))
    sections = h2_sections(text)
    for section in REQUIRED_SECTIONS:
        add(rows, f"section_present.{section}", "PASS" if section in sections else "FAIL", "required quickstart section")
    step_count = mechanical_step_count(text)
    add(rows, "mechanical_step_count_is_9", "PASS" if step_count == 9 else "FAIL", f"observed={step_count}")
    for check, phrase in REQUIRED_PHRASES.items():
        add(rows, f"phrase_present.{check}", "PASS" if " ".join(phrase.split()) in normalized_text else "FAIL", "required boundary/workflow phrase")
    for link in REQUIRED_LINKS:
        add(rows, f"link_present.{link}", "PASS" if link in text else "FAIL", "required navigation target")
    summary = read_json(summary_path)
    summary_expectations = {
        "markdown": "knowledge_external/templates/SOURCE_INTAKE_OPERATOR_QUICKSTART_V48.md",
        "n_mechanical_steps": 9,
        "overall_status": "PASS",
        "purpose": "V48 source-intake operator quickstart; template/navigation only; no biological claim",
    }
    for field, expected_value in summary_expectations.items():
        add(
            rows,
            f"summary_matches.{field}",
            "PASS" if summary.get(field, "") == expected_value else "FAIL",
            f"expected={expected_value} observed={summary.get(field, '')}",
        )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "source_intake_operator_quickstart_freshness_lint.tsv", rows, ["check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 source-intake operator quickstart freshness lint; template/navigation only; no biological claim",
        "n_required_sections": len(REQUIRED_SECTIONS),
        "n_required_links": len(REQUIRED_LINKS),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "source_intake_operator_quickstart_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    quickstart = outdir / "synthetic_quickstart.md"
    summary = outdir / "synthetic_summary.json"
    quickstart.write_text(
        "\n".join(
            [
                "# Synthetic Quickstart",
                "",
                "Status: template/navigation only.",
                "",
                "## Scope",
                "",
                "## Mechanical Intake Order",
                "",
                "1. Record a locator.",
                "2. Record a date.",
                "",
                "## Boundary",
                "",
                "This is an operator quickstart, not a source record.",
            ]
        )
        + "\n"
    )
    summary.write_text(json.dumps({"markdown": "stale", "n_mechanical_steps": 999, "overall_status": "FAIL"}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_quickstart(quickstart, summary, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "source_intake_operator_quickstart_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "missing_section_fails": any(row["check"] == "section_present.Safe Classification Table" and row["status"] == "FAIL" for row in rows),
        "bad_step_count_fails": any(row["check"] == "mechanical_step_count_is_9" and row["status"] == "FAIL" for row in rows),
        "missing_link_fails": any(row["check"].startswith("link_present.") and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["check"] == "summary_matches.n_mechanical_steps" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_source_intake_operator_quickstart_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 source-intake operator quickstart freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_source_intake_operator_quickstart_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_quickstart(args.quickstart, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
