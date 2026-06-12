# Clinical Data Dictionary / CRF Checklist V45

Status: collaborator-facing acquisition checklist. This is derived from the
frozen V42 preregistration, V43 power map, V44 batch guard, and V45 cohort
specification. It does not change the locked V22 rule or any threshold.

Machine-readable checklist:

- `docs/validation/input_schemas/V45_clinical_crf_checklist.tsv`

## Primary V22/V42 DMF/NEDA-Style Validation

Decision-grade target:

- minimum: `30` responders and `30` nonresponders only if the effect is large
  and labels/QC are clean;
- preferred: `60-80` responders and `60-80` nonresponders under realistic label
  noise, immune-tone confounding, or batch imperfections;
- `10-15` per group should be treated as effect-size/CI information unless the
  effect is very large and diagnostics are clean.

### Required Files

1. Expression matrix:
   - raw counts preferred, processed normalized expression acceptable if
     documented;
   - rows as genes/features, columns as sample IDs;
   - gene identifiers and annotation/mapping table.
2. Sample metadata:
   - sample ID, subject ID, timepoint, exact days since treatment;
   - treatment name/class;
   - sample QC pass/fail;
   - batch/run/library/lane/date fields.
3. Clinical outcome table:
   - subject ID;
   - binary NEDA-4 or equivalent responder/nonresponder label;
   - outcome assessment window;
   - component outcomes: relapse, MRI activity, disability progression, brain
     volume loss if applicable;
   - missingness/censoring reason.
4. Clinical covariates:
   - steroid/glucocorticoid exposure, dose, date, indication;
   - relapse/infection near draw;
   - prior/concomitant DMTs and washout;
   - age, sex, disease subtype, disease duration, baseline EDSS;
   - lymphocyte count and major immune-cell counts/fractions if available.
5. Data dictionary:
   - definitions of all codes/labels;
   - unit conventions;
   - data-use terms and publication permission for aggregate metrics.

### Required Timepoints

Primary:

- baseline before treatment or before biologically meaningful exposure;
- early on-treatment sample, ideal `4-8` weeks, acceptable `1-12` weeks only if
  exact days are recorded;
- long-term clinical outcome window, ideal `12-15` months for NEDA-4.

Optional:

- later transcriptomic timepoint for pharmacodynamic context.

### Clean-Validation Technical Requirements

A clean validation requires:

- sample-mapped outcome labels;
- paired baseline/early samples for both response groups;
- V22 module coverage;
- batch metadata that do not strongly track response;
- steroid and immune-tone/confounder panels scoreable;
- no large outlier or normalization pathology;
- receptor-only score does not outperform the locked score by AUC `>= 0.10`.

If these fail, the cohort may still inform effect size and future power, but it
does not produce a clean validation.

## Secondary Lead Add-Ons

### Postpartum APC-Arm

Required add-on fields:

- late-pregnancy sample ID;
- early postpartum sample ID, target `4-8` weeks;
- relapse status through 3 months postpartum;
- HLA-II and CD64/FCGR1 feature coverage;
- DMT stop/restart timing;
- steroid exposure, infection, lactation, and batch metadata.

### T/B Compartment Monitoring

Required add-on fields:

- baseline and early treated sample IDs;
- response/NEDA/remission label;
- B/plasma-like and T-like compartment scores, or single-cell/sorted expression
  sufficient to compute them;
- B, T, and myeloid fractions/counts;
- compartment method and coverage;
- steroid and batch metadata.

## Operational Intake Rule

When data arrive:

1. place files under the cohort-specific raw/quarantine directory;
2. compute checksums before opening;
3. update the manifest;
4. confirm the relevant preregistration applies;
5. if a cohort differs materially from the frozen plan, write an addendum before
   scoring outcomes;
6. run only the matching frozen harness.

