#!/usr/bin/env python3
"""V44 alternative/replication cohort scout.

This script records auditable search hit counts and a curated candidate
verification table for treatment-response transcriptomic cohorts. It does not
run validation and does not open any quarantined Gafson data.
"""

from __future__ import annotations

import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


OUT = Path("analysis/v44_alt_cohort_scout")
OUT.mkdir(parents=True, exist_ok=True)

NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


QUERIES = [
    {
        "id": "ms_dmf_response_transcriptome",
        "query": '("multiple sclerosis" AND "dimethyl fumarate" AND (response OR responder OR NEDA) AND (transcriptome OR RNA-seq OR microarray))',
    },
    {
        "id": "ms_gafson_dmf_neda",
        "query": '("Gafson" AND "dimethyl fumarate" AND "NEDA" AND "RNA")',
    },
    {
        "id": "ms_dmf_geo_accession",
        "query": '("dimethyl fumarate" AND "multiple sclerosis" AND "GEO" AND (GSE OR accession))',
    },
    {
        "id": "ms_fingolimod_response_transcriptome",
        "query": '("multiple sclerosis" AND fingolimod AND (response OR responder) AND (transcriptome OR RNA-seq OR microarray))',
    },
    {
        "id": "ms_ocrelizumab_response_transcriptome",
        "query": '("multiple sclerosis" AND ocrelizumab AND (response OR responder OR NEDA) AND (transcriptome OR RNA-seq OR microarray))',
    },
    {
        "id": "ms_natalizumab_response_transcriptome",
        "query": '("multiple sclerosis" AND natalizumab AND (response OR responder) AND (transcriptome OR RNA-seq OR microarray))',
    },
    {
        "id": "ms_teriflunomide_cladribine_alemtuzumab_transcriptome",
        "query": '("multiple sclerosis" AND (teriflunomide OR cladribine OR alemtuzumab) AND (response OR responder) AND (transcriptome OR RNA-seq OR microarray))',
    },
    {
        "id": "ra_jak_response_transcriptome",
        "query": '("rheumatoid arthritis" AND (tofacitinib OR upadacitinib OR baricitinib) AND (response OR responder OR remission) AND (transcriptome OR RNA-seq OR microarray))',
    },
    {
        "id": "ibd_jak_response_transcriptome",
        "query": '((ulcerative colitis OR Crohn OR IBD) AND (tofacitinib OR upadacitinib OR filgotinib) AND (response OR responder OR remission) AND (transcriptome OR RNA-seq OR microarray))',
    },
    {
        "id": "ibd_biologic_paired_response_transcriptome",
        "query": '((ulcerative colitis OR Crohn OR IBD) AND (vedolizumab OR ustekinumab OR infliximab OR adalimumab) AND (paired OR longitudinal OR baseline) AND (response OR responder OR remission) AND (transcriptome OR RNA-seq OR microarray))',
    },
    {
        "id": "psoriasis_response_transcriptome",
        "query": '(psoriasis AND (adalimumab OR methotrexate OR ustekinumab OR secukinumab) AND (response OR PASI75 OR responder) AND (transcriptome OR microarray OR RNA-seq))',
    },
]


def fetch_json(url: str, timeout: int = 30) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "ms-auto-research-v44"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def ncbi_search(db: str, query: str, retmax: int = 8) -> dict[str, Any]:
    params = urllib.parse.urlencode(
        {"db": db, "term": query, "retmode": "json", "retmax": retmax}
    )
    url = f"{NCBI_BASE}/esearch.fcgi?{params}"
    return fetch_json(url).get("esearchresult", {})


def ncbi_summary(db: str, ids: list[str]) -> dict[str, Any]:
    if not ids:
        return {}
    params = urllib.parse.urlencode({"db": db, "id": ",".join(ids), "retmode": "json"})
    url = f"{NCBI_BASE}/esummary.fcgi?{params}"
    return fetch_json(url)


def europe_pmc_search(query: str, page_size: int = 8) -> dict[str, Any]:
    params = urllib.parse.urlencode(
        {"query": query, "format": "json", "pageSize": page_size}
    )
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?{params}"
    return fetch_json(url).get("resultList", {})


def zenodo_search(query: str, page_size: int = 5) -> dict[str, Any]:
    params = urllib.parse.urlencode({"q": query, "size": page_size})
    url = f"https://zenodo.org/api/records?{params}"
    return fetch_json(url)


