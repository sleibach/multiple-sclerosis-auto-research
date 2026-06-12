# V45 Regression Aggregator

Status: synthetic/software regression infrastructure. No biological claim.

## Purpose

`scripts/v45_regression_aggregator.py` runs the core V45 guardrail regression
checks from one command. It is meant for future smoke testing before and after
changes to validation infrastructure.

It does not run any real cohort and does not make any biological claim.

## Command

```bash
.venv/bin/python scripts/v45_regression_aggregator.py
```

Outputs:

- `analysis/v45_regression_aggregator/regression_steps.tsv`
- `analysis/v45_regression_aggregator/regression_aggregator_summary.json`

## Current Result

Overall status: `PASS`

| Step | Status | Runtime seconds |
|---|---:|---:|
| primary harness regression | PASS | 69.343 |
| secondary/context harness regression | PASS | 2.166 |
| intake preflight regression | PASS | 0.476 |
| checksum manifest synthetic check | PASS | 0.363 |
| response-column synthetic check | PASS | 0.462 |
| subject-map synthetic check | PASS | 0.409 |

Total runtime: `73.219` seconds.

## Coverage

The aggregator confirms:

1. V42 primary synthetic null fails and planted signal passes cleanly.
2. Secondary postpartum and T/B harness synthetic null/planted checks pass.
3. Pharmacodynamic-only context harness remains context-only.
4. Intake preflight passes valid synthetic packages and rejects
   pharmacodynamic response-like labels.
5. Checksum manifest verification catches modified files.
6. Response-column audit rejects response-like columns.
7. Subject-map sanity accepts a verified map and rejects missing baseline,
   missing follow-up, and GSE228330 inferred public-order metadata.

## Guardrail

This is a software/method regression suite. Passing it means the guardrails still
behave mechanically; it does not validate the APC/HLA-II monitoring biology.
