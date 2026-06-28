# V50 Non-OpenGWAS Search Provenance Card

Status: provenance/navigation card. This file ties together V50 non-OpenGWAS
route checks, metadata searches, source-hit templates, and safe interpretations.
It does not add external records, import data, validate a cohort, or make a
biological claim.

## Route Health Layer

| artifact | role | latest status |
|---|---|---|
| `knowledge_external/synthesis/V50_NON_OPENGWAS_ROUTE_INVENTORY.md` | Lists public routes available while OpenGWAS is expired. | `8` routes registered. |
| `scripts/v50_check_non_opengwas_routes.py` | Transport/schema checker for registered public routes. | PASS, `8` routes, `0` failures, `0` OpenGWAS use. |
| `scripts/v50_run_public_guards.py` | Wrapper for public status freshness plus route health. | PASS, `2` guard families, `0` failures, `0` OpenGWAS use. |
| `meta/V50_PUBLIC_GUARD_STATUS.md` | Public guard status card. | PASS as of the last committed V50 guard run. |

Boundary: a reachable route means the API was accessible at transport/schema
level. It does **not** mean the route contains a usable validation cohort or any
biological evidence.

## Metadata Search Layer

| artifact | routes searched | result | safe interpretation |
|---|---|---|---|
| `knowledge_external/synthesis/V50_TREATMENT_RESPONSE_COHORT_SEARCH.md` | Europe PMC, NCBI GDS | `49` deduplicated hits; `5` manual candidate reviews; `0` verified exact cohorts. | Negative metadata source-search result only. |
| `knowledge_external/synthesis/V50_BIOSTUDIES_TREATMENT_RESPONSE_SEARCH.md` | BioStudies / ArrayExpress-style metadata | `56` deduplicated hits; `6` manual reviews; `3` near-candidates; `0` verified exact cohorts. | Near-candidates remain partial; no early-treatment replacement for Gafson. |
| `knowledge_external/synthesis/V50_TASK68_TEMPLATE_REPLAY.md` | QA replay of task-68 candidate rows | `5` rows replayed; `0` exact cohorts; `4` context-only; `1` false positive. | Confirms the source-hit template preserves the conservative manual boundary. |
| `knowledge_external/catalogs/indexes/V50_NEGATIVE_SOURCE_SEARCH_INDEX.md` | Index of negative/near-miss results | Search runs and near-misses cataloged. | Prevents duplicate search labor and accidental recategorization. |

Boundary: metadata search can identify source candidates and blockers. It cannot
validate the locked V22 rule, prove a cohort is usable, or replace source terms,
sample-level labels, module coverage, and pre-registered intake gates.

## Intake Control Layer

| artifact | control function |
|---|---|
| `knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md` | Requires locator, route, access tier, terms, data level, pairing, endpoint, module-gene coverage, same-definition status, and safe outcome. |
| `knowledge_external/synthesis/V50_V22_V32_CONTRADICTION_TRIGGER_PACKET.md` | Defines same-definition triggers for future sources before V22/V32 convergence or contradiction can be asserted. |
| `docs/validation/KAROLINSKA_LABEL_REQUEST_PACKET_V50.md` | Applies the V50 gates to the best parallel Karolinska DMF label path. |

## Current Safe Conclusions

1. OpenGWAS is still disabled until token renewal; V50 non-OpenGWAS searches did
   not call OpenGWAS.
2. V50 public route health is good enough for continued metadata search.
3. The searched non-OpenGWAS routes did not verify an exact paired
   early-treatment V22/V32 validation cohort.
4. `S-EPMC10360655` is the most useful new near-candidate, but it remains
   `partial_hit_metadata_only` because metadata show DMF PBMC RNA-seq response
   context at baseline/12 months, not clean early-treatment validation.
5. No metadata search result changes the locked V22 rule, V42 pre-registration,
   or V50 convergence/contradiction matrix.

## Future Handling Rule

If a future search finds a promising hit, first classify it with
`knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md`.
Only a hit satisfying all same-definition gates may become a future-grounding
candidate. All other hits remain context, partial, parked, or rejected rows.

## Provenance

Prepared on 2026-06-28 from committed V50 route-check summaries and
metadata-search outputs. Source: `docs/knowledge/EPISTEMIC_CLASSES.md`;
`knowledge_external/synthesis/V50_NON_OPENGWAS_ROUTE_INVENTORY.md`;
`knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md`.
