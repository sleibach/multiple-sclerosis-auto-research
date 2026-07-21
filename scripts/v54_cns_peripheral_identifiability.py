#!/usr/bin/env python3
"""Audit whether held data can separate CNS and peripheral progression states."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from scipy.stats import fisher_exact


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_cns_peripheral_identifiability"


def yn(value: bool) -> str:
    return "yes" if value else "no"


def evidence_row(
    *,
    dataset: str,
    compartment: str,
    artifact: str,
    n_units: int,
    phenotype: str,
    minimum_group_n: int,
    verified_subject_map: bool,
    processed_expression_held: bool,
    frozen_module_coverage: bool,
    source_batch_control: str,
    activity_treatment_control: str,
    composition_control: str,
    matched_cross_compartment_phenotype: bool,
    repeated_disability_or_conversion: bool,
    observed_result: str,
    blocker: str,
) -> dict[str, Any]:
    cross_sectional = all(
        [
            minimum_group_n >= 10,
            verified_subject_map,
            processed_expression_held,
            frozen_module_coverage,
            source_batch_control == "adequate",
            activity_treatment_control == "adequate",
            composition_control == "adequate",
            matched_cross_compartment_phenotype,
        ]
    )
    progression = cross_sectional and repeated_disability_or_conversion
    return {
        "dataset": dataset,
        "compartment": compartment,
        "source_artifact": artifact,
        "n_independent_units": n_units,
        "phenotype_contrast": phenotype,
        "minimum_group_n": minimum_group_n,
        "verified_subject_map": yn(verified_subject_map),
        "processed_expression_held": yn(processed_expression_held),
        "frozen_module_coverage": yn(frozen_module_coverage),
        "source_batch_control": source_batch_control,
        "activity_treatment_control": activity_treatment_control,
        "composition_control": composition_control,
        "matched_cross_compartment_phenotype": yn(matched_cross_compartment_phenotype),
        "repeated_disability_or_adjudicated_conversion": yn(
            repeated_disability_or_conversion
        ),
        "cross_sectional_separation_eligible": yn(cross_sectional),
        "progression_separation_eligible": yn(progression),
        "observed_result": observed_result,
        "blocking_reason": blocker,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    stage_summary_path = Path("analysis/v54_progressive_stage_modules/summary.json")
    lesion_summary_path = Path("analysis/v54_progression_lesion_state/summary.json")
    panel_summary_path = Path("analysis/v54_progression_lesion_module_panel/summary.json")
    stage_summary = json.loads((ROOT / stage_summary_path).read_text())
    lesion_summary = json.loads((ROOT / lesion_summary_path).read_text())
    panel_summary = json.loads((ROOT / panel_summary_path).read_text())

    assert stage_summary["n_donors"] == 44
    assert stage_summary["n_supported_modules"] == 0
    assert lesion_summary["gse180759_n_primary_pairs"] == 3
    assert lesion_summary["gse279972_n_donors"] == 21
    assert not panel_summary["orthogonally_consistent_modules"]

    gse228_path = Path(
        "analysis/v45_gse228330_outcome_scout/gse228330_sample_metadata.tsv"
    )
    gse228 = pd.read_csv(ROOT / gse228_path, sep="\t")
    baseline = gse228.loc[gse228["treatment_duration_month"].eq(0)].copy()
    baseline["subtype"] = baseline["ms_type"].str.split("-").str[0]
    baseline["activity"] = baseline["ms_type"].str.split("-").str[1]
    assert len(baseline) == 15
    assert baseline["subtype"].value_counts().to_dict() == {"RRMS": 10, "SPMS": 5}

    activity = (
        pd.crosstab(baseline["subtype"], baseline["activity"])
        .reindex(index=["RRMS", "SPMS"], columns=["a", "s"], fill_value=0)
        .astype(int)
    )
    sex = (
        pd.crosstab(baseline["subtype"], baseline["sex"])
        .reindex(index=["RRMS", "SPMS"], columns=["F", "M"], fill_value=0)
        .astype(int)
    )
    activity_or, activity_p = fisher_exact(activity.to_numpy(), alternative="two-sided")
    sex_or, sex_p = fisher_exact(sex.to_numpy(), alternative="two-sided")

    confounding_rows = []
    for variable, table, odds_ratio, p_value in [
        ("activity", activity, activity_or, activity_p),
        ("sex", sex, sex_or, sex_p),
    ]:
        for subtype in table.index:
            for level in table.columns:
                confounding_rows.append(
                    {
                        "variable": variable,
                        "subtype": subtype,
                        "level": level,
                        "count": int(table.loc[subtype, level]),
                        "two_sided_fisher_odds_ratio": float(odds_ratio),
                        "two_sided_fisher_p": float(p_value),
                    }
                )
    confounding = pd.DataFrame(confounding_rows)
    confounding.to_csv(OUT / "gse228330_baseline_confounding.tsv", sep="\t", index=False)

    rows = [
        evidence_row(
            dataset="Macnair discovery microglia",
            compartment="CNS postmortem microglia",
            artifact=str(stage_summary_path),
            n_units=44,
            phenotype="PPMS versus SPMS, source/tissue-overlap restricted",
            minimum_group_n=20,
            verified_subject_map=True,
            processed_expression_held=True,
            frozen_module_coverage=True,
            source_batch_control="adequate",
            activity_treatment_control="unavailable",
            composition_control="partial",
            matched_cross_compartment_phenotype=False,
            repeated_disability_or_conversion=False,
            observed_result="no module passed the portable cross-sectional stage gate",
            blocker=(
                "no peripheral PPMS-versus-SPMS counterpart; postmortem stage has no "
                "disability trajectory and treatment/activity metadata are unavailable"
            ),
        ),
        evidence_row(
            dataset="GSE180759 plus GSE279972",
            compartment="CNS postmortem lesion tissue",
            artifact=f"{lesion_summary_path};{panel_summary_path}",
            n_units=24,
            phenotype="chronic-active edge and foamy morphology pathology contexts",
            minimum_group_n=3,
            verified_subject_map=True,
            processed_expression_held=True,
            frozen_module_coverage=True,
            source_batch_control="partial",
            activity_treatment_control="unavailable",
            composition_control="adequate",
            matched_cross_compartment_phenotype=False,
            repeated_disability_or_conversion=False,
            observed_result="no module passed either frozen orthogonal-context gate",
            blocker=(
                "pathology phenotypes have no peripheral analogue, only three paired "
                "active/inactive donors, and no clinical progression outcome"
            ),
        ),
        evidence_row(
            dataset="GSE228330 baseline",
            compartment="peripheral PBMC",
            artifact=str(gse228_path),
            n_units=len(baseline),
            phenotype="RRMS versus SPMS at nominal pretreatment baseline",
            minimum_group_n=int(baseline["subtype"].value_counts().min()),
            verified_subject_map=False,
            processed_expression_held=False,
            frozen_module_coverage=False,
            source_batch_control="unavailable",
            activity_treatment_control="confounded",
            composition_control="unavailable",
            matched_cross_compartment_phenotype=False,
            repeated_disability_or_conversion=False,
            observed_result="not tested because the frozen eligibility gate fails",
            blocker=(
                "SPMS n=5; subtype is associated with activity suffix; subject map, "
                "processed expression, batch, age, cell composition, and disability are absent"
            ),
        ),
        evidence_row(
            dataset="GSE24427",
            compartment="peripheral whole blood",
            artifact=(
                "analysis/tier_0_triage/hyp_v6_006_gse24427_ms_ifnb_longitudinal/"
                "sample_metadata.tsv"
            ),
            n_units=25,
            phenotype="treated relapsing MS pharmacodynamics and relapse follow-up",
            minimum_group_n=0,
            verified_subject_map=True,
            processed_expression_held=True,
            frozen_module_coverage=True,
            source_batch_control="partial",
            activity_treatment_control="adequate",
            composition_control="unavailable",
            matched_cross_compartment_phenotype=False,
            repeated_disability_or_conversion=False,
            observed_result="ineligible phenotype; no progression-stage comparison run",
            blocker=(
                "no progressive subtype contrast, repeated EDSS, conversion event, or "
                "matched CNS treatment context"
            ),
        ),
    ]
    evidence = pd.DataFrame(rows)
    evidence.to_csv(OUT / "compartment_evidence_matrix.tsv", sep="\t", index=False)

    requirement_rows = []
    requirements = [
        ("same clinical contrast in CNS and periphery", False, "no compatible compartment pair"),
        ("at least 10 verified subjects per stage per compartment", False, "peripheral SPMS n=5"),
        ("verified sample-to-subject maps", False, "GSE228330 public map unverified"),
        ("processed expression and frozen-module coverage", False, "not held for GSE228330"),
        ("source/batch plus activity/treatment control", False, "GSE228330 batch absent and activity confounded"),
        ("measured or pre-specified cell-composition control", False, "peripheral composition unavailable"),
        ("formal compartment-by-stage contrast", False, "no eligible matched design"),
        ("repeated disability or adjudicated conversion", False, "absent from all candidate pairs"),
    ]
    for requirement, passed, reason in requirements:
        requirement_rows.append(
            {"requirement": requirement, "passed": yn(passed), "reason": reason}
        )
    pd.DataFrame(requirement_rows).to_csv(
        OUT / "eligibility_requirements.tsv", sep="\t", index=False
    )

    n_cross = int((evidence["cross_sectional_separation_eligible"] == "yes").sum())
    n_progression = int((evidence["progression_separation_eligible"] == "yes").sum())
    assert n_cross == n_progression == 0
    assert activity_p < 0.05

    summary = {
        "purpose": "CNS-versus-peripheral progression-state identifiability audit",
        "n_candidate_compartment_resources": len(evidence),
        "n_cross_sectional_separation_eligible": n_cross,
        "n_progression_separation_eligible": n_progression,
        "gse228330_baseline_n": len(baseline),
        "gse228330_rrms_n": int((baseline["subtype"] == "RRMS").sum()),
        "gse228330_spms_n": int((baseline["subtype"] == "SPMS").sum()),
        "gse228330_subtype_activity_fisher_odds_ratio": float(activity_or),
        "gse228330_subtype_activity_fisher_p": float(activity_p),
        "gse228330_subtype_sex_fisher_odds_ratio": float(sex_or),
        "gse228330_subtype_sex_fisher_p": float(sex_p),
        "verdict": "CNS_VS_PERIPHERAL_PROGRESSION_LOCALIZATION_NOT_IDENTIFIABLE",
        "boundary": (
            "Coverage/design failure, not a biological null. No CNS-intrinsic, "
            "peripheral-null, shared-state, causal, or therapeutic inference is permitted."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = f"""# V54 CNS-Versus-Peripheral Progression Identifiability Audit

