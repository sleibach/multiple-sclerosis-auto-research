# Wave94 APOC1/APOE/LPL Lipid-Macrophage Axis Sidecar

Question: after GPR183 closure, should the lipid-associated macrophage/apolipoprotein axis (`APOC1`/`APOE`/`LPL`) be promoted as a cross-autoimmune central-node candidate?

Verdict: **APOC1 is a biomarker/state marker, not a target.** It should not be advanced as a central intervention node. The strongest support is disease-state recurrence and MS lesion/CSF biomarker literature; the decisive blockers are absent APOC1-specific genetics/colocalization, no direct perturbation or druggable route, APOE-region LD ambiguity, and neighboring APOE/LPL audits already concluding marker/no-go rather than target.

## Local Evidence Used

Primary local artifacts:

- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank.tsv`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
- `results_v3/wave91_lipid_neighborhood_controller_scan/lipid_neighborhood_controller_rank.tsv`
- `results_v3/wave91_lipid_lysosomal_module_intervention_rank/lipid_lysosomal_intervention_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/wave86_external_geo_antitnf_gene_driver/external_geo_gene_meta_rank.tsv`
- `results_v3/wave89_psoriasis_gse85034_response/psoriasis_baseline_gene_response_tests.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- Prior APOC1 genetics sidecar: `subagents_v3/wave9_apoc1_genetics_report.md`

## APOC1 Local Signal

`APOC1` is locally interesting as a lipid/myeloid state marker:

- Broad H5AD summary: `positive_disease_count=3` (`Sjogren syndrome;type 1 diabetes mellitus;ulcerative colitis`), `negative_disease_count=1` (`ulcerative colitis`), `best_positive_p=0.007747831575156192`, `best_positive_fdr=0.33539965560265417`, `max_positive_delta_log2_cpm=1.507336097479321`, `median_positive_hedges_g=1.2341409625104072`.
- Top positive compartments: `t1d_acinar_cell:1.51,p=0.0077`; `sjogren_gland_epithelial:1.18,p=0.0097`; `ibd_uc_epithelial:1.28,p=0.047`.
- Negative compartment: `ibd_uc_stromal`, `delta_log2_cpm=-1.567049625672901`, `hedges_g=-1.229199735438806`, `p=0.04675520808954815`, `fdr=0.36705989849366844`.
- MS white matter GSE111972: `delta_log2=0.8063088065414767`, `hedges_g=0.9608733173113739`, `p=0.03334872558641595`, `fdr=0.8506970233122761`, `mean_case=12.039401755680897`, `mean_control=11.23309294913942`.

Stress-test interpretation: these are nominal expression/state signals, not target evidence. None of the APOC1 local signals pass FDR10 in broad H5AD or MS white matter.

## Wave39 Surfaceome Result

`results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank.tsv`

`APOC1` was already tested as a reachable protein/surfaceome-style rescue and failed:

- `wave39_call=NO_GO_SURFACEOME_RESCUE`
- `wave39_score=8.5`
- `wave39_reason=insufficient_breadth; directional_negative_disease_signal; reachable protein class by UniProt location/features`
- `positive_disease_count=3`
- `negative_disease_count=1`
- `ms_wm_delta_log2=0.8063088065414767`
- `ms_wm_p=0.0333487255864159`
- `best_positive_fdr=0.3353996556026541`

This is the best local “APOC1 as accessible protein” test, and it explicitly says no-go.

## Wave91 Neighborhood Result

`APOC1` is not present in either Wave91 rank table:

- `results_v3/wave91_lipid_neighborhood_controller_scan/lipid_neighborhood_controller_rank.tsv`
- `results_v3/wave91_lipid_lysosomal_module_intervention_rank/lipid_lysosomal_intervention_rank.tsv`

That absence matters: Wave91 was the post-LPL lipid-neighborhood controller scan, and it did not nominate APOC1 as a controller candidate.

For the neighboring axis:

`LPL` in `lipid_neighborhood_controller_rank.tsv`:

