#!/usr/bin/env python3
"""Wave84 stratification-first audit.

Target nomination has repeatedly failed because reachable nodes are broad and
specific residual nodes are not reachable. This wave tests a different
translation route: whether the lipid-lysosomal/myeloid module is a
treatment-response stratification state across independent autoimmune datasets.

The analysis uses individual-level module scores where available and treats
peripheral-blood contradiction as a real failure mode.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from v3_analyze_direct_h5ad_cell_states import ROOT


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave84_stratification_first_audit"

RA_WIDE = ROOT / "phases/v3/results" / "wave76_adjusted_response_specificity" / "ra_wide_patient_table.tsv"
IBD_WIDE = ROOT / "phases/v3/results" / "wave76_adjusted_response_specificity" / "ibd_wide_patient_cellstate_table.tsv"
RA_BLOOD = ROOT / "phases/v3/results" / "wave18_treatment_response" / "wave18_gse138746_ra_sample_module_scores.tsv"
W75_CROSS = ROOT / "phases/v3/results" / "wave75_response_state_stratification" / "cross_dataset_response_convergence.tsv"
W76_CROSS = ROOT / "phases/v3/results" / "wave76_adjusted_response_specificity" / "adjusted_cross_dataset_convergence.tsv"
PSO_PREPOST = ROOT / "phases/v3/results" / "wave18_treatment_response" / "wave18_gse183047_psoriasis_prepost_tests.tsv"
UC_TOFA = ROOT / "phases/v3/results" / "wave18_treatment_response" / "wave18_existing_gse253006_uc_summary.tsv"

MODULES = [
    "lysosomal_apc",
    "lysosomal_apc__resid_inflammatory_nfkb",
    "ifn_lysosomal_apc_composite",
    "ifn_lysosomal_apc_composite__resid_inflammatory_nfkb",
    "ifn_apc",
    "ifn_apc__resid_inflammatory_nfkb",
    "hla_ii_apc",
    "hla_ii_apc__resid_ifn_apc_inflammatory_nfkb",
    "lipid_loader_repair",
    "complement_phagocytosis",
    "mif_cd74_receptor_state",
    "inflammatory_nfkb",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
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
                vals.append(str(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def fdr_bh(pvalues: list[float]) -> list[float]:
    p = np.asarray([1.0 if not np.isfinite(x) else x for x in pvalues], dtype=float)
    n = len(p)
    if n == 0:
        return []
    order = np.argsort(p)
    ranked = p[order]
    q = ranked * n / (np.arange(n) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(n, dtype=float)
    out[order] = np.clip(q, 0.0, 1.0)
    return out.tolist()


def auc_score(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    pos = score[y == 1]
    neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    wins = 0.0
    total = len(pos) * len(neg)
    for value in pos:
        wins += float((value > neg).sum())
        wins += 0.5 * float((value == neg).sum())
    return wins / total


def design_matrix(df: pd.DataFrame, covariates: list[str]) -> np.ndarray:
    cols = [np.ones(len(df))]
    for covar in covariates:
        if covar not in df.columns:
            continue
        series = df[covar]
        if pd.api.types.is_numeric_dtype(series):
            values = pd.to_numeric(series, errors="coerce").fillna(series.median() if series.notna().any() else 0.0)
            sd = values.std(ddof=0)
            cols.append(((values - values.mean()) / (sd if sd > 0 else 1.0)).to_numpy(dtype=float))
        else:
            dummies = pd.get_dummies(series.fillna("missing").astype(str), prefix=covar, drop_first=True)
            for col in dummies.columns:
                cols.append(dummies[col].to_numpy(dtype=float))
    return np.column_stack(cols)


def residualize(y: np.ndarray, covar_df: pd.DataFrame, covariates: list[str]) -> np.ndarray:
    x = design_matrix(covar_df, covariates)
    beta, *_ = np.linalg.lstsq(x, y.astype(float), rcond=None)
    return y.astype(float) - x @ beta


def bootstrap_rate_diff(y: np.ndarray, oriented_score: np.ndarray, n_boot: int = 1000) -> tuple[float, float, float]:
    rng = np.random.default_rng(SEED)
    n = len(y)
    if n < 6 or len(np.unique(y)) < 2:
        return float("nan"), float("nan"), float("nan")

    def one(idx: np.ndarray) -> float:
        yy = y[idx]
        ss = oriented_score[idx]
        if len(np.unique(yy)) < 2:
            return float("nan")
        high = ss >= np.nanmedian(ss)
        if high.sum() == 0 or (~high).sum() == 0:
            return float("nan")
        return float(yy[high].mean() - yy[~high].mean())

    observed = one(np.arange(n))
    boots = [one(rng.integers(0, n, size=n)) for _ in range(n_boot)]
    boots = np.asarray([b for b in boots if np.isfinite(b)])
    if len(boots) == 0:
        return observed, float("nan"), float("nan")
    return observed, float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))


def analyze_context(
    *,
    dataset: str,
    system: str,
    df: pd.DataFrame,
    outcome_col: str,
    module_col_prefix: str,
    modules: list[str],
    covariates: list[str],
    context_note: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if df.empty or outcome_col not in df.columns:
        return rows
    base = df.copy()
    base[outcome_col] = pd.to_numeric(base[outcome_col], errors="coerce")
    base = base[base[outcome_col].isin([0, 1])].copy()
    for module in modules:
        col = f"{module_col_prefix}{module}"
        if col not in base.columns:
            continue
        selected_cols = [outcome_col, col]
        for covar in covariates:
            if covar in base.columns and covar not in selected_cols:
                selected_cols.append(covar)
        sub = base[selected_cols].copy()
        sub[col] = pd.to_numeric(sub[col], errors="coerce")
        sub = sub.dropna(subset=[outcome_col, col])
        if len(sub) < 8 or sub[outcome_col].nunique() < 2:
            continue
        y = sub[outcome_col].astype(int).to_numpy()
        score = sub[col].astype(float).to_numpy()
        raw_effect = float(score[y == 1].mean() - score[y == 0].mean())
        raw_t, raw_p = stats.ttest_ind(score[y == 1], score[y == 0], equal_var=False, nan_policy="omit")
        resid = residualize(score, sub, covariates)
        resid_effect = float(resid[y == 1].mean() - resid[y == 0].mean())
        resid_t, resid_p = stats.ttest_ind(resid[y == 1], resid[y == 0], equal_var=False, nan_policy="omit")
        raw_auc = auc_score(y, score)
        resid_auc = auc_score(y, resid)
        orientation = 1.0 if resid_effect >= 0 else -1.0
        oriented_resid = resid * orientation
        oriented_auc = auc_score(y, oriented_resid)
        rate_diff, rate_diff_lo, rate_diff_hi = bootstrap_rate_diff(y, oriented_resid)
        rows.append(
            {
                "dataset": dataset,
                "system": system,
                "context_note": context_note,
                "module": module,
                "n": int(len(sub)),
                "n_responders": int(y.sum()),
                "n_nonresponders": int((1 - y).sum()),
                "raw_effect_responder_minus_non": raw_effect,
                "raw_p": float(raw_p) if np.isfinite(raw_p) else 1.0,
                "raw_auc_high_score": raw_auc,
                "adjusted_effect_responder_minus_non": resid_effect,
                "adjusted_p": float(resid_p) if np.isfinite(resid_p) else 1.0,
                "adjusted_auc_high_score": resid_auc,
                "oriented_auc": oriented_auc,
                "oriented_high_vs_low_response_rate_diff": rate_diff,
                "rate_diff_boot_ci_low": rate_diff_lo,
                "rate_diff_boot_ci_high": rate_diff_hi,
                "direction": "higher_in_responders" if resid_effect >= 0 else "lower_in_responders",
                "covariates": ";".join([c for c in covariates if c in sub.columns]),
            }
        )
    return rows


def build_ra_blood_wide(path: Path) -> pd.DataFrame:
    scores = read_tsv(path)
    if scores.empty:
        return scores
    idx_cols = ["sample", "patient", "compartment", "drug", "response_code", "response_class", "eular_responder", "good_responder"]
    wide = scores.pivot_table(index=idx_cols, columns="module", values="score", aggfunc="mean").reset_index()
    wide.columns = [str(c) for c in wide.columns]
    for module in MODULES:
        if module in wide.columns:
            wide[f"score_{module}"] = wide[module]
    wide["eular_response"] = wide["eular_responder"].astype(bool).astype(int)
    wide["good_response"] = wide["good_responder"].astype(bool).astype(int)
    return wide


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    ra = read_tsv(RA_WIDE)
    ibd = read_tsv(IBD_WIDE)
    ra_blood = build_ra_blood_wide(RA_BLOOD)
    w75 = read_tsv(W75_CROSS)
    w76 = read_tsv(W76_CROSS)
    pso = read_tsv(PSO_PREPOST)
    uc_tofa = read_tsv(UC_TOFA)

    rows: list[dict[str, Any]] = []
    if not ra.empty:
        rows.extend(
            analyze_context(
                dataset="GSE198520",
                system="RA_synovium_antiTNF",
                df=ra,
                outcome_col="good_response",
                module_col_prefix="pre_score_",
                modules=MODULES,
                covariates=["pre_score_inflammatory_nfkb", "pathotype", "biologic", "inflammatory_score", "das28_score"],
                context_note="inflamed synovial biopsy bulk RNA, good EULAR response vs moderate/none",
            )
        )
    if not ibd.empty:
        for cell_state in ["DC", "Mono_macro"]:
            sub = ibd[ibd["cell_state"] == cell_state].copy()
            rows.extend(
                analyze_context(
                    dataset="GSE282122",
                    system=f"IBD_{cell_state}_antiTNF",
                    df=sub,
                    outcome_col="remission",
                    module_col_prefix="pre_score_",
                    modules=MODULES,
                    covariates=["baseline_inflammation_score", "Disease"],
                    context_note=f"intestinal myeloid pseudobulk, {cell_state}, remission vs non-remission",
                )
            )
    if not ra_blood.empty:
        for compartment in ["CD14_monocyte", "PBMC", "CD4_T_cell"]:
            sub = ra_blood[ra_blood["compartment"] == compartment].copy()
            rows.extend(
                analyze_context(
                    dataset="GSE138746",
                    system=f"RA_blood_{compartment}_antiTNF",
                    df=sub,
                    outcome_col="eular_response",
                    module_col_prefix="score_",
                    modules=MODULES,
                    covariates=["drug"],
                    context_note="sorted blood/PBMC baseline, moderate-or-good EULAR response vs none",
                )
            )

    tests = pd.DataFrame(rows)
    if not tests.empty:
        tests["adjusted_fdr"] = fdr_bh(tests["adjusted_p"].tolist())
        tests["raw_fdr"] = fdr_bh(tests["raw_p"].tolist())
        tests["nominal_adjusted_p10"] = tests["adjusted_p"] < 0.1
        tests["response_effect_abs"] = tests["adjusted_effect_responder_minus_non"].abs()
        tests = tests.sort_values(["nominal_adjusted_p10", "adjusted_p", "response_effect_abs"], ascending=[False, True, False])
    tests.to_csv(OUT / "stratification_context_tests.tsv", sep="\t", index=False)

    summaries: list[dict[str, Any]] = []
    for module, sub in tests.groupby("module", dropna=False):
        tissue = sub[sub["system"].isin(["RA_synovium_antiTNF", "IBD_DC_antiTNF", "IBD_Mono_macro_antiTNF"])]
        blood = sub[sub["system"].str.startswith("RA_blood")]
        tissue_nom = tissue[tissue["adjusted_p"] < 0.1]
        blood_nom = blood[blood["adjusted_p"] < 0.1]
        tissue_signs = set(tissue_nom["direction"])
        blood_signs = set(blood_nom["direction"])
        contradiction = bool(tissue_signs and blood_signs and not tissue_signs.issuperset(blood_signs))
        best_tissue = tissue.sort_values("adjusted_p").head(1)
        best_blood = blood.sort_values("adjusted_p").head(1)
        tissue_support_mask = (tissue["adjusted_p"] < 0.1) & (tissue["oriented_auc"] >= 0.6)
        blood_support_mask = (blood["adjusted_p"] < 0.1) & (blood["oriented_auc"] >= 0.6)
        n_tissue_support = int(tissue_support_mask.sum())
        n_tissue_support_datasets = int(tissue.loc[tissue_support_mask, "dataset"].nunique())
        n_blood_support = int(blood_support_mask.sum())
        tissue_direction_conflict = len(tissue_signs) > 1
        if n_tissue_support_datasets >= 2 and not contradiction and not tissue_direction_conflict:
            call = "PARK_TISSUE_STRATIFICATION_SIGNAL"
        elif n_tissue_support >= 2 and (contradiction or tissue_direction_conflict):
            call = "NO_GO_TISSUE_SIGNAL_BLOOD_CONTRADICTION"
        else:
            call = "NO_GO_STRATIFICATION_NOT_REPLICATED"
        summaries.append(
            {
                "module": module,
                "wave84_call": call,
                "n_contexts": int(len(sub)),
                "n_tissue_nominal_auc60": n_tissue_support,
                "n_tissue_support_datasets": n_tissue_support_datasets,
                "n_blood_nominal_auc60": n_blood_support,
                "tissue_nominal_directions": ";".join(sorted(tissue_signs)),
                "blood_nominal_directions": ";".join(sorted(blood_signs)),
                "tissue_direction_conflict": tissue_direction_conflict,
                "blood_tissue_direction_contradiction": contradiction,
                "best_tissue_system": best_tissue["system"].iloc[0] if not best_tissue.empty else "",
                "best_tissue_adjusted_effect": float(best_tissue["adjusted_effect_responder_minus_non"].iloc[0]) if not best_tissue.empty else float("nan"),
                "best_tissue_adjusted_p": float(best_tissue["adjusted_p"].iloc[0]) if not best_tissue.empty else float("nan"),
                "best_tissue_oriented_auc": float(best_tissue["oriented_auc"].iloc[0]) if not best_tissue.empty else float("nan"),
                "best_blood_system": best_blood["system"].iloc[0] if not best_blood.empty else "",
                "best_blood_adjusted_effect": float(best_blood["adjusted_effect_responder_minus_non"].iloc[0]) if not best_blood.empty else float("nan"),
                "best_blood_adjusted_p": float(best_blood["adjusted_p"].iloc[0]) if not best_blood.empty else float("nan"),
                "best_blood_oriented_auc": float(best_blood["oriented_auc"].iloc[0]) if not best_blood.empty else float("nan"),
            }
        )
    summary_df = pd.DataFrame(summaries)
    if not summary_df.empty:
        priority = {
            "PARK_TISSUE_STRATIFICATION_SIGNAL": 0,
            "NO_GO_TISSUE_SIGNAL_BLOOD_CONTRADICTION": 1,
            "NO_GO_STRATIFICATION_NOT_REPLICATED": 2,
        }
        summary_df["priority"] = summary_df["wave84_call"].map(priority).fillna(9).astype(int)
        summary_df = summary_df.sort_values(
            ["priority", "n_tissue_support_datasets", "n_tissue_nominal_auc60", "best_tissue_adjusted_p"],
            ascending=[True, False, False, True],
        ).drop(columns=["priority"])
    summary_df.to_csv(OUT / "module_stratification_summary.tsv", sep="\t", index=False)

    pharmaco_rows: list[dict[str, Any]] = []
    if not pso.empty:
        pso_sub = pso[(pso["marker_compartment"] == "myeloid_apc_like") & (pso["metric"] == "mean_score")].copy()
        for _, row in pso_sub.iterrows():
            pharmaco_rows.append(
                {
                    "dataset": "GSE183047",
                    "system": "psoriasis_secukinumab_myeloid_apc_like",
                    "module": row["module"],
                    "n": row["n_pairs"],
                    "effect_post_minus_pre": row["mean_delta"],
                    "p": row["p"],
                    "fdr": row["fdr"],
                    "note": "pharmacodynamic only; no responder/non-responder stratification",
                }
            )
    if not uc_tofa.empty:
        uc_sub = uc_tofa[uc_tofa["analysis_type"].astype(str).str.contains("baseline_response", na=False)].copy()
        for _, row in uc_sub.iterrows():
            pharmaco_rows.append(
                {
                    "dataset": "GSE253006",
                    "system": f"UC_tofacitinib_{row.get('compartment', '')}",
                    "module": row["module"],
                    "n": row["n"],
                    "effect_post_minus_pre": row["effect"],
                    "p": row["p"],
                    "fdr": row["fdr"],
                    "note": row["note"],
                }
            )
    pharmaco = pd.DataFrame(pharmaco_rows)
    pharmaco.to_csv(OUT / "secondary_pharmacodynamic_or_small_response_contexts.tsv", sep="\t", index=False)

    top_tests = tests.head(30).copy()
    top_summary = summary_df.head(20).copy()
    call_counts = summary_df["wave84_call"].value_counts().to_dict() if not summary_df.empty else {}
    summary = {
        "random_seed": SEED,
        "inputs": {
            "ra_wide": rel(RA_WIDE),
            "ibd_wide": rel(IBD_WIDE),
            "ra_blood": rel(RA_BLOOD),
            "wave75_cross": rel(W75_CROSS),
            "wave76_cross": rel(W76_CROSS),
            "pso_prepost": rel(PSO_PREPOST),
            "uc_tofa": rel(UC_TOFA),
        },
        "n_context_tests": int(len(tests)),
        "module_call_counts": call_counts,
        "top_module": summary_df.head(1).to_dict(orient="records")[0] if not summary_df.empty else {},
        "interpretation": "Parks are biomarker hypotheses only; no therapeutic target is nominated.",
    }
    write_json(OUT / "summary.json", summary)

    report = f"""# Wave84 Stratification-First Audit

