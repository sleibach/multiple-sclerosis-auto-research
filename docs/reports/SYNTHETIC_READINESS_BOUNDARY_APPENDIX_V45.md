# Synthetic And Readiness Boundary Appendix V45

Status: skeptical external-facing appendix. Synthesis only; no new analysis,
hypothesis, rule, or validation claim.

## Purpose

This appendix states the boundary between method/readiness evidence and
biological validation. It is meant to prevent the strongest V43-V45 operational
work from being misread as evidence that the APC/HLA-II monitoring rule has
been externally validated.

The short version:

> Synthetic and readiness outputs can prove that the project knows how to run,
> audit, power, and stress-test a frozen validation. They cannot prove that the
> rule works in MS patients.

## Evidence Classes

| Class | Examples | What it can support | What it cannot support |
|---|---|---|---|
| Real cohort evidence | `docs/validation/VALIDATION_LEDGER_V22.md`, `docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md` | empirical signal estimates in the cohorts actually analyzed | external Gafson/Karolinska validation before those data arrive |
| Locked-rule and preregistration evidence | `docs/locked_rules/LOCKED_RULE_V22.md`, `docs/validation/PREREGISTRATION_V42.md`, `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md` | that the rule and interpretation were frozen before the future test | that the future test will pass |
| Synthetic method-characterization | `docs/validation/POWER_MAP_V43.md`, `docs/validation/HARNESS_ROBUSTNESS_V43.md`, `docs/validation/BATCH_GUARD_CALIBRATION_FULL_V45.md`, `docs/validation/SEED_VARIATION_STABILITY_V45.md` | power, false-positive behavior, seed stability, and data-quality envelopes under stated simulated conditions | MS biology, clinical response effect sizes, or real cohort usability |
| Synthetic harness and intake verification | `analysis/v42_harness_validation/`, V45 preflight/regression outputs | that software gates fail/pass the intended synthetic cases | that a real package will be complete, analyzable, or positive |
| Readiness and operations | `docs/validation/V45_OPERATIONAL_HANDOFF_INDEX.md`, `docs/validation/CURRENT_ACTION_CARD_V45.md`, `docs/validation/EXTERNAL_BLOCKER_BOARD_V45.md` | that the project has an auditable route from receipt to frozen run | any treatment-response result |
| Internal convergence support | `docs/validation/APC_HLA_INTERNAL_CONVERGENCE_V44.md`, `docs/validation/APC_HLA_CONVERGENCE_SENSITIVITY_V45.md`, `docs/validation/APC_HLA_NO_REPORTS_CONVERGENCE_V45.md`, `docs/validation/APC_HLA_NO_READINESS_CONVERGENCE_V45.md` | that the APC/HLA/IFN axis recurs across the committed corpus under internal nulls | clinical validity or prospective utility |
| Model/RPT outputs | V31/V36/V45 lens outputs where present | proposal prioritization only, followed by grounding if used | facts, evidence, or validation |

## Correct Claims

It is correct to say:

- the V22 scalar rule is locked and immutable;
- the Gafson analysis is preregistered and mechanically specified;
- synthetic null/planted checks show the harness behaves as expected on seeded
  non-real fixtures;
- V43/V45 simulations estimate when a cohort is likely to be conclusive;
- synthetic batch and metadata stress tests define warning conditions under
  which a future validation should be downgraded or blocked;
- internal convergence remains robust after duplicate/source-family and
  readiness-circularity checks;
- these strengthen readiness and skepticism before external validation.

It is not correct to say:

- V43, V44, or V45 synthetic outputs validate the biological rule;
- a synthetic planted signal is evidence that MS patients carry the signal;
- readiness dashboards or command plans are response evidence;
- internal convergence replaces an external paired treatment-response cohort;
- Gafson, Karolinska, or GSE228330 results are known before the frozen real
  harness is run on received, preflight-passing data;
- pharmacodynamic-only context data are response validation without mapped
  response outcomes and a blinded addendum.

## Why Synthetic Outputs Were Still Worth Producing

The V43-V45 synthetic outputs answer method questions that cannot be answered by
waiting for one delayed cohort:

- how large a clean cohort must be to make a conclusive pass/fail likely;
- how often response-correlated batch can generate a false clean pass under
  explicit null conditions;
- whether the frozen harness rejects null fixtures and accepts planted-signal
  fixtures;
- which missingness, label, timepoint, or metadata pathologies make a future
  result uninterpretable;
- whether method-behavior conclusions are stable across seed families rather
  than cherry-picked.

Those are prerequisites for an interpretable validation. They are not the
validation itself.

## External-Writing Rules

When writing an abstract, manuscript, slide, or medical-team note:

1. Put the real status before the readiness status: "provisional monitoring
   lead awaiting external validation" comes before "harness hardened."
2. Place synthetic and readiness outputs in methods, limitations, or validation
   planning sections, not in a biological results section.
3. Attach the phrase "method behavior only" or equivalent whenever citing a
   synthetic stress test.
4. Keep internal convergence separate from clinical validation.
5. State that no V45 output changed `LOCKED_RULE_V22.md`,
   `PREREGISTRATION_V42.md`, or the V42 interpretation grid.
6. If a future real cohort passes only after ignoring a V45 warning condition,
   report that as a downgraded or non-clean result, not as rescue.

## Reviewer Red-Flag Phrases

Avoid these phrases unless a future real validation has actually produced the
corresponding evidence:

- "validated biomarker";
- "validated NEDA predictor";
- "synthetic validation";
- "clinical utility demonstrated";
- "Gafson-ready therefore Gafson-positive";
- "batch-safe" without the specific guard status;
- "response validation" for a context-only or label-missing cohort.

Preferred replacements:

- "validation-ready";
- "synthetic method-characterization";
- "internal convergence support";
- "pre-registered external test pending";
- "batch guard passed/flagged";
- "context-only pharmacodynamic evidence."

## Bottom Line For Reviewers

V45 increases trust in the eventual validation process by reducing degrees of
freedom, clarifying blockers, stress-testing the harness, and quantifying power
and failure modes. It does not increase the number of real externally validated
patients. The project remains scientifically stronger because it made that
distinction explicit before the delayed data arrive.
