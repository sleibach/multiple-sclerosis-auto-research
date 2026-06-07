#!/usr/bin/env python3
"""T-vs-B/plasma concordance audit for V36 compartment readability wording."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_tb_readability_concordance"


def spearman_permutation_p(x: np.ndarray, y: np.ndarray, observed: float, n_perm: int = 20000) -> float:
    rng = np.random.default_rng(20260607)
    extreme = 0
    for _ in range(n_perm):
        rho = stats.spearmanr(x, rng.permutation(y)).statistic
        if abs(float(rho)) >= abs(observed) - 1e-12:
            extreme += 1
    return float((extreme + 1) / (n_perm + 1))


def sign_concordance(a: np.ndarray, b: np.ndarray) -> float:
    keep = (a != 0) & (b != 0)
    if keep.sum() == 0:
        return math.nan
    return float((np.sign(a[keep]) == np.sign(b[keep])).mean())


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    clean = df.copy()
    for col in clean.columns:
        clean[col] = clean[col].map(lambda x: f"{x:.4g}" if isinstance(x, float) and np.isfinite(x) else x)
    header = "| " + " | ".join(clean.columns.astype(str)) + " |"
    sep = "| " + " | ".join(["---"] * len(clean.columns)) + " |"
    rows = ["| " + " | ".join(str(x) for x in row) + " |" for row in clean.to_numpy()]
    return "\n".join([header, sep, *rows])


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    path = ROOT / "analysis/v23_apc_hla_monitoring/gse253006_exact_compartments/gse253006_exact_compartment_paired_scores.tsv"
    df = pd.read_csv(path, sep="\t")
    keep = df[df["marker_compartment"].isin(["t_cell_like", "b_plasma_like"])].copy()
    wide = keep.pivot(index=["patient", "response"], columns="marker_compartment", values=["locked_signed_score", "delta_IFN_APC", "delta_HLAII", "delta_RECEPTOR"])
    wide.columns = [f"{feature}__{compartment}" for feature, compartment in wide.columns]
    wide = wide.reset_index()
    wide["response_binary"] = wide["response"].eq("Responder").astype(int)
    wide.to_csv(OUT / "tb_wide_scores.tsv", sep="\t", index=False)

    rows: list[dict[str, object]] = []
    for feature in ["locked_signed_score", "delta_IFN_APC", "delta_HLAII", "delta_RECEPTOR"]:
        t_col = f"{feature}__t_cell_like"
        b_col = f"{feature}__b_plasma_like"
        sub = wide.dropna(subset=[t_col, b_col])
        x = sub[t_col].to_numpy(float)
        y = sub[b_col].to_numpy(float)
        rho = float(stats.spearmanr(x, y).statistic)
        pearson = float(stats.pearsonr(x, y).statistic)
        rows.append(
            {
                "feature": feature,
                "n_patients": int(len(sub)),
                "spearman_rho_t_vs_bplasma": rho,
                "spearman_permutation_two_sided_p": spearman_permutation_p(x, y, rho),
                "pearson_r_t_vs_bplasma": pearson,
                "sign_concordance": sign_concordance(x, y),
                "responder_mean_t": float(sub.loc[sub["response_binary"].eq(1), t_col].mean()),
                "nonresponder_mean_t": float(sub.loc[sub["response_binary"].eq(0), t_col].mean()),
                "responder_mean_bplasma": float(sub.loc[sub["response_binary"].eq(1), b_col].mean()),
                "nonresponder_mean_bplasma": float(sub.loc[sub["response_binary"].eq(0), b_col].mean()),
            }
        )
    result = pd.DataFrame(rows)
    result.to_csv(OUT / "tb_readability_concordance.tsv", sep="\t", index=False)
    locked = result[result["feature"].eq("locked_signed_score")].iloc[0].to_dict()
    summary = {
        "question": "Do T-cell and B/plasma readouts rank the same patients similarly?",
        "n_patients": int(wide.shape[0]),
        "locked_signed_score": locked,
        "interpretation": "Cross-compartment readability is supported as a qualitative descriptor if rho/sign concordance are positive, but remains single-cohort exploratory.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = [
        "# V36 T/B Readability Concordance",
        "",
        "This grounds a Claude-proposed falsification test: if the V36 readout is",
        "really readable in both T-like and B/plasma-like compartments, the same",
        "patients should rank similarly across compartments.",
        "",
        markdown_table(result),
        "",
        "Interpretation: positive concordance supports only the wording that the",
        "broad IFN/APC/STAT1 response is T/B-readable. It does not make the",
        "compartment readouts independent mechanisms and does not override the",
        "multiplicity and single-cohort caveats.",
    ]
    (OUT / "summary.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
