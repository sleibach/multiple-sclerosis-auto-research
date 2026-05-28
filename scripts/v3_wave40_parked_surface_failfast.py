#!/usr/bin/env python3
"""Wave40 fail-fast of Wave39 parked surfaceome candidates.

Wave39 intentionally used an accessibility-first rescue. It produced no
GO_REVIEW candidates after fixing a proteasome/core-machinery classifier bug,
but it left six PARK_REVIEW rows. This script forces those parked rows through
candidate-specific demotion logic so they do not linger as implicit leads.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave40_parked_surface_failfast"
WAVE39 = ROOT / "results_v3" / "wave39_surfaceome_rescue_after_resolution_pivot" / "surfaceome_rescue_rank_full.tsv"
BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
RESIDUAL = ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
WAVE25 = ROOT / "results_v3" / "wave25_causal_genetics_module_proxy" / "causal_proxy_candidate_matrix.tsv"
WAVE34 = (
    ROOT
    / "results_v3"
    / "wave34_genetics_expression_druggability_scan"
    / "wave34_genetics_expression_druggability_rank.tsv"
)
WAVE21_PRIOR = ROOT / "results_v3" / "wave21_residual_candidate_prior_art" / "candidate_prior_art_gate.tsv"

SEED = 20260527


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def safe_num(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        val = float(value)
    except Exception:
        return default
    return val if math.isfinite(val) else default


def safe_int(value: Any, default: int = 0) -> int:
    return int(round(safe_num(value, default)))


def get_row(df: pd.DataFrame, gene: str, gene_col: str = "gene") -> pd.Series:
    if df.empty or gene_col not in df.columns:
        return pd.Series(dtype=object)
    sub = df.loc[df[gene_col].astype(str).str.upper().eq(gene)]
    if sub.empty:
        return pd.Series(dtype=object)
    return sub.iloc[0]


def classify(gene: str, row: pd.Series, residual: pd.Series, wave25: pd.Series, wave34: pd.Series, prior: pd.Series) -> tuple[str, str, list[str]]:
    blockers: list[str] = []
    required_evidence: list[str] = []

    europe = safe_int(row.get("europepmc_hit_count"))
    trials = safe_int(row.get("clinicaltrials_hit_count"))
    chembl_activity = safe_int(row.get("chembl_activity_count"))
    negative_diseases = safe_int(row.get("negative_disease_count"))
    pos_diseases = safe_int(row.get("positive_disease_count"))
    ms_p = safe_num(row.get("ms_wm_p"), 1.0)
    ms_fdr = safe_num(row.get("ms_wm_fdr"), 1.0)
    ms_delta = safe_num(row.get("ms_wm_delta_log2"))
    strict_residual = safe_int(residual.get("strict_core_covariate_surviving_disease_count"))
    residual_non_ibd = safe_int(residual.get("non_ibd_retained_positive_disease_count"))

    if pos_diseases < 5 and not (pos_diseases >= 4 and ms_delta > 0.5 and ms_p <= 0.1):
        blockers.append("breadth_or_MS_anchor_below_promotion_gate")
    if ms_fdr > 0.2:
        blockers.append("MS_anchor_nominal_or_trend_only_not_FDR_supported")
    if negative_diseases > 0:
        blockers.append("same_gene_has_negative_disease_or_compartment_signal")
    if strict_residual == 0:
        blockers.append("no_strict_core_covariate_residual_survival")
    if residual_non_ibd == 0:
        blockers.append("no_non_IBD_strict_residual_support")
    if europe >= 1000 or trials > 0:
        blockers.append("prior_art_or_trial_saturation")
    if chembl_activity == 0 and str(row.get("chembl_target_chembl_id", "") or "") == "":
        blockers.append("no_mature_chemical_target_package")

    wave25_call = str(wave25.get("proxy_call", "") or "")
    if wave25_call and wave25_call != "nan":
        blockers.append(f"wave25_{wave25_call}")
    wave34_call = str(wave34.get("wave34_call", "") or "")
    if wave34_call and wave34_call != "nan" and not wave34_call.startswith("PARK"):
        blockers.append(f"wave34_{wave34_call}")
    prior_rec = str(prior.get("recommendation", "") or "")
    if prior_rec and prior_rec != "nan":
        blockers.append(f"prior_review_{prior_rec[:80]}")

    if gene == "MMP7":
        blockers.extend(
            [
                "secreted_matrix_protease_repair_barrier_liability",
                "broad_inhibition_risks_tissue_remodeling_and_epithelial_repair",
            ]
        )
        required_evidence.extend(
            [
                "cell-type-specific MMP7 inhibition in MS lesion or gut/skin organoid that lowers pathogenic state without impairing barrier repair",
                "substrate-level proof that the pathogenic substrate, not generic injury remodeling, is causal",
            ]
        )
    elif gene == "CD82":
        blockers.extend(
            [
                "previously_demoted_as_raw_state_marker",
                "tetraspanin_direction_agonism_vs_blockade_undefined",
            ]
        )
        required_evidence.extend(
            [
                "isoform or complex-specific CD82 perturbation with target engagement",
                "strict residual survival independent of IFN/HLA-II/repair modules",
            ]
        )
    elif gene == "FXYD5":
        blockers.extend(
            [
                "single_negative_Crohn_signal_conflicts_with_cross_disease_direction",
                "no_ChEMBL_activity_or_defined_antibody_modality_in_local_scan",
                "NaK_ATPase_regulator_direction_not_autoimmune_specific",
            ]
        )
        required_evidence.extend(
            [
                "independent human tissue replication of FXYD5-positive pathogenic compartment",
                "non-depleting antibody or genetic perturbation showing state reversal and preserved epithelial/barrier function",
            ]
        )
    elif gene == "SCD":
        blockers.extend(
            [
                "lipid_metabolism_enzyme_reopens_failed_lipid_axis",
                "systemic_SCD_inhibition_has_metabolic_and_barrier_risk",
            ]
        )
        required_evidence.extend(
            [
                "local tissue-restricted SCD perturbation that reverses state without worsening repair/metabolic stress",
                "genetic or perturbational evidence not explained by generic lipid stress",
            ]
        )
    elif gene == "CCL20":
        blockers.extend(
            [
                "generic_CCL20_CCR6_trafficking_axis",
                "chemokine_blockade_direction_not_module_specific",
            ]
        )
        required_evidence.extend(
            [
                "CCR6/CCL20 target-resolved causal genetics or ex vivo neutralization outperforming generic anti-inflammatory suppression",
                "patient subset where CCL20 is upstream of lesion/tissue state rather than downstream inflammation",
            ]
        )
    elif gene == "IL23A":
        blockers.extend(
            [
                "established_IL23_autoimmune_axis_not_novel",
                "missing_local_target_resolved_coloc_or_MR_package",
            ]
        )
        required_evidence.extend(
            [
                "MS-specific or cross-autoimmune subgroup where IL23A predicts failure of existing DMTs and response to IL-23 blockade",
                "evidence that the IL23A signal is causal outside already established IBD/psoriasis biology",
            ]
        )

    blockers = sorted(set(blockers))
    required_evidence = sorted(set(required_evidence))
    call = "NO_GO_PARKED_SURFACE_FAILFAST"
    if gene == "FXYD5":
        call = "PARK_ONLY_IF_NEW_PERTURBATION"
    return call, "; ".join(blockers), required_evidence


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    wave39 = read_tsv(WAVE39)
    if wave39.empty:
        raise FileNotFoundError(WAVE39)
    broad = read_tsv(BROAD)
    residual = read_tsv(RESIDUAL)
    wave25 = read_tsv(WAVE25)
    wave34 = read_tsv(WAVE34)
    prior = read_tsv(WAVE21_PRIOR)

    parked = wave39.loc[wave39["wave39_call"].eq("PARK_REVIEW")].copy()
    rows = []
    for _, row in parked.iterrows():
        gene = str(row["gene"]).upper()
        b = get_row(broad, gene)
        r = get_row(residual, gene)
        w25 = get_row(wave25, gene)
        w34 = get_row(wave34, gene)
        pr = get_row(prior, gene, gene_col="candidate")
        call, blockers, required = classify(gene, row, r, w25, w34, pr)
        rows.append(
            {
                "gene": gene,
                "wave40_call": call,
                "blockers": blockers,
                "required_evidence_to_reopen": " | ".join(required),
                "wave39_score": row.get("wave39_score"),
                "positive_disease_count": row.get("positive_disease_count"),
                "negative_disease_count": row.get("negative_disease_count"),
                "positive_diseases": row.get("positive_diseases"),
                "ms_wm_delta_log2": row.get("ms_wm_delta_log2"),
                "ms_wm_p": row.get("ms_wm_p"),
                "ms_wm_fdr": b.get("ms_wm_fdr", row.get("ms_wm_fdr")),
                "strict_core_covariate_surviving_disease_count": r.get("strict_core_covariate_surviving_disease_count", ""),
                "non_ibd_retained_positive_disease_count": r.get("non_ibd_retained_positive_disease_count", ""),
                "wave25_proxy_call": w25.get("proxy_call", ""),
                "wave34_call": w34.get("wave34_call", ""),
                "wave34_primary_blocker": w34.get("primary_blocker", ""),
                "prior_review_recommendation": pr.get("recommendation", ""),
                "chembl_target_pref_name": row.get("chembl_target_pref_name", ""),
                "chembl_activity_count": row.get("chembl_activity_count", ""),
                "europepmc_hit_count": row.get("europepmc_hit_count", ""),
                "clinicaltrials_hit_count": row.get("clinicaltrials_hit_count", ""),
                "uniprot_locations": row.get("uniprot_locations", ""),
                "function_excerpt": row.get("function_excerpt", ""),
            }
        )

    out = pd.DataFrame(rows)
    out.to_csv(OUT / "parked_surface_failfast.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "parked_candidates_evaluated": int(len(out)),
        "call_counts": out["wave40_call"].value_counts().to_dict(),
        "genes": out["gene"].tolist(),
        "promoted_genes": [],
        "reopen_only_genes": out.loc[out["wave40_call"].eq("PARK_ONLY_IF_NEW_PERTURBATION"), "gene"].tolist(),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Wave40 Parked Surface Fail-Fast",
        "",
        "## Result",
        "",
        f"- Parked Wave39 candidates evaluated: {len(out)}.",
        f"- Calls: {json.dumps(summary['call_counts'], sort_keys=True)}.",
        "",
        "## Candidate Decisions",
        "",
    ]
    for _, row in out.iterrows():
        lines.append(f"- `{row['gene']}`: {row['wave40_call']}; {row['blockers']}")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "Wave39's parked surface/secreted candidates do not become V3 leads.",
            "`FXYD5` remains a narrow artifact/reopening check only because it is",
            "accessible and relatively less prior-art saturated, but it lacks a mature",
            "modality, has a conflicting Crohn signal, and has no target-level causal",
            "or perturbation evidence.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
