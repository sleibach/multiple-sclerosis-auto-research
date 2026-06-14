#!/usr/bin/env python3
"""Check that the V48 external-layer reader brief is fresh and boundary-safe."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BRIEF = ROOT / "knowledge_external/EXTERNAL_LAYER_READER_BRIEF_V48.md"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/external_layer_reader_brief_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_external_layer_reader_brief_freshness_linter"

REQUIRED_SECTIONS = [
    "The Short Version",
    "What The External Layer Can Do",
    "What The External Layer Cannot Do",
    "How To Interpret Convergence",
    "How To Interpret Contradiction",
    "How To Intake A New External Source",
    "Reader Checklist",
    "Boundary",
]

REQUIRED_LINKS = [
    "docs/knowledge/EPISTEMIC_CLASSES.md",
    "knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md",
    "knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md",
    "knowledge_external/synthesis/CONVERGENCE_SOURCE_INDEPENDENCE_V48.md",
    "knowledge_external/synthesis/DECISION_RELEVANT_CONVERGENCES_V48.md",
    "knowledge_external/synthesis/CONTRADICTION_READINESS_PLAYBOOK_V48.md",
    "knowledge_external/synthesis/CONTRADICTION_SURVEILLANCE_CHECKLIST_V48.md",
    "knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md",
    "scripts/v47_provenance_gate.py",
    "scripts/v48_governance_preflight.py",
]

REQUIRED_PHRASES = {
    "status_navigation_only": "class-aware public navigation only",
    "no_external_records": "does not add external records",
    "not_evidence": "It is not evidence for a project conclusion.",
    "no_override": "It cannot override a grounded project result.",
    "grounded_remains_evidence": "The project artifact remains the evidence.",
    "contradiction_not_override": "The external source does not override the grounded finding.",
}

EXTERNAL_MARKER_FRAGMENTS = [
    "external-verifiable",
    "external-unverifiable",
    "NOT_PROJECT_GROUNDED",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint external-layer reader brief freshness")
    lint.add_argument("--brief", type=Path, default=DEFAULT_BRIEF)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic reader-brief freshness fixtures")
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


def marker_lines_without_source(text: str) -> list[int]:
    failing_lines: list[int] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        if not any(fragment in line for fragment in EXTERNAL_MARKER_FRAGMENTS):
            continue
        if "source:" not in line.lower() and "http" not in line.lower() and "doi:" not in line.lower():
            failing_lines.append(line_no)
    return failing_lines


def lint_brief(brief: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    text = brief.read_text(errors="ignore") if brief.exists() else ""
    normalized_text = " ".join(text.split())
    rows: list[dict[str, object]] = []
    add(rows, "brief_exists", "PASS" if brief.exists() else "FAIL", str(brief))
    sections = h2_sections(text)
    for section in REQUIRED_SECTIONS:
        add(rows, f"section_present.{section}", "PASS" if section in sections else "FAIL", "required reader-brief section")
    for check, phrase in REQUIRED_PHRASES.items():
        add(rows, f"phrase_present.{check}", "PASS" if " ".join(phrase.split()) in normalized_text else "FAIL", "required boundary phrase")
    for link in REQUIRED_LINKS:
        add(rows, f"link_present.{link}", "PASS" if link in text else "FAIL", "required navigation target")
    failing_marker_lines = marker_lines_without_source(text)
    add(
        rows,
        "external_marker_lines_have_source",
        "PASS" if not failing_marker_lines else "FAIL",
        "failing_lines=" + ",".join(str(line_no) for line_no in failing_marker_lines),
    )
    summary = read_json(summary_path)
    summary_expectations = {
        "markdown": "knowledge_external/EXTERNAL_LAYER_READER_BRIEF_V48.md",
        "n_sections": len(REQUIRED_SECTIONS),
        "overall_status": "PASS",
        "purpose": "V48 external layer reader brief; class-aware public navigation only; no biological claim",
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
    write_tsv(outdir / "external_layer_reader_brief_freshness_lint.tsv", rows, ["check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 external layer reader brief freshness lint; navigation only; no biological claim",
        "n_required_sections": len(REQUIRED_SECTIONS),
        "n_required_links": len(REQUIRED_LINKS),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "external_layer_reader_brief_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    brief = outdir / "synthetic_brief.md"
    summary = outdir / "synthetic_summary.json"
    brief.write_text(
        "\n".join(
            [
                "# Synthetic Reader Brief",
                "",
                "Status: class-aware public navigation only. This synthetic fixture does not add external records.",
                "",
                "## The Short Version",
                "",
                "It is not evidence for a project conclusion.",
                "",
                "## Boundary",
                "",
                "The project artifact remains the evidence.",
            ]
        )
        + "\n"
    )
    summary.write_text(json.dumps({"markdown": "stale", "n_sections": 999, "overall_status": "FAIL"}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_brief(brief, summary, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "external_layer_reader_brief_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "missing_section_fails": any(row["check"] == "section_present.How To Interpret Convergence" and row["status"] == "FAIL" for row in rows),
        "missing_link_fails": any(row["check"].startswith("link_present.") and row["status"] == "FAIL" for row in rows),
        "missing_phrase_fails": any(row["check"] == "phrase_present.no_override" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["check"] == "summary_matches.n_sections" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_external_layer_reader_brief_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 external layer reader brief freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_external_layer_reader_brief_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_brief(args.brief, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
