# Wave80 CD58/CD2 Immune-Synapse Closure

## Question

Can the `CD58` partial survivor from Wave79 be reframed as a coherent
cross-autoimmune immune-synapse intervention or stratification axis, or is it
explained by mixture/immune-synapse biology plus prior-art blockade?

## Verdict

`PARK_CD58_RA_ONLY_PRIOR_ART_BLOCKED`

## Decision

Park CD58 as an RA-only response-state comparator: RA retains some signal after mixture/synapse adjustment, but IBD replication is absent and the intervention route is prior-art blocked.

## Attenuation Summary

| dataset | endpoint | raw_model | adjusted_model | raw_coef | adjusted_coef | abs_coef_ratio | attenuation_fraction | raw_p | adjusted_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE198520_RA_synovium_antiTNF | baseline | M0_clinical | M2_full_mixture | 0.9104 | 0.5402 | 0.5934 | 0.4066 | 0.002978 | 0.08459 |
| GSE198520_RA_synovium_antiTNF | delta | M0_clinical | M2_full_mixture | 0.7433 | 0.5708 | 0.768 | 0.232 | 0.08006 | 0.06242 |
| GSE282122_IBD_myeloid_antiTNF | baseline | M0_clinical | M2_full_mixture | -0.2099 | -0.08317 | 0.3962 | 0.6038 | 0.4212 | 0.7903 |
| GSE282122_IBD_myeloid_antiTNF | delta | M0_clinical | M2_full_mixture | -0.2055 | -0.3187 | 1.551 | -0.5508 | 0.3521 | 0.3796 |

## RA Models

| dataset | cell_state | endpoint | model | n | coef | p | r2 | status | formula |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline | M0_clinical | 42 | 0.9104 | 0.002978 | 0.5525 | ok | cd58_pre ~ good_response + generic_nfkb_score_pre + C(pathotype) + C(biologic) + inflammatory_score + das28_score |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline | M1_t_synapse | 42 | 0.826 | 0.0115 | 0.5597 | ok | cd58_pre ~ good_response + generic_nfkb_score_pre + t_synapse_score_pre + C(pathotype) + C(biologic) + inflammatory_score + das28_score |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | baseline | M2_full_mixture | 42 | 0.5402 | 0.08459 | 0.6704 | ok | cd58_pre ~ good_response + generic_nfkb_score_pre + t_synapse_score_pre + apc_hla_score_pre + myeloid_score_pre + b_cell_score_pre + stromal_injury_score_pre + C(pathotype) + C(biologic) + inflammatory_score + das28_score |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta | M0_clinical | 42 | 0.7433 | 0.08006 | 0.5794 | ok | cd58_delta ~ good_response + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + C(pathotype) + C(biologic) + inflammatory_score + das28_score |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta | M1_t_synapse | 42 | 0.5791 | 0.1636 | 0.6462 | ok | cd58_delta ~ good_response + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + t_synapse_score_pre + t_synapse_score_delta + C(pathotype) + C(biologic) + inflammatory_score + das28_score |
| GSE198520_RA_synovium_antiTNF | bulk_synovium | delta | M2_full_mixture | 42 | 0.5708 | 0.06242 | 0.8663 | ok | cd58_delta ~ good_response + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + t_synapse_score_pre + t_synapse_score_delta + apc_hla_score_pre + apc_hla_score_delta + myeloid_score_pre + myeloid_score_delta + b_cell_score_pre + b_cell_score_delta + stromal_injury_score_pre + C(pathotype) + C(biologic) + inflammatory_score + das28_score |

## IBD Models

