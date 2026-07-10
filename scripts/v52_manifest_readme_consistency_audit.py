#!/usr/bin/env python3
"""Audit V52 package manifest, README, quickstart, and handoff consistency."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v52_manifest_readme_consistency_audit/manifest_readme_consistency_audit.tsv"
CLASSIFIER = ROOT / "docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv"
TEMPLATE = ROOT / "docs/validation/INCOMING_PACKAGE_MANIFEST_TEMPLATE_V52.tsv"
DATA_OWNER_README = ROOT / "docs/validation/DATA_OWNER_PACKAGE_README_V52.md"
QUICKSTART = ROOT / "docs/validation/PACKAGE_INTAKE_OPERATOR_QUICKSTART_V52.md"
HANDOFF = ROOT / "docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md"

EXPECTED_TEMPLATE_COLUMNS = {
    "package_id",
    "expected_route",
    "provided_fields",
    "data_owner_contact",
    "allowed_use_summary",
    "package_type_signal",
    "subject_level_data_available",
    "aggregate_only",
    "expected_files",
    "expected_total_size_mb",
    "restricted_content_present",
    "notes",
}

README_ROUTE_PHRASES = {
    "monitoring_validation": "paired DMF-like PBMC response",
    "chr1_target_resolution": "chr1 genotype-linked",
    "chr1_modality_workup": "chr1 direction-matched perturbation",
    "postpartum_secondary_biology": "postpartum MS relapse-window data",
    "TB_secondary_monitoring": "T/B compartment data",
    "pharmacodynamic_context_only": "treatment-timed expression",
    "structure_context_only": "protein structure",
    "access_or_terms_blocked": "access-blocked",
    "metadata_only_or_aggregate_only": "aggregate paper table or plot",
}

QUICKSTART_REFERENCES = [
    "scripts/v52_validate_package_id.py",
    "docs/validation/PACKAGE_CHECKSUM_INTAKE_CHECKLIST_V52.md",
    "docs/validation/INCOMING_PACKAGE_MANIFEST_TEMPLATE_V52.tsv",
    "scripts/v52_package_route_classifier.py",
    "docs/validation/PACKAGE_ROUTE_CLASSIFIER_STATUS_DECISION_TABLE_V52.tsv",
    "scripts/v52_received_intake_safety_audit.py",
    "docs/validation/RECEIPT_BLOCKER_TEMPLATE_V52.md",
]

HANDOFF_REFERENCES = [
    "docs/validation/PACKAGE_INTAKE_OPERATOR_QUICKSTART_V52.md",
    "analysis/received_package_intake/README.md",
    "docs/validation/INCOMING_PACKAGE_MANIFEST_TEMPLATE_V52.tsv",
    "docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv",
    "docs/validation/VALIDATION_PACKAGE_FIELD_DICTIONARY_V52.tsv",
    "docs/validation/RECEIVED_PACKAGE_INTAKE_SAFETY_AUDIT_V52.md",
]


def add(rows: list[dict[str, str]], check: str, status: str, detail: str) -> None:
    rows.append({"check": check, "status": status, "detail": detail})


def read_text(path: Path) -> str:
    return path.read_text(errors="replace")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    classifier_rows = list(csv.DictReader(CLASSIFIER.open(), delimiter="\t"))
    route_classes = {row["route_class"] for row in classifier_rows}

    template_headers = next(csv.reader(TEMPLATE.open(), delimiter="\t"))
    missing_template = sorted(EXPECTED_TEMPLATE_COLUMNS - set(template_headers))
    extra_template = sorted(set(template_headers) - EXPECTED_TEMPLATE_COLUMNS)
    add(
        rows,
        "manifest_template_columns",
        "PASS" if not missing_template and not extra_template else "FAIL",
        f"missing={';'.join(missing_template)}; extra={';'.join(extra_template)}",
    )

    readme_text = read_text(DATA_OWNER_README)
    for route, phrase in README_ROUTE_PHRASES.items():
        status = "PASS" if route in route_classes and phrase in readme_text else "FAIL"
        add(rows, f"data_owner_readme_phrase_for_{route}", status, phrase)

    quickstart_text = read_text(QUICKSTART)
    for ref in QUICKSTART_REFERENCES:
        add(
            rows,
            f"quickstart_reference_{ref}",
            "PASS" if ref in quickstart_text else "FAIL",
            ref,
        )

    handoff_text = read_text(HANDOFF)
    for ref in HANDOFF_REFERENCES:
        add(
            rows,
            f"handoff_reference_{ref}",
            "PASS" if ref in handoff_text else "FAIL",
            ref,
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "status", "detail"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    failures = [row for row in rows if row["status"] != "PASS"]
    print({"checks": len(rows), "failures": len(failures), "out": str(args.out)})
    if failures and args.fail_on_error:
        raise SystemExit({"failures": failures})


if __name__ == "__main__":
    main()
