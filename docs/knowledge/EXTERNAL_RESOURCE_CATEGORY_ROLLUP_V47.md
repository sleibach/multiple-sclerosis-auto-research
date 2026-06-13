# External Resource Category Rollup V47

This is navigation infrastructure only. It groups external resource catalog
records under `knowledge_external/catalogs/resources/` into reader-facing
categories while preserving epistemic class, source, relationship tags, access
tier, and the explicit `NOT_PROJECT_GROUNDED` marker.

The rollup does not validate any external claim, does not make a biological
finding, and does not move external knowledge into grounded project evidence.

## Commands

```bash
.venv/bin/python scripts/v47_external_resource_category_rollup.py synthetic-check --outdir analysis/v47_external_resource_category_rollup --fail-on-error
.venv/bin/python scripts/v47_external_resource_category_rollup.py rollup --outdir knowledge_external/catalogs/indexes
```

## Outputs

- `knowledge_external/catalogs/indexes/external_resource_category_rollup.tsv`
- `knowledge_external/catalogs/indexes/external_resource_category_counts.tsv`
- `knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_CATEGORY_ROLLUP.md`
- `analysis/v47_external_resource_category_rollup/synthetic_category_rollup_summary.json`

The synthetic check verifies that category aggregation preserves the
`NOT_PROJECT_GROUNDED` marker and correctly routes simple synthetic PubMed and
GWAS Catalog examples to their intended categories.
