# Wave99 LITAF/CASP4 Stress-Generator Audit

Random seed: `20260527`.

## Question

Do `LITAF` or `CASP4` survive as upstream inflammatory stress-generator
intervention points for the C15ORF48/MOCCI state after adding real
macrophage time-course and perturbation evidence?

## Verdict

Analysis call: `NO_PROMOTABLE_LITAF_CASP4_STRESS_GENERATOR`.

Both genes remain biologically useful upstream-stress hypotheses, but
neither is a V3 therapeutic nomination.

## Candidate Calls

| candidate | call | gates_passed | gates_total | failed_gates |
| --- | --- | --- | --- | --- |
| CASP4 | PARK_CASP4_UPSTREAM_PYROPTOSIS_NODE_PRIOR_SELECTIVITY_BLOCKED | 3 | 10 | human_timecourse_temporal_lead_over_c15;perturbation_not_just_broad_jak_ifn_confounding;mouse_indirect_perturbation_consistent;ms_claim_grade_anchor;target_resolved_genetics_or_coloc;direct_crispr_or_foundation_support;prior_art_not_blocking |
| LITAF | PARK_LITAF_UPSTREAM_STRESS_MARKER_NO_MODALITY | 3 | 10 | real_perturbation_moves_candidate_and_c15;perturbation_not_just_broad_jak_ifn_confounding;mouse_indirect_perturbation_consistent;ms_claim_grade_anchor;target_resolved_genetics_or_coloc;direct_crispr_or_foundation_support;selective_druggable_modality |

## Local Evidence Summary

| gene | wave96_call | wave97_call | c15_positive_disease_count | c15_state_pearson_r | residual_case_positive_disease_count | median_residual_case_r | ms_delta_log2 | ms_p | ms_fdr | wave62_strong_qtl_coloc_disease_count | chembl_activity_count | uniprot_accessible | w68_remission_adjusted_delta | w68_remission_adjusted_p | w68_remission_adjusted_fdr | w37_screen_call | w37_contrast_lfc | w37_contrast_fdr | wave39_call | wave39_reason | geneformer_strong_support_contexts | wave81_call | wave81_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LITAF | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | PARK_RESIDUAL_COSTATE_WITH_MODALITY | 3 | 0.7172822938218422 | 3 | 0.4155200059342984 | 0.3084198322537244 | 0.1715754140954014 | 0.8993702893651148 | 0.0 | 0.0 | True | -0.45070248331681 | 0.0154538227996733 | 0.0331277722550743 | UNRESOLVED | 0.0487929518498577 | 0.9971256078463696 | NO_GO_SURFACEOME_RESCUE | insufficient_breadth; reachable protein class by UniProt location/features |  |  |  |
| CASP4 | PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE | PARK_RESIDUAL_COSTATE_WITH_MODALITY | 3 | 0.3915924365400109 | 2 | 0.3084462466572922 | 0.2066862758954002 | 0.4927047679399916 | 0.9271619615463814 | 0.0 | 61.0 | True | -0.7246019576004594 | 0.0105026519754263 | 0.0281235550111651 |  |  |  | NO_GO_SURFACEOME_RESCUE | insufficient_breadth; no_ms_anchor; reachable protein class by UniProt location/features; ChEMBL exact target found; ChEMBL activity records: 61 |  |  |  |

## Human Macrophage Time-Course Summary

| gene | trajectory | first_1_5x_rise_hour | peak_hour | peak_delta_log2 | delta_3h | delta_6h | delta_12h |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C15ORF48 | PBS_LPS | 3.0 | 12.0 | 3.107495650556766 | 1.6793691023596846 | 2.629064953729374 | 3.107495650556766 |
| C15ORF48 | IFNY_LPS | 3.0 | 12.0 | 3.531583523506219 | 1.8462194521959 | 2.841511471789774 | 3.531583523506219 |
| NDUFA4 | PBS_LPS |  | 0.0 | 0.0 | -0.4132958317322366 | -0.5503990140732897 | -0.808218846523288 |
| NDUFA4 | IFNY_LPS |  | 1.0 | 0.009617957803076393 | -0.25028546753317027 | -0.26513784618621195 | -0.3264420916448172 |
| LITAF | PBS_LPS | 3.0 | 3.0 | 1.5115601463134052 | 1.5115601463134052 | 1.293489016755812 | 0.4879200285848668 |
| LITAF | IFNY_LPS | 3.0 | 6.0 | 1.5400790510182922 | 1.391396020410708 | 1.5400790510182922 | 0.661126639855798 |
| CASP4 | PBS_LPS | 3.0 | 12.0 | 1.5750292074125785 | 1.0646620282104982 | 1.4803725384214568 | 1.5750292074125785 |
| CASP4 | IFNY_LPS |  | 3.0 | 0.4623293270594182 | 0.4623293270594182 | 0.31172574223840677 | 0.09896397749131047 |

