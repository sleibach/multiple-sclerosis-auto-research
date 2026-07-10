# Therapeutic Validation Handoff V52

Date: 2026-07-10

Status: additive readiness synthesis only. This document does not change
`docs/locked_rules/LOCKED_RULE_V22.md`, `docs/validation/PREREGISTRATION_V42.md`,
or `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`.

## Purpose

V52 concludes that the defensible near-term MS impact route is validation of an
early treatment-response monitoring / stratification signal, not a direct
therapeutic target. This handoff states exactly what Gafson, Karolinska, or an
equivalent cohort would need to show to make that route actionable.

## What A Successful Validation Would Mean

| validation result | clinically relevant meaning | what it would not establish |
|---|---|---|
| `PASS_CLEAN` under V42/V44 | The immutable V22 Class C score is externally supported as an early DMF-like pharmacodynamic monitoring readout in that cohort. | It is not a baseline patient-selection rule, not a clinical treatment-switching threshold, not a durable response guarantee, and not a drug target. |
| `PASS_IMMUNE_TONE_BOUNDED` | The signal is useful as an early immune-remodeling monitor with required immune-tone context. | It is not a clean APC/HLA-II-specific mechanism claim and cannot be used without confounder reporting. |
| `PASS_NON_SPECIFIC` | Some dynamic immune-state signal tracks response, but the intended V22 biology is not validated. | It should not be promoted as the project monitoring rule. |
| `INCONCLUSIVE_UNDERPOWERED` | The cohort contributes an effect-size and CI estimate for designing the next validation. | It is neither a pass nor a kill. |
| `FAIL_ADEQUATE_POWER` | The DMF/MS Class C branch is materially weakened under the frozen rule. | It does not refute every therapy class or permit post-hoc score revision. |
| `UNSCOREABLE_DATA` | The package cannot test the rule mechanically. | It is not biological evidence for or against the signal. |

## Minimum Data Package To Make The Result Actionable

The next useful validation package must contain:

1. Paired baseline and early on-treatment PBMC expression for each subject.
2. Subject-level NEDA-4 or pre-specified equivalent response labels.
3. Feature identifiers mappable to official gene symbols with V22 module
   coverage.
4. Batch/QC metadata sufficient for the V44 additive batch guard.
5. Steroid, relapse, infection, DMT timing, and cell-count metadata where
   available, so the V32 confounder panels can be interpreted.
6. Enough labeled responders and nonresponders to avoid a purely directional
   result where possible.

The V43 power map remains the design anchor: a cohort intended to settle the
rule should aim for at least `30` responders and `30` nonresponders when the
true effect is about `1.0` and labels are clean, with larger groups preferred
under label noise or immune-tone/composition confounding.

## Gafson / Karolinska Decision Path

| data route | if available | if delayed or incomplete |
|---|---|---|
| Gafson DMF PBMC/NEDA-4 | Run the frozen V42/V44 harness only; report one of the V42 pre-committed result classes. | Do not substitute endpoints or tune the rule. Record the missing component and keep pursuing a complete package. |
| Karolinska DMF labels / package | Treat as a parallel validation route only after paired structure, labels, and module coverage are verified. | Use it for package-readiness and returned-data handling only; do not count it as validation without the required fields. |
| GSE235357 or other DMF context source | Use only if sample-level paired response labels and compatible expression can be verified. | Keep as pharmacodynamic/context source; do not treat metadata or literature context as validation. |

## How V52 Changes Readiness

V52 adds therapeutic framing, not new validation degrees of freedom:

- The monitoring lead is the first priority because it is the only route that
  could become clinically useful from the next external cohort.
- The chr1 KIF21B/GPR25 route remains a target-development handoff, not a
  validation substitute.
- AlphaFold structure context does not affect the validation harness.
- Restored OpenGWAS access is not required for Gafson/Karolinska scoring, but
  can support bounded genetics checks outside the validation run.

## Medical-Team Actionable Ask

Request a validation package that satisfies the V42 input spec and explicitly
ask for:

- sample-level NEDA-4 labels and assessment window;
- baseline and earliest eligible on-treatment timepoint per subject;
- raw or documented normalized expression matrix;
- feature annotation;
- batch/QC fields;
- steroid/relapse/infection/cell-count metadata where available.

If the available cohort is below the V43 powered-design target, treat it as an
effect-size estimation cohort and pre-plan a larger follow-up rather than
forcing a pass/fail interpretation.
