#!/usr/bin/env python3
"""Check that the V48 model-lens usage boundary card is fresh and strict."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CARD = ROOT / "knowledge_external/catalogs/indexes/V48_MODEL_LENS_USAGE_BOUNDARY.md"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/v48_model_lens_usage_boundary_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_model_lens_usage_boundary_freshness_linter"

REQUIRED_SECTIONS = [
    "Rule",
    "Allowed Uses",
    "Forbidden Shortcuts",
    "Current Tooling Status",
    "Required Verification",
    "Boundary",
]

REQUIRED_LENSES = ["Claude", "Gemini", "RPT"]

REQUIRED_PHRASES = {
    "proposal_lenses_only": "proposal lenses only",
    "not_establish_biology": "may not establish a biological claim",
    "no_grounded_override": "may not validate, weaken, override, or alter a grounded project finding",
    "external_unverifiable_context": "external-unverifiable context",
    "no_generic_rpt_smoke": "do not use generic `smoke --model rpt`",
    "no_model_output_evidence": "does not authorize model output as evidence",
    "not_project_finding": "not a project finding",
}

REQUIRED_COMMANDS = [
    "python3 scripts/v47_provenance_gate.py audit --fail-on-error",
    "python3 scripts/v48_governance_preflight.py",
]

REQUIRED_LINKS = [
    "knowledge_external/catalogs/indexes/V48_AI_CORE_TOOLING_HEALTH.md",
]

EXPECTED_SUMMARY = {
    "markdown": "knowledge_external/catalogs/indexes/V48_MODEL_LENS_USAGE_BOUNDARY.md",
    "n_forbidden_shortcuts": 5,
    "n_lenses": 3,
    "overall_status": "PASS",
    "purpose": "V48 model-lens usage boundary; governance/navigation only; no biological claim",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint model-lens usage boundary freshness")
    lint.add_argument("--card", type=Path, default=DEFAULT_CARD)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic model-lens boundary freshness fixtures")
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
            if not stripped.lower().startswith("| lens ") and not stripped.lower().startswith("| shortcut "):
                count += 1
    return count


def normalized_contains(text: str, phrase: str) -> bool:
    return " ".join(phrase.split()) in " ".join(text.split())


def lint_boundary(card: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    text = card.read_text(errors="ignore") if card.exists() else ""
    rows: list[dict[str, object]] = []
    add(rows, "card_exists", "PASS" if card.exists() else "FAIL", str(card))
    sections = h2_sections(text)
    for section in REQUIRED_SECTIONS:
        add(rows, f"section_present.{section}", "PASS" if section in sections else "FAIL", "required model-lens boundary section")
    for lens in REQUIRED_LENSES:
        add(rows, f"lens_present.{lens}", "PASS" if f"| {lens} |" in text else "FAIL", "required lens row")
    for check, phrase in REQUIRED_PHRASES.items():
        add(rows, f"phrase_present.{check}", "PASS" if normalized_contains(text, phrase) else "FAIL", "required boundary phrase")
    for command in REQUIRED_COMMANDS:
        add(rows, f"command_present.{command}", "PASS" if command in text else "FAIL", "required verification command")
    for link in REQUIRED_LINKS:
        add(rows, f"link_present.{link}", "PASS" if link in text else "FAIL", "required navigation target")
    n_lenses = count_table_rows_after_section(text, "Allowed Uses")
    n_forbidden = count_table_rows_after_section(text, "Forbidden Shortcuts")
    add(rows, "table_count.allowed_uses", "PASS" if n_lenses == 3 else "FAIL", f"observed={n_lenses} expected=3")
    add(rows, "table_count.forbidden_shortcuts", "PASS" if n_forbidden == 5 else "FAIL", f"observed={n_forbidden} expected=5")
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
    write_tsv(outdir / "model_lens_usage_boundary_freshness_lint.tsv", rows, ["check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 model-lens usage boundary freshness lint; navigation only; no biological claim",
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "model_lens_usage_boundary_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    card = outdir / "synthetic_model_lens_boundary.md"
    summary = outdir / "synthetic_summary.json"
    card.write_text(
        "\n".join(
            [
                "# Synthetic Model Lens Boundary",
                "",
                "Status: navigation only.",
                "",
                "## Rule",
                "",
                "Models can suggest work.",
                "",
                "## Allowed Uses",
                "",
                "| lens | allowed use | required follow-up |",
                "|---|---|---|",
                "| Claude | Suggest checks. | Run a project analysis. |",
                "",
                "## Forbidden Shortcuts",
                "",
                "| shortcut | why forbidden |",
                "|---|---|",
                "| Treating agreement as proof. | It is not proof. |",
                "",
                "## Boundary",
                "",
                "This fixture deliberately omits required commands and route-specific RPT language.",
            ]
        )
        + "\n"
    )
    summary.write_text(json.dumps({"markdown": "stale", "n_forbidden_shortcuts": 1, "n_lenses": 1, "overall_status": "FAIL"}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_boundary(card, summary, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "model_lens_usage_boundary_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "missing_section_fails": any(row["check"] == "section_present.Current Tooling Status" and row["status"] == "FAIL" for row in rows),
        "missing_lens_fails": any(row["check"] == "lens_present.RPT" and row["status"] == "FAIL" for row in rows),
        "missing_rpt_route_phrase_fails": any(row["check"] == "phrase_present.no_generic_rpt_smoke" and row["status"] == "FAIL" for row in rows),
        "bad_forbidden_count_fails": any(row["check"] == "table_count.forbidden_shortcuts" and row["status"] == "FAIL" for row in rows),
        "bad_summary_fails": any(row["check"] == "summary_matches.n_lenses" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_model_lens_usage_boundary_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 model-lens usage boundary freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_model_lens_usage_boundary_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_boundary(args.card, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
