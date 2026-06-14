#!/usr/bin/env python3
"""Generate a prioritized review queue for missing source_terms metadata."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COVERAGE = ROOT / "knowledge_external/catalogs/indexes/source_terms_coverage_v48.tsv"
DEFAULT_DOMAIN_REVIEW = ROOT / "knowledge_external/catalogs/indexes/source_domain_review_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/catalogs/indexes"


HIGH_CLASSES = {
    "controlled_access_biomedical_archive",
    "mixed_commercial_or_registration_access",
    "application_or_registry_access",
    "registration_or_catalog_access",
    "manual_review_domain",
    "publisher_literature",
}
MEDIUM_CLASSES = {
    "public_or_controlled_biomedical_database",
    "public_biomedical_database",
    "public_database_catalog",
    "public_repository",
    "repository_platform",
    "public_target_platform_docs",
    "public_clinical_registry",
    "public_clinical_data_standard",
    "public_clinical_guideline",
    "public_regulatory_medicine_reference",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    parser.add_argument("--domain-review", type=Path, default=DEFAULT_DOMAIN_REVIEW)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def priority_for(review_class: str, record_type: str) -> tuple[str, str]:
    if review_class in HIGH_CLASSES:
        return "high", "controlled/commercial/manual/publisher terms can materially constrain reuse"
    if review_class in MEDIUM_CLASSES:
        return "medium", "public source but terms should be checked before data/text reuse"
    if record_type == "external_claim":
        return "medium", "claim-level source should keep citation and reuse caveats explicit"
    return "low", "lower-risk public context source; metadata-only cataloging remains conservative"


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def build(coverage_path: Path, domain_review_path: Path, outdir: Path) -> dict[str, object]:
    coverage = read_tsv(coverage_path)
    domain_review = {row.get("record_id", ""): row for row in read_tsv(domain_review_path)}
    rows: list[dict[str, object]] = []
    for row in coverage:
        if row.get("source_terms_status") != "missing_optional":
            continue
        review = domain_review.get(row.get("record_id", ""), {})
        review_class = review.get("review_class", "missing_review_class")
        priority, reason = priority_for(review_class, row.get("record_type", ""))
        rows.append(
            {
                "priority": priority,
                "record_id": row.get("record_id", ""),
                "record_type": row.get("record_type", ""),
                "epistemic_class": row.get("epistemic_class", ""),
                "source_domain": row.get("source_domain", ""),
                "review_class": review_class,
                "source_url": row.get("source_url", ""),
                "terms_review_reason": reason,
                "recommended_next_step": "Check source terms URL and add conservative source_terms metadata, or leave missing_optional if terms cannot be stated safely.",
            }
        )
    order = {"high": 0, "medium": 1, "low": 2}
    rows.sort(key=lambda row: (order.get(str(row["priority"]), 9), str(row["source_domain"]), str(row["record_id"])))
    outdir.mkdir(parents=True, exist_ok=True)
    fields = [
        "priority",
        "record_id",
        "record_type",
        "epistemic_class",
        "source_domain",
        "review_class",
        "source_url",
        "terms_review_reason",
        "recommended_next_step",
    ]
    write_tsv(outdir / "source_terms_review_queue_v48.tsv", rows, fields)
    priority_counts = Counter(str(row["priority"]) for row in rows)
    review_class_counts = Counter(str(row["review_class"]) for row in rows)
    summary = {
        "purpose": "V48 source_terms review queue; provenance/navigation only; no claim validation",
        "n_missing_source_terms_records": len(rows),
        "priority_counts": dict(sorted(priority_counts.items())),
        "review_class_counts": dict(sorted(review_class_counts.items())),
        "overall_status": "PASS",
        "markdown": "knowledge_external/catalogs/indexes/SOURCE_TERMS_REVIEW_QUEUE_V48.md",
        "tsv": "knowledge_external/catalogs/indexes/source_terms_review_queue_v48.tsv",
    }
    (outdir / "source_terms_review_queue_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Source-Terms Review Queue",
        "",
        "Status: provenance/navigation only. Missing source_terms metadata is a review target, not a claim-validity failure.",
        "",
        f"- missing source_terms records: `{summary['n_missing_source_terms_records']}`",
        "",
        "## Priority Counts",
        "",
        "| priority | count |",
        "|---|---:|",
    ]
    for key, value in sorted(priority_counts.items(), key=lambda kv: order.get(kv[0], 9)):
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "## Queue",
            "",
            "| priority | record | type | domain | review class | source | reason |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            f"`{md_escape(row['priority'])}` | "
            f"`{md_escape(row['record_id'])}` | "
            f"`{md_escape(row['record_type'])}` | "
            f"{md_escape(row['source_domain'])} | "
            f"`{md_escape(row['review_class'])}` | "
            f"{md_escape(row['source_url'])} | "
            f"{md_escape(row['terms_review_reason'])} |"
        )
    lines.extend(
        [
            "",
            "## Use",
            "",
            "- Add `source_terms` only where the terms can be stated conservatively and sourced.",
            "- Leave records as `missing_optional` where terms are ambiguous; ambiguity is safer than false reuse permission.",
            "- This queue does not authorize redistribution and does not validate source claims.",
            "",
        ]
    )
    (outdir / "SOURCE_TERMS_REVIEW_QUEUE_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    summary = build(args.coverage, args.domain_review, args.outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
