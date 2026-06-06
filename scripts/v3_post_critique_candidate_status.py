#!/usr/bin/env python3
"""Build post-critique candidate status table for V3 integration.

The raw candidate rankings over-reward broad recurrence. This script adds
explicit status labels after the hour-3 critique: residualization survival,
perturbation support, intervention tractability, and whether the lane is still
eligible for a V3 central finding.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "phases/v3/results"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    convergence = read_json(RESULTS / "cross_disease_convergence_summary.json")
    residual = read_json(RESULTS / "residualization" / "ifn_residualization_summary.json")
    pde4 = read_json(RESULTS / "pde4_camp_l1000_audit_summary.json")
    lipa_residual = read_json(RESULTS / "lipa_residualization" / "lipa_residualization_summary.json")
    central = pd.read_csv(RESULTS / "central_and_intervention_candidate_rank.tsv", sep="\t")
    first_pass = pd.read_csv(RESULTS / "central_node_first_pass_rank.tsv", sep="\t")

    module_summary = {row["module"]: row for row in convergence["top_modules"]}
    transition = convergence["transition_summary"][0]

    def first_pass_gene(gene: str) -> dict:
        hit = first_pass.loc[first_pass["gene"] == gene]
        return hit.iloc[0].to_dict() if len(hit) else {}

    rows = [
        {
            "lane": "IFNG_HLAII_CD74_transition",
            "central_node_or_state": "IFNG->IFNGR/JAK/STAT1->CIITA/RFX5/NLRC5->HLA-II/CD74/TAP/GILT",
            "raw_breadth": f"{transition['n_supportive_or_strong_diseases']}/{transition['n_diseases_tested']} supportive-or-strong diseases",
            "residualization_status": (
                f"{residual['ifn_residual_nominal_supported_tests']}/"
                f"{residual['n_tests']} tests retain nominal support; no residual FDR support"
            ),
            "perturbation_status": "Strong Mixscale controller support for IFNGR1/2, JAK1/2, STAT1; RFX5 narrow HLA/CD74 support",
            "intervention_status": "Broad IFNGR/JAK/STAT blockade rejected; local CIITA/HLA/CD74 gate remains hypothesis only",
            "genetics_status": "MHC and IRF1 support only; no single non-MHC coloc-grade pan-autoimmune anchor",
            "prior_art_status": "Broad IFN/JAK/CD74/MHC-II biology is heavily prior-arted",
            "checkpoint_disposition": "demote from pan-autoimmune mechanism to recurrent state/stratifier unless narrowed",
        },
        {
            "lane": "Residual_CD74_HLA_receptor_state",
            "central_node_or_state": "mif_cd74_receptor_state / CD74-HLA-CD44-CXCR4 state",
            "raw_breadth": (
                f"{module_summary['mif_cd74_receptor_state']['n_supportive_or_strong_diseases']}/"
                f"{module_summary['mif_cd74_receptor_state']['n_diseases_tested']} supportive-or-strong diseases"
            ),
            "residualization_status": "Nominal residual support in MS microglia and weak Sjogren epithelial/T1D signals; no residual FDR support",
            "perturbation_status": "RFX5 and upstream IFNG controllers suppress HLA/CD74 readouts in Mixscale; direct CD74 perturbation not validated here",
            "intervention_status": "Potential biomarker; direct CD74/MIF intervention prior-arted; local CIITA gate needs validation",
            "genetics_status": "Mostly MHC-generic; CD74 itself lacks strong genetic anchoring in local table",
            "prior_art_status": "CD74/MIF and HLA-II autoimmunity are crowded",
            "checkpoint_disposition": "biomarker-only demotion after wave-4 scout; not V3 central finding",
        },
        {
            "lane": "LIPA_lipid_lysosomal",
            "central_node_or_state": "LIPA / lysosomal acid lipase lipid-processing state",
            "raw_breadth": (
                f"{first_pass_gene('LIPA').get('positive_disease_count', 'NA')} positive and "
                f"{first_pass_gene('LIPA').get('negative_disease_count', 'NA')} negative diseases in first-pass heuristic; "
                f"lipid_loader_repair {module_summary['lipid_loader_repair']['n_supportive_or_strong_diseases']}/"
                f"{module_summary['lipid_loader_repair']['n_diseases_tested']} supportive-or-strong"
            ),
            "residualization_status": (
                f"{lipa_residual['n_lipa_raw_positive_nominal']} raw positive nominal and "
                f"{lipa_residual['n_lipa_raw_negative_nominal']} raw negative nominal compartments; "
                f"{len(lipa_residual['lipa_residual_retained_nominal_tests'])} univariate stress-residual tests retain nominal positive signal"
            ),
            "perturbation_status": "No current foundation/Mixscale perturbation evidence for LIPA in autoimmune disease cells",
            "intervention_status": "Potentially druggable biology via lysosomal acid lipase, but direction and tissue delivery unclear",
            "genetics_status": "No OpenTargets candidate hit in local cross-autoimmune table; needs dedicated genetics/prior-art audit",
            "prior_art_status": "Unknown in V3; wave-4 scout dispatched",
            "checkpoint_disposition": "active but compartment-specific; not currently pan-autoimmune",
        },
        {
            "lane": "HIF_NAMPT_inflammatory_metabolism",
            "central_node_or_state": "HIF1A/NAMPT/PFKFB3/HK2 inflammatory metabolic licensing",
            "raw_breadth": (
                f"hif_nampt_metabolic {module_summary['hif_nampt_metabolic']['n_supportive_or_strong_diseases']}/"
                f"{module_summary['hif_nampt_metabolic']['n_diseases_tested']} supportive-or-strong; "
                f"inflammatory_nfkb {module_summary['inflammatory_nfkb']['n_supportive_or_strong_diseases']}/"
                f"{module_summary['inflammatory_nfkb']['n_diseases_tested']} supportive-or-strong"
            ),
            "residualization_status": "Not an IFN/APC residual target; direct evidence is IBD/T1D-heavy, not pan-autoimmune",
            "perturbation_status": "Withaferin-a/NAMPT appears in L1000 full-signature top hits, but not a clean autoimmune intervention",
            "intervention_status": "Druggable but broad metabolic/toxicity issues; NAMPT rejected in V2 on prior-art/direction grounds",
            "genetics_status": "NAMPT/HIF1A weak or literature/RNA-heavy local support; no four-disease causal anchor",
            "prior_art_status": "NAMPT/metabolic inflammation is crowded",
            "checkpoint_disposition": "demote to IBD/T1D-specific backup lane",
        },
        {
            "lane": "PDE4_cAMP_local_CIITA_gate",
            "central_node_or_state": "PDE4/cAMP-PKA modulation of CIITA/MHC-II/CD74 gate",
            "raw_breadth": "Not a disease state; intervention hypothesis from scout",
            "residualization_status": "Depends on residual CD74/HLA lane; not independently validated",
            "perturbation_status": (
                f"LINCS has {pde4['n_lincs_unique_pert_ids_matching_terms']} PDE4/cAMP perturbagen IDs; "
                f"{pde4['n_l1000_top_hit_rows_matching_core_compounds']} core compounds in top L1000 hits"
            ),
            "intervention_status": "Tractable for local gut/skin delivery; weak L1000 support and medium-high prior-art risk",
            "genetics_status": "No direct genetics expected for pharmacologic class",
            "prior_art_status": "PDE4 in UC/psoriasis active; biomarker-specific angle only",
            "checkpoint_disposition": "do not promote without tissue/ex vivo PD validation",
        },
    ]

    out = pd.DataFrame(rows)
    out.to_csv(RESULTS / "post_critique_candidate_status.tsv", sep="\t", index=False)
    summary = {
        "random_seed": 20260526,
        "n_lanes": int(len(out)),
        "active_lanes": out.loc[
            out["checkpoint_disposition"].str.startswith("active") & ~out["checkpoint_disposition"].str.contains("biomarker-only"),
            "lane",
        ].tolist(),
        "demoted_or_hold_lanes": out.loc[
            ~(out["checkpoint_disposition"].str.startswith("active") & ~out["checkpoint_disposition"].str.contains("biomarker-only")),
            "lane",
        ].tolist(),
        "guardrail": "This table is qualitative integration from traceable local outputs; it is not a statistical test.",
    }
    (RESULTS / "post_critique_candidate_status_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
