# Wave79 Targetability Prior-Art and Directionality Sidecar

Date: 2026-05-27. Scope: hostile prior-art, druggability, and directionality scout for the non-LILRB shortlist `CD58`, `SPNS1`, `P4HB`, and `SEL1L3`. No code was edited. This is not a finding claim.

## Bottom line

Do not promote any of the four genes as a V3 therapeutic target on prior-art/directionality grounds, even if the next local audit is positive. `CD58` is the strongest evidence-bearing node, but the therapeutic direction is conflicted by MS genetics and blocked by alefacept/CD2-CD58 prior art. `SPNS1` is the most biologically interesting lysosomal-lipid node and has the best novelty profile, but it lacks MS target resolution, chemical matter, perturbation direction, and safety margin. `P4HB` is druggable but too generic and toxicology-prone. `SEL1L3` is too under-characterized for target promotion.

If local residualization is positive, retain only:

- `CD58` as a pharmacology/stratification comparator for CD2-CD58 biology, not a novel target.
- `SPNS1` as a preclinical lysosomal lipid-flux falsification lead, not a translational intervention point.

Close `P4HB` and `SEL1L3` as therapeutic target candidates unless the local audit produces an unexpectedly specific APC/myeloid perturbation and response-direction signal.

## Local evidence inspected

