# Validation Result Report Template V45

Status: report template. No validation has been run by this template.

Purpose: provide a fixed reporting structure for any future frozen-harness
validation result, especially Gafson DMF/NEDA-4, so the result is interpreted
through the pre-committed V42 outcome grid rather than post-hoc framing.

Copy this template to:

```text
analysis/validation_runs/<cohort>/VALIDATION_RESULT_REPORT.md
```

and fill only the bracketed fields after the frozen harness and gate checks
complete.

## Required Header

```text
Cohort: [cohort_id]
Role: [primary_gafson | karolinska_secondary | gse228330_context_only | gse228330_labeled_secondary | other_preregistered]
Frozen rule/preregistration: [path]
Locked hash audit: [PASS/FAIL, path]
Pre-commit readiness: [PASS/FAIL, path]
Harness command: [exact command]
Date run UTC: [timestamp]
Operator: [name/initials]
```

## Gate Status

| Gate | Status | Evidence path | Notes |
|---|---|---|---|
| data-use terms approved | `[PASS/FAIL/NA]` | `[path]` | `[notes]` |
| checksum manifest verified | `[PASS/FAIL/NA]` | `[path]` | `[notes]` |
| outcome dictionary frozen | `[PASS/FAIL/NA]` | `[path]` | `[notes]` |
| intake preflight passed | `[PASS/FAIL/NA]` | `[path]` | `[notes]` |
| module coverage precheck passed | `[PASS/FAIL/NA]` | `[path]` | `[notes]` |
| subject-map sanity passed | `[PASS/FAIL/NA]` | `[path]` | `[notes]` |
| preregistration/addendum committed | `[PASS/FAIL/NA]` | `[path]` | `[notes]` |
| locked-artifact hash audit passed | `[PASS/FAIL/NA]` | `[path]` | `[notes]` |
| synthetic/software regression passed | `[PASS/FAIL/NA]` | `[path]` | `[notes]` |

If any required gate is `FAIL`, stop here. Report `UNSCOREABLE_DATA` or
operational blocker as appropriate. Do not report a biological result.

## Primary Result Metrics

Fill from frozen harness outputs only.

| Metric | Value | Source file |
|---|---:|---|
| labeled paired subjects total | `[n]` | `[sample_attrition.tsv / validation_summary.json]` |
| responders | `[n]` | `[source]` |
| nonresponders | `[n]` | `[source]` |
| locked V22 AUC | `[value]` | `locked_rule_metrics.tsv` |
| AUC 95% CI lower | `[value]` | `locked_rule_metrics.tsv` |
| AUC 95% CI upper | `[value]` | `locked_rule_metrics.tsv` |
| signed Hedges g | `[value]` | `locked_rule_metrics.tsv` |
| permutation p value | `[value]` | `locked_rule_metrics.tsv` |
| receptor/control AUC | `[value/NA]` | `locked_rule_metrics.tsv` |

## V42 Result Class

Select exactly one:

- `[ ] PASS_CLEAN`
- `[ ] PASS_IMMUNE_TONE_BOUNDED`
- `[ ] PASS_NON_SPECIFIC`
- `[ ] FAIL_ADEQUATE_POWER`
- `[ ] INCONCLUSIVE_UNDERPOWERED`
- `[ ] UNSCOREABLE_DATA`

The selected class must follow
`docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`.

## Required Interpretation Sentence

Copy exactly one sentence and delete the others:

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

## Confounder And Batch Interpretation

| Audit | Status | Effect on interpretation | Source file |
|---|---|---|---|
| glucocorticoid/steroid | `[SURVIVES/ATTENUATES/EXPLAINED_AWAY/UNSCOREABLE]` | `[text]` | `confounder_adjustment_metrics.tsv` |
| cell composition | `[SURVIVES/ATTENUATES/EXPLAINED_AWAY/UNSCOREABLE]` | `[text]` | `confounder_adjustment_metrics.tsv` |
| metabolic/inflammatory/STAT1 | `[SURVIVES/ATTENUATES/EXPLAINED_AWAY/UNSCOREABLE]` | `[text]` | `confounder_adjustment_metrics.tsv` |
| joint confounder model | `[SURVIVES/ATTENUATES/EXPLAINED_AWAY/UNSCOREABLE]` | `[text]` | `joint_confounder_metrics.tsv` |
| batch diagnostic | `[PASS/WARN/FAIL/UNAVAILABLE]` | `[text]` | `batch_diagnostic_metrics.tsv` |

Confounder-adjusted success cannot convert a failed primary locked score into a
pass. Batch warnings must be reported even if the raw result passes.

## What This Result Establishes

Write in one paragraph:

`[Established: ...]`

## What This Result Does Not Establish

Required reminders:

- no baseline stratifier is established unless separately locked and validated;
- no clinical treatment-switch threshold is established by one cohort;
- no universal MS-DMT claim is established by one DMF/NEDA cohort;
- synthetic harness results are method behavior only.

## Required Next Action

Choose one:

- `[ ] update V22/V23 validation ledger and seek independent replication`
- `[ ] power the next cohort using observed effect size and CI`
- `[ ] request missing/repair data component: [component]`
- `[ ] write kill/demotion update only if V22 kill criteria are met across cohorts`

## Forbidden Additions

Do not add:

- alternative endpoints selected after seeing results;
- sign-flipped scores;
- new module genes;
- post-hoc thresholds;
- unregistered subgroup success claims;
- clinical utility claims beyond the V42 interpretation grid.
