# Post-Validation Route Update Playbook V52

Date: 2026-07-10

Status: future status-update playbook. This document adds no evidence, changes
no route status today, and does not authorize post-hoc rule changes. It defines
how future monitoring or chr1 package outcomes should update the V52 route map.

## Rule

Route status changes only after the relevant pre-specified gate has produced a
scoreable result. Context, structure, literature, model output, partial
packages, and unscoreable packages do not change route status.

## Monitoring Route Updates

| future result | route status after result | required update | forbidden update |
|---|---|---|---|
| `PASS_CLEAN` in complete external cohort | externally supported monitoring readout in that treatment context | update therapeutic dashboard, findings successor, and validation ledger; keep rule frozen | do not call clinical utility or treatment-switching threshold |
| `PASS_IMMUNE_TONE_BOUNDED` | externally supported immune-tone-aware monitoring readout | update route as bounded monitor; require confounder-rich replication | do not call pure APC/HLA-II-specific mechanism |
| `PASS_NON_SPECIFIC` | dynamic immune-state context; V22-specific biology not validated | demote specificity claim; add specificity-risk note | do not promote locked scalar as intended |
| `INCONCLUSIVE_UNDERPOWERED` | status unchanged, effect-size estimate added | update power/design notes and next-cohort requirements | do not treat favorable point estimate as pass or wide null as fail |
| `FAIL_ADEQUATE_POWER` | demoted or closed for tested DMF/MS context, depending on accumulated validation ledger | update route dashboard and findings successor; no retuning on same data | do not sign-flip, endpoint-swap, or fit a rescue rule |
| `UNSCOREABLE_DATA` | status unchanged; acquisition blocker recorded | update data-request gap and package log | do not treat as biology or negative validation |

## chr1 Route Updates

| future chr1 package outcome | route status after result | required update | forbidden update |
|---|---|---|---|
| Full chain passes: causal gene, cell state, protective direction, perturbation, modality | target-workup-ready handoff | write dedicated target-workup plan and route decision log | do not skip direction/modality because structure looks favorable |
| Causal gene and cell state pass, but perturbation or modality fails | biology-only | record mechanism finding; keep target route closed | do not start therapeutic program |
| Feasible perturbation moves opposite protective direction | wrong-direction closure for that modality | update no-go table and wrong-direction checklist | do not promote because assay effect is strong |
| Package lacks genotype, direction, or cell-state fields | data-incomplete | request missing fields; no route-status change | do not infer direction from prior preference |
| No candidate gene supports the locus after adequate package | closed for target workup under that package | update chr1 result template and route dashboard | do not rescue with favorite gene or structure context |

## Other Route Updates

| route | scoreable future result | allowed update | non-counting result |
|---|---|---|---|
| Postpartum HLA-II/CD64 APC arm | V44 postpartum harness pass in true postpartum MS relapse-window data | biology lead strengthened; still not direct therapeutic target | RA/SLE/healthy pregnancy-only support |
| T/B compartment state | V44 T/B harness pass with composition controls | secondary monitoring context strengthened | compartment signal explained by composition |
| PTGER4 | signal-specific MS-protective direction plus safe EP4 modality | reopened for future grounding only | general GPCR tractability or region-level association |
| ZMIZ1 | MS-specific protective modulation plus perturbation and modality | reopened for future grounding only | opposite-direction cross-disease signal alone |

## Required Files After A Future Update

Any status change must update or create:

1. `docs/reports/THERAPEUTIC_ROUTE_DECISION_LOG_TEMPLATE_V52.md` filled as a
   new decision log artifact.
2. `docs/reports/THERAPEUTIC_ROUTE_STATUS_DASHBOARD_V52.tsv`.
3. `docs/reports/THERAPEUTIC_TARGET_EVIDENCE_MATRIX_V52.tsv`.
4. `meta/CURRENT_STATUS.md`.
5. `meta/NEXT_ACTIONS.md`.
6. The relevant validation or chr1 result-report artifact.

If the result is unscoreable or incomplete, update only the package log, data
request, and next actions. Do not update scientific route status.

## Consistency Checks Before Committing A Future Route Change

| check | required answer |
|---|---|
| Was the relevant package scoreable? | yes, unless recording no-decision |
| Was the locked rule or preregistration unchanged? | yes |
| Was the route gate pre-specified? | yes |
| Are context-only inputs labeled non-counting? | yes |
| Does the status update match the public wording table or chr1 decision class? | yes |
| Are all downstream matrices and status files updated consistently? | yes |

## Source Artifacts

- `docs/reports/THERAPEUTIC_ROUTE_STATUS_DASHBOARD_V52.tsv`
- `docs/reports/THERAPEUTIC_ROUTE_DECISION_LOG_TEMPLATE_V52.md`
- `docs/reports/THERAPEUTIC_TARGET_EVIDENCE_MATRIX_V52.tsv`
- `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- `docs/validation/MONITORING_PUBLIC_WORDING_TABLE_V52.tsv`
- `docs/validation/MONITORING_RESULT_CLASS_EXAMPLES_V52.md`
- `docs/workups/genetics/CHR1_PACKAGE_RESULT_REPORT_TEMPLATE_V52.md`
- `docs/workups/genetics/CHR1_DIRECTION_MATCHED_EXPERIMENT_BLUEPRINT_V52.md`

