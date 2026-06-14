# V48 Source-Intake Audit Log Template

Status: template/navigation only. This template records future operator decisions
during external-source intake. It is an audit trail for routing choices, not a
source record, relationship row, evidence item, or project finding.

- audit fields: `14`
- decision event types: `8`
- required linked controls: `8`

## Required Controls

Use this audit log only with:

- `knowledge_external/templates/EXTERNAL_INTAKE_ONE_PAGE_CHECKLIST_V48.md`
- `knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md`
- `knowledge_external/templates/SOURCE_HIT_ACCESS_TERMS_PARKING_QUEUE_V48.md`
- `knowledge_external/templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md`
- `knowledge_external/templates/PARKED_SOURCE_RELEASE_CHECKLIST_V48.md`
- `knowledge_external/templates/PARKED_SOURCE_FUTURE_GROUNDING_HANDOFF_V48.md`
- `knowledge_external/templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md`
- `knowledge_external/templates/CONTRADICTION_TRIAGE_MINI_TEMPLATE_V48.md`

## Audit Fields

| order | field | purpose |
|---:|---|---|
| 1 | `audit_id` | Stable local ID for the decision event. |
| 2 | `date_utc` | UTC date/time of the decision. |
| 3 | `operator` | Person or agent making the routing decision. |
| 4 | `source_locator` | DOI, URL, accession, repository ID, or citation pointer. |
| 5 | `source_locator_status` | stable / unstable / missing. |
| 6 | `decision_event_type` | One of the event types below. |
| 7 | `decision_summary` | Short routing decision without copied external claims. |
| 8 | `control_used` | Checklist, tree, or linter that governed the decision. |
| 9 | `input_artifact` | Parking ID, source-hit packet, or candidate row ID, if any. |
| 10 | `output_artifact` | Next artifact or queue row, if any. |
| 11 | `boundary_statement` | Why this decision is not evidence or a finding. |
| 12 | `blocked_by` | External blocker if unresolved. |
| 13 | `verification_commands` | Commands run or required before commit. |
| 14 | `next_action` | Concrete next operator or future-grounding action. |

## Decision Event Types

| event_type | use when | boundary |
|---|---|---|
| `reject_source_hit` | Locator, access, terms, or relevance fails. | no intake |
| `park_access_terms` | Access, terms, reuse, or locator uncertainty remains. | no source claims copied |
| `canonicalize_duplicate` | Source hit duplicates or reuses an existing canonical source cluster. | no independent source count |
| `release_from_parking` | Parked source passes release checks. | intake may begin |
| `candidate_convergence_row` | Same-definition agreement appears plausible after checks. | candidate only |
| `candidate_contradiction_row` | Same-definition disagreement appears plausible after triage. | tension flag only |
| `future_grounding_route` | Testable claim/data route can be queued. | queued task only |
| `insufficient_overlap` | Source is adjacent but not same-definition. | context/routing only |

## Minimum Audit Entry Skeleton

```yaml
audit_id:
date_utc:
operator:
source_locator:
source_locator_status:
decision_event_type:
decision_summary:
control_used:
input_artifact:
output_artifact:
boundary_statement:
blocked_by:
verification_commands:
next_action:
```

## Forbidden Shortcuts

- Do not include copied source claims, abstracts, tables, figures, or long
  excerpts in an audit entry.
- Do not use an audit entry as evidence for a project conclusion.
- Do not let an audit entry create or modify a relationship row by itself.
- Do not use model/RPT outputs as the audit decision authority.
- Do not omit the boundary statement.

## Verification Before Commit

```bash
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit
python3 scripts/v48_governance_preflight.py
```

## Boundary

The audit log records operator decisions so future maintainers can reproduce
why a source hit was rejected, parked, released, canonicalized, or routed. It
does not make external material project-grounded and does not alter any grounded
finding, locked rule, validation plan, or evidence grade.
