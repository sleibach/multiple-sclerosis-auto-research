# Received-Package Decision Tree V45

Status: generated operator decision tree. No biological claim.

## Purpose

`scripts/v45_received_package_decision_tree.py` combines the current-action card
and state-machine validator into a route-specific first-24h decision table. It
answers, for each route:

- what the current action is;
- whether scoring is allowed now;
- what to do if a package arrives;
- which route-arrival packet and status updater/gate to use;
- what hard stop prevents premature scoring.

The tree does not inspect received files, expression matrices, labels, or run a
validation harness.

## Command

Live:

```bash
.venv/bin/python scripts/v45_received_package_decision_tree.py \
  --outdir analysis/v45_received_package_decision_tree/live
```

Synthetic premature-harness-ready regression:

```bash
.venv/bin/python scripts/v45_received_package_decision_tree.py \
  --synthetic-case premature_harness_ready \
  --expect-status FAIL \
  --outdir analysis/v45_received_package_decision_tree/synthetic_premature_harness_ready
```

## Current Result

Live status: `PASS`.

- routes covered: `4`;
- routes allowed to score now: `0`;
- hard issues: `0`.

Synthetic premature-harness-ready regression: expected `FAIL`.

## Machine-Readable Outputs

Live:

- `analysis/v45_received_package_decision_tree/live/received_package_decision_tree.tsv`
- `analysis/v45_received_package_decision_tree/live/received_package_decision_tree_issues.tsv`
- `analysis/v45_received_package_decision_tree/live/received_package_decision_tree_summary.json`

Synthetic regression:

- `analysis/v45_received_package_decision_tree/synthetic_premature_harness_ready/received_package_decision_tree.tsv`
- `analysis/v45_received_package_decision_tree/synthetic_premature_harness_ready/received_package_decision_tree_issues.tsv`
- `analysis/v45_received_package_decision_tree/synthetic_premature_harness_ready/received_package_decision_tree_summary.json`

## Interpretation Boundary

A live `PASS` means the operator decision tree is internally consistent with the
current action card and state-machine validator. It does not mean any package
has arrived, any route is harness-ready, or any validation has occurred.