## Human Ruxolitinib Perturbation Effects

| feature | feature_type | hour | rux_minus_ifny_lps_log2 |
| --- | --- | --- | --- |
| C15ORF48 | gene | 0 | 0.17153129605366146 |
| NDUFA4 | gene | 0 | 0.528512382828473 |
| LITAF | gene | 0 | 0.2585541411596495 |
| CASP4 | gene | 0 | -1.5486368746584604 |
| ifn_apc | module | 0 | -2.560054952573429 |
| nfkb_cytokine | module | 0 | -0.2958180228238477 |
| pyroptosis | module | 0 | -1.0695197924205773 |
| c15_switch | module | 0 | -0.17849054338740578 |
| C15ORF48 | gene | 1 | 0.8664992262698572 |
| NDUFA4 | gene | 1 | 0.36851853316699934 |
| LITAF | gene | 1 | 0.35144657185857753 |
| CASP4 | gene | 1 | -1.6919014614102759 |
| ifn_apc | module | 1 | -2.1422853906348562 |
| nfkb_cytokine | module | 1 | 0.4705262890309543 |
| pyroptosis | module | 1 | -0.9674632175298502 |
| c15_switch | module | 1 | 0.24899034655142893 |
| C15ORF48 | gene | 3 | -0.11268369103855935 |
| NDUFA4 | gene | 3 | 0.5449809178893963 |
| LITAF | gene | 3 | 0.10513697548214651 |
| CASP4 | gene | 3 | -1.4584386330642278 |
| ifn_apc | module | 3 | -2.0350393277861833 |
| nfkb_cytokine | module | 3 | 0.15816624769705312 |
| pyroptosis | module | 3 | -0.8925056257327691 |
| c15_switch | module | 3 | -0.3288323044639778 |
| C15ORF48 | gene | 6 | -0.32347035959974946 |
| NDUFA4 | gene | 6 | 0.7310245923038332 |
| LITAF | gene | 6 | -0.21883380531259178 |
| CASP4 | gene | 6 | -0.7045394829060942 |
| ifn_apc | module | 6 | -1.30584048350113 |
| nfkb_cytokine | module | 6 | 0.24041898329670053 |
| pyroptosis | module | 6 | -0.389096460484258 |
| c15_switch | module | 6 | -0.5272474759517913 |

## Mouse Indirect Perturbation

