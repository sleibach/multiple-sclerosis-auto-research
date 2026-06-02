#!/usr/bin/env python3
"""Analyze a small IBDMDB taxonomic-profile subset for V9 microbiome probing."""

from __future__ import annotations

from pathlib import Path
import argparse
import json
import re

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUBSET = ROOT / "analysis" / "v9_microbiome" / "ibdmdb_subset" / "selected_ibdmdb_samples.tsv"
DEFAULT_RAW_DIR = ROOT / "data" / "raw" / "v9_microbiome_ibd" / "tax_profiles_subset"
DEFAULT_OUT = ROOT / "analysis" / "v9_microbiome" / "ibdmdb_subset_analysis"

FEATURE_PATTERNS = {
    "akkermansia_mucin_barrier": [r"akkermansia"],
    "prevotella": [r"prevotella"],
    "faecalibacterium_butyrate": [r"faecalibacterium"],
    "bacteroides": [r"bacteroides"],
    "enterobacteriaceae_lps": [r"enterobacteriaceae", r"escherichia", r"shigella"],
    "butyrate_clostridia": [r"roseburia", r"eubacterium", r"coprococcus", r"butyricicoccus"],
}


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


def hedges_g(x: np.ndarray, y: np.ndarray) -> float:
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    if len(x) < 2 or len(y) < 2:
        return float("nan")
    nx, ny = len(x), len(y)
    pooled = ((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1)) / (nx + ny - 2)
    if pooled <= 0:
        return float("nan")
    return float(((np.mean(x) - np.mean(y)) / np.sqrt(pooled)) * (1 - 3 / (4 * (nx + ny) - 9)))


def read_profile(path: Path) -> dict[str, float]:
    if path.suffix == ".biom":
        obj = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
        row_names = [row["id"] for row in obj.get("rows", [])]
        values = {}
        for row_idx, _col_idx, value in obj.get("data", []):
            if 0 <= row_idx < len(row_names):
                values[row_names[row_idx].lower()] = float(value)
        return values

    rows: dict[str, float] = {}
    with path.open("r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            name = parts[0]
            try:
                value = float(parts[1])
            except ValueError:
                continue
            rows[name.lower()] = value
    return rows


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in df.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subset", type=Path, default=DEFAULT_SUBSET)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = pd.read_csv(args.subset, sep="\t")
    score_rows = []
    missing = []
    for row in meta.to_dict(orient="records"):
        sample_id = str(row["External ID"])
        path = args.raw_dir / f"{sample_id}.biom"
        if not path.exists() or path.stat().st_size == 0:
            missing.append(sample_id)
            continue
        profile = read_profile(path)
        scores = {
            "sample_id": sample_id,
            "diagnosis": str(row["diagnosis"]),
            "participant_id": str(row["Participant ID"]),
        }
        for family, patterns in FEATURE_PATTERNS.items():
            regex = re.compile("|".join(patterns), flags=re.I)
            matches = [value for taxon, value in profile.items() if regex.search(taxon)]
            # MetaPhlAn rows are hierarchical. Max avoids counting both parent
            # and child clades as independent abundance.
            scores[family] = max(matches) if matches else 0.0
        score_rows.append(scores)

    scores = pd.DataFrame(score_rows)
    scores.to_csv(out_dir / "ibdmdb_feature_family_scores.tsv", sep="\t", index=False)
    pd.DataFrame({"missing_sample_id": missing}).to_csv(out_dir / "missing_profiles.tsv", sep="\t", index=False)

    tests = []
    for disease in ["UC", "CD"]:
        for family in FEATURE_PATTERNS:
            x = scores.loc[scores["diagnosis"] == disease, family].astype(float).to_numpy()
            y = scores.loc[scores["diagnosis"] == "nonIBD", family].astype(float).to_numpy()
            if len(x) >= 2 and len(y) >= 2:
                p = stats.ttest_ind(x, y, equal_var=False).pvalue
                g = hedges_g(x, y)
                delta = float(np.mean(x) - np.mean(y))
            else:
                p, g, delta = np.nan, np.nan, np.nan
            tests.append(
                {
                    "disease": disease,
                    "feature_family": family,
                    "n_disease": len(x),
                    "n_nonibd": len(y),
                    "mean_disease": float(np.mean(x)) if len(x) else np.nan,
                    "mean_nonibd": float(np.mean(y)) if len(y) else np.nan,
                    "delta_disease_minus_nonibd": delta,
                    "hedges_g": g,
                    "p_value": p,
                }
            )
    tests_df = pd.DataFrame(tests)
    tests_df["fdr"] = bh_fdr(tests_df["p_value"].tolist())
    tests_df.to_csv(out_dir / "ibdmdb_feature_family_tests.tsv", sep="\t", index=False)

    report = [
        "# V9 IBDMDB Subset Analysis",
        "",
        f"Downloaded/usable profiles: {len(scores)}",
        f"Missing profiles: {len(missing)}",
        "",
        "This is a small resource-conscious primary-data subset, not the full IBDMDB.",
        "",
        markdown_table(tests_df),
        "",
    ]
    (out_dir / "REPORT.md").write_text("\n".join(report), encoding="utf-8")


if __name__ == "__main__":
    main()
