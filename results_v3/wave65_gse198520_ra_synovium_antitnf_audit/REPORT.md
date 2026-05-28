# Wave65 GSE198520 RA Synovium Anti-TNF Audit

Random seed: `20260527`.

## Data

- Accession: `GSE198520`.
- System: paired RA synovial bulk RNA-seq, baseline and week 12 after anti-TNF.
- Samples parsed: `92`; patients: `46`.
- Response counts: `{'good': 19, 'none': 14, 'moderate': 13}`.
- Pathotype counts: `{'Myeloid': 21, 'Lymphoid': 17, 'Fibroid': 8}`.

## Verdict

- No module is promoted as a V3 mechanism from this bulk tissue audit.
- Bulk synovium can test pharmacodynamic tissue movement, but it cannot prove myeloid cell-intrinsic intervention.
- Any apparent lipid/APC movement must exceed generic IFN/NF-kB movement and survive pathotype adjustment.

## Gate Summary

| module | all paired effect | all FDR | target/generic | adjusted response FDR | call | failed gates |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| mif_cd74_receptor_state | -0.3464 | 0.009266 | 0.9851 | 0.9723 | NO_GO_GSE198520_BULK_TISSUE | target_to_generic_ratio_lt_2;no_response_specific_effect_after_generic_pathotype_adjustment;bulk_synovium_cell_composition_unresolved;no_functional_repair_or_host_defense_guardrail |
| mixscale_validated_ifng_readout | -0.4037 | 0.009266 | 1.148 | 0.9723 | NO_GO_GSE198520_BULK_TISSUE | target_to_generic_ratio_lt_2;no_response_specific_effect_after_generic_pathotype_adjustment;bulk_synovium_cell_composition_unresolved;no_functional_repair_or_host_defense_guardrail |
| hif_nampt_metabolic | -0.2777 | 0.009266 | 0.7897 | 0.9723 | NO_GO_GSE198520_BULK_TISSUE | target_to_generic_ratio_lt_2;no_response_specific_effect_after_generic_pathotype_adjustment;bulk_synovium_cell_composition_unresolved;no_functional_repair_or_host_defense_guardrail |
| ifn_apc | -0.3516 | 0.02412 | 1 | 0.9723 | NO_GO_GSE198520_BULK_TISSUE | generic_module_positive_control;target_to_generic_ratio_lt_2;no_response_specific_effect_after_generic_pathotype_adjustment;bulk_synovium_cell_composition_unresolved;no_functional_repair_or_host_defense_guardrail |
| hla_ii_apc | -0.2824 | 0.02412 | 0.8032 | 0.9723 | NO_GO_GSE198520_BULK_TISSUE | target_to_generic_ratio_lt_2;no_response_specific_effect_after_generic_pathotype_adjustment;bulk_synovium_cell_composition_unresolved;no_functional_repair_or_host_defense_guardrail |
| lysosomal_apc | -0.2907 | 0.03404 | 0.8268 | 0.9723 | NO_GO_GSE198520_BULK_TISSUE | target_to_generic_ratio_lt_2;no_response_specific_effect_after_generic_pathotype_adjustment;bulk_synovium_cell_composition_unresolved;no_functional_repair_or_host_defense_guardrail |
| complement_phagocytosis | -0.2915 | 0.04516 | 0.8292 | 0.9991 | NO_GO_GSE198520_BULK_TISSUE | target_to_generic_ratio_lt_2;no_response_specific_effect_after_generic_pathotype_adjustment;bulk_synovium_cell_composition_unresolved;no_functional_repair_or_host_defense_guardrail |
| inflammatory_nfkb | -0.1411 | 0.1047 | 0.4012 | 0.6548 | NO_GO_GSE198520_BULK_TISSUE | generic_module_positive_control;no_fdr10_paired_pharmacodynamic_effect;target_to_generic_ratio_lt_2;no_response_specific_effect_after_generic_pathotype_adjustment;bulk_synovium_cell_composition_unresolved;no_functional_repair_or_host_defense_guardrail |
| lipid_loader_repair | -0.09674 | 0.2378 | 0.2751 | 0.9202 | NO_GO_GSE198520_BULK_TISSUE | no_fdr10_paired_pharmacodynamic_effect;target_to_generic_ratio_lt_2;no_response_specific_effect_after_generic_pathotype_adjustment;bulk_synovium_cell_composition_unresolved;no_functional_repair_or_host_defense_guardrail |

## Top Paired Pharmacodynamic Rows

