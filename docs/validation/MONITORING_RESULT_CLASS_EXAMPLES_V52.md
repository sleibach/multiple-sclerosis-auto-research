# Monitoring Result Class Examples V52

Date: 2026-07-10

Status: operational examples. This document adds no evidence, changes no
threshold, and does not alter the V42/V44 validation plan. It gives examples
of how future package outcomes should map to the pre-committed monitoring
result classes.

## Purpose

The V42 outcome grid and V52 wording table define the classes. This document
adds concrete examples so operators do not reinterpret ambiguous future results
after seeing a cohort.

## Examples

| scenario | result class | why | allowed public wording | not allowed |
|---|---|---|---|---|
| Complete paired PBMC/NEDA package; frozen score meets V42 pass threshold; receptor-only and batch/confounder audits do not invalidate. | `PASS_CLEAN` | The locked score passes and specificity/batch warnings do not bind the result. | "The frozen V22 early-treatment score externally supported an early pharmacodynamic monitoring readout in this cohort." | "This is a clinical treatment-switching rule." |
| Complete package; frozen score passes; metabolic/inflammatory/STAT1 adjustment attenuates but steroid and simple composition do not explain away. | `PASS_IMMUNE_TONE_BOUNDED` | This matches the V32 immune-tone-bounded interpretation. | "The frozen score passed, but interpretation is immune-tone bounded and requires confounder reporting." | "The cohort proves a pure APC/HLA-II mechanism." |
| Frozen score passes, but a receptor-only or broad immune-state control outperforms by the pre-specified margin. | `PASS_NON_SPECIFIC` | Response information exists, but intended V22 biology is not specifically validated. | "A dynamic immune-state signal tracked response, but the intended V22 biology was not specifically validated." | "The locked scalar validated as intended." |
| Scoreable package with favorable point estimate, but class balance or CI width misses the pre-committed pass/fail requirements. | `INCONCLUSIVE_UNDERPOWERED` | The cohort estimates effect size but cannot settle the rule. | "The cohort was informative for effect size and uncertainty but did not settle the rule." | "Trend-level validation." |
| Scoreable and adequately powered package; frozen score AUC is below the V42 fail threshold or direction is opposite under the locked orientation. | `FAIL_ADEQUATE_POWER` | The pre-registered rule fails in the tested context. | "The frozen V22 rule failed in an adequately powered scoreable cohort under the pre-registered criteria." | "We can rescue the rule by changing sign, endpoint, or timepoint." |
| Package has expression but no subject-level response label. | `UNSCOREABLE_DATA` | The primary endpoint cannot be reconstructed after receipt. | "The package could not test the rule because required data fields were missing or incompatible." | "The validation was negative." |
| Package has response labels and treatment timepoints, but feature annotation fails module coverage. | `UNSCOREABLE_DATA` | The frozen modules cannot be scored. | "The package could not test the rule because module coverage failed." | "The biology failed." |
| Package has baseline and treatment samples but the treatment sample is outside the pre-specified timing window. | `UNSCOREABLE_DATA` or context-only | The locked early delta is not available. | "The package is not eligible for primary validation; it may be pharmacodynamic context only if separately routed." | "Late-treatment data validate the early rule." |
| Package is technically complete but harness has not yet been run. | `TECHNICAL_SCOREABLE_ONLY` | Scoreability is not validation. | "The package is analyzable; no predictive claim follows from scoreability alone." | "Validation-ready means validated." |

## Decision Rule

When a future case seems to fit two rows, choose the more conservative class.
For example, a raw pass with a serious batch warning is not a clean pass; an
underpowered favorable point estimate is not a pass; an unscoreable package is
not a fail.

## Source Artifacts

- `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md`
- `docs/validation/MONITORING_PUBLIC_WORDING_TABLE_V52.tsv`
- `docs/validation/VALIDATION_PACKAGE_FIELD_DICTIONARY_V52.tsv`
- `docs/validation/MONITORING_CLINICAL_UTILITY_BOUNDARY_CHECKLIST_V52.md`

