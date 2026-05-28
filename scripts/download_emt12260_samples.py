#!/usr/bin/env python3
"""Download E-MTAB-12260 per-sample count tables listed in the SDRF."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SDRF = ROOT / "data/raw/E-MTAB-12260/E-MTAB-12260.sdrf.txt"
OUT_DIR = ROOT / "data/raw/E-MTAB-12260/samples"
DERIVED = ROOT / "data/derived/E-MTAB-12260"
BASE_URL = "https://www.ebi.ac.uk/biostudies/files/E-MTAB-12260"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)

    with SDRF.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    files = sorted({row["Derived Array Data File"] for row in rows if row.get("Derived Array Data File")})
    manifest_rows = []
    for filename in files:
        out_path = OUT_DIR / filename
        if not out_path.exists() or out_path.stat().st_size == 0:
            url = f"{BASE_URL}/{filename}"
            subprocess.run(["curl", "-L", url, "-o", str(out_path)], check=True)
        manifest_rows.append(
            {
                "file": filename,
                "path": str(out_path.relative_to(ROOT)),
                "size_bytes": out_path.stat().st_size,
                "sha256": sha256(out_path),
            }
        )

    manifest_path = DERIVED / "sample_file_manifest.tsv"
    with manifest_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["file", "path", "size_bytes", "sha256"])
        writer.writeheader()
        writer.writerows(manifest_rows)
    print(f"downloaded_or_verified={len(manifest_rows)} manifest={manifest_path}")


if __name__ == "__main__":
    main()