## Verdict

**CNS-versus-peripheral progression localization is not identifiable in the
held corpus.** Zero of {len(evidence)} candidate compartment resources forms an
eligible cross-compartment pair, and zero can test progression localization.
This is a design/coverage boundary, not a biological null.

## Peripheral Candidate Audit

GSE228330 provides {len(baseline)} nominal baseline PBMC samples: 10 RRMS and 5
SPMS. The deposited activity suffix is imbalanced by subtype (RRMS: 1 active, 9
stable; SPMS: 4 active, 1 stable; two-sided Fisher OR `{activity_or:.5g}`,
`p={activity_p:.6g}`). Sex imbalance is not statistically resolved in this tiny
sample (Fisher OR `{sex_or:.5g}`, `p={sex_p:.6g}`). More decisively, the public
subject map is unverified and processed expression, batch, age, measured cell
composition, and disability trajectory are not held. The peripheral comparison
therefore fails before expression scoring.

Downloading and processing the public arrays would not repair the phenotype
mismatch or missing design fields. No RRMS-versus-SPMS PBMC module test was run,
so this audit does not report a peripheral null.

## CNS Candidate Audit

The source-restricted Macnair brain analysis had 44 PPMS/SPMS donors, but no
module passed its frozen portable stage gate and no compatible peripheral
PPMS-versus-SPMS cohort exists. The two lesion resources encode pathology
contexts rather than clinical stage and produced no orthogonally supported
module. Neither resource has longitudinal disability.

These brain results cannot be labeled CNS-intrinsic merely because the corpus
lacks an eligible peripheral counterpart. A formal localization claim requires
the matched design specified in the frozen plan.

## Required Data

The minimum cross-sectional design is a common PPMS-versus-SPMS (or a common
longitudinal progression-outcome) contrast in CNS/CSF and blood, at least 10
verified subjects per group per compartment, processed expression with the
frozen modules, source/batch and activity/treatment control, cell-composition
measurement, and a formal compartment interaction. A claim about halting
progression additionally requires repeated disability or adjudicated conversion.

Machine-readable artifacts:

- `compartment_evidence_matrix.tsv`
- `gse228330_baseline_confounding.tsv`
- `eligibility_requirements.tsv`
- `summary.json`
"""
    (OUT / "REPORT.md").write_text(report)


if __name__ == "__main__":
    main()
