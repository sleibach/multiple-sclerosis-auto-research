# V50 Machine-Readable Negative Source-Search Index

Status: machine-readable source-search navigation artifact. This file points to
the generated TSV/JSON index used to prevent repeated V50 non-OpenGWAS metadata
hits from being recounted as independent validation cohorts. It is not
biological evidence, does not import expression data, and does not change any
grounded finding.

## Generated Outputs

| artifact | purpose |
|---|---|
| `analysis/v50_negative_source_search_index/negative_near_miss_index.tsv` | Row-level no-recount index for V50 metadata hits reviewed through the source-hit independence QA. |
| `analysis/v50_negative_source_search_index/summary.json` | Machine-readable summary counts for rows, safe-use classes, and canonical source clusters. |
| `scripts/v50_build_negative_source_search_index.py` | Reproducible generator for the TSV/JSON outputs. |

## Index Semantics

Each row is a reviewed source hit, not a cohort. The column
`exact_validation_candidate` is `false` for every current row, and
`no_recount_without_new_same_definition_package` is `true` for every current
row. A future scout may only reopen a row if a new package, label file, source
locator, or access-terms change satisfies the same-definition gates in
`knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md`.

The index distinguishes:

- `partial_hit_metadata_only`: metadata is potentially useful but insufficient
  for a validation run.
- `context_only`: adjacent MS/treatment biology but not a same-definition V22 /
  V32 validation cohort.
- `reject_false_positive`: keyword collision or otherwise irrelevant hit.

## Boundary

The machine-readable index prevents duplicated search labor and source-count
inflation. It does not prove that no validation cohort exists. It records only
that the reviewed V50 metadata routes produced `0` verified exact validation
candidates and `0` allowed independent source counts.

Source: `docs/knowledge/EPISTEMIC_CLASSES.md`;
`knowledge_external/synthesis/V50_SOURCE_HIT_INDEPENDENCE_QA.md`;
`knowledge_external/catalogs/indexes/V50_NEGATIVE_SOURCE_SEARCH_INDEX.md`.
