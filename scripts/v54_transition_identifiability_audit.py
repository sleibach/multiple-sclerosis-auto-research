#!/usr/bin/env python3
"""Audit whether held MS datasets can identify progression transition."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_transition_identifiability"


def yes(value: bool) -> str:
    return "yes" if value else "no"


def row(
    *,
    dataset: str,
    artifact: str,
    modality: str,
    n_rows: int,
    n_subjects: str,
    verified_subject_map: str,
    repeated_molecular_measurements: str,
    repeated_transcriptome: bool,
    time_varying_ms_stage: bool,
    baseline_disability: bool,
    repeated_disability_or_conversion: bool,
    treatment_context_available: bool,
    n_observed_transition_events: int,
    safe_use: str,
    blocker: str,
) -> dict[str, Any]:
    eligible = all(
        [
            verified_subject_map == "yes",
            repeated_transcriptome,
            time_varying_ms_stage,
            repeated_disability_or_conversion,
            treatment_context_available,
            n_observed_transition_events > 0,
        ]
    )
    return {
        "dataset": dataset,
        "artifact": artifact,
        "modality": modality,
        "n_rows": n_rows,
        "n_subjects_or_donors": n_subjects,
        "verified_subject_map": verified_subject_map,
        "repeated_molecular_measurements": repeated_molecular_measurements,
        "repeated_transcriptome": yes(repeated_transcriptome),
        "time_varying_ms_stage": yes(time_varying_ms_stage),
        "baseline_disability": yes(baseline_disability),
        "repeated_disability_or_adjudicated_conversion": yes(repeated_disability_or_conversion),
        "treatment_context_available": yes(treatment_context_available),
        "n_observed_transition_events": n_observed_transition_events,
        "transition_identifiable": yes(eligible),
        "safe_bounded_use": safe_use,
        "blocking_field": blocker,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []

    macnair_path = Path(
        "analysis/v53_ms_microglia_independent_cohort_scout/macnair_discovery/donor_scores.tsv"
    )
    macnair = pd.read_csv(ROOT / macnair_path, sep="\t")
    assert len(macnair) == macnair.canonical_donor.nunique() == 80
    rows.append(
        row(
            dataset="Macnair discovery microglia",
            artifact=str(macnair_path),
            modality="postmortem brain microglia pseudobulk",
            n_rows=len(macnair),
            n_subjects=str(macnair.canonical_donor.nunique()),
            verified_subject_map="yes",
            repeated_molecular_measurements=(
                f"same-death contexts; {int((macnair.n_samples > 1).sum())} donors have >1 source sample"
            ),
            repeated_transcriptome=False,
            time_varying_ms_stage=False,
            baseline_disability=False,
            repeated_disability_or_conversion=False,
            treatment_context_available=False,
            n_observed_transition_events=0,
            safe_use="source-restricted cross-sectional subtype association",
            blocker="one postmortem timepoint per donor; no disability trajectory or conversion event",
        )
    )

    gse180_path = Path("data/raw/GSE180759_annotation.txt.gz")
    gse180 = pd.read_csv(ROOT / gse180_path, sep="\t")
    assert len(gse180) == 66_432
    rows.append(
        row(
            dataset="GSE180759",
            artifact=str(gse180_path),
            modality="postmortem lesion single-nucleus RNA-seq",
            n_rows=len(gse180),
            n_subjects=str(gse180.NBB_case.nunique()),
            verified_subject_map="yes",
            repeated_molecular_measurements="same-death pathology contexts, not longitudinal timepoints",
            repeated_transcriptome=False,
            time_varying_ms_stage=False,
            baseline_disability=False,
            repeated_disability_or_conversion=False,
            treatment_context_available=False,
            n_observed_transition_events=0,
            safe_use="donor-aware lesion-state association",
            blocker="postmortem pathology repeats do not observe clinical transition",
        )
    )

    gse279_path = Path("data/derived/gse279972_sample_metadata.tsv")
    gse279 = pd.read_csv(ROOT / gse279_path, sep="\t")
    assert len(gse279) == 109 and gse279.donor.nunique() == 38
    rows.append(
        row(
            dataset="GSE279972",
            artifact=str(gse279_path),
            modality="postmortem lesion bulk RNA-seq",
            n_rows=len(gse279),
            n_subjects=str(gse279.donor.nunique()),
            verified_subject_map="yes",
            repeated_molecular_measurements="same-death lesion and morphology samples",
            repeated_transcriptome=False,
            time_varying_ms_stage=False,
            baseline_disability=False,
            repeated_disability_or_conversion=False,
            treatment_context_available=False,
            n_observed_transition_events=0,
            safe_use="donor-aware lesion/morphology association",
            blocker="no longitudinal time, subtype trajectory, disability, or treatment context",
        )
    )

    gse228_path = Path("analysis/v45_gse228330_outcome_scout/gse228330_sample_metadata.tsv")
    gse228 = pd.read_csv(ROOT / gse228_path, sep="\t")
    assert len(gse228) == 44
    assert set(gse228.treatment_duration_month.unique()) == {0.0, 0.5, 6.0}
    rows.append(
        row(
            dataset="GSE228330",
            artifact=str(gse228_path),
            modality="PBMC ocrelizumab pharmacodynamic microarray",
            n_rows=len(gse228),
            n_subjects="unverified (15 reported patients)",
            verified_subject_map="no",
            repeated_molecular_measurements="nominal baseline/week-2/month-6; public pairing unavailable",
            repeated_transcriptome=False,
            time_varying_ms_stage=False,
            baseline_disability=False,
            repeated_disability_or_conversion=False,
            treatment_context_available=True,
            n_observed_transition_events=0,
            safe_use="unpaired pharmacodynamic context after platform processing",
            blocker="no public subject map, repeated disability, response label, or transition event",
        )
    )

    gse244_path = Path(
        "analysis/tier_0_triage/hyp_v6_006_gse24427_ms_ifnb_longitudinal/sample_metadata.tsv"
    )
    gse244 = pd.read_csv(ROOT / gse244_path, sep="\t")
    unique_visits = gse244[["patient", "timepoint"]].drop_duplicates()
    n_repeated = int((unique_visits.groupby("patient").size() > 1).sum())
    assert gse244.patient.nunique() == n_repeated == 25
    assert gse244.edss_baseline.notna().all()
    rows.append(
        row(
            dataset="GSE24427",
            artifact=str(gse244_path),
            modality="longitudinal IFN-beta blood microarray",
            n_rows=len(gse244),
            n_subjects=str(gse244.patient.nunique()),
            verified_subject_map="yes",
            repeated_molecular_measurements=f"{n_repeated} subjects with >1 verified transcriptomic timepoint",
            repeated_transcriptome=True,
            time_varying_ms_stage=False,
            baseline_disability=True,
            repeated_disability_or_conversion=False,
            treatment_context_available=True,
            n_observed_transition_events=0,
            safe_use="IFN-beta pharmacodynamics and two-year relapse outcome",
            blocker="EDSS is baseline-only; relapse follow-up is not disability progression or subtype conversion",
        )
    )

    gse174_path = Path("data/derived/GSE17410/sample_metadata.tsv")
    gse174 = pd.read_csv(ROOT / gse174_path, sep="\t")
    titles = gse174.Sample_title.astype(str)
    pre_codes = {
        re.match(r"([A-Za-z]+)1\b", title).group(1)
        for title in titles
        if re.match(r"([A-Za-z]+)1\b", title)
    }
    month9_codes = {
        re.match(r"([A-Za-z]+)4\b", title).group(1)
        for title in titles
        if re.match(r"([A-Za-z]+)4\b", title)
    }
    obvious_pairs = sorted(pre_codes & month9_codes)
    assert len(gse174) == 17 and len(obvious_pairs) == 5
    rows.append(
        row(
            dataset="GSE17410",
            artifact=str(gse174_path),
            modality="MS pregnancy PBMC microarray",
            n_rows=len(gse174),
            n_subjects="partial title-derived mapping",
            verified_subject_map="partial",
            repeated_molecular_measurements=f"5 unambiguous title-code pre/month-9 pairs ({';'.join(obvious_pairs)})",
            repeated_transcriptome=True,
            time_varying_ms_stage=False,
            baseline_disability=False,
            repeated_disability_or_conversion=False,
            treatment_context_available=True,
            n_observed_transition_events=0,
            safe_use="pregnancy-state natural-experiment context",
            blocker="pregnancy time is not MS subtype transition; no repeated disability or conversion event",
        )
    )

    microbiome_path = Path(
        "analysis/v9_microbiome/ms_phyloseq_export/ms_before_after_stool_metadata.tsv"
    )
    microbiome = pd.read_csv(ROOT / microbiome_path, sep="\t")
    n_people = microbiome.SampleNr.nunique()
    n_repeated_microbiome = int((microbiome.groupby("SampleNr").TimePoint.nunique() > 1).sum())
    assert len(microbiome) == 95
    rows.append(
        row(
            dataset="Held pre/post-ocrelizumab MS microbiome",
            artifact=str(microbiome_path),
            modality="stool 16S microbiome",
            n_rows=len(microbiome),
            n_subjects=str(n_people),
            verified_subject_map="yes",
            repeated_molecular_measurements=f"{n_repeated_microbiome} subjects have >1 stool timepoint",
            repeated_transcriptome=False,
            time_varying_ms_stage=False,
            baseline_disability=False,
            repeated_disability_or_conversion=False,
            treatment_context_available=True,
            n_observed_transition_events=0,
            safe_use="treatment-associated microbiome context",
            blocker="wrong molecular modality and no subtype/disability trajectory",
        )
    )

    audit = pd.DataFrame(rows)
    audit.to_csv(OUT / "transition_identifiability.tsv", sep="\t", index=False)
    eligible = audit.transition_identifiable.eq("yes")
    if eligible.any():
        raise RuntimeError("Unexpected eligible dataset; freeze a separate analysis before testing")

    requirements = [
        {
            "requirement": "verified subject identifier",
            "n_datasets_meeting": int(audit.verified_subject_map.eq("yes").sum()),
        },
        {
            "requirement": "repeated transcriptome",
            "n_datasets_meeting": int(audit.repeated_transcriptome.eq("yes").sum()),
        },
        {
            "requirement": "time-varying MS stage or conversion",
            "n_datasets_meeting": int(audit.time_varying_ms_stage.eq("yes").sum()),
        },
        {
            "requirement": "repeated disability or adjudicated conversion",
            "n_datasets_meeting": int(
                audit.repeated_disability_or_adjudicated_conversion.eq("yes").sum()
            ),
        },
        {
            "requirement": "treatment context",
            "n_datasets_meeting": int(audit.treatment_context_available.eq("yes").sum()),
        },
    ]
    pd.DataFrame(requirements).to_csv(OUT / "requirement_coverage.tsv", sep="\t", index=False)
    summary = {
        "purpose": "Held-data transition identifiability audit; no biological claim",
        "n_datasets_audited": len(audit),
        "n_transition_identifiable": int(eligible.sum()),
        "n_with_verified_subject_map": int(audit.verified_subject_map.eq("yes").sum()),
        "n_with_repeated_transcriptome": int(audit.repeated_transcriptome.eq("yes").sum()),
        "n_with_time_varying_stage": int(audit.time_varying_ms_stage.eq("yes").sum()),
        "n_with_repeated_disability_or_conversion": int(
            audit.repeated_disability_or_adjudicated_conversion.eq("yes").sum()
        ),
        "verdict": "RRMS_TO_PROGRESSIVE_TRANSITION_NOT_IDENTIFIABLE_IN_HELD_CORPUS",
        "boundary": "This is a data-semantics boundary, not evidence that no transition biology exists.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V54 Progression Transition Identifiability Audit",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        "Seven held progression-adjacent or longitudinal MS datasets were checked",
        "against the five-field frozen contract. None links repeated transcriptomes",
        "to time-varying MS stage and repeated disability or an adjudicated conversion",
        "event. No transition-association test is therefore permitted.",
        "",
        "The nearest longitudinal transcriptomic dataset is GSE24427: 25 subjects",
        "have verified repeated blood measurements, baseline EDSS, and two-year relapse",
        "outcomes during IFN-beta treatment. EDSS is not repeated, no subtype conversion",
        "is observed, and relapse is not a substitute for disability progression.",
        "",
        "| dataset | repeated transcriptome | time-varying stage | repeated disability/conversion | verdict |",
        "|---|---:|---:|---:|---|",
    ]
    for item in rows:
        report.append(
            "| {dataset} | {repeated_transcriptome} | {time_varying_ms_stage} | "
            "{repeated_disability_or_adjudicated_conversion} | {transition_identifiable} |".format(
                **item
            )
        )
    report.extend(
        [
            "",
            "This fail-closed verdict prevents postmortem context, pharmacodynamic",
            "time, relapse follow-up, pregnancy, or microbiome change from being called",
            "an RRMS-to-progressive transition. It does not establish a biological null.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
