#!/usr/bin/env python3
"""Analyze Arc State released CD14 monocyte perturbation predictions.

Input files are official released outputs from the Hugging Face model repo
`arcinstitute/ST-HVG-Parse`, split 4, CD14_Mono. They contain model-predicted
and matched real differential expression for cytokine perturbations vs PBS.

The released DE files expose anonymous numeric HVG feature IDs. The exact
feature-to-gene order is blocked without very large companion AnnData files, so
this script does not make gene-level biological claims. It performs only
feature-agnostic validation of predicted vs observed perturbation effects and
records the gene-module scoring blocker.
"""

from __future__ import annotations

import json
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "state_parse_split4"
TMP = ROOT / "tmp_v3"
OUT = ROOT / "results_v3"
ADATA_REAL_PATH = RAW / "adata_real.h5ad"

MODEL_REPO = "arcinstitute/ST-HVG-Parse"
MODEL_SHA = "a69af46d5b8c6f8c036c489a8f71354f321d968b"
SOURCE_SPLIT = "fewshot/split_4"
CELL_TYPE = "CD14_Mono"

AXES = {
    "lysosomal_antigen_processing": ["IFI30", "CTSD", "CTSB", "CTSS", "LAMP1", "LAMP2", "TPP1", "HLA-DRA", "HLA-DRB1", "CD74"],
    "interferon_apc": ["STAT1", "IRF1", "IRF7", "CXCL10", "IFI30", "HLA-DRA", "HLA-DRB1", "CD74", "GBP1", "ISG15"],
    "metabolic_hif_nampt": ["HIF1A", "NAMPT", "LDHA", "SLC2A1", "NFKBIA", "IL1B"],
    "inflammatory_cytokine": ["IL1B", "TNF", "CXCL8", "CCL2", "CCL3", "CCL4", "NFKBIA", "TREM1"],
    "complement_phagocytosis": ["C1QA", "C1QB", "C1QC", "MSR1", "MARCO", "MERTK", "FCGR3A", "CD68"],
    "lipid_loader": ["ACSL1", "APOE", "GPNMB", "LPL", "PLIN2", "CD36", "LIPA", "FABP5", "TREM2"],
}

PERTURBATIONS_OF_INTEREST = [
    "IFN-alpha1",
    "IFN-beta",
    "IFN-gamma",
    "IFN-lambda1",
    "IL-1-alpha",
    "IL-17A",
    "IL-17C",
    "TNF-alpha",
    "GM-CSF",
    "C5a",
    "BAFF",
    "APRIL",
    "CD40L",
    "OSM",
    "TGF-beta",
]


def load_gene_map() -> tuple[dict[int, str], str]:
    with (TMP / "var_dims_split4.pkl").open("rb") as fh:
        var = pickle.load(fh)
    output_dim = int(var["output_dim"])
    if ADATA_REAL_PATH.exists() and ADATA_REAL_PATH.stat().st_size > 1_000_000:
        try:
            import anndata as ad

            adata = ad.read_h5ad(ADATA_REAL_PATH, backed="r")
            var_names = list(map(str, adata.var_names))
            if len(var_names) == output_dim:
                adata.file.close()
                return (
                    {i: gene for i, gene in enumerate(var_names)},
                    "mapped_from_adata_real_var_names",
                )
            status = f"adata_real_var_names_length_{len(var_names)}_does_not_match_output_dim_{output_dim}"
            adata.file.close()
            return ({i: f"FEATURE_{i}" for i in range(output_dim)}, status)
        except Exception as exc:
            return ({i: f"FEATURE_{i}" for i in range(output_dim)}, f"adata_real_mapping_failed:{type(exc).__name__}:{exc}")

    # Feature IDs in the released DE CSV are 0..1999. The companion full AnnData
    # object should define the exact HVG feature order. Until it is available,
    # we do not map these IDs to gene symbols; using the first 2,000 gene_names
    # in var_dims.pkl is wrong because candidate genes land outside that range.
    return (
        {i: f"FEATURE_{i}" for i in range(output_dim)},
        "feature IDs retained because exact HVG gene order requires adata_real.h5ad",
    )


