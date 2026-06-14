#!/usr/bin/env python3
"""Check that the V48 contradiction triage mini-template is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "knowledge_external/templates/CONTRADICTION_TRIAGE_MINI_TEMPLATE_V48.md"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/contradiction_triage_mini_template_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_contradiction_triage_mini_template_freshness_linter"

REQUIRED_SECTIONS = [
    "Required Controls",
    "Triage Questions",
    "Safe Outcomes",
    "Minimum Candidate Notes",
    "Boundary",
]

REQUIRED_LINKS = [
    "knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md",
    "knowledge_external/templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md",
    "knowledge_external/synthesis/CONTRADICTION_READINESS_PLAYBOOK_V48.md",
    "knowledge_external/synthesis/CONTRADICTION_SURVEILLANCE_CHECKLIST_V48.md",
    "knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md",
]

REQUIRED_PHRASES = {
    "template_navigation_only": "template/navigation only",
    "does_not_assert": "does not assert a contradiction",
    "does_not_resolve": "resolve a contradiction",
    "does_not_override": "override a grounded finding",
    "no_matrix_change": "change the V48 relationship matrix",
    "same_definition": "same population, disease subtype, compartment, direction, and outcome",
    "tension_flag": "External disagreement is a tension flag, not a decision",
    "grounded_remains_evidence": "grounded project artifact remains the evidence",
}

EXPECTED_SUMMARY = {
    "markdown": "knowledge_external/templates/CONTRADICTION_TRIAGE_MINI_TEMPLATE_V48.md",
    "n_required_linked_controls": 5,
    "n_safe_outcomes": 5,
    "n_triage_questions": 8,
    "overall_status": "PASS",
    "purpose": "V48 contradiction triage mini-template; template/navigation only; no biological claim",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint contradiction triage mini-template freshness")
    lint.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic contradiction triage fixtures")
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
            if not lowered.startswith("| order ") and not lowered.startswith("| outcome "):
                count += 1
    return count


def lint_template(template: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    text = template.read_text(errors="ignore") if template.exists() else ""
    rows: list[dict[str, object]] = []
    add(rows, "template_exists", "PASS" if template.exists() else "FAIL", str(template))
    sections = h2_sections(text)
    for section in REQUIRED_SECTIONS:
        add(rows, f"section_present.{section}", "PASS" if section in sections else "FAIL", "required contradiction-triage section")
    for link in REQUIRED_LINKS:
        add(rows, f"link_present.{link}", "PASS" if link in text else "FAIL", "required linked control")
    for check, phrase in REQUIRED_PHRASES.items():
        add(rows, f"phrase_present.{check}", "PASS" if normalized_contains(text, phrase) else "FAIL", "required boundary phrase")
    n_questions = count_table_rows_after_section(text, "Triage Questions")
    n_outcomes = count_table_rows_after_section(text, "Safe Outcomes")
    add(rows, "table_count.triage_questions", "PASS" if n_questions == 8 else "FAIL", f"observed={n_questions} expected=8")
    add(rows, "table_count.safe_outcomes", "PASS" if n_outcomes == 5 else "FAIL", f"observed={n_outcomes} expected=5")
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
    write_tsv(outdir / "contradiction_triage_mini_template_freshness_lint.tsv", rows, ["check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 contradiction triage mini-template freshness lint; template/navigation only; no biological claim",
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "contradiction_triage_mini_template_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    template = outdir / "synthetic_contradiction_template.md"
    summary = outdir / "synthetic_summary.json"
    template.write_text(
        "\n".join(
            [
                "# Synthetic Contradiction Triage",
                "",
                "Status: template/navigation only.",
                "",
                "## Triage Questions",
                "",
                "| order | question | safe handling |",
                "|---:|---|---|",
                "| 1 | one | note |",
                "",
                "## Boundary",
                "",
                "This fixture deliberately omits required controls.",
            ]
        )
        + "\n"
    )
    summary.write_text(json.dumps({"markdown": "stale", "n_triage_questions": 1, "n_safe_outcomes": 0, "overall_status": "FAIL"}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_template(template, summary, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "contradiction_triage_mini_template_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "missing_section_fails": any(row["check"] == "section_present.Required Controls" and row["status"] == "FAIL" for row in rows),
        "missing_link_fails": any(row["check"].startswith("link_present.") and row["status"] == "FAIL" for row in rows),
        "bad_question_count_fails": any(row["check"] == "table_count.triage_questions" and row["status"] == "FAIL" for row in rows),
        "bad_outcome_count_fails": any(row["check"] == "table_count.safe_outcomes" and row["status"] == "FAIL" for row in rows),
        "bad_summary_fails": any(row["check"] == "summary_matches.n_triage_questions" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_contradiction_triage_mini_template_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 contradiction triage mini-template freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_contradiction_triage_mini_template_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
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
