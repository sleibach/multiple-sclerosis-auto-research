#!/usr/bin/env python3
"""Prevent model/RPT output from being framed as evidence in V48 handoff text."""

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
    ROOT / "knowledge_external/EXTERNAL_LAYER_READER_BRIEF_V48.md",
    ROOT / "knowledge_external/catalogs/indexes/V48_MODEL_LENS_USAGE_BOUNDARY.md",
    ROOT / "knowledge_external/catalogs/indexes/V48_AI_CORE_TOOLING_HEALTH.md",
    ROOT / "knowledge_external/catalogs/indexes/V48_GOVERNANCE_NAVIGATION.md",
    ROOT / "knowledge_external/catalogs/indexes/V48_PREFLIGHT_SUMMARY_CARD.md",
    ROOT / "knowledge_external/catalogs/indexes/V48_EXTERNAL_GOVERNANCE_HANDOFF.md",
]
DEFAULT_OUTDIR = ROOT / "analysis/v48_model_evidence_claim_linter"

MODEL_TOKEN = re.compile(r"\b(model|models|claude|gemini|rpt|tabular predictor|sub-model)\b", re.IGNORECASE)
UNSAFE_EVIDENCE = re.compile(
    r"\b(is|are|as|counts as|constitutes|serves as|provides|providing|becomes|become)\b.{0,80}\bevidence\b",
    re.IGNORECASE,
)
UNSAFE_VERBS = re.compile(
    r"\b(validate|validates|validated|proves|prove|proven|establish|establishes|established|confirms|confirmed)\b",
    re.IGNORECASE,
)

SAFE_FRAGMENTS = [
    "not evidence",
    "never evidence",
    "not biological evidence",
    "not project-grounded evidence",
    "does not authorize model output as evidence",
    "no model output as evidence",
    "no model output is evidence",
    "no model/rpt output is evidence",
    "model output is never evidence",
    "without treating model output as evidence",
    "it is not biological evidence",
    "it is not evidence",
    "may not establish",
    "may not validate",
    "not validate",
    "does not validate",
    "proposal lens",
    "proposal lenses",
    "proposal-only",
    "proposals unless separately grounded",
    "unless separately grounded",
    "treating model agreement as evidence",
    "using model confidence",
    "model-validates-claim wording",
    "not calibrated",
    "scanner",
    "linter",
    "prevent",
    "prevents",
    "forbidden",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint model-output-as-evidence wording")
    lint.add_argument("--target", type=Path, action="append", default=None, help="File to scan; repeatable")
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic wording fixtures")
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


def safe_context(line: str) -> bool:
    lowered = line.lower()
    return any(fragment in lowered for fragment in SAFE_FRAGMENTS)


def issue_for_line(line: str) -> str:
    if not MODEL_TOKEN.search(line):
        return ""
    if safe_context(line):
        return ""
    if UNSAFE_EVIDENCE.search(line):
        return "model_output_as_evidence_claim"
    if UNSAFE_VERBS.search(line) and re.search(r"\b(finding|claim|conclusion|rule|biology|truth|result)\b", line, re.IGNORECASE):
        return "model_output_validates_claim"
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
                        "detail": line.strip()[:220],
                    }
                )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "model_evidence_claim_lint.tsv", rows, ["path", "line", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 model-output evidence-claim lint; wording/navigation only; no biological claim",
        "n_targets": len(targets),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "model_evidence_claim_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
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
                "Claude output is evidence for the project conclusion.",
                "RPT validates the biological claim.",
                "Gemini confirms the rule result.",
            ]
        )
        + "\n"
    )
    good.write_text(
        "\n".join(
            [
                "Model output is never evidence.",
                "RPT is a proposal lens only unless separately grounded.",
                "This linter prevents model-output-as-evidence wording.",
            ]
        )
        + "\n"
    )
    lint_out = outdir / "synthetic_lint"
    lint_targets([bad, good], lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "model_evidence_claim_lint.tsv").open(), delimiter="\t"))
    checks = {
        "direct_evidence_claim_fails": any(row["check"] == "model_output_as_evidence_claim" and row["status"] == "FAIL" for row in rows),
        "validation_claim_fails": any(row["check"] == "model_output_validates_claim" and row["status"] == "FAIL" for row in rows),
        "safe_boundary_language_passes": not any(row["path"].endswith("synthetic_good.md") and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_model_evidence_claim_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 model evidence-claim synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_model_evidence_claim_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
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
