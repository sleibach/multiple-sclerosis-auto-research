# Returned-Package Dependency Graph V46

Status: infrastructure dependency map. No validation result and no biological
claim.

## Purpose

`scripts/v46_returned_package_dependency_graph.py` turns the returned-package
handoff manifest, regression suite, smoke-test bundle, and stale-output registry
into a graph of scripts, docs, outputs, suites, and freshness dependencies.

This is a navigation and drift-detection artifact. It does not open returned
score tables, expression matrices, labels, or quarantined cohorts.

## Command

```bash
.venv/bin/python scripts/v46_returned_package_dependency_graph.py \
  --outdir analysis/v46_returned_package_dependency_graph \
  --fail-on-error
```

## Current Result

- nodes: `601`
- edges: `817`
- lint checks: `221`
- lint failures: `0`
- lint hard failures: `0`
- lint warnings: `0`
- strict status modes: `stale_status_mode=fail`, `suite_status_mode=fail`
- all `score_values_read`: `false`
- overall status: `PASS`

Machine-readable outputs:

- `analysis/v46_returned_package_dependency_graph/returned_package_dependency_summary.json`
- `analysis/v46_returned_package_dependency_graph/returned_package_dependency_nodes.tsv`
- `analysis/v46_returned_package_dependency_graph/returned_package_dependency_edges.tsv`
- `analysis/v46_returned_package_dependency_graph/returned_package_dependency_lint.tsv`
- `analysis/v46_returned_package_dependency_graph/returned_package_dependency_graph.dot`
- `analysis/v46_returned_package_dependency_graph/RETURNED_PACKAGE_DEPENDENCY_GRAPH.md`

## Boundary

The graph supports operator navigation and dependency audit only. It is not a
validation result and does not authorize interpretation of any returned package.

When the graph is run inside the aggregate regression or smoke-test suites, the
suite invokes stale/suite status rows in warning mode to avoid a self-refresh
cycle while those suites are being regenerated. The standalone command above is
the strict audit and must pass with `0` hard failures.
