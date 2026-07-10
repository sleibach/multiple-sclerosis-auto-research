# Therapeutic Path Summary Card V52

Date: 2026-07-10

Status: public-facing synthesis. This card summarizes committed V52 artifacts;
it does not add evidence, change locked rules, or reopen discovery.

## One-Sentence Bottom Line

The project’s most defensible near-term MS impact is **validation of an early
treatment-response monitoring / stratification signal**, not a direct
therapeutic target.

## What Is Closest To Actionable

| route | current status | actionability condition |
|---|---|---|
| Bounded APC/HLA-II early DMF-like monitoring scalar | provisional, internally robust, confounder-audited | Run the frozen V42/V44 harness on Gafson/Karolinska-style paired PBMC/NEDA data. A clean or immune-tone-bounded pass would support an early pharmacodynamic monitoring readout. |
| chr1 KIF21B/GPR25 biology | real shared MS-UC locus, not target-ready | Acquire genotype-linked immune/CSF expression or protein data that resolves causal gene, cell type, and protective direction. |
| PTGER4 | closed naive transfer target | Reopen only with signal-specific fine-mapping/QTL and MS-safe direction evidence; AlphaFold receptor context does not rescue it. |
| ZMIZ1 | transfer-validity warning | Use as a cross-disease transfer guardrail; restored OpenGWAS can polish the direction table but does not make it a target. |

## What V52 Added

- Verified renewed OpenGWAS access: POST-only checker returned HTTP 200; token
  expiry decoded as `2026-07-24 08:00 UTC`.
- Wrote the full therapeutic-path report:
  `docs/reports/THERAPEUTIC_PATH_V52.md`.
- Wrote the V52 therapeutic artifact index:
  `docs/reports/THERAPEUTIC_PATH_INDEX_V52.md`.
- Wrote the V52 therapeutic artifact manifest:
  `docs/reports/THERAPEUTIC_ARTIFACT_MANIFEST_V52.tsv`.
- Wrote the V52 artifact cross-link audit:
  `docs/reports/V52_ARTIFACT_CROSS_LINK_AUDIT.md`.
- Refreshed the local sparse knowledge index and updated:
  `knowledge/tools/RAG_STATUS.md`.
- Wrote V52 operator artifact hash snapshot:
  `docs/reports/V52_OPERATOR_ARTIFACT_HASH_SNAPSHOT.tsv`.
- Wrote V52 operator artifact hash verification command note:
  `docs/reports/V52_OPERATOR_ARTIFACT_HASH_VERIFY_COMMANDS.md`.
- Wrote the V52 therapeutic route status dashboard:
  `docs/reports/THERAPEUTIC_ROUTE_STATUS_DASHBOARD_V52.tsv`.
- Wrote the machine-readable target evidence matrix:
  `docs/reports/THERAPEUTIC_TARGET_EVIDENCE_MATRIX_V52.tsv`.
- Wrote therapeutic reviewer quickstart:
  `docs/reports/THERAPEUTIC_REVIEWER_QUICKSTART_V52.md`.
- Wrote therapeutic no-target public abstract:
  `docs/reports/THERAPEUTIC_NO_TARGET_PUBLIC_ABSTRACT_V52.md`.
- Wrote the structural evidence-boundary QA:
  `docs/reports/STRUCTURAL_EVIDENCE_BOUNDARY_QA_V52.md`.
- Added KIF21B and PTGER4 AlphaFold DB structural records under the segregated
  external structural layer.
- Wrote validation handoff:
  `docs/validation/THERAPEUTIC_VALIDATION_HANDOFF_V52.md`.
- Wrote prospective monitoring utility study sketch:
  `docs/validation/PROSPECTIVE_MONITORING_UTILITY_STUDY_SKETCH_V52.md`.
- Wrote monitoring clinical-utility boundary checklist:
  `docs/validation/MONITORING_CLINICAL_UTILITY_BOUNDARY_CHECKLIST_V52.md`.
