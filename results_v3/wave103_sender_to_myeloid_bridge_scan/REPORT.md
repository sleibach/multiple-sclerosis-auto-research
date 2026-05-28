# Wave103 Sender-to-Myeloid Bridge Scan

## Bottom Line

Branch call: `REOPEN_BRIDGE_AXIS_FOR_WAVE104`.

This scan ranks tissue-resident communication genes by same-donor
association with paired myeloid lipid/C15/inflammatory modules. It is
a bridge-discovery screen, not a therapeutic claim.

## Top Gene Summary

| gene | wave103_call | bridge_score | upregulated_bridge_link_disease_count | bridge_link_disease_count | raw_up_tissue_disease_count | raw_down_tissue_disease_count | case_link_count | best_wave30_axis | best_wave30_call | wave30_prior_blocking | best_bridge_link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CALR | REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT | 21 | 2 | 3 | 4 | 0 | 3 |  |  | False | ibd_uc_epithelial->ibd_uc_myeloid\|inflammatory_nfkb\|rho_all=0.888\|p_all=0.000114\|rho_case=0.314\|p_case=0.544\|sender_delta=0.459\|sender_p=0.000691 |
| HIF1A | REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT | 21 | 2 | 3 | 3 | 0 | 4 |  |  | False | ibd_uc_stromal->ibd_uc_myeloid\|c15_mocci_costate\|rho_all=0.923\|p_all=1.86e-05\|rho_case=0.771\|p_case=0.0724\|sender_delta=1.12\|sender_p=0.000612 |
| STAT3 | REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT | 20.05 | 2 | 3 | 2 | 0 | 3 | OSM_OSMR_IL6ST_STAT3 | NO_GO_NICHE_DRIVER | False | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.784\|p_all=1.56e-05\|rho_case=0.967\|p_case=2.16e-05\|sender_delta=-0.113\|sender_p=0.333 |
| ITGAV | REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT | 20.01 | 2 | 4 | 2 | 0 | 1 | SPP1_CD44_INTEGRIN_RETENTION | CENTRAL_STATE_DRIVER_NOT_SELECTIVE_THERAPEUTIC | False | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.719\|p_all=0.000164\|rho_case=0.833\|p_case=0.00527\|sender_delta=-0.0532\|sender_p=0.496 |
| IL1B | REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT | 19.17 | 2 | 3 | 2 | 0 | 2 | TREM1_TYROBP_AMPLIFICATION | NO_GO_NICHE_DRIVER | False | ibd_crohn_epithelial->ibd_crohn_myeloid\|c15_mocci_costate\|rho_all=0.832\|p_all=0.000785\|rho_case=0.543\|p_case=0.266\|sender_delta=0.431\|sender_p=0.0463 |
| C2 | REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT | 17 | 2 | 2 | 2 | 0 | 3 |  |  | False | ibd_uc_epithelial->ibd_uc_myeloid\|c15_mocci_costate\|rho_all=0.895\|p_all=8.37e-05\|rho_case=0.829\|p_case=0.0416\|sender_delta=0.786\|sender_p=0.00266 |
| CFB | REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT | 17 | 2 | 2 | 4 | 0 | 1 |  |  | False | ibd_crohn_epithelial->ibd_crohn_myeloid\|c15_mocci_costate\|rho_all=0.86\|p_all=0.000332\|rho_case=0.6\|p_case=0.208\|sender_delta=0.406\|sender_p=0.00712 |
| CXCL1 | REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT | 17 | 2 | 2 | 3 | 0 | 2 |  |  | False | ibd_crohn_epithelial->ibd_crohn_myeloid\|c15_mocci_costate\|rho_all=0.79\|p_all=0.00222\|rho_case=0.771\|p_case=0.0724\|sender_delta=0.637\|sender_p=0.0181 |
| NAMPT | REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT | 17 | 2 | 3 | 2 | 0 | 1 |  |  | False | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.814\|p_all=4.12e-06\|rho_case=0.733\|p_case=0.0246\|sender_delta=-0.0418\|sender_p=0.647 |
| TIMP1 | REOPEN_FOR_WAVE104_BRIDGE_PERTURBATION_AUDIT | 17 | 2 | 2 | 4 | 0 | 1 |  |  | False | ibd_uc_epithelial->ibd_uc_myeloid\|c15_mocci_costate\|rho_all=0.72\|p_all=0.00824\|rho_case=-0.0857\|p_case=0.872\|sender_delta=1.2\|sender_p=0.00662 |
| CD74 | PARK_BRIDGE_PRIOR_OR_DIRECTION_REVIEW | 17.82 | 2 | 2 | 4 | 0 | 2 | IFNG_IFNGR_JAK_STAT1_CIITA | CENTRAL_STATE_DRIVER_NOT_SELECTIVE_THERAPEUTIC | True | ibd_uc_epithelial->ibd_uc_myeloid\|c15_mocci_costate\|rho_all=0.713\|p_all=0.0092\|rho_case=0.486\|p_case=0.329\|sender_delta=0.77\|sender_p=0.0173 |
| CCL20 | PARK_BRIDGE_PRIOR_OR_DIRECTION_REVIEW | 16 | 2 | 2 | 4 | 0 | 0 |  |  | False | ibd_crohn_epithelial->ibd_crohn_myeloid\|c15_mocci_costate\|rho_all=0.867\|p_all=0.00026\|rho_case=0.371\|p_case=0.468\|sender_delta=0.429\|sender_p=0.000619 |
| CXCL2 | PARK_BRIDGE_PRIOR_OR_DIRECTION_REVIEW | 13 | 2 | 2 | 3 | 1 | 0 |  |  | False | ibd_uc_stromal->ibd_uc_myeloid\|c15_mocci_costate\|rho_all=0.769\|p_all=0.00345\|rho_case=0.257\|p_case=0.623\|sender_delta=0.574\|sender_p=0.00899 |
| CXCL3 | PARK_BRIDGE_PRIOR_OR_DIRECTION_REVIEW | 13 | 2 | 2 | 3 | 1 | 0 |  |  | False | ibd_crohn_epithelial->ibd_crohn_myeloid\|c15_mocci_costate\|rho_all=0.783\|p_all=0.00259\|rho_case=0.543\|p_case=0.266\|sender_delta=0.427\|sender_p=0.00768 |
| ANGPT2 | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 16 | 1 | 3 | 2 | 0 | 4 |  |  | False | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.545\|p_all=0.00873\|rho_case=0.833\|p_case=0.00527\|sender_delta=-0.0207\|sender_p=0.78 |
| EREG | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 16 | 1 | 3 | 2 | 0 | 4 |  |  | False | ibd_crohn_stromal->ibd_crohn_myeloid\|inflammatory_nfkb\|rho_all=0.777\|p_all=0.00292\|rho_case=0.829\|p_case=0.0416\|sender_delta=1.93\|sender_p=0.113 |
| JAK1 | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 15.82 | 1 | 3 | 1 | 0 | 5 | IFNG_IFNGR_JAK_STAT1_CIITA | CENTRAL_STATE_DRIVER_NOT_SELECTIVE_THERAPEUTIC | True | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.673\|p_all=0.000606\|rho_case=0.95\|p_case=8.76e-05\|sender_delta=-0.0822\|sender_p=0.48 |
| IL33 | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 15 | 1 | 4 | 1 | 0 | 2 |  |  | False | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.614\|p_all=0.00238\|rho_case=0.717\|p_case=0.0298\|sender_delta=-0.00397\|sender_p=0.97 |
| SERPINE1 | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 13 | 1 | 3 | 2 | 0 | 1 |  |  | False | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.677\|p_all=0.000539\|rho_case=0.75\|p_case=0.0199\|sender_delta=-0.055\|sender_p=0.292 |
| NPC1 | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 12.21 | 0 | 3 | 1 | 0 | 4 | NPC1_NPC2_CHOLESTEROL_EGRESS | NO_GO_NICHE_DRIVER | False | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.687\|p_all=0.000411\|rho_case=0.85\|p_case=0.0037\|sender_delta=-0.0419\|sender_p=0.45 |
| HBEGF | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 12 | 0 | 3 | 1 | 0 | 5 |  |  | False | ibd_uc_stromal->ibd_uc_myeloid\|lipid_loader_repair\|rho_all=0.725\|p_all=0.00759\|rho_case=0.841\|p_case=0.0361\|sender_delta=0.016\|sender_p=0.901 |
| SLC15A4 | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 11.8 | 0 | 3 | 1 | 0 | 3 | SLC15A4_TASL_IRF5_ENDOLYSOSOMAL_TLR | NO_GO_NICHE_DRIVER | False | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.726\|p_all=0.000133\|rho_case=0.933\|p_case=0.000236\|sender_delta=-0.0796\|sender_p=0.155 |
| ICAM1 | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 10 | 0 | 3 | 3 | 0 | 1 |  |  | False | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.755\|p_all=4.89e-05\|rho_case=0.767\|p_case=0.0159\|sender_delta=-0.0383\|sender_p=0.627 |
| TGFB3 | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 10 | 0 | 3 | 0 | 0 | 4 |  |  | False | ibd_uc_stromal->ibd_uc_myeloid\|lysosomal_apc\|rho_all=0.769\|p_all=0.00345\|rho_case=0.943\|p_case=0.0048\|sender_delta=0.172\|sender_p=0.144 |
| TNFSF10 | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 10 | 0 | 3 | 1 | 0 | 3 |  |  | False | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.715\|p_all=0.000182\|rho_case=0.6\|p_case=0.0876\|sender_delta=-0.113\|sender_p=0.274 |
| ANXA1 | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 9 | 1 | 3 | 2 | 2 | 1 |  |  | False | ibd_uc_epithelial->ibd_uc_myeloid\|inflammatory_nfkb\|rho_all=0.797\|p_all=0.0019\|rho_case=0.0857\|p_case=0.872\|sender_delta=1.01\|sender_p=0.0122 |
| CD40 | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 8.951 | 0 | 3 | 2 | 0 | 3 | CD40_CD40LG_APC_LICENSING | NO_GO_NICHE_DRIVER | True | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.659\|p_all=0.000853\|rho_case=0.5\|p_case=0.17\|sender_delta=-0.00936\|sender_p=0.901 |
| IL6ST | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 8.052 | 0 | 3 | 0 | 0 | 1 | OSM_OSMR_IL6ST_STAT3 | NO_GO_NICHE_DRIVER | False | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.757\|p_all=4.51e-05\|rho_case=0.85\|p_case=0.0037\|sender_delta=-0.135\|sender_p=0.292 |
| VEGFB | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 8 | 0 | 3 | 0 | 1 | 4 |  |  | False | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.602\|p_all=0.003\|rho_case=0.95\|p_case=8.76e-05\|sender_delta=-0.105\|sender_p=0.291 |
| TRAF6 | PARK_CORRELATION_ONLY_NOT_DISEASE_UP | 7.951 | 0 | 3 | 0 | 0 | 4 | CD40_CD40LG_APC_LICENSING | NO_GO_NICHE_DRIVER | True | sjogren_gland_stromal->sjogren_gland_apc\|lysosomal_apc\|rho_all=0.671\|p_all=0.000624\|rho_case=0.867\|p_case=0.0025\|sender_delta=-0.0297\|sender_p=0.539 |

