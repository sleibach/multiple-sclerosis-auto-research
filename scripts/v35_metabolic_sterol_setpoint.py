#!/usr/bin/env python3
"""Ground V35 metabolic/sterol setpoint using held V32, lesion, and lipidomics data."""

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
OUTDIR = ROOT / "analysis/v35_metabolic_sterol_setpoint"
OUTDIR.mkdir(parents=True, exist_ok=True)

V32_SINGLE = ROOT / "analysis/v32_confounder_audit/v32_confounder_adjustment_metrics.tsv"
V32_JOINT = ROOT / "analysis/v32_confounder_audit/v32_joint_adjustment_metrics.tsv"
GSE180759_EXPR = ROOT / "data/raw/GSE180759_expression_matrix.csv.gz"
GSE180759_ANN = ROOT / "data/raw/GSE180759_annotation.txt.gz"
ST003328_DATA = ROOT / "data/raw_v3/wave66_metabolomics_workbench/ST003328/data.json"
ST003328_FACTORS = ROOT / "data/raw_v3/wave66_metabolomics_workbench/ST003328/factors.json"

STEROL_GENES = {
    "efflux_lxr": ["ABCA1", "ABCG1", "APOE", "NR1H3", "LXR", "CH25H"],
    "cholesterol_synthesis": ["HMGCR", "HMGCS1", "SQLE", "SREBF2", "LDLR", "INSIG1"],
    "lysosomal_cholesterol": ["LIPA", "NPC1", "NPC2", "CTSD", "LAMP1"],
}


def stream_selected_expression(genes: set[str]) -> pd.DataFrame:
    selected = {}
    with gzip.open(GSE180759_EXPR, "rt") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        # Header contains only nucleus IDs; data rows prepend the gene symbol.
        sample_cols = header
        for row in reader:
            gene = row[0]
            if gene in genes:
                selected[gene] = [float(x) if x else 0.0 for x in row[1:]]
    return pd.DataFrame(selected, index=sample_cols)


def load_annotation() -> pd.DataFrame:
    return pd.read_csv(GSE180759_ANN, sep="\t")


def hedges_g(a: list[float], b: list[float]) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    na, nb = len(a), len(b)
    pooled = math.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    if pooled == 0:
        return 0.0
    g = (a.mean() - b.mean()) / pooled
    correction = 1 - (3 / (4 * (na + nb) - 9))
    return float(g * correction)


v32_single = pd.read_csv(V32_SINGLE, sep="\t")
v32_joint = pd.read_csv(V32_JOINT, sep="\t")
metabolic_rows = v32_single[
    v32_single["confounder"].str.contains("glycolysis|oxphos|immunometabolism", case=False, regex=True)
].copy()
metabolic_rows.to_csv(OUTDIR / "v32_metabolic_single_panel_rows.tsv", sep="\t", index=False)
v32_joint[v32_joint["risk_set"] == "metabolic_inflammatory_stat1"].to_csv(
    OUTDIR / "v32_metabolic_joint_row.tsv", sep="\t", index=False
)

all_genes = {g for genes in STEROL_GENES.values() for g in genes}
expr = stream_selected_expression(all_genes)
ann = load_annotation()
ann = ann[ann["nucleus_barcode"].isin(expr.index)].set_index("nucleus_barcode")
expr = expr.loc[expr.index.intersection(ann.index)]

module_rows = []
for module, genes in STEROL_GENES.items():
    present = [g for g in genes if g in expr.columns]
    if not present:
        continue
    score = expr[present].mean(axis=1)
    tmp = ann[["pathology", "cell_type"]].copy()
    tmp["score"] = score
    for (pathology, cell_type), sub in tmp.groupby(["pathology", "cell_type"]):
        module_rows.append(
            {
                "module": module,
                "pathology": pathology,
                "cell_type": cell_type,
                "n_nuclei": int(len(sub)),
                "mean_score": float(sub["score"].mean()),
                "present_genes": ";".join(present),
            }
        )
module_df = pd.DataFrame(module_rows)
module_df.to_csv(OUTDIR / "sterol_gene_modules_by_pathology_celltype.tsv", sep="\t", index=False)

lesion_tests = []
for module in sorted(module_df["module"].unique()):
    tmp_scores = []
    present = [g for g in STEROL_GENES[module] if g in expr.columns]
    score = expr[present].mean(axis=1)
    tmp = ann[["pathology", "cell_type"]].copy()
    tmp["score"] = score
    immune = tmp[tmp["cell_type"] == "immune"]
    ca = immune[immune["pathology"] == "chronic_active_MS_lesion_edge"]["score"].tolist()
    ctrl = immune[immune["pathology"] == "control_white_matter"]["score"].tolist()
    if len(ca) >= 3 and len(ctrl) >= 3:
        lesion_tests.append(
            {
                "module": module,
                "comparison": "immune_chronic_active_edge_vs_control_white_matter",
                "n_chronic_active": len(ca),
                "n_control": len(ctrl),
                "mean_chronic_active": float(np.mean(ca)),
                "mean_control": float(np.mean(ctrl)),
                "hedges_g_active_minus_control": hedges_g(ca, ctrl),
                "welch_p": float(stats.ttest_ind(ca, ctrl, equal_var=False).pvalue),
                "present_genes": ";".join(present),
            }
        )
