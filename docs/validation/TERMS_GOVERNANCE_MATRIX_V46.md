# Terms Governance Matrix V46

Status: validation-readiness governance infrastructure. No validation result and
no biological claim.

## Purpose

`scripts/v46_terms_governance_matrix.py` classifies non-sensitive data-use terms
into a mechanical validation-handling route before any local processing occurs.
It covers the edge cases most likely to arrive from collaborators:

- local preflight allowed;
- aggregate-only local preflight allowed;
- author-run-only;
- no processing allowed;
- ambiguous or pending terms.

The classifier reads only the V45 data-use terms capture summary. It does not
read expression data, clinical labels, private agreements, or validation scores.

## Command

```bash
.venv/bin/python scripts/v46_terms_governance_matrix.py classify \
  --terms data/quarantine/<cohort>/governance/data_use_terms_summary.tsv \
  --outdir analysis/v46_terms_governance_matrix/<cohort>
```

Synthetic edge-case matrix:

```bash
.venv/bin/python scripts/v46_terms_governance_matrix.py synthetic-check \
  --outdir analysis/v46_terms_governance_matrix
```

## Verified Synthetic Result

The committed synthetic matrix passed five cases with zero expectation failures:

| Case | Class | Operator gate status |
|---|---|---|
| local preflight allowed | `LOCAL_PREFLIGHT_ALLOWED` | `pass` |
| aggregate-only local preflight | `AGGREGATE_ONLY_LOCAL_PREFLIGHT` | `pass` |
| author-run-only | `AUTHOR_RUN_ONLY` | `blocked` |
| no processing | `NO_PROCESSING_ALLOWED` | `blocked` |
| ambiguous terms | `AMBIGUOUS_TERMS_BLOCK` | `blocked` |

Machine-readable outputs:

- `analysis/v46_terms_governance_matrix/terms_governance_synthetic_summary.json`
- `analysis/v46_terms_governance_matrix/terms_governance_synthetic_cases.tsv`
- per-case `terms_governance_summary.json`
- per-case `terms_governance_decision.tsv`

## Route Meanings

| Class | Safe route | Hard stop |
|---|---|---|
| `LOCAL_PREFLIGHT_ALLOWED` | local preflight and frozen harness may proceed after all other gates pass | do not commit raw/private files unless terms explicitly allow it |
| `AGGREGATE_ONLY_LOCAL_PREFLIGHT` | local processing may proceed; only derived aggregate summaries may be committed/reported | do not commit individual-level expression, clinical labels, or restricted agreements |
| `AUTHOR_RUN_ONLY` | use the author-run frozen harness packet and receive aggregate outputs only | do not process transferred individual-level data locally |
| `NO_PROCESSING_ALLOWED` | request revised terms or an allowed aggregate author-run return | do not run preflight, module coverage, harness, or score interpretation |
| `AMBIGUOUS_TERMS_BLOCK` | clarify terms first | do not treat unclear terms as approval |

## Boundary

This matrix decides only whether package handling may proceed and which route is
allowed. It does not make a validation claim, does not change any locked rule or
pre-registration, and does not substitute for the no-raw-data scanner.