## Upregulated Bridge Links

| gene | tissue_analysis | myeloid_analysis | disease_name | tissue_compartment | myeloid_module | n_paired_donors | spearman_rho_all | spearman_p_all | n_case_paired_donors | spearman_rho_case | spearman_p_case | sender_tissue_delta | sender_tissue_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ANGPT2 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | inflammatory_nfkb | 12 | 0.6853 | 0.01391 | 6 | 0.8857 | 0.01885 | 0.4128 | 0.07914 |
| ANGPT2 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | c15_mocci_costate | 12 | 0.6783 | 0.01532 | 6 | 0.7714 | 0.0724 | 0.4128 | 0.07914 |
| ANGPT2 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | lysosomal_apc | 12 | 0.6224 | 0.03068 | 6 | 0.4286 | 0.3965 | 0.4128 | 0.07914 |
| ANXA1 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | inflammatory_nfkb | 12 | 0.7972 | 0.0019 | 6 | 0.08571 | 0.8717 | 1.007 | 0.01221 |
| ANXA1 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | c15_mocci_costate | 12 | 0.6923 | 0.01259 | 6 | 0.02857 | 0.9572 | 1.007 | 0.01221 |
| C2 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | c15_mocci_costate | 12 | 0.8951 | 8.367e-05 | 6 | 0.8286 | 0.04156 | 0.786 | 0.002658 |
| C2 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | inflammatory_nfkb | 12 | 0.8042 | 0.001615 | 6 | 0.7714 | 0.0724 | 0.786 | 0.002658 |
| C2 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 12 | 0.7622 | 0.00395 | 6 | -0.2571 | 0.6228 | 0.7094 | 0.02212 |
| C2 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | lysosomal_apc | 12 | 0.6993 | 0.01137 | 6 | -0.1429 | 0.7872 | 0.786 | 0.002658 |
| C2 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | lipid_loader_repair | 12 | 0.5455 | 0.06661 | 6 | 0.9429 | 0.004805 | 0.786 | 0.002658 |
| CALR | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | inflammatory_nfkb | 12 | 0.8881 | 0.0001141 | 6 | 0.3143 | 0.5441 | 0.4587 | 0.0006908 |
| CALR | ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | colon stromal | c15_mocci_costate | 12 | 0.8252 | 0.0009514 | 6 | 0.8857 | 0.01885 | 0.3542 | 0.01297 |
| CALR | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | inflammatory_nfkb | 12 | 0.7692 | 0.003446 | 6 | 0.6 | 0.208 | 0.4179 | 0.003927 |
| CALR | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | c15_mocci_costate | 12 | 0.7692 | 0.003446 | 6 | 0.2 | 0.704 | 0.4587 | 0.0006908 |
| CALR | ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | colon stromal | inflammatory_nfkb | 12 | 0.7203 | 0.00824 | 6 | 0.9429 | 0.004805 | 0.3542 | 0.01297 |
| CALR | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 12 | 0.6923 | 0.01259 | 6 | 0.4857 | 0.3287 | 0.4179 | 0.003927 |
| CALR | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | lysosomal_apc | 12 | 0.6503 | 0.02203 | 6 | 0.2571 | 0.6228 | 0.4587 | 0.0006908 |
| CCL20 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 12 | 0.8671 | 0.0002598 | 6 | 0.3714 | 0.4685 | 0.4293 | 0.0006192 |
| CCL20 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | c15_mocci_costate | 12 | 0.7622 | 0.00395 | 6 | -0.4857 | 0.3287 | 0.7031 | 0.05999 |
| CCL20 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | inflammatory_nfkb | 12 | 0.7273 | 0.007355 | 6 | -0.3143 | 0.5441 | 0.7031 | 0.05999 |
| CCL20 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | inflammatory_nfkb | 12 | 0.7203 | 0.00824 | 6 | 0.6 | 0.208 | 0.4293 | 0.0006192 |
| CCL20 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | lysosomal_apc | 12 | 0.6783 | 0.01532 | 6 | -0.08571 | 0.8717 | 0.7031 | 0.05999 |
| CD24 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | inflammatory_nfkb | 12 | 0.6923 | 0.01259 | 6 | -0.1429 | 0.7872 | 0.371 | 0.008892 |
| CD24 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | c15_mocci_costate | 12 | 0.5874 | 0.04461 | 6 | -0.4286 | 0.3965 | 0.371 | 0.008892 |
| CD44 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 12 | 0.7273 | 0.007355 | 6 | 0.5429 | 0.2657 | 0.3112 | 0.0102 |
| CD44 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | inflammatory_nfkb | 12 | 0.7133 | 0.009202 | 6 | 0.7714 | 0.0724 | 0.3112 | 0.0102 |
| CD44 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | lipid_loader_repair | 12 | 0.03497 | 0.9141 | 6 | 0.8286 | 0.04156 | 0.3112 | 0.0102 |
| CD74 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | c15_mocci_costate | 12 | 0.7133 | 0.009202 | 6 | 0.4857 | 0.3287 | 0.7703 | 0.01729 |
| CD74 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 12 | 0.6224 | 0.03068 | 6 | -0.1429 | 0.7872 | 0.9462 | 0.01322 |
| CD74 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | lysosomal_apc | 12 | 0.6084 | 0.03581 | 6 | 0.08571 | 0.8717 | 0.7703 | 0.01729 |
| CFB | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 12 | 0.8601 | 0.0003317 | 6 | 0.6 | 0.208 | 0.4061 | 0.007118 |
| CFB | ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | colon stromal | c15_mocci_costate | 12 | 0.7203 | 0.00824 | 6 | 0.3143 | 0.5441 | 0.4189 | 0.007909 |
| CFB | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | inflammatory_nfkb | 12 | 0.6783 | 0.01532 | 6 | 0.7714 | 0.0724 | 0.4061 | 0.007118 |
| CFB | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | c15_mocci_costate | 12 | 0.5919 | 0.04259 | 6 | 0.08571 | 0.8717 | 0.5669 | 0.02032 |
| CFB | ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | colon stromal | inflammatory_nfkb | 12 | 0.5874 | 0.04461 | 6 | 0.08571 | 0.8717 | 0.4189 | 0.007909 |
| CSF3 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | c15_mocci_costate | 12 | 0.8951 | 8.367e-05 | 6 | 0.6 | 0.208 | 1.119 | 0.01186 |
| CSF3 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | inflammatory_nfkb | 12 | 0.8462 | 0.0005211 | 6 | 0.6571 | 0.1562 | 1.119 | 0.01186 |
| CSF3 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | lipid_loader_repair | 12 | 0.7622 | 0.00395 | 6 | 0.7143 | 0.1108 | 1.119 | 0.01186 |
| CSF3 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | lysosomal_apc | 12 | 0.7413 | 0.005801 | 6 | -0.1429 | 0.7872 | 1.119 | 0.01186 |
| CXCL1 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 12 | 0.7902 | 0.002223 | 6 | 0.7714 | 0.0724 | 0.6366 | 0.01811 |