- Wrote monitoring public wording table:
  `docs/validation/MONITORING_PUBLIC_WORDING_TABLE_V52.tsv`.
- Wrote monitoring result-class examples:
  `docs/validation/MONITORING_RESULT_CLASS_EXAMPLES_V52.md`.
- Wrote incoming-package communication templates:
  `docs/validation/INCOMING_PACKAGE_COMMUNICATION_TEMPLATES_V52.md`.
- Wrote package checksum intake checklist:
  `docs/validation/PACKAGE_CHECKSUM_INTAKE_CHECKLIST_V52.md`.
- Wrote monitoring validation result-report template:
  `docs/validation/MONITORING_VALIDATION_RESULT_REPORT_TEMPLATE_V52.md`.
- Wrote monitoring operator one-page card:
  `docs/validation/MONITORING_OPERATOR_ONE_PAGE_CARD_V52.md`.
- Wrote monitoring minimum viable package checklist:
  `docs/validation/MONITORING_MINIMUM_VIABLE_PACKAGE_CHECKLIST_V52.md`.
- Wrote a sendable medical-team request packet:
  `docs/validation/MEDICAL_TEAM_THERAPEUTIC_DATA_REQUEST_V52.md`.
- Wrote validation package field dictionary:
  `docs/validation/VALIDATION_PACKAGE_FIELD_DICTIONARY_V52.tsv`.
- Wrote validation package route classifier:
  `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv`.
- Wrote validation package route classifier examples:
  `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_EXAMPLES_V52.tsv`.
- Wrote incoming package preflight checklist:
  `docs/validation/INCOMING_PACKAGE_PREFLIGHT_CHECKLIST_V52.md`.
- Wrote therapeutic package handoff bundle index:
  `docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md`.
- Wrote bounded genetics handoff:
  `docs/workups/genetics/ZMIZ1_RESTORED_OPENGWAS_HANDOFF_V52.md`.
- Wrote bounded OpenGWAS pre-expiry command list:
  `docs/workups/genetics/OPENGWAS_PRE_EXPIRY_BOUNDED_POLISH_COMMANDS_V52.md`.
- Wrote OpenGWAS expiry-day runbook:
  `meta/OPENGWAS_EXPIRY_DAY_RUNBOOK_V52.md`.
- Wrote chr1 collaborator assay request appendix:
  `docs/workups/genetics/CHR1_COLLABORATOR_ASSAY_REQUEST_APPENDIX_V52.md`.
- Wrote chr1 no-go communication appendix:
  `docs/workups/genetics/CHR1_NO_GO_COMMUNICATION_APPENDIX_V52.md`.
- Wrote chr1 package result-report template:
  `docs/workups/genetics/CHR1_PACKAGE_RESULT_REPORT_TEMPLATE_V52.md`.
- Wrote chr1 operator one-page card:
  `docs/workups/genetics/CHR1_OPERATOR_ONE_PAGE_CARD_V52.md`.
- Wrote chr1 wrong-direction control checklist:
  `docs/workups/genetics/CHR1_WRONG_DIRECTION_CONTROL_CHECKLIST_V52.md`.
- Wrote chr1 target-resolution decision compact:
  `docs/workups/genetics/CHR1_TARGET_RESOLUTION_DECISION_COMPACT_V52.tsv`.
- Wrote therapeutic route risk register:
  `docs/reports/THERAPEUTIC_ROUTE_RISK_REGISTER_V52.md`.
- Wrote therapeutic route assumption ledger:
  `docs/reports/THERAPEUTIC_ROUTE_ASSUMPTION_LEDGER_V52.md`.
- Wrote therapeutic route decision-log template:
  `docs/reports/THERAPEUTIC_ROUTE_DECISION_LOG_TEMPLATE_V52.md`.
- Wrote post-validation route update playbook:
  `docs/reports/POST_VALIDATION_ROUTE_UPDATE_PLAYBOOK_V52.md`.
- Rechecked therapeutic external-context convergence:
  `knowledge_external/synthesis/V52_THERAPEUTIC_CONVERGENCE_CONTRADICTION.md`;
  no genuine therapeutic contradiction surfaced.

