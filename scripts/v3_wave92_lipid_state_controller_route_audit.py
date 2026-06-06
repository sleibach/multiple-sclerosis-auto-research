#!/usr/bin/env python3
"""Wave92 controller-route audit for the lipid-loader/lysosomal state.

Wave91 closed direct nomination of measured module genes. This script moves one
layer away from markers and tests candidate controller routes that could
regulate entry, persistence, or resolution of the lipid-loader/lysosomal myeloid
state.

The operationalization is route-level:

- anti-TNF baseline response association in external IBD, RA, and psoriasis;
- MS white-matter route-level expression support;
- broad h5ad disease-vs-control route recurrence;
- prior V3 route feasibility status.

This is deliberately not a claim generator. A route can only reopen if it has
cross-disease response support, MS anchoring, atlas support, and no prior-art or
translation blocker.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from v3_analyze_direct_h5ad_cell_states import ROOT
from v3_wave85_external_geo_antitnf_validation import (
    GPL570_ANNOT,
    SERIES_FILES,
    bh,
    cohort_specs,
    expression_to_gene_level as ibd_expression_to_gene_level,
    hedges_g,
    mask_for_spec,
    markdown_table,
    patient_level_scores,
    read_gpl570_gene_map,
    read_series_matrix as read_ibd_series_matrix,
    rel,
    residualize,
    sample_metadata as ibd_sample_metadata,
    write_json,
    zscore_rows,
)
from v3_wave89_psoriasis_gse85034_response_validation import (
    GPL10558_ANNOT,
    SERIES as PSO_SERIES,
    build_patient_response_table,
    expression_to_gene_level as pso_expression_to_gene_level,
    read_gpl10558_gene_map,
    read_series_matrix as read_pso_series_matrix,
    sample_metadata as pso_sample_metadata,
)


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave92_lipid_state_controller_route_audit"

RA_COUNTS = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"
MS_WM = ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv"
BROAD_H5AD = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
W30 = ROOT / "phases/v3/results" / "wave30_niche_driver_audit" / "niche_driver_axis_audit.tsv"
W32 = ROOT / "phases/v3/results" / "wave32c_resolution_prior_art_audit" / "route_feasibility_ranked.tsv"
W48 = ROOT / "phases/v3/results" / "wave48_resolution_reopener_audit" / "route_reopener_audit.tsv"
W74 = ROOT / "phases/v3/results" / "wave74_gpr183_oxysterol_niche" / "integrated_decision.tsv"


ROUTES: dict[str, dict[str, Any]] = {
    "FPR2_ANXA1_BIASED_RESOLUTION": {
        "genes": ["FPR2", "ANXA1"],
        "intervention_direction": "biased_agonism_or_resolution_enhancement",
        "prior_status": "NOT_BLOCKED_BUT_IMMATURE",
        "route_note": "least-blocked pro-resolution/efferocytosis route from Wave48, but prior art and weak MS anchor remain concerns",
    },
    "CD300_RECEPTOR_SPECIFIC_TUNING": {
        "genes": ["CD300A", "CD300C", "CD300E", "CD300LF", "CD300LG"],
        "intervention_direction": "receptor_specific_agonism_or_inhibitory_tuning",
        "prior_status": "NOT_BLOCKED_BUT_DIRECTION_AMBIGUOUS",
        "route_note": "lipid/efferocytosis receptor family with unresolved receptor-specific direction",
    },
    "GPR65_ENDOLYSOSOMAL_PH_CAMP": {
        "genes": ["GPR65"],
        "intervention_direction": "agonism_or_positive_allosteric_modulation",
        "prior_status": "PARK_GENETIC_DRUGGABLE_LOCAL_WEAK",
        "route_note": "genetic/druggable acid-sensing GPCR route; local lipid-state coupling previously weak",
    },
    "GPR183_EBI2_OXYSTEROL_NICHE": {
        "genes": ["GPR183", "CH25H", "CYP7B1", "HSD3B7", "CYP27A1"],
        "intervention_direction": "oxysterol_niche_modulation",
        "prior_status": "PARK_NO_COHERENT_LOCAL_PROGRAM",
        "route_note": "Wave74 parked because ligand, receptor, and response programs did not cohere across diseases",
    },
    "MERTK_AXL_TAM_GAS6_PROS1_AGONISM": {
        "genes": ["MERTK", "AXL", "TYRO3", "GAS6", "PROS1"],
        "intervention_direction": "agonism_restoration",
        "prior_status": "PARTLY_BLOCKED_AND_DIFFICULT",
        "route_note": "repair/efferocytosis biology but agonism format, oncology/fibrosis/coagulation risks, and weak local direction",
    },
    "LXR_ABCA1_ABCG1_EFFLUX": {
        "genes": ["NR1H3", "NR1H2", "ABCA1", "ABCG1"],
        "intervention_direction": "efflux_activation_without_lipogenesis",
        "prior_status": "BLOCKED_BY_PRIOR_ART_AND_SAFETY",
        "route_note": "MS white-matter lipid-efflux biology is plausible, but broad LXR agonism is prior-arted and lipogenic",
    },
    "PPAR_RXR_LIPID_REPAIR": {
        "genes": ["PPARG", "PPARA", "PPARD", "RXRA", "RXRB", "RARA", "RARG"],
        "intervention_direction": "nuclear_receptor_modulation",
        "prior_status": "BLOCKED_BY_PRIOR_ART_AND_TOXICITY",
        "route_note": "crowded autoimmune/remyelination literature and systemic metabolic/retinoid toxicity",
    },
    "NPC1_NPC2_CHOLESTEROL_EGRESS": {
        "genes": ["NPC1", "NPC2"],
        "intervention_direction": "functional_rescue_or_cholesterol_egress_enhancement",
        "prior_status": "NOT_PRIOR_ART_BLOCKED_BUT_TRANSLATIONALLY_WEAK",
        "route_note": "readout-like lysosomal cholesterol route; delivery and selectivity are weak",
    },
    "LIPA_LAL_LYSOSOMAL_LIPID_CLEARANCE": {
        "genes": ["LIPA"],
        "intervention_direction": "enzyme_enhancement_or_replacement",
        "prior_status": "NOT_DIRECTLY_AUTOIMMUNE_BLOCKED_BUT_WEAK",
        "route_note": "enzyme replacement precedent but systemic lipid flux and weak MS support",
    },
    "FADS_DESATURATION_AXIS": {
        "genes": ["FADS1", "FADS2"],
        "intervention_direction": "lipid_desaturation_modulation",
        "prior_status": "PARK_GENETIC_LIPID_AXIS_UNRESOLVED_DIRECTION",
        "route_note": "autoimmune lipid genetics route; direction and immune-cell specificity unresolved",
    },
    "SCD_MONOUNSATURATED_LIPID_AXIS": {
        "genes": ["SCD"],
        "intervention_direction": "SCD_modulation",
        "prior_status": "PARK_DRUGGABLE_METABOLIC_AXIS_UNRESOLVED_AUTOIMMUNE_DIRECTION",
        "route_note": "druggable metabolic enzyme; chronic autoimmune direction and tolerability unresolved",
    },
    "SQLE_STEROL_SYNTHESIS_AXIS": {
        "genes": ["SQLE"],
        "intervention_direction": "squalene_epoxidase_modulation",
        "prior_status": "PARK_DRUGGABLE_STEROL_AXIS_UNRESOLVED_RELEVANCE",
        "route_note": "drugged by antifungal chemistry but no clear MS/cross-autoimmune controller evidence yet",
    },
    "AHR_BARRIER_IMMUNE_METABOLITE_AXIS": {
        "genes": ["AHR", "CYP1A1"],
        "intervention_direction": "contextual_AHR_modulation",
        "prior_status": "PARK_PRIOR_ART_BROAD_CONTEXT_DEPENDENT",
        "route_note": "gut/skin/immune-metabolite axis with broad context dependence",
    },
    "PTGER4_PROSTAGLANDIN_E2_AXIS": {
        "genes": ["PTGER4", "PTGS2"],
        "intervention_direction": "EP4_axis_modulation",
        "prior_status": "PARK_GENETIC_PRIOR_ART_AND_DIRECTION_CONTEXT_DEPENDENT",
        "route_note": "autoimmune genetic locus and druggable GPCR, but agonism/antagonism direction varies by compartment",
    },
    "NAMPT_HIF_METABOLIC_STRESS": {
        "genes": ["NAMPT", "HIF1A"],
        "intervention_direction": "metabolic_stress_modulation",
        "prior_status": "BLOCKED_BY_PRIOR_ART_AND_SYSTEMIC_METABOLIC_RISK",
        "route_note": "prior-arted inflammatory metabolic route; systemic toxicity risk",
    },
}


def read_tsv(path: Path, **kwargs: Any) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False, **kwargs)


def all_route_genes() -> set[str]:
    return {gene.upper() for route in ROUTES.values() for gene in route["genes"]}


def log_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0).replace(0, np.nan)
    return np.log2(counts.div(lib, axis=1) * 1_000_000.0 + 1.0)


def auc_score(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    pos = score[y == 1]
    neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    wins = 0.0
    for value in pos:
        wins += float((value > neg).sum())
        wins += 0.5 * float((value == neg).sum())
    return wins / float(len(pos) * len(neg))


def route_score_wide(expr_gene: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    z = zscore_rows(expr_gene)
    score_rows: dict[str, pd.Series] = {}
    coverage: list[dict[str, Any]] = []
    for route, meta in ROUTES.items():
        genes = [g.upper() for g in meta["genes"]]
        present = [g for g in genes if g in z.index]
        coverage.append(
            {
                "route": route,
                "n_defined": len(genes),
                "n_present": len(present),
                "genes_present": ";".join(present),
                "genes_missing": ";".join([g for g in genes if g not in z.index]),
            }
        )
        if present:
            score_rows[route] = z.loc[present].mean(axis=0, skipna=True)
    return pd.DataFrame(score_rows), pd.DataFrame(coverage)


def test_response(df: pd.DataFrame, score_col: str, covariates: list[str] | None = None) -> dict[str, Any]:
    covariates = covariates or []
    base = df.copy()
    base = base[np.isfinite(pd.to_numeric(base[score_col], errors="coerce")) & base["response"].isin([0, 1])].copy()
    if len(base) < 6 or base["response"].nunique() < 2:
        return {}
    score = pd.to_numeric(base[score_col], errors="coerce").to_numpy(float)
    adjusted = residualize(score, base, covariates) if covariates else score
    y = base["response"].astype(int).to_numpy()
    responders = adjusted[y == 1]
    nonresponders = adjusted[y == 0]
    if len(responders) >= 3 and len(nonresponders) >= 3:
        t_stat, p_value = stats.ttest_ind(responders, nonresponders, equal_var=False, nan_policy="omit")
    else:
        t_stat, p_value = np.nan, 1.0
    effect = float(np.nanmean(responders) - np.nanmean(nonresponders))
    auc_response = auc_score(y, adjusted)
    return {
        "n_subjects": int(len(base)),
        "n_responders": int(y.sum()),
        "n_nonresponders": int((1 - y).sum()),
        "effect_responder_minus_non": effect,
        "hedges_g_responder_minus_non": hedges_g(responders, nonresponders),
        "auc_high_score_response": auc_response,
        "auc_high_score_nonresponse": float(1.0 - auc_response) if np.isfinite(auc_response) else np.nan,
        "t": float(t_stat) if np.isfinite(t_stat) else np.nan,
        "p": float(p_value) if np.isfinite(p_value) else 1.0,
        "nonresponse_high_direction": bool(effect < 0),
        "nominal_or_trend_nonresponse_high": bool(effect < 0 and (float(p_value) if np.isfinite(p_value) else 1.0) < 0.20),
    }


def external_ibd_route_tests() -> tuple[pd.DataFrame, pd.DataFrame]:
    wanted = all_route_genes()
    probe_to_genes, probe_map = read_gpl570_gene_map(GPL570_ANNOT, wanted)
    coverage_rows: list[pd.DataFrame] = []
    tests: list[dict[str, Any]] = []
    for series, path in SERIES_FILES.items():
        metadata, expr_probe = read_ibd_series_matrix(path)
        info = ibd_sample_metadata(series, metadata)
        gene_expr = ibd_expression_to_gene_level(expr_probe, probe_to_genes)
        scores, coverage = route_score_wide(gene_expr)
        coverage["dataset"] = series
        coverage_rows.append(coverage)
        for spec in cohort_specs(series, info):
            mask = mask_for_spec(info, spec)
            selected = info.loc[mask].copy()
            selected_samples = [sample for sample in selected["sample"] if sample in scores.index]
            if len(selected_samples) < 6:
                continue
            patient_scores = patient_level_scores(scores.loc[selected_samples], info.loc[mask], spec)
            for route in scores.columns:
                row = test_response(patient_scores, route, list(spec.adjustment_covariates))
                if not row:
                    continue
                row.update(
                    {
                        "system": "IBD_external_GEO_antiTNF",
                        "dataset": series,
                        "cohort": spec.cohort,
                        "overlap_group": spec.overlap_group,
                        "disease_scope": spec.disease_scope,
                        "tissue_scope": spec.tissue_scope,
                        "route": route,
                        "adjustment_covariates": ";".join(spec.adjustment_covariates),
                    }
                )
                tests.append(row)
    out = pd.DataFrame(tests)
    if not out.empty:
        out["fdr_within_ibd_route_tests"] = bh(out["p"].to_numpy(float))
    cov = pd.concat(coverage_rows, ignore_index=True) if coverage_rows else pd.DataFrame()
    return out, cov


def ra_route_tests() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not RA_COUNTS.exists() or not RA_META.exists():
        return pd.DataFrame(), pd.DataFrame()
    counts = read_tsv(RA_COUNTS).set_index("GeneSymbol")
    counts.index = counts.index.astype(str).str.upper()
    wanted = sorted(all_route_genes().intersection(set(counts.index)))
    gene_expr = log_cpm(counts.loc[wanted]) if wanted else pd.DataFrame()
    scores, coverage = route_score_wide(gene_expr)
    meta = read_tsv(RA_META)
    pre = meta[meta["timepoint"].astype(str).str.lower().eq("pre")].copy()
    pre = pre[pre["count_column"].isin(scores.index)].copy()
    pre["response"] = pre["responder_moderate_or_good"].astype(str).str.lower().isin(["true", "1", "yes"]).astype(int)
    pre = pre.merge(scores.reset_index().rename(columns={"index": "count_column"}), on="count_column", how="inner")
    tests: list[dict[str, Any]] = []
    for route in scores.columns:
        row = test_response(pre, route, ["pathotype", "biologic", "inflammatory_score", "das28_score"])
        if not row:
            continue
        row.update(
            {
                "system": "RA_synovium_GSE198520_antiTNF",
                "dataset": "GSE198520",
                "cohort": "GSE198520_RA_synovium_pre",
                "overlap_group": "GSE198520_RA_synovium",
                "disease_scope": "RA",
                "tissue_scope": "synovium",
                "route": route,
                "adjustment_covariates": "pathotype;biologic;inflammatory_score;das28_score",
            }
        )
        tests.append(row)
    out = pd.DataFrame(tests)
    if not out.empty:
        out["fdr_within_ra_route_tests"] = bh(out["p"].to_numpy(float))
    coverage["dataset"] = "GSE198520"
    return out, coverage


def psoriasis_route_tests() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not PSO_SERIES.exists() or not GPL10558_ANNOT.exists():
        return pd.DataFrame(), pd.DataFrame()
    wanted = all_route_genes()
    metadata, expr_probe = read_pso_series_matrix(PSO_SERIES)
    info = pso_sample_metadata(metadata)
    response = build_patient_response_table(info)
    probe_to_genes, probe_map = read_gpl10558_gene_map(GPL10558_ANNOT, wanted)
    gene_expr = pso_expression_to_gene_level(expr_probe, probe_to_genes)
    scores, coverage = route_score_wide(gene_expr)
    baseline = response[(response["has_baseline_ls"]) & (response["pasi75_wk16"].isin([0, 1]))].copy()
    baseline = baseline[baseline["baseline_ls_sample"].isin(scores.index)].copy()
    score_df = scores.loc[baseline["baseline_ls_sample"].tolist()].copy()
    score_df["baseline_ls_sample"] = score_df.index
    base = baseline.merge(score_df, on="baseline_ls_sample", how="inner")
    base["response"] = base["pasi75_wk16"].astype(int)
    tests: list[dict[str, Any]] = []
    for treatment, sub in base.groupby("treatment", sort=False):
        for route in scores.columns:
            row = test_response(sub, route, [])
            if not row:
                continue
            row.update(
                {
                    "system": "psoriasis_GSE85034_baseline_response",
                    "dataset": "GSE85034",
                    "cohort": f"GSE85034_{treatment}_baseline_LS",
                    "overlap_group": f"GSE85034_{treatment}",
                    "disease_scope": "psoriasis",
                    "tissue_scope": "skin_lesional_baseline",
                    "route": route,
                    "treatment": treatment,
                    "adjustment_covariates": "",
                }
            )
            tests.append(row)
    out = pd.DataFrame(tests)
    if not out.empty:
        out["fdr_within_psoriasis_route_tests"] = bh(out["p"].to_numpy(float))
    coverage["dataset"] = "GSE85034"
    return out, coverage


def ms_route_support() -> pd.DataFrame:
    ms = read_tsv(MS_WM)
    if ms.empty:
        return pd.DataFrame()
    ms["gene"] = ms["gene"].astype(str).str.upper()
    rows: list[dict[str, Any]] = []
    for route, meta in ROUTES.items():
        genes = [g.upper() for g in meta["genes"]]
        sub = ms[ms["gene"].isin(genes)].copy()
        if sub.empty:
            rows.append({"route": route, "ms_genes_present": 0, "ms_route_call": "NO_GENES_PRESENT"})
            continue
        delta = pd.to_numeric(sub["delta_log2"], errors="coerce")
        p = pd.to_numeric(sub["p"], errors="coerce").fillna(1.0).clip(lower=1e-300, upper=1.0)
        signed_z = stats.norm.isf(p / 2.0) * np.sign(delta.fillna(0.0))
        combined_z = float(np.nansum(signed_z) / math.sqrt(np.isfinite(signed_z).sum())) if np.isfinite(signed_z).sum() else np.nan
        combined_p = float(2.0 * stats.norm.sf(abs(combined_z))) if np.isfinite(combined_z) else 1.0
        mean_delta = float(np.nanmean(delta))
        rows.append(
            {
                "route": route,
                "ms_genes_present": int(len(sub)),
                "ms_genes": ";".join(sub["gene"].tolist()),
                "ms_mean_delta_log2": mean_delta,
                "ms_combined_signed_z": combined_z,
                "ms_combined_p": combined_p,
                "ms_positive_nominal": bool(mean_delta > 0 and combined_p < 0.05),
                "ms_negative_nominal": bool(mean_delta < 0 and combined_p < 0.05),
                "ms_route_call": "MS_ROUTE_UP_NOMINAL"
                if mean_delta > 0 and combined_p < 0.05
                else ("MS_ROUTE_DOWN_NOMINAL" if mean_delta < 0 and combined_p < 0.05 else "MS_ROUTE_NULL_OR_WEAK"),
                "ms_top_gene": str(sub.reindex(sub["delta_log2"].abs().sort_values(ascending=False).index).iloc[0]["gene"]),
            }
        )
    return pd.DataFrame(rows)


def broad_h5ad_route_support() -> pd.DataFrame:
    if not BROAD_H5AD.exists():
        return pd.DataFrame()
    usecols = ["analysis", "disease_name", "compartment", "role", "gene", "delta_log2_cpm", "p", "fdr"]
    broad = read_tsv(BROAD_H5AD, usecols=usecols)
    if broad.empty:
        return pd.DataFrame()
    broad["gene"] = broad["gene"].astype(str).str.upper()
    broad = broad[broad["gene"].isin(all_route_genes())].copy()
    rows: list[dict[str, Any]] = []
    for route, meta in ROUTES.items():
        genes = [g.upper() for g in meta["genes"]]
        sub_route = broad[broad["gene"].isin(genes)].copy()
        if sub_route.empty:
            rows.append({"route": route, "h5ad_contexts_present": 0})
            continue
        for context, sub in sub_route.groupby(["analysis", "disease_name", "compartment", "role"], sort=False):
            p = pd.to_numeric(sub["p"], errors="coerce").fillna(1.0).clip(lower=1e-300, upper=1.0)
            delta = pd.to_numeric(sub["delta_log2_cpm"], errors="coerce")
            signed_z = stats.norm.isf(p / 2.0) * np.sign(delta.fillna(0.0))
            combined_z = float(np.nansum(signed_z) / math.sqrt(np.isfinite(signed_z).sum())) if np.isfinite(signed_z).sum() else np.nan
            combined_p = float(2.0 * stats.norm.sf(abs(combined_z))) if np.isfinite(combined_z) else 1.0
            mean_delta = float(np.nanmean(delta))
            analysis, disease, compartment, role = context
            rows.append(
                {
                    "route": route,
                    "analysis": analysis,
                    "disease_name": disease,
                    "compartment": compartment,
                    "role": role,
                    "n_genes_present": int(len(sub)),
                    "genes_present": ";".join(sub["gene"].tolist()),
                    "mean_delta_log2_cpm": mean_delta,
                    "combined_signed_z": combined_z,
                    "combined_p": combined_p,
                    "positive_nominal": bool(mean_delta > 0 and combined_p < 0.05),
                    "negative_nominal": bool(mean_delta < 0 and combined_p < 0.05),
                }
            )
    context_df = pd.DataFrame(rows)
    if context_df.empty:
        return pd.DataFrame()
    summary_rows: list[dict[str, Any]] = []
    for route, sub in context_df.groupby("route", sort=False):
        pos = sub[sub["positive_nominal"]]
        neg = sub[sub["negative_nominal"]]
        top_pos = pos.sort_values("combined_p").head(3)
        top_neg = neg.sort_values("combined_p").head(3)
        summary_rows.append(
            {
                "route": route,
                "h5ad_contexts_present": int(len(sub)),
                "h5ad_positive_context_count": int(len(pos)),
                "h5ad_positive_disease_count": int(pos["disease_name"].nunique()),
                "h5ad_positive_diseases": ";".join(sorted(pos["disease_name"].unique())),
                "h5ad_negative_context_count": int(len(neg)),
                "h5ad_negative_disease_count": int(neg["disease_name"].nunique()),
                "h5ad_negative_diseases": ";".join(sorted(neg["disease_name"].unique())),
                "h5ad_best_positive_contexts": ";".join(
                    (top_pos["analysis"].astype(str) + ":" + top_pos["mean_delta_log2_cpm"].round(3).astype(str) + ",p=" + top_pos["combined_p"].map(lambda x: f"{x:.3g}")).tolist()
                ),
                "h5ad_best_negative_contexts": ";".join(
                    (top_neg["analysis"].astype(str) + ":" + top_neg["mean_delta_log2_cpm"].round(3).astype(str) + ",p=" + top_neg["combined_p"].map(lambda x: f"{x:.3g}")).tolist()
                ),
            }
        )
    context_df.to_csv(OUT / "broad_h5ad_route_context_tests.tsv", sep="\t", index=False)
    return pd.DataFrame(summary_rows)


def route_prior_support() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    w30 = read_tsv(W30)
    w32 = read_tsv(W32)
    w48 = read_tsv(W48)
    w74 = read_tsv(W74)
    w30_by_axis = w30.set_index("axis") if not w30.empty and "axis" in w30.columns else pd.DataFrame()
    w32_by_route = w32.set_index("route") if not w32.empty and "route" in w32.columns else pd.DataFrame()
    w48_by_route = w48.set_index("route") if not w48.empty and "route" in w48.columns else pd.DataFrame()
    for route, meta in ROUTES.items():
        row = {
            "route": route,
            "route_genes": ";".join(meta["genes"]),
            "intervention_direction": meta["intervention_direction"],
            "prior_status": meta["prior_status"],
            "route_note": meta["route_note"],
        }
        if route in w30_by_axis.index:
            src = w30_by_axis.loc[route]
            row.update(
                {
                    "wave30_call": src.get("wave30_call", ""),
                    "wave30_intervention_score": src.get("intervention_score", np.nan),
                    "wave30_gate_failures": src.get("gate_failures", ""),
                    "wave30_europepmc_hit_count": src.get("europepmc_hit_count", np.nan),
                    "wave30_clinicaltrials_hit_count": src.get("clinicaltrials_hit_count", np.nan),
                    "wave30_max_chembl_activity_records": src.get("max_chembl_activity_records", np.nan),
                }
            )
        route32 = route
        if route == "FPR2_ANXA1_BIASED_RESOLUTION":
            route32 = "specialized_pro_resolving_mediator_FPR2_axis"
        elif route == "CD300_RECEPTOR_SPECIFIC_TUNING":
            route32 = "CD300_family_modulation"
        elif route == "NPC1_NPC2_CHOLESTEROL_EGRESS":
            route32 = "NPC1_NPC2_cholesterol_egress"
        elif route == "LIPA_LAL_LYSOSOMAL_LIPID_CLEARANCE":
            route32 = "LIPA_LAL_enhancement"
        elif route == "MERTK_AXL_TAM_GAS6_PROS1_AGONISM":
            route32 = "MERTK_AXL_TAM_GAS6_PROS1_agonism"
        elif route == "LXR_ABCA1_ABCG1_EFFLUX":
            route32 = "LXR_ABCA1_ABCG1_activation"
        elif route == "PPAR_RXR_LIPID_REPAIR":
            route32 = "PPAR_RXR_retinoid_modulation"
        if not w32_by_route.empty and route32 in w32_by_route.index:
            src = w32_by_route.loc[route32]
            row.update(
                {
                    "wave32_blocking_status": src.get("blocking_status", ""),
                    "wave32_verdict": src.get("verdict", ""),
                    "wave32_lead_indication": src.get("lead_indication_if_any", ""),
                }
            )
        if not w48_by_route.empty:
            route48 = "FPR2_ANXA1_BIASED_RESOLUTION" if route == "FPR2_ANXA1_BIASED_RESOLUTION" else ("CD300_RECEPTOR_SPECIFIC_TUNING" if route == "CD300_RECEPTOR_SPECIFIC_TUNING" else route)
            if route48 in w48_by_route.index:
                src = w48_by_route.loc[route48]
                row.update({"wave48_verdict": src.get("verdict", ""), "wave48_blocker": src.get("blocker", "")})
        if route == "GPR183_EBI2_OXYSTEROL_NICHE" and not w74.empty:
            row.update({"wave74_call": str(w74.iloc[0].get("wave74b_call", "")), "wave74_blockers": str(w74.iloc[0].get("decision_blockers", ""))})
        rows.append(row)
    return pd.DataFrame(rows)


def summarize_response(ibd: pd.DataFrame, ra: pd.DataFrame, pso: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if not ibd.empty:
        best_ibd = ibd.sort_values("p").drop_duplicates(["route", "overlap_group"])
        for route, sub in best_ibd.groupby("route", sort=False):
            rows.append(
                {
                    "route": route,
                    "ibd_nonresponse_high_groups": int(sub["nonresponse_high_direction"].sum()),
                    "ibd_nominal_or_trend_groups": int(sub["nominal_or_trend_nonresponse_high"].sum()),
                    "ibd_weighted_mean_g": float(np.average(sub["hedges_g_responder_minus_non"], weights=sub["n_subjects"])) if sub["hedges_g_responder_minus_non"].notna().any() else np.nan,
                    "ibd_min_p": float(sub["p"].min()),
                    "ibd_best_cohort": str(sub.sort_values("p").iloc[0]["cohort"]),
                }
            )
    out = pd.DataFrame({"route": list(ROUTES)})
    if rows:
        out = out.merge(pd.DataFrame(rows), on="route", how="left")
    if not ra.empty:
        ra_small = ra[["route", "effect_responder_minus_non", "hedges_g_responder_minus_non", "p", "nonresponse_high_direction", "nominal_or_trend_nonresponse_high"]].copy()
        ra_small = ra_small.rename(
            columns={
                "effect_responder_minus_non": "ra_effect_responder_minus_non",
                "hedges_g_responder_minus_non": "ra_hedges_g_responder_minus_non",
                "p": "ra_p",
                "nonresponse_high_direction": "ra_nonresponse_high",
                "nominal_or_trend_nonresponse_high": "ra_nominal_or_trend_nonresponse_high",
            }
        )
        out = out.merge(ra_small, on="route", how="left")
    if not pso.empty:
        ada = pso[pso.get("treatment", "").eq("ADA")].copy()
        pso_small = ada[["route", "effect_responder_minus_non", "hedges_g_responder_minus_non", "p", "nonresponse_high_direction", "nominal_or_trend_nonresponse_high"]].copy()
        pso_small = pso_small.rename(
            columns={
                "effect_responder_minus_non": "psoriasis_ada_effect_responder_minus_non",
                "hedges_g_responder_minus_non": "psoriasis_ada_hedges_g_responder_minus_non",
                "p": "psoriasis_ada_p",
                "nonresponse_high_direction": "psoriasis_ada_nonresponse_high",
                "nominal_or_trend_nonresponse_high": "psoriasis_ada_nominal_or_trend_nonresponse_high",
            }
        )
        out = out.merge(pso_small, on="route", how="left")
    bool_cols = [
        "ra_nonresponse_high",
        "ra_nominal_or_trend_nonresponse_high",
        "psoriasis_ada_nonresponse_high",
        "psoriasis_ada_nominal_or_trend_nonresponse_high",
    ]
    for col in bool_cols:
        if col in out.columns:
            out[col] = out[col].fillna(False).astype(bool)
    numeric_cols = ["ibd_nonresponse_high_groups", "ibd_nominal_or_trend_groups"]
    for col in numeric_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0)
    out["response_nonresponse_high_system_count"] = (
        (out.get("ibd_nonresponse_high_groups", 0) > 0).astype(int)
        + out.get("ra_nonresponse_high", False).astype(int)
        + out.get("psoriasis_ada_nonresponse_high", False).astype(int)
    )
    out["response_nominal_or_trend_system_count"] = (
        (out.get("ibd_nominal_or_trend_groups", 0) > 0).astype(int)
        + out.get("ra_nominal_or_trend_nonresponse_high", False).astype(int)
        + out.get("psoriasis_ada_nominal_or_trend_nonresponse_high", False).astype(int)
    )
    effect_cols = [c for c in ["ibd_weighted_mean_g", "ra_hedges_g_responder_minus_non", "psoriasis_ada_hedges_g_responder_minus_non"] if c in out.columns]
    out["response_mean_hedges_g"] = out[effect_cols].apply(lambda x: float(np.nanmean(pd.to_numeric(x, errors="coerce"))) if pd.to_numeric(x, errors="coerce").notna().any() else np.nan, axis=1)
    out["response_effect_sd"] = out[effect_cols].apply(lambda x: float(np.nanstd(pd.to_numeric(x, errors="coerce"), ddof=1)) if pd.to_numeric(x, errors="coerce").notna().sum() > 1 else np.nan, axis=1)
    return out


def classify(row: pd.Series) -> str:
    prior = str(row.get("prior_status", ""))
    response_systems = int(row.get("response_nonresponse_high_system_count", 0) or 0)
    response_trends = int(row.get("response_nominal_or_trend_system_count", 0) or 0)
    ms_support = bool(row.get("ms_positive_nominal", False))
    h5ad_pos = int(row.get("h5ad_positive_disease_count", 0) or 0)
    h5ad_neg = int(row.get("h5ad_negative_disease_count", 0) or 0)

    if prior.startswith("BLOCKED"):
        return "NO_GO_PRIOR_ART_OR_SAFETY_BLOCKED"
    if response_systems < 2:
        return "NO_GO_ROUTE_NOT_SHARED_IN_RESPONSE_CONTEXTS"
    if response_trends < 1:
        return "PARK_DIRECTION_ONLY_UNDERPOWERED_RESPONSE_ROUTE"
    if not ms_support:
        return "NO_GO_NO_MS_WHITE_MATTER_ROUTE_ANCHOR"
    if h5ad_neg > h5ad_pos and h5ad_pos < 3:
        return "NO_GO_BROAD_ATLAS_DIRECTION_CONFLICT"
    if "WEAK" in prior or "IMMATURE" in prior or "DIRECTION" in prior or prior.startswith("PARK") or "PARTLY" in prior:
        return "PARK_ROUTE_BIOLOGY_NOT_TRANSLATION_READY"
    return "REOPEN_CONTROLLER_ROUTE"


def analyze() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    ibd_tests, ibd_cov = external_ibd_route_tests()
    ra_tests, ra_cov = ra_route_tests()
    pso_tests, pso_cov = psoriasis_route_tests()
    ms = ms_route_support()
    h5ad = broad_h5ad_route_support()
    prior = route_prior_support()
    response = summarize_response(ibd_tests, ra_tests, pso_tests)

    rows = pd.DataFrame({"route": list(ROUTES)})
    for table in [response, ms, h5ad, prior]:
        if not table.empty:
            rows = rows.merge(table, on="route", how="left")
    bool_cols = ["ms_positive_nominal", "ms_negative_nominal"]
    for col in bool_cols:
        if col in rows.columns:
            rows[col] = rows[col].fillna(False).astype(bool)
    count_cols = [
        "h5ad_positive_disease_count",
        "h5ad_negative_disease_count",
        "response_nonresponse_high_system_count",
        "response_nominal_or_trend_system_count",
    ]
    for col in count_cols:
        if col in rows.columns:
            rows[col] = pd.to_numeric(rows[col], errors="coerce").fillna(0)
    rows["wave92_call"] = rows.apply(classify, axis=1)
    rows["controller_route_score"] = (
        rows.get("response_nonresponse_high_system_count", 0).astype(float) * 2.0
        + rows.get("response_nominal_or_trend_system_count", 0).astype(float) * 1.5
        + np.where(rows.get("ms_positive_nominal", False), 2.0, 0.0)
        + rows.get("h5ad_positive_disease_count", 0).astype(float) * 0.5
        - rows.get("h5ad_negative_disease_count", 0).astype(float) * 0.75
        + np.where(rows.get("prior_status", "").astype(str).str.startswith("NOT_BLOCKED"), 1.0, 0.0)
        - np.where(rows.get("prior_status", "").astype(str).str.startswith("BLOCKED"), 4.0, 0.0)
        - np.where(rows.get("prior_status", "").astype(str).str.startswith("PARTLY"), 1.0, 0.0)
    )
    rank = rows.sort_values("controller_route_score", ascending=False).copy()

    ibd_tests.to_csv(OUT / "external_ibd_controller_route_response_tests.tsv", sep="\t", index=False)
    ra_tests.to_csv(OUT / "ra_controller_route_response_tests.tsv", sep="\t", index=False)
    pso_tests.to_csv(OUT / "psoriasis_controller_route_response_tests.tsv", sep="\t", index=False)
    pd.concat([ibd_cov, ra_cov, pso_cov], ignore_index=True).to_csv(OUT / "route_gene_coverage.tsv", sep="\t", index=False)
    response.to_csv(OUT / "controller_route_response_summary.tsv", sep="\t", index=False)
    ms.to_csv(OUT / "ms_white_matter_controller_route_support.tsv", sep="\t", index=False)
    h5ad.to_csv(OUT / "broad_h5ad_controller_route_summary.tsv", sep="\t", index=False)
    prior.to_csv(OUT / "controller_route_prior_status.tsv", sep="\t", index=False)
    rank.to_csv(OUT / "controller_route_rank.tsv", sep="\t", index=False)

    reopened = rank[rank["wave92_call"].eq("REOPEN_CONTROLLER_ROUTE")]
    summary = {
        "seed": SEED,
        "analysis_call": "NO_REOPEN_CONTROLLER_ROUTE" if reopened.empty else "REOPEN_CONTROLLER_ROUTE",
        "n_routes": int(len(rank)),
        "n_reopened": int(len(reopened)),
        "top_route": str(rank.iloc[0]["route"]) if not rank.empty else "",
        "top_route_call": str(rank.iloc[0]["wave92_call"]) if not rank.empty else "",
        "call_counts": {str(k): int(v) for k, v in rank["wave92_call"].value_counts().to_dict().items()},
        "inputs": {
            "external_ibd_geo_series": [rel(path) for path in SERIES_FILES.values()],
            "gpl570_annotation": rel(GPL570_ANNOT),
            "ra_counts": rel(RA_COUNTS),
            "ra_metadata": rel(RA_META),
            "psoriasis_series": rel(PSO_SERIES),
            "gpl10558_annotation": rel(GPL10558_ANNOT),
            "ms_white_matter": rel(MS_WM),
            "broad_h5ad_gene_contrasts": rel(BROAD_H5AD),
            "wave30_niche_driver_audit": rel(W30),
            "wave32_route_feasibility": rel(W32),
            "wave48_resolution_reopener": rel(W48),
            "wave74_gpr183": rel(W74),
        },
    }
    write_json(OUT / "summary.json", summary)

    selected = [
        "route",
        "controller_route_score",
        "wave92_call",
        "prior_status",
        "intervention_direction",
        "response_nonresponse_high_system_count",
        "response_nominal_or_trend_system_count",
        "response_mean_hedges_g",
        "response_effect_sd",
        "ibd_weighted_mean_g",
        "ibd_min_p",
        "ra_hedges_g_responder_minus_non",
        "ra_p",
        "psoriasis_ada_hedges_g_responder_minus_non",
        "psoriasis_ada_p",
        "ms_mean_delta_log2",
        "ms_combined_p",
        "ms_route_call",
        "h5ad_positive_disease_count",
        "h5ad_positive_diseases",
        "h5ad_negative_disease_count",
        "h5ad_negative_diseases",
        "wave30_call",
        "wave32_blocking_status",
        "wave32_verdict",
        "route_note",
    ]
    available = [c for c in selected if c in rank.columns]
    report = [
        "# Wave92 Lipid-State Controller Route Audit",
        "",
        f"Analysis call: `{summary['analysis_call']}`.",
        "",
        "## Route Rank",
        "",
        markdown_table(rank[available], max_rows=30),
        "",
        "## Strict Call Counts",
        "",
        markdown_table(pd.DataFrame(sorted(summary["call_counts"].items()), columns=["wave92_call", "n_routes"]), max_rows=20),
        "",
        "## Interpretation",
        "",
        "- This route-level audit tests controller classes rather than module-marker genes.",
        "- A route cannot advance unless response association, MS anchoring, broad h5ad recurrence, and prior/druggability status agree.",
        "- High scores that are prior-art or safety blocked remain useful comparator biology, not target nominations.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    np.random.seed(SEED)
    summary = analyze()
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
