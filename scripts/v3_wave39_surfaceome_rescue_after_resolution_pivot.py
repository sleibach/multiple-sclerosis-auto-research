#!/usr/bin/env python3
"""Wave39 accessibility-first rescue after resolution/efferocytosis closure.

This scan deliberately changes the starting point. Previous waves began from
the lipid-lysosomal/resolution module and repeatedly failed to nominate an
intervention. Here the first gate is therapeutic accessibility plus broad
cross-autoimmune recurrence.

The result is a triage table, not a therapeutic claim. A `GO_REVIEW` row means
"send to a full hostile novelty/mechanism package"; it is not a finding.
"""

from __future__ import annotations

import json
import math
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave39_surfaceome_rescue_after_resolution_pivot"
RAW = OUT / "raw_api"

BROAD_H5AD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
SURFACE_W15 = ROOT / "results_v3" / "wave15_surface_trafficking_dependency" / "candidate_ranked.tsv"
WAVE18 = ROOT / "results_v3" / "wave18_accessible_target_rescue" / "accessible_target_rescue_candidates.tsv"
WAVE21 = ROOT / "results_v3" / "wave21_residual_druggability_scan" / "wave21_residual_druggability_rank.tsv"
WAVE21_PRIOR = ROOT / "results_v3" / "wave21_residual_candidate_prior_art" / "candidate_prior_art_gate.tsv"
WAVE22_SUMMARY = ROOT / "results_v3" / "wave22_sqle_failfast" / "summary.json"
WAVE25 = ROOT / "results_v3" / "wave25_causal_genetics_module_proxy" / "causal_proxy_candidate_matrix.tsv"
WAVE34 = (
    ROOT
    / "results_v3"
    / "wave34_genetics_expression_druggability_scan"
    / "wave34_genetics_expression_druggability_rank.tsv"
)
WAVE38 = ROOT / "results_v3" / "wave38_crispr_state_druggability_rescue" / "crispr_state_druggability_rescue_rank.tsv"

USER_AGENT = "ms-auto-research-wave39-surfaceome-rescue/1.0"
SEED = 20260527

SYMBOL_RE = re.compile(r"^[A-Z0-9][A-Z0-9_.-]{1,20}$")

GENERIC_IFN = {
    "GBP1",
    "GBP2",
    "GBP3",
    "GBP4",
    "GBP5",
    "IFI27",
    "IFI30",
    "IFI35",
    "IFI44",
    "IFI44L",
    "IFIT1",
    "IFIT2",
    "IFIT3",
    "IFITM1",
    "IFITM2",
    "IFITM3",
    "IRF1",
    "IRF7",
    "ISG15",
    "MX1",
    "OAS1",
    "OAS2",
    "OAS3",
    "PSME1",
    "PSME2",
    "STAT1",
    "STAT2",
}

GENERIC_CYTOKINE_CHEMOKINE = {
    "CCL2",
    "CCL3",
    "CCL4",
    "CCL5",
    "CCL20",
    "CXCL8",
    "CXCL9",
    "CXCL10",
    "CXCL11",
    "IFNG",
    "IL1B",
    "IL6",
    "IL15",
    "TNF",
}

CORE_PREFIXES = ("RPL", "RPS", "MRPL", "MRPS", "HLA-")
CORE_MACHINERY = {
    "ACTB",
    "AQR",
    "B2M",
    "CBX3",
    "EEF1E1",
    "FAM136A",
    "GAPDH",
    "HSPA5",
    "HSPA9",
    "HSP90AA1",
    "LRRC59",
    "NME1",
    "POMP",
    "PPIA",
    "PPIB",
    "SEC61A1",
    "SEC61B",
    "TMSB10",
    "TPT1",
    "UBB",
}

PROTEASOME_CORE = {
    "PSMA1",
    "PSMA2",
    "PSMA3",
    "PSMA4",
    "PSMA5",
    "PSMA6",
    "PSMA7",
    "PSMB1",
    "PSMB2",
    "PSMB3",
    "PSMB4",
    "PSMB5",
    "PSMB6",
    "PSMB7",
    "PSMB8",
    "PSMB9",
    "PSMB10",
    "PSMD1",
    "PSMD2",
    "PSMD3",
    "PSMD4",
    "PSME1",
    "PSME2",
    "POMP",
}

