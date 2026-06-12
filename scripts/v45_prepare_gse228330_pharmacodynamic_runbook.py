#!/usr/bin/env python3
"""Prepare GSE228330 pharmacodynamic-only acquisition/runbook artifacts.

The output is intentionally conservative. Public GEO metadata provide
treatment-duration timepoints but do not provide a confirmed subject-pairing map
or response labels. The generated metadata table is therefore marked
`inferred_unverified` and must not be used for response validation.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis/v45_gse228330_outcome_scout/gse228330_sample_metadata.tsv"
OUT = ROOT / "analysis/v45_gse228330_pharmacodynamic_runbook"

SERIES_URLS = [
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE228nnn/GSE228330/suppl/GSE228330_Clariom_S_Human.hg38.main.probes.tab.gz",
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE228nnn/GSE228330/suppl/GSE228330_RAW.tar",
]


def days_from_months(months: object) -> object:
    if pd.isna(months):
        return pd.NA
    value = float(months)
    if value == 0:
        return 0
    if value == 0.5:
        return 14
    if value == 6:
        return 180
    return int(round(value * 30.4375))


def label_from_months(months: object) -> str:
    if pd.isna(months):
        return "unknown"
    value = float(months)
    if value == 0:
        return "baseline"
    if value == 0.5:
        return "week2"
    if value == 6:
        return "month6"
    return f"month{value:g}"


def public_file_code(row: pd.Series) -> str:
    text = str(row.get("supplementary_file_1", ""))
    match = re.search(r"_(O\d+|R\d+)_", text)
    return match.group(1) if match else ""


def build_download_manifest(meta: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for url in SERIES_URLS:
        rows.append(
            {
                "artifact_type": "series_supplementary",
                "geo_accession": "GSE228330",
                "sample_id": "",
                "url": url,
                "target_path": "data/quarantine/gse228330_pharmacodynamic/raw/" + Path(url).name,
                "required_for": "expression_or_raw_reprocessing",
            }
        )
    for _, row in meta.iterrows():
        for field, kind in [
            ("supplementary_file_1", "sample_raw_cel"),
            ("supplementary_file_2", "sample_chp"),
        ]:
            url = str(row.get(field, ""))
            if not url or url == "nan":
                continue
            https_url = url.replace("ftp://ftp.ncbi.nlm.nih.gov/", "https://ftp.ncbi.nlm.nih.gov/")
            rows.append(
                {
                    "artifact_type": kind,
                    "geo_accession": "GSE228330",
                    "sample_id": row["geo_accession"],
                    "url": https_url,
                    "target_path": "data/quarantine/gse228330_pharmacodynamic/raw/" + Path(https_url).name,
                    "required_for": "raw_reprocessing_or_audit",
                }
            )
    return pd.DataFrame(rows)


def build_draft_metadata(meta: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(
        {
            "sample_id": meta["geo_accession"],
            "subject": [f"UNVERIFIED_PUBLIC_ORDER_{i:02d}" for i in range(1, len(meta) + 1)],
            "timepoint": meta["treatment_duration_month"].map(label_from_months),
            "days_since_treatment": meta["treatment_duration_month"].map(days_from_months),
            "therapy": "ocrelizumab",
            "therapy_class": "anti_cd20",
            "expression_platform": "Clariom S Human array / GPL24539",
            "disease": "MS",
            "disease_subtype": meta["ms_type"],
            "clinical_status": meta["ms_type"].astype(str).str.split("-", n=1).str[-1],
            "batch": "not_public",
            "processing_batch": "not_public",
            "collection_date": "not_public",
            "steroid_exposure": "not_public",
            "prior_dmt": "not_public",
            "cell_count_metadata": "not_public",
            "qc_pass": "not_public",
            "sex": meta["sex"],
            "public_file_code": meta.apply(public_file_code, axis=1),
            "pairing_status": "inferred_unverified",
            "use_status": "context_only_subject_map_required_before_paired_delta",
        }
    )
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = pd.read_csv(SRC, sep="\t")
    manifest = build_download_manifest(meta)
    draft = build_draft_metadata(meta)
    timepoints = (
        draft.groupby(["timepoint", "days_since_treatment"], dropna=False)
        .size()
        .reset_index(name="n_samples")
        .sort_values(["days_since_treatment", "timepoint"])
    )
    subtype = (
        draft.groupby(["disease_subtype", "timepoint"], dropna=False)
        .size()
        .reset_index(name="n_samples")
        .sort_values(["disease_subtype", "timepoint"])
    )
    manifest.to_csv(OUT / "gse228330_download_manifest.tsv", sep="\t", index=False)
    draft.to_csv(OUT / "gse228330_draft_pharmacodynamic_metadata_unverified.tsv", sep="\t", index=False)
    timepoints.to_csv(OUT / "gse228330_timepoint_counts.tsv", sep="\t", index=False)
    subtype.to_csv(OUT / "gse228330_subtype_timepoint_counts.tsv", sep="\t", index=False)
    summary = {
        "accession": "GSE228330",
        "synthetic": False,
        "samples": int(len(draft)),
        "timepoint_counts": {str(row["timepoint"]): int(row["n_samples"]) for _, row in timepoints.iterrows()},
        "response_labels_public": False,
        "subject_pairing_publicly_confirmed": False,
        "metadata_use": "draft only; confirm subject map before paired deltas",
        "validation_use": "forbidden without response labels and cohort-specific preregistration addendum",
        "outputs": [
            "gse228330_download_manifest.tsv",
            "gse228330_draft_pharmacodynamic_metadata_unverified.tsv",
            "gse228330_timepoint_counts.tsv",
            "gse228330_subtype_timepoint_counts.tsv",
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
