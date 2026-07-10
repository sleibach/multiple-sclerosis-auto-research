# Monitoring Validation Result Report Template V52

Date: 2026-07-10

Status: future result-report template. This is a blank shell for a future
Gafson/Karolinska-style validation run. It adds no evidence, changes no locked
rule, and must not be filled before the package is quarantined, checked, and run
through the frozen harness.

## Cohort And Receipt

| field | value |
|---|---|
| cohort_id | `[fill after receipt]` |
| package path | `[quarantined local path]` |
| receipt date UTC | `[YYYY-MM-DDTHH:MM:SSZ]` |
| access terms checked | `[yes/no; summary path]` |
| checksum manifest | `[path]` |
| expression matrix | `[path]` |
| sample metadata | `[path]` |
| outcome metadata | `[path]` |
| feature annotation | `[path]` |

## Preflight Eligibility

| gate | result | output path | note |
|---|---|---|---|
| interpreter precheck | `[PASS/FAIL]` | `[path]` | `.venv/bin/python` dependency check |
| checksum manifest | `[PASS/FAIL]` | `[path]` | stop if fail |
| outcome dictionary | `[PASS/FAIL]` | `[path]` | stop if label/window ambiguous |
| intake preflight | `[PASS/FAIL]` | `[path]` | stop if schema/quarantine/sample IDs fail |
| module coverage | `[PASS/FAIL]` | `[path]` | stop if V22 modules unscoreable |
| subject map | `[PASS/FAIL]` | `[path]` | stop if pairing is not mechanical |
| harness synthetic self-test | `[PASS/FAIL]` | `[path]` | stop if null/planted mechanics fail |

If any stop condition fails, classify the report as `UNSCOREABLE_DATA` and do
not proceed to primary scoring.

## Frozen Harness Outputs

| output | path |
|---|---|
| validation_summary.json | `[path]` |
| paired_module_deltas.tsv | `[path]` |
| gene_mapping_coverage.tsv | `[path]` |
| sample_attrition.tsv | `[path]` |
| locked_rule_metrics.tsv | `[path]` |
| confounder_adjustment_metrics.tsv | `[path]` |
| joint_confounder_metrics.tsv | `[path]` |
| batch_diagnostic_metrics.tsv | `[path]` |

## Primary Metrics

| metric | value | confidence interval / uncertainty | note |
|---|---:|---|---|
| n subjects scoreable | `[n]` | `[NA]` | after attrition |
| n responders | `[n]` | `[NA]` | according to pre-specified label |
| n nonresponders | `[n]` | `[NA]` | according to pre-specified label |
| AUC | `[value]` | `[CI]` | locked score only |
| signed Hedges g | `[value]` | `[CI]` | locked orientation |
| primary p/null result | `[value]` | `[method]` | pre-specified method only |
| receptor/control comparison | `[value]` | `[NA]` | if applicable under V42 |

## Confounder And Batch Results

| panel | result class | effect on locked score | note |
|---|---|---|---|
| baseline APC/HLA-II state | `[SURVIVES/ATTENUATES/EXPLAINED_AWAY/NA]` | `[value]` | |
| glucocorticoid/steroid | `[SURVIVES/ATTENUATES/EXPLAINED_AWAY/NA]` | `[value]` | |
| cell composition | `[SURVIVES/ATTENUATES/EXPLAINED_AWAY/NA]` | `[value]` | |
| metabolic/inflammatory/STAT1 | `[SURVIVES/ATTENUATES/EXPLAINED_AWAY/NA]` | `[value]` | |
| proliferation | `[SURVIVES/ATTENUATES/EXPLAINED_AWAY/NA]` | `[value]` | |
| batch diagnostic | `[CLEAN/BOUNDED/INVALIDATING/NA]` | `[value]` | |

## Final Result Class

Select exactly one:

- `[ ] PASS_CLEAN`
- `[ ] PASS_IMMUNE_TONE_BOUNDED`
- `[ ] PASS_NON_SPECIFIC`
- `[ ] INCONCLUSIVE_UNDERPOWERED`
- `[ ] FAIL_ADEQUATE_POWER`
- `[ ] UNSCOREABLE_DATA`

Required sentence:

`[paste exactly one approved V42/V52 result sentence]`

## Interpretation

| question | answer |
|---|---|
| Does this externally support the locked monitoring scalar? | `[yes/bounded/no/inconclusive/unscoreable]` |
| Does this establish clinical utility? | `No, unless a separate prospective utility study has already supplied that evidence.` |
| Does this create or reopen a therapeutic target? | `No.` |
| Does this change the locked rule? | `No.` |
| Does this require a route-status update? | `[yes/no; path to update]` |

## Required Next Action

| result class | next action |
|---|---|
| `PASS_CLEAN` | seek independent replication and prospective utility study |
| `PASS_IMMUNE_TONE_BOUNDED` | replicate with confounder-rich cohort and report bounded monitor |
| `PASS_NON_SPECIFIC` | downgrade specificity; do not promote V22 biology |
| `INCONCLUSIVE_UNDERPOWERED` | use effect size and CI for next powered cohort |
| `FAIL_ADEQUATE_POWER` | update validation ledger; do not tune rescue rule on same data |
| `UNSCOREABLE_DATA` | request missing fields or replacement cohort |

## Non-Commands

Do not append exploratory plots, tuned thresholds, alternate endpoints, timepoint
searches, feature replacements, or target-development analyses to this report.
Those belong in separate pre-specified artifacts, if allowed at all.

## Source Artifacts

- `docs/validation/PREREGISTRATION_V42.md`
- `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- `docs/validation/MONITORING_VALIDATION_COMMAND_MANIFEST_V52.md`
- `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md`
- `docs/validation/THERAPEUTIC_VALIDATION_HANDOFF_V52.md`
- `docs/validation/MONITORING_CLINICAL_UTILITY_BOUNDARY_CHECKLIST_V52.md`
