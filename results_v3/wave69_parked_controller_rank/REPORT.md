# Wave69 Parked-Gene Controller Rank

## Verdict

Anchor genes: `ARHGAP31;CD274;CD80;DCLRE1B;FCGR2A;FCGR2B;IL7R;LPP;NCF1;RGS14;STAT4;TNFRSF9;TNFSF15`.
Calls: `{'DESCRIPTIVE_SINGLE_ANCHOR_NEIGHBOR': 93, 'NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY': 35, 'PARK_DRUGGABLE_CONTROLLER_SCOUT_NEEDS_DIRECT_VALIDATION': 2}`.

This gate does not promote a therapeutic claim. It asks whether the Wave68 parked genes converge on a less-blocked intervention point.

## Top Controller Nodes

| candidate_node | wave69_call | controller_score | connected_anchor_count | connected_anchors | connection_roles | chembl_target_id | chembl_activity_rows | chembl_mechanism_rows | europepmc_prior_hits | clinicaltrials_hits | manual_blocker | wave62_call | wave57_call | wave61_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRKDC | PARK_DRUGGABLE_CONTROLLER_SCOUT_NEEDS_DIRECT_VALIDATION | 18.028834961021648 | 2 | NCF1;RGS14 | incoming_to_anchor | CHEMBL3142 | 3093.0 | 1.0 | 676.0 | 5.0 |  |  |  |  |
| BLK | PARK_DRUGGABLE_CONTROLLER_SCOUT_NEEDS_DIRECT_VALIDATION | 16.118130157563485 | 2 | FCGR2A;FCGR2B | incoming_to_anchor | CHEMBL2250 | 1174.0 | 0.0 | 0.0 | 5.0 |  | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |
| JAK1 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 27.13404466328152 | 2 | CD274;IL7R | incoming_to_anchor;manual_seed_controller;outgoing_from_anchor | CHEMBL2835 | 19812.0 | 17.0 | 8081.0 | 5.0 | generic_JAK_STAT_axis_prior_art_host_defense | NO_GO_WAVE62_TARGET_RESOLUTION |  | NO_GO_WAVE61_GUARDRAIL |
| JAK2 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 25.049012441163672 | 2 | CD274;STAT4 | incoming_to_anchor;manual_seed_controller | CHEMBL2971 | 24544.0 | 25.0 | 10122.0 | 5.0 | generic_JAK_STAT_axis_prior_art_host_defense | NO_GO_WAVE62_TARGET_RESOLUTION |  | NO_GO_WAVE61_GUARDRAIL |
| JAK3 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 20.409336886049257 | 1 | IL7R | incoming_to_anchor;manual_seed_controller;outgoing_from_anchor |  | 0.0 | 0.0 | 0.0 | 0.0 | generic_JAK_STAT_axis_prior_art_host_defense |  |  |  |
| FYN | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 20.316121524177152 | 3 | FCGR2A;FCGR2B;LPP | incoming_to_anchor | CHEMBL1841 | 3572.0 | 1.0 | 1978.0 | 5.0 | broad_SRC_family_kinase_prior_art_selectivity_safety |  |  |  |
| SRC | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 20.12016656589379 | 3 | FCGR2A;FCGR2B;LPP | incoming_to_anchor | CHEMBL267 | 8363.0 | 8.0 | 12029.0 | 5.0 | broad_SRC_family_kinase_prior_art_selectivity_safety |  |  | NO_GO_WAVE61_GUARDRAIL |
| PDCD1 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 17.54641562711233 | 2 | CD274;FCGR2A | manual_seed_controller;outgoing_from_anchor | CHEMBL3307223 | 9.0 | 26.0 | 11157.0 | 5.0 | PD_1_checkpoint_prior_art_and_autoimmune_safety_direction_risk | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |
| GSK3B | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 17.333432874747828 | 3 | ARHGAP31;CD274;NCF1 | incoming_to_anchor | CHEMBL6067425 | 4.0 | 0.0 | 825.0 | 5.0 | GSK3_family_pleiotropic_neuroimmune_metabolic |  |  | NO_GO_WAVE61_GUARDRAIL |
| SYK | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 17.149645761932643 | 2 | FCGR2A;FCGR2B | incoming_to_anchor;manual_seed_controller | CHEMBL2599 | 8906.0 | 14.0 | 4655.0 | 5.0 | SYK_prior_art_broad_immunosuppression | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |
| CD274 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 17.040789927374952 | 2 | CD274;CD80 | incoming_to_anchor;outgoing_from_anchor;self_anchor | CHEMBL3580522 | 1882.0 | 13.0 | 3625.0 | 5.0 | PD_L1_checkpoint_prior_art_and_autoimmune_safety_direction_risk | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |
| CD80 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 16.470383103720312 | 2 | CD274;CD80 | incoming_to_anchor;outgoing_from_anchor;self_anchor | CHEMBL2364157 | 0.0 | 3.0 | 15783.0 | 5.0 | costimulation_axis_prior_art_and_broad_T_cell_APC_biology | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |
| MAPK14 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 15.99104551690587 | 2 | NCF1;STAT4 | incoming_to_anchor | CHEMBL260 | 8611.0 | 35.0 | 811.0 | 5.0 | p38_MAPK_autoimmune_prior_art_and_broad_stress_axis | NO_GO_WAVE62_TARGET_RESOLUTION |  | NO_GO_WAVE61_GUARDRAIL |
| TYK2 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 15.43998087842106 | 1 | STAT4 | incoming_to_anchor;manual_seed_controller |  | 0.0 | 0.0 | 0.0 | 0.0 | generic_JAK_STAT_axis_prior_art_host_defense | NO_GO_WAVE62_TARGET_RESOLUTION |  | NO_GO_WAVE61_GUARDRAIL |
| RELA | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 15.241221460428006 | 3 | CD274;TNFRSF9;TNFSF15 | manual_seed_controller | CHEMBL5533 | 175.0 | 0.0 | 5612.0 | 5.0 | generic_NFKB_host_defense |  |  |  |
| GSK3A | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 14.098284166902161 | 2 | ARHGAP31;CD274 | incoming_to_anchor | CHEMBL2850 | 3464.0 | 1.0 | 202.0 | 5.0 | GSK3_family_pleiotropic_neuroimmune_metabolic |  |  |  |
| INSR | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 13.221910450056532 | 2 | FCGR2A;LPP | incoming_to_anchor | CHEMBL1981 | 3018.0 | 30.0 | 2744.0 | 5.0 | systemic_insulin_receptor_metabolic_safety |  |  |  |
| LYN | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 12.618130157563485 | 2 | FCGR2A;FCGR2B | incoming_to_anchor | CHEMBL3905 | 2166.0 | 4.0 | 0.0 | 5.0 | broad_SRC_family_kinase_prior_art_selectivity_safety |  |  |  |
| PRKACA | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 12.4760760863746 | 1 | RGS14 | incoming_to_anchor;manual_seed_controller |  | 0.0 | 0.0 | 0.0 | 0.0 | broad_PKA_pleiotropy_no_myeloid_selectivity |  |  |  |
| CD28 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 11.730432008040129 | 1 | CD80 | incoming_to_anchor;manual_seed_controller;outgoing_from_anchor |  | 0.0 | 0.0 | 0.0 | 0.0 | costimulation_axis_approved_prior_art_systemic_T_cell_activation_risk | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |
| TNFRSF25 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 8.905019518177976 | 1 | TNFSF15 | manual_seed_controller;outgoing_from_anchor |  | 0.0 | 0.0 | 0.0 | 0.0 | TL1A_DR3_axis_prior_art_and_lymphocyte_pleiotropy |  |  |  |
| NFKB1 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 8.67908572383636 | 2 | TNFRSF9;TNFSF15 | manual_seed_controller | CHEMBL3251 | 1418.0 | 0.0 | 0.0 | 5.0 | generic_NFKB_host_defense | NO_GO_WAVE62_TARGET_RESOLUTION |  | NO_GO_WAVE61_GUARDRAIL |
| CTLA4 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 7.320288005360085 | 1 | CD80 | manual_seed_controller;outgoing_from_anchor |  | 0.0 | 0.0 | 0.0 | 0.0 | costimulation_axis_approved_prior_art | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |
| PRKACB | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 3.9880380431873004 | 1 | RGS14 | incoming_to_anchor |  | 0.0 | 0.0 | 0.0 | 0.0 | broad_PKA_pleiotropy_no_myeloid_selectivity |  |  |  |
| STAT4 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 3.9299934266150336 | 1 | STAT4 | self_anchor | CHEMBL4523296 | 5.0 | 0.0 | 4014.0 | 5.0 | STAT4_TF_not_selectively_druggable | PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW | NO_GO_MODEL_SCREEN | NO_GO_WAVE61_GUARDRAIL |
| HRAS | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 3.7380380431873004 | 1 | RGS14 | manual_seed_controller |  | 0.0 | 0.0 | 0.0 | 0.0 | oncogenic_RAS_not_chronic_autoimmune_target |  |  |  |
| RAF1 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 3.7380380431873004 | 1 | RGS14 | manual_seed_controller |  | 0.0 | 0.0 | 0.0 | 0.0 | MAPK_oncology_pleiotropy | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |
| IL7R | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 2.8285297481360625 | 1 | IL7R | self_anchor |  | 0.0 | 0.0 | 2197.0 | 5.0 | prior_art_CD127_autoimmune_axis | PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW | REOPEN_MODEL_SUPPORTED_INTERVENTION_FIRST |  |
| NCF1 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 2.797068870466034 | 1 | NCF1 | self_anchor | CHEMBL1613743 | 199.0 | 0.0 | 638.0 | 5.0 | NADPH_oxidase_host_defense_CGD_directionality_risk | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |
| STAT1 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 2.749434497146563 | 1 | CD274 | manual_seed_controller |  | 0.0 | 0.0 | 0.0 | 0.0 | generic_IFN_transcription_axis | NO_GO_WAVE62_TARGET_RESOLUTION |  | NO_GO_WAVE61_GUARDRAIL |
| EGFR | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 2.448518847279617 | 1 | FCGR2A | incoming_to_anchor |  | 0.0 | 0.0 | 0.0 | 0.0 |  | NO_GO_WAVE62_TARGET_RESOLUTION |  | NO_GO_L1000_MECHANISM_ONLY |
| CYBB | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 1.8875197101974557 | 1 | NCF1 | manual_seed_controller |  | 0.0 | 0.0 | 0.0 | 0.0 | NADPH_oxidase_host_defense_CGD_directionality_risk |  |  |  |
| NCF2 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 1.8875197101974557 | 1 | NCF1 | manual_seed_controller |  | 0.0 | 0.0 | 0.0 | 0.0 | NADPH_oxidase_host_defense_CGD_directionality_risk | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |
| FCGR2B | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 1.1891896914129672 | 1 | FCGR2B | self_anchor | CHEMBL4662940 | 0.0 | 1.0 | 834.0 | 5.0 | Fc_receptor_directionality_and_safety | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |
| CD86 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 1.1601440026800427 | 1 | CD80 | manual_seed_controller |  | 0.0 | 0.0 | 0.0 | 0.0 | costimulation_axis_prior_art_and_broad_T_cell_APC_biology | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE |  |  |
| FCGR2A | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 1.0933154518231971 | 1 | FCGR2A | self_anchor | CHEMBL5841 | 1.0 | 0.0 | 731.0 | 5.0 | Fc_receptor_directionality_and_safety | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |
| TNFSF15 | NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY | 0.8718309221190663 | 1 | TNFSF15 | self_anchor |  | 0.0 | 0.0 | 583.0 | 5.0 | TL1A_axis_prior_art_IBD_trials | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |
| TNFRSF6B | DESCRIPTIVE_SINGLE_ANCHOR_NEIGHBOR | 13.905019518177976 | 1 | TNFSF15 | incoming_to_anchor;outgoing_from_anchor |  | 0.0 | 0.0 | 0.0 | 0.0 |  | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |
| MAP2K6 | DESCRIPTIVE_SINGLE_ANCHOR_NEIGHBOR | 11.96999043921053 | 1 | STAT4 | incoming_to_anchor |  | 0.0 | 0.0 | 0.0 | 0.0 |  |  |  |  |
| PIAS2 | DESCRIPTIVE_SINGLE_ANCHOR_NEIGHBOR | 10.96999043921053 | 1 | STAT4 | incoming_to_anchor |  | 0.0 | 0.0 | 0.0 | 0.0 |  |  |  |  |

