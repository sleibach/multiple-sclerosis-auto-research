#!/usr/bin/env python3
"""Wave20 genetics-first alternate-axis triage.

This worker deliberately starts from the local OpenTargets/genetics files rather
than from the exhausted lipid-lysosomal/APC module. It asks whether any
genetically anchored, currently druggable, cross-autoimmune target axis remains
after explicit exclusions and prior-art checks.

The screen is conservative: local OpenTargets rows are treated as locus-level
evidence unless a separate coloc/MR-ready note is available. Public API counts
are saturation flags, not proof of direct blocking prior art.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave20_genetic_druggable_altaxis"

OT_CREDIBLE = ROOT / "phases/v3/tmp" / "wave13_opentargets_gwas_credible_sets.tsv"
WAVE14_TRUTH = ROOT / "phases/v3/results" / "wave14_target_level_genetics" / "target_level_genetics_truth_table.tsv"
BROAD_H5AD = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
CENTRAL_FIRST_PASS = ROOT / "phases/v3/results" / "central_node_first_pass_rank.tsv"
CENTRAL_INTERVENTION = ROOT / "phases/v3/results" / "central_and_intervention_candidate_rank.tsv"
DISEASE_AXIS = ROOT / "phases/v3/results" / "disease_axis_candidate_gene_rank.tsv"
LOCAL_CHEMBL = ROOT / "phases/v3/results" / "druggability" / "chembl_target_activity_summary.tsv"
WAVE19 = ROOT / "phases/v3/results" / "wave19_orchestrator_controller_triage" / "wave19_controller_triage.tsv"

USER_AGENT = "ms-auto-research-wave20-genetic-druggable-altaxis/1.0"

EXPLICIT_EXCLUSIONS = {
    "NAMPT": "explicitly excluded: prior-demoted NAMPT/metabolic route",
    "SLC15A4": "explicitly excluded: prior-demoted SLC15A4/TASL route",
    "TASL": "explicitly excluded: prior-demoted SLC15A4/TASL route",
    "CXorf21": "explicitly excluded: TASL/CXorf21 route",
    "GSK3B": "explicitly excluded: prior-demoted GSK3B",
    "CTSH": "explicitly excluded: prior-demoted CTSH",
    "CTSS": "explicitly excluded: prior-demoted CTSS",
    "CD44": "explicitly excluded: CD44/SPP1 axis",
    "SPP1": "explicitly excluded: CD44/SPP1 axis",
    "CD274": "explicitly excluded: PD-L1/CD274",
    "LGALS3": "explicitly excluded: galectins",
    "LGALS9": "explicitly excluded: galectins",
    "C1QA": "explicitly excluded: complement/Fc/TAM/TREM",
    "C1QB": "explicitly excluded: complement/Fc/TAM/TREM",
    "C1QC": "explicitly excluded: complement/Fc/TAM/TREM",
    "CFH": "explicitly excluded: complement/Fc/TAM/TREM",
    "FCGR2A": "explicitly excluded: complement/Fc/TAM/TREM",
    "FCGR3A": "explicitly excluded: complement/Fc/TAM/TREM",
    "MERTK": "explicitly excluded: complement/Fc/TAM/TREM",
    "AXL": "explicitly excluded: complement/Fc/TAM/TREM",
    "TYROBP": "explicitly excluded: complement/Fc/TAM/TREM",
    "TREM1": "explicitly excluded: complement/Fc/TAM/TREM",
    "TREM2": "explicitly excluded: complement/Fc/TAM/TREM",
}

GENERIC_JAK_IFN = {
    "TYK2",
    "JAK1",
    "JAK2",
    "JAK3",
    "IFNGR1",
    "IFNGR2",
    "STAT1",
    "STAT2",
    "IRF1",
    "CXCL10",
}

ALT_CANDIDATES: dict[str, dict[str, Any]] = {
    "GPR65": {
        "axis": "acidic tissue pH-sensing GPCR / cAMP brake",
        "class": "membrane GPCR",
        "expected_modality": "agonist or positive allosteric modulator",
        "direction": "agonism/PAM if anti-inflammatory tissue-pH response is confirmed",
        "manual_target_level_note": "locus plus cis-eQTL-ready; no local disease-by-eQTL coloc run",
        "druggability_score": 2.0,
        "perturbation_score": 2.0,
        "manual_prior_art_risk": "high",
        "manual_blocker": "GPR65 autoimmune/IBD therapeutic use and GPR65 modulators already appear in public literature/patents; no clinical-stage autoimmune drug or biomarker-defined population delta found.",
    },
    "PTPN2": {
        "axis": "TCPTP cytokine/TCR barrier-restoration brake",
        "class": "intracellular phosphatase",
        "expected_modality": "would need restoration/activation; inhibitors point in the wrong autoimmune direction",
        "direction": "increase or restore TCPTP activity/function",
        "manual_target_level_note": "broad local locus evidence plus cis-eQTL-ready, but local audit lacked paired summary stats for coloc",
        "druggability_score": 0.75,
        "perturbation_score": 2.5,
        "manual_prior_art_risk": "high",
        "manual_blocker": "Autoimmune biology is loss-of-function/restoration; current drug discovery has stronger inhibitor precedent for oncology, which would be directionally unsafe for autoimmunity.",
    },
    "TNFAIP3": {
        "axis": "A20 ubiquitin-editing NF-kappaB/TNF/TLR brake",
        "class": "intracellular ubiquitin-editing enzyme/scaffold",
        "expected_modality": "restore A20 function or mimic negative-feedback complex",
        "direction": "increase/restore A20 function",
        "manual_target_level_note": "broad local locus evidence; no usable local cis-eQTL instrument in Wave14 panel",
        "druggability_score": 0.5,
        "perturbation_score": 2.0,
        "manual_prior_art_risk": "high",
        "manual_blocker": "Strong biology but direct restoration modality is not druggable now; broad NF-kappaB prior art and haploinsufficiency literature are crowded.",
    },
    "SH2B3": {
        "axis": "LNK hematopoietic cytokine/JAK-adaptor brake",
        "class": "intracellular adaptor",
        "expected_modality": "restore adaptor function or downstream pathway selection",
        "direction": "increase/restore LNK negative-regulatory function",
        "manual_target_level_note": "broadest local locus evidence, but 12q24 pleiotropy and no local target-level coloc/MR",
        "druggability_score": 0.25,
        "perturbation_score": 1.5,
        "manual_prior_art_risk": "medium",
        "manual_blocker": "No direct drug modality; pleiotropic hematopoietic/platelet/cardiovascular locus makes autoimmune-specific targeting unclear.",
    },
    "IRF5": {
        "axis": "TLR7/8/9-IRF5 inflammatory transcriptional switch",
        "class": "transcription factor",
        "expected_modality": "allosteric inhibitor or degrader",
        "direction": "inhibit IRF5 activation in selected IRF5/TLR-high disease",
        "manual_target_level_note": "broad local locus evidence and cis-eQTL-ready; no local coloc/MR run",
        "druggability_score": 2.0,
        "perturbation_score": 2.5,
        "manual_prior_art_risk": "high",
        "manual_blocker": "Emerging small-molecule/degrader programs and lupus preclinical prior art are already direct; route is also close to generic TLR/type-I-IFN biology.",
    },
    "CLEC16A": {
        "axis": "CLEC16A mitophagy/autophagy quality-control",
        "class": "intracellular autophagy scaffold",
        "expected_modality": "indirect mitophagy/autophagy restoration",
        "direction": "restore CLEC16A-linked mitophagy without broad autophagy toxicity",
        "manual_target_level_note": "broad local locus evidence but 16p13 locus ambiguity with CIITA/DEXI/SOCS1",
        "druggability_score": 0.75,
        "perturbation_score": 2.0,
        "manual_prior_art_risk": "medium",
        "manual_blocker": "No selective direct CLEC16A drug; locus ambiguity and indirect mitophagy modulators block target-level promotion.",
    },
    "ATG16L1": {
        "axis": "autophagy/xenophagy epithelial-immune stress handling",
        "class": "intracellular autophagy scaffold",
        "expected_modality": "indirect autophagy modulation",
        "direction": "restore autophagy/xenophagy in risk-variant carriers",
        "manual_target_level_note": "broad local locus evidence, but target-level direction and disease tissue vary",
        "druggability_score": 0.5,
        "perturbation_score": 2.0,
        "manual_prior_art_risk": "medium_high",
        "manual_blocker": "Autophagy pathway modulation is indirect and broad; no selective ATG16L1 target engagement package.",
    },
    "IL10": {
        "axis": "IL-10 regulatory cytokine tolerance",
        "class": "secreted cytokine",
        "expected_modality": "recombinant/engineered IL-10 or IL10R agonism",
        "direction": "increase regulatory IL-10 signaling in responder subset",
        "manual_target_level_note": "broad local locus evidence; secreted cytokine genetics does not define a new target-level autoimmune use",
        "druggability_score": 2.5,
        "perturbation_score": 2.0,
        "manual_prior_art_risk": "high",
        "manual_blocker": "IL-10 therapy has direct autoimmune/IBD prior art; no new biomarker-defined cross-autoimmune delta found in local data.",
    },
    "IL6R": {
        "axis": "IL-6 receptor inflammatory cytokine signaling",
        "class": "membrane/soluble cytokine receptor",
        "expected_modality": "approved anti-IL6R biologics",
        "direction": "block IL-6R where IL-6 biology is pathogenic",
        "manual_target_level_note": "local locus evidence in five diseases; public druggability is established",
        "druggability_score": 3.0,
        "perturbation_score": 2.5,
        "manual_prior_art_risk": "blocking",
        "manual_blocker": "Approved/late clinical autoimmune use of IL-6R blockade is direct blocking prior art, with disease-specific safety/direction issues.",
    },
    "CARD9": {
        "axis": "CARD9 innate fungal/NF-kappaB adaptor",
        "class": "intracellular adaptor",
        "expected_modality": "would need protein-interaction or downstream selective modulation",
        "direction": "context-dependent; inhibit inflammatory CARD9 while preserving antifungal immunity",
        "manual_target_level_note": "local locus support reaches four diseases, but target-level druggability is poor",
        "druggability_score": 0.25,
        "perturbation_score": 1.5,
        "manual_prior_art_risk": "medium",
        "manual_blocker": "No direct druggability now and infectious-risk direction is unfavorable.",
    },
    "OSMR": {
        "axis": "OSM/OSMR tissue inflammatory remodeling",
        "class": "cytokine receptor",
        "expected_modality": "anti-OSM/anti-OSMR biologic",
        "direction": "block OSMR signaling in tissue-remodeling-high disease",
        "manual_target_level_note": "local OT locus support reaches four diseases but prior V3 notes demoted OSMR as UC/IBD-heavy",
        "druggability_score": 2.0,
        "perturbation_score": 1.5,
        "manual_prior_art_risk": "medium_high",
        "manual_blocker": "Existing OSM/OSMR inflammatory bowel/tissue-remodeling literature and limited cross-disease local biology block promotion.",
    },
    "TYK2": {
        "axis": "TYK2 IL-12/23/type-I-IFN cytokine kinase",
        "class": "kinase",
        "expected_modality": "approved/clinical allosteric or ATP-competitive inhibitors",
        "direction": "inhibit TYK2",
        "manual_target_level_note": "public coloc/MR-ready evidence exists, but this is generic JAK/IFN-family biology",
        "druggability_score": 3.0,
        "perturbation_score": 3.0,
        "manual_prior_art_risk": "blocking",
        "manual_blocker": "Explicitly excluded generic JAK/IFN route without a new modality or biomarker-delta; TYK2 inhibitors already have autoimmune clinical programs.",
    },
}


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t")


def safe_num(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or (isinstance(value, float) and math.isnan(value)) or pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def split_semicolon(value: Any) -> list[str]:
    if value is None or (isinstance(value, float) and math.isnan(value)) or pd.isna(value):
        return []
    return [x.strip() for x in str(value).split(";") if x.strip()]


def get_json(url: str, params: dict[str, Any] | None = None, timeout: int = 30) -> Any:
    full_url = url
    if params:
        full_url = f"{url}?{urlencode(params)}"
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urlopen(Request(full_url, headers=headers), timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            last_error = exc
            time.sleep(1.0 * (attempt + 1))
    raise RuntimeError(f"request failed for {full_url}: {last_error}")


def europepmc_count(query: str) -> dict[str, Any]:
    params = {"query": query, "format": "json", "pageSize": 3, "resultType": "lite"}
    data = get_json("https://www.ebi.ac.uk/europepmc/webservices/rest/search", params=params)
    examples = []
    for item in data.get("resultList", {}).get("result", []):
        examples.append(
            {
                "id": item.get("id", ""),
                "source": item.get("source", ""),
                "title": item.get("title", ""),
                "journal": item.get("journalTitle", ""),
                "year": item.get("pubYear", ""),
                "doi": item.get("doi", ""),
            }
        )
    return {
        "hit_count": int(data.get("hitCount", 0) or 0),
        "url": f"https://europepmc.org/search?query={quote_plus(query)}",
        "examples": examples,
    }


def clinical_trials(term: str) -> dict[str, Any]:
    params = {"query.term": term, "pageSize": 5, "format": "json"}
    data = get_json("https://clinicaltrials.gov/api/v2/studies", params=params)
    studies = []
    for st in data.get("studies", []):
        protocol = st.get("protocolSection", {})
        ident = protocol.get("identificationModule", {})
        status = protocol.get("statusModule", {})
        design = protocol.get("designModule", {})
        conditions = protocol.get("conditionsModule", {})
        interventions = protocol.get("armsInterventionsModule", {}).get("interventions", [])
        studies.append(
            {
                "nct_id": ident.get("nctId", ""),
                "title": ident.get("briefTitle", ""),
                "status": status.get("overallStatus", ""),
                "phase": ";".join(design.get("phases", []) or []),
                "conditions": ";".join(conditions.get("conditions", []) or []),
                "interventions": ";".join(i.get("name", "") for i in interventions),
            }
        )
    return {
        "hit_count": int(data.get("totalCount", len(studies)) or 0),
        "returned_count": len(studies),
        "url": f"https://clinicaltrials.gov/search?term={quote_plus(term)}",
        "studies": studies,
    }


def chembl_target_search(gene: str) -> dict[str, Any]:
    data = get_json("https://www.ebi.ac.uk/chembl/api/data/target/search.json", {"q": gene, "limit": 20})
    hits = []
    for target in data.get("targets", []):
        components = target.get("target_components") or []
        symbols = []
        accessions = []
        for comp in components:
            if comp.get("accession"):
                accessions.append(comp["accession"])
            for synonym in comp.get("target_component_synonyms") or []:
                if synonym.get("syn_type") == "GENE_SYMBOL":
                    symbols.append(synonym.get("component_synonym", ""))
        hits.append(
            {
                "target_chembl_id": target.get("target_chembl_id", ""),
                "pref_name": target.get("pref_name", ""),
                "target_type": target.get("target_type", ""),
                "organism": target.get("organism", ""),
                "accessions": ";".join(sorted(set(filter(None, accessions)))),
                "gene_symbols": ";".join(sorted(set(filter(None, symbols)))),
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
        "best": best or {},
        "n_search_hits": len(hits),
        "url": f"https://www.ebi.ac.uk/chembl/g/#search_results/all/query={quote_plus(gene)}",
    }


def chembl_activity_count(target_chembl_id: str | None) -> dict[str, Any]:
    if not target_chembl_id:
        return {"activity_records": None, "url": ""}
    params = {"target_chembl_id": target_chembl_id, "standard_units": "nM", "limit": 1}
    data = get_json("https://www.ebi.ac.uk/chembl/api/data/activity.json", params=params)
    total = data.get("page_meta", {}).get("total_count")
    return {
        "activity_records": int(total) if total is not None else None,
        "url": f"https://www.ebi.ac.uk/chembl/g/#browse/activities/filter/target_chembl_id%3A{target_chembl_id}",
    }


def local_open_targets_summary() -> pd.DataFrame:
    if OT_CREDIBLE.exists():
        ot = read_tsv(OT_CREDIBLE)
        gene_col = "query_gene"
        disease_col = "disease"
        score_col = "max_score"
        count_col = "evidence_count"
    else:
        ot = pd.DataFrame()
        gene_col = disease_col = score_col = count_col = ""
    rows = []
    all_genes = sorted(set(ALT_CANDIDATES) | set(EXPLICIT_EXCLUSIONS) | GENERIC_JAK_IFN)
    for gene in all_genes:
        if ot.empty:
            sub = pd.DataFrame()
        else:
            sub = ot[ot[gene_col].astype(str).eq(gene)].copy()
        diseases_any = sorted(
            sub.loc[(sub[count_col].fillna(0) > 0) | (sub[score_col].fillna(0) > 0), disease_col].dropna().astype(str).unique()
        ) if not sub.empty else []
        diseases_ge05 = sorted(sub.loc[sub[score_col].fillna(0) >= 0.5, disease_col].dropna().astype(str).unique()) if not sub.empty else []
        diseases_ge08 = sorted(sub.loc[sub[score_col].fillna(0) >= 0.8, disease_col].dropna().astype(str).unique()) if not sub.empty else []
        rows.append(
            {
                "gene": gene,
                "ot_rows": int(len(sub)),
                "ot_max_score": safe_num(sub[score_col].max() if not sub.empty else 0),
                "ot_evidence_count_sum": int(safe_num(sub[count_col].sum() if not sub.empty else 0)),
                "ot_n_diseases_any": len(diseases_any),
                "ot_diseases_any": ";".join(diseases_any),
                "ot_n_diseases_score_ge_0_5": len(diseases_ge05),
                "ot_diseases_score_ge_0_5": ";".join(diseases_ge05),
                "ot_n_diseases_score_ge_0_8": len(diseases_ge08),
                "ot_diseases_score_ge_0_8": ";".join(diseases_ge08),
            }
        )
    return pd.DataFrame(rows)


def local_metric_rows() -> pd.DataFrame:
    genes = sorted(ALT_CANDIDATES)
    broad = read_tsv(BROAD_H5AD)
    central_first = read_tsv(CENTRAL_FIRST_PASS)
    disease_axis = read_tsv(DISEASE_AXIS)
    wave19 = read_tsv(WAVE19)
    local_chembl = read_tsv(LOCAL_CHEMBL)

    rows = []
    for gene in genes:
        row: dict[str, Any] = {"gene": gene}
        b = broad[broad["gene"].astype(str).eq(gene)].head(1) if not broad.empty and "gene" in broad.columns else pd.DataFrame()
        c = central_first[central_first["gene"].astype(str).eq(gene)].head(1) if not central_first.empty and "gene" in central_first.columns else pd.DataFrame()
        d = disease_axis[disease_axis["gene"].astype(str).eq(gene)].head(1) if not disease_axis.empty and "gene" in disease_axis.columns else pd.DataFrame()
        w = wave19[wave19["gene"].astype(str).eq(gene)].head(1) if not wave19.empty and "gene" in wave19.columns else pd.DataFrame()
        lc = local_chembl[local_chembl["gene"].astype(str).eq(gene)].copy() if not local_chembl.empty and "gene" in local_chembl.columns else pd.DataFrame()

        if not b.empty:
            br = b.iloc[0]
            row.update(
                {
                    "broad_positive_disease_count": safe_num(br.get("positive_disease_count")),
                    "broad_negative_disease_count": safe_num(br.get("negative_disease_count")),
                    "broad_positive_diseases": br.get("positive_diseases", ""),
                    "broad_negative_diseases": br.get("negative_diseases", ""),
                    "ms_wm_delta_log2": safe_num(br.get("ms_wm_delta_log2"), float("nan")),
                    "ms_wm_p": safe_num(br.get("ms_wm_p"), float("nan")),
                    "discovery_priority_score": safe_num(br.get("discovery_priority_score")),
                }
            )
        else:
            row.update(
                {
                    "broad_positive_disease_count": 0,
                    "broad_negative_disease_count": 0,
                    "broad_positive_diseases": "",
                    "broad_negative_diseases": "",
                    "ms_wm_delta_log2": "",
                    "ms_wm_p": "",
                    "discovery_priority_score": 0,
                }
            )

        if not c.empty:
            cr = c.iloc[0]
            row.update(
                {
                    "central_node_priority_score": safe_num(cr.get("priority_score")),
                    "central_node_axis": cr.get("axis", ""),
                    "central_node_positive_disease_count": safe_num(cr.get("positive_disease_count")),
                    "central_node_negative_disease_count": safe_num(cr.get("negative_disease_count")),
                }
            )
        else:
            row.update(
                {
                    "central_node_priority_score": 0,
                    "central_node_axis": "",
                    "central_node_positive_disease_count": 0,
                    "central_node_negative_disease_count": 0,
                }
            )

        if not d.empty:
            dr = d.iloc[0]
            row.update(
                {
                    "disease_axis_priority_score": safe_num(dr.get("priority_score")),
                    "disease_axis_mentioned_disease_count": safe_num(dr.get("mentioned_disease_count")),
                    "disease_axis_mentioned_diseases": dr.get("mentioned_diseases", ""),
                }
            )
        else:
            row.update(
                {
                    "disease_axis_priority_score": 0,
                    "disease_axis_mentioned_disease_count": 0,
                    "disease_axis_mentioned_diseases": "",
                }
            )

        if not w.empty:
            wr = w.iloc[0]
            row.update(
                {
                    "wave19_local_score": safe_num(wr.get("local_score")),
                    "wave19_call": wr.get("orchestrator_call", ""),
                }
            )
        else:
            row.update({"wave19_local_score": 0, "wave19_call": ""})

        if not lc.empty:
            row["local_chembl_activity_values_nM_count"] = int(safe_num(lc["activity_values_nM_count"].fillna(0).max()))
            row["local_chembl_best_standard_value_nM"] = safe_num(lc["best_standard_value_nM"].min(), float("nan"))
        else:
            row["local_chembl_activity_values_nM_count"] = 0
            row["local_chembl_best_standard_value_nM"] = ""
        rows.append(row)
    return pd.DataFrame(rows)


def public_api_audit() -> pd.DataFrame:
    rows = []
    for gene, meta in ALT_CANDIDATES.items():
        query = f'("{gene}" OR "{meta["axis"].split()[0]}") autoimmune'
        trial_term = f"{gene} autoimmune"
        if gene == "IL10":
            query = '("IL-10" OR IL10) autoimmune'
            trial_term = "IL-10 autoimmune"
        elif gene == "IL6R":
            query = '("IL-6 receptor" OR IL6R OR tocilizumab OR sarilumab) autoimmune'
            trial_term = "IL-6 receptor autoimmune"
        elif gene == "GPR65":
            query = '("GPR65" OR TDAG8) autoimmune OR inflammatory bowel disease'
            trial_term = "GPR65 autoimmune"
        elif gene == "TNFAIP3":
            query = '("TNFAIP3" OR A20) autoimmune'
            trial_term = "TNFAIP3 autoimmune"
        elif gene == "SH2B3":
            query = '("SH2B3" OR LNK) autoimmune'
            trial_term = "SH2B3 autoimmune"
        elif gene == "ATG16L1":
            query = '("ATG16L1" OR autophagy) autoimmune Crohn'
            trial_term = "ATG16L1 autoimmune"
        elif gene == "OSMR":
            query = '("OSMR" OR "oncostatin M receptor") autoimmune'
            trial_term = "OSMR autoimmune"
        elif gene == "TYK2":
            query = '("TYK2" OR deucravacitinib) autoimmune'
            trial_term = "TYK2 autoimmune"

        row = {
            "gene": gene,
            "europepmc_query": query,
            "clinicaltrials_query": trial_term,
            "google_patents_url": f"https://patents.google.com/?q={quote_plus(gene + ' autoimmune drug')}",
        }
        try:
            epmc = europepmc_count(query)
            row["europepmc_hit_count"] = epmc["hit_count"]
            row["europepmc_url"] = epmc["url"]
            row["europepmc_examples_json"] = json.dumps(epmc["examples"], sort_keys=True)
        except Exception as exc:
            row["europepmc_hit_count"] = ""
            row["europepmc_url"] = ""
            row["europepmc_examples_json"] = f"ERROR: {type(exc).__name__}: {exc}"

        try:
            trials = clinical_trials(trial_term)
            row["clinicaltrials_hit_count"] = trials["hit_count"]
            row["clinicaltrials_returned_count"] = trials["returned_count"]
            row["clinicaltrials_url"] = trials["url"]
            row["clinicaltrials_examples_json"] = json.dumps(trials["studies"], sort_keys=True)
        except Exception as exc:
            row["clinicaltrials_hit_count"] = ""
            row["clinicaltrials_returned_count"] = ""
            row["clinicaltrials_url"] = ""
            row["clinicaltrials_examples_json"] = f"ERROR: {type(exc).__name__}: {exc}"

        try:
            target = chembl_target_search(gene)
            best = target.get("best") or {}
            activity = chembl_activity_count(best.get("target_chembl_id")) if best else {"activity_records": None, "url": target["url"]}
            row["chembl_target_chembl_id"] = best.get("target_chembl_id", "")
            row["chembl_target_pref_name"] = best.get("pref_name", "")
            row["chembl_target_type"] = best.get("target_type", "")
            row["chembl_activity_records"] = "" if activity["activity_records"] is None else activity["activity_records"]
            row["chembl_url"] = activity.get("url") or target["url"]
            row["chembl_search_hit_count"] = target.get("n_search_hits", "")
        except Exception as exc:
            row["chembl_target_chembl_id"] = ""
            row["chembl_target_pref_name"] = ""
            row["chembl_target_type"] = ""
            row["chembl_activity_records"] = ""
            row["chembl_url"] = ""
            row["chembl_search_hit_count"] = ""
            row["chembl_error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
        time.sleep(0.2)
    return pd.DataFrame(rows)


def rank_candidates(ot_summary: pd.DataFrame, local: pd.DataFrame, public: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    ot_by_gene = ot_summary.set_index("gene") if not ot_summary.empty else pd.DataFrame()
    local_by_gene = local.set_index("gene") if not local.empty else pd.DataFrame()
    public_by_gene = public.set_index("gene") if not public.empty else pd.DataFrame()

    ranked_rows = []
    excluded_rows = []
    for gene, meta in ALT_CANDIDATES.items():
        ot = ot_by_gene.loc[gene].to_dict() if gene in ot_by_gene.index else {}
        loc = local_by_gene.loc[gene].to_dict() if gene in local_by_gene.index else {}
        pub = public_by_gene.loc[gene].to_dict() if gene in public_by_gene.index else {}

        ge05 = int(safe_num(ot.get("ot_n_diseases_score_ge_0_5")))
        ge08 = int(safe_num(ot.get("ot_n_diseases_score_ge_0_8")))
        broad_pos = int(safe_num(loc.get("broad_positive_disease_count")))
        broad_neg = int(safe_num(loc.get("broad_negative_disease_count")))
        central_pos = int(safe_num(loc.get("central_node_positive_disease_count")))
        epmc = int(safe_num(pub.get("europepmc_hit_count")))
        trials = int(safe_num(pub.get("clinicaltrials_hit_count")))
        chembl = int(safe_num(pub.get("chembl_activity_records")))

        genetics_score = min(3.0, ge05 / 2.0) + min(1.0, ge08 / 8.0)
        local_biology_score = min(2.0, broad_pos / 2.0) - min(1.5, broad_neg * 0.75) + min(1.0, central_pos / 4.0)
        druggability_score = safe_num(meta["druggability_score"])
        perturbation_score = safe_num(meta["perturbation_score"])
        prior_art_penalty = 0.0
        if epmc >= 500:
            prior_art_penalty += 1.0
        if epmc >= 2000:
            prior_art_penalty += 1.0
        if trials >= 1:
            prior_art_penalty += 1.0
        if trials >= 5:
            prior_art_penalty += 1.0
        if str(meta["manual_prior_art_risk"]) in {"high", "blocking"}:
            prior_art_penalty += 2.0
        elif str(meta["manual_prior_art_risk"]) == "medium_high":
            prior_art_penalty += 1.25
        elif str(meta["manual_prior_art_risk"]) == "medium":
            prior_art_penalty += 0.75

        exclusion_reason = ""
        if gene in EXPLICIT_EXCLUSIONS:
            exclusion_reason = EXPLICIT_EXCLUSIONS[gene]
        elif gene in GENERIC_JAK_IFN:
            exclusion_reason = "explicitly excluded: generic JAK/IFN-family route; no new modality/population delta found"

        has_four_disease_genetics = ge05 >= 4
        target_level_signal = "coloc_or_mr_ready" if gene == "TYK2" else "locus_only_or_coloc_ready_not_run"
        if gene in {"PTPN2", "GPR65", "IRF5"}:
            target_level_signal = "defensible_future_coloc_ready_not_completed"
        if gene in {"SH2B3", "CLEC16A"}:
            target_level_signal = "locus_broad_but_ambiguous"

        promotion_gate = "NO_GO"
        gate_failures = []
        if exclusion_reason:
            gate_failures.append(exclusion_reason)
        if not has_four_disease_genetics:
            gate_failures.append("genetic breadth below four diseases at local OT score>=0.5")
        if target_level_signal not in {"coloc_or_mr_ready", "defensible_future_coloc_ready_not_completed"}:
            gate_failures.append("target-level coloc/MR signal not established")
        if druggability_score < 2.0:
            gate_failures.append("not druggable now for the required autoimmune direction")
        if perturbation_score < 2.0:
            gate_failures.append("real perturbation or strong model support is insufficient")
        if meta["manual_prior_art_risk"] in {"high", "blocking"}:
            gate_failures.append("blocking or near-blocking prior art for autoimmune use")
        if not gate_failures:
            promotion_gate = "GO_REVIEW"

        priority_score = (
            genetics_score
            + local_biology_score
            + druggability_score
            + perturbation_score
            - prior_art_penalty
            - (4.0 if exclusion_reason else 0.0)
        )

        ranked_rows.append(
            {
                "gene": gene,
                "axis": meta["axis"],
                "class": meta["class"],
                "expected_modality": meta["expected_modality"],
                "direction": meta["direction"],
                "promotion_gate": promotion_gate,
                "priority_score": round(priority_score, 3),
                "genetics_score": round(genetics_score, 3),
                "local_biology_score": round(local_biology_score, 3),
                "druggability_score_manual": druggability_score,
                "perturbation_score_manual": perturbation_score,
                "prior_art_penalty": round(prior_art_penalty, 3),
                "explicit_exclusion_reason": exclusion_reason,
                "target_level_signal": target_level_signal,
                "ot_n_diseases_score_ge_0_5": ge05,
                "ot_diseases_score_ge_0_5": ot.get("ot_diseases_score_ge_0_5", ""),
                "ot_n_diseases_score_ge_0_8": ge08,
                "broad_positive_disease_count": broad_pos,
                "broad_positive_diseases": loc.get("broad_positive_diseases", ""),
                "broad_negative_disease_count": broad_neg,
                "central_node_positive_disease_count": central_pos,
                "europepmc_hit_count": epmc,
                "clinicaltrials_hit_count": trials,
                "chembl_activity_records": chembl,
                "manual_target_level_note": meta["manual_target_level_note"],
                "manual_prior_art_risk": meta["manual_prior_art_risk"],
                "manual_blocker": meta["manual_blocker"],
                "gate_failures": "; ".join(gate_failures),
            }
        )
        if exclusion_reason:
            excluded_rows.append(
                {
                    "gene": gene,
                    "axis": meta["axis"],
                    "exclusion_reason": exclusion_reason,
                    "ot_n_diseases_score_ge_0_5": ge05,
                    "druggability_score_manual": druggability_score,
                    "manual_blocker": meta["manual_blocker"],
                }
            )

    ranked = pd.DataFrame(ranked_rows).sort_values(["promotion_gate", "priority_score"], ascending=[True, False])
    already_excluded = {row["gene"] for row in excluded_rows}
    for gene, reason in {**EXPLICIT_EXCLUSIONS, **{g: "explicitly excluded: generic JAK/IFN-family route" for g in GENERIC_JAK_IFN}}.items():
        if gene in already_excluded:
            continue
        ot = ot_by_gene.loc[gene].to_dict() if gene in ot_by_gene.index else {}
        excluded_rows.append(
            {
                "gene": gene,
                "axis": "",
                "exclusion_reason": reason,
                "ot_n_diseases_score_ge_0_5": int(safe_num(ot.get("ot_n_diseases_score_ge_0_5"))),
                "druggability_score_manual": "",
                "manual_blocker": "excluded by Wave20 prompt or generic route guardrail; no materially new modality, compartment, or biomarker-defined population delta found",
            }
        )
    excluded = pd.DataFrame(excluded_rows).sort_values("gene")
    return ranked, excluded


def source_interpretation_rows() -> pd.DataFrame:
    rows = [
        {
            "gene": "GPR65",
            "source": "PMCID:PMC8629932",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8629932/",
            "interpretation": "GPR65 has disease genetics and experimental colitis biology; the paper itself suggests GPR65 as an IBD intervention target, so the broad autoimmune-use concept is not cleanly novel.",
        },
        {
            "gene": "GPR65",
            "source": "Google Patents WO2023067322A1",
            "url": "https://patents.google.com/patent/WO2023067322A1/en",
            "interpretation": "GPR65 modulators are already patented with autoimmune-disease language, including MS/AS/IBD/Crohn references.",
        },
        {
            "gene": "PTPN2",
            "source": "PMCID:PMC9456094",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9456094/",
            "interpretation": "PTPN2 loss-of-function variants are linked to several immune diseases; therapeutic direction for autoimmunity is restoration, not inhibition.",
        },
        {
            "gene": "TNFAIP3",
            "source": "PMCID:PMC6942121",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6942121/",
            "interpretation": "A20/TNFAIP3 is a broad autoimmune genetics and NF-kappaB brake, but direct restoration is not a druggable current modality.",
        },
        {
            "gene": "SH2B3",
            "source": "PMCID:PMC4058736",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4058736/",
            "interpretation": "The 12q24/SH2B3 region is highly pleiotropic across autoimmune, hematologic, vascular, and other traits, weakening target-specific autoimmune inference.",
        },
        {
            "gene": "IRF5",
            "source": "PMCID:PMC7685739",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7685739/",
            "interpretation": "IRF5 inhibition has direct lupus-model prior art and human autoimmune genetic rationale; this supports feasibility but crowds novelty.",
        },
        {
            "gene": "IRF5",
            "source": "HotSpot Therapeutics 2026",
            "url": "https://www.hotspotthera.com/press_release/hotspot-therapeutics-presents-preclinical-data-from-small-molecule-irf5-inhibitor-program-at-15th-european-lupus-meeting/",
            "interpretation": "As of 2026-03-04, a company reports preclinical oral allosteric IRF5 inhibitors for SLE/additional autoimmune diseases, creating active program prior art.",
        },
        {
            "gene": "CLEC16A",
            "source": "PMCID:PMC10179542",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10179542/",
            "interpretation": "CLEC16A connects autoimmunity to autophagy/mitophagy and possible repurposing, but no selective direct CLEC16A drug exists.",
        },
        {
            "gene": "TYK2",
            "source": "PMCID:PMC9988426",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9988426/",
            "interpretation": "TYK2 has MR/coloc and clinical-trial support across autoimmune diseases, but it is a generic JAK/IFN-family route and heavily prior-arted.",
        },
        {
            "gene": "IL10",
            "source": "ClinicalTrials.gov search",
            "url": "https://clinicaltrials.gov/search?term=IL-10%20autoimmune",
            "interpretation": "IL-10/low-inflammatory regulatory cytokine therapeutic history is direct prior art; no local biomarker-delta rescues it.",
        },
        {
            "gene": "IL6R",
            "source": "ChEMBL/clinical class",
            "url": "https://www.ebi.ac.uk/chembl/g/#search_results/all/query=IL6R",
            "interpretation": "IL6R is druggable with approved autoimmune biologic precedent; novelty is blocked.",
        },
    ]
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    ot_summary = local_open_targets_summary()
    local_metrics = local_metric_rows()
    public_audit = public_api_audit()
    ranked, excluded = rank_candidates(ot_summary, local_metrics, public_audit)
    sources = source_interpretation_rows()

    ot_summary.to_csv(OUT / "local_opentargets_genetics_summary.tsv", sep="\t", index=False)
    local_metrics.to_csv(OUT / "local_biology_and_druggability_metrics.tsv", sep="\t", index=False)
    public_audit.to_csv(OUT / "public_api_prior_art_druggability_audit.tsv", sep="\t", index=False)
    ranked.to_csv(OUT / "negative_ranked_shortlist.tsv", sep="\t", index=False)
    excluded.to_csv(OUT / "excluded_axis_screen.tsv", sep="\t", index=False)
    sources.to_csv(OUT / "public_source_interpretation.tsv", sep="\t", index=False)

    summary = {
        "date": "2026-05-27",
        "candidate_count": len(ranked),
        "promoted_count": int((ranked["promotion_gate"] == "GO_REVIEW").sum()),
        "top_ranked_non_promoted": ranked.head(5).to_dict(orient="records"),
        "explicitly_excluded_count_in_screen": len(excluded),
        "verdict": "negative: no cross-autoimmune genetically anchored and druggable alternate axis cleared promotion bar",
        "promotion_bar": {
            "genetic_anchor": ">=4 local OpenTargets diseases at score>=0.5 or defensible coloc/MR-ready target-level signal",
            "druggability": "current direct modality in the required autoimmune direction",
            "perturbation": "real perturbation or strong mechanistic model support",
            "novelty": "no blocking autoimmune-use prior art for the specific target/axis",
        },
        "inputs": [
            str(OT_CREDIBLE.relative_to(ROOT)) if OT_CREDIBLE.exists() else str(WAVE14_TRUTH.relative_to(ROOT)),
            str(WAVE14_TRUTH.relative_to(ROOT)),
            str(BROAD_H5AD.relative_to(ROOT)),
            str(CENTRAL_FIRST_PASS.relative_to(ROOT)),
            str(CENTRAL_INTERVENTION.relative_to(ROOT)),
            str(DISEASE_AXIS.relative_to(ROOT)),
            str(LOCAL_CHEMBL.relative_to(ROOT)),
            str(WAVE19.relative_to(ROOT)),
            "EuropePMC API",
            "ClinicalTrials.gov API v2",
            "ChEMBL API",
            "manual public source interpretation table",
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"out": str(OUT.relative_to(ROOT)), "promoted_count": summary["promoted_count"]}, indent=2))


if __name__ == "__main__":
    main()
