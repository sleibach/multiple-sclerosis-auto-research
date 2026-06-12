# Author Label Escalation Matrix V45

Status: acquisition operations template. No cohort data received or analyzed.

Purpose: define escalation paths when requested labels, subject maps, or
processed expression are delayed after request packets are sent.

Machine-readable matrix:

`docs/validation/input_schemas/V45_author_label_escalation_matrix.tsv`

## Escalation Principles

- Delay is acquisition status, not biological evidence.
- Do not alter locked rules, thresholds, or interpretation grids because a
  cohort is delayed.
- Ask for the minimum de-identified derived material needed for the frozen
  harness before asking for broader controlled data.
- If labels cannot be shared, ask whether an author-run frozen script is
  possible.

## Matrix

| Cohort | Trigger | Escalation | Ask | If blocked |
|---|---|---|---|---|
| Gafson DMF PBMC/NEDA-4 | no reply 7 days after sent packet | send concise reminder with exact required files | paired expression, sample metadata, NEDA-4 dictionary, batch/QC/steroid metadata | keep primary path delayed; continue Karolinska/GSE228330 readiness |
| Gafson DMF PBMC/NEDA-4 | no reply 14 days | contact alternate corresponding/coauthor if public and appropriate | same files or author-run frozen harness | record delayed; do not demote lead |
| Gafson DMF PBMC/NEDA-4 | data cannot leave institution | offer author-run command package | run frozen V42 harness and return non-sensitive outputs | require enough output fields to fill V45 report; no private raw data needed |
| Karolinska DMF ROS | labels not shareable | ask for de-identified derived responder/nonresponder table and GSM map only | beneficial-response label, subject/timepoint map, terms | keep as secondary path; no outcome scoring |
| Karolinska DMF ROS | GSM mapping unavailable | ask authors to run subject-map sanity locally or provide paired table | baseline/6-month pair table | no validation; public expression remains insufficient |
| GSE228330 ocrelizumab | response labels unavailable | ask for context-only subject/timepoint map and processed expression | verified subject map, processed expression/probe mapping | run only context path if preregistered gates pass |
| GSE228330 ocrelizumab | labels available but limited | ask for minimal binary label dictionary before any scoring | label values, orientation, assessment window | write blind addendum before scoring |

## Author-Run Option

If data cannot be shared, send:

- frozen harness command;
- input schema;
- locked rule and hash baseline;
- validation result report template;
- list of non-sensitive outputs needed.

Use the bundle index to assemble the non-sensitive send list:

`docs/validation/AUTHOR_RUN_PACKET_BUNDLE_INDEX_V45.md`

Use the ready-to-send fallback text when data transfer is blocked:

`docs/validation/outbound_requests/author_run_fallback_ready_to_send_V45.md`

Acceptable returned outputs:

- summary JSON/Tables from the frozen harness;
- aggregate attrition counts;
- AUC/g/CI/permutation outputs;
- confounder/batch diagnostic summaries.

Not acceptable as validation evidence:

- verbal statement that the result "looked good";
- plots without the frozen metrics;
- metrics from modified modules, endpoints, signs, or thresholds.

## Stop Rule

If all escalation paths fail, mark the cohort as externally blocked and keep the
project moving on internally executable readiness tasks. Do not convert
non-response into a negative result.
