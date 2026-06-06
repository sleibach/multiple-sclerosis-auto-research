#!/usr/bin/env python3
"""Prior-art and trial audit for V3 intervention candidates.

This script queries public APIs with fixed search strings and records counts and
trial hits. It is a triage audit, not a substitute for full patent counsel or a
systematic review. Google Patents/Espacenet searches are recorded as query URLs
because neither source provides a simple unauthenticated stable JSON API here.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results"
LIT = ROOT / "phases/v3/literature"

CANDIDATES = {
    "IFNG_IFNGR_axis": {
        "terms": [
            '"IFNGR1" autoimmune',
            '"IFNGR2" autoimmune',
            '"interferon gamma receptor" autoimmune',
            '"anti-IFN-gamma" autoimmune',
            '"emapalumab" autoimmune',
            '"IFN-gamma" "multiple sclerosis"',
            '"IFN-gamma" Crohn psoriasis Sjogren',
        ],
        "trial_terms": [
            "IFN gamma autoimmune",
            "emapalumab autoimmune",
            "anti IFN gamma",
            "interferon gamma receptor autoimmune",
        ],
    },
    "IRF1_STAT1_program": {
        "terms": [
            '"IRF1" autoimmune',
            '"STAT1" autoimmune',
            '"IRF1" "multiple sclerosis"',
            '"IRF1" "Crohn"',
            '"IRF1" psoriasis',
            '"STAT1" "multiple sclerosis"',
            '"STAT1" Crohn psoriasis Sjogren',
        ],
        "trial_terms": ["IRF1 autoimmune", "STAT1 autoimmune"],
    },
    "CIITA_RFX5_HLAII_gate": {
        "terms": [
            '"CIITA" autoimmune',
            '"RFX5" autoimmune',
            '"CIITA inhibitor" autoimmune',
            '"MHC class II transactivator" autoimmune',
            '"RFX5" "multiple sclerosis"',
            '"CIITA" Crohn psoriasis Sjogren',
        ],
        "trial_terms": ["CIITA autoimmune", "RFX5 autoimmune", "MHC class II transactivator"],
    },
    "TYK2_JAK_STAT": {
        "terms": [
            '"TYK2 inhibitor" autoimmune',
            'deucravacitinib lupus Crohn ulcerative colitis multiple sclerosis',
            '"TYK2" "multiple sclerosis"',
        ],
        "trial_terms": ["deucravacitinib", "TYK2 inhibitor autoimmune", "zasocitinib", "ropsacitinib"],
    },
    "CTSS_cathepsin_S": {
        "terms": [
            '"cathepsin S inhibitor" autoimmune',
            '"cathepsin S" "multiple sclerosis"',
            '"CTSS" Sjogren',
            '"CTSS" celiac',
            '"CTSS" "primary biliary cholangitis"',
        ],
        "trial_terms": ["cathepsin S autoimmune", "RO5459072", "petesicatib", "RWJ-445380", "VBY-891"],
    },
    "IFI30_GILT": {
        "terms": [
            '"IFI30" autoimmune',
            '"GILT" antigen processing autoimmune',
            '"IFI30" "multiple sclerosis"',
            '"IFI30" "Crohn"',
            '"IFI30" psoriasis',
        ],
        "trial_terms": ["IFI30", "GILT autoimmune"],
    },
    "CD74_MIF": {
        "terms": [
            '"CD74" MIF autoimmune',
            '"CD74" "multiple sclerosis"',
            '"CD74" Sjogren',
            '"CD74" "primary biliary cholangitis"',
        ],
        "trial_terms": ["CD74 autoimmune", "milatuzumab", "MIF CD74 autoimmune"],
    },
    "CXCL10_CXCR3": {
        "terms": [
            '"CXCL10" autoimmune',
            '"CXCL10" "primary biliary cholangitis"',
            '"CXCL10" "multiple sclerosis"',
            '"CXCL10" Sjogren',
        ],
        "trial_terms": ["CXCL10 autoimmune", "NI-0801", "anti-CXCL10"],
    },
    "OSM_OSMR": {
        "terms": [
            '"oncostatin M" autoimmune',
            '"OSMR" Crohn ulcerative colitis psoriasis ankylosing',
            '"oncostatin M" "multiple sclerosis"',
            '"GSK2330811" Crohn',
        ],
        "trial_terms": ["GSK2330811", "oncostatin M", "OSM Crohn"],
    },
    "TREM1": {
        "terms": [
            '"TREM1" inflammatory bowel disease',
            '"TREM1" autoimmune',
            '"TREM1" multiple sclerosis',
        ],
        "trial_terms": ["TREM1 autoimmune", "TREM1 inflammatory bowel disease"],
    },
}


def europepmc_count(query: str) -> dict[str, object]:
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {"query": query, "format": "json", "pageSize": 3, "resultType": "lite"}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    examples = []
    for item in data.get("resultList", {}).get("result", []):
        examples.append(
            {
                "id": item.get("id"),
                "source": item.get("source"),
                "title": item.get("title"),
                "journal": item.get("journalTitle"),
                "year": item.get("pubYear"),
                "doi": item.get("doi"),
            }
        )
    return {
        "query": query,
        "hit_count": int(data.get("hitCount", 0)),
        "examples": examples,
        "url": f"https://europepmc.org/search?query={quote_plus(query)}",
    }


def clinical_trials(term: str) -> dict[str, object]:
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {"query.term": term, "pageSize": 10, "format": "json"}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    studies = []
    for st in r.json().get("studies", []):
        p = st.get("protocolSection", {})
        studies.append(
            {
                "nct_id": p.get("identificationModule", {}).get("nctId"),
                "title": p.get("identificationModule", {}).get("briefTitle"),
                "status": p.get("statusModule", {}).get("overallStatus"),
                "phase": ",".join(p.get("designModule", {}).get("phases", [])),
                "conditions": ";".join(p.get("conditionsModule", {}).get("conditions", [])),
                "interventions": ";".join(
                    i.get("name", "")
                    for i in p.get("armsInterventionsModule", {}).get("interventions", [])
                ),
            }
        )
    return {
        "term": term,
        "hit_count": len(studies),
        "studies": studies,
        "url": f"https://clinicaltrials.gov/search?term={quote_plus(term)}",
    }


def main() -> None:
    OUT.mkdir(exist_ok=True)
    LIT.mkdir(exist_ok=True)
    rows = []
    detail: dict[str, object] = {}
    for candidate, spec in CANDIDATES.items():
        detail[candidate] = {"literature": [], "trials": []}
        for query in spec["terms"]:
            item = europepmc_count(query)
            detail[candidate]["literature"].append(item)
            rows.append(
                {
                    "candidate": candidate,
                    "source": "EuropePMC",
                    "query": query,
                    "hit_count": item["hit_count"],
                    "url": item["url"],
                }
            )
        for term in spec["trial_terms"]:
            item = clinical_trials(term)
            detail[candidate]["trials"].append(item)
            rows.append(
                {
                    "candidate": candidate,
                    "source": "ClinicalTrials.gov",
                    "query": term,
                    "hit_count": item["hit_count"],
                    "url": item["url"],
                }
            )
        patent_query = " OR ".join(spec["terms"][:2])
        rows.append(
            {
                "candidate": candidate,
                "source": "Google Patents URL",
                "query": patent_query,
                "hit_count": None,
                "url": f"https://patents.google.com/?q=({quote_plus(patent_query)})",
            }
        )
        rows.append(
            {
                "candidate": candidate,
                "source": "Espacenet URL",
                "query": patent_query,
                "hit_count": None,
                "url": f"https://worldwide.espacenet.com/patent/search?q={quote_plus(patent_query)}",
            }
        )

    pd.DataFrame(rows).to_csv(OUT / "intervention_prior_art_audit.tsv", sep="\t", index=False)
    (LIT / "intervention_prior_art_audit_detail.json").write_text(json.dumps(detail, indent=2) + "\n")
    print(json.dumps({"rows": len(rows), "detail_file": str(LIT / "intervention_prior_art_audit_detail.json")}, indent=2))


if __name__ == "__main__":
    main()
