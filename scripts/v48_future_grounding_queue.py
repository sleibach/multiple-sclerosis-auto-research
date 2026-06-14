#!/usr/bin/env python3
"""Build a future-grounding queue from the V48 relationship matrix.

Rows are tasks, not findings. They preserve source and not-grounded markers
from the external relationship matrix and are meant to prevent vague external
context from becoming implicit evidence.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/synthesis"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/future_grounding_queue_v48_summary.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def task_priority(row: dict[str, str]) -> str:
    status = row.get("synthesis_status", "")
    finding = row.get("grounded_finding_id", "")
    if "RESOURCE_CAN_QUEUE" in status:
        return "high"
    if "NO_DIRECT_EXTERNAL_CORROBORATION" in status and "Bounded APC/HLA-II" in finding:
        return "high"
    if "CORROBORATION" in status:
        return "low"
    return "medium"


def task_status(row: dict[str, str]) -> str:
    if row.get("relationship_class") == "converges":
        return "optional_refresh_only"
    return "queued_for_future_grounding"


def queue_rows(matrix_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(matrix_rows, start=1):
        action = row.get("future_grounding_action", "").strip()
        if not action:
            continue
        rows.append(
            {
                "queue_id": f"V48_FG_{index:03d}",
                "priority": task_priority(row),
                "task_status": task_status(row),
                "grounded_finding_id": row.get("grounded_finding_id", ""),
                "grounded_artifact": row.get("grounded_artifact", ""),
                "external_record_id": row.get("external_record_id", ""),
                "epistemic_class": row.get("epistemic_class", ""),
                "external_source": row.get("external_source", ""),
                "not_project_grounded_marker": row.get("not_project_grounded_marker", ""),
                "relationship_class": row.get("relationship_class", ""),
                "synthesis_status": row.get("synthesis_status", ""),
                "future_grounding_action": action,
            }
        )
    return rows


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    lines = [
        "# V48 Future-Grounding Queue",
        "",
        "Status: queue only. These rows are not findings and do not alter grounded conclusions.",
        "",
        f"- queued tasks: `{summary['n_tasks']}`",
        f"- high-priority tasks: `{summary['n_high_priority']}`",
        f"- optional refresh tasks: `{summary['n_optional_refresh_only']}`",
        f"- missing not-grounded markers: `{summary['n_missing_not_grounded_marker']}`",
        f"- overall status: `{summary['overall_status']}`",
        "",
        "| queue id | priority | status | grounded finding | external record | source | action |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['queue_id']} | `{row['priority']}` | `{row['task_status']}` | {row['grounded_finding_id']} | `{row['external_record_id']}` ({row['epistemic_class']} / `{row['not_project_grounded_marker']}`) | {row['external_source']} | {row['future_grounding_action']} |"
        )
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    rows = queue_rows(read_tsv(args.matrix))
    fields = [
        "queue_id",
        "priority",
        "task_status",
        "grounded_finding_id",
        "grounded_artifact",
        "external_record_id",
        "epistemic_class",
        "external_source",
        "not_project_grounded_marker",
        "relationship_class",
        "synthesis_status",
        "future_grounding_action",
    ]
    n_missing_marker = sum(1 for row in rows if row["not_project_grounded_marker"] != "NOT_PROJECT_GROUNDED")
    summary = {
        "purpose": "V48 future-grounding queue; tasks only, no biological claim",
        "n_tasks": len(rows),
        "n_high_priority": sum(1 for row in rows if row["priority"] == "high"),
        "n_optional_refresh_only": sum(1 for row in rows if row["task_status"] == "optional_refresh_only"),
        "n_missing_not_grounded_marker": n_missing_marker,
        "overall_status": "PASS" if n_missing_marker == 0 else "FAIL",
        "queue": "knowledge_external/synthesis/future_grounding_queue_v48.tsv",
        "markdown": "knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md",
    }
    args.outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(args.outdir / "future_grounding_queue_v48.tsv", rows, fields)
    write_markdown(args.outdir / "FUTURE_GROUNDING_QUEUE_V48.md", rows, summary)
    DEFAULT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
