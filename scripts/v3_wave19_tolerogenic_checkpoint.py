#!/usr/bin/env python3
"""Wave19 tolerogenic/myeloid inhibitory checkpoint screen.

This script aggregates existing V3 local recurrence/state-coupling tables for
myeloid/tolerogenic checkpoint axes and appends a lightweight public-source
prior-art snapshot. API failures are recorded as failures, not as zero evidence.
"""

from __future__ import annotations

import csv
import json
import math
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results_v3"
OUT = RESULTS / "wave19_tolerogenic_checkpoint"
RAW = OUT / "raw_api"

AUTOIMMUNE_TERMS = (
    'autoimmune OR "multiple sclerosis" OR lupus OR "rheumatoid arthritis" OR '
    'Crohn OR "ulcerative colitis" OR psoriasis OR Sjogren OR "type 1 diabetes"'
)

CANDIDATES: dict[str, dict[str, Any]] = {
    "VSIR": {
        "axis": "VISTA/VSIR myeloid checkpoint",
        "aliases": "VISTA;B7-H5;PD-1H",
        "desired_direction": "agonize or enhance inhibitory VISTA signaling",
        "modality": "agonist antibody/fusion protein concept; oncology programs mostly antagonize",
        "delivery": "systemic biologic; tissue-selective delivery not established",
        "literature_query": '(VSIR OR "VISTA checkpoint" OR "V-domain Ig suppressor") autoimmune',
        "trial_query": "VSIR VISTA autoimmune",
        "patent_query": "VSIR VISTA agonist autoimmune disease",
    },
    "LILRB4": {
        "axis": "LILRB4/ILT3 inhibitory myeloid receptor",
        "aliases": "ILT3;CD85K",
        "desired_direction": "agonize inhibitory receptor on tolerogenic myeloid/APC cells",
        "modality": "agonist antibody or ligand-mimetic concept; oncology programs mostly block/deplete",
        "delivery": "systemic biologic; myeloid selectivity possible but tissue delivery undeveloped",
        "literature_query": '(LILRB4 OR ILT3 OR CD85K) autoimmune',
        "trial_query": "LILRB4 ILT3 autoimmune",
        "patent_query": "LILRB4 ILT3 agonist autoimmune disease",
    },
    "LAIR1": {
        "axis": "LAIR1 collagen/complement inhibitory receptor",
        "aliases": "CD305",
        "desired_direction": "agonize LAIR1 inhibitory signaling or restore receptor function",
        "modality": "agonist antibody/fusion protein concept",
        "delivery": "systemic biologic; collagen-rich tissues raise off-tissue complexity",
        "literature_query": '(LAIR1 OR CD305) autoimmune',
        "trial_query": "LAIR1 autoimmune",
        "patent_query": "LAIR1 agonist autoimmune disease",
    },
    "CD200R1": {
        "axis": "CD200-CD200R inhibitory myeloid checkpoint",
        "aliases": "CD200R",
        "desired_direction": "agonize CD200R1 or provide CD200-like ligand signal",
        "modality": "CD200-Fc/agonist antibody concept",
        "delivery": "systemic or mucosal biologic concept; local tissue route undeveloped",
        "literature_query": '(CD200R1 OR CD200R OR "CD200 receptor") autoimmune',
        "trial_query": "CD200R autoimmune",
        "patent_query": "CD200R agonist autoimmune disease",
    },
    "SIGLEC10": {
        "axis": "CD24-SIGLEC10 DAMP/glycan checkpoint",
        "aliases": "Siglec-10",
        "desired_direction": "agonize Siglec-10 via CD24/CD24Fc-like checkpoint engagement",
        "modality": "CD24Fc/fusion protein or Siglec agonist glycomimetic",
        "delivery": "systemic biologic; gut or CNS delivery not solved",
        "literature_query": '(SIGLEC10 OR "Siglec-10" OR CD24Fc) autoimmune',
        "trial_query": "CD24Fc autoimmune",
        "patent_query": "CD24Fc Siglec-10 autoimmune disease",
    },
    "LILRB3": {
        "axis": "LILRB3/ILT5 inhibitory myeloid receptor",
        "aliases": "ILT5;CD85A",
        "desired_direction": "agonize inhibitory receptor if disease-state coupling exists",
        "modality": "antibody modulation concept",
        "delivery": "systemic biologic; little tissue-targeted precedent",
        "literature_query": '(LILRB3 OR ILT5 OR CD85A) autoimmune',
        "trial_query": "LILRB3 autoimmune",
        "patent_query": "LILRB3 ILT5 autoimmune antibody",
    },
    "LILRB5": {
        "axis": "LILRB5 inhibitory receptor",
        "aliases": "LIR8;CD85C",
        "desired_direction": "agonize inhibitory receptor if disease-state coupling exists",
        "modality": "antibody modulation concept",
        "delivery": "systemic biologic; little tissue-targeted precedent",
        "literature_query": '(LILRB5 OR LIR8 OR CD85C) autoimmune',
        "trial_query": "LILRB5 autoimmune",
        "patent_query": "LILRB5 LIR8 autoimmune antibody",
    },
    "HAVCR2": {
        "axis": "TIM-3/HAVCR2 checkpoint",
        "aliases": "TIM-3;TIM3",
        "desired_direction": "agonize tolerogenic TIM-3 signaling, not oncology-style blockade",
        "modality": "agonist biologic concept; Gal-9/TIM-3 axis is crowded",
        "delivery": "systemic biologic; cell-selective direction difficult",
        "literature_query": '(HAVCR2 OR "TIM-3" OR TIM3) autoimmune',
        "trial_query": "TIM-3 autoimmune",
        "patent_query": "TIM-3 HAVCR2 agonist autoimmune disease",
    },
    "TIGIT": {
        "axis": "TIGIT/PVR checkpoint",
        "aliases": "TIGIT",
        "desired_direction": "agonize TIGIT inhibitory signaling; T-cell/Treg weighted",
        "modality": "agonist antibody concept; oncology programs mostly antagonize",
        "delivery": "systemic biologic; not myeloid/APC-state selective",
        "literature_query": '(TIGIT) autoimmune',
        "trial_query": "TIGIT autoimmune",
        "patent_query": "TIGIT agonist autoimmune disease",
    },
    "BTLA": {
        "axis": "BTLA-HVEM checkpoint",
        "aliases": "CD272",
        "desired_direction": "agonize BTLA inhibitory signaling",
        "modality": "agonist antibody or HVEM-ligand biologic concept",
        "delivery": "systemic biologic; T-cell weighted rather than myeloid selective",
        "literature_query": '(BTLA OR CD272) autoimmune',
        "trial_query": "BTLA autoimmune",
        "patent_query": "BTLA agonist autoimmune disease",
    },
    "CD300A": {
        "axis": "CD300A phospholipid inhibitory receptor",
        "aliases": "CMRF35H;IRC1",
        "desired_direction": "agonize inhibitory CD300A signaling if state-coupled",
        "modality": "antibody modulation concept",
        "delivery": "systemic biologic; no disease-tissue selectivity",
        "literature_query": '(CD300A OR CMRF35H) autoimmune',
        "trial_query": "CD300A autoimmune",
        "patent_query": "CD300A autoimmune antibody",
    },
    "CD300LF": {
        "axis": "CD300LF/CD300F phospholipid inhibitory receptor",
        "aliases": "CD300F;IREM1",
        "desired_direction": "agonize inhibitory CD300F/CD300LF signaling",
        "modality": "antibody modulation concept",
        "delivery": "systemic biologic; no disease-tissue selectivity",
        "literature_query": '(CD300LF OR CD300F OR IREM1) autoimmune',
        "trial_query": "CD300F autoimmune",
        "patent_query": "CD300F CD300LF autoimmune antibody",
    },
    "CD274": {
        "axis": "PD-L1/PD-1 tolerance checkpoint",
        "aliases": "PD-L1;B7-H1",
        "desired_direction": "agonize PD-1 pathway or provide PD-L1-like tolerogenic signal",
        "modality": "PD-L1-Fc/PD-1 agonist biologic concept",
        "delivery": "systemic biologic; tissue-targeted tolerization required to avoid broad suppression",
        "literature_query": '(CD274 OR "PD-L1" OR B7-H1) autoimmune',
        "trial_query": "PD-L1 autoimmune",
        "patent_query": "PD-L1 agonist autoimmune disease CD274",
    },
    "PDCD1LG2": {
        "axis": "PD-L2/PD-1 tolerance checkpoint",
        "aliases": "PD-L2;B7-DC",
        "desired_direction": "agonize PD-1 pathway via PD-L2-like signal",
        "modality": "fusion protein/agonist biologic concept",
        "delivery": "systemic biologic; tissue selectivity unresolved",
        "literature_query": '(PDCD1LG2 OR "PD-L2" OR B7-DC) autoimmune',
        "trial_query": "PD-L2 autoimmune",
        "patent_query": "PD-L2 agonist autoimmune disease",
    },
    "CD24": {
        "axis": "CD24-SIGLEC10 DAMP/glycan checkpoint ligand",
        "aliases": "CD24Fc",
        "desired_direction": "agonize CD24-Siglec-10 inhibitory DAMP checkpoint",
        "modality": "CD24Fc or engineered CD24 ligand",
        "delivery": "systemic biologic; tissue-local activity not proven",
        "literature_query": '(CD24 OR CD24Fc) autoimmune',
        "trial_query": "CD24Fc autoimmune",
        "patent_query": "CD24Fc autoimmune disease Siglec-10",
    },
    "CD200": {
        "axis": "CD200-CD200R inhibitory myeloid checkpoint ligand",
        "aliases": "OX2",
        "desired_direction": "provide CD200-like inhibitory signal to CD200R1",
        "modality": "CD200-Fc/ligand fusion concept",
        "delivery": "systemic or mucosal biologic concept",
        "literature_query": '(CD200 OR OX2) autoimmune',
        "trial_query": "CD200 autoimmune",
        "patent_query": "CD200 fusion autoimmune disease",
    },
    "LILRB1": {
        "axis": "LILRB1/ILT2 inhibitory HLA receptor",
        "aliases": "ILT2;CD85J",
        "desired_direction": "agonize inhibitory HLA receptor if disease-state coupling exists",
        "modality": "antibody/HLA-ligand biologic concept",
        "delivery": "systemic biologic; broad leukocyte expression risk",
        "literature_query": '(LILRB1 OR ILT2 OR CD85J) autoimmune',
        "trial_query": "LILRB1 autoimmune",
        "patent_query": "LILRB1 ILT2 autoimmune antibody",
    },
    "LILRB2": {
        "axis": "LILRB2/ILT4 inhibitory myeloid HLA receptor",
        "aliases": "ILT4;CD85D",
        "desired_direction": "agonize inhibitory myeloid HLA receptor",
        "modality": "agonist antibody/HLA-ligand biologic concept; oncology antagonists are opposite",
        "delivery": "systemic biologic; tissue-selective delivery undeveloped",
        "literature_query": '(LILRB2 OR ILT4 OR CD85D) autoimmune',
        "trial_query": "LILRB2 autoimmune",
        "patent_query": "LILRB2 ILT4 agonist autoimmune disease",
    },
    "SIRPA": {
        "axis": "CD47-SIRPA phagocytosis checkpoint receptor",
        "aliases": "SIRP-alpha;SIRPα",
        "desired_direction": "enhance inhibitory SIRPA signaling if repair-preserving; avoid oncology-style blockade",
        "modality": "SIRPA/CD47 biologic modulation",
        "delivery": "systemic biologic; macrophage phagocytosis liabilities",
        "literature_query": '(SIRPA OR "SIRP alpha" OR "SIRP-alpha") autoimmune',
        "trial_query": "SIRPA autoimmune",
        "patent_query": "SIRPA CD47 autoimmune disease",
    },
    "CD47": {
        "axis": "CD47-SIRPA phagocytosis checkpoint ligand",
        "aliases": "IAP",
        "desired_direction": "enhance do-not-eat signaling only if state-coupled; blockade likely wrong",
        "modality": "CD47/SIRPA biologic modulation",
        "delivery": "systemic biologic has anemia/phagocytosis liabilities",
        "literature_query": '(CD47 OR "integrin associated protein") autoimmune',
        "trial_query": "CD47 autoimmune",
        "patent_query": "CD47 SIRPA autoimmune disease",
    },
    "VSIG4": {
        "axis": "VSIG4/CRIg macrophage inhibitory/complement receptor",
        "aliases": "CRIg;Z39IG",
        "desired_direction": "agonize/restore macrophage inhibitory or complement-clearance function",
        "modality": "fusion protein/antibody concept",
        "delivery": "macrophage-rich tissue delivery unresolved",
        "literature_query": '(VSIG4 OR CRIg) autoimmune',
        "trial_query": "VSIG4 autoimmune",
        "patent_query": "VSIG4 CRIg autoimmune disease",
    },
    "CLEC12A": {
        "axis": "CLEC12A/MICL inhibitory myeloid receptor",
        "aliases": "MICL;CLL-1",
        "desired_direction": "agonize inhibitory myeloid receptor if state-coupled",
        "modality": "antibody modulation concept; oncology targeting precedent",
        "delivery": "systemic biologic; myeloid depletion risk if wrong format",
        "literature_query": '(CLEC12A OR MICL OR CLL-1) autoimmune',
        "trial_query": "CLEC12A autoimmune",
        "patent_query": "CLEC12A MICL autoimmune antibody",
    },
    "FCGR2B": {
        "axis": "Fc-gamma RIIB inhibitory Fc receptor",
        "aliases": "CD32B;FcgRIIB",
        "desired_direction": "agonize inhibitory Fc receptor in immune-complex settings",
        "modality": "Fc-engineered immune complexes/agonist antibody concept",
        "delivery": "systemic; disease-specific immune-complex context needed",
        "literature_query": '(FCGR2B OR CD32B OR FcgRIIB) autoimmune',
        "trial_query": "FCGR2B autoimmune",
        "patent_query": "FCGR2B CD32B autoimmune agonist",
    },
    "SIGLEC5": {
        "axis": "Siglec inhibitory glycan receptor",
        "aliases": "Siglec-5;CD170",
        "desired_direction": "agonize inhibitory glycan receptor if state-coupled",
        "modality": "glycomimetic/antibody concept",
        "delivery": "systemic biologic/glycan ligand; specificity difficult",
        "literature_query": '(SIGLEC5 OR "Siglec-5" OR CD170) autoimmune',
        "trial_query": "Siglec-5 autoimmune",
        "patent_query": "Siglec-5 autoimmune glycomimetic",
    },
    "SIGLEC7": {
        "axis": "Siglec inhibitory glycan receptor",
        "aliases": "Siglec-7;CD328",
        "desired_direction": "agonize inhibitory glycan receptor if state-coupled",
        "modality": "glycomimetic/antibody concept",
        "delivery": "systemic; NK/myeloid pleiotropy",
        "literature_query": '(SIGLEC7 OR "Siglec-7" OR CD328) autoimmune',
        "trial_query": "Siglec-7 autoimmune",
        "patent_query": "Siglec-7 autoimmune glycomimetic",
    },
    "SIGLEC9": {
        "axis": "Siglec inhibitory glycan receptor",
        "aliases": "Siglec-9;CD329",
        "desired_direction": "agonize inhibitory glycan receptor if state-coupled",
        "modality": "glycomimetic/antibody concept",
        "delivery": "systemic; neutrophil/myeloid pleiotropy",
        "literature_query": '(SIGLEC9 OR "Siglec-9" OR CD329) autoimmune',
        "trial_query": "Siglec-9 autoimmune",
        "patent_query": "Siglec-9 autoimmune glycomimetic",
    },
    "PVR": {
        "axis": "PVR/CD155 ligand for TIGIT/CD96/CD226",
        "aliases": "CD155",
        "desired_direction": "bias PVR axis toward TIGIT inhibitory signaling",
        "modality": "ligand engineering/antibody concept",
        "delivery": "systemic; competing activating receptors make direction risky",
        "literature_query": '(PVR OR CD155) TIGIT autoimmune',
        "trial_query": "PVR TIGIT autoimmune",
        "patent_query": "PVR CD155 TIGIT autoimmune",
    },
    "NECTIN2": {
        "axis": "NECTIN2/CD112 TIGIT-family ligand",
        "aliases": "CD112;PVRL2",
        "desired_direction": "bias TIGIT-family signaling toward inhibition",
        "modality": "ligand engineering/antibody concept",
        "delivery": "systemic; receptor competition unresolved",
        "literature_query": '(NECTIN2 OR CD112 OR PVRL2) TIGIT autoimmune',
        "trial_query": "NECTIN2 autoimmune",
        "patent_query": "NECTIN2 CD112 autoimmune TIGIT",
    },
    "PILRA": {
        "axis": "PILRA inhibitory paired Ig-like receptor",
        "aliases": "PILR-alpha",
        "desired_direction": "agonize inhibitory receptor if disease-state coupled",
        "modality": "antibody/ligand-mimetic concept",
        "delivery": "systemic biologic; tissue delivery undeveloped",
        "literature_query": '(PILRA OR "PILR alpha" OR "PILR-alpha") autoimmune',
        "trial_query": "PILRA autoimmune",
        "patent_query": "PILRA inhibitory receptor autoimmune",
    },
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: format_value(row.get(k, "")) for k in fieldnames})


