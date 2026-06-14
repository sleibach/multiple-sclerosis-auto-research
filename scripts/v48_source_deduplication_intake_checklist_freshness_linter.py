#!/usr/bin/env python3
"""Check that the V48 source de-duplication intake checklist is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "knowledge_external/templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/source_deduplication_intake_checklist_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_source_deduplication_intake_checklist_freshness_linter"

REQUIRED_SECTIONS = [
    "Required Controls",
    "De-Duplication Checks",
    "Duplicate States",
    "Safe Merge Actions",
    "Minimum Independence Note",
    "Forbidden Shortcuts",
    "Verification Before Commit",
    "Boundary",
]

REQUIRED_LINKS = [
    "knowledge_external/templates/SOURCE_INTAKE_PACKAGE_MANIFEST_V48.md",
    "knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md",
    "knowledge_external/templates/SOURCE_HIT_ACCESS_TERMS_PARKING_QUEUE_V48.md",
    "knowledge_external/catalogs/indexes/SOURCE_URL_DUPLICATE_REVIEW_V48.md",
    "knowledge_external/synthesis/CONVERGENCE_SOURCE_INDEPENDENCE_V48.md",
    "knowledge_external/catalogs/indexes/SOURCE_DOMAIN_INDEPENDENCE_ROLLUP_V48.md",
]

REQUIRED_PHRASES = {
    "template_navigation_only": "template/navigation only",
    "does_not_add_records": "does not add external records",
    "does_not_assert_relationship": "assert relationship rows",
    "does_not_change_grounded": "change grounded findings",
    "no_review_overcount": "Do not count a review as independent corroboration",
    "no_model_shortcut": "Do not use model/RPT summaries",
    "no_unclear_independence": "Do not create convergence or contradiction rows when independence is unclear",
    "not_evidence": "does not make an external source evidence",
    "same_source_overcounting": "same-source overcounting",
}

EXPECTED_SUMMARY = {
    "markdown": "knowledge_external/templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md",
    "n_deduplication_checks": 9,
    "n_duplicate_states": 5,
    "n_required_linked_controls": 6,
    "n_safe_merge_actions": 5,
    "overall_status": "PASS",
    "purpose": "V48 source de-duplication intake checklist; template/navigation only; no biological claim",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint source de-duplication intake checklist freshness")
    lint.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic de-duplication checklist fixtures")
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
            if not (
                lowered.startswith("| order ")
                or lowered.startswith("| state ")
                or lowered.startswith("| action ")
            ):
                count += 1
    return count


def lint_template(template: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    text = template.read_text(errors="ignore") if template.exists() else ""
    rows: list[dict[str, object]] = []
    add(rows, "template_exists", "PASS" if template.exists() else "FAIL", str(template))
    sections = h2_sections(text)
    for section in REQUIRED_SECTIONS:
        add(rows, f"section_present.{section}", "PASS" if section in sections else "FAIL", "required de-duplication checklist section")
    for link in REQUIRED_LINKS:
        add(rows, f"link_present.{link}", "PASS" if link in text else "FAIL", "required linked control")
    for check, phrase in REQUIRED_PHRASES.items():
        add(rows, f"phrase_present.{check}", "PASS" if normalized_contains(text, phrase) else "FAIL", "required boundary phrase")
    n_checks = count_table_rows_after_section(text, "De-Duplication Checks")
    n_states = count_table_rows_after_section(text, "Duplicate States")
    n_actions = count_table_rows_after_section(text, "Safe Merge Actions")
    add(rows, "table_count.deduplication_checks", "PASS" if n_checks == 9 else "FAIL", f"observed={n_checks} expected=9")
    add(rows, "table_count.duplicate_states", "PASS" if n_states == 5 else "FAIL", f"observed={n_states} expected=5")
    add(rows, "table_count.safe_merge_actions", "PASS" if n_actions == 5 else "FAIL", f"observed={n_actions} expected=5")
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
    write_tsv(outdir / "source_deduplication_intake_checklist_freshness_lint.tsv", rows, ["check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 source de-duplication intake checklist freshness lint; template/navigation only; no biological claim",
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "source_deduplication_intake_checklist_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    template = outdir / "synthetic_dedup_template.md"
    summary = outdir / "synthetic_summary.json"
    template.write_text(
        "\n".join(
            [
                "# Synthetic Source De-Duplication",
                "",
                "Status: template/navigation only.",
                "",
                "## De-Duplication Checks",
                "",
                "| order | check | safe handling |",
                "|---:|---|---|",
                "| 1 | one | note |",
                "",
                "## Boundary",
                "",
                "This fixture deliberately omits required links and counts.",
            ]
        )
        + "\n"
    )
    summary.write_text(json.dumps({"markdown": "stale", "n_deduplication_checks": 1, "n_duplicate_states": 0, "overall_status": "FAIL"}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_template(template, summary, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "source_deduplication_intake_checklist_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "missing_section_fails": any(row["check"] == "section_present.Required Controls" and row["status"] == "FAIL" for row in rows),
        "missing_link_fails": any(row["check"].startswith("link_present.") and row["status"] == "FAIL" for row in rows),
        "bad_deduplication_count_fails": any(row["check"] == "table_count.deduplication_checks" and row["status"] == "FAIL" for row in rows),
        "bad_state_count_fails": any(row["check"] == "table_count.duplicate_states" and row["status"] == "FAIL" for row in rows),
        "bad_action_count_fails": any(row["check"] == "table_count.safe_merge_actions" and row["status"] == "FAIL" for row in rows),
        "bad_summary_fails": any(row["check"] == "summary_matches.n_deduplication_checks" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_source_deduplication_intake_checklist_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 source de-duplication intake checklist freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_source_deduplication_intake_checklist_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
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
