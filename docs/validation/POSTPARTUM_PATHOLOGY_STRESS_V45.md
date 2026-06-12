# V45 Postpartum APC-Arm Harness Pathology Stress Test

## Status

Synthetic method-characterization only. These results are not biological
evidence about postpartum MS. No real postpartum MS cohort was read, and the
frozen V44 postpartum pre-registration was not changed.

## Question

V44 pre-registered the postpartum HLA-II/CD64 APC-arm hypothesis and verified
basic null/planted synthetic mechanics. V45 stress-tested whether realistic data
pathologies would cause false clean passes or make a true signal
uninterpretable.

## Simulation

Script:

- `scripts/v45_postpartum_harness_pathology_simulation.py`

Outputs:

- `analysis/v45_postpartum_pathology/summary.json`
- `analysis/v45_postpartum_pathology/postpartum_pathology_summary.tsv`
- `analysis/v45_postpartum_pathology/postpartum_pathology_metrics.tsv`
- `analysis/v45_postpartum_pathology/synthetic/postpartum_pathology_subjects.tsv.gz`

Scale:

- `6,300` seeded synthetic cohorts.
- Up to `378,000` synthetic subject rows before missing-timepoint attrition.
- `90` replicates per truth / pathology / severity cell.
- Pathologies: missing postpartum timepoint, response-correlated steroid,
  DMT-restart imbalance, response-correlated batch, combined
  steroid/DMT/batch, timepoint jitter, and module-coverage loss.

## Headline Results

| Metric | Result |
|---|---:|
| Worst synthetic-null raw primary pass rate | `0.7667` |
| Worst synthetic-null guarded clean pass rate | `0.0222` |
| Worst planted guarded-clean pass drop | `1.0000` |

Interpretation:

- Severe response-correlated batch can produce a high raw false-positive rate
  in the postpartum score if ignored.
- The pre-specified guard prevents those artifacts from being called clean:
  synthetic-null guarded clean pass never exceeded `0.0222`.
- The guard is conservative. True planted signals with severe batch imbalance
  or module-coverage loss are downgraded to non-specific or mechanically
  unscoreable, which is the correct failure mode for validation readiness.

## Pathology-Specific Takeaways

### Response-Correlated Batch

Synthetic null:

- severity `1.00`: raw pass `0.7667`, guarded clean pass `0.0000`;
- severity `0.75`: raw pass `0.2222`, guarded clean pass `0.0000`.

Planted:

- severity `0.75` and `1.00`: raw pass `1.0000`, guarded clean pass `0.0000`.

Decision: a future postpartum raw positive with response-correlated batch is
not a clean validation. It may still be biologically interesting, but it must be
reported as technically non-specific until replicated or batch-resolved.

### Steroid / DMT Imbalance

Steroid and DMT imbalance alone produced far lower synthetic-null clean-pass
risk than batch, but combined steroid/DMT/batch pathology generated raw null
passes up to `0.1222`, all prevented from clean interpretation by the guard.

Decision: steroid exposure and DMT restart timing remain mandatory metadata.

### Missing Timepoints

Missing postpartum samples primarily reduce information rather than producing a
large synthetic-null false-positive problem. At severity `1.00`, planted cohorts
still had raw pass `1.0000` but guarded clean pass `0.7222` because attrition and
chance diagnostic flags reduce clean interpretability.

Decision: a future postpartum validation should require late-pregnancy and
early-postpartum paired samples for as many subjects as possible; attrition
turns the result into an effect-size estimate, not a definitive test.

### Module-Coverage Loss

Severe synthetic module-coverage loss made planted cohorts mechanically fail or
be marked unscoreable despite high raw AUC values:

- severity `0.75`: planted raw primary pass `0.0000`, module coverage flag
  `1.0000`;
- severity `1.00`: planted raw primary pass `0.0000`, module coverage flag
  `1.0000`.

Decision: HLA-II and CD64/FCGR1 feature coverage is a hard acquisition
requirement for postpartum validation.

## Trustworthy Envelope

A future postpartum APC-arm validation is interpretable only if:

1. late-pregnancy and early-postpartum samples are paired and response labels
   are available;
2. HLA-II and CD64 arms meet the V44 coverage rules;
3. steroid exposure and DMT stop/restart are recorded;
4. batch metadata are recorded and not strongly response-correlated;
5. early postpartum timing is close enough to the pre-specified 4-8 week window
   to avoid interpreting timing noise as biology.

If any of these fail, the result can still be useful for power/effect-size
planning, but it should not be promoted as a clean validation.

