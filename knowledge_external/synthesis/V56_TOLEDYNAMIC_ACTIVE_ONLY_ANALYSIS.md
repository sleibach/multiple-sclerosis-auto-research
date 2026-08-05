# V56 ToleDYNAMIC Active-Only Analysis And Interpretation

Status: frozen pre-data Branch B plan. No ToleDYNAMIC assay value or
participant-level outcome has been obtained or viewed.

Boundary: `external-verifiable`; `NOT_PROJECT_GROUNDED`. Design source:
https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf. Date
accessed: 2026-08-05.

## Design Boundary

[`external-verifiable`; `NOT_PROJECT_GROUNDED`; source:
https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf]
Appendix 11 repeatedly describes samples from tolebrutinib-treated participants
before treatment and after initiation at months 3 and 12; it does not describe
placebo sampling. Therefore the public-design default is active-treatment-only.

The analysis below characterizes temporal trajectories observed under exposure.
It cannot separate treatment from time, regression to the mean, study
participation, selection, concomitant care, or unmeasured technical change. It
must not emit a randomized treatment effect, causal mechanism, clinical
mediation, CNS target-engagement, or individual treatment-response claim.

The machine contract is
`docs/validation/TOLEDYNAMIC_DESIGN_BRANCH_LOCK_V56.json`, canonical SHA-256
`1d7734fcc094b9a0fd975f92c53d2cc80a9358d4c2ecce0a139bf45f41e945c9`.
It binds the unchanged 18-slot module lock SHA-256
`6c34df056bd764850dd30173116c6c4162213b56fb3bd72bcc165a94b855c77d`.

## Current Extension Context

- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://clinicaltrials.gov/study/NCT06372145] The official extension registry is active, nonrandomized, open-label, and estimates completion in April 2029; no results are posted.
- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://clinicaltrials.gov/study/NCT06372145] It names ToleDYNAMIC, lists biomarker change from extension baseline through 12 months, and states that participants from the progressive-MS parent trials start open-label tolebrutinib.
- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://clinicaltrials.gov/study/NCT06372145] Qualified researchers may request participant-level data and documents through Vivli, but that policy does not establish current availability of an ongoing substudy package.

The relation between HERCULES Appendix 11 sampling and the extension registry's
ToleDYNAMIC sampling is not public. They may be continuous, transferred, or
distinct protocol periods. This must be resolved before selecting a baseline or
analysis population.

## Value-Blind Release Gates

Run before reading expression, function, or clinical outcomes:

1. `scripts/v56_toledynamic_intake_classifier.py` must assign
   `BRANCH_B_DESCRIPTIVE_ONLY`; Branch C or terms-blocked packages stop.
2. `scripts/v56_toledynamic_sample_preflight.py` must establish unique
   participant/visit records and eligible baseline-month-3 pairs separately by
   parent trial, assay, and cell type.
3. RNA-subset selection, visit missingness, site, processing delay, plate,
   batch, and assay-failure reasons must be tabulated without outcomes.
4. Perfect visit-by-batch confounding blocks inferential trajectory testing for
   that assay. Partial confounding is reported and requires the fixed adjusted
   sensitivity below.
5. The functional endpoint map must pass
   `scripts/v56_toledynamic_functional_mapping_gate.py` before functional
   values are read.

No post-value exclusion, endpoint substitution, or family shrinkage is allowed.

## Frozen Transcript Analysis

### Representation

- Analyze HERCULES and PERSEUS separately; never pool them to create power.
- Analyze sorted B cells and CD14 monocytes separately.
- Use the nine modules, gene membership, score direction, coverage rule, and
  18-slot family in `TOLEDYNAMIC_MODULE_LOCK_V56.json` without substitution.
- When raw integer counts are available, use package-wide TMM library-size
  factors and log2 counts per million with prior count `0.5`, within each parent
  trial and cell type. Standardize each retained gene using the eligible
  baseline samples' mean and sample standard deviation, then apply those fixed
  baseline parameters to month 3 and month 12. A zero-baseline-variance gene is
  nonvariable under the frozen coverage rule.
- If raw counts are unavailable, use only a sponsor-SAP frozen normalized
  matrix with documented gene identifiers. Label this a representation
  sensitivity and do not combine it with a raw-count result.
- The MOCCI score is baseline-standardized `C15ORF48 - NDUFA4`; other modules
  are the mean of baseline-standardized available frozen genes.

### Primary family

For each participant and valid slot, calculate month-3 minus baseline score.
The observed statistic is the studentized mean paired change. Generate at least
`100,000` joint participant-level sign-flip permutations, using the same sign
for all slots from a participant so cross-module dependence is retained. The
family statistic is the maximum absolute studentized statistic across every
valid slot in the original 18-slot universe. Monte Carlo p-values use the
plus-one correction.

If outcome-blind technical covariates are identifiable, residualize paired
change on the frozen site and assay-batch terms under the null and sign-flip
participant residual vectors jointly. Report unadjusted and adjusted results;
neither may rescue perfect visit-by-batch confounding.

A HERCULES slot is a **robust temporal trajectory** only when all hold:

1. max-T family-wise p `< 0.05`;
2. a `10,000`-resample participant bootstrap 95% interval excludes zero;
3. every leave-one-participant-out estimate retains direction; and
4. the result retains direction under the frozen technical-covariate
   sensitivity where that model is identifiable.