| scope | module | n | mean post-pre | p | FDR |
| --- | --- | ---: | ---: | ---: | ---: |
| all_patients | hif_nampt_metabolic | 46 | -0.2777 | 0.0003247 | 0.009266 |
| all_patients | mif_cd74_receptor_state | 46 | -0.3464 | 0.0008237 | 0.009266 |
| all_patients | mixscale_validated_ifng_readout | 46 | -0.4037 | 0.0007038 | 0.009266 |
| moderate_or_good | mif_cd74_receptor_state | 32 | -0.4651 | 0.0008089 | 0.009266 |
| moderate_or_good | hif_nampt_metabolic | 32 | -0.3404 | 0.001496 | 0.01347 |
| all_patients | hla_ii_apc | 46 | -0.2824 | 0.004558 | 0.02412 |
| all_patients | ifn_apc | 46 | -0.3516 | 0.005425 | 0.02412 |
| good_responders | mif_cd74_receptor_state | 19 | -0.5405 | 0.006432 | 0.02412 |
| good_responders | mixscale_validated_ifng_readout | 19 | -0.6147 | 0.006286 | 0.02412 |
| moderate_or_good | ifn_apc | 32 | -0.4839 | 0.005592 | 0.02412 |
| moderate_or_good | lysosomal_apc | 32 | -0.4258 | 0.003806 | 0.02412 |
| moderate_or_good | mixscale_validated_ifng_readout | 32 | -0.4547 | 0.004536 | 0.02412 |
| all_patients | lysosomal_apc | 46 | -0.2907 | 0.009835 | 0.03404 |
| good_responders | inflammatory_nfkb | 19 | -0.3849 | 0.01102 | 0.03542 |
| good_responders | hif_nampt_metabolic | 19 | -0.3907 | 0.01254 | 0.03761 |
| good_responders | ifn_apc | 19 | -0.6377 | 0.01586 | 0.03965 |
| moderate_or_good | complement_phagocytosis | 32 | -0.4149 | 0.01439 | 0.03965 |
| moderate_or_good | inflammatory_nfkb | 32 | -0.2561 | 0.01553 | 0.03965 |
| good_responders | lysosomal_apc | 19 | -0.5059 | 0.01805 | 0.04275 |
| all_patients | complement_phagocytosis | 46 | -0.2915 | 0.02007 | 0.04516 |

## Top Response-Delta Rows

| contrast | module | raw delta | raw FDR | adjusted delta | adjusted FDR | max generic r |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| moderate_good_vs_none | inflammatory_nfkb | -0.3779 | 0.04487 | -0.2285 | 0.6548 | 0.5732 |
| good_vs_moderate_none | inflammatory_nfkb | -0.4154 | 0.1063 | -0.2712 | 0.6548 | 0.5732 |
| moderate_good_vs_none | mixscale_validated_ifng_readout | -0.1676 | 0.4903 | 0.2026 | 0.6548 | 0.8901 |
| good_vs_moderate_none | lipid_loader_repair | -0.002823 | 0.9857 | 0.1881 | 0.9202 | 0.4385 |
| moderate_good_vs_none | ifn_apc | -0.4348 | 0.1137 | -0.06808 | 0.9723 | 0.5732 |
| moderate_good_vs_none | lysosomal_apc | -0.4438 | 0.1137 | -0.05733 | 0.9723 | 0.8915 |
| moderate_good_vs_none | mif_cd74_receptor_state | -0.3902 | 0.1137 | -0.1222 | 0.9723 | 0.7352 |
| good_vs_moderate_none | ifn_apc | -0.4875 | 0.1756 | -0.1408 | 0.9723 | 0.5732 |
| moderate_good_vs_none | hif_nampt_metabolic | -0.2063 | 0.1756 | 0.03798 | 0.9723 | 0.6909 |
| good_vs_moderate_none | lysosomal_apc | -0.3666 | 0.2007 | 0.06212 | 0.9723 | 0.8915 |
| good_vs_moderate_none | mif_cd74_receptor_state | -0.3308 | 0.2007 | -0.02751 | 0.9723 | 0.7352 |
| good_vs_moderate_none | mixscale_validated_ifng_readout | -0.3595 | 0.2007 | 0.02027 | 0.9723 | 0.8901 |

## Gene Coverage

- `ifn_apc`: 8/8 genes present.
- `hla_ii_apc`: 7/7 genes present.
- `lysosomal_apc`: 7/7 genes present.
- `mif_cd74_receptor_state`: 7/7 genes present.
- `mixscale_validated_ifng_readout`: 8/8 genes present.
- `lipid_loader_repair`: 12/12 genes present.
- `complement_phagocytosis`: 7/7 genes present.
- `hif_nampt_metabolic`: 8/8 genes present.
- `inflammatory_nfkb`: 9/9 genes present.
