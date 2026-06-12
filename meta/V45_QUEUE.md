# V45 Queue: Continuous Self-Directed Research Block

Block start UTC: 2026-06-12T16:06:13Z
Target UTC (+360 min): 2026-06-12T22:06:13Z

## Stop Conditions

Valid stops only:

1. cumulative measured runtime >= 360 minutes and clean resumable point;
2. external termination;
3. documented all-fronts block after every internally executable alternative is exhausted.

Backlog exhaustion is not a stop. When executable todo items drop below five,
generate more internally executable tasks before continuing.

## Iterations

| Iteration | Start UTC | End UTC | Status | Notes |
|---|---:|---:|---|---|
| 1 | 2026-06-12T16:06:13Z |  | in-progress | Initialized V45. OpenGWAS POST check passed; JWT expires 2026-06-19 12:28 UTC. SAP AI Core Claude/Gemini/RPT smoke-passed. |
| 1r | 2026-06-12T16:14:02Z |  | in-progress | Resumed V45. OpenGWAS POST check passed; Claude/Gemini/RPT smoke-passed with corrected Gemini exact model name. |

## Live Backlog

| Priority | Front | Item | Status | Notes |
|---:|---|---|---|---|
| 1 | Cohort dependence | Write concrete Karolinska DMF label-access package and exact request steps | done | Wrote `docs/validation/KAROLINSKA_DMF_LABEL_REQUEST_V45.md`; verified GEO/PubMed metadata into `analysis/v45_karolinska_access/`; blocker is labels plus GSM-to-patient/timepoint map. |
| 2 | Cohort dependence | Deep paper/supplement scout specifically for GSE228330 anti-CD20/ocrelizumab outcomes | done | Wrote `docs/validation/GSE228330_OUTCOME_SCOUT_V45.md`; public metadata verify 44 PBMC ocrelizumab samples with baseline/0.5m/6m timing but no response/NEDA/relapse labels. |
| 3 | Robustness | Extend batch guard simulations to multi-confounder technical structures | done | Wrote `docs/validation/MULTICONFOUNDER_BATCH_GUARD_V45.md`; 5,600 synthetic cohorts show existing individual guard keeps worst synthetic-null acceptable pass at 0.0125, while naive joint guard is worse at 0.1000. |
| 4 | Robustness | Stress-test V44 postpartum APC-arm harness under missing timepoints, steroid metadata, and batch imbalance | done | Wrote `docs/validation/POSTPARTUM_PATHOLOGY_STRESS_V45.md`; 6,300 synthetic cohorts show guarded null clean-pass max 0.0222 despite raw batch false positives up to 0.7667. |
| 5 | Robustness | Stress-test V44 T/B compartment harness under composition shifts and compartment-label noise | done | Wrote `docs/validation/TB_COMPARTMENT_PATHOLOGY_STRESS_V45.md`; 6,300 synthetic cohorts show composition adjustment controls pure composition artifacts, but batch guard is required for response-correlated batch. |
| 6 | Power/design | Produce medical-team cohort specification from V43/V44 simulations | done | Wrote `docs/validation/MEDICAL_TEAM_COHORT_SPEC_V45.md`; specifies minimum 30+30 for large clean effects and preferred 60-80 per group with batch-balanced metadata for robust validation. |
| 7 | Data-free validation | Run alternative convergence nulls using evidence-row weighting and source-family collapse | done | Wrote `docs/validation/APC_HLA_CONVERGENCE_SENSITIVITY_V45.md`; target remains rank 1 under source-file weighting and source-family collapse, all FWER p=0.00005. |
| 8 | Data-free validation | Leave-one-artifact-family-out APC convergence check | done | Wrote `docs/validation/APC_HLA_FAMILY_JACKKNIFE_V45.md`; removing any of 12 source families leaves target rank 1 and above all V45 p99 envelopes. |
| 9 | Infrastructure | Package validation harness command templates and expected input schemas into a reusable validation README | done | Wrote `docs/validation/VALIDATION_HARNESS_README_V45.md` plus primary, postpartum, and T/B input schema TSVs. |
| 10 | Infrastructure/RPT | Exercise RPT on V44 structured readiness tables as proposal-only and verify no evidence claim changes | done | Wrote `docs/validation/RPT_READINESS_PASS_V45.md`; RPT matched 4/4 artifact-derived action classes and changed no evidence claim. |
| 11 | External account | Expand skeptical peer-review draft into methods/limitations checklist with rebuttal table | done | Wrote `docs/reports/EXTERNAL_REBUTTAL_CHECKLIST_V45.md`; captures skeptical challenges, honest answers, residual gaps, and wording guardrails. |
| 12 | Pre-registration breadth | Draft data-ingestion preregistration skeleton for open pharmacodynamic-only cohorts such as GSE228330 | done | Wrote `docs/validation/PHARMACODYNAMIC_ONLY_PREREGISTRATION_V45.md` plus schema; explicitly forbids response-validation claims without labels. |
| 13 | Robustness | Calibrate batch diagnostic over-flagging with permutation/FDR across many technical fields | done | Wrote `docs/validation/BATCH_GUARD_CALIBRATION_V45.md`; focused 900-cohort pilot shows q<=0.10 calibration improves planted independent acceptable pass 0.2333→0.9333 with worst tested null clean pass 0.0000. |
| 14 | Robustness | Calibrate secondary-lead batch diagnostics for chance over-flagging in small planted cohorts | done | Wrote `docs/validation/SECONDARY_BATCH_CALIBRATION_V45.md`; 12,600 synthetic cohorts show q-calibration improves planted retention but raises worst postpartum null clean pass 0.0222→0.0333, so it remains sensitivity-only. |
| 15 | Infrastructure | Implement real-cohort ingestion scripts for secondary postpartum and T/B schemas before opening matching data | done | Wrote `scripts/v45_secondary_real_cohort_harness.py` and `docs/validation/SECONDARY_REAL_INGEST_HARNESS_V45.md`; synthetic null/planted checks pass for both secondary leads. |
| 16 | Infrastructure | Implement pharmacodynamic-only module trajectory harness for GSE228330-like open cohorts | done | Wrote `scripts/v45_pharmacodynamic_only_harness.py` and `docs/validation/PHARMACODYNAMIC_ONLY_HARNESS_V45.md`; synthetic context-only check writes all preregistered outputs and performs no response validation. |
| 17 | Cohort dependence | Build outbound data-request tracker for Gafson, Karolinska, and GSE228330 outcome-label requests | done | Wrote `docs/validation/OUTBOUND_DATA_REQUEST_TRACKER_V45.md` and machine-readable tracker `analysis/v45_outbound_data_requests/request_tracker.tsv`. |
| 18 | Power/design | Convert V45 cohort specification into a one-page clinical data dictionary / CRF checklist | done | Wrote `docs/validation/CLINICAL_DATA_DICTIONARY_CRF_V45.md` and machine-readable checklist `docs/validation/input_schemas/V45_clinical_crf_checklist.tsv`. |
| 19 | Data-free validation | Re-run convergence sensitivity excluding all corpus-synthesis/report-derived rows | done | Wrote `docs/validation/APC_HLA_NO_REPORTS_CONVERGENCE_V45.md`; after excluding 63 corpus/report rows, target remains rank 1 with FWER p=0.00005 in all three recurrence formulations. |
| 20 | Robustness | Run seed-variation stability checks for V45 synthetic simulations | done | Wrote `docs/validation/SEED_VARIATION_STABILITY_V45.md`; 31,500 synthetic cohorts across five seed families keep worst guarded null pass <=0.0333 for all three V45 harness families. |
| 21 | Robustness | Optimize and scale batch-guard calibration to the full V45 multi-confounder grid | done | Wrote `docs/validation/BATCH_GUARD_CALIBRATION_FULL_V45.md`; all-scenario scale-up rejects q-calibration as a replacement because worst synthetic-null acceptable pass rises to 0.400 (q<=0.10) / 0.125 (q<=0.20). |
| 22 | Cohort dependence | Write Karolinska-specific preregistration addendum template, to be finalized only if labels arrive | done | Wrote `docs/validation/KAROLINSKA_PREREGISTRATION_TEMPLATE_V45.md`; freezes role choices and forbids outcome scoring until labels/mapping are received and addendum is finalized blind. |
| 23 | Infrastructure | Build validation intake preflight script for quarantine checksums, schema checks, and no-response-label guardrails | done | Wrote `scripts/v45_validation_intake_preflight.py` and `docs/validation/VALIDATION_INTAKE_PREFLIGHT_V45.md`; synthetic preflight passes primary and pharmacodynamic packages and fails pharmacodynamic packages with response-like labels. |
| 24 | Pharmacodynamic context | Prepare GSE228330 pharmacodynamic-only acquisition/runbook for the context harness | done | Wrote `docs/validation/GSE228330_PHARMACODYNAMIC_RUNBOOK_V45.md` and `scripts/v45_prepare_gse228330_pharmacodynamic_runbook.py`; public files resolve, but processed expression and confirmed subject map remain blockers before context harness use. |
| 25 | Data-free validation | Re-run APC convergence excluding all validation/readiness artifacts generated after V42 | done | Wrote `docs/validation/APC_HLA_NO_READINESS_CONVERGENCE_V45.md`; the V41 frame contains zero post-V42 readiness rows, and APC/HLA/IFN remains rank 1 at the 20,000-replicate FWER floor. |
| 26 | External account | Update skeptical external checklist with V45 secondary harness and request-tracker readiness claims | in-progress | Generated by V45 items 15-17; keeps the external account current. |
| 27 | Robustness | Add regression tests for context-only and secondary-real-ingest harness synthetic checks | todo | Generated by V45 items 15-16; infrastructure should fail fast if future edits break guardrails. |
| 28 | Infrastructure | Add regression tests for the validation intake preflight synthetic checks | todo | Generated by V45 item 23; ensures checksum/schema/response guardrails fail fast after future edits. |
| 29 | Cohort dependence | Prepare outbound email-ready data request packets for Gafson, Karolinska, and GSE228330 | todo | Generated by V45 item 17; reduces delay from collaborator access paths. |
| 30 | Infrastructure | Add a synthetic-data retention/index document for V43-V45 method-characterization outputs | todo | Generated by V45 synthetic expansion; prevents synthetic artifacts from being mistaken for biological evidence. |
| 31 | Validation readiness | Dry-run the intake preflight command templates against synthetic primary and pharmacodynamic packages from the docs | todo | Generated by V45 item 23; verifies docs and commands remain executable. |
| 32 | Power/design | Build a compact validation power table for stakeholder-facing cohort-size decisions | todo | Generated by V45 item 6/21; distills simulation results into a fast decision aid. |
| 33 | External account | Update the skeptical methods section with intake-preflight and seed-stability guardrails | todo | Generated by V45 items 20/23; keeps external evidence account aligned with current readiness. |

