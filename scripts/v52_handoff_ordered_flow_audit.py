#!/usr/bin/env python3
"""Audit Universal Intake handoff bundle ordering."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md"
DEFAULT_OUT = ROOT / "analysis/v52_handoff_ordered_flow_audit/handoff_ordered_flow_audit.tsv"

EXPECTED_ORDER = [
    ("quickstart", "docs/validation/PACKAGE_INTAKE_OPERATOR_QUICKSTART_V52.md"),
    ("access_terms", "docs/validation/PACKAGE_CHECKSUM_INTAKE_CHECKLIST_V52.md"),
    ("safe_paths", "docs/validation/RECEIVED_PACKAGE_FILE_NAMING_POLICY_V52.md"),
    ("intake_readme", "analysis/received_package_intake/README.md"),
    ("package_id", "docs/validation/PACKAGE_ID_VALIDATION_NOTE_V52.md"),
    ("metadata_policy", "docs/validation/MANIFEST_METADATA_VS_RAW_DATA_GIT_POLICY_V52.md"),
    ("blocker_template", "docs/validation/RECEIPT_BLOCKER_TEMPLATE_V52.md"),
    ("manifest_template", "docs/validation/INCOMING_PACKAGE_MANIFEST_TEMPLATE_V52.tsv"),
    ("preflight", "docs/validation/INCOMING_PACKAGE_PREFLIGHT_CHECKLIST_V52.md"),
    ("route_classifier", "docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv"),
    ("operator_note", "docs/validation/PACKAGE_ROUTE_CLASSIFIER_OPERATOR_NOTE_V52.md"),
    ("decision_table", "docs/validation/PACKAGE_ROUTE_CLASSIFIER_STATUS_DECISION_TABLE_V52.tsv"),
    ("examples", "docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_EXAMPLES_V52.tsv"),
    ("field_dictionary", "docs/validation/VALIDATION_PACKAGE_FIELD_DICTIONARY_V52.tsv"),
    ("acceptance_criteria", "docs/validation/TARGET_PACKAGE_ACCEPTANCE_CRITERIA_V52.tsv"),
    ("safety_audit", "docs/validation/RECEIVED_PACKAGE_INTAKE_SAFETY_AUDIT_V52.md"),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff", type=Path, default=HANDOFF)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    text = args.handoff.read_text(errors="replace")
    rows: list[dict[str, str]] = []
    last_position = -1
    for expected_index, (step, artifact) in enumerate(EXPECTED_ORDER, start=1):
        position = text.find(artifact)
        exists = (ROOT / artifact).exists()
        if position == -1:
            status = "FAIL"
            detail = "missing from handoff"
        elif not exists:
            status = "FAIL"
            detail = "artifact missing"
        elif position < last_position:
            status = "FAIL"
            detail = "out of expected order"
        else:
            status = "PASS"
            detail = "ordered and exists"
        rows.append(
            {
                "expected_index": str(expected_index),
                "step": step,
                "artifact": artifact,
                "position": str(position),
                "status": status,
                "detail": detail,
            }
        )
        if position != -1:
            last_position = position

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["expected_index", "step", "artifact", "position", "status", "detail"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    failures = [row for row in rows if row["status"] != "PASS"]
    print({"checks": len(rows), "failures": len(failures), "out": str(args.out)})
    if failures and args.fail_on_error:
        raise SystemExit({"failures": failures})


if __name__ == "__main__":
    main()
