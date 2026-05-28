#!/usr/bin/env python3
"""Wave32-C prior-art and translational-feasibility source inventory.

This script performs reproducible public-source searches for downstream
resolution/macrophage-repair intervention routes. It deliberately does not
promote a target. The output is a traceable source inventory to support a
manual route-by-route prior-art and feasibility attack.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave32c_resolution_prior_art_audit"
RAW = OUT / "raw_api"
SEED = 20260527


ROUTES = [
    {
        "route": "TAM_receptor_agonism",
        "direction": "agonism",
        "targets": ["MERTK", "AXL", "TYRO3", "GAS6", "PROS1"],
        "pubmed_queries": [
            '(MERTK OR MerTK OR AXL OR TYRO3 OR "TAM receptor") AND (agonist OR activation OR GAS6 OR PROS1 OR "Protein S") AND ("multiple sclerosis" OR EAE OR autoimmune OR lupus OR rheumatoid OR psoriasis OR colitis OR "inflammatory bowel")',
            '(GAS6 OR PROS1 OR "Protein S") AND (MERTK OR MerTK OR AXL OR TYRO3) AND (efferocytosis OR macrophage OR microglia) AND autoimmune',
        ],
        "europepmc_queries": [
            '(MERTK OR MerTK OR AXL OR TYRO3 OR "TAM receptor") AND (agonist OR activation OR GAS6 OR PROS1 OR "Protein S") AND (autoimmune OR "multiple sclerosis" OR lupus OR colitis)',
            '(MERTK OR MerTK OR AXL OR TYRO3) AND (bioRxiv OR medRxiv) AND (agonist OR GAS6 OR PROS1) AND autoimmune',
        ],
        "clinicaltrials_terms": ["MERTK agonist", "GAS6", "PROS1 Protein S autoimmune"],
        "patent_queries": [
            'MERTK agonist autoimmune',
            'GAS6 MERTK autoimmune biologic',
            'PROS1 MERTK autoimmune biologic',
        ],
    },
    {
        "route": "TAM_receptor_inhibition",
        "direction": "inhibition",
        "targets": ["MERTK", "AXL", "TYRO3"],
        "pubmed_queries": [
            '(MERTK OR MerTK OR AXL OR TYRO3 OR "TAM receptor") AND (inhibitor OR antagonist OR blockade) AND ("multiple sclerosis" OR EAE OR autoimmune OR lupus OR rheumatoid OR psoriasis OR colitis OR "inflammatory bowel")',
            '(bemcentinib OR gilteritinib OR "AXL inhibitor" OR "MERTK inhibitor") AND (autoimmune OR inflammatory OR lupus OR colitis OR arthritis)',
        ],
        "europepmc_queries": [
            '(MERTK OR MerTK OR AXL OR TYRO3 OR "TAM receptor") AND (inhibitor OR antagonist OR blockade) AND autoimmune',
            '(AXL inhibitor OR MERTK inhibitor OR bemcentinib) AND (autoimmune OR inflammatory disease)',
        ],
        "clinicaltrials_terms": ["AXL inhibitor", "MERTK inhibitor", "bemcentinib autoimmune"],
        "patent_queries": [
            'MERTK inhibitor autoimmune',
            'AXL inhibitor autoimmune',
            'TAM receptor inhibitor autoimmune disease',
        ],
    },
    {
        "route": "TREM2_agonism",
        "direction": "agonism",
        "targets": ["TREM2", "TYROBP"],
        "pubmed_queries": [
            '(TREM2 AND (agonist OR "agonistic antibody" OR activation) AND ("multiple sclerosis" OR EAE OR autoimmune OR remyelination OR microglia))',
            '(TREM2 AND ("multiple sclerosis" OR EAE OR remyelination) AND (microglia OR macrophage OR lipid))',
        ],
        "europepmc_queries": [
            'TREM2 agonist antibody autoimmune microglia',
            'TREM2 multiple sclerosis remyelination microglia lipid',
        ],
        "clinicaltrials_terms": ["TREM2 agonist", "AL002", "INVOKE-2", "TREM2 antibody"],
        "patent_queries": [
            'TREM2 agonist antibody autoimmune',
            'TREM2 agonist antibody multiple sclerosis',
        ],
    },
    {
        "route": "LXR_ABCA1_activation",
        "direction": "agonism",
        "targets": ["NR1H3", "NR1H2", "ABCA1", "ABCG1"],
        "pubmed_queries": [
            '("LXR agonist" OR "liver X receptor agonist" OR T0901317 OR GW3965) AND ("experimental autoimmune encephalomyelitis" OR "multiple sclerosis" OR autoimmune)',
            '(ABCA1 OR ABCG1) AND (microglia OR macrophage) AND ("multiple sclerosis" OR EAE OR remyelination OR autoimmune)',
        ],
        "europepmc_queries": [
            '"LXR agonist" "experimental autoimmune encephalomyelitis"',
            '(ABCA1 OR ABCG1) microglia multiple sclerosis remyelination',
        ],
        "clinicaltrials_terms": ["LXR agonist autoimmune", "LXR-623", "ABCA1 multiple sclerosis"],
        "patent_queries": [
            'LXR agonist multiple sclerosis autoimmune',
            'ABCA1 agonist autoimmune',
        ],
    },
    {
        "route": "PPAR_retinoid_modulation",
        "direction": "agonism_or_modulation",
        "targets": ["PPARG", "PPARA", "RARA", "RARG", "RXRA", "RXRB"],
        "pubmed_queries": [
            '("PPAR gamma" OR pioglitazone OR rosiglitazone) AND ("multiple sclerosis" OR EAE OR autoimmune OR ulcerative colitis OR Crohn)',
            '(retinoid OR "retinoic acid" OR bexarotene OR "RXR agonist") AND ("multiple sclerosis" OR EAE OR autoimmune OR Treg)',
        ],
        "europepmc_queries": [
            'pioglitazone multiple sclerosis clinical trial',
            'retinoic acid autoimmune Treg multiple sclerosis EAE',
        ],
        "clinicaltrials_terms": ["pioglitazone multiple sclerosis", "PPAR gamma ulcerative colitis", "bexarotene multiple sclerosis"],
        "patent_queries": [
            'PPAR gamma agonist multiple sclerosis autoimmune',
            'retinoid receptor agonist multiple sclerosis autoimmune',
        ],
    },
    {
        "route": "GPNMB_modulation",
        "direction": "agonism_or_inhibition_ambiguous",
        "targets": ["GPNMB"],
        "pubmed_queries": [
            '(GPNMB OR "glycoprotein nonmetastatic melanoma protein B") AND ("multiple sclerosis" OR EAE OR autoimmune OR macrophage OR microglia)',
            '(GPNMB OR "glycoprotein nonmetastatic melanoma protein B") AND (antibody OR inhibitor OR agonist OR "antibody-drug conjugate" OR glembatumumab)',
        ],
        "europepmc_queries": [
            'GPNMB multiple sclerosis microglia',
            'GPNMB antibody drug conjugate glembatumumab',
        ],
        "clinicaltrials_terms": ["GPNMB", "glembatumumab vedotin"],
        "patent_queries": [
            'GPNMB autoimmune multiple sclerosis antibody',
            'GPNMB agonist autoimmune',
        ],
    },
    {
        "route": "CD300_family_modulation",
        "direction": "agonism_or_inhibition_ambiguous",
        "targets": ["CD300A", "CD300LF", "CD300E", "CD300C", "CD300LG"],
        "pubmed_queries": [
            '(CD300A OR CD300F OR CD300LF OR CD300E OR "CD300 family") AND (autoimmune OR "multiple sclerosis" OR lupus OR colitis OR psoriasis OR rheumatoid)',
            '(CD300A OR CD300F OR CD300LF) AND (agonist OR antibody OR phosphatidylserine OR ceramide OR efferocytosis OR macrophage)',
        ],
        "europepmc_queries": [
            'CD300F autoimmune efferocytosis macrophage',
            'CD300A CD300F antibody autoimmune disease',
        ],
        "clinicaltrials_terms": ["CD300 autoimmune", "CD300F antibody", "CD300A antibody"],
        "patent_queries": [
            'CD300F agonist antibody autoimmune',
            'CD300A antibody autoimmune disease',
        ],
    },
    {
        "route": "LIPA_LAL_enhancement",
        "direction": "enhancement_replacement",
        "targets": ["LIPA"],
        "pubmed_queries": [
            '("lysosomal acid lipase" OR LIPA OR sebelipase) AND ("multiple sclerosis" OR EAE OR remyelination OR autoimmune)',
            '("lysosomal acid lipase" OR LIPA) AND (macrophage OR microglia OR efferocytosis OR inflammation)',
        ],
        "europepmc_queries": [
            '"lysosomal acid lipase" autoimmune',
            'LIPA multiple sclerosis remyelination microglia',
        ],
        "clinicaltrials_terms": ["sebelipase alfa autoimmune", "lysosomal acid lipase", "LIPA"],
        "patent_queries": [
            'lysosomal acid lipase autoimmune',
            'sebelipase alfa autoimmune',
            'LIPA multiple sclerosis remyelination',
        ],
    },
    {
        "route": "NPC1_NPC2_cholesterol_egress",
        "direction": "enhancement_functional_rescue",
        "targets": ["NPC1", "NPC2"],
        "pubmed_queries": [
            '(NPC1 OR NPC2 OR "Niemann-Pick type C" OR cyclodextrin) AND (autoimmune OR macrophage OR microglia OR "multiple sclerosis")',
            '("hydroxypropyl beta cyclodextrin" OR HPBCD OR adrabetadex) AND (clinical trial OR CNS OR intrathecal OR "Niemann-Pick")',
        ],
        "europepmc_queries": [
            'NPC1 NPC2 autoimmune macrophage',
            'hydroxypropyl beta cyclodextrin Niemann Pick clinical trial CNS',
        ],
        "clinicaltrials_terms": ["hydroxypropyl beta cyclodextrin Niemann-Pick", "adrabetadex", "NPC1 autoimmune"],
        "patent_queries": [
            'NPC1 autoimmune macrophage therapy',
            'hydroxypropyl beta cyclodextrin autoimmune',
        ],
    },
    {
        "route": "specialized_pro_resolving_mediator_FPR2_axis",
        "direction": "agonism",
        "targets": ["FPR2", "ALX", "ALOX15"],
        "pubmed_queries": [
            '(FPR2 OR ALX OR resolvin OR "lipoxin A4" OR annexin A1) AND ("multiple sclerosis" OR EAE OR autoimmune OR colitis OR arthritis OR psoriasis)',
            '("specialized pro-resolving mediator" OR resolvin OR maresin OR protectin) AND (autoimmune OR "multiple sclerosis" OR colitis OR arthritis)',
        ],
        "europepmc_queries": [
            'FPR2 agonist autoimmune colitis arthritis multiple sclerosis',
            'specialized pro-resolving mediator autoimmune disease clinical trial',
        ],
        "clinicaltrials_terms": ["resolvin autoimmune", "FPR2 agonist", "annexin A1 autoimmune"],
        "patent_queries": [
            'FPR2 agonist autoimmune disease',
            'resolvin autoimmune multiple sclerosis',
        ],
    },
]


DRUG_TERMS = [
    "bemcentinib",
    "gilteritinib",
    "UNC2025",
    "AL002",
    "TREM2 agonist antibody",
    "T0901317",
    "GW3965",
    "LXR-623",
    "pioglitazone",
    "rosiglitazone",
    "bexarotene",
    "all-trans retinoic acid",
    "glembatumumab vedotin",
    "sebelipase alfa",
    "hydroxypropyl beta cyclodextrin",
    "adrabetadex",
    "lipoxin A4",
    "resolvin D1",
]


def slug(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
    return text[:90] or hashlib.sha1(text.encode()).hexdigest()[:12]


def get_json(url: str, params: dict[str, Any] | None = None) -> tuple[int | None, Any]:
    try:
        r = requests.get(
            url,
            params=params,
            timeout=35,
            headers={"User-Agent": "ms-auto-research-wave32c/1.0"},
        )
        status = r.status_code
        if status != 200:
            return status, {"error": r.text[:500]}
        return status, r.json()
    except Exception as exc:  # noqa: BLE001 - retained as source inventory
        return None, {"error": repr(exc)}


def pubmed_search(query: str) -> tuple[int | None, dict[str, Any]]:
    status, data = get_json(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        {"db": "pubmed", "retmode": "json", "retmax": 8, "sort": "relevance", "term": query},
    )
    if not isinstance(data, dict) or "esearchresult" not in data:
        return status, {"search": data, "summaries": {}}
    ids = data["esearchresult"].get("idlist", [])
    summaries: dict[str, Any] = {}
    if ids:
        time.sleep(0.34)
        s_status, s_data = get_json(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
            {"db": "pubmed", "retmode": "json", "id": ",".join(ids)},
        )
        summaries = {"status": s_status, "data": s_data}
    return status, {"search": data, "summaries": summaries}


def europepmc_search(query: str) -> tuple[int | None, Any]:
    return get_json(
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
        {
            "query": query,
            "format": "json",
            "pageSize": 8,
            "resultType": "core",
        },
    )


def clinicaltrials_search(term: str) -> tuple[int | None, Any]:
    return get_json(
        "https://clinicaltrials.gov/api/v2/studies",
        {
            "query.term": term,
            "format": "json",
            "pageSize": 8,
        },
    )


def chembl_target_search(term: str) -> tuple[int | None, Any]:
    return get_json(
        "https://www.ebi.ac.uk/chembl/api/data/target/search.json",
        {"q": term, "limit": 8},
    )


def chembl_molecule_search(term: str) -> tuple[int | None, Any]:
    return get_json(
        "https://www.ebi.ac.uk/chembl/api/data/molecule/search.json",
        {"q": term, "limit": 8},
    )


def pubchem_compound_search(term: str) -> tuple[int | None, Any]:
    safe = quote_plus(term)
    return get_json(
        f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{safe}/cids/JSON",
        None,
    )


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def summarize_pubmed(data: dict[str, Any]) -> tuple[int | None, list[str]]:
    try:
        search = data["search"]["esearchresult"]
        count = int(search["count"])
        ids = search.get("idlist", [])
        result = data.get("summaries", {}).get("data", {}).get("result", {})
        titles = []
        for pmid in ids[:5]:
            entry = result.get(pmid, {})
            title = entry.get("title")
            if title:
                titles.append(f"{pmid}: {title}")
        return count, titles
    except Exception:  # noqa: BLE001
        return None, []


def summarize_europepmc(data: dict[str, Any]) -> tuple[int | None, list[str]]:
    try:
        count = int(data.get("hitCount", 0))
        rows = []
        for hit in data.get("resultList", {}).get("result", [])[:5]:
            pmid = hit.get("pmid") or hit.get("id")
            title = hit.get("title", "")
            pub_type = hit.get("pubType", "")
            rows.append(f"{pmid}: {title} [{pub_type}]")
        return count, rows
    except Exception:  # noqa: BLE001
        return None, []


def summarize_trials(data: dict[str, Any]) -> tuple[int | None, list[str]]:
    try:
        studies = data.get("studies", [])
        count = data.get("totalCount")
        rows = []
        for study in studies[:5]:
            protocol = study.get("protocolSection", {})
            ident = protocol.get("identificationModule", {})
            status = protocol.get("statusModule", {})
            conditions = protocol.get("conditionsModule", {}).get("conditions", [])
            design = protocol.get("designModule", {})
            rows.append(
                f"{ident.get('nctId')}: {ident.get('briefTitle')} | "
                f"{status.get('overallStatus')} | {'; '.join(conditions[:3])} | "
                f"{design.get('phases', [])}"
            )
        return count if count is not None else len(studies), rows
    except Exception:  # noqa: BLE001
        return None, []


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    query_rows: list[dict[str, Any]] = []
    hit_rows: list[dict[str, Any]] = []
    db_rows: list[dict[str, Any]] = []
    patent_rows: list[dict[str, Any]] = []

    for route in ROUTES:
        route_name = route["route"]
        for query in route["pubmed_queries"]:
            status, data = pubmed_search(query)
            raw_path = RAW / f"pubmed__{slug(route_name)}__{slug(query)}.json"
            write_json(raw_path, data)
            count, titles = summarize_pubmed(data if isinstance(data, dict) else {})
            query_rows.append(
                {
                    "route": route_name,
                    "direction": route["direction"],
                    "source": "PubMed",
                    "query": query,
                    "status": status,
                    "count": count,
                    "raw_path": str(raw_path.relative_to(ROOT)),
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/?term={quote_plus(query)}",
                }
            )
            hit_rows.append(
                {
                    "route": route_name,
                    "source": "PubMed",
                    "query": query,
                    "count": count,
                    "top_hits": " | ".join(titles),
                }
            )
            time.sleep(0.34)

        for query in route["europepmc_queries"]:
            status, data = europepmc_search(query)
            raw_path = RAW / f"europepmc__{slug(route_name)}__{slug(query)}.json"
            write_json(raw_path, data)
            count, titles = summarize_europepmc(data if isinstance(data, dict) else {})
            query_rows.append(
                {
                    "route": route_name,
                    "direction": route["direction"],
                    "source": "EuropePMC",
                    "query": query,
                    "status": status,
                    "count": count,
                    "raw_path": str(raw_path.relative_to(ROOT)),
                    "url": f"https://europepmc.org/search?query={quote_plus(query)}",
                }
            )
            hit_rows.append(
                {
                    "route": route_name,
                    "source": "EuropePMC",
                    "query": query,
                    "count": count,
                    "top_hits": " | ".join(titles),
                }
            )

        for term in route["clinicaltrials_terms"]:
            status, data = clinicaltrials_search(term)
            raw_path = RAW / f"clinicaltrials__{slug(route_name)}__{slug(term)}.json"
            write_json(raw_path, data)
            count, titles = summarize_trials(data if isinstance(data, dict) else {})
            query_rows.append(
                {
                    "route": route_name,
                    "direction": route["direction"],
                    "source": "ClinicalTrials.gov",
                    "query": term,
                    "status": status,
                    "count": count,
                    "raw_path": str(raw_path.relative_to(ROOT)),
                    "url": f"https://clinicaltrials.gov/search?term={quote_plus(term)}",
                }
            )
            hit_rows.append(
                {
                    "route": route_name,
                    "source": "ClinicalTrials.gov",
                    "query": term,
                    "count": count,
                    "top_hits": " | ".join(titles),
                }
            )

        for query in route["patent_queries"]:
            patent_rows.append(
                {
                    "route": route_name,
                    "direction": route["direction"],
                    "source": "GooglePatents",
                    "query": query,
                    "url": f"https://patents.google.com/?q={quote_plus(query)}",
                }
            )
            patent_rows.append(
                {
                    "route": route_name,
                    "direction": route["direction"],
                    "source": "Espacenet",
                    "query": query,
                    "url": f"https://worldwide.espacenet.com/patent/search?q={quote_plus(query)}",
                    "note": "Espacenet returned HTTP 403 in this environment during spot-check; URL retained for manual/browser verification.",
                }
            )

    for target in sorted({t for route in ROUTES for t in route["targets"]}):
        status, data = chembl_target_search(target)
        raw_path = RAW / f"chembl_target__{slug(target)}.json"
        write_json(raw_path, data)
        targets = data.get("targets", []) if isinstance(data, dict) else []
        for hit in targets[:5]:
            db_rows.append(
                {
                    "database": "ChEMBL target",
                    "query": target,
                    "status": status,
                    "id": hit.get("target_chembl_id"),
                    "name": hit.get("pref_name"),
                    "type": hit.get("target_type"),
                    "organism": hit.get("organism"),
                    "url": f"https://www.ebi.ac.uk/chembl/target_report_card/{hit.get('target_chembl_id')}/"
                    if hit.get("target_chembl_id")
                    else "",
                    "raw_path": str(raw_path.relative_to(ROOT)),
                }
            )

    for drug in DRUG_TERMS:
        status, data = chembl_molecule_search(drug)
        raw_path = RAW / f"chembl_molecule__{slug(drug)}.json"
        write_json(raw_path, data)
        molecules = data.get("molecules", []) if isinstance(data, dict) else []
        for hit in molecules[:5]:
            db_rows.append(
                {
                    "database": "ChEMBL molecule",
                    "query": drug,
                    "status": status,
                    "id": hit.get("molecule_chembl_id"),
                    "name": hit.get("pref_name"),
                    "type": hit.get("molecule_type"),
                    "organism": "",
                    "url": f"https://www.ebi.ac.uk/chembl/compound_report_card/{hit.get('molecule_chembl_id')}/"
                    if hit.get("molecule_chembl_id")
                    else "",
                    "raw_path": str(raw_path.relative_to(ROOT)),
                }
            )

        pc_status, pc_data = pubchem_compound_search(drug)
        pc_path = RAW / f"pubchem_compound__{slug(drug)}.json"
        write_json(pc_path, pc_data)
        cids = pc_data.get("IdentifierList", {}).get("CID", []) if isinstance(pc_data, dict) else []
        for cid in cids[:3]:
            db_rows.append(
                {
                    "database": "PubChem compound",
                    "query": drug,
                    "status": pc_status,
                    "id": cid,
                    "name": drug,
                    "type": "compound",
                    "organism": "",
                    "url": f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}",
                    "raw_path": str(pc_path.relative_to(ROOT)),
                }
            )

    pd.DataFrame(query_rows).to_csv(OUT / "source_query_log.tsv", sep="\t", index=False)
    pd.DataFrame(hit_rows).to_csv(OUT / "api_hit_summary.tsv", sep="\t", index=False)
    pd.DataFrame(db_rows).to_csv(OUT / "target_drug_database_hits.tsv", sep="\t", index=False)
    pd.DataFrame(patent_rows).to_csv(OUT / "patent_search_urls.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "n_routes": len(ROUTES),
        "n_source_queries": len(query_rows),
        "n_db_rows": len(db_rows),
        "n_patent_urls": len(patent_rows),
        "outputs": [
            "source_query_log.tsv",
            "api_hit_summary.tsv",
            "target_drug_database_hits.tsv",
            "patent_search_urls.tsv",
            "raw_api/",
        ],
    }
    write_json(OUT / "summary.json", summary)


if __name__ == "__main__":
    main()
