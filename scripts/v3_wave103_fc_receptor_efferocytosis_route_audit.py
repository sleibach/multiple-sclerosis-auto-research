#!/usr/bin/env python3
"""Wave103 Fc/FcRn/efferocytosis intervention-route audit.

The accessible-marker branch failed residualization. This wave tests a more
intervention-first route: Fc receptors, FcRn, and efferocytosis regulators.

Rationale:
- Wave37 provides real CRISPR screen evidence for some genes where KO enhances
  efferocytosis.
- FcRn and Fc receptor biology is druggable or biologic-accessible.
- The route is cross-autoimmune plausible, but safety, direction, prior art,
  and MS/module anchoring are likely blockers.

This script is a forcing audit, not a target claim.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave103_fc_receptor_efferocytosis_route_audit"

W37 = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W34 = ROOT / "phases/v3/results" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv"
W55 = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W62 = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W81 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
BROAD = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
MS_SIG = ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv"

CANDIDATES = [
    "FCGRT",
    "FCGR2A",
    "FCGR2B",
    "FCGR3A",
    "FCGR3B",
    "FCGR1A",
    "FCER1G",
    "DAB2",
    "CD9",
    "MERTK",
    "AXL",
    "TYROBP",
    "PDCD6IP",
    "TSC1",
    "RYK",
]

MANUAL = {
    "FCGRT": {
        "route": "FcRn blockade to reduce pathogenic IgG/immune-complex recycling and lysosomal Fc load",
        "modality": "approved/clinical biologics and Fc fragments exist for FcRn blockade",
        "manual_modality_ready": True,
        "manual_direction_blocked": False,
        "manual_prior_blocked": True,
        "manual_safety_blocker": "IgG lowering infection and humoral-immunity risk; MS/CNS compartment delivery uncertain",
    },
    "FCGR2A": {
        "route": "activating Fc-gamma receptor tuning",
        "modality": "antibody-accessible receptor but activation/inhibition selectivity is difficult",
        "manual_modality_ready": True,
        "manual_direction_blocked": True,
        "manual_prior_blocked": True,
        "manual_safety_blocker": "activating Fc receptor host-defense and immune-complex safety blocker",
    },
    "FCGR2B": {
        "route": "inhibitory Fc-gamma receptor agonism/restoration",
        "modality": "agonist biologic concept possible but receptor-family selectivity is difficult",
        "manual_modality_ready": True,
        "manual_direction_blocked": True,
        "manual_prior_blocked": False,
        "manual_safety_blocker": "Fc receptor balance and B-cell/myeloid immunosuppression risk",
    },
    "FCGR3A": {
        "route": "activating Fc-gamma receptor tuning",
        "modality": "antibody-accessible but selective safe anti-inflammatory direction is unresolved",
        "manual_modality_ready": True,
        "manual_direction_blocked": True,
        "manual_prior_blocked": True,
        "manual_safety_blocker": "NK/myeloid effector biology and host-defense risk",
    },
    "FCGR3B": {
        "route": "neutrophil Fc-gamma receptor tuning",
        "modality": "antibody-accessible but neutrophil biology creates safety and selectivity blockers",
        "manual_modality_ready": True,
        "manual_direction_blocked": True,
        "manual_prior_blocked": True,
        "manual_safety_blocker": "neutrophil immune-complex clearance and infection risk",
    },
    "FCGR1A": {
        "route": "high-affinity activating Fc receptor tuning",
        "modality": "antibody-accessible but high host-defense risk",
        "manual_modality_ready": True,
        "manual_direction_blocked": True,
        "manual_prior_blocked": True,
        "manual_safety_blocker": "macrophage activation and host-defense risk",
    },
    "FCER1G": {
        "route": "Fc receptor gamma-chain signaling adapter",
        "modality": "intracellular adaptor; no selective tissue-safe modality",
        "manual_modality_ready": False,
        "manual_direction_blocked": True,
        "manual_prior_blocked": True,
        "manual_safety_blocker": "shared Fc receptor signaling adapter with broad innate immune effects",
    },
    "DAB2": {
        "route": "endocytic/efferocytosis negative-regulator modulation",
        "modality": "intracellular adaptor; no clean selective modality",
        "manual_modality_ready": False,
        "manual_direction_blocked": False,
        "manual_prior_blocked": False,
        "manual_safety_blocker": "broad endocytosis, platelet, and tumor-biology liabilities",
    },
    "CD9": {
        "route": "tetraspanin membrane microdomain/efferocytosis tuning",
        "modality": "surface biologic possible but tetraspanin selectivity and direction are poor",
        "manual_modality_ready": True,
        "manual_direction_blocked": True,
        "manual_prior_blocked": False,
        "manual_safety_blocker": "ubiquitous tetraspanin and exosome biology",
    },
    "MERTK": {
        "route": "TAM receptor agonism to improve debris clearance/resolution",
        "modality": "agonist antibody/ligand concepts possible; inhibitor precedent is opposite direction",
        "manual_modality_ready": True,
        "manual_direction_blocked": True,
        "manual_prior_blocked": True,
        "manual_safety_blocker": "oncology, immune tolerance, and receptor agonism-direction blockers",
    },
    "AXL": {
        "route": "TAM receptor tuning",
        "modality": "small-molecule inhibitors exist but likely opposite of desired resolution direction",
        "manual_modality_ready": True,
        "manual_direction_blocked": True,
        "manual_prior_blocked": True,
        "manual_safety_blocker": "oncology/infection biology and wrong-direction inhibitor precedent",
    },
    "TYROBP": {
        "route": "DAP12 Fc/myeloid signaling adapter",
        "modality": "intracellular adapter; no clean selective modality",
        "manual_modality_ready": False,
        "manual_direction_blocked": True,
        "manual_prior_blocked": True,
        "manual_safety_blocker": "shared innate immune signaling adapter",
    },
    "PDCD6IP": {
        "route": "ALIX/endosomal trafficking-efferocytosis regulator",
        "modality": "intracellular trafficking protein; no clean autoimmune modality",
        "manual_modality_ready": False,
        "manual_direction_blocked": False,
        "manual_prior_blocked": False,
        "manual_safety_blocker": "broad endosomal and exosome biology",
    },
    "TSC1": {
        "route": "mTOR/autophagy/efferocytosis tuning",
        "modality": "pathway drugs exist but target-specific TSC1 modulation is not feasible",
        "manual_modality_ready": False,
        "manual_direction_blocked": True,
        "manual_prior_blocked": True,
        "manual_safety_blocker": "mTOR pathway pleiotropy and prior-art saturation",
    },
    "RYK": {
        "route": "Wnt-related efferocytosis screen hit",
        "modality": "surface receptor but autoimmune direction and selectivity unclear",
        "manual_modality_ready": True,
        "manual_direction_blocked": True,
        "manual_prior_blocked": False,
        "manual_safety_blocker": "developmental/Wnt-pathway pleiotropy",
    },
}


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value)


def num(value: Any, default: float = math.nan) -> float:
    try:
        if pd.isna(value):
            return default
        out = float(value)
        return out if math.isfinite(out) else default
    except (TypeError, ValueError):
        return default


def first(df: pd.DataFrame, gene: str, col: str = "gene") -> pd.Series | None:
    if df.empty or col not in df.columns:
        return None
    sub = df[df[col].astype(str).str.upper().eq(gene.upper())]
    if sub.empty:
        return None
    return sub.iloc[0]


def collect() -> pd.DataFrame:
    w37 = read_tsv(W37)
    w34 = read_tsv(W34)
    w55 = read_tsv(W55)
    w62 = read_tsv(W62)
    w81 = read_tsv(W81)
    broad = read_tsv(BROAD)
    ms = read_tsv(MS_SIG)
    rows: list[dict[str, Any]] = []
    for gene in CANDIDATES:
        manual = MANUAL[gene]
        r37 = first(w37, gene, "gene_symbol")
        r34 = first(w34, gene)
        r55 = first(w55, gene)
        r62 = first(w62, gene)
        r81 = first(w81, gene)
        rb = first(broad, gene)
        rms = first(ms, gene)
        rows.append(
            {
                "gene": gene,
                **manual,
                "wave37_screen_call": clean(r37.get("screen_call")) if r37 is not None else "",
                "wave37_contrast_lfc": num(r37.get("median_efficient_minus_noneater_lfc")) if r37 is not None else math.nan,
                "wave37_contrast_fdr": num(r37.get("contrast_fdr"), 1.0) if r37 is not None else 1.0,
                "wave37_efficient_consistent_positive": bool(r37.get("efficient_consistent_positive")) if r37 is not None else False,
                "wave81_call": clean(r81.get("wave81_call")) if r81 is not None else "",
                "wave81_direct_perturbation": num(r81.get("direct_perturbation"), 0.0) if r81 is not None else 0.0,
                "wave81_foundation_model_support": num(r81.get("foundation_model_support"), 0.0) if r81 is not None else 0.0,
                "wave81_blocker": clean(r81.get("blocker")) if r81 is not None else "",
                "wave34_call": clean(r34.get("wave34_call")) if r34 is not None else "",
                "wave34_gwas_trait_count": num(r34.get("gwas_catalog_trait_count"), 0.0) if r34 is not None else 0.0,
                "wave34_local_positive_disease_count": num(r34.get("local_positive_disease_count"), 0.0) if r34 is not None else 0.0,
                "wave55_genetic_diseases_ge_0_25": num(r55.get("genetic_diseases_ge_0_25"), 0.0) if r55 is not None else 0.0,
                "wave55_genetic_diseases": clean(r55.get("genetic_diseases")) if r55 is not None else "",
                "wave62_call": clean(r62.get("wave62_call")) if r62 is not None else "",
                "wave62_manual_blocker": clean(r62.get("manual_blocker")) if r62 is not None else "",
                "wave62_strong_l2g_disease_count": num(r62.get("strong_l2g_disease_count"), 0.0) if r62 is not None else 0.0,
                "wave62_strong_qtl_coloc_disease_count": num(r62.get("strong_qtl_coloc_disease_count"), 0.0) if r62 is not None else 0.0,
                "wave62_ms_max_l2g_score": num(r62.get("ms_max_l2g_score"), 0.0) if r62 is not None else 0.0,
                "broad_positive_disease_count": num(rb.get("positive_disease_count"), 0.0) if rb is not None else 0.0,
                "broad_negative_disease_count": num(rb.get("negative_disease_count"), 0.0) if rb is not None else 0.0,
                "broad_positive_diseases": clean(rb.get("positive_diseases")) if rb is not None else "",
                "broad_negative_diseases": clean(rb.get("negative_diseases")) if rb is not None else "",
                "ms_delta_log2": num(rms.get("delta_log2")) if rms is not None else math.nan,
                "ms_p": num(rms.get("p"), 1.0) if rms is not None else 1.0,
                "ms_fdr": num(rms.get("fdr"), 1.0) if rms is not None else 1.0,
            }
        )
    return pd.DataFrame(rows)


def add_gates(rank: pd.DataFrame) -> pd.DataFrame:
    rank = rank.copy()
    rank["gate_real_efferocytosis_perturbation"] = rank["wave37_screen_call"].str.contains(
        "KO_ENHANCES_EFFEROCYTOSIS", na=False
    ) | (rank["wave81_direct_perturbation"] > 0)
    rank["gate_ms_anchor"] = (rank["ms_delta_log2"] > 0.20) & (rank["ms_p"] < 0.10)
    rank["gate_cross_disease_expression"] = (rank["broad_positive_disease_count"] >= 3) & (
        rank["broad_negative_disease_count"] <= 1
    )
    rank["gate_genetic_breadth"] = (
        (rank["wave55_genetic_diseases_ge_0_25"] >= 4)
        | (rank["wave34_gwas_trait_count"] >= 8)
        | (rank["wave62_strong_l2g_disease_count"] >= 3)
        | (rank["wave62_strong_qtl_coloc_disease_count"] >= 3)
    )
    rank["gate_target_resolved_ms"] = rank["wave62_ms_max_l2g_score"] >= 0.5
    rank["gate_modality_ready"] = rank["manual_modality_ready"]
    rank["gate_direction_clear"] = ~rank["manual_direction_blocked"]
    rank["gate_prior_not_blocked"] = ~rank["manual_prior_blocked"]
    rank["gate_no_fc_safety_blocker"] = ~rank["manual_safety_blocker"].str.contains(
        "host-defense|infection|immune-complex|IgG lowering|pleiotropy|ubiquitous|shared",
        case=False,
        na=False,
    )
    rank["wave103_gate_count"] = rank[
        [
            "gate_real_efferocytosis_perturbation",
            "gate_ms_anchor",
            "gate_cross_disease_expression",
            "gate_genetic_breadth",
            "gate_target_resolved_ms",
            "gate_modality_ready",
            "gate_direction_clear",
            "gate_prior_not_blocked",
            "gate_no_fc_safety_blocker",
        ]
    ].sum(axis=1)
    rank["wave103_score"] = (
        2 * rank["wave103_gate_count"]
        + rank["wave37_contrast_lfc"].fillna(0).clip(lower=0, upper=2)
        + rank["broad_positive_disease_count"].fillna(0).clip(upper=5)
        + rank["wave55_genetic_diseases_ge_0_25"].fillna(0).clip(upper=5)
        + rank["wave62_strong_qtl_coloc_disease_count"].fillna(0).clip(upper=5)
        + rank["manual_modality_ready"].astype(int)
        - 2 * rank["manual_direction_blocked"].astype(int)
        - 2 * rank["manual_prior_blocked"].astype(int)
        - 2 * rank["broad_negative_disease_count"].fillna(0).clip(upper=3)
    )
    missing_rows = []
    calls = []
    critical = [
        "gate_real_efferocytosis_perturbation",
        "gate_ms_anchor",
        "gate_cross_disease_expression",
        "gate_genetic_breadth",
        "gate_modality_ready",
        "gate_direction_clear",
        "gate_prior_not_blocked",
    ]
    for _, row in rank.iterrows():
        missing = [col.replace("gate_", "") for col in critical if not bool(row[col])]
        missing_rows.append(";".join(missing))
        if bool(row["manual_prior_blocked"]) and row["gene"] != "FCGRT":
            calls.append("NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED")
        elif bool(row["manual_direction_blocked"]):
            calls.append("NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED")
        elif not bool(row["gate_real_efferocytosis_perturbation"]):
            calls.append("NO_GO_NO_EFFEROCYTOSIS_PERTURBATION")
        elif not bool(row["gate_ms_anchor"]) and not bool(row["gate_target_resolved_ms"]):
            calls.append("PARK_EFFEROCYTOSIS_ROUTE_NO_MS_ANCHOR")
        elif not bool(row["gate_cross_disease_expression"]) and not bool(row["gate_genetic_breadth"]):
            calls.append("PARK_EFFEROCYTOSIS_ROUTE_WEAK_CROSS_DISEASE_ANCHOR")
        elif not bool(row["gate_modality_ready"]):
            calls.append("PARK_EFFEROCYTOSIS_PERTURBATION_NO_MODALITY")
        elif row["gene"] == "FCGRT" and bool(row["manual_prior_blocked"]):
            calls.append("PARK_FCRN_REPURPOSING_PRIOR_ART_NO_MS_MODULE_ANCHOR")
        elif not bool(row["gate_prior_not_blocked"]):
            calls.append("PARK_PRIOR_ART_HEAVY_REPURPOSING_ONLY")
        else:
            calls.append("REOPEN_FC_EFFEROCYTOSIS_TARGET_FORCING")
    rank["wave103_missing_gates"] = missing_rows
    rank["wave103_call"] = calls
    priority = {
        "REOPEN_FC_EFFEROCYTOSIS_TARGET_FORCING": 0,
        "PARK_FCRN_REPURPOSING_PRIOR_ART_NO_MS_MODULE_ANCHOR": 1,
        "PARK_EFFEROCYTOSIS_ROUTE_NO_MS_ANCHOR": 2,
        "PARK_EFFEROCYTOSIS_ROUTE_WEAK_CROSS_DISEASE_ANCHOR": 3,
        "PARK_EFFEROCYTOSIS_PERTURBATION_NO_MODALITY": 4,
        "PARK_PRIOR_ART_HEAVY_REPURPOSING_ONLY": 5,
        "NO_GO_NO_EFFEROCYTOSIS_PERTURBATION": 6,
        "NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED": 7,
    }
    rank["wave103_call_priority"] = rank["wave103_call"].map(priority).fillna(99).astype(int)
    return rank.sort_values(["wave103_call_priority", "wave103_score"], ascending=[True, False])


def write_report(rank: pd.DataFrame, summary: dict[str, Any]) -> None:
    cols = [
        "gene",
        "wave103_call",
        "wave103_score",
        "wave103_gate_count",
        "wave37_screen_call",
        "wave37_contrast_lfc",
        "ms_delta_log2",
        "ms_p",
        "broad_positive_disease_count",
        "broad_negative_disease_count",
        "wave55_genetic_diseases_ge_0_25",
        "wave62_strong_qtl_coloc_disease_count",
        "wave62_ms_max_l2g_score",
        "modality",
        "manual_safety_blocker",
        "wave103_missing_gates",
    ]
    report = f"""# Wave103 Fc/FcRn/Efferocytosis Route Audit

