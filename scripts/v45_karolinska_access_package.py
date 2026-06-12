#!/usr/bin/env python3
"""Build a reproducible Karolinska DMF label-request metadata package.

This is data-access preparation only. It verifies public GEO/PubMed metadata
for the GSE130478/GSE130491/GSE130494 Karolinska DMF cohort and writes a
machine-readable request checklist. It does not run validation or analyze
expression data.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v45_karolinska_access"
OUT.mkdir(parents=True, exist_ok=True)

SERIES = ["GSE130494", "GSE130478", "GSE130491"]
PUBMED_ID = "31300673"


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "ms-auto-research-v45/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_soft(text: str) -> dict[str, object]:
    fields: dict[str, list[str]] = {}
    for raw in text.splitlines():
        if not raw.startswith("!Series_"):
            continue
        key, value = raw.split(" = ", 1)
        fields.setdefault(key.replace("!Series_", ""), []).append(value.strip())
    return {
        "accession": fields.get("geo_accession", [""])[0],
        "title": fields.get("title", [""])[0],
        "status": fields.get("status", [""])[0],
        "pubmed_id": fields.get("pubmed_id", [""])[0],
        "summary": fields.get("summary", [""])[0],
        "overall_design": fields.get("overall_design", [""])[0],
        "types": "; ".join(fields.get("type", [])),
        "sample_count": len(fields.get("sample_id", [])),
        "contact_name": fields.get("contact_name", [""])[0],
        "contact_email": fields.get("contact_email", [""])[0],
        "contact_institute": fields.get("contact_institute", [""])[0],
        "supplementary_files": "; ".join(fields.get("supplementary_file", [])),
        "platforms": "; ".join(fields.get("platform_id", [])),
        "relations": "; ".join(fields.get("relation", [])),
    }


def fetch_pubmed_summary() -> dict[str, object]:
    params = urllib.parse.urlencode({"db": "pubmed", "id": PUBMED_ID, "retmode": "json"})
    payload = json.loads(fetch_text(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?{params}"))
    record = payload["result"][PUBMED_ID]
    return {
        "pubmed_id": PUBMED_ID,
        "title": record.get("title", ""),
        "journal": record.get("fulljournalname", record.get("source", "")),
        "pubdate": record.get("pubdate", ""),
        "doi": next(
            (item["value"] for item in record.get("articleids", []) if item.get("idtype") == "doi"),
            "",
        ),
        "pmc": next(
            (item["value"] for item in record.get("articleids", []) if item.get("idtype") == "pmc"),
            "",
        ),
        "last_author": record.get("lastauthor", ""),
    }


def main() -> int:
    rows = []
    raw_dir = OUT / "raw_public_metadata"
    raw_dir.mkdir(parents=True, exist_ok=True)
    for accession in SERIES:
        url = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={accession}&targ=self&form=text&view=full"
        text = fetch_text(url)
        (raw_dir / f"{accession}.soft.txt").write_text(text)
        row = parse_soft(text)
        row["source_url"] = url
        rows.append(row)
    geo = pd.DataFrame(rows)
    geo.to_csv(OUT / "karolinska_geo_series_summary.tsv", sep="\t", index=False)

    pubmed = fetch_pubmed_summary()
    (OUT / "karolinska_pubmed_summary.json").write_text(json.dumps(pubmed, indent=2, sort_keys=True) + "\n")

    request_items = pd.DataFrame(
        [
            {
                "priority": 1,
                "needed_item": "patient_level_beneficial_response_labels",
                "why_needed": "public GEO metadata states beneficial response/nonresponder biology but does not map labels to expression samples",
                "minimum_acceptable": "one response label per patient ID for the 14 GSE130478 expression-paired subjects",
            },
            {
                "priority": 2,
                "needed_item": "gsm_to_patient_timepoint_celltype_map",
                "why_needed": "validation requires pairing baseline and 6-month CD4 expression samples from the same subject",
                "minimum_acceptable": "GSM, patient_id, timepoint, cell_type, platform for all GSE130478 samples",
            },
            {
                "priority": 3,
                "needed_item": "clinical_outcome_definition",
                "why_needed": "beneficial response must be interpreted consistently and not post-hoc",
                "minimum_acceptable": "definition used in PMID 31300673 and responder/nonresponder cutoffs",
            },
            {
                "priority": 4,
                "needed_item": "technical_covariates",
                "why_needed": "V44 batch guard requires technical metadata to distinguish biology from response-correlated batch",
                "minimum_acceptable": "array batch/date/file, processing date, RNA quality if available",
            },
            {
                "priority": 5,
                "needed_item": "monocyte_count_ros_mapping",
                "why_needed": "paper reports monocyte counts and ROS distinguish response; these are important confounders/context variables",
                "minimum_acceptable": "patient-level monocyte count and ROS summaries with timepoints, if shareable",
            },
        ]
    )
    request_items.to_csv(OUT / "karolinska_request_checklist.tsv", sep="\t", index=False)

    summary = {
        "status": "complete",
        "accessions": SERIES,
        "pubmed_id": PUBMED_ID,
        "contact_email": geo["contact_email"].dropna().iloc[0],
        "contact_name": geo["contact_name"].dropna().iloc[0],
        "expression_series": "GSE130478",
        "methylation_series": "GSE130491",
        "superseries": "GSE130494",
        "expression_sample_count": int(geo.loc[geo["accession"].eq("GSE130478"), "sample_count"].iloc[0]),
        "methylation_sample_count": int(geo.loc[geo["accession"].eq("GSE130491"), "sample_count"].iloc[0]),
        "blocker": "patient-level beneficial-response labels and GSM-to-patient/timepoint mapping are not public in GEO metadata",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