- `wave91_call=PARK_MARKER_OR_WEAK_CONTROLLER`
- `wave91_score=4.35`
- failures: `case_control_negative_context_present;no_usable_foundation_model_rows;weak_direct_druggability;major_safety_or_selectivity_liability`
- route: `enzyme/extracellular lipid hydrolysis`
- liability: `systemic triglyceride biology; direct autoimmune modulation unsafe/unselective`
- MS WM: `ms_wm_delta=1.7595984466157422`, `ms_wm_p=0.0006219963760009`, `ms_wm_fdr=0.7144250374746858`

`APOE` in `lipid_neighborhood_controller_rank.tsv`:

- `wave91_call=NO_GO_LIPID_NEIGHBORHOOD_NODE`
- `wave91_score=-0.95`
- failures: `no_nominal_ms_wm_up_anchor;case_control_negative_context_present;weak_direct_druggability;manual_prior_or_class_pressure`
- route: `apolipoprotein/lipid transport state`
- liability: `genotype- and CNS-biology complexity; marker more than target`

`LPL` in `lipid_lysosomal_intervention_rank.tsv`:

- `wave91_call=NO_GO_DIRECT_ATLAS_CONTRADICTION`
- `route_blocker=NO_GO_DIRECT_SYSTEMIC_LIPOLYSIS_TARGET_MARKER_ONLY`
- direct H5AD: `direct_positive_p05_disease_count=1` (`Crohn disease`), `direct_negative_p05_disease_count=1` (`psoriasis`), `direct_positive_fdr10_disease_count=0`, `direct_negative_fdr10_disease_count=0`
- response: IBD `ibd_wave86_call=NO_GENE_LEVEL_CONVERGENCE`, RA `ra_call=NONRESPONSE_HIGH_TREND`, psoriasis ADA `psoriasis_ada_call=NONRESPONSE_HIGH_NOMINAL`

`APOE` in `lipid_lysosomal_intervention_rank.tsv`:

- `wave91_call=NO_GO_NO_MS_WHITE_MATTER_SINGLE_GENE_ANCHOR`
- `route_blocker=NO_GO_SECRETED_LIPID_CARRIER_MARKER_CNS_AND_SYSTEMIC_LIPID_RISK`
- direct H5AD: `direct_positive_p05_disease_count=0`, `direct_negative_p05_disease_count=1` (`psoriasis`)
- response: IBD `ibd_wave86_call=PARK_DIRECTIONAL_NONRESPONSE_GENE`, psoriasis ADA `psoriasis_ada_call=NO_SUPPORT`

Interpretation: the best-studied local neighbors already fail as intervention nodes. APOC1 is less target-resolved than either.

## Response Evidence

`APOC1` is not covered in the Wave86/Wave89 response outputs used for APOE/LPL. That is a blocker, not neutral support.

`APOE` anti-TNF IBD, `results_v3/wave86_external_geo_antitnf_gene_driver/external_geo_gene_meta_rank.tsv`:

- `call=PARK_DIRECTIONAL_NONRESPONSE_GENE`
- `n_primary_contexts=4`
- `nonresponse_high_contexts=3`
- `responder_high_contexts=1`
- `nominal_nonresponse_contexts_p_lt_0_05=1`
- `fdr10_nonresponse_contexts=1`
- `weighted_mean_hedges_g_responder_minus_non=-0.47444093945970656`
- `median_auc_high_score_nonresponse=0.625`
- `min_p=0.024946099541531475`

`LPL` anti-TNF IBD:

- `call=NO_GENE_LEVEL_CONVERGENCE`
- `n_primary_contexts=4`
- `nonresponse_high_contexts=3`
- `responder_high_contexts=1`
- `nominal_nonresponse_contexts_p_lt_0_05=0`
- `fdr10_nonresponse_contexts=0`
- `weighted_mean_hedges_g_responder_minus_non=-0.2044930888200467`
- `median_auc_high_score_nonresponse=0.5470238095238096`
- `min_p=0.25080455283827324`

`LPL` psoriasis GSE85034 ADA, `results_v3/wave89_psoriasis_gse85034_response/psoriasis_baseline_gene_response_tests.tsv`:

