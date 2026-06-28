# V50 Source-Hit No-Recount Checker

Status: source-search operations template. This is a navigation and guardrail
artifact only; it is not biological evidence and does not validate or refute
any project finding.

## Purpose

Future source scouts should run the no-recount checker before treating a
metadata hit as a fresh independent validation source. The checker compares
candidate rows against the V50 machine-readable negative/near-miss index by
`hit_id`, `locator`, and `canonical_cluster`.

## Command

```bash
python3 scripts/v50_check_source_hit_recount.py \
  --input path/to/candidate_hits.tsv \
  --index analysis/v50_negative_source_search_index/negative_near_miss_index.tsv \
  --outdir analysis/v50_source_hit_recount_checker \
  --fail-on-recount
```

Required input columns are flexible but the checker can only match columns that
are present. Use at least one of:

- `hit_id`
- `locator`
- `canonical_cluster`

## Interpretation

`BLOCK_RECOUNT` means the hit matches a reviewed V50 near-miss, context-only
row, false-positive row, or duplicate/already-existing source cluster. It must
not be counted as an independent validation cohort unless a new same-definition
package, label file, source locator, or access-terms change is documented and
routed through
`knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md`.

`PASS_NEW_OR_UNINDEXED` does not mean a hit is usable. It only means it was not
found in the current no-recount index and still requires full source-hit review.

## Current Self-Audit

The committed self-audit uses the current machine-readable index as its own
input and therefore intentionally flags all current rows as `BLOCK_RECOUNT`.
Outputs:

- `analysis/v50_source_hit_recount_checker/source_hit_recount_flags.tsv`
- `analysis/v50_source_hit_recount_checker/summary.json`

Source: `docs/knowledge/EPISTEMIC_CLASSES.md`;
`knowledge_external/catalogs/indexes/V50_NEGATIVE_SOURCE_SEARCH_INDEX_MACHINE_READABLE.md`.
