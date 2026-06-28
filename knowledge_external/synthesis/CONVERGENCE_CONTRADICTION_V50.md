# V50 Convergence / Contradiction Reassessment

Status: external-layer synthesis. This updates the V48/V49 convergence matrix
after adding sharper, source-specific external records for DMF treatment
response, ZMIZ1, chr1 KIF21B/GPR25, and GPR25 tractability.

Boundary rule: all external rows below remain external-layer context or
corroboration only. The project artifacts remain the evidence, and no external
record changes a grounded finding, locked rule, or pre-registration. Source:
`docs/knowledge/EPISTEMIC_CLASSES.md`.

## Summary

Compared with V48/V49:

- V48 relationship rows: `23`
- V48 convergences asserted: `7`
- V48 contradictions flagged: `0`
- V48 insufficient-overlap/context rows: `16`

After V50 sharper-source acquisition:

- original high-priority gap rows revisited so far: `7` of `16`
- newly added source-specific external records assessed here: `24`
- decision-relevant new convergences: `11`
- genuine contradictions surfaced: `0`
- source-specific confounder-scope context records added without changing the
  V22 rule-corroboration count: `6`
- high-priority rows that remain non-corroborating despite sharper context:
  `2` (`bounded V22 scalar`, `V22 immune-tone/confounder audit`)

Main result: V50 materially sharpens the genetics and APC-axis external layer.
ZMIZ1 now has a direct source-specific external convergence record for opposite
MS/Crohn allele direction; chr1 now has source-specific support for real MS locus
context plus GPR25 tractability caution; and the coupled APC-axis row now has
source-specific CD74/MIF/HLA-II plausibility context instead of generic MSGD
metadata. The treatment-response records are much more specific than the DMF
drug label, but they still do not independently assert the frozen V22 APC/HLA-II
scalar or its confounder audit. They therefore remain validation-context
records, not external corroboration of the rule.
Sharper EBV records also improve mechanistic context but still do not test the
project's autoimmune-specific IFN/APC imprint controls.
IBD treatment-response records now provide direct Crohn interferon-module
response context, with an explicit external caution that baseline transcriptome
differences were not sufficiently sensitive as a clinical predictor.
PTGER4 now has a source-specific same-rsid MS/Crohn opposite-allele record and
Crohn-side expression-modulation context, strengthening the project's closure of
naive PTGER4 transfer.
V50 also added six steroid/glucocorticoid and leukocyte-composition records.
These sharpen why the V32 confounder audit was necessary, but they do not
externally corroborate the project-specific result that the locked V22 scalar is
immune-tone bounded rather than explained by steroid or composition effects.

## Decision-Relevant New Convergences

- Grounded: `ZMIZ1 opposite-direction MS/Crohn decoupling` (supported; source
  artifact: `docs/workups/genetics/GENETICS_EQTL_WORKUP_V16.md`;
  `docs/history/LEAD_INVENTORY_V29.md`). External:
  `claim.gwas_catalog.zmiz1_rs1250550_ms_crohn_opposite_alleles.2026-06-28`
  (source:
  https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs1250550&projection=associationBySnp).
  Status:
  `CORROBORATION_FROM_INDEPENDENT_SOURCE`. The external GWAS Catalog rows
  preserve the same rsid with MS and Crohn risk alleles in opposite allelic
  directions. This aligns with the project's ZMIZ1 decoupling result; the
  project artifact remains the evidence, and allele-harmonized rerun remains a
  future grounding task.
- Grounded: `chr1 KIF21B/GPR25 locus resolves to real biology but hard target`
  (supported; source artifact:
  `docs/workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md`). External:
  `claim.gwas_catalog.chr1_rs7522462_kif21b_gpr25_ms.2026-06-28`
  (source:
  https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs7522462&projection=associationBySnp).
  Status:
  `CORROBORATION_FROM_INDEPENDENT_SOURCE`. The external record converges on a
  real MS chr1q32.1 association overlapping the project's locus, while keeping
  causal-gene ambiguity visible.
