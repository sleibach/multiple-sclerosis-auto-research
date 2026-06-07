#!/usr/bin/env python3
"""Ground IFN independence and leave-one-gene dependence tests for V36."""

from __future__ import annotations

import itertools
import json
import math
import pathlib

import numpy as np
import pandas as pd
from scipy import stats


ROOT = pathlib.Path(__file__).resolve().parents[1]
DELTAS = ROOT / "analysis" / "v36_cross_compartment_ifn_specificity" / "cross_compartment_gene_deltas.tsv"
OUT = ROOT / "analysis" / "v36_ifn_independence_dependence"
IFN_STAT = ["STAT1", "IRF1", "GBP1", "ISG15"]


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


def residualize(y: np.ndarray, x: np.ndarray) -> np.ndarray:
    design = np.column_stack([np.ones(len(x)), x])
    beta, *_ = np.linalg.lstsq(design, y, rcond=None)
    return y - design @ beta


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DELTAS, sep="\t")
    rows: list[dict[str, object]] = []
    for comp, frame in df.groupby("compartment"):
        score = -frame[[f"delta_{gene}" for gene in IFN_STAT]].mean(axis=1)
        for patient, label, value in zip(frame["patient"], frame["label"], score):
            rows.append(
                {
                    "patient": patient,
                    "compartment": comp,
                    "label": int(label),
                    "ifn_stat_score": float(value),
                }
            )
    scores = pd.DataFrame(rows)
    wide = scores.pivot(index=["patient", "label"], columns="compartment", values="ifn_stat_score")
    wide = wide.reset_index()
    wide.to_csv(OUT / "ifn_stat_scores_by_compartment.tsv", sep="\t", index=False)

    b = wide["b_plasma_like"].to_numpy(dtype=float)
    my = wide["myeloid_apc_like"].to_numpy(dtype=float)
    labels = wide["label"].astype(int).tolist()
    pearson = stats.pearsonr(b, my)
    spearman = stats.spearmanr(b, my)
    b_auc, b_p = exact_oriented(b.tolist(), labels)
    my_auc, my_p = exact_oriented(my.tolist(), labels)
    b_resid = residualize(b, my)
    b_resid_auc, b_resid_p = exact_oriented(b_resid.tolist(), labels)
    my_resid = residualize(my, b)
    my_resid_auc, my_resid_p = exact_oriented(my_resid.tolist(), labels)

    # Leave-one-gene dependence in B/plasma.
    delta = df[df["compartment"] == "b_plasma_like"].copy()
    gene_rows: list[dict[str, object]] = []
    full = -delta[[f"delta_{gene}" for gene in IFN_STAT]].mean(axis=1)
    full_auc, full_p = exact_oriented(full.astype(float).tolist(), labels)
    gene_rows.append(
        {
            "score": "full_ifn_stat",
            "genes": ",".join(IFN_STAT),
            "auc": full_auc,
            "exact_p": full_p,
        }
    )
    for omitted in IFN_STAT:
        kept = [gene for gene in IFN_STAT if gene != omitted]
        score = -delta[[f"delta_{gene}" for gene in kept]].mean(axis=1)
        auc, p = exact_oriented(score.astype(float).tolist(), labels)
        gene_rows.append(
            {
                "score": f"omit_{omitted}",
                "genes": ",".join(kept),
                "auc": auc,
                "exact_p": p,
            }
        )
    for gene in IFN_STAT:
        score = -delta[f"delta_{gene}"]
        auc, p = exact_oriented(score.astype(float).tolist(), labels)
        gene_rows.append(
            {
                "score": f"single_{gene}",
                "genes": gene,
                "auc": auc,
                "exact_p": p,
            }
        )
    gene_df = pd.DataFrame(gene_rows)
    gene_df.to_csv(OUT / "b_plasma_ifn_stat_leave_gene.tsv", sep="\t", index=False)

    summary = {
        "patients": int(len(wide)),
        "b_myeloid_pearson_r": float(pearson.statistic),
        "b_myeloid_pearson_p": float(pearson.pvalue),
        "b_myeloid_spearman_r": float(spearman.statistic),
        "b_myeloid_spearman_p": float(spearman.pvalue),
        "b_plasma_ifn_stat_auc": float(b_auc),
        "b_plasma_ifn_stat_exact_p": float(b_p),
        "myeloid_ifn_stat_auc": float(my_auc),
        "myeloid_ifn_stat_exact_p": float(my_p),
        "b_residual_after_myeloid_auc": float(b_resid_auc),
        "b_residual_after_myeloid_exact_p": float(b_resid_p),
        "myeloid_residual_after_b_auc": float(my_resid_auc),
        "myeloid_residual_after_b_exact_p": float(my_resid_p),
        "min_omit_one_gene_auc": float(
            gene_df[gene_df["score"].str.startswith("omit_")]["auc"].min()
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    lines = [
        "# V36 IFN Independence and Gene Dependence",
        "",
        "Status: **completed_grounding_of_two_lineage_proposals**.",
        "",
        f"- Patients: `{summary['patients']}`.",
        f"- B/plasma vs myeloid IFN/STAT Pearson r: `{summary['b_myeloid_pearson_r']:.3f}` "
        f"(p `{summary['b_myeloid_pearson_p']:.4f}`).",
        f"- B/plasma vs myeloid IFN/STAT Spearman rho: `{summary['b_myeloid_spearman_r']:.3f}` "
        f"(p `{summary['b_myeloid_spearman_p']:.4f}`).",
        f"- B/plasma IFN/STAT AUC: `{summary['b_plasma_ifn_stat_auc']:.3f}` "
        f"(exact p `{summary['b_plasma_ifn_stat_exact_p']:.4f}`).",
        f"- Myeloid IFN/STAT AUC: `{summary['myeloid_ifn_stat_auc']:.3f}` "
        f"(exact p `{summary['myeloid_ifn_stat_exact_p']:.4f}`).",
        f"- B/plasma residual after myeloid AUC: `{summary['b_residual_after_myeloid_auc']:.3f}` "
        f"(exact p `{summary['b_residual_after_myeloid_exact_p']:.4f}`).",
        "",
        "B/plasma leave-one-gene dependence:",
        "",
        "| Score | Genes | AUC | Exact p |",
        "|---|---|---:|---:|",
    ]
    for _, row in gene_df.iterrows():
        lines.append(
            f"| `{row['score']}` | `{row['genes']}` | {row['auc']:.3f} | {row['exact_p']:.4f} |"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- High B/plasma-myeloid correlation would support a broad shared IFN",
            "  remodeling interpretation.",
            "- Collapse after residualizing B/plasma against myeloid would argue against",
            "  B/plasma-independent signal.",
            "- A leave-one-gene collapse would indicate a single-gene signature rather",
            "  than a module.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
