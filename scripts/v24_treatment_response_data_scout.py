#!/usr/bin/env python3
"""V24 exhaustive scout for fresh treatment-response validation cohorts."""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v24_data_scout"
USED = {
    "GSE282122",
    "GSE138064",
    "GSE24427",
    "GSE16879",
    "GSE73661",
    "GSE8350",
    "GSE12051",
    "GSE12251",
    "GSE138746",
    "GSE235357",
    "GSE250453",
    "GSE85034",
    "GSE253006",
}

QUERIES = [
    "multiple sclerosis dimethyl fumarate transcriptome response",
    "multiple sclerosis dimethyl fumarate RNA sequencing responder",
    "multiple sclerosis natalizumab transcriptome response",
    "multiple sclerosis ocrelizumab transcriptome response",
    "multiple sclerosis teriflunomide transcriptome response",
    "multiple sclerosis cladribine transcriptome response",
    "multiple sclerosis interferon beta longitudinal transcriptome response",
    "multiple sclerosis DMT PBMC transcriptome responder",
    "multiple sclerosis treatment response RNA-seq baseline longitudinal",
    "ulcerative colitis tofacitinib transcriptome response baseline week",
    "rheumatoid arthritis tofacitinib transcriptome response baseline",
    "rheumatoid arthritis baricitinib transcriptome response baseline",
    "psoriasis tofacitinib transcriptome response baseline",
    "lupus anifrolumab transcriptome response baseline transcriptome",
    "IBD JAK inhibitor transcriptome response baseline",
]


@dataclass
class QueryResult:
    source_type: str
    endpoint: str
    query: str
    status: str
    hit_count: int | None
    ids_or_titles: str
    error: str = ""


@dataclass
class Candidate:
    source_type: str
    accession_or_id: str
    title: str
    url: str
    search_basis: str
    already_used: bool
    access_tier: str
    spec_fit: str
    paired_or_longitudinal: str
    response_labels: str
    module_genes_present: str
    verified_usability: str
    notes: str


def get_json(url: str, timeout: int = 8) -> tuple[int, object | None, str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ms-auto-research-v24"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8", errors="ignore")), ""
    except Exception as exc:  # noqa: BLE001
        return 0, None, repr(exc)


def get_text(url: str, timeout: int = 8) -> tuple[int, str, str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ms-auto-research-v24"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="ignore"), ""
    except Exception as exc:  # noqa: BLE001
        return 0, "", repr(exc)


def geo_search() -> tuple[list[QueryResult], list[Candidate]]:
    results: list[QueryResult] = []
    candidates: list[Candidate] = []
    for q in QUERIES:
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(
            {"db": "gds", "term": q, "retmax": 20, "retmode": "json"}
        )
        status, obj, err = get_json(url)
        if status != 200 or not isinstance(obj, dict):
            results.append(QueryResult("GEO", url, q, "error", None, "", err))
            time.sleep(0.4)
            continue
        ids = obj.get("esearchresult", {}).get("idlist", [])
        count = int(obj.get("esearchresult", {}).get("count", 0))
        results.append(QueryResult("GEO", url, q, "ok", count, ";".join(ids[:20])))
        if ids:
            summ_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?" + urllib.parse.urlencode(
                {"db": "gds", "id": ",".join(ids[:20]), "retmode": "json"}
            )
            s_status, summ, s_err = get_json(summ_url)
            if s_status == 200 and isinstance(summ, dict):
                for gid in ids[:20]:
                    rec = summ.get("result", {}).get(gid, {})
                    title = rec.get("title", "")
                    acc = rec.get("accession", "") or rec.get("gds", "") or gid
                    gse_hits = re.findall(r"GSE\d+", title + " " + json.dumps(rec))
                    accession = gse_hits[0] if gse_hits else acc
                    if not accession:
                        accession = gid
                    candidates.append(
                        Candidate(
                            source_type="GEO",
                            accession_or_id=accession,
                            title=title,
                            url=f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={accession}" if accession.startswith("GSE") else summ_url,
                            search_basis=q,
                            already_used=any(u in accession or u in title for u in USED),
                            access_tier="Tier 1 if supplementary matrices/metadata include labels; otherwise unknown",
                            spec_fit="nominal_hit_needs_record_inspection",
                            paired_or_longitudinal="unverified",
                            response_labels="unverified",
                            module_genes_present="unverified",
                            verified_usability="not_verified",
                            notes="GEO search hit; title-level only.",
                        )
                    )
            else:
                results.append(QueryResult("GEO", summ_url, q + " summary", "error", None, "", s_err))
        time.sleep(0.4)
    return results, candidates