- Grounded: `chr1 KIF21B/GPR25 locus resolves to real biology but hard target`
  (supported; source artifact:
  `docs/workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md`). External:
  `claim.jmg_2010.kif21b_ms_susceptibility_replication.2026-06-28`
  (source: https://pubmed.ncbi.nlm.nih.gov/20587413/). Status:
  `CORROBORATION_FROM_INDEPENDENT_SOURCE`. The external literature context
  independently supports KIF21B as a real susceptibility-locus context, but not
  as a direction-matched drug target.
- Grounded: `GPR25 demoted from protected favorite` (negative-established;
  source artifact: `docs/workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md`).
  External: `claim.iuphar.gpr25_orphan_gpcr_context.2026-06-28`
  (source: https://www.guidetopharmacology.org/services/targets?name=GPR25).
  Status:
  `CORROBORATION_FROM_INDEPENDENT_SOURCE`. The external target record supports
  the project's caution that GPR25 target-class appeal does not equal a
  direction-matched MS intervention.
- Grounded: `Coupled APC remodeling architecture` (supported; source artifact:
  `docs/workups/deep_structure/DEEP_STRUCTURE_V26.md`). External:
  `claim.eji_2018.mif_cd74_bcell_ms_context.2026-06-28` (source:
  https://pubmed.ncbi.nlm.nih.gov/30160778/). Status:
  `CORROBORATION_FROM_INDEPENDENT_SOURCE`. The external MS B-cell source
  independently places MIF, CD74, and CXCR4 in an MS immune-cell state context,
  supporting the plausibility of the MIF-CD74 arm of the project axis without
  validating the full coupled architecture.
- Grounded: `Coupled APC remodeling architecture` (supported; source artifact:
  `docs/workups/deep_structure/DEEP_STRUCTURE_V26.md`). External:
  `claim.ncbi_gene.cd74_mhc2_mif_molecular_context.2026-06-28` (source:
  https://www.ncbi.nlm.nih.gov/gene/972). Status:
  `CORROBORATION_FROM_INDEPENDENT_SOURCE`. The external annotation independently
  places CD74 at the intersection of MHC-II antigen presentation and MIF receptor
  biology, matching the molecular bridge implied by the project axis.
- Grounded: `Coupled APC remodeling architecture` (supported; source artifact:
  `docs/workups/deep_structure/DEEP_STRUCTURE_V26.md`). External:
  `claim.jimmunol_2014.hla_dra1_cd74_mif_eae_context.2026-06-28` (source:
  https://pubmed.ncbi.nlm.nih.gov/24683185/). Status:
  `CORROBORATION_FROM_INDEPENDENT_SOURCE`. The external EAE source links
  HLA-DR, CD74, and MIF in CNS autoimmune model biology, strengthening
  mechanistic plausibility while remaining outside project-grounded human MS
  evidence.
- Grounded: `Crohn downstream IFN/APC convergence exceeds genetic proximity`
  (supported; source artifact: `docs/findings/AXIS_DISAGREEMENT_FINDINGS_V12.md`;
  `docs/findings/KILL_HYP_V6_006.md`). External:
  `claim.jcc_2024.crohn_pants_antitnf_interferon_modules.2026-06-28`
  (source: https://pubmed.ncbi.nlm.nih.gov/37776235/). Status:
  `CORROBORATION_FROM_INDEPENDENT_SOURCE_WITH_PREDICTION_CAVEAT`. The external
  Crohn anti-TNF blood transcriptome source independently supports
  interferon-related treatment-response biology, while warning that baseline
  expression alone was not clinically predictive enough.
- Grounded: `Layer-specific autoimmune transfer-validity map` (supported;
  source artifact: `docs/findings/AXIS_DISAGREEMENT_FINDINGS_V12.md`). External:
  `claim.nat_immunol_2024.imid_antitnf_single_cell_atlas.2026-06-28` (source:
  https://pubmed.ncbi.nlm.nih.gov/39438660/). Status:
  `CORROBORATION_FROM_INDEPENDENT_SOURCE`. The external single-cell atlas
  independently supports cross-disease cellular treatment-response mapping as a
  valid layer, without validating any specific project module.
- Grounded: `PTGER4 mixed shared/distinct signal closes naive transfer`
  (negative-established; source artifact: `docs/reports/FINDINGS_REPORT_V37.md`).
  External:
  `claim.gwas_catalog.ptger4_rs4613763_ms_crohn_opposite_alleles.2026-06-28`
  (source:
  https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs4613763&projection=associationBySnp).
  Status: `CORROBORATION_FROM_INDEPENDENT_SOURCE`. The external same-rsid rows
  preserve opposite MS/Crohn risk alleles at PTGER4, supporting the project's
  naive-transfer closure.
- Grounded: `PTGER4 mixed shared/distinct signal closes naive transfer`
  (negative-established; source artifact: `docs/reports/FINDINGS_REPORT_V37.md`).
  External: `claim.plos_genet_2007.ptger4_crohn_expression_modulation.2026-06-28`
  (source: https://pubmed.ncbi.nlm.nih.gov/17447842/). Status:
  `CORROBORATION_FROM_INDEPENDENT_SOURCE`. The external Crohn-side expression
  modulation source supports signal-specific PTGER4 biology while not implying
  direction-matched MS transfer.

## Contradictions Flagged

- None in this V50 pass. The sharper records add specific convergence and one
  causal-gene ambiguity note, but no external source directly contradicts a
  grounded finding under the same definition. The chr1 rs7522462 row preserves
  a useful tension, not a contradiction: external author-gene and local-context
  fields mention C1orf106/KIF21B/GPR25 in different ways, which reinforces the
  project's caution around causal-gene assignment rather than refuting it.

## Revisited Gap Rows

| original gap | new external record | class / marker | source | relationship | status | interpretation |
|---|---|---|---|---|---|---|
| Bounded APC/HLA-II early treatment-response monitoring scalar | `claim.gafson_2018.dmf_pbmc_neda4_transcriptome_context.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://pmc.ncbi.nlm.nih.gov/articles/PMC6168332/ | `insufficient-overlap` | `SPECIFIC_VALIDATION_CONTEXT_NOT_RULE_CORROBORATION` | This source matches the paired DMF PBMC/NEDA-4 validation setting, but it does not independently assert the locked APC/HLA-II scalar or threshold. It is validation-context, not external evidence for the rule. |
| Bounded APC/HLA-II early treatment-response monitoring scalar | `claim.carlstrom_2019.dmf_monocyte_ros_response_context.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://www.nature.com/articles/s41467-019-11139-3 | `orthogonal` | `SPECIFIC_DMF_RESPONSE_BUT_DIFFERENT_MARKER` | This source sharpens DMF response monitoring context but uses monocyte/ROS response biology, not the project APC/HLA-II scalar. |
| Bounded APC/HLA-II early treatment-response monitoring scalar | `claim.sanchez_sanz_2023.dmf_pbmc_response_signature_context.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://www.omicsdi.org/dataset/geo/GSE235357 | `insufficient-overlap` | `POTENTIALLY_GROUNDABLE_DATASET_CONTEXT` | This source is closer than a drug label because it has PBMC transcriptomic response context, but the project has not ingested the data under the frozen harness. |
| Bounded APC/HLA-II early treatment-response monitoring scalar | `claim.diebold_2022.dmf_high_dimensional_immune_monitoring_context.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://www.pnas.org/doi/10.1073/pnas.2205042119 | `orthogonal` | `SPECIFIC_IMMUNE_MONITORING_BUT_DIFFERENT_READOUT` | This source supports high-dimensional DMF immune monitoring as a field context, but it does not test the locked scalar. |
| V22 scalar is immune-tone bounded, not steroid/composition artifact | `claim.gafson_2018.dmf_pbmc_neda4_transcriptome_context.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://pmc.ncbi.nlm.nih.gov/articles/PMC6168332/ | `insufficient-overlap` | `CONFOUNDER_AUDIT_REMAINS_PROJECT_SPECIFIC` | The source may eventually support a frozen validation run, but the external record itself does not score glucocorticoid, composition, metabolic, STAT1, batch, or immune-tone confounders. |
| Coupled APC remodeling architecture | `claim.eji_2018.mif_cd74_bcell_ms_context.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://pubmed.ncbi.nlm.nih.gov/30160778/ | `converges` | `CORROBORATION_FROM_INDEPENDENT_SOURCE` | The source-specific external record supports MS B-cell MIF/CD74/CXCR4 context, but does not independently reproduce the full V26 coupled-axis structure. |
| Coupled APC remodeling architecture | `claim.ncbi_gene.cd74_mhc2_mif_molecular_context.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://www.ncbi.nlm.nih.gov/gene/972 | `converges` | `CORROBORATION_FROM_INDEPENDENT_SOURCE` | The source-specific external record supports CD74 as a molecular bridge between MHC-II antigen presentation and MIF receptor biology. |
| Coupled APC remodeling architecture | `claim.jimmunol_2014.hla_dra1_cd74_mif_eae_context.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://pubmed.ncbi.nlm.nih.gov/24683185/ | `converges` | `CORROBORATION_FROM_INDEPENDENT_SOURCE` | The source-specific external record links HLA-DR, CD74, and MIF in an EAE model; this strengthens plausibility, not human MS validation. |
| ZMIZ1 opposite-direction MS/Crohn decoupling | `claim.gwas_catalog.zmiz1_rs1250550_ms_crohn_opposite_alleles.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs1250550&projection=associationBySnp | `converges` | `CORROBORATION_FROM_INDEPENDENT_SOURCE` | The source-specific external rows directly address the direction-dependent finding and converge with the project result, pending future allele-harmonized grounding. |
| ZMIZ1 opposite-direction MS/Crohn decoupling | `claim.hmg_2019.zmiz1_dendritic_vitamin_d_context.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://academic.oup.com/hmg/article/28/2/269/5115479 | `orthogonal` | `MECHANISTIC_CONTEXT_NOT_DIRECTION_TEST` | This source adds immune-cell/vitamin-D mechanistic context around ZMIZ1, but it is not a direct MS/Crohn allele-direction test. |
| chr1 KIF21B/GPR25 locus resolves to real biology but hard target | `claim.gwas_catalog.chr1_rs7522462_kif21b_gpr25_ms.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs7522462&projection=associationBySnp | `converges` | `CORROBORATION_FROM_INDEPENDENT_SOURCE` | The external row converges on a real MS chr1 locus and keeps causal-gene ambiguity explicit, aligning with the project hard-target interpretation. |
| chr1 KIF21B/GPR25 locus resolves to real biology but hard target | `claim.jmg_2010.kif21b_ms_susceptibility_replication.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://pubmed.ncbi.nlm.nih.gov/20587413/ | `converges` | `CORROBORATION_FROM_INDEPENDENT_SOURCE` | The external record supports KIF21B susceptibility-locus context but does not promote KIF21B to intervention-grade status. |
| GPR25 demoted from protected favorite | `claim.iuphar.gpr25_orphan_gpcr_context.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://www.guidetopharmacology.org/services/targets?name=GPR25 | `converges` | `CORROBORATION_FROM_INDEPENDENT_SOURCE` | The external record supports the demotion logic: GPR25 being a GPCR is not enough when it remains orphan/emerging-pharmacology and direction is unresolved. |
| EBV/IFN APC imprint downgraded by specificity control | `claim.nature_2022.ebna1_glialcam_crossreactive_bcells_ms.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://pubmed.ncbi.nlm.nih.gov/35073561/ | `orthogonal` | `EBV_MS_MECHANISM_NOT_APC_SPECIFICITY_TEST` | The source supports EBV-linked B-cell molecular mimicry context in MS, but it does not test whether the project's EBV/IFN APC imprint is specific versus autoimmune comparators. |
| EBV/IFN APC imprint downgraded by specificity control | `claim.biorxiv_2026.ebv_anti_cns_bcell_apc_ms_context.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://pubmed.ncbi.nlm.nih.gov/41727017/ | `orthogonal` | `PREPRINT_EBV_APC_CONTEXT_NOT_GROUNDED_SPECIFICITY` | The source is closer to the EBV/APC hypothesis than generic EBV-risk literature, but preprint status and no project rerun keep it as context; it does not overturn the specificity-control downgrade. |
| Crohn downstream IFN/APC convergence exceeds genetic proximity | `claim.jcc_2024.crohn_pants_antitnf_interferon_modules.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://pubmed.ncbi.nlm.nih.gov/37776235/ | `converges` | `CORROBORATION_FROM_INDEPENDENT_SOURCE_WITH_PREDICTION_CAVEAT` | The source overlaps Crohn treatment response and interferon-related blood modules; it converges with downstream response-layer biology while warning that baseline expression differences were not sufficiently sensitive for clinical prediction. |
| Layer-specific autoimmune transfer-validity map | `claim.nat_immunol_2024.imid_antitnf_single_cell_atlas.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://pubmed.ncbi.nlm.nih.gov/39438660/ | `converges` | `CORROBORATION_FROM_INDEPENDENT_SOURCE` | The source supports cross-disease cellular treatment-response mapping as a distinct layer, consistent with the project's transfer-validity map. |
| PTGER4 mixed shared/distinct signal closes naive transfer | `claim.gwas_catalog.ptger4_rs4613763_ms_crohn_opposite_alleles.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs4613763&projection=associationBySnp | `converges` | `CORROBORATION_FROM_INDEPENDENT_SOURCE` | Same-rsid external rows preserve opposite MS/Crohn PTGER4 risk alleles, supporting transfer caution rather than a shared-direction target claim. |
| PTGER4 mixed shared/distinct signal closes naive transfer | `claim.plos_genet_2007.ptger4_crohn_expression_modulation.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://pubmed.ncbi.nlm.nih.gov/17447842/ | `converges` | `CORROBORATION_FROM_INDEPENDENT_SOURCE` | The source supports Crohn-side PTGER4 regulatory biology but does not rescue PTGER4 as a direction-matched MS target. |

## Treatment-Response Confounder Context Added In Task 20

These records are source-specific context for the V32 audit design. They support
the need to score steroid and composition confounders, but they do not validate
the locked V22 scalar or the V32 survival/attenuation result.

| project item | new external record | class / marker | source | relationship | status | interpretation |
|---|---|---|---|---|---|---|
| V22 scalar is immune-tone bounded, not steroid/composition artifact | `claim.jneurol_2004.methylprednisolone_ms_immune_gene_suppression.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://link.springer.com/article/10.1007/s00415-004-0516-y | `context` | `CONFIRMS_CONFOUNDER_CLASS_NOT_AUDIT_RESULT` | Steroid therapy can reshape MS blood immune-expression signals, supporting glucocorticoid scoring as a required validation guard. It does not test the V22 scalar. |
| V22 scalar is immune-tone bounded, not steroid/composition artifact | `claim.cns_neurosci_ther_2024.glucocorticoid_resistance_ms_whole_blood.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://pmc.ncbi.nlm.nih.gov/articles/PMC10848073/ | `context` | `CONFIRMS_CONFOUNDER_CLASS_NOT_AUDIT_RESULT` | Whole-blood transcriptomic glucocorticoid-response heterogeneity reinforces steroid-response confounding risk in MS relapse biology. It does not evaluate the project score. |
| V22 scalar is immune-tone bounded, not steroid/composition artifact | `claim.biopha_2024.methylprednisolone_b_t_cell_transcriptome_ms.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://pubmed.ncbi.nlm.nih.gov/38749180/ | `context` | `POTENTIALLY_GROUNDABLE_STEROID_PANEL_DATA` | Cell-type-specific B-cell and T-helper-cell methylprednisolone transcriptomes are a concrete future route to test or refine steroid-response panels. No V22 adjustment result follows until rerun. |
| V22 scalar is immune-tone bounded, not steroid/composition artifact | `claim.sci_rep_2018.dmf_persistent_immune_composition_ms.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://www.nature.com/articles/s41598-018-26519-w | `context` | `CONFIRMS_COMPOSITION_CONFOUNDER_CLASS_NOT_AUDIT_RESULT` | Persistent DMF-associated immune-cell composition shifts support the need for composition diagnostics and deconvolution in validation. They do not explain or validate the V22 scalar. |
| V22 scalar is immune-tone bounded, not steroid/composition artifact | `claim.plos_one_2020.dmf_leukocyte_response_patient_factors_ms.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://pubmed.ncbi.nlm.nih.gov/32045436/ | `context` | `CONFIRMS_COMPOSITION_DIAGNOSTIC_NEED_NOT_AUDIT_RESULT` | Leukocyte-count and neutrophil-lymphocyte-ratio modulation supports simple composition diagnostics alongside transcriptomic validation. It does not test V22. |
| V22 scalar is immune-tone bounded, not steroid/composition artifact | `claim.mult_scler_2017.dmf_response_lymphocyte_subsets_ms.2026-06-28` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://journals.sagepub.com/doi/10.1177/1352458517703799 | `context` | `CONFIRMS_RESPONSE_LINKED_SUBSET_SHIFT_NOT_AUDIT_RESULT` | Response-linked lymphocyte-subset changes sharpen the cell-composition risk around DMF response work. They do not validate the project scalar. |

## Updated Decision List

Externally corroborated grounded findings added by V50:

1. `ZMIZ1 opposite-direction MS/Crohn decoupling`
2. `chr1 KIF21B/GPR25 locus resolves to real biology but hard target`
3. `GPR25 demoted from protected favorite`
4. `Coupled APC remodeling architecture`
5. `Crohn downstream IFN/APC convergence exceeds genetic proximity`
6. `PTGER4 mixed shared/distinct signal closes naive transfer`

Rows still needing sharper same-definition sources or future grounding:

1. `Bounded APC/HLA-II early treatment-response monitoring scalar`: now has
   validation-context sources, but still no external record that independently
   tests the frozen scalar.
2. `V22 scalar is immune-tone bounded, not steroid/composition artifact`: still
   project-specific until a real validation cohort is ingested and adjusted
   through the pre-registered harness.
3. `Coupled APC remodeling architecture`: now has source-specific molecular and
   MS B-cell plausibility records, but still needs direct human multi-modality
   grounding outside the project's own data before it can be externally
   validated.
4. `T/B-readable early IFN/APC/STAT1 monitoring state`: still needs
   compartment-resolved treatment-response data or literature.
5. `EBV/IFN APC imprint downgraded by specificity control`: still needs
   EBV-stratified expression sources with autoimmune comparators.

## Future Grounding Actions

- Queue an allele-harmonized ZMIZ1 rs1250550 comparison using imported GWAS
  Catalog rows and the project's MS/Crohn direction framework. This is a future
  grounding route; no conclusion changes until rerun.
- Keep the chr1 locus classified as real but not intervention-grade unless a
  future record supplies direction-matched KIF21B/GPR25 functional and
  pharmacological evidence.
- Treat Gafson 2018 and GSE235357 as validation-data routes, not literature
  corroboration. They should enter only through the frozen V42/V44 harness and
  associated quarantine rules.
- Treat steroid/glucocorticoid and leukocyte-composition sources as validation
  guard context. They strengthen the pre-specified need for confounder scoring,
  but do not change the V32 verdict until rerun on a validation cohort.
- Treat the CD74/MIF/HLA-II sources as mechanistic context only. A future
  external-validation route would need independent human MS cell-state data that
  jointly scores HLA-II/IFN-APC and MIF-CD74 structure under the V26 axis
  definitions.
- Treat EBV mechanistic and preprint sources as context only until an accessible
  dataset can test EBV-linked IFN/APC module behavior against non-MS autoimmune
  comparators under the project's predefined specificity controls.
- Treat the PANTS Crohn source as response-layer corroboration with a biomarker
  caution: it supports IFN-related treatment-response biology but warns against
  naive clinical prediction from baseline expression alone.
- Treat PTGER4 external records as stronger support for transfer caution, not
  for reactivation. Same-rsid opposite alleles and Crohn-side expression
  modulation preserve the need for direction-matched grounding before any target
  claim.
