#!/usr/bin/env python3
"""V32 confounder audit for the immutable V22 APC/HLA-II scalar.

This script does not edit or refit LOCKED_RULE_V22. It recomputes the bounded
V22/V23 cohorts, scores frozen confounder panels, and tests whether the locked
signed score survives residualization against each confounder plus cohort.
"""

from __future__ import annotations

import gzip
import json
import math
import re
import warnings
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import io, stats
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

import v22_apply_locked_rule_ms_dmt as ms_dmt
import v23_rescore_gse253006_exact_locked as tof_exact


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v32_confounder_audit"
SEED = 32032

warnings.filterwarnings(
    "ignore",
    message="Skipping features without any observed values",
    category=UserWarning,
    module="sklearn.impute._base",
)

IFN_APC = ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"]
HLAII = ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"]

GENE_SETS: dict[str, list[str]] = {
    "glycolysis": [
        "HK1",
        "HK2",
        "GPI",
        "PFKP",
        "PFKM",
        "ALDOA",
        "GAPDH",
        "PGK1",
        "PGAM1",
        "ENO1",
        "PKM",
        "LDHA",
        "SLC2A1",
        "PFKFB3",
    ],
    "oxphos": [
        "NDUFA1",
        "NDUFA2",
        "NDUFA9",
        "NDUFB8",
        "SDHA",
        "SDHB",
        "UQCRC1",
        "UQCRC2",
        "COX4I1",
        "COX5A",
        "ATP5F1A",
        "ATP5F1B",
        "ATP5MC1",
    ],
    "immunometabolism_hif_nampt": [
        "NAMPT",
        "HIF1A",
        "SLC2A1",
        "LDHA",
        "PFKFB3",
        "ENO1",
        "HK2",
        "VEGFA",
        "BNIP3",
        "NDRG1",
    ],
    "glucocorticoid_response": [
        "FKBP5",
        "TSC22D3",
        "DUSP1",
        "KLF9",
        "ZBTB16",
        "PER1",
        "SGK1",
        "NFKBIA",
        "GILZ",
        "SOCS1",
    ],
    "general_inflammatory_tone": [
        "IL1B",
        "TNF",
        "IL6",
        "CXCL8",
        "CCL2",
        "NFKB1",
        "NFKBIA",
        "PTGS2",
        "ICAM1",
        "JUN",
        "FOS",
    ],
    "ifn_suppression_inverse_isg": [
        "ISG15",
        "IFI6",
        "IFI44L",
        "MX1",
        "OAS1",
        "OAS2",
        "IFIT1",
        "IFIT3",
        "RSAD2",
        "CXCL10",
    ],
    "stat1_axis": [
        "STAT1",
        "IRF1",
        "GBP1",
        "GBP2",
        "CXCL10",
        "IDO1",
        "TAP1",
        "PSMB9",
        "WARS1",
    ],
    "proliferation": [
        "MKI67",
        "TOP2A",
        "PCNA",
        "MCM2",
        "MCM5",
        "TYMS",
        "UBE2C",
        "BIRC5",
        "CDK1",
        "CCNB1",
    ],
    "monocyte_myeloid_composition": [
        "LYZ",
        "LST1",
        "S100A8",
        "S100A9",
        "FCGR3A",
        "MS4A7",
        "CD14",
        "CTSS",
        "CST3",
    ],
    "t_cell_composition": ["CD3D", "CD3E", "TRAC", "CD4", "CD8A", "IL7R", "CCR7", "NKG7"],
    "b_cell_composition": ["MS4A1", "CD79A", "CD79B", "CD74", "BANK1", "CD19"],
}


@dataclass
class CohortData:
    cohort: str
    expression: pd.DataFrame
    metadata: pd.DataFrame
    therapy_class: str


def auc_score(scores: np.ndarray, y: np.ndarray) -> float:
    ok = np.isfinite(scores)
    scores = scores[ok]
    y = y[ok]
    if len(set(y.tolist())) < 2:
        return math.nan
    ranks = pd.Series(scores).rank(method="average").to_numpy()
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def signed_auc(scores: np.ndarray, y: np.ndarray) -> tuple[float, int]:
    auc = auc_score(scores, y)
    if not np.isfinite(auc):
        return math.nan, 1
    if auc < 0.5:
        return 1.0 - auc, -1
    return auc, 1