## Question

Does the lipid-lysosomal/myeloid state stratify treatment response across
independent autoimmune datasets strongly enough to support a biomarker-guided
claim?

## Verdict

This wave does not produce a therapeutic target. It tests whether a
stratification route is more defensible than direct target nomination.

## Module Calls

{markdown_table(summary_df[["module", "wave84_call", "n_tissue_nominal_auc60", "n_tissue_support_datasets", "n_blood_nominal_auc60", "tissue_direction_conflict", "blood_tissue_direction_contradiction", "best_tissue_system", "best_tissue_adjusted_effect", "best_tissue_adjusted_p", "best_tissue_oriented_auc", "best_blood_system", "best_blood_adjusted_effect", "best_blood_adjusted_p"]])}

## Top Individual Context Tests

{markdown_table(top_tests[["dataset", "system", "module", "n", "n_responders", "adjusted_effect_responder_minus_non", "adjusted_p", "adjusted_fdr", "oriented_auc", "oriented_high_vs_low_response_rate_diff", "direction", "covariates"]])}

## Existing Cross-Dataset Summaries Used As Guardrails

Wave75 best cross-dataset response rows:

{markdown_table(w75.head(8))}

Wave76 adjusted specificity rows:

{markdown_table(w76.head(8))}

## Secondary Pharmacodynamic / Small Response Contexts

{markdown_table(pharmaco.head(20))}

## Interpretation

Tissue-level anti-TNF datasets provide the only plausible stratification signal.
Peripheral blood and small non-anti-TNF contexts do not cleanly replicate it.
Any downstream claim must therefore be restricted to tissue-resident inflammatory
myeloid/APC states and cannot be generalized to a blood biomarker or a direct
MS target from these data.

## Outputs

- `stratification_context_tests.tsv`
- `module_stratification_summary.tsv`
- `secondary_pharmacodynamic_or_small_response_contexts.tsv`
- `summary.json`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
