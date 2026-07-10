# Data Owner Package README V52

Date: 2026-07-10

Status: external-facing package guide. This document adds no evidence and does
not change any validation rule. It tells a data owner what package to send so the
project can classify it mechanically before analysis.

## What To Send First

Send a manifest before sending raw data. The manifest should state:

1. what data type is available;
2. whether subject-level data can be shared or only aggregate summaries;
3. allowed-use terms;
4. whether paired samples, labels, genotype, or perturbation readouts are
   present;
5. expected file sizes and formats.

Do not send restricted raw data until the allowed-use terms are clear.

Use `docs/validation/INCOMING_PACKAGE_MANIFEST_TEMPLATE_V52.tsv` as the starting
manifest shape. The `provided_fields` column should list semicolon-separated
field names that match the route classifier and field dictionary.

## Package Types We Can Use

| package type | minimum content | likely route |
|---|---|---|
| paired DMF-like PBMC response | baseline and early treatment PBMC expression, response labels, subject IDs, feature map, batch/QC metadata | monitoring validation |
| chr1 genotype-linked immune or CSF readout | chr1 credible-set dosage, ancestry PCs, candidate-gene expression/protein, cell-state labels | chr1 target-resolution handoff |
| chr1 direction-matched perturbation | resolved candidate gene, protective direction, matched perturbation, MS-relevant phenotype, controls | chr1 modality workup |
| postpartum MS relapse-window data | postpartum timing, relapse timing, immune profile, APC/HLA-II/CD64 coverage, treatment/confounder metadata | secondary biology validation |
| T/B compartment data | T/B resolution, timing or labels, composition metadata, batch/QC metadata | secondary monitoring validation |
| treatment-timed expression without response labels | treatment timing and expression or immune profile | pharmacodynamic context only |
| protein structure or tractability file | protein ID, source and version, confidence metrics, relationship to lead | feasibility context only |
| aggregate paper table or plot | source description and available fields | acquisition lead or context only |

## What Makes A Monitoring Package Scoreable

A scoreable monitoring package needs:

1. stable subject IDs;
2. baseline PBMC expression;
3. early on-treatment PBMC expression;
4. subject-level response labels;
5. expression feature annotation;
6. enough V22 module gene coverage;
7. batch/QC metadata sufficient for the pre-specified guard.

Steroid, relapse, infection, DMT timing, and cell-count metadata are strongly
preferred because they determine how much trust can be placed in the result.

## What Makes A Chr1 Package Useful

A chr1 package is useful only if it can connect genotype to molecular state. It
needs chr1 credible-set dosage, candidate-gene readout, ancestry covariates, and
cell-state labels. A structure file, an inhibitor assay, or a paper-level locus
summary is not enough to reopen GPR25 or KIF21B as a target.

## Files To Read Before Sending

| purpose | artifact |
|---|---|
| universal preflight | `docs/validation/INCOMING_PACKAGE_PREFLIGHT_CHECKLIST_V52.md` |
| manifest template | `docs/validation/INCOMING_PACKAGE_MANIFEST_TEMPLATE_V52.tsv` |
| metadata versus raw data git policy | `docs/validation/MANIFEST_METADATA_VS_RAW_DATA_GIT_POLICY_V52.md` |
| route classifier | `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv` |
| route examples | `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_EXAMPLES_V52.tsv` |
| monitoring minimum package | `docs/validation/MONITORING_MINIMUM_VIABLE_PACKAGE_CHECKLIST_V52.md` |
| chr1 target-resolution package | `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md` |
| complete handoff bundles | `docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md` |

## What Not To Send

Do not send:

1. raw restricted files before allowed-use terms are documented;
2. files larger than repository limits for direct git storage;
3. aggregate-only figures as if they were validation data;
4. response labels with no paired expression samples;
5. structure files as substitutes for genotype-linked or response data.

## Expected Project Response

The project will classify the package as one of:

1. scoreable monitoring validation;
2. chr1 target-resolution handoff;
3. chr1 modality workup;
4. secondary biology or monitoring route;
5. context only;
6. access-blocked;
7. reject or unscoreable.

The classification happens before analysis and does not change the frozen V22
rule or any closed target verdict.
