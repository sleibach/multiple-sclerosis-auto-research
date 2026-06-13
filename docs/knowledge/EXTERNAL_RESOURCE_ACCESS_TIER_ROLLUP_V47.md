# External Resource Access-Tier Rollup V47

This is navigation infrastructure only. It groups external resource catalog
records by `access_tier` while preserving epistemic class, source, relationship
tags, and the explicit `NOT_PROJECT_GROUNDED` marker.

Access tier is not evidence strength. A controlled resource can contain highly
useful data; an open resource can contain only contextual metadata. The rollup
exists so readers can distinguish immediately browseable public resources from
registration, application, mixed-access, or controlled resources.

## Commands

```bash
.venv/bin/python scripts/v47_external_resource_access_tier_rollup.py synthetic-check --outdir analysis/v47_external_resource_access_tier_rollup --fail-on-error
.venv/bin/python scripts/v47_external_resource_access_tier_rollup.py rollup --outdir knowledge_external/catalogs/indexes
```

## Outputs

- `knowledge_external/catalogs/indexes/external_resource_access_tier_rollup.tsv`
- `knowledge_external/catalogs/indexes/external_resource_access_tier_counts.tsv`
- `knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_ACCESS_TIER_ROLLUP.md`
- `analysis/v47_external_resource_access_tier_rollup/synthetic_access_tier_rollup_summary.json`
