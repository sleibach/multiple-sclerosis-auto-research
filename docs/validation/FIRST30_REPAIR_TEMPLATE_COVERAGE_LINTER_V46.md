# First-30 Repair Template Coverage Linter V46

Status: operations infrastructure. No validation result and no biological claim.

Purpose: verify that every first-30-minute returned-package stop route either remains a local operator guard or maps to an existing safe repair-request template. This closes the handoff from triage stop to concrete author/request action.

## Current Run

Command:

```bash
.venv/bin/python scripts/v46_first30_repair_template_coverage_linter.py --outdir analysis/v46_first30_repair_template_coverage_linter --fail-on-error
```

Result:

- overall status: `PASS`
- first-30 rows checked: `46`
- coverage rows: `143`
- safe classes with templates: `9`
- template IDs: `10`
- local operator guard rows: `15`
- dynamic safe-class rows: `100`
- explicit template rows: `28`
- lint checks: `152`
- lint failures: `0`
- all `score_values_read`: `false`

## Boundary

The linter reads only the generated first-30-minute decision table and the generated repair-template index/lint. It does not inspect returned packages, returned score values, expression data, labels, or quarantined cohorts.

Local operator stops, such as software/readiness repair and no-raw scanner routing, do not require author-facing repair templates. Author-facing explicit or dynamic safe-class stops must resolve to an existing template whose forbidden-language lint passes.

## Outputs

- `analysis/v46_first30_repair_template_coverage_linter/first30_repair_template_coverage_summary.json`
- `analysis/v46_first30_repair_template_coverage_linter/first30_repair_template_coverage.tsv`
- `analysis/v46_first30_repair_template_coverage_linter/repair_template_safe_class_coverage.tsv`
- `analysis/v46_first30_repair_template_coverage_linter/first30_repair_template_coverage_lint.tsv`
- `analysis/v46_first30_repair_template_coverage_linter/FIRST30_REPAIR_TEMPLATE_COVERAGE.md`
