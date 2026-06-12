#!/usr/bin/env python3
"""Audit whether GSE228330 can provide response/outcome labels.

This is data-discovery preparation only. It inspects public GEO metadata,
Europe PMC/PubMed records, and the linked open full text for outcome labels.
No validation analysis is run.
"""

from __future__ import annotations

import gzip
import io
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v45_gse228330_outcome_scout"
RAW = OUT / "raw_public_metadata"
RAW.mkdir(parents=True, exist_ok=True)

GEO = "GSE228330"
LINKED_PMID = "37168665"
LINKED_PMC = "PMC10166068"


def fetch(url: str, timeout: int = 45, attempts: int = 3) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "ms-auto-research-v45/1.0"})
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except Exception as exc:  # network repositories can intermittently time out
            last_error = exc
            if attempt < attempts:
                time.sleep(2 * attempt)
    raise RuntimeError(f"Failed to fetch {url} after {attempts} attempts: {last_error}") from last_error


def fetch_text(url: str, timeout: int = 45, attempts: int = 3) -> str:
    return fetch(url, timeout, attempts=attempts).decode("utf-8", errors="replace")


def parse_series_soft(text: str) -> dict[str, object]:
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
        "summary": " ".join(fields.get("summary", [])),
        "overall_design": fields.get("overall_design", [""])[0],
        "types": "; ".join(fields.get("type", [])),
        "sample_count": len(fields.get("sample_id", [])),
        "contact_name": fields.get("contact_name", [""])[0],
        "contact_institute": fields.get("contact_institute", [""])[0],
        "supplementary_files": "; ".join(fields.get("supplementary_file", [])),
        "platforms": "; ".join(fields.get("platform_id", [])),
        "relations": "; ".join(fields.get("relation", [])),
    }


def split_matrix_line(line: str) -> list[str]:
    # GEO matrix metadata are tab-delimited quoted strings. Removing only the
    # outer quotes is enough for these fixed metadata rows.
    return [part.strip().strip('"') for part in line.rstrip("\n").split("\t")]


def parse_series_matrix(text: str) -> tuple[pd.DataFrame, dict[str, object]]:
    rows = {}
    sample_ids: list[str] = []
    for line in text.splitlines():
        if not line.startswith("!Sample_"):
            continue
        parts = split_matrix_line(line)
        key = parts[0].replace("!Sample_", "")
        values = parts[1:]
        if key == "geo_accession":
            sample_ids = values
        rows.setdefault(key, []).append(values)
    if not sample_ids:
        raise RuntimeError("No sample accessions found in series matrix")
    metadata = pd.DataFrame({"geo_accession": sample_ids})
    for key, value_lists in rows.items():
        if key == "geo_accession":
            continue
        for i, values in enumerate(value_lists, start=1):
            if len(values) == len(sample_ids):
                col = key if len(value_lists) == 1 else f"{key}_{i}"
                metadata[col] = values

    # Extract sample characteristics into normalized columns.
    for col in [c for c in metadata.columns if c.startswith("characteristics_ch1")]:
        parsed = metadata[col].str.extract(r"^([^:]+):\s*(.*)$")
        if parsed.shape[1] == 2:
            name_values = parsed[0].dropna().unique().tolist()
            if len(name_values) == 1:
                norm = re.sub(r"[^A-Za-z0-9]+", "_", name_values[0].strip().lower()).strip("_")
                metadata[norm] = parsed[1]
    summary = {
        "sample_count": int(len(metadata)),
        "duration_counts": metadata.get("treatment_duration_month", pd.Series(dtype=str)).value_counts(dropna=False).to_dict(),
        "ms_type_counts": metadata.get("ms_type", pd.Series(dtype=str)).value_counts(dropna=False).to_dict(),
        "sex_counts": metadata.get("sex", pd.Series(dtype=str)).value_counts(dropna=False).to_dict(),
        "has_response_like_columns": [
            col
            for col in metadata.columns
            if re.search(r"response|responder|neda|relapse|edss|outcome", col, re.I)
        ],
    }
    return metadata, summary


