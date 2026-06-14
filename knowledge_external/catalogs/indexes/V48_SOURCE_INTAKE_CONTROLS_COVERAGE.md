# V48 Source-Intake Controls Coverage

Status: governance/navigation only. This card summarizes how V48 source-intake
controls guard against common external-knowledge failure modes. It does not add
external records, assert relationships, evaluate scientific truth, or change
grounded findings.

- safeguards: `13`
- failure modes covered: `11`
- required linked controls: `13`

## Coverage Table

| safeguard | primary failure mode prevented | control artifact | boundary |
|---|---|---|---|
| Epistemic class definitions | external material confused with grounded evidence | `docs/knowledge/EPISTEMIC_CLASSES.md` | class definitions only |
| Reader brief | public reader over-trusts external layer | `knowledge_external/EXTERNAL_LAYER_READER_BRIEF_V48.md` | reader/navigation only |
| Source intake package manifest | operator skips required intake order | `knowledge_external/templates/SOURCE_INTAKE_PACKAGE_MANIFEST_V48.md` | future-search routing only |
| One-page intake checklist | operator loses the end-to-end source-hit sequence | `knowledge_external/templates/EXTERNAL_INTAKE_ONE_PAGE_CHECKLIST_V48.md` | routing only |
| Source-hit acceptance decision tree | source hit is promoted before same-definition review | `knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md` | routing only |
| Access/terms parking queue | blocked or restricted source is summarized too early | `knowledge_external/templates/SOURCE_HIT_ACCESS_TERMS_PARKING_QUEUE_V48.md` | parking only |
| De-duplication checklist | same source is overcounted as independent corroboration | `knowledge_external/templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md` | independence routing only |
| Parked-source release checklist | parked source leaves quarantine without release checks | `knowledge_external/templates/PARKED_SOURCE_RELEASE_CHECKLIST_V48.md` | release routing only |
| Future-grounding handoff | testable external claim is treated as supported before rerun | `knowledge_external/templates/PARKED_SOURCE_FUTURE_GROUNDING_HANDOFF_V48.md` | queued work only |
| Relationship-row candidate template | candidate convergence/contradiction becomes matrix row too early | `knowledge_external/templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md` | candidate only |
| Contradiction triage mini-template | external disagreement overrides a grounded result | `knowledge_external/templates/CONTRADICTION_TRIAGE_MINI_TEMPLATE_V48.md` | tension flag only |
| Audit log template | operator decision is not reproducible | `knowledge_external/templates/SOURCE_INTAKE_AUDIT_LOG_TEMPLATE_V48.md` | audit trail only |
| Decision error taxonomy | process error is hidden or misclassified | `knowledge_external/templates/SOURCE_INTAKE_DECISION_ERROR_TAXONOMY_V48.md` | QA classification only |

## Failure Modes Covered

| failure mode | covered by |
|---|---|
| `external_as_grounded` | epistemic classes, reader brief, provenance gate |
| `source_terms_bypass` | access/terms parking queue, parked-source release checklist |
| `copied_claim_leakage` | parking queue, audit log template, provenance gate |
| `same_source_overcount` | de-duplication checklist, source-independence matrix |
| `review_as_primary` | de-duplication checklist, source-hit acceptance decision tree |
| `same_definition_failure` | source-hit acceptance decision tree, relationship-row candidate template |
| `candidate_promoted_too_early` | relationship-row candidate template, future-grounding handoff |
| `external_override_attempt` | contradiction triage mini-template, reader brief |
| `model_output_as_evidence` | model-lens boundary, decision error taxonomy |
| `missing_audit_trail` | audit log template, reproducibility checklist |
| `unreproducible_operator_decision` | reproducibility checklist, decision error taxonomy |

## Verification Commands

```bash
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit
python3 scripts/v48_governance_preflight.py
```

## Boundary

This card is a navigation summary over existing controls. It is not evidence
that any external source is correct and does not change any grounded finding,
locked rule, validation plan, or evidence grade.
