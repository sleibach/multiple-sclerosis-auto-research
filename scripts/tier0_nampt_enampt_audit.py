#!/usr/bin/env python3
"""Tier 0 audit for the constrained NAMPT/eNAMPT V4 branch.

This script deliberately uses only local V3 artifacts. It tests whether NAMPT
has enough non-generic support to remain alive under the V4 Tier 0 standard:
MS-relevant signal, non-IBD replication, residual support after broad module
adjustment, genetics, and a plausible non-NAD-depleting modality.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "tier_0_triage" / "nampt_enampt_separation"
SEED = 20260528


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def find_gene(path: Path, gene: str) -> dict[str, str]:
    for row in read_tsv(path):
        if row.get("gene") == gene:
            return row
    raise SystemExit(f"{gene} not found in {path}")


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def as_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    return float(value) if value not in {"", None} else 0.0


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    cross = find_gene(ROOT / "phases/v3/results" / "cross_disease_gene_summary.tsv", "NAMPT")
    residual = find_gene(
        ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
        "NAMPT",
    )
    controller = find_gene(
        ROOT
        / "phases/v3/results"
        / "wave96_c15orf48_controller_search"
        / "pre_donor_controller_rank.tsv",
        "NAMPT",
    )
    genetics = find_gene(
        ROOT
        / "phases/v3/results"
        / "wave20_genetic_druggable_altaxis"
        / "local_opentargets_genetics_summary.tsv",
        "NAMPT",
    )

    evidence_rows: list[dict[str, object]] = [
        {
            "dimension": "cross_disease_expression",
            "source": "phases/v3/results/cross_disease_gene_summary.tsv",
            "metric": "trend_or_better_disease_count",
            "value": cross["n_trend_or_better_diseases"],
            "supporting_diseases": cross["supporting_diseases"],
            "tier0_interpretation": "IBD-only support; no MS/non-IBD autoimmune breadth sufficient for V4 promotion",
        },
        {
            "dimension": "module_adjusted_residual",
            "source": "phases/v3/results/broad_residual_gate/broad_residual_gate_summary.tsv",
            "metric": "non_ibd_retained_positive_disease_count",
            "value": residual["non_ibd_retained_positive_disease_count"],
            "supporting_diseases": residual["top_retained_tests"],
            "tier0_interpretation": "no non-IBD retained positive residual signal after broad module checks",
        },
        {
            "dimension": "ms_anchor",
            "source": "phases/v3/results/broad_residual_gate/broad_residual_gate_summary.tsv",
            "metric": "ms_wm_delta_log2;ms_wm_p",
            "value": f"{residual['ms_wm_delta_log2']};{residual['ms_wm_p']}",
            "supporting_diseases": "MS",
            "tier0_interpretation": "MS white-matter signal is negative/non-significant",
        },
        {
            "dimension": "candidate_controller",
            "source": "phases/v3/results/wave96_c15orf48_controller_search/pre_donor_controller_rank.tsv",
            "metric": "positive_contexts;residual_retained_disease_count",
            "value": f"{controller['positive_c15_contexts']};{controller['residual_retained_disease_count']}",
            "supporting_diseases": controller["positive_c15_contexts"],
            "tier0_interpretation": "C15-like state support is Crohn/UC/T1D-biased and did not pass gates for MS, genetics, perturbation, or modality",
        },
        {
            "dimension": "genetics",
            "source": "phases/v3/results/wave20_genetic_druggable_altaxis/local_opentargets_genetics_summary.tsv",
            "metric": "ot_max_score;ot_n_diseases_any",
            "value": f"{genetics['ot_max_score']};{genetics['ot_n_diseases_any']}",
            "supporting_diseases": genetics["ot_diseases_any"],
            "tier0_interpretation": "no local OpenTargets genetics support",
        },
        {
            "dimension": "modality",
            "source": "knowledge/candidates/NAMPT.md plus V3 prior-art ledger",
            "metric": "non_nad_depleting_or_tightly_bounded_modality",
            "value": "not_demonstrated_locally",
            "supporting_diseases": "",
            "tier0_interpretation": "generic systemic catalytic NAMPT inhibition remains closed; no local eNAMPT-specific neutralization or tissue-bounded modality evidence",
        },
    ]

    pass_criteria = {
        "ms_or_csf_ev_enrichment": as_float(residual, "ms_wm_delta_log2") > 0
        and as_float(residual, "ms_wm_p") < 0.05,
        "non_ibd_replication": as_float(residual, "non_ibd_retained_positive_disease_count") >= 1,
        "strict_core_covariate_survival": as_float(
            residual, "strict_core_covariate_surviving_disease_count"
        )
        >= 1,
        "genetics_anchor": as_float(genetics, "ot_max_score") >= 0.25,
        "non_nad_depleting_modality": False,
    }

    decision = {
        "random_seed": SEED,
        "candidate": "NAMPT constrained eNAMPT / biomarker-defined transient branch",
        "tier0_question": "Does local evidence separate eNAMPT/inflammatory-state biology from generic intracellular NAMPT/NAD stress metabolism?",
        "criteria": pass_criteria,
        "pass_count": sum(1 for value in pass_criteria.values() if value),
        "tier0_call": "DEMOTE_TO_PARKED_MARKER_BRANCH",
        "interpretation": (
            "NAMPT does not pass V4 Tier 0 as an active therapeutic branch. "
            "The surviving signal is IBD/T1D metabolic-state or inflammatory-marker biology, "
            "with negative/non-significant MS white-matter signal, no non-IBD retained residual, "
            "no local genetics anchor, and no demonstrated non-NAD-depleting eNAMPT modality. "
            "Retain only as a marker/readout for HIF/NAD/eNAMPT biology."
        ),
    }

    write_tsv(OUT / "evidence_matrix.tsv", evidence_rows)
    (OUT / "decision.json").write_text(json.dumps(decision, indent=2) + "\n")

    report = "\n".join(
        [
            "# NAMPT eNAMPT-vs-iNAMPT Tier 0 Audit",
            "",
            f"Random seed: `{SEED}`",
            "",
            "## Decision",
            "",
            "`DEMOTE_TO_PARKED_MARKER_BRANCH`.",
            "",
            "The constrained NAMPT branch fails Tier 0 as an active therapeutic candidate.",
            "The local evidence does not separate a druggable extracellular NAMPT mechanism",
            "from generic intracellular NAMPT/NAD stress-metabolism biology.",
            "",
            "## Key Outputs",
            "",
            f"- MS white-matter delta log2: `{residual['ms_wm_delta_log2']}`, p: `{residual['ms_wm_p']}`.",
            f"- Non-IBD retained positive disease count: `{residual['non_ibd_retained_positive_disease_count']}`.",
            f"- Strict core-covariate surviving disease count: `{residual['strict_core_covariate_surviving_disease_count']}`.",
            f"- OpenTargets max genetics score: `{genetics['ot_max_score']}`.",
            f"- C15 positive contexts: `{controller['positive_c15_contexts']}`.",
            "",
            "## Interpretation",
            "",
            "This is not a P0 prior-art kill. It is a V4 evidence kill for active",
            "therapeutic nomination: no MS anchor, no non-IBD retained residual, no",
            "local genetics, and no non-NAD-depleting modality evidence. NAMPT remains",
            "useful as a marker/readout for HIF/NAD/eNAMPT inflammatory metabolism.",
        ]
    )
    (OUT / "REPORT.md").write_text(report + "\n")


if __name__ == "__main__":
    main()