def europepmc_search() -> tuple[list[QueryResult], list[Candidate]]:
    results: list[QueryResult] = []
    candidates: list[Candidate] = []
    for q in QUERIES + ["MultipleMS transcriptomics treatment response", "MS PATHS transcriptomics treatment response"]:
        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(
            {"query": q, "format": "json", "pageSize": 15}
        )
        status, obj, err = get_json(url)
        if status != 200 or not isinstance(obj, dict):
            results.append(QueryResult("EuropePMC", url, q, "error", None, "", err))
            continue
        hit_count = int(obj.get("hitCount", 0))
        titles = []
        for rec in obj.get("resultList", {}).get("result", [])[:15]:
            title = rec.get("title", "")
            titles.append(title)
            text = title + " " + rec.get("abstractText", "")
            for acc in sorted(set(re.findall(r"GSE\d+|E-MTAB-\d+|EGA[SD]\d+|SRP\d+|PRJNA\d+", text))):
                candidates.append(
                    Candidate(
                        source_type="Published-paper mining",
                        accession_or_id=acc,
                        title=title,
                        url=rec.get("doi") or rec.get("pmid") or url,
                        search_basis=q,
                        already_used=any(u in acc for u in USED),
                        access_tier="unknown_from_paper_mining",
                        spec_fit="paper_mentions_accession_needs_record_inspection",
                        paired_or_longitudinal="unverified",
                        response_labels="unverified",
                        module_genes_present="unverified",
                        verified_usability="not_verified",
                        notes="Accession mined from Europe PMC title/abstract.",
                    )
                )
        results.append(QueryResult("EuropePMC", url, q, "ok", hit_count, " | ".join(titles[:5])))
        time.sleep(0.25)
    return results, candidates


def biostudies_search() -> tuple[list[QueryResult], list[Candidate]]:
    results: list[QueryResult] = []
    candidates: list[Candidate] = []
    for q in QUERIES:
        url = "https://www.ebi.ac.uk/biostudies/api/v1/search?" + urllib.parse.urlencode({"query": q, "pageSize": 20})
        status, obj, err = get_json(url)
        if status != 200 or not isinstance(obj, dict):
            results.append(QueryResult("ArrayExpress/BioStudies", url, q, "error", None, "", err))
            continue
        hits = obj.get("hits", []) or obj.get("content", [])
        titles = []
        for rec in hits[:20]:
            acc = rec.get("accession") or rec.get("accno") or rec.get("id", "")
            title = rec.get("title", "") or rec.get("name", "")
            titles.append(f"{acc}:{title}")
            candidates.append(
                Candidate(
                    source_type="ArrayExpress/BioStudies",
                    accession_or_id=acc,
                    title=title,
                    url=f"https://www.ebi.ac.uk/biostudies/{acc}" if acc else url,
                    search_basis=q,
                    already_used=any(u in acc or u in title for u in USED),
                    access_tier="Tier 1 if files public; Tier 3 if EGA linked",
                    spec_fit="nominal_hit_needs_record_inspection",
                    paired_or_longitudinal="unverified",
                    response_labels="unverified",
                    module_genes_present="unverified",
                    verified_usability="not_verified",
                    notes="BioStudies search hit.",
                )
            )
        results.append(QueryResult("ArrayExpress/BioStudies", url, q, "ok", len(hits), " | ".join(titles[:5])))
        time.sleep(0.25)
    return results, candidates