def hedges_g(scores: np.ndarray, y: np.ndarray) -> float:
    ok = np.isfinite(scores)
    scores = scores[ok]
    y = y[ok]
    a = scores[y == 1]
    b = scores[y == 0]
    if len(a) < 2 or len(b) < 2:
        return math.nan
    pooled = math.sqrt(((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0:
        return 0.0
    return float(((np.mean(a) - np.mean(b)) / pooled) * (1 - 3 / (4 * (len(a) + len(b)) - 9)))


def module_scores(expr: pd.DataFrame, gene_sets: dict[str, list[str]]) -> tuple[pd.DataFrame, list[dict[str, object]]]:
    z = expr.sub(expr.mean(axis=1), axis=0).div(expr.std(axis=1).replace(0, np.nan), axis=0)
    scores = pd.DataFrame(index=expr.columns)
    coverage = []
    for name, genes in gene_sets.items():
        present = [g for g in genes if g in z.index]
        coverage.append(
            {
                "module": name,
                "n_genes": len(genes),
                "n_present": len(present),
                "fraction_present": len(present) / len(genes),
                "present_genes": ";".join(present),
            }
        )
        if len(present) / len(genes) >= 0.4:
            scores[name] = z.loc[present].mean(axis=0)
        else:
            scores[name] = np.nan
    return scores, coverage


def load_gse235() -> CohortData:
    ds = ms_dmt.load_gse235()
    md = ds.metadata[ds.metadata["disease"].eq("MS")].copy()
    samples = [s for s in md["sample"] if s in ds.expression.columns]
    return CohortData("GSE235357", ds.expression[samples].copy(), md, "Class C")


def parse_gse253006_metadata() -> pd.DataFrame:
    return tof_exact.parse_soft_metadata()


def read_features(prefix: str) -> pd.DataFrame:
    rows = []
    with gzip.open(tof_exact.MATRIX_DIR / f"{prefix}_features.tsv.gz", "rt") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                rows.append((parts[0], parts[1]))
    return pd.DataFrame(rows, columns=["gene_id", "gene_symbol"])


def gse253006_sample_gene_means(prefix: str, target_genes: set[str]) -> dict[str, float | str | int]:
    features = read_features(prefix)
    gene_to_idx = {}
    for i, gene in enumerate(features["gene_symbol"].astype(str)):
        if gene in target_genes and gene not in gene_to_idx:
            gene_to_idx[gene] = i
    mat = io.mmread(str(tof_exact.MATRIX_DIR / f"{prefix}_matrix.mtx.gz")).tocsr().astype(float)
    if mat.shape[0] != len(features) and mat.shape[1] == len(features):
        mat = mat.T.tocsr()
    lib = np.asarray(mat.sum(axis=0)).ravel()
    valid = np.isfinite(lib) & (lib > 0)
    lib_safe = lib.copy()
    lib_safe[~valid] = np.nan
    out: dict[str, float | str | int] = {"sample_prefix": prefix, "n_cells": int(valid.sum())}
    for gene in sorted(target_genes):
        if gene not in gene_to_idx:
            out[gene] = math.nan
            continue
        vals = np.asarray(mat[gene_to_idx[gene], :].todense()).ravel()
        norm = np.divide(vals, lib_safe, out=np.zeros_like(vals, dtype=float), where=np.isfinite(lib_safe)) * 1e4
        log_norm = np.log1p(norm[valid])
        out[gene] = float(np.mean(log_norm)) if log_norm.size else math.nan
    return out


def load_gse253006() -> CohortData:
    target = set(IFN_APC + HLAII)
    for genes in GENE_SETS.values():
        target.update(genes)
    meta = parse_gse253006_metadata()
    rows = [gse253006_sample_gene_means(prefix, target) for prefix in meta["sample_prefix"]]
    gene_df = pd.DataFrame(rows).merge(meta, on="sample_prefix", how="left")
    expr = gene_df.set_index("gsm")[sorted(target)].T
    md = gene_df.rename(columns={"gsm": "sample"}).copy()
    md["response"] = np.where(md["responder"], "Responder", "Non-responder")
    md["timepoint"] = np.where(md["timepoint_norm"].eq("W0"), "baseline", "treated")
    order = {"W0": 0, "W8": 8, "W16": 16, "W24": 24, "W48": 48}
    md["_order"] = md["timepoint_norm"].map(order)
    # Keep baseline and earliest post-treatment per patient, matching V23 exact.
    keep = []
    for _patient, sub in md.groupby("patient"):
        base = sub[sub["timepoint_norm"].eq("W0")]
        post = sub[sub["timepoint_norm"].isin(["W8", "W16", "W24", "W48"])]
        if base.empty or post.empty:
            continue
        keep.append(base.sort_values("sample").iloc[0]["sample"])
        keep.append(post.sort_values("_order").iloc[0]["sample"])
    md = md[md["sample"].isin(keep)].copy()
    expr = expr[[s for s in md["sample"] if s in expr.columns]]
    return CohortData("GSE253006_TOF_exact", expr, md, "Class A")


def signed_score(therapy_class: str, ifn: float, hla: float) -> float:
    if therapy_class == "Class A":
        return -ifn
    if therapy_class == "Class C":
        return hla - ifn
    return hla


def pair_cohort(cohort: CohortData) -> tuple[pd.DataFrame, pd.DataFrame]:
    gene_sets = {"IFN_APC": IFN_APC, "HLAII": HLAII} | GENE_SETS
    scores, coverage = module_scores(cohort.expression, gene_sets)
    rows = []
    for patient, sub in cohort.metadata.groupby("patient"):
        if not {"baseline", "treated"}.issubset(set(sub["timepoint"])):
            continue
        b = sub[sub["timepoint"].eq("baseline")].sort_values("sample").iloc[0]
        if cohort.cohort == "GSE253006_TOF_exact":
            t = sub[sub["timepoint"].eq("treated")].sort_values("_order").iloc[0]
        else:
            t = sub[sub["timepoint"].eq("treated")].sort_values("sample").iloc[0]
        if b["sample"] not in scores.index or t["sample"] not in scores.index:
            continue
        row = {
            "cohort": cohort.cohort,
            "patient": patient,
            "response": b["response"],
            "baseline_sample": b["sample"],
            "treated_sample": t["sample"],
        }
        for mod in scores.columns:
            base = float(scores.loc[b["sample"], mod])
            post = float(scores.loc[t["sample"], mod])
            row[f"baseline_{mod}"] = base
            row[f"delta_{mod}"] = post - base
        row["locked_signed_score"] = signed_score(
            cohort.therapy_class, row["delta_IFN_APC"], row["delta_HLAII"]
        )
        row["baseline_apc_hla_level"] = signed_score(
            cohort.therapy_class, row["baseline_IFN_APC"], row["baseline_HLAII"]
        )
        rows.append(row)
    cov = pd.DataFrame(coverage)
    cov.insert(0, "cohort", cohort.cohort)
    return pd.DataFrame(rows), cov


def residualize(values: np.ndarray, covariates: pd.DataFrame) -> np.ndarray:
    x = covariates.copy()
    for col in x.columns:
        x[col] = pd.to_numeric(x[col], errors="coerce")
    x = x.fillna(x.mean(numeric_only=True))
    design = np.column_stack([np.ones(len(x)), x.to_numpy(float)])
    beta = np.linalg.pinv(design) @ values
    return values - design @ beta


def bootstrap_ci(scores: np.ndarray, y: np.ndarray, cohorts: np.ndarray, n_boot: int = 2000) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    aucs = []
    for _ in range(n_boot):
        idx = []
        for cohort in np.unique(cohorts):
            where = np.where(cohorts == cohort)[0]
            idx.extend(rng.choice(where, size=len(where), replace=True).tolist())
        idx = np.asarray(idx)
        if len(set(y[idx].tolist())) < 2:
            continue
        aucs.append(auc_score(scores[idx], y[idx]))
    if not aucs:
        return math.nan, math.nan
    return float(np.percentile(aucs, 2.5)), float(np.percentile(aucs, 97.5))


def stratified_permutation_p(scores: np.ndarray, y: np.ndarray, cohorts: np.ndarray, observed_auc: float, n_perm: int = 2000) -> float:
    rng = np.random.default_rng(SEED)
    count = 1
    total = 1
    for _ in range(n_perm):
        yp = y.copy()
        for cohort in np.unique(cohorts):
            where = np.where(cohorts == cohort)[0]
            yp[where] = rng.permutation(yp[where])
        if auc_score(scores, yp) >= observed_auc:
            count += 1
        total += 1
    return count / total


def loocv_auc(features: pd.DataFrame, y: np.ndarray) -> float:
    x = features.copy()
    for col in x.columns:
        x[col] = pd.to_numeric(x[col], errors="coerce")
    x = x.fillna(x.mean(numeric_only=True))
    x = pd.get_dummies(x, columns=[c for c in x.columns if x[c].dtype == object], drop_first=True)
    probs = np.full(len(x), np.nan)
    for i in range(len(x)):
        train = np.ones(len(x), dtype=bool)
        train[i] = False
        if len(set(y[train].tolist())) < 2:
            continue
        model = make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            LogisticRegression(C=1.0, solver="liblinear", random_state=SEED),
        )
        model.fit(x.iloc[train].to_numpy(float), y[train])
        probs[i] = model.predict_proba(x.iloc[[i]].to_numpy(float))[0, 1]
    return auc_score(probs, y)


def summarize_adjustments(paired: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    y = paired["response"].eq("Responder").astype(int).to_numpy()
    cohorts = paired["cohort"].to_numpy(str)
    raw = paired["locked_signed_score"].to_numpy(float)
    raw_auc = auc_score(raw, y)
    raw_lo, raw_hi = bootstrap_ci(raw, y, cohorts)
    rows = []
    confounder_features = ["baseline_apc_hla_level"]
    for name in GENE_SETS:
        confounder_features.append(f"baseline_{name}")
        confounder_features.append(f"delta_{name}")
    # Remove all-NA/constant features.
    cleaned = []
    for feat in confounder_features:
        if feat in paired.columns and paired[feat].notna().sum() >= 6 and paired[feat].nunique(dropna=True) > 1:
            cleaned.append(feat)
    for feat in cleaned:
        conf = paired[feat].to_numpy(float)
        conf_auc, orientation = signed_auc(conf, y)
        corr = float(pd.Series(raw).corr(pd.Series(conf), method="spearman"))
        design = pd.get_dummies(paired["cohort"], prefix="cohort", drop_first=True)
        design[feat] = conf
        resid = residualize(raw, design)
        # Keep responder-higher orientation.
        if auc_score(resid, y) < 0.5:
            resid = -resid
        adj_auc = auc_score(resid, y)
        lo, hi = bootstrap_ci(resid, y, cohorts)
        perm_p = stratified_permutation_p(resid, y, cohorts, adj_auc)
        attenuation = raw_auc - adj_auc
        if adj_auc < 0.65 and attenuation >= 0.10:
            verdict = "explained_away"
        elif attenuation >= 0.05 or adj_auc < 0.70:
            verdict = "attenuates"
        else:
            verdict = "survives"
        rows.append(
            {
                "confounder": feat,
                "raw_locked_auc": raw_auc,
                "raw_locked_auc_ci_low": raw_lo,
                "raw_locked_auc_ci_high": raw_hi,
                "confounder_auc_oriented": conf_auc,
                "confounder_orientation": orientation,
                "spearman_with_locked": corr,
                "adjusted_locked_auc": adj_auc,
                "adjusted_auc_ci_low": lo,
                "adjusted_auc_ci_high": hi,
                "adjusted_permutation_p": perm_p,
                "loocv_auc_confounder_only": loocv_auc(pd.DataFrame({"confounder": conf, "cohort": paired["cohort"]}), y),
                "loocv_auc_locked_plus_confounder": loocv_auc(
                    pd.DataFrame(
                        {
                            "locked_signed_score": raw,
                            "confounder": conf,
                            "cohort": paired["cohort"],
                        }
                    ),
                    y,
                ),
                "auc_attenuation": attenuation,
                "verdict": verdict,
            }
        )
    metrics = pd.DataFrame(rows).sort_values(["verdict", "auc_attenuation"], ascending=[True, False])
    # Joint adjustment for features that individually attenuate, capped for small n.
    candidates = metrics[metrics["verdict"].isin(["attenuates", "explained_away"])].sort_values("auc_attenuation", ascending=False)["confounder"].head(4).tolist()
    joint_rows = []
    if candidates:
        design = pd.get_dummies(paired["cohort"], prefix="cohort", drop_first=True)
        for feat in candidates:
            design[feat] = paired[feat].to_numpy(float)
        resid = residualize(raw, design)
        if auc_score(resid, y) < 0.5:
            resid = -resid
        adj_auc = auc_score(resid, y)
        lo, hi = bootstrap_ci(resid, y, cohorts)
        perm_p = stratified_permutation_p(resid, y, cohorts, adj_auc)
        attenuation = raw_auc - adj_auc
        if adj_auc < 0.65 and attenuation >= 0.10:
            verdict = "explained_away"
        elif attenuation >= 0.05 or adj_auc < 0.70:
            verdict = "attenuates"
        else:
            verdict = "survives"
        joint_rows.append(
            {
                "features": ";".join(candidates),
                "raw_locked_auc": raw_auc,
                "joint_adjusted_auc": adj_auc,
                "joint_adjusted_auc_ci_low": lo,
                "joint_adjusted_auc_ci_high": hi,
                "joint_adjusted_permutation_p": perm_p,
                "auc_attenuation": attenuation,
                "verdict": verdict,
            }
        )
    risk_sets = {
        "baseline_and_steroid": [
            "baseline_apc_hla_level",
            "baseline_glucocorticoid_response",
            "delta_glucocorticoid_response",
        ],
        "composition": [
            "baseline_monocyte_myeloid_composition",
            "delta_monocyte_myeloid_composition",
            "baseline_t_cell_composition",
            "delta_t_cell_composition",
            "baseline_b_cell_composition",
            "delta_b_cell_composition",
        ],
        "metabolic_inflammatory_stat1": [
            "baseline_glycolysis",
            "delta_glycolysis",
            "baseline_immunometabolism_hif_nampt",
            "delta_immunometabolism_hif_nampt",
            "baseline_general_inflammatory_tone",
            "delta_general_inflammatory_tone",
            "baseline_stat1_axis",
            "delta_stat1_axis",
            "baseline_ifn_suppression_inverse_isg",
            "delta_ifn_suppression_inverse_isg",
        ],
    }
    for label, features in risk_sets.items():
        keep = [f for f in features if f in paired.columns and paired[f].notna().sum() >= 6 and paired[f].nunique(dropna=True) > 1]
        if not keep:
            continue
        design = pd.get_dummies(paired["cohort"], prefix="cohort", drop_first=True)
        for feat in keep:
            design[feat] = paired[feat].to_numpy(float)
        resid = residualize(raw, design)
        if auc_score(resid, y) < 0.5:
            resid = -resid
        adj_auc = auc_score(resid, y)
        lo, hi = bootstrap_ci(resid, y, cohorts)
        perm_p = stratified_permutation_p(resid, y, cohorts, adj_auc)
        attenuation = raw_auc - adj_auc
        if adj_auc < 0.65 and attenuation >= 0.10:
            verdict = "explained_away"
        elif attenuation >= 0.05 or adj_auc < 0.70:
            verdict = "attenuates"
        else:
            verdict = "survives"
        joint_rows.append(
            {
                "features": ";".join(keep),
                "risk_set": label,
                "raw_locked_auc": raw_auc,
                "joint_adjusted_auc": adj_auc,
                "joint_adjusted_auc_ci_low": lo,
                "joint_adjusted_auc_ci_high": hi,
                "joint_adjusted_permutation_p": perm_p,
                "loocv_auc_confounders_only": loocv_auc(pd.concat([paired[keep], paired[["cohort"]]], axis=1), y),
                "loocv_auc_locked_plus_confounders": loocv_auc(
                    pd.concat([paired[["locked_signed_score"] + keep], paired[["cohort"]]], axis=1),
                    y,
                ),
                "auc_attenuation": attenuation,
                "verdict": verdict,
            }
        )
    return metrics, pd.DataFrame(joint_rows)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    cohorts = [load_gse235(), load_gse253006()]
    paired_frames = []
    coverage_frames = []
    for cohort in cohorts:
        paired, coverage = pair_cohort(cohort)
        paired_frames.append(paired)
        coverage_frames.append(coverage)
    paired_all = pd.concat(paired_frames, ignore_index=True, sort=False)
    coverage_all = pd.concat(coverage_frames, ignore_index=True, sort=False)
    metrics, joint = summarize_adjustments(paired_all)
    paired_all.to_csv(OUT / "v32_subject_confounder_scores.tsv", sep="\t", index=False)
    coverage_all.to_csv(OUT / "v32_confounder_gene_coverage.tsv", sep="\t", index=False)
    metrics.to_csv(OUT / "v32_confounder_adjustment_metrics.tsv", sep="\t", index=False)
    joint.to_csv(OUT / "v32_joint_adjustment_metrics.tsv", sep="\t", index=False)
    summary = {
        "seed": SEED,
        "n_subjects": int(len(paired_all)),
        "cohorts": sorted(paired_all["cohort"].unique().tolist()),
        "raw_locked_auc": float(metrics["raw_locked_auc"].iloc[0]) if not metrics.empty else math.nan,
        "panel_counts": metrics["verdict"].value_counts().to_dict() if not metrics.empty else {},
        "joint_verdict": joint.iloc[0].to_dict() if not joint.empty else {},
    }
    (OUT / "v32_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
