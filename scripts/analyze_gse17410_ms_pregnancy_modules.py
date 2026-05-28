#!/usr/bin/env python3
"""MS pregnancy module screen from processed GSE17410 SOFT tables."""

from __future__ import annotations

import csv
import gzip
import json
import math
from pathlib import Path

import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
SOFT = ROOT / "data" / "raw" / "GSE17410" / "GSE17410_family.soft.gz"
META = ROOT / "data" / "derived" / "GSE17410" / "sample_metadata.tsv"
OUT = ROOT / "results" / "pregnancy_dimension" / "gse17410_ms_modules"
SEED = 20260528


MODULES = {
    "mif_cd74_receptor_state": ["CD74", "CD44", "CXCR4", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1"],
    "hla_ii_only": ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1"],
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"],
    "lysosomal_apc": ["CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "IFI30", "CD74"],
    "hif_nampt_metabolic": ["HIF1A", "NAMPT", "SLC2A1", "LDHA", "PGK1"],
}


def load_metadata() -> pd.DataFrame:
    rows = []
    with META.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            title = row["Sample_title"]
            if "preMS" in title:
                state = "pre_pregnancy_ms"
            elif "GRA9p" in title or "9th month pregnancy" in row["Sample_characteristics_ch1"]:
                state = "month9_pregnancy_ms"
            else:
                state = "other"
            rows.append(
                {
                    "geo_accession": row["geo_accession"],
                    "title": title,
                    "state": state,
                }
            )
    return pd.DataFrame(rows)


def parse_soft() -> tuple[pd.DataFrame, pd.DataFrame]:
    platform_rows = []
    sample_tables: dict[str, dict[str, float]] = {}
    in_platform = False
    platform_header: list[str] | None = None
    current_sample: str | None = None
    in_sample_table = False

    with gzip.open(SOFT, "rt", errors="replace") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line == "!platform_table_begin":
                in_platform = True
                platform_header = None
                continue
            if line == "!platform_table_end":
                in_platform = False
                continue
            if line.startswith("^SAMPLE = "):
                current_sample = line.split(" = ", 1)[1]
                continue
            if line == "!sample_table_begin":
                in_sample_table = True
                sample_tables[current_sample or ""] = {}
                handle.readline()
                continue
            if line == "!sample_table_end":
                in_sample_table = False
                continue
            if in_platform:
                if platform_header is None:
                    platform_header = line.split("\t")
                else:
                    parts = line.split("\t")
                    if len(parts) == len(platform_header):
                        platform_rows.append(dict(zip(platform_header, parts)))
            elif in_sample_table and current_sample:
                parts = line.split("\t")
                if len(parts) >= 2:
                    try:
                        sample_tables[current_sample][parts[0]] = float(parts[1])
                    except ValueError:
                        pass

    platform = pd.DataFrame(platform_rows)
    expr = pd.DataFrame(sample_tables)
    expr.index.name = "probe_id"
    return platform, expr


def hedges_g(a: pd.Series, b: pd.Series) -> float:
    a = a.dropna()
    b = b.dropna()
    pooled = math.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    d = (a.mean() - b.mean()) / pooled
    correction = 1 - (3 / (4 * (len(a) + len(b)) - 9))
    return d * correction


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = load_metadata()
    platform, expr = parse_soft()

    probe_map = platform[["ID", "Gene Symbol"]].rename(columns={"ID": "probe_id", "Gene Symbol": "symbol"})
    probe_map["symbol"] = probe_map["symbol"].fillna("").str.split(" /// ").str[0].str.strip()
    wanted = sorted({gene for genes in MODULES.values() for gene in genes})
    probe_map = probe_map[probe_map["symbol"].isin(wanted)]
    probe_map.to_csv(OUT / "module_probe_map.tsv", sep="\t", index=False)

    expr = expr.loc[expr.index.intersection(probe_map["probe_id"])]
    symbol_expr = expr.merge(probe_map, left_index=True, right_on="probe_id").groupby("symbol").mean(numeric_only=True)

    rows = []
    missing = []
    for module, genes in MODULES.items():
        present = [gene for gene in genes if gene in symbol_expr.index]
        absent = [gene for gene in genes if gene not in symbol_expr.index]
        if absent:
            missing.append({"module": module, "missing_symbols": ";".join(absent)})
        scores = symbol_expr.loc[present].mean(axis=0)
        for sample, score in scores.items():
            rows.append(
                {
                    "geo_accession": sample,
                    "module": module,
                    "score": score,
                    "n_genes_present": len(present),
                    "genes_present": ";".join(present),
                }
            )
    long = pd.DataFrame(rows).merge(meta, on="geo_accession", how="left")
    long.to_csv(OUT / "sample_module_scores.tsv", sep="\t", index=False)
    pd.DataFrame(missing).to_csv(OUT / "missing_module_genes.tsv", sep="\t", index=False)

    contrast_rows = []
    for module in MODULES:
        sub = long[long["module"] == module]
        pre = sub[sub["state"] == "pre_pregnancy_ms"]["score"]
        month9 = sub[sub["state"] == "month9_pregnancy_ms"]["score"]
        stat = stats.ttest_ind(month9, pre, equal_var=False, nan_policy="omit")
        contrast_rows.append(
            {
                "module": module,
                "n_pre": len(pre),
                "n_month9": len(month9),
                "mean_pre": pre.mean(),
                "mean_month9": month9.mean(),
                "delta_month9_minus_pre": month9.mean() - pre.mean(),
                "hedges_g": hedges_g(month9, pre),
                "welch_p": stat.pvalue,
            }
        )
    pd.DataFrame(contrast_rows).to_csv(OUT / "month9_vs_pre_contrasts.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "dataset": "GSE17410",
        "n_samples": int(len(meta)),
        "states": meta["state"].value_counts().to_dict(),
        "module_count": len(MODULES),
        "note": "Processed SOFT VALUE tables used; no CEL reprocessing.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
