# External MS Knowledge Index

Status: external knowledge navigation only. External records are `NOT_PROJECT_GROUNDED` and are not project evidence.

Grounded project findings remain in the normal project report/history/validation trees. This index points only to the segregated external tree.

## Counts

- external records indexed: `2`
- missing sources: `0`
- missing not-grounded markers: `0`
- source domains represented: `2`
- reachability maintenance warnings: `1`
- V48 convergence rows asserted: `1`
- V48 contradiction rows flagged: `0`
- placeholder skeleton linked rows: `0`

## Epistemic-Class Counts

| field | value | count |
|---|---|---:|
| `epistemic_class` | `external-unverifiable` | 2 |

## Navigation

| artifact | purpose | boundary |
|---|---|---|
| [Class-aware external record index](catalogs/indexes/EXTERNAL_KNOWLEDGE_INDEX.md) | Browse every external record with source and class markers. | external only |
| [Resource category rollup](catalogs/indexes/EXTERNAL_RESOURCE_CATEGORY_ROLLUP.md) | Browse resource metadata by category. | external resource metadata only |
| [V48 external resource comparator matrix](catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md) | Compare external resources by coverage, access tier, unique gap, and this repo's distinct role. | external resource metadata only |
| [Access-tier rollup](catalogs/indexes/EXTERNAL_RESOURCE_ACCESS_TIER_ROLLUP.md) | Browse public/registration/application/controlled access tiers. | access metadata only |
| [Source-domain rollup](catalogs/indexes/EXTERNAL_SOURCE_DOMAIN_ROLLUP.md) | Browse records by source domain. | source locator metadata only |
| [Source URL reachability](catalogs/indexes/EXTERNAL_SOURCE_URL_REACHABILITY.md) | Transport-status maintenance report. | HTTP status is not claim validation |
| [V48 convergence/contradiction analysis](synthesis/CONVERGENCE_CONTRADICTION_V48.md) | Populated comparison of selected grounded findings and segregated external records. | external agreement is context; project artifacts remain evidence |
| [Convergence/contradiction skeleton](synthesis/CONVERGENCE_CONTRADICTION_SKELETON.md) | Placeholder rows until a grounded-link review is performed. | no convergence claim unless linked and grounded |
| [Intake templates](templates/README.md) | Templates for future external-verifiable claim intake. | queued claims are not findings |

## Current Guardrails

- External claims never alter grounded findings, locked rules, or pre-registrations.
- External-verifiable records require a future grounding route before they can be considered.
- External-unverifiable records remain context only.
- Model/RPT outputs are external-unverifiable proposals unless separately grounded.
