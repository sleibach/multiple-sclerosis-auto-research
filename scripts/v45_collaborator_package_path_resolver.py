#!/usr/bin/env python3
"""Resolve concrete artifact paths referenced by the V45 collaborator package.

This is infrastructure governance only. It checks that collaborator-facing
README and manifest references still point to files in the repository. It
ignores placeholders such as ``<cohort>`` because those are operator examples,
not committed artifacts.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_collaborator_path_resolver"
DEFAULT_SOURCES = [
    ROOT / "docs/validation/COLLABORATOR_VALIDATION_PACKAGE_README_V45.md",
    ROOT / "docs/validation/AUTHOR_RUN_PACKET_BUNDLE_INDEX_V45.md",
    ROOT / "analysis/v45_collaborator_package/collaborator_package_manifest.tsv",
    ROOT / "analysis/v45_author_run_packet_bundle/author_run_packet_bundle_index.tsv",
]

PATH_RE = re.compile(r"(?<![A-Za-z0-9_./-])((?:docs|analysis|scripts|meta)/(?:[A-Za-z0-9_./-]+))(?![A-Za-z0-9_./-])")
TRAILING = ".,;:)"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    check = sub.add_parser("check")
    check.add_argument("--source", type=Path, action="append", help="Markdown/TSV source to inspect. Repeatable.")
    check.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    check.add_argument("--fail-on-missing", action="store_true")

    syn = sub.add_parser("synthetic-check")
    syn.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def clean_reference(value: str) -> str:
    return value.strip().strip("`'\"").rstrip(TRAILING)


def ignored_reason(reference: str) -> str:
    if any(char in reference for char in "<>{}*"):
        return "placeholder_or_glob"
    if reference.endswith("/"):
        return "directory_example"
    return ""


def extract_paths_from_text(text: str) -> list[str]:
    paths: set[str] = set()
    for match in PATH_RE.finditer(text):
        paths.add(clean_reference(match.group(1)))
    return sorted(paths)


def extract_paths(source: Path) -> list[dict[str, str]]:
    text = source.read_text(errors="ignore")
    references = extract_paths_from_text(text)
    rows: list[dict[str, str]] = []
    for reference in references:
        rows.append(
            {
                "source": rel(source),
                "reference": reference,
                "ignored_reason": ignored_reason(reference),
            }
        )
    if source.suffix.lower() == ".tsv":
        with source.open(newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row_number, record in enumerate(reader, start=2):
                for column, value in record.items():
                    for reference in extract_paths_from_text(value or ""):
                        rows.append(
                            {
                                "source": rel(source),
                                "reference": reference,
                                "ignored_reason": ignored_reason(reference),
                                "tsv_row": str(row_number),
                                "tsv_column": column,
                            }
                        )
    return rows


def dedupe(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str, str, str, str]] = set()
    out: list[dict[str, str]] = []
    for row in rows:
        key = (
            row.get("source", ""),
            row.get("reference", ""),
            row.get("ignored_reason", ""),
            row.get("tsv_row", ""),
            row.get("tsv_column", ""),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def run_check(sources: list[Path], outdir: Path, fail_on_missing: bool) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    for source in sources:
        source_path = resolve(source)
        if not source_path.exists():
            rows.append(
                {
                    "source": rel(source_path),
                    "reference": rel(source_path),
                    "ignored_reason": "",
                    "exists": "no",
                    "status": "MISSING_SOURCE",
                }
            )
            continue
        rows.extend(extract_paths(source_path))
    rows = dedupe(rows)

    resolved: list[dict[str, str]] = []
    for row in rows:
        reference = row["reference"]
        ignore = row.get("ignored_reason", "")
        exists = bool(ignore) or (ROOT / reference).exists()
        status = "IGNORED" if ignore else ("PASS" if exists else "MISSING")
        resolved.append(
            {
                "source": row.get("source", ""),
                "reference": reference,
                "tsv_row": row.get("tsv_row", ""),
                "tsv_column": row.get("tsv_column", ""),
                "ignored_reason": ignore,
                "exists": "yes" if exists and not ignore else ("ignored" if ignore else "no"),
                "status": status,
            }
        )

    out_path = outdir / "collaborator_package_path_resolution.tsv"
    with out_path.open("w", newline="") as handle:
        fieldnames = ["source", "reference", "tsv_row", "tsv_column", "ignored_reason", "exists", "status"]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(resolved)

    n_missing = sum(1 for row in resolved if row["status"] in {"MISSING", "MISSING_SOURCE"})
    n_pass = sum(1 for row in resolved if row["status"] == "PASS")
    n_ignored = sum(1 for row in resolved if row["status"] == "IGNORED")
    summary = {
        "synthetic": "synthetic" in rel(outdir).lower(),
        "purpose": "collaborator package path resolution; no biological claim",
        "sources": [rel(resolve(source)) for source in sources],
        "resolution_table": rel(out_path),
        "n_references": len(resolved),
        "n_pass": n_pass,
        "n_missing": n_missing,
        "n_ignored_placeholders": n_ignored,
        "overall_status": "PASS" if n_missing == 0 else "FAIL",
    }
    (outdir / "collaborator_package_path_resolution_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if fail_on_missing and n_missing else 0


def synthetic_check(outdir: Path) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    broken = outdir / "synthetic_broken_readme.md"
    broken.write_text(
        "# Synthetic Broken Collaborator README\n\n"
        "synthetic: true\n\n"
        "Good link: `docs/validation/COLLABORATOR_VALIDATION_PACKAGE_README_V45.md`\n\n"
        "Missing link: `docs/validation/DOES_NOT_EXIST_SYNTHETIC_V45.md`\n\n"
        "Placeholder ignored: `docs/validation/outbound_requests/<cohort>_sent_YYYY-MM-DD.md`\n"
    )
    live_rc = run_check(DEFAULT_SOURCES, outdir / "live_sources", True)
    broken_rc = run_check([broken], outdir / "synthetic_broken_source", False)
    broken_summary = json.loads((outdir / "synthetic_broken_source/collaborator_package_path_resolution_summary.json").read_text())
    live_summary = json.loads((outdir / "live_sources/collaborator_package_path_resolution_summary.json").read_text())
    summary = {
        "synthetic": True,
        "purpose": "path resolver positive/negative regression; no biological claim",
        "live_sources_status": live_summary["overall_status"],
        "live_sources_missing": live_summary["n_missing"],
        "synthetic_broken_status": broken_summary["overall_status"],
        "synthetic_broken_missing": broken_summary["n_missing"],
        "synthetic_broken_ignored_placeholders": broken_summary["n_ignored_placeholders"],
        "live_exit_code": live_rc,
        "synthetic_broken_exit_code_without_fail_on_missing": broken_rc,
    }
    (outdir / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return live_rc


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(resolve(args.outdir))
    sources = [resolve(path) for path in args.source] if args.source else DEFAULT_SOURCES
    return run_check(sources, resolve(args.outdir), args.fail_on_missing)


if __name__ == "__main__":
    raise SystemExit(main())
