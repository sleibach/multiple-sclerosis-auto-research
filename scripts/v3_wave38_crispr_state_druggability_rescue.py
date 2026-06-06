#!/usr/bin/env python3
"""Wave38 rescue scan from direct efferocytosis CRISPR hits.

Question: does the direct GSE212008 efferocytosis screen contain an overlooked
target that survives cross-autoimmune disease-state, druggability, and
prior-art gates?

This is deliberately conservative. GSE212008 is a phenotypic mouse BMDM screen,
so a screen hit is only a hypothesis generator unless the desired intervention
direction matches disease-state evidence and tractable pharmacology.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave38_crispr_state_druggability_rescue"
API = OUT / "raw_api"
SEED = 20260527
USER_AGENT = "ms-auto-research-wave38-crispr-state-druggability/1.0"

SCREEN_PATH = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
BROAD_PATH = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
WAVE34_PATH = ROOT / "phases/v3/results" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv"


def get_json(url: str, path: Path, timeout: int = 30) -> dict:
    API.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        try:
            return json.loads(path.read_text())
        except Exception:
            pass
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def chembl_target(gene: str) -> dict:
    safe = quote(gene)
    payload = get_json(
        f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={safe}",
        API / f"chembl_target_{gene}.json",
    )
    targets = payload.get("targets", [])
    exact = []
    for target in targets:
        for comp in target.get("target_components", []):
            for syn in comp.get("target_component_synonyms", []):
                if str(syn.get("component_synonym", "")).upper() == gene:
                    exact.append(target)
                    break
    target = exact[0] if exact else (targets[0] if targets else {})
    tid = target.get("target_chembl_id", "")
    activity_count = 0
    best_nM = np.nan
    if tid:
        act_url = (
            "https://www.ebi.ac.uk/chembl/api/data/activity.json?"
            + urlencode(
                {
                    "target_chembl_id": tid,
                    "standard_units": "nM",
                    "limit": "1000",
                }
            )
        )
        act = get_json(act_url, API / f"chembl_activity_{gene}_{tid}.json", timeout=45)
        values = []
        for row in act.get("activities", []):
            try:
                val = float(row.get("standard_value"))
            except (TypeError, ValueError):
                continue
            if np.isfinite(val) and val > 0:
                values.append(val)
        activity_count = len(values)
        best_nM = float(min(values)) if values else np.nan
    return {
        "chembl_target_id": tid,
        "chembl_pref_name": target.get("pref_name", ""),
        "chembl_target_type": target.get("target_type", ""),
        "chembl_activity_count": activity_count,
        "chembl_best_nM": best_nM,
        "chembl_search_total": payload.get("page_meta", {}).get("total_count", 0),
    }


def europepmc_count(gene: str) -> dict:
    query = f'"{gene}" autoimmune OR "multiple sclerosis" OR "inflammatory bowel disease" OR psoriasis OR lupus'
    url = (
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
        + urlencode({"query": query, "format": "json", "pageSize": "5"})
    )
    payload = get_json(url, API / f"europepmc_{gene}.json")
    result = payload.get("resultList", {}).get("result", [])
    return {
        "europepmc_query": query,
        "europepmc_hit_count": int(payload.get("hitCount", 0) or 0),
        "europepmc_examples_json": json.dumps(
            [
                {
                    "id": r.get("id"),
                    "title": r.get("title"),
                    "year": r.get("pubYear"),
                    "doi": r.get("doi"),
                }
                for r in result[:3]
            ],
            sort_keys=True,
        ),
    }


def clinicaltrials_count(gene: str) -> dict:
    query = f"{gene} autoimmune"
    url = (
        "https://clinicaltrials.gov/api/v2/studies?"
        + urlencode({"query.term": query, "pageSize": "5", "format": "json"})
    )
    try:
        payload = get_json(url, API / f"clinicaltrials_{gene}.json")
    except Exception as exc:
        return {"clinicaltrials_query": query, "clinicaltrials_hit_count": np.nan, "clinicaltrials_error": repr(exc)}
    studies = payload.get("studies", [])
    total = payload.get("totalCount", len(studies))
    examples = []
    for study in studies[:3]:
        proto = study.get("protocolSection", {})
        ident = proto.get("identificationModule", {})
        status = proto.get("statusModule", {})
        cond = proto.get("conditionsModule", {})
        examples.append(
            {
                "nct_id": ident.get("nctId"),
                "title": ident.get("briefTitle"),
                "status": status.get("overallStatus"),
                "conditions": ";".join(cond.get("conditions", [])),
            }
        )
    return {
        "clinicaltrials_query": query,
        "clinicaltrials_hit_count": int(total or 0),
        "clinicaltrials_examples_json": json.dumps(examples, sort_keys=True),
    }


def load_candidates() -> pd.DataFrame:
    screen = pd.read_csv(SCREEN_PATH, sep="\t")
    screen["gene"] = screen["gene_symbol"].astype(str).str.upper()

    enhancers = (
        screen[screen["screen_call"].eq("KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR")]
        .sort_values("median_efficient_minus_noneater_lfc", ascending=False)
        .head(80)
    )
    positives = (
        screen[screen["screen_call"].eq("KO_IMPAIRS_EFFEROCYTOSIS_POSITIVE_REGULATOR")]
        .sort_values("median_efficient_minus_noneater_lfc", ascending=True)
        .head(40)
    )
    tracked = screen[(screen["tracked_candidate"]) | (screen["modules"].fillna("").ne(""))]
    return pd.concat([enhancers, positives, tracked], ignore_index=True).drop_duplicates("gene")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    API.mkdir(parents=True, exist_ok=True)

    candidates = load_candidates()
    broad = pd.read_csv(BROAD_PATH, sep="\t").rename(columns={"gene": "gene"})
    broad["gene"] = broad["gene"].astype(str).str.upper()
    if WAVE34_PATH.exists():
        wave34 = pd.read_csv(WAVE34_PATH, sep="\t").rename(columns={"gene": "gene"})
        wave34["gene"] = wave34["gene"].astype(str).str.upper()
    else:
        wave34 = pd.DataFrame({"gene": []})

    merged = candidates.merge(broad, on="gene", how="left", suffixes=("", "_broad"))
    wave34_cols = [
        "gene",
        "gwas_catalog_trait_count",
        "gwas_catalog_min_p",
        "druggable_activity_count",
        "chembl_target_id",
        "clinicaltrials_autoimmune_count",
        "europepmc_autoimmune_hit_count",
        "wave34_call",
        "manual_blocker_class",
        "primary_blocker",
    ]
    merged = merged.merge(wave34[[c for c in wave34_cols if c in wave34.columns]], on="gene", how="left")

    api_rows = []
    for gene in merged["gene"].head(120):
        row = {"gene": gene}
        try:
            row.update(chembl_target(gene))
        except Exception as exc:
            row["chembl_error"] = repr(exc)
        try:
            row.update(europepmc_count(gene))
        except Exception as exc:
            row["europepmc_error"] = repr(exc)
        row.update(clinicaltrials_count(gene))
        api_rows.append(row)
    api_df = pd.DataFrame(api_rows)
    merged = merged.merge(api_df, on="gene", how="left", suffixes=("", "_api"))

    # Directional disease-state consistency:
    # - KO enhancer implies target inhibition. Disease-up is supportive.
    # - KO impairment implies target activation/restoration. Disease-down is supportive.
    merged["desired_intervention"] = np.where(
        merged["screen_call"].eq("KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR"),
        "inhibit_or_reduce",
        np.where(merged["screen_call"].eq("KO_IMPAIRS_EFFEROCYTOSIS_POSITIVE_REGULATOR"), "activate_or_restore", "unresolved"),
    )
    merged["directional_disease_support_count"] = np.where(
        merged["desired_intervention"].eq("inhibit_or_reduce"),
        merged["positive_disease_count"].fillna(0),
        np.where(
            merged["desired_intervention"].eq("activate_or_restore"),
            merged["negative_disease_count"].fillna(0),
            0,
        ),
    )
    merged["directional_conflict_count"] = np.where(
        merged["desired_intervention"].eq("inhibit_or_reduce"),
        merged["negative_disease_count"].fillna(0),
        np.where(
            merged["desired_intervention"].eq("activate_or_restore"),
            merged["positive_disease_count"].fillna(0),
            0,
        ),
    )
    merged["ms_anchor_directional"] = np.where(
        merged["desired_intervention"].eq("inhibit_or_reduce"),
        merged["ms_wm_delta_log2"].fillna(0) > 0.2,
        np.where(merged["desired_intervention"].eq("activate_or_restore"), merged["ms_wm_delta_log2"].fillna(0) < -0.2, False),
    )
    merged["has_chembl_target"] = merged["chembl_target_id"].fillna("").astype(str).ne("")
    merged["has_activity"] = merged["chembl_activity_count"].fillna(0).astype(float) > 0
    merged["prior_art_heavy"] = (
        merged["europepmc_hit_count"].fillna(0).astype(float) > 500
    ) | (merged["clinicaltrials_hit_count"].fillna(0).astype(float) > 0)

    merged["rescue_score"] = (
        merged["median_efficient_minus_noneater_lfc"].abs().fillna(0)
        + 1.5 * merged["directional_disease_support_count"].fillna(0)
        - 1.5 * merged["directional_conflict_count"].fillna(0)
        + 1.0 * merged["ms_anchor_directional"].astype(float)
        + 1.0 * merged["has_chembl_target"].astype(float)
        + 1.0 * merged["has_activity"].astype(float)
        - 2.0 * merged["prior_art_heavy"].astype(float)
    )

    gate_failures = []
    calls = []
    for _, row in merged.iterrows():
        failures = []
        if row["desired_intervention"] == "unresolved":
            failures.append("screen_direction_unresolved")
        if row.get("n_sgrna", 0) < 3:
            failures.append("too_few_guides")
        if row.get("directional_disease_support_count", 0) < 3:
            failures.append("insufficient_directional_cross_disease_state_support")
        if row.get("directional_conflict_count", 0) >= 2:
            failures.append("disease_state_direction_conflict")
        if not bool(row.get("ms_anchor_directional", False)):
            failures.append("no_ms_directional_anchor")
        if not bool(row.get("has_chembl_target", False)):
            failures.append("no_chembl_target")
        if not bool(row.get("has_activity", False)):
            failures.append("no_chembl_activity")
        if bool(row.get("prior_art_heavy", False)):
            failures.append("prior_art_or_trial_crowded")
        if row.get("efficient_fdr", 1.0) < 0.2 or row.get("noneater_fdr", 1.0) < 0.2 or row.get("contrast_fdr", 1.0) < 0.2:
            screen_support = True
        else:
            screen_support = False
            failures.append("screen_wilcoxon_fdr_not_significant")
        gate_failures.append(";".join(failures))
        if not failures:
            calls.append("PROMOTE_CRISPR_STATE_DRUGGABILITY_RESCUE")
        elif len(failures) <= 2 and screen_support:
            calls.append("PARK_NEEDS_REPLICATION")
        else:
            calls.append("NO_GO_CRISPR_RESCUE")
    merged["gate_failures"] = gate_failures
    merged["wave38_call"] = calls

    merged = merged.sort_values("rescue_score", ascending=False)
    merged.to_csv(OUT / "crispr_state_druggability_rescue_rank.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "n_candidates_scanned": int(len(merged)),
        "call_counts": merged["wave38_call"].value_counts().to_dict(),
        "promoted": merged[merged["wave38_call"].str.startswith("PROMOTE")].head(20).to_dict(orient="records"),
        "top_ranked": merged.head(20).to_dict(orient="records"),
        "interpretation": (
            "A direct efferocytosis CRISPR hit was not sufficient. Promotion "
            "required directional cross-disease state support, MS anchor, "
            "druggability, and tolerable novelty/prior-art burden."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
