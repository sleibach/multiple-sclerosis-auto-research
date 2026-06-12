#!/usr/bin/env python3
"""Build a dry-run send-readiness manifest for the V45 author-run packet.

This is an operational guard only. It checks committed non-sensitive packet
files, checksums, command-plan consistency, and current-action routing. It does
not bundle files, send files, inspect external data, or run validation.
"""

from __future__ import annotations

import argparse
import csv
import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_author_run_bundle_dryrun_manifest/live"
DEFAULTS = {
    "bundle_index": ROOT / "analysis/v45_author_run_packet_bundle/author_run_packet_bundle_index.tsv",
    "checksum_manifest": ROOT / "analysis/v45_author_run_packet_checksums/write/author_run_packet_sha256_manifest.tsv",
    "checksum_verify": ROOT / "analysis/v45_author_run_packet_checksums/verify/author_run_packet_checksum_verify.tsv",
    "checksum_write_summary": ROOT / "analysis/v45_author_run_packet_checksums/write/author_run_packet_checksum_summary.json",
    "checksum_verify_summary": ROOT / "analysis/v45_author_run_packet_checksums/verify/author_run_packet_checksum_verify_summary.json",
    "command_plan_summary": ROOT / "analysis/v45_command_plan_consistency/command_plan_consistency_summary.json",
    "current_actions": ROOT / "analysis/v45_current_action_card/current_action_card.tsv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument(
        "--synthetic-case",
        choices=["none", "missing_required"],
        default="none",
        help="Apply a labeled synthetic mutation for regression testing.",
    )
    parser.add_argument("--expect-status", choices=["PASS", "FAIL"], default="PASS")
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text()) if path.exists() else {}


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def add_violation(violations: list[dict[str, str]], severity: str, path: str, check: str, detail: str) -> None:
    violations.append({"severity": severity, "path": path, "check": check, "detail": detail})


def apply_synthetic_case(bundle_rows: list[dict[str, str]], synthetic_case: str) -> list[dict[str, str]]:
    rows = deepcopy(bundle_rows)
    if synthetic_case == "missing_required":
        for row in rows:
            if row.get("include_in_author_packet") == "yes" and row.get("required_or_optional") == "required":
                row["path"] = "docs/validation/SYNTHETIC_MISSING_AUTHOR_PACKET_FILE.md"
                row["artifact_role"] = "synthetic_missing_required_file"
                break
    return rows


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    bundle_rows = apply_synthetic_case(read_tsv(DEFAULTS["bundle_index"]), args.synthetic_case)
    checksum_rows = {row.get("path", ""): row for row in read_tsv(DEFAULTS["checksum_verify"])}
    checksum_manifest_rows = {row.get("path", ""): row for row in read_tsv(DEFAULTS["checksum_manifest"])}
    checksum_write_summary = read_json(DEFAULTS["checksum_write_summary"])
    checksum_verify_summary = read_json(DEFAULTS["checksum_verify_summary"])
    command_plan_summary = read_json(DEFAULTS["command_plan_summary"])
    current_actions = read_tsv(DEFAULTS["current_actions"])

    manifest_rows: list[dict[str, str]] = []
    violations: list[dict[str, str]] = []
    included = [row for row in bundle_rows if row.get("include_in_author_packet") == "yes"]
    excluded = [row for row in bundle_rows if row.get("include_in_author_packet") != "yes"]

    for row in included:
        path = row.get("path", "")
        observed = checksum_rows.get(path, {})
        in_manifest = path in checksum_manifest_rows
        exists = (ROOT / path).exists()
        verify_status = observed.get("verify_status", "")
        status = "PASS" if exists and in_manifest and verify_status == "PASS" else "FAIL"
        if not exists:
            add_violation(violations, "hard", path, "included_path_exists", "included packet file is missing")
        if not in_manifest:
            add_violation(violations, "hard", path, "checksum_manifest_membership", "included packet file is absent from checksum manifest")
        if verify_status and verify_status != "PASS":
            add_violation(violations, "hard", path, "checksum_verify_status", f"verify_status={verify_status}")
        if not verify_status:
            add_violation(violations, "hard", path, "checksum_verify_row_missing", "included packet file has no checksum verification row")
        manifest_rows.append(
            {
                "section": row.get("section", ""),
                "artifact_role": row.get("artifact_role", ""),
                "path": path,
                "required_or_optional": row.get("required_or_optional", ""),
                "exists": "yes" if exists else "no",
                "in_checksum_manifest": "yes" if in_manifest else "no",
                "verify_status": verify_status,
                "dryrun_status": status,
            }
        )

    forbidden_included = [
        row for row in bundle_rows
        if row.get("include_in_author_packet") == "yes"
        and (row.get("path", "").startswith("data/raw") or row.get("path", "").startswith("data/quarantine") or row.get("path", "") == ".env")
    ]
    for row in forbidden_included:
        add_violation(violations, "hard", row.get("path", ""), "forbidden_path_included", "raw/quarantine/env path marked include=yes")

    if checksum_write_summary.get("overall_status") != "PASS":
        add_violation(violations, "hard", rel(DEFAULTS["checksum_write_summary"]), "checksum_write_summary", "checksum manifest write summary is not PASS")
    if checksum_verify_summary.get("overall_status") != "PASS":
        add_violation(violations, "hard", rel(DEFAULTS["checksum_verify_summary"]), "checksum_verify_summary", "checksum manifest verify summary is not PASS")
    if command_plan_summary.get("overall_status") != "PASS":
        add_violation(violations, "hard", rel(DEFAULTS["command_plan_summary"]), "command_plan_consistency", "command-plan consistency summary is not PASS")
    if not any(row.get("cohort_id") == "any_author_run_fallback" for row in current_actions):
        add_violation(violations, "hard", rel(DEFAULTS["current_actions"]), "author_run_route_missing", "current action card lacks author-run fallback row")

    manifest_path = outdir / "author_run_bundle_dryrun_manifest.tsv"
    violations_path = outdir / "author_run_bundle_dryrun_violations.tsv"
    write_tsv(
        manifest_path,
        manifest_rows,
        [
            "section",
            "artifact_role",
            "path",
            "required_or_optional",
            "exists",
            "in_checksum_manifest",
            "verify_status",
            "dryrun_status",
        ],
    )
    write_tsv(violations_path, violations, ["severity", "path", "check", "detail"])

    n_hard = sum(1 for row in violations if row["severity"] == "hard")
    observed = "PASS" if n_hard == 0 else "FAIL"
    summary = {
        "synthetic": args.synthetic_case != "none",
        "synthetic_case": args.synthetic_case,
        "purpose": "V45 author-run packet dry-run send-readiness manifest; no biological claim",
        "observed_status": observed,
        "expected_status": args.expect_status,
        "expectation_met": observed == args.expect_status,
        "n_included": len(included),
        "n_excluded": len(excluded),
        "n_hard_violations": n_hard,
        "checksum_write_status": checksum_write_summary.get("overall_status", "MISSING"),
        "checksum_verify_status": checksum_verify_summary.get("overall_status", "MISSING"),
        "command_plan_consistency_status": command_plan_summary.get("overall_status", "MISSING"),
        "manifest": rel(manifest_path),
        "violations": rel(violations_path),
    }
    (outdir / "author_run_bundle_dryrun_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["expectation_met"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
