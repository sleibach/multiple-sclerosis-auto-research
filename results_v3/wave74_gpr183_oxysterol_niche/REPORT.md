# Wave74-B GPR183/EBI2 Oxysterol-Niche Re-Evaluation

## Question

Does local cell-state evidence support a coherent `CH25H/CYP7B1/HSD3B7/CYP27A1` ligand-production program coupled to direct `GPR183` receptor and migration/myeloid response biology in autoimmune tissues?

## Verdict

PARK_GPR183_OXYSTEROL_NICHE

Promotion required cross-disease cell-state replication, disease-specific response or genetics support, and a direct `GPR183` receptor/intervention anchor. `EBI3` was not used as receptor support because it is not EBI2/GPR183.

## Integrated Decision

| candidate | wave74b_call | gate_count | local_coherent_program_cross_disease | ligand_module_cross_disease | direct_gpr183_receptor_anchor | response_module_cross_disease | specificity_vs_ifn_apc_generic | ms_support | ibd_response_support | ra_response_support | oxysterol_like_metabolite_support | target_resolved_genetics_or_druggability | coherent_program_disease_count | coherent_program_diseases | ligand_positive_diseases | gpr183_positive_diseases | best_coherent_context | wave66_oxysterol_supportive_diseases | wave62_gpr183_call | wave62_gpr183_score | decision_blockers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPR183_EBI2_oxysterol_niche | PARK_GPR183_OXYSTEROL_NICHE | 5 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  | type 1 diabetes mellitus | Crohn disease;Sjogren syndrome;ulcerative colitis |  |  | NO_GO_WAVE62_TARGET_RESOLUTION | 1.240930199623108 | no cross-disease coherent ligand-plus-GPR183-plus-response context; no local target-resolved genetics or direct intervention/druggability anchor; Wave66 oxysterol-like metabolites remain sparse |

## Module Definitions

| module | module_class | genes | n_genes | rationale | used_for_promotion | ebi3_handling |
| --- | --- | --- | --- | --- | --- | --- |
| ligand_production_core | ligand_production | CH25H;CYP7B1;HSD3B7;CYP27A1 | 4 | Enzymes capable of producing or processing GPR183-relevant oxysterol ligands and sterol intermediates. | True |  |
| gpr183_receptor_anchor | receptor_anchor | GPR183 | 1 | Direct EBI2 receptor anchor; promotion requires this signal, not only ligand enzymes. | True |  |
| lymphoid_trafficking_response | receptor_response | GPR183;CCR7;CCL19;CCL21;CXCL13;CXCR5;LTA;LTB | 8 | Migration and ectopic-lymphoid/niche genes expected to co-occur with a GPR183 trafficking axis. | True |  |
| myeloid_apc_migration_response | receptor_response | GPR183;CCR7;CCL19;CD83;LAMP3;ITGAX;CCL17;CCL22 | 8 | Myeloid/DC activation and migration state that could host a local oxysterol-guided niche. | True |  |
| ifn_apc_comparator | specificity_comparator | STAT1;IRF1;CXCL10;ISG15;GBP1;IFI30;HLA-DRA;CD74 | 8 | Interferon/APC comparator; GPR183 support should not be reducible to this axis. | False |  |
| generic_inflammation_comparator | specificity_comparator | TNF;IL1B;IL6;CXCL8;CCL2;CCL3;CCL4;NFKBIA;TNFAIP3 | 9 | Generic inflammatory comparator. | False |  |
| apc_lysosome_comparator | specificity_comparator | CD74;HLA-DRA;HLA-DRB1;HLA-DPA1;HLA-DPB1;IFI30;CTSS;LAMP1;LAMP2 | 9 | APC/lysosome comparator. | False |  |
| ebi3_nomenclature_control | negative_nomenclature_control | EBI3 | 1 | EBI3 is not EBI2/GPR183; it is tracked only to avoid alias-driven false support. | False | excluded_from_GPR183_receptor_program |

## Broad h5ad Summary