def format_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float) and not math.isfinite(value):
        return ""
    if isinstance(value, (list, dict)):
        return json.dumps(value, sort_keys=True)
    return value


def fnum(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        val = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(val):
        return None
    return val


def inum(value: Any) -> int:
    val = fnum(value)
    return int(val) if val is not None else 0


def split_semicolon(value: Any) -> set[str]:
    if not value:
        return set()
    return {part.strip() for part in str(value).split(";") if part.strip()}


def get_json(url: str, params: dict[str, Any] | None = None) -> Any:
    full_url = url
    if params:
        full_url = f"{url}?{urlencode(params)}"
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            req = Request(full_url, headers={"User-Agent": "ms-auto-research-wave19/1.0"})
            with urlopen(req, timeout=40) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001 - keep API failures in output.
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"request failed for {full_url}: {last_error}")


def safe_json(source: str, gene: str, query: str, url: str, params: dict[str, Any]) -> tuple[Any | None, str]:
    RAW.mkdir(parents=True, exist_ok=True)
    raw_path = RAW / f"{source}_{gene}.json"
    if raw_path.exists():
        try:
            return json.loads(raw_path.read_text()), ""
        except Exception:
            pass
    try:
        data = get_json(url, params)
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)
    raw_path.write_text(json.dumps(data, indent=2, sort_keys=True))
    return data, ""


