# Therapeutic Route Decision Log Template V52

Date: 2026-07-10

Status: future decision-log template. This blank template adds no evidence,
changes no verdict, and does not authorize a route-status change. It defines the
minimum fields required before any future V52 route can be promoted, demoted,
closed, or reopened.

## Decision Metadata

| field | value |
|---|---|
| decision_id | `[stable ID]` |
| decision date UTC | `[YYYY-MM-DDTHH:MM:SSZ]` |
| route or lead | `[monitoring scalar / chr1 / GPR25 / KIF21B / PTGER4 / etc.]` |
| previous status | `[status before decision]` |
| proposed new status | `[status after decision]` |
| operator / reviewer | `[name or process]` |
| package or artifact triggering review | `[path or citation]` |

## Evidence Basis

| evidence item | class | path / source | required gate passed | role in decision |
|---|---|---|---|---|
| primary grounded result | `[project result / validation result / target package result]` | `[path]` | `[yes/no/NA]` | `[primary evidence]` |
| confounder / batch / specificity gate | `[diagnostic]` | `[path]` | `[yes/no/NA]` | `[supports/bounds/demotes]` |
| structure context | `[context only / NA]` | `[path]` | `[yes/no/NA]` | `[context only; not sufficient]` |
| external context | `[context only / NA]` | `[path]` | `[yes/no/NA]` | `[corroboration/tension flag only]` |
| non-counting evidence | `[literature / model / structure / incomplete package / other]` | `[path]` | `[NA]` | `[state why it does not count]` |

## Required Route Gate

| route type | required gate | met? | note |
|---|---|---|---|
| monitoring validation | frozen V42/V44 class plus V52 decision tree | `[yes/no/NA]` | |
| monitoring clinical utility | prospective decision-impact evidence | `[yes/no/NA]` | |
| chr1 target workup | causal gene, cell state, protective direction, perturbation, modality | `[yes/no/NA]` | |
| GPR25 target workup | protective GPR25 restoration/agonism chain | `[yes/no/NA]` | |
| KIF21B target workup | protective KIF21B restoration/up-function chain | `[yes/no/NA]` | |
| PTGER4 reopen | signal-specific MS-protective direction and safe EP4 modality | `[yes/no/NA]` | |
| closed/negative route | adequate pre-specified fail or missing required chain | `[yes/no/NA]` | |

## Decision Class

Select exactly one:

- `[ ] status unchanged`
- `[ ] promoted within current claim level`
- `[ ] promoted to externally supported monitoring`
- `[ ] promoted to clinical-utility workup`
- `[ ] promoted to target-workup ready`
- `[ ] demoted`
- `[ ] closed`
- `[ ] reopened for future grounding only`
- `[ ] unscoreable / no decision`

## Required Justification

Write one paragraph:

`[State the new decision, the evidence that counts, the evidence that does not
count, the exact gate met or failed, and the next action. Do not cite structure,
external context, model output, or an incomplete package as sufficient primary
evidence.]`

## Consistency Checks

Before committing a status change, verify:

| check | pass? |
|---|---|
| no locked rule or pre-registration changed | `[yes/no]` |
| no broad public-data discovery reopened | `[yes/no]` |
| relevant provenance/structure gates pass | `[yes/no]` |
| size/tmp push guard passes | `[yes/no]` |
| result is reflected in the appropriate V52 matrix/index/status artifact | `[yes/no/NA]` |
| non-counting evidence is explicitly labeled non-counting | `[yes/no]` |

## Source Artifacts

- `docs/reports/THERAPEUTIC_PATH_V52.md`
- `docs/reports/THERAPEUTIC_CLAIM_HIERARCHY_V52.md`
- `docs/reports/THERAPEUTIC_ROUTE_ASSUMPTION_LEDGER_V52.md`
- `docs/reports/THERAPEUTIC_ROUTE_RISK_REGISTER_V52.md`
- `docs/reports/THERAPEUTIC_REOPEN_CHECKLIST_V52.tsv`
- `docs/validation/MONITORING_VALIDATION_RESULT_REPORT_TEMPLATE_V52.md`
- `docs/workups/genetics/CHR1_PACKAGE_RESULT_REPORT_TEMPLATE_V52.md`
