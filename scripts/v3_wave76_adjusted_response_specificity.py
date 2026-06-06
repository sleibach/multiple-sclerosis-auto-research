#!/usr/bin/env python3
"""Wave76 adjusted response-specificity stress test.

Wave75 reopened an IFN/APC + lysosomal/APC response-stratification signal.
This wave attacks that result with patient-level covariate adjustment and a
target-vs-generic specificity gate.

Pass criteria for a response-stratification survivor:
- same module and endpoint has same-direction response coefficient in RA and
  IBD DC data;
- adjusted response p <= 0.10 in both datasets;
- target/generic absolute coefficient ratio >= 2 in both datasets;
- module is not the generic inflammatory NF-kB comparator.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import ROOT


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave76_adjusted_response_specificity"

RA_PAIRS = ROOT / "phases/v3/results" / "wave75_response_state_stratification" / "ra_patient_module_pairs.tsv"
IBD_PAIRS = ROOT / "phases/v3/results" / "wave75_response_state_stratification" / "ibd_patient_module_pairs.tsv"
RA_META = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"

FROZEN_MODULES = [
    "lysosomal_apc",
    "ifn_lysosomal_apc_composite",
    "ifn_apc",
    "lysosomal_apc__resid_inflammatory_nfkb",
    "ifn_lysosomal_apc_composite__resid_inflammatory_nfkb",
    "ifn_apc__resid_inflammatory_nfkb",
    "inflammatory_nfkb",
]
GENERIC_MODULE = "inflammatory_nfkb"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
    if df.empty:
        return "_No rows._"
    view = df.head(max_rows).copy()
    cols = list(view.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in view.iterrows():
        vals = []
        for col in cols:
            value = row[col]
            if isinstance(value, float):
                vals.append("" if math.isnan(value) else f"{value:.4g}")
            else:
                vals.append(str(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def bh(values: pd.Series | np.ndarray) -> np.ndarray:
    return multipletests(pd.Series(values).fillna(1.0).to_numpy(float), method="fdr_bh")[1]


def numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series.replace("NA", np.nan), errors="coerce")


def build_ra_wide() -> pd.DataFrame:
    pairs = pd.read_csv(RA_PAIRS, sep="\t")
    meta = pd.read_csv(RA_META, sep="\t")
    pre_meta = meta[meta["timepoint"].eq("pre")].copy()
    keep = [
        "patient",
        "pathotype",
        "biologic",
        "steroids_(medication)",
        "gender",
        "age",
        "inflammatory_score",
        "das28_score",
        "crp",
        "esr",
    ]
    pre_meta = pre_meta[[c for c in keep if c in pre_meta.columns]].drop_duplicates("patient")
    for col in ["age", "inflammatory_score", "das28_score", "crp", "esr"]:
        if col in pre_meta.columns:
            pre_meta[col] = numeric(pre_meta[col])
    wide = (
        pairs.pivot_table(
            index=[
                "patient",
                "response_code",
                "response_class",
                "responder_good_only",
                "responder_moderate_or_good",
                "pathotype",
                "delta_das28",
            ],
            columns="module",
            values=["pre_score", "post_minus_pre"],
            aggfunc="first",
        )
        .reset_index()
    )
    wide.columns = [
        "_".join([str(x) for x in col if str(x)]) if isinstance(col, tuple) else str(col)
        for col in wide.columns
    ]
    wide = wide.merge(pre_meta.drop(columns=["pathotype"], errors="ignore"), on="patient", how="left")
    wide["good_response"] = wide["response_code"].eq("r").astype(int)
    wide["moderate_good_response"] = wide["response_code"].isin(["r", "mr"]).astype(int)
    wide["delta_das28"] = numeric(wide["delta_das28"])
    return wide


def build_ibd_wide() -> pd.DataFrame:
    pairs = pd.read_csv(IBD_PAIRS, sep="\t")
    wide = (
        pairs.pivot_table(
            index=["Patient", "Disease", "Remission_status", "cell_state", "baseline_inflammation_score"],
            columns="module",
            values=["pre_score", "post_minus_pre"],
            aggfunc="first",
        )
        .reset_index()
    )
    wide.columns = [
        "_".join([str(x) for x in col if str(x)]) if isinstance(col, tuple) else str(col)
        for col in wide.columns
    ]
    wide["remission"] = wide["Remission_status"].eq("Remission").astype(int)
    wide["baseline_inflammation_score"] = numeric(wide["baseline_inflammation_score"])
    return wide


def fit_response_model(
    data: pd.DataFrame,
    y_col: str,
    response_col: str,
    formula_rhs: str,
    dataset: str,
    cell_state: str,
    endpoint: str,
    comparison: str,
    module: str,
) -> dict[str, Any]:
    needed = [y_col, response_col]
    for token in [
        "pre_score_inflammatory_nfkb",
        "post_minus_pre_inflammatory_nfkb",
        "baseline_inflammation_score",
        "inflammatory_score",
        "das28_score",
        "delta_das28",
    ]:
        if token in formula_rhs:
            needed.append(token)
    needed = [c for c in needed if c in data.columns]
    model_df = data.dropna(subset=needed).copy()
    if model_df[response_col].nunique() < 2 or model_df.shape[0] < 12:
        return {
            "dataset": dataset,
            "cell_state": cell_state,
            "endpoint": endpoint,
            "comparison": comparison,
            "module": module,
            "n": int(model_df.shape[0]),
            "response_coef": np.nan,
            "response_p": np.nan,
            "model_status": "insufficient_rows_or_response_levels",
            "formula": "",
        }
    formula = f"y ~ {formula_rhs}"
    model_df = model_df.rename(columns={y_col: "y"})
    try:
        model = smf.ols(formula, data=model_df).fit()
        coef = float(model.params.get(response_col, np.nan))
        pval = float(model.pvalues.get(response_col, np.nan))
        status = "ok"
    except Exception as exc:  # noqa: BLE001
        coef = np.nan
        pval = np.nan
        status = f"fit_failed:{type(exc).__name__}:{exc}"
    return {
        "dataset": dataset,
        "cell_state": cell_state,
        "endpoint": endpoint,
        "comparison": comparison,
        "module": module,
        "n": int(model_df.shape[0]),
        "response_coef": coef,
        "response_p": pval,
        "model_status": status,
        "formula": formula,
    }


def ra_adjusted_models(ra: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for comparison, response_col in [
        ("good_vs_moderate_none", "good_response"),
        ("moderate_good_vs_none", "moderate_good_response"),
    ]:
        for module in FROZEN_MODULES:
            pre_col = f"pre_score_{module}"
            delta_col = f"post_minus_pre_{module}"
            if pre_col not in ra.columns:
                continue
            if module == GENERIC_MODULE:
                baseline_rhs = f"{response_col} + C(pathotype) + C(biologic) + inflammatory_score + das28_score"
            else:
                baseline_rhs = (
                    f"{response_col} + pre_score_{GENERIC_MODULE} + C(pathotype) + "
                    "C(biologic) + inflammatory_score + das28_score"
                )
            rows.append(
                fit_response_model(
                    ra,
                    pre_col,
                    response_col,
                    baseline_rhs,
                    "GSE198520_RA_synovium_antiTNF",
                    "bulk_synovium",
                    "baseline_pre",
                    comparison,
                    module,
                )
            )
            if delta_col not in ra.columns:
                continue
            if module == GENERIC_MODULE:
                delta_rhs = (
                    f"{response_col} + pre_score_{GENERIC_MODULE} + C(pathotype) + "
                    "C(biologic) + inflammatory_score + das28_score"
                )
            else:
                delta_rhs = (
                    f"{response_col} + {pre_col} + pre_score_{GENERIC_MODULE} + "
                    f"post_minus_pre_{GENERIC_MODULE} + C(pathotype) + C(biologic) + "
                    "inflammatory_score + das28_score"
                )
            rows.append(
                fit_response_model(
                    ra,
                    delta_col,
                    response_col,
                    delta_rhs,
                    "GSE198520_RA_synovium_antiTNF",
                    "bulk_synovium",
                    "delta_post_minus_pre",
                    comparison,
                    module,
                )
            )
    out = pd.DataFrame(rows)
    out["response_fdr"] = bh(out["response_p"])
    return out


def ibd_adjusted_models(ibd: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for cell_state, sub in ibd.groupby("cell_state", observed=True):
        for module in FROZEN_MODULES:
            pre_col = f"pre_score_{module}"
            delta_col = f"post_minus_pre_{module}"
            if pre_col not in sub.columns:
                continue
            if module == GENERIC_MODULE:
                baseline_rhs = "remission + C(Disease) + baseline_inflammation_score"
            else:
                baseline_rhs = f"remission + pre_score_{GENERIC_MODULE} + C(Disease) + baseline_inflammation_score"
            rows.append(
                fit_response_model(
                    sub,
                    pre_col,
                    "remission",
                    baseline_rhs,
                    "GSE282122_IBD_myeloid_antiTNF",
                    str(cell_state),
                    "baseline_pre",
                    "remission_vs_nonremission",
                    module,
                )
            )
            if delta_col not in sub.columns:
                continue
            if module == GENERIC_MODULE:
                delta_rhs = "remission + pre_score_inflammatory_nfkb + C(Disease) + baseline_inflammation_score"
            else:
                delta_rhs = (
                    f"remission + {pre_col} + pre_score_{GENERIC_MODULE} + "
                    f"post_minus_pre_{GENERIC_MODULE} + C(Disease) + baseline_inflammation_score"
                )
            rows.append(
                fit_response_model(
                    sub,
                    delta_col,
                    "remission",
                    delta_rhs,
                    "GSE282122_IBD_myeloid_antiTNF",
                    str(cell_state),
                    "delta_post_minus_pre",
                    "remission_vs_nonremission",
                    module,
                )
            )
    out = pd.DataFrame(rows)
    out["response_fdr"] = bh(out["response_p"])
    return out


def add_specificity_ratios(models: pd.DataFrame) -> pd.DataFrame:
    out = models.copy()
    generic = out[out["module"].eq(GENERIC_MODULE)][
        ["dataset", "cell_state", "endpoint", "comparison", "response_coef", "response_p"]
    ].rename(columns={"response_coef": "generic_response_coef", "response_p": "generic_response_p"})
    out = out.merge(generic, on=["dataset", "cell_state", "endpoint", "comparison"], how="left")
    out["target_generic_abs_ratio"] = np.where(
        out["generic_response_coef"].abs() > 1e-9,
        out["response_coef"].abs() / out["generic_response_coef"].abs(),
        np.inf,
    )
    return out


def convergence(models: pd.DataFrame) -> pd.DataFrame:
    rows = []
    ra = models[
        models["dataset"].eq("GSE198520_RA_synovium_antiTNF")
        & models["comparison"].isin(["good_vs_moderate_none", "moderate_good_vs_none"])
    ].copy()
    ibd = models[
        models["dataset"].eq("GSE282122_IBD_myeloid_antiTNF")
        & models["comparison"].eq("remission_vs_nonremission")
        & models["cell_state"].eq("DC")
    ].copy()
    modules = sorted((set(FROZEN_MODULES) - {GENERIC_MODULE}) & set(ra["module"]) & set(ibd["module"]))
    for module in modules:
        for endpoint in ["baseline_pre", "delta_post_minus_pre"]:
            rsub = ra[(ra["module"].eq(module)) & (ra["endpoint"].eq(endpoint)) & ra["model_status"].eq("ok")]
            isub = ibd[(ibd["module"].eq(module)) & (ibd["endpoint"].eq(endpoint)) & ibd["model_status"].eq("ok")]
            if rsub.empty or isub.empty:
                continue
            rbest = rsub.sort_values("response_p").iloc[0]
            ibest = isub.sort_values("response_p").iloc[0]
            r_coef = float(rbest["response_coef"])
            i_coef = float(ibest["response_coef"])
            sign_stable = math.isfinite(r_coef) and math.isfinite(i_coef) and np.sign(r_coef) == np.sign(i_coef)
            rows.append(
                {
                    "module": module,
                    "endpoint": endpoint,
                    "ra_comparison": rbest["comparison"],
                    "ra_n": int(rbest["n"]),
                    "ra_coef": r_coef,
                    "ra_p": float(rbest["response_p"]),
                    "ra_fdr": float(rbest["response_fdr"]),
                    "ra_generic_coef": float(rbest["generic_response_coef"]),
                    "ra_target_generic_abs_ratio": float(rbest["target_generic_abs_ratio"]),
                    "ibd_cell_state": ibest["cell_state"],
                    "ibd_n": int(ibest["n"]),
                    "ibd_coef": i_coef,
                    "ibd_p": float(ibest["response_p"]),
                    "ibd_fdr": float(ibest["response_fdr"]),
                    "ibd_generic_coef": float(ibest["generic_response_coef"]),
                    "ibd_target_generic_abs_ratio": float(ibest["target_generic_abs_ratio"]),
                    "sign_stable": bool(sign_stable),
                    "both_adjusted_p10": bool(sign_stable and rbest["response_p"] <= 0.10 and ibest["response_p"] <= 0.10),
                    "both_ratio_ge2": bool(
                        sign_stable
                        and rbest["target_generic_abs_ratio"] >= 2.0
                        and ibest["target_generic_abs_ratio"] >= 2.0
                    ),
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["passes_wave76_specificity"] = out["both_adjusted_p10"] & out["both_ratio_ge2"]
        out["priority"] = (
            3 * out["passes_wave76_specificity"].astype(int)
            + 2 * out["both_adjusted_p10"].astype(int)
            + out["sign_stable"].astype(int)
        )
        out = out.sort_values(["priority", "ra_p", "ibd_p"], ascending=[False, True, True])
    return out


def make_decision(conv: pd.DataFrame) -> pd.DataFrame:
    if conv.empty:
        call = "NO_GO_WAVE76_NO_COMPARABLE_MODELS"
        reason = "no adjusted comparable RA/IBD DC models fit"
        best: dict[str, Any] = {}
    else:
        best = conv.iloc[0].to_dict()
        if bool(best.get("passes_wave76_specificity")):
            call = "STRENGTHEN_RESPONSE_STRATIFICATION"
            reason = "adjusted cross-dataset response signal survives target/generic specificity gate"
        elif bool(best.get("both_adjusted_p10")):
            call = "PARK_RESPONSE_SIGNAL_GENERIC_LIMITED"
            reason = "adjusted response signal replicates but does not beat generic inflammation by ratio >=2 in both datasets"
        elif bool(best.get("sign_stable")):
            call = "PARK_RESPONSE_SIGNAL_ADJUSTED_WEAK"
            reason = "adjusted signs are stable but p-value gate fails"
        else:
            call = "NO_GO_RESPONSE_SIGNAL_CONFOUNDED"
            reason = "Wave75 response signal does not survive adjusted specificity stress test"
    return pd.DataFrame(
        [
            {
                "candidate": "IFN_APC_lysosomal_APC_response_stratification",
                "wave76_call": call,
                "decision_reason": reason,
                "best_module": best.get("module", ""),
                "best_endpoint": best.get("endpoint", ""),
                "ra_coef": best.get("ra_coef", np.nan),
                "ra_p": best.get("ra_p", np.nan),
                "ra_target_generic_abs_ratio": best.get("ra_target_generic_abs_ratio", np.nan),
                "ibd_coef": best.get("ibd_coef", np.nan),
                "ibd_p": best.get("ibd_p", np.nan),
                "ibd_target_generic_abs_ratio": best.get("ibd_target_generic_abs_ratio", np.nan),
                "sign_stable": best.get("sign_stable", False),
                "both_adjusted_p10": best.get("both_adjusted_p10", False),
                "both_ratio_ge2": best.get("both_ratio_ge2", False),
                "passes_wave76_specificity": best.get("passes_wave76_specificity", False),
            }
        ]
    )


def write_report(decision: pd.DataFrame, conv: pd.DataFrame, models: pd.DataFrame) -> None:
    lines = [
        "# Wave76 Adjusted Response-Specificity Stress Test",
        "",
        "## Question",
        "",
        "Does the Wave75 IFN/APC plus lysosomal/APC response-stratification signal",
        "survive patient-level adjustment and target/generic specificity gates?",
        "",
        "## Verdict",
        "",
        str(decision.iloc[0]["wave76_call"]),
        "",
        "## Integrated Decision",
        "",
        markdown_table(decision),
        "",
        "## Cross-Dataset Adjusted Convergence",
        "",
        markdown_table(conv, max_rows=40),
        "",
        "## Adjusted Model Rows",
        "",
        markdown_table(
            models.sort_values("response_p")[
                [
                    "dataset",
                    "cell_state",
                    "endpoint",
                    "comparison",
                    "module",
                    "n",
                    "response_coef",
                    "response_p",
                    "response_fdr",
                    "generic_response_coef",
                    "target_generic_abs_ratio",
                    "model_status",
                ]
            ],
            max_rows=80,
        ),
        "",
        "## Frozen Gate",
        "",
        "- RA baseline models adjust for generic inflammatory NF-kB score, pathotype,",
        "  biologic, baseline tissue inflammatory score, and baseline DAS28.",
        "- RA delta models also adjust for baseline target module and delta generic",
        "  inflammatory NF-kB score.",
        "- IBD baseline models adjust for generic inflammatory NF-kB score, disease",
        "  label, and baseline inflammation score within cell state.",
        "- IBD delta models also adjust for baseline target module and delta generic",
        "  inflammatory NF-kB score.",
        "- A survivor requires same sign, adjusted p <= 0.10 in RA and IBD DC, and",
        "  target/generic absolute response-coefficient ratio >= 2 in both datasets.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    ra = build_ra_wide()
    ibd = build_ibd_wide()
    ra_models = ra_adjusted_models(ra)
    ibd_models = ibd_adjusted_models(ibd)
    models = add_specificity_ratios(pd.concat([ra_models, ibd_models], ignore_index=True))
    conv = convergence(models)
    decision = make_decision(conv)

    ra.to_csv(OUT / "ra_wide_patient_table.tsv", sep="\t", index=False)
    ibd.to_csv(OUT / "ibd_wide_patient_cellstate_table.tsv", sep="\t", index=False)
    models.to_csv(OUT / "adjusted_response_models.tsv", sep="\t", index=False)
    conv.to_csv(OUT / "adjusted_cross_dataset_convergence.tsv", sep="\t", index=False)
    decision.to_csv(OUT / "adjusted_response_specificity_decision.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "inputs": {
            "wave75_ra_pairs": rel(RA_PAIRS),
            "wave75_ibd_pairs": rel(IBD_PAIRS),
            "ra_meta": rel(RA_META),
        },
        "ra_n": int(ra.shape[0]),
        "ibd_n_patient_cellstates": int(ibd.shape[0]),
        "decision": decision.replace({np.nan: None}).to_dict(orient="records")[0],
        "top_convergence": conv.head(20).replace({np.nan: None}).to_dict(orient="records") if not conv.empty else [],
    }
    write_json(OUT / "summary.json", summary)
    write_report(decision, conv, models)


if __name__ == "__main__":
    main()
