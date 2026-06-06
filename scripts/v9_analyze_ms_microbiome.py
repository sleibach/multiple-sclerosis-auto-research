#!/usr/bin/env python3
"""Analyze exported MS phyloseq stool tables for V9 microbiome axis.

This script is intentionally conservative. It does not try to discover every
taxon; it tests pre-specified feature families from MAP_METHODOLOGY_V9.
"""

from __future__ import annotations

from pathlib import Path
import re

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "analysis" / "v9_microbiome" / "ms_phyloseq_export"
OUT = ROOT / "analysis" / "v9_microbiome" / "ms_primary_analysis"

FEATURE_PATTERNS = {
    "akkermansia_mucin_barrier": [r"akkermansia"],
    "prevotella": [r"prevotella"],
    "faecalibacterium_butyrate": [r"faecalibacterium"],
    "bacteroides": [r"bacteroides"],
    "enterobacteriaceae_lps": [r"enterobacteriaceae", r"escherichia", r"shigella"],
    "butyrate_clostridia": [r"roseburia", r"eubacterium", r"coprococcus", r"butyricicoccus"],
}

GROUP_COL_HINTS = [
    "diagnosis",
    "disease",
    "group",
    "condition",
    "status",
    "phenotype",
    "case",
    "subject_group",
]


def bh_fdr(pvals: list[float]) -> list[float]:
    p = np.array([1.0 if pd.isna(x) else float(x) for x in pvals])
    n = len(p)
    order = np.argsort(p)
    ranks = np.empty(n, dtype=float)
    ranks[order] = np.arange(1, n + 1)
    q = p * n / ranks
    q_sorted = np.minimum.accumulate(q[order][::-1])[::-1]
    out = np.empty(n, dtype=float)
    out[order] = np.minimum(q_sorted, 1.0)
    return out.tolist()


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in df.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(lines)


def hedges_g(x: np.ndarray, y: np.ndarray) -> float:
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    if len(x) < 2 or len(y) < 2:
        return float("nan")
    nx, ny = len(x), len(y)
    sx, sy = np.var(x, ddof=1), np.var(y, ddof=1)
    pooled = ((nx - 1) * sx + (ny - 1) * sy) / (nx + ny - 2)
    if pooled <= 0:
        return float("nan")
    d = (np.mean(x) - np.mean(y)) / np.sqrt(pooled)
    correction = 1 - 3 / (4 * (nx + ny) - 9)
    return float(d * correction)


def collapse_taxonomy(tax: pd.DataFrame) -> pd.Series:
    cols = [c for c in tax.columns if c != "feature_id"]
    return tax[cols].fillna("").astype(str).agg(";".join, axis=1).str.lower()


def choose_group_column(meta: pd.DataFrame) -> str | None:
    for hint in GROUP_COL_HINTS:
        for col in meta.columns:
            if hint in col.lower():
                values = meta[col].dropna().astype(str).str.lower().unique()
                joined = " ".join(values)
                if any(term in joined for term in ["ms", "multiple", "healthy", "control", "hc"]):
                    return col
    for col in meta.columns:
        values = meta[col].dropna().astype(str).str.lower().unique()
        if 2 <= len(values) <= 6:
            joined = " ".join(values)
            if any(term in joined for term in ["ms", "multiple", "healthy", "control", "hc"]):
                return col
    return None


def classify_groups(series: pd.Series) -> pd.Series:
    values = series.astype(str).str.lower()
    out = pd.Series("other", index=series.index)
    out[values.str.contains(r"\bms\b|multiple")] = "MS"
    out[values.str.contains(r"healthy|control|\bhc\b")] = "control"
    return out