## Bottom Line

Branch call: `{summary["branch_call"]}`.

The Fc/FcRn/efferocytosis route has real perturbation and translational
interest, but no candidate currently combines MS anchoring, cross-disease
module anchoring, genetics, clear intervention direction, safety, and novelty.

## Candidate Ranking

{markdown_table(rank[cols], max_rows=30)}

## Interpretation

- `FCGRT` is the most intervention-ready node because FcRn blockade has human
  drug precedent and Wave37 CRISPR evidence suggests KO can enhance
  efferocytosis. It fails the V3 route here because local MS expression is
  null, broad h5ad expression is negative/contradictory, target-resolved
  autoimmune genetics are absent, and prior art is heavy.
- `DAB2` and `CD9` have MS white-matter expression anchors plus real
  efferocytosis-screen support, but lack target-resolved genetics and clean
  modality/direction.
- Activating Fc receptors (`FCGR2A`, `FCGR3A`, `FCGR3B`, `FCGR1A`) and shared
  adaptors (`FCER1G`, `TYROBP`) are blocked by direction and host-defense
  safety.
- TAM receptors (`MERTK`, `AXL`) remain biologically plausible resolution
  comparators, but local MS anchoring, agonist modality, and prior-art/direction
  issues block promotion.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave103_fc_receptor_efferocytosis_route_audit.py")}`
