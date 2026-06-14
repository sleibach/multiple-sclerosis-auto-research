# V49 Insufficient-Overlap Triage

Status: synthesis/navigation only. This document classifies existing insufficient-overlap rows so future work does not mistake context for corroboration.

Boundary: rows here remain not corroborated by the paired external source. A listed next test is a future route, not a finding, and no grounded project conclusion is changed.

## Summary

- insufficient-overlap rows triaged: `16`
- high actionability rows: `4`
- medium actionability rows: `5`
- low actionability rows: `7`

## Actionability Classes

| actionability | class | count |
|---|---|---:|
| `low` | `closed_unless_direction_and_tractability_evidence_arrive` | 1 |
| `low` | `closed_unless_new_perturbation_validation_data_arrive` | 1 |
| `low` | `closed_unless_preregistered_external_comparison_arrives` | 1 |
| `low` | `closed_unless_same_failure_mode_dataset_arrives` | 1 |
| `low` | `closed_unless_signal_specific_data_arrive` | 1 |
| `low` | `closed_until_null_tested_invariant_candidate_exists` | 1 |
| `low` | `context_only_until_ms_or_ra_response_transfer_data` | 1 |
| `medium` | `needs_compartment_resolved_response_data` | 1 |
| `medium` | `needs_crohn_response_data` | 1 |
| `medium` | `needs_ebv_stratified_expression_with_specificity_controls` | 1 |
| `medium` | `needs_true_postpartum_ms_trajectory` | 1 |
| `high` | `ready_when_blind_validation_data_arrive` | 1 |
| `medium` | `source_specific_import_before_comparison` | 3 |
| `high` | `validation_guardrail_already_preregistered` | 1 |

## Rows