PRIOR_CLASS_EXCLUSIONS = {
    "ACSL1": "prior ACSL1 demotion: marker/state association, not intervention",
    "ACSL3": "prior lipid-handling route with no safe direction",
    "AXL": "prior TAM/efferocytosis route demoted",
    "C1QA": "prior complement route demoted",
    "C1QB": "prior complement route demoted",
    "C1QC": "prior complement route demoted",
    "CD44": "prior CD44/SPP1 route parked/demoted",
    "CD47": "prior CD47/SIRPA phagocytosis checkpoint demoted",
    "CD74": "HLA-II/CD74 state marker and crowded CD74/MIF biology",
    "CD82": "prior Wave21 demotion: broad raw state marker, no strict residual or direction",
    "CD274": "prior PD-L1 checkpoint route crowded and directionally complex",
    "CFB": "prior complement route demoted",
    "CHI3L1": "secreted biomarker-dominated route; prior Wave18 parked",
    "CTSH": "prior cathepsin route demoted after chemistry/selectivity",
    "CTSS": "prior cathepsin route demoted due clinical/prior-art crowding",
    "GPNMB": "prior lipid-loader/repair glycoprotein route demoted",
    "LGALS3": "prior galectin route demoted",
    "LGALS9": "prior galectin route demoted",
    "LIPA": "prior lysosomal lipid route demoted",
    "MERTK": "prior TAM/efferocytosis route demoted",
    "MSR1": "prior scavenger-receptor route parked without direction",
    "NAMPT": "prior metabolic route blocked by prior art",
    "PDPN": "stromal/repair surface marker with repair liability",
    "SIRPA": "prior CD47/SIRPA phagocytosis checkpoint demoted",
    "SPP1": "prior CD44/SPP1 route demoted",
    "SQLE": "prior Wave22 fail-fast negative",
    "TGM2": "celiac/fibrosis/repair route; no new autoimmune delta",
    "TIMP1": "matrix/repair marker with unsafe direction",
    "TREM1": "prior TREM route demoted",
    "TREM2": "prior TREM route demoted",
    "TYROBP": "intracellular adaptor in prior TREM/DAP12 route",
}


def clean_symbol(value: Any) -> str:
    text = str(value or "").strip().upper()
    return text if SYMBOL_RE.match(text) else ""


