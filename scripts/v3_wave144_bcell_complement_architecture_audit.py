#!/usr/bin/env python3
"""Wave144 B-cell/plasma-autoantibody/complement architecture audit."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT


SEED = 20260527
OUT = ROOT / "results_v3" / "wave144_bcell_complement_architecture_audit"

REPORTS = {
    "myasthenia_gravis": ROOT / "subagents_v3" / "myasthenia_gravis_dalton_report.md",
    "autoimmune_thyroid": ROOT / "subagents_v3" / "autoimmune_thyroid_dirac_report.md",
    "celiac": ROOT / "subagents_v3" / "celiac_plato_report.md",
    "pbc": ROOT / "subagents_v3" / "pbc_goodall_report.md",
}

TABLES = {
    "cfb_wave44": ROOT / "results_v3" / "wave44_cfb_complement_stratification_audit" / "summary.json",
    "cfb_report": ROOT / "results_v3" / "wave44_cfb_complement_stratification_audit" / "REPORT.md",
    "mg_module": ROOT / "results_v3" / "wave14_gse227835_myasthenia" / "gse227835_module_support_summary.tsv",
    "celiac_modules": ROOT / "results_v3" / "gse315138_celiac_marker" / "gse315138_donor_module_comparisons.tsv",
    "thyroid_modules": ROOT / "results_v3" / "gse248205_thyroid_spatial" / "gse248205_module_gene_contrasts.tsv",
}

AXES = {
    "anti_cd20_b_cell_depletion": ["CD20", "MS4A1", "B cell", "B-cell"],
    "baff_april_plasma_survival": ["BAFF", "APRIL", "TNFSF13B", "TNFRSF13B", "BCMA", "TNFRSF17"],
    "plasma_cell_cd38": ["plasma", "CD38", "plasmablast"],
    "classical_or_alternative_complement": ["complement", "C1q", "C1QA", "C3", "CFB", "MAC"],
    "disease_specific_antigen_entry": ["TSHR", "TG", "TPO", "TGM2", "HLA-DQ", "AChR", "autoantigen"],
    "hla_cd74_antigen_processing": ["HLA-II", "CD74", "CTSS", "IFI30", "antigen processing"],
}

PRIOR_OR_BLOCKER = {
    "anti_cd20_b_cell_depletion": "anti-CD20/B-cell depletion is established/prior-art in MS and other autoimmune diseases; not a novel cross-autoimmune target",
    "baff_april_plasma_survival": "BAFF/APRIL/BCMA plasma-cell survival is clinically crowded and disease-context dependent",
    "plasma_cell_cd38": "CD38/plasma-cell depletion has oncology/autoimmune precedent and broad humoral-immunity safety liabilities",
    "classical_or_alternative_complement": "CFB/complement route already failed Wave44 for MS anchor, target-resolved genetics, host-defense safety, and prior art",
    "disease_specific_antigen_entry": "strong biology is disease-specific antigen architecture, not a shared intervention node",
    "hla_cd74_antigen_processing": "HLA/CD74/antigen-processing route is host-defense and antigen-presentation prior blocked",
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() and path.stat().st_size else pd.DataFrame()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report_text = {k: text(v) for k, v in REPORTS.items()}
    cfb_report = text(TABLES["cfb_report"])
    local_tables = {k: read_tsv(v) for k, v in TABLES.items() if v.suffix == ".tsv"}

    rows = []
    for axis, terms in AXES.items():
        disease_hits = []
        term_hits = []
        for disease, body in report_text.items():
            body_l = body.lower()
            matched = [t for t in terms if t.lower() in body_l]
            if matched:
                disease_hits.append(disease)
                term_hits.extend(f"{disease}:{t}" for t in matched)

        local_table_hits = []
        for name, df in local_tables.items():
            if df.empty:
                continue
            blob = " ".join(df.astype(str).head(200).agg(" ".join, axis=1).tolist()).lower()
            matched = [t for t in terms if t.lower() in blob]
            if matched:
                local_table_hits.append(name)

        gates = {
            "reported_in_ge3_disease_architectures": len(set(disease_hits)) >= 3,
            "quantified_local_table_support": len(local_table_hits) >= 2,
            "ms_specific_target_anchor": axis == "anti_cd20_b_cell_depletion",
            "shared_single_intervention_node": axis
            in {"anti_cd20_b_cell_depletion", "baff_april_plasma_survival", "plasma_cell_cd38", "classical_or_alternative_complement"},
            "not_disease_specific_antigen": axis != "disease_specific_antigen_entry",
            "not_prior_or_safety_blocked": False,
        }
        call = "B_CELL_COMPLEMENT_SHARED_TARGET_CANDIDATE" if all(gates.values()) else "NO_BCELL_COMPLEMENT_SHARED_TARGET"
        if call.startswith("NO_") and gates["reported_in_ge3_disease_architectures"]:
            call = "DISEASE_ARCHITECTURE_ONLY"
        rows.append(
            {
                "axis": axis,
                "call": call,
                "pass_count": int(sum(gates.values())),
                "failed_gates": ";".join(k for k, v in gates.items() if not v),
                **gates,
                "disease_hit_count": len(set(disease_hits)),
                "disease_hits": ";".join(sorted(set(disease_hits))),
                "term_hits": ";".join(term_hits),
                "local_table_hits": ";".join(local_table_hits),
                "manual_blocker": PRIOR_OR_BLOCKER[axis],
            }
        )

    out = pd.DataFrame(rows).sort_values(["call", "pass_count", "disease_hit_count"], ascending=[True, False, False])
    out.to_csv(OUT / "bcell_complement_architecture_rank.tsv", sep="\t", index=False)

    cfb_failed = [
        line.strip("- ")
        for line in cfb_report.splitlines()
        if line.startswith("- no_") or line.startswith("- factor_") or line.startswith("- systemic_")
    ]
    summary = {
        "random_seed": SEED,
        "branch_call": "NO_BCELL_COMPLEMENT_SHARED_THERAPEUTIC_TARGET",
        "n_shared_target_candidates": int((out["call"] == "B_CELL_COMPLEMENT_SHARED_TARGET_CANDIDATE").sum()),
        "n_architecture_only_axes": int((out["call"] == "DISEASE_ARCHITECTURE_ONLY").sum()),
        "cfb_wave44_failed_gates": cfb_failed,
        "inputs": {
            **{k: str(v.relative_to(ROOT)) for k, v in REPORTS.items()},
            **{k: str(v.relative_to(ROOT)) for k, v in TABLES.items()},
        },
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    report = f"""# Wave144 B-Cell/Plasma/Complement Architecture Audit

## Bottom Line

Branch call: `{summary['branch_call']}`.

The humoral/complement axis recurs across disease-specialist reports, but as
disease architecture and prior-art therapeutic classes rather than a novel
shared target.

## Counts

- Shared target candidates: {summary['n_shared_target_candidates']}
- Architecture-only axes: {summary['n_architecture_only_axes']}

## Interpretation

MG, AITD, celiac, and PBC support antibody/B-cell, disease-specific antigen,
HLA/CD74, or complement biology in different ways. The shared intervention
classes are already crowded (`anti-CD20`, BAFF/APRIL/plasma-cell targeting,
CD38/plasma-cell depletion, complement inhibition), while the strongest
mechanistic chains are disease-specific antigen-entry routes. This does not
produce a V3 cross-autoimmune target.
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