def analyze_prefix(prefix: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    otu = pd.read_csv(IN / f"{prefix}_otu_table.tsv", sep="\t")
    tax_path = IN / f"{prefix}_taxonomy.tsv"
    meta = pd.read_csv(IN / f"{prefix}_metadata.tsv", sep="\t")
    tax = pd.read_csv(tax_path, sep="\t") if tax_path.exists() else pd.DataFrame()

    sample_cols = [c for c in otu.columns if c != "feature_id"]
    counts = otu.set_index("feature_id")[sample_cols].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    rel = counts.div(counts.sum(axis=0).replace(0, np.nan), axis=1).fillna(0.0)

    if not tax.empty:
        tax_text = pd.Series(collapse_taxonomy(tax).values, index=tax["feature_id"].astype(str))
    else:
        tax_text = pd.Series({fid: str(fid).lower() for fid in rel.index})

    group_col = choose_group_column(meta)
    if not group_col:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    meta = meta.copy()
    meta["inferred_group"] = classify_groups(meta[group_col]) if group_col else "other"
    usable_samples = [s for s in sample_cols if s in set(meta["sample_id"])]
    meta_by_sample = meta.set_index("sample_id").loc[usable_samples]

    feature_scores = {}
    feature_members = {}
    for family, patterns in FEATURE_PATTERNS.items():
        regex = re.compile("|".join(patterns), flags=re.I)
        members = [fid for fid in rel.index if regex.search(tax_text.get(fid, str(fid)))]
        feature_members[family] = members
        if members:
            feature_scores[family] = rel.loc[members, usable_samples].sum(axis=0)
        else:
            feature_scores[family] = pd.Series(np.nan, index=usable_samples)

    score_df = pd.DataFrame(feature_scores)
    score_df.insert(0, "sample_id", usable_samples)
    score_df.insert(1, "group", meta_by_sample["inferred_group"].values)
    score_df.insert(2, "source_prefix", prefix)
    score_df["age"] = pd.to_numeric(meta_by_sample.get("Age", pd.Series(np.nan, index=meta_by_sample.index)), errors="coerce").values
    score_df["sex"] = meta_by_sample.get("Sex", pd.Series("", index=meta_by_sample.index)).astype(str).str.lower().values

    rows = []
    adjusted_rows = []
    for family in FEATURE_PATTERNS:
        x = score_df.loc[score_df["group"] == "MS", family].astype(float).to_numpy()
        y = score_df.loc[score_df["group"] == "control", family].astype(float).to_numpy()
        if len(x) >= 2 and len(y) >= 2:
            p = stats.ttest_ind(x, y, equal_var=False, nan_policy="omit").pvalue
            g = hedges_g(x, y)
            delta = float(np.nanmean(x) - np.nanmean(y))
        else:
            p, g, delta = np.nan, np.nan, np.nan
        rows.append(
            {
                "source_prefix": prefix,
                "feature_family": family,
                "n_features_matched": len(feature_members[family]),
                "n_ms": int(np.sum(score_df["group"] == "MS")),
                "n_control": int(np.sum(score_df["group"] == "control")),
                "mean_ms": float(np.nanmean(x)) if len(x) else np.nan,
                "mean_control": float(np.nanmean(y)) if len(y) else np.nan,
                "delta_ms_minus_control": delta,
                "hedges_g_ms_minus_control": g,
                "p_value": p,
                "matched_feature_ids": ";".join(feature_members[family][:50]),
                "group_column": group_col or "",
            }
        )
        model_df = score_df.loc[score_df["group"].isin(["MS", "control"]), [family, "group", "age", "sex"]].copy()
        model_df = model_df.rename(columns={family: "feature"})
        model_df["is_ms"] = (model_df["group"] == "MS").astype(int)
        model_df["sex_male"] = model_df["sex"].str.startswith("m").astype(int)
        model_df = model_df.dropna(subset=["feature", "is_ms", "age", "sex_male"])
        if len(model_df) >= 10 and model_df["is_ms"].nunique() == 2:
            fit = smf.ols("feature ~ is_ms + age + sex_male", data=model_df).fit()
            coef = float(fit.params.get("is_ms", np.nan))
            p_adj = float(fit.pvalues.get("is_ms", np.nan))
            n_model = int(fit.nobs)
        else:
            coef, p_adj, n_model = np.nan, np.nan, int(len(model_df))
        adjusted_rows.append(
            {
                "source_prefix": prefix,
                "feature_family": family,
                "n_model": n_model,
                "coef_is_ms_adjusted_age_sex": coef,
                "p_value_adjusted_age_sex": p_adj,
            }
        )
    stats_df = pd.DataFrame(rows)
    stats_df["fdr"] = bh_fdr(stats_df["p_value"].tolist())
    adjusted_df = pd.DataFrame(adjusted_rows)
    adjusted_df["fdr_adjusted_age_sex"] = bh_fdr(adjusted_df["p_value_adjusted_age_sex"].tolist())
    return score_df, stats_df, adjusted_df


def analyze_timepoint_prefix(prefix: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    otu = pd.read_csv(IN / f"{prefix}_otu_table.tsv", sep="\t")
    tax_path = IN / f"{prefix}_taxonomy.tsv"
    meta = pd.read_csv(IN / f"{prefix}_metadata.tsv", sep="\t")
    tax = pd.read_csv(tax_path, sep="\t") if tax_path.exists() else pd.DataFrame()

    sample_cols = [c for c in otu.columns if c != "feature_id"]
    counts = otu.set_index("feature_id")[sample_cols].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    rel = counts.div(counts.sum(axis=0).replace(0, np.nan), axis=1).fillna(0.0)

    if not tax.empty:
        tax_text = pd.Series(collapse_taxonomy(tax).values, index=tax["feature_id"].astype(str))
    else:
        tax_text = pd.Series({fid: str(fid).lower() for fid in rel.index})

    required_cols = {"sample_id", "Samples", "TimePoint"}
    if not required_cols.issubset(meta.columns):
        return pd.DataFrame(), pd.DataFrame()

    usable_samples = [s for s in sample_cols if s in set(meta["sample_id"])]
    meta_by_sample = meta.set_index("sample_id").loc[usable_samples]

    feature_scores = {}
    feature_members = {}
    for family, patterns in FEATURE_PATTERNS.items():
        regex = re.compile("|".join(patterns), flags=re.I)
        members = [fid for fid in rel.index if regex.search(tax_text.get(fid, str(fid)))]
        feature_members[family] = members
        if members:
            feature_scores[family] = rel.loc[members, usable_samples].sum(axis=0)
        else:
            feature_scores[family] = pd.Series(np.nan, index=usable_samples)

    score_df = pd.DataFrame(feature_scores)
    score_df.insert(0, "sample_id", usable_samples)
    score_df.insert(1, "source_prefix", prefix)
    score_df.insert(2, "subject_id", meta_by_sample["Samples"].astype(str).values)
    score_df.insert(3, "timepoint", meta_by_sample["TimePoint"].astype(str).values)
    score_df.insert(4, "ocrevus", meta_by_sample.get("Ocrevus", pd.Series("", index=meta_by_sample.index)).astype(str).values)

    rows = []
    comparisons = [("TP2", "TP1"), ("TP3", "TP1"), ("TP4", "TP1")]
    for later, baseline in comparisons:
        for family in FEATURE_PATTERNS:
            pivot = score_df.pivot_table(index="subject_id", columns="timepoint", values=family, aggfunc="mean")
            if later in pivot.columns and baseline in pivot.columns:
                delta = (pivot[later] - pivot[baseline]).dropna().to_numpy(dtype=float)
            else:
                delta = np.array([], dtype=float)
            if len(delta) >= 2:
                p = stats.ttest_1samp(delta, 0.0, nan_policy="omit").pvalue
                mean_delta = float(np.nanmean(delta))
                sd = float(np.nanstd(delta, ddof=1))
                g = float(mean_delta / sd * (1 - 3 / (4 * len(delta) - 1))) if sd > 0 else np.nan
            else:
                p, mean_delta, g = np.nan, np.nan, np.nan
            rows.append(
                {
                    "source_prefix": prefix,
                    "comparison": f"{later}_minus_{baseline}",
                    "feature_family": family,
                    "n_pairs": int(len(delta)),
                    "mean_delta": mean_delta,
                    "hedges_g_delta_vs_zero": g,
                    "p_value": p,
                    "n_features_matched": len(feature_members[family]),
                    "matched_feature_ids": ";".join(feature_members[family][:50]),
                }
            )
    stats_df = pd.DataFrame(rows)
    stats_df["fdr"] = bh_fdr(stats_df["p_value"].tolist())
    return score_df, stats_df


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    all_scores = []
    all_stats = []
    all_adjusted = []
    all_timepoint_scores = []
    all_timepoint_stats = []
    for summary_path in IN.glob("*_summary.tsv"):
        prefix = summary_path.name.replace("_summary.tsv", "")
        scores, stats_df, adjusted_df = analyze_prefix(prefix)
        if not scores.empty:
            all_scores.append(scores)
            all_stats.append(stats_df)
            all_adjusted.append(adjusted_df)
        tp_scores, tp_stats = analyze_timepoint_prefix(prefix)
        if not tp_scores.empty:
            all_timepoint_scores.append(tp_scores)
            all_timepoint_stats.append(tp_stats)

    scores = pd.concat(all_scores, ignore_index=True) if all_scores else pd.DataFrame()
    stats_df = pd.concat(all_stats, ignore_index=True) if all_stats else pd.DataFrame()
    adjusted_df = pd.concat(all_adjusted, ignore_index=True) if all_adjusted else pd.DataFrame()
    scores.to_csv(OUT / "ms_feature_family_scores.tsv", sep="\t", index=False)
    stats_df.to_csv(OUT / "ms_feature_family_tests.tsv", sep="\t", index=False)
    adjusted_df.to_csv(OUT / "ms_feature_family_adjusted_tests.tsv", sep="\t", index=False)
    if all_timepoint_scores:
        tp_scores = pd.concat(all_timepoint_scores, ignore_index=True)
        tp_stats = pd.concat(all_timepoint_stats, ignore_index=True)
        tp_scores.to_csv(OUT / "ms_timepoint_feature_family_scores.tsv", sep="\t", index=False)
        tp_stats.to_csv(OUT / "ms_timepoint_feature_family_tests.tsv", sep="\t", index=False)

    with (OUT / "REPORT.md").open("w", encoding="utf-8") as fh:
        fh.write("# V9 MS Microbiome Primary Analysis\n\n")
        fh.write("Pre-specified feature-family tests from `docs/locked_rules/MAP_METHODOLOGY_V9.md`.\n\n")
        fh.write("## MS Versus Control\n\n")
        fh.write(markdown_table(stats_df))
        fh.write("\n\n## MS Versus Control, Age/Sex-Adjusted OLS\n\n")
        fh.write(markdown_table(adjusted_df))
        if all_timepoint_scores:
            fh.write("\n\n## MS Paired Timepoint Deltas\n\n")
            fh.write("Exploratory paired within-subject deltas for available MS timepoints.\n\n")
            fh.write(markdown_table(tp_stats))
        fh.write("\n")


if __name__ == "__main__":
    main()
