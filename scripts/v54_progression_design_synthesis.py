#!/usr/bin/env python3
"""Build the artifact-traced V54 prospective progression design table."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_design_synthesis"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    event_time = load("analysis/v54_progression_event_time_power_design/summary.json")
    assumptions = load(
        "analysis/v54_progression_event_time_assumption_robustness/summary.json"
    )
    competing = load("analysis/v54_progression_competing_risk_robustness/summary.json")
    schedule = load("analysis/v54_progression_visit_schedule_robustness/summary.json")
    repeated = load("analysis/v54_progression_repeated_score_reliability/summary.json")
    multisite = load("analysis/v54_progression_multisite_transportability/summary.json")
    p2 = load("analysis/v54_progression_p2_interaction_power/summary.json")
    role_matrix = load("analysis/v54_progression_candidate_role_matrix/summary.json")
    transport = pd.read_csv(
        ROOT / "analysis/v54_progression_multisite_transportability/transport_readiness.tsv",
        sep="\t",
    )
    ready = transport.loc[transport.transport_ready]
    if len(ready) != 2:
        raise RuntimeError(f"Expected two transport-ready reference cells, found {len(ready)}")
    if set(ready.n_requested) != {450} or set(ready.latent_event_probability) != {0.30}:
        raise RuntimeError("Transport-ready reference design changed")
    if set(ready.allocation) != {"balanced"}:
        raise RuntimeError("Transport-ready allocation changed")

    requirements = [
        {
            "component": "role",
            "reference_design": "P1 longitudinal progression; optional linked P2",
            "hard_boundary": "Do not substitute relapse, stage, morphology, or pharmacodynamic change",
            "evidence_type": "grounded metadata/method audit",
            "supporting_artifact": "docs/validation/PROGRESSION_COHORT_ACQUISITION_SPEC_V54.md",
        },
        {
            "component": "total sample size",
            "reference_design": "450 across 3 balanced sites for the stress-tested transport scenario",
            "hard_boundary": "Not a universal minimum; rerun blinded cohort-specific power at actual event rate/effect assumptions",
            "evidence_type": "seeded synthetic method behavior",
            "supporting_artifact": "analysis/v54_progression_multisite_transportability/transport_readiness.tsv",
        },
        {
            "component": "site allocation",
            "reference_design": "150/150/150 target; predeclare every site",
            "hard_boundary": "60/30/10 allocation did not pass full transport at the same total n",
            "evidence_type": "seeded synthetic method behavior",
            "supporting_artifact": "analysis/v54_progression_multisite_transportability/transport_readiness.tsv",
        },
        {
            "component": "progression event yield",
            "reference_design": "30% cumulative event setting; median minimum 26 events/site in passing cells",
            "hard_boundary": "15% event setting did not pass transport by n=450; fewer than 10 events is descriptive-only",
            "evidence_type": "seeded synthetic method behavior",
            "supporting_artifact": "analysis/v54_progression_multisite_transportability/transport_readiness.tsv",
        },
        {
            "component": "clinical visits",
            "reference_design": "quarterly assessment over the modeled 2-year horizon",
            "hard_boundary": "Actual cadence and confirmation interval must be frozen from protocol; annual schedules lost substantial ascertainment/power",
            "evidence_type": "seeded synthetic method behavior",
            "supporting_artifact": "analysis/v54_progression_visit_schedule_robustness/calibrated_observed_route_power.tsv",
        },
        {
            "component": "endpoint confirmation",
            "reference_design": "raw components plus later protocol-valid confirmation; CDP and PIRA separate",
            "hard_boundary": "Missing/mistimed confirmation remains inconclusive, never negative",
            "evidence_type": "synthetic regression behavior",
            "supporting_artifact": "analysis/v54_progression_endpoint_adjudication/summary.json",
        },
        {
            "component": "visit missingness",
            "reference_design": "capture expected/actual date, attendance, and reason for every visit",
            "hard_boundary": "Score-dependent or joint score/risk attendance invalidates ordinary observed-time inference",
            "evidence_type": "seeded synthetic method behavior",
            "supporting_artifact": "analysis/v54_progression_visit_schedule_robustness/null_calibration_by_route_mechanism.tsv",
        },
        {
            "component": "molecular score reliability",
            "reference_design": "blinded pilot/test-retest estimate before choosing repeat count",
            "hard_boundary": "Repeat collection is conditionally useful only from low reliability with sufficiently independent error",
            "evidence_type": "seeded synthetic method behavior",
            "supporting_artifact": "analysis/v54_progression_repeated_score_reliability/repeat_measurement_power_gains.tsv",
        },
        {
            "component": "molecular repeats",
            "reference_design": "one at reliability about 0.70; consider 3 fixed-average repeats near reliability 0.40 if errors are demonstrably not shared",
            "hard_boundary": "No outcome-informed weighting/timepoint selection; repeats cannot repair sparse events",
            "evidence_type": "seeded synthetic method behavior",
            "supporting_artifact": "analysis/v54_progression_repeated_score_reliability/summary.json",
        },
        {
            "component": "death/competing event",
            "reference_design": "capture date/cause and freeze cause-specific sensitivity before score access",
            "hard_boundary": "Joint score/progression-risk death invalidates ordinary censoring; no post-hoc death composite",
            "evidence_type": "seeded synthetic method behavior",
            "supporting_artifact": "analysis/v54_progression_competing_risk_robustness/summary.json",
        },
        {
            "component": "dropout/censoring",
            "reference_design": "complete dates/reasons plus IPCW, worst-case, joint-dependence, and time-variation diagnostics when required",
            "hard_boundary": "Unknown/outcome-related loss fails closed; crossing effects cannot be rescued by comparing window p-values",
            "evidence_type": "seeded synthetic + gate behavior",
            "supporting_artifact": "docs/validation/PROGRESSION_EVENT_TIME_ASSUMPTION_GATE_V54.md",
        },
        {
            "component": "primary inference",
            "reference_design": "site- and treatment/source-stratified event-time route",
            "hard_boundary": "Pooled route is invalid under site-score/baseline-hazard alignment",
            "evidence_type": "seeded synthetic method behavior",
            "supporting_artifact": "analysis/v54_progression_multisite_transportability/null_calibration_by_route.tsv",
        },
        {
            "component": "transport decision",
            "reference_design": "global positive + every-site direction + every leave-site-out positive + >=10 events/site + heterogeneity p>=0.05",
            "hard_boundary": "Global significance alone is not transport",
            "evidence_type": "seeded synthetic method behavior",
            "supporting_artifact": "docs/plans/PROGRESSION_MULTISITE_TRANSPORTABILITY_V54.md",
        },
        {
            "component": "P2 composition",
            "reference_design": "direct linked composition in both compartments; direct interaction only",
            "hard_boundary": "Noisy composition under true imbalance and unadjusted analyses are invalid",
            "evidence_type": "seeded synthetic + gate behavior",
            "supporting_artifact": "docs/validation/PROGRESSION_P2_COMPOSITION_ACCEPTANCE_V54.md",
        },
        {
            "component": "P2 sample planning",
            "reference_design": "paired where possible; rerun grid with blinded pairing/correlation/composition reliability",
            "hard_boundary": "Synthetic 0.7-SD interaction ranged from 15-80/group; not an empirical effect or universal minimum",
            "evidence_type": "seeded synthetic method behavior",
            "supporting_artifact": "analysis/v54_progression_p2_interaction_power/minimum_group_n.tsv",
        },
        {
            "component": "therapeutic interpretation",
            "reference_design": "P1 association -> P2 localization -> separate P3 direction-resolved functional validation",
            "hard_boundary": "A progression predictor is not a causal target and cannot establish halting progression",
            "evidence_type": "grounded project decision boundary",
            "supporting_artifact": "analysis/v54_progression_intervention_direction_map/summary.json",
        },
    ]
    frame = pd.DataFrame(requirements)
    frame.to_csv(OUT / "prospective_design_requirements.tsv", sep="\t", index=False)
    summary = {
        "purpose": "Artifact-traced synthesis of the V54 prospective progression cohort reference design",
        "synthetic_or_method_only": True,
        "n_requirements": len(frame),
        "n_source_artifacts": int(frame.supporting_artifact.nunique()),
        "reference_total_n": 450,
        "reference_sites": 3,
        "reference_allocation": "balanced",
        "reference_event_probability": 0.30,
        "reference_median_minimum_site_events": int(
            ready.median_minimum_site_events_across_seeds.min()
        ),
        "reference_visit_interval_years": 0.25,
        "current_known_p1_eligible_cohorts": role_matrix["P1_eligible"],
        "source_summary_verdicts": {
            "event_time": event_time["verdict"],
            "assumptions": assumptions["verdict"],
            "competing_risk": competing["verdict"],
            "visit_schedule": schedule["verdict"],
            "repeated_score": repeated["verdict"],
            "multisite": multisite["verdict"],
            "p2": p2["verdict"],
        },
        "verdict": "REFERENCE_DESIGN_SPECIFIED_BUT_NO_CURRENT_COHORT_ELIGIBLE",
        "boundary": "This synthesis combines method audits and acquisition gates. It is not biological evidence, a guaranteed sample size, or a claim that any state halts MS progression.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