| gene | NTC_US | NTC_IFNg | Gsk3b_US | Gsk3b_IFNg | Med16_US | Med16_IFNg | NTC_IFNg_vs_NTC_US | Gsk3b_IFNg_vs_NTC_IFNg | Med16_IFNg_vs_NTC_IFNg | Gsk3b_US_vs_NTC_US | Med16_US_vs_NTC_US |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Casp1 | 10.948123841446456 | 12.129390356332754 | 11.75112558336727 | 12.281253907016296 | 11.563355185588147 | 12.407002147924201 | 1.181266514886298 | 0.15186355068354196 | 0.2776117915914469 | 0.8030017419208129 | 0.6152313441416908 |
| Casp4 | 8.632995197142957 | 10.236412891651382 | 9.171593821802931 | 9.767080925074277 | 9.613482540731207 | 11.314016703901357 | 1.6034176945084244 | -0.46933196657710496 | 1.0776038122499756 | 0.5385986246599739 | 0.9804873435882495 |
| Cd74 | 10.223599529236369 | 15.481809940769674 | 12.179183414342234 | 14.530548583654053 | 12.046441948007311 | 12.991935132701927 | 5.258210411533305 | -0.9512613571156212 | -2.4898748080677464 | 1.955583885105865 | 1.8228424187709429 |
| Ciita | 3.415037499278844 | 11.62814171892075 | 2.2223924213364477 | 9.804668838539365 | 3.169925001442312 | 8.257387842692651 | 8.213104219641906 | -1.8234728803813844 | -3.3707538762280986 | -1.1926450779423963 | -0.24511249783653177 |
| Gsdmd | 10.454984659447938 | 11.517833395982667 | 11.007494536546924 | 11.900615270182032 | 11.166581558367941 | 11.981567281903015 | 1.062848736534729 | 0.38278187419936494 | 0.46373388592034814 | 0.552509877098986 | 0.7115968989200034 |
| Il1b | 4.624490864907794 | 6.910892526166014 | 6.1765887317233235 | 7.752659401271352 | 6.554588851677638 | 7.062495925733764 | 2.2864016612582203 | 0.8417668751053373 | 0.15160339956774926 | 1.5520978668155294 | 1.9300979867698436 |
| Litaf | 12.69855998492287 | 12.90407007654614 | 12.367141694552364 | 12.668146314934209 | 12.717462230349666 | 12.811307789016649 | 0.20551009162326928 | -0.23592376161193052 | -0.09276228752949045 | -0.33141829037050563 | 0.01890224542679597 |
| Ndufa4 | 12.347252251247228 | 12.331663421490079 | 12.219168520462162 | 11.820045964485535 | 12.645358214939957 | 11.99270235104369 | -0.01558882975714937 | -0.5116174570045438 | -0.33896107044638946 | -0.1280837307850664 | 0.2981059636927288 |
| Stat1 | 10.152284842306582 | 14.764526076414983 | 10.401946123976536 | 14.493751228601676 | 10.048486873992337 | 13.34091641632652 | 4.612241234108401 | -0.27077484781330696 | -1.423609660088463 | 0.2496612816699546 | -0.10379796831424493 |
| Tnf | 9.637228637735175 | 11.411864027299503 | 10.545286283329531 | 12.235316202095806 | 9.989631026616454 | 11.31741261376487 | 1.7746353895643274 | 0.8234521747963033 | -0.09445141353463349 | 0.9080576455943561 | 0.35240238888127884 |

## Gate Matrix

| candidate | gate | status | evidence |
| --- | --- | --- | --- |
| LITAF | residual_c15_costate_replicates | True | c15_positive_diseases=3; residual_case_positive_diseases=3; median_residual_r=0.4155 |
| LITAF | human_timecourse_temporal_lead_over_c15 | True | PBS_LPS: LITAF first=3h peak=3h; C15ORF48 first=3h peak=12h; IFNY_LPS: LITAF first=3h peak=6h; C15ORF48 first=3h peak=12h |
| LITAF | real_perturbation_moves_candidate_and_c15 | False | rux_mean_3_6h_LITAF=-0.05685; rux_6h_C15ORF48=-0.3235; rux_6h_ifn_apc=-1.306; rux_6h_pyroptosis=-0.3891 |
| LITAF | perturbation_not_just_broad_jak_ifn_confounding | False | rux_6h_ifn_apc=-1.306; if this is strongly negative, candidate suppression is broad JAK/IFN confounding rather than selective stress-node perturbation |
| LITAF | mouse_indirect_perturbation_consistent | False | Gsk3b_KO_IFNg_vs_NTC_IFNg=-0.2359; Med16_KO_IFNg_vs_NTC_IFNg=-0.09276; C15orf48 absent from this mouse matrix |
| LITAF | ms_claim_grade_anchor | False | MS delta=0.3084; p=0.1716; fdr=0.8994 |
| LITAF | target_resolved_genetics_or_coloc | False | strong_qtl_coloc_diseases=0 |
| LITAF | direct_crispr_or_foundation_support | False | Wave37=UNRESOLVED; contrast_lfc=0.04879; contrast_fdr=0.9971; Geneformer strong contexts= |
| LITAF | selective_druggable_modality | False | ChEMBL activity count=0; uniprot_accessible=True; for CASP4 this is only provisional because CASP1/CASP5 selectivity is not shown |
| LITAF | prior_art_not_blocking | True | LITAF has close macrophage/TNF and arthritis prior plus no modality; CASP4/CASP11 has direct EAE/demyelination and inhibitor-patent prior |
| CASP4 | residual_c15_costate_replicates | True | c15_positive_diseases=3; residual_case_positive_diseases=2; median_residual_r=0.3084 |
| CASP4 | human_timecourse_temporal_lead_over_c15 | False | PBS_LPS: CASP4 first=3h peak=12h; C15ORF48 first=3h peak=12h; IFNY_LPS: CASP4 first=h peak=3h; C15ORF48 first=3h peak=12h |
| CASP4 | real_perturbation_moves_candidate_and_c15 | True | rux_mean_3_6h_CASP4=-1.081; rux_6h_C15ORF48=-0.3235; rux_6h_ifn_apc=-1.306; rux_6h_pyroptosis=-0.3891 |
| CASP4 | perturbation_not_just_broad_jak_ifn_confounding | False | rux_6h_ifn_apc=-1.306; if this is strongly negative, candidate suppression is broad JAK/IFN confounding rather than selective stress-node perturbation |
| CASP4 | mouse_indirect_perturbation_consistent | False | Gsk3b_KO_IFNg_vs_NTC_IFNg=-0.4693; Med16_KO_IFNg_vs_NTC_IFNg=1.078; C15orf48 absent from this mouse matrix |
| CASP4 | ms_claim_grade_anchor | False | MS delta=0.2067; p=0.4927; fdr=0.9272 |
| CASP4 | target_resolved_genetics_or_coloc | False | strong_qtl_coloc_diseases=0 |
| CASP4 | direct_crispr_or_foundation_support | False | Wave37=; contrast_lfc=; contrast_fdr=; Geneformer strong contexts= |
| CASP4 | selective_druggable_modality | True | ChEMBL activity count=61; uniprot_accessible=True; for CASP4 this is only provisional because CASP1/CASP5 selectivity is not shown |
| CASP4 | prior_art_not_blocking | False | LITAF has close macrophage/TNF and arthritis prior plus no modality; CASP4/CASP11 has direct EAE/demyelination and inhibitor-patent prior |