PERSEUS receives the unchanged genes, cell type, score, direction, visit, and
18-slot denominator. Cross-trial concordance requires the same direction, a
bootstrap interval excluding zero, leave-one-out sign stability, and nominal p
`< 0.05/18`. It is not randomized replication.

Month 12 tests durability with the same family and cannot rescue month 3.

### Secondary initiation-versus-continuation contrast

If complete parent-arm and exposure metadata show both former-placebo
participants initiating open-label tolebrutinib and former-tolebrutinib
participants continuing it, estimate the difference in paired month-3 change
between those groups. This is secondary to the within-participant trajectory.
It compares early exposure with continued exposure among selected rollover and
substudy survivors; it is not a current randomized drug-versus-placebo effect.

The contrast is released only when all are available: a parent-arm rollover
CONSORT from randomization through extension eligibility, extension enrollment,
substudy consent, and paired assay completion; actual exposure/interruption and
washout; reasons and dates for every selection step; parent-exit and extension-
baseline clinical covariates with common support; and laboratory blinding to
parent arm. Report standardized covariate balance and stop if positivity fails.

Use the same fixed 18-slot max-T family. In addition to the unadjusted contrast,
report a prespecified parent-exit/baseline adjusted estimate, inverse-probability
weights for observed extension/substudy participation when the parent
denominator is available, quantitative selection-bias bounds, leave-one-site-
out and leave-one-batch-out estimates, and placebo-era slope subtraction if
compatible pre-extension molecular samples exist. A nonzero trajectory among
continuers directly falsifies a simple steady-state-reference interpretation.

Allowed wording is `selection-conditional initiation-versus-continuation
trajectory`. Parent randomization does not erase post-trial survivor selection,
differential prior exposure, open-label behavior, or extension/substudy
selection. Do not use `treatment effect`, `placebo-controlled`, or `causal`.

## Frozen Functional Analysis

Analyze only endpoints admitted by the blinded functional mapping gate:
myelin-phagocytosis capacity, CD64 abundance/intensity, ROS, basal and spare
respiratory capacity, and a sponsor-SAP-designated primary inflammatory
cytokine summary if one exists. Apply the same joint paired sign-flip max-T,
bootstrap, leave-one-out, and technical sensitivity rules as a separate family.

`Functionally concordant trajectory` is allowed only when a transcript slot and
its prespecified functional anchor independently pass their own corrected
families in the same trial and frozen direction. This phrase does not mean
treatment mechanism or mediation.

## Clinical Link: Estimation Only

For a cross-trial-concordant trajectory, estimate its continuous association
with the fixed 24-month EDSS-only progression endpoint separately in HERCULES
and PERSEUS. Report effect estimates, full intervals, participant count,
missingness, and influence diagnostics. Do not define a cutoff, select a
subgroup, train a classifier, or use a clinical association to upgrade a
trajectory. The estimate cannot establish that the trajectory mediates a
treatment effect.

## Precommitted Result Grid

| HERCULES | PERSEUS | function | permitted interpretation |
|---|---|---|---|
| pass | same-direction pass | pass in matched families | Functionally concordant temporal trajectory under exposure across two progressive-MS contexts; it is not a randomized effect or mechanism and cannot alone explain divergent parent-trial efficacy. |
| pass | same-direction pass | fail/unavailable | Cross-trial-concordant transcript trajectory; functional relevance unestablished. |
| pass | fail | any | HERCULES-context trajectory or substudy-selection result; no shared progression-treatment mechanism. |
| fail | pass | any | PERSEUS-only trajectory; the prespecified HERCULES-first route does not advance. |
| fail | fail | any | No detectable frozen month-3 trajectory in the available package; interpret against the achieved-sample power envelope. |
| any | opposite-direction pass | any | Cross-trial contradiction; no common trajectory and no favorable mechanistic narrative. |
| invalid/confounded | any | any | Assay-level no-result; request repair or report the data limitation. |

The first row is evidence that the measured peripheral trajectory is not a
context-independent marker sufficient to distinguish the two trial contexts:

- [`external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: https://pubmed.ncbi.nlm.nih.gov/40202696/] the published HERCULES aggregate primary progression outcome favored tolebrutinib; and
- [`external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: https://www.sanofi.com/en/media-room/press-releases/2025/2025-12-15-06-05-00-3205094] Sanofi reported that PERSEUS did not significantly delay disability progression.

Disease-stage, selection, and unmeasured contextual differences remain
unresolved. A shared trajectory is not proof that the trajectory is
biologically irrelevant.

## Power Boundary

Seeded method simulations are in
`docs/validation/TOLEDYNAMIC_POWER_ENVELOPE_V56.md`. With 40 paired participants,
a standardized temporal change of `0.8` has simulated family-wise power
`0.961-0.982`; with an RNA subset of 10, even a change of `1.2` has power only
`0.466-0.535`. A corrected null in a small RNA subset is therefore
inconclusive, whereas a null in a complete 40-participant functional assay can
exclude only large trajectories under the simulation assumptions. These are
synthetic method properties, not biological effects.

## What Would Upgrade The Design

Only sponsor documentation showing placebo samples, outcome-blind substudy
selection, paired baseline/month-3 coverage in both randomized arms, and no
arm-by-batch aliasing can route the package to Branch A. That branch uses the
randomized treatment-by-time contrast already frozen in the original module
lock. Favorable assay values cannot change the branch.
