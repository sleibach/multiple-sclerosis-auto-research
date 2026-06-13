# V47 External-Verifiable Intake

Status: queueing infrastructure only.

External-verifiable records are external claims the project could test later on
held or reachable data. Until that grounding happens, they are not project
findings and not evidence.

Use `knowledge_external/templates/external_verifiable_claim_template.json.template`
when creating a future live claim record. The live record must include:

- `epistemic_class: external-verifiable`
- a source locator
- `date_accessed`
- `relationship_to_project_findings`
- `not_project_grounded_marker: NOT_PROJECT_GROUNDED`
- `future_grounding_route`
- `grounding_data_needed`
- `grounding_status`

Verification:

```bash
.venv/bin/python scripts/v47_external_verifiable_intake_linter.py synthetic-check --fail-on-error
.venv/bin/python scripts/v47_external_verifiable_intake_linter.py lint --fail-on-error
```

