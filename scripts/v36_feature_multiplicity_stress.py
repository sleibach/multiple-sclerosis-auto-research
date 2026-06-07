#!/usr/bin/env python3
"""Multiplicity stress test across V36 generated patient-level features."""

from __future__ import annotations

import itertools
import json
import math
import pathlib

import pandas as pd


ROOT = pathlib.Path(__file__).resolve().parents[1]
V32 = ROOT / "analysis" / "v32_confounder_audit" / "v32_subject_confounder_scores.tsv"
BASEDELTA = ROOT / "analysis" / "v36_baseline_delta_decomposition" / "baseline_delta_scores.tsv"
SUBSTATE = ROOT / "analysis" / "v36_b_plasma_substate_audit" / "b_plasma_substate_paired_scores.tsv"
OUT = ROOT / "analysis" / "v36_feature_multiplicity_stress"


def auc_score(values: list[float], labels: list[int]) -> float:
    pos = [v for v, y in zip(values, labels) if y == 1]
    neg = [v for v, y in zip(values, labels) if y == 0]
    if not pos or not neg:
        return math.nan
    wins = 0.0
    for p in pos:
        for n in neg:
            if p > n:
                wins += 1.0
            elif p == n:
                wins += 0.5
    return wins / (len(pos) * len(neg))


def oriented_auc(values: list[float], labels: list[int]) -> float:
    auc = auc_score(values, labels)
    return max(auc, 1.0 - auc)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    v32 = pd.read_csv(V32, sep="\t")
    v32 = v32[v32["cohort"] == "GSE253006_TOF_exact"].copy()
    v32["label"] = (v32["response"] == "Responder").astype(int)
    base = v32[["patient", "label"]].copy()
    numeric_cols = [
        col
        for col in v32.columns
        if col
        not in {
            "cohort",
            "patient",
            "response",
            "baseline_sample",
            "treated_sample",
            "label",
        }
        and pd.api.types.is_numeric_dtype(v32[col])
    ]
    feature_frames = [base.set_index("patient")]
    feature_frames.append(v32.set_index("patient")[numeric_cols].add_prefix("v32__"))

    bd = pd.read_csv(BASEDELTA, sep="\t")
    for comp, frame in bd.groupby("compartment"):
        cols = [
            "baseline_IFN_APC",
            "treated_IFN_APC",
            "locked_delta_score",
            "baseline_HLAII",
            "treated_HLAII",
            "hla_delta_score",
        ]
        feature_frames.append(frame.set_index("patient")[cols].add_prefix(f"bd_{comp}__"))

    sub = pd.read_csv(SUBSTATE, sep="\t")
    candidate_sub_cols = [
        col
        for col in sub.columns
        if col.startswith("baseline_") or col.startswith("treated_") or col.startswith("delta_")
    ]
    sub_cols = [col for col in candidate_sub_cols if pd.api.types.is_numeric_dtype(sub[col])]
    feature_frames.append(sub.set_index("patient")[sub_cols].add_prefix("substate__"))

    mat = pd.concat(feature_frames, axis=1, join="inner")
    labels = mat["label"].astype(int).tolist()
    feature_cols = [col for col in mat.columns if col != "label"]
    feature_scores = []
    for col in feature_cols:
        vals = mat[col].astype(float).tolist()
        if any(pd.isna(vals)):
            continue
        feature_scores.append(
            {
                "feature": col,
                "oriented_auc": oriented_auc(vals, labels),
            }
        )
    feature_df = pd.DataFrame(feature_scores).sort_values("oriented_auc", ascending=False)
    feature_df.to_csv(OUT / "feature_auc_rank.tsv", sep="\t", index=False)
    observed_max = float(feature_df["oriented_auc"].max())
    max_rows = []
    n_pos = sum(labels)
    for pos_idx in itertools.combinations(range(len(labels)), n_pos):
        perm = [0] * len(labels)
        for idx in pos_idx:
            perm[idx] = 1
        max_auc = 0.0
        for col in feature_cols:
            vals = mat[col].astype(float).tolist()
            if any(pd.isna(vals)):
                continue
            max_auc = max(max_auc, oriented_auc(vals, perm))
        max_rows.append({"max_auc": max_auc})
    max_df = pd.DataFrame(max_rows)
    max_df.to_csv(OUT / "permutation_max_auc.tsv", sep="\t", index=False)
    empirical_p = float((max_df["max_auc"] >= observed_max - 1e-12).mean())
    summary = {
        "patients": int(len(mat)),
        "features_tested": int(len(feature_df)),
        "observed_max_auc": observed_max,
        "features_at_max_auc": int((feature_df["oriented_auc"] >= observed_max - 1e-12).sum()),
        "total_label_permutations": int(len(max_df)),
        "max_auc_empirical_p": empirical_p,
        "permutation_fraction_max_ge_0_95": float((max_df["max_auc"] >= 0.95 - 1e-12).mean()),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    lines = [
        "# V36 Feature Multiplicity Stress Test",
        "",
        "Status: **completed_exact_max_auc_null**.",
        "",
        f"- Patients: `{summary['patients']}`.",
        f"- Features tested: `{summary['features_tested']}`.",
        f"- Observed max AUC: `{summary['observed_max_auc']:.3f}`.",
        f"- Features at max AUC: `{summary['features_at_max_auc']}`.",
        f"- Label permutations: `{summary['total_label_permutations']}`.",
        f"- Empirical p for max AUC >= observed max: `{summary['max_auc_empirical_p']:.4f}`.",
        f"- Fraction of permutations with max AUC >= 0.95: `{summary['permutation_fraction_max_ge_0_95']:.4f}`.",
        "",
        "Top features:",
        "",
        "| Rank | Feature | AUC |",
        "|---:|---|---:|",
    ]
    for i, (_, row) in enumerate(feature_df.head(15).iterrows(), start=1):
        lines.append(f"| {i} | `{row['feature']}` | {row['oriented_auc']:.3f} |")
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- This controls only the post-hoc feature search within generated V36",
            "  patient-level features; it does not replace external replication.",
            "- If high max AUC is common under label permutations, perfect individual",
            "  features must be treated as exploratory rather than validated.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
