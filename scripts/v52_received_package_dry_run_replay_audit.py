#!/usr/bin/env python3
"""Replay the V52 received-package dry run and compare classifier output."""

from __future__ import annotations

import argparse
import csv
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "analysis/received_package_intake/20260710_synthetic_monitoring_manifest/manifest.tsv"
DEFAULT_EXPECTED = ROOT / "analysis/received_package_intake/20260710_synthetic_monitoring_manifest/route_classification.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v52_received_package_dry_run_replay"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--expected", type=Path, default=DEFAULT_EXPECTED)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    replayed = args.outdir / "replayed_route_classification.tsv"
    summary = args.outdir / "dry_run_replay_summary.tsv"

    subprocess.run(
        [
            "python3",
            "scripts/v52_package_route_classifier.py",
            "--manifests",
            str(args.manifest.relative_to(ROOT)),
            "--out",
            str(replayed.relative_to(ROOT)),
        ],
        cwd=ROOT,
        check=True,
    )

    expected_rows = read_tsv(args.expected)
    replayed_rows = read_tsv(replayed)
    matches = expected_rows == replayed_rows

    rows = [
        {"metric": "manifest", "value": str(args.manifest.relative_to(ROOT))},
        {"metric": "expected_output", "value": str(args.expected.relative_to(ROOT))},
        {"metric": "replayed_output", "value": str(replayed.relative_to(ROOT))},
        {"metric": "expected_rows", "value": str(len(expected_rows))},
        {"metric": "replayed_rows", "value": str(len(replayed_rows))},
        {"metric": "exact_row_match", "value": str(matches)},
    ]
    with summary.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print({"summary": str(summary), "exact_row_match": matches})
    if args.fail_on_error and not matches:
        raise SystemExit({"expected": expected_rows, "replayed": replayed_rows})


if __name__ == "__main__":
    main()
