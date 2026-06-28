#!/usr/bin/env python3
"""Build the V50 BioStudies query reproducibility packet."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode


ROOT = Path(__file__).resolve().parents[1]
INDIR = ROOT / "analysis/v50_biostudies_treatment_response_search"
HITS = INDIR / "biostudies_hits.tsv"
DEDUP = INDIR / "biostudies_hits_dedup.tsv"
MANUAL = INDIR / "candidate_manual_review.tsv"
OUTDIR = ROOT / "analysis/v50_biostudies_query_reproducibility"
QUERIES = OUTDIR / "biostudies_query_packet.tsv"
SUMMARY = OUTDIR / "summary.json"
API = "https://www.ebi.ac.uk/biostudies/api/v1/search"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    checked_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    hits = read_tsv(HITS)
    dedup = read_tsv(DEDUP)
    manual = read_tsv(MANUAL)

    raw_counts = Counter(row["query"] for row in hits)
    dedup_counts = Counter(row["query"] for row in dedup)
    top_accessions: dict[str, list[str]] = defaultdict(list)
    for row in dedup:
        if len(top_accessions[row["query"]]) < 5:
            top_accessions[row["query"]].append(row["accession"])

    manual_by_accession = {row["accession"]: row for row in manual}
    reviewed_by_query: dict[str, list[str]] = defaultdict(list)
    reviewed_status_by_query: dict[str, Counter[str]] = defaultdict(Counter)
    for row in dedup:
        accession = row["accession"]
        if accession in manual_by_accession:
            reviewed_by_query[row["query"]].append(accession)
            reviewed_status_by_query[row["query"]][manual_by_accession[accession]["safe_outcome"]] += 1

    fieldnames = [
        "checked_utc",
        "query",
        "api_url",
        "page_size",
        "raw_hits_recorded",
        "deduplicated_hits_recorded",
        "top_deduplicated_accessions",
        "manual_review_accessions",
        "manual_review_safe_outcome_counts",
        "verified_exact_candidates",
        "open_gwas_used",
        "source_hits_tsv",
        "source_dedup_tsv",
    ]
    rows: list[dict[str, str]] = []
    for query in sorted(raw_counts):
        api_url = f"{API}?{urlencode({'query': query, 'pageSize': '10'})}"
        status_counts = reviewed_status_by_query[query]
        rows.append(
            {
                "checked_utc": checked_utc,
                "query": query,
                "api_url": api_url,
                "page_size": "10",
                "raw_hits_recorded": str(raw_counts[query]),
                "deduplicated_hits_recorded": str(dedup_counts[query]),
                "top_deduplicated_accessions": ";".join(top_accessions[query]),
                "manual_review_accessions": ";".join(reviewed_by_query[query]),
                "manual_review_safe_outcome_counts": json.dumps(dict(sorted(status_counts.items())), sort_keys=True),
                "verified_exact_candidates": "0",
                "open_gwas_used": "false",
                "source_hits_tsv": str(HITS.relative_to(ROOT)),
                "source_dedup_tsv": str(DEDUP.relative_to(ROOT)),
            }
        )

    with QUERIES.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "checked_utc": checked_utc,
        "queries": len(rows),
        "raw_hits_recorded": len(hits),
        "deduplicated_hits_recorded": len(dedup),
        "manual_review_rows": len(manual),
        "verified_exact_candidates": 0,
        "output": str(QUERIES.relative_to(ROOT)),
        "purpose": "V50 BioStudies query reproducibility packet; metadata search navigation only; no biological claim",
        "open_gwas_used": False,
        "synthetic": False,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