| module | module_class | tested_context_count | positive_context_count | negative_context_count | positive_fdr10_context_count | positive_disease_count | negative_disease_count | positive_diseases | negative_diseases | best_positive_context | best_negative_context |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ligand_production_core | ligand_production | 15 | 4 | 0 | 3 | 1 | 0 | type 1 diabetes mellitus |  | t1d_endothelial_cell\|type 1 diabetes mellitus\|pancreatic endothelial cell\|effect=1.4\|p=0.00184\|fdr=0.00736 |  |
| gpr183_receptor_anchor | receptor_anchor | 17 | 3 | 1 | 1 | 3 | 1 | Crohn disease;Sjogren syndrome;ulcerative colitis | psoriasis | ibd_crohn_epithelial\|Crohn disease\|colon epithelial\|effect=1.13\|p=0.0323\|fdr=0.0811 | psoriasis_skin_apc\|psoriasis\|skin APC\|effect=-1.25\|p=0.0496\|fdr=0.111 |
| lymphoid_trafficking_response | receptor_response | 17 | 9 | 0 | 8 | 4 | 0 | Crohn disease;Sjogren syndrome;type 1 diabetes mellitus;ulcerative colitis |  | ibd_crohn_myeloid\|Crohn disease\|colon myeloid\|effect=2.8\|p=8.21e-08\|fdr=2.1e-06 |  |
| myeloid_apc_migration_response | receptor_response | 17 | 6 | 1 | 6 | 4 | 1 | Crohn disease;Sjogren syndrome;type 1 diabetes mellitus;ulcerative colitis | ulcerative colitis | ibd_crohn_myeloid\|Crohn disease\|colon myeloid\|effect=2.52\|p=5.32e-09\|fdr=6.81e-07 | ibd_uc_epithelial\|ulcerative colitis\|colon epithelial\|effect=-0.373\|p=0.0588\|fdr=0.13 |
| ifn_apc_comparator | specificity_comparator | 17 | 14 | 0 | 13 | 5 | 0 | Crohn disease;Sjogren syndrome;psoriasis;type 1 diabetes mellitus;ulcerative colitis |  | t1d_beta_cell\|type 1 diabetes mellitus\|pancreatic beta cell\|effect=1.8\|p=0.000179\|fdr=0.00109 |  |
| generic_inflammation_comparator | specificity_comparator | 17 | 11 | 2 | 11 | 3 | 1 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | psoriasis | ibd_uc_myeloid\|ulcerative colitis\|colon myeloid\|effect=1.64\|p=3.42e-05\|fdr=0.000365 | psoriasis_skin_apc\|psoriasis\|skin APC\|effect=-1.19\|p=0.0055\|fdr=0.019 |
| apc_lysosome_comparator | specificity_comparator | 17 | 9 | 0 | 9 | 5 | 0 | Crohn disease;Sjogren syndrome;psoriasis;type 1 diabetes mellitus;ulcerative colitis |  | ibd_uc_epithelial\|ulcerative colitis\|colon epithelial\|effect=1.89\|p=0.00011\|fdr=0.00078 |  |
| ebi3_nomenclature_control | negative_nomenclature_control | 11 | 1 | 0 | 0 | 1 | 0 | ulcerative colitis |  | ibd_uc_myeloid\|ulcerative colitis\|colon myeloid\|effect=0.892\|p=0.0878\|fdr=0.18 |  |

## Coherent Cell-State Contexts

