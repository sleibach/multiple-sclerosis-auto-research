# Monitoring Minimum Viable Package Checklist V52

Date: 2026-07-10

Status: operational checklist. This document adds no evidence and does not
change the frozen V22 rule, V42 pre-registration, or V44 batch guard. It defines
the minimum package needed before a paired PBMC treatment-response validation can
be run.

## Minimum Viable Package

| field group | required for scoreable package | acceptable form | missing-field action |
|---|---|---|---|
| subject identifiers | yes | stable subject ID shared across expression, sample metadata, and outcomes | reject as unscoreable until pairing can be reconstructed |
| baseline sample | yes | pre-treatment PBMC expression sample | reject as unscoreable for frozen delta rule |
| early on-treatment sample | yes | earliest eligible on-treatment PBMC expression sample with timing metadata | reject as unscoreable if no eligible treatment sample exists |
| response label | yes | subject-level NEDA-4 or pre-specified equivalent binary response label | reject as response validation; route to pharmacodynamic context if treatment timing is present |
| outcome window | yes | documented response follow-up window | partial only if label is pre-specified and window ambiguity is recorded |
| feature annotation | yes | gene symbols, Ensembl IDs, or probe-to-gene mapping | reject if V22 module genes cannot be mapped |
| expression values | yes | raw counts or documented normalized expression matrix | reject if no scoreable expression matrix exists |
| module gene coverage | yes | coverage sufficient for frozen module scoring | reject if coverage fails the command manifest |
| batch/QC metadata | yes for full-trust run | batch, lane, processing date, RIN or equivalent, depth, mapping, QC flags | reduced-trust or reject depending on batch guard outcome |

## Strongly Preferred Metadata

These fields are not allowed to tune the rule, but they determine whether the
result is clean, immune-tone-bounded, confounded, or reduced-trust.

| metadata | why it matters | missing-field interpretation |
|---|---|---|
| steroid exposure | glucocorticoid signatures were a priority confounder in V32 | report confounder panel as limited |
| relapse timing | separates treatment response from acute disease activity | report clinical-context limitation |
| infection status | prevents generic immune activation from masquerading as signal | report immune-tone limitation |
| DMT timing | confirms treatment window and avoids mixed-treatment interpretation | route to context-only if timing cannot be reconstructed |
| blood counts or cell fractions | supports composition and batch guard interpretation | composition adjustment limited |
| sample processing details | supports batch-correlated response checks | reduce trust if batch cannot be audited |

## Package Size Expectation

Small packages can estimate effect size but may not settle the rule. The V43
power work keeps the practical ask at roughly `30` responders and `30`
nonresponders when the goal is a conclusive validation rather than a descriptive
estimate.

## Pass To Analysis Only If

1. terms and checksum preflight pass;
2. route classifier returns `monitoring_validation`;
3. required minimum fields are present;
4. module gene coverage is scoreable;
5. batch/QC metadata are sufficient to run or explicitly limit the batch guard;
6. the result-report shell is selected before outputs are known.

## Source Artifacts

- `docs/validation/PREREGISTRATION_V42.md`
- `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md`
- `docs/validation/MONITORING_VALIDATION_COMMAND_MANIFEST_V52.md`
- `docs/validation/VALIDATION_PACKAGE_FIELD_DICTIONARY_V52.tsv`
- `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv`
- `docs/validation/INCOMING_PACKAGE_PREFLIGHT_CHECKLIST_V52.md`
- `docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md`
- `docs/validation/POWER_MAP_V43.md`
