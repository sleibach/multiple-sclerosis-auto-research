# V48 Governance Navigation

Status: external-knowledge governance/navigation only. These controls keep external context separate from grounded findings; they do not validate external claims.

- artifacts tracked: `53`
- missing artifacts: `0`
- summaries with failures: `0`

## Controls

| artifact | exists | status | purpose | boundary | path |
|---|---|---|---|---|---|
| V48 convergence/contradiction analysis | `yes` | `PASS` | Classed relationship analysis between selected grounded findings and external records. | external agreement is context; project artifacts remain evidence | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md` |
| V48 relationship-matrix data dictionary | `yes` | `PASS` | Schema dictionary for V48 convergence/contradiction matrix fields and controlled values. | synthesis/navigation only | `knowledge_external/catalogs/indexes/V48_RELATIONSHIP_MATRIX_DATA_DICTIONARY.md` |
| V48 future-grounding queue | `yes` | `not_applicable` | Future tasks from convergence or insufficient-overlap rows. | queued tasks are not findings | `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md` |
| V48 external resource comparator matrix | `yes` | `PASS` | External resource coverage, access tier, and unique gap matrix. | external resource metadata only | `knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md` |
| V48 source-domain review | `yes` | `PASS` | Domain classification for access and terms maintenance. | domain maintenance only | `knowledge_external/catalogs/indexes/SOURCE_DOMAIN_REVIEW_V48.md` |
| V48 source-terms coverage | `yes` | `not_applicable` | Source-terms metadata coverage and conservative reuse-note map. | source terms metadata only | `knowledge_external/catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md` |
| V48 evidence-boundary glossary | `yes` | `PASS` | Glossary for V48 evidence and governance boundary labels. | synthesis/navigation only | `knowledge_external/catalogs/indexes/V48_EVIDENCE_BOUNDARY_GLOSSARY.md` |
| V47 provenance gate | `yes` | `PASS` | Machine-enforced segregation of external knowledge from grounded trees. | segregation control | `scripts/v47_provenance_gate.py` |
| External record schema linter | `yes` | `PASS` | Required external-record fields and source/class markers. | schema control | `scripts/v47_external_record_schema_linter.py` |
| External record uniqueness linter | `yes` | `PASS` | Ensures external record IDs and paths remain unique. | schema control | `scripts/v47_external_record_uniqueness_linter.py` |
| External Markdown index linter | `yes` | `PASS` | Ensures generated external Markdown rows retain source locators. | markdown provenance control | `scripts/v47_external_markdown_index_linter.py` |
| External-verifiable intake linter | `yes` | `PASS` | Ensures future-groundable external claims remain queued, not findings. | future-grounding control | `scripts/v47_external_verifiable_intake_linter.py` |
| Source URL reachability checker | `yes` | `PASS` | Records transport-level URL status for external source locators; not included in deterministic preflight because third-party network status can change. | transport maintenance only | `scripts/v47_source_url_reachability_checker.py` |
| Relationship vocabulary linter | `yes` | `PASS` | Allowed relationship vocabulary for external records. | vocabulary control | `scripts/v47_relationship_vocabulary_linter.py` |
| Public external index crosslink linter | `yes` | `PASS` | Public external index link target freshness. | navigation control | `scripts/v48_public_index_crosslink_linter.py` |
| Public external index freshness linter | `yes` | `PASS` | Ensures required V48 external artifacts are linked from the public external index. | navigation control | `scripts/v48_public_index_freshness_linter.py` |
| Governance navigation freshness linter | `yes` | `PASS` | Ensures governance navigation remains aligned with the current preflight suite. | navigation control | `scripts/v48_governance_navigation_freshness_linter.py` |
| Preflight summary card freshness linter | `yes` | `PASS` | Ensures the V48 preflight summary card matches current component summaries and command handoff. | handoff/navigation control | `scripts/v48_preflight_summary_card_freshness_linter.py` |
| Convergence executive-card freshness linter | `yes` | `PASS` | Ensures the V48 convergence/contradiction executive card matches current relationship, independence, gap-priority, and preflight summaries. | synthesis coverage control | `scripts/v48_convergence_executive_card_freshness_linter.py` |
| Governance failure-mode matrix freshness linter | `yes` | `PASS` | Ensures the governance failure-mode matrix matches current governance navigation rows. | governance mapping control | `scripts/v48_governance_failure_mode_freshness_linter.py` |
| Source locator normalization linter | `yes` | `PASS` | Source locator shape checks for external records. | source locator control | `scripts/v48_source_locator_normalization_linter.py` |
| Source-terms metadata linter | `yes` | `PASS` | Completeness checks for optional source_terms objects. | source terms control | `scripts/v48_source_terms_metadata_linter.py` |
| Source-terms freshness linter | `yes` | `PASS` | Checked-date freshness checks for optional source_terms objects. | source terms control | `scripts/v48_source_terms_freshness_linter.py` |
| Source-terms coverage freshness linter | `yes` | `PASS` | Ensures the source-terms coverage report matches current external records. | source terms control | `scripts/v48_source_terms_coverage_freshness_linter.py` |
| High-priority source-terms packet freshness linter | `yes` | `PASS` | Ensures the high-priority packet matches current high-priority source_terms review rows. | source terms control | `scripts/v48_high_priority_source_terms_packet_freshness_linter.py` |
| High-priority external sourcing plan freshness linter | `yes` | `PASS` | Ensures the high-priority external sourcing plan matches current high-priority V37 coverage gaps. | future-grounding control | `scripts/v48_high_priority_external_sourcing_plan_freshness_linter.py` |
| High-priority source-search query freshness linter | `yes` | `PASS` | Ensures the high-priority source-search query packet matches the current sourcing plan. | future-search control | `scripts/v48_high_priority_source_search_query_freshness_linter.py` |
| High-priority source intake checklist | `yes` | `PASS` | Template for safely reviewing high-priority source hits before any segregated external-record intake. | future-search control | `knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md` |
| High-priority source intake checklist freshness linter | `yes` | `PASS` | Ensures the high-priority source intake checklist matches the current source plan and query packet. | future-search control | `scripts/v48_high_priority_source_intake_checklist_freshness_linter.py` |
| External claim-length safety linter | `yes` | `PASS` | Prevents oversized external claim summaries or excerpt-like fields from entering external records. | copyright/provenance hygiene control | `scripts/v48_external_claim_length_linter.py` |
| Support/contradiction coverage linter | `yes` | `PASS` | Ensures support/contradiction records appear in the V48 matrix. | synthesis coverage control | `scripts/v48_support_contradiction_coverage_linter.py` |
| Relationship-matrix data dictionary freshness linter | `yes` | `PASS` | Ensures the V48 relationship-matrix data dictionary matches the current matrix header and controlled vocabularies. | schema control | `scripts/v48_relationship_matrix_data_dictionary_freshness_linter.py` |
| Contradiction-intake linter | `yes` | `PASS` | Ensures future contradiction records remain queued for grounding. | future-grounding control | `scripts/v48_contradiction_intake_linter.py` |
| Contradiction readiness freshness linter | `yes` | `PASS` | Ensures contradiction readiness playbook counts and stages match the current matrix. | future-grounding control | `scripts/v48_contradiction_readiness_freshness_linter.py` |
| Contradiction surveillance freshness linter | `yes` | `PASS` | Ensures the contradiction surveillance checklist matches current matrix rows and high-priority sourcing plan rows. | future-grounding control | `scripts/v48_contradiction_surveillance_freshness_linter.py` |
| Unresolved external coverage handoff | `yes` | `PASS` | Consolidated unresolved source-search, source-acceptance, future-grounding, and surveillance actions. | queued tasks are not findings | `knowledge_external/synthesis/UNRESOLVED_EXTERNAL_COVERAGE_HANDOFF_V48.md` |
| Unresolved external coverage handoff freshness linter | `yes` | `PASS` | Ensures the unresolved external coverage handoff matches current source-search, future-grounding, and surveillance inputs. | handoff/navigation control | `scripts/v48_unresolved_external_coverage_handoff_freshness_linter.py` |
| Source-domain review freshness linter | `yes` | `PASS` | Ensures the source-domain review matches current external records. | domain review control | `scripts/v48_source_domain_review_freshness_linter.py` |
| Source-domain relationship freshness linter | `yes` | `PASS` | Ensures the source-domain relationship rollup matches current external records and V48 matrix rows. | domain relationship control | `scripts/v48_source_domain_relationship_freshness_linter.py` |
| Source-domain independence freshness linter | `yes` | `PASS` | Ensures the source-domain independence rollup matches the current row-level source-independence matrix. | domain relationship control | `scripts/v48_source_domain_independence_freshness_linter.py` |
| Source URL duplicate freshness linter | `yes` | `PASS` | Ensures the source URL duplicate review matches current external source records. | source maintenance control | `scripts/v48_source_url_duplicate_freshness_linter.py` |
| External synthesis dependency freshness linter | `yes` | `PASS` | Ensures the external synthesis dependency graph matches current generator-declared artifacts, inputs, controls, and counts. | dependency/navigation control | `scripts/v48_external_synthesis_dependency_freshness_linter.py` |
| Evidence-boundary glossary freshness linter | `yes` | `PASS` | Ensures the evidence-boundary glossary matches the current governance failure-mode matrix. | vocabulary control | `scripts/v48_evidence_boundary_glossary_freshness_linter.py` |
| V37 external-coverage freshness linter | `yes` | `PASS` | Ensures the V37 scored-finding coverage map matches current V37 scores and V48 matrix rows. | synthesis coverage control | `scripts/v48_v37_coverage_freshness_linter.py` |
| V37 uncovered-rationale freshness linter | `yes` | `PASS` | Ensures the V37 uncovered-finding rationale table matches the current coverage map. | synthesis coverage control | `scripts/v48_v37_uncovered_rationale_freshness_linter.py` |
| V37 external gap-priority freshness linter | `yes` | `PASS` | Ensures the V37 external coverage gap priority map matches current coverage and rationale inputs. | sourcing priority control | `scripts/v48_v37_gap_priority_freshness_linter.py` |
| Decision-relevant convergence freshness linter | `yes` | `PASS` | Ensures the decision-relevant convergence shortlist matches current converges/contradicts matrix rows. | synthesis coverage control | `scripts/v48_decision_relevant_convergence_freshness_linter.py` |
| Convergence source-independence freshness linter | `yes` | `PASS` | Ensures source-independence accounting matches current V48 convergence matrix rows. | synthesis coverage control | `scripts/v48_convergence_source_independence_freshness_linter.py` |
| Convergence matrix coverage linter | `yes` | `PASS` | Ensures priority grounded findings remain represented in the V48 matrix. | synthesis coverage control | `scripts/v48_convergence_matrix_coverage_linter.py` |
| Convergence status vocabulary linter | `yes` | `PASS` | Checks controlled relationship/status vocabulary in the V48 matrix. | vocabulary control | `scripts/v48_convergence_status_vocabulary_linter.py` |
| Future-grounding queue freshness linter | `yes` | `PASS` | Ensures matrix follow-up actions are represented in the future-grounding queue. | future-grounding control | `scripts/v48_future_grounding_queue_freshness_linter.py` |
| Project-finding reference linter | `yes` | `PASS` | Checks external support/contradiction records point to existing project finding artifacts. | synthesis reference control | `scripts/v48_project_finding_reference_linter.py` |
| Resource comparator freshness linter | `yes` | `PASS` | Ensures the resource comparator matrix matches current external resource records. | resource metadata control | `scripts/v48_resource_comparator_freshness_linter.py` |

## Use

- Run the listed linters after adding or editing external records.
- A PASS means the provenance/navigation control passed; it is not biological evidence.
- Grounded project findings remain in the normal project report/history/validation trees.