## Generated Follow-Ups

Generated tasks must be added here before backlog drops below five executable
todo items.

## Per-Iteration Notes

- Iteration 1 started at 2026-06-12T16:06:13Z.
- Tooling health: OpenGWAS POST check passed; SAP AI Core Claude/Gemini/RPT
  smoke-passed. RPT remains proposal-only.
- First selected task: Karolinska DMF label-access package.
- Karolinska access package completed at 2026-06-12T16:09:44Z plus metadata
  verification run. Public GEO records verify `GSE130478` expression has `28`
  CD4+ T-cell samples from `14` MS patients at baseline/6 months, `GSE130491`
  methylation has `82` samples, and the public blocker is patient-level
  beneficial-response labels plus GSM-to-patient/timepoint mapping.
- New generated follow-up: if Karolinska labels arrive, write a secondary
  Karolinska-specific preregistration before any module scoring because the
  platform and timing differ from Gafson/V42.
- Next selected task: GSE228330 anti-CD20/ocrelizumab outcome scout.
- Resumed at 2026-06-12T16:14:02Z. OpenGWAS POST check still passes; JWT expiry
  remains 2026-06-19 12:28 UTC. Claude and RPT smoke-passed immediately; Gemini
  smoke-passed with exact model name `gemini-2.5-pro`.
