#!/usr/bin/env python3
"""Build a source URL duplicate/canonicalization review for external records."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_DIRS = [
    ROOT / "knowledge_external/records",
    ROOT / "knowledge_external/catalogs/resources",
]
OUTDIR = ROOT / "knowledge_external/catalogs/indexes"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=OUTDIR)
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_record(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text())
    return data if isinstance(data, dict) else {}


def record_paths() -> list[Path]:
    paths: list[Path] = []
    for base in EXTERNAL_DIRS:
        if base.exists():
            paths.extend(path for path in base.rglob("*.json") if not path.name.endswith(".schema.json"))
    return sorted(paths)


def source_url(data: dict[str, object]) -> str:
    source = data.get("source")
    if isinstance(source, dict):
        return str(source.get("url", "")).strip()
    return ""


def canonical_url(url: str) -> str:
    if not url:
        return ""
    parts = urlsplit(url)
    scheme = parts.scheme.lower() or "https"
    netloc = parts.netloc.lower()
    path = parts.path.rstrip("/") or "/"
    query = urlencode(sorted(parse_qsl(parts.query, keep_blank_values=True)))
    return urlunsplit((scheme, netloc, path, query, ""))


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build(outdir: Path) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for path in record_paths():
        data = read_record(path)
        url = source_url(data)
        canonical = canonical_url(url)
        rows.append(
            {
                "record_id": data.get("record_id", ""),
                "record_type": data.get("record_type", ""),
                "epistemic_class": data.get("epistemic_class", ""),
                "source_url": url,
                "canonical_url": canonical,
                "record_path": rel(path),
                "not_project_grounded_marker": data.get("not_project_grounded_marker", ""),
            }
        )
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[str(row["canonical_url"])].append(row)
    review_rows: list[dict[str, object]] = []
    for canonical, grouped in sorted(groups.items()):
        if len(grouped) < 2:
            continue
        record_ids = ";".join(str(row["record_id"]) for row in grouped)
        paths = ";".join(str(row["record_path"]) for row in grouped)
        review_rows.append(
            {
                "canonical_url": canonical,
                "n_records": len(grouped),
                "record_ids": record_ids,
                "record_paths": paths,
                "review_reason": "Multiple external records cite the same canonical source URL; verify this is intentional and source terms are reviewed once per source.",
                "boundary": "source URL maintenance only; duplicate source URLs are not claim corroboration.",
            }
        )
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(
        outdir / "source_url_duplicate_review_v48.tsv",
        review_rows,
        ["canonical_url", "n_records", "record_ids", "record_paths", "review_reason", "boundary"],
    )
    n_missing_url = sum(1 for row in rows if not row["source_url"])
    n_missing_marker = sum(1 for row in rows if row["not_project_grounded_marker"] != "NOT_PROJECT_GROUNDED")
    summary = {
        "purpose": "V48 source URL duplicate/canonicalization review; source maintenance only; no claim validation",
        "n_external_records": len(rows),
        "n_missing_source_urls": n_missing_url,
        "n_missing_not_project_grounded_markers": n_missing_marker,
        "n_duplicate_canonical_urls": len(review_rows),
        "overall_status": "PASS" if n_missing_url == 0 and n_missing_marker == 0 else "FAIL",
        "markdown": "knowledge_external/catalogs/indexes/SOURCE_URL_DUPLICATE_REVIEW_V48.md",
        "tsv": "knowledge_external/catalogs/indexes/source_url_duplicate_review_v48.tsv",
    }
    (outdir / "source_url_duplicate_review_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Source URL Duplicate Review",
        "",
        "Status: source-maintenance only. Duplicate source URLs are not evidence of independent corroboration.",
        "",
        f"- external records checked: `{summary['n_external_records']}`",
        f"- missing source URLs: `{summary['n_missing_source_urls']}`",
        f"- duplicate canonical URLs: `{summary['n_duplicate_canonical_urls']}`",
        "",
        "## Duplicate Canonical URLs",
        "",
        "| canonical URL | records | record IDs | review reason |",
        "|---|---:|---|---|",
    ]
    if review_rows:
        for row in review_rows:
            lines.append(
                "| "
                f"{md_escape(row['canonical_url'])} | "
                f"{row['n_records']} | "
                f"{md_escape(row['record_ids'])} | "
                f"{md_escape(row['review_reason'])} |"
            )
    else:
        lines.append("| none | 0 | none | no duplicate canonical source URLs detected |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This review only identifies source URL reuse and canonicalization targets.",
            "- A repeated URL does not increase evidence strength; it usually means records share the same source.",
            "- External records remain segregated in the external knowledge layer.",
            "",
        ]
    )
    (outdir / "SOURCE_URL_DUPLICATE_REVIEW_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    summary = build(args.outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
