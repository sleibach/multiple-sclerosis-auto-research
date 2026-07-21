#!/usr/bin/env python3
"""Inventory held data that can and cannot answer progression questions.

This is a semantic and coverage audit. It does not test biological hypotheses.
Counts are recomputed from committed metadata/results, and every row records the
artifact that supports its eligibility boundary.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_data_inventory"


def require(path: str) -> Path:
    resolved = ROOT / path
    if not resolved.is_file():
        raise FileNotFoundError(resolved)
    return resolved


def compact_counts(series: pd.Series) -> str:
    counts = series.astype(str).value_counts().sort_index()
    return ";".join(f"{key}:{int(value)}" for key, value in counts.items())


def add_row(rows: list[dict[str, object]], **kwargs: object) -> None:
    rows.append(kwargs)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []

    discovery_path = require(
        "analysis/v53_ms_microglia_independent_cohort_scout/"
        "macnair_discovery/donor_scores.tsv"
    )
    discovery = pd.read_csv(discovery_path, sep="\t")
    source_path = require(
        "analysis/v53_macnair_source_influence/discovery_donor_source_map.tsv"
    )
    source = pd.read_csv(source_path, sep="\t")
    discovery = discovery.merge(source, on="canonical_donor", validate="one_to_one")
    discovery_source_stage = (
        discovery.groupby(["source_family", "diagnosis"], observed=True)
        .size()
        .rename("n_donors")
        .reset_index()
    )
    discovery_source_stage.to_csv(
        OUT / "macnair_discovery_source_stage_counts.tsv", sep="\t", index=False
    )
    overlapping_sources = sorted(
        set(discovery.loc[discovery.diagnosis.eq("PPMS"), "source_family"])
        & set(discovery.loc[discovery.diagnosis.eq("SPMS"), "source_family"])
    )
    overlap = discovery[
        discovery.source_family.isin(overlapping_sources)
        & discovery.diagnosis.isin(["PPMS", "SPMS"])
    ]
    add_row(
        rows,
        dataset="Macnair discovery / Zenodo 8338963",
        material="postmortem brain microglia pseudobulk",
        n_units=len(discovery),
        n_donors=discovery.canonical_donor.nunique(),
        progression_labels=compact_counts(discovery.diagnosis),
        source_structure=";".join(overlapping_sources),
        longitudinal="no",
        direct_disability_outcome="no",
        source_auditable="yes",
        eligible_now=(
            "cross-sectional PPMS-vs-SPMS module comparison restricted to "
            f"overlapping sources ({compact_counts(overlap.diagnosis)})"
        ),
        not_identifiable="RRMS transition; progression rate; disability accumulation",
        status="eligible_with_source_restriction",
        artifact=str(discovery_path.relative_to(ROOT)),
    )

    validation_path = require(
        "analysis/v53_ms_microglia_independent_cohort_scout/"
        "macnair_validation/donor_scores.tsv"
    )
    validation = pd.read_csv(validation_path, sep="\t")
    add_row(
        rows,
        dataset="Macnair validation / Zenodo 8338963",
        material="postmortem brain microglia pseudobulk",
        n_units=len(validation),
        n_donors=validation.canonical_donor.nunique(),
        progression_labels=compact_counts(validation.diagnosis),
        source_structure=compact_counts(validation.study),
        longitudinal="no",
        direct_disability_outcome="no",
        source_auditable="yes",
        eligible_now="SPMS-vs-control state sensitivity by source",
        not_identifiable="PPMS-vs-SPMS with adequate PPMS n; RRMS transition; progression rate",
        status="supportive_only_ppms_n_2",
        artifact=str(validation_path.relative_to(ROOT)),
    )

    lesion_path = require("data/raw/GSE180759_annotation.txt.gz")
    lesion = pd.read_csv(lesion_path, sep="\t")
    lesion_counts = (
        lesion.groupby(["NBB_case", "pathology", "cell_type"], observed=True)
        .size()
        .rename("n_nuclei")
        .reset_index()
    )
    lesion_counts.to_csv(OUT / "gse180759_donor_pathology_counts.tsv", sep="\t", index=False)
    add_row(
        rows,
        dataset="GSE180759",
        material="postmortem lesion single-nucleus RNA-seq",
        n_units=len(lesion),
        n_donors=lesion.NBB_case.nunique(),
        progression_labels=compact_counts(lesion.pathology),
        source_structure="single deposited study; donor ID available",
        longitudinal="no",
        direct_disability_outcome="no",
        source_auditable="donor only; no acquisition-site field",
        eligible_now="paired donor chronic-active-vs-inactive/periplaque lesion-state tests",
        not_identifiable="clinical progression; RRMS-to-SPMS transition; treatment effect",
        status="eligible_lesion_proxy_small_donor_n",
        artifact=str(lesion_path.relative_to(ROOT)),
    )

    bulk_path = require("data/derived/gse279972_sample_metadata.tsv")
    bulk = pd.read_csv(bulk_path, sep="\t")
    add_row(
        rows,
        dataset="GSE279972",
        material="postmortem white-matter bulk RNA-seq",
        n_units=len(bulk),
        n_donors=bulk.donor.nunique(),
        progression_labels=compact_counts(bulk.lesion_type),
        source_structure="donor available; source/site not available in analysis table",
        longitudinal="no",
        direct_disability_outcome="no",
        source_auditable="donor and morphology; no clinical-stage label",
        eligible_now="donor-aware lesion/morphology association and exclusion tests",
        not_identifiable="progressive subtype; progression rate; causal lesion transition",
        status="eligible_lesion_proxy_no_stage",
        artifact=str(bulk_path.relative_to(ROOT)),
    )

    treatment_path = require(
        "analysis/v45_gse228330_outcome_scout/gse228330_sample_metadata.tsv"
    )
    treatment = pd.read_csv(treatment_path, sep="\t")
    add_row(
        rows,
        dataset="GSE228330",
        material="PBMC ocrelizumab pharmacodynamic microarray",
        n_units=len(treatment),
        n_donors="unverified public sample-to-subject map",
        progression_labels=compact_counts(treatment.ms_type),
        source_structure="single cohort; samples randomized; batch labels unavailable",
        longitudinal="nominal baseline/week2/month6; public pairing unverified",
        direct_disability_outcome="no",
        source_auditable="no subject map and no response/disability labels",
        eligible_now="metadata feasibility and unpaired pharmacodynamic context only",
        not_identifiable="paired subtype response; progression slowing; clinical benefit",
        status="blocked_for_progression_inference",
        artifact=str(treatment_path.relative_to(ROOT)),
    )

    lineage_path = require(
        "analysis/v53_microglia_source_lineage_audit/donor_lineage_manifest.tsv"
    )
    lineage = pd.read_csv(lineage_path, sep="\t")
    gse111972 = lineage[lineage.cohort.eq("gse111972")]
    add_row(
        rows,
        dataset="GSE111972",
        material="sorted white/grey-matter microglia expression",
        n_units=len(gse111972),
        n_donors=gse111972.donor_id.nunique(),
        progression_labels=compact_counts(gse111972.disease_group),
        source_structure="single GEO study",
        longitudinal="no",
        direct_disability_outcome="no",
        source_auditable="single source; age/sex/region available",
        eligible_now="MS-vs-control microglial state association",
        not_identifiable="progressive subtype; lesion rim; progression rate",
        status="not_progression_specific",
        artifact=str(lineage_path.relative_to(ROOT)),
    )

    gse301908_path = require(
        "analysis/v53_microglia_source_lineage_audit/gse301908_donor_manifest.tsv"
    )
    gse301908 = pd.read_csv(gse301908_path, sep="\t")
    diagnosis_col = "diagnosis" if "diagnosis" in gse301908.columns else "disease"
    donor_col = next(
        column
        for column in ["canonical_donor", "donor", "donor_id"]
        if column in gse301908.columns
    )
    add_row(
        rows,
        dataset="GSE301908",
        material="single-nucleus brain microglia sensitivity cohort",
        n_units=len(gse301908),
        n_donors=gse301908[donor_col].nunique(),
        progression_labels=compact_counts(gse301908[diagnosis_col]),
        source_structure="single GEO study; only three controls",
        longitudinal="no",
        direct_disability_outcome="no",
        source_auditable="limited; normalized layer only",
        eligible_now="low-control MS state sensitivity only",
        not_identifiable="progressive subtype; progression rate; robust replication",
        status="not_progression_specific_low_control_n",
        artifact=str(gse301908_path.relative_to(ROOT)),
    )

    inventory = pd.DataFrame(rows)
    inventory.to_csv(OUT / "progression_data_inventory.tsv", sep="\t", index=False)

    questions = pd.DataFrame(
        [
            {
                "question": "Does a molecular state predict longitudinal disability accumulation?",
                "status": "blocked",
                "reason": "No held transcriptomic cohort has repeated disability outcomes.",
            },
            {
                "question": "Does a state differ between PPMS and SPMS?",
                "status": "testable_cross_sectionally",
                "reason": "Macnair discovery has both stages in Amsterdam and UK sources; this is not transition or progression-rate evidence.",
            },
            {
                "question": "Does a state distinguish RRMS from progressive MS?",
                "status": "blocked",
                "reason": "Only two RRMS donors occur in the usable brain package and no validation RRMS donors are present.",
            },
            {
                "question": "Is a state enriched at chronic-active lesion edges?",
                "status": "testable_small_n_proxy",
                "reason": "GSE180759 has donor/pathology labels, but only three donors contribute chronic-active immune nuclei and paired contrasts are sparse.",
            },
            {
                "question": "Does treatment slow progression through a measured state?",
                "status": "blocked",
                "reason": "GSE228330 lacks a verified subject map and disability/response outcomes; other held treatment cohorts are relapse/response focused.",
            },
            {
                "question": "Can cross-sectional subtype labels identify RRMS-to-SPMS transition?",
                "status": "not_identifiable",
                "reason": "No; transition requires longitudinal within-person stage/outcome data.",
            },
        ]
    )
    questions.to_csv(OUT / "progression_question_semantic_contract.tsv", sep="\t", index=False)

    summary = {
        "purpose": "Progression-data coverage and semantic eligibility audit; no biological claim",
        "n_datasets_inventory": len(inventory),
        "n_questions": len(questions),
        "n_questions_directly_testable": int(questions.status.str.startswith("testable").sum()),
        "n_questions_blocked_or_not_identifiable": int(
            questions.status.isin(["blocked", "not_identifiable"]).sum()
        ),
        "highest_value_executable_test": (
            "Source-overlap-restricted, cross-sectional PPMS-vs-SPMS module "
            "comparison in Macnair discovery"
        ),
        "critical_boundary": (
            "No held dataset measures longitudinal disability accumulation; "
            "cross-sectional stage and lesion-state tests cannot establish halted progression."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    report = [
        "# V54 Progression Data Inventory",
        "",
        "Status: **coverage audit complete; no biological result**.",
        "",
        "The held corpus supports two bounded progression-adjacent questions: a",
        "cross-sectional PPMS-versus-SPMS comparison within overlapping brain-bank",
        "sources, and small-donor chronic-active lesion-state tests. It contains no",
        "transcriptomic cohort with repeated disability outcomes, and therefore cannot",
        "test whether a molecular state predicts or halts disability accumulation.",
        "",
        "The first executable test is the Macnair discovery PPMS-versus-SPMS",
        "comparison restricted to Amsterdam and UK sources. It is a disease-stage",
        "association test only, not evidence about transition, rate, causality, or",
        "treatment benefit.",
        "",
        "Machine-readable inventory: `progression_data_inventory.tsv`.",
        "Semantic contract: `progression_question_semantic_contract.tsv`.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
