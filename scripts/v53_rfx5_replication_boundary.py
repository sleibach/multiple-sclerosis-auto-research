#!/usr/bin/env python3
"""Define the evidence and replication boundary for the V53 RFX5 signal.

The power component is seeded synthetic method characterization. It is not
biological evidence and does not estimate an RFX5 effect from donor-level data,
which the project does not hold.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PERTURBATIONS = ROOT / "analysis/v26_deep_structure/perturbation_module_matrix.tsv"
NETWORK_TESTS = ROOT / "analysis/v53_network_control_probe/control_signature_tests.tsv"
TIER0 = ROOT / "analysis/tier_0_triage/ciita_mediator_selectivity/selectivity_evidence.tsv"
GENETICS = ROOT / "phases/v3/results/wave14_target_level_genetics/target_level_genetics_truth_table.tsv"
ROUTE_GATES = ROOT / "phases/v3/results/wave53_perturbation_first_pivot/decision_matrix.tsv"
OUT = ROOT / "analysis/v53_rfx5_replication_boundary"

SEEDS = (53011, 53012, 53013)
N_REPLICATES_PER_SEED = 3_000
SAMPLE_SIZES = (8, 12, 16, 20, 24, 32, 40, 48, 64, 96)
STANDARDIZED_TARGET_EFFECTS = (0.5, 0.8, 1.0, 1.2, 1.5)
TARGET_EFFECT_FLOOR = -0.5
COLLATERAL_MEAN_FLOOR = -0.3


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def exact_one_sided_sign_p_lookup(n: int) -> np.ndarray:
    """Return P[Binomial(n, 0.5) >= k] for k=0..n."""
    probabilities = np.array([math.comb(n, k) / (2**n) for k in range(n + 1)])
    return np.cumsum(probabilities[::-1])[::-1]


def power_sweep() -> list[dict[str, Any]]:
    # Assumed endpoint correlation only; no held donor-level covariance exists.
    covariance = np.array(
        [
            [1.0, 0.5, 0.2, 0.2],
            [0.5, 1.0, 0.2, 0.2],
            [0.2, 0.2, 1.0, 0.3],
            [0.2, 0.2, 0.3, 1.0],
        ]
    )
    transform = np.linalg.cholesky(covariance)
    rows: list[dict[str, Any]] = []
    for target_effect in STANDARDIZED_TARGET_EFFECTS:
        for n_donors in SAMPLE_SIZES:
            sign_lookup = exact_one_sided_sign_p_lookup(n_donors)
            seed_powers = []
            for seed in SEEDS:
                rng = np.random.default_rng(seed + n_donors * 101 + round(target_effect * 1000))
                noise = rng.normal(
                    size=(N_REPLICATES_PER_SEED, n_donors, 4)
                ) @ transform.T
                effects = noise + np.array([-target_effect, -target_effect, 0.0, 0.0])
                target_means = effects[:, :, :2].mean(axis=1)
                collateral_means = effects[:, :, 2:].mean(axis=1)
                negative_counts = (effects[:, :, :2] < 0).sum(axis=1)
                sign_p = sign_lookup[negative_counts]
                # With two BH-adjusted target tests, both q<=0.10 iff max raw p<=0.10.
                target_gate = (
                    (np.max(sign_p, axis=1) <= 0.10)
                    & np.all(target_means <= TARGET_EFFECT_FLOOR, axis=1)
                )
                collateral_guard = np.all(
                    collateral_means >= COLLATERAL_MEAN_FLOOR, axis=1
                )
                per_context_success = target_gate & collateral_guard
                seed_powers.append(float(np.mean(per_context_success)))
            mean_power = float(np.mean(seed_powers))
            rows.append(
                {
                    "assumed_standardized_target_effect_each_primary_module": target_effect,
                    "n_donors_per_context": n_donors,
                    "replicates_per_seed": N_REPLICATES_PER_SEED,
                    "n_seeds": len(SEEDS),
                    "per_context_success_probability_mean": mean_power,
                    "per_context_success_probability_min_seed": min(seed_powers),
                    "per_context_success_probability_max_seed": max(seed_powers),
                    "two_independent_context_joint_probability": mean_power**2,
                    "target_gate": "both one-sided sign-test BH q<=0.10 and both standardized means<=-0.5",
                    "collateral_guard": "mean IFN/APC and GILT/lysosomal effects each>=-0.3",
                    "synthetic_marker": "SYNTHETIC_METHOD_CHARACTERIZATION_NOT_BIOLOGICAL_EVIDENCE",
                }
            )
    return rows


def main() -> int:
    perturbation_rows = read_tsv(PERTURBATIONS)
    perturbation_label = next(iter(perturbation_rows[0]))
    rfx5_rows = [row for row in perturbation_rows if row[perturbation_label].endswith(":RFX5")]
    if len(rfx5_rows) != 1:
        raise RuntimeError(f"Expected exactly one RFX5 perturbation row, found {len(rfx5_rows)}")
    rfx5 = rfx5_rows[0]

    network = next(row for row in read_tsv(NETWORK_TESTS) if row["node"] == "RFX5")
    tier0 = next(row for row in read_tsv(TIER0) if row["perturbation"] == "RFX5")
    genetics = next(row for row in read_tsv(GENETICS) if row["gene"] == "RFX5")
    route_rows = [
        row
        for row in read_tsv(ROUTE_GATES)
        if row["route"] == "RFX5_MHCII_PARTIAL_SUPPRESSION"
    ]
    route_passes = sum(row["passed"] == "True" for row in route_rows)

    boundary_rows = [
        {
            "boundary": "held_perturbation_contexts",
            "value": len(rfx5_rows),
            "source": str(PERTURBATIONS.relative_to(ROOT)),
            "interpretation": "one IFNG context only; no cross-stimulus replication",
        },
        {
            "boundary": "hla_ii_apc_effect",
            "value": rfx5["hla_ii_apc"],
            "source": str(PERTURBATIONS.relative_to(ROOT)),
            "interpretation": "descriptive aggregate perturbation effect",
        },
        {
            "boundary": "mif_cd74_receptor_state_effect",
            "value": rfx5["mif_cd74_receptor_state"],
            "source": str(PERTURBATIONS.relative_to(ROOT)),
            "interpretation": "descriptive aggregate perturbation effect",
        },
        {
            "boundary": "ifn_apc_effect",
            "value": rfx5["ifn_apc"],
            "source": str(PERTURBATIONS.relative_to(ROOT)),
            "interpretation": "descriptive collateral module effect",
        },
        {
            "boundary": "network_selective_score_q_bh",
            "value": network["score_q_bh"],
            "source": str(NETWORK_TESTS.relative_to(ROOT)),
            "interpretation": "fails the pre-specified corrected null gate",
        },
        {
            "boundary": "network_goal_cosine_q_bh",
            "value": network["cosine_q_bh"],
            "source": str(NETWORK_TESTS.relative_to(ROOT)),
            "interpretation": "fails the pre-specified corrected null gate",
        },
        {
            "boundary": "tier0_selectivity_call",
            "value": tier0["evidence_call"],
            "source": str(TIER0.relative_to(ROOT)),
            "interpretation": tier0["tier0_interpretation"],
        },
        {
            "boundary": "therapeutic_route_gates_passed",
            "value": f"{route_passes}/{len(route_rows)}",
            "source": str(ROUTE_GATES.relative_to(ROOT)),
            "interpretation": "perturbation selectivity and model-support gates only",
        },
        {
            "boundary": "target_level_genetics",
            "value": genetics["target_level_genetics_dod_call"],
            "source": str(GENETICS.relative_to(ROOT)),
            "interpretation": genetics["audit_priority_call"],
        },
    ]

    power_rows = power_sweep()
    minimum_n: dict[str, int | None] = {}
    for target_effect in STANDARDIZED_TARGET_EFFECTS:
        eligible = [
            int(row["n_donors_per_context"])
            for row in power_rows
            if row["assumed_standardized_target_effect_each_primary_module"] == target_effect
            and row["two_independent_context_joint_probability"] >= 0.80
        ]
        minimum_n[str(target_effect)] = min(eligible) if eligible else None

    replication_spec = {
        "purpose": "Pre-specified independent replication boundary for a nominal single-context RFX5 perturbation pattern",
        "current_status": "NOT_A_CONTROL_CANDIDATE_AND_NOT_A_THERAPEUTIC_TARGET",
        "contexts_required": [
            "primary human monocyte-derived APCs under IFN-gamma stimulation",
            "primary human B cells under a pre-locked constitutive-or-CD40L HLA-II condition",
        ],
        "design": [
            "paired donor design with RFX5 CRISPRi and non-targeting control in each context",
            "pre-lock one guide-quality threshold and exclude failed perturbations without using module outcomes",
            "freeze the V26 HLA-II/APC, receptor-state, IFN/APC, and GILT/lysosomal gene sets before assay",
            "analyze donor-level pseudobulk; technical cells are not independent replicates",
            "include a broad IFN/JAK control and a transcriptional-gate comparator, neither counted as RFX5 replication",
        ],
        "molecular_replication_gate": {
            "primary_targets": ["hla_ii_apc", "mif_cd74_receptor_state"],
            "criterion": "both expected-direction one-sided sign tests BH q<=0.10 and standardized mean effects<=-0.5 in each context",
            "collateral_guard": "mean standardized IFN/APC and GILT/lysosomal effects each>=-0.3 in each context",
            "cross_context_rule": "the complete gate must pass independently in both contexts",
        },
        "therapeutic_reopening_gate": [
            "molecular replication alone retains RFX5 as a mechanism comparator, not a drug target",
            "a practical partial-modulation modality must phenocopy the molecular gate",
            "the same modality must preserve broad IFN/APC and antigen-presentation host-defense function in a pre-specified functional assay",
            "an MS-relevant causal or response anchor must be established independently",
        ],
        "power_boundary": {
            "minimum_n_per_context_for_joint_power_ge_0_80_by_assumed_effect": minimum_n,
            "warning": "The project has no donor-level RFX5 variance estimate. These are assumption-labeled synthetic design probabilities, not an empirical effect-size estimate.",
        },
    }

    summary = {
        "purpose": "V53 RFX5 single-context evidence and replication boundary",
        "held_rfx5_contexts": len(rfx5_rows),
        "network_score_q_bh": float(network["score_q_bh"]),
        "network_cosine_q_bh": float(network["cosine_q_bh"]),
        "therapeutic_route_gates_passed": route_passes,
        "therapeutic_route_gates_total": len(route_rows),
        "target_level_genetics_call": genetics["target_level_genetics_dod_call"],
        "power_seeds": list(SEEDS),
        "synthetic_cohorts_simulated": len(SEEDS)
        * N_REPLICATES_PER_SEED
        * len(SAMPLE_SIZES)
        * len(STANDARDIZED_TARGET_EFFECTS),
        "verdict": "DESCRIPTIVE_SINGLE_CONTEXT_PATTERN_FAILS_CORRECTED_NULL_AND_REPLICATION_GATES",
        "promotion": False,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "current_evidence_boundary.tsv", boundary_rows)
    write_tsv(OUT / "synthetic_replication_power_map.tsv", power_rows)
    (OUT / "replication_spec.json").write_text(
        json.dumps(replication_spec, indent=2, sort_keys=True) + "\n"
    )
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    report = [
        "# V53 RFX5 Replication Boundary",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        "RFX5 has one held IFN-gamma perturbation summary. Its descriptive HLA-II/APC",
        f"effect is `{float(rfx5['hla_ii_apc']):.4f}` and receptor-state effect is",
        f"`{float(rfx5['mif_cd74_receptor_state']):.4f}`, while IFN/APC is",
        f"`{float(rfx5['ifn_apc']):.4f}`. In the pre-specified network-control null,",
        f"the selective-score q-value is `{float(network['score_q_bh']):.3f}` and the",
        f"goal-cosine q-value is `{float(network['cosine_q_bh']):.3f}`. It therefore",
        "does not pass even a preliminary corrected context gate and has no independent",
        "stimulus replication.",
        "",
        f"The prior route audit passes only `{route_passes}/{len(route_rows)}` gates, and",
        f"the target-level genetics call is `{genetics['target_level_genetics_dod_call']}`.",
        "The appropriate status is a nominal mechanistic comparator, not a control node",
        "and not a therapeutic target.",
        "",
        "## Exact Evidence Needed",
        "",
        "The committed replication specification requires paired donor-level RFX5 CRISPRi",
        "in two independent primary-human APC contexts. Both HLA-II/APC and receptor-state",
        "modules must pass the fixed direction/effect/null gate in each context while",
        "IFN/APC and lysosomal collateral remain within the fixed guard. Even success at",
        "that molecular gate would retain RFX5 as a mechanism comparator until a practical",
        "partial-modulation modality, functional host-defense preservation, and an",
        "independent MS-relevant anchor are shown.",
        "",
        "## Synthetic Design Map",
        "",
        f"The power map contains `{summary['synthetic_cohorts_simulated']:,}` seeded synthetic",
        "cohorts across three seeds. It varies assumed standardized target effect and donor",
        "count; it does not estimate the biological effect because no donor-level RFX5",
        "variance is held. The synthetic outputs characterize the proposed method only.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
