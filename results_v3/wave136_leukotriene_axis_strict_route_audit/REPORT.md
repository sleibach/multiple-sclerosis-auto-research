# Wave136 Leukotriene/Oxylipin Strict Route Audit

## Bottom Line

Branch call: `NO_REOPEN_LEUKOTRIENE_AXIS_SMALL_N_ONLY`.

Corrected Wave135 did not find a directionally reproduced MS treatment-response
rescue signal in the leukotriene/oxylipin panel. Earlier small-n sensitivity
language is superseded by the corrected Wave135 run.

## Gate Matrix

| Gate | Passed | Critical |
| --- | --- | --- |
| wave135_stable_small_n_signal | False | False |
| fdr_grade_ms_response | False | True |
| signal_in_both_datasets_for_same_feature | False | False |
| target_resolved_genetics | False | True |
| class_route_previously_reopened | False | True |
| direction_and_safety_clear | False | True |
| prior_art_not_blocking | False | True |
| single_selective_intervention_node_defined | False | True |

## Failed Critical Gates

fdr_grade_ms_response; target_resolved_genetics; class_route_previously_reopened; direction_and_safety_clear; prior_art_not_blocking; single_selective_intervention_node_defined

## Interpretation

The corrected response evidence is not sufficient even as a stable biomarker
clue. The class remains genetically unresolved, directionally ambiguous,
prior-art crowded, and lacks a single selective intervention node tied to the
cross-autoimmune lipid-lysosomal module.
