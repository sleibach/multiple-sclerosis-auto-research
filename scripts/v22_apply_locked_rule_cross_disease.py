#!/usr/bin/env python3
"""Apply LOCKED_RULE_V22 to local held-out cross-disease dynamic cohorts."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import v3_wave89_psoriasis_gse85034_response_validation as psor  # noqa: E402

OUT = ROOT / "analysis" / "v22_locked_apc_hla_validation"
SEED = 20260606

IFN_APC = ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"]
HLAII = ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"]
RECEPTOR = ["CD74", "CD44", "CXCR4"]


def auc_score(scores: np.ndarray, y: np.ndarray) -> float:
    if len(set(y.tolist())) < 2:
        return math.nan
    ranks = pd.Series(scores).rank(method="average").to_numpy()
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    rank_sum = float(ranks[y == 1].sum())
    return float((rank_sum - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def hedges_g(responder: list[float], nonresponder: list[float]) -> float:
    a = np.asarray([x for x in responder if np.isfinite(x)], dtype=float)
    b = np.asarray([x for x in nonresponder if np.isfinite(x)], dtype=float)
    if len(a) < 2 or len(b) < 2:
        return math.nan
    pooled = math.sqrt(((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0:
        return 0.0
    return float(((np.mean(a) - np.mean(b)) / pooled) * (1.0 - 3.0 / (4.0 * (len(a) + len(b)) - 9.0)))


def bootstrap_auc_ci(scores: np.ndarray, y: np.ndarray, n_boot: int = 2000) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    idx = np.arange(len(scores))
    aucs = []
    for _ in range(n_boot):
        sample = rng.choice(idx, size=len(idx), replace=True)
        if len(set(y[sample].tolist())) < 2:
            continue
        aucs.append(auc_score(scores[sample], y[sample]))
    if not aucs:
        return math.nan, math.nan
    return float(np.percentile(aucs, 2.5)), float(np.percentile(aucs, 97.5))


def summarize(cohort: str, disease: str, therapy: str, n: int, y: np.ndarray, signed: np.ndarray, receptor: np.ndarray, notes: str) -> dict[str, object]:
    auc = auc_score(signed, y)
    rauc = auc_score(receptor, y)
    lo, hi = bootstrap_auc_ci(signed, y)
    r = signed[y == 1].tolist()
    nr = signed[y == 0].tolist()
    g = hedges_g(r, nr)
    p = float(stats.ttest_ind(r, nr, equal_var=False).pvalue) if len(r) >= 2 and len(nr) >= 2 else math.nan
    passed = auc >= 0.70 and g >= 0.50 and (n < 30 or lo > 0.55)
    return {
        "cohort": cohort,
        "disease": disease,
        "therapy": therapy,
        "therapy_class": "Class A",
        "n_labeled": n,
        "n_responders": int(y.sum()),
        "n_nonresponders": int(n - y.sum()),
        "feature_applied": "-delta_IFN_APC",
        "auc": auc,
        "auc_ci_low": lo,
        "auc_ci_high": hi,
        "hedges_g": g,
        "welch_p": p,
        "receptor_auc": rauc,
        "receptor_auc_delta": rauc - auc if np.isfinite(rauc) and np.isfinite(auc) else math.nan,
        "pass_fail": "pass" if passed else "fail",
        "validation_scope": "primary_locked",
        "specificity": "non_specific" if np.isfinite(rauc) and rauc - auc >= 0.10 else "specificity_ok",
        "present_IFN_APC": "",
        "present_HLAII": "",
        "present_RECEPTOR": "",
        "notes": notes,
    }


def module_scores(expr: pd.DataFrame, genes: list[str]) -> tuple[pd.Series, list[str]]:
    present = [g for g in genes if g in expr.index]
    if len(present) / len(genes) < 0.5:
        return pd.Series(dtype=float), present
    z = expr.sub(expr.mean(axis=1), axis=0).div(expr.std(axis=1).replace(0, np.nan), axis=0)
    return z.loc[present].mean(axis=0), present


def eval_gse85034() -> tuple[dict[str, object], pd.DataFrame]:
    wanted = set(IFN_APC + HLAII + RECEPTOR)
    metadata, expr_probe = psor.read_series_matrix(psor.SERIES)
    info = psor.sample_metadata(metadata)
    patients = psor.build_patient_response_table(info)
    probe_to_genes, _coverage = psor.read_gpl10558_gene_map(psor.GPL10558_ANNOT, wanted)
    gene_expr = psor.expression_to_gene_level(expr_probe, probe_to_genes)
    ifn, ifn_present = module_scores(gene_expr, IFN_APC)
    hla, hla_present = module_scores(gene_expr, HLAII)
    rec, rec_present = module_scores(gene_expr, RECEPTOR)
    rows = []
    for _, row in patients[patients["treatment"].eq("ADA")].iterrows():
        subject = row["subject_id"]
        base = row["baseline_ls_sample"]
        if not base or not np.isfinite(row["pasi75_wk16"]):
            continue
        wk1 = info[(info["subject_id"].eq(subject)) & (info["timepoint"].eq("WK1"))]["sample"]
        if wk1.empty:
            continue
        wk1_sample = wk1.iloc[0]
        if base not in ifn.index or wk1_sample not in ifn.index:
            continue
        delta_ifn = float(ifn[wk1_sample] - ifn[base])
        delta_hla = float(hla[wk1_sample] - hla[base]) if base in hla.index and wk1_sample in hla.index else math.nan
        delta_rec = float(rec[wk1_sample] - rec[base]) if base in rec.index and wk1_sample in rec.index else math.nan
        rows.append(
            {
                "cohort": "GSE85034_ADA",
                "patient": subject,
                "response": "Responder" if int(row["pasi75_wk16"]) == 1 else "Non-responder",
                "baseline_sample": base,
                "treated_sample": wk1_sample,
                "delta_IFN_APC": delta_ifn,
                "delta_HLAII": delta_hla,
                "locked_signed_score": -delta_ifn,
                "delta_RECEPTOR": -delta_rec,
            }
        )
    df = pd.DataFrame(rows)
    y = df["response"].eq("Responder").astype(int).to_numpy()
    res = summarize(
        "GSE85034_ADA",
        "psoriasis",
        "adalimumab",
        len(df),
        y,
        df["locked_signed_score"].to_numpy(float),
        df["delta_RECEPTOR"].to_numpy(float),
        "Lesional skin baseline to week 1; PASI75 at week 16; adalimumab arm.",
    )
    res["present_IFN_APC"] = ";".join(ifn_present)
    res["present_HLAII"] = ";".join(hla_present)
    res["present_RECEPTOR"] = ";".join(rec_present)
    return res, df


def eval_gse253006() -> tuple[dict[str, object], pd.DataFrame]:
    path = ROOT / "phases/v3/results" / "gse253006_tofacitinib" / "gse253006_sample_target_scores.tsv"
    df = pd.read_csv(path, sep="\t", low_memory=False)
    rows = []
    for patient, sub in df.groupby("patient"):
        b = sub[sub["timepoint_norm"].eq("W0")]
        post = sub[sub["timepoint_norm"].isin(["W8", "W16", "W24", "W48"])].copy()
        if b.empty or post.empty:
            continue
        post["_order"] = post["timepoint_norm"].map({"W8": 8, "W16": 16, "W24": 24, "W48": 48})
        p0 = b.sort_values("gsm").iloc[0]
        p1 = post.sort_values("_order").iloc[0]
        delta_ifn = float(p1["module_ifn_apc"] - p0["module_ifn_apc"])
        delta_hla = float(p1["module_hla_ii_apc"] - p0["module_hla_ii_apc"])
        delta_rec = float(p1["module_mif_cd74_receptor_state"] - p0["module_mif_cd74_receptor_state"])
        rows.append(
            {
                "cohort": "GSE253006_TOF",
                "patient": patient,
                "response": "Responder" if bool(p0["responder"]) else "Non-responder",
                "baseline_sample": p0["gsm"],
                "treated_sample": p1["gsm"],
                "delta_IFN_APC": delta_ifn,
                "delta_HLAII": delta_hla,
                "locked_signed_score": -delta_ifn,
                "delta_RECEPTOR": -delta_rec,
            }
        )
    out = pd.DataFrame(rows)
    y = out["response"].eq("Responder").astype(int).to_numpy()
    res = summarize(
        "GSE253006_TOF",
        "ulcerative_colitis",
        "tofacitinib",
        len(out),
        y,
        out["locked_signed_score"].to_numpy(float),
        out["delta_RECEPTOR"].to_numpy(float),
        "All-cell single-cell sample summaries, baseline to earliest post-treatment; compartment-unresolved weaker evidence.",
    )
    res["validation_scope"] = "exploratory_module_approximation"
    res["present_IFN_APC"] = "STAT1;IRF1;CXCL10;GBP1;CD74;IFI30;HLA-DRA;HLA-DRB1"
    res["present_HLAII"] = "CD74;HLA-DRA;HLA-DRB1;HLA-DPA1;HLA-DPB1;CIITA;RFX5"
    res["present_RECEPTOR"] = "CD74;CD44;CXCR4;HLA-DRA;HLA-DRB1;HLA-DPA1;HLA-DPB1"
    return res, out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    paired = []
    for fn in [eval_gse85034, eval_gse253006]:
        res, df = fn()
        results.append(res)
        paired.append(df)
    ledger = pd.DataFrame(results)
    paired_df = pd.concat(paired, ignore_index=True)
    ledger.to_csv(OUT / "validation_ledger_v22_cross_disease.tsv", sep="\t", index=False)
    paired_df.to_csv(OUT / "paired_locked_scores_v22_cross_disease.tsv", sep="\t", index=False)
    print(json.dumps({"cohorts": results}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
