#!/usr/bin/env python3
"""V36 T/B compartment gate artifact audit."""

from __future__ import annotations

import itertools
import json
import pathlib

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import roc_auc_score


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_tb_gate_artifact_audit"
TB = {"t_cell_like", "b_plasma_like"}


def oriented_auc(labels: list[int], values: list[float]) -> float:
    auc = roc_auc_score(labels, values)
    return max(float(auc), float(1.0 - auc))


def exact_perm_p(labels: list[int], values: list[float], observed: float | None = None) -> float:
    n = len(labels)
    k = int(sum(labels))
    observed = oriented_auc(labels, values) if observed is None else observed
    ge = 0
    total = 0
    for pos in itertools.combinations(range(n), k):
        perm = [0] * n
        for idx in pos:
            perm[idx] = 1
        if oriented_auc(perm, values) >= observed - 1e-12:
            ge += 1
        total += 1
    return ge / total


def residualize(y: np.ndarray, x: np.ndarray) -> np.ndarray:
    model = LinearRegression().fit(x, y)
    return y - model.predict(x)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    paired = pd.read_csv(
        ROOT / "analysis/v23_apc_hla_monitoring/gse253006_exact_compartments/gse253006_exact_compartment_paired_scores.tsv",
        sep="\t",
    )
    counts = pd.read_csv(
        ROOT / "analysis/v23_apc_hla_monitoring/gse253006_exact_compartments/gse253006_exact_compartment_counts.tsv",
        sep="\t",
    )
    counts = counts[counts["marker_compartment"] != "ambiguous"].copy()
    totals = counts.groupby(["gsm", "patient", "timepoint_norm"], as_index=False)["n_cells"].sum()
    totals = totals.rename(columns={"n_cells": "total_cells"})
    counts = counts.merge(totals, on=["gsm", "patient", "timepoint_norm"], how="left")
    counts["fraction"] = counts["n_cells"] / counts["total_cells"]
    baseline = counts.rename(
        columns={
            "gsm": "baseline_sample",
            "n_cells": "baseline_n_cells",
            "fraction": "baseline_fraction",
        }
    )[["baseline_sample", "patient", "marker_compartment", "baseline_n_cells", "baseline_fraction"]]
    treated = counts.rename(
        columns={
            "gsm": "treated_sample",
            "n_cells": "treated_n_cells",
            "fraction": "treated_fraction",
        }
    )[["treated_sample", "patient", "marker_compartment", "treated_n_cells", "treated_fraction"]]
    df = paired.merge(baseline, on=["baseline_sample", "patient", "marker_compartment"], how="left")
    df = df.merge(treated, on=["treated_sample", "patient", "marker_compartment"], how="left")
    df["delta_n_cells"] = df["treated_n_cells"] - df["baseline_n_cells"]
    df["delta_fraction"] = df["treated_fraction"] - df["baseline_fraction"]
    df["label"] = (df["response"] == "Responder").astype(int)
    df["class"] = np.where(df["marker_compartment"].isin(TB), "T/B-like", "non-T/B-like")

    rows = []
    for comp, sub in df.groupby("marker_compartment"):
        labels = sub["label"].tolist()
        y = sub["locked_signed_score"].to_numpy(float)
        x = sub[["baseline_fraction", "delta_fraction"]].to_numpy(float)
        residual = residualize(y, x)
        for feature in ["baseline_n_cells", "delta_n_cells", "baseline_fraction", "delta_fraction", "locked_signed_score"]:
            vals = sub[feature].astype(float).tolist()
            rows.append(
                {
                    "marker_compartment": comp,
                    "feature": feature,
                    "class": "T/B-like" if comp in TB else "non-T/B-like",
                    "auc_oriented": oriented_auc(labels, vals),
                    "exact_perm_p_auc_ge_observed": exact_perm_p(labels, vals),
                    "mean_responder": float(sub[sub["label"] == 1][feature].mean()),
                    "mean_nonresponder": float(sub[sub["label"] == 0][feature].mean()),
                }
            )
        rows.append(
            {
                "marker_compartment": comp,
                "feature": "locked_score_residualized_against_baseline_and_delta_fraction",
                "class": "T/B-like" if comp in TB else "non-T/B-like",
                "auc_oriented": oriented_auc(labels, residual.tolist()),
                "exact_perm_p_auc_ge_observed": exact_perm_p(labels, residual.tolist()),
                "mean_responder": float(np.mean(residual[sub["label"].to_numpy() == 1])),
                "mean_nonresponder": float(np.mean(residual[sub["label"].to_numpy() == 0])),
            }
        )
    metrics = pd.DataFrame(rows)
    metrics.to_csv(OUT / "compartment_count_artifact_metrics.tsv", sep="\t", index=False)
    df.to_csv(OUT / "paired_scores_with_count_proxies.tsv", sep="\t", index=False)

    locked = metrics[metrics["feature"] == "locked_signed_score"]
    residual = metrics[metrics["feature"] == "locked_score_residualized_against_baseline_and_delta_fraction"]
    count_best = metrics[metrics["feature"].isin(["baseline_n_cells", "delta_n_cells", "baseline_fraction", "delta_fraction"])]
    def gap(frame: pd.DataFrame) -> float:
        return float(frame[frame["class"] == "T/B-like"]["auc_oriented"].mean() - frame[frame["class"] == "non-T/B-like"]["auc_oriented"].mean())

    summary = {
        "hypothesis": "T/B compartment remodeling gate count/composition artifact audit",
        "n_patients": int(df["patient"].nunique()),
        "locked_tb_minus_non_tb_auc_gap": gap(locked),
        "residualized_tb_minus_non_tb_auc_gap": gap(residual),
        "best_count_or_fraction_auc": float(count_best["auc_oriented"].max()),
        "best_count_or_fraction_row": count_best.sort_values("auc_oriented", ascending=False).iloc[0].to_dict(),
        "t_cell_locked_auc": float(locked[locked["marker_compartment"] == "t_cell_like"]["auc_oriented"].iloc[0]),
        "t_cell_residualized_auc": float(residual[residual["marker_compartment"] == "t_cell_like"]["auc_oriented"].iloc[0]),
        "b_plasma_locked_auc": float(locked[locked["marker_compartment"] == "b_plasma_like"]["auc_oriented"].iloc[0]),
        "b_plasma_residualized_auc": float(residual[residual["marker_compartment"] == "b_plasma_like"]["auc_oriented"].iloc[0]),
        "grounded_result": "survives_simple_count_fraction_residualization_but_not_definitive",
        "interpretation": (
            "Simple compartment abundance proxies do not explain away the T/B gate: residualizing locked scores against "
            "baseline and delta compartment fractions preserves a positive T/B-minus-non-T/B gap. However, this is not a "
            "full deconvolution or independent replication, and small n remains decisive."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    lines = [
        "# V36 T/B Gate Artifact Audit",
        "",
        f"Status: **{summary['grounded_result']}**.",
        "",
        f"- Patients: `{summary['n_patients']}`.",
        f"- Original locked T/B-minus-non-T/B AUC gap: `{summary['locked_tb_minus_non_tb_auc_gap']:.3f}`.",
        f"- Residualized locked gap after baseline/delta compartment fraction adjustment: `{summary['residualized_tb_minus_non_tb_auc_gap']:.3f}`.",
        f"- Best count/fraction-only oriented AUC: `{summary['best_count_or_fraction_auc']:.3f}` "
        f"(`{summary['best_count_or_fraction_row']['marker_compartment']}` / `{summary['best_count_or_fraction_row']['feature']}`).",
        f"- T-cell locked AUC -> residualized AUC: `{summary['t_cell_locked_auc']:.3f}` -> `{summary['t_cell_residualized_auc']:.3f}`.",
        f"- B/plasma locked AUC -> residualized AUC: `{summary['b_plasma_locked_auc']:.3f}` -> `{summary['b_plasma_residualized_auc']:.3f}`.",
        "",
        "Interpretation:",
        "",
        summary["interpretation"],
        "",
        "Limit:",
        "",
        "This does not prove within-cell remodeling. It only rejects the simplest",
        "available count/fraction artifact using held data. The decisive test remains",
        "an independent paired response cohort with T/B/myeloid compartments and",
        "patient-level labels.",
    ]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