def europepmc_snapshot(gene: str, query: str, preprint_only: bool = False) -> dict[str, Any]:
    full_query = f"({query}) AND SRC:PPR" if preprint_only else query
    data, error = safe_json(
        "europepmc_preprint" if preprint_only else "europepmc",
        gene,
        full_query,
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
        {"query": full_query, "format": "json", "pageSize": 3, "resultType": "lite"},
    )
    examples = []
    count = ""
    if data is not None:
        count = int(data.get("hitCount", 0))
        for item in data.get("resultList", {}).get("result", []):
            examples.append(
                {
                    "id": item.get("id", ""),
                    "source": item.get("source", ""),
                    "year": item.get("pubYear", ""),
                    "title": item.get("title", ""),
                    "doi": item.get("doi", ""),
                }
            )
    return {
        "gene": gene,
        "source": "EuropePMC_preprint" if preprint_only else "EuropePMC",
        "query": full_query,
        "hit_count": count,
        "url": f"https://europepmc.org/search?query={quote_plus(full_query)}",
        "top_examples": examples,
        "status": "ok" if not error else "failed",
        "error": error,
    }


def pubmed_snapshot(gene: str, query: str) -> dict[str, Any]:
    data, error = safe_json(
        "pubmed",
        gene,
        query,
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        {"db": "pubmed", "retmode": "json", "retmax": 3, "term": query},
    )
    count = ""
    ids: list[str] = []
    if data is not None:
        result = data.get("esearchresult", {})
        count = int(result.get("count", 0))
        ids = result.get("idlist", [])
    return {
        "gene": gene,
        "source": "PubMed",
        "query": query,
        "hit_count": count,
        "url": f"https://pubmed.ncbi.nlm.nih.gov/?term={quote_plus(query)}",
        "top_examples": [{"pmid": pmid} for pmid in ids],
        "status": "ok" if not error else "failed",
        "error": error,
    }


