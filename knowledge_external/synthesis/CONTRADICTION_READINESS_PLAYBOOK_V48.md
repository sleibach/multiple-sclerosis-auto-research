# V48 Contradiction Readiness Playbook

Status: governance/navigation only. This playbook defines what to do if future external context conflicts with a grounded project finding.

- current matrix rows: `12`
- current contradictions: `0`
- playbook steps: `4`

## Current State

- No contradictions are currently flagged in the V48 matrix.

## Playbook

| stage | trigger | required artifact | safe action | forbidden action |
|---|---|---|---|---|
| `intake` | external source appears to disagree with a grounded project finding | `knowledge_external/templates/contradiction_intake_template.json.template` | create a segregated external-verifiable intake record with source, class, project-finding reference, relationship note, and future grounding route | do not edit the grounded finding, locked rule, or validation pre-registration |
| `triage` | intake record exists | `scripts/v48_contradiction_intake_linter.py` | classify likely explanation: population, phenotype definition, modality, directionality, date/version, or true discrepancy | do not resolve by deferring to the external source |
| `future_grounding` | concrete project data or reachable public data can test the tension | `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md` | queue the exact test and required data; keep the contradiction as a flag until grounded | do not report model or literature agreement as evidence |
| `grounded_resolution` | a future rerunnable project analysis tests the contradiction | `normal grounded project artifact outside knowledge_external` | update the grounded project state only through rerunnable analysis with evidence grade and artifact reference | do not let an external record directly change project scores or conclusions |

## Boundary

- External disagreement raises a flag; it does not override a rerunnable project finding.
- Any resolution must be produced by a future grounded analysis artifact.
- Locked rules and validation pre-registrations are unchanged by this playbook.
