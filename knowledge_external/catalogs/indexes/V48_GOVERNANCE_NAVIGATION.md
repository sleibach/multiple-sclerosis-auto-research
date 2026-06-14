# V48 Governance Navigation

Status: external-knowledge governance/navigation only. These controls keep external context separate from grounded findings; they do not validate external claims.

- artifacts tracked: `15`
- missing artifacts: `0`
- summaries with failures: `0`

## Controls

| artifact | exists | status | purpose | boundary | path |
|---|---|---|---|---|---|
| V48 convergence/contradiction analysis | `yes` | `PASS` | Classed relationship analysis between selected grounded findings and external records. | external agreement is context; project artifacts remain evidence | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md` |
| V48 future-grounding queue | `yes` | `not_applicable` | Future tasks from convergence or insufficient-overlap rows. | queued tasks are not findings | `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md` |
| V48 external resource comparator matrix | `yes` | `PASS` | External resource coverage, access tier, and unique gap matrix. | external resource metadata only | `knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md` |
| V48 source-domain review | `yes` | `PASS` | Domain classification for access and terms maintenance. | domain maintenance only | `knowledge_external/catalogs/indexes/SOURCE_DOMAIN_REVIEW_V48.md` |
| V48 source-terms coverage | `yes` | `not_applicable` | Source-terms metadata coverage and conservative reuse-note map. | source terms metadata only | `knowledge_external/catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md` |
| V47 provenance gate | `yes` | `PASS` | Machine-enforced segregation of external knowledge from grounded trees. | segregation control | `scripts/v47_provenance_gate.py` |
| External record schema linter | `yes` | `PASS` | Required external-record fields and source/class markers. | schema control | `scripts/v47_external_record_schema_linter.py` |
| Relationship vocabulary linter | `yes` | `PASS` | Allowed relationship vocabulary for external records. | vocabulary control | `scripts/v47_relationship_vocabulary_linter.py` |
| Public external index crosslink linter | `yes` | `PASS` | Public external index link target freshness. | navigation control | `scripts/v48_public_index_crosslink_linter.py` |
| Source locator normalization linter | `yes` | `PASS` | Source locator shape checks for external records. | source locator control | `scripts/v48_source_locator_normalization_linter.py` |
| Source-terms metadata linter | `yes` | `PASS` | Completeness checks for optional source_terms objects. | source terms control | `scripts/v48_source_terms_metadata_linter.py` |
| Source-terms freshness linter | `yes` | `PASS` | Checked-date freshness checks for optional source_terms objects. | source terms control | `scripts/v48_source_terms_freshness_linter.py` |
| Support/contradiction coverage linter | `yes` | `PASS` | Ensures support/contradiction records appear in the V48 matrix. | synthesis coverage control | `scripts/v48_support_contradiction_coverage_linter.py` |
| Contradiction-intake linter | `yes` | `PASS` | Ensures future contradiction records remain queued for grounding. | future-grounding control | `scripts/v48_contradiction_intake_linter.py` |
| Source-domain review freshness linter | `yes` | `PASS` | Ensures the source-domain review matches current external records. | domain review control | `scripts/v48_source_domain_review_freshness_linter.py` |

## Use

- Run the listed linters after adding or editing external records.
- A PASS means the provenance/navigation control passed; it is not biological evidence.
- Grounded project findings remain in the normal project report/history/validation trees.
