# V45 Outcome-Label Dictionary Template

Status: validation-readiness template. No labels received or analyzed.

## Purpose

If authors provide Gafson, Karolinska, GSE228330, or other response labels, the
project must freeze their meaning before module scoring. This template captures
the response/outcome definition, class orientation, assessment window, component
outcomes, censoring, and missingness rules before any cohort-specific addendum is
finalized.

Machine-readable blank template:

`docs/validation/input_schemas/V45_outcome_label_dictionary_template.tsv`

Recommended per-cohort filled output after receipt:

`data/quarantine/<cohort>/metadata/outcome_label_dictionary.tsv`

## Required Before Scoring

A cohort-specific preregistration/addendum may not score response labels until
the filled dictionary answers:

1. What is the exact binary outcome?
2. Which value is the positive class for the frozen harness?
3. Which value is the negative class?
4. What is the assessment window?
5. Which component outcomes define a composite such as NEDA-4?
6. How are censoring, dropout, indeterminate labels, and missing components
   handled?
7. Which subject ID links the outcome table to transcriptomic samples?
8. Who defined/provided the label and when?

## Orientation Rule

For V22/V42 primary validation, the dictionary must map the clinical labels to
the harness response convention before analysis:

- positive class: responder / NEDA achieved / event-free / treatment success;
- negative class: nonresponder / disease activity / relapse/MRI/disability
  activity / treatment failure.

If the author label has the opposite orientation, record the raw values and the
pre-specified recoding in the dictionary before running any module score.

## Missingness Rule

Labels with ambiguous outcome state must be explicitly assigned one of:

- `exclude_before_analysis`
- `censored_effect_size_only`
- `component_missing_composite_unscoreable`
- `other_preregistered_rule`

No post-hoc imputation of response labels is allowed.

## Guardrail

This template is additive. It does not change the locked rule, the V42
success/failure thresholds, or the interpretation grid. It prevents ambiguous
labels from being interpreted after seeing module scores.
