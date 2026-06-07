#!/usr/bin/env python3
"""Score GSE162516 host EBV module in local GSE17410 PBMC data."""

from __future__ import annotations

import gzip
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
SOFT = ROOT / "data/raw/GSE17410/GSE17410_family.soft.gz"
EBV_UP = ROOT / "analysis/v35_ebv_module_gse162516/host_ebv_transformation_up_top200.tsv"
EBV_DOWN = ROOT / "analysis/v35_ebv_module_gse162516/host_ebv_transformation_down_top200.tsv"
OUTDIR = ROOT / "analysis/v35_ebv_module_gse17410_portability"
OUTDIR.mkdir(parents=True, exist_ok=True)


up_genes = set(pd.read_csv(EBV_UP, sep="\t")["tracking_id"].head(100))
down_genes = set(pd.read_csv(EBV_DOWN, sep="\t")["tracking_id"].head(100))


def subject_key(title: str) -> str:
    first = title.split()[0]
    token = first.split("_")[0]
    token = re.sub(r"(preMS|GRA9p)$", "", token)
    return re.sub(r"\d+$", "", token) or token


platform: dict[str, set[str]] = {}
samples: dict[str, dict[str, object]] = {}
current_sample = None
in_platform = False
platform_header = None
sample_table = False

with gzip.open(SOFT, "rt", errors="ignore") as fh:
    for line in fh:
        line = line.rstrip("\n")
        if line.startswith("^PLATFORM"):
            in_platform = True
            continue
        if line.startswith("^SAMPLE"):
            in_platform = False
            current_sample = line.split("=", 1)[1].strip()
            samples[current_sample] = {"geo_accession": current_sample, "values": {}}
            continue
        if in_platform:
            if line.startswith("ID\t"):
                platform_header = line.split("\t")
                continue
            if platform_header and line and not line.startswith("!") and not line.startswith("#"):
                parts = line.split("\t")
                if len(parts) < len(platform_header):
                    parts += [""] * (len(platform_header) - len(parts))
                row = dict(zip(platform_header, parts))
                pid = row.get("ID")
                genes = set()
                for col in ["Gene Symbol", "GENE_SYMBOL", "Gene symbol"]:
                    if col in row:
                        genes.update(g.strip() for g in re.split(r"///|//|;", row[col]) if g.strip())
                if pid and genes:
                    platform[pid] = genes
            continue
        if current_sample:
            if line.startswith("!Sample_title"):
                samples[current_sample]["title"] = line.split("=", 1)[1].strip()
            elif line.startswith("!Sample_characteristics_ch1"):
                samples[current_sample].setdefault("characteristics", []).append(line.split("=", 1)[1].strip())
            elif line == "!sample_table_begin":
                sample_table = True
            elif line == "!sample_table_end":
                sample_table = False
            elif sample_table and line and not line.startswith("ID_REF"):
                pid, val = line.split("\t")[:2]
                try:
                    samples[current_sample]["values"][pid] = float(val)
                except ValueError:
                    pass

up_probes = sorted([pid for pid, genes in platform.items() if genes & up_genes])
down_probes = sorted([pid for pid, genes in platform.items() if genes & down_genes])

rows = []
for sample, info in samples.items():
    title = str(info.get("title", ""))
    chars = " | ".join(info.get("characteristics", []))
    if "9th month pregnancy" in chars or "GRA9p" in title:
        timepoint = "month9_pregnancy"
    elif "preMS" in title:
        timepoint = "pre_pregnancy"
    else:
        timepoint = "other"
    values = info["values"]
    up_vals = [values[p] for p in up_probes if p in values]
    down_vals = [values[p] for p in down_probes if p in values]
    rows.append(
        {
            "geo_accession": sample,
            "title": title,
            "subject_key": subject_key(title),
            "timepoint": timepoint,
            "ebv_up_score": float(np.mean(up_vals)) if up_vals else np.nan,
            "ebv_down_score": float(np.mean(down_vals)) if down_vals else np.nan,
            "ebv_up_minus_down": float(np.mean(up_vals) - np.mean(down_vals)) if up_vals and down_vals else np.nan,
            "n_up_probes": len(up_vals),
            "n_down_probes": len(down_vals),
        }
    )

df = pd.DataFrame(rows)
df.to_csv(OUTDIR / "sample_ebv_module_scores.tsv", sep="\t", index=False)

tests = []
pre = df[df["timepoint"] == "pre_pregnancy"]
m9 = df[df["timepoint"] == "month9_pregnancy"]
for score in ["ebv_up_score", "ebv_down_score", "ebv_up_minus_down"]:
    tests.append(
        {
            "score": score,
            "comparison": "month9_pregnancy_vs_pre_pregnancy_unpaired",
            "n_pre": int(pre[score].notna().sum()),
            "n_month9": int(m9[score].notna().sum()),
            "mean_pre": float(pre[score].mean()),
            "mean_month9": float(m9[score].mean()),
            "delta_month9_minus_pre": float(m9[score].mean() - pre[score].mean()),
            "welch_p": float(stats.ttest_ind(m9[score].dropna(), pre[score].dropna(), equal_var=False).pvalue),
        }
    )

paired = pre.merge(m9, on="subject_key", suffixes=("_pre", "_month9"))
for score in ["ebv_up_score", "ebv_down_score", "ebv_up_minus_down"]:
    if len(paired) >= 2:
        diff = paired[f"{score}_month9"] - paired[f"{score}_pre"]
        tests.append(
            {
                "score": score,
                "comparison": "month9_pregnancy_vs_pre_pregnancy_paired_by_title_key",
                "n_pre": int(len(paired)),
                "n_month9": int(len(paired)),
                "mean_pre": float(paired[f"{score}_pre"].mean()),
                "mean_month9": float(paired[f"{score}_month9"].mean()),
                "delta_month9_minus_pre": float(diff.mean()),
                "welch_p": float(stats.ttest_1samp(diff, 0.0).pvalue),
            }
        )

pd.DataFrame(tests).to_csv(OUTDIR / "ebv_module_pregnancy_phase_tests.tsv", sep="\t", index=False)

summary = {
    "hypothesis": "EBV host module portability to GSE17410 PBMC",
    "grounded_result": "portable_with_probe_coverage_not_ebv_specific",
    "n_up_genes_top100": len(up_genes),
    "n_down_genes_top100": len(down_genes),
    "n_up_probes_on_gpl571": len(up_probes),
    "n_down_probes_on_gpl571": len(down_probes),
    "n_samples": int(len(df)),
    "tests": tests,
    "interpretation": (
        "The host EBV-transformation module has enough GPL571 probe coverage to "
        "score in GSE17410 PBMC. Any pregnancy-phase shift is technical/context "
        "information only, because this cohort lacks EBV status and postpartum "
        "relapse-window sampling."
    ),
}
with (OUTDIR / "summary.json").open("w") as fh:
    json.dump(summary, fh, indent=2, sort_keys=True)
print(json.dumps(summary, indent=2, sort_keys=True))
