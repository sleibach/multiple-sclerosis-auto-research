#!/usr/bin/env python3
"""Audit V55 heading hierarchy and table semantics.

This is an accessibility-maintenance check. It does not validate scientific
content or measure human comprehension.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis" / "v55_semantic_structure_audit"
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")


@dataclass(frozen=True)
class Heading:
    line: int
    level: int
    text: str


class SemanticHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.line = 1
        self.headings: list[Heading] = []
        self._heading_level: int | None = None
        self._heading_line = 0
        self._heading_parts: list[str] = []
        self.tables: list[dict[str, object]] = []
        self._table: dict[str, object] | None = None
        self._row_has_header = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.line = self.getpos()[0]
        if re.fullmatch(r"h[1-6]", tag):
            self._heading_level = int(tag[1])
            self._heading_line = self.line
            self._heading_parts = []
        elif tag == "table":
            self._table = {"line": self.line, "rows": 0, "header_rows": 0}
        elif tag == "tr" and self._table is not None:
            self._row_has_header = False
        elif tag == "th" and self._table is not None:
            self._row_has_header = True

    def handle_endtag(self, tag: str) -> None:
        if re.fullmatch(r"h[1-6]", tag) and self._heading_level is not None:
            text = " ".join("".join(self._heading_parts).split())
            self.headings.append(Heading(self._heading_line, self._heading_level, text))
            self._heading_level = None
        elif tag == "tr" and self._table is not None:
            self._table["rows"] = int(self._table["rows"]) + 1
            if self._row_has_header:
                self._table["header_rows"] = int(self._table["header_rows"]) + 1
        elif tag == "table" and self._table is not None:
            self.tables.append(self._table)
            self._table = None

    def handle_data(self, data: str) -> None:
        if self._heading_level is not None:
            self._heading_parts.append(data)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def public_documents() -> list[Path]:
    paths = [ROOT / "README.md", ROOT / "CONTRIBUTING.md"]
    paths.extend(sorted((ROOT / "docs" / "onboarding").glob("*.md")))
    paths.extend(sorted((ROOT / "docs" / "onboarding").glob("*.html")))
    return [path for path in paths if path.is_file()]


def without_fenced_code(lines: list[str]) -> list[str]:
    visible: list[str] = []
    fence: str | None = None
    for line in lines:
        marker = line.lstrip()[:3]
        if marker in {"```", "~~~"}:
            fence = None if fence == marker else marker if fence is None else fence
            visible.append("")
        elif fence is None:
            visible.append(line)
        else:
            visible.append("")
    return visible


def normalize_heading(text: str) -> str:
    text = re.sub(r"\[([^]]+)]\([^)]*\)", r"\1", text)
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def markdown_headings(lines: list[str]) -> list[Heading]:
    result: list[Heading] = []
    for index, line in enumerate(without_fenced_code(lines), start=1):
        match = HEADING_RE.match(line)
        if match:
            result.append(Heading(index, len(match.group(1)), match.group(2).strip()))
    return result


def split_table_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [cell.replace(r"\|", "|").strip() for cell in re.split(r"(?<!\\)\|", body)]


def markdown_tables(lines: list[str]) -> list[dict[str, object]]:
    visible = without_fenced_code(lines)
    tables: list[dict[str, object]] = []
    index = 0
    while index < len(visible):
        if not visible[index].lstrip().startswith("|"):
            index += 1
            continue
        start = index
        block: list[str] = []
        while index < len(visible) and visible[index].lstrip().startswith("|"):
            block.append(visible[index])
            index += 1
        if len(block) >= 2:
            tables.append({"line": start + 1, "rows": [split_table_row(row) for row in block]})
    return tables


def add_check(
    rows: list[dict[str, object]], path: Path, line: int, check: str, passed: bool, detail: str
) -> None:
    rows.append(
        {
            "path": str(path.relative_to(ROOT)),
            "line": line,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
    )


def audit_headings(path: Path, headings: list[Heading], rows: list[dict[str, object]]) -> None:
    h1_count = sum(heading.level == 1 for heading in headings)
    add_check(rows, path, headings[0].line if headings else 1, "one_h1", h1_count == 1, f"h1_count={h1_count}")
    add_check(
        rows,
        path,
        headings[0].line if headings else 1,
        "first_heading_h1",
        bool(headings) and headings[0].level == 1,
        "no headings" if not headings else f"first_level={headings[0].level}",
    )
    for previous, current in zip(headings, headings[1:]):
        passed = current.level <= previous.level + 1
        add_check(
            rows,
            path,
            current.line,
            "heading_level_step",
            passed,
            f"previous=h{previous.level} current=h{current.level} text={current.text}",
        )
    normalized = [normalize_heading(heading.text) for heading in headings]
    repeated_labels = {name for name, count in Counter(normalized).items() if name and count > 1}

    # A repeated leaf label can be useful in a templated document when its
    # named parent is different. Fail only when the complete heading path is
    # duplicated, which is the ambiguous anchor/navigation case.
    stack: dict[int, str] = {}
    heading_paths: list[tuple[str, ...]] = []
    for heading, name in zip(headings, normalized):
        stack = {level: value for level, value in stack.items() if level < heading.level}
        stack[heading.level] = name
        heading_paths.append(tuple(stack[level] for level in sorted(stack)))
    duplicate_paths = {
        heading_path for heading_path, count in Counter(heading_paths).items() if heading_path and count > 1
    }
    for heading, heading_path in zip(headings, heading_paths):
        if heading_path in duplicate_paths:
            add_check(
                rows,
                path,
                heading.line,
                "unique_heading_path",
                False,
                f"duplicate_path={' > '.join(heading_path)}",
            )
    if not duplicate_paths:
        add_check(
            rows,
            path,
            headings[0].line if headings else 1,
            "unique_heading_paths",
            True,
            "no duplicate full heading paths",
        )
    if repeated_labels:
        repeated_instances = sum(normalized.count(label) for label in repeated_labels)
        add_check(
            rows,
            path,
            headings[0].line if headings else 1,
            "contextual_repeated_heading_labels",
            not duplicate_paths,
            f"labels={len(repeated_labels)} instances={repeated_instances} full_paths_unique={not duplicate_paths}",
        )


def audit_markdown(path: Path, rows: list[dict[str, object]]) -> tuple[int, int]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    headings = markdown_headings(lines)
    audit_headings(path, headings, rows)
    tables = markdown_tables(lines)
    for table in tables:
        table_rows = table["rows"]
        assert isinstance(table_rows, list)
        header = table_rows[0]
        separator = table_rows[1]
        add_check(rows, path, int(table["line"]), "table_header_nonempty", all(header), f"columns={len(header)}")
        separator_ok = len(separator) == len(header) and all(SEPARATOR_RE.fullmatch(cell) for cell in separator)
        add_check(rows, path, int(table["line"]) + 1, "table_header_separator", separator_ok, f"header={len(header)} separator={len(separator)}")
        for offset, data_row in enumerate(table_rows[2:], start=2):
            add_check(
                rows,
                path,
                int(table["line"]) + offset,
                "table_column_count",
                len(data_row) == len(header),
                f"expected={len(header)} actual={len(data_row)}",
            )
    return len(headings), len(tables)


def audit_html(path: Path, rows: list[dict[str, object]]) -> tuple[int, int]:
    parser = SemanticHTMLParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    audit_headings(path, parser.headings, rows)
    for table in parser.tables:
        has_header = int(table["header_rows"]) > 0
        add_check(
            rows,
            path,
            int(table["line"]),
            "html_table_has_header_cells",
            has_header,
            f"rows={table['rows']} header_rows={table['header_rows']}",
        )
    return len(parser.headings), len(parser.tables)


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    n_headings = 0
    n_tables = 0
    documents = public_documents()
    for path in documents:
        if path.suffix == ".html":
            headings, tables = audit_html(path, rows)
        else:
            headings, tables = audit_markdown(path, rows)
        n_headings += headings
        n_tables += tables

    checks_path = outdir / "semantic_structure_checks.tsv"
    with checks_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("path", "line", "check", "status", "detail"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    failures = [row for row in rows if row["status"] == "FAIL"]
    summary = {
        "purpose": "V55 heading/table semantic audit; no scientific claim",
        "n_documents": len(documents),
        "n_headings": n_headings,
        "n_tables": n_tables,
        "n_checks": len(rows),
        "n_fail": len(failures),
        "overall_status": "PASS" if not failures else "FAIL",
        "checks": str(checks_path.relative_to(ROOT)),
        "interpretation": "Structural accessibility checks only; not evidence of comprehension or scientific validity.",
    }
    summary_path = outdir / "semantic_structure_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 1 if args.fail_on_error and failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
