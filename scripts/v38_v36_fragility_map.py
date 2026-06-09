#!/usr/bin/env python3
"""Aggregate V36 exploratory fragility modes.

V36 produced many grounded side analyses. This V38 pass treats those outputs as
a dataset and asks which unconventional hypothesis classes repeatedly failed:
multiplicity, confounding/composition, therapy/timepoint specificity, data
absence, or sample-size fragility.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "analysis/v38_v36_fragility_map"


def load_json(rel: str) -> dict:
    with (ROOT / rel).open() as handle:
        return json.load(handle)


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rows = []

    mult = load_json("analysis/v36_feature_multiplicity_stress/summary.json")
    rows.append(
        {
            "artifact": "v36_feature_multiplicity_stress",
            "source": "analysis/v36_feature_multiplicity_stress/summary.json",
            "fragility_family": "multiplicity_overfit",
            "grounded_status": "blocks_posthoc_feature_promotion",
            "key_metric": f"{mult['features_tested']} features; observed max AUC {mult['observed_max_auc']}; empirical max-AUC p {mult['max_auc_empirical_p']}",
            "promotion_effect": "demote_complex_or_perfect_auc_posthoc_features",
        }
    )

    gene_null = load_json("analysis/v36_locked_gene_module_null/summary.json")
    rows.append(
        {
            "artifact": "v36_locked_gene_module_null",
            "source": "analysis/v36_locked_gene_module_null/summary.json",
            "fragility_family": "multiplicity_overfit",
            "grounded_status": "blocks_locked_gene_subset_claim",
            "key_metric": f"top IFN/STAT AUC {gene_null['top_ifn_stat_auc']}; empirical p {gene_null['top_ifn_stat_empirical_p']}",
            "promotion_effect": "gene-subset variants not promoted",
        }
    )

    combo = load_json("analysis/v36_compartment_combo_scan/summary.json")
    rows.append(
        {
            "artifact": "v36_compartment_combo_scan",
            "source": "analysis/v36_compartment_combo_scan/summary.json",
            "fragility_family": "multiplicity_compartment_scan",
            "grounded_status": "overfit_warning",
            "key_metric": f"{combo['n_combinations']} compartment combinations; best {combo['best_combo']['combo']} AUC {combo['best_combo']['auc_oriented']}; B/plasma AUC {combo['b_plasma_only']['auc_oriented']}",
            "promotion_effect": "report compartments separately; no combo successor",
        }
    )

    tb = load_json("analysis/v36_tb_gate_artifact_audit/summary.json")
    rows.append(
        {
            "artifact": "v36_tb_gate_artifact_audit",
            "source": "analysis/v36_tb_gate_artifact_audit/summary.json",
            "fragility_family": "composition_confounding",
            "grounded_status": tb["grounded_result"],
            "key_metric": f"T/B gap {tb['locked_tb_minus_non_tb_auc_gap']} -> {tb['residualized_tb_minus_non_tb_auc_gap']}; T-cell {tb['t_cell_locked_auc']} -> {tb['t_cell_residualized_auc']}; B/plasma {tb['b_plasma_locked_auc']} -> {tb['b_plasma_residualized_auc']}",
            "promotion_effect": "narrows T/B gate toward B/plasma-stabler signal",
        }
    )

    comp = load_json("analysis/v36_compartment_confounder_residualization/summary.json")
    rows.append(
        {
            "artifact": "v36_compartment_confounder_residualization",
            "source": "analysis/v36_compartment_confounder_residualization/summary.json",
            "fragility_family": "composition_confounding",
            "grounded_status": "strong_attenuation_under_confounders",
            "key_metric": f"worst T-cell residual AUC {comp['worst_t_cell_residual_auc']}; worst B/plasma residual AUC {comp['worst_b_plasma_residual_auc']}",
            "promotion_effect": "compartment signal remains audit target, not locked rule",
        }
    )

    dmt = load_json("analysis/v36_ms_dmt_locked_sensitivity/summary.json")
    rows.append(
        {
            "artifact": "v36_ms_dmt_locked_sensitivity",
            "source": "analysis/v36_ms_dmt_locked_sensitivity/summary.json",
            "fragility_family": "small_n_therapy_specificity",
            "grounded_status": "dmf_directional_fingolimod_null",
            "key_metric": f"DMF AUC {dmt['dmf_locked']['auc']} exact p {dmt['dmf_locked']['exact_auc_p']}; fingolimod AUC {dmt['fingolimod_locked']['auc']} exact p {dmt['fingolimod_locked']['exact_auc_p']}",
            "promotion_effect": "keep bounded DMF/JAK-like domain; no cross-DMT claim",
        }
    )

    therapy = load_json("analysis/v36_therapy_branch_map/summary.json")
    branch_bits = [
        f"{row['therapy']}:{row['branch']} maxAUC={row['max_auc']}"
        for row in therapy["branch_summary"]
    ]
    rows.append(
        {
            "artifact": "v36_therapy_branch_map",
            "source": "analysis/v36_therapy_branch_map/summary.json",
            "fragility_family": "therapy_branch_specificity",
            "grounded_status": "mechanism_bounded_not_universal",
            "key_metric": "; ".join(branch_bits),
            "promotion_effect": "validation must be therapy-branch aware",
        }
    )

    power = load_json("analysis/v36_gafson_power_simulation/summary.json")
    n30 = next(row for row in power["power_table"] if row["n_per_group"] == 30)
    n40 = next(row for row in power["power_table"] if row["n_per_group"] == 40)
    rows.append(
        {
            "artifact": "v36_gafson_power_simulation",
            "source": "analysis/v36_gafson_power_simulation/summary.json",
            "fragility_family": "sample_size_power",
            "grounded_status": "fresh_validation_needs_substantial_n",
            "key_metric": f"n=30/group p<0.05 power {n30['power_one_sided_p_lt_0_05']}; n=40/group power {n40['power_one_sided_p_lt_0_05']}",
            "promotion_effect": "small validation cohorts can estimate direction but not settle claim",
        }
    )

    generated = load_json("analysis/v36_tri_source_generation/grounded_generated_hypotheses.json")
    for item in generated:
        rows.append(
            {
                "artifact": "v36_tri_source_generation",
                "source": "analysis/v36_tri_source_generation/grounded_generated_hypotheses.json",
                "fragility_family": "creative_generation_data_gate",
                "grounded_status": item["grounded_result"],
                "key_metric": json.dumps(item.get("key_numbers", {}), sort_keys=True),
                "promotion_effect": "no upgrade from tri-source generated hypothesis",
            }
        )

    rows.extend(
        [
            {
                "artifact": "v36_postpartum_ms_specificity",
                "source": "analysis/v36_postpartum_ms_specificity/summary.md",
                "fragility_family": "missing_decisive_metadata",
                "grounded_status": "pregnancy_phase_supported_postpartum_relapse_test_blocked",
                "key_metric": "MS month-9 HLA-II-minus-CD64 delta -1.332 p=0.00127; no postpartum samples or relapse labels",
                "promotion_effect": "data-acquisition lead only",
            },
            {
                "artifact": "v36_remaining_shortlist_deepening",
                "source": "analysis/v36_remaining_shortlist_deepening/summary.md",
                "fragility_family": "missing_decisive_modality",
                "grounded_status": "no_shortlist_upgrades",
                "key_metric": "metabolic context only; lysosomal no flux/peptidomics; complement/EBV not supported without new stratified data",
                "promotion_effect": "keeps V35/V36 shortlist data-gated",
            },
            {
                "artifact": "v36_technical_qc_batch_feasibility",
                "source": "analysis/v36_technical_qc_batch_feasibility/summary.json",
                "fragility_family": "technical_qc_limit",
                "grounded_status": "limited_batch_covariate_structure",
                "key_metric": "single instrument model, single processing category; W8 samples n=8",
                "promotion_effect": "QC audit cannot fully de-risk treated-timepoint features",
            },
        ]
    )

    df = pd.DataFrame(rows)
    df.to_csv(OUTDIR / "v36_fragility_items.tsv", sep="\t", index=False)

    counts = (
        df.groupby("fragility_family")
        .size()
        .reset_index(name="n_items")
        .sort_values("n_items", ascending=False)
    )
    counts.to_csv(OUTDIR / "v36_fragility_family_counts.tsv", sep="\t", index=False)

    summary = {
        "n_items": int(len(df)),
        "fragility_family_counts": counts.to_dict(orient="records"),
        "main_interpretation": (
            "V36 did not fail because ideas were biologically implausible; it "
            "failed to promote them because strict gates exposed recurring "
            "fragility: multiplicity/overfit, composition/confounder sensitivity, "
            "therapy-branch specificity, small-n power limits, and missing decisive "
            "metadata/modalities."
        ),
        "surviving_narrow_signal": (
            "B/plasma-like IFN/APC remodeling remains the most stable internal "
            "carrier, but it is still single-cohort and validation-gated."
        ),
    }
    with (OUTDIR / "v36_fragility_map_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2)


if __name__ == "__main__":
    main()
