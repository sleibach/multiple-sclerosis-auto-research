# Gafson DMF Data Request: Ready-To-Send Draft V45

Status: unsent draft. Send only if the medical team approves the external
contact. Save the exact sent text separately after sending.

To: corresponding author/team for Gafson et al. 2018, PMID `30283812`

Subject: `Data request for DMF PBMC RNA-seq response cohort (PMID 30283812)`

Attachments/references to mention if useful:

- `docs/validation/PREREGISTRATION_V42.md`
- `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- `docs/validation/CLINICAL_DATA_DICTIONARY_CRF_V45.md`
- `docs/validation/MEDICAL_TEAM_COHORT_SPEC_V45.md`

## Email Body

```text
Dear Dr. Gafson and colleagues,

I am working on an independent, pre-specified validation of an early
treatment-response transcriptomic monitoring rule in multiple sclerosis. Your
dimethyl fumarate PBMC RNA-seq cohort is the best match we have identified
because it includes baseline, early on-treatment, and later samples together
with NEDA-4 response status.

Would you be willing to share processed and/or raw expression data and
sample-level metadata for the cohort in PMID 30283812?

The minimum files needed are:

- gene expression matrix for all baseline, 6-week, and 15-month PBMC samples;
- sample-to-patient mapping;
- sample timepoint labels and exact days since treatment where available;
- NEDA-4 responder/nonresponder status per patient;
- gene identifiers used in the expression matrix;
- data dictionary for all labels/codes.

If available, these covariates would make the pre-specified confounder audit
substantially more informative:

- relapse, MRI, disability, brain-volume-loss, and other NEDA-4 component
  outcomes;
- glucocorticoid/steroid exposure, dose, timing, and indication;
- sequencing run, lane, library-preparation, batch, processing-date, and other
  technical metadata;
- sample-level QC metrics such as library size, mapping rate, mitochondrial or
  ribosomal fraction, and any contamination/ambient-RNA estimates;
- blood counts, PBMC composition, or deconvolution/cell-count covariates;
- age, sex, MS subtype, disease duration, prior/concomitant DMT exposure, and
  baseline disease activity if shareable.

The analysis plan is frozen before data access. We will apply the locked rule
without re-fitting and will report the raw result together with pre-specified
confounder and batch/QC diagnostics. The report will not rely on p-values alone:
it uses effect-size and confidence-interval criteria, and underpowered or
technically flagged results will be reported as inconclusive or non-clean rather
than forced into a positive interpretation.

We can work with raw counts, normalized expression, or both, and will follow any
data-use terms you require.

Kind regards,

[Name / affiliation]
```

## If Data Are Received

Place files under:

```text
data/raw_v3/gafson_dmf_2018/
```

Required gates before analysis:

1. preserve original filenames and terms;
2. checksum all files;
3. run `scripts/v45_validation_intake_preflight.py`;
4. verify paired baseline/6-week samples and NEDA-4 labels;
5. run `scripts/v42_gafson_validation_harness.py` mechanically under V42/V44/V45
   readiness docs.