def clinical_trials_snapshot(gene: str, query: str) -> dict[str, Any]:
    data, error = safe_json(
        "clinicaltrials",
        gene,
        query,
        "https://clinicaltrials.gov/api/v2/studies",
        {"query.term": query, "pageSize": 5, "format": "json"},
    )
    examples = []
    count = ""
    if data is not None:
        count = int(data.get("totalCount", len(data.get("studies", []))))
        for study in data.get("studies", []):
            protocol = study.get("protocolSection", {})
            ident = protocol.get("identificationModule", {})
            status = protocol.get("statusModule", {})
            cond = protocol.get("conditionsModule", {})
            examples.append(
                {
                    "nct_id": ident.get("nctId", ""),
                    "title": ident.get("briefTitle", ""),
                    "status": status.get("overallStatus", ""),
                    "conditions": ";".join(cond.get("conditions", [])),
                }
            )
    return {
        "gene": gene,
        "source": "ClinicalTrials.gov",
        "query": query,
        "hit_count": count,
        "url": f"https://clinicaltrials.gov/search?term={quote_plus(query)}",
        "top_examples": examples,
        "status": "ok" if not error else "failed",
        "error": error,
    }


def patent_snapshot(gene: str, query: str) -> dict[str, Any]:
    return {
        "gene": gene,
        "source": "Google Patents",
        "query": query,
        "hit_count": "",
        "url": f"https://patents.google.com/?q={quote_plus(query)}",
        "top_examples": [],
        "status": "query_url_only",
        "error": "Google Patents has no unauthenticated count API used in this script",
    }


