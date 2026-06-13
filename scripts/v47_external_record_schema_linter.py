#!/usr/bin/env python3
"""Lint V47 external records using built-in schema rules.

This is a dependency-free guard for external records when jsonschema is not
available. It checks required fields, source provenance, epistemic class,
relationship tags, not-grounded markers, and class-specific explanation fields.
It does not validate external claims and does not make biological conclusions.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v47_external_record_schema_linter"
EXTERNAL_ROOT = "knowledge_external"
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"
CLASSES = {"external-verifiable", "external-unverifiable"}
RELATIONSHIPS = {"supports", "contradicts", "orthogonal", "untested"}
RESOURCE_ACCESS_TIERS = {"open", "registration", "application", "controlled", "mixed", "unknown"}
RESOURCE_REQUIRED = {
    "record_id",
    "record_type",
    "resource_name",
    "claim",
    "epistemic_class",
    "source",
    "date_accessed",
    "access_tier",
    "relationship_to_project_findings",
    "not_project_grounded_marker",
    "why_unverifiable",
    "future_grounding_route",
    "project_use",
}
GENERIC_REQUIRED = {
    "record_id",
    "claim",
    "epistemic_class",
    "source",
    "date_accessed",
    "relationship_to_project_findings",
    "not_project_grounded_marker",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint real external records")
    lint.add_argument("--root", type=Path, default=ROOT)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic pass/fail schema fixtures")
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


def source_present(source: Any) -> bool:
    if not isinstance(source, dict):
        return False
    label = str(source.get("label", "")).strip()
    locator = any(str(source.get(field, "")).strip() for field in ["url", "doi", "pmid", "citation"])
    return bool(label and locator)


def record_paths(root: Path) -> list[Path]:
    bases = [root / EXTERNAL_ROOT / "records", root / EXTERNAL_ROOT / "catalogs/resources"]
    paths: list[Path] = []
    for base in bases:
        if base.exists():
            paths.extend(path for path in base.rglob("*.json") if not path.name.endswith(".schema.json"))
    return sorted(paths)


def add_check(rows: list[dict[str, object]], path: str, record_id: str, check: str, ok: bool, detail: str = "") -> None:
    rows.append(
        {
            "path": path,
            "record_id": record_id,
            "check": check,
            "status": "PASS" if ok else "FAIL",
            "detail": detail or "-",
        }
    )


def lint_record(root: Path, path: Path) -> list[dict[str, object]]:
    rel_path = rel(root, path)
    rows: list[dict[str, object]] = []
    try:
        data = json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001 - report parser failure as lint row.
        return [{"path": rel_path, "record_id": "", "check": "json_parse", "status": "FAIL", "detail": str(exc)}]
    if not isinstance(data, dict):
        return [{"path": rel_path, "record_id": "", "check": "json_object", "status": "FAIL", "detail": "record is not an object"}]
    record_id = str(data.get("record_id", ""))
    record_type = str(data.get("record_type", "external_claim_record"))
    required = RESOURCE_REQUIRED if record_type == "external_resource_catalog" else GENERIC_REQUIRED
    for field in sorted(required):
        add_check(rows, rel_path, record_id, f"required_{field}", bool(str(data.get(field, "")).strip()), "")
    add_check(rows, rel_path, record_id, "epistemic_class_allowed", data.get("epistemic_class") in CLASSES, str(data.get("epistemic_class", "")))
    add_check(rows, rel_path, record_id, "relationship_allowed", data.get("relationship_to_project_findings") in RELATIONSHIPS, str(data.get("relationship_to_project_findings", "")))
    add_check(rows, rel_path, record_id, "source_present", source_present(data.get("source")), "")
    add_check(rows, rel_path, record_id, "not_grounded_marker", data.get("not_project_grounded_marker") == NOT_GROUNDED, str(data.get("not_project_grounded_marker", "")))
    if data.get("epistemic_class") == "external-unverifiable":
        add_check(rows, rel_path, record_id, "why_unverifiable_present", bool(str(data.get("why_unverifiable", "")).strip()), "")
    if data.get("epistemic_class") == "external-verifiable":
        add_check(rows, rel_path, record_id, "future_grounding_route_present", bool(str(data.get("future_grounding_route", "")).strip()), "")
    if record_type == "external_resource_catalog":
        add_check(rows, rel_path, record_id, "access_tier_allowed", data.get("access_tier") in RESOURCE_ACCESS_TIERS, str(data.get("access_tier", "")))
        add_check(rows, rel_path, record_id, "resource_record_type", data.get("record_type") == "external_resource_catalog", str(data.get("record_type", "")))
    return rows


def lint_root(root: Path, outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else root / outdir
    rows: list[dict[str, object]] = []
    paths = record_paths(root)
    for path in paths:
        rows.extend(lint_record(root, path))
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    write_tsv(outdir / "external_record_schema_lint.tsv", rows, ["path", "record_id", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V47 dependency-free external-record schema lint; no biological claim",
        "n_records": len(paths),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": rel(root, outdir / "external_record_schema_lint.tsv") if root == ROOT else str(outdir / "external_record_schema_lint.tsv"),
    }
    (outdir / "external_record_schema_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def write_record(path: Path, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(kwargs, indent=2, sort_keys=True) + "\n")


def build_synthetic_root(outdir: Path) -> Path:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    resources = root / EXTERNAL_ROOT / "catalogs/resources"
    records = root / EXTERNAL_ROOT / "records"
    resources.mkdir(parents=True)
    records.mkdir(parents=True)
    good = {
        "record_id": "SYNTH_GOOD_RESOURCE",
        "record_type": "external_resource_catalog",
        "resource_name": "Synthetic resource",
        "claim": "Synthetic resource claim.",
        "epistemic_class": "external-unverifiable",
        "source": {"label": "Synthetic source", "url": "https://example.invalid/resource"},
        "date_accessed": "2026-06-13",
        "access_tier": "open",
        "relationship_to_project_findings": "orthogonal",
        "not_project_grounded_marker": NOT_GROUNDED,
        "why_unverifiable": "Synthetic fixture.",
        "future_grounding_route": "Synthetic route.",
        "project_use": "Synthetic fixture.",
    }
    write_record(resources / "good_resource.json", **good)
    bad_missing_source = dict(good)
    bad_missing_source["record_id"] = "SYNTH_BAD_MISSING_SOURCE"
    bad_missing_source["source"] = {"label": ""}
    write_record(resources / "bad_missing_source.json", **bad_missing_source)
    bad_marker = dict(good)
    bad_marker["record_id"] = "SYNTH_BAD_MARKER"
    bad_marker["not_project_grounded_marker"] = "MISSING"
    write_record(resources / "bad_marker.json", **bad_marker)
    write_record(
        records / "good_verifiable.json",
        record_id="SYNTH_GOOD_VERIFIABLE",
        claim="Synthetic verifiable external claim.",
        epistemic_class="external-verifiable",
        source={"label": "Synthetic source", "url": "https://example.invalid/claim"},
        date_accessed="2026-06-13",
        relationship_to_project_findings="untested",
        not_project_grounded_marker=NOT_GROUNDED,
        future_grounding_route="Synthetic route.",
    )
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root = build_synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_root(root, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "external_record_schema_lint.tsv").open(), delimiter="\t"))
    checks = {
        "good_resource_passes": not any(row["record_id"] == "SYNTH_GOOD_RESOURCE" and row["status"] == "FAIL" for row in rows),
        "good_verifiable_passes": not any(row["record_id"] == "SYNTH_GOOD_VERIFIABLE" and row["status"] == "FAIL" for row in rows),
        "missing_source_fails": any(row["record_id"] == "SYNTH_BAD_MISSING_SOURCE" and row["check"] == "source_present" and row["status"] == "FAIL" for row in rows),
        "bad_marker_fails": any(row["record_id"] == "SYNTH_BAD_MARKER" and row["check"] == "not_grounded_marker" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_schema_lint_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V47 external-record schema linter synthetic fixtures; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_schema_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
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