lesion_df = pd.DataFrame(lesion_tests)
lesion_df.to_csv(OUTDIR / "sterol_gene_lesion_edge_tests.tsv", sep="\t", index=False)

data = json.load(open(ST003328_DATA))
factors_raw = json.load(open(ST003328_FACTORS))
factors = {v["local_sample_id"]: v["factors"] for v in factors_raw.values()}
chol = next(v for v in data.values() if v.get("metabolite_name") == "cholesterol")
chol_rows = []
for sample, value in chol["DATA"].items():
    fac = factors[sample]
    status = fac.split("Disease status:")[1].split(" |")[0]
    treatment = fac.split("Treatment:")[1]
    chol_rows.append(
        {
            "sample": sample,
            "disease_status": status,
            "treatment": treatment,
            "cholesterol_peak_area": float(value),
            "log2_cholesterol": math.log2(float(value) + 1),
        }
    )
chol_df = pd.DataFrame(chol_rows)
chol_df.to_csv(OUTDIR / "st003328_cholesterol_values.tsv", sep="\t", index=False)

chol_tests = []
for treatment in sorted(chol_df["treatment"].unique()):
    pms = chol_df[(chol_df["disease_status"] == "PMS") & (chol_df["treatment"] == treatment)][
        "log2_cholesterol"
    ].tolist()
    amc = chol_df[(chol_df["disease_status"] == "AMC") & (chol_df["treatment"] == treatment)][
        "log2_cholesterol"
    ].tolist()
    chol_tests.append(
        {
            "comparison": f"PMS_vs_AMC_{treatment}",
            "n_pms": len(pms),
            "n_amc": len(amc),
            "mean_log2_pms": float(np.mean(pms)),
            "mean_log2_amc": float(np.mean(amc)),
            "delta_log2_pms_minus_amc": float(np.mean(pms) - np.mean(amc)),
            "hedges_g": hedges_g(pms, amc),
            "welch_p": float(stats.ttest_ind(pms, amc, equal_var=False).pvalue),
        }
    )
for status in sorted(chol_df["disease_status"].unique()):
    sv = chol_df[(chol_df["disease_status"] == status) & (chol_df["treatment"] == "SV")][
        "log2_cholesterol"
    ].tolist()
    untreated = chol_df[(chol_df["disease_status"] == status) & (chol_df["treatment"] == "untreated")][
        "log2_cholesterol"
    ].tolist()
    chol_tests.append(
        {
            "comparison": f"SV_vs_untreated_{status}",
            "n_pms": len(sv),
            "n_amc": len(untreated),
            "mean_log2_pms": float(np.mean(sv)),
            "mean_log2_amc": float(np.mean(untreated)),
            "delta_log2_pms_minus_amc": float(np.mean(sv) - np.mean(untreated)),
            "hedges_g": hedges_g(sv, untreated),
            "welch_p": float(stats.ttest_ind(sv, untreated, equal_var=False).pvalue),
        }
    )
chol_test_df = pd.DataFrame(chol_tests)
chol_test_df.to_csv(OUTDIR / "st003328_cholesterol_tests.tsv", sep="\t", index=False)

joint = v32_joint[v32_joint["risk_set"] == "metabolic_inflammatory_stat1"].iloc[0].to_dict()
summary = {
    "hypothesis": "metabolic/sterol setpoint",
    "grounded_result": "supported_as_context_axis_not_intervention_grade",
    "v32_metabolic_joint": {
        "raw_locked_auc": float(joint["raw_locked_auc"]),
        "joint_adjusted_auc": float(joint["joint_adjusted_auc"]),
        "auc_attenuation": float(joint["auc_attenuation"]),
        "joint_adjusted_permutation_p": float(joint["joint_adjusted_permutation_p"]),
        "verdict": joint["verdict"],
    },
    "metabolic_single_panels_n": int(len(metabolic_rows)),
    "st003328_cholesterol_tests": chol_tests,
    "sterol_lesion_edge_tests": lesion_tests,
    "interpretation": (
        "Metabolic/sterol state is a real context layer: V32 metabolic/"
        "inflammatory/STAT1 adjustment attenuates the monitoring signal, ST003328 "
        "shows higher cholesterol in progressive MS-derived neural stem-cell "
        "models and strong simvastatin lowering, and lesion-edge immune cells "
        "show sterol-handling transcript context. This is not yet a direct MS "
        "therapeutic hypothesis because current evidence mixes iNSC lipidomics, "
        "lesion transcript state, and treatment-response confounding rather than "
        "a unified APC-resolved causal sterol pathway."
    ),
    "minimum_next_test": [
        "APC-resolved MS blood/CSF or lesion lipidomics with oxysterols and cholesterol-efflux markers.",
        "Perturb LXR/ABCA1/ABCG1/CH25H/SREBF2 axis in APCs and measure APC/HLA-II response modules plus lipid output.",
        "Reject therapeutic interpretation if sterol signal remains tissue/metabolism-only and does not modulate APC remodeling after immune-tone adjustment.",
    ],
}
with (OUTDIR / "summary.json").open("w") as fh:
    json.dump(summary, fh, indent=2, sort_keys=True)
print(json.dumps(summary, indent=2, sort_keys=True))
