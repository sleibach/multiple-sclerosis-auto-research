#!/usr/bin/env python3
"""Wave120 strict EPHX2/sEH target-PD coherence closure audit."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "results_v3" / "wave120_ephx2_target_pd_coherence_closure"

DIRECT_RATIO = ROOT / "results_v3" / "wave74_ephx2_direct_ratio_audit" / "ephx2_direct_ratio_decision.tsv"
FINAL_DECISION = ROOT / "results_v3" / "wave74_ephx2_oxylipin_specificity" / "final_decision.tsv"
GENE_EVIDENCE = ROOT / "results_v3" / "wave74_ephx2_oxylipin_specificity" / "ephx2_gene_evidence.tsv"
MODULE_MARGINS = ROOT / "results_v3" / "wave74_ephx2_oxylipin_specificity" / "module_specificity_margins.tsv"
METABOLITE_STATS = ROOT / "results_v3" / "wave74_ephx2_oxylipin_specificity" / "metabolite_cross_disease_stats.tsv"
PRIOR_ART = ROOT / "subagents_v3" / "wave74c_prior_art_druggability_scout.md"


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def first_row(df: pd.DataFrame) -> dict[str, object]:
    return df.to_dict(orient="records")[0] if not df.empty else {}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    direct = read_tsv(DIRECT_RATIO)
    final = read_tsv(FINAL_DECISION)
    gene = read_tsv(GENE_EVIDENCE)
    margins = read_tsv(MODULE_MARGINS)
    metabolites = read_tsv(METABOLITE_STATS)
    prior_text = PRIOR_ART.read_text(encoding="utf-8") if PRIOR_ART.exists() else ""

    direct_row = first_row(direct)
    final_row = first_row(final)

    direct_ratio_available = (
        int(direct_row.get("direct_epoxide_diol_pairs", 0) or 0) > 0
        and int(direct_row.get("direct_ratio_supportive_tests", 0) or 0) > 0
    )
    target_level_ephx2_support = as_bool(final_row.get("target_level_ephx2_support", False))
    specificity_vs_generic_modules = as_bool(final_row.get("specificity_vs_generic_modules", False))
    independent_response_replication = as_bool(final_row.get("independent_response_replication", False))
    cross_disease_specific_biochemistry = as_bool(final_row.get("cross_disease_specific_biochemistry", False))
    prior_art_unblocked = "BLOCKED_BY_PRIOR_ART" not in prior_text

    gate_rows = pd.DataFrame(
        [
            {
                "gate": "direct_target_pd_ratio_available",
                "pass": direct_ratio_available,
                "observed": (
                    f"direct_epoxide_diol_pairs={direct_row.get('direct_epoxide_diol_pairs', '')}; "
                    f"direct_ratio_supportive_tests={direct_row.get('direct_ratio_supportive_tests', '')}"
                ),
                "required": "same-study paired epoxide/diol ratio support",
            },
            {
                "gate": "target_level_ephx2_support",
                "pass": target_level_ephx2_support,
                "observed": final_row.get("target_support_source_count", ""),
                "required": "expression/genetics/target-resolution support for EPHX2 itself",
            },
            {
                "gate": "specificity_vs_generic_lipid_inflammation",
                "pass": specificity_vs_generic_modules,
                "observed": final_row.get("specificity_pass_context_count", ""),
                "required": "EPHX2 axis beats generic lipid, inflammatory, and lysosomal APC comparators",
            },
            {
                "gate": "independent_response_replication",
                "pass": independent_response_replication,
                "observed": final_row.get("ephx2_response_module_support_count", ""),
                "required": "treatment response or perturbation evidence in an independent dataset",
            },
            {
                "gate": "cross_disease_specific_biochemistry",
                "pass": cross_disease_specific_biochemistry,
                "observed": final_row.get("specific_supportive_disease_count", ""),
                "required": "specific EPHX2 substrate/product class recurrence across diseases",
            },
            {
                "gate": "prior_art_unblocked",
                "pass": prior_art_unblocked,
                "observed": "BLOCKED_BY_PRIOR_ART" if not prior_art_unblocked else "not detected",
                "required": "no blocking broad autoimmune/MS/IBD sEH prior art for the same use",
            },
        ]
    )

    gate_pass_count = int(gate_rows["pass"].sum())
    branch_call = (
        "REOPEN_EPHX2_TARGET_PD_COHERENT"
        if gate_pass_count == len(gate_rows)
        else "NO_REOPEN_EPHX2_TARGET_PD_COHERENCE"
    )

    evidence_rows = []
    for name, frame in [
        ("direct_ratio_decision", direct),
        ("final_decision", final),
        ("gene_evidence", gene),
        ("module_specificity_margins", margins),
        ("metabolite_cross_disease_stats", metabolites),
    ]:
        evidence_rows.append(
            {
                "source": name,
                "rows": int(len(frame)),
                "supportive_rows": int(frame["support"].sum()) if "support" in frame.columns else "",
                "path": rel(
                    {
                        "direct_ratio_decision": DIRECT_RATIO,
                        "final_decision": FINAL_DECISION,
                        "gene_evidence": GENE_EVIDENCE,
                        "module_specificity_margins": MODULE_MARGINS,
                        "metabolite_cross_disease_stats": METABOLITE_STATS,
                    }[name]
                ),
            }
        )
    evidence = pd.DataFrame(evidence_rows)

    gate_rows.to_csv(OUT / "ephx2_target_pd_gates.tsv", sep="\t", index=False)
    evidence.to_csv(OUT / "ephx2_target_pd_evidence_inventory.tsv", sep="\t", index=False)

    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "branch_call": branch_call,
            "gate_pass_count": gate_pass_count,
            "gate_count": int(len(gate_rows)),
            "inputs": {
                "direct_ratio": rel(DIRECT_RATIO),
                "final_decision": rel(FINAL_DECISION),
                "gene_evidence": rel(GENE_EVIDENCE),
                "module_margins": rel(MODULE_MARGINS),
                "metabolite_stats": rel(METABOLITE_STATS),
                "prior_art": rel(PRIOR_ART),
            },
        },
    )

    report = f"""# Wave120 EPHX2/sEH Target-PD Coherence Closure

## Bottom Line

Branch call: `{branch_call}`.

EPHX2/sEH remains biologically and pharmacologically interesting, but this V3
route cannot be promoted because the available local evidence does not connect
target-level EPHX2, paired epoxy-fatty-acid/diol pharmacodynamics,
cross-disease specificity, and treatment-response behavior in one coherent
chain.

## Strict Gates

{markdown_table(gate_rows, max_rows=20)}

## Evidence Inventory

{markdown_table(evidence, max_rows=20)}

## Interpretation

This is a closure audit, not a claim that sEH biology is irrelevant to
autoimmunity. The rejected claim is narrower: the current V3 evidence is
insufficient for an EPHX2/sEH target nomination in the shared
lipid-lysosomal myeloid module, and prior art blocks broad autoimmune
repurposing without a new stratified or mechanistically distinct angle.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave120_ephx2_target_pd_coherence_closure.py")}`
- Output: `{rel(OUT / "ephx2_target_pd_gates.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
