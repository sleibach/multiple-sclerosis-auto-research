#!/usr/bin/env python3
"""Write and verify lightweight SHA256 manifests for handoff packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v45_checksum_manifest_validator"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def package_files(root: Path, manifest_path: Path | None = None) -> list[Path]:
    root = root.resolve()
    manifest_resolved = manifest_path.resolve() if manifest_path else None
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if manifest_resolved and path.resolve() == manifest_resolved:
            continue
        files.append(path)
    return files


def write_manifest(root: Path, manifest: Path) -> pd.DataFrame:
    root = root.resolve()
    manifest.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in package_files(root, manifest):
        rel = str(path.relative_to(root))
        rows.append(
            {
                "relative_path": rel,
                "sha256": sha256(path),
                "bytes": int(path.stat().st_size),
            }
        )
    table = pd.DataFrame(rows, columns=["relative_path", "sha256", "bytes"])
    table.to_csv(manifest, sep="\t", index=False)
    return table


def verify_manifest(root: Path, manifest: Path, outdir: Path) -> dict[str, object]:
    root = root.resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    expected = pd.read_csv(manifest, sep="\t")
    rows = []
    for _, row in expected.iterrows():
        rel = str(row["relative_path"])
        path = root / rel
        exists = path.exists()
        observed_sha = sha256(path) if exists else ""
        observed_bytes = int(path.stat().st_size) if exists else 0
        expected_sha = str(row["sha256"]).lower()
        status = "PASS"
        if not exists:
            status = "FAIL_MISSING_FILE"
        elif observed_sha.lower() != expected_sha:
            status = "FAIL_SHA256_MISMATCH"
        elif "bytes" in expected.columns and pd.notna(row["bytes"]) and int(row["bytes"]) != observed_bytes:
            status = "FAIL_BYTE_COUNT_MISMATCH"
        rows.append(
            {
                "relative_path": rel,
                "expected_sha256": expected_sha,
                "observed_sha256": observed_sha,
                "expected_bytes": int(row["bytes"]) if "bytes" in expected.columns and pd.notna(row["bytes"]) else "",
                "observed_bytes": observed_bytes,
                "status": status,
            }
        )

    manifest_paths = set(expected["relative_path"].astype(str))
    extra_files = sorted(str(path.relative_to(root)) for path in package_files(root, manifest) if str(path.relative_to(root)) not in manifest_paths)
    for rel in extra_files:
        path = root / rel
        rows.append(
            {
                "relative_path": rel,
                "expected_sha256": "",
                "observed_sha256": sha256(path),
                "expected_bytes": "",
                "observed_bytes": int(path.stat().st_size),
                "status": "WARN_EXTRA_FILE_NOT_IN_MANIFEST",
            }
        )

    audit = pd.DataFrame(rows)
    audit.to_csv(outdir / "manifest_audit.tsv", sep="\t", index=False)
    n_fail = int(audit["status"].astype(str).str.startswith("FAIL").sum())
    n_warn = int(audit["status"].astype(str).str.startswith("WARN").sum())
    summary = {
        "root": str(root),
        "manifest": str(manifest),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "n_manifest_rows": int(len(expected)),
        "n_audit_rows": int(len(audit)),
        "n_fail": n_fail,
        "n_warn": n_warn,
    }
    (outdir / "manifest_audit_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def run_synthetic_check(outdir: Path) -> dict[str, object]:
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    package = outdir / "synthetic_package"
    package.mkdir()
    (package / "README.txt").write_text("synthetic package\n")
    (package / "metadata.tsv").write_text("sample_id\tsubject\nS1\tP1\n")
    manifest = outdir / "synthetic_manifest.tsv"
    write_manifest(package, manifest)
    pass_summary = verify_manifest(package, manifest, outdir / "pass_verify")
    (package / "metadata.tsv").write_text("sample_id\tsubject\nS1\tP2\n")
    fail_summary = verify_manifest(package, manifest, outdir / "fail_verify")
    assertions = {
        "synthetic": True,
        "pass_manifest_verifies": pass_summary["overall_status"] == "PASS",
        "modified_file_fails": fail_summary["overall_status"] == "FAIL",
        "pass_summary": pass_summary,
        "fail_summary": fail_summary,
    }
    assertions["overall_status"] = (
        "PASS"
        if assertions["pass_manifest_verifies"] and assertions["modified_file_fails"]
        else "FAIL"
    )
    (outdir / "synthetic_check_assertions.json").write_text(json.dumps(assertions, indent=2, sort_keys=True) + "\n")
    return assertions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    write = sub.add_parser("write", help="Write SHA256 manifest for a folder.")
    write.add_argument("--root", required=True, type=Path)
    write.add_argument("--manifest", required=True, type=Path)

    verify = sub.add_parser("verify", help="Verify a SHA256 manifest.")
    verify.add_argument("--root", required=True, type=Path)
    verify.add_argument("--manifest", required=True, type=Path)
    verify.add_argument("--outdir", required=True, type=Path)
    verify.add_argument("--fail-on-error", action="store_true")

    synth = sub.add_parser("synthetic-check", help="Run seeded pass/fail manifest checks.")
    synth.add_argument("--outdir", required=True, type=Path)

    args = parser.parse_args()
    if args.command == "write":
        table = write_manifest(args.root, args.manifest)
        print(json.dumps({"manifest": str(args.manifest), "n_files": int(len(table))}, indent=2, sort_keys=True))
        return 0
    if args.command == "verify":
        summary = verify_manifest(args.root, args.manifest, args.outdir)
        print(json.dumps(summary, indent=2, sort_keys=True))
        if args.fail_on_error and summary["overall_status"] != "PASS":
            return 2
        return 0
    assertions = run_synthetic_check(args.outdir)
    print(json.dumps(assertions, indent=2, sort_keys=True))
    return 0 if assertions["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