- `n_subjects=14`, `n_pasi75_responders=9`, `n_pasi75_nonresponders=5`
- `effect_responder_minus_non=-0.67165690386129`
- `hedges_g_responder_minus_non=-2.208896818102851`
- `auc_high_score_nonresponse=0.9555555555555556`
- `p=0.011107701824316356`
- `fdr_within_treatment=0.499846582094236`

`APOE` psoriasis ADA:

- `effect_responder_minus_non=0.5413090932403735`
- `hedges_g_responder_minus_non=0.7924492941076007`
- `auc_high_score_nonresponse=0.2222222222222222`
- `p=0.08557674575156887`
- `fdr_within_treatment=0.8144849241386118`

Response conclusion: local neighboring axis can behave as a nonresponse marker in places, especially APOE in IBD and LPL in psoriasis ADA, but there is no APOC1 response evidence and no corrected cross-disease treatment-response support that would make APOC1 a central intervention node.

## Genetics and Target Resolution

`results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`

`APOC1`:

- `wave62_call=NO_GO_WAVE62_TARGET_RESOLUTION`
- `wave62_score=1.0896429941058159`
- `strong_l2g_disease_count=0`
- `strong_qtl_coloc_disease_count=0`
- `ms_max_l2g_score=0.0`
- `ms_max_qtl_h4=0.0`
- `chembl_target_id` blank
- `druggable_activity_count=0.0`

`APOE`:

- `wave62_call=NO_GO_WAVE62_TARGET_RESOLUTION`
- `wave62_score=1.961044430732727`
- `strong_l2g_disease_count=1` (`Crohn`)
- `strong_qtl_coloc_disease_count=0`
- `ms_max_l2g_score=0.0`
- `ms_max_qtl_h4=0.0`

`LPL`: no positive target-resolution summary row for the axis; Wave55 lists `n_diseases_genetic_ge_0_25=0`, `ms_genetic_association=0.0`, `ms_overall_score=0.0`.

Prior sidecar `subagents_v3/wave9_apoc1_genetics_report.md` reached the same conclusion: APOC1 is not genetically anchored as a causal autoimmune target. It specifically warns that the chr19 `NECTIN2`-`TOMM40`-`APOE`-`APOC1` haplotype block prevents assigning an APOC1 causal claim without fine-mapping/conditioning on APOE epsilon and neighboring markers.

## GPR183 Comparator After Closure

`results_v3/wave93_gpr183_oxysterol_forcing_test/target_resolution_rows.tsv` and related outputs explain why the post-GPR183 pivot should not simply move to APOC1:

- `GPR183` had stronger treatment-response signal than APOC1: IBD anti-TNF `nonresponse_high_contexts=4`, `weighted_mean_hedges_g_responder_minus_non=-1.1082226616268842`, `min_p=0.0008985987348273754`.
- It still failed local MS/target-resolution anchors: `ms_wm_delta_log2=-0.1364089401905186`, `ms_wm_p=0.6637151735644201`, `ms_wm_fdr=0.9565589890801192`, `wave62_call=NO_GO_WAVE62_TARGET_RESOLUTION`.
- APOC1 has the reverse shape: nominal MS expression and some broad state positives, but no response coverage and no genetics/target resolution.

If GPR183 is closed despite a stronger response signature, APOC1 cannot be reopened on weaker causal/intervention evidence.

## External Prior Art: Light Audit

This was not an exhaustive prior-art search. It was intended to classify whether APOC1 has autoimmune/MS intervention precedent.

PubMed/eutils query:

```text
(APOC1[Title/Abstract] OR "apolipoprotein C1"[Title/Abstract] OR "apolipoprotein C-I"[Title/Abstract])
AND (multiple sclerosis OR autoimmune OR rheumatoid OR Crohn OR ulcerative colitis OR psoriasis)
```

Returned 12 PubMed records. Relevant interpretation:

- MS biomarker/state literature exists. A Scientific Reports MS CSF proteome paper reported APOC1 as an MS-specific upregulated CSF protein with transcript support in active lesions. Link: https://www.nature.com/articles/s41598-021-83591-5
- MS myeloid-state literature supports APOC1 as part of MS-associated / foamy microglia biology. A 2024 Nature Communications paper lists APOC1 among enriched markers of an MS microglial cluster and cites MS-associated microglia expressing high CTSD/APOC1/GPNMB/ANXA2/LGALS1. Link: https://www.nature.com/articles/s41467-024-49312-y
- General APOC1 biology supports lipid/immunity plausibility but not autoimmune targetability. A 2019 review describes APOC1 lipid metabolism, APOE linkage disequilibrium, and immune/inflammatory associations. PubMed: https://pubmed.ncbi.nlm.nih.gov/31779116/
- PubMed autoimmune-adjacent titles include psoriasis, ulcerative colitis/DSS colitis, rheumatoid arthritis biomarker, Graves disease macrophage/Tfh crosstalk, and septic-vs-rheumatoid arthritis synovial fluid discrimination, but these are biomarker/pathway papers rather than APOC1-directed autoimmune interventions.

ClinicalTrials.gov API query for `APOC1 OR "Apolipoprotein C1"` found no APOC1 autoimmune/MS therapeutic trial. The clearly APOC1-named study is `NCT02816099`, a completed type 1 diabetes lipid/CETP observational/metabolic study, not an autoimmune disease-modifying intervention. Link: https://clinicaltrials.gov/study/NCT02816099

Patent-light check found diagnostic/biomarker-style APOC1/IP around HDL-associated protein detection, not autoimmune treatment. Example: `EP4524152A2` includes ApoC1 binding agents and ApoC1 mass spectrometry standards in HDL-associated biomarker panels, with CVD/reverse cholesterol transport risk language. Link: https://data.epo.org/publication-server/rest/v1.2/patents/EP4524152NWA2/document.pdf

External conclusion: prior art supports APOC1 as a biomarker and lipid/immunity state molecule. I did not find APOC1-specific autoimmune/MS intervention precedent, clinical trial precedent, or a mature therapeutic modality.

## Target vs Biomarker vs No-Go

Classification: **biomarker/state marker**.

Do not call APOC1 a target. Do not call APOC1 a central cross-autoimmune node. The defensible statement is:

> APOC1 marks lipid-associated macrophage/microglial/apolipoprotein biology with nominal MS and cross-disease state recurrence, but current local and external evidence supports marker status only.

Concrete blockers:

1. **No APOC1 target resolution/genetics:** `wave62_call=NO_GO_WAVE62_TARGET_RESOLUTION`, `strong_l2g_disease_count=0`, `strong_qtl_coloc_disease_count=0`, `ms_max_l2g_score=0.0`, `ms_max_qtl_h4=0.0`.
2. **APOE-region LD ambiguity:** chr19 APOE/APOC1 locus cannot support APOC1-specific causal claims without conditioning/fine-mapping.
3. **No druggable handle:** no ChEMBL target id or activity in Wave62; no local direct perturbation evidence.
4. **Surfaceome rescue already failed:** Wave39 `NO_GO_SURFACEOME_RESCUE` due to insufficient breadth and directional negative disease signal.
5. **Wave91 did not nominate APOC1:** neighboring `APOE` and `LPL` are marker/no-go, not central-node targets.
6. **Response gap:** no APOC1 Wave86/Wave89 treatment-response coverage; APOE/LPL response signals are marker-like and not corrected cross-disease intervention evidence.
7. **Systemic lipid/CNS liability:** APOE/LPL route blockers flag CNS/genotype/systemic lipid risk; APOC1 biology is in the same secreted apolipoprotein/lipoprotein transport space.

Recommended status: keep APOC1 only as a lesion/lipid-macrophage biomarker and module readout. Reopen only if a future dataset provides APOC1-specific perturbation in disease-relevant macrophages/microglia, conditioned APOC1-specific genetics/colocalization independent of APOE/TOMM40/NECTIN2, and a tractable local or CNS-selective modality.

