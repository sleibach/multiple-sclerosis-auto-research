# V38 adversarial inversion prompt

You are an adversarial reviewer. Treat model output as proposal-only.

Project claim to invert:

The bounded V22/V23 APC/HLA-II early treatment-response scalar is the primary
provisional MS validation lead. It is pre-locked, positive in the bounded
DMF + exact tofacitinib set, statistically tool-robust under V28, and not
explained by glucocorticoid or simple composition controls in V32. It is still
small-n, immune-tone bounded, and externally unvalidated.

Known evidence summary:

- Bounded set: n=19, AUC 0.811, permutation p 0.008, Hedges g 1.191.
- Unbounded primary locked all: n=34, AUC 0.547.
- DMF alone: AUC 0.72, n=10. Fingolimod: AUC 0.60, n=10. Adalimumab: AUC 0.511,
  n=14. Exact tofacitinib: AUC 0.95, n=9, cross-disease.
- V32 broad metabolic/inflammatory/STAT1 joint adjustment attenuates AUC to
  0.656, p 0.163; steroid/composition adjustments survive.
- Flexible ML/coupled/dynamic variants do not beat the scalar.

Task:

Return JSON only with 4-6 concrete adversarial inversion hypotheses. Each item
must include:

- `inversion`: the strongest way the claim could be wrong or overstated.
- `grounding_test`: a concrete test using the existing committed tables above.
- `expected_demotion_if_true`: how the claim should be demoted if the test
  supports the inversion.

Do not propose new data acquisition as a grounding test. Do not treat your
answer as evidence.
