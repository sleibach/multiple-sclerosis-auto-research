#!/usr/bin/env python3
"""Ensure support/contradiction external records are covered in the V48 matrix.

External records tagged as supporting or contradicting project findings require
explicit representation in the convergence/contradiction synthesis. This linter
does not validate external claims; it prevents provenance-linked records from
quietly escaping the classed synthesis table.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = "knowledge_external"
DEFAULT_OUTDIR = ROOT / "analysis/v48_support_contradiction_coverage_linter"
MATRIX_PATH = Path("knowledge_external/synthesis/convergence_contradiction_v48.tsv")
REQUIRED_MATRIX_CLASS = {"supports": "converges", "contradicts": "contradicts"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint support/contradiction matrix coverage")
    lint.add_argument("--root", type=Path, default=ROOT)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--matrix", type=Path, default=MATRIX_PATH)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic coverage fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def record_paths(root: Path) -> list[Path]:
    base = root / EXTERNAL_ROOT / "records"
    if not base.exists():
        return []
    return sorted(path for path in base.rglob("*.json") if not path.name.endswith(".schema.json"))


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def support_records(root: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in record_paths(root):
        try:
            data = json.loads(path.read_text())
        except Exception:  # noqa: BLE001
            continue
        relationship = str(data.get("relationship_to_project_findings", ""))
        if relationship in REQUIRED_MATRIX_CLASS:
            records.append({"path": rel(root, path), **data})
    return records


def matrix_index(root: Path, matrix: Path) -> dict[tuple[str, str], list[dict[str, str]]]:
    path = matrix if matrix.is_absolute() else root / matrix
    index: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in read_tsv(path):
        record_id = row.get("external_record_id", "")
        relation = row.get("relationship_class", "")
        index.setdefault((record_id, relation), []).append(row)
    return index


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def add(rows: list[dict[str, object]], record: dict[str, object], check: str, status: str, detail: str) -> None:
    rows.append(
        {
            "path": str(record.get("path", "")),
            "record_id": str(record.get("record_id", "")),
            "relationship_to_project_findings": str(record.get("relationship_to_project_findings", "")),
            "check": check,
            "status": status,
            "detail": detail,
        }
    )


def lint_root(root: Path, outdir: Path, matrix: Path, fail_on_error: bool) -> int:
    root = root.resolve()
    outdir = outdir if outdir.is_absolute() else root / outdir
    records = support_records(root)
    index = matrix_index(root, matrix)
    rows: list[dict[str, object]] = []
    for record in records:
        relationship = str(record.get("relationship_to_project_findings", ""))
        expected_class = REQUIRED_MATRIX_CLASS[relationship]
        reference = record.get("project_finding_reference")
        has_reference = isinstance(reference, dict) and bool(str(reference.get("finding_id", "")).strip()) and bool(str(reference.get("artifact", "")).strip())
        add(rows, record, "project_finding_reference_present", "PASS" if has_reference else "FAIL", json.dumps(reference, sort_keys=True) if reference else "missing")
        matrix_rows = index.get((str(record.get("record_id", "")), expected_class), [])
        add(rows, record, "covered_by_v48_matrix_expected_relationship", "PASS" if matrix_rows else "FAIL", f"expected_relationship_class={expected_class}; rows={len(matrix_rows)}")
        if matrix_rows and has_reference:
            finding_id = str(reference.get("finding_id", ""))  # type: ignore[union-attr]
            matching_finding = any(row.get("grounded_finding_id") == finding_id for row in matrix_rows)
            add(rows, record, "matrix_row_matches_project_finding_id", "PASS" if matching_finding else "FAIL", finding_id)
    n_fail = sum(1 for row in rows if row["status"] == "FAIL")
    summary = {
        "synthetic": False,
        "purpose": "V48 support/contradiction convergence coverage lint; no biological claim",
        "n_support_or_contradiction_records": len(records),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": rel(root, outdir / "support_contradiction_coverage_lint.tsv") if root == ROOT else str(outdir / "support_contradiction_coverage_lint.tsv"),
    }
    write_tsv(outdir / "support_contradiction_coverage_lint.tsv", rows, ["path", "record_id", "relationship_to_project_findings", "check", "status", "detail"])
    (outdir / "support_contradiction_coverage_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def write_record(path: Path, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(kwargs, indent=2, sort_keys=True) + "\n")


def synthetic_root(outdir: Path) -> tuple[Path, Path]:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    base = root / EXTERNAL_ROOT / "records"
    synthesis = root / EXTERNAL_ROOT / "synthesis"
    synthesis.mkdir(parents=True, exist_ok=True)
    common = {
        "claim": "Synthetic support coverage claim.",
        "date_accessed": "2026-06-14",
        "epistemic_class": "external-unverifiable",
        "source": {"label": "Synthetic", "url": "https://example.invalid"},
        "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
        "record_type": "external_claim",
        "why_unverifiable": "Synthetic fixture.",
    }
    write_record(
        base / "good_support.json",
        **common,
        record_id="SYNTH_SUPPORT_GOOD",
        relationship_to_project_findings="supports",
        project_finding_reference={"finding_id": "Finding A", "artifact": "docs/reports/FINDINGS_REPORT_V37.md"},
    )
    write_record(
        base / "missing_matrix.json",
        **common,
        record_id="SYNTH_SUPPORT_MISSING_MATRIX",
        relationship_to_project_findings="supports",
        project_finding_reference={"finding_id": "Finding B", "artifact": "docs/reports/FINDINGS_REPORT_V37.md"},
    )
    write_record(
        base / "missing_reference.json",
        **common,
        record_id="SYNTH_CONTRADICTS_MISSING_REFERENCE",
        relationship_to_project_findings="contradicts",
    )
    matrix = synthesis / "convergence_contradiction_v48.tsv"
    with matrix.open("w", newline="") as handle:
        fields = ["grounded_finding_id", "external_record_id", "relationship_class"]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerow({"grounded_finding_id": "Finding A", "external_record_id": "SYNTH_SUPPORT_GOOD", "relationship_class": "converges"})
        writer.writerow({"grounded_finding_id": "Wrong finding", "external_record_id": "SYNTH_CONTRADICTS_MISSING_REFERENCE", "relationship_class": "contradicts"})
    return root, matrix.relative_to(root)


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root, matrix = synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_root(root, lint_out, matrix, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "support_contradiction_coverage_lint.tsv").open(), delimiter="\t"))
    checks = {
        "good_support_passes": any(row["record_id"] == "SYNTH_SUPPORT_GOOD" and row["check"] == "matrix_row_matches_project_finding_id" and row["status"] == "PASS" for row in rows),
        "missing_matrix_fails": any(row["record_id"] == "SYNTH_SUPPORT_MISSING_MATRIX" and row["check"] == "covered_by_v48_matrix_expected_relationship" and row["status"] == "FAIL" for row in rows),
        "missing_reference_fails": any(row["record_id"] == "SYNTH_CONTRADICTS_MISSING_REFERENCE" and row["check"] == "project_finding_reference_present" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_support_contradiction_coverage_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 support/contradiction coverage synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_support_contradiction_coverage_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_root(args.root, args.outdir, args.matrix, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
