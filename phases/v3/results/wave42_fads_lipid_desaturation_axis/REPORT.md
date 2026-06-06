# Wave42 FADS Lipid-Desaturation Axis

## Result

FADS1/FADS2 remains mechanistically interesting as a lipid-genetic hypothesis, but Wave42 does not promote it. The autoimmune evidence is locus-level rather than target-level, risk-allele direction is not resolved, local cell-state evidence is weak and non-MS, and no LINCS FADS perturbagen is available to validate module reversal. FADS1 chemistry exists, so the route is parked only for future coloc/MR and perturbation work.

## Failed Gates

- target_level_colocalization_or_mr_direction_absent
- GWAS_Catalog_signal_is_11q12_locus_level_with_TMEM258_MYRF_FEN1_ambiguity
- local_cell_state_support_weak_and_not_lipid_lysosomal_myeloid_specific
- no_LINCS_FADS1_or_FADS2_perturbagen_present_for_signature_validation
- intervention_direction_unresolved_from_risk_alleles

## Local Wave34 Rows

| gene | wave34_call | wave34_score | gwas_catalog_trait_count | local_positive_disease_count | residual_retained_disease_count | druggable_activity_count | chembl_target_id | chembl_pref_name | chembl_best_nM | failed_gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FADS1 | PARK_GENETIC_DRUGGABLE_NEEDS_CELL_STATE | 19.5 | 9 | 2.0 | 0.0 | 61.0 | CHEMBL5840 | Acyl-CoA (8-3)-desaturase | 0.52 | gate_local_cell_state;gate_perturbation_or_model |
| FADS2 | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY | 18.0 | 10 | 2.0 | 0.0 | 0.0 | CHEMBL6097 | Acyl-CoA 6-desaturase |  | gate_local_cell_state;gate_druggable_surface;gate_perturbation_or_model |
| FADS3 | NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY | 1.2 | 1 | 0.0 | 0.0 | 0.0 |  |  |  | gate_genetic_breadth;gate_local_cell_state;gate_druggable_surface;gate_perturbation_or_model |

## GWAS Locus Ambiguity

Autoimmune FADS-locus rows: 39; distinct traits: 18; rows naming FADS genes: 27; rows also naming non-FADS locus genes: 15.

| MAPPED_GENE | n_rows | n_traits | min_p |
| --- | --- | --- | --- |
| FADS2, FADS1 | 11 | 9 | 8e-16 |
| FADS1, FADS2 | 7 | 2 | 3e-13 |
| TMEM258, MYRF | 7 | 5 | 2e-12 |
| FADS2 | 5 | 4 | 2e-16 |
| FEN1, FADS2 | 2 | 2 | 2e-15 |
| MYRF, TMEM258 | 2 | 2 | 4e-08 |
| POU2AF3 - MIR4491 | 1 | 1 | 2e-11 |
| TMEM258 | 1 | 1 | 2e-11 |
| FADS1, FADS2, MIR1908 | 1 | 1 | 3e-09 |
| MYRF | 1 | 1 | 2e-08 |
| PRANCR, MYRFL | 1 | 1 | 8e-07 |

## Local Cell-State Evidence

| gene | positive_disease_count | positive_diseases | best_positive_p | best_positive_fdr | top_positive_compartments | ms_wm_delta_log2 | ms_wm_p | ms_wm_fdr | in_lipid_lysosomal_myeloid_neighborhood |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FADS2 | 2 | Crohn disease;ulcerative colitis | 0.0006770173460368 | 0.0789352505154614 | ibd_crohn_epithelial:2.65,p=0.00068;ibd_uc_stromal:1.19,p=0.0093;ibd_uc_epithelial:2.21,p=0.048 | -1.511731792716413 | 0.1303764679615833 | 0.8989378106274888 | False |
| FADS1 | 2 | psoriasis;ulcerative colitis | 0.006434480633229 | 0.1829280880022899 | ibd_uc_stromal:1.09,p=0.0064;psoriasis_skin_stromal:1.44,p=0.03 | -0.5582998002248747 | 0.0302817182679143 | 0.8506970233122761 | False |
| FADS3 | 0 |  |  |  |  | -0.4647765054188522 | 0.2561536269226456 | 0.9037679420388188 | False |

## ChEMBL Druggability

| gene | target_chembl_id | target_pref_name | target_type | organism | activity_total_count | returned_activity_rows | activity_values_nM_count | unique_molecules_returned | best_standard_nM | median_standard_nM | assay_type_counts | best_molecule_chembl_id | best_molecule_pref_name | best_assay_description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FADS1 | CHEMBL5840 | Acyl-CoA (8-3)-desaturase | SINGLE PROTEIN | Homo sapiens | 145 | 145 | 61 | 137 | 0.52 | 60.0 | {"B": 145} | CHEMBL4084502 |  | Inhibition of D5D in human HepG2 cells assessed as [14C]AA formation from [14C]DGLA preincubated for 30 mins followed by [14C]eicosatrienoic acid addition measured after 3 hrs by TLC analysis |
| FADS2 | CHEMBL6097 | Acyl-CoA 6-desaturase | SINGLE PROTEIN | Homo sapiens | 104 | 104 | 11 | 101 | 407.65 | 80000.0 | {"B": 104} | CHEMBL5653589 |  | Binding affinity to human FADS2 incubated for 45 mins by Kinobead based pull down assay |

## Perturbation Availability

LINCS FADS1/FADS2 perturbagen rows found by exact target/MOA search: 0.

## Model Scope

The lipid-flux model is assumption-explicit and not fitted to patient or biochemical data. It is only a sanity check that FADS1 inhibition lacks an obvious disease-selective window without genotype or lipidomic stratification.

