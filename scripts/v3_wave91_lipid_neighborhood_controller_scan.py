#!/usr/bin/env python3
"""Wave91 lipid-neighborhood controller scan.

Wave90 parked LPL as a marker, not an intervention node. This scan asks which
nearby lipid-loader / phagolysosomal candidates have a better therapeutic
profile across the existing V3 evidence stack.

Inputs are all local artifacts produced earlier in the V3 run. The output is a
ranked audit, not a therapeutic claim. Manual feasibility annotations are used
only for coarse targetability/known-liability flags and are recorded in the
script for reproducibility.
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
from v3_wave85_external_geo_antitnf_validation import bh, hedges_g, markdown_table, rel, residualize, write_json, zscore_rows


SEED = 20260527
OUT = ROOT / "results_v3" / "wave91_lipid_neighborhood_controller_scan"

MS_WM = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
DIRECT_H5AD = ROOT / "results_v3" / "direct_h5ad_gene_replication" / "direct_h5ad_gene_donor_comparisons.tsv"
W86_META = ROOT / "results_v3" / "wave86_external_geo_antitnf_gene_driver" / "external_geo_gene_meta_rank.tsv"
RA_COUNTS = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"
PSO_TESTS = ROOT / "results_v3" / "wave89_psoriasis_gse85034_response" / "psoriasis_baseline_gene_response_tests.tsv"
GENETICS = ROOT / "results_v3" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W81 = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W82 = ROOT / "results_v3" / "wave82_parked_perturbation_intervention_audit" / "wave82_integrated_intervention_rank.tsv"
W83 = ROOT / "results_v3" / "wave83_intervention_class_first_scan" / "reachable_intervention_rank.tsv"
GENEFORMER_FILES = [
    ROOT / "results_v3" / "geneformer_pivot_panel_delete" / "geneformer_pivot_panel_context_metrics_ranked.tsv",
    ROOT / "results_v3" / "geneformer_unrestricted_survivor_delete" / "geneformer_unrestricted_survivor_context_metrics_ranked.tsv",
    ROOT / "results_v3" / "geneformer_broad_residual_delete" / "geneformer_broad_residual_context_metrics_ranked.tsv",
    ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_geneformer_metrics.tsv",
    ROOT / "results_v3" / "wave70c_inhibitory_receptor_geneformer_direction" / "geneformer_direction_metrics.tsv",
]

CANDIDATES = [
    "LPL",
    "NR1H3",
    "NR1H2",
    "ABCA1",
    "ABCG1",
    "APOE",
    "LIPA",
    "PLIN2",
    "GPNMB",
    "MERTK",
    "MSR1",
    "CD36",
    "TREM2",
    "ACSL1",
    "FABP5",
    "PPARD",
    "PPARG",
]

FEASIBILITY = {
    "LPL": {
        "route": "enzyme/extracellular lipid hydrolysis",
        "druggability": 1,
        "liability": "systemic triglyceride biology; direct autoimmune modulation unsafe/unselective",
        "manual_prior_pressure": 1,
    },
    "NR1H3": {
        "route": "LXR-alpha nuclear receptor agonism/modulation",
        "druggability": 4,
        "liability": "hepatic lipogenesis and broad nuclear-receptor prior art",
        "manual_prior_pressure": 2,
    },
    "NR1H2": {
        "route": "LXR-beta nuclear receptor agonism/modulation",
        "druggability": 4,
        "liability": "LXR-class lipogenesis/sterol biology; CNS-selective beta agonism would be needed",
        "manual_prior_pressure": 2,
    },
    "ABCA1": {
        "route": "cholesterol efflux transporter, indirect activation",
        "druggability": 1,
        "liability": "poor direct small-molecule target; usually reached through LXR/apoA1",
        "manual_prior_pressure": 1,
    },
    "ABCG1": {
        "route": "cholesterol efflux transporter, indirect activation",
        "druggability": 1,
        "liability": "poor direct small-molecule target; usually reached through LXR",
        "manual_prior_pressure": 1,
    },
    "APOE": {
        "route": "apolipoprotein/lipid transport state",
        "druggability": 1,
        "liability": "genotype- and CNS-biology complexity; marker more than target",
        "manual_prior_pressure": 2,
    },
    "LIPA": {
        "route": "lysosomal acid lipase replacement/activation",
        "druggability": 3,
        "liability": "enzyme replacement exists but CNS/tissue macrophage delivery is difficult",
        "manual_prior_pressure": 1,
    },
    "PLIN2": {
        "route": "lipid droplet coat protein",
        "druggability": 0,
        "liability": "intracellular structural marker, no clean modality",
        "manual_prior_pressure": 0,
    },
    "GPNMB": {
        "route": "surface/secreted glycoprotein; antibody/ADC precedent, agonism unresolved",
        "druggability": 3,
        "liability": "direction uncertain; oncology ADC precedent mostly depletes target cells",
        "manual_prior_pressure": 1,
    },
    "MERTK": {
        "route": "efferocytosis receptor tyrosine kinase agonism",
        "druggability": 3,
        "liability": "oncogenic/pro-fibrotic risk; agonist modality less mature than inhibitors",
        "manual_prior_pressure": 2,
    },
    "MSR1": {
        "route": "scavenger receptor modulation",
        "druggability": 2,
        "liability": "broad innate lipid uptake receptor, selectivity and direction unclear",
        "manual_prior_pressure": 1,
    },
    "CD36": {
        "route": "fatty-acid/scavenger receptor inhibition/modulation",
        "druggability": 2,
        "liability": "broad metabolic/platelet/vascular roles",
        "manual_prior_pressure": 2,
    },
    "TREM2": {
        "route": "microglial/myeloid receptor agonism",
        "druggability": 3,
        "liability": "neurodegeneration prior art; peripheral autoimmune direction uncertain",
        "manual_prior_pressure": 2,
    },
    "ACSL1": {
        "route": "long-chain acyl-CoA synthetase inhibition",
        "druggability": 2,
        "liability": "metabolic housekeeping; prior V3 module-adjusted demotion",
        "manual_prior_pressure": 1,
    },
    "FABP5": {
        "route": "fatty-acid binding protein inhibitor",
        "druggability": 3,
        "liability": "pleiotropic lipid signaling and barrier/keratinocyte biology",
        "manual_prior_pressure": 1,
    },
    "PPARD": {
        "route": "PPAR-delta agonism/modulation",
        "druggability": 4,
        "liability": "broad metabolic nuclear receptor; prior-art and oncogenicity concerns",
        "manual_prior_pressure": 2,
    },
    "PPARG": {
        "route": "PPAR-gamma agonism/modulation",
        "druggability": 4,
        "liability": "approved agonists but edema/weight/cardiometabolic liabilities and extensive autoimmune prior art",
        "manual_prior_pressure": 3,
    },
}


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


def log_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0).replace(0, np.nan)
    return np.log2(counts.div(lib, axis=1) * 1_000_000.0 + 1.0)


def load_ms() -> pd.DataFrame:
    ms = pd.read_csv(MS_WM, sep="\t", low_memory=False)
    ms["gene"] = ms["gene"].astype(str).str.upper()
    keep = ms[ms["gene"].isin(CANDIDATES)].copy()
    keep = keep.rename(columns={"delta_log2": "ms_wm_delta", "hedges_g": "ms_wm_hedges_g", "p": "ms_wm_p", "fdr": "ms_wm_fdr"})
    return keep[["gene", "ms_wm_delta", "ms_wm_hedges_g", "ms_wm_p", "ms_wm_fdr"]]


def load_direct_summary() -> pd.DataFrame:
    df = pd.read_csv(DIRECT_H5AD, sep="\t", low_memory=False)
    df["gene"] = df["gene"].astype(str).str.upper()
    keep = df[(df["gene"].isin(CANDIDATES)) & (df["metric"].eq("mean_z_vs_controls"))].copy()
    rows = []
    for gene, group in keep.groupby("gene"):
        g = group.copy()
        g["positive"] = (pd.to_numeric(g["delta_case_minus_control"], errors="coerce") > 0) & (pd.to_numeric(g["p"], errors="coerce") < 0.10)
        g["negative"] = (pd.to_numeric(g["delta_case_minus_control"], errors="coerce") < 0) & (pd.to_numeric(g["p"], errors="coerce") < 0.10)
        best = g.sort_values("p").iloc[0]
        rows.append(
            {
                "gene": gene,
                "direct_contexts": int(len(g)),
                "direct_positive_contexts_p_lt_0_10": int(g["positive"].sum()),
                "direct_negative_contexts_p_lt_0_10": int(g["negative"].sum()),
                "direct_positive_diseases": ";".join(sorted(set(g.loc[g["positive"], "disease_name"].astype(str)))),
                "direct_negative_diseases": ";".join(sorted(set(g.loc[g["negative"], "disease_name"].astype(str)))),
                "direct_best_context": str(best["analysis"]),
                "direct_best_delta": float(best["delta_case_minus_control"]),
                "direct_best_p": float(best["p"]),
            }
        )
    return pd.DataFrame(rows)


def load_ibd_response() -> pd.DataFrame:
    meta = pd.read_csv(W86_META, sep="\t", low_memory=False)
    meta["gene"] = meta["gene"].astype(str).str.upper()
    keep = meta[meta["gene"].isin(CANDIDATES)].copy()
    if keep.empty:
        return pd.DataFrame(columns=["gene"])
    return keep[
        [
            "gene",
            "n_primary_contexts",
            "nonresponse_high_contexts",
            "responder_high_contexts",
            "weighted_mean_hedges_g_responder_minus_non",
            "median_auc_high_score_nonresponse",
            "min_p",
            "call",
        ]
    ].rename(
        columns={
            "call": "ibd_wave86_call",
            "weighted_mean_hedges_g_responder_minus_non": "ibd_weighted_g_resp_minus_non",
            "median_auc_high_score_nonresponse": "ibd_median_auc_nonresponse",
            "min_p": "ibd_min_p",
        }
    )


def test_ra_baseline(expr: pd.DataFrame, meta: pd.DataFrame, gene: str) -> dict[str, Any]:
    if gene not in expr.index:
        return {"gene": gene, "ra_tested": False}
    pre = meta[meta["timepoint"].astype(str).str.lower().eq("pre")].copy()
    pre = pre[pre["count_column"].isin(expr.columns)].copy()
    pre["response"] = pre["responder_moderate_or_good"].astype(str).str.lower().isin(["true", "1", "yes"]).astype(int)
    pre["_score"] = expr.loc[gene, pre["count_column"].tolist()].astype(float).to_numpy()
    pre = pre[np.isfinite(pre["_score"]) & pre["response"].isin([0, 1])].copy()
    if len(pre) < 8 or pre["response"].nunique() < 2:
        return {"gene": gene, "ra_tested": False}
    adjusted = residualize(pre["_score"].to_numpy(float), pre, ["pathotype", "biologic", "inflammatory_score", "das28_score"])
    y = pre["response"].astype(int).to_numpy()
    responders = adjusted[y == 1]
    nonresponders = adjusted[y == 0]
    t_stat, p_value = stats.ttest_ind(responders, nonresponders, equal_var=False, nan_policy="omit")
    effect = float(np.nanmean(responders) - np.nanmean(nonresponders))
    auc_response = auc_score(y, adjusted)
    return {
        "gene": gene,
        "ra_tested": True,
        "ra_n": int(len(pre)),
        "ra_effect_resp_minus_non": effect,
        "ra_hedges_g_resp_minus_non": hedges_g(responders, nonresponders),
        "ra_auc_nonresponse": float(1.0 - auc_response) if np.isfinite(auc_response) else np.nan,
        "ra_p": float(p_value) if np.isfinite(p_value) else 1.0,
        "ra_nonresponse_high": bool(effect < 0),
    }


def load_ra_response() -> pd.DataFrame:
    counts = pd.read_csv(RA_COUNTS, sep="\t", low_memory=False).set_index("GeneSymbol")
    counts.index = counts.index.astype(str).str.upper()
    meta = pd.read_csv(RA_META, sep="\t", low_memory=False)
    expr = zscore_rows(log_cpm(counts))
    rows = [test_ra_baseline(expr, meta, gene) for gene in CANDIDATES]
    return pd.DataFrame(rows)


def load_psoriasis_response() -> pd.DataFrame:
    pso = pd.read_csv(PSO_TESTS, sep="\t", low_memory=False)
    pso["gene"] = pso["feature"].astype(str).str.upper()
    keep = pso[(pso["gene"].isin(CANDIDATES)) & (pso["treatment"].eq("ADA"))].copy()
    return keep[
        [
            "gene",
            "n_subjects",
            "effect_responder_minus_non",
            "hedges_g_responder_minus_non",
            "auc_high_score_nonresponse",
            "p",
            "fdr_within_treatment",
            "nonresponse_high_direction",
        ]
    ].rename(
        columns={
            "n_subjects": "pso_ada_n",
            "effect_responder_minus_non": "pso_ada_effect_resp_minus_non",
            "hedges_g_responder_minus_non": "pso_ada_hedges_g_resp_minus_non",
            "auc_high_score_nonresponse": "pso_ada_auc_nonresponse",
            "p": "pso_ada_p",
            "fdr_within_treatment": "pso_ada_fdr",
            "nonresponse_high_direction": "pso_ada_nonresponse_high",
        }
    )


def load_genetics_and_prior_outputs() -> pd.DataFrame:
    rows = []
    frames = []
    if GENETICS.exists():
        g = pd.read_csv(GENETICS, sep="\t", low_memory=False)
        g["gene"] = g["gene"].astype(str).str.upper()
        for _, row in g[g["gene"].isin(CANDIDATES)].iterrows():
            rows.append(
                {
                    "gene": row["gene"],
                    "genetics_score": row.get("score", np.nan),
                    "genetic_breadth_count": row.get("genetic_breadth_disease_count", np.nan),
                    "genetic_breadth_diseases": row.get("genetic_breadth_diseases", ""),
                    "wave55_score": row.get("score", np.nan),
                    "wave55_do_not_promote": row.get("do_not_promote", ""),
                }
            )
    base = pd.DataFrame(rows).drop_duplicates("gene") if rows else pd.DataFrame({"gene": CANDIDATES})
    for path, prefix in [(W81, "wave81"), (W82, "wave82"), (W83, "wave83")]:
        if not path.exists():
            continue
        df = pd.read_csv(path, sep="\t", low_memory=False)
        if "gene" not in df.columns:
            continue
        df["gene"] = df["gene"].astype(str).str.upper()
        keep_cols = ["gene"]
        for col in df.columns:
            if col in {"gene", f"{prefix}_call", "wave81_call", "wave82_call", "wave83_call", "total_score", "score", "hard_failures", "manual_blocker", "manual_closure_reason", "primary_route_note", "chembl_activity_count", "chembl_exact_human_target_count"}:
                keep_cols.append(col)
        sub = df[df["gene"].isin(CANDIDATES)][list(dict.fromkeys(keep_cols))].copy()
        rename = {col: f"{prefix}_{col}" for col in sub.columns if col != "gene" and not col.startswith(prefix)}
        frames.append(sub.rename(columns=rename))
    out = base
    for frame in frames:
        out = out.merge(frame, on="gene", how="outer")
    return out


def load_geneformer_summary() -> pd.DataFrame:
    rows = []
    for path in GENEFORMER_FILES:
        if not path.exists():
            continue
        try:
            df = pd.read_csv(path, sep="\t", low_memory=False)
        except Exception:
            continue
        if "gene" not in df.columns:
            continue
        df["gene"] = df["gene"].astype(str).str.upper()
        sub = df[df["gene"].isin(CANDIDATES)].copy()
        if sub.empty:
            continue
        status_cols = [col for col in sub.columns if "status" in col.lower() or "note" in col.lower()]
        for gene, group in sub.groupby("gene"):
            status_text = " ".join(group[status_cols].astype(str).agg(" ".join, axis=1).tolist()) if status_cols else ""
            unusable = group.astype(str).apply(lambda s: s.str.contains("token_not_detected", case=False, na=False)).any(axis=1)
            support_cols = [col for col in group.columns if "support" in col.lower() or "direction" in col.lower()]
            rows.append(
                {
                    "gene": gene,
                    "geneformer_source": rel(path),
                    "geneformer_rows": int(len(group)),
                    "geneformer_usable_rows": int((~unusable).sum()),
                    "geneformer_token_not_detected_rows": int(unusable.sum()),
                    "geneformer_support_fields": ";".join(support_cols[:8]),
                    "geneformer_status_excerpt": status_text[:200],
                }
            )
    if not rows:
        return pd.DataFrame({"gene": CANDIDATES})
    df = pd.DataFrame(rows)
    summary = df.groupby("gene").agg(
        geneformer_sources=("geneformer_source", lambda s: ";".join(sorted(set(s)))),
        geneformer_rows=("geneformer_rows", "sum"),
        geneformer_usable_rows=("geneformer_usable_rows", "sum"),
        geneformer_token_not_detected_rows=("geneformer_token_not_detected_rows", "sum"),
        geneformer_support_fields=("geneformer_support_fields", lambda s: ";".join(sorted(set([x for x in s if x])))),
    ).reset_index()
    return summary


def score_rows(df: pd.DataFrame) -> pd.DataFrame:
    for col in [
        "ms_wm_delta",
        "ms_wm_p",
        "direct_positive_contexts_p_lt_0_10",
        "direct_negative_contexts_p_lt_0_10",
        "nonresponse_high_contexts",
        "responder_high_contexts",
        "ibd_min_p",
        "ra_hedges_g_resp_minus_non",
        "ra_p",
        "pso_ada_hedges_g_resp_minus_non",
        "pso_ada_p",
        "geneformer_usable_rows",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    def finite_or_zero(value: Any) -> float:
        try:
            val = float(value)
        except (TypeError, ValueError):
            return 0.0
        return val if np.isfinite(val) else 0.0

    scores = []
    calls = []
    hard_failures = []
    for _, row in df.iterrows():
        gene = str(row["gene"])
        feas = FEASIBILITY.get(gene, {})
        score = 0.0
        failures = []
        ms_delta = row.get("ms_wm_delta", np.nan)
        ms_p = row.get("ms_wm_p", np.nan)
        if np.isfinite(ms_delta) and ms_delta > 0 and np.isfinite(ms_p) and ms_p < 0.05:
            score += 3.0
        else:
            failures.append("no_nominal_ms_wm_up_anchor")
        pos = finite_or_zero(row.get("direct_positive_contexts_p_lt_0_10", 0))
        neg = finite_or_zero(row.get("direct_negative_contexts_p_lt_0_10", 0))
        score += min(pos, 4) * 1.0
        score -= min(neg, 4) * 1.0
        if neg > 0:
            failures.append("case_control_negative_context_present")
        response_points = 0.0
        ibd_ctx = row.get("nonresponse_high_contexts", np.nan)
        if np.isfinite(ibd_ctx) and ibd_ctx >= 3:
            response_points += 0.75
        ra_g = row.get("ra_hedges_g_resp_minus_non", np.nan)
        ra_p = row.get("ra_p", np.nan)
        if np.isfinite(ra_g) and ra_g < 0:
            response_points += 0.75 if np.isfinite(ra_p) and ra_p < 0.10 else 0.35
        pso_g = row.get("pso_ada_hedges_g_resp_minus_non", np.nan)
        pso_p = row.get("pso_ada_p", np.nan)
        if np.isfinite(pso_g) and pso_g < 0:
            response_points += 0.75 if np.isfinite(pso_p) and pso_p < 0.10 else 0.35
        score += response_points
        if response_points < 1.0:
            failures.append("weak_or_inconsistent_response_direction")
        geneformer = row.get("geneformer_usable_rows", np.nan)
        if np.isfinite(geneformer) and geneformer > 0:
            score += min(float(geneformer), 3.0) * 0.25
        else:
            failures.append("no_usable_foundation_model_rows")
        druggability = float(feas.get("druggability", 0))
        score += druggability * 0.8
        if druggability < 2:
            failures.append("weak_direct_druggability")
        prior = float(feas.get("manual_prior_pressure", 0))
        score -= prior * 0.8
        if prior >= 2:
            failures.append("manual_prior_or_class_pressure")
        liability = str(feas.get("liability", ""))
        if "systemic" in liability or "broad" in liability or "oncogenic" in liability:
            score -= 0.5
            failures.append("major_safety_or_selectivity_liability")
        scores.append(score)
        hard_failures.append(";".join(failures))
        if score >= 7 and not failures:
            calls.append("ADVANCE_CONTROLLER_CANDIDATE")
        elif score >= 6 and "no_nominal_ms_wm_up_anchor" not in failures and "weak_direct_druggability" not in failures:
            calls.append("PARK_CONTROLLER_FOR_DEEP_VALIDATION")
        elif score >= 4:
            calls.append("PARK_MARKER_OR_WEAK_CONTROLLER")
        else:
            calls.append("NO_GO_LIPID_NEIGHBORHOOD_NODE")
    df["wave91_score"] = scores
    df["wave91_failures"] = hard_failures
    df["wave91_call"] = calls
    df["intervention_route"] = df["gene"].map(lambda g: FEASIBILITY.get(g, {}).get("route", ""))
    df["manual_liability"] = df["gene"].map(lambda g: FEASIBILITY.get(g, {}).get("liability", ""))
    df["manual_druggability_0_4"] = df["gene"].map(lambda g: FEASIBILITY.get(g, {}).get("druggability", 0))
    df["manual_prior_pressure_0_3"] = df["gene"].map(lambda g: FEASIBILITY.get(g, {}).get("manual_prior_pressure", 0))
    call_order = {
        "ADVANCE_CONTROLLER_CANDIDATE": 0,
        "PARK_CONTROLLER_FOR_DEEP_VALIDATION": 1,
        "PARK_MARKER_OR_WEAK_CONTROLLER": 2,
        "NO_GO_LIPID_NEIGHBORHOOD_NODE": 3,
    }
    df["_call_order"] = df["wave91_call"].map(call_order).fillna(99).astype(int)
    return df.sort_values(["_call_order", "wave91_score"], ascending=[True, False]).drop(columns=["_call_order"])


def analyze() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    base = pd.DataFrame({"gene": CANDIDATES})
    for frame in [
        load_ms(),
        load_direct_summary(),
        load_ibd_response(),
        load_ra_response(),
        load_psoriasis_response(),
        load_genetics_and_prior_outputs(),
        load_geneformer_summary(),
    ]:
        if frame.empty:
            continue
        base = base.merge(frame, on="gene", how="left")
    ranked = score_rows(base)
    ranked.to_csv(OUT / "lipid_neighborhood_controller_rank.tsv", sep="\t", index=False)
    summary = {
        "seed": SEED,
        "n_candidates": int(len(ranked)),
        "call_counts": {str(k): int(v) for k, v in ranked["wave91_call"].value_counts().to_dict().items()},
        "top_gene": str(ranked.iloc[0]["gene"]) if not ranked.empty else "",
        "top_call": str(ranked.iloc[0]["wave91_call"]) if not ranked.empty else "",
        "top_score": float(ranked.iloc[0]["wave91_score"]) if not ranked.empty else np.nan,
        "inputs": {
            "ms_wm_signature": rel(MS_WM),
            "direct_h5ad": rel(DIRECT_H5AD),
            "wave86_meta": rel(W86_META),
            "ra_counts": rel(RA_COUNTS),
            "ra_metadata": rel(RA_META),
            "psoriasis_tests": rel(PSO_TESTS),
            "genetics": rel(GENETICS),
        },
    }
    write_json(OUT / "summary.json", summary)
    report_cols = [
        "gene",
        "wave91_call",
        "wave91_score",
        "ms_wm_delta",
        "ms_wm_p",
        "direct_positive_contexts_p_lt_0_10",
        "direct_negative_contexts_p_lt_0_10",
        "nonresponse_high_contexts",
        "ra_hedges_g_resp_minus_non",
        "ra_p",
        "pso_ada_hedges_g_resp_minus_non",
        "pso_ada_p",
        "geneformer_usable_rows",
        "manual_druggability_0_4",
        "manual_prior_pressure_0_3",
        "intervention_route",
        "wave91_failures",
    ]
    report = [
        "# Wave91 Lipid-Neighborhood Controller Scan",
        "",
        "Question: after parking LPL, which lipid-loader neighborhood node has a better mix of MS anchoring, cross-disease support, response evidence, foundation-model availability, and druggability?",
        "",
        "## Ranked Candidates",
        "",
        markdown_table(ranked[[col for col in report_cols if col in ranked.columns]], max_rows=30),
        "",
        "## Interpretation",
        "",
        "No candidate is promoted as a V3 therapeutic finding by this scan alone. The top rows are parked for deeper validation only if their failures are addressable.",
        "",
        "The most important guardrail is that nuclear-receptor and scavenger-receptor routes are druggable but broad; marker strength does not equal safe intervention.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    np.random.seed(SEED)
    result = analyze()
    print(json.dumps(result, indent=2, sort_keys=True))
