#!/usr/bin/env python3
"""Rank V6 Tier -1 hypotheses for Tier 0 promotion attempts."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MINING = ROOT / "analysis" / "tier_minus_1_exploration" / "v6_initial_pattern_mining"
OUT = ROOT / "analysis" / "tier_minus_1_exploration" / "v6_promotion_ranking"


HYPOTHESES = [
    {
        "id": "HYP_V6_007",
        "name": "SLE pregnancy HLA-II / monocyte-CD64 decoupling",
        "patterns": ["GSE108497 monocyte_cd64", "GSE108497 hla_ii", "GSE108497 mif_cd74"],
        "independent_support": 2,
        "specificity": 3,
        "testability": 3,
        "first_tier0_test": "Test the same decoupling in GSE235508 RA/SLE timecourse and separate uncomplicated/complicated outcome where available.",
    },
    {
        "id": "HYP_V6_006",
        "name": "Anti-TNF IFN/APC-down and HLA-II remodeling",
        "patterns": ["GSE282122 major Mono_macro ifn_apc raw", "GSE282122 major Mono_macro hla_ii_without_cd74 raw", "GSE282122 major DC hla_ii_without_cd74 raw"],
        "independent_support": 2,
        "specificity": 3,
        "testability": 3,
        "first_tier0_test": "Search and test an independent treated IBD/RA myeloid dataset with response labels using separated IFN/APC, HLA-II, and receptor-only components.",
    },
    {
        "id": "HYP_V6_001",
        "name": "MS pregnancy erythroid/platelet/neutrophil axis",
        "patterns": ["GSE17410 month9_vs_pre erythroid_marker", "GSE17410 month9_vs_pre platelet_marker", "GSE17410 month9_vs_pre neutrophil_marker"],
        "independent_support": 1,
        "specificity": 2,
        "testability": 2,
        "first_tier0_test": "Check whether the module appears in GSE235508/healthy pregnancy as generic pregnancy physiology or is MS-skewed; seek postpartum relapse linkage.",
    },
    {
        "id": "HYP_V6_002",
        "name": "MS pregnancy pDC-depletion / ISG-source switch",
        "patterns": ["GSE17410 month9_vs_pre isg_only", "GSE17410 month9_vs_pre pdc_marker", "GSE17410 residual isg_only"],
        "independent_support": 1,
        "specificity": 3,
        "testability": 2,
        "first_tier0_test": "Use single-cell pregnancy references or sorted-cell datasets to identify non-pDC ISG source.",
    },
    {
        "id": "HYP_V6_004",
        "name": "APC-state controller upstream of CD74",
        "patterns": ["GSE282122 major Mono_macro ifn_apc raw", "GSE282122 major DC ifn_apc raw"],
        "independent_support": 2,
        "specificity": 2,
        "testability": 3,
        "first_tier0_test": "Rank perturbations that change CD74/HLA-II via IFN/APC and compare with CIITA/Mediator selectivity tables.",
    },
    {
        "id": "HYP_V6_003",
        "name": "Postpartum T-cell trafficking readiness",
        "patterns": ["E-MTAB-12260 trafficking"],
        "independent_support": 1,
        "specificity": 3,
        "testability": 2,
        "first_tier0_test": "Test trafficking module in GSE235508 postpartum samples and search MS relapse/postpartum datasets.",
    },
    {
        "id": "HYP_V6_005",
        "name": "OPC CD74 lesion-stress state",
        "patterns": ["MS pseudobulk OPC cd74_alone"],
        "independent_support": 1,
        "specificity": 3,
        "testability": 2,
        "first_tier0_test": "Validate in a single-nucleus lesion atlas with OPC/oligodendrocyte annotations.",
    },
]


def evidence_score(flagged: pd.DataFrame, patterns: list[str]) -> tuple[int, float, float]:
    mask = pd.Series(False, index=flagged.index)
    for pattern in patterns:
        mask |= flagged["pattern"].str.contains(pattern, case=False, regex=False, na=False)
    subset = flagged[mask]
    if subset.empty:
        return 0, 1.0, 0.0
    min_p = subset["p_value"].dropna().min()
    max_g = subset["hedges_g"].abs().dropna().max()
    return int(len(subset)), float(min_p) if pd.notna(min_p) else 1.0, float(max_g) if pd.notna(max_g) else 0.0


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    flagged = pd.read_csv(MINING / "tier_minus_1_flagged_patterns.tsv", sep="\t")
    rows = []
    for hyp in HYPOTHESES:
        n, min_p, max_abs_g = evidence_score(flagged, hyp["patterns"])
        loose_evidence = min(4, n) + (1 if min_p < 0.01 else 0) + (1 if max_abs_g > 1.0 else 0)
        score = loose_evidence + hyp["independent_support"] + hyp["specificity"] + hyp["testability"]
        rows.append(
            {
                "hypothesis_id": hyp["id"],
                "name": hyp["name"],
                "n_matching_flagged_patterns": n,
                "min_p": min_p,
                "max_abs_hedges_g": max_abs_g,
                "loose_evidence_score": loose_evidence,
                "independent_support_score": hyp["independent_support"],
                "specificity_score": hyp["specificity"],
                "testability_score": hyp["testability"],
                "total_priority_score": score,
                "first_tier0_test": hyp["first_tier0_test"],
            }
        )
    df = pd.DataFrame(rows).sort_values(
        ["total_priority_score", "min_p"], ascending=[False, True]
    )
    df.to_csv(OUT / "promotion_ranking.tsv", sep="\t", index=False)
    summary = {
        "top_hypotheses": df.head(5).to_dict(orient="records"),
        "scoring": "loose evidence + independent support + specificity + testability; exploration ranking only",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = [
        "# V6 Tier -1 Promotion Ranking",
        "",
        "This ranking is for allocating V6 Tier 0 attempts. It is not a validation",
        "or therapeutic-priority score.",
        "",
        "| Rank | Hypothesis | Score | Matching patterns | Best p | Max abs(g) | First Tier 0 test |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for i, r in enumerate(df.itertuples(index=False), start=1):
        lines.append(
            f"| {i} | `{r.hypothesis_id}` {r.name} | {r.total_priority_score} | "
            f"{r.n_matching_flagged_patterns} | {r.min_p:.3g} | {r.max_abs_hedges_g:.3g} | "
            f"{r.first_tier0_test} |"
        )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
