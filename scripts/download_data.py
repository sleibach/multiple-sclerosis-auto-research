#!/usr/bin/env python3
"""Download the preregistered public inputs and record cryptographic hashes."""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


FILES = [
    {
        "accession": "GSE180759",
        "role": "discovery_annotation",
        "filename": "GSE180759_annotation.txt.gz",
        "url": (
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE180nnn/GSE180759/"
            "suppl/GSE180759_annotation.txt.gz"
        ),
    },
    {
        "accession": "GSE180759",
        "role": "discovery_expression",
        "filename": "GSE180759_expression_matrix.csv.gz",
        "url": (
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE180nnn/GSE180759/"
            "suppl/GSE180759_expression_matrix.csv.gz"
        ),
    },
    {
        "accession": "GSE279972",
        "role": "validation_expression_archive",
        "filename": "GSE279972_RAW.tar",
        "url": (
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE279nnn/GSE279972/"
            "suppl/GSE279972_RAW.tar"
        ),
    },
    {
        "accession": "GSE279972",
        "role": "validation_metadata_soft",
        "filename": "GSE279972_family.soft.gz",
        "url": (
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE279nnn/GSE279972/"
            "soft/GSE279972_family.soft.gz"
        ),
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download(url: str, target: Path, force: bool) -> None:
    if target.exists() and not force:
        print(f"reuse {target}", file=sys.stderr)
        return
    part = target.with_suffix(target.suffix + ".part")
    if part.exists():
        part.unlink()
    print(f"download {url}", file=sys.stderr)
    with urllib.request.urlopen(url) as response, part.open("wb") as output:
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            output.write(block)
    part.replace(target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument(
        "--manifest", type=Path, default=Path("data/derived/data_manifest.tsv")
    )
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    args.raw_dir.mkdir(parents=True, exist_ok=True)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)

    manifest_rows = []
    retrieved_at = datetime.now(timezone.utc).isoformat()
    for spec in FILES:
        target = args.raw_dir / spec["filename"]
        download(spec["url"], target, args.force)
        manifest_rows.append(
            {
                **spec,
                "bytes": target.stat().st_size,
                "sha256": sha256(target),
                "retrieved_at_utc": retrieved_at,
            }
        )

    with args.manifest.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            fieldnames=[
                "accession",
                "role",
                "filename",
                "url",
                "bytes",
                "sha256",
                "retrieved_at_utc",
            ],
        )
        writer.writeheader()
        writer.writerows(manifest_rows)
    print(f"wrote {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