def ena_search() -> tuple[list[QueryResult], list[Candidate]]:
    results: list[QueryResult] = []
    candidates: list[Candidate] = []
    for q in QUERIES[:10]:
        url = "https://www.ebi.ac.uk/ena/portal/api/search?" + urllib.parse.urlencode(
            {"result": "study", "query": f'description="{q}"', "fields": "study_accession,secondary_study_accession,study_title", "format": "json", "limit": 20}
        )
        status, obj, err = get_json(url)
        if status != 200 or not isinstance(obj, list):
            results.append(QueryResult("ENA/SRA", url, q, "error", None, "", err))
            continue
        titles = []
        for rec in obj:
            acc = rec.get("study_accession") or rec.get("secondary_study_accession", "")
            title = rec.get("study_title", "")
            titles.append(f"{acc}:{title}")
            candidates.append(
                Candidate("ENA/SRA", acc, title, f"https://www.ebi.ac.uk/ena/browser/view/{acc}", q, any(u in title for u in USED), "Tier 1 raw sequencing if metadata adequate", "nominal_hit_needs_metadata", "unverified", "unverified", "unverified", "not_verified", "ENA study hit; raw data may lack response labels.")
            )
        results.append(QueryResult("ENA/SRA", url, q, "ok", len(obj), " | ".join(titles[:5])))
        time.sleep(0.25)
    return results, candidates


def repository_search(source: str, base: str, parser: str) -> tuple[list[QueryResult], list[Candidate]]:
    results: list[QueryResult] = []
    candidates: list[Candidate] = []
    for q in QUERIES[:8]:
        url = base.format(q=urllib.parse.quote(q))
        status, obj, err = get_json(url)
        if status != 200:
            results.append(QueryResult(source, url, q, "error", None, "", err))
            continue
        records = []
        if parser == "zenodo":
            records = obj.get("hits", {}).get("hits", []) if isinstance(obj, dict) else []
        elif parser == "figshare":
            records = obj if isinstance(obj, list) else []
        elif parser == "osf":
            records = obj.get("data", []) if isinstance(obj, dict) else []
        titles = []
        for rec in records[:10]:
            if parser == "zenodo":
                meta = rec.get("metadata", {})
                acc = str(rec.get("id", ""))
                title = meta.get("title", "")
                link = rec.get("links", {}).get("html", url)
            elif parser == "figshare":
                acc = str(rec.get("id", ""))
                title = rec.get("title", "")
                link = rec.get("url_public_html", url)
            else:
                acc = rec.get("id", "")
                title = rec.get("attributes", {}).get("title", "")
                link = rec.get("links", {}).get("html", url)
            titles.append(title)
            candidates.append(Candidate(source, acc, title, link, q, any(u in title for u in USED), "Tier 1 if files public", "nominal_repository_hit", "unverified", "unverified", "unverified", "not_verified", f"{source} search hit."))
        results.append(QueryResult(source, url, q, "ok", len(records), " | ".join(titles[:5])))
        time.sleep(0.25)
    return results, candidates


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    all_results: list[QueryResult] = []
    all_candidates: list[Candidate] = []
    for fn in [geo_search, europepmc_search, biostudies_search, ena_search]:
        r, c = fn()
        all_results.extend(r)
        all_candidates.extend(c)
    for source, base, parser in [
        ("Zenodo", "https://zenodo.org/api/records?q={q}&size=10", "zenodo"),
        ("Figshare", "https://api.figshare.com/v2/articles/search?search_for={q}&page_size=10", "figshare"),
        ("OSF", "https://api.osf.io/v2/search/?q={q}&page[size]=10", "osf"),
    ]:
        r, c = repository_search(source, base, parser)
        all_results.extend(r)
        all_candidates.extend(c)

    # Dryad has less stable public search APIs; capture a web-search URL for audit.
    for q in QUERIES[:8]:
        all_results.append(QueryResult("Dryad", f"https://datadryad.org/search?q={urllib.parse.quote(q)}", q, "manual_url_recorded", None, "", "Dryad API not used; manual URL recorded for audit."))

    # De-duplicate candidates by accession/title/source.
    seen = set()
    unique = []
    for cand in all_candidates:
        key = (cand.source_type, cand.accession_or_id, cand.title)
        if key in seen:
            continue
        seen.add(key)
        unique.append(cand)

    pd = __import__("pandas")
    pd.DataFrame([asdict(x) for x in all_results]).to_csv(OUT / "v24_search_log.tsv", sep="\t", index=False)
    pd.DataFrame([asdict(x) for x in unique]).to_csv(OUT / "v24_candidate_inventory_raw.tsv", sep="\t", index=False)
    print(json.dumps({"queries": len(all_results), "raw_candidates": len(all_candidates), "unique_candidates": len(unique)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
