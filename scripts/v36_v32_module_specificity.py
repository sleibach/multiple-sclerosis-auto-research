#!/usr/bin/env python3
"""Compare V32 modules in GSE253006_TOF_exact for V36 specificity."""

from __future__ import annotations

import itertools
import json
import math
import pathlib

import pandas as pd


ROOT = pathlib.Path(__file__).resolve().parents[1]
V32 = ROOT / "analysis" / "v32_confounder_audit" / "v32_subject_confounder_scores.tsv"
OUT = ROOT / "analysis" / "v36_v32_module_specificity"


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


def exact_oriented(values: list[float], labels: list[int]) -> tuple[float, float, int, int]:
    raw = auc_score(values, labels)
    obs = max(raw, 1.0 - raw)
    n_pos = sum(labels)
    ge = 0
    total = 0
    for pos_idx in itertools.combinations(range(len(labels)), n_pos):
        perm = [0] * len(labels)
        for idx in pos_idx:
            perm[idx] = 1
        auc = auc_score(values, perm)
        if max(auc, 1.0 - auc) >= obs - 1e-12:
            ge += 1
        total += 1
    return raw, obs, ge, total


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(V32, sep="\t")
    df = df[df["cohort"] == "GSE253006_TOF_exact"].copy()
    df["label"] = (df["response"] == "Responder").astype(int)
    labels = df["label"].astype(int).tolist()
    exclude = {
        "cohort",
        "patient",
        "response",
        "baseline_sample",
        "treated_sample",
        "label",
    }
    numeric = [
        col
        for col in df.columns
        if col not in exclude and pd.api.types.is_numeric_dtype(df[col])
    ]
    rows = []
    for col in numeric:
        vals = df[col].astype(float).tolist()
        raw, oriented, ge, total = exact_oriented(vals, labels)
        rows.append(
            {
                "module_feature": col,
                "raw_auc_high_in_responders": raw,
                "oriented_auc": oriented,
                "same_or_better_permutations": ge,
                "total_permutations": total,
                "exact_p": ge / total,
                "mean_responders": df.loc[df["label"] == 1, col].mean(),
                "mean_nonresponders": df.loc[df["label"] == 0, col].mean(),
                "direction_in_responders": "higher" if raw >= 0.5 else "lower",
            }
        )
    result = pd.DataFrame(rows).sort_values(
        ["exact_p", "oriented_auc"], ascending=[True, False]
    )
    result["rank"] = range(1, len(result) + 1)
    result.to_csv(OUT / "v32_module_specificity.tsv", sep="\t", index=False)
    top = result.head(12)
    ifn_features = result[
        result["module_feature"].str.contains("IFN_APC|stat1_axis|ifn_suppression", case=False)
    ].copy()
    summary = {
        "patients": int(len(df)),
        "features_tested": int(len(result)),
        "top_feature": str(result.iloc[0]["module_feature"]),
        "top_auc": float(result.iloc[0]["oriented_auc"]),
        "top_exact_p": float(result.iloc[0]["exact_p"]),
        "ifn_feature_ranks": ifn_features[["module_feature", "rank", "oriented_auc", "exact_p"]].to_dict(
            orient="records"
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    lines = [
        "# V36 V32 Module Specificity",
        "",
        "Status: **completed_subject_level_module_specificity_scan**.",
        "",
        f"- Patients: `{summary['patients']}`.",
        f"- V32 numeric features tested: `{summary['features_tested']}`.",
        f"- Top feature: `{summary['top_feature']}` (AUC `{summary['top_auc']:.3f}`, exact p `{summary['top_exact_p']:.4f}`).",
        "",
        "Top module features:",
        "",
        "| Rank | Feature | AUC | Exact p | Direction in responders |",
        "|---:|---|---:|---:|---|",
    ]
    for _, row in top.iterrows():
        lines.append(
            f"| {int(row['rank'])} | `{row['module_feature']}` | {row['oriented_auc']:.3f} | "
            f"{row['exact_p']:.4f} | {row['direction_in_responders']} |"
        )
    lines.extend(
        [
            "",
            "IFN/STAT-related feature ranks:",
            "",
            "| Feature | Rank | AUC | Exact p |",
            "|---|---:|---:|---:|",
        ]
    )
    for _, row in ifn_features.iterrows():
        lines.append(
            f"| `{row['module_feature']}` | {int(row['rank'])} | {row['oriented_auc']:.3f} | {row['exact_p']:.4f} |"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- This is a subject-level module scan over V32 panels in the exact",
            "  tofacitinib cohort.",
            "- If many non-IFN modules tie the IFN/STAT modules, the response state is",
            "  broad immune/metabolic remodeling rather than IFN-specific.",
            "- Exact p-values are discrete at n=9 and should be interpreted as ranking",
            "  and stress-testing, not validation.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
