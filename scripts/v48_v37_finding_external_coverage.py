#!/usr/bin/env python3
"""Map V37 scored findings to V48 external convergence/contradiction rows."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_V37 = ROOT / "docs/reports/FINDINGS_SCORES_V37.tsv"
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/synthesis"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--v37", type=Path, default=DEFAULT_V37)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def build(v37_path: Path, matrix_path: Path, outdir: Path) -> dict[str, object]:
    v37_rows = read_tsv(v37_path)
    matrix_rows = read_tsv(matrix_path)
    matrix_by_finding: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in matrix_rows:
        matrix_by_finding[row.get("grounded_finding_id", "")].append(row)

    coverage_rows: list[dict[str, object]] = []
    for row in v37_rows:
        item = row.get("item", "")
        linked = matrix_by_finding.get(item, [])
        relation_counts = Counter(link.get("relationship_class", "") for link in linked)
        status_counts = Counter(link.get("synthesis_status", "") for link in linked)
        if any(link.get("relationship_class") == "converges" for link in linked):
            coverage = "has_external_convergence"
        elif any(link.get("relationship_class") == "contradicts" for link in linked):
            coverage = "has_external_contradiction"
        elif linked:
            coverage = "has_external_context_only"
        else:
            coverage = "no_v48_external_relationship_row"
        coverage_rows.append(
            {
                "item": item,
                "category": row.get("category", ""),
                "relevance": row.get("relevance", ""),
                "novelty": row.get("novelty", ""),
                "evidence_grade": row.get("evidence_grade", ""),
                "supporting_artifact": row.get("supporting_artifact", ""),
                "status": row.get("status", ""),
                "v48_coverage": coverage,
                "n_v48_rows": len(linked),
                "relationship_classes": ";".join(f"{key}:{value}" for key, value in sorted(relation_counts.items()) if key),
                "synthesis_statuses": ";".join(f"{key}:{value}" for key, value in sorted(status_counts.items()) if key),
                "external_record_ids": ";".join(sorted({link.get("external_record_id", "") for link in linked if link.get("external_record_id")})),
                "external_sources": ";".join(sorted({link.get("external_source", "") for link in linked if link.get("external_source")})),
            }
        )

    outdir.mkdir(parents=True, exist_ok=True)
    fields = [
        "item",
        "category",
        "relevance",
        "novelty",
        "evidence_grade",
        "supporting_artifact",
        "status",
        "v48_coverage",
        "n_v48_rows",
        "relationship_classes",
        "synthesis_statuses",
        "external_record_ids",
        "external_sources",
    ]
    write_tsv(outdir / "v37_finding_external_coverage_v48.tsv", coverage_rows, fields)
    coverage_counts = Counter(str(row["v48_coverage"]) for row in coverage_rows)
    category_counts = Counter(str(row["category"]) for row in coverage_rows)
    summary = {
        "purpose": "V48 V37 scored-finding external coverage map; navigation/synthesis only; external context is not evidence",
        "n_v37_findings": len(coverage_rows),
        "n_v48_matrix_rows": len(matrix_rows),
        "coverage_counts": dict(sorted(coverage_counts.items())),
        "category_counts": dict(sorted(category_counts.items())),
        "overall_status": "PASS",
        "markdown": "knowledge_external/synthesis/V37_FINDING_EXTERNAL_COVERAGE_V48.md",
        "tsv": "knowledge_external/synthesis/v37_finding_external_coverage_v48.tsv",
    }
    summary_path = ROOT / "knowledge_external/catalogs/indexes/v37_finding_external_coverage_v48_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    lines = [
        "# V37 Finding External Coverage V48",
        "",
        "Status: synthesis/navigation only. V48 external rows are classed context; grounded V37 artifacts remain the evidence.",
        "",
        f"- V37 scored findings: `{summary['n_v37_findings']}`",
        f"- V48 convergence/contradiction matrix rows: `{summary['n_v48_matrix_rows']}`",
        "",
        "## Coverage Counts",
        "",
        "| coverage | count |",
        "|---|---:|",
    ]
    for key, value in sorted(coverage_counts.items()):
        lines.append(f"| `{md_escape(key)}` | {value} |")
    lines.extend(
        [
            "",
            "## Findings",
            "",
            "| finding | category | evidence | V48 coverage | V48 rows | relationship classes | external sources |",
            "|---|---|---|---|---:|---|---|",
        ]
    )
    for row in coverage_rows:
        sources = row["external_sources"] or "none"
        lines.append(
            "| "
            f"{md_escape(row['item'])} | "
            f"`{md_escape(row['category'])}` | "
            f"`{md_escape(row['evidence_grade'])}` | "
            f"`{md_escape(row['v48_coverage'])}` | "
            f"{row['n_v48_rows']} | "
            f"`{md_escape(row['relationship_classes'] or 'none')}` | "
            f"{md_escape(sources)} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `has_external_convergence` means an independent external source aligns with a grounded project finding; the grounded artifact remains the evidence.",
            "- `has_external_context_only` means V48 found related external context but no direct corroboration or contradiction.",
            "- `no_v48_external_relationship_row` means V48 has not linked an external record to that finding.",
            "- No row here changes any V37 score, locked rule, or validation plan.",
            "",
        ]
    )
    (outdir / "V37_FINDING_EXTERNAL_COVERAGE_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    v37 = args.v37 if args.v37.is_absolute() else root / args.v37
    matrix = args.matrix if args.matrix.is_absolute() else root / args.matrix
    outdir = args.outdir if args.outdir.is_absolute() else root / args.outdir
    summary = build(v37, matrix, outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
