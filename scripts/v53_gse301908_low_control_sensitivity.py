#!/usr/bin/env python3
"""Run the pre-declared low-control GSE301908 CD44/CXCR4 sensitivity."""

from __future__ import annotations

import gzip
import json
import re
import subprocess
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v53_gse301908_low_control_sensitivity"
RDS = ROOT / "data/raw/GSE301908_sn_all.rds"
SOFT = ROOT / "data/raw/GSE284005_family.soft.gz"


def parse_soft() -> pd.DataFrame:
    records: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    with gzip.open(SOFT, "rt") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line.startswith("!Sample_title = "):
                if current is not None:
                    records.append(current)
                current = {"donor_id": line.split(" = ", 1)[1]}
            elif current is not None and line.startswith("!Sample_characteristics_ch1 = "):
                value = line.split(" = ", 1)[1]
                if ":" in value:
                    key, item = value.split(":", 1)
                    current[key.strip().lower().replace(" ", "_")] = item.strip()
    if current is not None:
        records.append(current)
    frame = pd.DataFrame(records)
    required = {"donor_id", "gender", "ms_duration", "age"}
    if missing := required - set(frame):
        raise ValueError(f"paired SOFT metadata missing fields: {sorted(missing)}")
    frame["age"] = pd.to_numeric(frame["age"])
    frame["sex_male"] = frame["gender"].str.lower().eq("male").astype(int)
    frame["soft_disease"] = np.where(pd.to_numeric(frame["ms_duration"]).eq(0), "ctrl", "patient")
    return frame[["donor_id", "age", "sex_male", "soft_disease"]]


def design(frame: pd.DataFrame, disease: np.ndarray) -> np.ndarray:
    age = frame.age.to_numpy(dtype=float)
    age_z = (age - age.mean()) / age.std(ddof=0)
    return np.column_stack(
        [np.ones(len(frame)), disease, age_z, age_z**2, frame.sex_male.to_numpy(dtype=float)]
    )


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    expression_path = OUT / "donor_target_gene_means.tsv"
    subprocess.run(
        [
            "Rscript",
            str(ROOT / "scripts/v53_export_gse301908_microglia_scores.R"),
            str(RDS),
            str(expression_path),
        ],
        check=True,
    )
    frame = pd.read_csv(expression_path, sep="\t").merge(
        parse_soft(), on="donor_id", how="left", validate="one_to_one"
    )
    if frame[["age", "sex_male", "soft_disease"]].isna().any().any():
        raise ValueError("incomplete paired SOFT metadata")
    if not frame.diagnosis.eq(frame.soft_disease).all():
        raise ValueError("RDS and paired SOFT diagnosis disagree")
    frame["disease_binary"] = frame.diagnosis.eq("patient").astype(int)

    genes = ["CD44", "CXCR4"]
    z = (frame[genes] - frame[genes].mean()) / frame[genes].std(ddof=0)
    frame["receptor_cd44_cxcr4"] = z.mean(axis=1)
    y = frame.receptor_cd44_cxcr4.to_numpy(dtype=float)
    observed_disease = frame.disease_binary.to_numpy(dtype=float)
    observed_design = design(frame, observed_disease)
    if np.linalg.matrix_rank(observed_design) != observed_design.shape[1]:
        raise ValueError("observed low-control design is rank deficient")
    model = sm.OLS(y, observed_design).fit(cov_type="HC3")
    beta = float(model.params[1])
    ci = model.conf_int()[1]

    permutation_betas = []
    for control_indices in combinations(range(len(frame)), 3):
        disease = np.ones(len(frame), dtype=float)
        disease[list(control_indices)] = 0.0
        candidate = design(frame, disease)
        if np.linalg.matrix_rank(candidate) != candidate.shape[1]:
            continue
        permutation_betas.append(float((np.linalg.pinv(candidate) @ y)[1]))
    null = np.asarray(permutation_betas)
    exact_p = float(np.mean(np.abs(null) >= abs(beta) - 1e-12))
    observed_rank = int(np.sum(np.abs(null) >= abs(beta) - 1e-12))

    control = frame.loc[frame.disease_binary.eq(0), "receptor_cd44_cxcr4"]
    ms = frame.loc[frame.disease_binary.eq(1), "receptor_cd44_cxcr4"]
    score_count_rho = float(frame[["receptor_cd44_cxcr4", "n_microglia"]].corr(method="spearman").iloc[0, 1])
    summary = {
        "purpose": "Pre-declared GSE301908 low-control sensitivity; not clean replication",
        "assay_layer": "Seurat RNA normalized data; raw counts absent",
        "n_donors": len(frame),
        "n_ms": int(frame.disease_binary.sum()),
        "n_control": int((1 - frame.disease_binary).sum()),
        "n_microglia": int(frame.n_microglia.sum()),
        "primary_adjusted_beta": beta,
        "primary_hc3_se": float(model.bse[1]),
        "primary_hc3_ci_low": float(ci[0]),
        "primary_hc3_ci_high": float(ci[1]),
        "primary_hc3_p": float(model.pvalues[1]),
        "exact_label_assignments_tested": len(null),
        "exact_two_sided_label_p": exact_p,
        "exact_null_exceedances": observed_rank,
        "raw_ms_minus_control": float(ms.mean() - control.mean()),
        "score_microglia_count_spearman_rho": score_count_rho,
        "verdict": (
            "POSITIVE_LOW_CONTROL_SENSITIVITY"
            if beta > 0 and exact_p <= 0.10 and ci[0] > 0
            else "LOW_CONTROL_SENSITIVITY_NOT_SUPPORTED"
        ),
        "boundary": (
            "Only three controls, normalized-data-only assay, and no clean frozen-platform "
            "match. This cohort cannot be counted as independent replication regardless of "
            "the observed direction or p-value."
        ),
    }
    frame.to_csv(OUT / "donor_scores.tsv", sep="\t", index=False)
    pd.DataFrame({"permuted_disease_beta": null}).to_csv(
        OUT / "exact_label_null.tsv", sep="\t", index=False
    )
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 GSE301908 Low-Control Sensitivity",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"The held object contributes `{summary['n_ms']}` MS and only",
        f"`{summary['n_control']}` control donors (`{summary['n_microglia']:,}` deposited",
        "Micro nuclei). Its RNA assay contains normalized `data` but no raw-count layer,",
        "so the test averages deposited normalized expression per donor and applies the",
        "unchanged CD44/CXCR4 z-score as a platform-mismatched sensitivity.",
        "",
        f"Disease beta after age, quadratic age, and sex adjustment is `{beta:.3f}`",
        f"(HC3 CI `{ci[0]:.3f}` to `{ci[1]:.3f}`, p `{model.pvalues[1]:.4g}`).",
        f"The exact null enumerates `{len(null)}` full-rank placements of three controls;",
        f"two-sided p is `{exact_p:.4f}`. Score/microglia-count Spearman rho is",
        f"`{score_count_rho:.3f}`.",
        "",
        "Regardless of direction, three controls cannot satisfy the frozen replication",
        "definition or support a mechanism, stage claim, monitoring rule, intervention",
        "direction, or target. The result is retained only as a low-control sensitivity.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
