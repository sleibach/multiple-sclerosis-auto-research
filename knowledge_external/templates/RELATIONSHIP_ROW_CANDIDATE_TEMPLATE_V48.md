# V48 Relationship-Row Candidate Template

Status: template/navigation only. This template is for drafting future candidate
rows before they are accepted into the V48 convergence/contradiction matrix. It
does not add a matrix row, assert convergence, flag contradiction, or change any
grounded finding.

- required fields: `15`
- allowed candidate statuses: `4`
- forbidden shortcuts: `5`

## When To Use

Use this template only after a source hit has passed the source-hit acceptance
decision tree:

- `knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md`

If the source hit fails same-definition overlap review, do not use this
template. Record an insufficient-overlap note instead.

## Candidate Row Fields

| field | required | meaning |
|---|---|---|
| `candidate_id` | yes | Stable draft identifier for the candidate row. |
| `grounded_finding_id` | yes | Existing project finding ID from the scored findings report or V48 matrix. |
| `grounded_artifact` | yes | Existing grounded artifact path; the project artifact remains the evidence. |
| `external_record_or_source_id` | yes | External record ID if already ingested, or source-hit locator if not yet ingested. |
| `source_locator` | yes | DOI, URL, accession, or repository identifier. |
| `date_accessed` | yes | Date the source was checked. |
| `epistemic_class` | yes | Class assigned using `docs/knowledge/EPISTEMIC_CLASSES.md`. Source: `docs/knowledge/EPISTEMIC_CLASSES.md`. |
| `candidate_status` | yes | One of the allowed candidate statuses below. |
| `same_definition_overlap` | yes | Exact population, layer, direction, outcome, and comparator overlap review. |
| `relationship_rationale` | yes | Short reason the source might converge, contradict, or fail overlap. |
| `source_independence_note` | yes | Whether this is a new canonical source cluster or same-source reuse. |
| `forbidden_shortcut_review` | yes | Explicit check that generic adjacent context was not counted. |
| `future_grounding_route` | conditional | Required if the source is testable later on reachable data. |
| `candidate_reviewer` | yes | Person/session preparing the candidate. |
| `candidate_not_accepted_marker` | yes | Explicit marker that this is not yet a relationship-matrix assertion. |

## Allowed Candidate Statuses

| status | use |
|---|---|
| `candidate_convergence` | Source appears to independently agree under the same definition, pending review. |
| `candidate_contradiction` | Source appears to disagree under the same definition, pending review. |
| `insufficient_overlap` | Source is useful context but fails same-definition overlap. |
| `future_grounding_only` | Source proposes a reachable test but cannot support a relationship row yet. |

## Forbidden Shortcuts

| shortcut | required handling |
|---|---|
| Generic MS context presented as same-definition corroboration. | Mark insufficient overlap. |
| Shared-source reuse counted as independent corroboration. | Add source-independence note and do not overcount. |
| External disagreement used to override a grounded finding. | Route as candidate contradiction only. |
| Dataset existence treated as evidence before project analysis. | Queue future grounding only. |
| Model-generated source summary treated as source evidence. | Require the actual source locator and source review. |

## Promotion Rules

A candidate row can enter `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md`
only after:

1. The source is stored or referenced under the segregated external process.
2. Same-definition overlap is reviewed against the grounded finding.
3. Source-independence is checked.
4. The relationship vocabulary is one of the controlled V48 values.
5. `scripts/v48_governance_preflight.py` passes.

## Boundary

- This template creates drafts only.
- Candidate rows are not findings and are not evidence.
- The grounded project artifact remains the evidence.
- External agreement can become corroborating context only after review; it
  never becomes project-grounded evidence by itself.
