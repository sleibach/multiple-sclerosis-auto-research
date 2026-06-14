#!/usr/bin/env python3
"""Lint project_finding_reference objects on linked external records."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECORD_DIRS = [ROOT / "knowledge_external/records", ROOT / "knowledge_external/catalogs/resources"]
DEFAULT_SCORES = ROOT / "docs/reports/FINDINGS_SCORES_V37.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v48_project_finding_reference_linter"
LINKED_RELATIONSHIPS = {"supports", "contradicts"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint real project finding references")
    lint.add_argument("--scores", type=Path, default=DEFAULT_SCORES)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic reference fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def record_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for relative in ["knowledge_external/records", "knowledge_external/catalogs/resources"]:
        base = root / relative
        if base.exists():
            paths.extend(path for path in base.rglob("*.json") if not path.name.endswith(".schema.json"))
    return sorted(paths)


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def finding_items(scores: Path) -> set[str]:
    return {row.get("item", "") for row in read_tsv(scores)}


def add(rows: list[dict[str, object]], path: str, record_id: str, check: str, ok: bool, detail: str) -> None:
    rows.append({"path": path, "record_id": record_id, "check": check, "status": "PASS" if ok else "FAIL", "detail": detail})


def lint_records(root: Path, scores: Path, outdir: Path, fail_on_error: bool) -> int:
    root = root.resolve()
    outdir = outdir if outdir.is_absolute() else root / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    items = finding_items(scores)
    rows: list[dict[str, object]] = []
    linked_count = 0
    for path in record_paths(root):
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            continue
        relationship = str(data.get("relationship_to_project_findings", ""))
        if relationship not in LINKED_RELATIONSHIPS:
            continue
        linked_count += 1
        rel_path = rel(root, path)
        record_id = str(data.get("record_id", ""))
        reference: Any = data.get("project_finding_reference")
        add(rows, rel_path, record_id, "reference_object_present", isinstance(reference, dict), str(type(reference).__name__))
        if not isinstance(reference, dict):
            continue
        finding_id = str(reference.get("finding_id", ""))
        artifact = str(reference.get("artifact", ""))
        add(rows, rel_path, record_id, "finding_id_present", bool(finding_id), finding_id)
        add(rows, rel_path, record_id, "finding_id_in_v37_scores", finding_id in items, finding_id)
        add(rows, rel_path, record_id, "artifact_present", bool(artifact), artifact)
        add(rows, rel_path, record_id, "artifact_exists", bool(artifact) and (root / artifact).exists(), artifact)
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    write_tsv(outdir / "project_finding_reference_lint.tsv", rows, ["path", "record_id", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 project finding reference lint; no biological claim",
        "n_linked_external_records": linked_count,
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": rel(root, outdir / "project_finding_reference_lint.tsv") if root == ROOT else str(outdir / "project_finding_reference_lint.tsv"),
    }
    (outdir / "project_finding_reference_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def write_record(path: Path, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(kwargs, indent=2, sort_keys=True) + "\n")


def synthetic_root(outdir: Path) -> Path:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    (root / "knowledge_external/records").mkdir(parents=True)
    (root / "docs/reports").mkdir(parents=True)
    (root / "docs/reports/FINDINGS_SCORES_V37.tsv").write_text("item\tcategory\nevidence one\tpositive\n")
    (root / "docs/reports/FINDINGS_REPORT_V37.md").write_text("report\n")
    base = {
        "claim": "Synthetic linked external claim.",
        "epistemic_class": "external-unverifiable",
        "source": {"label": "Synthetic", "url": "https://example.invalid"},
        "date_accessed": "2026-06-14",
        "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
        "why_unverifiable": "Synthetic fixture.",
    }
    write_record(
        root / "knowledge_external/records/good.json",
        **base,
        record_id="SYNTH_GOOD_REF",
        relationship_to_project_findings="supports",
        project_finding_reference={"finding_id": "evidence one", "artifact": "docs/reports/FINDINGS_REPORT_V37.md"},
    )
    write_record(
        root / "knowledge_external/records/bad.json",
        **base,
        record_id="SYNTH_BAD_REF",
        relationship_to_project_findings="supports",
        project_finding_reference={"finding_id": "missing", "artifact": "docs/reports/MISSING.md"},
    )
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    root = synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_records(root, root / "docs/reports/FINDINGS_SCORES_V37.tsv", lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "project_finding_reference_lint.tsv")
    checks = {
        "good_reference_passes": not any(row["record_id"] == "SYNTH_GOOD_REF" and row["status"] == "FAIL" for row in rows),
        "missing_finding_fails": any(row["record_id"] == "SYNTH_BAD_REF" and row["check"] == "finding_id_in_v37_scores" and row["status"] == "FAIL" for row in rows),
        "missing_artifact_fails": any(row["record_id"] == "SYNTH_BAD_REF" and row["check"] == "artifact_exists" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_project_finding_reference_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 project finding reference synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_project_finding_reference_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_records(ROOT, args.scores, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
