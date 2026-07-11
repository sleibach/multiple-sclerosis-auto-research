#!/usr/bin/env python3
"""Audit source, package, and donor-label overlap for V53 microglia cohorts."""

from __future__ import annotations

import json
import re
import subprocess
from itertools import combinations
from pathlib import Path

import pandas as pd

import v3_analyze_gse111972_microglia as gse111972


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v53_microglia_source_lineage_audit"
MACNAIR = ROOT / "analysis/v53_ms_microglia_independent_cohort_scout"
GSE301908_RDS = ROOT / "data/raw/GSE301908_sn_all.rds"

VALIDATION_STUDIES = {
    "a2021": "Absinta et al. 2021",
    "j2019": "Jaekel et al. 2019",
    "s2019": "Schirmer et al. 2019",
    "roche": "new validation samples in the Macnair package",
}


def normalized_token(value: object) -> str:
    return re.sub(r"\s+", "", str(value).strip().lower())


def disease_group(value: object) -> str:
    return "MS" if str(value).upper() not in {"CONTROL", "CTR", "CTRL"} else "control"


def prepare_gse301908() -> pd.DataFrame:
    output = OUT / "gse301908_donor_manifest.tsv"
    subprocess.run(
        [
            "Rscript",
            str(ROOT / "scripts/v53_export_gse301908_donor_manifest.R"),
            str(GSE301908_RDS),
            str(output),
        ],
        check=True,
    )
    frame = pd.read_csv(output, sep="\t")
    frame["disease_group"] = frame["diagnosis"].map(disease_group)
    return frame


def cohort_frames() -> dict[str, pd.DataFrame]:
    gse = gse111972.load_sample_metadata()
    gse = (
        gse.groupby("patient", as_index=False)
        .agg(
            diagnosis=("disease", "first"),
            disease_group=("disease", "first"),
            age=("age", "first"),
            sex_male=("sex_male", "first"),
            n_samples=("sample", "nunique"),
        )
        .rename(columns={"patient": "donor_id"})
    )
    gse["disease_group"] = gse["disease_group"].map(disease_group)
    gse["study"] = "GSE111972"

    discovery = pd.read_csv(MACNAIR / "macnair_discovery/donor_scores.tsv", sep="\t")
    discovery = discovery.rename(columns={"canonical_donor": "donor_id"})
    discovery["disease_group"] = discovery["diagnosis"].map(disease_group)
    discovery["age"] = discovery["age_at_death"]
    discovery["sex_male"] = discovery["sex"].eq("M").astype(int)

    validation = pd.read_csv(MACNAIR / "macnair_validation/donor_scores.tsv", sep="\t")
    validation = validation.rename(columns={"canonical_donor": "donor_id"})
    validation["disease_group"] = validation["diagnosis"].map(disease_group)
    validation["age"] = validation["age_at_death"]
    validation["sex_male"] = validation["sex"].eq("M").astype(int)

    gse301908 = prepare_gse301908()
    gse301908["study"] = "GSE301908"
    gse301908["age"] = pd.NA
    gse301908["sex_male"] = pd.NA
    gse301908["n_samples"] = 1

    return {
        "gse111972": gse,
        "macnair_discovery": discovery,
        "macnair_validation": validation,
        "gse301908": gse301908,
    }


