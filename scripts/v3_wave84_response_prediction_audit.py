#!/usr/bin/env python3
"""Wave84 response-prediction audit.

Wave75/Wave76 showed a directionally stable baseline lysosomal/APC response
association across RA anti-TNF synovium and IBD anti-TNF DC pseudobulk, but it
was too generic-limited for a target claim. This wave reformulates the question
as stratification:

Does a frozen baseline lipid/lysosomal/APC module improve out-of-sample
response prediction over generic inflammation and available clinical/pathotype
covariates?

The script is deliberately conservative. It uses only pre-treatment features,
leave-one-out predictions, fixed random seeds, and permutation tests for the
primary added-AUC comparison.
"""

from __future__ import annotations

import json
import math
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, balanced_accuracy_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import LeaveOneOut
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from v3_analyze_direct_h5ad_cell_states import ROOT


warnings.filterwarnings(
    "ignore",
    message="'penalty' was deprecated.*",
    category=FutureWarning,
)

SEED = 20260527
N_PERM = 499
OUT = ROOT / "results_v3" / "wave84_response_prediction_audit"

RA_WIDE = ROOT / "results_v3" / "wave76_adjusted_response_specificity" / "ra_wide_patient_table.tsv"
IBD_WIDE = ROOT / "results_v3" / "wave76_adjusted_response_specificity" / "ibd_wide_patient_cellstate_table.tsv"
UC_DONOR = ROOT / "results_v3" / "gse253006_tofacitinib_marker" / "gse253006_marker_donor_module_scores.tsv"
W76_CONV = ROOT / "results_v3" / "wave76_adjusted_response_specificity" / "adjusted_cross_dataset_convergence.tsv"
W18_RA_TESTS = ROOT / "results_v3" / "wave18_treatment_response" / "wave18_gse138746_ra_baseline_response_tests.tsv"
W18_PSORIASIS = ROOT / "results_v3" / "wave18_treatment_response" / "wave18_gse183047_psoriasis_prepost_tests.tsv"

PRIMARY_MODULE = "lysosomal_apc__resid_inflammatory_nfkb"
SECONDARY_MODULES = [
    "lysosomal_apc",
    "ifn_lysosomal_apc_composite__resid_inflammatory_nfkb",
    "ifn_lysosomal_apc_composite",
    "ifn_apc__resid_inflammatory_nfkb",
    "ifn_apc",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value)


def markdown_table(df: pd.DataFrame, max_rows: int = 40) -> str:
    if df.empty:
        return "_No rows._"
    view = df.head(max_rows).copy()
    cols = list(view.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in view.iterrows():
        vals: list[str] = []
        for col in cols:
            value = row[col]
            if isinstance(value, float):
                vals.append("" if math.isnan(value) else f"{value:.4g}")
            else:
                vals.append(clean_text(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def existing_columns(df: pd.DataFrame, cols: list[str]) -> list[str]:
    return [col for col in cols if col in df.columns]


def make_pipeline(numeric: list[str], categorical: list[str]) -> Pipeline:
    transformers = []
    if numeric:
        transformers.append(
            (
                "num",
                Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]),
                numeric,
            )
        )
    if categorical:
        transformers.append(
            (
                "cat",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                    ]
                ),
                categorical,
            )
        )
    pre = ColumnTransformer(transformers=transformers, remainder="drop")
    clf = LogisticRegression(
        solver="liblinear",
        penalty="l2",
        C=1.0,
        class_weight="balanced",
        max_iter=1000,
        random_state=SEED,
    )
    return Pipeline([("pre", pre), ("logit", clf)])


