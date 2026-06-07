#!/usr/bin/env python3
"""Ground V36 adversarial cross-exam items with held data."""

from __future__ import annotations

import json
import pathlib

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_deep_cross_exam"
TB = {"t_cell_like", "b_plasma_like"}


def oriented_auc(labels, values) -> float:
    auc = roc_auc_score(labels, values)
    return max(float(auc), float(1 - auc))


def tb_bootstrap(seed: int = 3607, n_boot: int = 5000) -> dict:
    rng = np.random.default_rng(seed)
    metrics = pd.read_csv(ROOT / "analysis/v36_tb_gate_artifact_audit/compartment_count_artifact_metrics.tsv", sep="\t")
    df = pd.read_csv(ROOT / "analysis/v36_tb_gate_artifact_audit/paired_scores_with_count_proxies.tsv", sep="\t")
    residual_feature = "locked_score_residualized_against_baseline_and_delta_fraction"
    # Map residualized AUC already computed by compartment for point estimate.
    residual = metrics[metrics["feature"] == residual_feature].copy()
    point_gap = (
        residual[residual["class"] == "T/B-like"]["auc_oriented"].mean()
        - residual[residual["class"] == "non-T/B-like"]["auc_oriented"].mean()
    )
    patient_ids = sorted(df["patient"].unique())
    boot_gaps = []
    for _ in range(n_boot):
        sampled = rng.choice(patient_ids, size=len(patient_ids), replace=True)
        parts = []
        for i, patient in enumerate(sampled):
            sub = df[df["patient"] == patient].copy()
            sub["boot_patient"] = f"{patient}_{i}"
            parts.append(sub)
        boot = pd.concat(parts, ignore_index=True)
        rows = []
        for comp, sub in boot.groupby("marker_compartment"):
            labels = sub["label"].tolist()
            if len(set(labels)) < 2:
                continue
            vals = sub["locked_signed_score"].astype(float).tolist()
            # Bootstrap uses raw locked score because residualized per-boot refit would
            # be unstable in n=9 and already audited separately.
            rows.append(
                {
                    "compartment": comp,
                    "class": "T/B-like" if comp in TB else "non-T/B-like",
                    "auc": oriented_auc(labels, vals),
                }
            )
        frame = pd.DataFrame(rows)
        if not frame.empty and set(frame["class"]) == {"T/B-like", "non-T/B-like"}:
            boot_gaps.append(
                frame[frame["class"] == "T/B-like"]["auc"].mean()
                - frame[frame["class"] == "non-T/B-like"]["auc"].mean()
            )
    arr = np.array(boot_gaps)
    pd.DataFrame({"tb_minus_non_tb_gap": arr}).to_csv(OUT / "tb_gap_bootstrap.tsv", sep="\t", index=False)
    return {
        "test": "patient bootstrap of raw locked T/B-minus-non-T/B AUC gap",
        "point_residualized_gap": float(point_gap),
        "bootstrap_raw_gap_mean": float(arr.mean()),
        "bootstrap_raw_gap_ci_low": float(np.quantile(arr, 0.025)),
        "bootstrap_raw_gap_ci_high": float(np.quantile(arr, 0.975)),
        "bootstrap_p_gap_le_zero": float(np.mean(arr <= 0)),
        "n_bootstrap": int(len(arr)),
    }


def b_only_vs_tb() -> dict:
    paired = pd.read_csv(
        ROOT / "analysis/v36_tb_gate_artifact_audit/paired_scores_with_count_proxies.tsv",
        sep="\t",
    )
    labels_by_patient = paired.drop_duplicates("patient").set_index("patient")["label"].to_dict()
    wide = paired.pivot(index="patient", columns="marker_compartment", values="locked_signed_score")
    labels = [labels_by_patient[p] for p in wide.index]
    b_score = wide["b_plasma_like"].tolist()
    t_score = wide["t_cell_like"].tolist()
    tb_mean = wide[["b_plasma_like", "t_cell_like"]].mean(axis=1).tolist()
    return {
        "test": "B/plasma-only versus T-cell-only versus T/B mean locked score",
        "b_plasma_auc": oriented_auc(labels, b_score),
        "t_cell_auc": oriented_auc(labels, t_score),
        "tb_mean_auc": oriented_auc(labels, tb_mean),
        "interpretation": "B/plasma-only retains most of the T/B signal; combined T/B does not outperform the best single T/B component in n=9.",
    }


def postpartum_component_correlation() -> dict:
    scores = pd.read_csv(ROOT / "analysis/v35_gse17410_pregnancy_apc/sample_module_scores.tsv", sep="\t")
    corr = scores[["hla_ii_score", "cd64_score"]].corr(method="spearman").iloc[0, 1]
    return {
        "test": "MS pregnancy-phase HLA-II and CD64 component separability",
        "spearman_hla_ii_vs_cd64_all_samples": float(corr),
        "n_samples": int(len(scores)),
        "interpretation": "The metric combines separable arms; it should be reported as component-wise HLA-II and CD64 plus the difference, not as a single opaque score.",
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    results = {
        "claude_status": "empty_output_file_in_this_round",
        "gemini_status": "usable_fenced_json",
        "grounded_items": [tb_bootstrap(), b_only_vs_tb(), postpartum_component_correlation()],
    }
    (OUT / "grounded_cross_exam.json").write_text(json.dumps(results, indent=2, sort_keys=True))
    lines = [
        "# V36 Deep Cross-Exam Grounding",
        "",
        "- Claude status: empty output file in this round.",
        "- Gemini status: usable fenced JSON critique.",
        "",
    ]
    for item in results["grounded_items"]:
        lines.append(f"## {item['test']}")
        lines.append("")
        for k, v in item.items():
            if k == "test":
                continue
            lines.append(f"- {k}: `{v}`")
        lines.append("")
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
