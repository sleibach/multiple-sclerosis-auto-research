# Wave 4 Residual CD74/HLA Receptor-State Scout Report

## Bottom line

The IFN-residual `mif_cd74_receptor_state` signal should **not** be advanced as a V3 central cross-autoimmune mechanism. It is best treated as a **stratification and pharmacodynamic biomarker** for a tissue-resident APC-like state, especially in MS white-matter microglia and possibly Sjogren salivary epithelium. The cross-disease raw recurrence is real, but the signal mostly collapses when controlled against same-sample `ifn_apc`; T1D ductal/acinar support is raw IFN/HLA/CD74 recurrence, not residual CD74/HLA receptor-state biology. Direct CD74/MIF, anti-CD74, CIITA/MHC-II-gate, CTSS, PDE4/cAMP, and MIF-blocking approaches all have either heavy prior art, broad biology, weak druggability, or weak current in-silico reversal support.

Recommendation: **biomarker-only demotion** unless a component-level residual analysis and a target-cell perturbation experiment show that CD74/CD44/CXCR4 or HLA-II/CD74 remains disease-informative and drug-modulable after generic IFN and tissue-inflammation controls.

## Residual evidence

Source files read:

- `CRITIQUE_V3.md`
- `LAB_NOTEBOOK_V3.md`
- `ORCHESTRATION_LOG_V3.md`
- `results_v3/residualization/ifn_residualization_summary.json`
- `results_v3/residualization/ifn_residualization_module_tests.tsv`
- `results_v3/cross_disease_convergence_summary.json`
- `subagents_v3/intervention_scout_report.md`

Global residualization result:

- Input units: 217 donor/sample units.
- Tests: 56 target-module contrasts.
- Raw nominal positive tests: 30.
- IFN-residual nominal positive tests: 4.
- No residual test survives global residual FDR.
- Residual support by disease: MS (`mif_cd74_receptor_state`, `lysosomal_apc`), Sjogren (`mif_cd74_receptor_state`), T1D (`mixscale_validated_ifng_readout`, not `mif_cd74_receptor_state`).

MS white-matter microglia:

- Dataset/compartment: `GSE111972_white_matter`, sorted bulk microglia.
- `mif_cd74_receptor_state` raw: n=10 MS, n=11 control; delta=0.614; Hedges g=1.341; p=0.00547; raw FDR=0.0388.
- IFN-residual: delta=0.456; Hedges g=1.248; p=0.00789; residual FDR=0.442.
- Target-vs-IFN R2=0.394, so this is the cleanest residual signal in the current package.
- Component audit weakens a literal CD74 claim: in MS white matter, CD74 alone is not significant (delta_log2=0.255, p=0.219, FDR=0.437). The module is driven by a composite of HLA-DP/DR plus CD44/CXCR4 and CD74, not by CD74 alone. HLA-DPA1 is the strongest component by nominal p (p=0.0135, FDR=0.197); CD44 is nominal (p=0.0332, FDR=0.208); CXCR4 has an adjusted disease beta p=0.0447 but unadjusted contrast p=0.318.

Sjogren salivary epithelial:

- Dataset/compartment: `sjogren_gland_epithelial`, single-cell/single-nucleus donor-level h5ad.
- `mif_cd74_receptor_state` raw: n=11 Sjogren, n=14 control; delta=0.207; Hedges g=1.075; p=0.0207; raw FDR=0.0682.
- IFN-residual: delta=0.0447; Hedges g=0.683; p=0.0734; residual FDR=0.974.
- Target-vs-IFN R2=0.902. Interpretation: nearly all disease separation is generic IFN/HLA/APC intensity. This is weak residual support.
- Component audit: epithelial CD74 mean-z is nominally high (delta=0.362, p=0.00173) but broad tracked-gene FDR is 0.175. HLA-DRA/HLA-DRB1 are nominal-to-trend only; CD44 is lower in cases. This fits an epithelial HLA/CD74 activation marker, not a specific CD74 receptor mechanism.

T1D ductal/acinar:

- `t1d_ductal_cell` `mif_cd74_receptor_state` raw: n=5 T1D, n=19 control; delta=0.172; Hedges g=1.142; p=0.00364; raw FDR=0.0388 in residualization table and FDR=0.0482 in direct h5ad module table.
- `t1d_ductal_cell` IFN-residual: delta=-0.0060; Hedges g=-0.077; p=0.864; residual FDR=0.993. This falsifies residual CD74/HLA receptor-state support in T1D ductal cells under the current model.
- `t1d_acinar_cell` `mif_cd74_receptor_state` raw: delta=0.0813; Hedges g=0.600; p=0.0803; residual delta=-0.0328; p=0.518.
- T1D acinar has nominal residual support for `mixscale_validated_ifng_readout` (residual p=0.0821), but that is not the CD74/HLA receptor-state module.
- Component audit: ductal CD74 mean-z is strongly nominal (delta=0.544, p=0.000375), but broad gene-panel FDR remains 0.175. This should be treated as a raw CD74-expression observation that is mostly explained by IFN/APC state.

Cross-disease raw convergence:

- `mif_cd74_receptor_state` is the top raw breadth module: tested in 8 diseases, strong in 3, supportive-or-strong in 6, no negative-trend diseases.
- Supporting diseases by raw/trend criteria: Crohn disease, Hashimoto thyroiditis, MS, Sjogren syndrome, T1D, and ulcerative colitis.
- This breadth is useful as a **state marker**, but the residual analysis shows it is not a robust IFN-independent cross-disease mechanism.

## Confounders and why the signal may be artifact

1. **Generic IFN/APC confounding.** The target module overlaps conceptually and genetically with IFN-induced antigen presentation. Residualizing against `ifn_apc` is a harsh control because both modules share HLA/CD74 biology, but it is the right hostile test for the claim "CD74/HLA receptor state beyond generic IFN." Most disease signals fail that test.