def outcome_metrics(y: np.ndarray, prob: np.ndarray) -> dict[str, Any]:
    mask = np.isfinite(prob)
    y = y[mask].astype(int)
    prob = prob[mask].astype(float)
    if len(y) == 0 or len(np.unique(y)) < 2:
        return {
            "auc": np.nan,
            "average_precision": np.nan,
            "brier": np.nan,
            "balanced_accuracy_0_5": np.nan,
            "n": int(len(y)),
            "n_positive": int(y.sum()) if len(y) else 0,
            "n_negative": int((1 - y).sum()) if len(y) else 0,
        }
    pred = (prob >= 0.5).astype(int)
    return {
        "auc": float(roc_auc_score(y, prob)),
        "average_precision": float(average_precision_score(y, prob)),
        "brier": float(brier_score_loss(y, prob)),
        "balanced_accuracy_0_5": float(balanced_accuracy_score(y, pred)),
        "n": int(len(y)),
        "n_positive": int(y.sum()),
        "n_negative": int((1 - y).sum()),
    }


def loocv_probabilities(df: pd.DataFrame, outcome: str, numeric: list[str], categorical: list[str]) -> tuple[np.ndarray, str]:
    features = numeric + categorical
    data = df[features + [outcome]].copy()
    for col in numeric:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data = data.dropna(subset=[outcome]).reset_index(drop=True)
    y = data[outcome].astype(int).to_numpy()
    if data.shape[0] < 8 or len(np.unique(y)) < 2 or min(np.bincount(y)) < 2:
        return np.full(data.shape[0], np.nan), "insufficient_rows_or_classes"
    probs = np.full(data.shape[0], np.nan, dtype=float)
    loo = LeaveOneOut()
    for train_idx, test_idx in loo.split(data):
        y_train = y[train_idx]
        if len(np.unique(y_train)) < 2:
            continue
        model = make_pipeline(numeric, categorical)
        try:
            model.fit(data.iloc[train_idx][features], y_train)
            probs[test_idx[0]] = float(model.predict_proba(data.iloc[test_idx][features])[:, 1][0])
        except Exception:  # noqa: BLE001
            return probs, "fit_failed"
    return probs, "ok"


def full_model_target_coef(df: pd.DataFrame, outcome: str, numeric: list[str], categorical: list[str], target_feature: str) -> float:
    features = numeric + categorical
    data = df[features + [outcome]].dropna(subset=[outcome]).reset_index(drop=True)
    y = data[outcome].astype(int).to_numpy()
    if data.shape[0] < 8 or len(np.unique(y)) < 2 or target_feature not in numeric:
        return np.nan
    model = make_pipeline(numeric, categorical)
    try:
        model.fit(data[features], y)
        names = model.named_steps["pre"].get_feature_names_out()
        coefs = model.named_steps["logit"].coef_[0]
        target_name = f"num__{target_feature}"
        if target_name in names:
            return float(coefs[list(names).index(target_name)])
    except Exception:  # noqa: BLE001
        return np.nan
    return np.nan


def evaluate_model(
    *,
    df: pd.DataFrame,
    dataset: str,
    outcome: str,
    response_definition: str,
    model_name: str,
    numeric: list[str],
    categorical: list[str],
    target_feature: str = "",
) -> dict[str, Any]:
    probs, status = loocv_probabilities(df, outcome, numeric, categorical)
    y = df.dropna(subset=[outcome])[outcome].astype(int).to_numpy()
    metrics = outcome_metrics(y, probs)
    return {
        "dataset": dataset,
        "response_definition": response_definition,
        "model_name": model_name,
        "numeric_features": ";".join(numeric),
        "categorical_features": ";".join(categorical),
        "target_feature": target_feature,
        "fit_status": status,
        "full_model_target_coef": full_model_target_coef(df, outcome, numeric, categorical, target_feature),
        **metrics,
    }


