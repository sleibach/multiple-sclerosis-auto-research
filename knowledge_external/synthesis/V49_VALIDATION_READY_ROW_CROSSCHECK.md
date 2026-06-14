# V49 Validation-Ready Row Crosscheck

Status: synthesis/navigation only. This document crosschecks V49
insufficient-overlap rows that pointed toward validation against the already
frozen validation artifacts. It does not add external claims, alter the V22
locked rule, or change any pre-registration.

Boundary: the row labels come from
`knowledge_external/synthesis/V49_INSUFFICIENT_OVERLAP_TRIAGE.md`. The
validation coverage evidence comes from the project's frozen validation docs and
scripts. A row marked covered here means "mechanically ready when the required
blind data arrive", not validated.

## Summary

- validation-facing rows reviewed: `7`
- fully covered by frozen V42/V44 primary harness path: `2`
- covered by frozen V44 secondary-lead harness path: `2`
- not validation-harness rows; handled by source-specific import packets: `3`
- new mechanical validation checks required now: `0`

## Crosscheck Table

| V49 row | route type | mechanical status | covered by | missing input or action | notes |
|---|---|---|---|---|---|
| Bounded APC/HLA-II early treatment-response monitoring scalar | primary blind validation | `READY_BLIND_DATA` | `docs/validation/PREREGISTRATION_V42.md`; `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`; `scripts/v42_gafson_validation_harness.py`; `docs/validation/BATCH_GUARD_V44.md` | Paired baseline/early-treatment transcriptomes, NEDA-4 or comparable response labels, module-gene coverage, and technical/confounder metadata. Renew OpenGWAS token before any validation-adjacent OpenGWAS check after expiry. | The frozen plan specifies eligibility, timepoint selection, expression preprocessing, V22 score, thresholds, bootstrap/permutation metrics, receptor control, confounder panels, batch diagnostics, and output files. No new V49 check is needed. |
| V22 scalar is immune-tone bounded, not steroid/composition artifact | primary interpretation guardrail | `READY_AS_ADDITIVE_DIAGNOSTIC` | `docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md`; `docs/validation/PREREGISTRATION_V42.md`; `docs/validation/BATCH_GUARD_V44.md`; `scripts/v42_gafson_validation_harness.py` | Same future validation package as the primary row, with enough coverage for glucocorticoid, cell-composition, metabolic, STAT1/immune-tone, and technical metadata audits. | V32 defines the caveat, V42 freezes confounder scoring and adjustment labels, and V44 adds batch-risk downgrading. The audit cannot create a pass or rescue a fail. |
| T/B-readable early IFN/APC/STAT1 monitoring state | secondary future validation | `READY_SECONDARY_DATA` | `docs/validation/TB_COMPARTMENT_PREREGISTRATION_V44.md`; `scripts/v44_secondary_lead_harnesses.py`; `analysis/v44_secondary_lead_harnesses/secondary_harness_summary.json` | Future paired response cohort with single-cell, sorted-cell, CITE-seq, or defensible deconvolution readouts for T-like and B/plasma-like compartments. | V44 freezes compartment features, primary B/plasma criterion, T-like companion readout, composition/batch audits, and synthetic null/planted checks. It is not a replacement for V22 primary validation. |
| Postpartum HLA-II/CD64 APC-arm imbalance | secondary future validation | `READY_SECONDARY_DATA` | `docs/validation/POSTPARTUM_APC_ARM_PREREGISTRATION_V44.md`; `scripts/v44_secondary_lead_harnesses.py`; `analysis/v44_secondary_lead_harnesses/secondary_harness_summary.json` | True MS late-pregnancy plus early-postpartum immune-expression cohort with relapse-window labels and steroid, DMT restart, infection, lactation, batch, and composition metadata where available. | V44 freezes HLA-II/CD64 modules, risk-score orientation, pass/fail/inconclusive criteria, confounder audits, and synthetic null/planted checks. Existing pregnancy context is not decisive validation. |
| ZMIZ1 opposite-direction MS/Crohn decoupling | source-specific import, not validation harness | `NOT_A_VALIDATION_HARNESS_ROW` | `knowledge_external/synthesis/V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md` | Import ZMIZ1-specific source records with disease, direction/effect, variant/gene mapping, source version/date, and snapshots before any comparison. | This row needs source-specific record intake, not a cohort validation harness. It should not be routed through the V42/V44 validation machinery. |
| chr1 KIF21B/GPR25 locus resolves to real biology but hard target | source-specific import, not validation harness | `NOT_A_VALIDATION_HARNESS_ROW` | `knowledge_external/synthesis/V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md` | Import signal-specific GWAS/fine-mapping/QTL records preserving variant, effect allele, direction, trait, study accession, publication, and source version/date. | The acceptance gate is direction-preserving signal specificity. Generic catalog-level locus existence is not enough. |
| Coupled APC remodeling architecture | source-specific import, not validation harness | `NOT_A_VALIDATION_HARNESS_ROW` | `knowledge_external/synthesis/V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md` | Import source-specific CD74, MIF, HLA, IFN/APC, APC-axis, cell-state, or interaction records before comparison to V26. | Resource-level metadata cannot corroborate architecture. This remains a future source-intake route, not a validation-harness gap. |

## Decision

No new validation-harness work is required by the V49 high-actionability rows.
The primary V22 validation route and its confounder/batch interpretation
guardrails are already frozen and synthetic-checked. The T/B and postpartum
secondary routes are also pre-registered and synthetic-checked, but they await
specific future data types.

The only open V49 actions are not harness gaps:

1. Receive or acquire blind validation data and run the existing frozen primary
   or secondary harness as applicable.
2. Use `V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md` for the three source-import
   routes before making any future relationship-matrix comparison.
3. Keep OpenGWAS expiry visible: validation itself is OpenGWAS-independent, but
   any validation-adjacent OpenGWAS query after token expiry requires renewal
   first.

