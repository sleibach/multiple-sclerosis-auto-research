#!/usr/bin/env python3
"""Donor-aware hardening for V35 complement/lipid progressive axis."""

from __future__ import annotations

import csv
import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
EXPR = ROOT / "data/raw/GSE180759_expression_matrix.csv.gz"
ANN = ROOT / "data/raw/GSE180759_annotation.txt.gz"
OUTDIR = ROOT / "analysis/v35_donor_aware_complement_lipid"
OUTDIR.mkdir(parents=True, exist_ok=True)

MODULES = {
    "complement_phagocytosis": ["C1QA", "C1QB", "C1QC", "C3", "ITGAM", "ITGB2", "TYROBP", "AIF1"],
    "lipid_repair": ["APOE", "LPL", "TREM2", "ABCA1", "ABCG1", "SPP1", "LGALS3", "GPNMB"],
    "ifn_hla_apc": ["STAT1", "IRF1", "CXCL10", "ISG15", "CD74", "HLA-DRA", "HLA-DPA1"],
}


def stream_selected(genes: set[str]) -> pd.DataFrame:
    selected = {}
    with gzip.open(EXPR, "rt") as fh:
        reader = csv.reader(fh)
        header = next(reader)  # nucleus IDs only
        for row in reader:
            gene = row[0]
            if gene in genes:
                selected[gene] = [float(x) if x else 0.0 for x in row[1:]]
    return pd.DataFrame(selected, index=header)


def hedges_g(a: list[float], b: list[float]) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    pooled = math.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0:
        return 0.0
    correction = 1 - (3 / (4 * (len(a) + len(b)) - 9))
    return float(((a.mean() - b.mean()) / pooled) * correction)


genes = {g for xs in MODULES.values() for g in xs}
expr = stream_selected(genes)
ann = pd.read_csv(ANN, sep="\t").set_index("nucleus_barcode")
common = expr.index.intersection(ann.index)
expr = expr.loc[common]
ann = ann.loc[common]

score_df = ann[["NBB_case", "pathology", "cell_type"]].copy()
for module, wanted in MODULES.items():
    present = [g for g in wanted if g in expr.columns]
    score_df[module] = expr[present].mean(axis=1)

immune = score_df[score_df["cell_type"] == "immune"].copy()
donor_means = (
    immune.groupby(["NBB_case", "pathology"])
    .agg(
        n_nuclei=("cell_type", "size"),
        complement_phagocytosis=("complement_phagocytosis", "mean"),
        lipid_repair=("lipid_repair", "mean"),
        ifn_hla_apc=("ifn_hla_apc", "mean"),
    )
    .reset_index()
)
donor_means.to_csv(OUTDIR / "immune_donor_pathology_module_means.tsv", sep="\t", index=False)

tests = []
active = "chronic_active_MS_lesion_edge"
comparators = [
    "control_white_matter",
    "MS_periplaque_white_matter",
    "chronic_inactive_MS_lesion_edge",
    "MS_lesion_core",
]
for module in MODULES:
    for comp in comparators:
        a_df = donor_means[donor_means["pathology"] == active][["NBB_case", module]]
        b_df = donor_means[donor_means["pathology"] == comp][["NBB_case", module]]
        paired = a_df.merge(b_df, on="NBB_case", suffixes=("_active", "_comp"))
        if len(paired) >= 2:
            diff = paired[f"{module}_active"] - paired[f"{module}_comp"]
            stat_p = float(stats.ttest_1samp(diff, 0.0).pvalue) if len(diff) > 1 else float("nan")
            tests.append(
                {
                    "module": module,
                    "comparison": f"{active}_vs_{comp}",
                    "test_type": "paired_donor_ttest",
                    "n_donors": int(len(paired)),
                    "mean_active": float(paired[f"{module}_active"].mean()),
                    "mean_comparator": float(paired[f"{module}_comp"].mean()),
                    "delta_active_minus_comparator": float(diff.mean()),
                    "p_value": stat_p,
                    "hedges_g": float(diff.mean() / diff.std(ddof=1)) if len(diff) > 1 and diff.std(ddof=1) else float("nan"),
                }
            )
        a = a_df[module].tolist()
        b = b_df[module].tolist()
        if len(a) >= 2 and len(b) >= 2:
            tests.append(
                {
                    "module": module,
                    "comparison": f"{active}_vs_{comp}",
                    "test_type": "unpaired_donor_welch",
                    "n_donors": int(len(a) + len(b)),
                    "mean_active": float(np.mean(a)),
                    "mean_comparator": float(np.mean(b)),
                    "delta_active_minus_comparator": float(np.mean(a) - np.mean(b)),
                    "p_value": float(stats.ttest_ind(a, b, equal_var=False).pvalue),
                    "hedges_g": hedges_g(a, b),
                }
            )

test_df = pd.DataFrame(tests)
test_df.to_csv(OUTDIR / "donor_aware_tests.tsv", sep="\t", index=False)

key = test_df[
    (test_df["module"].isin(["lipid_repair", "complement_phagocytosis"]))
    & (test_df["comparison"].isin([f"{active}_vs_control_white_matter", f"{active}_vs_MS_periplaque_white_matter"]))
].copy()

summary = {
    "hypothesis": "complement/lipid progressive axis donor-aware hardening",
    "n_immune_nuclei": int(len(immune)),
    "n_donor_pathology_bins": int(len(donor_means)),
    "grounded_result": "lipid_repair_partly_supported_complement_not_supported",
    "key_tests": key.to_dict(orient="records"),
    "interpretation": (
        "Donor-level aggregation reduces nucleus-level pseudo-replication. The "
        "lipid-repair arm remains directionally higher at chronic-active lesion "
        "edge in several comparisons, but sample counts are very small at donor "
        "level. The complement/phagocytosis arm does not show a clean active-edge "
        "increase and should not be promoted as part of the same lead."
    ),
}
with (OUTDIR / "summary.json").open("w") as fh:
    json.dump(summary, fh, indent=2, sort_keys=True)
print(json.dumps(summary, indent=2, sort_keys=True))
