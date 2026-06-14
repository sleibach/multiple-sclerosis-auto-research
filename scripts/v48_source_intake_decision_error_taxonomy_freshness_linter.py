#!/usr/bin/env python3
"""Check that the V48 source-intake decision error taxonomy is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "knowledge_external/templates/SOURCE_INTAKE_DECISION_ERROR_TAXONOMY_V48.md"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/source_intake_decision_error_taxonomy_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_source_intake_decision_error_taxonomy_freshness_linter"

REQUIRED_SECTIONS = [
    "Required Controls",
    "Error Classes",
    "Severity Levels",
    "Minimum QA Record",
    "Forbidden Shortcuts",
    "Verification Before Commit",
    "Boundary",
]

REQUIRED_LINKS = [
    "knowledge_external/templates/EXTERNAL_INTAKE_ONE_PAGE_CHECKLIST_V48.md",
    "knowledge_external/templates/SOURCE_INTAKE_AUDIT_LOG_TEMPLATE_V48.md",
    "knowledge_external/templates/SOURCE_HIT_ACCESS_TERMS_PARKING_QUEUE_V48.md",
    "knowledge_external/templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md",
    "knowledge_external/templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md",
    "knowledge_external/templates/CONTRADICTION_TRIAGE_MINI_TEMPLATE_V48.md",
    "scripts/v47_provenance_gate.py",
]

REQUIRED_PHRASES = {
    "template_navigation_only": "template/navigation only",
    "does_not_add_records": "does not add external records",
    "does_not_judge_truth": "judge scientific truth",
    "does_not_change_grounded": "change grounded findings",
    "external_override_critical": "external_override_attempt",
    "model_output_error": "model_output_as_evidence",
    "no_reclassify_grounded": "Do not fix an error by reclassifying external material as grounded",
    "no_audit_deletion": "Do not hide an error by deleting the audit trail",
    "protects_boundary": "protect provenance, source independence, and the grounded/external boundary",
}

EXPECTED_SUMMARY = {
    "markdown": "knowledge_external/templates/SOURCE_INTAKE_DECISION_ERROR_TAXONOMY_V48.md",
    "n_error_classes": 10,
    "n_required_linked_controls": 7,
    "n_severity_levels": 4,
    "overall_status": "PASS",
    "purpose": "V48 source-intake decision error taxonomy; template/navigation only; no biological claim",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint source-intake error taxonomy freshness")
    lint.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic source-intake error taxonomy fixtures")
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


def normalized_contains(text: str, phrase: str) -> bool:
    return " ".join(phrase.split()).lower() in " ".join(text.split()).lower()


def count_table_rows_after_section(text: str, section: str) -> int:
    lines = text.splitlines()
    in_section = False
    count = 0
    for line in lines:
        if line == f"## {section}":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section:
            continue
        stripped = line.strip()
        if stripped.startswith("|") and not stripped.startswith("|---") and "---|" not in stripped:
            lowered = stripped.lower()
            if not lowered.startswith("| error_class ") and not lowered.startswith("| severity "):
                count += 1
    return count


def lint_template(template: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    text = template.read_text(errors="ignore") if template.exists() else ""
    rows: list[dict[str, object]] = []
    add(rows, "template_exists", "PASS" if template.exists() else "FAIL", str(template))
    sections = h2_sections(text)
    for section in REQUIRED_SECTIONS:
        add(rows, f"section_present.{section}", "PASS" if section in sections else "FAIL", "required decision-error taxonomy section")
    for link in REQUIRED_LINKS:
        add(rows, f"link_present.{link}", "PASS" if link in text else "FAIL", "required linked control")
    for check, phrase in REQUIRED_PHRASES.items():
        add(rows, f"phrase_present.{check}", "PASS" if normalized_contains(text, phrase) else "FAIL", "required boundary phrase")
    n_errors = count_table_rows_after_section(text, "Error Classes")
    n_severity = count_table_rows_after_section(text, "Severity Levels")
    add(rows, "table_count.error_classes", "PASS" if n_errors == 10 else "FAIL", f"observed={n_errors} expected=10")
    add(rows, "table_count.severity_levels", "PASS" if n_severity == 4 else "FAIL", f"observed={n_severity} expected=4")
    summary = read_json(summary_path)
    for field, expected_value in EXPECTED_SUMMARY.items():
        add(
            rows,
            f"summary_matches.{field}",
            "PASS" if summary.get(field, "") == expected_value else "FAIL",
            f"expected={expected_value} observed={summary.get(field, '')}",
        )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "source_intake_decision_error_taxonomy_freshness_lint.tsv", rows, ["check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 source-intake decision error taxonomy freshness lint; template/navigation only; no biological claim",
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "source_intake_decision_error_taxonomy_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    template = outdir / "synthetic_error_taxonomy.md"
    summary = outdir / "synthetic_summary.json"
    template.write_text(
        "\n".join(
            [
                "# Synthetic Error Taxonomy",
                "",
                "Status: template/navigation only.",
                "",
                "## Error Classes",
                "",
                "| error_class | description | correction route |",
                "|---|---|---|",
                "| one | note | route |",
                "",
                "## Boundary",
                "",
                "This fixture deliberately omits required links and counts.",
            ]
        )
        + "\n"
    )
    summary.write_text(json.dumps({"markdown": "stale", "n_error_classes": 1, "n_severity_levels": 0, "overall_status": "FAIL"}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_template(template, summary, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "source_intake_decision_error_taxonomy_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "missing_section_fails": any(row["check"] == "section_present.Required Controls" and row["status"] == "FAIL" for row in rows),
        "missing_link_fails": any(row["check"].startswith("link_present.") and row["status"] == "FAIL" for row in rows),
        "bad_error_count_fails": any(row["check"] == "table_count.error_classes" and row["status"] == "FAIL" for row in rows),
        "bad_severity_count_fails": any(row["check"] == "table_count.severity_levels" and row["status"] == "FAIL" for row in rows),
        "bad_summary_fails": any(row["check"] == "summary_matches.n_error_classes" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_source_intake_decision_error_taxonomy_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 source-intake decision error taxonomy freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_source_intake_decision_error_taxonomy_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_template(args.template, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
