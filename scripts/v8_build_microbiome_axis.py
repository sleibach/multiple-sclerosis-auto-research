#!/usr/bin/env python3
"""Build V8 microbiome axis from verified literature/data-source evidence."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v8_map"

ROWS = [
    {
        "disease": "Crohn disease",
        "placement": "near",
        "grade": "provisional",
        "confidence": "medium",
        "evidence": "HMP2/iHMP followed IBD subjects longitudinally with stool, biopsy, and blood multi-omics over one year; this is a direct gut immune-barrier disease context and shares the microbial-metabolite/SCFA/barrier axis implicated in MS.",
        "source": "https://www.nature.com/articles/s41586-019-1237-9",
        "caveat": "Near on gut microbial-immune axis, not proof that Crohn and MS share initiating causes.",
        "causality": "longitudinal",
    },
    {
        "disease": "ulcerative colitis",
        "placement": "near",
        "grade": "provisional",
        "confidence": "medium",
        "evidence": "Same HMP2/iHMP IBD longitudinal multi-omics resource includes UC and captures functional dysbiosis during disease activity; V7 also found intestinal response IFN/APC downshift across IFX and VDZ in UC.",
        "source": "https://www.nature.com/articles/s41586-019-1237-9;analysis/v7_hyp_v7_001_specificity/REPORT.md",
        "caveat": "Microbiome proximity is stronger for gut-barrier biology than for CNS lesion biology.",
        "causality": "longitudinal;treatment_perturbation",
    },
    {
        "disease": "rheumatoid arthritis",
        "placement": "intermediate",
        "grade": "provisional",
        "confidence": "low",
        "evidence": "RA has gut-joint microbiome evidence focused on Prevotella copri and oral/gut bacteria; this is microbial-immune but differs from the MS/IBD SCFA/barrier/mucin-degradation framing.",
        "source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11007908/;https://www.mdpi.com/1422-0067/25/6/3386",
        "caveat": "RA microbiome evidence may be mechanistically real but points to gut-joint/Prevotella/oral pathogen routes rather than the MS gut-brain pattern.",
        "causality": "literature_review;mechanistic_animal",
    },
    {
        "disease": "type 1 diabetes mellitus",
        "placement": "near",
        "grade": "provisional",
        "confidence": "medium",
        "evidence": "TEDDY provides large longitudinal infant gut metagenomics in relation to islet autoimmunity and T1D, with functional evidence supporting protective SCFA-producing microbiota.",
        "source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6296767/;https://diabetesjournals.org/care/article/48/7/1125/158197/Unfolding-the-Mystery-of-Autoimmunity-The",
        "caveat": "Near on longitudinal microbiome/SCFA/early-autoimmunity axis, not on target tissue or age-of-onset biology.",
        "causality": "longitudinal",
    },
    {
        "disease": "psoriasis",
        "placement": "intermediate",
        "grade": "provisional",
        "confidence": "low",
        "evidence": "Recent systematic review supports psoriasis gut dysbiosis literature, but evidence is mostly cross-sectional and less mechanistically tied to MS-like gut-brain or IBD-like mucosal inflammation.",
        "source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12029981/",
        "caveat": "Skin-gut axis is plausible, but longitudinal/causal microbial evidence remains thinner than IBD/T1D.",
        "causality": "literature_review",
    },
    {
        "disease": "Sjogren syndrome",
        "placement": "intermediate",
        "grade": "provisional",
        "confidence": "low",
        "evidence": "Systematic review/meta-analysis reports gut microbiota disruption in primary Sjogren's syndrome.",
        "source": "https://pubmed.ncbi.nlm.nih.gov/37682372/",
        "caveat": "Evidence supports dysbiosis but not a well-resolved MS-shared microbial mechanism.",
        "causality": "literature_review",
    },
    {
        "disease": "celiac disease",
        "placement": "near",
        "grade": "provisional",
        "confidence": "low",
        "evidence": "Longitudinal prospective at-risk-child studies report microbiome signatures during progression toward celiac disease onset, making celiac close to MS on gut-barrier/microbiome plausibility but disease-specific to gluten/HLA.",
        "source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8307711/",
        "caveat": "Near is driven by gut-barrier longitudinal design, not by shared antigen trigger with MS.",
        "causality": "longitudinal",
    },
    {
        "disease": "systemic lupus erythematosus",
        "placement": "intermediate",
        "grade": "provisional",
        "confidence": "low",
        "evidence": "SLE microbiome literature includes gut dysbiosis and bacterial trigger/molecular mimicry themes, but this aligns more with systemic immune activation than with MS/IBD gut-barrier architecture.",
        "source": "https://www.nature.com/articles/s41584-023-01071-8",
        "caveat": "SLE may be closer to MS on infectious-trigger/IFN axes than on microbiome axis.",
        "causality": "literature_review",
    },
    {
        "disease": "Hashimoto thyroiditis",
        "placement": "unresolved",
        "grade": "provisional",
        "confidence": "low",
        "evidence": "No V8-verified thyroid-specific gut microbiome source was added in this pass.",
        "source": "",
        "caveat": "AITD is not absent; it is unresolved pending thyroid-focused microbiome sources.",
        "causality": "none",
    },
    {
        "disease": "Graves disease",
        "placement": "unresolved",
        "grade": "provisional",
        "confidence": "low",
        "evidence": "No V8-verified Graves-specific gut microbiome source was added in this pass.",
        "source": "",
        "caveat": "AITD is not absent; it is unresolved pending thyroid-focused microbiome sources.",
        "causality": "none",
    },
    {
        "disease": "myasthenia gravis",
        "placement": "unresolved",
        "grade": "provisional",
        "confidence": "low",
        "evidence": "No V8-verified myasthenia-specific microbiome source was added in this pass.",
        "source": "",
        "caveat": "Unresolved, not far.",
        "causality": "none",
    },
    {
        "disease": "ankylosing spondylitis",
        "placement": "near",
        "grade": "provisional",
        "confidence": "low",
        "evidence": "Spondyloarthritis is gut-linked in multiple reviews and appears in microbiome-autoimmunity discussions, but V8 has not yet added disease-specific longitudinal evidence.",
        "source": "https://link.springer.com/article/10.1007/s40588-023-00213-6",
        "caveat": "Near is biologically plausible gut-joint axis, but low confidence until disease-specific sources are added.",
        "causality": "literature_review",
    },
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    evidence_rows = []
    placement_rows = []
    for row in ROWS:
        eid = f"V8_axis_03_microbiome_{row['disease'].replace(' ', '_')}"
        evidence_rows.append(
            {
                "evidence_id": eid,
                "axis": "axis_03_microbiome",
                "disease": row["disease"],
                "compartment": "gut microbiome",
                "data_type": "literature_or_public_cohort",
                "dataset_or_source": row["source"],
                "effect_direction": row["evidence"],
                "statistic": "",
                "p_value": "",
                "fdr_or_correction": "literature evidence; no matrix p-value",
                "sample_size": "",
                "causality_level": row["causality"],
                "supports_placement": row["placement"],
                "caveat": row["caveat"],
                "file_or_url": row["source"],
            }
        )
        placement_rows.append(
            {
                "axis": "axis_03_microbiome",
                "disease": row["disease"],
                "placement": row["placement"],
                "grade": row["grade"],
                "confidence": row["confidence"],
                "primary_evidence_ids": eid,
                "contradiction_ids": "",
                "compartment_summary": "gut microbiome",
                "causality_summary": row["causality"],
                "selection_bias_risk": "medium" if row["grade"] == "supported" else "high",
                "notes": row["caveat"],
            }
        )
    pd.DataFrame(evidence_rows).to_csv(OUT / "axis_03_microbiome_evidence.tsv", sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)
    pd.DataFrame(placement_rows).to_csv(OUT / "axis_03_microbiome_placements.tsv", sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)
    lines = [
        "# V8 Microbiome Axis",
        "",
        "Interpretation: on the microbiome axis only, MS is placed nearer to IBD and T1D than to RA when the criterion is longitudinal gut microbial-immune/metabolite evidence. This is not a binary disease clustering. RA is intermediate because its gut-joint microbiome route is plausible but mechanistically different, with Prevotella/oral-pathogen themes rather than the MS/IBD SCFA-barrier/mucin axis.",
        "",
        "| disease | placement | grade | confidence | main caveat |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in placement_rows:
        lines.append(f"| {row['disease']} | {row['placement']} | {row['grade']} | {row['confidence']} | {row['notes']} |")
    (OUT / "AXIS_03_MICROBIOME_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
