#!/usr/bin/env python3
"""Build the V48 high-priority source_terms review packet.

The packet is a navigation/terms-review artifact only. It does not grant reuse
permission, validate external claims, or move external knowledge into the
grounded project layer.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = ROOT / "knowledge_external/catalogs/indexes/source_terms_review_queue_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/catalogs/indexes"
EXTERNAL_DIRS = [
    ROOT / "knowledge_external/records",
    ROOT / "knowledge_external/catalogs/resources",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def record_index() -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for base in EXTERNAL_DIRS:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.json")):
            if path.name.endswith(".schema.json"):
                continue
            data = json.loads(path.read_text())
            record_id = str(data.get("record_id", ""))
            if record_id:
                index[record_id] = {"path": rel(path), "data": data}
    return index


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def build(queue: Path, outdir: Path) -> dict[str, object]:
    source_rows = [row for row in read_tsv(queue) if row.get("priority") == "high"]
    records = record_index()
    rows: list[dict[str, object]] = []
    for row in source_rows:
        record_id = row.get("record_id", "")
        record = records.get(record_id, {})
        data = record.get("data", {}) if isinstance(record.get("data"), dict) else {}
        rows.append(
            {
                "record_id": record_id,
                "record_path": record.get("path", "MISSING_RECORD_PATH"),
                "record_type": row.get("record_type", ""),
                "epistemic_class": row.get("epistemic_class", ""),
                "source_domain": row.get("source_domain", ""),
                "review_class": row.get("review_class", ""),
                "source_url": row.get("source_url", ""),
                "date_accessed": data.get("date_accessed", ""),
                "not_project_grounded_marker": data.get("not_project_grounded_marker", ""),
                "terms_review_reason": row.get("terms_review_reason", ""),
                "recommended_next_step": row.get("recommended_next_step", ""),
                "packet_boundary": "Terms metadata triage only; NOT reuse permission and NOT project-grounded evidence.",
            }
        )
    rows.sort(key=lambda row: (str(row["source_domain"]), str(row["record_id"])))
    outdir.mkdir(parents=True, exist_ok=True)
    fields = [
        "record_id",
        "record_path",
        "record_type",
        "epistemic_class",
        "source_domain",
        "review_class",
        "source_url",
        "date_accessed",
        "not_project_grounded_marker",
        "terms_review_reason",
        "recommended_next_step",
        "packet_boundary",
    ]
    write_tsv(outdir / "high_priority_source_terms_packet_v48.tsv", rows, fields)
    n_missing_paths = sum(1 for row in rows if row["record_path"] == "MISSING_RECORD_PATH")
    n_missing_markers = sum(1 for row in rows if row["not_project_grounded_marker"] != "NOT_PROJECT_GROUNDED")
    summary = {
        "purpose": "V48 high-priority source_terms review packet; source-terms triage only; no claim validation",
        "n_high_priority_records": len(rows),
        "n_missing_record_paths": n_missing_paths,
        "n_missing_not_project_grounded_markers": n_missing_markers,
        "overall_status": "PASS" if n_missing_paths == 0 and n_missing_markers == 0 else "FAIL",
        "markdown": "knowledge_external/catalogs/indexes/HIGH_PRIORITY_SOURCE_TERMS_PACKET_V48.md",
        "tsv": "knowledge_external/catalogs/indexes/high_priority_source_terms_packet_v48.tsv",
    }
    (outdir / "high_priority_source_terms_packet_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 High-Priority Source-Terms Review Packet",
        "",
        "Status: source-terms triage only. This packet does not grant reuse permission, validate external claims, or move any external source into the grounded project layer.",
        "",
        f"- high-priority records: `{summary['n_high_priority_records']}`",
        f"- missing record paths: `{summary['n_missing_record_paths']}`",
        f"- missing NOT_PROJECT_GROUNDED markers: `{summary['n_missing_not_project_grounded_markers']}`",
        "",
        "## Review Targets",
        "",
        "| record | type | class | domain | review class | source | path | next step |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"`{md_escape(row['record_id'])}` | "
            f"`{md_escape(row['record_type'])}` | "
            f"`{md_escape(row['epistemic_class'])}` | "
            f"{md_escape(row['source_domain'])} | "
            f"`{md_escape(row['review_class'])}` | "
            f"{md_escape(row['source_url'])} | "
            f"`{md_escape(row['record_path'])}` | "
            f"{md_escape(row['recommended_next_step'])} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Every row remains external-classed and `NOT_PROJECT_GROUNDED`.",
            "- Add source_terms metadata only when terms can be stated conservatively from a source.",
            "- If terms remain ambiguous, leave the record in review rather than inventing permission.",
            "",
        ]
    )
    (outdir / "HIGH_PRIORITY_SOURCE_TERMS_PACKET_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    summary = build(args.queue, args.outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
