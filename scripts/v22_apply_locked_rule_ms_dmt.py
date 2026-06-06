#!/usr/bin/env python3
"""Apply LOCKED_RULE_V22 to local held-out MS DMT cohorts.

This script deliberately fits no model. It consumes local GSE235357 and
GSE250453 files that pre-date V22 but were not used in the V6/V7 APC/HLA-II
derivation or validation exclusions.
"""

from __future__ import annotations

import gzip
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "wave96_ms_treatment"
OUT = ROOT / "analysis" / "v22_locked_apc_hla_validation"
SEED = 20260606

IFN_APC = ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"]
HLAII = ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"]
RECEPTOR = ["CD74", "CD44", "CXCR4"]


@dataclass
class Dataset:
    accession: str
    therapy: str
    expression: pd.DataFrame
    metadata: pd.DataFrame
    notes: str


def read_gzip_text(path: Path) -> str:
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
        return handle.read()


def parse_sample_titles(series_matrix: Path) -> list[str]:
    text = read_gzip_text(series_matrix)
    for line in text.splitlines():
        if line.startswith("!Sample_title"):
            return [x.strip().strip('"') for x in line.split("\t")[1:]]
    raise ValueError(f"No !Sample_title in {series_matrix}")


def gse235_metadata() -> pd.DataFrame:
    titles = parse_sample_titles(RAW / "GSE235357_series_matrix.txt.gz")
    rows = []
    for i, title in enumerate(titles, start=1):
        sample = f"SM002604_{i}"
        title_lower = title.lower()
        if title_lower.startswith("healthy") or title_lower.startswith("helathy") or "donor" in title_lower:
            rows.append(
                {
                    "sample": sample,
                    "title": title,
                    "disease": "healthy",
                    "response": "healthy",
                    "timepoint": "single",
                    "patient": re.sub(r"\D+", "", title) or str(i),
                }
            )
            continue
        response = "Responder" if "Responder" in title and "Non-responder" not in title else "Non-responder"
        timepoint = "baseline" if "Baseline" in title else "treated"
        patient_match = re.search(r"(Responder|Non-responder) (\d+)", title)
        patient = f"{response}_{patient_match.group(2)}" if patient_match else title
        rows.append(
            {
                "sample": sample,
                "title": title,
                "disease": "MS",
                "response": response,
                "timepoint": timepoint,
                "patient": patient,
            }
        )
    return pd.DataFrame(rows)


def load_gse235() -> Dataset:
    expr_path = RAW / "GSE235357_normalized_annotated.csv.gz"
    df = pd.read_csv(expr_path, compression="gzip", low_memory=False)
    sample_cols = [c for c in df.columns if c.startswith("SM002604_")]
    expr = df[["SYMBOL"] + sample_cols].dropna(subset=["SYMBOL"]).copy()
    expr = expr.groupby("SYMBOL", as_index=True)[sample_cols].mean()
    expr = np.log2(expr.astype(float) + 1.0)
    return Dataset(
        accession="GSE235357",
        therapy="dimethyl_fumarate",
        expression=expr,
        metadata=gse235_metadata(),
        notes="PBMC paired baseline/treated; 5 responders and 5 nonresponders; local V3 cache.",
    )


def build_symbol_map() -> dict[str, str]:
    df = pd.read_csv(
        RAW / "GSE235357_normalized_annotated.csv.gz",
        compression="gzip",
        usecols=["Row.names", "SYMBOL"],
        low_memory=False,
    )
    return dict(zip(df["Row.names"].astype(str), df["SYMBOL"].astype(str)))