## All Positive Bridge Links

| gene | tissue_analysis | myeloid_analysis | disease_name | tissue_compartment | myeloid_module | spearman_rho_all | spearman_p_all | spearman_rho_case | spearman_p_case | sender_tissue_delta | sender_tissue_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1QA | psoriasis_skin_stromal | psoriasis_skin_apc | psoriasis | skin stromal | lysosomal_apc | 1 | 0 |  |  | 0.08051 | 0.4338 |
| NFKB1 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.8735 | 1.111e-07 | 0.9667 | 2.155e-05 | -0.09238 | 0.2129 |
| NAMPT | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.8137 | 4.116e-06 | 0.7333 | 0.02455 | -0.04178 | 0.6471 |
| CSF1 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.8137 | 4.116e-06 | 0.9333 | 0.0002359 | -0.01596 | 0.8544 |
| RELA | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.7922 | 1.112e-05 | 0.9833 | 1.936e-06 | -0.08888 | 0.188 |
| STAT3 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.7843 | 1.56e-05 | 0.9667 | 2.155e-05 | -0.1129 | 0.3329 |
| HIF1A | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | c15_mocci_costate | 0.9231 | 1.862e-05 | 0.7714 | 0.0724 | 1.119 | 0.0006121 |
| PROS1 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.773 | 2.469e-05 | 0.8667 | 0.002495 | -0.09693 | 0.2751 |
| TGFB1 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.7696 | 2.82e-05 | 0.8667 | 0.002495 | -0.1342 | 0.04583 |
| IL6ST | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.7572 | 4.506e-05 | 0.85 | 0.003705 | -0.1349 | 0.2923 |
| ICAM1 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.7549 | 4.893e-05 | 0.7667 | 0.01594 | -0.03831 | 0.6273 |
| NFKBIA | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.7459 | 6.743e-05 | 0.65 | 0.05807 | -0.07419 | 0.3984 |
| SCARB2 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.7425 | 7.579e-05 | 0.9167 | 0.0005066 | -0.1053 | 0.2003 |
| C2 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | c15_mocci_costate | 0.8951 | 8.367e-05 | 0.8286 | 0.04156 | 0.786 | 0.002658 |
| CSF3 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | c15_mocci_costate | 0.8951 | 8.367e-05 | 0.6 | 0.208 | 1.119 | 0.01186 |
| TNFRSF1A | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.7357 | 9.526e-05 | 0.4333 | 0.244 | -0.06342 | 0.5014 |
| HIF1A | ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | colon stromal | c15_mocci_costate | 0.8881 | 0.0001141 | 0.6 | 0.208 | 0.9017 | 0.01448 |
| CALR | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | inflammatory_nfkb | 0.8881 | 0.0001141 | 0.3143 | 0.5441 | 0.4587 | 0.0006908 |
| SLC15A4 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.7256 | 0.0001326 | 0.9333 | 0.0002359 | -0.07964 | 0.1555 |
| ITGAV | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.7188 | 0.000164 | 0.8333 | 0.005266 | -0.05322 | 0.4964 |
| CD274 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 0.8792 | 0.0001651 | 0.7714 | 0.0724 | 0.108 | 0.02147 |
| TNFSF10 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.7154 | 0.000182 | 0.6 | 0.08762 | -0.1131 | 0.2735 |
| UNC93B1 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.7132 | 0.0001949 | 0.7167 | 0.02982 | -0.03624 | 0.3262 |
| CCL20 | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 0.8671 | 0.0002598 | 0.3714 | 0.4685 | 0.4293 | 0.0006192 |
| TRAF3 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.703 | 0.0002633 | 0.9 | 0.0009431 | 0.003036 | 0.9505 |
| CFB | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 0.8601 | 0.0003317 | 0.6 | 0.208 | 0.4061 | 0.007118 |
| TYRO3 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lipid_loader_repair | 0.6928 | 0.0003515 | 0.7667 | 0.01594 | -0.05499 | 0.1479 |
| CIITA | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.6917 | 0.0003627 | 0.95 | 8.763e-05 | -0.1001 | 0.1082 |
| HIF1A | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.6917 | 0.0003627 | 0.8 | 0.009628 | -0.04239 | 0.5957 |
| NPC1 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.6872 | 0.0004107 | 0.85 | 0.003705 | -0.0419 | 0.4499 |
| CXCL8 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | c15_mocci_costate | 0.8531 | 0.0004181 | 0.4857 | 0.3287 | 0.5515 | 0.001134 |
| MMP9 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | inflammatory_nfkb | 0.8491 | 0.0004752 | 0.6 | 0.208 | 1.058 | 0.03887 |
| HIF1A | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | inflammatory_nfkb | 0.8462 | 0.0005211 | 0.8857 | 0.01885 | 1.119 | 0.0006121 |
| CSF3 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | inflammatory_nfkb | 0.8462 | 0.0005211 | 0.6571 | 0.1562 | 1.119 | 0.01186 |
| SERPINE1 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.677 | 0.000539 | 0.75 | 0.01994 | -0.05505 | 0.2921 |
| JAK1 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.6725 | 0.0006062 | 0.95 | 8.763e-05 | -0.08221 | 0.4799 |
| OSMR | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.6725 | 0.0006062 | 0.9 | 0.0009431 | -0.08976 | 0.2785 |
| TRAF6 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.6714 | 0.0006241 | 0.8667 | 0.002495 | -0.02966 | 0.5391 |
| NPC1 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lipid_loader_repair | 0.668 | 0.0006804 | 0.7833 | 0.01252 | -0.0419 | 0.4499 |
| PDCD1LG2 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.6676 | 0.000687 | 0.3333 | 0.3807 | -0.09071 | 0.08725 |
| CHUK | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.6646 | 0.0007411 | 0.8667 | 0.002495 | -0.004953 | 0.9178 |
| TGFB2 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lipid_loader_repair | 0.6635 | 0.0007624 | 0.7 | 0.03577 | -0.1019 | 0.03691 |
| CXCL11 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | inflammatory_nfkb | 0.8322 | 0.0007854 | 0.7714 | 0.0724 | 0.6876 | 0.05194 |
| ITGAV | ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | colon stromal | c15_mocci_costate | 0.8322 | 0.0007854 | 0.6571 | 0.1562 | 0.3994 | 0.001043 |
| IL1B | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 0.8322 | 0.0007854 | 0.5429 | 0.2657 | 0.4307 | 0.04628 |
| CD40 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.6589 | 0.0008526 | 0.5 | 0.1705 | -0.009363 | 0.9013 |
| STAT3 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lipid_loader_repair | 0.6589 | 0.0008526 | 0.8667 | 0.002495 | -0.1129 | 0.3329 |
| TNFSF10 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lipid_loader_repair | 0.6556 | 0.0009261 | 0.5 | 0.1705 | -0.1131 | 0.2735 |
| CALR | ibd_crohn_stromal | ibd_crohn_myeloid | Crohn disease | colon stromal | c15_mocci_costate | 0.8252 | 0.0009514 | 0.8857 | 0.01885 | 0.3542 | 0.01297 |
| CXCL8 | ibd_uc_epithelial | ibd_uc_myeloid | ulcerative colitis | colon epithelial | c15_mocci_costate | 0.8252 | 0.0009514 | 0.02857 | 0.9572 | 0.4919 | 0.01945 |
| MERTK | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.6533 | 0.000978 | 0.9 | 0.0009431 | -0.03338 | 0.3608 |
| IFNGR1 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.6522 | 0.001005 | 0.7833 | 0.01252 | -0.111 | 0.219 |
| S100A12 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | lipid_loader_repair | 0.819 | 0.001119 | 0.8827 | 0.01982 | 0.1643 | 0.3045 |
| NFKB1 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lipid_loader_repair | 0.6465 | 0.001149 | 0.8667 | 0.002495 | -0.09238 | 0.2129 |
| TGFB2 | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.6454 | 0.00118 | 0.65 | 0.05807 | -0.1019 | 0.03691 |
| S100A12 | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | c15_mocci_costate | 0.8115 | 0.001352 | 0.8827 | 0.01982 | 0.1643 | 0.3045 |
| HIF1A | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 0.8112 | 0.001363 | 0.3714 | 0.4685 | 0.3602 | 0.001913 |
| HIF1A | ibd_uc_stromal | ibd_uc_myeloid | ulcerative colitis | colon stromal | lysosomal_apc | 0.8112 | 0.001363 | 0.4286 | 0.3965 | 1.119 | 0.0006121 |
| CHUK | ibd_crohn_epithelial | ibd_crohn_myeloid | Crohn disease | colon epithelial | c15_mocci_costate | 0.8112 | 0.001363 | 0.4857 | 0.3287 | 0.1247 | 0.0002063 |
| CALR | sjogren_gland_stromal | sjogren_gland_apc | Sjogren syndrome | salivary gland stromal/endothelial | lysosomal_apc | 0.6375 | 0.001416 | 0.85 | 0.003705 | -0.06906 | 0.5122 |

