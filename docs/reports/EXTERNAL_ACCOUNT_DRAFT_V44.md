# External Account Draft V44

Date: 2026-06-12

Status: skeptical external-facing draft. This is synthesis only, not new analysis.

## Working Title

Computational Boundary Mapping Of A Multiple-Sclerosis Treatment-Monitoring Signal: A Locked Rule, Negative Target Workups, And Validation Readiness

## Abstract Draft

This project evaluated whether public autoimmune genetics, immune-QTL, single-cell, perturbation, and treatment-response data could nominate actionable multiple-sclerosis targets or response-monitoring biomarkers. The target-discovery branch produced no intervention-grade target: several biologically real signals failed direction, colocalization, or tractability gates. The strongest surviving result is not a target but a provisional early-treatment monitoring signal: a locked APC/HLA-II/IFN module-change scalar that appears mechanism-bounded to immune-remodeling/JAK-STAT contexts and does not improve with more complex model classes.

The signal remains unvalidated clinically. Its internal support comes from independent computational checks: locked-rule small-cohort validation, heterogeneous-method robustness, confounder auditing, cross-modality recurrence, synthetic-null self-audit, and blind validation-harness hardening. V44/V45 add readiness improvements: no open, ready-to-run alternative primary cohort was found beyond Gafson/DMF and related low-barrier requests; a batch-diagnostic guard prevents response-correlated batch from producing a clean pass in synthetic nulls; seed-stability and regression checks make the synthetic method behavior reproducible; intake preflight now checks checksums, schemas, sample IDs, and response-label guardrails before any harness; and convergence evidence remains beyond global, modality-aware, source-local, no-report, and no-readiness-circularity nulls.

The project's defensible conclusion is boundary-setting rather than clinical deployment. Public-data computation has been substantially exhausted for unconstrained discovery. The rational next step is external paired treatment-response validation using the frozen preregistered harness, plus independent replication if Gafson is underpowered or technically confounded.

## V45 Methods Addendum

V45 did not reopen discovery. It reduced dependence on a single delayed cohort
and hardened the validation boundary.

Additional readiness artifacts:

- `docs/validation/VALIDATION_INTAKE_PREFLIGHT_V45.md`: quarantine checksums,
  metadata schema checks, expression/sample-ID checks, and pharmacodynamic
  no-response-label guardrails before any frozen harness.
- `docs/validation/HARNESS_REGRESSION_TESTS_V45.md` and
  `docs/validation/PREFLIGHT_REGRESSION_TESTS_V45.md`: executable synthetic
  regression tests for secondary harnesses, pharmacodynamic context-only
  behavior, and intake preflight.
- `docs/validation/SEED_VARIATION_STABILITY_V45.md`: seed variation across
  `31,500` synthetic cohorts, keeping worst guarded synthetic-null clean pass at
  or below `0.0333` for the tested harness families.
- `docs/validation/BATCH_GUARD_CALIBRATION_FULL_V45.md`: full-grid calibration
  rejects looser q-calibrated batch guards as replacements for the stricter
  effect-threshold guard.
- `docs/validation/APC_HLA_NO_REPORTS_CONVERGENCE_V45.md` and
  `docs/validation/APC_HLA_NO_READINESS_CONVERGENCE_V45.md`: recurrence is not
  driven by V37 report rows, and the V41 integrated frame contains zero post-V42
  readiness rows.
- `docs/validation/VALIDATION_POWER_DECISION_TABLE_V45.md`: Gafson-sized cohorts
  are useful but often inconclusive; `30+30` is decision-grade only for large
  clean effects; noisy/moderate immune-tone cases may require larger or cleaner
  data.
- `docs/reports/SYNTHETIC_READINESS_BOUNDARY_APPENDIX_V45.md`: reviewer-facing
  boundary statement separating synthetic/readiness method evidence from
  biological validation.
- `docs/reports/EXTERNAL_REPORT_EVIDENCE_MANIFEST_V45.md`: citation manifest
  mapping external-report artifact references to evidence/allowed-use classes.

Correct external framing:

> V45 improves validation readiness and auditability. It does not add clinical
> validation and does not make synthetic data biological evidence.

## V45 Readiness Appendix For Reviewers

V45 now has a reviewer-oriented handoff layer. These artifacts are operational
and methodological; none is a biological validation result.

