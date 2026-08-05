#!/usr/bin/env python3
"""Select and retrieve the frozen GSE247181 rapid/slow SPMS CEL cohort."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import os
from pathlib import Path
import shutil
import sys
import urllib.request


SERIES_FIELDS = {
    "!Sample_title",
    "!Sample_geo_accession",
    "!Sample_source_name_ch1",
    "!Sample_characteristics_ch1",
    "!Sample_supplementary_file",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--series-matrix",
        type=Path,
        default=Path("data/raw/gse247181/GSE247181_series_matrix.txt.gz"),
    )
    parser.add_argument(
        "--file-list",
        type=Path,
        default=Path("data/raw/gse247181/filelist.txt"),
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path("data/raw/gse247181/eligible_cel"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("analysis/v56_gse247181_progression_modules"),
    )
    parser.add_argument("--download", action="store_true")
    return parser.parse_args()


def read_series(path: Path) -> list[dict[str, str]]:
    rows: dict[str, list[list[str]]] = {}
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.startswith("!Sample_"):
                continue
            parsed = next(csv.reader([line.rstrip("\n")], delimiter="\t"))
            if parsed[0] in SERIES_FIELDS:
                rows.setdefault(parsed[0], []).append(parsed[1:])

    accessions = rows["!Sample_geo_accession"][0]
    n_samples = len(accessions)
    for key, blocks in rows.items():
        if any(len(block) != n_samples for block in blocks):
            raise ValueError(f"metadata width mismatch for {key}")

    records: list[dict[str, str]] = []
    for index, accession in enumerate(accessions):
        characteristics: dict[str, str] = {}
        for block in rows["!Sample_characteristics_ch1"]:
            value = block[index]
            if ":" not in value:
                raise ValueError(f"unparsed characteristic for {accession}: {value}")
            key, item = value.split(":", 1)
            characteristics[key.strip().lower()] = item.strip()

        supplementary = [
            block[index] for block in rows["!Sample_supplementary_file"]
        ]
        cel_urls = [url for url in supplementary if url.lower().endswith(".cel.gz")]
        if len(cel_urls) != 1:
            raise ValueError(f"expected one CEL URL for {accession}, found {cel_urls}")
        records.append(
            {
                "geo_accession": accession,
                "title": rows["!Sample_title"][0][index],
                "source": rows["!Sample_source_name_ch1"][0][index],
                "sex": characteristics.get("sex", ""),
                "treatment": characteristics.get("treatment duration (hours)", ""),
                "ms_type": characteristics.get("ms-type", ""),
                "cel_url": cel_urls[0].replace("ftp://", "https://"),
            }
        )
    return records


def expected_sizes(path: Path) -> dict[str, int]:
    sizes: dict[str, int] = {}
    with path.open(encoding="utf-8") as handle:
        reader = csv.reader(handle, delimiter="\t")
        next(reader)
        for row in reader:
            if len(row) >= 5 and row[0] == "File":
                sizes[row[1]] = int(row[3])
    return sizes


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, destination: Path, expected_size: int) -> None:
    if destination.exists() and destination.stat().st_size == expected_size:
        return
    partial = destination.with_suffix(destination.suffix + ".part")
    partial.unlink(missing_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "ms-auto-research/56"})
    with urllib.request.urlopen(request, timeout=180) as response, partial.open("wb") as out:
        shutil.copyfileobj(response, out, length=1024 * 1024)
    size = partial.stat().st_size
    if size != expected_size:
        partial.unlink(missing_ok=True)
        raise IOError(f"size mismatch for {url}: expected {expected_size}, got {size}")
    os.replace(partial, destination)


def main() -> int:
    args = parse_args()
    records = read_series(args.series_matrix)
    sizes = expected_sizes(args.file_list)

    eligible = []
    for record in records:
        if record["treatment"] != "Untreated":
            continue
        if record["ms_type"] not in {"SPMS-s", "SPMS-a"}:
            continue
        item = dict(record)
        item["progression_group"] = (
            "slow" if record["ms_type"] == "SPMS-s" else "rapid"
        )
        item["file_name"] = Path(record["cel_url"]).name
        if item["file_name"] not in sizes:
            raise ValueError(f"file absent from NCBI list: {item['file_name']}")
        item["expected_bytes"] = sizes[item["file_name"]]
        eligible.append(item)

    counts = {
        group: sum(item["progression_group"] == group for item in eligible)
        for group in ("slow", "rapid")
    }
    if len(eligible) != 20 or counts != {"slow": 10, "rapid": 10}:
        raise ValueError(f"frozen cohort mismatch: n={len(eligible)}, groups={counts}")
    if len({item["geo_accession"] for item in eligible}) != 20:
        raise ValueError("duplicate eligible accession")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.raw_dir.mkdir(parents=True, exist_ok=True)
    if args.download:
        for index, item in enumerate(eligible, start=1):
            destination = args.raw_dir / item["file_name"]
            print(f"[{index:02d}/20] {item['geo_accession']} {item['progression_group']}")
            download(item["cel_url"], destination, int(item["expected_bytes"]))
            item["local_path"] = str(destination)
            item["observed_bytes"] = destination.stat().st_size
            item["sha256"] = sha256(destination)
    else:
        for item in eligible:
            destination = args.raw_dir / item["file_name"]
            item["local_path"] = str(destination)
            item["observed_bytes"] = destination.stat().st_size if destination.exists() else ""
            item["sha256"] = sha256(destination) if destination.exists() else ""

    fields = [
        "geo_accession",
        "title",
        "source",
        "sex",
        "treatment",
        "ms_type",
        "progression_group",
        "cel_url",
        "file_name",
        "expected_bytes",
        "observed_bytes",
        "sha256",
        "local_path",
    ]
    manifest = args.output_dir / "retrieval_manifest.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(eligible)
    print(f"wrote {manifest}; groups={counts}; download={args.download}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
