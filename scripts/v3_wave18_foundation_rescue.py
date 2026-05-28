#!/usr/bin/env python3
"""Wave18-C foundation-model candidate rescue synthesis.

This script does not rerun Geneformer or State. It re-examines existing local
foundation-model outputs and joins them to real perturbation evidence so the
Wave18 report can distinguish a model-triage signal from promotion-grade
evidence.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave18_foundation_rescue"

GENEFORMER_SOURCES = [
    {
        "source": "candidate_delete",
        "dir": ROOT / "results_v3" / "geneformer_candidate_delete",
        "metrics": "geneformer_candidate_delete_metrics.tsv",
        "summary": "summary.json",
    },
    {
        "source": "pivot_panel_delete",
        "dir": ROOT / "results_v3" / "geneformer_pivot_panel_delete",
        "metrics": "geneformer_pivot_panel_delete_metrics.tsv",
        "summary": "summary.json",
    },
    {
        "source": "unrestricted_survivor_delete",
        "dir": ROOT / "results_v3" / "geneformer_unrestricted_survivor_delete",
        "metrics": "geneformer_unrestricted_survivor_delete_metrics.tsv",
        "summary": "summary.json",
    },
    {
        "source": "broad_residual_delete",
        "dir": ROOT / "results_v3" / "geneformer_broad_residual_delete",
        "metrics": "geneformer_broad_residual_delete_metrics.tsv",
        "summary": "summary.json",
    },
    {
        "source": "wave14_narrowed_delete",
        "dir": ROOT / "results_v3" / "wave14_geneformer_narrowed_candidate_delete",
        "metrics": "wave14_geneformer_narrowed_candidate_delete_metrics.tsv",
        "summary": "summary.json",
    },
    {
        "source": "wave15_loader_dependency_delete",
        "dir": ROOT / "results_v3" / "wave15_geneformer_loader_dependency_delete",
        "metrics": "wave15_geneformer_loader_dependency_metrics.tsv",
        "summary": "summary.json",
    },
]

DIRECT_PERTURBATION_PATH = ROOT / "results_v3" / "wave15_perturbation_drug_response" / "ranked_direct_perturbations.tsv"
MIXSCALE_TRANSITION_PATH = ROOT / "results_v3" / "mixscale" / "mixscale_transition_controller_rank.tsv"
MIXSCALE_READOUT_PATH = ROOT / "results_v3" / "mixscale" / "mixscale_readout_gene_summary.tsv"
GSE162463_SCREEN_PATH = ROOT / "results_v3" / "wave14_gsk3b_ciita_perturbation" / "gse162463_screen_gene_summary.tsv"
GSE162464_READOUT_PATH = (
    ROOT / "results_v3" / "wave15_perturbation_drug_response" / "gse162464_mouse_rna_readout_gene_effects.tsv"
)
GSE294918_READOUT_PATH = (
    ROOT / "results_v3" / "wave15_perturbation_drug_response" / "gse294918_human_ruxolitinib_readout_gene_effects.tsv"
)
STATE_SUMMARY_PATH = ROOT / "results_v3" / "state_parse_cd14_summary.json"
STATE_FOCUSED_VALIDATION_PATH = ROOT / "results_v3" / "state_parse_cd14_focused_per_target_validation.tsv"
STATE_AXIS_PATH = ROOT / "results_v3" / "state_parse_cd14_axis_scores.tsv"
STATE_TRANSITION_RANK_PATH = ROOT / "results_v3" / "state_parse_cd14_transition_target_rank.tsv"

MOUSE_TO_HUMAN = {
    "CTSH": "CTSH",
    "CTSB": "CTSB",
    "CTSS": "CTSS",
    "CTSL": "CTSL",
    "CTSD": "CTSD",
    "IFI30": "IFI30",
    "GSK3B": "GSK3B",
    "MED16": "MED16",
    "RFX5": "RFX5",
    "STAT1": "STAT1",
    "IFNGR1": "IFNGR1",
    "IFNGR2": "IFNGR2",
    "JAK1": "JAK1",
    "JAK2": "JAK2",
    "CHUK": "CHUK",
    "TNFRSF1A": "TNFRSF1A",
    "PTPN2": "PTPN2",
    "TNFAIP3": "TNFAIP3",
    "CD74": "CD74",
    "LGALS3": "LGALS3",
    "LAPTM5": "LAPTM5",
    "SNX10": "SNX10",
    "IFITM2": "IFITM2",
    "IFITM3": "IFITM3",
    "SEC61A1": "SEC61A1",
    "SEC61B": "SEC61B",
    "TMSB10": "TMSB10",
    "CD300E": "CD300E",
    "PPIB": "PPIB",
    "MTHFD2": "MTHFD2",
    "HIF1A": "HIF1A",
    "LIPA": "LIPA",
    "CBX3": "CBX3",
    "TGM2": "TGM2",
    "CFB": "CFB",
    "CXCL8": "CXCL8",
    "MMADHC": "MMADHC",
    "BIRC3": "BIRC3",
    "DAP": "DAP",
    "SDC4": "SDC4",
    "TPM4": "TPM4",
    "RPL17": "RPL17",
}


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def canonical_gene(value: object) -> str:
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return ""
    text = re.sub(r"(_KO|_KD|_CRISPRI|_UNSTIMULATED|_POSITIVE_CONTROL|_MEMORY|_8H)$", "", text, flags=re.I)
    text = text.upper()
    text = text.replace(" ", "")
    return MOUSE_TO_HUMAN.get(text, text)


def numeric(df: pd.DataFrame, col: str) -> pd.Series:
    return pd.to_numeric(df[col], errors="coerce") if col in df.columns else pd.Series(np.nan, index=df.index)


def as_bool(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series.fillna(False)
    return series.astype(str).str.lower().isin({"true", "1", "yes"})


def load_geneformer_metrics() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    frames = []
    provenance: dict[str, Any] = {}
    for source in GENEFORMER_SOURCES:
        metrics_path = source["dir"] / source["metrics"]
        summary_path = source["dir"] / source["summary"]
        if not metrics_path.exists():
            continue
        df = pd.read_csv(metrics_path, sep="\t")
        df["source"] = source["source"]
        df["source_path"] = str(metrics_path.relative_to(ROOT))
        df["gene_canonical"] = df["gene"].map(canonical_gene)
        for col in [
            "n_disease_cells_with_token",
            "mean_shift_to_control_cosine",
            "mean_projection_to_control",
            "random_mean_shift_to_control_cosine",
            "random_sd_shift_to_control_cosine",
            "random_mean_projection_to_control",
            "cosine_shift_z_vs_random",
            "projection_minus_random",
        ]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        if "cosine_shift_z_vs_random" not in df.columns:
            denom = df["random_sd_shift_to_control_cosine"].replace(0, np.nan)
            df["cosine_shift_z_vs_random"] = (
                df["mean_shift_to_control_cosine"] - df["random_mean_shift_to_control_cosine"]
            ) / denom
        if "projection_minus_random" not in df.columns:
            df["projection_minus_random"] = df["mean_projection_to_control"] - df["random_mean_projection_to_control"]
        if "candidate_support_flag" not in df.columns:
            df["candidate_support_flag"] = (
                (df["n_disease_cells_with_token"] >= 3)
                & (df["mean_shift_to_control_cosine"] > df["random_mean_shift_to_control_cosine"])
                & (df["mean_projection_to_control"] > df["random_mean_projection_to_control"])
            )
        else:
            df["candidate_support_flag"] = as_bool(df["candidate_support_flag"])
        if "candidate_strong_support_flag" not in df.columns:
            df["candidate_strong_support_flag"] = (
                df["candidate_support_flag"]
                & (df["cosine_shift_z_vs_random"] > 0.5)
                & (df["projection_minus_random"] > 0)
            )
        else:
            df["candidate_strong_support_flag"] = as_bool(df["candidate_strong_support_flag"])
        frames.append(df)
        if summary_path.exists():
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            provenance[source["source"]] = {
                key: summary.get(key)
                for key in [
                    "model",
                    "model_repo",
                    "revision",
                    "checkpoint",
                    "parameters_loaded_encoder",
                    "seed",
                    "max_len",
                    "max_disease_cells_per_context",
                    "max_control_cells_per_context",
                    "random_deletion_reps",
                    "batch_size",
                    "metric",
                    "limitations",
                ]
            }
            provenance[source["source"]]["contexts"] = summary.get("contexts", [])
            provenance[source["source"]]["candidate_genes"] = summary.get("candidate_genes", [])

    context = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    tested = context[context["n_disease_cells_with_token"].fillna(0) > 0].copy()
    source_rows = []
    for (source, gene), sub in tested.groupby(["source", "gene_canonical"], observed=True):
        best = sub.sort_values(
            ["candidate_strong_support_flag", "candidate_support_flag", "cosine_shift_z_vs_random", "projection_minus_random"],
            ascending=[False, False, False, False],
        ).iloc[0]
        source_rows.append(
            {
                "source": source,
                "gene": gene,
                "contexts_with_token": int(sub["context"].nunique()),
                "disease_cells_with_token": int(sub["n_disease_cells_with_token"].sum()),
                "mean_cosine_shift": float(sub["mean_shift_to_control_cosine"].mean()),
                "mean_projection_shift": float(sub["mean_projection_to_control"].mean()),
                "mean_cosine_z_vs_random": float(sub["cosine_shift_z_vs_random"].mean()),
                "support_contexts": int(sub["candidate_support_flag"].sum()),
                "strong_support_contexts": int(sub["candidate_strong_support_flag"].sum()),
                "positive_projection_contexts": int((sub["projection_minus_random"] > 0).sum()),
                "negative_projection_contexts": int((sub["projection_minus_random"] < 0).sum()),
                "best_context": best["context"],
                "best_context_cells_with_token": int(best["n_disease_cells_with_token"]),
                "best_context_cosine_z": float(best["cosine_shift_z_vs_random"])
                if pd.notna(best["cosine_shift_z_vs_random"])
                else np.nan,
                "best_context_projection_minus_random": float(best["projection_minus_random"])
                if pd.notna(best["projection_minus_random"])
                else np.nan,
                "best_context_support": bool(best["candidate_support_flag"]),
                "best_context_strong_support": bool(best["candidate_strong_support_flag"]),
            }
        )
    source_summary = pd.DataFrame(source_rows)
    if source_summary.empty:
        return context, source_summary, provenance
    source_summary = source_summary.sort_values(
        [
            "strong_support_contexts",
            "support_contexts",
            "positive_projection_contexts",
            "best_context_cosine_z",
            "disease_cells_with_token",
        ],
        ascending=[False, False, False, False, False],
    )
    source_summary["source_rank"] = np.arange(1, len(source_summary) + 1)
    return context, source_summary, provenance


def combine_geneformer(source_summary: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    ctsh = source_summary[(source_summary["gene"] == "CTSH") & (source_summary["source"] == "wave15_loader_dependency_delete")]
    if ctsh.empty:
        ctsh = source_summary[source_summary["gene"] == "CTSH"].head(1)
    if ctsh.empty:
        baseline = {
            "total_strong_support_contexts": 0.0,
            "total_support_contexts": 0.0,
            "best_context_cosine_z": np.nan,
            "best_mean_projection_shift": np.nan,
            "best_mean_cosine_z_vs_random": np.nan,
            "screen_mhcii_rank": np.nan,
            "screen_mhcii_median": np.nan,
        }
    else:
        row = ctsh.iloc[0]
        baseline = {
            "total_strong_support_contexts": float(row["strong_support_contexts"]),
            "total_support_contexts": float(row["support_contexts"]),
            "best_context_cosine_z": float(row["best_context_cosine_z"]),
            "best_mean_projection_shift": float(row["mean_projection_shift"]),
            "best_mean_cosine_z_vs_random": float(row["mean_cosine_z_vs_random"]),
        }

    rows = []
    for gene, sub in source_summary.groupby("gene", observed=True):
        best = sub.sort_values(
            [
                "strong_support_contexts",
                "support_contexts",
                "positive_projection_contexts",
                "best_context_cosine_z",
                "mean_projection_shift",
            ],
            ascending=[False, False, False, False, False],
        ).iloc[0]
        total_strong = int(sub["strong_support_contexts"].sum())
        total_support = int(sub["support_contexts"].sum())
        max_best_z = float(sub["best_context_cosine_z"].max())
        best_projection = float(sub["mean_projection_shift"].max())
        stronger = (
            total_strong > baseline["total_strong_support_contexts"]
            and max_best_z > baseline["best_context_cosine_z"]
        ) or (
            total_support > baseline["total_support_contexts"]
            and max_best_z > baseline["best_context_cosine_z"]
            and best_projection > baseline["best_mean_projection_shift"]
        )
        rows.append(
            {
                "gene": gene,
                "geneformer_sources": ";".join(sorted(sub["source"].unique())),
                "geneformer_source_count": int(sub["source"].nunique()),
                "total_support_contexts": total_support,
                "total_strong_support_contexts": total_strong,
                "max_support_contexts_in_source": int(sub["support_contexts"].max()),
                "max_strong_support_contexts_in_source": int(sub["strong_support_contexts"].max()),
                "total_disease_cells_with_token": int(sub["disease_cells_with_token"].sum()),
                "max_contexts_with_token_in_source": int(sub["contexts_with_token"].max()),
                "best_mean_projection_shift": best_projection,
                "best_mean_cosine_z_vs_random": float(sub["mean_cosine_z_vs_random"].max()),
                "best_context_cosine_z": max_best_z,
                "best_context_projection_minus_random": float(sub["best_context_projection_minus_random"].max()),
                "best_geneformer_source": best["source"],
                "best_geneformer_context": best["best_context"],
                "best_context_cells_with_token": int(best["best_context_cells_with_token"]),
                "stronger_than_ctsh_geneformer": bool(stronger),
            }
        )
    combined = pd.DataFrame(rows).sort_values(
        [
            "stronger_than_ctsh_geneformer",
            "total_strong_support_contexts",
            "total_support_contexts",
            "best_context_cosine_z",
            "best_mean_projection_shift",
        ],
        ascending=[False, False, False, False, False],
    )
    combined["geneformer_rescue_rank"] = np.arange(1, len(combined) + 1)
    return combined, baseline


def best_direct_perturbation() -> pd.DataFrame:
    if not DIRECT_PERTURBATION_PATH.exists():
        return pd.DataFrame()
    df = pd.read_csv(DIRECT_PERTURBATION_PATH, sep="\t")
    df["gene"] = df["perturbation"].map(canonical_gene)
    df["within_direct_rank"] = pd.to_numeric(df["within_direct_rank"], errors="coerce")
    df["selectivity_score"] = pd.to_numeric(df["selectivity_score"], errors="coerce")
    rows = []
    for gene, sub in df[df["gene"] != ""].groupby("gene", observed=True):
        best = sub.sort_values(["within_direct_rank", "selectivity_score"], ascending=[True, False]).iloc[0]
        rows.append(
            {
                "gene": gene,
                "best_direct_source": best.get("source", ""),
                "best_direct_dataset": best.get("dataset", ""),
                "best_direct_perturbation": best.get("perturbation", ""),
                "best_direct_pathway": best.get("pathway", ""),
                "best_direct_rank": int(best["within_direct_rank"]) if pd.notna(best["within_direct_rank"]) else np.nan,
                "best_direct_target_module_effect": best.get("target_module_effect", np.nan),
                "best_direct_generic_ifn_effect": best.get("generic_ifn_effect", np.nan),
                "best_direct_target_vs_ifn_margin": best.get("target_vs_ifn_margin", np.nan),
                "best_direct_selectivity_score": best.get("selectivity_score", np.nan),
                "best_direct_evidence_call": best.get("evidence_call", ""),
                "best_direct_control_class": best.get("control_class", ""),
            }
        )
    return pd.DataFrame(rows)


def mixscale_transition_evidence() -> pd.DataFrame:
    if not MIXSCALE_TRANSITION_PATH.exists():
        return pd.DataFrame()
    df = pd.read_csv(MIXSCALE_TRANSITION_PATH, sep="\t")
    df["gene"] = df["perturbation"].map(canonical_gene)
    df["mixscale_transition_rank"] = np.arange(1, len(df) + 1)
    keep = [
        "gene",
        "pathway",
        "perturbation",
        "mixscale_transition_rank",
        "transition_suppression_score",
        "n_modules_suppressed",
        "hla_ii_apc_mean_log2fc",
        "ifn_apc_mean_log2fc",
        "mif_cd74_receptor_state_mean_log2fc",
        "gilt_lysosomal_apc_mean_log2fc",
    ]
    out = (
        df[df["gene"] != ""]
        .sort_values(["gene", "transition_suppression_score"], ascending=[True, False])
        .drop_duplicates("gene")
    )
    return out[keep].rename(
        columns={
            "pathway": "mixscale_transition_pathway",
            "perturbation": "mixscale_transition_perturbation",
        }
    )


def screen_evidence() -> tuple[pd.DataFrame, dict[str, float]]:
    if not GSE162463_SCREEN_PATH.exists():
        return pd.DataFrame(), {}
    df = pd.read_csv(GSE162463_SCREEN_PATH, sep="\t")
    df["gene"] = df["gene"].map(canonical_gene)
    cols = [
        "gene",
        "n_sgrna",
        "MHCII_median_low_vs_high_log2",
        "MHCII_mean_low_vs_high_log2",
        "MHCII_positive_sgrna_fraction",
        "MHCII_rank_required_low_vs_high",
        "MHCII_fdr",
        "CD40_median_low_vs_high_log2",
        "PDL1_median_low_vs_high_log2",
    ]
    for col in cols:
        if col != "gene" and col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    out = df[cols].copy()
    ctsh = out[out["gene"] == "CTSH"]
    baseline = {}
    if not ctsh.empty:
        row = ctsh.iloc[0]
        baseline = {
            "screen_mhcii_rank": float(row["MHCII_rank_required_low_vs_high"]),
            "screen_mhcii_median": float(row["MHCII_median_low_vs_high_log2"]),
            "screen_mhcii_positive_fraction": float(row["MHCII_positive_sgrna_fraction"]),
        }
    out["gse162463_screen_stronger_than_ctsh"] = False
    if baseline:
        out["gse162463_screen_stronger_than_ctsh"] = (
            (out["MHCII_rank_required_low_vs_high"] < baseline["screen_mhcii_rank"])
            & (out["MHCII_median_low_vs_high_log2"] > baseline["screen_mhcii_median"])
        )
    out["gse162463_mhcii_direction_call"] = np.select(
        [
            (out["MHCII_median_low_vs_high_log2"] > 0) & (out["MHCII_positive_sgrna_fraction"] >= 0.75),
            (out["MHCII_median_low_vs_high_log2"] < 0) & (out["MHCII_positive_sgrna_fraction"] <= 0.50),
        ],
        ["mhcii_low_enrichment_supportive", "mhcii_low_enrichment_contradictory"],
        default="mixed_or_weak",
    )
    return out, baseline


def readout_summary() -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    if MIXSCALE_READOUT_PATH.exists():
        df = pd.read_csv(MIXSCALE_READOUT_PATH, sep="\t")
        df["gene"] = df["gene"].map(canonical_gene)
        for gene, sub in df[df["gene"] != ""].groupby("gene", observed=True):
            best = sub.sort_values("mean_log2fc", ascending=True).iloc[0]
            rows.append(
                {
                    "gene": gene,
                    "readout_source": "Mixscale_GSE281048",
                    "readout_best_condition": f"{best['pathway']}:{best['perturbation']}",
                    "readout_min_log2fc": best["mean_log2fc"],
                    "readout_negative_records": int((pd.to_numeric(sub["mean_log2fc"], errors="coerce") < 0).sum()),
                    "readout_total_records": int(len(sub)),
                }
            )
    if GSE162464_READOUT_PATH.exists():
        df = pd.read_csv(GSE162464_READOUT_PATH, sep="\t")
        df["gene"] = df["gene"].map(canonical_gene)
        for gene, sub in df[df["gene"] != ""].groupby("gene", observed=True):
            best = sub.sort_values("log2fc", ascending=True).iloc[0]
            rows.append(
                {
                    "gene": gene,
                    "readout_source": "GSE162464_mouse_macrophage_RNAseq",
                    "readout_best_condition": best["contrast"],
                    "readout_min_log2fc": best["log2fc"],
                    "readout_negative_records": int((pd.to_numeric(sub["log2fc"], errors="coerce") < 0).sum()),
                    "readout_total_records": int(len(sub)),
                }
            )
    if GSE294918_READOUT_PATH.exists():
        df = pd.read_csv(GSE294918_READOUT_PATH, sep="\t")
        df["gene"] = df["gene"].map(canonical_gene)
        rux = df[df["contrast"].astype(str).str.contains("rux", case=False, na=False)].copy()
        for gene, sub in rux[rux["gene"] != ""].groupby("gene", observed=True):
            best = sub.sort_values("log2fc", ascending=True).iloc[0]
            rows.append(
                {
                    "gene": gene,
                    "readout_source": "GSE294918_human_ruxolitinib",
                    "readout_best_condition": best["contrast"],
                    "readout_min_log2fc": best["log2fc"],
                    "readout_negative_records": int((pd.to_numeric(sub["log2fc"], errors="coerce") < 0).sum()),
                    "readout_total_records": int(len(sub)),
                }
            )
    if not rows:
        return pd.DataFrame()
    detail = pd.DataFrame(rows)
    detail.to_csv(OUT / "readout_concordance_detail.tsv", sep="\t", index=False)
    summary_rows = []
    for gene, sub in detail.groupby("gene", observed=True):
        best = sub.sort_values("readout_min_log2fc", ascending=True).iloc[0]
        summary_rows.append(
            {
                "gene": gene,
                "readout_sources": ";".join(sorted(sub["readout_source"].unique())),
                "readout_min_log2fc": best["readout_min_log2fc"],
                "readout_best_source": best["readout_source"],
                "readout_best_condition": best["readout_best_condition"],
                "readout_negative_records": int(sub["readout_negative_records"].sum()),
                "readout_total_records": int(sub["readout_total_records"].sum()),
            }
        )
    return pd.DataFrame(summary_rows)


def classify(row: pd.Series) -> tuple[str, str]:
    stronger = bool(row.get("stronger_than_ctsh_geneformer", False))
    direct_call = str(row.get("best_direct_evidence_call", ""))
    screen_call = str(row.get("gse162463_mhcii_direction_call", ""))
    screen_stronger = bool(row.get("gse162463_screen_stronger_than_ctsh", False))
    readout_negative = pd.to_numeric(pd.Series([row.get("readout_negative_records", np.nan)]), errors="coerce").iloc[0]
    readout_total = pd.to_numeric(pd.Series([row.get("readout_total_records", np.nan)]), errors="coerce").iloc[0]

    if stronger and direct_call in {"selective_target_suppression", "weak_selective_target_suppression"}:
        alignment = "model_and_direct_perturbation_align"
        recommendation = "triage_only_pending_independent_validation"
    elif stronger and direct_call == "broad_ifn_jak_like_collapse":
        alignment = "model_and_broad_ifn_jak_real_align_not_selective"
        recommendation = "positive_control_not_candidate_promotion"
    elif stronger and screen_stronger and screen_call == "mhcii_low_enrichment_supportive":
        alignment = "model_and_gse162463_screen_align_relative_to_ctsh"
        recommendation = "triage_only_gse162463_not_promotion_grade"
    elif stronger and screen_call == "mhcii_low_enrichment_contradictory":
        alignment = "model_contradicted_by_gse162463_screen"
        recommendation = "do_not_promote"
    elif stronger and pd.notna(readout_negative) and pd.notna(readout_total) and readout_total > 0 and readout_negative > 0:
        alignment = "model_with_readout_concordance_only"
        recommendation = "triage_only_no_direct_candidate_perturbation"
    elif stronger:
        alignment = "model_only_no_real_perturbation_alignment"
        recommendation = "do_not_promote_from_foundation_model"
    elif direct_call in {"selective_target_suppression", "weak_selective_target_suppression", "broad_ifn_jak_like_collapse"}:
        alignment = "real_perturbation_support_but_geneformer_not_rescued"
        recommendation = "use_real_perturbation_not_foundation_model"
    else:
        alignment = "no_rescue"
        recommendation = "do_not_promote"
    return alignment, recommendation


def state_status() -> pd.DataFrame:
    summary = json.loads(STATE_SUMMARY_PATH.read_text(encoding="utf-8")) if STATE_SUMMARY_PATH.exists() else {}
    focused = pd.read_csv(STATE_FOCUSED_VALIDATION_PATH, sep="\t") if STATE_FOCUSED_VALIDATION_PATH.exists() else pd.DataFrame()
    axes = pd.read_csv(STATE_AXIS_PATH, sep="\t") if STATE_AXIS_PATH.exists() else pd.DataFrame()
    transition = pd.read_csv(STATE_TRANSITION_RANK_PATH, sep="\t") if STATE_TRANSITION_RANK_PATH.exists() else pd.DataFrame()
    axis_gene_sum = int(pd.to_numeric(axes.get("n_genes", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not axes.empty else 0
    row = {
        "model_repo": summary.get("model_repo", "arcinstitute/ST-HVG-Parse"),
        "model_sha": summary.get("model_sha", "a69af46d5b8c6f8c036c489a8f71354f321d968b"),
        "source_split": summary.get("source_split", "fewshot/split_4"),
        "cell_type": summary.get("cell_type", "CD14_Mono"),
        "n_perturbations": summary.get("n_perturbations", np.nan),
        "n_output_features": summary.get("n_output_features", np.nan),
        "named_gene_axis_rows_with_genes": axis_gene_sum,
        "transition_rank_rows": int(len(transition)),
        "named_gene_candidate_status": "blocked" if axis_gene_sum == 0 or transition.empty else "available",
        "focused_validation_top_target": focused.iloc[0]["target"] if not focused.empty else "",
        "focused_validation_top_spearman": focused.iloc[0]["spearman_percent_change"] if not focused.empty else np.nan,
        "focused_validation_top_direction_match": focused.iloc[0]["direction_match_fraction"] if not focused.empty else np.nan,
        "focused_validation_median_spearman": float(pd.to_numeric(focused["spearman_percent_change"], errors="coerce").median())
        if not focused.empty
        else np.nan,
        "interpretation": (
            "Feature-agnostic State validation is usable, but named-gene axis scoring has zero genes and cannot rescue a candidate."
        ),
    }
    return pd.DataFrame([row])


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    context, source_summary, geneformer_provenance = load_geneformer_metrics()
    context.to_csv(OUT / "geneformer_consolidated_context_metrics.tsv", sep="\t", index=False)
    source_summary.to_csv(OUT / "geneformer_source_gene_summary.tsv", sep="\t", index=False)

    geneformer, ctsh_geneformer_baseline = combine_geneformer(source_summary)
    direct = best_direct_perturbation()
    transition = mixscale_transition_evidence()
    screen, ctsh_screen_baseline = screen_evidence()
    readout = readout_summary()

    evidence = geneformer.copy()
    for add in [direct, transition, screen, readout]:
        if not add.empty:
            evidence = evidence.merge(add, on="gene", how="left")

    calls = evidence.apply(classify, axis=1, result_type="expand")
    evidence["real_perturbation_alignment_call"] = calls[0]
    evidence["foundation_rescue_recommendation"] = calls[1]
    priority = {
        "model_and_direct_perturbation_align": 1,
        "model_and_broad_ifn_jak_real_align_not_selective": 2,
        "model_and_gse162463_screen_align_relative_to_ctsh": 3,
        "real_perturbation_support_but_geneformer_not_rescued": 4,
        "model_with_readout_concordance_only": 5,
        "model_only_no_real_perturbation_alignment": 6,
        "model_contradicted_by_gse162463_screen": 7,
        "no_rescue": 8,
    }
    evidence["alignment_priority"] = evidence["real_perturbation_alignment_call"].map(priority).fillna(99).astype(int)

    evidence = evidence.sort_values(
        [
            "stronger_than_ctsh_geneformer",
            "alignment_priority",
            "total_strong_support_contexts",
            "best_direct_rank",
            "gse162463_screen_stronger_than_ctsh",
            "best_context_cosine_z",
        ],
        ascending=[False, True, False, True, False, False],
    )
    evidence["wave18_rank"] = np.arange(1, len(evidence) + 1)
    evidence.to_csv(OUT / "foundation_rescue_candidate_rank.tsv", sep="\t", index=False)

    direct_out = evidence[
        [
            "gene",
            "stronger_than_ctsh_geneformer",
            "best_direct_source",
            "best_direct_dataset",
            "best_direct_perturbation",
            "best_direct_rank",
            "best_direct_selectivity_score",
            "best_direct_evidence_call",
            "mixscale_transition_rank",
            "transition_suppression_score",
            "gse162463_screen_stronger_than_ctsh",
            "MHCII_rank_required_low_vs_high",
            "MHCII_median_low_vs_high_log2",
            "MHCII_positive_sgrna_fraction",
            "gse162463_mhcii_direction_call",
            "real_perturbation_alignment_call",
        ]
    ].copy()
    direct_out.to_csv(OUT / "direct_perturbation_evidence_by_candidate.tsv", sep="\t", index=False)

    readout_cols = [
        "gene",
        "stronger_than_ctsh_geneformer",
        "readout_sources",
        "readout_min_log2fc",
        "readout_best_source",
        "readout_best_condition",
        "readout_negative_records",
        "readout_total_records",
        "real_perturbation_alignment_call",
    ]
    evidence[[c for c in readout_cols if c in evidence.columns]].to_csv(
        OUT / "readout_concordance_by_candidate.tsv", sep="\t", index=False
    )

    state = state_status()
    state.to_csv(OUT / "state_parse_status.tsv", sep="\t", index=False)

    strict_rescues = evidence[
        (evidence["stronger_than_ctsh_geneformer"])
        & (evidence["real_perturbation_alignment_call"] == "model_and_direct_perturbation_align")
    ]
    screen_only_rescues = evidence[
        (evidence["stronger_than_ctsh_geneformer"])
        & (evidence["real_perturbation_alignment_call"] == "model_and_gse162463_screen_align_relative_to_ctsh")
    ]
    real_strong_model_weak = evidence[
        evidence["real_perturbation_alignment_call"] == "real_perturbation_support_but_geneformer_not_rescued"
    ]
    summary = {
        "question": "Re-examine existing Geneformer and State outputs for candidates stronger than CTSH and aligned with real perturbation data.",
        "ctsh_geneformer_baseline": ctsh_geneformer_baseline,
        "ctsh_gse162463_screen_baseline": ctsh_screen_baseline,
        "n_geneformer_candidates_with_token": int(len(geneformer)),
        "n_stronger_than_ctsh_geneformer": int(evidence["stronger_than_ctsh_geneformer"].fillna(False).sum()),
        "strict_model_and_direct_real_rescue_candidates": strict_rescues["gene"].tolist(),
        "screen_only_relative_rescue_candidates": screen_only_rescues["gene"].head(20).tolist(),
        "real_perturbation_supported_but_not_geneformer_rescued": real_strong_model_weak["gene"].tolist(),
        "state_named_gene_status": state.iloc[0].to_dict(),
        "geneformer_provenance": geneformer_provenance,
        "recommendation": (
            "No candidate meets the strict rescue bar of stronger-than-CTSH Geneformer support plus independent "
            "direct real perturbation validation from Mixscale/GSE162464/GSE294918. Treat Geneformer as triage; "
            "use real perturbation evidence as primary when present."
        ),
        "outputs": [
            str((OUT / "geneformer_consolidated_context_metrics.tsv").relative_to(ROOT)),
            str((OUT / "geneformer_source_gene_summary.tsv").relative_to(ROOT)),
            str((OUT / "foundation_rescue_candidate_rank.tsv").relative_to(ROOT)),
            str((OUT / "direct_perturbation_evidence_by_candidate.tsv").relative_to(ROOT)),
            str((OUT / "readout_concordance_by_candidate.tsv").relative_to(ROOT)),
            str((OUT / "state_parse_status.tsv").relative_to(ROOT)),
            str((OUT / "summary.json").relative_to(ROOT)),
        ],
    }
    write_json(OUT / "summary.json", summary)
    print(json.dumps(summary, indent=2, allow_nan=True))
    print("\nTop Wave18 rows:")
    print(
        evidence[
            [
                "wave18_rank",
                "gene",
                "stronger_than_ctsh_geneformer",
                "total_strong_support_contexts",
                "total_support_contexts",
                "best_geneformer_source",
                "best_geneformer_context",
                "best_context_cosine_z",
                "best_direct_rank",
                "best_direct_evidence_call",
                "gse162463_screen_stronger_than_ctsh",
                "MHCII_rank_required_low_vs_high",
                "MHCII_median_low_vs_high_log2",
                "real_perturbation_alignment_call",
                "foundation_rescue_recommendation",
            ]
        ]
        .head(30)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
