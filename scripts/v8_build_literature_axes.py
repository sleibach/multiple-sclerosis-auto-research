#!/usr/bin/env python3
"""Build selected V8 literature/local-evidence axes.

Axes covered here are intentionally conservative:
- axis_05_complement_innate
- axis_09_sex_hormonal_pregnancy
- axis_10_infectious_trigger

Rows are evidence-traced and capped at supported/provisional unless the project
has repeated local rediscovery plus independent literature support.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v8_map"

ROWS = [
    # T-cell and adaptive repertoire
    {
        "axis": "axis_06_tcell_adaptive_repertoire",
        "disease": "psoriasis",
        "placement": "near",
        "grade": "provisional",
        "confidence": "medium",
        "compartment": "skin/blood",
        "data_type": "literature_review/approved_drug_mechanism",
        "source": "IL-23/Th17 biology is central in psoriasis and overlaps with MS/EAE adaptive immune mechanisms, although IL-17 blockade has not translated cleanly to MS.",
        "statistic": "approved IL-17/IL-23 axis drugs in psoriasis; qualitative shared Th17 axis",
        "causality": "clinical_perturbation/literature",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11054058/",
        "caveat": "Near for Th17/adaptive axis, not for CNS tissue injury or treatment-response architecture.",
    },
    {
        "axis": "axis_06_tcell_adaptive_repertoire",
        "disease": "Crohn disease",
        "placement": "intermediate",
        "grade": "provisional",
        "confidence": "medium",
        "compartment": "intestinal mucosa",
        "data_type": "literature_review/approved_drug_mechanism",
        "source": "Crohn disease has strong Th1/Th17 and IL-23 biology, but clinical IL-17 blockade can worsen IBD, separating it from simple MS/EAE Th17 transfer.",
        "statistic": "qualitative therapy-class evidence",
        "causality": "clinical_perturbation/literature",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11054058/",
        "caveat": "Intermediate because adaptive axis overlaps but intervention direction differs by tissue/barrier context.",
    },
    {
        "axis": "axis_06_tcell_adaptive_repertoire",
        "disease": "ulcerative colitis",
        "placement": "intermediate",
        "grade": "provisional",
        "confidence": "medium",
        "compartment": "intestinal mucosa",
        "data_type": "literature_review/approved_drug_mechanism",
        "source": "UC shares IL-23/Th17 pathway involvement but differs from MS in tissue and therapy-transfer behavior.",
        "statistic": "qualitative therapy-class evidence",
        "causality": "clinical_perturbation/literature",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11054058/",
        "caveat": "Intermediate rather than near because barrier-tissue constraints dominate intervention consequences.",
    },
    {
        "axis": "axis_06_tcell_adaptive_repertoire",
        "disease": "rheumatoid arthritis",
        "placement": "intermediate",
        "grade": "provisional",
        "confidence": "low",
        "compartment": "synovium/blood",
        "data_type": "literature_review",
        "source": "RA has T-cell involvement but V7 treatment-response evidence argues against a shared blood APC response rule with MS.",
        "statistic": "qualitative",
        "causality": "literature",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11054058/",
        "caveat": "Compartment likely matters; synovial adaptive states are not captured by V7 blood failures.",
    },
    {
        "axis": "axis_06_tcell_adaptive_repertoire",
        "disease": "type 1 diabetes mellitus",
        "placement": "near",
        "grade": "provisional",
        "confidence": "medium",
        "compartment": "pancreatic islets/blood",
        "data_type": "literature_review",
        "source": "T1D and MS are both organ-specific autoimmune diseases with strong HLA/T-cell antigen specificity themes.",
        "statistic": "qualitative HLA/T-cell organ-specific autoimmunity",
        "causality": "genetic/literature",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11054058/",
        "caveat": "Near on adaptive specificity, not on microbiome age-window or tissue repair biology.",
    },
    # Tissue repair and resolution
    {
        "axis": "axis_08_tissue_repair_resolution",
        "disease": "Crohn disease",
        "placement": "near",
        "grade": "supported",
        "confidence": "medium",
        "compartment": "intestinal mucosa",
        "data_type": "local_treatment_response/literature",
        "source": "V7 HYP_V7_001: early intestinal IFN/APC downshift tracks response and likely mucosal healing/plasticity; repair-state dynamics are therefore near MS's repair/resolution question at the level of monitoring architecture.",
        "statistic": "GSE16879 AUC 0.754, Hedges g 0.985 for paired early IFN/APC downshift",
        "causality": "treatment_perturbation",
        "url": "docs/validation/VALIDATION_LEDGER.md",
        "caveat": "Near on response-monitoring/repair dynamics, not on remyelination biology.",
    },
    {
        "axis": "axis_08_tissue_repair_resolution",
        "disease": "ulcerative colitis",
        "placement": "near",
        "grade": "supported",
        "confidence": "medium",
        "compartment": "intestinal mucosa",
        "data_type": "local_treatment_response/literature",
        "source": "V7 HYP_V7_001: UC infliximab and vedolizumab early mucosal IFN/APC downshift tracks response, interpreted as mucosal healing/plasticity rather than pretreatment stratification.",
        "statistic": "GSE73661_IFX AUC 0.825, Hedges g 1.390; vedolizumab exploratory AUC 0.889, Hedges g 1.286",
        "causality": "treatment_perturbation",
        "url": "knowledge/hypotheses/HYP_V7_001_IBD_IFN_APC_DOWNSHIFT.md",
        "caveat": "UC baseline prediction is contradictory; dynamic repair monitoring is the near placement.",
    },
    {
        "axis": "axis_08_tissue_repair_resolution",
        "disease": "rheumatoid arthritis",
        "placement": "far",
        "grade": "supported",
        "confidence": "medium",
        "compartment": "blood/synovium",
        "data_type": "local_treatment_response",
        "source": "V7 RA anti-TNF blood cohorts fail the early IFN/APC downshift response-monitoring rule that works in IBD mucosa.",
        "statistic": "GSE8350 AUC 0.450; GSE12051 AUC 0.382; GSE138746_CD14 AUC 0.485",
        "causality": "treatment_perturbation",
        "url": "docs/validation/VALIDATION_LEDGER.md",
        "caveat": "Far for blood response-monitoring architecture; RA synovial tissue repair remains less tested.",
    },
    {
        "axis": "axis_08_tissue_repair_resolution",
        "disease": "psoriasis",
        "placement": "intermediate",
        "grade": "provisional",
        "confidence": "low",
        "compartment": "skin",
        "data_type": "literature_review",
        "source": "Barrier-tissue repair and resolution are central in psoriasis, but no V8-local response-monitoring evidence aligns it with MS/IBD repair architecture.",
        "statistic": "qualitative",
        "causality": "literature",
        "url": "",
        "caveat": "Needs psoriasis biologic response transcriptomics to upgrade.",
    },
    # Complement / innate effector biology
    {
        "axis": "axis_05_complement_innate",
        "disease": "systemic lupus erythematosus",
        "placement": "near",
        "grade": "provisional",
        "confidence": "medium",
        "compartment": "blood/kidney/immune-complex tissue",
        "data_type": "literature_review",
        "source": "Complement activation is a core SLE effector and biomarker axis; compare with complement/innate effector activity in MS lesions and neuroinflammation.",
        "statistic": "qualitative strong disease-mechanism evidence",
        "causality": "mechanistic/literature",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9953581/",
        "caveat": "Near on complement/innate-effector axis only; SLE is not globally near MS.",
    },
    {
        "axis": "axis_05_complement_innate",
        "disease": "rheumatoid arthritis",
        "placement": "intermediate",
        "grade": "provisional",
        "confidence": "low",
        "compartment": "synovium/blood",
        "data_type": "literature_review",
        "source": "Complement contributes to RA synovitis, but RA's project-local IFN/APC blood response architecture diverges from MS.",
        "statistic": "qualitative",
        "causality": "literature",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9953581/",
        "caveat": "Synovium may be closer than blood; compartment-specific evidence needed.",
    },
    {
        "axis": "axis_05_complement_innate",
        "disease": "Crohn disease",
        "placement": "intermediate",
        "grade": "provisional",
        "confidence": "low",
        "compartment": "intestinal mucosa",
        "data_type": "literature_review",
        "source": "IBD has innate effector/complement activity, but V8 MS proximity is stronger on microbiome and IFN/APC axes.",
        "statistic": "qualitative",
        "causality": "literature",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9953581/",
        "caveat": "Not upgraded without disease-specific complement statistics.",
    },
    {
        "axis": "axis_05_complement_innate",
        "disease": "ulcerative colitis",
        "placement": "intermediate",
        "grade": "provisional",
        "confidence": "low",
        "compartment": "intestinal mucosa",
        "data_type": "literature_review",
        "source": "IBD has innate effector/complement activity, but V8 MS proximity is stronger on microbiome and IFN/APC axes.",
        "statistic": "qualitative",
        "causality": "literature",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9953581/",
        "caveat": "Not upgraded without disease-specific complement statistics.",
    },
    {
        "axis": "axis_05_complement_innate",
        "disease": "myasthenia gravis",
        "placement": "near",
        "grade": "supported",
        "confidence": "medium",
        "compartment": "neuromuscular junction",
        "data_type": "approved_drug_mechanism/literature",
        "source": "Complement blockade is clinically validated in AChR-positive generalized myasthenia gravis, indicating a strong complement-effector disease axis.",
        "statistic": "approved C5 inhibition class in MG",
        "causality": "clinical_perturbation",
        "url": "https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/761108s031lbl.pdf",
        "caveat": "Near to MS only on complement effector biology; adaptive trigger and tissue target differ sharply.",
    },
    # Sex, hormonal, pregnancy modulation
    {
        "axis": "axis_09_sex_hormonal_pregnancy",
        "disease": "rheumatoid arthritis",
        "placement": "near",
        "grade": "supported",
        "confidence": "medium",
        "compartment": "blood",
        "data_type": "local_pregnancy_transcriptomics",
        "source": "GSE235508 seropositive RA late-pregnancy trough and postpartum rebound in IFN/APC, HLA-II-only, MIF/CD74 receptor state, and lysosomal/APC modules.",
        "statistic": "see results/pregnancy_dimension/gse235508_timecourse/timepoint_contrasts.tsv",
        "causality": "natural_experiment",
        "url": "results/pregnancy_dimension/gse235508_timecourse/REPORT.md",
        "caveat": "Near on pregnancy modulation kinetics despite RA being far on blood treatment-response IFN/APC.",
    },
    {
        "axis": "axis_09_sex_hormonal_pregnancy",
        "disease": "systemic lupus erythematosus",
        "placement": "near",
        "grade": "provisional",
        "confidence": "medium",
        "compartment": "blood",
        "data_type": "local_pregnancy_transcriptomics",
        "source": "GSE108497 and GSE235508 show SLE pregnancy/postpartum APC-axis dynamics, including HLA-II rebound or monocyte-CD64 decoupling depending on outcome/context.",
        "statistic": "GSE108497 uncomplicated SLE postpartum HLA-II rebound delta 0.4525, Hedges g 0.597, p 0.0458 in V5 notebook",
        "causality": "natural_experiment",
        "url": "results/pregnancy_dimension/gse108497_sle/REPORT.md",
        "caveat": "Outcome-specific and not a simple remission axis.",
    },
    {
        "axis": "axis_09_sex_hormonal_pregnancy",
        "disease": "Crohn disease",
        "placement": "unresolved",
        "grade": "provisional",
        "confidence": "low",
        "compartment": "none",
        "data_type": "not_yet_populated",
        "source": "No V8-local pregnancy/natural-experiment evidence consolidated for Crohn.",
        "statistic": "",
        "causality": "none",
        "url": "",
        "caveat": "Unresolved, not far.",
    },
    {
        "axis": "axis_09_sex_hormonal_pregnancy",
        "disease": "ulcerative colitis",
        "placement": "unresolved",
        "grade": "provisional",
        "confidence": "low",
        "compartment": "none",
        "data_type": "not_yet_populated",
        "source": "No V8-local pregnancy/natural-experiment evidence consolidated for UC.",
        "statistic": "",
        "causality": "none",
        "url": "",
        "caveat": "Unresolved, not far.",
    },
    # Infectious triggers
    {
        "axis": "axis_10_infectious_trigger",
        "disease": "systemic lupus erythematosus",
        "placement": "near",
        "grade": "supported",
        "confidence": "medium",
        "compartment": "B cells/systemic immune",
        "data_type": "literature_review",
        "source": "EBV is strongly implicated in MS and has substantial mechanistic/serologic links to SLE, including molecular mimicry and abnormal EBV control themes.",
        "statistic": "qualitative strong EBV-autoimmunity literature",
        "causality": "infectious_association/mechanistic",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10136495/",
        "caveat": "SLE-EBV evidence is not equivalent to the Bjornevik-style near-necessary MS epidemiologic result.",
    },
    {
        "axis": "axis_10_infectious_trigger",
        "disease": "rheumatoid arthritis",
        "placement": "intermediate",
        "grade": "provisional",
        "confidence": "low",
        "compartment": "mucosa/joint/systemic immune",
        "data_type": "literature_review",
        "source": "RA has infectious and mucosal-trigger hypotheses, but no MS-like EBV near-necessity signal.",
        "statistic": "qualitative",
        "causality": "infectious_association",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10136495/",
        "caveat": "Intermediate because infectious-trigger architecture differs from MS.",
    },
    {
        "axis": "axis_10_infectious_trigger",
        "disease": "Crohn disease",
        "placement": "intermediate",
        "grade": "provisional",
        "confidence": "low",
        "compartment": "intestinal mucosa",
        "data_type": "literature_review",
        "source": "IBD has microbial-trigger/barrier-immune mechanisms, but they are not the same as EBV-centered MS risk architecture.",
        "statistic": "qualitative",
        "causality": "microbial_trigger",
        "url": "https://www.nature.com/articles/s41586-019-1237-9",
        "caveat": "IBD is near on microbiome, not necessarily near on infectious-trigger specificity.",
    },
    {
        "axis": "axis_10_infectious_trigger",
        "disease": "ulcerative colitis",
        "placement": "intermediate",
        "grade": "provisional",
        "confidence": "low",
        "compartment": "intestinal mucosa",
        "data_type": "literature_review",
        "source": "IBD has microbial-trigger/barrier-immune mechanisms, but they are not the same as EBV-centered MS risk architecture.",
        "statistic": "qualitative",
        "causality": "microbial_trigger",
        "url": "https://www.nature.com/articles/s41586-019-1237-9",
        "caveat": "UC is near on microbiome/genetics but only intermediate on EBV-like infectious-trigger biology.",
    },
]

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

AXES = [
    "axis_06_tcell_adaptive_repertoire",
    "axis_08_tissue_repair_resolution",
    "axis_05_complement_innate",
    "axis_09_sex_hormonal_pregnancy",
    "axis_10_infectious_trigger",
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = list(ROWS)
    keyed = {(r["axis"], r["disease"]) for r in rows}
    for axis in AXES:
        for disease in TARGET_DISEASES:
            if (axis, disease) in keyed:
                continue
            rows.append(
                {
                    "axis": axis,
                    "disease": disease,
                    "placement": "unresolved",
                    "grade": "provisional",
                    "confidence": "low",
                    "compartment": "none",
                    "data_type": "not_yet_populated",
                    "source": f"No V8 evidence row populated yet for {disease} on {axis}.",
                    "statistic": "",
                    "causality": "none",
                    "url": "",
                    "caveat": "Unresolved, not far.",
                }
            )

    evidence = []
    placements = []
    for i, row in enumerate(rows, start=1):
        eid = f"V8_{row['axis']}_{row['disease'].replace(' ', '_')}_{i}"
        evidence.append(
            {
                "evidence_id": eid,
                "axis": row["axis"],
                "disease": row["disease"],
                "compartment": row["compartment"],
                "data_type": row["data_type"],
                "dataset_or_source": row["source"],
                "effect_direction": row["placement"],
                "statistic": row["statistic"],
                "p_value": "",
                "fdr_or_correction": "literature/local-evidence placement under MAP_METHODOLOGY_V8; no quantitative matrix correction",
                "sample_size": "",
                "causality_level": row["causality"],
                "supports_placement": row["placement"],
                "caveat": row["caveat"],
                "file_or_url": row["url"],
            }
        )
        placements.append(
            {
                "axis": row["axis"],
                "disease": row["disease"],
                "placement": row["placement"],
                "grade": row["grade"],
                "confidence": row["confidence"],
                "primary_evidence_ids": eid,
                "contradiction_ids": "",
                "compartment_summary": row["compartment"],
                "causality_summary": row["causality"],
                "selection_bias_risk": "medium" if row["grade"] == "supported" else "high",
                "notes": row["caveat"],
            }
        )

    evidence_df = pd.DataFrame(evidence)
    placement_df = pd.DataFrame(placements)
    evidence_df.to_csv(OUT / "literature_axes_evidence.tsv", sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)
    placement_df.to_csv(OUT / "literature_axes_placements.tsv", sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)

    lines = [
        "# V8 Literature / Local Natural-Experiment Axes",
        "",
        "These axes are populated conservatively. They are useful for map coverage but should not be treated as equivalent to the quantitative IFN/APC or V7 treatment-response evidence.",
        "",
    ]
    for axis in AXES:
        sub = placement_df[placement_df["axis"] == axis]
        lines.extend([f"## {axis}", "", "| disease | placement | grade | confidence | caveat |", "| --- | --- | --- | --- | --- |"])
        for r in sub.itertuples(index=False):
            lines.append(f"| {r.disease} | {r.placement} | {r.grade} | {r.confidence} | {r.notes} |")
        lines.append("")
    (OUT / "LITERATURE_AXES_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
