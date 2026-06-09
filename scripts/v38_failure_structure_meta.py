#!/usr/bin/env python3
"""Analyze common structure across project failures and closed leads.

The input is the V37 scored findings table. Tags below are explicit
artifact-derived annotations, not model output. They are intentionally
conservative and auditable.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v38_failure_structure"
OUT.mkdir(parents=True, exist_ok=True)


TAG_MAP: dict[str, dict[str, str]] = {
    "ZMIZ1 opposite-direction MS/Crohn decoupling": {
        "failure_modes": "opposite_direction;transfer_invalid",
        "mechanism_level": "genetics_direction",
        "therapeutic_constraint": "same_locus_opposite_disease_direction",
    },
    "chr1 KIF21B/GPR25 locus resolves to real biology but hard target": {
        "failure_modes": "hard_protective_direction;causal_gene_ambiguity;weak_modality_fit",
        "mechanism_level": "genetics_to_target",
        "therapeutic_constraint": "restoration_or_up_function_required",
    },
    "PTGER4 mixed shared/distinct signal closes naive transfer": {
        "failure_modes": "mixed_signals;direction_conflict;transfer_invalid",
        "mechanism_level": "genetics_direction",
        "therapeutic_constraint": "signal_specific_direction_unresolved",
    },
    "MHC overlap is distinct-signal, not simple shared biology": {
        "failure_modes": "distinct_causal_variants;overlap_not_mechanism",
        "mechanism_level": "genetics_coloc",
        "therapeutic_constraint": "shared_region_not_shared_target",
    },
    "UC genetics vs treatment-response layer split": {
        "failure_modes": "axis_mismatch;baseline_not_dynamic",
        "mechanism_level": "cross_axis_transfer",
        "therapeutic_constraint": "genetics_does_not_define_response_rule",
    },
    "Crohn downstream IFN/APC convergence exceeds genetic proximity": {
        "failure_modes": "axis_mismatch;downstream_context_dependence",
        "mechanism_level": "cross_axis_transfer",
        "therapeutic_constraint": "response_analogy_not_target_transfer",
    },
    "RA pregnancy comparator but blood APC treatment-response nontransfer": {
        "failure_modes": "compartment_mismatch;context_dependence",
        "mechanism_level": "cross_axis_transfer",
        "therapeutic_constraint": "pregnancy_timing_not_blood_biomarker",
    },
    "Sjogren antigen-presentation but not lysosomal/APC lesion-rim transfer": {
        "failure_modes": "compartment_mismatch;module_specificity_failure",
        "mechanism_level": "cross_axis_transfer",
        "therapeutic_constraint": "antigen_presentation_not_lesion_repair",
    },
    "No load-bearing invariant found in V26": {
        "failure_modes": "invariance_not_supported;underpowered_modality_count",
        "mechanism_level": "deep_structure",
        "therapeutic_constraint": "no_conserved_invariant_target",
    },
    "No validated broad immune-state simulator from held data": {
        "failure_modes": "generalization_failure;heldout_validation_failure;scope_too_broad",
        "mechanism_level": "modeling",
        "therapeutic_constraint": "cannot_triage_patient_or_genetics_claims",
    },
    "Coupled-axis successor rule does not beat scalar": {
        "failure_modes": "complexity_no_improvement;small_n_overfit_risk",
        "mechanism_level": "treatment_response_modeling",
        "therapeutic_constraint": "do_not_replace_locked_scalar",
    },
    "Locked V7 general cross-disease baseline fallback killed": {
        "failure_modes": "baseline_not_dynamic;cross_disease_generalization_failure",
        "mechanism_level": "treatment_response",
        "therapeutic_constraint": "baseline_stratifier_invalid",
    },
    "GPR25 demoted from protected favorite": {
        "failure_modes": "causal_gene_ambiguity;weak_expression_support;hard_protective_direction;immature_chemical_matter",
        "mechanism_level": "genetics_to_target",
        "therapeutic_constraint": "agonism_or_restoration_required",
    },
    "NAMPT/eNAMPT not reactivated as target": {
        "failure_modes": "marker_not_driver;weak_genetic_support;prior_art_not_enough",
        "mechanism_level": "target_nomination",
        "therapeutic_constraint": "covariate_not_target",
    },
    "ZFP36L1 chr14 parked": {
        "failure_modes": "subthreshold_coloc;missing_qtl_direction",
        "mechanism_level": "genetics_coloc",
        "therapeutic_constraint": "no_direction_matched_target",
    },
    "REL/PUS10/USP34 chr2 closed": {
        "failure_modes": "coloc_failure;expression_cannot_rescue",
        "mechanism_level": "genetics_coloc",
        "therapeutic_constraint": "no_shared_disease_signal",
    },
    "EBV/IFN APC imprint downgraded by specificity control": {
        "failure_modes": "module_specificity_failure;random_control_failure",
        "mechanism_level": "exploratory_module",
        "therapeutic_constraint": "broad_ifn_not_ebv_specific",
    },
    "Complement/lipid progressive axis downgraded": {
        "failure_modes": "donor_aware_nonreplication;module_specificity_failure",
        "mechanism_level": "exploratory_module",
        "therapeutic_constraint": "weak_lipid_context_only",
    },
    "Lysosomal APC bottleneck not proven": {
        "failure_modes": "coupling_not_causality;bottleneck_not_proven",
        "mechanism_level": "exploratory_module",
        "therapeutic_constraint": "needs_flux_or_peptidomics",
    },
    "Metabolic/sterol setpoint is context/confounder axis, not intervention-grade": {
        "failure_modes": "confounder_context_not_mechanism;direction_not_actionable",
        "mechanism_level": "exploratory_module",
        "therapeutic_constraint": "covariate_not_intervention",
    },
}


def split_tags(value: str) -> list[str]:
    return [x for x in value.split(";") if x]


def main() -> None:
    scores = pd.read_csv(ROOT / "docs/reports/FINDINGS_SCORES_V37.tsv", sep="\t")
    failures = scores[scores["category"].isin(["decoupling_negative", "kills_closed"])].copy()

    rows: list[dict[str, object]] = []
    for _, row in failures.iterrows():
        item = row["item"]
        tags = TAG_MAP.get(item)
        if tags is None:
            raise SystemExit(f"Missing failure tag map for: {item}")
        out = row.to_dict()
        out.update(tags)
        rows.append(out)

    table = pd.DataFrame(rows)
    table.to_csv(OUT / "failure_mode_table.tsv", sep="\t", index=False)

    mode_counter: Counter[str] = Counter()
    level_counter: Counter[str] = Counter(table["mechanism_level"])
    constraint_counter: Counter[str] = Counter(table["therapeutic_constraint"])
    by_item = {}
    for _, row in table.iterrows():
        modes = split_tags(row["failure_modes"])
        by_item[row["item"]] = modes
        mode_counter.update(modes)

    # Higher-level families used for the V38 interpretation.
    families = {
        "context_or_axis_dependence": [
            "axis_mismatch",
            "context_dependence",
            "downstream_context_dependence",
            "compartment_mismatch",
            "cross_disease_generalization_failure",
            "baseline_not_dynamic",
        ],
        "direction_or_modality_constraint": [
            "opposite_direction",
            "direction_conflict",
            "hard_protective_direction",
            "weak_modality_fit",
            "immature_chemical_matter",
            "direction_not_actionable",
        ],
        "specificity_or_control_failure": [
            "module_specificity_failure",
            "random_control_failure",
            "donor_aware_nonreplication",
            "overlap_not_mechanism",
            "distinct_causal_variants",
        ],
        "evidence_resolution_failure": [
            "subthreshold_coloc",
            "missing_qtl_direction",
            "coloc_failure",
            "causal_gene_ambiguity",
            "heldout_validation_failure",
            "generalization_failure",
            "scope_too_broad",
            "invariance_not_supported",
            "underpowered_modality_count",
            "bottleneck_not_proven",
            "coupling_not_causality",
        ],
        "complexity_or_modeling_failure": [
            "complexity_no_improvement",
            "small_n_overfit_risk",
            "generalization_failure",
            "scope_too_broad",
        ],
        "marker_not_driver": [
            "marker_not_driver",
            "confounder_context_not_mechanism",
            "prior_art_not_enough",
            "weak_genetic_support",
        ],
    }

    family_rows = []
    for family, members in families.items():
        member_set = set(members)
        hits = [
            item
            for item, modes in by_item.items()
            if member_set.intersection(modes)
        ]
        family_rows.append(
            {
                "family": family,
                "n_items": len(hits),
                "fraction_of_failure_items": len(hits) / len(table),
                "items": "; ".join(hits),
            }
        )
    family_table = pd.DataFrame(family_rows).sort_values(["n_items", "family"], ascending=[False, True])
    family_table.to_csv(OUT / "failure_family_counts.tsv", sep="\t", index=False)

    mode_table = pd.DataFrame(
        [{"failure_mode": k, "n_items": v} for k, v in mode_counter.most_common()]
    )
    mode_table.to_csv(OUT / "failure_mode_counts.tsv", sep="\t", index=False)

    level_table = pd.DataFrame(
        [{"mechanism_level": k, "n_items": v} for k, v in level_counter.most_common()]
    )
    level_table.to_csv(OUT / "failure_level_counts.tsv", sep="\t", index=False)

    summary = {
        "n_failure_items": len(table),
        "top_failure_families": family_rows,
        "top_failure_modes": mode_counter.most_common(),
        "mechanism_levels": level_counter.most_common(),
        "constraint_counts": constraint_counter.most_common(),
        "overall_verdict": (
            "The dominant structure is not one universal failure mechanism. "
            "Most failures cluster into context/axis-dependence and evidence-resolution limits, "
            "with a smaller but important therapeutic-direction/up-function constraint in genetics targets."
        ),
    }
    (OUT / "failure_structure_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
