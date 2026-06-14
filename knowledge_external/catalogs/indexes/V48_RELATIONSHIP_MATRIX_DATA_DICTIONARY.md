# V48 Relationship-Matrix Data Dictionary

Status: navigation/schema only. This data dictionary explains fields in the V48 convergence/contradiction matrix; it does not add external records, assert convergence, or change grounded findings.

- matrix fields: `15`
- missing definitions: `0`

## Fields

| order | field | class | definition | allowed values |
|---:|---|---|---|---|
| 1 | `grounded_finding_id` | `grounded_project_finding` | Project finding label used for relationship classification. |  |
| 2 | `grounded_category` | `grounded_project_finding` | V37-style finding category such as positive, negative/decoupling, kill/closed, or methodological. |  |
| 3 | `grounded_evidence_grade` | `grounded_project_finding` | Evidence grade assigned by the grounded project report. |  |
| 4 | `grounded_artifact` | `grounded_project_finding` | Project artifact path that remains the evidence source. |  |
| 5 | `external_record_id` | `external_record` | Segregated external record identifier. |  |
| 6 | `external_record_type` | `external_record` | External record subtype used for navigation and source-domain accounting. |  |
| 7 | `external_record_path` | `external_record` | Path to the segregated external record. |  |
| 8 | `epistemic_class` | `external_record` | External epistemic class; not a project-grounded finding. | external-verifiable;external-unverifiable |
| 9 | `external_source` | `external_record` | External source locator used for provenance. |  |
| 10 | `not_project_grounded_marker` | `external_record` | Explicit marker preserving the external/grounded boundary. | NOT_PROJECT_GROUNDED |
| 11 | `relationship_class` | `relationship_classification` | Controlled relationship label between the grounded finding and external record. | contradicts;converges;insufficient-overlap |
| 12 | `synthesis_status` | `relationship_classification` | Controlled operational status derived from the relationship class. | CORROBORATION_FROM_INDEPENDENT_SOURCE;GENERAL_CONTEXT_NOT_LOCUS_CORROBORATION;NO_DIRECT_EXTERNAL_CORROBORATION;RESOURCE_CAN_QUEUE_FUTURE_CHECK |
| 13 | `interpretation` | `relationship_classification` | Short boundary-safe interpretation; external context never overrides grounded artifacts. |  |
| 14 | `future_grounding_action` | `future_work` | Queued action if further grounding or refresh is warranted. |  |
| 15 | `row_status` | `quality_control` | Row-level generation/check status. |  |

## Boundary

- Field definitions are schema/navigation metadata, not project evidence.
- `grounded_artifact` points to the evidence source; external fields remain provenance/context fields.
- Controlled values are enforced by the V48 relationship/status vocabulary linter.
