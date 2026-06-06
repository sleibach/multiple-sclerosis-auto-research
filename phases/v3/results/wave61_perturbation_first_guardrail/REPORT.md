# Wave61 Perturbation-First Guardrail Scorer

Random seed: `20260527`.

## Verdict

- Promotion candidates: `0`.
- Reopened perturbation candidates: `0`.
- L1000-only candidates were capped at support-only status by design.

The scorer treats real perturbation evidence as necessary but not sufficient. A route also needs selectivity over generic IFN/JAK/NF-kB collapse, stress/viability guardrails, repair or efferocytosis guardrails, disease recurrence including MS, genetics or response anchoring, druggability, and no manual safety/prior-art blocker.

## Top Direct Perturbation Rows

| evidence_tier | candidate | gene | source | target_suppression | generic_ifn_suppression | target_vs_ifn_margin | selectivity_score | gate_count | direct_priority_score | manual_blocker | wave61_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| real_direct_perturbation | Med16_KO | MED16 | mouse_macrophage_RNAseq | 3.139501453617054 | 0.797854931783739 | 2.3416465218333142 | 2.3051173986620066 | 5 | 10.792060152948057 | broad_transcriptional_Mediator_risk | NO_GO_WAVE61_GUARDRAIL |
| real_direct_perturbation | Gsk3b_KO | GSK3B | mouse_macrophage_RNAseq | 1.6223580114004137 | 0.7952007387801626 | 0.8271572726202511 | 0.7779563820432978 | 5 | 8.511336202422061 | pleiotropic_neuroimmune_metabolic | NO_GO_WAVE61_GUARDRAIL |
| real_direct_perturbation | TNFRSF1A | TNFRSF1A | Mixscale_CRISPRi | 0.9683862679530189 | 0.305972733625738 | 0.6624135343272808 | 0.6211601610564657 | 6 | 6.7789663484812515 | MS_directionally_unsafe_TNF_axis | NO_GO_WAVE61_GUARDRAIL |
| real_direct_perturbation | RFX5 | RFX5 | Mixscale_CRISPRi | 0.5517938735080701 | 0.0 | 0.5517938735080701 | 0.5231987939104686 | 4 | 6.313393270463303 | nonselective_MHCII_host_defense | NO_GO_WAVE61_GUARDRAIL |
| real_direct_perturbation | ruxolitinib | RUXOLITINIB | human_macrophage_RNAseq_descriptive | 1.0198365329867134 | 3.245924547797378 | -2.2260880148106645 | -2.261522305659348 | 3 | 5.019836532986713 |  | NO_GO_WAVE61_GUARDRAIL |
| real_direct_perturbation | ruxolitinib | RUXOLITINIB | human_macrophage_RNAseq_descriptive | 0.9913150391191098 | 3.735873527849472 | -2.744558488730362 | -2.7580832665045834 | 3 | 4.99131503911911 |  | NO_GO_WAVE61_GUARDRAIL |
| real_direct_perturbation | ruxolitinib | RUXOLITINIB | human_macrophage_RNAseq_descriptive | 0.9468639501073736 | 4.099711571915987 | -3.152847621808613 | -3.16990119272749 | 3 | 4.946863950107374 |  | NO_GO_WAVE61_GUARDRAIL |
| real_direct_perturbation | ruxolitinib | RUXOLITINIB | human_macrophage_RNAseq_descriptive | 0.7613338105220838 | 3.349528138153343 | -2.588194327631259 | -2.632783417380891 | 3 | 4.761333810522084 |  | NO_GO_WAVE61_GUARDRAIL |
| real_direct_perturbation | STAT2 | STAT2 | Mixscale_CRISPRi | 0.7054128313832698 | 1.314542040638374 | -0.609129209255104 | -0.6135408238992132 | 5 | 4.70541283138327 |  | NO_GO_WAVE61_GUARDRAIL |
| real_direct_perturbation | IFNAR2 | IFNAR2 | Mixscale_CRISPRi | 0.6611289298703412 | 1.1205011385471957 | -0.4593722086768544 | -0.5097787971595411 | 5 | 4.661128929870341 |  | NO_GO_WAVE61_GUARDRAIL |
| real_direct_perturbation | CHUK | CHUK | Mixscale_CRISPRi | 0.672021576511123 | 0.269125495016825 | 0.402896081494298 | 0.3353338408117842 | 4 | 4.339688496917016 | broad_NFKB_host_defense | NO_GO_WAVE61_GUARDRAIL |
| real_direct_perturbation | Gsk3b_KO_unstimulated | GSK3B_KO_UNSTIMULATED | mouse_macrophage_RNAseq | 0.2667613312426131 | 0.4713951094410252 | -0.2046337781984121 | -0.2072887748916699 | 4 | 3.766761331242613 |  | NO_GO_WAVE61_GUARDRAIL |

## Efferocytosis Negative-Regulator Reopener Scan

