# V48 Source-Intake Decision Error Taxonomy

Status: template/navigation only. This taxonomy classifies future operator
errors in external-source intake so they can be corrected without weakening the
V47/V48 provenance boundary. It does not add external records, judge scientific
truth, assert relationships, or change grounded findings.

- error classes: `10`
- severity levels: `4`
- required linked controls: `7`

## Required Controls

Use this taxonomy only with:

- `knowledge_external/templates/EXTERNAL_INTAKE_ONE_PAGE_CHECKLIST_V48.md`
- `knowledge_external/templates/SOURCE_INTAKE_AUDIT_LOG_TEMPLATE_V48.md`
- `knowledge_external/templates/SOURCE_HIT_ACCESS_TERMS_PARKING_QUEUE_V48.md`
- `knowledge_external/templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md`
- `knowledge_external/templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md`
- `knowledge_external/templates/CONTRADICTION_TRIAGE_MINI_TEMPLATE_V48.md`
- `scripts/v47_provenance_gate.py`

## Error Classes

| error_class | description | correction route |
|---|---|---|
| `missing_locator` | Source hit was handled without a stable locator. | reject or park until locator exists |
| `terms_bypass` | Source was summarized or routed before access/reuse terms were clear. | park and remove copied content |
| `copied_claim_leakage` | External source claim, excerpt, table, or abstract text entered a routing artifact. | remove content and rerun provenance gates |
| `same_source_overcount` | Publisher, repository, supplement, database, or review pages were counted as independent. | canonicalize to one source cluster |
| `review_as_primary` | Review/opinion/database restatement was treated as primary evidence. | downgrade to context or locate primary source |
| `same_definition_failure` | Source was treated as convergence/contradiction despite mismatched population, layer, outcome, direction, or scope. | reclassify as insufficient overlap |
| `candidate_promoted_too_early` | Candidate row or future-grounding task was treated as a finding before project grounding. | demote to candidate/queue |
| `external_override_attempt` | External source was used to alter or overrule a grounded finding, locked rule, or validation plan. | revert and record contradiction/tension only |
| `model_output_as_evidence` | Model/RPT output was treated as evidence or source authority. | remove and reroute as proposal-only |
| `audit_trail_missing` | Routing decision lacks required audit fields or boundary statement. | add audit entry before commit |

## Severity Levels

| severity | meaning | required action |
|---|---|---|
| `low` | Documentation drift that does not affect source classification. | correct artifact and rerun linter |
| `medium` | Intake route unclear but no evidence leakage occurred. | park or re-review before use |
| `high` | Source independence, relationship candidate, or future-grounding route may be wrong. | quarantine affected row and rerun controls |
| `critical` | External material was treated as evidence or changed grounded/locked artifacts. | revert immediately; run full provenance/preflight audit |

## Minimum QA Record

Record these fields when logging a decision error:

1. Audit ID or source locator.
2. Error class.
3. Severity level.
4. Affected artifact path.
5. Correction route.
6. Whether any external claim text must be removed.
7. Verification commands rerun.
8. Statement that the correction does not alter grounded findings.

## Forbidden Shortcuts

- Do not fix an error by reclassifying external material as grounded.
- Do not hide an error by deleting the audit trail.
- Do not let model/RPT output decide severity.
- Do not keep copied external claims in any routing artifact.
- Do not reinterpret a critical error as convergence or contradiction.

## Verification Before Commit

```bash
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit
python3 scripts/v48_governance_preflight.py
```

## Boundary

This taxonomy classifies intake-process errors only. It is not a scientific
finding and does not establish whether any external source is correct. Its job
is to protect provenance, source independence, and the grounded/external
boundary.