def safe_num(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        val = float(value)
    except Exception:
        return default
    return val if math.isfinite(val) else default


def safe_int(value: Any, default: int = 0) -> int:
    return int(round(safe_num(value, default)))


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def get_json(url: str, params: dict[str, Any] | None = None, timeout: int = 45) -> Any:
    full_url = url if params is None else f"{url}?{urlencode(params)}"
    req = Request(full_url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            last_error = exc
            time.sleep(1.0 + attempt)
    raise RuntimeError(f"request failed for {full_url}: {last_error}")


def cached_json(name: str, fetcher) -> Any:
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / name
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    data = fetcher()
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return data


def split_diseases(value: Any) -> list[str]:
    if value is None or pd.isna(value):
        return []
    return [part.strip() for part in str(value).split(";") if part.strip()]


def has_ms_anchor(row: pd.Series) -> bool:
    return (
        bool(row.get("ms_positive_trend", False))
        or bool(row.get("ms_positive_nominal", False))
        or (safe_num(row.get("ms_wm_delta_log2")) > 0.25 and safe_num(row.get("ms_wm_p"), 1.0) <= 0.25)
    )


def load_broad_pool() -> pd.DataFrame:
    broad = read_tsv(BROAD_H5AD)
    if broad.empty:
        raise FileNotFoundError(BROAD_H5AD)
    broad["gene"] = broad["gene"].map(clean_symbol)
    broad = broad.loc[broad["gene"].ne("")].copy()
    for col in [
        "positive_disease_count",
        "negative_disease_count",
        "positive_compartment_count",
        "positive_fdr10_compartment_count",
        "negative_fdr10_compartment_count",
        "best_positive_p",
        "best_positive_fdr",
        "median_positive_hedges_g",
        "max_positive_delta_log2_cpm",
        "ms_wm_delta_log2",
        "ms_wm_p",
        "ms_wm_fdr",
        "opentargets_disease_count",
        "opentargets_max_genetic_association",
        "discovery_priority_score",
    ]:
        if col in broad.columns:
            broad[col] = pd.to_numeric(broad[col], errors="coerce")
    for col in ["ms_positive_nominal", "ms_positive_trend", "in_lipid_lysosomal_myeloid_neighborhood"]:
        if col in broad.columns:
            broad[col] = broad[col].astype(str).str.lower().isin({"true", "1", "yes"})
    broad["has_ms_anchor"] = broad.apply(has_ms_anchor, axis=1)
    broad["broad_pool_reason"] = broad.apply(
        lambda r: (
            "positive_disease_count>=4"
            if safe_int(r.get("positive_disease_count")) >= 4
            else "positive_disease_count>=3_with_MS_anchor"
        ),
        axis=1,
    )
    pool = broad.loc[
        (broad["positive_disease_count"].fillna(0) >= 4)
        | ((broad["positive_disease_count"].fillna(0) >= 3) & broad["has_ms_anchor"])
    ].copy()
    pool = pool.sort_values(
        ["positive_disease_count", "has_ms_anchor", "discovery_priority_score"],
        ascending=[False, False, False],
    ).reset_index(drop=True)
    return pool


def summarize_uniprot(gene: str, raw: dict[str, Any]) -> dict[str, Any]:
    results = raw.get("results", [])
    if not results:
        return {"gene": gene, "uniprot_status": "not_found"}
    top = results[0]
    protein = top.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", "")
    if not protein:
        subs = top.get("proteinDescription", {}).get("submissionNames") or []
        protein = subs[0].get("fullName", {}).get("value", "") if subs else ""

    comments = top.get("comments") or []
    functions: list[str] = []
    locations: list[str] = []
    for comment in comments:
        if comment.get("commentType") == "FUNCTION":
            functions.extend(t.get("value", "") for t in comment.get("texts", []) if t.get("value"))
        if comment.get("commentType") == "SUBCELLULAR LOCATION":
            for loc in comment.get("subcellularLocations") or []:
                value = loc.get("location", {}).get("value")
                if value:
                    locations.append(value)
    keywords = [kw.get("name", "") for kw in top.get("keywords", []) if kw.get("name")]
    features = top.get("features") or []
    feature_types = [f.get("type", "") for f in features if f.get("type")]
    transmembrane_features = [f for f in features if f.get("type") == "Transmembrane"]
    active_features = [
        f"{f.get('type')}:{f.get('description','')}".strip(":")
        for f in features
        if f.get("type") in {"Active site", "Binding site", "Metal binding", "DNA binding"}
    ]
    sequence = top.get("sequence", {}).get("value", "")
    location_keyword_blob = " ".join([";".join(locations), ";".join(keywords), ";".join(feature_types)]).lower()
    function_blob = " ".join([protein, " ".join(functions)]).lower()
    combined_blob = " ".join([function_blob, location_keyword_blob])
    access_tokens = ["cell membrane", "plasma membrane", "secreted", "extracellular", "transmembrane", "cell surface"]
    accessible = any(token in location_keyword_blob for token in access_tokens) or bool(transmembrane_features)
    # Do not treat incidental words such as "reference proteome" as evidence of
    # accessibility. Receptor/cytokine wording must be supported by membrane,
    # extracellular, secreted, or transmembrane annotations above.
    enzymatic = any(token in combined_blob for token in ["enzyme", "catalytic", "hydrolase", "kinase", "protease", "phosphatase"])
    return {
        "gene": gene,
        "uniprot_status": "found",
        "uniprot_accession": top.get("primaryAccession", ""),
        "protein_name": protein,
        "sequence_length": len(sequence),
        "uniprot_locations": ";".join(sorted(set(locations))),
        "uniprot_keywords": ";".join(sorted(set(keywords))),
        "uniprot_accessible": accessible,
        "uniprot_enzymatic_or_catalytic": enzymatic,
        "uniprot_transmembrane_feature_count": len(transmembrane_features),
        "uniprot_active_or_binding_features": ";".join(active_features[:20]),
        "function_excerpt": " ".join(functions)[:700],
    }


def uniprot_for_gene(gene: str) -> dict[str, Any]:
    fields = ",".join(
        [
            "accession",
            "id",
            "protein_name",
            "gene_names",
            "cc_function",
            "cc_subcellular_location",
            "keyword",
            "ft_act_site",
            "ft_binding",
            "ft_topo_dom",
            "ft_transmem",
            "sequence",
        ]
    )

    def fetch():
        return get_json(
            "https://rest.uniprot.org/uniprotkb/search",
            {
                "query": f"(gene_exact:{gene}) AND (organism_id:9606) AND (reviewed:true)",
                "format": "json",
                "fields": fields,
                "size": 3,
            },
        )

    try:
        raw = cached_json(f"uniprot_{gene}.json", fetch)
        return summarize_uniprot(gene, raw)
    except Exception as exc:
        return {"gene": gene, "uniprot_status": "api_error", "uniprot_error": f"{type(exc).__name__}: {exc}"}


def exact_chembl_target(gene: str) -> dict[str, Any]:
    def fetch():
        return get_json("https://www.ebi.ac.uk/chembl/api/data/target/search.json", {"q": gene, "limit": 20})

    try:
        data = cached_json(f"chembl_target_{gene}.json", fetch)
    except Exception as exc:
        return {"gene": gene, "chembl_status": "api_error", "chembl_error": f"{type(exc).__name__}: {exc}"}
    hits = []
    for target in data.get("targets", []):
        symbols: set[str] = set()
        accessions: set[str] = set()
        for comp in target.get("target_components") or []:
            if comp.get("accession"):
                accessions.add(comp["accession"])
            for syn in comp.get("target_component_synonyms") or []:
                if syn.get("syn_type") == "GENE_SYMBOL" and syn.get("component_synonym"):
                    symbols.add(syn["component_synonym"].upper())
        hits.append(
            {
                "target_chembl_id": target.get("target_chembl_id", ""),
                "pref_name": target.get("pref_name", ""),
                "target_type": target.get("target_type", ""),
                "organism": target.get("organism", ""),
                "accessions": ";".join(sorted(accessions)),
                "gene_symbols": ";".join(sorted(symbols)),
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
            symbols = set(hit["gene_symbols"].split(";")) if hit["gene_symbols"] else set()
            if gene in symbols and hit["organism"] == "Homo sapiens":
                best = hit
                break
    if best is None:
        return {
            "gene": gene,
            "chembl_status": "not_found_exact",
            "chembl_search_hit_count": len(hits),
            "chembl_url": f"https://www.ebi.ac.uk/chembl/g/#search_results/all/query={quote_plus(gene)}",
        }
    return {
        "gene": gene,
        "chembl_status": "found",
        "chembl_target_chembl_id": best["target_chembl_id"],
        "chembl_target_pref_name": best["pref_name"],
        "chembl_target_type": best["target_type"],
        "chembl_target_organism": best["organism"],
        "chembl_target_accessions": best["accessions"],
        "chembl_search_hit_count": len(hits),
        "chembl_url": f"https://www.ebi.ac.uk/chembl/g/#search_results/all/query={quote_plus(gene)}",
    }


def chembl_activity(target_chembl_id: str | None) -> dict[str, Any]:
    if not target_chembl_id:
        return {"chembl_activity_count": 0, "chembl_activity_values_nM_count": 0}

    def fetch():
        return get_json(
            "https://www.ebi.ac.uk/chembl/api/data/activity.json",
            {"target_chembl_id": target_chembl_id, "standard_units": "nM", "limit": 100},
        )

    try:
        data = cached_json(f"chembl_activity_{target_chembl_id}.json", fetch)
    except Exception as exc:
        return {
            "chembl_activity_count": 0,
            "chembl_activity_values_nM_count": 0,
            "chembl_activity_error": f"{type(exc).__name__}: {exc}",
        }
    activities = data.get("activities", [])
    values = []
    molecules: set[str] = set()
    for act in activities:
        value = safe_num(act.get("standard_value"), default=math.nan)
        if math.isfinite(value):
            values.append(value)
        if act.get("molecule_chembl_id"):
            molecules.add(act["molecule_chembl_id"])
    total = data.get("page_meta", {}).get("total_count", len(activities))
    return {
        "chembl_activity_count": safe_int(total),
        "chembl_activity_values_nM_count": len(values),
        "chembl_unique_molecules_returned": len(molecules),
        "chembl_best_standard_value_nM_returned": min(values) if values else math.nan,
        "chembl_median_standard_value_nM_returned": float(pd.Series(values).median()) if values else math.nan,
    }


def europepmc_count(gene: str) -> dict[str, Any]:
    query = f'"{gene}" AND (autoimmune OR "multiple sclerosis" OR lupus OR psoriasis OR Crohn OR "ulcerative colitis")'

    def fetch():
        return get_json(
            "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
            {"query": query, "format": "json", "pageSize": 3, "resultType": "lite"},
        )

    try:
        data = cached_json(f"europepmc_{gene}.json", fetch)
    except Exception as exc:
        return {"gene": gene, "europepmc_query": query, "europepmc_error": f"{type(exc).__name__}: {exc}"}
    examples = []
    for item in data.get("resultList", {}).get("result", []):
        examples.append(
            {
                "id": item.get("id"),
                "title": item.get("title"),
                "year": item.get("pubYear"),
                "doi": item.get("doi"),
                "source": item.get("source"),
            }
        )
    return {
        "gene": gene,
        "europepmc_query": query,
        "europepmc_hit_count": safe_int(data.get("hitCount")),
        "europepmc_examples_json": json.dumps(examples, sort_keys=True),
        "europepmc_url": f"https://europepmc.org/search?query={quote_plus(query)}",
    }


def clinical_trials_count(gene: str) -> dict[str, Any]:
    term = f"{gene} autoimmune"

    def fetch():
        return get_json("https://clinicaltrials.gov/api/v2/studies", {"query.term": term, "pageSize": 5, "format": "json"})

    try:
        data = cached_json(f"clinicaltrials_{gene}.json", fetch)
    except Exception as exc:
        return {"gene": gene, "clinicaltrials_query": term, "clinicaltrials_error": f"{type(exc).__name__}: {exc}"}
    studies = []
    for st in data.get("studies", []):
        protocol = st.get("protocolSection", {})
        ident = protocol.get("identificationModule", {})
        status = protocol.get("statusModule", {})
        cond = protocol.get("conditionsModule", {})
        studies.append(
            {
                "nct_id": ident.get("nctId"),
                "title": ident.get("briefTitle"),
                "status": status.get("overallStatus"),
                "conditions": cond.get("conditions", []),
            }
        )
    return {
        "gene": gene,
        "clinicaltrials_query": term,
        "clinicaltrials_hit_count": safe_int(data.get("totalCount", len(studies))),
        "clinicaltrials_examples_json": json.dumps(studies, sort_keys=True),
        "clinicaltrials_url": f"https://clinicaltrials.gov/search?term={quote_plus(term)}",
    }


def load_prior_flags() -> dict[str, list[str]]:
    flags: dict[str, list[str]] = {}

    def add(gene: str, flag: str) -> None:
        gene = clean_symbol(gene)
        if gene:
            flags.setdefault(gene, []).append(flag)

    for gene, reason in PRIOR_CLASS_EXCLUSIONS.items():
        add(gene, reason)

    wave18 = read_tsv(WAVE18)
    if not wave18.empty:
        for _, row in wave18.iterrows():
            gene = clean_symbol(row.get("gene"))
            call = str(row.get("wave18_call", ""))
            reason = str(row.get("wave18_call_reason", ""))
            if gene:
                add(gene, f"Wave18 accessible-target rescue: {call}; {reason[:220]}")

    wave21 = read_tsv(WAVE21)
    if not wave21.empty:
        for _, row in wave21.iterrows():
            gene = clean_symbol(row.get("gene"))
            call = str(row.get("gate_call", ""))
            reason = str(row.get("gate_reason", ""))
            if gene and call and call != "GO_REVIEW":
                add(gene, f"Wave21 residual-druggability: {call}; {reason[:220]}")

    wave21_prior = read_tsv(WAVE21_PRIOR)
    if not wave21_prior.empty:
        for _, row in wave21_prior.iterrows():
            gene = clean_symbol(row.get("candidate"))
            rec = str(row.get("recommendation", ""))
            if gene:
                add(gene, f"Wave21 prior-art review: {rec[:220]}")

    wave25 = read_tsv(WAVE25)
    if not wave25.empty:
        for _, row in wave25.iterrows():
            gene = clean_symbol(row.get("gene"))
            call = str(row.get("proxy_call", ""))
            if gene and "NOT_GENETICALLY" in call:
                add(gene, f"Wave25 causal proxy: {call}")

    wave34 = read_tsv(WAVE34)
    if not wave34.empty:
        for _, row in wave34.iterrows():
            gene = clean_symbol(row.get("gene"))
            call = str(row.get("wave34_call", ""))
            blocker = str(row.get("primary_blocker", ""))
            if gene and call.startswith("NO_GO"):
                add(gene, f"Wave34 genetics/druggability: {call}; {blocker}")

    wave38 = read_tsv(WAVE38)
    if not wave38.empty:
        for _, row in wave38.iterrows():
            gene = clean_symbol(row.get("gene_symbol") or row.get("gene"))
            call = str(row.get("wave38_call", ""))
            failures = str(row.get("gate_failures", ""))
            if gene and call:
                add(gene, f"Wave38 CRISPR rescue: {call}; {failures[:220]}")

    if WAVE22_SUMMARY.exists():
        try:
            summary = json.loads(WAVE22_SUMMARY.read_text(encoding="utf-8"))
            add("SQLE", f"Wave22 fail-fast: {summary.get('call', 'NO_GO')}")
        except Exception:
            pass

    return flags


def local_surface_metrics(genes: list[str]) -> pd.DataFrame:
    surface = read_tsv(SURFACE_W15)
    if surface.empty:
        return pd.DataFrame({"gene": genes})
    surface["gene"] = surface["gene"].map(clean_symbol)
    keep = [
        "gene",
        "family",
        "n_delta_fdr10_positive_diseases",
        "n_delta_trend_or_better_diseases",
        "n_delta_negative_trend_diseases",
        "n_state_resid_non_ifn_r_ge_0_35_diseases",
        "n_confounder_dominant_diseases",
        "rank_score",
        "go_no_go",
        "demotion_or_support_reason",
    ]
    return surface[[c for c in keep if c in surface.columns]].drop_duplicates("gene")


def classify_candidate(row: pd.Series) -> tuple[str, str, float]:
    gene = row["gene"]
    failures: list[str] = []
    notes: list[str] = []
    score = 0.0

    pos_diseases = safe_int(row.get("positive_disease_count"))
    neg_diseases = safe_int(row.get("negative_disease_count"))
    ms_anchor = bool(row.get("has_ms_anchor"))
    accessible = bool(row.get("uniprot_accessible", False))
    enzymatic = bool(row.get("uniprot_enzymatic_or_catalytic", False))
    activity_count = safe_int(row.get("chembl_activity_count"))
    chembl_found = str(row.get("chembl_status", "")).startswith("found")
    prior_flags = str(row.get("prior_flags", ""))
    europe = safe_int(row.get("europepmc_hit_count"))
    trials = safe_int(row.get("clinicaltrials_hit_count"))
    surface_resid = safe_int(row.get("n_state_resid_non_ifn_r_ge_0_35_diseases"))
    surface_conf = safe_int(row.get("n_confounder_dominant_diseases"))

    score += pos_diseases * 2.0
    score += 2.0 if ms_anchor else 0.0
    score += 2.0 if accessible else 0.0
    score += 1.5 if enzymatic else 0.0
    score += min(activity_count, 500) / 100.0
    score += min(surface_resid, 5) * 0.75
    score -= neg_diseases * 1.5
    score -= min(surface_conf, 5) * 0.5
    score -= 3.0 if prior_flags else 0.0
    score -= 3.0 if europe >= 2000 else (1.5 if europe >= 500 else 0.0)
    score -= 2.0 if trials > 0 else 0.0

    if pos_diseases < 5 and not (pos_diseases >= 4 and ms_anchor):
        failures.append("insufficient_breadth")
    if not ms_anchor:
        failures.append("no_ms_anchor")
    if not accessible:
        failures.append("not_surface_secreted_extracellular_by_uniprot")
    if not chembl_found and activity_count == 0 and not accessible:
        failures.append("no_druggability_route")
    if prior_flags:
        failures.append("prior_demoted_or_class_blocked")
    if gene in GENERIC_IFN or gene in GENERIC_CYTOKINE_CHEMOKINE:
        failures.append("generic_ifn_cytokine_or_chemokine_axis")
    if gene in CORE_MACHINERY or gene in PROTEASOME_CORE or gene.startswith(CORE_PREFIXES):
        failures.append("core_machinery_or_hla_marker")
    if neg_diseases > 0:
        failures.append("directional_negative_disease_signal")
    if europe >= 2000 or trials > 0:
        failures.append("prior_art_or_trial_saturation")
    if surface_conf >= 4:
        failures.append("surface_state_confounder_dominant")

    if accessible:
        notes.append("reachable protein class by UniProt location/features")
    if chembl_found:
        notes.append("ChEMBL exact target found")
    if activity_count > 0:
        notes.append(f"ChEMBL activity records: {activity_count}")
    if surface_resid > 0:
        notes.append(f"Wave15 residual state support in {surface_resid} diseases")

    hard_failures = set(failures)
    if not hard_failures and score >= 11:
        return "GO_REVIEW", "; ".join(notes), score
    if accessible and ms_anchor and pos_diseases >= 4 and len(hard_failures) <= 2:
        return "PARK_REVIEW", "; ".join(failures + notes), score
    return "NO_GO_SURFACEOME_RESCUE", "; ".join(failures + notes), score


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    broad_pool = load_broad_pool()
    broad_pool.to_csv(OUT / "candidate_pool_pre_api.tsv", sep="\t", index=False)
    genes = broad_pool["gene"].drop_duplicates().tolist()

    uniprot_rows = [uniprot_for_gene(gene) for gene in genes]
    uniprot = pd.DataFrame(uniprot_rows)
    uniprot.to_csv(OUT / "uniprot_accessibility.tsv", sep="\t", index=False)

    merged = broad_pool.merge(uniprot, on="gene", how="left")
    surface = local_surface_metrics(genes)
    if not surface.empty:
        merged = merged.merge(surface, on="gene", how="left")

    # Limit external druggability and prior-art calls to the reachable or
    # otherwise high-priority subset; unreached genes are already no-go.
    external_subset = merged.loc[
        merged.get("uniprot_accessible", False).fillna(False)
        | merged.get("uniprot_enzymatic_or_catalytic", False).fillna(False)
        | merged["has_ms_anchor"].fillna(False)
    ].copy()
    external_subset = external_subset.sort_values(
        ["positive_disease_count", "has_ms_anchor", "discovery_priority_score"],
        ascending=[False, False, False],
    ).head(90)
    ext_genes = external_subset["gene"].tolist()

    chembl_rows = []
    for gene in ext_genes:
        target = exact_chembl_target(gene)
        activity = chembl_activity(target.get("chembl_target_chembl_id"))
        target.update(activity)
        chembl_rows.append(target)
    chembl = pd.DataFrame(chembl_rows)
    chembl.to_csv(OUT / "chembl_druggability.tsv", sep="\t", index=False)
    if not chembl.empty:
        merged = merged.merge(chembl, on="gene", how="left")

    # Literature/trial counts are run only after chemistry/accessibility
    # filtering to avoid confusing generic mentions with candidate evidence.
    prior_subset = merged.loc[
        merged.get("uniprot_accessible", False).fillna(False)
        | merged.get("chembl_status", "").fillna("").astype(str).str.startswith("found")
    ].copy()
    prior_subset = prior_subset.sort_values(
        ["positive_disease_count", "has_ms_anchor", "discovery_priority_score"],
        ascending=[False, False, False],
    ).head(60)
    prior_genes = prior_subset["gene"].tolist()

    epmc = pd.DataFrame([europepmc_count(gene) for gene in prior_genes])
    trials = pd.DataFrame([clinical_trials_count(gene) for gene in prior_genes])
    epmc.to_csv(OUT / "europepmc_prior_counts.tsv", sep="\t", index=False)
    trials.to_csv(OUT / "clinicaltrials_prior_counts.tsv", sep="\t", index=False)
    if not epmc.empty:
        merged = merged.merge(epmc, on="gene", how="left")
    if not trials.empty:
        merged = merged.merge(trials, on="gene", how="left")

    flags = load_prior_flags()
    merged["prior_flags"] = merged["gene"].map(lambda g: " | ".join(flags.get(g, [])))
    merged["google_patents_url"] = merged["gene"].map(
        lambda g: f"https://patents.google.com/?q={quote_plus(str(g) + ' autoimmune antibody inhibitor agonist')}"
    )

    calls = merged.apply(classify_candidate, axis=1)
    merged["wave39_call"] = [x[0] for x in calls]
    merged["wave39_reason"] = [x[1] for x in calls]
    merged["wave39_score"] = [x[2] for x in calls]
    merged = merged.sort_values(
        ["wave39_call", "wave39_score", "positive_disease_count", "has_ms_anchor"],
        ascending=[True, False, False, False],
    ).reset_index(drop=True)

    output_cols = [
        "gene",
        "wave39_call",
        "wave39_score",
        "wave39_reason",
        "positive_disease_count",
        "negative_disease_count",
        "positive_diseases",
        "has_ms_anchor",
        "ms_wm_delta_log2",
        "ms_wm_p",
        "best_positive_p",
        "best_positive_fdr",
        "median_positive_hedges_g",
        "top_positive_compartments",
        "uniprot_status",
        "uniprot_accession",
        "protein_name",
        "uniprot_locations",
        "uniprot_keywords",
        "uniprot_accessible",
        "uniprot_enzymatic_or_catalytic",
        "uniprot_transmembrane_feature_count",
        "chembl_status",
        "chembl_target_chembl_id",
        "chembl_target_pref_name",
        "chembl_activity_count",
        "chembl_best_standard_value_nM_returned",
        "europepmc_hit_count",
        "clinicaltrials_hit_count",
        "family",
        "n_delta_trend_or_better_diseases",
        "n_state_resid_non_ifn_r_ge_0_35_diseases",
        "n_confounder_dominant_diseases",
        "go_no_go",
        "demotion_or_support_reason",
        "prior_flags",
        "europepmc_url",
        "clinicaltrials_url",
        "chembl_url",
        "google_patents_url",
        "function_excerpt",
    ]
    existing_cols = [c for c in output_cols if c in merged.columns]
    merged[existing_cols].to_csv(OUT / "surfaceome_rescue_rank.tsv", sep="\t", index=False)
    merged.to_csv(OUT / "surfaceome_rescue_rank_full.tsv", sep="\t", index=False)

    call_counts = merged["wave39_call"].value_counts().to_dict()
    top = merged[existing_cols].head(20).copy()
    summary = {
        "seed": SEED,
        "candidate_pool_size": int(len(broad_pool)),
        "uniprot_queried_genes": int(len(genes)),
        "external_druggability_queried_genes": int(len(ext_genes)),
        "prior_art_queried_genes": int(len(prior_genes)),
        "call_counts": call_counts,
        "go_review_genes": merged.loc[merged["wave39_call"].eq("GO_REVIEW"), "gene"].tolist(),
        "park_review_genes": merged.loc[merged["wave39_call"].eq("PARK_REVIEW"), "gene"].head(30).tolist(),
        "top_ranked_genes": top["gene"].tolist(),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report_lines = [
        "# Wave39 Surfaceome Rescue After Resolution Pivot",
        "",
        "## Question",
        "",
        (
            "After the resolution/efferocytosis branch failed, can any broad "
            "cross-autoimmune surface, secreted, extracellular, or enzyme-accessible "
            "candidate survive therapeutic gates?"
        ),
        "",
        "## Scale",
        "",
        f"- Candidate pool from broad h5ad recurrence: {len(broad_pool)} genes.",
        f"- UniProt accessibility queried: {len(genes)} genes.",
        f"- ChEMBL target/activity queried: {len(ext_genes)} genes.",
        f"- Europe PMC and ClinicalTrials.gov prior-art counts queried: {len(prior_genes)} genes.",
        f"- Calls: {json.dumps(call_counts, sort_keys=True)}.",
        "",
        "## Result",
        "",
    ]
    if summary["go_review_genes"]:
        report_lines.append(f"- `GO_REVIEW`: {', '.join(summary['go_review_genes'])}.")
    else:
        report_lines.append("- `GO_REVIEW`: none.")
    if summary["park_review_genes"]:
        report_lines.append(f"- `PARK_REVIEW`: {', '.join(summary['park_review_genes'][:20])}.")
    else:
        report_lines.append("- `PARK_REVIEW`: none.")
    report_lines.extend(
        [
            "",
            "Top-ranked rows are in `surfaceome_rescue_rank.tsv`. This scan is a no-go",
            "unless a row survives breadth, MS-anchor, accessibility, modality, direction,",
            "and non-crowded prior-art gates together.",
            "",
            "## Top Rows",
            "",
        ]
    )
    for _, row in top.head(12).iterrows():
        report_lines.append(
            "- "
            f"`{row.get('gene')}`: {row.get('wave39_call')}, score={safe_num(row.get('wave39_score')):.2f}; "
            f"breadth={safe_int(row.get('positive_disease_count'))}, "
            f"MS_anchor={bool(row.get('has_ms_anchor'))}, "
            f"accessible={bool(row.get('uniprot_accessible'))}; "
            f"{str(row.get('wave39_reason', ''))[:260]}"
        )
    (OUT / "REPORT.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