def load_de(path: Path, kind: str, gene_map: dict[int, str]) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["gene"] = df["feature"].map(gene_map)
    df["kind"] = kind
    return df


def signed_metric(df: pd.DataFrame) -> pd.Series:
    # Use percent_change as signed effect. It is directly released in both files.
    return df.set_index(["target", "gene"])["percent_change"]


def module_scores(metric: pd.Series, kind: str) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    targets = sorted(metric.index.get_level_values("target").unique())
    for target in targets:
        target_series = metric.loc[target]
        for axis, genes in AXES.items():
            present = [g for g in genes if g in target_series.index]
            vals = target_series.reindex(present).dropna()
            if vals.empty:
                rows.append(
                    {
                        "kind": kind,
                        "target": target,
                        "axis": axis,
                        "n_genes": 0,
                        "genes_present": "",
                        "mean_percent_change": np.nan,
                        "median_percent_change": np.nan,
                        "positive_fraction": np.nan,
                    }
                )
                continue
            rows.append(
                {
                    "kind": kind,
                    "target": target,
                    "axis": axis,
                    "n_genes": int(len(vals)),
                    "genes_present": ",".join(vals.index.tolist()),
                    "mean_percent_change": float(vals.mean()),
                    "median_percent_change": float(vals.median()),
                    "positive_fraction": float((vals > 0).mean()),
                }
            )
    return pd.DataFrame(rows)


def compare_pred_real(pred: pd.DataFrame, real: pd.DataFrame) -> pd.DataFrame:
    merged = pred.merge(real, on=["target", "axis"], suffixes=("_pred", "_real"))
    rows = []
    for axis, sub in merged.groupby("axis"):
        ok = sub[["mean_percent_change_pred", "mean_percent_change_real"]].dropna()
        if len(ok) >= 3:
            rho = stats.spearmanr(ok["mean_percent_change_pred"], ok["mean_percent_change_real"]).statistic
            pearson = stats.pearsonr(ok["mean_percent_change_pred"], ok["mean_percent_change_real"]).statistic
            direction = float(np.mean(np.sign(ok["mean_percent_change_pred"]) == np.sign(ok["mean_percent_change_real"])))
        else:
            rho = np.nan
            pearson = np.nan
            direction = np.nan
        rows.append(
            {
                "axis": axis,
                "n_targets": int(len(ok)),
                "spearman_pred_real": float(rho) if pd.notna(rho) else np.nan,
                "pearson_pred_real": float(pearson) if pd.notna(pearson) else np.nan,
                "direction_match_fraction": direction,
            }
        )
    return pd.DataFrame(rows).sort_values("spearman_pred_real", ascending=False)


