#!/usr/bin/env python3
"""Lint generated V47 external Markdown indexes for source-bearing rows.

The linter checks generated Markdown tables under ``knowledge_external``. If a
table has a ``source`` column and a row contains an external epistemic class or
NOT_PROJECT_GROUNDED marker, the row must contain a source locator. Aggregate
count tables without a source column are ignored.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v47_external_markdown_index_linter"
EXTERNAL_ROOT = "knowledge_external"
EXTERNAL_MARKERS = ["external-verifiable", "external-unverifiable", "NOT_PROJECT_GROUNDED"]
SOURCE_LOCATOR = re.compile(r"https?://|doi:|pmid", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint real generated external Markdown indexes")
    lint.add_argument("--root", type=Path, default=ROOT)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic Markdown source fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
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


def markdown_paths(root: Path) -> list[Path]:
    base = root / EXTERNAL_ROOT
    if not base.exists():
        return []
    return sorted(path for path in base.rglob("*.md") if "schema" not in path.parts)


def row_has_external_marker(line: str) -> bool:
    return any(marker in line for marker in EXTERNAL_MARKERS)


def lint_markdown(root: Path, path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    rel_path = rel(root, path)
    current_header = ""
    in_source_table = False
    for line_no, line in enumerate(path.read_text(errors="ignore").splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            current_header = ""
            in_source_table = False
            continue
        cells = [cell.strip().lower() for cell in stripped.strip("|").split("|")]
        if "source" in cells:
            current_header = stripped
            in_source_table = True
            continue
        if set(stripped.replace("|", "").replace("-", "").replace(":", "").strip()) == set():
            continue
        if in_source_table and row_has_external_marker(stripped):
            ok = bool(SOURCE_LOCATOR.search(stripped))
            rows.append(
                {
                    "path": rel_path,
                    "line": line_no,
                    "check": "external_row_has_source_locator",
                    "status": "PASS" if ok else "FAIL",
                    "detail": stripped[:240],
                    "header": current_header,
                }
            )
    if not rows:
        rows.append(
            {
                "path": rel_path,
                "line": 0,
                "check": "no_source_table_external_rows",
                "status": "PASS",
                "detail": "No source-bearing external rows found; aggregate-only or structural doc.",
                "header": "not_applicable",
            }
        )
    return rows


def lint_root(root: Path, outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else root / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    paths = markdown_paths(root)
    for path in paths:
        rows.extend(lint_markdown(root, path))
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    write_tsv(outdir / "external_markdown_index_lint.tsv", rows, ["path", "line", "check", "status", "detail", "header"])
    summary = {
        "synthetic": False,
        "purpose": "V47 generated external Markdown source/provenance lint; no biological claim",
        "n_markdown_files": len(paths),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": rel(root, outdir / "external_markdown_index_lint.tsv") if root == ROOT else str(outdir / "external_markdown_index_lint.tsv"),
    }
    (outdir / "external_markdown_index_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def build_synthetic_root(outdir: Path) -> Path:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    indexes = root / EXTERNAL_ROOT / "catalogs/indexes"
    indexes.mkdir(parents=True, exist_ok=True)
    (indexes / "good.md").write_text(
        "\n".join(
            [
                "# Good",
                "",
                "| resource | class | source | marker |",
                "|---|---|---|---|",
                "| Good | `external-unverifiable` | https://example.invalid/source | `NOT_PROJECT_GROUNDED` |",
                "",
                "| field | value | count |",
                "|---|---|---:|",
                "| epistemic_class | external-unverifiable | 1 |",
            ]
        )
        + "\n"
    )
    (indexes / "bad.md").write_text(
        "\n".join(
            [
                "# Bad",
                "",
                "| resource | class | source | marker |",
                "|---|---|---|---|",
                "| Bad | `external-unverifiable` | missing | `NOT_PROJECT_GROUNDED` |",
            ]
        )
        + "\n"
    )
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root = build_synthetic_root(outdir)
    lint_out = outdir / "synthetic_lint"
    lint_root(root, lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "external_markdown_index_lint.tsv").open(), delimiter="\t"))
    checks = {
        "good_row_passes": any(row["path"].endswith("good.md") and row["status"] == "PASS" for row in rows),
        "aggregate_row_ignored": not any(row["path"].endswith("good.md") and "epistemic_class" in row["detail"] and row["status"] == "FAIL" for row in rows),
        "bad_row_fails": any(row["path"].endswith("bad.md") and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_external_markdown_index_lint_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V47 generated external Markdown source/provenance synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_external_markdown_index_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_root(args.root.resolve(), args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
