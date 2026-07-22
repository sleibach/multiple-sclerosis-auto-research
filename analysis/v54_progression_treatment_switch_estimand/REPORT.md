# V54 Treatment-Switch Estimand Audit

Status: **ESTIMAND_MUST_BE_FROZEN_SWITCHING_CAN_CHANGE_OR_INVALIDATE_INTERPRETATION**.

This is seeded synthetic method behavior only. It is not evidence about an MS
treatment, switching process, molecular predictor, or effect.

## Invalid Direct-Prognostic Families

- `joint_score_progression_risk|censor_at_switch`
- `joint_score_progression_risk|treatment_policy`
- `score_dependent|treatment_policy`

## Strict-Cell Flags Compatible With Family Maxima

- `independent|censor_at_switch`
- `independent|treatment_policy`

These families are not called invalid, but are conservatively excluded from
positive-performance interpretation. The initial implementation overcalled
them by omitting the already-frozen family-maximum adjudication; that mismatch
was corrected before this result was committed.

## Calibrated Families

- `none|censor_at_switch`: median null `0.048`, maximum `0.058`.
- `none|treatment_policy`: median null `0.048`, maximum `0.058`.
- `progression_risk_dependent|censor_at_switch`: median null `0.046`, maximum `0.049`.
- `progression_risk_dependent|treatment_policy`: median null `0.046`, maximum `0.052`.
- `score_dependent|censor_at_switch`: median null `0.052`, maximum `0.057`.

The treatment-policy route follows observed post-switch outcomes and therefore
answers a policy-specific association question. When treatment assignment
depends on score and the treatment changes progression hazard, a non-null score
association can arise even when the direct molecular progression HR is one.
That is not the untreated prognostic estimand.

Censoring at switch removes post-switch treatment effects but is not a generic
repair: joint score/progression-risk switching can select the risk set and must
be audited as informative censoring. Both estimands must be frozen and reported;
neither may be selected because its direction or p-value is favorable.

## Boundary

These simulations identify method failure regimes under a fixed generator.
They do not select a clinical estimand, estimate causal treatment effects, or
show that any molecular state predicts or halts MS progression.
