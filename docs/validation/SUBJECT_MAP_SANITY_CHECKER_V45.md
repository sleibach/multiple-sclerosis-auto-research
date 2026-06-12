# V45 Subject-Map Sanity Checker

## Purpose

Longitudinal treatment-response validation requires a verified mapping from
samples to subjects and timepoints. Public sample order is not a subject map.
This V45 guard prevents public-order, inferred, or placeholder longitudinal
metadata from entering any paired-delta validation harness.

The checker is method infrastructure only. It makes no biological claim and
does not score the V22 rule.

## Script

`scripts/v45_subject_map_sanity_check.py`

Primary command:

```bash
.venv/bin/python scripts/v45_subject_map_sanity_check.py check \
  --metadata path/to/metadata.tsv \
  --outdir analysis/v45_subject_map_sanity_check/<cohort_name> \
  --min-paired-subjects 2 \
  --fail-on-error
```

Required metadata columns:

| Column | Requirement |
|---|---|
| `sample_id` | unique sample identifier |
| `subject` | verified patient/participant identifier |
| `timepoint` | baseline/on-treatment timepoint label |

Optional but strongly preferred:

| Column | Use |
|---|---|
| `days_since_treatment` | confirms baseline day 0 and positive follow-up days |
| `pairing_status` | must not indicate inferred/unverified mapping |

## Failure Rules

The audit fails if any of these hold:

1. Required columns are absent.
2. Duplicate `sample_id` values exist.
3. `subject` contains placeholder tokens such as `UNVERIFIED`, `INFERRED`,
   `PUBLIC_ORDER`, `PSEUDO`, or `PLACEHOLDER`.
4. `pairing_status` contains `unverified`, `inferred`, `public_order`, or
   `placeholder`.
5. A subject lacks exactly one baseline sample.
6. A subject lacks an on-treatment/nonbaseline sample.
7. A subject has duplicated timepoint labels.
8. Baseline day is not 0 or follow-up days are not positive when
   `days_since_treatment` is provided.
9. The number of usable paired subjects is below `--min-paired-subjects`.

Outputs:

| File | Contents |
|---|---|
| `subject_map_audit.tsv` | row-level failures/warnings |
| `subject_summary.tsv` | per-subject baseline/follow-up summary |
| `subject_map_summary.json` | machine-readable pass/fail summary |

## Synthetic Verification

Command run:

```bash
.venv/bin/python scripts/v45_subject_map_sanity_check.py synthetic-check \
  --outdir analysis/v45_subject_map_sanity_check
```

Result:

| Fixture | Expected | Observed |
|---|---:|---:|
| verified synthetic longitudinal map | pass | pass |
| current GSE228330 public-order draft map | fail | fail |

The synthetic fixture wrote:

`analysis/v45_subject_map_sanity_check/synthetic_check_assertions.json`

Key results:

| Metric | Value |
|---|---:|
| valid synthetic samples | 9 |
| valid synthetic paired subjects | 3 |
| valid synthetic failures | 0 |
| GSE228330 draft samples audited | 44 |
| GSE228330 draft usable paired subjects | 0 |
| GSE228330 draft failures | 133 |

## Cohort Implications

### GSE228330

The current draft metadata at
`analysis/v45_gse228330_pharmacodynamic_runbook/gse228330_draft_pharmacodynamic_metadata_unverified.tsv`
fails as intended because it uses `UNVERIFIED_PUBLIC_ORDER_*` subject
placeholders and `pairing_status=inferred_unverified`.

Therefore GSE228330 remains context-only until a verified GSM-to-subject and
timepoint map is obtained from the authors or a confirmable supplement. It must
not be used for paired-delta response validation.

### Karolinska DMF

Public summaries verify that longitudinal expression data exist, but the
validation blocker remains sample-level patient/timepoint mapping plus
beneficial-response labels. Any received Karolinska mapping must pass this
checker before the Karolinska preregistration addendum can be finalized and
before any paired-delta scoring is run.

## Validation Status

This is an additive blind guardrail. It does not alter `LOCKED_RULE_V22.md`, the
V42 preregistration, or any success/failure threshold. It only prevents invalid
longitudinal sample pairing from being treated as validated input.
