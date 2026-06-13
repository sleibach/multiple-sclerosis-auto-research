# Repair Request: below_planning_floor_labeled_pairs

Status: draft request template. No validation result and no biological claim.

Subject: More labeled paired subjects needed for interpretable validation

Dear <collaborator_or_data_provider>,

Thank you for the returned package for `<cohort_id>`. Our pre-registered intake
checks cannot proceed to interpretation in its current form.

Blocked state:

- V46 safe class: `BELOW_V45_PLANNING_FLOOR`
- failure code: `UNDERPOWERED_GROUP_SIZE`
- trigger: labeled group sizes below V42 clean-pass threshold
- allowed repair: report inconclusive/effect estimate per grid

Requested repair:

- The available labeled paired subjects are below the V45 planning floor for validation interpretation.
- Please provide additional eligible baseline/early-treatment paired subjects with mapped labels, or confirm that no larger labeled subset is available.

Please return:

- additional paired labeled subjects if available
- attrition counts by exclusion reason
- confirmation if this is the complete eligible cohort

Please do not send:

- dropping subjects based on scores
- favorable subset selection
- changed early-treatment window

This request does not ask for any new analysis, changed rule, changed endpoint,
changed threshold, or interpretation. Once the repaired package is received, we
will rerun the same frozen intake and returned-package gates before any result
wording is drafted.
