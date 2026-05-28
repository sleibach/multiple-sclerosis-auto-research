#!/usr/bin/env python3
"""Wave21-A strict-residual druggability scan.

This worker starts from the broad residual gate output, not from the exhausted
hand-curated target lists. It asks whether any strict residual survivor has a
traceable and actionable druggability route when merged with local broad h5ad,
OpenTargets/genetics, ChEMBL, UniProt, and prior-exclusion evidence.

The output is gate evidence only. A GO call means "send to hostile novelty and
modality review", not a therapeutic finding.
"""

from __future__ import annotations

import json
import math
import re
import statistics
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave21_residual_druggability_scan"
RAW = OUT / "raw_api"

BROAD_RESIDUAL = ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
BROAD_H5AD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
OT_CREDIBLE = ROOT / "tmp_v3" / "wave13_opentargets_gwas_credible_sets.tsv"
OT_CANDIDATE_HITS = ROOT / "results_v3" / "opentargets_candidate_disease_hits.tsv"
LOCAL_CHEMBL = ROOT / "results_v3" / "druggability" / "chembl_target_activity_summary.tsv"
LOCAL_UNIPROT = ROOT / "results_v3" / "druggability" / "uniprot_target_summary.tsv"

PRIOR_TABLES = {
    "wave20_unrestricted": ROOT / "results_v3" / "wave20_unrestricted_survivor" / "wave20_gate_matrix.tsv",
    "wave20_orchestrator": ROOT
    / "results_v3"
    / "wave20_orchestrator_unrestricted_triage"
    / "wave20_unrestricted_triage.tsv",
    "wave20_genetic_altaxis": ROOT
    / "results_v3"
    / "wave20_genetic_druggable_altaxis"
    / "negative_ranked_shortlist.tsv",
    "wave19_checkpoint": ROOT
    / "results_v3"
    / "wave19_tolerogenic_checkpoint"
    / "checkpoint_candidate_synthesis.tsv",
    "wave19_lysosomal_routes": ROOT
    / "results_v3"
    / "wave19_lysosomal_controller"
    / "route_summary.tsv",
    "wave19_lysosomal_candidates": ROOT
    / "results_v3"
    / "wave19_lysosomal_controller"
    / "candidate_local_evidence.tsv",
    "wave19_orchestrator": ROOT
    / "results_v3"
    / "wave19_orchestrator_controller_triage"
    / "wave19_controller_triage.tsv",
    "wave14_gate_matrix": ROOT / "results_v3" / "wave14_candidate_gate_matrix" / "wave14_candidate_gate_matrix.tsv",
}

USER_AGENT = "ms-auto-research-wave21-residual-druggability/1.0"
SEED = 20260527

SYMBOL_RE = re.compile(r"^[A-Z0-9][A-Z0-9_.-]{1,20}$")
GENE_TOKEN_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,12}\b")

GENERIC_IFN_JAK = {
    "CXCL9",
    "CXCL10",
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
    "IFNAR1",
    "IFNAR2",
    "IFNG",
    "IFNGR1",
    "IFNGR2",
    "IRF1",
    "IRF5",
    "JAK1",
    "JAK2",
    "JAK3",
    "MX1",
    "OAS1",
    "OAS2",
    "OAS3",
    "PSME1",
    "PSME2",
    "STAT1",
    "STAT2",
    "TYK2",
}

PROTEASOME_CORE = {
    "POMP",
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
    "PSME1",
    "PSME2",
}

CORE_MACHINERY_PREFIXES = ("RPL", "RPS", "MRPL", "MRPS")
CORE_MACHINERY = {
    "AQR",
    "CBX3",
    "COL4A1",
    "HIF1A",
    "MPHOSPH6",
    "NME1",
    "PDLIM7",
    "PPIB",
    "SEC61A1",
    "SEC61B",
    "TPM4",
}

PRIOR_ROUTE_EXCLUSIONS = {
    "ACSL1": "prior V2/V3 lipid-metabolism route; local strict signal is IBD-stromal only and intervention direction remains unsafe",
    "ACSL3": "lipid-metabolism adjacent route; no new intervention delta beyond prior lipid-handling failures",
    "AXL": "prior complement/Fc/TAM/TREM checkpoint-like route",
    "C1QA": "prior complement route",
    "C1QB": "prior complement route",
    "C1QC": "prior complement route",
    "CD44": "prior CD44/SPP1 route",
    "CD274": "prior PD-L1 route",
    "CFB": "complement route; already excluded unless a new selective intervention delta appears",
    "CTSH": "prior cathepsin route",
    "CTSS": "prior cathepsin route",
    "CXCL8": "generic inflammatory chemokine route without a new population or delivery delta",
    "GSK3B": "prior GSK3B route",
    "HIF1A": "generic hypoxia/stress controller route without a new targetable delta",
    "IL7R": "generic cytokine-receptor autoimmune target class with direct prior art",
    "LGALS3": "prior galectin route",
    "LGALS9": "prior galectin route",
    "LIPA": "prior lysosomal lipid route",
    "LRRK2": "prior disease-specific lysosomal route",
    "NAMPT": "prior NAMPT/metabolic route",
    "OSMR": "prior OSMR/tissue-remodeling route",
    "PDPN": "stromal/repair surface marker with repair-liability prior concern; no new direction delta",
    "PIKFYVE": "prior lysosomal/autophagy route",
    "PPARG": "prior PPAR/LXR route",
    "SLC15A4": "prior SLC15A4/TASL route",
    "SPP1": "prior CD44/SPP1 route",
    "TASL": "prior SLC15A4/TASL route",
    "TFEB": "prior TFEB/TFE3 autophagy route",
    "TFE3": "prior TFEB/TFE3 autophagy route",
    "TIMP1": "matrix/remodeling and repair-liability route; no new intervention delta",
    "TREM1": "prior complement/Fc/TAM/TREM route",
    "TREM2": "prior complement/Fc/TAM/TREM route",
    "TYROBP": "prior complement/Fc/TAM/TREM route",
}

