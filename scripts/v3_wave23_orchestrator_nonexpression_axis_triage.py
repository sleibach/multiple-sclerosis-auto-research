#!/usr/bin/env python3
"""Wave23 orchestrator triage for non-expression-first escape routes.

Wave22 closed the strict-residual/druggability branch. This script pivots to
route-level evidence: metabolite/barrier circuits, genetics-first restoration
modalities, and treatment-response/biomarker routes. It uses expression only as
context, not as a promotion gate.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave23_orchestrator_nonexpression_axis_triage"
RAW = OUT / "raw_api"
SEED = 20260527
USER_AGENT = "ms-auto-research-wave23-orchestrator/1.0"

PATHS = {
    "broad_h5ad": ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "broad_residual": ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
    "opentargets_credible": ROOT / "tmp_v3" / "wave13_opentargets_gwas_credible_sets.tsv",
    "wave14_gate": ROOT / "results_v3" / "wave14_candidate_gate_matrix" / "wave14_candidate_gate_matrix.tsv",
    "wave18_foundation": ROOT / "results_v3" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv",
    "wave15_direct_perturb": ROOT
    / "results_v3"
    / "wave15_perturbation_drug_response"
    / "candidate_level_synthesis.tsv",
    "l1000_summary": ROOT / "results_v3" / "l1000fwd_compound_summary.tsv",
    "wave20_genetic": ROOT
    / "results_v3"
    / "wave20_genetic_druggable_altaxis"
    / "negative_ranked_shortlist.tsv",
    "chembl_local": ROOT / "results_v3" / "druggability" / "chembl_target_activity_summary.tsv",
    "treatment_response_ra": ROOT
    / "results_v3"
    / "wave18_treatment_response"
    / "wave18_gse138746_ra_baseline_response_tests.tsv",
    "treatment_response_uc": ROOT
    / "results_v3"
    / "wave18_treatment_response"
    / "wave18_existing_gse253006_uc_summary.tsv",
    "treatment_response_psoriasis": ROOT
    / "results_v3"
    / "wave18_treatment_response"
    / "wave18_gse183047_psoriasis_prepost_tests.tsv",
}


ROUTES = [
    {
        "route": "GPR65_pH_endolysosomal_gpcr",
        "track": "metabolite_barrier_and_genetics",
        "genes": ["GPR65"],
        "direction": "agonize or positively modulate acidic-tissue cAMP signaling if disease variants reduce protective function",
        "modality": "GPCR small-molecule agonist/PAM",
        "manual_prior_status": "crowded",
        "manual_blocker": "GPR65/TDAG8 IBD biology and modulator patents were already identified in Wave20; no new population or non-IBD delta yet.",
    },
    {
        "route": "AHR_tryptophan_barrier_tolerance",
        "track": "metabolite_barrier",
        "genes": ["AHR", "CYP1A1", "CYP1B1"],
        "direction": "activate ligand-dependent epithelial/immune tolerance if local ligand deficiency or barrier readout is demonstrated",
        "modality": "small-molecule AHR ligands or microbiome/metabolite intervention",
        "manual_prior_status": "crowded",
        "manual_blocker": "AHR/tryptophan tolerance is broad autoimmune/IBD/skin prior art; local V3 data do not yet define a new autoimmune subgroup.",
    },
    {
        "route": "FXR_TGR5_bile_acid_axis",
        "track": "metabolite_barrier",
        "genes": ["NR1H4", "GPBAR1", "SLC10A2"],
        "direction": "activate bile-acid receptor signaling in gut/liver immune barrier compartments",
        "modality": "nuclear-receptor or GPCR agonist",
        "manual_prior_status": "crowded",
        "manual_blocker": "Bile-acid receptor agonism is well explored in metabolic/liver/IBD-like inflammation; CNS/MS relevance and cross-autoimmune genetics are weak locally.",
    },
    {
        "route": "PPAR_LXR_cholesterol_efflux",
        "track": "metabolite_barrier",
        "genes": ["PPARA", "PPARD", "PPARG", "NR1H3", "NR1H2", "ABCA1", "ABCG1"],
        "direction": "activate cholesterol-efflux / lipid-resolution programs without broad metabolic toxicity",
        "modality": "PPAR/LXR agonists or selective modulators",
        "manual_prior_status": "crowded",
        "manual_blocker": "Wave19 already demoted PPAR/LXR because chemical matter and autoimmune literature are saturated and systemic metabolic liabilities are large.",
    },
    {
        "route": "SCFA_HCAR_FFAR_barrier_axis",
        "track": "metabolite_barrier",
        "genes": ["HCAR2", "FFAR2", "FFAR3"],
        "direction": "activate microbial-metabolite anti-inflammatory signaling in barrier tissues",
        "modality": "agonists, diet/microbiome-derived metabolite intervention",
        "manual_prior_status": "crowded",
        "manual_blocker": "SCFA/niacin receptor biology is broad and includes fumarate/HCAR2-adjacent MS prior art; local target-level evidence is weak.",
    },
    {
        "route": "S1P_receptor_trafficking_axis",
        "track": "metabolite_barrier",
        "genes": ["S1PR1", "S1PR2", "S1PR3", "S1PR4", "S1PR5"],
        "direction": "modulate lymphocyte trafficking or glial S1P signaling",
        "modality": "S1P receptor modulators",
        "manual_prior_status": "approved_prior_art",
        "manual_blocker": "S1P modulators are approved MS therapies and are not a novel cross-autoimmune discovery route.",
    },
    {
        "route": "VDR_retinoid_barrier_axis",
        "track": "metabolite_barrier",
        "genes": ["VDR", "RXRA", "RXRB", "RARA", "RARB", "RARG"],
        "direction": "activate nuclear-receptor barrier/tolerance programs in deficiency-defined subgroups",
        "modality": "vitamin D/retinoid/nuclear-receptor modulators",
        "manual_prior_status": "crowded",
        "manual_blocker": "Vitamin-D/retinoid autoimmunity literature is saturated; no V3-specific target or patient stratum is established.",
    },
    {
        "route": "eicosanoid_leukotriene_prostaglandin_axis",
        "track": "metabolite_barrier",
        "genes": ["ALOX5", "LTB4R", "LTB4R2", "CYSLTR1", "CYSLTR2", "PTGER2", "PTGER4", "PTGS2"],
        "direction": "block pathogenic lipid mediators or bias pro-resolving receptor signaling",
        "modality": "enzyme inhibitors, GPCR antagonists/agonists",
        "manual_prior_status": "crowded",
        "manual_blocker": "Eicosanoid targeting is broad inflammatory prior art; local V3 data do not identify a non-generic autoimmune module dependency.",
    },
    {
        "route": "PTPN2_TCPTP_restoration",
        "track": "genetics_restoration",
        "genes": ["PTPN2"],
        "direction": "restore TCPTP negative regulation of JAK/STAT/barrier signaling",
        "modality": "restoration/stabilization required; inhibitors are wrong direction",
        "manual_prior_status": "wrong_direction",
        "manual_blocker": "Strong genetics, but therapeutic direction is restoration; no target-selective clinical-ready TCPTP activator/restorer exists.",
    },
    {
        "route": "SH2B3_LNK_restoration",
        "track": "genetics_restoration",
        "genes": ["SH2B3"],
        "direction": "restore LNK cytokine-signaling brake in hematopoietic cells",
        "modality": "protein/RNA/gene restoration would be required",
        "manual_prior_status": "no_modality",
        "manual_blocker": "Broad pleiotropic 12q24 locus and no direct modality for tissue-selective LNK restoration.",
    },
    {
        "route": "TNFAIP3_A20_restoration",
        "track": "genetics_restoration",
        "genes": ["TNFAIP3"],
        "direction": "restore A20 NF-kB/TLR/TNF brake",
        "modality": "restoration or pathway-specific mimicry",
        "manual_prior_status": "no_modality",
        "manual_blocker": "Strong biology but direct A20 restoration is not currently a tractable selective drug modality; prior art is crowded.",
    },
    {
        "route": "CLEC16A_mitophagy_restoration",
        "track": "genetics_restoration",
        "genes": ["CLEC16A"],
        "direction": "restore CLEC16A-linked mitophagy/autophagy quality control",
        "modality": "indirect mitophagy/autophagy modulation",
        "manual_prior_status": "locus_ambiguous",
        "manual_blocker": "16p13 locus ambiguity and no selective CLEC16A drug or target-engagement package.",
    },
    {
        "route": "ATG16L1_xenophagy_restoration",
        "track": "genetics_restoration",
        "genes": ["ATG16L1"],
        "direction": "restore autophagy/xenophagy competence without broad autophagy toxicity",
        "modality": "indirect autophagy modulation",
        "manual_prior_status": "no_selectivity",
        "manual_blocker": "Autophagy modulation is broad; no selective ATG16L1 restoration modality is evident.",
    },
    {
        "route": "IL10_augmentation",
        "track": "genetics_restoration",
        "genes": ["IL10", "IL10RA", "IL10RB"],
        "direction": "augment IL-10 anti-inflammatory signaling in deficient subgroup",
        "modality": "cytokine/agonist/gene delivery",
        "manual_prior_status": "crowded",
        "manual_blocker": "IL-10 augmentation has extensive inflammatory disease prior art and delivery/safety constraints; no V3-defined subgroup yet.",
    },
    {
        "route": "IRF5_CARD9_myeloid_program",
        "track": "genetics_restoration",
        "genes": ["IRF5", "CARD9"],
        "direction": "inhibit pathogenic myeloid inflammatory programming only if independent of generic IFN/NF-kB",
        "modality": "TF/pathway inhibition is difficult; CARD9 pathway modulation indirect",
        "manual_prior_status": "crowded",
        "manual_blocker": "IRF5/CARD9 are known autoimmune/myeloid axes; no cross-disease V3 novelty or direct selectivity package.",
    },
    {
        "route": "baseline_module_response_biomarker",
        "track": "treatment_response_stratification",
        "genes": ["CD74", "IFI30", "CTSS", "LIPA", "APOE", "C1QA", "C1QB", "C1QC", "GPNMB", "SPP1"],
        "direction": "use baseline lipid-lysosomal/APC module to stratify biologic/JAK/S1P/fumarate response",
        "modality": "biomarker, not direct target",
        "manual_prior_status": "needs_prediction",
        "manual_blocker": "Wave18 found no corrected baseline response predictor; only pharmacodynamic comparator signals so far.",
    },
]


def read_table(path: Path, **kwargs: object) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False, **kwargs)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def num(value: object, default: float = 0.0) -> float:
    try:
        val = float(value)
    except (TypeError, ValueError):
        return default
    if np.isnan(val):
        return default
    return val


def split_semicolon(value: object) -> set[str]:
    if value is None:
        return set()
    text = str(value)
    if not text or text.lower() == "nan":
        return set()
    return {part.strip() for part in text.split(";") if part.strip()}


def fetch_json(url: str, cache_path: Path, delay: float = 0.08) -> dict:
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=30) as handle:
        payload = json.loads(handle.read().decode("utf-8"))
    cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    time.sleep(delay)
    return payload


def chembl_api_for_gene(gene: str) -> dict[str, object]:
    RAW.mkdir(parents=True, exist_ok=True)
    search_url = "https://www.ebi.ac.uk/chembl/api/data/target/search.json?" + urlencode(
        {"q": gene, "limit": 10}
    )
    try:
        search = fetch_json(search_url, RAW / f"chembl_search_{gene}.json")
    except Exception as exc:  # noqa: BLE001
        return {"gene": gene, "chembl_error": repr(exc)}
    targets = search.get("targets", [])
    human_targets = [
        t
        for t in targets
        if str(t.get("organism", "")).lower() == "homo sapiens"
        and str(t.get("target_type", "")).upper() in {"SINGLE PROTEIN", "PROTEIN COMPLEX", "PROTEIN FAMILY"}
    ]
    chosen = human_targets[0] if human_targets else (targets[0] if targets else {})
    chembl_id = chosen.get("target_chembl_id", "")
    activity_count = 0
    best_value = np.nan
    if chembl_id:
        activity_url = "https://www.ebi.ac.uk/chembl/api/data/activity.json?" + urlencode(
            {
                "target_chembl_id": chembl_id,
                "limit": 100,
                "standard_type__in": "IC50,EC50,Ki,Kd",
            }
        )
        try:
            activities = fetch_json(activity_url, RAW / f"chembl_activity_{gene}_{chembl_id}.json")
            records = activities.get("activities", [])
            vals = [
                num(r.get("standard_value"), np.nan)
                for r in records
                if str(r.get("standard_units", "")).lower() in {"nm", "nanomolar", ""}
            ]
            vals = [v for v in vals if not np.isnan(v)]
            activity_count = len(records)
            best_value = min(vals) if vals else np.nan
        except Exception as exc:  # noqa: BLE001
            return {
                "gene": gene,
                "chembl_target_id": chembl_id,
                "chembl_pref_name": chosen.get("pref_name", ""),
                "chembl_target_type": chosen.get("target_type", ""),
                "chembl_activity_error": repr(exc),
            }
    return {
        "gene": gene,
        "chembl_target_id": chembl_id,
        "chembl_pref_name": chosen.get("pref_name", ""),
        "chembl_target_type": chosen.get("target_type", ""),
        "chembl_organism": chosen.get("organism", ""),
        "chembl_activity_records_scanned": activity_count,
        "chembl_best_standard_value_nM": best_value,
    }


def gene_evidence(route: dict[str, object], tables: dict[str, pd.DataFrame], chembl_api: dict[str, dict]) -> list[dict]:
    evidence = []
    genes = route["genes"]
    for gene in genes:
        rec: dict[str, object] = {"route": route["route"], "track": route["track"], "gene": gene}

        broad = tables["broad_h5ad"]
        if not broad.empty and "gene" in broad.columns:
            row = broad[broad["gene"].astype(str).str.upper().eq(gene.upper())]
            if not row.empty:
                r = row.iloc[0]
                rec.update(
                    {
                        "expr_positive_disease_count": num(r.get("positive_disease_count")),
                        "expr_negative_disease_count": num(r.get("negative_disease_count")),
                        "expr_positive_diseases": r.get("positive_diseases", ""),
                        "ms_wm_delta_log2": r.get("ms_wm_delta_log2", np.nan),
                        "ms_wm_p": r.get("ms_wm_p", np.nan),
                    }
                )

        residual = tables["broad_residual"]
        if not residual.empty and "gene" in residual.columns:
            row = residual[residual["gene"].astype(str).str.upper().eq(gene.upper())]
            if not row.empty:
                r = row.iloc[0]
                rec.update(
                    {
                        "residual_retained_positive_disease_count": num(r.get("retained_positive_disease_count")),
                        "residual_non_ibd_retained_positive_disease_count": num(
                            r.get("non_ibd_retained_positive_disease_count")
                        ),
                        "strict_core_covariate_surviving_disease_count": num(
                            r.get("strict_core_covariate_surviving_disease_count")
                        ),
                        "strict_core_covariate_surviving_analyses": r.get(
                            "strict_core_covariate_surviving_analyses", ""
                        ),
                    }
                )

        ot = tables["opentargets_credible"]
        if not ot.empty and "approved_symbol" in ot.columns:
            row = ot[ot["approved_symbol"].astype(str).str.upper().eq(gene.upper())]
            if not row.empty:
                rec.update(
                    {
                        "ot_credible_disease_count_ge_0_5": row[row["max_score"].fillna(0) >= 0.5][
                            "disease"
                        ].nunique(),
                        "ot_credible_disease_count_ge_0_8": row[row["max_score"].fillna(0) >= 0.8][
                            "disease"
                        ].nunique(),
                        "ot_credible_max_score": row["max_score"].max(),
                        "ot_credible_diseases_ge_0_5": ";".join(
                            sorted(row[row["max_score"].fillna(0) >= 0.5]["disease"].dropna().astype(str).unique())
                        ),
                    }
                )

        foundation = tables["wave18_foundation"]
        if not foundation.empty and "gene" in foundation.columns:
            row = foundation[foundation["gene"].astype(str).str.upper().eq(gene.upper())]
            if not row.empty:
                r = row.iloc[0]
                rec.update(
                    {
                        "geneformer_support_contexts": num(r.get("total_support_contexts")),
                        "geneformer_strong_support_contexts": num(r.get("total_strong_support_contexts")),
                        "real_perturbation_alignment_call": r.get("real_perturbation_alignment_call", ""),
                        "foundation_rescue_recommendation": r.get("foundation_rescue_recommendation", ""),
                    }
                )

        direct = tables["wave15_direct_perturb"]
        if not direct.empty and "candidate" in direct.columns:
            row = direct[direct["candidate"].astype(str).str.upper().str.replace("_KO", "", regex=False).eq(gene.upper())]
            if not row.empty:
                r = row.iloc[0]
                rec.update(
                    {
                        "direct_perturbation_sources": r.get("sources", ""),
                        "direct_selectivity_score": r.get("best_direct_selectivity_score", np.nan),
                        "direct_evidence_calls": r.get("direct_evidence_calls", ""),
                    }
                )

        local_chembl = tables["chembl_local"]
        if not local_chembl.empty and "gene" in local_chembl.columns:
            row = local_chembl[local_chembl["gene"].astype(str).str.upper().eq(gene.upper())]
            if not row.empty:
                r = row.iloc[0]
                rec.update(
                    {
                        "local_chembl_target_id": r.get("target_chembl_id", ""),
                        "local_chembl_activity_records": num(r.get("activity_records_returned")),
                        "local_chembl_best_nM": r.get("best_standard_value_nM", np.nan),
                    }
                )

        rec.update(chembl_api.get(gene, {}))
        evidence.append(rec)
    return evidence


def score_route(route: dict[str, object], rows: list[dict], tables: dict[str, pd.DataFrame]) -> dict[str, object]:
    genes = route["genes"]
    max_expr = max([num(r.get("expr_positive_disease_count")) for r in rows] or [0])
    max_strict = max([num(r.get("strict_core_covariate_surviving_disease_count")) for r in rows] or [0])
    max_genetics = max([num(r.get("ot_credible_disease_count_ge_0_5")) for r in rows] or [0])
    max_genetics_08 = max([num(r.get("ot_credible_disease_count_ge_0_8")) for r in rows] or [0])
    max_geneformer = max([num(r.get("geneformer_support_contexts")) for r in rows] or [0])
    real_perturb_calls = ";".join(
        sorted({str(r.get("real_perturbation_alignment_call")) for r in rows if r.get("real_perturbation_alignment_call")})
    )
    direct_calls = ";".join(sorted({str(r.get("direct_evidence_calls")) for r in rows if r.get("direct_evidence_calls")}))
    max_chembl_records = max(
        [
            max(num(r.get("local_chembl_activity_records")), num(r.get("chembl_activity_records_scanned")))
            for r in rows
        ]
        or [0]
    )
    best_chembl_nM_values = [
        num(r.get("local_chembl_best_nM"), np.nan)
        for r in rows
        if not np.isnan(num(r.get("local_chembl_best_nM"), np.nan))
    ] + [
        num(r.get("chembl_best_standard_value_nM"), np.nan)
        for r in rows
        if not np.isnan(num(r.get("chembl_best_standard_value_nM"), np.nan))
    ]
    best_chembl_nM = min(best_chembl_nM_values) if best_chembl_nM_values else np.nan

    l1000 = tables["l1000_summary"]
    l1000_hits = 0
    if not l1000.empty:
        text = l1000.astype(str)
        mask = pd.Series(False, index=l1000.index)
        for gene in genes:
            mask = mask | text.apply(lambda col, g=gene: col.str.contains(g, case=False, na=False)).any(axis=1)
        l1000_hits = int(mask.sum())

    # Treatment-response evidence is route-level for the module biomarker.
    treatment_baseline_hits = 0
    treatment_baseline_nominal_hits = 0
    treatment_pharmacodynamic_hits = 0
    if route["track"] == "treatment_response_stratification":
        ra = tables["treatment_response_ra"]
        uc = tables["treatment_response_uc"]
        ps = tables["treatment_response_psoriasis"]
        if not ra.empty:
            fdr = pd.to_numeric(ra.get("fdr"), errors="coerce")
            adj_fdr = pd.to_numeric(ra.get("drug_adjusted_fdr"), errors="coerce")
            p = pd.to_numeric(ra.get("p"), errors="coerce")
            adj_p = pd.to_numeric(ra.get("drug_adjusted_p"), errors="coerce")
            treatment_baseline_hits += int(((fdr < 0.1) | (adj_fdr < 0.1)).sum())
            treatment_baseline_nominal_hits += int(((p < 0.05) | (adj_p < 0.05)).sum())
        if not uc.empty:
            baseline = uc[uc.get("analysis_type", pd.Series(dtype=str)).astype(str).eq("baseline_response")]
            pharm = uc[uc.get("analysis_type", pd.Series(dtype=str)).astype(str).eq("prepost_pharmacodynamic")]
            treatment_baseline_hits += int((pd.to_numeric(baseline.get("fdr"), errors="coerce") < 0.1).sum())
            treatment_baseline_nominal_hits += int((pd.to_numeric(baseline.get("p"), errors="coerce") < 0.05).sum())
            treatment_pharmacodynamic_hits += int((pd.to_numeric(pharm.get("fdr"), errors="coerce") < 0.1).sum())
        if not ps.empty:
            treatment_pharmacodynamic_hits += int((pd.to_numeric(ps.get("fdr"), errors="coerce") < 0.1).sum())

    genetics_score = min(max_genetics, 5.0)
    perturbation_score = 0.0
    if "selective_target_suppression" in direct_calls:
        perturbation_score += 2.5
    if max_geneformer >= 3:
        perturbation_score += 1.0
    if "contradicted" in real_perturb_calls:
        perturbation_score -= 2.0
    druggability_score = 0.0
    if max_chembl_records >= 50:
        druggability_score += 2.0
    elif max_chembl_records > 0:
        druggability_score += 1.0
    if route["modality"] and route["manual_prior_status"] not in {"no_modality", "wrong_direction", "no_selectivity"}:
        druggability_score += 1.0
    response_score = 2.0 if treatment_baseline_hits > 0 else 0.0
    if treatment_pharmacodynamic_hits and not treatment_baseline_hits:
        response_score += 0.5

    penalty = 0.0
    if route["manual_prior_status"] in {"crowded", "approved_prior_art"}:
        penalty += 3.0
    if route["manual_prior_status"] in {"wrong_direction", "no_modality", "no_selectivity", "locus_ambiguous"}:
        penalty += 4.0
    if route["manual_prior_status"] == "needs_prediction":
        penalty += 2.0
    if max_genetics == 0 and route["track"] != "treatment_response_stratification":
        penalty += 1.0
    if perturbation_score <= 0 and route["track"] != "treatment_response_stratification":
        penalty += 1.0

    priority_score = genetics_score + perturbation_score + druggability_score + response_score - penalty

    failures = []
    if route["track"] != "treatment_response_stratification" and max_genetics < 4:
        failures.append("insufficient_cross_disease_genetics")
    if perturbation_score <= 0 and route["track"] != "treatment_response_stratification":
        failures.append("no_positive_independent_perturbation_or_model_alignment")
    if druggability_score < 2 and route["track"] != "treatment_response_stratification":
        failures.append("weak_or_wrong_direction_modality")
    if route["manual_prior_status"] in {"crowded", "approved_prior_art"}:
        failures.append("crowded_or_approved_prior_art")
    if route["manual_prior_status"] in {"wrong_direction", "no_modality", "no_selectivity", "locus_ambiguous"}:
        failures.append(f"modality_blocker_{route['manual_prior_status']}")
    if route["track"] == "treatment_response_stratification" and treatment_baseline_hits == 0:
        failures.append("no_corrected_baseline_response_predictor")

    if not failures and priority_score >= 5:
        call = "GO_REVIEW"
    elif priority_score >= 1 and len(failures) <= 2:
        call = "PARK_REVIEW"
    else:
        call = "NO_GO"

    return {
        "route": route["route"],
        "track": route["track"],
        "genes": ";".join(genes),
        "direction": route["direction"],
        "modality": route["modality"],
        "manual_prior_status": route["manual_prior_status"],
        "manual_blocker": route["manual_blocker"],
        "max_expr_positive_disease_count": max_expr,
        "max_strict_residual_disease_count": max_strict,
        "max_ot_credible_disease_count_ge_0_5": max_genetics,
        "max_ot_credible_disease_count_ge_0_8": max_genetics_08,
        "max_geneformer_support_contexts": max_geneformer,
        "real_perturbation_alignment_calls": real_perturb_calls,
        "direct_perturbation_calls": direct_calls,
        "max_chembl_activity_records": max_chembl_records,
        "best_chembl_nM": best_chembl_nM,
        "l1000_gene_or_target_hits": l1000_hits,
        "treatment_baseline_signal_count": treatment_baseline_hits,
        "treatment_baseline_nominal_signal_count": treatment_baseline_nominal_hits,
        "treatment_pharmacodynamic_signal_count": treatment_pharmacodynamic_hits,
        "genetics_score": genetics_score,
        "perturbation_score": perturbation_score,
        "druggability_score": druggability_score,
        "response_score": response_score,
        "penalty": penalty,
        "priority_score": priority_score,
        "route_call": call,
        "gate_failures": ";".join(failures),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    tables = {name: read_table(path) for name, path in PATHS.items()}

    genes = sorted({gene for route in ROUTES for gene in route["genes"]})
    chembl_api = {gene: chembl_api_for_gene(gene) for gene in genes}
    pd.DataFrame(chembl_api.values()).to_csv(OUT / "chembl_api_target_snapshot.tsv", sep="\t", index=False)

    all_gene_rows = []
    route_rows = []
    for route in ROUTES:
        rows = gene_evidence(route, tables, chembl_api)
        all_gene_rows.extend(rows)
        route_rows.append(score_route(route, rows, tables))

    gene_df = pd.DataFrame(all_gene_rows)
    route_df = pd.DataFrame(route_rows).sort_values(
        ["route_call", "priority_score"], ascending=[True, False]
    )
    # Put reviewable routes first in a stable order.
    call_order = {"GO_REVIEW": 0, "PARK_REVIEW": 1, "NO_GO": 2}
    route_df["_call_order"] = route_df["route_call"].map(call_order).fillna(9)
    route_df = route_df.sort_values(["_call_order", "priority_score"], ascending=[True, False]).drop(columns=["_call_order"])

    gene_df.to_csv(OUT / "wave23_gene_evidence.tsv", sep="\t", index=False)
    route_df.to_csv(OUT / "wave23_route_triage.tsv", sep="\t", index=False)

    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "route_count": int(len(route_df)),
        "gene_count": int(len(genes)),
        "route_call_counts": route_df["route_call"].value_counts().to_dict(),
        "top_routes": route_df.head(8).replace({np.nan: None}).to_dict(orient="records"),
        "interpretation": (
            "No route is promoted by orchestrator triage. The best-scoring routes are genetically "
            "anchored but fail current-modality or prior-art gates, or are druggable but already approved/crowded."
        ),
        "input_paths": {name: rel(path) for name, path in PATHS.items()},
        "output_paths": {
            "route_triage": rel(OUT / "wave23_route_triage.tsv"),
            "gene_evidence": rel(OUT / "wave23_gene_evidence.tsv"),
            "chembl_api_target_snapshot": rel(OUT / "chembl_api_target_snapshot.tsv"),
        },
    }
    write_json(OUT / "summary.json", summary)


if __name__ == "__main__":
    main()
