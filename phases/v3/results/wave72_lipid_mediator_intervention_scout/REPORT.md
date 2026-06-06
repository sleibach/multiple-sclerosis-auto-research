# Wave72 Lipid-Mediator Intervention Scout

## Question

Do the Wave71-C biochemical intervention routes (`NAAA`, `EPHX2`, `GPR183`, `P2RX7`) survive a real public metabolomics/lipidomics fail-fast when joined to local V3 gene-level evidence?

## Verdict

No branch is promoted. The strongest orthogonal signal is biochemical-class level, not target-level. `P2RX7` has broad purine-class disturbance but this is nonspecific; `EPHX2` has scattered DiHOME/eicosanoid rows but no replicated EpFA:diol ratio; `NAAA` substrates are essentially absent from the available feature panels; `GPR183` oxysterol evidence is sparse.

## Branch Decisions

| branch | gene | wave72_call | gate_count | biochemical_supportive_disease_count | normalizing_treatment_hit_count | local_positive_disease_count | local_negative_disease_count | genetic_anchor_count | geneformer_support_contexts | ms_foamy_proteome_pass | decisive_blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NAAA_lipid_amide_preservation | NAAA | NO_GO_WAVE72 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | False | biochemical feature support is absent or underpowered |
| EPHX2_sEH_oxylipin_diol | EPHX2 | PARK_ORTHOGONAL_BIOCHEMICAL_SCOUT | 1 | 2 | 1 | 0 | 2 | 0 | 0 | False | biochemical pattern lacks target-level gene convergence |
| GPR183_oxysterol_gradient | GPR183 | NO_GO_WAVE72 | 0 | 1 | 0 | 2 | 1 | 1 | 0 | False | biochemical feature support is absent or underpowered |
| P2RX7_purinergic_inflammasome | P2RX7 | PARK_ORTHOGONAL_BIOCHEMICAL_SCOUT | 2 | 5 | 4 | 1 | 1 | 0 | 0 | False | biochemical pattern lacks target-level gene convergence |

## Biochemical Feature Summary

| branch | gene | intervention | feature_match_count | disease_like_match_count | treatment_like_match_count | supportive_disease_count | supportive_diseases | supportive_feature_count | normalizing_treatment_hit_count | normalizing_treatment_hits | fdr10_feature_count | best_nominal_feature | support_logic | manual_blocker | biochemical_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NAAA_lipid_amide_preservation | NAAA | NAAA inhibition to preserve PEA/OEA-like N-acylethanolamide tone | 1 | 1 | 0 | 0 |  | 0 | 0 |  | 0 | ST000422\|T1D\|T1D_vs_control\|Anandamide-O-phosphate\|g=0.131\|p=0.428\|fdr=0.659 | substrates lower in disease/worse state and higher after improvement | requires direct PEA/OEA depletion or NAAA activity evidence; transcript recurrence alone is weak | NO_GO_INSUFFICIENT_BIOCHEMICAL_SUPPORT |
| EPHX2_sEH_oxylipin_diol | EPHX2 | soluble epoxide hydrolase inhibition to reduce inflammatory diols and preserve epoxy-fatty acids | 19 | 14 | 5 | 2 | MS_model;UC | 3 | 1 | ST002470:UC_week12_inactive_vs_week0_modsev:9,10-DiHOME | 3 | ST003328\|MS_model\|PMS_untreated_vs_AMC_untreated\|Eicosatrienoic acid\|g=3.82\|p=3.87e-06\|fdr=5.65e-05 | diol/oxylipin branch higher in disease/worse state and lower after improvement | requires real EpFA:diol ratios; transcript/protein EPHX2 is not sufficient | PARK_BIOCHEMICAL_PATTERN_INSUFFICIENT_FOR_TARGET |
| GPR183_oxysterol_gradient | GPR183 | GPR183/EBI2 antagonism or spatial modulation of oxysterol-driven inflammatory niches | 25 | 25 | 0 | 1 | T1D | 3 | 0 |  | 2 | ST000422\|T1D\|T1D_vs_control\|24,24-Difluoro-25-hydroxy-26,27-dimethylvitamin D3\|g=0.644\|p=0.000555\|fdr=0.0436 | oxysterol-gradient metabolites higher in disease/worse state and lower after improvement | direction is niche-dependent and needs spatial cell-state support | NO_GO_INSUFFICIENT_BIOCHEMICAL_SUPPORT |
| P2RX7_purinergic_inflammasome | P2RX7 | P2RX7 antagonism in purine/inflammasome-high myeloid disease states | 162 | 126 | 36 | 5 | AS;Crohn;RA;T1D;UC | 12 | 4 | ST002470:UC_week12_inactive_vs_week0_modsev:Hypoxanthine;ST002470:UC_week12_inactive_vs_week0_modsev:Inosine;ST002470:UC_week12_inactive_vs_week0_modsev:Xanthine;ST002470:UC_week12_inactive_vs_week0_modsev:1-Methyladenosine | 23 | ST002949\|AS\|AS_vs_control\|Hypoxanthine\|g=1.97\|p=2.75e-16\|fdr=1.43e-15 | purine danger/turnover metabolites higher in disease/worse state and lower after improvement | purine metabolomics is nonspecific unless linked to P2RX7/IL1B/NLRP3 cell state | REOPEN_BIOCHEMICAL_SCOUT_NEEDS_GENE_LEVEL_VALIDATION |

## Gene-Level Evidence