- GSE228330 scout completed. Public GEO and linked full-text audit found paired
  ocrelizumab PBMC pharmacodynamic samples but no sample-mapped responder/NEDA/
  relapse/EDSS-change label, so it is not response-validation ready. It remains
  useful as open anti-CD20 pharmacodynamic context or an author-label request
  target.
- Next selected task: multi-confounder batch-guard simulation extension.
- Multi-confounder batch-guard simulation completed. The V44 individual-feature
  guard remained specific under distributed synthetic technical confounding
  (worst synthetic-null acceptable pass `0.0125` despite worst raw pass `0.8625`).
  A naive joint technical residualization guard was worse (`0.1000` worst null
  acceptable pass), so no harness rule change is made from this run. New
  follow-up generated: calibrate diagnostic over-flagging with permutation/FDR
  because the conservative guard downgrades some planted technically clean-ish
  small cohorts by chance when many metadata fields are audited.
- Next selected task: postpartum APC-arm harness pathology stress test.
- Postpartum pathology stress test completed. Severe response-correlated batch
  can create raw synthetic-null postpartum passes (`0.7667`), but guarded clean
  passes stay low (`0.0222` max). True planted signals with strong batch or
  module-coverage loss are correctly downgraded to non-specific/unscoreable.
  New follow-up generated: calibrate secondary-lead diagnostic over-flagging so
  small planted cohorts are not downgraded merely because many metadata fields
  are audited.
