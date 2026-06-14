#!/usr/bin/env python3
"""Check that the V48 AI Core tooling-health handoff card is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CARD = ROOT / "knowledge_external/catalogs/indexes/V48_AI_CORE_TOOLING_HEALTH.md"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/v48_ai_core_tooling_health_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_ai_core_tooling_health_freshness_linter"

EXPECTED_COMMANDS = {
    "claude": "python3 scripts/sap_ai_core_client.py smoke --model claude --timeout 45",
    "gemini": "python3 scripts/sap_ai_core_client.py smoke --model gemini --timeout 45",
    "rpt": "python3 scripts/sap_ai_core_client.py rpt-smoke --timeout 120",
}

EXPECTED_CARD_PHRASES = {
    "claude_status": "| Claude via SAP AI Core Orchestration |",
    "gemini_status": "| Gemini via SAP AI Core |",
    "rpt_status": "| SAP RPT tabular route |",
    "rpt_pass": "`PASS`",
    "rpt_predict_route": "rpt-smoke",
    "rpt_model_detail": "sap-rpt-1-large 1 d61aae51af327bbc",
    "proposal_only": "model output is never evidence",
    "no_secret_storage": "no key or bearer token stored here",
}

EXPECTED_SUMMARY = {
    "markdown": "knowledge_external/catalogs/indexes/V48_AI_CORE_TOOLING_HEALTH.md",
    "claude_status": "PASS",
    "gemini_status": "PASS",
    "rpt_status": "PASS",
    "rpt_status_detail": "sap-rpt-1-large 1 d61aae51af327bbc; status message ok",
    "model_spend": "not_exposed_by_client",
    "purpose": "V48 AI Core tooling-health handoff; no biological claim",
    "overall_status": "PASS",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint AI Core tooling-health handoff freshness")
    lint.add_argument("--card", type=Path, default=DEFAULT_CARD)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic AI Core tooling-health freshness fixtures")
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


def lint_health(card: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    text = card.read_text(errors="ignore") if card.exists() else ""
    rows: list[dict[str, object]] = []
    add(rows, "card_exists", "PASS" if card.exists() else "FAIL", str(card))
    for route, command in EXPECTED_COMMANDS.items():
        add(rows, f"command_present.{route}", "PASS" if command in text else "FAIL", "expected smoke command")
    for check, phrase in EXPECTED_CARD_PHRASES.items():
        add(rows, f"phrase_present.{check}", "PASS" if phrase in text else "FAIL", "expected tooling-health phrase")
    summary = read_json(summary_path)
    for field, expected_value in EXPECTED_SUMMARY.items():
        add(
            rows,
            f"summary_matches.{field}",
            "PASS" if summary.get(field, "") == expected_value else "FAIL",
            f"expected={expected_value} observed={summary.get(field, '')}",
        )
    add(rows, "summary_has_checked_utc", "PASS" if str(summary.get("checked_utc", "")).endswith("Z") else "FAIL", "checked_utc must be an ISO-like UTC timestamp")
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "ai_core_tooling_health_freshness_lint.tsv", rows, ["check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 AI Core tooling-health freshness lint; tooling/navigation only; no biological claim",
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "ai_core_tooling_health_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    card = outdir / "synthetic_ai_core_health.md"
    summary = outdir / "synthetic_summary.json"
    card.write_text(
        "\n".join(
            [
                "# Synthetic AI Core Health",
                "",
                "| Claude via SAP AI Core Orchestration | stale command | `PASS` | OK | proposal only |",
                "| Gemini via SAP AI Core | stale command | `PASS` | OK | proposal only |",
                "| SAP RPT tabular route | stale command | `UNAVAILABLE` | wrong | wrong |",
                "",
                "no key or bearer token stored here",
            ]
        )
        + "\n"
    )
    summary.write_text(json.dumps({"checked_utc": "not_utc", "claude_status": "PASS", "gemini_status": "FAIL", "rpt_status": "UNAVAILABLE"}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_health(card, summary, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "ai_core_tooling_health_freshness_lint.tsv").open(), delimiter="\t"))
    checks = {
        "missing_command_fails": any(row["check"] == "command_present.claude" and row["status"] == "FAIL" for row in rows),
        "missing_rpt_predict_route_fails": any(row["check"] == "phrase_present.rpt_predict_route" and row["status"] == "FAIL" for row in rows),
        "bad_summary_status_fails": any(row["check"] == "summary_matches.rpt_status" and row["status"] == "FAIL" for row in rows),
        "bad_checked_utc_fails": any(row["check"] == "summary_has_checked_utc" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_ai_core_tooling_health_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 AI Core tooling-health freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_ai_core_tooling_health_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_health(args.card, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