| Reviewer question | Artifact |
|---|---|
| What did V45 produce, and how should each output be interpreted? | `docs/validation/V45_ARTIFACT_INDEX.md`; `analysis/v45_artifact_index/v45_artifact_index.tsv` |
| What should a collaborator send? | `docs/validation/COLLABORATOR_VALIDATION_PACKAGE_README_V45.md`; `docs/validation/CLINICAL_DATA_DICTIONARY_CRF_V45.md` |
| Which cohorts are live, and what blocks each? | `docs/validation/LIVE_COHORT_ACQUISITION_PACKET_INDEX_V45.md`; `docs/validation/OUTBOUND_DATA_REQUEST_TRACKER_V45.md` |
| What exact request packets are ready? | `docs/validation/outbound_requests/` |
| How are data-use terms captured before analysis? | `docs/validation/DATA_USE_TERMS_CAPTURE_V45.md`; `docs/validation/input_schemas/V45_data_use_terms_capture_template.tsv` |
| How are received outcome labels defined before scoring? | `docs/validation/OUTCOME_LABEL_DICTIONARY_TEMPLATE_V45.md`; `docs/validation/input_schemas/V45_outcome_label_dictionary_template.tsv` |
| What command sequence runs before a harness? | `docs/validation/VALIDATION_COMMAND_RUNNER_V45.md`; `analysis/v45_validation_command_runner/` |
| How is invalid sample pairing blocked? | `docs/validation/SUBJECT_MAP_SANITY_CHECKER_V45.md` |
| How is pharmacodynamic-only response leakage blocked? | `docs/validation/RESPONSE_COLUMN_AUDIT_V45.md` |
| How are small handoff packages checksummed? | `docs/validation/CHECKSUM_MANIFEST_VALIDATOR_V45.md` |
| Are array/CEL cohorts locally processable now? | `docs/validation/ARRAY_PROCESSING_READINESS_V45.md` |
| How does dropout/missingness affect planning? | `docs/validation/DROPOUT_MISSING_TIMEPOINT_SENSITIVITY_V45.md`; `docs/validation/SECONDARY_MISSING_TIMEPOINT_STRESS_V45.md` |
| Is the primary harness regression-tested? | `docs/validation/PRIMARY_HARNESS_REGRESSION_TESTS_V45.md` |
| How should synthetic/readiness outputs be interpreted externally? | `docs/reports/SYNTHETIC_READINESS_BOUNDARY_APPENDIX_V45.md` |

Reviewer path:

1. Start with the artifact index to separate synthetic method behavior,
   public-metadata scouting, software, internal convergence nulls, and
   operational documents.
2. Read the collaborator package README to see the full intake order.
3. Verify that the command-runner plans require terms, checksums, preflight,
   subject-map sanity, and preregistration confirmation before harness handoff.
4. Check that the subject-map and response-column guards fail the expected
   negative fixtures.
5. Confirm that no V45 artifact changes the V22 locked rule or V42 thresholds.

Short form:

> V45 converts delayed-data waiting time into an auditable validation operations
> layer. It makes future external validation harder to fool, but it does not
> itself validate the monitoring signal.

## Main Claims

### Claim 1: No Intervention-Grade Genetics Target Was Produced

Supported by:

- chr1/KIF21B/GPR25 reevaluation: real biology, wrong/restorative direction and hard modality.
- PTGER4: direction-conflicted shared/distinct signal; closed as naive transfer.
- ZMIZ1: clean MS/Crohn opposite-direction decoupling; transfer warning, not a target.
- REL/PUS10/USP34 and ZFP36L1: not promoted under robust coloc/QTL direction gates.

Skeptical interpretation: this is not a failed search hidden behind a biomarker pivot. It is an explicit negative result. The direction and modality constraints are the result.

### Claim 2: The Surviving APC/HLA-II Signal Is A Monitoring Lead, Not A Clinical Rule

Supported by:

- locked V22 rule and validation ledger;
- V23 mechanism-bounding;
- V28 heterogeneous-method robustness;
- V32 confounder audit;
- V42 preregistration and V44 batch hardening.

The lead is provisional because all real validation cohorts so far are small, heterogeneous, and partly project-derived. It should not be described as a baseline stratifier, a validated NEDA predictor, or a treatment-selection tool.

### Claim 3: Complexity Did Not Improve The Signal

V27/V28 tested coupled-axis, flexible ML, and methodologically different reanalyses. More complex versions did not fairly beat the simple locked scalar under small-n-aware evaluation. This is important because it prevents post-hoc feature expansion while waiting for Gafson.

External wording should be blunt:

> The current best form is the simple locked scalar, not because it is biologically complete, but because added complexity did not earn predictive credibility in held data.

### Claim 4: The Signal Is Confounder-Bounded, Not Confounder-Free

V32 found that glucocorticoid and simple composition controls did not explain the V22 signal away, but immune-tone / STAT1 / metabolic adjustment attenuated it. V44 then added a batch guard because V43 synthetic robustness showed response-correlated batch can generate false positives.

Correct interpretation:

- clean validation requires the raw score to pass and the batch guard not to flag;
- raw pass plus batch or immune-tone attenuation is not a clean clinical validation;
- confounder-aware reporting is part of the claim, not an optional sensitivity analysis.

### Claim 5: Internal Convergence Is Stronger Than Joint-Discovery Significance

V41's joint-inference gate recovered APC/HLA/IFN as the top known-context structure but was borderline against the family-wise max-z null. V44 resolved the weak leg: the recurrence/convergence formulation is more defensible.

Key internal numbers:

- APC/HLA/IFN recurrence: `78` positive source units across `11` modalities.
- Strictest V44 source-local null p99: `41`.
- V44 target FWER under source-local null: `0.00005` in `20,000` replicates.
- Removing `treatment_response` leaves recurrence `46`.
- Removing the densest source file leaves recurrence `55`.

This supports the statement that the APC/HLA/IFN monitoring axis is repeatedly recovered across the corpus. It still does not validate clinical prediction.

### Claim 6: Gafson Is Necessary But May Not Be Sufficient

V43 power simulations showed a Gafson-sized cohort may be inconclusive at plausible effect sizes. V44 therefore reduced single-cohort dependence:

- repeated alternative-cohort scouting found no fresh open, ready primary validation cohort;
- Gafson remains the best low-barrier primary target;
- Karolinska DMF data are open for expression/methylation but require labels;
- GSE228330 anti-CD20/ocrelizumab is open pharmacodynamic context, not a labeled response-validation cohort.

The validation plan must treat Gafson as the next rational test, not as guaranteed final arbitration.

## Evidence Table For A Skeptical Reader

| Evidence layer | Main artifact | What it supports | What it does not support |
|---|---|---|---|
| Genetics/coloc | V19/V21/V37 reports | No direction-matched intervention-grade genetics target; MS-UC backdrop | Target nomination |
| Locked rule | `LOCKED_RULE_V22.md` | Pre-specified scalar exists | External clinical validity |
| Validation ledger | `VALIDATION_LEDGER_V22.md`, V23 | Small-cohort bounded monitoring signal | Broad cross-therapy rule |
| Robustness | `ROBUSTNESS_MAP_V28.md` | Scalar is not a single-method artifact | Superiority to fresh data |
| Confounders | `CONFOUNDER_AUDIT_V32.md` | Not steroid/simple-composition artifact; immune-tone bounded | Confounder-free mechanism |
| Preregistration | `PREREGISTRATION_V42.md` | Gafson analysis frozen before data | A result before data arrive |
| Power/robustness | `POWER_MAP_V43.md`, `HARNESS_ROBUSTNESS_V43.md`, `VALIDATION_POWER_DECISION_TABLE_V45.md` | Expected interpretability limits and acquisition sizing | Biological evidence |
| V44 batch guard | `BATCH_GUARD_V44.md` | Batch false-positive risk controlled in synthetic nulls | Changed V22 rule |
| V45 seed/regression guards | `SEED_VARIATION_STABILITY_V45.md`, `HARNESS_REGRESSION_TESTS_V45.md`, `PREFLIGHT_REGRESSION_TESTS_V45.md` | Synthetic method behavior and software guardrails are reproducible | Biological evidence |
| V45 intake preflight | `VALIDATION_INTAKE_PREFLIGHT_V45.md`, `INTAKE_TEMPLATE_DRYRUN_V45.md` | New cohorts must pass checksum/schema/sample-ID/response-guard checks before harness use | A result on any real cohort |
| V44/V45 convergence | `APC_HLA_INTERNAL_CONVERGENCE_V44.md`, V45 sensitivity/no-report/no-readiness checks | Corpus-level recurrence is robust to stricter and circularity nulls | Clinical validation |
| V44/V45 cohort scout | `ALT_COHORT_SCOUT_V44.md`, `GSE228330_PHARMACODYNAMIC_RUNBOOK_V45.md`, outbound request packets | No verified open primary alternative found; low-barrier paths are operationalized | Proof no private/controlled data exist |

## Limitations To State Explicitly

1. No intervention-grade target has been produced.
2. No prospective validation has been run.
3. Existing real validation cohorts are small and heterogeneous.
4. The central signal is immune-tone bounded and must be interpreted with confounders.
5. Synthetic simulations characterize method behavior only; they are not biological evidence.
6. Public-data discovery appears exhausted under the V41 corpus-level gate, but this is a bound on this corpus and vocabulary, not biology generally.
7. Gafson may be underpowered or technically confounded; a non-clean result should update the lead rather than be forced into pass/fail rhetoric.
8. V45 synthetic and regression artifacts are software/method checks only; they
   should appear in methods/readiness sections, not results-as-biology sections.
9. Pharmacodynamic-only cohorts such as GSE228330 must not be described as
   response validation unless sample-mapped outcomes are obtained and a blinded
   addendum is committed before scoring.

## Proposed External Bottom Line

The project's strongest contribution is not a cure target. It is a disciplined validation-ready monitoring hypothesis and a clear boundary map of failed target routes. The APC/HLA-II/IFN early-treatment scalar is internally recurrent, method-robust, confounder-audited, batch-guarded, and preregistered for external testing, but it remains provisional until a blinded external paired response cohort is run.

If Gafson passes cleanly, the next step is independent replication in a second paired MS DMT response cohort and a prospective sampling design. If Gafson is inconclusive, the V43 power map should determine the next cohort size rather than post-hoc reinterpretation. If Gafson fails cleanly, the monitoring lead should be demoted or killed according to the V42 outcome grid.
