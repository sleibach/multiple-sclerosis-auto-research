#!/usr/bin/env python3
"""Wave92 FABP5 prior-art audit.

Wave91 parked FABP5 for deep validation. Before spending more compute on it,
this script checks whether FABP5 inhibition is already prior-arted for MS or
autoimmune disease. PubMed and ClinicalTrials are queried through public APIs;
patent search URLs are recorded because Google Patents/Espacenet do not expose
a simple stable unauthenticated JSON API.
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import pandas as pd

from v3_analyze_direct_h5ad_cell_states import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave92_fabp5_prior_art_audit"

PUBMED_QUERIES = [
    'FABP5 multiple sclerosis',
    '"fatty acid-binding protein 5" "multiple sclerosis"',
    'FABP5 experimental autoimmune encephalomyelitis',
    'FABP5 inhibitor autoimmune',
    'FABP5 psoriasis',
    'FABP5 inflammatory bowel disease',
    'FABP5 rheumatoid arthritis',
]

CLINICALTRIALS_QUERIES = [
    'FABP5',
    '"fatty acid binding protein 5"',
    'MF6 FABP',
    'FABP inhibitor autoimmune',
]

PATENT_SEARCH_URLS = [
    {
        "database": "Google Patents",
        "query": "FABP5 inhibitor multiple sclerosis",
        "url": "https://patents.google.com/?q=%22FABP5%22+%22multiple+sclerosis%22",
    },
    {
        "database": "Google Patents",
        "query": "fatty acid binding protein 5 autoimmune inhibitor",
        "url": "https://patents.google.com/?q=%22fatty+acid+binding+protein+5%22+autoimmune+inhibitor",
    },
    {
        "database": "Google Patents",
        "query": "MF6 FABP5 FABP7 inhibitor",
        "url": "https://patents.google.com/?q=MF6+FABP5+FABP7+inhibitor",
    },
    {
        "database": "Espacenet",
        "query": "FABP5 inhibitor multiple sclerosis",
        "url": "https://worldwide.espacenet.com/patent/search?q=FABP5%20inhibitor%20multiple%20sclerosis",
    },
]

KNOWN_BLOCKER_PMIDS = {"34624687", "33124722"}


def url_json(url: str, timeout: int = 30) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": "ms-auto-research/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as handle:
        return json.load(handle)


def pubmed_search(query: str, retmax: int = 20) -> list[str]:
    params = urllib.parse.urlencode({"db": "pubmed", "term": query, "retmode": "json", "retmax": retmax})
    data = url_json(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{params}")
    return data.get("esearchresult", {}).get("idlist", [])


def pubmed_summary(ids: list[str]) -> list[dict[str, Any]]:
    if not ids:
        return []
    params = urllib.parse.urlencode({"db": "pubmed", "id": ",".join(ids), "retmode": "json"})
    data = url_json(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?{params}")
    rows = []
    for pid in ids:
        rec = data.get("result", {}).get(pid, {})
        if not rec:
            continue
        doi = ""
        pmc = ""
        for item in rec.get("articleids", []):
            if item.get("idtype") == "doi":
                doi = item.get("value", "")
            if item.get("idtype") == "pmcid":
                pmc = item.get("value", "")
        rows.append(
            {
                "pmid": pid,
                "title": rec.get("title", ""),
                "journal": rec.get("fulljournalname", ""),
                "pubdate": rec.get("pubdate", ""),
                "doi": doi,
                "pmcid": pmc,
                "source": "PubMed E-utilities",
            }
        )
    return rows


def clinicaltrials_search(query: str) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"query.term": query, "pageSize": 10, "format": "json"})
    data = url_json(f"https://clinicaltrials.gov/api/v2/studies?{params}")
    rows = []
    for study in data.get("studies", []):
        protocol = study.get("protocolSection", {})
        ident = protocol.get("identificationModule", {})
        status = protocol.get("statusModule", {})
        conditions = protocol.get("conditionsModule", {}).get("conditions", [])
        interventions = protocol.get("armsInterventionsModule", {}).get("interventions", [])
        rows.append(
            {
                "query": query,
                "nct_id": ident.get("nctId", ""),
                "title": ident.get("briefTitle", ""),
                "status": status.get("overallStatus", ""),
                "conditions": ";".join(conditions),
                "interventions": ";".join([item.get("name", "") for item in interventions]),
            }
        )
    return rows


def analyze() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    pubmed_query_rows = []
    all_pmids: set[str] = set()
    for query in PUBMED_QUERIES:
        ids = pubmed_search(query)
        all_pmids.update(ids)
        pubmed_query_rows.append({"query": query, "n_pmids_returned": len(ids), "pmids": ",".join(ids[:20])})
        time.sleep(0.34)
    pubmed_rows = pubmed_summary(sorted(all_pmids))
    pubmed_queries = pd.DataFrame(pubmed_query_rows)
    pubmed = pd.DataFrame(pubmed_rows)

    clinical_rows = []
    for query in CLINICALTRIALS_QUERIES:
        clinical_rows.extend(clinicaltrials_search(query))
        time.sleep(0.2)
    clinical = pd.DataFrame(clinical_rows)
    patents = pd.DataFrame(PATENT_SEARCH_URLS)

    pubmed_queries.to_csv(OUT / "pubmed_query_log.tsv", sep="\t", index=False)
    pubmed.to_csv(OUT / "pubmed_records.tsv", sep="\t", index=False)
    clinical.to_csv(OUT / "clinicaltrials_records.tsv", sep="\t", index=False)
    patents.to_csv(OUT / "patent_search_urls.tsv", sep="\t", index=False)

    blockers = pubmed[pubmed["pmid"].astype(str).isin(KNOWN_BLOCKER_PMIDS)].copy() if not pubmed.empty else pd.DataFrame()
    blocker_pmids_found = sorted(set(blockers["pmid"].astype(str))) if not blockers.empty else []
    call = "FABP5_PRIOR_ART_BLOCKED_FOR_MS_THERAPEUTIC_NOVELTY" if "34624687" in blocker_pmids_found else "FABP5_PRIOR_ART_UNRESOLVED"

    summary = {
        "seed": SEED,
        "analysis_call": call,
        "n_pubmed_queries": len(PUBMED_QUERIES),
        "n_unique_pubmed_records": int(len(pubmed)),
        "known_blocker_pmids_found": blocker_pmids_found,
        "n_clinicaltrials_records": int(len(clinical)),
        "patent_search_url_count": int(len(patents)),
        "outputs": {
            "pubmed_query_log": rel(OUT / "pubmed_query_log.tsv"),
            "pubmed_records": rel(OUT / "pubmed_records.tsv"),
            "clinicaltrials_records": rel(OUT / "clinicaltrials_records.tsv"),
            "patent_search_urls": rel(OUT / "patent_search_urls.tsv"),
        },
    }
    write_json(OUT / "summary.json", summary)

    report = [
        "# Wave92 FABP5 Prior-Art Audit",
        "",
        f"Analysis call: `{call}`.",
        "",
        "## Blocking PubMed Records",
        "",
        markdown_table(blockers[["pmid", "title", "journal", "pubdate", "doi"]] if not blockers.empty else pd.DataFrame(), max_rows=20),
        "",
        "## PubMed Query Log",
        "",
        markdown_table(pubmed_queries, max_rows=20),
        "",
        "## ClinicalTrials Query Results",
        "",
        markdown_table(clinical.head(20) if not clinical.empty else pd.DataFrame(), max_rows=20),
        "",
        "## Patent Search URLs",
        "",
        markdown_table(patents, max_rows=20),
        "",
        "## Decision",
        "",
        "Do not promote FABP5 as a novel MS therapeutic target. PMID 34624687 directly reports a FABP5/FABP7 inhibitor in MS mouse models, and PMID 33124722 directly links Fabp5 mechanistically to EAE susceptibility.",
        "",
        "A future FABP5 branch would need to be explicitly framed as replication, a different modality, or a precisely stratified cross-autoimmune extension rather than a new target nomination.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    result = analyze()
    print(json.dumps(result, indent=2, sort_keys=True))
