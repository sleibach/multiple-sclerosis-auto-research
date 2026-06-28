# V50 Treatment-Response Cohort Search

Status: metadata-only source search. This artifact uses Europe PMC and NCBI GDS
public metadata only, does not import expression data, does not call OpenGWAS,
and does not count any cohort usable without paired timing, response labels, and
module-gene coverage.

## Inputs

- `knowledge_external/synthesis/V50_NON_OPENGWAS_ROUTE_INVENTORY.md`
- `knowledge_external/synthesis/V50_V22_V32_CONTRADICTION_TRIGGER_PACKET.md`
- Europe PMC REST metadata search
- NCBI E-utilities / GDS metadata search

## Outputs

- `analysis/v50_treatment_response_cohort_search/europepmc_hits.tsv`
- `analysis/v50_treatment_response_cohort_search/ncbi_gds_hits.tsv`
- `analysis/v50_treatment_response_cohort_search/trigger_triage.tsv`
- `analysis/v50_treatment_response_cohort_search/candidate_manual_review.tsv`
- `analysis/v50_treatment_response_cohort_search/summary.json`

## Search Scale

| metric | value |
|---|---:|
| Europe PMC queries | `4` |
| Europe PMC deduplicated hits | `32` |
| NCBI GDS queries | `3` |
| NCBI GDS deduplicated hits | `17` |
| heuristic candidate rows | `5` |
| manually reviewed candidate rows | `5` |
| verified exact paired treatment-response candidates | `0` |
| OpenGWAS used | `false` |

## Manual Candidate Review

The heuristic trigger intentionally over-called candidates. Title-level manual
review reduced all five to not-ready or false-positive rows:

| source | item | manual status | reason |
|---|---|---|---|
| Europe PMC | Apheresis relapse-treatment gene-expression paper | not exact V22/V32 candidate | Relapse apheresis/NMOSD context, not DMF or immune-remodeling/JAK-STAT paired baseline/early-on-treatment response validation with V22/V32-compatible endpoint. |
| NCBI GDS | `GSE261258` regulatory memory B cells in MS | not exact V22/V32 candidate | MS immune-cell dysfunction dataset by title; not treatment-response cohort with paired baseline/early-treatment samples and response labels. |
| NCBI GDS | `GSE239703` RelA/c-Rel CD4+ T-cell function scRNA | not exact V22/V32 candidate | Mechanistic cell-function dataset by title; not DMF/paired treatment-response validation cohort. |
| NCBI GDS | `GSE239700` RelA/c-Rel CD4+ T-cell function bulk mouse | not exact V22/V32 candidate | Mouse/mechanistic dataset by title; not human paired treatment-response validation cohort. |
| NCBI GDS | `GSE312339` guinea pig liver transcriptomes | false positive | Non-MS animal/liver record; keyword collision only. |

## Verdict

This pass found **no verified exact paired treatment-response cohort candidate**
that can reduce dependence on Gafson under the V50 trigger rules. That is a
negative source-search result, not a biological null.

The result does not rule out such a cohort existing. It says these specific
Europe PMC and NCBI GDS metadata queries did not surface a verified candidate
with enough title/metadata evidence to count as usable.

## Next Safe Search Moves

1. Broaden query terms to include treatment names beyond dimethyl fumarate only
   after keeping the V22/V32 same-definition trigger rules in force.
2. Use BioStudies/ArrayExpress metadata for accessions surfaced by papers, not
   broad expression-data harvesting.
3. Keep Gafson and Karolinska request paths active because public metadata
   search still does not produce a ready substitute.

## Provenance

Prepared on 2026-06-28 from metadata-only public API searches. No expression
matrix, sample-level labels, or OpenGWAS endpoint was accessed.
