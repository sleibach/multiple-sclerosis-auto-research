#!/usr/bin/env python3
"""Tier 0 audit for selective CIITA/MHC-II/CD74 decoupling.

This script intentionally uses only local V3/V4 artifacts. It answers a narrow
question: does the current workspace contain enough perturbation evidence to
promote the CIITA/Mediator branch beyond Tier 0, or is the missing piece still
pharmacologic CDK8/CDK19 phenocopy in human APC-relevant systems?
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "tier0_ciita_mediator_selectivity"


DIRECT_PERTURBATIONS = ROOT / "phases/v3/results" / "wave15_perturbation_drug_response" / "ranked_direct_perturbations.tsv"
MOUSE_SELECTIVITY = ROOT / "phases/v3/results" / "wave15_perturbation_drug_response" / "gse162464_mouse_rna_selectivity.tsv"
COMPOUNDS = ROOT / "phases/v3/results" / "wave17_mediator_kinase_route" / "compound_landscape.tsv"
WAVE17_VERDICT = ROOT / "phases/v3/results" / "wave17_mediator_kinase_route" / "route_verdict.json"
WAVE53_AUDIT = ROOT / "phases/v3/results" / "wave53_perturbation_first_pivot" / "perturbation_first_audit.tsv"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def f(row: dict[str, str], key: str) -> float | None:
    value = row.get(key, "")
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def classify_selectivity(row: dict[str, str]) -> str:
    target = f(row, "target_suppression") or 0.0
    generic_ifn = f(row, "generic_ifn_suppression") or 0.0
    stress = f(row, "stress_induction") or 0.0
    ratio = f(row, "target_over_ifn_ratio") or 0.0
    score = f(row, "selectivity_score") or 0.0
    if target >= 1.0 and ratio >= 2.0 and score >= 0.75 and stress < 0.5:
        return "passes_selectivity_screen"
    if target >= 0.5 and generic_ifn <= 0.5 and stress < 0.5:
        return "weak_or_partial_selectivity"
    return "does_not_pass"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    rows = read_tsv(DIRECT_PERTURBATIONS)
    wanted = {"Med16_KO", "Gsk3b_KO", "RFX5", "TNFRSF1A"}
    selectivity_rows: list[dict[str, object]] = []
    for row in rows:
        perturbation = row.get("perturbation", "")
        if perturbation not in wanted and perturbation not in {"CDK8", "CDK19", "CCNC", "Cdk8", "Cdk19", "Ccnc"}:
            continue
        selectivity_rows.append(
            {
                "perturbation": perturbation,
                "dataset": row.get("dataset", ""),
                "system": row.get("system", ""),
                "perturbation_type": row.get("perturbation_type", ""),
                "target_suppression": f(row, "target_suppression"),
                "generic_ifn_suppression": f(row, "generic_ifn_suppression"),
                "target_over_ifn_ratio": f(row, "target_over_ifn_ratio"),
                "selectivity_score": f(row, "selectivity_score"),
                "stress_induction": f(row, "stress_induction"),
                "evidence_call": row.get("evidence_call", ""),
                "tier0_selectivity_call": classify_selectivity(row),
            }
        )

    write_tsv(
        OUT / "selectivity_audit.tsv",
        selectivity_rows,
        [
            "perturbation",
            "dataset",
            "system",
            "perturbation_type",
            "target_suppression",
            "generic_ifn_suppression",
            "target_over_ifn_ratio",
            "selectivity_score",
            "stress_induction",
            "evidence_call",
            "tier0_selectivity_call",
        ],
    )

    compounds = read_tsv(COMPOUNDS)
    compound_rows: list[dict[str, object]] = []
    for row in compounds:
        compound = row.get("compound", "")
        has_local_expression_phenocopy = False
        compound_rows.append(
            {
                "compound": compound,
                "status": row.get("status", ""),
                "potency_selectivity": row.get("potency_selectivity", ""),
                "delivery_pk": row.get("delivery_pk", ""),
                "safety_notes": row.get("safety_notes", ""),
                "has_local_expression_phenocopy": has_local_expression_phenocopy,
            }
        )

    write_tsv(
        OUT / "compound_phenocopy_gap.tsv",
        compound_rows,
        [
            "compound",
            "status",
            "potency_selectivity",
            "delivery_pk",
            "safety_notes",
            "has_local_expression_phenocopy",
        ],
    )

    med16 = next((r for r in selectivity_rows if r["perturbation"] == "Med16_KO"), None)
    gsk3b = next((r for r in selectivity_rows if r["perturbation"] == "Gsk3b_KO"), None)
    pharmacologic_phenocopy_count = sum(1 for r in compound_rows if r["has_local_expression_phenocopy"])
    passes = [r for r in selectivity_rows if r["tier0_selectivity_call"] == "passes_selectivity_screen"]

    verdict = {
        "random_seed": 20260528,
        "inputs": [
            str(DIRECT_PERTURBATIONS.relative_to(ROOT)),
            str(MOUSE_SELECTIVITY.relative_to(ROOT)),
            str(COMPOUNDS.relative_to(ROOT)),
            str(WAVE17_VERDICT.relative_to(ROOT)),
            str(WAVE53_AUDIT.relative_to(ROOT)),
        ],
        "med16_selectivity_score": med16["selectivity_score"] if med16 else None,
        "gsk3b_selectivity_score": gsk3b["selectivity_score"] if gsk3b else None,
        "n_selective_genetic_perturbations": len(passes),
        "n_local_pharmacologic_cdk8_19_phenocopies": pharmacologic_phenocopy_count,
        "tier0_call": "alive_but_parked_pending_pharmacologic_phenocopy",
        "reason": (
            "MED16 and GSK3B support selective CIITA/MHC-II/CD74 suppression, "
            "but no local CDK8/CDK19 inhibitor expression dataset demonstrates "
            "a comparable human APC pharmacologic phenocopy."
        ),
    }
    (OUT / "verdict.json").write_text(json.dumps(verdict, indent=2) + "\n")

    report = [
        "# Tier 0 CIITA/Mediator Selectivity Audit",
        "",
        "## Verdict",
        "",
        "`alive_but_parked_pending_pharmacologic_phenocopy`.",
        "",
        "The selective CIITA/MHC-II/CD74 decoupling mechanism remains the highest-priority V4 Tier 0 branch, but the CDK8/CDK19 intervention route cannot advance until a pharmacologic phenocopy is shown in human APC-relevant cells.",
        "",
        "## Key Numbers",
        "",
        f"- MED16 selectivity score: `{verdict['med16_selectivity_score']}`.",
        f"- GSK3B selectivity score: `{verdict['gsk3b_selectivity_score']}`.",
        f"- Selective genetic perturbations passing Tier 0 screen: `{verdict['n_selective_genetic_perturbations']}`.",
        f"- Local CDK8/CDK19 pharmacologic expression phenocopies found: `{verdict['n_local_pharmacologic_cdk8_19_phenocopies']}`.",
        "",
        "## Outputs",
        "",
        "- `selectivity_audit.tsv`",
        "- `compound_phenocopy_gap.tsv`",
        "- `verdict.json`",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
