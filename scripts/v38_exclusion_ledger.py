#!/usr/bin/env python3
"""Write a conservative V38 exclusion/non-replication ledger."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v38_exclusion_ledger"
OUT.mkdir(parents=True, exist_ok=True)


ROWS = [
    {
        "exclusion": "Baseline IFN/APC is not a valid general fallback stratifier",
        "scope": "cross-disease treatment response",
        "strength": "negative_established",
        "artifact": "docs/findings/KILL_HYP_V6_006.md",
        "decision_value": "Do not substitute baseline IFN/APC for early on-treatment delta.",
    },
    {
        "exclusion": "V22 scalar is not a broad cross-therapy response rule",
        "scope": "MS/autoimmune treatment response",
        "strength": "negative_established",
        "artifact": "docs/findings/FINDING_V22.md; analysis/v23_apc_hla_monitoring/v23_pooled_locked_rule_summary.tsv",
        "decision_value": "Do not transfer the rule to fingolimod, adalimumab, or arbitrary DMTs without direct validation.",
    },
    {
        "exclusion": "V22 scalar is not a calibrated clinical threshold",
        "scope": "clinical utility",
        "strength": "negative_established",
        "artifact": "analysis/v31_multi_lineage_review/v31_cross_cohort_score_grounding.tsv; analysis/v38_adversarial_monitoring/grounded_inversion_results.tsv",
        "decision_value": "Use only rank/direction validation until a fresh cohort calibrates a threshold.",
    },
    {
        "exclusion": "Glucocorticoid/steroid signature does not explain the bounded scalar",
        "scope": "treatment-response confounding",
        "strength": "supported_exclusion",
        "artifact": "docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md",
        "decision_value": "Steroid control remains required, but current data do not justify killing the scalar as steroid artifact.",
    },
    {
        "exclusion": "Simple marker-level cell-composition shift does not explain the bounded scalar",
        "scope": "treatment-response confounding",
        "strength": "supported_exclusion",
        "artifact": "docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md",
        "decision_value": "Future validation still needs composition adjustment, but current data do not reduce the scalar to composition.",
    },
    {
        "exclusion": "Receptor-only CD74/CD44/CXCR4 does not dominate the scalar",
        "scope": "treatment-response mechanism",
        "strength": "negative_established",
        "artifact": "docs/workups/treatment_response/ROBUSTNESS_MAP_V28.md",
        "decision_value": "Do not replace the scalar with receptor-only readout.",
    },
    {
        "exclusion": "Coupled/dynamic/flexible ML variants do not improve over the scalar",
        "scope": "treatment-response modeling",
        "strength": "negative_established",
        "artifact": "docs/workups/treatment_response/ROBUSTNESS_MAP_V28.md; analysis/v27_coupled_axis/v27_scalar_vs_coupled_metrics.tsv",
        "decision_value": "Do not lock a successor rule from held data.",
    },
    {
        "exclusion": "A broad immune-state simulator is not validated from current data",
        "scope": "in-silico modeling",
        "strength": "negative_established",
        "artifact": "docs/workups/treatment_response/MODEL_CARD_V25.md; analysis/v25_immune_state_model/model_validation_summary.json",
        "decision_value": "Do not use the simulator for patient response, single-cell simulation, or genetics-direction claims.",
    },
    {
        "exclusion": "No load-bearing invariant was established",
        "scope": "deep structure",
        "strength": "negative_established",
        "artifact": "docs/findings/DEEP_STRUCTURE_V26.md",
        "decision_value": "Do not target a claimed invariant without new evidence.",
    },
    {
        "exclusion": "PTGER4 is not a clean MS-UC transfer target",
        "scope": "shared genetics target transfer",
        "strength": "negative_established",
        "artifact": "docs/workups/genetics/GENETICS_EQTL_WORKUP_V16.md; docs/history/LEAD_INVENTORY_V29.md",
        "decision_value": "Do not pursue naive PTGER4 agonist/antagonist transfer without signal-specific direction data.",
    },
    {
        "exclusion": "MHC/HLA overlap is not simple shared causal biology",
        "scope": "shared genetics interpretation",
        "strength": "negative_established",
        "artifact": "analysis/v14_locus_landscape/REPORT.md; analysis/v14_susie_coloc/REPORT.md",
        "decision_value": "Do not infer shared causal variant from HLA overlap alone.",
    },
    {
        "exclusion": "EBV/IFN APC imprint is not EBV-specific in current data",
        "scope": "infectious-trigger exploratory biology",
        "strength": "negative_established",
        "artifact": "docs/history/HYPOTHESIS_SLATE_V35.md; docs/history/HYPOTHESIS_SLATE_V36.md",
        "decision_value": "Do not revive without EBV-stratified B-cell/APC data beyond random-module controls.",
    },
    {
        "exclusion": "Complement/lipid progressive axis is not supported as a combined axis",
        "scope": "progressive/lesion biology",
        "strength": "negative_established",
        "artifact": "docs/history/HYPOTHESIS_SLATE_V35.md; docs/history/HYPOTHESIS_SLATE_V36.md",
        "decision_value": "Do not pursue without donor-aware lesion-rim spatial lipid/complement data.",
    },
    {
        "exclusion": "NAMPT/eNAMPT is not reactivated as an MS target",
        "scope": "target nomination",
        "strength": "negative_established",
        "artifact": "docs/history/LEAD_INVENTORY_V29.md",
        "decision_value": "Use NAMPT/HIF/glycolysis as covariate/context, not target nomination.",
    },
    {
        "exclusion": "REL/PUS10/USP34 chr2 is not a current shared-locus lead",
        "scope": "genetics colocalization",
        "strength": "negative_established",
        "artifact": "docs/history/LEAD_SLATE_V21.md",
        "decision_value": "Expression/QTL context cannot rescue a failed disease-coloc screen.",
    },
    {
        "exclusion": "ZFP36L1 chr14 is not robust enough for lead status",
        "scope": "genetics colocalization",
        "strength": "data_gated_not_established",
        "artifact": "docs/history/LEAD_SLATE_V21.md",
        "decision_value": "Park until robust disease coloc and allele-aligned QTL direction exist.",
    },
]


def main() -> None:
    table = pd.DataFrame(ROWS)
    table.to_csv(OUT / "exclusion_nonreplication_ledger.tsv", sep="\t", index=False)
    counts = table.groupby(["strength", "scope"]).size().reset_index(name="n")
    counts.to_csv(OUT / "exclusion_counts.tsv", sep="\t", index=False)
    summary = {
        "n_exclusions": len(table),
        "strength_counts": table["strength"].value_counts().to_dict(),
        "scope_counts": table["scope"].value_counts().to_dict(),
        "overall_verdict": (
            "The strongest unpublishable result is a decision ledger: many attractive "
            "directions are not supported as targets/rules under current evidence, even "
            "though some remain biologically relevant context."
        ),
    }
    (OUT / "exclusion_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