| analysis | disease_name | compartment | role | ligand_effect | ligand_p | gpr183_effect | gpr183_p | lymphoid_response_effect | myeloid_response_effect | best_response_effect | best_response_p | ligand_pass | gpr183_anchor_pass | response_pass | coherent_program_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t1d_endothelial_cell | type 1 diabetes mellitus | pancreatic endothelial cell | tissue_resident | 1.4031780493963935 | 0.0018405488245703207 | 0.6952280183326858 | 0.5694688335435334 | 0.47134163268480284 | 0.996654254620986 | 0.996654254620986 | 0.026530735137177807 | True | False | True | False |
| t1d_stellate_cell | type 1 diabetes mellitus | pancreatic stellate cell | tissue_resident | 0.8714948404706867 | 0.09391996650141991 | 1.0447685424676991 | 0.31320431044433705 | 1.666758428928695 | 1.5212865357101109 | 1.666758428928695 | 0.0033572778282159833 | True | False | True | False |
| t1d_ductal_cell | type 1 diabetes mellitus | pancreatic ductal cell | tissue_resident | 0.43607164499379997 | 0.035264175909388566 | 0.174490272584245 | 0.4518700712563468 | 0.5281550697259652 | 0.20483483644838377 | 0.5281550697259652 | 0.08986014336886551 | True | False | True | False |
| t1d_acinar_cell | type 1 diabetes mellitus | pancreatic acinar cell | tissue_resident | 0.4264817049510337 | 0.035671340690226455 | -0.1082652916562196 | 0.8173308974440575 | 0.37628515328786416 | -0.14099671225290059 | 0.37628515328786416 | 0.6317460097792859 | True | False | False | False |
| sjogren_gland_stromal | Sjogren syndrome | salivary gland stromal/endothelial | tissue_resident | 0.3649463556598834 | 0.18835218058500913 | 0.4374128207154784 | 0.3669730803744491 | 0.5297871981456873 | 0.2679876616242349 | 0.5297871981456873 | 0.003553965309566657 | True | False | True | False |
| ibd_crohn_stromal | Crohn disease | colon stromal | tissue_resident | 0.29383828047870886 | 0.6098865278849033 | 0.6731743726654338 | 0.24136452213284187 | 0.8614916703072111 | 0.017731347614062212 | 0.8614916703072111 | 0.09511340563430085 | False | False | True | False |
| psoriasis_keratinocyte | psoriasis | skin keratinocyte | tissue_resident | 0.28621966983641256 | 0.18692690886041696 | -0.6470595637869949 | 0.3445086431728491 | 0.00246680875362702 | 0.17530876637701656 | 0.17530876637701656 | 0.16804330313307414 | True | False | False | False |
| ibd_crohn_myeloid | Crohn disease | colon myeloid | myeloid_apc | 0.23452243275661966 | 0.48100291834929787 | 0.975302839797214 | 0.14133886917618182 | 2.8046547137624556 | 2.5166383272467368 | 2.8046547137624556 | 5.320992591828428e-09 | False | True | True | False |
| ibd_uc_myeloid | ulcerative colitis | colon myeloid | myeloid_apc | 0.06017636325505206 | 0.9205752233676625 | 1.0385480940916807 | 0.09693210316192737 | 2.3213772661445233 | 2.466632101351478 | 2.466632101351478 | 1.9824962091908655e-08 | False | True | True | False |
| t1d_beta_cell | type 1 diabetes mellitus | pancreatic beta cell | tissue_resident | 0.03583016674550492 | 0.32641390622509925 | 0.7168551823734177 | 0.5778244446088122 | 1.2113059650733597 | 0.590984888312716 | 1.2113059650733597 | 0.022598337245701143 | False | False | True | False |
| ibd_uc_stromal | ulcerative colitis | colon stromal | tissue_resident | 0.019006504747335437 | 0.9417312379281083 | 0.4366689388990394 | 0.4133182608369611 | 0.9797626305949819 | 0.5130185044965384 | 0.9797626305949819 | 0.2359921311252784 | False | False | False | False |
| psoriasis_skin_apc | psoriasis | skin APC | myeloid_apc | -0.013294453612385702 | 0.6235325604588697 | -1.2498901037911736 | 0.04960820400152706 | -0.27439277131225565 | 0.030975258602004146 | 0.030975258602004146 | 0.6222166932721391 | False | False | False | False |

## Specificity Versus IFN/APC And Generic Inflammation

