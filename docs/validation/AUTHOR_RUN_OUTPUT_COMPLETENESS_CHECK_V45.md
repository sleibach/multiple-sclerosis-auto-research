# Author-Run Output Completeness Check V45

Status: aggregate-package completeness check. No biological claim.

Purpose: verify that a collaborator-run frozen-harness return package contains
the minimum non-sensitive aggregate outputs required by
`docs/validation/AUTHOR_RUN_MINIMUM_OUTPUT_SPEC_V45.md`.

## Commands

Check a returned scored aggregate package:

```bash
.venv/bin/python scripts/v45_author_run_output_check.py check \
  --root analysis/validation_runs/<cohort_author_run_return> \
  --package-state scored \
  --outdir analysis/v45_author_run_output_check/<cohort> \
  --fail-on-error
```

Check an unscoreable aggregate package:

```bash
.venv/bin/python scripts/v45_author_run_output_check.py check \
  --root analysis/validation_runs/<cohort_author_run_return> \
  --package-state unscoreable \
  --outdir analysis/v45_author_run_output_check/<cohort> \
  --fail-on-error
```

Synthetic completeness fixture:

```bash
.venv/bin/python scripts/v45_author_run_output_check.py synthetic-check \
  --outdir analysis/v45_author_run_output_check
```

## Current Synthetic Verification

The synthetic complete package is assembled from the existing V42 primary
synthetic planted outputs plus synthetic run metadata and a report stub.

| Check | Result |
|---|---:|
| complete synthetic package | `PASS` |
| required rows in scored state | `9` |
| hard failures in complete package | `0` |
| deliberate incomplete synthetic package | `FAIL` |
| hard failures in incomplete package | `3` |

The incomplete negative control uses the older V42 planted-result directory
without the full author-run metadata/report/batch bundle and correctly fails.

## What Is Checked

The checker reads only aggregate files named in
`docs/validation/input_schemas/V45_author_run_minimum_output_spec.tsv`.

It checks:

- required file presence for scored or unscoreable states;
- non-empty JSON/TSV/text files;
- parseable JSON/TSV files;
- key metric columns for the locked-rule, confounder, joint-confounder,
  gene-coverage, and batch-diagnostic tables;
- command/software text in `RUN_METADATA.txt`.

It does not check or infer:

- raw expression matrices;
- private clinical labels;
- individual-level sample identities;
- biological validity;
- whether the result passes the V42 grid.

## Interpretation

A `PASS` means the aggregate return package is structurally complete enough to
enter the V45 handoff and result-reporting path. It is not a validation result.

A `FAIL` means the returned package is incomplete. The correct response is to
request the missing aggregate files or classify the package using the preflight
failure taxonomy. Do not fill missing metrics from prose or plots.