- Next selected task: T/B compartment harness pathology stress test.
- T/B compartment pathology stress test completed. Worst synthetic-null raw and
  composition-adjusted pass rates were both `0.3333` under response-correlated
  batch, while guarded clean pass was `0.0111`. Pure composition artifacts were
  controlled by residualization, but batch metadata and compartment coverage are
  non-negotiable for this lead.
- Next selected task: medical-team cohort specification from V43/V44/V45
  simulations.
- Medical-team cohort specification completed. The decision-grade target is not
  merely "get Gafson": Gafson remains best fit but likely underpowered; pursue
  Karolinska labels in parallel; a prospective/collaborator cohort should target
  at least `60+60` and preferably `80+80` with clean early timepoints, NEDA-style
  labels, cell/technical covariates, and response-balanced processing.
- Next selected task: alternative convergence nulls using evidence-row weighting
  and source-family collapse.
- Alternative convergence nulls completed. `apc_hla_ifn_monitoring` remains rank
  1 under source-file weighting (`12.5267`, max-null p99 `4.0756`), modality
  source-family collapse (`16`, p99 `8`), and source-family collapse (`10`, p99
  `6`); all FWER p-values hit the 20,000-replicate floor `0.00005`.
- Next selected task: leave-one-artifact-family-out convergence check.
- Leave-one-source-family convergence check completed. Removing any of 12 source
  families, including V32 (`25` target units), V26 (`21` target units), or
  `docs/reports` (`9` target units), leaves `apc_hla_ifn_monitoring` rank 1 and
  above all V45 p99 envelopes.
- Next selected task: reusable validation README and input schema templates.
- Validation README and schema templates completed. Primary V22/V42 real-cohort
  harness is executable now; secondary postpartum and T/B real-ingest schemas are
  frozen, but real-ingest scripts remain a generated infrastructure task before
  any matching cohort is opened.
- Next selected task: RPT structured readiness pass as proposal-only.
- RPT structured readiness pass completed. RPT matched all four artifact-derived
  action classes: batch calibration = `HARDEN_METHOD`, secondary real-ingest =
  `IMPLEMENT_INFRA`, `GSE85034` MTX = `CONTEXT_ONLY`, Karolinska =
  `REQUEST_LABELS`. No evidence claim changed.
- Next selected task: skeptical peer-review methods/limitations checklist with
  rebuttal table.
- Skeptical external checklist completed. It makes the main external critique
  explicit: no target, monitoring lead provisional, immune-tone/batch bounded,
  synthetic results method-only, internal convergence not clinical validation,
  and Gafson may be underpowered.
- Next selected task: pharmacodynamic-only data-ingestion preregistration
  skeleton for open cohorts such as GSE228330.
- Pharmacodynamic-only preregistration skeleton completed. It freezes allowed
  context-only analyses for open unlabeled longitudinal cohorts and explicitly
  forbids response-validation claims without sample-mapped labels. Backlog
  refilled above threshold with new internally executable tasks.
- Next selected task: primary batch diagnostic over-flag calibration with
  permutation/FDR.
- Primary batch diagnostic calibration pilot completed. In the focused 900-cohort
  subset, q<=0.10 permutation/FDR calibration improved planted independent
  acceptable pass from `0.2333` to `0.9333` while preserving `0.0000` worst
  tested synthetic-null acceptable pass. No harness change yet; full-grid,
  multi-seed confirmation is now a generated follow-up.
- Next selected task: secondary-lead batch diagnostic calibration.
- Resumed at 2026-06-12T16:56:53Z and completed the secondary-lead batch
  diagnostic calibration. The q-calibrated guard improves planted-signal
  retention (`0.9111` to `0.9556` best planted clean pass) but slightly worsens
  the worst synthetic-null clean pass (`0.0222` to `0.0333`) in the postpartum
  APC-arm grid. The stricter existing guard remains primary; calibration is
  sensitivity-only.
- Next selected task: real-cohort ingestion scripts for the secondary
  postpartum APC-arm and T/B compartment schemas.
- Secondary real-cohort ingest harness completed. `scripts/v45_secondary_real_cohort_harness.py`
  implements the frozen postpartum APC-arm and T/B compartment subject-level
  schemas, writes fixed metrics/QC/batch diagnostics, and passed synthetic
  null/planted checks for all four scenarios. Synthetic labels are explicit in
  every generated summary.
