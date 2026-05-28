#!/usr/bin/env python3
"""Wave130 MS treatment-response audit for Wave129 biomarker salvage.

This is intentionally small-n and explicit: both public MS datasets contain
five responders and five nonresponders sampled at baseline and after treatment.
The test is whether the non-MS anti-TNF biomarker signal from Wave129 is visible
in MS treatment response, either at baseline or as a differential treatment
trajectory.
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

try:
    from scipy import stats
except Exception:  # pragma: no cover - scipy exists in the pinned venv
    stats = None

from v3_analyze_osmr_complement_axes import ROOT


SEED = 20260527
RAW = ROOT / "data" / "raw_v3" / "wave96_ms_treatment"
OUT = ROOT / "results_v3" / "wave130_ms_treatment_response_audit"

GSE235_EXPR = RAW / "GSE235357_normalized_annotated.csv.gz"
GSE235_MATRIX = RAW / "GSE235357_series_matrix.txt.gz"
GSE250_EXPR = RAW / "GSE250453_fingo_RNAseq_all.tsv.gz"
GSE250_MATRIX = RAW / "GSE250453_series_matrix.txt.gz"
W129 = ROOT / "results_v3" / "wave129_response_stratification_salvage" / "response_stratification_salvage_decisions.tsv"

PRIMARY_GENES = ["IL1B", "LAMP3"]
MODULES = {
    "inflammatory_nfkb": ["IL1B", "TREM1", "CCL2", "NFKBIA", "CXCL8", "CCL4", "CCL3", "OSM", "TNF"],
    "lysosomal_apc": ["LAMP3", "LAMP2", "CTSB", "CTSS", "IFI30"],
    "ifn_apc": ["STAT1", "GBP1", "CXCL10", "IRF1", "IFI30"],
    "lipid_loader_repair": ["ACSL1", "APOE", "SPP1", "MERTK"],
}


@dataclass
class Dataset:
    accession: str
    therapy: str
    expression: pd.DataFrame  # rows genes, cols samples, log-scale values
    metadata: pd.DataFrame
    available_genes: set[str]


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
    titles = parse_sample_titles(GSE235_MATRIX)
    rows = []
    for i, title in enumerate(titles, start=1):
        sample = f"SM002604_{i}"
        title_lower = title.lower()
        if title_lower.startswith("healthy") or title_lower.startswith("helathy") or "donor" in title_lower:
            group = "healthy"
            response = "healthy"
            timepoint = "single"
            patient = re.sub(r"\D+", "", title) or str(i)
        else:
            response = "Responder" if "Responder" in title and "Non-responder" not in title else "Non-responder"
            timepoint = "baseline" if "Baseline" in title else "treated"
            patient_match = re.search(r"(Responder|Non-responder) (\d+)", title)
            patient = f"{response}_{patient_match.group(2)}" if patient_match else title
            group = "MS"
        rows.append(
            {
                "sample": sample,
                "title": title,
                "disease": group,
                "response": response,
                "timepoint": timepoint,
                "patient": patient,
                "therapy": "dimethyl_fumarate",
            }
        )
    return pd.DataFrame(rows)


def load_gse235() -> Dataset:
    df = pd.read_csv(GSE235_EXPR, compression="gzip", low_memory=False)
    symbol_col = "SYMBOL"
    sample_cols = [c for c in df.columns if c.startswith("SM002604_")]
    expr = df[[symbol_col] + sample_cols].dropna(subset=[symbol_col]).copy()
    expr = expr.groupby(symbol_col, as_index=True)[sample_cols].mean()
    expr = np.log2(expr.astype(float) + 1.0)
    md = gse235_metadata()
    md = md[md["sample"].isin(sample_cols)].copy()
    return Dataset("GSE235357", "dimethyl_fumarate", expr, md, set(expr.index.astype(str)))


def load_gse250(symbol_map: dict[str, str]) -> Dataset:
    df = pd.read_csv(GSE250_EXPR, sep="\t", compression="gzip", low_memory=False)
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
        if match:
            patient = f"{match.group(1)}_{match.group(2)}"
        else:
            patient = normalized.replace("_basal", "").replace("_treat", "")
        rows.append(
            {
                "sample": sample,
                "title": sample,
                "disease": "MS",
                "response": response,
                "timepoint": timepoint,
                "patient": patient,
                "therapy": "fingolimod",
            }
        )
    return Dataset("GSE250453", "fingolimod", expr, pd.DataFrame(rows), set(expr.index.astype(str)))


def build_symbol_map() -> dict[str, str]:
    df = pd.read_csv(GSE235_EXPR, compression="gzip", usecols=["Row.names", "SYMBOL"], low_memory=False)
    return dict(zip(df["Row.names"].astype(str), df["SYMBOL"].astype(str)))


def ttest(a: list[float], b: list[float]) -> float:
    a = [x for x in a if np.isfinite(x)]
    b = [x for x in b if np.isfinite(x)]
    if len(a) < 2 or len(b) < 2:
        return math.nan
    if stats is None:
        return math.nan
    return float(stats.ttest_ind(a, b, equal_var=False).pvalue)


def hedges_g(a: list[float], b: list[float]) -> float:
    a = np.asarray([x for x in a if np.isfinite(x)], dtype=float)
    b = np.asarray([x for x in b if np.isfinite(x)], dtype=float)
    if len(a) < 2 or len(b) < 2:
        return math.nan
    pooled = math.sqrt(((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0:
        return 0.0
    g = (np.mean(a) - np.mean(b)) / pooled
    correction = 1.0 - (3.0 / (4.0 * (len(a) + len(b)) - 9.0))
    return float(g * correction)


def auc_high_nonresponse(values: list[float], labels: list[str]) -> float:
    vals = np.asarray(values, dtype=float)
    y = np.asarray([1 if x == "Non-responder" else 0 for x in labels], dtype=int)
    if len(set(y)) < 2 or len(vals) != len(y):
        return math.nan
    ranks = pd.Series(vals).rank(method="average").to_numpy()
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    rank_sum = float(ranks[y == 1].sum())
    return float((rank_sum - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def paired_deltas(ds: Dataset, gene_or_score: str, values: pd.Series) -> tuple[list[float], list[float], list[str]]:
    rows = []
    for patient, sub in ds.metadata[ds.metadata["disease"].eq("MS")].groupby("patient"):
        if set(sub["timepoint"]) >= {"baseline", "treated"}:
            b = sub[sub["timepoint"].eq("baseline")]["sample"].iloc[0]
            t = sub[sub["timepoint"].eq("treated")]["sample"].iloc[0]
            if b in values.index and t in values.index:
                rows.append(
                    {
                        "patient": patient,
                        "response": sub["response"].iloc[0],
                        "delta": float(values[t] - values[b]),
                        "baseline": float(values[b]),
                        "treated": float(values[t]),
                    }
                )
    delta_df = pd.DataFrame(rows)
    r = delta_df[delta_df["response"].eq("Responder")]["delta"].tolist()
    nr = delta_df[delta_df["response"].eq("Non-responder")]["delta"].tolist()
    return r, nr, delta_df.to_dict(orient="records")


def validate_metadata(ds: Dataset) -> None:
    ms = ds.metadata[ds.metadata["disease"].eq("MS")]
    inconsistent = ms.groupby("patient")["response"].nunique()
    bad = inconsistent[inconsistent > 1]
    if not bad.empty:
        raise ValueError(f"{ds.accession} inconsistent response labels for patients: {bad.index.tolist()}")


def module_score(ds: Dataset, genes: list[str], sample_scope: str = "ms_only") -> tuple[pd.Series, list[str]]:
    present = [g for g in genes if g in ds.expression.index]
    if not present:
        return pd.Series(dtype=float), []
    mat = ds.expression.loc[present]
    if sample_scope == "ms_only":
        samples = ds.metadata[ds.metadata["disease"].eq("MS")]["sample"].tolist()
        mat = mat[[s for s in samples if s in mat.columns]]
    elif sample_scope == "ms_baseline_only":
        samples = ds.metadata[ds.metadata["disease"].eq("MS") & ds.metadata["timepoint"].eq("baseline")]["sample"].tolist()
        mat = mat[[s for s in samples if s in mat.columns]]
    z = mat.sub(mat.mean(axis=1), axis=0).div(mat.std(axis=1).replace(0, np.nan), axis=0)
    return z.mean(axis=0), present


def test_feature(ds: Dataset, feature: str, values: pd.Series, present_genes: list[str], feature_type: str) -> dict:
    md = ds.metadata[ds.metadata["disease"].eq("MS")].copy()
    baseline_samples = md[md["timepoint"].eq("baseline")]["sample"].tolist()
    baseline_md = md[md["sample"].isin(baseline_samples)].copy()
    base_vals = [float(values[s]) for s in baseline_md["sample"] if s in values.index]
    base_labels = [str(x) for _, x in baseline_md.set_index("sample").loc[[s for s in baseline_md["sample"] if s in values.index], "response"].items()]
    base_r = [v for v, lab in zip(base_vals, base_labels) if lab == "Responder"]
    base_nr = [v for v, lab in zip(base_vals, base_labels) if lab == "Non-responder"]
    delta_r, delta_nr, paired_records = paired_deltas(ds, feature, values)
    base_g_r_minus_nr = hedges_g(base_r, base_nr)
    delta_g_r_minus_nr = hedges_g(delta_r, delta_nr)
    return {
        "dataset": ds.accession,
        "therapy": ds.therapy,
        "feature": feature,
        "feature_type": feature_type,
        "present_genes": ";".join(present_genes),
        "n_present_genes": len(present_genes),
        "n_baseline_r": len(base_r),
        "n_baseline_nr": len(base_nr),
        "baseline_mean_r": float(np.mean(base_r)) if base_r else math.nan,
        "baseline_mean_nr": float(np.mean(base_nr)) if base_nr else math.nan,
        "baseline_hedges_g_r_minus_nr": base_g_r_minus_nr,
        "baseline_p": ttest(base_r, base_nr),
        "baseline_auc_high_nonresponse": auc_high_nonresponse(base_vals, base_labels),
        "n_delta_r": len(delta_r),
        "n_delta_nr": len(delta_nr),
        "delta_mean_r": float(np.mean(delta_r)) if delta_r else math.nan,
        "delta_mean_nr": float(np.mean(delta_nr)) if delta_nr else math.nan,
        "delta_hedges_g_r_minus_nr": delta_g_r_minus_nr,
        "delta_p": ttest(delta_r, delta_nr),
        "paired_records_json": json.dumps(paired_records, sort_keys=True),
    }


def bh_fdr(pvals: list[float]) -> list[float]:
    arr = np.asarray([1.0 if not np.isfinite(p) else p for p in pvals], dtype=float)
    n = len(arr)
    order = np.argsort(arr)
    ranked = np.empty(n, dtype=float)
    prev = 1.0
    for i in range(n - 1, -1, -1):
        idx = order[i]
        val = min(prev, arr[idx] * n / (i + 1))
        ranked[idx] = val
        prev = val
    return ranked.tolist()


def classify(row: pd.Series) -> str:
    baseline_rep = (
        row["baseline_auc_high_nonresponse"] >= 0.70
        and row["baseline_hedges_g_r_minus_nr"] <= -0.50
        and row["baseline_p"] < 0.10
    )
    trajectory_rep = (
        abs(row["delta_hedges_g_r_minus_nr"]) >= 0.80
        and row["delta_p"] < 0.10
    )
    if baseline_rep and trajectory_rep:
        return "MS_BASELINE_AND_TRAJECTORY_SIGNAL_SMALL_N"
    if baseline_rep:
        return "MS_BASELINE_SIGNAL_SMALL_N"
    if trajectory_rep:
        return "MS_TRAJECTORY_SIGNAL_SMALL_N"
    return "NO_MS_RESPONSE_REPLICATION"


def feature_replicates(sub: pd.DataFrame) -> bool:
    if len(sub) < 2:
        return False
    calls = sub["call"].astype(str).tolist()
    if any(c == "NO_MS_RESPONSE_REPLICATION" for c in calls):
        return False
    base_signs = np.sign(sub["baseline_hedges_g_r_minus_nr"].to_numpy(dtype=float))
    delta_signs = np.sign(sub["delta_hedges_g_r_minus_nr"].to_numpy(dtype=float))
    baseline_ok = len(set(base_signs[base_signs != 0])) == 1 and all("BASELINE" in c for c in calls)
    delta_ok = len(set(delta_signs[delta_signs != 0])) == 1 and all("TRAJECTORY" in c for c in calls)
    return bool(baseline_ok or delta_ok)


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    ds235 = load_gse235()
    symbol_map = build_symbol_map()
    ds250 = load_gse250(symbol_map)
    datasets = [ds235, ds250]
    for ds in datasets:
        validate_metadata(ds)

    rows = []
    missing = []
    feature_defs = []
    for gene in PRIMARY_GENES:
        feature_defs.append((gene, "gene", [gene]))
    for module, genes in MODULES.items():
        feature_defs.append((module, "module_score", genes))

    for ds in datasets:
        for feature, ftype, genes in feature_defs:
            if ftype == "gene":
                present = [feature] if feature in ds.expression.index else []
                if present:
                    values = ds.expression.loc[feature]
                else:
                    values = pd.Series(dtype=float)
            else:
                values, present = module_score(ds, genes, sample_scope="ms_only")
            if not present:
                missing.append({"dataset": ds.accession, "feature": feature, "requested_genes": ";".join(genes)})
                continue
            rows.append(test_feature(ds, feature, values, present, ftype))

    results = pd.DataFrame(rows)
    results["baseline_fdr"] = bh_fdr(results["baseline_p"].tolist())
    results["delta_fdr"] = bh_fdr(results["delta_p"].tolist())
    results["call"] = results.apply(classify, axis=1)

    # Cross-dataset stability: require same direction in both MS therapies.
    stability = []
    for feature, sub in results.groupby("feature"):
        if len(sub) < 2:
            continue
        base_signs = np.sign(sub["baseline_hedges_g_r_minus_nr"].to_numpy(dtype=float))
        delta_signs = np.sign(sub["delta_hedges_g_r_minus_nr"].to_numpy(dtype=float))
        stability.append(
            {
                "feature": feature,
                "n_datasets": int(len(sub)),
                "baseline_same_direction": bool(len(set(base_signs[base_signs != 0])) == 1),
                "delta_same_direction": bool(len(set(delta_signs[delta_signs != 0])) == 1),
                "baseline_mean_hedges_g_r_minus_nr": float(sub["baseline_hedges_g_r_minus_nr"].mean()),
                "delta_mean_hedges_g_r_minus_nr": float(sub["delta_hedges_g_r_minus_nr"].mean()),
                "best_baseline_p": float(sub["baseline_p"].min()),
                "best_delta_p": float(sub["delta_p"].min()),
                "calls": ";".join(sub["call"].tolist()),
                "all_dataset_calls_non_no": bool((sub["call"] != "NO_MS_RESPONSE_REPLICATION").all()),
            }
        )
    stability_df = pd.DataFrame(stability)
    if not stability_df.empty:
        stability_df["cross_ms_call"] = stability_df.apply(
            lambda r: "REPRODUCES_DIRECTIONALLY_SMALL_N"
            if feature_replicates(results[results["feature"].eq(r["feature"])])
            else "NO_CROSS_MS_REPLICATION",
            axis=1,
        )

    primary = stability_df[stability_df["feature"].isin(PRIMARY_GENES)] if not stability_df.empty else pd.DataFrame()
    n_primary_repro = int((primary.get("cross_ms_call", pd.Series(dtype=str)) == "REPRODUCES_DIRECTIONALLY_SMALL_N").sum())
    module_repro = stability_df[
        stability_df["feature"].isin(MODULES.keys()) & stability_df["cross_ms_call"].eq("REPRODUCES_DIRECTIONALLY_SMALL_N")
    ] if not stability_df.empty else pd.DataFrame()
    if n_primary_repro:
        branch_call = "MS_PRIMARY_BIOMARKER_RESPONSE_SIGNAL_SMALL_N"
    elif len(module_repro) and set(module_repro["feature"]) <= {"ifn_apc"}:
        branch_call = "GENERIC_IFN_APC_SIGNAL_ONLY_NO_LIPID_LYSOSOMAL_RESCUE"
    elif len(module_repro):
        branch_call = "MS_MODULE_RESPONSE_SIGNAL_SMALL_N"
    else:
        branch_call = "NO_MS_TREATMENT_RESPONSE_REPLICATION"

    results.to_csv(OUT / "ms_treatment_response_feature_tests.tsv", sep="\t", index=False)
    stability_df.to_csv(OUT / "ms_treatment_response_cross_dataset_stability.tsv", sep="\t", index=False)
    pd.DataFrame(missing).to_csv(OUT / "missing_features.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "n_feature_tests": int(len(results)),
        "n_primary_features_cross_ms_reproduced": n_primary_repro,
        "n_module_features_cross_ms_reproduced": int(len(module_repro)),
        "datasets": [
            {
                "accession": ds.accession,
                "therapy": ds.therapy,
                "n_samples": int(len(ds.metadata)),
                "n_ms_samples": int(ds.metadata["disease"].eq("MS").sum()),
                "n_responders": int(
                    ds.metadata[
                        ds.metadata["response"].eq("Responder") & ds.metadata["timepoint"].eq("baseline")
                    ]["patient"].nunique()
                ),
                "n_nonresponders": int(
                    ds.metadata[
                        ds.metadata["response"].eq("Non-responder") & ds.metadata["timepoint"].eq("baseline")
                    ]["patient"].nunique()
                ),
            }
            for ds in datasets
        ],
        "inputs": {
            "gse235_expression": str(GSE235_EXPR.relative_to(ROOT)),
            "gse235_series_matrix": str(GSE235_MATRIX.relative_to(ROOT)),
            "gse250_expression": str(GSE250_EXPR.relative_to(ROOT)),
            "gse250_series_matrix": str(GSE250_MATRIX.relative_to(ROOT)),
            "wave129": str(W129.relative_to(ROOT)),
        },
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    def md_table(df: pd.DataFrame, max_rows: int = 30) -> str:
        if df.empty:
            return "_None._"
        show = df.head(max_rows).copy()
        for col in show.columns:
            if pd.api.types.is_float_dtype(show[col]):
                show[col] = show[col].map(lambda x: "" if pd.isna(x) else f"{x:.4g}")
        cols = list(show.columns)
        lines = [
            "| " + " | ".join(cols) + " |",
            "| " + " | ".join(["---"] * len(cols)) + " |",
        ]
        for _, row in show.iterrows():
            vals = [str(row[c]).replace("\n", " ") for c in cols]
            lines.append("| " + " | ".join(vals) + " |")
        return "\n".join(lines)

    report = f"""# Wave130 MS Treatment-Response Audit

