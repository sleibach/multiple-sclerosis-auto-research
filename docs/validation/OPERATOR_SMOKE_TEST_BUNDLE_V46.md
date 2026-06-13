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
9. V46 receipt-manifest schema linter synthetic check.
10. V46 package-manifest shape classifier synthetic check.
11. V46 receipt-manifest-to-command-plan handoff.
12. V46 returned-package command-order planner synthetic check.
13. V46 returned-package route-state matrix.
14. V46 aggregate-only returned-package composition dry run.
15. V46 unscoreable-return composition dry run.
16. V46 safe-interpretation classifier synthetic check.
17. V46 safe-wording fixture linter.
18. V46 result-report safe-class linter.
19. V46 report-header metadata linter.
20. V46 report-header repair-template coverage.
21. V46 safe-class report-template readiness map.
22. V46 small-n conclusion language table.
23. V46 analyzable-pair confidence envelope.
24. V46 safe-interpretation examples.
25. V46 return repair-request templates.
26. V46 partial-label repair prioritization.
27. V46 first-30-minute returned-package decision table.
28. V46 first-30 repair-template coverage linter.
29. V46 first-30 returned-package status-board dry run.
30. V46 returned-package status-board schema linter.
31. V46 status-board Markdown round-trip renderer.
32. V46 returned-package preflight dry run.
33. V46 returned-package state-transition validator.
34. V46 operator transcript fixture.
35. V46 returned-package handoff bundle manifest.
36. V46 returned-package generated quickstart README.
37. V46 returned-package documentation cross-link linter.
38. V46 returned-package dependency graph.
39. V45 no-raw-data git scanner.

## Current Result

The committed run passed:

- steps: `39`;
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
