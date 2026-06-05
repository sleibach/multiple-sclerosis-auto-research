#!/usr/bin/env python3
"""Build V8 genetics-axis evidence from local and verified public sources.

The default layer is a first-pass target/locus overlap using existing V3
OpenTargets pulls. Where a verified LDSC-style genetic-correlation result is
available, it overrides the proxy placement for that disease.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v8_map"
RAW = ROOT / "results_v3" / "wave55_external_genetics_druggability_sweep" / "opentargets_associated_targets_raw.tsv"

DISEASE_LABELS = {
    "RA": "rheumatoid arthritis",
    "Crohn": "Crohn disease",
    "UC": "ulcerative colitis",
    "SLE": "systemic lupus erythematosus",
    "Psoriasis": "psoriasis",
    "T1D": "type 1 diabetes mellitus",
    "Sjogren": "Sjogren syndrome",
    "AITD": "autoimmune thyroid disease",
    "Celiac": "celiac disease",
    "AS": "ankylosing spondylitis",
    "PBC": "primary biliary cholangitis",
}

TARGET_DISEASES = [
    "rheumatoid arthritis",
    "Crohn disease",
    "ulcerative colitis",
    "systemic lupus erythematosus",
    "psoriasis",
    "type 1 diabetes mellitus",
    "Sjogren syndrome",
    "Hashimoto thyroiditis",
    "Graves disease",
    "celiac disease",
    "myasthenia gravis",
    "ankylosing spondylitis",
]

LITERATURE_OVERRIDES = {
    "Crohn disease": {
        "evidence_id": "V8_axis_02_genetics_Crohn_LDSC_Yang2021",
        "placement": "intermediate",
        "grade": "supported",
        "confidence": "medium",
        "dataset_or_source": "Yang et al. Nat Commun 2021; doi:10.1038/s41467-021-25768-0",
        "effect_direction": "MS-CD rg=0.16; MS-IBD rg=0.28",
        "statistic": "LDSC cross-trait genetic correlation; SMR/TWAS also performed in source study",
        "p_value": "source reports significant MS-IBD and weaker MS-CD than MS-UC",
        "fdr_or_correction": "source-level LDSC/FDR; matrix placement pre-specified in MAP_METHODOLOGY_V8",
        "sample_size": "summary statistics: MS=47,429; IBD=59,957; CD=40,266; UC=45,975 in source",
        "file_or_url": "https://www.nature.com/articles/s41467-021-25768-0",
        "notes": "Verified LDSC source reports weaker MS-CD genetic correlation than MS-UC; placement is intermediate, not near.",
    },
    "ulcerative colitis": {
        "evidence_id": "V8_axis_02_genetics_UC_LDSC_Yang2021",
        "placement": "near",
        "grade": "supported",
        "confidence": "medium",
        "dataset_or_source": "Yang et al. Nat Commun 2021; doi:10.1038/s41467-021-25768-0",
        "effect_direction": "MS-UC rg=0.33; MS-IBD rg=0.28",
        "statistic": "LDSC cross-trait genetic correlation; source highlights stronger MS-UC than MS-CD",
        "p_value": "source reports significant MS-IBD/MS-UC genetic correlation",
        "fdr_or_correction": "source-level LDSC/FDR; matrix placement pre-specified in MAP_METHODOLOGY_V8",
        "sample_size": "summary statistics: MS=47,429; IBD=59,957; CD=40,266; UC=45,975 in source",
        "file_or_url": "https://www.nature.com/articles/s41467-021-25768-0",
        "notes": "Verified LDSC source upgrades UC from target-overlap proxy to near supported on genetic architecture.",
    },
}


def place(jaccard: float, shared: int, ms_n: int, other_n: int) -> tuple[str, str, str]:
    if other_n == 0:
        return "unresolved", "provisional", "low"
    if shared >= 20 and jaccard >= 0.20:
        return "near", "supported", "medium"
    if shared >= 10 and jaccard >= 0.10:
        return "intermediate", "supported", "medium"
    if shared >= 5:
        return "intermediate", "provisional", "low"
    return "far", "provisional", "low"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(RAW, sep="\t")
    genetic = df[df["genetic_association"].fillna(0) >= 0.5].copy()
    by_disease = {
        disease: set(sub["gene"].dropna().astype(str))
        for disease, sub in genetic.groupby("disease", observed=True)
    }
    ms = by_disease.get("MS", set())

    evidence_rows = []
    placement_rows = []
    for target in TARGET_DISEASES:
        source_diseases: list[str]
        if target in {"Hashimoto thyroiditis", "Graves disease"}:
            source_diseases = ["AITD"]
        else:
            source_diseases = [k for k, v in DISEASE_LABELS.items() if v == target]
        other = set()
        source_names = []
        for source in source_diseases:
            other |= by_disease.get(source, set())
            source_names.append(source)
        shared = ms & other
        union = ms | other
        jaccard = len(shared) / len(union) if union else 0.0
        placement, grade, confidence = place(jaccard, len(shared), len(ms), len(other))
        eid = f"V8_axis_02_genetics_{target.replace(' ', '_')}"
        proxy_eid = eid
        evidence_rows.append(
            {
                "evidence_id": proxy_eid,
                "axis": "axis_02_genetics",
                "disease": target,
                "compartment": "germline",
                "data_type": "OpenTargets_genetic_association_overlap",
                "dataset_or_source": ",".join(source_names),
                "effect_direction": f"shared_with_MS={len(shared)}; jaccard={jaccard:.3f}",
                "statistic": f"MS_genetic_targets={len(ms)}; disease_genetic_targets={len(other)}",
                "p_value": "",
                "fdr_or_correction": "threshold genetic_association>=0.5; no LDSC/coloc",
                "sample_size": f"targets_shared={len(shared)}",
                "causality_level": "genetic",
                "supports_placement": placement,
                "caveat": "Target-overlap proxy, not genome-wide genetic correlation or colocalization.",
                "file_or_url": str(RAW.relative_to(ROOT)),
            }
        )
        primary_evidence_ids = proxy_eid
        contradiction_ids = ""
        notes = f"OpenTargets target-overlap proxy; shared genes include: {', '.join(sorted(shared)[:12])}"

        override = LITERATURE_OVERRIDES.get(target)
        if override:
            literature_eid = override["evidence_id"]
            evidence_rows.append(
                {
                    "evidence_id": literature_eid,
                    "axis": "axis_02_genetics",
                    "disease": target,
                    "compartment": "germline",
                    "data_type": "LDSC_genetic_correlation",
                    "dataset_or_source": override["dataset_or_source"],
                    "effect_direction": override["effect_direction"],
                    "statistic": override["statistic"],
                    "p_value": override["p_value"],
                    "fdr_or_correction": override["fdr_or_correction"],
                    "sample_size": override["sample_size"],
                    "causality_level": "genetic_correlation",
                    "supports_placement": override["placement"],
                    "caveat": "Genetic correlation does not prove shared causal variant or shared effector cell type.",
                    "file_or_url": override["file_or_url"],
                }
            )
            placement = override["placement"]
            grade = override["grade"]
            confidence = override["confidence"]
            primary_evidence_ids = f"{literature_eid};{proxy_eid}"
            notes = f"{override['notes']} Proxy shared genes include: {', '.join(sorted(shared)[:8])}"

        placement_rows.append(
            {
                "axis": "axis_02_genetics",
                "disease": target,
                "placement": placement,
                "grade": grade,
                "confidence": confidence,
                "primary_evidence_ids": primary_evidence_ids,
                "contradiction_ids": contradiction_ids,
                "compartment_summary": "germline",
                "causality_summary": "genetic_correlation" if override else "genetic",
                "selection_bias_risk": "medium" if grade == "supported" else "high",
                "notes": notes,
            }
        )

    pd.DataFrame(evidence_rows).to_csv(OUT / "axis_02_genetics_evidence.tsv", sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)
    pd.DataFrame(placement_rows).to_csv(OUT / "axis_02_genetics_placements.tsv", sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)
    report = [
        "# V8 Genetics Axis",
        "",
        "Default evidence is a first-pass proxy using existing V3 OpenTargets genetic association pulls.",
        "Crohn disease and ulcerative colitis include verified LDSC genetic-correlation evidence from Yang et al. 2021, which overrides the proxy placement.",
        "The remaining diseases are not yet LDSC/MR/fine-mapping/coloc and remain provisional.",
        "",
        "| disease | placement | grade | confidence | notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in placement_rows:
        report.append(f"| {row['disease']} | {row['placement']} | {row['grade']} | {row['confidence']} | {row['notes']} |")
    (OUT / "AXIS_02_GENETICS_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
