#!/usr/bin/env python3
"""Wave17 Mediator/CDK8-CDK19 translational gate.

This gate asks whether the strong Med16 knockout perturbation profile in
GSE162464 can be translated into a druggable Mediator kinase intervention.

It combines:
- existing local perturbation outputs for Med16/Gsk3b/RFX5/JAK controls;
- local cross-disease expression rows for MED16/CDK8/CDK19/CCNC/MED12;
- ChEMBL public activity depth for CDK8/CDK19 and related complexes/family;
- Europe PMC and ClinicalTrials.gov query logs for prior art and trial crowding.

The output is a gate verdict, not a final target claim.
"""

from __future__ import annotations

import json
import math
import urllib.parse
from pathlib import Path
from typing import Any

import pandas as pd
import requests


OUT = Path("phases/v3/results/wave17_mediator_route_gate")
OUT.mkdir(parents=True, exist_ok=True)
SEED = 20260526

CHEMBL_TARGETS = {
    "CDK8": "CHEMBL5719",
    "CDK19": "CHEMBL6002",
    "CDK8_CyclinC_complex": "CHEMBL3038474",
    "CDK19_CyclinC_complex": "CHEMBL3883323",
    "CDK8_CDK19_family": "CHEMBL3885556",
}

EUROPEPMC_QUERIES = {
    "mediator_kinase_ifn": '"CDK8" "CDK19" interferon',
    "mediator_kinase_autoimmune": '("CDK8" OR "CDK19" OR "Mediator kinase") autoimmune',
    "mediator_kinase_mhc2": '("CDK8" OR "CDK19" OR "Mediator kinase") ("MHC class II" OR CIITA)',
    "med16_mhc2": '"MED16" "MHCII" macrophage',
    "cortistatin_autoimmune": '"cortistatin A" autoimmune',
}

CLINICALTRIAL_TERMS = [
    "CDK8 CDK19 autoimmune",
    "CDK8 inhibitor autoimmune",
    "CDK8 inhibitor multiple sclerosis",
    "CDK8 inhibitor lupus",
    "cortistatin A autoimmune",
    "CDK8 CDK19 interferon",
]

LOCAL_GENES = ["MED16", "CDK8", "CDK19", "CCNC", "MED12", "MED13", "MED23", "STAT1", "CIITA", "CD74"]


def read_existing_perturbation() -> pd.DataFrame:
    p = Path("phases/v3/results/wave15_perturbation_drug_response/ranked_direct_perturbations.tsv")
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_csv(p, sep="\t")
    keep = df[df["perturbation"].isin(["Med16_KO", "Gsk3b_KO", "RFX5", "JAK1", "JAK2", "STAT1", "ruxolitinib"])]
    return keep.copy()


def read_local_gene_rows() -> pd.DataFrame:
    rows = []
    p = Path("phases/v3/results/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv")
    if p.exists():
        broad = pd.read_csv(p, sep="\t", low_memory=False)
        for _, row in broad[broad["gene"].isin(LOCAL_GENES)].iterrows():
            rows.append(
                {
                    "source": "broad_h5ad_gene_discovery",
                    "gene": row["gene"],
                    "positive_disease_count": row.get("positive_disease_count"),
                    "negative_disease_count": row.get("negative_disease_count"),
                    "positive_fdr10_compartment_count": row.get("positive_fdr10_compartment_count"),
                    "positive_diseases": row.get("positive_diseases"),
                    "negative_diseases": row.get("negative_diseases"),
                    "ms_wm_delta_log2": row.get("ms_wm_delta_log2"),
                    "ms_wm_p": row.get("ms_wm_p"),
                    "ms_wm_fdr": row.get("ms_wm_fdr"),
                    "discovery_priority_score": row.get("discovery_priority_score"),
                }
            )
    p2 = Path("phases/v3/results/wave14_gsk3b_local_gate/gsk3b_local_gate_gene_summary.tsv")
    if p2.exists():
        gate = pd.read_csv(p2, sep="\t")
        for _, row in gate[gate["gene"].isin(LOCAL_GENES)].iterrows():
            rows.append(
                {
                    "source": "wave14_gsk3b_local_gate",
                    "gene": row["gene"],
                    "positive_disease_count": row.get("n_trend_or_better_diseases"),
                    "negative_disease_count": row.get("n_negative_trend_diseases"),
                    "positive_fdr10_compartment_count": row.get("n_fdr10_positive_diseases"),
                    "positive_diseases": row.get("supporting_diseases"),
                    "negative_diseases": row.get("negative_diseases"),
                    "ms_wm_delta_log2": None,
                    "ms_wm_p": None,
                    "ms_wm_fdr": None,
                    "discovery_priority_score": None,
                }
            )
    return pd.DataFrame(rows)


