#!/usr/bin/env python3
"""Wave156: ELR+ chemokine intervention audit after CUX1 demotion."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


SEED = 20260527
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave156_elr_chemokine_intervention_audit"
OUT.mkdir(parents=True, exist_ok=True)

GENES = ["CXCL1", "CXCL2", "CXCL3", "CXCL5", "CXCL8"]


def read_optional(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path, sep="\t")
    return pd.DataFrame()


def main() -> None:
    wave155 = read_optional(ROOT / "phases/v3/results" / "wave155_cux1_gene_specificity_vs_stat" / "gene_specificity_summary.tsv")
    wave21 = read_optional(ROOT / "phases/v3/results" / "wave21_residual_druggability_scan" / "wave21_residual_druggability_rank.tsv")
    wave71 = read_optional(ROOT / "phases/v3/results" / "wave71_global_survivor_meta_rank" / "global_survivor_meta_rank.tsv")
    wave103 = read_optional(ROOT / "phases/v3/results" / "wave103_intervention_first_successor_triage" / "intervention_first_successor_rank.tsv")

    rows = []
    for gene in GENES:
        r155 = wave155[wave155["gene"] == gene] if not wave155.empty else pd.DataFrame()
        r21 = wave21[wave21["gene"] == gene] if "gene" in wave21.columns else pd.DataFrame()
        r71 = wave71[wave71["gene"] == gene] if "gene" in wave71.columns else pd.DataFrame()
        r103 = wave103[wave103["gene"] == gene] if "gene" in wave103.columns else pd.DataFrame()
        cux1_contexts = int(r155["n_cux1_selective_nominal"].iloc[0]) if not r155.empty else 0
        cux1_suppressed = int(r155["n_cux1_nominal_suppressed"].iloc[0]) if not r155.empty else 0
        blockers = []
        if not r21.empty:
            blockers.append(str(r21.get("manual_or_prior_blocker", pd.Series([""])).iloc[0]))
            blockers.append(str(r21.get("failure_reason", pd.Series([""])).iloc[0]))
            blockers.append(str(r21.get("decision", pd.Series([""])).iloc[0]))
        if not r71.empty:
            blockers.append(str(r71.get("decision", pd.Series([""])).iloc[0]))
            blockers.append(str(r71.get("blockers", pd.Series([""])).iloc[0]))
            blockers.append(str(r71.get("failure_reason", pd.Series([""])).iloc[0]))
        if not r103.empty:
            blockers.append(str(r103.get("strict_branch", pd.Series([""])).iloc[0]))
            blockers.append(str(r103.get("manual_or_prior_blocker", pd.Series([""])).iloc[0]))
            blockers.append(str(r103.get("route_blockers", pd.Series([""])).iloc[0]))
        blocker_text = " | ".join(b for b in blockers if b and b != "nan")
        has_cux1_signal = cux1_contexts > 0 or cux1_suppressed > 0
        prior_or_class_blocked = any(
            token in blocker_text.lower()
            for token in [
                "generic inflammatory chemokine",
                "generic_neutrophil",
                "prior",
                "no_target_resolved_coloc_or_mr",
                "cannot anchor target causality",
                "does not pass broad genetics",
                "no_go_expression_or_class_only",
                "no_go_causal_proxy",
                "no_strong_ms_anchor",
            ]
        )
        promoted = bool(has_cux1_signal and not prior_or_class_blocked)
        rows.append(
            {
                "gene": gene,
                "cux1_nominal_suppressed_contexts": cux1_suppressed,
                "cux1_selective_nominal_contexts": cux1_contexts,
                "local_prior_blocker_text": blocker_text,
                "has_cux1_nonstat_signal": has_cux1_signal,
                "prior_or_class_blocked": prior_or_class_blocked,
                "promote_as_intervention": promoted,
            }
        )
    audit = pd.DataFrame(rows)
    audit.to_csv(OUT / "elr_chemokine_intervention_audit.tsv", sep="\t", index=False)
    promoted = audit[audit["promote_as_intervention"]]
    branch = "ELR_CHEMOKINE_INTERVENTION_PROMOTABLE" if len(promoted) else "NO_ELR_CHEMOKINE_INTERVENTION_PROMOTION"
    summary = {
        "branch_call": branch,
        "random_seed": SEED,
        "genes_audited": GENES,
        "n_promoted": int(len(promoted)),
        "interpretation": "CUX1-selective ELR chemokine suppression is real as an in-silico state signal, but local prior/druggability/genetic/MS-anchor audits block direct intervention promotion.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUT / "REPORT.md").write_text(
        "# Wave156 ELR+ Chemokine Intervention Audit\n\n"
        f"Branch call: `{branch}`.\n\n"
        "This wave asks whether the CUX1-selective ELR+ chemokine subset can be promoted as a "
        "therapeutic intervention point. It integrates Wave155 with prior local druggability, "
        "global survivor, and intervention-first audits.\n"
    )


if __name__ == "__main__":
    main()