| gene | broad_positive_disease_count | broad_negative_disease_count | broad_positive_diseases | broad_negative_diseases | broad_best_positive_fdr | broad_in_lipid_lysosomal_neighborhood | wave62_score | wave62_call | wave62_strong_l2g_disease_count | wave62_strong_qtl_coloc_disease_count | wave62_ms_max_relevant_qtl_h4 | geneformer_wave57_call | geneformer_support_contexts | geneformer_strong_support_contexts | geneformer_model_priority_score | gse282122_best_cell_state | gse282122_raw_p | gse282122_raw_fdr | gse282122_paired_fdr | gse282122_integrated_score | gse282122_wave68_call | ms_foamy_proteome_passes_convergence_gate | ms_foamy_proteome_mean_delta | ms_foamy_proteome_gee_p | ms_foamy_proteome_fdr_bh |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NAAA | 0 | 2 |  | Crohn disease;ulcerative colitis |  | False |  |  |  |  |  |  |  |  |  | DC | 0.1697393038829068 | 1.0 | 1.0 | 1.1483847029518686 | DESCRIPTIVE_GENE_SIGNAL | False | 0.0051191905402183 | 9.01294688709173e-05 | 0.0021067764938539 |
| EPHX2 | 0 | 2 |  | psoriasis;ulcerative colitis |  | False |  |  |  |  |  |  |  |  |  | Mono_macro | 0.1201218220122457 | 1.0 | 1.0 | 1.5020860823690692 | DESCRIPTIVE_GENE_SIGNAL | False | 0.0060246673286895 | 0.745069182891662 | 0.891672336635959 |
| GPR183 | 2 | 1 | Crohn disease;Sjogren syndrome | psoriasis | 0.2452077373699298 | False | 1.240930199623108 | NO_GO_WAVE62_TARGET_RESOLUTION | 1.0 | 0.0 | 0.0 |  |  |  |  | DC | 0.0822992639831455 | 1.0 | 1.0 | 2.147547758438998 | DESCRIPTIVE_GENE_SIGNAL |  |  |  |  |
| P2RX7 | 1 | 1 | type 1 diabetes mellitus | ulcerative colitis | 0.3568862161623112 | False |  |  |  |  |  |  |  |  |  | DC | 0.2961735891453396 | 1.0 | 1.0 | 1.741681531856015 | DESCRIPTIVE_GENE_SIGNAL | False | 0.0143660847536592 | 0.0204897929317287 | 0.1044200208244 |
| MFGE8 | 1 | 0 | type 1 diabetes mellitus |  | 0.2033207085232548 | False |  |  |  |  |  |  |  |  |  | Mono_macro | 0.0022612143547957 | 0.5984736235424485 | 1.0 | 2.948815730947822 | DESCRIPTIVE_GENE_SIGNAL |  |  |  |  |
| GPR65 | 1 | 2 | Sjogren syndrome | type 1 diabetes mellitus;ulcerative colitis | 0.8441184433525579 | False | 4.2649283939359135 | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE | 2.0 | 1.0 | 0.982319288825745 |  |  |  |  | DC | 0.0321767641410888 | 1.0 | 1.0 | 2.887984173899131 | DESCRIPTIVE_GENE_SIGNAL |  |  |  |  |
| SLC15A4 | 1 | 0 | Crohn disease |  | 0.2122184894027283 | False | 2.382724674313512 | NO_GO_WAVE62_TARGET_RESOLUTION | 1.0 | 1.0 | 0.0 |  |  |  |  | Mono_macro | 0.0269938464341292 | 0.8488954332555355 | 1.0 | 2.8059017297066005 | DESCRIPTIVE_GENE_SIGNAL |  |  |  |  |

## Purine Class Context

```json
{
  "purine_best_rows": [
    {
      "contrast": "AS_vs_control",
      "disease": "AS",
      "fdr_within_study_contrast": 1.233745055517054e-06,
      "hedges_g_case_minus_control": 0.6745869171914296,
      "p": 4.6265439581889524e-07,
      "study_id": "ST002949"
    },
    {
      "contrast": "Crohn_vs_control",
      "disease": "Crohn",
      "fdr_within_study_contrast": 0.0768666627738789,
      "hedges_g_case_minus_control": -0.6278026303099806,
      "p": 0.0499633308030213,
      "study_id": "ST000899"
    },
    {
      "contrast": "UC_vs_control",
      "disease": "UC",
      "fdr_within_study_contrast": 0.5693528515674731,
      "hedges_g_case_minus_control": -0.2420640357399322,
      "p": 0.4396948269903085,
      "study_id": "ST000899"
    },
    {
      "contrast": "T1D_vs_control",
      "disease": "T1D",
      "fdr_within_study_contrast": 0.7059855255965622,
      "hedges_g_case_minus_control": 0.0825454481276034,
      "p": 0.580044328074991,
      "study_id": "ST000422"
    },
    {
      "contrast": "UC_week0_modsev_vs_mild",
      "disease": "UC",
      "fdr_within_study_contrast": 0.8854433823141206,
      "hedges_g_case_minus_control": -0.0494829631181484,
      "p": 0.8854433823141206,
      "study_id": "ST002470"
    }
  ],
  "purine_class_rows": 8,
  "purine_normalizing_treatment_rows": 0,
  "purine_supportive_disease_count": 1,
  "purine_supportive_diseases": "AS"
}
```

## Interpretation

- This wave answers Wave71-C's strongest new computational test with existing public data.
- Available metabolomics panels are not rich enough in PEA/OEA, EpFA:diol pairs, or GPR183 oxysterols to support a target claim.
- `P2RX7` remains a possible stratification concept only if future baseline ATP/purine plus `IL1B/NLRP3` cell-state data can identify a responder subset; current data are too nonspecific.