def chembl_target_snapshot(gene: str) -> dict[str, Any]:
    data, error = safe_json(
        "chembl_target",
        gene,
        gene,
        "https://www.ebi.ac.uk/chembl/api/data/target/search.json",
        {"q": gene, "limit": 25},
    )
    hits = []
    best = None
    if data is not None:
        for target in data.get("targets", []):
            gene_symbols = set()
            accessions = set()
            for component in target.get("target_components") or []:
                accession = component.get("accession")
                if accession:
                    accessions.add(accession)
                for syn in component.get("target_component_synonyms") or []:
                    if syn.get("syn_type") == "GENE_SYMBOL":
                        gene_symbols.add(syn.get("component_synonym"))
            hit = {
                "target_chembl_id": target.get("target_chembl_id", ""),
                "pref_name": target.get("pref_name", ""),
                "target_type": target.get("target_type", ""),
                "organism": target.get("organism", ""),
                "gene_symbols": ";".join(sorted(filter(None, gene_symbols))),
                "accessions": ";".join(sorted(accessions)),
            }
            hits.append(hit)
        for hit in hits:
            if (
                gene in split_semicolon(hit["gene_symbols"])
                and hit["organism"] == "Homo sapiens"
                and hit["target_type"] == "SINGLE PROTEIN"
            ):
                best = hit
                break
        if best is None:
            for hit in hits:
                if hit["organism"] == "Homo sapiens" and hit["target_type"] == "SINGLE PROTEIN":
                    best = hit
                    break

    activity_count = ""
    activity_error = ""
    activity_url = ""
    if best:
        target_id = best["target_chembl_id"]
        activity_url = (
            "https://www.ebi.ac.uk/chembl/g/#browse/activities/filter/"
            f"target_chembl_id%3A{target_id}"
        )
        data2, activity_error = safe_json(
            "chembl_activity",
            gene,
            target_id,
            "https://www.ebi.ac.uk/chembl/api/data/activity.json",
            {"target_chembl_id": target_id, "standard_units": "nM", "limit": 1, "offset": 0},
        )
        if data2 is not None:
            total = data2.get("page_meta", {}).get("total_count")
            activity_count = int(total) if total is not None else ""

    return {
        "gene": gene,
        "status": "ok" if not error else "failed",
        "error": error,
        "target_chembl_id": best.get("target_chembl_id", "") if best else "",
        "pref_name": best.get("pref_name", "") if best else "",
        "target_type": best.get("target_type", "") if best else "",
        "organism": best.get("organism", "") if best else "",
        "gene_symbols": best.get("gene_symbols", "") if best else "",
        "nM_activity_count": activity_count,
        "activity_error": activity_error,
        "target_search_url": f"https://www.ebi.ac.uk/chembl/g/#search_results/all/query={quote_plus(gene)}",
        "activity_url": activity_url,
        "n_search_hits": len(hits),
        "search_hits": hits[:8],
    }


def first_by_gene(path: Path, gene_col: str = "gene") -> dict[str, dict[str, str]]:
    return {r.get(gene_col, ""): r for r in read_tsv(path)}


