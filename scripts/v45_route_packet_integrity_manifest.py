#!/usr/bin/env python3
"""Build and verify a V45 route-arrival packet integrity manifest.

This is an operational guard only. It hashes generated command packets and
checks freshness against their source tracker/acquisition/generator inputs. It
does not inspect real validation data or run any scoring.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET_DIR = ROOT / "analysis/v45_route_arrival_packets"
DEFAULT_OUTDIR = ROOT / "analysis/v45_route_packet_integrity_manifest/live"
SOURCE_PATHS = [
    ROOT / "scripts/v45_route_arrival_packet_generator.py",
    ROOT / "analysis/v45_live_cohort_acquisition_index/live_cohort_acquisition_index.tsv",
    ROOT / "analysis/v45_outbound_data_requests/request_tracker.tsv",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def utc_mtime(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat().replace("+00:00", "Z")


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
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_expected_packets(packet_dir: Path, synthetic_case: str) -> tuple[list[dict[str, str]], dict[str, object]]:
    index_path = packet_dir / "route_arrival_packet_index.tsv"
    summary_path = packet_dir / "route_arrival_packet_summary.json"
    index_rows = read_tsv(index_path)
    summary = json.loads(summary_path.read_text())
    if synthetic_case == "missing_packet":
        index_rows = deepcopy(index_rows)
        if index_rows:
            index_rows[0]["packet"] = "analysis/v45_route_arrival_packets/SYNTHETIC_MISSING_PACKET.md"
    return index_rows, summary


def main() -> int:
    args = parse_args()
    packet_dir = args.packet_dir if args.packet_dir.is_absolute() else ROOT / args.packet_dir
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    index_rows, summary = load_expected_packets(packet_dir, args.synthetic_case)
    summary_packets = set(summary.get("packets", []))
    max_source_mtime = max(path.stat().st_mtime for path in SOURCE_PATHS if path.exists())
    source_rows = [
        {
            "source": rel(path),
            "exists": str(path.exists()).lower(),
            "mtime_utc": utc_mtime(path) if path.exists() else "",
            "sha256": sha256(path) if path.exists() else "",
            "bytes": str(path.stat().st_size) if path.exists() else "",
        }
        for path in SOURCE_PATHS
    ]

    manifest_rows: list[dict[str, str]] = []
    violations: list[dict[str, str]] = []
    for row in index_rows:
        packet_rel = row.get("packet", "")
        packet_path = ROOT / packet_rel
        exists = packet_path.exists()
        status = "PASS"
        if not exists:
            status = "MISSING"
            violations.append(
                {
                    "severity": "hard",
                    "packet": packet_rel,
                    "check": "packet_exists",
                    "detail": "packet listed in index does not exist",
                }
            )
        elif packet_path.stat().st_mtime < max_source_mtime:
            status = "STALE"
            violations.append(
                {
                    "severity": "hard",
                    "packet": packet_rel,
                    "check": "packet_freshness",
                    "detail": "packet mtime is older than at least one source input",
                }
            )
        if packet_rel not in summary_packets:
            violations.append(
                {
                    "severity": "hard",
                    "packet": packet_rel,
                    "check": "summary_membership",
                    "detail": "packet listed in index is absent from route_arrival_packet_summary.json",
                }
            )
            if status == "PASS":
                status = "SUMMARY_MISMATCH"
        manifest_rows.append(
            {
                "cohort_id": row.get("cohort_id", ""),
                "packet": packet_rel,
                "exists": str(exists).lower(),
                "status": status,
                "bytes": str(packet_path.stat().st_size) if exists else "",
                "sha256": sha256(packet_path) if exists else "",
                "mtime_utc": utc_mtime(packet_path) if exists else "",
                "role": row.get("role", ""),
                "blocker": row.get("blocker", ""),
            }
        )

    expected_n = int(summary.get("n_packets", -1))
    if expected_n != len(index_rows):
        violations.append(
            {
                "severity": "hard",
                "packet": "route_arrival_packet_index.tsv",
                "check": "packet_count",
                "detail": f"summary n_packets={expected_n}; index rows={len(index_rows)}",
            }
        )

    manifest_path = outdir / "route_packet_integrity_manifest.tsv"
    source_path = outdir / "route_packet_integrity_sources.tsv"
    violation_path = outdir / "route_packet_integrity_violations.tsv"
    write_tsv(
        manifest_path,
        manifest_rows,
        ["cohort_id", "packet", "exists", "status", "bytes", "sha256", "mtime_utc", "role", "blocker"],
    )
    write_tsv(source_path, source_rows, ["source", "exists", "mtime_utc", "sha256", "bytes"])
    write_tsv(violation_path, violations, ["severity", "packet", "check", "detail"])

    n_hard = sum(1 for row in violations if row["severity"] == "hard")
    observed = "PASS" if n_hard == 0 else "FAIL"
    out_summary = {
        "synthetic": args.synthetic_case != "none",
        "synthetic_case": args.synthetic_case,
        "purpose": "V45 route-arrival packet checksum/freshness guard; no biological claim",
        "observed_status": observed,
        "expected_status": args.expect_status,
        "expectation_met": observed == args.expect_status,
        "n_packets": len(manifest_rows),
        "n_hard_violations": n_hard,
        "manifest": rel(manifest_path),
        "sources": rel(source_path),
        "violations": rel(violation_path),
        "packet_dir": rel(packet_dir),
    }
    (outdir / "route_packet_integrity_summary.json").write_text(json.dumps(out_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out_summary, indent=2, sort_keys=True))
    return 0 if out_summary["expectation_met"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
