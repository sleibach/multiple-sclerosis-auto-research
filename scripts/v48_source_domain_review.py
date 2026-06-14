#!/usr/bin/env python3
"""Build a V48 source-domain review report for external records."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECORD_ROOT = ROOT / "knowledge_external"
DEFAULT_OUTDIR = ROOT / "knowledge_external/catalogs/indexes"


DOMAIN_CLASSES = [
    ("ncbi.nlm.nih.gov", "public_biomedical_database"),
    ("pubmed.ncbi.nlm.nih.gov", "public_biomedical_database"),
    ("clinicaltrials.gov", "public_clinical_registry"),
    ("ebi.ac.uk", "public_or_controlled_biomedical_database"),
    ("ega-archive.org", "controlled_access_biomedical_archive"),
    ("nature.com", "publisher_literature"),
    ("dailymed.nlm.nih.gov", "public_us_government_drug_label"),
    ("fda.gov", "public_us_government_drug_label"),
    ("ema.europa.eu", "public_regulatory_medicine_reference"),
    ("nice.org.uk", "public_clinical_guideline"),
    ("england.nhs.uk", "public_clinical_guideline"),
    ("nationalmssociety.org", "public_patient_professional_reference"),
    ("mssociety.org.uk", "public_patient_professional_reference"),
    ("commondataelements.ninds.nih.gov", "public_clinical_data_standard"),
    ("msbase.org", "application_or_registry_access"),
    ("narcoms.org", "application_or_registry_access"),
    ("msda.emif-catalogue.eu", "registration_or_catalog_access"),
    ("ngdc.cncb.ac.cn", "public_database_catalog"),
    ("disgenet.com", "mixed_commercial_or_registration_access"),
    ("platform-docs.opentargets.org", "public_target_platform_docs"),
    ("atlasofms.org", "public_epidemiology_reference"),
    ("zenodo.org", "public_repository"),
    ("about.zenodo.org", "public_repository"),
    ("figshare.com", "repository_platform"),
    ("info.figshare.com", "repository_platform"),
    ("datadryad.org", "public_repository"),
    ("cos.io", "repository_platform"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record-root", type=Path, default=DEFAULT_RECORD_ROOT)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def record_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for base in [root / "records", root / "catalogs/resources"]:
        if base.exists():
            paths.extend(path for path in base.rglob("*.json") if not path.name.endswith(".schema.json"))
    return sorted(paths)


def source_url(data: dict) -> str:
    source = data.get("source")
    if not isinstance(source, dict):
        return ""
    return str(source.get("url", "")).strip()


def domain_for_url(url: str) -> str:
    if not url:
        return "NO_URL"
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def review_class(domain: str) -> str:
    for token, label in DOMAIN_CLASSES:
        if domain == token or domain.endswith("." + token):
            return label
    return "manual_review_domain"


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build(record_root: Path, outdir: Path) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for path in record_paths(record_root):
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            continue
        url = source_url(data)
        domain = domain_for_url(url)
        rows.append(
            {
                "domain": domain,
                "review_class": review_class(domain),
                "record_id": data.get("record_id", ""),
                "record_type": data.get("record_type", ""),
                "source_url": url,
                "access_tier": data.get("access_tier", ""),
                "path": str(path.relative_to(ROOT)),
            }
        )
    class_counts = Counter(str(row["review_class"]) for row in rows)
    domain_counts = Counter(str(row["domain"]) for row in rows)
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "source_domain_review_v48.tsv", rows, ["domain", "review_class", "record_id", "record_type", "source_url", "access_tier", "path"])
    write_tsv(
        outdir / "source_domain_review_class_counts_v48.tsv",
        [{"review_class": key, "count": value} for key, value in sorted(class_counts.items())],
        ["review_class", "count"],
    )
    summary = {
        "purpose": "V48 source-domain review; maintenance/navigation only, no biological claim",
        "n_records": len(rows),
        "n_domains": len(domain_counts),
        "n_review_classes": len(class_counts),
        "n_manual_review_domains": sum(1 for row in rows if row["review_class"] == "manual_review_domain"),
        "overall_status": "PASS",
    }
    (outdir / "source_domain_review_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Source-Domain Review",
        "",
        "Status: maintenance/navigation only. This report classifies source domains for future access and terms review; it does not validate source claims.",
        "",
        f"- records reviewed: `{summary['n_records']}`",
        f"- source domains: `{summary['n_domains']}`",
        f"- review classes: `{summary['n_review_classes']}`",
        f"- manual-review domain rows: `{summary['n_manual_review_domains']}`",
        "",
        "## Review Class Counts",
        "",
        "| review class | count |",
        "|---|---:|",
    ]
    for key, value in sorted(class_counts.items()):
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Domains", "", "| domain | review class | records |", "|---|---|---:|"])
    for domain, count in sorted(domain_counts.items()):
        lines.append(f"| {domain} | `{review_class(domain)}` | {count} |")
    (outdir / "SOURCE_DOMAIN_REVIEW_V48.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    summary = build(args.record_root, args.outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
