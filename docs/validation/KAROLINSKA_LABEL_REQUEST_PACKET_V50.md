# Karolinska / Parallel DMF Label Request Packet V50

Status: outbound request overlay. This document does not send a request, receive
data, run analysis, or alter the locked V22 rule or any frozen pre-registration.
It tightens the V45 Karolinska request using the V50 source-hit review gates.

## Why This Exists

The Gafson DMF PBMC RNA-seq cohort remains the best primary validation target,
but V43 showed that a small cohort may be inconclusive. The Karolinska DMF ROS
cohort remains the best parallel low-barrier MS DMF path already identified:

- SuperSeries: `GSE130494`
- Expression subseries: `GSE130478`
- Methylation subseries: `GSE130491`
- Publication: PMID `31300673`, DOI `10.1038/s41467-019-11139-3`
- Existing packet: `docs/validation/KAROLINSKA_DMF_LABEL_REQUEST_V45.md`
- Ready-to-send draft: `docs/validation/outbound_requests/karolinska_dmf_ready_to_send_V45.md`

V50 adds one rule: the cohort is not usable, even as secondary validation, until
the missing fields satisfy the source-hit gates in
`knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md`.

## Current Safe Classification

| route | current status | reason |
|---|---|---|
| Karolinska DMF public GEO | `partial_hit_metadata_only` | Public expression/methylation records exist, but response labels and GSM-to-subject/timepoint mapping are not public. |
| Karolinska as primary V22 validation | `not allowed` | CD4+ T-cell array at baseline/6 months is not the primary early PBMC RNA-seq Gafson-like design. |
| Karolinska as secondary DMF stress test | `blocked pending labels` | Possible only after labels, mapping, response definition, module coverage, and technical covariates are received and a Karolinska addendum is finalized blind. |

## Minimum Requested Fields

These fields are the minimum package that would allow a safe V50 intake
decision:

| field | required content | why required |
|---|---|---|
| `GSM` | GEO sample accession for every shared row. | Connects labels to public expression/methylation samples. |
| `subject_id` | Pseudonymous patient ID stable across timepoints and cell types. | Establishes pairing. |
| `timepoint` | Baseline, 3 months, 6 months, or exact day/month since DMF start. | Freezes timepoint interpretation. |
| `cell_type` | CD4+ T cell, CD14+ monocyte, or other sorted compartment. | Prevents PBMC-vs-compartment overclaiming. |
| `platform` | Expression array, methylation array, or other assay. | Freezes module-coverage expectations. |
| `beneficial_response_label` | Binary or categorical label used in the publication. | Required for any response analysis. |
| `response_definition` | Text definition and cutoffs for beneficial responder/nonresponder. | Prevents post-hoc endpoint interpretation. |
| `technical_batch_or_qc` | Array batch/date/file, processing date, RNA quality, or explicit absence. | Feeds V44/V45 batch guard and quality interpretation. |
| `monocyte_count_ros` | Patient/timepoint monocyte count and ROS summaries, if shareable. | Connects the public paper's mechanism to expression/methylation rows. |
| `data_use_terms` | Any restrictions on storage, publication, sharing, or aggregate output. | Determines whether local analysis or author-run fallback is allowed. |

Optional but valuable covariates: age, sex, disease duration, baseline disease
activity, prior DMT, steroid exposure near sampling, relapse/MRI/disability
components, and NOX3 genotype/variant information if shareable.

## V50 Intake Decision Grid

| received package shape | safe action |
|---|---|
| Labels plus GSM-to-subject/timepoint map plus response definition | Finalize `docs/validation/KAROLINSKA_PREREGISTRATION_TEMPLATE_V45.md` into a blind Karolinska addendum before any scoring. |
| Labels without complete sample map | `partial_hit_metadata_only`; request missing map, no scoring. |
| Sample map without response labels | pharmacodynamic/context only; no AUC or validation language. |
| Aggregate-only author response | Use the author-run fallback minimum-output specification; do not treat prose-only summaries as validation evidence. |
| Terms block local use | Park in access/terms review; offer author-run fallback if allowed. |
| No labels were collected | Context only; do not pursue as response validation. |

## Updated Email Overlay

Use the V45 ready-to-send draft as the base. Add this paragraph after the
minimum useful fields:

```text
To avoid post-hoc interpretation, we would classify the returned package before
any scoring. A package with response labels and GSM-to-subject/timepoint mapping
would allow a secondary, pre-specified Karolinska addendum. A package with
sample mapping but no response labels would be used only as pharmacodynamic
context. If individual-level data cannot leave your institution, we can provide
a frozen author-run aggregate-output option instead.
```

Add this sentence near the end:

```text
We would not treat the Karolinska cohort as a primary replacement for the early
PBMC RNA-seq validation cohort; it would be explicitly reported as a secondary
late-timepoint/platform stress test.
```

## Handling If Data Arrive

1. Place files under `data/raw_v3/karolinska_dmf_ros_2019/`.
2. Preserve original filenames and all provided terms.
3. Compute `SHA256SUMS` before opening contents for analysis.
4. Fill a received-package manifest and source terms note.
5. Run schema, subject-map, response-column, and route readiness validators.
6. Finalize a Karolinska-specific preregistration addendum before computing any
   module score or response metric.

No module-response scoring is allowed until those steps pass.

## Relationship To V50 Source-Search Results

The BioStudies pass found no exact public early-treatment validation cohort and
identified only near-candidates. That makes the Karolinska label request still
useful, but it does not change Karolinska's role: it is a secondary stress-test
path until labels and mapping arrive.

## Source Boundary

This packet is an operations artifact. It records what to request and how to
classify a returned package; it is not evidence about MS biology and does not
promote any cohort to validation-ready status. Relevant controls:
`docs/validation/KAROLINSKA_DMF_LABEL_REQUEST_V45.md`,
`docs/validation/KAROLINSKA_PREREGISTRATION_TEMPLATE_V45.md`,
`knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md`,
and `docs/knowledge/EPISTEMIC_CLASSES.md`.
