# V48 Source Intake Package Manifest

Status: template/navigation only. This manifest ties the V48 source-search and
intake artifacts into one operator package. It does not run searches, add
external records, assert convergence, flag contradiction, or change grounded
findings.

- package components: `6`
- required verification commands: `4`
- mandatory operator order steps: `6`

## Package Components

| order | artifact | purpose | boundary |
|---:|---|---|---|
| 1 | `knowledge_external/EXTERNAL_LAYER_READER_BRIEF_V48.md` | Read the public boundary before handling external material. | reader/navigation only |
| 2 | `knowledge_external/synthesis/HIGH_PRIORITY_EXTERNAL_SOURCING_PLAN_V48.md` | Identify the high-priority finding gap and required source type. | future intake/navigation only |
| 3 | `knowledge_external/synthesis/HIGH_PRIORITY_SOURCE_SEARCH_QUERIES_V48.md` | Choose the prewritten query route for the gap. | query packet only; no searches run here |
| 4 | `knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md` | Apply the per-item acceptance criteria and forbidden-shortcut checks. | checklist/navigation only |
| 5 | `knowledge_external/templates/SOURCE_INTAKE_OPERATOR_QUICKSTART_V48.md` | Follow the mechanical source-hit handling order. | operator/navigation only |
| 6 | `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md` | Queue exact future grounding routes when a source hit can be tested later. | queued tasks are not findings |

## Mandatory Operator Order

1. Read the external-layer reader brief before using the search packet.
2. Select a high-priority sourcing-plan row and its accepted source type.
3. Run or prepare only the matching query route from the source-search packet.
4. Apply the high-priority checklist before any source record is created.
5. Use the operator quickstart to assign safe handling: insufficient overlap,
   source-terms review, candidate relationship row, or future grounding route.
6. Run the verification commands before committing any source-intake artifact.

## Verification Commands

```bash
python3 scripts/v47_external_record_schema_linter.py lint --fail-on-error
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit --fail-on-error
python3 scripts/v48_governance_preflight.py
```

## What This Package Does Not Do

- It does not make any external source a project finding.
- It does not decide whether a grounded finding is true.
- It does not create convergence or contradiction by itself.
- It does not permit generic adjacent context to satisfy same-definition
  source requirements.
- It does not change locked rules, validation plans, or evidence grades.

## Boundary

This manifest is a routing layer over existing V48 source-intake controls. The
grounded project artifact remains the evidence unless a future project analysis
regrounds a specific external-verifiable proposal on project data. Source:
`docs/knowledge/EPISTEMIC_CLASSES.md`.
