# Wave97 C15 Residual Co-State Falsification

Random seed: `20260527`.

## Question

Do Wave96 parked C15ORF48-proximal candidates remain coupled to C15ORF48
after residualizing donor-level pseudo-bulk expression against disease
status and a generic inflammatory/metabolic covariate mean?

## Verdict

Reopened after residualization: `1`.
Parked residual co-state with modality: `9`.

## Call Counts

| wave97_call | n |
| --- | --- |
| PARK_RESIDUAL_COSTATE_WITH_MODALITY | 9 |
| NO_GO_GENERIC_INFLAMMATION_CONFONDED | 2 |
| NO_GO_RESIDUAL_COSTATE_WEAK | 1 |
| REOPEN_AFTER_RESIDUAL_COSTATE | 1 |

## Candidate Summary

| gene | wave97_call | residual_case_positive_context_count | residual_case_positive_disease_count | residual_all_positive_context_count | median_raw_case_r | median_residual_case_r | gate_ms_anchor | gate_genetics | gate_modality | gate_cell_response_or_transition | ms_delta_log2 | ms_p | wave96_call | wave96_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JAK3 | NO_GO_GENERIC_INFLAMMATION_CONFONDED | 0 | 0 | 2 | 0.5772 | 0.1105 | False | False | True | True | -1.274 | 0.01499 | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | 20.54 |
| IL15 | NO_GO_GENERIC_INFLAMMATION_CONFONDED | 0 | 0 | 1 | 0.5943 | -0.2259 | False | False | True | True | 1.196 | 0.1226 | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | 18.82 |
| IL23A | NO_GO_RESIDUAL_COSTATE_WEAK | 0 | 0 | 0 | 0.1616 | 0.05229 | True | False | True | True | 0.6573 | 0.09161 | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | 21.08 |
| LITAF | PARK_RESIDUAL_COSTATE_WITH_MODALITY | 3 | 3 | 3 | 0.7024 | 0.4155 | False | False | True | True | 0.3084 | 0.1716 | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | 21.93 |
| CASP4 | PARK_RESIDUAL_COSTATE_WITH_MODALITY | 3 | 2 | 2 | 0.5964 | 0.3084 | False | False | True | True | 0.2067 | 0.4927 | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | 21.28 |
| CD200 | PARK_RESIDUAL_COSTATE_WITH_MODALITY | 3 | 2 | 2 | 0.2819 | -0.1339 | True | False | True | False | 1.838 | 0.09086 | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | 19.87 |
| SLPI | PARK_RESIDUAL_COSTATE_WITH_MODALITY | 2 | 2 | 1 | 0.07564 | -0.04826 | False | False | True | False | -2.815 | 0.0173 | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | 18.15 |
| MTHFD2 | PARK_RESIDUAL_COSTATE_WITH_MODALITY | 2 | 2 | 3 | 0.1477 | -0.6116 | False | False | True | False | 0.04616 | 0.8145 | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | 16.67 |
| PDPN | PARK_RESIDUAL_COSTATE_WITH_MODALITY | 2 | 2 | 2 | 0.08486 | -0.4747 | False | False | True | False | 0.1647 | 0.4972 | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | 15.41 |
| FKBP1A | PARK_RESIDUAL_COSTATE_WITH_MODALITY | 2 | 1 | 3 | 0.705 | 0.3913 | False | False | True | True | -0.3349 | 0.2385 | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | 21.41 |
| PIK3R2 | PARK_RESIDUAL_COSTATE_WITH_MODALITY | 1 | 1 | 2 | 0.5107 | 0.3979 | False | False | True | False | -0.03954 | 0.8468 | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | 17.75 |
| PLEK2 | PARK_RESIDUAL_COSTATE_WITH_MODALITY | 3 | 1 | 4 | 0.4266 | 0.3143 | True | False | True | False | 3.046 | 0.007379 | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | 17.68 |
| CCL20 | REOPEN_AFTER_RESIDUAL_COSTATE | 1 | 1 | 2 | 0.7801 | 0.1878 | True | True | True | False | 1.147 | 0.06111 | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | 21.92 |

## Interpretation

This wave is a confounding check, not a causal model. Loss of residual
co-state means the Wave96 signal is likely dominated by generic
inflammatory/metabolic burden. Survival keeps a candidate alive only for
prior-art and mechanism-directionality forcing tests.

## Output Files

- `results_v3/wave97_c15_residual_costate_falsification/residual_costate_context_tests.tsv`
- `results_v3/wave97_c15_residual_costate_falsification/donor_covariate_scores.tsv`
- `results_v3/wave97_c15_residual_costate_falsification/residual_costate_candidate_summary.tsv`
- `results_v3/wave97_c15_residual_costate_falsification/summary.json`
- `results_v3/wave97_c15_residual_costate_falsification/REPORT.md`
