# V57 Prospective Balanced-Batch Design Result

## Scope

This is **seeded synthetic method characterization only**. It makes no claim
about MS biology and changes neither the locked V22 score nor the V42/V44
validation rules. It asks whether batch confounding can be prevented at the
laboratory-layout stage rather than only detected afterward.

## Result

| method | median response imbalance | maximum response imbalance | median design imbalance | mean null raw AUC >=0.70 | max null raw AUC >=0.70 |
|---|---:|---:|---:|---:|---:|
| capacity_random | 0.503 | 0.778 | 0.688 | 0.0036 | 0.0072 |
| outcome_blind_constrained | 0.503 | 0.869 | 0.346 | 0.0049 | 0.0107 |
| outcome_aware_constrained | 0.302 | 0.372 | 0.363 | 0.0015 | 0.0021 |

- Method gate: **PASS**.
- All 27 layouts kept paired samples together and placed equal
  baseline and early sample counts in every batch.
- Scale: 540,000 technical-null
  cohorts across three cohort structures, three seeds, and three methods.

## Decision

The prospective option is a computer-generated, capacity-constrained layout
that keeps each patient's timepoints together and, when finalized labels exist,
balances response together with site, sex, and age stratum. The laboratory must
remain blinded to labels. If labels cannot legitimately be used before
processing, use the outcome-blind layout and do **not** claim response balance.

This is prevention, not a replacement for the V44 guard: batch/QC metadata and
the pre-specified diagnostic remain mandatory because unmeasured technical
structure can persist. The method has not been tested on a real validation
cohort and cannot validate the APC/HLA-II signal.
