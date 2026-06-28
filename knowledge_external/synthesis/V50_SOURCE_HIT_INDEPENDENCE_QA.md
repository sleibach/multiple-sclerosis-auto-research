# V50 Source-Hit Independence QA

Status: source-search QA / de-duplication audit. This artifact reviews V50
non-OpenGWAS cohort-search hits for duplicate/source-cluster risk. It does not
import data, assert validation, or treat external metadata as evidence.

## Inputs

- `analysis/v50_treatment_response_cohort_search/candidate_manual_review.tsv`
- `analysis/v50_biostudies_treatment_response_search/candidate_manual_review.tsv`
- `knowledge_external/templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md`
- `knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md`

## Outputs

- `analysis/v50_source_hit_independence_qa/source_hit_independence_qa.tsv`
- `analysis/v50_source_hit_independence_qa/summary.json`

## QA Result

| metric | value |
|---|---:|
| rows reviewed | `11` |
| independent source counts allowed | `0` |
| duplicate or already-existing clusters | `3` |
| partial-hit rows | `3` |
| context-only rows | `7` |
| false-positive rows | `1` |
| OpenGWAS used | `false` |

## Main De-Duplication Findings

| source hit | cluster decision | safe handling |
|---|---|---|
| `S-EPMC10360655` | Same source cluster as Sánchez-Sanz / `GSE235357`, already represented by local held data and a V50 external record. | Do not count as fresh independent validation; keep as partial metadata route only. |
| `S-EPMC9351505` | Same source cluster as the existing Diebold 2022 high-dimensional DMF immune-monitoring external record and V24 scout row. | Context only; not an independent transcriptomic validation source. |
| `S-EPMC6068231` / `S-EPMC10855583` | Fingolimod response transcriptome family overlaps the already-audited non-DMF fingolimod response lineage; not a DMF/V22 exact route. | Partial/context only; do not count as independent DMF corroboration. |
| Task-68 NCBI/Europe PMC rows | Adjacent context or false-positive clusters. | Do not count as cohort candidates. |

## Verdict

The V50 non-OpenGWAS metadata searches did not add any independent validation
source count. Their value is narrower but still useful:

1. `S-EPMC10360655` is a concrete near-candidate/source route, but it is not new
   independent evidence because the project already holds/used `GSE235357` and
   already has a V50 external context record for the same source family.
2. Diebold 2022 and fingolimod transcriptome hits should be kept as context or
   partial rows, not independent corroboration of the locked V22 scalar.
3. Future source-search accounting should count source clusters, not individual
   API hits or alternate paper/repository pages.

This QA prevents overclaiming: repeated metadata hits strengthen navigation, not
evidence, unless they identify a genuinely independent cohort that satisfies all
same-definition gates.

## Provenance

Prepared on 2026-06-28 from committed V50 metadata-search outputs. Source:
`docs/knowledge/EPISTEMIC_CLASSES.md`;
`knowledge_external/templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md`.
