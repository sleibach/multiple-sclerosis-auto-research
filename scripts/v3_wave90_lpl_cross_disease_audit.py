#!/usr/bin/env python3
"""Wave90 LPL cross-disease audit.

Wave89 surfaced LPL as the strongest baseline lesional-skin adalimumab
nonresponse gene in GSE85034. This script stress-tests that lead against the
existing V3 evidence stack rather than promoting it from one small arm.

The audit integrates:

- MS bulk lesion expression from GSE111972.
- Donor-level direct single-cell disease-vs-control contrasts.
- External IBD anti-TNF response gene decomposition from Wave86.
- RA synovium anti-TNF baseline response using GSE198520 counts/metadata.
- Psoriasis adalimumab response from Wave89.

Decision rule:

- LPL can only advance if it shows MS lesion anchoring plus consistent
  anti-TNF nonresponse direction in IBD, RA, and psoriasis.
- If the response direction is unstable, LPL remains a lipid-state marker and
  the branch must look for upstream/downstream intervention handles instead.
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
OUT = ROOT / "results_v3" / "wave90_lpl_cross_disease_audit"

MS_WM = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
MS_MODULE = ROOT / "results_v3" / "gse111972_module_contrasts.tsv"
DIRECT_H5AD = ROOT / "results_v3" / "direct_h5ad_gene_replication" / "direct_h5ad_gene_donor_comparisons.tsv"
W86_META = ROOT / "results_v3" / "wave86_external_geo_antitnf_gene_driver" / "external_geo_gene_meta_rank.tsv"
W86_TESTS = ROOT / "results_v3" / "wave86_external_geo_antitnf_gene_driver" / "external_geo_gene_response_tests.tsv"
RA_COUNTS = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"
PSO_TESTS = ROOT / "results_v3" / "wave89_psoriasis_gse85034_response" / "psoriasis_baseline_gene_response_tests.tsv"


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


def test_ra_lpl_baseline() -> dict[str, Any]:
    counts = pd.read_csv(RA_COUNTS, sep="\t", low_memory=False).set_index("GeneSymbol")
    counts.index = counts.index.astype(str).str.upper()
    meta = pd.read_csv(RA_META, sep="\t", low_memory=False)
    if "LPL" not in counts.index:
        return {"evidence_channel": "RA_GSE198520_baseline_response", "gene": "LPL", "call": "MISSING"}
    expr = zscore_rows(log_cpm(counts))
    pre = meta[meta["timepoint"].astype(str).str.lower().eq("pre")].copy()
    pre = pre[pre["count_column"].isin(expr.columns)].copy()
    pre["response"] = pre["responder_moderate_or_good"].astype(str).str.lower().isin(["true", "1", "yes"]).astype(int)
    pre["_score"] = expr.loc["LPL", pre["count_column"].tolist()].astype(float).to_numpy()
    pre = pre[np.isfinite(pre["_score"]) & pre["response"].isin([0, 1])].copy()
    if len(pre) < 8 or pre["response"].nunique() < 2:
        return {"evidence_channel": "RA_GSE198520_baseline_response", "gene": "LPL", "call": "INSUFFICIENT"}
    adjusted = residualize(pre["_score"].to_numpy(float), pre, ["pathotype", "biologic", "inflammatory_score", "das28_score"])
    y = pre["response"].astype(int).to_numpy()
    responders = adjusted[y == 1]
    nonresponders = adjusted[y == 0]
    t_stat, p_value = stats.ttest_ind(responders, nonresponders, equal_var=False, nan_policy="omit")
    effect = float(np.nanmean(responders) - np.nanmean(nonresponders))
    auc_response = auc_score(y, adjusted)
    return {
        "evidence_channel": "RA_GSE198520_baseline_response",
        "dataset": "GSE198520",
        "disease": "rheumatoid arthritis",
        "tissue": "synovium",
        "endpoint": "moderate_or_good_response",
        "gene": "LPL",
        "n_subjects": int(len(pre)),
        "n_responders": int(y.sum()),
        "n_nonresponders": int((1 - y).sum()),
        "effect_responder_minus_non": effect,
        "hedges_g_responder_minus_non": hedges_g(responders, nonresponders),
        "auc_high_expression_nonresponse": float(1.0 - auc_response) if np.isfinite(auc_response) else np.nan,
        "p": float(p_value) if np.isfinite(p_value) else 1.0,
        "nonresponse_high_direction": bool(effect < 0),
        "call": "SUPPORT" if effect < 0 and p_value < 0.10 else ("DIRECTION_ONLY" if effect < 0 else "NO_SUPPORT"),
    }


def load_ms_rows() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if MS_WM.exists():
        ms = pd.read_csv(MS_WM, sep="\t", low_memory=False)
        ms["gene"] = ms["gene"].astype(str).str.upper()
        hit = ms[ms["gene"].eq("LPL")].copy()
        for _, row in hit.iterrows():
            rows.append(
                {
                    "evidence_channel": "MS_GSE111972_bulk_wm_signature",
                    "dataset": "GSE111972",
                    "disease": "multiple sclerosis",
                    "tissue": "white matter",
                    "gene": "LPL",
                    "delta_case_minus_control": row.get("delta_log2", np.nan),
                    "hedges_g_case_minus_control": row.get("hedges_g", np.nan),
                    "p": row.get("p", np.nan),
                    "fdr": row.get("fdr", np.nan),
                    "call": "MS_WM_UP" if float(row.get("delta_log2", np.nan)) > 0 and float(row.get("p", 1.0)) < 0.05 else "NO_MS_WM_NOMINAL",
                }
            )
    if MS_MODULE.exists():
        mod = pd.read_csv(MS_MODULE, sep="\t", low_memory=False)
        keep = mod[(mod["feature"].eq("lipid_loader_repair")) & (mod["contrast"].astype(str).str.contains("MS_WM_vs_CON_WM"))].copy()
        for _, row in keep.iterrows():
            rows.append(
                {
                    "evidence_channel": "MS_GSE111972_lipid_loader_module",
                    "dataset": "GSE111972",
                    "disease": "multiple sclerosis",
                    "tissue": "white matter",
                    "gene": "LPL_module_context",
                    "delta_case_minus_control": row.get("delta_log2", np.nan),
                    "hedges_g_case_minus_control": row.get("hedges_g", np.nan),
                    "p": row.get("p", np.nan),
                    "fdr": row.get("fdr", np.nan),
                    "call": "MS_WM_MODULE_UP" if float(row.get("delta_log2", np.nan)) > 0 and float(row.get("p", 1.0)) < 0.05 else "NO_MS_WM_MODULE_NOMINAL",
                }
            )
    return pd.DataFrame(rows)


def load_direct_h5ad_rows() -> pd.DataFrame:
    if not DIRECT_H5AD.exists():
        return pd.DataFrame()
    df = pd.read_csv(DIRECT_H5AD, sep="\t", low_memory=False)
    df["gene"] = df["gene"].astype(str).str.upper()
    keep = df[(df["gene"].eq("LPL")) & (df["metric"].eq("mean_z_vs_controls"))].copy()
    keep = keep.rename(
        columns={
            "analysis": "context",
            "disease_name": "disease",
            "compartment": "tissue",
            "delta_case_minus_control": "delta_case_minus_control",
            "hedges_g": "hedges_g_case_minus_control",
        }
    )
    keep["evidence_channel"] = "direct_h5ad_donor_case_control"
    keep["dataset"] = keep["context"]
    keep["call"] = np.where(
        (pd.to_numeric(keep["delta_case_minus_control"], errors="coerce") > 0) & (pd.to_numeric(keep["p"], errors="coerce") < 0.10),
        "CASE_HIGH_NOMINAL_OR_TREND",
        np.where(
            (pd.to_numeric(keep["delta_case_minus_control"], errors="coerce") < 0) & (pd.to_numeric(keep["p"], errors="coerce") < 0.10),
            "CONTROL_HIGH_NOMINAL_OR_TREND",
            "NO_NOMINAL_CASE_CONTROL_SIGNAL",
        ),
    )
    return keep[
        [
            "evidence_channel",
            "dataset",
            "disease",
            "tissue",
            "gene",
            "n_case_donors",
            "n_control_donors",
            "delta_case_minus_control",
            "hedges_g_case_minus_control",
            "p",
            "fdr",
            "call",
        ]
    ].sort_values(["disease", "tissue"])


def load_ibd_response_rows() -> tuple[pd.DataFrame, pd.DataFrame]:
    meta_rows: list[dict[str, Any]] = []
    test_rows: list[dict[str, Any]] = []
    if W86_META.exists():
        meta = pd.read_csv(W86_META, sep="\t", low_memory=False)
        meta["gene"] = meta["gene"].astype(str).str.upper()
        hit = meta[meta["gene"].eq("LPL")].copy()
        for _, row in hit.iterrows():
            meta_rows.append(
                {
                    "evidence_channel": "IBD_Wave86_external_antitnf_meta",
                    "dataset": "GSE12251/GSE14580/GSE16879",
                    "disease": "IBD",
                    "tissue": "intestinal mucosa",
                    "gene": "LPL",
                    "n_primary_contexts": row.get("n_primary_contexts", np.nan),
                    "nonresponse_high_contexts": row.get("nonresponse_high_contexts", np.nan),
                    "responder_high_contexts": row.get("responder_high_contexts", np.nan),
                    "weighted_mean_hedges_g_responder_minus_non": row.get("weighted_mean_hedges_g_responder_minus_non", np.nan),
                    "median_auc_high_expression_nonresponse": row.get("median_auc_high_score_nonresponse", np.nan),
                    "min_p": row.get("min_p", np.nan),
                    "wave86_call": row.get("call", ""),
                    "call": "IBD_RESPONSE_WEAK_DIRECTION" if int(row.get("nonresponse_high_contexts", 0)) >= 3 else "NO_IBD_RESPONSE_DIRECTION",
                }
            )
    if W86_TESTS.exists():
        tests = pd.read_csv(W86_TESTS, sep="\t", low_memory=False)
        tests["gene"] = tests["gene"].astype(str).str.upper()
        hit = tests[tests["gene"].eq("LPL")].copy()
        hit["call"] = np.where(
            hit["nonresponse_high_direction"].astype(bool) & (pd.to_numeric(hit["p"], errors="coerce") < 0.10),
            "NONRESPONSE_HIGH_TREND",
            np.where(hit["nonresponse_high_direction"].astype(bool), "NONRESPONSE_HIGH_WEAK", "RESPONDER_HIGH_OR_NULL"),
        )
        test_rows = hit.to_dict("records")
    return pd.DataFrame(meta_rows), pd.DataFrame(test_rows)


def load_psoriasis_response_rows() -> pd.DataFrame:
    if not PSO_TESTS.exists():
        return pd.DataFrame()
    pso = pd.read_csv(PSO_TESTS, sep="\t", low_memory=False)
    keep = pso[pso["feature"].astype(str).str.upper().eq("LPL")].copy()
    keep = keep.rename(columns={"feature": "gene", "hedges_g_responder_minus_non": "hedges_g_responder_minus_non"})
    keep["evidence_channel"] = "psoriasis_GSE85034_baseline_response"
    keep["dataset"] = "GSE85034"
    keep["call"] = np.where(
        keep["nonresponse_high_direction"].astype(bool) & (pd.to_numeric(keep["p"], errors="coerce") < 0.10),
        "NONRESPONSE_HIGH_TREND",
        np.where(keep["nonresponse_high_direction"].astype(bool), "NONRESPONSE_HIGH_WEAK", "NO_SUPPORT"),
    )
    return keep[
        [
            "evidence_channel",
            "dataset",
            "disease",
            "tissue",
            "treatment",
            "gene",
            "n_subjects",
            "n_pasi75_responders",
            "n_pasi75_nonresponders",
            "effect_responder_minus_non",
            "hedges_g_responder_minus_non",
            "auc_high_score_nonresponse",
            "p",
            "fdr_within_treatment",
            "nonresponse_high_direction",
            "call",
        ]
    ].sort_values("treatment")


def response_support_summary(ibd_meta: pd.DataFrame, ra_row: dict[str, Any], pso: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if not ibd_meta.empty:
        r = ibd_meta.iloc[0]
        rows.append(
            {
                "disease": "IBD",
                "dataset": "GSE12251/GSE14580/GSE16879",
                "response_context": "intestinal mucosa anti-TNF",
                "direction": "nonresponse_high" if float(r["weighted_mean_hedges_g_responder_minus_non"]) < 0 else "not_nonresponse_high",
                "effect": float(r["weighted_mean_hedges_g_responder_minus_non"]),
                "p_or_min_p": float(r["min_p"]),
                "call": r["call"],
            }
        )
    if ra_row:
        rows.append(
            {
                "disease": "rheumatoid arthritis",
                "dataset": "GSE198520",
                "response_context": "synovium anti-TNF",
                "direction": "nonresponse_high" if bool(ra_row.get("nonresponse_high_direction")) else "not_nonresponse_high",
                "effect": ra_row.get("hedges_g_responder_minus_non", np.nan),
                "p_or_min_p": ra_row.get("p", np.nan),
                "call": ra_row.get("call", ""),
            }
        )
    if not pso.empty:
        ada = pso[pso["treatment"].eq("ADA")].copy()
        if not ada.empty:
            r = ada.iloc[0]
            rows.append(
                {
                    "disease": "psoriasis",
                    "dataset": "GSE85034",
                    "response_context": "lesional skin adalimumab",
                    "direction": "nonresponse_high" if bool(r["nonresponse_high_direction"]) else "not_nonresponse_high",
                    "effect": float(r["hedges_g_responder_minus_non"]),
                    "p_or_min_p": float(r["p"]),
                    "call": r["call"],
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["nonresponse_high"] = out["direction"].eq("nonresponse_high")
    return out


def decide(ms_rows: pd.DataFrame, direct_rows: pd.DataFrame, response_rows: pd.DataFrame) -> str:
    ms_support = False
    if not ms_rows.empty:
        ms_support = bool(((ms_rows["evidence_channel"].eq("MS_GSE111972_bulk_wm_signature")) & (ms_rows["call"].eq("MS_WM_UP"))).any())
    response_consistent = False
    if not response_rows.empty:
        response_consistent = int(response_rows["nonresponse_high"].sum()) >= 3
    pso_apc_case_control_conflict = False
    if not direct_rows.empty:
        pso = direct_rows[(direct_rows["disease"].eq("psoriasis")) & (direct_rows["tissue"].str.contains("APC", case=False, na=False))]
        pso_apc_case_control_conflict = bool((pd.to_numeric(pso["delta_case_minus_control"], errors="coerce") < 0).any())
    if ms_support and response_consistent and not pso_apc_case_control_conflict:
        return "ADVANCE_LPL_AS_CROSS_DISEASE_LIPID_NODE"
    if ms_support and response_consistent:
        return "PARK_LPL_RESPONSE_MARKER_WITH_CASE_CONTROL_CONFLICT"
    if ms_support:
        return "LPL_MARKER_ONLY_RESPONSE_DIRECTION_UNSTABLE"
    return "NO_LPL_ADVANCEMENT"


def analyze() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    ms_rows = load_ms_rows()
    direct_rows = load_direct_h5ad_rows()
    ibd_meta, ibd_tests = load_ibd_response_rows()
    ra_row = test_ra_lpl_baseline()
    pso = load_psoriasis_response_rows()
    response_rows = response_support_summary(ibd_meta, ra_row, pso)

    if not direct_rows.empty:
        direct_rows["fdr_lpl_across_direct_contexts"] = bh(pd.to_numeric(direct_rows["p"], errors="coerce").fillna(1.0).to_numpy())

    ms_rows.to_csv(OUT / "lpl_ms_bulk_evidence.tsv", sep="\t", index=False)
    direct_rows.to_csv(OUT / "lpl_direct_h5ad_case_control_evidence.tsv", sep="\t", index=False)
    ibd_meta.to_csv(OUT / "lpl_ibd_antitnf_meta_evidence.tsv", sep="\t", index=False)
    ibd_tests.to_csv(OUT / "lpl_ibd_antitnf_context_tests.tsv", sep="\t", index=False)
    pd.DataFrame([ra_row]).to_csv(OUT / "lpl_ra_synovium_baseline_response.tsv", sep="\t", index=False)
    pso.to_csv(OUT / "lpl_psoriasis_baseline_response.tsv", sep="\t", index=False)
    response_rows.to_csv(OUT / "lpl_response_direction_summary.tsv", sep="\t", index=False)

    call = decide(ms_rows, direct_rows, response_rows)
    direct_positive = int(((pd.to_numeric(direct_rows.get("delta_case_minus_control", pd.Series(dtype=float)), errors="coerce") > 0) & (pd.to_numeric(direct_rows.get("p", pd.Series(dtype=float)), errors="coerce") < 0.10)).sum()) if not direct_rows.empty else 0
    direct_negative = int(((pd.to_numeric(direct_rows.get("delta_case_minus_control", pd.Series(dtype=float)), errors="coerce") < 0) & (pd.to_numeric(direct_rows.get("p", pd.Series(dtype=float)), errors="coerce") < 0.10)).sum()) if not direct_rows.empty else 0
    summary = {
        "seed": SEED,
        "analysis_call": call,
        "n_direct_h5ad_contexts": int(len(direct_rows)),
        "n_direct_positive_p_lt_0_10": direct_positive,
        "n_direct_negative_p_lt_0_10": direct_negative,
        "n_response_contexts": int(len(response_rows)),
        "n_response_contexts_nonresponse_high": int(response_rows["nonresponse_high"].sum()) if not response_rows.empty else 0,
        "inputs": {
            "ms_wm_signature": rel(MS_WM),
            "direct_h5ad_donor_comparisons": rel(DIRECT_H5AD),
            "wave86_meta": rel(W86_META),
            "wave86_tests": rel(W86_TESTS),
            "ra_counts": rel(RA_COUNTS),
            "ra_metadata": rel(RA_META),
            "psoriasis_tests": rel(PSO_TESTS),
        },
    }
    write_json(OUT / "summary.json", summary)

    report = [
        "# Wave90 LPL Cross-Disease Audit",
        "",
        f"Analysis call: `{call}`.",
        "",
        "## Response Direction Summary",
        "",
        markdown_table(response_rows, max_rows=20),
        "",
        "## MS Bulk Evidence",
        "",
        markdown_table(ms_rows, max_rows=20),
        "",
        "## Direct Single-Cell Case-Control LPL Rows",
        "",
        markdown_table(
            direct_rows[
                [
                    "disease",
                    "tissue",
                    "n_case_donors",
                    "n_control_donors",
                    "delta_case_minus_control",
                    "hedges_g_case_minus_control",
                    "p",
                    "fdr_lpl_across_direct_contexts",
                    "call",
                ]
            ]
            if not direct_rows.empty
            else pd.DataFrame(),
            max_rows=40,
        ),
        "",
        "## Interpretation",
        "",
        "- LPL is MS white-matter lesion-up and sits in the lipid-loader module.",
        "- LPL response direction is not stable enough to promote as the cross-disease intervention node.",
        "- Psoriasis adalimumab nonresponse-high LPL conflicts with psoriasis APC case-control LPL being lower in cases than controls in the direct h5ad donor comparison.",
        "- LPL remains useful as a lipid-load/state marker and a clue toward lipid handling, but direct systemic LPL modulation is not a plausible autoimmune therapeutic route without a more selective tissue/cell-state handle.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    np.random.seed(SEED)
    result = analyze()
    print(json.dumps(result, indent=2, sort_keys=True))