def donor_manifest(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for cohort, frame in frames.items():
        for row in frame.itertuples(index=False):
            study = str(getattr(row, "study", cohort))
            if cohort == "macnair_validation":
                source_family = f"macnair_validation:{study}"
                publication_family = VALIDATION_STUDIES.get(study, study)
                package_family = "zenodo_8338963"
            elif cohort == "macnair_discovery":
                source_family = "macnair_discovery"
                publication_family = "Macnair et al. discovery cohort"
                package_family = "zenodo_8338963"
            elif cohort == "gse111972":
                source_family = "GSE111972"
                publication_family = "van der Poel et al. GSE111972"
                package_family = "GEO_GSE111972"
            else:
                source_family = "GSE301908"
                publication_family = "GSE301908 / GSE284005 companion study"
                package_family = "GEO_GSE301908"
            rows.append(
                {
                    "cohort": cohort,
                    "package_family": package_family,
                    "source_family": source_family,
                    "publication_family": publication_family,
                    "donor_id": str(row.donor_id),
                    "normalized_donor_token": normalized_token(row.donor_id),
                    "disease_group": str(row.disease_group),
                    "age": getattr(row, "age", pd.NA),
                    "sex_male": getattr(row, "sex_male", pd.NA),
                }
            )
    return pd.DataFrame(rows)


def overlap_pairs(manifest: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    cohorts = sorted(manifest["cohort"].unique())
    for left, right in combinations(cohorts, 2):
        a = manifest[manifest.cohort.eq(left)]
        b = manifest[manifest.cohort.eq(right)]
        token_overlap = sorted(set(a.normalized_donor_token) & set(b.normalized_donor_token))
        demographic_matches = 0
        if a["age"].notna().any() and b["age"].notna().any():
            aa = a.dropna(subset=["age", "sex_male"])
            bb = b.dropna(subset=["age", "sex_male"])
            merged = aa.merge(bb, on=["age", "sex_male", "disease_group"])
            demographic_matches = len(merged)
        same_package = bool(set(a.package_family) & set(b.package_family))
        rows.append(
            {
                "left_cohort": left,
                "right_cohort": right,
                "left_n_donors": len(a),
                "right_n_donors": len(b),
                "exact_normalized_token_overlap_n": len(token_overlap),
                "exact_normalized_token_overlap": ";".join(token_overlap),
                "exact_age_sex_disease_candidate_pairs": demographic_matches,
                "shared_deposition_package": same_package,
                "person_level_independence_verdict": (
                    "NOT_FULLY_VERIFIABLE_FROM_COHORT_SPECIFIC_ANONYMIZED_IDS"
                    if left.startswith("macnair") or right.startswith("macnair")
                    else "NO_TOKEN_OVERLAP_OBSERVED_IDENTIFIERS_NOT_GLOBAL"
                ),
            }
        )
    return pd.DataFrame(rows)


def validation_duplicates() -> pd.DataFrame:
    sample = pd.read_csv(MACNAIR / "macnair_validation/sample_metadata.tsv", sep="\t")
    sample["canonical_donor"] = sample["donor_id"].str.replace(r"^[^_]+_", "", regex=True)
    studies = (
        sample.groupby("canonical_donor")["study"]
        .agg(lambda values: ";".join(sorted(set(values))))
        .reset_index(name="source_studies")
    )
    studies["n_source_studies"] = studies["source_studies"].str.count(";") + 1
    return studies[studies.n_source_studies.gt(1)].reset_index(drop=True)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    frames = cohort_frames()
    manifest = donor_manifest(frames)
    pairs = overlap_pairs(manifest)
    duplicates = validation_duplicates()

    cohort_summary = (
        manifest.groupby(["cohort", "package_family"], as_index=False)
        .agg(
            n_donors=("donor_id", "nunique"),
            n_ms=("disease_group", lambda values: int((values == "MS").sum())),
            n_control=("disease_group", lambda values: int((values == "control").sum())),
            n_source_families=("source_family", "nunique"),
            source_families=("source_family", lambda values: ";".join(sorted(set(values)))),
        )
    )
    summary = {
        "purpose": "Source-lineage and donor-label audit; no biological hypothesis test",
        "n_cohorts": int(manifest.cohort.nunique()),
        "n_deposition_packages": int(manifest.package_family.nunique()),
        "n_exact_cross_cohort_donor_token_overlaps": int(
            pairs.exact_normalized_token_overlap_n.sum()
        ),
        "n_macnair_validation_cross_study_duplicate_donors_resolved": len(duplicates),
        "macnair_discovery_validation_share_deposition_package": True,
        "person_level_independence_fully_verifiable": False,
        "counting_rule": (
            "Treat GSE111972 and Zenodo 8338963 as separate package/source families. "
            "Treat the Macnair discovery and validation matrices as two deposited data "
            "partitions within one package, not two publication-independent replications. "
            "The validation partition contains three named source studies after deterministic "
            "within-partition donor de-duplication. Do not count GSE301908 as replication "
            "because it has only three controls and has not passed the frozen replication gate."
        ),
        "verdict": "NO_EXACT_TOKEN_OVERLAP_BUT_PERSON_LEVEL_INDEPENDENCE_NOT_FULLY_VERIFIABLE",
        "boundary": (
            "Cohort-specific anonymized identifiers cannot prove that no person appears in "
            "two source publications. Exact token non-overlap is a data-integrity check, not "
            "proof of biological independence."
        ),
    }

    manifest.to_csv(OUT / "donor_lineage_manifest.tsv", sep="\t", index=False)
    cohort_summary.to_csv(OUT / "cohort_lineage_summary.tsv", sep="\t", index=False)
    pairs.to_csv(OUT / "cross_cohort_overlap_checks.tsv", sep="\t", index=False)
    duplicates.to_csv(OUT / "macnair_validation_cross_study_duplicates.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    report = [
        "# V53 Microglia Source-Lineage Audit",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        "## What Is Independently Countable",
        "",
        "The original GSE111972 experiment and the Macnair Zenodo 8338963 package are",
        "separate deposition/source families. Within the Macnair package, discovery and",
        "validation are distinct deposited matrices with zero exact donor-token collisions,",
        "but they are not two publication-independent replications. The validation matrix",
        "itself combines Absinta 2021, Jaekel 2019, and Schirmer 2019 source studies.",
        "",
        f"The validation raw metadata contains `{len(duplicates)}` donor codes in more than",
        "one source study. The frozen analysis resolved these before outcome modeling using",
        "the pre-outcome microglial-yield rule. Across all cohort pairs, the audit found",
        f"`{summary['n_exact_cross_cohort_donor_token_overlaps']}` exact normalized donor-token",
        "collisions.",
        "",
        "## Limitation",
        "",
        "Cohort-specific anonymization prevents a proof of person-level non-overlap across",
        "publications. Age/sex/disease quasi-matches are reported only as ambiguity checks and",
        "must not be used to identify donors. Therefore the defensible wording is one",
        "independent Macnair package with two analyzed partitions and three named validation",
        "source studies, plus the separate original GSE111972 source family.",
        "",
        "GSE301908 is a separate GEO package and has zero exact donor-token collisions, but",
        "its three controls make it a sensitivity cohort only. It is not counted as a clean",
        "replication unless a pre-specified low-control analysis is explicitly reported as",
        "such.",
        "",
        "This audit changes replication-count wording only. It does not alter any cohort's",
        "within-cohort estimate or promote a mechanism or target.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
