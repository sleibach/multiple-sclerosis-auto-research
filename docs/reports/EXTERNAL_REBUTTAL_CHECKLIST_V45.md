# V45 Skeptical External Methods And Limitations Checklist

## Status

Synthesis only. No new analysis, hypothesis, rule, or validation claim is made
here.

## Purpose

Convert the V44 external account draft into a peer-review-style checklist:
what a skeptical reader will ask, whether the project has already answered it,
where the answer is still incomplete, and what evidence must not be overstated.

## Methods Checklist

| Requirement | Current artifact | Status | Gap / next action |
|---|---|---|---|
| Locked rule before validation | `docs/locked_rules/LOCKED_RULE_V22.md` | complete | Do not edit. |
| Frozen external-validation plan | `docs/validation/PREREGISTRATION_V42.md` | complete | Run mechanically only after data arrive. |
| Pre-committed interpretation grid | `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md` | complete | Use even if Gafson result is inconvenient. |
| Primary executable harness | `scripts/v42_gafson_validation_harness.py` | complete | Real run awaits quarantined data. |
| Synthetic null/planted harness check | `analysis/v42_harness_validation/` | complete | Synthetic only; not biological evidence. |
| Power map | `docs/validation/POWER_MAP_V43.md` | complete | Gafson-sized cohort may be inconclusive. |
| Batch robustness guard | `docs/validation/BATCH_GUARD_V44.md` | complete | Guard is conservative; calibrate over-flagging separately. |
| Multi-confounder guard stress | `docs/validation/MULTICONFOUNDER_BATCH_GUARD_V45.md` | complete | Do not adopt naive joint technical residualization. |
| Seed-stability audit | `docs/validation/SEED_VARIATION_STABILITY_V45.md` | complete | Method behavior stable across seed families; synthetic only. |
| Full-grid batch calibration | `docs/validation/BATCH_GUARD_CALIBRATION_FULL_V45.md` | complete | Rejects q-calibrated guard as replacement; strict guard remains primary. |
| Confounder audit on held cohorts | `docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md` | complete | Signal is immune-tone bounded, not confounder-free. |
| Internal recurrence nulls | `docs/validation/APC_HLA_INTERNAL_CONVERGENCE_V44.md` | complete | Internal support only, not clinical validation. |
| Weighted/collapsed recurrence sensitivity | `docs/validation/APC_HLA_CONVERGENCE_SENSITIVITY_V45.md` | complete | Supports convergence against duplicate-row objection. |
| Leave-one-family convergence | `docs/validation/APC_HLA_FAMILY_JACKKNIFE_V45.md` | complete | Supports against single-artifact-family objection. |
| No-report convergence sensitivity | `docs/validation/APC_HLA_NO_REPORTS_CONVERGENCE_V45.md` | complete | Shows recurrence does not depend on V37 report rows. |
| No-readiness convergence sensitivity | `docs/validation/APC_HLA_NO_READINESS_CONVERGENCE_V45.md` | complete | V41 frame contains zero post-V42 readiness rows; readiness circularity absent. |
| Alternative cohort scout | `docs/validation/ALT_COHORT_SCOUT_V44.md`; `docs/validation/GSE228330_OUTCOME_SCOUT_V45.md` | complete for current public scout | Does not prove private/controlled cohorts absent. |
| Karolinska label request package | `docs/validation/KAROLINSKA_DMF_LABEL_REQUEST_V45.md` | complete | Human must send/request labels. |
| Outbound data-request tracker | `docs/validation/OUTBOUND_DATA_REQUEST_TRACKER_V45.md` | complete | Requests still require human send/access action. |
| Decision-grade cohort spec | `docs/validation/MEDICAL_TEAM_COHORT_SPEC_V45.md` | complete | Use for acquisition negotiation. |
| Clinical CRF checklist | `docs/validation/CLINICAL_DATA_DICTIONARY_CRF_V45.md` | complete | Must be enforced in collaborator data requests. |
| Intake preflight guard | `docs/validation/VALIDATION_INTAKE_PREFLIGHT_V45.md`; `scripts/v45_validation_intake_preflight.py` | complete | Must be run before any frozen harness touches a new cohort. |
| Secondary lead preregistrations | V44 postpartum and T/B prereg docs | complete as plans | Await matching real cohorts. |
| Secondary real-ingest harnesses | `docs/validation/SECONDARY_REAL_INGEST_HARNESS_V45.md`; `scripts/v45_secondary_real_cohort_harness.py` | complete | Synthetic null/planted mechanics only; no real matching cohort opened. |
| Secondary pathology stress tests | V45 postpartum and T/B pathology docs | complete | Synthetic only; defines data-quality envelope. |
| Pharmacodynamic-only context path | `docs/validation/PHARMACODYNAMIC_ONLY_HARNESS_V45.md`; `docs/validation/GSE228330_PHARMACODYNAMIC_RUNBOOK_V45.md` | complete as infrastructure | GSE228330 needs expression reprocessing and confirmed subject map before context harness use. |
| V45 readiness handoff/index | `docs/validation/V45_ARTIFACT_INDEX.md`; `docs/validation/COLLABORATOR_VALIDATION_PACKAGE_README_V45.md`; `docs/validation/VALIDATION_COMMAND_RUNNER_V45.md` | complete as operational appendix | Does not create validation evidence; it makes future intake auditable. |
| Synthetic/readiness interpretation boundary | `docs/reports/SYNTHETIC_READINESS_BOUNDARY_APPENDIX_V45.md` | complete as external appendix | Must be cited whenever V43-V45 synthetic/readiness artifacts are summarized externally. |
| External-report citation manifest | `docs/reports/EXTERNAL_REPORT_EVIDENCE_MANIFEST_V45.md` | complete as citation-governance appendix | Use to keep cited artifacts inside their allowed evidence class. |

