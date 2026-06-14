# V48 Source-Hit Acceptance Decision Tree

Status: template/navigation only. This decision tree is for future source hits
found from V48 search packets. It does not run searches, add source records,
assert convergence, flag contradiction, or change grounded findings.

- decision nodes: `10`
- safe outcomes: `6`
- required linked controls: `6`

## Required Inputs

Use this decision tree only after opening the package manifest:

- `knowledge_external/templates/SOURCE_INTAKE_PACKAGE_MANIFEST_V48.md`

Then keep these controls open while classifying the hit:

- `knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md`
- `knowledge_external/templates/SOURCE_INTAKE_OPERATOR_QUICKSTART_V48.md`
- `knowledge_external/synthesis/HIGH_PRIORITY_EXTERNAL_SOURCING_PLAN_V48.md`
- `knowledge_external/synthesis/CONTRADICTION_READINESS_PLAYBOOK_V48.md`
- `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md`

## Decision Tree

| order | decision | if yes | if no |
|---:|---|---|---|
| 1 | Is there a stable source locator: URL, DOI, accession, or repository ID? | Continue to 2. | Outcome A: reject for intake until locator exists. |
| 2 | Is the source reachable or otherwise inspectable without violating access terms? | Continue to 3. | Outcome B: park in access/terms review. |
| 3 | Are source terms/reuse constraints known enough to store a short summary? | Continue to 4. | Outcome B: park in access/terms review. |
| 4 | Does the source match a high-priority sourcing-plan row? | Continue to 5. | Outcome C: insufficient-overlap note; do not create a relationship row. |
| 5 | Does it match the same definition, population, layer, direction, and outcome required by that row? | Continue to 6. | Outcome C: insufficient-overlap note; do not create a relationship row. |
| 6 | Is the source merely generic adjacent MS context? | Outcome C: insufficient-overlap note; do not create a relationship row. | Continue to 7. |
| 7 | Does the source independently agree with a grounded project finding under the same definition? | Outcome D: prepare a candidate convergence row for review. | Continue to 8. |
| 8 | Does the source disagree with a grounded project finding under the same definition? | Outcome E: prepare a candidate contradiction row and route to the contradiction readiness playbook. | Continue to 9. |
| 9 | Does the source provide reachable data or a testable claim that can be regrounded later? | Outcome F: add a future-grounding route; do not conclude the claim now. | Continue to 10. |
| 10 | Is the source useful only as external context without a same-definition relationship? | Outcome C: insufficient-overlap/context note. | Outcome A: reject for intake. |

## Safe Outcomes

| outcome | action | boundary |
|---|---|---|
| A | Reject for intake and continue searching. | no external record added |
| B | Park in source-terms or access review. | no source summary stored until terms are clear |
| C | Record insufficient-overlap/context note only if useful. | no convergence or contradiction asserted |
| D | Prepare a candidate convergence row with provenance for later review. | candidate only; project artifact remains evidence |
| E | Prepare a candidate contradiction row and route to the readiness playbook. | tension flag only; no external override |
| F | Queue a future-grounding route. | queued task only; not a finding |

## Verification Before Commit

```bash
python3 scripts/v47_external_record_schema_linter.py lint --fail-on-error
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit --fail-on-error
python3 scripts/v48_governance_preflight.py
```

## Boundary

- This decision tree classifies source-hit handling, not scientific truth.
- It does not promote any external source to evidence.
- It does not allow external context to override grounded project artifacts.
- It does not change locked rules, validation plans, or scored findings.