def per_target_validation(pred: pd.DataFrame, real: pd.DataFrame) -> pd.DataFrame:
    merged = pred.merge(
        real,
        on=["target", "feature"],
        suffixes=("_pred", "_real"),
        validate="one_to_one",
    )
    rows: list[dict[str, object]] = []
    for target, sub in merged.groupby("target"):
        ok = sub[
            [
                "percent_change_pred",
                "percent_change_real",
                "fdr_pred",
                "fdr_real",
                "p_value_pred",
                "p_value_real",
            ]
        ].replace([np.inf, -np.inf], np.nan)
        valid_effect = ok[["percent_change_pred", "percent_change_real"]].dropna()
        if len(valid_effect) >= 5:
            spearman = stats.spearmanr(valid_effect["percent_change_pred"], valid_effect["percent_change_real"]).statistic
            pearson = stats.pearsonr(valid_effect["percent_change_pred"], valid_effect["percent_change_real"]).statistic
            direction = float(
                np.mean(
                    np.sign(valid_effect["percent_change_pred"])
                    == np.sign(valid_effect["percent_change_real"])
                )
            )
            mae = float(
                np.mean(
                    np.abs(valid_effect["percent_change_pred"] - valid_effect["percent_change_real"])
                )
            )
        else:
            spearman = np.nan
            pearson = np.nan
            direction = np.nan
            mae = np.nan
        real_sig = ok["fdr_real"] < 0.05
        pred_sig = ok["fdr_pred"] < 0.05
        overlap = int((real_sig & pred_sig).sum())
        rows.append(
            {
                "target": target,
                "n_features": int(len(valid_effect)),
                "spearman_percent_change": float(spearman) if pd.notna(spearman) else np.nan,
                "pearson_percent_change": float(pearson) if pd.notna(pearson) else np.nan,
                "direction_match_fraction": direction,
                "mean_abs_error_percent_change": mae,
                "real_sig_features_fdr05": int(real_sig.sum()),
                "pred_sig_features_fdr05": int(pred_sig.sum()),
                "sig_feature_overlap": overlap,
                "sig_feature_recall": float(overlap / real_sig.sum()) if int(real_sig.sum()) else np.nan,
                "sig_feature_precision": float(overlap / pred_sig.sum()) if int(pred_sig.sum()) else np.nan,
                "mean_abs_real_percent_change": float(valid_effect["percent_change_real"].abs().mean()),
                "mean_abs_pred_percent_change": float(valid_effect["percent_change_pred"].abs().mean()),
                "is_perturbation_of_interest": target in PERTURBATIONS_OF_INTEREST,
            }
        )
    return pd.DataFrame(rows).sort_values(["is_perturbation_of_interest", "spearman_percent_change"], ascending=[False, False])


def focused_table(scores: pd.DataFrame) -> pd.DataFrame:
    return scores[scores["target"].isin(PERTURBATIONS_OF_INTEREST)].sort_values(
        ["axis", "kind", "mean_percent_change"], ascending=[True, True, False]
    )


