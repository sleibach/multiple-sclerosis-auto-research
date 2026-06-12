# Handoff Completeness Check V45

Status: executable packaging/readiness check. No biological claim.

Purpose: mechanically compare the V45 validation handoff bundle template against
the current repository state, so a future validation result or unscoreable-data
report cannot be handed off with missing gate evidence.

## Command

Current pre-receipt Gafson readiness check:

```bash
.venv/bin/python scripts/v45_handoff_completeness_check.py \
  --cohort gafson_pending \
  --package-state not_received \
  --outdir analysis/v45_handoff_completeness
```

Machine-readable outputs:

- `analysis/v45_handoff_completeness/handoff_completeness.tsv`
- `analysis/v45_handoff_completeness/handoff_completeness_summary.json`
- `analysis/v45_handoff_completeness/HANDOFF_COMPLETENESS_SUMMARY.md`

## Current Result

The current pre-receipt check status is `PASS`.

| Metric | Value |
|---|---:|
| template rows | `18` |
| required now | `2` |
| present required rows | `2` |
| hard failures | `0` |
| static references present | `6` |
| not yet applicable until received/scored data | `10` |

This means the static repository-side pieces needed before receipt are present.
It does not mean a received package is complete, harness-ready, or biologically
validated.

A deliberate scored-state negative control was also run before any real package
exists:

```bash
.venv/bin/python scripts/v45_handoff_completeness_check.py \
  --cohort gafson_pending \
  --package-state scored \
  --outdir analysis/v45_handoff_completeness_scored_missing
```

That check correctly reports `FAIL` with `9` hard missing cohort-specific output
rows. This is expected before a real frozen harness run and verifies that the
checker does not allow a scored handoff bundle to pass without validation
outputs.

## Package States

The checker supports four lifecycle states:

| State | Intended use |
|---|---|
| `not_received` | current pre-data state; only static commit/handoff references are required |
| `received` | package received but not scored; receipt, terms, checksum, intake, and report gates become required |
| `scored` | frozen harness ran; preregistration, software readiness, and harness outputs become required |
| `unscoreable` | package failed a required gate; failed gate evidence, taxonomy code, and redaction evidence become required |

Rows with cohort-specific placeholders such as `<cohort>` are not treated as
missing before the relevant lifecycle state. Once a package is received or
scored, those same rows become hard requirements.

## Interpretation Guard

This checker is a packaging gate only:

- it does not read raw validation data;
- it does not compute module scores or response metrics;
- it does not alter `LOCKED_RULE_V22.md` or any preregistration;
- it does not rescue a failed validation result.

A `PASS` means the handoff bundle is mechanically complete for the declared
lifecycle state. The scientific result still comes only from the frozen
preregistered harness and V42 outcome grid.
