#!/usr/bin/env python3
"""V42 Gafson validation harness and synthetic-data self-test.

This script implements the pre-registered V42 plan around the immutable V22
rule. It can ingest a paired baseline/early-treatment expression matrix and
metadata, compute frozen modules, and run the primary V22 metrics plus the
pre-specified V32 confounder audits. It also generates synthetic null and
planted-signal cohorts to verify the mechanics before any real Gafson data are
available.

No model is fitted for the primary V22 score.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


SEED = 20260606

IFN_APC = ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"]
HLAII = ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"]
RECEPTOR = ["CD74", "CD44", "CXCR4"]

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

ALL_MODULES = {"IFN_APC": IFN_APC, "HLAII": HLAII, "RECEPTOR": RECEPTOR} | GENE_SETS


@dataclass
class ValidationResult:
    paired: pd.DataFrame
    coverage: pd.DataFrame
    metrics: pd.DataFrame
    confounder_metrics: pd.DataFrame
    joint_metrics: pd.DataFrame
    summary: dict[str, object]


def normalize_gene_id(gene: str) -> str:
    gene = str(gene).strip()
    if gene.startswith("ENSG") and "." in gene:
        gene = gene.split(".", 1)[0]
    return gene.upper()


def load_expression(path: Path, expression_type: str) -> pd.DataFrame:
    expr = pd.read_csv(path, sep="\t", index_col=0)
    expr.index = [normalize_gene_id(idx) for idx in expr.index]
    expr = expr.apply(pd.to_numeric, errors="coerce")
    expr = expr.groupby(expr.index).mean()
    if expression_type == "auto":
        non_na = expr.stack(dropna=True)
        looks_counts = (
            len(non_na) > 0
            and (non_na >= 0).all()
            and np.nanmax(non_na.to_numpy(float)) > 50
            and np.nanmean(np.mod(non_na.to_numpy(float), 1) == 0) > 0.95
        )
        expression_type = "raw_counts" if looks_counts else "normalized_log"
    if expression_type == "raw_counts":
        lib = expr.sum(axis=0).replace(0, np.nan)
        expr = np.log2(expr.div(lib, axis=1) * 1_000_000.0 + 1.0)
    elif expression_type != "normalized_log":
        raise ValueError(f"Unknown expression type: {expression_type}")
    return expr


def response_binary(value: object) -> int | None:
    val = str(value).strip().lower()
    if val in {"responder", "response", "yes", "true", "1", "neda", "neda-4", "neda4", "achieved", "maintained", "event-free"}:
        return 1
    if val in {"non-responder", "nonresponder", "no", "false", "0", "not achieved", "disease activity", "active"}:
        return 0
    return None


def select_samples(metadata: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    required = {"sample_id", "patient", "timepoint", "response"}
    missing = required - set(metadata.columns)
    if missing:
        raise ValueError(f"Metadata missing required columns: {sorted(missing)}")
    md = metadata.copy()
    md["sample_id"] = md["sample_id"].astype(str)
    md["patient"] = md["patient"].astype(str)
    md["timepoint_norm"] = md["timepoint"].astype(str).str.lower()
    if "days_since_treatment" not in md.columns:
        md["days_since_treatment"] = np.nan
    md["days_since_treatment"] = pd.to_numeric(md["days_since_treatment"], errors="coerce")
    md["response_binary"] = md["response"].map(response_binary)
    if "qc_pass" in md.columns:
        qc = md["qc_pass"].astype(str).str.lower().isin({"1", "true", "yes", "pass", "passed"})
    else:
        qc = pd.Series(True, index=md.index)
    md = md[qc].copy()

    rows = []
    attrition = []
    for patient, sub in md.groupby("patient", sort=True):
        base = sub[sub["timepoint_norm"].isin({"baseline", "pretreatment", "pre", "w0", "week0", "0"})]
        eligible_post = sub[
            (
                sub["timepoint_norm"].isin({"treated", "post", "on-treatment", "early", "w1", "w2", "w4", "w6", "w8", "w12"})
                | sub["days_since_treatment"].between(1, 84, inclusive="both")
            )
            & ~sub["timepoint_norm"].isin({"baseline", "pretreatment", "pre", "w0", "week0", "0"})
        ].copy()
        eligible_post = eligible_post[
            eligible_post["days_since_treatment"].isna()
            | eligible_post["days_since_treatment"].between(1, 84, inclusive="both")
        ]
        reason = ""
        if base.empty:
            reason = "missing_baseline"
        elif eligible_post.empty:
            reason = "missing_eligible_early_treated"
        elif sub["response_binary"].dropna().empty:
            reason = "missing_mappable_response"
        if reason:
            attrition.append({"patient": patient, "included": False, "reason": reason})
            continue
        b = base.sort_values(["sample_id"]).iloc[0]
        post_sort = eligible_post.assign(
            sort_days=eligible_post["days_since_treatment"].fillna(9999)
        ).sort_values(["sort_days", "sample_id"])
        t = post_sort.iloc[0]
        response_values = sub["response_binary"].dropna().unique()
        if len(response_values) != 1:
            attrition.append({"patient": patient, "included": False, "reason": "ambiguous_response"})
            continue
        rows.append(
            {
                "patient": patient,
                "baseline_sample": b["sample_id"],
                "treated_sample": t["sample_id"],
                "response": "Responder" if int(response_values[0]) == 1 else "Non-responder",
                "response_binary": int(response_values[0]),
                "treated_days_since_treatment": t["days_since_treatment"],
            }
        )
        attrition.append({"patient": patient, "included": True, "reason": "included"})
    return pd.DataFrame(rows), pd.DataFrame(attrition)


def module_scores(expr: pd.DataFrame, selected_samples: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    expr = expr[selected_samples].copy()
    z = expr.sub(expr.mean(axis=1), axis=0).div(expr.std(axis=1).replace(0, np.nan), axis=0)
    score_df = pd.DataFrame(index=selected_samples)
    coverage_rows = []
    for name, genes in ALL_MODULES.items():
        present = [gene for gene in genes if gene in z.index]
        threshold = 0.5 if name in {"IFN_APC", "HLAII", "RECEPTOR"} else 0.4
        frac = len(present) / len(genes)
        coverage_rows.append(
            {
                "module": name,
                "n_genes": len(genes),
                "n_present": len(present),
                "fraction_present": frac,
                "scoreable": frac >= threshold,
                "threshold": threshold,
                "present_genes": ";".join(present),
            }
        )
        score_df[name] = z.loc[present].mean(axis=0) if frac >= threshold else np.nan
    return score_df, pd.DataFrame(coverage_rows)


def build_paired(expr: pd.DataFrame, metadata: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    pairs, attrition = select_samples(metadata)
    samples = sorted(set(pairs["baseline_sample"]).union(set(pairs["treated_sample"])))
    missing_samples = [sample for sample in samples if sample not in expr.columns]
    if missing_samples:
        raise ValueError(f"Expression matrix missing selected metadata samples: {missing_samples[:10]}")
    scores, coverage = module_scores(expr, samples)
    out_rows = []
    for row in pairs.to_dict(orient="records"):
        b = row["baseline_sample"]
        t = row["treated_sample"]
        out = {
            "cohort": "Gafson_DMF_synthetic_or_future",
            "patient": row["patient"],
            "response": row["response"],
            "response_binary": row["response_binary"],
            "baseline_sample": b,
            "treated_sample": t,
            "treated_days_since_treatment": row["treated_days_since_treatment"],
            "therapy_class": "Class C",
        }
        for module in scores.columns:
            out[f"baseline_{module}"] = float(scores.loc[b, module])
            out[f"treated_{module}"] = float(scores.loc[t, module])
            out[f"delta_{module}"] = float(scores.loc[t, module] - scores.loc[b, module])
        out["v22_locked_signed_score"] = out["delta_HLAII"] - out["delta_IFN_APC"]
        out["receptor_only_score"] = out["delta_RECEPTOR"]
        out["baseline_apc_hla_level"] = out["baseline_HLAII"] - out["baseline_IFN_APC"]
        out_rows.append(out)
    paired = pd.DataFrame(out_rows)
    return paired, coverage, attrition


def auc_score(y: np.ndarray, score: np.ndarray) -> float:
    ok = np.isfinite(score) & np.isfinite(y)
    y = y[ok].astype(int)
    score = score[ok].astype(float)
    pos = score[y == 1]
    neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return math.nan
    wins = 0.0
    for value in pos:
        wins += float(np.sum(value > neg))
        wins += 0.5 * float(np.sum(value == neg))
    return wins / (len(pos) * len(neg))


def hedges_g(y: np.ndarray, score: np.ndarray) -> float:
    ok = np.isfinite(score) & np.isfinite(y)
    y = y[ok].astype(int)
    score = score[ok].astype(float)
    a = score[y == 1]
    b = score[y == 0]
    if len(a) < 2 or len(b) < 2:
        return math.nan
    pooled = math.sqrt(((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0:
        return 0.0
    correction = 1 - 3 / (4 * (len(a) + len(b)) - 9)
    return float(((np.mean(a) - np.mean(b)) / pooled) * correction)


def bootstrap_auc_ci(y: np.ndarray, score: np.ndarray, n_boot: int = 2000) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    aucs = []
    idx_all = np.arange(len(y))
    for _ in range(n_boot):
        idx = rng.choice(idx_all, size=len(idx_all), replace=True)
        if len(np.unique(y[idx])) < 2:
            continue
        aucs.append(auc_score(y[idx], score[idx]))
    if not aucs:
        return math.nan, math.nan
    return float(np.percentile(aucs, 2.5)), float(np.percentile(aucs, 97.5))


def permutation_p(y: np.ndarray, score: np.ndarray, observed: float, n_perm: int = 10000) -> float:
    rng = np.random.default_rng(SEED)
    count = 1
    total = 1
    for _ in range(n_perm):
        yp = rng.permutation(y)
        if auc_score(yp, score) >= observed:
            count += 1
        total += 1
    return count / total


def residualize(values: np.ndarray, covariates: pd.DataFrame) -> np.ndarray:
    x = covariates.copy()
    for col in x.columns:
        x[col] = pd.to_numeric(x[col], errors="coerce")
    x = x.replace([np.inf, -np.inf], np.nan)
    x = x.fillna(x.mean(numeric_only=True)).fillna(0.0)
    values = np.asarray(values, dtype=float)
    if not np.isfinite(values).all():
        finite_mean = np.nanmean(np.where(np.isfinite(values), values, np.nan))
        values = np.where(np.isfinite(values), values, finite_mean if np.isfinite(finite_mean) else 0.0)
    design = np.column_stack([np.ones(len(x)), x.to_numpy(float)])
    beta = np.linalg.lstsq(design, values, rcond=None)[0]
    return values - design @ beta


def verdict_from_metrics(n: int, n_resp: int, n_non: int, auc: float, g: float, ci_low: float, receptor_auc: float) -> str:
    if not np.isfinite(auc) or not np.isfinite(g):
        return "UNSCOREABLE_DATA"
    receptor_bad = np.isfinite(receptor_auc) and receptor_auc - auc >= 0.10
    if n >= 30:
        passes = auc >= 0.70 and g >= 0.50 and ci_low > 0.55 and not receptor_bad
    else:
        passes = auc >= 0.70 and g >= 0.50 and not receptor_bad
    if passes and min(n_resp, n_non) < 15:
        return "PASS_PROVISIONAL_SMALL_N"
    if passes:
        return "PASS_CLEAN"
    if receptor_bad and auc >= 0.70:
        return "PASS_NON_SPECIFIC"
    if n >= 30 and min(n_resp, n_non) >= 10 and (auc < 0.60 or g < 0.20):
        return "FAIL_ADEQUATE_POWER"
    if auc < 0.45:
        return "FAIL_ADEQUATE_POWER"
    return "INCONCLUSIVE_UNDERPOWERED"


def adjustment_label(raw_auc: float, adjusted_auc: float) -> str:
    attenuation = raw_auc - adjusted_auc
    if adjusted_auc < 0.65 and attenuation >= 0.10:
        return "EXPLAINED_AWAY"
    if attenuation >= 0.05 or adjusted_auc < 0.70:
        return "ATTENUATES"
    return "SURVIVES"


def primary_metrics(paired: pd.DataFrame) -> pd.DataFrame:
    y = paired["response_binary"].to_numpy(int)
    rows = []
    for feature in ["v22_locked_signed_score", "receptor_only_score"]:
        score = paired[feature].to_numpy(float)
        auc = auc_score(y, score)
        g = hedges_g(y, score)
        ci_low, ci_high = bootstrap_auc_ci(y, score)
        p = permutation_p(y, score, auc)
        rows.append(
            {
                "feature": feature,
                "n": len(paired),
                "n_responders": int(y.sum()),
                "n_nonresponders": int((1 - y).sum()),
                "auc": auc,
                "hedges_g": g,
                "auc_ci_low": ci_low,
                "auc_ci_high": ci_high,
                "permutation_p": p,
            }
        )
    return pd.DataFrame(rows)


def confounder_adjustments(paired: pd.DataFrame, raw_auc: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    y = paired["response_binary"].to_numpy(int)
    locked = paired["v22_locked_signed_score"].to_numpy(float)
    features = ["baseline_apc_hla_level"]
    for name in GENE_SETS:
        features.extend([f"baseline_{name}", f"delta_{name}"])
    rows = []
    for feature in features:
        if feature not in paired.columns or paired[feature].notna().sum() < 6 or paired[feature].nunique(dropna=True) <= 1:
            rows.append({"confounder": feature, "verdict": "UNSCOREABLE"})
            continue
        conf = paired[feature].to_numpy(float)
        resid = residualize(locked, pd.DataFrame({feature: conf}))
        adj_auc = auc_score(y, resid)
        if adj_auc < 0.5:
            resid = -resid
            adj_auc = auc_score(y, resid)
        rows.append(
            {
                "confounder": feature,
                "confounder_auc": auc_score(y, conf),
                "spearman_with_locked": float(pd.Series(conf).corr(pd.Series(locked), method="spearman")),
                "adjusted_auc": adj_auc,
                "adjusted_hedges_g": hedges_g(y, resid),
                "adjusted_auc_ci_low": bootstrap_auc_ci(y, resid)[0],
                "adjusted_auc_ci_high": bootstrap_auc_ci(y, resid)[1],
                "adjusted_permutation_p": permutation_p(y, resid, adj_auc),
                "auc_attenuation": raw_auc - adj_auc,
                "verdict": adjustment_label(raw_auc, adj_auc),
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
    joint_rows = []
    for label, candidates in risk_sets.items():
        keep = [
            feature
            for feature in candidates
            if feature in paired.columns and paired[feature].notna().sum() >= 6 and paired[feature].nunique(dropna=True) > 1
        ]
        if not keep:
            joint_rows.append({"risk_set": label, "verdict": "UNSCOREABLE", "features": ""})
            continue
        if len(paired) / max(len(keep), 1) < 5:
            joint_rows.append({"risk_set": label, "verdict": "UNDERPOWERED", "features": ";".join(keep)})
            continue
        resid = residualize(locked, paired[keep])
        adj_auc = auc_score(y, resid)
        if adj_auc < 0.5:
            resid = -resid
            adj_auc = auc_score(y, resid)
        ci_low, ci_high = bootstrap_auc_ci(y, resid)
        joint_rows.append(
            {
                "risk_set": label,
                "features": ";".join(keep),
                "adjusted_auc": adj_auc,
                "adjusted_hedges_g": hedges_g(y, resid),
                "adjusted_auc_ci_low": ci_low,
                "adjusted_auc_ci_high": ci_high,
                "adjusted_permutation_p": permutation_p(y, resid, adj_auc),
                "auc_attenuation": raw_auc - adj_auc,
                "verdict": adjustment_label(raw_auc, adj_auc),
            }
        )
    return pd.DataFrame(rows), pd.DataFrame(joint_rows)


def run_validation(expression: Path, metadata: Path, outdir: Path, expression_type: str) -> ValidationResult:
    outdir.mkdir(parents=True, exist_ok=True)
    expr = load_expression(expression, expression_type)
    md = pd.read_csv(metadata, sep="\t")
    paired, coverage, attrition = build_paired(expr, md)
    if paired.empty:
        raise ValueError("No eligible paired subjects after applying fixed selection rules")
    metrics = primary_metrics(paired)
    primary = metrics[metrics["feature"].eq("v22_locked_signed_score")].iloc[0]
    receptor = metrics[metrics["feature"].eq("receptor_only_score")].iloc[0]
    conf, joint = confounder_adjustments(paired, float(primary["auc"]))
    final_verdict = verdict_from_metrics(
        int(primary["n"]),
        int(primary["n_responders"]),
        int(primary["n_nonresponders"]),
        float(primary["auc"]),
        float(primary["hedges_g"]),
        float(primary["auc_ci_low"]),
        float(receptor["auc"]),
    )
    summary = {
        "n": int(primary["n"]),
        "n_responders": int(primary["n_responders"]),
        "n_nonresponders": int(primary["n_nonresponders"]),
        "primary_auc": float(primary["auc"]),
        "primary_hedges_g": float(primary["hedges_g"]),
        "primary_auc_ci_low": float(primary["auc_ci_low"]),
        "primary_auc_ci_high": float(primary["auc_ci_high"]),
        "receptor_auc": float(receptor["auc"]),
        "final_verdict": final_verdict,
        "seed": SEED,
    }
    paired.to_csv(outdir / "paired_module_deltas.tsv", sep="\t", index=False)
    coverage.to_csv(outdir / "gene_mapping_coverage.tsv", sep="\t", index=False)
    attrition.to_csv(outdir / "sample_attrition.tsv", sep="\t", index=False)
    metrics.to_csv(outdir / "locked_rule_metrics.tsv", sep="\t", index=False)
    conf.to_csv(outdir / "confounder_adjustment_metrics.tsv", sep="\t", index=False)
    joint.to_csv(outdir / "joint_confounder_metrics.tsv", sep="\t", index=False)
    (outdir / "validation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    return ValidationResult(paired, coverage, metrics, conf, joint, summary)


def synthetic_inputs(outdir: Path, mode: str, n_subjects: int = 60) -> tuple[Path, Path]:
    rng = np.random.default_rng(SEED + (1 if mode == "planted" else 0))
    genes = sorted(set(sum(ALL_MODULES.values(), []) + [f"CONTROL{i}" for i in range(1, 31)]))
    patients = [f"S{i:03d}" for i in range(n_subjects)]
    labels = np.array([1] * (n_subjects // 2) + [0] * (n_subjects - n_subjects // 2))
    rng.shuffle(labels)
    samples = []
    meta_rows = []
    expression_columns = {}
    base_gene_mean = {gene: rng.normal(8.0, 0.5) for gene in genes}
    for patient, label in zip(patients, labels):
        for timepoint, day in [("baseline", 0), ("treated", 56)]:
            sample = f"{patient}_{timepoint}"
            samples.append(sample)
            meta_rows.append(
                {
                    "sample_id": sample,
                    "patient": patient,
                    "timepoint": timepoint,
                    "days_since_treatment": day,
                    "response": "Responder" if label == 1 else "Non-responder",
                    "qc_pass": "pass",
                }
            )
            values = []
            for gene in genes:
                value = base_gene_mean[gene] + rng.normal(0, 0.35)
                if timepoint == "treated":
                    if mode == "planted":
                        if gene in HLAII and label == 1:
                            value += 1.35
                        if gene in HLAII and label == 0:
                            value += 0.05
                        if gene in IFN_APC and gene not in HLAII and label == 1:
                            value -= 0.35
                        if gene in IFN_APC and gene not in HLAII and label == 0:
                            value += 0.25
                    else:
                        if gene in HLAII:
                            value += rng.normal(0.15, 0.12)
                        if gene in IFN_APC and gene not in HLAII:
                            value += rng.normal(0.05, 0.12)
                    if gene in GENE_SETS["glucocorticoid_response"]:
                        value += rng.normal(0.1, 0.2)
                    if gene in GENE_SETS["glycolysis"]:
                        value += rng.normal(0.05, 0.15)
                values.append(value)
            expression_columns[sample] = values
    outdir.mkdir(parents=True, exist_ok=True)
    expr_path = outdir / "synthetic_expression.tsv"
    meta_path = outdir / "synthetic_metadata.tsv"
    expr = pd.DataFrame(expression_columns, index=genes)
    expr.to_csv(expr_path, sep="\t")
    pd.DataFrame(meta_rows).to_csv(meta_path, sep="\t", index=False)
    return expr_path, meta_path


def write_synthetic_report(outdir: Path, null_result: ValidationResult, planted_result: ValidationResult) -> None:
    lines = [
        "# V42 Synthetic Harness Validation",
        "",
        "These data are synthetic and were generated only to test the frozen validation mechanics.",
        "",
        "| Scenario | Expected | Verdict | AUC | Hedges g | Receptor AUC |",
        "|---|---|---|---:|---:|---:|",
    ]
    for name, expected, result in [
        ("null", "must not pass", null_result),
        ("planted", "must pass", planted_result),
    ]:
        summary = result.summary
        lines.append(
            f"| {name} | {expected} | `{summary['final_verdict']}` | "
            f"{summary['primary_auc']:.3f} | {summary['primary_hedges_g']:.3f} | {summary['receptor_auc']:.3f} |"
        )
    lines.extend(
        [
            "",
            "Pass criteria for this harness self-test:",
            "",
            "- null synthetic cohort final verdict is not `PASS_CLEAN` or `PASS_PROVISIONAL_SMALL_N`;",
            "- planted synthetic cohort final verdict is `PASS_CLEAN`;",
            "- both cohorts write the same core artifacts expected from a future Gafson run.",
        ]
    )
    (outdir / "README.md").write_text("\n".join(lines) + "\n")


def cmd_run(args: argparse.Namespace) -> int:
    result = run_validation(Path(args.expression), Path(args.metadata), Path(args.outdir), args.expression_type)
    print(json.dumps(result.summary, indent=2, sort_keys=True))
    return 0


def cmd_synthetic_check(args: argparse.Namespace) -> int:
    outdir = Path(args.outdir)
    null_expr, null_meta = synthetic_inputs(outdir / "null_inputs", "null")
    planted_expr, planted_meta = synthetic_inputs(outdir / "planted_inputs", "planted")
    null_result = run_validation(null_expr, null_meta, outdir / "null_result", "normalized_log")
    planted_result = run_validation(planted_expr, planted_meta, outdir / "planted_result", "normalized_log")
    write_synthetic_report(outdir, null_result, planted_result)
    null_ok = null_result.summary["final_verdict"] not in {"PASS_CLEAN", "PASS_PROVISIONAL_SMALL_N"}
    planted_ok = planted_result.summary["final_verdict"] == "PASS_CLEAN"
    summary = {
        "null_expected_fail": bool(null_ok),
        "null_verdict": null_result.summary["final_verdict"],
        "null_auc": null_result.summary["primary_auc"],
        "planted_expected_pass": bool(planted_ok),
        "planted_verdict": planted_result.summary["final_verdict"],
        "planted_auc": planted_result.summary["primary_auc"],
    }
    (outdir / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if null_ok and planted_ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run frozen validation on expression and metadata")
    run.add_argument("--expression", required=True, help="gene x sample TSV")
    run.add_argument("--metadata", required=True, help="sample metadata TSV")
    run.add_argument("--outdir", required=True)
    run.add_argument("--expression-type", choices=["auto", "raw_counts", "normalized_log"], default="auto")
    run.set_defaults(func=cmd_run)

    synthetic = sub.add_parser("synthetic-check", help="Generate null and planted synthetic cohorts and validate harness")
    synthetic.add_argument("--outdir", default="analysis/v42_harness_validation")
    synthetic.set_defaults(func=cmd_synthetic_check)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