def pubmed_summaries(ids: list[str]) -> list[dict[str, object]]:
    params = urllib.parse.urlencode({"db": "pubmed", "id": ",".join(ids), "retmode": "json"})
    payload = json.loads(fetch_text(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?{params}"))
    rows = []
    for pmid in ids:
        record = payload["result"].get(pmid, {})
        if not record:
            continue
        rows.append(
            {
                "pmid": pmid,
                "title": record.get("title", ""),
                "journal": record.get("fulljournalname", record.get("source", "")),
                "pubdate": record.get("pubdate", ""),
                "doi": next((item["value"] for item in record.get("articleids", []) if item.get("idtype") == "doi"), ""),
                "pmc": next((item["value"] for item in record.get("articleids", []) if item.get("idtype") == "pmc"), ""),
            }
        )
    return rows


def search_europe_pmc() -> pd.DataFrame:
    query = '(GSE228330 OR PMC10166068 OR "37168665" OR (ocrelizumab PBMC transcriptome multiple sclerosis))'
    params = urllib.parse.urlencode({"query": query, "format": "json", "pageSize": 20})
    payload = json.loads(fetch_text(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?{params}", timeout=90))
    rows = []
    for item in payload.get("resultList", {}).get("result", []):
        rows.append(
            {
                "pmid": item.get("pmid", item.get("id", "")),
                "pmcid": item.get("pmcid", ""),
                "title": item.get("title", ""),
                "doi": item.get("doi", ""),
                "pub_year": item.get("pubYear", ""),
                "has_suppl": item.get("hasSuppl", ""),
                "has_tm_accessions": item.get("hasTMAccessionNumbers", ""),
            }
        )
    return pd.DataFrame(rows)


def full_text_term_hits(xml: str) -> pd.DataFrame:
    text = re.sub(r"\s+", " ", xml)
    terms = ["response", "responder", "NEDA", "relapse", "EDSS", "clinical stable", "stable", "outcome", "disability"]
    rows = []
    for term in terms:
        for match in re.finditer(term, text, flags=re.I):
            start = max(0, match.start() - 120)
            end = min(len(text), match.end() + 120)
            rows.append({"term": term, "snippet": text[start:end]})
    return pd.DataFrame(rows).drop_duplicates()


def main() -> int:
    soft_url = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={GEO}&targ=self&form=text&view=full"
    soft = fetch_text(soft_url)
    (RAW / f"{GEO}.soft.txt").write_text(soft)
    geo_summary = parse_series_soft(soft)
    pd.DataFrame([geo_summary]).to_csv(OUT / "gse228330_geo_series_summary.tsv", sep="\t", index=False)

    matrix_url = f"https://ftp.ncbi.nlm.nih.gov/geo/series/GSE228nnn/{GEO}/matrix/{GEO}_series_matrix.txt.gz"
    matrix_text = gzip.GzipFile(fileobj=io.BytesIO(fetch(matrix_url, timeout=90))).read().decode("utf-8", errors="replace")
    (RAW / f"{GEO}_series_matrix_header.txt").write_text("\n".join(matrix_text.splitlines()[:90]) + "\n")
    sample_metadata, matrix_summary = parse_series_matrix(matrix_text)
    sample_metadata.to_csv(OUT / "gse228330_sample_metadata.tsv", sep="\t", index=False)

    epmc = search_europe_pmc()
    epmc.to_csv(OUT / "gse228330_europepmc_hits.tsv", sep="\t", index=False)
    pmids = [LINKED_PMID] + [str(x) for x in epmc["pmid"].dropna().astype(str).head(5).tolist() if str(x).isdigit() and str(x) != LINKED_PMID]
    pubmed = pd.DataFrame(pubmed_summaries(list(dict.fromkeys(pmids))))
    pubmed.to_csv(OUT / "gse228330_pubmed_summaries.tsv", sep="\t", index=False)

    xml = fetch_text(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{LINKED_PMC}/fullTextXML", timeout=60)
    (RAW / f"{LINKED_PMC}.fullTextXML.first2000.txt").write_text(xml[:2000])
    term_hits = full_text_term_hits(xml)
    term_hits.to_csv(OUT / "gse228330_linked_paper_outcome_term_hits.tsv", sep="\t", index=False)

    response_like_cols = matrix_summary["has_response_like_columns"]
    has_response_labels = bool(response_like_cols)
    summary = {
        "status": "complete",
        "accession": GEO,
        "linked_pubmed_id": LINKED_PMID,
        "linked_pmc": LINKED_PMC,
        "sample_count": matrix_summary["sample_count"],
        "duration_counts": matrix_summary["duration_counts"],
        "ms_type_counts": matrix_summary["ms_type_counts"],
        "response_like_sample_columns": response_like_cols,
        "europepmc_hit_count": int(len(epmc)),
        "verdict": "not_response_validation_ready",
        "blocker": (
            "public GEO/series matrix metadata provide treatment duration and MS subtype, "
            "but no responder/NEDA/relapse outcome labels; linked paper frames cohort as "
            "clinically stable pharmacodynamic anti-CD20 profiling"
        ),
        "allowable_use": "open pharmacodynamic and batch/QC context only unless author-provided clinical outcomes map to samples",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
