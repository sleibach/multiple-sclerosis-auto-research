#!/usr/bin/env python3
"""Post-hoc recurrence check for the GSE85034 MTX receptor-side observation."""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_receptor_coupling_followup"


def auc_score(scores: np.ndarray, y: np.ndarray) -> float:
    if len(set(y.tolist())) < 2:
        return math.nan
    ranks = pd.Series(scores).rank(method="average").to_numpy()
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    rank_sum = float(ranks[y == 1].sum())
    return float((rank_sum - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def exact_auc_p(scores: np.ndarray, y: np.ndarray) -> float:
    n = len(y)
    n_pos = int(y.sum())
    observed = auc_score(scores, y)
    if not np.isfinite(observed) or n_pos == 0 or n_pos == n:
        return math.nan
    total = 0
    extreme = 0
    for pos_idx in itertools.combinations(range(n), n_pos):
        yy = np.zeros(n, dtype=int)
        yy[list(pos_idx)] = 1
        total += 1
        if auc_score(scores, yy) >= observed - 1e-12:
            extreme += 1
    return float(extreme / total)


def hedges_g(pos: np.ndarray, neg: np.ndarray) -> float:
    if len(pos) < 2 or len(neg) < 2:
        return math.nan
    pooled = math.sqrt(((len(pos) - 1) * np.var(pos, ddof=1) + (len(neg) - 1) * np.var(neg, ddof=1)) / (len(pos) + len(neg) - 2))
    if pooled == 0:
        return 0.0
    return float(((np.mean(pos) - np.mean(neg)) / pooled) * (1.0 - 3.0 / (4.0 * (len(pos) + len(neg)) - 9.0)))


def summarize(df: pd.DataFrame, cohort: str, source: str, feature: str) -> dict[str, object]:
    sub = df.dropna(subset=[feature, "response_binary"]).copy()
    y = sub["response_binary"].astype(int).to_numpy()
    scores = sub[feature].to_numpy(float)
    responders = scores[y == 1]
    nonresponders = scores[y == 0]
    return {
        "cohort": cohort,
        "source": source,
        "feature": feature,
        "n": int(len(sub)),
        "n_responders": int(y.sum()),
        "n_nonresponders": int(len(y) - y.sum()),
        "auc_high_score_response": auc_score(scores, y),
        "exact_auc_p": exact_auc_p(scores, y),
        "hedges_g_responder_minus_non": hedges_g(responders, nonresponders),
        "welch_p": float(stats.ttest_ind(responders, nonresponders, equal_var=False).pvalue)
        if len(responders) >= 2 and len(nonresponders) >= 2
        else math.nan,
    }


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    clean = df.copy()
    for col in clean.columns:
        clean[col] = clean[col].map(lambda x: f"{x:.4g}" if isinstance(x, float) and np.isfinite(x) else x)
    header = "| " + " | ".join(clean.columns.astype(str)) + " |"
    sep = "| " + " | ".join(["---"] * len(clean.columns)) + " |"
    rows = ["| " + " | ".join(str(x) for x in row) + " |" for row in clean.to_numpy()]
    return "\n".join([header, sep, *rows])


def load_data() -> dict[str, pd.DataFrame]:
    out: dict[str, pd.DataFrame] = {}

    cross = pd.read_csv(ROOT / "analysis/v22_locked_apc_hla_validation/paired_locked_scores_v22_cross_disease.tsv", sep="\t")
    cross["response_binary"] = cross["response"].eq("Responder").astype(int)
    cross["negative_delta_RECEPTOR"] = -pd.to_numeric(cross["delta_RECEPTOR"], errors="coerce")
    out["GSE85034_ADA"] = cross[cross["cohort"].eq("GSE85034_ADA")].copy()
    out["GSE253006_TOF_all_cell_approx"] = cross[cross["cohort"].eq("GSE253006_TOF")].copy()

    mtx = pd.read_csv(ROOT / "analysis/v36_gse85034_mtx_stress/gse85034_mtx_paired_scores.tsv", sep="\t")
    mtx["response_binary"] = mtx["pasi75_wk16"].astype(int)
    out["GSE85034_MTX"] = mtx

    comp = pd.read_csv(ROOT / "analysis/v23_apc_hla_monitoring/gse253006_exact_compartments/gse253006_exact_compartment_paired_scores.tsv", sep="\t")
    comp["response_binary"] = comp["response"].eq("Responder").astype(int)
    comp["negative_delta_RECEPTOR"] = -pd.to_numeric(comp["delta_RECEPTOR"], errors="coerce")
    for compartment, group in comp.groupby("marker_compartment"):
        out[f"GSE253006_TOF_exact_{compartment}"] = group.copy()
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for cohort, df in load_data().items():
        source = "hypothesis_source" if cohort == "GSE85034_MTX" else "recurrence_check"
        for feature in ["negative_delta_RECEPTOR", "delta_RECEPTOR", "locked_signed_score"]:
            if feature in df.columns:
                rows.append(summarize(df, cohort, source, feature))
    result = pd.DataFrame(rows).sort_values(["feature", "source", "cohort"])
    result.to_csv(OUT / "receptor_recurrence_tests.tsv", sep="\t", index=False)

    summary = {
        "question": "Does the post-hoc GSE85034_MTX receptor-side observation recur in ADA or TOF artifacts?",
        "status": "exploratory_post_hoc_only",
        "n_tests": int(len(result)),
        "mtx_negative_delta_receptor_auc": float(result[(result["cohort"].eq("GSE85034_MTX")) & (result["feature"].eq("negative_delta_RECEPTOR"))]["auc_high_score_response"].iloc[0]),
        "strongest_recurrence": result[result["source"].eq("recurrence_check")]
        .sort_values(["auc_high_score_response", "exact_auc_p"], ascending=[False, True])
        .head(5)
        .to_dict("records"),
        "interpretation": "Receptor dynamics are direction- and context-dependent; no receptor successor rule is warranted without a pre-specified fresh test.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = [
        "# V36 Receptor/Coupling Follow-Up",
        "",
        "The MTX stress test produced a high post-hoc `negative_delta_RECEPTOR`",
        "metric. This script checks recurrence in already-held ADA and TOF paired",
        "score artifacts. It is explicitly exploratory and cannot alter the locked",
        "V22 rule.",
        "",
        markdown_table(result),
        "",
        "## Interpretation",
        "",
        "The receptor-side observation is not a stable, same-orientation successor",
        "rule across artifacts. Some exact TOF compartments show high positive",
        "`delta_RECEPTOR` AUCs, while MTX showed high `negative_delta_RECEPTOR`.",
        "That direction/context instability blocks any upgrade. If receptor/coupling",
        "biology is revisited, it should be a separately locked hypothesis tested in",
        "fresh data, not a post-hoc substitute for the V22 IFN/APC rule.",
    ]
    (OUT / "summary.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