def load_gse250(symbol_map: dict[str, str]) -> Dataset:
    expr_path = RAW / "GSE250453_fingo_RNAseq_all.tsv.gz"
    df = pd.read_csv(expr_path, sep="\t", compression="gzip", low_memory=False)
    sample_cols = [c for c in df.columns if c != "ensembl_gene_id"]
    df["SYMBOL"] = df["ensembl_gene_id"].map(symbol_map)
    expr = df.dropna(subset=["SYMBOL"])[["SYMBOL"] + sample_cols].copy()
    expr = expr.groupby("SYMBOL", as_index=True)[sample_cols].sum()
    counts = expr.astype(float)
    lib = counts.sum(axis=0).replace(0, np.nan)
    expr = np.log2(counts.div(lib, axis=1) * 1_000_000.0 + 1.0)
    rows = []
    for sample in sample_cols:
        normalized = sample.replace("Res4", "R_4")
        response = "Responder" if normalized.startswith("R_") else "Non-responder"
        timepoint = "baseline" if "basal" in normalized else "treated"
        match = re.search(r"^(NR|R)_(?:basal|treat)_(\d+)$", normalized)
        patient = f"{match.group(1)}_{match.group(2)}" if match else normalized.replace("_basal", "").replace("_treat", "")
        rows.append(
            {
                "sample": sample,
                "title": sample,
                "disease": "MS",
                "response": response,
                "timepoint": timepoint,
                "patient": patient,
            }
        )
    return Dataset(
        accession="GSE250453",
        therapy="fingolimod",
        expression=expr,
        metadata=pd.DataFrame(rows),
        notes="PBMC paired baseline/treated; 5 responders and 5 nonresponders; local V3 cache.",
    )


def zscore_modules(ds: Dataset) -> tuple[pd.DataFrame, dict[str, list[str]]]:
    ms_samples = ds.metadata.loc[ds.metadata["disease"].eq("MS"), "sample"].tolist()
    mat = ds.expression[[s for s in ms_samples if s in ds.expression.columns]].copy()
    z = mat.sub(mat.mean(axis=1), axis=0).div(mat.std(axis=1).replace(0, np.nan), axis=0)
    modules = {"IFN_APC": IFN_APC, "HLAII": HLAII, "RECEPTOR": RECEPTOR}
    present: dict[str, list[str]] = {}
    scores = pd.DataFrame(index=z.columns)
    for name, genes in modules.items():
        genes_present = [g for g in genes if g in z.index]
        present[name] = genes_present
        if len(genes_present) / len(genes) < 0.5:
            scores[name] = np.nan
        else:
            scores[name] = z.loc[genes_present].mean(axis=0)
    return scores, present


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
    correction = 1.0 - (3.0 / (4.0 * (len(a) + len(b)) - 9.0))
    return float(((np.mean(a) - np.mean(b)) / pooled) * correction)


def bootstrap_auc_ci(scores: np.ndarray, y: np.ndarray, n_boot: int = 2000) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    aucs = []
    idx = np.arange(len(scores))
    for _ in range(n_boot):
        sample = rng.choice(idx, size=len(idx), replace=True)
        if len(set(y[sample].tolist())) < 2:
            continue
        aucs.append(auc_score(scores[sample], y[sample]))
    if not aucs:
        return math.nan, math.nan
    return float(np.percentile(aucs, 2.5)), float(np.percentile(aucs, 97.5))


