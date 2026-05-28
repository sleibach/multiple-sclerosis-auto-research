# Wave62 Open Targets Target-Resolution Audit

Random seed: `20260527`.

## Verdict

- Reopen calls: `0`.
- Park calls: `32`.
- No output is a therapeutic claim; target resolution still requires intervention, safety, and prior-art validation.

## Top Target-Resolution Rows

| gene | wave62_call | wave62_score | manual_blocker | prior_context_blocker | max_l2g_score | best_l2g_disease | strong_l2g_disease_count | strong_l2g_diseases | ms_max_l2g_score | ms_max_relevant_qtl_h4 | ms_relevant_qtl_biosamples | local_positive_disease_count | residual_retained_disease_count | wave61_best_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RGS1 | PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW | 6.883494989496564 |  |  | 0.8937927484512329 | T1D | 4 | Celiac;MS;Psoriasis;T1D | 0.884235680103302 | 0.9856571406462533 | B cell;CD14-low, CD16-positive monocyte;CD14-positive, CD16-negative classical monocyte;macrophage;neutrophil | 1.0 | 0.0 |  |
| INAVA | PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW | 6.872153629325313 |  |  | 0.8847459554672241 | UC | 4 | AS;Crohn;MS;UC | 0.6894342303276062 | 0.9828462411264802 | skin of body;suprapubic skin | 1.0 | 0.0 |  |
| ANKRD55 | PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW | 6.823852360248566 |  |  | 0.8238523602485657 | RA | 4 | Crohn;MS;RA;T1D | 0.7806254625320435 | 0.9983304925105229 | CD4-positive, alpha-beta T cell;naive regulatory T cell | 0.0 | 0.0 |  |
| IL7R | PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW | 6.446508829028122 | prior_art_CD127_autoimmune_axis |  | 0.9528712630271912 | PBC | 4 | Crohn;MS;PBC;T1D | 0.9447864890098572 | 0.9844688660839737 | CD14-positive, CD16-negative classical monocyte;CD4-positive, alpha-beta T cell;blood;fibroblast;macrophage | 3.0 | 2.0 |  |
| SP140 | PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW | 6.36468645455028 |  |  | 0.8754889965057373 | MS | 3 | Crohn;MS;Psoriasis | 0.8754889965057373 | 0.9868116204726999 | CD14-positive, CD16-negative classical monocyte;T cell;blood;lymphoblastoid cell line;naive regulatory T cell;transverse colon | 4.0 | 1.0 |  |
| GALC | PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW | 6.189795435748273 |  |  | 0.7024610638618469 | MS | 2 | Crohn;MS | 0.7024610638618469 | 0.9873343718864264 | CD14-positive, CD16-negative classical monocyte;fibroblast;neutrophil;thyroid gland | 3.0 | 0.0 |  |
| IL2RA | PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW | 4.443186856221253 | CD25_IL2_axis_prior_art_directionality | prior_branch_blocker_or_directionality_unresolved | 0.9520419239997864 | RA | 5 | Crohn;MS;Psoriasis;RA;T1D | 0.8340961933135986 | 0.8424868378351196 | lymphoblastoid cell line | 0.0 | 0.0 |  |
| STAT4 | PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW | 4.377520842140743 | STAT4_TF_not_selectively_druggable | prior_branch_blocker_or_directionality_unresolved | 0.8833943605422974 | RA | 8 | Celiac;Crohn;MS;PBC;RA;SLE;Sjogren;T1D | 0.845672070980072 | 0.955404271318453 | CD14-positive, CD16-negative classical monocyte;CD4-positive, alpha-beta T cell;CD8-positive, alpha-beta T cell;T-helper 17 cell;blood;fibroblast;macrophage;naive regulatory T cell;right lobe of liver;transverse colon | 2.0 | 0.0 | NO_GO_WAVE61_GUARDRAIL |
| PTGER4 | PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW | 4.24586032993851 | EP4_directionality_prior_art_conflicted | prior_branch_blocker_or_directionality_unresolved | 0.7531872987747192 | T1D | 5 | Crohn;MS;Psoriasis;T1D;UC | 0.5558526515960693 | 0.9291922636901229 | CD4-positive, alpha-beta T cell;central memory CD4-positive, alpha-beta T cell | 2.0 | 0.0 |  |
| MMEL1 | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE | 5.329183466048283 |  |  | 0.8332656621932983 | MS | 2 | Celiac;MS | 0.8332656621932983 | 0.9565789491198184 | CD14-positive, CD16-negative classical monocyte;CD4-positive, alpha-beta T cell;CD8-positive, alpha-beta T cell;blood;spleen;thyroid gland | 1.0 | 0.0 |  |
| RGS14 | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE | 5.299052728193885 |  |  | 0.8030093312263489 | MS | 3 | Crohn;MS;Psoriasis | 0.8030093312263489 | 0.9952074420704351 | T cell;dorsolateral prefrontal cortex;right lobe of liver;skin of body;spleen;suprapubic skin;transverse colon | 1.0 | 0.0 |  |
| RMI2 | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE | 5.2866275933786335 |  |  | 0.7914115786552429 | MS | 2 | MS;T1D | 0.7914115786552429 | 0.9780145044618388 | dorsolateral prefrontal cortex;fibroblast;lymphoblastoid cell line | 0.0 | 0.0 |  |
| ZC2HC1A | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE | 5.24743070728794 |  |  | 0.8042101263999939 | MS | 2 | MS;Psoriasis | 0.8042101263999939 | 0.9404102247449961 | blood;lymphoblastoid cell line;skin of body | 0.0 | 0.0 |  |
| GPR65 | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE | 4.2649283939359135 |  | prior_branch_blocker_or_directionality_unresolved | 0.7826091051101685 | AS | 2 | AS;MS | 0.6238155364990234 | 0.982319288825745 | fibroblast | 1.0 | 0.0 |  |
| TNFRSF1A | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE | 3.953750382123653 | TNF_axis_prior_art_and_MS_paradox_risk |  | 0.9539542198181152 | MS | 3 | AS;MS;PBC | 0.9539542198181152 | 0.999796162305538 | CD14-low, CD16-positive monocyte;CD14-positive, CD16-negative classical monocyte;anterior cingulate cortex;blood;dorsolateral prefrontal cortex;fibroblast;macrophage;neutrophil;right lobe of liver;sigmoid colon;skin of body;spleen;suprapubic skin;thyroid gland;transverse colon | 0.0 | 0.0 | NO_GO_WAVE61_GUARDRAIL |
| CD58 | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE | 3.448185430270665 |  |  | 0.9513845443725586 | MS | 1 | MS | 0.9513845443725586 | 0.9944626523267263 | CD14-positive, CD16-negative classical monocyte;blood plasma;lymphoblastoid cell line | 3.0 | 0.0 |  |
| CD86 | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE | 2.4702414870262146 |  |  | 0.9702414870262146 | MS | 1 | MS | 0.9702414870262146 | 0.9982892957376484 | B cell;CD14-positive, CD16-negative classical monocyte;blood plasma;lymphoblastoid cell line | 0.0 | 0.0 |  |
| CD5 | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE | 2.3979762344117934 |  |  | 0.9009516835212708 | MS | 1 | MS | 0.9009516835212708 | 0.9970245508905227 | CD8-positive, alpha-beta T cell;blood plasma | 0.0 | 0.0 |  |
| CYP24A1 | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE | 2.3913259255163437 |  |  | 0.8928307294845581 | MS | 1 | MS | 0.8928307294845581 | 0.9984951960317858 | anterior cingulate cortex;dorsolateral prefrontal cortex;frontal cortex | 1.0 | 0.0 |  |
| MAPK3 | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE | 2.3656849056083527 |  |  | 0.8696510791778564 | MS | 1 | MS | 0.8696510791778564 | 0.9957851255480086 | B cell;CD14-positive, CD16-negative classical monocyte;blood;blood plasma;dorsolateral prefrontal cortex;frontal cortex | 1.0 | 0.0 |  |