| gene | median_efficient_minus_noneater_lfc | positive_disease_count | ms_wm_delta_log2 | ms_wm_p | residual_retained_disease_count | gwas_catalog_trait_count | chembl_target_id | reopener_score | reopener_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FAM49B | 0.7903403938506244 | 3.0 | 0.1048061004481475 | 0.3462797066387407 | 0.0 | 1.0 |  | 3.2903403938506246 | NO_GO_EFFEROCYTOSIS_ONLY |
| EFR3A | 0.8947628318325367 | 1.0 | 0.2644865146297235 | 0.0409895429330483 | 0.0 | 1.0 |  | 2.8947628318325367 | NO_GO_EFFEROCYTOSIS_ONLY |
| DAB2 | 0.6555390813258746 | 0.0 | 0.5378984279794476 | 0.0111306912319104 | 0.0 | 1.0 |  | 2.6555390813258746 | NO_GO_EFFEROCYTOSIS_ONLY |
| NFKBIZ | 0.6299464031376492 | 2.0 | 0.0370507959818766 | 0.8969292908307444 | 0.0 | 5.0 |  | 2.629946403137649 | NO_GO_EFFEROCYTOSIS_ONLY |
| EVI5 | 0.3926431387598291 | 1.0 | 0.0549982494341865 | 0.7772798209915935 | 0.0 | 5.0 |  | 2.392643138759829 | NO_GO_EFFEROCYTOSIS_ONLY |
| BLK | 0.3763039238517932 | 1.0 | 0.0 | 1.0 | 0.0 | 10.0 |  | 2.3763039238517933 | NO_GO_EFFEROCYTOSIS_ONLY |
| MYNN | 0.294948291238398 | 0.0 | -0.1030849512065348 | 0.6037675722433599 | 0.0 | 4.0 |  | 2.294948291238398 | NO_GO_EFFEROCYTOSIS_ONLY |
| TSC1 | 1.1788476545613715 | 0.0 | 0.0364246955213065 | 0.7995019245596273 | 0.0 | 1.0 |  | 2.1788476545613715 | NO_GO_EFFEROCYTOSIS_ONLY |
| CLEC7A | 0.6670469582228472 | 3.0 | -0.3549463925802421 | 0.128706751389563 | 0.0 | 0.0 |  | 2.1670469582228473 | NO_GO_EFFEROCYTOSIS_ONLY |
| NDUFV3 | 0.5493777324277445 | 3.0 | -0.3460232445599303 | 0.0754322654204795 | 0.0 | 0.0 |  | 2.0493777324277445 | NO_GO_EFFEROCYTOSIS_ONLY |
| MMS22L | 1.041004774142687 | 1.0 | -0.3694222186304907 | 0.6584127480472038 | 0.0 | 1.0 |  | 2.041004774142687 | NO_GO_EFFEROCYTOSIS_ONLY |
| STARD5 | 0.4749259401880717 | 3.0 | 0.3405236664023316 | 0.2090343477941671 | 0.0 | 0.0 |  | 1.9749259401880717 | NO_GO_EFFEROCYTOSIS_ONLY |

## Summary JSON

```json
{
  "inputs": {
    "broad_h5ad": "results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv",
    "broad_residual": "results_v3/broad_residual_gate/broad_residual_gate_summary.tsv",
    "wave15_direct": "results_v3/wave15_perturbation_drug_response/ranked_direct_perturbations.tsv",
    "wave15_synthesis": "results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv",
    "wave24_l1000": "results_v3/wave24_l1000_recurrent_reversal/recurrent_l1000_compound_triage.tsv",
    "wave24_mechanisms": "results_v3/wave24_l1000_recurrent_reversal/recurrent_l1000_mechanism_summary.tsv",
    "wave27_unknown": "results_v3/wave27_l1000_unknown_deconvolution/unknown_l1000_deconvolution.tsv",
    "wave34": "results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv",
    "wave35_contrasts": "results_v3/wave35_resolution_perturbation/contrast_level_calls.tsv",
    "wave37_efferocytosis": "results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv",
    "wave53_decision": "results_v3/wave53_perturbation_first_pivot/decision_matrix.tsv",
    "wave55": "results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv",
    "wave57_calls": "results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv"
  },
  "interpretation": "Intervention-level triage only. No candidate is promoted without real perturbation, guardrails, translational feasibility, and prior-art clearance.",
  "n_direct_perturbation_rows": 186,
  "n_evidence_rows": 395,
  "n_l1000_rows": 180,
  "n_resolution_rows": 29,
  "promotion_candidates": [],
  "reopened_candidates": [],
  "seed": 20260527,
  "top_direct_candidates": [
    "Med16_KO",
    "Gsk3b_KO",
    "TNFRSF1A",
    "RFX5",
    "ruxolitinib",
    "ruxolitinib",
    "ruxolitinib",
    "ruxolitinib",
    "STAT2",
    "IFNAR2"
  ],
  "top_efferocytosis_reopeners": [
    "FAM49B",
    "EFR3A",
    "DAB2",
    "NFKBIZ",
    "EVI5",
    "BLK",
    "MYNN",
    "TSC1",
    "CLEC7A",
    "NDUFV3"
  ]
}
```

## Guardrail

No route from this wave is a therapeutic claim unless subagent prior-art and translational audits agree. The output is an intervention triage layer for the continuing V3 session.
