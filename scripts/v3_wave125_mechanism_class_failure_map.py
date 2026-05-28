#!/usr/bin/env python3
"""Wave125 mechanism-class failure map from Wave122 fresh scan."""

from __future__ import annotations

from collections import Counter, defaultdict

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "results_v3" / "wave125_mechanism_class_failure_map"

W122 = ROOT / "results_v3" / "wave122_fresh_breadth_target_scan" / "fresh_breadth_target_rank.tsv"
TOP_N = 300


CLASS_KEYWORDS = {
    "ros_host_defense": ["NCF", "CYBB", "CYBA", "NOX", "NADPH"],
    "chemokine_neutrophil": ["CXCL", "CCL", "CXCR", "CCR", "IL8"],
    "adhesion_matrix": ["ITGA", "ITGB", "VCAM", "ICAM", "SDC", "LIMS", "FMNL", "DIAPH", "NRCAM"],
    "ifn_antigen_processing": ["STAT", "IRF", "GBP", "IFI", "TAP", "PSMB", "HLA", "CIITA", "NLRC5"],
    "lysosomal_protease": ["CTS", "LIPA", "LAMP", "GBA", "HEXA", "HEXB", "GALC", "ASAH"],
    "lipid_apoe_apoc": ["APOC", "APOE", "LPL", "PLIN", "FABP", "ACSL"],
    "secreted_remodeling": ["CHI3", "MMP", "TIMP", "COL", "FN1", "SPARC"],
    "intracellular_housekeeping": ["BTF", "AQR", "PPIL", "RPL", "RPS", "CBX", "CRTAP"],
}


def classify_gene(gene: str, blocker: str) -> str:
    text = f"{gene} {blocker}".upper()
    for cls, terms in CLASS_KEYWORDS.items():
        if any(term in text for term in terms):
            return cls
    return "other"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rank = pd.read_csv(W122, sep="\t", low_memory=False)
    top = rank.head(TOP_N).copy()
    top["mechanism_class"] = top.apply(lambda r: classify_gene(str(r["gene"]), str(r.get("blocker_text", ""))), axis=1)
    top["failure_marker_only"] = (
        top["ms"].astype(bool)
        & top["broad_cell_state"].astype(bool)
        & ~top["genetics"].astype(bool)
        & ~top["perturbation_or_model"].astype(bool)
        & ~top["modality"].astype(bool)
    )
    top["failure_safety_or_prior"] = top["blocker_flag"].astype(bool)
    top["failure_no_causal_channel"] = ~top["genetics"].astype(bool) & ~top["perturbation_or_model"].astype(bool)
    top["failure_no_modality"] = ~top["modality"].astype(bool)
    top["failure_ms_not_fdr"] = top["ms"].astype(bool) & (top["ms_fdr"].astype(float) >= 0.10)
    top["failure_response_absent"] = ~top["response"].astype(bool)

    class_rows = []
    for cls, grp in top.groupby("mechanism_class"):
        class_rows.append(
            {
                "mechanism_class": cls,
                "n_top": int(len(grp)),
                "best_gene": grp.iloc[0]["gene"],
                "best_score": grp.iloc[0]["fresh_score"],
                "n_marker_only": int(grp["failure_marker_only"].sum()),
                "n_safety_or_prior": int(grp["failure_safety_or_prior"].sum()),
                "n_no_causal_channel": int(grp["failure_no_causal_channel"].sum()),
                "n_no_modality": int(grp["failure_no_modality"].sum()),
                "n_ms_not_fdr": int(grp["failure_ms_not_fdr"].sum()),
                "n_response_absent": int(grp["failure_response_absent"].sum()),
                "top_genes": ";".join(grp.head(10)["gene"].astype(str)),
            }
        )
    class_summary = pd.DataFrame(class_rows).sort_values(["best_score", "n_top"], ascending=[False, False])

    failure_counts = Counter()
    for col in [
        "failure_marker_only",
        "failure_safety_or_prior",
        "failure_no_causal_channel",
        "failure_no_modality",
        "failure_ms_not_fdr",
        "failure_response_absent",
    ]:
        failure_counts[col] = int(top[col].sum())
    failure_summary = pd.DataFrame(
        [{"failure_mode": k, "count": v, "fraction_top_n": v / len(top)} for k, v in failure_counts.items()]
    ).sort_values("count", ascending=False)

    pivot_rows = []
    for _, r in class_summary.iterrows():
        cls = r["mechanism_class"]
        if r["n_safety_or_prior"] > 0 and cls in {"ros_host_defense", "chemokine_neutrophil", "ifn_antigen_processing"}:
            recommendation = "avoid_direct_targeting; use as stratification/readout only"
        elif r["n_marker_only"] >= max(2, r["n_top"] // 4):
            recommendation = "requires perturbation data before reopening"
        elif r["n_no_modality"] >= max(2, r["n_top"] // 3):
            recommendation = "search upstream druggable regulator, not class member"
        elif r["n_no_causal_channel"] >= max(2, r["n_top"] // 3):
            recommendation = "seek genetics or perturb-seq evidence first"
        else:
            recommendation = "low_priority_manual_review"
        pivot_rows.append({**r.to_dict(), "pivot_recommendation": recommendation})
    pivot_summary = pd.DataFrame(pivot_rows)

    top.to_csv(OUT / "top_wave122_failure_annotations.tsv", sep="\t", index=False)
    class_summary.to_csv(OUT / "mechanism_class_failure_summary.tsv", sep="\t", index=False)
    failure_summary.to_csv(OUT / "failure_mode_summary.tsv", sep="\t", index=False)
    pivot_summary.to_csv(OUT / "pivot_recommendations.tsv", sep="\t", index=False)

    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "branch_call": "MECHANISM_FAILURE_MAP_COMPLETE",
            "top_n": TOP_N,
            "n_classes": int(len(class_summary)),
            "dominant_failure_mode": failure_summary.iloc[0]["failure_mode"],
            "dominant_failure_count": int(failure_summary.iloc[0]["count"]),
            "top_mechanism_class": class_summary.iloc[0]["mechanism_class"],
            "input": rel(W122),
        },
    )

    report = f"""# Wave125 Mechanism-Class Failure Map

## Bottom Line

Branch call: `MECHANISM_FAILURE_MAP_COMPLETE`.

This wave maps why the top {TOP_N} Wave122 candidates fail, so the next pivot is
based on failure structure rather than another single-gene rank.

## Failure Modes

{markdown_table(failure_summary, max_rows=20)}

## Mechanism Classes

{markdown_table(class_summary, max_rows=30)}

## Pivot Recommendations

{markdown_table(pivot_summary, max_rows=30)}

## Interpretation

If the dominant failure is marker-only recurrence or absence of causal/
perturbational channels, more expression ranking will not solve the problem.
The next useful pivot must add a new modality or explicitly search upstream
drugged regulators of the recurring marker classes.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave125_mechanism_class_failure_map.py")}`
- Output: `{rel(OUT / "mechanism_class_failure_summary.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
