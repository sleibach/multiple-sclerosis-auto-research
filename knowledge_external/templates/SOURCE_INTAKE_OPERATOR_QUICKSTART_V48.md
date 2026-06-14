# V48 Source Intake Operator Quickstart

Status: template/navigation only. This quickstart tells future operators how to
handle a source found from the high-priority search packet. It does not add
external records, assert convergence, or change grounded findings.

## Scope

Use this quickstart after a future session runs a search from:

- `knowledge_external/synthesis/HIGH_PRIORITY_SOURCE_SEARCH_QUERIES_V48.md`
- `knowledge_external/synthesis/HIGH_PRIORITY_EXTERNAL_SOURCING_PLAN_V48.md`

Do not use this quickstart to decide whether a project finding is true. It only
decides whether a source hit is safe to intake into the segregated external
layer.

## Mechanical Intake Order

1. Identify the source hit and record its stable locator: URL, DOI, accession,
   or repository identifier.
2. Check source terms and reuse constraints before copying or summarizing any
   content.
3. Record the date accessed and, where practical, a source snapshot or source
   hash.
4. Assign the source to an epistemic class using `docs/knowledge/EPISTEMIC_CLASSES.md`. If it can be tested later on reachable data, it is future-groundable context; if it cannot currently be regrounded, it remains context only. Source: `docs/knowledge/EPISTEMIC_CLASSES.md`.
5. Preserve the not-project-grounded marker required by the external record
   schema. Source: `docs/knowledge/EPISTEMIC_CLASSES.md`.
6. Review whether the source addresses the same definition, population, layer,
   disease comparator, direction, and outcome as the project finding.
7. Apply the source-plan forbidden shortcut. Generic adjacent context cannot
   satisfy a source-specific acceptance criterion.
8. If overlap is specific enough, prepare a candidate relationship row for the
   convergence/contradiction matrix. Do not call it convergence until the row is
   reviewed and classed.
9. If the source is future-groundable, add the exact future grounding route to
   the future-grounding queue.

## Required Checklist

The authoritative per-item checklist is:

- `knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md`

A source hit is not ready for relationship-matrix review until every checklist
step for the relevant source-plan item is complete.

## Safe Classification Table

| situation | safe action | forbidden action |
|---|---|---|
| Source is a generic MS review but the plan requires a same-locus or same-layer source. | Mark insufficient overlap and keep searching. | Treat broad background as corroboration. |
| Source provides a relevant dataset but no direct conclusion. | Queue a future grounding route. | Report the dataset as evidence before running the project analysis. |
| Source is specific and independently agrees with a grounded project finding. | Prepare a candidate convergence row with source, class, and overlap notes. | Claim the external source confirms the project finding. |
| Source conflicts with a grounded project finding. | Prepare a candidate contradiction row and route to the contradiction readiness playbook. | Override the grounded project result with the external source. |
| Source terms are unclear. | Park the hit in the source-terms review queue. | Store copied source content or long excerpts. |

## Minimum Record Fields

Before a source hit becomes a segregated external record, the record needs:

- `record_id`
- `claim`
- `epistemic_class`
- `source`
- `date_accessed`
- `relationship_to_project_findings`
- `not_project_grounded_marker`
- `why_unverifiable` or `future_grounding_route`, depending on class

Use the templates in:

- `knowledge_external/templates/README.md`

## Verification Before Commit

Run:

```bash
python3 scripts/v47_external_record_schema_linter.py lint --fail-on-error
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit --fail-on-error
python3 scripts/v48_governance_preflight.py
```

## Boundary

- This is an operator quickstart, not a source record.
- It adds no external knowledge.
- It does not classify any specific source hit.
- It does not change grounded findings, locked rules, validation plans, or
  source-acceptance criteria.