def main() -> None:
    OUT.mkdir(exist_ok=True)
    gene_map, gene_mapping_status = load_gene_map()
    pred = load_de(RAW / "CD14_Mono_pred_de.csv", "state_predicted", gene_map)
    real = load_de(RAW / "CD14_Mono_real_de.csv", "real_observed", gene_map)
    combined_de = pd.concat([pred, real], ignore_index=True)
    combined_de.to_csv(OUT / "state_parse_cd14_de_with_gene_symbols.tsv", sep="\t", index=False)

    pred_scores = module_scores(signed_metric(pred), "state_predicted")
    real_scores = module_scores(signed_metric(real), "real_observed")
    scores = pd.concat([pred_scores, real_scores], ignore_index=True)
    scores.to_csv(OUT / "state_parse_cd14_axis_scores.tsv", sep="\t", index=False)

    validation = compare_pred_real(pred_scores, real_scores)
    validation.to_csv(OUT / "state_parse_cd14_prediction_validation.tsv", sep="\t", index=False)

    target_validation = per_target_validation(pred, real)
    target_validation.to_csv(OUT / "state_parse_cd14_per_target_validation.tsv", sep="\t", index=False)
    target_validation[target_validation["is_perturbation_of_interest"]].to_csv(
        OUT / "state_parse_cd14_focused_per_target_validation.tsv", sep="\t", index=False
    )

    focused = focused_table(scores)
    focused.to_csv(OUT / "state_parse_cd14_focused_perturbations.tsv", sep="\t", index=False)

    if int(scores["n_genes"].fillna(0).sum()) == 0:
        target_rank = pd.DataFrame(
            columns=[
                "target",
                "real_lysosomal_antigen_processing",
                "pred_lysosomal_antigen_processing",
                "real_interferon_apc",
                "pred_interferon_apc",
                "real_metabolic_hif_nampt",
                "pred_metabolic_hif_nampt",
                "real_inflammatory_cytokine",
                "pred_inflammatory_cytokine",
                "real_transition_score",
                "pred_transition_score",
            ]
        )
    else:
        real_wide = real_scores.pivot(index="target", columns="axis", values="mean_percent_change")
        pred_wide = pred_scores.pivot(index="target", columns="axis", values="mean_percent_change")
        ranked = []
        for target in sorted(set(real_wide.index) & set(pred_wide.index)):
            ranked.append(
                {
                    "target": target,
                    "real_lysosomal_antigen_processing": real_wide.loc[target].get("lysosomal_antigen_processing", np.nan),
                    "pred_lysosomal_antigen_processing": pred_wide.loc[target].get("lysosomal_antigen_processing", np.nan),
                    "real_interferon_apc": real_wide.loc[target].get("interferon_apc", np.nan),
                    "pred_interferon_apc": pred_wide.loc[target].get("interferon_apc", np.nan),
                    "real_metabolic_hif_nampt": real_wide.loc[target].get("metabolic_hif_nampt", np.nan),
                    "pred_metabolic_hif_nampt": pred_wide.loc[target].get("metabolic_hif_nampt", np.nan),
                    "real_inflammatory_cytokine": real_wide.loc[target].get("inflammatory_cytokine", np.nan),
                    "pred_inflammatory_cytokine": pred_wide.loc[target].get("inflammatory_cytokine", np.nan),
                }
            )
        target_rank = pd.DataFrame(ranked)
        target_rank["real_transition_score"] = (
            target_rank["real_lysosomal_antigen_processing"].fillna(0)
            + target_rank["real_interferon_apc"].fillna(0)
            + target_rank["real_metabolic_hif_nampt"].fillna(0)
        )
        target_rank["pred_transition_score"] = (
            target_rank["pred_lysosomal_antigen_processing"].fillna(0)
            + target_rank["pred_interferon_apc"].fillna(0)
            + target_rank["pred_metabolic_hif_nampt"].fillna(0)
        )
        target_rank = target_rank.sort_values("real_transition_score", ascending=False)
    target_rank.to_csv(OUT / "state_parse_cd14_transition_target_rank.tsv", sep="\t", index=False)

    summary = {
        "model_repo": MODEL_REPO,
        "model_sha": MODEL_SHA,
        "source_split": SOURCE_SPLIT,
        "cell_type": CELL_TYPE,
        "n_perturbations": int(pred["target"].nunique()),
        "n_output_features": int(pred["feature"].nunique()),
        "n_mapped_features": int(
            sum(not str(gene).startswith("FEATURE_") for gene in pred.drop_duplicates("feature")["gene"])
        ),
        "gene_mapping_status": gene_mapping_status,
        "top_real_transition_targets": target_rank.head(10)["target"].tolist(),
        "module_scoring_status": "blocked_no_gene_symbols_for_feature_ids" if target_rank.empty else "completed",
        "feature_agnostic_per_target_validation": {
            "median_spearman": float(target_validation["spearman_percent_change"].median()),
            "median_direction_match_fraction": float(target_validation["direction_match_fraction"].median()),
            "focused_perturbations": target_validation[target_validation["is_perturbation_of_interest"]][
                [
                    "target",
                    "spearman_percent_change",
                    "pearson_percent_change",
                    "direction_match_fraction",
                    "sig_feature_recall",
                    "sig_feature_precision",
                    "mean_abs_real_percent_change",
                ]
            ].to_dict(orient="records"),
        },
        "axis_validation": validation.to_dict(orient="records"),
        "interpretation": (
            "Released State CD14 monocyte predictions and matched real perturbation data; "
            "used to validate model-level perturbation ranking only where feature identity is not needed; gene-module scoring is blocked until HVG order is recovered."
        ),
    }
    (OUT / "state_parse_cd14_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print("\nTop transition targets:")
    if target_rank.empty:
        print("blocked: exact HVG feature-to-gene mapping unavailable without large AnnData downloads")
    else:
        print(target_rank.head(20).to_string(index=False))
    print("\nValidation:")
    print(validation.to_string(index=False))
    print("\nFeature-agnostic per-target validation for perturbations of interest:")
    print(
        target_validation[target_validation["is_perturbation_of_interest"]]
        .head(30)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
