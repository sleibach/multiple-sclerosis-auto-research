# Wave 82b cross-disease evidence stress test

Scope: DAB2, CD9, PARK7, PSAP, LYN, HEXA, HEXB, SP140, RGS14, STAT4. I treated row/table presence as non-evidence unless the row had positive support metrics. Source tables are local under `/Users/soeren.leibach/Projects/ms-auto-research`.

## Bottom line

No candidate cleanly passes as a cross-autoimmune therapeutic finding. The only candidates with real cross-autoimmune breadth in the local tables are genetics/colocalization-heavy or disease-state-heavy rather than intervention-ready:

- `STAT4`: strongest cross-autoimmune genetics/colocalization breadth, but blocked by wrong/no correct-direction modality and no positive foundation-model support.
- `SP140`: strong cross-autoimmune genetics/colocalization plus disease-state recurrence, but explicitly blocked as prior-art/chemistry-limited and lacks direct perturbation/foundation support.
- `RGS14`: genetics/colocalization spans Crohn/MS/Psoriasis, but local disease-state breadth is only Crohn and the integrated call says no cross-disease module.
- `LYN`: broad disease-state recurrence and a positive Geneformer direction row, but no genetics/target-resolution support and blocked as broad SRC-family comparator.
- `PARK7`: external genetics/proxy breadth and weak foundation support, but target resolution fails and local support is not MS/genetics anchored.
- `DAB2`, `CD9`, `PSAP`, `HEXA`, `HEXB`: do not show true cross-autoimmune breadth beyond isolated state/model/perturbation flags.

## Primary integrated gate

Source: `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`

| Gene | Integrated call | Direct perturbation | Foundation support | MS anchor | Genetics/target resolution | Broad positive disease count | IBD response FDR10 | Key blocker/stat |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| DAB2 | `PARK_PERTURBATION_FIRST_CANDIDATE` | 1 | 0 | 1 | 0 | 0 | 0 | `ms_delta_log2=0.5378984279794476`, `ms_p=0.0111306912319104`; critical MS/genetics/modality/direction gates fail |
| CD9 | `PARK_PERTURBATION_FIRST_CANDIDATE` | 1 | 0 | 1 | 0 | 0 | 0 | `ms_delta_log2=1.1100295973517351`, `ms_p=0.0019686305906988`; critical gates fail |
| PSAP | `PARK_PERTURBATION_FIRST_CANDIDATE` | 0 | 1 | 1 | 0 | 0 | 0 | `wave57:support=1,strong=0,token_contexts=6`; no breadth/genetics |
| LYN | `PARK_PERTURBATION_FIRST_CANDIDATE` | 0 | 1 | 0 | 0 | 3 | 0 | Broad positives: Crohn disease, psoriasis, ulcerative colitis; no genetics/MS anchor |
| HEXA | `PARK_PERTURBATION_FIRST_CANDIDATE` | 0 | 1 | 0 | 0 | 1 | 0 | Only Crohn disease broad positive |
| HEXB | `PARK_PERTURBATION_FIRST_CANDIDATE` | 0 | 1 | 0 | 0 | 0 | 0 | No broad positive disease |
| SP140 | `NO_GO_PERTURBATION_FIRST_BLOCKED` | 0 | 0 | 1 | 1 | 4 | 0 | Crohn/Sjogren/psoriasis/UC broad positives; `PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW`; closed prior branch |
| RGS14 | `NO_GO_PERTURBATION_FIRST_BLOCKED` | 0 | 0 | 1 | 1 | 1 | 0 | Only Crohn disease broad positive; `PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE` |
| STAT4 | `NO_GO_PERTURBATION_FIRST_BLOCKED` | 0 | 0 | 1 | 1 | 2 | 0 | Crohn/UC broad positives; generic JAK/STAT/Th1-Th17 TF axis |
| PARK7 | `NO_GO_PERTURBATION_FIRST_BLOCKED` | 0 | 1 | 0 | 1 | 2 | 0 | psoriasis/UC broad positives; `NO_GO_WAVE62_TARGET_RESOLUTION` |

## Genetics and colocalization

Sources:

- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_candidate_audit.tsv`
- `results_v3/wave34a_genetics_first_target_rescue/genetics_first_candidate_rank.tsv`

`STAT4` has the strongest genetic breadth: `max_l2g_score=0.8833943605422974`, `best_l2g_disease=RA`, `strong_l2g_disease_count=8` (`Celiac;Crohn;MS;PBC;RA;SLE;Sjogren;T1D`), `strong_qtl_coloc_disease_count=7` (`Celiac;Crohn;MS;PBC;RA;SLE;Sjogren`), `max_qtl_h4=0.9941264815984456`, `ms_max_qtl_h4=0.955404271318453`. Stress-test penalty: `wave62_call=PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW`, `wave34a_call=DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION`, `druggable_activity_count=0.0`, and `ms_wm_fdr=0.9239963547089984`.

`SP140` has real but narrower genetic breadth: `max_l2g_score=0.8754889965057373`, `best_l2g_disease=MS`, `strong_l2g_disease_count=3` (`Crohn;MS;Psoriasis`), `strong_qtl_coloc_disease_count=3` (`Crohn;MS;Psoriasis`), `myeloid_qtl_coloc_disease_count=3`, `max_qtl_h4=0.9891974580445424`, `ms_max_qtl_h4=0.9868116204726999`. Stress-test penalty: `wave62_call=PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW`, `druggable_activity_count=0.0`, `ms_wm_fdr=0.9677805697088556`, and the integrated blocker is a closed SP140 branch.

`RGS14` has target-resolution signal but not local cross-disease state breadth: `max_l2g_score=0.8030093312263489`, `best_l2g_disease=MS`, `strong_l2g_disease_count=3` (`Crohn;MS;Psoriasis`), `strong_qtl_coloc_disease_count=3`, `max_qtl_h4=0.9960433969675369`, `ms_max_qtl_h4=0.9952074420704351`. Stress-test penalty: `wave62_call=PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE`, `local_positive_disease_count=1.0` (`Crohn disease`), `ms_wm_fdr=0.8744776374054363`, no ChEMBL target/activity.

`PARK7` is a weak genetics/proxy case, not target resolved: `wave62_call=NO_GO_WAVE62_TARGET_RESOLUTION`, `max_l2g_score=0.12831711769104004`, `strong_l2g_disease_count=0`, `strong_qtl_coloc_disease_count=1` (`UC`), `ms_max_qtl_h4=0.0`. Wave55 lists `n_diseases_genetic_ge_0_25=5` (`AS;Crohn;Psoriasis;RA;UC`) but `ms_genetic_association=0.0` and `ms_overall_score=0.0`.

`DAB2`, `CD9`, `LYN`, `PSAP`, `HEXA`, `HEXB` have no positive genetics/target-resolution support in the integrated table (`genetics_or_target_resolution=0`). Wave55 rank rows exist for `LYN`, `PSAP`, and `CD9`, but their genetics counts are `0`, and table presence is not evidence.

## Single-cell/spatial disease-state recurrence

Source: `results_v3/wave81_perturbation_first_rescue/perturbation_first_broad_summary.tsv`

Positive disease-state breadth by table metric:

| Gene | Positive disease count | Positive diseases | Negative disease count | Best p | Max abs delta |
|---|---:|---|---:|---:|---:|
| SP140 | 4 | Crohn disease; Sjogren syndrome; psoriasis; ulcerative colitis | 0 | 0.0009903277300131 | 2.444937521428715 |
| LYN | 3 | Crohn disease; psoriasis; ulcerative colitis | 0 | 0.0014884442769417 | 2.4250122019920344 |
| STAT4 | 2 | Crohn disease; ulcerative colitis | 0 | 0.022492262445724 | 1.9152945697213184 |
| PARK7 | 2 | psoriasis; ulcerative colitis | 0 | 0.0112373384944221 | 0.8720188387053938 |
| HEXA | 1 | Crohn disease | 0 | 0.0120465998768706 | 0.9135122702261405 |
| RGS14 | 1 | Crohn disease | 0 | 0.0306688027655698 | 0.95141524887717 |
| DAB2 | 0 |  | 3 | 0.0026989827017581 | 2.616269136034033 |
| CD9 | 0 |  | 2 | 0.0029045418350274 | 1.3366874864716172 |
| HEXB | 0 |  | 2 | 0.0115601768822797 | 0.9020599603821812 |
| PSAP | 0 |  | 1 | 0.001848673240445 | 0.8687617781922139 |

Interpretation: SP140 and LYN have the clearest state-recurrence breadth; STAT4 and PARK7 are moderate; HEXA/RGS14 are single-disease only. DAB2/CD9/HEXB/PSAP are negative-direction or no-positive cases by this table.

## Treatment-response association

Sources:

- `results_v3/wave81_perturbation_first_rescue/perturbation_first_ibd_response_summary.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/adjusted_top_gene_ols.tsv`

No candidate has IBD treatment-response support at FDR10 in the summary table: every candidate has `ibd_response_fdr10=0`. Nominal-only rows should not be counted as robust cross-autoimmune breadth.

Best summary statistics:

| Gene | Nominal IBD response | FDR10 | Best raw p/FDR | Best paired p/FDR |
|---|---:|---:|---:|---:|
| STAT4 | 1 | 0 | 0.0015163184704909 / 0.5873562852590756 | 0.5808361587347401 / 1.0 |
| SP140 | 1 | 0 | 0.0152328403374826 / 0.7417124806231342 | 0.6397325281783008 / 1.0 |
| LYN | 1 | 0 | 0.0124701068861812 / 0.735902312729011 | 0.8536441932351698 / 1.0 |
| RGS14 | 1 | 0 | 0.0231153036723188 / 1.0 | 0.0287252207518441 / 1.0 |
| PARK7 | 1 | 0 | 0.6241174547054757 / 1.0 | 0.007300224821745 / 0.6155718115592173 |
| HEXA | 1 | 0 | 0.2452265677169609 / 1.0 | 0.0013822504255144 / 0.5416990453726748 |
| HEXB | 1 | 0 | 0.2747581303543149 / 1.0 | 0.0351922658670569 / 1.0 |
| DAB2 | 1 | 0 | 0.0836599691107984 / 1.0 | 0.047169838467308 / 1.0 |
| CD9 | 0 | 0 | 0.1780830366271985 / 1.0 | 0.1854140139866797 / 1.0 |
| PSAP | 0 | 0 | 0.355494913816343 / 1.0 | 0.3035476276872365 / 1.0 |

Adjusted OLS rows from `wave68` do show disease-response signals, but these are IBD-dataset signals, not cross-autoimmune breadth by themselves: `RGS14` DC `remission_adjusted_delta=1.872360653346221`, `p=0.0006732168657248546`, `fdr=0.011331376879442459`; `LYN` Mono_macro `delta=-0.6878028968421033`, `p=0.00016534662308785643`, `fdr=0.007837786068337288`; `SP140` Mono_macro `delta=-1.5082456826269486`, `p=0.030807388264140596`, `fdr=0.046867067896824384`; `STAT4` Mono_macro `delta=-2.7638924115452257`, `p=0.0001654893239718979`, `fdr=0.007837786068337288`.

## Foundation-model support

Sources:

- `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave57_rows.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave69d_rows.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave70c_rows.tsv`

Positive support metrics:

- `LYN`: `support_contexts=3`, `strong_support_contexts=1`, best context `GSE282122_DC_post_nonremission_to_remission`, `best_cosine_shift_z_vs_random=0.8605005174901813`, `best_projection_minus_random=0.0270023738376848`; also `opposing_contexts=1`. This is the best foundation-model support among the candidates, but it is blocked as a broad SRC-family comparator.
- `HEXA`: `support_contexts=1`, `strong_support_contexts=1`, best context `psoriasis_macrophage`, `best_cosine_shift_z_vs_random=0.8895572828571129`, `best_projection_minus_random=0.0376647322943124`. Single context only.
- `HEXB`: `support_contexts=1`, `strong_support_contexts=1`, best context `t1d_acinar`, `best_cosine_shift_z_vs_random=0.5882702689970096`, `best_projection_minus_random=0.0282737346682956`. Single context only.
- `PARK7`: `support_contexts=2`, `strong_support_contexts=0`, supporting contexts `IBD_myeloid;sjogren_APC`, best `best_cosine_shift_z_vs_random=0.4312510315284708`, `best_projection_minus_random=0.0110094174775037`. Weak support.
- `PSAP`: `support_contexts=1`, `strong_support_contexts=0`, best context `IBD_myeloid`, `best_cosine_shift_z_vs_random=0.0577827831532968`, `best_projection_minus_random=0.0206675017284902`. Weak support.

Negative/non-support rows:

- `STAT4`: wave57 and wave69d both have `support_contexts=0`, `strong_support_contexts=0`; wave69d best projection is negative (`-0.0172170472725863`).
- `SP140`: wave57 and wave69d both have `support_contexts=0`, `strong_support_contexts=0`; wave69d best projection is negative (`-0.0240805782151356`).
- `RGS14`: wave69d has `support_contexts=0`, `strong_support_contexts=0`.
- `DAB2`, `CD9`: no foundation table support in the integrated table (`foundation_table_presence=0`, `foundation_model_support=0`).

## Direct perturbation

Sources:

- `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave37_rows.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave15_rows.tsv`

`DAB2` and `CD9` have direct perturbation calls in the integrated table, but the support statistics are weak after adjustment. `DAB2` has `screen_call=KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR`, `efficient_p_wilcoxon=0.375`, `efficient_fdr=0.9052095024317248`, `contrast_p_wilcoxon=0.375`, `contrast_fdr=0.9965506589785832`. `CD9` has `screen_call=KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR`, `efficient_p_wilcoxon=0.875`, `efficient_fdr=1.0`, `contrast_p_wilcoxon=0.875`, `contrast_fdr=1.0`.

`STAT4` has table presence from Mixscale CRISPRi but not positive support: `best_direct_selectivity_score=-0.0502650068931169`, `best_direct_target_suppression=0.0`, `best_direct_target_vs_ifn_margin=0.0`, `direct_evidence_calls=null_or_wrong_direction`, `nomination_strength=not_nominated`.

All other candidates in wave37 are `UNRESOLVED` with non-significant adjusted statistics: SP140 `contrast_fdr=0.920009505703422`; RGS14 `contrast_fdr=0.9971256078463696`; PSAP `contrast_fdr=0.920009505703422`; HEXA `contrast_fdr=0.9971256078463696`; PARK7 `contrast_fdr=0.9965506589785832`; HEXB `contrast_fdr=0.920009505703422`; LYN `contrast_fdr=0.920009505703422`.

## Candidate-by-candidate stress verdict

`DAB2`: not cross-autoimmune. Evidence is direct-perturbation table call plus MS expression (`ms_delta_log2=0.5378984279794476`, `ms_p=0.0111306912319104`), but genetics/target-resolution is `0`, broad positive disease count is `0`, foundation support is `0`, and direct perturbation FDRs are weak (`efficient_fdr=0.9052095024317248`, `contrast_fdr=0.9965506589785832`).

`CD9`: not cross-autoimmune. Similar to DAB2 with stronger MS expression (`ms_delta_log2=1.1100295973517351`, `ms_p=0.0019686305906988`) but no genetics, no broad positive diseases, no foundation support, and direct perturbation FDRs of `1.0`.

`PARK7`: weak proxy breadth only. Wave55 lists `n_diseases_genetic_ge_0_25=5`, but wave62 fails target resolution (`max_l2g_score=0.12831711769104004`, `strong_l2g_disease_count=0`, `ms_genetic_association=0.0`). Foundation support is weak (`support_contexts=2`, `strong_support_contexts=0`). No FDR10 treatment response.

`PSAP`: not cross-autoimmune. Foundation support is weak single-context (`support_contexts=1`, `strong_support_contexts=0`), genetics/target-resolution is `0`, broad positive disease count is `0`, and treatment-response FDR10 is `0`.

`LYN`: disease-state/foundation signal but not a genetics-backed cross-autoimmune candidate. Broad positives are `3` (`Crohn disease;psoriasis;ulcerative colitis`) and Geneformer has `support_contexts=3`, `strong_support_contexts=1`, but genetics/target-resolution is `0`, MS anchor is `0`, and wave71 blocks it as `SRC_family_broad_selectivity_safety`.

`HEXA`: isolated model/state signal only. Broad positive disease count is `1` (`Crohn disease`), foundation support is single-context strong (`support_contexts=1`, `strong_support_contexts=1`), but genetics/target-resolution is `0`, MS anchor is `0`, and no FDR10 treatment response.

`HEXB`: isolated foundation signal only. Broad positive disease count is `0`; foundation has `support_contexts=1`, `strong_support_contexts=1`; genetics/target-resolution is `0`; no direct perturbation or treatment-response FDR support.

`SP140`: true cross-autoimmune breadth exists, but it is not intervention-ready. Genetics/colocalization and state recurrence are positive (`strong_l2g_disease_count=3`, `strong_qtl_coloc_disease_count=3`, broad positive disease count `4`), but direct perturbation is absent/negative, foundation support is `0`, treatment response does not pass FDR10, and the branch is explicitly blocked as closed/prior-art/chemistry-limited.

`RGS14`: genetics/target-resolution without cross-disease state breadth. It has `strong_l2g_disease_count=3`, `strong_qtl_coloc_disease_count=3`, and `ms_max_qtl_h4=0.9952074420704351`, but broad positive disease count is only `1` (`Crohn disease`), foundation support is `0`, direct perturbation support is absent, and wave62 calls `PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE`.

`STAT4`: strongest true genetics breadth but blocked mechanistically/druggability-wise. Genetics are broad (`strong_l2g_disease_count=8`, `strong_qtl_coloc_disease_count=7`, `max_qtl_h4=0.9941264815984456`), and disease-state positives are Crohn/UC. But direct perturbation is `null_or_wrong_direction`, foundation support is `0`, treatment-response FDR10 is `0`, `druggable_activity_count=0.0`, and both wave34a/wave71 demote it as wrong-direction/generic JAK-STAT/TF biology.

