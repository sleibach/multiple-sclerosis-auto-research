# External MS Knowledge Index

Status: external knowledge navigation only. External records are `NOT_PROJECT_GROUNDED` and are not project evidence.

Grounded project findings remain in the normal project report/history/validation trees. This index points only to the segregated external tree.

## Counts

- external records indexed: `74`
- missing sources: `0`
- missing not-grounded markers: `0`
- source domains represented: `35`
- records with source_terms metadata: `40`
- records missing optional source_terms metadata: `34`
- V48 governance controls tracked: `95`
- reachability maintenance warnings: `2`
- V48 convergence rows asserted: `7`
- V48 contradiction rows flagged: `0`
- V50 additional source-specific convergences asserted: `11`
- V50 contradictions flagged: `0`
- V52 therapeutic convergence rows reviewed: `10`
- V52 therapeutic contradictions flagged: `0`
- placeholder skeleton linked rows: `unknown`

## Epistemic-Class Counts

| field | value | count |
|---|---|---:|
| `epistemic_class` | `external-unverifiable` | 74 |
| `relationship_to_project_findings` | `orthogonal` | 44 |
| `relationship_to_project_findings` | `supports` | 30 |
| `record_type` | `external_claim` | 40 |
| `record_type` | `external_resource_catalog` | 31 |
| `record_type` | `structural_prediction` | 3 |

## Navigation

