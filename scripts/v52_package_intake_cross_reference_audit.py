#!/usr/bin/env python3
"""Audit package-intake documents for broken repository path references."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCS = [
    "docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md",
    "docs/validation/PACKAGE_INTAKE_OPERATOR_QUICKSTART_V52.md",
    "analysis/received_package_intake/README.md",
    "docs/validation/RECEIVED_PACKAGE_INTAKE_SAFETY_AUDIT_V52.md",
    "docs/validation/PACKAGE_ID_VALIDATION_NOTE_V52.md",
    "docs/validation/PACKAGE_ID_VALIDATOR_REGRESSION_FIXTURE_V52.md",
    "docs/validation/RECEIVED_PACKAGE_INTAKE_SAFETY_AUDIT_REGRESSION_FIXTURE_V52.md",
    "docs/validation/DATA_OWNER_PACKAGE_README_V52.md",
    "docs/validation/INCOMING_PACKAGE_MANIFEST_TEMPLATE_V52.tsv",
]
DEFAULT_OUT = ROOT / "analysis/v52_package_intake_cross_reference_audit/package_intake_cross_reference_audit.tsv"
PATH_PREFIXES = ("analysis/", "docs/", "scripts/", "knowledge_external/", "meta/")
BACKTICK_RE = re.compile(r"`([^`]+)`")


def references_from_text(text: str) -> list[str]:
    refs: list[str] = []
    for match in BACKTICK_RE.findall(text):
        for token in match.replace("\n", " ").split():
            token = token.strip(".,;:()[]")
            if token.startswith(PATH_PREFIXES):
                refs.append(token)
    return refs


def audit_doc(doc: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    text = doc.read_text(errors="replace")
    for ref in sorted(set(references_from_text(text))):
        if "<" in ref or ">" in ref:
            status = "SKIP_PLACEHOLDER"
            detail = "placeholder path"
        elif (ROOT / ref).exists():
            status = "PASS"
            detail = "exists"
        else:
            status = "FAIL"
            detail = "missing"
        rows.append(
            {
                "document": str(doc.relative_to(ROOT)),
                "reference": ref,
                "status": status,
                "detail": detail,
            }
        )
    if not rows:
        rows.append(
            {
                "document": str(doc.relative_to(ROOT)),
                "reference": "",
                "status": "PASS",
                "detail": "no repository-path references",
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs", nargs="*", default=DEFAULT_DOCS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    for doc_name in args.docs:
        doc = ROOT / doc_name
        if not doc.exists():
            rows.append(
                {
                    "document": doc_name,
                    "reference": "",
                    "status": "FAIL",
                    "detail": "document missing",
                }
            )
            continue
        rows.extend(audit_doc(doc))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["document", "reference", "status", "detail"]
    with args.out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    failures = [row for row in rows if row["status"] == "FAIL"]
    print({"documents": len(args.docs), "references": len(rows), "failures": len(failures), "out": str(args.out)})
    if failures and args.fail_on_error:
        raise SystemExit({"failures": failures})


if __name__ == "__main__":
    main()
