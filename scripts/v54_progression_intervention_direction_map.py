#!/usr/bin/env python3
"""Build a sequential intervention-direction gate for V54 progression states."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_intervention_direction_map"


def load_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text())


def get_row(frame: pd.DataFrame, module: str) -> pd.Series:
    selected = frame.loc[frame["module"].eq(module)]
    assert len(selected) == 1, module
    return selected.iloc[0]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    stage_path = "analysis/v54_progressive_stage_modules/module_tests.tsv"
    lesion_path = "analysis/v54_progression_lesion_state/cross_context_outcomes.tsv"
    panel_path = "analysis/v54_progression_lesion_module_panel/cross_context_outcomes.tsv"
    stage = pd.read_csv(ROOT / stage_path, sep="\t")
    lesion = pd.read_csv(ROOT / lesion_path, sep="\t")
    panel = pd.read_csv(ROOT / panel_path, sep="\t")

    coupling = load_json("analysis/v54_oxphos_lysosomal_coupling/summary.json")
    network = load_json("analysis/v53_network_control_probe/summary.json")
    combinations = load_json("analysis/v53_combinatorial_intervention_probe/summary.json")
    causal = load_json("analysis/v53_causal_identifiability_sensitivity/summary.json")
    component = load_json("analysis/v53_ms_microglia_component_specificity/summary.json")
    microglia = load_json("analysis/v53_ms_microglia_independent_cohort_scout/summary.json")
    mif = load_json("analysis/v53_mif_cd74_grounded_audit/summary.json")

    assert coupling["verdict"] == "BOTH_MORPHOLOGY_ASSOCIATIONS_SEPARABLE_UNDER_TESTED_MODEL"
    assert network["replicated_control_candidates"] == []
    assert combinations["n_prioritization_gate_passes"] == 0
    assert causal["n_variants_with_any_consensus_orientation"] == 0
    assert component["component_specificity_gate_pass"] is False
    assert microglia["cohorts"]["macnair_validation"]["frozen_primary_pass"] is True
    assert mif["receptor_specific_adjusted_successes"] == 0

    receptor_stage = get_row(stage, "receptor_cd44_cxcr4")
    receptor_lesion = get_row(lesion, "receptor_cd44_cxcr4")
    hla_stage = get_row(stage, "hla_regulatory")
    hla_lesion = get_row(lesion, "hla_regulatory")
    ifn_stage = get_row(stage, "ifn_apc_unique")
    ifn_lesion = get_row(lesion, "ifn_apc_unique")
    mif_stage = get_row(stage, "mif_ligand")
    lys_stage = get_row(stage, "lysosomal_unique")
    lys_lesion = get_row(lesion, "lysosomal_unique")
    oxphos = get_row(panel, "oxphos")
    lipid = get_row(lesion, "lipid_repair")
    resolution = get_row(panel, "resolution_efferocytosis_proxy")
    mocci = get_row(panel, "mocci_inflammatory_switch")

    candidates = [
        {
            "candidate": "CD44/CXCR4 receptor state",
            "observed_context": (
                f"replicated MS microglial state; V54 SPMS-PPMS beta "
                f"{receptor_stage.spms_minus_ppms_standardized_beta:.3f}, max-T "
                f"p={receptor_stage.max_t_fwer_p:.3f}; lesion outcome "
                f"{receptor_lesion.outcome}"
            ),
            "progression_status": "inconclusive",
            "direction_problem": (
                "MS disease-state association is broad-state bounded; no disability "
                "trajectory or component-specific pathogenic direction"
            ),
            "reopen_evidence": (
                "longitudinal progression association plus component-resolved selective "
                "perturbation with functional and host-defense readouts"
            ),
            "artifacts": (
                f"{stage_path};{lesion_path};analysis/v53_ms_microglia_"
                "component_specificity/summary.json"
            ),
        },
        {
            "candidate": "HLA regulatory state",
            "observed_context": (
                f"V54 stage outcome {hla_stage.outcome}; lesion outcome {hla_lesion.outcome}"
            ),
            "progression_status": "not_supported",
            "direction_problem": "source/context direction is not portable and HLA modulation has broad immune collateral",
            "reopen_evidence": "portable progression association and selective APC perturbation preserving antigen defense",
            "artifacts": f"{stage_path};{lesion_path}",
        },
        {
            "candidate": "IFN/APC state",
            "observed_context": (
                f"V54 stage beta {ifn_stage.spms_minus_ppms_standardized_beta:.3f}, "
                f"max-T p={ifn_stage.max_t_fwer_p:.3f}; lesion outcome {ifn_lesion.outcome}"
            ),
            "progression_status": "inconclusive",
            "direction_problem": "generic immune tone and host-defense collateral remain inseparable",
            "reopen_evidence": "progression-linked within-cell state plus selective modulation sparing antiviral defense",
            "artifacts": f"{stage_path};{lesion_path};analysis/v53_network_control_probe/summary.json",
        },
        {
            "candidate": "MIF ligand state",
            "observed_context": (
                f"V54 stage outcome {mif_stage.outcome}; V53 receptor-specific successes "
                f"{mif['receptor_specific_adjusted_successes']}"
            ),
            "progression_status": "not_supported",
            "direction_problem": "ligand causality and stable therapy direction are absent",
            "reopen_evidence": "component-resolved progression association and direction-consistent MIF perturbation",
            "artifacts": f"{stage_path};analysis/v53_mif_cd74_grounded_audit/summary.json",
        },
        {
            "candidate": "Lysosomal state",
            "observed_context": (
                f"higher in foamy morphology (beta {lys_lesion.gse279972_foamy_adjusted_beta:.3f}, "
                f"max-T p={lys_lesion.gse279972_max_t_p:.3f}) but active-edge direction mixed; "
                f"stage outcome {lys_stage.outcome}"
            ),
            "progression_status": "morphology_only",
            "direction_problem": "higher lysosomal transcript state may be pathogenic, compensatory, or reparative; flux unmeasured",
            "reopen_evidence": "orthogonal longitudinal progression support plus measured flux and direction-matched perturbation",
            "artifacts": f"{stage_path};{lesion_path};analysis/v54_lysosomal_morphology_specificity/summary.json",
        },
        {
            "candidate": "OXPHOS state",
            "observed_context": (
                f"lower in foamy morphology (beta {oxphos.gse279972_foamy_adjusted_beta:.3f}, "
                f"max-module p={oxphos.gse279972_max_module_p:.3f}) but cross-context direction discordant"
            ),
            "progression_status": "morphology_only",
            "direction_problem": "transcript score is not metabolic flux and raising OXPHOS lacks functional safety direction",
            "reopen_evidence": "orthogonal progression support, flux assay, and selective rescue with viability/remyelination guards",
            "artifacts": f"{panel_path};analysis/v54_oxphos_lysosomal_coupling/summary.json",
        },
        {
            "candidate": "Lipid-repair state",
            "observed_context": (
                f"same-direction contexts but morphology max-T p={lipid.gse279972_max_t_p:.3f}"
            ),
            "progression_status": "inconclusive",
            "direction_problem": "repair-associated expression is not measured repair or a causal intervention direction",
            "reopen_evidence": "replicated progression association with lipid flux, myelin clearance, and remyelination endpoints",
            "artifacts": lesion_path,
        },
        {
            "candidate": "Resolution/efferocytosis proxy",
            "observed_context": (
                f"3/3 active-edge positive; morphology beta {resolution.gse279972_foamy_adjusted_beta:.3f}, "
                f"p={resolution.gse279972_donor_wild_p:.3f}"
            ),
            "progression_status": "inconclusive",
            "direction_problem": "transcript proxy does not measure efferocytosis or remyelination function",
            "reopen_evidence": "functional clearance/remyelination assay linked to progression and selective pro-resolution perturbation",
            "artifacts": panel_path,
        },
        {
            "candidate": "MOCCI inflammatory switch",
            "observed_context": (
                f"3/3 active-edge positive; morphology beta {mocci.gse279972_foamy_adjusted_beta:.3f}, "
                f"p={mocci.gse279972_donor_wild_p:.3f}"
            ),
            "progression_status": "inconclusive",
            "direction_problem": "context association is underpowered and has no causal node or functional direction",
            "reopen_evidence": "independent progression cohort and selective perturbation with functional readout",
            "artifacts": panel_path,
        },
    ]

    rows = []
    for candidate in candidates:
        progression_pass = False
        direction_pass = False
        causal_pass = False
        perturbation_pass = False
        collateral_pass = False
        modality_fit = False
        rows.append(
            {
                **candidate,
                "progression_specific_association_pass": progression_pass,
                "pathogenic_direction_resolved": direction_pass,
                "causal_node_specificity_pass": causal_pass,
                "selective_perturbation_pass": perturbation_pass,
                "collateral_guardrails_pass": collateral_pass,
                "modality_fit_pass": modality_fit,
                "alphafold_context_eligible": False,
                "target_revisit": False,
                "verdict": "not_target_ready",
            }
        )

    result = pd.DataFrame(rows)
    result.to_csv(OUT / "progression_intervention_direction_map.tsv", sep="\t", index=False)

    gate_counts = []
    gates = [
        "progression_specific_association_pass",
        "pathogenic_direction_resolved",
        "causal_node_specificity_pass",
        "selective_perturbation_pass",
        "collateral_guardrails_pass",
        "modality_fit_pass",
        "alphafold_context_eligible",
        "target_revisit",
    ]
    for gate in gates:
        gate_counts.append(
            {"gate": gate, "n_pass": int(result[gate].sum()), "n_candidates": len(result)}
        )
    pd.DataFrame(gate_counts).to_csv(OUT / "gate_counts.tsv", sep="\t", index=False)

    summary = {
        "purpose": "Sequential progression intervention-direction audit; no discovery claim",
        "n_candidates": len(result),
        "n_progression_specific_association_pass": int(
            result["progression_specific_association_pass"].sum()
        ),
        "n_target_revisit": int(result["target_revisit"].sum()),
        "held_perturbation_signatures": network["n_perturbation_signatures"],
        "held_replicated_selective_control_nodes": len(network["replicated_control_candidates"]),
        "held_additive_pair_gate_passes": combinations["n_prioritization_gate_passes"],
        "causal_skeleton_variants_with_consensus_orientation": causal[
            "n_variants_with_any_consensus_orientation"
        ],
        "alphafold_context_used": False,
        "verdict": "NO_PROGRESSION_DIRECTION_RESOLVED_INTERVENTION_ROUTE",
        "boundary": (
            "No candidate passes the first progression-specific gate. This confirms "
            "no current target route; it does not establish that future intervention is impossible."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = f"""# V54 Progression Intervention-Direction Map

