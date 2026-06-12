#!/usr/bin/env python3
"""Verify V45 outbound request packet completeness and checksums.

This is an operations/readiness guard. It hashes committed, non-sensitive
request drafts only. It does not send email, mark requests as sent, receive
data, inspect private data, or run validation.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_outbound_request_packet_integrity/live"
DEFAULT_EXTERNAL = ROOT / "analysis/v45_external_blocker_board/external_blocker_board.tsv"
DEFAULT_PACKET_DIR = ROOT / "docs/validation/outbound_requests"

SEND_APPROVAL_PHRASES = [
    "send only if",
    "send only after",
]
SENT_COPY_PHRASE = "save the exact sent"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--external", type=Path, default=DEFAULT_EXTERNAL)
    parser.add_argument("--packet-dir", type=Path, default=DEFAULT_PACKET_DIR)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument(
        "--synthetic-case",
        choices=["none", "missing_packet"],
        default="none",
        help="Apply a labeled synthetic mutation for regression testing.",
    )
    parser.add_argument("--expect-status", choices=["PASS", "FAIL"], default="PASS")
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def has_guard_language(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(errors="ignore").lower()
    return any(phrase in text for phrase in SEND_APPROVAL_PHRASES) and SENT_COPY_PHRASE in text


def has_recipient_and_subject(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(errors="ignore").lower()
    recipient_ok = "to:" in text or "dear " in text
    subject_ok = "subject:" in text or "## subject" in text
    return recipient_ok and subject_ok


def packet_files(packet_dir: Path) -> set[str]:
    return {
        rel(path)
        for path in packet_dir.glob("*.md")
        if path.name != "README_V45.md"
    }


def main() -> int:
    args = parse_args()
    external_path = resolve(args.external)
    packet_dir = resolve(args.packet_dir)
    outdir = resolve(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    route_rows = read_tsv(external_path)
    if args.synthetic_case == "missing_packet" and route_rows:
        route_rows = [dict(row) for row in route_rows]
        route_rows[0]["request_packet"] = "docs/validation/outbound_requests/SYNTHETIC_MISSING_REQUEST.md"

    mapped_packets = {row.get("request_packet", "") for row in route_rows if row.get("request_packet", "")}
    extra_packets = sorted(packet_files(packet_dir) - mapped_packets)

    manifest_rows: list[dict[str, str]] = []
    issues: list[dict[str, str]] = []

    def add_issue(severity: str, cohort_id: str, check: str, detail: str) -> None:
        issues.append({"severity": severity, "cohort_id": cohort_id, "check": check, "detail": detail})

    for row in sorted(route_rows, key=lambda item: item.get("cohort_id", "")):
        cohort_id = row.get("cohort_id", "")
        packet_rel = row.get("request_packet", "")
        packet_path = resolve(Path(packet_rel))
        exists = packet_path.exists() and packet_path.is_file()
        nonempty = exists and packet_path.stat().st_size > 0
        guard_language = has_guard_language(packet_path)
        recipient_subject = has_recipient_and_subject(packet_path)

        if not packet_rel:
            add_issue("hard", cohort_id, "request_packet_blank", "external blocker board row lacks request_packet")
        if not exists:
            add_issue("hard", cohort_id, "request_packet_missing", f"missing request packet: {packet_rel}")
        if exists and not nonempty:
            add_issue("hard", cohort_id, "request_packet_empty", f"empty request packet: {packet_rel}")
        if exists and not guard_language:
            add_issue("hard", cohort_id, "send_guard_language_missing", "packet lacks send-only-if and save-sent-copy guard language")
        if exists and not recipient_subject:
            add_issue("hard", cohort_id, "recipient_or_subject_missing", "packet lacks To:/Subject: fields")

        manifest_rows.append(
            {
                "cohort_id": cohort_id,
                "role": row.get("role", ""),
                "request_packet": packet_rel,
                "exists": str(exists).lower(),
                "nonempty": str(nonempty).lower(),
                "send_guard_language": str(guard_language).lower(),
                "recipient_and_subject": str(recipient_subject).lower(),
                "size_bytes": str(packet_path.stat().st_size) if exists else "",
                "sha256": sha256(packet_path) if exists else "",
            }
        )

    for packet in extra_packets:
        add_issue("soft", "unmapped_packet", "packet_not_in_external_board", f"packet exists but is not mapped to a live route: {packet}")

    manifest_path = outdir / "outbound_request_packet_manifest.tsv"
    issues_path = outdir / "outbound_request_packet_issues.tsv"
    write_tsv(
        manifest_path,
        manifest_rows,
        [
            "cohort_id",
            "role",
            "request_packet",
            "exists",
            "nonempty",
            "send_guard_language",
            "recipient_and_subject",
            "size_bytes",
            "sha256",
        ],
    )
    write_tsv(issues_path, issues, ["severity", "cohort_id", "check", "detail"])

    n_hard = sum(1 for row in issues if row["severity"] == "hard")
    n_soft = sum(1 for row in issues if row["severity"] == "soft")
    observed = "PASS" if n_hard == 0 else "FAIL"
    summary = {
        "synthetic": args.synthetic_case != "none",
        "synthetic_case": args.synthetic_case,
        "purpose": "V45 outbound request packet completeness/checksum guard; no biological claim",
        "observed_status": observed,
        "expected_status": args.expect_status,
        "expectation_met": observed == args.expect_status,
        "n_routes": len(route_rows),
        "n_packets_hashed": sum(1 for row in manifest_rows if row["exists"] == "true"),
        "n_hard_issues": n_hard,
        "n_soft_issues": n_soft,
        "manifest": rel(manifest_path),
        "issues": rel(issues_path),
        "sources": {
            "external": rel(external_path),
            "packet_dir": rel(packet_dir),
        },
    }
    (outdir / "outbound_request_packet_integrity_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["expectation_met"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
