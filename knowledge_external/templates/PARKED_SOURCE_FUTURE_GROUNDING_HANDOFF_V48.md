# V48 Parked Source Future-Grounding Handoff Rules

Status: template/navigation only. These rules apply when a source hit has left
access/terms parking and appears to contain a claim, data route, or method that
could be regrounded by a future project run. The handoff creates a queued task
only; it does not conclude the claim, assert convergence, flag contradiction, or
change grounded findings.

- handoff criteria: `8`
- handoff outcomes: `5`
- required linked controls: `7`

## Required Controls

Use these rules only with:

- `knowledge_external/templates/SOURCE_HIT_ACCESS_TERMS_PARKING_QUEUE_V48.md`
- `knowledge_external/templates/PARKED_SOURCE_RELEASE_CHECKLIST_V48.md`
- `knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md`
- `knowledge_external/templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md`
- `knowledge_external/templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md`
- `knowledge_external/templates/CONTRADICTION_TRIAGE_MINI_TEMPLATE_V48.md`
- `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md`

## Handoff Criteria

| order | criterion | required handling |
|---:|---|---|
| 1 | Source has a stable locator and cleared access/terms route. | Cite locator in the queued task only. |
| 2 | De-duplication and source-independence review are complete. | Record canonical source cluster. |
| 3 | The source contains a claim, dataset, or method that can be tested on reachable data. | Define the exact future test. |
| 4 | The project has or can reasonably acquire the needed data without violating terms. | Name held/reachable data or blocker. |
| 5 | The claim maps to a specific grounded finding, V37 gap, or V48 relationship question. | Name the project artifact and gap. |
| 6 | The test does not require changing a locked rule or pre-registration. | If it would, route as tension only. |
| 7 | The queued test has a falsifiable pass/fail/inconclusive criterion. | State the criterion before running. |
| 8 | Multiple-testing and provenance gates are identified. | Name the linter/gate or future analysis guard. |

## Handoff Outcomes

| outcome | use when | boundary |
|---|---|---|
| `queue_future_grounding` | Testable claim/data route exists and terms permit queued summary. | queued task only |
| `queue_definition_mapping` | Source terminology differs but may map to a grounded finding. | definition task only |
| `queue_access_request` | Claim appears testable but data/access is not yet available. | external blocker |
| `park_insufficient_specificity` | The source is too vague to test. | no conclusion |
| `reject_no_grounding_route` | No reachable or plausible test can be defined. | no follow-up |

## Minimum Future-Grounding Task

Record these fields before adding or updating a future-grounding queue row:

1. Source locator and release checklist ID.
2. Canonical source cluster/de-duplication note.
3. Project finding, V37 gap, or relationship row it may address.
4. Exact testable prediction.
5. Required data and whether it is held, reachable, or blocked.
6. Pre-specified supported/not-supported/inconclusive criterion.
7. Required null, cross-validation, or multiple-testing guard.
8. Explicit statement that the queued task is not a finding.

## Forbidden Shortcuts

- Do not promote a queued future-grounding task into a convergence or
  contradiction row before the project has run the test.
- Do not treat a source's own confidence, author language, model summary, or
  database score as evidence.
- Do not queue vague claims that cannot be falsified.
- Do not bypass locked rules or pre-registrations.
- Do not use future-grounding status to change evidence grades, validation
  plans, or grounded findings.

## Verification Before Commit

```bash
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit
python3 scripts/v48_governance_preflight.py
```

## Boundary

This handoff is a work-queue control. It can preserve a testable idea for a
future project run, but the idea remains ungrounded until that run executes on
project data under the normal evidence gate.
