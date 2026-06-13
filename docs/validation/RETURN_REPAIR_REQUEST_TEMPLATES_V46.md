# Return Repair Request Templates V46

Status: operations infrastructure. No validation result and no biological claim.

## Purpose

`scripts/v46_return_repair_request_templates.py` generates safe request
templates for returned packages that are blocked before interpretation. The
templates turn the first failing returned-package gate into an author-facing
repair ask while preserving the V42/V45/V46 no-score-before-gates boundary.

The generator does not read real cohort data, private labels, expression values,
returned scores, AUCs, p-values, or effect sizes.

## Command

```bash
.venv/bin/python scripts/v46_return_repair_request_templates.py \
  --outdir analysis/v46_return_repair_request_templates \
  --fail-on-error
```

## Inputs

- `docs/validation/input_schemas/V45_preflight_failure_taxonomy.tsv`
- `docs/validation/input_schemas/V45_author_run_minimum_output_spec.tsv`
- `docs/validation/AUTHOR_RUN_RETURN_OPERATOR_CHECKLIST_V45.md`
- `docs/validation/RETURNED_PACKAGE_SAFE_INTERPRETATION_V46.md`
- `analysis/v46_small_n_conclusion_language/small_n_conclusion_language.tsv`

## Current Result

Current status: `PASS`.

The generated suite contains `10` repair templates covering:

- terms or receipt not cleared;
- redaction/private-content block;
- missing score-bearing aggregate outputs;
- schema or metric-format mismatch;
- absent or unmapped response labels;
- ambiguous response-label orientation;
- below-planning-floor labeled pairs;
- metadata or pairing contradiction;
- primary module coverage block;
- batch or confounder metadata needed.

The built-in linter currently checks `100` forbidden-language patterns across the
templates and reports `0` failures.

Machine-readable outputs:

- `analysis/v46_return_repair_request_templates/return_repair_request_templates_summary.json`
- `analysis/v46_return_repair_request_templates/repair_request_template_index.tsv`
- `analysis/v46_return_repair_request_templates/repair_request_template_lint.tsv`
- `analysis/v46_return_repair_request_templates/RETURN_REPAIR_REQUEST_TEMPLATES.md`
- per-template markdown files under `analysis/v46_return_repair_request_templates/templates/`

## Boundary

These are repair requests, not validation reports. A template may request
missing aggregate outputs or metadata clarification, but it must not infer,
summarize, or discuss returned scores. After a repaired package arrives, the same
frozen returned-package gates must be rerun before any result wording is drafted.
