# V50 Non-OpenGWAS Source-Hit Review Template

Status: template/navigation only. This template is for future review of source
hits found through non-OpenGWAS routes such as Europe PMC, NCBI GDS,
BioStudies/ArrayExpress, ENA, Crossref, ClinicalTrials.gov, Open Targets, or
GWAS Catalog metadata. It does not import expression data, assert cohort
usability, create convergence, flag contradiction, or change grounded findings.

- minimum review fields: `18`
- same-definition cohort gates: `7`
- safe outcomes: `5`

## Required Inputs

Use this template with:

- `knowledge_external/synthesis/V50_NON_OPENGWAS_ROUTE_INVENTORY.md`
- `knowledge_external/synthesis/V50_NON_OPENGWAS_FUTURE_GROUNDING_QUEUE.md`
- `knowledge_external/synthesis/V50_V22_V32_CONTRADICTION_TRIGGER_PACKET.md`
- `knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md`
- `docs/knowledge/EPISTEMIC_CLASSES.md`

## Minimum Review Fields

| field | required entry |
|---|---|
| `review_date_utc` | UTC date/time of review. |
| `reviewer` | Human or agent identifier. |
| `route` | Public route used, e.g. Europe PMC, NCBI GDS, BioStudies, ENA. |
| `query` | Exact query string or accession lookup. |
| `source_locator` | DOI, PMID, accession, URL, or stable API identifier. |
| `title` | Source title as metadata reports it. |
| `source_type` | Paper, repository record, accession, clinical trial, database row, or other. |
| `access_tier` | Open, low-barrier, controlled, access-unclear, or terms-blocked. |
| `terms_checked` | Yes/no plus note on reuse/download constraints. |
| `data_level_seen` | Metadata only, aggregate tables, sample-level metadata, expression matrix, or unknown. |
| `expression_imported` | Must be `no` unless a separate pre-registered grounded run allows it. |
| `disease_population` | MS subtype/population, comparator, species, and tissue/cell layer. |
| `treatment_or_exposure` | Drug, treatment, perturbation, or exposure described by the source. |
| `timepoints` | Whether baseline and early on-treatment timepoints are present. |
| `paired_subjects` | Whether paired subject/sample structure is visible in metadata. |
| `response_endpoint` | NEDA-4, relapse, MRI, clinical response, pharmacodynamic endpoint, or none visible. |
| `module_gene_coverage_visible` | Whether V22/V32 module-gene coverage can be assessed from metadata only. |
| `same_definition_status` | Exact, partial, adjacent, insufficient, false positive, or blocked. |
| `safe_outcome` | One of the five safe outcomes below. |
| `next_action` | Mechanical next step or named blocker. |

## Same-Definition Cohort Gates

A source hit can be marked `candidate_exact_cohort` only if all seven gates are
satisfied from metadata or terms-permitted inspection:

| gate | pass criterion | fail handling |
|---:|---|---|
| 1 | Human MS cohort, not animal-only, cell-line-only, or generic autoimmune context. | `reject_false_positive` or `context_only`. |
| 2 | Relevant treatment or immune-remodeling exposure is explicit. | `context_only` unless the route was for general source context. |
| 3 | Baseline and early on-treatment or comparable paired timepoints are visible. | `partial_hit_metadata_only`. |
| 4 | Subject-level pairing is visible or can be requested under clear terms. | `partial_hit_metadata_only` or `park_access_terms`. |
| 5 | Response, NEDA-like, relapse/MRI, or pre-specified pharmacodynamic labels are visible or requestable. | `partial_hit_metadata_only` or `park_access_terms`. |
| 6 | Transcriptomic layer is compatible with the frozen modules, and gene identifiers appear recoverable. | `partial_hit_metadata_only` until checked. |
| 7 | Access/reuse terms permit the next planned handling step. | `park_access_terms`. |

Do not count a source as usable if any gate is unknown. Unknown means blocked or
partial, not accepted.

## Safe Outcomes

| outcome | when to use | allowed next action |
|---|---|---|
| `reject_false_positive` | Metadata clearly shows non-MS, wrong species/layer, no treatment-response relevance, or keyword collision. | Record in search output only. |
| `context_only` | Source is relevant external context but cannot meet the same-definition cohort gates. | Link as context only if provenance adds reader value. |
| `partial_hit_metadata_only` | Source may be relevant, but metadata does not prove pairing, labels, module coverage, or terms. | Queue exact missing fields and source-contact/repository-check steps. |
| `park_access_terms` | The hit may be useful, but access, reuse, or controlled-data terms block inspection. | Add to an access/terms parking queue; do not summarize restricted contents. |
| `candidate_exact_cohort` | All same-definition gates pass without importing data outside an approved grounded run. | Prepare a future-grounding route; still not a validation result. |

## Forbidden Shortcuts

- Do not infer paired design from a treatment name alone.
- Do not infer response labels from a clinical cohort title alone.
- Do not treat pharmacodynamic time-course data as response validation unless
  the endpoint is visible and pre-specified.
- Do not count an accession usable until module-gene coverage can be checked.
- Do not import expression matrices during metadata-only source search.
- Do not call OpenGWAS while the V50 JWT is expired.
- Do not let model/RPT summaries decide usability, convergence, or
  contradiction.
- Do not use external metadata as evidence for or against the locked V22 rule.

## Review Row Template

```tsv
review_date_utc	reviewer	route	query	source_locator	title	source_type	access_tier	terms_checked	data_level_seen	expression_imported	disease_population	treatment_or_exposure	timepoints	paired_subjects	response_endpoint	module_gene_coverage_visible	same_definition_status	safe_outcome	next_action
```

## Verification Before Commit

```bash
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v48_public_index_crosslink_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit
```

## Boundary

This template reviews source-hit handling only. A source hit remains external
context or a queued future-grounding route until a separate grounded project
analysis reruns the relevant test on allowed data. Source:
`docs/knowledge/EPISTEMIC_CLASSES.md`; related controls:
`knowledge_external/synthesis/V50_NON_OPENGWAS_FUTURE_GROUNDING_QUEUE.md` and
`knowledge_external/synthesis/V50_V22_V32_CONTRADICTION_TRIGGER_PACKET.md`.