| finding | external record | actionability | triage class | next test | required input | reason |
|---|---|---|---|---|---|---|
| Bounded APC/HLA-II early treatment-response monitoring scalar | `claim.dailymed.dimethyl_fumarate_mechanism_context.2026-06-13` | `high` | `ready_when_blind_validation_data_arrive` | Run the frozen V42/V44 validation harness on paired labeled DMF or immune-remodeling/JAK-STAT response data. | Paired baseline/early-treatment transcriptomes, response labels, module genes, and predeclared batch/confounder metadata. | The external treatment label is not validation, but the project already has a frozen harness for the exact future test. |
| V22 scalar is immune-tone bounded, not steroid/composition artifact | `claim.dailymed.dimethyl_fumarate_mechanism_context.2026-06-13` | `high` | `validation_guardrail_already_preregistered` | Apply the V42/V44 confounder and batch diagnostics alongside the frozen scalar in the validation cohort. | Validation cohort with enough expression coverage to score steroid, cell-composition, metabolic, STAT1/immune-tone, and batch diagnostics. | This row is not externally corroborated, but it is already converted into a mechanical validation guardrail. |
| Coupled APC remodeling architecture | `resource.msgd.database_commons.2026-06-13` | `medium` | `source_specific_import_before_comparison` | Import source-specific CD74, MIF, HLA, IFN/APC, and APC-axis records before comparing against V26. | Specific external records or datasets with source snapshots, not resource-level metadata. | Resource metadata cannot corroborate architecture; only source-specific axis records can be compared. |
| T/B-readable early IFN/APC/STAT1 monitoring state | `claim.dailymed.ocrelizumab_mechanism_context.2026-06-13` | `medium` | `needs_compartment_resolved_response_data` | Run the pre-registered T/B-compartment monitoring harness on paired response data with compartment-resolved or deconvolved readouts. | Paired treatment-response data with T/B compartment signal or defensible deconvolution. | A CD20 therapy label is not a monitoring-state validation; the row becomes testable only with compartment-resolved response data. |
| Postpartum HLA-II/CD64 APC-arm imbalance | `claim.national_ms_society.rrms_course_context.2026-06-13` | `medium` | `needs_true_postpartum_ms_trajectory` | Test HLA-II-minus-CD64 APC-arm trajectory against postpartum relapse-window timing in MS. | MS pregnancy/postpartum immune trajectory data with relapse-window timing and APC readouts. | General RRMS course context is not postpartum APC evidence; the missing data type is specific and already defined. |
| ZMIZ1 opposite-direction MS/Crohn decoupling | `resource.disgenet.platform.2026-06-13` | `high` | `source_specific_import_before_comparison` | Import specific ZMIZ1 disease-gene, variant, QTL, or direction records, then compare to the project's MS/Crohn directionality. | Source-specific ZMIZ1 records with disease, direction, variant/gene mapping, and source snapshots. | The current DisGeNET row is only resource metadata; source-specific ZMIZ1 direction records are readily definable. |
| chr1 KIF21B/GPR25 locus resolves to real biology but hard target | `resource.gwas_catalog.ms.2026-06-13` | `high` | `source_specific_import_before_comparison` | Import specific GWAS Catalog or fine-mapping association records for KIF21B/GPR25 and compare direction/tractability to V19. | Signal-specific associations or fine-mapping/QTL records with variant, effect, trait, and date/version. | Catalog-level existence is insufficient, but the source-specific import path is concrete. |
| PTGER4 mixed shared/distinct signal closes naive transfer | `claim.ms_ibd.treatment_transfer_caution_context.2026-06-14` | `low` | `closed_unless_signal_specific_data_arrive` | Only reopen if PTGER4-specific fine-mapping, QTL, or treatment-transfer data directly address the mixed-signal failure mode. | PTGER4 signal-specific external data with direction and disease-layer definitions. | General treatment-transfer caution is context only; the project finding is already negative-established for naive transfer. |
| No validated broad immune-state simulator from held data | `resource.msgd.database_commons.2026-06-13` | `low` | `closed_unless_new_perturbation_validation_data_arrive` | Do not reopen simulator claims without a held-out perturbation dataset and frozen split. | Held-out perturbation or response dataset suitable for simulator validation. | External resource metadata cannot address the simulator validation failure. |
| Coupled-axis successor rule does not beat scalar | `claim.dailymed.dimethyl_fumarate_mechanism_context.2026-06-13` | `low` | `closed_unless_preregistered_external_comparison_arrives` | Retest only under a preregistered external scalar-versus-successor comparison. | External cohort with frozen scalar and any pre-locked successor evaluated under the V27/V42 comparison rules. | A treatment label cannot evaluate the predictive comparison; current project result remains negative-established. |
| Locked V7 general cross-disease baseline fallback killed | `claim.probast_tripod.prediction_model_validation_context.2026-06-14` | `low` | `closed_unless_same_failure_mode_dataset_arrives` | Only retest the baseline fallback in a predefined external dataset directly matching the cross-disease baseline-fallback rule. | Dataset with baseline-only cross-disease transfer structure and predefined failure-mode comparison. | Generic prediction-model guidance supports discipline but not the specific kill. |
| Crohn downstream IFN/APC convergence exceeds genetic proximity | `claim.nature.ms_uc_greater_genetic_correlation_context.2026-06-14` | `medium` | `needs_crohn_response_data` | Test downstream IFN/APC response convergence in Crohn paired response data before using Crohn as a monitoring comparator. | Crohn paired treatment-response transcriptomic data with IFN/APC module coverage. | MS-UC/MS-CD genetic proximity context does not test downstream response convergence. |
| RA pregnancy comparator but blood APC treatment-response nontransfer | `claim.ard.ra_sle_pregnancy_transcriptome_context.2026-06-14` | `low` | `context_only_until_ms_or_ra_response_transfer_data` | Use RA/SLE pregnancy data for timing context only unless paired MS/RA treatment-response transfer data are acquired. | Paired treatment-response transfer data, not pregnancy transcriptome context alone. | Pregnancy transcriptomes help postpartum timing questions but do not test blood APC treatment-response nontransfer. |
| EBV/IFN APC imprint downgraded by specificity control | `claim.science.ebv_ms_longitudinal_risk_context.2026-06-14` | `medium` | `needs_ebv_stratified_expression_with_specificity_controls` | Rerun the imprint test only with EBV-stratified expression and predefined autoimmune/control specificity panels. | EBV-stratified MS/control/comparator transcriptomes with enough APC/IFN module coverage. | EBV-MS risk context does not rescue a specificity-failed APC/IFN imprint. |
| GPR25 demoted from protected favorite | `claim.nature.ms_ibd_gpr25_context.2026-06-14` | `low` | `closed_unless_direction_and_tractability_evidence_arrive` | Only reconsider if signal-specific direction and tractability evidence directly resolves the V19 demotion reason. | GPR25-specific direction, QTL, fine-mapping, and tractability evidence. | External nomination of GPR25 as a putative gene is not direction-matched target evidence. |
| No load-bearing invariant found in V26 | `claim.cshperspect.ms_biomarker_heterogeneity_context.2026-06-14` | `low` | `closed_until_null_tested_invariant_candidate_exists` | Do not promote an invariant unless a new candidate passes cross-modality null-tested invariant gates. | A predefined invariant candidate and cross-modality data sufficient for null/permutation testing. | General biomarker heterogeneity context is not an invariant-search replication. |

## Interpretation

- `high` means the row has a concrete frozen-harness or source-specific import route already defined.
- `medium` means the row is scientifically testable but needs a specific data type not currently in hand.
- `low` means the row should stay closed or context-only unless a narrowly matching future source arrives.
- No row in this file is evidence for or against the underlying grounded finding; the V37/V48 grounded artifacts remain authoritative.
