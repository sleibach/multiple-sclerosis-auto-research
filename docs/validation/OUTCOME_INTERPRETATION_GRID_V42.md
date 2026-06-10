# OUTCOME INTERPRETATION GRID V42: Gafson DMF/NEDA Validation

Status: **pre-committed while blind to the Gafson validation data**
Date: 2026-06-10
Applies to: `docs/validation/PREREGISTRATION_V42.md` and the immutable
`docs/locked_rules/LOCKED_RULE_V22.md`

This grid fixes what each possible Gafson result means before expression or
NEDA-4 labels are visible. It prevents interpreting any result as confirmation
after the fact.

## Fixed Result Classes

| Result class | Mechanical condition | Interpretation |
|---|---|---|
| `PASS_CLEAN` | Primary V22 score meets the V42 pass threshold; receptor-only does not outperform by AUC `>= 0.10`; key confounder families are `SURVIVES` or only mild `ATTENUATES` | Strengthens the DMF/MS Class C early-monitoring lead. It validates a pharmacodynamic monitoring signal in this cohort, not a pretreatment stratifier and not a clinical decision threshold. |
| `PASS_IMMUNE_TONE_BOUNDED` | Primary V22 score meets pass threshold, but metabolic/inflammatory/STAT1 adjustment is `ATTENUATES`; steroid and cell-composition families do not explain it away | Supports the V32 interpretation: the signal is real but immune-tone bounded. It should be framed as an early immune-remodeling/pharmacodynamic readout, not a purely APC/HLA-II-specific biomarker. |
| `PASS_NON_SPECIFIC` | Primary V22 score passes, but receptor-only outperforms by AUC `>= 0.10` or a composition/control audit is `EXPLAINED_AWAY` | Does not validate the intended APC/HLA-II monitoring biology. The result is downgraded to non-specific immune-state tracking unless a separate pre-registered explanation exists. |
| `FAIL_ADEQUATE_POWER` | Data are scoreable with adequate sample size and the primary score has AUC `< 0.60`, signed Hedges g `< 0.20`, or opposite direction under V42 criteria | Weakens or may close the DMF/MS Class C validation path. It does not automatically refute all therapy classes in V22, but it makes the Gafson/DMF branch a negative result. |
| `INCONCLUSIVE_UNDERPOWERED` | Data are scoreable but sample size, class balance, or CI width cannot support pass or fail | No validation claim. Report effect size and CI for future power planning. Do not upgrade or kill the lead. |
| `UNSCOREABLE_DATA` | Missing paired samples, missing NEDA-4, failed module coverage, or unusable metadata prevents primary scoring | No validation occurred. Treat as a data-acquisition or compatibility failure, not as a biological result. |

## Clean Pass

If `PASS_CLEAN`:

- Established: the immutable V22 Class C early delta score predicts NEDA-4
  response in an independent DMF MS cohort under the pre-registered harness.
- Not established: clinical utility, baseline patient selection, durable
  treatment switching threshold, mechanism specificity, or generalization to
  all MS DMTs.
- Required next step: prospective or independently acquired validation with
  enough labeled responders and nonresponders to estimate a stable clinical
  threshold and decision-curve utility.
- Project update: move the treatment-response lead from provisional to
  externally supported for DMF early monitoring, while retaining the
  immune-tone and mechanism-bounded caveats.

## Pass With Immune-Tone Attenuation

If `PASS_IMMUNE_TONE_BOUNDED`:

- Established: the locked score contains response-predictive information in
  Gafson, but part of the signal overlaps the metabolic/inflammatory/STAT1
  context identified in V32.
- Not established: an APC/HLA-II-specific mechanism independent of broader
  immune tone.
- Required next step: future validation must measure both the V22 score and the
  confounder panels; clinical use would require a two-output report: locked
  monitoring score plus immune-tone context.
- Project update: strengthen the monitoring lead but narrow the biological
  interpretation to an immune-remodeling state. Do not call it a clean APC
  biomarker.

## Raw Pass But Non-Specific Control Wins

If `PASS_NON_SPECIFIC`:

- Established: a dynamic expression signal tracks response in this cohort.
- Not established: the V22 APC/HLA-II biology. A receptor-only, composition, or
  control signal may be carrying the association.
