# V48 Source-Intake Reproducibility Checklist

Status: template/navigation only. This checklist lets a future reviewer rerun
and reproduce an external-source intake decision from the locator, audit log,
and governance controls. It does not add external records, assert relationships,
judge scientific truth, or change grounded findings.

- reproducibility checks: `12`
- reviewer outcomes: `5`
- required linked controls: `8`

## Required Controls

Use this checklist only with:

- `knowledge_external/templates/EXTERNAL_INTAKE_ONE_PAGE_CHECKLIST_V48.md`
- `knowledge_external/templates/SOURCE_INTAKE_AUDIT_LOG_TEMPLATE_V48.md`
- `knowledge_external/templates/SOURCE_INTAKE_DECISION_ERROR_TAXONOMY_V48.md`
- `knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md`
- `knowledge_external/templates/SOURCE_HIT_ACCESS_TERMS_PARKING_QUEUE_V48.md`
- `knowledge_external/templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md`
- `knowledge_external/templates/PARKED_SOURCE_RELEASE_CHECKLIST_V48.md`
- `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md`

## Reproducibility Checks

| order | check | pass condition |
|---:|---|---|
| 1 | Source locator can be re-opened or resolved. | Stable DOI, URL, accession, or citation still works. |
| 2 | Access/terms route matches the audit record. | No unsupported access or reuse assumption is present. |
| 3 | No copied external claims entered routing artifacts. | Audit/routing text is locator-level or operator-level only. |
| 4 | Source de-duplication can be rerun. | Canonical source cluster is reproducible. |
| 5 | Source independence conclusion is reproducible. | Same-source and secondary-source checks match the audit note. |
| 6 | Same-definition overlap decision is reproducible. | Population, layer, outcome, direction, and scope assessment matches. |
| 7 | Acceptance-tree outcome is reproducible. | Safe outcome A-F can be independently re-derived. |
| 8 | Parking or release decision is reproducible. | Blocker/resolution status matches the linked control. |
| 9 | Candidate relationship or future-grounding route remains a candidate only. | No finding/evidence language was introduced. |
| 10 | Required verification commands were run or are queued before commit. | Gate command list is present. |
| 11 | Any process error is classed with the decision error taxonomy. | Error class and severity are recorded if needed. |
| 12 | The reviewer reaches the same safe routing outcome. | If not, record a reproducibility discrepancy. |

## Reviewer Outcomes

| outcome | use when | required action |
|---|---|---|
| `reproduced` | Reviewer reaches the same routing outcome with the same boundary. | Leave decision in place. |
| `minor_documentation_fix` | Outcome is sound but a field or note is incomplete. | Patch documentation and rerun gates. |
| `route_discrepancy` | Reviewer reaches a different safe routing outcome. | Reclassify using the audit log and error taxonomy. |
| `quarantine_required` | Evidence leakage, external override, or unsafe relationship promotion occurred. | Quarantine affected artifact and rerun full preflight. |
| `external_blocked` | Reproduction is blocked by access, terms, or missing locator. | Park with explicit blocker. |

## Minimum Review Record

Record these fields for each reproducibility review:

1. Audit ID and source locator.
2. Reviewer and UTC date.
3. Controls rerun.
4. Reproducibility check failures, if any.
5. Reviewer outcome.
6. Correction route or blocker.
7. Verification commands rerun.
8. Statement that review outcome does not make the source evidence.

## Forbidden Shortcuts

- Do not call a source-intake decision reproducible without reopening the
  locator or documenting why access is blocked.
- Do not treat reviewer agreement as scientific evidence.
- Do not use model/RPT output to replace reviewer reproduction.
- Do not leave evidence leakage unquarantined.
- Do not change grounded findings, locked rules, validation plans, or evidence
  grades during reproducibility review.

## Verification Before Commit

```bash
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit
python3 scripts/v48_governance_preflight.py
```

## Boundary

This checklist reproduces operator routing decisions only. Reproducible intake
does not mean the external source is correct and does not turn external material
into project-grounded evidence.
