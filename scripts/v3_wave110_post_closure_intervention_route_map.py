#!/usr/bin/env python3
"""Wave110 post-closure intervention route map.

After CD82 and MFGE8 failed promotion, this script ranks remaining intervention
classes by which *specific* missing experiment could still change the decision.
It is a planning/forcing map, not a finding claim.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "results_v3" / "wave110_post_closure_intervention_route_map"
W83 = ROOT / "results_v3" / "wave83_intervention_class_meta_rank" / "intervention_class_meta_rank.tsv"
W91 = ROOT / "results_v3" / "wave91_lipid_lysosomal_module_intervention_rank" / "lipid_lysosomal_intervention_rank.tsv"
W81 = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"


MANUAL_ROUTE_NOTES = {
    "GPR183_EBI2_OXYSTEROL_NICHE": {
        "next_test": "MS-spatial/lesion validation of GPR183 plus CH25H/CYP7B1 ligand-axis in same APC niche; kill if receptor and ligand do not co-localize.",
        "escape_logic": "Druggable GPCR and coherent niche biology; only Wave83 PARK route.",
    },
    "FPR2_ANXA1_BIASED_RESOLUTION": {
        "next_test": "Cross-disease response-state test of ANXA1/FPR2 ligand-receptor module with MS lesion anchor; kill if no MS/resolution-state support.",
        "escape_logic": "Biased pro-resolution GPCR has tractable modalities and a wet-lab-only reopener.",
    },
    "P2RX7_PURINERGIC_STRATIFICATION": {
        "next_test": "Target-level P2RX7 expression/genetics plus inflammasome-high subgroup test; kill if P2RX7 is not the subgroup driver.",
        "escape_logic": "Small-molecule class exists and stratification, not pan-treatment, may avoid broad failure.",
    },
    "PARK7_RESIDUAL_ROUTE": {
        "next_test": "MS anchor and perturbation direction test in myeloid lipid-stress datasets; kill if PARK7 remains generic stress biology.",
        "escape_logic": "Small-molecule DJ-1/PARK7 route exists and foundation support was nonzero.",
    },
    "PSAP": {
        "next_test": "Check PSAP/prosaposin against MS lesion, direct h5ad lipid-loader contexts, and perturbation/foundation rows; kill if no cross-disease recurrence.",
        "escape_logic": "Secreted lysosomal lipid cofactor with MS nominal anchor and foundation-model support.",
    },
}


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def score_w83(row: pd.Series) -> dict[str, Any]:
    critical = float(row.get("critical_gate_count", 0) or 0)
    support = float(row.get("support_gate_count", 0) or 0)
    interesting = float(row.get("interestingness_score", 0) or 0)
    missing = str(row.get("wave83_missing_gates", ""))
    blocker = str(row.get("primary_blocker", ""))
    reachable = int(row.get("reachable_modality", 0) or 0)
    prior = int(row.get("prior_not_blocked", 0) or 0)
    safety = int(row.get("safety_direction_clear", 0) or 0)
    response = int(row.get("response_support", 0) or 0)
    direct = int(row.get("direct_perturbation", 0) or 0)
    foundation = int(row.get("foundation_model", 0) or 0)
    ms = int(row.get("ms_anchor", 0) or 0)
    genetics = int(row.get("genetic_or_target_resolution", 0) or 0)
    specificity = int(row.get("specificity_support", 0) or 0)
    escape_score = (
        1.2 * reachable
        + 1.0 * prior
        + 1.0 * safety
        + 0.8 * response
        + 0.8 * direct
        + 0.8 * foundation
        + 0.7 * ms
        + 0.7 * genetics
        + 0.7 * specificity
        + 0.15 * interesting
        - 0.25 * critical
    )
    if "prior_not_blocked" in missing:
        escape_score -= 1.5
    if "safety_direction_clear" in missing:
        escape_score -= 1.0
    if "ms_anchor" in missing:
        escape_score -= 0.7
    if "source_audit_not_promotional" in missing:
        escape_score -= 0.5
    if "NO_GO" in str(row.get("source_call", "")):
        escape_score -= 0.7
    return {
        "candidate": row.get("candidate", ""),
        "source": "wave83",
        "source_wave": row.get("source_wave", ""),
        "mechanism": row.get("mechanism", ""),
        "modality": row.get("modality", ""),
        "source_call": row.get("source_call", ""),
        "primary_blocker": blocker,
        "missing_gates": missing,
        "escape_score": escape_score,
        "support_summary": (
            f"reachable={reachable};prior={prior};safety={safety};response={response};"
            f"direct={direct};foundation={foundation};ms={ms};genetics={genetics};specificity={specificity}"
        ),
    }


def score_w81(row: pd.Series) -> dict[str, Any]:
    gene = str(row.get("gene", ""))
    score = float(row.get("score", 0) or 0)
    direct = int(row.get("direct_perturbation", 0) or 0)
    foundation = int(row.get("foundation_model_support", 0) or 0)
    ms = int(row.get("ms_anchor", 0) or 0)
    genetics = int(row.get("genetics_or_target_resolution", 0) or 0)
    broad = float(row.get("broad_positive_disease_count", 0) or 0)
    modality = int(row.get("modality_channel", 0) or 0)
    prior = int(row.get("prior_not_blocked", 0) or 0)
    escape = 0.4 * score + direct + foundation + ms + genetics + 0.25 * broad + modality + prior
    if not modality:
        escape -= 1.0
    if not ms:
        escape -= 0.5
    return {
        "candidate": gene,
        "source": "wave81",
        "source_wave": "wave81_perturbation_first_rescue",
        "mechanism": row.get("direct_perturbation_detail", "") or row.get("foundation_model_detail", ""),
        "modality": "gene/protein route unresolved",
        "source_call": row.get("wave81_call", ""),
        "primary_blocker": row.get("decision_reason", ""),
        "missing_gates": "",
        "escape_score": escape,
        "support_summary": (
            f"score={score};direct={direct};foundation={foundation};ms={ms};"
            f"genetics={genetics};broad={broad};modality={modality};prior={prior}"
        ),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    w83 = read_tsv(W83)
    for _, row in w83.iterrows():
        rows.append(score_w83(row))
    w81 = read_tsv(W81)
    for _, row in w81.head(80).iterrows():
        rows.append(score_w81(row))
    out = pd.DataFrame(rows)
    if not out.empty:
        out = out[~out["candidate"].astype(str).str.contains("CD82", case=False, na=False)].copy()
        out = out[~out["candidate"].astype(str).str.contains("MFGE8", case=False, na=False)].copy()
        out["manual_escape_logic"] = out["candidate"].map(lambda x: MANUAL_ROUTE_NOTES.get(str(x), {}).get("escape_logic", ""))
        out["recommended_next_test"] = out["candidate"].map(lambda x: MANUAL_ROUTE_NOTES.get(str(x), {}).get("next_test", ""))
        out["has_concrete_next_test"] = out["recommended_next_test"].ne("")
        out = out.sort_values(["has_concrete_next_test", "escape_score"], ascending=[False, False])
    out.to_csv(OUT / "post_closure_route_map.tsv", sep="\t", index=False)
    top = out.head(15) if not out.empty else pd.DataFrame()
    branch_call = "NO_PROMOTABLE_ROUTE_SELECT_NEXT_FORCING_TEST"
    payload = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "n_routes": int(len(out)),
        "top_candidates": top[["candidate", "source", "escape_score", "recommended_next_test"]].to_dict(orient="records")
        if not top.empty
        else [],
        "inputs": {"wave83": rel(W83), "wave91": rel(W91), "wave81": rel(W81)},
    }
    write_json(OUT / "summary.json", payload)
    cols = [
        "candidate",
        "source",
        "source_wave",
        "escape_score",
        "source_call",
        "support_summary",
        "primary_blocker",
        "manual_escape_logic",
        "recommended_next_test",
    ]
    report = f"""# Wave110 Post-Closure Intervention Route Map

## Bottom Line

Branch call: `{branch_call}`.

CD82 and MFGE8 are excluded from promotion. This map ranks remaining routes by
whether a concrete local forcing test could still change the decision.

## Top Routes

{markdown_table(top[cols], max_rows=15) if not top.empty else "_No routes._"}

## Interpretation

No route is promoted here. The map is used to choose the next forcing test.
Routes without a concrete test remain parked even if their aggregate score is
high.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave110_post_closure_intervention_route_map.py")}`
- Output: `{rel(OUT / "post_closure_route_map.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
