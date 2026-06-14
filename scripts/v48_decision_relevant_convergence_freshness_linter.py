#!/usr/bin/env python3
"""Check that the V48 decision-relevant convergence shortlist is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_SHORTLIST = ROOT / "knowledge_external/synthesis/decision_relevant_convergences_v48.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/decision_relevant_convergences_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_decision_relevant_convergence_freshness_linter"
COMPARE_FIELDS = [
    "grounded_finding_id",
    "grounded_evidence_grade",
    "grounded_artifact",
    "external_record_id",
    "epistemic_class",
    "external_source",
    "relationship_class",
    "synthesis_status",
    "interpretation",
    "future_grounding_action",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint decision-relevant convergence shortlist freshness")
    lint.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    lint.add_argument("--shortlist", type=Path, default=DEFAULT_SHORTLIST)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic freshness fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


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


def shortlist_class(row: dict[str, str]) -> str:
    if row.get("relationship_class") == "converges":
        return "corroborated_grounded_context"
    if row.get("relationship_class") == "contradicts":
        return "external_tension_to_ground"
    return ""


def row_key(row: dict[str, str]) -> str:
    return f"{row.get('grounded_finding_id', '')}||{row.get('external_record_id', '')}"


def add(rows: list[dict[str, object]], key: str, check: str, status: str, detail: str) -> None:
    rows.append({"row_key": key, "check": check, "status": status, "detail": detail})


def lint_shortlist(matrix: Path, shortlist: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    matrix_rows = [row for row in read_tsv(matrix) if shortlist_class(row)]
    shortlist_rows = read_tsv(shortlist)
    expected = {row_key(row): row for row in matrix_rows}
    observed = {row_key(row): row for row in shortlist_rows}
    rows: list[dict[str, object]] = []
    for key, matrix_row in sorted(expected.items()):
        short_row = observed.get(key)
        add(rows, key, "present_in_shortlist", "PASS" if short_row else "FAIL", str(shortlist))
        if not short_row:
            continue
        add(
            rows,
            key,
            "shortlist_class_matches_relationship",
            "PASS" if short_row.get("shortlist_class", "") == shortlist_class(matrix_row) else "FAIL",
            f"expected={shortlist_class(matrix_row)} observed={short_row.get('shortlist_class', '')}",
        )
        for field in COMPARE_FIELDS:
            add(
                rows,
                key,
                f"field_matches.{field}",
                "PASS" if short_row.get(field, "") == matrix_row.get(field, "") else "FAIL",
                f"expected={matrix_row.get(field, '')} observed={short_row.get(field, '')}",
            )
    for key in sorted(set(observed) - set(expected)):
        add(rows, key, "no_extra_shortlist_row", "FAIL", "shortlist row is not a converges/contradicts matrix row")
    summary = read_json(summary_path)
    add(
        rows,
        "summary",
        "summary_shortlist_count_matches_rows",
        "PASS" if int(summary.get("n_shortlist_rows", -1)) == len(shortlist_rows) else "FAIL",
        f"summary={summary.get('n_shortlist_rows', '')} rows={len(shortlist_rows)}",
    )
    add(
        rows,
        "summary",
        "summary_matrix_count_matches_current_matrix",
        "PASS" if int(summary.get("n_matrix_rows", -1)) == len(read_tsv(matrix)) else "FAIL",
        f"summary={summary.get('n_matrix_rows', '')} matrix={len(read_tsv(matrix))}",
    )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "decision_relevant_convergence_freshness_lint.tsv", rows, ["row_key", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 decision-relevant convergence shortlist freshness lint; synthesis/navigation only; no biological claim",
        "n_expected_shortlist_rows": len(expected),
        "n_shortlist_rows": len(shortlist_rows),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "decision_relevant_convergence_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    matrix = outdir / "synthetic_matrix.tsv"
    shortlist = outdir / "synthetic_shortlist.tsv"
    summary = outdir / "synthetic_summary.json"
    matrix_fields = [*COMPARE_FIELDS]
    short_fields = ["shortlist_class", *COMPARE_FIELDS, "evidence_boundary"]
    base = {
        "grounded_finding_id": "A",
        "grounded_evidence_grade": "supported",
        "grounded_artifact": "docs/example.md",
        "external_record_id": "E1",
        "epistemic_class": "external-unverifiable",
        "external_source": "https://example.org",
        "relationship_class": "converges",
        "synthesis_status": "CORROBORATION_FROM_INDEPENDENT_SOURCE",
        "interpretation": "synthetic",
        "future_grounding_action": "none",
    }
    missing = {**base, "grounded_finding_id": "B", "external_record_id": "E2"}
    write_tsv(matrix, [base, missing], matrix_fields)
    stale = {**base, "shortlist_class": "external_tension_to_ground", "interpretation": "stale", "evidence_boundary": "synthetic"}
    extra = {**base, "grounded_finding_id": "EXTRA", "external_record_id": "E3", "shortlist_class": "corroborated_grounded_context", "evidence_boundary": "synthetic"}
    write_tsv(shortlist, [stale, extra], short_fields)
    summary.write_text(json.dumps({"n_shortlist_rows": 99, "n_matrix_rows": 99}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_shortlist(matrix, shortlist, summary, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "decision_relevant_convergence_freshness_lint.tsv")
    checks = {
        "missing_row_fails": any(row["row_key"] == "B||E2" and row["check"] == "present_in_shortlist" and row["status"] == "FAIL" for row in rows),
        "stale_class_fails": any(row["row_key"] == "A||E1" and row["check"] == "shortlist_class_matches_relationship" and row["status"] == "FAIL" for row in rows),
        "stale_field_fails": any(row["row_key"] == "A||E1" and row["check"] == "field_matches.interpretation" and row["status"] == "FAIL" for row in rows),
        "extra_row_fails": any(row["row_key"] == "EXTRA||E3" and row["check"] == "no_extra_shortlist_row" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["row_key"] == "summary" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_decision_relevant_convergence_freshness_checks.tsv", check_rows, ["check", "status"])
    synth_summary = {
        "synthetic": True,
        "purpose": "V48 decision-relevant convergence freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_decision_relevant_convergence_freshness_summary.json").write_text(json.dumps(synth_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synth_summary, indent=2, sort_keys=True))
    return 0 if synth_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_shortlist(args.matrix, args.shortlist, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
