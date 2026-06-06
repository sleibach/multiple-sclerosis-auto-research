#!/usr/bin/env python3
"""Wave31 dynamic transition-controller audit.

Wave30 closed static upstream ligand/receptor scoring as a therapeutic rescue.
This wave asks a stricter dynamic question:

Which perturbations selectively decouple the HLA-II/CD74 antigen-presentation
transition from generic IFN/JAK host-defense genes, and do any of those
perturbations map to a tractable, cross-autoimmune intervention point?

The script integrates existing V3 outputs only. It does not claim that L1000 or
Mixscale cell-line signatures are autoimmune APC perturbations; those sources
are explicitly downgraded unless supported by primary immune-cell data.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave31_dynamic_transition_controller_audit"
SEED = 20260527

PATHS = {
    "direct_ranked": ROOT / "phases/v3/results" / "wave15_perturbation_drug_response" / "ranked_direct_perturbations.tsv",
    "candidate_synthesis": ROOT / "phases/v3/results" / "wave15_perturbation_drug_response" / "candidate_level_synthesis.tsv",
    "l1000_selective": ROOT
    / "phases/v3/results"
    / "wave15_perturbation_drug_response"
    / "l1000fwd_selectivity_compound_rank.tsv",
    "l1000_recurrent": ROOT
    / "phases/v3/results"
    / "wave24_l1000_recurrent_reversal"
    / "recurrent_l1000_compound_triage.tsv",
    "mediator_verdict": ROOT / "phases/v3/results" / "wave17_mediator_kinase_route" / "route_verdict.json",
    "mediator_local": ROOT / "phases/v3/results" / "wave17_mediator_kinase_route" / "local_perturbation_evidence.tsv",
    "wave25_genetics": ROOT / "phases/v3/results" / "wave25_causal_genetics_module_proxy" / "causal_proxy_candidate_matrix.tsv",
    "wave28_target_first": ROOT / "phases/v3/results" / "wave28_target_first_rescue" / "target_first_rescue_matrix.tsv",
    "wave14_local": ROOT / "phases/v3/results" / "wave14_gsk3b_local_gate" / "gsk3b_local_gate_gene_summary.tsv",
}


MANUAL_CANDIDATES: dict[str, dict[str, Any]] = {
    "MED16": {
        "intervention_handle": "none direct; translational hypothesis is Mediator kinase/CDK8-CDK19 modulation",
        "druggability": 0.0,
        "manual_prior_risk": "medium",
        "manual_blocker": "Strong primary macrophage perturbation clue, but MED16 itself is not a drug target and CDK8/CDK19 loss does not phenocopy it in the local MHC-II CRISPR screen.",
    },
    "CDK8_CDK19_MEDIATOR_KINASE": {
        "intervention_handle": "CDK8/CDK19/Cyclin C inhibitors",
        "druggability": 3.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Chemical matter exists, but Wave17 found broad IFN/IL-10/Treg prior art and no direct autoimmune APC inhibitor phenocopy.",
    },
    "GSK3B": {
        "intervention_handle": "GSK3B inhibition",
        "druggability": 2.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Primary macrophage perturbation is partially selective, but target genetics/local breadth are weak and chronic GSK3B modulation is pleiotropic.",
    },
    "RFX5": {
        "intervention_handle": "none direct; transcription-factor gate",
        "druggability": 0.0,
        "manual_prior_risk": "medium",
        "manual_blocker": "Mechanistically selective HLA-II gate but not a tractable drug target.",
    },
    "TNFRSF1A": {
        "intervention_handle": "TNF/TNFR blockade or receptor modulation",
        "druggability": 3.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Mixscale selectivity is not an autoimmune APC result; TNF blockade is saturated and demyelination risk makes it unsuitable as an MS cure route.",
    },
    "CHUK_IKK": {
        "intervention_handle": "IKK/NF-kB inhibition",
        "druggability": 2.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Weak selectivity in Mixscale and broad NF-kB toxicity/prior art.",
    },
    "LRRK2": {
        "intervention_handle": "LRRK2 kinase inhibition",
        "druggability": 3.0,
        "manual_prior_risk": "high",
        "manual_blocker": "L1000 antigen-presentation reversal exists for XMD-1150, but prior V3 gates found no shared cross-autoimmune module support beyond IBD-skewed biology.",
    },
    "CTNNB1": {
        "intervention_handle": "beta-catenin pathway modulation",
        "druggability": 1.0,
        "manual_prior_risk": "high",
        "manual_blocker": "L1000 signal is cell-line only and Wnt/beta-catenin intervention is broad, tissue-context dependent, and not linked to the V3 module.",
    },
    "HSP90AA1": {
        "intervention_handle": "HSP90 inhibition",
        "druggability": 2.5,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Strong L1000 reversal is likely stress/proteostasis/cytotoxic signature, not a selective autoimmune APC transition controller.",
    },
    "PLK1": {
        "intervention_handle": "PLK inhibition",
        "druggability": 2.5,
        "manual_prior_risk": "blocking",
        "manual_blocker": "L1000 signal is oncology/cell-cycle heavy and not compatible with chronic autoimmune therapy.",
    },
    "CTSB": {
        "intervention_handle": "cathepsin B inhibition",
        "druggability": 1.5,
        "manual_prior_risk": "high",
        "manual_blocker": "L1000 CA-074-Me reversal does not overcome prior cathepsin selectivity and lysosomal repair-direction blockers.",
    },
    "FAAH": {
        "intervention_handle": "FAAH inhibition",
        "druggability": 2.0,
        "manual_prior_risk": "high",
        "manual_blocker": "L1000 signal is not supported by V3 module genetics or immune-cell perturbation and overlaps prior inflammatory/pain biology.",
    },
    "MKNK1": {
        "intervention_handle": "MNK inhibition",
        "druggability": 2.0,
        "manual_prior_risk": "high",
        "manual_blocker": "L1000 signal only; translation/initiation kinase route lacks V3 target-specific autoimmune support.",
    },
    "MAPK14": {
        "intervention_handle": "p38 MAPK inhibition",
        "druggability": 2.5,
        "manual_prior_risk": "blocking",
        "manual_blocker": "p38 inflammatory biology is saturated and broad; L1000 signal is insufficient.",
    },
    "CXCR2": {
        "intervention_handle": "CXCR2 antagonism",
        "druggability": 2.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Chemokine recruitment route is not a demonstrated transition-controller and lacks V3 immune-cell selectivity.",
    },
    "PIK3CG": {
        "intervention_handle": "PI3K-gamma inhibition",
        "druggability": 2.5,
        "manual_prior_risk": "high",
        "manual_blocker": "Immune kinase is druggable but prior V3 target-first audit found no module-specific rescue.",
    },
    "RARG": {
        "intervention_handle": "retinoid receptor modulation",
        "druggability": 2.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Retinoid autoimmunity/barrier biology is crowded and V3-specific target support is absent.",
    },
}


CYTOTOXIC_OR_STRESS_TARGETS = {
    "HSP90AA1",
    "PLK1",
    "TUBB",
    "TOP1",
    "TOP2A",
    "PSMB1",
    "ATP5F1A",
    "ATP2A1",
    "ND1",
}


def read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t")


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def clean_gene(name: str) -> str:
    n = str(name).replace("_KO", "").replace("_IFNg", "").replace("_unstimulated", "")
    return n.upper()


def direct_metrics_for(candidate: str, direct: pd.DataFrame) -> dict[str, Any]:
    if direct.empty:
        return {}
    candidate_upper = candidate.upper()
    mask = pd.Series(False, index=direct.index)
    for col in ["perturbation", "condition"]:
        if col in direct.columns:
            mask |= direct[col].astype(str).str.upper().str.contains(candidate_upper, regex=False, na=False)
    if candidate == "CDK8_CDK19_MEDIATOR_KINASE":
        mask = pd.Series(False, index=direct.index)
        for term in ["CDK8", "CDK19", "CCNC", "MED16"]:
            for col in ["perturbation", "condition"]:
                if col in direct.columns:
                    mask |= direct[col].astype(str).str.upper().str.contains(term, regex=False, na=False)
    if candidate == "CHUK_IKK":
        mask = pd.Series(False, index=direct.index)
        for term in ["CHUK", "IKBKB", "IKBKG"]:
            for col in ["perturbation", "condition"]:
                if col in direct.columns:
                    mask |= direct[col].astype(str).str.upper().str.contains(term, regex=False, na=False)
    sub = direct[mask].copy()
    if sub.empty:
        return {}
    sub["selectivity_score_num"] = pd.to_numeric(sub.get("selectivity_score"), errors="coerce")
    best = sub.sort_values("selectivity_score_num", ascending=False).iloc[0].to_dict()
    return {
        "best_direct_source": best.get("source", ""),
        "best_direct_dataset": best.get("dataset", ""),
        "best_direct_perturbation": best.get("perturbation", ""),
        "best_direct_condition": best.get("condition", ""),
        "direct_target_suppression": safe_float(best.get("target_suppression")),
        "direct_generic_ifn_suppression": safe_float(best.get("generic_ifn_suppression")),
        "direct_target_vs_ifn_margin": safe_float(best.get("target_vs_ifn_margin")),
        "direct_target_over_ifn_ratio": safe_float(best.get("target_over_ifn_ratio")),
        "direct_stress_induction": safe_float(best.get("stress_induction")),
        "direct_selectivity_score": safe_float(best.get("selectivity_score")),
        "direct_evidence_call": best.get("evidence_call", ""),
        "direct_is_primary_immune": bool(str(best.get("source", "")).startswith("mouse_macrophage_RNAseq")),
        "n_direct_records": int(len(sub)),
    }


def l1000_metrics_for(candidate: str, l1000: pd.DataFrame) -> dict[str, Any]:
    if l1000.empty or "target" not in l1000.columns:
        return {}
    if candidate == "CDK8_CDK19_MEDIATOR_KINASE":
        terms = ["CDK8", "CDK19"]
    elif candidate == "CHUK_IKK":
        terms = ["IKBKB", "CHUK", "IKBKG"]
    else:
        terms = [candidate]
    mask = pd.Series(False, index=l1000.index)
    for term in terms:
        mask |= l1000["target"].astype(str).str.upper().str.contains(term.upper(), regex=False, na=False)
        mask |= l1000["moa"].astype(str).str.upper().str.contains(term.upper(), regex=False, na=False)
        mask |= l1000["cmap_name"].astype(str).str.upper().str.contains(term.upper(), regex=False, na=False)
    sub = l1000[mask].copy()
    if sub.empty:
        return {}
    sub["strength"] = pd.to_numeric(sub.get("l1000_target_minus_generic_reversal_strength"), errors="coerce").fillna(0)
    best = sub.sort_values("strength", ascending=False).iloc[0].to_dict()
    return {
        "l1000_best_pert_id": best.get("pert_id", ""),
        "l1000_best_cmap_name": best.get("cmap_name", ""),
        "l1000_target": best.get("target", ""),
        "l1000_moa": best.get("moa", ""),
        "l1000_selectivity_call": best.get("l1000_selectivity_call", ""),
        "l1000_target_antigen_best_rank": safe_float(best.get("target_antigen_presentation_best_rank")),
        "l1000_target_antigen_min_qval": safe_float(best.get("target_antigen_presentation_min_qval"), np.nan),
        "l1000_reversal_strength": safe_float(best.get("target_antigen_presentation_max_reversal_strength")),
        "l1000_minus_generic_strength": safe_float(best.get("l1000_target_minus_generic_reversal_strength")),
        "n_l1000_records": int(len(sub)),
    }


def genetics_metrics_for(candidate: str, genetics: pd.DataFrame) -> dict[str, Any]:
    if genetics.empty or "gene" not in genetics.columns:
        return {}
    if candidate == "CDK8_CDK19_MEDIATOR_KINASE":
        genes = ["CDK8", "CDK19", "CCNC", "MED16"]
    elif candidate == "CHUK_IKK":
        genes = ["CHUK", "IKBKB", "IKBKG"]
    else:
        genes = [candidate]
    sub = genetics[genetics["gene"].astype(str).str.upper().isin(genes)]
    if sub.empty:
        return {}
    return {
        "max_ot_disease_count": float(pd.to_numeric(sub.get("ot_n_diseases_score_ge_0_5"), errors="coerce").fillna(0).max()),
        "max_genetics_ready_score": float(pd.to_numeric(sub.get("genetics_ready_score"), errors="coerce").fillna(0).max()),
        "genetics_calls": ";".join(sorted(set(sub.get("proxy_call", pd.Series(dtype=str)).dropna().astype(str)))),
    }


def target_first_metrics_for(candidate: str, target_first: pd.DataFrame) -> dict[str, Any]:
    if target_first.empty or "gene" not in target_first.columns:
        return {}
    if candidate == "CDK8_CDK19_MEDIATOR_KINASE":
        genes = ["CDK8", "CDK19", "CCNC", "MED16"]
    elif candidate == "CHUK_IKK":
        genes = ["CHUK", "IKBKB", "IKBKG"]
    else:
        genes = [candidate]
    sub = target_first[target_first["gene"].astype(str).str.upper().isin(genes)]
    if sub.empty:
        return {}
    return {
        "target_first_calls": ";".join(sorted(set(sub.get("gate_call", pd.Series(dtype=str)).dropna().astype(str)))),
        "target_first_best_priority": float(pd.to_numeric(sub.get("target_first_priority_score"), errors="coerce").fillna(0).max())
        if "target_first_priority_score" in sub.columns
        else 0.0,
        "target_first_manual_blockers": "; ".join(sorted(set(sub.get("manual_blocker", pd.Series(dtype=str)).dropna().astype(str)))),
    }


def local_metrics_for(candidate: str, local: pd.DataFrame) -> dict[str, Any]:
    if local.empty or "gene" not in local.columns:
        return {}
    if candidate == "CDK8_CDK19_MEDIATOR_KINASE":
        genes = ["CDK8", "CDK19", "CCNC", "MED16"]
    elif candidate == "CHUK_IKK":
        genes = ["CHUK", "IKBKB", "IKBKG"]
    else:
        genes = [candidate]
    sub = local[local["gene"].astype(str).str.upper().isin(genes)]
    if sub.empty:
        return {}
    return {
        "local_delta_trend_diseases": float(pd.to_numeric(sub.get("n_trend_or_better_diseases"), errors="coerce").fillna(0).max())
        if "n_trend_or_better_diseases" in sub.columns
        else 0.0,
        "local_fdr10_positive_diseases": float(pd.to_numeric(sub.get("n_fdr10_positive_diseases"), errors="coerce").fillna(0).max())
        if "n_fdr10_positive_diseases" in sub.columns
        else 0.0,
        "local_supporting_diseases": ";".join(sorted(set(";".join(sub.get("supporting_diseases", pd.Series(dtype=str)).dropna().astype(str)).split(";")))),
    }


def prior_penalty(label: str) -> float:
    return {"low": 0.0, "medium": 1.0, "high": 3.0, "blocking": 4.0}.get(label, 2.0)


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    direct = read_table(PATHS["direct_ranked"])
    l1000 = read_table(PATHS["l1000_selective"])
    genetics = read_table(PATHS["wave25_genetics"])
    target_first = read_table(PATHS["wave28_target_first"])
    local = read_table(PATHS["wave14_local"])
    mediator_verdict = {}
    if PATHS["mediator_verdict"].exists():
        mediator_verdict = json.loads(PATHS["mediator_verdict"].read_text())

    rows: list[dict[str, Any]] = []
    gate_rows: list[dict[str, Any]] = []

    for candidate, meta in MANUAL_CANDIDATES.items():
        row: dict[str, Any] = {
            "candidate": candidate,
            "intervention_handle": meta["intervention_handle"],
            "manual_druggability": meta["druggability"],
            "manual_prior_risk": meta["manual_prior_risk"],
            "manual_blocker": meta["manual_blocker"],
        }
        row.update(direct_metrics_for(candidate, direct))
        row.update(l1000_metrics_for(candidate, l1000))
        row.update(genetics_metrics_for(candidate, genetics))
        row.update(target_first_metrics_for(candidate, target_first))
        row.update(local_metrics_for(candidate, local))

        if candidate == "CDK8_CDK19_MEDIATOR_KINASE" and mediator_verdict:
            row["mediator_route_go_no_go"] = mediator_verdict.get("go_no_go", "")
            row["mediator_route_summary"] = mediator_verdict.get("summary", "")
        else:
            row["mediator_route_go_no_go"] = ""
            row["mediator_route_summary"] = ""

        direct_selectivity = safe_float(row.get("direct_selectivity_score"))
        direct_target = safe_float(row.get("direct_target_suppression"))
        direct_generic = safe_float(row.get("direct_generic_ifn_suppression"))
        direct_margin = safe_float(row.get("direct_target_vs_ifn_margin"))
        direct_stress = safe_float(row.get("direct_stress_induction"))
        l1000_strength = safe_float(row.get("l1000_minus_generic_strength"))
        local_diseases = safe_float(row.get("local_delta_trend_diseases"))
        genetics_diseases = safe_float(row.get("max_ot_disease_count"))
        druggability = safe_float(meta["druggability"])
        prior = prior_penalty(str(meta["manual_prior_risk"]))
        cytotoxic_flag = candidate in CYTOTOXIC_OR_STRESS_TARGETS

        gates = {
            "immune_relevant_selective_perturbation": bool(row.get("direct_is_primary_immune"))
            and direct_target >= 1.0
            and direct_margin >= 0.75
            and direct_generic <= 1.0,
            "non_stress_or_cytotoxic": direct_stress <= 0.5 and not cytotoxic_flag,
            "druggable_or_translatable_handle": druggability >= 2.0,
            "translational_phenocopy_available": candidate not in {"MED16", "CDK8_CDK19_MEDIATOR_KINASE"}
            or (candidate == "CDK8_CDK19_MEDIATOR_KINASE" and row.get("mediator_route_go_no_go") == "GO"),
            "cross_disease_target_support": max(local_diseases, genetics_diseases) >= 3,
            "not_prior_art_blocked": prior < 3,
            "l1000_not_only_evidence": bool(row.get("direct_evidence_call")) or l1000_strength == 0,
        }
        failures = [gate for gate, passed in gates.items() if not passed]

        dynamic_score = (
            2.0 * direct_selectivity
            + 1.0 * min(direct_target, 3.0)
            + 0.25 * max(l1000_strength, 0.0)
            + 0.5 * max(local_diseases, genetics_diseases)
            + 0.75 * druggability
            - 1.25 * prior
            - (3.0 if cytotoxic_flag else 0.0)
        )

        if all(gates.values()):
            call = "GO_TO_HOSTILE_NOVELTY_REVIEW"
        elif gates["immune_relevant_selective_perturbation"] and not gates["druggable_or_translatable_handle"]:
            call = "PARK_STRONG_PERTURBATION_NO_DRUGGABLE_HANDLE"
        elif gates["immune_relevant_selective_perturbation"] and gates["druggable_or_translatable_handle"]:
            call = "PARK_SELECTIVE_PERTURBATION_BUT_TRANSLATION_BLOCKED"
        elif l1000_strength > 10 and not gates["l1000_not_only_evidence"]:
            call = "NO_GO_L1000_ONLY_CONTROLLER"
        else:
            call = "NO_GO_DYNAMIC_CONTROLLER"

        row.update(
            {
                "cytotoxic_or_stress_target": cytotoxic_flag,
                "dynamic_controller_score": dynamic_score,
                "n_gate_failures": len(failures),
                "gate_failures": ";".join(failures),
                "wave31_call": call,
            }
        )
        rows.append(row)
        for gate, passed in gates.items():
            gate_rows.append(
                {
                    "candidate": candidate,
                    "gate": gate,
                    "passed": bool(passed),
                    "direct_selectivity": direct_selectivity,
                    "direct_target_suppression": direct_target,
                    "direct_generic_ifn_suppression": direct_generic,
                    "l1000_minus_generic_strength": l1000_strength,
                    "local_diseases": local_diseases,
                    "genetics_diseases": genetics_diseases,
                }
            )

    ranked = pd.DataFrame(rows).sort_values("dynamic_controller_score", ascending=False)
    ranked.to_csv(OUT / "dynamic_transition_controller_audit.tsv", sep="\t", index=False)
    pd.DataFrame(gate_rows).to_csv(OUT / "dynamic_transition_gate_matrix.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "n_candidates": int(len(ranked)),
        "call_counts": ranked["wave31_call"].value_counts().to_dict(),
        "top_dynamic_scores": ranked.head(8)[
            [
                "candidate",
                "dynamic_controller_score",
                "wave31_call",
                "direct_selectivity_score",
                "direct_target_suppression",
                "direct_generic_ifn_suppression",
                "l1000_minus_generic_strength",
                "manual_blocker",
            ]
        ].to_dict(orient="records"),
        "interpretation": (
            "MED16 remains the cleanest selective perturbation comparator, but it has no direct druggable handle. "
            "L1000-only reversals and broad kinase/cytotoxic signatures are insufficient for a therapeutic claim."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
