#!/usr/bin/env python3
"""Feasibility and limited HLA-II/CD64 scoring for local GSE17410/GSE17449."""

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
OUTDIR = ROOT / "analysis/v35_gse17410_pregnancy_apc"
OUTDIR.mkdir(parents=True, exist_ok=True)

HLA_GENES = {"HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"}
CD64_GENES = {"FCGR1A", "FCGR1B", "FCGR1C"}


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

hla_probes = sorted([pid for pid, genes in platform.items() if genes & HLA_GENES])
cd64_probes = sorted([pid for pid, genes in platform.items() if genes & CD64_GENES])

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
    hla_vals = [values[p] for p in hla_probes if p in values]
    cd64_vals = [values[p] for p in cd64_probes if p in values]
    rows.append(
        {
            "geo_accession": sample,
            "title": title,
            "subject_key": subject_key(title),
            "timepoint": timepoint,
            "hla_ii_score": float(np.mean(hla_vals)) if hla_vals else np.nan,
            "cd64_score": float(np.mean(cd64_vals)) if cd64_vals else np.nan,
            "hla_minus_cd64": float(np.mean(hla_vals) - np.mean(cd64_vals)) if hla_vals and cd64_vals else np.nan,
            "n_hla_probes": len(hla_vals),
            "n_cd64_probes": len(cd64_vals),
        }
    )

df = pd.DataFrame(rows)
df.to_csv(OUTDIR / "sample_module_scores.tsv", sep="\t", index=False)

tests = []
pre = df[df["timepoint"] == "pre_pregnancy"]
m9 = df[df["timepoint"] == "month9_pregnancy"]
for score in ["hla_ii_score", "cd64_score", "hla_minus_cd64"]:
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
for score in ["hla_ii_score", "cd64_score", "hla_minus_cd64"]:
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

test_df = pd.DataFrame(tests)
test_df.to_csv(OUTDIR / "pregnancy_phase_tests.tsv", sep="\t", index=False)

summary = {
    "hypothesis": "postpartum APC-arm imbalance MS specificity feasibility",
    "grounded_result": "pregnancy_phase_scoring_feasible_postpartum_window_absent",
    "n_samples": int(len(df)),
    "timepoint_counts": df["timepoint"].value_counts().to_dict(),
    "n_hla_probes": len(hla_probes),
    "n_cd64_probes": len(cd64_probes),
    "paired_subject_keys": paired["subject_key"].tolist() if len(paired) else [],
    "tests": tests,
    "interpretation": (
        "Local GSE17410/GSE17449 can score PBMC HLA-II and CD64 probes for "
        "pre-pregnancy versus 9th-month pregnancy MS samples. It cannot test "
        "the decisive postpartum relapse-window hypothesis because no postpartum "
        "timepoints or relapse-window labels are present in the held SOFT file."
    ),
}
with (OUTDIR / "summary.json").open("w") as fh:
    json.dump(summary, fh, indent=2, sort_keys=True)
print(json.dumps(summary, indent=2, sort_keys=True))