## Skeptical Rebuttal Table

| Skeptical challenge | Honest answer | Evidence | Residual weakness |
|---|---|---|---|
| "This project found no target and is reframing failure as success." | Correct that no intervention-grade target was found. That is reported as a negative result, not hidden. The surviving lead is a monitoring hypothesis, not a target. | V37 findings report; V19 chr1 reevaluation; V25 simulator negative; V27/V28 successor-rule failures. | External audiences may still expect target discovery; title/abstract must state boundary-mapping clearly. |
| "The APC/HLA-II rule is overfit to tiny cohorts." | Existing real cohorts are small. The rule was locked before held-out tests and complexity did not improve it, but it remains provisional pending external validation. | V22 lock/ledger; V23 bounded workup; V27/V28 scalar-vs-complexity results. | Gafson or another cohort is required; no clinical claim before that. |
| "The signal is just steroids." | The V32 audit found glucocorticoid/steroid-response controls did not explain it away. | `CONFOUNDER_AUDIT_V32.md`. | Steroid metadata still mandatory in external validation; future cohort may differ. |
| "The signal is just cell composition." | Simple marker-level composition controls did not explain the V22 scalar; T/B and postpartum secondary leads explicitly require composition/fraction adjustment. | V32, V44 T/B preregistration, V45 T/B pathology stress. | Better single-cell/compartment-resolved validation would be stronger. |
| "The signal is just immune tone." | Partly true. The project now describes it as immune-tone bounded; broad metabolic/inflammatory/STAT1 adjustment attenuates it. | V32; V39; V43/V44/V45 diagnostics. | Mechanistic specificity remains bounded, not absolute. |
| "Batch effects can fake response." | Yes. V43 showed this and V44/V45 added a conservative diagnostic guard that prevents synthetic batch nulls from clean passes. | V43 robustness; V44 batch guard; V45 multi-confounder and secondary pathology stress tests; V45 seed-stability audit. | Full-grid calibration rejected looser q-guards as replacements, so the strict guard remains primary and may downgrade some true positives. |
| "Synthetic simulations are not evidence for biology." | Correct. They are method-behavior checks only, labeled synthetic, seeded, and never used as biological support. | V43/V44/V45 synthetic artifacts; `docs/reports/SYNTHETIC_READINESS_BOUNDARY_APPENDIX_V45.md`. | Must maintain this wording in any external manuscript. |
| "Internal convergence is circular because project reports repeat the same idea." | V45 tested this directly. APC/HLA/IFN remains rank 1 after source-file weighting, source-family collapse, leave-one-family removal, and removal of report-derived rows. The V41 frame contains zero post-V42 readiness rows. | V44 internal convergence; V45 convergence sensitivity; V45 family jackknife; V45 no-report and no-readiness sensitivities. | Internal convergence still cannot replace external clinical validation. |
| "RPT/LLMs are being treated as evidence." | No. Model outputs are proposal/prioritization only and are grounded or ignored. | V31/V36/V45 RPT docs. | Keep model-generated text out of evidence claims. |
| "Gafson may be too small to settle the rule." | Correct. V43 says Gafson-sized data can be informative but may be inconclusive. The project now pursues Karolinska labels and a larger cohort spec in parallel. | V43 power map; V44 cohort scout; V45 cohort spec. | Until new data arrive, the validation lead remains pending. |
| "No public cohort found does not mean no cohort exists." | Correct. V24/V44/V45 establish public/low-barrier scout status, not a universal absence claim. GSE228330 is open context material, not response validation. | V24/V44 scout docs; V45 GSE228330 audit and runbook. | Controlled and collaborator data remain the rational next path; GSE228330 needs expression reprocessing and a confirmed subject map even for formal context deltas. |
| "The coupled APC axis sounds like a post-hoc successor rule." | It is not used as a successor rule. V27/V28 showed coupled/complex features did not fairly beat the scalar. | V26; V27; V28. | Coupling should be presented as mechanism context only. |
| "Secondary live leads are being quietly upgraded without validation." | No. Postpartum APC-arm and T/B compartment leads are pre-registered and synthetic-verified, but have not been validated on real matching cohorts. | V44 secondary preregistrations; V45 secondary real-ingest harness; V45 pathology stress tests. | They are readiness assets, not clinical findings. |
| "A received collaborator file could be inspected before the frozen run." | V45 added an intake preflight guard for checksums, schema, sample matching, and response-label guardrails before harness execution. | V45 intake preflight doc and synthetic checks. | Operational discipline is still required: a human must place files in quarantine and run preflight before analysis. |