def added_auc_permutation(
    df: pd.DataFrame,
    outcome: str,
    base_numeric: list[str],
    augmented_numeric: list[str],
    categorical: list[str],
    observed_delta: float,
    rng: np.random.Generator,
) -> dict[str, Any]:
    if not np.isfinite(observed_delta) or observed_delta <= 0:
        return {"n_perm": 0, "delta_auc_perm_p": 1.0, "perm_mean_delta_auc": np.nan}
    work = df.copy().dropna(subset=[outcome]).reset_index(drop=True)
    y = work[outcome].astype(int).to_numpy()
    if len(np.unique(y)) < 2 or min(np.bincount(y)) < 2:
        return {"n_perm": 0, "delta_auc_perm_p": np.nan, "perm_mean_delta_auc": np.nan}
    deltas = []
    for _ in range(N_PERM):
        perm = rng.permutation(y)
        tmp = work.copy()
        tmp[outcome] = perm
        base_prob, base_status = loocv_probabilities(tmp, outcome, base_numeric, categorical)
        aug_prob, aug_status = loocv_probabilities(tmp, outcome, augmented_numeric, categorical)
        if base_status != "ok" or aug_status != "ok":
            continue
        base_auc = outcome_metrics(perm, base_prob)["auc"]
        aug_auc = outcome_metrics(perm, aug_prob)["auc"]
        if np.isfinite(base_auc) and np.isfinite(aug_auc):
            deltas.append(float(aug_auc - base_auc))
    if not deltas:
        return {"n_perm": 0, "delta_auc_perm_p": np.nan, "perm_mean_delta_auc": np.nan}
    arr = np.asarray(deltas)
    p = (1.0 + float(np.sum(arr >= observed_delta))) / (len(arr) + 1.0)
    return {"n_perm": int(len(arr)), "delta_auc_perm_p": float(p), "perm_mean_delta_auc": float(arr.mean())}


def bootstrap_auc_delta(
    y: np.ndarray,
    base_prob: np.ndarray,
    aug_prob: np.ndarray,
    rng: np.random.Generator,
    n_boot: int = 1000,
) -> dict[str, Any]:
    mask = np.isfinite(base_prob) & np.isfinite(aug_prob)
    y = y[mask].astype(int)
    base_prob = base_prob[mask]
    aug_prob = aug_prob[mask]
    if len(y) < 8 or len(np.unique(y)) < 2:
        return {"delta_auc_boot_ci_low": np.nan, "delta_auc_boot_ci_high": np.nan}
    vals = []
    n = len(y)
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        if len(np.unique(y[idx])) < 2:
            continue
        vals.append(float(roc_auc_score(y[idx], aug_prob[idx]) - roc_auc_score(y[idx], base_prob[idx])))
    if not vals:
        return {"delta_auc_boot_ci_low": np.nan, "delta_auc_boot_ci_high": np.nan}
    arr = np.asarray(vals)
    return {
        "delta_auc_boot_ci_low": float(np.quantile(arr, 0.025)),
        "delta_auc_boot_ci_high": float(np.quantile(arr, 0.975)),
    }


