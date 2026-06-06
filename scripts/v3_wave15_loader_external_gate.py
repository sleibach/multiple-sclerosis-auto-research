#!/usr/bin/env python3
"""External genetics, trial, and prior-art gate for HLA-II loading candidates.

This script checks the loader/dependency candidates surfaced in wave 15 against
public APIs. It deliberately treats Open Targets evidence as locus-level triage
only; no coloc/MR claim is made.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave15_loader_external_gate"
LIT = ROOT / "phases/v3/literature"

OPEN_TARGETS = "https://api.platform.opentargets.org/api/v4/graphql"
EUROPEPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
CLINICALTRIALS = "https://clinicaltrials.gov/api/v2/studies"

CANDIDATES = {
    "CTSH": "ENSG00000103811",
    "CTSS": "ENSG00000163131",
    "CTSB": "ENSG00000164733",
    "CTSL": "ENSG00000135047",
    "CTSD": "ENSG00000117984",
    "IFI30": "ENSG00000216490",
    "HLA-DMA": "ENSG00000204257",
    "HLA-DMB": "ENSG00000242574",
    "LIPA": "ENSG00000107798",
    "LAPTM5": "ENSG00000162511",
    "LGALS3": "ENSG00000131981",
    "LGALS9": "ENSG00000168961",
    "CD44": "ENSG00000026508",
    "SNX10": "ENSG00000086300",
    "RAB5A": "ENSG00000144566",
    "VPS35": "ENSG00000069329",
}

DISEASES = {
    "MS": "MONDO_0005301",
    "RA": "EFO_0000685",
    "SLE": "MONDO_0007915",
    "Crohn": "EFO_0000384",
    "UC": "EFO_0000729",
    "Psoriasis": "EFO_0000676",
    "T1D": "MONDO_0005147",
    "Sjogren": "EFO_0000699",
    "AS": "EFO_0003898",
    "AITD": "EFO_0006812",
    "Celiac": "EFO_0001060",
    "PBC": "EFO_1001486",
}

ALIASES = {
    "CTSH": ["CTSH", '"cathepsin H"'],
    "CTSS": ["CTSS", '"cathepsin S"'],
    "CTSB": ["CTSB", '"cathepsin B"'],
    "CTSL": ["CTSL", '"cathepsin L"'],
    "CTSD": ["CTSD", '"cathepsin D"'],
    "IFI30": ["IFI30", "GILT", '"gamma-interferon-inducible lysosomal thiol reductase"'],
    "HLA-DMA": ['"HLA-DMA"', '"HLA-DM"'],
    "HLA-DMB": ['"HLA-DMB"', '"HLA-DM"'],
    "LIPA": ["LIPA", '"lysosomal acid lipase"'],
    "LAPTM5": ["LAPTM5"],
    "LGALS3": ["LGALS3", "galectin-3"],
    "LGALS9": ["LGALS9", "galectin-9"],
    "CD44": ["CD44"],
    "SNX10": ["SNX10"],
    "RAB5A": ["RAB5A"],
    "VPS35": ["VPS35"],
}

DISEASE_QUERY = (
    '("multiple sclerosis" OR "rheumatoid arthritis" OR lupus OR Crohn OR '
    '"ulcerative colitis" OR psoriasis OR "type 1 diabetes" OR Sjogren OR '
    '"ankylosing spondylitis" OR celiac OR "autoimmune thyroid" OR '
    '"primary biliary cholangitis" OR autoimmune)'
)


def post_graphql(query: str, variables: dict[str, object]) -> dict[str, object]:
    try:
        r = requests.post(OPEN_TARGETS, json={"query": query, "variables": variables}, timeout=45)
        r.raise_for_status()
        data = r.json()
        if "errors" in data:
            return {"status": "graphql_error", "errors": data["errors"]}
        return {"status": "ok", "data": data.get("data")}
    except requests.RequestException as exc:
        return {"status": "request_error", "error": f"{type(exc).__name__}: {exc}"}


def open_targets_gwas(gene: str, ensembl: str) -> list[dict[str, object]]:
    query = """
    query Evidence($ensemblId:String!,$efoIds:[String!]!,$datasourceIds:[String!]){
      target(ensemblId:$ensemblId){
        approvedSymbol
        evidences(efoIds:$efoIds,datasourceIds:$datasourceIds,size:100){
          count
          rows{
            datasourceId
            datatypeId
            score
            disease{ id name }
            literature
          }
        }
      }
    }
    """
    result = post_graphql(
        query,
        {
            "ensemblId": ensembl,
            "efoIds": list(DISEASES.values()),
            "datasourceIds": ["gwas_credible_sets"],
        },
    )
    rows = []
    if result["status"] != "ok":
        return [
            {
                "gene": gene,
                "ensembl": ensembl,
                "status": result["status"],
                "error": json.dumps(result),
            }
        ]
    target = (result.get("data") or {}).get("target") or {}
    evidence = target.get("evidences") or {}
    for row in evidence.get("rows") or []:
        disease = row.get("disease") or {}
        rows.append(
            {
                "gene": gene,
                "ensembl": ensembl,
                "approved_symbol": target.get("approvedSymbol"),
                "status": "ok",
                "disease_id": disease.get("id"),
                "disease_name": disease.get("name"),
                "score": row.get("score"),
                "datasource_id": row.get("datasourceId"),
                "datatype_id": row.get("datatypeId"),
                "literature": ";".join(row.get("literature") or []),
                "error": "",
            }
        )
    if not rows:
        rows.append(
            {
                "gene": gene,
                "ensembl": ensembl,
                "approved_symbol": target.get("approvedSymbol"),
                "status": "ok_no_rows",
                "disease_id": "",
                "disease_name": "",
                "score": 0,
                "datasource_id": "gwas_credible_sets",
                "datatype_id": "",
                "literature": "",
                "error": "",
            }
        )
    return rows


def europepmc_count(query: str) -> dict[str, object]:
    params = {"query": query, "format": "json", "pageSize": 5, "resultType": "lite"}
    try:
        r = requests.get(EUROPEPMC, params=params, timeout=45)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as exc:
        return {
            "query": query,
            "hit_count": None,
            "examples": [],
            "error": f"{type(exc).__name__}: {exc}",
            "url": f"https://europepmc.org/search?query={quote_plus(query)}",
        }
    examples = [
        {
            "id": item.get("id"),
            "source": item.get("source"),
            "title": item.get("title"),
            "journal": item.get("journalTitle"),
            "year": item.get("pubYear"),
            "doi": item.get("doi"),
        }
        for item in data.get("resultList", {}).get("result", [])
    ]
    return {
        "query": query,
        "hit_count": int(data.get("hitCount", 0)),
        "examples": examples,
        "error": "",
        "url": f"https://europepmc.org/search?query={quote_plus(query)}",
    }


def clinical_trials(term: str) -> dict[str, object]:
    try:
        r = requests.get(CLINICALTRIALS, params={"query.term": term, "pageSize": 10, "format": "json"}, timeout=45)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as exc:
        return {
            "term": term,
            "hit_count": None,
            "studies": [],
            "error": f"{type(exc).__name__}: {exc}",
            "url": f"https://clinicaltrials.gov/search?term={quote_plus(term)}",
        }
    studies = []
    for st in data.get("studies", []):
        p = st.get("protocolSection", {})
        studies.append(
            {
                "nct_id": p.get("identificationModule", {}).get("nctId"),
                "title": p.get("identificationModule", {}).get("briefTitle"),
                "status": p.get("statusModule", {}).get("overallStatus"),
                "conditions": ";".join(p.get("conditionsModule", {}).get("conditions", [])),
                "interventions": ";".join(
                    i.get("name", "") for i in p.get("armsInterventionsModule", {}).get("interventions", [])
                ),
            }
        )
    return {
        "term": term,
        "hit_count": len(studies),
        "studies": studies,
        "error": "",
        "url": f"https://clinicaltrials.gov/search?term={quote_plus(term)}",
    }


def literature_queries(gene: str) -> list[str]:
    alias_query = "(" + " OR ".join(ALIASES.get(gene, [gene])) + ")"
    return [
        f"{alias_query} AND {DISEASE_QUERY}",
        f"{alias_query} AND (\"MHC class II\" OR HLA OR CD74 OR CIITA OR \"antigen presentation\")",
        f"{alias_query} AND (inhibitor OR antagonist OR antibody OR trial OR therapeutic)",
    ]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LIT.mkdir(parents=True, exist_ok=True)

    ot_rows: list[dict[str, object]] = []
    for gene, ensembl in CANDIDATES.items():
        ot_rows.extend(open_targets_gwas(gene, ensembl))
        time.sleep(0.2)
    ot = pd.DataFrame(ot_rows)
    ot.to_csv(OUT / "open_targets_gwas_credible_sets.tsv", sep="\t", index=False)

    lit_rows = []
    detail: dict[str, object] = {"europepmc": {}, "clinical_trials": {}, "patent_urls": {}}
    for gene in CANDIDATES:
        detail["europepmc"][gene] = []
        for query in literature_queries(gene):
            item = europepmc_count(query)
            detail["europepmc"][gene].append(item)
            lit_rows.append(
                {
                    "gene": gene,
                    "source": "EuropePMC",
                    "query": query,
                    "hit_count": item["hit_count"],
                    "error": item.get("error", ""),
                    "url": item["url"],
                }
            )
            time.sleep(0.2)
        trial_term = " OR ".join(ALIASES.get(gene, [gene]))
        trial_item = clinical_trials(trial_term)
        detail["clinical_trials"][gene] = trial_item
        lit_rows.append(
            {
                "gene": gene,
                "source": "ClinicalTrials.gov",
                "query": trial_term,
                "hit_count": trial_item["hit_count"],
                "error": trial_item.get("error", ""),
                "url": trial_item["url"],
            }
        )
        patent_query = " ".join(ALIASES.get(gene, [gene])[:2] + ["autoimmune", "antigen presentation"])
        detail["patent_urls"][gene] = {
            "google_patents": f"https://patents.google.com/?q={quote_plus(patent_query)}",
            "espacenet": f"https://worldwide.espacenet.com/patent/search?q={quote_plus(patent_query)}",
            "query": patent_query,
        }
        lit_rows.append(
            {
                "gene": gene,
                "source": "Google Patents URL",
                "query": patent_query,
                "hit_count": None,
                "error": "",
                "url": detail["patent_urls"][gene]["google_patents"],
            }
        )
        lit_rows.append(
            {
                "gene": gene,
                "source": "Espacenet URL",
                "query": patent_query,
                "hit_count": None,
                "error": "",
                "url": detail["patent_urls"][gene]["espacenet"],
            }
        )

    lit = pd.DataFrame(lit_rows)
    lit.to_csv(OUT / "literature_trial_patent_query_log.tsv", sep="\t", index=False)
    (LIT / "wave15_loader_external_gate_detail.json").write_text(json.dumps(detail, indent=2) + "\n")

    summary_rows = []
    for gene in CANDIDATES:
        sub_ot = ot[(ot["gene"] == gene) & (ot["status"] == "ok")].copy()
        sub_ot["score_num"] = pd.to_numeric(sub_ot["score"], errors="coerce").fillna(0)
        diseases_ge_05 = sorted(sub_ot.loc[sub_ot["score_num"] >= 0.5, "disease_name"].dropna().unique())
        diseases_any = sorted(sub_ot.loc[sub_ot["score_num"] > 0, "disease_name"].dropna().unique())
        epmc = lit[(lit["gene"] == gene) & (lit["source"] == "EuropePMC")]
        trial = lit[(lit["gene"] == gene) & (lit["source"] == "ClinicalTrials.gov")]
        hit_counts = pd.to_numeric(epmc["hit_count"], errors="coerce")
        summary_rows.append(
            {
                "gene": gene,
                "ensembl": CANDIDATES[gene],
                "ot_gwas_rows": int(len(sub_ot)),
                "ot_max_score": float(sub_ot["score_num"].max()) if not sub_ot.empty else 0.0,
                "ot_diseases_any": ";".join(diseases_any),
                "ot_n_diseases_any": len(diseases_any),
                "ot_diseases_score_ge_0_5": ";".join(diseases_ge_05),
                "ot_n_diseases_score_ge_0_5": len(diseases_ge_05),
                "europepmc_total_hits_across_queries": int(hit_counts.fillna(0).sum()) if hit_counts.notna().any() else None,
                "clinical_trials_hit_count": trial["hit_count"].iloc[0] if not trial.empty else None,
                "interpretation": "external gate only; Open Targets rows are locus-level and patents are URL queries",
            }
        )
    summary = pd.DataFrame(summary_rows).sort_values(
        ["ot_n_diseases_score_ge_0_5", "ot_n_diseases_any", "europepmc_total_hits_across_queries"],
        ascending=[False, False, True],
    )
    summary.to_csv(OUT / "loader_external_gate_summary.tsv", sep="\t", index=False)
    result = {
        "open_targets_graphql": OPEN_TARGETS,
        "europepmc_api": EUROPEPMC,
        "clinicaltrials_api": CLINICALTRIALS,
        "summary": summary.to_dict(orient="records"),
        "guardrail": "No target-level coloc/MR is claimed; this is an external triage gate.",
    }
    (OUT / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
