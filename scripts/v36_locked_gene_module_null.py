#!/usr/bin/env python3
"""Empirical module-combination null using locked genes in GSE253006 compartments."""

from __future__ import annotations

import itertools
import json
import math
import pathlib

import pandas as pd


ROOT = pathlib.Path(__file__).resolve().parents[1]
DELTAS = ROOT / "analysis" / "v36_cross_compartment_ifn_specificity" / "cross_compartment_gene_deltas.tsv"
OUT = ROOT / "analysis" / "v36_locked_gene_module_null"
IFN_STAT = ("STAT1", "IRF1", "GBP1", "ISG15")


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


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DELTAS, sep="\t")
    module_cols = {"delta_IFN_APC", "delta_HLAII"}
    genes = sorted(
        [
            c.removeprefix("delta_")
            for c in df.columns
            if c.startswith("delta_") and c not in module_cols
        ]
    )
    combo_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    for comp, frame in df.groupby("compartment"):
        labels = frame["label"].astype(int).tolist()
        comp_combo_rows = []
        for combo in itertools.combinations(genes, len(IFN_STAT)):
            score = -frame[[f"delta_{gene}" for gene in combo]].mean(axis=1)
            auc = auc_score(score.astype(float).tolist(), labels)
            row = {
                "compartment": comp,
                "combo": ",".join(combo),
                "is_ifn_stat": int(set(combo) == set(IFN_STAT)),
                "auc": auc,
            }
            combo_rows.append(row)
            comp_combo_rows.append(row)
        comp_df = pd.DataFrame(comp_combo_rows)
        ifn_auc = float(comp_df.loc[comp_df["is_ifn_stat"] == 1, "auc"].iloc[0])
        ge = int((comp_df["auc"] >= ifn_auc - 1e-12).sum())
        total = int(len(comp_df))
        summary_rows.append(
            {
                "compartment": comp,
                "ifn_stat_auc": ifn_auc,
                "combos_same_or_better": ge,
                "total_combos": total,
                "empirical_combo_p": ge / total,
                "percentile": float((comp_df["auc"] < ifn_auc).mean()),
                "best_combo": str(comp_df.sort_values("auc", ascending=False).iloc[0]["combo"]),
                "best_combo_auc": float(comp_df["auc"].max()),
            }
        )
    combo_df = pd.DataFrame(combo_rows)
    combo_df.to_csv(OUT / "locked_gene_four_gene_combos.tsv", sep="\t", index=False)
    summary_df = pd.DataFrame(summary_rows).sort_values("ifn_stat_auc", ascending=False)
    summary_df.to_csv(OUT / "ifn_stat_empirical_null.tsv", sep="\t", index=False)
    top = summary_df.iloc[0].to_dict()
    summary = {
        "genes_available": len(genes),
        "combo_size": len(IFN_STAT),
        "combos_per_compartment": int(summary_df["total_combos"].iloc[0]),
        "ifn_stat_genes": list(IFN_STAT),
        "top_ifn_stat_compartment": str(top["compartment"]),
        "top_ifn_stat_auc": float(top["ifn_stat_auc"]),
        "top_ifn_stat_empirical_p": float(top["empirical_combo_p"]),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    lines = [
        "# V36 Locked-Gene Module Null",
        "",
        "Status: **completed_limited_empirical_null**.",
        "",
        "Important limitation: the exact compartment matrix contains the locked",
        "module genes, not a full transcriptome. This control compares the IFN/STAT",
        "four-gene set against all same-size combinations of the available locked",
        "genes; it is not a genome-wide random-gene null.",
        "",
        f"- Available genes: `{summary['genes_available']}`.",
        f"- Combo size: `{summary['combo_size']}`.",
        f"- Combos per compartment: `{summary['combos_per_compartment']}`.",
        f"- IFN/STAT set: `{', '.join(IFN_STAT)}`.",
        "",
        "| Compartment | IFN/STAT AUC | Empirical combo p | Same/better combos | Best combo | Best AUC |",
        "|---|---:|---:|---:|---|---:|",
    ]
    for _, row in summary_df.iterrows():
        lines.append(
            f"| `{row['compartment']}` | {row['ifn_stat_auc']:.3f} | "
            f"{row['empirical_combo_p']:.4f} | {int(row['combos_same_or_better'])}/"
            f"{int(row['total_combos'])} | `{row['best_combo']}` | {row['best_combo_auc']:.3f} |"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- If the IFN/STAT set sits near the top of this locked-gene combination",
            "  null, the signal is not trivially reproduced by arbitrary locked genes.",
            "- If many same-size combinations match or beat it, the apparent module",
            "  specificity is weak within the measured gene set.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
