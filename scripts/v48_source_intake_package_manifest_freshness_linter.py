#!/usr/bin/env python3
"""Check that the V48 source-intake package manifest is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "knowledge_external/templates/SOURCE_INTAKE_PACKAGE_MANIFEST_V48.md"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/source_intake_package_manifest_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_source_intake_package_manifest_freshness_linter"

REQUIRED_SECTIONS = [
    "Package Components",
    "Mandatory Operator Order",
    "Verification Commands",
    "What This Package Does Not Do",
    "Boundary",
]

REQUIRED_LINKS = [
    "knowledge_external/EXTERNAL_LAYER_READER_BRIEF_V48.md",
    "knowledge_external/synthesis/HIGH_PRIORITY_EXTERNAL_SOURCING_PLAN_V48.md",
    "knowledge_external/synthesis/HIGH_PRIORITY_SOURCE_SEARCH_QUERIES_V48.md",
    "knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md",
    "knowledge_external/templates/SOURCE_INTAKE_OPERATOR_QUICKSTART_V48.md",
    "knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md",
    "docs/knowledge/EPISTEMIC_CLASSES.md",
]

REQUIRED_COMMANDS = [
    "python3 scripts/v47_external_record_schema_linter.py lint --fail-on-error",
    "python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error",
    "python3 scripts/v47_provenance_gate.py audit --fail-on-error",
    "python3 scripts/v48_governance_preflight.py",
]

REQUIRED_PHRASES = {
    "status_navigation_only": "template/navigation only",
    "no_searches": "does not run searches",
    "no_external_records": "add external records",
    "no_convergence": "assert convergence",
    "no_contradiction": "flag contradiction",
    "no_grounded_change": "change grounded findings",
    "not_project_finding": "does not make any external source a project finding",
    "generic_context_forbidden": "does not permit generic adjacent context",
    "grounded_remains_evidence": "grounded project artifact remains the evidence",
}

EXPECTED_SUMMARY = {
    "markdown": "knowledge_external/templates/SOURCE_INTAKE_PACKAGE_MANIFEST_V48.md",
    "n_package_components": 6,
    "n_operator_order_steps": 6,
    "n_required_verification_commands": 4,
    "overall_status": "PASS",
    "purpose": "V48 source-intake package manifest; template/navigation only; no biological claim",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint source-intake package manifest freshness")
    lint.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic package-manifest freshness fixtures")
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


def count_numbered_steps(text: str, section: str) -> int:
    lines = text.splitlines()
    in_section = False
    count = 0
    for line in lines:
        if line == f"## {section}":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and re.match(r"^\d+\.\s+", line):
            count += 1
    return count


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
            if not stripped.lower().startswith("| order "):
                count += 1
    return count


def lint_manifest(manifest: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    text = manifest.read_text(errors="ignore") if manifest.exists() else ""
    rows: list[dict[str, object]] = []
    add(rows, "manifest_exists", "PASS" if manifest.exists() else "FAIL", str(manifest))
    sections = h2_sections(text)
    for section in REQUIRED_SECTIONS:
        add(rows, f"section_present.{section}", "PASS" if section in sections else "FAIL", "required source-intake package section")
    for link in REQUIRED_LINKS:
        add(rows, f"link_present.{link}", "PASS" if link in text else "FAIL", "required package component or source link")
    for command in REQUIRED_COMMANDS:
        add(rows, f"command_present.{command}", "PASS" if command in text else "FAIL", "required verification command")
    for check, phrase in REQUIRED_PHRASES.items():
        add(rows, f"phrase_present.{check}", "PASS" if normalized_contains(text, phrase) else "FAIL", "required boundary phrase")
    n_components = count_table_rows_after_section(text, "Package Components")
    n_steps = count_numbered_steps(text, "Mandatory Operator Order")
    add(rows, "table_count.package_components", "PASS" if n_components == 6 else "FAIL", f"observed={n_components} expected=6")
    add(rows, "step_count.operator_order", "PASS" if n_steps == 6 else "FAIL", f"observed={n_steps} expected=6")
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
    write_tsv(outdir / "source_intake_package_manifest_freshness_lint.tsv", rows, ["check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 source-intake package manifest freshness lint; template/navigation only; no biological claim",
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "source_intake_package_manifest_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    manifest = outdir / "synthetic_manifest.md"
    summary = outdir / "synthetic_summary.json"
    manifest.write_text(
        "\n".join(
            [
                "# Synthetic Manifest",
                "",
                "Status: template/navigation only.",
                "",
                "## Package Components",
                "",
                "| order | artifact | purpose | boundary |",
                "|---:|---|---|---|",
                "| 1 | `a.md` | one | navigation |",
                "",
                "## Mandatory Operator Order",
                "",
                "1. Do one thing.",
                "",
                "## Boundary",
                "",
                "This fixture deliberately omits required package controls.",
            ]
        )
        + "\n"
    )
    summary.write_text(json.dumps({"markdown": "stale", "n_package_components": 1, "n_operator_order_steps": 1, "overall_status": "FAIL"}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_manifest(manifest, summary, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "source_intake_package_manifest_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "missing_section_fails": any(row["check"] == "section_present.Verification Commands" and row["status"] == "FAIL" for row in rows),
        "missing_link_fails": any(row["check"].startswith("link_present.") and row["status"] == "FAIL" for row in rows),
        "bad_component_count_fails": any(row["check"] == "table_count.package_components" and row["status"] == "FAIL" for row in rows),
        "bad_step_count_fails": any(row["check"] == "step_count.operator_order" and row["status"] == "FAIL" for row in rows),
        "bad_summary_fails": any(row["check"] == "summary_matches.n_package_components" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_source_intake_package_manifest_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 source-intake package manifest freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_source_intake_package_manifest_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_manifest(args.manifest, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
