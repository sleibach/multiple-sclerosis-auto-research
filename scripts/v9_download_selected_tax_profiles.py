#!/usr/bin/env python3
"""Download selected IBDMDB taxonomic-profile BIOM files."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
from pathlib import Path
import urllib.request

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_URLS = ROOT / "analysis" / "v9_microbiome" / "ibdmdb_subset" / "selected_tax_profile_urls.tsv"
DEFAULT_OUT = ROOT / "data" / "raw" / "v9_microbiome_ibd" / "tax_profiles_subset"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", type=Path, default=DEFAULT_URLS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--workers", type=int, default=1)
    return parser.parse_args()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    urls = pd.read_csv(args.urls, sep="\t")

    def fetch(row: dict[str, object]) -> dict[str, object]:
        sample_id = str(row["sample_id"])
        url = str(row["url"])
        out_path = args.out_dir / f"{sample_id}.biom"
        status = "exists"
        if not out_path.exists() or out_path.stat().st_size == 0:
            status = "downloaded"
            with urllib.request.urlopen(url, timeout=120) as response:
                out_path.write_bytes(response.read())
        return {
            "sample_id": sample_id,
            "url": url,
            "path": str(out_path),
            "bytes": out_path.stat().st_size,
            "sha256": sha256(out_path),
            "status": status,
        }

    input_rows = urls.to_dict(orient="records")
    if args.workers <= 1:
        rows = [fetch(row) for row in input_rows]
    else:
        rows = []
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(fetch, row) for row in input_rows]
            for future in as_completed(futures):
                rows.append(future.result())
        rows.sort(key=lambda row: str(row["sample_id"]))
    manifest = args.manifest or args.out_dir / "download_manifest.tsv"
    pd.DataFrame(rows).to_csv(manifest, sep="\t", index=False)
    print(f"wrote {manifest} with {len(rows)} rows")


if __name__ == "__main__":
    main()
