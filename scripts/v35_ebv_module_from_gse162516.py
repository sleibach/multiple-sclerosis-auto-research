#!/usr/bin/env python3
"""Build a host EBV-transformation response module from GSE162516."""

from __future__ import annotations

import json
import math
import re
import zipfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw_v35/ebv_gse162516"
OUTDIR = ROOT / "analysis/v35_ebv_module_gse162516"
OUTDIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "D0": "GSM4953581_LCLd0_analysed.txt.gz",
    "D3": "GSM4953582_LCLd3_analysed.txt.gz",
    "D7": "GSM4953583_LCLd7_analysed.txt.gz",
    "D14": "GSM4953584_LCLd14_analysed.txt.gz",
    "D21": "GSM4953585_LCLd21_analysed.txt.gz",
    "LCL": "GSM4953586_LCL_analysed.txt.gz",
}

IFN_APC = {
    "STAT1", "IRF1", "CXCL10", "ISG15", "GBP1", "CD74", "HLA-DRA",
    "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1",
}


def read_inner_table(path: Path, label: str) -> pd.DataFrame:
    with zipfile.ZipFile(path) as zf:
        name = zf.namelist()[0]
        with zf.open(name) as fh:
            df = pd.read_csv(fh, sep="\t")
    rpkm_col = [c for c in df.columns if c.endswith("_RPKM")][0]
    out = df[["tracking_id", "gene_type", rpkm_col, "Description"]].copy()
    out = out.rename(columns={rpkm_col: f"{label}_RPKM"})
    # tracking_id is generally the gene symbol; keep simple symbols only.
    out = out[out["tracking_id"].map(lambda x: bool(re.match(r"^[A-Za-z0-9_.-]+$", str(x))))]
    return out


merged = None
for label, fn in FILES.items():
    df = read_inner_table(RAW / fn, label)
    cols = ["tracking_id", "gene_type", f"{label}_RPKM", "Description"]
    if merged is None:
        merged = df[cols]
    else:
        merged = merged.merge(df[["tracking_id", f"{label}_RPKM"]], on="tracking_id", how="outer")

assert merged is not None
for label in FILES:
    merged[f"{label}_RPKM"] = pd.to_numeric(merged[f"{label}_RPKM"], errors="coerce").fillna(0.0)

merged["late_mean_RPKM"] = merged[["D14_RPKM", "D21_RPKM", "LCL_RPKM"]].mean(axis=1)
merged["early_mean_RPKM"] = merged[["D3_RPKM", "D7_RPKM"]].mean(axis=1)
merged["log2_late_vs_D0"] = (merged["late_mean_RPKM"] + 0.1).map(math.log2) - (
    merged["D0_RPKM"] + 0.1
).map(math.log2)
merged["log2_early_vs_D0"] = (merged["early_mean_RPKM"] + 0.1).map(math.log2) - (
    merged["D0_RPKM"] + 0.1
).map(math.log2)

protein = merged[merged["gene_type"].fillna("").str.contains("protein_coding", case=False)].copy()
up = protein[(protein["late_mean_RPKM"] >= 1.0) & (protein["log2_late_vs_D0"] >= 1.0)].copy()
up = up.sort_values(["log2_late_vs_D0", "late_mean_RPKM"], ascending=False)
down = protein[(protein["D0_RPKM"] >= 1.0) & (protein["log2_late_vs_D0"] <= -1.0)].copy()
down = down.sort_values(["log2_late_vs_D0", "D0_RPKM"], ascending=True)

up.head(200).to_csv(OUTDIR / "host_ebv_transformation_up_top200.tsv", sep="\t", index=False)
down.head(200).to_csv(OUTDIR / "host_ebv_transformation_down_top200.tsv", sep="\t", index=False)
merged.to_csv(OUTDIR / "gse162516_rpkm_merged.tsv", sep="\t", index=False)

ifn_overlap = sorted(set(up["tracking_id"]).intersection(IFN_APC))
viral_markers = ["EBNA1", "EBNA2", "LMP1", "LMP2A", "LMP2B", "BZLF1"]
viral_present = sorted(set(merged["tracking_id"]).intersection(viral_markers))

summary = {
    "hypothesis": "EBV/IFN APC imprint module acquisition",
    "source": "GSE162516 processed supplementary archive",
    "archive_sha256_recorded_elsewhere": "642fa1ac9c2ac6e643030859d0344cc4aabf954dd195a4b752808e05bf89375e",
    "n_genes_total": int(len(merged)),
    "n_protein_coding": int(len(protein)),
    "n_host_late_up_log2fc_ge_1_rpkm_ge_1": int(len(up)),
    "n_host_late_down_log2fc_le_minus_1": int(len(down)),
    "ifn_apc_overlap_in_up_module": ifn_overlap,
    "viral_latency_markers_present_in_human_table": viral_present,
    "grounded_result": "host_ebv_transformation_module_acquired_not_yet_ms_sle_tested",
    "interpretation": (
        "GSE162516 provides a usable host B-cell EBV-transformation time-course "
        "module. It does not by itself establish an MS/SLE EBV imprint and does "
        "not include viral EBNA/LMP marker rows in the parsed human gene table. "
        "The next grounding step is to score this host module in MS/SLE B-cell "
        "or APC data and residualize against generic STAT1/IFN/APC tone."
    ),
    "minimum_next_test": [
        "Score host_ebv_transformation_up_top200 in MS/SLE B-cell/APC datasets.",
        "Adjust for STAT1/IFN/APC module to test EBV-specific residual signal.",
        "Require EBV-serostatus or viral-load metadata before claiming EBV imprint.",
    ],
}
with (OUTDIR / "summary.json").open("w") as fh:
    json.dump(summary, fh, indent=2, sort_keys=True)
print(json.dumps(summary, indent=2, sort_keys=True))
