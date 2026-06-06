#!/usr/bin/env python3
"""Wave53 perturbation-first pivot audit.

This wave starts from real perturbation effects rather than expression
recurrence. The question is whether any perturbation-positive branch can be
converted into a V3 therapeutic claim after druggability, MS anchoring,
cross-autoimmune breadth, safety, and novelty gates are applied.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave53_perturbation_first_pivot"
RAW = OUT / "raw_api"
SEED = 20260527

INPUTS = {
    "wave15_synthesis": ROOT / "phases/v3/results" / "wave15_perturbation_drug_response" / "candidate_level_synthesis.tsv",
    "wave15_direct": ROOT / "phases/v3/results" / "wave15_perturbation_drug_response" / "ranked_direct_perturbations.tsv",
    "wave18_foundation": ROOT / "phases/v3/results" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv",
    "wave24_l1000": ROOT / "phases/v3/results" / "wave24_l1000_recurrent_reversal" / "recurrent_l1000_mechanism_summary.tsv",
    "wave26_baseline": ROOT / "phases/v3/results" / "wave26_treatment_response_strict_audit" / "strict_baseline_response_audit.tsv",
    "wave34": ROOT / "phases/v3/results" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv",
    "broad_h5ad": ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "broad_residual": ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
}

ROUTES = {
    "MED16_MEDIATOR_MODULE": {
        "genes": ["MED16", "CDK8", "CDK19", "MED12", "CCNC"],
        "perturbations": ["Med16_KO"],
        "intervention": "drug Mediator regulatory machinery, ideally via a selective CDK8/19 or Mediator-module strategy",
        "manual_safety": "high_risk_broad_transcription",
    },
    "GSK3B_INHIBITION": {
        "genes": ["GSK3B"],
        "perturbations": ["Gsk3b_KO", "GSK3B"],
        "intervention": "partial GSK3B inhibition to damp antigen-processing readouts",
        "manual_safety": "pleiotropic_neuroimmune_metabolic",
    },
    "TNFRSF1A_DAMPING": {
        "genes": ["TNFRSF1A"],
        "perturbations": ["TNFRSF1A"],
        "intervention": "modulate TNFR1/TNF pathway output without worsening demyelination",
        "manual_safety": "ms_directionally_unsafe",
    },
    "RFX5_MHCII_PARTIAL_SUPPRESSION": {
        "genes": ["RFX5"],
        "perturbations": ["RFX5"],
        "intervention": "partially suppress RFX5/MHC-II transcriptional output",
        "manual_safety": "antigen_presentation_host_defense",
    },
    "CHUK_IKK_MODULATION": {
        "genes": ["CHUK"],
        "perturbations": ["CHUK"],
        "intervention": "modulate IKK-alpha/NF-kB pathway output",
        "manual_safety": "broad_nfkb_host_defense",
    },
}

PUBLIC_QUERIES = {
    "MED16_MEDIATOR_MODULE": [
        ("EuropePMC", "MED16 Mediator complex autoimmune macrophage antigen presentation"),
        ("EuropePMC", "CDK8 CDK19 inhibitor autoimmune inflammatory disease"),
        ("ClinicalTrials.gov", "CDK8 autoimmune"),
    ],
    "GSK3B_INHIBITION": [
        ("EuropePMC", "GSK3B inhibitor multiple sclerosis autoimmune disease"),
        ("EuropePMC", "lithium glycogen synthase kinase 3 autoimmune encephalomyelitis"),
        ("ClinicalTrials.gov", "GSK3 multiple sclerosis"),
    ],
    "TNFRSF1A_DAMPING": [
        ("EuropePMC", "TNFRSF1A TNFR1 multiple sclerosis anti TNF demyelination"),
        ("EuropePMC", "TNFR1 selective inhibitor autoimmune multiple sclerosis"),
        ("ClinicalTrials.gov", "TNFR1 multiple sclerosis"),
    ],
    "RFX5_MHCII_PARTIAL_SUPPRESSION": [
        ("EuropePMC", "RFX5 MHC class II autoimmune therapeutic target"),
        ("EuropePMC", "RFX5 antigen presentation inhibitor autoimmune disease"),
        ("ClinicalTrials.gov", "RFX5 autoimmune"),
    ],
    "CHUK_IKK_MODULATION": [
        ("EuropePMC", "CHUK IKK alpha inhibitor autoimmune disease"),
        ("EuropePMC", "IKK alpha NF-kB autoimmune therapeutic target"),
        ("ClinicalTrials.gov", "IKK autoimmune"),
    ],
}

PATENT_QUERIES = {
    "MED16_MEDIATOR_MODULE": ["CDK8 inhibitor autoimmune disease", "Mediator complex inhibitor autoimmune"],
    "GSK3B_INHIBITION": ["GSK3 beta inhibitor multiple sclerosis autoimmune", "glycogen synthase kinase 3 inhibitor autoimmune"],
    "TNFRSF1A_DAMPING": ["TNFR1 selective inhibitor multiple sclerosis", "TNFRSF1A autoimmune therapy"],
    "RFX5_MHCII_PARTIAL_SUPPRESSION": ["RFX5 inhibitor autoimmune", "MHC class II transcription inhibitor autoimmune"],
    "CHUK_IKK_MODULATION": ["IKK alpha inhibitor autoimmune", "CHUK inhibitor inflammatory disease"],
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def f(value: Any) -> float | None:
    if value is None or pd.isna(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def s(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value)


def i(value: Any) -> int:
    value_f = f(value)
    return int(value_f) if value_f is not None else 0


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def cache_name(source: str, query: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{source}_{query}")[:180]
    return safe.strip("_") + ".json"


def get_json(url: str, cache_path: Path, timeout: int = 25) -> tuple[int | None, dict[str, Any] | None, str]:
    if cache_path.exists():
        try:
            return 200, json.loads(cache_path.read_text(encoding="utf-8")), "cache"
        except json.JSONDecodeError:
            pass
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "ms-auto-research-wave53/1.0"})
        payload = response.json() if response.text.strip() else {}
        cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(0.15)
        return response.status_code, payload, "live"
    except Exception as exc:  # noqa: BLE001
        payload = {"error": type(exc).__name__, "message": str(exc), "url": url}
        cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return None, payload, "error"


def public_search() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for route, queries in PUBLIC_QUERIES.items():
        for source, query in queries:
            if source == "EuropePMC":
                url = (
                    "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
                    f"?query={quote_plus(query)}&format=json&pageSize=5&resultType=lite"
                )
                status, payload, mode = get_json(url, RAW / cache_name("europepmc", query))
                hits = (((payload or {}).get("resultList") or {}).get("result") or [])
                count = i((payload or {}).get("hitCount"))
                top_hits = " | ".join(
                    f"{h.get('pmid') or h.get('id')}: {h.get('title', '')} ({h.get('pubYear', '')})"
                    for h in hits[:5]
                )
            else:
                url = f"https://clinicaltrials.gov/api/v2/studies?query.term={quote_plus(query)}&pageSize=5"
                status, payload, mode = get_json(url, RAW / cache_name("clinicaltrials", query))
                studies = (payload or {}).get("studies") or []
                count = i((payload or {}).get("totalCount"))
                if count == 0 and studies:
                    count = len(studies)
                top_hits = " | ".join(
                    f"{(study.get('protocolSection') or {}).get('identificationModule', {}).get('nctId', '')}: "
                    f"{(study.get('protocolSection') or {}).get('identificationModule', {}).get('briefTitle', '')}"
                    for study in studies[:5]
                )
            rows.append(
                {
                    "route": route,
                    "source": source,
                    "query": query,
                    "count": count,
                    "top_hits": top_hits,
                    "status": status,
                    "mode": mode,
                    "url": url,
                    "raw_path": rel(RAW / cache_name(source.lower(), query)),
                }
            )
    return pd.DataFrame(rows)


def chembl_gene(gene: str) -> dict[str, Any]:
    target_url = f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={quote_plus(gene)}&limit=10"
    status, payload, mode = get_json(target_url, RAW / cache_name("chembl_target", gene))
    targets = (payload or {}).get("targets") or []
    human = [target for target in targets if s(target.get("organism")).lower() == "homo sapiens"]
    target = human[0] if human else (targets[0] if targets else {})
    target_id = target.get("target_chembl_id") or ""
    activity_url = (
        f"https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id={quote_plus(target_id)}&standard_units=nM&limit=100"
        if target_id
        else ""
    )
    a_status, a_payload, a_mode = (
        get_json(activity_url, RAW / cache_name("chembl_activity", target_id or gene))
        if activity_url
        else (None, {}, "")
    )
    values = [
        f(activity.get("standard_value"))
        for activity in ((a_payload or {}).get("activities") or [])
        if f(activity.get("standard_value")) is not None
    ]
    return {
        "gene": gene,
        "target_chembl_id": target_id,
        "target_name": target.get("pref_name") or "",
        "target_type": target.get("target_type") or "",
        "organism": target.get("organism") or "",
        "target_status": status,
        "target_mode": mode,
        "activity_status": a_status,
        "activity_mode": a_mode,
        "activity_rows_bounded": len(values),
        "best_nM_bounded": min(values) if values else None,
    }


def chembl_summary() -> pd.DataFrame:
    genes = sorted({gene for route in ROUTES.values() for gene in route["genes"]})
    return pd.DataFrame([chembl_gene(gene) for gene in genes])


def patent_urls() -> pd.DataFrame:
    rows: list[dict[str, str]] = []
    for route, queries in PATENT_QUERIES.items():
        for query in queries:
            rows.append({"route": route, "database": "GooglePatents", "query": query, "url": f"https://patents.google.com/?q={quote_plus(query)}"})
            rows.append({"route": route, "database": "Espacenet", "query": query, "url": f"https://worldwide.espacenet.com/patent/search?q={quote_plus(query)}"})
    return pd.DataFrame(rows)


def row_match(df: pd.DataFrame, cols: list[str], tokens: list[str]) -> pd.DataFrame:
    if df.empty:
        return df
    mask = pd.Series(False, index=df.index)
    for col in cols:
        if col not in df.columns:
            continue
        values = df[col].astype(str)
        for token in tokens:
            mask |= values.eq(token)
    return df[mask].copy()


def split_diseases(values: pd.Series) -> set[str]:
    diseases: set[str] = set()
    for value in values.astype(str).tolist():
        if not value or value.lower() == "nan":
            continue
        for part in value.split(";"):
            part = part.strip()
            if part and part.lower() != "nan":
                diseases.add(part)
    return diseases


def local_route_evidence() -> pd.DataFrame:
    frames = {name: read_tsv(path) for name, path in INPUTS.items()}
    rows: list[dict[str, Any]] = []
    for route, cfg in ROUTES.items():
        direct = row_match(frames["wave15_direct"], ["perturbation"], cfg["perturbations"])
        synth = row_match(frames["wave15_synthesis"], ["candidate"], cfg["perturbations"])
        foundation = row_match(frames["wave18_foundation"], ["gene", "best_direct_perturbation"], cfg["genes"] + cfg["perturbations"])
        broad = row_match(frames["broad_h5ad"], ["gene"], cfg["genes"])
        residual = row_match(frames["broad_residual"], ["gene"], cfg["genes"])
        wave34 = row_match(frames["wave34"], ["gene"], cfg["genes"])
        treatment = frames["wave26_baseline"]

        target_suppression = max(
            [f(v) or 0.0 for v in direct.get("target_suppression", pd.Series(dtype=float)).tolist()]
            + [f(v) or 0.0 for v in synth.get("best_direct_target_suppression", pd.Series(dtype=float)).tolist()]
            or [0.0]
        )
        selectivity = max(
            [f(v) or 0.0 for v in direct.get("selectivity_score", pd.Series(dtype=float)).tolist()]
            + [f(v) or 0.0 for v in synth.get("best_direct_selectivity_score", pd.Series(dtype=float)).tolist()]
            or [0.0]
        )
        target_vs_ifn = max(
            [f(v) or -999.0 for v in direct.get("target_vs_ifn_margin", pd.Series(dtype=float)).tolist()]
            + [f(v) or -999.0 for v in synth.get("best_direct_target_vs_ifn_margin", pd.Series(dtype=float)).tolist()]
            or [-999.0]
        )
        direct_sources = ";".join(sorted(set(s(v) for v in synth.get("sources", pd.Series(dtype=str)).tolist() if s(v))))
        direct_calls = ";".join(sorted(set(s(v) for v in synth.get("direct_evidence_calls", pd.Series(dtype=str)).tolist() if s(v))))
        foundation_recommendations = ";".join(sorted(set(s(v) for v in foundation.get("foundation_rescue_recommendation", pd.Series(dtype=str)).tolist() if s(v))))
        foundation_support = int((foundation.get("foundation_rescue_recommendation", pd.Series(dtype=str)).astype(str).str.contains("promote|use_real|triage", case=False, na=False)).sum())
        positive_disease_set = split_diseases(broad.get("positive_diseases", pd.Series(dtype=str)))
        negative_disease_set = split_diseases(broad.get("negative_diseases", pd.Series(dtype=str)))
        local_pos = float(len(positive_disease_set))
        local_neg = float(len(negative_disease_set))
        pos_diseases = ";".join(sorted(positive_disease_set))
        ms_delta = max([f(v) or -999.0 for v in broad.get("ms_wm_delta_log2", pd.Series(dtype=float)).tolist()] or [-999.0])
        ms_p = min([f(v) for v in broad.get("ms_wm_p", pd.Series(dtype=float)).tolist() if f(v) is not None] or [1.0])
        ms_fdr = min([f(v) for v in broad.get("ms_wm_fdr", pd.Series(dtype=float)).tolist() if f(v) is not None] or [1.0])
        strict_residual = max([f(v) or 0.0 for v in residual.get("strict_core_covariate_surviving_disease_count", pd.Series(dtype=float)).tolist()] or [0.0])
        gwas_traits = max([f(v) or 0.0 for v in wave34.get("gwas_catalog_trait_count", pd.Series(dtype=float)).tolist()] or [0.0])
        gwas_min_p = min([f(v) for v in wave34.get("gwas_catalog_min_p", pd.Series(dtype=float)).tolist() if f(v) is not None] or [1.0])
        strict_baseline_claims = 0
        if not treatment.empty:
            strict_baseline_claims = int(treatment.get("strict_claim_allowed", pd.Series(dtype=bool)).astype(str).str.lower().eq("true").sum())
        rows.append(
            {
                "route": route,
                "genes": ";".join(cfg["genes"]),
                "intervention": cfg["intervention"],
                "manual_safety": cfg["manual_safety"],
                "target_suppression": target_suppression,
                "selectivity_score": selectivity,
                "target_vs_ifn_margin": target_vs_ifn,
                "direct_sources": direct_sources,
                "direct_calls": direct_calls,
                "foundation_support_rows": foundation_support,
                "foundation_recommendations": foundation_recommendations,
                "local_positive_disease_count": local_pos,
                "local_negative_disease_count": local_neg,
                "positive_diseases": pos_diseases,
                "ms_wm_delta_log2": ms_delta,
                "ms_wm_p": ms_p,
                "ms_wm_fdr": ms_fdr if ms_fdr < 1.0 else None,
                "strict_residual_disease_count": strict_residual,
                "gwas_trait_count": gwas_traits,
                "gwas_min_p": gwas_min_p,
                "strict_baseline_response_claims_in_wave26": strict_baseline_claims,
            }
        )
    return pd.DataFrame(rows)


@dataclass
class Gate:
    route: str
    gate: str
    passed: bool
    value: str
    rationale: str


def evaluate(local_df: pd.DataFrame, public_df: pd.DataFrame, chembl_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    audits: list[dict[str, Any]] = []
    gates: list[Gate] = []
    for _, row in local_df.iterrows():
        route = s(row["route"])
        cfg = ROUTES[route]
        public = public_df[public_df["route"] == route]
        chembl = chembl_df[chembl_df["gene"].isin(cfg["genes"])]
        emax = int(public.loc[public["source"] == "EuropePMC", "count"].max()) if not public.empty else 0
        ctmax = int(public.loc[public["source"] == "ClinicalTrials.gov", "count"].max()) if not public.empty else 0
        activity_rows = int(max([f(v) or 0.0 for v in chembl.get("activity_rows_bounded", pd.Series(dtype=float)).tolist()] or [0.0]))
        best_nm_vals = [f(v) for v in chembl.get("best_nM_bounded", pd.Series(dtype=float)).tolist() if f(v) is not None]
        best_nm = min(best_nm_vals) if best_nm_vals else None
        chemical_matter = activity_rows >= 10 and best_nm is not None and best_nm <= 1000
        if route == "MED16_MEDIATOR_MODULE":
            chemical_matter = bool(chemical_matter and chembl["gene"].astype(str).isin(["CDK8", "CDK19"]).any())
        real_perturbation = bool(row["target_suppression"] >= 0.75 and row["selectivity_score"] >= 0.5 and row["target_vs_ifn_margin"] > 0.5)
        if route in {"RFX5_MHCII_PARTIAL_SUPPRESSION", "CHUK_IKK_MODULATION"}:
            real_perturbation = bool(row["target_suppression"] >= 0.5 and row["selectivity_score"] >= 0.3)
        foundation_support = bool(row["foundation_support_rows"] >= 1 and "do_not_promote" not in s(row["foundation_recommendations"]).lower())
        cross_disease_local = bool(row["local_positive_disease_count"] >= 3 and row["local_negative_disease_count"] <= 1)
        ms_anchor = bool((f(row["ms_wm_delta_log2"]) or -999.0) > 0 and (f(row["ms_wm_p"]) or 1.0) < 0.05 and (f(row["ms_wm_fdr"]) or 1.0) < 0.1)
        genetics = bool((f(row["gwas_trait_count"]) or 0.0) >= 5 and (f(row["gwas_min_p"]) or 1.0) < 5e-8)
        treatment_anchor = bool((f(row["strict_baseline_response_claims_in_wave26"]) or 0.0) > 0)
        safe_direction = False
        novelty = False
        route_gates = [
            Gate(route, "real_perturbation_selectivity", real_perturbation, f"suppression={row['target_suppression']}; selectivity={row['selectivity_score']}; target_vs_ifn={row['target_vs_ifn_margin']}", "requires real perturbation that suppresses target readout more than generic IFN/stress"),
            Gate(route, "foundation_or_model_support", foundation_support, f"rows={row['foundation_support_rows']}; recommendations={row['foundation_recommendations']}", "requires foundation/model support that is not explicitly do-not-promote"),
            Gate(route, "cross_disease_cell_state_support", cross_disease_local, f"positive={row['local_positive_disease_count']}; negative={row['local_negative_disease_count']}; diseases={row['positive_diseases']}", "requires signal in at least three diseases without contradiction"),
            Gate(route, "strict_ms_anchor", ms_anchor, f"delta={row['ms_wm_delta_log2']}; p={row['ms_wm_p']}; fdr={row['ms_wm_fdr']}", "requires FDR-supported target/intervention-specific MS signal"),
            Gate(route, "genetic_or_response_anchor", bool(genetics or treatment_anchor), f"GWAS_traits={row['gwas_trait_count']}; min_p={row['gwas_min_p']}; strict_response_claims={row['strict_baseline_response_claims_in_wave26']}", "requires genetics or strict treatment-response anchoring"),
            Gate(route, "tractable_druggability", chemical_matter or route in {"TNFRSF1A_DAMPING"}, f"activity_rows={activity_rows}; best_nM={best_nm}; clinical_trials={ctmax}", "requires practical chemical/biologic modality"),
            Gate(route, "safe_selective_direction", safe_direction, s(row["manual_safety"]), "requires directionality that avoids host-defense, demyelination, and broad transcription toxicity"),
            Gate(route, "novelty_prior_art_unblocked", novelty, f"EuropePMC={emax}; ClinicalTrials={ctmax}", "requires a non-blocked novelty delta"),
        ]
        gates.extend(route_gates)
        pass_count = sum(g.passed for g in route_gates)
        if pass_count == len(route_gates):
            call = "PROMOTE_V3_PERTURBATION_FIRST"
        elif route == "MED16_MEDIATOR_MODULE" and real_perturbation:
            call = "WETLAB_ONLY_MED16_SELECTIVE_NONDRUGGABLE_ROUTE"
        elif route == "GSK3B_INHIBITION" and real_perturbation:
            call = "NO_GO_GSK3B_REAL_PERTURBATION_PRIOR_ART_PLEIOTROPY"
        else:
            call = "NO_GO_PERTURBATION_FIRST_PIVOT"
        audit_row = row.to_dict()
        audit_row.update(
            {
                "europepmc_max_count": emax,
                "clinicaltrials_max_count": ctmax,
                "chembl_activity_rows": activity_rows,
                "chembl_best_nM": best_nm,
                "chemical_matter": chemical_matter,
                "call": call,
                "critical_gate_pass_count": pass_count,
                "critical_gate_total": len(route_gates),
                "primary_blocker": primary_blocker(route),
                "decisive_reopen_test": decisive_reopen_test(route),
            }
        )
        audits.append(audit_row)
    return pd.DataFrame(audits), pd.DataFrame([g.__dict__ for g in gates])


def primary_blocker(route: str) -> str:
    return {
        "MED16_MEDIATOR_MODULE": "The real Med16_KO signal is strong, but the route lacks a target-specific MS anchor and a safe selective druggable handle; practical Mediator/CDK8/19 modulation risks broad transcriptional or oncology-like toxicity.",
        "GSK3B_INHIBITION": "Gsk3b_KO has real perturbation support but GSK3B is pleiotropic, prior-art crowded in neuroimmune disease, and locally lacks FDR-supported MS/cross-disease cell-state anchoring.",
        "TNFRSF1A_DAMPING": "TNFRSF1A/TNF perturbation is genetically broad but MS direction is unsafe because TNF blockade can worsen demyelinating biology; local MS expression is negative.",
        "RFX5_MHCII_PARTIAL_SUPPRESSION": "RFX5 is a direct antigen-presentation transcriptional node, but the whole HLA-II axis is already closed for host-defense and nonselective antigen-presentation suppression risk.",
        "CHUK_IKK_MODULATION": "CHUK/IKK-alpha is weakly perturbation-positive but broad NF-kB biology lacks selectivity and novelty.",
    }[route]


def decisive_reopen_test(route: str) -> str:
    return {
        "MED16_MEDIATOR_MODULE": "Perform graded MED16 or Mediator-module perturbation in human primary myeloid cells and MS lesion slice co-culture; require selective MHC-II/lipid-module reduction without loss of viability, housekeeping transcription, phagocytosis, or repair.",
        "GSK3B_INHIBITION": "Use isoform-selective, dose-graded GSK3B perturbation in primary human myeloid/MS lesion organoid systems; reopen only if antigen-processing suppression is separable from WNT/metabolic/neurotoxicity and replicates in MS tissue.",
        "TNFRSF1A_DAMPING": "Only a TNFR1-selective approach that improves MS lesion repair without worsening demyelination in humanized/ex vivo systems would reopen; broad anti-TNF-like effects remain no-go.",
        "RFX5_MHCII_PARTIAL_SUPPRESSION": "Reopen only if tunable RFX5 modulation selectively reduces pathogenic antigen presentation while preserving antimicrobial MHC-II response in primary APCs.",
        "CHUK_IKK_MODULATION": "Reopen only if a selective CHUK-biased intervention suppresses the disease module without broad NF-kB/host-defense loss across primary immune assays.",
    }[route]


def write_report(audit: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = ["# Wave53 Perturbation-First Pivot", "", f"Random seed: `{SEED}`.", "", "## Verdict", ""]
    for _, row in audit.iterrows():
        lines.append(f"- `{row['route']}`: `{row['call']}`; {int(row['critical_gate_pass_count'])}/{int(row['critical_gate_total'])} gates passed.")
        lines.append(f"  - Primary blocker: {row['primary_blocker']}")
        lines.append(f"  - Decisive reopen test: {row['decisive_reopen_test']}")
    lines.extend(["", "## Gate Matrix", ""])
    for _, gate in gates.iterrows():
        status = "PASS" if bool(gate["passed"]) else "FAIL"
        lines.append(f"- `{gate['route']}` / `{gate['gate']}`: {status} (`{gate['value']}`) - {gate['rationale']}.")
    OUT.joinpath("REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    local_df = local_route_evidence()
    public_df = public_search()
    chembl_df = chembl_summary()
    audit, gates = evaluate(local_df, public_df, chembl_df)
    patents = patent_urls()
    local_df.to_csv(OUT / "local_route_evidence.tsv", sep="\t", index=False)
    public_df.to_csv(OUT / "public_api_counts.tsv", sep="\t", index=False)
    chembl_df.to_csv(OUT / "chembl_summary.tsv", sep="\t", index=False)
    patents.to_csv(OUT / "patent_search_urls.tsv", sep="\t", index=False)
    audit.to_csv(OUT / "perturbation_first_audit.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "decision_matrix.tsv", sep="\t", index=False)
    write_report(audit, gates)
    summary = {
        "seed": SEED,
        "promoted_count": int(audit["call"].astype(str).str.contains("PROMOTE").sum()),
        "wetlab_only_count": int(audit["call"].astype(str).str.contains("WETLAB_ONLY").sum()),
        "calls": dict(zip(audit["route"], audit["call"], strict=True)),
        "output_dir": rel(OUT),
        "key_outputs": [
            rel(OUT / "perturbation_first_audit.tsv"),
            rel(OUT / "decision_matrix.tsv"),
            rel(OUT / "REPORT.md"),
        ],
    }
    write_json(OUT / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
