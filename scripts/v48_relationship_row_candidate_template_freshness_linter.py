#!/usr/bin/env python3
"""Check that the V48 relationship-row candidate template is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "knowledge_external/templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/relationship_row_candidate_template_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_relationship_row_candidate_template_freshness_linter"

REQUIRED_SECTIONS = [
    "When To Use",
    "Candidate Row Fields",
    "Allowed Candidate Statuses",
    "Forbidden Shortcuts",
    "Promotion Rules",
    "Boundary",
]

REQUIRED_LINKS = [
    "knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md",
    "knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md",
    "docs/knowledge/EPISTEMIC_CLASSES.md",
    "scripts/v48_governance_preflight.py",
]

REQUIRED_PHRASES = {
    "template_navigation_only": "template/navigation only",
    "does_not_add_row": "does not add a matrix row",
    "no_convergence": "assert convergence",
    "no_contradiction": "flag contradiction",
    "same_definition": "same-definition overlap",
    "source_independence": "source-independence",
    "candidate_not_finding": "Candidate rows are not findings",
    "not_evidence": "not evidence",
    "grounded_remains_evidence": "grounded project artifact remains the evidence",
}

EXPECTED_STATUSES = [
    "candidate_convergence",
    "candidate_contradiction",
    "insufficient_overlap",
    "future_grounding_only",
]

EXPECTED_SUMMARY = {
    "markdown": "knowledge_external/templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md",
    "n_allowed_candidate_statuses": 4,
    "n_forbidden_shortcuts": 5,
    "n_required_fields": 15,
    "overall_status": "PASS",
    "purpose": "V48 relationship-row candidate template; template/navigation only; no biological claim",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint relationship-row candidate template freshness")
    lint.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic relationship-row template fixtures")
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
            if not lowered.startswith("| field ") and not lowered.startswith("| status ") and not lowered.startswith("| shortcut "):
                count += 1
    return count


def lint_template(template: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    text = template.read_text(errors="ignore") if template.exists() else ""
    rows: list[dict[str, object]] = []
    add(rows, "template_exists", "PASS" if template.exists() else "FAIL", str(template))
    sections = h2_sections(text)
    for section in REQUIRED_SECTIONS:
        add(rows, f"section_present.{section}", "PASS" if section in sections else "FAIL", "required candidate-template section")
    for link in REQUIRED_LINKS:
        add(rows, f"link_present.{link}", "PASS" if link in text else "FAIL", "required link")
    for status in EXPECTED_STATUSES:
        add(rows, f"candidate_status_present.{status}", "PASS" if f"`{status}`" in text else "FAIL", "required candidate status")
    for check, phrase in REQUIRED_PHRASES.items():
        add(rows, f"phrase_present.{check}", "PASS" if normalized_contains(text, phrase) else "FAIL", "required boundary phrase")
    n_fields = count_table_rows_after_section(text, "Candidate Row Fields")
    n_statuses = count_table_rows_after_section(text, "Allowed Candidate Statuses")
    n_shortcuts = count_table_rows_after_section(text, "Forbidden Shortcuts")
    add(rows, "table_count.required_fields", "PASS" if n_fields == 15 else "FAIL", f"observed={n_fields} expected=15")
    add(rows, "table_count.allowed_statuses", "PASS" if n_statuses == 4 else "FAIL", f"observed={n_statuses} expected=4")
    add(rows, "table_count.forbidden_shortcuts", "PASS" if n_shortcuts == 5 else "FAIL", f"observed={n_shortcuts} expected=5")
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
    write_tsv(outdir / "relationship_row_candidate_template_freshness_lint.tsv", rows, ["check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 relationship-row candidate template freshness lint; template/navigation only; no biological claim",
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "relationship_row_candidate_template_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    template = outdir / "synthetic_template.md"
    summary = outdir / "synthetic_summary.json"
    template.write_text(
        "\n".join(
            [
                "# Synthetic Candidate Template",
                "",
                "Status: template/navigation only.",
                "",
                "## Candidate Row Fields",
                "",
                "| field | required | meaning |",
                "|---|---|---|",
                "| `candidate_id` | yes | one |",
                "",
                "## Boundary",
                "",
                "This fixture deliberately omits required statuses and controls.",
            ]
        )
        + "\n"
    )
    summary.write_text(json.dumps({"markdown": "stale", "n_required_fields": 1, "n_allowed_candidate_statuses": 0, "overall_status": "FAIL"}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_template(template, summary, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "relationship_row_candidate_template_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "missing_section_fails": any(row["check"] == "section_present.When To Use" and row["status"] == "FAIL" for row in rows),
        "missing_status_fails": any(row["check"] == "candidate_status_present.candidate_convergence" and row["status"] == "FAIL" for row in rows),
        "bad_field_count_fails": any(row["check"] == "table_count.required_fields" and row["status"] == "FAIL" for row in rows),
        "bad_status_count_fails": any(row["check"] == "table_count.allowed_statuses" and row["status"] == "FAIL" for row in rows),
        "bad_summary_fails": any(row["check"] == "summary_matches.n_required_fields" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_relationship_row_candidate_template_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 relationship-row candidate template freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_relationship_row_candidate_template_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
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
