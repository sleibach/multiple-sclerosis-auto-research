# Outbound Data Request Tracker V45

Status: acquisition operations artifact. No data were received or analyzed by
this checkpoint.

## Purpose

V43 showed that a Gafson-sized cohort may be inconclusive, and V44/V45 reduced
single-cohort dependence by identifying parallel acquisition paths. This tracker
keeps the external blockers explicit so the project does not silently wait for a
single delayed dataset.

Machine-readable tracker:

- `analysis/v45_outbound_data_requests/request_tracker.tsv`

## Current Requests

| Priority | Cohort | Role | Current status | External blocker | Prepared request |
|---:|---|---|---|---|---|
| 1 | Gafson et al. 2018 DMF PBMC RNA-seq, PMID `30283812` | Best primary V22/V42 validation target | ready to request | processed/raw expression plus sample-level NEDA-4 labels and covariates not local | `docs/validation/GAFSON_DATA_REQUEST_V36.md` |
| 2 | Karolinska DMF ROS, `GSE130478/GSE130491/GSE130494`, PMID `31300673` | Best parallel secondary MS DMF label path | ready to request | beneficial-response labels plus GSM-to-patient/timepoint map absent from public GEO | `docs/validation/KAROLINSKA_DMF_LABEL_REQUEST_V45.md` |
| 3 | `GSE228330` ocrelizumab PBMC, PMID `37168665` | Open pharmacodynamic context; possible label request | optional request | public data lack responder/NEDA/relapse/EDSS-change labels | this document |
| 4 | any cohort owner unable to transfer individual-level data | Author-run frozen harness fallback | ready after transfer blocker | cohort owner must run frozen harness locally and return aggregate outputs | `docs/validation/outbound_requests/author_run_fallback_ready_to_send_V45.md` |

## Gafson Request

Prepared package:

- `docs/validation/GAFSON_DATA_REQUEST_V36.md`

Minimum requested files:

- gene expression matrix for all baseline, 6-week, and 15-month PBMC samples;
- sample-to-patient mapping;
- NEDA-4 responder/nonresponder status per patient;
- sample timepoint labels;
- gene identifiers used in the expression matrix;
- batch/QC, steroid, cell-composition, and clinical covariates where available.

Placement if received:

`data/raw_v3/gafson_dmf_2018/`

Pre-analysis gates:

1. checksum and manifest all received files;
2. confirm sample-mapped baseline and 6-week pairs;
3. confirm NEDA-4 outcome definition and window;
4. confirm the cohort was not used to construct V22/V42;
5. run the frozen V42 harness mechanically, with no rule edits.

## Karolinska Request

Prepared package:

- `docs/validation/KAROLINSKA_DMF_LABEL_REQUEST_V45.md`

Contact from public GEO metadata:

- Ewoud Ewing, `ewoud.ewing@ki.se`

Minimum requested files:

- patient-level beneficial-response labels for the 14 expression-paired
  `GSE130478` subjects;
- GSM-to-patient/timepoint/cell-type/platform map;
- exact clinical outcome definition and cutoff;
- array batch/date/file, processing date, RNA quality, or other QC;
- monocyte count / ROS mapping if shareable.

Placement if received:

`data/raw_v3/karolinska_dmf_ros_2019/`

Pre-analysis gates:

1. checksum and manifest all received files;
2. write a Karolinska-specific preregistration addendum before module scoring,
   because the expression platform, cell type, and timing differ from Gafson;
3. verify module coverage on `GPL17692`;
4. decide in advance whether the result is secondary late-timepoint validation
   or pharmacodynamic/context only.

## GSE228330 Optional Label Request

Current role from V45:

- open anti-CD20 pharmacodynamic context only;
- not response-validation ready from public data.

Suggested subject:

`Request for outcome-label mapping for GSE228330 ocrelizumab MS PBMC cohort`

Suggested body:

```text
Dear authors,

I am working on a pre-specified validation-readiness project for longitudinal
immune transcriptomic monitoring in multiple sclerosis. We reviewed the public
GEO record for GSE228330 and the linked ocrelizumab PBMC transcriptome paper
(PMID 37168665). The public data appear to include PBMC expression before
ocrelizumab, at 2 weeks, and at 6 months, but we could not find sample-mapped
clinical outcome labels such as responder/nonresponder status, NEDA, relapse,
EDSS change, or another treatment outcome endpoint.

Would you be willing to share, if available, a de-identified sample-level
mapping table with:

- GSM/sample ID;
- subject ID;
- timepoint;
- treatment group;
- clinical outcome label and definition, if any;
- relapse, EDSS, MRI, or NEDA component outcomes, if available;
- technical batch/QC and steroid exposure metadata, if shareable?

If no outcome labels were collected, we would use GSE228330 only as
pharmacodynamic context and would not make response-validation claims.

Kind regards,

[Name / affiliation]
```

Placement if received:

`data/raw_v3/gse228330_ocrelizumab_outcomes/`

Pre-analysis gate:

- If outcome labels are shared, write a cohort-specific preregistration addendum
  before any response-label scoring. If no outcome labels are shared, use only
  `scripts/v45_pharmacodynamic_only_harness.py`.

## Tracker Procedure

For every outbound request:

1. Save the exact sent email text as
   `docs/validation/outbound_requests/<cohort>_sent_YYYY-MM-DD.md`.
2. Record send date, recipient, and follow-up date in
   `analysis/v45_outbound_data_requests/request_tracker.tsv`.
3. On receipt, place files only in the specified raw/quarantine directory.
4. Checksum before opening.
5. Write any cohort-specific preregistration addendum before scoring outcomes.

## Author-Run Fallback

If a cohort owner cannot transfer individual-level data, offer:

`docs/validation/outbound_requests/author_run_fallback_ready_to_send_V45.md`

The returned package is acceptable only if it includes the aggregate outputs
specified by `docs/validation/AUTHOR_RUN_MINIMUM_OUTPUT_SPEC_V45.md` and passes
handoff-completeness/redaction checks. A prose-only result is not validation
evidence.
