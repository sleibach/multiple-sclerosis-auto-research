#!/usr/bin/env python3
"""Check that the high-priority source_terms packet matches the review queue."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = ROOT / "knowledge_external/catalogs/indexes/source_terms_review_queue_v48.tsv"
DEFAULT_PACKET = ROOT / "knowledge_external/catalogs/indexes/high_priority_source_terms_packet_v48.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v48_high_priority_source_terms_packet_freshness_linter"
COMPARE_FIELDS = [
    "record_type",
    "epistemic_class",
    "source_domain",
    "review_class",
    "source_url",
    "terms_review_reason",
    "recommended_next_step",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint high-priority source_terms packet freshness")
    lint.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    lint.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic freshness fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def add(rows: list[dict[str, object]], record_id: str, check: str, status: str, detail: str) -> None:
    rows.append({"record_id": record_id, "check": check, "status": status, "detail": detail})


def lint_packet(queue_path: Path, packet_path: Path, outdir: Path, fail_on_error: bool) -> int:
    queue_rows = [row for row in read_tsv(queue_path) if row.get("priority") == "high"]
    packet_rows = read_tsv(packet_path) if packet_path.exists() else []
    expected = {row.get("record_id", ""): row for row in queue_rows}
    observed = {row.get("record_id", ""): row for row in packet_rows}
    rows: list[dict[str, object]] = []
    for record_id, queue_row in sorted(expected.items()):
        packet_row = observed.get(record_id)
        add(rows, record_id, "present_in_packet", "PASS" if packet_row else "FAIL", str(packet_path))
        if not packet_row:
            continue
        for field in COMPARE_FIELDS:
            status = "PASS" if queue_row.get(field, "") == packet_row.get(field, "") else "FAIL"
            add(rows, record_id, f"field_matches.{field}", status, f"queue={queue_row.get(field, '')} packet={packet_row.get(field, '')}")
        add(
            rows,
            record_id,
            "not_project_grounded_marker",
            "PASS" if packet_row.get("not_project_grounded_marker", "") == "NOT_PROJECT_GROUNDED" else "FAIL",
            "packet row must preserve external/not-grounded boundary marker",
        )
        add(
            rows,
            record_id,
            "record_path_resolved",
            "PASS" if packet_row.get("record_path", "") and packet_row.get("record_path") != "MISSING_RECORD_PATH" else "FAIL",
            "packet row must point back to its external JSON record",
        )
    for record_id in sorted(set(observed) - set(expected)):
        add(rows, record_id, "no_extra_packet_record", "FAIL", "packet contains a record that is not high-priority in the queue")
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "high_priority_source_terms_packet_freshness_lint.tsv", rows, ["record_id", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 high-priority source_terms packet freshness lint; source-terms triage only; no claim validation",
        "n_expected_high_priority_records": len(expected),
        "n_packet_records": len(observed),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "high_priority_source_terms_packet_freshness_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    queue = outdir / "synthetic_queue.tsv"
    packet = outdir / "synthetic_packet.tsv"
    queue_fields = ["priority", "record_id", *COMPARE_FIELDS]
    packet_fields = ["record_id", "record_path", *COMPARE_FIELDS, "not_project_grounded_marker"]
    write_tsv(
        queue,
        [
            {
                "priority": "high",
                "record_id": "SYN_HIGH_PRESENT",
                "record_type": "external_claim",
                "epistemic_class": "external-unverifiable",
                "source_domain": "example.org",
                "review_class": "publisher_literature",
                "source_url": "https://example.org/a",
                "terms_review_reason": "terms matter",
                "recommended_next_step": "review terms",
            },
            {
                "priority": "high",
                "record_id": "SYN_HIGH_MISSING",
                "record_type": "external_claim",
                "epistemic_class": "external-unverifiable",
                "source_domain": "example.org",
                "review_class": "publisher_literature",
                "source_url": "https://example.org/b",
                "terms_review_reason": "terms matter",
                "recommended_next_step": "review terms",
            },
        ],
        queue_fields,
    )
    write_tsv(
        packet,
        [
            {
                "record_id": "SYN_HIGH_PRESENT",
                "record_path": "knowledge_external/records/synthetic.json",
                "record_type": "external_claim",
                "epistemic_class": "external-unverifiable",
                "source_domain": "example.org",
                "review_class": "publisher_literature",
                "source_url": "https://example.org/a",
                "terms_review_reason": "terms matter",
                "recommended_next_step": "review terms",
                "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
            },
            {
                "record_id": "SYN_HIGH_STALE",
                "record_path": "knowledge_external/records/stale.json",
                "record_type": "external_claim",
                "epistemic_class": "external-unverifiable",
                "source_domain": "example.org",
                "review_class": "publisher_literature",
                "source_url": "https://example.org/stale",
                "terms_review_reason": "terms matter",
                "recommended_next_step": "review terms",
                "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
            },
        ],
        packet_fields,
    )
    lint_out = outdir / "synthetic_lint"
    lint_packet(queue, packet, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "high_priority_source_terms_packet_freshness_lint.tsv")
    checks = {
        "present_record_passes": any(row["record_id"] == "SYN_HIGH_PRESENT" and row["check"] == "present_in_packet" and row["status"] == "PASS" for row in rows),
        "missing_record_fails": any(row["record_id"] == "SYN_HIGH_MISSING" and row["check"] == "present_in_packet" and row["status"] == "FAIL" for row in rows),
        "extra_record_fails": any(row["record_id"] == "SYN_HIGH_STALE" and row["check"] == "no_extra_packet_record" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_high_priority_source_terms_packet_freshness_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 high-priority source_terms packet freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_high_priority_source_terms_packet_freshness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_packet(args.queue, args.packet, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