def fetch_chembl_activity(gene: str, target_id: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    url = "https://www.ebi.ac.uk/chembl/api/data/activity.json"
    params: dict[str, Any] | None = {
        "target_chembl_id": target_id,
        "limit": 1000,
        "standard_units": "nM",
        "standard_type__in": "IC50,Ki,EC50,Potency",
    }
    total_count = None
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        total_count = data.get("page_meta", {}).get("total_count")
        for act in data.get("activities", []):
            try:
                value = float(act.get("standard_value"))
            except (TypeError, ValueError):
                continue
            if value <= 0 or math.isnan(value):
                continue
            rows.append(
                {
                    "gene_or_target": gene,
                    "target_chembl_id": target_id,
                    "molecule_chembl_id": act.get("molecule_chembl_id"),
                    "standard_type": act.get("standard_type"),
                    "standard_value_nM": value,
                    "pchembl_value": act.get("pchembl_value"),
                    "document_chembl_id": act.get("document_chembl_id"),
                    "assay_chembl_id": act.get("assay_chembl_id"),
                }
            )
    except Exception as exc:  # noqa: BLE001
        errors.append(str(exc))
    return rows, {"gene_or_target": gene, "target_chembl_id": target_id, "total_count": total_count, "errors": errors}


def chembl_summary(df: pd.DataFrame, meta: list[dict[str, Any]]) -> pd.DataFrame:
    meta_df = pd.DataFrame(meta)
    if df.empty:
        return meta_df
    stats = (
        df.groupby("gene_or_target")
        .agg(
            retained_activity_rows=("molecule_chembl_id", "size"),
            unique_molecules=("molecule_chembl_id", "nunique"),
            min_nM=("standard_value_nM", "min"),
            median_nM=("standard_value_nM", "median"),
            n_sub_100nM=("standard_value_nM", lambda s: int((s <= 100).sum())),
            n_sub_1000nM=("standard_value_nM", lambda s: int((s <= 1000).sum())),
        )
        .reset_index()
    )
    return meta_df.merge(stats, on="gene_or_target", how="left")


def europepmc_query(name: str, query: str) -> dict[str, Any]:
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {"query": query, "format": "json", "pageSize": 5, "resultType": "core"}
    row: dict[str, Any] = {"resource": "Europe PMC", "name": name, "query": query}
    try:
        resp = requests.get(url, params=params, timeout=30)
        row["status_code"] = resp.status_code
        data = resp.json()
        row["hit_count"] = int(data.get("hitCount", 0))
        results = []
        for res in data.get("resultList", {}).get("result", [])[:5]:
            results.append(
                {
                    "id": res.get("id"),
                    "pmid": res.get("pmid"),
                    "pmcid": res.get("pmcid"),
                    "doi": res.get("doi"),
                    "title": res.get("title"),
                    "pubYear": res.get("pubYear"),
                }
            )
        row["top_results_json"] = json.dumps(results, ensure_ascii=False)
    except Exception as exc:  # noqa: BLE001
        row["error"] = str(exc)
    return row


def clinicaltrials_query(term: str) -> dict[str, Any]:
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {"query.term": term, "pageSize": 10}
    row: dict[str, Any] = {"resource": "ClinicalTrials.gov", "query": term}
    try:
        resp = requests.get(url, params=params, timeout=30)
        row["status_code"] = resp.status_code
        data = resp.json()
        studies = []
        for st in data.get("studies", [])[:10]:
            proto = st.get("protocolSection", {})
            ident = proto.get("identificationModule", {})
            status = proto.get("statusModule", {})
            cond = proto.get("conditionsModule", {})
            studies.append(
                {
                    "nct_id": ident.get("nctId"),
                    "title": ident.get("briefTitle"),
                    "status": status.get("overallStatus"),
                    "conditions": cond.get("conditions"),
                }
            )
        row["n_returned"] = len(studies)
        row["top_studies_json"] = json.dumps(studies, ensure_ascii=False)
    except Exception as exc:  # noqa: BLE001
        row["error"] = str(exc)
    return row


def main() -> None:
    perturb = read_existing_perturbation()
    perturb.to_csv(OUT / "mediator_relevant_existing_perturbations.tsv", sep="\t", index=False)

    local = read_local_gene_rows()
    local.to_csv(OUT / "mediator_gene_local_expression_rows.tsv", sep="\t", index=False)

    chembl_rows = []
    chembl_meta = []
    for gene, target_id in CHEMBL_TARGETS.items():
        rows, meta = fetch_chembl_activity(gene, target_id)
        chembl_rows.extend(rows)
        chembl_meta.append(meta)
    chembl = pd.DataFrame(chembl_rows)
    chembl.to_csv(OUT / "mediator_chembl_activity_records.tsv", sep="\t", index=False)
    chembl_stats = chembl_summary(chembl, chembl_meta)
    chembl_stats.to_csv(OUT / "mediator_chembl_activity_summary.tsv", sep="\t", index=False)

    query_rows = []
    for name, query in EUROPEPMC_QUERIES.items():
        query_rows.append(europepmc_query(name, query))
    for term in CLINICALTRIAL_TERMS:
        query_rows.append(clinicaltrials_query(term))
    queries = pd.DataFrame(query_rows)
    queries.to_csv(OUT / "mediator_prior_art_query_log.tsv", sep="\t", index=False)

    med16 = perturb[perturb["perturbation"].eq("Med16_KO")]
    med16_selectivity_score = float(med16["selectivity_score"].max()) if not med16.empty else None
    med16_target_effect = float(med16["target_module_effect"].min()) if not med16.empty else None
    med16_ifn_effect = float(med16["generic_ifn_effect"].min()) if not med16.empty else None

    cdk8_local = local[local["gene"].isin(["CDK8", "CDK19"])]
    cdk8_positive_diseases = (
        int(pd.to_numeric(cdk8_local.get("positive_disease_count", pd.Series(dtype=float)), errors="coerce").fillna(0).max())
        if not cdk8_local.empty
        else 0
    )
    n_cdk8_trials = 0
    if not queries.empty and "top_studies_json" in queries.columns:
        for s in queries.loc[queries["resource"].eq("ClinicalTrials.gov"), "top_studies_json"].dropna():
            try:
                n_cdk8_trials += len(json.loads(s))
            except json.JSONDecodeError:
                pass

    go_reasons = []
    no_go_reasons = []
    if med16_selectivity_score is not None and med16_selectivity_score >= 2:
        go_reasons.append("Med16_KO has a strong selective antigen-presentation suppression profile in GSE162464.")
    else:
        no_go_reasons.append("No strong Med16 perturbation profile was available.")
    if not chembl_stats.empty and chembl_stats["unique_molecules"].fillna(0).max() >= 50:
        go_reasons.append("Public CDK8/CDK19/Mediator-kinase chemical matter exists in ChEMBL.")
    if cdk8_positive_diseases < 3:
        no_go_reasons.append("CDK8/CDK19 local expression recurrence is weak and does not define the cross-disease state.")
    no_go_reasons.append("No direct local CDK8/CDK19 inhibitor perturbation dataset was found that proves Med16_KO phenocopy in autoimmune APCs.")
    no_go_reasons.append("Mediator kinase inhibition is expected to affect broad transcriptional/inflammatory programs; selectivity over generic IFN remains unproven.")
    if n_cdk8_trials == 0:
        no_go_reasons.append("ClinicalTrials.gov targeted queries returned no direct autoimmune CDK8/CDK19 interventional trial evidence.")

    verdict = "PARK_AS_PERTURBATION_DERIVED_INTERVENTION_HYPOTHESIS"
    if med16_selectivity_score is None or cdk8_positive_diseases == 0:
        verdict = "NO_GO_CURRENTLY"

    summary = {
        "seed": SEED,
        "verdict": verdict,
        "med16_target_module_effect": med16_target_effect,
        "med16_generic_ifn_effect": med16_ifn_effect,
        "med16_selectivity_score": med16_selectivity_score,
        "max_cdk8_or_cdk19_positive_disease_count": cdk8_positive_diseases,
        "n_clinicaltrials_returned_across_terms": n_cdk8_trials,
        "go_reasons": go_reasons,
        "no_go_reasons": no_go_reasons,
        "interpretation": "Mediator kinase is more plausible than CTSH as a perturbation-derived controller, but current data support a parked hypothesis, not V3 promotion.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
