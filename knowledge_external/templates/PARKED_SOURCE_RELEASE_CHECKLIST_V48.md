# V48 Parked Source Release Checklist

Status: template/navigation only. This checklist controls when a source hit
previously parked for access, terms, reuse, locator, or independence uncertainty
can leave parking and proceed to normal V48 source intake. It does not add
external records, copy source claims, assert convergence, flag contradiction, or
change grounded findings.

- release checks: `10`
- release outcomes: `5`
- required linked controls: `7`

## Required Controls

Use this checklist only with:

- `knowledge_external/templates/SOURCE_HIT_ACCESS_TERMS_PARKING_QUEUE_V48.md`
- `knowledge_external/templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md`
- `knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md`
- `knowledge_external/templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md`
- `knowledge_external/templates/CONTRADICTION_TRIAGE_MINI_TEMPLATE_V48.md`
- `knowledge_external/catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md`
- `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md`

## Release Checks

| order | check | pass condition |
|---:|---|---|
| 1 | Stable locator confirmed. | DOI, accession, persistent URL, or complete citation is recorded. |
| 2 | Access route documented. | Public, requested, author-provided, or controlled-access route is known. |
| 3 | Reuse/summary terms reviewed. | A source_terms metadata entry can be written without guessing. |
| 4 | No restricted content copied during parking. | Parking record contains locator and blocker notes only. |
| 5 | De-duplication completed. | Canonical source cluster and independence note are assigned. |
| 6 | Same-definition overlap checked. | Population, layer, outcome, direction, and scope are comparable or not. |
| 7 | Source class assigned. | Primary data, database annotation, review, secondary context, or repository record. |
| 8 | Safe intake route chosen. | Insufficient overlap, candidate relationship, future grounding, or reject. |
| 9 | Boundary language retained. | Source remains external and non-evidence until project grounding. |
| 10 | Verification commands planned. | Provenance gate and governance preflight will run before commit. |

## Release Outcomes

| outcome | use when | next control |
|---|---|---|
| `release_to_intake` | Locator, access, terms, and de-duplication all pass. | Source-hit acceptance decision tree. |
| `release_to_candidate_relationship` | Same-definition convergence or contradiction candidate is plausible after intake. | Relationship-row candidate template. |
| `release_to_future_grounding` | Source contains a claim/data route that can be regrounded later. | Future-grounding queue. |
| `remain_parked` | One or more release checks still fail. | Parking queue. |
| `reject_after_review` | Source is unusable, unstable, or terms-prohibited. | No further intake. |

## Minimum Release Note

Before a parked source can be released, record:

1. Original parking ID.
2. What blocker was resolved.
3. Stable locator and access route.
4. Terms/reuse note.
5. De-duplication/source-independence note.
6. Same-definition overlap result.
7. Selected release outcome and next control.
8. Statement that release does not make the source evidence.

## Forbidden Shortcuts

- Do not release a source because it is scientifically attractive.
- Do not release a source without stable locator, terms, and de-duplication
  review.
- Do not copy restricted source content into the release note.
- Do not use model/RPT summaries as a replacement for terms or independence
  review.
- Do not treat release from parking as convergence, contradiction, evidence, or
  future-grounding completion.

## Verification Before Commit

```bash
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit
python3 scripts/v48_governance_preflight.py
```

## Boundary

Release from parking is an operator-routing event only. It permits normal intake
review to begin; it does not create a source record, relationship row, or project
finding by itself. Grounded project artifacts remain the evidence.
