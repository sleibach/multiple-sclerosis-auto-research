#!/usr/bin/env python3
"""Write the current V8 MS-centered mechanism map synthesis from matrix files."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v8_map"
MATRIX = OUT / "placement_matrix.tsv"
EVIDENCE = OUT / "evidence_registry.tsv"
DEST = ROOT / "docs/findings/MS_MECHANISM_MAP_V8.md"

AXIS_LABELS = {
    "axis_01_ifn_apc": "IFN/APC Antigen-Presentation State",
    "axis_02_genetics": "Genetic Risk Architecture",
    "axis_03_microbiome": "Gut Microbiome And Microbial-Immune Signaling",
    "axis_04_lipid_lysosomal": "Lipid-Lysosomal / Foamy Myeloid State",
    "axis_05_complement_innate": "Complement And Innate Effector Biology",
    "axis_06_tcell_adaptive_repertoire": "T-Cell And Adaptive Repertoire",
    "axis_07_treatment_response": "Treatment-Response Architecture",
    "axis_08_tissue_repair_resolution": "Tissue Repair And Resolution Biology",
    "axis_09_sex_hormonal_pregnancy": "Sex, Hormonal, And Pregnancy Modulation",
    "axis_10_infectious_trigger": "Infectious-Trigger Biology",
}

DISEASE_ORDER = [
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


def compact_cell(row: pd.Series) -> str:
    return f"{row['placement']} / {row['grade']} / {row['confidence']}"


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in df.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(lines)


def summarize_disease(matrix: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for disease in DISEASE_ORDER:
        sub = matrix[matrix["disease"] == disease]
        counts = defaultdict(int)
        supported_axes = []
        caveats = []
        for row in sub.itertuples(index=False):
            counts[row.placement] += 1
            if row.grade in {"supported", "robust"}:
                supported_axes.append(f"{row.axis}:{row.placement}")
            if row.placement == "contradictory":
                caveats.append(row.axis)
        rows.append(
            {
                "disease": disease,
                "near": counts["near"],
                "intermediate": counts["intermediate"],
                "far": counts["far"],
                "contradictory": counts["contradictory"],
                "unresolved": counts["unresolved"],
                "supported_or_robust_axes": "; ".join(supported_axes),
                "major_caveat": "contradictory: " + "; ".join(caveats) if caveats else "",
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    matrix = pd.read_csv(MATRIX, sep="\t").fillna("")
    evidence = pd.read_csv(EVIDENCE, sep="\t").fillna("")

    pivot_rows = []
    for disease in DISEASE_ORDER:
        row = {"disease": disease}
        for axis, label in AXIS_LABELS.items():
            sub = matrix[(matrix["disease"] == disease) & (matrix["axis"] == axis)]
            row[label] = compact_cell(sub.iloc[0]) if len(sub) else "missing"
        pivot_rows.append(row)
    pivot = pd.DataFrame(pivot_rows)
    disease_summary = summarize_disease(matrix)
    axis_summary = (
        matrix.groupby("axis")
        .agg(
            placements=("disease", "count"),
            supported_or_robust=("grade", lambda s: int(s.isin(["supported", "robust"]).sum())),
            robust=("grade", lambda s: int((s == "robust").sum())),
            unresolved=("placement", lambda s: int((s == "unresolved").sum())),
        )
        .reset_index()
    )
    axis_summary["axis_label"] = axis_summary["axis"].map(AXIS_LABELS)
    axis_summary = axis_summary[["axis", "axis_label", "placements", "supported_or_robust", "robust", "unresolved"]]

    lines = [
        "# MS Mechanism Map V8",
        "",
        "Status: current V8 synthesis, generated from `analysis/v8_map/placement_matrix.tsv` and `analysis/v8_map/evidence_registry.tsv`.",
        "",
        "This is an MS-centered, multi-axis map. It is not a binary disease clustering. Each cell is placement / grade / confidence relative to MS on that axis only.",
        "",
        "Methodology was pre-specified in `docs/locked_rules/MAP_METHODOLOGY_V8.md` and committed before placement generation (`9c2e548`). The map currently contains "
        f"{len(matrix)} disease-axis placements and {len(evidence)} evidence rows.",
        "",
        "## Executive Interpretation",
        "",
        "1. The repeated project-level partition survives in a narrower form: RA is far from MS on blood IFN/APC treatment-response architecture, but not globally far from MS on every axis.",
        "2. UC and Crohn are closest to MS on the axes currently best supported by project-local evidence: mucosal IFN/APC dynamics, tissue-repair response monitoring, and UC genetic correlation. Their microbiome proximity is plausible but remains provisional until a harmonized quantitative microbiome matrix is built.",
        "3. SLE is not IBD-like; it is provisionally MS-adjacent on complement/innate effector and pregnancy axes, and supported on the infectious-trigger/EBV axis in the current matrix. This suggests a distinct MS-SLE hypothesis space, but it is not yet a robust neighborhood.",
        "4. T1D is near MS on IFN/APC and lipid-lysosomal local axes and provisionally near on microbiome/adaptive antigen-specific autoimmunity, but its tissue-repair and treatment-response axes remain unresolved.",
        "5. The current genetics axis is still incomplete: only UC/Crohn have verified genetic-correlation upgrades; most other diseases remain target-overlap proxies.",
        "",
        "## Axis Coverage",
        "",
        markdown_table(axis_summary),
        "",
        "## Full Placement Matrix",
        "",
        markdown_table(pivot),
        "",
        "## Disease-Level Summary",
        "",
        markdown_table(disease_summary),
        "",
        "## Robust And Supported Core",
        "",
        "- **RA divergence is axis-specific.** RA is `far/supported` on IFN/APC treatment-response behavior in blood and `far/supported` on the V7 response-monitoring axis, but `near/supported` on pregnancy modulation and `intermediate/provisional` on genetics and microbiome.",
        "- **IBD proximity is mucosal and dynamic.** Crohn and UC are near MS on mucosal IFN/APC and repair/response-monitoring axes. UC is contradictory on treatment-response because early dynamic response validates while baseline prediction fails.",
        "- **MS-gut question, current answer:** MS is provisionally closer to IBD and T1D than to RA on the microbiome axis, but this is not yet supported-grade because the current axis is literature anchored rather than computed from a harmonized microbiome effect-size matrix.",
        "- **SLE is a provisional distinct comparator space.** SLE is supported on infectious-trigger/EBV and provisional on complement/pregnancy axes, while its IFN/APC local placement is unresolved in the current matrix.",
        "",
        "## Main Negative And Unresolved Content",
        "",
        "- The map does not support a single pan-autoimmune IFN/APC mechanism. RA repeatedly breaks the blood/treatment-response version of that axis.",
        "- The map does not support transferring IBD mucosal response biomarkers directly to RA blood.",
        "- Genetics is not yet strong enough outside UC/Crohn to adjudicate whether transcriptomic proximity is genetically anchored.",
        "- Axes with many unresolved placements: pregnancy, infectious triggers, complement, repair, and treatment response outside IBD/RA.",
        "",
        "## MS-Specific Implications",
        "",
        "- **Drug-repositioning watchlist:** IBD mechanisms should be watched for mucosal/barrier/microbiome and dynamic inflammatory-resolution biomarkers, not assumed to transfer as baseline MS stratifiers.",
        "- **Biomarker-transfer hypothesis:** early IFN/APC downshift is a repair/response-monitoring architecture in barrier tissue; the MS analogue would need CNS/CSF or lesion-edge sampling, not PBMC baseline measurement.",
        "- **Adjacent-disease comparator strategy:** RA should be used as a negative or axis-divergent comparator for blood APC response rules; SLE should be used as a comparator for EBV/complement/IFN-trigger mechanisms.",
        "- **Microbiome implication:** current evidence justifies testing whether MS-IBD proximity is mediated by gut barrier/metabolite axes, especially SCFA/bile-acid/mucin-linked biology, rather than generic dysbiosis. It does not yet establish that claim.",
        "",
        "## Falsification Paths",
        "",
        "1. **MS-IBD mucosal/proxy transfer:** In paired MS CSF/lesion-edge or gut-biopsy cohorts with treatment response, test whether early IFN/APC downshift precedes and predicts tissue repair. Stop-loss: AUC < 0.60 or effect direction opposite in two independent cohorts.",
        "2. **Microbiome axis:** Build a harmonized MS/IBD/RA/T1D metagenomic-metabolomic matrix and test whether MS is closer to IBD/T1D than RA after age, sex, medication, stool-processing, and geography adjustment. Stop-loss: no MS-IBD/T1D proximity after correction and effect-size stability < 50% across cohorts.",
        "3. **Genetics axis:** Run LDSC/HDL and coloc across MS, UC, Crohn, RA, SLE, psoriasis, T1D, celiac, and thyroid disease. Stop-loss: UC/Crohn proximity disappears under genome-wide correlation or shared loci fail colocalization at major immune loci.",
        "",
        "## Reproducibility",
        "",
        "Entry points:",
        "",
        "```bash",
        ".venv/bin/python scripts/v8_build_local_axis_evidence.py",
        ".venv/bin/python scripts/v8_build_genetics_axis.py",
        ".venv/bin/python scripts/v8_build_microbiome_axis.py",
        ".venv/bin/python scripts/v8_build_literature_axes.py",
        ".venv/bin/python scripts/v8_merge_axis_outputs.py",
        ".venv/bin/python scripts/v8_write_map_synthesis.py",
        "```",
        "",
        "Key outputs:",
        "",
        "- `analysis/v8_map/evidence_registry.tsv`",
        "- `analysis/v8_map/placement_matrix.tsv`",
        "- `analysis/v8_map/MAP_MERGE_REPORT.md`",
        "- `docs/findings/MS_MECHANISM_MAP_V8.md`",
        "",
        "Known limitation: several axes are literature/local-evidence placements, not harmonized raw-data re-analyses. Their grade and confidence are intentionally capped.",
        "",
    ]
    DEST.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
