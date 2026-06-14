# V48 External Intake One-Page Checklist

Status: template/navigation only. This one-page checklist is the operator-facing
entry point for future external-source intake. It routes source hits through the
V47/V48 controls without adding claims, asserting convergence, flagging
contradictions, or changing grounded findings.

- operator steps: `10`
- stop conditions: `6`
- required linked controls: `10`

## Required Controls

Keep these controls open while processing any source hit:

- `docs/knowledge/EPISTEMIC_CLASSES.md`
- `knowledge_external/EXTERNAL_LAYER_READER_BRIEF_V48.md`
- `knowledge_external/templates/SOURCE_INTAKE_PACKAGE_MANIFEST_V48.md`
- `knowledge_external/templates/SOURCE_INTAKE_OPERATOR_QUICKSTART_V48.md`
- `knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md`
- `knowledge_external/templates/SOURCE_HIT_ACCESS_TERMS_PARKING_QUEUE_V48.md`
- `knowledge_external/templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md`
- `knowledge_external/templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md`
- `knowledge_external/templates/CONTRADICTION_TRIAGE_MINI_TEMPLATE_V48.md`
- `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md`

## Operator Steps

| order | action | pass condition |
|---:|---|---|
| 1 | Confirm the source hit has a stable locator. | DOI, URL, accession, repository ID, or complete citation exists. |
| 2 | Confirm access and reuse terms are safe enough to inspect. | Terms route is known; otherwise park. |
| 3 | Run de-duplication before any relationship assessment. | Source cluster and independence note are assigned. |
| 4 | Match the hit to a specific V48 sourcing gap or project finding. | Same definition can be evaluated. |
| 5 | Apply the source-hit acceptance decision tree. | Safe outcome A-F is assigned. |
| 6 | If blocked, park in access/terms review. | No source claims are copied. |
| 7 | If adjacent only, record insufficient overlap or skip. | No relationship row is created. |
| 8 | If same-definition agreement appears plausible, draft a candidate convergence row. | Candidate only; grounded artifact remains evidence. |
| 9 | If same-definition disagreement appears plausible, run contradiction triage first. | Tension flag only; no external override. |
| 10 | If the claim is testable later, add a future-grounding route. | Queued task only; not a finding. |

## Stop Conditions

| condition | required handling |
|---|---|
| Locator missing or unstable. | Reject or park; do not summarize. |
| Access blocked or terms unclear. | Use the access/terms parking queue. |
| Duplicate or same-source material. | Canonicalize; do not count as independent. |
| Same-definition overlap fails. | Record insufficient overlap only if useful. |
| Independence unclear. | Park for source-independence review. |
| External source would require changing a grounded finding or locked rule. | Do not change it; route as tension/future grounding only. |

## Final Verification

Before committing any source-intake artifact, run:

```bash
python3 scripts/v47_external_record_schema_linter.py lint --fail-on-error
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit
python3 scripts/v48_governance_preflight.py
```

## Boundary

This checklist is a routing document. External source hits remain external,
non-evidence material unless a future project run regrounds a specific proposal
on project data. The grounded project artifact remains the evidence; external
agreement can only be recorded as corroboration from an independent source, and
external disagreement can only be recorded as a tension flag.
