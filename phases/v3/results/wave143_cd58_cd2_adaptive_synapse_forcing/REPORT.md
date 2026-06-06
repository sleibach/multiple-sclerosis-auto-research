# Wave143 CD58/CD2 Adaptive-Synapse Forcing Test

## Bottom Line

Branch call: `NO_CD58_CD2_ADAPTIVE_SYNAPSE_PROMOTION`.

`CD58/CD2` remains an informative adaptive-synapse comparator with MS genetic
anchoring and RA baseline association, but it is not promotable as a V3 target.

## Gate Matrix

| Gate | Passed | Critical |
| --- | --- | --- |
| ms_target_resolved_genetic_anchor | True | True |
| ra_signal_survives_t_cell_adjustment | True | False |
| ra_signal_survives_full_mixture_adjustment | False | True |
| ibd_replication_after_mixture | False | True |
| cross_disease_local_replication_ge3 | False | False |
| response_specificity_ra_and_ibd | False | True |
| direction_resolved_restore_vs_block | False | True |
| non_prior_art_intervention_route | False | True |
| cd2_cd58_not_rejected_by_wave141 | False | False |

## Key Evidence

- RA baseline CD58 association after T-cell/effector-memory adjustment:
  coef `0.8700443058575238`, p
  `0.0087144366152823`.
- RA baseline after full mixture adjustment: coef
  `0.540226391415028`, p
  `0.0845935812729626`.
- IBD full-mixture positive rows with p < 0.10:
  `0`.
- Strict residual surviving disease count:
  `0.0`.
- Alefacept/CD2-CD58 prior art present:
  `True`.

## Interpretation

The decisive failures are IBD/non-RA replication, full-mixture robustness,
response specificity, unresolved restore-versus-block direction, and generic
autoimmune prior art around alefacept/CD2 targeting. The route should remain a
comparator for adaptive-synapse biology rather than a therapeutic finding.
