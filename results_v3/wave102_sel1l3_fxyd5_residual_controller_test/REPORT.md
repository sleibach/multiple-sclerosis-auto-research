# Wave102 SEL1L3/FXYD5 Residual Controller Test

## Bottom Line

Branch call: `NO_REOPEN_ACCESSIBLE_SURVIVOR_AFTER_RESIDUAL_TEST`.

`SEL1L3` and `FXYD5` do not clear the residual/controller bar. Their
accessible disease signals remain insufficiently separated from
generic lipid-lysosomal, lysosomal, IFN/APC, NF-kB, HIF/NAMPT, and
C15/MOCCI-like tissue state variation.

## Integrated Candidate Summary

| gene | integrated_call | wave101_score | ms_delta_log2 | ms_p | raw_positive_disease_count | residual_retained_disease_count | same_donor_positive_link_disease_count | blocker_notes | best_residual_context | best_same_donor_link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CD82 | NO_GO_RESIDUAL_CONTROLLER_NOT_PROVEN | 17.16 | 0.5037 | 0.1729 | 2 | 1 | 3 | residual_retained_diseases_lt2;wave101_missing:ms_anchor_or_trend;perturbation_or_model;genetic_anchor;prior_not_known_block | ibd_uc_stromal\|ulcerative colitis\|colon stromal\|delta=0.673\|p=0.0327 | ibd_uc_epithelial->ibd_uc_myeloid\|lipid_loader_repair\|rho_all=0.741\|p_all=0.0058\|rho_case=0.543\|p_case=0.266 |
| LAPTM5 | NO_GO_RESIDUAL_CONTROLLER_NOT_PROVEN | 15.11 | 0.2727 | 0.1304 | 1 | 1 | 2 | residual_retained_diseases_lt2;wave101_missing:ms_anchor_or_trend;perturbation_or_model;genetic_anchor;direction_not_conflicted | ibd_uc_stromal\|ulcerative colitis\|colon stromal\|delta=0.377\|p=0.0328 | ibd_uc_stromal->ibd_uc_myeloid\|inflammatory_nfkb\|rho_all=0.748\|p_all=0.00512\|rho_case=0.543\|p_case=0.266 |
| SEL1L3 | NO_GO_RESIDUAL_CONTROLLER_NOT_PROVEN | 22.78 | 0.9225 | 0.01814 | 0 | 0 | 4 | residual_retained_diseases_lt2;wave101_missing:perturbation_or_model;genetic_anchor |  | ibd_uc_stromal->ibd_uc_myeloid\|inflammatory_nfkb\|rho_all=0.685\|p_all=0.0139\|rho_case=0.714\|p_case=0.111 |
| FXYD5 | NO_GO_RESIDUAL_CONTROLLER_NOT_PROVEN | 17.23 | 0.3525 | 0.05871 | 3 | 0 | 2 | residual_retained_diseases_lt2;residual_negative_context_present;wave101_missing:perturbation_or_model;genetic_anchor;direction_not_conflicted |  | ibd_uc_epithelial->ibd_uc_myeloid\|inflammatory_nfkb\|rho_all=0.608\|p_all=0.0358\|rho_case=0.0286\|p_case=0.957 |
| APOC1 | NO_GO_RESIDUAL_CONTROLLER_NOT_PROVEN | 14.41 | 0.8063 | 0.03335 | 0 | 0 | 2 | residual_retained_diseases_lt2;residual_negative_context_present;wave101_missing:response_signal;perturbation_or_model;genetic_anchor;direction_not_conflicted |  | ibd_uc_epithelial->ibd_uc_myeloid\|c15_mocci_costate\|rho_all=0.594\|p_all=0.0415\|rho_case=-0.0857\|p_case=0.872 |

## Retained Residual Contexts

| gene | analysis | disease_name | compartment | role | raw_delta_case_minus_control | raw_p | residual_delta_case_minus_control | residual_p | covariate_modules |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CD82 | ibd_uc_stromal | ulcerative colitis | colon stromal | tissue_resident | 0.6689 | 0.03413 | 0.6728 | 0.03266 | lipid_loader_repair;lysosomal_apc;ifn_apc;inflammatory_nfkb;hif_nampt_metabolic;c15_mocci_costate |
| LAPTM5 | ibd_uc_stromal | ulcerative colitis | colon stromal | tissue_resident | 0.3827 | 0.03045 | 0.3769 | 0.03285 | lipid_loader_repair;lysosomal_apc;ifn_apc;inflammatory_nfkb;hif_nampt_metabolic;c15_mocci_costate |

## Same-Donor Tissue-to-Myeloid Links