| analysis | disease_name | compartment | role | target_module | target_effect | max_specificity_comparator_effect | specificity_margin | specificity_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ibd_crohn_myeloid | Crohn disease | colon myeloid | myeloid_apc | lymphoid_trafficking_response | 2.8046547137624556 | 1.630948999020061 | 1.1737057147423946 | True |
| ibd_crohn_myeloid | Crohn disease | colon myeloid | myeloid_apc | myeloid_apc_migration_response | 2.5166383272467368 | 1.630948999020061 | 0.8856893282266758 | True |
| ibd_uc_myeloid | ulcerative colitis | colon myeloid | myeloid_apc | myeloid_apc_migration_response | 2.466632101351478 | 1.6406067611682977 | 0.8260253401831803 | True |
| ibd_uc_myeloid | ulcerative colitis | colon myeloid | myeloid_apc | lymphoid_trafficking_response | 2.3213772661445233 | 1.6406067611682977 | 0.6807705049762256 | True |
| sjogren_gland_stromal | Sjogren syndrome | salivary gland stromal/endothelial | tissue_resident | lymphoid_trafficking_response | 0.5297871981456873 | 0.26256496672442436 | 0.26722223142126295 | True |
| sjogren_gland_apc | Sjogren syndrome | salivary gland APC | myeloid_apc | lymphoid_trafficking_response | 0.7796797951445484 | 0.5642974540017329 | 0.21538234114281551 | True |
| t1d_stellate_cell | type 1 diabetes mellitus | pancreatic stellate cell | tissue_resident | lymphoid_trafficking_response | 1.666758428928695 | 1.4706295036643893 | 0.1961289252643057 | False |
| sjogren_gland_stromal | Sjogren syndrome | salivary gland stromal/endothelial | tissue_resident | gpr183_receptor_anchor | 0.4374128207154784 | 0.26256496672442436 | 0.17484785399105401 | False |
| ibd_uc_stromal | ulcerative colitis | colon stromal | tissue_resident | lymphoid_trafficking_response | 0.9797626305949819 | 0.8598656130854461 | 0.11989701750953585 | False |
| sjogren_gland_apc | Sjogren syndrome | salivary gland APC | myeloid_apc | myeloid_apc_migration_response | 0.6634828174374192 | 0.5642974540017329 | 0.09918536343568629 | False |
| t1d_stellate_cell | type 1 diabetes mellitus | pancreatic stellate cell | tissue_resident | myeloid_apc_migration_response | 1.5212865357101109 | 1.4706295036643893 | 0.050657032045721584 | False |
| sjogren_gland_stromal | Sjogren syndrome | salivary gland stromal/endothelial | tissue_resident | myeloid_apc_migration_response | 0.2679876616242349 | 0.26256496672442436 | 0.0054226948998105096 | False |

## MS GSE111972 Module Tests

| dataset | module | module_class | n_genes_present | genes_present | mean_effect | median_effect | combined_z | combined_p | fdr | positive_nominal | negative_nominal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE111972_MS_white_matter_microglia | ligand_production_core | ligand_production | 4 | CH25H;CYP27A1;CYP7B1;HSD3B7 | 0.07109881866522438 | 0.35324435052222114 | 1.156609634173048 | 0.24743188433124397 | 0.49486376866248794 | False | False |
| GSE111972_MS_white_matter_microglia | gpr183_receptor_anchor | receptor_anchor | 1 | GPR183 | -0.1364089401905186 | -0.1364089401905186 | -0.4347895737299986 | 0.6637151735644201 | 0.7437452561398225 | False | False |
| GSE111972_MS_white_matter_microglia | lymphoid_trafficking_response | receptor_response | 6 | CCL19;CCR7;CXCR5;GPR183;LTA;LTB | -0.2224636011286528 | -0.03468753318829165 | -0.48923523541957453 | 0.6246751665297153 | 0.7437452561398225 | False | False |
| GSE111972_MS_white_matter_microglia | myeloid_apc_migration_response | receptor_response | 8 | CCL17;CCL19;CCL22;CCR7;CD83;GPR183;ITGAX;LAMP3 | 0.08567786398728658 | 0.047768310823417204 | 0.689065343618554 | 0.4907821479438752 | 0.7437452561398225 | False | False |
| GSE111972_MS_white_matter_microglia | ifn_apc_comparator | specificity_comparator | 8 | CD74;CXCL10;GBP1;HLA-DRA;IFI30;IRF1;ISG15;STAT1 | 0.3368345248637704 | 0.27226116990233695 | 2.9461774627273583 | 0.003217277579396275 | 0.0128691103175851 | True | False |
| GSE111972_MS_white_matter_microglia | generic_inflammation_comparator | specificity_comparator | 9 | CCL2;CCL3;CCL4;CXCL8;IL1B;IL6;NFKBIA;TNF;TNFAIP3 | 0.029776291321779565 | 0.0490525604706171 | 0.32689770608288354 | 0.7437452561398225 | 0.7437452561398225 | False | False |
| GSE111972_MS_white_matter_microglia | apc_lysosome_comparator | specificity_comparator | 9 | CD74;CTSS;HLA-DPA1;HLA-DPB1;HLA-DRA;HLA-DRB1;IFI30;LAMP1;LAMP2 | 0.3165849979697071 | 0.2553907019006836 | 4.621437532617576 | 3.8109008785158988e-06 | 3.048720702812719e-05 | True | False |
| GSE111972_MS_white_matter_microglia | ebi3_nomenclature_control | negative_nomenclature_control | 1 | EBI3 | -0.6870150191586522 | -0.6870150191586522 | -2.5500747960534196 | 0.0107699810281324 | 0.028719949408353068 | False | True |

