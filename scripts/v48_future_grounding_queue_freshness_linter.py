#!/usr/bin/env python3
"""Check that V48 future-grounding queue rows match matrix follow-up actions."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_QUEUE = ROOT / "knowledge_external/synthesis/future_grounding_queue_v48.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v48_future_grounding_queue_freshness_linter"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint real V48 future-grounding queue freshness")
    lint.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    lint.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic freshness fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def key(row: dict[str, str]) -> tuple[str, str]:
    return row.get("grounded_finding_id", ""), row.get("external_record_id", "")


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def lint_freshness(matrix: Path, queue: Path, outdir: Path, fail_on_error: bool) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    matrix_rows = read_tsv(matrix) if matrix.exists() else []
    queue_rows = read_tsv(queue) if queue.exists() else []
    queue_keys = {key(row) for row in queue_rows}
    matrix_keys = {key(row) for row in matrix_rows if row.get("future_grounding_action", "").strip()}
    lint_rows: list[dict[str, object]] = []
    for finding_id, external_id in sorted(matrix_keys):
        lint_rows.append(
            {
                "grounded_finding_id": finding_id,
                "external_record_id": external_id,
                "check": "matrix_followup_has_queue_row",
                "status": "PASS" if (finding_id, external_id) in queue_keys else "FAIL",
                "detail": "",
            }
        )
    for finding_id, external_id in sorted(queue_keys - matrix_keys):
        lint_rows.append(
            {
                "grounded_finding_id": finding_id,
                "external_record_id": external_id,
                "check": "queue_row_has_matrix_followup",
                "status": "FAIL",
                "detail": "stale queue row",
            }
        )
    n_fail = sum(1 for row in lint_rows if row["status"] != "PASS")
    write_tsv(outdir / "future_grounding_queue_freshness_lint.tsv", lint_rows, ["grounded_finding_id", "external_record_id", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 future-grounding queue freshness lint; no biological claim",
        "n_matrix_followups": len(matrix_keys),
        "n_queue_rows": len(queue_keys),
        "n_checks": len(lint_rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": str(outdir / "future_grounding_queue_freshness_lint.tsv"),
    }
    (outdir / "future_grounding_queue_freshness_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    matrix = outdir / "matrix.tsv"
    queue = outdir / "queue.tsv"
    write_tsv(
        matrix,
        [
            {"grounded_finding_id": "A", "external_record_id": "X", "future_grounding_action": "do x"},
            {"grounded_finding_id": "B", "external_record_id": "Y", "future_grounding_action": "do y"},
        ],
        ["grounded_finding_id", "external_record_id", "future_grounding_action"],
    )
    write_tsv(
        queue,
        [
            {"grounded_finding_id": "A", "external_record_id": "X"},
            {"grounded_finding_id": "STALE", "external_record_id": "Z"},
        ],
        ["grounded_finding_id", "external_record_id"],
    )
    lint_out = outdir / "synthetic_lint"
    lint_freshness(matrix, queue, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "future_grounding_queue_freshness_lint.tsv")
    checks = {
        "matching_row_passes": any(row["grounded_finding_id"] == "A" and row["status"] == "PASS" for row in rows),
        "missing_queue_row_fails": any(row["grounded_finding_id"] == "B" and row["status"] == "FAIL" for row in rows),
        "stale_queue_row_fails": any(row["grounded_finding_id"] == "STALE" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": k, "status": "PASS" if v else "FAIL"} for k, v in checks.items()]
    write_tsv(outdir / "synthetic_future_grounding_queue_freshness_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 future-grounding queue freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_future_grounding_queue_freshness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_freshness(args.matrix, args.queue, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
