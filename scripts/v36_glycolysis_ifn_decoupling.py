#!/usr/bin/env python3
"""Test whether glycolysis is independent of IFN/STAT in GSE253006_TOF_exact."""

from __future__ import annotations

import itertools
import json
import math
import pathlib

import numpy as np
import pandas as pd


ROOT = pathlib.Path(__file__).resolve().parents[1]
V32 = ROOT / "analysis" / "v32_confounder_audit" / "v32_subject_confounder_scores.tsv"
OUT = ROOT / "analysis" / "v36_glycolysis_ifn_decoupling"


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


def exact_oriented(values: list[float], labels: list[int]) -> tuple[float, float]:
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
    return obs, ge / total


def residualize(y: np.ndarray, xs: list[np.ndarray]) -> np.ndarray:
    design = np.column_stack([np.ones(len(y)), *xs])
    beta, *_ = np.linalg.lstsq(design, y, rcond=None)
    return y - design @ beta


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(V32, sep="\t")
    df = df[df["cohort"] == "GSE253006_TOF_exact"].copy()
    df["label"] = (df["response"] == "Responder").astype(int)
    labels = df["label"].astype(int).tolist()
    features = {
        "delta_glycolysis": df["delta_glycolysis"].to_numpy(dtype=float),
        "delta_IFN_APC": df["delta_IFN_APC"].to_numpy(dtype=float),
        "delta_stat1_axis": df["delta_stat1_axis"].to_numpy(dtype=float),
        "delta_ifn_suppression_inverse_isg": df["delta_ifn_suppression_inverse_isg"].to_numpy(dtype=float),
    }
    rows: list[dict[str, object]] = []
    tests = {
        "glycolysis_raw": features["delta_glycolysis"],
        "ifn_apc_raw": features["delta_IFN_APC"],
        "stat1_axis_raw": features["delta_stat1_axis"],
        "glycolysis_resid_ifn_apc": residualize(
            features["delta_glycolysis"], [features["delta_IFN_APC"]]
        ),
        "glycolysis_resid_stat1": residualize(
            features["delta_glycolysis"], [features["delta_stat1_axis"]]
        ),
        "glycolysis_resid_ifn_and_stat1": residualize(
            features["delta_glycolysis"],
            [features["delta_IFN_APC"], features["delta_stat1_axis"]],
        ),
        "ifn_apc_resid_glycolysis": residualize(
            features["delta_IFN_APC"], [features["delta_glycolysis"]]
        ),
        "stat1_resid_glycolysis": residualize(
            features["delta_stat1_axis"], [features["delta_glycolysis"]]
        ),
    }
    for name, values in tests.items():
        auc, p = exact_oriented(values.astype(float).tolist(), labels)
        rows.append(
            {
                "test": name,
                "oriented_auc": auc,
                "exact_p": p,
                "mean_responders": float(np.mean(values[np.array(labels) == 1])),
                "mean_nonresponders": float(np.mean(values[np.array(labels) == 0])),
            }
        )
    result = pd.DataFrame(rows).sort_values(["exact_p", "oriented_auc"], ascending=[True, False])
    result.to_csv(OUT / "glycolysis_ifn_decoupling.tsv", sep="\t", index=False)
    corr_rows = []
    for a, b in itertools.combinations(features, 2):
        corr_rows.append(
            {
                "feature_a": a,
                "feature_b": b,
                "spearman": float(pd.Series(features[a]).corr(pd.Series(features[b]), method="spearman")),
                "pearson": float(pd.Series(features[a]).corr(pd.Series(features[b]), method="pearson")),
            }
        )
    corr = pd.DataFrame(corr_rows)
    corr.to_csv(OUT / "module_correlations.tsv", sep="\t", index=False)
    summary = {
        "patients": int(len(df)),
        "glycolysis_raw_auc": float(result[result["test"] == "glycolysis_raw"]["oriented_auc"].iloc[0]),
        "glycolysis_resid_ifn_stat1_auc": float(
            result[result["test"] == "glycolysis_resid_ifn_and_stat1"]["oriented_auc"].iloc[0]
        ),
        "ifn_apc_resid_glycolysis_auc": float(
            result[result["test"] == "ifn_apc_resid_glycolysis"]["oriented_auc"].iloc[0]
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    lines = [
        "# V36 Glycolysis-IFN Decoupling",
        "",
        "Status: **completed_subject_level_decoupling_test**.",
        "",
        f"- Patients: `{summary['patients']}`.",
        f"- Raw glycolysis AUC: `{summary['glycolysis_raw_auc']:.3f}`.",
        f"- Glycolysis residualized against IFN/APC + STAT1 AUC: `{summary['glycolysis_resid_ifn_stat1_auc']:.3f}`.",
        f"- IFN/APC residualized against glycolysis AUC: `{summary['ifn_apc_resid_glycolysis_auc']:.3f}`.",
        "",
        "| Test | AUC | Exact p |",
        "|---|---:|---:|",
    ]
    for _, row in result.iterrows():
        lines.append(f"| `{row['test']}` | {row['oriented_auc']:.3f} | {row['exact_p']:.4f} |")
    lines.extend(
        [
            "",
            "Module correlations:",
            "",
            "| Feature A | Feature B | Spearman | Pearson |",
            "|---|---|---:|---:|",
        ]
    )
    for _, row in corr.iterrows():
        lines.append(
            f"| `{row['feature_a']}` | `{row['feature_b']}` | {row['spearman']:.3f} | {row['pearson']:.3f} |"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- If glycolysis residualized against IFN/STAT collapses, glycolysis is not",
            "  an independent component of the response signal.",
            "- If IFN/APC residualized against glycolysis remains high, IFN/APC is the",
            "  more primary readout in this held data.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