## Top Enrichr Terms

| library | rank | term | adjusted_p | overlap_genes |
| --- | --- | --- | --- | --- |
| Reactome_2022 | 1 | Immune System R-HSA-168256 | 2.824954417547414e-05 | CD274;FCGR2A;NCF1;TNFSF15;CD80;TNFRSF9;STAT4;FCGR2B;IL7R |
| WikiPathway_2023_Human | 1 | T Cell Modulation In Pancreatic Cancer WP5078 | 0.00013778176969944474 | CD274;CD80;TNFRSF9 |
| GO_Biological_Process_2023 | 1 | Negative Regulation Of Lymphocyte Proliferation (GO:0050672) | 0.00040036762313980934 | CD274;CD80;FCGR2B |
| GO_Biological_Process_2023 | 2 | Negative Regulation Of T Cell Activation (GO:0050868) | 0.0004020570962049601 | CD274;CD80;FCGR2B |
| WikiPathway_2023_Human | 2 | FOXP3 In COVID 19 WP5063 | 0.0008762382659316642 | CD80;IL7R |
| KEGG_2021_Human | 1 | Fc gamma R-mediated phagocytosis | 0.0012823592270117252 | FCGR2A;NCF1;FCGR2B |
| KEGG_2021_Human | 2 | Osteoclast differentiation | 0.001433525378531205 | FCGR2A;NCF1;FCGR2B |
| KEGG_2021_Human | 3 | Phagosome | 0.0016295309688173934 | FCGR2A;NCF1;FCGR2B |
| Reactome_2022 | 2 | Cytokine Signaling In Immune System R-HSA-1280215 | 0.0020045638467129736 | TNFSF15;CD80;TNFRSF9;STAT4;IL7R |
| WikiPathway_2023_Human | 3 | Interactions Between Immune Cells And microRNAs In Tumor Microenvironment WP4559 | 0.0020929941738406658 | CD274;CD80 |
| WikiPathway_2023_Human | 4 | Genetic Causes Of Porto Sinusoidal Vascular Disease WP5269 | 0.0025799639403273084 | ARHGAP31;NCF1 |
| WikiPathway_2023_Human | 5 | Thymic Stromal Lymphopoietin TSLP Signaling Pathway WP2203 | 0.0025799639403273084 | STAT4;IL7R |
| GO_Biological_Process_2023 | 3 | Negative Regulation Of Interleukin-10 Production (GO:0032693) | 0.0027668454202139673 | CD274;FCGR2B |
| GO_Biological_Process_2023 | 4 | Cellular Response To Molecule Of Bacterial Origin (GO:0071219) | 0.0027668454202139673 | CD274;CD80;FCGR2B |
| WikiPathway_2023_Human | 6 | 8P23 1 Copy Number Variation Syndrome WP5346 | 0.003638917953401061 | FCGR2A;FCGR2B |
| Reactome_2022 | 3 | TNFs Bind Their Physiological Receptors R-HSA-5669034 | 0.003919548702908302 | TNFSF15;TNFRSF9 |
| TRRUST_Transcription_Factors_2019 | 1 | SPI1 mouse | 0.004692062468916975 | NCF1;IL7R |
| TRRUST_Transcription_Factors_2019 | 2 | RELA human | 0.004692062468916975 | CD80;TNFRSF9;STAT4 |
| TRRUST_Transcription_Factors_2019 | 3 | NFKB1 human | 0.004692062468916975 | CD80;TNFRSF9;STAT4 |
| ChEA_2022 | 1 | MECOM 23826213 ChIP-Seq KASUMI Mouse | 0.007620964485991921 | DCLRE1B;CD274;ARHGAP31;RGS14;NCF1;TNFRSF9;FCGR2B |
| KEGG_2021_Human | 4 | Cytokine-cytokine receptor interaction | 0.008548381832879075 | TNFSF15;TNFRSF9;IL7R |
| WikiPathway_2023_Human | 7 | T Cell Activation SARS CoV 2 WP5098 | 0.008886400971191087 | CD80;STAT4 |
| KEGG_2021_Human | 5 | Leishmaniasis | 0.00932582772686183 | FCGR2A;NCF1 |
| GO_Biological_Process_2023 | 5 | Negative Regulation Of T Cell Proliferation (GO:0042130) | 0.010046105059136785 | CD274;CD80 |
| KEGG_2021_Human | 6 | Staphylococcus aureus infection | 0.011781194326599471 | FCGR2A;FCGR2B |
| GO_Biological_Process_2023 | 6 | Regulation Of Interleukin-10 Production (GO:0032653) | 0.013703312089675974 | CD274;FCGR2B |
| TRRUST_Transcription_Factors_2019 | 4 | GABPA mouse | 0.014533611549336392 | IL7R |
| TRRUST_Transcription_Factors_2019 | 5 | TRERF1 human | 0.014533611549336392 | CD80 |
| Reactome_2022 | 4 | Costimulation By CD28 Family R-HSA-388841 | 0.01472770586665288 | CD274;CD80 |
| Reactome_2022 | 5 | Adaptive Immune System R-HSA-1280218 | 0.01472770586665288 | CD274;NCF1;CD80;FCGR2B |

