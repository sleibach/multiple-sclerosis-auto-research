# V50 Source-Search Deduplication Decision Table

Status: public source-accounting guide. This is navigation and operations
material only. It is not biological evidence, does not validate any cohort, and
does not change the locked V22 rule or any validation pre-registration.

## Decision Table

| incoming source-hit pattern | current V50 handling | reason | required next action |
|---|---|---|---|
| Matches `hit_id`, `locator`, or `canonical_cluster` in `analysis/v50_negative_source_search_index/negative_near_miss_index.tsv` | `BLOCK_RECOUNT` | Already reviewed as duplicate, partial metadata, context-only, or false positive. | Run `scripts/v50_check_source_hit_recount.py`; do not count unless a new same-definition package or terms change exists. |
| Same Sánchez-Sanz / `GSE235357` / `S-EPMC10360655` source family | Already-known source family, not an independent cohort | The project already has the local GSE235357 evidence lane and V50 has the external metadata lane. | Use `knowledge_external/synthesis/V50_GSE235357_SEPMC10360655_HANDOFF.md`. |
| Same Diebold 2022 DMF immune-monitoring source family | Context only, not transcriptomic V22 validation | Mass-cytometry / flow context does not satisfy the transcriptomic same-definition gate. | Keep as context unless a new compatible transcriptomic package appears. |
| Same fingolimod response transcriptome family | Partial/context only | Different drug and late timepoint; not a DMF/V22 exact validation route. | Only use under a preregistered non-DMF monitoring question. |
| Broad treatment-response paper without sample-level pairing, labels, and module-gene coverage | `context_only` or `partial_hit_metadata_only` | Metadata is insufficient for validation-source counting. | Fill the V50 source-hit review template before any count changes. |
| New accession with paired baseline/early treatment, response endpoint, and module-gene coverage visible | Candidate route, not yet evidence | It may satisfy same-definition gates, but metadata is not validation. | Quarantine package; run intake template, no-recount checker, and frozen harness only if terms allow. |

## Rule

Count source clusters, not API hits. Repeated appearances across Europe PMC,
BioStudies, GEO/OmicsDI, or paper pages improve navigation but do not create
independent validation evidence. Source: `docs/knowledge/EPISTEMIC_CLASSES.md`;
`knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md`;
`knowledge_external/templates/V50_SOURCE_HIT_NO_RECOUNT_CHECKER.md`.

## Current Anchors

- Machine-readable no-recount index:
  `knowledge_external/catalogs/indexes/V50_NEGATIVE_SOURCE_SEARCH_INDEX_MACHINE_READABLE.md`
- Query reproducibility packet:
  `knowledge_external/synthesis/V50_BIOSTUDIES_QUERY_REPRODUCIBILITY_PACKET.md`
- Source-family handoff:
  `knowledge_external/synthesis/V50_GSE235357_SEPMC10360655_HANDOFF.md`
