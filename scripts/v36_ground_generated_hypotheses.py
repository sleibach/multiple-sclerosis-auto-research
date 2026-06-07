#!/usr/bin/env python3
"""Ground executable V36 generated hypotheses against held project data."""

from __future__ import annotations

import json
import math
import pathlib
import re
from statistics import mean

import pandas as pd
from scipy import stats
from sklearn.metrics import roc_auc_score


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_tri_source_generation"


def read_model_json(path: pathlib.Path) -> dict:
    text = path.read_text()
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.S)
    if match:
        text = match.group(1)
    return json.loads(text)


def safe_auc(labels: list[int], values: list[float]) -> float:
    auc = roc_auc_score(labels, values)
    return max(auc, 1.0 - auc)


def exact_perm_auc(labels: list[int], values: list[float]) -> float:
    # Enumerate all assignments with same number of responders for n <= 20.
    import itertools

    n = len(labels)
    k = sum(labels)
    observed = safe_auc(labels, values)
    ge = 0
    total = 0
    for positive in itertools.combinations(range(n), k):
        perm = [0] * n
        for idx in positive:
            perm[idx] = 1
        if safe_auc(perm, values) >= observed - 1e-12:
            ge += 1
        total += 1
    return ge / total


def ground_tofa_glycolytic_brake() -> dict:
    scores = pd.read_csv(ROOT / "analysis/v32_confounder_audit/v32_subject_confounder_scores.tsv", sep="\t")
    tof = scores[scores["cohort"] == "GSE253006_TOF_exact"].copy()
    tof["label"] = (tof["response"] == "Responder").astype(int)
    rows = []
    for feature in [
        "delta_glycolysis",
        "delta_oxphos",
        "delta_immunometabolism_hif_nampt",
        "delta_t_cell_composition",
        "locked_signed_score",
    ]:
        vals = tof[feature].astype(float).tolist()
        labels = tof["label"].tolist()
        r_vals = tof[tof["label"] == 1][feature].astype(float)
        nr_vals = tof[tof["label"] == 0][feature].astype(float)
        rows.append(
            {
                "feature": feature,
                "n": len(tof),
                "auc_oriented": safe_auc(labels, vals),
                "exact_perm_p_auc_ge_observed": exact_perm_auc(labels, vals),
                "mean_responder": float(r_vals.mean()),
                "mean_nonresponder": float(nr_vals.mean()),
                "welch_p": float(stats.ttest_ind(r_vals, nr_vals, equal_var=False).pvalue),
            }
        )
    pd.DataFrame(rows).to_csv(OUT / "tofacitinib_metabolic_feature_tests.tsv", sep="\t", index=False)
    gly = next(row for row in rows if row["feature"] == "delta_glycolysis")
    locked = next(row for row in rows if row["feature"] == "locked_signed_score")
    return {
        "hypothesis_ids": ["tofa_treg_glycolytic_brake"],
        "source_models": ["claude"],
        "grounded_result": "inconclusive_partial_context_only",
        "test": "GSE253006 exact all-cell V32 metabolic confounder scores; Treg-specific glycolysis is not available in held exact compartment matrix.",
        "key_numbers": {
            "delta_glycolysis_auc_oriented": gly["auc_oriented"],
            "delta_glycolysis_exact_perm_p": gly["exact_perm_p_auc_ge_observed"],
            "locked_signed_score_auc_oriented": locked["auc_oriented"],
            "locked_signed_score_exact_perm_p": locked["exact_perm_p_auc_ge_observed"],
        },
        "interpretation": (
            "All-cell glycolysis delta can be scored, but it is not a Treg- or T-cell-specific brake test. "
            "The exact compartment matrix only carries the locked module genes, not glycolysis genes. "
            "The hypothesis remains a plausible mechanism proposal, not a grounded finding."
        ),
        "next_test": "Treg/effector-T sorted or single-cell paired treatment data with glycolysis genes and response labels.",
    }


