#!/usr/bin/env python3
"""Lint returned-package receipt manifests before shape classification.

This is returned-package operations infrastructure. It checks only the manifest
schema and non-sensitive file-list metadata needed by the V46 package-manifest
shape classifier. It does not open returned tables, read result values, inspect
expression data, or access quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from urllib.parse import urlparse

import v46_author_run_metric_format_adapter as adapter


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_receipt_manifest_schema_linter"

REQUIRED_COLUMNS = [
    "cohort_id",
    "receipt_timestamp_utc",
    "received_from",
    "relative_path_or_external_location",
    "file_role",
    "bytes",
    "sha256_if_recordable",
    "sensitivity_class",
    "terms_status",
    "commit_allowed",
    "next_gate",
    "notes",
]
SAFE_SENSITIVITY_CLASSES = {
    "derived_non_sensitive_summary",
    "aggregate_non_sensitive_summary",
    "public_metadata",
    "non_sensitive_manifest",
}
SAFE_COMMIT_VALUES = {"yes", "terms_dependent"}
RAW_OR_PRIVATE_PATH_TOKENS = [
    "raw",
    "counts",
    "expression",
    "sample_metadata",
    "clinical",
    "private",
    "agreement",
    "quarantine",
    "data/raw",
    "gafson_dmf_2018",
    "karolinska_dmf_ros_2019",
    "gse228330_ocrelizumab_outcomes",
]
PRIVATE_URI_SCHEMES = {"s3", "gs", "http", "https", "ftp"}
SAFE_AGGREGATE_FILENAMES = {
    alias.lower()
    for aliases in adapter.FILE_ALIASES.values()
    for alias in aliases
}.union(
    {
        "terms_summary.tsv",
        "outcome_label_dictionary.tsv",
        "partial_response_label_metadata.tsv",
        "partial_label_metadata.tsv",
        "readme.md",
    }
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    lint = sub.add_parser("lint")
    lint.add_argument("--manifest", type=Path, required=True)
    lint.add_argument("--outdir", type=Path, required=True)
    lint.add_argument("--fail-on-error", action="store_true")

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


def read_tsv_with_header(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = reader.fieldnames or []
        rows = [{key: value or "" for key, value in row.items()} for row in reader]
    return fieldnames, rows


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def path_is_relative_metadata(value: str) -> tuple[bool, str]:
    if not value:
        return False, "empty_path"
    parsed = urlparse(value)
    if parsed.scheme in PRIVATE_URI_SCHEMES:
        return False, "external_uri_not_manifest_safe"
    candidate = Path(value)
    if candidate.is_absolute():
        return False, "absolute_path_not_allowed"
    lower = value.lower()
    hits = [token for token in RAW_OR_PRIVATE_PATH_TOKENS if token in lower]
    if hits:
        return False, f"raw_or_private_path_token:{';'.join(hits)}"
    basename = candidate.name.lower()
    if basename not in SAFE_AGGREGATE_FILENAMES:
        return False, f"unexpected_filename:{basename}"
    return True, "relative_non_sensitive_aggregate_path"


def lint_manifest(manifest: Path, outdir: Path, synthetic_case: str = "none") -> dict[str, object]:
    fieldnames, rows = read_tsv_with_header(manifest)
    checks: list[dict[str, object]] = []

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
    extra_columns = [column for column in fieldnames if column not in REQUIRED_COLUMNS]
    checks.append(
        {
            "case": synthetic_case,
            "row_number": "",
            "check": "required_columns_present",
            "status": "PASS" if not missing_columns else "FAIL",
            "detail": ";".join(missing_columns) if missing_columns else "all required columns present",
        }
    )
    checks.append(
        {
            "case": synthetic_case,
            "row_number": "",
            "check": "no_extra_columns",
            "status": "PASS" if not extra_columns else "FAIL",
            "detail": ";".join(extra_columns) if extra_columns else "no extra columns",
        }
    )
    checks.append(
        {
            "case": synthetic_case,
            "row_number": "",
            "check": "has_at_least_one_row",
            "status": "PASS" if rows else "FAIL",
            "detail": str(len(rows)),
        }
    )

    for index, row in enumerate(rows, start=1):
        path_value = row.get("relative_path_or_external_location", "")
        path_ok, path_detail = path_is_relative_metadata(path_value)
        sensitivity = row.get("sensitivity_class", "")
        commit_allowed = row.get("commit_allowed", "")
        bytes_value = row.get("bytes", "")
        sha = row.get("sha256_if_recordable", "")
        row_checks = [
            ("path_is_relative_non_sensitive_aggregate", path_ok, path_detail),
            ("sensitivity_class_safe", sensitivity in SAFE_SENSITIVITY_CLASSES, sensitivity),
            ("commit_allowed_safe", commit_allowed in SAFE_COMMIT_VALUES, commit_allowed),
            ("bytes_present_or_unknown", bool(bytes_value), bytes_value),
            ("sha_recorded_or_not_recordable", bool(sha), sha),
        ]
        for check, ok, detail in row_checks:
            checks.append(
                {
                    "case": synthetic_case,
                    "row_number": index,
                    "check": check,
                    "status": "PASS" if ok else "FAIL",
                    "detail": detail,
                }
            )

    n_fail = sum(1 for row in checks if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    lint_path = outdir / "receipt_manifest_schema_lint.tsv"
    summary_path = outdir / "receipt_manifest_schema_lint_summary.json"
    write_tsv(lint_path, checks, ["case", "row_number", "check", "status", "detail"])
    summary = {
        "synthetic": synthetic_case != "none",
        "synthetic_case": synthetic_case,
        "purpose": "V46 receipt-manifest schema lint; no biological claim and no score values read",
        "manifest": rel(manifest),
        "n_rows": len(rows),
        "n_checks": len(checks),
        "n_fail": n_fail,
        "all_score_values_read_false": True,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": rel(lint_path),
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def manifest_row(filename: str, role: str = "") -> dict[str, str]:
    return {
        "cohort_id": "synthetic_return",
        "receipt_timestamp_utc": "2026-06-13T00:00:00Z",
        "received_from": "synthetic_fixture",
        "relative_path_or_external_location": filename,
        "file_role": role or Path(filename).name.removesuffix(".tsv").removesuffix(".json").removesuffix(".txt").removesuffix(".md"),
        "bytes": "123",
        "sha256_if_recordable": "synthetic",
        "sensitivity_class": "derived_non_sensitive_summary",
        "terms_status": "synthetic",
        "commit_allowed": "yes",
        "next_gate": "manifest_shape_classifier",
        "notes": "",
    }


def write_manifest(path: Path, rows: list[dict[str, str]], columns: list[str] | None = None) -> None:
    fieldnames = columns or REQUIRED_COLUMNS
    write_tsv(path, [{key: row.get(key, "") for key in fieldnames} for row in rows], fieldnames)


def synthetic_manifests(base: Path) -> list[dict[str, object]]:
    canonical_files = [
        "RUN_METADATA.txt",
        "validation_summary.json",
        "sample_attrition.tsv",
        "gene_mapping_coverage.tsv",
        "locked_rule_metrics.tsv",
        "confounder_adjustment_metrics.tsv",
        "joint_confounder_metrics.tsv",
        "batch_diagnostic_metrics.tsv",
        "validation_result_report.md",
    ]
    cases: list[dict[str, object]] = []

    def add_case(case: str, expected_status: str, rows: list[dict[str, str]], columns: list[str] | None = None) -> None:
        manifest_path = base / case / "receipt_manifest.tsv"
        write_manifest(manifest_path, rows, columns)
        cases.append({"case": case, "expected_status": expected_status, "manifest": manifest_path})

    add_case("clean_aggregate_manifest", "PASS", [manifest_row(name) for name in canonical_files])
    add_case(
        "missing_required_column",
        "FAIL",
        [manifest_row("locked_rule_metrics.tsv")],
        [column for column in REQUIRED_COLUMNS if column != "sha256_if_recordable"],
    )
    add_case("raw_expression_path", "FAIL", [manifest_row("raw/expression_counts.tsv", "raw_expression")])
    add_case("private_agreement_path", "FAIL", [manifest_row("private_agreement_or_email", "private_terms_or_correspondence")])
    add_case("absolute_local_path", "FAIL", [manifest_row("/Users/example/private/locked_rule_metrics.tsv", "locked_rule_metrics")])
    add_case("remote_private_url", "FAIL", [manifest_row("https://private.example.org/locked_rule_metrics.tsv", "locked_rule_metrics")])
    restricted = manifest_row("locked_rule_metrics.tsv", "locked_rule_metrics")
    restricted["sensitivity_class"] = "restricted_clinical"
    restricted["commit_allowed"] = "no"
    add_case("restricted_sensitivity_class", "FAIL", [restricted])
    add_case("unexpected_score_filename", "FAIL", [manifest_row("mystery_auc_results.tsv", "unknown_result")])
    add_case("empty_manifest", "FAIL", [])
    return cases


def synthetic_check(outdir: Path) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    case_rows: list[dict[str, object]] = []
    lint_rows: list[dict[str, object]] = []
    for case in synthetic_manifests(outdir / "synthetic"):
        case_outdir = outdir / case["case"]
        summary = lint_manifest(Path(case["manifest"]), case_outdir, synthetic_case=str(case["case"]))
        observed = str(summary["overall_status"])
        expected = str(case["expected_status"])
        case_rows.append(
            {
                "case": case["case"],
                "expected_status": expected,
                "observed_status": observed,
                "status_ok": str(expected == observed).lower(),
                "n_rows": summary["n_rows"],
                "n_checks": summary["n_checks"],
                "n_fail": summary["n_fail"],
                "all_score_values_read_false": str(summary["all_score_values_read_false"]).lower(),
                "summary": rel(case_outdir / "receipt_manifest_schema_lint_summary.json"),
            }
        )
        for row in read_tsv(case_outdir / "receipt_manifest_schema_lint.tsv"):
            lint_rows.append({"case": case["case"], **row})

    write_tsv(
        outdir / "receipt_manifest_schema_synthetic_cases.tsv",
        case_rows,
        [
            "case",
            "expected_status",
            "observed_status",
            "status_ok",
            "n_rows",
            "n_checks",
            "n_fail",
            "all_score_values_read_false",
            "summary",
        ],
    )
    write_tsv(
        outdir / "receipt_manifest_schema_synthetic_lint.tsv",
        lint_rows,
        ["case", "row_number", "check", "status", "detail"],
    )
    n_mismatch = sum(1 for row in case_rows if row["status_ok"] != "true")
    summary = {
        "synthetic": True,
        "purpose": "V46 receipt-manifest schema linter synthetic verification; no biological claim",
        "n_cases": len(case_rows),
        "n_expected_pass": sum(1 for row in case_rows if row["expected_status"] == "PASS"),
        "n_expected_fail": sum(1 for row in case_rows if row["expected_status"] == "FAIL"),
        "n_status_mismatch": n_mismatch,
        "all_score_values_read_false": all(row["all_score_values_read_false"] == "true" for row in case_rows),
        "overall_status": "PASS" if n_mismatch == 0 else "FAIL",
        "cases": rel(outdir / "receipt_manifest_schema_synthetic_cases.tsv"),
        "lint": rel(outdir / "receipt_manifest_schema_synthetic_lint.tsv"),
    }
    (outdir / "receipt_manifest_schema_synthetic_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_mismatch == 0 else 1


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(resolve(args.outdir))
    if args.cmd == "lint":
        outdir = resolve(args.outdir)
        summary = lint_manifest(resolve(args.manifest), outdir)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 1 if args.fail_on_error and summary["overall_status"] != "PASS" else (0 if summary["overall_status"] == "PASS" else 2)
    raise ValueError(args.cmd)


if __name__ == "__main__":
    raise SystemExit(main())
