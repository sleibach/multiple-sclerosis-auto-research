#!/usr/bin/env python3
"""Test C15ORF48/MOCCI versus NDUFA4 switch pattern in local V3 datasets."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave20_c15orf48_ndufa4_switch"
SEED = 20260527


def read_tsv(path: str) -> pd.DataFrame:
    full = ROOT / path
    if not full.exists():
        return pd.DataFrame()
    return pd.read_csv(full, sep="\t")


def classify(row: pd.Series) -> str:
    c_delta = float(row["c15orf48_delta"])
    n_delta = float(row["ndufa4_delta"])
    c_p = float(row["c15orf48_p"])
    n_p = float(row["ndufa4_p"])
    if c_delta > 0.2 and c_p < 0.10 and n_delta < -0.2 and n_p < 0.10:
        return "canonical_switch_c15_up_ndufa4_down"
    if c_delta > 0.2 and c_p < 0.10 and n_delta <= 0.2:
        return "c15_up_no_ndufa4_up"
    if c_delta > 0.2 and c_p < 0.10 and n_delta > 0.2:
        return "both_up_not_switch"
    if n_delta > 0.2 and n_p < 0.10:
        return "ndufa4_up_without_c15"
    return "no_switch_signal"


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    broad = read_tsv("phases/v3/results/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv")
    ms = read_tsv("phases/v3/results/gse111972_full_ms_wm_signature.tsv")
    if broad.empty:
        raise FileNotFoundError("broad_h5ad_gene_contrasts.tsv missing")

    sub = broad[broad["gene"].isin(["C15ORF48", "NDUFA4"])].copy()
    pivot = sub.pivot_table(
        index=["analysis", "dataset_path", "disease_name", "compartment", "role"],
        columns="gene",
        values=[
            "delta_log2_cpm",
            "hedges_g",
            "p",
            "fdr",
            "mean_case_log2_cpm",
            "mean_control_log2_cpm",
            "n_case_donors",
            "n_control_donors",
        ],
        aggfunc="first",
    )
    pivot.columns = [f"{gene.lower()}_{metric}" for metric, gene in pivot.columns]
    pivot = pivot.reset_index()
    pivot = pivot.rename(
        columns={
            "c15orf48_delta_log2_cpm": "c15orf48_delta",
            "ndufa4_delta_log2_cpm": "ndufa4_delta",
            "c15orf48_p": "c15orf48_p",
            "ndufa4_p": "ndufa4_p",
            "c15orf48_fdr": "c15orf48_fdr",
            "ndufa4_fdr": "ndufa4_fdr",
            "c15orf48_hedges_g": "c15orf48_hedges_g",
            "ndufa4_hedges_g": "ndufa4_hedges_g",
        }
    )
    required = ["c15orf48_delta", "ndufa4_delta", "c15orf48_p", "ndufa4_p"]
    pivot = pivot.dropna(subset=required).copy()
    pivot["switch_delta_c15_minus_ndufa4"] = pivot["c15orf48_delta"] - pivot["ndufa4_delta"]
    pivot["switch_call"] = pivot.apply(classify, axis=1)
    pivot = pivot.sort_values(["switch_call", "switch_delta_c15_minus_ndufa4"], ascending=[True, False])

    ms_rows = []
    if not ms.empty and {"gene", "delta_log2", "p", "fdr", "hedges_g"}.issubset(ms.columns):
        ms_sub = ms[ms["gene"].isin(["C15ORF48", "NDUFA4"])].copy()
        vals = ms_sub.set_index("gene")
        if {"C15ORF48", "NDUFA4"}.issubset(vals.index):
            c = vals.loc["C15ORF48"]
            n = vals.loc["NDUFA4"]
            ms_row = {
                "analysis": "GSE111972_MS_WM_microglia",
                "dataset": "data/raw_v3/gse111972/GSE111972_norm_data.txt.gz",
                "disease_name": "MS",
                "compartment": "white matter microglia",
                "role": "ms_anchor",
                "c15orf48_delta": float(c["delta_log2"]),
                "ndufa4_delta": float(n["delta_log2"]),
                "c15orf48_p": float(c["p"]),
                "ndufa4_p": float(n["p"]),
                "c15orf48_fdr": float(c["fdr"]),
                "ndufa4_fdr": float(n["fdr"]),
                "c15orf48_hedges_g": float(c["hedges_g"]),
                "ndufa4_hedges_g": float(n["hedges_g"]),
            }
            ms_row["switch_delta_c15_minus_ndufa4"] = ms_row["c15orf48_delta"] - ms_row["ndufa4_delta"]
            ms_row["switch_call"] = classify(pd.Series(ms_row))
            ms_rows.append(ms_row)

    out = pd.concat([pivot, pd.DataFrame(ms_rows)], ignore_index=True, sort=False)
    out.to_csv(OUT / "c15orf48_ndufa4_switch_by_compartment.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "n_compartments": int(len(out)),
        "switch_calls": out["switch_call"].value_counts().to_dict(),
        "canonical_switch_compartments": out[out["switch_call"].eq("canonical_switch_c15_up_ndufa4_down")]
        .to_dict(orient="records"),
        "c15_up_no_ndufa4_up_compartments": out[out["switch_call"].eq("c15_up_no_ndufa4_up")]
        .sort_values("switch_delta_c15_minus_ndufa4", ascending=False)
        .head(20)
        .to_dict(orient="records"),
        "interpretation": (
            "C15ORF48/MOCCI induction is locally recurrent, but the canonical "
            "C15ORF48-up/NDUFA4-down switch is required for a strong local "
            "complex-IV subunit-switch claim."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
