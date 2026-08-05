#!/usr/bin/env python3
"""Prepare ignored GeoMx inputs and committed metadata for V56 reconstruction."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import shutil
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/gse281805"
WORK = RAW / "reconstruction"
OUT = ROOT / "analysis/v56_gse281805_raw_reconstruction"
SOURCE_MATRIX = RAW / "41591_2025_3625_MOESM5_ESM.xlsx"
PKC_GZ = RAW / "GSE264094_Hs_R_NGS_WTA_v1.0.pkc.gz"
SOFT_FILES = ("GSE264094_family.soft.gz", "GSE281805_family.soft.gz")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_soft(path: Path, series: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current: dict[str, str] = {}
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            if line.startswith("^SAMPLE = "):
                if current:
                    rows.append(current)
                current = {"geo_accession": line.split("=", 1)[1].strip(), "series": series}
            elif line.startswith("!Sample_title = "):
                current["title"] = line.split("=", 1)[1].strip()
            elif line.startswith("!Sample_characteristics_ch1 = ") and "location:" in line.lower():
                current["location"] = line.lower().split("location:", 1)[1].strip()
            elif line.startswith("!Sample_supplementary_file_1 = "):
                current["dcc_url"] = line.split("=", 1)[1].strip()
    if current:
        rows.append(current)
    return rows


def tissue_label(location: str) -> str:
    mapping = {
        "brl rim": "BRL_RIM",
        "lesion rim": "BRL_RIM",
        "mixed rim": "mixed_RIM",
        "active center": "active_center",
        "nawm": "NAWM",
        "nawm/ppwm": "NAWM_PPWM",
    }
    if location not in mapping:
        raise ValueError(f"Unrecognized location: {location}")
    return mapping[location]


def source_samples() -> set[str]:
    raw = pd.read_excel(SOURCE_MATRIX, sheet_name="Source_Data_Fig4_a", header=None)
    return set(raw.iloc[2, 6:].dropna().astype(str))


def build_metadata() -> pd.DataFrame:
    records: list[dict[str, str]] = []
    for file_name in SOFT_FILES:
        series = file_name.split("_", 1)[0]
        records.extend(parse_soft(RAW / file_name, series))
    expected_source = source_samples()
    rows: list[dict[str, object]] = []
    for record in records:
        dcc_gz_name = record["dcc_url"].rsplit("/", 1)[-1]
        match = re.search(r"_(DSP-[^.]+)[.]dcc[.]gz$", dcc_gz_name)
        if not match:
            raise ValueError(f"Cannot parse DSP identifier: {dcc_gz_name}")
        sample_id = match.group(1)
        donor_match = re.match(r"(MS\d+|ctrl\d+)", record["title"], flags=re.IGNORECASE)
        if not donor_match:
            raise ValueError(f"Cannot parse donor: {record['title']}")
        donor = donor_match.group(1).upper()
        slide_match = re.match(r"(DSP-\d+-[A-Z])-[A-Z]\d+$", sample_id)
        if not slide_match:
            raise ValueError(f"Cannot parse slide: {sample_id}")
        local_gz = RAW / dcc_gz_name
        rows.append(
            {
                "Sample_ID": sample_id,
                "SegmentDisplayName": sample_id,
                "geo_accession": record["geo_accession"],
                "series": record["series"],
                "title": record["title"],
                "location": record["location"],
                "Type_main": tissue_label(record["location"]),
                "Patient_ID": donor,
                "Slide.Name": slide_match.group(1),
                "Run": record["series"],
                "is_ms": donor.startswith("MS"),
                "in_author_figure4": sample_id in expected_source,
                "dcc_gz_name": dcc_gz_name,
                "dcc_deposited": local_gz.exists(),
            }
        )
    metadata = pd.DataFrame(rows).sort_values("Sample_ID").reset_index(drop=True)
    if len(metadata) != 296 or metadata.Sample_ID.nunique() != 296:
        raise RuntimeError(f"Expected 296 unique GEO AOIs, found {metadata.shape}")
    if int(metadata.in_author_figure4.sum()) != 117:
        raise RuntimeError("Expected 117 deposited DCCs overlapping author Figure 4")
    if int(metadata.dcc_deposited.sum()) != 296:
        raise RuntimeError("A GEO-listed DCC is absent from the local raw package")
    return metadata


def unpack_inputs(metadata: pd.DataFrame) -> None:
    dcc_dir = WORK / "dcc"
    dcc_dir.mkdir(parents=True, exist_ok=True)
    for row in metadata.itertuples(index=False):
        source = RAW / row.dcc_gz_name
        destination = dcc_dir / f"{row.Sample_ID}.dcc"
        if destination.exists() and destination.stat().st_mtime >= source.stat().st_mtime:
            continue
        with gzip.open(source, "rb") as src, destination.open("wb") as dst:
            shutil.copyfileobj(src, dst)
    pkc = WORK / "Hs_R_NGS_WTA_v1.0.pkc"
    if not pkc.exists() or pkc.stat().st_mtime < PKC_GZ.stat().st_mtime:
        with gzip.open(PKC_GZ, "rb") as src, pkc.open("wb") as dst:
            shutil.copyfileobj(src, dst)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata-only", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    metadata = build_metadata()
    metadata.to_csv(OUT / "sample_metadata.tsv", sep="\t", index=False)
    if not args.metadata_only:
        unpack_inputs(metadata)
    manifest = {
        "synthetic": False,
        "raw_root": str(RAW.relative_to(ROOT)),
        "n_geo_aois": len(metadata),
        "n_author_figure4_with_dcc": int(metadata.in_author_figure4.sum()),
        "n_ms": int(metadata.is_ms.sum()),
        "type_counts": metadata.Type_main.value_counts().sort_index().to_dict(),
        "input_sha256": {
            file_name: sha256(RAW / file_name) for file_name in (*SOFT_FILES, PKC_GZ.name)
        },
    }
    (OUT / "preparation_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