## Parked Druggable Controller Scouts

| candidate_node | wave69_call | controller_score | connected_anchor_count | connected_anchors | connection_roles | chembl_target_id | chembl_activity_rows | chembl_mechanism_rows | europepmc_prior_hits | clinicaltrials_hits | manual_blocker | wave62_call | wave57_call | wave61_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRKDC | PARK_DRUGGABLE_CONTROLLER_SCOUT_NEEDS_DIRECT_VALIDATION | 18.028834961021648 | 2 | NCF1;RGS14 | incoming_to_anchor | CHEMBL3142 | 3093.0 | 1.0 | 676.0 | 5.0 |  |  |  |  |
| BLK | PARK_DRUGGABLE_CONTROLLER_SCOUT_NEEDS_DIRECT_VALIDATION | 16.118130157563485 | 2 | FCGR2A;FCGR2B | incoming_to_anchor | CHEMBL2250 | 1174.0 | 0.0 | 0.0 | 5.0 |  | NO_GO_WAVE62_TARGET_RESOLUTION |  |  |

## Guardrails

- Immediate network convergence is not causality.
- ChEMBL activity or mechanism rows mean chemical matter exists, not that tissue-selective autoimmune target engagement is feasible.
- Manual blockers encode already-known V3 and clinical-class failures so prior-art-heavy checkpoint/JAK/TNF/TL1A axes do not masquerade as discoveries.
