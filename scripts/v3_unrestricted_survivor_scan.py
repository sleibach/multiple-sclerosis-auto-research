#!/usr/bin/env python3
"""Scan all broad h5ad genes for post-APOC1 survivor candidates.

APOC1 passed the local breadth/MS gate but failed the Geneformer deletion gate.
This script re-opens the full broad discovery table rather than repeatedly
recycling the same hand-picked lipid-lysosomal panel.

Output is a routing table for additional testing, not a target nomination.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "unrestricted_survivor_scan"

MANUAL_LABELS: dict[str, dict[str, str]] = {
    "CBX3": {"status": "generic_hold", "reason": "chromatin/proliferation-associated; no clear lipid-lysosomal intervention point"},
    "CHI3L1": {"status": "prior_art_demote", "reason": "crowded YKL-40 biomarker/target prior art"},
    "LTA4H": {"status": "prior_art_demote", "reason": "direct EAE/MS and inflammatory-disease inhibitor prior art; prior Geneformer veto"},
    "CXCL9": {"status": "generic_hold", "reason": "IFN/CXCR3 chemokine axis; likely broad inflammatory trafficking rather than module-specific node"},
    "IL2RG": {"status": "generic_hold", "reason": "common gamma-chain immunology; strong safety and nonselective immunosuppression liability"},
    "PPP3CA": {"status": "prior_art_hold", "reason": "calcineurin is drugged by cyclosporine/tacrolimus with broad toxicity and direct transplant/autoimmunity precedent"},
    "HLA-B": {"status": "generic_hold", "reason": "HLA genetics/antigen-presentation marker, not selective intervention point here"},
    "HLA-DPB1": {"status": "generic_hold", "reason": "HLA class II marker, not selective intervention point here"},
    "APOC1": {"status": "model_demote", "reason": "post-triage Geneformer deletion screen showed no normalization support"},
    "CD44": {"status": "model_demote", "reason": "Geneformer deletion veto and crowded matrix/integrin prior art"},
    "C15ORF48": {"status": "model_blocked_hold", "reason": "strong expression marker but absent from Geneformer token dictionary in the current route"},
}


def safe_float(x: Any) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    broad = pd.read_csv(ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv", sep="\t", low_memory=False)
    gf_paths = [
        ROOT / "results_v3" / "geneformer_pivot_panel_delete" / "geneformer_pivot_panel_gene_summary.tsv",
        ROOT / "results_v3" / "geneformer_unrestricted_survivor_delete" / "geneformer_unrestricted_survivor_gene_summary.tsv",
    ]
    gf_tables = [pd.read_csv(path, sep="\t") for path in gf_paths if path.exists()]
    gf_pivot = pd.concat(gf_tables, ignore_index=True) if gf_tables else pd.DataFrame()

    candidates = broad.loc[
        (broad["ms_positive_nominal"] == True)
        & (broad["positive_disease_count"] >= 3)
        & (broad["negative_disease_count"] <= 1)
    ].copy()
    candidates["manual_status"] = candidates["gene"].map(lambda g: MANUAL_LABELS.get(str(g), {}).get("status", "unknown"))
    candidates["manual_reason"] = candidates["gene"].map(lambda g: MANUAL_LABELS.get(str(g), {}).get("reason", ""))
    candidates["module_relevance"] = np.where(
        candidates["in_lipid_lysosomal_myeloid_neighborhood"] == True,
        "curated_lipid_lysosomal_neighborhood",
        "unrestricted_cross_disease_survivor",
    )
    candidates["opentargets_evidence_present"] = pd.to_numeric(
        candidates.get("opentargets_disease_count", 0), errors="coerce"
    ).fillna(0) > 0

    if not gf_pivot.empty:
        gf_cols = [
            "gene",
            "contexts_with_token",
            "disease_cells_with_token",
            "support_contexts",
            "strong_support_contexts",
            "mean_cosine_z_vs_random",
            "mean_projection_shift",
        ]
        gf_agg = (
            gf_pivot[[c for c in gf_cols if c in gf_pivot.columns]]
            .groupby("gene", observed=True)
            .agg(
                contexts_with_token=("contexts_with_token", "sum"),
                disease_cells_with_token=("disease_cells_with_token", "sum"),
                support_contexts=("support_contexts", "sum"),
                strong_support_contexts=("strong_support_contexts", "sum"),
                mean_cosine_z_vs_random=("mean_cosine_z_vs_random", "mean"),
                mean_projection_shift=("mean_projection_shift", "mean"),
            )
            .reset_index()
        )
        candidates = candidates.merge(gf_agg, on="gene", how="left")
    else:
        for col in [
            "contexts_with_token",
            "disease_cells_with_token",
            "support_contexts",
            "strong_support_contexts",
            "mean_cosine_z_vs_random",
            "mean_projection_shift",
        ]:
            candidates[col] = np.nan

    candidates["needs_geneformer"] = candidates["contexts_with_token"].isna()
    candidates["survivor_priority_score"] = (
        2.0 * candidates["positive_disease_count"].astype(float)
        - 1.5 * candidates["negative_disease_count"].astype(float)
        + 2.0 * candidates["ms_wm_hedges_g"].astype(float).clip(lower=0)
        + candidates["positive_compartment_count"].astype(float).clip(upper=6) * 0.4
        + np.where(candidates["in_lipid_lysosomal_myeloid_neighborhood"] == True, 1.0, 0.0)
        + pd.to_numeric(candidates["support_contexts"], errors="coerce").fillna(0).clip(upper=4)
    )
    candidates["routing_decision"] = "test_or_scout"
    candidates.loc[candidates["manual_status"].isin(["prior_art_demote", "model_demote"]), "routing_decision"] = "demote"
    candidates.loc[candidates["manual_status"].isin(["generic_hold", "prior_art_hold", "model_blocked_hold"]), "routing_decision"] = "hold"
    candidates.loc[candidates["needs_geneformer"] & (candidates["routing_decision"] == "test_or_scout"), "routing_decision"] = "geneformer_next"

    cols = [
        "gene",
        "routing_decision",
        "manual_status",
        "manual_reason",
        "module_relevance",
        "positive_disease_count",
        "negative_disease_count",
        "positive_compartment_count",
        "negative_compartment_count",
        "positive_diseases",
        "negative_diseases",
        "top_positive_compartments",
        "ms_wm_delta_log2",
        "ms_wm_hedges_g",
        "ms_wm_p",
        "ms_wm_fdr",
        "contexts_with_token",
        "disease_cells_with_token",
        "support_contexts",
        "strong_support_contexts",
        "mean_cosine_z_vs_random",
        "mean_projection_shift",
        "opentargets_evidence_present",
        "opentargets_disease_count",
        "opentargets_channels_present",
        "survivor_priority_score",
    ]
    out = candidates[[c for c in cols if c in candidates.columns]].sort_values(
        ["routing_decision", "survivor_priority_score", "positive_disease_count"],
        ascending=[True, False, False],
    )
    out.to_csv(OUT / "unrestricted_survivor_candidates.tsv", sep="\t", index=False)

    next_genes = out.loc[out["routing_decision"] == "geneformer_next", "gene"].head(24).tolist()
    summary = {
        "random_seed": SEED,
        "selection_rule": "MS positive nominal; >=3 positive diseases; <=1 negative disease in broad h5ad gene discovery",
        "n_candidates": int(len(out)),
        "routing_counts": out["routing_decision"].value_counts().to_dict(),
        "next_geneformer_genes": next_genes,
        "guardrail": (
            "This is still donor-level observational expression plus existing screens. "
            "Generic inflammatory and prior-arted nodes are held or demoted even when statistically strong."
        ),
    }
    (OUT / "unrestricted_survivor_candidates.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(out.to_string(index=False))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
