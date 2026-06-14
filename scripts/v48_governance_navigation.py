#!/usr/bin/env python3
"""Generate a V48 governance navigation page for external-knowledge controls."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "knowledge_external/catalogs/indexes"


ARTIFACTS = [
    {
        "artifact": "V48 convergence/contradiction analysis",
        "path": "knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md",
        "summary": "knowledge_external/catalogs/indexes/convergence_contradiction_v48_summary.json",
        "purpose": "Classed relationship analysis between selected grounded findings and external records.",
        "boundary": "external agreement is context; project artifacts remain evidence",
    },
    {
        "artifact": "V48 relationship-matrix data dictionary",
        "path": "knowledge_external/catalogs/indexes/V48_RELATIONSHIP_MATRIX_DATA_DICTIONARY.md",
        "summary": "knowledge_external/catalogs/indexes/v48_relationship_matrix_data_dictionary_summary.json",
        "purpose": "Schema dictionary for V48 convergence/contradiction matrix fields and controlled values.",
        "boundary": "synthesis/navigation only",
    },
    {
        "artifact": "V48 future-grounding queue",
        "path": "knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md",
        "summary": "knowledge_external/synthesis/future_grounding_queue_v48_summary.json",
        "purpose": "Future tasks from convergence or insufficient-overlap rows.",
        "boundary": "queued tasks are not findings",
    },
    {
        "artifact": "V48 external resource comparator matrix",
        "path": "knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md",
        "summary": "knowledge_external/catalogs/indexes/external_resource_comparator_matrix_v48_summary.json",
        "purpose": "External resource coverage, access tier, and unique gap matrix.",
        "boundary": "external resource metadata only",
    },
    {
        "artifact": "V48 source-domain review",
        "path": "knowledge_external/catalogs/indexes/SOURCE_DOMAIN_REVIEW_V48.md",
        "summary": "knowledge_external/catalogs/indexes/source_domain_review_v48_summary.json",
        "purpose": "Domain classification for access and terms maintenance.",
        "boundary": "domain maintenance only",
    },
    {
        "artifact": "V48 source-terms coverage",
        "path": "knowledge_external/catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md",
        "summary": "knowledge_external/catalogs/indexes/source_terms_coverage_v48_summary.json",
        "purpose": "Source-terms metadata coverage and conservative reuse-note map.",
        "boundary": "source terms metadata only",
    },
    {
        "artifact": "V48 evidence-boundary glossary",
        "path": "knowledge_external/catalogs/indexes/V48_EVIDENCE_BOUNDARY_GLOSSARY.md",
        "summary": "knowledge_external/catalogs/indexes/v48_evidence_boundary_glossary_summary.json",
        "purpose": "Glossary for V48 evidence and governance boundary labels.",
        "boundary": "synthesis/navigation only",
    },
    {
        "artifact": "V48 external layer reader brief",
        "path": "knowledge_external/EXTERNAL_LAYER_READER_BRIEF_V48.md",
        "summary": "knowledge_external/catalogs/indexes/external_layer_reader_brief_v48_summary.json",
        "purpose": "Plain-language guide to the external layer's capabilities, limits, and evidence boundary.",
        "boundary": "synthesis/navigation only",
    },
    {
        "artifact": "V48 AI Core tooling-health card",
        "path": "knowledge_external/catalogs/indexes/V48_AI_CORE_TOOLING_HEALTH.md",
        "summary": "knowledge_external/catalogs/indexes/v48_ai_core_tooling_health_summary.json",
        "purpose": "Records current Claude/Gemini smoke status and route-specific RPT `rpt-smoke` status without treating model output as evidence.",
        "boundary": "synthesis/navigation only",
    },
    {
        "artifact": "V48 model-lens usage boundary",
        "path": "knowledge_external/catalogs/indexes/V48_MODEL_LENS_USAGE_BOUNDARY.md",
        "summary": "knowledge_external/catalogs/indexes/v48_model_lens_usage_boundary_summary.json",
        "purpose": "Public boundary for using Claude, Gemini, and route-specific RPT `rpt-smoke` as proposal lenses only.",
        "boundary": "synthesis/navigation only",
    },
    {
        "artifact": "V47 provenance gate",
        "path": "scripts/v47_provenance_gate.py",
        "summary": "analysis/v47_provenance_gate/provenance_gate_summary.json",
        "purpose": "Machine-enforced segregation of external knowledge from grounded trees.",
        "boundary": "segregation control",
    },
    {
        "artifact": "External record schema linter",
        "path": "scripts/v47_external_record_schema_linter.py",
        "summary": "analysis/v47_external_record_schema_linter/external_record_schema_lint_summary.json",
        "purpose": "Required external-record fields and source/class markers.",
        "boundary": "schema control",
    },
    {
        "artifact": "External record uniqueness linter",
        "path": "scripts/v47_external_record_uniqueness_linter.py",
        "summary": "analysis/v47_external_record_uniqueness_linter/external_record_uniqueness_lint_summary.json",
        "purpose": "Ensures external record IDs and paths remain unique.",
        "boundary": "schema control",
    },
    {
        "artifact": "External Markdown index linter",
        "path": "scripts/v47_external_markdown_index_linter.py",
        "summary": "analysis/v47_external_markdown_index_linter/external_markdown_index_lint_summary.json",
        "purpose": "Ensures generated external Markdown rows retain source locators.",
        "boundary": "markdown provenance control",
    },
    {
        "artifact": "External-verifiable intake linter",
        "path": "scripts/v47_external_verifiable_intake_linter.py",
        "summary": "analysis/v47_external_verifiable_intake_linter/external_verifiable_intake_lint_summary.json",
        "purpose": "Ensures future-groundable external claims remain queued, not findings.",
        "boundary": "future-grounding control",
    },
    {
        "artifact": "Source URL reachability checker",
        "path": "scripts/v47_source_url_reachability_checker.py",
        "summary": "knowledge_external/catalogs/indexes/external_source_url_reachability_summary.json",
        "purpose": "Records transport-level URL status for external source locators; not included in deterministic preflight because third-party network status can change.",
        "boundary": "transport maintenance only",
    },
    {
        "artifact": "Relationship vocabulary linter",
        "path": "scripts/v47_relationship_vocabulary_linter.py",
        "summary": "analysis/v47_relationship_vocabulary_linter/relationship_vocabulary_lint_summary.json",
        "purpose": "Allowed relationship vocabulary for external records.",
        "boundary": "vocabulary control",
    },
    {
        "artifact": "Public external index crosslink linter",
        "path": "scripts/v48_public_index_crosslink_linter.py",
        "summary": "analysis/v48_public_index_crosslink_linter/public_index_crosslink_lint_summary.json",
        "purpose": "Public external index link target freshness.",
        "boundary": "navigation control",
    },
    {
        "artifact": "Public external index freshness linter",
        "path": "scripts/v48_public_index_freshness_linter.py",
        "summary": "analysis/v48_public_index_freshness_linter/public_index_freshness_lint_summary.json",
        "purpose": "Ensures required V48 external artifacts are linked from the public external index.",
        "boundary": "navigation control",
    },
    {
        "artifact": "External layer reader brief freshness linter",
        "path": "scripts/v48_external_layer_reader_brief_freshness_linter.py",
        "summary": "analysis/v48_external_layer_reader_brief_freshness_linter/external_layer_reader_brief_freshness_lint_summary.json",
        "purpose": "Ensures the public reader brief keeps required boundary sections, links, and source markers.",
        "boundary": "navigation control",
    },
    {
        "artifact": "AI Core tooling-health freshness linter",
        "path": "scripts/v48_ai_core_tooling_health_freshness_linter.py",
        "summary": "analysis/v48_ai_core_tooling_health_freshness_linter/ai_core_tooling_health_freshness_lint_summary.json",
        "purpose": "Ensures the AI Core tooling-health handoff keeps reproducible command strings and truthful route statuses.",
        "boundary": "navigation control",
    },
    {
        "artifact": "RPT availability claim linter",
        "path": "scripts/v48_rpt_availability_claim_linter.py",
        "summary": "analysis/v48_rpt_availability_claim_linter/rpt_availability_claim_lint_summary.json",
        "purpose": "Prevents queue and external navigation text from claiming RPT availability through the wrong route or stale unavailable status.",
        "boundary": "navigation control",
    },
    {
        "artifact": "Model-lens usage boundary freshness linter",
        "path": "scripts/v48_model_lens_usage_boundary_freshness_linter.py",
        "summary": "analysis/v48_model_lens_usage_boundary_freshness_linter/model_lens_usage_boundary_freshness_lint_summary.json",
        "purpose": "Ensures the model-lens usage boundary keeps required sections, route-specific RPT wording, and no-model-output-as-evidence rules.",
        "boundary": "navigation control",
    },
    {
        "artifact": "Model-output evidence-claim linter",
        "path": "scripts/v48_model_evidence_claim_linter.py",
        "summary": "analysis/v48_model_evidence_claim_linter/model_evidence_claim_lint_summary.json",
        "purpose": "Prevents model-lens output from being framed as evidence or validation in handoff/navigation text.",
        "boundary": "navigation control",
    },
    {
        "artifact": "Governance navigation freshness linter",
        "path": "scripts/v48_governance_navigation_freshness_linter.py",
        "summary": "analysis/v48_governance_navigation_freshness_linter/governance_navigation_freshness_lint_summary.json",
        "purpose": "Ensures governance navigation remains aligned with the current preflight suite.",
        "boundary": "navigation control",
    },
    {
        "artifact": "Preflight summary card freshness linter",
        "path": "scripts/v48_preflight_summary_card_freshness_linter.py",
        "summary": "analysis/v48_preflight_summary_card_freshness_linter/preflight_summary_card_freshness_lint_summary.json",
        "purpose": "Ensures the V48 preflight summary card matches current component summaries and command handoff.",
        "boundary": "handoff/navigation control",
    },
    {
        "artifact": "Convergence executive-card freshness linter",
        "path": "scripts/v48_convergence_executive_card_freshness_linter.py",
        "summary": "analysis/v48_convergence_executive_card_freshness_linter/convergence_executive_card_freshness_lint_summary.json",
        "purpose": "Ensures the V48 convergence/contradiction executive card matches current relationship, independence, gap-priority, and preflight summaries.",
        "boundary": "synthesis coverage control",
    },
    {
        "artifact": "Governance failure-mode matrix freshness linter",
        "path": "scripts/v48_governance_failure_mode_freshness_linter.py",
        "summary": "analysis/v48_governance_failure_mode_freshness_linter/governance_failure_mode_freshness_lint_summary.json",
        "purpose": "Ensures the governance failure-mode matrix matches current governance navigation rows.",
        "boundary": "governance mapping control",
    },
    {
        "artifact": "Source locator normalization linter",
        "path": "scripts/v48_source_locator_normalization_linter.py",
        "summary": "analysis/v48_source_locator_normalization_linter/source_locator_normalization_lint_summary.json",
        "purpose": "Source locator shape checks for external records.",
        "boundary": "source locator control",
    },
    {
        "artifact": "Source-terms metadata linter",
        "path": "scripts/v48_source_terms_metadata_linter.py",
        "summary": "analysis/v48_source_terms_metadata_linter/source_terms_metadata_lint_summary.json",
        "purpose": "Completeness checks for optional source_terms objects.",
        "boundary": "source terms control",
    },
    {
        "artifact": "Source-terms freshness linter",
        "path": "scripts/v48_source_terms_freshness_linter.py",
        "summary": "analysis/v48_source_terms_freshness_linter/source_terms_freshness_lint_summary.json",
        "purpose": "Checked-date freshness checks for optional source_terms objects.",
        "boundary": "source terms control",
    },
    {
        "artifact": "Source-terms coverage freshness linter",
        "path": "scripts/v48_source_terms_coverage_freshness_linter.py",
        "summary": "analysis/v48_source_terms_coverage_freshness_linter/source_terms_coverage_freshness_lint_summary.json",
        "purpose": "Ensures the source-terms coverage report matches current external records.",
        "boundary": "source terms control",
    },
    {
        "artifact": "High-priority source-terms packet freshness linter",
        "path": "scripts/v48_high_priority_source_terms_packet_freshness_linter.py",
        "summary": "analysis/v48_high_priority_source_terms_packet_freshness_linter/high_priority_source_terms_packet_freshness_lint_summary.json",
        "purpose": "Ensures the high-priority packet matches current high-priority source_terms review rows.",
        "boundary": "source terms control",
    },
    {
        "artifact": "High-priority external sourcing plan freshness linter",
        "path": "scripts/v48_high_priority_external_sourcing_plan_freshness_linter.py",
        "summary": "analysis/v48_high_priority_external_sourcing_plan_freshness_linter/high_priority_external_sourcing_plan_freshness_lint_summary.json",
        "purpose": "Ensures the high-priority external sourcing plan matches current high-priority V37 coverage gaps.",
        "boundary": "future-grounding control",
    },
    {
        "artifact": "High-priority source-search query freshness linter",
        "path": "scripts/v48_high_priority_source_search_query_freshness_linter.py",
        "summary": "analysis/v48_high_priority_source_search_query_freshness_linter/high_priority_source_search_query_freshness_lint_summary.json",
        "purpose": "Ensures the high-priority source-search query packet matches the current sourcing plan.",
        "boundary": "future-search control",
    },
    {
        "artifact": "High-priority source intake checklist",
        "path": "knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md",
        "summary": "knowledge_external/catalogs/indexes/high_priority_source_intake_checklist_v48_summary.json",
        "purpose": "Template for safely reviewing high-priority source hits before any segregated external-record intake.",
        "boundary": "future-search control",
    },
    {
        "artifact": "High-priority source intake checklist freshness linter",
        "path": "scripts/v48_high_priority_source_intake_checklist_freshness_linter.py",
        "summary": "analysis/v48_high_priority_source_intake_checklist_freshness_linter/high_priority_source_intake_checklist_freshness_lint_summary.json",
        "purpose": "Ensures the high-priority source intake checklist matches the current source plan and query packet.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake operator quickstart",
        "path": "knowledge_external/templates/SOURCE_INTAKE_OPERATOR_QUICKSTART_V48.md",
        "summary": "knowledge_external/catalogs/indexes/source_intake_operator_quickstart_v48_summary.json",
        "purpose": "Operator guide mapping source-search hits through checklist-based segregated intake.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake operator quickstart freshness linter",
        "path": "scripts/v48_source_intake_operator_quickstart_freshness_linter.py",
        "summary": "analysis/v48_source_intake_operator_quickstart_freshness_linter/source_intake_operator_quickstart_freshness_lint_summary.json",
        "purpose": "Ensures the source-intake operator quickstart keeps required workflow sections, links, and boundary phrases.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake package manifest",
        "path": "knowledge_external/templates/SOURCE_INTAKE_PACKAGE_MANIFEST_V48.md",
        "summary": "knowledge_external/catalogs/indexes/source_intake_package_manifest_v48_summary.json",
        "purpose": "Package-level routing manifest tying source search, checklist, quickstart, reader brief, and future-grounding queue.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake package manifest freshness linter",
        "path": "scripts/v48_source_intake_package_manifest_freshness_linter.py",
        "summary": "analysis/v48_source_intake_package_manifest_freshness_linter/source_intake_package_manifest_freshness_lint_summary.json",
        "purpose": "Ensures the source-intake package manifest keeps required components, operator steps, commands, and boundary phrases.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-hit acceptance decision tree",
        "path": "knowledge_external/templates/SOURCE_HIT_ACCEPTANCE_DECISION_TREE_V48.md",
        "summary": "knowledge_external/catalogs/indexes/source_hit_acceptance_decision_tree_v48_summary.json",
        "purpose": "Decision tree for safely routing future source hits before external-record or relationship-row intake.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-hit acceptance decision tree freshness linter",
        "path": "scripts/v48_source_hit_acceptance_decision_tree_freshness_linter.py",
        "summary": "analysis/v48_source_hit_acceptance_decision_tree_freshness_linter/source_hit_acceptance_decision_tree_freshness_lint_summary.json",
        "purpose": "Ensures the source-hit acceptance decision tree keeps required links, decision nodes, safe outcomes, and boundary phrases.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-hit access/terms parking queue",
        "path": "knowledge_external/templates/SOURCE_HIT_ACCESS_TERMS_PARKING_QUEUE_V48.md",
        "summary": "knowledge_external/catalogs/indexes/source_hit_access_terms_parking_queue_v48_summary.json",
        "purpose": "Template for parking promising source hits blocked by access, terms, reuse, or locator uncertainty without copying claims or making evidence.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-hit access/terms parking queue freshness linter",
        "path": "scripts/v48_source_hit_access_terms_parking_queue_freshness_linter.py",
        "summary": "analysis/v48_source_hit_access_terms_parking_queue_freshness_linter/source_hit_access_terms_parking_queue_freshness_lint_summary.json",
        "purpose": "Ensures the parking queue keeps required fields, statuses, release conditions, linked controls, and no-evidence language.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source de-duplication intake checklist",
        "path": "knowledge_external/templates/SOURCE_DEDUPLICATION_INTAKE_CHECKLIST_V48.md",
        "summary": "knowledge_external/catalogs/indexes/source_deduplication_intake_checklist_v48_summary.json",
        "purpose": "Checklist for avoiding duplicate source and same-source overcounting before relationship or future-grounding intake.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source de-duplication intake checklist freshness linter",
        "path": "scripts/v48_source_deduplication_intake_checklist_freshness_linter.py",
        "summary": "analysis/v48_source_deduplication_intake_checklist_freshness_linter/source_deduplication_intake_checklist_freshness_lint_summary.json",
        "purpose": "Ensures the de-duplication checklist keeps required checks, duplicate states, safe merge actions, and no-overcounting language.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Parked source release checklist",
        "path": "knowledge_external/templates/PARKED_SOURCE_RELEASE_CHECKLIST_V48.md",
        "summary": "knowledge_external/catalogs/indexes/parked_source_release_checklist_v48_summary.json",
        "purpose": "Checklist for releasing parked source hits only after locator, access, terms, de-duplication, and boundary checks pass.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Parked source release checklist freshness linter",
        "path": "scripts/v48_parked_source_release_checklist_freshness_linter.py",
        "summary": "analysis/v48_parked_source_release_checklist_freshness_linter/parked_source_release_checklist_freshness_lint_summary.json",
        "purpose": "Ensures the parked-source release checklist keeps release checks, outcomes, linked controls, and no-evidence language.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Parked source future-grounding handoff",
        "path": "knowledge_external/templates/PARKED_SOURCE_FUTURE_GROUNDING_HANDOFF_V48.md",
        "summary": "knowledge_external/catalogs/indexes/parked_source_future_grounding_handoff_v48_summary.json",
        "purpose": "Rules for routing released, testable source hits to queued future-grounding tasks only.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Parked source future-grounding handoff freshness linter",
        "path": "scripts/v48_parked_source_future_grounding_handoff_freshness_linter.py",
        "summary": "analysis/v48_parked_source_future_grounding_handoff_freshness_linter/parked_source_future_grounding_handoff_freshness_lint_summary.json",
        "purpose": "Ensures the parked-source handoff keeps criteria, outcomes, linked controls, and not-a-finding language.",
        "boundary": "future-search control",
    },
    {
        "artifact": "External intake one-page checklist",
        "path": "knowledge_external/templates/EXTERNAL_INTAKE_ONE_PAGE_CHECKLIST_V48.md",
        "summary": "knowledge_external/catalogs/indexes/external_intake_one_page_checklist_v48_summary.json",
        "purpose": "Compact operator checklist for routing future source hits through V47/V48 intake controls.",
        "boundary": "future-search control",
    },
    {
        "artifact": "External intake one-page checklist freshness linter",
        "path": "scripts/v48_external_intake_one_page_checklist_freshness_linter.py",
        "summary": "analysis/v48_external_intake_one_page_checklist_freshness_linter/external_intake_one_page_checklist_freshness_lint_summary.json",
        "purpose": "Ensures the one-page intake checklist keeps required controls, operator steps, stop conditions, and boundary language.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake audit log template",
        "path": "knowledge_external/templates/SOURCE_INTAKE_AUDIT_LOG_TEMPLATE_V48.md",
        "summary": "knowledge_external/catalogs/indexes/source_intake_audit_log_template_v48_summary.json",
        "purpose": "Audit trail template for future source-intake operator routing decisions without storing claims or evidence.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake audit log template freshness linter",
        "path": "scripts/v48_source_intake_audit_log_template_freshness_linter.py",
        "summary": "analysis/v48_source_intake_audit_log_template_freshness_linter/source_intake_audit_log_template_freshness_lint_summary.json",
        "purpose": "Ensures the audit log template keeps audit fields, event types, linked controls, and no-evidence language.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake decision error taxonomy",
        "path": "knowledge_external/templates/SOURCE_INTAKE_DECISION_ERROR_TAXONOMY_V48.md",
        "summary": "knowledge_external/catalogs/indexes/source_intake_decision_error_taxonomy_v48_summary.json",
        "purpose": "QA taxonomy for classifying future external-source intake process errors without judging scientific truth.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake decision error taxonomy freshness linter",
        "path": "scripts/v48_source_intake_decision_error_taxonomy_freshness_linter.py",
        "summary": "analysis/v48_source_intake_decision_error_taxonomy_freshness_linter/source_intake_decision_error_taxonomy_freshness_lint_summary.json",
        "purpose": "Ensures the decision-error taxonomy keeps error classes, severity levels, linked controls, and boundary language.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake reproducibility checklist",
        "path": "knowledge_external/templates/SOURCE_INTAKE_REPRODUCIBILITY_CHECKLIST_V48.md",
        "summary": "knowledge_external/catalogs/indexes/source_intake_reproducibility_checklist_v48_summary.json",
        "purpose": "Reviewer checklist for reproducing future source-intake routing decisions from locator, audit log, and controls.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake reproducibility checklist freshness linter",
        "path": "scripts/v48_source_intake_reproducibility_checklist_freshness_linter.py",
        "summary": "analysis/v48_source_intake_reproducibility_checklist_freshness_linter/source_intake_reproducibility_checklist_freshness_lint_summary.json",
        "purpose": "Ensures the reproducibility checklist keeps checks, reviewer outcomes, linked controls, and no-evidence language.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake stop/go scorecard",
        "path": "knowledge_external/templates/SOURCE_INTAKE_STOP_GO_SCORECARD_V48.md",
        "summary": "knowledge_external/catalogs/indexes/source_intake_stop_go_scorecard_v48_summary.json",
        "purpose": "Pre-specified stop, park, or proceed routing template for future source hits.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake stop/go scorecard freshness linter",
        "path": "scripts/v48_source_intake_stop_go_scorecard_freshness_linter.py",
        "summary": "analysis/v48_source_intake_stop_go_scorecard_freshness_linter/source_intake_stop_go_scorecard_freshness_lint_summary.json",
        "purpose": "Ensures the stop/go scorecard keeps criteria, outcomes, linked controls, and no-evidence-score language.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake reviewer handoff checklist",
        "path": "knowledge_external/templates/SOURCE_INTAKE_REVIEWER_HANDOFF_CHECKLIST_V48.md",
        "summary": "knowledge_external/catalogs/indexes/source_intake_reviewer_handoff_checklist_v48_summary.json",
        "purpose": "Session-to-session handoff checklist for future source-intake review continuity.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake reviewer handoff checklist freshness linter",
        "path": "scripts/v48_source_intake_reviewer_handoff_checklist_freshness_linter.py",
        "summary": "analysis/v48_source_intake_reviewer_handoff_checklist_freshness_linter/source_intake_reviewer_handoff_checklist_freshness_lint_summary.json",
        "purpose": "Ensures the reviewer handoff checklist keeps fields, statuses, links, and operational-only boundary language.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Source-intake controls coverage card",
        "path": "knowledge_external/catalogs/indexes/V48_SOURCE_INTAKE_CONTROLS_COVERAGE.md",
        "summary": "knowledge_external/catalogs/indexes/source_intake_controls_coverage_v48_summary.json",
        "purpose": "Summary card mapping V48 source-intake safeguards to the failure modes they prevent.",
        "boundary": "governance/navigation only",
    },
    {
        "artifact": "Source-intake controls coverage card freshness linter",
        "path": "scripts/v48_source_intake_controls_coverage_freshness_linter.py",
        "summary": "analysis/v48_source_intake_controls_coverage_freshness_linter/source_intake_controls_coverage_freshness_lint_summary.json",
        "purpose": "Ensures the source-intake controls coverage card keeps safeguard counts, failure-mode counts, links, and boundary language.",
        "boundary": "governance/navigation only",
    },
    {
        "artifact": "Active-time accounting audit card",
        "path": "knowledge_external/catalogs/indexes/V48_ACTIVE_TIME_ACCOUNTING_AUDIT.md",
        "summary": "knowledge_external/catalogs/indexes/active_time_accounting_audit_v48_summary.json",
        "purpose": "Operational card distinguishing cumulative active time from wall-clock span for V48 reporting.",
        "boundary": "governance/navigation only",
    },
    {
        "artifact": "Active-time accounting audit card freshness linter",
        "path": "scripts/v48_active_time_accounting_audit_freshness_linter.py",
        "summary": "analysis/v48_active_time_accounting_audit_freshness_linter/active_time_accounting_audit_freshness_lint_summary.json",
        "purpose": "Ensures the active-time accounting audit keeps timing rules, audit checks, links, and operational-only boundary language.",
        "boundary": "governance/navigation only",
    },
    {
        "artifact": "Relationship-row candidate template",
        "path": "knowledge_external/templates/RELATIONSHIP_ROW_CANDIDATE_TEMPLATE_V48.md",
        "summary": "knowledge_external/catalogs/indexes/relationship_row_candidate_template_v48_summary.json",
        "purpose": "Draft template for future candidate convergence/contradiction rows before matrix acceptance.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Relationship-row candidate template freshness linter",
        "path": "scripts/v48_relationship_row_candidate_template_freshness_linter.py",
        "summary": "analysis/v48_relationship_row_candidate_template_freshness_linter/relationship_row_candidate_template_freshness_lint_summary.json",
        "purpose": "Ensures the relationship-row candidate template keeps required fields, candidate statuses, forbidden shortcuts, and promotion rules.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Contradiction triage mini-template",
        "path": "knowledge_external/templates/CONTRADICTION_TRIAGE_MINI_TEMPLATE_V48.md",
        "summary": "knowledge_external/catalogs/indexes/contradiction_triage_mini_template_v48_summary.json",
        "purpose": "Compact safe-routing template for future source hits that appear to disagree with grounded findings.",
        "boundary": "future-search control",
    },
    {
        "artifact": "Contradiction triage mini-template freshness linter",
        "path": "scripts/v48_contradiction_triage_mini_template_freshness_linter.py",
        "summary": "analysis/v48_contradiction_triage_mini_template_freshness_linter/contradiction_triage_mini_template_freshness_lint_summary.json",
        "purpose": "Ensures the contradiction triage mini-template keeps required controls, triage questions, safe outcomes, and no-override language.",
        "boundary": "future-search control",
    },
    {
        "artifact": "External claim-length safety linter",
        "path": "scripts/v48_external_claim_length_linter.py",
        "summary": "analysis/v48_external_claim_length_linter/external_claim_length_lint_summary.json",
        "purpose": "Prevents oversized external claim summaries or excerpt-like fields from entering external records.",
        "boundary": "copyright/provenance hygiene control",
    },
    {
        "artifact": "Support/contradiction coverage linter",
        "path": "scripts/v48_support_contradiction_coverage_linter.py",
        "summary": "analysis/v48_support_contradiction_coverage_linter/support_contradiction_coverage_lint_summary.json",
        "purpose": "Ensures support/contradiction records appear in the V48 matrix.",
        "boundary": "synthesis coverage control",
    },
    {
        "artifact": "Relationship-matrix data dictionary freshness linter",
        "path": "scripts/v48_relationship_matrix_data_dictionary_freshness_linter.py",
        "summary": "analysis/v48_relationship_matrix_data_dictionary_freshness_linter/relationship_matrix_data_dictionary_freshness_lint_summary.json",
        "purpose": "Ensures the V48 relationship-matrix data dictionary matches the current matrix header and controlled vocabularies.",
        "boundary": "schema control",
    },
    {
        "artifact": "Contradiction-intake linter",
        "path": "scripts/v48_contradiction_intake_linter.py",
        "summary": "analysis/v48_contradiction_intake_linter/contradiction_intake_lint_summary.json",
        "purpose": "Ensures future contradiction records remain queued for grounding.",
        "boundary": "future-grounding control",
    },
    {
        "artifact": "Contradiction readiness freshness linter",
        "path": "scripts/v48_contradiction_readiness_freshness_linter.py",
        "summary": "analysis/v48_contradiction_readiness_freshness_linter/contradiction_readiness_freshness_lint_summary.json",
        "purpose": "Ensures contradiction readiness playbook counts and stages match the current matrix.",
        "boundary": "future-grounding control",
    },
    {
        "artifact": "Contradiction surveillance freshness linter",
        "path": "scripts/v48_contradiction_surveillance_freshness_linter.py",
        "summary": "analysis/v48_contradiction_surveillance_freshness_linter/contradiction_surveillance_freshness_lint_summary.json",
        "purpose": "Ensures the contradiction surveillance checklist matches current matrix rows and high-priority sourcing plan rows.",
        "boundary": "future-grounding control",
    },
    {
        "artifact": "Unresolved external coverage handoff",
        "path": "knowledge_external/synthesis/UNRESOLVED_EXTERNAL_COVERAGE_HANDOFF_V48.md",
        "summary": "knowledge_external/catalogs/indexes/unresolved_external_coverage_handoff_v48_summary.json",
        "purpose": "Consolidated unresolved source-search, source-acceptance, future-grounding, and surveillance actions.",
        "boundary": "queued tasks are not findings",
    },
    {
        "artifact": "Unresolved external coverage handoff freshness linter",
        "path": "scripts/v48_unresolved_external_coverage_handoff_freshness_linter.py",
        "summary": "analysis/v48_unresolved_external_coverage_handoff_freshness_linter/unresolved_external_coverage_handoff_freshness_lint_summary.json",
        "purpose": "Ensures the unresolved external coverage handoff matches current source-search, future-grounding, and surveillance inputs.",
        "boundary": "handoff/navigation control",
    },
    {
        "artifact": "Source-domain review freshness linter",
        "path": "scripts/v48_source_domain_review_freshness_linter.py",
        "summary": "analysis/v48_source_domain_review_freshness_linter/source_domain_review_freshness_lint_summary.json",
        "purpose": "Ensures the source-domain review matches current external records.",
        "boundary": "domain review control",
    },
    {
        "artifact": "Source-domain relationship freshness linter",
        "path": "scripts/v48_source_domain_relationship_freshness_linter.py",
        "summary": "analysis/v48_source_domain_relationship_freshness_linter/source_domain_relationship_freshness_lint_summary.json",
        "purpose": "Ensures the source-domain relationship rollup matches current external records and V48 matrix rows.",
        "boundary": "domain relationship control",
    },
    {
        "artifact": "Source-domain independence freshness linter",
        "path": "scripts/v48_source_domain_independence_freshness_linter.py",
        "summary": "analysis/v48_source_domain_independence_freshness_linter/source_domain_independence_freshness_lint_summary.json",
        "purpose": "Ensures the source-domain independence rollup matches the current row-level source-independence matrix.",
        "boundary": "domain relationship control",
    },
    {
        "artifact": "Source URL duplicate freshness linter",
        "path": "scripts/v48_source_url_duplicate_freshness_linter.py",
        "summary": "analysis/v48_source_url_duplicate_freshness_linter/source_url_duplicate_freshness_lint_summary.json",
        "purpose": "Ensures the source URL duplicate review matches current external source records.",
        "boundary": "source maintenance control",
    },
    {
        "artifact": "External synthesis dependency freshness linter",
        "path": "scripts/v48_external_synthesis_dependency_freshness_linter.py",
        "summary": "analysis/v48_external_synthesis_dependency_freshness_linter/external_synthesis_dependency_freshness_lint_summary.json",
        "purpose": "Ensures the external synthesis dependency graph matches current generator-declared artifacts, inputs, controls, and counts.",
        "boundary": "dependency/navigation control",
    },
    {
        "artifact": "Evidence-boundary glossary freshness linter",
        "path": "scripts/v48_evidence_boundary_glossary_freshness_linter.py",
        "summary": "analysis/v48_evidence_boundary_glossary_freshness_linter/evidence_boundary_glossary_freshness_lint_summary.json",
        "purpose": "Ensures the evidence-boundary glossary matches the current governance failure-mode matrix.",
        "boundary": "vocabulary control",
    },
    {
        "artifact": "V37 external-coverage freshness linter",
        "path": "scripts/v48_v37_coverage_freshness_linter.py",
        "summary": "analysis/v48_v37_coverage_freshness_linter/v37_coverage_freshness_lint_summary.json",
        "purpose": "Ensures the V37 scored-finding coverage map matches current V37 scores and V48 matrix rows.",
        "boundary": "synthesis coverage control",
    },
    {
        "artifact": "V37 uncovered-rationale freshness linter",
        "path": "scripts/v48_v37_uncovered_rationale_freshness_linter.py",
        "summary": "analysis/v48_v37_uncovered_rationale_freshness_linter/v37_uncovered_rationale_freshness_lint_summary.json",
        "purpose": "Ensures the V37 uncovered-finding rationale table matches the current coverage map.",
        "boundary": "synthesis coverage control",
    },
    {
        "artifact": "V37 external gap-priority freshness linter",
        "path": "scripts/v48_v37_gap_priority_freshness_linter.py",
        "summary": "analysis/v48_v37_gap_priority_freshness_linter/v37_gap_priority_freshness_lint_summary.json",
        "purpose": "Ensures the V37 external coverage gap priority map matches current coverage and rationale inputs.",
        "boundary": "sourcing priority control",
    },
    {
        "artifact": "Decision-relevant convergence freshness linter",
        "path": "scripts/v48_decision_relevant_convergence_freshness_linter.py",
        "summary": "analysis/v48_decision_relevant_convergence_freshness_linter/decision_relevant_convergence_freshness_lint_summary.json",
        "purpose": "Ensures the decision-relevant convergence shortlist matches current converges/contradicts matrix rows.",
        "boundary": "synthesis coverage control",
    },
    {
        "artifact": "Convergence source-independence freshness linter",
        "path": "scripts/v48_convergence_source_independence_freshness_linter.py",
        "summary": "analysis/v48_convergence_source_independence_freshness_linter/convergence_source_independence_freshness_lint_summary.json",
        "purpose": "Ensures source-independence accounting matches current V48 convergence matrix rows.",
        "boundary": "synthesis coverage control",
    },
    {
        "artifact": "Convergence matrix coverage linter",
        "path": "scripts/v48_convergence_matrix_coverage_linter.py",
        "summary": "analysis/v48_convergence_matrix_coverage_linter/convergence_matrix_coverage_lint_summary.json",
        "purpose": "Ensures priority grounded findings remain represented in the V48 matrix.",
        "boundary": "synthesis coverage control",
    },
    {
        "artifact": "Convergence status vocabulary linter",
        "path": "scripts/v48_convergence_status_vocabulary_linter.py",
        "summary": "analysis/v48_convergence_status_vocabulary_linter/convergence_status_vocabulary_lint_summary.json",
        "purpose": "Checks controlled relationship/status vocabulary in the V48 matrix.",
        "boundary": "vocabulary control",
    },
    {
        "artifact": "Future-grounding queue freshness linter",
        "path": "scripts/v48_future_grounding_queue_freshness_linter.py",
        "summary": "analysis/v48_future_grounding_queue_freshness_linter/future_grounding_queue_freshness_lint_summary.json",
        "purpose": "Ensures matrix follow-up actions are represented in the future-grounding queue.",
        "boundary": "future-grounding control",
    },
    {
        "artifact": "Project-finding reference linter",
        "path": "scripts/v48_project_finding_reference_linter.py",
        "summary": "analysis/v48_project_finding_reference_linter/project_finding_reference_lint_summary.json",
        "purpose": "Checks external support/contradiction records point to existing project finding artifacts.",
        "boundary": "synthesis reference control",
    },
    {
        "artifact": "Resource comparator freshness linter",
        "path": "scripts/v48_resource_comparator_freshness_linter.py",
        "summary": "analysis/v48_resource_comparator_freshness_linter/resource_comparator_freshness_lint_summary.json",
        "purpose": "Ensures the resource comparator matrix matches current external resource records.",
        "boundary": "resource metadata control",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    return parser.parse_args()


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return data if isinstance(data, dict) else {}


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build(root: Path) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for item in ARTIFACTS:
        artifact_path = root / str(item["path"])
        summary_path = root / str(item["summary"])
        summary = read_json(summary_path)
        rows.append(
            {
                "artifact": item["artifact"],
                "path": item["path"],
                "exists": "yes" if artifact_path.exists() else "no",
                "purpose": item["purpose"],
                "boundary": item["boundary"],
                "summary": item["summary"],
                "summary_exists": "yes" if summary_path.exists() else "no",
                "overall_status": summary.get("overall_status", "not_applicable"),
                "n_fail": summary.get("n_fail", "not_applicable"),
            }
        )
    outdir = root / "knowledge_external/catalogs/indexes"
    fields = ["artifact", "path", "exists", "purpose", "boundary", "summary", "summary_exists", "overall_status", "n_fail"]
    write_tsv(outdir / "v48_governance_navigation.tsv", rows, fields)
    n_missing = sum(1 for row in rows if row["exists"] != "yes")
    n_summary_fail = sum(1 for row in rows if str(row["n_fail"]) not in {"0", "not_applicable"})
    summary = {
        "purpose": "V48 governance navigation; external-knowledge controls only; no biological claim",
        "n_artifacts": len(rows),
        "n_missing_artifacts": n_missing,
        "n_summaries_with_failures": n_summary_fail,
        "overall_status": "PASS" if n_missing == 0 and n_summary_fail == 0 else "FAIL",
        "markdown": "knowledge_external/catalogs/indexes/V48_GOVERNANCE_NAVIGATION.md",
        "tsv": "knowledge_external/catalogs/indexes/v48_governance_navigation.tsv",
    }
    (outdir / "v48_governance_navigation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Governance Navigation",
        "",
        "Status: external-knowledge governance/navigation only. These controls keep external context separate from grounded findings; they do not validate external claims.",
        "",
        f"- artifacts tracked: `{summary['n_artifacts']}`",
        f"- missing artifacts: `{summary['n_missing_artifacts']}`",
        f"- summaries with failures: `{summary['n_summaries_with_failures']}`",
        "",
        "## Controls",
        "",
        "| artifact | exists | status | purpose | boundary | path |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row['artifact']} | "
            f"`{row['exists']}` | "
            f"`{row['overall_status']}` | "
            f"{row['purpose']} | "
            f"{row['boundary']} | "
            f"`{row['path']}` |"
        )
    lines.extend(
        [
            "",
            "## Use",
            "",
            "- Run the listed linters after adding or editing external records.",
            "- A PASS means the provenance/navigation control passed; it is not biological evidence.",
            "- Grounded project findings remain in the normal project report/history/validation trees.",
            "",
        ]
    )
    (outdir / "V48_GOVERNANCE_NAVIGATION.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    summary = build(args.root.resolve())
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
