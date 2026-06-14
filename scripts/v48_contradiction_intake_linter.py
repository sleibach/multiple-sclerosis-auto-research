#!/usr/bin/env python3
"""Lint contradiction-intake records for strict future-grounding provenance.

An external contradiction is a tension flag. It never overrides a grounded
project finding unless a later rerunnable project analysis grounds it.
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
DEFAULT_OUTDIR = ROOT / "analysis/v48_contradiction_intake_linter"
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"
ALLOWED_STATUS = {
    "queued_for_future_grounding",
    "blocked_needs_data",
    "blocked_needs_access",
    "blocked_needs_human_decision",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint contradiction-intake records")
    lint.add_argument("--root", type=Path, default=ROOT)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic contradiction-intake fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def record_paths(root: Path) -> list[Path]:
    base = root / EXTERNAL_ROOT / "records"
    if not base.exists():
        return []
    return sorted(path for path in base.rglob("*.json") if not path.name.endswith(".schema.json"))


def has_source_locator(source: Any) -> bool:
    if not isinstance(source, dict):
        return False
    return any(str(source.get(field, "")).strip() for field in ["url", "doi", "pmid", "citation"])


def contradiction_records(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    records: list[tuple[Path, dict[str, Any]]] = []
    for path in record_paths(root):
        data = json.loads(path.read_text())
        if isinstance(data, dict) and data.get("relationship_to_project_findings") == "contradicts":
            records.append((path, data))
    return records


def add(rows: list[dict[str, object]], root: Path, path: Path, data: dict[str, Any], check: str, status: str, detail: str) -> None:
    rows.append(
        {
            "path": rel(root, path),
            "record_id": str(data.get("record_id", "")),
            "check": check,
            "status": status,
            "detail": detail,
        }
    )


def check_record(root: Path, path: Path, data: dict[str, Any]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    reference = data.get("project_finding_reference")
    has_reference = isinstance(reference, dict) and bool(str(reference.get("finding_id", "")).strip()) and bool(str(reference.get("artifact", "")).strip())
    checks = {
        "epistemic_class_external_verifiable": data.get("epistemic_class") == "external-verifiable",
        "source_locator_present": has_source_locator(data.get("source")),
        "not_project_grounded_marker": data.get("not_project_grounded_marker") == NOT_GROUNDED,
        "project_finding_reference_present": has_reference,
        "relationship_note_present": bool(str(data.get("relationship_note", "")).strip()),
        "future_grounding_route_present": bool(str(data.get("future_grounding_route", "")).strip()),
        "grounding_data_needed_present": bool(str(data.get("grounding_data_needed", "")).strip()),
        "grounding_status_valid": data.get("grounding_status") in ALLOWED_STATUS,
    }
    for check, ok in checks.items():
        add(rows, root, path, data, check, "PASS" if ok else "FAIL", "external contradiction must remain a queued future-grounding flag")
    return rows


def lint_root(root: Path, outdir: Path, fail_on_error: bool) -> int:
    root = root.resolve()
    outdir = outdir if outdir.is_absolute() else root / outdir
    rows: list[dict[str, object]] = []
    records = contradiction_records(root)
    for path, data in records:
        rows.extend(check_record(root, path, data))
    if not rows:
        rows.append({"path": "knowledge_external/records", "record_id": "", "check": "no_contradiction_records_present", "status": "PASS", "detail": "No live contradiction-intake records."})
    n_fail = sum(1 for row in rows if row["status"] == "FAIL")
    write_tsv(outdir / "contradiction_intake_lint.tsv", rows, ["path", "record_id", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 contradiction-intake lint; queueing/provenance only; no claim validation",
        "n_contradiction_records": len(records),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": rel(root, outdir / "contradiction_intake_lint.tsv") if root == ROOT else str(outdir / "contradiction_intake_lint.tsv"),
    }
    (outdir / "contradiction_intake_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def write_record(path: Path, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(kwargs, indent=2, sort_keys=True) + "\n")


def synthetic_root(outdir: Path) -> Path:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    base = root / EXTERNAL_ROOT / "records"
    common = {
        "record_type": "external_claim",
        "claim": "Synthetic contradiction-intake claim.",
        "date_accessed": "2026-06-14",
        "relationship_to_project_findings": "contradicts",
        "source": {"label": "Synthetic", "url": "https://example.invalid"},
        "not_project_grounded_marker": NOT_GROUNDED,
        "relationship_note": "Synthetic contradiction flag.",
        "future_grounding_route": "Run a synthetic grounding check.",
        "grounding_data_needed": "Synthetic data.",
        "grounding_status": "queued_for_future_grounding",
        "project_finding_reference": {"finding_id": "Finding A", "artifact": "docs/reports/FINDINGS_REPORT_V37.md"},
    }
    write_record(base / "good.json", **common, record_id="SYNTH_CONTRADICTION_GOOD", epistemic_class="external-verifiable")
    write_record(base / "bad_class.json", **common, record_id="SYNTH_CONTRADICTION_BAD_CLASS", epistemic_class="external-unverifiable")
    write_record(base / "bad_missing_route.json", **{**common, "future_grounding_route": ""}, record_id="SYNTH_CONTRADICTION_BAD_ROUTE", epistemic_class="external-verifiable")
    write_record(base / "bad_missing_reference.json", **{k: v for k, v in common.items() if k != "project_finding_reference"}, record_id="SYNTH_CONTRADICTION_BAD_REFERENCE", epistemic_class="external-verifiable")
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root = synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_root(root, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "contradiction_intake_lint.tsv").open(), delimiter="\t"))
    checks = {
        "good_passes": any(row["record_id"] == "SYNTH_CONTRADICTION_GOOD" and row["status"] == "PASS" for row in rows),
        "bad_class_fails": any(row["record_id"] == "SYNTH_CONTRADICTION_BAD_CLASS" and row["check"] == "epistemic_class_external_verifiable" and row["status"] == "FAIL" for row in rows),
        "missing_route_fails": any(row["record_id"] == "SYNTH_CONTRADICTION_BAD_ROUTE" and row["check"] == "future_grounding_route_present" and row["status"] == "FAIL" for row in rows),
        "missing_reference_fails": any(row["record_id"] == "SYNTH_CONTRADICTION_BAD_REFERENCE" and row["check"] == "project_finding_reference_present" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_contradiction_intake_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 contradiction-intake synthetic fixture; no claim validation",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_contradiction_intake_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_root(args.root, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
