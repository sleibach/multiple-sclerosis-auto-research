# V4 Tiering Rulebook

## Candidate States

- `alive`: active at a specified tier.
- `parked`: plausible but missing a required data source or modality.
- `demoted`: evidence-driven failure under current standards.
- `prior_art_recalibration_pending`: V3 demotion needs V4 review.
- `validation_ready`: Tier 4 package is ready for synthesis or handoff.

## Tier 0 - Triage

Budget: about 15 active minutes per candidate.

Advance if all are true:
- V4 contribution is explicit.
- At least one support channel beyond the V3 baseline exists.
- No fatal modality blocker under current biotech capability.

Demote if:
- Contribution is only "known target is interesting".
- Biology was disconfirmed independent of prior art.
- Correct-direction modality is not conceivable.

## Tier 1 - Mechanism

Budget: about 2 active hours per candidate.

Advance if:
- Molecule-to-cell-to-tissue chain has at least two evidenced steps.
- Evidence spans at least three orthogonal dimensions.
- Real perturbation or foundation-model support survives veto checks.

Demote if:
- Mechanism relies on one weak proxy.
- Direction of intervention remains ambiguous after focused testing.
- Cross-disease claim collapses to a single disease without a reason.

## Tier 2 - Causal Evidence

Budget: about 4 active hours per candidate.

Advance if:
- At least one longitudinal or natural-experiment dimension supports the claim.
- Genetic causal inference is attempted when applicable.
- Direction of effect is supported by perturbation or cross-species evidence.

Demote if:
- Candidate remains purely cross-sectional.
- Genetic and perturbation directions conflict without a resolution.

## Tier 3 - Translational Feasibility

Budget: about 4 active hours per candidate.

Advance if:
- Druggability or modality precedent exists.
- Tissue delivery is plausible for the lead indication.
- Biomarker readout for target engagement is specified.
- Safety and failure modes are explicit.

Demote if:
- Target engagement cannot be measured.
- Safety margin is incompatible with chronic autoimmune use.
- Required delivery is not feasible with current technology.

## Tier 4 - Validation-Ready

Budget: as needed.

Output requires:
- Therapeutic claim with target, indication, subgroup, and mechanism.
- Five orthogonal dimensions, including longitudinal or natural experiment.
- V4 prior-art contribution.
- Mechanistic chain with perturbation or simulation grounding.
- Translational audit.
- Falsification plan with wet-lab and clinical stop-loss criteria.
- Reproducible code, manifests, and environment.

## Resource Allocation

- Tier 0 receives small fixed budgets.
- Tier 1 receives focused mechanism scripts and limited subagents.
- Tier 2 receives dimensional expansion and causal methods.
- Tier 3 receives druggability, delivery, biomarker, and trial simulation.
- Tier 4 receives full synthesis and hostile review cycles.

Higher-tier candidates take priority over lower-tier candidates. Lower-tier
work may continue in parallel via subagents only when it does not block the
highest-tier work.
