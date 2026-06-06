#!/usr/bin/env python3
"""Wave115 SPNS1 controller falsification audit.

This is intentionally not a target-promotion script. It asks whether SPNS1
behaves like an upstream lysosomal-lipid controller rather than a recurrent
activation marker.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave115_spns1_controller_falsification_audit"

DONOR = ROOT / "phases/v3/results" / "wave79_targetability_shortlist_residual_audit" / "direct_shortlist_donor_scores.tsv"
MATRIX = ROOT / "phases/v3/results" / "wave79_targetability_shortlist_residual_audit" / "targetability_shortlist_candidate_matrix.tsv"
MS = ROOT / "phases/v3/results" / "wave79_targetability_shortlist_residual_audit" / "ms_white_matter_shortlist_rows.tsv"
RA_RESPONSE = ROOT / "phases/v3/results" / "wave79_targetability_shortlist_residual_audit" / "ra_antitnf_shortlist_response_rows.tsv"
IBD_RESPONSE = ROOT / "phases/v3/results" / "wave79_targetability_shortlist_residual_audit" / "ibd_antitnf_shortlist_response_rows.tsv"
W37 = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W62 = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W94 = ROOT / "phases/v3/results" / "wave94_accessible_state_rerank" / "accessible_state_candidate_rank.tsv"

DOWNSTREAM_MODULES = [
    "module_lipid_loader_repair",
    "module_hla_ii_apc",
    "module_lysosomal_apc",
    "module_ifn_apc",
]
CORE_COVARS = [
    "generic_inflammation_mean",
    "injury_stress_mean",
    "module_t_cell_admixture",
]
STRICT_COVARS = [
    "module_ifn_apc",
    "module_hla_ii_apc",
    "module_lysosomal_apc",
    "module_inflammatory_nfkb",
    "generic_inflammation_mean",
    "injury_stress_mean",
    "module_t_cell_admixture",
]


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def bh_fdr(pvalues: pd.Series) -> pd.Series:
    vals = pd.to_numeric(pvalues, errors="coerce")
    out = pd.Series(np.nan, index=vals.index, dtype=float)
    valid = vals.dropna().sort_values()
    if valid.empty:
        return out
    n = len(valid)
    adj = valid * n / np.arange(1, n + 1)
    adj = np.minimum.accumulate(adj.iloc[::-1]).iloc[::-1].clip(upper=1.0)
    out.loc[adj.index] = adj
    return out


def residualize(y: pd.Series, covars: pd.DataFrame) -> np.ndarray:
    yv = pd.to_numeric(y, errors="coerce").to_numpy(dtype=float)
    x = covars.apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    ok = np.isfinite(yv) & np.isfinite(x).all(axis=1)
    resid = np.full(len(yv), np.nan)
    if ok.sum() <= x.shape[1] + 2:
        return resid
    x_ok = x[ok]
    design = np.column_stack([np.ones(ok.sum()), x_ok])
    beta = np.linalg.lstsq(design, yv[ok], rcond=None)[0]
    resid[ok] = yv[ok] - design @ beta
    return resid


def partial_spearman(frame: pd.DataFrame, target: str, outcome: str, covars: list[str]) -> dict[str, object]:
    cols = [target, outcome] + covars
    work = frame[cols].copy()
    for col in cols:
        work[col] = pd.to_numeric(work[col], errors="coerce")
    work = work.dropna()
    if len(work) <= len(covars) + 3:
        return {
            "n": len(work),
            "rho": np.nan,
            "p": np.nan,
            "status": f"underpowered_n_le_covars_plus_3:{len(work)}<={len(covars)+3}",
        }
    ranked = work.rank(method="average")
    target_resid = residualize(ranked[target], ranked[covars])
    outcome_resid = residualize(ranked[outcome], ranked[covars])
    ok = np.isfinite(target_resid) & np.isfinite(outcome_resid)
    if ok.sum() < 5 or np.nanstd(target_resid[ok]) == 0 or np.nanstd(outcome_resid[ok]) == 0:
        return {"n": int(ok.sum()), "rho": np.nan, "p": np.nan, "status": "degenerate_residuals"}
    rho, p = stats.pearsonr(target_resid[ok], outcome_resid[ok])
    return {"n": int(ok.sum()), "rho": float(rho), "p": float(p), "status": "ok"}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    donor = read_tsv(DONOR)
    matrix = read_tsv(MATRIX)
    ms = read_tsv(MS)
    ra = read_tsv(RA_RESPONSE)
    ibd = read_tsv(IBD_RESPONSE)
    w37 = read_tsv(W37)
    w62 = read_tsv(W62)
    w94 = read_tsv(W94)

    rows = []
    if not donor.empty:
        cases = donor[donor["group"].eq("case")].copy()
        for (analysis, disease_name, compartment, role), sub in cases.groupby(
            ["analysis", "disease_name", "compartment", "role"], dropna=False
        ):
            for module in DOWNSTREAM_MODULES:
                for covar_label, covars in {
                    "core": CORE_COVARS,
                    "strict": STRICT_COVARS,
                }.items():
                    available = [c for c in covars if c in sub.columns and c != module]
                    res = partial_spearman(sub, "target_SPNS1", module, available)
                    rows.append(
                        {
                            "analysis": analysis,
                            "disease_name": disease_name,
                            "compartment": compartment,
                            "role": role,
                            "module": module,
                            "covar_set": covar_label,
                            "covariates": ";".join(available),
                            **res,
                        }
                    )
    controller = pd.DataFrame(rows)
    if not controller.empty:
        controller["fdr"] = bh_fdr(controller["p"])
        controller["positive_controller_like"] = (
            controller["status"].eq("ok")
            & (controller["rho"] >= 0.60)
            & (controller["p"] < 0.10)
            & (controller["fdr"] < 0.20)
            & controller["module"].isin(["module_lipid_loader_repair", "module_hla_ii_apc", "module_lysosomal_apc"])
        )
        controller["myeloid_positive"] = controller["positive_controller_like"] & controller["role"].eq("myeloid_apc")
    else:
        controller["fdr"] = []
        controller["positive_controller_like"] = []
        controller["myeloid_positive"] = []
    controller.to_csv(OUT / "spns1_case_only_partial_controller_tests.tsv", sep="\t", index=False)

    disease_summary = (
        controller.groupby("disease_name", dropna=False)
        .agg(
            tested_contexts=("analysis", "nunique"),
            positive_contexts=("positive_controller_like", "sum"),
            myeloid_positive_contexts=("myeloid_positive", "sum"),
            best_rho=("rho", "max"),
            best_p=("p", "min"),
            best_fdr=("fdr", "min"),
        )
        .reset_index()
        if not controller.empty
        else pd.DataFrame()
    )
    disease_summary["disease_pass"] = (
        (disease_summary["positive_contexts"] > 0) & (disease_summary["myeloid_positive_contexts"] > 0)
        if not disease_summary.empty
        else []
    )
    disease_summary.to_csv(OUT / "spns1_controller_disease_summary.tsv", sep="\t", index=False)

    spns1_matrix = matrix[matrix["gene"].eq("SPNS1")].copy() if not matrix.empty and "gene" in matrix.columns else pd.DataFrame()
    spns1_ms = ms[ms["gene"].eq("SPNS1")].copy() if not ms.empty and "gene" in ms.columns else pd.DataFrame()
    spns1_ra = ra[ra["gene"].eq("SPNS1")].copy() if not ra.empty and "gene" in ra.columns else pd.DataFrame()
    spns1_ibd = ibd[ibd["gene"].eq("SPNS1")].copy() if not ibd.empty and "gene" in ibd.columns else pd.DataFrame()
    spns1_w37 = w37[w37["gene_symbol"].eq("SPNS1")].copy() if not w37.empty and "gene_symbol" in w37.columns else pd.DataFrame()
    spns1_w62 = w62[w62["gene"].eq("SPNS1")].copy() if not w62.empty and "gene" in w62.columns else pd.DataFrame()
    spns1_w94 = w94[w94["gene"].eq("SPNS1")].copy() if not w94.empty and "gene" in w94.columns else pd.DataFrame()

    controller_pass_diseases = (
        int(disease_summary["disease_pass"].sum()) if not disease_summary.empty and "disease_pass" in disease_summary else 0
    )
    myeloid_pass_contexts = int(controller["myeloid_positive"].sum()) if not controller.empty else 0
    ms_anchor = (not spns1_ms.empty) and bool(spns1_ms.iloc[0].get("ms_anchor", False))
    response_support = (
        (not spns1_ra.empty and bool(spns1_ra.get("supportive_suppression_response", pd.Series([False])).any()))
        or (not spns1_ibd.empty and bool(spns1_ibd.get("supportive_suppression_response", pd.Series([False])).any()))
    )
    crispr_support = (not spns1_w37.empty) and str(spns1_w37.iloc[0].get("screen_call", "")).startswith("KO_")
    target_resolution_call = str(spns1_w62.iloc[0].get("wave62_call", "")) if not spns1_w62.empty else ""
    target_resolution = (not spns1_w62.empty) and target_resolution_call != "" and not target_resolution_call.startswith("NO_GO")
    modality_ready = bool(spns1_matrix.iloc[0].get("modality_ready_local", False)) if not spns1_matrix.empty else False
    branch_call = (
        "REOPEN_SPNS1_PRECLINICAL_CONTROLLER_ONLY"
        if controller_pass_diseases >= 2 and myeloid_pass_contexts >= 2 and ms_anchor and response_support and crispr_support
        else "NO_REOPEN_SPNS1_CONTROLLER_ROUTE"
    )

    evidence = pd.DataFrame(
        [
            {"evidence": "wave79_candidate_matrix", "value": spns1_matrix.to_dict(orient="records")},
            {"evidence": "ms_white_matter", "value": spns1_ms.to_dict(orient="records")},
            {"evidence": "ra_response", "value": spns1_ra.to_dict(orient="records")},
            {"evidence": "ibd_response", "value": spns1_ibd.to_dict(orient="records")},
            {"evidence": "crispr_efferocytosis", "value": spns1_w37.to_dict(orient="records")},
            {"evidence": "target_resolution", "value": spns1_w62.to_dict(orient="records")},
            {"evidence": "wave94_accessible_rank", "value": spns1_w94.to_dict(orient="records")},
        ]
    )
    evidence.to_csv(OUT / "spns1_external_gate_evidence.tsv", sep="\t", index=False)

    payload = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "controller_pass_diseases": controller_pass_diseases,
        "myeloid_pass_contexts": myeloid_pass_contexts,
        "ms_anchor": bool(ms_anchor),
        "response_support": bool(response_support),
        "crispr_support": bool(crispr_support),
        "target_resolution": bool(target_resolution),
        "modality_ready": bool(modality_ready),
        "inputs": {
            "donor_scores": rel(DONOR),
            "candidate_matrix": rel(MATRIX),
            "ms": rel(MS),
            "ra_response": rel(RA_RESPONSE),
            "ibd_response": rel(IBD_RESPONSE),
            "crispr": rel(W37),
            "target_resolution": rel(W62),
            "wave94": rel(W94),
        },
    }
    write_json(OUT / "summary.json", payload)

    top_controller = (
        controller.sort_values(["positive_controller_like", "fdr", "p"], ascending=[False, True, True]).head(20)
        if not controller.empty
        else pd.DataFrame()
    )
    report = f"""# Wave115 SPNS1 Controller Falsification Audit

## Bottom Line

Branch call: `{branch_call}`.

This is a controller falsification test, not a target nomination. It asks
whether case-only donor variation in `SPNS1` predicts downstream lipid/APC
state after residualizing generic inflammation, injury/stress, and T-cell
admixture.

## Controller Summary

{markdown_table(disease_summary, max_rows=20)}

## Top Partial-Correlation Rows

{markdown_table(top_controller, max_rows=20)}

## External Gate Evidence

{markdown_table(evidence, max_rows=20)}

## Decision Rule

Reopen only as a preclinical biology route if at least two diseases have
myeloid controller-like contexts, MS expression support is present, and at
least one response plus one direct perturbation gate is supportive. Therapeutic
promotion would still require chemical/modality evidence, which is absent here.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave115_spns1_controller_falsification_audit.py")}`
- Main output: `{rel(OUT / "spns1_case_only_partial_controller_tests.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
