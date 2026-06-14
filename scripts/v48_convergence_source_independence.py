#!/usr/bin/env python3
"""Build a V48 convergence source-independence matrix."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
OUTDIR = ROOT / "knowledge_external/synthesis"
SUMMARY_PATH = ROOT / "knowledge_external/catalogs/indexes/convergence_source_independence_v48_summary.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--outdir", type=Path, default=OUTDIR)
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


def canonical_url(url: str) -> str:
    if not url:
        return ""
    parts = urlsplit(url)
    scheme = parts.scheme.lower() or "https"
    netloc = parts.netloc.lower()
    path = parts.path.rstrip("/") or "/"
    query = urlencode(sorted(parse_qsl(parts.query, keep_blank_values=True)))
    return urlunsplit((scheme, netloc, path, query, ""))


def source_domain(url: str) -> str:
    return urlsplit(url).netloc.lower()


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def source_independence_class(relationship: str, group_size: int) -> str:
    if relationship not in {"converges", "contradicts"}:
        return "not_decision_relationship"
    if group_size == 1:
        return "single_row_source"
    return "shared_source_cluster"


def build(matrix: Path, outdir: Path) -> dict[str, object]:
    matrix_rows = read_tsv(matrix)
    canonical_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in matrix_rows:
        canonical_groups[canonical_url(row.get("external_source", ""))].append(row)
    rows: list[dict[str, object]] = []
    for row in matrix_rows:
        canonical = canonical_url(row.get("external_source", ""))
        group = canonical_groups[canonical]
        relationship = row.get("relationship_class", "")
        rows.append(
            {
                "grounded_finding_id": row.get("grounded_finding_id", ""),
                "external_record_id": row.get("external_record_id", ""),
                "relationship_class": relationship,
                "synthesis_status": row.get("synthesis_status", ""),
                "external_source": row.get("external_source", ""),
                "canonical_source_url": canonical,
                "source_domain": source_domain(canonical),
                "canonical_source_row_count": len(group),
                "canonical_source_relationships": ";".join(sorted(Counter(item.get("relationship_class", "") for item in group))),
                "source_independence_class": source_independence_class(relationship, len(group)),
                "interpretation_boundary": "A shared canonical source is one external source cluster, not multiple independent corroborations.",
            }
        )
    outdir.mkdir(parents=True, exist_ok=True)
    fields = [
        "grounded_finding_id",
        "external_record_id",
        "relationship_class",
        "synthesis_status",
        "external_source",
        "canonical_source_url",
        "source_domain",
        "canonical_source_row_count",
        "canonical_source_relationships",
        "source_independence_class",
        "interpretation_boundary",
    ]
    write_tsv(outdir / "convergence_source_independence_v48.tsv", rows, fields)
    decision_rows = [row for row in rows if row["relationship_class"] in {"converges", "contradicts"}]
    decision_sources = {str(row["canonical_source_url"]) for row in decision_rows}
    converges = [row for row in rows if row["relationship_class"] == "converges"]
    converges_sources = {str(row["canonical_source_url"]) for row in converges}
    source_class_counts = Counter(str(row["source_independence_class"]) for row in rows)
    summary = {
        "purpose": "V48 convergence source-independence matrix; synthesis/navigation only; no biological claim",
        "n_matrix_rows": len(rows),
        "n_decision_relationship_rows": len(decision_rows),
        "n_decision_canonical_sources": len(decision_sources),
        "n_converges_rows": len(converges),
        "n_converges_canonical_sources": len(converges_sources),
        "source_independence_class_counts": dict(sorted(source_class_counts.items())),
        "overall_status": "PASS",
        "markdown": "knowledge_external/synthesis/CONVERGENCE_SOURCE_INDEPENDENCE_V48.md",
        "tsv": "knowledge_external/synthesis/convergence_source_independence_v48.tsv",
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Convergence Source-Independence Matrix",
        "",
        "Status: synthesis/navigation only. This matrix prevents overcounting multiple rows from the same external source as independent corroborations.",
        "",
        f"- matrix rows: `{summary['n_matrix_rows']}`",
        f"- decision relationship rows: `{summary['n_decision_relationship_rows']}`",
        f"- decision canonical sources: `{summary['n_decision_canonical_sources']}`",
        f"- convergence rows: `{summary['n_converges_rows']}`",
        f"- convergence canonical sources: `{summary['n_converges_canonical_sources']}`",
        "",
        "## Decision Relationship Source Clusters",
        "",
        "| relationship | grounded finding | external record | canonical source | source class | boundary |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        if row["relationship_class"] not in {"converges", "contradicts"}:
            continue
        lines.append(
            "| "
            f"`{md_escape(row['relationship_class'])}` | "
            f"{md_escape(row['grounded_finding_id'])} | "
            f"`{md_escape(row['external_record_id'])}` | "
            f"{md_escape(row['canonical_source_url'])} | "
            f"`{md_escape(row['source_independence_class'])}` | "
            f"{md_escape(row['interpretation_boundary'])} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Current V48 convergence rows are useful corroborating context, but source independence is counted by canonical source URL, not row count.",
            "- If multiple rows share one canonical source, treat them as one source cluster for independence accounting.",
            "- This matrix does not change any grounded finding or evidence grade.",
            "",
        ]
    )
    (outdir / "CONVERGENCE_SOURCE_INDEPENDENCE_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    matrix = args.matrix if args.matrix.is_absolute() else ROOT / args.matrix
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    summary = build(matrix, outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