- Required next step: do not promote the rule clinically. Treat the cohort as a
  warning that the signal may be a generic immune-state proxy unless future
  data separate specificity.
- Project update: downgrade the V22 interpretation and add the result to the
  specificity-risk ledger. It is not a clean validation.

## Adequately Powered Fail

If `FAIL_ADEQUATE_POWER`:

- Established: the Gafson DMF/NEDA cohort does not support the immutable V22
  Class C score under the pre-registered test.
- Not established: failure of IFN-beta Class B, cytokine/JAK Class A, or
  every possible APC/HLA-II-related monitoring readout.
- Required next step: update the V22/V23 validation ledger. If the fail
  completes the V22 kill criteria across reachable MS DMT cohorts, write the
  corresponding kill update. If not, bound the rule away from DMF/NEDA.
- Project update: demote the treatment-response lead for DMF. Do not rescue it
  by changing timepoint, endpoint, sign, module genes, or fitted weights.

## Opposite-Direction Result

If the primary score is strongly opposite direction:

- If AUC `< 0.45` with adequate sample size, classify as
  `FAIL_ADEQUATE_POWER`.
- Interpret as evidence against the locked Class C generalization in DMF.
- Do not flip the sign or re-label nonresponders as responders.
- Report whether confounders explain the inversion; the inversion itself
  remains a primary failure.

## Inconclusive Result

If `INCONCLUSIVE_UNDERPOWERED`:

- Established: only an effect estimate and uncertainty interval.
- Not established: validation, kill, or clinical usefulness.
- Required next step: use the observed AUC/g and CI to power the next cohort.
- Project update: keep the lead provisional. Do not classify as pass because
  the point estimate is favorable, and do not classify as kill because the CI is
  wide.

## Unscoreable Data

If `UNSCOREABLE_DATA`:

- Established: the acquired data package cannot test V22 under this plan.
- Not established: any biological property of DMF response.
- Required next step: request the missing field or a replacement cohort. The
  missing component must be named precisely: paired early timepoint, NEDA-4
  label, module gene coverage, feature annotation, or QC/metadata.
- Project update: no evidence-grade change.

## Confounder-Specific Interpretation

| Confounder outcome | Meaning |
|---|---|
| Steroid/glucocorticoid `EXPLAINED_AWAY` | Treat as a critical vulnerability. The signal may reflect steroid exposure or glucocorticoid biology rather than DMF response. Do not promote without direct medication metadata replication. |
| Cell-composition `EXPLAINED_AWAY` | Treat as a composition artifact risk. The result supports changing cell mixture, not within-cell APC/HLA-II state, unless single-cell or sorted validation separates the two. |
| Metabolic/inflammatory/STAT1 `ATTENUATES` | Expected under V32. Interpret as immune-tone bounded, not automatically artifact. |
| Metabolic/inflammatory/STAT1 `EXPLAINED_AWAY` | Downgrade to broad immune-tone proxy. The V22 feature may still monitor pharmacodynamics but is not biologically specific enough for target/mechanism claims. |
| Baseline state explains delta | The result does not validate an early-monitoring rule. It becomes a possible baseline-stratification hypothesis only if separately locked and validated elsewhere. |

## Minimum Report Language

Every Gafson validation report must include one of these sentences:

- "The cohort produced a clean pre-registered pass of the immutable V22 Class C
  early-monitoring rule."
- "The cohort produced a pre-registered pass, but the signal is immune-tone
  bounded and must not be interpreted as APC/HLA-II-specific."
- "The cohort produced a non-specific pass because the negative/control or
  confounder audit outperformed or explained the locked score."
- "The cohort failed the immutable V22 Class C rule under adequate scoring
  conditions."
- "The cohort was inconclusive and supplies only an effect-size estimate for
  future power planning."
- "The cohort was unscoreable for the primary validation."

## What This Grid Does Not Permit

This grid does not permit:

- changing the V22 rule;
- fitting a Gafson-specific threshold;
- changing NEDA-4 to another endpoint after seeing data;
- treating confounder-adjusted success as the primary pass if the raw locked
  score fails;
- treating a single clean Gafson pass as clinical readiness;
- hiding a fail behind a favorable secondary audit.

The grid is deliberately conservative. Its job is to make the validation mean
one thing no matter what the data show.