def collect_local_evidence() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    broad = first_by_gene(RESULTS / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv")
    residual = first_by_gene(RESULTS / "broad_residual_gate" / "broad_residual_gate_summary.tsv")
    orchestrator = first_by_gene(
        RESULTS / "wave15_orchestrator_dependency_scan" / "candidate_dependency_priority_summary.tsv"
    )
    accessible = first_by_gene(RESULTS / "wave18_accessible_target_rescue" / "accessible_target_rescue_candidates.tsv")
    pivot = first_by_gene(RESULTS / "pivot_panel_triage" / "pivot_panel_summary.tsv")
    ms = first_by_gene(RESULTS / "gse111972_full_ms_wm_signature.tsv")

    existing_by_gene: dict[str, list[dict[str, str]]] = {}
    for row in read_tsv(RESULTS / "existing_evidence_candidate_matrix.tsv"):
        existing_by_gene.setdefault(row.get("gene", ""), []).append(row)

    residual_retained_diseases: dict[str, set[str]] = {}
    residual_retained_tests: dict[str, list[str]] = {}
    for row in read_tsv(RESULTS / "broad_residual_gate" / "broad_residual_residual_tests.tsv"):
        if row.get("retains_nominal_positive") != "True":
            continue
        gene = row.get("gene", "")
        if gene not in CANDIDATES:
            continue
        disease = row.get("disease_name", "")
        if disease:
            residual_retained_diseases.setdefault(gene, set()).add(disease)
        residual_retained_tests.setdefault(gene, []).append(
            f"{row.get('analysis', '')}|{row.get('covariate_set', '')}:"
            f"{row.get('residual_delta_case_minus_control', '')},p={row.get('residual_p', '')}"
        )

    local_rows: list[dict[str, Any]] = []
    detail_rows: list[dict[str, Any]] = []
    for gene, meta in CANDIDATES.items():
        b = broad.get(gene, {})
        r = residual.get(gene, {})
        o = orchestrator.get(gene, {})
        a = accessible.get(gene, {})
        p = pivot.get(gene, {})
        m = ms.get(gene, {})
        existing_rows = existing_by_gene.get(gene, [])
        existing_pos = [x for x in existing_rows if x.get("positive_nominal") == "True"]
        existing_neg = [x for x in existing_rows if x.get("negative_nominal") == "True"]

        recurrence_diseases = set()
        recurrence_diseases |= split_semicolon(b.get("positive_diseases", ""))
        recurrence_diseases |= split_semicolon(a.get("local_recurrence_disease_union", ""))
        recurrence_diseases |= split_semicolon(o.get("expression_supporting_diseases", ""))
        recurrence_diseases |= residual_retained_diseases.get(gene, set())
        state_diseases = set()
        state_diseases |= split_semicolon(a.get("local_state_coupled_disease_union", ""))
        state_diseases |= split_semicolon(o.get("resid_state_supporting_diseases", ""))

        row = {
            "gene": gene,
            "axis": meta["axis"],
            "aliases": meta["aliases"],
            "desired_direction": meta["desired_direction"],
            "modality": meta["modality"],
            "delivery": meta["delivery"],
            "broad_positive_disease_count": inum(b.get("positive_disease_count")),
            "broad_positive_diseases": b.get("positive_diseases", ""),
            "broad_negative_disease_count": inum(b.get("negative_disease_count")),
            "broad_negative_diseases": b.get("negative_diseases", ""),
            "broad_positive_fdr10_compartment_count": inum(b.get("positive_fdr10_compartment_count")),
            "broad_top_positive_compartments": b.get("top_positive_compartments", ""),
            "broad_discovery_priority_score": b.get("discovery_priority_score", ""),
            "ms_wm_delta_log2": b.get("ms_wm_delta_log2", m.get("mean_case", "")),
            "ms_wm_hedges_g": b.get("ms_wm_hedges_g", m.get("hedges_g", "")),
            "ms_wm_p": b.get("ms_wm_p", m.get("p", "")),
            "ms_wm_fdr": b.get("ms_wm_fdr", m.get("fdr", "")),
            "residual_gate_retained_positive_disease_count": inum(r.get("retained_positive_disease_count")),
            "residual_gate_non_ibd_retained_positive_disease_count": inum(
                r.get("non_ibd_retained_positive_disease_count")
            ),
            "residual_gate_strict_core_surviving_disease_count": inum(
                r.get("strict_core_covariate_surviving_disease_count")
            ),
            "residual_gate_top_retained_tests": r.get("top_retained_tests", ""),
            "residual_gate_retained_diseases": ";".join(sorted(residual_retained_diseases.get(gene, set()))),
            "residual_gate_retained_tests_from_detail": ";".join(residual_retained_tests.get(gene, [])[:12]),
            "residual_gate_priority_score": r.get("residual_gate_priority_score", ""),
            "orchestrator_expr_trend_diseases": inum(o.get("n_expr_trend_or_better_diseases")),
            "orchestrator_expr_negative_diseases": inum(o.get("n_expr_negative_trend_diseases")),
            "orchestrator_resid_state_support_diseases": inum(o.get("n_resid_state_support_diseases")),
            "orchestrator_expression_supporting_diseases": o.get("expression_supporting_diseases", ""),
            "orchestrator_resid_supporting_diseases": o.get("resid_state_supporting_diseases", ""),
            "wave18_call": a.get("wave18_call", ""),
            "wave18_reason": a.get("wave18_call_reason", ""),
            "wave18_local_recurrence_count": inum(a.get("local_recurrence_disease_count_union")),
            "wave18_local_state_count": inum(a.get("local_state_coupled_disease_count_union")),
            "pivot_call": p.get("decision", ""),
            "pivot_reason": p.get("decision_reason", p.get("manual_intervention_reason", "")),
            "existing_positive_rows": len(existing_pos),
            "existing_negative_rows": len(existing_neg),
            "existing_positive_diseases": ";".join(sorted({x.get("disease", "") for x in existing_pos})),
            "existing_negative_diseases": ";".join(sorted({x.get("disease", "") for x in existing_neg})),
            "local_recurrence_disease_count_union": len(recurrence_diseases),
            "local_recurrence_disease_union": ";".join(sorted(recurrence_diseases)),
            "local_state_coupled_count_union": len(state_diseases),
            "local_state_coupled_union": ";".join(sorted(state_diseases)),
        }
        local_rows.append(row)

        for source, source_row in [
            ("broad_h5ad_gene_rank", b),
            ("broad_residual_gate_summary", r),
            ("wave15_orchestrator_dependency", o),
            ("wave18_accessible_target_rescue", a),
            ("pivot_panel_triage", p),
            ("gse111972_ms_white_matter_signature", m),
        ]:
            if source_row:
                detail = {"gene": gene, "source_table": source}
                detail.update(source_row)
                detail_rows.append(detail)

    return local_rows, detail_rows


def collect_perturbation_foundation() -> list[dict[str, Any]]:
    candidates_upper = set(CANDIDATES)
    rows_by_gene: dict[str, dict[str, Any]] = {
        gene: {
            "gene": gene,
            "gse162463_gene": "",
            "gse162463_mhcii_median_low_vs_high_log2": "",
            "gse162463_mhcii_rank_required_low_vs_high": "",
            "gse162463_cd40_median_low_vs_high_log2": "",
            "gse162463_pdl1_median_low_vs_high_log2": "",
            "geneformer_sources": "",
            "geneformer_total_contexts_with_token": 0,
            "geneformer_total_disease_cells_with_token": 0,
            "geneformer_total_support_contexts": 0,
            "geneformer_total_strong_support_contexts": 0,
            "geneformer_best_mean_cosine_z": "",
            "geneformer_best_source": "",
            "wave18_foundation_call": "",
        }
        for gene in CANDIDATES
    }

    gse = read_tsv(RESULTS / "wave15_perturbation_drug_response" / "gse162463_mouse_crispr_screen_gene_summary.tsv")
    for row in gse:
        upper = row.get("gene", "").upper()
        if upper in candidates_upper:
            out = rows_by_gene[upper]
            out.update(
                {
                    "gse162463_gene": row.get("gene", ""),
                    "gse162463_mhcii_median_low_vs_high_log2": row.get("MHCII_median_low_vs_high_log2", ""),
                    "gse162463_mhcii_rank_required_low_vs_high": row.get("MHCII_rank_required_low_vs_high", ""),
                    "gse162463_cd40_median_low_vs_high_log2": row.get("CD40_median_low_vs_high_log2", ""),
                    "gse162463_pdl1_median_low_vs_high_log2": row.get("PDL1_median_low_vs_high_log2", ""),
                }
            )

    gf_files = sorted(RESULTS.glob("**/*gene_summary.tsv"))
    gf_seen: dict[str, list[dict[str, str]]] = {gene: [] for gene in CANDIDATES}
    for path in gf_files:
        if "geneformer" not in str(path):
            continue
        for row in read_tsv(path):
            upper = row.get("gene", "").upper()
            if upper in candidates_upper:
                record = dict(row)
                record["source_file"] = str(path.relative_to(ROOT))
                gf_seen[upper].append(record)
    for gene, records in gf_seen.items():
        if not records:
            continue
        out = rows_by_gene[gene]
        out["geneformer_sources"] = ";".join(sorted({r["source_file"] for r in records}))
        out["geneformer_total_contexts_with_token"] = sum(inum(r.get("contexts_with_token")) for r in records)
        out["geneformer_total_disease_cells_with_token"] = sum(inum(r.get("disease_cells_with_token")) for r in records)
        out["geneformer_total_support_contexts"] = sum(inum(r.get("support_contexts")) for r in records)
        out["geneformer_total_strong_support_contexts"] = sum(inum(r.get("strong_support_contexts")) for r in records)
        best = max((fnum(r.get("mean_cosine_z_vs_random")) or -999 for r in records), default="")
        out["geneformer_best_mean_cosine_z"] = best
        for r in records:
            if fnum(r.get("mean_cosine_z_vs_random")) == best:
                out["geneformer_best_source"] = r["source_file"]
                break

    fnd = first_by_gene(RESULTS / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv")
    for gene, row in fnd.items():
        if gene in rows_by_gene:
            rows_by_gene[gene]["wave18_foundation_call"] = row.get("rescue_call", row.get("recommendation", "present"))

    return [rows_by_gene[gene] for gene in CANDIDATES]


def collect_external() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    query_rows: list[dict[str, Any]] = []
    chembl_rows: list[dict[str, Any]] = []
    for gene, meta in CANDIDATES.items():
        query = meta["literature_query"]
        query_rows.append(europepmc_snapshot(gene, query, preprint_only=False))
        query_rows.append(pubmed_snapshot(gene, query))
        query_rows.append(europepmc_snapshot(gene, query, preprint_only=True))
        query_rows.append(clinical_trials_snapshot(gene, meta["trial_query"]))
        query_rows.append(patent_snapshot(gene, meta["patent_query"]))
        chembl_rows.append(chembl_target_snapshot(gene))
    return query_rows, chembl_rows


def index_query_counts(query_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {gene: {} for gene in CANDIDATES}
    for row in query_rows:
        gene = row["gene"]
        source = row["source"]
        key = {
            "EuropePMC": "europepmc",
            "PubMed": "pubmed",
            "EuropePMC_preprint": "preprint",
            "ClinicalTrials.gov": "clinicaltrials",
        }.get(source)
        if not key:
            continue
        out[gene][f"{key}_hit_count"] = row["hit_count"]
        out[gene][f"{key}_url"] = row["url"]
    return out


def index_chembl(chembl_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {row["gene"]: row for row in chembl_rows}


def assign_call(row: dict[str, Any]) -> tuple[str, str]:
    recurrence = inum(row.get("local_recurrence_disease_count_union"))
    state = inum(row.get("local_state_coupled_count_union"))
    broad_neg = inum(row.get("broad_negative_disease_count"))
    recurrence_names = split_semicolon(row.get("local_recurrence_disease_union", ""))
    europepmc_count = inum(row.get("europepmc_hit_count"))
    trial_count = inum(row.get("clinicaltrials_hit_count"))
    chembl_count = inum(row.get("chembl_nM_activity_count"))
    axis = row.get("axis", "")

    reasons = []
    if recurrence < 3:
        reasons.append(f"local recurrence below gate ({recurrence}<3 diseases/tissues)")
    if state < 3:
        reasons.append(f"state coupling below gate ({state}<3)")
    if broad_neg:
        reasons.append(f"directional local negatives present ({broad_neg} broad negative diseases)")
    if "TIGIT" in axis or row["gene"] in {"BTLA", "TIGIT", "PDCD1", "PVR", "NECTIN2"}:
        reasons.append("checkpoint biology is not myeloid/APC-state selective")
    if europepmc_count >= 1000 or trial_count >= 5:
        reasons.append(f"crowded prior art snapshot (EuropePMC={europepmc_count}, CT.gov={trial_count})")
    if row["gene"] in {"HAVCR2", "CD274", "CD24", "CD47", "SIRPA"}:
        reasons.append("known checkpoint/tolerance axis with non-novel autoimmune direction")
    if chembl_count >= 100:
        reasons.append(f"tractable but saturated ChEMBL small-molecule/assay footprint ({chembl_count} nM records)")

    if recurrence >= 3 and state >= 3 and broad_neg == 0 and europepmc_count < 1000 and trial_count < 5:
        return "PROMOTE", "meets local recurrence/state and prior-art gates"
    if recurrence >= 3 and not broad_neg:
        return "PARK", "; ".join(reasons) if reasons else "local recurrence but insufficient state/prior-art package"
    if len(recurrence_names) >= 2 and not broad_neg:
        return "PARK_LOW", "; ".join(reasons) if reasons else "limited two-disease support only"
    return "NO_GO", "; ".join(reasons) if reasons else "insufficient local or modality support"


def synthesize(
    local_rows: list[dict[str, Any]],
    perturb_rows: list[dict[str, Any]],
    query_rows: list[dict[str, Any]],
    chembl_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    query_idx = index_query_counts(query_rows)
    chembl_idx = index_chembl(chembl_rows)
    perturb_idx = {row["gene"]: row for row in perturb_rows}
    synthesis = []
    for row in local_rows:
        gene = row["gene"]
        out = dict(row)
        out.update(query_idx.get(gene, {}))
        ch = chembl_idx.get(gene, {})
        out.update(
            {
                "chembl_target_chembl_id": ch.get("target_chembl_id", ""),
                "chembl_pref_name": ch.get("pref_name", ""),
                "chembl_target_type": ch.get("target_type", ""),
                "chembl_nM_activity_count": ch.get("nM_activity_count", ""),
                "chembl_activity_url": ch.get("activity_url", ""),
            }
        )
        p = perturb_idx.get(gene, {})
        out.update(
            {
                "gse162463_mhcii_median_low_vs_high_log2": p.get(
                    "gse162463_mhcii_median_low_vs_high_log2", ""
                ),
                "gse162463_mhcii_rank_required_low_vs_high": p.get(
                    "gse162463_mhcii_rank_required_low_vs_high", ""
                ),
                "geneformer_total_support_contexts": p.get("geneformer_total_support_contexts", ""),
                "geneformer_total_strong_support_contexts": p.get("geneformer_total_strong_support_contexts", ""),
            }
        )
        call, reason = assign_call(out)
        out["wave19_call"] = call
        out["wave19_reason"] = reason
        synthesis.append(out)

    def sort_key(row: dict[str, Any]) -> tuple[int, int, int, int, str]:
        call_rank = {"PROMOTE": 0, "PARK": 1, "PARK_LOW": 2, "NO_GO": 3}.get(row["wave19_call"], 4)
        return (
            call_rank,
            -inum(row.get("local_recurrence_disease_count_union")),
            -inum(row.get("local_state_coupled_count_union")),
            inum(row.get("broad_negative_disease_count")),
            row["gene"],
        )

    return sorted(synthesis, key=sort_key)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    local_rows, local_detail = collect_local_evidence()
    perturb_rows = collect_perturbation_foundation()
    query_rows, chembl_rows = collect_external()
    synthesis = synthesize(local_rows, perturb_rows, query_rows, chembl_rows)

    local_fields = [
        "gene",
        "axis",
        "aliases",
        "desired_direction",
        "modality",
        "delivery",
        "broad_positive_disease_count",
        "broad_positive_diseases",
        "broad_negative_disease_count",
        "broad_negative_diseases",
        "broad_positive_fdr10_compartment_count",
        "broad_top_positive_compartments",
        "ms_wm_delta_log2",
        "ms_wm_hedges_g",
        "ms_wm_p",
        "ms_wm_fdr",
        "residual_gate_retained_positive_disease_count",
        "residual_gate_non_ibd_retained_positive_disease_count",
        "residual_gate_strict_core_surviving_disease_count",
        "residual_gate_retained_diseases",
        "residual_gate_top_retained_tests",
        "residual_gate_retained_tests_from_detail",
        "orchestrator_expr_trend_diseases",
        "orchestrator_expr_negative_diseases",
        "orchestrator_resid_state_support_diseases",
        "orchestrator_expression_supporting_diseases",
        "orchestrator_resid_supporting_diseases",
        "wave18_call",
        "wave18_reason",
        "existing_positive_rows",
        "existing_negative_rows",
        "local_recurrence_disease_count_union",
        "local_recurrence_disease_union",
        "local_state_coupled_count_union",
        "local_state_coupled_union",
    ]
    perturb_fields = [
        "gene",
        "gse162463_gene",
        "gse162463_mhcii_median_low_vs_high_log2",
        "gse162463_mhcii_rank_required_low_vs_high",
        "gse162463_cd40_median_low_vs_high_log2",
        "gse162463_pdl1_median_low_vs_high_log2",
        "geneformer_sources",
        "geneformer_total_contexts_with_token",
        "geneformer_total_disease_cells_with_token",
        "geneformer_total_support_contexts",
        "geneformer_total_strong_support_contexts",
        "geneformer_best_mean_cosine_z",
        "geneformer_best_source",
        "wave18_foundation_call",
    ]
    query_fields = [
        "gene",
        "source",
        "query",
        "hit_count",
        "url",
        "top_examples",
        "status",
        "error",
    ]
    chembl_fields = [
        "gene",
        "status",
        "error",
        "target_chembl_id",
        "pref_name",
        "target_type",
        "organism",
        "gene_symbols",
        "nM_activity_count",
        "activity_error",
        "target_search_url",
        "activity_url",
        "n_search_hits",
        "search_hits",
    ]
    synthesis_fields = [
        "gene",
        "wave19_call",
        "wave19_reason",
        "axis",
        "aliases",
        "desired_direction",
        "modality",
        "delivery",
        "local_recurrence_disease_count_union",
        "local_recurrence_disease_union",
        "local_state_coupled_count_union",
        "local_state_coupled_union",
        "broad_positive_disease_count",
        "broad_positive_diseases",
        "broad_negative_disease_count",
        "broad_negative_diseases",
        "residual_gate_retained_positive_disease_count",
        "residual_gate_retained_diseases",
        "orchestrator_resid_state_support_diseases",
        "ms_wm_delta_log2",
        "ms_wm_p",
        "gse162463_mhcii_median_low_vs_high_log2",
        "gse162463_mhcii_rank_required_low_vs_high",
        "geneformer_total_support_contexts",
        "geneformer_total_strong_support_contexts",
        "europepmc_hit_count",
        "pubmed_hit_count",
        "preprint_hit_count",
        "clinicaltrials_hit_count",
        "chembl_target_chembl_id",
        "chembl_pref_name",
        "chembl_nM_activity_count",
        "europepmc_url",
        "pubmed_url",
        "preprint_url",
        "clinicaltrials_url",
        "chembl_activity_url",
    ]

    write_tsv(OUT / "local_checkpoint_evidence.tsv", local_rows, local_fields)
    write_tsv(OUT / "local_checkpoint_evidence_detail.tsv", local_detail, sorted({k for r in local_detail for k in r}))
    write_tsv(OUT / "perturbation_foundation_checkpoint_evidence.tsv", perturb_rows, perturb_fields)
    write_tsv(OUT / "external_prior_art_query_log.tsv", query_rows, query_fields)
    write_tsv(OUT / "chembl_checkpoint_target_snapshot.tsv", chembl_rows, chembl_fields)
    write_tsv(OUT / "checkpoint_candidate_synthesis.tsv", synthesis, synthesis_fields)

    summary = {
        "candidate_count": len(CANDIDATES),
        "call_counts": {call: sum(1 for r in synthesis if r["wave19_call"] == call) for call in ["PROMOTE", "PARK", "PARK_LOW", "NO_GO"]},
        "promoted": [r["gene"] for r in synthesis if r["wave19_call"] == "PROMOTE"],
        "parked": [r["gene"] for r in synthesis if r["wave19_call"] == "PARK"],
        "script": "scripts/v3_wave19_tolerogenic_checkpoint.py",
        "outputs": [
            "results_v3/wave19_tolerogenic_checkpoint/local_checkpoint_evidence.tsv",
            "results_v3/wave19_tolerogenic_checkpoint/local_checkpoint_evidence_detail.tsv",
            "results_v3/wave19_tolerogenic_checkpoint/perturbation_foundation_checkpoint_evidence.tsv",
            "results_v3/wave19_tolerogenic_checkpoint/external_prior_art_query_log.tsv",
            "results_v3/wave19_tolerogenic_checkpoint/chembl_checkpoint_target_snapshot.tsv",
            "results_v3/wave19_tolerogenic_checkpoint/checkpoint_candidate_synthesis.tsv",
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