## IBD GSE282122 Treatment-Response Tests

| dataset | test | cell_state | module | module_class | n_genes_present | genes_present | mean_effect | median_effect | combined_z | combined_p | normalizing_response_support | fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE282122 | post_treatment_delta_remission_minus_nonremission | Mono_macro | ligand_production_core | ligand_production | 4 | CH25H;CYP27A1;CYP7B1;HSD3B7 | -1.2834471486454841 | -1.3435090430969157 | -4.428196112677193 | 9.50244822686173e-06 | True | 0.0003040783432595754 |
| GSE282122 | post_treatment_delta_remission_minus_nonremission | DC | myeloid_apc_migration_response | receptor_response | 8 | CCL17;CCL19;CCL22;CCR7;CD83;GPR183;ITGAX;LAMP3 | -1.1804340925332133 | -0.9121615541026368 | -3.5712083215484873 | 0.0003553381193480835 | True | 0.0022741639638277347 |
| GSE282122 | post_treatment_delta_remission_minus_nonremission | DC | lymphoid_trafficking_response | receptor_response | 8 | CCL19;CCL21;CCR7;CXCL13;CXCR5;GPR183;LTA;LTB | -0.6218376876882673 | -0.5272080487313994 | -2.768486256781907 | 0.005631736079362636 | True | 0.020023950504400485 |
| GSE282122 | post_treatment_delta_remission_minus_nonremission | DC | ligand_production_core | ligand_production | 4 | CH25H;CYP27A1;CYP7B1;HSD3B7 | -0.5851643448411379 | -0.4429190886580796 | -2.0077578371865745 | 0.04466903125403556 | True | 0.11911741667742816 |
| GSE282122 | post_treatment_delta_remission_minus_nonremission | DC | gpr183_receptor_anchor | receptor_anchor | 1 | GPR183 | -0.5048554153398023 | -0.5048554153398023 | -1.7374982424149927 | 0.08229926398314552 | True | 0.19599040698002448 |
| GSE282122 | post_treatment_delta_remission_minus_nonremission | Mono_macro | myeloid_apc_migration_response | receptor_response | 8 | CCL17;CCL19;CCL22;CCR7;CD83;GPR183;ITGAX;LAMP3 | -0.3575053187996197 | -0.2065851547519817 | -1.71827864250789 | 0.08574580305376071 | True | 0.19599040698002448 |
| GSE282122 | post_treatment_delta_remission_minus_nonremission | Mono_macro | lymphoid_trafficking_response | receptor_response | 8 | CCL19;CCL21;CCR7;CXCL13;CXCR5;GPR183;LTA;LTB | -0.1367736790935108 | -0.2408792600035637 | -1.641196151400655 | 0.10075670437064689 | False | 0.21494763599071337 |
| GSE282122 | paired_post_minus_pre_all | DC | myeloid_apc_migration_response | receptor_response | 8 | CCL17;CCL19;CCL22;CCR7;CD83;GPR183;ITGAX;LAMP3 | -0.27387139351471124 | -0.07215308235411685 | -1.2566165453314606 | 0.20889252062299846 | False | 0.3713644811075528 |
| GSE282122 | paired_post_minus_pre_all | Mono_macro | lymphoid_trafficking_response | receptor_response | 8 | CCL19;CCL21;CCR7;CXCL13;CXCR5;GPR183;LTA;LTB | -0.12592576803299496 | -0.06068154839148521 | -1.0957903017772845 | 0.2731705536123836 | False | 0.44445512616931 |
| GSE282122 | paired_post_minus_pre_all | Mono_macro | gpr183_receptor_anchor | receptor_anchor | 1 | GPR183 | 0.2259821042046697 | 0.2259821042046697 | 0.9975813172391294 | 0.3184824242366946 | False | 0.48530655121782035 |
| GSE282122 | paired_post_minus_pre_all | DC | gpr183_receptor_anchor | receptor_anchor | 1 | GPR183 | 0.1122794636919861 | 0.1122794636919861 | 0.9134388250582907 | 0.36101179390371685 | False | 0.5022772784747365 |
| GSE282122 | paired_post_minus_pre_all | Mono_macro | ligand_production_core | ligand_production | 4 | CH25H;CYP27A1;CYP7B1;HSD3B7 | -0.2798229337697145 | -0.19032104502282576 | -0.8602790039818896 | 0.38963526377857216 | False | 0.5113100259950514 |