## Source Anchors

| gene_or_axis | source_id | kind | claim_used | effect_on_wave99 |
| --- | --- | --- | --- | --- |
| LITAF | PMID:21984950 | literature | LITAF mediates increased TNF-alpha secretion from inflamed colonic lamina propria macrophages. | mechanistically close IBD macrophage/TNF prior art; supports stress-generator biology but not novelty/druggability |
| LITAF | PMID:22160695 | literature | Whole-body Litaf deletion improved endotoxic shock and inflammatory arthritis in mice. | direct inflammatory arthritis prior; systemic deletion not a selective modality |
| CASP4/CASP11 | PMID:11136825 | literature | Mouse caspase-11 mediated oligodendrocyte cell death and autoimmune demyelination pathogenesis. | direct MS/EAE-adjacent inflammatory caspase prior art |
| CASP4 | WO2026055444 | patent | Caspase-4 inhibitor patent family surfaced in prior Wave97 audit. | selective-inhibitor route is patent-crowded and requires CASP4-vs-CASP1/CASP5 selectivity |
| C15ORF48/MOCCI | PMID:33837217;PMID:34878835;PMID:38296961 | mechanism | C15ORF48/MOCCI is inflammation-induced mitochondrial complex-IV/autophagy brake biology. | defines the state being ordered against LITAF/CASP4 |

## Decision

- `LITAF`: park as an upstream macrophage/TNF/endolysosomal stress marker;
  no selective modality and no MS/genetic support.
- `CASP4`: park as an upstream pyroptosis/danger-state node; druggability
  exists only provisionally and is limited by selectivity and prior art.
- Next branch should not promote C15 co-state markers without direct
  target perturbation, MS spatial validation, and target-resolved genetics.

## Output Files

- `results_v3/wave99_litaf_casp4_stress_generator_audit/litaf_casp4_gate_matrix.tsv`
- `results_v3/wave99_litaf_casp4_stress_generator_audit/litaf_casp4_calls.tsv`
- `results_v3/wave99_litaf_casp4_stress_generator_audit/litaf_casp4_local_evidence_summary.tsv`
- `results_v3/wave99_litaf_casp4_stress_generator_audit/gse294918_log2cpm_selected_genes.tsv`
- `results_v3/wave99_litaf_casp4_stress_generator_audit/gse294918_lps_timecourse_deltas.tsv`
- `results_v3/wave99_litaf_casp4_stress_generator_audit/gse294918_timecourse_summary.tsv`
- `results_v3/wave99_litaf_casp4_stress_generator_audit/gse294918_ruxolitinib_effects.tsv`
- `results_v3/wave99_litaf_casp4_stress_generator_audit/gse162464_mouse_perturbation_selected_genes.tsv`
- `results_v3/wave99_litaf_casp4_stress_generator_audit/source_anchor_table.tsv`
- `results_v3/wave99_litaf_casp4_stress_generator_audit/summary.json`
- `results_v3/wave99_litaf_casp4_stress_generator_audit/REPORT.md`
