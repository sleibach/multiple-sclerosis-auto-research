#!/usr/bin/env python3
"""Check that the V48 active-time accounting audit card is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CARD = ROOT / "knowledge_external/catalogs/indexes/V48_ACTIVE_TIME_ACCOUNTING_AUDIT.md"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/active_time_accounting_audit_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_active_time_accounting_audit_freshness_linter"

REQUIRED_SECTIONS = [
    "Required Controls",
    "Timing Rules",
    "Audit Checks",
    "Reporting Template",
    "Boundary",
]

REQUIRED_LINKS = [
    "meta/V48_QUEUE.md",
    "knowledge_external/catalogs/indexes/V48_PREFLIGHT_SUMMARY_CARD.md",
    "knowledge_external/catalogs/indexes/V48_GOVERNANCE_NAVIGATION.md",
    "scripts/v47_provenance_gate.py",
]

REQUIRED_PHRASES = {
    "governance_navigation_only": "governance/navigation only",
    "active_sum": "sum of recorded session intervals",
    "exclude_gaps": "Idle gaps between sessions are excluded",
    "target_metric": "21600 active seconds",
    "separate_wall_clock": "Wall-clock span must be reported separately",
    "operational_metadata": "operational timing metadata only",
    "does_not_affect_findings": "does not affect external knowledge provenance, project findings, locked rules, validation plans, or evidence grades",
}

EXPECTED_SUMMARY = {
    "markdown": "knowledge_external/catalogs/indexes/V48_ACTIVE_TIME_ACCOUNTING_AUDIT.md",
    "n_audit_checks": 6,
    "n_required_linked_controls": 4,
    "n_timing_rules": 5,
    "overall_status": "PASS",
    "purpose": "V48 active-time accounting audit card; governance/navigation only; no biological claim",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint active-time accounting audit freshness")
    lint.add_argument("--card", type=Path, default=DEFAULT_CARD)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic active-time accounting fixtures")
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
            if not lowered.startswith("| rule ") and not lowered.startswith("| check "):
                count += 1
    return count


def lint_card(card: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    text = card.read_text(errors="ignore") if card.exists() else ""
    rows: list[dict[str, object]] = []
    add(rows, "card_exists", "PASS" if card.exists() else "FAIL", str(card))
    sections = h2_sections(text)
    for section in REQUIRED_SECTIONS:
        add(rows, f"section_present.{section}", "PASS" if section in sections else "FAIL", "required active-time audit section")
    for link in REQUIRED_LINKS:
        add(rows, f"link_present.{link}", "PASS" if link in text else "FAIL", "required linked control")
    for check, phrase in REQUIRED_PHRASES.items():
        add(rows, f"phrase_present.{check}", "PASS" if normalized_contains(text, phrase) else "FAIL", "required boundary phrase")
    n_rules = count_table_rows_after_section(text, "Timing Rules")
    n_checks = count_table_rows_after_section(text, "Audit Checks")
    add(rows, "table_count.timing_rules", "PASS" if n_rules == 5 else "FAIL", f"observed={n_rules} expected=5")
    add(rows, "table_count.audit_checks", "PASS" if n_checks == 6 else "FAIL", f"observed={n_checks} expected=6")
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
    write_tsv(outdir / "active_time_accounting_audit_freshness_lint.tsv", rows, ["check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 active-time accounting audit freshness lint; governance/navigation only; no biological claim",
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "active_time_accounting_audit_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    card = outdir / "synthetic_active_time.md"
    summary = outdir / "synthetic_summary.json"
    card.write_text(
        "\n".join(
            [
                "# Synthetic Active Time",
                "",
                "Status: governance/navigation only.",
                "",
                "## Timing Rules",
                "",
                "| rule | requirement |",
                "|---|---|",
                "| one | note |",
                "",
                "## Boundary",
                "",
                "This fixture deliberately omits required links and counts.",
            ]
        )
        + "\n"
    )
    summary.write_text(json.dumps({"markdown": "stale", "n_timing_rules": 1, "n_audit_checks": 0, "overall_status": "FAIL"}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_card(card, summary, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "active_time_accounting_audit_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "missing_section_fails": any(row["check"] == "section_present.Required Controls" and row["status"] == "FAIL" for row in rows),
        "missing_link_fails": any(row["check"].startswith("link_present.") and row["status"] == "FAIL" for row in rows),
        "bad_rule_count_fails": any(row["check"] == "table_count.timing_rules" and row["status"] == "FAIL" for row in rows),
        "bad_audit_count_fails": any(row["check"] == "table_count.audit_checks" and row["status"] == "FAIL" for row in rows),
        "bad_summary_fails": any(row["check"] == "summary_matches.n_timing_rules" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_active_time_accounting_audit_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 active-time accounting audit freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_active_time_accounting_audit_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_card(args.card, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