def ground_lysosomal_sterol_coupling() -> dict:
    sterol = pd.read_csv(ROOT / "analysis/v35_metabolic_sterol_setpoint/sterol_gene_lesion_edge_tests.tsv", sep="\t")
    lys = pd.read_csv(ROOT / "analysis/v35_lysosomal_apc_bottleneck/lysosomal_module_correlations.tsv", sep="\t")
    lys_chol = sterol[sterol["module"] == "lysosomal_cholesterol"].iloc[0].to_dict()
    chol_syn = sterol[sterol["module"] == "cholesterol_synthesis"].iloc[0].to_dict()
    top_lys = lys.sort_values("spearman_r", key=lambda s: s.abs(), ascending=False).iloc[0].to_dict()
    return {
        "hypothesis_ids": ["sterol_setpoint_lysosomal_coupling", "pvm_lysosomal_blockade"],
        "source_models": ["claude", "gemini", "rpt"],
        "grounded_result": "not_supported_as_coupled_bottleneck_with_current_data",
        "test": "Compare MS lesion-edge sterol/lysosomal cholesterol modules with V35 Mixscale lysosomal APC perturbation coupling.",
        "key_numbers": {
            "lesion_edge_lysosomal_cholesterol_hedges_g": float(lys_chol["hedges_g_active_minus_control"]),
            "lesion_edge_lysosomal_cholesterol_p": float(lys_chol["welch_p"]),
            "lesion_edge_cholesterol_synthesis_hedges_g": float(chol_syn["hedges_g_active_minus_control"]),
            "lesion_edge_cholesterol_synthesis_p": float(chol_syn["welch_p"]),
            "mixscale_top_lysosomal_pair": top_lys["comparison"],
            "mixscale_top_spearman_r": float(top_lys["spearman_r"]),
            "mixscale_top_perm_p": float(top_lys["spearman_perm_p_two_sided"]),
        },
        "interpretation": (
            "The perturbation data strongly couples GILT/lysosomal APC to IFN/APC, and lesion-edge immune cells show "
            "cholesterol-synthesis context, but the lesion-edge lysosomal-cholesterol module itself is weak and non-significant. "
            "Current data do not support a unified sterol-lysosomal bottleneck."
        ),
        "next_test": "APC- or perivascular-macrophage-resolved lipid/lysosomal flux or HLA-peptidomics in MS lesions.",
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    proposals = []
    for model in ["claude", "gemini"]:
        data = read_model_json(OUT / f"{model}_hypotheses.json")
        for hyp in data["hypotheses"]:
            hyp = dict(hyp)
            hyp["model"] = model
            proposals.append(hyp)
    pd.DataFrame(proposals).to_csv(OUT / "consolidated_model_hypotheses.tsv", sep="\t", index=False)
    groundings = [ground_tofa_glycolytic_brake(), ground_lysosomal_sterol_coupling()]
    (OUT / "grounded_generated_hypotheses.json").write_text(json.dumps(groundings, indent=2, sort_keys=True))
    lines = [
        "# V36 Generated Hypothesis Grounding",
        "",
        f"Model proposals consolidated: `{len(proposals)}` (`8` Claude, `8` Gemini).",
        "",
        "Grounded executable subset:",
        "",
    ]
    for item in groundings:
        lines.extend(
            [
                f"## {', '.join(item['hypothesis_ids'])}",
                "",
                f"- Source models: {', '.join(item['source_models'])}.",
                f"- Grounded result: **{item['grounded_result']}**.",
                f"- Test: {item['test']}",
                f"- Key numbers: `{json.dumps(item['key_numbers'], sort_keys=True)}`",
                f"- Interpretation: {item['interpretation']}",
                f"- Next test: {item['next_test']}",
                "",
            ]
        )
    lines.extend(
        [
            "Non-grounded proposals remain proposals only. They are queued only if a",
            "concrete held-data test can be specified without reading quarantined data.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