## What Structure Changed

Structure made the tractability discussion sharper, not more permissive.

- GPR25: GPCR-like structural context is compatible with receptor tractability,
  but causal-gene uncertainty, weak MS cell-state support, immature chemical
  matter, and required agonism/restoration remain blockers.
- KIF21B: motor/binding-site regions are structurally interpretable, but the
  genetics-facing direction is restoration/up-function; generic inhibition,
  degradation, or knockdown is likely wrong-direction.
- PTGER4: receptor-core context is expected for an EP4 receptor, but the closure
  is caused by mixed signal and direction conflict, not structural intractability.

Predicted structures remain context only and are not project-grounded evidence.

## What The Medical Team Should Ask For Next

Primary validation package:

1. Paired baseline and early on-treatment PBMC expression.
2. Subject-level NEDA-4 or pre-specified equivalent response labels.
3. Feature annotation sufficient for V22 module scoring.
4. Batch/QC metadata.
5. Steroid, relapse, infection, DMT timing, and cell-count metadata where
   available.
6. Preferably at least `30` responders and `30` nonresponders if the cohort is
   intended to settle the rule rather than estimate effect size.

Target-development package, if target work remains a priority:

1. Genotype-linked immune or CSF single-cell expression/protein data for the
   chr1 haplotype.
2. Perturbation readout for the resolved causal gene.
3. A modality that moves in the genetically protective direction.

Concrete field specification:
`docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md`.

## What Not To Do

- Do not spend wet-lab budget on GPR25, KIF21B, PTGER4, or ZMIZ1 as
  intervention-grade MS targets from current evidence.
- Do not treat AlphaFold confidence as disease evidence.
- Do not tune the V22 scalar on Gafson/Karolinska.
- Do not convert an underpowered validation into a pass or kill.
- Do not use external literature context as validation of the locked scalar.

## Source Artifacts