- Next selected task: pharmacodynamic-only module trajectory harness for
  GSE228330-like open cohorts.
- Pharmacodynamic-only harness completed. `scripts/v45_pharmacodynamic_only_harness.py`
  supports expression-matrix or precomputed-module-score input, writes module
  coverage, paired deltas, timepoint summaries, batch/QC diagnostics, and an
  explicit context-only markdown summary. Synthetic check generated `36`
  samples, `24` paired deltas, all required output files, and
  `response_validation_performed: false`.
- Next selected task: outbound data-request tracker for Gafson, Karolinska, and
  GSE228330 outcome-label requests.
- Outbound data-request tracker completed. The tracker consolidates Gafson,
  Karolinska, and optional GSE228330 outcome-label paths, requested fields,
  target raw-data paths, preregistration gates, and follow-up rules. Backlog was
  refilled above the executable threshold with additional internally executable
  cohort-dependence, infrastructure, validation, and external-account tasks.
- Next selected task: one-page clinical data dictionary / CRF checklist.
- Clinical data dictionary / CRF checklist completed. The artifact condenses the
  V45 cohort specification into collaborator-facing required files, timepoints,
  clean-validation requirements, secondary add-ons, intake rules, and a
  machine-readable field checklist.
- Next selected task: convergence sensitivity excluding all corpus-synthesis and
  report-derived rows.
- No-report convergence sensitivity completed. Excluding `63` corpus/report rows
  from `docs/reports/FINDINGS_SCORES_V37.tsv` leaves `922` evidence rows and
  `86` positive source units; `apc_hla_ifn_monitoring` remains rank `1` under
  source-file weighting, modality/source-family collapse, and source-family
  collapse, with FWER p-values at the `20,000`-replicate floor.
- Next selected task: seed-variation stability checks for V45 synthetic
  simulations.
- Seed-variation stability completed. Across `31,500` synthetic cohorts and
  five seed families, primary multi-confounder, postpartum APC-arm, and T/B
  compartment harnesses all kept worst guarded synthetic-null clean pass at or
  below `0.0333`, despite raw null pass rates up to `0.9000`. This stabilizes
  the V45 method-behavior claim without changing any guard.
- Next selected task: optimize and scale batch-guard calibration to the full
  V45 multi-confounder grid.
- Full-grid batch-guard calibration completed. The focused pilot does not
  generalize: q-calibrated guards recover planted independent signals but allow
  synthetic-null acceptable pass rates up to `0.400` under q<=0.10 and `0.125`
  under q<=0.20, mainly in immune-tone-plus-batch and normalization-depth
  scenarios. The current stricter effect-threshold guard remains operative.
- Next selected task: Karolinska-specific preregistration addendum template.
- Karolinska-specific preregistration template completed. It pre-specifies that
  Karolinska is secondary late-timepoint/platform stress testing only unless
  unexpected early/PBMC-equivalent data arrive, and it forbids any outcome
  scoring before author labels/mapping are received, checksummed, and a
  finalized addendum is committed.
- Next selected task: validation intake preflight script for quarantine,
  checksums, schemas, and response-label guardrails.
- Validation intake preflight completed. `scripts/v45_validation_intake_preflight.py`
  checks package checksums, frozen metadata schemas, optional expression sample
  IDs, and response-label guardrails before any frozen harness runs. Synthetic
  verification passed the primary and pharmacodynamic packages and failed a
  pharmacodynamic package containing a response-like column, as intended.
- Backlog refilled above the executable threshold with intake-regression,
  outbound-request, synthetic-index, command-dry-run, power-table, and external
  methods-update tasks.
- Next selected task: GSE228330 pharmacodynamic-only acquisition/runbook for the
  context harness.
- GSE228330 pharmacodynamic-only runbook completed. The public 5.1 MB series
  file resolves but is an annotation/probe table, not expression; the 1.8 GB raw
  archive resolves and would need CEL reprocessing. The draft metadata is
  explicitly marked `inferred_unverified` because the public subject-pairing map
  is not confirmed. No response-validation use is allowed.
- Next selected task: APC convergence sensitivity excluding validation/readiness
  artifacts generated after V42.
- No-readiness convergence sensitivity completed. The V41 integrated evidence
  frame contains `0` post-V42 validation/readiness rows, so V45 readiness
  artifacts cannot inflate the convergence object. With the same recurrence
  formulations, `apc_hla_ifn_monitoring` remains rank `1` and all FWER p-values
  are at the `20,000`-replicate floor.
- Next selected task: update skeptical external checklist with V45 secondary
  harness and request-tracker readiness claims.
