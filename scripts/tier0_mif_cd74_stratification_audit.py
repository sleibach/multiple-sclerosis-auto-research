#!/usr/bin/env python3
"""Tier 0 audit for MIF/CD74 stratification.

This is not a target-nomination audit. The V4 question is whether a
CD74/CD44/CXCR4/HLA-II receptor-state score is strong enough to enter Tier 1 as
a predictive or enrichment biomarker for response/resistance.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "tier_0_triage" / "mif_cd74_stratification"
SEED = 20260528
MODULE = "mif_cd74_receptor_state"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def f(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    return float(value) if value not in {"", None} else 0.0


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    residual_rows = [
        row
        for row in read_tsv(
            ROOT / "results_v3" / "residualization" / "ifn_residualization_module_tests.tsv"
        )
        if row["target_module"] == MODULE
    ]

    summary = json.loads(
        (ROOT / "results_v3" / "residualization" / "ifn_residualization_summary.json").read_text()
    )

    rows: list[dict[str, object]] = []
    for row in residual_rows:
        rows.append(
            {
                "dataset": row["dataset"],
                "disease_name": row["disease_name"],
                "compartment": row["compartment"],
                "raw_delta": row["raw_delta_case_minus_control"],
                "raw_hedges_g": row["raw_hedges_g"],
                "raw_p": row["raw_p"],
                "raw_fdr": row["raw_fdr"],
                "residual_delta": row["residual_delta_case_minus_control"],
                "residual_hedges_g": row["residual_hedges_g"],
                "residual_p": row["residual_p"],
                "residual_fdr": row["residual_fdr"],
                "target_vs_ifn_r2": row["target_vs_ifn_r2"],
                "residual_retains_nominal_support": row["residual_retains_nominal_support"],
            }
        )

    nominal_residual = [
        row
        for row in residual_rows
        if row["residual_retains_nominal_support"] == "True"
        and f(row, "residual_delta_case_minus_control") > 0
    ]
    fdr_residual = [row for row in nominal_residual if f(row, "residual_fdr") <= 0.10]
    ms_nominal = [
        row for row in nominal_residual if row["disease_name"] == "MS" and "white_matter" in row["dataset"]
    ]

    remission_path = (
        ROOT / "results_v3" / "wave67_gse282122_myeloid_pseudobulk" / "remission_interaction_tests.tsv"
    )
    remission_modules = set()
    if remission_path.exists():
        remission_modules = {row.get("module", "") for row in read_tsv(remission_path)}

    pass_criteria = {
        "ms_residual_nominal": bool(ms_nominal),
        "cross_disease_residual_fdr10_in_2_systems": len({row["disease_name"] for row in fdr_residual})
        >= 2,
        "component_resolved_cd74_receptor_without_hla_done": False,
        "treatment_resistance_or_remission_interaction_available": MODULE in remission_modules,
        "prior_art_delta_is_stratification_not_target": True,
    }

    call = (
        "PARK_TIER0_COMPONENT_AND_TREATMENT_INTERACTION_REQUIRED"
        if pass_criteria["ms_residual_nominal"]
        else "DEMOTE_BIOMARKER_ONLY"
    )

    decision = {
        "random_seed": SEED,
        "candidate": "MIF_CD74_STRATIFICATION",
        "tier0_question": "Can a CD74/CD44/CXCR4/HLA-II receptor-state score serve as a predictive/enrichment biomarker rather than a universal target?",
        "criteria": pass_criteria,
        "nominal_residual_systems": sorted({row["disease_name"] for row in nominal_residual}),
        "fdr10_residual_systems": sorted({row["disease_name"] for row in fdr_residual}),
        "mif_cd74_in_remission_interaction_table": MODULE in remission_modules,
        "tier0_call": call,
        "interpretation": (
            "The branch survives only as a parked stratification hypothesis. "
            "MS white-matter microglia show nominal IFN-residual support, but no "
            "MIF/CD74 residual test survives FDR<=0.10, cross-disease residual breadth is weak, "
            "component-resolved CD74-vs-HLA testing is not locally complete, and the available "
            "IBD remission interaction table does not test the MIF/CD74 module."
        ),
    }

    write_tsv(OUT / "residual_evidence.tsv", rows)
    (OUT / "decision.json").write_text(json.dumps(decision, indent=2) + "\n")

    ms_row = ms_nominal[0] if ms_nominal else None
    report_lines = [
        "# MIF/CD74 Stratification Tier 0 Audit",
        "",
        f"Random seed: `{SEED}`",
        "",
        "## Decision",
        "",
        f"`{call}`.",
        "",
        "The branch is not promoted to Tier 1. It remains a parked stratification",
        "hypothesis, not a therapeutic target nomination.",
        "",
        "## Key Outputs",
        "",
        f"- Nominal IFN-residual diseases: `{';'.join(decision['nominal_residual_systems'])}`.",
        f"- FDR<=0.10 IFN-residual diseases: `{';'.join(decision['fdr10_residual_systems'])}`.",
        f"- Remission interaction table contains `{MODULE}`: `{MODULE in remission_modules}`.",
    ]
    if ms_row:
        report_lines.extend(
            [
                f"- MS white-matter residual delta: `{ms_row['residual_delta_case_minus_control']}`.",
                f"- MS white-matter residual Hedges g: `{ms_row['residual_hedges_g']}`.",
                f"- MS white-matter residual p: `{ms_row['residual_p']}`.",
                f"- MS white-matter residual FDR: `{ms_row['residual_fdr']}`.",
            ]
        )
    report_lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "Under V4 prior-art rules, MIF/CD74 is not killed merely because ibudilast",
            "and CD74/MIF prior art exist. The surviving contribution would be a",
            "treatment-by-biomarker or lesion/CSF enrichment test. The local evidence",
            "does not yet provide that interaction test. The next valid analysis is",
            "component-resolved residualization plus treatment-response interaction,",
            "not another raw CD74/HLA expression screen.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    main()
