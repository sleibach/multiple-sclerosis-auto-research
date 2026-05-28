# Wave102 Accessible-Survivor Residual Compartment Test

## Bottom Line

Branch call: `NO_ACCESSIBLE_SURVIVOR_RESIDUAL_REOPEN`.

This test asks whether accessible survivors remain disease-associated after
same-compartment donor-level adjustment for lipid-lysosomal, lysosomal/APC,
IFN/APC, NF-kB, and HIF/NAMPT inflammatory modules. Passing this test is not a
therapeutic claim; it only justifies spending effort on target-specific
perturbation, genetics, and modality.

## Candidate Summary

| gene | wave102_call | wave102_residual_priority_score | present_analysis_count | raw_positive_disease_count | retained_positive_disease_count | strict_core_covariate_surviving_disease_count | core_all_multivariable_surviving_disease_count | non_ibd_retained_positive_disease_count | lipid_lysosomal_surviving_disease_count | raw_negative_analysis_count | raw_positive_analyses | top_retained_tests |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHI3L1 | PARK_WEAK_RESIDUAL_SIGNAL_ONLY | 6 | 17 | 2 | 2 | 0 | 0 | 1 | 2 | 0 | ibd_uc_stromal:4.14,p=0.02;psoriasis_skin_stromal:0.477,p=0.047 | psoriasis_skin_stromal\|hif_nampt_metabolic:0.455,p=0.01;ibd_uc_stromal\|complement_effector:4.19,p=0.012;ibd_uc_stromal\|ifn_apc:4.02,p=0.016;ibd_uc_stromal\|hla_ii_apc:4.19,p=0.018;psoriasis_skin_stromal\|inflammatory_nfkb:0.481,p=0.018;psoriasis_skin_stromal\|lipid_loader_repair:0.493,p=0.02;ibd_uc_stromal\|lysosomal_apc:4.03,p=0.024;psoriasis_skin_stromal\|c1q_phagocytic_myeloid:0.48,p=0.045 |
| FXYD5 | PARK_WEAK_RESIDUAL_SIGNAL_ONLY | 5 | 18 | 3 | 2 | 0 | 0 | 1 | 1 | 1 | psoriasis_keratinocyte:0.365,p=0.029;t1d_endothelial_cell:0.367,p=0.029;ibd_uc_epithelial:0.426,p=0.036 | psoriasis_keratinocyte\|hif_nampt_metabolic:0.237,p=0.032;ibd_uc_epithelial\|lysosomal_apc:0.43,p=0.032;ibd_uc_epithelial\|complement_phagocytosis:0.423,p=0.036;psoriasis_keratinocyte\|inflammatory_nfkb:0.356,p=0.049 |
| NRCAM | PARK_WEAK_RESIDUAL_SIGNAL_ONLY | 4 | 18 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | psoriasis_skin_stromal:0.379,p=0.018 | psoriasis_skin_stromal\|inflammatory_nfkb:0.373,p=0.00047;psoriasis_skin_stromal\|hif_nampt_metabolic:0.39,p=0.0024;psoriasis_skin_stromal\|c1q_phagocytic_myeloid:0.363,p=0.022;psoriasis_skin_stromal\|lipid_loader_repair:0.349,p=0.03 |
| SEL1L3 | PARK_WEAK_RESIDUAL_SIGNAL_ONLY | 3 | 18 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | ibd_uc_stromal:0.282,p=0.035 | ibd_uc_stromal\|lysosomal_apc:0.327,p=0.0051;ibd_uc_stromal\|complement_effector:0.288,p=0.011;ibd_uc_stromal\|core_lysosomal_lipid:0.254,p=0.022;ibd_uc_stromal\|hla_ii_apc:0.255,p=0.026;ibd_uc_stromal\|ifn_apc:0.287,p=0.029 |
| CD82 | PARK_WEAK_RESIDUAL_SIGNAL_ONLY | 2 | 18 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | ibd_uc_stromal:0.669,p=0.034 | ibd_uc_stromal\|complement_effector:0.686,p=0.0018;ibd_uc_stromal\|hla_ii_apc:0.701,p=0.018;ibd_uc_stromal\|ifn_apc:0.636,p=0.019;ibd_uc_stromal\|lysosomal_apc:0.702,p=0.024;ibd_uc_stromal\|inflammatory_nfkb:0.691,p=0.027 |
| LAPTM5 | PARK_WEAK_RESIDUAL_SIGNAL_ONLY | 2 | 18 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | ibd_uc_stromal:0.383,p=0.03 | ibd_uc_stromal\|lysosomal_apc:0.405,p=0.019;ibd_uc_stromal\|ifn_apc:0.386,p=0.028;ibd_uc_stromal\|complement_effector:0.382,p=0.03;ibd_uc_stromal\|hla_ii_apc:0.362,p=0.031;ibd_uc_stromal\|core_lysosomal_lipid:0.265,p=0.039;ibd_uc_stromal\|inflammatory_nfkb:0.353,p=0.048 |
| ADM | PARK_WEAK_RESIDUAL_SIGNAL_ONLY | -1 | 18 | 3 | 2 | 0 | 0 | 0 | 1 | 2 | ibd_uc_myeloid:0.579,p=0.02;ibd_crohn_myeloid:0.743,p=0.036;psoriasis_keratinocyte:0.343,p=0.045 | ibd_crohn_myeloid\|hla_ii_apc:0.846,p=0.0016;ibd_crohn_myeloid\|mif_cd74_receptor_state:0.804,p=0.02;ibd_crohn_myeloid\|complement_effector:0.769,p=0.028;ibd_uc_myeloid\|hla_ii_apc:0.523,p=0.033;ibd_crohn_myeloid\|core_lysosomal_lipid:0.637,p=0.038;ibd_crohn_myeloid\|c1q_phagocytic_myeloid:0.561,p=0.043 |
| CD200 | NO_GO_NO_DIRECT_H5AD_REPLICATION | 0 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |
| BTN2A2 | NO_GO_NO_DIRECT_H5AD_REPLICATION | 0 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |
| MFGE8 | NO_GO_NO_DIRECT_H5AD_REPLICATION | -3 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |  |  |
| GPNMB | NO_GO_NO_DIRECT_H5AD_REPLICATION | -3 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |  |  |
| APOC1 | NO_GO_NO_DIRECT_H5AD_REPLICATION | -5 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |  |  |

## Guardrail

Residual survival can still reflect severity, cell composition within broad
compartments, batch, medication, tissue injury, or unmodeled stromal state.
Failure, however, is strong evidence against treating a candidate expression
signal as a mechanistic anchor in this V3 session.

## Reproducibility

- Script: `scripts/v3_wave102_accessible_survivor_residual_compartment_test.py`
- Donor scores: `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_donor_scores.tsv`
- Raw tests: `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_raw_tests.tsv`
- Residual tests: `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_residual_tests.tsv`
- Summary: `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_residual_summary.tsv`
- Seed: `20260527`