| artifact | purpose | boundary |
|---|---|---|
| [V48 external layer reader brief](EXTERNAL_LAYER_READER_BRIEF_V48.md) | Plain-language guide to what the external layer can and cannot do. | class-aware public navigation only |
| [Class-aware external record index](catalogs/indexes/EXTERNAL_KNOWLEDGE_INDEX.md) | Browse every external record with source and class markers. | external only |
| [Resource category rollup](catalogs/indexes/EXTERNAL_RESOURCE_CATEGORY_ROLLUP.md) | Browse resource metadata by category. | external resource metadata only |
| [V48 external resource comparator matrix](catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md) | Compare external resources by coverage, access tier, unique gap, and this repo's distinct role. | external resource metadata only |
| [V49 comparator matrix review](catalogs/indexes/V49_COMPARATOR_MATRIX_REVIEW.md) | Review showing V49 source-domain additions do not require new resource-level comparator rows. | external resource metadata only |
| [V49 absent resource intake candidates](catalogs/indexes/V49_ABSENT_RESOURCE_INTAKE_CANDIDATES.md) | Future metadata-only intake candidates for resources not yet represented in the comparator matrix. | future intake/navigation only |
| [V49 absent resource routing audit](catalogs/indexes/V49_ABSENT_RESOURCE_ROUTING_AUDIT.md) | Safe-routing audit confirming absent resource candidates stay metadata-only until source terms and specific accessions are reviewed. | future intake/navigation only |
| [Access-tier rollup](catalogs/indexes/EXTERNAL_RESOURCE_ACCESS_TIER_ROLLUP.md) | Browse public/registration/application/controlled access tiers. | access metadata only |
| [Source-domain rollup](catalogs/indexes/EXTERNAL_SOURCE_DOMAIN_ROLLUP.md) | Browse records by source domain. | source locator metadata only |
| [V48 source-domain review](catalogs/indexes/SOURCE_DOMAIN_REVIEW_V48.md) | Classify source domains for maintenance, access, and terms review. | domain maintenance only |
| [V48 source-domain relationship rollup](catalogs/indexes/SOURCE_DOMAIN_RELATIONSHIP_ROLLUP_V48.md) | Summarize external source domains by project-relationship and V48 matrix classes. | domain relationship metadata only |
| [V48 source-domain independence rollup](catalogs/indexes/SOURCE_DOMAIN_INDEPENDENCE_ROLLUP_V48.md) | Summarize canonical-source concentration by source domain for V48 matrix rows. | provenance/navigation only |
| [V48 source URL duplicate review](catalogs/indexes/SOURCE_URL_DUPLICATE_REVIEW_V48.md) | Review repeated canonical source URLs so shared-source records are not overcounted as independent corroboration. | source maintenance only |
| [V48 source-terms coverage](catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md) | Browse external records by source-terms metadata coverage and conservative reuse notes. | source terms metadata only |
| [V48 source-terms review queue](catalogs/indexes/SOURCE_TERMS_REVIEW_QUEUE_V48.md) | Prioritized terms-review queue for records missing explicit source_terms metadata. | source terms metadata only |
| [V48 high-priority source-terms packet](catalogs/indexes/HIGH_PRIORITY_SOURCE_TERMS_PACKET_V48.md) | Focused packet for high-priority missing source_terms records. | source terms triage only |
| [V49 source-terms follow-up](catalogs/indexes/V49_SOURCE_TERMS_FOLLOWUP.md) | Row-specific fuller-reuse follow-up for V49 records that already have metadata-only source_terms. | source terms metadata only |
| [V50 source-terms gap audit](catalogs/indexes/V50_SOURCE_TERMS_GAP_AUDIT.md) | Focused audit showing no V50 sharper records are blocked by optional source-terms gaps and prioritizing only high-value follow-ups. | source terms metadata only |
| [V50 high-priority source-terms packet](catalogs/indexes/V50_HIGH_PRIORITY_SOURCE_TERMS_PACKET.md) | Operator-ready terms-review packet for GWAS Catalog, MSGD, MSDA, MSBase, and NARCOMS resource rows. | source terms triage only |
| [V48 governance navigation](catalogs/indexes/V48_GOVERNANCE_NAVIGATION.md) | Browse V48 external-knowledge controls and latest pass/fail summaries. | governance/navigation only |
| [V48 governance failure-mode matrix](catalogs/indexes/GOVERNANCE_FAILURE_MODE_MATRIX_V48.md) | Map each governance control to the failure mode it prevents. | governance/navigation only |
| [V48 external synthesis dependency graph](catalogs/indexes/V48_EXTERNAL_SYNTHESIS_DEPENDENCY_GRAPH.md) | Map V48 external synthesis artifacts to their upstream inputs and freshness controls. | governance/navigation only |
| [V48 evidence-boundary glossary](catalogs/indexes/V48_EVIDENCE_BOUNDARY_GLOSSARY.md) | Explain the boundary labels used by V48 external-knowledge controls. | governance/navigation only |
| [V48 preflight summary card](catalogs/indexes/V48_PREFLIGHT_SUMMARY_CARD.md) | Fast command/status handoff for V48 governance checks. | governance/navigation only |
| [V48 external-governance handoff](catalogs/indexes/V48_EXTERNAL_GOVERNANCE_HANDOFF.md) | Compact command handoff and boundary rules for future external-knowledge sessions. | governance/navigation only |
| [V48 AI Core tooling-health card](catalogs/indexes/V48_AI_CORE_TOOLING_HEALTH.md) | Current smoke-test status for Claude, Gemini, and RPT client paths. | tooling/navigation only |
| [V48 model-lens usage boundary](catalogs/indexes/V48_MODEL_LENS_USAGE_BOUNDARY.md) | Public boundary for using Claude, Gemini, and RPT as proposal lenses only. | governance/navigation only |
| [Source URL reachability](catalogs/indexes/EXTERNAL_SOURCE_URL_REACHABILITY.md) | Transport-status maintenance report. | HTTP status is not claim validation |
| [V50 source reachability delta](catalogs/indexes/V50_SOURCE_REACHABILITY_DELTA.md) | Transport-status summary for V50-added records; three HTTP 403 maintenance warnings, no claim-validity change. | HTTP status is not claim validation |
| [V48 convergence/contradiction analysis](synthesis/CONVERGENCE_CONTRADICTION_V48.md) | Populated comparison of selected grounded findings and segregated external records. | external agreement is context; project artifacts remain evidence |
| [V50 convergence/contradiction reassessment](synthesis/CONVERGENCE_CONTRADICTION_V50.md) | Reassessment of high-priority insufficient-overlap rows after adding sharper DMF, ZMIZ1, chr1, and GPR25 source-specific records. | external agreement is context; project artifacts remain evidence |
| [V52 therapeutic convergence/contradiction check](synthesis/V52_THERAPEUTIC_CONVERGENCE_CONTRADICTION.md) | Therapeutic-path review of source-specific V50/V51/V52 context; zero genuine therapeutic contradictions surfaced. | external context does not change therapeutic-path evidence |
| [V48 convergence decision table](synthesis/CONVERGENCE_DECISION_TABLE_V48.md) | Compact operational interpretation of each convergence/insufficient-overlap row. | synthesis/navigation only |
| [V48 convergence/contradiction executive card](synthesis/CONVERGENCE_CONTRADICTION_EXECUTIVE_CARD_V48.md) | Medical-team summary of relationship counts, source-independence limits, and high-priority gaps. | synthesis/navigation only |
| [V48 convergence source-independence matrix](synthesis/CONVERGENCE_SOURCE_INDEPENDENCE_V48.md) | Row-level canonical-source accounting for convergence and insufficient-overlap rows. | provenance/navigation only |
| [V49 source-independence delta](synthesis/V49_SOURCE_INDEPENDENCE_DELTA.md) | V49 note that 7 convergence/context rows correspond to 5 canonical source clusters. | provenance/navigation only |
| [V50 source-independence delta](synthesis/V50_SOURCE_INDEPENDENCE_DELTA.md) | V50 note that 11 source-specific convergence rows correspond to 9 platform-level source families, with 6 separate confounder-context records. | provenance/navigation only |
| [V50 GWAS Catalog allele routing](synthesis/V50_GWAS_CATALOG_ALLELE_ROUTING.md) | Non-OpenGWAS route and API extraction manifest for rs1250550, rs4613763, and rs7522462 allele follow-up. | routing/navigation only |
| [V50 GWAS Catalog fetcher validation](synthesis/V50_GWAS_FETCHER_VALIDATION.md) | Validation showing the reusable non-OpenGWAS fetcher reproduces the prior V50 rsid routing table. | synthesis/navigation only |
| [V50 allele-harmonization checklist](synthesis/V50_ALLELE_HARMONIZATION_CHECKLIST.md) | Minimum future steps before GWAS Catalog rsid routes can become project-grounded direction checks. | future checklist/navigation only |
| [V50 allele-harmonization preparation](synthesis/V50_ALLELE_HARMONIZATION_PREP.md) | Prepared GWAS Catalog rsid rows for future harmonization while explicitly refusing current project-direction conclusions. | routing/navigation only |
| [V50 GWAS harmonization route result](synthesis/V50_GWAS_HARMONIZATION_ROUTE_RESULT.md) | Non-OpenGWAS route result showing source-reported rsid allele contrasts are extractable but not project-direction harmonized. | routing/navigation only |
| [V50 GSE255952 metadata scout](synthesis/V50_GSE255952_METADATA_SCOUT.md) | Metadata-only route for future methylprednisolone B/T-cell steroid-panel stress testing without importing expression values. | routing/navigation only |
| [V50 GSE255952 import checklist](synthesis/V50_GSE255952_IMPORT_CHECKLIST.md) | Future import stop/go checklist for steroid-panel stress testing without treating GSE255952 as V22 validation. | future import/navigation only |
| [V50 zero-contradiction specificity audit](synthesis/V50_ZERO_CONTRADICTION_SPECIFICITY_AUDIT.md) | Explains why V50 has zero same-definition contradictions without implying broad external consensus. | synthesis/navigation only |
| [V50 remaining source search packet](synthesis/V50_REMAINING_SOURCE_SEARCH_PACKET.md) | Narrow future-search queries and acceptance gates for T/B-readable monitoring and EBV specificity rows. | future search/navigation only |
| [V50 T/B monitoring source-search results](synthesis/V50_TB_MONITORING_SOURCE_SEARCH_RESULTS.md) | Narrow search audit for T/B-readable IFN/APC/STAT1 monitoring sources; no same-definition hit found. | future search/navigation only |
| [V50 EBV specificity source-search results](synthesis/V50_EBV_SPECIFICITY_SOURCE_SEARCH_RESULTS.md) | Narrow search audit for EBV/IFN APC specificity-control sources; no same-definition comparator hit found. | future search/navigation only |
| [V50 candidate source parking queue](synthesis/V50_CANDIDATE_SOURCE_PARKING_QUEUE.md) | Parked partial T/B and EBV source hits with release conditions before any future intake. | future search/navigation only |
| [V49 relationship provenance audit](synthesis/V49_RELATIONSHIP_PROVENANCE_AUDIT.md) | Row-level audit showing all 23 relationship rows carry grounded artifact, source, class, marker, and relationship provenance. | provenance/navigation only |
| [V49 corroboration strength tiers](synthesis/V49_CORROBORATION_STRENGTH_TIERS.md) | Tiered interpretation of the 7 convergence rows by source independence, decision relevance, and evidence boundary. | synthesis/navigation only |
| [V48 decision-relevant convergence shortlist](synthesis/DECISION_RELEVANT_CONVERGENCES_V48.md) | Shortlist of current corroborated-context rows and contradictions, if any. | synthesis/navigation only |
| [V48 contradiction readiness playbook](synthesis/CONTRADICTION_READINESS_PLAYBOOK_V48.md) | Predefined handling for future external contradictions without overriding grounded findings. | future-grounding control |
| [V48 contradiction surveillance checklist](synthesis/CONTRADICTION_SURVEILLANCE_CHECKLIST_V48.md) | Future contradiction surveillance triggers by source class and finding category. | future-grounding control |
| [V49 contradiction surveillance shortlist](synthesis/V49_CONTRADICTION_SURVEILLANCE_SHORTLIST.md) | Prioritized rows where a same-definition future source could create a real tension. | future-grounding control |
| [V49 contradiction routing audit](synthesis/V49_CONTRADICTION_ROUTING_AUDIT.md) | Safe-routing audit confirming every contradiction-surveillance row has a future-grounding route and no current contradiction claim. | future-grounding control |
| [V49 contradiction evidence-type map](synthesis/V49_CONTRADICTION_EVIDENCE_TYPES.md) | Minimum evidence fields and non-triggers for future sources before any surveillance row can become a real contradiction. | future-grounding control |
| [V49 zero-contradiction caveat](synthesis/V49_ZERO_CONTRADICTION_CAVEAT.md) | Reader note explaining that zero current contradiction rows does not imply external consensus. | synthesis/navigation only |
| [V48 V37 finding external coverage map](synthesis/V37_FINDING_EXTERNAL_COVERAGE_V48.md) | Coverage map showing which V37 scored findings have V48 external relationship rows. | synthesis/navigation only |
| [V48 V37 uncovered finding rationale](synthesis/V37_UNCOVERED_FINDING_RATIONALE_V48.md) | Rationale for V37 scored findings without V48 external relationship rows. | synthesis/navigation only |
| [V48 V37 external coverage gap priority](synthesis/V37_EXTERNAL_COVERAGE_GAP_PRIORITY_V48.md) | Sourcing-priority map for uncovered V37 findings. | sourcing/navigation only |
| [V48 high-priority external sourcing plan](synthesis/HIGH_PRIORITY_EXTERNAL_SOURCING_PLAN_V48.md) | Source-route plan for high-priority V37 external coverage gaps. | future intake/navigation only |
| [V48 high-priority source-search query packet](synthesis/HIGH_PRIORITY_SOURCE_SEARCH_QUERIES_V48.md) | Concrete search-query packet for high-priority sourcing gaps; queries are candidates only. | future search/navigation only |
| [V48 high-priority source intake checklist](templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md) | Checklist for safely reviewing source hits before any segregated external-record intake. | future search/navigation only |
| [V48 source-intake operator quickstart](templates/SOURCE_INTAKE_OPERATOR_QUICKSTART_V48.md) | Mechanical operator guide for routing source-search hits through safe segregated intake. | future search/navigation only |
| [V48 source-intake package manifest](templates/SOURCE_INTAKE_PACKAGE_MANIFEST_V48.md) | Package-level map tying search packet, checklist, quickstart, reader brief, and future-grounding queue. | future search/navigation only |
| [V48 external intake one-page checklist](templates/EXTERNAL_INTAKE_ONE_PAGE_CHECKLIST_V48.md) | Compact operator checklist for routing source hits through V47/V48 intake controls. | future search/navigation only |
| [V48 source-hit acceptance decision tree](templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md) | Safe routing tree for future source hits before external-record or relationship-row intake. | future search/navigation only |
| [V48 source-hit access/terms parking queue](templates/SOURCE_HIT_ACCESS_TERMS_PARKING_QUEUE_V48.md) | Safe parking template for promising source hits blocked by access, terms, reuse, or locator uncertainty. | future search/navigation only |
| [V48 source de-duplication intake checklist](templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md) | Checklist for avoiding same-source overcounting before relationship or future-grounding intake. | future search/navigation only |
| [V48 parked source release checklist](templates/PARKED_SOURCE_RELEASE_CHECKLIST_V48.md) | Checklist for moving a source hit out of access/terms parking without creating evidence. | future search/navigation only |
| [V48 parked source future-grounding handoff](templates/PARKED_SOURCE_FUTURE_GROUNDING_HANDOFF_V48.md) | Rules for turning released, testable source hits into queued future-grounding tasks only. | future search/navigation only |
| [V48 source-intake audit log template](templates/SOURCE_INTAKE_AUDIT_LOG_TEMPLATE_V48.md) | Audit trail template for future source-intake operator decisions. | future search/navigation only |
| [V48 source-intake decision error taxonomy](templates/SOURCE_INTAKE_DECISION_ERROR_TAXONOMY_V48.md) | QA taxonomy for classifying future source-intake process errors. | future search/navigation only |
| [V48 source-intake reproducibility checklist](templates/SOURCE_INTAKE_REPRODUCIBILITY_CHECKLIST_V48.md) | Reviewer checklist for reproducing future source-intake routing decisions. | future search/navigation only |
| [V48 source-intake stop/go scorecard](templates/SOURCE_INTAKE_STOP_GO_SCORECARD_V48.md) | Pre-specified stop, park, or proceed routing template for future source hits. | future search/navigation only |
| [V48 source-intake reviewer handoff checklist](templates/SOURCE_INTAKE_REVIEWER_HANDOFF_CHECKLIST_V48.md) | Session-to-session handoff checklist for future source-intake review. | future search/navigation only |
| [V50 non-OpenGWAS source-hit review template](templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md) | Metadata-only review template for non-OpenGWAS source hits before any cohort usability or future-grounding claim. | future search/navigation only |
| [V48 source-intake controls coverage](catalogs/indexes/V48_SOURCE_INTAKE_CONTROLS_COVERAGE.md) | Summary card mapping source-intake safeguards to failure modes. | governance/navigation only |
| [V48 active-time accounting audit](catalogs/indexes/V48_ACTIVE_TIME_ACCOUNTING_AUDIT.md) | Operational card distinguishing cumulative active time from wall-clock span. | governance/navigation only |
| [V48 relationship-row candidate template](templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md) | Draft template for future relationship rows before matrix acceptance. | future search/navigation only |
| [V48 contradiction triage mini-template](templates/CONTRADICTION_TRIAGE_MINI_TEMPLATE_V48.md) | Compact safe-routing template for future source hits that appear to disagree with grounded findings. | future search/navigation only |
| [V48 unresolved external coverage handoff](synthesis/UNRESOLVED_EXTERNAL_COVERAGE_HANDOFF_V48.md) | Consolidated unresolved source-search, source-acceptance, future-grounding, and surveillance actions. | work-queue/navigation only |
| [V49 unresolved action reconciliation](synthesis/V49_UNRESOLVED_ACTION_RECONCILIATION.md) | Overlay showing which V48 handoff rows are covered, narrowed, closed-unless-triggered, or unchanged after V49. | work-queue/navigation only |
| [V48 future-grounding queue](synthesis/FUTURE_GROUNDING_QUEUE_V48.md) | Concrete follow-up tasks from V48 convergence/insufficient-overlap rows. | queued tasks are not findings |
| [V49 relationship delta note](synthesis/V49_RELATIONSHIP_DELTA_NOTE.md) | Compact summary of what V49 added to the V48 convergence/contradiction layer. | synthesis/navigation only |
| [V49 content handoff](synthesis/V49_CONTENT_HANDOFF.md) | Medical-team handoff for V49 hygiene, gap closure, validation routing, import packets, and closure guardrails. | synthesis/navigation only |
| [V50 content handoff](synthesis/V50_CONTENT_HANDOFF.md) | Medical-team handoff for V50 source-specific corroborations, non-corroborations, and zero-contradiction caveat. | synthesis/navigation only |
| [V50 validation-context boundary card](synthesis/V50_VALIDATION_CONTEXT_BOUNDARY_CARD.md) | Boundary card explaining why DMF/steroid/composition sources sharpen validation context but do not validate the V22 scalar. | synthesis/navigation only |
| [V50 no-claim language audit](synthesis/V50_NO_CLAIM_LANGUAGE_AUDIT.md) | Audit showing V50 reader-facing shorthand preserves the evidence boundary and does not turn external records into project evidence. | synthesis/navigation only |
| [V50 public MS knowledge-base position card](synthesis/V50_PUBLIC_MS_KB_POSITION_CARD.md) | Class-aware answer to whether another public MS source matches this repo's cross-modal, grounded, validation-ready breadth. | external resource navigation only |
| [V50 public reader path](synthesis/V50_PUBLIC_READER_PATH.md) | Short GitHub-to-evidence route showing how to navigate grounded findings and external context without mixing them. | class-aware public navigation only |
| [V50 public citation card](synthesis/V50_PUBLIC_CITATION_CARD.md) | Conservative public wording for describing or citing the repository without overstating validation, novelty, or external consensus. | class-aware public navigation only |
| [V50 relationship glossary](synthesis/V50_RELATIONSHIP_GLOSSARY.md) | Compact definitions for convergence, contradiction, validation, context, insufficient overlap, and future grounding. | class-aware public navigation only |
| [External structural predictions](structures/README.md) | Browse segregated AlphaFold-style predicted structure records and confidence payloads. | structural predictions are external context only |
| [V51 GPR25 AlphaFold context](synthesis/V51_GPR25_ALPHAFOLD_DRUGGABILITY_CONTEXT.md) | Confidence-qualified AlphaFold DB context for GPR25 druggability-direction discussion. | prediction-informed context only |
| [V52 KIF21B AlphaFold context](synthesis/V52_KIF21B_ALPHAFOLD_DRUGGABILITY_CONTEXT.md) | Confidence-qualified AlphaFold DB context for KIF21B motor-domain druggability-direction discussion. | prediction-informed context only |
| [V52 PTGER4 AlphaFold context](synthesis/V52_PTGER4_ALPHAFOLD_DRUGGABILITY_CONTEXT.md) | Confidence-qualified AlphaFold DB context for PTGER4 druggability-direction discussion. | prediction-informed context only |
| [V50 V22/V32 contradiction trigger packet](synthesis/V50_V22_V32_CONTRADICTION_TRIGGER_PACKET.md) | Same-definition intake rules for future sources before V22/V32 convergence or contradiction can be asserted. | future-grounding control |
| [V50 next source prioritization](synthesis/V50_NEXT_SOURCE_PRIORITIZATION.md) | Ranking of V50 source routes by decision value and executability while OpenGWAS is expired. | synthesis/navigation only |
| [V50 non-OpenGWAS route inventory](synthesis/V50_NON_OPENGWAS_ROUTE_INVENTORY.md) | Smoke-tested public API routes that remain usable while the OpenGWAS JWT is expired. | routing/navigation only |
| [V50 non-OpenGWAS future-grounding queue](synthesis/V50_NON_OPENGWAS_FUTURE_GROUNDING_QUEUE.md) | Route-specific future tasks for safe public API use while OpenGWAS is expired. | queued tasks are not findings |
| [V50 treatment-response cohort search](synthesis/V50_TREATMENT_RESPONSE_COHORT_SEARCH.md) | Metadata-only Europe PMC / NCBI GDS search; no verified exact paired treatment-response cohort candidate found. | source search/navigation only |
| [V50 BioStudies treatment-response search](synthesis/V50_BIOSTUDIES_TREATMENT_RESPONSE_SEARCH.md) | Metadata-only BioStudies/ArrayExpress-style search; identified near-candidates but no verified exact early-treatment validation cohort. | source search/navigation only |
| [V50 BioStudies query reproducibility packet](synthesis/V50_BIOSTUDIES_QUERY_REPRODUCIBILITY_PACKET.md) | Exact BioStudies query strings, encoded API URLs, and recorded hit counts for the V50 treatment-response metadata search. | source search/navigation only |
| [V50 task-68 template replay](synthesis/V50_TASK68_TEMPLATE_REPLAY.md) | QA replay applying the V50 source-hit template to Europe PMC / NCBI GDS heuristic candidates; zero exact cohorts. | source search/navigation only |
| [V50 negative source-search index](catalogs/indexes/V50_NEGATIVE_SOURCE_SEARCH_INDEX.md) | Catalog of V50 non-OpenGWAS metadata searches and near-misses that should not be recounted as exact validation cohorts. | source search/navigation only |
| [V50 machine-readable negative source-search index](catalogs/indexes/V50_NEGATIVE_SOURCE_SEARCH_INDEX_MACHINE_READABLE.md) | Generated TSV/JSON no-recount index for reviewed V50 source-search hits; zero exact cohorts and zero independent source counts. | source search/navigation only |
| [V50 source-hit no-recount checker](templates/V50_SOURCE_HIT_NO_RECOUNT_CHECKER.md) | Operator template and CLI for flagging future metadata hits that match reviewed V50 near-misses, duplicates, or false positives. | source search/navigation only |
| [V50 GSE235357 / S-EPMC10360655 handoff](synthesis/V50_GSE235357_SEPMC10360655_HANDOFF.md) | Route-specific no-recount handoff for the Sánchez-Sanz 2023 DMF PBMC response source family. | source search/navigation only |
| [V50 source-search deduplication decision table](synthesis/V50_SOURCE_SEARCH_DEDUPLICATION_DECISION_TABLE.md) | Compact source-accounting rules for duplicate, partial, context-only, and candidate validation-source hits. | source search/navigation only |
| [V50 non-OpenGWAS search provenance card](synthesis/V50_NON_OPENGWAS_SEARCH_PROVENANCE_CARD.md) | Public chain from route health to metadata search outputs, template gates, and safe interpretations. | source search/navigation only |
| [V50 source-hit independence QA](synthesis/V50_SOURCE_HIT_INDEPENDENCE_QA.md) | De-duplication QA showing V50 non-OpenGWAS source hits add zero independent validation-source counts. | source search/navigation only |
| [V49 reader quickstart](synthesis/V49_READER_QUICKSTART.md) | Question-to-artifact routing guide for V49 content and resume paths. | navigation only |
| [V49 insufficient-overlap triage](synthesis/V49_INSUFFICIENT_OVERLAP_TRIAGE.md) | Actionability triage for insufficient-overlap rows so context-only rows are not reopened without the named trigger. | synthesis/navigation only |
| [V49 insufficient-overlap cause summary](synthesis/V49_INSUFFICIENT_OVERLAP_CAUSE_SUMMARY.md) | Cause-level closure summary explaining why the 16 insufficient-overlap rows are not unresolved gaps. | synthesis/navigation only |
| [V49 context-only closure guardrail](synthesis/V49_CONTEXT_ONLY_CLOSURE_GUARDRAIL.md) | Compact reopen-trigger rules for the seven low-actionability/context-only rows. | synthesis/navigation only |
| [V49 uncovered finding triage](synthesis/V49_UNCOVERED_FINDING_TRIAGE.md) | Direct-source and no-expand routing for V37 findings still uncovered by relationship rows. | sourcing/navigation only |
| [V49 source-specific import packets](synthesis/V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md) | Narrow acceptance gates for future ZMIZ1, chr1 KIF21B/GPR25, and coupled APC-axis source intake. | future intake/navigation only |
| [V49 import-packet queue reconciliation](synthesis/V49_IMPORT_PACKET_QUEUE_RECONCILIATION.md) | Overlay mapping generated future-grounding queue rows to the stricter V49 import-packet field gates. | queue/navigation only |
| [V49 validation-ready row crosscheck](synthesis/V49_VALIDATION_READY_ROW_CROSSCHECK.md) | Crosscheck showing which validation-facing V49 rows are already covered by frozen V42/V44 harnesses. | synthesis/navigation only |
| [V49 new source-domain review](catalogs/indexes/V49_NEW_SOURCE_DOMAIN_REVIEW.md) | Access/terms review for the eight records added during V49. | source maintenance only |
| [V50 future-grounding delta queue](synthesis/FUTURE_GROUNDING_QUEUE_V50.md) | Safe routing of V50 sharper external records into future grounding tasks, blocked routes, and context-only records. | queued tasks are not findings |
| [Convergence/contradiction skeleton](synthesis/CONVERGENCE_CONTRADICTION_SKELETON.md) | Placeholder rows until a grounded-link review is performed. | no convergence claim unless linked and grounded |
| [Intake templates](templates/README.md) | Templates for future external-verifiable claim intake. | queued claims are not findings |

## Current Guardrails

- External claims never alter grounded findings, locked rules, or pre-registrations.
- External-verifiable records require a future grounding route before they can be considered.
- External-unverifiable records remain context only.
- Model/RPT outputs are external-unverifiable proposals unless separately grounded.
