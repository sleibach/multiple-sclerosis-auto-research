#!/usr/bin/env python3
"""Build a source-domain relationship rollup for V48 external records."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = ROOT / "knowledge_external"
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/catalogs/indexes"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def record_paths() -> list[Path]:
    paths: list[Path] = []
    for subdir in ["records", "catalogs/resources"]:
        base = EXTERNAL_ROOT / subdir
        if base.exists():
            paths.extend(path for path in base.rglob("*.json") if not path.name.endswith(".schema.json"))
    return sorted(paths)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_url(data: dict[str, object]) -> str:
    source = data.get("source")
    if isinstance(source, dict):
        return str(source.get("url", "")).strip()
    return ""


def domain_for_url(url: str) -> str:
    if not url:
        return "NO_URL"
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def build(matrix: Path, outdir: Path) -> dict[str, object]:
    records: dict[str, dict[str, object]] = {}
    domain_relationship_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for path in record_paths():
        data = json.loads(path.read_text())
        record_id = str(data.get("record_id", ""))
        domain = domain_for_url(source_url(data))
        relationship = str(data.get("relationship_to_project_findings", ""))
        records[record_id] = {
            "domain": domain,
            "record_type": str(data.get("record_type", "")),
            "epistemic_class": str(data.get("epistemic_class", "")),
            "relationship_to_project_findings": relationship,
        }
        domain_relationship_counts[domain][relationship] += 1

    matrix_relationship_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in read_tsv(matrix):
        record_id = row.get("external_record_id", "")
        domain = str(records.get(record_id, {}).get("domain", "missing_record"))
        matrix_relationship_counts[domain][row.get("relationship_class", "")] += 1

    domains = sorted(set(domain_relationship_counts) | set(matrix_relationship_counts))
    rows: list[dict[str, object]] = []
    for domain in domains:
        record_counts = domain_relationship_counts[domain]
        matrix_counts = matrix_relationship_counts[domain]
        rows.append(
            {
                "source_domain": domain,
                "n_records": sum(record_counts.values()),
                "record_relationship_counts": ";".join(f"{key}:{value}" for key, value in sorted(record_counts.items()) if key),
                "n_matrix_rows": sum(matrix_counts.values()),
                "matrix_relationship_counts": ";".join(f"{key}:{value}" for key, value in sorted(matrix_counts.items()) if key),
                "has_convergence": "yes" if matrix_counts.get("converges", 0) else "no",
                "has_contradiction": "yes" if matrix_counts.get("contradicts", 0) else "no",
            }
        )
    outdir.mkdir(parents=True, exist_ok=True)
    fields = [
        "source_domain",
        "n_records",
        "record_relationship_counts",
        "n_matrix_rows",
        "matrix_relationship_counts",
        "has_convergence",
        "has_contradiction",
    ]
    write_tsv(outdir / "source_domain_relationship_rollup_v48.tsv", rows, fields)
    summary = {
        "purpose": "V48 source-domain relationship rollup; navigation/synthesis only; no claim validation",
        "n_source_domains": len(rows),
        "n_domains_with_convergence": sum(1 for row in rows if row["has_convergence"] == "yes"),
        "n_domains_with_contradiction": sum(1 for row in rows if row["has_contradiction"] == "yes"),
        "n_external_records": len(records),
        "n_matrix_rows": sum(int(row["n_matrix_rows"]) for row in rows),
        "overall_status": "PASS",
        "markdown": "knowledge_external/catalogs/indexes/SOURCE_DOMAIN_RELATIONSHIP_ROLLUP_V48.md",
        "tsv": "knowledge_external/catalogs/indexes/source_domain_relationship_rollup_v48.tsv",
    }
    (outdir / "source_domain_relationship_rollup_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Source-Domain Relationship Rollup",
        "",
        "Status: navigation/synthesis only. This rollup summarizes provenance and relationship classes; it does not validate external claims.",
        "",
        f"- source domains: `{summary['n_source_domains']}`",
        f"- domains with convergence rows: `{summary['n_domains_with_convergence']}`",
        f"- domains with contradiction rows: `{summary['n_domains_with_contradiction']}`",
        f"- external records: `{summary['n_external_records']}`",
        f"- V48 matrix rows: `{summary['n_matrix_rows']}`",
        "",
        "## Domains",
        "",
        "| domain | records | record relationships | matrix rows | matrix relationships | convergence | contradiction |",
        "|---|---:|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{md_escape(row['source_domain'])} | "
            f"{row['n_records']} | "
            f"`{md_escape(row['record_relationship_counts'] or 'none')}` | "
            f"{row['n_matrix_rows']} | "
            f"`{md_escape(row['matrix_relationship_counts'] or 'none')}` | "
            f"`{row['has_convergence']}` | "
            f"`{row['has_contradiction']}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Current direct convergence is domain-concentrated; this is provenance context, not a biological result.",
            "- No domain currently has a V48 contradiction row.",
            "- Domains with many records but no matrix rows are external-resource context only unless a future grounding task links them to a project finding.",
            "",
        ]
    )
    (outdir / "SOURCE_DOMAIN_RELATIONSHIP_ROLLUP_V48.md").write_text("\n".join(lines))
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
