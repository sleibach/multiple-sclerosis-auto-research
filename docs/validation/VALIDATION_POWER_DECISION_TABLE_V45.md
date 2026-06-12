# Validation Power Decision Table V45

Status: stakeholder-facing synthesis from V43 synthetic method-characterization.
Synthetic results are not biological evidence.

## Purpose

Translate the V43 power map and V45 cohort specification into a compact table for
data-acquisition decisions. The question is practical:

> Which cohort sizes are likely to settle the locked V22/V42 validation question,
> and which are useful mainly as effect-size / confidence-interval information?

Machine-readable outputs:

- `analysis/v45_power_decision_table/stakeholder_power_decision_table.tsv`
- `analysis/v45_power_decision_table/selected_scenarios_by_n.tsv`
- `analysis/v45_power_decision_table/summary.json`

Dropout/missing-timepoint sensitivity:

- `docs/validation/DROPOUT_MISSING_TIMEPOINT_SENSITIVITY_V45.md`
- `analysis/v45_dropout_sensitivity_table/dropout_enrollment_targets.tsv`
- `analysis/v45_dropout_sensitivity_table/nominal_attrition_power_impact.tsv`

Generator:

- `scripts/v45_power_decision_table.py`

## Headline

Gafson-sized cohorts are worth running if obtained, but they should not be
treated as guaranteed arbitration. In the V43 synthetic power grid:

- `10-15` per group had mean conclusive rate `0.578` and mean pass rate `0.352`
  across the grid;
- `30+30` reached a decision-grade pass probability only in the large-clean-effect
  scenario;
- moderate effects, especially with immune-tone structure or label noise, did
  not reach `80%` pass probability up to `80` per group in the selected planning
  scenarios.

## Stakeholder Decision Table

| Decision question | Machine result | Action |
|---|---|---|
| Synthetic null false-positive rate? | `0.016` average false-positive rate | Never interpret raw pass without batch/confounder diagnostics. |
| Can Gafson-sized data settle the rule? | `10-15/group` mean conclusive rate `0.578`, mean pass rate `0.352` | Run Gafson if obtained, but pursue Karolinska labels and larger cohorts in parallel. |
| Moderate effect, clean labels, no confounder? | `80%` pass probability not reached up to `80/group` | Do not expect this to settle without larger n or stronger/cleaner effect. |
| Large effect, clean labels, no confounder? | first reaches `>=80%` pass at `30/group` (`pass_rate 0.917`) | `30+30` is the minimum decision-grade planning cell only under clean large-effect assumptions. |
| Moderate effect, 10% label noise, immune-tone structure? | `80%` pass probability not reached up to `80/group` | Need cleaner labels/confounder control, larger cohort, or accept directional inference. |
| Large effect, 10% label noise, immune-tone structure? | `80%` pass probability not reached up to `80/group` | Immune-tone/label noise can prevent a decisive result despite large synthetic effect. |
| What should the medical team seek? | minimum `30+30` only for large clean effects; preferred `60-80/group`; noisy/moderate cases may require `>80/group` or better metadata | Ask for Gafson, Karolinska labels, and any prospective/collaborator cohort with paired early samples, batch balance, steroid metadata, and cell-composition covariates. |

## Caveat

The selected scenario rows average small V43 parameter cells (`24` synthetic
cohorts per n/scenario in the table), so exact pass rates are planning bands, not
precision estimates. The robust conclusion is directional:

- small cohorts are often informative but inconclusive;
- sample size alone is insufficient if labels are noisy or immune-tone/batch
  structure is uncontrolled;
- data quality and covariates are as important as n.

## Bottom Line For Acquisition

1. **Run Gafson if obtained**, because it is the best biological fit, but frame
   it as potentially inconclusive.
2. **Pursue Karolinska labels in parallel**, because Gafson should not be a
   single point of failure.
3. **For a shaped collaborator/prospective cohort**, request at least `60-80`
   responders and `60-80` nonresponders where possible, with the V45 CRF fields
   mandatory.
4. **Account for missing paired samples up front**: to retain `60-80` analyzable
   paired subjects per group, enrollment must be about `75-100/group` at `20%`
   missing/dropout and `100-134/group` at `40%` missing/dropout.
5. **If only `10-15/group` is available**, treat the output as effect-size and CI
   information unless the result is very large and diagnostically clean.
