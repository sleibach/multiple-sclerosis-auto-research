# Pre-Commit Readiness Checklist V45

Status: executable integrity checklist. No biological claim.

Purpose: run the required V45 safety checks before committing validation
readiness work or before touching any received validation package.

## Command

```bash
.venv/bin/python scripts/v45_precommit_readiness_check.py
```

The wrapper runs, in order:

1. no-raw-data-in-git scanner;
2. locked-artifact hash audit;
3. V45 synthetic/software regression aggregator;
4. V45 governance refresh.

## Current Result

Current wrapper status: `PASS`.

| Step | Status | Elapsed seconds |
|---|---|---:|
| no raw git scanner | `PASS` | `0.451` |
| locked artifact hash audit | `PASS` | `0.073` |
| regression aggregator | `PASS` | `72.626` |
| governance refresh | `PASS` | `12.880` |
| total | `PASS` | `86.030` |

Machine-readable outputs:

- `analysis/v45_precommit_readiness/precommit_readiness_steps.tsv`
- `analysis/v45_precommit_readiness/precommit_readiness_summary.json`

## What A Pass Means

A pass means:

- no hard raw/quarantine/restricted-data path is staged or tracked;
- locked/frozen artifacts match the committed hash baseline;
- synthetic/software regression checks pass;
- governance summaries were refreshed.

It does not mean any biological validation occurred, and it does not authorize
rule edits or real-data inspection outside the preregistered harness.

## What A Failure Means

| Failed step | Correct response |
|---|---|
| no raw git scanner | remove restricted/raw/quarantine data from git; keep only permitted summaries |
| locked artifact hash audit | investigate drift before validation; do not refresh baseline to hide accidental edits |
| regression aggregator | fix software or synthetic fixtures before real harness execution |
| governance refresh | repair index/storage generator before release or handoff |

## When To Run

Run this checklist:

- before committing a validation-readiness checkpoint;
- before running any received-cohort frozen harness;
- before external handoff;
- after any change to harness scripts, preregistration guardrails, or generated
  governance outputs.
