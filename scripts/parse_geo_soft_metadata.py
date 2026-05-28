#!/usr/bin/env python3
"""Extract sample-level metadata from GEO SOFT family files."""

from __future__ import annotations

import argparse
import csv
import gzip
from pathlib import Path


def parse_soft(path: Path) -> list[dict[str, str]]:
    samples: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    with gzip.open(path, "rt", errors="replace") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line.startswith("^SAMPLE = "):
                if current:
                    samples.append(current)
                current = {"geo_accession": line.split(" = ", 1)[1]}
            elif current is not None and line.startswith("!Sample_"):
                key, value = line[1:].split(" = ", 1)
                if key == "Sample_characteristics_ch1":
                    values = current.setdefault(key, "")
                    current[key] = f"{values} | {value}" if values else value
                elif key in current:
                    current[key] = f"{current[key]} | {value}"
                else:
                    current[key] = value

    if current:
        samples.append(current)
    return samples


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("soft_gz", type=Path)
    parser.add_argument("out_tsv", type=Path)
    args = parser.parse_args()

    rows = parse_soft(args.soft_gz)
    args.out_tsv.parent.mkdir(parents=True, exist_ok=True)

    preferred = [
        "geo_accession",
        "Sample_title",
        "Sample_source_name_ch1",
        "Sample_organism_ch1",
        "Sample_characteristics_ch1",
        "Sample_molecule_ch1",
        "Sample_extract_protocol_ch1",
        "Sample_data_processing",
        "Sample_platform_id",
    ]
    fields = preferred + sorted({key for row in rows for key in row if key not in preferred})

    with args.out_tsv.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    summary = args.out_tsv.with_suffix(".summary.txt")
    summary.write_text(f"samples\t{len(rows)}\nsource\t{args.soft_gz}\n")


if __name__ == "__main__":
    main()
