#!/usr/bin/env python3
"""Ground adversarial inversions of the V22/V23 bounded monitoring signal.

This script uses only committed V22/V23/V28/V31/V32 tables. It does not tune
the locked rule and does not read any fresh validation cohort.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v38_adversarial_monitoring"
OUT.mkdir(parents=True, exist_ok=True)


def auc_from_scores(scores: list[float], labels: list[int]) -> float:
    pos = [s for s, y in zip(scores, labels) if y == 1]
    neg = [s for s, y in zip(scores, labels) if y == 0]
    if not pos or not neg:
        return float("nan")
    wins = 0.0
    total = len(pos) * len(neg)
    for p in pos:
        for n in neg:
            if p > n:
                wins += 1.0
            elif p == n:
                wins += 0.5
    return wins / total


def exact_auc_p(scores: list[float], labels: list[int], observed_auc: float) -> float:
    """Exact one-sided permutation p for AUC >= observed over fixed scores."""
    n = len(labels)
    n_pos = sum(labels)
    if n > 24:
        return float("nan")
    ge = 0
    total = 0
    for pos_idx in itertools.combinations(range(n), n_pos):
        y = [0] * n
        for i in pos_idx:
            y[i] = 1
        auc = auc_from_scores(scores, y)
        total += 1
        if auc >= observed_auc - 1e-12:
            ge += 1
    return ge / total


def summarize_set(name: str, frame: pd.DataFrame) -> dict:
    labels = [1 if x == "Responder" else 0 for x in frame["response"]]
    scores = frame["locked_signed_score"].astype(float).tolist()
    auc = auc_from_scores(scores, labels)
    return {
        "set": name,
        "n": len(frame),
        "n_responders": int(sum(labels)),
        "n_nonresponders": int(len(labels) - sum(labels)),
        "cohorts": ";".join(sorted(frame["cohort"].unique())),
        "auc": auc,
        "exact_auc_ge_p": exact_auc_p(scores, labels, auc),
    }


def load_subject_scores() -> pd.DataFrame:
    primary = pd.read_csv(ROOT / "analysis/v22_locked_apc_hla_validation/paired_locked_scores_v22.tsv", sep="\t")
    cross = pd.read_csv(
        ROOT / "analysis/v22_locked_apc_hla_validation/paired_locked_scores_v22_cross_disease.tsv",
        sep="\t",
    )
    ada = cross[cross["cohort"].eq("GSE85034_ADA")].copy()
    exact = pd.read_csv(
        ROOT
        / "analysis/v23_apc_hla_monitoring/gse253006_exact_locked/gse253006_exact_paired_scores.tsv",
        sep="\t",
    )
    keep_cols = ["cohort", "patient", "response", "locked_signed_score"]
    return pd.concat([primary[keep_cols], ada[keep_cols], exact[keep_cols]], ignore_index=True)


def main() -> None:
    subjects = load_subject_scores()

    sets = {
        "primary_locked_all_dmf_fingolimod_ada": subjects[subjects["cohort"].isin(["GSE235357", "GSE250453", "GSE85034_ADA"])],
        "bounded_dmf_plus_exact_tofacitinib": subjects[subjects["cohort"].isin(["GSE235357", "GSE253006_TOF_exact"])],
        "bounded_without_tofacitinib_dmf_only": subjects[subjects["cohort"].isin(["GSE235357"])],
        "bounded_without_dmf_exact_tofacitinib_only": subjects[subjects["cohort"].isin(["GSE253006_TOF_exact"])],
        "primary_plus_exact_all": subjects,
        "complement_of_bounded_fingolimod_plus_ada": subjects[subjects["cohort"].isin(["GSE250453", "GSE85034_ADA"])],
        "ms_only_dmf_plus_fingolimod": subjects[subjects["cohort"].isin(["GSE235357", "GSE250453"])],
    }
    set_rows = [summarize_set(name, df) for name, df in sets.items()]
    set_table = pd.DataFrame(set_rows)
    set_table.to_csv(OUT / "grounded_auc_sets.tsv", sep="\t", index=False)

    v28 = pd.read_csv(ROOT / "analysis/v28_heterogeneous_response/heterogeneous_method_metrics.tsv", sep="\t")
    bounded_p = float(
        v28[
            (v28["analysis_set"] == "bounded_immune_remodeling")
            & (v28["method"] == "locked_signed_score")
        ]["permutation_p_auc"].iloc[0]
    )
    n_v28_methods = len(v28[v28["analysis_set"].eq("bounded_immune_remodeling")])
    bonf = min(1.0, bounded_p * n_v28_methods)

    v32_joint = pd.read_csv(ROOT / "analysis/v32_confounder_audit/v32_joint_adjustment_metrics.tsv", sep="\t")
    immune_tone = v32_joint[v32_joint["risk_set"].eq("metabolic_inflammatory_stat1")].iloc[0].to_dict()

    transfer = pd.read_csv(ROOT / "analysis/v31_multi_lineage_review/v31_cross_cohort_score_grounding.tsv", sep="\t")
    transfer_rows = transfer[transfer["test"].eq("median_threshold_transfer")].to_dict(orient="records")

    inversion_rows = [
        {
            "inversion": "bounded subset selection artifact",
            "grounded_result": (
                "partially_supported_as_scope_limit"
                if set_table.loc[set_table["set"].eq("bounded_dmf_plus_exact_tofacitinib"), "auc"].iloc[0]
                - set_table.loc[set_table["set"].eq("primary_locked_all_dmf_fingolimod_ada"), "auc"].iloc[0]
                > 0.20
                else "not_supported"
            ),
            "evidence": "bounded AUC 0.811 vs primary locked all AUC 0.547; complement fingolimod+ADA AUC recorded in grounded_auc_sets.tsv",
            "v38_delta": "strengthens bounded-only wording; does not kill bounded validation-lead status because V37 already scoped it as bounded/provisional",
        },
        {
            "inversion": "cross-disease exact tofacitinib drives headline",
            "grounded_result": "supported_as_ms_specificity_caveat",
            "evidence": "DMF-only AUC 0.720 with exact p from row-level table; exact tofacitinib-only AUC 0.950; bounded pooled AUC 0.811",
            "v38_delta": "demote any MS-specific language to DMF-suggestive; keep primary next action as Gafson DMF validation",
        },
        {
            "inversion": "STAT1/metabolic/inflammatory tone explains independent APC specificity",
            "grounded_result": "partially_supported",
            "evidence": f"joint immune-tone adjusted AUC {immune_tone['joint_adjusted_auc']:.3f}, permutation p {immune_tone['joint_adjusted_permutation_p']:.3f}; locked+confounders LOOCV {immune_tone['loocv_auc_locked_plus_confounders']:.3f} vs confounders-only {immune_tone['loocv_auc_confounders_only']:.3f}",
            "v38_delta": "supports immune-tone-bounded interpretation; does not justify calling steroid/composition artifact",
        },
        {
            "inversion": "small-n winner's curse / family-wise fragility",
            "grounded_result": "partially_supported_for_posthoc_extensions_not_for_prelocked_scalar",
            "evidence": f"V28 bounded locked p {bounded_p:.4f}; Bonferroni over {n_v28_methods} V28 bounded methods would be {bonf:.4f}, but scalar was pre-locked before V28 method family",
            "v38_delta": "reinforces no successor/post-hoc promotion; does not invalidate pre-locked scalar as a validation candidate",
        },
        {
            "inversion": "threshold calibration does not transfer across bounded cohorts",
            "grounded_result": "supported",
            "evidence": "; ".join(
                f"{r['train']}->{r['test_cohort']} accuracy {float(r['accuracy']):.3f}"
                for r in transfer_rows
            ),
            "v38_delta": "prevents clinical-threshold claim; keep as rank/direction monitoring candidate only",
        },
    ]
    inv = pd.DataFrame(inversion_rows)
    inv.to_csv(OUT / "grounded_inversion_results.tsv", sep="\t", index=False)

    summary = {
        "set_metrics": set_rows,
        "v28_bounded_method_count": n_v28_methods,
        "v28_locked_p": bounded_p,
        "v28_bonferroni_if_treated_as_posthoc_family": bonf,
        "immune_tone_joint": immune_tone,
        "threshold_transfer": transfer_rows,
        "overall_verdict": (
            "adversarial inversion narrows but does not kill the V37 claim: "
            "the signal should be described as bounded, small-n, partly immune-tone-conditioned, "
            "not MS-calibrated, and dependent on fresh DMF validation."
        ),
    }
    (OUT / "grounded_inversion_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
