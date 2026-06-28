# V50 BioStudies Treatment-Response Cohort Search

Status: metadata-only source search. This artifact uses the EBI BioStudies API
as a BioStudies/ArrayExpress-style route. It does not import expression data,
does not call OpenGWAS, does not validate any project finding, and does not
count any cohort usable without the V50 same-definition gates.

## Inputs

- `knowledge_external/synthesis/V50_NON_OPENGWAS_ROUTE_INVENTORY.md`
- `knowledge_external/synthesis/V50_NON_OPENGWAS_FUTURE_GROUNDING_QUEUE.md`
- `knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md`
- EBI BioStudies API metadata search

## Outputs

- `analysis/v50_biostudies_treatment_response_search/biostudies_hits.tsv`
- `analysis/v50_biostudies_treatment_response_search/biostudies_hits_dedup.tsv`
- `analysis/v50_biostudies_treatment_response_search/biostudies_trigger_triage.tsv`
- `analysis/v50_biostudies_treatment_response_search/candidate_manual_review.tsv`
- `analysis/v50_biostudies_treatment_response_search/summary.json`
- `analysis/v50_biostudies_query_reproducibility/biostudies_query_packet.tsv`
- `analysis/v50_biostudies_query_reproducibility/summary.json`

Exact query strings and encoded BioStudies API URLs are recorded in
`knowledge_external/synthesis/V50_BIOSTUDIES_QUERY_REPRODUCIBILITY_PACKET.md`.

## Search Scale

| metric | value |
|---|---:|
| BioStudies queries | `8` |
| raw BioStudies hits | `80` |
| deduplicated hits | `56` |
| detail records fetched | `29` |
| heuristic candidate rows | `6` |
| manually reviewed rows | `6` |
| near candidates, not exact | `3` |
| verified exact paired treatment-response candidates | `0` |
| OpenGWAS used | `false` |

## Manual Candidate Review

BioStudies metadata surfaced sharper near-candidates than the earlier
Europe PMC / NCBI GDS pass, but none can be counted as an exact frozen V22/V32
validation cohort from metadata alone.

| accession | safe outcome | reason |
|---|---|---|
| `S-EPMC10360655` | partial hit | DMF PBMC RNA-seq with baseline and 12-month treatment sampling plus NEDA-3/EDA-3 response labels. Useful near-candidate, but not exact early-treatment V22/V32 validation timing from metadata, and not yet a verified runnable package. |
| `S-EPMC10855583` | partial hit | Fingolimod PBMC RNA-seq with baseline and 12-month responder/non-responder structure. Relevant treatment-response transcriptome context, but different drug and late timepoint. |
| `S-EPMC6068231` | partial hit | Fingolimod translational study with baseline and 6-month sampling and NEDA-3/NEDA-4 outcomes. Relevant monitoring-state context, but not DMF/V22 exact validation. |
| `S-EPMC4654830` | context only | Interferon beta / SPMS transcriptional response context; different drug and disease-stage frame. |
| `S-EPMC5413827` | context only | DMF NEDA clinical analysis, but no PBMC transcriptomic paired module-validation package visible from metadata. |
| `S-EPMC9351505` | context only | DMF response biomarker study with longitudinal PBMC immune profiling, but mass-cytometry/flow context rather than a transcriptomic V22 module readout. |

## Verdict

This pass found **no verified exact paired treatment-response cohort candidate**
that can mechanically replace Gafson for the frozen V22/V32 validation. It did,
however, identify a higher-value near-candidate route:
`S-EPMC10360655`, a DMF PBMC RNA-seq response study with baseline and 12-month
sampling and NEDA/EDA response labels. That route should be handled as
`partial_hit_metadata_only`: request or inspect allowed package metadata for
sample-level pairing, gene identifiers, normalization, and whether any permitted
timepoint can be interpreted under a pre-specified secondary analysis. It is not
currently a clean early-treatment validation cohort.

This is a source-search result only. It is not a biological null and it does not
change the locked V22 rule, the V42 pre-registration, or the V50 convergence /
contradiction matrix.

## Next Safe Search Moves

1. Use the V50 source-hit review template on `S-EPMC10360655` specifically and
   record the missing fields needed before any future-grounding route.
2. Keep `S-EPMC10855583` and `S-EPMC6068231` as non-DMF monitoring-state
   context only unless a future preregistered non-DMF validation question is
   opened.
3. Add `S-EPMC10360655` to the negative/near-miss source-search index so future
   sessions do not rediscover it as a fresh exact cohort.

## Provenance

Prepared on 2026-06-28 from EBI BioStudies API metadata. External source
metadata is external context until the project regrounds a permitted dataset in
a separate analysis. Source: `docs/knowledge/EPISTEMIC_CLASSES.md`; API route:
`https://www.ebi.ac.uk/biostudies/api/v1/search`.
