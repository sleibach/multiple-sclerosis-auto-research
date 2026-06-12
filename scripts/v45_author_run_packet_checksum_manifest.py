#!/usr/bin/env python3
"""Write or verify checksums for the V45 author-run packet bundle.

This hashes only committed, non-sensitive packet files listed for inclusion in
the author-run packet index. It does not touch raw, quarantined, or private
data.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "analysis/v45_author_run_packet_bundle/author_run_packet_bundle_index.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v45_author_run_packet_checksums"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    write = sub.add_parser("write")
    write.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    write.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)

    verify = sub.add_parser("verify")
    verify.add_argument("--manifest", type=Path, required=True)
    verify.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR / "verify")
    verify.add_argument("--fail-on-error", action="store_true")

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


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def included_rows(index_path: Path) -> list[dict[str, str]]:
    rows = []
    for row in read_tsv(index_path):
        include = row.get("include_in_author_packet", "").strip().lower()
        if include != "yes":
            continue
        rows.append(row)
    return rows


def write_manifest(index_path: Path, outdir: Path) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for row in included_rows(index_path):
        packet_path = ROOT / row["path"]
        exists = packet_path.exists() and packet_path.is_file()
        rows.append(
            {
                "section": row.get("section", ""),
                "artifact_role": row.get("artifact_role", ""),
                "path": row.get("path", ""),
                "required_or_optional": row.get("required_or_optional", ""),
                "exists": "yes" if exists else "no",
                "size_bytes": packet_path.stat().st_size if exists else "",
                "sha256": sha256(packet_path) if exists else "",
            }
        )
    manifest = outdir / "author_run_packet_sha256_manifest.tsv"
    write_tsv(
        manifest,
        rows,
        ["section", "artifact_role", "path", "required_or_optional", "exists", "size_bytes", "sha256"],
    )
    n_missing = sum(1 for row in rows if row["exists"] != "yes")
    summary = {
        "synthetic": False,
        "purpose": "author-run packet checksum manifest; no biological claim",
        "index": rel(index_path),
        "manifest": rel(manifest),
        "n_included": len(rows),
        "n_missing": n_missing,
        "overall_status": "PASS" if n_missing == 0 else "FAIL",
    }
    (outdir / "author_run_packet_checksum_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_missing == 0 else 2


def verify_manifest(manifest_path: Path, outdir: Path, fail_on_error: bool) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for row in read_tsv(manifest_path):
        packet_path = ROOT / row["path"]
        exists = packet_path.exists() and packet_path.is_file()
        observed = sha256(packet_path) if exists else ""
        expected = row.get("sha256", "")
        status = "PASS" if exists and observed == expected else ("MISSING" if not exists else "HASH_MISMATCH")
        rows.append(
            {
                **row,
                "observed_sha256": observed,
                "verify_status": status,
            }
        )
    audit = outdir / "author_run_packet_checksum_verify.tsv"
    write_tsv(
        audit,
        rows,
        [
            "section",
            "artifact_role",
            "path",
            "required_or_optional",
            "exists",
            "size_bytes",
            "sha256",
            "observed_sha256",
            "verify_status",
        ],
    )
    n_fail = sum(1 for row in rows if row["verify_status"] != "PASS")
    summary = {
        "synthetic": "synthetic" in rel(manifest_path).lower(),
        "purpose": "author-run packet checksum verification; no biological claim",
        "manifest": rel(manifest_path),
        "audit": rel(audit),
        "n_rows": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "author_run_packet_checksum_verify_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if fail_on_error and n_fail else 0


def synthetic_check(outdir: Path) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    write_rc = write_manifest(DEFAULT_INDEX, outdir / "write")
    manifest = outdir / "write/author_run_packet_sha256_manifest.tsv"
    verify_rc = verify_manifest(manifest, outdir / "verify", True)

    broken_manifest = outdir / "synthetic_broken_manifest.tsv"
    shutil.copy2(manifest, broken_manifest)
    rows = read_tsv(broken_manifest)
    if rows:
        rows[0]["sha256"] = "0" * 64
    write_tsv(
        broken_manifest,
        rows,
        ["section", "artifact_role", "path", "required_or_optional", "exists", "size_bytes", "sha256"],
    )
    broken_verify_rc = verify_manifest(broken_manifest, outdir / "synthetic_broken_verify", False)
    broken_summary = json.loads((outdir / "synthetic_broken_verify/author_run_packet_checksum_verify_summary.json").read_text())
    verify_summary = json.loads((outdir / "verify/author_run_packet_checksum_verify_summary.json").read_text())
    summary = {
        "synthetic": True,
        "purpose": "author-run packet checksum synthetic regression; no biological claim",
        "write_exit_code": write_rc,
        "verify_exit_code": verify_rc,
        "verify_status": verify_summary["overall_status"],
        "synthetic_broken_verify_exit_code_without_fail_on_error": broken_verify_rc,
        "synthetic_broken_verify_status": broken_summary["overall_status"],
        "synthetic_broken_n_fail": broken_summary["n_fail"],
    }
    (outdir / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return 0 if write_rc == 0 and verify_rc == 0 and broken_summary["overall_status"] == "FAIL" else 2


def main() -> int:
    args = parse_args()
    if args.cmd == "write":
        return write_manifest(resolve(args.index), resolve(args.outdir))
    if args.cmd == "verify":
        return verify_manifest(resolve(args.manifest), resolve(args.outdir), args.fail_on_error)
    return synthetic_check(resolve(args.outdir))


if __name__ == "__main__":
    raise SystemExit(main())