def osf_search(query: str, page_size: int = 5) -> dict[str, Any]:
    params = urllib.parse.urlencode({"filter[q]": query, "page[size]": page_size})
    url = f"https://api.osf.io/v2/preprints/?{params}"
    return fetch_json(url)


def biostudies_search(query: str, page_size: int = 5) -> dict[str, Any]:
    params = urllib.parse.urlencode({"query": query, "pageSize": page_size})
    url = f"https://www.ebi.ac.uk/biostudies/api/v1/search?{params}"
    return fetch_json(url)


def ena_search(query: str, limit: int = 5) -> list[dict[str, Any]]:
    # ENA requires a structured query; this intentionally records the exact
    # API behavior for broad free-text repository scouting.
    params = urllib.parse.urlencode(
        {
            "result": "study",
            "query": query,
            "fields": "study_accession,study_title",
            "format": "json",
            "limit": limit,
        }
    )
    url = f"https://www.ebi.ac.uk/ena/portal/api/search?{params}"
    payload = fetch_json(url)
    return payload if isinstance(payload, list) else []


def figshare_search(query: str, page_size: int = 5) -> list[dict[str, Any]]:
    url = "https://api.figshare.com/v2/articles/search"
    body = json.dumps({"search_for": query, "page_size": page_size}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "User-Agent": "ms-auto-research-v44",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload if isinstance(payload, list) else []


def dryad_search(query: str, page_size: int = 5) -> dict[str, Any]:
    params = urllib.parse.urlencode({"query": query, "per_page": page_size})
    url = f"https://datadryad.org/api/v2/search?{params}"
    return fetch_json(url)


def safe_call(fn, *args) -> tuple[str, Any]:
    try:
        return "ok", fn(*args)
    except Exception as exc:  # noqa: BLE001 - this is an audit script
        return f"error: {type(exc).__name__}: {exc}", None


def first_titles_from_ncbi_summary(db: str, ids: list[str]) -> list[dict[str, str]]:
    status, payload = safe_call(ncbi_summary, db, ids)
    if status != "ok" or not payload:
        return [{"id": ",".join(ids), "title": status, "source": db}]
    result = payload.get("result", {})
    titles = []
    for uid in result.get("uids", []):
        item = result.get(uid, {})
        title = item.get("title") or item.get("caption") or ""
        titles.append({"id": uid, "title": title, "source": db})
    return titles


def search_all() -> None:
    rows: list[dict[str, Any]] = []
    raw_hits: dict[str, Any] = {}
    for spec in QUERIES:
        qid = spec["id"]
        query = spec["query"]
        raw_hits[qid] = {}
        for db in ["gds", "pubmed", "sra"]:
            status, result = safe_call(ncbi_search, db, query)
            ids = result.get("idlist", []) if result else []
            count = int(result.get("count", 0)) if result else 0
            raw_hits[qid][db] = {"status": status, "count": count, "ids": ids}
            rows.append(
                {
                    "query_id": qid,
                    "source": f"ncbi_{db}",
                    "status": status,
                    "count": count,
                    "top_ids": ";".join(ids),
                    "query": query,
                }
            )
            time.sleep(0.35)
            raw_hits[qid][f"{db}_summaries"] = first_titles_from_ncbi_summary(db, ids)
            time.sleep(0.35)
        for label, fn in [
            ("europe_pmc", europe_pmc_search),
            ("biostudies_arrayexpress", biostudies_search),
            ("ena_study", ena_search),
            ("zenodo", zenodo_search),
            ("figshare", figshare_search),
            ("dryad", dryad_search),
            ("osf_preprints", osf_search),
        ]:
            status, result = safe_call(fn, query)
            if label == "europe_pmc" and result:
                hits = result.get("result", [])
                count = int(result.get("hitCount", len(hits)))
                top_ids = [
                    (hit.get("pmid") or hit.get("pmcid") or hit.get("doi") or hit.get("id") or "")
                    for hit in hits
                ]
                raw_hits[qid][label] = {
                    "status": status,
                    "count": count,
                    "hits": [
                        {
                            "id": top_ids[i] if i < len(top_ids) else "",
                            "title": hit.get("title", ""),
                            "journal": hit.get("journalTitle", ""),
                            "year": hit.get("pubYear", ""),
                            "doi": hit.get("doi", ""),
                        }
                        for i, hit in enumerate(hits)
                    ],
                }
            elif label == "biostudies_arrayexpress" and result:
                hits = result.get("hits", [])
                count = int(result.get("totalHits", len(hits)))
                top_ids = [hit.get("accession", "") for hit in hits]
                raw_hits[qid][label] = {
                    "status": status,
                    "count": count,
                    "hits": [
                        {
                            "id": hit.get("accession", ""),
                            "title": hit.get("title", ""),
                            "type": hit.get("type", ""),
                        }
                        for hit in hits
                    ],
                }
            elif label == "ena_study" and result:
                hits = result
                count = len(hits)
                top_ids = [hit.get("study_accession", "") for hit in hits]
                raw_hits[qid][label] = {
                    "status": status,
                    "count": count,
                    "hits": hits,
                }
            elif label == "zenodo" and result:
                hits = result.get("hits", {}).get("hits", [])
                count = int(result.get("hits", {}).get("total", 0))
                top_ids = [str(hit.get("id", "")) for hit in hits]
                raw_hits[qid][label] = {
                    "status": status,
                    "count": count,
                    "hits": [
                        {
                            "id": hit.get("id", ""),
                            "title": hit.get("metadata", {}).get("title", ""),
                            "doi": hit.get("doi", ""),
                        }
                        for hit in hits
                    ],
                }
            elif label == "figshare" and result:
                hits = result
                count = len(hits)
                top_ids = [str(hit.get("id", "")) for hit in hits]
                raw_hits[qid][label] = {
                    "status": status,
                    "count": count,
                    "hits": [
                        {
                            "id": hit.get("id", ""),
                            "title": hit.get("title", ""),
                            "doi": hit.get("doi", ""),
                            "url": hit.get("url_public_html", ""),
                        }
                        for hit in hits
                    ],
                }
            elif label == "dryad" and result:
                hits = result.get("_embedded", {}).get("stash:datasets", [])
                count = int(result.get("total", len(hits)))
                top_ids = [
                    hit.get("identifier", "") or hit.get("id", "")
                    for hit in hits
                ]
                raw_hits[qid][label] = {
                    "status": status,
                    "count": count,
                    "hits": [
                        {
                            "id": hit.get("identifier", ""),
                            "title": hit.get("title", ""),
                        }
                        for hit in hits
                    ],
                }
            elif label == "osf_preprints" and result:
                hits = result.get("data", [])
                count = len(hits)
                top_ids = [hit.get("id", "") for hit in hits]
                raw_hits[qid][label] = {
                    "status": status,
                    "count": count,
                    "hits": [
                        {
                            "id": hit.get("id", ""),
                            "title": hit.get("attributes", {}).get("title", ""),
                        }
                        for hit in hits
                    ],
                }
            else:
                count = 0
                top_ids = []
                raw_hits[qid][label] = {"status": status, "count": count, "hits": []}
            rows.append(
                {
                    "query_id": qid,
                    "source": label,
                    "status": status,
                    "count": count,
                    "top_ids": ";".join(top_ids),
                    "query": query,
                }
            )
            time.sleep(0.35)

    with (OUT / "search_counts.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["query_id", "source", "status", "count", "top_ids", "query"], delimiter="\t"
        )
        writer.writeheader()
        writer.writerows(rows)
    (OUT / "raw_search_hits.json").write_text(json.dumps(raw_hits, indent=2, sort_keys=True))


def write_candidate_inventory() -> None:
    candidates = [
        {
            "rank": 1,
            "source": "Gafson et al. 2018 DMF PBMC RNA-seq, PMID 30283812",
            "accession_or_url": "https://pubmed.ncbi.nlm.nih.gov/30283812/",
            "fresh_status": "fresh_not_used",
            "access_tier": "Tier 2 low-barrier author/data request",
            "paired_or_longitudinal": "yes: baseline, 6 weeks, 15 months reported",
            "response_labels": "yes: NEDA-4 reported, sample-level labels not public",
            "module_gene_coverage": "not verified until expression files received",
            "validation_fit": "best primary MS DMF validation target; not public ready-to-run",
            "verdict": "best_next_data_request",
        },
        {
            "rank": 2,
            "source": "GSE130478/GSE130491/GSE130494 Karolinska DMF ROS cohort",
            "accession_or_url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE130494",
            "fresh_status": "fresh_not_used_for_locked_validation",
            "access_tier": "Tier 1 expression/methylation open; Tier 2 labels",
            "paired_or_longitudinal": "yes: baseline/3m/6m across CD4/CD14; expression mainly CD4 baseline/6m",
            "response_labels": "beneficial response in paper/GEO summary; patient-level label mapping absent from public matrix",
            "module_gene_coverage": "likely expression-compatible, not enough for V42 until labels and exact expression table are mapped",
            "validation_fit": "secondary MS DMF cohort after label acquisition; timepoint later than V42 early window",
            "verdict": "low_barrier_label_request",
        },
        {
            "rank": 3,
            "source": "GSE228330 anti-CD20/oCRELIZUMAB PBMC expression",
            "accession_or_url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE228330",
            "fresh_status": "fresh_not_used",
            "access_tier": "Tier 1 open",
            "paired_or_longitudinal": "yes: ocrelizumab patients before, 2 weeks, and 6 months after first infusion",
            "response_labels": "no responder/nonresponder or NEDA labels found in GEO record",
            "module_gene_coverage": "platform should cover module genes, but not counted because response labels absent",
            "validation_fit": "pharmacodynamic QC/context cohort only, not validation",
            "verdict": "open_but_unlabeled_pharmacodynamic",
        },
        {
            "rank": 4,
            "source": "GSE85034 methotrexate arm",
            "accession_or_url": "local: data/raw_v3/wave89_psoriasis_response/GSE85034_series_matrix.txt.gz",
            "fresh_status": "same_study_as_used_ADA_arm_but_MTX_arm_unused",
            "access_tier": "Tier 1 local/open",
            "paired_or_longitudinal": "yes: baseline/week16 lesional skin",
            "response_labels": "yes: PASI75-labeled locally",
            "module_gene_coverage": "verified by V24 as 9 frozen genes represented",
            "validation_fit": "secondary stress test only; non-MS, late, same source as used ADA arm",
            "verdict": "caveated_secondary_stress_test",
        },
        {
            "rank": 5,
            "source": "GSE253495 RA upadacitinib CD14 monocytes",
            "accession_or_url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE253495",
            "fresh_status": "fresh_not_used",
            "access_tier": "Tier 1 open",
            "paired_or_longitudinal": "yes: baseline and 3 months",
            "response_labels": "no discriminating labels; all improved in V24 record review",
            "module_gene_coverage": "RNA-seq, likely module genes present, not a validation cohort",
            "validation_fit": "JAK-class pharmacodynamic source only",
            "verdict": "open_but_no_nonresponder_class",
        },
        {
            "rank": 6,
            "source": "Pharmacogenomics of clinical response to natalizumab, PMID 39264442",
            "accession_or_url": "https://pubmed.ncbi.nlm.nih.gov/39264442/",
            "fresh_status": "fresh_not_used",
            "access_tier": "publication open; data type not transcriptomic",
            "paired_or_longitudinal": "response follow-up, but genome-wide pharmacogenomics rather than expression",
            "response_labels": "yes in paper",
            "module_gene_coverage": "not applicable; no expression modules",
            "validation_fit": "not usable for V22 module validation",
            "verdict": "not_transcriptomic",
        },
        {
            "rank": 7,
            "source": "GSE235357 DMF",
            "accession_or_url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE235357",
            "fresh_status": "already_used_V22",
            "access_tier": "Tier 1 local/open",
            "paired_or_longitudinal": "yes",
            "response_labels": "yes",
            "module_gene_coverage": "yes",
            "validation_fit": "not fresh; already counted",
            "verdict": "exclude_already_used",
        },
        {
            "rank": 8,
            "source": "GSE250453 fingolimod",
            "accession_or_url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE250453",
            "fresh_status": "already_used_V22",
            "access_tier": "Tier 1 local/open",
            "paired_or_longitudinal": "yes",
            "response_labels": "yes",
            "module_gene_coverage": "yes",
            "validation_fit": "not fresh; already counted",
            "verdict": "exclude_already_used",
        },
    ]
    with (OUT / "candidate_inventory.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(candidates[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(candidates)


def main() -> int:
    search_all()
    write_candidate_inventory()
    summary = {
        "status": "complete",
        "query_count": len(QUERIES),
        "candidate_count": 8,
        "verified_ready_primary_tier1_count": 0,
        "best_low_barrier_target": "Gafson et al. 2018 DMF PBMC RNA-seq, PMID 30283812",
        "best_open_secondary": "GSE85034 methotrexate arm, caveated non-MS secondary stress test",
        "new_open_pharmacodynamic_not_validation": "GSE228330 anti-CD20/oCRELIZUMAB PBMC expression",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
