#!/usr/bin/env python3
"""Precheck collaborator author-run aggregate packages for redaction risks.

This is a governance gate, not a biological analysis. It scans returned
aggregate packages for filenames, columns, and text patterns that suggest raw
expression, individual-level labels, credentials, private correspondence, or
identifiers were included when only aggregate outputs should be handled.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_author_run_redaction_precheck"
SYNTHETIC_COMPLETE_SOURCE = ROOT / "analysis/v45_author_run_output_check/synthetic_complete_author_run_package"

ALLOWED_FILENAMES = {
    "validation_summary.json",
    "sample_attrition.tsv",
    "gene_mapping_coverage.tsv",
    "locked_rule_metrics.tsv",
    "confounder_adjustment_metrics.tsv",
    "joint_confounder_metrics.tsv",
    "batch_diagnostic_metrics.tsv",
    "RUN_METADATA.txt",
    "validation_result_report.md",
    "EXPORT_ATTESTATION.json",
}

FILENAME_BLOCK_PATTERNS = [
    (re.compile(r"(^|[_\-])(raw|counts?|expression|expr|matrix)([_\-.]|$)", re.I), "raw_expression_or_matrix_filename"),
    (re.compile(r"(sample|subject|patient|gsm)[_\-]?(map|metadata|labels?|ids?)", re.I), "sample_or_subject_level_filename"),
    (re.compile(r"(clinical|neda|edss|relapse|response)[_\-]?(labels?|metadata|outcomes?)", re.I), "clinical_label_filename"),
    (re.compile(r"(agreement|contract|du[a-z]*|correspondence|reply|email)", re.I), "private_correspondence_or_agreement_filename"),
    (re.compile(r"(\.env|credential|secret|token|password|private[_\-]?url|bearer)", re.I), "credential_or_private_url_filename"),
]

COLUMN_BLOCK_PATTERNS = [
    (re.compile(r"^(sample|subject|patient|participant|person|gsm|geo_accession)_?id$", re.I), "sample_or_subject_identifier_column"),
    (re.compile(r"(sample|subject|patient|gsm)[_\-]?(map|metadata|label|id)", re.I), "sample_or_subject_level_column"),
    (re.compile(r"(raw|individual)[_\-]?(expression|count|label|outcome)", re.I), "raw_or_individual_level_column"),
    (re.compile(r"(neda|edss|relapse|response|clinical)[_\-]?(label|status|outcome|score)$", re.I), "clinical_label_column"),
    (re.compile(r"(email|token|secret|password|credential|private[_\-]?url)", re.I), "credential_or_private_contact_column"),
]

TEXT_BLOCK_PATTERNS = [
    (re.compile(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.I), "email_address_text"),
    (re.compile(r"(bearer\s+[A-Za-z0-9_\-.]+|api[_\-]?key|clientsecret|password\s*=|token\s*=)", re.I), "credential_text"),
    (re.compile(r"(signed\s+agreement|data\s+use\s+agreement|private\s+correspondence)", re.I), "private_agreement_or_correspondence_text"),
    (re.compile(r"(individual[-\s]?level|patient[-\s]?level|sample[-\s]?level)\s+(label|outcome|clinical|expression)", re.I), "individual_level_text"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    check = sub.add_parser("check")
    check.add_argument("--root", type=Path, required=True, help="Returned aggregate package directory.")
    check.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    check.add_argument("--fail-on-error", action="store_true")

    syn = sub.add_parser("synthetic-check")
    syn.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def pattern_hits(name: str, patterns: list[tuple[re.Pattern[str], str]]) -> list[str]:
    return [reason for pattern, reason in patterns if pattern.search(name)]


def file_columns(path: Path) -> list[str]:
    if path.suffix.lower() not in {".tsv", ".csv"}:
        return []
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    try:
        with path.open(newline="") as handle:
            reader = csv.reader(handle, delimiter=delimiter)
            return next(reader, [])
    except Exception:
        return []


def text_hits(path: Path) -> list[str]:
    if path.suffix.lower() not in {".txt", ".md", ".json", ".tsv", ".csv"}:
        return []
    try:
        text = path.read_text(errors="ignore")[:65536]
    except Exception:
        return ["unreadable_text_for_redaction_scan"]
    return pattern_hits(text, TEXT_BLOCK_PATTERNS)


def check_package(root: Path, outdir: Path, fail_on_error: bool) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    if not root.exists():
        raise SystemExit(f"package root does not exist: {root}")

    rows: list[dict[str, object]] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel_package = str(path.relative_to(root))
        filename_reasons = [] if path.name in ALLOWED_FILENAMES else pattern_hits(rel_package, FILENAME_BLOCK_PATTERNS)
        column_reasons: list[str] = []
        for column in file_columns(path):
            column_reasons.extend(pattern_hits(column, COLUMN_BLOCK_PATTERNS))
        text_reasons = text_hits(path)
        reasons = sorted(set(filename_reasons + column_reasons + text_reasons))
        severity = "BLOCK" if reasons else "PASS"
        if not reasons and path.name not in ALLOWED_FILENAMES:
            severity = "WARN"
            reasons = ["unexpected_file_review_manually"]
        rows.append(
            {
                "package_file": rel_package,
                "allowed_minimum_output_name": path.name in ALLOWED_FILENAMES,
                "severity": severity,
                "reasons": ";".join(reasons),
            }
        )

    audit_path = outdir / "author_run_redaction_precheck.tsv"
    with audit_path.open("w", newline="") as handle:
        fieldnames = ["package_file", "allowed_minimum_output_name", "severity", "reasons"]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    n_block = sum(1 for row in rows if row["severity"] == "BLOCK")
    n_warn = sum(1 for row in rows if row["severity"] == "WARN")
    summary = {
        "synthetic": "synthetic" in str(root).lower(),
        "purpose": "author-run aggregate package redaction precheck; no biological claim",
        "root": rel(root),
        "n_files_scanned": len(rows),
        "n_block": n_block,
        "n_warn": n_warn,
        "overall_status": "PASS" if n_block == 0 else "FAIL",
        "audit": rel(audit_path),
    }
    (outdir / "author_run_redaction_precheck_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if fail_on_error and n_block else 0


def copy_complete_fixture(target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(SYNTHETIC_COMPLETE_SOURCE, target)


def synthetic_check(outdir: Path) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    complete = outdir / "synthetic_complete_aggregate_package"
    risky = outdir / "synthetic_risky_aggregate_package"
    copy_complete_fixture(complete)
    copy_complete_fixture(risky)
    (risky / "raw_expression_matrix.tsv").write_text(
        "sample_id\tpatient_id\tGENE1\tGENE2\n"
        "SYN_SAMPLE_001\tSYN_PATIENT_001\t1.2\t3.4\n"
    )
    (risky / "clinical_response_labels.tsv").write_text(
        "patient_id\tneda4_label\trelapse_status\n"
        "SYN_PATIENT_001\tresponder\tno_relapse\n"
    )
    (risky / "private_email_reply.txt").write_text(
        "synthetic: true\n"
        "This synthetic private correspondence includes person@example.test for scanner testing.\n"
    )

    complete_out = outdir / "complete_fixture"
    risky_out = outdir / "risky_fixture"
    rc_complete = check_package(complete, complete_out, True)
    rc_risky = check_package(risky, risky_out, False)
    complete_summary = json.loads((complete_out / "author_run_redaction_precheck_summary.json").read_text())
    risky_summary = json.loads((risky_out / "author_run_redaction_precheck_summary.json").read_text())
    summary = {
        "synthetic": True,
        "purpose": "synthetic redaction precheck regression; no biological claim",
        "complete_fixture_exit_code": rc_complete,
        "risky_fixture_exit_code_without_fail_on_error": rc_risky,
        "complete_expected": "PASS",
        "risky_expected": "FAIL",
        "complete_overall_status": complete_summary["overall_status"],
        "complete_n_block": complete_summary["n_block"],
        "risky_overall_status": risky_summary["overall_status"],
        "risky_n_block": risky_summary["n_block"],
    }
    (outdir / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return rc_complete


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(resolve(args.outdir))
    return check_package(resolve(args.root), resolve(args.outdir), args.fail_on_error)


if __name__ == "__main__":
    raise SystemExit(main())
