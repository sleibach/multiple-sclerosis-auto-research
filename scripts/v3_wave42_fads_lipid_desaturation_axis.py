#!/usr/bin/env python3
"""Wave42 genetics-first audit of the FADS1/FADS2 lipid-desaturation axis.

Reason for this branch:
- FADS1/FADS2 surfaced in Wave34 as a genetics-first lipid-relevant locus.
- This route should not be judged mainly by differential expression, because
  a lipid-composition mechanism could be driven by inherited enzyme activity or
  substrate flux rather than disease-cell expression level.

Hard guardrail:
- GWAS Catalog mapped-gene recurrence is locus evidence, not target-level
  causality. Promotion requires direction-resolved genetics, perturbation, or
  colocalization. This script audits whether that bar is currently met.
"""

from __future__ import annotations

import json
import math
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave42_fads_lipid_desaturation_axis"
RAW = OUT / "raw_api"
SEED = 20260527

WAVE34 = ROOT / "results_v3" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv"
BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
RESIDUAL = ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
GWAS = ROOT / "tmp_v3" / "gwascatalog_associations_20260317_convert.parquet"
L1000_COMPOUNDS = ROOT / "data" / "raw_v3" / "lincs2020" / "compoundinfo_beta.txt"

GENES = ["FADS1", "FADS2", "FADS3"]
LOCUS_GENES = ["FADS1", "FADS2", "FADS3", "TMEM258", "MYRF", "FEN1", "C11orf10", "C11orf9", "RAB3IL1"]
AUTOIMMUNE_TERMS = [
    "multiple sclerosis",
    "crohn",
    "ulcerative colitis",
    "inflammatory bowel",
    "rheumatoid",
    "lupus",
    "systemic lupus",
    "type 1 diabetes",
    "psoriasis",
    "sjogren",
    "sjoegren",
    "ankylosing",
    "myasthenia",
    "thyroid",
    "celiac",
    "coeliac",
    "primary biliary",
    "vitiligo",
    "atopic dermatitis",
    "autoimmune",
]

CHEMBL_TARGETS = {
    "FADS1": "CHEMBL5840",
    "FADS2": "CHEMBL6097",
}

USER_AGENT = "ms-auto-research-wave42/1.0"


