# V49 Artifact Manifest

Status: operational manifest. This lists new files added during V49 and their
boundary class so reviewers can find the right artifacts without confusing
navigation/source-context outputs with grounded evidence.

## Summary

- new V49 files listed: `51`
- segregated source-context records: `8`
- external synthesis/catalog/navigation files: `34`
- reproducibility scripts: `2`
- generated source-navigation summaries: `2`
- operational meta files: `5`
- grounded finding or locked-rule files added: `0`

## New Files

| path | boundary class | purpose |
|---|---|---|
| `knowledge_external/records/ebv_ms_longitudinal_risk_context.json` | segregated source-context record | EBV/MS risk context record used for insufficient-overlap review. |
| `knowledge_external/records/gpr25_ms_ibd_shared_genetics_context.json` | segregated source-context record | GPR25/MS/IBD context record used for demotion review. |
| `knowledge_external/records/ibd_tofacitinib_mhc_stat1_context.json` | segregated source-context record | UC tofacitinib/MHC/STAT1 context record used for convergence-context review. |
| `knowledge_external/records/method_prediction_model_validation_context.json` | segregated source-context record | Prediction-model validation methods context. |
| `knowledge_external/records/method_target_direction_tractability_context.json` | segregated source-context record | Target direction/tractability methods context. |
| `knowledge_external/records/mhc_ms_finemapping_independent_effects_context.json` | segregated source-context record | MHC fine-mapping context record. |
| `knowledge_external/records/ms_biomarker_heterogeneity_context.json` | segregated source-context record | MS biomarker heterogeneity context record. |
| `knowledge_external/records/ra_sle_pregnancy_transcriptome_context.json` | segregated source-context record | RA/SLE pregnancy transcriptome context record. |
| `scripts/v49_insufficient_overlap_triage.py` | reproducibility script | Builds V49 insufficient-overlap triage outputs. |
| `scripts/v49_uncovered_finding_triage.py` | reproducibility script | Builds V49 uncovered-finding triage outputs. |
| `knowledge_external/catalogs/indexes/v49_insufficient_overlap_triage_summary.json` | generated source-navigation summary | Machine-readable summary for insufficient-overlap triage. |
| `knowledge_external/synthesis/V49_INSUFFICIENT_OVERLAP_TRIAGE.md` | external synthesis/navigation | Actionability triage for insufficient-overlap rows. |
| `knowledge_external/synthesis/v49_insufficient_overlap_triage.tsv` | external synthesis/navigation | Machine-readable insufficient-overlap triage table. |
| `knowledge_external/catalogs/indexes/v49_uncovered_finding_triage_summary.json` | generated source-navigation summary | Machine-readable summary for uncovered-finding triage. |
| `knowledge_external/synthesis/V49_UNCOVERED_FINDING_TRIAGE.md` | external synthesis/navigation | Triage of V37 findings still uncovered by relationship rows. |
| `knowledge_external/synthesis/v49_uncovered_finding_triage.tsv` | external synthesis/navigation | Machine-readable uncovered-finding triage table. |
| `knowledge_external/synthesis/V49_RELATIONSHIP_DELTA_NOTE.md` | external synthesis/navigation | Summary of relationship-matrix changes during V49. |
| `knowledge_external/synthesis/v49_relationship_delta_note.tsv` | external synthesis/navigation | Machine-readable relationship-delta table. |
| `knowledge_external/catalogs/indexes/V49_NEW_SOURCE_DOMAIN_REVIEW.md` | source maintenance/navigation | Access/terms review for eight V49-added source domains. |
| `knowledge_external/catalogs/indexes/v49_new_source_domain_review.tsv` | source maintenance/navigation | Machine-readable V49 source-domain review table. |
| `knowledge_external/synthesis/V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md` | future source-intake/navigation | Narrow import packets for ZMIZ1, chr1 KIF21B/GPR25, and coupled APC axis. |
| `knowledge_external/synthesis/v49_source_specific_import_packets.tsv` | future source-intake/navigation | Machine-readable source-specific import packet table. |
| `knowledge_external/synthesis/V49_VALIDATION_READY_ROW_CROSSCHECK.md` | external synthesis/navigation | Crosscheck that validation-facing rows are covered by frozen V42/V44 routes. |
| `knowledge_external/synthesis/v49_validation_ready_row_crosscheck.tsv` | external synthesis/navigation | Machine-readable validation-ready row crosscheck. |
| `knowledge_external/synthesis/V49_CONTEXT_ONLY_CLOSURE_GUARDRAIL.md` | external synthesis/navigation | Reopen-trigger guardrail for seven low-actionability rows. |
| `knowledge_external/synthesis/v49_context_only_closure_guardrail.tsv` | external synthesis/navigation | Machine-readable context-only closure table. |
| `knowledge_external/synthesis/V49_CONTENT_HANDOFF.md` | external synthesis/navigation | Medical-team handoff for V49 content changes. |
| `knowledge_external/synthesis/v49_content_handoff.tsv` | external synthesis/navigation | Machine-readable content handoff table. |
| `knowledge_external/synthesis/V49_IMPORT_PACKET_QUEUE_RECONCILIATION.md` | queue/navigation overlay | Maps generated future-grounding rows to V49 import-packet gates. |
| `knowledge_external/synthesis/v49_import_packet_queue_reconciliation.tsv` | queue/navigation overlay | Machine-readable import-packet queue reconciliation. |
| `knowledge_external/catalogs/indexes/V49_COMPARATOR_MATRIX_REVIEW.md` | source maintenance/navigation | Review showing V49 source domains do not require new comparator rows. |
| `knowledge_external/catalogs/indexes/v49_comparator_matrix_review.tsv` | source maintenance/navigation | Machine-readable comparator-matrix review. |
| `knowledge_external/synthesis/V49_CONTRADICTION_SURVEILLANCE_SHORTLIST.md` | future source-intake/navigation | Shortlist of rows where future same-definition sources could create real tension. |
| `knowledge_external/synthesis/v49_contradiction_surveillance_shortlist.tsv` | future source-intake/navigation | Machine-readable contradiction surveillance shortlist. |
| `knowledge_external/catalogs/indexes/V49_SOURCE_TERMS_FOLLOWUP.md` | source maintenance/navigation | Fuller-reuse terms/access follow-up for V49 records. |
| `knowledge_external/catalogs/indexes/v49_source_terms_followup.tsv` | source maintenance/navigation | Machine-readable source-terms follow-up table. |
| `knowledge_external/synthesis/V49_ZERO_CONTRADICTION_CAVEAT.md` | external synthesis/navigation | Caveat that zero current contradiction rows does not imply consensus. |
| `knowledge_external/synthesis/v49_zero_contradiction_caveat.tsv` | external synthesis/navigation | Machine-readable zero-contradiction caveat table. |
| `knowledge_external/catalogs/indexes/V49_ABSENT_RESOURCE_INTAKE_CANDIDATES.md` | future source-intake/navigation | Candidate resources absent from the current comparator matrix. |
| `knowledge_external/catalogs/indexes/v49_absent_resource_intake_candidates.tsv` | future source-intake/navigation | Machine-readable absent-resource candidate table. |
| `knowledge_external/synthesis/V49_UNRESOLVED_ACTION_RECONCILIATION.md` | queue/navigation overlay | Overlay reconciling V48 unresolved handoff rows after V49. |
| `knowledge_external/synthesis/v49_unresolved_action_reconciliation.tsv` | queue/navigation overlay | Machine-readable unresolved-action reconciliation. |
| `meta/V49_REWRITE_PUSH_HANDOFF.md` | operational meta | Human handoff for rewritten history push and clone re-sync. |
| `knowledge_external/synthesis/V49_SOURCE_INDEPENDENCE_DELTA.md` | external synthesis/navigation | Source-cluster accounting for V49 convergence/context rows. |
| `knowledge_external/synthesis/v49_source_independence_delta.tsv` | external synthesis/navigation | Machine-readable source-independence delta table. |
| `knowledge_external/synthesis/V49_READER_QUICKSTART.md` | navigation | Question-to-artifact routing guide for V49 outputs. |
| `knowledge_external/synthesis/v49_reader_quickstart.tsv` | navigation | Machine-readable reader quickstart table. |
| `meta/V49_GROUNDED_INDEX_BOUNDARY_CHECK.md` | operational meta | Confirms V49 external artifacts are excluded from grounded TF-IDF index. |
| `meta/V49_RESUME_CHECKPOINT.md` | operational meta | Resume card with current state, open tasks, and next action. |
| `meta/V49_ARTIFACT_MANIFEST.md` | operational meta | Boundary-class manifest for V49-added files. |
| `meta/V49_PURGED_ARTIFACT_REFERENCE_AUDIT.md` | operational meta | Audit of remaining references to purged large/cache/generated artifacts. |

## Modified Existing Files Of Note

- `meta/V49_QUEUE.md`: live V49 active-time and backlog state.
- `knowledge_external/INDEX.md`: class-aware public navigation links for V49
  artifacts.
- generated linter/preflight outputs under `analysis/v47_*` and
  `analysis/v48_*`: verification trail for the external layer.
- `.gitignore`: rewritten-history state includes V49 large-file recurrence
  protections from the Phase 0 hygiene work.

## Boundary

No file in this manifest is a new grounded finding or locked rule. V49's new
source-context records and synthesis outputs live in the segregated external
layer or in operational metadata.
