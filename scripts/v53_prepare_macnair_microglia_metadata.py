#!/usr/bin/env python3
"""Prepare frozen-gene metadata maps for the Macnair MS snRNA-seq cohorts.

This script downloads only public metadata and gene annotations. It does not
download or commit either multi-gigabyte count matrix. The generated
column-group map preserves deposited matrix order for a streaming targeted
extractor.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import json
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Iterator


ZENODO_API = "https://zenodo.org/api/records/8338963"
TARGET_GENES = [
    "CD44",
    "CXCR4",
    "CIITA",
    "RFX5",
    "MIF",
    "DDT",
    "STAT1",
    "IRF1",
    "CXCL10",
    "GBP1",
    "CTSS",
    "CTSB",
    "CTSD",
    "LAMP1",
    "LAMP2",
    "LAMP3",
]
MS_DIAGNOSES = {"PPMS", "RRMS", "SPMS"}

COHORT_FILES = {
    "discovery": {
        "metadata": "ms_lesions_snRNAseq_col_data_2023-09-12.txt.gz",
        "row_data": "ms_lesions_snRNAseq_row_data_2023-09-12.txt.gz",
        "matrix": "ms_lesions_snRNAseq_cleaned_counts_matrix_2023-09-12.mtx.gz",
    },
    "validation": {
        "metadata": "ms_lesions_snRNAseq_validation_col_data_2023-09-12.txt.gz",
        "row_data": "ms_lesions_snRNAseq_validation_row_data_2023-09-12.txt.gz",
        "matrix": "ms_lesions_snRNAseq_validation_cleaned_counts_matrix_2023-09-12.mtx.gz",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cohort", choices=sorted(COHORT_FILES), required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    return parser.parse_args()


def fetch_manifest() -> dict[str, object]:
    with urllib.request.urlopen(ZENODO_API, timeout=60) as response:  # noqa: S310 - fixed public URL
        return json.load(response)


def file_info(manifest: dict[str, object], name: str) -> dict[str, object]:
    for item in manifest["files"]:  # type: ignore[index]
        if item["key"] == name:
            return {
                "name": name,
                "size": item["size"],
                "checksum": item["checksum"],
                "url": item["links"]["self"],
            }
    raise KeyError(f"Zenodo record is missing {name}")


def streamed_csv(url: str) -> Iterator[dict[str, str]]:
    with urllib.request.urlopen(url, timeout=120) as response:  # noqa: S310 - manifest URL
        with gzip.GzipFile(fileobj=response) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as text:
                yield from csv.DictReader(text)


def normalized_row(cohort: str, row: dict[str, str]) -> dict[str, str]:
    if cohort == "discovery":
        return {
            "sample_id": row["sample_id_anon"],
            "donor_id": row["individual_id_anon"],
            "study": "macnair_discovery",
            "diagnosis": row["diagnosis"],
            "lesion_type": row["lesion_type"],
            "matter": row["matter"],
            "sex": row["sex"],
            "age_at_death": row["age_at_death"],
            "pmi_minutes": row["pmi_minutes"],
            "batch": row["seq_pool"],
        }
    return {
        "sample_id": row["sample_id"],
        "donor_id": row["donor_id"],
        "study": row["study"],
        "diagnosis": row["diagnosis"],
        "lesion_type": row["lesion_type"],
        "matter": "GM" if row["lesion_type"] in {"GM", "NAGM", "GML"} else "WM",
        "sex": row["sex"],
        "age_at_death": row["age_at_death"],
        "pmi_minutes": row["pmi_minutes"],
        "batch": row["study"],
    }


def eligible_cell(cohort: str, row: dict[str, str]) -> bool:
    if row.get("type_broad") != "Microglia":
        return False
    if cohort == "discovery" and row.get("exclude_pseudobulk") == "TRUE":
        return False
    return row.get("diagnosis") == "CTR" or row.get("diagnosis") in MS_DIAGNOSES


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    manifest = fetch_manifest()
    files = COHORT_FILES[args.cohort]
    source = {role: file_info(manifest, name) for role, name in files.items()}

    target_rows: list[dict[str, object]] = []
    for index, row in enumerate(streamed_csv(str(source["row_data"]["url"])), start=1):
        if row["symbol"] in TARGET_GENES:
            target_rows.append({"row_index": index, "gene": row["symbol"], "gene_id": row["gene_id"]})
    observed = Counter(str(row["gene"]) for row in target_rows)
    if observed != Counter(TARGET_GENES):
        raise ValueError(f"frozen target coverage mismatch: {observed}")

    group_by_sample: dict[str, int] = {}
    group_metadata: dict[int, dict[str, str]] = {}
    column_rows: list[dict[str, object]] = []
    total_cells = 0
    for column_index, row in enumerate(streamed_csv(str(source["metadata"]["url"])), start=1):
        total_cells += 1
        if not eligible_cell(args.cohort, row):
            continue
        normalized = normalized_row(args.cohort, row)
        sample = normalized["sample_id"]
        if sample not in group_by_sample:
            group_idx = len(group_by_sample)
            group_by_sample[sample] = group_idx
            group_metadata[group_idx] = normalized
        else:
            group_idx = group_by_sample[sample]
            if group_metadata[group_idx] != normalized:
                raise ValueError(f"sample metadata changed within {sample}")
        column_rows.append({"column_index": column_index, "group_idx": group_idx})

    sample_rows: list[dict[str, object]] = []
    cells_per_group = Counter(int(row["group_idx"]) for row in column_rows)
    for group_idx in sorted(group_metadata):
        row = dict(group_metadata[group_idx])
        diagnosis = row["diagnosis"]
        sample_rows.append(
            {
                "group_idx": group_idx,
                **row,
                "disease_binary": 0 if diagnosis == "CTR" else 1,
                "n_microglia": cells_per_group[group_idx],
            }
        )

    write_tsv(args.outdir / "column_groups.tsv", column_rows, ["column_index", "group_idx"])
    write_tsv(args.outdir / "target_rows.tsv", target_rows, ["row_index", "gene", "gene_id"])
    sample_fields = [
        "group_idx",
        "sample_id",
        "donor_id",
        "study",
        "diagnosis",
        "disease_binary",
        "lesion_type",
        "matter",
        "sex",
        "age_at_death",
        "pmi_minutes",
        "batch",
        "n_microglia",
    ]
    write_tsv(args.outdir / "sample_metadata.tsv", sample_rows, sample_fields)

    donors = {
        diagnosis: sorted({row["donor_id"] for row in sample_rows if row["diagnosis"] == diagnosis})
        for diagnosis in ["CTR", "PPMS", "RRMS", "SPMS"]
    }
    summary = {
        "purpose": "Public-cohort eligibility and frozen-gene extraction preparation; no biological result",
        "cohort": args.cohort,
        "zenodo_record": 8338963,
        "n_matrix_columns": total_cells,
        "n_eligible_microglia": len(column_rows),
        "n_eligible_samples": len(sample_rows),
        "n_donors_by_diagnosis": {key: len(value) for key, value in donors.items()},
        "n_ms_donors": sum(len(donors[key]) for key in MS_DIAGNOSES),
        "n_control_donors": len(donors["CTR"]),
        "n_target_genes": len(target_rows),
        "target_coverage_complete": True,
        "source_files": source,
        "matrix_committed": False,
    }
    (args.outdir / "metadata_preparation_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
