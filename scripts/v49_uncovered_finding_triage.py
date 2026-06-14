#!/usr/bin/env python3
"""Triage V37 findings still lacking V48 external relationship rows.

This is source-intake planning only. It does not add external claims and does
not change grounded project findings. It decides whether future source intake
would be useful, risky, or data-first for the remaining uncovered findings.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_UNCOVERED = ROOT / "knowledge_external/synthesis/v37_uncovered_finding_rationale_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/synthesis"
SUMMARY_PATH = ROOT / "knowledge_external/catalogs/indexes/v49_uncovered_finding_triage_summary.json"


TRIAGE: dict[str, dict[str, str]] = {
    "IFN-beta HLA-II/CD74 branch": {
        "intake_decision": "dataset_or_predefined_test_only",
        "priority": "medium",
        "safe_source_type": "paired IFN-beta response transcriptomic dataset or predefined validation protocol",
        "avoid": "broad IFN-beta mechanism reviews or therapy labels",
        "rationale": "The project finding is provisional and therapy-specific; context could easily overstate it unless it points to a concrete validation route.",
    },
    "Sjogren antigen-presentation but not lysosomal/APC lesion-rim transfer": {
        "intake_decision": "narrow_direct_source_only",
        "priority": "low",
        "safe_source_type": "source directly comparing Sjogren antigen presentation with lysosomal/APC lesion-rim biology",
        "avoid": "generic Sjogren antigen-presentation literature",
        "rationale": "Generic antigen-presentation context would not address the project's negative transfer boundary.",
    },
    "NAMPT/eNAMPT not reactivated as target": {
        "intake_decision": "do_not_expand_without_direction_matched_target_evidence",
        "priority": "low",
        "safe_source_type": "MS-specific NAMPT/eNAMPT direction, safety, and intervention evidence that matches the project failure mode",
        "avoid": "general NAMPT immunometabolism or cancer-metabolism sources",
        "rationale": "The project already demoted NAMPT to marker/covariate; broad target enthusiasm would be a false-corrobation risk.",
    },
    "ZFP36L1 chr14 parked": {
        "intake_decision": "source_specific_genetics_only",
        "priority": "medium",
        "safe_source_type": "fine-mapping, QTL, or colocalization source resolving chr14 ZFP36L1 direction and robustness",
        "avoid": "gene-function or immune-regulation context without locus direction",
        "rationale": "The parked status is about weak coloc/QTL direction, so only signal-level sources are useful.",
    },
    "REL/PUS10/USP34 chr2 closed": {
        "intake_decision": "source_specific_genetics_only",
        "priority": "low",
        "safe_source_type": "disease SuSiE-coloc or equivalent signal-specific summary resolving the chr2 closure reason",
        "avoid": "general NF-kB/REL biology or pathway context",
        "rationale": "The closure reason is absence of disease SuSiE-coloc support, not lack of pathway plausibility.",
    },
    "Complement/lipid progressive axis downgraded": {
        "intake_decision": "direct_progressive_lesion_dataset_preferred",
        "priority": "medium",
        "safe_source_type": "progressive MS or chronic-active lesion dataset/source with complement and lipid-axis measurements",
        "avoid": "broad complement or lipid reviews without progressive/lesion specificity",
        "rationale": "This is one of the remaining biological hypotheses where a direct progressive-lesion source could be decision-useful.",
    },
    "Lysosomal APC bottleneck not proven": {
        "intake_decision": "direct_apc_perturbation_or_flux_source_only",
        "priority": "medium",
        "safe_source_type": "APC cathepsin/V-ATPase/lysosomal-flux perturbation data or source tied to MS-relevant antigen processing",
        "avoid": "generic lysosome or antigen-processing pathway context",
        "rationale": "The project observed coupling but not a bottleneck; only perturbation/flux evidence can address the missing causal step.",
    },
    "Metabolic/sterol setpoint is context/confounder axis, not intervention-grade": {
        "intake_decision": "covariate_context_only",
        "priority": "low",
        "safe_source_type": "sources that specify metabolic/sterol signatures as covariates or confounders in MS immune profiling",
        "avoid": "therapeutic repurposing claims based only on metabolic pathway overlap",
        "rationale": "The project treats this as context/confounding, not an intervention-grade target; external intake should preserve that boundary.",
    },
    "Multi-lineage and RPT lenses add prioritization, not evidence": {
        "intake_decision": "method_governance_source_optional",
        "priority": "low",
        "safe_source_type": "method literature on model-assisted review, provenance, or human/AI evidence boundaries",
        "avoid": "vendor/model capability claims",
        "rationale": "The project governance is already explicit; additional method context is optional and must not inflate model output into evidence.",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--uncovered", type=Path, default=DEFAULT_UNCOVERED)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def build_rows(uncovered: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in uncovered:
        item = row["item"]
        triage = TRIAGE[item]
        rows.append(
            {
                "item": item,
                "category": row.get("category", ""),
                "evidence_grade": row.get("evidence_grade", ""),
                "rationale_class": row.get("rationale_class", ""),
                "current_next_action": row.get("next_action", ""),
                **triage,
            }
        )
    return rows


def write_markdown(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    lines = [
        "# V49 Uncovered Finding Triage",
        "",
        "Status: source-intake planning only. This document does not add external records, assert convergence, or change any grounded finding.",
        "",
        "Boundary: remaining uncovered findings should not be padded with broad context. A future source is useful only when it addresses the exact failure mode, direction, data type, or method-governance question named here.",
        "",
        "## Summary",
        "",
        f"- uncovered findings triaged: `{summary['n_rows']}`",
        f"- dataset/test-only or direct-source rows: `{summary['direct_or_dataset_rows']}`",
        f"- low-priority/optional rows: `{summary['low_priority_rows']}`",
        "",
        "## Triage Table",
        "",
        "| finding | priority | intake decision | safe source type | avoid | rationale |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{md(row['item'])} | "
            f"`{md(row['priority'])}` | "
            f"`{md(row['intake_decision'])}` | "
            f"{md(row['safe_source_type'])} | "
            f"{md(row['avoid'])} | "
            f"{md(row['rationale'])} |"
        )
    lines.extend(
        [
            "",
            "## Operational Rule",
            "",
            "- Intake is warranted only for sources matching the row's safe source type.",
            "- Broad biological plausibility should stay out of the convergence matrix for these findings.",
            "- Any accepted future source still enters as segregated context and requires a later grounded test before it can affect project conclusions.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    uncovered = read_tsv(args.uncovered)
    rows = build_rows(uncovered)
    priority_counts: dict[str, int] = {}
    decision_counts: dict[str, int] = {}
    for row in rows:
        priority_counts[row["priority"]] = priority_counts.get(row["priority"], 0) + 1
        decision_counts[row["intake_decision"]] = decision_counts.get(row["intake_decision"], 0) + 1
    summary = {
        "purpose": "V49 uncovered finding triage; source-intake planning only; no biological claim",
        "n_rows": len(rows),
        "priority_counts": dict(sorted(priority_counts.items())),
        "decision_counts": dict(sorted(decision_counts.items())),
        "direct_or_dataset_rows": sum(1 for row in rows if row["priority"] == "medium"),
        "low_priority_rows": sum(1 for row in rows if row["priority"] == "low"),
        "overall_status": "PASS" if len(rows) == 9 else "REVIEW_NEEDED",
        "markdown": "knowledge_external/synthesis/V49_UNCOVERED_FINDING_TRIAGE.md",
        "tsv": "knowledge_external/synthesis/v49_uncovered_finding_triage.tsv",
    }
    fields = [
        "item",
        "category",
        "evidence_grade",
        "rationale_class",
        "current_next_action",
        "intake_decision",
        "priority",
        "safe_source_type",
        "avoid",
        "rationale",
    ]
    args.outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(args.outdir / "v49_uncovered_finding_triage.tsv", rows, fields)
    write_markdown(args.outdir / "V49_UNCOVERED_FINDING_TRIAGE.md", rows, summary)
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
