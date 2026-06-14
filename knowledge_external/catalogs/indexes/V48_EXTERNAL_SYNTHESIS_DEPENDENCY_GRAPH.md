# V48 External Synthesis Dependency Graph

Status: governance/navigation only. This graph maps external-layer synthesis artifacts to their inputs and freshness controls; it does not add external records, assert convergence, or change grounded findings.

- artifact nodes: `23`
- dependency/control edges: `66`
- missing outputs: `0`
- missing control sources: `0`
- unguarded nodes: `0`

## Artifact Nodes

| artifact | output | inputs | controls | boundary |
|---|---|---:|---:|---|
| V48 convergence/contradiction matrix | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md` | 2 | 4 | relationship classification only; external agreement is context and project artifacts remain evidence |
| V48 future-grounding queue | `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md` | 1 | 2 | queued tasks are not findings |
| V48 decision-relevant convergence shortlist | `knowledge_external/synthesis/DECISION_RELEVANT_CONVERGENCES_V48.md` | 1 | 1 | navigation shortlist only; no score or rule change |
| V48 convergence source-independence matrix | `knowledge_external/synthesis/CONVERGENCE_SOURCE_INDEPENDENCE_V48.md` | 2 | 1 | independence accounting only; prevents overcounting same-source corroboration |
| V48 source-domain independence rollup | `knowledge_external/catalogs/indexes/SOURCE_DOMAIN_INDEPENDENCE_ROLLUP_V48.md` | 1 | 1 | source-domain accounting only |
| V48 convergence/contradiction executive card | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_EXECUTIVE_CARD_V48.md` | 4 | 1 | handoff/navigation only |
| V48 external resource comparator matrix | `knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md` | 1 | 1 | external resource metadata only |
| V48 source-domain review | `knowledge_external/catalogs/indexes/SOURCE_DOMAIN_REVIEW_V48.md` | 1 | 1 | domain maintenance only |
| V48 source-terms coverage | `knowledge_external/catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md` | 1 | 3 | source terms metadata only |
| V48 high-priority source-terms packet | `knowledge_external/catalogs/indexes/HIGH_PRIORITY_SOURCE_TERMS_PACKET_V48.md` | 1 | 1 | source terms review queue only |
| V37 finding external coverage map | `knowledge_external/synthesis/V37_FINDING_EXTERNAL_COVERAGE_V48.md` | 2 | 1 | coverage accounting only |
| V37 uncovered finding rationale | `knowledge_external/synthesis/V37_UNCOVERED_FINDING_RATIONALE_V48.md` | 1 | 1 | coverage-gap rationale only |
| V37 external coverage gap priority | `knowledge_external/synthesis/V37_EXTERNAL_COVERAGE_GAP_PRIORITY_V48.md` | 2 | 1 | sourcing priority only; not corroboration |
| High-priority external sourcing plan | `knowledge_external/synthesis/HIGH_PRIORITY_EXTERNAL_SOURCING_PLAN_V48.md` | 1 | 1 | future-source planning only |
| High-priority source-search query packet | `knowledge_external/synthesis/HIGH_PRIORITY_SOURCE_SEARCH_QUERIES_V48.md` | 1 | 1 | future-search/navigation only |
| Contradiction readiness playbook | `knowledge_external/synthesis/CONTRADICTION_READINESS_PLAYBOOK_V48.md` | 1 | 1 | future contradiction handling only |
| Contradiction surveillance checklist | `knowledge_external/synthesis/CONTRADICTION_SURVEILLANCE_CHECKLIST_V48.md` | 2 | 1 | future contradiction surveillance only |
| External source URL duplicate review | `knowledge_external/catalogs/indexes/SOURCE_URL_DUPLICATE_REVIEW_V48.md` | 1 | 1 | source maintenance only |
| V48 external synthesis dependency graph | `knowledge_external/catalogs/indexes/V48_EXTERNAL_SYNTHESIS_DEPENDENCY_GRAPH.md` | 1 | 1 | dependency/navigation control |
| V48 governance navigation | `knowledge_external/catalogs/indexes/V48_GOVERNANCE_NAVIGATION.md` | 2 | 1 | navigation control |
| V48 governance failure-mode matrix | `knowledge_external/catalogs/indexes/GOVERNANCE_FAILURE_MODE_MATRIX_V48.md` | 1 | 1 | governance mapping control |
| V48 preflight summary card | `knowledge_external/catalogs/indexes/V48_PREFLIGHT_SUMMARY_CARD.md` | 3 | 1 | handoff/navigation only |
| Public external index | `knowledge_external/INDEX.md` | 2 | 3 | class-aware public navigation only |

## Boundary

- Inputs and controls are provenance/governance dependencies, not biological evidence.
- A dependency edge means an artifact should be regenerated or linted if the upstream source changes.
- Future external sources must still enter through V47 segregation before appearing in synthesis rows.
