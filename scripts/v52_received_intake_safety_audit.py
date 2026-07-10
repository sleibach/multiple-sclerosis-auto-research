#!/usr/bin/env python3
"""Smoke-audit tracked received-package intake artifacts for commit safety.

This is an operational guard. It does not inspect raw package data and does not
make biological claims.
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INTAKE_ROOT = ROOT / "analysis/received_package_intake"
DEFAULT_OUT = ROOT / "analysis/v52_received_intake_safety_audit/intake_safety_audit.tsv"
ALLOWED_SUFFIXES = {".md", ".sha256", ".tsv"}
FORBIDDEN_SUFFIXES = {
    ".bam",
    ".cram",
    ".fastq",
    ".fq",
    ".gz",
    ".h5",
    ".h5ad",
    ".loom",
    ".mtx",
    ".parquet",
    ".rds",
    ".safetensors",
    ".sam",
    ".vcf",
}
FORBIDDEN_TSV_HEADERS = {
    "age",
    "birth_date",
    "dob",
    "edss",
    "gene",
    "gene_id",
    "participant_id",
    "patient_id",
    "raw_count",
    "read_count",
    "response_label",
    "sample_id",
    "subject_id",
}
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def intake_files(intake_root: Path, all_files: bool) -> list[Path]:
    if all_files:
        return sorted(path for path in intake_root.rglob("*") if path.is_file())
    rel_root = intake_root.relative_to(ROOT)
    output = subprocess.check_output(["git", "ls-files", str(rel_root)], cwd=ROOT, text=True)
    return [ROOT / line for line in output.splitlines() if line.strip()]


def add(rows: list[dict[str, str]], path: Path, check: str, status: str, detail: str) -> None:
    rows.append(
        {
            "path": str(path.resolve().relative_to(ROOT)),
            "check": check,
            "status": status,
            "detail": detail,
        }
    )


def audit_file(path: Path, rows: list[dict[str, str]], max_bytes: int) -> None:
    suffixes = {suffix.lower() for suffix in path.suffixes}
    suffix = path.suffix.lower()
    size = path.stat().st_size

    add(rows, path, "size", "PASS" if size <= max_bytes else "FAIL", f"bytes={size}; max={max_bytes}")

    bad_suffixes = sorted(suffixes & FORBIDDEN_SUFFIXES)
    add(
        rows,
        path,
        "raw_extension",
        "FAIL" if bad_suffixes else "PASS",
        "forbidden_suffixes=" + ";".join(bad_suffixes),
    )

    add(
        rows,
        path,
        "allowed_suffix",
        "PASS" if suffix in ALLOWED_SUFFIXES else "FAIL",
        f"suffix={suffix}",
    )

    text = path.read_text(errors="replace")
    real_emails = [email for email in EMAIL_RE.findall(text) if not email.endswith(".invalid")]
    add(
        rows,
        path,
        "non_placeholder_email",
        "FAIL" if real_emails else "PASS",
        "emails=" + ";".join(real_emails[:5]),
    )

    if suffix == ".tsv":
        with path.open(newline="") as handle:
            reader = csv.reader(handle, delimiter="\t")
            headers = next(reader, [])
        normalized = {header.strip().lower() for header in headers}
        forbidden_headers = sorted(normalized & FORBIDDEN_TSV_HEADERS)
        add(
            rows,
            path,
            "raw_like_tsv_headers",
            "FAIL" if forbidden_headers else "PASS",
            "headers=" + ";".join(forbidden_headers),
        )


def write_rows(rows: list[dict[str, str]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["path", "check", "status", "detail"]
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake-root", type=Path, default=DEFAULT_INTAKE_ROOT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    parser.add_argument("--all-files", action="store_true")
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    intake_root = args.intake_root if args.intake_root.is_absolute() else ROOT / args.intake_root
    files = intake_files(intake_root.resolve(), args.all_files)
    rows: list[dict[str, str]] = []
    for path in files:
        audit_file(path, rows, args.max_bytes)
    write_rows(rows, args.out)

    failures = [row for row in rows if row["status"] != "PASS"]
    print({"files": len(files), "checks": len(rows), "failures": len(failures), "out": str(args.out)})
    if failures and args.fail_on_error:
        raise SystemExit({"failures": failures})


if __name__ == "__main__":
    main()