## Interpretation

- A top bridge hit needs disease-up sender expression and same-donor
  myeloid module association across multiple autoimmune tissues.
- Links that are not disease-up may still be useful biology, but they
  are not intervention-ready because they can reflect tissue composition
  or compensatory repair.
- Wave30 prior-risk flags are carried forward; prior-blocked canonical
  axes should not be promoted without a narrow new therapeutic delta.

## Run Log

| analysis | status | sender_rows | genes_present |
| --- | --- | --- | --- |
| ibd_crohn_myeloid | completed | 2016 | 168 |
| ibd_uc_myeloid | completed | 2016 | 168 |
| ibd_crohn_epithelial | completed | 2016 | 168 |
| ibd_uc_epithelial | completed | 2016 | 168 |
| ibd_crohn_stromal | completed | 2016 | 168 |
| ibd_uc_stromal | completed | 2016 | 168 |
| psoriasis_skin_apc | completed | 912 | 152 |
| psoriasis_keratinocyte | completed | 912 | 152 |
| psoriasis_skin_stromal | completed | 912 | 152 |
| sjogren_gland_apc | completed | 3696 | 168 |
| sjogren_gland_epithelial | completed | 4200 | 168 |
| sjogren_gland_stromal | completed | 4032 | 168 |
| ra_blood_myeloid | completed | 5796 | 161 |
| t1d_beta_cell | completed | 3652 | 166 |
| t1d_ductal_cell | completed | 3984 | 166 |
| t1d_acinar_cell | completed | 3818 | 166 |
| t1d_stellate_cell | completed | 3486 | 166 |
| t1d_endothelial_cell | completed | 3652 | 166 |

## Reproducibility

- Script: `scripts/v3_wave103_sender_to_myeloid_bridge_scan.py`
- Sender scores: `results_v3/wave103_sender_to_myeloid_bridge_scan/sender_gene_scores.tsv`
- Raw contrasts: `results_v3/wave103_sender_to_myeloid_bridge_scan/sender_raw_contrasts.tsv`
- Bridge links: `results_v3/wave103_sender_to_myeloid_bridge_scan/sender_to_myeloid_bridge_links.tsv`
- Summary: `results_v3/wave103_sender_to_myeloid_bridge_scan/sender_bridge_gene_summary.tsv`
- Seed: `20260527`
