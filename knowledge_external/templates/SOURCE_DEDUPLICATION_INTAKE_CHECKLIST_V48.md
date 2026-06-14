# V48 Source De-Duplication Intake Checklist

Status: template/navigation only. This checklist is for future external-source
intake before any source is counted as independent corroboration, candidate
contradiction, or future-grounding input. It does not add external records,
assert relationship rows, merge evidence, or change grounded findings.

- de-duplication checks: `9`
- duplicate states: `5`
- safe merge actions: `5`
- required linked controls: `6`

## Required Controls

Use this checklist only with:

- `knowledge_external/templates/SOURCE_INTAKE_PACKAGE_MANIFEST_V48.md`
- `knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md`
- `knowledge_external/templates/SOURCE_HIT_ACCESS_TERMS_PARKING_QUEUE_V48.md`
- `knowledge_external/catalogs/indexes/SOURCE_URL_DUPLICATE_REVIEW_V48.md`
- `knowledge_external/synthesis/CONVERGENCE_SOURCE_INDEPENDENCE_V48.md`
- `knowledge_external/catalogs/indexes/SOURCE_DOMAIN_INDEPENDENCE_ROLLUP_V48.md`

## De-Duplication Checks

| order | check | safe handling |
|---:|---|---|
| 1 | Does the hit have the same DOI, PMID, accession, or canonical URL as an existing record? | Mark as exact duplicate; do not count as independent. |
| 2 | Does a redirected, shortened, or alternate URL resolve to an already-recorded source? | Canonicalize to the existing source locator. |
| 3 | Is the hit a publisher page, repository landing page, or supplement page for the same underlying paper/data? | Link as same-source material, not a new source. |
| 4 | Is the hit a review, editorial, or database annotation citing the same primary source already counted? | Treat as secondary context unless it adds a distinct primary locator. |
| 5 | Does the hit share authors, cohort, accession, and measurement layer with an existing source? | Treat as possible cohort/source reuse; require independence note. |
| 6 | Does the hit report the same cohort under a different disease, drug, or endpoint framing? | Record definition difference; do not overcount source independence. |
| 7 | Does it reuse a public database export of the same underlying association? | Count the database and primary source as one canonical source cluster. |
| 8 | Does it provide a genuinely independent cohort, dataset, or analysis under the same definition? | Candidate independent source; proceed to relationship-row review. |
| 9 | Is independence unclear after the checks above? | Park for source-independence review before any relationship update. |

## Duplicate States

| state | meaning | boundary |
|---|---|---|
| `exact_duplicate` | Same DOI/PMID/accession/canonical URL as an existing record. | no new source count |
| `same_source_material` | Same paper/data under supplement, repository, or publisher page. | same canonical cluster |
| `secondary_restatement` | Review/database/opinion restates an already-counted primary source. | context only |
| `possible_reuse` | Same cohort/authors/accession/layer but not conclusively identical. | park for review |
| `candidate_independent` | Distinct cohort/data/source under same definition. | candidate only until reviewed |

## Safe Merge Actions

| action | when allowed | required note |
|---|---|---|
| `canonicalize_locator` | Exact or redirected duplicate. | Preferred source locator and alternate locator. |
| `link_same_source_material` | Supplement/repository/publisher pages for one source. | Canonical source cluster ID. |
| `context_only_secondary` | Review or database restatement. | Primary source it restates, if known. |
| `park_independence_review` | Possible reuse or unclear independence. | Missing information needed. |
| `proceed_candidate_independent` | Distinct source under same definition. | Source-independence rationale. |

## Minimum Independence Note

Before a source can be counted as independent, record:

1. Canonical locator and alternate locators checked.
2. Existing source records compared.
3. Cohort, accession, population, layer, and outcome overlap review.
4. Whether the source is primary data, database annotation, review, or
   secondary context.
5. Canonical source cluster assignment.
6. Why it can or cannot be counted as independent corroboration.

## Forbidden Shortcuts

- Do not count publisher, repository, supplement, and database pages for one
  study as multiple independent sources.
- Do not count a review as independent corroboration of a primary source it
  merely restates.
- Do not use model/RPT summaries to decide source independence.
- Do not create convergence or contradiction rows when independence is unclear.
- Do not let duplicate external sources change grounded findings, locked rules,
  validation plans, or evidence grades.

## Verification Before Commit

```bash
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit
python3 scripts/v48_governance_preflight.py
```

## Boundary

This checklist controls source independence and duplicate handling only. It
does not decide scientific truth, does not make an external source evidence,
and does not override the grounded project artifact. It protects the V48
convergence/contradiction layer from same-source overcounting.
