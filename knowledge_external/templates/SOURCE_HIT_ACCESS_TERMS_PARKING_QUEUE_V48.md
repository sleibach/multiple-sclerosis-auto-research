# V48 Source-Hit Access/Terms Parking Queue Template

Status: template/navigation only. This template is for future source hits that
look promising but cannot be safely integrated because access, licensing, reuse
terms, or stable locator details are not yet clear. It does not store source
content, add external records, assert convergence, flag contradiction, or change
grounded findings.

- required fields: `12`
- parking statuses: `5`
- release conditions: `6`
- required linked controls: `6`

## Required Controls

Use this template only with:

- `knowledge_external/templates/SOURCE_INTAKE_PACKAGE_MANIFEST_V48.md`
- `knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md`
- `knowledge_external/catalogs/indexes/SOURCE_TERMS_REVIEW_QUEUE_V48.md`
- `knowledge_external/catalogs/indexes/HIGH_PRIORITY_SOURCE_TERMS_PACKET_V48.md`
- `knowledge_external/templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md`
- `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md`

## Required Fields

| order | field | allowed content | boundary |
|---:|---|---|---|
| 1 | `parking_id` | Stable local ID for the parked hit. | identifier only |
| 2 | `date_parked` | ISO date. | provenance only |
| 3 | `operator` | Person or agent that parked the hit. | provenance only |
| 4 | `source_locator` | DOI, URL, accession, repository ID, or citation pointer. | locator only |
| 5 | `locator_stability` | stable / unstable / unknown. | access triage only |
| 6 | `candidate_project_gap` | V48 sourcing-plan row or project gap it may address. | gap routing only |
| 7 | `parking_status` | One of the statuses below. | no relationship asserted |
| 8 | `access_blocker` | Short blocker statement. | no source content copied |
| 9 | `terms_blocker` | Terms/reuse uncertainty, if any. | no source content copied |
| 10 | `minimum_safe_summary` | One-line locator-level summary without copied claims. | not evidence |
| 11 | `release_condition` | Exact condition that must be met before intake. | future action only |
| 12 | `next_owner_action` | Concrete next access/terms step. | task routing only |

## Parking Statuses

| status | use when | allowed action |
|---|---|---|
| `terms_unknown` | Source can be located but reuse or citation terms are unclear. | Park; do not summarize claims. |
| `access_blocked` | Source requires login, request, paywall, author response, or controlled repository access. | Park with access step. |
| `controlled_access` | Source points to controlled data or a formal data-access process. | Park; record access route only. |
| `locator_unstable` | Source locator is incomplete, transient, or not reproducible. | Park until stable locator exists. |
| `reuse_restricted` | Terms allow reading but not storing derivative summaries in this repo. | Park; store locator and restriction only. |

## Release Conditions

| order | condition | required evidence before release |
|---:|---|---|
| 1 | Stable locator confirmed. | DOI, accession, persistent URL, or complete citation. |
| 2 | Access route documented. | Public route, request route, or controlled-access route recorded. |
| 3 | Reuse terms reviewed. | Source terms metadata can be written without guesswork. |
| 4 | Safe summary allowed. | Terms permit storing a short provenance-bearing summary. |
| 5 | Same-definition relevance checked. | Source-hit acceptance decision tree completed. |
| 6 | Boundary reviewed. | Candidate remains external until future project grounding. |

## Minimum Safe Entry Skeleton

```yaml
parking_id:
date_parked:
operator:
source_locator:
locator_stability:
candidate_project_gap:
parking_status:
access_blocker:
terms_blocker:
minimum_safe_summary:
release_condition:
next_owner_action:
```

## Forbidden Shortcuts

- Do not copy source claims, tables, abstracts, figures, or supplemental text
  into this parking queue.
- Do not create a relationship row from a parked hit.
- Do not treat a parked hit as convergence, contradiction, or future-grounding
  evidence.
- Do not use model/RPT summaries to bypass access or terms review.
- Do not let a blocked source change grounded findings, locked rules, or
  validation plans.

## Verification Before Commit

```bash
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit
python3 scripts/v48_governance_preflight.py
```

## Boundary

This queue is a safety buffer for external-source intake. A parked source hit is
not a project finding, not evidence, not a relationship-matrix row, and not a
permission to store external claims. It can move forward only after the release
conditions above are satisfied and the normal V47/V48 provenance gates pass.
