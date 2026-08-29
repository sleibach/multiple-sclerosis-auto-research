# V57 V22 Specification-Curve Audit

## Result

All 26 frozen V32 specifications were included: 23
single-confounder adjustments and 3 named joint risk
sets. Adjusted AUC ranged from 0.656 to
0.978 (median 0.861),
versus raw AUC 0.811.

- responder-higher direction: 100.0%;
- adjusted AUC >= 0.60: 100.0%;
- nominal stratified-permutation p <= 0.05: 96.2%;
- positive leave-one-out incremental AUC: 100.0%.

The predeclared aggregate gates all pass. This means the score's direction,
practical discrimination, and incremental value are not dependent on selecting
one favorable V32 adjustment. It does **not** make these specifications
independent replications or validate V22 externally.

## Mandatory Least-Favorable Result

`joint:metabolic_inflammatory_stat1` was least favorable: adjusted AUC
0.656, permutation p
0.163, and incremental leave-one-out
AUC +0.122. The specifications
without nominal permutation support were: `joint:metabolic_inflammatory_stat1`.

That broad metabolic/inflammatory/STAT1 joint adjustment remains the important
exception and preserves V32's **partially confounded / immune-tone bounded**
interpretation. The aggregate curve strengthens robustness to ordinary
specification choice; it does not erase the broad-joint attenuation or the need
for an external cohort.

## Epistemic Boundary

This is a reanalysis of existing held subjects and frozen V32 outputs. It is a
methodological robustness result, not new MS discovery, not a revised locked
rule, and not external validation. Nominal p-values are displayed as stress-test
diagnostics and are not counted as independent evidence.
