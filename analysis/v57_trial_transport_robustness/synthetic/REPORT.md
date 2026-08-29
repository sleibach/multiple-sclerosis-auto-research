# V57 Trial-Transport Robustness Audit

## Synthetic-Only Result

- Synthetic trial pairs: 2,700
- Participants per source/target pair: 2,400/2,400
- Seeds: 57101, 57102, 57103
- Candidate verdict: **CANDIDATE_TRANSPORT_HARNESS_NOT_VERIFIED**
- Original V57 transport verdict: **UNCHANGED FAILED**

| Gate | Passed under every seed |
|---|---|
| eligible_scenarios_overlap | False |
| linear_correct_estimators | True |
| sampling_wrong_one_nuisance_robust | True |
| outcome_wrong_one_nuisance_robust | True |
| both_wrong_quadratic_rescue | True |
| hidden_modifier_detected | True |
| positivity_rejected | True |

## Interpretation

Six of seven gates passed. The only failed gate was overlap eligibility for
the two variance-shift scenarios: seed-specific pass rates were 19.3%-26.0%.
The candidate guard did not fail because of its weight-tail threshold;
effective sample fractions and weighted first/second-moment balance were at
or beyond their frozen boundaries. The linear estimator nevertheless met its
one-correct-nuisance accuracy gate, and the quadratic estimator rescued the
both-wrong scenario, but a real transport analysis must still fail closed when
the observed populations have this little usable overlap.

This audit therefore removes the sample-maximum defect but does not verify the
full harness. A fixed-guard severity sweep can map where population shift
becomes ineligible; it cannot retroactively rescue either failed result. The
method also cannot establish source-to-target exchangeability in a real trial.
Synthetic verification never constitutes MS or treatment evidence.
