# Preflight Failure Taxonomy V45

Status: validation-operations guardrail. No biological claim.

Purpose: map common V45 intake, integrity, and harness-readiness failures to
allowed repair actions before any real validation data are scored.

Machine-readable table:

`docs/validation/input_schemas/V45_preflight_failure_taxonomy.tsv`

## Core Rule

A failed guard is not a negative biological result. It is either:

- a repairable intake/package issue;
- a preregistration/addendum blocker;
- an integrity/software blocker;
- or a hard stop that requires a new package or external clarification.

No repair may use expression-outcome performance, alter the locked rule, lower a
threshold, flip outcome orientation after scoring, or drop samples because they
move the V22 score.

## Failure Classes

| Failure code | Trigger | Allowed repair | Disallowed repair |
|---|---|---|---|
| `TERMS_NOT_APPROVED` | data-use capture is missing or not approved for preflight | request clarification or approval; keep files quarantined | running preflight or scoring before approval |
| `CHECKSUM_MANIFEST_MISSING` | no manifest for received package | generate manifest from unchanged received files and log source | silently modifying files before manifesting |
| `CHECKSUM_DRIFT` | observed file hash differs from manifest | re-download/request replacement; document new manifest | accepting drift without source explanation |
| `RAW_DATA_GIT_HARD_FAIL` | no-raw scanner finds restricted/private data staged for git | unstage/remove from git; keep in quarantine | committing raw/private data |
| `OUTCOME_DICTIONARY_MISSING` | outcome labels exist but no frozen mapping/orientation | ask provider; freeze dictionary before scoring | infer orientation from score performance |
| `OUTCOME_DICTIONARY_AMBIGUOUS` | label values or assessment window unclear | request clarification; mark validation blocked | reconstruct endpoint post hoc |
| `METADATA_REQUIRED_COLUMN_MISSING` | intake preflight schema lacks required fields | repair from source metadata or request corrected table | drop affected subjects based on outcome/score |
| `EXPRESSION_SAMPLE_MISMATCH` | expression columns and metadata sample IDs disagree | repair sample IDs from source documentation | reorder or infer IDs from outcome patterns |
| `PRIMARY_MODULE_COVERAGE_FAIL` | V22 primary modules fail coverage precheck | repair gene mapping under V42 rules or request processed matrix | change module genes or lower coverage threshold |
| `CONFOUNDER_PANEL_UNSCOREABLE` | one or more confounder panels lack coverage | report unavailable panel; continue only if primary modules scoreable | substitute new post-hoc confounder panel |
| `SUBJECT_MAP_NO_BASELINE` | paired map lacks baseline for a subject | request/repair subject map | infer baseline from sample order |
| `SUBJECT_MAP_NO_EARLY_FOLLOWUP` | paired map lacks eligible early treatment timepoint | request/repair timepoint metadata | widen the V42 early window post hoc |
| `SUBJECT_MAP_DUPLICATE_OR_TIE` | duplicate samples/tied timepoint ambiguity | apply pre-registered lexicographic tie rule or request clarification | choose sample based on score/outcome |
| `PHARMACODYNAMIC_RESPONSE_COLUMN_PRESENT` | context-only package contains response-like columns | stop; require response-validation preregistration/addendum before labels are used | run context analysis while silently ignoring labels and later interpreting response |
| `LOCKED_HASH_DRIFT` | locked-artifact hash audit detects drift | identify intentional edit; revert or explicitly re-baseline before data scoring if allowed | refresh baseline to hide accidental drift |
| `REGRESSION_AGGREGATOR_FAIL` | synthetic/software regression check fails | fix software and rerun synthetic regression | run real validation anyway |
| `ARRAY_TOOLCHAIN_MISSING` | required local array/Bioconductor packages absent | use author processed matrix or install documented packages before processing | ad hoc probe summarization |
| `BATCH_DIAGNOSTIC_WARNING` | response-correlated batch/QC metadata detected | report through V42/V44 interpretation grid | batch-correct primary locked score post hoc |
| `UNDERPOWERED_GROUP_SIZE` | labeled group sizes below V42 clean-pass threshold | report inconclusive/effect estimate per grid | claim pass/kill from favorable point estimate |

## Operator Routing

1. Identify the first failing gate in the command-runner or runbook order.
2. Map it to this taxonomy.
3. Apply only the allowed repair.
4. Rerun the same failed guard.
5. Continue only when the guard passes.

If a failure is not listed here, stop and write a cohort-specific blinded
addendum before scoring. Do not invent a repair while looking at outcome-linked
module scores.
