# V57 Hierarchical Environment Model

## Boundary

This compares transport methods around the frozen cohort effects. It is not a
new biomarker or biological finding.

## Result

- Environments: 4
- Reference-prior LOO log-score gain over `tau=0`: -0.192
- Within-cohort label-permutation p: 0.3748
- Gain range over 12 prior settings: -0.775 to
  -0.053
- Worst reference-prior held-cohort gain: -0.136

Verdict: **HIERARCHICAL_MODEL_NOT_READY**.

With four environments, explicitly modeling heterogeneity does not earn a
dedicated biological interpretation unless it improves unseen-cohort
prediction robustly across priors and beyond the label null. Failure of that
gate means a richer hierarchy is not a substitute for additional independent
MS environments.
