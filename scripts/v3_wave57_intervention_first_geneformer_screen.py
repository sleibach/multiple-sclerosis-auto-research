#!/usr/bin/env python3
"""Wave57 intervention-first Geneformer deletion screen.

This wave responds to repeated marker-only failures. It asks whether any
module-proximal, druggable/modality-addressable candidate has foundation-model
triage support across disease-relevant contexts. The screen reuses the bounded
Geneformer V2-104M token-deletion machinery already used in prior V3 waves.

Interpretation limits:
- This is a model-hypothesis screen, not a causal perturbation experiment.
- A positive result is only a reopener if it is paired with local expression,
  external genetics, and an intervention modality.
- A negative result is sufficient to prevent model-based promotion but does
  not prove the gene is biologically irrelevant.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "phases/v3/tmp" / "foundation_wave6" / "geneformer_tiny_delete_screen.py"
OUT = ROOT / "phases/v3/results" / "wave57_intervention_first_geneformer_screen"
SEED = 20260527

CANDIDATE_GENES = [
    # Lysosomal/lipid enzyme and clearance axis.
    "GALC",
    "LIPA",
    "CTSD",
    "CTSB",
    "CTSS",
    "SMPD1",
    "GBA1",
    "GLA",
    "HEXA",
    "HEXB",
    "PSAP",
    "ASAH1",
    # Wave55 cross-disease / local recurrence axes.
    "SP140",
    "IL7R",
    "CCL20",
    "PTPN2",
    "DAP",
    "PARK7",
    "CARMIL1",
    "CCDC88B",
    "TRIB2",
    # Druggable or semi-druggable comparators.
    "CXCR2",
    "PRKCB",
    "HDAC7",
    "STAT4",
    "CD40",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_wave6_module():
    spec = importlib.util.spec_from_file_location("geneformer_wave6_intervention", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def zscore_against_random(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    denom = out["random_sd_shift_to_control_cosine"].replace(0, pd.NA)
    out["cosine_shift_z_vs_random"] = (
        out["mean_shift_to_control_cosine"] - out["random_mean_shift_to_control_cosine"]
    ) / denom
    out["projection_minus_random"] = out["mean_projection_to_control"] - out["random_mean_projection_to_control"]
    out["candidate_support_flag"] = (
        (out["n_disease_cells_with_token"] >= 3)
        & (out["mean_shift_to_control_cosine"] > out["random_mean_shift_to_control_cosine"])
        & (out["mean_projection_to_control"] > out["random_mean_projection_to_control"])
    )
    out["candidate_strong_support_flag"] = (
        out["candidate_support_flag"]
        & (out["cosine_shift_z_vs_random"] > 0.5)
        & (out["projection_minus_random"] > 0)
    )
    return out


def summarize(metrics: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gene, sub in metrics.groupby("gene", dropna=False):
        support = sub[sub["candidate_support_flag"].fillna(False)]
        strong = sub[sub["candidate_strong_support_flag"].fillna(False)]
        token_contexts = sub[sub["n_disease_cells_with_token"].fillna(0) >= 3]
        best = sub.sort_values(
            ["candidate_strong_support_flag", "candidate_support_flag", "cosine_shift_z_vs_random", "projection_minus_random"],
            ascending=[False, False, False, False],
        ).iloc[0]
        rows.append(
            {
                "gene": gene,
                "contexts_tested": int(sub["context"].nunique()),
                "contexts_with_token_ge_3_cells": int(token_contexts["context"].nunique()),
                "support_contexts": int(support["context"].nunique()),
                "strong_support_contexts": int(strong["context"].nunique()),
                "best_context": best.get("context"),
                "best_n_disease_cells_with_token": best.get("n_disease_cells_with_token"),
                "best_cosine_shift_z_vs_random": best.get("cosine_shift_z_vs_random"),
                "best_projection_minus_random": best.get("projection_minus_random"),
                "best_mean_shift_to_control_cosine": best.get("mean_shift_to_control_cosine"),
                "best_random_mean_shift_to_control_cosine": best.get("random_mean_shift_to_control_cosine"),
                "supporting_contexts": ";".join(sorted(support["context"].astype(str).unique())),
                "strong_supporting_contexts": ";".join(sorted(strong["context"].astype(str).unique())),
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["wave57_model_priority_score"] = (
        out["strong_support_contexts"].fillna(0) * 5
        + out["support_contexts"].fillna(0) * 2
        + out["contexts_with_token_ge_3_cells"].fillna(0) * 0.25
    )
    return out.sort_values(
        ["wave57_model_priority_score", "strong_support_contexts", "support_contexts", "best_cosine_shift_z_vs_random"],
        ascending=[False, False, False, False],
    )


def join_external(summary: pd.DataFrame) -> pd.DataFrame:
    rank_path = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
    broad_path = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
    residual_path = ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
    wave37_path = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
    rank = pd.read_csv(rank_path, sep="\t", low_memory=False) if rank_path.exists() else pd.DataFrame()
    broad = pd.read_csv(broad_path, sep="\t", low_memory=False) if broad_path.exists() else pd.DataFrame()
    residual = pd.read_csv(residual_path, sep="\t", low_memory=False) if residual_path.exists() else pd.DataFrame()
    wave37 = pd.read_csv(wave37_path, sep="\t", low_memory=False) if wave37_path.exists() else pd.DataFrame()

    out = summary.copy()
    if not rank.empty:
        cols = [
            "gene",
            "n_diseases_genetic_ge_0_25",
            "diseases_genetic_ge_0_25",
            "ms_genetic_association",
            "max_clinical_score",
            "max_literature_score",
        ]
        out = out.merge(rank[[c for c in cols if c in rank.columns]], on="gene", how="left")
    if not broad.empty:
        cols = [
            "gene",
            "positive_disease_count",
            "negative_disease_count",
            "positive_diseases",
            "negative_diseases",
            "ms_wm_delta_log2",
            "ms_wm_p",
            "ms_wm_fdr",
            "best_positive_tests",
            "in_lipid_lysosomal_myeloid_neighborhood",
        ]
        out = out.merge(broad[[c for c in cols if c in broad.columns]], on="gene", how="left")
    if not residual.empty:
        cols = [
            "gene",
            "retained_positive_disease_count",
            "strict_core_covariate_surviving_disease_count",
            "strict_core_covariate_surviving_analyses",
            "top_retained_tests",
        ]
        out = out.merge(residual[[c for c in cols if c in residual.columns]], on="gene", how="left")
    if not wave37.empty:
        cols = [
            "gene_symbol",
            "median_efficient_minus_noneater_lfc",
            "contrast_fdr",
            "screen_call",
        ]
        eff = wave37[[c for c in cols if c in wave37.columns]].rename(columns={"gene_symbol": "gene"})
        out = out.merge(eff, on="gene", how="left")
    return out


def call_candidates(joined: pd.DataFrame) -> pd.DataFrame:
    out = joined.copy()
    out["cross_disease_genetics_pass"] = out["n_diseases_genetic_ge_0_25"].fillna(0) >= 4
    out["local_recurrence_pass"] = (out["positive_disease_count"].fillna(0) >= 3) & (out["negative_disease_count"].fillna(0) <= 1)
    out["strict_ms_pass"] = out["ms_wm_fdr"].fillna(1.0) < 0.1
    out["model_support_pass"] = out["strong_support_contexts"].fillna(0) >= 1
    out["efferocytosis_pass"] = (
        (out["median_efficient_minus_noneater_lfc"].fillna(0) > 0.5)
        & (out["contrast_fdr"].fillna(1.0) < 0.2)
    )
    out["critical_gate_pass_count"] = out[
        [
            "cross_disease_genetics_pass",
            "local_recurrence_pass",
            "strict_ms_pass",
            "model_support_pass",
            "efferocytosis_pass",
        ]
    ].sum(axis=1)
    out["wave57_call"] = "NO_GO_MODEL_SCREEN"
    out.loc[
        (out["cross_disease_genetics_pass"])
        & (out["local_recurrence_pass"])
        & (out["model_support_pass"]),
        "wave57_call",
    ] = "REOPEN_MODEL_SUPPORTED_INTERVENTION_FIRST"
    out.loc[
        (out["cross_disease_genetics_pass"])
        & (out["local_recurrence_pass"])
        & (out["model_support_pass"])
        & (out["strict_ms_pass"]),
        "wave57_call",
    ] = "PROMOTE_FOR_FULL_THERAPEUTIC_AUDIT"
    priority = {
        "PROMOTE_FOR_FULL_THERAPEUTIC_AUDIT": 0,
        "REOPEN_MODEL_SUPPORTED_INTERVENTION_FIRST": 1,
        "NO_GO_MODEL_SCREEN": 2,
    }
    out["wave57_call_priority"] = out["wave57_call"].map(priority).fillna(9)
    return out.sort_values(
        ["wave57_call_priority", "critical_gate_pass_count", "wave57_model_priority_score"],
        ascending=[True, False, False],
    )


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        vals = []
        for col in cols:
            val = "" if pd.isna(row[col]) else str(row[col])
            vals.append(val.replace("\n", " ").replace("|", "\\|")[:500])
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    gf = load_wave6_module()
    gf.OUT = OUT
    gf.SEED = SEED
    gf.CANDIDATE_GENES = CANDIDATE_GENES
    gf.MAX_DISEASE = 24
    gf.MAX_CONTROL = 24
    gf.RANDOM_REPS = 3
    gf.CONTEXTS = [
        gf.Context("IBD_myeloid", "data/raw_v3/cell_state/ibd_human_10x.h5ad", "myeloid cell", tuple(CANDIDATE_GENES)),
        gf.Context("IBD_epithelial", "data/raw_v3/cell_state/ibd_human_10x.h5ad", "colon epithelial cell", tuple(CANDIDATE_GENES)),
        gf.Context("psoriasis_macrophage", "data/raw_v3/cell_state/psoriasis_skin.h5ad", "macrophage", tuple(CANDIDATE_GENES)),
        gf.Context("psoriasis_dendritic", "data/raw_v3/cell_state/psoriasis_skin.h5ad", "dendritic cell, human", tuple(CANDIDATE_GENES)),
        gf.Context("psoriasis_keratinocyte", "data/raw_v3/cell_state/psoriasis_skin.h5ad", "keratinocyte_family", tuple(CANDIDATE_GENES)),
        gf.Context("sjogren_APC", "data/raw_v3/cell_state/sjogren_salivary.h5ad", "salivary_APC", tuple(CANDIDATE_GENES)),
        gf.Context("t1d_ductal", "data/raw_v3/cell_state/t1d_hpap_islet.h5ad", "pancreatic ductal cell", tuple(CANDIDATE_GENES)),
        gf.Context("t1d_acinar", "data/raw_v3/cell_state/t1d_hpap_islet.h5ad", "pancreatic acinar cell", tuple(CANDIDATE_GENES)),
        gf.Context("ra_classical_monocyte", "data/raw_v3/cell_state/ra_binvignat_blood.h5ad", "classical monocyte", tuple(CANDIDATE_GENES)),
        gf.Context("ra_nonclassical_monocyte", "data/raw_v3/cell_state/ra_binvignat_blood.h5ad", "non-classical monocyte", tuple(CANDIDATE_GENES)),
        gf.Context("ra_myeloid_dendritic", "data/raw_v3/cell_state/ra_binvignat_blood.h5ad", "myeloid dendritic cell", tuple(CANDIDATE_GENES)),
    ]
    gf.main()
    metrics = pd.read_csv(OUT / "geneformer_tiny_delete_metrics.tsv", sep="\t")
    metrics = zscore_against_random(metrics)
    metrics.to_csv(OUT / "wave57_geneformer_metrics.tsv", sep="\t", index=False)
    summary = summarize(metrics)
    summary.to_csv(OUT / "wave57_geneformer_gene_summary.tsv", sep="\t", index=False)
    joined = join_external(summary)
    called = call_candidates(joined)
    called.to_csv(OUT / "wave57_intervention_first_candidate_calls.tsv", sep="\t", index=False)
    reopened = called[called["wave57_call"].str.contains("REOPEN|PROMOTE", regex=True, na=False)]
    payload = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "candidate_gene_count": len(CANDIDATE_GENES),
        "contexts": [ctx.name for ctx in gf.CONTEXTS],
        "promote_count": int((called["wave57_call"] == "PROMOTE_FOR_FULL_THERAPEUTIC_AUDIT").sum()),
        "reopen_count": int((called["wave57_call"] == "REOPEN_MODEL_SUPPORTED_INTERVENTION_FIRST").sum()),
        "top_calls": called.head(12)[["gene", "wave57_call", "critical_gate_pass_count", "wave57_model_priority_score"]].to_dict("records"),
        "outputs": {
            "metrics": rel(OUT / "wave57_geneformer_metrics.tsv"),
            "gene_summary": rel(OUT / "wave57_geneformer_gene_summary.tsv"),
            "candidate_calls": rel(OUT / "wave57_intervention_first_candidate_calls.tsv"),
        },
        "interpretation": (
            "Wave57 is a foundation-model triage screen. Promotion requires downstream full audit; "
            "model support alone is not treated as therapeutic evidence."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")
    report = [
        "# Wave57 Intervention-First Geneformer Screen",
        "",
        "## Summary",
        "",
        f"Promote count: {payload['promote_count']}; reopen count: {payload['reopen_count']}.",
        "",
        "## Top Candidate Calls",
        "",
        markdown_table(called.head(25)),
        "",
        "## Reopened Candidates",
        "",
        markdown_table(reopened),
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
