#!/usr/bin/env python3
"""Generate class-aware indexes for V47 external knowledge records.

The index is navigation infrastructure only. It preserves epistemic class,
source, access date, relationship tags, and the explicit NOT_PROJECT_GROUNDED
marker for every external record. It does not validate external claims and does
not turn them into project-grounded findings.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = "knowledge_external"
DEFAULT_OUTDIR = ROOT / EXTERNAL_ROOT / "catalogs/indexes"
DEFAULT_SYNTHETIC_OUTDIR = ROOT / "analysis/v47_external_knowledge_index"
EXTERNAL_RECORD_DIRS = [
    f"{EXTERNAL_ROOT}/records",
    f"{EXTERNAL_ROOT}/catalogs/resources",
]
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    index = sub.add_parser("index", help="Index real external knowledge records")
    index.add_argument("--root", type=Path, default=ROOT)
    index.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth = sub.add_parser("synthetic-check", help="Verify class labels survive aggregation")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_SYNTHETIC_OUTDIR)
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


def write_markdown(path: Path, summary: dict[str, object], count_rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# External Knowledge Index",
        "",
        "Status: navigation only. No project-grounded finding is made here.",
        "",
        f"- records indexed: `{summary['n_records']}`",
        f"- records missing source: `{summary['n_missing_source']}`",
        f"- records missing not-grounded marker: `{summary['n_missing_not_grounded_marker']}`",
        f"- overall status: `{summary['overall_status']}`",
        "",
        "## Counts",
        "",
        "| field | value | count |",
        "|---|---|---:|",
    ]
    for row in count_rows:
        lines.append(f"| {row['field']} | {row['value']} | {row['count']} |")
    lines.extend(
        [
            "",
            "## Files",
            "",
            "- `external_knowledge_index.tsv`",
            "- `external_knowledge_index_counts.tsv`",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n")


def record_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for directory in EXTERNAL_RECORD_DIRS:
        base = root / directory
        if not base.exists():
            continue
        paths.extend(
            path
            for path in base.rglob("*.json")
            if not path.name.endswith(".schema.json") and "schema" not in path.parts
        )
    return sorted(paths)


def load_record(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"Record is not a JSON object: {path}")
    return data


def source_field(source: Any, field: str) -> str:
    if isinstance(source, dict):
        return str(source.get(field, "")).strip()
    return ""


def source_present(source: Any) -> bool:
    if not isinstance(source, dict):
        return False
    return bool(source_field(source, "label")) and any(
        source_field(source, field) for field in ["url", "doi", "pmid", "citation"]
    )


def row_for_record(root: Path, path: Path, data: dict[str, Any]) -> dict[str, object]:
    source = data.get("source")
    return {
        "record_id": str(data.get("record_id", "")),
        "record_type": str(data.get("record_type", "external_claim_record")),
        "epistemic_class": str(data.get("epistemic_class", "")),
        "relationship_to_project_findings": str(data.get("relationship_to_project_findings", "")),
        "date_accessed": str(data.get("date_accessed", "")),
        "not_project_grounded_marker": str(data.get("not_project_grounded_marker", "")),
        "source_label": source_field(source, "label"),
        "source_url": source_field(source, "url"),
        "source_doi": source_field(source, "doi"),
        "source_pmid": source_field(source, "pmid"),
        "source_present": source_present(source),
        "claim": str(data.get("claim", "")),
        "path": rel(root, path),
    }


def count_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for field in ["epistemic_class", "relationship_to_project_findings", "record_type"]:
        counter = Counter(str(row.get(field, "")) for row in rows)
        for value, count in sorted(counter.items()):
            result.append({"field": field, "value": value or "MISSING", "count": count})
    return result


def write_index(root: Path, outdir: Path) -> dict[str, object]:
    outdir = outdir if outdir.is_absolute() else root / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for path in record_paths(root):
        rows.append(row_for_record(root, path, load_record(path)))
    fields = [
        "record_id",
        "record_type",
        "epistemic_class",
        "relationship_to_project_findings",
        "date_accessed",
        "not_project_grounded_marker",
        "source_label",
        "source_url",
        "source_doi",
        "source_pmid",
        "source_present",
        "claim",
        "path",
    ]
    counts = count_rows(rows)
    n_missing_source = sum(1 for row in rows if not row["source_present"])
    n_missing_marker = sum(1 for row in rows if row["not_project_grounded_marker"] != NOT_GROUNDED)
    summary = {
        "synthetic": False,
        "purpose": "V47 external knowledge class-aware navigation index; no biological claim",
        "n_records": len(rows),
        "n_missing_source": n_missing_source,
        "n_missing_not_grounded_marker": n_missing_marker,
        "overall_status": "PASS" if n_missing_source == 0 and n_missing_marker == 0 else "REVIEW_NEEDED",
        "index": rel(root, outdir / "external_knowledge_index.tsv"),
        "counts": rel(root, outdir / "external_knowledge_index_counts.tsv"),
    }
    write_tsv(outdir / "external_knowledge_index.tsv", rows, fields)
    write_tsv(outdir / "external_knowledge_index_counts.tsv", counts, ["field", "value", "count"])
    write_markdown(outdir / "EXTERNAL_KNOWLEDGE_INDEX.md", summary, counts)
    return summary


def write_record(path: Path, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(kwargs, indent=2, sort_keys=True) + "\n")


def build_synthetic_root(outdir: Path) -> Path:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    records = root / EXTERNAL_ROOT / "records"
    catalog = root / EXTERNAL_ROOT / "catalogs/resources"
    records.mkdir(parents=True)
    catalog.mkdir(parents=True)
    write_record(
        records / "synthetic_claim.json",
        record_id="SYNTH_CLAIM_001",
        record_type="external_claim_record",
        claim="Synthetic external claim used only to test index aggregation.",
        epistemic_class="external-verifiable",
        source={"label": "Synthetic source", "url": "https://example.invalid/synthetic-claim"},
        date_accessed="2026-06-13",
        relationship_to_project_findings="untested",
        not_project_grounded_marker=NOT_GROUNDED,
        future_grounding_route="Synthetic grounding route.",
    )
    write_record(
        catalog / "synthetic_resource.json",
        record_id="SYNTH_RESOURCE_001",
        record_type="external_resource_catalog",
        resource_name="Synthetic MS resource",
        claim="Synthetic resource metadata used only to test index aggregation.",
        epistemic_class="external-unverifiable",
        source={"label": "Synthetic resource source", "url": "https://example.invalid/synthetic-resource"},
        date_accessed="2026-06-13",
        access_tier="open",
        relationship_to_project_findings="orthogonal",
        not_project_grounded_marker=NOT_GROUNDED,
        why_unverifiable="Synthetic resource has no real source to reground.",
        future_grounding_route="No biological grounding; fixture only.",
        project_use="Synthetic index test.",
    )
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root = build_synthetic_root(outdir)
    summary = write_index(root, outdir / "synthetic_index")
    counts_path = outdir / "synthetic_index/external_knowledge_index_counts.tsv"
    counts = list(csv.DictReader(counts_path.open(), delimiter="\t"))
    checks = {
        "n_records_is_2": summary["n_records"] == 2,
        "status_pass": summary["overall_status"] == "PASS",
        "verifiable_count_is_1": any(
            row["field"] == "epistemic_class" and row["value"] == "external-verifiable" and row["count"] == "1"
            for row in counts
        ),
        "unverifiable_count_is_1": any(
            row["field"] == "epistemic_class" and row["value"] == "external-unverifiable" and row["count"] == "1"
            for row in counts
        ),
    }
    rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_index_checks.tsv", rows, ["check", "status"])
    synthetic_summary = {
        "synthetic": True,
        "purpose": "V47 external knowledge index synthetic aggregation check; no biological claim",
        "n_checks": len(rows),
        "n_fail": sum(1 for row in rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
        "index_summary": summary,
    }
    (outdir / "synthetic_index_summary.json").write_text(json.dumps(synthetic_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synthetic_summary, indent=2, sort_keys=True))
    return 0 if synthetic_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "index":
        summary = write_index(args.root.resolve(), args.outdir)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())

