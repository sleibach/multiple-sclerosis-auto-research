# V47 Source URL Reachability Checker

Status: source-maintenance artifact only.

`scripts/v47_source_url_reachability_checker.py` checks whether the source URLs
attached to external records are reachable at the HTTP transport layer.

This checker does not validate external claims, does not interpret source
quality, and does not promote any external record to project-grounded evidence.
HTTP 2xx means only that a URL responded. HTTP errors, redirects, or network
errors are maintenance statuses only.

Verification:

```bash
.venv/bin/python scripts/v47_source_url_reachability_checker.py synthetic-check --fail-on-error
.venv/bin/python scripts/v47_source_url_reachability_checker.py check --timeout 8
```

Expected outputs:

- `knowledge_external/catalogs/indexes/external_source_url_reachability.tsv`
- `knowledge_external/catalogs/indexes/external_source_url_reachability_counts.tsv`
- `knowledge_external/catalogs/indexes/EXTERNAL_SOURCE_URL_REACHABILITY.md`
- `knowledge_external/catalogs/indexes/external_source_url_reachability_summary.json`

