#!/usr/bin/env python3
"""Lint external-verifiable claim records for future grounding routes.

This linter does not ground or validate external claims. It only verifies that
any record labeled external-verifiable remains explicitly queued for grounding
and cannot be confused with project evidence.
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
DEFAULT_OUTDIR = ROOT / "analysis/v47_external_verifiable_intake_linter"
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"
ALLOWED_GROUNDING_STATUS = {
    "queued_for_future_grounding",
    "blocked_needs_data",
    "blocked_needs_access",
    "blocked_needs_human_decision",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint real external-verifiable records")
    lint.add_argument("--root", type=Path, default=ROOT)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic intake fixtures")
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


def candidate_json_paths(root: Path) -> list[Path]:
    base = root / EXTERNAL_ROOT
    if not base.exists():
        return []
    return sorted(
        path
        for path in base.rglob("*.json")
        if not path.name.endswith(".schema.json")
        and "indexes" not in path.parts
        and "synthesis" not in path.parts
    )


def load_record(path: Path) -> dict[str, Any] | None:
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or "epistemic_class" not in data:
        return None
    return data


def has_source_locator(source: Any) -> bool:
    if not isinstance(source, dict):
        return False
    return any(str(source.get(field, "")).strip() for field in ["url", "doi", "pmid", "citation"])


def check_record(root: Path, path: Path, data: dict[str, Any]) -> list[dict[str, object]]:
    rel_path = rel(root, path)
    record_id = str(data.get("record_id", ""))
    if data.get("epistemic_class") != "external-verifiable":
        return [
            {
                "path": rel_path,
                "record_id": record_id,
                "check": "not_external_verifiable_record",
                "status": "PASS",
                "detail": "Record is outside this linter's external-verifiable scope.",
            }
        ]
    checks = {
        "source_locator_present": has_source_locator(data.get("source")),
        "not_project_grounded_marker": data.get("not_project_grounded_marker") == NOT_GROUNDED,
        "future_grounding_route_present": bool(str(data.get("future_grounding_route", "")).strip()),
        "grounding_data_needed_present": bool(str(data.get("grounding_data_needed", "")).strip()),
        "grounding_status_valid": data.get("grounding_status") in ALLOWED_GROUNDING_STATUS,
        "relationship_not_support_or_contradict_without_grounding": data.get("relationship_to_project_findings") in {"orthogonal", "untested"},
    }
    return [
        {
            "path": rel_path,
            "record_id": record_id,
            "check": check,
            "status": "PASS" if ok else "FAIL",
            "detail": "external-verifiable must remain queued for future grounding",
        }
        for check, ok in checks.items()
    ]


def lint_root(root: Path, outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else root / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    n_external_verifiable = 0
    for path in candidate_json_paths(root):
        data = load_record(path)
        if data is None:
            continue
        if data.get("epistemic_class") == "external-verifiable":
            n_external_verifiable += 1
        rows.extend(check_record(root, path, data))
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    write_tsv(outdir / "external_verifiable_intake_lint.tsv", rows, ["path", "record_id", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V47 external-verifiable intake lint; queueing infrastructure only, no claim validation",
        "n_records_checked": len({row["path"] for row in rows}),
        "n_external_verifiable_records": n_external_verifiable,
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "external_verifiable_intake_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
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
        "record_type": "external_claim",
        "claim": "Synthetic external-verifiable claim.",
        "epistemic_class": "external-verifiable",
        "date_accessed": "2026-06-13",
        "relationship_to_project_findings": "untested",
        "not_project_grounded_marker": NOT_GROUNDED,
        "source": {"label": "Synthetic source", "url": "https://example.invalid/source"},
        "project_use": "Synthetic queueing test.",
    }
    write_record(
        records / "good_external_verifiable.json",
        **base,
        record_id="SYNTH_GOOD_VERIFIABLE",
        future_grounding_route="Run a synthetic held-data check before any conclusion.",
        grounding_data_needed="Synthetic data matrix.",
        grounding_status="queued_for_future_grounding",
    )
    write_record(
        records / "bad_missing_route.json",
        **base,
        record_id="SYNTH_BAD_MISSING_ROUTE",
        future_grounding_route="",
        grounding_data_needed="Synthetic data matrix.",
        grounding_status="queued_for_future_grounding",
    )
    write_record(
        records / "bad_supports_without_grounding.json",
        **{**base, "relationship_to_project_findings": "supports"},
        record_id="SYNTH_BAD_SUPPORTS",
        future_grounding_route="Run a synthetic held-data check before any conclusion.",
        grounding_data_needed="Synthetic data matrix.",
        grounding_status="queued_for_future_grounding",
    )
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root = build_synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_root(root, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "external_verifiable_intake_lint.tsv").open(), delimiter="\t"))
    checks = {
        "good_record_passes": any(row["record_id"] == "SYNTH_GOOD_VERIFIABLE" and row["status"] == "PASS" for row in rows),
        "missing_route_fails": any(row["record_id"] == "SYNTH_BAD_MISSING_ROUTE" and row["check"] == "future_grounding_route_present" and row["status"] == "FAIL" for row in rows),
        "supports_without_grounding_fails": any(row["record_id"] == "SYNTH_BAD_SUPPORTS" and row["check"] == "relationship_not_support_or_contradict_without_grounding" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_external_verifiable_intake_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V47 external-verifiable intake synthetic fixture; no claim validation",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_external_verifiable_intake_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
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
