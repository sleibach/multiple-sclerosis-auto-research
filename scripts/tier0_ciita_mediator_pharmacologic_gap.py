#!/usr/bin/env python3
"""Tier 0 CIITA/Mediator pharmacologic-phenocopy gap test.

This script does not invent new perturbation data. It makes the V4 Tier 0
decision reproducible from locally cached V3 evidence:

- MED16 KO selective CIITA/MHC-II/CD74 suppression benchmark.
- GSE162463 CRISPR FACS signals for Cdk8/Cdk19/Ccnc vs Med16.
- Local CDK8/19 compound landscape.
- Local L1000 cache search for named CDK8/19 probes.

The Tier 0 question is whether CDK8/CDK19 is ready to advance from a plausible
Mediator-kinase route into mechanism budget. It advances only if direct
pharmacologic phenocopy evidence exists locally or is found in the perturbation
cache. Otherwise it remains alive but not promoted.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "tier0_ciita_mediator_pharmacologic_gap"

NAMED_PROBES = {
    "cortistatin",
    "cortistatin a",
    "dca",
    "cct251921",
    "msc2530818",
    "rvu120",
    "sel120",
    "senexin",
    "bcd-115",
    "brd6989",
    "as2863619",
    "cdk8",
    "cdk19",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def contains_probe(row: dict[str, str]) -> bool:
    text = " ".join(str(v).lower() for v in row.values())
    return any(probe in text for probe in NAMED_PROBES)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    summary_path = ROOT / "phases/v3/results" / "wave17_mediator_route_gate" / "summary.json"
    local_path = ROOT / "phases/v3/results" / "wave17_mediator_kinase_route" / "local_perturbation_evidence.tsv"
    compounds_path = ROOT / "phases/v3/results" / "wave17_mediator_kinase_route" / "compound_landscape.tsv"
    l1000_path = ROOT / "phases/v3/results" / "l1000fwd_compound_summary.tsv"

    summary = json.loads(summary_path.read_text())
    local_rows = read_tsv(local_path)
    compound_rows = read_tsv(compounds_path)
    l1000_rows = read_tsv(l1000_path) if l1000_path.exists() else []

    cdk_crispr_rows = [
        row for row in local_rows
        if row.get("perturbation", "").lower().startswith(("cdk8", "cdk19", "ccnc"))
    ]
    med16_rows = [
        row for row in local_rows
        if row.get("perturbation", "").lower().startswith("med16")
    ]
    l1000_probe_hits = [row for row in l1000_rows if contains_probe(row)]

    med16_selectivity = float(summary["med16_selectivity_score"])
    med16_target = float(summary["med16_target_module_effect"])
    med16_ifn = float(summary["med16_generic_ifn_effect"])

    has_named_chemical_matter = len(compound_rows) >= 3
    has_direct_pharmacologic_phenocopy = len(l1000_probe_hits) > 0
    cdk_genetic_phenocopy = False
    for row in cdk_crispr_rows:
        effect = row.get("effect", "").lower()
        if "rank 42" in effect or "strong" in row.get("interpretation", "").lower():
            cdk_genetic_phenocopy = True

    pass_tier0 = (
        med16_selectivity >= 2.0
        and has_named_chemical_matter
        and has_direct_pharmacologic_phenocopy
        and cdk_genetic_phenocopy
    )

    decision = {
        "candidate": "CDK8_CDK19_MEDIATOR / CIITA_SELECTIVE",
        "tier0_call": "DO_NOT_ADVANCE_TO_TIER1_YET" if not pass_tier0 else "ADVANCE_TO_TIER1",
        "seed": 20260528,
        "med16_target_module_effect": med16_target,
        "med16_generic_ifn_effect": med16_ifn,
        "med16_selectivity_score": med16_selectivity,
        "named_compounds_in_landscape": len(compound_rows),
        "local_l1000_named_probe_hits": len(l1000_probe_hits),
        "cdk8_cdk19_ccnc_crispr_rows": len(cdk_crispr_rows),
        "cdk8_cdk19_genetic_phenocopy": cdk_genetic_phenocopy,
        "interpretation": (
            "MED16 remains a strong selective CIITA/MHC-II/CD74 comparator and "
            "CDK8/19 chemical matter exists, but local evidence does not contain "
            "direct CDK8/19 pharmacologic phenocopy of MED16 in autoimmune APCs. "
            "The branch stays alive at Tier 0, not Tier 1."
        ),
        "next_test": (
            "Human monocyte-derived macrophage/DC IFN-gamma dose-response with "
            "cortistatin A, CCT251921, MSC2530818/RVU120 or inactive analogs; "
            "require CIITA/HLA-DRA/CD74 suppression selectivity ratio >=2 versus "
            "generic IFN/stress genes, preserved viability, and surface HLA-DR "
            "reduction."
        ),
    }

    write_tsv(OUT / "med16_rows.tsv", med16_rows)
    write_tsv(OUT / "cdk_crispr_rows.tsv", cdk_crispr_rows)
    write_tsv(OUT / "compound_landscape.tsv", compound_rows)
    write_tsv(OUT / "l1000_named_probe_hits.tsv", l1000_probe_hits)
    (OUT / "decision.json").write_text(json.dumps(decision, indent=2) + "\n")

    report = f"""# Tier 0 CIITA/Mediator Pharmacologic Gap

## Call

{decision['tier0_call']}

## Quantitative Evidence

- MED16 target module effect: {med16_target:.3f}
- MED16 generic IFN effect: {med16_ifn:.3f}
- MED16 selectivity score: {med16_selectivity:.3f}
- Named CDK8/19 compounds in V3 landscape: {len(compound_rows)}
- Local L1000 named CDK8/19 probe hits: {len(l1000_probe_hits)}
- Cdk8/Cdk19/Ccnc CRISPR rows: {len(cdk_crispr_rows)}
- Cdk8/Cdk19 genetic phenocopy of MED16: {cdk_genetic_phenocopy}

## Interpretation

MED16 is still a strong perturbation-derived comparator for selective
CIITA/MHC-II/CD74 suppression. CDK8/CDK19 has tractable chemical matter, but
local V3 data do not prove pharmacologic phenocopy. Cdk8/Cdk19/Ccnc genetic
screen rows are weak or non-phenocopy, and the local L1000 cache contains no
named CDK8/19 probe hit.

## Decision

Do not spend Tier 1 mechanism budget until the direct pharmacologic phenocopy
experiment exists or an external perturbation dataset is imported. Keep the
branch alive at Tier 0 because the wet-lab experiment is clear and feasible.
"""
    (OUT / "REPORT.md").write_text(report)
    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    main()