## Summary JSON

```json
{
  "caps": {
    "coloc_page_size": 25,
    "l2g_page_size": 10,
    "max_credible_sets_per_study": 250,
    "max_studies_per_disease": 60
  },
  "diseases": {
    "AITD": "EFO_0006812",
    "AS": "EFO_0003898",
    "Celiac": "EFO_0001060",
    "Crohn": "EFO_0000384",
    "MS": "MONDO_0005301",
    "PBC": "EFO_1001486",
    "Psoriasis": "EFO_0000676",
    "RA": "EFO_0000685",
    "SLE": "MONDO_0007915",
    "Sjogren": "EFO_0000699",
    "T1D": "MONDO_0005147",
    "UC": "EFO_0000729"
  },
  "inputs": {
    "broad_h5ad": "results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv",
    "broad_residual": "results_v3/broad_residual_gate/broad_residual_gate_summary.tsv",
    "wave34": "results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv",
    "wave34a": "results_v3/wave34a_genetics_first_target_rescue/genetics_first_candidate_rank.tsv",
    "wave55": "results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv",
    "wave61": "results_v3/wave61_perturbation_first_guardrail/intervention_evidence_tiers.tsv"
  },
  "interpretation": "Target-resolution triage only. L2G/QTL colocalisation is not therapeutic causality.",
  "n_credible_sets": 2506,
  "n_eligible_gwas_studies": 95,
  "n_l2g_rows": 4821,
  "n_qtl_coloc_rows": 16823,
  "n_study_rows": 539,
  "n_targets": 2028,
  "park_count": 32,
  "reopen_count": 0,
  "seed": 20260527,
  "top_targets": [
    "RGS1",
    "INAVA",
    "ANKRD55",
    "IL7R",
    "SP140",
    "GALC",
    "IL2RA",
    "STAT4",
    "PTGER4",
    "MMEL1",
    "RGS14",
    "RMI2",
    "ZC2HC1A",
    "GPR65",
    "TNFRSF1A"
  ]
}
```

## Guardrail

Open Targets L2G plus QTL colocalisation can prioritize a target but does not prove therapeutic causality. HLA/antigen-processing rows require especially strict intervention and host-defense review.
