#!/usr/bin/env python3
"""Generate V48 source-terms metadata coverage report for external records.

This is provenance/navigation infrastructure only. It does not validate any
external claim and does not convert external knowledge into project-grounded
evidence.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = ROOT / "knowledge_external"
OUTDIR = EXTERNAL_ROOT / "catalogs/indexes"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    return parser.parse_args()


def record_paths(root: Path) -> list[Path]:
    base = root / "knowledge_external"
    paths: list[Path] = []
    for subdir in ["records", "catalogs/resources"]:
        path = base / subdir
        if path.exists():
            paths.extend(p for p in path.rglob("*.json") if not p.name.endswith(".schema.json"))
    return sorted(paths)


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def source_url(data: dict[str, object]) -> str:
    source = data.get("source")
    if isinstance(source, dict):
        return str(source.get("url", "")).strip()
    if isinstance(source, str):
        return source.strip()
    return ""


def source_label(data: dict[str, object]) -> str:
    source = data.get("source")
    if isinstance(source, dict):
        return str(source.get("label", "")).strip()
    return ""


def domain(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url)
    return parsed.netloc.lower()


def row_for(root: Path, path: Path) -> dict[str, str]:
    data = json.loads(path.read_text())
    terms = data.get("source_terms")
    terms_obj = terms if isinstance(terms, dict) else {}
    url = source_url(data)
    terms_url = str(terms_obj.get("terms_url", "")).strip()
    return {
        "path": rel(root, path),
        "record_id": str(data.get("record_id", "")),
        "record_type": str(data.get("record_type", "")),
        "epistemic_class": str(data.get("epistemic_class", "")),
        "not_project_grounded_marker": str(data.get("not_project_grounded_marker", "")),
        "source_label": source_label(data),
        "source_url": url,
        "source_domain": domain(url),
        "source_terms_status": "present" if terms_obj else "missing_optional",
        "license_or_terms_label": str(terms_obj.get("license_or_terms_label", "")).strip(),
        "terms_url": terms_url,
        "terms_domain": domain(terms_url),
        "checked_date": str(terms_obj.get("checked_date", "")).strip(),
        "redistribution_allowed": str(terms_obj.get("redistribution_allowed", "")).strip(),
        "reuse_notes": str(terms_obj.get("reuse_notes", "")).strip(),
    }


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def count_by(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        key = row.get(field, "") or "missing"
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def write_markdown(root: Path, rows: list[dict[str, str]], summary: dict[str, object]) -> Path:
    path = root / "knowledge_external/catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md"
    lines = [
        "# V48 Source-Terms Coverage",
        "",
        "Status: provenance/navigation only. External records remain `external-unverifiable` or `external-verifiable` as tagged; source-terms metadata is not project-grounded evidence.",
        "",
        f"- records checked: `{summary['n_records']}`",
        f"- records with source_terms: `{summary['n_records_with_source_terms']}`",
        f"- records missing optional source_terms: `{summary['n_records_missing_source_terms']}`",
        f"- NOT project grounded marker: `NOT_PROJECT_GROUNDED`",
        "",
        "## Redistribution Coverage",
        "",
        "| redistribution_allowed | count |",
        "|---|---:|",
    ]
    for key, count in summary["redistribution_counts"].items():  # type: ignore[index, union-attr]
        lines.append(f"| `{md_escape(str(key))}` | {count} |")
    lines.extend(
        [
            "",
            "## Records",
            "",
            "| record | class | source | source_terms | redistribution | checked | terms | marker |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for row in rows:
        source = row["source_url"] or "missing-source"
        terms = row["terms_url"] or "missing-terms-url"
        lines.append(
            "| "
            f"`{md_escape(row['record_id'])}` | "
            f"`{md_escape(row['epistemic_class'])}` | "
            f"{md_escape(source)} | "
            f"`{md_escape(row['source_terms_status'])}` | "
            f"`{md_escape(row['redistribution_allowed'] or 'missing')}` | "
            f"`{md_escape(row['checked_date'] or 'missing')}` | "
            f"{md_escape(terms)} | "
            f"`{md_escape(row['not_project_grounded_marker'])}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `present` means the record has a complete `source_terms` object that passed the V48 linter.",
            "- `missing_optional` is not a failure; it marks a future terms-review target.",
            "- `metadata_only` is the conservative default for external resources unless a future record-specific review justifies more.",
            "- This report does not authorize data redistribution and does not alter any grounded finding, locked rule, or pre-registration.",
            "",
        ]
    )
    path.write_text("\n".join(lines))
    return path


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    rows = [row_for(root, path) for path in record_paths(root)]
    fields = [
        "path",
        "record_id",
        "record_type",
        "epistemic_class",
        "not_project_grounded_marker",
        "source_label",
        "source_url",
        "source_domain",
        "source_terms_status",
        "license_or_terms_label",
        "terms_url",
        "terms_domain",
        "checked_date",
        "redistribution_allowed",
        "reuse_notes",
    ]
    outdir = root / "knowledge_external/catalogs/indexes"
    write_tsv(outdir / "source_terms_coverage_v48.tsv", rows, fields)
    n_with_terms = sum(1 for row in rows if row["source_terms_status"] == "present")
    summary: dict[str, object] = {
        "purpose": "V48 source-terms coverage report; provenance/navigation only; no biological claim",
        "n_records": len(rows),
        "n_records_with_source_terms": n_with_terms,
        "n_records_missing_source_terms": len(rows) - n_with_terms,
        "source_terms_status_counts": count_by(rows, "source_terms_status"),
        "redistribution_counts": count_by(rows, "redistribution_allowed"),
        "source_domain_counts": count_by(rows, "source_domain"),
        "markdown": "knowledge_external/catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md",
        "tsv": "knowledge_external/catalogs/indexes/source_terms_coverage_v48.tsv",
    }
    (outdir / "source_terms_coverage_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_markdown(root, rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