2. **Module-composition artifact.** `mif_cd74_receptor_state` contains `CD74`, `CD44`, `CXCR4`, `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, and `HLA-DPB1`. A significant module does not imply CD74 receptor signaling. In MS white matter, CD74 alone is not significant while the composite module is.

3. **Cell-state versus cell-composition leakage.** Single-cell donor means can rise because a compartment contains more activated APC-like cells, not because each resident cell has entered a distinct CD74 receptor state. This is especially relevant for salivary gland epithelial preparations and T1D pancreatic ductal/acinar compartments, where inflamed samples may differ in immune proximity, dissociation survival, and epithelial stress.

4. **Sample-size and multiple-testing fragility.** The residual positives are nominal only. The best MS result has residual p=0.00789 but residual FDR=0.442 across 56 tests. Sjogren residual p=0.0734 and T1D CD74/HLA residual p=0.864 are not adequate for a central-node claim.

5. **Spatial and severity ambiguity.** The MS result is sorted microglia from white matter, not spatially anchored chronic active lesion rim microglia. It may reflect lesion burden, microglial activation stage, age/sex/region effects not fully captured by the model, or postmortem tissue context.

6. **No target-level genetics.** Current genetics is pathway-compatible through HLA/MHC and related IFN regulatory loci, but there is no acceptable cross-disease MR/colocalization for CD74, CIITA, RFX5, CTSS, IFNGR/JAK/STAT, or IFI30 as the intervention point.

7. **No direct perturbation in target disease cells.** Mixscale validates IFNGR/JAK/STAT/RFX5 wiring in a perturbation system, but there is no perturbation showing that CD74 receptor-state suppression in human MS microglia, Sjogren epithelium, or T1D ductal cells reverses disease-relevant outputs without broad IFN blockade.

## Therapeutic handles

Direct CD74/MIF or CD74/MIF-2 blockade:

- Mechanistically relevant to MS microglia/macrophage and monocyte biology.
- Not suitable as a new V3 intervention claim: heavily prior-arted in MS/EAE and autoimmune patent space; systemic CD74 targeting risks broad APC/B-cell biology.
- Possible use: comparator or enrichment marker for CD74/MIF-axis activity.

CIITA/RFX5/HLA-II transcriptional gate:

- Mechanistically sharper than direct IFNGR/JAK blockade because it gates MHC-II/CD74 output downstream of IFN.
- Druggability is weak for classic small molecules. Local ASO/siRNA/CRISPRi or promoter-IV-biased epigenetic repression is conceptually possible but not translationally mature.
- Current residual evidence is too narrow for cross-disease central-node status. Could be an assay handle in target-cell models.

PDE4/cAMP/PKA modulation:

- Plausible non-JAK route to lower CIITA/MHC-II induction. Existing drug class and local/topical delivery make it practical in gut or skin.
- Current local V3 audit is weak: PDE4/cAMP perturbagens exist in LINCS metadata, but no core PDE4/cAMP compounds appeared among the retrieved top L1000FWD opposite hits for V3 MS microglia signatures (`results_v3/pde4_camp_l1000_audit_summary.json`).
- Prior art in UC, psoriasis, and MS is substantial. Use only as a biomarker-stratified PD experiment, not as a novel CD74/HLA target claim.

CTSS / invariant-chain processing:

- Druggable and directly tied to CD74/MHC-II antigen processing.
- Poor fit for this residual question: CTSS changes peptide processing, not necessarily CD74/HLA expression or receptor-state biology. Existing Sjogren and broader autoimmune cathepsin-S work creates prior-art crowding.

SPPL2a / HLA-DM / CLIP-loading axis:

- Mechanistically adjacent to CD74 processing and MHC-II peptide loading.
- Not currently supported by V3 residual evidence and not obviously selective for pathogenic resident-cell states. Keep as mechanistic background, not a lead.

CD44/CXCR4 co-receptor axis:

- Present in the module and may matter for MIF/CD74 signaling context.
- Too broad and not anchored by the residual evidence. CXCR4 and CD44 have extensive biology in immune trafficking, repair, fibrosis, and cancer; direct targeting would not be CD74/HLA-state-selective.

## Prior art

Searches performed during this scout:

- PubMed / web: `CD74 MIF multiple sclerosis`, `CD74 MIF type 1 diabetes`, `CD74 Sjogren salivary epithelial`, `CIITA autoimmune inhibitor MHC class II`, `PDE4 cAMP CIITA IFN-gamma MHC class II`, `CD74 HLA-DR epithelial Sjogren`.
- Europe PMC API: same query families as above.
- ClinicalTrials.gov: milatuzumab SLE, ibudilast MS, apremilast UC, roflumilast psoriasis.
- Google Patents: `CD74 autoimmune`, `MIF CD74 multiple sclerosis`, `CIITA autoimmune MHC class II inhibitor`, `PDE4 ulcerative colitis CD74`.

Closest blocking or constraining prior art:

- CD74/MIF in MS/EAE is already a developed therapeutic axis. `DRalpha1`/MHC-II-derived constructs bind CD74 and inhibit MIF/D-DT signaling in EAE/MS-relevant models: https://pmc.ncbi.nlm.nih.gov/articles/PMC6364671/
- MIF/D-DT are reported as severity modifiers in male MS subjects and the axis has EAE support: https://pubmed.ncbi.nlm.nih.gov/28923927/
- MIF is necessary for EAE progression in prior mouse work: https://pubmed.ncbi.nlm.nih.gov/16237048/
- Patent prior art explicitly covers MIF/CD74/MS/EAE and CD74-binding peptides/constructs: https://patents.google.com/patent/US20170114117A1/en
- Anti-CD74 antibodies have autoimmune clinical/prior-art coverage. Milatuzumab was tested in active SLE (NCT01845740): https://clinicaltrials.gov/study/NCT01845740
- Anti-CD74 antibody/ADC patents explicitly list Sjogren syndrome, multiple sclerosis, diabetes mellitus, ulcerative colitis, Hashimoto thyroiditis, and other autoimmune diseases: https://patents.google.com/patent/WO2012104344A1/en
- Sjogren epithelial MHC-II expression is long-established, so the epithelial HLA/CD74 signal is not new as a disease biology observation: https://pubmed.ncbi.nlm.nih.gov/3501352/
- T1D CD74/MIF biology is also prior-arted through NOD/T1D macrophage and pancreatic tissue work: https://pmc.ncbi.nlm.nih.gov/articles/PMC5667746/
- CIITA/MHC-II inhibitor discovery for autoimmune disease is old patent territory, including isotype-specific CIITA-dependent transcription inhibition: https://patents.google.com/patent/US5672473
- cAMP/PKA inhibition of CIITA/MHC-II expression is established: https://pubmed.ncbi.nlm.nih.gov/11416140/ and https://pubmed.ncbi.nlm.nih.gov/8206755/
- PDE4 intervention is prior-arted in UC and MS. Apremilast UC phase 2: https://pubmed.ncbi.nlm.nih.gov/31926340/ and https://clinicaltrials.gov/study/NCT02289417. Ibudilast progressive MS: https://clinicaltrials.gov/study/NCT01982942 and slowly enlarging lesion analysis: https://pubmed.ncbi.nlm.nih.gov/38286755/
- Cathepsin-S inhibition has Sjogren-specific biocompartment prior art: https://doi.org/10.1186/s13075-019-1955-2

Prior-art conclusion: a new claim that "CD74/MIF", "anti-CD74", "CIITA/MHC-II inhibition", "PDE4 for UC/MS/psoriasis", or "CTSS in Sjogren/autoimmunity" is therapeutic would be blocked or heavily crowded. The only less-crowded angle is **patient/lesion stratification by IFN-residual CD74/HLA receptor-state score**, but current evidence only supports that as an exploratory biomarker.

## Recommendation for central-node status

Reject central-node status for residual CD74/HLA receptor-state biology in V3.

Rationale:

- It does not meet cross-disease residual breadth: MS is strong nominally, Sjogren is weak nominally, T1D ductal/acinar CD74/HLA residual support fails.
- It does not meet target specificity: the module is not CD74-specific and may be driven by HLA genes or CD44/CXCR4 context.
- It does not meet intervention tractability: the clean controllers are IFNGR/JAK/STAT/RFX5, which are broad or poorly druggable; narrower handles are prior-arted or weakly supported.
- It remains valuable as an enrichment and PD readout: MS chronic active lesion/microglial studies, Sjogren salivary epithelial studies, and T1D ductal/acinar studies can use this score to identify resident-cell APC-like states and to stratify response to existing or experimental modulators.

Recommended framing for the orchestrator:

> Residual CD74/HLA receptor-state score is a candidate **biomarker of IFN-adjacent resident-cell antigen-presentation stress**, not a validated pan-autoimmune causal mechanism or standalone therapeutic target.

## Exact next falsifying analysis

Run a component-resolved, leave-one-axis-out residual analysis in the existing MS, Sjogren, and T1D datasets before any further therapeutic synthesis.

Required tests:

1. Recompute donor/sample-level scores for four submodules:
   - HLA-II-only: `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`.
   - CD74-only: CD74 mean expression and CD74 detection fraction.
   - Receptor-only: `CD44`, `CXCR4`.
   - CD74-receptor without HLA: `CD74`, `CD44`, `CXCR4`.

2. For each target compartment (`GSE111972_white_matter`, `sjogren_gland_epithelial`, `t1d_ductal_cell`, `t1d_acinar_cell`), fit:

   `submodule_score ~ disease + ifn_apc + n_cells + available sample covariates`

   Use existing GSE111972 age/sex/region covariates for MS. For h5ad datasets, include donor-level `n_cells` and, if available in `.obs`, batch/site/library/sample covariates and immune-fraction or APC-proximity summaries.

3. Add a negative-control module matched for IFN responsiveness but unrelated to CD74/MHC-II receptor biology. The signal should not merely track the negative-control IFN module.

4. Falsification rule:
   - Demote permanently if CD74-only or CD74-receptor-without-HLA residual disease beta is not positive in at least **2 of 3 disease systems** (MS, Sjogren, T1D) with sign-stable effect and FDR <=0.10 within the component panel.
   - Demote permanently if the residual signal disappears when high-IFN or low-cell-count donors are leave-one-out removed.
   - Demote permanently if HLA-II-only explains the module while CD74-only and receptor-only fail; that means the current module is an HLA/APC marker, not CD74 receptor-state biology.

Wet-lab falsification after the in-silico test, only if the in-silico result survives:

- Use human iPSC-derived microglia, primary/organotypic salivary epithelial cultures, and pancreatic ductal/acinar organoid or slice models.
- Induce chronic IFN-gamma, then wash out IFN-gamma and perturb CD74/MIF, CIITA/RFX5, PDE4/cAMP, or CTSS separately.
- Falsify therapeutic relevance if the intervention reduces generic IFN/viability more than CD74/HLA receptor-state output, or if it fails to reduce CD74/HLA/CD44/CXCR4 state by at least 30% at non-toxic exposure while preserving antiviral ISG controls (`STAT1`, `IRF1`, `CXCL10`) within 80% of IFN-induced levels.
