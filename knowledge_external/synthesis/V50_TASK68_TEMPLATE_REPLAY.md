# V50 Task-68 Template Replay

Status: QA replay / source-search process audit. This artifact applies the
V50 non-OpenGWAS source-hit review template to the five heuristic candidate rows
from the Europe PMC / NCBI GDS treatment-response search. It does not import
expression data, call OpenGWAS, assert cohort usability, or make a biological
claim.

## Inputs

- `analysis/v50_treatment_response_cohort_search/candidate_manual_review.tsv`
- `knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md`

## Outputs

- `analysis/v50_task68_template_replay/task68_template_replay.tsv`
- `analysis/v50_task68_template_replay/summary.json`

## Replay Result

| metric | value |
|---|---:|
| rows replayed | `5` |
| candidate exact cohorts | `0` |
| partial metadata hits | `0` |
| context-only rows | `4` |
| rejected false positives | `1` |
| OpenGWAS used | `false` |

## Row-Level Safe Outcomes

| source | item | safe outcome | reason |
|---|---|---|---|
| Europe PMC `39949773` | Apheresis relapse-treatment gene-expression paper | context only | Relapse/aferesis context is not same-definition DMF or immune-remodeling/JAK-STAT paired baseline/early-treatment response validation. |
| NCBI GDS `GSE261258` | Regulatory memory B cells in MS | context only | Human MS immune-cell dysfunction context, but no treatment-response exposure, paired treatment timing, or response endpoint visible. |
| NCBI GDS `GSE239703` | RelA/c-Rel CD4+ T-cell function scRNA | context only | Mechanistic MS/cancer cell-function context, not a paired treatment-response validation cohort. |
| NCBI GDS `GSE239700` | RelA/c-Rel CD4+ T-cell function bulk mouse | context only | Mouse/mechanistic context, not a human paired treatment-response validation cohort. |
| NCBI GDS `GSE312339` | Guinea pig liver transcriptomes | reject false positive | Non-MS animal/liver keyword collision. |

## QA Verdict

The V50 source-hit review template reproduces the stricter manual outcome for
the task-68 heuristic candidates: none can be counted as an exact cohort, and no
row should move into validation or future-grounding without new same-definition
metadata. This supports using the template for subsequent non-OpenGWAS
metadata searches, because it makes the conservative decision boundary explicit.

This is a process QA result only. It is not evidence about MS biology and does
not change the V22 rule, V42 pre-registration, or any grounded finding.

## Provenance

Prepared on 2026-06-28 from task-68 metadata-only review rows. Source:
`docs/knowledge/EPISTEMIC_CLASSES.md`; template:
`knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md`.