- Rank table: `{rel(OUT / "fc_efferocytosis_route_rank.tsv")}`
- Summary: `{rel(OUT / "summary.json")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    rank = add_gates(collect())
    rank.to_csv(OUT / "fc_efferocytosis_route_rank.tsv", sep="\t", index=False)
    reopened = rank[rank["wave103_call"].eq("REOPEN_FC_EFFEROCYTOSIS_TARGET_FORCING")]
    summary = {
        "random_seed": SEED,
        "branch_call": "REOPEN_FC_EFFEROCYTOSIS_TARGET_FORCING" if not reopened.empty else "NO_REOPEN_FC_EFFEROCYTOSIS_ROUTE",
        "n_candidates": int(len(rank)),
        "call_counts": rank["wave103_call"].value_counts().to_dict(),
        "top_candidate": clean(rank.iloc[0]["gene"]) if not rank.empty else "",
        "top_candidate_call": clean(rank.iloc[0]["wave103_call"]) if not rank.empty else "",
        "inputs": {
            "wave37": rel(W37),
            "wave34": rel(W34),
            "wave55": rel(W55),
            "wave62": rel(W62),
            "wave81": rel(W81),
            "broad": rel(BROAD),
            "ms_signature": rel(MS_SIG),
        },
        "guardrail": (
            "This audit includes manual translational blockers for Fc/FcRn/TAM "
            "biology. Manual blockers are routing labels, not literature proof; "
            "claim-grade prior art would require a separate verified search."
        ),
    }
    write_json(OUT / "summary.json", summary)
    write_report(rank, summary)


if __name__ == "__main__":
    main()
