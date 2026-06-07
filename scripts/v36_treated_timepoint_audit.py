#!/usr/bin/env python3
"""Audit timepoint structure for V36 treated IFN/APC readouts."""

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
OUT = ROOT / "analysis" / "v36_treated_timepoint_audit"
IFN_APC = ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"]


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


def module_score(frame: pd.DataFrame) -> pd.Series:
    cols = [f"gene_{gene}" for gene in IFN_APC if f"gene_{gene}" in frame.columns]
    vals = frame[cols]
    z = (vals - vals.mean(axis=0)) / vals.std(axis=0).replace(0, pd.NA)
    return z.mean(axis=1)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(GENE_SCORES, sep="\t")
    df = df[df["marker_compartment"].ne("ambiguous")].copy()
    scored = []
    order = {"W0": 0, "W8": 8, "W16": 16, "W24": 24, "W48": 48}
    for comp, frame in df.groupby("marker_compartment"):
        frame = frame.copy()
        frame["ifn_apc_score"] = module_score(frame)
        scored.append(frame)
    scored_df = pd.concat(scored, ignore_index=True)
    scored_df["label"] = scored_df["responder"].astype(bool).astype(int)
    scored_df["time_order"] = scored_df["timepoint_norm"].map(order)
    scored_df.to_csv(OUT / "timepoint_ifn_apc_scores.tsv", sep="\t", index=False)

    rows: list[dict[str, object]] = []
    for comp, comp_df in scored_df.groupby("marker_compartment"):
        for tp, frame in comp_df.groupby("timepoint_norm"):
            labels = frame["label"].astype(int).tolist()
            if len(frame) >= 4 and len(set(labels)) == 2:
                auc, p = exact_oriented(frame["ifn_apc_score"].astype(float).tolist(), labels)
            else:
                auc, p = math.nan, math.nan
            rows.append(
                {
                    "compartment": comp,
                    "timepoint": tp,
                    "n": int(len(frame)),
                    "responders": int(sum(labels)),
                    "nonresponders": int(len(labels) - sum(labels)),
                    "treated_ifn_apc_auc": auc,
                    "exact_p": p,
                }
            )
    result = pd.DataFrame(rows).sort_values(["compartment", "timepoint"])
    result.to_csv(OUT / "timepoint_auc.tsv", sep="\t", index=False)

    # Patient trajectory summaries in b/plasma and T-cell for compact reporting.
    traj = scored_df[scored_df["marker_compartment"].isin(["b_plasma_like", "t_cell_like"])][
        ["patient", "responder", "marker_compartment", "timepoint_norm", "ifn_apc_score"]
    ].sort_values(["marker_compartment", "patient", "timepoint_norm"])
    traj.to_csv(OUT / "btcell_ifn_apc_trajectories.tsv", sep="\t", index=False)
    w8 = result[result["timepoint"] == "W8"].copy()
    summary = {
        "patients_total": int(scored_df["patient"].nunique()),
        "w8_rows": w8.to_dict(orient="records"),
        "timepoints": sorted(scored_df["timepoint_norm"].dropna().unique().tolist()),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    lines = [
        "# V36 Treated-Timepoint Audit",
        "",
        "Status: **completed_sparse_trajectory_audit**.",
        "",
        f"- Patients total: `{summary['patients_total']}`.",
        f"- Timepoints present: `{', '.join(summary['timepoints'])}`.",
        "",
        "AUC by compartment and timepoint:",
        "",
        "| Compartment | Timepoint | n | responders | AUC | Exact p |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for _, row in result.iterrows():
        auc = "" if math.isnan(row["treated_ifn_apc_auc"]) else f"{row['treated_ifn_apc_auc']:.3f}"
        p = "" if math.isnan(row["exact_p"]) else f"{row['exact_p']:.4f}"
        lines.append(
            f"| `{row['compartment']}` | `{row['timepoint']}` | {int(row['n'])} | "
            f"{int(row['responders'])} | {auc} | {p} |"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- W8 is the only post-baseline timepoint with enough mixed responder status",
            "  for a minimally interpretable early-monitoring check.",
            "- Later timepoints are sparse/imbalanced and should be treated as",
            "  trajectory context only, not validation.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
