#!/usr/bin/env python3
"""Flag source-search hits that must not be recounted as independent cohorts."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "analysis/v50_negative_source_search_index/negative_near_miss_index.tsv"
DEFAULT_INPUT = DEFAULT_INDEX
DEFAULT_OUTDIR = ROOT / "analysis/v50_source_hit_recount_checker"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def key_values(row: dict[str, str], fields: tuple[str, ...]) -> set[str]:
    values: set[str] = set()
    for field in fields:
        value = row.get(field, "").strip()
        if value:
            values.add(value)
    return values


def build_blocklist(index_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    blocklist: dict[str, dict[str, str]] = {}
    for row in index_rows:
        for key in key_values(row, ("hit_id", "locator", "canonical_cluster")):
            blocklist[key] = row
    return blocklist


def classify_row(row: dict[str, str], blocklist: dict[str, dict[str, str]]) -> tuple[str, dict[str, str] | None, str]:
    for field in ("hit_id", "locator", "canonical_cluster"):
        value = row.get(field, "").strip()
        if value and value in blocklist:
            return "BLOCK_RECOUNT", blocklist[value], field
    return "PASS_NEW_OR_UNINDEXED", None, ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Candidate/source-hit TSV to audit.")
    parser.add_argument("--index", default=str(DEFAULT_INDEX), help="Machine-readable no-recount TSV.")
    parser.add_argument("--outdir", default=str(DEFAULT_OUTDIR), help="Output directory.")
    parser.add_argument("--fail-on-recount", action="store_true", help="Exit non-zero when blocked rows are found.")
    args = parser.parse_args()

    input_path = Path(args.input)
    index_path = Path(args.index)
    outdir = Path(args.outdir)
    if not input_path.is_absolute():
        input_path = ROOT / input_path
    if not index_path.is_absolute():
        index_path = ROOT / index_path
    if not outdir.is_absolute():
        outdir = ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)

    checked_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    index_rows = read_tsv(index_path)
    input_rows = read_tsv(input_path)
    blocklist = build_blocklist(index_rows)

    output = outdir / "source_hit_recount_flags.tsv"
    fieldnames = [
        "checked_utc",
        "row_number",
        "status",
        "matched_on",
        "input_hit_id",
        "input_locator",
        "input_canonical_cluster",
        "blocked_hit_id",
        "blocked_canonical_cluster",
        "blocked_safe_use",
        "blocked_reason",
        "open_gwas_used",
    ]
    output_rows: list[dict[str, str]] = []
    for idx, row in enumerate(input_rows, start=1):
        status, match, matched_on = classify_row(row, blocklist)
        output_rows.append(
            {
                "checked_utc": checked_utc,
                "row_number": str(idx),
                "status": status,
                "matched_on": matched_on,
                "input_hit_id": row.get("hit_id", ""),
                "input_locator": row.get("locator", ""),
                "input_canonical_cluster": row.get("canonical_cluster", ""),
                "blocked_hit_id": match.get("hit_id", "") if match else "",
                "blocked_canonical_cluster": match.get("canonical_cluster", "") if match else "",
                "blocked_safe_use": match.get("safe_use", "") if match else "",
                "blocked_reason": match.get("reason", "") if match else "",
                "open_gwas_used": "false",
            }
        )

    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(output_rows)

    counts = Counter(row["status"] for row in output_rows)
    summary = {
        "checked_utc": checked_utc,
        "input": str(input_path.relative_to(ROOT)),
        "index": str(index_path.relative_to(ROOT)),
        "output": str(output.relative_to(ROOT)),
        "purpose": "V50 source-hit no-recount checker; navigation only; no biological claim",
        "rows_checked": len(output_rows),
        "blocked_recount_rows": counts.get("BLOCK_RECOUNT", 0),
        "pass_new_or_unindexed_rows": counts.get("PASS_NEW_OR_UNINDEXED", 0),
        "open_gwas_used": False,
        "synthetic": False,
    }
    (outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_recount and summary["blocked_recount_rows"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