| gene | tissue_analysis | myeloid_analysis | disease_name | tissue_compartment | myeloid_module | n_paired_donors | spearman_rho_all | spearman_p_all | n_case_paired_donors | spearman_rho_case | spearman_p_case |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APOC1 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | c15_mocci_costate | 12 | 0.5944 | 0.04152 | 6 | -0.08571 | 0.8717 |
| APOC1 | psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | skin stromal | lipid_loader_repair | 6 | 0.8286 | 0.04156 | 3 |  |  |
| APOC1 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | inflammatory_nfkb | 12 | 0.5804 | 0.04786 | 6 | 0.1429 | 0.7872 |
| APOC1 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | lysosomal_apc | 12 | 0.5455 | 0.06661 | 6 | 0.2571 | 0.6228 |
| CD82 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | lipid_loader_repair | 12 | 0.7413 | 0.005801 | 6 | 0.5429 | 0.2657 |
| CD82 | ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | colon stromal | inflammatory_nfkb | 12 | 0.7273 | 0.007355 | 6 | 0.8286 | 0.04156 |
| CD82 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | c15_mocci_costate | 12 | 0.7273 | 0.007355 | 6 | 0.4286 | 0.3965 |
| CD82 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | c15_mocci_costate | 22 | 0.5426 | 0.009073 | 9 | 0.3833 | 0.3085 |
| CD82 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | lysosomal_apc | 12 | 0.6993 | 0.01137 | 6 | 0.02857 | 0.9572 |
| CD82 | ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | colon stromal | c15_mocci_costate | 12 | 0.6713 | 0.01683 | 6 | 0.9429 | 0.004805 |
| CD82 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | lipid_loader_repair | 12 | 0.6643 | 0.01845 | 6 | 0.1429 | 0.7872 |
| CD82 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | lysosomal_apc | 12 | 0.6643 | 0.01845 | 6 | 0.2571 | 0.6228 |
| CD82 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 12 | 0.6573 | 0.02019 | 6 | 0.2 | 0.704 |
| CD82 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | inflammatory_nfkb | 12 | 0.6224 | 0.03068 | 6 | 0.2571 | 0.6228 |
| CD82 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | inflammatory_nfkb | 12 | 0.5944 | 0.04152 | 6 | 0.2571 | 0.6228 |
| CD82 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 22 | 0.4342 | 0.04347 | 9 | 0.25 | 0.5165 |
| FXYD5 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | inflammatory_nfkb | 12 | 0.6084 | 0.03581 | 6 | 0.02857 | 0.9572 |
| FXYD5 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | inflammatory_nfkb | 12 | 0.5944 | 0.04152 | 6 | 0.5429 | 0.2657 |
| FXYD5 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 12 | 0.4406 | 0.1517 | 6 | 0.7714 | 0.0724 |
| FXYD5 | ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | colon stromal | lipid_loader_repair | 12 | 0.2727 | 0.3911 | 6 | 0.8286 | 0.04156 |
| LAPTM5 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | inflammatory_nfkb | 12 | 0.7483 | 0.005124 | 6 | 0.5429 | 0.2657 |
| LAPTM5 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | c15_mocci_costate | 12 | 0.7063 | 0.01025 | 6 | 0.2571 | 0.6228 |
| LAPTM5 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | lysosomal_apc | 12 | 0.6783 | 0.01532 | 6 | 0.8286 | 0.04156 |
| LAPTM5 | ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | colon stromal | lipid_loader_repair | 12 | 0.2557 | 0.4225 | 6 | 1 | 0 |
| SEL1L3 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | inflammatory_nfkb | 12 | 0.6853 | 0.01391 | 6 | 0.7143 | 0.1108 |
| SEL1L3 | psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | skin stromal | c15_mocci_costate | 6 | 0.8857 | 0.01885 | 3 |  |  |
| SEL1L3 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | c15_mocci_costate | 12 | 0.6364 | 0.0261 | 6 | 0.6 | 0.208 |
| SEL1L3 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | c15_mocci_costate | 22 | 0.4647 | 0.02933 | 9 | 0.4667 | 0.2054 |
| SEL1L3 | ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | colon stromal | c15_mocci_costate | 12 | 0.6154 | 0.03317 | 6 | 0.6 | 0.208 |
| SEL1L3 | ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | colon stromal | inflammatory_nfkb | 12 | 0.5944 | 0.04152 | 6 | 0.4857 | 0.3287 |

## Interpretation

- This test is stricter than Wave101 because it asks whether candidate
  expression retains disease signal after state-module adjustment and
  whether tissue candidate expression tracks same-donor myeloid state.
- A retained residual is still observational; it does not prove that the
  candidate controls the myeloid module.
- A no-reopen call means the branch should not proceed without direct
  perturbation data.

## Run Log

| analysis | status | gene_rows | module_rows |
| --- | --- | --- | --- |
| ibd_crohn_myeloid | completed | 60 | 96 |
| ibd_uc_myeloid | completed | 60 | 96 |
| ibd_crohn_epithelial | completed | 60 | 96 |
| ibd_uc_epithelial | completed | 60 | 96 |
| ibd_crohn_stromal | completed | 60 | 96 |
| ibd_uc_stromal | completed | 60 | 96 |
| psoriasis_skin_apc | completed | 30 | 48 |
| psoriasis_keratinocyte | completed | 30 | 48 |
| psoriasis_skin_stromal | completed | 30 | 48 |
| sjogren_gland_apc | completed | 110 | 176 |
| sjogren_gland_epithelial | completed | 125 | 200 |
| sjogren_gland_stromal | completed | 120 | 192 |
| ra_blood_myeloid | completed | 180 | 288 |
| t1d_beta_cell | completed | 110 | 176 |
| t1d_ductal_cell | completed | 120 | 192 |
| t1d_acinar_cell | completed | 115 | 184 |
| t1d_stellate_cell | completed | 105 | 168 |
| t1d_endothelial_cell | completed | 110 | 176 |

## Reproducibility

- Script: `scripts/v3_wave102_sel1l3_fxyd5_residual_controller_test.py`
- Candidate gene scores: `results_v3/wave102_sel1l3_fxyd5_residual_controller_test/candidate_gene_scores.tsv`
- Module scores: `results_v3/wave102_sel1l3_fxyd5_residual_controller_test/candidate_module_scores.tsv`
- Residual tests: `results_v3/wave102_sel1l3_fxyd5_residual_controller_test/candidate_multicovariate_residual_tests.tsv`
- Same-donor links: `results_v3/wave102_sel1l3_fxyd5_residual_controller_test/same_donor_tissue_to_myeloid_links.tsv`
- Seed: `20260527`