- `subagents_v3/wave75c_cross_disease_targetability_scout.md`
- `CONVERGENCE_CHECK_38.md`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/REPORT.md`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank.tsv`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/uniprot_accessibility.tsv`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/chembl_druggability.tsv`
- `results_v3/wave62_opentargets_target_resolution/REPORT.md`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_gate_matrix.tsv`
- `results_v3/wave71_global_survivor_meta_rank/REPORT.md`
- `results_v3/wave71_global_survivor_meta_rank/global_survivor_meta_rank.tsv`
- `subagents_v3/wave39b_accessibility_prior_art_critique.md`
- `subagents_v3/wave62v_opentargets_target_resolution.md`
- `subagents_v3/wave71a_global_survivor_meta_rank.md`
- `subagents_v3/wave78_lilrb_prior_art_directionality.md`

## External source checks

Searches were done for each gene plus autoimmune/MS, therapeutic modality, trial, patent, and toxicity terms. Verified sources used below include PubMed/PMC, ClinicalTrials.gov, FDA labeling, NCBI Gene, ChEMBL/Open Targets local captures, and Google Patents.

Key verified sources:

- CD58/MS genetics: De Jager et al., PNAS 2009, "The role of the CD58 locus in multiple sclerosis", PMID `19237575`, PMC `PMC2664005`, https://pmc.ncbi.nlm.nih.gov/articles/PMC2664005/
- Later CD58 expression direction: PLOS Genetics 2019, "A genetic variant associated with multiple sclerosis inversely affects the expression of CD58 and microRNA-548ac from the same gene", PMC `PMC6382214`, https://pmc.ncbi.nlm.nih.gov/articles/PMC6382214/
- Alefacept mechanism/label: FDA label, https://www.accessdata.fda.gov/drugsatfda_docs/label/2003/alefbio013003LB.htm; NCI drug dictionary, https://www.cancer.gov/publications/dictionaries/cancer-drug/def/alefacept
- Alefacept T1D trial: ClinicalTrials.gov `NCT00965458`, https://clinicaltrials.gov/study/NCT00965458; T1DAL PubMed `24622414`, https://pubmed.ncbi.nlm.nih.gov/24622414/
- CD2-CD58 autoimmune patent: `US20200347136A1`, https://patents.google.com/patent/US20200347136A1/en
- SPNS1 lysosomal lipid transport: PubMed `37075117`, https://pubmed.ncbi.nlm.nih.gov/37075117/; PubMed `39739806`, https://pubmed.ncbi.nlm.nih.gov/39739806/
- SPNS1 gene/function: NCBI Gene `83985`, https://www.ncbi.nlm.nih.gov/gene/83985
- P4HB/cell-surface PDI and T-cell migration: PubMed `21670307`, https://pubmed.ncbi.nlm.nih.gov/21670307/
- PDI inhibition clinical precedent: PubMed `30652973`, https://pubmed.ncbi.nlm.nih.gov/30652973/; trial `NCT02195232`, https://clinicaltrials.gov/study/NCT02195232
- PDI inhibitor patents: `EP4203894A1`, https://patents.google.com/patent/EP4203894A1/en; `US20160145209A1`, https://patents.google.com/patent/US20160145209A1/en
- SEL1L3 gene/function: NCBI Gene `23231`, https://www.ncbi.nlm.nih.gov/gene/23231

## Per-gene audit

| Gene | Plausible modality and direction | Local support | Blocking prior art or toxicity | Remains promotable if local audit is positive? |
|---|---|---|---|---|
| `CD58` | Modality: biologic or small protein/peptide inhibitor of CD2-CD58 interaction; alefacept-like CD58-Fc/CD2 targeting is the precedent. Disease-expression direction would suggest blockade if high `CD58` marks pathogenic APC/T-cell synapse activity. MS-genetic direction argues the opposite: protective higher CD58/restored CD58 may be beneficial, so systemic blockade is directionally unsafe for MS. | Wave71 top non-reopener; Wave62 MS L2G `0.951`, same-target QTL in Crohn/MS, module-link true; broad h5ad positives Crohn/T1D/UC. Wave34 parks for missing perturbation/model and not-currently-druggable cell-state proof. | Direct prior art: alefacept was an FDA-approved CD58/LFA-3-Fc psoriasis biologic and tested in new-onset T1D. `US20200347136A1` explicitly covers constrained cyclic peptides inhibiting CD2:CD58 for autoimmune/inflammatory disease. Safety/direction risks include T-cell depletion/immunosuppression and conflict with CD58-protective MS genetics. | No as a novel therapeutic target. If local audit is positive, keep as a benchmark or stratification comparator only. A positive local signal would mostly say "CD2-CD58 biology is present in this cell state", not "new intervention available". |
| `SPNS1` | Modality: future small-molecule/allosteric transporter modulator or genetic perturbation tool. Direction should default to restoration/preservation of SPNS1 lysosomal lysophospholipid efflux, not inhibition, because deficiency impairs lipid salvage/autophagy and can produce lysosomal-storage-like biology. Local disease-upregulation could be compensatory, not pathogenic. | Wave39 positive in 4 diseases (`Crohn`, `Sjogren`, `psoriasis`, `T1D`) and identifies a lysosomal membrane/transporter protein. Wave62 gives `NO_GO_WAVE62_TARGET_RESOLUTION`: no MS L2G, no relevant QTL, no cross-disease coloc, no druggability. ChEMBL exact target not found locally. | No strong direct autoimmune prior-art blocker found, which is a novelty advantage. The blocker is translational: no chemical matter, no target-level genetics, no MS anchor, ubiquitous lysosomal survival biology, and deficiency data pointing toward harm from inhibition. | Not as a therapeutic target. Yes only as a preclinical discovery lead if the local audit shows MS-positive APC/myeloid residual signal and a direct perturbation experiment shows that SPNS1 restoration normalizes lysosomal/APC inflammation without killing cells. |
| `P4HB` | Modality: small-molecule extracellular protein disulfide isomerase/PDI inhibitor. Plausible direction: inhibit extracellular/cell-surface PDI if it drives T-cell migration, platelet/coagulation, or inflammatory redox signaling. But ER/chaperone biology argues against broad inhibition and disease expression can reflect ER stress/injury. | Wave39 top surfaceome-rescue row by score, accessible/catalytic, ChEMBL exact target `CHEMBL5422`, 702 activity rows, best returned value `3 nM`; positive in Crohn/Sjogren/psoriasis/UC. However no MS anchor and Wave71 has only a causal-proxy no-go. | PDI inhibitors are already an active chemistry/clinical area, especially thrombosis/cancer-associated hypercoagulability. Isoquercetin/PDI clinical work (`NCT02195232`, PMID `30652973`) and PDI inhibitor patents crowd the modality. Toxicology/selectivity risks are high because P4HB is an essential ER folding enzyme and extracellular PDI regulates platelets/coagulation. | No. Even a positive local audit is likely to mean generic ER stress, tissue injury, or redox/coagulation biology. Promote only if an unexpectedly narrow extracellular APC/T-cell PDI mechanism appears with MS support, which current artifacts do not show. |
| `SEL1L3` | Modality: theoretical antibody/surface handle only. Direction is unknown; no ligand, pathway, catalytic function, or validated immune mechanism was found in this pass. | Broad h5ad MS-positive rank shows Crohn/T1D/UC positives plus MS white-matter delta `0.923`, p `0.018`, but FDR `0.837`. Wave39 calls it accessible membrane but `NO_GO_SURFACEOME_RESCUE`. Wave62 has no target-resolution support and no druggability. Local signal is largely stromal/endothelial/epithelial rather than clean APC/myeloid. | No direct autoimmune prior-art blocker found. The blocker is absence of target biology: NCBI describes predicted membrane localization, broad expression, and SEL1-like repeats, but no actionable immune mechanism. No ChEMBL target/matter locally. | No as a target. If local audit is positive, retain at most as a localization/biomarker clue; do not route into intervention discovery without ligand/function and perturbation data. |

## Directionality conclusions

`CD58` is a directionality trap. Local expression recurrence and CD2-CD58 blockade history point toward inhibition, while MS genetics and remission biology suggest that higher/restored CD58 can be protective. The same molecule cannot be promoted until the cell type and direction are resolved experimentally.

`SPNS1` has coherent module biology but no intervention. The safest mechanistic hypothesis is not "inhibit SPNS1"; it is "loss or insufficiency of SPNS1-mediated lysosomal lysophospholipid export may contribute to maladaptive lipid/APC states." That hypothesis would require restoration biology, not conventional inhibitor discovery.

`P4HB` has chemical matter but fails specificity. It is an accessible enzyme in many stress and coagulation contexts; a cross-autoimmune expression signal is not enough to separate useful extracellular PDI modulation from harmful ER/chaperone interference.

`SEL1L3` has neither direction nor mechanism. Treat it as a marker until a ligand, pathway, or perturbation result exists.

## Exact pivot recommendation

1. Do not run another broad targetability re-rank from expression recurrence.
2. If a local Wave80 audit is run, limit it to `CD58` and `SPNS1`.
3. For `CD58`, run only a falsification audit:
   - residualize in APC/myeloid compartments against T/NK/CD2 admixture, HLA-II/CD74, IFN/APC, lysosome/APC, cell-count, and generic inflammation;
   - require MS plus at least two non-MS APC/myeloid diseases after residualization;
   - require response-direction consistency in GSE282122 and GSE198520 beyond generic inflammation;
   - close if the signal is T-cell-admixture driven or if therapeutic direction remains blockade despite MS-protective higher-CD58 genetics.
4. For `SPNS1`, run only a biology-validation audit:
   - require nominal MS support and at least three residual APC/myeloid disease contexts;
   - require localization to macrophage/DC/microglia-like compartments rather than epithelium/stroma;
   - if positive, move to CRISPRa/CRISPRi plus lipidomics design in primary human macrophages/DCs; do not claim druggability.
5. Close `P4HB` and `SEL1L3` now for V3 therapeutic promotion unless the user explicitly wants marker discovery rather than intervention discovery.
6. Main V3 route should pivot away from this shortlist toward either:
   - perturbation-first targets with real autoimmune reversal data and non-conflicted direction, or
   - a stratification claim where CD58/lysosomal-APC state is used only as a biomarker, not as the drug target.

## Final sidecar call

`NO_PROMOTION_FOR_TARGETABILITY_SHORTLIST`.

`CD58`: `PARK_PRIOR_ART_DIRECTIONALITY`; benchmark/stratification comparator only.

`SPNS1`: `PARK_PRECLINICAL_LYSOSOMAL_LIPID_FLUX_LEAD`; no translational target claim.

`P4HB`: `NO_GO_GENERIC_ER_REDox_PDI_TOXICITY_PRIOR_ART`.

`SEL1L3`: `NO_GO_UNCHARACTERIZED_MARKER_NO_MODALITY`.
