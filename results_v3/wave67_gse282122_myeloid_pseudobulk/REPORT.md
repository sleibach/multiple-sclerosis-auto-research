# Wave67 GSE282122 Myeloid Pseudobulk Audit

Random seed: `20260527`.

## Data

- Accession context: `GSE282122`; processed myeloid object from Zenodo record `14007626`.
- Myeloid h5ad: `data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad`.
- Paired manifest: `data/raw_v3/wave67_gse282122_myeloid/paired_sample_list.csv`.
- Cells in paired myeloid analysis strata: `34703`.
- Paired manifest samples: `110`.
- Pseudobulk strata: `754`.
- Site/state/module deltas: `4059`.

## Gate Summary

| cell state | module | n pairs | n patients | all delta | all FDR | target/generic | adjusted response FDR | call | failed gates |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Mono_macro | complement_phagocytosis | 43 | 29 | 0.0815 | 0.9399 | 0.449 | 1 | NO_GO_GSE282122_MYELOID | no_all_pair_fdr10_pharmacodynamic_delta;target_to_generic_delta_ratio_lt_2;no_remission_interaction_after_generic_adjustment;cd_uc_effect_direction_not_stable |
| DC | lipid_loader_repair | 43 | 29 | 0.008596 | 1 | 0.1006 | 0.9761 | NO_GO_GSE282122_MYELOID | no_all_pair_fdr10_pharmacodynamic_delta;target_to_generic_delta_ratio_lt_2;no_remission_interaction_after_generic_adjustment;cd_uc_effect_direction_not_stable |
| Mono_macro | lipid_loader_repair | 43 | 29 | -0.007466 | 1 | 0.04113 | 1 | NO_GO_GSE282122_MYELOID | no_all_pair_fdr10_pharmacodynamic_delta;target_to_generic_delta_ratio_lt_2;no_remission_interaction_after_generic_adjustment;cd_uc_effect_direction_not_stable |
| DC | lysosomal_apc | 43 | 29 | 0.144 | 0.7084 | 1.686 | 1 | PARK_CELL_RESOLVED_PD_SIGNAL_ONLY | no_all_pair_fdr10_pharmacodynamic_delta;target_to_generic_delta_ratio_lt_2;no_remission_interaction_after_generic_adjustment |
| Mono_macro | lysosomal_apc | 43 | 29 | 0.1223 | 0.8357 | 0.6738 | 1 | PARK_CELL_RESOLVED_PD_SIGNAL_ONLY | no_all_pair_fdr10_pharmacodynamic_delta;target_to_generic_delta_ratio_lt_2;no_remission_interaction_after_generic_adjustment |
| DC | complement_phagocytosis | 43 | 29 | 0.05869 | 1 | 0.687 | 1 | PARK_CELL_RESOLVED_PD_SIGNAL_ONLY | no_all_pair_fdr10_pharmacodynamic_delta;target_to_generic_delta_ratio_lt_2;no_remission_interaction_after_generic_adjustment |

## Top Paired Pharmacodynamic Tests

| scope | state | module | n pairs | n patients | mean delta | p | FDR |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| disease_CD | DC | hla_ii_apc | 22 | 15 | 0.3382 | 0.0003334 | 0.1027 |
| outcome_Remission | DC | hla_ii_apc | 19 | 13 | 0.4803 | 0.0002011 | 0.1027 |
| CD_Remission | DC | hla_ii_apc | 15 | 10 | 0.3774 | 0.0007133 | 0.1465 |
| outcome_Remission | DC | mif_cd74_receptor_state | 19 | 13 | 0.3541 | 0.001945 | 0.1997 |
| outcome_Remission | Mono_macro | hla_ii_apc | 18 | 13 | 0.6396 | 0.001741 | 0.1997 |
| outcome_Remission | Mono_macro | mif_cd74_receptor_state | 18 | 13 | 0.5447 | 0.001795 | 0.1997 |
| disease_CD | DC | mif_cd74_receptor_state | 22 | 15 | 0.2741 | 0.002462 | 0.2167 |
| outcome_Remission | CD1Chi DC | hla_ii_apc | 14 | 10 | 0.4347 | 0.003236 | 0.2492 |
| UC_Non_Remission | CD1Chi DC | mixscale_validated_ifng_readout | 8 | 6 | 0.469 | 0.0043 | 0.2761 |
| UC_Non_Remission | Mono_macro | mixscale_validated_ifng_readout | 19 | 11 | 0.3465 | 0.004482 | 0.2761 |
| disease_CD | CD1Chi DC | hla_ii_apc | 19 | 14 | 0.3127 | 0.005349 | 0.2995 |
| CD_Remission | CD1Chi DC | hla_ii_apc | 13 | 9 | 0.4033 | 0.007608 | 0.3905 |
| UC_Non_Remission | C1Qhi IL1Blo macro | hif_nampt_metabolic | 9 | 8 | 0.3983 | 0.009918 | 0.4364 |
| disease_UC | C1Qhi IL1Blo macro | hif_nampt_metabolic | 9 | 8 | 0.3983 | 0.009918 | 0.4364 |
| CD_Remission | DC | mif_cd74_receptor_state | 15 | 10 | 0.2254 | 0.01103 | 0.4442 |
| CD_Remission | Mono_macro | hla_ii_apc | 14 | 10 | 0.4446 | 0.01209 | 0.4442 |
| UC_Non_Remission | CD1Chi DC | ifn_apc | 8 | 6 | 0.3985 | 0.01576 | 0.4442 |
| UC_Non_Remission | DC | mixscale_validated_ifng_readout | 17 | 11 | 0.3787 | 0.01515 | 0.4442 |
| all | DC | hla_ii_apc | 43 | 29 | 0.2285 | 0.01587 | 0.4442 |
| disease_CD | CD1Chi DC | mif_cd74_receptor_state | 19 | 14 | 0.2804 | 0.01337 | 0.4442 |
| disease_UC | CD1Chi DC | ifn_apc | 9 | 7 | 0.3613 | 0.01493 | 0.4442 |
| outcome_Remission | CD1Chi DC | mif_cd74_receptor_state | 14 | 10 | 0.3346 | 0.01513 | 0.4442 |
| CD_Remission | Mono_macro | mif_cd74_receptor_state | 14 | 10 | 0.33 | 0.01726 | 0.4621 |
| outcome_Non_Remission | DC | lysosomal_apc | 24 | 16 | 0.2189 | 0.02093 | 0.5371 |
| UC_Remission | Mono_macro | mif_cd74_receptor_state | 4 | 3 | 1.296 | 0.02285 | 0.5414 |
| outcome_Non_Remission | C1Qhi IL1Blo macro | hif_nampt_metabolic | 13 | 12 | 0.34 | 0.02252 | 0.5414 |
| outcome_Non_Remission | DC | lipid_loader_repair | 24 | 16 | 0.227 | 0.02402 | 0.5434 |
| outcome_Remission | DC | lipid_loader_repair | 19 | 13 | -0.2672 | 0.0247 | 0.5434 |
| CD_Non_Remission | Mono_macro | ifn_apc | 6 | 5 | -0.4141 | 0.03012 | 0.5887 |
| CD_Remission | CD1Chi DC | mif_cd74_receptor_state | 13 | 9 | 0.2833 | 0.03195 | 0.5887 |