| dataset | cell_state | endpoint | model | n | coef | p | r2 | status | formula |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline | M0_clinical | 29 | -0.2099 | 0.4212 | 0.2441 | ok | cd58_pre ~ remission + generic_nfkb_score_pre + C(Disease) + baseline_inflammation_score |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline | M1_t_synapse | 29 | -0.1898 | 0.4762 | 0.256 | ok | cd58_pre ~ remission + generic_nfkb_score_pre + t_synapse_score_pre + C(Disease) + baseline_inflammation_score |
| GSE282122_IBD_myeloid_antiTNF | DC | baseline | M2_full_mixture | 29 | -0.08317 | 0.7903 | 0.3343 | ok | cd58_pre ~ remission + generic_nfkb_score_pre + t_synapse_score_pre + apc_hla_score_pre + myeloid_score_pre + b_cell_score_pre + stromal_injury_score_pre + C(Disease) + baseline_inflammation_score |
| GSE282122_IBD_myeloid_antiTNF | DC | delta | M0_clinical | 29 | -0.2055 | 0.3521 | 0.5958 | ok | cd58_delta ~ remission + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + C(Disease) + baseline_inflammation_score |
| GSE282122_IBD_myeloid_antiTNF | DC | delta | M1_t_synapse | 29 | -0.2871 | 0.2488 | 0.6111 | ok | cd58_delta ~ remission + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + t_synapse_score_pre + t_synapse_score_delta + C(Disease) + baseline_inflammation_score |
| GSE282122_IBD_myeloid_antiTNF | DC | delta | M2_full_mixture | 29 | -0.3187 | 0.3796 | 0.6702 | ok | cd58_delta ~ remission + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + t_synapse_score_pre + t_synapse_score_delta + apc_hla_score_pre + apc_hla_score_delta + myeloid_score_pre + myeloid_score_delta + b_cell_score_pre + b_cell_score_delta + stromal_injury_score_pre + C(Disease) + baseline_inflammation_score |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | baseline | M0_clinical | 29 | 0.1818 | 0.1732 | 0.6888 | ok | cd58_pre ~ remission + generic_nfkb_score_pre + C(Disease) + baseline_inflammation_score |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | baseline | M1_t_synapse | 29 | 0.1992 | 0.1343 | 0.7103 | ok | cd58_pre ~ remission + generic_nfkb_score_pre + t_synapse_score_pre + C(Disease) + baseline_inflammation_score |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | baseline | M2_full_mixture | 29 | 0.0398 | 0.8261 | 0.7888 | ok | cd58_pre ~ remission + generic_nfkb_score_pre + t_synapse_score_pre + apc_hla_score_pre + myeloid_score_pre + b_cell_score_pre + stromal_injury_score_pre + C(Disease) + baseline_inflammation_score |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta | M0_clinical | 29 | 0.2535 | 0.3284 | 0.5266 | ok | cd58_delta ~ remission + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + C(Disease) + baseline_inflammation_score |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta | M1_t_synapse | 29 | 0.2519 | 0.3596 | 0.5352 | ok | cd58_delta ~ remission + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + t_synapse_score_pre + t_synapse_score_delta + C(Disease) + baseline_inflammation_score |
| GSE282122_IBD_myeloid_antiTNF | Mono_macro | delta | M2_full_mixture | 29 | 0.1302 | 0.8043 | 0.6119 | ok | cd58_delta ~ remission + cd58_pre + generic_nfkb_score_pre + generic_nfkb_score_delta + t_synapse_score_pre + t_synapse_score_delta + apc_hla_score_pre + apc_hla_score_delta + myeloid_score_pre + myeloid_score_delta + b_cell_score_pre + b_cell_score_delta + stromal_injury_score_pre + C(Disease) + baseline_inflammation_score |

## CD58 Correlations With Mixture/Synapse Scores

