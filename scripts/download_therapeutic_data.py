#!/usr/bin/env python3
"""Download spatial therapeutic-discovery inputs with SHA-256 provenance."""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
import urllib.request
from pathlib import Path


FILES = [
    {
        "accession": "GSE284005",
        "role": "human_chronic_active_ms_merfish_raw",
        "filename": "GSE284005_RAW.tar",
        "url": (
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE284nnn/GSE284005/"
            "suppl/GSE284005_RAW.tar"
        ),
    },
    {
        "accession": "GSE284005",
        "role": "human_chronic_active_ms_merfish_metadata_soft",
        "filename": "GSE284005_family.soft.gz",
        "url": (
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE284nnn/GSE284005/"
            "soft/GSE284005_family.soft.gz"
        ),
    },
    {
        "accession": "GSE301908",
        "role": "independent_human_chronic_active_ms_snrnaseq_seurat_object",
        "filename": "GSE301908_sn_all.rds",
        "url": (
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE301nnn/GSE301908/"
            "suppl/GSE301908_sn_all.rds"
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
    if part.exists() and force:
        part.unlink()
    offset = part.stat().st_size if part.exists() else 0
    request = urllib.request.Request(
        url, headers={"Range": f"bytes={offset}-"} if offset else {}
    )
    action = f"resume at {offset} bytes" if offset else "download"
    print(f"{action} {url}", file=sys.stderr)
    with urllib.request.urlopen(request, timeout=60) as response:
        if offset and response.status != 206:
            raise RuntimeError(
                f"server did not honor ranged resume for {target}; remove {part} and retry"
            )
        mode = "ab" if offset else "wb"
        output = part.open(mode)
        try:
            while block := response.read(1024 * 1024):
                output.write(block)
        finally:
            output.close()
    part.replace(target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("data/derived/therapeutic_data_manifest.tsv"),
    )
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    args.raw_dir.mkdir(parents=True, exist_ok=True)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)

    manifest_rows = []
    for spec in FILES:
        target = args.raw_dir / spec["filename"]
        download(spec["url"], target, args.force)
        manifest_rows.append({**spec, "bytes": target.stat().st_size, "sha256": sha256(target)})

    with args.manifest.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            fieldnames=["accession", "role", "filename", "url", "bytes", "sha256"],
        )
        writer.writeheader()
        writer.writerows(manifest_rows)
    print(f"wrote {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
