# V48 Contradiction Triage Mini-Template

Status: template/navigation only. This mini-template is for future source hits
that appear to disagree with a grounded project finding. It does not assert a
contradiction, resolve a contradiction, override a grounded finding, or change
the V48 relationship matrix.

- triage questions: `8`
- safe outcomes: `5`
- required linked controls: `5`

## Required Controls

Use this template only with:

- `knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md`
- `knowledge_external/templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md`
- `knowledge_external/synthesis/CONTRADICTION_READINESS_PLAYBOOK_V48.md`
- `knowledge_external/synthesis/CONTRADICTION_SURVEILLANCE_CHECKLIST_V48.md`
- `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md`

## Triage Questions

| order | question | safe handling |
|---:|---|---|
| 1 | Which grounded finding is allegedly contradicted? | Record the exact finding ID and grounded artifact path. |
| 2 | Is the source using the same population, disease subtype, compartment, direction, and outcome? | If not, mark insufficient overlap instead of contradiction. |
| 3 | Is the source independent from any already-counted canonical source cluster? | If not, record same-source reuse and avoid overcounting. |
| 4 | Is the source a review/opinion rather than primary data or a data-bearing resource? | Treat as context only unless a primary route is supplied. |
| 5 | Does the source actually disagree, or only use different terminology? | If terminology differs, queue a definition-mapping note. |
| 6 | Can the disagreement be regrounded on reachable data? | If yes, add an exact future-grounding route. |
| 7 | Is the disagreement clinically or methodologically decision-relevant? | If not, park as low-priority context. |
| 8 | Would accepting this source require changing a locked rule or grounded finding? | Do not change it; route as tension only pending project grounding. |

## Safe Outcomes

| outcome | action | boundary |
|---|---|---|
| `insufficient_overlap` | Do not create a contradiction row; record overlap failure if useful. | no contradiction asserted |
| `terminology_mismatch` | Queue a definition-mapping note. | no contradiction asserted |
| `candidate_contradiction` | Draft a candidate row using the relationship-row candidate template. | candidate only |
| `future_grounding_route` | Add a concrete test to the future-grounding queue. | queued task only |
| `low_priority_context` | Park as context if not decision-relevant. | no matrix change |

## Minimum Candidate Notes

Before a contradiction candidate can be reviewed, record:

1. Grounded finding ID and artifact path.
2. Source locator and access date.
3. Same-definition overlap review.
4. Source-independence note.
5. Exact disagreement statement.
6. Future-grounding route if one exists.
7. Why the external source does not override the grounded result.

## Boundary

- External disagreement is a tension flag, not a decision.
- The grounded project artifact remains the evidence until a future project run
  regrounds the issue on project data.
- Candidate contradictions must pass the V47 provenance gate and V48 governance
  preflight before any relationship-matrix update is considered.