- `docs/reports/THERAPEUTIC_PATH_V52.md`
- `docs/reports/THERAPEUTIC_PATH_INDEX_V52.md`
- `docs/reports/THERAPEUTIC_ARTIFACT_MANIFEST_V52.tsv`
- `docs/reports/V52_ARTIFACT_CROSS_LINK_AUDIT.md`
- `knowledge/tools/RAG_STATUS.md`
- `docs/reports/V52_OPERATOR_ARTIFACT_HASH_SNAPSHOT.tsv`
- `docs/reports/V52_OPERATOR_ARTIFACT_HASH_VERIFY_COMMANDS.md`
- `docs/reports/THERAPEUTIC_ROUTE_STATUS_DASHBOARD_V52.tsv`
- `docs/reports/THERAPEUTIC_TARGET_EVIDENCE_MATRIX_V52.tsv`
- `docs/reports/THERAPEUTIC_REOPEN_CHECKLIST_V52.tsv`
- `docs/reports/THERAPEUTIC_SKEPTIC_REBUTTAL_CHECKLIST_V52.md`
- `docs/reports/THERAPEUTIC_REVIEWER_QUICKSTART_V52.md`
- `docs/reports/THERAPEUTIC_NO_TARGET_PUBLIC_ABSTRACT_V52.md`
- `docs/reports/THERAPEUTIC_ARTIFACT_CONSISTENCY_AUDIT_V52.md`
- `docs/reports/THERAPEUTIC_CLAIM_HIERARCHY_V52.md`
- `docs/reports/THERAPEUTIC_ROUTE_RISK_REGISTER_V52.md`
- `docs/reports/THERAPEUTIC_ROUTE_ASSUMPTION_LEDGER_V52.md`
- `docs/reports/THERAPEUTIC_ROUTE_DECISION_LOG_TEMPLATE_V52.md`
- `docs/reports/POST_VALIDATION_ROUTE_UPDATE_PLAYBOOK_V52.md`
- `docs/reports/STRUCTURAL_EVIDENCE_BOUNDARY_QA_V52.md`
- `docs/reports/THERAPEUTIC_CONTRADICTION_SURVEILLANCE_V52.md`
- `docs/validation/THERAPEUTIC_VALIDATION_HANDOFF_V52.md`
- `docs/validation/MEDICAL_TEAM_THERAPEUTIC_DATA_REQUEST_V52.md`
- `docs/validation/TARGET_PACKAGE_ACCEPTANCE_CRITERIA_V52.tsv`
- `docs/validation/VALIDATION_PACKAGE_FIELD_DICTIONARY_V52.tsv`
- `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv`
- `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_EXAMPLES_V52.tsv`
- `docs/validation/INCOMING_PACKAGE_PREFLIGHT_CHECKLIST_V52.md`
- `docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md`
- `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md`
- `docs/validation/MONITORING_VALIDATION_COMMAND_MANIFEST_V52.md`
- `docs/validation/MONITORING_VALIDATION_RESULT_REPORT_TEMPLATE_V52.md`
- `docs/validation/MONITORING_OPERATOR_ONE_PAGE_CARD_V52.md`
- `docs/validation/MONITORING_MINIMUM_VIABLE_PACKAGE_CHECKLIST_V52.md`
- `docs/validation/PROSPECTIVE_MONITORING_UTILITY_STUDY_SKETCH_V52.md`
- `docs/validation/MONITORING_CLINICAL_UTILITY_BOUNDARY_CHECKLIST_V52.md`
- `docs/validation/MONITORING_PUBLIC_WORDING_TABLE_V52.tsv`
- `docs/validation/MONITORING_RESULT_CLASS_EXAMPLES_V52.md`
- `docs/validation/INCOMING_PACKAGE_COMMUNICATION_TEMPLATES_V52.md`
- `docs/validation/PACKAGE_CHECKSUM_INTAKE_CHECKLIST_V52.md`
- `docs/workups/genetics/RESTORED_OPENGWAS_CATCHUP_V52.md`
- `docs/workups/genetics/RESTORED_OPENGWAS_BOUNDED_RERUN_MANIFEST_V52.md`
- `docs/workups/genetics/OPENGWAS_PRE_EXPIRY_BOUNDED_POLISH_COMMANDS_V52.md`
- `meta/OPENGWAS_EXPIRY_DAY_RUNBOOK_V52.md`
- `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md`
- `docs/workups/genetics/CHR1_DIRECTION_MATCHED_EXPERIMENT_BLUEPRINT_V52.md`
- `docs/workups/genetics/CHR1_COLLABORATOR_ASSAY_REQUEST_APPENDIX_V52.md`
- `docs/workups/genetics/CHR1_NO_GO_COMMUNICATION_APPENDIX_V52.md`
- `docs/workups/genetics/CHR1_PACKAGE_RESULT_REPORT_TEMPLATE_V52.md`
- `docs/workups/genetics/CHR1_OPERATOR_ONE_PAGE_CARD_V52.md`
- `docs/workups/genetics/CHR1_WRONG_DIRECTION_CONTROL_CHECKLIST_V52.md`
- `docs/workups/genetics/CHR1_TARGET_RESOLUTION_DECISION_COMPACT_V52.tsv`
- `docs/workups/genetics/STRUCTURE_AWARE_NO_GO_TABLE_V52.md`
- `docs/workups/genetics/GPR25_DIRECTION_MATCHED_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/KIF21B_RESTORATION_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/PTGER4_SIGNAL_SPECIFIC_REOPEN_SPEC_V52.md`
- `docs/workups/genetics/ZMIZ1_RESTORED_OPENGWAS_HANDOFF_V52.md`
- `knowledge_external/synthesis/V51_GPR25_ALPHAFOLD_DRUGGABILITY_CONTEXT.md`
- `knowledge_external/synthesis/V52_KIF21B_ALPHAFOLD_DRUGGABILITY_CONTEXT.md`
- `knowledge_external/synthesis/V52_PTGER4_ALPHAFOLD_DRUGGABILITY_CONTEXT.md`
