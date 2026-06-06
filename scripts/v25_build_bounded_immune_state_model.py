#!/usr/bin/env python3
"""Build and validate the V25 bounded immune-state module-response model."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v25_immune_state_model"
MODULE_SUMMARY = ROOT / "results_v3" / "mixscale" / "mixscale_module_summary.tsv"
SPLIT = OUT / "TRAIN_HELDOUT_SPLIT_V25.tsv"


def sign3(x: float, eps: float = 0.05) -> int:
    if pd.isna(x) or abs(x) < eps:
        return 0
    return 1 if x > 0 else -1


def label_sign(s: int) -> str:
    return {1: "increase", -1: "decrease", 0: "neutral"}[int(s)]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(MODULE_SUMMARY, sep="\t")
    split = pd.read_csv(SPLIT, sep="\t")
    data = data.merge(split[["pathway", "perturbation", "split"]], on=["pathway", "perturbation"], how="inner")
    train = data[data["split"].eq("train")].copy()
    held = data[data["split"].eq("held_out")].copy()

    model = (
        train.groupby(["pathway", "module"], dropna=False)
        .agg(
            pred_mean_log2fc=("mean_module_log2fc_across_cell_types", "mean"),
            pred_sd_log2fc=("mean_module_log2fc_across_cell_types", "std"),
            n_train_perturbations=("perturbation", "nunique"),
            train_negative_fraction=("cell_type_negative_fraction", "mean"),
        )
        .reset_index()
    )
    model["pred_sd_log2fc"] = model["pred_sd_log2fc"].fillna(0.0)
    model["confidence_raw"] = (
        model["pred_mean_log2fc"].abs() / (model["pred_sd_log2fc"].fillna(0) + 0.10)
    ).clip(0, 5)
    model["confidence_bin"] = pd.cut(
        model["confidence_raw"],
        bins=[-0.001, 0.5, 1.0, 2.0, 10.0],
        labels=["low", "medium", "high", "very_high"],
    )
    model.to_csv(OUT / "bounded_model_parameters.tsv", sep="\t", index=False)

    val = held.merge(model, on=["pathway", "module"], how="left")
    val["actual"] = val["mean_module_log2fc_across_cell_types"].astype(float)
    val["pred"] = val["pred_mean_log2fc"].astype(float)
    val["actual_sign"] = val["actual"].map(sign3)
    val["pred_sign"] = val["pred"].map(sign3)
    val["direction_correct"] = val["actual_sign"].eq(val["pred_sign"])
    val["abs_error"] = (val["actual"] - val["pred"]).abs()
    val["squared_error"] = (val["actual"] - val["pred"]) ** 2
    val["actual_direction"] = val["actual_sign"].map(label_sign)
    val["predicted_direction"] = val["pred_sign"].map(label_sign)
    val.to_csv(OUT / "heldout_predictions.tsv", sep="\t", index=False)

    overall = {
        "n_rows": int(len(val)),
        "n_heldout_perturbations": int(val[["pathway", "perturbation"]].drop_duplicates().shape[0]),
        "n_modules": int(val["module"].nunique()),
        "direction_accuracy": float(val["direction_correct"].mean()),
        "mae_log2fc": float(val["abs_error"].mean()),
        "rmse_log2fc": float(math.sqrt(val["squared_error"].mean())),
        "pearson_pred_actual": float(val[["pred", "actual"]].corr().iloc[0, 1]),
        "spearman_pred_actual": float(val[["pred", "actual"]].corr(method="spearman").iloc[0, 1]),
    }
    by_module = (
        val.groupby("module")
        .agg(
            n=("direction_correct", "size"),
            direction_accuracy=("direction_correct", "mean"),
            mae_log2fc=("abs_error", "mean"),
            pearson_pred_actual=("pred", lambda s: float(pd.Series(s).corr(val.loc[s.index, "actual"])) if len(s) > 1 else np.nan),
        )
        .reset_index()
    )
    by_module.to_csv(OUT / "heldout_metrics_by_module.tsv", sep="\t", index=False)

    cal = (
        val.groupby("confidence_bin", observed=False)
        .agg(
            n=("direction_correct", "size"),
            empirical_direction_accuracy=("direction_correct", "mean"),
            mean_confidence_raw=("confidence_raw", "mean"),
            mean_abs_error=("abs_error", "mean"),
        )
        .reset_index()
    )
    cal.to_csv(OUT / "calibration_by_confidence_bin.tsv", sep="\t", index=False)

    # Project checks and live hypothesis triage. Abstain outside validated domain.
    live = [
        {
            "hypothesis": "IFN/JAK-STAT immune-remodeling monitoring signal",
            "query_pathway": "IFNG",
            "query_perturbation": "JAK2",
            "module": "ifn_apc",
            "interpretation": "proxy for JAK/IFN pathway suppression of IFN/APC modules",
        },
        {
            "hypothesis": "HLA-II/APC remodeling through IFNG pathway blockade",
            "query_pathway": "IFNG",
            "query_perturbation": "STAT1",
            "module": "hla_ii_apc",
            "interpretation": "proxy for upstream IFNG-STAT1 axis",
        },
        {
            "hypothesis": "KIF21B/GPR25 chr1 expression-direction lead",
            "query_pathway": "",
            "query_perturbation": "KIF21B/GPR25",
            "module": "ifn_apc",
            "interpretation": "genetics/eQTL expression direction, not represented in Mixscale pathway domain",
        },
        {
            "hypothesis": "ZMIZ1 opposite-direction MS/Crohn decoupling",
            "query_pathway": "",
            "query_perturbation": "ZMIZ1",
            "module": "ifn_apc",
            "interpretation": "genetic decoupling, not a pathway perturbation in validated domain",
        },
    ]
    rows = []
    for item in live:
        if item["query_pathway"] and ((model["pathway"].eq(item["query_pathway"])) & (model["module"].eq(item["module"]))).any():
            m = model[(model["pathway"].eq(item["query_pathway"])) & (model["module"].eq(item["module"]))].iloc[0]
            rows.append(
                {
                    **item,
                    "domain_flag": "inside_bounded_pathway_module_domain",
                    "prediction_log2fc": m["pred_mean_log2fc"],
                    "predicted_direction": label_sign(sign3(m["pred_mean_log2fc"])),
                    "confidence_bin": m["confidence_bin"],
                    "confidence_raw": m["confidence_raw"],
                    "action": "use_as_low_resolution_directional_prior_only",
                }
            )
        else:
            rows.append(
                {
                    **item,
                    "domain_flag": "outside_validated_domain_abstain",
                    "prediction_log2fc": np.nan,
                    "predicted_direction": "abstain",
                    "confidence_bin": "abstain",
                    "confidence_raw": np.nan,
                    "action": "do_not_use_model_for_this_hypothesis",
                }
            )
    pd.DataFrame(rows).to_csv(OUT / "live_hypothesis_triage.tsv", sep="\t", index=False)

    summary = {
        "architecture": "bounded_empirical_pathway_module_mean_model",
        "train_perturbations": int(train[["pathway", "perturbation"]].drop_duplicates().shape[0]),
        "heldout_perturbations": overall["n_heldout_perturbations"],
        "metrics": overall,
        "validated_domain": "directional module effects for Mixscale-like IFNB/IFNG/TNFA pathway contexts; low-resolution only",
        "not_validated_for": [
            "patient-level response prediction",
            "single-cell compartment simulation",
            "genetics-only expression-direction hypotheses",
            "unseen pathways or unseen module definitions",
        ],
    }
    (OUT / "model_validation_summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
