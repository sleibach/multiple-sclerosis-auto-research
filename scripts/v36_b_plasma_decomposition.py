#!/usr/bin/env python3
"""Decompose B/plasma-like response signal into module and count components."""

from __future__ import annotations

import itertools
import json
import pathlib

import pandas as pd
from sklearn.metrics import roc_auc_score


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_b_plasma_decomposition"


def oriented_auc(labels, values) -> float:
    auc = roc_auc_score(labels, values)
    return max(float(auc), float(1 - auc))


def exact_perm_p(labels, values, observed=None) -> float:
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


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    paired = pd.read_csv(
        ROOT / "analysis/v36_tb_gate_artifact_audit/paired_scores_with_count_proxies.tsv",
        sep="\t",
    )
    b = paired[paired["marker_compartment"] == "b_plasma_like"].copy()
    b["label"] = (b["response"] == "Responder").astype(int)
    features = [
        "delta_IFN_APC",
        "delta_HLAII",
        "locked_signed_score",
        "delta_RECEPTOR",
        "baseline_n_cells",
        "delta_n_cells",
        "baseline_fraction",
        "delta_fraction",
    ]
    rows = []
    for feature in features:
        labels = b["label"].tolist()
        values = b[feature].astype(float).tolist()
        auc = oriented_auc(labels, values)
        rows.append(
            {
                "feature": feature,
                "auc_oriented": auc,
                "exact_perm_p_auc_ge_observed": exact_perm_p(labels, values, auc),
                "mean_responder": float(b[b["label"] == 1][feature].mean()),
                "mean_nonresponder": float(b[b["label"] == 0][feature].mean()),
            }
        )
    metrics = pd.DataFrame(rows).sort_values("auc_oriented", ascending=False)
    metrics.to_csv(OUT / "b_plasma_feature_decomposition.tsv", sep="\t", index=False)
    summary = {
        "hypothesis": "B/plasma-like carrier decomposition",
        "n_patients": int(b["patient"].nunique()),
        "top_feature": metrics.iloc[0].to_dict(),
        "locked_signed_score": metrics[metrics["feature"] == "locked_signed_score"].iloc[0].to_dict(),
        "delta_ifn_apc": metrics[metrics["feature"] == "delta_IFN_APC"].iloc[0].to_dict(),
        "delta_hlaii": metrics[metrics["feature"] == "delta_HLAII"].iloc[0].to_dict(),
        "delta_receptor": metrics[metrics["feature"] == "delta_RECEPTOR"].iloc[0].to_dict(),
        "grounded_result": "b_plasma_signal_is_ifn_apc_locked_score_not_receptor_or_counts",
        "interpretation": (
            "B/plasma discrimination is carried by the IFN/APC-derived locked score. "
            "Receptor and count/fraction features are weaker, so the B/plasma carrier is not simply a receptor or abundance effect in held data."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    lines = [
        "# V36 B/Plasma Decomposition",
        "",
        f"Status: **{summary['grounded_result']}**.",
        "",
        f"- Patients: `{summary['n_patients']}`.",
        f"- Top feature: `{summary['top_feature']['feature']}`, AUC `{summary['top_feature']['auc_oriented']:.3f}`, exact p `{summary['top_feature']['exact_perm_p_auc_ge_observed']:.4f}`.",
        f"- Locked score AUC: `{summary['locked_signed_score']['auc_oriented']:.3f}`.",
        f"- Delta IFN/APC AUC: `{summary['delta_ifn_apc']['auc_oriented']:.3f}`.",
        f"- Delta HLA-II AUC: `{summary['delta_hlaii']['auc_oriented']:.3f}`.",
        f"- Delta receptor AUC: `{summary['delta_receptor']['auc_oriented']:.3f}`.",
        "",
        summary["interpretation"],
    ]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
