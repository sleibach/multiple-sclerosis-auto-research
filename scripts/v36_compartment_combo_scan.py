#!/usr/bin/env python3
"""Exhaustive compartment-combination scan for V36 T/B lead."""

from __future__ import annotations

import itertools
import json
import pathlib

import pandas as pd
from sklearn.metrics import roc_auc_score


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_compartment_combo_scan"


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
        ROOT / "analysis/v23_apc_hla_monitoring/gse253006_exact_compartments/gse253006_exact_compartment_paired_scores.tsv",
        sep="\t",
    )
    labels = paired.drop_duplicates("patient").set_index("patient")["response"].eq("Responder").astype(int)
    wide = paired.pivot(index="patient", columns="marker_compartment", values="locked_signed_score").loc[labels.index]
    comps = list(wide.columns)
    rows = []
    for r in range(1, len(comps) + 1):
        for combo in itertools.combinations(comps, r):
            values = wide[list(combo)].mean(axis=1).tolist()
            lab = labels.tolist()
            auc = oriented_auc(lab, values)
            rows.append(
                {
                    "combo": ";".join(combo),
                    "n_compartments": r,
                    "auc_oriented": auc,
                    "exact_perm_p_auc_ge_observed": exact_perm_p(lab, values, auc),
                    "is_tb_only": set(combo).issubset({"t_cell_like", "b_plasma_like"}),
                    "includes_b_plasma": "b_plasma_like" in combo,
                    "includes_t_cell": "t_cell_like" in combo,
                }
            )
    result = pd.DataFrame(rows).sort_values(
        ["auc_oriented", "n_compartments"], ascending=[False, True]
    )
    result.to_csv(OUT / "compartment_combo_scan.tsv", sep="\t", index=False)
    best = result.iloc[0].to_dict()
    tb_mean = result[result["combo"] == "b_plasma_like;t_cell_like"].iloc[0].to_dict()
    b = result[result["combo"] == "b_plasma_like"].iloc[0].to_dict()
    t = result[result["combo"] == "t_cell_like"].iloc[0].to_dict()
    summary = {
        "hypothesis": "exhaustive compartment combination scan",
        "n_combinations": int(len(result)),
        "best_combo": best,
        "b_plasma_only": b,
        "t_cell_only": t,
        "tb_mean": tb_mean,
        "grounded_result": "single_t_cell_tops_auc_but_b_plasma_matches_tb_mean_and_is_more_residualization_stable",
        "interpretation": (
            "The highest raw AUC is the single T-cell compartment, but V36 residualization showed the T-cell signal is composition-sensitive. "
            "B/plasma-only matches the two-compartment T/B mean AUC and remained more stable after count/fraction adjustment."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    lines = [
        "# V36 Compartment Combination Scan",
        "",
        f"Status: **{summary['grounded_result']}**.",
        "",
        f"- Combinations tested: `{summary['n_combinations']}`.",
        f"- Best raw combo: `{best['combo']}`, AUC `{best['auc_oriented']:.3f}`, exact p `{best['exact_perm_p_auc_ge_observed']:.4f}`.",
        f"- B/plasma only: AUC `{b['auc_oriented']:.3f}`, exact p `{b['exact_perm_p_auc_ge_observed']:.4f}`.",
        f"- T-cell only: AUC `{t['auc_oriented']:.3f}`, exact p `{t['exact_perm_p_auc_ge_observed']:.4f}`.",
        f"- T/B mean: AUC `{tb_mean['auc_oriented']:.3f}`, exact p `{tb_mean['exact_perm_p_auc_ge_observed']:.4f}`.",
        "",
        "Interpretation:",
        "",
        summary["interpretation"],
    ]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
