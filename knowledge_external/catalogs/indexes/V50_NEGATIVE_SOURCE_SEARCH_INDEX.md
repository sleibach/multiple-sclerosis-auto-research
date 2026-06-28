# V50 Negative Source-Search Index

Status: source-search navigation index. This catalog records V50 non-OpenGWAS
metadata searches that did **not** produce a verified exact validation cohort,
plus near-misses that should not be rediscovered as fresh exact candidates. It
does not make biological claims, import expression data, or change any grounded
finding.

## Search Runs Indexed

| search artifact | routes | scale | exact validation candidates | safe interpretation |
|---|---|---:|---:|---|
| `knowledge_external/synthesis/V50_TREATMENT_RESPONSE_COHORT_SEARCH.md` | Europe PMC, NCBI GDS | `4` Europe PMC queries, `3` NCBI GDS queries, `49` deduplicated hits | `0` | Negative metadata source-search result; not a biological null. |
| `knowledge_external/synthesis/V50_BIOSTUDIES_TREATMENT_RESPONSE_SEARCH.md` | EBI BioStudies / ArrayExpress-style metadata | `8` queries, `80` raw hits, `56` deduplicated hits | `0` | Found near-candidates, but no exact early-treatment V22/V32 validation cohort. |
| `knowledge_external/synthesis/V50_TASK68_TEMPLATE_REPLAY.md` | QA replay of Europe PMC / NCBI GDS candidates | `5` candidate rows replayed | `0` | Template replay confirmed `4` context-only rows and `1` false positive. |

## Near-Miss Rows To Avoid Re-Counting

| source | why it is useful | why it is not exact | future handling |
|---|---|---|---|
| BioStudies `S-EPMC10360655` | DMF PBMC RNA-seq with baseline and 12-month sampling plus NEDA-3/EDA-3 response labels. | Not early-treatment V22/V32 validation timing from metadata; not yet a verified runnable package. | Treat as `partial_hit_metadata_only`; request/check package fields only under explicit terms. |
| BioStudies `S-EPMC10855583` | Fingolimod PBMC RNA-seq treatment-response transcriptome context. | Different drug and late timepoint. | Context for non-DMF monitoring-state questions only. |
| BioStudies `S-EPMC6068231` | Fingolimod baseline/6-month transcriptome and NEDA-3/NEDA-4 outcomes. | Different drug; not DMF/V22 exact validation. | Context or future non-DMF preregistered question only. |
| BioStudies `S-EPMC9351505` | DMF longitudinal PBMC immune-response biomarker context. | Mass-cytometry/flow context, not transcriptomic V22 module readout. | Context only. |
| Europe PMC `39949773` | Relapse-treatment gene-expression context. | Apheresis/NMOSD relapse-treatment frame, not same-definition DMF/APC-HLA monitoring validation. | Context only unless a full package shows exact V22/V32 gates. |
| NCBI GDS `GSE261258` | Human MS B-cell dysfunction context. | No treatment-response exposure, paired treatment timing, or response endpoint visible. | Context only. |
| NCBI GDS `GSE239703` | MS/cancer CD4+ T-cell function scRNA context. | Mechanistic cell-function dataset, not paired treatment-response validation. | Context only. |
| NCBI GDS `GSE239700` | RelA/c-Rel mouse mechanistic context. | Not a human paired treatment-response validation cohort. | Context only; do not count for validation. |
| NCBI GDS `GSE312339` | None for this project. | Non-MS animal/liver keyword collision. | Reject as false positive. |

## Rules For Future Searches

1. Do not rerun the same query route just to rediscover these near-misses unless
   a new source locator, release, package, or access-terms change appears.
2. Do not count any near-miss as a usable validation cohort until all
   same-definition gates in
   `knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md`
   are satisfied.
3. If a near-miss becomes inspectable under allowed terms, create a new
   future-grounding route; do not edit the historical negative-search result.
4. Keep OpenGWAS disabled until token renewal; these indexed searches used only
   non-OpenGWAS metadata routes.

## Boundary

This index prevents duplicated source-search labor and overcounting of
near-misses. It does not prove that no external validation cohort exists. It
only records that these V50 non-OpenGWAS metadata searches did not verify one.
Source: `docs/knowledge/EPISTEMIC_CLASSES.md`;
`knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md`.
