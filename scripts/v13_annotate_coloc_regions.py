#!/usr/bin/env python3
"""Annotate V13 coloc regions with nearby GRCh37 Ensembl genes."""

from __future__ import annotations

import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v13_genetics_coloc"
RAW = OUT / "raw_gene_annotations"
RAW.mkdir(parents=True, exist_ok=True)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open() as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def fetch_genes(chrom: str, start: int, end: int) -> list[dict]:
    cache = RAW / f"grch37_chr{chrom}_{start}_{end}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    region = urllib.parse.quote(f"{chrom}:{start}-{end}")
    url = f"https://grch37.rest.ensembl.org/overlap/region/human/{region}?feature=gene"
    req = urllib.request.Request(url, headers={"Content-Type": "application/json", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    cache.write_bytes(data)
    time.sleep(0.1)
    return json.loads(data.decode("utf-8"))


def main() -> None:
    rows = read_rows(OUT / "coloc_region_summary.tsv")
    annotated: list[dict[str, object]] = []
    for row in rows:
        chrom = row["chr"]
        start = int(row["start"])
        end = int(row["end"])
        genes = fetch_genes(chrom, start, end)
        protein_coding = [
            g for g in genes if str(g.get("biotype", "")).lower() == "protein_coding"
        ]
        symbols = sorted(
            {
                str(g.get("external_name") or g.get("id"))
                for g in protein_coding
                if g.get("external_name") or g.get("id")
            }
        )
        annotated.append(
            {
                **row,
                "n_protein_coding_genes": len(symbols),
                "protein_coding_genes": ";".join(symbols[:40]),
            }
        )
    write_tsv(
        OUT / "coloc_region_summary_annotated.tsv",
        annotated,
        list(rows[0].keys()) + ["n_protein_coding_genes", "protein_coding_genes"] if rows else [],
    )
    print(json.dumps({"annotated_regions": len(annotated)}, indent=2))


if __name__ == "__main__":
    main()
