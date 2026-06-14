# V48 Source-Intake Reviewer Handoff Checklist

Status: template/navigation only. This checklist is for handing future
external-source intake work from one session or operator to the next. It
preserves state, blockers, and required gates; it does not add external records,
assert relationships, or change grounded findings.

- handoff fields: `12`
- handoff statuses: `5`
- required linked controls: `8`

## Required Controls

Use this checklist only with:

- `meta/V48_QUEUE.md`
- `knowledge_external/templates/SOURCE_INTAKE_AUDIT_LOG_TEMPLATE_V48.md`
- `knowledge_external/templates/SOURCE_INTAKE_STOP_GO_SCORECARD_V48.md`
- `knowledge_external/templates/SOURCE_INTAKE_REPRODUCIBILITY_CHECKLIST_V48.md`
- `knowledge_external/templates/SOURCE_INTAKE_DECISION_ERROR_TAXONOMY_V48.md`
- `knowledge_external/catalogs/indexes/V48_SOURCE_INTAKE_CONTROLS_COVERAGE.md`
- `knowledge_external/catalogs/indexes/V48_PREFLIGHT_SUMMARY_CARD.md`
- `knowledge_external/catalogs/indexes/V48_GOVERNANCE_NAVIGATION.md`

## Handoff Fields

| order | field | required content |
|---:|---|---|
| 1 | `handoff_id` | Stable local handoff ID. |
| 2 | `date_utc` | UTC handoff timestamp. |
| 3 | `operator_from` | Session or operator handing off. |
| 4 | `operator_to` | Intended next reviewer, if known. |
| 5 | `active_source_locator` | Source locator or `none`. |
| 6 | `active_artifact` | Template, queue, audit log, or generated control under review. |
| 7 | `handoff_status` | One of the statuses below. |
| 8 | `last_completed_gate` | Last verification command that passed. |
| 9 | `open_blocker` | Data/access/terms/tool blocker or `none`. |
| 10 | `next_required_action` | Concrete next command or edit. |
| 11 | `do_not_do` | Specific unsafe shortcut to avoid. |
| 12 | `boundary_statement` | Why the handoff is not evidence or a finding. |

## Handoff Statuses

| status | meaning | next action |
|---|---|---|
| `clean_resume` | Work can continue from the named next action. | Continue with listed task. |
| `needs_gate_rerun` | Artifact exists but a required linter/preflight needs rerun. | Run gate before edits. |
| `blocked_external` | External access, terms, data, or human input is needed. | Park and switch fronts. |
| `quarantine_review` | Possible evidence leakage or boundary issue exists. | Do not proceed until gate passes. |
| `complete_checkpoint` | Task is committed and no immediate action remains. | Pick next queue item. |

## Minimum Handoff Entry

```yaml
handoff_id:
date_utc:
operator_from:
operator_to:
active_source_locator:
active_artifact:
handoff_status:
last_completed_gate:
open_blocker:
next_required_action:
do_not_do:
boundary_statement:
```

## Forbidden Shortcuts

- Do not hand off uncommitted source-intake work without naming the active
  artifact and next action.
- Do not treat handoff status as evidence or source validation.
- Do not omit a known blocker.
- Do not continue from a quarantined handoff without rerunning the provenance
  gate.
- Do not let a handoff note change grounded findings, locked rules, validation
  plans, or evidence grades.

## Verification Before Commit

```bash
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit
python3 scripts/v48_governance_preflight.py
```

## Boundary

This checklist preserves operational continuity only. It is not a source
record, not a relationship row, not evidence, and not a scientific conclusion.
