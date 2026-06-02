#!/usr/bin/env python3
"""Select a small HMP2/IBDMDB MGX subset for V9 microbiome probing."""

from __future__ import annotations

from pathlib import Path
import argparse
import re

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "v9_microbiome_ibd" / "hmp2_metadata_2018-08-20.csv"
PRODUCTS = ROOT / "data" / "raw" / "v9_microbiome_ibd" / "products_MGX_2017-08-12.html"
DEFAULT_OUT = ROOT / "analysis" / "v9_microbiome" / "ibdmdb_subset"


def parse_tax_profile_urls() -> dict[str, str]:
    text = PRODUCTS.read_text(encoding="utf-8", errors="ignore")
    urls = re.findall(r"https://[^']+/tax_profiles/([^'/]+)_taxonomic_profile\.biom", text)
    full = re.findall(r"https://[^']+/tax_profiles/[^']+_taxonomic_profile\.biom", text)
    return dict(zip(urls, full))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-diagnosis", type=int, default=10)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--all-samples", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    tax_urls = parse_tax_profile_urls()
    df = pd.read_csv(RAW, low_memory=False)
    mgx = df[df["data_type"].astype(str).str.contains("metagenomics|MGX", case=False, na=False)].copy()
    if mgx.empty:
        mgx = df[df["data_type"].astype(str).str.contains("stool", case=False, na=False)].copy()
    if mgx.empty:
        mgx = df.copy()

    required = ["External ID", "Participant ID", "diagnosis", "data_type", "week_num"]
    present = [c for c in required if c in mgx.columns]
    mgx["product_id"] = mgx["External ID"].astype(str).str.replace(r"_P$", "", regex=True)
    mgx = mgx[mgx["product_id"].isin(tax_urls)].copy()

    if args.all_samples:
        subset = mgx[mgx["diagnosis"].astype(str).isin(["nonIBD", "UC", "CD"])].copy()
    else:
        subset_rows = []
        for diagnosis in ["nonIBD", "UC", "CD"]:
            sub = mgx[mgx["diagnosis"].astype(str) == diagnosis].copy()
            if sub.empty:
                continue
            # Prefer one early sample per participant for independence.
            sub["week_num_num"] = pd.to_numeric(sub.get("week_num", pd.Series(index=sub.index)), errors="coerce")
            sub = sub.sort_values(["Participant ID", "week_num_num"], na_position="last")
            sub = sub.drop_duplicates("Participant ID", keep="first").head(args.per_diagnosis)
            subset_rows.append(sub)
        subset = pd.concat(subset_rows, ignore_index=True) if subset_rows else mgx.head(args.per_diagnosis * 3)
    present_with_product = present + [c for c in ["product_id"] if c not in present]
    subset[present_with_product].to_csv(out_dir / "selected_ibdmdb_samples.tsv", sep="\t", index=False)

    # IBDMDB tax-profile product IDs appear to use External ID-like sample IDs.
    urls = []
    for sample_id, product_id in zip(subset["External ID"].astype(str), subset["product_id"].astype(str)):
        urls.append(
            {
                "sample_id": sample_id,
                "product_id": product_id,
                "url": tax_urls[product_id],
            }
        )
    pd.DataFrame(urls).to_csv(out_dir / "selected_tax_profile_urls.tsv", sep="\t", index=False)

    report = [
        "# V9 IBDMDB Subset",
        "",
        f"Metadata rows: {len(df)}",
        f"Candidate rows after data_type filtering: {len(mgx)}",
        f"Selected rows: {len(subset)}",
        "",
        "Diagnosis counts:",
        "",
        subset["diagnosis"].astype(str).value_counts().to_string(),
        "",
    ]
    (out_dir / "REPORT.md").write_text("\n".join(report), encoding="utf-8")


if __name__ == "__main__":
    main()
