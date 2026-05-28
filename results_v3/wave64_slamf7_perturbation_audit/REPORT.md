# Wave64 SLAMF7 Perturbation Audit

Random seed: `20260527`.

## Data

- Direct perturbation: `GSE185509`, human monocyte-derived macrophages, all samples IFN-g pre-incubated for 24 h, then 4 h unstimulated, anti-SLAMF7, or recombinant SLAMF7.
- Genetics: local Wave62 Open Targets QTL colocalisation table.
- Cell-state: local broad h5ad donor-level disease-vs-control table plus MS white-matter microglia table.

## Verdict

- Call: `PARK_AS_DIRECTIONAL_INFLAMMATORY_RECEPTOR_NOT_V3_TARGET`.
- Reasons:
  - `direct_slamf7_engagement_amplifies_inflammatory_or_apc_modules`
  - `broad_autoimmune_qtl_coloc_present`
  - `local_cell_state_or_ms_anchor_insufficient`
  - `published_ms_eae_direction_conflict_requires_hostile_review`
  - `existing_elotuzumab_is_activating_not_clean_antagonist`

## Top Module Effects

| module | treatment | n paired | mean treated - unstim | paired mean diff | paired p | paired FDR | Hedges g |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| hif_nampt_metabolic | r-SLAMF7 | 4 | 0.7914 | 0.7914 | 4.598e-05 | 0.001104 | 2.552 |
| hla_ii_apc | r-SLAMF7 | 4 | -0.9992 | -0.9992 | 0.002454 | 0.01616 | -1.46 |
| lipid_loader_repair | r-SLAMF7 | 4 | -0.8594 | -0.8594 | 0.002693 | 0.01616 | -2.117 |
| tnf_autocrine_nfkb | anti-SLAMF7 | 3 | 1.628 | 1.767 | 0.001845 | 0.01616 | 4.407 |
| tnf_autocrine_nfkb | r-SLAMF7 | 4 | 1.56 | 1.56 | 0.003603 | 0.01729 | 4.834 |
| complement_phagocytosis | r-SLAMF7 | 4 | -1.476 | -1.476 | 0.005266 | 0.01805 | -2.72 |
| inflammatory_nfkb | anti-SLAMF7 | 3 | 1.615 | 1.801 | 0.004932 | 0.01805 | 3.481 |
| host_defense_cost | r-SLAMF7 | 4 | 1.185 | 1.185 | 0.006424 | 0.01836 | 5.432 |
| inflammatory_nfkb | r-SLAMF7 | 4 | 1.5 | 1.5 | 0.008169 | 0.01836 | 3.797 |
| lysosomal_apc | r-SLAMF7 | 4 | -1.182 | -1.182 | 0.008234 | 0.01836 | -3.144 |
| mixscale_validated_ifng_readout | anti-SLAMF7 | 3 | -0.6155 | -0.6899 | 0.008414 | 0.01836 | -2.831 |
| host_defense_cost | anti-SLAMF7 | 3 | 1.328 | 1.421 | 0.009778 | 0.01956 | 5.916 |

## QTL Colocalisation Summary

| disease | qtl type | rows | strong coloc | max h4 | max clpp | directions | biosamples |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| UC | eqtl | 6 | 6 | 0.9988 | 0.4164 | -0.0088692677748584;-0.0106892589410372;-0.0143357889133466;-0.0522838443283871;-0.0701300405461454;-0.16 | lymphoblastoid cell line |
| T1D | pqtl | 4 | 3 | 0.9971 | 0.2363 | -0.0655265666384579;-0.0780474794945636;-0.2182443156099665;0.0028697564261032 | blood plasma |
| SLE | eqtl | 2 | 2 | 0.9941 | 0.1344 | -0.0530132171297721;0.0 | lymphoblastoid cell line |
| Psoriasis | pqtl | 2 | 2 | 0.9915 | 0.09775 | -0.0109515733450906;-0.0176062340205465 | blood plasma |
| AS | eqtl | 1 | 1 | 0.9982 | 0.3363 | -0.0253178079842898 | lymphoblastoid cell line |
| Crohn | eqtl | 1 | 1 | 0.9971 | 0.2352 | -0.0073025392084787 | lymphoblastoid cell line |
| UC | pqtl | 1 | 1 | 0.9799 | 0.0421 | 0.0068645150784741 | blood plasma |

## Local Cell-State Anchor

- Broad h5ad positive diseases for SLAMF7: `Crohn disease;Sjogren syndrome`.
- Broad h5ad positive disease count: `2`.
- MS white-matter delta/FDR from broad row: `0.2484880405129503` / `0.9761732664217524`.

## Interpretation

This is useful as a directional receptor audit, not a target nomination. If SLAMF7 engagement amplifies the module, the therapeutic direction would require antagonism or signal-biasing. Existing clinical SLAMF7 antibody precedent is not automatically usable because elotuzumab is immunostimulatory, and published EAE work raises MS-direction concerns. A V3 claim would require disease-cell antagonist perturbation, not stimulation data alone.
