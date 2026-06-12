# Blinded Deviation Log Template V45

Status: validation-operations template. No data received or analyzed.

Purpose: record mismatches between a received package and the frozen
preregistration before any module scoring or outcome-linked inspection.

Machine-readable template:

`docs/validation/input_schemas/V45_blinded_deviation_log_template.tsv`

## When To Use

Use this log when a package differs from the expected preregistered structure,
for example:

- timepoint labels differ from the expected baseline/early window;
- outcome name or coding differs from the expected NEDA-4 dictionary;
- platform requires a different feature annotation path;
- batch/QC/steroid metadata are absent;
- subject identifiers or paired maps need repair.

The log must be filled while blind to V22 scores and response performance.

## Allowed Deviation Resolutions

| Resolution | Meaning |
|---|---|
| `acceptable_by_existing_preregistration` | existing frozen plan already specifies the handling |
| `repair_requested` | external metadata/file clarification is needed |
| `blind_addendum_required` | a new cohort-specific addendum must be written before scoring |
| `blocked_unscoreable` | primary validation cannot proceed with current package |
| `context_only` | response validation is not allowed, but context-only preregistered use may be possible |

## Forbidden Resolutions

Do not record any resolution based on:

- whether the V22 score looks favorable;
- responder/nonresponder separation;
- post-hoc endpoint substitution;
- dropping samples that weaken the result;
- changing module genes, signs, or thresholds.

## Review Rule

Every deviation row must name:

- the affected preregistration section;
- the observed mismatch;
- the allowed resolution;
- whether a blind addendum is required;
- the evidence path supporting the decision.

If the resolution is unclear, stop and treat the package as blocked until the
human/project lead resolves it before scoring.