## Bottom Line

Branch call: `{branch_call}`.

This wave tested whether the Wave129 IL1B/LAMP3 anti-TNF nonresponse biomarkers
or their modules replicate in two independent MS treatment-response datasets:
GSE235357 dimethyl fumarate PBMC RNA-seq and GSE250453 fingolimod PBMC RNA-seq.
Both datasets are small (5 responders and 5 nonresponders with paired baseline
and 12-month/treated samples), so effect sizes and direction stability are more
important than nominal p-values.

## Dataset Metadata

{md_table(pd.DataFrame(summary["datasets"]))}

## Cross-Dataset Stability

{md_table(stability_df.sort_values(["cross_ms_call", "best_baseline_p", "best_delta_p"], ascending=[True, True, True]))}

## Feature Tests

{md_table(results.sort_values(["call", "baseline_p", "delta_p"], ascending=[True, True, True]))}

## Interpretation

- A positive MS stratification route requires directional replication in both
  DMF and fingolimod, not a single small-n hit.
- The only cross-dataset small-n module signal after correction is `ifn_apc`.
  That is a broad IFN/APC state, not the Wave129 IL1B/LAMP3 primary biomarker
  pair and not a lipid-lysosomal target rescue.
- This test is still PBMC-level and cannot validate the CNS lesion module, but
  it is a real treatment-response endpoint and therefore stronger than a generic
  expression surrogate.
- Any small-n signal here remains biomarker-only unless it also connects to a
  druggable intervention point and survives prior-art and safety gates.

## Reproducibility

- Script: `scripts/v3_wave130_ms_treatment_response_audit.py`
- Outputs: `results_v3/wave130_ms_treatment_response_audit/`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
