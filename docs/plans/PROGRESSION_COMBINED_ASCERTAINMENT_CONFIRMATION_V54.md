# V54 Combined-Ascertainment Independent Confirmation

Status: frozen on 2026-07-22T01:07:15Z after the primary family result was
observed and before any confirmation run.

## Why Confirmation Is Required

The frozen primary audit classified `weak_joint_all` under the guarded route as
family-invalid: maximum null call probability `0.0617`, Wilson lower bound
`0.0527`, and six-cell family tail `0.0363`. The three constituent weak-joint
families calibrated. The elevation was not uniform across primary seeds.

That is sufficient under the original rule but too close to the boundary to
lead without an independent replication. This confirmation is a separate,
transparent post-primary check, not a replacement or tuning of the primary.

## Frozen Confirmation

- independent seeds: `55201`, `55207`, `55213`;
- `2,000` cohorts per seed/cell;
- sample sizes `180`, `320`, `450`;
- event probabilities `0.15`, `0.30`;
- molecular HR fixed to null `1.0`;
- stacks: attendance weak-joint, death weak-joint, switch weak-joint, and all
  three weak-joint processes;
- route: guarded within-site standardized, site-stratified Cox only;
- generator, censoring targets, coefficients, score reliability, and family
  adjudication exactly as in the primary plan.

Confirmation requires all three constituents to remain calibrated and the
combined family to remain invalid under the same strict-cell plus family-tail
rule. If it does not, the primary result is reported as marginal/non-replicated
and cannot establish compounded invalidity.

## Boundary

This is independent synthetic method replication only. It is not evidence that
any MS cohort follows the simulated ascertainment process or that a molecular
state predicts progression.