def evaluate(ds: Dataset) -> tuple[dict[str, object], pd.DataFrame]:
    scores, present = zscore_modules(ds)
    rows = []
    paired = []
    for patient, sub in ds.metadata[ds.metadata["disease"].eq("MS")].groupby("patient"):
        if not {"baseline", "treated"}.issubset(set(sub["timepoint"])):
            continue
        b = sub[sub["timepoint"].eq("baseline")]["sample"].iloc[0]
        t = sub[sub["timepoint"].eq("treated")]["sample"].iloc[0]
        if b not in scores.index or t not in scores.index:
            continue
        delta_ifn = float(scores.loc[t, "IFN_APC"] - scores.loc[b, "IFN_APC"])
        delta_hla = float(scores.loc[t, "HLAII"] - scores.loc[b, "HLAII"])
        delta_rec = float(scores.loc[t, "RECEPTOR"] - scores.loc[b, "RECEPTOR"])
        signed = delta_hla - delta_ifn
        receptor_signed = delta_rec
        response = sub["response"].iloc[0]
        paired.append(
            {
                "cohort": ds.accession,
                "patient": patient,
                "response": response,
                "baseline_sample": b,
                "treated_sample": t,
                "delta_IFN_APC": delta_ifn,
                "delta_HLAII": delta_hla,
                "locked_signed_score": signed,
                "delta_RECEPTOR": receptor_signed,
            }
        )
    paired_df = pd.DataFrame(paired)
    if paired_df.empty:
        raise ValueError(f"No paired subjects for {ds.accession}")
    y = paired_df["response"].eq("Responder").astype(int).to_numpy()
    signed_scores = paired_df["locked_signed_score"].to_numpy(dtype=float)
    receptor_scores = paired_df["delta_RECEPTOR"].to_numpy(dtype=float)
    auc = auc_score(signed_scores, y)
    receptor_auc = auc_score(receptor_scores, y)
    ci_low, ci_high = bootstrap_auc_ci(signed_scores, y)
    r_scores = paired_df.loc[paired_df["response"].eq("Responder"), "locked_signed_score"].tolist()
    nr_scores = paired_df.loc[paired_df["response"].eq("Non-responder"), "locked_signed_score"].tolist()
    g = hedges_g(r_scores, nr_scores)
    p = float(stats.ttest_ind(r_scores, nr_scores, equal_var=False).pvalue) if len(r_scores) >= 2 and len(nr_scores) >= 2 else math.nan
    n = int(len(paired_df))
    pass_fail = "pass" if auc >= 0.70 and g >= 0.50 and (n < 30 or ci_low > 0.55) else "fail"
    specificity = "non_specific" if np.isfinite(receptor_auc) and receptor_auc - auc >= 0.10 else "specificity_ok"
    result = {
        "cohort": ds.accession,
        "disease": "MS",
        "therapy": ds.therapy,
        "therapy_class": "Class C",
        "n_labeled": n,
        "n_responders": int(y.sum()),
        "n_nonresponders": int(n - y.sum()),
        "feature_applied": "delta_HLAII - delta_IFN_APC",
        "auc": auc,
        "auc_ci_low": ci_low,
        "auc_ci_high": ci_high,
        "hedges_g": g,
        "welch_p": p,
        "receptor_auc": receptor_auc,
        "receptor_auc_delta": receptor_auc - auc if np.isfinite(receptor_auc) and np.isfinite(auc) else math.nan,
        "pass_fail": pass_fail,
        "specificity": specificity,
        "present_IFN_APC": ";".join(present["IFN_APC"]),
        "present_HLAII": ";".join(present["HLAII"]),
        "present_RECEPTOR": ";".join(present["RECEPTOR"]),
        "notes": ds.notes,
    }
    return result, paired_df


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    symbol_map = build_symbol_map()
    datasets = [load_gse235(), load_gse250(symbol_map)]
    ledger_rows = []
    paired_frames = []
    for ds in datasets:
        result, paired = evaluate(ds)
        ledger_rows.append(result)
        paired_frames.append(paired)
    ledger = pd.DataFrame(ledger_rows)
    paired = pd.concat(paired_frames, ignore_index=True)
    ledger.to_csv(OUT / "validation_ledger_v22_ms_dmt.tsv", sep="\t", index=False)
    paired.to_csv(OUT / "paired_locked_scores_v22.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "locked_rule": "docs/locked_rules/LOCKED_RULE_V22.md",
        "n_cohorts": int(len(ledger)),
        "n_pass": int((ledger["pass_fail"] == "pass").sum()),
        "n_fail": int((ledger["pass_fail"] == "fail").sum()),
        "all_reachable_ms_dmt_failed": bool((ledger["pass_fail"] == "fail").all()),
        "cohorts": ledger.to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
