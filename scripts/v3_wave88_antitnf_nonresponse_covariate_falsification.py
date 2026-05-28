#!/usr/bin/env python3
"""Wave88 falsification of the inflammatory anti-TNF nonresponse circuit.

This is a hostile follow-up to Wave86/87. The question is whether the
IL1B/TREM1/CXCL8/OSM signal adds information beyond tissue damage and
cell-composition proxies in leave-source-out validation.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import LeaveOneOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from v3_analyze_direct_h5ad_cell_states import ROOT
from v3_wave85_external_geo_antitnf_validation import (
    GPL570_ANNOT,
    SERIES_FILES,
    CohortSpec,
    bh,
    cohort_specs,
    expression_to_gene_level,
    hedges_g,
    markdown_table,
    mask_for_spec,
    read_gpl570_gene_map,
    read_series_matrix,
    rel,
    residualize,
    sample_metadata,
    write_json,
    zscore_rows,
)


SEED = 20260527
OUT = ROOT / "results_v3" / "wave88_antitnf_nonresponse_covariate_falsification"

PRIMARY_COHORTS = {
    "GSE12251_UC_ACT1_baseline",
    "GSE14580_UC_Leuven_baseline",
    "GSE16879_Crohn_colitis_Leuven_baseline",
    "GSE16879_Crohn_ileitis_Leuven_baseline",
}

PANELS: dict[str, list[str]] = {
    "circuit_il1b_trem1_cxcl8_osm": ["IL1B", "TREM1", "CXCL8", "OSM"],
    "wave86_il1b_lamp3_cross_system": ["IL1B", "LAMP3"],
    "neutrophil_granulocyte_proxy": ["S100A8", "S100A9", "MPO", "FCGR3B", "CXCR2", "CSF3R", "NAMPT"],
    "stromal_ulceration_proxy": ["COL1A1", "COL1A2", "COL3A1", "PDPN", "VIM", "MMP3", "MMP7", "FN1"],
    "epithelial_marker_mean": ["EPCAM", "KRT8", "KRT18", "KRT19", "VIL1", "MUC2", "TFF3", "CDH1"],
    "generic_inflammatory_proxy": ["TNF", "NFKBIA", "IL6", "CXCL1", "CXCL2", "CXCL3", "PTGS2"],
    "ifn_apc_proxy": ["STAT1", "CXCL10", "GBP1", "IFI30", "IRF1", "HLA-DRA", "CD74"],
    "housekeeping_negative_control": ["ACTB", "GAPDH", "RPLP0", "B2M", "HPRT1"],
}

INDIVIDUAL_GENES = [
    "IL1B",
    "TREM1",
    "CXCL8",
    "OSM",
    "LAMP3",
    "STAT1",
    "CCL2",
    "ACSL1",
    "IFI30",
    "SPP1",
]

BASELINE_PROXY_FEATURES = [
    "score_neutrophil_granulocyte_proxy",
    "score_stromal_ulceration_proxy",
    "score_epithelial_depletion_proxy",
    "score_generic_inflammatory_proxy",
    "score_ifn_apc_proxy",
]

TEST_FEATURES = {
    "circuit_il1b_trem1_cxcl8_osm": ["score_circuit_il1b_trem1_cxcl8_osm"],
    "il1b_lamp3_cross_system": ["score_wave86_il1b_lamp3_cross_system"],
    "IL1B": ["gene_IL1B"],
    "LAMP3": ["gene_LAMP3"],
    "TREM1": ["gene_TREM1"],
    "CXCL8": ["gene_CXCL8"],
    "OSM": ["gene_OSM"],
}


def auc(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    if len(np.unique(y)) < 2:
        return float("nan")
    return float(roc_auc_score(y, score))


def safe_average_precision(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    if len(np.unique(y)) < 2:
        return float("nan")
    return float(average_precision_score(y, score))


def fit_predict(train: pd.DataFrame, test: pd.DataFrame, features: list[str], categorical: bool = False) -> np.ndarray:
    train_x = train[features].copy()
    test_x = test[features].copy()
    if categorical:
        train_cat = pd.get_dummies(train[["disease", "tissue"]].fillna("missing").astype(str), drop_first=False)
        test_cat = pd.get_dummies(test[["disease", "tissue"]].fillna("missing").astype(str), drop_first=False)
        test_cat = test_cat.reindex(columns=train_cat.columns, fill_value=0)
        train_x = pd.concat([train_x.reset_index(drop=True), train_cat.reset_index(drop=True)], axis=1)
        test_x = pd.concat([test_x.reset_index(drop=True), test_cat.reset_index(drop=True)], axis=1)
    y = train["nonresponse"].astype(int).to_numpy()
    if len(np.unique(y)) < 2:
        return np.full(len(test), np.nan)
    model = make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler(),
        LogisticRegression(max_iter=2000, C=0.5, class_weight="balanced", solver="lbfgs", random_state=SEED),
    )
    model.fit(train_x.to_numpy(float), y)
    return model.predict_proba(test_x.to_numpy(float))[:, 1]


def loocv_predictions(df: pd.DataFrame, features: list[str]) -> np.ndarray:
    pred = np.full(len(df), np.nan)
    splitter = LeaveOneOut()
    for train_idx, test_idx in splitter.split(df):
        train = df.iloc[train_idx].copy()
        test = df.iloc[test_idx].copy()
        pred[test_idx] = fit_predict(train, test, features, categorical=False)
    return pred


def leave_group_out_predictions(df: pd.DataFrame, features: list[str], group_col: str) -> pd.DataFrame:
    rows = []
    all_pred = np.full(len(df), np.nan)
    for group, test_idx in df.groupby(group_col).groups.items():
        test_idx = list(test_idx)
        train_idx = [idx for idx in df.index if idx not in set(test_idx)]
        train = df.loc[train_idx].copy()
        test = df.loc[test_idx].copy()
        pred = fit_predict(train, test, features, categorical=True)
        all_pred[[df.index.get_loc(idx) for idx in test_idx]] = pred
        y = test["nonresponse"].astype(int).to_numpy()
        rows.append(
            {
                group_col: group,
                "n_test": int(len(test)),
                "n_nonresponders": int(y.sum()),
                "auc": auc(y, pred),
                "average_precision": safe_average_precision(y, pred),
                "brier": float(brier_score_loss(y, pred)) if np.isfinite(pred).all() and len(np.unique(y)) > 1 else np.nan,
            }
        )
    out = pd.DataFrame(rows)
    full_y = df["nonresponse"].astype(int).to_numpy()
    out.attrs["full_auc"] = auc(full_y, all_pred)
    out.attrs["full_average_precision"] = safe_average_precision(full_y, all_pred)
    out.attrs["full_brier"] = float(brier_score_loss(full_y, all_pred)) if np.isfinite(all_pred).all() and len(np.unique(full_y)) > 1 else np.nan
    return out


def panel_score(z: pd.DataFrame, genes: list[str]) -> tuple[pd.Series, list[str]]:
    present = [gene for gene in genes if gene in z.index]
    if not present:
        return pd.Series(np.nan, index=z.columns), []
    return z.loc[present].mean(axis=0, skipna=True), present


def cohort_source_label(cohort: str) -> str:
    if cohort == "GSE12251_UC_ACT1_baseline":
        return "ACT1_GSE12251_UC"
    if cohort == "GSE14580_UC_Leuven_baseline":
        return "Leuven_GSE14580_UC"
    if cohort == "GSE16879_Crohn_colitis_Leuven_baseline":
        return "Leuven_GSE16879_Crohn_colitis"
    if cohort == "GSE16879_Crohn_ileitis_Leuven_baseline":
        return "Leuven_GSE16879_Crohn_ileitis"
    return cohort


def publication_label(cohort: str) -> str:
    if cohort in {"GSE12251_UC_ACT1_baseline", "GSE14580_UC_Leuven_baseline"}:
        return "PMID19700435_UC_programs"
    if cohort.startswith("GSE16879"):
        return "PMID19956723_Leuven_GSE16879"
    return cohort


def build_patient_table() -> tuple[pd.DataFrame, pd.DataFrame]:
    wanted = sorted({gene for genes in PANELS.values() for gene in genes} | set(INDIVIDUAL_GENES))
    probe_to_genes, probe_map = read_gpl570_gene_map(GPL570_ANNOT, set(wanted))
    patient_rows: list[pd.DataFrame] = []
    coverage_rows: list[dict[str, Any]] = []

    for series, path in SERIES_FILES.items():
        metadata, expr_probe = read_series_matrix(path)
        info = sample_metadata(series, metadata)
        gene_expr = expression_to_gene_level(expr_probe, probe_to_genes)

        for spec in cohort_specs(series, info):
            if spec.cohort not in PRIMARY_COHORTS:
                continue
            mask = mask_for_spec(info, spec)
            selected = info.loc[mask].copy()
            samples = [sample for sample in selected["sample"] if sample in gene_expr.columns]
            if len(samples) < 6:
                continue
            z = zscore_rows(gene_expr[samples])
            score_df = pd.DataFrame(index=samples)
            for panel, genes in PANELS.items():
                score, present = panel_score(z, genes)
                name = f"score_{panel}"
                score_df[name] = score.reindex(samples).to_numpy(float)
                coverage_rows.append(
                    {
                        "cohort": spec.cohort,
                        "feature": name,
                        "n_defined": len(genes),
                        "n_present": len(present),
                        "genes_present": ";".join(present),
                        "genes_missing": ";".join([gene for gene in genes if gene not in present]),
                    }
                )
            score_df["score_epithelial_depletion_proxy"] = -score_df["score_epithelial_marker_mean"]
            for gene in INDIVIDUAL_GENES:
                score_df[f"gene_{gene}"] = z.loc[gene].reindex(samples).to_numpy(float) if gene in z.index else np.nan

            tmp = selected.merge(score_df.reset_index().rename(columns={"index": "sample"}), on="sample", how="inner")
            numeric_cols = [col for col in tmp.columns if col.startswith("score_") or col.startswith("gene_")]
            agg_numeric = tmp.groupby("patient_id", as_index=False)[numeric_cols].mean(numeric_only=True)
            first = tmp.groupby("patient_id", as_index=False)[["series", "disease", "tissue", "response", "response_label", "title"]].first()
            patients = first.merge(agg_numeric, on="patient_id", how="left")
            patients["cohort"] = spec.cohort
            patients["source_group"] = cohort_source_label(spec.cohort)
            patients["publication_group"] = publication_label(spec.cohort)
            patients["nonresponse"] = 1 - patients["response"].astype(int)
            patients["n_samples_aggregated"] = tmp.groupby("patient_id")["sample"].size().reindex(patients["patient_id"]).fillna(1).to_numpy(int)
            patient_rows.append(patients)

    table = pd.concat(patient_rows, ignore_index=True) if patient_rows else pd.DataFrame()
    return table, pd.DataFrame(coverage_rows).drop_duplicates()


def model_metrics(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rows = []
    heldout_rows = []
    pred_rows = []
    for test_name, add_features in TEST_FEATURES.items():
        for model_name, features in [
            ("proxy_baseline", BASELINE_PROXY_FEATURES),
            (f"proxy_plus_{test_name}", BASELINE_PROXY_FEATURES + add_features),
        ]:
            preds = leave_group_out_predictions(df, features, "source_group")
            full_auc = preds.attrs["full_auc"]
            rows.append(
                {
                    "test_feature": test_name,
                    "model_name": model_name,
                    "features": ";".join(features),
                    "validation": "leave_source_group_out",
                    "n": int(len(df)),
                    "n_nonresponders": int(df["nonresponse"].sum()),
                    "auc": full_auc,
                    "average_precision": preds.attrs["full_average_precision"],
                    "brier": preds.attrs["full_brier"],
                }
            )
            tmp = preds.copy()
            tmp["test_feature"] = test_name
            tmp["model_name"] = model_name
            heldout_rows.append(tmp)

        for cohort, sub in df.groupby("cohort"):
            if sub["nonresponse"].nunique() < 2 or len(sub) < 10:
                continue
            for model_name, features in [
                ("proxy_baseline", BASELINE_PROXY_FEATURES),
                (f"proxy_plus_{test_name}", BASELINE_PROXY_FEATURES + add_features),
            ]:
                pred = loocv_predictions(sub.reset_index(drop=True), features)
                y = sub["nonresponse"].astype(int).to_numpy()
                pred_rows.append(
                    {
                        "test_feature": test_name,
                        "cohort": cohort,
                        "model_name": model_name,
                        "validation": "within_cohort_loocv",
                        "n": int(len(sub)),
                        "n_nonresponders": int(y.sum()),
                        "auc": auc(y, pred),
                        "average_precision": safe_average_precision(y, pred),
                        "brier": float(brier_score_loss(y, pred)) if np.isfinite(pred).all() and len(np.unique(y)) > 1 else np.nan,
                    }
                )

    metrics = pd.DataFrame(rows)
    deltas = []
    for test_name, sub in metrics.groupby("test_feature"):
        base = sub[sub["model_name"] == "proxy_baseline"].iloc[0]
        aug = sub[sub["model_name"] == f"proxy_plus_{test_name}"].iloc[0]
        deltas.append(
            {
                "test_feature": test_name,
                "validation": "leave_source_group_out",
                "baseline_auc": base["auc"],
                "augmented_auc": aug["auc"],
                "delta_auc": aug["auc"] - base["auc"],
                "baseline_ap": base["average_precision"],
                "augmented_ap": aug["average_precision"],
                "delta_ap": aug["average_precision"] - base["average_precision"],
                "baseline_brier": base["brier"],
                "augmented_brier": aug["brier"],
                "delta_brier": aug["brier"] - base["brier"],
            }
        )

    heldout = pd.concat(heldout_rows, ignore_index=True) if heldout_rows else pd.DataFrame()
    within = pd.DataFrame(pred_rows)
    return metrics, heldout, within.merge(
        pd.DataFrame(deltas)[["test_feature", "baseline_auc", "augmented_auc", "delta_auc"]],
        on="test_feature",
        how="left",
        suffixes=("", "_overall"),
    ) if not within.empty else within


def effect_tests(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    features = [item for sublist in TEST_FEATURES.values() for item in sublist]
    features = sorted(set(features))
    for feature in features:
        base = df[np.isfinite(df[feature])].copy()
        if base.empty or base["nonresponse"].nunique() < 2:
            continue
        raw_non = base.loc[base["nonresponse"] == 1, feature].to_numpy(float)
        raw_resp = base.loc[base["nonresponse"] == 0, feature].to_numpy(float)
        raw_effect = float(np.nanmean(raw_non) - np.nanmean(raw_resp))
        raw_g = hedges_g(raw_non, raw_resp)

        resid = residualize(base[feature].to_numpy(float), base, BASELINE_PROXY_FEATURES + ["disease", "tissue"])
        base["_resid"] = resid
        res_non = base.loc[base["nonresponse"] == 1, "_resid"].to_numpy(float)
        res_resp = base.loc[base["nonresponse"] == 0, "_resid"].to_numpy(float)
        res_effect = float(np.nanmean(res_non) - np.nanmean(res_resp))
        res_g = hedges_g(res_non, res_resp)
        p_raw = stats.ttest_ind(raw_non, raw_resp, equal_var=False, nan_policy="omit").pvalue if len(raw_non) >= 3 and len(raw_resp) >= 3 else np.nan
        p_res = stats.ttest_ind(res_non, res_resp, equal_var=False, nan_policy="omit").pvalue if len(res_non) >= 3 and len(res_resp) >= 3 else np.nan
        rows.append(
            {
                "feature": feature,
                "scope": "pooled_primary_contexts",
                "n": int(len(base)),
                "raw_effect_nonresponse_minus_response": raw_effect,
                "raw_hedges_g_nonresponse_minus_response": raw_g,
                "raw_p": float(p_raw) if np.isfinite(p_raw) else np.nan,
                "residual_effect_after_proxies": res_effect,
                "residual_hedges_g_after_proxies": res_g,
                "residual_p_after_proxies": float(p_res) if np.isfinite(p_res) else np.nan,
                "abs_residual_to_raw_g_ratio": abs(res_g) / abs(raw_g) if np.isfinite(raw_g) and abs(raw_g) > 1e-9 and np.isfinite(res_g) else np.nan,
            }
        )
        for cohort, sub in base.groupby("cohort"):
            non = sub.loc[sub["nonresponse"] == 1, feature].to_numpy(float)
            resp = sub.loc[sub["nonresponse"] == 0, feature].to_numpy(float)
            if len(non) < 3 or len(resp) < 3:
                continue
            rows.append(
                {
                    "feature": feature,
                    "scope": cohort,
                    "n": int(len(sub)),
                    "raw_effect_nonresponse_minus_response": float(np.nanmean(non) - np.nanmean(resp)),
                    "raw_hedges_g_nonresponse_minus_response": hedges_g(non, resp),
                    "raw_p": float(stats.ttest_ind(non, resp, equal_var=False, nan_policy="omit").pvalue),
                    "residual_effect_after_proxies": np.nan,
                    "residual_hedges_g_after_proxies": np.nan,
                    "residual_p_after_proxies": np.nan,
                    "abs_residual_to_raw_g_ratio": np.nan,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["raw_fdr"] = bh(out["raw_p"].fillna(1.0))
        out["residual_fdr"] = bh(out["residual_p_after_proxies"].fillna(1.0))
    return out


def permutation_added_auc(df: pd.DataFrame, test_feature: str, n_perm: int = 199) -> dict[str, Any]:
    rng = np.random.default_rng(SEED + abs(hash(test_feature)) % 10000)
    add_features = TEST_FEATURES[test_feature]
    base_metrics, _, _ = model_metrics(df)
    delta_row = []
    m = base_metrics[base_metrics["test_feature"] == test_feature]
    base = float(m[m["model_name"] == "proxy_baseline"]["auc"].iloc[0])
    aug = float(m[m["model_name"] == f"proxy_plus_{test_feature}"]["auc"].iloc[0])
    observed = aug - base
    perms = []
    for _ in range(n_perm):
        perm = df.copy()
        for _, idx in perm.groupby("source_group").groups.items():
            values = perm.loc[list(idx), "nonresponse"].to_numpy()
            rng.shuffle(values)
            perm.loc[list(idx), "nonresponse"] = values
        preds_base = leave_group_out_predictions(perm, BASELINE_PROXY_FEATURES, "source_group").attrs["full_auc"]
        preds_aug = leave_group_out_predictions(perm, BASELINE_PROXY_FEATURES + add_features, "source_group").attrs["full_auc"]
        perms.append(preds_aug - preds_base)
    p = (1 + sum(value >= observed for value in perms)) / (1 + len(perms))
    return {
        "test_feature": test_feature,
        "observed_delta_auc": observed,
        "n_perm": n_perm,
        "perm_mean_delta_auc": float(np.nanmean(perms)),
        "perm_sd_delta_auc": float(np.nanstd(perms, ddof=1)),
        "perm_p_delta_auc_ge_observed": float(p),
    }


def classify(deltas: pd.DataFrame, effects: pd.DataFrame) -> tuple[str, str]:
    primary = deltas[deltas["test_feature"] == "circuit_il1b_trem1_cxcl8_osm"].iloc[0]
    primary_effect = effects[
        (effects["feature"] == "score_circuit_il1b_trem1_cxcl8_osm") & (effects["scope"] == "pooled_primary_contexts")
    ].iloc[0]
    if primary["delta_auc"] <= 0.05:
        return "FALSIFY_CIRCUIT_ADDED_VALUE", "added AUC beyond proxy baseline is <=0.05"
    if abs(primary_effect["residual_hedges_g_after_proxies"]) < 0.3:
        return "FALSIFY_CIRCUIT_AS_INDEPENDENT_SIGNAL", "proxy-adjusted pooled effect size is below 0.3"
    if primary_effect["abs_residual_to_raw_g_ratio"] < 0.3:
        return "FALSIFY_CIRCUIT_AS_PROXY_ABSORBED", "cell-composition/severity proxies absorb more than 70 percent of raw effect size"
    return "PARK_CIRCUIT_SURVIVES_PARTIAL_PROXY_TEST", "signal survives proxy adjustment but still needs cell-resolved treatment-specificity validation"


def run() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    patients, coverage = build_patient_table()
    patients.to_csv(OUT / "primary_context_patient_scores.tsv", sep="\t", index=False)
    coverage.to_csv(OUT / "feature_gene_coverage.tsv", sep="\t", index=False)

    metrics, heldout, within = model_metrics(patients)
    deltas = []
    for test_feature, sub in metrics.groupby("test_feature"):
        base = sub[sub["model_name"] == "proxy_baseline"].iloc[0]
        aug = sub[sub["model_name"] == f"proxy_plus_{test_feature}"].iloc[0]
        deltas.append(
            {
                "test_feature": test_feature,
                "baseline_auc": base["auc"],
                "augmented_auc": aug["auc"],
                "delta_auc": aug["auc"] - base["auc"],
                "baseline_average_precision": base["average_precision"],
                "augmented_average_precision": aug["average_precision"],
                "delta_average_precision": aug["average_precision"] - base["average_precision"],
                "baseline_brier": base["brier"],
                "augmented_brier": aug["brier"],
                "delta_brier": aug["brier"] - base["brier"],
            }
        )
    deltas_df = pd.DataFrame(deltas).sort_values("delta_auc", ascending=False)
    effects = effect_tests(patients)
    perm = pd.DataFrame([permutation_added_auc(patients, "circuit_il1b_trem1_cxcl8_osm", n_perm=199)])
    call, reason = classify(deltas_df, effects)

    metrics.to_csv(OUT / "leave_source_model_metrics.tsv", sep="\t", index=False)
    heldout.to_csv(OUT / "heldout_source_metrics.tsv", sep="\t", index=False)
    within.to_csv(OUT / "within_cohort_loocv_metrics.tsv", sep="\t", index=False)
    deltas_df.to_csv(OUT / "added_value_summary.tsv", sep="\t", index=False)
    effects.to_csv(OUT / "effect_proxy_adjustment_tests.tsv", sep="\t", index=False)
    perm.to_csv(OUT / "permutation_added_auc.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "call": call,
        "call_reason": reason,
        "n_patients": int(len(patients)),
        "n_nonresponders": int(patients["nonresponse"].sum()),
        "n_source_groups": int(patients["source_group"].nunique()),
        "primary_circuit_delta_auc": float(deltas_df[deltas_df["test_feature"] == "circuit_il1b_trem1_cxcl8_osm"]["delta_auc"].iloc[0]),
        "primary_circuit_permutation_p": float(perm["perm_p_delta_auc_ge_observed"].iloc[0]),
        "inputs": {
            "series_files": {series: rel(path) for series, path in SERIES_FILES.items()},
            "gpl570_annotation": rel(GPL570_ANNOT),
        },
    }
    write_json(OUT / "summary.json", summary)

    primary_effect = effects[
        (effects["feature"] == "score_circuit_il1b_trem1_cxcl8_osm") & (effects["scope"] == "pooled_primary_contexts")
    ].copy()
    report = [
        "# Wave88 Anti-TNF Nonresponse Covariate Falsification",
        "",
        "Question: does the Wave86 `IL1B/TREM1/CXCL8/OSM` inflammatory nonresponse circuit add response information beyond neutrophil, stromal/ulceration, epithelial depletion, generic inflammation, and IFN/APC proxies under leave-source-out validation?",
        "",
        f"Decision: `{call}`.",
        "",
        f"Reason: {reason}.",
        "",
        "## Added Predictive Value",
        "",
        markdown_table(deltas_df, max_rows=20),
        "",
        "## Primary Circuit Proxy-Adjustment Effect",
        "",
        markdown_table(primary_effect, max_rows=10),
        "",
        "## Held-Out Source Metrics",
        "",
        markdown_table(heldout[heldout["test_feature"].eq("circuit_il1b_trem1_cxcl8_osm")].sort_values(["source_group", "model_name"]), max_rows=20),
        "",
        "## Permutation",
        "",
        markdown_table(perm, max_rows=10),
        "",
        "## Guardrail",
        "",
        "This remains bulk mucosal treatment-response modeling. A surviving proxy-adjusted association would still be a biomarker/pathotype hypothesis, not a causal circuit or intervention point.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    run()


if __name__ == "__main__":
    main()
