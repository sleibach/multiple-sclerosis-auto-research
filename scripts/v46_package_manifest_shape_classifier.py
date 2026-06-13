#!/usr/bin/env python3
"""Classify returned-package shape from a receipt manifest only.

This is returned-package operations infrastructure. It maps a non-sensitive file
listing plus terms class to the first-30-minute V46 scenario and command-order
inputs without opening score-bearing tables. It does not read returned scores,
expression data, private labels, or quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path

import v46_author_run_metric_format_adapter as adapter


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_package_manifest_shape_classifier"
TERMS_BLOCKING = {"UNKNOWN", "AMBIGUOUS_TERMS_BLOCK", "NO_PROCESSING_ALLOWED"}
REQUIRED_SCORED_FILES = [name for name in adapter.FILE_ALIASES if name != "failure_taxonomy_code.txt"]
FIRST30_SCENARIOS = {
    "scored_canonical_aggregate",
    "scored_noncanonical_aggregate",
    "scored_unknown_alias_aggregate",
    "unscoreable_aggregate",
    "partial_label_scored_aggregate",
    "terms_blocked_return",
}
SCORE_LIKE_TOKENS = ["metric", "result", "summary", "auc", "score", "validation"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    classify = sub.add_parser("classify")
    classify.add_argument("--manifest", type=Path, required=True)
    classify.add_argument("--terms-class", default="UNKNOWN")
    classify.add_argument("--outdir", type=Path, required=True)
    classify.add_argument("--fail-on-error", action="store_true")

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


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def basename(value: str) -> str:
    return Path(value).name.lower()


def manifest_file_names(rows: list[dict[str, str]]) -> set[str]:
    names = set()
    for row in rows:
        name = basename(row.get("relative_path_or_external_location", ""))
        if name:
            names.add(name)
    return names


def any_partial_label_marker(rows: list[dict[str, str]]) -> bool:
    for row in rows:
        text = " ".join(str(row.get(key, "")) for key in ["file_role", "notes", "relative_path_or_external_location"]).lower()
        if "partial_label" in text or "partial response" in text or "subset_label" in text:
            return True
    return False


def known_alias_map(names: set[str]) -> tuple[dict[str, str], dict[str, str]]:
    canonical_present: dict[str, str] = {}
    alias_present: dict[str, str] = {}
    for canonical, aliases in adapter.FILE_ALIASES.items():
        lower_aliases = [alias.lower() for alias in aliases]
        if canonical.lower() in names:
            canonical_present[canonical] = canonical
            continue
        hit = next((alias for alias in lower_aliases if alias in names), "")
        if hit:
            alias_present[canonical] = hit
    return canonical_present, alias_present


def has_unknown_score_like(names: set[str], known_names: set[str]) -> bool:
    for name in names:
        if name in known_names:
            continue
        if any(token in name for token in SCORE_LIKE_TOKENS):
            return True
    return False


def classify_manifest(manifest: Path, terms_class: str, outdir: Path) -> dict[str, object]:
    rows = read_tsv(manifest)
    names = manifest_file_names(rows)
    known_alias_names = {alias.lower() for aliases in adapter.FILE_ALIASES.values() for alias in aliases}
    canonical_present, alias_present = known_alias_map(names)
    found_required = set(canonical_present).union(alias_present)
    missing_required = [name for name in REQUIRED_SCORED_FILES if name not in found_required]
    failure_code_present = "failure_taxonomy_code.txt" in canonical_present or "failure_taxonomy_code.txt" in alias_present
    partial_label_marker = any_partial_label_marker(rows)
    unknown_score_like = has_unknown_score_like(names, known_alias_names)

    if terms_class in TERMS_BLOCKING:
        scenario = "terms_blocked_return"
        package_state = "scored" if "locked_rule_metrics.tsv" in found_required else "unscoreable"
        metric_state = "canonical" if package_state == "scored" else "unknown"
        route_reason = f"terms_class={terms_class} blocks package handling before file-shape routing"
    elif failure_code_present:
        scenario = "unscoreable_aggregate"
        package_state = "unscoreable"
        metric_state = "canonical" if not alias_present and not unknown_score_like else "unknown"
        route_reason = "manifest declares a failure taxonomy"
    elif unknown_score_like:
        scenario = "scored_unknown_alias_aggregate"
        package_state = "scored"
        metric_state = "unknown"
        route_reason = "manifest contains score-like files outside accepted alias set; adapter branch or repair request required"
    elif "locked_rule_metrics.tsv" not in found_required:
        scenario = "unscoreable_aggregate"
        package_state = "unscoreable"
        metric_state = "canonical" if not alias_present else "unknown"
        route_reason = "manifest lacks score-bearing locked-rule metrics"
    elif partial_label_marker:
        scenario = "partial_label_scored_aggregate"
        package_state = "scored"
        metric_state = "canonical" if not alias_present else "noncanonical"
        route_reason = "manifest marks partial response-label coverage"
    elif not missing_required and not alias_present:
        scenario = "scored_canonical_aggregate"
        package_state = "scored"
        metric_state = "canonical"
        route_reason = "all required scored aggregate outputs use canonical names"
    elif not missing_required:
        scenario = "scored_noncanonical_aggregate"
        package_state = "scored"
        metric_state = "noncanonical"
        route_reason = "all required scored aggregate outputs are present through accepted aliases"
    else:
        scenario = "unscoreable_aggregate"
        package_state = "unscoreable"
        metric_state = "unknown"
        route_reason = "manifest is incomplete for scored aggregate routing"

    classification = {
        "manifest": rel(manifest),
        "terms_class": terms_class,
        "n_manifest_rows": len(rows),
        "n_unique_filenames": len(names),
        "n_required_canonical_present": len([name for name in REQUIRED_SCORED_FILES if name in canonical_present]),
        "n_required_alias_present": len([name for name in REQUIRED_SCORED_FILES if name in alias_present]),
        "n_required_missing": len(missing_required),
        "missing_required": ";".join(missing_required),
        "partial_label_marker": str(partial_label_marker).lower(),
        "failure_taxonomy_present": str(failure_code_present).lower(),
        "unknown_score_like_filename_present": str(unknown_score_like).lower(),
        "first30_scenario": scenario,
        "package_state_for_command_order": package_state,
        "metric_format_state_for_command_order": metric_state,
        "score_values_read": "false",
        "route_reason": route_reason,
    }

    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(
        outdir / "package_manifest_shape_classification.tsv",
        [classification],
        [
            "manifest",
            "terms_class",
            "n_manifest_rows",
            "n_unique_filenames",
            "n_required_canonical_present",
            "n_required_alias_present",
            "n_required_missing",
            "missing_required",
            "partial_label_marker",
            "failure_taxonomy_present",
            "unknown_score_like_filename_present",
            "first30_scenario",
            "package_state_for_command_order",
            "metric_format_state_for_command_order",
            "score_values_read",
            "route_reason",
        ],
    )
    summary = {
        "synthetic": "synthetic" in str(manifest).lower() or "synthetic" in str(outdir).lower(),
        "purpose": "V46 package-manifest shape classification; no biological claim and no score values read",
        "overall_status": "PASS" if scenario in FIRST30_SCENARIOS and classification["score_values_read"] == "false" else "FAIL",
        "first30_scenario": scenario,
        "package_state_for_command_order": package_state,
        "metric_format_state_for_command_order": metric_state,
        "score_values_read": False,
        "classification": rel(outdir / "package_manifest_shape_classification.tsv"),
    }
    (outdir / "package_manifest_shape_classification_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return classification


def manifest_row(filename: str, role: str, notes: str = "") -> dict[str, str]:
    return {
        "cohort_id": "synthetic_return",
        "receipt_timestamp_utc": "2026-06-13T00:00:00Z",
        "received_from": "synthetic_fixture",
        "relative_path_or_external_location": filename,
        "file_role": role,
        "bytes": "123",
        "sha256_if_recordable": "synthetic",
        "sensitivity_class": "derived_non_sensitive_summary",
        "terms_status": "synthetic",
        "commit_allowed": "yes",
        "next_gate": "manifest_shape_classifier",
        "notes": notes,
    }


def write_manifest(path: Path, rows: list[dict[str, str]]) -> None:
    write_tsv(
        path,
        rows,
        [
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
        ],
    )


def canonical_rows(partial: bool = False) -> list[dict[str, str]]:
    rows = [manifest_row(name, name.removesuffix(".tsv").removesuffix(".json").removesuffix(".txt")) for name in REQUIRED_SCORED_FILES]
    if partial:
        rows.append(manifest_row("metadata/partial_response_label_metadata.tsv", "partial_label_metadata", "partial_label subset"))
    return rows


def alias_rows() -> list[dict[str, str]]:
    rows = []
    for canonical in REQUIRED_SCORED_FILES:
        alias = adapter.FILE_ALIASES[canonical][1] if len(adapter.FILE_ALIASES[canonical]) > 1 else canonical
        rows.append(manifest_row(alias, canonical.removesuffix(".tsv").removesuffix(".json").removesuffix(".txt")))
    return rows


def synthetic_cases(base: Path) -> list[tuple[str, str, list[dict[str, str]], str]]:
    unknown_alias = [
        manifest_row("run_info.txt", "run_metadata"),
        manifest_row("validation_result_summary.json", "validation_summary"),
        manifest_row("sample_retention.tsv", "sample_attrition"),
        manifest_row("module_coverage.tsv", "gene_mapping_coverage"),
        manifest_row("primary_metrics_table.tsv", "unknown_score_like_metric"),
        manifest_row("confounder_metrics.tsv", "confounder_adjustment_metrics"),
        manifest_row("joint_adjustment_metrics.tsv", "joint_confounder_metrics"),
        manifest_row("batch_qc.tsv", "batch_diagnostic_metrics"),
        manifest_row("result_report.md", "validation_result_report"),
    ]
    unscoreable = [
        manifest_row("RUN_METADATA.txt", "run_metadata"),
        manifest_row("validation_summary.json", "validation_summary"),
        manifest_row("sample_attrition.tsv", "sample_attrition"),
        manifest_row("gene_mapping_coverage.tsv", "gene_mapping_coverage"),
        manifest_row("failure_taxonomy_code.txt", "failure_taxonomy"),
        manifest_row("validation_result_report.md", "validation_result_report"),
    ]
    return [
        ("scored_canonical_manifest", "AGGREGATE_ONLY_LOCAL_PREFLIGHT", canonical_rows(), "scored_canonical_aggregate"),
        ("scored_noncanonical_manifest", "AGGREGATE_ONLY_LOCAL_PREFLIGHT", alias_rows(), "scored_noncanonical_aggregate"),
        ("scored_unknown_alias_manifest", "LOCAL_PREFLIGHT_ALLOWED", unknown_alias, "scored_unknown_alias_aggregate"),
        ("unscoreable_manifest", "AUTHOR_RUN_ONLY", unscoreable, "unscoreable_aggregate"),
        ("partial_label_manifest", "AGGREGATE_ONLY_LOCAL_PREFLIGHT", canonical_rows(partial=True), "partial_label_scored_aggregate"),
        ("terms_blocked_manifest", "NO_PROCESSING_ALLOWED", canonical_rows(), "terms_blocked_return"),
    ]


def synthetic_check(outdir: Path) -> int:
    outdir = resolve(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    manifest_dir = outdir / "synthetic_manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    checks: list[dict[str, object]] = []
    for case, terms_class, manifest_rows, expected_scenario in synthetic_cases(manifest_dir):
        manifest = manifest_dir / f"{case}.tsv"
        write_manifest(manifest, manifest_rows)
        case_out = outdir / case
        classification = classify_manifest(manifest, terms_class, case_out)
        observed = str(classification["first30_scenario"])
        row = {
            "case": case,
            "terms_class": terms_class,
            "expected_first30_scenario": expected_scenario,
            "observed_first30_scenario": observed,
            "package_state_for_command_order": classification["package_state_for_command_order"],
            "metric_format_state_for_command_order": classification["metric_format_state_for_command_order"],
            "score_values_read": classification["score_values_read"],
            "summary": rel(case_out / "package_manifest_shape_classification_summary.json"),
        }
        rows.append(row)
        checks.extend(
            [
                {
                    "case": case,
                    "check": "expected_first30_scenario",
                    "status": "PASS" if observed == expected_scenario else "FAIL",
                    "detail": f"expected={expected_scenario};observed={observed}",
                },
                {
                    "case": case,
                    "check": "score_values_read_false",
                    "status": "PASS" if classification["score_values_read"] == "false" else "FAIL",
                    "detail": str(classification["score_values_read"]),
                },
            ]
        )
    write_tsv(
        outdir / "package_manifest_shape_synthetic_cases.tsv",
        rows,
        [
            "case",
            "terms_class",
            "expected_first30_scenario",
            "observed_first30_scenario",
            "package_state_for_command_order",
            "metric_format_state_for_command_order",
            "score_values_read",
            "summary",
        ],
    )
    write_tsv(outdir / "package_manifest_shape_synthetic_lint.tsv", checks, ["case", "check", "status", "detail"])
    n_fail = sum(1 for row in checks if row["status"] != "PASS")
    summary = {
        "synthetic": True,
        "purpose": "V46 package-manifest shape classifier synthetic verification; no biological claim",
        "n_cases": len(rows),
        "n_lint_checks": len(checks),
        "n_lint_fail": n_fail,
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in rows),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "cases": rel(outdir / "package_manifest_shape_synthetic_cases.tsv"),
        "lint": rel(outdir / "package_manifest_shape_synthetic_lint.tsv"),
    }
    (outdir / "package_manifest_shape_synthetic_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_fail == 0 else 2


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir)
    outdir = resolve(args.outdir)
    classification = classify_manifest(resolve(args.manifest), args.terms_class, outdir)
    failed = classification["first30_scenario"] not in FIRST30_SCENARIOS or classification["score_values_read"] != "false"
    if args.fail_on_error and failed:
        return 1
    return 0 if not failed else 2


if __name__ == "__main__":
    raise SystemExit(main())
