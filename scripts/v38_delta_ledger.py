#!/usr/bin/env python3
"""Write the structured V37-to-V38 delta ledger."""

from __future__ import annotations

import json
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "analysis/v38_delta_ledger"


ROWS = [
    {
        "v37_item": "bounded APC/HLA-II V22/V23 monitoring scalar",
        "v38_delta": "strengthened_and_narrowed",
        "evidence_grade_change": "no_change_provisional",
        "supporting_v38_artifacts": "analysis/v38_adversarial_monitoring/grounded_inversion_summary.json; analysis/v38_control_system/control_system_summary.json; analysis/v38_tone_residual_scalar/tone_residual_scalar_summary.json",
        "delta_statement": "Survived adversarial inversion and broad-tone residual test, but remains bounded, small-n, not MS-calibrated, not a clinical threshold, and pending Gafson/DMF validation.",
        "next_action": "Run frozen validation harness on fresh Gafson/DMF or equivalent paired response cohort.",
    },
    {
        "v37_item": "V26 coupled APC architecture",
        "v38_delta": "strengthened_and_narrowed",
        "evidence_grade_change": "no_change_supported_structural",
        "supporting_v38_artifacts": "analysis/v38_coupled_architecture_inversion/coupled_inversion_summary.json",
        "delta_statement": "Core APC dependencies survive row-wise global-tone residualization, but the architecture is heavily tone-loaded and remains mechanistic context, not a predictive successor.",
        "next_action": "Measure coupled modules as secondary exploratory outputs in fresh validation; do not replace V22 scalar.",
    },
    {
        "v37_item": "MS-UC genome-wide genetic-correlation backdrop",
        "v38_delta": "strengthened_and_narrowed",
        "evidence_grade_change": "no_change_supported",
        "supporting_v38_artifacts": "analysis/v38_rg_backdrop_inversion/rg_backdrop_inversion_summary.json",
        "delta_statement": "MS-UC rg withstands recorded MHC/sample-overlap inversion, but MHC sensitivity is not independent because the verified LDSC panel was already effectively MHC-free.",
        "next_action": "Avoid locus-level transfer claims from rg; extend LDSC only with intercept and MHC-reference caveats.",
    },
    {
        "v37_item": "V10/V12 layer-transfer map",
        "v38_delta": "strengthened_and_narrowed",
        "evidence_grade_change": "no_change_supported",
        "supporting_v38_artifacts": "analysis/v38_layer_transfer_inversion/layer_transfer_inversion_summary.json; analysis/v38_layer_heterogeneity_null/layer_heterogeneity_null_summary.json",
        "delta_statement": "Map withstands narrative-similarity inversion through disagreement-cell evidence, but simple 4/4 disease heterogeneity is not statistically exceptional by itself.",
        "next_action": "Use as transfer-warning/triage framework, not intervention transfer.",
    },
    {
        "v37_item": "closed/negative lead structure",
        "v38_delta": "new_operational_prefilter",
        "evidence_grade_change": "new_supported_methodological",
        "supporting_v38_artifacts": "analysis/v38_failure_structure/failure_structure_summary.json; analysis/v38_direction_modality_prefilter/direction_modality_prefilter_summary.json",
        "delta_statement": "Failures cluster around evidence resolution, context/axis dependence, direction/modality, and specificity/control; direction/modality affects 5/6 target-like closed/negative items.",
        "next_action": "Apply direction-matched-modality and context/axis prefilters before deep work on future target leads.",
    },
    {
        "v37_item": "exclusion / non-replication side of the project",
        "v38_delta": "strengthened_negative_ledger",
        "evidence_grade_change": "new_negative_established_ledger",
        "supporting_v38_artifacts": "analysis/v38_exclusion_ledger/exclusion_summary.json",
        "delta_statement": "V38 turned scattered kills into a 16-item stop-spending ledger of unsupported transfer, target, simulator, and biomarker interpretations.",
        "next_action": "Require named new evidence before reopening any ledger item.",
    },
    {
        "v37_item": "V36 exploratory hypothesis machinery",
        "v38_delta": "new_fragility_structure",
        "evidence_grade_change": "new_supported_methodological",
        "supporting_v38_artifacts": "analysis/v38_v36_fragility_map/v36_fragility_map_summary.json; analysis/v38_failure_fragility_concordance/failure_fragility_concordance_summary.json",
        "delta_statement": "V36 creative hypotheses failed promotion at multiplicity, confounder/composition, therapy-branch, power, and missing-modality gates; this is complementary to the V38 lead-failure map.",
        "next_action": "Use both maps: V38 for lead triage, V36 for analysis-design triage.",
    },
    {
        "v37_item": "RPT/tabular-lens contribution",
        "v38_delta": "methodological_value_without_evidence_upgrade",
        "evidence_grade_change": "no_finding_upgrade",
        "supporting_v38_artifacts": "analysis/v38_rpt_structural_mining/v38_rpt_grounded_summary.json",
        "delta_statement": "RPT mostly reproduced the action taxonomy and sharpened that the bounded scalar is operationally prioritized, not structurally exceptional.",
        "next_action": "Continue using RPT as prioritization lens only; never as evidence.",
    },
]


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    fieldnames = list(ROWS[0].keys())
    with (OUTDIR / "v37_v38_delta_ledger.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(ROWS)
    delta_counts: dict[str, int] = {}
    evidence_counts: dict[str, int] = {}
    for row in ROWS:
        delta_counts[row["v38_delta"]] = delta_counts.get(row["v38_delta"], 0) + 1
        evidence_counts[row["evidence_grade_change"]] = evidence_counts.get(row["evidence_grade_change"], 0) + 1
    summary = {
        "n_delta_items": len(ROWS),
        "delta_counts": delta_counts,
        "evidence_grade_changes": evidence_counts,
        "demotions": [row for row in ROWS if "demot" in row["v38_delta"].lower()],
    }
    with (OUTDIR / "v37_v38_delta_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2)


if __name__ == "__main__":
    main()