@dataclass
class ExternalCall:
    source: str
    query: str
    url: str
    status: str
    cache_file: str


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def safe_name(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_")[:180] or "blank"


def fetch_json(source: str, query: str, url: str, cache_name: str, calls: list[ExternalCall], sleep_s: float = 0.15) -> dict[str, Any]:
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / f"{safe_name(cache_name)}.json"
    if cache.exists():
        try:
            calls.append(ExternalCall(source, query, url, "cache_hit", rel(cache)))
            return json.loads(cache.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cache.unlink()
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        with urlopen(req, timeout=45) as handle:
            payload = json.loads(handle.read().decode("utf-8"))
        write_json(cache, payload)
        calls.append(ExternalCall(source, query, url, "ok", rel(cache)))
        time.sleep(sleep_s)
        return payload
    except Exception as exc:  # noqa: BLE001
        payload = {"error": str(exc), "url": url}
        write_json(cache, payload)
        calls.append(ExternalCall(source, query, url, f"error:{type(exc).__name__}", rel(cache)))
        return payload


def read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def contains_any(series: pd.Series, terms: list[str]) -> pd.Series:
    pattern = "|".join(re.escape(t) for t in terms)
    return series.fillna("").astype(str).str.contains(pattern, case=False, regex=True, na=False)


def collect_local_evidence() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    wave34 = read_table(WAVE34)
    broad = read_table(BROAD)
    residual = read_table(RESIDUAL)

    wave34_sub = wave34[wave34.get("gene", pd.Series(dtype=str)).astype(str).isin(GENES)].copy()
    broad_sub = broad[broad.get("gene", pd.Series(dtype=str)).astype(str).isin(GENES)].copy()
    residual_sub = residual[residual.get("gene", pd.Series(dtype=str)).astype(str).isin(GENES)].copy()
    return wave34_sub, broad_sub, residual_sub


def audit_gwas_catalog() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if not GWAS.exists():
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    cols = [
        "DISEASE/TRAIT",
        "REPORTED GENE(S)",
        "MAPPED_GENE",
        "SNP_GENE_IDS",
        "STRONGEST SNP-RISK ALLELE",
        "SNPS",
        "P-VALUE",
        "OR or BETA",
        "STUDY ACCESSION",
        "PUBMEDID",
        "FIRST AUTHOR",
        "DATE",
    ]
    gwas = pd.read_parquet(GWAS, columns=cols)
    autoimmune = gwas[contains_any(gwas["DISEASE/TRAIT"], AUTOIMMUNE_TERMS)].copy()
    locus_cols = ["REPORTED GENE(S)", "MAPPED_GENE", "SNP_GENE_IDS"]
    locus_mask = pd.Series(False, index=autoimmune.index)
    for col in locus_cols:
        locus_mask |= contains_any(autoimmune[col], LOCUS_GENES)
    locus = autoimmune[locus_mask].copy()
    locus["contains_fads_gene_name"] = False
    for col in locus_cols:
        locus["contains_fads_gene_name"] |= contains_any(locus[col], GENES)
    locus["contains_non_fads_locus_gene"] = False
    for col in locus_cols:
        locus["contains_non_fads_locus_gene"] |= contains_any(locus[col], ["TMEM258", "MYRF", "FEN1", "C11orf10", "C11orf9", "RAB3IL1"])
    locus["risk_allele_base"] = locus["STRONGEST SNP-RISK ALLELE"].fillna("").astype(str).str.extract(r"-([ACGT?])", expand=False)

    trait_summary = (
        locus.groupby("DISEASE/TRAIT", dropna=False)
        .agg(
            n_rows=("DISEASE/TRAIT", "size"),
            min_p=("P-VALUE", "min"),
            n_unique_snps=("SNPS", pd.Series.nunique),
            mapped_gene_values=("MAPPED_GENE", lambda s: ";".join(sorted(set(map(str, s.dropna()))))[:500]),
            risk_alleles=("STRONGEST SNP-RISK ALLELE", lambda s: ";".join(sorted(set(map(str, s.dropna()))))[:500]),
            has_non_fads=("contains_non_fads_locus_gene", "max"),
        )
        .reset_index()
        .sort_values(["n_rows", "min_p"], ascending=[False, True])
    )
    mapped_summary = (
        locus.groupby("MAPPED_GENE", dropna=False)
        .agg(n_rows=("MAPPED_GENE", "size"), n_traits=("DISEASE/TRAIT", pd.Series.nunique), min_p=("P-VALUE", "min"))
        .reset_index()
        .sort_values(["n_rows", "min_p"], ascending=[False, True])
    )
    return locus, trait_summary, mapped_summary


def chembl_target(chembl_id: str, calls: list[ExternalCall]) -> dict[str, Any]:
    url = f"https://www.ebi.ac.uk/chembl/api/data/target/{quote(chembl_id)}.json"
    return fetch_json("ChEMBL", chembl_id, url, f"chembl_target_{chembl_id}", calls)


def chembl_activities(chembl_id: str, calls: list[ExternalCall]) -> dict[str, Any]:
    url = f"https://www.ebi.ac.uk/chembl/api/data/activity.json?{urlencode({'target_chembl_id': chembl_id, 'limit': 1000})}"
    return fetch_json("ChEMBL", chembl_id, url, f"chembl_activity_{chembl_id}", calls)


def aggregate_activities(gene: str, target_id: str, target: dict[str, Any], activities: dict[str, Any]) -> dict[str, Any]:
    rows = activities.get("activities", []) if isinstance(activities, dict) else []
    values = []
    molecules = set()
    assay_types = {}
    best_row: dict[str, Any] | None = None
    for row in rows:
        if row.get("molecule_chembl_id"):
            molecules.add(row["molecule_chembl_id"])
        if row.get("assay_type"):
            assay_types[row["assay_type"]] = assay_types.get(row["assay_type"], 0) + 1
        try:
            value = float(row.get("standard_value")) if row.get("standard_units") == "nM" else math.nan
        except Exception:
            value = math.nan
        if np.isfinite(value):
            values.append(value)
            if best_row is None or value < float(best_row.get("standard_value", float("inf"))):
                best_row = row
    return {
        "gene": gene,
        "target_chembl_id": target_id,
        "target_pref_name": target.get("pref_name"),
        "target_type": target.get("target_type"),
        "organism": target.get("organism"),
        "activity_total_count": activities.get("page_meta", {}).get("total_count") if isinstance(activities, dict) else None,
        "returned_activity_rows": len(rows),
        "activity_values_nM_count": len(values),
        "unique_molecules_returned": len(molecules),
        "best_standard_nM": min(values) if values else None,
        "median_standard_nM": float(np.median(values)) if values else None,
        "assay_type_counts": json.dumps(assay_types, sort_keys=True),
        "best_molecule_chembl_id": best_row.get("molecule_chembl_id") if best_row else None,
        "best_molecule_pref_name": best_row.get("molecule_pref_name") if best_row else None,
        "best_assay_description": best_row.get("assay_description") if best_row else None,
    }


def europepmc_count(query: str, calls: list[ExternalCall]) -> int | None:
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urlencode(
        {"query": query, "format": "json", "pageSize": 1}
    )
    payload = fetch_json("Europe PMC", query, url, f"europepmc_{query}", calls)
    try:
        return int(payload.get("hitCount"))
    except Exception:
        return None


def clinicaltrials_count(query: str, calls: list[ExternalCall]) -> int | None:
    url = "https://clinicaltrials.gov/api/v2/studies?" + urlencode({"query.term": query, "pageSize": 1})
    payload = fetch_json("ClinicalTrials.gov", query, url, f"clinicaltrials_{query}", calls)
    try:
        if payload.get("totalCount") is not None:
            return int(payload.get("totalCount"))
        if isinstance(payload.get("studies"), list):
            return len(payload.get("studies"))
        return None
    except Exception:
        return None


def lincs_fads_presence() -> pd.DataFrame:
    compoundinfo = read_table(L1000_COMPOUNDS)
    if compoundinfo.empty:
        return pd.DataFrame()
    text_cols = [c for c in ["target", "moa", "cmap_name", "compound_aliases"] if c in compoundinfo.columns]
    mask = pd.Series(False, index=compoundinfo.index)
    for col in text_cols:
        mask |= compoundinfo[col].fillna("").astype(str).str.contains(r"\bFADS1\b|\bFADS2\b|delta-5 desaturase|delta 5 desaturase", case=False, regex=True)
    return compoundinfo.loc[mask, [c for c in ["pert_id", "cmap_name", "target", "moa", "compound_aliases", "inchi_key"] if c in compoundinfo.columns]].copy()


def lipid_flux_sensitivity_model() -> pd.DataFrame:
    """A deliberately simple non-claim model.

    The model asks whether FADS1 inhibition has an obvious selective window
    under generic assumptions. It does not estimate real biochemistry.
    """
    rows = []
    rng = np.random.default_rng(SEED)
    for inhibition in np.linspace(0.1, 0.9, 9):
        for _ in range(1000):
            baseline_aa_flux = rng.uniform(0.6, 1.4)
            compensation = rng.uniform(0.0, 0.8)
            dglA_benefit_weight = rng.uniform(0.2, 0.8)
            host_lipid_cost_weight = rng.uniform(0.1, 0.7)
            aa_drop = baseline_aa_flux * inhibition * (1 - 0.35 * compensation)
            precursor_shift = inhibition * (1 + compensation)
            inflammatory_eicosanoid_drop = aa_drop
            potentially_pro_resolving_shift = precursor_shift * dglA_benefit_weight
            host_lipid_cost = inhibition * host_lipid_cost_weight
            selectivity_index = inflammatory_eicosanoid_drop + potentially_pro_resolving_shift - host_lipid_cost
            rows.append(
                {
                    "fads1_inhibition_fraction": inhibition,
                    "inflammatory_eicosanoid_drop_proxy": inflammatory_eicosanoid_drop,
                    "potentially_pro_resolving_shift_proxy": potentially_pro_resolving_shift,
                    "host_lipid_cost_proxy": host_lipid_cost,
                    "selectivity_index_proxy": selectivity_index,
                }
            )
    df = pd.DataFrame(rows)
    summary = (
        df.groupby("fads1_inhibition_fraction")
        .agg(
            median_eicosanoid_drop=("inflammatory_eicosanoid_drop_proxy", "median"),
            median_resolution_shift=("potentially_pro_resolving_shift_proxy", "median"),
            median_host_cost=("host_lipid_cost_proxy", "median"),
            p_selectivity_positive=("selectivity_index_proxy", lambda s: float(np.mean(s > 0.5))),
            p_host_cost_gt_0_3=("host_lipid_cost_proxy", lambda s: float(np.mean(s > 0.3))),
        )
        .reset_index()
    )
    return summary


def markdown_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    if df.empty:
        return "_No rows._"
    shown = df.head(max_rows).copy()
    cols = list(shown.columns)
    rows = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in shown.iterrows():
        values = []
        for col in cols:
            value = "" if pd.isna(row[col]) else str(row[col])
            value = value.replace("\n", " ").replace("|", "\\|")
            values.append(value)
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    calls: list[ExternalCall] = []

    wave34_sub, broad_sub, residual_sub = collect_local_evidence()
    locus, trait_summary, mapped_summary = audit_gwas_catalog()

    chembl_rows = []
    for gene, target_id in CHEMBL_TARGETS.items():
        target = chembl_target(target_id, calls)
        activities = chembl_activities(target_id, calls)
        write_json(RAW / f"chembl_bundle_{gene}.json", {"target": target, "activities_page": activities})
        chembl_rows.append(aggregate_activities(gene, target_id, target, activities))
    chembl_df = pd.DataFrame(chembl_rows)

    lit_queries = [
        '"FADS1" AND ("autoimmune" OR "multiple sclerosis" OR "rheumatoid arthritis" OR "lupus" OR "IBD" OR "psoriasis")',
        '"FADS2" AND ("autoimmune" OR "multiple sclerosis" OR "rheumatoid arthritis" OR "lupus" OR "IBD" OR "psoriasis")',
        '"delta-5 desaturase inhibitor" AND ("autoimmune" OR "inflammatory bowel" OR "rheumatoid" OR "multiple sclerosis")',
        '"FADS1 inhibitor" AND ("autoimmune" OR "inflammatory bowel" OR "rheumatoid" OR "multiple sclerosis")',
        '"FADS1" AND "TMEM258" AND ("Crohn" OR "inflammatory bowel" OR "rheumatoid")',
    ]
    literature = pd.DataFrame(
        [{"query": q, "europepmc_hit_count": europepmc_count(q, calls)} for q in lit_queries]
    )
    trial_queries = [
        "FADS1 autoimmune",
        "FADS2 autoimmune",
        "delta-5 desaturase inhibitor",
        "D5D inhibitor",
        "FADS1 inhibitor",
        "AMG 786",
    ]
    trials = pd.DataFrame([{"query": q, "clinicaltrials_count": clinicaltrials_count(q, calls)} for q in trial_queries])
    patents = pd.DataFrame(
        [
            {
                "query": q,
                "google_patents_url": "https://patents.google.com/?" + urlencode({"q": q}),
            }
            for q in ["FADS1 inhibitor autoimmune", "delta-5 desaturase inhibitor inflammatory disease", "FADS2 inhibitor autoimmune"]
        ]
    )

    lincs = lincs_fads_presence()
    model = lipid_flux_sensitivity_model()

    wave34_sub.to_csv(OUT / "wave34_fads_rows.tsv", sep="\t", index=False)
    broad_sub.to_csv(OUT / "local_cellstate_fads_rows.tsv", sep="\t", index=False)
    residual_sub.to_csv(OUT / "local_residual_fads_rows.tsv", sep="\t", index=False)
    locus.to_csv(OUT / "gwascatalog_fads_locus_autoimmune_rows.tsv", sep="\t", index=False)
    trait_summary.to_csv(OUT / "gwascatalog_fads_locus_trait_summary.tsv", sep="\t", index=False)
    mapped_summary.to_csv(OUT / "gwascatalog_fads_locus_mapped_gene_summary.tsv", sep="\t", index=False)
    chembl_df.to_csv(OUT / "chembl_fads_activity_summary.tsv", sep="\t", index=False)
    lincs.to_csv(OUT / "lincs_fads_perturbagen_presence.tsv", sep="\t", index=False)
    literature.to_csv(OUT / "fads_literature_query_counts.tsv", sep="\t", index=False)
    trials.to_csv(OUT / "fads_clinicaltrials_query_counts.tsv", sep="\t", index=False)
    patents.to_csv(OUT / "fads_patent_search_urls.tsv", sep="\t", index=False)
    model.to_csv(OUT / "fads_lipid_flux_sensitivity_model.tsv", sep="\t", index=False)
    pd.DataFrame([asdict(c) for c in calls]).to_csv(OUT / "api_call_log.tsv", sep="\t", index=False)

    n_autoimmune_traits = int(locus["DISEASE/TRAIT"].nunique()) if not locus.empty else 0
    n_locus_rows = int(len(locus))
    n_fads_named = int(locus["contains_fads_gene_name"].sum()) if not locus.empty else 0
    n_non_fads_named = int(locus["contains_non_fads_locus_gene"].sum()) if not locus.empty else 0
    fads1_broad = broad_sub[broad_sub["gene"].eq("FADS1")].iloc[0].to_dict() if not broad_sub[broad_sub["gene"].eq("FADS1")].empty else {}
    fads2_broad = broad_sub[broad_sub["gene"].eq("FADS2")].iloc[0].to_dict() if not broad_sub[broad_sub["gene"].eq("FADS2")].empty else {}

    failed_gates = [
        "target_level_colocalization_or_mr_direction_absent",
        "GWAS_Catalog_signal_is_11q12_locus_level_with_TMEM258_MYRF_FEN1_ambiguity",
        "local_cell_state_support_weak_and_not_lipid_lysosomal_myeloid_specific",
        "no_LINCS_FADS1_or_FADS2_perturbagen_present_for_signature_validation",
        "intervention_direction_unresolved_from_risk_alleles",
    ]
    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "branch": "FADS1/FADS2 genetics-first lipid-desaturation axis",
        "promotion_status": "NO_THERAPEUTIC_CLAIM",
        "wave42_call": "PARK_ONLY_IF_COLOC_DIRECTION_AND_PERTURBATION_APPEAR",
        "failed_gates": failed_gates,
        "gwas_catalog_autoimmune_locus_rows": n_locus_rows,
        "gwas_catalog_autoimmune_trait_count": n_autoimmune_traits,
        "gwas_catalog_rows_with_fads_gene_name": n_fads_named,
        "gwas_catalog_rows_with_non_fads_locus_gene": n_non_fads_named,
        "mapped_gene_top_counts": mapped_summary.head(10).to_dict("records") if not mapped_summary.empty else [],
        "local_cell_state_summary": {
            "FADS1_positive_diseases": fads1_broad.get("positive_diseases"),
            "FADS1_positive_disease_count": fads1_broad.get("positive_disease_count"),
            "FADS1_ms_delta": fads1_broad.get("ms_wm_delta_log2"),
            "FADS1_ms_p": fads1_broad.get("ms_wm_p"),
            "FADS2_positive_diseases": fads2_broad.get("positive_diseases"),
            "FADS2_positive_disease_count": fads2_broad.get("positive_disease_count"),
            "FADS2_ms_delta": fads2_broad.get("ms_wm_delta_log2"),
            "FADS2_ms_p": fads2_broad.get("ms_wm_p"),
            "residual_summary_rows": int(len(residual_sub)),
        },
        "chembl_summary": chembl_df.to_dict("records"),
        "lincs_fads_perturbagen_rows": int(len(lincs)),
        "interpretation": (
            "FADS1/FADS2 remains mechanistically interesting as a lipid-genetic hypothesis, but Wave42 does not "
            "promote it. The autoimmune evidence is locus-level rather than target-level, risk-allele direction is "
            "not resolved, local cell-state evidence is weak and non-MS, and no LINCS FADS perturbagen is available "
            "to validate module reversal. FADS1 chemistry exists, so the route is parked only for future coloc/MR "
            "and perturbation work."
        ),
        "output_paths": {
            "wave34_fads_rows": rel(OUT / "wave34_fads_rows.tsv"),
            "local_cellstate_fads_rows": rel(OUT / "local_cellstate_fads_rows.tsv"),
            "gwascatalog_rows": rel(OUT / "gwascatalog_fads_locus_autoimmune_rows.tsv"),
            "gwascatalog_trait_summary": rel(OUT / "gwascatalog_fads_locus_trait_summary.tsv"),
            "gwascatalog_mapped_gene_summary": rel(OUT / "gwascatalog_fads_locus_mapped_gene_summary.tsv"),
            "chembl_summary": rel(OUT / "chembl_fads_activity_summary.tsv"),
            "lincs_presence": rel(OUT / "lincs_fads_perturbagen_presence.tsv"),
            "literature_counts": rel(OUT / "fads_literature_query_counts.tsv"),
            "clinicaltrials_counts": rel(OUT / "fads_clinicaltrials_query_counts.tsv"),
            "patent_urls": rel(OUT / "fads_patent_search_urls.tsv"),
            "model": rel(OUT / "fads_lipid_flux_sensitivity_model.tsv"),
            "api_call_log": rel(OUT / "api_call_log.tsv"),
        },
    }
    write_json(OUT / "summary.json", summary)

    report = [
        "# Wave42 FADS Lipid-Desaturation Axis",
        "",
        "## Result",
        "",
        summary["interpretation"],
        "",
        "## Failed Gates",
        "",
        "\n".join(f"- {x}" for x in failed_gates),
        "",
        "## Local Wave34 Rows",
        "",
        markdown_table(wave34_sub[[c for c in [
            "gene",
            "wave34_call",
            "wave34_score",
            "gwas_catalog_trait_count",
            "local_positive_disease_count",
            "residual_retained_disease_count",
            "druggable_activity_count",
            "chembl_target_id",
            "chembl_pref_name",
            "chembl_best_nM",
            "failed_gates",
        ] if c in wave34_sub.columns]]),
        "",
        "## GWAS Locus Ambiguity",
        "",
        f"Autoimmune FADS-locus rows: {n_locus_rows}; distinct traits: {n_autoimmune_traits}; rows naming FADS genes: {n_fads_named}; rows also naming non-FADS locus genes: {n_non_fads_named}.",
        "",
        markdown_table(mapped_summary.head(12)),
        "",
        "## Local Cell-State Evidence",
        "",
        markdown_table(broad_sub[[c for c in [
            "gene",
            "positive_disease_count",
            "positive_diseases",
            "best_positive_p",
            "best_positive_fdr",
            "top_positive_compartments",
            "ms_wm_delta_log2",
            "ms_wm_p",
            "ms_wm_fdr",
            "in_lipid_lysosomal_myeloid_neighborhood",
        ] if c in broad_sub.columns]]),
        "",
        "## ChEMBL Druggability",
        "",
        markdown_table(chembl_df),
        "",
        "## Perturbation Availability",
        "",
        f"LINCS FADS1/FADS2 perturbagen rows found by exact target/MOA search: {len(lincs)}.",
        "",
        "## Model Scope",
        "",
        "The lipid-flux model is assumption-explicit and not fitted to patient or biochemical data. It is only a sanity check that FADS1 inhibition lacks an obvious disease-selective window without genotype or lipidomic stratification.",
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
