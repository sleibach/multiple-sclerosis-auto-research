#!/usr/bin/env python3
"""Build a machine-readable V50 negative / near-miss source-search index.

This is a navigation and provenance artifact only. It reads committed V50
metadata-search QA outputs and writes a compact table that future cohort scouts
can use to avoid recounting duplicate, context-only, partial, or false-positive
source hits as independent validation cohorts.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v50_source_hit_independence_qa/source_hit_independence_qa.tsv"
OUTDIR = ROOT / "analysis/v50_negative_source_search_index"
OUTPUT = OUTDIR / "negative_near_miss_index.tsv"
SUMMARY = OUTDIR / "summary.json"


def source_search_family(route: str) -> str:
    if route == "BioStudies":
        return "task74_biostudies_arrayexpress_metadata_search"
    if route == "Europe PMC":
        return "task68_europepmc_metadata_search"
    if route == "NCBI GDS":
        return "task68_ncbi_gds_metadata_search"
    return "unknown_v50_metadata_search"


def same_definition_gate_status(safe_use: str) -> str:
    if safe_use == "partial_hit_metadata_only":
        return "not_satisfied_metadata_partial"
    if safe_use == "context_only":
        return "not_satisfied_context_only"
    if safe_use == "reject_false_positive":
        return "not_applicable_false_positive"
    return "not_satisfied"


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    checked_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with INPUT.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    fieldnames = [
        "index_date_utc",
        "hit_id",
        "title",
        "route",
        "locator",
        "canonical_cluster",
        "cluster_status",
        "safe_use",
        "same_definition_gate_status",
        "independent_source_count_allowed",
        "exact_validation_candidate",
        "no_recount_without_new_same_definition_package",
        "source_search_family",
        "open_gwas_used",
        "reason",
        "source_qa_input",
    ]

    output_rows: list[dict[str, str]] = []
    for row in rows:
        safe_use = row["safe_use"]
        output_rows.append(
            {
                "index_date_utc": checked_utc,
                "hit_id": row["hit_id"],
                "title": row["title"],
                "route": row["route"],
                "locator": row["locator"],
                "canonical_cluster": row["canonical_cluster"],
                "cluster_status": row["cluster_status"],
                "safe_use": safe_use,
                "same_definition_gate_status": same_definition_gate_status(safe_use),
                "independent_source_count_allowed": row["independent_source_count_allowed"],
                "exact_validation_candidate": "false",
                "no_recount_without_new_same_definition_package": "true",
                "source_search_family": source_search_family(row["route"]),
                "open_gwas_used": "false",
                "reason": row["reason"],
                "source_qa_input": str(INPUT.relative_to(ROOT)),
            }
        )

    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(output_rows)

    safe_counts = Counter(row["safe_use"] for row in output_rows)
    cluster_counts = Counter(row["canonical_cluster"] for row in output_rows)
    summary = {
        "checked_utc": checked_utc,
        "input": str(INPUT.relative_to(ROOT)),
        "output": str(OUTPUT.relative_to(ROOT)),
        "purpose": (
            "V50 machine-readable negative/near-miss source-search index; "
            "navigation only; no biological claim"
        ),
        "rows_indexed": len(output_rows),
        "exact_validation_candidates": 0,
        "independent_source_count_allowed": 0,
        "safe_use_counts": dict(sorted(safe_counts.items())),
        "canonical_clusters": dict(sorted(cluster_counts.items())),
        "open_gwas_used": False,
        "synthetic": False,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
