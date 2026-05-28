#!/usr/bin/env python3
"""Wave18 accessible/druggable target rescue screen.

The screen is intentionally conservative. It starts from local V3 recurrence
and dependency tables, then adds a lightweight public-source snapshot for
druggability/prior-art triage. Public API failures are recorded rather than
treated as zero evidence.
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
OUT = RESULTS / "wave18_accessible_target_rescue"
RAW = OUT / "raw"

AUTOIMMUNE_CLAUSE = (
    '"multiple sclerosis" OR "rheumatoid arthritis" OR lupus OR Crohn OR '
    '"ulcerative colitis" OR psoriasis OR Sjogren OR "type 1 diabetes" OR '
    'celiac OR "autoimmune thyroid" OR "primary biliary cholangitis" OR autoimmune'
)

BLOCKED = {
    "CTSH": "NO_GO prior Wave16 chemistry/selectivity",
    "CTSS": "NO_GO direct autoimmune CTSS trial/prior-art crowding",
    "CD74": "NO_GO CD74/MIF crowded and state-definition marker",
    "MIF": "NO_GO CD74/MIF crowded/directional",
    "LGALS9": "NO_GO prior Wave15/Wave16 crowded and directionally complex",
    "LAPTM5": "PARK prior Wave17 modality poor",
    "CDK8": "PARK mediator kinase route parked",
    "CDK19": "PARK mediator kinase route parked",
}

CANDIDATES: dict[str, dict[str, Any]] = {
    "CD44": {
        "class": "hyaluronan/SPP1 glycan-adhesion receptor",
        "accessibility": "membrane_receptor",
        "modality": "antibody/ligand blockade; hyaluronan or SPP1-axis modulation",
        "direction": "blockade might reduce retention/migration; could also impair repair and leukocyte trafficking",
        "query": '"CD44" autoimmune',
        "trial_term": "CD44 autoimmune",
        "patent_query": "CD44 antibody autoimmune disease hyaluronan",
    },
    "CD274": {
        "class": "PD-L1 immune checkpoint",
        "accessibility": "membrane_ligand",
        "modality": "checkpoint agonism/PD-L1-Fc or PD-1 pathway engagement",
        "direction": "agonism/tolerizing direction, not oncology-style blockade",
        "query": '("PD-L1" OR CD274) autoimmune',
        "trial_term": "PD-L1 autoimmune",
        "patent_query": "PD-L1 agonist autoimmune disease CD274",
    },
    "CD24": {
        "class": "CD24-SIGLEC10 DAMP/glycan checkpoint",
        "accessibility": "membrane_glycoprotein",
        "modality": "CD24Fc/Siglec-10 checkpoint agonism or CD24-directed biologic",
        "direction": "agonize inhibitory DAMP checkpoint; local state link must be proven",
        "query": '("CD24" OR "CD24Fc") autoimmune',
        "trial_term": "CD24Fc autoimmune",
        "patent_query": "CD24Fc autoimmune disease Siglec-10",
    },
    "CD47": {
        "class": "CD47-SIRPA phagocytosis checkpoint",
        "accessibility": "membrane_ligand",
        "modality": "CD47/SIRPA antibody or engineered agonist/antagonist",
        "direction": "blockade increases phagocytosis and may be wrong for repair-preserving APC state",
        "query": '("CD47" OR SIRPA) autoimmune',
        "trial_term": "CD47 autoimmune",
        "patent_query": "CD47 SIRPA autoimmune disease",
    },
    "SIRPA": {
        "class": "CD47-SIRPA phagocytosis checkpoint receptor",
        "accessibility": "membrane_receptor",
        "modality": "SIRPA antibody/fusion proteins",
        "direction": "blockade increases phagocytosis; agonism would need repair-preserving proof",
        "query": '("SIRPA" OR "SIRP alpha") autoimmune',
        "trial_term": "SIRPA autoimmune",
        "patent_query": "SIRPA autoimmune disease antibody",
    },
    "LILRB1": {
        "class": "inhibitory myeloid/HLA receptor",
        "accessibility": "membrane_receptor",
        "modality": "antibody modulation",
        "direction": "agonism may suppress APC activation; oncology antagonist precedent cuts opposite direction",
        "query": '("LILRB1" OR ILT2) autoimmune',
        "trial_term": "LILRB1 autoimmune",
        "patent_query": "LILRB1 ILT2 autoimmune antibody",
    },
    "LILRB2": {
        "class": "inhibitory myeloid/HLA receptor",
        "accessibility": "membrane_receptor",
        "modality": "antibody modulation",
        "direction": "agonism may suppress myeloid activation; needs disease-direction proof",
        "query": '("LILRB2" OR ILT4) autoimmune',
        "trial_term": "LILRB2 autoimmune",
        "patent_query": "LILRB2 ILT4 autoimmune antibody",
    },
    "CHI3L1": {
        "class": "secreted chitinase-like inflammatory glycoprotein",
        "accessibility": "secreted_protein",
        "modality": "neutralizing antibody or ligand/receptor-axis modulation",
        "direction": "inhibition might reduce inflammatory tissue remodeling; biomarker role dominates",
        "query": '("CHI3L1" OR "YKL-40") autoimmune',
        "trial_term": "CHI3L1 autoimmune",
        "patent_query": "CHI3L1 YKL-40 antibody autoimmune disease",
    },
    "GPNMB": {
        "class": "surface/secreted lipid-loader repair-state glycoprotein",
        "accessibility": "membrane_secreted",
        "modality": "antibody/ADC precedent; non-cytotoxic agonist or delivery handle would be needed",
        "direction": "do not deplete unless pathogenic subset proven; likely marker/delivery handle",
        "query": '("GPNMB" OR osteoactivin) autoimmune',
        "trial_term": "GPNMB autoimmune",
        "patent_query": "GPNMB autoimmune antibody osteoactivin",
    },
    "SPP1": {
        "class": "secreted osteopontin/CD44-integrin axis",
        "accessibility": "secreted_ligand",
        "modality": "neutralizing antibody/aptamer or receptor-axis blockade",
        "direction": "blockade may reduce inflammatory retention but repair/fibrosis direction is context-dependent",
        "query": '("SPP1" OR osteopontin) autoimmune',
        "trial_term": "osteopontin autoimmune",
        "patent_query": "osteopontin SPP1 autoimmune antibody",
    },
    "TREM1": {
        "class": "amplifying myeloid receptor",
        "accessibility": "membrane_receptor",
        "modality": "inhibitory peptide/antibody; nangibotide-like route",
        "direction": "inhibit acute myeloid amplification; chronic autoimmune state breadth is weak",
        "query": '("TREM1" OR "TREM-1") autoimmune',
        "trial_term": "TREM1 autoimmune",
        "patent_query": "TREM1 inhibitor autoimmune inflammatory bowel disease",
    },
    "TREM2": {
        "class": "lipid/efferocytosis myeloid receptor",
        "accessibility": "membrane_receptor",
        "modality": "agonistic antibody in principle; CNS delivery difficult",
        "direction": "agonism/repair-preserving activation more plausible than blockade",
        "query": '("TREM2" OR "TREM-2") autoimmune',
        "trial_term": "TREM2 autoimmune",
        "patent_query": "TREM2 agonist autoimmune multiple sclerosis",
    },
    "TYROBP": {
        "class": "TREM/DAP12 adaptor",
        "accessibility": "intracellular_adaptor",
        "modality": "poor direct modality; pathway readout",
        "direction": "direction follows receptor context; not directly accessible",
        "query": '("TYROBP" OR DAP12) autoimmune',
        "trial_term": "TYROBP autoimmune",
        "patent_query": "TYROBP DAP12 autoimmune",
    },
    "ITGAM": {
        "class": "CD11b/complement receptor 3 integrin",
        "accessibility": "membrane_receptor",
        "modality": "integrin antibody/allosteric modulation",
        "direction": "activate/restore phagocytic regulation in SLE genetics; broad blockade unsafe",
        "query": '("ITGAM" OR CD11b OR "complement receptor 3") autoimmune',
        "trial_term": "ITGAM autoimmune",
        "patent_query": "ITGAM CD11b autoimmune integrin",
    },
    "ITGAX": {
        "class": "CD11c integrin/APC receptor",
        "accessibility": "membrane_receptor",
        "modality": "antibody or cell-targeting marker; direct chronic modulation unattractive",
        "direction": "likely APC marker/depletion handle, not state-specific rescue",
        "query": '("ITGAX" OR CD11c) autoimmune',
        "trial_term": "ITGAX autoimmune",
        "patent_query": "ITGAX CD11c autoimmune antibody",
    },
    "FCGR2A": {
        "class": "Fc-gamma receptor uptake receptor",
        "accessibility": "membrane_receptor",
        "modality": "Fc engineering, blocking/agonist antibodies",
        "direction": "direction depends on immune-complex disease context",
        "query": '("FCGR2A" OR "Fc gamma receptor IIA") autoimmune',
        "trial_term": "FCGR2A autoimmune",
        "patent_query": "FCGR2A autoimmune Fc receptor antibody",
    },
    "FCGR3A": {
        "class": "Fc-gamma receptor uptake receptor",
        "accessibility": "membrane_receptor",
        "modality": "Fc engineering, blocking/agonist antibodies",
        "direction": "direction depends on immune-complex disease context",
        "query": '("FCGR3A" OR CD16A) autoimmune',
        "trial_term": "FCGR3A autoimmune",
        "patent_query": "FCGR3A CD16A autoimmune Fc receptor",
    },
    "C1QA": {
        "class": "classical complement ligand",
        "accessibility": "secreted_complement",
        "modality": "anti-C1q/classical-complement inhibition",
        "direction": "inhibit only in biomarker-defined classical-complement injury; C1q also protective",
        "query": '("C1QA" OR C1q) autoimmune',
        "trial_term": "C1q autoimmune",
        "patent_query": "anti-C1q autoimmune lupus nephritis",
    },
    "C1QB": {
        "class": "classical complement ligand",
        "accessibility": "secreted_complement",
        "modality": "anti-C1q/classical-complement inhibition",
        "direction": "same as C1QA; double-edged clearance biology",
        "query": '("C1QB" OR C1q) autoimmune',
        "trial_term": "C1q autoimmune",
        "patent_query": "anti-C1q autoimmune lupus nephritis",
    },
    "MSR1": {
        "class": "scavenger receptor A/CD204",
        "accessibility": "membrane_receptor",
        "modality": "antibody/ligand modulation; delivery handle",
        "direction": "blocking may impair debris/lipid clearance; agonism unclear",
        "query": '("MSR1" OR "scavenger receptor A" OR CD204) autoimmune',
        "trial_term": "MSR1 autoimmune",
        "patent_query": "MSR1 CD204 autoimmune antibody",
    },
    "MERTK": {
        "class": "TAM efferocytosis receptor",
        "accessibility": "membrane_receptor_tyrosine_kinase",
        "modality": "small-molecule inhibitor exists; autoimmune direction likely agonism/repair",
        "direction": "agonize repair/efferocytosis if anything; inhibition likely wrong",
        "query": '("MERTK" OR MerTK) autoimmune',
        "trial_term": "MERTK autoimmune",
        "patent_query": "MERTK autoimmune agonist efferocytosis",
    },
    "AXL": {
        "class": "TAM efferocytosis receptor",
        "accessibility": "membrane_receptor_tyrosine_kinase",
        "modality": "small-molecule/antibody inhibitor exists; autoimmune direction ambiguous",
        "direction": "inhibition is oncology-oriented and may impair resolution; agonism immature",
        "query": '("AXL" OR "AXL receptor") autoimmune',
        "trial_term": "AXL autoimmune",
        "patent_query": "AXL autoimmune efferocytosis",
    },
    "LGALS3": {
        "class": "galectin-3 glycan checkpoint",
        "accessibility": "secreted_intracellular_lectin",
        "modality": "galectin-3 inhibitors/biologics",
        "direction": "inhibition could reduce inflammation/fibrosis but may impair repair/remyelination",
        "query": '("LGALS3" OR "galectin-3") autoimmune',
        "trial_term": "galectin-3 inhibitor autoimmune",
        "patent_query": "galectin-3 inhibitor autoimmune disease",
    },
    "LGALS9": {
        "class": "galectin-9 glycan checkpoint",
        "accessibility": "secreted_lectin",
        "modality": "recombinant Gal-9/antibody modulation",
        "direction": "tolerance-promoting versus inflammatory effects are context-dependent",
        "query": '("LGALS9" OR "galectin-9") autoimmune',
        "trial_term": "galectin-9 autoimmune",
        "patent_query": "galectin-9 autoimmune disease",
    },
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def fnum(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        val = float(value)
    except ValueError:
        return None
    if not math.isfinite(val):
        return None
    return val


def inum(value: str | None) -> int:
    val = fnum(value)
    if val is None:
        return 0
    return int(val)


def split_semicolon(value: str | None) -> set[str]:
    if not value:
        return set()
    return {part.strip() for part in value.split(";") if part.strip()}


def get_json(url: str, params: dict[str, Any] | None = None, payload: dict[str, Any] | None = None) -> Any:
    full_url = url
    data = None
    headers = {"User-Agent": "ms-auto-research-wave18/1.0"}
    if params:
        full_url = f"{url}?{urlencode(params)}"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            req = Request(full_url, data=data, headers=headers)
            with urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"request failed for {full_url}: {last_error}")


def europepmc_count(query: str) -> dict[str, Any]:
    params = {"query": query, "format": "json", "pageSize": 3, "resultType": "lite"}
    data = get_json("https://www.ebi.ac.uk/europepmc/webservices/rest/search", params=params)
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
        "hit_count": int(data.get("hitCount", 0)),
        "url": f"https://europepmc.org/search?query={quote_plus(query)}",
        "examples": examples,
    }


def clinical_trials(term: str) -> dict[str, Any]:
    params = {"query.term": term, "pageSize": 10, "format": "json"}
    data = get_json("https://clinicaltrials.gov/api/v2/studies", params=params)
    studies = data.get("studies", [])
    parsed = []
    for st in studies:
        protocol = st.get("protocolSection", {})
        ident = protocol.get("identificationModule", {})
        status = protocol.get("statusModule", {})
        design = protocol.get("designModule", {})
        cond = protocol.get("conditionsModule", {})
        interventions = protocol.get("armsInterventionsModule", {}).get("interventions", [])
        parsed.append(
            {
                "nct_id": ident.get("nctId"),
                "title": ident.get("briefTitle"),
                "status": status.get("overallStatus"),
                "phase": ";".join(design.get("phases", [])),
                "conditions": ";".join(cond.get("conditions", [])),
                "interventions": ";".join(i.get("name", "") for i in interventions),
            }
        )
    return {
        "hit_count": int(data.get("totalCount", len(studies))),
        "returned_count": len(studies),
        "url": f"https://clinicaltrials.gov/search?term={quote_plus(term)}",
        "studies": parsed,
    }


def chembl_target_search(gene: str) -> dict[str, Any]:
    data = get_json("https://www.ebi.ac.uk/chembl/api/data/target/search.json", params={"q": gene, "limit": 20})
    hits = []
    for target in data.get("targets", []):
        components = target.get("target_components") or []
        accessions = []
        gene_names = []
        for comp in components:
            accession = comp.get("accession")
            if accession:
                accessions.append(accession)
            for synonym in comp.get("target_component_synonyms") or []:
                if synonym.get("syn_type") == "GENE_SYMBOL":
                    gene_names.append(synonym.get("component_synonym"))
        hits.append(
            {
                "target_chembl_id": target.get("target_chembl_id"),
                "pref_name": target.get("pref_name"),
                "target_type": target.get("target_type"),
                "organism": target.get("organism"),
                "accessions": ";".join(sorted(set(filter(None, accessions)))),
                "gene_symbols": ";".join(sorted(set(filter(None, gene_names)))),
            }
        )
    best = None
    for hit in hits:
        symbols = set(hit["gene_symbols"].split(";")) if hit["gene_symbols"] else set()
        if gene in symbols and hit["organism"] == "Homo sapiens" and hit["target_type"] == "SINGLE PROTEIN":
            best = hit
            break
    if best is None:
        for hit in hits:
            if hit["organism"] == "Homo sapiens" and hit["target_type"] == "SINGLE PROTEIN":
                best = hit
                break
    return {
        "best": best,
        "hits": hits,
        "url": f"https://www.ebi.ac.uk/chembl/g/#search_results/all/query={quote_plus(gene)}",
    }


def chembl_activity_count(target_chembl_id: str | None) -> dict[str, Any]:
    if not target_chembl_id:
        return {"activity_records": None, "activity_values_nM_count": None, "url": ""}
    params = {
        "target_chembl_id": target_chembl_id,
        "standard_units": "nM",
        "limit": 1,
        "offset": 0,
    }
    data = get_json("https://www.ebi.ac.uk/chembl/api/data/activity.json", params=params)
    total = data.get("page_meta", {}).get("total_count")
    return {
        "activity_records": int(total) if total is not None else None,
        "activity_values_nM_count": int(total) if total is not None else None,
        "url": (
            "https://www.ebi.ac.uk/chembl/g/#browse/activities/filter/"
            f"target_chembl_id%3A{target_chembl_id}"
        ),
    }


def collect_local_metrics() -> dict[str, dict[str, Any]]:
    metrics: dict[str, dict[str, Any]] = {gene: {"gene": gene} for gene in CANDIDATES}

    broad = {r["gene"]: r for r in read_tsv(RESULTS / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv")}
    cross_summary = {r["gene"]: r for r in read_tsv(RESULTS / "cross_disease_gene_summary.tsv")}
    surface = {r["gene"]: r for r in read_tsv(RESULTS / "wave15_surface_trafficking_dependency" / "candidate_ranked.tsv")}
    orchestrator = {
        r["gene"]: r
        for r in read_tsv(RESULTS / "wave15_orchestrator_dependency_scan" / "candidate_dependency_priority_summary.tsv")
    }
    disease_axis = {r["gene"]: r for r in read_tsv(RESULTS / "disease_axis_candidate_gene_rank.tsv")}

    existing_rows = read_tsv(RESULTS / "existing_evidence_candidate_matrix.tsv")
    existing_by_gene: dict[str, list[dict[str, str]]] = {}
    for row in existing_rows:
        existing_by_gene.setdefault(row.get("gene", ""), []).append(row)

    ot_rows = read_tsv(RESULTS / "opentargets_candidate_disease_hits.tsv")
    ot_by_gene: dict[str, list[dict[str, str]]] = {}
    for row in ot_rows:
        ot_by_gene.setdefault(row.get("target", ""), []).append(row)

    for gene, meta in CANDIDATES.items():
        row = metrics[gene]
        row.update(meta)
        b = broad.get(gene, {})
        row.update(
            {
                "broad_positive_disease_count": inum(b.get("positive_disease_count")),
                "broad_negative_disease_count": inum(b.get("negative_disease_count")),
                "broad_positive_diseases": b.get("positive_diseases", ""),
                "broad_negative_diseases": b.get("negative_diseases", ""),
                "broad_ms_wm_delta_log2": b.get("ms_wm_delta_log2", ""),
                "broad_ms_wm_p": b.get("ms_wm_p", ""),
                "broad_discovery_priority_score": b.get("discovery_priority_score", ""),
            }
        )

        cs = cross_summary.get(gene, {})
        row.update(
            {
                "cross_trend_or_better_diseases": inum(cs.get("n_trend_or_better_diseases")),
                "cross_negative_trend_diseases": inum(cs.get("n_negative_trend_diseases")),
                "cross_supporting_diseases": cs.get("supporting_diseases", ""),
                "cross_median_positive_hedges_g": cs.get("median_positive_hedges_g", ""),
            }
        )

        s = surface.get(gene, {})
        row.update(
            {
                "surface_family": s.get("family", ""),
                "surface_delta_trend_diseases": inum(s.get("n_delta_trend_or_better_diseases")),
                "surface_delta_fdr10_diseases": inum(s.get("n_delta_fdr10_positive_diseases")),
                "surface_negative_delta_diseases": inum(s.get("n_delta_negative_trend_diseases")),
                "surface_resid_state_diseases": inum(s.get("n_state_resid_non_ifn_r_ge_0_35_diseases")),
                "surface_raw_state_diseases": inum(s.get("n_state_raw_r_ge_0_5_diseases")),
                "surface_confounder_dominant_diseases": inum(s.get("n_confounder_dominant_diseases")),
                "surface_rank_score": s.get("rank_score", ""),
                "surface_local_call": s.get("go_no_go", ""),
                "surface_delta_supporting_diseases": s.get("delta_supporting_diseases", ""),
                "surface_resid_supporting_diseases": s.get("resid_non_ifn_supporting_diseases", ""),
                "surface_reason": s.get("demotion_or_support_reason", ""),
            }
        )

        o = orchestrator.get(gene, {})
        row.update(
            {
                "orchestrator_class": o.get("candidate_class", ""),
                "orchestrator_expr_trend_diseases": inum(o.get("n_expr_trend_or_better_diseases")),
                "orchestrator_expr_negative_diseases": inum(o.get("n_expr_negative_trend_diseases")),
                "orchestrator_resid_state_diseases": inum(o.get("n_resid_state_support_diseases")),
                "orchestrator_raw_state_diseases": inum(o.get("n_raw_state_support_diseases")),
                "orchestrator_priority_score": o.get("priority_score", ""),
                "orchestrator_expression_supporting_diseases": o.get("expression_supporting_diseases", ""),
                "orchestrator_resid_supporting_diseases": o.get("resid_state_supporting_diseases", ""),
            }
        )

        da = disease_axis.get(gene, {})
        row.update(
            {
                "axis_mentions": da.get("axes", ""),
                "axis_mentioned_disease_count": inum(da.get("mentioned_disease_count")),
                "axis_mentioned_diseases": da.get("mentioned_diseases", ""),
                "axis_priority_score": da.get("priority_score", ""),
            }
        )

        ex = existing_by_gene.get(gene, [])
        pos = [r for r in ex if r.get("positive_nominal") == "True"]
        neg = [r for r in ex if r.get("negative_nominal") == "True"]
        row.update(
            {
                "existing_positive_rows": len(pos),
                "existing_negative_rows": len(neg),
                "existing_positive_diseases": ";".join(sorted({r.get("disease", "") for r in pos if r.get("disease")})),
                "existing_negative_diseases": ";".join(sorted({r.get("disease", "") for r in neg if r.get("disease")})),
            }
        )

        ot = ot_by_gene.get(gene, [])
        row.update(
            {
                "local_opentargets_disease_rows": len(ot),
                "local_opentargets_diseases": ";".join(sorted({r.get("disease", "") for r in ot if r.get("disease")})),
                "local_opentargets_max_overall": (
                    max((fnum(r.get("overall_score")) or 0 for r in ot), default=0)
                ),
                "local_opentargets_max_genetic_association": (
                    max((fnum(r.get("datatype_genetic_association")) or 0 for r in ot), default=0)
                ),
            }
        )

        recurrent_diseases = set()
        recurrent_diseases |= split_semicolon(row["broad_positive_diseases"])
        recurrent_diseases |= split_semicolon(row["cross_supporting_diseases"])
        recurrent_diseases |= split_semicolon(row["surface_delta_supporting_diseases"])
        recurrent_diseases |= split_semicolon(row["orchestrator_expression_supporting_diseases"])
        state_diseases = split_semicolon(row["surface_resid_supporting_diseases"]) | split_semicolon(
            row["orchestrator_resid_supporting_diseases"]
        )
        row["local_recurrence_disease_count_union"] = len(recurrent_diseases)
        row["local_recurrence_disease_union"] = ";".join(sorted(recurrent_diseases))
        row["local_state_coupled_disease_count_union"] = len(state_diseases)
        row["local_state_coupled_disease_union"] = ";".join(sorted(state_diseases))

    return metrics


def score_and_call(row: dict[str, Any]) -> None:
    gene = row["gene"]
    if gene in BLOCKED:
        row["blocked_status_note"] = BLOCKED[gene]
    else:
        row["blocked_status_note"] = ""

    recurrence = int(row["local_recurrence_disease_count_union"])
    state = int(row["local_state_coupled_disease_count_union"])
    broad_pos = int(row["broad_positive_disease_count"])
    broad_neg = int(row["broad_negative_disease_count"])
    surface_conf = int(row["surface_confounder_dominant_diseases"])
    surface_neg = int(row["surface_negative_delta_diseases"])
    orch_neg = int(row["orchestrator_expr_negative_diseases"])
    ot_rows = int(row["local_opentargets_disease_rows"])
    chembl_records = row.get("chembl_activity_records")
    chembl_count = int(chembl_records) if isinstance(chembl_records, int) else 0
    epmc_count = int(row.get("europepmc_hit_count") or 0)
    trial_count = int(row.get("clinical_trials_hit_count") or 0)

    local_score = (
        recurrence * 1.5
        + state * 1.2
        + int(row["surface_delta_fdr10_diseases"]) * 1.2
        + int(row["orchestrator_resid_state_diseases"]) * 0.5
        + ot_rows * 0.25
        - broad_neg * 1.5
        - surface_neg * 1.5
        - orch_neg
        - max(0, surface_conf - 3) * 0.6
    )
    drug_score = 0
    if row["accessibility"].startswith(("membrane", "secreted")) or "secreted" in row["accessibility"]:
        drug_score += 2
    if "receptor_tyrosine_kinase" in row["accessibility"] or chembl_count >= 100:
        drug_score += 1
    if "intracellular" in row["accessibility"]:
        drug_score -= 2

    saturation_penalty = 0
    if epmc_count >= 5000:
        saturation_penalty += 3
    elif epmc_count >= 1000:
        saturation_penalty += 2
    elif epmc_count >= 250:
        saturation_penalty += 1
    if trial_count >= 20:
        saturation_penalty += 2
    elif trial_count >= 5:
        saturation_penalty += 1
    if gene in {"LGALS3", "LGALS9", "C1QA", "C1QB", "FCGR2A", "FCGR3A", "CD47", "CD274", "ITGAM", "SPP1"}:
        saturation_penalty += 1

    direction_penalty = 0
    if any(term in row["direction"] for term in ["ambiguous", "context-dependent", "wrong", "impair", "double-edged"]):
        direction_penalty += 1
    if gene in {"GPNMB", "TREM2", "MERTK", "AXL", "C1QA", "C1QB", "CD47", "SPP1", "LGALS3", "LGALS9"}:
        direction_penalty += 1

    rescue_score = local_score + drug_score - saturation_penalty - direction_penalty
    row["local_evidence_score"] = round(local_score, 3)
    row["druggability_access_score"] = drug_score
    row["prior_art_saturation_penalty"] = saturation_penalty
    row["direction_penalty"] = direction_penalty
    row["wave18_rescue_score"] = round(rescue_score, 3)

    reasons = []
    if recurrence < 4:
        reasons.append(f"local recurrence below promotion threshold ({recurrence}<4 disease union)")
    if state < 4:
        reasons.append(f"state-coupled support below threshold ({state}<4 disease union)")
    if broad_neg or surface_neg or orch_neg:
        reasons.append(f"directional contradictions/negative trends present (broad={broad_neg}, surface={surface_neg}, orchestrator={orch_neg})")
    if surface_conf >= 5:
        reasons.append(f"confounder/myeloid dominance high in surface screen ({surface_conf} diseases)")
    if saturation_penalty >= 3:
        reasons.append(f"prior-art saturation high (EuropePMC={epmc_count}, ClinicalTrials={trial_count})")
    if direction_penalty >= 2:
        reasons.append("intervention direction is repair/checkpoint-context dependent")
    if gene in BLOCKED:
        reasons.append(BLOCKED[gene])

    if gene in BLOCKED or rescue_score < 4 or recurrence < 2:
        call = "NO_GO"
    elif recurrence >= 4 and state >= 4 and saturation_penalty <= 2 and direction_penalty <= 1 and rescue_score >= 9:
        call = "GO"
    else:
        call = "PARK"

    # Manual conservative override for state-linked but saturated/crowded axes.
    if gene in {"CD44", "CD274", "CHI3L1", "GPNMB"} and call == "NO_GO" and recurrence >= 3:
        call = "PARK"
    if gene in {"LGALS9", "LGALS3", "C1QA", "C1QB", "FCGR2A", "FCGR3A"}:
        call = "NO_GO"

    row["wave18_call"] = call
    row["wave18_call_reason"] = "; ".join(reasons) if reasons else "passes quantitative screen; requires human perturbation validation"


def add_external(metrics: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for gene, row in metrics.items():
        query = row["query"]
        clinical_term = row["trial_term"]
        patent_query = row["patent_query"]

        try:
            epmc = europepmc_count(query)
            row["europepmc_hit_count"] = epmc["hit_count"]
            row["europepmc_url"] = epmc["url"]
            sources.append(
                {
                    "gene": gene,
                    "source": "EuropePMC",
                    "query": query,
                    "hit_count": epmc["hit_count"],
                    "url": epmc["url"],
                    "notes": json.dumps(epmc["examples"], sort_keys=True),
                }
            )
        except Exception as exc:
            row["europepmc_hit_count"] = ""
            row["europepmc_url"] = ""
            sources.append({"gene": gene, "source": "EuropePMC", "query": query, "hit_count": "", "url": "", "notes": f"ERROR: {exc}"})

        try:
            trials = clinical_trials(clinical_term)
            row["clinical_trials_hit_count"] = trials["hit_count"]
            row["clinical_trials_returned_count"] = trials["returned_count"]
            row["clinical_trials_url"] = trials["url"]
            sources.append(
                {
                    "gene": gene,
                    "source": "ClinicalTrials.gov",
                    "query": clinical_term,
                    "hit_count": trials["hit_count"],
                    "url": trials["url"],
                    "notes": json.dumps(trials["studies"], sort_keys=True),
                }
            )
        except Exception as exc:
            row["clinical_trials_hit_count"] = ""
            row["clinical_trials_returned_count"] = ""
            row["clinical_trials_url"] = ""
            sources.append(
                {
                    "gene": gene,
                    "source": "ClinicalTrials.gov",
                    "query": clinical_term,
                    "hit_count": "",
                    "url": "",
                    "notes": f"ERROR: {exc}",
                }
            )

        try:
            chembl = chembl_target_search(gene)
            best = chembl["best"] or {}
            activity = chembl_activity_count(best.get("target_chembl_id"))
            row["chembl_target_chembl_id"] = best.get("target_chembl_id", "")
            row["chembl_target_pref_name"] = best.get("pref_name", "")
            row["chembl_target_type"] = best.get("target_type", "")
            row["chembl_activity_records"] = activity["activity_records"] if activity["activity_records"] is not None else ""
            row["chembl_url"] = activity["url"] or chembl["url"]
            sources.append(
                {
                    "gene": gene,
                    "source": "ChEMBL",
                    "query": gene,
                    "hit_count": row["chembl_activity_records"],
                    "url": row["chembl_url"],
                    "notes": json.dumps({"best_target": best, "n_search_hits": len(chembl["hits"])}, sort_keys=True),
                }
            )
        except Exception as exc:
            row["chembl_target_chembl_id"] = ""
            row["chembl_target_pref_name"] = ""
            row["chembl_target_type"] = ""
            row["chembl_activity_records"] = ""
            row["chembl_url"] = ""
            sources.append({"gene": gene, "source": "ChEMBL", "query": gene, "hit_count": "", "url": "", "notes": f"ERROR: {exc}"})

        patents_url = f"https://patents.google.com/?q={quote_plus(patent_query)}"
        row["google_patents_url"] = patents_url
        sources.append(
            {
                "gene": gene,
                "source": "Google Patents",
                "query": patent_query,
                "hit_count": "NA_browser",
                "url": patents_url,
                "notes": "query URL recorded; no unauthenticated count API used",
            }
        )

        opentargets_url = f"https://platform.opentargets.org/search?q={quote_plus(gene)}"
        row["opentargets_url"] = opentargets_url
        sources.append(
            {
                "gene": gene,
                "source": "OpenTargets",
                "query": gene,
                "hit_count": row["local_opentargets_disease_rows"],
                "url": opentargets_url,
                "notes": "local opentargets_candidate_disease_hits.tsv row count used for selected autoimmune panel",
            }
        )

        # Be polite to public APIs.
        time.sleep(0.25)

    return sources


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    metrics = collect_local_metrics()
    sources = add_external(metrics)
    for row in metrics.values():
        score_and_call(row)

    rows = sorted(metrics.values(), key=lambda r: ({"GO": 0, "PARK": 1, "NO_GO": 2}[r["wave18_call"]], -float(r["wave18_rescue_score"]), r["gene"]))

    candidate_fields = [
        "gene",
        "wave18_call",
        "wave18_rescue_score",
        "local_evidence_score",
        "druggability_access_score",
        "prior_art_saturation_penalty",
        "direction_penalty",
        "class",
        "accessibility",
        "modality",
        "direction",
        "wave18_call_reason",
        "local_recurrence_disease_count_union",
        "local_recurrence_disease_union",
        "local_state_coupled_disease_count_union",
        "local_state_coupled_disease_union",
        "broad_positive_disease_count",
        "broad_negative_disease_count",
        "broad_positive_diseases",
        "broad_negative_diseases",
        "broad_ms_wm_delta_log2",
        "broad_ms_wm_p",
        "broad_discovery_priority_score",
        "cross_trend_or_better_diseases",
        "cross_negative_trend_diseases",
        "cross_supporting_diseases",
        "surface_delta_trend_diseases",
        "surface_delta_fdr10_diseases",
        "surface_negative_delta_diseases",
        "surface_resid_state_diseases",
        "surface_raw_state_diseases",
        "surface_confounder_dominant_diseases",
        "surface_rank_score",
        "surface_local_call",
        "surface_delta_supporting_diseases",
        "surface_resid_supporting_diseases",
        "surface_reason",
        "orchestrator_class",
        "orchestrator_expr_trend_diseases",
        "orchestrator_expr_negative_diseases",
        "orchestrator_resid_state_diseases",
        "orchestrator_raw_state_diseases",
        "orchestrator_priority_score",
        "orchestrator_expression_supporting_diseases",
        "orchestrator_resid_supporting_diseases",
        "axis_mentions",
        "axis_mentioned_disease_count",
        "axis_mentioned_diseases",
        "existing_positive_rows",
        "existing_negative_rows",
        "existing_positive_diseases",
        "existing_negative_diseases",
        "local_opentargets_disease_rows",
        "local_opentargets_diseases",
        "local_opentargets_max_overall",
        "local_opentargets_max_genetic_association",
        "europepmc_hit_count",
        "clinical_trials_hit_count",
        "clinical_trials_returned_count",
        "chembl_target_chembl_id",
        "chembl_target_pref_name",
        "chembl_target_type",
        "chembl_activity_records",
        "europepmc_url",
        "clinical_trials_url",
        "chembl_url",
        "opentargets_url",
        "google_patents_url",
        "blocked_status_note",
    ]
    write_tsv(OUT / "accessible_target_rescue_candidates.tsv", rows, candidate_fields)

    source_fields = ["gene", "source", "query", "hit_count", "url", "notes"]
    write_tsv(OUT / "accessible_target_rescue_source_log.tsv", sources, source_fields)

    summary = {
        "n_candidates": len(rows),
        "calls": {call: sum(1 for r in rows if r["wave18_call"] == call) for call in ["GO", "PARK", "NO_GO"]},
        "go_genes": [r["gene"] for r in rows if r["wave18_call"] == "GO"],
        "park_genes": [r["gene"] for r in rows if r["wave18_call"] == "PARK"],
        "no_go_genes": [r["gene"] for r in rows if r["wave18_call"] == "NO_GO"],
        "created": "2026-05-27",
        "inputs": [
            "results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv",
            "results_v3/cross_disease_gene_summary.tsv",
            "results_v3/disease_axis_candidate_gene_rank.tsv",
            "results_v3/wave15_surface_trafficking_dependency/candidate_ranked.tsv",
            "results_v3/wave15_orchestrator_dependency_scan/candidate_dependency_priority_summary.tsv",
            "results_v3/existing_evidence_candidate_matrix.tsv",
            "results_v3/opentargets_candidate_disease_hits.tsv",
            "results_v3/intervention_prior_art_audit.tsv",
            "subagents_v3 wave5-wave17 reports",
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
