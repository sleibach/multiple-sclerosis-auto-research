# V54 Progression Endpoint-Confirmation Error Audit

Status: **synthetic method audit complete; score-linked confirmation error
invalidates inference**.

## Boundary

This is seeded, labeled synthetic method characterization. It estimates no MS
effect, event rate, or real adjudication-error rate. It does not alter a locked
rule, endpoint, or pre-registration. The frozen design is in
`docs/plans/PROGRESSION_CONFIRMATION_ERROR_V54.md`; executable outputs are in
`analysis/v54_progression_confirmation_error/`.

## Scale And Gate

The run generated 230,400 cohorts over three seeds, three analyzable sample
sizes, two event probabilities, null and HR-1.5 states, and eight confirmation
mechanisms. Every cell used blinded within-site score standardization and a
site-stratified Cox route. Each mechanism's six-cell null family was adjudicated
before any positive-performance or minimum-N result was read.

## Grounded Method Result

Four mechanisms calibrated:

- complete confirmation;
- 10% independent missed confirmation;
- 10% latent-risk-only missed confirmation; and
- 2% independent false confirmation.

Four mechanisms were invalid and are excluded from power interpretation:

| Mechanism | Maximum null call rate | Direction at maximum | Verdict |
|---|---:|---|---|
| score-dependent missed confirmation | 0.329 | negative/protective | invalid |
| joint score/risk missed confirmation | 0.407 | negative/protective | invalid |
| score-dependent false confirmation | 0.335 | positive/harmful | invalid |
| joint miss plus score-dependent false confirmation | 0.104 | predominantly negative | invalid |

These are not ordinary losses of sensitivity. Outcome confirmation that depends
on the molecular score, directly or jointly with latent risk, can manufacture
an association under the null. A high apparent positive-call rate is therefore
not interpretable when the corresponding null family is invalid.

Among calibrated families, the HR-1.5 reference reaches the frozen rule at
`n=900` with 15% events and `n=450` with 30% events under complete
confirmation. Independent error and risk-only missed confirmation retain those
same thresholds in this generator. That does not make those values universal
sample-size requirements.

## Operational Consequence

A future P1 package must supply endpoint-adjudication provenance sufficient to
exclude score-linked or joint score/risk confirmation. Unknown dependence is a
fail-closed interpretation boundary. It cannot be repaired by post-result
adjustment or relabeled as reduced power. The audit supports acquisition of
confirmation dates, ascertainment process, assessor blindness, missing-
confirmation reasons, and source/site-specific adjudication metadata before
score access.

The result concerns method trustworthiness only. It supplies no evidence that a
molecular state predicts or can halt MS progression.
