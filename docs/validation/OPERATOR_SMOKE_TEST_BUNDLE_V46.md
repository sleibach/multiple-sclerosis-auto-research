# Operator Smoke-Test Bundle V46

Status: validation-readiness operator infrastructure. No validation result and
no biological claim.

## Purpose

`scripts/v46_operator_smoke_test_bundle.py` runs the compact local readiness
check set in dependency order. It is intended for a cold operator before acting
on a received package or aggregate author-run return.

The bundle uses only credential metadata, locked-artifact hashes, synthetic
fixtures, and repository safety scans. It does not read real cohort data, run a
validation harness, or interpret biology.

## Command

```bash
.venv/bin/python scripts/v46_operator_smoke_test_bundle.py \
  --outdir analysis/v46_operator_smoke_test_bundle \
  --fail-on-error
```

## Included Checks

1. OpenGWAS expiry sentinel.
2. Locked-artifact hash audit.
3. V45 author-run return gate synthetic check.
4. V45 author-run schema validator synthetic check.
5. V45 route analyzable-pair synthetic check.
6. V46 terms-governance matrix synthetic check.
7. V46 metric-format adapter synthetic check.
8. V46 partial-label classifier synthetic check.
9. V46 returned-package command-order planner synthetic check.
10. V46 returned-package route-state matrix.
11. V46 aggregate-only returned-package composition dry run.
12. V46 unscoreable-return composition dry run.
13. V46 safe-interpretation classifier synthetic check.
14. V46 safe-wording fixture linter.
15. V46 result-report safe-class linter.
16. V46 small-n conclusion language table.
17. V46 return repair-request templates.
18. V45 no-raw-data git scanner.

## Current Result

The committed run passed:

- steps: `18`;
- failures: `0`;
- overall status: `PASS`.

Machine-readable outputs:

- `analysis/v46_operator_smoke_test_bundle/operator_smoke_test_summary.json`
- `analysis/v46_operator_smoke_test_bundle/operator_smoke_test_steps.tsv`
- isolated per-check subdirectories under `analysis/v46_operator_smoke_test_bundle/`

## Boundary

A passing smoke-test means the local readiness machinery is mechanically
healthy. It does not mean data have arrived, terms permit processing, or any
validation has occurred.
