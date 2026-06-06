#!/usr/bin/env python3
"""Broad residual-gated panel search after survivor-gene failure.

This script reuses the selected-gene aggregation and residualization machinery
from `v3_snx10_c15orf48_residual_gate.py`, but expands the gene panel from the
full broad h5ad rank table plus mechanistic scout genes. The goal is to find
whether any expression-recurrent gene survives generic-inflammation and
stress/lysosomal/lipid covariate gates before further foundation-model,
genetics, or prior-art work is spent on it.

This remains a discovery gate. It is not a therapeutic finding.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse

import v3_snx10_c15orf48_residual_gate as gate
from v3_analyze_osmr_complement_axes import CONFIGS, ROOT

SEED = 20260526
RESULTS = ROOT / "phases/v3/results"
OUT = RESULTS / "broad_residual_gate"
BROAD_RANK = RESULTS / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
MS_SIGNATURE = RESULTS / "gse111972_full_ms_wm_signature.tsv"

MAX_RANK_PANEL = 180
SYMBOL_RE = re.compile(r"^[A-Z][A-Z0-9_.-]{1,20}$")

MECHANISTIC_SCOUT_GENES = [
    "ACSL1",
    "ACSL3",
    "ACSL4",
    "APOC1",
    "AXL",
    "CALR",
    "CARD16",
    "CASP4",
    "CASP8",
    "CD200R1",
    "CD24",
    "CD300A",
    "CD300E",
    "CD300F",
    "CD300LF",
    "CD36",
    "CD74",
    "CD82",
    "CHI3L1",
    "CTSB",
    "CTSL",
    "CTSS",
    "CXCL9",
    "DAP",
    "FABP5",
    "FCGR2B",
    "GPNMB",
    "HIF1A",
    "IDO1",
    "IFI30",
    "IFITM2",
    "IFITM3",
    "IL15",
    "IL23A",
    "IL2RG",
    "IRF1",
    "JAK1",
    "JAK2",
    "JAK3",
    "LAMP3",
    "LIPA",
    "LTA4H",
    "MARCO",
    "MERTK",
    "MIF",
    "MSR1",
    "NAMPT",
    "NLRP3",
    "NLRC5",
    "NR1H3",
    "OSM",
    "OSMR",
    "PDE4B",
    "PDE4D",
    "PIKFYVE",
    "POMP",
    "PPARG",
    "PSME1",
    "PSME2",
    "SDC4",
    "SIGLEC10",
    "SNX10",
    "SPP1",
    "STAT1",
    "TFEB",
    "TFE3",
    "TIMP1",
    "TNFAIP8L1",
    "TREM2",
    "TYK2",
    "TYROBP",
]


def valid_symbol(symbol: object) -> str | None:
    value = str(symbol).strip().upper()
    if not SYMBOL_RE.match(value):
        return None
    if value.startswith(("ENSG", "LOC", "LINC", "MIR", "RNU", "SNOR")):
        return None
    return value


def load_ms_signature() -> pd.DataFrame:
    if not MS_SIGNATURE.exists():
        return pd.DataFrame(columns=["gene", "ms_wm_delta_log2", "ms_wm_p", "ms_wm_fdr"])
    ms = pd.read_csv(MS_SIGNATURE, sep="\t")
    ms["gene"] = ms["gene"].astype(str).str.upper()
    return ms.rename(columns={"delta_log2": "ms_wm_delta_log2", "p": "ms_wm_p", "fdr": "ms_wm_fdr"})[
        ["gene", "ms_wm_delta_log2", "ms_wm_p", "ms_wm_fdr"]
    ]


def build_candidate_panel() -> pd.DataFrame:
    rank = pd.read_csv(BROAD_RANK, sep="\t", low_memory=False)
    rank["gene"] = rank["gene"].map(valid_symbol)
    rank = rank.loc[rank["gene"].notna()].copy()
    for col in [
        "positive_disease_count",
        "negative_disease_count",
        "positive_compartment_count",
        "negative_compartment_count",
        "discovery_priority_score",
    ]:
        rank[col] = pd.to_numeric(rank[col], errors="coerce").fillna(0)
    rank["ms_positive_nominal"] = rank["ms_positive_nominal"].fillna(False).astype(bool)
    rank["in_lipid_lysosomal_myeloid_neighborhood"] = rank[
        "in_lipid_lysosomal_myeloid_neighborhood"
    ].fillna(False).astype(bool)

    selected: dict[str, set[str]] = {}

    def add(gene: str, reason: str) -> None:
        selected.setdefault(gene, set()).add(reason)

    for _, row in rank.head(MAX_RANK_PANEL).iterrows():
        add(row["gene"], "top_rank")
    for _, row in rank.loc[rank["positive_disease_count"] >= 5].iterrows():
        add(row["gene"], "five_disease")
    for _, row in rank.loc[
        (rank["positive_disease_count"] >= 4) & (rank["negative_disease_count"] <= 1)
    ].iterrows():
        add(row["gene"], "four_disease_low_contradiction")
    for _, row in rank.loc[
        (rank["positive_disease_count"] >= 3)
        & (rank["negative_disease_count"] <= 1)
        & rank["ms_positive_nominal"]
    ].iterrows():
        add(row["gene"], "ms_positive_three_disease")
    for _, row in rank.loc[
        (rank["positive_disease_count"] >= 2) & rank["in_lipid_lysosomal_myeloid_neighborhood"]
    ].iterrows():
        add(row["gene"], "lipid_lysosomal_two_disease")
    for gene in MECHANISTIC_SCOUT_GENES:
        symbol = valid_symbol(gene)
        if symbol:
            add(symbol, "mechanistic_scout")

    panel = pd.DataFrame(
        [{"gene": gene, "selection_reasons": ";".join(sorted(reasons))} for gene, reasons in selected.items()]
    )
    panel = panel.merge(
        rank[
            [
                "gene",
                "discovery_priority_score",
                "positive_disease_count",
                "negative_disease_count",
                "positive_compartment_count",
                "negative_compartment_count",
                "positive_fdr10_compartment_count",
                "ms_positive_nominal",
                "ms_wm_delta_log2",
                "ms_wm_p",
                "ms_wm_fdr",
                "in_lipid_lysosomal_myeloid_neighborhood",
                "top_positive_compartments",
            ]
        ],
        on="gene",
        how="left",
    )
    panel = panel.merge(load_ms_signature(), on="gene", how="left", suffixes=("", "_sig"))
    for col in ["ms_wm_delta_log2", "ms_wm_p", "ms_wm_fdr"]:
        sig_col = f"{col}_sig"
        if sig_col in panel.columns:
            panel[col] = panel[col].combine_first(panel[sig_col])
            panel = panel.drop(columns=[sig_col])
    panel = panel.sort_values(
        ["positive_disease_count", "ms_positive_nominal", "discovery_priority_score"],
        ascending=[False, False, False],
    )
    return panel.reset_index(drop=True)


def strict_summary(raw_tests: pd.DataFrame, residuals: pd.DataFrame, panel: pd.DataFrame) -> pd.DataFrame:
    raw_gene = raw_tests.loc[raw_tests["metric"] == "mean_z_vs_controls"].copy()
    rows: list[dict[str, object]] = []
    for gene, info in panel.set_index("gene").iterrows():
        raw_sub = raw_gene.loc[raw_gene["gene"] == gene]
        resid_sub = residuals.loc[residuals["gene"] == gene]
        raw_pos = raw_sub.loc[raw_sub["positive_nominal"]]
        raw_neg = raw_sub.loc[raw_sub["negative_nominal"]]
        retained = resid_sub.loc[resid_sub["retains_nominal_positive"]]
        core_uni = resid_sub.loc[
            resid_sub["residual_model"].eq("univariate")
            & resid_sub["covariate_set"].isin(gate.CORE_COVARIATES)
        ]
        strict_rows = []
        for analysis, sub in core_uni.groupby("analysis", observed=True):
            if len(sub) == len(gate.CORE_COVARIATES) and bool(sub["retains_nominal_positive"].all()):
                first = sub.iloc[0]
                strict_rows.append(
                    {
                        "analysis": analysis,
                        "disease_name": first["disease_name"],
                        "compartment": first["compartment"],
                    }
                )
        strict_df = pd.DataFrame(strict_rows)
        non_ibd_retained = retained.loc[
            ~retained["disease_name"].astype(str).isin(["Crohn disease", "ulcerative colitis"])
        ]
        rows.append(
            {
                "gene": gene,
                "selection_reasons": info.get("selection_reasons", ""),
                "discovery_priority_score": info.get("discovery_priority_score", np.nan),
                "broad_positive_disease_count": info.get("positive_disease_count", np.nan),
                "broad_negative_disease_count": info.get("negative_disease_count", np.nan),
                "broad_ms_positive_nominal": bool(info.get("ms_positive_nominal", False)),
                "ms_wm_delta_log2": info.get("ms_wm_delta_log2", np.nan),
                "ms_wm_p": info.get("ms_wm_p", np.nan),
                "in_lipid_lysosomal_myeloid_neighborhood": bool(
                    info.get("in_lipid_lysosomal_myeloid_neighborhood", False)
                ),
                "raw_positive_analysis_count": int(raw_pos["analysis"].nunique()),
                "raw_positive_disease_count": int(raw_pos["disease_name"].nunique()),
                "raw_negative_analysis_count": int(raw_neg["analysis"].nunique()),
                "retained_positive_analysis_count": int(retained["analysis"].nunique()),
                "retained_positive_disease_count": int(retained["disease_name"].nunique()),
                "non_ibd_retained_positive_analysis_count": int(non_ibd_retained["analysis"].nunique()),
                "non_ibd_retained_positive_disease_count": int(non_ibd_retained["disease_name"].nunique()),
                "strict_core_covariate_surviving_analysis_count": int(len(strict_df)),
                "strict_core_covariate_surviving_disease_count": int(strict_df["disease_name"].nunique())
                if not strict_df.empty
                else 0,
                "strict_core_covariate_surviving_analyses": ";".join(
                    strict_df.apply(lambda r: f"{r['analysis']}:{r['disease_name']}", axis=1).tolist()
                )
                if not strict_df.empty
                else "",
                "raw_positive_analyses": ";".join(
                    raw_pos.sort_values(["p", "delta_case_minus_control"], ascending=[True, False])
                    .head(8)
                    .apply(lambda r: f"{r['analysis']}:{r['delta_case_minus_control']:.3g},p={r['p']:.2g}", axis=1)
                    .tolist()
                ),
                "top_retained_tests": ";".join(
                    retained.sort_values(["residual_p", "residual_delta_case_minus_control"], ascending=[True, False])
                    .head(8)
                    .apply(
                        lambda r: (
                            f"{r['analysis']}|{r['covariate_set']}:"
                            f"{r['residual_delta_case_minus_control']:.3g},p={r['residual_p']:.2g}"
                        ),
                        axis=1,
                    )
                    .tolist()
                ),
            }
        )
    out = pd.DataFrame(rows)
    out["residual_gate_priority_score"] = (
        5 * out["strict_core_covariate_surviving_disease_count"].fillna(0)
        + 2 * out["strict_core_covariate_surviving_analysis_count"].fillna(0)
        + 2 * out["non_ibd_retained_positive_disease_count"].fillna(0)
        + out["retained_positive_disease_count"].fillna(0)
        + 2 * out["broad_ms_positive_nominal"].astype(int)
        + out["in_lipid_lysosomal_myeloid_neighborhood"].astype(int)
        - 3 * out["raw_negative_analysis_count"].fillna(0)
    )
    out = out.sort_values(
        [
            "residual_gate_priority_score",
            "strict_core_covariate_surviving_disease_count",
            "non_ibd_retained_positive_disease_count",
            "retained_positive_disease_count",
            "raw_positive_disease_count",
        ],
        ascending=[False, False, False, False, False],
    )
    return out


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    panel = build_candidate_panel()
    panel.to_csv(OUT / "broad_residual_candidate_panel.tsv", sep="\t", index=False)

    gate.TARGET_GENES = sorted(panel["gene"].astype(str).unique())
    cache: dict[Path, tuple] = {}
    gene_score_tables: list[pd.DataFrame] = []
    presence_tables: list[pd.DataFrame] = []
    run_log: list[dict[str, object]] = []
    for config in CONFIGS:
        try:
            print(f"[broad-residual] starting {config.name}", flush=True)
            if config.path not in cache:
                a = ad.read_h5ad(config.path)
                x = a.X.tocsr() if sparse.issparse(a.X) else sparse.csr_matrix(a.X)
                cache[config.path] = (a, x)
            a, x = cache[config.path]
            scores, presence = gate.aggregate_config(config, a, x)
            gene_score_tables.append(scores)
            presence_tables.append(presence)
            run_log.append(
                {
                    "analysis": config.name,
                    "status": "completed",
                    "n_donor_gene_rows": int(len(scores)),
                    "n_present_panel_genes": int(presence["gene"].nunique()),
                }
            )
            print(
                f"[broad-residual] completed {config.name}: "
                f"{len(scores)} donor-gene rows, {presence['gene'].nunique()} genes",
                flush=True,
            )
        except Exception as exc:
            run_log.append(
                {
                    "analysis": config.name,
                    "status": "failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            print(f"[broad-residual] failed {config.name}: {type(exc).__name__}: {exc}", flush=True)

    gene_scores = pd.concat(gene_score_tables, ignore_index=True) if gene_score_tables else pd.DataFrame()
    presence = pd.concat(presence_tables, ignore_index=True) if presence_tables else pd.DataFrame()
    gene_scores.to_csv(OUT / "broad_residual_gene_donor_scores.tsv", sep="\t", index=False)
    presence.to_csv(OUT / "broad_residual_gene_presence.tsv", sep="\t", index=False)

    raw_tests = gate.run_raw_tests(gene_scores)
    residuals = gate.run_residual_tests(gene_scores, gate.load_module_wide())
    summary = strict_summary(raw_tests, residuals, panel)

    raw_tests.to_csv(OUT / "broad_residual_raw_tests.tsv", sep="\t", index=False)
    residuals.to_csv(OUT / "broad_residual_residual_tests.tsv", sep="\t", index=False)
    summary.to_csv(OUT / "broad_residual_gate_summary.tsv", sep="\t", index=False)

    payload = {
        "random_seed": SEED,
        "n_panel_genes": int(panel["gene"].nunique()),
        "run_log": run_log,
        "selection_logic": {
            "max_rank_panel": MAX_RANK_PANEL,
            "criteria": [
                "top discovery-priority genes",
                "all genes with >=5 positive diseases",
                "all genes with >=4 positive diseases and <=1 negative disease",
                "all MS-positive genes with >=3 positive diseases and <=1 negative disease",
                "all lipid/lysosomal-neighborhood genes with >=2 positive diseases",
                "manual mechanistic scout genes",
            ],
        },
        "top_gate_rows": summary.head(40).to_dict(orient="records"),
        "guardrail": (
            "This is a residualized expression recurrence screen. It does not provide "
            "genetics, causal perturbation, druggability, novelty, or safety evidence."
        ),
    }
    (OUT / "broad_residual_gate_summary.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
