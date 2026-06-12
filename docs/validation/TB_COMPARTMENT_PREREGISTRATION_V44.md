# T/B COMPARTMENT MONITORING PREREGISTRATION V44

Status: frozen validation-readiness plan for a future compartment-resolved
treatment-response cohort. Date: 2026-06-12.

This is a preparation artifact, not a new finding. It freezes a test of the
V35/V36 T/B-readable monitoring state without changing the immutable V22 scalar.

## Hypothesis

The V36 interpretation is not that T/B compartments define a new independent
mechanism. The frozen test is narrower:

> The broad early IFN/APC/STAT1 treatment-response monitoring state is readable
> in B/plasma-like and T-like compartments, with B/plasma-like remodeling the
> more stable carrier and T-like remodeling a companion readout vulnerable to
> composition/QC.

## Required Cohort

Human treatment-response transcriptomic cohort with:

- baseline plus early on-treatment samples;
- response/remission/NEDA or comparable binary outcome;
- compartment resolution by single-cell, CITE-seq, sorted T/B/myeloid
  expression, or a pre-specified validated deconvolution sufficient to score
  T-like and B/plasma-like compartments;
- cell counts/fractions and batch/QC metadata.

Preferred therapy domain:

- immune-remodeling/JAK-STAT or DMF-like contexts, matching the bounded V22/V23
  lead.

Not acceptable for primary validation:

- bulk-only cohort without validated compartment estimates;
- response labels absent;
- only post-treatment samples without baseline;
- post-hoc selected compartments.

## Frozen Features

Use the V22 module definitions:

- IFN/APC: `STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`, `CD74`, `HLA-DRA`
- HLA-II: `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `HLA-DQA1`,
  `HLA-DQB1`

For each eligible compartment:

`locked_delta = delta_HLAII - delta_IFN_APC`

Primary compartment readouts:

1. `B/plasma-like locked_delta`
2. `T-like locked_delta`

No fitted weights and no post-hoc compartment combination are allowed. B/plasma
and T-like readouts are reported separately. A T/B mean may be reported
descriptively only after the two fixed readouts are shown.

## Frozen Primary Test

Responder-higher orientation is fixed.

Clean T/B-readable support requires all:

- B/plasma-like AUC `>= 0.70`;
- B/plasma-like Hedges g `>= 0.50`;
- lower B/plasma-like bootstrap 95% AUC CI `> 0.55` for `n >= 30`;
- T-like AUC `>= 0.60` in the same direction;
- B/plasma-like residual AUC after compartment fraction/count adjustment
  `>= 0.65`;
- no batch guard flag that makes the result technically non-specific.

The B/plasma criterion is primary because V36 showed it was more stable after
composition adjustment than the T-cell component.

## Failure And Inconclusive Criteria

Fail:

- adequate-power cohort (`n >= 30`) with B/plasma-like AUC `< 0.60` or Hedges g
  `< 0.20`;
- B/plasma-like direction opposite to prediction with AUC `< 0.45`;
- B/plasma-like signal disappears after composition adjustment
  (residual AUC `< 0.55`) in an otherwise adequate cohort.

Inconclusive:

- missing compartment coverage;
- insufficient response labels;
- too few subjects per response group;
- batch/composition artifacts cannot be separated.

## Composition And Technical Audits

The future run must report:

- baseline and delta T-like, B/plasma-like, and myeloid/APC fractions or counts;
- residualized B/plasma-like and T-like locked deltas after fraction/count
  adjustment;
- V44 batch diagnostics where metadata exist;
- leave-one-subject influence;
- timepoint leverage, especially if one treated sample is much later than the
  rest.

None of these audits can rescue a failed primary B/plasma readout.

## Synthetic Harness Check

Script:

- `scripts/v44_secondary_lead_harnesses.py`

Outputs:

- `analysis/v44_secondary_lead_harnesses/secondary_harness_summary.json`
- `analysis/v44_secondary_lead_harnesses/secondary_harness_metrics.tsv`
- `analysis/v44_secondary_lead_harnesses/synthetic/tb_null_synthetic.tsv`
- `analysis/v44_secondary_lead_harnesses/synthetic/tb_planted_synthetic.tsv`

Synthetic result:

- null synthetic: B/plasma AUC `0.442`, expected fail, observed fail;
- planted synthetic: B/plasma AUC `0.853`, B/plasma residual AUC `0.861`, T-like
  AUC `0.614`, expected pass, observed pass.

Synthetic data are method checks only and are not evidence about MS.

## Interpretation Grid

| Future result | Interpretation |
|---|---|
| Clean pass | Supports T/B-readability of the monitoring state; does not create a new independent T/B mechanism. |
| B/plasma pass, T-like fail | Supports B/plasma-readable state only; demote broad T/B wording. |
| Raw pass but composition/batch-confounded | Non-specific compartment artifact until replicated or technically resolved. |
| Adequate-power fail | Demote T/B-readable lead; keep V22 scalar as primary validation target. |
| Inconclusive | Use effect size and artifacts to define next acquisition; do not promote. |

