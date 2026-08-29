# V57 Outcome-Blind Cohort-Shift Preflight: Frozen Plan

Status: **frozen before outcome analysis**

## Purpose

Test a new validation method: detect whether a held-out cohort occupies a
different module-delta distribution before using response labels. This is a
diagnostic around the frozen V22 validation, not a rule change and not a
biological finding.

## Fixed Data and Features

- Use the same four held cohorts and audited patient rows as the V57
  environment-stability probe.
- Use exactly three nonredundant early-change components:
  `delta_IFN_APC`, `delta_HLAII`, and `delta_RECEPTOR`.
- Do not use response labels in representation, scaling, distance, or the
  shift test.
- Scale each feature by the global outcome-blind median and IQR. An IQR of
  zero is replaced by one.

## Primary Shift Statistic

For each cohort versus the pooled other three, compute multivariate energy
distance. Generate 200,000 global cohort-label permutations preserving all
four cohort sizes, seed 57041. Correct the four-cohort family with the maximum
energy statistic.

A cohort is flagged out-of-distribution (OOD) when its max-statistic FWER
p-value is <= 0.10. The diagnostic does not invalidate or rescue its outcome
result; it marks transport interpretation as unsafe.

## Sensitivity

Compute an unbiased radial-basis-kernel maximum mean discrepancy (MMD) using
the pooled median nonzero squared distance as the fixed bandwidth. Run the
same global-label permutations and four-cohort max-statistic correction.
Concordant energy/MMD flags are stronger diagnostics. MMD is sensitivity and
does not expand the primary family.

## Prospective Use

The implementation is reusable for a new cohort only after gene/module and
timepoint eligibility checks. It must run before outcome labels are opened.
It cannot tune the locked score, choose exclusions, or alter pre-registered
success thresholds.
