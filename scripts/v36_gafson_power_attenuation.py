#!/usr/bin/env python3
"""Effect-attenuation sensitivity for DMF validation power."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_gafson_power_attenuation"
SEED = 20260607


def auc_score(scores: np.ndarray, y: np.ndarray) -> float:
    ranks = pd.Series(scores).rank(method="average").to_numpy()
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    return float((float(ranks[y == 1].sum()) - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def normal_auc_p(scores: np.ndarray, y: np.ndarray) -> float:
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    u = auc_score(scores, y) * n1 * n0
    mean = n1 * n0 / 2.0
    sd = math.sqrt(n1 * n0 * (n1 + n0 + 1) / 12.0)
    return float(1.0 - stats.norm.cdf((u - mean) / sd))


def simulate(responder: np.ndarray, nonresponder: np.ndarray, attenuation: float, n_per_group: int, n_sim: int = 15000) -> dict[str, object]:
    rng = np.random.default_rng(SEED + int(attenuation * 1000) + n_per_group)
    nr_mean = float(np.mean(nonresponder))
    attenuated_responder = nr_mean + attenuation * (responder - nr_mean)
    y = np.array([1] * n_per_group + [0] * n_per_group, dtype=int)
    aucs = []
    pvals = []
    for _ in range(n_sim):
        r = rng.choice(attenuated_responder, size=n_per_group, replace=True)
        nr = rng.choice(nonresponder, size=n_per_group, replace=True)
        scores = np.concatenate([r, nr])
        aucs.append(auc_score(scores, y))
        pvals.append(normal_auc_p(scores, y))
    aucs = np.asarray(aucs)
    pvals = np.asarray(pvals)
    return {
        "attenuation_fraction": attenuation,
        "n_per_group": n_per_group,
        "total_n": n_per_group * 2,
        "median_auc": float(np.nanmedian(aucs)),
        "power_one_sided_p_lt_0_05": float(np.nanmean(pvals < 0.05)),
        "power_auc_ge_0_70": float(np.nanmean(aucs >= 0.70)),
    }


def markdown_table(df: pd.DataFrame) -> str:
    clean = df.copy()
    for col in clean.columns:
        clean[col] = clean[col].map(lambda x: f"{x:.4g}" if isinstance(x, float) and np.isfinite(x) else x)
    header = "| " + " | ".join(clean.columns.astype(str)) + " |"
    sep = "| " + " | ".join(["---"] * len(clean.columns)) + " |"
    rows = ["| " + " | ".join(str(x) for x in row) + " |" for row in clean.to_numpy()]
    return "\n".join([header, sep, *rows])


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(ROOT / "analysis/v22_locked_apc_hla_validation/paired_locked_scores_v22.tsv", sep="\t")
    dmf = df[df["cohort"].eq("GSE235357")]
    responder = dmf.loc[dmf["response"].eq("Responder"), "locked_signed_score"].to_numpy(float)
    nonresponder = dmf.loc[dmf["response"].eq("Non-responder"), "locked_signed_score"].to_numpy(float)
    rows = [
        simulate(responder, nonresponder, attenuation, n)
        for attenuation in [1.0, 0.75, 0.5, 0.25]
        for n in [20, 30, 40, 50, 75, 100]
    ]
    result = pd.DataFrame(rows)
    result.to_csv(OUT / "dmf_power_attenuation.tsv", sep="\t", index=False)
    summary = {
        "question": "How sensitive is DMF validation power to weaker-than-observed effect sizes?",
        "attenuation_definition": "Responder scores are moved toward the nonresponder mean by the attenuation fraction; 1.0 is observed effect, 0.5 is half separation.",
        "power_table": result.to_dict("records"),
        "interpretation": "If the true effect is half the observed GSE235357 separation, even 100 per group remains underpowered by this simple bootstrap model.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = [
        "# V36 DMF Power Attenuation Sensitivity",
        "",
        "Responder scores are moved toward the nonresponder mean before bootstrap",
        "sampling. This shows how strongly validation size depends on the small",
        "`GSE235357` effect estimate being representative.",
        "",
        markdown_table(result),
        "",
        "## Interpretation",
        "",
        "The planning conclusion is conservative: if the Gafson/fresh-cohort effect",
        "is materially weaker than the observed n=5/5 template, sample size needs",
        "rise quickly and may exceed ordinary public-cohort sizes. This reinforces",
        "that a small fresh cohort should be treated as directional evidence unless",
        "the effect is large and covariates are well measured.",
    ]
    (OUT / "summary.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