## RA GSE198520 Anti-TNF Tests

| dataset | module | n_patients | mean_post_minus_pre | paired_t | paired_p | good_vs_other_delta | good_vs_other_p | modgood_vs_none_delta | modgood_vs_none_p | normalizing_response_support | paired_fdr | good_vs_other_fdr | modgood_vs_none_fdr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE198520_RA_synovium_antiTNF | lymphoid_trafficking_response | 46 | -0.2737830755897026 | -3.593863397029514 | 0.0008039962038260487 | -0.45643721503894785 | 0.0043527804642187135 | -0.2853231672961214 | 0.05542651535284156 | True | 0.006431969630608389 | 0.03482224371374971 | 0.11085303070568311 |
| GSE198520_RA_synovium_antiTNF | gpr183_receptor_anchor | 46 | 0.010138084943425375 | 0.09678024486567215 | 0.9233306669733227 | -0.46576691345757315 | 0.0485494399226586 | -0.22768959774251007 | 0.23358116137844032 | True | 0.9233306669733227 | 0.17970043434381683 | 0.3160388757542909 |
| GSE198520_RA_synovium_antiTNF | myeloid_apc_migration_response | 46 | -0.2215472901020175 | -2.4963624724868745 | 0.01627751308648525 | -0.21776134729692495 | 0.28513999682924546 | 0.023922939970538237 | 0.8776145868139613 | False | 0.0325550261729705 | 0.32587428209056624 | 0.8776145868139613 |
| GSE198520_RA_synovium_antiTNF | ligand_production_core | 46 | -0.008977074982024486 | -0.14501445508639965 | 0.885347036606907 | -0.08665424312611182 | 0.5357018575048467 | 0.13579891843169156 | 0.23702915681571818 | False | 0.9233306669733227 | 0.5357018575048467 | 0.3160388757542909 |

## Wave66 Oxysterol-Like Metabolite Support

| oxysterol_like_feature_rows | supportive_feature_rows | supportive_disease_count | supportive_diseases | best_supportive_feature |
| --- | --- | --- | --- | --- |
| 6 | 0 | 0 |  |  |

## Target-Level External Evidence

| gene | wave62_score | wave62_call | wave62_strong_l2g_disease_count | wave62_strong_l2g_diseases | wave62_relevant_qtl_coloc_disease_count | wave62_relevant_qtl_coloc_diseases | wave62_druggable_activity_count | wave62_chembl_target_id | wave57_geneformer_present | wave69d_geneformer_present | wave72_broad_positive_disease_count | wave72_broad_positive_diseases | wave72_gse282122_best_cell_state | wave72_gse282122_integrated_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPR183 | 1.240930199623108 | NO_GO_WAVE62_TARGET_RESOLUTION | 1.0 | Psoriasis | 0.0 |  | 0.0 |  | False | False | 2.0 | Crohn disease;Sjogren syndrome | DC | 2.147547758438998 |
| CH25H | 1.3178709745407104 | NO_GO_WAVE62_TARGET_RESOLUTION | 1.0 | UC | 0.0 |  | 0.0 |  | False | False |  |  |  |  |
| CYP7B1 |  |  |  |  |  |  |  |  | False | False |  |  |  |  |
| HSD3B7 | 1.3169242742527143 | NO_GO_WAVE62_TARGET_RESOLUTION | 0.0 |  | 1.0 | Psoriasis | 0.0 |  | False | False |  |  |  |  |
| CYP27A1 |  |  |  |  |  |  |  |  | False | False |  |  |  |  |

## Local Inputs

- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/raw_remission_response_gene_tests.tsv` and `results_v3/wave68_gse282122_unrestricted_gene_screen/paired_gene_delta_tests.tsv`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv` and `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
- `results_v3/wave66_metabolomics_class_convergence/feature_contrast_effects.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave57_intervention_first_geneformer_screen/wave57_geneformer_gene_summary.tsv` and `results_v3/wave69d_gse282122_geneformer_remission_centroid/geneformer_remission_gene_summary.tsv`
- `results_v3/wave72_lipid_mediator_intervention_scout/lipid_mediator_feature_matches.tsv` and `results_v3/wave72_lipid_mediator_intervention_scout/lipid_mediator_gene_evidence.tsv`
