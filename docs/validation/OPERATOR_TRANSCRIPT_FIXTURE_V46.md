# Operator Transcript Fixture V46

Status: synthetic operator-navigation infrastructure. No validation result and
no biological claim.

## Purpose

`scripts/v46_operator_transcript_fixture.py` builds end-to-end synthetic
transcripts showing how a returned package moves from receipt-manifest metadata
through the first-30-minute status board and into a report skeleton without
opening score-bearing values.

The fixture covers three safe operator routes:

1. scoreable canonical aggregate, still pre-result;
2. unscoreable aggregate requiring repair;
3. terms-blocked package where no package review is permitted.

## Command

```bash
.venv/bin/python scripts/v46_operator_transcript_fixture.py \
  --outdir analysis/v46_operator_transcript_fixture \
  --fail-on-error
```

## Current Result

The committed run passed:

- scenarios: `3`
- transcript steps: `12`
- lint checks: `69`
- lint failures: `0`
- all `score_values_read`: `false`

## Outputs

- `analysis/v46_operator_transcript_fixture/operator_transcript_fixture_summary.json`
- `analysis/v46_operator_transcript_fixture/operator_transcript_cases.tsv`
- `analysis/v46_operator_transcript_fixture/operator_transcript_steps.tsv`
- `analysis/v46_operator_transcript_fixture/operator_transcript_lint.tsv`
- `analysis/v46_operator_transcript_fixture/OPERATOR_TRANSCRIPT_FIXTURE.md`
- per-scenario skeletons under `analysis/v46_operator_transcript_fixture/report_skeletons/`
- per-scenario transcripts under `analysis/v46_operator_transcript_fixture/transcripts/`

## Boundary

The transcript fixture is an operator training and regression artifact only. It
does not run validation, does not inspect returned scores, does not read labels
or expression data, does not alter the immutable V22 locked rule, and does not
change the frozen V42 pre-registration.
