# First 24 Hours Received-Data Operator Checklist V45

Status: operational checklist. No data received or analyzed.

Purpose: define what to do in the first day after any Gafson, Karolinska, or
GSE228330 package arrives, without creating analysis degrees of freedom.

Machine-readable status template:

`docs/validation/input_schemas/V45_first_24h_operator_status_template.tsv`

Status-board updater:

`docs/validation/RECEIVED_STATUS_UPDATER_V45.md`

## Before Touching Files

- Do not open expression matrices beside file-listing/checksum operations.
- Do not inspect expression by outcome, response group, or sample phenotype.
- Do not edit locked rules, preregistrations, thresholds, endpoint mappings, or
  module definitions.
- Keep raw/private data under `data/quarantine/<cohort>/` or a non-git
  restricted location allowed by terms.
- Run `scripts/v45_no_raw_git_scanner.py` before committing any receipt update.

## First 30 Minutes

| Step | Action | Output |
|---:|---|---|
| 1 | Create received-data folder under `data/quarantine/<cohort>/` or record a non-git restricted path | path recorded locally; no raw data committed |
| 2 | Record sender, receipt timestamp, file names, byte sizes, and whether terms permit local processing | non-sensitive receipt note |
| 3 | Capture terms using `docs/validation/input_schemas/V45_data_use_terms_capture_template.tsv` | `governance/data_use_terms_summary.tsv` |
| 4 | If terms are unclear, stop before preflight | named terms blocker |

## First 2 Hours

| Step | Action | Command/artifact |
|---:|---|---|
| 5 | Generate or verify SHA-256 manifest | `scripts/v45_checksum_manifest_validator.py` |
| 6 | Update received-data triage board | `docs/validation/RECEIVED_DATA_TRIAGE_STATUS_BOARD_V45.md` |
| 7 | Freeze outcome label dictionary before scoring any outcome-enabled package | `docs/validation/input_schemas/V45_outcome_label_dictionary_template.tsv` |
| 8 | Run intake preflight for the cohort mode | `scripts/v45_validation_intake_preflight.py` |
| 9 | Run module-coverage precheck for expression-matrix packages | `scripts/v45_module_coverage_precheck.py` |
| 10 | Run subject-map sanity for paired-delta packages | `scripts/v45_subject_map_sanity_check.py` |

## Same Day, Only If All Gates Pass

| Cohort role | Required committed plan before scoring |
|---|---|
| exact Gafson DMF/NEDA-4 primary package | `docs/validation/PREREGISTRATION_V42.md` and `docs/validation/GAFSON_ARRIVAL_RUNBOOK_V45.md` |
| Karolinska DMF labels/mapping | finalize a cohort-specific addendum from `docs/validation/KAROLINSKA_PREREGISTRATION_TEMPLATE_V45.md`, blind to scores |
| GSE228330 context-only | `docs/validation/PHARMACODYNAMIC_ONLY_PREREGISTRATION_V45.md`; no response claims |
| GSE228330 with author-provided labels | finalize addendum from `docs/validation/GSE228330_OUTCOME_LABEL_ADDENDUM_TEMPLATE_V45.md`, blind to scores |

Before running any harness:

```bash
.venv/bin/python scripts/v45_locked_artifact_hash_audit.py audit \
  --baseline docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv \
  --outdir analysis/v45_locked_artifact_hash_audit \
  --fail-on-drift

.venv/bin/python scripts/v45_regression_aggregator.py \
  --outdir analysis/v45_regression_aggregator
```

If either fails, stop. That is a software/integrity blocker, not a data result.

## Stop Rules

Stop before scoring if any of these occur:

- data-use terms are missing or do not permit local analysis;
- checksums fail or files changed after manifesting;
- outcome orientation is ambiguous;
- preflight fails;
- primary module coverage fails;
- subject-map sanity fails;
- batch/metadata fields required by the preregistration are absent and the
  applicable runbook says they are mandatory;
- locked-artifact hash audit detects drift;
- synthetic/software regression aggregator fails.

## What May Be Committed In The First 24 Hours

Allowed:

- non-sensitive receipt summaries;
- checksum manifests if permitted by terms;
- preflight summaries and guard outputs;
- updated triage/status boards;
- cohort-specific preregistration addendum if written blind before scoring;
- validation result summaries only after all frozen gates pass.

Forbidden:

- raw expression matrices or clinical labels unless terms explicitly allow;
- credentials, API tokens, private URLs, signed agreements, or private email
  content;
- any exploratory plot/table linking expression to outcome before the frozen
  harness runs.

## The One Sentence To Use Until Harness Ready

```text
Data have been received, but no validation has occurred until terms, checksum,
preflight, module coverage, subject-map, outcome-dictionary, locked-hash, and
regression gates pass.
```
