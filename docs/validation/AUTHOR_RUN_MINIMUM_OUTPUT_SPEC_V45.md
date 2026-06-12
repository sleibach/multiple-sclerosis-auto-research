# Author-Run Minimum Output Specification V45

Status: external-run output specification. No validation has been run by this
document.

Purpose: define the minimum non-sensitive aggregate outputs required from a
collaborator-run frozen harness when individual-level data cannot leave the
author institution.

Machine-readable specification:

`docs/validation/input_schemas/V45_author_run_minimum_output_spec.tsv`

Executable completeness checker:

`docs/validation/AUTHOR_RUN_OUTPUT_COMPLETENESS_CHECK_V45.md`

Redaction precheck to run before completeness:

`docs/validation/AUTHOR_RUN_REDACTION_PRECHECK_V45.md`

## Minimum Required Files

Returned outputs must be sufficient to:

- verify the frozen command and locked rule were used;
- classify the result under the V42 outcome grid;
- reproduce reported AUC/g/CI/confounder/batch interpretation from aggregate
  tables;
- identify unscoreable or underpowered conditions.

## Redaction Boundary

The minimum output package should exclude raw expression values, sample-level
clinical labels, private identifiers, and signed/private correspondence unless
terms explicitly permit transfer.

Run the redaction precheck before the completeness checker on every returned
aggregate package.

## Unacceptable Returns

Not sufficient:

- verbal summary only;
- plot screenshot only;
- "significant/not significant" statement without frozen metrics;
- output from changed module genes, endpoint, sign, threshold, or timepoint
  rule;
- metrics missing attrition and group-size counts.

## Report Link

The returned files should fill:

`docs/validation/VALIDATION_RESULT_REPORT_TEMPLATE_V45.md`
