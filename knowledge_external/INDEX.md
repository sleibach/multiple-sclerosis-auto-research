# External MS Knowledge Index

Status: external knowledge navigation only. External records are `NOT_PROJECT_GROUNDED` and are not project evidence.

Grounded project findings remain in the normal project report/history/validation trees. This index points only to the segregated external tree.

## Counts

- external records indexed: `37`
- missing sources: `0`
- missing not-grounded markers: `0`
- source domains represented: `26`
- reachability maintenance warnings: `2`
- convergence rows linked to grounded findings: `unknown`

## Epistemic-Class Counts

| field | value | count |
|---|---|---:|
| `epistemic_class` | `external-unverifiable` | 37 |
| `relationship_to_project_findings` | `orthogonal` | 37 |
| `record_type` | `external_claim` | 6 |
| `record_type` | `external_resource_catalog` | 31 |

## Navigation

| artifact | purpose | boundary |
|---|---|---|
| [Class-aware external record index](catalogs/indexes/EXTERNAL_KNOWLEDGE_INDEX.md) | Browse every external record with source and class markers. | external only |
| [Resource category rollup](catalogs/indexes/EXTERNAL_RESOURCE_CATEGORY_ROLLUP.md) | Browse resource metadata by category. | external resource metadata only |
| [Access-tier rollup](catalogs/indexes/EXTERNAL_RESOURCE_ACCESS_TIER_ROLLUP.md) | Browse public/registration/application/controlled access tiers. | access metadata only |
| [Source-domain rollup](catalogs/indexes/EXTERNAL_SOURCE_DOMAIN_ROLLUP.md) | Browse records by source domain. | source locator metadata only |
| [Source URL reachability](catalogs/indexes/EXTERNAL_SOURCE_URL_REACHABILITY.md) | Transport-status maintenance report. | HTTP status is not claim validation |
| [Convergence/contradiction skeleton](synthesis/CONVERGENCE_CONTRADICTION_SKELETON.md) | Placeholder rows until a grounded-link review is performed. | no convergence claim unless linked and grounded |
| [Intake templates](templates/README.md) | Templates for future external-verifiable claim intake. | queued claims are not findings |

## Current Guardrails

- External claims never alter grounded findings, locked rules, or pre-registrations.
- External-verifiable records require a future grounding route before they can be considered.
- External-unverifiable records remain context only.
- Model/RPT outputs are external-unverifiable proposals unless separately grounded.
