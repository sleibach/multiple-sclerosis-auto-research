# Gafson DMF PBMC RNA-seq Data Request V36

Purpose: obtain the best identified fresh validation cohort for the locked
V22/V23 APC/HLA-II treatment-response monitoring rule, with the V36 secondary
audit covariates.

## Target Study

- Gafson et al. 2018
- PMID: `30283812`
- DOI: `10.1212/nxi.0000000000000470`
- Design noted in V24 scout: RRMS patients treated with dimethyl fumarate,
  PBMC RNA-seq at baseline, 6 weeks, and 15 months, with NEDA-4 response status.

## Suggested Email Subject

Data request for DMF PBMC RNA-seq response cohort (PMID 30283812)

## Request Text

Dear Dr. Gafson and colleagues,

I am working on an independent validation of a pre-specified early
treatment-response transcriptomic monitoring rule in multiple sclerosis. Your
dimethyl fumarate PBMC RNA-seq cohort is the best match we have identified
because it includes baseline, early on-treatment, and later samples together with
NEDA-4 response status.

Would you be willing to share processed and/or raw expression data and
sample-level metadata for the cohort in PMID 30283812?

The minimum files needed are:

- gene expression matrix for all baseline, 6-week, and 15-month PBMC samples;
- sample-to-patient mapping;
- NEDA-4 responder/nonresponder status per patient;
- sample timepoint labels;
- gene identifiers used in the expression matrix.

If available, these covariates would be especially valuable for a pre-specified
confounder audit:

- relapse, MRI, disability, and other NEDA-4 component outcomes;
- concomitant glucocorticoid/steroid exposure, dose, and timing;
- batch, lane, library-preparation, sequencing-run, or processing-date metadata;
- sample-level QC metrics such as library size, mapping rate, mitochondrial or
  ribosomal fraction, and any ambient RNA/contamination estimates;
- blood count, PBMC composition, or deconvolution/cell-count covariates;
- age, sex, disease duration, prior DMT exposure, and baseline disease activity
  if shareable under your data-use terms.

The primary analysis will apply a locked rule without re-fitting. Secondary
pre-specified audits will test baseline versus early on-treatment dynamics,
STAT1/IFN-axis dependence, glycolysis coupling, cell-composition effects, and
technical QC/batch sensitivity.

We can work with either raw counts, normalized counts, or both, and will follow
any data-use conditions you require.

Kind regards,

[Name / affiliation]

## Placement Once Obtained

Place received files under:

`data/raw_v3/gafson_dmf_2018/`

Suggested naming:

- `expression_counts.tsv` or `expression_normalized.tsv`
- `sample_metadata.tsv`
- `data_dictionary.tsv`
- `README_source.txt`

After placement, run:

```bash
shasum -a 256 data/raw_v3/gafson_dmf_2018/* > data/raw_v3/gafson_dmf_2018/SHA256SUMS
```

Then update `data/manifest.tsv` and run the locked validation harness only after
confirming the cohort was not used for rule construction.
