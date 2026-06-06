#!/usr/bin/env python3
"""Focused LGALS3/glycan-checkpoint analysis across local autoimmune h5ads.

Wave 7 nominated LGALS3 as the next computational test, not as a final target.
This script is designed to falsify that handoff quickly. It asks whether
LGALS3 and a galectin/phagolysosomal checkpoint program reproduce across local
autoimmune tissues after controlling for generic IFN/APC, lysosomal, lipid
loader, OSM/complement, and injury/stromal programs.

This is still observational donor-level pseudobulk, not causal evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

import v3_analyze_osmr_complement_axes as base

SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "lgals3_glycan_checkpoint"

TARGET_MODULES = {
    "lgals3_core": ["LGALS3"],
    "galectin_checkpoint": ["LGALS3", "LGALS1", "LGALS9", "LGALS3BP"],
    "foamy_phagolysosomal_checkpoint": [
        "LGALS3",
        "GPNMB",
        "APOE",
        "CTSD",
        "CTSL",
        "CTSB",
        "LAMP1",
        "LAMP2",
        "TREM2",
        "TYROBP",
        "MERTK",
        "LRP1",
    ],
    "repair_efferocytosis_control": ["GPNMB", "TREM2", "MERTK", "LRP1", "APOE", "CTSD", "CTSL"],
}

COVARIATE_MODULES = {
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "CD74", "IFI30", "HLA-DRA", "HLA-DRB1"],
    "hla_ii_apc": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "CIITA", "RFX5"],
    "lysosomal_apc": ["IFI30", "CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"],
    "lipid_loader_repair": [
        "ACSL1",
        "APOE",
        "GPNMB",
        "LPL",
        "PLIN2",
        "CD36",
        "LIPA",
        "FABP5",
        "TREM2",
        "MSR1",
        "MERTK",
        "SPP1",
    ],
    "hif_nampt_metabolic": ["HIF1A", "NAMPT", "LDHA", "SLC2A1", "NFKBIA", "IL1B", "HK2", "PFKFB3"],
    "inflammatory_nfkb": ["IL1B", "TNF", "CXCL8", "CCL2", "CCL3", "CCL4", "NFKBIA", "TREM1", "OSM"],
    "osmr_tissue_response": ["OSMR", "IL6ST", "STAT3", "SOCS3", "JUNB", "FOS", "C3", "SERPINE1"],
    "c1q_phagocytic_myeloid": ["C1QA", "C1QB", "C1QC", "TYROBP", "TREM2", "APOE", "GPNMB", "LPL", "CD68", "MERTK", "MSR1", "LRP1"],
    "tissue_injury_remodeling": ["CHI3L1", "TIMP1", "MMP7", "MMP9", "SPP1", "CD44", "FN1", "COL1A1", "COL1A2"],
}

MODULES = {**TARGET_MODULES, **COVARIATE_MODULES}
GENES_OF_INTEREST = [
    "LGALS3",
    "LGALS1",
    "LGALS9",
    "LGALS3BP",
    "GPNMB",
    "CTSD",
    "CTSL",
    "CTSB",
    "TREM2",
    "TYROBP",
    "MERTK",
    "LRP1",
    "FABP5",
    "MSR1",
    "SCARB2",
    "CD44",
    "SPP1",
]


def configure_base() -> None:
    base.OUT = OUT
    base.TARGET_MODULES = TARGET_MODULES
    base.COVARIATE_MODULES = COVARIATE_MODULES
    base.MODULES = MODULES
    base.TARGET_GENES = sorted({gene for genes in MODULES.values() for gene in genes} | set(GENES_OF_INTEREST))


def residual_tests(module_scores: pd.DataFrame, gene_scores: pd.DataFrame) -> pd.DataFrame:
    module_wide = module_scores.pivot_table(
        index=["analysis", "donor_id"],
        columns="module",
        values="mean_score",
        aggfunc="mean",
    ).reset_index()
    sample_meta = module_scores.drop_duplicates(["analysis", "donor_id"])[
        ["analysis", "donor_id", "disease_name", "compartment", "role", "group"]
    ]
    module_wide = sample_meta.merge(module_wide, on=["analysis", "donor_id"], how="left")

    rows: list[dict[str, object]] = []
    for target in TARGET_MODULES:
        for (analysis, compartment), sub in module_wide.groupby(["analysis", "compartment"], observed=True):
            if target not in sub.columns:
                continue
            raw = base.compare_values(sub[target], sub["group"])
            for covariate in COVARIATE_MODULES:
                if covariate not in sub.columns:
                    continue
                residuals, slope, r2 = base.residualize(sub[target].to_numpy(float), sub[covariate].to_numpy(float))
                residual = base.compare_values(pd.Series(residuals, index=sub.index), sub["group"])
                first = sub.iloc[0]
                rows.append(
                    {
                        "feature_type": "module",
                        "feature": target,
                        "analysis": analysis,
                        "disease_name": first["disease_name"],
                        "compartment": compartment,
                        "role": first["role"],
                        "covariate_module": covariate,
                        "covariate_slope": slope,
                        "covariate_r2": r2,
                        **{f"raw_{k}": v for k, v in raw.items()},
                        **{f"residual_{k}": v for k, v in residual.items()},
                    }
                )

    covariates = module_wide[
        ["analysis", "donor_id", *[c for c in COVARIATE_MODULES if c in module_wide.columns]]
    ]
    gene_aug = gene_scores.loc[gene_scores["gene"].isin(GENES_OF_INTEREST)].merge(
        covariates, on=["analysis", "donor_id"], how="left"
    )
    for (analysis, gene), sub in gene_aug.groupby(["analysis", "gene"], observed=True):
        raw = base.compare_values(sub["mean_z_vs_controls"], sub["group"])
        for covariate in COVARIATE_MODULES:
            if covariate not in sub.columns:
                continue
            residuals, slope, r2 = base.residualize(
                sub["mean_z_vs_controls"].to_numpy(float),
                sub[covariate].to_numpy(float),
            )
            residual = base.compare_values(pd.Series(residuals, index=sub.index), sub["group"])
            first = sub.iloc[0]
            rows.append(
                {
                    "feature_type": "gene",
                    "feature": gene,
                    "analysis": analysis,
                    "disease_name": first["disease_name"],
                    "compartment": first["compartment"],
                    "role": first["role"],
                    "covariate_module": covariate,
                    "covariate_slope": slope,
                    "covariate_r2": r2,
                    **{f"raw_{k}": v for k, v in raw.items()},
                    **{f"residual_{k}": v for k, v in residual.items()},
                }
            )

    out = pd.DataFrame(rows)
    if not out.empty:
        out["residual_fdr"] = multipletests(out["residual_p"].fillna(1.0), method="fdr_bh")[1]
        out["retains_nominal_positive"] = (
            (out["raw_delta_case_minus_control"] > 0)
            & (out["raw_p"] < 0.05)
            & (out["residual_delta_case_minus_control"] > 0)
            & (out["residual_p"] < 0.05)
        )
    return out


def disease_summary(module_comparisons: pd.DataFrame, gene_comparisons: pd.DataFrame, residuals: pd.DataFrame) -> pd.DataFrame:
    module_mean = module_comparisons.loc[module_comparisons["metric"] == "mean_score"].copy()
    gene_mean = gene_comparisons.loc[gene_comparisons["metric"] == "mean_z_vs_controls"].copy()
    rows: list[dict[str, object]] = []
    for disease in sorted(set(module_mean["disease_name"]) | set(gene_mean["disease_name"])):
        dmods = module_mean.loc[module_mean["disease_name"] == disease]
        dgenes = gene_mean.loc[gene_mean["disease_name"] == disease]
        dres = residuals.loc[residuals["disease_name"] == disease] if not residuals.empty else pd.DataFrame()
        pos_modules = dmods.loc[
            dmods["module"].isin(TARGET_MODULES)
            & (dmods["delta_case_minus_control"] > 0)
            & (dmods["p"] < 0.05)
        ]
        neg_modules = dmods.loc[
            dmods["module"].isin(TARGET_MODULES)
            & (dmods["delta_case_minus_control"] < 0)
            & (dmods["p"] < 0.05)
        ]
        pos_genes = dgenes.loc[
            dgenes["gene"].isin(GENES_OF_INTEREST)
            & (dgenes["delta_case_minus_control"] > 0)
            & (dgenes["p"] < 0.05)
        ]
        neg_genes = dgenes.loc[
            dgenes["gene"].isin(GENES_OF_INTEREST)
            & (dgenes["delta_case_minus_control"] < 0)
            & (dgenes["p"] < 0.05)
        ]
        retained = dres.loc[dres["retains_nominal_positive"]] if not dres.empty else pd.DataFrame()
        rows.append(
            {
                "disease_name": disease,
                "n_positive_target_modules_nominal": int(len(pos_modules)),
                "positive_target_modules": ";".join(
                    pos_modules.sort_values("p")["analysis"].astype(str)
                    + ":"
                    + pos_modules.sort_values("p")["module"].astype(str)
                ),
                "n_negative_target_modules_nominal": int(len(neg_modules)),
                "negative_target_modules": ";".join(
                    neg_modules.sort_values("p")["analysis"].astype(str)
                    + ":"
                    + neg_modules.sort_values("p")["module"].astype(str)
                ),
                "n_positive_genes_nominal": int(len(pos_genes)),
                "positive_genes": ";".join(
                    pos_genes.sort_values("p")["analysis"].astype(str)
                    + ":"
                    + pos_genes.sort_values("p")["gene"].astype(str)
                ),
                "n_negative_genes_nominal": int(len(neg_genes)),
                "negative_genes": ";".join(
                    neg_genes.sort_values("p")["analysis"].astype(str)
                    + ":"
                    + neg_genes.sort_values("p")["gene"].astype(str)
                ),
                "n_residual_retained_nominal_tests": int(len(retained)),
                "residual_retained_features": ";".join(
                    retained.sort_values("residual_p")["analysis"].astype(str)
                    + ":"
                    + retained.sort_values("residual_p")["feature"].astype(str)
                    + "|"
                    + retained.sort_values("residual_p")["covariate_module"].astype(str)
                )
                if not retained.empty
                else "",
            }
        )
    return pd.DataFrame(rows)


def candidate_crosswalk(gene_comparisons: pd.DataFrame, residuals: pd.DataFrame) -> pd.DataFrame:
    broad_path = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
    existing_path = ROOT / "phases/v3/results" / "existing_evidence_candidate_matrix.tsv"
    geneformer_path = ROOT / "phases/v3/results" / "geneformer_candidate_delete" / "geneformer_candidate_delete_gene_summary.tsv"

    candidates = ["LGALS3", "LGALS1", "LGALS9", "LGALS3BP", "FABP5", "MSR1", "SCARB2", "GPNMB", "CD44", "SPP1"]
    broad = pd.read_csv(broad_path, sep="\t") if broad_path.exists() else pd.DataFrame()
    existing = pd.read_csv(existing_path, sep="\t") if existing_path.exists() else pd.DataFrame()
    geneformer = pd.read_csv(geneformer_path, sep="\t") if geneformer_path.exists() else pd.DataFrame()

    rows: list[dict[str, object]] = []
    gene_mean = gene_comparisons.loc[gene_comparisons["metric"] == "mean_z_vs_controls"].copy()
    for gene in candidates:
        direct = gene_mean.loc[gene_mean["gene"] == gene]
        pos_direct = direct.loc[(direct["delta_case_minus_control"] > 0) & (direct["p"] < 0.05)]
        neg_direct = direct.loc[(direct["delta_case_minus_control"] < 0) & (direct["p"] < 0.05)]
        retained = residuals.loc[
            (residuals["feature_type"] == "gene")
            & (residuals["feature"] == gene)
            & residuals["retains_nominal_positive"]
        ] if not residuals.empty else pd.DataFrame()
        brow = broad.loc[broad["gene"] == gene].head(1) if not broad.empty and "gene" in broad.columns else pd.DataFrame()
        erow = existing.loc[existing["gene"] == gene] if not existing.empty and "gene" in existing.columns else pd.DataFrame()
        gf = geneformer.loc[geneformer["gene"] == gene].head(1) if not geneformer.empty and "gene" in geneformer.columns else pd.DataFrame()
        rows.append(
            {
                "gene": gene,
                "direct_positive_disease_count": int(pos_direct["disease_name"].nunique()),
                "direct_positive_compartment_count": int(len(pos_direct)),
                "direct_positive_compartments": ";".join(
                    pos_direct.sort_values("p")["analysis"].astype(str)
                    + ":"
                    + pos_direct.sort_values("delta_case_minus_control", ascending=False)["delta_case_minus_control"].round(3).astype(str)
                ),
                "direct_negative_disease_count": int(neg_direct["disease_name"].nunique()),
                "direct_negative_compartment_count": int(len(neg_direct)),
                "direct_negative_compartments": ";".join(
                    neg_direct.sort_values("p")["analysis"].astype(str)
                    + ":"
                    + neg_direct.sort_values("delta_case_minus_control")["delta_case_minus_control"].round(3).astype(str)
                ),
                "residual_retained_positive_test_count": int(len(retained)),
                "residual_retained_disease_count": int(retained["disease_name"].nunique()) if not retained.empty else 0,
                "broad_positive_disease_count": int(brow.iloc[0]["positive_disease_count"]) if not brow.empty and pd.notna(brow.iloc[0].get("positive_disease_count")) else 0,
                "broad_negative_disease_count": int(brow.iloc[0]["negative_disease_count"]) if not brow.empty and pd.notna(brow.iloc[0].get("negative_disease_count")) else 0,
                "broad_ms_wm_delta_log2": float(brow.iloc[0]["ms_wm_delta_log2"]) if not brow.empty and pd.notna(brow.iloc[0].get("ms_wm_delta_log2")) else np.nan,
                "broad_ms_wm_p": float(brow.iloc[0]["ms_wm_p"]) if not brow.empty and pd.notna(brow.iloc[0].get("ms_wm_p")) else np.nan,
                "existing_positive_disease_count": int(erow.loc[erow["positive_nominal"], "disease"].nunique()) if not erow.empty and {"positive_nominal", "disease"}.issubset(erow.columns) else 0,
                "existing_negative_disease_count": int(erow.loc[erow["negative_nominal"], "disease"].nunique()) if not erow.empty and {"negative_nominal", "disease"}.issubset(erow.columns) else 0,
                "geneformer_support_contexts": int(gf.iloc[0]["support_contexts"]) if not gf.empty and pd.notna(gf.iloc[0].get("support_contexts")) else np.nan,
                "geneformer_mean_cosine_shift": float(gf.iloc[0]["mean_cosine_shift"]) if not gf.empty and pd.notna(gf.iloc[0].get("mean_cosine_shift")) else np.nan,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    np.random.seed(SEED)
    configure_base()
    OUT.mkdir(parents=True, exist_ok=True)

    cache: dict[Path, tuple] = {}
    module_tables: list[pd.DataFrame] = []
    gene_tables: list[pd.DataFrame] = []
    module_gene_tables: list[pd.DataFrame] = []
    run_log: list[dict[str, object]] = []

    for config in base.CONFIGS:
        try:
            if config.path not in cache:
                cache[config.path] = base.read_counts(config.path)
            a, x = cache[config.path]
            modules, genes, module_genes = base.analyze_config(config, a, x)
            module_tables.append(modules)
            gene_tables.append(genes)
            module_gene_tables.append(module_genes)
            run_log.append(
                {
                    "analysis": config.name,
                    "status": "completed",
                    "n_module_rows": int(len(modules)),
                    "n_gene_rows": int(len(genes)),
                    "path": str(config.path.relative_to(ROOT)),
                }
            )
        except Exception as exc:
            run_log.append({"analysis": config.name, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})

    module_scores = pd.concat(module_tables, ignore_index=True) if module_tables else pd.DataFrame()
    gene_scores = pd.concat(gene_tables, ignore_index=True) if gene_tables else pd.DataFrame()
    module_genes = pd.concat(module_gene_tables, ignore_index=True) if module_gene_tables else pd.DataFrame()
    module_comparisons = base.compare_modules(module_scores) if not module_scores.empty else pd.DataFrame()
    gene_comparisons = base.compare_genes(gene_scores) if not gene_scores.empty else pd.DataFrame()
    residual_table = residual_tests(module_scores, gene_scores) if not module_scores.empty and not gene_scores.empty else pd.DataFrame()
    disease = disease_summary(module_comparisons, gene_comparisons, residual_table)
    crosswalk = candidate_crosswalk(gene_comparisons, residual_table)

    module_scores.to_csv(OUT / "lgals3_donor_module_scores.tsv", sep="\t", index=False)
    gene_scores.to_csv(OUT / "lgals3_gene_scores.tsv", sep="\t", index=False)
    module_genes.to_csv(OUT / "lgals3_module_genes_present.tsv", sep="\t", index=False)
    module_comparisons.to_csv(OUT / "lgals3_module_comparisons.tsv", sep="\t", index=False)
    gene_comparisons.to_csv(OUT / "lgals3_gene_comparisons.tsv", sep="\t", index=False)
    residual_table.to_csv(OUT / "lgals3_residual_tests.tsv", sep="\t", index=False)
    disease.to_csv(OUT / "lgals3_disease_summary.tsv", sep="\t", index=False)
    crosswalk.to_csv(OUT / "lgals3_candidate_crosswalk.tsv", sep="\t", index=False)

    positive_target_modules = module_comparisons.loc[
        (module_comparisons["metric"] == "mean_score")
        & (module_comparisons["module"].isin(TARGET_MODULES))
        & (module_comparisons["delta_case_minus_control"] > 0)
    ].sort_values(["fdr", "p", "hedges_g"], ascending=[True, True, False])
    positive_genes = gene_comparisons.loc[
        (gene_comparisons["metric"] == "mean_z_vs_controls")
        & (gene_comparisons["gene"].isin(GENES_OF_INTEREST))
        & (gene_comparisons["delta_case_minus_control"] > 0)
    ].sort_values(["fdr", "p", "hedges_g"], ascending=[True, True, False])
    retained = (
        residual_table.loc[residual_table["retains_nominal_positive"]]
        .sort_values(["residual_fdr", "residual_p", "residual_hedges_g"], ascending=[True, True, False])
        if not residual_table.empty
        else pd.DataFrame()
    )

    summary = {
        "random_seed": SEED,
        "run_log": run_log,
        "n_module_comparisons": int(len(module_comparisons)),
        "n_gene_comparisons": int(len(gene_comparisons)),
        "n_residual_tests": int(len(residual_table)),
        "target_modules": TARGET_MODULES,
        "covariate_modules": COVARIATE_MODULES,
        "top_positive_target_modules": positive_target_modules.head(50).to_dict(orient="records"),
        "top_positive_genes": positive_genes.head(80).to_dict(orient="records"),
        "residual_retained_nominal_positive_tests": retained.head(120).to_dict(orient="records"),
        "disease_summary": disease.to_dict(orient="records"),
        "candidate_crosswalk": crosswalk.to_dict(orient="records"),
        "interpretation_guardrail": (
            "LGALS3 is promoted only if it shows MS support plus direct cross-disease replication and residualized "
            "signal beyond generic IFN/APC, lysosomal, lipid-loader, OSM/complement, and injury modules. "
            "This script is observational and cannot establish causality or repair-preserving safety."
        ),
    }
    (OUT / "lgals3_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
