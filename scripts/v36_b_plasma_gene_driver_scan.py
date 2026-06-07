#!/usr/bin/env python3
"""Scan gene-level drivers of the V36 B/plasma IFN/APC carrier."""

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
OUT = ROOT / "analysis" / "v36_b_plasma_gene_driver_scan"


def auc_score(values: list[float], labels: list[int]) -> float:
    pos = [v for v, y in zip(values, labels) if y == 1]
    neg = [v for v, y in zip(values, labels) if y == 0]
    wins = 0.0
    total = len(pos) * len(neg)
    if total == 0:
        return math.nan
    for p in pos:
        for n in neg:
            if p > n:
                wins += 1.0
            elif p == n:
                wins += 0.5
    return wins / total


def exact_p_oriented(values: list[float], labels: list[int]) -> tuple[float, float, float]:
    """Return raw AUC, oriented AUC, exact same-case-count permutation p."""
    raw = auc_score(values, labels)
    obs = max(raw, 1.0 - raw)
    n = len(labels)
    n_pos = sum(labels)
    ge = 0
    total = 0
    for pos_idx in itertools.combinations(range(n), n_pos):
        perm = [0] * n
        for idx in pos_idx:
            perm[idx] = 1
        val = auc_score(values, perm)
        if max(val, 1.0 - val) >= obs - 1e-12:
            ge += 1
        total += 1
    return raw, obs, ge / total


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    genes_df = pd.read_csv(GENE_SCORES, sep="\t")
    paired = pd.read_csv(PAIRED, sep="\t")
    paired = paired[paired["marker_compartment"] == "b_plasma_like"].copy()
    b = genes_df[genes_df["marker_compartment"] == "b_plasma_like"].copy()
    by_gsm = b.set_index("gsm")
    gene_cols = [c for c in b.columns if c.startswith("gene_")]
    rows: list[dict[str, object]] = []
    paired_rows: list[dict[str, object]] = []

    for _, pair in paired.iterrows():
        baseline = by_gsm.loc[pair["baseline_sample"]]
        treated = by_gsm.loc[pair["treated_sample"]]
        row: dict[str, object] = {
            "patient": pair["patient"],
            "response": pair["response"],
            "label": 1 if pair["response"] == "Responder" else 0,
            "treated_timepoint": pair["treated_timepoint"],
        }
        for col in gene_cols:
            gene = col.removeprefix("gene_")
            row[f"delta_{gene}"] = float(treated[col]) - float(baseline[col])
        paired_rows.append(row)
    deltas = pd.DataFrame(paired_rows)
    deltas.to_csv(OUT / "b_plasma_gene_deltas.tsv", sep="\t", index=False)

    labels = deltas["label"].astype(int).tolist()
    for col in [c for c in deltas.columns if c.startswith("delta_")]:
        gene = col.removeprefix("delta_")
        vals = deltas[col].astype(float).tolist()
        raw_auc, oriented_auc, exact_p = exact_p_oriented(vals, labels)
        # The locked response score uses -delta IFN/APC. This reports whether
        # response is associated with downshift (raw AUC < 0.5) or upshift.
        signed_score_auc, _, _ = exact_p_oriented([-v for v in vals], labels)
        loo_oriented: list[float] = []
        for i in range(len(vals)):
            loo_vals = vals[:i] + vals[i + 1 :]
            loo_labels = labels[:i] + labels[i + 1 :]
            _, loo_auc, _ = exact_p_oriented(loo_vals, loo_labels)
            loo_oriented.append(loo_auc)
        rows.append(
            {
                "gene": gene,
                "raw_auc_delta_high_in_responders": raw_auc,
                "auc_minus_delta_high_in_responders": signed_score_auc,
                "oriented_auc": oriented_auc,
                "exact_p_oriented": exact_p,
                "mean_delta_responders": deltas.loc[deltas["label"] == 1, col].mean(),
                "mean_delta_nonresponders": deltas.loc[deltas["label"] == 0, col].mean(),
                "direction_in_responders": "downshift" if raw_auc < 0.5 else "upshift",
                "loo_min_oriented_auc": min(loo_oriented),
                "loo_max_oriented_auc": max(loo_oriented),
            }
        )
    result = pd.DataFrame(rows).sort_values(
        ["exact_p_oriented", "oriented_auc"], ascending=[True, False]
    )
    result.to_csv(OUT / "b_plasma_gene_driver_scan.tsv", sep="\t", index=False)

    top = result.head(8)
    n_sig = int((result["exact_p_oriented"] <= 0.05).sum())
    n_oriented_09 = int((result["oriented_auc"] >= 0.9).sum())
    summary = {
        "patients": int(len(deltas)),
        "responders": int(sum(labels)),
        "nonresponders": int(len(labels) - sum(labels)),
        "genes_tested": int(len(result)),
        "genes_exact_p_le_0_05": n_sig,
        "genes_oriented_auc_ge_0_9": n_oriented_09,
        "top_gene": str(top.iloc[0]["gene"]),
        "top_gene_oriented_auc": float(top.iloc[0]["oriented_auc"]),
        "top_gene_exact_p": float(top.iloc[0]["exact_p_oriented"]),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    lines = [
        "# V36 B/Plasma Gene Driver Scan",
        "",
        "Status: **completed_gene_level_driver_audit**.",
        "",
        f"- Patients: `{summary['patients']}` "
        f"({summary['responders']}` responders, `{summary['nonresponders']}` non-responders).",
        f"- Genes tested: `{summary['genes_tested']}` locked module genes.",
        f"- Genes with oriented AUC >= 0.9: `{summary['genes_oriented_auc_ge_0_9']}`.",
        f"- Genes with exact oriented permutation p <= 0.05: `{summary['genes_exact_p_le_0_05']}`.",
        "",
        "Top genes:",
        "",
        "| Gene | Oriented AUC | Exact p | Direction in responders | LOO min AUC |",
        "|---|---:|---:|---|---:|",
    ]
    for _, row in top.iterrows():
        lines.append(
            f"| `{row['gene']}` | {row['oriented_auc']:.3f} | "
            f"{row['exact_p_oriented']:.4f} | {row['direction_in_responders']} | "
            f"{row['loo_min_oriented_auc']:.3f} |"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- This is a driver audit, not independent validation.",
            "- A broad carrier would show multiple locked IFN/APC genes moving in",
            "  the responder-associated direction rather than a single idiosyncratic",
            "  gene dominating the score.",
            "- Leave-one-out sensitivity is reported because n=9 makes single-patient",
            "  leverage a major risk.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
