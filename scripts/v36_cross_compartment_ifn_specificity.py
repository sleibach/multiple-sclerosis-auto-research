#!/usr/bin/env python3
"""Cross-compartment specificity scan for V36 STAT1/IFN response signal."""

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
OUT = ROOT / "analysis" / "v36_cross_compartment_ifn_specificity"


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


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    genes = pd.read_csv(GENE_SCORES, sep="\t").set_index(["gsm", "marker_compartment"])
    paired = pd.read_csv(PAIRED, sep="\t")
    paired["label"] = (paired["response"] == "Responder").astype(int)
    rows: list[dict[str, object]] = []
    deltas: list[dict[str, object]] = []
    gene_features = ["STAT1", "IRF1", "GBP1", "ISG15", "CD74", "HLA-DRA"]

    for _, pair in paired.iterrows():
        comp = pair["marker_compartment"]
        base_key = (pair["baseline_sample"], comp)
        treated_key = (pair["treated_sample"], comp)
        if base_key not in genes.index or treated_key not in genes.index:
            continue
        base = genes.loc[base_key]
        treated = genes.loc[treated_key]
        row: dict[str, object] = {
            "patient": pair["patient"],
            "compartment": comp,
            "response": pair["response"],
            "label": int(pair["label"]),
            "treated_timepoint": pair["treated_timepoint"],
            "locked_signed_score": float(pair["locked_signed_score"]),
            "delta_IFN_APC": float(pair["delta_IFN_APC"]),
            "delta_HLAII": float(pair["delta_HLAII"]),
        }
        for gene in gene_features:
            row[f"delta_{gene}"] = float(treated[f"gene_{gene}"]) - float(base[f"gene_{gene}"])
        deltas.append(row)
    delta_df = pd.DataFrame(deltas)
    delta_df.to_csv(OUT / "cross_compartment_gene_deltas.tsv", sep="\t", index=False)

    for comp, frame in delta_df.groupby("compartment"):
        labels = frame["label"].astype(int).tolist()
        for feature, signed in [
            ("locked_signed_score", False),
            ("delta_IFN_APC", True),
            ("delta_STAT1", True),
            ("delta_IRF1", True),
            ("delta_GBP1", True),
            ("delta_ISG15", True),
            ("delta_CD74", True),
            ("delta_HLA-DRA", True),
            ("delta_HLAII", True),
        ]:
            vals = frame[feature].astype(float).tolist()
            if signed:
                vals = [-v for v in vals]
            auc, p = exact_oriented(vals, labels)
            rows.append(
                {
                    "compartment": comp,
                    "feature": feature,
                    "n": int(len(frame)),
                    "responders": int(sum(labels)),
                    "nonresponders": int(len(labels) - sum(labels)),
                    "oriented_auc": auc,
                    "exact_p": p,
                }
            )
    result = pd.DataFrame(rows).sort_values(
        ["feature", "oriented_auc"], ascending=[True, False]
    )
    result.to_csv(OUT / "cross_compartment_ifn_specificity.tsv", sep="\t", index=False)

    stat1 = result[result["feature"] == "delta_STAT1"].sort_values(
        "oriented_auc", ascending=False
    )
    locked = result[result["feature"] == "locked_signed_score"].sort_values(
        "oriented_auc", ascending=False
    )
    summary = {
        "compartments": int(result["compartment"].nunique()),
        "patients_per_compartment": int(result["n"].max()),
        "top_stat1_compartment": str(stat1.iloc[0]["compartment"]),
        "top_stat1_auc": float(stat1.iloc[0]["oriented_auc"]),
        "top_stat1_exact_p": float(stat1.iloc[0]["exact_p"]),
        "top_locked_compartment": str(locked.iloc[0]["compartment"]),
        "top_locked_auc": float(locked.iloc[0]["oriented_auc"]),
        "top_locked_exact_p": float(locked.iloc[0]["exact_p"]),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    lines = [
        "# V36 Cross-Compartment IFN Specificity",
        "",
        "Status: **completed_specificity_scan**.",
        "",
        f"- Compartments tested: `{summary['compartments']}`.",
        f"- Patients per compartment: `{summary['patients_per_compartment']}`.",
        f"- Top STAT1 compartment: `{summary['top_stat1_compartment']}` "
        f"(AUC `{summary['top_stat1_auc']:.3f}`, exact p `{summary['top_stat1_exact_p']:.4f}`).",
        f"- Top locked-score compartment: `{summary['top_locked_compartment']}` "
        f"(AUC `{summary['top_locked_auc']:.3f}`, exact p `{summary['top_locked_exact_p']:.4f}`).",
        "",
        "STAT1 downshift by compartment:",
        "",
        "| Compartment | AUC | Exact p |",
        "|---|---:|---:|",
    ]
    for _, row in stat1.iterrows():
        lines.append(
            f"| `{row['compartment']}` | {row['oriented_auc']:.3f} | {row['exact_p']:.4f} |"
        )
    lines.extend(
        [
            "",
            "Locked score by compartment:",
            "",
            "| Compartment | AUC | Exact p |",
            "|---|---:|---:|",
        ]
    )
    for _, row in locked.iterrows():
        lines.append(
            f"| `{row['compartment']}` | {row['oriented_auc']:.3f} | {row['exact_p']:.4f} |"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- If STAT1 downshift is high across many compartments, the B/plasma",
            "  carrier is likely a compartment-resolved view of generic IFN response.",
            "- If B/plasma is selectively high after comparison with other compartments,",
            "  the carrier interpretation is more specific.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
