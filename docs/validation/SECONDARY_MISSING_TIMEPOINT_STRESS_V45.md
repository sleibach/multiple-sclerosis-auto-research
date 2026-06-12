# V45 Secondary Missing-Timepoint / Dropout Stress Check

Status: synthetic method-characterization. No biological claim.

## Purpose

V45 already stress-tested secondary postpartum and T/B harnesses against
batch/composition/pathology artifacts. This focused check tests the operational
failure modes most likely in small external cohorts:

1. missing required sample identifiers for paired analyses;
2. row-level dropout that reduces analyzable paired subjects.

Generator:

`scripts/v45_secondary_missing_timepoint_stress.py`

Outputs:

- `analysis/v45_secondary_missing_timepoint_stress/summary.json`
- `analysis/v45_secondary_missing_timepoint_stress/secondary_missing_timepoint_stress.tsv`
- synthetic inputs and per-scenario harness outputs under
  `analysis/v45_secondary_missing_timepoint_stress/`

## Scale

| Metric | Value |
|---|---:|
| secondary leads tested | 2 |
| truth modes | null, planted |
| row-dropout fractions | 0%, 10%, 25%, 40%, 60% |
| stress rows | 24 |
| bootstrap replicates per run | 120 |
| required-field failures expected | 4 |
| unexpected required-field passes | 0 |
| row-dropout run errors | 0 |

## Required Field Result

The harnesses correctly hard-fail before metrics when required paired sample
fields are missing:

| Lead | Missing field | Observed |
|---|---|---|
| postpartum APC-arm | `postpartum_sample` | expected failure |
| T/B compartment | `treated_sample` | expected failure |

This means a future cohort with missing sample-pair identifiers is not
interpretable by the secondary harness until the metadata are repaired.

## Row-Dropout Result

### Postpartum APC-Arm

| Truth | Dropout | n retained | AUC | Guarded clean pass | Interpretation |
|---|---:|---:|---:|---:|---|
| null | 0% | 60 | 0.508 | false | fail |
| null | 60% | 25 | 0.571 | false | inconclusive |
| planted | 0% | 60 | 0.993 | true | clean pass |
| planted | 25% | 40 | 0.995 | false | raw pass batch-flagged non-specific |
| planted | 60% | 28 | 0.990 | false | small-n directional provisional |

### T/B Compartment

| Truth | Dropout | n retained | AUC | Guarded clean pass | Interpretation |
|---|---:|---:|---:|---:|---|
| null | 0% | 60 | 0.416 | false | fail |
| null | 60% | 22 | 0.542 | false | inconclusive |
| planted | 0% | 60 | 0.951 | true | clean pass |
| planted | 40% | 43 | 0.963 | true | clean pass |
| planted | 60% | 24 | 0.874 | false | small-n directional provisional |

## Interpretation

The secondary harnesses behave conservatively under missingness:

- missing required paired sample fields stop the run before metrics;
- high dropout does not create synthetic clean false positives;
- high dropout can demote a planted signal to provisional/inconclusive due to
  small n or diagnostic flags.

The practical consequence matches the V45 primary power guidance: future
secondary cohorts should be requested with enough enrollment to retain adequate
paired analyzable subjects after missing late-pregnancy/postpartum or
baseline/early-treatment samples.

## Guardrail

These are synthetic method checks only. They do not support or refute postpartum
or T/B biology. They only characterize how the frozen secondary harnesses behave
when metadata are incomplete or paired subjects are lost.