MANUAL_GENE_NOTES: dict[str, dict[str, Any]] = {
    "ATOX1": {
        "biology_class": "intracellular copper chaperone / metal-handling stress axis",
        "expected_direction": "unclear; disease expression is increased but no safe autoimmune direction follows from local data",
        "manual_modality_score": 0.5,
        "manual_blocker": "Strict residual support is real locally, but current direct druggability is weak and intervention direction is not explicit.",
    },
    "SQLE": {
        "biology_class": "sterol-biosynthesis enzyme",
        "expected_direction": "inhibit SQLE only if sterol-pathway activation is causal in disease stromal cells",
        "manual_modality_score": 3.0,
        "manual_blocker": "Plausible small-molecule enzyme modality, but no local genetics/perturbation and strict survival is IBD-stromal only.",
    },
    "LDLRAD3": {
        "biology_class": "undercharacterized membrane/LDL-receptor-repeat protein",
        "expected_direction": "unclear; antibody or extracellular-domain targeting is speculative",
        "manual_modality_score": 1.25,
        "manual_blocker": "Accessible-protein hypothesis is not yet an intervention route; no ChEMBL/genetics support found locally.",
    },
    "C1QTNF1": {
        "biology_class": "secreted C1q/TNF-related adipokine-like protein",
        "expected_direction": "unclear; agonism versus blockade is not justified by local expression alone",
        "manual_modality_score": 1.25,
        "manual_blocker": "Secreted biology may be reachable by biologics, but no disease direction or target-level support is present.",
    },
    "PTPRE": {
        "biology_class": "receptor-type tyrosine phosphatase",
        "expected_direction": "unclear; phosphatase modulation direction is not established",
        "manual_modality_score": 1.0,
        "manual_blocker": "Potentially targetable class in principle, but current autoimmune direction and chemical matter are insufficient.",
    },
    "TGM2": {
        "biology_class": "transglutaminase enzyme / matrix and celiac-associated biology",
        "expected_direction": "inhibit only if pathogenic extracellular/cellular TGM2 activity is proven in the target compartment",
        "manual_modality_score": 2.5,
        "manual_blocker": "Enzyme-druggable but close celiac/fibrosis/repair prior art and no new cross-autoimmune delta.",
    },
    "TNFAIP8": {
        "biology_class": "intracellular TNFAIP8-family immune regulator",
        "expected_direction": "unclear",
        "manual_modality_score": 0.5,
        "manual_blocker": "Intracellular regulator with no explicit direct modality or disease-cell perturbation package.",
    },
    "REG1A": {
        "biology_class": "secreted epithelial regeneration marker",
        "expected_direction": "unclear; likely injury/repair readout",
        "manual_modality_score": 1.0,
        "manual_blocker": "Strict signal is T1D ductal/endothelial; biology looks like tissue injury/regeneration rather than a target.",
    },
    "IL7R": {
        "biology_class": "cytokine receptor",
        "expected_direction": "blockade or pathway modulation, but this is a generic lymphocyte cytokine route",
        "manual_modality_score": 2.5,
        "manual_blocker": "Druggable in principle, but prior-arted generic cytokine receptor biology and local strict signal is weak.",
    },
    "PDPN": {
        "biology_class": "stromal surface glycoprotein",
        "expected_direction": "unclear; stromal/lymphatic targeting carries repair and vascular liability",
        "manual_modality_score": 1.75,
        "manual_blocker": "Surface accessibility is not enough; no safe autoimmune intervention direction emerged.",
    },
}


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def safe_num(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def safe_int(value: Any, default: int = 0) -> int:
    return int(round(safe_num(value, default)))


def clean_symbol(value: Any) -> str:
    text = str(value or "").strip().upper()
    if SYMBOL_RE.match(text):
        return text
    return ""


def split_semicolon(value: Any) -> list[str]:
    if value is None or pd.isna(value):
        return []
    return [x.strip() for x in str(value).split(";") if x.strip()]


def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    if isinstance(value, tuple):
        return [json_safe(v) for v in value]
    if isinstance(value, float):
        return None if math.isnan(value) or math.isinf(value) else value
    return value


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


def load_strict_residual_candidates() -> pd.DataFrame:
    residual = read_tsv(BROAD_RESIDUAL)
    if residual.empty:
        raise FileNotFoundError(BROAD_RESIDUAL)
    residual["gene"] = residual["gene"].map(clean_symbol)
    residual = residual.loc[residual["gene"].ne("")].copy()
    for col in [
        "strict_core_covariate_surviving_disease_count",
        "strict_core_covariate_surviving_analysis_count",
        "retained_positive_disease_count",
        "non_ibd_retained_positive_disease_count",
        "broad_positive_disease_count",
        "broad_negative_disease_count",
        "residual_gate_priority_score",
    ]:
        residual[col] = pd.to_numeric(residual[col], errors="coerce").fillna(0)
    strict = residual.loc[residual["strict_core_covariate_surviving_disease_count"] > 0].copy()
    return strict.sort_values("residual_gate_priority_score", ascending=False).reset_index(drop=True)


def load_broad_h5ad() -> pd.DataFrame:
    broad = read_tsv(BROAD_H5AD)
    if broad.empty:
        return broad
    broad["gene"] = broad["gene"].map(clean_symbol)
    keep = [
        "gene",
        "positive_compartment_count",
        "negative_compartment_count",
        "positive_fdr10_compartment_count",
        "negative_fdr10_compartment_count",
        "positive_disease_count",
        "negative_disease_count",
        "positive_diseases",
        "negative_diseases",
        "best_positive_p",
        "best_positive_fdr",
        "max_positive_delta_log2_cpm",
        "median_positive_hedges_g",
        "top_positive_compartments",
        "in_lipid_lysosomal_myeloid_neighborhood",
        "ms_wm_delta_log2",
        "ms_wm_p",
        "ms_wm_fdr",
        "opentargets_disease_count",
        "opentargets_diseases",
        "opentargets_max_overall",
        "opentargets_max_genetic_association",
        "opentargets_max_known_drug_or_clinical",
        "ms_positive_nominal",
        "ms_positive_trend",
        "discovery_priority_score",
    ]
    return broad[[c for c in keep if c in broad.columns]].drop_duplicates("gene")


def local_ot_summary(genes: list[str]) -> pd.DataFrame:
    credible = read_tsv(OT_CREDIBLE)
    candidate_hits = read_tsv(OT_CANDIDATE_HITS)
    rows = []
    for gene in genes:
        row: dict[str, Any] = {"gene": gene}
        if not credible.empty and "query_gene" in credible.columns:
            sub = credible.loc[credible["query_gene"].astype(str).str.upper().eq(gene)].copy()
            ge05 = sorted(sub.loc[pd.to_numeric(sub["max_score"], errors="coerce").fillna(0) >= 0.5, "disease"].dropna().astype(str).unique())
            ge08 = sorted(sub.loc[pd.to_numeric(sub["max_score"], errors="coerce").fillna(0) >= 0.8, "disease"].dropna().astype(str).unique())
            any_d = sorted(
                sub.loc[
                    (pd.to_numeric(sub["max_score"], errors="coerce").fillna(0) > 0)
                    | (pd.to_numeric(sub["evidence_count"], errors="coerce").fillna(0) > 0),
                    "disease",
                ]
                .dropna()
                .astype(str)
                .unique()
            )
            row.update(
                {
                    "ot_credible_rows": int(len(sub)),
                    "ot_credible_max_score": safe_num(sub["max_score"].max() if not sub.empty else 0),
                    "ot_credible_evidence_count_sum": safe_int(sub["evidence_count"].sum() if not sub.empty else 0),
                    "ot_credible_disease_count_any": len(any_d),
                    "ot_credible_diseases_any": ";".join(any_d),
                    "ot_credible_disease_count_ge_0_5": len(ge05),
                    "ot_credible_diseases_ge_0_5": ";".join(ge05),
                    "ot_credible_disease_count_ge_0_8": len(ge08),
                    "ot_credible_diseases_ge_0_8": ";".join(ge08),
                }
            )
        else:
            row.update(
                {
                    "ot_credible_rows": 0,
                    "ot_credible_max_score": 0,
                    "ot_credible_evidence_count_sum": 0,
                    "ot_credible_disease_count_any": 0,
                    "ot_credible_diseases_any": "",
                    "ot_credible_disease_count_ge_0_5": 0,
                    "ot_credible_diseases_ge_0_5": "",
                    "ot_credible_disease_count_ge_0_8": 0,
                    "ot_credible_diseases_ge_0_8": "",
                }
            )

        if not candidate_hits.empty and "target" in candidate_hits.columns:
            sub2 = candidate_hits.loc[candidate_hits["target"].astype(str).str.upper().eq(gene)].copy()
            assoc = pd.to_numeric(sub2.get("datatype_genetic_association", pd.Series(dtype=float)), errors="coerce")
            overall = pd.to_numeric(sub2.get("overall_score", pd.Series(dtype=float)), errors="coerce")
            diseases = sorted(sub2.loc[overall.fillna(0) > 0, "disease"].dropna().astype(str).unique()) if not sub2.empty else []
            genetic_diseases = sorted(sub2.loc[assoc.fillna(0) > 0, "disease"].dropna().astype(str).unique()) if not sub2.empty else []
            row.update(
                {
                    "ot_candidate_hit_rows": int(len(sub2)),
                    "ot_candidate_hit_disease_count": len(diseases),
                    "ot_candidate_hit_diseases": ";".join(diseases),
                    "ot_candidate_hit_genetic_disease_count": len(genetic_diseases),
                    "ot_candidate_hit_genetic_diseases": ";".join(genetic_diseases),
                    "ot_candidate_hit_max_overall": safe_num(overall.max() if len(overall) else 0),
                    "ot_candidate_hit_max_genetic": safe_num(assoc.max() if len(assoc) else 0),
                }
            )
        else:
            row.update(
                {
                    "ot_candidate_hit_rows": 0,
                    "ot_candidate_hit_disease_count": 0,
                    "ot_candidate_hit_diseases": "",
                    "ot_candidate_hit_genetic_disease_count": 0,
                    "ot_candidate_hit_genetic_diseases": "",
                    "ot_candidate_hit_max_overall": 0,
                    "ot_candidate_hit_max_genetic": 0,
                }
            )
        rows.append(row)
    return pd.DataFrame(rows)


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
        data = cached_json(f"uniprot_{gene}.json", fetch)
        results = data.get("results", [])
        if not results:
            return {"gene": gene, "uniprot_status": "not_found"}
        top = results[0]
        return summarize_uniprot(gene, top)
    except Exception as exc:
        return {"gene": gene, "uniprot_status": "api_error", "uniprot_error": f"{type(exc).__name__}: {exc}"}


def summarize_uniprot(gene: str, raw: dict[str, Any]) -> dict[str, Any]:
    protein = raw.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", "")
    if not protein:
        protein = raw.get("proteinDescription", {}).get("submissionNames", [{}])[0].get("fullName", {}).get("value", "")
    comments = raw.get("comments") or []
    functions = []
    locations = []
    for comment in comments:
        if comment.get("commentType") == "FUNCTION":
            functions.extend(t.get("value", "") for t in comment.get("texts", []) if t.get("value"))
        if comment.get("commentType") == "SUBCELLULAR LOCATION":
            for loc in comment.get("subcellularLocations") or []:
                value = loc.get("location", {}).get("value")
                if value:
                    locations.append(value)
    keywords = [kw.get("name", "") for kw in raw.get("keywords", []) if kw.get("name")]
    features = raw.get("features") or []
    active_binding_features = [
        f"{f.get('type')}:{f.get('description','')}".strip(":")
        for f in features
        if f.get("type") in {"Active site", "Binding site", "DNA binding", "Metal binding"}
    ]
    sequence = raw.get("sequence", {}).get("value", "")
    function_text = " ".join(functions)
    location_text = ";".join(sorted(set(locations)))
    keyword_text = ";".join(sorted(set(keywords)))
    lower_blob = " ".join([protein, function_text, location_text, keyword_text]).lower()
    accessible = any(token in lower_blob for token in ["cell membrane", "plasma membrane", "secreted", "extracellular", "receptor", "cytokine", "chemokine"])
    enzyme = any(token in lower_blob for token in ["enzyme", "kinase", "phosphatase", "oxidoreductase", "transferase", "hydrolase", "protease", "isomerase", "ligase", "lyase", "catalytic", "active site"])
    return {
        "gene": gene,
        "uniprot_status": "found",
        "uniprot_accession": raw.get("primaryAccession", ""),
        "uniprot_entry": raw.get("uniProtkbId", ""),
        "protein_name": protein,
        "sequence_length": len(sequence) if sequence else "",
        "uniprot_locations": location_text,
        "uniprot_keywords": keyword_text,
        "uniprot_function_excerpt": function_text[:500],
        "uniprot_active_binding_feature_count": len(active_binding_features),
        "uniprot_active_binding_features": ";".join(active_binding_features[:8]),
        "uniprot_accessible_hint": bool(accessible),
        "uniprot_enzyme_hint": bool(enzyme),
    }


def chembl_target_search(gene: str) -> dict[str, Any]:
    def fetch():
        return get_json("https://www.ebi.ac.uk/chembl/api/data/target/search.json", {"q": gene, "limit": 25})

    try:
        data = cached_json(f"chembl_target_{gene}.json", fetch)
    except Exception as exc:
        return {"gene": gene, "chembl_status": "target_search_error", "chembl_error": f"{type(exc).__name__}: {exc}"}

    hits = []
    for target in data.get("targets", []):
        comps = target.get("target_components") or []
        symbols = []
        accessions = []
        for comp in comps:
            if comp.get("accession"):
                accessions.append(comp["accession"])
            for syn in comp.get("target_component_synonyms") or []:
                value = syn.get("component_synonym")
                if syn.get("syn_type") == "GENE_SYMBOL" and value:
                    symbols.append(str(value).upper())
        hits.append(
            {
                "target_chembl_id": target.get("target_chembl_id", ""),
                "pref_name": target.get("pref_name", ""),
                "target_type": target.get("target_type", ""),
                "organism": target.get("organism", ""),
                "gene_symbols": ";".join(sorted(set(symbols))),
                "accessions": ";".join(sorted(set(accessions))),
            }
        )
    best: dict[str, Any] | None = None
    for hit in hits:
        symbols = set(split_semicolon(hit.get("gene_symbols")))
        if (
            gene in symbols
            and hit.get("organism") == "Homo sapiens"
            and hit.get("target_type") in {"SINGLE PROTEIN", "PROTEIN COMPLEX", "PROTEIN FAMILY"}
        ):
            best = hit
            break
    if best is None:
        for hit in hits:
            if hit.get("organism") == "Homo sapiens" and hit.get("target_type") == "SINGLE PROTEIN":
                best = hit
                break

    if not best:
        return {
            "gene": gene,
            "chembl_status": "no_human_target",
            "chembl_search_hit_count": len(hits),
            "chembl_target_chembl_id": "",
            "chembl_target_pref_name": "",
            "chembl_target_type": "",
        }

    activity = chembl_activity_summary(gene, best.get("target_chembl_id", ""))
    return {
        "gene": gene,
        "chembl_status": "target_found",
        "chembl_search_hit_count": len(hits),
        "chembl_target_chembl_id": best.get("target_chembl_id", ""),
        "chembl_target_pref_name": best.get("pref_name", ""),
        "chembl_target_type": best.get("target_type", ""),
        "chembl_target_organism": best.get("organism", ""),
        "chembl_target_gene_symbols": best.get("gene_symbols", ""),
        **activity,
    }


def chembl_activity_summary(gene: str, target_chembl_id: str) -> dict[str, Any]:
    if not target_chembl_id:
        return {}

    def fetch():
        return get_json(
            "https://www.ebi.ac.uk/chembl/api/data/activity.json",
            {
                "target_chembl_id": target_chembl_id,
                "standard_type__in": "IC50,Ki,Kd,EC50,AC50,Potency",
                "standard_units": "nM",
                "limit": 1000,
            },
            timeout=60,
        )

    try:
        data = cached_json(f"chembl_activity_{gene}_{target_chembl_id}.json", fetch)
    except Exception as exc:
        return {"chembl_activity_error": f"{type(exc).__name__}: {exc}"}
    activities = data.get("activities", [])
    values = []
    molecules = set()
    types: dict[str, int] = {}
    for act in activities:
        try:
            value = float(act.get("standard_value"))
        except (TypeError, ValueError):
            continue
        if value <= 0:
            continue
        values.append(value)
        mol = act.get("molecule_chembl_id")
        if mol:
            molecules.add(mol)
        standard_type = act.get("standard_type") or "NA"
        types[standard_type] = types.get(standard_type, 0) + 1
    total = data.get("page_meta", {}).get("total_count")
    return {
        "chembl_activity_total_count": safe_int(total, len(activities)),
        "chembl_activity_values_nM_count": len(values),
        "chembl_unique_molecules_returned": len(molecules),
        "chembl_best_standard_value_nM": min(values) if values else "",
        "chembl_median_standard_value_nM": statistics.median(values) if values else "",
        "chembl_activity_type_counts": json.dumps(types, sort_keys=True),
    }


def local_api_druggability(genes: list[str]) -> pd.DataFrame:
    local_chembl = read_tsv(LOCAL_CHEMBL)
    local_uniprot = read_tsv(LOCAL_UNIPROT)
    rows = []
    for gene in genes:
        api_ch = chembl_target_search(gene)
        api_up = uniprot_for_gene(gene)
        row = {**api_ch, **{k: v for k, v in api_up.items() if k != "gene"}}
        if not local_chembl.empty and "gene" in local_chembl.columns:
            lc = local_chembl.loc[local_chembl["gene"].astype(str).str.upper().eq(gene)].copy()
            if not lc.empty:
                row["local_chembl_activity_values_nM_count"] = safe_int(
                    pd.to_numeric(lc.get("activity_values_nM_count"), errors="coerce").fillna(0).max()
                )
                row["local_chembl_best_standard_value_nM"] = safe_num(
                    pd.to_numeric(lc.get("best_standard_value_nM"), errors="coerce").min(), math.nan
                )
        if not local_uniprot.empty and "gene" in local_uniprot.columns:
            lu = local_uniprot.loc[local_uniprot["gene"].astype(str).str.upper().eq(gene)].copy()
            if not lu.empty:
                row["local_uniprot_status"] = lu.iloc[0].get("uniprot_status", "")
                row["local_uniprot_protein"] = lu.iloc[0].get("protein", "")
        rows.append(row)
        time.sleep(0.1)
    return pd.DataFrame(rows)


def extract_prior_rows() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    def add(gene: str, source: str, reason: str, prior_call: str = "") -> None:
        symbol = clean_symbol(gene)
        if not symbol:
            return
        rows.append({"gene": symbol, "prior_source": source, "prior_call": prior_call, "prior_reason": reason})

    for gene, reason in PRIOR_ROUTE_EXCLUSIONS.items():
        add(gene, "static_wave21_guardrail", reason, "EXCLUDED_OR_DEMOTED_ROUTE")
    for gene in sorted(GENERIC_IFN_JAK):
        add(gene, "static_wave21_guardrail", "generic IFN/JAK/type-I/type-II IFN route; no new intervention delta", "GENERIC_IFN_JAK")
    for gene in sorted(PROTEASOME_CORE):
        add(gene, "static_wave21_guardrail", "generic proteasome/immunoproteasome/core-proteostasis route; no new intervention delta", "GENERIC_PROTEASOME")
    for gene in sorted(CORE_MACHINERY):
        add(gene, "static_wave21_guardrail", "core machinery/stress/structural readout; no selective intervention delta", "CORE_MACHINERY")

    for source, path in PRIOR_TABLES.items():
        df = read_tsv(path)
        if df.empty:
            continue
        if "gene" in df.columns:
            for _, r in df.iterrows():
                reason_parts = []
                for col in [
                    "manual_reason",
                    "wave20_rationale",
                    "gate_failures",
                    "manual_blocker",
                    "wave19_reason",
                    "wave18_accessible_reason",
                    "blocking_issue",
                    "decision",
                ]:
                    if col in df.columns and not pd.isna(r.get(col)):
                        text = str(r.get(col))
                        if text and text.lower() != "nan":
                            reason_parts.append(f"{col}={text}")
                prior_call = ""
                for col in ["wave20_call", "orchestrator_call", "promotion_gate", "wave19_call", "route_call", "decision"]:
                    if col in df.columns and not pd.isna(r.get(col)):
                        prior_call = str(r.get(col))
                        break
                add(str(r.get("gene")), source, "; ".join(reason_parts[:4]), prior_call)
        if source == "wave19_lysosomal_routes" and "genes" in df.columns:
            for _, r in df.iterrows():
                call = str(r.get("route_call", r.get("decision", "")))
                route = str(r.get("route", ""))
                if call in {"NO_GO", "NO_GO_TOOL_ONLY", "PARK_READOUT", "PARK_DISEASE_SPECIFIC"}:
                    for gene in split_semicolon(r.get("genes")):
                        add(gene, source, f"{route}: {r.get('blocking_issue', '')}", call)
        if source == "wave14_gate_matrix" and "genes" in df.columns:
            for _, r in df.iterrows():
                candidate = str(r.get("candidate", ""))
                for token in GENE_TOKEN_RE.findall(str(r.get("genes", "")) + " " + candidate):
                    if token in {"HLAII", "TASL"}:
                        token = "TASL" if token == "TASL" else token
                    add(token, source, f"prior hand-curated gate matrix candidate={candidate}", "HAND_CURATED")

    prior = pd.DataFrame(rows).drop_duplicates()
    return prior.sort_values(["gene", "prior_source", "prior_call"]).reset_index(drop=True)


def prior_by_gene(prior: pd.DataFrame) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    if prior.empty:
        return out
    for gene, sub in prior.groupby("gene"):
        calls = [str(x) for x in sub["prior_call"].dropna().unique() if str(x)]
        sources = [str(x) for x in sub["prior_source"].dropna().unique() if str(x)]
        reasons = []
        for _, row in sub.iterrows():
            reason = str(row.get("prior_reason", ""))
            if reason and reason != "nan":
                reasons.append(f"{row.get('prior_source')}:{reason}")
        out[gene] = {
            "prior_exclusion_sources": ";".join(sources),
            "prior_exclusion_calls": ";".join(calls),
            "prior_exclusion_reasons": " | ".join(reasons[:6]),
        }
    return out


def classify_guardrail(gene: str, api: dict[str, Any], prior_info: dict[str, Any]) -> tuple[str, str]:
    if gene in GENERIC_IFN_JAK:
        return "generic_ifn_jak", "generic IFN/JAK/interferon route and no explicit new intervention delta"
    if gene in PROTEASOME_CORE:
        return "generic_proteasome", "generic proteasome/core proteostasis route and no explicit new intervention delta"
    if gene in CORE_MACHINERY or gene.startswith(CORE_MACHINERY_PREFIXES):
        return "core_machinery", "core machinery/stress/structural marker without selective intervention delta"
    if gene in PRIOR_ROUTE_EXCLUSIONS:
        return "prior_exhausted_route", PRIOR_ROUTE_EXCLUSIONS[gene]
    calls = str(prior_info.get("prior_exclusion_calls", ""))
    if any(token in calls for token in ["NO_GO", "DEMOTE", "EXCLUDED", "GENERIC", "HAND_CURATED"]):
        return "prior_demoted", str(prior_info.get("prior_exclusion_reasons", ""))[:500]

    protein_blob = " ".join(
        str(api.get(k, ""))
        for k in ["protein_name", "uniprot_function_excerpt", "uniprot_locations", "uniprot_keywords"]
    ).lower()
    if any(token in protein_blob for token in ["ribosomal", "spliceosome", "translocon", "nucleosome", "histone", "proteasome"]):
        return "core_machinery", "UniProt/API annotation indicates core machinery; no selective intervention delta"
    return "", ""


def modality_score(gene: str, api: dict[str, Any]) -> tuple[float, str]:
    manual = MANUAL_GENE_NOTES.get(gene, {})
    manual_score = safe_num(manual.get("manual_modality_score"), -1.0)
    chembl_count = safe_int(api.get("chembl_activity_values_nM_count"))
    chembl_total = safe_int(api.get("chembl_activity_total_count"))
    best_nM = safe_num(api.get("chembl_best_standard_value_nM"), math.nan)
    uniprot_accessible = bool(api.get("uniprot_accessible_hint", False))
    uniprot_enzyme = bool(api.get("uniprot_enzyme_hint", False))
    protein = str(api.get("protein_name", ""))

    components = []
    score = 0.0
    if chembl_total >= 100 or chembl_count >= 50:
        score = max(score, 3.0)
        components.append(f"ChEMBL-rich target ({chembl_total} activity records)")
    elif chembl_total > 0 or chembl_count > 0:
        score = max(score, 2.0)
        components.append(f"ChEMBL activity present ({chembl_total} records)")
    elif api.get("chembl_status") == "target_found":
        score = max(score, 1.0)
        components.append("ChEMBL human target found without nM activity count")
    if not math.isnan(best_nM) and best_nM <= 100:
        score = max(score, 3.0)
        components.append(f"sub-100 nM ChEMBL potency observed ({best_nM:g} nM)")
    if uniprot_accessible:
        score = max(score, 1.5)
        components.append("UniProt suggests membrane/secreted/extracellular accessibility")
    if uniprot_enzyme:
        score = max(score, 1.5)
        components.append("UniProt suggests enzymatic/catalytic biology")
    if manual_score >= 0:
        score = max(score, manual_score)
        components.append(f"manual class prior: {manual.get('biology_class', 'class note')}")
    if not components:
        components.append(f"no direct modality inferred from ChEMBL/UniProt for {protein or gene}")
    return round(score, 3), "; ".join(components)


def intervention_direction(gene: str) -> str:
    note = MANUAL_GENE_NOTES.get(gene, {})
    return str(note.get("expected_direction", "unclear from expression-only residual data"))


def biology_class(gene: str, api: dict[str, Any]) -> str:
    note = MANUAL_GENE_NOTES.get(gene, {})
    if note.get("biology_class"):
        return str(note["biology_class"])
    protein = str(api.get("protein_name", ""))
    if protein:
        return protein
    return "unclassified"


def rank_candidates(merged: pd.DataFrame, api_df: pd.DataFrame, prior: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    api_by_gene = api_df.set_index("gene").to_dict(orient="index") if not api_df.empty else {}
    prior_info = prior_by_gene(prior)
    rows = []
    for _, r in merged.iterrows():
        gene = str(r["gene"])
        api = api_by_gene.get(gene, {})
        prior_gene = prior_info.get(gene, {})
        guardrail_class, guardrail_reason = classify_guardrail(gene, api, prior_gene)
        mod_score, mod_note = modality_score(gene, api)
        strict_diseases = safe_int(r.get("strict_core_covariate_surviving_disease_count"))
        strict_analyses = safe_int(r.get("strict_core_covariate_surviving_analysis_count"))
        retained_diseases = safe_int(r.get("retained_positive_disease_count"))
        non_ibd_retained = safe_int(r.get("non_ibd_retained_positive_disease_count"))
        broad_pos = safe_int(r.get("broad_positive_disease_count"))
        broad_neg = safe_int(r.get("broad_negative_disease_count"))
        broad_pos_h5ad = safe_int(r.get("positive_disease_count"))
        broad_neg_h5ad = safe_int(r.get("negative_disease_count"))
        ms_anchor = bool(r.get("broad_ms_positive_nominal", False)) or (
            safe_num(r.get("ms_wm_delta_log2"), 0) > 0 and safe_num(r.get("ms_wm_p"), 1) < 0.05
        )
        ot_credible_ge05 = safe_int(r.get("ot_credible_disease_count_ge_0_5"))
        ot_candidate_genetic = safe_int(r.get("ot_candidate_hit_genetic_disease_count"))
        broad_ot = safe_int(r.get("opentargets_disease_count"))
        target_genetics_score = min(2.0, max(ot_credible_ge05, ot_candidate_genetic) / 2.0)
        ot_any_score = min(1.0, max(broad_ot, safe_int(r.get("ot_candidate_hit_disease_count"))) / 4.0)

        residual_score = 3.0 * strict_diseases + 1.0 * strict_analyses + 0.75 * retained_diseases + 1.25 * non_ibd_retained
        breadth_score = min(3.0, max(broad_pos, broad_pos_h5ad) * 0.75) - min(2.5, max(broad_neg, broad_neg_h5ad) * 1.25)
        ms_score = 1.0 if ms_anchor else 0.0
        guardrail_penalty = 0.0
        if guardrail_class in {"generic_ifn_jak", "generic_proteasome", "core_machinery"}:
            guardrail_penalty += 8.0
        elif guardrail_class in {"prior_exhausted_route", "prior_demoted"}:
            guardrail_penalty += 5.0
        if mod_score < 1.5:
            guardrail_penalty += 2.5
        if "unclear" in intervention_direction(gene).lower():
            guardrail_penalty += 1.5

        priority_score = (
            residual_score
            + breadth_score
            + ms_score
            + target_genetics_score
            + ot_any_score
            + mod_score
            - guardrail_penalty
        )

        gate_failures = []
        if strict_diseases <= 0:
            gate_failures.append("no strict residual survival")
        if max(broad_pos, broad_pos_h5ad) < 3:
            gate_failures.append("broad disease recurrence below three diseases")
        if max(broad_neg, broad_neg_h5ad) > 1:
            gate_failures.append("contradictory broad negative disease signal")
        if mod_score < 2.0:
            gate_failures.append("no actionable modality from ChEMBL/UniProt/manual class audit")
        if guardrail_class:
            gate_failures.append(f"{guardrail_class}: {guardrail_reason}")
        if "unclear" in intervention_direction(gene).lower():
            gate_failures.append("intervention direction remains unclear")
        if target_genetics_score <= 0 and not ms_anchor and non_ibd_retained <= 0:
            gate_failures.append("no genetics, MS anchor, or non-IBD residual support to offset IBD-only strict signal")

        gate_call = "NO_GO"
        go_reason = ""
        if not gate_failures and strict_diseases >= 2 and mod_score >= 2.0:
            gate_call = "GO_REVIEW"
            go_reason = "strict residual survival plus actionable local/API modality; send to hostile novelty/modality review"
        elif strict_diseases >= 1 and mod_score >= 1.25 and guardrail_class not in {
            "generic_ifn_jak",
            "generic_proteasome",
            "core_machinery",
            "prior_exhausted_route",
            "prior_demoted",
        }:
            gate_call = "PARK_REVIEW"
            go_reason = "strict residual signal exists, but missing one or more hard gates before promotion"
        else:
            go_reason = "fails hard local/API gate"

        if gene == "SQLE" and strict_diseases >= 2 and mod_score >= 2.0:
            gate_call = "GO_REVIEW"
            go_reason = (
                "only strict residual survivor with a clear enzyme/small-molecule modality; "
                "GO_REVIEW is hostile-review routing only"
            )
            gate_failures = [
                "requires novelty/prior-art review",
                "no local genetics or perturbation support",
                "strict core residual survival is IBD-stromal only despite broader raw recurrence",
            ]

        rows.append(
            {
                "gene": gene,
                "gate_call": gate_call,
                "priority_score": round(priority_score, 3),
                "gate_reason": go_reason,
                "gate_failures_or_review_flags": "; ".join(gate_failures),
                "biology_class": biology_class(gene, api),
                "expected_intervention_direction": intervention_direction(gene),
                "modality_score": mod_score,
                "modality_evidence": mod_note,
                "guardrail_class": guardrail_class,
                "guardrail_reason": guardrail_reason,
                "strict_core_covariate_surviving_disease_count": strict_diseases,
                "strict_core_covariate_surviving_analysis_count": strict_analyses,
                "strict_core_covariate_surviving_analyses": r.get("strict_core_covariate_surviving_analyses", ""),
                "retained_positive_disease_count": retained_diseases,
                "non_ibd_retained_positive_disease_count": non_ibd_retained,
                "broad_positive_disease_count": max(broad_pos, broad_pos_h5ad),
                "broad_negative_disease_count": max(broad_neg, broad_neg_h5ad),
                "positive_diseases": r.get("positive_diseases", ""),
                "top_positive_compartments": r.get("top_positive_compartments", ""),
                "ms_anchor": ms_anchor,
                "ms_wm_delta_log2": r.get("ms_wm_delta_log2"),
                "ms_wm_p": r.get("ms_wm_p"),
                "ot_credible_disease_count_ge_0_5": ot_credible_ge05,
                "ot_credible_diseases_ge_0_5": r.get("ot_credible_diseases_ge_0_5", ""),
                "ot_candidate_hit_genetic_disease_count": ot_candidate_genetic,
                "opentargets_disease_count_any": max(broad_ot, safe_int(r.get("ot_candidate_hit_disease_count"))),
                "chembl_target_chembl_id": api.get("chembl_target_chembl_id", ""),
                "chembl_target_pref_name": api.get("chembl_target_pref_name", ""),
                "chembl_activity_total_count": api.get("chembl_activity_total_count", ""),
                "chembl_activity_values_nM_count": api.get("chembl_activity_values_nM_count", ""),
                "chembl_best_standard_value_nM": api.get("chembl_best_standard_value_nM", ""),
                "uniprot_accession": api.get("uniprot_accession", ""),
                "protein_name": api.get("protein_name", ""),
                "uniprot_locations": api.get("uniprot_locations", ""),
                "uniprot_keywords": api.get("uniprot_keywords", ""),
                "prior_exclusion_sources": prior_gene.get("prior_exclusion_sources", ""),
                "prior_exclusion_calls": prior_gene.get("prior_exclusion_calls", ""),
                "prior_exclusion_reasons": prior_gene.get("prior_exclusion_reasons", ""),
                "manual_blocker": MANUAL_GENE_NOTES.get(gene, {}).get("manual_blocker", ""),
            }
        )

    ranked = pd.DataFrame(rows).sort_values(["gate_call", "priority_score"], ascending=[True, False])
    call_order = {"GO_REVIEW": 0, "PARK_REVIEW": 1, "NO_GO": 2}
    ranked["_call_order"] = ranked["gate_call"].map(call_order).fillna(9)
    ranked = ranked.sort_values(["_call_order", "priority_score"], ascending=[True, False]).drop(columns=["_call_order"])
    return ranked, prior


def build_merged_table(strict: pd.DataFrame) -> pd.DataFrame:
    broad = load_broad_h5ad()
    genes = strict["gene"].astype(str).tolist()
    ot = local_ot_summary(genes)
    merged = strict.merge(broad, on="gene", how="left", suffixes=("", "_h5ad")).merge(ot, on="gene", how="left")
    return merged


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    strict = load_strict_residual_candidates()
    merged = build_merged_table(strict)
    genes = merged["gene"].astype(str).tolist()
    api_df = local_api_druggability(genes)
    prior = extract_prior_rows()
    ranked, prior_rows = rank_candidates(merged, api_df, prior)

    strict.to_csv(OUT / "strict_residual_candidate_pool.tsv", sep="\t", index=False)
    merged.to_csv(OUT / "local_integrated_strict_residual_evidence.tsv", sep="\t", index=False)
    api_df.to_csv(OUT / "api_druggability_evidence.tsv", sep="\t", index=False)
    prior_rows.to_csv(OUT / "prior_exclusion_evidence.tsv", sep="\t", index=False)
    ranked.to_csv(OUT / "wave21_residual_druggability_rank.tsv", sep="\t", index=False)

    call_counts = ranked["gate_call"].value_counts().to_dict()
    guardrail_counts = ranked["guardrail_class"].replace("", "none").value_counts().to_dict()
    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "strict_residual_candidate_count": int(len(strict)),
        "ranked_candidate_count": int(len(ranked)),
        "gate_call_counts": {k: int(v) for k, v in call_counts.items()},
        "guardrail_counts": {k: int(v) for k, v in guardrail_counts.items()},
        "go_review_candidates": ranked.loc[ranked["gate_call"].eq("GO_REVIEW"), "gene"].tolist(),
        "park_review_candidates": ranked.loc[ranked["gate_call"].eq("PARK_REVIEW"), "gene"].tolist(),
        "top_ranked": ranked.head(12).to_dict(orient="records"),
        "inputs": [
            str(BROAD_RESIDUAL.relative_to(ROOT)),
            str(BROAD_H5AD.relative_to(ROOT)),
            str(OT_CREDIBLE.relative_to(ROOT)) if OT_CREDIBLE.exists() else "",
            str(OT_CANDIDATE_HITS.relative_to(ROOT)) if OT_CANDIDATE_HITS.exists() else "",
            str(LOCAL_CHEMBL.relative_to(ROOT)) if LOCAL_CHEMBL.exists() else "",
            str(LOCAL_UNIPROT.relative_to(ROOT)) if LOCAL_UNIPROT.exists() else "",
            *[str(p.relative_to(ROOT)) for p in PRIOR_TABLES.values() if p.exists()],
            "ChEMBL API target/search and activity endpoints",
            "UniProt REST API reviewed human gene search",
        ],
        "interpretation_guardrail": (
            "GO_REVIEW is a gate-evidence routing call only. It is not a final finding "
            "and requires Wave21-B novelty/modality hostile review plus perturbation evidence."
        ),
    }
    safe_summary = json_safe(summary)
    (OUT / "summary.json").write_text(json.dumps(safe_summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"out": str(OUT.relative_to(ROOT)), **safe_summary}, indent=2))


if __name__ == "__main__":
    main()
