# Cross-Route Readiness Linter V45

Status: operational readiness guard. No biological claim.

## Purpose

`scripts/v45_cross_route_readiness_linter.py` checks that every live validation
or acquisition route has the minimum handoff components needed before any future
data package can move toward a frozen harness:

- outbound request artifact;
- explicit blocker state;
- route-specific arrival packet;
- no-scoring hard-stop language in the arrival packet;
- generated command plan, or the author-run return gate equivalent for the
  author-run fallback route.

The linter does not open quarantined data, score modules, inspect outcomes, or
run a validation harness.

## Command

```bash
.venv/bin/python scripts/v45_cross_route_readiness_linter.py
```

Synthetic regression:

```bash
.venv/bin/python scripts/v45_cross_route_readiness_linter.py \
  --synthetic-case missing_request \
  --expect-status FAIL \
  --outdir analysis/v45_cross_route_readiness_linter/synthetic_missing_request
```

## Current Result

Live status: `PASS`.

The live linter covers `4` routes and reports `0` hard issues and `0` soft
issues. The Karolinska route now has a plan-only command runner output:

- `analysis/v45_validation_command_runner/karolinska_primary_plan/command_plan_summary.json`

The author-run fallback is intentionally handled through the author-run return
gate runner rather than the quarantine package command runner.

Synthetic missing-request regression status: expected `FAIL`.

## Machine-Readable Outputs

Live:

- `analysis/v45_cross_route_readiness_linter/live/cross_route_readiness_lint.tsv`
- `analysis/v45_cross_route_readiness_linter/live/cross_route_readiness_issues.tsv`
- `analysis/v45_cross_route_readiness_linter/live/cross_route_readiness_lint_summary.json`

Synthetic regression:

- `analysis/v45_cross_route_readiness_linter/synthetic_missing_request/cross_route_readiness_lint.tsv`
- `analysis/v45_cross_route_readiness_linter/synthetic_missing_request/cross_route_readiness_issues.tsv`
- `analysis/v45_cross_route_readiness_linter/synthetic_missing_request/cross_route_readiness_lint_summary.json`

## Interpretation Boundary

A `PASS` means cross-route operational handoff artifacts are present and
internally linked. It does not mean:

- any real validation package has arrived;
- any cohort is harness-ready;
- any biological result has been produced;
- the V22 rule, V42 preregistration, or any secondary preregistration changed.