## Wording Guardrails

Use:

- "provisional monitoring lead";
- "validation-ready, not validated";
- "immune-tone bounded";
- "synthetic method-characterization";
- "internal convergence support";
- "context-only pharmacodynamic cohort";
- "intake-preflight passed/failed";
- "no intervention-grade target".

Do not use:

- "validated biomarker";
- "clinical rule";
- "baseline stratifier";
- "predicts NEDA" without external validation;
- "drug target" for APC/HLA/IFN, KIF21B, GPR25, PTGER4, or NAMPT;
- "confounder-free";
- "synthetic evidence for MS biology".
- "response validation" for pharmacodynamic-only cohorts without sample-mapped
  outcomes.

## External Manuscript Structure

1. State negative target-discovery result first.
2. Present the locked monitoring rule as the surviving provisional lead.
3. Show why complexity was rejected.
4. Show confounder and batch boundaries.
5. Present internal convergence as support, not validation.
6. Present power/readiness and the exact external validation plan.
7. End with the boundary: public-data computation is exhausted for new
   discovery under the V41 gate; new paired response data are required.

## Current Publication-Grade Gap List

| Gap | Severity | Close path |
|---|---|---|
| No external Gafson/DMF result yet | high | Acquire data and run V42/V44 harness. |
| Gafson may be underpowered | high | Karolinska labels plus larger prospective/collaborator cohort spec. |
| Batch guard is conservative | medium | V45 full-grid calibration rejected looser q-guards as replacements; report strict-guard downgrade risk honestly. |
| Secondary leads lack real data | medium | Real-ingest scripts now exist; acquire matching postpartum/TB-compartment cohorts before claiming validation. |
| Pharmacodynamic-only context cohorts require processing | medium | GSE228330 raw archive is open but needs CEL reprocessing plus confirmed subject pairing before context harness use. |
| Intake discipline is operational, not automatic | medium | Run V45 preflight on every quarantined cohort before any harness. |
| Mechanistic specificity is immune-tone bounded | medium | Report bounded interpretation; do not claim APC-specific causality. |
| No intervention-grade target | not a gap to hide | Present as a negative result and boundary map. |
