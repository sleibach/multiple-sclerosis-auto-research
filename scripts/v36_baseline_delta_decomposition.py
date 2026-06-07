#!/usr/bin/env python3
"""Decompose exact compartment readouts into baseline, treated, and delta signals."""

from __future__ import annotations

import itertools
import json
import math
import pathlib

import pandas as pd


ROOT = pathlib.Path(__file__).resolve().parents[1]
GENE_SCORES = (
    ROOT
    / "analysis"
    / "v23_apc_hla_monitoring"
    / "gse253006_exact_compartments"
    / "gse253006_exact_compartment_gene_scores.tsv"
)
PAIRED = (
    ROOT
    / "analysis"
    / "v23_apc_hla_monitoring"
    / "gse253006_exact_compartments"
    / "gse253006_exact_compartment_paired_scores.tsv"
)
OUT = ROOT / "analysis" / "v36_baseline_delta_decomposition"
IFN_APC = ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"]
HLAII = ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"]


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


def module_score(frame: pd.DataFrame, genes: list[str]) -> pd.Series:
    cols = [f"gene_{gene}" for gene in genes if f"gene_{gene}" in frame.columns]
    vals = frame[cols]
    z = (vals - vals.mean(axis=0)) / vals.std(axis=0).replace(0, pd.NA)
    return z.mean(axis=1)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    scores = pd.read_csv(GENE_SCORES, sep="\t")
    paired = pd.read_csv(PAIRED, sep="\t")
    by_key = {}
    module_rows = []
    for comp, frame in scores.groupby("marker_compartment"):
        frame = frame.copy()
        frame["module_IFN_APC"] = module_score(frame, IFN_APC)
        frame["module_HLAII"] = module_score(frame, HLAII)
        for _, row in frame.iterrows():
            by_key[(row["gsm"], comp)] = row
    rows: list[dict[str, object]] = []
    for _, pair in paired.iterrows():
        comp = pair["marker_compartment"]
        base = by_key[(pair["baseline_sample"], comp)]
        treated = by_key[(pair["treated_sample"], comp)]
        rows.append(
            {
                "patient": pair["patient"],
                "compartment": comp,
                "response": pair["response"],
                "label": 1 if pair["response"] == "Responder" else 0,
                "treated_timepoint": pair["treated_timepoint"],
                "baseline_IFN_APC": float(base["module_IFN_APC"]),
                "treated_IFN_APC": float(treated["module_IFN_APC"]),
                "locked_delta_score": float(-(treated["module_IFN_APC"] - base["module_IFN_APC"])),
                "baseline_HLAII": float(base["module_HLAII"]),
                "treated_HLAII": float(treated["module_HLAII"]),
                "hla_delta_score": float(-(treated["module_HLAII"] - base["module_HLAII"])),
            }
        )
    decomp = pd.DataFrame(rows)
    decomp.to_csv(OUT / "baseline_delta_scores.tsv", sep="\t", index=False)

    result_rows: list[dict[str, object]] = []
    features = [
        "baseline_IFN_APC",
        "treated_IFN_APC",
        "locked_delta_score",
        "baseline_HLAII",
        "treated_HLAII",
        "hla_delta_score",
    ]
    for comp, frame in decomp.groupby("compartment"):
        labels = frame["label"].astype(int).tolist()
        for feature in features:
            auc, p = exact_oriented(frame[feature].astype(float).tolist(), labels)
            result_rows.append(
                {
                    "compartment": comp,
                    "feature": feature,
                    "auc": auc,
                    "exact_p": p,
                }
            )
    result = pd.DataFrame(result_rows).sort_values(
        ["compartment", "auc"], ascending=[True, False]
    )
    result.to_csv(OUT / "baseline_delta_feature_auc.tsv", sep="\t", index=False)
    top_by_comp = result.groupby("compartment").head(1)
    summary = {
        "patients": int(decomp["patient"].nunique()),
        "compartments": int(decomp["compartment"].nunique()),
        "top_features": top_by_comp.to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    lines = [
        "# V36 Baseline-Versus-Delta Decomposition",
        "",
        "Status: **completed_monitoring_vs_baseline_audit**.",
        "",
        f"- Patients: `{summary['patients']}`.",
        f"- Compartments: `{summary['compartments']}`.",
        "",
        "| Compartment | Feature | AUC | Exact p |",
        "|---|---|---:|---:|",
    ]
    for _, row in result.iterrows():
        lines.append(
            f"| `{row['compartment']}` | `{row['feature']}` | {row['auc']:.3f} | {row['exact_p']:.4f} |"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- If baseline features match or beat delta, the readout is closer to",
            "  stratification than monitoring.",
            "- If delta/treatment features dominate, the monitoring interpretation is",
            "  better supported.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
