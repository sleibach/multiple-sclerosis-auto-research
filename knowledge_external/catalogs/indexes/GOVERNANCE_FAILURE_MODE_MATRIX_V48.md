# V48 Governance Failure-Mode Matrix

Status: governance/navigation only. This matrix explains what each control prevents; it does not validate external claims.

- controls mapped: `73`
- boundary classes: `27`
- unmapped boundaries: `0`

## Failure-Mode Matrix

| control | boundary | failure mode prevented | status | path |
|---|---|---|---|---|
| External claim-length safety linter | `copyright/provenance hygiene control` | external summaries become oversized copied source passages | `PASS` | `scripts/v48_external_claim_length_linter.py` |
| External synthesis dependency freshness linter | `dependency/navigation control` | artifact dependency maps drift from current generated outputs, inputs, or controls | `PASS` | `scripts/v48_external_synthesis_dependency_freshness_linter.py` |
| V48 source-domain review | `domain maintenance only` | domain classifications are overread as source-validity claims | `PASS` | `knowledge_external/catalogs/indexes/SOURCE_DOMAIN_REVIEW_V48.md` |
| Source-domain independence freshness linter | `domain relationship control` | source-domain relationship rollups drift from records or matrix rows | `PASS` | `scripts/v48_source_domain_independence_freshness_linter.py` |
| Source-domain relationship freshness linter | `domain relationship control` | source-domain relationship rollups drift from records or matrix rows | `PASS` | `scripts/v48_source_domain_relationship_freshness_linter.py` |
| Source-domain review freshness linter | `domain review control` | source-domain classifications become stale | `PASS` | `scripts/v48_source_domain_review_freshness_linter.py` |
| V48 convergence/contradiction analysis | `external agreement is context; project artifacts remain evidence` | external agreement is over-promoted into evidence | `PASS` | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md` |
| V48 external resource comparator matrix | `external resource metadata only` | resource catalog facts are overread as biological findings | `PASS` | `knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md` |
| Contradiction readiness freshness linter | `future-grounding control` | external-verifiable ideas are treated as findings before grounding | `PASS` | `scripts/v48_contradiction_readiness_freshness_linter.py` |
| Contradiction surveillance freshness linter | `future-grounding control` | external-verifiable ideas are treated as findings before grounding | `PASS` | `scripts/v48_contradiction_surveillance_freshness_linter.py` |
| Contradiction-intake linter | `future-grounding control` | external-verifiable ideas are treated as findings before grounding | `PASS` | `scripts/v48_contradiction_intake_linter.py` |
| External-verifiable intake linter | `future-grounding control` | external-verifiable ideas are treated as findings before grounding | `PASS` | `scripts/v47_external_verifiable_intake_linter.py` |
| Future-grounding queue freshness linter | `future-grounding control` | external-verifiable ideas are treated as findings before grounding | `PASS` | `scripts/v48_future_grounding_queue_freshness_linter.py` |
| High-priority external sourcing plan freshness linter | `future-grounding control` | external-verifiable ideas are treated as findings before grounding | `PASS` | `scripts/v48_high_priority_external_sourcing_plan_freshness_linter.py` |
| Contradiction triage mini-template | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `knowledge_external/templates/CONTRADICTION_TRIAGE_MINI_TEMPLATE_V48.md` |
| Contradiction triage mini-template freshness linter | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `scripts/v48_contradiction_triage_mini_template_freshness_linter.py` |
| High-priority source intake checklist | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md` |
| High-priority source intake checklist freshness linter | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `scripts/v48_high_priority_source_intake_checklist_freshness_linter.py` |
| High-priority source-search query freshness linter | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `scripts/v48_high_priority_source_search_query_freshness_linter.py` |
| Relationship-row candidate template | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `knowledge_external/templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md` |
| Relationship-row candidate template freshness linter | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `scripts/v48_relationship_row_candidate_template_freshness_linter.py` |
| Source-hit acceptance decision tree | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md` |
| Source-hit acceptance decision tree freshness linter | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `scripts/v48_source_hit_acceptance_decision_tree_freshness_linter.py` |
| Source-hit access/terms parking queue | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `knowledge_external/templates/SOURCE_HIT_ACCESS_TERMS_PARKING_QUEUE_V48.md` |
| Source-hit access/terms parking queue freshness linter | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `scripts/v48_source_hit_access_terms_parking_queue_freshness_linter.py` |
| Source-intake operator quickstart | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `knowledge_external/templates/SOURCE_INTAKE_OPERATOR_QUICKSTART_V48.md` |
| Source-intake operator quickstart freshness linter | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `scripts/v48_source_intake_operator_quickstart_freshness_linter.py` |
| Source-intake package manifest | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `knowledge_external/templates/SOURCE_INTAKE_PACKAGE_MANIFEST_V48.md` |
| Source-intake package manifest freshness linter | `future-search control` | future search queries are mistaken for integrated external records, corroboration, or biological evidence | `PASS` | `scripts/v48_source_intake_package_manifest_freshness_linter.py` |
| Governance failure-mode matrix freshness linter | `governance mapping control` | control-to-failure-mode explanations drift from current governance navigation | `PASS` | `scripts/v48_governance_failure_mode_freshness_linter.py` |
| Preflight summary card freshness linter | `handoff/navigation control` | handoff card drifts from current checks or commands | `PASS` | `scripts/v48_preflight_summary_card_freshness_linter.py` |
| Unresolved external coverage handoff freshness linter | `handoff/navigation control` | handoff card drifts from current checks or commands | `PASS` | `scripts/v48_unresolved_external_coverage_handoff_freshness_linter.py` |
| External Markdown index linter | `markdown provenance control` | generated Markdown drops source/provenance labels | `PASS` | `scripts/v47_external_markdown_index_linter.py` |
| AI Core tooling-health freshness linter | `navigation control` | public or operator navigation becomes stale and hides required artifacts | `PASS` | `scripts/v48_ai_core_tooling_health_freshness_linter.py` |
| External layer reader brief freshness linter | `navigation control` | public or operator navigation becomes stale and hides required artifacts | `PASS` | `scripts/v48_external_layer_reader_brief_freshness_linter.py` |
| Governance navigation freshness linter | `navigation control` | public or operator navigation becomes stale and hides required artifacts | `PASS` | `scripts/v48_governance_navigation_freshness_linter.py` |
| Model-lens usage boundary freshness linter | `navigation control` | public or operator navigation becomes stale and hides required artifacts | `PASS` | `scripts/v48_model_lens_usage_boundary_freshness_linter.py` |
| Model-output evidence-claim linter | `navigation control` | public or operator navigation becomes stale and hides required artifacts | `PASS` | `scripts/v48_model_evidence_claim_linter.py` |
| Public external index crosslink linter | `navigation control` | public or operator navigation becomes stale and hides required artifacts | `PASS` | `scripts/v48_public_index_crosslink_linter.py` |
| Public external index freshness linter | `navigation control` | public or operator navigation becomes stale and hides required artifacts | `PASS` | `scripts/v48_public_index_freshness_linter.py` |
| RPT availability claim linter | `navigation control` | public or operator navigation becomes stale and hides required artifacts | `PASS` | `scripts/v48_rpt_availability_claim_linter.py` |
| Unresolved external coverage handoff | `queued tasks are not findings` | future tasks are misread as established results | `PASS` | `knowledge_external/synthesis/UNRESOLVED_EXTERNAL_COVERAGE_HANDOFF_V48.md` |
| V48 future-grounding queue | `queued tasks are not findings` | future tasks are misread as established results | `not_applicable` | `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md` |
| Resource comparator freshness linter | `resource metadata control` | resource comparator metadata drifts from source records | `PASS` | `scripts/v48_resource_comparator_freshness_linter.py` |
| External record schema linter | `schema control` | external records lack mandatory source, class, marker, or relationship fields | `PASS` | `scripts/v47_external_record_schema_linter.py` |
| External record uniqueness linter | `schema control` | external records lack mandatory source, class, marker, or relationship fields | `PASS` | `scripts/v47_external_record_uniqueness_linter.py` |
| Relationship-matrix data dictionary freshness linter | `schema control` | external records lack mandatory source, class, marker, or relationship fields | `PASS` | `scripts/v48_relationship_matrix_data_dictionary_freshness_linter.py` |
| V47 provenance gate | `segregation control` | external knowledge leaks into grounded trees or gains project-evidence authority | `PASS` | `scripts/v47_provenance_gate.py` |
| Source locator normalization linter | `source locator control` | source locators become malformed or non-normalized | `PASS` | `scripts/v48_source_locator_normalization_linter.py` |
| Source URL duplicate freshness linter | `source maintenance control` | duplicate source URLs are mistaken for independent corroboration or left unreviewed | `PASS` | `scripts/v48_source_url_duplicate_freshness_linter.py` |
| High-priority source-terms packet freshness linter | `source terms control` | source terms/reuse status is ambiguous or stale | `PASS` | `scripts/v48_high_priority_source_terms_packet_freshness_linter.py` |
| Source-terms coverage freshness linter | `source terms control` | source terms/reuse status is ambiguous or stale | `PASS` | `scripts/v48_source_terms_coverage_freshness_linter.py` |
| Source-terms freshness linter | `source terms control` | source terms/reuse status is ambiguous or stale | `PASS` | `scripts/v48_source_terms_freshness_linter.py` |
| Source-terms metadata linter | `source terms control` | source terms/reuse status is ambiguous or stale | `PASS` | `scripts/v48_source_terms_metadata_linter.py` |
| V48 source-terms coverage | `source terms metadata only` | terms-review metadata is mistaken for reuse permission | `not_applicable` | `knowledge_external/catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md` |
| V37 external gap-priority freshness linter | `sourcing priority control` | external sourcing priorities are mistaken for corroboration, contradiction, or biological evidence | `PASS` | `scripts/v48_v37_gap_priority_freshness_linter.py` |
| Convergence executive-card freshness linter | `synthesis coverage control` | convergence/contradiction rows fall out of sync with grounded findings or source records | `PASS` | `scripts/v48_convergence_executive_card_freshness_linter.py` |
| Convergence matrix coverage linter | `synthesis coverage control` | convergence/contradiction rows fall out of sync with grounded findings or source records | `PASS` | `scripts/v48_convergence_matrix_coverage_linter.py` |
| Convergence source-independence freshness linter | `synthesis coverage control` | convergence/contradiction rows fall out of sync with grounded findings or source records | `PASS` | `scripts/v48_convergence_source_independence_freshness_linter.py` |
| Decision-relevant convergence freshness linter | `synthesis coverage control` | convergence/contradiction rows fall out of sync with grounded findings or source records | `PASS` | `scripts/v48_decision_relevant_convergence_freshness_linter.py` |
| Support/contradiction coverage linter | `synthesis coverage control` | convergence/contradiction rows fall out of sync with grounded findings or source records | `PASS` | `scripts/v48_support_contradiction_coverage_linter.py` |
| V37 external-coverage freshness linter | `synthesis coverage control` | convergence/contradiction rows fall out of sync with grounded findings or source records | `PASS` | `scripts/v48_v37_coverage_freshness_linter.py` |
| V37 uncovered-rationale freshness linter | `synthesis coverage control` | convergence/contradiction rows fall out of sync with grounded findings or source records | `PASS` | `scripts/v48_v37_uncovered_rationale_freshness_linter.py` |
| Project-finding reference linter | `synthesis reference control` | external support/contradiction records point to missing grounded artifacts | `PASS` | `scripts/v48_project_finding_reference_linter.py` |
| V48 AI Core tooling-health card | `synthesis/navigation only` | navigation rows are overread as evidence or score changes | `PASS` | `knowledge_external/catalogs/indexes/V48_AI_CORE_TOOLING_HEALTH.md` |
| V48 evidence-boundary glossary | `synthesis/navigation only` | navigation rows are overread as evidence or score changes | `PASS` | `knowledge_external/catalogs/indexes/V48_EVIDENCE_BOUNDARY_GLOSSARY.md` |
| V48 external layer reader brief | `synthesis/navigation only` | navigation rows are overread as evidence or score changes | `PASS` | `knowledge_external/EXTERNAL_LAYER_READER_BRIEF_V48.md` |
| V48 model-lens usage boundary | `synthesis/navigation only` | navigation rows are overread as evidence or score changes | `PASS` | `knowledge_external/catalogs/indexes/V48_MODEL_LENS_USAGE_BOUNDARY.md` |
| V48 relationship-matrix data dictionary | `synthesis/navigation only` | navigation rows are overread as evidence or score changes | `PASS` | `knowledge_external/catalogs/indexes/V48_RELATIONSHIP_MATRIX_DATA_DICTIONARY.md` |
| Source URL reachability checker | `transport maintenance only` | source URLs rot or redirect without being visible to maintainers | `PASS` | `scripts/v47_source_url_reachability_checker.py` |
| Convergence status vocabulary linter | `vocabulary control` | relationship/status values drift into ambiguous uncontrolled labels | `PASS` | `scripts/v48_convergence_status_vocabulary_linter.py` |
| Evidence-boundary glossary freshness linter | `vocabulary control` | relationship/status values drift into ambiguous uncontrolled labels | `PASS` | `scripts/v48_evidence_boundary_glossary_freshness_linter.py` |
| Relationship vocabulary linter | `vocabulary control` | relationship/status values drift into ambiguous uncontrolled labels | `PASS` | `scripts/v47_relationship_vocabulary_linter.py` |

## Boundary

- The matrix maps governance risks, not biology.
- A passing control means the specific provenance/navigation failure mode is checked.
- It does not promote external knowledge into the grounded evidence layer.
