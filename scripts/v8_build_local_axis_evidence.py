#!/usr/bin/env python3
"""Build V8 local evidence registry and preliminary placements.

This script only consolidates pre-existing local evidence and V7 locked outputs.
It does not populate genetics or microbiome axes.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v8_map"

DISEASES = [
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

AXES = {
    "axis_01_ifn_apc": "IFN/APC antigen-presentation state",
    "axis_04_lipid_lysosomal": "Lipid-lysosomal / foamy myeloid state",
    "axis_07_treatment_response": "Treatment-response architecture",
}

IFN_MODULES = {"ifn_apc", "hla_ii_apc", "mif_cd74_receptor_state", "mixscale_validated_ifng_readout"}
LIPID_MODULES = {"lysosomal_apc", "lipid_loader_repair"}


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]).replace("|", "/") for col in cols) + " |")
    return "\n".join(lines)


def evidence_row(
    evidence_id: str,
    axis: str,
    disease: str,
    compartment: str,
    data_type: str,
    dataset_or_source: str,
    effect_direction: str,
    statistic: str,
    p_value: str,
    fdr_or_correction: str,
    sample_size: str,
    causality_level: str,
    supports_placement: str,
    caveat: str,
    file_or_url: str,
) -> dict[str, str]:
    return {
        "evidence_id": evidence_id,
        "axis": axis,
        "disease": disease,
        "compartment": compartment,
        "data_type": data_type,
        "dataset_or_source": dataset_or_source,
        "effect_direction": effect_direction,
        "statistic": statistic,
        "p_value": p_value,
        "fdr_or_correction": fdr_or_correction,
        "sample_size": sample_size,
        "causality_level": causality_level,
        "supports_placement": supports_placement,
        "caveat": caveat,
        "file_or_url": file_or_url,
    }


def strongest_support(sub: pd.DataFrame, modules: set[str]) -> pd.DataFrame:
    x = sub[sub["module"].isin(modules)].copy()
    if x.empty:
        return x
    order = {"strong": 4, "supportive": 3, "trend": 2, "positive_null": 1, "negative_trend": -1, "null_or_negative": -2}
    x["support_rank"] = x["support_level"].map(order).fillna(0)
    return x.sort_values(["support_rank", "hedges_g"], ascending=[False, False])


def placement_from_local(disease: str, rows: list[dict[str, str]], axis: str) -> dict[str, str]:
    if not rows:
        return {
            "axis": axis,
            "disease": disease,
            "placement": "unresolved",
            "grade": "provisional",
            "confidence": "low",
            "primary_evidence_ids": "",
            "contradiction_ids": "",
            "compartment_summary": "no local evidence consolidated",
            "causality_summary": "none",
            "selection_bias_risk": "high",
            "notes": "Requires external/literature/genetic evidence.",
        }
    supports = [r for r in rows if r["supports_placement"] in {"near", "intermediate"}]
    negs = [r for r in rows if r["supports_placement"] in {"far", "contradictory_negative"}]
    ids = ";".join(r["evidence_id"] for r in rows)
    contradiction = ""
    if supports and negs:
        placement = "contradictory"
        grade = "supported" if len(rows) >= 2 else "provisional"
        confidence = "medium"
        contradiction = ";".join(r["evidence_id"] for r in negs)
    elif supports:
        placement = "near" if any(r["supports_placement"] == "near" for r in supports) else "intermediate"
        grade = "supported" if len(supports) >= 2 or any("locked" in r["fdr_or_correction"] for r in supports) else "provisional"
        if any("strong" in r["statistic"] or "locked pass" in r["fdr_or_correction"] for r in supports) and len(supports) >= 2:
            grade = "robust"
        confidence = "high" if grade == "robust" else "medium"
    else:
        placement = "far"
        grade = "supported" if len(negs) >= 2 else "provisional"
        confidence = "medium" if len(negs) >= 2 else "low"
    return {
        "axis": axis,
        "disease": disease,
        "placement": placement,
        "grade": grade,
        "confidence": confidence,
        "primary_evidence_ids": ids,
        "contradiction_ids": contradiction,
        "compartment_summary": "; ".join(sorted({r["compartment"] for r in rows})),
        "causality_summary": "; ".join(sorted({r["causality_level"] for r in rows})),
        "selection_bias_risk": "medium" if grade in {"supported", "robust"} else "high",
        "notes": "Local V3-V7 evidence only; genetics/microbiome/literature axes not yet incorporated.",
    }


def build_cell_state_evidence() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    path = ROOT / "results_v3" / "cross_disease_cell_state_convergence.tsv"
    df = pd.read_csv(path, sep="\t")
    evidence: list[dict[str, str]] = []
    placements: list[dict[str, str]] = []

    disease_alias = {
        "MS": "multiple sclerosis",
    }

    for axis, modules in [("axis_01_ifn_apc", IFN_MODULES), ("axis_04_lipid_lysosomal", LIPID_MODULES)]:
        grouped: dict[str, list[dict[str, str]]] = {d: [] for d in DISEASES}
        for disease in ["MS", *DISEASES]:
            sub = strongest_support(df[df["disease"] == disease], modules)
            if sub.empty:
                continue
            # Keep top two rows so compartment contradictions are visible but output remains bounded.
            for rank, (_, row) in enumerate(sub.head(2).iterrows(), start=1):
                support = str(row["support_level"])
                if support in {"strong", "supportive"}:
                    supports_placement = "near"
                elif support == "trend":
                    supports_placement = "intermediate"
                elif support == "positive_null":
                    supports_placement = "unresolved"
                elif support in {"negative_trend", "null_or_negative"}:
                    supports_placement = "far"
                else:
                    supports_placement = "unresolved"
                out_disease = disease_alias.get(disease, disease)
                eid = f"V8_{axis}_{out_disease.replace(' ', '_')}_{rank}"
                erow = evidence_row(
                    evidence_id=eid,
                    axis=axis,
                    disease=out_disease,
                    compartment=str(row["compartment"]),
                    data_type=str(row["modality"]),
                    dataset_or_source=str(row["dataset"]),
                    effect_direction=f"delta={row['delta']:.4g}; hedges_g={row['hedges_g']:.4g}; support={support}",
                    statistic=f"module={row['module']}; p={row['p']:.4g}; fdr={row['fdr']:.4g}; {support}",
                    p_value=f"{row['p']:.8g}",
                    fdr_or_correction=f"axis-local FDR={row['fdr']:.8g}",
                    sample_size=f"case={int(row['n_case'])}; control={int(row['n_control'])}",
                    causality_level="cross_sectional",
                    supports_placement=supports_placement,
                    caveat="Compartment-specific local case/control module evidence; not causal.",
                    file_or_url=str(path.relative_to(ROOT)),
                )
                evidence.append(erow)
                if out_disease in grouped:
                    grouped[out_disease].append(erow)

        for disease in DISEASES:
            placements.append(placement_from_local(disease, grouped[disease], axis))

    return evidence, placements


def build_treatment_response_evidence() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    path = ROOT / "analysis" / "v7_validation" / "v7_validation_summary.tsv"
    df = pd.read_csv(path, sep="\t")
    disease_map = {
        "RA": "rheumatoid arthritis",
        "IBD": "Crohn disease;ulcerative colitis",
        "UC": "ulcerative colitis",
    }
    evidence: list[dict[str, str]] = []
    grouped: dict[str, list[dict[str, str]]] = {d: [] for d in DISEASES}
    for idx, row in df.iterrows():
        diseases = disease_map.get(str(row["disease"]), str(row["disease"])).split(";")
        for disease in diseases:
            disease = disease.strip()
            if disease not in grouped:
                continue
            if row["pass_fail"] == "pass":
                supports = "near"
            elif float(row["auc"]) < 0.55 or float(row["hedges_g"]) < 0.20:
                supports = "far"
            else:
                supports = "intermediate"
            eid = f"V8_axis_07_treatment_{row['cohort']}_{disease.replace(' ', '_')}"
            erow = evidence_row(
                evidence_id=eid,
                axis="axis_07_treatment_response",
                disease=disease,
                compartment="blood" if "blood" in str(row["notes"]).lower() or "CD14" in str(row["cohort"]) else "intestinal mucosa",
                data_type="locked_validation_or_followon",
                dataset_or_source=str(row["cohort"]),
                effect_direction=f"AUC={row['auc']:.3f}; hedges_g={row['hedges_g']:.3f}; feature={row['locked_feature']}",
                statistic=f"locked V7 {row['pass_fail']}; n={int(row['n_labeled'])}",
                p_value=f"{row['p_value']:.8g}",
                fdr_or_correction="locked V7 thresholds",
                sample_size=str(int(row["n_labeled"])),
                causality_level="treatment_perturbation",
                supports_placement=supports,
                caveat="Treatment-response architecture only; V7 killed cross-disease baseline fallback.",
                file_or_url=str(path.relative_to(ROOT)),
            )
            evidence.append(erow)
            grouped[disease].append(erow)

    # Add exploratory vedolizumab context as intermediate/non-locked support for UC repair/response.
    vdz = ROOT / "analysis" / "v7_hyp_v7_001_specificity" / "gse73661_vdz_w6_result.json"
    if vdz.exists():
        erow = evidence_row(
            evidence_id="V8_axis_07_treatment_GSE73661_VDZ_UC",
            axis="axis_07_treatment_response",
            disease="ulcerative colitis",
            compartment="intestinal mucosa",
            data_type="exploratory_treatment_perturbation",
            dataset_or_source="GSE73661_VDZ_W6_exploratory",
            effect_direction="AUC=0.889; hedges_g=1.286; feature=-delta_IFN_APC",
            statistic="exploratory Class C; not locked V7 validation",
            p_value="0.1622",
            fdr_or_correction="not counted in V7 locked validation",
            sample_size="24",
            causality_level="treatment_perturbation",
            supports_placement="intermediate",
            caveat="Suggests mucosal healing/plasticity rather than anti-TNF specificity.",
            file_or_url=str(vdz.relative_to(ROOT)),
        )
        evidence.append(erow)
        grouped["ulcerative colitis"].append(erow)

    placements = [placement_from_local(disease, grouped[disease], "axis_07_treatment_response") for disease in DISEASES]
    return evidence, placements


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    evidence: list[dict[str, str]] = []
    placements: list[dict[str, str]] = []
    ev, pl = build_cell_state_evidence()
    evidence.extend(ev)
    placements.extend(pl)
    ev, pl = build_treatment_response_evidence()
    evidence.extend(ev)
    placements.extend(pl)

    evidence_df = pd.DataFrame(evidence)
    placement_df = pd.DataFrame(placements)
    evidence_df.to_csv(OUT / "local_evidence_registry.tsv", sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)
    placement_df.to_csv(OUT / "local_placement_matrix.tsv", sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)
    for axis in AXES:
        placement_df[placement_df["axis"] == axis].to_csv(OUT / f"{axis}_placements.tsv", sep="\t", index=False)
        evidence_df[evidence_df["axis"] == axis].to_csv(OUT / f"{axis}_evidence.tsv", sep="\t", index=False)

    summary = placement_df.groupby(["axis", "placement", "grade"]).size().reset_index(name="n")
    summary.to_csv(OUT / "local_axis_summary.tsv", sep="\t", index=False)

    report = [
        "# V8 Local Axis Consolidation",
        "",
        "Generated from existing V3-V7 outputs after `docs/locked_rules/MAP_METHODOLOGY_V8.md` was committed.",
        "",
        "## Placement Summary",
        "",
        markdown_table(summary),
        "",
        "## Scope",
        "",
        "Axes populated here: IFN/APC antigen-presentation, lipid-lysosomal/foamy myeloid, and treatment-response architecture.",
        "",
        "Genetics, microbiome, complement, adaptive repertoire, repair/resolution, pregnancy, and infectious-trigger axes remain to be populated.",
    ]
    (OUT / "LOCAL_AXIS_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
