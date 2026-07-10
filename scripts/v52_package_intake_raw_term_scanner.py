#!/usr/bin/env python3
"""Scan package-intake operator docs for unsafe credential/raw-data wording."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCS = [
    "docs/validation/PACKAGE_INTAKE_OPERATOR_QUICKSTART_V52.md",
    "analysis/received_package_intake/README.md",
    "docs/validation/RECEIVED_PACKAGE_FILE_NAMING_POLICY_V52.md",
    "docs/validation/MANIFEST_METADATA_VS_RAW_DATA_GIT_POLICY_V52.md",
    "docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md",
    "docs/validation/DATA_OWNER_PACKAGE_README_V52.md",
    "docs/validation/RECEIVED_PACKAGE_INTAKE_SAFETY_AUDIT_V52.md",
]
DEFAULT_OUT = ROOT / "analysis/v52_package_intake_raw_term_scanner/raw_term_scan.tsv"
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
JWT_LIKE_RE = re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}")
SIGNED_URL_RE = re.compile(r"(X-Amz-Signature=|X-Amz-Credential=|[?&](token|sig|signature)=)", re.I)
RAW_TERMS = ("raw", "restricted", "credential", "token", "signed url", "email")
SAFE_CONTEXT = (
    "do not",
    "do not include",
    "do not send",
    "never",
    "must not",
    "not ",
    "not allowed",
    "no ",
    "quarantine",
    "out of git",
    "outside git",
    "ignored",
    "prohibit",
    "forbidden",
    "blocked",
    "before touching",
    "before sending",
    "before allowed-use",
    "boundary",
    "safe",
    "redacted",
    "absent",
    "missing",
    "avoid",
    "checklist",
    "policy",
    "versus",
    "where received-package metadata",
    "may be committed",
    "treat it",
    "allowed-use",
    "what not to send",
)


def add(rows: list[dict[str, str]], document: str, line_no: int, check: str, status: str, detail: str) -> None:
    rows.append(
        {
            "document": document,
            "line": str(line_no),
            "check": check,
            "status": status,
            "detail": detail,
        }
    )


def scan_doc(doc_name: str, rows: list[dict[str, str]]) -> None:
    path = ROOT / doc_name
    text = path.read_text(errors="replace")
    lines = text.splitlines()
    for idx, line in enumerate(lines, start=1):
        lower = line.lower()
        context = " ".join(lines[max(0, idx - 8) : min(len(lines), idx + 2)]).lower()
        emails = [email for email in EMAIL_RE.findall(line) if not email.endswith(".invalid")]
        if emails:
            add(rows, doc_name, idx, "non_placeholder_email", "FAIL", ";".join(emails[:5]))
        if JWT_LIKE_RE.search(line):
            add(rows, doc_name, idx, "jwt_like_token", "FAIL", "jwt-like token pattern")
        if SIGNED_URL_RE.search(line):
            add(rows, doc_name, idx, "signed_url_or_token_param", "FAIL", "signed URL or token query parameter")
        if any(term in lower for term in RAW_TERMS):
            contextual = any(term in context for term in SAFE_CONTEXT)
            add(
                rows,
                doc_name,
                idx,
                "raw_or_credential_wording",
                "PASS_CONTEXTUAL" if contextual else "WARN_REVIEW",
                line.strip()[:240],
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs", nargs="*", default=DEFAULT_DOCS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    for doc_name in args.docs:
        scan_doc(doc_name, rows)

    if not rows:
        add(rows, "", 0, "scan", "PASS", "no raw or credential wording detected")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["document", "line", "check", "status", "detail"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    failures = [row for row in rows if row["status"] == "FAIL"]
    warnings = [row for row in rows if row["status"] == "WARN_REVIEW"]
    print({"checks": len(rows), "failures": len(failures), "warnings": len(warnings), "out": str(args.out)})
    if failures and args.fail_on_error:
        raise SystemExit({"failures": failures})


if __name__ == "__main__":
    main()
