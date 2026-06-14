#!/usr/bin/env python3
"""Prevent stale or false RPT availability claims in V48 handoff/navigation docs."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGETS = [
    ROOT / "meta/V48_QUEUE.md",
    ROOT / "knowledge_external/INDEX.md",
    ROOT / "knowledge_external/catalogs/indexes/V48_AI_CORE_TOOLING_HEALTH.md",
    ROOT / "knowledge_external/catalogs/indexes/V48_GOVERNANCE_NAVIGATION.md",
    ROOT / "knowledge_external/catalogs/indexes/V48_PREFLIGHT_SUMMARY_CARD.md",
]
DEFAULT_OUTDIR = ROOT / "analysis/v48_rpt_availability_claim_linter"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint RPT availability claims")
    lint.add_argument("--target", type=Path, action="append", default=None, help="File to scan; repeatable")
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic RPT availability claim fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def is_rpt_line(line: str) -> bool:
    lowered = line.lower()
    return "rpt" in lowered or "sap-rpt" in lowered


def allowed_negative_context(line: str) -> bool:
    lowered = line.lower()
    return any(token in lowered for token in ["false pass", "prevent", "synthetic fixture", "stale command"])


def corrected_route_present(line: str) -> bool:
    lowered = line.lower()
    return "rpt-smoke" in lowered or "rpt-predict" in lowered or "sap-rpt-1-large" in lowered or "route-specific" in lowered


def issue_for_line(line: str) -> str:
    lowered = line.lower()
    if not is_rpt_line(line):
        return ""
    if allowed_negative_context(line):
        return ""
    if "smoke-passed" in lowered and "rpt-smoke" not in lowered:
        return "generic_smoke_pass_claim"
    if any(token in lowered for token in ["unavailable", "unimplemented", "no implemented request schema"]):
        if "generic" in lowered and "unsupported" in lowered:
            return ""
        return "stale_unavailable_claim"
    if re.search(r"\bpass\b", lowered) and not corrected_route_present(line):
        return "rpt_pass_without_correct_route"
    return ""


def lint_targets(targets: list[Path], outdir: Path, fail_on_error: bool) -> int:
    rows: list[dict[str, object]] = []
    for target in targets:
        text = target.read_text(errors="ignore") if target.exists() else ""
        rows.append(
            {
                "path": rel(target),
                "line": "",
                "check": "target_exists",
                "status": "PASS" if target.exists() else "FAIL",
                "detail": str(target),
            }
        )
        for line_no, line in enumerate(text.splitlines(), start=1):
            issue = issue_for_line(line)
            if issue:
                rows.append(
                    {
                        "path": rel(target),
                        "line": line_no,
                        "check": issue,
                        "status": "FAIL",
                        "detail": line.strip()[:200],
                    }
                )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "rpt_availability_claim_lint.tsv", rows, ["path", "line", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 RPT availability claim lint; tooling/navigation only; no biological claim",
        "n_targets": len(targets),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "rpt_availability_claim_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    bad = outdir / "synthetic_bad.md"
    good = outdir / "synthetic_good.md"
    bad.write_text(
        "\n".join(
            [
                "SAP AI Core smoke-passed for Claude, Gemini, and RPT.",
                "RPT smoke: UNAVAILABLE due to No implemented request schema for model: sap-rpt-1-large.",
                "RPT PASS.",
            ]
        )
        + "\n"
    )
    good.write_text(
        "\n".join(
            [
                "RPT PASS via rpt-smoke with sap-rpt-1-large.",
                "Do not use generic smoke --model rpt; that route is unsupported.",
                "Prevent RPT status from drifting back to a false PASS.",
            ]
        )
        + "\n"
    )
    lint_out = outdir / "synthetic_lint"
    lint_targets([bad, good], lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "rpt_availability_claim_lint.tsv").open(), delimiter="\t"))
    checks = {
        "generic_smoke_pass_fails": any(row["check"] == "generic_smoke_pass_claim" and row["status"] == "FAIL" for row in rows),
        "stale_unavailable_fails": any(row["check"] == "stale_unavailable_claim" and row["status"] == "FAIL" for row in rows),
        "route_missing_pass_fails": any(row["check"] == "rpt_pass_without_correct_route" and row["status"] == "FAIL" for row in rows),
        "corrected_route_passes": not any(row["path"].endswith("synthetic_good.md") and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_rpt_availability_claim_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 RPT availability claim synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_rpt_availability_claim_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_targets(args.target or DEFAULT_TARGETS, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