| dataset | timepoint | covariate | n | spearman_rho | p | Treatment | cell_state |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GSE198520_RA_synovium_antiTNF | pre | myeloid_score | 46 | 0.6571 | 7.041e-07 |  |  |
| GSE198520_RA_synovium_antiTNF | pre | stromal_injury_score | 46 | 0.6541 | 8.212e-07 |  |  |
| GSE198520_RA_synovium_antiTNF | pre | apc_hla_score | 46 | 0.5034 | 0.0003621 |  |  |
| GSE198520_RA_synovium_antiTNF | post | stromal_injury_score | 46 | 0.4795 | 0.0007471 |  |  |
| GSE198520_RA_synovium_antiTNF | post | t_synapse_score | 46 | -0.4455 | 0.001921 |  |  |
| GSE198520_RA_synovium_antiTNF | post | apc_hla_score | 46 | 0.36 | 0.014 |  |  |
| GSE198520_RA_synovium_antiTNF | post | myeloid_score | 46 | 0.3444 | 0.01908 |  |  |
| GSE198520_RA_synovium_antiTNF | pre | generic_nfkb_score | 46 | 0.2657 | 0.07426 |  |  |
| GSE198520_RA_synovium_antiTNF | post | b_cell_score | 46 | -0.254 | 0.08847 |  |  |
| GSE198520_RA_synovium_antiTNF | pre | t_synapse_score | 46 | -0.1863 | 0.2151 |  |  |
| GSE198520_RA_synovium_antiTNF | pre | b_cell_score | 46 | 0.1743 | 0.2465 |  |  |
| GSE198520_RA_synovium_antiTNF | post | generic_nfkb_score | 46 | -0.09516 | 0.5293 |  |  |
| GSE282122_IBD_myeloid_antiTNF |  | t_synapse_score | 55 | 0.3411 | 0.01083 | Post | DC |
| GSE282122_IBD_myeloid_antiTNF |  | stromal_injury_score | 55 | 0.2732 | 0.04361 | Post | DC |
| GSE282122_IBD_myeloid_antiTNF |  | stromal_injury_score | 55 | 0.2716 | 0.04484 | Pre | DC |
| GSE282122_IBD_myeloid_antiTNF |  | apc_hla_score | 55 | -0.2589 | 0.05626 | Post | DC |
| GSE282122_IBD_myeloid_antiTNF |  | b_cell_score | 55 | -0.2306 | 0.09031 | Pre | DC |
| GSE282122_IBD_myeloid_antiTNF |  | generic_nfkb_score | 55 | -0.09481 | 0.4911 | Post | DC |
| GSE282122_IBD_myeloid_antiTNF |  | t_synapse_score | 55 | 0.08716 | 0.5269 | Pre | DC |
| GSE282122_IBD_myeloid_antiTNF |  | myeloid_score | 55 | -0.07338 | 0.5945 | Pre | DC |
| GSE282122_IBD_myeloid_antiTNF |  | myeloid_score | 55 | -0.0443 | 0.7481 | Post | DC |
| GSE282122_IBD_myeloid_antiTNF |  | apc_hla_score | 55 | 0.0158 | 0.9088 | Pre | DC |
| GSE282122_IBD_myeloid_antiTNF |  | generic_nfkb_score | 55 | 0.007576 | 0.9562 | Pre | DC |
| GSE282122_IBD_myeloid_antiTNF |  | b_cell_score | 55 | -0.001227 | 0.9929 | Post | DC |
| GSE282122_IBD_myeloid_antiTNF |  | stromal_injury_score | 55 | 0.4561 | 0.0004665 | Pre | Mono_macro |
| GSE282122_IBD_myeloid_antiTNF |  | generic_nfkb_score | 55 | 0.3692 | 0.00554 | Pre | Mono_macro |
| GSE282122_IBD_myeloid_antiTNF |  | myeloid_score | 55 | -0.3441 | 0.01009 | Post | Mono_macro |
| GSE282122_IBD_myeloid_antiTNF |  | b_cell_score | 55 | -0.34 | 0.01108 | Pre | Mono_macro |
| GSE282122_IBD_myeloid_antiTNF |  | generic_nfkb_score | 55 | 0.3231 | 0.01613 | Post | Mono_macro |
| GSE282122_IBD_myeloid_antiTNF |  | apc_hla_score | 55 | -0.2625 | 0.05287 | Pre | Mono_macro |
| GSE282122_IBD_myeloid_antiTNF |  | stromal_injury_score | 55 | 0.2435 | 0.07317 | Post | Mono_macro |
| GSE282122_IBD_myeloid_antiTNF |  | t_synapse_score | 55 | -0.1459 | 0.2879 | Pre | Mono_macro |
| GSE282122_IBD_myeloid_antiTNF |  | apc_hla_score | 55 | -0.08492 | 0.5376 | Post | Mono_macro |
| GSE282122_IBD_myeloid_antiTNF |  | myeloid_score | 55 | 0.04747 | 0.7307 | Pre | Mono_macro |
| GSE282122_IBD_myeloid_antiTNF |  | b_cell_score | 55 | -0.01194 | 0.931 | Post | Mono_macro |
| GSE282122_IBD_myeloid_antiTNF |  | t_synapse_score | 55 | -0.009596 | 0.9446 | Post | Mono_macro |

## Interpretation

- RA uses bulk synovium, so `CD58` can reflect cell mixture, immune-synapse
  density, stromal/injury signal, or a true response-relevant state.
- IBD uses myeloid/DC pseudobulk, so T-cell markers are interpreted as ambient
  contamination, doublets, or sample-level lymphocyte proximity rather than
  true myeloid expression.
- A promotable target claim would require RA and IBD response coherence after
  these covariates, plus a non-prior-art intervention direction. That is not
  expected from Wave79 sidecar constraints.

## Output Files

- `results_v3/wave80_cd58_synapse_closure/ra_cd58_synapse_models.tsv`
- `results_v3/wave80_cd58_synapse_closure/ibd_cd58_synapse_models.tsv`
- `results_v3/wave80_cd58_synapse_closure/cd58_synapse_attenuation.tsv`
- `results_v3/wave80_cd58_synapse_closure/cd58_synapse_correlations.tsv`
- `results_v3/wave80_cd58_synapse_closure/ra_cd58_synapse_pairs.tsv`
- `results_v3/wave80_cd58_synapse_closure/ibd_cd58_synapse_pairs.tsv`
- `results_v3/wave80_cd58_synapse_closure/summary.json`
