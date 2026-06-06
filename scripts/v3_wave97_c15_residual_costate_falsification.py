#!/usr/bin/env python3
"""Wave97 residual donor-level falsification for C15ORF48 parked candidates.

Wave96 found parked proximal candidates around the C15ORF48 state, but the
largest weakness is confounding by generic inflammatory/metabolic burden. This
wave reuses raw h5ad atlases and asks whether candidate-C15 donor co-state
survives residualization against disease status and broad covariate modules.

This is intentionally a falsification wave: surviving residual co-state is
necessary but still not sufficient for therapeutic promotion.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse, stats

from v3_analyze_osmr_complement_axes import CONFIGS, COVARIATE_MODULES, ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave97_c15_residual_costate_falsification"

W96 = ROOT / "phases/v3/results" / "wave96_c15orf48_controller_search" / "c15orf48_controller_candidate_rank.tsv"
ANCHORS = ROOT / "phases/v3/results" / "wave96_c15orf48_controller_search" / "c15orf48_anchor_contexts.tsv"


def clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value)


def gene_symbol_map(a: ad.AnnData, symbol_column: str, genes: set[str]) -> dict[str, int]:
    if symbol_column in a.var.columns:
        symbols = a.var[symbol_column].astype(str).str.upper()
    elif "feature_name" in a.var.columns:
        symbols = a.var["feature_name"].astype(str).str.upper()
    else:
        symbols = pd.Series(a.var_names.astype(str)).str.upper()
    wanted = {gene.upper() for gene in genes}
    mapping: dict[str, int] = {}
    for idx, symbol in enumerate(symbols):
        if symbol in wanted and symbol not in mapping:
            mapping[symbol] = idx
    return mapping


def residualize(y: np.ndarray, design: np.ndarray) -> np.ndarray:
    y = np.asarray(y, dtype=float)
    design = np.asarray(design, dtype=float)
    ok = np.isfinite(y) & np.isfinite(design).all(axis=1)
    out = np.full_like(y, np.nan, dtype=float)
    if ok.sum() < max(4, design.shape[1] + 2):
        return out
    x = np.column_stack([np.ones(ok.sum()), design[ok]])
    beta, *_ = np.linalg.lstsq(x, y[ok], rcond=None)
    out[ok] = y[ok] - x @ beta
    return out


def corr_pair(x: np.ndarray, y: np.ndarray) -> tuple[float, float, int]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    ok = np.isfinite(x) & np.isfinite(y)
    n = int(ok.sum())
    if n < 3 or np.nanstd(x[ok]) < 1e-9 or np.nanstd(y[ok]) < 1e-9:
        return math.nan, math.nan, n
    r, p = stats.pearsonr(x[ok], y[ok])
    return float(r), float(p), n


def donor_table(config: Any, genes: set[str]) -> pd.DataFrame:
    a = ad.read_h5ad(config.path)
    obs = a.obs.copy()
    mask = obs["disease"].isin([config.disease_label, config.control_label]) & obs["cell_type"].isin(config.cell_types)
    if mask.sum() == 0:
        return pd.DataFrame()
    x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
    mapping = gene_symbol_map(a, config.gene_symbol_column, genes)
    if "C15ORF48" not in mapping:
        return pd.DataFrame()
    present = sorted(mapping)
    cell_idx = np.flatnonzero(mask.to_numpy())
    gene_idx = [mapping[gene] for gene in present]
    sub_x = x[cell_idx][:, gene_idx].astype(float)
    lib_size = np.asarray(x[cell_idx].sum(axis=1)).ravel().astype(float)
    lib_size[~np.isfinite(lib_size) | (lib_size <= 0)] = np.nan
    scale = np.divide(1e4, lib_size, out=np.zeros_like(lib_size), where=np.isfinite(lib_size))
    log_expr = np.log1p(sub_x.multiply(scale[:, None]).toarray())
    expr = pd.DataFrame(log_expr, columns=present)
    meta = obs.loc[mask, ["donor_id", "disease"]].reset_index(drop=True)
    expr["donor_id"] = meta["donor_id"].astype(str).values
    expr["disease"] = meta["disease"].astype(str).values
    donor = expr.groupby(["donor_id", "disease"], as_index=False)[present].mean()

    control = donor["disease"].eq(config.control_label).to_numpy()
    for gene in present:
        mean = donor.loc[control, gene].mean()
        sd = donor.loc[control, gene].std(ddof=1)
        if not np.isfinite(sd) or sd < 1e-6:
            sd = 1.0
        donor[f"{gene}__z"] = (donor[gene] - mean) / sd
    for module, module_genes in COVARIATE_MODULES.items():
        z_cols = [f"{gene}__z" for gene in module_genes if f"{gene}__z" in donor.columns]
        donor[module] = donor[z_cols].mean(axis=1) if z_cols else np.nan
    module_cols = [m for m in COVARIATE_MODULES if m in donor.columns]
    donor["generic_covariate_mean"] = donor[module_cols].mean(axis=1)
    donor["disease_binary"] = donor["disease"].eq(config.disease_label).astype(float)
    return donor


def per_context_residual_tests(
    anchors: pd.DataFrame, candidates: list[str], genes: set[str]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    config_by_name = {config.name: config for config in CONFIGS}
    rows = []
    donor_rows = []
    for _, anchor in anchors[anchors["c15_anchor_trend"]].iterrows():
        analysis = clean(anchor["analysis"])
        config = config_by_name.get(analysis)
        if config is None:
            continue
        donor = donor_table(config, genes)
        if donor.empty or "C15ORF48__z" not in donor.columns:
            continue
        donor_export = donor[["donor_id", "disease", "disease_binary", "C15ORF48__z", "generic_covariate_mean"]].copy()
        donor_export["analysis"] = analysis
        donor_rows.append(donor_export)

        all_design = donor[["disease_binary", "generic_covariate_mean"]].to_numpy(float)
        case_mask = donor["disease"].eq(config.disease_label).to_numpy()
        case_design = donor.loc[case_mask, ["generic_covariate_mean"]].to_numpy(float)
        c15_all_resid = residualize(donor["C15ORF48__z"].to_numpy(float), all_design)
        c15_case_resid = residualize(donor.loc[case_mask, "C15ORF48__z"].to_numpy(float), case_design)
        for gene in candidates:
            z_col = f"{gene}__z"
            if z_col not in donor.columns:
                continue
            raw_all_r, raw_all_p, raw_all_n = corr_pair(donor["C15ORF48__z"], donor[z_col])
            cand_all_resid = residualize(donor[z_col].to_numpy(float), all_design)
            all_r, all_p, all_n = corr_pair(c15_all_resid, cand_all_resid)
            raw_case_r, raw_case_p, raw_case_n = corr_pair(donor.loc[case_mask, "C15ORF48__z"], donor.loc[case_mask, z_col])
            cand_case_resid = residualize(donor.loc[case_mask, z_col].to_numpy(float), case_design)
            case_r, case_p, case_n = corr_pair(c15_case_resid, cand_case_resid)
            rows.append(
                {
                    "analysis": analysis,
                    "disease_name": anchor["disease_name"],
                    "compartment": anchor["compartment"],
                    "role": anchor["role"],
                    "gene": gene,
                    "raw_all_r": raw_all_r,
                    "raw_all_p": raw_all_p,
                    "raw_all_n": raw_all_n,
                    "residual_all_r": all_r,
                    "residual_all_p": all_p,
                    "residual_all_n": all_n,
                    "raw_case_r": raw_case_r,
                    "raw_case_p": raw_case_p,
                    "raw_case_n": raw_case_n,
                    "residual_case_r": case_r,
                    "residual_case_p": case_p,
                    "residual_case_n": case_n,
                }
            )
    donor_export = pd.concat(donor_rows, ignore_index=True) if donor_rows else pd.DataFrame()
    return pd.DataFrame(rows), donor_export


def summarize_tests(tests: pd.DataFrame, w96: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gene, sub in tests.groupby("gene", sort=False):
        all_pos = sub[(sub["residual_all_r"] >= 0.30) & (sub["residual_all_p"].fillna(1.0) <= 0.20)]
        case_pos = sub[(sub["residual_case_r"] >= 0.30) & (sub["residual_case_p"].fillna(1.0) <= 0.20)]
        raw_case_pos = sub[(sub["raw_case_r"] >= 0.30) & (sub["raw_case_p"].fillna(1.0) <= 0.20)]
        rows.append(
            {
                "gene": gene,
                "contexts_tested": int(sub["analysis"].nunique()),
                "raw_case_positive_context_count": int(len(raw_case_pos)),
                "raw_case_positive_disease_count": int(raw_case_pos["disease_name"].nunique()),
                "residual_case_positive_context_count": int(len(case_pos)),
                "residual_case_positive_disease_count": int(case_pos["disease_name"].nunique()),
                "residual_all_positive_context_count": int(len(all_pos)),
                "residual_all_positive_disease_count": int(all_pos["disease_name"].nunique()),
                "median_raw_case_r": float(sub["raw_case_r"].median()) if not sub.empty else math.nan,
                "median_residual_case_r": float(sub["residual_case_r"].median()) if not sub.empty else math.nan,
                "median_residual_all_r": float(sub["residual_all_r"].median()) if not sub.empty else math.nan,
                "best_residual_context": clean(sub.sort_values(["residual_case_p", "residual_case_r"], ascending=[True, False]).iloc[0]["analysis"] if not sub.empty else ""),
                "best_residual_case_r": float(sub["residual_case_r"].max()) if not sub.empty else math.nan,
            }
        )
    summary = pd.DataFrame(rows)
    keep = [
        "gene",
        "wave96_call",
        "wave96_score",
        "critical_gate_count",
        "support_gate_count",
        "gate_ms_anchor",
        "gate_genetics",
        "gate_modality",
        "gate_cell_response_or_transition",
        "ms_delta_log2",
        "ms_p",
        "chembl_activity_count",
        "wave55_n_genetic_diseases_ge_0_25",
        "wave62_strong_qtl_coloc_disease_count",
    ]
    merged = summary.merge(w96[[c for c in keep if c in w96.columns]], on="gene", how="left")
    merged["residual_survival_fraction"] = (
        merged["residual_case_positive_context_count"] / merged["raw_case_positive_context_count"].replace(0, np.nan)
    )
    merged["gate_residual_costate_survives"] = (
        (merged["residual_case_positive_context_count"] >= 2)
        | ((merged["residual_case_positive_context_count"] >= 1) & (merged["residual_all_positive_context_count"] >= 2))
    )
    calls = []
    for rec in merged.to_dict("records"):
        if rec["gate_residual_costate_survives"] and bool(rec.get("gate_ms_anchor")) and bool(rec.get("gate_modality")) and (bool(rec.get("gate_genetics")) or bool(rec.get("gate_cell_response_or_transition"))):
            calls.append("REOPEN_AFTER_RESIDUAL_COSTATE")
        elif rec["gate_residual_costate_survives"] and bool(rec.get("gate_modality")):
            calls.append("PARK_RESIDUAL_COSTATE_WITH_MODALITY")
        elif rec["raw_case_positive_context_count"] > 0 and rec["residual_case_positive_context_count"] == 0:
            calls.append("NO_GO_GENERIC_INFLAMMATION_CONFONDED")
        else:
            calls.append("NO_GO_RESIDUAL_COSTATE_WEAK")
    merged["wave97_call"] = calls
    return merged.sort_values(
        ["wave97_call", "gate_residual_costate_survives", "residual_case_positive_disease_count", "wave96_score"],
        ascending=[True, False, False, False],
    )


def report_table(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "gene",
        "wave97_call",
        "residual_case_positive_context_count",
        "residual_case_positive_disease_count",
        "residual_all_positive_context_count",
        "median_raw_case_r",
        "median_residual_case_r",
        "gate_ms_anchor",
        "gate_genetics",
        "gate_modality",
        "gate_cell_response_or_transition",
        "ms_delta_log2",
        "ms_p",
        "wave96_call",
        "wave96_score",
    ]
    return df[[c for c in cols if c in df.columns]].copy()


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    w96 = pd.read_csv(W96, sep="\t", low_memory=False)
    w96["gene"] = w96["gene"].astype(str).str.upper()
    anchors = pd.read_csv(ANCHORS, sep="\t")
    candidates = sorted(w96.loc[w96["wave96_call"].eq("PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE"), "gene"].astype(str).str.upper())
    genes = set(candidates) | {"C15ORF48"}
    for module_genes in COVARIATE_MODULES.values():
        genes.update(g.upper() for g in module_genes)
    tests, donor_export = per_context_residual_tests(anchors, candidates, genes)
    summary = summarize_tests(tests, w96)

    tests.to_csv(OUT / "residual_costate_context_tests.tsv", sep="\t", index=False)
    donor_export.to_csv(OUT / "donor_covariate_scores.tsv", sep="\t", index=False)
    summary.to_csv(OUT / "residual_costate_candidate_summary.tsv", sep="\t", index=False)

    call_counts = summary["wave97_call"].value_counts().to_dict()
    reopened = summary[summary["wave97_call"].eq("REOPEN_AFTER_RESIDUAL_COSTATE")]
    parked = summary[summary["wave97_call"].eq("PARK_RESIDUAL_COSTATE_WITH_MODALITY")]
    write_json(
        OUT / "summary.json",
        {
            "seed": SEED,
            "analysis_call": "C15_RESIDUAL_COSTATE_FALSIFICATION_COMPLETED",
            "n_candidates": int(len(candidates)),
            "n_reopened": int(len(reopened)),
            "n_parked_residual": int(len(parked)),
            "call_counts": call_counts,
            "reopened": reopened["gene"].tolist(),
            "parked_residual": parked["gene"].tolist(),
            "inputs": {"wave96": rel(W96), "anchors": rel(ANCHORS)},
        },
    )

    report = [
        "# Wave97 C15 Residual Co-State Falsification",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Question",
        "",
        "Do Wave96 parked C15ORF48-proximal candidates remain coupled to C15ORF48",
        "after residualizing donor-level pseudo-bulk expression against disease",
        "status and a generic inflammatory/metabolic covariate mean?",
        "",
        "## Verdict",
        "",
        f"Reopened after residualization: `{len(reopened)}`.",
        f"Parked residual co-state with modality: `{len(parked)}`.",
        "",
        "## Call Counts",
        "",
        markdown_table(pd.DataFrame([{"wave97_call": k, "n": v} for k, v in call_counts.items()])),
        "",
        "## Candidate Summary",
        "",
        markdown_table(report_table(summary), max_rows=30),
        "",
        "## Interpretation",
        "",
        "This wave is a confounding check, not a causal model. Loss of residual",
        "co-state means the Wave96 signal is likely dominated by generic",
        "inflammatory/metabolic burden. Survival keeps a candidate alive only for",
        "prior-art and mechanism-directionality forcing tests.",
        "",
        "## Output Files",
        "",
        f"- `{rel(OUT / 'residual_costate_context_tests.tsv')}`",
        f"- `{rel(OUT / 'donor_covariate_scores.tsv')}`",
        f"- `{rel(OUT / 'residual_costate_candidate_summary.tsv')}`",
        f"- `{rel(OUT / 'summary.json')}`",
        f"- `{rel(OUT / 'REPORT.md')}`",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
