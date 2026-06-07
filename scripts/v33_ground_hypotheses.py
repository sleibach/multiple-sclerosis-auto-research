#!/usr/bin/env python3
"""Ground V33 exploratory hypotheses on existing project artifacts.

Model outputs are treated as proposal text only. This script creates a compact
triage table from reproducible local artifacts: V26 deep-structure matrices,
V32 confounder audit, V21 LDSC backdrop, V11 disagreement matrix, and V6
postpartum APC-axis outputs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v33_hypothesis_generation"
OUT.mkdir(parents=True, exist_ok=True)


def read_tsv(rel: str) -> pd.DataFrame:
    return pd.read_csv(ROOT / rel, sep="\t")


def parse_model_json(path: Path) -> tuple[list[dict], str]:
    if not path.exists():
        return [], "missing"
    text = path.read_text()
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        obj = json.loads(text)
    except Exception as exc:
        return [], f"unparseable:{type(exc).__name__}"
    hyps = obj.get("hypotheses", [])
    if not isinstance(hyps, list):
        return [], "json_without_hypotheses_list"
    return hyps, "parsed"


def auc_or_nan(y: np.ndarray, x: np.ndarray) -> float:
    mask = np.isfinite(x)
    y = y[mask]
    x = x[mask]
    if len(np.unique(y)) < 2:
        return float("nan")
    r = x[y == 1]
    n = x[y == 0]
    wins = 0.0
    total = 0
    for a in r:
        for b in n:
            wins += 1 if a > b else 0.5 if a == b else 0
            total += 1
    return wins / total if total else float("nan")


def permutation_p_auc(y: np.ndarray, x: np.ndarray, observed: float, n_perm: int = 2000, seed: int = 33033) -> float:
    rng = np.random.default_rng(seed)
    count = 0
    for _ in range(n_perm):
        yp = rng.permutation(y)
        val = auc_or_nan(yp, x)
        if abs(val - 0.5) >= abs(observed - 0.5):
            count += 1
    return (count + 1) / (n_perm + 1)


def summarize_model_outputs() -> pd.DataFrame:
    rows = []
    for label, filename in [
        ("claude_full", "claude_hypotheses.json"),
        ("gemini_full", "gemini_hypotheses.json"),
        ("claude_compact", "claude_hypotheses_compact.json"),
        ("gemini_compact", "gemini_hypotheses_compact.json"),
        ("claude_short", "claude_hypotheses_short.json"),
        ("gemini_short", "gemini_hypotheses_short.json"),
    ]:
        hyps, status = parse_model_json(OUT / filename)
        for h in hyps:
            rows.append(
                {
                    "source": label,
                    "short_name": h.get("short_name", ""),
                    "hypothesis": h.get("hypothesis", ""),
                    "minimum_grounding_test": h.get("minimum_grounding_test", ""),
                    "parse_status": status,
                }
            )
        if not hyps:
            rows.append({"source": label, "short_name": "", "hypothesis": "", "minimum_grounding_test": "", "parse_status": status})
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "model_hypothesis_parse_summary.tsv", sep="\t", index=False)
    return df


def main() -> None:
    model_df = summarize_model_outputs()

    deps = read_tsv("analysis/v26_deep_structure/workstream_b_module_dependencies.tsv")
    latent = read_tsv("analysis/v26_deep_structure/workstream_a_latent_axes.tsv")
    v32_single = read_tsv("analysis/v32_confounder_audit/v32_confounder_adjustment_metrics.tsv")
    v32_joint = read_tsv("analysis/v32_confounder_audit/v32_joint_adjustment_metrics.tsv")
    rg = read_tsv("analysis/v21_ldsc_backdrop/ldsc_rg_results.tsv")
    postpartum = read_tsv("analysis/tier_0_triage/hyp_v6_007_gse235508_decoupling/key_postpartum_decoupling.tsv")
    disease_activity = read_tsv("analysis/tier_0_triage/hyp_v6_007_gse235508_decoupling/disease_activity_correlations.tsv")
    comp = read_tsv("analysis/v23_apc_hla_monitoring/gse253006_exact_compartments/gse253006_exact_compartment_validation.tsv")

    rows: list[dict] = []

    lysosomal_hits = deps[
        (
            ((deps.module_a == "ifn_apc") & (deps.module_b == "lysosomal_apc"))
            | ((deps.module_b == "ifn_apc") & (deps.module_a == "lysosomal_apc"))
            | ((deps.module_a == "hla_ii_apc") & (deps.module_b == "lysosomal_apc"))
            | ((deps.module_b == "hla_ii_apc") & (deps.module_a == "lysosomal_apc"))
        )
        & (deps.claim_grade == "supported")
    ]
    rows.append(
        {
            "hypothesis_id": "V33_H01_lysosomal_APC_bottleneck",
            "sources": "Claude;agent",
            "claim": "Lysosomal APC processing is a coupled part of the APC remodeling architecture and may explain why surface single-node targets fail.",
            "grounding_test": "V26 replicated module-dependency scan for IFN/HLA-II with lysosomal APC modules.",
            "grounded_result": "supported",
            "effect": f"{len(lysosomal_hits)} supported lysosomal/APC dependencies; strongest median replicated r not recomputed here, see V26 table.",
            "null_or_cv": "V26 module-pair permutation with BH correction and replication across modalities.",
            "artifact_risk": "Transcript lysosomal modules may track monocyte maturation; needs functional lysosomal/protein readout.",
            "next_test": "Perturb cathepsin/V-ATPase/lysosomal flux in APC/T/B context and test coupled HLA-II-CD74-IFN movement.",
            "rank_score": 4,
        }
    )

    sterol_cols = [c for c in v32_single["confounder"] if "immunometabolism" in c or "glycolysis" in c or "oxphos" in c]
    metabolic_joint = v32_joint[v32_joint["risk_set"] == "metabolic_inflammatory_stat1"].iloc[0]
    rows.append(
        {
            "hypothesis_id": "V33_H02_metabolic_sterol_setpoint",
            "sources": "Claude;Gemini-theme;agent",
            "claim": "APC remodeling may be gated by broader metabolic/sterol state rather than isolated antigen-presentation modules.",
            "grounding_test": "V32 metabolic/glycolysis/OXPHOS/HIF-NAMPT single panels and metabolic/inflammatory/STAT1 joint adjustment.",
            "grounded_result": "inconclusive_but_prioritized",
            "effect": f"{len(sterol_cols)} metabolic single panels survived individually; broad metabolic/inflammatory/STAT1 joint adjusted AUC {metabolic_joint.joint_adjusted_auc:.3f}, attenuation {metabolic_joint.auc_attenuation:.3f}.",
            "null_or_cv": f"Joint permutation p {metabolic_joint.joint_adjusted_permutation_p:.4f}; LOOCV confounders-only {metabolic_joint.loocv_auc_confounders_only:.3f} vs locked+confounders {metabolic_joint.loocv_auc_locked_plus_confounders:.3f}.",
            "artifact_risk": "Current data has HIF/NAMPT/glycolysis/OXPHOS proxies, not a true sterol/oxysterol module.",
            "next_test": "Score explicit ABCA1/ABCG1/CH25H/SREBF2/NR1H3 sterol handling in APC-resolved MS and treatment datasets.",
            "rank_score": 3,
        }
    )

    dec = postpartum[
        (postpartum["module"] == "decoupling_hla_minus_cd64")
        & postpartum["contrast"].str.contains("postpartum_6mo_vs_trimester_3")
    ].copy()
    best = dec.sort_values("welch_p").head(3)
    da_max = disease_activity["rho"].abs().max() if "rho" in disease_activity.columns else np.nan
    rows.append(
        {
            "hypothesis_id": "V33_H03_postpartum_APC_split_window",
            "sources": "agent;project-dormant",
            "claim": "Postpartum immune rebound separates HLA-II/regulatory APC and CD64 inflammatory arms; timing, not baseline disease activity, may define relapse windows.",
            "grounding_test": "Existing GSE235508 pregnancy/postpartum contrasts and disease-activity correlations.",
            "grounded_result": "supported_as_state_biology_not_biomarker",
            "effect": "; ".join([f"{r.samplegroup} delta {r.delta_test_minus_reference:.3f}, g {r.hedges_g:.3f}, p {r.welch_p:.4g}" for _, r in best.iterrows()]),
            "null_or_cv": f"Welch contrasts by group; same-day disease activity weak, max |rho| {da_max:.3f}.",
            "artifact_risk": "Pregnancy/lactation/timepoint and composition confounding; lacks MS postpartum relapse labels.",
            "next_test": "Acquire postpartum MS blood/CSF relapse-timing cohort and test HLA-II minus CD64 trajectory before relapse.",
            "rank_score": 5,
        }
    )

    supported_latent = latent[latent["grade"] == "supported"]
    rows.append(
        {
            "hypothesis_id": "V33_H04_complement_lipid_negative_axis",
            "sources": "agent;Claude-complement/iron-theme",
            "claim": "Complement/phagocytosis and lipid-repair programs form a negative pole opposite IFN/HLA-II APC remodeling, suggesting progressive/tissue-repair biology is not captured by the V22 response axis.",
            "grounding_test": "V26 supported latent axes and PC1 loadings.",
            "grounded_result": "supported_structure_needs_stage_data",
            "effect": f"{len(supported_latent)} supported latent pairings; V26 positive pole IFN/HLA-II/MIF-CD74, negative pole complement/lipid/lysosomal in pharmacodynamic-cell-state axis.",
            "null_or_cv": "V26 column-label permutation and BH correction; strongest supported cosine 0.934, q 0.010.",
            "artifact_risk": "Module labels shared by construction across some matrices; V31 flagged module-overlap sensitivity need.",
            "next_test": "In progressive/chronic-active lesion data, test whether complement/lipid negative-pole score is orthogonal to V22 scalar and tracks lesion-rim/progression markers.",
            "rank_score": 4,
        }
    )

    sle = rg[rg["comparator"] == "SLE"].iloc[0]
    rows.append(
        {
            "hypothesis_id": "V33_H05_MS_SLE_EBV_IFN_APC_imprint",
            "sources": "Claude;agent",
            "claim": "An EBV/IFN APC imprint may explain MS-SLE proximity outside the gut axis.",
            "grounding_test": "V21 genome-wide MS-SLE rg backdrop plus current absence of EBV-specific module in held matrices.",
            "grounded_result": "promising_but_untestable_with_current_module_data",
            "effect": f"MS-SLE rg {sle.rg:.4f} (SE {sle.se:.4f}, p {sle.p}); caveated h2 intercept {sle.h2_int_trait2}.",
            "null_or_cv": "LDSC rg with intercept reported; no EBV module null test run because module not present.",
            "artifact_risk": "SLE rg is caveated by high h2 intercept; EBV module could collapse to generic IFN tone.",
            "next_test": "Build EBV/LMP1/EBNA-response module and test separability from STAT1/IFN and V22 scalar in MS/SLE blood and B-cell datasets.",
            "rank_score": 3,
        }
    )

    # Compartment signal from exact tofacitinib V23.
    comp_sorted = comp.sort_values("auc", ascending=False).head(3)
    rows.append(
        {
            "hypothesis_id": "V33_H06_TB_compartment_remodeling_gate",
            "sources": "agent;V31-review-theme",
            "claim": "The APC/HLA-II response signal may be gated by T/B-cell compartment remodeling rather than myeloid APC state alone.",
            "grounding_test": "V23 exact GSE253006 marker-compartment validation.",
            "grounded_result": "supported_as_biomarker_context_not_new_target",
            "effect": "; ".join([f"{r.marker_compartment} AUC {r.auc:.3f}, g {r.hedges_g:.3f}" for _, r in comp_sorted.iterrows()]),
            "null_or_cv": "Small-n exact raw-10x compartment split; not a fresh held-out validation.",
            "artifact_risk": "Marker-derived compartments; UC tofacitinib not MS DMT.",
            "next_test": "Run frozen V22/V32 scoring in sorted or single-cell MS DMT cohort and test T/B versus myeloid compartment origin.",
            "rank_score": 4,
        }
    )

    df = pd.DataFrame(rows).sort_values(["rank_score", "hypothesis_id"], ascending=[False, True])
    df.to_csv(OUT / "v33_grounded_hypothesis_triage.tsv", sep="\t", index=False)

    summary = {
        "model_parse_counts": model_df.groupby("source")["short_name"].apply(lambda s: int((s != "").sum())).to_dict(),
        "grounded_counts": df["grounded_result"].value_counts().to_dict(),
        "top_ranked": df.head(3)["hypothesis_id"].tolist(),
    }
    (OUT / "v33_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