## Top Remission-Interaction Tests

| state | module | n | remission delta | nonremission delta | adjusted delta | adjusted FDR | formula |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| C1Qhi IL1Blo macro | inflammatory_nfkb | 17 | -0.3205 | 0.4187 | -0.5384 | 0.9761 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| DC | lipid_loader_repair | 29 | -0.1826 | 0.1659 | -0.2717 | 0.9761 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| C1Qhi IL1Bhi macro | tnf_autocrine_nfkb | 14 | 0.2288 | 0.08319 | 0.3557 | 0.9761 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| C1Qhi IL1Bhi macro | lipid_loader_repair | 14 | 0.3793 | 0.1353 | 0.05985 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| C1Qhi IL1Bhi macro | lysosomal_apc | 14 | 0.2972 | 0.07988 | 0.04671 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| C1Qhi IL1Bhi macro | complement_phagocytosis | 14 | -0.06695 | 0.17 | -0.2115 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| C1Qhi IL1Bhi macro | ifn_apc | 14 | -0.2078 | 0.01192 | -0.2711 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| C1Qhi IL1Blo macro | lipid_loader_repair | 17 | -0.1298 | 0.02764 | -0.02223 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| C1Qhi IL1Blo macro | lysosomal_apc | 17 | 0.05991 | -0.1148 | 0.1843 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| C1Qhi IL1Blo macro | complement_phagocytosis | 17 | -0.104 | 0.09491 | 0.1334 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| C1Qhi IL1Blo macro | ifn_apc | 17 | -0.08852 | 0.08445 | 0.05783 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| C1Qhi IL1Blo macro | tnf_autocrine_nfkb | 17 | -0.3019 | 0.3051 | -0.3127 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| CD1Chi DC | lipid_loader_repair | 21 | -0.2334 | 0.1184 | -0.2377 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| CD1Chi DC | lysosomal_apc | 21 | -0.001845 | 0.1331 | -0.1052 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| CD1Chi DC | complement_phagocytosis | 21 | -0.243 | 0.1169 | -0.08745 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| CD1Chi DC | inflammatory_nfkb | 21 | -0.08045 | 0.1645 | -0.1504 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| DC | ifn_apc | 29 | -0.06197 | 0.125 | 0.00256 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| Mono_macro | lysosomal_apc | 29 | 0.267 | -0.04129 | 0.3523 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| Mono_macro | complement_phagocytosis | 29 | -0.05512 | 0.1271 | 0.1158 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |
| CD1Chi DC | ifn_apc | 21 | -0.01625 | 0.1494 | 0.04343 | 1 | target_delta ~ remission_binary + baseline_target + generic_delta + baseline_inflammation_score + C(Disease) |

## Gene Coverage

- `ifn_apc`: 8/8 genes present.
- `hla_ii_apc`: 7/7 genes present.
- `lysosomal_apc`: 14/14 genes present.
- `mif_cd74_receptor_state`: 7/7 genes present.
- `mixscale_validated_ifng_readout`: 8/8 genes present.
- `lipid_loader_repair`: 14/14 genes present.
- `complement_phagocytosis`: 12/12 genes present.
- `hif_nampt_metabolic`: 8/8 genes present.
- `inflammatory_nfkb`: 9/9 genes present.
- `tnf_autocrine_nfkb`: 12/12 genes present.
- `host_defense_cost`: 8/8 genes present.

## Interpretation Guardrails

- This is patient/site-level pseudobulk in annotated myeloid states, not single-cell causal perturbation.
- Anti-TNF is a broad intervention. Module movement must exceed or survive generic TNF/NF-kB/IFN controls before a controller can be reopened.
- Remission status is an outcome association and not randomized target perturbation.
- Fine-state rows are secondary because many states lack enough paired cells.
