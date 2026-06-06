#!/usr/bin/env python3
"""Wave23 metabolite-sensing / barrier-repair circuit scout.

This worker asks whether the V3 cross-autoimmune lipid-lysosomal/APC state is
better explained by an upstream metabolite-sensing or barrier-repair circuit
than by a single residual gene. It is deliberately conservative: local V3
recurrence and residual survival are required before public druggability or
prior-art evidence can upgrade a route.
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
OUT = ROOT / "phases/v3/results" / "wave23_metabolite_barrier_circuit"
RAW_API = OUT / "raw_api"
USER_AGENT = "ms-auto-research-wave23-metabolite-barrier-circuit/1.0"
SEED = 20260527

INPUTS = {
    "broad_h5ad": ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "broad_residual_summary": ROOT
    / "phases/v3/results"
    / "broad_residual_gate"
    / "broad_residual_gate_summary.tsv",
    "broad_residual_tests": ROOT
    / "phases/v3/results"
    / "broad_residual_gate"
    / "broad_residual_residual_tests.tsv",
    "wave19_controller": ROOT
    / "phases/v3/results"
    / "wave19_orchestrator_controller_triage"
    / "wave19_controller_triage.tsv",
    "wave19_lysosomal_local": ROOT
    / "phases/v3/results"
    / "wave19_lysosomal_controller"
    / "candidate_local_evidence.tsv",
    "wave19_lysosomal_routes": ROOT
    / "phases/v3/results"
    / "wave19_lysosomal_controller"
    / "route_summary.tsv",
    "ot_credible": ROOT / "phases/v3/tmp" / "wave13_opentargets_gwas_credible_sets.tsv",
    "ot_reopen": ROOT / "phases/v3/tmp" / "wave13_opentargets_reopen_scores.tsv",
    "l1000_compounds": ROOT / "phases/v3/results" / "l1000fwd_compound_summary.tsv",
    "l1000_hits": ROOT / "phases/v3/results" / "l1000fwd_reversal_hits.tsv",
    "wave15_l1000_selectivity": ROOT
    / "phases/v3/results"
    / "wave15_perturbation_drug_response"
    / "l1000fwd_selectivity_compound_rank.tsv",
    "lincs_compoundinfo": ROOT / "data" / "raw_v3" / "lincs2020" / "compoundinfo_beta.txt",
}


ROUTES: dict[str, dict[str, Any]] = {
    "ahr_tryptophan": {
        "route_label": "AHR / tryptophan-kynurenine sensing",
        "genes": [
            "AHR",
            "AHRR",
            "ARNT",
            "IDO1",
            "IDO2",
            "TDO2",
            "KMO",
            "KYNU",
            "HAAO",
            "CYP1A1",
            "CYP1B1",
        ],
        "core_genes": ["AHR", "IDO1", "KYNU", "KMO", "TDO2"],
        "direction": "unclear: AHR/IDO can be tolerogenic, but high IDO1/KYNU is also an IFN/APC activation readout",
        "modality": "AHR agonists/antagonists and IDO/TDO enzyme inhibitors exist; route direction is disease- and ligand-context dependent",
        "delivery": "oral/topical small molecules are feasible, but systemic AHR/tryptophan modulation is pleiotropic",
        "manual_prior_blocker": "AHR/IDO/kynurenine immunoregulation is broad, crowded, and often immunosuppressive rather than a selective barrier-repair control.",
        "manual_crowding": "blocking",
        "query": '("aryl hydrocarbon receptor" OR AHR OR IDO1 OR kynurenine) autoimmune',
        "clinical_query": "AHR IDO autoimmune",
        "patent_query": "AHR IDO autoimmune drug",
        "lincs_terms": [
            "AHR agonist",
            "AHR antagonist",
            "aryl hydrocarbon receptor",
            "IDO inhibitor",
            "kynurenine",
            "tapinarof",
            "laquinimod",
            "tranilast",
            "epacadostat",
            "CH223191",
        ],
    },
    "bile_acid_fxr_tgr5": {
        "route_label": "Bile-acid receptors FXR/TGR5",
        "genes": ["NR1H4", "GPBAR1", "NR0B2"],
        "core_genes": ["NR1H4", "GPBAR1"],
        "direction": "activate gut/liver bile-acid sensing only if it repairs epithelial/myeloid barrier tone without cholestatic liability",
        "modality": "FXR agonists and TGR5 agonist chemistry exist; gut-restricted FXR concepts are plausible",
        "delivery": "oral gut/liver exposure is realistic; CNS and non-gut autoimmune delivery would be indirect",
        "manual_prior_blocker": "This is the least obviously saturated cross-autoimmune route, but local V3 state support is absent and PBC/IBD/metabolic bile-acid art is substantial.",
        "manual_crowding": "medium",
        "query": '("FXR agonist" OR NR1H4 OR GPBAR1 OR TGR5 OR "bile acid receptor") autoimmune OR "inflammatory bowel disease"',
        "clinical_query": "FXR agonist autoimmune inflammatory bowel disease",
        "patent_query": "FXR TGR5 autoimmune inflammatory bowel disease",
        "lincs_terms": [
            "FXR agonist",
            "TGR5 agonist",
            "bile acid receptor",
            "obeticholic acid",
            "chenodeoxycholic acid",
            "ursodeoxycholic acid",
            "tropifexor",
            "fexaramine",
            "INT-777",
        ],
    },
    "ppar_lxr_lipid_nuclear": {
        "route_label": "PPAR/LXR/RXR lipid nuclear receptors",
        "genes": ["PPARA", "PPARD", "PPARG", "NR1H3", "NR1H2", "RXRA", "RXRB", "RXRG", "ABCA1", "ABCG1"],
        "core_genes": ["PPARA", "PPARD", "PPARG", "NR1H3", "NR1H2", "RXRA", "RXRB", "RXRG"],
        "direction": "activate lipid efflux / repair programs, but avoid broad metabolic and lipogenic toxicity",
        "modality": "approved PPAR agonists and preclinical LXR agonists exist; RXR agonists are pleiotropic",
        "delivery": "oral systemic delivery is feasible; tissue-selective immune/barrier delivery is the unsolved part",
        "manual_prior_blocker": "Already demoted in Wave19 for mixed/negative local signal and saturated PPAR/LXR autoimmune/metabolic prior art.",
        "manual_crowding": "blocking",
        "query": '("PPAR gamma" OR PPARG OR "LXR agonist" OR NR1H3 OR NR1H2 OR RXR) autoimmune',
        "clinical_query": "PPAR gamma LXR autoimmune",
        "patent_query": "PPAR LXR autoimmune agonist",
        "lincs_terms": [
            "PPAR agonist",
            "PPAR gamma agonist",
            "LXR agonist",
            "RXR agonist",
            "pioglitazone",
            "rosiglitazone",
            "fenofibrate",
            "bezafibrate",
            "bexarotene",
            "GW3965",
            "T0901317",
        ],
    },
    "scfa_ffar_hcar": {
        "route_label": "SCFA receptors FFAR2/FFAR3/HCAR2",
        "genes": ["FFAR2", "FFAR3", "HCAR2", "HCAR3", "SLC5A8"],
        "core_genes": ["FFAR2", "FFAR3", "HCAR2"],
        "direction": "activate gut-local SCFA/HCAR anti-inflammatory barrier signaling if disease-tissue target engagement is real",
        "modality": "SCFAs, niacin/HCAR2 agonism, and synthetic GPCR ligands exist, but selectivity and exposure are weak",
        "delivery": "gut-local exposure is feasible; systemic cross-autoimmune delivery is nonspecific",
        "manual_prior_blocker": "Microbiome/SCFA and niacin anti-inflammatory routes are crowded and hard to make target-selective.",
        "manual_crowding": "high",
        "query": '("short chain fatty acid receptor" OR FFAR2 OR FFAR3 OR HCAR2 OR GPR109A OR butyrate) autoimmune',
        "clinical_query": "butyrate niacin autoimmune inflammatory bowel disease",
        "patent_query": "FFAR2 HCAR2 autoimmune agonist",
        "lincs_terms": [
            "short chain fatty acid",
            "butyrate",
            "propionate",
            "niacin",
            "nicotinic acid",
            "HCAR2 agonist",
            "GPR109A agonist",
            "FFAR2 agonist",
        ],
    },
    "retinoid_vdr_rxr": {
        "route_label": "Retinoid/RAR/RXR/VDR differentiation-barrier axis",
        "genes": [
            "RARA",
            "RARB",
            "RARG",
            "RXRA",
            "RXRB",
            "RXRG",
            "VDR",
            "CYP27B1",
            "CYP24A1",
            "ALDH1A1",
            "ALDH1A2",
            "ALDH1A3",
        ],
        "core_genes": ["RARA", "RARB", "RARG", "RXRA", "RXRB", "RXRG", "VDR"],
        "direction": "activate differentiation/tolerogenic programs only in tissue contexts where barrier repair, not broad immune suppression, is measured",
        "modality": "retinoids, rexinoids, vitamin-D analogs, and VDR agonists exist",
        "delivery": "oral/topical delivery is feasible, but systemic retinoid/VDR toxicity limits chronic broad autoimmune use",
        "manual_prior_blocker": "Vitamin D, retinoic-acid, and RXR/RAR immunomodulation are very crowded and pleiotropic.",
        "manual_crowding": "blocking",
        "query": '("retinoic acid" OR RARA OR RARG OR RXR OR VDR OR "vitamin D receptor") autoimmune',
        "clinical_query": "retinoic acid vitamin D receptor autoimmune",
        "patent_query": "retinoid VDR autoimmune",
        "lincs_terms": [
            "retinoic acid",
            "retinoid",
            "RAR agonist",
            "RXR agonist",
            "VDR agonist",
            "vitamin D",
            "calcitriol",
            "tretinoin",
            "alitretinoin",
            "bexarotene",
        ],
    },
    "s1p_receptors": {
        "route_label": "S1P receptor trafficking / barrier axis",
        "genes": ["S1PR1", "S1PR2", "S1PR3", "S1PR4", "S1PR5", "SPHK1", "SPHK2", "SGPL1"],
        "core_genes": ["S1PR1", "S1PR2", "S1PR3", "S1PR4", "S1PR5"],
        "direction": "functionally antagonize S1PR1 lymphocyte egress or tune S1P barrier tone; this is not APC-state selective",
        "modality": "approved/clinical S1P receptor modulators exist",
        "delivery": "oral systemic delivery is established; tissue-selective delivery is not the point of current drugs",
        "manual_prior_blocker": "Approved MS and UC S1P modulators make this direct broad immunosuppressive trafficking prior art.",
        "manual_crowding": "blocking",
        "query": '("S1P receptor modulator" OR S1PR1 OR fingolimod OR ozanimod OR etrasimod) autoimmune',
        "clinical_query": "S1P receptor modulator autoimmune",
        "patent_query": "S1P receptor autoimmune modulator",
        "lincs_terms": [
            "S1P receptor modulator",
            "sphingosine-1-phosphate receptor",
            "fingolimod",
            "siponimod",
            "ozanimod",
            "ponesimod",
            "etrasimod",
        ],
    },
    "eicosanoid_receptors": {
        "route_label": "Eicosanoid / leukotriene / prostaglandin sensors",
        "genes": [
            "PTGER1",
            "PTGER2",
            "PTGER3",
            "PTGER4",
            "PTGDR",
            "PTGDR2",
            "PTGIR",
            "PTGFR",
            "TBXA2R",
            "CYSLTR1",
            "CYSLTR2",
            "LTB4R",
            "LTB4R2",
            "OXER1",
            "FPR2",
            "GPR183",
            "PTGS1",
            "PTGS2",
            "ALOX5",
            "ALOX5AP",
            "LTA4H",
        ],
        "core_genes": [
            "PTGER1",
            "PTGER2",
            "PTGER3",
            "PTGER4",
            "CYSLTR1",
            "CYSLTR2",
            "LTB4R",
            "TBXA2R",
            "PTGDR2",
            "LTA4H",
        ],
        "direction": "unclear: inhibit inflammatory leukotrienes/prostaglandins or agonize pro-resolving receptors depending on tissue context",
        "modality": "NSAIDs, leukotriene modifiers, prostanoid receptor ligands, and LTA4H inhibitors provide chemical matter",
        "delivery": "oral/topical/inhaled delivery is feasible; barrier repair and infection/wound-healing liabilities are major",
        "manual_prior_blocker": "Leukotriene/prostaglandin immunology is crowded, directionally contradictory, and not selective for the V3 APC state.",
        "manual_crowding": "high",
        "query": '("leukotriene receptor" OR "prostaglandin receptor" OR PTGER4 OR LTA4H OR CYSLTR1) autoimmune',
        "clinical_query": "leukotriene prostaglandin receptor autoimmune",
        "patent_query": "leukotriene prostaglandin receptor autoimmune",
        "lincs_terms": [
            "leukotriene receptor antagonist",
            "prostaglandin receptor",
            "eicosanoid",
            "LTA4H inhibitor",
            "montelukast",
            "zileuton",
            "celecoxib",
            "NSAID",
            "EP4 antagonist",
            "PTGER4 antagonist",
        ],
    },
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_")[:140]


def read_table(path: Path, **kwargs: Any) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False, **kwargs)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def safe_num(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or (isinstance(value, float) and math.isnan(value)) or pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def safe_int(value: Any) -> int:
    return int(safe_num(value, 0.0))


def split_semicolon(value: Any) -> list[str]:
    if value is None or (isinstance(value, float) and math.isnan(value)) or pd.isna(value):
        return []
    return [part.strip() for part in str(value).split(";") if part.strip()]


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def first_record(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {}
    return df.iloc[0].replace({pd.NA: None}).to_dict()


def get_json_cached(cache_stem: str, url: str, params: dict[str, Any] | None = None, timeout: int = 30) -> Any:
    RAW_API.mkdir(parents=True, exist_ok=True)
    cache_path = RAW_API / f"{slug(cache_stem)}.json"
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    full_url = url
    if params:
        full_url = f"{url}?{urlencode(params)}"
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urlopen(Request(full_url, headers=headers), timeout=timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
            cache_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            return data
        except Exception as exc:
            last_error = exc
            time.sleep(0.75 * (attempt + 1))
    payload = {"error": f"{type(last_error).__name__}: {last_error}", "url": full_url}
    cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def route_gene_map() -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    for route, meta in ROUTES.items():
        for gene in meta["genes"]:
            mapping.setdefault(gene, []).append(route)
    return mapping


def all_candidate_genes() -> list[str]:
    return sorted(route_gene_map())


def local_gene_evidence() -> pd.DataFrame:
    genes = all_candidate_genes()
    gene_to_routes = route_gene_map()

    broad = read_table(INPUTS["broad_h5ad"])
    residual_summary = read_table(INPUTS["broad_residual_summary"])
    residual_tests = read_table(INPUTS["broad_residual_tests"])
    wave19_controller = read_table(INPUTS["wave19_controller"])
    wave19_lysosomal_local = read_table(INPUTS["wave19_lysosomal_local"])
    ot_credible = read_table(INPUTS["ot_credible"])
    ot_reopen = read_table(INPUTS["ot_reopen"])

    rows: list[dict[str, Any]] = []
    for gene in genes:
        row: dict[str, Any] = {
            "gene": gene,
            "routes": ";".join(gene_to_routes[gene]),
        }

        if not broad.empty and "gene" in broad.columns:
            b = broad[broad["gene"].astype(str).str.upper().eq(gene)].head(1)
        else:
            b = pd.DataFrame()
        brec = first_record(b)
        row.update(
            {
                "broad_tested_compartment_count": safe_int(brec.get("tested_compartment_count")),
                "broad_positive_compartment_count": safe_int(brec.get("positive_compartment_count")),
                "broad_negative_compartment_count": safe_int(brec.get("negative_compartment_count")),
                "broad_positive_fdr10_compartment_count": safe_int(brec.get("positive_fdr10_compartment_count")),
                "broad_negative_fdr10_compartment_count": safe_int(brec.get("negative_fdr10_compartment_count")),
                "broad_positive_disease_count": safe_int(brec.get("positive_disease_count")),
                "broad_negative_disease_count": safe_int(brec.get("negative_disease_count")),
                "broad_positive_diseases": brec.get("positive_diseases", ""),
                "broad_negative_diseases": brec.get("negative_diseases", ""),
                "top_positive_compartments": brec.get("top_positive_compartments", ""),
                "ms_wm_delta_log2": safe_num(brec.get("ms_wm_delta_log2"), float("nan")),
                "ms_wm_p": safe_num(brec.get("ms_wm_p"), float("nan")),
                "discovery_priority_score": safe_num(brec.get("discovery_priority_score")),
            }
        )

        if not residual_summary.empty and "gene" in residual_summary.columns:
            rs = residual_summary[residual_summary["gene"].astype(str).str.upper().eq(gene)].head(1)
        else:
            rs = pd.DataFrame()
        rrec = first_record(rs)
        row.update(
            {
                "residual_summary_present": bool(rrec),
                "raw_positive_disease_count": safe_int(rrec.get("raw_positive_disease_count")),
                "retained_positive_disease_count": safe_int(rrec.get("retained_positive_disease_count")),
                "non_ibd_retained_positive_disease_count": safe_int(
                    rrec.get("non_ibd_retained_positive_disease_count")
                ),
                "strict_core_covariate_surviving_disease_count": safe_int(
                    rrec.get("strict_core_covariate_surviving_disease_count")
                ),
                "strict_core_covariate_surviving_analyses": rrec.get("strict_core_covariate_surviving_analyses", ""),
                "top_retained_tests": rrec.get("top_retained_tests", ""),
                "residual_gate_priority_score": safe_num(rrec.get("residual_gate_priority_score")),
            }
        )

        if not residual_tests.empty and "gene" in residual_tests.columns:
            rt = residual_tests[residual_tests["gene"].astype(str).str.upper().eq(gene)].copy()
        else:
            rt = pd.DataFrame()
        if not rt.empty:
            raw_pos = rt[(rt["raw_delta_case_minus_control"].fillna(0) > 0) & (rt["raw_p"].fillna(1) < 0.05)]
            retained = rt[
                (rt["residual_delta_case_minus_control"].fillna(0) > 0)
                & (rt["residual_p"].fillna(1) < 0.05)
                & rt["retains_nominal_positive"].map(as_bool)
            ]
            retained_any = rt[
                (rt["residual_delta_case_minus_control"].fillna(0) > 0)
                & rt["retains_direction_only"].map(as_bool)
            ]
            row.update(
                {
                    "residual_test_rows": len(rt),
                    "residual_raw_positive_diseases_from_tests": ";".join(
                        sorted(raw_pos["disease_name"].dropna().astype(str).unique())
                    ),
                    "residual_retained_positive_diseases_from_tests": ";".join(
                        sorted(retained["disease_name"].dropna().astype(str).unique())
                    ),
                    "residual_direction_retained_diseases_from_tests": ";".join(
                        sorted(retained_any["disease_name"].dropna().astype(str).unique())
                    ),
                    "best_residual_p": safe_num(rt["residual_p"].min(), float("nan")),
                    "best_raw_p": safe_num(rt["raw_p"].min(), float("nan")),
                }
            )
        else:
            row.update(
                {
                    "residual_test_rows": 0,
                    "residual_raw_positive_diseases_from_tests": "",
                    "residual_retained_positive_diseases_from_tests": "",
                    "residual_direction_retained_diseases_from_tests": "",
                    "best_residual_p": "",
                    "best_raw_p": "",
                }
            )

        if not wave19_controller.empty and "gene" in wave19_controller.columns:
            w = wave19_controller[wave19_controller["gene"].astype(str).str.upper().eq(gene)].head(1)
        else:
            w = pd.DataFrame()
        wrec = first_record(w)
        row.update(
            {
                "wave19_controller_call": wrec.get("orchestrator_call", ""),
                "wave19_controller_classes": wrec.get("classes", ""),
                "wave19_controller_local_score": safe_num(wrec.get("local_score")),
                "wave19_residual_state_support_diseases": safe_num(
                    wrec.get("orchestrator_residual_state_support_diseases")
                ),
            }
        )

        if not wave19_lysosomal_local.empty and "gene" in wave19_lysosomal_local.columns:
            wl = wave19_lysosomal_local[wave19_lysosomal_local["gene"].astype(str).str.upper().eq(gene)].head(1)
        else:
            wl = pd.DataFrame()
        wlrec = first_record(wl)
        row.update(
            {
                "wave19_lysosomal_route": wlrec.get("route", ""),
                "wave19_lysosomal_local_call": wlrec.get("local_evidence_call", ""),
            }
        )

        ot_any_diseases: set[str] = set()
        ot_ge05_diseases: set[str] = set()
        ot_max_score = 0.0
        ot_rows = 0
        if not ot_credible.empty:
            ot = ot_credible[ot_credible["query_gene"].astype(str).str.upper().eq(gene)]
            ot_rows += len(ot)
            ot_max_score = max(ot_max_score, safe_num(ot.get("max_score", pd.Series([0])).max()))
            ot_any_diseases.update(
                ot.loc[
                    (ot.get("max_score", 0).fillna(0) > 0) | (ot.get("evidence_count", 0).fillna(0) > 0),
                    "disease",
                ]
                .dropna()
                .astype(str)
            )
            ot_ge05_diseases.update(ot.loc[ot.get("max_score", 0).fillna(0) >= 0.5, "disease"].dropna().astype(str))
        if not ot_reopen.empty:
            ot = ot_reopen[ot_reopen["gene"].astype(str).str.upper().eq(gene)]
            ot_rows += len(ot)
            ot_max_score = max(ot_max_score, safe_num(ot.get("genetic_score", pd.Series([0])).max()))
            ot_any_diseases.update(ot.loc[ot.get("genetic_score", 0).fillna(0) > 0, "disease"].dropna().astype(str))
            ot_ge05_diseases.update(
                ot.loc[ot.get("genetic_score", 0).fillna(0) >= 0.5, "disease"].dropna().astype(str)
            )
        row.update(
            {
                "local_genetics_rows": ot_rows,
                "local_genetics_max_score": ot_max_score,
                "local_genetics_disease_count_any": len(ot_any_diseases),
                "local_genetics_diseases_any": ";".join(sorted(ot_any_diseases)),
                "local_genetics_disease_count_ge_0_5": len(ot_ge05_diseases),
                "local_genetics_diseases_ge_0_5": ";".join(sorted(ot_ge05_diseases)),
            }
        )

        row["expression_only_flag"] = bool(
            row["broad_positive_disease_count"] > 0
            and row["retained_positive_disease_count"] == 0
            and row["strict_core_covariate_surviving_disease_count"] == 0
            and row["local_genetics_disease_count_ge_0_5"] == 0
        )
        rows.append(row)

    return pd.DataFrame(rows).sort_values(
        [
            "strict_core_covariate_surviving_disease_count",
            "retained_positive_disease_count",
            "broad_positive_disease_count",
            "discovery_priority_score",
            "gene",
        ],
        ascending=[False, False, False, False, True],
    )


def text_match(value: Any, terms: list[str]) -> bool:
    text = str(value or "").lower()
    return any(term.lower() in text for term in terms if term)


def target_symbol_match(value: Any, genes: list[str]) -> bool:
    tokens = re.split(r"[^A-Za-z0-9]+", str(value or "").upper())
    return any(gene.upper() in tokens for gene in genes)


def collect_l1000_evidence() -> tuple[pd.DataFrame, pd.DataFrame]:
    l1000_tables = []
    for key in ["l1000_compounds", "wave15_l1000_selectivity"]:
        df = read_table(INPUTS[key])
        if not df.empty:
            df = df.copy()
            df["source_table"] = key
            l1000_tables.append(df)
    l1000 = pd.concat(l1000_tables, ignore_index=True, sort=False) if l1000_tables else pd.DataFrame()
    compoundinfo = read_table(INPUTS["lincs_compoundinfo"])

    match_rows: list[dict[str, Any]] = []
    presence_rows: list[dict[str, Any]] = []

    for route, meta in ROUTES.items():
        genes = meta["genes"]
        terms = meta.get("lincs_terms", []) + meta.get("core_genes", [])
        if not l1000.empty:
            for _, row in l1000.iterrows():
                hay = " ".join(
                    str(row.get(col, ""))
                    for col in ["cmap_name", "target", "moa", "compound_aliases", "pert_id", "query_name"]
                )
                if target_symbol_match(row.get("target", ""), genes) or text_match(hay, terms):
                    match_rows.append(
                        {
                            "route": route,
                            "route_label": meta["route_label"],
                            "source_table": row.get("source_table", ""),
                            "query_name": row.get("query_name", ""),
                            "mode": row.get("mode", ""),
                            "pert_id": row.get("pert_id", ""),
                            "cmap_name": row.get("cmap_name", ""),
                            "target": row.get("target", ""),
                            "moa": row.get("moa", ""),
                            "best_rank": row.get("best_rank", ""),
                            "min_qval": row.get("min_qval", ""),
                            "max_abs_combined_score": row.get("max_abs_combined_score", ""),
                            "target_antigen_presentation_best_rank": row.get(
                                "target_antigen_presentation_best_rank", ""
                            ),
                            "target_antigen_presentation_min_qval": row.get(
                                "target_antigen_presentation_min_qval", ""
                            ),
                            "l1000_selectivity_call": row.get("l1000_selectivity_call", ""),
                        }
                    )
        if not compoundinfo.empty:
            keep = []
            for _, row in compoundinfo.iterrows():
                hay = " ".join(
                    str(row.get(col, "")) for col in ["cmap_name", "target", "moa", "compound_aliases", "pert_id"]
                )
                if target_symbol_match(row.get("target", ""), genes) or text_match(hay, terms):
                    keep.append(row)
            for row in keep[:50]:
                presence_rows.append(
                    {
                        "route": route,
                        "route_label": meta["route_label"],
                        "pert_id": row.get("pert_id", ""),
                        "cmap_name": row.get("cmap_name", ""),
                        "target": row.get("target", ""),
                        "moa": row.get("moa", ""),
                        "compound_aliases": row.get("compound_aliases", ""),
                    }
                )
            if len(keep) > 50:
                presence_rows.append(
                    {
                        "route": route,
                        "route_label": meta["route_label"],
                        "pert_id": "",
                        "cmap_name": f"{len(keep) - 50} additional matching LINCS metadata rows omitted",
                        "target": "",
                        "moa": "",
                        "compound_aliases": "",
                    }
                )

    matches = pd.DataFrame(match_rows)
    presence = pd.DataFrame(presence_rows)
    return matches, presence


def europepmc_snapshot(route: str, query: str) -> dict[str, Any]:
    data = get_json_cached(
        f"europepmc_{route}",
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
        {"query": query, "format": "json", "pageSize": 3, "resultType": "lite"},
        timeout=40,
    )
    examples = []
    for item in data.get("resultList", {}).get("result", []):
        url = ""
        if item.get("pmcid"):
            url = f"https://pmc.ncbi.nlm.nih.gov/articles/{item['pmcid']}/"
        elif item.get("id") and item.get("source") == "MED":
            url = f"https://pubmed.ncbi.nlm.nih.gov/{item['id']}/"
        elif item.get("doi"):
            url = f"https://doi.org/{item['doi']}"
        examples.append(
            {
                "id": item.get("id", ""),
                "source": item.get("source", ""),
                "title": item.get("title", ""),
                "journal": item.get("journalTitle", ""),
                "year": item.get("pubYear", ""),
                "doi": item.get("doi", ""),
                "url": url,
            }
        )
    return {
        "hit_count": safe_int(data.get("hitCount")),
        "url": f"https://europepmc.org/search?query={quote_plus(query)}",
        "examples": examples,
        "status": "error" if "error" in data else "ok",
    }


def clinical_trials_snapshot(route: str, term: str) -> dict[str, Any]:
    data = get_json_cached(
        f"clinicaltrials_{route}",
        "https://clinicaltrials.gov/api/v2/studies",
        {"query.term": term, "pageSize": 5, "format": "json"},
        timeout=40,
    )
    studies = []
    for study in data.get("studies", []):
        protocol = study.get("protocolSection", {})
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
                "interventions": ";".join(item.get("name", "") for item in interventions),
            }
        )
    return {
        "hit_count": safe_int(data.get("totalCount", len(studies))),
        "returned_count": len(studies),
        "url": f"https://clinicaltrials.gov/search?term={quote_plus(term)}",
        "studies": studies,
        "status": "error" if "error" in data else "ok",
    }


def chembl_target_search(gene: str) -> dict[str, Any]:
    data = get_json_cached(
        f"chembl_target_{gene}",
        "https://www.ebi.ac.uk/chembl/api/data/target/search.json",
        {"q": gene, "limit": 20},
        timeout=40,
    )
    hits = []
    for target in data.get("targets", []):
        components = target.get("target_components") or []
        symbols: set[str] = set()
        accessions: set[str] = set()
        for component in components:
            if component.get("accession"):
                accessions.add(component["accession"])
            for synonym in component.get("target_component_synonyms") or []:
                if synonym.get("syn_type") == "GENE_SYMBOL":
                    symbols.add(str(synonym.get("component_synonym", "")))
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
    best: dict[str, Any] = {}
    for hit in hits:
        symbols = set(hit["gene_symbols"].split(";")) if hit["gene_symbols"] else set()
        if gene in symbols and hit["organism"] == "Homo sapiens" and hit["target_type"] == "SINGLE PROTEIN":
            best = hit
            break
    if not best:
        for hit in hits:
            if hit["organism"] == "Homo sapiens" and hit["target_type"] == "SINGLE PROTEIN":
                best = hit
                break
    if not best and hits:
        best = hits[0]
    return {
        "best": best,
        "n_search_hits": len(hits),
        "status": "error" if "error" in data else "ok",
        "search_url": f"https://www.ebi.ac.uk/chembl/g/#search_results/all/query={quote_plus(gene)}",
    }


def chembl_activity_count(gene: str, target_chembl_id: str | None) -> dict[str, Any]:
    if not target_chembl_id:
        return {"activity_records": 0, "activity_url": "", "status": "no_target"}
    data = get_json_cached(
        f"chembl_activity_{gene}_{target_chembl_id}",
        "https://www.ebi.ac.uk/chembl/api/data/activity.json",
        {"target_chembl_id": target_chembl_id, "standard_units": "nM", "limit": 1},
        timeout=40,
    )
    return {
        "activity_records": safe_int(data.get("page_meta", {}).get("total_count")),
        "activity_url": f"https://www.ebi.ac.uk/chembl/g/#browse/activities/filter/target_chembl_id%3A{target_chembl_id}",
        "status": "error" if "error" in data else "ok",
    }


def public_prior_art_audit() -> pd.DataFrame:
    rows = []
    for route, meta in ROUTES.items():
        epmc = europepmc_snapshot(route, meta["query"])
        trials = clinical_trials_snapshot(route, meta["clinical_query"])
        rows.append(
            {
                "route": route,
                "route_label": meta["route_label"],
                "europepmc_query": meta["query"],
                "europepmc_hit_count": epmc["hit_count"],
                "europepmc_url": epmc["url"],
                "europepmc_examples_json": json.dumps(epmc["examples"], sort_keys=True),
                "clinicaltrials_query": meta["clinical_query"],
                "clinicaltrials_hit_count": trials["hit_count"],
                "clinicaltrials_returned_count": trials["returned_count"],
                "clinicaltrials_url": trials["url"],
                "clinicaltrials_examples_json": json.dumps(trials["studies"], sort_keys=True),
                "google_patents_url": f"https://patents.google.com/?q={quote_plus(meta['patent_query'])}",
                "manual_prior_blocker": meta["manual_prior_blocker"],
                "manual_crowding": meta["manual_crowding"],
                "api_status": f"EuropePMC={epmc['status']};ClinicalTrials={trials['status']}",
            }
        )
        time.sleep(0.15)
    return pd.DataFrame(rows)


def chembl_audit() -> pd.DataFrame:
    rows = []
    for gene in all_candidate_genes():
        target = chembl_target_search(gene)
        best = target["best"] or {}
        activity = chembl_activity_count(gene, best.get("target_chembl_id"))
        rows.append(
            {
                "gene": gene,
                "routes": ";".join(route_gene_map().get(gene, [])),
                "target_chembl_id": best.get("target_chembl_id", ""),
                "pref_name": best.get("pref_name", ""),
                "target_type": best.get("target_type", ""),
                "organism": best.get("organism", ""),
                "accessions": best.get("accessions", ""),
                "gene_symbols": best.get("gene_symbols", ""),
                "chembl_search_hit_count": target["n_search_hits"],
                "chembl_activity_records_nM": activity["activity_records"],
                "chembl_search_url": target["search_url"],
                "chembl_activity_url": activity["activity_url"],
                "api_status": f"target={target['status']};activity={activity['status']}",
            }
        )
        time.sleep(0.15)
    return pd.DataFrame(rows).sort_values(["chembl_activity_records_nM", "gene"], ascending=[False, True])


def route_local_summary(gene_evidence: pd.DataFrame) -> pd.DataFrame:
    rows = []
    wave19_routes = read_table(INPUTS["wave19_lysosomal_routes"])
    for route, meta in ROUTES.items():
        sub = gene_evidence[gene_evidence["routes"].astype(str).str.contains(route, regex=False)].copy()
        pos_diseases: set[str] = set()
        neg_diseases: set[str] = set()
        retained_diseases: set[str] = set()
        direction_retained_diseases: set[str] = set()
        genetics_diseases: set[str] = set()
        strict_analyses: list[str] = []
        for _, row in sub.iterrows():
            pos_diseases.update(split_semicolon(row.get("broad_positive_diseases")))
            neg_diseases.update(split_semicolon(row.get("broad_negative_diseases")))
            retained_diseases.update(split_semicolon(row.get("residual_retained_positive_diseases_from_tests")))
            direction_retained_diseases.update(split_semicolon(row.get("residual_direction_retained_diseases_from_tests")))
            genetics_diseases.update(split_semicolon(row.get("local_genetics_diseases_ge_0_5")))
            strict_analyses.extend(split_semicolon(row.get("strict_core_covariate_surviving_analyses")))

        wave19_note = ""
        if not wave19_routes.empty and "route" in wave19_routes.columns:
            if route == "ppar_lxr_lipid_nuclear":
                w = wave19_routes[
                    wave19_routes["route"].astype(str).eq("PPAR_LXR_cholesterol_efflux_activation")
                ].head(1)
                if not w.empty:
                    rec = first_record(w)
                    wave19_note = f"{rec.get('route_call', '')}: {rec.get('blocking_issue', '')}"

        rows.append(
            {
                "route": route,
                "route_label": meta["route_label"],
                "genes_present_in_broad_h5ad": int((sub["broad_tested_compartment_count"].fillna(0) > 0).sum()),
                "max_gene_broad_positive_disease_count": int(sub["broad_positive_disease_count"].fillna(0).max())
                if not sub.empty
                else 0,
                "route_positive_disease_union_count": len(pos_diseases),
                "route_positive_disease_union": ";".join(sorted(pos_diseases)),
                "route_negative_disease_union_count": len(neg_diseases),
                "route_negative_disease_union": ";".join(sorted(neg_diseases)),
                "genes_with_any_broad_positive": int((sub["broad_positive_disease_count"].fillna(0) > 0).sum()),
                "genes_with_broad_positive_ge3_diseases": int(
                    (sub["broad_positive_disease_count"].fillna(0) >= 3).sum()
                ),
                "genes_with_expression_only_flag": int(sub["expression_only_flag"].fillna(False).sum()),
                "retained_positive_disease_union_count": len(retained_diseases),
                "retained_positive_disease_union": ";".join(sorted(retained_diseases)),
                "direction_retained_disease_union_count": len(direction_retained_diseases),
                "direction_retained_disease_union": ";".join(sorted(direction_retained_diseases)),
                "strict_core_covariate_surviving_gene_count": int(
                    (sub["strict_core_covariate_surviving_disease_count"].fillna(0) > 0).sum()
                ),
                "strict_core_covariate_surviving_disease_max": int(
                    sub["strict_core_covariate_surviving_disease_count"].fillna(0).max()
                )
                if not sub.empty
                else 0,
                "strict_core_covariate_surviving_analyses": ";".join(sorted(set(strict_analyses))),
                "local_genetics_ge_0_5_disease_union_count": len(genetics_diseases),
                "local_genetics_ge_0_5_disease_union": ";".join(sorted(genetics_diseases)),
                "max_local_genetics_score": safe_num(sub["local_genetics_max_score"].max()) if not sub.empty else 0,
                "best_ms_wm_delta_log2": safe_num(sub["ms_wm_delta_log2"].max(), float("nan")) if not sub.empty else "",
                "best_ms_wm_p": safe_num(sub["ms_wm_p"].min(), float("nan")) if not sub.empty else "",
                "wave19_prior_route_note": wave19_note,
                "direction": meta["direction"],
                "modality": meta["modality"],
                "delivery": meta["delivery"],
            }
        )
    return pd.DataFrame(rows)


def route_l1000_summary(matches: pd.DataFrame, presence: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for route, meta in ROUTES.items():
        m = matches[matches["route"].eq(route)] if not matches.empty else pd.DataFrame()
        p = presence[presence["route"].eq(route)] if not presence.empty else pd.DataFrame()
        opposite = m[m.get("mode", pd.Series([], dtype=str)).astype(str).eq("opposite")] if not m.empty else pd.DataFrame()
        sig = opposite[opposite.get("min_qval", pd.Series([], dtype=float)).fillna(1) <= 0.05] if not opposite.empty else pd.DataFrame()
        selectivity = (
            m[m.get("target_antigen_presentation_min_qval", pd.Series([], dtype=float)).fillna(1) <= 0.05]
            if not m.empty
            else pd.DataFrame()
        )
        rows.append(
            {
                "route": route,
                "route_label": meta["route_label"],
                "l1000_local_match_count": len(m),
                "l1000_opposite_match_count": len(opposite),
                "l1000_opposite_qval_le_0_05_count": len(sig),
                "wave15_target_antigen_qval_le_0_05_count": len(selectivity),
                "best_l1000_opposite_rank": safe_num(opposite["best_rank"].min(), float("nan"))
                if not opposite.empty and "best_rank" in opposite.columns
                else "",
                "best_l1000_opposite_qval": safe_num(opposite["min_qval"].min(), float("nan"))
                if not opposite.empty and "min_qval" in opposite.columns
                else "",
                "lincs_metadata_presence_count_capped": len(p),
                "example_lincs_compounds": ";".join(
                    p["cmap_name"].dropna().astype(str).head(8).tolist()
                )
                if not p.empty and "cmap_name" in p.columns
                else "",
            }
        )
    return pd.DataFrame(rows)


def route_chembl_summary(chembl: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for route, meta in ROUTES.items():
        genes = set(meta["genes"])
        sub = chembl[chembl["gene"].isin(genes)].copy()
        druggable_genes = sub[sub["chembl_activity_records_nM"].fillna(0) > 0]
        top = (
            druggable_genes.sort_values("chembl_activity_records_nM", ascending=False)
            .head(8)
            .apply(lambda r: f"{r['gene']}:{safe_int(r['chembl_activity_records_nM'])}", axis=1)
            .tolist()
        )
        rows.append(
            {
                "route": route,
                "route_label": meta["route_label"],
                "genes_with_chembl_target": int((sub["target_chembl_id"].astype(str) != "").sum()),
                "genes_with_chembl_activity": len(druggable_genes),
                "max_chembl_activity_records_nM": int(sub["chembl_activity_records_nM"].fillna(0).max())
                if not sub.empty
                else 0,
                "top_chembl_activity_genes": ";".join(top),
            }
        )
    return pd.DataFrame(rows)


def decide_routes(
    local: pd.DataFrame,
    l1000: pd.DataFrame,
    chembl: pd.DataFrame,
    prior: pd.DataFrame,
) -> pd.DataFrame:
    merged = local.merge(l1000, on=["route", "route_label"], how="left")
    merged = merged.merge(chembl, on=["route", "route_label"], how="left")
    merged = merged.merge(prior, on=["route", "route_label"], how="left")

    rows = []
    for _, row in merged.iterrows():
        route = str(row["route"])
        meta = ROUTES[route]
        local_expression = safe_int(row.get("route_positive_disease_union_count")) > 0
        residual_support = safe_int(row.get("strict_core_covariate_surviving_disease_max")) > 0 or safe_int(
            row.get("retained_positive_disease_union_count")
        ) >= 2
        genetics_support = safe_int(row.get("local_genetics_ge_0_5_disease_union_count")) >= 2
        l1000_support = safe_int(row.get("l1000_opposite_qval_le_0_05_count")) > 0 or safe_int(
            row.get("wave15_target_antigen_qval_le_0_05_count")
        ) > 0
        druggable = safe_int(row.get("genes_with_chembl_activity")) > 0 or meta["manual_crowding"] in {
            "high",
            "blocking",
            "medium",
        }
        crowded = (
            meta["manual_crowding"] == "blocking"
            or safe_int(row.get("clinicaltrials_hit_count")) > 0
            or safe_int(row.get("europepmc_hit_count")) >= 1000
        )
        expression_only_kill = local_expression and not residual_support and not genetics_support and not l1000_support
        no_local_support = not local_expression and not residual_support and not genetics_support

        blockers = []
        positive = []
        if residual_support:
            positive.append("some residual retention")
        else:
            blockers.append("no strict/residual route support")
        if genetics_support:
            positive.append("multi-disease local genetics")
        else:
            blockers.append("no local multi-disease genetics")
        if l1000_support:
            positive.append("local L1000/perturbation match")
        else:
            blockers.append("no disease-signature L1000 support")
        if druggable:
            positive.append("druggable chemical/modality precedent")
        else:
            blockers.append("weak direct druggability")
        if crowded:
            blockers.append("crowded or blocking prior art")
        if expression_only_kill:
            blockers.append("expression-only route under V3 gates")
        if no_local_support:
            blockers.append("absent/near-absent local recurrence")

        if route == "bile_acid_fxr_tgr5" and no_local_support and not l1000_support:
            call = "PARK"
            rationale = (
                "Least crowded and most gut-deliverable of this panel, but local V3 recurrence/residual evidence is absent; "
                "park only for future metabolomics or gut-restricted perturbation data."
            )
        elif expression_only_kill or meta["manual_crowding"] == "blocking" or crowded or no_local_support:
            call = "NO_GO"
            rationale = "; ".join(blockers[:5])
        elif residual_support and (genetics_support or l1000_support) and druggable and not crowded:
            call = "GO"
            rationale = "; ".join(positive)
        else:
            call = "PARK"
            rationale = "; ".join(blockers[:4])

        rank_score = (
            2.0 * safe_num(row.get("strict_core_covariate_surviving_disease_max"))
            + safe_num(row.get("retained_positive_disease_union_count"))
            + 0.5 * safe_num(row.get("route_positive_disease_union_count"))
            + 2.0 * safe_num(row.get("local_genetics_ge_0_5_disease_union_count"))
            + 2.0 * safe_num(row.get("l1000_opposite_qval_le_0_05_count"))
            + min(safe_num(row.get("genes_with_chembl_activity")), 3.0)
            - (4.0 if meta["manual_crowding"] == "blocking" else 0.0)
            - (2.0 if crowded else 0.0)
            - (2.0 if expression_only_kill else 0.0)
            - (1.0 if no_local_support else 0.0)
        )
        if call == "PARK":
            rank_score += 1.0
        elif call == "GO":
            rank_score += 3.0

        out = row.to_dict()
        out.update(
            {
                "rank_score": round(rank_score, 3),
                "gate_call": call,
                "gate_rationale": rationale,
                "expression_only_kill": expression_only_kill,
                "crowded_prior_art_flag": crowded,
                "manual_prior_blocker": meta["manual_prior_blocker"],
                "not_already_crowded_assessment": "least_crowded_but_unsupported"
                if route == "bile_acid_fxr_tgr5"
                else ("no" if crowded or meta["manual_crowding"] in {"high", "blocking"} else "unclear"),
            }
        )
        rows.append(out)

    call_order = {"GO": 0, "PARK": 1, "NO_GO": 2}
    result = pd.DataFrame(rows)
    result["call_sort"] = result["gate_call"].map(call_order).fillna(9)
    return result.sort_values(["call_sort", "rank_score", "route"], ascending=[True, False, True]).drop(
        columns=["call_sort"]
    )


def source_links(prior: pd.DataFrame, chembl: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, row in prior.iterrows():
        rows.append(
            {
                "scope": row["route"],
                "source": "EuropePMC API",
                "query": row["europepmc_query"],
                "url": row["europepmc_url"],
                "used_for": "prior-art/crowding snapshot",
            }
        )
        rows.append(
            {
                "scope": row["route"],
                "source": "ClinicalTrials.gov API v2",
                "query": row["clinicaltrials_query"],
                "url": row["clinicaltrials_url"],
                "used_for": "clinical prior-art snapshot",
            }
        )
        rows.append(
            {
                "scope": row["route"],
                "source": "Google Patents search URL",
                "query": ROUTES[row["route"]]["patent_query"],
                "url": row["google_patents_url"],
                "used_for": "patent-search pointer; not counted as fetched evidence",
            }
        )
    for _, row in chembl.iterrows():
        if str(row.get("target_chembl_id", "")):
            rows.append(
                {
                    "scope": row["gene"],
                    "source": "ChEMBL API",
                    "query": row["gene"],
                    "url": row["chembl_activity_url"] or row["chembl_search_url"],
                    "used_for": "target/druggability snapshot",
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW_API.mkdir(parents=True, exist_ok=True)

    gene_evidence = local_gene_evidence()
    gene_evidence.to_csv(OUT / "candidate_gene_local_evidence.tsv", sep="\t", index=False)

    l1000_matches, lincs_presence = collect_l1000_evidence()
    l1000_matches.to_csv(OUT / "route_l1000_matches.tsv", sep="\t", index=False)
    lincs_presence.to_csv(OUT / "lincs_compound_presence.tsv", sep="\t", index=False)
    l1000_summary = route_l1000_summary(l1000_matches, lincs_presence)
    l1000_summary.to_csv(OUT / "route_l1000_summary.tsv", sep="\t", index=False)

    public_prior = public_prior_art_audit()
    public_prior.to_csv(OUT / "route_public_api_audit.tsv", sep="\t", index=False)

    chembl = chembl_audit()
    chembl.to_csv(OUT / "chembl_target_snapshot.tsv", sep="\t", index=False)
    chembl_summary = route_chembl_summary(chembl)
    chembl_summary.to_csv(OUT / "route_chembl_summary.tsv", sep="\t", index=False)

    local_summary = route_local_summary(gene_evidence)
    local_summary.to_csv(OUT / "route_local_summary.tsv", sep="\t", index=False)

    ranked = decide_routes(local_summary, l1000_summary, chembl_summary, public_prior)
    ranked.to_csv(OUT / "wave23_ranked_routes.tsv", sep="\t", index=False)

    links = source_links(public_prior, chembl)
    links.to_csv(OUT / "source_links.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "inputs": {key: rel(path) for key, path in INPUTS.items() if path.exists()},
        "output_dir": rel(OUT),
        "candidate_gene_count": len(all_candidate_genes()),
        "route_count": len(ROUTES),
        "gate_call_counts": ranked["gate_call"].value_counts().to_dict(),
        "go_routes": ranked.loc[ranked["gate_call"].eq("GO"), "route"].tolist(),
        "park_routes": ranked.loc[ranked["gate_call"].eq("PARK"), "route"].tolist(),
        "no_go_routes": ranked.loc[ranked["gate_call"].eq("NO_GO"), "route"].tolist(),
        "top_routes": ranked[["route", "gate_call", "rank_score", "gate_rationale"]].head(10).to_dict(
            orient="records"
        ),
    }
    write_json(OUT / "summary.json", summary)


if __name__ == "__main__":
    main()
