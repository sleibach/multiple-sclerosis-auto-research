# Cohort Follow-Up Calendar Template V45

Status: acquisition operations template. No cohort data received or analyzed.

Purpose: provide a relative follow-up schedule for Gafson, Karolinska, and
GSE228330 requests so delayed author labels or data packages do not create idle
time or ad hoc decisions.

Machine-readable template:

`docs/validation/input_schemas/V45_cohort_followup_calendar_template.tsv`

## How To Use

When a request is sent:

1. copy the relevant rows from the TSV into the live request tracker;
2. fill `sent_date_utc`, `owner`, and `actual_status`;
3. calculate due dates from `relative_due`;
4. save the exact sent text under `docs/validation/outbound_requests/`;
5. continue internally executable readiness work while waiting.

No row authorizes analysis. A package becomes harness-ready only through the
received-data triage and validation gates.

## Relative Follow-Up Schedule

| Cohort | Relative due | Action | If no response |
|---|---|---|---|
| Gafson DMF PBMC/NEDA-4 | day 0 | send primary data request packet | keep V42/Gafson harness ready; continue parallel cohort paths |
| Gafson DMF PBMC/NEDA-4 | day 3 business | polite receipt confirmation | no analysis change |
| Gafson DMF PBMC/NEDA-4 | day 7 calendar | first follow-up with exact required files | continue Karolinska/GSE228330 paths |
| Gafson DMF PBMC/NEDA-4 | day 14 calendar | escalation to alternative contact/coauthor if available | treat Gafson as delayed, not failed |
| Gafson DMF PBMC/NEDA-4 | day 28 calendar | no-data checkpoint | update status board; do not reinterpret lead |
| Karolinska DMF ROS | day 0 | send beneficial-response label and GSM mapping request | keep addendum template unfinalized |
| Karolinska DMF ROS | day 7 calendar | follow up on labels and patient/timepoint map | do not score public expression without labels/map |
| Karolinska DMF ROS | day 21 calendar | ask whether de-identified derived labels can be shared if raw data cannot | keep as secondary parallel path |
| GSE228330 ocrelizumab | day 0 | send optional outcome-label and subject-map request | context-only path remains separate |
| GSE228330 ocrelizumab | day 7 calendar | ask for processed expression or probe mapping plus verified subject map | do not infer pairing from public order |
| GSE228330 ocrelizumab | day 21 calendar | ask whether only pharmacodynamic metadata can be clarified | keep no-response-claim guard |

## No-Data Deadline Actions

If a request is unanswered by its no-data checkpoint:

- record the status as delayed, not negative;
- update `docs/validation/RECEIVED_DATA_TRIAGE_STATUS_BOARD_V45.md`;
- continue internally executable work from `meta/V45_QUEUE.md`;
- do not alter the locked rule, thresholds, or interpretation grid;
- do not downgrade the biological lead because an author did not respond.

## Evidence Gates Before Any Analysis

| Cohort | Minimum gates before scoring |
|---|---|
| Gafson | data-use approval, checksums, NEDA-4 dictionary, intake preflight, module coverage, subject-map sanity, locked-hash audit, regression pass |
| Karolinska | labels + GSM-to-subject/timepoint map, finalized blind addendum, terms/checksums/preflight, module coverage if expression used |
| GSE228330 context-only | processed expression/probe mapping, verified subject map, response-column audit pass, pharmacodynamic-only preregistration |
| GSE228330 with labels | all context gates plus outcome dictionary and finalized blind addendum before scoring |

## Guardrail

Calendar deadlines are acquisition management, not evidence. Missing data,
delayed replies, or refusal to share data cannot be counted as a biological
negative or a validation failure.
