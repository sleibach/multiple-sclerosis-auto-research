# V47 External Source-Domain Rollup

Status: governance/navigation artifact only.

`scripts/v47_external_source_domain_rollup.py` parses source locators from
records under `knowledge_external/`, groups them by source domain, and writes
class-preserving indexes under `knowledge_external/catalogs/indexes/`.

The rollup does not validate any external claim, does not interpret source
quality, and does not promote any external record to project-grounded evidence.
Every row preserves:

- `epistemic_class`
- `relationship_to_project_findings`
- source locator
- `NOT_PROJECT_GROUNDED`

Verification:

```bash
.venv/bin/python scripts/v47_external_source_domain_rollup.py synthetic-check --fail-on-error
.venv/bin/python scripts/v47_external_source_domain_rollup.py rollup
```

Expected outputs:

- `knowledge_external/catalogs/indexes/external_source_domain_rollup.tsv`
- `knowledge_external/catalogs/indexes/external_source_domain_counts.tsv`
- `knowledge_external/catalogs/indexes/EXTERNAL_SOURCE_DOMAIN_ROLLUP.md`
- `knowledge_external/catalogs/indexes/external_source_domain_rollup_summary.json`