## Verdict

**No progression-direction-resolved intervention route is supported.** None of
the {len(result)} frozen candidates passes the first progression-specific gate,
so none is eligible for AlphaFold-informed modality assessment or target
revisit.

## Why The Gate Stops Early

The strongest V54 observations are an OXPHOS-low/lysosomal-high foamy
morphology state in one cohort. Both survive mutual adjustment, but neither
transfers through the paired chronic-active-edge context and neither is linked
to disability. Foamy association does not identify whether a state is damaging,
compensatory, or reparative; transcript scores are not metabolic or lysosomal
flux.

CD44/CXCR4 remains a replicated MS microglial disease-state association from
V53, but its V54 PPMS-versus-SPMS and lesion tests are inconclusive. It also
failed the V53 component-specificity gate. It is therefore not a
progression-specific control node.

## Perturbation Boundary

The held perturbation layer contains {network['n_perturbation_signatures']}
signatures. V53 found zero replicated selective control nodes after correction,
zero additive pair-prioritization passes, and zero consensus causal edge
orientations across ten frozen skeleton variants. Those results do not prove
that intervention cannot work; they show that current aggregate signatures do
not identify a safe, direction-matched route.

## Structure Boundary

AlphaFold context was not invoked. Predicted structure can inform modality fit
only after progression association, pathogenic direction, causal specificity,
and selective perturbation pass. Running pocket analysis now would add
tractability decoration to candidates that lack a biological intervention
direction.

## Decision

No V52/V53 target closure changes. The only responsible route forward is new
longitudinal progression-linked and functional perturbation data. Candidate-
specific reopening requirements are recorded in
`progression_intervention_direction_map.tsv`.
"""
    (OUT / "REPORT.md").write_text(report)


if __name__ == "__main__":
    main()
