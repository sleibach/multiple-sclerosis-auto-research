#!/usr/bin/env python3
"""Lint V47 relationship-to-project-findings tags.

The general provenance gate verifies that relationship tags come from the
allowed vocabulary. This stricter linter documents and enforces the intended
semantics: ``supports`` and ``contradicts`` are not free-floating labels. They
must point to a specific grounded project finding reference before a record can
use them.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v47_relationship_vocabulary_linter"
EXTERNAL_ROOT = "knowledge_external"
ALLOWED_RELATIONSHIPS = {"supports", "contradicts", "orthogonal", "untested"}
LINK_REQUIRED = {"supports", "contradicts"}
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint real external relationship tags")
    lint.add_argument("--root", type=Path, default=ROOT)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic relationship-vocabulary fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def record_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for directory in [root / EXTERNAL_ROOT / "records", root / EXTERNAL_ROOT / "catalogs/resources"]:
        if directory.exists():
            paths.extend(path for path in directory.rglob("*.json") if not path.name.endswith(".schema.json"))
    return sorted(paths)


def has_project_finding_reference(data: dict[str, Any]) -> bool:
    reference = data.get("project_finding_reference")
    if not isinstance(reference, dict):
        return False
    return bool(str(reference.get("finding_id", "")).strip() and str(reference.get("artifact", "")).strip())


def add(rows: list[dict[str, object]], path: str, record_id: str, relationship: str, check: str, ok: bool, detail: str = "") -> None:
    rows.append(
        {
            "path": path,
            "record_id": record_id,
            "relationship_to_project_findings": relationship,
            "check": check,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
        }
    )


def lint_record(root: Path, path: Path) -> list[dict[str, object]]:
    rel_path = rel(root, path)
    rows: list[dict[str, object]] = []
    try:
        data = json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001 - report parser failure as lint row.
        return [{"path": rel_path, "record_id": "", "relationship_to_project_findings": "", "check": "json_parse", "status": "FAIL", "detail": str(exc)}]
    if not isinstance(data, dict):
        return [{"path": rel_path, "record_id": "", "relationship_to_project_findings": "", "check": "json_object", "status": "FAIL", "detail": "record is not an object"}]
    record_id = str(data.get("record_id", ""))
    relationship = str(data.get("relationship_to_project_findings", ""))
    add(rows, rel_path, record_id, relationship, "relationship_allowed", relationship in ALLOWED_RELATIONSHIPS, relationship)
    add(rows, rel_path, record_id, relationship, "not_project_grounded_marker", data.get("not_project_grounded_marker") == NOT_GROUNDED, str(data.get("not_project_grounded_marker", "")))
    if relationship in LINK_REQUIRED:
        add(
            rows,
            rel_path,
            record_id,
            relationship,
            "supports_or_contradicts_has_grounded_reference",
            has_project_finding_reference(data),
            "supports/contradicts require project_finding_reference.finding_id and .artifact",
        )
    else:
        add(
            rows,
            rel_path,
            record_id,
            relationship,
            "non_link_relationship_does_not_require_reference",
            True,
            "orthogonal/untested do not create convergence or contradiction",
        )
    return rows


def lint_root(root: Path, outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else root / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    paths = record_paths(root)
    for path in paths:
        rows.extend(lint_record(root, path))
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    write_tsv(outdir / "relationship_vocabulary_lint.tsv", rows, ["path", "record_id", "relationship_to_project_findings", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V47 relationship vocabulary lint; no biological claim",
        "n_records": len(paths),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": rel(root, outdir / "relationship_vocabulary_lint.tsv") if root == ROOT else str(outdir / "relationship_vocabulary_lint.tsv"),
    }
    (outdir / "relationship_vocabulary_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def write_record(path: Path, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(kwargs, indent=2, sort_keys=True) + "\n")


def build_synthetic_root(outdir: Path) -> Path:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    records = root / EXTERNAL_ROOT / "records"
    records.mkdir(parents=True, exist_ok=True)
    base = {
        "claim": "Synthetic relationship vocabulary claim.",
        "epistemic_class": "external-unverifiable",
        "source": {"label": "Synthetic source", "url": "https://example.invalid/relationship"},
        "date_accessed": "2026-06-13",
        "not_project_grounded_marker": NOT_GROUNDED,
        "why_unverifiable": "Synthetic fixture.",
        "future_grounding_route": "Synthetic route.",
    }
    write_record(records / "orthogonal_ok.json", **base, record_id="SYNTH_ORTHOGONAL_OK", relationship_to_project_findings="orthogonal")
    write_record(
        records / "supports_ok.json",
        **base,
        record_id="SYNTH_SUPPORTS_OK",
        relationship_to_project_findings="supports",
        project_finding_reference={"finding_id": "SYNTH_GROUNDED_FINDING", "artifact": "docs/reports/FINDINGS_REPORT_V37.md"},
    )
    write_record(records / "supports_bad.json", **base, record_id="SYNTH_SUPPORTS_BAD", relationship_to_project_findings="supports")
    write_record(records / "bad_value.json", **base, record_id="SYNTH_BAD_VALUE", relationship_to_project_findings="confirms")
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root = build_synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_root(root, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "relationship_vocabulary_lint.tsv").open(), delimiter="\t"))
    checks = {
        "orthogonal_ok_passes": not any(row["record_id"] == "SYNTH_ORTHOGONAL_OK" and row["status"] == "FAIL" for row in rows),
        "supports_with_reference_passes": not any(row["record_id"] == "SYNTH_SUPPORTS_OK" and row["status"] == "FAIL" for row in rows),
        "supports_without_reference_fails": any(row["record_id"] == "SYNTH_SUPPORTS_BAD" and row["check"] == "supports_or_contradicts_has_grounded_reference" and row["status"] == "FAIL" for row in rows),
        "bad_relationship_value_fails": any(row["record_id"] == "SYNTH_BAD_VALUE" and row["check"] == "relationship_allowed" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_relationship_vocabulary_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V47 relationship vocabulary linter synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_relationship_vocabulary_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_root(args.root.resolve(), args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
