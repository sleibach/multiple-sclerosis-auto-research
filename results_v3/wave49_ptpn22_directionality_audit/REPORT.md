# Wave49 PTPN22 Directionality Audit

Random seed: `20260527`.

## Verdict

`PTPN22`: `NO_GO_BROAD_GENETICS_WITH_UNRESOLVED_DIRECTION_AND_SELECTIVITY`.

PTPN22 has broad autoimmune GWAS evidence (28 traits, min p=4.999999999999999e-174) and ChEMBL chemical matter (100 nM activity rows, best nM=270.0), but the V3-promotable claim fails because target-resolved direction, strict MS anchoring, disease-cell perturbation, phosphatase selectivity, and novelty are not established.

Primary blocker: Broad genetics does not specify a disease-safe intervention direction. Available chemistry is inhibitor-skewed and selectivity over related phosphatases is not proven; local cell-state support is narrow and MS support is nominal rather than FDR-supported.

Decisive reopen test: Allele-stratified primary human T cell, B cell, and myeloid assays from RA/T1D/SLE/MS donors, comparing selective PTPN22 inhibition or restoration/editing with on-target phosphatase rescue, plus coloc/MR resolving risk-allele direction.

## Gate Matrix

- `cross_autoimmune_genetic_breadth`: PASS (`28; min_p=4.999999999999999e-174`) - requires many autoimmune GWAS traits.
- `target_resolved_direction`: FAIL (`not_run/no_coloc_or_MR`) - requires target-resolved coloc/MR and allele-to-function direction.
- `strict_ms_anchor`: FAIL (`ms_gwas=False; delta=0.81950776939291; p=0.0313351961928456; fdr=0.8506970233122761`) - requires MS genetics or FDR-supported MS state evidence.
- `cross_disease_cell_state_support`: FAIL (`local_positive=1.0; residual_positive=0.0`) - requires expression/state support beyond genetics.
- `disease_relevant_perturbation_anchor`: FAIL (`absent`) - requires PTPN22 perturbation in relevant disease cells with rescue readout.
- `chemical_matter_exists`: PASS (`activity_rows=100; best_nM=270.0`) - requires tractable chemistry.
- `phosphatase_selectivity_established`: FAIL (`min_offtarget_over_ptpn22_ratio=0.4173076923076923`) - requires evidence top molecules are selective over close phosphatases.
- `disease_safe_modulation_direction`: FAIL (`conflicted_inhibition_vs_restoration`) - requires a safe direction for R620W-like risk biology.
- `novelty_prior_art_not_blocking`: FAIL (`EuropePMC_max=658; ClinicalTrials_max=5`) - requires not being a crowded autoimmune target/modality route.

## Public Source Snapshot

- EuropePMC `PTPN22 R620W gain loss function autoimmune directionality`: count=2; top hits: 38915894: Based on systematic druggable genome-wide Mendelian randomization identifies therapeutic targets for diabetes. (2024) | 27807193: PTPN22 Is a Critical Regulator of Fcγ Receptor-Mediated Neutrophil Activation. (2016)
- EuropePMC `PTPN22 inhibitor autoimmune disease rheumatoid lupus type 1 diabetes`: count=454; top hits: 41064203: Immune System-Related Genetic Risk Factors for Inhibitory Antibody Development in Patients With Hemophilia: Reviewing an Old Problem From a New Perspective-A Narrative Review. (2025) | 41703739: Neutrophil extracellular traps in rheumatoid arthritis: biomarkers, drivers, and emerging therapeutic targets. (2026) | 41208109: Type I interferon production in myeloid cells is regulated by factors independent of Ptpn22. (2025) | 40839671: Integrative molecular network analysis of genetic risk factors to infer biomarkers and therapeutic targets for rheumatoid arthritis. (2025) | 39944077: Protein phosphatases in systemic autoimmunity. (2025)
- EuropePMC `PTPN22 multiple sclerosis genetics immune cells`: count=658; top hits: 41757875: Clinical, serological, and targeted genetic analysis of systemic lupus erythematosus in Kazakhstan. (2026) | 41136183: First genome-wide association study reveals immune-mediated aetiopathology in idiopathic achalasia. (2025) | 41283471: Systemic Sclerosis in Kazakh Patients: A Preliminary Case-Control Immunogenetic Profiling Study. (2025) | 39796280: Whole-Exome Sequencing: Discovering Genetic Causes of Granulomatous Mastitis. (2025) | 40839671: Integrative molecular network analysis of genetic risk factors to infer biomarkers and therapeutic targets for rheumatoid arthritis. (2025)
- EuropePMC `PTPN22 inhibitor selectivity phosphatase autoimmune`: count=131; top hits: 41585704: Targeting PTPN22 at Nonorthosteric Binding SitesA Fragment Approach. (2026) | 41454526: Discovery of a First-in-Class Covalent Allosteric SHP1 Inhibitor with Immunotherapeutic Activity. (2026) | 41465179: Insights into the Genetic and Epigenetic Landscape of Endocrine Autoimmunity: A Systematic Review. (2025) | 39693863: Structure-activity relationship studies and design of a PTPN22 inhibitor with enhanced isozyme selectivity and cellular efficacy. (2025) | 39461876: Dendritic cell-intrinsic PTPN22 negatively regulates antitumor immunity and impacts anti-PD-L1 efficacy. (2024)
- ClinicalTrials.gov `PTPN22 autoimmune`: count=5; top hits: NCT01276743: Study of PTPN22 C1858T Polymorphism in Children and Adolescents of Greek Origin With T1DM [; COMPLETED] | NCT07510750: rT3 and Inflammation in Hashimoto's Thyroiditis [; COMPLETED] | NCT04139369: Methylation of DNA in Children and Adolescents With Type 1 Diabetes Mellitus (METHYLDIAB) [; COMPLETED] | NCT00958113: Autoimmune Thyroid Disease Genetic Study [; COMPLETED] | NCT03988764: Monogenic Diabetes Misdiagnosed as Type 1 [; RECRUITING]
- ClinicalTrials.gov `PTPN22 inhibitor`: count=0; top hits: 
