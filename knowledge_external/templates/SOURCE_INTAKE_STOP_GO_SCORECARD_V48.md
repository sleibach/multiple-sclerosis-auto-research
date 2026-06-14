# V48 Source-Intake Stop/Go Scorecard

Status: template/navigation only. This scorecard gives future operators a
pre-specified stop/park/go routing decision for external source hits. It does
not score scientific truth, add external records, assert relationships, or
change grounded findings.

- scorecard criteria: `10`
- decision outcomes: `5`
- required linked controls: `8`

## Required Controls

Use this scorecard only with:

- `knowledge_external/templates/EXTERNAL_INTAKE_ONE_PAGE_CHECKLIST_V48.md`
- `knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md`
- `knowledge_external/templates/SOURCE_HIT_ACCESS_TERMS_PARKING_QUEUE_V48.md`
- `knowledge_external/templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md`
- `knowledge_external/templates/SOURCE_INTAKE_AUDIT_LOG_TEMPLATE_V48.md`
- `knowledge_external/templates/SOURCE_INTAKE_DECISION_ERROR_TAXONOMY_V48.md`
- `knowledge_external/templates/SOURCE_INTAKE_REPRODUCIBILITY_CHECKLIST_V48.md`
- `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md`

## Scorecard Criteria

| order | criterion | stop | park | go |
|---:|---|---|---|---|
| 1 | Stable locator | missing | unstable | stable |
| 2 | Access route | prohibited | unclear | documented |
| 3 | Reuse/summary terms | restricted | unknown | safe for short summary |
| 4 | Copied source content | present | unclear | absent |
| 5 | De-duplication | duplicate and unhandled | possible reuse | canonical cluster assigned |
| 6 | Source independence | not independent | unclear | independent or same-source labeled |
| 7 | Same-definition overlap | fails | partial/unclear | passes |
| 8 | Relationship/future-grounding route | none | unclear | safe candidate/queue route |
| 9 | Auditability | missing audit fields | incomplete | complete |
| 10 | Boundary risk | external would override grounded result | tension unresolved | boundary preserved |

## Decision Outcomes

| outcome | use when | required next action |
|---|---|---|
| `stop_reject` | Any non-recoverable stop condition is present. | Reject source hit; record audit note. |
| `park_access_terms` | Access, terms, locator, or copied-content uncertainty remains. | Park without source claims. |
| `park_independence_or_definition` | Independence or same-definition overlap is unclear. | Run de-duplication or definition review. |
| `go_candidate_intake` | Locator, terms, independence, and same-definition checks pass. | Use candidate relationship or future-grounding controls. |
| `go_context_only` | Source is useful but not same-definition. | Record context/insufficient-overlap only if needed. |

## Minimum Scorecard Entry

```yaml
source_locator:
date_utc:
operator:
criteria:
  stable_locator:
  access_route:
  reuse_terms:
  copied_content:
  deduplication:
  source_independence:
  same_definition_overlap:
  route:
  auditability:
  boundary_risk:
decision_outcome:
next_action:
boundary_statement:
```

## Forbidden Shortcuts

- Do not use the scorecard to rate biological plausibility.
- Do not average criteria into a numeric evidence score.
- Do not proceed when access/terms, copied-content, or external-override risk
  is unresolved.
- Do not let model/RPT output override a stop or park condition.
- Do not treat `go_candidate_intake` as a finding.

## Verification Before Commit

```bash
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit
python3 scripts/v48_governance_preflight.py
```

## Boundary

The stop/go scorecard is an intake-routing tool. It decides whether a source hit
can proceed to another control, not whether the source is true and not whether a
project conclusion should change.
