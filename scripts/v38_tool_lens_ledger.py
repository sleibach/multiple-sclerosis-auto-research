#!/usr/bin/env python3
"""Summarize V38 model/RPT lens contribution versus grounded evidence."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "analysis/v38_tool_lens_ledger"


ROWS = [
    {
        "lens": "RPT",
        "artifact": "analysis/v38_rpt_structural_mining/v38_rpt_grounded_summary.json",
        "proposal_or_signal": "Masked V37 action-class predictions over scored findings table.",
        "grounded_followup": "Compared RPT predictions to artifact-derived V37 action classes.",
        "grounded_result": "Matched 5/6; single contradiction treated bounded scalar as data-gated rather than external-validation priority.",
        "evidence_upgrade": "none",
        "actual_value": "Sharpened wording: scalar priority is operational/clinical, not structurally exceptional.",
    },
    {
        "lens": "Claude",
        "artifact": "analysis/v38_model_proposal_pass/claude_remaining_tests.json",
        "proposal_or_signal": "Proposed tone-stripped residual scalar, failure-vs-fragility concordance, and layer-label permutation tests.",
        "grounded_followup": "Implemented tone-residual scalar test and failure-vs-fragility concordance; also ran layer heterogeneity null.",
        "grounded_result": "Tone-residual scalar AUC 0.844 vs broad-tone prediction AUC 0.589; maps complementary; heterogeneity count not exceptional.",
        "evidence_upgrade": "none_new_rule",
        "actual_value": "Generated concrete adversarial tests that narrowed artifact interpretations.",
    },
    {
        "lens": "Gemini",
        "artifact": "analysis/v38_model_proposal_pass/gemini_remaining_tests.json",
        "proposal_or_signal": "Proposed fragility-failure resonance, exclusionary override cascade, scalar-APC gating analysis.",
        "grounded_followup": "Grounded the overlapping fragility-failure resonance via gate-level concordance; other proposals were too abstract for current tables.",
        "grounded_result": "Concordance showed V38 and V36 maps complementary, not redundant.",
        "evidence_upgrade": "none",
        "actual_value": "Converged on the failure/fragility comparison priority; less concrete than Claude in this pass.",
    },
    {
        "lens": "Agent-native deterministic scripts",
        "artifact": "scripts/v38_*.py",
        "proposal_or_signal": "Direct adversarial and unconventional tests from committed project artifacts.",
        "grounded_followup": "All V38 core outputs: inversions, ledgers, nulls, residualization, and delta table.",
        "grounded_result": "Produced all evidence-bearing V38 results.",
        "evidence_upgrade": "source_of_evidence",
        "actual_value": "Only real-data scripts counted as evidence; model/RPT output only selected or sharpened tests.",
    },
]


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    with (OUTDIR / "tool_lens_contribution_ledger.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ROWS[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(ROWS)
    summary = {
        "n_lenses": len(ROWS),
        "model_or_rpt_evidence_upgrades": 0,
        "model_spend_report": "SAP AI Core client does not expose per-call spend in local outputs; usage was limited to V38 prompt calls and smoke-tested deployments.",
        "interpretation": (
            "RPT and models added value by proposing or prioritizing adversarial "
            "tests, but no model/RPT output was treated as evidence and no lens "
            "alone upgraded a finding."
        ),
    }
    with (OUTDIR / "tool_lens_contribution_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2)


if __name__ == "__main__":
    main()
