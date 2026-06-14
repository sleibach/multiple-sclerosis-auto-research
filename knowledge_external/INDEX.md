# External MS Knowledge Index

Status: external knowledge navigation only. External records are `NOT_PROJECT_GROUNDED` and are not project evidence.

Grounded project findings remain in the normal project report/history/validation trees. This index points only to the segregated external tree.

## Counts

- external records indexed: `39`
- missing sources: `0`
- missing not-grounded markers: `0`
- source domains represented: `27`
- records with source_terms metadata: `8`
- records missing optional source_terms metadata: `31`
- V48 governance controls tracked: `17`
- reachability maintenance warnings: `2`
- V48 convergence rows asserted: `2`
- V48 contradiction rows flagged: `0`
- placeholder skeleton linked rows: `unknown`

## Epistemic-Class Counts

| field | value | count |
|---|---|---:|
| `epistemic_class` | `external-unverifiable` | 39 |
| `relationship_to_project_findings` | `orthogonal` | 37 |
| `relationship_to_project_findings` | `supports` | 2 |
| `record_type` | `external_claim` | 8 |
| `record_type` | `external_resource_catalog` | 31 |

## Navigation

| artifact | purpose | boundary |
|---|---|---|
| [Class-aware external record index](catalogs/indexes/EXTERNAL_KNOWLEDGE_INDEX.md) | Browse every external record with source and class markers. | external only |
| [Resource category rollup](catalogs/indexes/EXTERNAL_RESOURCE_CATEGORY_ROLLUP.md) | Browse resource metadata by category. | external resource metadata only |
| [V48 external resource comparator matrix](catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md) | Compare external resources by coverage, access tier, unique gap, and this repo's distinct role. | external resource metadata only |
| [Access-tier rollup](catalogs/indexes/EXTERNAL_RESOURCE_ACCESS_TIER_ROLLUP.md) | Browse public/registration/application/controlled access tiers. | access metadata only |
| [Source-domain rollup](catalogs/indexes/EXTERNAL_SOURCE_DOMAIN_ROLLUP.md) | Browse records by source domain. | source locator metadata only |
| [V48 source-domain review](catalogs/indexes/SOURCE_DOMAIN_REVIEW_V48.md) | Classify source domains for maintenance, access, and terms review. | domain maintenance only |
| [V48 source-terms coverage](catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md) | Browse external records by source-terms metadata coverage and conservative reuse notes. | source terms metadata only |
| [V48 governance navigation](catalogs/indexes/V48_GOVERNANCE_NAVIGATION.md) | Browse V48 external-knowledge controls and latest pass/fail summaries. | governance/navigation only |
| [V48 external-governance handoff](catalogs/indexes/V48_EXTERNAL_GOVERNANCE_HANDOFF.md) | Compact command handoff and boundary rules for future external-knowledge sessions. | governance/navigation only |
| [Source URL reachability](catalogs/indexes/EXTERNAL_SOURCE_URL_REACHABILITY.md) | Transport-status maintenance report. | HTTP status is not claim validation |
| [V48 convergence/contradiction analysis](synthesis/CONVERGENCE_CONTRADICTION_V48.md) | Populated comparison of selected grounded findings and segregated external records. | external agreement is context; project artifacts remain evidence |
| [V48 future-grounding queue](synthesis/FUTURE_GROUNDING_QUEUE_V48.md) | Concrete follow-up tasks from V48 convergence/insufficient-overlap rows. | queued tasks are not findings |
| [Convergence/contradiction skeleton](synthesis/CONVERGENCE_CONTRADICTION_SKELETON.md) | Placeholder rows until a grounded-link review is performed. | no convergence claim unless linked and grounded |
| [Intake templates](templates/README.md) | Templates for future external-verifiable claim intake. | queued claims are not findings |

## Current Guardrails

- External claims never alter grounded findings, locked rules, or pre-registrations.
- External-verifiable records require a future grounding route before they can be considered.
- External-unverifiable records remain context only.
- Model/RPT outputs are external-unverifiable proposals unless separately grounded.