def paired_model_comparisons(
    *,
    df: pd.DataFrame,
    dataset: str,
    outcome: str,
    response_definition: str,
    base_numeric: list[str],
    categorical: list[str],
    modules: list[str],
    rng: np.random.Generator,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    model_rows = []
    comparison_rows = []
    base_numeric = existing_columns(df, base_numeric)
    categorical = existing_columns(df, categorical)
    base_row = evaluate_model(
        df=df,
        dataset=dataset,
        outcome=outcome,
        response_definition=response_definition,
        model_name="generic_clinical_baseline",
        numeric=base_numeric,
        categorical=categorical,
    )
    model_rows.append(base_row)

    for module in modules:
        target = f"pre_score_{module}"
        if target not in df.columns:
            continue
        augmented_numeric = existing_columns(df, base_numeric + [target])
        target_row = evaluate_model(
            df=df,
            dataset=dataset,
            outcome=outcome,
            response_definition=response_definition,
            model_name=f"generic_plus_{module}",
            numeric=augmented_numeric,
            categorical=categorical,
            target_feature=target,
        )
        model_rows.append(target_row)

        # Recompute probabilities once for paired bootstrap/permutation.
        base_prob, base_status = loocv_probabilities(df, outcome, base_numeric, categorical)
        aug_prob, aug_status = loocv_probabilities(df, outcome, augmented_numeric, categorical)
        y = df.dropna(subset=[outcome])[outcome].astype(int).to_numpy()
        base_auc = outcome_metrics(y, base_prob)["auc"] if base_status == "ok" else np.nan
        aug_auc = outcome_metrics(y, aug_prob)["auc"] if aug_status == "ok" else np.nan
        delta = float(aug_auc - base_auc) if np.isfinite(base_auc) and np.isfinite(aug_auc) else np.nan
        perm = (
            added_auc_permutation(df, outcome, base_numeric, augmented_numeric, categorical, delta, rng)
            if module == PRIMARY_MODULE
            else {"n_perm": 0, "delta_auc_perm_p": np.nan, "perm_mean_delta_auc": np.nan}
        )
        boot = (
            bootstrap_auc_delta(y, base_prob, aug_prob, rng)
            if module == PRIMARY_MODULE
            else {"delta_auc_boot_ci_low": np.nan, "delta_auc_boot_ci_high": np.nan}
        )
        comparison_rows.append(
            {
                "dataset": dataset,
                "response_definition": response_definition,
                "module": module,
                "baseline_auc": base_auc,
                "augmented_auc": aug_auc,
                "delta_auc": delta,
                "baseline_average_precision": outcome_metrics(y, base_prob)["average_precision"],
                "augmented_average_precision": outcome_metrics(y, aug_prob)["average_precision"],
                "baseline_brier": outcome_metrics(y, base_prob)["brier"],
                "augmented_brier": outcome_metrics(y, aug_prob)["brier"],
                "target_coef": target_row["full_model_target_coef"],
                "target_coef_positive": bool(target_row["full_model_target_coef"] > 0) if np.isfinite(target_row["full_model_target_coef"]) else False,
                **perm,
                **boot,
            }
        )
    return pd.DataFrame(model_rows), pd.DataFrame(comparison_rows)


def build_uc_compartment_tables() -> pd.DataFrame:
    donor = read_tsv(UC_DONOR)
    if donor.empty:
        return pd.DataFrame()
    base = donor[donor["timepoint_norm"].eq("W0")].copy()
    base["responder_int"] = base["responder"].astype(bool).astype(int)
    collapsed = (
        base.groupby(["patient", "marker_compartment", "responder_int"], observed=True)
        .agg(
            {
                "mean_score": "mean",
                "high_fraction": "mean",
                "module": lambda x: ";".join(sorted(set(map(str, x)))),
            }
        )
        .reset_index()
    )
    # Build a patient x compartment x module wide table from mean_score only;
    # high_fraction is noisier and was already reported in the marker script.
    mean_wide = (
        base.groupby(["patient", "marker_compartment", "responder_int", "module"], observed=True)["mean_score"]
        .mean()
        .reset_index()
        .pivot_table(index=["patient", "marker_compartment", "responder_int"], columns="module", values="mean_score", aggfunc="first")
        .reset_index()
    )
    mean_wide.columns = [f"pre_score_{c}" if c not in {"patient", "marker_compartment", "responder_int"} else c for c in mean_wide.columns]
    return mean_wide


def uc_stress_tests(rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    uc = build_uc_compartment_tables()
    if uc.empty:
        return pd.DataFrame(), pd.DataFrame()
    model_rows = []
    comparison_rows = []
    modules = ["lysosomal_apc", "ifn_apc"]
    for compartment, sub in uc.groupby("marker_compartment", observed=True):
        if compartment == "ambiguous" or sub["responder_int"].nunique() < 2 or sub.shape[0] < 8:
            continue
        base_numeric = existing_columns(sub, ["pre_score_inflammatory_nfkb"])
        categorical: list[str] = []
        base_row = evaluate_model(
            df=sub,
            dataset="GSE253006_UC_tofacitinib_marker",
            outcome="responder_int",
            response_definition=f"{compartment}_baseline_responder",
            model_name="generic_baseline",
            numeric=base_numeric,
            categorical=categorical,
        )
        model_rows.append(base_row)
        for module in modules:
            target = f"pre_score_{module}"
            if target not in sub.columns:
                continue
            augmented_numeric = existing_columns(sub, base_numeric + [target])
            row = evaluate_model(
                df=sub,
                dataset="GSE253006_UC_tofacitinib_marker",
                outcome="responder_int",
                response_definition=f"{compartment}_baseline_responder",
                model_name=f"generic_plus_{module}",
                numeric=augmented_numeric,
                categorical=categorical,
                target_feature=target,
            )
            model_rows.append(row)
            base_prob, _ = loocv_probabilities(sub, "responder_int", base_numeric, categorical)
            aug_prob, _ = loocv_probabilities(sub, "responder_int", augmented_numeric, categorical)
            y = sub["responder_int"].astype(int).to_numpy()
            base_auc = outcome_metrics(y, base_prob)["auc"]
            aug_auc = outcome_metrics(y, aug_prob)["auc"]
            comparison_rows.append(
                {
                    "dataset": "GSE253006_UC_tofacitinib_marker",
                    "response_definition": f"{compartment}_baseline_responder",
                    "module": module,
                    "baseline_auc": base_auc,
                    "augmented_auc": aug_auc,
                    "delta_auc": float(aug_auc - base_auc) if np.isfinite(base_auc) and np.isfinite(aug_auc) else np.nan,
                    "target_coef": row["full_model_target_coef"],
                    "n": int(sub.shape[0]),
                    "note": "small orthogonal stress test; not a primary anti-TNF replication dataset",
                }
            )
    return pd.DataFrame(model_rows), pd.DataFrame(comparison_rows)


def legacy_response_sensitivity() -> pd.DataFrame:
    rows = []
    w18 = read_tsv(W18_RA_TESTS)
    if not w18.empty:
        keep = w18[
            w18["module"].isin(["lysosomal_apc", "ifn_apc"])
            & w18["test"].isin(["eular_responder_moderate_or_good_vs_none", "good_responder_vs_none"])
        ].copy()
        keep["rank_p"] = pd.to_numeric(keep["p"], errors="coerce")
        for _, r in keep.sort_values("rank_p").head(20).iterrows():
            rows.append(
                {
                    "dataset": "GSE138746_RA_sorted_blood_antiTNF",
                    "evidence_type": "baseline_response_sensitivity",
                    "context": f"{r['compartment']}|{r['drug_scope']}|{r['test']}",
                    "module": r["module"],
                    "effect_or_delta": r.get("delta_responder_minus_nonresponder"),
                    "p": r.get("p"),
                    "fdr": r.get("fdr"),
                    "auc_responder_high": r.get("auc_responder_high"),
                    "interpretation": "blood/sorted-compartment sensitivity; not primary tissue replication",
                }
            )
    ps = read_tsv(W18_PSORIASIS)
    if not ps.empty:
        keep = ps[ps["module"].isin(["lysosomal_apc", "ifn_apc"])].copy()
        keep["rank_p"] = pd.to_numeric(keep["p"], errors="coerce")
        for _, r in keep.sort_values("rank_p").head(10).iterrows():
            rows.append(
                {
                    "dataset": "GSE183047_psoriasis_secukinumab",
                    "evidence_type": "pharmacodynamic_sensitivity_no_response_labels",
                    "context": f"{r['marker_compartment']}|{r['test']}|{r['metric']}",
                    "module": r["module"],
                    "effect_or_delta": r.get("mean_delta"),
                    "p": r.get("p"),
                    "fdr": r.get("fdr"),
                    "auc_responder_high": np.nan,
                    "interpretation": "pharmacodynamic only; no responder labels in local GEO metadata",
                }
            )
    return pd.DataFrame(rows)


def make_decision(primary: pd.DataFrame, uc: pd.DataFrame, legacy: pd.DataFrame) -> pd.DataFrame:
    focus = primary[primary["module"].eq(PRIMARY_MODULE)].copy()
    ra = focus[focus["dataset"].str.contains("RA_synovium", regex=False)]
    ibd = focus[focus["dataset"].str.contains("IBD_DC", regex=False)]
    if ra.empty or ibd.empty:
        call = "NO_GO_WAVE84_NO_PRIMARY_REPLICATION"
        reason = "primary RA and IBD comparisons were not both available"
        best: dict[str, Any] = {}
    else:
        r = ra.iloc[0]
        i = ibd.iloc[0]
        both_delta_positive = bool(r["delta_auc"] > 0 and i["delta_auc"] > 0)
        both_coef_positive = bool(r["target_coef"] > 0 and i["target_coef"] > 0)
        both_perm_support = bool(r["delta_auc_perm_p"] <= 0.10 and i["delta_auc_perm_p"] <= 0.10)
        both_perm_trend = bool(r["delta_auc_perm_p"] <= 0.20 and i["delta_auc_perm_p"] <= 0.20)
        both_auc_ge_060 = bool(r["augmented_auc"] >= 0.60 and i["augmented_auc"] >= 0.60)
        both_boot_ci_excludes_zero = bool(r["delta_auc_boot_ci_low"] > 0 and i["delta_auc_boot_ci_low"] > 0)
        best = {
            "ra_delta_auc": r["delta_auc"],
            "ra_augmented_auc": r["augmented_auc"],
            "ra_delta_auc_perm_p": r["delta_auc_perm_p"],
            "ra_delta_auc_boot_ci_low": r["delta_auc_boot_ci_low"],
            "ibd_delta_auc": i["delta_auc"],
            "ibd_augmented_auc": i["augmented_auc"],
            "ibd_delta_auc_perm_p": i["delta_auc_perm_p"],
            "ibd_delta_auc_boot_ci_low": i["delta_auc_boot_ci_low"],
            "both_delta_positive": both_delta_positive,
            "both_coef_positive": both_coef_positive,
            "both_perm_support": both_perm_support,
            "both_perm_trend": both_perm_trend,
            "both_boot_ci_excludes_zero": both_boot_ci_excludes_zero,
            "both_auc_ge_060": both_auc_ge_060,
        }
        if (
            both_delta_positive
            and both_coef_positive
            and both_perm_support
            and both_boot_ci_excludes_zero
            and both_auc_ge_060
        ):
            call = "STRENGTHEN_STRATIFICATION_PREDICTIVE_SIGNAL"
            reason = "frozen lysosomal/APC module improves prediction in both primary datasets with permutation and bootstrap support"
        elif both_delta_positive and both_coef_positive and both_perm_trend and both_auc_ge_060:
            call = "PARK_STRATIFICATION_WEAK_PREDICTIVE_SIGNAL"
            reason = "direction and added AUC are stable, but permutation p-values are trend-level and bootstrap CIs include zero"
        elif both_delta_positive and both_coef_positive:
            call = "PARK_STRATIFICATION_DIRECTION_ONLY"
            reason = "direction and added AUC are stable, but predictive evidence is not statistically strong"
        else:
            call = "NO_GO_STRATIFICATION_PREDICTION_NOT_REPLICATED"
            reason = "module does not consistently improve prediction over generic-inflammation baseline"
    return pd.DataFrame(
        [
            {
                "candidate": "lysosomal_APC_baseline_antiTNF_response_stratification",
                "wave84_call": call,
                "decision_reason": reason,
                "primary_module": PRIMARY_MODULE,
                **best,
                "uc_stress_best_delta_auc": float(uc["delta_auc"].max()) if not uc.empty else np.nan,
                "legacy_rows": int(legacy.shape[0]) if not legacy.empty else 0,
            }
        ]
    )


def write_report(decision: pd.DataFrame, models: pd.DataFrame, comparisons: pd.DataFrame, uc: pd.DataFrame, legacy: pd.DataFrame) -> None:
    lines = [
        "# Wave84 Response-Prediction Audit",
        "",
        "## Question",
        "",
        "Does a frozen baseline lysosomal/APC response state improve out-of-sample",
        "anti-TNF response prediction beyond generic inflammation and available",
        "clinical/pathotype covariates?",
        "",
        "## Verdict",
        "",
        clean_text(decision.iloc[0]["wave84_call"]),
        "",
        "## Decision",
        "",
        markdown_table(decision),
        "",
        "## Primary RA/IBD Added-AUC Comparisons",
        "",
        markdown_table(comparisons, max_rows=80),
        "",
        "## Primary Model Metrics",
        "",
        markdown_table(
            models[
                [
                    "dataset",
                    "response_definition",
                    "model_name",
                    "target_feature",
                    "fit_status",
                    "n",
                    "n_positive",
                    "n_negative",
                    "auc",
                    "average_precision",
                    "brier",
                    "balanced_accuracy_0_5",
                    "full_model_target_coef",
                ]
            ],
            max_rows=120,
        ),
        "",
        "## UC Tofacitinib Orthogonal Stress Test",
        "",
        markdown_table(uc, max_rows=60),
        "",
        "## Legacy Sensitivity Evidence",
        "",
        markdown_table(legacy, max_rows=40),
        "",
        "## Guardrails",
        "",
        "- This is not causal target evidence.",
        "- Leave-one-out AUC estimates are high-variance at these sample sizes.",
        "- The primary module was frozen from Wave76 before this prediction audit.",
        "- UC tofacitinib and psoriasis secukinumab rows are stress tests, not",
        "  anti-TNF replication.",
        "- A positive added-AUC result would support only biomarker enrichment, not",
        "  a new intervention point.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rng = np.random.default_rng(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    modules = [PRIMARY_MODULE] + SECONDARY_MODULES
    ra = read_tsv(RA_WIDE)
    ibd = read_tsv(IBD_WIDE)
    ibd_dc = ibd[ibd["cell_state"].eq("DC")].copy() if not ibd.empty else pd.DataFrame()

    ra_models, ra_cmp = paired_model_comparisons(
        df=ra,
        dataset="GSE198520_RA_synovium_antiTNF",
        outcome="good_response",
        response_definition="good_vs_moderate_none",
        base_numeric=["pre_score_inflammatory_nfkb", "inflammatory_score", "das28_score"],
        categorical=["pathotype", "biologic"],
        modules=modules,
        rng=rng,
    )
    ibd_models, ibd_cmp = paired_model_comparisons(
        df=ibd_dc,
        dataset="GSE282122_IBD_DC_antiTNF",
        outcome="remission",
        response_definition="remission_vs_nonremission",
        base_numeric=["pre_score_inflammatory_nfkb", "baseline_inflammation_score"],
        categorical=["Disease"],
        modules=modules,
        rng=rng,
    )

    uc_models, uc_cmp = uc_stress_tests(rng)
    legacy = legacy_response_sensitivity()

    models = pd.concat([ra_models, ibd_models, uc_models], ignore_index=True)
    comparisons = pd.concat([ra_cmp, ibd_cmp], ignore_index=True)
    decision = make_decision(comparisons, uc_cmp, legacy)

    models.to_csv(OUT / "loocv_model_metrics.tsv", sep="\t", index=False)
    comparisons.to_csv(OUT / "primary_added_auc_comparisons.tsv", sep="\t", index=False)
    uc_cmp.to_csv(OUT / "uc_tofacitinib_stress_added_auc.tsv", sep="\t", index=False)
    legacy.to_csv(OUT / "legacy_response_sensitivity.tsv", sep="\t", index=False)
    decision.to_csv(OUT / "response_prediction_decision.tsv", sep="\t", index=False)

    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "n_permutations_primary": N_PERM,
            "inputs": {
                "ra_wide": rel(RA_WIDE),
                "ibd_wide": rel(IBD_WIDE),
                "uc_donor_scores": rel(UC_DONOR),
                "wave76_convergence": rel(W76_CONV),
                "wave18_ra_tests": rel(W18_RA_TESTS),
                "wave18_psoriasis": rel(W18_PSORIASIS),
            },
            "decision": decision.replace({np.nan: None}).to_dict(orient="records")[0],
            "primary_comparisons": comparisons.replace({np.nan: None}).to_dict(orient="records"),
        },
    )
    write_report(decision, models, comparisons, uc_cmp, legacy)


if __name__ == "__main__":
    main()
